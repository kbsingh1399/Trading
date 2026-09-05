"""
================================================================================
CANONICAL TECHNICAL & MICROSTRUCTURE INDICATOR KERNELS (VECTORISED, CAUSAL)
================================================================================
Every kernel in this module satisfies the *prefix-invariance* property:

    f(x[:n])[:k] == f(x)[:k]   for all k <= n

i.e. the value at bar t depends only on bars <= t. This is asserted by
verification/test_pipeline_offline.py::test_prefix_invariance.

No kernel iterates over bars in Python. Recursive filters (EMA / Wilder RMA)
are expressed as exactly-seeded exponentially weighted means, which are
bit-identical to the textbook per-bar recursion.
================================================================================
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

DAY_MS = 86_400_000
_EPS = 1e-12


# ------------------------------------------------------------------------------
# Symbol scale helpers
# ------------------------------------------------------------------------------
def get_merge_level(symbol: str) -> float:
    """Canonical value-area bucket size (price units) per asset scale."""
    s = symbol.upper()
    if s.startswith("BTC"):
        return 25.0
    if s.startswith("ETH"):
        return 1.0
    if any(s.startswith(x) for x in ("SOL", "BNB", "BCH", "AVAX", "LTC", "APT", "LINK")):
        return 0.1
    if any(s.startswith(x) for x in ("DOT", "NEAR", "SUI", "OP", "ARB")):
        return 0.01
    return 0.0001


def nice_bin_step(prices: np.ndarray, bps: float = 3.5) -> np.ndarray:
    """
    Element-wise 'nice' price bin step targeting ``bps`` basis points of price.
    Vectorised equivalent of the rounding ladder used by the tick fetcher so
    exact and synthetic rungs share identical geometry rules.
    """
    raw = np.asarray(prices, dtype=np.float64) * (bps / 10_000.0)
    step = np.where(
        raw >= 10.0, np.round(raw / 5.0) * 5.0,
        np.where(raw >= 1.0, np.round(raw, 1),
        np.where(raw >= 0.1, np.round(raw, 2),
        np.where(raw >= 0.01, np.round(raw, 3),
        np.where(raw >= 0.001, np.round(raw, 4),
        np.round(raw, 6))))),
    )
    return np.maximum(step, 1e-6)


# ------------------------------------------------------------------------------
# Recursive smoothers
# ------------------------------------------------------------------------------
def compute_ema_series(prices: np.ndarray, period: int) -> np.ndarray:
    """EMA seeded at bar 0 (ema[0] = price[0]), alpha = 2 / (period + 1)."""
    x = np.asarray(prices, dtype=np.float64)
    if x.size == 0:
        return x.copy()
    return pd.Series(x).ewm(span=period, adjust=False).mean().to_numpy()


def compute_wilder_rma_series(values: np.ndarray, period: int) -> np.ndarray:
    """
    Wilder RMA with causal warm-up:
        bars 0 .. period-2 : expanding mean of values[:t+1]
        bars period-1 ..   : y_t = y_{t-1} + (x_t - y_{t-1}) / period
    Bit-identical to the per-bar recursion (verified max|delta| = 0.0).
    """
    x = np.asarray(values, dtype=np.float64)
    n = x.size
    if n == 0:
        return x.copy()
    expanding = np.cumsum(x) / np.arange(1, n + 1, dtype=np.float64)
    if n <= period:
        return expanding
    seeded = x.copy()
    seeded[period - 1] = expanding[period - 1]
    tail = pd.Series(seeded[period - 1:]).ewm(alpha=1.0 / period, adjust=False).mean().to_numpy()
    out = np.empty(n, dtype=np.float64)
    out[: period - 1] = expanding[: period - 1]
    out[period - 1:] = tail
    return out


def compute_wilder_rsi_series(closes: np.ndarray, period: int = 14) -> np.ndarray:
    """Wilder RSI; bar 0 = 50. Degenerate zero-loss bars map to 100 / 50."""
    c = np.asarray(closes, dtype=np.float64)
    n = c.size
    if n == 0:
        return c.copy()
    rsi = np.full(n, 50.0, dtype=np.float64)
    if n == 1:
        return rsi
    d = np.diff(c)
    gains = np.maximum(d, 0.0)
    losses = np.maximum(-d, 0.0)
    avg_gain = compute_wilder_rma_series(gains, period)
    avg_loss = compute_wilder_rma_series(losses, period)
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = avg_gain / avg_loss
        body = 100.0 - 100.0 / (1.0 + rs)
    zero_loss = avg_loss <= _EPS
    body = np.where(zero_loss, np.where(avg_gain > _EPS, 100.0, 50.0), body)
    rsi[1:] = body
    return np.clip(rsi, 0.0, 100.0)


def compute_true_range(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray) -> np.ndarray:
    h = np.asarray(highs, dtype=np.float64)
    l = np.asarray(lows, dtype=np.float64)
    c = np.asarray(closes, dtype=np.float64)
    prev_c = np.empty_like(c)
    prev_c[0] = c[0] if c.size else 0.0
    prev_c[1:] = c[:-1]
    return np.maximum(h - l, np.maximum(np.abs(h - prev_c), np.abs(l - prev_c)))


def compute_wilder_atr_series(highs, lows, closes, period: int = 14) -> np.ndarray:
    if len(closes) == 0:
        return np.array([], dtype=np.float64)
    return compute_wilder_rma_series(compute_true_range(highs, lows, closes), period)


def compute_sma_series(values: np.ndarray, window: int) -> np.ndarray:
    """Simple moving average with causal expanding warm-up (min_periods = 1)."""
    x = np.asarray(values, dtype=np.float64)
    if x.size == 0:
        return x.copy()
    return pd.Series(x).rolling(window, min_periods=1).mean().to_numpy()


def compute_volume_sma9_series(volumes: np.ndarray) -> np.ndarray:
    return compute_sma_series(volumes, 9)


def compute_rolling_zscore(values: np.ndarray, window: int) -> np.ndarray:
    """(x - mean_w) / std_w (ddof = 0). 0.0 during warm-up or when std ~ 0."""
    s = pd.Series(np.asarray(values, dtype=np.float64))
    mean = s.rolling(window, min_periods=window).mean()
    std = s.rolling(window, min_periods=window).std(ddof=0)
    z = (s - mean) / std.where(std > _EPS)
    return z.replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy()


# ------------------------------------------------------------------------------
# Session (00:00 UTC anchored) accumulators
# ------------------------------------------------------------------------------
def session_day_index(timestamps_ms: np.ndarray) -> np.ndarray:
    return (np.asarray(timestamps_ms, dtype=np.int64) // DAY_MS)


def compute_session_cvd(timestamps_ms: np.ndarray, deltas: np.ndarray) -> np.ndarray:
    """Running cumulative delta resetting at each 00:00 UTC boundary."""
    if len(deltas) == 0:
        return np.array([], dtype=np.float64)
    day = session_day_index(timestamps_ms)
    return pd.Series(np.asarray(deltas, dtype=np.float64)).groupby(day).cumsum().to_numpy()


def compute_session_vwap(timestamps_ms, highs, lows, closes, volumes) -> np.ndarray:
    """
    Session VWAP anchored at 00:00 UTC using typical price (H+L+C)/3.
    Falls back to close while the session has zero traded volume.
    """
    c = np.asarray(closes, dtype=np.float64)
    if c.size == 0:
        return c.copy()
    tp = (np.asarray(highs, dtype=np.float64) + np.asarray(lows, dtype=np.float64) + c) / 3.0
    v = np.asarray(volumes, dtype=np.float64)
    day = session_day_index(timestamps_ms)
    pv = pd.Series(tp * v).groupby(day).cumsum().to_numpy()
    cv = pd.Series(v).groupby(day).cumsum().to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        vwap = np.where(cv > _EPS, pv / np.where(cv > _EPS, cv, 1.0), c)
    return vwap


def compute_vwap_zscore(closes, vwap, window: int = 24) -> np.ndarray:
    dev = np.asarray(closes, dtype=np.float64) - np.asarray(vwap, dtype=np.float64)
    s = pd.Series(dev)
    std = s.rolling(window, min_periods=window).std(ddof=0)
    z = s / std.where(std > _EPS)
    return z.replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy()


# ------------------------------------------------------------------------------
# Depth proxy
# ------------------------------------------------------------------------------
def estimate_depth_from_volatility(closes, atrs, base_vols) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    +-1% resting depth proxy from ATR elasticity and traded volume.
    Returns positive magnitudes: (bid_usd, ask_usd, bid_coin, ask_coin).
    """
    c = np.asarray(closes, dtype=np.float64)
    atr = np.asarray(atrs, dtype=np.float64)
    v = np.asarray(base_vols, dtype=np.float64)
    rel_vol = np.maximum(atr / np.maximum(c, 1e-12), 0.001) * 100.0
    scaling = np.clip(1.0 / rel_vol, 0.5, 2.0)
    depth_coin = v * 0.025 * scaling
    depth_usd = depth_coin * c
    return depth_usd, depth_usd.copy(), depth_coin, depth_coin.copy()


