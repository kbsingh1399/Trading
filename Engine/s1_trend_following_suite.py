#!/usr/bin/env python3
"""
================================================================================
S1 — INSTITUTIONAL TREND-FOLLOWING ORDERFLOW SUITE (Schema v2.2, dual-grid)
================================================================================
Self-contained backtesting engine for the 20 canonical OOS quarterly windows
(2021 Q1 -> 2025 Q4) over the Binance USDT-M perpetual dual-table dataset
(58-col 15m master + 13-col footprint ladder).

DUAL-GRID ARCHITECTURE (mission Section 5, engineered from first principles)
--------------------------------------------------------------------------
  SIGNAL GRID   4h bars, causally resampled from the 15m master (16 x 15m).
                Macro regime (EMA50/200 structure + slope), sleeve triggers,
                ATR(4h) stops, ratchet decisions.
  EXECUTION GRID 15m bars. Entries fill at the FIRST 15m open after the 4h
                signal bar closes (strict bar j+1 semantics). Stops are
                checked on every 15m bar (gap fills at 15m opens). Ratchet /
                trailing updates are computed only at 4h closes and take
                effect from the next 15m bar (no intra-4h-bar favourable
                ratcheting). Time-decay is evaluated on 15m closes.
  ORDERFLOW     15m CVD, footprint stacked imbalances, taker ratio and OI
                deltas are aggregated INTO each 4h bar (fully causal) and
                drive the institutional sleeves.

SLEEVES
-------
  T1  Quiet-flow volatility breakout: Donchian expansion with volume and
      aggressive-flow confirmation (compression-qualified).
  T2  Trapped-trader absorption / value-area pullback: trend-aligned pullback
      to EMA21(4h) with CVD absorption and resumption reclaim of EMA8(4h);
      prev-day VAL/VAH sweep-reclaim variant.
  T3  Institutional delta expansion: stacked footprint imbalance rungs +
      footprint delta share + taker ratio + OI expansion continuation.

FRICTION MODEL (mission Section 1.3 — non-negotiable)
-----------------------------------------------------
  Taker fee 8 bps on BOTH entry and exit notional + 10 bps entry slippage +
  15 bps exit slippage = 41 bps round trip deducted from every trade.
  Position size makes a full stop-out lose exactly the $50 risk budget
  INCLUDING friction (1.0 R is the true worst-case loss).

PURGE INVARIANT (mission Section 2)
-----------------------------------
  Each window is evaluated independently from $5,000 flat. New entries stop
  72h before window end (t_purge). Positions are hard-closed after 10 days
  (60 x 4h) and any residual open mark is settled at the final bar. Windows
  share no state; indicators are the pipeline's causal prefix-invariant
  series (or causal resamples thereof). The 72h boundary additionally
  embargoes the trailing-data used by the causal re-optimization harness.

PARAMETER-SCALING NOTE
----------------------
  The mission's time-decay safeguard is specified as 24 x 15m bars (6h) for
  the 15m microstructure engine. On the 4h signal grid, 6h is sub-one-bar;
  the safeguard's intent (liquidate dead positions) is preserved with a
  scaled horizon of 24 x 4h bars (4 days), exposed as `time_decay_4h`.

COMPANION FILES
---------------
  Engine/runners/run_s1_failfast.py      mission §4.5 fail-fast causal
                                         walk-forward harness (fixed grid,
                                         trailing-365d + 72h embargo,
                                         zero-regression verification).
  Engine/verification/verify_s1_invariants.py
                                         10 anti-lookahead & execution-
                                         semantics invariant tests.
  Engine/runners/generate_s1_report.py   final mission report generator.

USAGE
-----
  python Engine/s1_trend_following_suite.py --out results.json
  python Engine/s1_trend_following_suite.py --mode single --window 6
  python Engine/s1_trend_following_suite.py --params overrides.json
================================================================================
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, asdict, replace
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "Engine", "binance_backtesting_data")
CACHE_DIR = os.path.join(REPO_ROOT, "Engine", "cache", "s1_trend")

DAY_MS = 86_400_000
BAR_MS = 900_000            # 15m
H4_MS = 14_400_000          # 4h
HOUR_MS = 3_600_000
F15_PER_4H = 16

SYMBOLS_ALL = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT",
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT",
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT",
]

# ---------------------------------------------------------------------------
# The 20 canonical OOS quarterly windows (mission Section 2)
# ---------------------------------------------------------------------------
OOS_WINDOWS: List[Dict] = [
    {"id": 1,  "label": "2021Q1", "start": "2021-01-01", "end": "2021-04-01",
     "name": "Bull Run Momentum Expansion"},
    {"id": 2,  "label": "2021Q2", "start": "2021-04-01", "end": "2021-07-01",
     "name": "Structural Peak & May Deleveraging Crash"},
    {"id": 3,  "label": "2021Q3", "start": "2021-07-01", "end": "2021-10-01",
     "name": "Summer Accumulation & Q3 Recovery"},
    {"id": 4,  "label": "2021Q4", "start": "2021-10-01", "end": "2022-01-01",
     "name": "All-Time High Blow-Off & Distribution"},
    {"id": 5,  "label": "2022Q1", "start": "2022-01-01", "end": "2022-04-01",
     "name": "Macro Bear Market Descent"},
    {"id": 6,  "label": "2022Q2", "start": "2022-04-01", "end": "2022-07-01",
     "name": "Terra/Luna Contagion & Liquidity Cascade"},
    {"id": 7,  "label": "2022Q3", "start": "2022-07-01", "end": "2022-10-01",
     "name": "Compressed Bear Consolidation"},
    {"id": 8,  "label": "2022Q4", "start": "2022-10-01", "end": "2023-01-01",
     "name": "FTX Insolvency & Macro Capitulation Lows"},
    {"id": 9,  "label": "2023Q1", "start": "2023-01-01", "end": "2023-04-01",
     "name": "Post-FTX Momentum Expansion"},
    {"id": 10, "label": "2023Q2", "start": "2023-04-01", "end": "2023-07-01",
     "name": "Regulatory Pressure & Range Grind"},
    {"id": 11, "label": "2023Q3", "start": "2023-07-01", "end": "2023-10-01",
     "name": "Ultra-Low Volatility Regime"},
    {"id": 12, "label": "2023Q4", "start": "2023-10-01", "end": "2024-01-01",
     "name": "Spot ETF Anticipation Trend Breakout"},
    {"id": 13, "label": "2024Q1", "start": "2024-01-01", "end": "2024-04-01",
     "name": "Institutional Inflows & New All-Time Highs"},
    {"id": 14, "label": "2024Q2", "start": "2024-04-01", "end": "2024-07-01",
     "name": "Halving Chop & High-Beta Rotation"},
    {"id": 15, "label": "2024Q3", "start": "2024-07-01", "end": "2024-10-01",
     "name": "Macro Volatility & Carry-Trade Unwind"},
    {"id": 16, "label": "2024Q4", "start": "2024-10-01", "end": "2025-01-01",
     "name": "Election Expansion & Altcoin Surge"},
    {"id": 17, "label": "2025Q1", "start": "2025-01-01", "end": "2025-04-01",
     "name": "Institutional Flow Expansion"},
    {"id": 18, "label": "2025Q2", "start": "2025-04-01", "end": "2025-07-01",
     "name": "Mid-Year Regime Rotation"},
    {"id": 19, "label": "2025Q3", "start": "2025-07-01", "end": "2025-10-01",
     "name": "Consolidation & Liquidity Harvesting"},
    {"id": 20, "label": "2025Q4", "start": "2025-10-01", "end": "2026-01-01",
     "name": "Year-End Structural Expansion"},
]

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FrictionConfig:
    """41 bps round trip: 8+8 bps taker fees, 10 bps entry, 15 bps exit."""
    taker_fee: float = 0.0008
    entry_slippage: float = 0.0010
    exit_slippage: float = 0.0015

    @property
    def round_trip_bps(self) -> float:
        return (2.0 * self.taker_fee + self.entry_slippage + self.exit_slippage) * 1e4


@dataclass(frozen=True)
class RiskConfig:
    initial_capital: float = 5000.0
    risk_usd: float = 50.0            # 1.0% fixed risk budget per trade
    max_concurrent: int = 2           # portfolio cap (mission: 2 to 3)
    dd_halt: float = 0.028            # risk-off: block new entries at this DD
    dd_resume: float = 0.014          # risk-on: re-enable below this DD
    dd_hard_cap: float = 0.05         # reporting cap (< 5.00%)
    equity_floor_frac: float = 0.952  # hard breaker: 4.8% loss from window start
    quarantine_4h: int = 18           # 72h risk-off quarantine, then re-baseline
    cooldown_bars: int = 4            # per-symbol re-entry cooldown (4h bars)
    cooldown_stop_bars: int = 8       # longer cooldown after stop-outs
    max_hold_4h: int = 60             # 10-day hard resolution
    purge_hours: int = 72             # no new entries inside final 72h


@dataclass(frozen=True)
class TrendParams:
    """Global (non-window-keyed) strategy parameters."""
    # --- Macro regime filter (4h grid) ----------------------------------------
    regime_slope_bars: int = 8        # EMA200(4h) slope lookback (32h)
    regime_use_vwap: bool = True      # 4h close vs session VWAP alignment
    er_lookback: int = 30             # efficiency-ratio lookback (5 days, 4h)
    er_min: float = 0.0               # chop veto: no entries when ER < er_min
    short_anchor_800: bool = False    # shorts additionally require c < EMA800(4h)
    # --- Sleeve T1: compression breakout (4h grid) -----------------------------
    t1_enabled: bool = True
    t1_comp_ratio: float = 1.10       # ATR14/ATR100(4h) quiet-flow ceiling
    t1_comp_required: bool = False    # pure Donchian if False
    t1_donch_bars: int = 48           # 8-day breakout channel (4h bars)
    t1_vol_ratio_min: float = 1.00    # 4h quote-volume vs SMA9 expansion
    t1_taker_min: float = 1.00        # 4h taker buy/sell ratio in direction
    t1_break_buffer_atr: float = 0.05 # buffer beyond channel
    # --- Sleeve T2: pullback absorption (4h grid) ------------------------------
    t2_enabled: bool = True
    t2_pb_atr_lo: float = -2.20       # (close-EMA21)/ATR(4h) band
    t2_pb_atr_hi: float = 0.60
    t2_rsi_lo: float = 32.0
    t2_rsi_hi: float = 64.0
    t2_cvd_min: float = 0.0           # legacy raw-coin CVD floor (0 = off)
    t2_cvd_frac_min: float = 0.03     # 4h dollar-delta / dollar-volume absorption
    t2_sweep: bool = True             # prev-day VAL/VAH sweep-reclaim variant
    t2_struct_lookback: int = 6       # structural stop swing window (4h bars)
    # --- Sleeve T3: institutional delta expansion (4h grid) --------------------
    # Core institutional conditions: stacked footprint imbalance rungs +
    # footprint delta share + directional taker pressure, in the macro regime.
    # (Rare by design — stacked-imbalance clusters are selective events.)
    t3_enabled: bool = True
    t3_stacked_min: int = 2           # stacked rungs summed over the 4h bar
    t3_delta_share_min: float = 0.08  # footprint net delta share (4h)
    t3_taker_min: float = 1.00
    t3_vol_ratio_min: float = 0.00    # 0 = no additional volume gate
    t3_close_pos_min: float = 0.55
    t3_oi_sum_min: float = 0.0        # 4h cumulative OI change rising (if live)
    # --- Entry gating -----------------------------------------------------------
    entry_gap_max_frac: float = 0.70  # skip if 15m open gaps > 0.7 x stop
    # --- Stops (4h ATR with floors/caps) ---------------------------------------
    stop_k_atr_t1: float = 2.00
    stop_k_atr_t2: float = 2.00
    stop_k_atr_t3: float = 2.00
    stop_min_frac: float = 0.0080     # 80 bps floor
    stop_max_frac: float = 0.0600     # 6% cap
    stop_struct_pad_atr: float = 0.30 # structural stop padding (T2)
    # --- Ratchet engine (mission Section 5.3, R-based) --------------------------
    ratchet_arm0_r: float = 0.90      # breakeven lock arm
    ratchet_lock0_r: float = 0.25     # covers friction, locks net profit
    ratchet_arm1_r: float = 1.90      # profit lock arm
    ratchet_lock1_r: float = 1.05
    trail_start_r: float = 2.60       # chandelier runner engages
    trail_atr_mult: float = 4.00      # chandelier width in ATR(4h)
    trail_ema21_pad_atr: float = 0.50 # EMA21(4h) structural trail pad
    time_decay_4h: int = 24           # liquidate if <+0.20R after 4 days
    time_decay_r: float = 0.20


SLEEVE_PRIORITY = {"T3": 0, "T1": 1, "T2": 2}   # delta expansion most urgent


# ---------------------------------------------------------------------------
# Section A — Data loading, 4h resampling & feature engineering
# ---------------------------------------------------------------------------

MASTER_COLS = [
    "open_time_ms", "open", "high", "low", "close", "volume_quote",
    "rsi_14", "atr_14", "atr_100",
    "ema_8", "ema_21", "ema_50", "ema_200", "ema_800",
    "future_cvd_15m", "funding_rate_pct",
    "oi_change_pct", "taker_volume_ratio",
    "taker_buy_vol_btc", "taker_sell_vol_btc",
    "prev_day_vah", "prev_day_val", "session_vwap",
    "volume_ratio",
]

LADDER_FEATURE_COLS = [
    "n_stacked_buy", "n_stacked_sell", "n_buy_imb", "n_sell_imb",
    "delta_share", "ladder_vol",
]


def _rolling_sum(a: np.ndarray, n: int) -> np.ndarray:
    c = np.cumsum(a, dtype=np.float64)
    out = np.empty_like(c)
    out[:n] = c[:n]
    out[n:] = c[n:] - c[:-n]
    return out


def _rolling_max(a: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(a).rolling(n, min_periods=1).max().to_numpy()


def _rolling_min(a: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(a).rolling(n, min_periods=1).min().to_numpy()


def _ema(x: np.ndarray, period: int) -> np.ndarray:
    out = np.empty_like(x)
    k = 2.0 / (period + 1.0)
    out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = k * x[i] + (1.0 - k) * out[i - 1]
    return out


def _wilder_atr(h: np.ndarray, l: np.ndarray, c: np.ndarray, period: int) -> np.ndarray:
    n = len(c)
    tr = np.empty(n)
    tr[0] = h[0] - l[0]
    pc = np.roll(c, 1)
    tr[1:] = np.maximum(h[1:] - l[1:], np.maximum(np.abs(h[1:] - pc[1:]), np.abs(l[1:] - pc[1:])))
    atr = np.empty(n)
    atr[0] = tr[0]
    a = 1.0 / period
    for i in range(1, n):
        atr[i] = (1.0 - a) * atr[i - 1] + a * tr[i]
    return atr


def _wilder_rsi(c: np.ndarray, period: int = 14) -> np.ndarray:
    n = len(c)
    delta = np.diff(c, prepend=c[0])
    up = np.clip(delta, 0, None)
    dn = np.clip(-delta, 0, None)
    au = np.empty(n); ad = np.empty(n)
    au[0] = up[0]; ad[0] = dn[0]
    a = 1.0 / period
    for i in range(1, n):
        au[i] = (1 - a) * au[i - 1] + a * up[i]
        ad[i] = (1 - a) * ad[i - 1] + a * dn[i]
    rs = au / np.maximum(ad, 1e-12)
    return 100.0 - 100.0 / (1.0 + rs)


def build_ladder_features(symbol: str, data_dir: str = DATA_DIR,
                          cache_dir: str = CACHE_DIR) -> Optional[pd.DataFrame]:
    """Aggregate the 13-col footprint ladder into per-15m-bar stats (cached)."""
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{symbol}_ladder_feat.parquet")
    if os.path.exists(cache_path):
        return pd.read_parquet(cache_path).set_index("open_time_ms")
    lad_path = os.path.join(data_dir, f"{symbol}_15m_footprint_ladder.parquet")
    if not os.path.exists(lad_path):
        return None
    lad = pd.read_parquet(lad_path)
    g = lad.groupby("open_time_ms", sort=True)
    feat = pd.DataFrame({
        "n_stacked_buy": g["is_stacked_buy_imb"].sum().astype(np.float64),
        "n_stacked_sell": g["is_stacked_sell_imb"].sum().astype(np.float64),
        "n_buy_imb": g["is_buy_imbalance"].sum().astype(np.float64),
        "n_sell_imb": g["is_sell_imbalance"].sum().astype(np.float64),
        "delta_share": (g["net_delta_coin"].sum()
                        / g["total_vol_coin"].sum().clip(lower=1e-12)).clip(-1.0, 1.0),
        "ladder_vol": g["total_vol_coin"].sum(),
    })
    feat = feat.reset_index()
    feat.to_parquet(cache_path, index=False)
    return feat.set_index("open_time_ms")


class SymbolData:
    """One symbol's causal feature stack: 15m execution grid + 4h signal grid."""

    def __init__(self, symbol: str, data_dir: str = DATA_DIR,
                 cache_dir: str = CACHE_DIR):
        self.symbol = symbol
        mpath = os.path.join(data_dir, f"{symbol}_15m_master_2020_2026.parquet")
        df = pd.read_parquet(mpath, columns=MASTER_COLS)
        df = df.sort_values("open_time_ms").reset_index(drop=True)
        lad = build_ladder_features(symbol, data_dir, cache_dir)
        for col in LADDER_FEATURE_COLS:
            if lad is not None and col in lad.columns:
                df[col] = df["open_time_ms"].map(lad[col]).fillna(0.0).to_numpy()
            else:
                df[col] = 0.0
        self._engineer(df)

    # ------------------------------------------------------------------ 15m --
    def _engineer(self, df: pd.DataFrame) -> None:
        t = df["open_time_ms"].to_numpy(dtype=np.int64)
        assert np.all(np.diff(t) == BAR_MS), f"{self.symbol}: non-uniform 15m grid"
        self.t = t
        self.o = df["open"].to_numpy(dtype=np.float64)
        self.h = df["high"].to_numpy(dtype=np.float64)
        self.l = df["low"].to_numpy(dtype=np.float64)
        self.c = df["close"].to_numpy(dtype=np.float64)
        self.n = len(t)
        self.session_vwap = df["session_vwap"].to_numpy(dtype=np.float64)
        self.prev_day_val = df["prev_day_val"].to_numpy(dtype=np.float64)
        self.prev_day_vah = df["prev_day_vah"].to_numpy(dtype=np.float64)

        # ---------------- 4h resample (causal; UTC-aligned 4h buckets) ----------
        # align to the next 4h UTC boundary after the first 15m bar so the
        # signal grid is consistent with session VWAP / prev-day levels
        first_4h = ((int(t[0]) + H4_MS - 1) // H4_MS) * H4_MS
        start15 = int(np.searchsorted(t, first_4h, side="left"))
        m = (self.n - start15) // F15_PER_4H
        self.start15 = start15           # 15m index of the first aligned 4h bar

        def r16(col, how):
            a = col[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
            return a.max(axis=1) if how == "max" else (
                a.min(axis=1) if how == "min" else (
                    a[:, 0] if how == "first" else a[:, -1]))
        t4 = t[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)[:, 0]
        o4, h4, l4, c4 = (r16(self.o, "first"), r16(self.h, "max"),
                          r16(self.l, "min"), r16(self.c, "last"))
        self.t4, self.o4, self.h4, self.l4, self.c4 = t4, o4, h4, l4, c4
        self.n4 = m

        # 4h indicators (computed on the resampled series — causal)
        self.atr4 = _wilder_atr(h4, l4, c4, 14)
        self.atr4_100 = _wilder_atr(h4, l4, c4, 100)
        self.rsi4 = _wilder_rsi(c4, 14)
        self.ema4_8 = _ema(c4, 8)
        self.ema4_21 = _ema(c4, 21)
        self.ema4_50 = _ema(c4, 50)
        self.ema4_200 = _ema(c4, 200)
        self.ema4_800 = _ema(c4, 800)   # ~33-day dominant trend anchor
        self.atr_ratio4 = self.atr4 / np.maximum(self.atr4_100, 1e-12)

        # 4h orderflow aggregation (from 15m empirical flow)
        vq = df["volume_quote"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        cvd = df["future_cvd_15m"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        oic = df["oi_change_pct"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        stb = df["n_stacked_buy"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        sts = df["n_stacked_sell"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        dsh = df["delta_share"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        lv = df["ladder_vol"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        tb = df["taker_buy_vol_btc"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        ts = df["taker_sell_vol_btc"].to_numpy(dtype=np.float64)[start15:start15 + m * F15_PER_4H].reshape(-1, F15_PER_4H)
        vq4 = vq.sum(axis=1)
        self.vq4 = vq4
        self.vol_ratio4 = vq4 / np.maximum(_rolling_mean(vq4, 9), 1e-12)
        self.cvd4 = cvd.sum(axis=1)
        self.oi4 = oic.sum(axis=1)
        self.stacked4_buy = stb.sum(axis=1)
        self.stacked4_sell = sts.sum(axis=1)
        w = lv.sum(axis=1)
        self.delta4_share = np.where(w > 1e-12, (dsh * lv).sum(axis=1) / np.maximum(w, 1e-12), 0.0)
        self.taker4 = tb.sum(axis=1) / np.maximum(ts.sum(axis=1), 1e-12)
        self.close_pos4 = (c4 - l4) / np.maximum(h4 - l4, 1e-12)
        # OI feed liveness: Binance OI metrics for non-BTC assets only exist
        # from 2022 onward. A causal trailing-activity detector decides
        # whether the OI gate is enforceable on each 4h bar (no lookahead:
        # uses only the trailing 7 days of oi_change_pct).
        oi_abs = np.abs(oic).sum(axis=1)
        self.oi_alive4 = _rolling_sum(oi_abs, 42) > 1e-9

        # efficiency ratio (Kaufman) on 4h closes: trendiness in [0, 1]
        lb = 30
        er = np.zeros(m)
        dc = np.abs(np.diff(c4, prepend=c4[0]))
        denom = _rolling_sum(dc, lb)
        er[lb:] = np.abs(c4[lb:] - c4[:-lb]) / np.maximum(denom[lb:], 1e-12)
        self.er4 = er
        # dollar-normalised CVD fraction (aggressor delta / quote volume)
        self.cvd_frac4 = (cvd.sum(axis=1) * c4) / np.maximum(vq4, 1e-12)

        # macro regime (4h)
        slope = np.zeros(m)
        sl = 8
        slope[sl:] = self.ema4_200[sl:] - self.ema4_200[:-sl]
        vwap_at_4h = self.session_vwap[start15 + (np.arange(m) * F15_PER_4H) + F15_PER_4H - 1]
        self.regime_long = (self.ema4_50 > self.ema4_200) & (c4 > self.ema4_200) & (slope > 0)
        self.regime_short = (self.ema4_50 < self.ema4_200) & (c4 < self.ema4_200) & (slope < 0)
        self.regime_long &= c4 > vwap_at_4h
        self.regime_short &= c4 < vwap_at_4h

        # Donchian channels on 4h, EXCLUDING current bar
        self.donch4_hi = {n: np.roll(_rolling_max(h4, n), 1) for n in (24, 48, 96)}
        self.donch4_lo = {n: np.roll(_rolling_min(l4, n), 1) for n in (24, 48, 96)}
        for n in (24, 48, 96):
            self.donch4_hi[n][:n] = np.nan
            self.donch4_lo[n][:n] = np.nan
        # structural swings (4h)
        self.swing4_lo = _rolling_min(l4, 6)
        self.swing4_hi = _rolling_max(h4, 6)

    def idx_of(self, ts_ms: int) -> int:
        i = int(np.searchsorted(self.t, ts_ms, side="left"))
        if i >= self.n or self.t[i] != ts_ms:
            return -1
        return i

    def idx4_of(self, ts_ms: int) -> int:
        i = int(np.searchsorted(self.t4, ts_ms, side="left"))
        if i >= self.n4 or self.t4[i] != ts_ms:
            return -1
        return i


def _rolling_mean(a: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(a).rolling(n, min_periods=1).mean().to_numpy()


# ---------------------------------------------------------------------------
# Section B — Candidate signal generation (4h grid, causal)
# ---------------------------------------------------------------------------

@dataclass
class Candidate:
    symbol: str
    j4: int               # signal bar index on the 4h grid
    side: int             # +1 long, -1 short
    sleeve: str           # T1 / T2 / T3
    stop_dist: float      # price units, from 4h bar-j4 data only


def generate_candidates(sd: SymbolData, p: TrendParams,
                        j_lo: int, j_hi: int) -> List[Candidate]:
    """Sleeve triggers for 4h signal bars j4 in [j_lo, j_hi)."""
    out: List[Candidate] = []
    c = sd.c4
    atr = sd.atr4
    n = sd.n4
    j_hi = min(j_hi, n - 1)  # entry needs the next 4h bar to exist

    reg_l, reg_s = sd.regime_long, sd.regime_short
    if p.short_anchor_800:
        reg_s = reg_s & (c < sd.ema4_800)
    valid = (np.arange(n) >= j_lo) & (np.arange(n) < j_hi) & np.isfinite(atr) & (atr > 0)
    if p.er_min > 0:
        valid = valid & (sd.er4 >= p.er_min)   # chop veto: trendiness gate

    def stop_for(k_atr: float, j: int) -> float:
        d = max(k_atr * atr[j], p.stop_min_frac * c[j])
        return float(min(d, p.stop_max_frac * c[j]))

    # ---------------- T1: compression breakout ---------------------------------
    if p.t1_enabled:
        comp = sd.atr_ratio4 < p.t1_comp_ratio
        d = p.t1_donch_bars
        buf = p.t1_break_buffer_atr * atr
        brk_up = c > (sd.donch4_hi[d] + buf)
        brk_dn = c < (sd.donch4_lo[d] - buf)
        vol_ok = sd.vol_ratio4 > p.t1_vol_ratio_min
        taker_l = sd.taker4 > p.t1_taker_min
        taker_s = sd.taker4 < (1.0 / max(p.t1_taker_min, 1e-9))
        gate = comp if p.t1_comp_required else np.ones(n, bool)
        for mask, side in ((gate & brk_up & vol_ok & taker_l & reg_l, 1),
                           (gate & brk_dn & vol_ok & taker_s & reg_s, -1)):
            idx = np.nonzero(mask & valid)[0]
            for j in idx:
                out.append(Candidate(sd.symbol, int(j), side, "T1", stop_for(p.stop_k_atr_t1, j)))

    # ---------------- T2: pullback absorption / sweep-reclaim ------------------
    if p.t2_enabled:
        depth = (c - sd.ema4_21) / np.maximum(atr, 1e-12)
        in_band = (depth >= p.t2_pb_atr_lo) & (depth <= p.t2_pb_atr_hi)
        rsi_ok = (sd.rsi4 >= p.t2_rsi_lo) & (sd.rsi4 <= p.t2_rsi_hi)
        green = c > sd.o4
        cvd_pos = (sd.cvd4 >= p.t2_cvd_min) & (sd.cvd_frac4 >= p.t2_cvd_frac_min)
        cvd_neg = (sd.cvd4 <= -p.t2_cvd_min) & (sd.cvd_frac4 <= -p.t2_cvd_frac_min)
        resume_l = (c > sd.ema4_8) & green
        resume_s = (c < sd.ema4_8) & ~green
        # prev-day VAL/VAH sweep-reclaim, evaluated at the 4h close
        pdv = sd.prev_day_val[sd.start15 + (np.arange(n) * F15_PER_4H) + F15_PER_4H - 1]
        pdh = sd.prev_day_vah[sd.start15 + (np.arange(n) * F15_PER_4H) + F15_PER_4H - 1]
        sweep_l = (sd.l4 <= pdv) & (c > pdv) & green if p.t2_sweep else np.zeros(n, bool)
        sweep_s = (sd.h4 >= pdh) & (c < pdh) & ~green if p.t2_sweep else np.zeros(n, bool)
        base_l = in_band & rsi_ok & cvd_pos & resume_l
        base_s = in_band & rsi_ok & cvd_neg & resume_s
        long_mask = (base_l & reg_l) | (sweep_l & reg_l & cvd_pos & rsi_ok)
        short_mask = (base_s & reg_s) | (sweep_s & reg_s & cvd_neg & rsi_ok)
        for mask, side in ((long_mask, 1), (short_mask, -1)):
            idx = np.nonzero(mask & valid)[0]
            for j in idx:
                d_atr = stop_for(p.stop_k_atr_t2, j)
                if side == 1:
                    struct = (c[j] - sd.swing4_lo[j]) + p.stop_struct_pad_atr * atr[j]
                else:
                    struct = (sd.swing4_hi[j] - c[j]) + p.stop_struct_pad_atr * atr[j]
                dist = float(min(max(d_atr, struct), p.stop_max_frac * c[j]))
                out.append(Candidate(sd.symbol, int(j), side, "T2", dist))

    # ---------------- T3: institutional delta expansion ------------------------
    if p.t3_enabled:
        stacked_l = sd.stacked4_buy >= p.t3_stacked_min
        stacked_s = sd.stacked4_sell >= p.t3_stacked_min
        delta_l = sd.delta4_share >= p.t3_delta_share_min
        delta_s = sd.delta4_share <= -p.t3_delta_share_min
        taker_l = sd.taker4 >= p.t3_taker_min
        taker_s = sd.taker4 <= (1.0 / max(p.t3_taker_min, 1e-9))
        vol_ok = sd.vol_ratio4 >= p.t3_vol_ratio_min
        cp_l = sd.close_pos4 >= p.t3_close_pos_min
        cp_s = sd.close_pos4 <= (1.0 - p.t3_close_pos_min)
        oi_up = sd.oi4 > p.t3_oi_sum_min
        long_mask = (stacked_l & delta_l & taker_l & vol_ok & cp_l & oi_up & reg_l)
        short_mask = (stacked_s & delta_s & taker_s & vol_ok & cp_s & oi_up & reg_s)
        for mask, side in ((long_mask, 1), (short_mask, -1)):
            idx = np.nonzero(mask & valid)[0]
            for j in idx:
                out.append(Candidate(sd.symbol, int(j), side, "T3", stop_for(p.stop_k_atr_t3, j)))

    return out


# ---------------------------------------------------------------------------
# Section C — Trade simulation (15m execution grid, 4h-close ratchets)
# ---------------------------------------------------------------------------

@dataclass
class Trade:
    symbol: str
    sleeve: str
    side: int
    entry_bar: int          # 15m bar index of the fill
    exit_bar: int           # 15m bar index of the exit
    entry_ts: int
    exit_ts: int
    entry_price: float
    exit_price: float
    stop_dist: float
    qty: float
    risk_usd: float
    pnl: float
    r: float
    mfe_r: float
    reason: str


def simulate_trade(sd: SymbolData, cand: Candidate, p: TrendParams,
                   fric: FrictionConfig, risk: RiskConfig,
                   bar_end: int) -> Optional[Trade]:
    """Simulate one candidate: entry at the first 15m open after 4h bar j4.

    Ordering on every 15m bar:
      1) stop-gap fill at the 15m open;
      2) intrabar stop touch (fill at stop level);
      3) time-decay at the 15m close (4h-age based);
      4) MFE update;
      5) at 4h boundaries only: ratchet/trail recompute -> effective next bar.
    """
    side, j4 = cand.side, cand.j4
    t0 = sd.start15 + (j4 + 1) * F15_PER_4H
    if t0 >= sd.n or t0 > bar_end:
        return None
    entry = sd.o[t0] * (1.0 + side * fric.entry_slippage)
    stop_dist = cand.stop_dist
    stop_price = entry - side * stop_dist
    if not (stop_dist > 0) or not np.isfinite(stop_price) or stop_price <= 0:
        return None
    # entry-gap guard (observed at the fill open itself)
    gap = side * (sd.o[t0] - sd.c4[j4])
    if gap > p.entry_gap_max_frac * stop_dist:
        return None

    stop_fill_px = stop_price * (1.0 - side * fric.exit_slippage)
    loss_at_stop = side * (entry - stop_fill_px) + fric.taker_fee * (entry + stop_fill_px)
    if loss_at_stop <= 0:
        return None
    qty = risk.risk_usd / loss_at_stop
    r_pu = loss_at_stop                      # $ risk per unit qty

    stop = stop_price
    mfe_r = 0.0
    hh = sd.h[t0] if side == 1 else sd.l[t0]  # running favourable extreme
    reason, exit_bar, exit_price = None, None, None
    last = min(bar_end + 1, sd.n)

    def _pnl_at(px: float) -> float:
        return qty * (side * (px - entry) - fric.taker_fee * (entry + px))

    for t in range(t0, last):
        bo, bh, bl, bc = sd.o[t], sd.h[t], sd.l[t], sd.c[t]
        # 1) gap through stop at the open
        if side * (stop - bo) >= 0:
            reason, exit_bar, exit_price = "STOP_OPEN", t, bo * (1.0 - side * fric.exit_slippage)
            break
        # 2) intrabar stop touch
        adverse = bl if side == 1 else bh
        if side * (stop - adverse) >= 0:
            reason, exit_bar, exit_price = "STOP", t, stop * (1.0 - side * fric.exit_slippage)
            break
        # 3) time-decay safeguard (4h age) at the close
        age_4h = (t - t0) // F15_PER_4H
        cur_r = side * (bc - entry) / r_pu
        if age_4h >= p.time_decay_4h and cur_r < p.time_decay_r:
            reason, exit_bar, exit_price = "TIME_DECAY", t, bc * (1.0 - side * fric.exit_slippage)
            break
        if age_4h >= risk.max_hold_4h:
            reason, exit_bar, exit_price = "MAX_HOLD", t, bc * (1.0 - side * fric.exit_slippage)
            break
        # 4) favourable excursion update
        if side == 1:
            hh = max(hh, bh)
            mfe_r = max(mfe_r, (bh - entry) / r_pu)
        else:
            hh = min(hh, bl)
            mfe_r = max(mfe_r, (entry - bl) / r_pu)
        # 5) ratchet recompute at 4h close boundaries, effective next 15m bar
        if (t + 1 - sd.start15) % F15_PER_4H == 0 and t + 1 < last:
            j4c = (t + 1 - sd.start15) // F15_PER_4H - 1
            atr4 = sd.atr4[j4c]
            prop_r = -np.inf
            if mfe_r >= p.ratchet_arm1_r:
                prop_r = max(prop_r, p.ratchet_lock1_r)
            elif mfe_r >= p.ratchet_arm0_r:
                prop_r = max(prop_r, p.ratchet_lock0_r)
            if mfe_r >= p.trail_start_r:
                chand = hh - side * p.trail_atr_mult * atr4
                ema_tr = sd.ema4_21[j4c] - side * p.trail_ema21_pad_atr * atr4
                trail_px = max(chand, ema_tr) if side == 1 else min(chand, ema_tr)
                prop_r = max(prop_r, side * (trail_px - entry) / r_pu)
            if prop_r > -np.inf:
                new_stop = entry + side * prop_r * r_pu
                stop = max(stop, new_stop) if side == 1 else min(stop, new_stop)

    if exit_bar is None:
        t = last - 1
        reason, exit_bar, exit_price = "SETTLE", t, sd.c[t] * (1.0 - side * fric.exit_slippage)

    pnl = _pnl_at(exit_price)
    return Trade(
        symbol=cand.symbol, sleeve=cand.sleeve, side=side,
        entry_bar=t0, exit_bar=exit_bar,
        entry_ts=int(sd.t[t0]), exit_ts=int(sd.t[exit_bar]),
        entry_price=entry, exit_price=exit_price,
        stop_dist=stop_dist, qty=qty, risk_usd=risk.risk_usd,
        pnl=float(pnl), r=float(pnl / risk.risk_usd), mfe_r=float(mfe_r),
        reason=reason,
    )


# ---------------------------------------------------------------------------
# Section D — Portfolio assembly (15m timeline, concurrency, DD protocol)
# ---------------------------------------------------------------------------

def assemble_portfolio(trades_by_key: Dict[Tuple[str, int, int], Trade],
                       cands: List[Candidate], sds: Dict[str, SymbolData],
                       risk: RiskConfig, window: Dict) -> Dict:
    t_start = int(pd.Timestamp(window["start"]).value // 1e6)
    t_end = int(pd.Timestamp(window["end"]).value // 1e6)
    t_purge = t_end - risk.purge_hours * HOUR_MS

    n_bars = (t_end - t_start) // BAR_MS
    all_ts = t_start + np.arange(n_bars, dtype=np.int64) * BAR_MS

    # per-symbol closes aligned to the 15m timeline
    closes: Dict[str, np.ndarray] = {}
    for s, sd in sds.items():
        arr = np.full(n_bars, np.nan)
        lo = int(np.searchsorted(sd.t, t_start, side="left"))
        hi = int(np.searchsorted(sd.t, t_end, side="left"))
        for k in range(lo, hi):
            i = int((sd.t[k] - t_start) // BAR_MS)
            if 0 <= i < n_bars:
                arr[i] = sd.c[k]
        closes[s] = arr

    # candidates grouped by entry timeline index (first 15m bar of 4h bar j4+1)
    by_entry: Dict[int, List[Candidate]] = {}
    for cand in cands:
        sd = sds[cand.symbol]
        i15 = sd.start15 + (cand.j4 + 1) * F15_PER_4H
        if i15 >= sd.n:
            continue
        ts_e = int(sd.t[i15])
        if ts_e < t_start or ts_e >= t_end:
            continue
        by_entry.setdefault(int((ts_e - t_start) // BAR_MS), []).append(cand)
    for k in by_entry:
        by_entry[k].sort(key=lambda cd_: (SLEEVE_PRIORITY.get(cd_.sleeve, 9), cd_.symbol))

    cash = risk.initial_capital
    open_pos: Dict[str, Trade] = {}
    cooldown_until: Dict[str, int] = {}
    admitted: List[Trade] = []
    eq = np.full(n_bars, risk.initial_capital, dtype=np.float64)
    peak = risk.initial_capital        # true reporting peak (never re-anchored)
    op_peak = risk.initial_capital     # operational peak for the risk protocol
    halted = False
    halt_idx = None
    halt_start = None
    max_dd_seen = 0.0
    prev_eq = risk.initial_capital
    floor = risk.initial_capital * risk.equity_floor_frac
    dead = False

    for i in range(n_bars):
        ts = int(all_ts[i])
        # 1) exits of previously-open positions settling this bar
        for s in [s for s, tr in open_pos.items() if tr.exit_ts == ts]:
            tr = open_pos.pop(s)
            cash += tr.pnl
            cd_bars = risk.cooldown_stop_bars if tr.reason in ("STOP", "STOP_OPEN") else risk.cooldown_bars
            cooldown_until[s] = ts + cd_bars * H4_MS
        # 2) entry admission at this bar's open
        newly: List[Trade] = []
        # Institutional risk-off / risk-on protocol on mark-to-market DD:
        #  - halt new entries when operational DD >= dd_halt;
        #  - resume when DD recovers to dd_resume, or after a 72h quarantine
        #    with a flat book (operational peak re-baselined to equity).
        # The REPORTED drawdown always uses the true (never re-anchored) peak.
        dd_op = (op_peak - prev_eq) / op_peak if op_peak > 0 else 0.0
        if prev_eq <= floor:
            dead = True     # hard 4.8% circuit breaker: window over
        if dead:
            halted = True
            halt_idx = i if halt_idx is None else halt_idx
        if not halted:
            if dd_op >= risk.dd_halt:
                halted = True
                halt_idx = i if halt_idx is None else halt_idx
                halt_start = i
        else:
            flat = len(open_pos) == 0
            quarantine_over = (i - halt_start) >= risk.quarantine_4h * F15_PER_4H
            if dd_op <= risk.dd_resume or (flat and quarantine_over):
                halted = False
                op_peak = max(prev_eq, 1e-9)
        if not halted and i in by_entry and ts <= t_purge:
            for cand in by_entry[i]:
                if len(open_pos) >= risk.max_concurrent:
                    break
                s = cand.symbol
                if s in open_pos:
                    continue
                cd_ = cooldown_until.get(s)
                if cd_ is not None and ts <= cd_:
                    continue
                tr = trades_by_key.get((s, cand.j4, cand.side))
                if tr is None or tr.entry_ts != ts:
                    continue
                open_pos[s] = tr
                admitted.append(tr)
                newly.append(tr)
        # 3) same-bar stop-outs of just-admitted trades
        for tr in newly:
            if tr.exit_ts == ts:
                open_pos.pop(tr.symbol, None)
                cash += tr.pnl
                cooldown_until[tr.symbol] = ts + risk.cooldown_stop_bars * H4_MS
        # 4) mark-to-market equity at this bar's close
        eq_i = cash
        for s, tr in open_pos.items():
            mkt = closes[s][i]
            if np.isfinite(mkt):
                eq_i += tr.qty * tr.side * (mkt - tr.entry_price)
        eq[i] = eq_i
        prev_eq = eq_i
        peak = max(peak, eq_i)
        op_peak = max(op_peak, eq_i)
        max_dd_seen = max(max_dd_seen, (peak - eq_i) / peak if peak > 0 else 0.0)

    return {
        "trades": sorted(admitted, key=lambda tr: (tr.entry_ts, tr.symbol)),
        "equity": eq,
        "timeline": all_ts,
        "max_dd": max_dd_seen,
        "halted": halted,
        "final_equity": float(eq[-1]),
    }


# ---------------------------------------------------------------------------
# Section E — Window evaluation
# ---------------------------------------------------------------------------

def evaluate_window(sds: Dict[str, SymbolData], window: Dict, p: TrendParams,
                    fric: FrictionConfig, risk: RiskConfig) -> Dict:
    t_start = int(pd.Timestamp(window["start"]).value // 1e6)
    t_end = int(pd.Timestamp(window["end"]).value // 1e6)
    t_purge = t_end - risk.purge_hours * HOUR_MS

    cands: List[Candidate] = []
    trades_by_key: Dict[Tuple[str, int, int], Trade] = {}
    n_cands_raw = 0
    for sym, sd in sds.items():
        j_lo = max(0, int(np.searchsorted(sd.t4, t_start, side="left")))
        # signals up to 72h before window end (entry then fills in-window)
        j_hi = int(np.searchsorted(sd.t4, t_purge, side="right"))
        if j_hi <= j_lo:
            continue
        # simulation may run to the last 15m bar inside the window
        bar_end = int(np.searchsorted(sd.t, t_end, side="right")) - 1
        sym_cands = generate_candidates(sd, p, j_lo, j_hi)
        n_cands_raw += len(sym_cands)
        best: Dict[Tuple[int, int], Candidate] = {}
        for cd_ in sym_cands:
            key = (cd_.j4, cd_.side)
            if key not in best or (SLEEVE_PRIORITY.get(cd_.sleeve, 9)
                                   < SLEEVE_PRIORITY.get(best[key].sleeve, 9)):
                best[key] = cd_
        for cd_ in best.values():
            tr = simulate_trade(sd, cd_, p, fric, risk, bar_end)
            if tr is not None and tr.exit_ts < t_end:
                cands.append(cd_)
                trades_by_key[(cd_.symbol, cd_.j4, cd_.side)] = tr

    port = assemble_portfolio(trades_by_key, cands, sds, risk, window)
    trades = port["trades"]
    eq = port["equity"]
    max_dd = float(port["max_dd"])

    pnls = np.array([tr.pnl for tr in trades]) if trades else np.zeros(0)
    rs = np.array([tr.r for tr in trades]) if trades else np.zeros(0)
    n = len(trades)
    wins = pnls[pnls > 0]
    losses = pnls[pnls <= 0]
    gross_win = float(wins.sum())
    gross_loss = float(-losses.sum())
    pf = gross_win / gross_loss if gross_loss > 0 else (99.99 if gross_win > 0 else 0.0)
    final_eq = float(eq[-1])
    roi = (final_eq - risk.initial_capital) / risk.initial_capital * 100.0
    wr = float((pnls > 0).mean() * 100.0) if n else 0.0
    max_r_realized = float(rs.max()) if n else 0.0
    max_mfe = max([tr.mfe_r for tr in trades], default=0.0)
    longs = [tr for tr in trades if tr.side == 1]
    shorts = [tr for tr in trades if tr.side == -1]

    verdict_pass = (
        roi >= 10.0 and max_dd < 5.0 and wr >= 40.0 and n >= 15
        and pf >= 1.40 and (max_r_realized >= 4.0 or max_mfe >= 4.0)
    )
    fails = []
    if roi < 10.0: fails.append("roi")
    if max_dd >= 5.0: fails.append("dd")
    if wr < 40.0: fails.append("wr")
    if n < 15: fails.append("trades")
    if pf < 1.40: fails.append("pf")
    if max_r_realized < 4.0 and max_mfe < 4.0: fails.append("maxR")

    return {
        "window_id": window["id"], "label": window["label"], "name": window["name"],
        "start": window["start"], "end": window["end"],
        "n_candidates": n_cands_raw,
        "n_trades": n,
        "net_pnl_usd": float(pnls.sum()) if n else 0.0,
        "final_equity": final_eq,
        "roi_pct": roi,
        "max_dd_pct": max_dd * 100.0,
        "win_rate_pct": wr,
        "profit_factor": min(pf, 99.99),
        "avg_r": float(rs.mean()) if n else 0.0,
        "max_r_realized": max_r_realized,
        "max_mfe_r": max_mfe,
        "n_long": len(longs), "n_short": len(shorts),
        "long_pnl": float(sum(tr.pnl for tr in longs)),
        "short_pnl": float(sum(tr.pnl for tr in shorts)),
        "halted": port["halted"],
        "verdict": "PASS" if verdict_pass else "FAIL",
        "fail_reasons": fails,
        "sleeve_counts": {s: len([tr for tr in trades if tr.sleeve == s])
                          for s in ("T1", "T2", "T3")},
        "exit_reasons": _reason_counts(trades),
        "trades": [_trade_row(tr) for tr in trades],
    }


def _reason_counts(trades: List[Trade]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for tr in trades:
        out[tr.reason] = out.get(tr.reason, 0) + 1
    return out


def _trade_row(tr: Trade) -> Dict:
    return {
        "symbol": tr.symbol, "sleeve": tr.sleeve,
        "side": "LONG" if tr.side == 1 else "SHORT",
        "entry_ts": int(tr.entry_ts), "exit_ts": int(tr.exit_ts),
        "entry_price": round(tr.entry_price, 8), "exit_price": round(tr.exit_price, 8),
        "qty": tr.qty, "pnl": round(tr.pnl, 2), "r": round(tr.r, 4),
        "mfe_r": round(tr.mfe_r, 4), "reason": tr.reason,
    }


# ---------------------------------------------------------------------------
# Section F — System-level statistics
# ---------------------------------------------------------------------------

def system_statistics(window_results: List[Dict], risk: RiskConfig) -> Dict:
    factors = [1.0 + w["roi_pct"] / 100.0 for w in window_results]
    compounded = risk.initial_capital
    for f in factors:
        compounded *= f
    total_return = compounded / risk.initial_capital - 1.0
    years = len(factors) / 4.0
    cagr = (compounded / risk.initial_capital) ** (1.0 / years) - 1.0 if years > 0 else 0.0
    rois = np.array([w["roi_pct"] for w in window_results], dtype=np.float64)
    q_mean = float(rois.mean())
    q_std = float(rois.std(ddof=1)) if len(rois) > 1 else 0.0
    sharpe_q = q_mean / q_std * 2.0 if q_std > 0 else 0.0
    max_dd = max(w["max_dd_pct"] for w in window_results)
    calmar = cagr / max_dd if max_dd > 0 else 0.0
    net = sum(w["net_pnl_usd"] for w in window_results)
    return {
        "initial_capital": risk.initial_capital,
        "final_compounded_equity": compounded,
        "cumulative_net_profit_usd_noncompounded": float(net),
        "total_return_pct": total_return * 100.0,
        "cagr_pct": cagr * 100.0,
        "worst_window_dd_pct": max_dd,
        "sharpe_annualized_quarterly": sharpe_q,
        "calmar_ratio": calmar,
        "total_trades": int(sum(w["n_trades"] for w in window_results)),
        "total_long": int(sum(w["n_long"] for w in window_results)),
        "total_short": int(sum(w["n_short"] for w in window_results)),
        "long_pnl_total": float(sum(w["long_pnl"] for w in window_results)),
        "short_pnl_total": float(sum(w["short_pnl"] for w in window_results)),
        "avg_r_all_trades": float(np.mean([w["avg_r"] for w in window_results])),
        "windows_passed": int(sum(1 for w in window_results if w["verdict"] == "PASS")),
        "windows_total": len(window_results),
    }


# ---------------------------------------------------------------------------
# Section G — Harness
# ---------------------------------------------------------------------------

def load_symbols(symbols: List[str], data_dir: str = DATA_DIR) -> Dict[str, SymbolData]:
    sds: Dict[str, SymbolData] = {}
    for s in symbols:
        mpath = os.path.join(data_dir, f"{s}_15m_master_2020_2026.parquet")
        if not os.path.exists(mpath):
            continue
        sd = SymbolData(s, data_dir)
        if sd.n < 1000:
            continue
        sds[s] = sd
    return sds


def run_all_windows(sds: Dict[str, SymbolData], p: TrendParams,
                    fric: FrictionConfig, risk: RiskConfig,
                    windows: Optional[List[Dict]] = None,
                    verbose: bool = True) -> List[Dict]:
    windows = windows or OOS_WINDOWS
    results = []
    for w in windows:
        t0 = time.time()
        res = evaluate_window(sds, w, p, fric, risk)
        res["eval_seconds"] = round(time.time() - t0, 2)
        results.append(res)
        if verbose:
            print(f"W{w['id']:02d} {w['label']} | "
                  f"ROI {res['roi_pct']:>7.2f}% | DD {res['max_dd_pct']:>5.2f}% | "
                  f"WR {res['win_rate_pct']:>5.1f}% | trades {res['n_trades']:>3d} | "
                  f"PF {res['profit_factor']:>5.2f} | maxR {res['max_r_realized']:>5.2f} "
                  f"(MFE {res['max_mfe_r']:.2f}) | {res['verdict']}"
                  f"{' ' + ','.join(res['fail_reasons']) if res['fail_reasons'] else ''}",
                  flush=True)
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="S1 Trend-Following Orderflow Suite")
    ap.add_argument("--mode", choices=["fixed", "single"], default="fixed")
    ap.add_argument("--window", type=int, default=None)
    ap.add_argument("--params", type=str, default=None)
    ap.add_argument("--symbols", type=str, default=",".join(SYMBOLS_ALL))
    ap.add_argument("--out", type=str, default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    overrides = {}
    if args.params:
        with open(args.params) as f:
            overrides = json.load(f)
    p = TrendParams(**{k: v for k, v in overrides.items()
                       if k in TrendParams.__dataclass_fields__})
    fric = FrictionConfig()
    risk = RiskConfig()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    print(f"[S1] screening symbols: {symbols}", flush=True)
    t0 = time.time()
    sds = load_symbols(symbols)
    print(f"[S1] active symbols with full history: {sorted(sds)} "
          f"(load {time.time()-t0:.1f}s)", flush=True)
    print(f"[S1] friction round-trip: {fric.round_trip_bps:.1f} bps | "
          f"risk ${risk.risk_usd}/trade | max concurrent {risk.max_concurrent} | "
          f"signal grid 4h / execution grid 15m", flush=True)

    if args.mode == "single" and args.window:
        windows = [w for w in OOS_WINDOWS if w["id"] == args.window]
    else:
        windows = OOS_WINDOWS

    results = run_all_windows(sds, p, fric, risk, windows, verbose=not args.quiet)
    stats = system_statistics(results, risk)
    payload = {
        "strategy": "S1 Institutional Trend-Following Orderflow Suite (dual-grid)",
        "params": asdict(p),
        "friction": asdict(fric),
        "risk": asdict(risk),
        "symbols_active": sorted(sds),
        "summary": stats,
        "windows": [{k: v for k, v in r.items() if k != "trades"} for r in results],
        "trades_by_window": {str(r["window_id"]): r["trades"] for r in results},
    }
    if args.out:
        out_dir = os.path.dirname(os.path.abspath(args.out))
        os.makedirs(out_dir, exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(payload, f, indent=1)
        print(f"[S1] results written to {args.out}", flush=True)

    print("\n=== 20-WINDOW SCORECARD ===")
    print(f"{'W':>4} {'Period':>8} {'Net ROI %':>10} {'MaxDD %':>8} {'WR %':>6} {'Trades':>7} {'PF':>6} {'Verdict':>8}")
    for r in results:
        print(f"W{r['window_id']:02d} {r['label']:>8} {r['roi_pct']:>10.2f} "
              f"{r['max_dd_pct']:>8.2f} {r['win_rate_pct']:>6.1f} {r['n_trades']:>7d} "
              f"{r['profit_factor']:>6.2f} {r['verdict']:>8}")
    print(f"\npassed {stats['windows_passed']}/{stats['windows_total']} windows | "
          f"CAGR {stats['cagr_pct']:.1f}% | worst window DD {stats['worst_window_dd_pct']:.2f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
