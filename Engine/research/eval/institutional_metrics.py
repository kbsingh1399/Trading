"""
================================================================================
ENGINE RESEARCH: LOPEZ DE PRADO (2026) NON-IID INSTITUTIONAL METRICS
================================================================================
Implements:
1. Non-IID Sharpe Ratio Variance with skewness (gamma_3) and kurtosis (gamma_4)
2. Probabilistic Sharpe Ratio (PSR)
3. Minimum Track Record Length (MinTRL)
4. Deflated Sharpe Ratio (DSR) under multi-testing selection
5. Maximum Drawdown, Calmar Ratio, and Win Rate
================================================================================
"""
import numpy as np
import scipy.stats as stats
from typing import Dict, Any


def compute_moments_and_sharpe(returns: np.ndarray, rf: float = 0.0) -> Dict[str, float]:
    """Computes mean, variance, skewness, Pearson kurtosis, and annual Sharpe."""
    n = len(returns)
    if n < 5:
        return {"mean": 0.0, "std": 0.0, "sharpe": 0.0, "skew": 0.0, "kurt": 3.0, "n": n}

    mean_r = float(np.mean(returns))
    std_r = float(np.std(returns, ddof=1))
    if std_r < 1e-12:
        return {"mean": mean_r, "std": 0.0, "sharpe": 0.0, "skew": 0.0, "kurt": 3.0, "n": n}

    sr = (mean_r - rf) / std_r
    skew_r = float(stats.skew(returns, bias=False))
    # Pearson kurtosis where normal = 3.0
    kurt_r = float(stats.kurtosis(returns, fisher=False, bias=False))

    return {
        "mean": mean_r,
        "std": std_r,
        "sharpe": sr,
        "skew": skew_r,
        "kurt": kurt_r,
        "n": n
    }


def compute_psr(sr: float, sr_benchmark: float, t_obs: int, skew: float, kurt: float) -> float:
    """
    Probabilistic Sharpe Ratio:
    PSR(sr*) = Phi( (sr - sr*) * sqrt(T - 1) / sqrt(1 - skew*sr + (kurt - 1)/4 * sr^2) )
    """
    denom = 1.0 - skew * sr + ((kurt - 1.0) / 4.0) * (sr ** 2)
    denom = max(1e-6, denom)
    z = (sr - sr_benchmark) * np.sqrt(max(1, t_obs - 1)) / np.sqrt(denom)
    return float(stats.norm.cdf(z))


def compute_min_trl(sr: float, sr_benchmark: float, skew: float, kurt: float, alpha: float = 0.05) -> float:
    """
    Minimum Track Record Length (in bars):
    MinTRL = 1 + [1 - skew*sr + (kurt - 1)/4 * sr^2] * [z_alpha / (sr - sr*)]^2
    """
    if sr <= sr_benchmark:
        return float("inf")
    z_alpha = stats.norm.ppf(1.0 - alpha)
    var_mult = 1.0 - skew * sr + ((kurt - 1.0) / 4.0) * (sr ** 2)
    var_mult = max(1e-6, var_mult)
    min_t = 1.0 + var_mult * ((z_alpha / (sr - sr_benchmark)) ** 2)
    return float(min_t)


def compute_deflated_sharpe_ratio(
    sr: float,
    all_tested_srs: np.ndarray,
    t_obs: int,
    skew: float,
    kurt: float
) -> float:
    """
    Deflated Sharpe Ratio (DSR) under selection bias over K tested strategies.
    E[max(SR)] approximated via Euler-Mascheroni constant:
    E[max] = (1 - gamma) * Phi^{-1}(1 - 1/K) + gamma * Phi^{-1}(1 - 1/(K*e))
    """
    k = len(all_tested_srs)
    if k <= 1:
        return compute_psr(sr, 0.0, t_obs, skew, kurt)

    em_const = 0.57721566490153286  # Euler-Mascheroni
    var_srs = float(np.var(all_tested_srs, ddof=1)) if k > 1 else 0.0
    sigma_sr = np.sqrt(max(1e-6, var_srs))

    # Expected max SR under null hypothesis of zero true skill
    p1 = stats.norm.ppf(1.0 - 1.0 / k)
    p2 = stats.norm.ppf(1.0 - 1.0 / (k * np.e))
    e_max_sr = sigma_sr * ((1.0 - em_const) * p1 + em_const * p2)

    return compute_psr(sr, e_max_sr, t_obs, skew, kurt)
