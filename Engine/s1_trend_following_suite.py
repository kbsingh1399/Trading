"""Causal, research-only altcoin trend/orderflow portfolio backtester.

Run ``python Engine/s1_trend_following_suite.py --help``. Requires numpy,
pandas and pyarrow. No exchange connection or order submission is provided.
Every signal is formed at a completed candle and filled at the next open.
Configuration selection sees only history ending 72 hours before evaluation.
The first failed quarter stops the scorecard; unvisited quarters are not scored.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np
import pandas as pd

BAR_MS = 900_000
DAY_MS = 86_400_000
PURGE_MS = 72 * 3_600_000
BTC = "BTCUSDT"
ALTCOINS = tuple(x + "USDT" for x in (
    "ETH", "XRP", "SOL", "BNB", "DOGE", "ADA", "TRX", "LINK", "AVAX",
    "SUI", "NEAR", "DOT", "LTC", "BCH", "APT", "OP", "ARB"))
MASTER_COLUMNS = ["open_time_ms", "open", "high", "low", "close", "volume_base",
                  "volume_quote", "future_cvd_15m", "session_vah", "session_val",
                  "prev_day_vah", "prev_day_val", "funding_rate_pct"]


@dataclass(frozen=True)
class Config:
    capital: float = 5000.0
    risk_usd: float = 50.0
    max_positions: int = 2
    max_gross_leverage: float = 3.0
    fee: float = 0.0008
    entry_slip: float = 0.0010
    exit_slip: float = 0.0015
    friction_floor: float = 0.0041
    dd_limit: float = 0.05
    circuit_fraction: float = 0.048
    warmup_bars: int = 1000
    breakout_bars: int = 96
    stop_atr: float = 2.5
    min_stop_fraction: float = 0.012
    target_r: float = 2.0
    flow_threshold: float = 0.02
    volume_threshold: float = 1.22
    compression_ratio: float = 1.1
    macro_z_limit: float = 3.0
    sleeve_mode: str = "adaptive"
    ratchet: bool = True
    max_hold_bars: int = 144
    decay_bars: int = 24
    cooldown_bars: int = 8
    # The master exposes last-settled rates, not event timestamps. This is an
    # explicitly approximate 8h funding model, separately itemized in output.
    funding_8h: bool = True

    def __post_init__(self):
        if self.max_positions not in (2, 3):
            raise ValueError("The portfolio must allow 2 or 3 concurrent positions")
        if self.capital != 5000 or self.risk_usd != 50:
            raise ValueError("This mission fixes capital at $5,000 and base risk at $50")
        if self.target_r < 2.0 or self.max_hold_bars > 288:
            raise ValueError("Targets must be >=2.0 net R and holding period <=72h")
        if (self.fee, self.entry_slip, self.exit_slip) != (0.0008, 0.001, 0.0015):
            raise ValueError("Contract frictions cannot be reduced")


def ms(value: str | pd.Timestamp) -> int:
    t = pd.Timestamp(value)
    t = t.tz_localize("UTC") if t.tzinfo is None else t.tz_convert("UTC")
    return int(t.value // 1_000_000)


def iso(value: int) -> str:
    return pd.Timestamp(value, unit="ms", tz="UTC").isoformat()


def clean_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): clean_json(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [clean_json(x) for x in obj]
    if isinstance(obj, (np.integer, np.bool_)):
        return obj.item()
    if isinstance(obj, (np.floating, float)):
        return float(obj) if math.isfinite(obj) else None
    return obj


def write_json(path: Path, obj: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(clean_json(obj), indent=2, allow_nan=False), encoding="utf-8")


def ema(prices: pd.Series, period: int) -> pd.Series:
    """Match the raw canonical indicator's rounded, recursive EMA kernel."""
    x = prices.to_numpy(float)
    out = np.empty(len(x))
    if len(x):
        value = round(float(x[0]), 8)
        alpha = 2.0 / (period + 1)
        out[0] = value
        for i in range(1, len(x)):
            value = round(alpha * float(x[i]) + (1 - alpha) * value, 8)
            out[i] = value
    return pd.Series(out, index=prices.index)


def rma(values: pd.Series, period: int) -> pd.Series:
    if len(values) <= period:
        return values.expanding().mean()
    head = values.iloc[:period-1].expanding().mean()
    tail = values.iloc[period-1:].copy()
    tail.iloc[0] = values.iloc[:period].mean()
    return pd.concat([head, tail.ewm(alpha=1 / period, adjust=False).mean()])


