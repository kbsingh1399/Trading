#!/usr/bin/env python3
"""
================================================================================
S1 FAMILY FAIL-FAST CAUSAL WALK-FORWARD HARNESS (mission Section 4.5)
================================================================================
Family of strategy books in ONE portfolio engine:
  FAST TREND    T1 breakout / T2 pullback absorption / T3 delta expansion
  SLOW MOMENTUM M1 30-day Donchian runner (chandelier or ratchet managed)
  ABSORPTION    M2 N-bar extreme absorbed by opposite flow (target 1.2R)
  MR FADES      R1..R5 stretch / sweep-reclaim / funding / bear-rally / bull-dip

Protocol (identical to mission Section 4.5):
  sequential windows; on failure halt -> causally re-optimize on trailing
  365d data only (72h embargo) over a FIXED 256-config family grid ->
  verify zero regression on previously passed windows -> resume.
No window-keyed parameters anywhere.
================================================================================
"""
import argparse
import json
import os
import sys
import time
from dataclasses import replace

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Engine"))

import pandas as pd
import numpy as np

from s1_trend_following_suite import (TrendParams, FrictionConfig, RiskConfig,
                                      load_symbols, evaluate_window, OOS_WINDOWS,
                                      system_statistics)

# ---------------------------------------------------------------------------
# FIXED family grid (256 configs; identical for every re-optimization)
# ---------------------------------------------------------------------------
GRID = [dict(stop_k_atr=sk, trail_atr_mult=tr, donch=db, er_min=er,
             m1_mode=m1, m2_mode=m2, r_on=ro, mc=mc)
        for sk in (2.0, 2.4)
        for tr in (4.0, 5.0)
        for db in (48, 96)
        for er in (0.0, 0.10)
        for m1 in ("off", "pure", "ratchet")
        for m2 in ("off", "loose", "tight")
        for ro in (True, False)
        for mc in (2, 3)]

BASE_P = TrendParams()
BASE_R = RiskConfig()
FRIC = FrictionConfig()
RATCHET_SLOW = dict(ratchet_arm0_r=1.40, ratchet_lock0_r=0.60,
                    ratchet_arm1_r=2.40, ratchet_lock1_r=1.40, trail_start_r=2.60)


def make_config(g: dict):
    p = replace(BASE_P, **RATCHET_SLOW,
                stop_k_atr_t1=g["stop_k_atr"], stop_k_atr_t2=g["stop_k_atr"],
                stop_k_atr_t3=g["stop_k_atr"], trail_atr_mult=g["trail_atr_mult"],
                t1_donch_bars=g["donch"], er_min=g["er_min"],
                m1_enabled=(g["m1_mode"] != "off"),
                m1_trail_atr_mult=5.00, m1_stop_k_atr=3.00, m1_max_hold_4h=120,
                m2_enabled=(g["m2_mode"] != "off"),
                m2_cvd_frac_min=0.02 if g["m2_mode"] == "loose" else 0.04,
                m2_delta_share_min=0.10 if g["m2_mode"] == "loose" else 0.15,
                r1_enabled=g["r_on"], r2_enabled=g["r_on"], r3_enabled=g["r_on"],
                r4_enabled=g["r_on"], r5_enabled=g["r_on"])
    # m1 ratchet mode: keep ratchets active on the slow book too
    if g["m1_mode"] == "ratchet":
        p = replace(p, m1_trail_atr_mult=5.00)
        # ratchets apply when no_ratchet=False; M1 candidates set no_ratchet
        # dynamically below via param plumbing — simplest: engine flag
        p = replace(p, m1_stop_k_atr=3.00)
    r = replace(BASE_R, max_concurrent=g["mc"])
    return p, r


def _m1_no_ratchet_flag(p: TrendParams, g: dict) -> TrendParams:
    """M1 candidates hardcode no_ratchet=True in the engine; for 'ratchet' mode
    we emulate by tightening the slow book to ratchet+EMA21 trail management.
    Implemented via m1 params: narrower chandelier + ratchets is engine-level;
    here we simply select wider participation (stop same, trail tighter)."""
    # engine sets no_racket=True for M1 always; 'ratchet' mode approximates
    # profit-locking by a tighter chandelier (locks giveback)
    if g["m1_mode"] == "ratchet":
        return replace(p, m1_trail_atr_mult=3.50)
    return p


def quarter_score(res: dict) -> float:
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


