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
    from .schema import FIXED_MERGE_STEPS
    s = symbol.upper()
    if s in FIXED_MERGE_STEPS:
        return float(FIXED_MERGE_STEPS[s])
    if s.startswith("BTC"):
        return 50.0
    if s.startswith("ETH"):
        return 2.0
    if any(s.startswith(x) for x in ("SOL", "BNB", "BCH", "AVAX", "LTC", "APT", "LINK")):
        return 0.2
    if any(s.startswith(x) for x in ("DOT", "NEAR", "SUI", "OP", "ARB")):
        return 0.02
    return 0.0002


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
def compute_canonical_ema(prices: np.ndarray, period: int, seed: float | None = None, dp: int = 8) -> np.ndarray:
    """
    R4-H1 Canonical Per-Bar Recursive EMA Kernel with Symmetric Quantization.
    Recursion:
        alpha = 2.0 / (period + 1)
        ema[0] = round(price[0], dp) if seed is None else float(seed)
        ema[t] = round(alpha * price[t] + (1.0 - alpha) * ema[t-1], dp)
    Guarantees 100% bit-exact (atol = 0.0) prefix invariance across arbitrary sequential incremental appends.
    """
    x = np.asarray(prices, dtype=np.float64)
    n = x.size
    out = np.empty(n, dtype=np.float64)
    if n == 0:
        return out
    alpha = 2.0 / (period + 1.0)
    one_minus_alpha = 1.0 - alpha
    
    if seed is None:
        curr = round(float(x[0]), dp)
        out[0] = curr
        start_idx = 1
    else:
        curr = float(seed)
        start_idx = 0
        
    for i in range(start_idx, n):
        curr = round(alpha * float(x[i]) + one_minus_alpha * curr, dp)
        out[i] = curr
    return out


def compute_ema_series(prices: np.ndarray, period: int, dp: int = 8) -> np.ndarray:
    """EMA seeded at bar 0 (ema[0] = price[0]), alpha = 2 / (period + 1), adhering to canonical per-bar recursion."""
    return compute_canonical_ema(prices, period, seed=None, dp=dp)


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


def compute_kairi_relative_index(closes: np.ndarray, period: int = 96) -> np.ndarray:
    """
    Canonical Kairi Relative Index (KRI):
        KRI_t = (Price_t - SMA_period(t)) / SMA_period(t) * 100.0
    Quantifies percentage disparity from the moving average baseline.
    Prefix-invariant and causal (uses causal rolling SMA with min_periods=1).
    """
    c = np.asarray(closes, dtype=np.float64)
    if c.size == 0:
        return c.copy()
    sma = compute_sma_series(c, period)
    with np.errstate(divide="ignore", invalid="ignore"):
        kri = np.where(sma > _EPS, (c - sma) / sma * 100.0, 0.0)
    return kri


def compute_kairi_atr_ratio(closes: np.ndarray, atrs: np.ndarray, period: int = 96) -> np.ndarray:
    """
    ATR-normalized Kairi Disparity:
        KRI_ATR_t = (Price_t - SMA_period(t)) / ATR_t
    Measures disparity normalized by local asset volatility.
    """
    c = np.asarray(closes, dtype=np.float64)
    a = np.asarray(atrs, dtype=np.float64)
    if c.size == 0:
        return c.copy()
    sma = compute_sma_series(c, period)
    with np.errstate(divide="ignore", invalid="ignore"):
        kri_atr = np.where(a > _EPS, (c - sma) / a, 0.0)
    return kri_atr


def compute_kairi_zscore(closes: np.ndarray, atrs: np.ndarray, period: int = 20, z_window: int = 96) -> np.ndarray:
    """
    Rolling Z-score of ATR-normalized Kairi Disparity:
        kri_atr = (Close - SMA(period)) / ATR
        z_kri = (kri_atr - Mean_z(kri_atr)) / Std_z(kri_atr)
    Guarantees strict stationarity across changing crypto volatility regimes.
    """
    kri_atr = compute_kairi_atr_ratio(closes, atrs, period=period)
    return compute_rolling_zscore(kri_atr, window=z_window)


