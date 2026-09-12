"""Event studies: does a level / POC event actually carry forward edge?

For every event bar *i* we enter at the **open of bar i+1** (the certified fill
convention), place a stop at the family's structural distance and a take profit
at ``target_r`` *net* R, then walk the next ``horizon`` bars with a stop-first
tie-break.

Reported R is net of the certified 41 bps round-trip friction, expressed in R
units (``friction_r = min(0.0041 * price / stop_distance, 0.6)``), so a mean net R
below zero means the concept cannot pay for its own costs.

An event can have positive expectancy per trade and still fail the portfolio
mandate (concurrency, drawdown, trade count) and vice versa -- both views are
reported by the lab.
"""
from __future__ import annotations

import numpy as np
from numba import njit, prange

FRICTION_FLOOR = 0.0041
MAX_FRICTION_R = 0.6


@njit(cache=True, fastmath=True)
def barrier_outcome(
    o, h, lo, c, i, side, dist, target_r, stop_r, horizon, friction_r
):
    """Net R of a trade entered at the open of ``i+1`` with a fixed barrier pair."""
    n = len(c)
    if i + 1 >= n:
        return np.nan
    entry = o[i + 1]
    if not (dist > 0.0) or not np.isfinite(dist) or not np.isfinite(entry):
        return np.nan
    tgt = entry + side * target_r * dist
    stp = entry - side * stop_r * dist
    end = min(i + 1 + horizon, n)
    exit_r = 0.0
    closed = False
    for j in range(i + 1, end):
        if side == 1:
            if lo[j] <= stp:
                exit_r = -stop_r
                closed = True
                break
            if h[j] >= tgt:
                exit_r = target_r
                closed = True
                break
        else:
            if h[j] >= stp:
                exit_r = -stop_r
                closed = True
                break
            if lo[j] <= tgt:
                exit_r = target_r
                closed = True
                break
    if not closed:
        last = end - 1
        exit_r = (c[last] - entry) / dist if side == 1 else (entry - c[last]) / dist
    return exit_r - friction_r


@njit(cache=True, parallel=True)
def batch_outcomes(o, h, lo, c, idx, side, dist, target_r, horizon):
    out = np.empty(len(idx), np.float64)
    for k in prange(len(idx)):
        i = idx[k]
        d = dist[k]
        e = o[i + 1] if i + 1 < len(o) else np.nan
        fr = 0.0
        if np.isfinite(e) and d > 0.0:
            fr = FRICTION_FLOOR * e / d
            if fr > MAX_FRICTION_R:
                fr = MAX_FRICTION_R
        out[k] = barrier_outcome(o, h, lo, c, i, side[k], d, target_r, 1.0, horizon, fr)
    return out


def summarize(r: np.ndarray) -> dict:
    r = r[np.isfinite(r)]
    if len(r) == 0:
        return {"n": 0, "win_rate": None, "mean_r": None, "median_r": None, "t_stat": None}
    mean = float(r.mean())
    sd = float(r.std(ddof=1)) if len(r) > 1 else 0.0
    se = sd / np.sqrt(len(r)) if len(r) > 1 else np.inf
    return {
        "n": int(len(r)),
        "win_rate": float((r > 0).mean() * 100.0),
        "mean_r": mean,
        "median_r": float(np.median(r)),
        "sd_r": sd,
        "t_stat": float(mean / se) if np.isfinite(se) and se > 0 else None,
        "ci95": float(1.96 * se) if np.isfinite(se) else None,
    }