def trailing_objective(sds, p, r, t_start_ms):
    embargo = t_start_ms - 72 * 3_600_000
    quarters = []
    for k in range(4, 0, -1):
        q_end = embargo - (k - 1) * 90 * 86_400_000
        q_start = max(embargo - k * 90 * 86_400_000,
                      int(pd.Timestamp("2020-09-15").value // 1e6))
        if q_end - q_start < 30 * 86_400_000:
            continue
        w = {"id": -k, "label": f"train{k}",
             "start": pd.Timestamp(q_start, unit="ms").strftime("%Y-%m-%d"),
             "end": pd.Timestamp(q_end, unit="ms").strftime("%Y-%m-%d"),
             "name": "train"}
        quarters.append(evaluate_window(sds, w, p, FRIC, r))
    if not quarters:
        return -1e9, []
    total = sum(quarter_score(q) for q in quarters)
    year_roi = sum(q["roi_pct"] for q in quarters)
    return total + 0.3 * year_roi, quarters


_SDS = None
_TSTART = None
_GRID_G = None


def _score_worker(args):
    g, = args
    p, r = make_config(g)
    p = _m1_no_ratchet_flag(p, g)
    obj, _ = trailing_objective(_SDS, p, r, _TSTART)
    return (obj, g)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="Engine/verification/s1_family_failfast.json")
    ap.add_argument("--symbols", type=str, default="BTCUSDT,ETHUSDT,XRPUSDT,SOLUSDT")
    ap.add_argument("--max-reopt", type=int, default=25)
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()

    sds = load_symbols([s.strip() for s in args.symbols.split(",")])
    print(f"[family] symbols: {sorted(sds)} | grid size: {len(GRID)}", flush=True)

    # initial configuration: design-frozen defaults with the full family ON
    cur = dict(stop_k_atr=2.0, trail_atr_mult=4.0, donch=48, er_min=0.0,
               m1_mode="pure", m2_mode="loose", r_on=True, mc=2)

    results = []
    n_reopt = 0
    t_all = time.time()

    for w in OOS_WINDOWS:
        p, r = make_config(cur)
        p = _m1_no_ratchet_flag(p, cur)
        res = evaluate_window(sds, w, p, FRIC, r)
        res["config"] = dict(cur)
        if res["verdict"] == "PASS" or n_reopt >= args.max_reopt:
            results.append(res)
            print(f"W{w['id']:02d} {w['label']} | ROI {res['roi_pct']:>7.2f}% DD {res['max_dd_pct']:>5.2f}% "
                  f"WR {res['win_rate_pct']:>5.1f}% n={res['n_trades']:>3} PF {res['profit_factor']:>5.2f} "
                  f"maxR {res['max_r_realized']:>5.2f} | {res['verdict']}", flush=True)
            continue

        n_reopt += 1
        t_start_ms = int(pd.Timestamp(w["start"]).value // 1e6)
        print(f"W{w['id']:02d} {w['label']} FAILED ({','.join(res['fail_reasons'])}) -> causal re-opt "
              f"on trailing data strictly before {w['start']}", flush=True)
        t0 = time.time()
        global _SDS, _TSTART
        _SDS, _TSTART = sds, t_start_ms
        if args.workers > 1:
            import multiprocessing as mp
            with mp.Pool(args.workers) as pool:
                scored = pool.map(_score_worker, [(g,) for g in GRID], chunksize=4)
        else:
            scored = [_score_worker((g,)) for g in GRID]
        scored.sort(key=lambda x: -x[0])
        print(f"   [re-opt {n_reopt}] {len(GRID)} configs scored in {time.time()-t0:.0f}s | "
              f"best objective {scored[0][0]:.1f}", flush=True)

        passed_idx = [i for i, rr in enumerate(results) if rr["verdict"] == "PASS"]
        adopted = None
        for obj, g in scored[:10]:
            if g == cur:
                continue
            pg, rg = make_config(g)
            pg = _m1_no_ratchet_flag(pg, g)
            ok = True
            for i in passed_idx:
                rj = evaluate_window(sds, OOS_WINDOWS[i], pg, FRIC, rg)
                if rj["verdict"] != "PASS":
                    ok = False
                    break
            if ok:
                adopted = (obj, g)
                break
        if adopted is None:
            print("   [re-opt] no zero-regression improvement found; keeping current config", flush=True)
            results.append(res)
            print(f"W{w['id']:02d} {w['label']} | ROI {res['roi_pct']:>7.2f}% ... | {res['verdict']} (kept)", flush=True)
            continue

        cur = adopted[1]
        print(f"   [re-opt] adopted {adopted[1]} (obj {adopted[0]:.1f})", flush=True)
        p, r = make_config(cur)
        p = _m1_no_ratchet_flag(p, cur)
        res = evaluate_window(sds, w, p, FRIC, r)
        res["config"] = dict(cur)
        results.append(res)
        print(f"W{w['id']:02d} {w['label']} | ROI {res['roi_pct']:>7.2f}% DD {res['max_dd_pct']:>5.2f}% "
              f"WR {res['win_rate_pct']:>5.1f}% n={res['n_trades']:>3} PF {res['profit_factor']:>5.2f} "
              f"maxR {res['max_r_realized']:>5.2f} | {res['verdict']} (re-optimized)", flush=True)

    stats = system_statistics(results, BASE_R)
    payload = {
        "strategy": "S1 Family (fast trend + slow momentum + absorption + MR fades) — fail-fast causal walk-forward",
        "protocol": "Mission Section 4.5: sequential fail-fast, causal family re-optimization "
                    "(trailing 365d + 72h embargo, fixed 256-config grid), zero-regression verification",
        "grid_size": len(GRID),
        "n_reoptimizations": n_reopt,
        "summary": stats,
        "windows": [{k: v for k, v in r.items() if k != "trades"} for r in results],
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=1, default=str)
    print(f"\n[family] wrote {args.out}")
    print(f"passed {stats['windows_passed']}/{stats['windows_total']} | "
          f"CAGR {stats['cagr_pct']:.1f}% | total time {time.time()-t_all:.0f}s")


if __name__ == "__main__":
    main()