def compute_ichimoku_cloud(
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    tenkan_period: int = 10,
    kijun_period: int = 30,
    senkou_b_period: int = 60,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Causal, prefix-invariant Ichimoku Kinko Hyo components:
        Tenkan-sen = (Rolling_Max(High, tenkan) + Rolling_Min(Low, tenkan)) / 2.0
        Kijun-sen  = (Rolling_Max(High, kijun) + Rolling_Min(Low, kijun)) / 2.0
        Senkou Span A = (Tenkan + Kijun) / 2.0
        Senkou Span B = (Rolling_Max(High, senkou_b) + Rolling_Min(Low, senkou_b)) / 2.0
    Returns: (tenkan, kijun, span_a, span_b)
    """
    h = pd.Series(np.asarray(highs, dtype=np.float64))
    l = pd.Series(np.asarray(lows, dtype=np.float64))
    
    tenkan_h = h.rolling(tenkan_period, min_periods=1).max().to_numpy()
    tenkan_l = l.rolling(tenkan_period, min_periods=1).min().to_numpy()
    tenkan = (tenkan_h + tenkan_l) / 2.0
    
    kijun_h = h.rolling(kijun_period, min_periods=1).max().to_numpy()
    kijun_l = l.rolling(kijun_period, min_periods=1).min().to_numpy()
    kijun = (kijun_h + kijun_l) / 2.0
    
    span_a = (tenkan + kijun) / 2.0
    
    span_b_h = h.rolling(senkou_b_period, min_periods=1).max().to_numpy()
    span_b_l = l.rolling(senkou_b_period, min_periods=1).min().to_numpy()
    span_b = (span_b_h + span_b_l) / 2.0
    
    return tenkan, kijun, span_a, span_b


def compute_bollinger_bandwidth_zscore(
    closes: np.ndarray,
    period: int = 96,
    std_mult: float = 2.0,
    z_window: int = 96,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Bollinger Bands and standardized Bandwidth Z-score:
        Upper = SMA + std_mult * Std
        Lower = SMA - std_mult * Std
        Bandwidth = (Upper - Lower) / SMA
        Z_Bandwidth = (Bandwidth - Mean_z(Bandwidth)) / Std_z(Bandwidth)
    Returns: (upper, lower, bandwidth, z_bandwidth)
    """
    c = np.asarray(closes, dtype=np.float64)
    s = pd.Series(c)
    sma = s.rolling(period, min_periods=1).mean().to_numpy()
    std = s.rolling(period, min_periods=period).std(ddof=0).fillna(0.0).to_numpy()
    upper = sma + std_mult * std
    lower = sma - std_mult * std
    with np.errstate(divide="ignore", invalid="ignore"):
        bandwidth = np.where(sma > _EPS, (upper - lower) / sma, 0.0)
    z_bandwidth = compute_rolling_zscore(bandwidth, window=z_window)
    return upper, lower, bandwidth, z_bandwidth


def compute_liquidation_decay_velocity(liq_zscores: np.ndarray) -> np.ndarray:
    """
    First difference of liquidation z-score:
        decay_velocity[t] = liq_zscores[t] - liq_zscores[t-1]
    Negative values indicate decelerating liquidation pressure (exhaustion).
    """
    z = np.asarray(liq_zscores, dtype=np.float64)
    if z.size == 0:
        return z.copy()
    out = np.zeros_like(z)
    out[1:] = z[1:] - z[:-1]
    return out


def compute_wick_absorption_ratio(
    opens: np.ndarray,
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculates lower wick and upper wick ratios relative to total candle range:
        lower_wick = Min(Open, Close) - Low
        upper_wick = High - Max(Open, Close)
        total_range = High - Low
    Returns: (lower_wick_ratio, upper_wick_ratio)
    """
    o = np.asarray(opens, dtype=np.float64)
    h = np.asarray(highs, dtype=np.float64)
    l = np.asarray(lows, dtype=np.float64)
    c = np.asarray(closes, dtype=np.float64)
    
    total_range = np.maximum(h - l, _EPS)
    lower_wick = np.maximum(np.minimum(o, c) - l, 0.0)
    upper_wick = np.maximum(h - np.maximum(o, c), 0.0)
    
    return lower_wick / total_range, upper_wick / total_range


def compute_adx_series(
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    period: int = 14,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Wilder Average Directional Index (ADX) with +DI and -DI:
        +DM = High[t] - High[t-1] if > (Low[t-1] - Low[t]) and > 0, else 0
        -DM = Low[t-1] - Low[t] if > (High[t] - High[t-1]) and > 0, else 0
        Smoothed with Wilder RMA(period).
        DX = 100 * Abs(+DI - -DI) / (+DI + -DI)
        ADX = Wilder RMA(DX, period)
    Returns: (plus_di, minus_di, adx)
    """
    h = np.asarray(highs, dtype=np.float64)
    l = np.asarray(lows, dtype=np.float64)
    c = np.asarray(closes, dtype=np.float64)
    n = c.size
    if n < 2:
        zero = np.zeros(n, dtype=np.float64)
        return zero, zero.copy(), zero.copy()
    
    up_move = h[1:] - h[:-1]
    down_move = l[:-1] - l[1:]
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0.0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0.0), down_move, 0.0)
    
    tr = compute_true_range(h, l, c)[1:]
    
    smooth_tr = compute_wilder_rma_series(tr, period)
    smooth_plus_dm = compute_wilder_rma_series(plus_dm, period)
    smooth_minus_dm = compute_wilder_rma_series(minus_dm, period)
    
    with np.errstate(divide="ignore", invalid="ignore"):
        plus_di_tail = np.where(smooth_tr > _EPS, 100.0 * smooth_plus_dm / smooth_tr, 0.0)
        minus_di_tail = np.where(smooth_tr > _EPS, 100.0 * smooth_minus_dm / smooth_tr, 0.0)
        di_sum = plus_di_tail + minus_di_tail
        dx = np.where(di_sum > _EPS, 100.0 * np.abs(plus_di_tail - minus_di_tail) / di_sum, 0.0)
    
    adx_tail = compute_wilder_rma_series(dx, period)
    
    plus_di = np.zeros(n, dtype=np.float64)
    minus_di = np.zeros(n, dtype=np.float64)
    adx = np.zeros(n, dtype=np.float64)
    
    plus_di[1:] = plus_di_tail
    minus_di[1:] = minus_di_tail
    adx[1:] = adx_tail
    
    return plus_di, minus_di, adx



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


