"""OX64 harness: candidates A (TSMOM-12M), B (daily reversal), C (vol-managed F6).
Implements docs/ox64_research/PROTOCOL.md §3 exactly. Reuses OX62/OX63 code paths for
all shared mechanics (frames, F6R signals, monolithic/scaled exits, replay, metrics).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "ox62_research"))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "ox63_research"))

from Engine.core.strategy_kernel import CANONICAL_18_ASSETS  # noqa: F401
from Engine.core.base_strategy import EngineConfig  # noqa: F401
from ox62_lib import load_frame, add_harness_cols, generate_candidates, SPAN_END, pool_stats  # noqa: F401
from ox63_lib import (add_msb_anchor, sig_F6R, generate_candidates_scaled, replay_economics,  # noqa: F401
                      portfolio_metrics, RISK_RESEARCH_USD, RISK_PRODUCTION_USD)

HERE = Path(__file__).parent
HORIZON_REASON = 4  # Q5: hold-to-horizon exit (replay ignores; disclosure only)


def daily_bars(df15):
    """Resample 15m frame to UTC-day OHLC + bar positions. Q0: trading day = ≥10 bars."""
    d = df15[["datetime", "open", "high", "low", "close"]].copy()
    d["datetime"] = pd.to_datetime(d["datetime"], utc=True)
    d["_day"] = d["datetime"].dt.floor("D")
    d["__pos__"] = np.arange(len(d))
    daily = (d.groupby("_day")
             .agg(day_open=("open", "first"), day_high=("high", "max"),
                  day_low=("low", "min"), day_close=("close", "last"),
                  n_bars=("close", "size"), first_idx=("__pos__", "first"),
                  last_idx=("__pos__", "last"))
             .reset_index().sort_values("_day").reset_index(drop=True))
    daily["trading"] = daily["n_bars"] >= 10
    return daily


def add_trailing_stats(daily):
    """Causal trailing stats on the trading-day frame (every term reads days ≤ i only)."""
    t = daily[daily["trading"]].copy().reset_index(drop=True)
    t["_pos"] = np.arange(len(t))
    c = t["day_close"]
    t["day_ret"] = c / c.shift(1) - 1
    t["sigma20"] = t["day_ret"].rolling(20, min_periods=20).std(ddof=1)
    t["atr20"] = (t["day_high"] - t["day_low"]).rolling(20, min_periods=15).mean()
    t["med60sig"] = t["sigma20"].rolling(60, min_periods=40).median()
    t["form12M"] = c / c.shift(252) - 1
    return t


def _first_kz_after(kz, pos, n):
    j = int(pos) + 1
    while j < n and not bool(kz[j]):
        j += 1
    return j if j < n else None


def generate_candidates_A(df15, t, span_start):
    """TSMOM-12M: month-end sign(12M formation), 1-calendar-month hold, no SL/TP."""
    rows = []
    n = len(df15)
    opens = df15["open"].values
    closes = df15["close"].values
    kz = df15["is_kill_zone"].values
    ym_pos = {}
    for ym, g in t.groupby(t["_day"].dt.strftime("%Y-%m")):
        ym_pos[ym] = int(g["_pos"].iloc[-1])
    for ym, spos in ym_pos.items():
        S = t.iloc[spos]
        if S["_day"] < span_start or S["_day"] > SPAN_END:
            continue
        f = S["form12M"]
        if not np.isfinite(f) or f == 0.0:  # Q1
            continue
        direction = 1 if f > 0 else -1
        ym_next = (S["_day"] + pd.offsets.MonthBegin(1)).strftime("%Y-%m")
        if ym_next not in ym_pos:
            continue
        E = t.iloc[ym_pos[ym_next]]
        R = 1.5 * S["atr20"]  # Q4
        if not np.isfinite(R) or R <= 0:
            continue
        j = _first_kz_after(kz, S["last_idx"], n)
        if j is None:
            continue
        entry = opens[j]
        e_last = int(E["last_idx"])
        if e_last <= j:
            continue
        r_pre = direction * (closes[e_last] - entry) / R  # A1(a)
        rows.append({"datetime": S["_day"], "signal": direction,
                     "r_realized": round(r_pre - 0.08, 4), "hold_bars": int(e_last - j),
                     "exit_reason": HORIZON_REASON})
    return pd.DataFrame(rows)


def generate_candidates_B(df15, t, span_start):
    """Daily short-term reversal: fade prior-day move beyond 0.5σ, hold 1 trading day."""
    rows = []
    n = len(df15)
    opens = df15["open"].values
    closes = df15["close"].values
    kz = df15["is_kill_zone"].values
    for i in range(1, len(t) - 1):
        S = t.iloc[i]
        if S["_day"] < span_start or S["_day"] > SPAN_END:
            continue
        f = S["day_ret"]
        sig = S["sigma20"]
        if not np.isfinite(f) or not np.isfinite(sig) or sig <= 0:
            continue
        if abs(f) <= 0.5 * sig:  # Q2
            continue
        direction = -1 if f > 0 else 1
        E = t.iloc[i + 1]
        R = 1.5 * S["atr20"]  # Q4
        if not np.isfinite(R) or R <= 0:
            continue
        j = _first_kz_after(kz, S["last_idx"], n)
        if j is None:
            continue
        entry = opens[j]
        e_last = int(E["last_idx"])
        if e_last <= j:
            continue
        r_pre = direction * (closes[e_last] - entry) / R  # A1(a)
        rows.append({"datetime": S["_day"], "signal": direction,
                     "r_realized": round(r_pre - 0.08, 4), "hold_bars": int(e_last - j),
                     "exit_reason": HORIZON_REASON})
    return pd.DataFrame(rows)


def generate_candidates_C(df15h, t, span_start, scaled=False):
    """Vol-managed F6: F6R + verbatim OX62 (or OX63-scaled) geometry, R rescaled by mult."""
    lm, sm = sig_F6R(df15h)
    gen = generate_candidates_scaled if scaled else generate_candidates
    base = gen(df15h, lm, sm, span_start)
    if len(base) == 0:
        return base
    stat = {row["_day"]: (row["sigma20"], row["med60sig"]) for _, row in t.iterrows()}
    mults = []
    for sig_dt in base["datetime"]:
        day = pd.Timestamp(sig_dt).floor("D")
        s, m = stat.get(day, (np.nan, np.nan))
        if not np.isfinite(s) or not np.isfinite(m) or m <= 0:
            mults.append(1.0)  # Q3 neutral
        else:
            mults.append(float(min(2.0, max(0.5, s / m))))  # Q3 cap
    base = base.copy()
    base["mult"] = mults
    base["r_realized"] = round((base["r_realized"] + 0.08) / base["mult"] - 0.08, 4)  # A1(b)
    return base
