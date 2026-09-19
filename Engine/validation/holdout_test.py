"""
Strict Holdout Test -- guarding against the auditor's own selection bias
========================================================================

Why this file exists
--------------------
The edge scan and the walk-forward runs above explored a configuration space:
4 event types x 5 target-R x 3 horizons, then a cost filter, then a basket
subset. That is >100 looks at the same data. Reporting the best cell from that
search as a result would reproduce precisely the overfitting the Ox_Alpha_43
audit rejected -- just with better paperwork.

So the selection is quarantined in time:

    SELECTION  era  : 2020-09 .. 2024-12-31   -- everything may be tuned here
    HOLDOUT    era  : 2025-01-01 .. present   -- touched exactly ONCE, at the end

The holdout is evaluated a single time, after the configuration is frozen and
written to disk. Whatever it prints is the reported number. No iteration on it.

Multiple-testing control
------------------------
Deflated Sharpe / Bonferroni style: with N configurations searched, the
significance bar for the selected one is raised accordingly, and the expected
number of false positives at the chosen bar is stated explicitly.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Engine.validation.honest_walkforward import (  # noqa: E402
    CRITERIA_PATH, WINDOWS_PATH, RiskConfig, build_candidate_pool,
    load_universe, monte_carlo_bootstrap, run_walkforward,
)

SELECTION_END = "2024-12-31"
HOLDOUT_START = "2025-01-01"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cost-frac", type=float, default=0.05)
    ap.add_argument("--target-r", type=float, default=2.0)
    ap.add_argument("--hold-bars", type=int, default=24)
    ap.add_argument("--direction", type=int, default=-1)
    ap.add_argument("--mc-runs", type=int, default=5000)
    ap.add_argument("--n-configs-searched", type=int, default=60,
                    help="Configurations explored during selection, for the "
                         "multiple-testing correction")
    ap.add_argument("--out", type=str, default="reports/holdout_test.json")
    args = ap.parse_args()

    print("=" * 96)
    print("STRICT HOLDOUT TEST")
    print(f"  selection era : .. {SELECTION_END}   (tuning allowed)")
    print(f"  holdout era   : {HOLDOUT_START} ..   (evaluated once)")
    print("=" * 96)

    with open(CRITERIA_PATH) as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)

    cfg = RiskConfig(capital=criteria.get("initial_capital_usd", 5000.0))

    assets = load_universe()
    assets = [a for a in assets if a.cost_frac <= args.max_cost_frac]
    print(f"\nAssets after cost filter (<= {args.max_cost_frac} R): {len(assets)}")

    pool = build_candidate_pool(
        assets, args.target_r, args.hold_bars,
        verbose=False, direction=args.direction,
    )
    print(f"Candidates: {len(pool):,}")

    sel_cut = int(pd.Timestamp(SELECTION_END, tz="UTC").timestamp())
    hold_windows = [
        w for w in windows
        if pd.Timestamp(w["start_date"], tz="UTC") >= pd.Timestamp(HOLDOUT_START, tz="UTC")
    ]
    sel_windows = [
        w for w in windows
        if pd.Timestamp(w["start_date"], tz="UTC") < pd.Timestamp(HOLDOUT_START, tz="UTC")
    ]
    print(f"Selection windows: {len(sel_windows)}   Holdout windows: {len(hold_windows)}")

    variants = {
        "Full Multiverse": None,
        "Forex only": ["Forex"],
        "Crypto only": ["Crypto"],
        "CFD only": ["CFD"],
        "Forex + CFD": ["Forex", "CFD"],
    }

    print("\n--- SELECTION ERA (tuning permitted) ---")
    sel_scores: Dict[str, float] = {}
    for label, bl in variants.items():
        res, ex = run_walkforward(
            pool, sel_windows, cfg, criteria, baskets=bl,
            seed=42, verbose=False,
        )
        pnl = sum(r.net_pnl for r in res)
        tr = sum(r.trades for r in res)
        exp_r = float(ex["r_mult"].mean()) if len(ex) else 0.0
        sel_scores[label] = pnl
        print(f"  {label:<18} trades={tr:>5}  PnL={pnl:>+10,.2f}  exp={exp_r:+.4f} R")

    best = max(sel_scores, key=sel_scores.get)
    print(f"\nSELECTED on selection era: '{best}'  (PnL {sel_scores[best]:+,.2f})")
    print("Configuration is now FROZEN. Evaluating holdout once.")

    print("\n--- HOLDOUT ERA (single evaluation) ---")
    res, ex = run_walkforward(
        pool, hold_windows, cfg, criteria, baskets=variants[best],
        seed=42, verbose=True,
    )
    tr = sum(r.trades for r in res)
    pnl = sum(r.net_pnl for r in res)
    n_pass = sum(1 for r in res if r.status == "PASS")
    n_prof = sum(1 for r in res if r.net_pnl > 0)
    exp_r = float(ex["r_mult"].mean()) if len(ex) else 0.0
    se = float(ex["r_mult"].std(ddof=1) / np.sqrt(len(ex))) if len(ex) > 1 else 0.0
    t_stat = exp_r / se if se > 0 else 0.0

    print("-" * 96)
    print(f"  Holdout trades     : {tr:,}")
    print(f"  Holdout PnL        : {pnl:+,.2f} USD  ({pnl / cfg.capital * 100:+.2f}%)")
    print(f"  Holdout expectancy : {exp_r:+.4f} R/trade   t = {t_stat:+.2f}")
    print(f"  Windows PASS/PROFIT: {n_pass}/{len(res)}  |  {n_prof}/{len(res)}")

    # Multiple-testing correction.
    n_searched = args.n_configs_searched + len(variants)
    bar = float(np.abs(np.percentile(np.random.default_rng(0).standard_normal(200000), 100 * (1 - 0.05 / n_searched))))
    print(f"\n  Multiple testing: {n_searched} configurations searched")
    print(f"  Bonferroni t-bar at alpha=0.05 : {bar:.2f}")
    print(f"  Observed holdout t             : {t_stat:+.2f}  -> "
          f"{'SURVIVES' if t_stat > bar else 'DOES NOT SURVIVE'}")

    mc = monte_carlo_bootstrap(ex["r_mult"].values, cfg, n_runs=args.mc_runs, seed=42) if len(ex) else {}
    if mc:
        print(f"\n  Bootstrap ({args.mc_runs:,} runs) on holdout trades:")
        print(f"    ROI p05/p50/p95 : {mc['roi_p05']:+.2f}% / {mc['roi_p50']:+.2f}% / {mc['roi_p95']:+.2f}%")
        print(f"    MaxDD p95/p99   : {mc['dd_p95']:.2f}% / {mc['dd_p99']:.2f}%")
        print(f"    P(net loss)     : {mc['prob_loss']:.2f}%")

    payload = {
        "selection_era_end": SELECTION_END,
        "holdout_era_start": HOLDOUT_START,
        "config": vars(args),
        "selection_scores": sel_scores,
        "selected_variant": best,
        "holdout": {
            "trades": tr, "net_pnl": pnl,
            "net_roi_pct": pnl / cfg.capital * 100,
            "expectancy_r": exp_r, "t_stat": t_stat,
            "windows_pass": n_pass, "windows_profitable": n_prof,
            "windows_total": len(res),
            "scorecard": [r.__dict__ for r in res],
        },
        "multiple_testing": {
            "n_configs_searched": n_searched,
            "bonferroni_t_bar": bar,
            "survives": bool(t_stat > bar),
        },
        "monte_carlo": mc,
    }
    out = REPO_ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, default=float)
    print(f"\nWrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
