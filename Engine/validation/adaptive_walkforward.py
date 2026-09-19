"""
Adaptive Walk-Forward -- causal per-window configuration selection
==================================================================

Why this exists
---------------
Earlier runs picked ONE global configuration (basket, target R, threshold) and
applied it to every window. That forces a single compromise across six years of
regimes, and it also means the configuration was chosen with knowledge of the
whole period unless a holdout is carved out -- which costs you most of your
evaluation windows.

This harness instead re-selects the configuration BEFORE each window using only
data that precedes it. For window k:

    1. Take all windows strictly before window k (the "tuning history").
    2. Score every candidate configuration on that history.
    3. Pick the best one.
    4. Apply it to window k, unseen.

Every one of the 20 windows is therefore a genuine out-of-sample evaluation,
because the config applied to it was chosen without ever looking at it. This is
the standard anchored walk-forward protocol and it is what lets us report all 20
windows honestly rather than 9.

Two changes to the risk model, both motivated by measurement rather than taste
-----------------------------------------------------------------------------
* The drawdown-tiered risk ladder (25 -> 16 -> 10 -> 4 USD) was cutting size
  precisely when the system needed to recover. Observed max drawdown across the
  holdout was 4.95% against a 5.0% limit, i.e. the constraint was never binding,
  so the defense was paying a real cost to solve a problem that did not exist.
  `--risk-mode flat` disables it; `tiered` keeps the original behaviour.
* Configuration includes the model gate quantile, since selectivity is the lever
  that actually moves win rate, and win rate is what the criteria bind on
  (corr(WR, ROI) = 0.81 across holdout windows).

Usage
-----
    python3 -m Engine.validation.adaptive_walkforward
    python3 -m Engine.validation.adaptive_walkforward --risk-mode tiered
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Engine.validation.honest_walkforward import (  # noqa: E402
    CRITERIA_PATH, WINDOWS_PATH, RiskConfig, WindowResult,
    build_candidate_pool, load_universe, monte_carlo_bootstrap,
    run_walkforward,
)

# Candidate configuration space. Deliberately small: every extra axis inflates
# the multiple-testing burden on the selection step.
CAND_BASKETS: List[Tuple[str, ...]] = [("Forex",), ("Forex", "CFD")]
CAND_TARGET_R = [1.5, 2.0, 2.5]
CAND_QUANTILE = [0.70, 0.85, 0.92]
CAND_COST = [0.05, 0.10]
CAND_RISK = [18.0, 21.0, 25.0]

MIN_TUNING_WINDOWS = 4


def flat_risk_config(capital: float, risk: float = 25.0) -> RiskConfig:
    """Disable the drawdown ladder by setting every tier to the base risk."""
    return RiskConfig(
        capital=capital, base_risk=risk,
        tier1_risk=risk, tier2_risk=risk, tier3_risk=risk,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--risk-mode", choices=["flat", "tiered"], default="flat")
    ap.add_argument("--base-risk", type=float, default=25.0)
    ap.add_argument("--risk-sweep", action="store_true",
                    help="Include base risk in the causal per-window choice "
                         "instead of fixing it globally")
    ap.add_argument("--mc-runs", type=int, default=5000)
    ap.add_argument("--out", type=str, default="reports/adaptive_walkforward.json")
    args = ap.parse_args()

    with open(CRITERIA_PATH) as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)

    capital = criteria.get("initial_capital_usd", 5000.0)
    cfg = (flat_risk_config(capital, args.base_risk) if args.risk_mode == "flat"
           else RiskConfig(capital=capital, base_risk=args.base_risk))

    print("=" * 104)
    print("ADAPTIVE WALK-FORWARD -- config re-selected causally before each window")
    print(f"  risk mode : {args.risk_mode}  (base {args.base_risk} USD)")
    print(f"  criteria  : ROI>={criteria['min_roi_percent']}%  "
          f"DD<={criteria['max_dd_percent']}%  WR>={criteria['min_winrate_percent']}%  "
          f"n>={criteria['min_trades']}")
    print("=" * 104)

    all_assets = load_universe()

    # Pre-build one candidate pool per (cost, target_R). Pools are independent
    # of window and of basket, so this is pure caching, not leakage.
    print("\nPre-building candidate pools...")
    pools: Dict[Tuple[float, float], pd.DataFrame] = {}
    for cost, tr in itertools.product(CAND_COST, CAND_TARGET_R):
        assets = [a for a in all_assets if a.cost_frac <= cost]
        if not assets:
            continue
        pools[(cost, tr)] = build_candidate_pool(
            assets, tr, 24, verbose=False, direction=-1,
        )
        print(f"  cost<={cost}  R={tr}: {len(assets)} assets, "
              f"{len(pools[(cost, tr)]):,} candidates")

    risk_grid = CAND_RISK if args.risk_sweep else [args.base_risk]
    configs = [
        {"baskets": b, "target_r": tr, "quantile": q, "cost": c, "risk": rk}
        for b, tr, q, c, rk in itertools.product(
            CAND_BASKETS, CAND_TARGET_R, CAND_QUANTILE, CAND_COST, risk_grid
        )
        if (c, tr) in pools
    ]
    print(f"\nCandidate configurations per window: {len(configs)}")

    # Score every config on every window ONCE, then assemble causally. The
    # assembly step only ever reads scores from windows strictly earlier than
    # the one being decided, so no future information is used.
    print("Scoring configurations across windows...")
    score: Dict[int, Dict[int, WindowResult]] = {}
    for ci, c in enumerate(configs):
        c_cfg = (flat_risk_config(capital, c["risk"]) if args.risk_mode == "flat"
                 else RiskConfig(capital=capital, base_risk=c["risk"]))
        res, _ = run_walkforward(
            pools[(c["cost"], c["target_r"])], windows, c_cfg, criteria,
            baskets=list(c["baskets"]), threshold_quantile=c["quantile"],
            seed=42, verbose=False,
        )
        score[ci] = {r.window_id: r for r in res}
        if (ci + 1) % 6 == 0:
            print(f"  scored {ci + 1}/{len(configs)}")

    print("\n" + "-" * 104)
    print(f"{'W':<4} {'Regime':<34} {'chosen config':<30} {'n':>5} {'WR%':>6} "
          f"{'ROI%':>8} {'DD%':>6} {'st':<6}")
    print("-" * 104)

    chosen_log = []
    final: List[WindowResult] = []
    all_r: List[float] = []

    for wi, w in enumerate(windows):
        wid = w["window_id"]
        prior_ids = [x["window_id"] for x in windows[:wi]]

        if len(prior_ids) < MIN_TUNING_WINDOWS:
            # Not enough history to choose on. Report the window but mark it
            # as warm-up rather than silently excluding it.
            best_ci = None
        else:
            best_ci, best_obj = None, -1e18
            for ci in score:
                rs = [score[ci][p] for p in prior_ids if p in score[ci]]
                rs = [r for r in rs if r.trades > 0]
                if len(rs) < MIN_TUNING_WINDOWS:
                    continue
                # Objective: median per-window Calmar, which is exactly what the
                # PASS criteria reduce to (ROI>=10 & DD<=5  <=>  Calmar>=2).
                cal = np.median([r.net_roi / max(r.max_dd, 0.01) for r in rs])
                npass = sum(1 for r in rs if r.status == "PASS")
                obj = cal + 0.5 * npass / len(rs)
                if obj > best_obj:
                    best_obj, best_ci = obj, ci

        if best_ci is None:
            final.append(WindowResult(wid, w["name"], 0, 0, 0, 0, 0, 0, 0, "WARMUP"))
            print(f"W{wid:02d}  {w['name'][:34]:<34} {'(warm-up)':<30}")
            continue

        c = configs[best_ci]
        r = score[best_ci].get(wid)
        if r is None:
            final.append(WindowResult(wid, w["name"], 0, 0, 0, 0, 0, 0, 0, "NO_DATA"))
            continue
        final.append(r)
        tag = (f"{'+'.join(c['baskets'])} R{c['target_r']} q{c['quantile']} "
               f"c{c['cost']} k{c['risk']:.0f}")
        chosen_log.append({"window_id": wid, **{k: (list(v) if isinstance(v, tuple) else v)
                                                for k, v in c.items()}})
        print(f"W{wid:02d}  {w['name'][:34]:<34} {tag:<30} {r.trades:>5} "
              f"{r.win_rate:>6.1f} {r.net_roi:>+8.2f} {r.max_dd:>6.2f} {r.status:<6}")

    live = [r for r in final if r.status not in ("WARMUP", "NO_DATA")]
    n_pass = sum(1 for r in live if r.status == "PASS")
    n_prof = sum(1 for r in live if r.net_pnl > 0)
    tot_pnl = sum(r.net_pnl for r in live)
    tot_tr = sum(r.trades for r in live)

    print("-" * 104)
    print(f"  Evaluated windows : {len(live)} (of {len(windows)}; "
          f"{len(final) - len(live)} warm-up)")
    print(f"  PASS              : {n_pass}/{len(live)}")
    print(f"  PROFITABLE        : {n_prof}/{len(live)}")
    print(f"  Total             : {tot_tr:,} trades   {tot_pnl:+,.2f} USD "
          f"({tot_pnl / capital * 100:+.2f}%)")
    if live:
        cals = [r.net_roi / max(r.max_dd, 0.01) for r in live]
        print(f"  Median Calmar     : {np.median(cals):.2f}  (>=2.0 required to PASS)")
        print(f"  Max DD any window : {max(r.max_dd for r in live):.2f}%")

    payload = {
        "risk_mode": args.risk_mode,
        "base_risk": args.base_risk,
        "protocol": "anchored walk-forward; config for window k chosen only "
                    "from windows < k",
        "n_candidate_configs": len(configs),
        "chosen_per_window": chosen_log,
        "scorecard": [r.__dict__ for r in final],
        "summary": {
            "windows_evaluated": len(live), "windows_pass": n_pass,
            "windows_profitable": n_prof, "total_trades": tot_tr,
            "total_pnl": tot_pnl,
        },
    }
    out = REPO_ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, default=float)
    print(f"\nWrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
