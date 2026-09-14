"""CUSUM event filter features (Lopez de Prado, AFML ch. 2).

The filter accumulates volatility-normalised returns and fires an "event" when the
running sum exceeds a threshold ``k`` ATRs, then resets.  It is a *structural move*
detector rather than a calendar event: it fires when price has moved a meaningful
distance in ATR terms since the last event, so it concentrates sampling on bars
that matter and marks how much pressure is currently built up.

Motivation for adding it here: the 2025 crypto triple-barrier study surveyed for
this lab found CUSUM-filtered sampling with triple-barrier labels turning a
negative baseline into ETH Sharpe 1.42 / BTC 0.51, and the same idea is
standard in the meta-labelling literature.  This lab's own failure analysis says
per-trade *edge* is the binding constraint, so an event-quality feature is the
right thing to test.

Features are causal: all values at bar ``t`` use returns up to and including ``t``.
"""
from __future__ import annotations

import numpy as np
import numba as nb

CUSUM_COLUMNS = ["cs_up_age", "cs_dn_age", "cs_dir", "cs_pressure"]


@nb.njit(cache=True, fastmath=True)
def _cusum(close: np.ndarray, atr: np.ndarray, k: float) -> tuple:
    """Return (up_age, dn_age, dir, pressure) arrays; ages are bars since the event."""
    n = len(close)
    up_age = np.full(n, 1 << 20, np.int64)
    dn_age = np.full(n, 1 << 20, np.int64)
    direction = np.zeros(n, np.int8)
    pressure = np.zeros(n, np.float64)
    s_pos = 0.0
    s_neg = 0.0
    last_dir = 0
    h = 1.0                       # threshold in ATR units; scale cancels in s/h
    for i in range(1, n):
        a = atr[i]
        if not np.isfinite(a) or a <= 0:
            a = close[i] * 0.004
        r = (close[i] - close[i - 1]) / a
        s_pos = max(0.0, s_pos + r)
        s_neg = min(0.0, s_neg + r)
        if s_pos > k:
            up_age[i] = 0
            last_dir = 1
            s_pos = 0.0
            s_neg = 0.0
        elif s_neg < -k:
            dn_age[i] = 0
            last_dir = -1
            s_pos = 0.0
            s_neg = 0.0
        up_age[i] = min(up_age[i], up_age[i - 1] + 1) if up_age[i] != 0 else 0
        dn_age[i] = min(dn_age[i], dn_age[i - 1] + 1) if dn_age[i] != 0 else 0
        direction[i] = last_dir
        pressure[i] = (s_pos - s_neg) / h
    return up_age, dn_age, direction, pressure


def cusum_features(close: np.ndarray, atr: np.ndarray, k: float = 2.0) -> dict:
    """CUSUM features for one symbol: event ages, last direction and pressure."""
    up_age, dn_age, direction, pressure = _cusum(
        np.ascontiguousarray(close, dtype=np.float64),
        np.ascontiguousarray(atr, dtype=np.float64), float(k))
    clip = 200.0
    return {
        "cs_up_age": np.minimum(up_age, clip).astype(np.float32),
        "cs_dn_age": np.minimum(dn_age, clip).astype(np.float32),
        "cs_dir": direction.astype(np.float32),
        "cs_pressure": np.clip(pressure, -5.0, 5.0).astype(np.float32),
    }
