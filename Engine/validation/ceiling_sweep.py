"""
Ceiling Sweep -- what is the best achievable pass rate, honestly?
=================================================================

The stated goal is 20/20 OOS windows under Engine/target_oos_criteria.json
(ROI >= +10%, MaxDD <= 5%, WR >= 40%, trades >= 15).

The binding constraint is not ROI or drawdown separately -- it is their ratio.
Requiring ROI >= +10% AND MaxDD <= 5% in the same window is equivalent to
requiring a per-window Calmar of >= 2.0. Calmar is approximately invariant to
risk scaling: doubling risk per trade roughly doubles both the numerator and
the denominator. So position sizing cannot buy a pass. Only a better signal can.

This sweep searches the honest lever space on the SELECTION ERA ONLY
(<= 2024-12-31) and reports the resulting pass rate and Calmar distribution.
The 2025+ holdout has already been consumed once by holdout_test.py; re-running
a sweep against it and reporting the winner would be p-hacking, so it is
deliberately not touched here.

Levers searched:
  * threshold quantile  -- selectivity of the model gate
  * max cost fraction   -- excludes instruments where cost exceeds the edge
  * target R            -- payoff geometry
  * basket subset       -- Forex / CFD / combinations
"""

from __future__ import annotations

import argparse
import itertools
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
    load_universe, run_walkforward,
)

SELECTION_END = "2025-01-01"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="reports/ceiling_sweep.json")
    args = ap.parse_args()

    with open(CRITERIA_PATH) as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)

    sel_windows = [
        w for w in windows
        if pd.Timestamp(w["start_date"], tz="UTC") < pd.Timestamp(SELECTION_END, tz="UTC")
    ]
    cfg = RiskConfig(capital=criteria.get("initial_capital_usd", 5000.0))

    print("=" * 100)
    print("CEILING SWEEP -- selection era only (<= 2024-12-31)")
    print(f"Criteria: ROI>={criteria['min_roi_percent']}%  DD<={criteria['max_dd_percent']}%  "
          f"WR>={criteria['min_winrate_percent']}%  n>={criteria['min_trades']}")
    print("Equivalent requirement: per-window Calmar >= "
          f"{criteria['min_roi_percent'] / criteria['max_dd_percent']:.1f}")
    print("=" * 100)

    all_assets = load_universe()
    rows = []

    grid = list(itertools.product(
        [0.03, 0.05, 0.10],          # max cost frac
        [1.5, 2.0, 2.5],             # target R
        [0.70, 0.85, 0.92],          # threshold quantile
        [("Forex",), ("Forex", "CFD"), ("CFD",)],
    ))
    print(f"\nConfigurations: {len(grid)}\n")
    print(f"{'cost':>6} {'R':>4} {'q':>5} {'baskets':<14} {'n':>6} {'PASS':>6} "
          f"{'PnL':>11} {'medCal':>7}")
    print("-" * 100)

    pool_cache: Dict[tuple, pd.DataFrame] = {}

    for max_cost, target_r, q, baskets in grid:
        key = (max_cost, target_r)
        if key not in pool_cache:
            assets = [a for a in all_assets if a.cost_frac <= max_cost]
            if not assets:
                pool_cache[key] = pd.DataFrame()
            else:
                pool_cache[key] = build_candidate_pool(
                    assets, target_r, 24, verbose=False, direction=-1,
                )
        pool = pool_cache[key]
        if pool.empty:
            continue

        res, ex = run_walkforward(
            pool, sel_windows, cfg, criteria, baskets=list(baskets),
            threshold_quantile=q, seed=42, verbose=False,
        )
        live = [r for r in res if r.trades > 0]
        if not live:
            continue
        n_pass = sum(1 for r in res if r.status == "PASS")
        pnl = sum(r.net_pnl for r in res)
        cals = [r.net_roi / max(r.max_dd, 0.01) for r in live]
        med_cal = float(np.median(cals))
        rows.append({
            "max_cost": max_cost, "target_r": target_r, "quantile": q,
            "baskets": list(baskets), "windows": len(live),
            "passes": n_pass, "pass_rate": n_pass / len(live),
            "net_pnl": pnl, "median_calmar": med_cal,
            "windows_calmar_ge_2": sum(1 for c in cals if c >= 2.0),
        })
        print(f"{max_cost:>6.2f} {target_r:>4.1f} {q:>5.2f} {'+'.join(baskets):<14} "
              f"{len(live):>6} {n_pass:>6} {pnl:>+11,.0f} {med_cal:>7.2f}")

    df = pd.DataFrame(rows).sort_values("passes", ascending=False)
    print("-" * 100)
    if df.empty:
        print("No configuration produced trades.")
        return

    best = df.iloc[0]
    print(f"\nBEST pass rate on selection era: {int(best['passes'])}/{int(best['windows'])} "
          f"({best['pass_rate'] * 100:.0f}%)")
    print(f"  config: cost<={best['max_cost']} R={best['target_r']} q={best['quantile']} "
          f"baskets={best['baskets']}")
    print(f"  median per-window Calmar: {best['median_calmar']:.2f}  (need >= 2.0 to pass)")
    print(f"\nConfigurations reaching 100% pass rate: "
          f"{int((df['pass_rate'] >= 1.0).sum())}/{len(df)}")

    out = REPO_ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({"selection_end": SELECTION_END, "results": df.to_dict("records")},
                  f, indent=2, default=float)
    print(f"\nWrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
