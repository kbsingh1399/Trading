"""OX63 harness: F6R signals (P11), scaled candidates (P4-P8), dual-economics replay (P13-P14).
Entry/SL/floor/Friday/KZ/friction mechanics are verbatim copies of the OX62 code path;
the ONLY deltas are marked DELTA-OX63 below (veto 1.20, scaled exits, scaled flag).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "ox62_research"))

from Engine.core.strategy_kernel import (
    CANONICAL_18_ASSETS, MAX_STOP_PCT, MIN_R_MULTIPLE,
    UX_MAX_R_EFF, UX_MIN_R_EFF_SCALED, _ux_exit_scaled_long, _ux_exit_scaled_short,
)
from Engine.core.base_strategy import EngineConfig, ParallelForexStrategy, FOREX_CLUSTER_MAP
from ox62_lib import load_frame, add_harness_cols, SPAN_END  # noqa: F401  (identical code path)

HERE = Path(__file__).parent
RISK_RESEARCH_USD = 50.0
RISK_PRODUCTION_USD = 10.0
INITIAL_CAPITAL_USD = 5000.0


def _b(x):
    return pd.Series(np.asarray(x, dtype=bool), index=getattr(x, "index", None))


def add_msb_anchor(df):
    """20-bar 4H-close Donchian break on the shifted as-of series (P3). Causal: every
    term reads bars <= i only (shift/rolling are trailing). NaN -> False by comparison."""
    a = df["close_4h_asof"]
    trailing_max = a.shift(1).rolling(20, min_periods=20).max()
    trailing_min = a.shift(1).rolling(20, min_periods=20).min()
    df["msb_up"] = _b(a > trailing_max)
    df["msb_dn"] = _b(a < trailing_min)
    return df


def sig_F6R(df):
    """F6{d:1.0} with htf>0 -> (htf>0 | msb) (P11, mandate M3.1). Expansion: F6 => F6R."""
    disp = (df["high"] - df["low"]) > 1.0 * df["atr_14"]
    base_l = (df["sweep_pdl"] == 1) & (df["close"] > df["pdl"]) & disp
    base_s = (df["sweep_pdh"] == 1) & (df["close"] < df["pdh"]) & disp
    anchor_l = (df["htf_4h_trend"] > 0) | (df["msb_up"])
    anchor_s = (df["htf_4h_trend"] < 0) | (df["msb_dn"])
    return (_b(base_l & anchor_l), _b(base_s & anchor_s))


def generate_candidates_scaled(df, long_mask, short_mask, span_start):
    """Live-spec candidate generation with 2-stage scaled exits (P4-P8).
    Verbatim OX62 plumbing except DELTA-OX63 marks."""
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
            if r_eff < UX_MIN_R_EFF_SCALED:  # DELTA-OX63 (P4): veto 1.20, was MIN_R_MULTIPLE 2.50
                continue
            tp = entry + min(r_eff, UX_MAX_R_EFF) * r if is_long else entry - min(r_eff, UX_MAX_R_EFF) * r
        else:
            tp = entry + MIN_R_MULTIPLE * r if is_long else entry - MIN_R_MULTIPLE * r
        if not np.isfinite(tp):
            continue
        fn = _ux_exit_scaled_long if is_long else _ux_exit_scaled_short  # DELTA-OX63 (P5-P8)
        res = fn(opens, highs, lows, closes, dows, hrs, mns, n, e, entry, sl0, tp, r)
        if res is None:
            continue  # data-end truncation: no candidate
        r_pre, exit_j, reason, scaled = res  # DELTA-OX63: 4-tuple
        rows.append({"datetime": sig_dt, "signal": 1 if is_long else -1,
                     "r_realized": round(r_pre - 0.08, 4), "hold_bars": int(exit_j - e),
                     "exit_reason": int(reason), "scaled": bool(scaled)})  # DELTA-OX63: scaled flag
    return pd.DataFrame(rows)


def replay_economics(cand, cfg, tag, base_risk_usd):
    """Filed per-window replay under one economics (P13). Returns (scorecard_df, executed_df).
    Mechanics = OX62 replay_family + trades capture; only base_risk differs."""
    cfg.criteria.base_risk_usd = base_risk_usd
    cfg.criteria.initial_capital_usd = INITIAL_CAPITAL_USD
    c = cand.copy()
    c["sleeve"] = tag
    c["cluster"] = c["asset"].map(lambda x: FOREX_CLUSTER_MAP.get(x, "OTHER"))
    c["datetime"] = pd.to_datetime(c["datetime"], utc=True)
    c = c.sort_values("datetime").reset_index(drop=True)
    strat = ParallelForexStrategy(config=cfg)
    strat._cached_candidate_trades = c
    score_rows, exec_frames = [], []
    for w in cfg.windows:
        res = strat.run_backtest(start_date=w.start_date, end_date=w.end_date, save_plot=False)
        score_rows.append({"window_id": w.window_id, "window": f"W{w.window_id:02d}", "name": w.name,
                           "trades": res.total_trades, "win_rate": res.win_rate, "net_r": res.net_r,
                           "pnl_usd": res.net_pnl_usd, "roi_pct": res.net_roi_pct,
                           "max_dd_pct": res.max_dd_pct,
                           "status": "PASS" if res.passed_criteria else "FAIL",
                           "failures": "; ".join(res.failure_reasons)})
        if res.trades_df is not None and not res.trades_df.empty:
            tdf = res.trades_df.copy()
            tdf["window_id"] = w.window_id
            exec_frames.append(tdf)
    score = pd.DataFrame(score_rows)
    executed = (pd.concat(exec_frames, ignore_index=True).sort_values("datetime").reset_index(drop=True)
                if exec_frames else pd.DataFrame())
    return score, executed


def portfolio_metrics(executed, label):
    """Continuous-equity portfolio metrics from filed executions (P13 + A1)."""
    if executed.empty:
        return {"economics": label, "trades": 0, "sharpe": 0.0, "profit_factor": 0.0,
                "max_dd_pct": 0.0, "annual": {}, "net_pnl": 0.0, "net_r": 0.0}
    ex = executed.sort_values("datetime").reset_index(drop=True)
    ex["equity"] = INITIAL_CAPITAL_USD + ex["pnl_usd"].cumsum()
    ex["peak"] = ex["equity"].cummax()
    max_dd_pct = float(((ex["peak"] - ex["equity"]) / ex["peak"]).max() * 100.0)
    gp = float(ex.loc[ex["pnl_usd"] > 0, "pnl_usd"].sum())
    gl = float(-ex.loc[ex["pnl_usd"] < 0, "pnl_usd"].sum())
    pf = float(gp / gl) if gl > 0 else (99.9 if gp > 0 else 0.0)
    # Sharpe on Mon-Fri daily returns vs running start-of-day equity (A1)
    d = ex.copy()
    d["day"] = pd.to_datetime(d["datetime"], utc=True).dt.floor("D")
    daily_pnl = d.groupby("day")["pnl_usd"].sum()
    daily_eq = INITIAL_CAPITAL_USD + daily_pnl.cumsum().shift(1, fill_value=0.0)
    rets = daily_pnl / daily_eq
    rets = rets[[i for i in rets.index if i.weekday() < 5]]
    if len(rets) < 2 or float(rets.std(ddof=1)) <= 0:
        sharpe = 0.0
    else:
        sharpe = float(rets.mean() / rets.std(ddof=1) * np.sqrt(252))
    d["year"] = pd.to_datetime(d["datetime"], utc=True).dt.year
    annual = {int(y): round(float(g["pnl_usd"].sum()), 2) for y, g in d.groupby("year")}
    return {"economics": label, "trades": len(ex), "sharpe": round(sharpe, 3),
            "profit_factor": round(pf, 3), "max_dd_pct": round(max_dd_pct, 2),
            "annual": annual, "net_pnl": round(float(ex["pnl_usd"].sum()), 2),
            "net_r": round(float(ex["r_realized"].sum()), 2)}
