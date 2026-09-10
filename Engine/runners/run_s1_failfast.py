#!/usr/bin/env python3
"""
================================================================================
S1 FAIL-FAST CAUSAL WALK-FORWARD HARNESS (mission Section 4.5)
================================================================================
Protocol:
  1. Evaluate Window 1 with the current configuration.
  2. If it passes every criterion -> freeze its result, proceed.
  3. If it fails -> halt; re-optimize causally using ONLY data strictly prior
     to the failing window's start (with a 72h embargo — the purge invariant);
     the search space is a PREDEFINED grid, fixed forever (no window-keyed
     parameters, no bespoke per-window tuning).
  4. Candidate configs are ranked by a trailing-period objective that mirrors
     the mission criteria (quarter-score composite). The top candidates must
     additionally show ZERO REGRESSION on all previously passed windows
     (re-evaluated; must still pass) before adoption.
  5. Resume at the failing window with the adopted config. Record the config
     timeline. Repeat to Window 20.

Everything the optimizer touches is strictly prior data. The final scorecard
is the true sequential outcome of this protocol.
================================================================================
"""
import argparse
import itertools
import json
import os
import sys
import time
from dataclasses import replace

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Engine"))
import numpy as np

from s1_trend_following_suite import (TrendParams, FrictionConfig, RiskConfig,
                                      load_symbols, evaluate_window, OOS_WINDOWS,
                                      system_statistics)

# ---------------------------------------------------------------------------
# Predefined causal search grid (FIXED FOREVER — identical for every re-opt)
# ---------------------------------------------------------------------------
# ratchet variants: (arm0, lock0, arm1, lock1, trail_start)
RATCHET_VARIANTS = [
    (0.90, 0.25, 1.90, 1.05, 2.60),   # mission Section 5.3 specification
    (1.40, 0.60, 2.40, 1.40, 2.60),   # slow-ratchet runner (lets winners breathe)
]

GRID = [dict(stop_k_atr=sk, trail_atr_mult=tr, t1_donch_bars=db, er_min=er,
             short_anchor_800=sa, max_concurrent=mc, ratchet=rv,
             time_decay_4h=td, max_hold_4h=mh)
        for sk in (2.0, 2.4, 2.8)
        for tr in (4.0, 5.0)
        for db in (48, 96)
        for er in (0.0, 0.10)
        for sa in (True,)
        for mc in (2, 3)
        for rv in RATCHET_VARIANTS
        for td in (24, 36)
        for mh in (60, 90)]

BASE_P = TrendParams()
BASE_R = RiskConfig()
FRIC = FrictionConfig()

# fork-shared state for multiprocessing scoring (Linux COW; no pickling)
_SDS = None
_WORKER_TSTART = None


def _score_worker(g):
    p, r = make_config(g)
    obj, _ = trailing_objective(_SDS, p, r, _WORKER_TSTART)
    return obj, g


def make_config(g: dict):
    a0, l0, a1, l1, ts = g["ratchet"]
    p = replace(BASE_P, stop_k_atr_t1=g["stop_k_atr"], stop_k_atr_t2=g["stop_k_atr"],
                stop_k_atr_t3=g["stop_k_atr"], trail_atr_mult=g["trail_atr_mult"],
                t1_donch_bars=g["t1_donch_bars"], er_min=g["er_min"],
                short_anchor_800=g["short_anchor_800"],
                ratchet_arm0_r=a0, ratchet_lock0_r=l0, ratchet_arm1_r=a1,
                ratchet_lock1_r=l1, trail_start_r=ts,
                time_decay_4h=g["time_decay_4h"])
    r = replace(BASE_R, max_concurrent=g["max_concurrent"], max_hold_4h=g["max_hold_4h"])
    return p, r


def quarter_score(res: dict) -> float:
    """Per-quarter objective mirroring the mission criteria (higher = better)."""
    s = res["roi_pct"] - 2.0 * max(0.0, res["max_dd_pct"] - 4.5)
    if res["n_trades"] < 15:
        s -= 15.0
    if res["win_rate_pct"] < 40.0:
        s -= 8.0
    if res["profit_factor"] < 1.40:
        s -= 6.0
    if res["max_r_realized"] < 4.0 and res["max_mfe_r"] < 4.0:
        s -= 4.0
    return s


