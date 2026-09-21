"""OX62 shared harness: causal features, live-spec exits, candidate gen, frozen replay.
All families share this code path; families differ ONLY in entry signals (protocol §2).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Engine.core.strategy_kernel import (
    CANONICAL_18_ASSETS, engineer_features_polars, check_setup_criteria,
    _ux_exit_long, _ux_exit_short, MIN_R_MULTIPLE, MAX_STOP_PCT,
)
from Engine.core.strategy_kernel import UX_MAX_R_EFF
from Engine.core.base_strategy import EngineConfig, ParallelForexStrategy, FOREX_CLUSTER_MAP

DATA_DIR = str(PROJECT_ROOT / "Forex_Backtesting_Data")
HERE = Path(__file__).parent

OX62_BASE_RISK_USD = 50.0  # OX61 economics (protocol §1.8; tip $10 recorded in manifest)
SPAN_END = pd.Timestamp("2026-03-31", tz="UTC")  # protocol amendment 1: clip


def load_frame(sym):
    df = engineer_features_polars(sym, DATA_DIR)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    return df.sort_values("datetime").reset_index(drop=True)


def add_harness_cols(df):
    """Trailing-only indicators. All causal by construction (no future input)."""
    c = df["close"]
    for s in (12, 20, 24, 48, 96):
        df[f"ema_{s}"] = c.ewm(span=s, adjust=False, min_periods=1).mean()
    for n in (20, 55):
        df[f"hh_{n}"] = df["high"].shift(1).rolling(n, min_periods=n).max()
        df[f"ll_{n}"] = df["low"].shift(1).rolling(n, min_periods=n).min()
    # Prior-calendar-day extremes (causal groupby-shift, mirrors kernel streaming path)
    df["_day"] = df["datetime"].dt.floor("D")
    daily = df.groupby("_day").agg({"high": "max", "low": "min"}).shift(1)
    df["pdh"] = df["_day"].map(daily["high"])
    df["pdl"] = df["_day"].map(daily["low"])
    # Session map for F7 (calendar-fixed 10:45 bar = causal 'last hour-10 bar')
    dt = df["datetime"]
    df["_hh"] = dt.dt.hour.values
    df["_mn"] = dt.dt.minute.values
    df["_dow"] = dt.dt.weekday.values
    sess = df[df["_hh"] == 7].groupby("_day")["open"].first()
    df["_sess_open"] = df["_day"].map(sess)
    return df


def generate_candidates(df, long_mask, short_mask, span_start):
    """Live-spec candidate generation (protocol §2). Returns candidate rows."""
    n = len(df)
    opens = df["open"].values
    highs = df["high"].values
    lows = df["low"].values
    closes = df["close"].values
    lo20 = df["local_low_20"].values
    hi20 = df["local_high_20"].values
    atr14 = df["atr_14"].values
    kz = df["is_kill_zone"].values
    dts = df["datetime"]
    dows = dts.dt.weekday.values
    hrs = dts.dt.hour.values
    mns = dts.dt.minute.values
    lm = np.asarray(long_mask, dtype=bool)
    sm = np.asarray(short_mask, dtype=bool)
    rows = []
    for i in np.where(lm | sm)[0]:
        sig_dt = dts.iloc[i]
        if sig_dt < span_start or sig_dt > SPAN_END:
            continue
        if not bool(kz[i]):
            continue
        e = i + 1
        if e >= n:
            continue
        if dows[e] == 4 and hrs[e] >= 18:
            continue  # Friday entry veto (live lockout)
        entry = opens[e]
        is_long = bool(lm[i])
        sl0 = lo20[i] if is_long else hi20[i]
        r = (entry - sl0) if is_long else (sl0 - entry)
        floor = 1.5 * atr14[i]
        if r < floor:
            r = floor
            sl0 = entry - r if is_long else entry + r
        if not np.isfinite(r) or r <= 0 or (r / entry) > MAX_STOP_PCT:
            continue
        tp_struct = hi20[i] if is_long else lo20[i]
        beyond = (tp_struct > entry) if is_long else (tp_struct < entry)
        if beyond:
            r_eff = abs(tp_struct - entry) / r
            if r_eff < MIN_R_MULTIPLE:
                continue
            tp = entry + min(r_eff, UX_MAX_R_EFF) * r if is_long else entry - min(r_eff, UX_MAX_R_EFF) * r
        else:
            tp = entry + MIN_R_MULTIPLE * r if is_long else entry - MIN_R_MULTIPLE * r
        if not np.isfinite(tp):
            continue
        fn = _ux_exit_long if is_long else _ux_exit_short
        res = fn(opens, highs, lows, closes, dows, hrs, mns, n, e, entry, sl0, tp, r)
        if res is None:
            continue  # data-end truncation: no candidate
        r_pre, exit_j, reason = res
        rows.append({"datetime": sig_dt, "signal": 1 if is_long else -1,
                     "r_realized": round(r_pre - 0.08, 4), "hold_bars": int(exit_j - e),
                     "exit_reason": int(reason)})
    return pd.DataFrame(rows)


def replay_family(cand, cfg, tag):
    """Frozen filed replay (protocol §1.4), solo sleeve, OX61 $50 economics."""
    cfg.criteria.base_risk_usd = OX62_BASE_RISK_USD
    c = cand.copy()
    c["sleeve"] = tag
    c["cluster"] = c["asset"].map(lambda x: FOREX_CLUSTER_MAP.get(x, "OTHER"))
    c["datetime"] = pd.to_datetime(c["datetime"], utc=True)
    c = c.sort_values("datetime").reset_index(drop=True)
    strat = ParallelForexStrategy(config=cfg)
    strat._cached_candidate_trades = c
    rows = []
    for w in cfg.windows:
        res = strat.run_backtest(start_date=w.start_date, end_date=w.end_date, save_plot=False)
        rows.append({"window_id": w.window_id, "window": f"W{w.window_id:02d}", "name": w.name,
                     "trades": res.total_trades, "win_rate": res.win_rate, "net_r": res.net_r,
                     "pnl_usd": res.net_pnl_usd, "roi_pct": res.net_roi_pct,
                     "max_dd_pct": res.max_dd_pct,
                     "status": "PASS" if res.passed_criteria else "FAIL",
                     "failures": "; ".join(res.failure_reasons)})
    return pd.DataFrame(rows)


def pool_stats(cand):
    r = cand["r_realized"].values
    return {"n": len(cand), "avgR": round(float(r.mean()), 4),
            "WR": round(100 * float((r > 0).mean()), 1),
            "netR": round(float(r.sum()), 2)}
