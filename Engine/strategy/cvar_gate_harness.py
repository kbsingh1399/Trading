"""
================================================================================
CVaR99 GATE HARNESS  --  the un-gameable measuring instrument (Phase 4B)
================================================================================
Location: Engine/strategy/cvar_gate_harness.py

WHY THIS EXISTS
---------------
Three mechanisms (cumulative Bayesian, decaying Bayesian, regime governor) each
produced a plausible positive PnL on the OOS windows and each proved to be an
artefact. PnL is gameable: select the variant that maximises it over the same
windows and out-of-sample quietly becomes in-sample.

This harness evaluates an entry veto by TAIL-RISK REDUCTION against an
equal-sized RANDOM-DROP control, following Rajendran & Singaravelu (2026,
SSRN-6344338). The control is drawn from the same trade population, so it
cannot be improved by tuning. A gate that beats random by chance alone will
show up as a high p-value, not as a large ratio.

DEFINITIONS
-----------
CVaR_alpha(S) = mean of the worst ceil(alpha * n_FULL) outcomes in S.

The tail COUNT is fixed from the FULL trade population and reused for every
candidate subset, so a gate and a random control that both drop k trades are
scored on an identical basis. Reducing n and recomputing the tail count would
let a gate look better merely by shrinking the sample.

CVaR on trade RETURNS is negative, so an improved (less bad) tail is a LARGER
number. The sign convention below is therefore:

reduction(S)  = CVaR_alpha(S) - CVaR_alpha(FULL)     # POSITIVE == tail risk reduced
efficiency    = reduction(GATE) / E[reduction(RANDOM)]
p_value       = P(reduction(RANDOM) >= reduction(GATE))

A positive reduction is an improvement.

STRUCTURAL PROPERTY, verified in the unit tests: because the tail count is
fixed and a veto only REMOVES trades, CVaR can never get worse. A veto that
misses the tail entirely scores exactly 0.0 (not negative) -- dropping good
trades leaves the worst-k set untouched. So the harness answers precisely one
question: what fraction of the tail does your veto catch, relative to chance?
That is the whole point. A gate scoring 0.0 was useless; a gate scoring 1.0x
was no better than random.

MEASURED ON
-----------
Primary: post-cost `r_gain` (R multiples). This is the trade-outcome
distribution and is comparable across symbols and regimes.
Secondary: USD `pnl`, reported alongside because capital impact is what a desk
actually feels.

HONEST LIMITATION
-----------------
CVaR99 on n trades averages the worst ~n/100 outcomes. Pooled (1,058 trades)
that is ~11 trades; primary alone (326) is ~3. A 99% tail on a few hundred
observations is noisy, so the harness also reports CVaR95, a bootstrap CI, and
the exact tail count used. Read CVaR99 with that in mind; do not read a third
decimal place.
================================================================================
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np

DEFAULT_ALPHA = 0.99
DEFAULT_MC = 20_000
DEFAULT_BOOT = 10_000


# ------------------------------------------------------------------ core maths
def cvar_at(values: Sequence[float], tail_count: int) -> float:
    """Mean of the worst `tail_count` outcomes. tail_count is fixed by the caller."""
    a = np.asarray(values, dtype=float)
    if a.size == 0:
        return float("nan")
    k = int(max(1, min(tail_count, a.size)))
    return float(np.sort(a)[:k].mean())


def tail_count_for(n: int, alpha: float) -> int:
    """Number of tail observations defining CVaR for a population of size n."""
    return int(max(1, math.ceil((1.0 - alpha) * n)))


def bootstrap_ci(values: Sequence[float], tail_count: int,
                 n_boot: int = DEFAULT_BOOT, seed: int = 7) -> tuple:
    """Percentile bootstrap CI for the CVaR estimate."""
    a = np.asarray(values, dtype=float)
    if a.size <= 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    k = int(max(1, min(tail_count, a.size)))
    idx = rng.integers(0, a.size, size=(n_boot, a.size))
    draws = np.sort(a[idx], axis=1)[:, :k].mean(axis=1)
    return (float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5)))


# ------------------------------------------------------------------- evaluation
def evaluate_gate(r_all: np.ndarray,
                  drop_mask: np.ndarray,
                  alpha: float = DEFAULT_ALPHA,
                  n_mc: int = DEFAULT_MC,
                  seed: int = 11) -> Dict[str, float]:
    """Score one veto against an equal-sized random-drop control.

    drop_mask: bool array, True for trades the veto removes.
    Returns the full comparison dict.
    """
    r_all = np.asarray(r_all, dtype=float)
    n = int(r_all.size)
    k_drop = int(np.count_nonzero(drop_mask))
    k_tail = tail_count_for(n, alpha)

    base = cvar_at(r_all, k_tail)
    kept_gate = r_all[~drop_mask]
    gate_cvar = cvar_at(kept_gate, k_tail)
    # positive == the veto reduced tail risk (CVaR moved up, i.e. losses shrank)
    gate_red = gate_cvar - base

    result = {
        "n_trades": n,
        "alpha": alpha,
        "tail_count": k_tail,
        "n_dropped": k_drop,
        "drop_pct": 100.0 * k_drop / n if n else float("nan"),
        "cvar_base": base,
        "cvar_gated": gate_cvar,
        "reduction": gate_red,
    }

    if k_drop <= 0:
        result.update(mean_random_reduction=0.0, efficiency=float("nan"),
                      p_value=float("nan"), mc_draws=0,
                      random_reduction_std=0.0)
        return result
    if k_drop >= n:
        result.update(mean_random_reduction=float("nan"), efficiency=float("nan"),
                      p_value=float("nan"), mc_draws=0, random_reduction_std=0.0)
        return result

    rng = np.random.default_rng(seed)
    reds = np.empty(n_mc, dtype=float)
    for i in range(n_mc):
        drop = rng.choice(n, size=k_drop, replace=False)
        keep = np.ones(n, dtype=bool)
        keep[drop] = False
        reds[i] = cvar_at(r_all[keep], k_tail) - base

    mean_rand = float(reds.mean())
    result["mean_random_reduction"] = mean_rand
    result["random_reduction_std"] = float(reds.std(ddof=1))
    result["efficiency"] = float(gate_red / mean_rand) if abs(mean_rand) > 1e-15 else float("inf")
    # one-sided: how often does a random drop do at least as well as the gate?
    result["p_value"] = float(np.mean(reds >= gate_red))
    result["mc_draws"] = n_mc
    result["random_reduction_p95"] = float(np.percentile(reds, 95))
    return result


# --------------------------------------------------------------- named vetoes
def build_veto(rows: List[Dict], spec: str) -> np.ndarray:
    """Translate a veto spec into a boolean drop mask over `rows`.

    Supported specs:
        <field><op><X>     threshold any numeric ledger field (vol_rank, stress,
                           gross_r) with one of >= <= > <. e.g. vol_rank>=0.88,
                           stress>=1.5. All three are knowable at entry, so a
                           veto built on them is tradable.
        strat==S1|T1       drop one sleeve
        regime==LABEL      drop trades in windows with that regime label
        worst_r>=X         drop trades already known to lose more than X R
                           (ORACLE / UPPER BOUND -- uses the outcome, so it is
                           NOT a tradable gate; it exists to calibrate what a
                           perfect forecaster would score)
    """
    op_map = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b,
              ">": lambda a, b: a > b, "<": lambda a, b: a < b}
    # Numeric ledger fields that a veto spec may threshold. `stress` is the causal
    # volatility-regime friction multiplier attached to the trade at entry, so a
    # `stress>=X` veto is knowable before the trade and is tradable.
    numeric_fields = ("vol_rank", "stress", "gross_r")
    m = np.zeros(len(rows), dtype=bool)
    for i, r in enumerate(rows):
        field = next((f for f in numeric_fields if spec.startswith(f)), None)
        if field is not None:
            rest = spec[len(field):]
            for op, fn in op_map.items():
                if rest.startswith(op):
                    thr = float(rest[len(op):])
                    val = r.get(field)
                    m[i] = (val is not None) and fn(float(val), thr)
                    break
        elif spec.startswith("strat=="):
            m[i] = r.get("strat") == spec.split("==", 1)[1]
        elif spec.startswith("regime=="):
            m[i] = r.get("regime_label") == spec.split("==", 1)[1]
        elif spec.startswith("worst_r>="):
            thr = float(spec.split(">=", 1)[1])
            m[i] = float(r.get("r_gain", 0.0)) <= -abs(thr)
        else:
            raise ValueError(f"unknown veto spec: {spec!r}")
    return m


# ------------------------------------------------------------------------ CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="CVaR99 gate harness")
    ap.add_argument("--ledger", required=True, help="ledger JSON from run_t1_oos.py --dump-ledger")
    ap.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    ap.add_argument("--mc", type=int, default=DEFAULT_MC)
    ap.add_argument("--widths", type=str, default="",
                    help="Comma-separated drop percentages for the vol_rank sweep, e.g. 0.1,0.5,1,2,5")
    ap.add_argument("--vetoes", type=str, default="",
                    help="Comma-separated veto specs, e.g. vol_rank>=0.88,strat==T1")
    ap.add_argument("--out-json", type=str, default=None)
    args = ap.parse_args(argv)

    data = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    rows = data["rows"]
    r_all = np.array([float(r["r_gain"]) for r in rows], dtype=float)
    pnl_all = np.array([float(r["pnl"]) for r in rows], dtype=float)
    n = len(rows)
    k_tail = tail_count_for(n, args.alpha)

    print("=" * 104)
    print(f"CVaR{args.alpha*100:.0f} GATE HARNESS   n={n:,d} trades   tail_count={k_tail}   "
          f"MC draws={args.mc:,d}")
    print("=" * 104)
    lo, hi = bootstrap_ci(r_all, k_tail)
    print(f"\nBASELINE (no gate)")
    print(f"  CVaR{args.alpha*100:.0f} on r_gain : {cvar_at(r_all, k_tail):+.5f} R   "
          f"(95% bootstrap CI {lo:+.5f} .. {hi:+.5f})")
    print(f"  CVaR{args.alpha*100:.0f} on USD pnl: {cvar_at(pnl_all, k_tail):+.2f} USD")
    print(f"  mean r_gain           : {r_all.mean():+.5f} R      "
          f"worst trade: {r_all.min():+.4f} R")
    print(f"  total pnl             : {pnl_all.sum():+,.2f} USD")
    print(f"\n  NOTE: a CVaR{args.alpha*100:.0f} tail on {n:,d} trades averages the worst "
          f"{k_tail} outcomes. That is a small sample;")
    print(f"        treat the third decimal place as noise.")

    report = {
        "n_trades": n, "alpha": args.alpha, "tail_count": k_tail,
        "baseline_cvar_r": cvar_at(r_all, k_tail),
        "baseline_ci": [lo, hi],
        "baseline_cvar_usd": cvar_at(pnl_all, k_tail),
        "total_pnl": float(pnl_all.sum()),
        "gates": [],
    }

    # ---- oracle upper bound: calibrates what a PERFECT forecaster would score
    print(f"\n{'-'*104}")
    print("CALIBRATION -- oracle gate (uses the realised outcome, NOT tradable)")
    print("-" * 104)
    oracle = build_veto(rows, "worst_r>=0.0")
    orc = evaluate_gate(r_all, oracle, args.alpha, args.mc)
    print(f"  drops the {orc['n_dropped']} trades that actually lost money "
          f"({orc['drop_pct']:.2f}%): efficiency {orc['efficiency']:.2f}x, "
          f"CVaR {orc['cvar_base']:+.5f} -> {orc['cvar_gated']:+.5f}")
    print("  ^ this is the ceiling. No causal gate can beat it.")
    report["oracle"] = orc

    # ---- requested vetoes
    for spec in [v.strip() for v in args.vetoes.split(",") if v.strip()]:
        mask = build_veto(rows, spec)
        res = evaluate_gate(r_all, mask, args.alpha, args.mc)
        res["spec"] = spec
        report["gates"].append(res)
        print(f"\n{'-'*104}")
        print(f"VETO  {spec}")
        print("-" * 104)
        print(f"  drops {res['n_dropped']:>5} trades ({res['drop_pct']:.2f}%)   "
              f"CVaR{args.alpha*100:.0f}: {res['cvar_base']:+.5f} -> {res['cvar_gated']:+.5f} R   "
              f"reduction {res['reduction']:+.5f}")
        print(f"  random equal-size control: mean reduction {res['mean_random_reduction']:+.5f} "
              f"(sd {res['random_reduction_std']:.5f}, p95 {res.get('random_reduction_p95', float('nan')):+.5f})")
        print(f"  EFFICIENCY  {res['efficiency']:.3f}x        p-value {res['p_value']:.4f}   "
              f"({'BEATS random' if res['p_value'] < 0.05 else 'NOT distinguishable from random'})")

    # ---- width sweep: vol_rank threshold chosen to hit target drop widths
    if args.widths:
        print(f"\n{'-'*104}")
        print("WIDTH SWEEP -- drop the highest-vol_rank trades at each target width")
        print("-" * 104)
        vr = np.array([float(r.get("vol_rank") or 0.0) for r in rows])
        order = np.argsort(-vr)  # highest vol_rank first
        print(f"  {'width':>7} {'k_drop':>7} {'thr':>7} {'CVaR gated':>11} {'reduction':>10} "
              f"{'efficiency':>11} {'p-value':>8}")
        for w in [float(x) for x in args.widths.split(",") if x.strip()]:
            k = max(1, int(round(n * w / 100.0)))
            mask = np.zeros(n, dtype=bool)
            mask[order[:k]] = True
            thr = float(vr[order[k - 1]])
            res = evaluate_gate(r_all, mask, args.alpha, args.mc)
            res["spec"] = f"top{w}pct_vol_rank"
            res["vol_rank_threshold"] = thr
            report["gates"].append(res)
            flag = "  <<" if res["p_value"] < 0.05 else ""
            print(f"  {w:>6.2f}% {res['n_dropped']:>7} {thr:>7.3f} {res['cvar_gated']:>+11.5f} "
                  f"{res['reduction']:>+10.5f} {res['efficiency']:>10.3f}x {res['p_value']:>8.4f}{flag}")

    if args.out_json:
        p = Path(args.out_json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(report, indent=2, default=float), encoding="utf-8")
        print(f"\n[Harness] report written to {p}")
    return report


if __name__ == "__main__":
    main()
