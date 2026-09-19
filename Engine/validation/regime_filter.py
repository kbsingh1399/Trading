"""
Regime Filter -- stand aside when mean reversion is the wrong hypothesis
========================================================================

Motivation
----------
The adaptive walk-forward reached 9/15 PASS. Its single hard failure was W13,
"Spring 2025 Precious Metals All-Time High / Sovereign Gold Accumulation Shock"
(-4.33% ROI, 8.74% DD). The strategy is a mean-reversion fade: it shorts the
20-bar high expecting reversion. In a sustained one-way trend that is not a bug,
it is the strategy being applied in the regime it is structurally wrong for.

The Quant-Developers-Resources curriculum names the standard instruments for
exactly this problem:

  * ADX -- "Measures trend strength (0-100) ... Confirms if trend trading is
    suitable" (Technical_Indicators/readme.md). Used here inverted: high ADX
    means trending, so a mean-reversion system should stand down.
  * Hurst exponent -- H > 0.5 trending / persistent, H < 0.5 mean-reverting
    / anti-persistent. Already implemented in
    Engine/research/features/advanced_quant_math.py.
  * Volatility clustering (GARCH family, Risk Management/README.md) -- proxied
    here by a causal realised-vol ratio, since a full GARCH fit per bar is not
    justified by the sample size.

All three are computed causally: every value at bar i uses only bars <= i.

Design note
-----------
The gate is applied as a FEATURE and as a HARD VETO, and both are exposed, so
the walk-forward can decide which (if either) helps. The veto thresholds are
themselves part of the causally-selected configuration -- they are never tuned
against the window being scored.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from numba import njit


@njit(cache=True, fastmath=True)
def _adx_kernel(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int):
    """
    Wilder's ADX, computed causally with his original smoothing.

    Returns (adx, plus_di, minus_di). Index i reflects bars 0..i only.
    """
    n = high.shape[0]
    adx = np.full(n, np.nan, dtype=np.float64)
    pdi = np.full(n, np.nan, dtype=np.float64)
    mdi = np.full(n, np.nan, dtype=np.float64)
    if n < 2 * period + 2:
        return adx, pdi, mdi

    tr_s = 0.0
    plus_s = 0.0
    minus_s = 0.0

    # Wilder warm-up: simple sums over the first `period` bars.
    for i in range(1, period + 1):
        up = high[i] - high[i - 1]
        dn = low[i - 1] - low[i]
        plus_dm = up if (up > dn and up > 0.0) else 0.0
        minus_dm = dn if (dn > up and dn > 0.0) else 0.0
        hl = high[i] - low[i]
        hc = abs(high[i] - close[i - 1])
        lc = abs(low[i] - close[i - 1])
        tr = hl if hl > hc else hc
        if lc > tr:
            tr = lc
        tr_s += tr
        plus_s += plus_dm
        minus_s += minus_dm

    dx_sum = 0.0
    dx_count = 0

    for i in range(period + 1, n):
        up = high[i] - high[i - 1]
        dn = low[i - 1] - low[i]
        plus_dm = up if (up > dn and up > 0.0) else 0.0
        minus_dm = dn if (dn > up and dn > 0.0) else 0.0
        hl = high[i] - low[i]
        hc = abs(high[i] - close[i - 1])
        lc = abs(low[i] - close[i - 1])
        tr = hl if hl > hc else hc
        if lc > tr:
            tr = lc

        # Wilder smoothing
        tr_s = tr_s - tr_s / period + tr
        plus_s = plus_s - plus_s / period + plus_dm
        minus_s = minus_s - minus_s / period + minus_dm

        if tr_s > 1e-12:
            p = 100.0 * plus_s / tr_s
            m = 100.0 * minus_s / tr_s
        else:
            p = 0.0
            m = 0.0
        pdi[i] = p
        mdi[i] = m

        denom = p + m
        dx = 100.0 * abs(p - m) / denom if denom > 1e-12 else 0.0

        if dx_count < period:
            dx_sum += dx
            dx_count += 1
            if dx_count == period:
                adx[i] = dx_sum / period
        else:
            prev = adx[i - 1]
            if np.isnan(prev):
                prev = dx_sum / period
            adx[i] = (prev * (period - 1) + dx) / period

    return adx, pdi, mdi


def compute_adx(df: pd.DataFrame, period: int = 14) -> np.ndarray:
    h = np.ascontiguousarray(df["high"].values, dtype=np.float64)
    l = np.ascontiguousarray(df["low"].values, dtype=np.float64)
    c = np.ascontiguousarray(df["close"].values, dtype=np.float64)
    adx, _, _ = _adx_kernel(h, l, c, int(period))
    return adx


@njit(cache=True, fastmath=True)
def _hurst_kernel(log_p: np.ndarray, window: int, step: int):
    """
    Rolling rescaled-range Hurst exponent, causal.

    H > 0.5 persistent (trending), H < 0.5 anti-persistent (mean reverting).
    Computed every `step` bars and held forward, which is a deliberate
    accuracy/cost trade-off -- the statistic is slow-moving by construction.
    """
    n = log_p.shape[0]
    out = np.full(n, 0.5, dtype=np.float64)
    if n < window + 2:
        return out

    diff = np.empty(n, dtype=np.float64)
    diff[0] = 0.0
    for i in range(1, n):
        diff[i] = log_p[i] - log_p[i - 1]

    last = 0.5
    for i in range(window, n):
        if (i - window) % step == 0:
            s = 0.0
            for k in range(i - window + 1, i + 1):
                s += diff[k]
            m = s / window
            cum = 0.0
            mn = 1e18
            mx = -1e18
            var = 0.0
            for k in range(i - window + 1, i + 1):
                d = diff[k] - m
                cum += d
                if cum < mn:
                    mn = cum
                if cum > mx:
                    mx = cum
                var += d * d
            sd = np.sqrt(var / (window - 1)) if window > 1 else 0.0
            rng = mx - mn
            if sd > 1e-12 and rng > 1e-12:
                h = np.log(rng / sd) / np.log(window)
                if h < 0.1:
                    h = 0.1
                elif h > 0.9:
                    h = 0.9
                last = h
        out[i] = last
    return out


def compute_hurst(df: pd.DataFrame, window: int = 96, step: int = 8) -> np.ndarray:
    c = np.ascontiguousarray(df["close"].values, dtype=np.float64)
    log_p = np.log(np.maximum(c, 1e-12))
    return _hurst_kernel(log_p, int(window), int(step))


def compute_vol_ratio(df: pd.DataFrame, fast: int = 24, slow: int = 96) -> np.ndarray:
    """
    Causal realised-volatility ratio -- a cheap stand-in for a GARCH
    conditional-variance term. Values > 1 mean volatility is expanding.
    """
    r = pd.Series(df["close"].values).pct_change()
    f = r.rolling(fast).std()
    s = r.rolling(slow).std()
    out = (f / (s + 1e-12)).to_numpy()
    return np.nan_to_num(out, nan=1.0, posinf=1.0, neginf=1.0)


def regime_features(df: pd.DataFrame) -> pd.DataFrame:
    """All regime diagnostics for one asset, causally aligned to df's index."""
    return pd.DataFrame({
        "adx": np.nan_to_num(compute_adx(df), nan=0.0),
        "hurst": compute_hurst(df),
        "vol_ratio_rg": compute_vol_ratio(df),
    }, index=df.index)


def mean_reversion_allowed(
    adx: np.ndarray,
    hurst: np.ndarray,
    max_adx: float = 35.0,
    max_hurst: float = 0.58,
) -> np.ndarray:
    """
    Boolean mask: True where a mean-reversion trade is admissible.

    Vetoes strong directional trends (high ADX) and persistent / trending
    price structure (high Hurst) -- the W13 failure mode.
    """
    return (adx <= max_adx) & (hurst <= max_hurst)
