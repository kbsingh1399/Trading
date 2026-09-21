"""OX62 PRIMARY: single-shot full-20 evaluation at canonical params (protocol §4(i)).
Usage: /home/user/ox61venv/bin/python docs/ox62_research/run_ox62_primary.py [--family F1]
"""
import sys, os, json, time, hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))
os.chdir(PROJECT_ROOT)

import pandas as pd
from ox62_lib import (load_frame, add_harness_cols, generate_candidates, replay_family,
                      pool_stats, HERE, OX62_BASE_RISK_USD)
from ox62_families import SIG, CANONICAL, NAMES
from Engine.core.strategy_kernel import CANONICAL_18_ASSETS
from Engine.core.base_strategy import EngineConfig

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def run_family(fid, cfg, w01_start):
    t0 = time.time()
    params = CANONICAL[fid]
    all_c = []
    for sym in CANONICAL_18_ASSETS:
        df = add_harness_cols(load_frame(sym))
        lm, sm = SIG[fid](df, params)
        c = generate_candidates(df, lm, sm, w01_start)
        if len(c):
            c["asset"] = sym
            all_c.append(c)
    cand = pd.concat(all_c, ignore_index=True) if all_c else pd.DataFrame()
    if len(cand) == 0:
        print(f"{fid} ({NAMES[fid]}): NO CANDIDATES", flush=True)
        return None
    cand.to_parquet(HERE / f"cand_primary_{fid}.parquet", index=False)
    sc = replay_family(cand, cfg, fid)
    sc.to_csv(HERE / f"scorecard_primary_{fid}.csv", index=False)
    n_pass = int((sc["status"] == "PASS").sum())
    ps = pool_stats(cand)
    print(f"{fid} ({NAMES[fid]}): {n_pass}/20 PASS | pool {ps} | "
          f"PnL {sc['pnl_usd'].sum():+,.2f} | {time.time()-t0:.0f}s", flush=True)
    return {"family": fid, "name": NAMES[fid], "params": params, "pass": n_pass,
            "pnl": round(float(sc["pnl_usd"].sum()), 2),
            "maxDD": round(float(sc["max_dd_pct"].max()), 2), "pool": ps}

if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--family") + 1] if "--family" in sys.argv else None
    fids = [only] if only else sorted(SIG)
    cfg = EngineConfig.load()
    w01_start = pd.Timestamp(cfg.windows[0].start_date, tz="UTC")
    print(f"W01 start: {w01_start.date()} | base_risk override: ${OX62_BASE_RISK_USD} (tip: ${cfg.criteria.base_risk_usd})")
    results = []
    for fid in fids:
        r = run_family(fid, cfg, w01_start)
        if r:
            results.append(r)
    if not only:
        man = {"program": "OX62 PRIMARY single-shot", "protocol": "docs/ox62_research/PROTOCOL.md",
               "economics": {"base_risk_usd": OX62_BASE_RISK_USD, "tip_base_risk_usd": float(cfg.criteria.base_risk_usd)},
               "w01_start": str(w01_start.date()), "results": results,
               "code_hashes": {f: sha256(HERE / f) for f in
                               ["ox62_lib.py", "ox62_families.py", "run_ox62_primary.py", "PROTOCOL.md"]}}
        with open(HERE / "manifest_primary.json", "w") as f:
            json.dump(man, f, indent=1)
        print("PRIMARY COMPLETE")
