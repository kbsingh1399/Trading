"""Frozen breakout/retest order-flow system, with a causal portfolio backtest.

Standalone research implementation of docs/specs/altcoin_inefficiency_strategy_20260915.md.
Requires numpy, pandas and pyarrow. Never submits exchange orders.
CLI defaults to sequential quarterly evaluation, stopping at the first failure.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

BAR = 900_000
DAY = 86_400_000
H4 = 16 * BAR
BTC = "BTCUSDT"
ALTS = tuple(s + "USDT" for s in "ETH XRP SOL BNB DOGE ADA TRX LINK AVAX SUI NEAR DOT LTC BCH APT OP ARB".split())
INPUTS = ["open_time_ms", "open", "high", "low", "close", "volume_base", "volume_quote",
          "future_cvd_15m", "spot_cvd_15m", "funding_rate_pct"]


@dataclass(frozen=True)
class Config:
    capital: float = 5000.0
    risk: float = 50.0
    max_positions: int = 2
    leverage_cap: float = 3.0
    cost: float = 0.0041
    cost_multiplier: float = 1.0
    warmup_15m: int = 4000
    warmup_4h: int = 1000
    lookback: int = 96
    volume_ratio: float = 1.5
    flow_threshold: float = 0.10
    retest_bars: int = 4
    retest_buffer_atr: float = 0.25
    max_entry_gap_atr: float = 0.5
    target_r: float = 4.0
    runner_r: float = 6.0
    target_atr_cap: float = 3.0
    max_hold_bars: int = 288
    decay_bars: int = 24
    cooldown: int = 16
    daily_stop_usd: float = 100.0
    circuit_fraction: float = 0.04
    funding_mode: str = "estimated_8h"
    use_flow: bool = True
    use_retest: bool = True

    def __post_init__(self):
        if self.capital != 5000 or self.risk != 50 or self.max_positions != 2:
            raise ValueError("The fixed capital/risk/capacity contract cannot be relaxed")
        if self.target_r < 4 or self.cost < 0.0041 or self.cost_multiplier < 1:
            raise ValueError("The 4R target and 41bps cost minimum cannot be relaxed")
        if not 1 <= self.max_hold_bars <= 288:
            raise ValueError("Holding deadline must be at most 72h")
        if self.funding_mode not in ("estimated_8h", "transaction_only"):
            raise ValueError("Unknown funding model")


def ms(value):
    return int(pd.Timestamp(value, tz="UTC").value // 1_000_000)


def iso(t):
    return pd.Timestamp(int(t), unit="ms", tz="UTC").isoformat()


def write_json(path, obj):
    def clean(v):
        if isinstance(v, dict):
            return {str(k): clean(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [clean(x) for x in v]
        if isinstance(v, (np.integer, np.bool_)):
            return v.item()
        if isinstance(v, (float, np.floating)):
            return float(v) if math.isfinite(v) else None
        return v
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(clean(obj), indent=2, allow_nan=False), encoding="utf-8")


def ema(s, period):
    a = 2/(period+1)
    result = np.empty(len(s))
    if len(s):
        result[0] = round(float(s.iloc[0]), 8)
        for i in range(1, len(s)):
            result[i] = round(a*float(s.iloc[i])+(1-a)*result[i-1], 8)
    return pd.Series(result, index=s.index)


def atr(f, period=14):
    c = f.close.shift()
    tr = pd.concat([f.high-f.low, (f.high-c).abs(), (f.low-c).abs()], axis=1).max(axis=1)
    if len(tr) <= period:
        return tr.expanding().mean()
    tail = tr.iloc[period-1:].copy()
    tail.iloc[0] = tr.iloc[:period].mean()
    return pd.concat([tr.iloc[:period-1].expanding().mean(), tail.ewm(alpha=1/period, adjust=False).mean()])


def features(master):
    """Prefix-invariant features; partial 4h candles never join onto decisions."""
    f = master.copy().reset_index(drop=True)
    if f.empty:
        return f
    if not np.isfinite(f[INPUTS].to_numpy(float)).all():
        raise ValueError("Nonfinite input")
    ts = f.open_time_ms.to_numpy(np.int64)
    if len(ts) > 1 and not np.all(np.diff(ts) == BAR):
        raise ValueError("Gaps/duplicates in master grid")
    if not ((f.low > 0) & (f.low <= f[["open", "close"]].min(axis=1)) &
            (f.high >= f[["open", "close"]].max(axis=1))).all():
        raise ValueError("Invalid OHLC")
    f["atr"] = atr(f)
    f["e21"] = ema(f.close, 21)
    f["age"] = np.arange(1, len(f)+1)
    f["flow"] = f.future_cvd_15m.rolling(4).sum()/f.volume_base.rolling(4).sum().replace(0, np.nan)
    f["spot_flow"] = f.spot_cvd_15m.rolling(4).sum()
    # Zero delta is ambiguous between absent input and exactly balanced flow.
    # Conservatively require four nonzero spot deltas; never infer availability
    # from retrospective whole-file coverage or is_imputed_metrics.
    f["spot_observed"] = f.spot_cvd_15m.ne(0).rolling(4).sum().eq(4)
    f["active"] = f.volume_base.gt(0).rolling(4).sum().eq(4)
    relative_atr = f.atr/f.close
    prior = relative_atr.shift().rolling(1920, min_periods=1920)
    f["atr_z"] = (relative_atr-prior.mean())/prior.std(ddof=0).replace(0, np.nan)
    # Retain only complete buckets, including a bucket's last constituent bar
    # at its close; availability timestamp is the bucket's exclusive end.
    group = f.assign(bucket=ts//H4*H4).groupby("bucket", sort=True)
    h = group.agg(open=("open", "first"), high=("high", "max"), low=("low", "min"),
                  close=("close", "last"), count=("open", "size"))
    h = h[h["count"] == 16].copy()
    h["h4e50"] = ema(h.close, 50)
    h["h4e200"] = ema(h.close, 200)
    h["h4slope"] = h.h4e50-h.h4e50.shift(6)
    h["h4atr"] = atr(h)
    h["h4age"] = np.arange(1, len(h)+1)
    h["available_ms"] = h.index+H4
    h = h.rename(columns={"close": "h4close"})
    joined = pd.merge_asof(pd.DataFrame({"available_ms": ts+BAR}),
                          h[["available_ms", "h4close", "h4e50", "h4e200", "h4slope", "h4atr", "h4age"]],
                          on="available_ms", direction="backward")
    for name in joined.columns:
        if name != "available_ms":
            f[name] = joined[name].to_numpy()
    # Estimated reserve uses only past boundary observations, no future rate.
    settlement = f.loc[f.open_time_ms.mod(8*3_600_000).eq(0), ["open_time_ms", "funding_rate_pct"]].copy()
    settlement["funding_reserve_frac"] = settlement.funding_rate_pct.abs().rolling(90, min_periods=1).max()/100*9
    reserve = pd.merge_asof(f[["open_time_ms"]], settlement[["open_time_ms", "funding_reserve_frac"]],
                            on="open_time_ms", direction="backward")
    f["funding_reserve_frac"] = reserve.funding_reserve_frac.fillna(0)
    return f


def signals(f, btc, cfg):
    if f.empty:
        return f.copy()
    f = f.copy()
    b = btc.set_index("open_time_ms").reindex(f.open_time_ms).reset_index(drop=True)
    macro_ok = b.age.ge(cfg.warmup_15m) & b.h4age.ge(cfg.warmup_4h) & b.atr_z.le(3)
    long_macro = macro_ok & ~((b.h4close < b.h4e200) & (b.h4slope < 0))
    short_macro = macro_ok & ~((b.h4close > b.h4e200) & (b.h4slope > 0))
    ready = f.age.ge(cfg.warmup_15m) & f.h4age.ge(cfg.warmup_4h) & f.active
    long_trend = ready & (f.h4close > f.h4e50) & (f.h4e50 > f.h4e200) & (f.h4slope > 0) & long_macro
    short_trend = ready & (f.h4close < f.h4e50) & (f.h4e50 < f.h4e200) & (f.h4slope < 0) & short_macro
    lf = (f.flow >= cfg.flow_threshold) & (f.spot_flow > 0) & f.spot_observed
    sf = (f.flow <= -cfg.flow_threshold) & (f.spot_flow < 0) & f.spot_observed
    if not cfg.use_flow:
        lf = sf = pd.Series(True, index=f.index)
    hi = f.high.shift().rolling(cfg.lookback).max().to_numpy()
    lo = f.low.shift().rolling(cfg.lookback).min().to_numpy()
    vol = (f.volume_quote >= cfg.volume_ratio*f.volume_quote.shift().rolling(cfg.lookback).median()).to_numpy()
    eligible_l = (long_trend & lf).to_numpy()
    eligible_s = (short_trend & sf).to_numpy()
    close, high, low, op, av = [f[c].to_numpy(float) for c in ("close", "high", "low", "open", "atr")]
    side_out = np.zeros(len(f), dtype=np.int8)
    stop_out = np.full(len(f), np.nan)
    breakout_at = np.full(len(f), -1, dtype=np.int64)
    setup = None
    for j in range(len(f)):
        if setup is not None:
            d, origin, level, initial_atr = setup
            invalid = (d*(close[j]-level) < -0.5*initial_atr) or j-origin > cfg.retest_bars
            if invalid:
                setup = None
            else:
                extreme = low[j] if d == 1 else high[j]
                touch = abs(extreme-level) <= cfg.retest_buffer_atr*initial_atr
                eligible = eligible_l[j] if d == 1 else eligible_s[j]
                if touch and eligible and d*(close[j]-level) > 0 and d*(close[j]-op[j]) > 0:
                    side_out[j] = d
                    stop_out[j] = (low[origin:j+1].min()-cfg.retest_buffer_atr*av[j] if d == 1
                                   else high[origin:j+1].max()+cfg.retest_buffer_atr*av[j])
                    breakout_at[j] = int(f.open_time_ms.iloc[origin])
                    setup = None
        if setup is None and side_out[j] == 0 and vol[j]:
            d = 1 if eligible_l[j] and close[j] > hi[j] else (-1 if eligible_s[j] and close[j] < lo[j] else 0)
            if d:
                if cfg.use_retest:
                    setup = (d, j, hi[j] if d == 1 else lo[j], av[j])
                else:
                    side_out[j] = d
                    stop_out[j] = low[j]-0.25*av[j] if d == 1 else high[j]+0.25*av[j]
                    breakout_at[j] = int(f.open_time_ms.iloc[j])
    f["signal"] = side_out
    f["stop_ref"] = stop_out
    f["breakout_ms"] = breakout_at
    return f


def net(p, raw, cfg):
    return p["qty"]*(p["side"]*(raw-p["entry_ref"])-cfg.cost*cfg.cost_multiplier*p["entry_ref"])-p["funding"]


def price_for_r(p, r, cfg, reserve=False):
    funding = max(p["funding"], p["funding_reserve"]) if reserve else p["funding"]
    return p["entry_ref"]+p["side"]*((r*cfg.risk+funding)/p["qty"]+cfg.cost*cfg.cost_multiplier*p["entry_ref"])


def new_position(symbol, side, entry, stop, t, cfg, reserve_frac=0.0):
    if symbol not in ALTS:
        raise ValueError("Execution universe forbids BTC and other symbols")
    distance = side*(entry-stop)
    if distance <= 0 or stop <= 0 or entry <= 0:
        raise ValueError("Invalid stop geometry")
    reserve_frac = reserve_frac if cfg.funding_mode == "estimated_8h" else 0
    q = cfg.risk/(distance+(cfg.cost*cfg.cost_multiplier+reserve_frac)*entry)
    p = {"symbol": symbol, "side": side, "qty": q, "entry_ref": entry,
         "entry_fill": entry+side*0.001*cfg.cost_multiplier*entry,
         "entry_ms": int(t), "signal_close_ms": int(t-1), "initial_stop": stop, "stop": stop,
         "funding": 0.0, "funding_reserve": q*entry*reserve_frac, "max_close_r": -math.inf,
         "target_r": cfg.target_r, "entry_cost": q*entry*0.0018*cfg.cost_multiplier, "exit_next": ""}
    p["target"] = price_for_r(p, cfg.target_r, cfg, reserve=True)
    return p


def simulate(data, start, end, cfg):
    """Next-open event simulation; daily and total loss guards, costed MTM."""
    if any(s not in ALTS for s in data):
        raise ValueError("Invalid tradable symbol")
    cols = ["open", "high", "low", "close", "volume_base", "volume_quote", "atr", "e21",
            "flow", "signal", "stop_ref", "h4atr", "funding_rate_pct", "funding_reserve_frac", "breakout_ms"]
    ix = {s: i for i, s in enumerate(cols)}
    grid = np.arange(start, end, BAR, dtype=np.int64)
    table = {s: f.set_index("open_time_ms").reindex(np.r_[start-BAR, grid])[cols].to_numpy(float)
             for s, f in data.items() if not f.empty}
    cash = cfg.capital
    peak = cfg.capital
    day_start_equity = cfg.capital
    day_id = None
    daily_halt = False
    halted = False
    positions, cooldown = {}, {}
    trades, equity = [], []
    diagnostics = {"candidate_signals": 0, "invalid_or_chased": 0, "target_too_far": 0,
                   "capacity_rejected": 0, "risk_rejected": 0, "zero_volume_execution": 0,
                   "max_positions": 0, "daily_halt_count": 0}

    def mark(prices):
        return cash+sum(net(p, prices[s], cfg)+p["entry_cost"]+p["funding"] for s, p in positions.items())

    def close(s, raw, time, reason, bar):
        nonlocal cash
        p = positions.pop(s)
        pnl = net(p, raw, cfg)
        cash += pnl+p["entry_cost"]+p["funding"]
        costs = p["qty"]*p["entry_ref"]*cfg.cost*cfg.cost_multiplier
        trades.append({**p, "exit_ms": int(time), "exit_ref": raw,
                       "exit_fill": raw-p["side"]*0.0015*cfg.cost_multiplier*p["entry_ref"],
                       "fees": p["qty"]*p["entry_ref"]*0.0016*cfg.cost_multiplier,
                       "slippage": p["qty"]*p["entry_ref"]*0.0025*cfg.cost_multiplier,
                       "transaction_cost": costs, "net_pnl": pnl, "net_r": pnl/cfg.risk,
                       "reason": reason, "time_precision": "bar_open" if time % BAR == 0 else "bar_end_proxy"})
        cooldown[s] = time+cfg.cooldown*BAR
        if bar[ix["volume_base"]] == 0:
            diagnostics["zero_volume_execution"] += 1

    for k, t in enumerate(grid, 1):
        bars = {s: a[k] for s, a in table.items() if np.isfinite(a[k, ix["open"]])}
        if set(positions)-set(bars):
            raise ValueError("Missing held-asset valuation data")
        # Preserve the previous close as UTC day starting equity, so overnight
        # opening gaps count toward today's loss, not disappear in a reset.
        if t//DAY != day_id:
            day_id = t//DAY
            day_start_equity = equity[-1]["equity"] if equity else cfg.capital
            daily_halt = False
        if cfg.funding_mode == "estimated_8h" and t % (8*3_600_000) == 0:
            for s, p in positions.items():
                funding = p["side"]*p["qty"]*bars[s][ix["open"]]*bars[s][ix["funding_rate_pct"]]/100
                p["funding"] += funding
                cash -= funding
        open_equity = mark({s: bars[s][ix["open"]] for s in positions})
        peak = max(peak, open_equity)
        open_dd = (peak-open_equity)/peak
        if open_equity <= day_start_equity-cfg.daily_stop_usd:
            if not daily_halt:
                diagnostics["daily_halt_count"] += 1
            daily_halt = True
        halted |= open_dd >= cfg.circuit_fraction
        for s, p in list(positions.items()):
            o = bars[s][ix["open"]]
            if halted or p["exit_next"] or daily_halt:
                close(s, o, t, "portfolio_guard" if halted else p["exit_next"] or "daily_guard", bars[s])
            elif p["side"]*(o-p["stop"]) <= 0:
                close(s, o, t, "gap_stop", bars[s])
        # Capture opening drawdown even when trades subsequently recover.
        low_equity = min(open_equity, cash if not positions else open_equity)
        candidates = []
        if not halted and not daily_halt and k < len(grid):
            for s, a in table.items():
                prev = a[k-1]
                if s in bars and np.isfinite(prev[ix["signal"]]) and prev[ix["signal"]] != 0:
                    diagnostics["candidate_signals"] += 1
                    if s not in positions and t >= cooldown.get(s, -1):
                        candidates.append((abs(prev[ix["flow"]]), prev[ix["volume_quote"]], s, prev))
        for _, _, s, prev in sorted(candidates, key=lambda x: (-x[0], -x[1], x[2])):
            if len(positions) == cfg.max_positions:
                diagnostics["capacity_rejected"] += 1
                continue
            side, o, stop = int(prev[ix["signal"]]), bars[s][ix["open"]], prev[ix["stop_ref"]]
            if side*(o-prev[ix["close"]]) > cfg.max_entry_gap_atr*prev[ix["atr"]] or side*(o-stop) <= 0 or stop <= 0:
                diagnostics["invalid_or_chased"] += 1
                continue
            p = new_position(s, side, o, stop, t, cfg, prev[ix["funding_reserve_frac"]])
            p["breakout_ms"] = int(prev[ix["breakout_ms"]])
            if p["target"] <= 0 or abs(p["target"]-o) > cfg.target_atr_cap*prev[ix["h4atr"]]:
                diagnostics["target_too_far"] += 1
                continue
            current = mark({a: bars[a][ix["open"]] for a in positions})
            gross = sum(x["qty"]*bars[a][ix["open"]] for a, x in positions.items())
            stop_equity = cash+sum(net(x, x["stop"], cfg)+x["entry_cost"]+x["funding"] for x in positions.values())
            floor = max(peak*(1-cfg.circuit_fraction), day_start_equity-cfg.daily_stop_usd)
            if gross+p["qty"]*o > current*cfg.leverage_cap or stop_equity-cfg.risk < floor-1e-9:
                diagnostics["risk_rejected"] += 1
                continue
            positions[s] = p
            cash -= p["entry_cost"]
            diagnostics["max_positions"] = max(diagnostics["max_positions"], len(positions))
            if bars[s][ix["volume_base"]] == 0:
                diagnostics["zero_volume_execution"] += 1
        # Track conservative simultaneous adverse marks under standing stops.
        # These extrema are evaluation evidence only, NEVER used for sizing.
        adverse = {}
        favorable = {}
        for s, p in positions.items():
            b = bars[s]
            adverse[s] = max(b[ix["low"]], p["stop"]) if p["side"] > 0 else min(b[ix["high"]], p["stop"])
            favorable[s] = min(b[ix["high"]], p["target"]) if p["side"] > 0 else max(b[ix["low"]], p["target"])
        low_equity = min(low_equity, mark(adverse))
        high_bound = max(peak, mark(favorable))
        intrabar_dd_bound = max(0, (high_bound-low_equity)/high_bound)
        for s, p in list(positions.items()):
            b = bars[s]
            stop_hit = b[ix["low"]] <= p["stop"] if p["side"] > 0 else b[ix["high"]] >= p["stop"]
            target_hit = b[ix["high"]] >= p["target"] if p["side"] > 0 else b[ix["low"]] <= p["target"]
            if stop_hit:
                close(s, p["stop"], t+BAR-1, "stop", b)
                continue
            if target_hit:
                close(s, p["target"], t+BAR-1, "target", b)
                continue
            holding_bars = (t-p["entry_ms"])//BAR+1
            if holding_bars >= cfg.max_hold_bars:
                close(s, b[ix["close"]], t+BAR-1, "max_hold", b)
                continue
            r = net(p, b[ix["close"]], cfg)/cfg.risk
            p["max_close_r"] = max(p["max_close_r"], r)
            if holding_bars >= cfg.decay_bars and p["max_close_r"] < 0.2:
                p["exit_next"] = "time_decay"
            lock = 1 if r >= 2 else (0.2 if r >= 1 else None)
            proposal = p["stop"] if lock is None else price_for_r(p, lock, cfg)
            if r >= 3:
                p["target_r"] = cfg.runner_r
                trail = b[ix["e21"]]-p["side"]*0.5*b[ix["atr"]]
                proposal = max(proposal, trail) if p["side"] > 0 else min(proposal, trail)
            # Both amendments become active on the NEXT iteration only.
            p["stop"] = max(p["stop"], proposal) if p["side"] > 0 else min(p["stop"], proposal)
            p["target"] = price_for_r(p, p["target_r"], cfg, reserve=True)
        if k == len(grid):
            for s in list(positions):
                close(s, bars[s][ix["close"]], t+BAR-1, "quarter_end", bars[s])
        eq = mark({s: bars[s][ix["close"]] for s in positions})
        peak = max(peak, eq)
        dd = max(open_dd, (peak-eq)/peak, (peak-low_equity)/peak)
        if eq <= day_start_equity-cfg.daily_stop_usd or low_equity <= day_start_equity-cfg.daily_stop_usd:
            if not daily_halt:
                diagnostics["daily_halt_count"] += 1
            daily_halt = True
            for p in positions.values():
                p["exit_next"] = "daily_guard"
        if dd >= cfg.circuit_fraction:
            halted = True
        equity.append({"time_ms": int(t+BAR-1), "equity": eq, "cash": cash, "open_positions": len(positions),
                       "observed_dd_percent": max(open_dd, (peak-eq)/peak)*100,
                       "adverse_dd_percent": dd*100, "intrabar_order_unknown_dd_bound_percent": intrabar_dd_bound*100,
                       "daily_halted": daily_halt, "portfolio_halted": halted})
    if not math.isclose(cash-cfg.capital, sum(t["net_pnl"] for t in trades), abs_tol=1e-7):
        raise AssertionError("Trade/cash reconciliation failed")
    return {"trades": trades, "equity": equity, "diagnostics": diagnostics,
            "metrics": metrics(trades, equity, cfg)}


def metrics(trades, curve, cfg):
    q = pd.DataFrame(curve)
    p = np.array([t["net_pnl"] for t in trades])
    profit = float(p.sum())
    loss = -p[p < 0].sum()
    pf = float(p[p > 0].sum()/loss) if loss else (math.inf if profit > 0 else 0)
    eq = q.equity.to_numpy() if len(q) else np.array([cfg.capital])
    observed_dd = float(q.observed_dd_percent.max()) if len(q) else 0
    dd = float(q.adverse_dd_percent.max()) if len(q) else 0
    dd_bound = float(q.intrabar_order_unknown_dd_bound_percent.max()) if len(q) else 0
    peak = np.maximum.accumulate(np.r_[cfg.capital, eq])
    maxdd_usd = float(np.max(peak-np.r_[cfg.capital, eq]))
    daily = pd.DataFrame()
    if len(q):
        daily_eq = pd.Series(eq, index=pd.to_datetime(q.time_ms.to_numpy(), unit="ms", utc=True)).resample("1D").last()
        daily_pnl = daily_eq.diff()
        daily_pnl.iloc[0] = daily_eq.iloc[0]-cfg.capital
        ret = daily_eq.pct_change()
        ret.iloc[0] = daily_pnl.iloc[0]/cfg.capital
        daily = pd.DataFrame({"equity": daily_eq, "net_pnl": daily_pnl, "return": ret})
    ndays = len(daily)
    cagr = ((eq[-1]/cfg.capital)**(365.25/ndays)-1)*100 if ndays and eq[-1] > 0 else None
    sharpe = float(daily["return"].mean()/daily["return"].std(ddof=1)*np.sqrt(365.25)) if ndays > 1 and daily["return"].std(ddof=1) > 0 else None
    checks = {"roi": profit/cfg.capital >= 0.10, "max_dd": max(dd, dd_bound) < 5,
              "win_rate": len(p) > 0 and float(np.mean(p > 0)) >= 0.40,
              "trade_count": len(p) >= 15, "profit_factor": pf >= 1.40, "planned_target_r": cfg.target_r >= 4}
    result = {"net_profit_usd": profit, "net_roi_percent": profit/cfg.capital*100,
              "max_dd_percent": observed_dd, "adverse_max_dd_percent": dd,
              "intrabar_unknown_order_dd_bound_percent": dd_bound,
              "max_close_dd_usd": maxdd_usd, "win_rate_percent": float(np.mean(p > 0)*100) if len(p) else 0,
              "total_trades": len(p), "profit_factor": pf, "average_net_r": float(p.mean()/cfg.risk) if len(p) else None,
              "cagr_percent": cagr, "sharpe_daily": sharpe, "calmar_observed": cagr/observed_dd if observed_dd and cagr is not None else None,
              "transaction_cost_usd": sum(t["transaction_cost"] for t in trades),
              "funding_usd": sum(t["funding"] for t in trades), "checks": checks,
              "verdict": "PASS" if all(checks.values()) else "FAIL"}
    for side, label in ((1, "long"), (-1, "short")):
        subset = np.array([t["net_pnl"] for t in trades if t["side"] == side])
        result[label] = {"trades": len(subset), "net_profit_usd": float(subset.sum()),
                         "win_rate_percent": float(np.mean(subset > 0)*100) if len(subset) else None,
                         "average_net_r": float(subset.mean()/cfg.risk) if len(subset) else None}
    if ndays:
        d = daily.net_pnl.to_numpy()
        streak = longest = 0
        for value in d:
            streak = streak+1 if value < -1e-9 else 0
            longest = max(longest, streak)
        rng = np.random.default_rng(9152026)
        block = min(7, ndays)
        draws = []
        for _ in range(2000):
            starts = rng.integers(0, ndays, size=math.ceil(ndays/block))
            indices = (starts[:, None]+np.arange(block)) % ndays
            draws.append(float(d[indices.ravel()[:ndays]].mean()))
        result["daily"] = {"days": ndays, "profitable": int((d > 1e-9).sum()), "losing": int((d < -1e-9).sum()),
                           "flat": int((np.abs(d) <= 1e-9).sum()), "worst_usd": float(d.min()),
                           "mean_usd": float(d.mean()), "median_usd": float(np.median(d)),
                           "longest_losing_streak": longest, "mean_95pct_block_bootstrap_usd": np.quantile(draws, [0.025, 0.975]).tolist(),
                           "bootstrap": "2000 circular resamples of 7-day blocks; evaluated prefix only"}
        result["daily_rows"] = [{"date": str(i.date()), **row.to_dict()} for i, row in daily.iterrows()]
    return result


def load(data_dir, end):
    import pyarrow.parquet as pq
    result, inventory = {}, []
    for s in (BTC,)+ALTS:
        path = Path(data_dir)/f"{s}_15m_master_2020_2026.parquet"
        master = pq.read_table(path, columns=INPUTS, filters=[("open_time_ms", "<", end)]).to_pandas()
        result[s] = features(master)
        first_ready = result[s].loc[result[s].h4age >= 1000, "open_time_ms"] if len(master) else []
        inventory.append({"symbol": s, "rows": len(master), "four_hour_ready": iso(first_ready.iloc[0]+BAR) if len(first_ready) else None})
        print(f"Prepared {s}: {len(master):,} bars", flush=True)
    return result, inventory


def windows():
    dates = pd.date_range("2021-01-01", "2026-01-01", freq="QS", tz="UTC")
    return [(f"W{i+1:02d}", f"{a.year}Q{a.quarter}", int(a.value//1_000_000), int(b.value//1_000_000))
            for i, (a, b) in enumerate(zip(dates[:-1], dates[1:]))]


def scorecard(rows):
    lines = ["| Window | Period | Net ROI (%) | Max DD (%) | Win Rate (%) | Total Trades | Profit Factor | Verdict |",
             "| ------ | ------ | ----------- | ---------- | ------------ | ------------ | ------------- | ------- |"]
    for r in rows:
        m = r.get("metrics")
        if m is None:
            lines.append(f"| {r['window']} | {r['period']} | — | — | — | — | — | NOT RUN |")
        else:
            lines.append(f"| {r['window']} | {r['period']} | {m['net_roi_percent']:.2f} | {m['max_dd_percent']:.2f} | {m['win_rate_percent']:.2f} | {m['total_trades']} | {m['profit_factor']:.2f} | {m['verdict']} |")
    return "\n".join(lines)+"\n"


def evaluate(loader, cfg, output, compare=True):
    """Injectable loader permits an adversarial test that W02 is never read."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    rows, results = [], []
    failed = False
    for name, period, start, end in windows():
        if failed:
            rows.append({"window": name, "period": period, "metrics": None})
            continue
        f, inventory = loader(end)
        data = {s: signals(x, f[BTC], cfg) for s, x in f.items() if s != BTC and len(x)}
        r = simulate(data, start, end, cfg)
        results.append(r)
        rows.append({"window": name, "period": period, "metrics": r["metrics"]})
        write_json(output/f"{name}_metrics.json", r["metrics"])
        write_json(output/f"{name}_diagnostics.json", r["diagnostics"])
        write_json(output/f"{name}_inventory.json", inventory)
        pd.DataFrame(r["trades"]).to_csv(output/f"{name}_trades.csv", index=False)
        pd.DataFrame(r["equity"]).to_parquet(output/f"{name}_equity.parquet", index=False)
        pd.DataFrame(r["metrics"].get("daily_rows", [])).to_csv(output/f"{name}_daily.csv", index=False)
        print(name, json.dumps({k: r["metrics"][k] for k in ("net_roi_percent", "max_dd_percent", "total_trades", "verdict")}), flush=True)
        # Predeclared comparisons on this already-evaluated quarter. No later
        # quarter is visited, no configuration is selected using comparisons.
        if compare:
            variants = {"no_flow_filter": replace(cfg, use_flow=False),
                        "no_flow_no_retest": replace(cfg, use_flow=False, use_retest=False),
                        "cost_1_5x": replace(cfg, cost_multiplier=1.5),
                        "cost_2x": replace(cfg, cost_multiplier=2),
                        "transaction_only": replace(cfg, funding_mode="transaction_only")}
            comparisons = {}
            for label, c in variants.items():
                d = data if label.startswith("cost") or label == "transaction_only" else {s: signals(x, f[BTC], c) for s, x in f.items() if s != BTC and len(x)}
                sr = simulate(d, start, end, c)
                comparisons[label] = sr["metrics"]
                print(f"Comparison {name}/{label}: {sr['metrics']['net_profit_usd']:.2f} USD", flush=True)
            write_json(output/f"{name}_comparisons.json", comparisons)
        failed = r["metrics"]["verdict"] != "PASS"
        del f, data
    write_json(output/"scorecard.json", rows)
    (output/"scorecard.md").write_text(scorecard(rows), encoding="utf-8")
    return rows, results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir", default="scratch/trend_suite_20260910/raw_data")
    p.add_argument("--criteria", default="scratch/trend_suite_20260910/references/Engine__target_oos_criteria.json")
    p.add_argument("--output", default="Engine/inefficiency_results_20260915")
    p.add_argument("--no-comparisons", action="store_true")
    args = p.parse_args()
    output = Path(args.output)
    cfg = Config()
    contract = json.loads(Path(args.criteria).read_text(encoding="utf-8"))
    expected = {"initial_capital_usd": 5000, "base_risk_usd": 50, "min_roi_percent": 10,
                "max_dd_percent": 5, "min_winrate_percent": 40, "min_r_multiple": 4, "min_trades": 15}
    if any(contract["target_criteria"][k] != v for k, v in expected.items()):
        raise ValueError("Source contract mismatch")
    write_json(output/"protocol.json", {"frozen_config": asdict(cfg), "source_contract": contract,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "selection": "Fixed proposed design; zero parameter fitting; no OOS-driven selection",
        "purge": "No fitted labels or training trades; any training outcomes must end before window_start-72h",
        "funding": "Estimated 8h settlement schedule with last-settled master rate, not exact event replay",
        "cost_convention": "41bps entry-reference notional; fees/slippage itemized, not double charged",
        "comparisons": ["no_flow_filter", "no_flow_no_retest", "cost_1_5x", "cost_2x", "transaction_only"],
        "deployment_status": "Research only; exact funding, exchange filters and live fills remain unverified"})
    rows, results = evaluate(lambda end: load(args.data_dir, end), cfg, output, not args.no_comparisons)
    # Additive stitching respects the explicitly reset $5,000 quarterly budget.
    combined, trades, offset = [], [], 0.0
    for r in results:
        combined.extend([{**e, "equity": e["equity"]+offset} for e in r["equity"]])
        trades.extend(r["trades"])
        offset += r["metrics"]["net_profit_usd"]
    summary = metrics(trades, combined, cfg)
    summary["evaluated_windows"] = len(results)
    summary["all_twenty_pass"] = len(results) == 20 and all(r["metrics"]["verdict"] == "PASS" for r in results)
    summary["annualization_scope"] = "Evaluated prefix only; not a realized five-year CAGR"
    write_json(output/"portfolio_statistics.json", summary)


if __name__ == "__main__":
    main()
