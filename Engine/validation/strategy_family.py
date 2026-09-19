"""
Multi-Strategy Book -- a family of sleeves run simultaneously
=============================================================

Every previous harness in this repo answers the question "which single
configuration should I run?" That framing is the problem. The oracle test
(`oracle_ceiling.py`) showed the per-window optimum jumps between 13 distinct
configs across 19 windows with no persistence, so *choosing* one is choosing
noise, and choosing it causally recovers only 9/15.

A multi-strategy firm does not choose. It runs several sleeves with genuinely
different alpha at once and lets diversification smooth the equity curve. That
is a structurally different — and strictly honest — proposition:

  * There is NO per-window selection step, so there is nothing to leak.
    The book is fixed in advance and applied unchanged to every window.
  * Because nothing is tuned on prior windows, there is no warm-up requirement.
    All 20 windows become evaluable instead of 15.
  * Sleeve weights are EQUAL and fixed. No optimisation of the blend.

The sleeves are deliberately built to fail at different times:

  S1 FADE-MR    direction=-1, admitted only when ADX/Hurst say mean-reverting.
                The historical book. Profits in chop, bleeds in trends (W13).
  S2 TREND-MOM  direction=+1, admitted only when ADX/Hurst say persistent.
                The missing alpha. Exists precisely to cover W13-type regimes.
  S3 FADE-WIDE  direction=-1, higher target R, ungated.
                Slower fade; different holding period to S1.
  S4 TREND-FAST direction=+1, lower target R, gated looser.
                Quicker momentum; decorrelated from S2 by horizon.

S1/S3 and S2/S4 take OPPOSITE sides gated on the SAME statistics with reversed
inequalities, which is what makes their return streams structurally
uncorrelated rather than merely differently-parameterised.

Critically the sleeves are merged into ONE book before simulation, so they
share a single capital base, the global concurrency cap and the per-cluster
cap. Summing four independently-simulated equity curves would silently quadruple
risk and violate the cluster governance; that would be a reporting artefact, not
diversification.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Engine.validation.honest_walkforward import (  # noqa: E402
    CRITERIA_PATH, FEATURES, PURGE_HOURS, WINDOWS_PATH, RiskConfig,
    WindowResult, build_candidate_pool, load_universe, simulate_portfolio,
    _fit_threshold_on_train,
)


# ----------------------------------------------------------------------------
# Sleeve definitions -- fixed in advance, never tuned per window
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Sleeve:
    name: str
    direction: int            # -1 fade, +1 momentum
    target_r: float
    quantile: float           # ML threshold quantile, fitted on train only
    cost_cap: float
    regime_veto: bool
    regime_mode: str          # "fade" | "trend"
    adx: float
    hurst: float
    baskets: Tuple[str, ...]
    max_hold: int = 24


DEFAULT_BOOK: Tuple[Sleeve, ...] = (
    Sleeve("S1_FADE_MR",    -1, 1.5, 0.92, 0.10, True,  "fade",  28.0, 0.54, ("Forex",)),
    Sleeve("S2_TREND_MOM",  +1, 2.0, 0.92, 0.10, True,  "trend", 25.0, 0.50, ("Forex", "CFD")),
    Sleeve("S3_FADE_WIDE",  -1, 2.5, 0.85, 0.05, False, "fade",  35.0, 0.58, ("Forex",)),
    Sleeve("S4_TREND_FAST", +1, 1.5, 0.85, 0.10, True,  "trend", 22.0, 0.48, ("Forex", "CFD")),
)


# ----------------------------------------------------------------------------
# Per-sleeve signal generation (model fit per window, train-only, as before)
# ----------------------------------------------------------------------------

def sleeve_signals(
    pool: pd.DataFrame,
    sleeve: Sleeve,
    start: int,
    end: int,
    seed: int,
) -> pd.DataFrame:
    """Return the signals this sleeve would fire in [start, end], or empty."""
    from sklearn.ensemble import HistGradientBoostingClassifier

    sub = pool[pool["basket"].isin(sleeve.baskets)]
    if len(sub) == 0:
        return pd.DataFrame()

    purge_s = PURGE_HOURS * 3600
    train = sub[sub["exit_time"] < (start - purge_s)]
    test = sub[(sub["time"] >= start) & (sub["time"] <= end)]
    if len(train) < 400 or len(test) == 0:
        return pd.DataFrame()

    X_tr = train[FEATURES].values
    y_tr = (train["r_mult"].values > 0).astype(int)
    if y_tr.sum() < 20 or (1 - y_tr).sum() < 20:
        return pd.DataFrame()

    model = HistGradientBoostingClassifier(
        max_iter=150, max_depth=4, learning_rate=0.06,
        min_samples_leaf=40, l2_regularization=1.0,
        early_stopping=False, random_state=seed,
    )
    model.fit(X_tr, y_tr)
    p_tr = model.predict_proba(X_tr)[:, 1]
    thresh = _fit_threshold_on_train(p_tr, y_tr, sleeve.quantile)

    p_te = model.predict_proba(test[FEATURES].values)[:, 1]
    sel = test.loc[p_te >= thresh].copy()
    if len(sel) == 0:
        return pd.DataFrame()
    sel["prob"] = p_te[p_te >= thresh]
    sel["sleeve"] = sleeve.name
    return sel


def build_pools(book: Sequence[Sleeve], verbose: bool = True) -> Dict[str, pd.DataFrame]:
    """One candidate pool per distinct (direction, target_r, cost, regime) key."""
    all_assets = load_universe()
    pools: Dict[str, pd.DataFrame] = {}
    for s in book:
        assets = [a for a in all_assets if a.cost_frac <= s.cost_cap]
        if not assets:
            pools[s.name] = pd.DataFrame()
            continue
        if verbose:
            print(f"  building {s.name:<14} dir={s.direction:+d} R{s.target_r} "
                  f"gate={s.regime_mode if s.regime_veto else 'none':<5} "
                  f"assets={len(assets)}")
        pools[s.name] = build_candidate_pool(
            assets, s.target_r, s.max_hold, verbose=False,
            direction=s.direction,
            regime_veto=s.regime_veto,
            max_adx=s.adx, max_hurst=s.hurst,
            regime_mode=s.regime_mode,
        )
    return pools


# ----------------------------------------------------------------------------
# The book: merge sleeves into ONE portfolio, then simulate once
# ----------------------------------------------------------------------------

def run_book(
    book: Sequence[Sleeve],
    pools: Dict[str, pd.DataFrame],
    windows: List[dict],
    cfg: RiskConfig,
    criteria: dict,
    seed: int = 42,
    verbose: bool = True,
) -> Tuple[List[WindowResult], pd.DataFrame, Dict[int, Dict[str, int]]]:
    min_roi = criteria["min_roi_percent"]
    max_dd_lim = criteria["max_dd_percent"]
    min_wr = criteria["min_winrate_percent"]
    min_trd = criteria["min_trades"]

    results: List[WindowResult] = []
    executed: List[pd.DataFrame] = []
    contrib: Dict[int, Dict[str, int]] = {}

    for w in windows:
        start = int(pd.Timestamp(w["start_date"], tz="UTC").timestamp())
        end = int(pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").timestamp())

        parts = []
        for s in book:
            pl = pools.get(s.name)
            if pl is None or len(pl) == 0:
                continue
            sig = sleeve_signals(pl, s, start, end, seed)
            if len(sig):
                parts.append(sig)

        if not parts:
            results.append(WindowResult(w["window_id"], w["name"], 0, 0, 0, 0, 0, 0, 0, "NO_DATA"))
            contrib[w["window_id"]] = {}
            continue

        # ONE merged book. Equal weight = every sleeve's signals enter the same
        # queue on equal terms; the shared caps then arbitrate between them.
        merged = pd.concat(parts, ignore_index=True).sort_values("time")
        merged = merged.reset_index(drop=True)

        stats = simulate_portfolio(merged, cfg)
        is_pass = (
            stats["net_roi"] >= min_roi
            and stats["max_dd"] <= max_dd_lim
            and stats["win_rate"] >= min_wr
            and stats["trades"] >= min_trd
        )
        status = "PASS" if is_pass else ("PROFIT" if stats["net_pnl"] > 0 else "FAIL")

        results.append(WindowResult(
            w["window_id"], w["name"], stats["trades"], stats["win_rate"],
            stats["net_pnl"], stats["net_roi"], stats["max_dd"],
            stats["rejected_concurrency"], stats["rejected_cluster"], status,
        ))
        contrib[w["window_id"]] = merged["sleeve"].value_counts().to_dict()
        executed.append(merged)

        if verbose:
            mix = " ".join(f"{k.split('_')[0]}:{v}"
                           for k, v in sorted(contrib[w["window_id"]].items()))
            print(f"  W{w['window_id']:02d} | {w['name'][:30]:<30} | "
                  f"n={stats['trades']:>4} | WR={stats['win_rate']:>5.1f}% | "
                  f"ROI={stats['net_roi']:>+8.2f}% | DD={stats['max_dd']:>5.2f}% | "
                  f"{status:<7} | {mix}")

    ex = pd.concat(executed, ignore_index=True) if executed else pd.DataFrame()
    return results, ex, contrib


def sleeve_correlation(
    book: Sequence[Sleeve],
    pools: Dict[str, pd.DataFrame],
    windows: List[dict],
    cfg: RiskConfig,
    criteria: dict,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Standalone per-sleeve window ROI, used to verify the sleeves are actually
    decorrelated. If this matrix is all +0.9 the 'family' is one strategy in
    four costumes and the diversification claim is false.
    """
    rows: Dict[str, Dict[int, float]] = {s.name: {} for s in book}
    for s in book:
        pl = pools.get(s.name)
        if pl is None or len(pl) == 0:
            continue
        for w in windows:
            start = int(pd.Timestamp(w["start_date"], tz="UTC").timestamp())
            end = int(pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").timestamp())
            sig = sleeve_signals(pl, s, start, end, seed)
            if len(sig) == 0:
                rows[s.name][w["window_id"]] = 0.0
                continue
            st = simulate_portfolio(sig.sort_values("time"), cfg)
            rows[s.name][w["window_id"]] = st["net_roi"]
    return pd.DataFrame(rows)


def admit_sleeves_causally(
    book: Sequence[Sleeve],
    pools: Dict[str, pd.DataFrame],
    cutoff_ts: int,
    cfg: RiskConfig,
    seed: int = 42,
    verbose: bool = True,
) -> List[Sleeve]:
    """
    Decide which sleeves get capital using ONLY data strictly before the first
    OOS window. A sleeve must show positive expectancy in-sample to be funded.

    This is the honest analogue of a firm's capital-allocation committee: you do
    not fund a book because it decorrelates, you fund it because it makes money
    AND it decorrelates. Because the cutoff predates W01, the decision is
    identical for every window and leaks nothing -- so all 20 windows stay
    evaluable, unlike a trailing-window allocator which would burn a warm-up.
    """
    admitted: List[Sleeve] = []
    if verbose:
        print("\n  Sleeve admission (in-sample, strictly pre-W01, ML-gated):")
        print("    NOTE raw expectancy is negative for every sleeve -- round-trip")
        print("    cost exceeds the raw signal. The ML gate is the edge, so the")
        print("    admission test must be run on GATED signals, not raw labels.")
    for s in book:
        pl = pools.get(s.name)
        if pl is None or len(pl) == 0:
            continue
        hist = pl[pl["exit_time"] < cutoff_ts]
        if len(hist) < 2000:
            if verbose:
                print(f"    {s.name:<14} REJECT  insufficient pre-window history")
            continue
        # Split the pre-window era: fit on the first 70%, validate on the last
        # 30%. Both lie strictly before W01, so nothing from any scored window
        # informs the funding decision.
        cut = hist["time"].quantile(0.70)
        tr = hist[hist["exit_time"] < cut]
        va = hist[hist["time"] >= cut]
        if len(tr) < 400 or len(va) < 100:
            if verbose:
                print(f"    {s.name:<14} REJECT  split too small")
            continue
        y_tr = (tr["r_mult"].values > 0).astype(int)
        if y_tr.sum() < 20 or (1 - y_tr).sum() < 20:
            if verbose:
                print(f"    {s.name:<14} REJECT  degenerate labels")
            continue
        from sklearn.ensemble import HistGradientBoostingClassifier
        mdl = HistGradientBoostingClassifier(
            max_iter=150, max_depth=4, learning_rate=0.06,
            min_samples_leaf=40, l2_regularization=1.0,
            early_stopping=False, random_state=seed,
        )
        mdl.fit(tr[FEATURES].values, y_tr)
        p_tr = mdl.predict_proba(tr[FEATURES].values)[:, 1]
        th = _fit_threshold_on_train(p_tr, y_tr, s.quantile)
        p_va = mdl.predict_proba(va[FEATURES].values)[:, 1]
        sel = va.loc[p_va >= th]
        if len(sel) < 30:
            if verbose:
                print(f"    {s.name:<14} REJECT  only {len(sel)} gated signals")
            continue
        r = sel["r_mult"].values
        exp_r = float(np.mean(r))
        t_stat = exp_r / (np.std(r) / np.sqrt(len(r))) if np.std(r) > 0 else 0.0
        ok = exp_r > 0 and t_stat > 1.5
        if verbose:
            print(f"    {s.name:<14} {'ADMIT ' if ok else 'REJECT'}  "
                  f"gated n={len(sel):>6,}  E[R]={exp_r:+.4f}  t={t_stat:+.2f}")
        if ok:
            admitted.append(s)
    return admitted


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="reports/strategy_family.json")
    ap.add_argument("--base-risk", type=float, default=25.0)
    ap.add_argument("--max-concurrent", type=int, default=3)
    ap.add_argument("--max-per-cluster", type=int, default=1)
    ap.add_argument("--corr", action="store_true",
                    help="also compute the standalone sleeve correlation matrix")
    ap.add_argument("--causal-admit", action="store_true",
                    help="fund only sleeves with positive pre-W01 expectancy")
    ap.add_argument("--split-risk", action="store_true",
                    help="divide base risk across funded sleeves (constant gross)")
    args = ap.parse_args()

    with open(CRITERIA_PATH) as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)
    capital = criteria.get("initial_capital_usd", 5000.0)

    cfg = RiskConfig(
        capital=capital,
        base_risk=args.base_risk, tier1_risk=args.base_risk,
        tier2_risk=args.base_risk, tier3_risk=args.base_risk,
        max_concurrent=args.max_concurrent,
        max_per_cluster=args.max_per_cluster,
    )

    print("=" * 108)
    print("MULTI-STRATEGY BOOK -- fixed sleeves, equal weight, one shared risk budget")
    print("No per-window selection => nothing to leak => all 20 windows evaluable")
    print("=" * 108)
    for s in DEFAULT_BOOK:
        print(f"  {s.name:<14} dir={s.direction:+d} R{s.target_r} q{s.quantile} "
              f"cost<={s.cost_cap} gate={s.regime_mode if s.regime_veto else 'none':<5} "
              f"({s.adx},{s.hurst}) baskets={'+'.join(s.baskets)}")

    print("\nBuilding candidate pools...")
    pools = build_pools(DEFAULT_BOOK)
    for k, v in pools.items():
        print(f"    {k:<14} {len(v):>8,} candidates")

    book = list(DEFAULT_BOOK)
    if args.causal_admit:
        cutoff = int(pd.Timestamp(windows[0]["start_date"], tz="UTC").timestamp())
        book = admit_sleeves_causally(DEFAULT_BOOK, pools, cutoff, cfg)
        print(f"\n  Funded {len(book)}/{len(DEFAULT_BOOK)} sleeves: "
              f"{', '.join(s.name for s in book)}")
    if args.split_risk and book:
        per = args.base_risk / len(book)
        cfg = RiskConfig(
            capital=capital, base_risk=per, tier1_risk=per,
            tier2_risk=per, tier3_risk=per,
            max_concurrent=args.max_concurrent,
            max_per_cluster=args.max_per_cluster,
        )
        print(f"  Risk split across {len(book)} sleeves: {per:.2f} USD each "
              f"(gross unchanged at {args.base_risk:.2f})")

    print("\nRunning the book:")
    results, executed, contrib = run_book(
        book, pools, windows, cfg, criteria, verbose=True,
    )

    live = [r for r in results if r.status != "NO_DATA"]
    n_pass = sum(1 for r in live if r.status == "PASS")
    n_prof = sum(1 for r in live if r.net_pnl > 0)
    total = sum(r.net_pnl for r in live)
    print("\n" + "=" * 108)
    print(f"PASS {n_pass}/{len(live)}   profitable {n_prof}/{len(live)}   "
          f"trades {sum(r.trades for r in live):,}   "
          f"net {total:+,.2f} USD ({total / capital * 100:+.2f}%)")
    if live:
        cal = [r.net_roi / max(r.max_dd, 0.01) for r in live]
        print(f"median per-window Calmar {np.median(cal):.2f}   "
              f"worst DD {max(r.max_dd for r in live):.2f}%")

    payload = {
        "book": [s.__dict__ for s in book],
        "risk": cfg.__dict__,
        "pass": n_pass, "evaluated": len(live), "profitable": n_prof,
        "net_pnl": total, "net_roi_pct": total / capital * 100.0,
        "scorecard": [r.__dict__ for r in results],
        "sleeve_mix": {str(k): v for k, v in contrib.items()},
    }

    if args.corr:
        print("\nStandalone sleeve ROI per window (diversification check):")
        m = sleeve_correlation(DEFAULT_BOOK, pools, windows, cfg, criteria)
        print(m.round(2).to_string())
        c = m.corr()
        print("\nSleeve correlation matrix:")
        print(c.round(3).to_string())
        payload["sleeve_roi"] = m.to_dict()
        payload["sleeve_corr"] = c.to_dict()

    out = REPO_ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, default=float)
    print(f"\nWrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