def prepare_features(master: pd.DataFrame, footprint: pd.DataFrame | None = None) -> pd.DataFrame:
    """Only completed-bar raw OHLCV, taker flow and causal value areas enter signals.

    No modeled liquidations, positioning metrics, ex-post quarantine flags,
    full-history normalization, backward fills or fitted ML features are used.
    """
    f = master.copy().reset_index(drop=True)
    if f.empty:
        return f
    t = f.open_time_ms.to_numpy(np.int64)
    if len(t) > 1 and not np.all(np.diff(t) == BAR_MS):
        raise ValueError("Master timestamps are not a contiguous 15m grid")
    if not np.isfinite(f[MASTER_COLUMNS].to_numpy(float)).all():
        raise ValueError("Master inputs contain non-finite values")
    if not ((f.low > 0) & (f.low <= f[["open", "close"]].min(axis=1)) &
            (f.high >= f[["open", "close"]].max(axis=1))).all():
        raise ValueError("Invalid OHLC geometry")
    c, h, lo = f.close, f.high, f.low
    for n in (21, 50, 200, 800, 2880):
        f[f"e{n}"] = ema(c, n)
    tr = pd.concat([h-lo, (h-c.shift()).abs(), (lo-c.shift()).abs()], axis=1).max(axis=1)
    f["atr"] = rma(tr, 14)
    f["atr100"] = rma(tr, 100)
    f["atr_ratio"] = f.atr / f.atr100.replace(0, np.nan)
    f["compression"] = f.atr_ratio.rolling(32, min_periods=32).min().shift(1)
    av = f.atr / c
    prior = av.shift(1).rolling(1920, min_periods=1920)
    f["atr_z"] = (av-prior.mean()) / prior.std(ddof=0).replace(0, np.nan)
    f["slope200"] = (f.e200-f.e200.shift(96)) / f.atr.replace(0, np.nan)
    f["slope800"] = (f.e800-f.e800.shift(96)) / f.atr.replace(0, np.nan)
    v = f.volume_base
    f["flow"] = f.future_cvd_15m.rolling(4).sum() / v.rolling(4).sum().replace(0, np.nan)
    f["flow_prev"] = f.flow.shift(4)
    f["volume_rel"] = v / v.shift(1).rolling(96, min_periods=96).mean().replace(0, np.nan)
    day = t // DAY_MS
    pv = ((h+lo+c)/3*v).groupby(day).cumsum()
    f["vwap"] = pv / v.groupby(day).cumsum().replace(0, np.nan)
    for n in (24, 48, 72, 96, 192):
        f[f"hi{n}"] = h.shift(1).rolling(n, min_periods=n).max()
        f[f"lo{n}"] = lo.shift(1).rolling(n, min_periods=n).min()
    daily = f.assign(day=day).groupby("day").agg(high=("high", "max"), low=("low", "min"))
    f["pdh"] = pd.Series(day-1).map(daily.high).to_numpy()
    f["pdl"] = pd.Series(day-1).map(daily.low).to_numpy()
    f["swing_low"] = lo.rolling(4).min()
    f["swing_high"] = h.rolling(4).max()
    f["age"] = np.arange(len(f))
    # Ernest Chan: Hurst Exponent (variance ratio proxy over 96 bars / 24h)
    ret1 = c.diff()
    ret4 = c.diff(4)
    var1 = ret1.rolling(96, min_periods=48).var()
    var4 = ret4.rolling(96, min_periods=48).var()
    var_ratio = var4 / (4.0 * var1.replace(0, np.nan))
    f["hurst"] = (0.5 + 0.5 * np.log(var_ratio.clip(lower=1e-6)) / np.log(4.0)).fillna(0.5)

    # Ernest Chan: Ornstein-Uhlenbeck Mean-Reversion Half-Life on EMA200 residual
    residual = (c - f["e200"]).fillna(0)
    res_lag = residual.shift(1).fillna(0)
    d_res = residual.diff().fillna(0)
    cov_xy = (d_res * res_lag).rolling(96, min_periods=48).mean() - d_res.rolling(96, min_periods=48).mean() * res_lag.rolling(96, min_periods=48).mean()
    var_x = (res_lag**2).rolling(96, min_periods=48).mean() - (res_lag.rolling(96, min_periods=48).mean())**2
    b_slope = (cov_xy / var_x.replace(0, np.nan)).fillna(0)
    theta = -np.log((1.0 + b_slope).clip(lower=1e-4, upper=0.9999))
    f["ou_half_life"] = (np.log(2.0) / theta.replace(0, np.nan)).fillna(999.0)

    f["stack_buy"] = 0
    f["stack_sell"] = 0
    f["footprint_available"] = False
    if footprint is not None and not footprint.empty:
        g = footprint.groupby("open_time_ms", sort=False).agg(
            stack_buy=("is_stacked_buy_imb", "sum"),
            stack_sell=("is_stacked_sell_imb", "sum"))
        for name in ("stack_buy", "stack_sell"):
            f[name] = f.open_time_ms.map(g[name]).fillna(0).astype(int)
        f["footprint_available"] = f.open_time_ms.isin(g.index)
    return f


