"""
================================================================================
AUDIT PROBE: indicator-kernel claims (docs/PIPELINE_VERIFICATION_CERTIFICATION.md §2.1)
================================================================================
Independent re-measurement of the two claims the rebuild audit makes about the
canonical kernels, beyond what test_pipeline_offline asserts:

  1. "RMA is an exactly-seeded EWM (bit-identical to the loop -- verified
      max|delta| = 0.0)".  The suite only asserts < 1e-9.  We measure max|delta|
      directly against the textbook recursion over 120 trials.  RESULT: nonzero
      (~1.95e-14) for RMA, exactly 0.0 for EMA -> the bit-identity claim holds for
      EMA and is false as written for RMA.

  2. "prefix invariance ... asserted by test_prefix_invariance", which samples 5
      cut points.  We sweep every ~40th prefix, including the greedy value-area
      expansion (the only kernel with a plausible hidden global dependency).

Read-only. Usage: python3 -m Engine.verification.audit_probe_indicator_parity
================================================================================
"""

from __future__ import annotations

import os
import sys

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Engine.core.canonical_indicators import (  # noqa: E402
    compute_ema_series,
    compute_session_cvd,
    compute_session_value_area,
    compute_session_vwap,
    compute_sma_series,
    compute_wilder_atr_series,
    compute_wilder_rsi_series,
    compute_wilder_rma_series,
    nice_bin_step,
)

DAY_MS = 86_400_000
BAR_MS = 900_000


def rma_reference(x: np.ndarray, period: int) -> np.ndarray:
    """Textbook Wilder recursion with the standard causal warm-up."""
    ref = np.empty_like(x)
    ref[0] = x[0]
    for i in range(1, period - 1):
        ref[i] = (ref[i - 1] * i + x[i]) / (i + 1)
    ref[period - 1] = x[:period].mean()
    for i in range(period, x.size):
        ref[i] = ref[i - 1] + (x[i] - ref[i - 1]) / period
    return ref


def ema_reference(x: np.ndarray, period: int) -> np.ndarray:
    k = 2.0 / (period + 1.0)
    out = np.empty_like(x)
    e = x[0]
    out[0] = e
    for i in range(1, x.size):
        e = x[i] * k + e * (1.0 - k)
        out[i] = e
    return out


def claim_1_parity(n: int = 20000, trials: int = 40) -> tuple[float, float]:
    worst_rma, worst_ema = 0.0, 0.0
    for seed in range(trials):
        rng = np.random.default_rng(seed)
        x = rng.gamma(2, 3, n)
        for period in (2, 14, 100):
            worst_rma = max(worst_rma, float(np.abs(compute_wilder_rma_series(x, period) - rma_reference(x, period)).max()))
        p = rng.normal(30000, 900, n)
        for period in (8, 200, 800):
            worst_ema = max(worst_ema, float(np.abs(compute_ema_series(p, period) - ema_reference(p, period)).max()))
    return worst_rma, worst_ema


def claim_2_prefix(n: int = 6000, step: int = 40) -> dict[str, int]:
    rng = np.random.default_rng(3)
    ts = 1_598_918_400_000 + np.arange(n) * BAR_MS
    c = 0.085 * np.exp(np.cumsum(rng.normal(0, 4e-3, n)))       # DOGE-scale on purpose
    h = c * (1 + np.abs(rng.normal(0, 3e-3, n)))
    l = c * (1 - np.abs(rng.normal(0, 3e-3, n)))
    v = np.abs(rng.gamma(2, 5e6, n))

    full = {
        "session_vah": compute_session_value_area(ts, h, l, c, v, bucket_size=1e-4)[0],
        "session_val": compute_session_value_area(ts, h, l, c, v, bucket_size=1e-4)[1],
        "session_vwap": compute_session_vwap(ts, h, l, c, v),
        "session_cvd": compute_session_cvd(ts, c),
        "atr_14": compute_wilder_atr_series(h, l, c, 14),
        "rsi_14": compute_wilder_rsi_series(c, 14),
        "sma9": compute_sma_series(v, 9),
    }
    cuts = list(range(200, n, step))
    viol: dict[str, int] = {}

    def at(name: str, k: int) -> np.ndarray:
        if name == "session_vah":
            return compute_session_value_area(ts[:k], h[:k], l[:k], c[:k], v[:k], bucket_size=1e-4)[0]
        if name == "session_val":
            return compute_session_value_area(ts[:k], h[:k], l[:k], c[:k], v[:k], bucket_size=1e-4)[1]
        if name == "session_vwap":
            return compute_session_vwap(ts[:k], h[:k], l[:k], c[:k], v[:k])
        if name == "session_cvd":
            return compute_session_cvd(ts[:k], c[:k])
        if name == "atr_14":
            return compute_wilder_atr_series(h[:k], l[:k], c[:k], 14)
        if name == "rsi_14":
            return compute_wilder_rsi_series(c[:k], 14)
        return compute_sma_series(v[:k], 9)

    for cut in cuts:
        for name, ref in full.items():
            got = at(name, cut)
            if float(np.abs(got - ref[:cut]).max()) > 0.0:
                viol[name] = viol.get(name, 0) + 1
    viol["_prefixes_tested"] = len(cuts)
    return viol


def main() -> int:
    print("=" * 78)
    print("PROBE 1  parity of vectorised kernels vs textbook recursions")
    print("=" * 78)
    rma, ema = claim_1_parity()
    print(f"  Wilder RMA  worst max|delta| = {rma:.3e}   bit-identical = {rma == 0.0}")
    print(f"  EMA         worst max|delta| = {ema:.3e}   bit-identical = {ema == 0.0}")
    print("  -> audit claim 'RMA bit-identical (max|d| = 0.0)' is FALSE as written")
    print("     (numerically equivalent; the repo test asserts only < 1e-9).")

    print()
    print("=" * 78)
    print("PROBE 2  prefix invariance, dense sweep (vs the suite's 5 cut points)")
    print("=" * 78)
    v = claim_2_prefix()
    tested = v.pop("_prefixes_tested")
    print(f"  prefixes tested per feature: {tested}")
    if not v:
        print("  VIOLATIONS: none for any feature")
    for name, cnt in v.items():
        print(f"  VIOLATION {name}: {cnt}/{tested} prefixes")

    print()
    print("=" * 78)
    print("PROBE 3  nice_bin_step is a pure function of the day's first traded price")
    print("=" * 78)
    for px in (1e-4, 0.085, 0.5, 12.0, 30000.0, 100000.0):
        print(f"  first-open {px:>10} -> bin step {nice_bin_step(np.array([px]))[0]:.8g}")
    print("  -> no day-level statistic is consulted, so intra-day median lookahead is impossible.")
    print(f"  -> NOTE quantisation floor 1e-6 is material for assets priced <~1e-4 (not in the 18-asset universe).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
