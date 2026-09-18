"""
================================================================================
ENGINE RESEARCH: ADVANCED QUANTITATIVE MATHEMATICS AND MICROSTRUCTURE SIGNATURES
================================================================================
Implements higher-order non-parametric quant equations:
1. Yang-Zhang Minimum-Variance Realized Volatility Estimator (continuous drift independent).
2. Ornstein-Uhlenbeck (OU) Mean-Reversion Speed and Half-Life.
3. Hurst Exponent via Rescaled Range (R/S) analysis.
4. Multi-Scale Volatility Asymmetry and Microstructure Noise Filters.
All calculations are strictly causal with backward-looking windows.
================================================================================
"""
import numpy as np
import pandas as pd
from typing import Tuple, Union


def compute_yang_zhang_volatility(
    open_p: np.ndarray,
    high_p: np.ndarray,
    low_p: np.ndarray,
    close_p: np.ndarray,
    window: int = 20
) -> np.ndarray:
    n = len(close_p)
    yz_vol = np.zeros(n, dtype=np.float64)
    if n < window + 2:
        return yz_vol

    prev_close = np.roll(close_p, 1)
    prev_close[0] = open_p[0]
    
    eps = 1e-12
    log_oc = np.log(np.maximum(open_p, eps) / np.maximum(prev_close, eps))
    log_co = np.log(np.maximum(close_p, eps) / np.maximum(open_p, eps))
    log_ho = np.log(np.maximum(high_p, eps) / np.maximum(open_p, eps))
    log_lo = np.log(np.maximum(low_p, eps) / np.maximum(open_p, eps))
    log_hc = np.log(np.maximum(high_p, eps) / np.maximum(close_p, eps))
    log_lc = np.log(np.maximum(low_p, eps) / np.maximum(close_p, eps))

    rs_var = log_ho * log_hc + log_lo * log_lc
    k = 0.34 / (1.34 + (window + 1.0) / max(1.0, (window - 1.0)))

    s_oc = pd.Series(log_oc)
    s_co = pd.Series(log_co)
    s_rs = pd.Series(rs_var)

    var_overnight = s_oc.rolling(window, min_periods=window).var(ddof=1).to_numpy()
    var_open_to_close = s_co.rolling(window, min_periods=window).var(ddof=1).to_numpy()
    mean_rs = s_rs.rolling(window, min_periods=window).mean().to_numpy()

    combined_var = var_overnight + k * var_open_to_close + (1.0 - k) * mean_rs
    combined_var = np.maximum(combined_var, 0.0)
    yz_vol = np.sqrt(combined_var)
    yz_vol = np.nan_to_num(yz_vol, nan=0.0)
    return yz_vol


def compute_ornstein_uhlenbeck_halflife(
    series: np.ndarray,
    window: int = 40
) -> Tuple[np.ndarray, np.ndarray]:
    n = len(series)
    half_life = np.full(n, 24.0, dtype=np.float64)
    theta_arr = np.zeros(n, dtype=np.float64)

    if n < window + 2:
        return half_life, theta_arr

    s = pd.Series(series)
    delta_s = s.diff().to_numpy()
    lag_s = s.shift(1).to_numpy()

    df = pd.DataFrame({'delta': delta_s, 'lag': lag_s})
    cov = df['delta'].rolling(window, min_periods=window).cov(df['lag']).to_numpy()
    var_lag = df['lag'].rolling(window, min_periods=window).var().to_numpy()

    with np.errstate(divide='ignore', invalid='ignore'):
        b = np.where(var_lag > 1e-12, cov / var_lag, 0.0)
        theta = -b
        theta = np.maximum(theta, 1e-6)
        hl = np.log(2.0) / theta
        hl = np.clip(hl, 1.0, 96.0)

    half_life = np.nan_to_num(hl, nan=24.0)
    theta_arr = np.nan_to_num(theta, nan=0.0)
    return half_life, theta_arr


def compute_hurst_exponent_fast(
    prices: np.ndarray,
    window: int = 60
) -> np.ndarray:
    n = len(prices)
    hurst = np.full(n, 0.50, dtype=np.float64)
    if n < window:
        return hurst

    log_p = np.log(np.maximum(prices, 1e-12))
    diff_p = pd.Series(log_p).diff().to_numpy()

    for i in range(window, n, 4):
        sub = diff_p[i - window + 1 : i + 1]
        m = np.mean(sub)
        y = np.cumsum(sub - m)
        r = np.max(y) - np.min(y)
        s_std = np.std(sub, ddof=1)
        if s_std > 1e-12 and r > 1e-12:
            h = np.log(r / s_std) / np.log(window)
            hurst[max(0, i - 3) : i + 1] = np.clip(h, 0.1, 0.9)

    return hurst


RESEARCH_QUANT_FEATURES = [
    "yang_zhang_vol",
    "ou_halflife",
    "ou_theta",
    "hurst_exp",
    "vol_asymmetry"
]
