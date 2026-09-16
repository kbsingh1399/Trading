"""
================================================================================
EXECUTION COST MODEL -- SINGLE SOURCE OF TRUTH
================================================================================
Location: Engine/execution_costs.py

Every sleeve in this repository MUST charge the same round-trip cost, expressed
in PRICE terms (basis points of entry price) and only then converted into R
units for the triple-barrier accounting.

Why price terms and not R units: R is a volatility-scaled distance
(R = 1.2 * ATR). A fee expressed as a flat fraction of R therefore varies with
the regime -- it silently charges almost nothing in calm markets and far too
much in violent ones. Real exchange fees, funding and slippage are charged on
notional, so they must be modelled on notional.

History: prior to this module, S1 paid a flat 0.18R (= 25.9 bps while the ATR
floor bound) and T1 paid a flat 20.5 bps, while both the engine docstring and
the master runner docstring claimed 41.0 bps / -0.25R. Neither sleeve was
charged the documented cost and the two sleeves disagreed with each other.
The constant below is now the only place the number lives.
================================================================================
"""

from pathlib import Path


# Round-trip execution drag: taker fee in + taker fee out + modelled slippage.
# 41.0 bps of entry notional, charged identically on every sleeve.
ROUND_TRIP_BPS: float = 41.0

# Same constant as a decimal fraction of price, for (entry_px * ROUND_TRIP_FRAC).
ROUND_TRIP_FRAC: float = ROUND_TRIP_BPS / 10_000.0


def r_units(entry_px: float, r_dist: float) -> float:
    """Convert the round-trip cost into R units for a given entry price and R distance.

    Pure helper for non-JIT call paths. Inside @njit kernels the arithmetic is
    inlined as (entry_p * ROUND_TRIP_FRAC) / dist, which Numba resolves to the
    same value because module-level float globals are compiled as constants.
    """
    if r_dist <= 0.0:
        return 0.0
    return (entry_px * ROUND_TRIP_FRAC) / r_dist


# ==============================================================================
# PHASE 4A -- REGIME-DEPENDENT FRICTION STRESS (Tripathi ssrn-6444878, Lim ssrn-6891658)
# ==============================================================================
# The base 41.0 bps is a calm-market cost. Tripathi stresses execution friction at
# 3x baseline during high-volatility expansions; Lim shows displayed-liquidity
# proxies are most biased during cascades. Both say our cost model is too
# optimistic exactly where the system takes the most damage.
#
# The schedule below was PRE-REGISTERED before any backtest was run, and the
# thresholds are inherited from the regime governor (shock 0.88, elevated 0.70)
# so that one definition of "high volatility" governs the whole repository.
#
# INVARIANT: the multiplier is >= 1.0 always. This is a penalty branch only --
# it can never make execution cheaper than the base cost.
# ==============================================================================

# (vol_rank threshold, multiplier), evaluated in descending order.
STRESS_SCHEDULE = (
    (0.88, 3.0),
    (0.70, 1.5),
)

# Volatility rank is computed on the same 4h BTC series the regime governor uses:
# percentile rank of trailing_30d_atr_pct over the trailing 365 days.
BARS_4H_PER_30D = 180
BARS_4H_PER_365D = 2190
MIN_RANK_HISTORY_BARS = 365


def stress_multiplier(vol_rank) -> float:
    """Map a causal volatility rank onto a friction multiplier. Never below 1.0."""
    if vol_rank is None:
        return 1.0
    try:
        vr = float(vol_rank)
    except (TypeError, ValueError):
        return 1.0
    if vr != vr:  # NaN
        return 1.0
    for threshold, mult in STRESS_SCHEDULE:
        if vr >= threshold:
            return max(1.0, float(mult))
    return 1.0


def build_stress_series(cache_dir) -> "pd.DataFrame":
    """Causal 4h volatility-rank -> friction-multiplier series.

    Uses exactly the regime governor's definition so that one notion of "high
    volatility" governs the whole repository:
      atr_pct            = atr / close * 100
      trailing_30d_atr_pct = atr_pct.rolling(180).mean()      (180 x 4h = 30d)
      vol_rank           = percentile rank of the current value within the
                           trailing 2190 bars (2190 x 4h = 365d)

    ZERO LOOKAHEAD: the returned series is indexed by each 4h bar's CLOSE time
    (open + 4h), so a consumer joining on it can only ever see a rank that was
    fully determined before the joining bar opened.
    """
    import pandas as pd
    import numpy as np

    path = Path(cache_dir) / "BTCUSDT_4h.parquet"
    d = pd.read_parquet(path)
    d["time"] = pd.to_datetime(d["time"], utc=True)
    d = d.sort_values("time").reset_index(drop=True)
    d["atr_pct"] = (d["atr"] / d["close"]) * 100.0
    d["t30"] = d["atr_pct"].rolling(BARS_4H_PER_30D).mean()
    d["vol_rank"] = (
        d["t30"]
        .rolling(BARS_4H_PER_365D, min_periods=MIN_RANK_HISTORY_BARS)
        .apply(lambda x: float((x <= x[-1]).mean()), raw=True)
    )
    d["mult"] = d["vol_rank"].map(stress_multiplier)
    # Index by bar CLOSE so any downstream as-of join is strictly causal.
    d["avail_time"] = (d["time"] + pd.Timedelta(hours=4)).astype("datetime64[ns, UTC]")
    return d[["avail_time", "vol_rank", "mult"]].dropna(subset=["mult"])