# ------------------------------------------------------------------------------
# Developing session value area (dense per-session prefix-sum profile)
# ------------------------------------------------------------------------------
def compute_session_value_area(
    timestamps_ms: np.ndarray,
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    volumes: np.ndarray,
    bucket_size: float = 25.0,
    volume_pct: float = 0.70,
    max_cells_per_chunk: int = 4_000_000,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Developing 70% value area per UTC session plus the prior session's final VA.

    Each bar's volume is spread uniformly over the price buckets it spans
    (floor(low/b) .. floor(high/b)). The developing profile at bar t is the
    prefix sum of the session's per-bar distributions up to and including t,
    so the value at t never sees bars > t.

    The value area is built the classical way: start at the POC bucket and
    repeatedly absorb whichever adjacent bucket (above / below) holds more
    volume until >= ``volume_pct`` of the session volume is enclosed. VAH/VAL
    are the upper/lower bucket prices of that contiguous region.

    Sessions are processed as dense tensors [sessions, bars, buckets]; the only
    Python loops are over session-chunks and over expansion steps (bounded by
    the bucket count), never over bars.
    """
    n = len(timestamps_ms)
    out_vah = np.zeros(n, dtype=np.float64)
    out_val = np.zeros(n, dtype=np.float64)
    if n == 0:
        return out_vah, out_val, out_vah.copy(), out_val.copy()

    h = np.asarray(highs, dtype=np.float64)
    l = np.asarray(lows, dtype=np.float64)
    c = np.asarray(closes, dtype=np.float64)
    v = np.asarray(volumes, dtype=np.float64)
    day = session_day_index(timestamps_ms)

    lo_b = np.floor(l / bucket_size + 1e-9).astype(np.int64)
    hi_b = np.maximum(np.floor(h / bucket_size + 1e-9).astype(np.int64), lo_b)
    cl_b = np.floor(c / bucket_size + 1e-9).astype(np.int64)
    per_bin = v / (hi_b - lo_b + 1)

    _, day_start, bars_per_day = np.unique(day, return_index=True, return_counts=True)
    n_days = day_start.size
    day_of_bar = np.repeat(np.arange(n_days), bars_per_day)
    pos_in_day = np.arange(n) - day_start[day_of_bar]
    day_lo = np.minimum.reduceat(lo_b, day_start)
    day_hi = np.maximum.reduceat(hi_b, day_start)
    day_bins = day_hi - day_lo + 1
    max_bars_global = int(bars_per_day.max())
    # causal traded range inside the session (running min low / running max high)
    run_lo = pd.Series(lo_b).groupby(day).cummin().to_numpy()
    run_hi = pd.Series(hi_b).groupby(day).cummax().to_numpy()

    # greedy session chunking under a dense-cell budget (loop over ~2k sessions)
    chunks = []
    cur_start, cur_max_bins = 0, 0
    for i in range(n_days):
        cand_max = max(cur_max_bins, int(day_bins[i]))
        if i > cur_start and (i - cur_start + 1) * max_bars_global * (cand_max + 1) > max_cells_per_chunk:
            chunks.append((cur_start, i))
            cur_start, cur_max_bins = i, int(day_bins[i])
        else:
            cur_max_bins = cand_max
    chunks.append((cur_start, n_days))

    for d0, d1 in chunks:
        days_in_chunk = np.arange(d0, d1)
        nd = days_in_chunk.size
        idx = np.where((day_of_bar >= d0) & (day_of_bar < d1))[0]
        max_bars = int(bars_per_day[days_in_chunk].max())
        max_bins = int(day_bins[days_in_chunk].max())

        local_day = day_of_bar[idx] - d0
        local_pos = pos_in_day[idx]
        base = day_lo[day_of_bar[idx]]
        col_lo = lo_b[idx] - base
        col_hi = hi_b[idx] - base + 1  # exclusive

        diff = np.zeros((nd, max_bars, max_bins + 1), dtype=np.float64)
        np.add.at(diff, (local_day, local_pos, col_lo), per_bin[idx])
        np.add.at(diff, (local_day, local_pos, col_hi), -per_bin[idx])
        profile = np.cumsum(np.cumsum(diff, axis=2)[:, :, :max_bins], axis=1)
        del diff

        total = profile.sum(axis=2)
        target = total * volume_pct
        # expansion bounds = buckets traded so far in the session (causal)
        lo_bound = np.zeros((nd, max_bars), dtype=np.int64)
        hi_bound = np.zeros((nd, max_bars), dtype=np.int64)
        lo_bound[local_day, local_pos] = run_lo[idx] - base
        hi_bound[local_day, local_pos] = run_hi[idx] - base

        poc = profile.argmax(axis=2)
        a = poc.copy()
        b = poc.copy()
        cur = np.take_along_axis(profile, poc[:, :, None], axis=2)[:, :, 0]
        active = (cur < target) & (total > _EPS)
        for _ in range(max_bins):
            if not active.any():
                break
            up_ok = (b + 1) <= hi_bound
            down_ok = (a - 1) >= lo_bound
            up_v = np.where(up_ok, np.take_along_axis(profile, np.minimum(b + 1, max_bins - 1)[:, :, None], axis=2)[:, :, 0], -1.0)
            down_v = np.where(down_ok, np.take_along_axis(profile, np.maximum(a - 1, 0)[:, :, None], axis=2)[:, :, 0], -1.0)
            choose_up = active & up_ok & (up_v >= down_v)
            choose_down = active & ~choose_up & down_ok
            b = np.where(choose_up, b + 1, b)
            a = np.where(choose_down, a - 1, a)
            cur = cur + np.where(choose_up, up_v, 0.0) + np.where(choose_down, down_v, 0.0)
            active = active & (cur < target) & (((b + 1) <= hi_bound) | ((a - 1) >= lo_bound))
        del profile

        vah_bin = b[local_day, local_pos]
        val_bin = a[local_day, local_pos]
        zero_vol = total[local_day, local_pos] <= _EPS
        close_col = cl_b[idx] - base
        vah_bin = np.where(zero_vol, close_col, vah_bin)
        val_bin = np.where(zero_vol, close_col, val_bin)
        out_vah[idx] = (vah_bin + base) * bucket_size
        out_val[idx] = (val_bin + base) * bucket_size

    # prior-session finalised VA: value at the last bar of the previous session
    day_end = day_start + bars_per_day - 1
    prev_vah_day = np.empty(n_days, dtype=np.float64)
    prev_val_day = np.empty(n_days, dtype=np.float64)
    prev_vah_day[1:] = out_vah[day_end][:-1]
    prev_val_day[1:] = out_val[day_end][:-1]
    prev_vah_day[0] = np.nan
    prev_val_day[0] = np.nan
    prev_vah = np.repeat(prev_vah_day, bars_per_day)
    prev_val = np.repeat(prev_val_day, bars_per_day)
    first = day_of_bar == 0
    prev_vah[first] = out_vah[first]
    prev_val[first] = out_val[first]
    return out_vah, out_val, prev_vah, prev_val