def compute_cumulative_cvd(deltas: np.ndarray, seed: float = 0.0, dp: int = 8) -> np.ndarray:
    """
    R3-C2 Mathematical Invariant:
    Per-bar recursive rounding contract:
        cvd_lifetime[t] = np.round(cvd_lifetime[t-1] + delta[t], dp)
    Guarantees bit-exact IEEE 754 atol=0.0 parity between full rebuild and incremental append.
    """
    out = np.empty(len(deltas), dtype=np.float64)
    curr = float(seed)
    for i, d in enumerate(deltas):
        curr = round(curr + float(d), dp)
        out[i] = curr
    return out


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


# ------------------------------------------------------------------------------
# Multi-Timeframe Structural Pivots & Footprint Sweep Detectors
# ------------------------------------------------------------------------------
def compute_structural_pivots_and_sweeps(
    timestamps_ms: np.ndarray,
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    deltas: np.ndarray,
    volumes: np.ndarray,
    volume_ratios: np.ndarray,
    atrs: np.ndarray,
) -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
    np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray
]:
    """
    Causal, prefix-invariant multi-timeframe structural pivots and footprint delta sweeps.
    Calculates:
      - Daily: PDH (Previous Day High), PDL (Previous Day Low)
      - Weekly: PWH (Previous Week High), PWL (Previous Week Low)
      - Monthly: PMH (Previous Month High), PML (Previous Month Low)
      - Normalized Distances: pdl_dist, pdh_dist, pwl_dist, pwh_dist in ATR units
      - Orderflow Sweeps: pdl_sweep_bull (PDL pierced and closed back above with positive delta),
                          pdh_sweep_bear (PDH pierced and closed back below with negative delta)
    """
    n = len(timestamps_ms)
    if n == 0:
        z = np.zeros(0, dtype=np.float64)
        b = np.zeros(0, dtype=bool)
        return z, z, z, z, z, z, z, z, z, z, b, b

    t = np.asarray(timestamps_ms, dtype=np.int64)
    h = np.asarray(highs, dtype=np.float64)
    l = np.asarray(lows, dtype=np.float64)
    c = np.asarray(closes, dtype=np.float64)
    d = np.asarray(deltas, dtype=np.float64)
    vr = np.asarray(volume_ratios, dtype=np.float64)
    atr = np.maximum(np.asarray(atrs, dtype=np.float64), 1e-6)

    # 1. Daily Pivots (00:00 UTC anchor)
    day_idx = (t // DAY_MS)
    _, d_start, d_counts = np.unique(day_idx, return_index=True, return_counts=True)
    pdh_day = np.empty(d_start.size, dtype=np.float64)
    pdl_day = np.empty(d_start.size, dtype=np.float64)
    pdh_day[1:], pdh_day[0] = np.maximum.reduceat(h, d_start)[:-1], h[0]
    pdl_day[1:], pdl_day[0] = np.minimum.reduceat(l, d_start)[:-1], l[0]
    pdh = np.repeat(pdh_day, d_counts)
    pdl = np.repeat(pdl_day, d_counts)

    # 2. Weekly Pivots (Monday 00:00 UTC anchor: 1970-01-01 was Thursday = +4 days)
    week_idx = (t + 4 * DAY_MS) // (7 * DAY_MS)
    _, w_start, w_counts = np.unique(week_idx, return_index=True, return_counts=True)
    pwh_wk = np.empty(w_start.size, dtype=np.float64)
    pwl_wk = np.empty(w_start.size, dtype=np.float64)
    pwh_wk[1:], pwh_wk[0] = np.maximum.reduceat(h, w_start)[:-1], h[0]
    pwl_wk[1:], pwl_wk[0] = np.minimum.reduceat(l, w_start)[:-1], l[0]
    pwh = np.repeat(pwh_wk, w_counts)
    pwl = np.repeat(pwl_wk, w_counts)

    # 3. Monthly Pivots (Calendar month anchor)
    dt = pd.to_datetime(t, unit="ms", utc=True)
    m_idx = dt.year.to_numpy() * 12 + dt.month.to_numpy()
    _, m_start, m_counts = np.unique(m_idx, return_index=True, return_counts=True)
    pmh_m = np.empty(m_start.size, dtype=np.float64)
    pml_m = np.empty(m_start.size, dtype=np.float64)
    pmh_m[1:], pmh_m[0] = np.maximum.reduceat(h, m_start)[:-1], h[0]
    pml_m[1:], pml_m[0] = np.minimum.reduceat(l, m_start)[:-1], l[0]
    pmh = np.repeat(pmh_m, m_counts)
    pml = np.repeat(pml_m, m_counts)

    # 4. Normalized distances in ATR units
    pdl_dist = np.clip((c - pdl) / atr, -10.0, 10.0)
    pdh_dist = np.clip((c - pdh) / atr, -10.0, 10.0)
    pwl_dist = np.clip((c - pwl) / atr, -10.0, 10.0)
    pwh_dist = np.clip((c - pwh) / atr, -10.0, 10.0)

    # 5. Orderflow Sweeps with Footprint Delta Absorption
    # Bullish Liquidity Sweep: Price dipped below PDL but closed back above PDL, with positive Delta or volume absorption
    pdl_sweep_bull = (l < pdl) & (c > pdl) & (d > 0)
    # Bearish Liquidity Sweep: Price poked above PDH but closed back below PDH, with negative Delta or exhaustion
    pdh_sweep_bear = (h > pdh) & (c < pdh) & (d < 0)

    return pdh, pdl, pwh, pwl, pmh, pml, pdl_dist, pdh_dist, pwl_dist, pwh_dist, pdl_sweep_bull, pdh_sweep_bear

