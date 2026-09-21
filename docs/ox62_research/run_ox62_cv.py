"""OX62 SECONDARY: bidirectional 2-fold blocked-CV (protocol §(ii) + amendment 2).
Usage: /home/user/ox61venv/bin/python docs/ox62_research/run_ox62_cv.py
"""
import sys, os, json, time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))
os.chdir(PROJECT_ROOT)

import numpy as np
import pandas as pd
from ox62_lib import (load_frame, add_harness_cols, generate_candidates, replay_family,
                      HERE)
from ox62_families import SIG, GRIDS, NAMES
from Engine.core.strategy_kernel import CANONICAL_18_ASSETS
from Engine.core.base_strategy import EngineConfig

PURGE = pd.Timedelta(days=5)

def gen_combo(fid, ci, params, w01_start):
    out = HERE / f"cand_cv_{fid}_{ci}.parquet"
    if out.exists():
        return pd.read_parquet(out)
    all_c = []
    for sym in CANONICAL_18_ASSETS:
        df = add_harness_cols(load_frame(sym))
        lm, sm = SIG[fid](df, params)
        c = generate_candidates(df, lm, sm, w01_start)
        if len(c):
            c["asset"] = sym
            all_c.append(c)
    cand = pd.concat(all_c, ignore_index=True) if all_c else pd.DataFrame()
    if len(cand):
        cand.to_parquet(out, index=False)
    return cand

def fold_netr(cand, lo, hi):
    if len(cand) == 0:
        return -np.inf, 0
    d = pd.to_datetime(cand["datetime"], utc=True)
    m = (d >= lo) & (d < hi)
    sub = cand[m]
    if len(sub) == 0:
        return -np.inf, 0
    return float(sub["r_realized"].sum()), len(sub)

if __name__ == "__main__":
    cfg = EngineConfig.load()
    w01_start = pd.Timestamp(cfg.windows[0].start_date, tz="UTC")
    t_mid = pd.Timestamp(cfg.windows[10].start_date, tz="UTC")  # W11 start
    data_end = pd.Timestamp("2026-04-01", tz="UTC")
    print(f"folds: A select [W01, Tmid-5d) score W11-20 | B select [Tmid, end) score W01-10 | Tmid={t_mid.date()}")
    summary = []
    for fid in sorted(SIG):
        combos = GRIDS[fid]
        cands = [gen_combo(fid, ci, p, w01_start) for ci, p in enumerate(combos)]
        # Fold A selection (purged) / Fold B selection
        nA = [fold_netr(c, w01_start, t_mid - PURGE) for c in cands]
        nB = [fold_netr(c, t_mid, data_end) for c in cands]
        wA = int(np.argmax([x[0] for x in nA])) if len(combos) > 1 else 0
        wB = int(np.argmax([x[0] for x in nB])) if len(combos) > 1 else 0
        row = {"family": fid, "name": NAMES[fid],
               "selA": {"combo": wA, "params": combos[wA], "netR": round(nA[wA][0], 2), "n": nA[wA][1]},
               "selB": {"combo": wB, "params": combos[wB], "netR": round(nB[wB][0], 2), "n": nB[wB][1]}}
        for fold, wsel, wins in (("A", wA, list(range(11, 21))), ("B", wB, list(range(1, 11)))):
            sc = replay_family(cands[wsel], cfg, f"{fid}{fold}")
            sc.to_csv(HERE / f"scorecard_cv_{fid}_{fold}.csv", index=False)
            sub = sc[sc["window_id"].isin(wins)]
            row[f"score{fold}"] = {"pass": f"{int((sub['status']=='PASS').sum())}/10",
                                   "pnl": round(float(sub["pnl_usd"].sum()), 2)}
        totA = int(row["scoreA"]["pass"].split("/")[0]); totB = int(row["scoreB"]["pass"].split("/")[0])
        row["total"] = f"{totA + totB}/20"
        summary.append(row)
        print(f"{fid} ({NAMES[fid]}): A sel c{wA} {combos[wA]} -> score {row['scoreA']['pass']} | "
              f"B sel c{wB} {combos[wB]} -> score {row['scoreB']['pass']} | TOTAL {row['total']}", flush=True)
    with open(HERE / "manifest_cv.json", "w") as f:
        json.dump({"program": "OX62 SECONDARY bidirectional 2-fold CV", "t_mid": str(t_mid.date()),
                   "purge_days": 5, "folds": summary}, f, indent=1)
    print("CV COMPLETE")
