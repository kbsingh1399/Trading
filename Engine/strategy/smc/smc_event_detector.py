# Engine/strategy/smc_event_detector.py
from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class SMCConfig:
    min_r_dist_pct: float = 0.015        # structural stop >= 1.5% -> friction < 0.2R
    max_r_dist_pct: float = 0.040        # sanity ceiling
    sweep_max_penetr_atr: float = 0.5    # sweep wick beyond level <= 0.5 ATR_d
    fvg_min_size_atr: float = 0.30       # gap must be >= 0.3 daily ATR
    fvg_max_age_days: int = 10           # unmitigated gaps expire
    ob_max_pullback_bars: int = 96       # 24h of 15m bars to reach the OB
    stop_buffer_atr_frac: float = 0.10   # stop = level +/- 0.10 * ATR_d
    reclaim_min_bars: int = 1            # bars holding beyond level before signal


class SMCEventDetector:
    """
    Detects, on 15m data with daily structural levels:
      A. UsmanNoah sweep:   price pierces PDH/PDL then closes back inside the
                            prior day range (failed breakout = liquidity grab).
      B. FVG retest:        price returns into an unmitigated daily FVG zone.
      C. OB/Breaker tap:    price pulls back to the origin extreme of the last
                            displacement leg that broke structure.
    Signal bar t -> filled at Open[t+1] by the kernel (strictly causal).
    """

    COLS = ("side", "raw_r", "structural_level", "invalidation_price", "event_type")

    def __init__(self, cfg: SMCConfig = SMCConfig()):
        self.cfg = cfg

    # ------------------------------------------------------------------
    # Daily structure map - computed ONLY from completed daily candles
    # ------------------------------------------------------------------
    def daily_structure(self, df15: pd.DataFrame) -> pd.DataFrame:
        d = pd.DataFrame({
            "high_d": df15["high"].resample("1D").max(),
            "low_d": df15["low"].resample("1D").min(),
            "open_d": df15["open"].resample("1D").first(),
            "close_d": df15["close"].resample("1D").last()
        }).dropna()
        d["atr_d"] = (d["high_d"] - d["low_d"]).rolling(14, min_periods=5).mean().ffill()

        # PDH/PDL = previous COMPLETED day's extremes (shift(1) -> causal)
        d["pdh"] = d["high_d"].shift(1)
        d["pdl"] = d["low_d"].shift(1)

        # Daily FVG: gap between day[i-2].high and day[i].low (bearish) or
        # day[i-2].low and day[i].high (bullish). Attached to day i.
        d["fvg_bull_lo"] = d["high_d"].shift(2)
        d["fvg_bull_hi"] = np.where(d["low_d"] > d["fvg_bull_lo"], d["low_d"], np.nan)
        d["fvg_bear_lo"] = np.where(d["high_d"] < d["low_d"].shift(2), d["high_d"], np.nan)
        d["fvg_bear_hi"] = d["low_d"].shift(2)

        # Displacement OB: day with range > 1.5*atr_d and body/range > 0.5
        body = (d["close_d"] - d["open_d"]).abs()
        rng = (d["high_d"] - d["low_d"]).clip(lower=1e-12)
        big = (rng > 1.5 * d["atr_d"]) & (body / rng > 0.5)
        d["ob_bull_level"] = d["low_d"].where(big & (d["close_d"] > d["open_d"]))
        d["ob_bear_level"] = d["high_d"].where(big & (d["close_d"] < d["open_d"]))

        # Forward-fill valid zone levels with expiry
        for z in ("fvg_bull", "fvg_bear"):
            d[f"{z}_lo_f"] = d[f"{z}_lo"].ffill(limit=self.cfg.fvg_max_age_days)
            d[f"{z}_hi_f"] = d[f"{z}_hi"].ffill(limit=self.cfg.fvg_max_age_days)

        # CRITICAL CAUSALITY FIX (Note 4): shift the entire daily frame by 1 day
        # so day i is only visible at day i+1 00:00 UTC!
        d_causal = d.shift(1)
        return d_causal

    # ------------------------------------------------------------------
    # Event emission on 15m bars
    # ------------------------------------------------------------------
    def generate_signals(self, df: pd.DataFrame,
                         structure: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        T = len(df)
        idx = df.index
        sig = pd.DataFrame({
            "side": np.zeros(T, dtype=np.int8),
            "raw_r": np.zeros(T, dtype=np.float64),
            "structural_level": np.zeros(T, dtype=np.float64),
            "invalidation_price": np.zeros(T, dtype=np.float64),
            "event_type": np.zeros(T, dtype=object)
        }, index=idx)

        if structure is None:
            structure = self.daily_structure(df)
        st = structure.reindex(df.index, method="ffill")

        o = df["open"].to_numpy(np.float64)
        h = df["high"].to_numpy(np.float64)
        l = df["low"].to_numpy(np.float64)
        c = df["close"].to_numpy(np.float64)
        atr_d = st["atr_d"].to_numpy(np.float64)
        atr_d = np.where(np.isnan(atr_d) | (atr_d < 1e-9), c * 0.02, atr_d)
        C = self.cfg

        pdh = st["pdh"].to_numpy()
        pdl = st["pdl"].to_numpy()

        # ---------- A. SWEEP & RECLAIM (Usman Noah) ----------
        swept_low = (l < pdl) & ((pdl - l) <= C.sweep_max_penetr_atr * atr_d) & (c > pdl) & np.isfinite(pdl)
        swept_high = (h > pdh) & ((h - pdh) <= C.sweep_max_penetr_atr * atr_d) & (c < pdh) & np.isfinite(pdh)

        # ---------- B. FVG RETEST ----------
        fvg_b_hi = st["fvg_bull_hi_f"].to_numpy()
        fvg_b_lo = st["fvg_bull_lo_f"].to_numpy()
        in_bull_fvg = (l <= fvg_b_hi) & (c >= fvg_b_lo) & np.isfinite(fvg_b_lo)

        fvg_s_lo = st["fvg_bear_lo_f"].to_numpy()
        fvg_s_hi = st["fvg_bear_hi_f"].to_numpy()
        in_bear_fvg = (h >= fvg_s_lo) & (c <= fvg_s_hi) & np.isfinite(fvg_s_hi)

        # ---------- C. ORDER BLOCK TAP ----------
        ob_bull = st["ob_bull_level"].ffill(limit=C.ob_max_pullback_bars // 96).to_numpy()
        ob_bear = st["ob_bear_level"].ffill(limit=C.ob_max_pullback_bars // 96).to_numpy()
        tap_ob_bull = (l <= ob_bull) & (c > ob_bull) & np.isfinite(ob_bull)
        tap_ob_bear = (h >= ob_bear) & (c < ob_bear) & np.isfinite(ob_bear)

        buffer = C.stop_buffer_atr_frac * atr_d

        # Long candidate coordinate emission
        for mask, stop_src, etype in (
            (swept_low, pdl - buffer, "SWEEP_PDL"),
            (in_bull_fvg, fvg_b_lo - buffer, "FVG_BULL"),
            (tap_ob_bull, ob_bull - buffer, "OB_BULL"),
        ):
            stop = np.where(mask, stop_src, 0.0)
            r_dist = c - stop
            ok = mask & (r_dist / c >= C.min_r_dist_pct) & (r_dist / c <= C.max_r_dist_pct)
            sig.loc[ok, "side"] = 1
            sig.loc[ok, "raw_r"] = r_dist[ok]
            sig.loc[ok, "structural_level"] = pdl[ok] if etype == "SWEEP_PDL" else stop_src[ok]
            sig.loc[ok, "invalidation_price"] = stop[ok]
            sig.loc[ok, "event_type"] = etype

        # Short candidate coordinate emission (don't overwrite long same bar)
        for mask, stop_src, etype in (
            (swept_high, pdh + buffer, "SWEEP_PDH"),
            (in_bear_fvg, fvg_s_hi + buffer, "FVG_BEAR"),
            (tap_ob_bear, ob_bear + buffer, "OB_BEAR"),
        ):
            stop = np.where(mask, stop_src, 0.0)
            r_dist = stop - c
            ok = mask & (r_dist / c >= C.min_r_dist_pct) & (r_dist / c <= C.max_r_dist_pct) & (sig["side"].to_numpy() == 0)
            sig.loc[ok, "side"] = -1
            sig.loc[ok, "raw_r"] = r_dist[ok]
            sig.loc[ok, "structural_level"] = stop_src[ok]
            sig.loc[ok, "invalidation_price"] = stop[ok]
            sig.loc[ok, "event_type"] = etype

        return sig

    def event_features(self, df: pd.DataFrame, sig: pd.DataFrame) -> pd.DataFrame:
        idx = df.index
        st = self.daily_structure(df).reindex(idx, method="ffill")
        atr_d = st["atr_d"].reindex(idx).ffill().clip(lower=1e-9)
        c = df["close"]
        F = pd.DataFrame(index=idx)
        pdl = st["pdl"].reindex(idx).ffill()
        F["dist_to_pdl_atr"] = (((c - pdl) / atr_d).fillna(0.0)).clip(-5, 5)
        fvg_w = (st["fvg_bull_hi_f"] - st["fvg_bull_lo_f"]).reindex(idx).ffill()
        F["fvg_depth_pct"] = ((fvg_w / c).fillna(0.0)).clip(0, 0.05)
        d_hi = st["high_d"].reindex(idx).ffill()
        d_lo = st["low_d"].reindex(idx).ffill()
        F["reclaim_strength"] = (((c - d_lo) / (d_hi - d_lo).clip(lower=1e-9)).fillna(0.5)).clip(0, 1)
        F["day_range_atr"] = (((d_hi - d_lo) / atr_d).fillna(1.0)).clip(0, 5)
        return F