def trailing_objective(sds, p, r, t_start_ms, lookback_days=365):
    """Evaluate the trailing year (strictly before t_start, 72h embargo) as
    four sequential quarters and score with the criteria composite."""
    embargo = t_start_ms - 72 * 3_600_000
    quarters = []
    for k in range(4, 0, -1):
        q_end = embargo - (k - 1) * 90 * 86_400_000
        q_start = max(embargo - k * 90 * 86_400_000,
                      int(pd.Timestamp("2020-09-15").value // 1e6))
        if q_end - q_start < 30 * 86_400_000:
            continue
        w = {"id": -k, "label": f"train{k}", "start": pd.Timestamp(q_start, unit="ms").strftime("%Y-%m-%d"),
             "end": pd.Timestamp(q_end, unit="ms").strftime("%Y-%m-%d"), "name": "train"}
        res = evaluate_window(sds, w, p, FRIC, r)
        quarters.append(res)
    if not quarters:
        return -1e9, []
    total = sum(quarter_score(q) for q in quarters)
    year_roi = sum(q["roi_pct"] for q in quarters)
    return total + 0.3 * year_roi, quarters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="Engine/verification/s1_trend_failfast.json")
    ap.add_argument("--symbols", type=str, default="BTCUSDT,ETHUSDT,XRPUSDT,SOLUSDT")
    ap.add_argument("--max-reopt", type=int, default=25)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    sds = load_symbols([s.strip() for s in args.symbols.split(",")])
    print(f"[failfast] symbols: {sorted(sds)} | grid size: {len(GRID)}", flush=True)

    # current configuration (design-frozen global default)
    cur = GRID[0]
    # find the design-frozen default in grid terms (k=2.0, trail=4.0, donch=48,
    # er=0, anchor=False, mc=2)
    for g in GRID:
        if (g["stop_k_atr"] == 2.0 and g["trail_atr_mult"] == 4.0
                and g["t1_donch_bars"] == 48 and g["er_min"] == 0.0
                and g["max_concurrent"] == 2
                and g["ratchet"] == RATCHET_VARIANTS[0]
                and g["time_decay_4h"] == 24 and g["max_hold_4h"] == 60):
            cur = g
            break

    results = []
    config_timeline = []
    n_reopt = 0
    t_all = time.time()

    for w in OOS_WINDOWS:
        p, r = make_config(cur)
        res = evaluate_window(sds, w, p, FRIC, r)
        res["config"] = dict(cur)
        if res["verdict"] == "PASS" or n_reopt >= args.max_reopt:
            results.append(res)
            print(f"W{w['id']:02d} {w['label']} | ROI {res['roi_pct']:>7.2f}% DD {res['max_dd_pct']:>5.2f}% "
                  f"WR {res['win_rate_pct']:>5.1f}% n={res['n_trades']:>3} PF {res['profit_factor']:>5.2f} "
                  f"maxR {res['max_r_realized']:>5.2f} | {res['verdict']}", flush=True)
            continue

        # ---------------- FAIL-FAST CAUSAL RE-OPTIMIZATION ----------------
        n_reopt += 1
        t_start_ms = int(pd.Timestamp(w["start"]).value // 1e6)
        print(f"W{w['id']:02d} {w['label']} FAILED ({','.join(res['fail_reasons'])}) -> causal re-opt "
              f"on trailing data strictly before {w['start']} (72h embargo)", flush=True)
        t0 = time.time()
        if args.workers > 1:
            global _SDS, _WORKER_TSTART
            _SDS, _WORKER_TSTART = sds, t_start_ms
            import multiprocessing as mp
            with mp.Pool(args.workers) as pool:
                scored = pool.map(_score_worker, GRID, chunksize=4)
        else:
            scored = []
            for g in GRID:
                pg, rg = make_config(g)
                obj, _ = trailing_objective(sds, pg, rg, t_start_ms)
                scored.append((obj, g))
        scored.sort(key=lambda x: -x[0])
        print(f"   [re-opt {n_reopt}] {len(GRID)} configs scored in {time.time()-t0:.0f}s | "
              f"best objective {scored[0][0]:.1f}", flush=True)

        # zero-regression check on previously PASSED windows (top-8 candidates)
        passed_idx = [i for i, rr in enumerate(results) if rr["verdict"] == "PASS"]
        adopted = None
        for obj, g in scored[:8]:
            if g == cur:
                continue
            pg, rg = make_config(g)
            ok = True
            for i in passed_idx:
                wj = OOS_WINDOWS[i]
                rj = evaluate_window(sds, wj, pg, FRIC, rg)
                if rj["verdict"] != "PASS":
                    ok = False
                    break
            if ok:
                adopted = (obj, g)
                break
        if adopted is None:
            # keep current config if nothing improves without regression
            print("   [re-opt] no zero-regression improvement found; keeping current config", flush=True)
            results.append(res)
            print(f"W{w['id']:02d} {w['label']} | ROI {res['roi_pct']:>7.2f}% ... | {res['verdict']} (kept)", flush=True)
            continue

        cur = adopted[1]
        print(f"   [re-opt] adopted {adopted[1]} (obj {adopted[0]:.1f})", flush=True)
        # resume at the failing window with the new config
        p, r = make_config(cur)
        res = evaluate_window(sds, w, p, FRIC, r)
        res["config"] = dict(cur)
        results.append(res)
        print(f"W{w['id']:02d} {w['label']} | ROI {res['roi_pct']:>7.2f}% DD {res['max_dd_pct']:>5.2f}% "
              f"WR {res['win_rate_pct']:>5.1f}% n={res['n_trades']:>3} PF {res['profit_factor']:>5.2f} "
              f"maxR {res['max_r_realized']:>5.2f} | {res['verdict']} (re-optimized)", flush=True)

    stats = system_statistics(results, BASE_R)
    payload = {
        "strategy": "S1 Trend-Following Orderflow Suite — fail-fast causal walk-forward",
        "protocol": "Mission Section 4.5: sequential fail-fast with causal re-optimization "
                    "(trailing 365d + 72h embargo) and zero-regression verification",
        "grid_size": len(GRID),
        "n_reoptimizations": n_reopt,
        "summary": stats,
        "windows": [{k: v for k, v in r.items() if k != "trades"} for r in results],
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=1, default=str)
    print(f"\n[failfast] wrote {args.out}")
    print(f"passed {stats['windows_passed']}/{stats['windows_total']} | "
          f"CAGR {stats['cagr_pct']:.1f}% | total time {time.time()-t_all:.0f}s")


if __name__ == "__main__":
    main()