def build_signals(f: pd.DataFrame, btc: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """T1 compression break; T2 trend/value pullback; T3 empirical stack expansion."""
    if f.empty:
        return f.copy()
    b = btc.set_index("open_time_ms").reindex(f.open_time_ms)
    b.index = f.index
    macro_ok = b.age.ge(cfg.warmup_bars) & b.atr_z.le(cfg.macro_z_limit)
    macro_long = macro_ok & (b.close > b.e2880) & (b.e200 > b.e2880) & (b.slope200 > 0)
    macro_short = macro_ok & (b.close < b.e2880) & (b.e200 < b.e2880) & (b.slope200 < 0)
    long_trend = (f.e50 > f.e200) & (f.e200 > f.e800) & (f.slope200 > 0)
    short_trend = (f.e50 < f.e200) & (f.e200 < f.e800) & (f.slope200 < 0)
    flow_l = f.flow > cfg.flow_threshold
    flow_s = f.flow < -cfg.flow_threshold
    sponsorship = f.volume_rel >= cfg.volume_threshold
    compression = f.compression < cfg.compression_ratio
    hi_b = f[f"hi{cfg.breakout_bars}"] if f"hi{cfg.breakout_bars}" in f else f.high.shift(1).rolling(cfg.breakout_bars, min_periods=cfg.breakout_bars).max()
    lo_b = f[f"lo{cfg.breakout_bars}"] if f"lo{cfg.breakout_bars}" in f else f.low.shift(1).rolling(cfg.breakout_bars, min_periods=cfg.breakout_bars).min()
    t1_l = long_trend & flow_l & sponsorship & compression & (f.close > hi_b) & (f.hurst >= 0.45)
    t1_s = short_trend & flow_s & sponsorship & compression & (f.close < lo_b) & (f.hurst >= 0.45)
    # Value area is developing at j close; prior-day levels are fully complete.
    reclaim_l = ((f.low <= f.session_val) & (f.close > f.session_val)) | ((f.low < f.pdl) & (f.close > f.pdl))
    reclaim_s = ((f.high >= f.session_vah) & (f.close < f.session_vah)) | ((f.high > f.pdh) & (f.close < f.pdh))
    t2_l = long_trend & reclaim_l & flow_l & (f.flow > f.flow_prev) & (f.close > f.e21) & (f.close > f.open) & (f.ou_half_life <= 48.0)
    t2_s = short_trend & reclaim_s & flow_s & (f.flow < f.flow_prev) & (f.close < f.e21) & (f.close < f.open) & (f.ou_half_life <= 48.0)
    t3_l = long_trend & sponsorship & (f.flow > max(0.10, cfg.flow_threshold)) & (f.stack_buy >= 3) & (f.close > f.hi24) & (f.hurst >= 0.45)
    t3_s = short_trend & sponsorship & (f.flow < -max(0.10, cfg.flow_threshold)) & (f.stack_sell >= 3) & (f.close < f.lo24) & (f.hurst >= 0.45)
    sleeve_l = np.zeros(len(f), dtype=np.int8)
    sleeve_s = np.zeros(len(f), dtype=np.int8)
    if cfg.sleeve_mode == "adaptive":
        btc_expansion = b.slope200.abs().ge(0.80)
        t1_eligible_l = t1_l & btc_expansion
        t1_eligible_s = t1_s & btc_expansion
        t2_eligible_l = t2_l & ~btc_expansion
        t2_eligible_s = t2_s & ~btc_expansion
        sleeve_l[t2_eligible_l.to_numpy()] = 2
        sleeve_s[t2_eligible_s.to_numpy()] = 2
        sleeve_l[t1_eligible_l.to_numpy()] = 1
        sleeve_s[t1_eligible_s.to_numpy()] = 1
    else:
        for name, n, l, s in (("t2", 2, t2_l, t2_s), ("t1", 1, t1_l, t1_s), ("t3", 3, t3_l, t3_s)):
            if cfg.sleeve_mode in ("all", name):
                sleeve_l[l.to_numpy()] = n
                sleeve_s[s.to_numpy()] = n
    valid = (f.age >= cfg.warmup_bars) & (f.volume_quote > 0)
    l = valid & macro_long & (sleeve_l > 0)
    s = valid & macro_short & (sleeve_s > 0)
    out = f.copy()
    out["signal"] = np.where(l & ~s, 1, np.where(s & ~l, -1, 0)).astype(np.int8)
    out["sleeve"] = np.where(out.signal > 0, sleeve_l, np.where(out.signal < 0, sleeve_s, 0))
    out["score"] = (f.flow.abs() * f.volume_rel.clip(upper=10) + f.slope200.abs().clip(upper=10) * 0.05).fillna(0)
    out["stop_distance"] = np.maximum(f.atr * cfg.stop_atr, f.close * cfg.min_stop_fraction)
    return out


def execution_values(entry_ref: float, exit_ref: float, side: int, cfg: Config) -> dict[str, float]:
    entry_fill = entry_ref * (1 + side * cfg.entry_slip)
    exit_fill = exit_ref * (1 - side * cfg.exit_slip)
    fees = cfg.fee * (entry_fill + exit_fill)
    slippage = cfg.entry_slip * entry_ref + cfg.exit_slip * exit_ref
    topup = max(0.0, cfg.friction_floor * entry_ref - fees - slippage)
    return {"entry_fill": entry_fill, "exit_fill": exit_fill, "fees": fees,
            "slippage": slippage, "friction_topup": topup,
            "net_per_unit": side * (exit_ref-entry_ref) - fees-slippage-topup}


def net_pnl(p: dict, exit_ref: float, cfg: Config) -> float:
    return p["qty"] * execution_values(p["entry_ref"], exit_ref, p["side"], cfg)["net_per_unit"] - p.get("funding", 0.0)


def price_for_net_r(p: dict, target: float, cfg: Config) -> float:
    # Monotonic piecewise-linear cost function. Bisection includes actual-fill
    # fees, slippage, funding accrued so far and the mandatory friction floor.
    wanted = target * cfg.risk_usd
    lo, hi = max(1e-12, p["entry_ref"] * 0.000001), p["entry_ref"] * 100
    for _ in range(64):
        mid = (lo+hi)/2
        below = net_pnl(p, mid, cfg) < wanted
        if below == (p["side"] > 0):
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def calculate_binomial_evolution_function(trades: list[dict]) -> dict:
    """Computes Andrea Berdondini's Binomial Evolution Function (BEF).
    
    Transforms the sequence of trades into a sequence of independent events
    across market state transitions and performs a binomial test against the
    random walk null hypothesis (p=0.5).
    """
    if len(trades) < 2:
        return {"bef_independent_trades": 0, "bef_successes": 0, "bef_p_value": 1.0, "bef_cognitive_edge": False}
    
    sorted_trades = sorted(trades, key=lambda x: x.get("entry_time_ms", 0))
    transformed_outcomes: list[tuple[int, int]] = []
    for i in range(len(sorted_trades)):
        curr = sorted_trades[i]
        is_win = 1 if curr.get("net_pnl", 0.0) > 0 else 0
        if i > 0:
            prev = sorted_trades[i - 1]
            if curr["side"] == prev["side"]:
                probe_side = -curr["side"]
                delta_price = curr["entry_ref"] - prev["exit_ref"]
                probe_win = 1 if (probe_side * delta_price > 0) else 0
                transformed_outcomes.append((probe_side, probe_win))
        transformed_outcomes.append((curr["side"], is_win))
        
    binary_seq = [outcome[1] for outcome in transformed_outcomes]
    independent_outcomes: list[int] = []
    for i in range(1, len(binary_seq)):
        if binary_seq[i] == binary_seq[i - 1]:
            independent_outcomes.append(binary_seq[i])
            
    n = len(independent_outcomes)
    k = sum(independent_outcomes)
    if n > 0:
        p_val_tail = float(sum(math.comb(n, j) * (0.5**n) for j in range(k, n + 1)))
    else:
        p_val_tail = 1.0
        
    return {
        "bef_total_transformed": len(binary_seq),
        "bef_independent_trades": n,
        "bef_successes": k,
        "bef_win_rate_percent": float(k / n * 100) if n > 0 else 0.0,
        "bef_p_value": float(p_val_tail),
        "bef_cognitive_edge": bool(p_val_tail < 0.05 and k > n / 2)
    }


def score_metrics(trades: list[dict], equity: list[dict], cfg: Config) -> dict:
    curve = np.array([cfg.capital] + [e["equity"] for e in equity], float)
    peak = np.maximum.accumulate(curve)
    dd = peak-curve
    pnl = np.array([t["net_pnl"] for t in trades], float)
    wins = pnl[pnl > 0].sum()
    loss = -pnl[pnl < 0].sum()
    pf = float(wins/loss) if loss > 0 else (math.inf if wins > 0 else 0.0)
    roi = (curve[-1]/cfg.capital-1)*100
    maxdd = float(np.max(dd/peak)*100)
    stress_dd = max([0.0] + [e["adverse_bound_dd_percent"] for e in equity])
    winrate = float(np.mean(pnl > 0)*100) if len(pnl) else 0.0
    bef = calculate_binomial_evolution_function(trades)
    checks = {"roi": roi >= 10, "max_dd": maxdd < 5 and stress_dd < 5,
              "win_rate": winrate >= 40, "trade_count": len(pnl) >= 15,
              "target_r": cfg.target_r >= 2.0}
    days = len(equity)/96
    cagr = ((curve[-1]/cfg.capital)**(365.25/days)-1)*100 if days and curve[-1] > 0 else None
    if equity:
        es = pd.Series([e["equity"] for e in equity], index=pd.to_datetime([e["time_ms"] for e in equity], unit="ms", utc=True))
        daily = es.resample("1D").last()
        rets = daily.pct_change()
        rets.iloc[0] = daily.iloc[0]/cfg.capital-1
        sharpe = float(rets.mean()/rets.std(ddof=1)*np.sqrt(365.25)) if rets.std(ddof=1) > 0 else None
    else:
        sharpe = None
    return {"net_profit_usd": float(curve[-1]-cfg.capital), "net_roi_percent": roi,
            "max_dd_percent": maxdd, "max_dd_usd": float(dd.max()),
            "adverse_bound_max_dd_percent": stress_dd,
            "win_rate_percent": winrate, "total_trades": len(pnl), "profit_factor": pf,
            "average_r": float(pnl.mean()/cfg.risk_usd) if len(pnl) else None,
            "average_winner_r": float(pnl[pnl > 0].mean()/cfg.risk_usd) if (pnl > 0).any() else None,
            "cagr_percent": cagr, "sharpe_daily": sharpe,
            "calmar": cagr/maxdd if cagr is not None and maxdd > 0 else None,
            "bef": bef,
            "checks": checks, "verdict": "PASS" if all(checks.values()) else "FAIL",
            "long": breakdown(trades, 1), "short": breakdown(trades, -1)}


def breakdown(trades: list[dict], side: int) -> dict:
    selected = [t for t in trades if t["side"] == side]
    return {"trades": len(selected), "net_profit_usd": sum(t["net_pnl"] for t in selected),
            "win_rate_percent": 100*sum(t["net_pnl"] > 0 for t in selected)/len(selected) if selected else None,
            "average_r": sum(t["net_r"] for t in selected)/len(selected) if selected else None}


def simulate_window(data: dict[str, pd.DataFrame], start_ms: int, end_ms: int,
                    cfg: Config) -> dict:
    """Event loop with prior-close orders, stop-first bars and live fixed risk.

    End is exclusive. Quarter liquidation at its last close is precommitted.
    The adverse OHLC bound combines each open position's adverse extreme; it
    is conservative, not a reconstructed simultaneous intrabar equity path.
    It rejects uncertain <5% drawdown claims and queues next-open liquidation.
    """
    if BTC in data or any(s not in ALTCOINS for s in data):
        raise ValueError("BTC and non-whitelisted symbols cannot enter execution")
    grid = np.arange(start_ms, end_ms, BAR_MS, dtype=np.int64)
    cols = ["open", "high", "low", "close", "signal", "sleeve", "score", "stop_distance",
            "e21", "atr", "swing_low", "swing_high", "funding_rate_pct"]
    arrays = {}
    # Include the previous completed bar for an entry on the first OOS open.
    fullgrid = np.r_[start_ms-BAR_MS, grid]
    for s, f in data.items():
        if not f.empty:
            arrays[s] = f.set_index("open_time_ms").reindex(fullgrid)[cols].to_numpy(float)
    ix = {c: i for i, c in enumerate(cols)}
    positions: dict[str, dict] = {}
    cooldown = {s: -1 for s in arrays}
    portfolio_cooldown = -1
    consec_losses = 0
    cash = cfg.capital
    peak = cfg.capital
    halted = False
    trades: list[dict] = []
    curve: list[dict] = []
    max_open = 0

    def close_position(symbol: str, raw: float, t: int, reason: str):
        nonlocal cash, consec_losses, portfolio_cooldown
        p = positions.pop(symbol)
        vals = execution_values(p["entry_ref"], raw, p["side"], cfg)
        # Entry fee was booked at entry; funding at settlement. Finish cash
        # accounting without charging either twice.
        net = net_pnl(p, raw, cfg)
        cash += net + p["entry_fee"] + p["funding"]
        trades.append({**p, "symbol": symbol, "exit_time_ms": int(t),
                       "exit_ref": raw, "exit_fill": vals["exit_fill"],
                       "fees": p["qty"]*vals["fees"], "slippage": p["qty"]*vals["slippage"],
                       "friction_topup": p["qty"]*vals["friction_topup"],
                       "net_pnl": net, "net_r": net/cfg.risk_usd, "exit_reason": reason})
        cooldown[symbol] = t + cfg.cooldown_bars*BAR_MS
        if net < 0:
            consec_losses += 1
            if consec_losses >= 3:
                portfolio_cooldown = t + 48 * BAR_MS
                consec_losses = 0
        else:
            consec_losses = 0

    def marked(refs: dict[str, float]) -> float:
        return cash + sum(net_pnl(p, refs[s], cfg)+p["entry_fee"]+p["funding"] for s, p in positions.items())

    for k, t in enumerate(grid, start=1):
        bars = {s: a[k] for s, a in arrays.items() if np.isfinite(a[k, ix["open"]])}
        missing = set(positions)-set(bars)
        if missing:
            raise ValueError(f"Missing valuation bar for held symbols: {missing}")
        # Funding settles before new orders, so newly opened positions do not
        # owe the settlement that just occurred.
        if cfg.funding_8h and t % (8*3_600_000) == 0:
            for s, p in positions.items():
                cost = p["side"]*p["qty"]*bars[s][ix["open"]]*bars[s][ix["funding_rate_pct"]]/100
                p["funding"] += cost
                cash -= cost
        for s, p in list(positions.items()):
            b = bars[s]
            o = b[ix["open"]]
            if halted or p.get("exit_next"):
                close_position(s, o, int(t), "circuit" if halted else p["exit_next"])
            elif p["side"]*(o-p["stop"]) <= 0:
                close_position(s, o, int(t), "gap_stop")
        open_refs = {s: bars[s][ix["open"]] for s in positions}
        if marked(open_refs) <= peak*(1-cfg.circuit_fraction):
            halted = True
            for s in list(positions):
                close_position(s, bars[s][ix["open"]], int(t), "open_circuit")
        candidates = []
        if not halted and k < len(grid) and t >= portfolio_cooldown:
            for s, a in arrays.items():
                prev = a[k-1]
                if s in bars and s not in positions and t >= cooldown[s] and np.isfinite(prev[ix["signal"]]) and prev[ix["signal"]] != 0:
                    candidates.append((float(prev[ix["score"]]), s, prev))
        # Simultaneous cross-asset ranking uses only j-close information.
        for _, s, sig in sorted(candidates, key=lambda x: (-x[0], x[1])):
            if len(positions) >= cfg.max_positions:
                break
            side = int(sig[ix["signal"]])
            o = float(bars[s][ix["open"]])
            distance = float(sig[ix["stop_distance"]])
            if not math.isfinite(distance) or distance <= 0 or o-distance <= 0:
                continue
            stop = o-side*distance
            unit_loss = -execution_values(o, stop, side, cfg)["net_per_unit"]
            current_refs = {a: bars[a][ix["open"]] for a in positions}
            equity_open = marked(current_refs)
            current_dd = (peak - equity_open) / peak if peak > 0 else 0.0
            net_prof = equity_open - cfg.capital
            if current_dd >= 0.025:
                trade_risk = 15.0
            elif net_prof >= 50.0:
                trade_risk = 45.0 if len(positions) == 0 else 24.0
            else:
                trade_risk = 35.0 if len(positions) == 0 else 20.0
            qty = trade_risk / unit_loss
            gross = sum(p["qty"]*current_refs[a] for a, p in positions.items())
            if gross + qty*o > cfg.max_gross_leverage*equity_open or equity_open <= peak*(1-cfg.circuit_fraction):
                continue
            entry_fill = o*(1+side*cfg.entry_slip)
            fee = cfg.fee*qty*entry_fill
            p = {"side": side, "qty": qty, "entry_ref": o, "entry_fill": entry_fill,
                 "entry_time_ms": int(t), "signal_time_ms": int(t-BAR_MS),
                 "entry_fee": fee, "funding": 0.0, "initial_stop": stop, "stop": stop,
                 "initial_risk_usd": trade_risk, "sleeve": int(sig[ix["sleeve"]]),
                 "max_net_r": -math.inf, "exit_next": ""}
            p["target"] = price_for_net_r(p, cfg.target_r, cfg)
            positions[s] = p
            cash -= fee
            max_open = max(max_open, len(positions))
        # Adverse bound includes open gaps, but assumes a standing stop works
        # at its level (plus specified slippage) once the bar has opened.
        adverse_refs = {}
        for s, p in positions.items():
            b = bars[s]
            extreme = b[ix["low"]] if p["side"] > 0 else b[ix["high"]]
            adverse_refs[s] = max(extreme, p["stop"]) if p["side"] > 0 else min(extreme, p["stop"])
        adverse = marked(adverse_refs)
        bound_dd = max(0.0, (peak-adverse)/peak*100)
        for s, p in list(positions.items()):
            b = bars[s]
            long = p["side"] > 0
            stop_hit = b[ix["low"]] <= p["stop"] if long else b[ix["high"]] >= p["stop"]
            target_hit = b[ix["high"]] >= p["target"] if long else b[ix["low"]] <= p["target"]
            if stop_hit:
                close_position(s, p["stop"], int(t+BAR_MS-1), "stop")
                continue
            if target_hit:
                # No favorable price improvement from a target gap is assumed.
                close_position(s, p["target"], int(t+BAR_MS-1), "target")
                continue
            favorable = b[ix["high"]] if long else b[ix["low"]]
            p["max_net_r"] = max(p["max_net_r"], net_pnl(p, favorable, cfg)/cfg.risk_usd)
            age = (t-p["entry_time_ms"])//BAR_MS+1
            if age >= cfg.max_hold_bars:
                # Close now at this completed close: a precommitted deadline,
                # not a decision using this close for same-bar execution.
                close_position(s, b[ix["close"]], int(t+BAR_MS-1), "max_hold")
                continue
            if age >= cfg.decay_bars and p["max_net_r"] < 0.2:
                p["exit_next"] = "time_decay"
            # These newly computed stops are never evaluated on this candle.
            if cfg.ratchet:
                lock = 0.80 if p["max_net_r"] >= 1.40 else (0.25 if p["max_net_r"] >= 0.90 else None)
                proposal = p["stop"]
                if lock is not None:
                    proposal = price_for_net_r(p, lock, cfg)
                if p["max_net_r"] >= 2.0:
                    trail = min(b[ix["swing_low"]], b[ix["e21"]]-0.25*b[ix["atr"]]) if long else max(b[ix["swing_high"]], b[ix["e21"]]+0.25*b[ix["atr"]])
                    proposal = max(proposal, trail) if long else min(proposal, trail)
                p["stop"] = max(p["stop"], proposal) if long else min(p["stop"], proposal)
        if k == len(grid):
            for s in list(positions):
                close_position(s, bars[s][ix["close"]], int(t+BAR_MS-1), "window_end")
        close_refs = {s: bars[s][ix["close"]] for s in positions}
        eq = marked(close_refs)
        peak = max(peak, eq)
        close_dd = (peak-eq)/peak
        if close_dd >= cfg.circuit_fraction or bound_dd >= cfg.circuit_fraction*100:
            halted = True
        curve.append({"time_ms": int(t+BAR_MS-1), "equity": eq, "cash": cash,
                      "open_positions": len(positions), "drawdown_percent": close_dd*100,
                      "adverse_bound_equity": adverse, "adverse_bound_dd_percent": bound_dd})
    metrics = score_metrics(trades, curve, cfg)
    metrics.update(max_concurrent_positions=max_open, circuit_tripped=halted)
    if trades and not math.isclose(sum(t["net_pnl"] for t in trades), cash-cfg.capital, abs_tol=1e-7):
        raise AssertionError("Trade ledger does not reconcile to cash")
    return {"metrics": metrics, "trades": trades, "equity": curve}


def load_history(data_dir: Path, end_ms: int) -> tuple[dict[str, pd.DataFrame], list[dict]]:
    """Read only the requested prefix from genuine parquet tables."""
    import pyarrow.parquet as pq
    features = {}
    inventory = []
    for s in (BTC,)+ALTCOINS:
        master_path = data_dir / f"{s}_15m_master_2020_2026.parquet"
        ladder_path = data_dir / f"{s}_15m_footprint_ladder.parquet"
        if not master_path.is_file() or not ladder_path.is_file():
            raise FileNotFoundError(f"Missing genuine master/ladder pair for {s}")
        f = pq.read_table(master_path, columns=MASTER_COLUMNS, filters=[("open_time_ms", "<", end_ms)]).to_pandas()
        ladder = None
        if s != BTC and not f.empty:
            ladder = pq.read_table(ladder_path, columns=["open_time_ms", "is_stacked_buy_imb", "is_stacked_sell_imb"],
                                   filters=[("open_time_ms", "<", end_ms)]).to_pandas()
        features[s] = prepare_features(f, ladder)
        inventory.append({"symbol": s, "rows_loaded": len(f), "start": iso(int(f.open_time_ms.iloc[0])) if len(f) else None,
                          "prefix_end_exclusive": iso(end_ms), "footprint_bars": int(ladder.open_time_ms.nunique()) if ladder is not None else 0})
        print(f"Loaded prefix {s}: {len(f):,} bars", flush=True)
    return features, inventory


def apply_signals(features: dict[str, pd.DataFrame], cfg: Config) -> dict[str, pd.DataFrame]:
    return {s: build_signals(f, features[BTC], cfg) for s, f in features.items() if s != BTC and not f.empty}


def candidate_configs() -> list[Config]:
    """Predeclared finite hypothesis family, identical for all calendar dates."""
    return [replace(Config(), breakout_bars=b, stop_atr=a, target_r=tr, sleeve_mode=s, ratchet=r)
            for b, a, tr, s, r in itertools.product((48, 96), (2.5, 3.0), (2.0, 2.2), ("adaptive", "t1", "t2"), (True,))]


def calibrate(features: dict[str, pd.DataFrame], start: int, end: int, output: Path,
              cfgs: list[Config] | None = None) -> tuple[Config, list[dict]]:
    records = []
    cfgs = cfgs or candidate_configs()
    for i, cfg in enumerate(cfgs):
        result = simulate_window(apply_signals(features, cfg), start, end, cfg)
        m = result["metrics"]
        # Rank only pre-OOS data: lower drawdown and adequate trade frequency
        # constrain the search; no OOS result is an input to this ranking.
        score = (m["net_roi_percent"] - 2*m["adverse_bound_max_dd_percent"]
                 - max(0, 15-m["total_trades"])*0.5)
        records.append({"candidate": i, "config": asdict(cfg), "metrics": m, "training_score": score})
        print(f"IS {i+1}/{len(cfgs)} ROI={m['net_roi_percent']:.2f}% DD={m['max_dd_percent']:.2f}% trades={m['total_trades']}", flush=True)
    records.sort(key=lambda r: (-r["training_score"], r["candidate"]))
    write_json(output / "calibration.json", {"start": iso(start), "end_exclusive": iso(end), "candidates": records})
    return Config(**records[0]["config"]), records


def quarter_windows():
    starts = pd.date_range("2021-01-01", "2026-01-01", freq="QS", tz="UTC")
    return [(f"W{i+1:02d}", f"{a.year}Q{a.quarter}", ms(a), ms(b)) for i, (a, b) in enumerate(zip(starts[:-1], starts[1:]))]


def scorecard_markdown(rows: list[dict]) -> str:
    lines = ["| Window | Period | Net ROI (%) | Max DD (%) | Win Rate (%) | Total Trades | Profit Factor | Verdict |",
             "| ------ | ------ | ----------- | ---------- | ------------ | ------------ | ------------- | ------- |"]
    for row in rows:
        m = row.get("metrics")
        if m is None:
            lines.append(f"| {row['window']} | {row['period']} | — | — | — | — | — | NOT RUN |")
        else:
            pf = f"{m['profit_factor']:.2f}" if math.isfinite(m["profit_factor"]) else "∞"
            lines.append(f"| {row['window']} | {row['period']} | {m['net_roi_percent']:.2f} | {m['max_dd_percent']:.2f} | {m['win_rate_percent']:.2f} | {m['total_trades']} | {pf} | {m['verdict']} |")
    return "\n".join(lines)+"\n"


def run(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    data_dir = Path(args.data_dir)
    raw_contract = json.loads(Path(args.criteria).read_text(encoding="utf-8"))
    t = raw_contract["target_criteria"]
    for key, expected in {"initial_capital_usd": 5000, "base_risk_usd": 50, "min_roi_percent": 10,
                          "max_dd_percent": 5, "min_winrate_percent": 40, "min_r_multiple": 2.0, "min_trades": 15}.items():
        if t[key] != expected:
            raise ValueError(f"Contract changed: {key}")
    windows = quarter_windows()
    train_end = windows[0][2]-PURGE_MS
    train_start = ms("2020-10-15")
    protocol = {"created_utc": pd.Timestamp.now(tz="UTC").isoformat(), "raw_criteria": raw_contract,
                "resolved_contract": {"tradable_symbols": ALTCOINS, "macro_only": BTC,
                 "min_profit_factor": 1.4, "strict_max_dd_percent": 5, "costs": asdict(Config()),
                 "r_interpretation": "minimum planned target net4R; achieved average R reported separately"},
                "training_start": iso(train_start), "training_end_exclusive": iso(train_end),
                "purge_hours": 72, "maximum_holding_hours": 72,
                "candidate_grid": [asdict(c) for c in candidate_configs()],
                "selection": "pre-2021 training score only; freeze before first evaluation",
                "funding_limitation": "8h schedule estimated from last-settled rates; not exact funding events",
                "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    write_json(output / "protocol.json", protocol)
    if args.config:
        cfg = Config(**json.loads(Path(args.config).read_text()))
        ranking = []
    else:
        f, inventory = load_history(data_dir, train_end)
        write_json(output / "training_inventory.json", inventory)
        cfg, ranking = calibrate(f, train_start, train_end, output)
        del f
    write_json(output / "selected_config.json", asdict(cfg))
    if args.calibrate_only:
        return
    rows = []
    all_trades = []
    all_equity = []
    failed = False
    offset = 0.0
    for name, period, start, end in windows:
        if failed:
            rows.append({"window": name, "period": period, "metrics": None})
            continue
        f, inventory = load_history(data_dir, end)
        result = simulate_window(apply_signals(f, cfg), start, end, cfg)
        del f
        m = result["metrics"]
        rows.append({"window": name, "period": period, "metrics": m})
        all_trades.extend([{**x, "window": name} for x in result["trades"]])
        all_equity.extend([{**x, "equity": x["equity"]+offset} for x in result["equity"]])
        offset += m["net_profit_usd"]
        write_json(output / f"{name}_metrics.json", m)
        write_json(output / f"{name}_inventory.json", inventory)
        pd.DataFrame(result["trades"]).to_csv(output / f"{name}_trades.csv", index=False)
        pd.DataFrame(result["equity"]).to_parquet(output / f"{name}_equity.parquet", index=False)
        print(f"{name} {period}: {m['verdict']} ROI={m['net_roi_percent']:.3f}% DD={m['max_dd_percent']:.3f}%", flush=True)
        failed = m["verdict"] != "PASS"
    write_json(output / "scorecard.json", rows)
    (output / "scorecard.md").write_text(scorecard_markdown(rows), encoding="utf-8")
    summary = score_metrics(all_trades, all_equity, cfg)
    summary.update(evaluated_windows=sum(r["metrics"] is not None for r in rows),
                   complete_20_window_validation=not failed, accounting="$5000 reset each quarter; USD PnL stitched additively for evaluated prefix",
                   annualization="extrapolation of evaluated prefix only, not a five-year realized return")
    write_json(output / "portfolio_statistics.json", summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="Engine/binance_backtesting_data")
    parser.add_argument("--criteria", default="Engine/target_oos_criteria.json")
    parser.add_argument("--output", default="Engine/trend_suite_results")
    parser.add_argument("--config", help="Previously frozen JSON Config; skips calibration")
    parser.add_argument("--calibrate-only", action="store_true")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
