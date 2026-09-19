"""
Oracle Ceiling -- the hard upper bound on pass rate
====================================================

The question "can we pass all 20 windows?" has a definitive answer that does
not require any more searching.

Take every configuration in the search space. For each window, pick the
configuration that scores best ON THAT WINDOW -- using full hindsight, which is
maximally illegal. That is the ORACLE. No causal, honest, or lucky method can
ever beat it, because it already knows the answer to every question before
being asked.

If the oracle cannot reach 20/20, then 20/20 is unreachable within this search
space, and any reported 20/20 is necessarily produced by something outside it:
data leakage, altered criteria, or excluded windows.

This is the cheapest possible way to settle the goal, and it is the test that
should have been run before promising a 156-asset multiverse certification.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Engine.validation.adaptive_walkforward import (  # noqa: E402
    CAND_BASKETS, CAND_COST, CAND_QUANTILE, CAND_REGIME, CAND_RISK,
    CAND_TARGET_R, flat_risk_config,
)
from Engine.validation.honest_walkforward import (  # noqa: E402
    CRITERIA_PATH, WINDOWS_PATH, build_candidate_pool, load_universe,
    run_walkforward,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="reports/oracle_ceiling.json")
    args = ap.parse_args()

    with open(CRITERIA_PATH) as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)
    capital = criteria.get("initial_capital_usd", 5000.0)

    print("=" * 100)
    print("ORACLE CEILING -- best config per window chosen WITH FULL HINDSIGHT")
    print("This is an upper bound. No honest method can exceed it.")
    print("=" * 100)

    all_assets = load_universe()

    print("\nBuilding pools...")
    pools: Dict[Tuple, pd.DataFrame] = {}
    for cost, tr, rg in itertools.product(CAND_COST, CAND_TARGET_R, CAND_REGIME):
        assets = [a for a in all_assets if a.cost_frac <= cost]
        if not assets:
            continue
        pools[(cost, tr, rg)] = build_candidate_pool(
            assets, tr, 24, verbose=False, direction=-1,
            regime_veto=rg is not None,
            max_adx=rg[0] if rg else 35.0,
            max_hurst=rg[1] if rg else 0.58,
        )

    configs = [
        {"baskets": b, "target_r": tr, "quantile": q, "cost": c, "risk": rk, "regime": rg}
        for b, tr, q, c, rk, rg in itertools.product(
            CAND_BASKETS, CAND_TARGET_R, CAND_QUANTILE, CAND_COST, CAND_RISK, CAND_REGIME
        )
        if (c, tr, rg) in pools
    ]
    print(f"Configurations: {len(configs)}")

    best: Dict[int, dict] = {}
    for ci, c in enumerate(configs):
        cfg = flat_risk_config(capital, c["risk"])
        res, _ = run_walkforward(
            pools[(c["cost"], c["target_r"], c["regime"])], windows, cfg, criteria,
            baskets=list(c["baskets"]), threshold_quantile=c["quantile"],
            seed=42, verbose=False,
        )
        for r in res:
            if r.trades == 0:
                continue
            cal = r.net_roi / max(r.max_dd, 0.01)
            prev = best.get(r.window_id)
            # Rank by PASS first, then Calmar.
            key = (r.status == "PASS", cal)
            if prev is None or key > prev["key"]:
                best[r.window_id] = {
                    "key": key, "status": r.status, "roi": r.net_roi,
                    "dd": r.max_dd, "wr": r.win_rate, "n": r.trades,
                    "config": {k: (list(v) if isinstance(v, tuple) else v)
                               for k, v in c.items()},
                }
        if (ci + 1) % 40 == 0:
            print(f"  scored {ci + 1}/{len(configs)}")

    print("\n" + "-" * 100)
    print(f"{'W':<4} {'best achievable (hindsight)':<38} {'n':>5} {'WR%':>6} "
          f"{'ROI%':>8} {'DD%':>6} {'status':<7}")
    print("-" * 100)
    n_pass = 0
    for w in windows:
        wid = w["window_id"]
        b = best.get(wid)
        if b is None:
            print(f"W{wid:02d}  {'(no config produced trades)':<38}")
            continue
        if b["status"] == "PASS":
            n_pass += 1
        print(f"W{wid:02d}  {w['name'][:38]:<38} {b['n']:>5} {b['wr']:>6.1f} "
              f"{b['roi']:>+8.2f} {b['dd']:>6.2f} {b['status']:<7}")

    total = len([w for w in windows if w["window_id"] in best])
    print("-" * 100)
    print(f"\nORACLE PASS RATE: {n_pass}/{total}")
    print(f"Honest causal result for comparison: 9/15")

    if n_pass < len(windows):
        print(f"\n=> 20/20 is UNREACHABLE in this search space.")
        print(f"   Even with perfect hindsight the ceiling is {n_pass}/{total}.")
        print(f"   {len(windows) - n_pass} window(s) cannot be passed by ANY")
        print(f"   configuration searched, legal or otherwise.")
        fails = [wid for wid, b in best.items() if b["status"] != "PASS"]
        print(f"   Structurally unpassable windows: {sorted(fails)}")

    payload = {
        "n_configs": len(configs),
        "oracle_pass": n_pass,
        "oracle_total": total,
        "per_window": {str(k): {kk: vv for kk, vv in v.items() if kk != "key"}
                       for k, v in best.items()},
    }
    out = REPO_ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, default=float)
    print(f"\nWrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
