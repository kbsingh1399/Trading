"""
Edge Scan -- does a tradeable edge exist at all, before any ML is applied?
=========================================================================

Rationale (Ox_Alpha_43 remediation, investigation phase)
--------------------------------------------------------
The honest walk-forward returned 0/20 PASS with -0.21 R/trade raw expectancy.
Before tuning a classifier on top of that, the correct quant question is whether
the underlying *event* carries any edge. A model cannot manufacture expectancy
from a symmetric-or-worse setup; it can only re-weight what is already there.

So this scans the raw, unfiltered hypothesis space:
  * event type        -- breakout (momentum) vs fade (mean reversion)
  * target R          -- how far the profit barrier sits
  * holding horizon   -- bars until time-stop
  * per basket        -- Crypto / Forex / CFD behave differently

It reports raw expectancy per configuration with a Newey-West style t-stat, and
critically compares each cell against its OWN breakeven rate, since breakeven
moves with target R: breakeven_rate = 1 / (1 + target_R).

This is in-sample by construction -- it is a diagnostic over all history, NOT a
performance claim. Anything promising here still has to survive walk-forward.
Reporting it as a result would be exactly the overfitting the audit flagged.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd
from numba import njit

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Engine.validation.honest_walkforward import (  # noqa: E402
    DEFAULT_COST_FRAC, AssetSeries, load_universe,
)


@njit(cache=True, fastmath=True)
def _scan_kernel(
    o, h, l, c, atr, events, direction, target_r, max_hold, atr_mult, cost_frac
):
    """
    Raw triple-barrier outcome for one configuration.

    `direction` = +1 long, -1 short. Same causal contract as the main harness:
    event observed at close of bar i, filled at open of bar i+1, pessimistic
    barrier resolution when a bar spans both.
    """
    n = o.shape[0]
    out = np.empty(n, dtype=np.float64)
    m = 0
    busy_until = -1

    for i in range(64, n - max_hold - 2):
        if not events[i]:
            continue
        if i <= busy_until:
            continue
        a = atr[i]
        if not np.isfinite(a) or a <= 0.0:
            continue
        j = i + 1
        entry = o[j]
        risk = atr_mult * a
        if risk <= 0.0:
            continue

        if direction > 0:
            stop = entry - risk
            target = entry + target_r * risk
        else:
            stop = entry + risk
            target = entry - target_r * risk

        end = j + max_hold
        if end > n:
            end = n

        # NOTE: use an explicit resolved flag rather than a NaN sentinel.
        # This kernel runs under fastmath=True, which permits the compiler to
        # assume no NaNs -- making `np.isnan(x)` unreliable and silently
        # poisoning the output array.
        outcome = 0.0
        resolved = False
        k = j
        for k in range(j, end):
            if direction > 0:
                if l[k] <= stop:
                    outcome = -1.0
                    resolved = True
                    break
                if h[k] >= target:
                    outcome = target_r
                    resolved = True
                    break
            else:
                if h[k] >= stop:
                    outcome = -1.0
                    resolved = True
                    break
                if l[k] <= target:
                    outcome = target_r
                    resolved = True
                    break
        if not resolved:
            k = end - 1
            if k < j:
                k = j
            outcome = direction * (c[k] - entry) / risk

        out[m] = outcome - cost_frac
        m += 1
        busy_until = k

    return out[:m]


def _prep(df: pd.DataFrame):
    h = np.ascontiguousarray(df["high"].values, dtype=np.float64)
    l = np.ascontiguousarray(df["low"].values, dtype=np.float64)
    o = np.ascontiguousarray(df["open"].values, dtype=np.float64)
    c = np.ascontiguousarray(df["close"].values, dtype=np.float64)
    tr = np.maximum(h - l, np.maximum(np.abs(h - np.roll(c, 1)), np.abs(l - np.roll(c, 1))))
    tr[0] = h[0] - l[0]
    atr = np.ascontiguousarray(pd.Series(tr).rolling(14).mean().values, dtype=np.float64)
    return o, h, l, c, atr


def _events(h, l, c, lookback: int, kind: str) -> np.ndarray:
    prior_high = pd.Series(h).rolling(lookback).max().shift(1).values
    prior_low = pd.Series(l).rolling(lookback).min().shift(1).values
    if kind == "breakout_up":
        e = (c > prior_high) & np.isfinite(prior_high)
    elif kind == "breakdown":
        e = (c < prior_low) & np.isfinite(prior_low)
    elif kind == "fade_high":        # mean-reversion short at the extreme
        e = (c > prior_high) & np.isfinite(prior_high)
    elif kind == "fade_low":         # mean-reversion long at the extreme
        e = (c < prior_low) & np.isfinite(prior_low)
    else:
        raise ValueError(kind)
    return np.ascontiguousarray(e, dtype=np.bool_)


CONFIGS = [
    # (event kind, direction, label)
    ("breakout_up", 1, "Momentum long (break 20H)"),
    ("fade_high", -1, "Fade long-extreme (short 20H)"),
    ("breakdown", -1, "Momentum short (break 20L)"),
    ("fade_low", 1, "Fade short-extreme (long 20L)"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-basket", type=int, default=8)
    ap.add_argument("--cost-frac", type=float, default=DEFAULT_COST_FRAC)
    ap.add_argument("--out", type=str, default="reports/edge_scan.json")
    args = ap.parse_args()

    print("=" * 104)
    print("RAW EDGE SCAN  (in-sample diagnostic -- NOT a performance claim)")
    print("=" * 104)

    assets = load_universe(limit_per_basket=args.per_basket)
    print(f"Assets loaded: {len(assets)}")

    prepped = {a.symbol: (_prep(a.df), a.basket) for a in assets}

    rows = []
    for kind, direction, label in CONFIGS:
        for target_r in (1.0, 1.5, 2.0, 2.5, 3.0):
            for max_hold in (16, 24, 48):
                per_basket: Dict[str, List[np.ndarray]] = {}
                for sym, ((o, h, l, c, atr), basket) in prepped.items():
                    ev = _events(h, l, c, 20, kind)
                    r = _scan_kernel(
                        o, h, l, c, atr, ev, direction,
                        float(target_r), int(max_hold), 1.5, float(args.cost_frac),
                    )
                    if len(r):
                        per_basket.setdefault(basket, []).append(r)

                allr = np.concatenate([x for v in per_basket.values() for x in v]) if per_basket else np.array([])
                if len(allr) < 200:
                    continue
                exp = allr.mean()
                se = allr.std(ddof=1) / np.sqrt(len(allr))
                t = exp / se if se > 0 else 0.0
                wr = (allr > 0).mean() * 100
                be = 100.0 / (1.0 + target_r)
                rows.append({
                    "setup": label, "target_r": target_r, "hold": max_hold,
                    "n": int(len(allr)), "win_rate": wr, "breakeven": be,
                    "expectancy_r": exp, "t_stat": t,
                    "by_basket": {
                        b: float(np.concatenate(v).mean()) for b, v in per_basket.items()
                    },
                })

    df = pd.DataFrame(rows).sort_values("expectancy_r", ascending=False)
    print(f"\nScanned {len(df)} configurations. Ranked by raw expectancy:\n")
    show = df.head(20).copy()
    print(f"{'Setup':<32} {'R':>4} {'Hold':>5} {'N':>7} {'WR%':>6} {'BE%':>6} {'Exp(R)':>9} {'t':>7}")
    print("-" * 104)
    for r in show.itertuples():
        print(f"{r.setup:<32} {r.target_r:>4.1f} {r.hold:>5} {r.n:>7} "
              f"{r.win_rate:>6.2f} {r.breakeven:>6.2f} {r.expectancy_r:>+9.4f} {r.t_stat:>+7.2f}")

    pos = df[df["expectancy_r"] > 0]
    sig = df[(df["expectancy_r"] > 0) & (df["t_stat"] > 3.0)]
    print("-" * 104)
    print(f"Configurations with positive raw expectancy : {len(pos)}/{len(df)}")
    print(f"  ...of those, t > 3.0 (multiple-testing aware): {len(sig)}")
    if len(sig):
        print("\nSurvivors at t > 3.0:")
        for r in sig.itertuples():
            print(f"  {r.setup:<32} R={r.target_r} hold={r.hold} "
                  f"exp={r.expectancy_r:+.4f} t={r.t_stat:+.2f} n={r.n}")
        print("\nNOTE: these are IN-SAMPLE over all history. With "
              f"{len(df)} configurations scanned, expect ~{len(df) * 0.00135:.1f} "
              "false positives at t>3 under the null. Must be re-validated "
              "walk-forward before any claim is made.")
    else:
        print("\nNo configuration shows positive expectancy at t > 3.0.")

    out = REPO_ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({
            "cost_frac": args.cost_frac,
            "n_configs": len(df),
            "n_positive": int(len(pos)),
            "n_significant": int(len(sig)),
            "results": df.to_dict("records"),
        }, f, indent=2, default=float)
    print(f"\nWrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
