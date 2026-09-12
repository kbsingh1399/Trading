"""Portfolio execution kernel for the levels / POC lab.

This is a deliberate clone of the certified event loop in
``Engine/s1_trend_following_suite.py`` (next-open fills, stop-first bars,
adverse-bound drawdown, funding at 8h settlements, friction floor) with the risk
schedule parameterised so the lab can study the *economics* of the mission
criteria without weakening the cost model.

Cost model, fills and rejection rules are imported from the certified suite --
they are not re-implemented here.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Engine.s1_trend_following_suite import (  # noqa: E402
    BAR_MS,
    Config,
    execution_values,
    net_pnl,
    price_for_net_r,
    score_metrics,
)

CERTIFIED = Config()  # fee 8 bps, entry slip 10 bps, exit slip 15 bps, floor 41 bps


@dataclass(frozen=True)
class LabConfig:
    capital: float = 5000.0
    base_risk_usd: float = 50.0
    max_positions: int = 3
    max_gross_leverage: float = 3.0
    dd_limit: float = 0.05
    circuit_fraction: float = 0.045
    target_r: float = 4.0
    max_hold_bars: int = 288
    cooldown_bars: int = 8
    ratchet: bool = True
    trail: bool = True
    funding: bool = True
    # SSRN 4824172 (effective intraday momentum) / SSRN 2440866: ride winners with a
    # dynamic trailing stop instead of exiting at the fixed profit target.
    ride_winners: bool = False
    ride_lock_r: float = 3.0      # stop lock once the configured target is reached
    vwap_trail: bool = False      # swing/EMA trail anchored additionally to session VWAP
    trail_after_r: float = 2.0
    # risk schedule
    cost_profile: str = "certified"  # certified (41 bps) | realistic (15 bps) | zero
    risk_mode: str = "flat"          # flat | dd_scaled | dd_budget
    risk_scale: float = 1.0          # multiplier on base_risk_usd
    risk_ceiling_usd: float = 200.0
    champion_mode: bool = True       # risk up while ahead, down while behind
    max_concurrent_risk_frac: float = 0.04   # total open risk <= 4 % of capital
    # Reservation schedule for the scarce slots: with 2-3 concurrent positions the
    # kernel otherwise fills a free slot with whatever candidate arrives first,
    # which makes the gate's cross-sectional ranking nearly irrelevant.  With
    # ``reserve`` the required score starts at ``reserve_hi`` and decays linearly to
    # ``reserve_lo`` across the window, so early slots go to the best candidates and
    # the remaining slots are filled late with the best of what is left.
    reserve: bool = False
    reserve_hi: float = 1.0
    reserve_lo: float = 0.0


def simulate(data: dict[str, pd.DataFrame], start_ms: int, end_ms: int, cfg: LabConfig,
             certified: Config | None = None) -> dict:
    """Event loop over one OOS window. ``end_ms`` is inclusive here."""
    cert = replace(certified or CERTIFIED, target_r=cfg.target_r,
                   max_positions=cfg.max_positions, max_hold_bars=cfg.max_hold_bars,
                   cooldown_bars=cfg.cooldown_bars, dd_limit=cfg.dd_limit,
                   circuit_fraction=cfg.circuit_fraction, funding_8h=cfg.funding,
                   ratchet=cfg.ratchet)
    # Cost profile sensitivity: "certified" is the mission contract and is never
    # weakened in the headline results; "realistic" models a retail taker on
    # liquid Binance perps (4 bps/side fee, 2/4 bps slippage, 15 bps floor).
    if cfg.cost_profile == "realistic":
        for k, v in (("fee", 0.0004), ("entry_slip", 0.0002), ("exit_slip", 0.0004),
                     ("friction_floor", 0.0015)):
            object.__setattr__(cert, k, v)
    elif cfg.cost_profile == "zero":
        for k in ("fee", "entry_slip", "exit_slip", "friction_floor"):
            object.__setattr__(cert, k, 0.0)
    grid = np.arange(start_ms, end_ms, BAR_MS, dtype=np.int64)  # end exclusive, as certified
    cols = ["open", "high", "low", "close", "signal", "score", "stop_distance",
            "e21", "atr", "swing_low", "swing_high", "funding_rate_pct", "sess_vwap"]
    arrays = {}
    fullgrid = np.r_[start_ms - BAR_MS, grid]
    for s, f in data.items():
        if not f.empty:
            arrays[s] = f.set_index("open_time_ms").reindex(fullgrid)[cols].to_numpy(float)
    ix = {c: i for i, c in enumerate(cols)}

    positions: dict[str, dict] = {}
    cooldown = {s: -1 for s in arrays}
    portfolio_cooldown = -1
    cash = cfg.capital
    peak = cfg.capital
    halted = False
    trades = []
    curve = []
    max_open = 0

    def close_position(symbol: str, raw: float, t: int, reason: str):
        nonlocal cash
        p = positions.pop(symbol)
        vals = execution_values(p["entry_ref"], raw, p["side"], cert)
        net = net_pnl(p, raw, cert)
        cash += net + p["entry_fee"] + p["funding"]
        trades.append({**p, "symbol": symbol, "exit_time_ms": int(t), "exit_ref": raw,
                       "exit_fill": vals["exit_fill"], "net_pnl": net,
                       "net_r": net / p["initial_risk_usd"], "exit_reason": reason,
                       "fees": p["qty"] * vals["fees"],
                       "slippage": p["qty"] * vals["slippage"],
                       "friction_topup": p["qty"] * vals["friction_topup"]})
        cooldown[symbol] = t + cfg.cooldown_bars * BAR_MS

    def marked(refs: dict[str, float]) -> float:
        return cash + sum(net_pnl(p, refs[s], cert) + p["entry_fee"] + p["funding"]
                          for s, p in positions.items())

    for k, t in enumerate(grid, start=1):
        bars = {s: a[k] for s, a in arrays.items() if np.isfinite(a[k, ix["open"]])}
        if any(s not in bars for s in positions):
            missing = set(positions) - set(bars)
            raise ValueError(f"Missing valuation bar for held symbols: {missing}")
        if cfg.funding and t % (8 * 3_600_000) == 0:
            for s, p in positions.items():
                cost = p["side"] * p["qty"] * bars[s][ix["open"]] * bars[s][ix["funding_rate_pct"]] / 100.0
                p["funding"] += cost
                cash -= cost
        for s, p in list(positions.items()):
            b = bars[s]
            o = b[ix["open"]]
            if halted or p.get("exit_next"):
                close_position(s, o, int(t), "circuit" if halted else p["exit_next"])
            elif p["side"] * (o - p["stop"]) <= 0:
                close_position(s, o, int(t), "gap_stop")
        open_refs = {s: bars[s][ix["open"]] for s in positions}
        if marked(open_refs) <= peak * (1 - cfg.circuit_fraction):
            halted = True
            for s in list(positions):
                close_position(s, bars[s][ix["open"]], int(t), "open_circuit")

        candidates = []
        if not halted and k < len(grid):
            for s, a in arrays.items():
                prev = a[k - 1]
                if (s in bars and s not in positions and t >= cooldown[s]
                        and np.isfinite(prev[ix["signal"]]) and prev[ix["signal"]] != 0):
                    candidates.append((float(prev[ix["score"]]), s, prev))

        frac = ((t - start_ms) / max(1, end_ms - start_ms)) if (cfg.reserve and end_ms > start_ms) else 0.0
        need = cfg.reserve_hi + (cfg.reserve_lo - cfg.reserve_hi) * min(1.0, max(0.0, frac))
        for score_, s, sig in sorted(candidates, key=lambda x: (-x[0], x[1])):
            if cfg.reserve and score_ < need:
                continue
            if len(positions) >= cfg.max_positions:
                break
            side = int(sig[ix["signal"]])
            o = float(bars[s][ix["open"]])
            distance = float(sig[ix["stop_distance"]])
            if not math.isfinite(distance) or distance <= 0 or o - distance <= 0:
                continue
            stop = o - side * distance
            unit_loss = -execution_values(o, stop, side, cert)["net_per_unit"]
            if unit_loss <= 0:
                continue
            current_refs = {a: bars[a][ix["open"]] for a in positions}
            equity_open = marked(current_refs)
            current_dd = (peak - equity_open) / peak if peak > 0 else 0.0
            risk_usd = _risk_for(cfg, equity_open, peak, current_dd, len(positions), cert)
            open_risk = sum(p["initial_risk_usd"] for p in positions.values())
            room = cfg.capital * cfg.max_concurrent_risk_frac - open_risk
            risk_usd = max(0.0, min(risk_usd, room))
            if risk_usd <= 0:
                continue
            qty = risk_usd / unit_loss
            gross = sum(p["qty"] * current_refs[a] for a, p in positions.items())
            if gross + qty * o > cfg.max_gross_leverage * equity_open:
                continue
            if equity_open <= peak * (1 - cfg.circuit_fraction):
                continue
            entry_fill = o * (1 + side * cert.entry_slip)
            fee = cert.fee * qty * entry_fill
            p = {"side": side, "qty": qty, "entry_ref": o, "entry_fill": entry_fill,
                 "entry_time_ms": int(t), "signal_time_ms": int(t - BAR_MS),
                 "entry_fee": fee, "funding": 0.0, "initial_stop": stop, "stop": stop,
                 "initial_risk_usd": risk_usd, "sleeve": int(sig[ix["signal"]]),
                 "max_net_r": -math.inf, "exit_next": ""}
            p["target"] = price_for_net_r(p, cfg.target_r, cert)
            positions[s] = p
            cash -= fee
            max_open = max(max_open, len(positions))

        adverse_refs = {}
        for s, p in positions.items():
            b = bars[s]
            extreme = b[ix["low"]] if p["side"] > 0 else b[ix["high"]]
            adverse_refs[s] = max(extreme, p["stop"]) if p["side"] > 0 else min(extreme, p["stop"])
        adverse = marked(adverse_refs)
        bound_dd = max(0.0, (peak - adverse) / peak * 100)

        for s, p in list(positions.items()):
            b = bars[s]
            long = p["side"] > 0
            stop_hit = b[ix["low"]] <= p["stop"] if long else b[ix["high"]] >= p["stop"]
            target_hit = b[ix["high"]] >= p["target"] if long else b[ix["low"]] <= p["target"]
            if stop_hit:
                close_position(s, p["stop"], int(t + BAR_MS - 1), "stop")
                continue
            if target_hit:
                if cfg.ride_winners and not p.get("ridden"):
                    # Convert the fixed target into a locked, trailing stop and keep
                    # the position open: the level-break drift persists for days
                    # (see REPORT.md impulse study) but rarely stops exactly at 4R.
                    p["ridden"] = True
                    lock_price = price_for_net_r(p, cfg.ride_lock_r, cert)
                    p["stop"] = max(p["stop"], lock_price) if long else min(p["stop"], lock_price)
                else:
                    close_position(s, p["target"], int(t + BAR_MS - 1), "target")
                    continue
            favorable = b[ix["high"]] if long else b[ix["low"]]
            p["max_net_r"] = max(p["max_net_r"], net_pnl(p, favorable, cert) / p["initial_risk_usd"])
            age = (t - p["entry_time_ms"]) // BAR_MS + 1
            if age >= cfg.max_hold_bars:
                close_position(s, b[ix["close"]], int(t + BAR_MS - 1), "max_hold")
                continue
            if cfg.ratchet:
                lock = 0.80 if p["max_net_r"] >= 1.40 else (0.25 if p["max_net_r"] >= 0.90 else None)
                proposal = p["stop"]
                if lock is not None:
                    proposal = price_for_net_r(p, lock, cert)
                if cfg.trail and (p["max_net_r"] >= cfg.trail_after_r or p.get("ridden")):
                    trail = (min(b[ix["swing_low"]], b[ix["e21"]] - 0.25 * b[ix["atr"]]) if long
                             else max(b[ix["swing_high"]], b[ix["e21"]] + 0.25 * b[ix["atr"]]))
                    if cfg.vwap_trail and math.isfinite(b[ix["sess_vwap"]]):
                        vw = b[ix["sess_vwap"]] - 0.25 * b[ix["atr"]] if long else b[ix["sess_vwap"]] + 0.25 * b[ix["atr"]]
                        trail = max(trail, vw) if long else min(trail, vw)
                    proposal = max(proposal, trail) if long else min(proposal, trail)
                p["stop"] = max(p["stop"], proposal) if long else min(p["stop"], proposal)
        if k == len(grid):
            for s in list(positions):
                close_position(s, bars[s][ix["close"]], int(t + BAR_MS - 1), "window_end")
        close_refs = {s: bars[s][ix["close"]] for s in positions}
        eq = marked(close_refs)
        peak = max(peak, eq)
        close_dd = (peak - eq) / peak
        if close_dd >= cfg.circuit_fraction or bound_dd >= cfg.circuit_fraction * 100:
            halted = True
        curve.append({"time_ms": int(t + BAR_MS - 1), "equity": eq, "cash": cash,
                      "open_positions": len(positions), "drawdown_percent": close_dd * 100,
                      "adverse_bound_equity": adverse, "adverse_bound_dd_percent": bound_dd})

    metrics = score_metrics(trades, curve, cert)
    metrics.update(max_concurrent_positions=max_open, circuit_tripped=halted,
                   final_equity=float(curve[-1]["equity"]) if curve else cfg.capital)
    if trades and not math.isclose(sum(t["net_pnl"] for t in trades), cash - cfg.capital, abs_tol=1e-6):
        raise AssertionError("Trade ledger does not reconcile to cash")
    return {"metrics": metrics, "trades": trades, "equity": curve}


def _risk_for(cfg: LabConfig, equity: float, peak: float, dd: float, open_positions: int,
              cert: Config) -> float:
    """Risk per trade in USD under the configured schedule."""
    base = cfg.base_risk_usd * cfg.risk_scale
    if cfg.risk_mode == "flat":
        return min(base, cfg.risk_ceiling_usd)
    if cfg.risk_mode == "dd_scaled":
        # scale down as drawdown grows: 1.0 at no DD, 0.4 at the 4.5 % circuit
        scale = max(0.4, 1.0 - dd / max(cfg.circuit_fraction, 1e-9) * 0.6)
        return min(base * scale, cfg.risk_ceiling_usd)
    if cfg.risk_mode == "dd_budget":
        # never risk more than a third of the remaining distance to the hard floor
        room = max(0.0, (peak * (1 - cfg.circuit_fraction)) - equity)
        return min(base, max(0.0, room / 3.0), cfg.risk_ceiling_usd)
    raise ValueError(cfg.risk_mode)


def prepare_execution_frame(f: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    """Join the signal columns onto the certified execution inputs."""
    out = signals.copy()
    out["e21"] = f.ema_21.to_numpy(float)
    out["atr"] = np.maximum(f.atr.to_numpy(float), f.close.to_numpy(float) * 0.004)
    out["swing_low"] = f.low.rolling(4).min().to_numpy(float)
    out["swing_high"] = f.high.rolling(4).max().to_numpy(float)
    out["funding_rate_pct"] = f.funding_rate_pct.to_numpy(float)
    out["sess_vwap"] = f.sess_vwap.to_numpy(float)
    return out
