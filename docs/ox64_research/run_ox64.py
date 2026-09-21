"""OX64 single-shot: candidates A/B/C + dual-economics replay + portfolio grading.
Usage: /home/user/ox61venv/bin/python docs/ox64_research/run_ox64.py [--check-only]
--check-only: verify filed artifact hashes + re-run pipeline in memory (determinism proof).
"""
import sys
import os
import json
import time
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "ox62_research"))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "ox63_research"))
os.chdir(PROJECT_ROOT)

import pandas as pd
from ox64_lib import (daily_bars, add_trailing_stats, generate_candidates_A,
                      generate_candidates_B, generate_candidates_C, HERE)
from ox62_lib import load_frame, add_harness_cols, pool_stats
from ox63_lib import add_msb_anchor, replay_economics, portfolio_metrics
from ox63_lib import RISK_RESEARCH_USD, RISK_PRODUCTION_USD
from Engine.core.strategy_kernel import CANONICAL_18_ASSETS
from Engine.core.base_strategy import EngineConfig

CANDS = ["A", "B", "C", "Cs"]
ARTIFACTS = ([f"cand_ox64_{c}.parquet" for c in CANDS]
             + [f"scorecard_ox64_{c}_{e}.csv" for c in CANDS for e in ("50", "10")]
             + [f"exec_ox64_{c}_{e}.parquet" for c in CANDS for e in ("50", "10")])
CODE_FILES = ["ox64_lib.py", "run_ox64.py", "test_ox64_signals.py", "PROTOCOL.md"]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def logical_hash(df):
    if df is None or len(df) == 0:
        return {"rows": 0, "hash": "empty"}
    return {"rows": int(len(df)),
            "hash": hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values.tobytes()).hexdigest()}


def build_candidates(w01_start):
    acc = {c: [] for c in CANDS}
    for sym in CANONICAL_18_ASSETS:
        df = load_frame(sym)
        t = add_trailing_stats(daily_bars(df))
        for c, fn in [("A", generate_candidates_A), ("B", generate_candidates_B)]:
            cc = fn(df, t, w01_start)
            if len(cc):
                cc["asset"] = sym
                acc[c].append(cc)
        h = add_msb_anchor(add_harness_cols(df))
        for c, sc in [("C", False), ("Cs", True)]:
            cc = generate_candidates_C(h, t, w01_start, scaled=sc)
            if len(cc):
                cc["asset"] = sym
                acc[c].append(cc)
    return {c: (pd.concat(acc[c], ignore_index=True) if acc[c] else pd.DataFrame()) for c in CANDS}


def run_pipeline(cfg, w01_start):
    cand = build_candidates(w01_start)
    out = {"cand": cand}
    for c in CANDS:
        out[f"sc{c}50"], out[f"ex{c}50"] = replay_economics(cand[c], cfg, f"OX64-{c}", RISK_RESEARCH_USD)
        out[f"sc{c}10"], out[f"ex{c}10"] = replay_economics(cand[c], cfg, f"OX64-{c}", RISK_PRODUCTION_USD)
        out[f"pf{c}50"] = portfolio_metrics(out[f"ex{c}50"], f"{c}-research-$50")
        out[f"pf{c}10"] = portfolio_metrics(out[f"ex{c}10"], f"{c}-production-$10")
    return out


def verdict(m):
    return {"sharpe_ge_1.50": m["sharpe"] >= 1.50,
            "pf_ge_1.35": m["profit_factor"] >= 1.35,
            "dd_le_10": m["max_dd_pct"] <= 10.0,
            "y2024_pos": m["annual"].get(2024, 0) > 0,
            "y2025_pos": m["annual"].get(2025, 0) > 0}


def main():
    check_only = "--check-only" in sys.argv
    cfg = EngineConfig.load()
    w01_start = pd.Timestamp(cfg.windows[0].start_date, tz="UTC")
    man_path = HERE / "manifest_ox64.json"

    if check_only:
        man = json.load(open(man_path))
        ok = True
        for f, h in man["artifact_sha256"].items():
            match = sha256_file(HERE / f) == h
            ok &= match
            print(f"  [{'OK' if match else 'MISMATCH'}] {f}")
        for f, h in man["code_hashes"].items():
            match = sha256_file(HERE / f) == h
            ok &= match
            print(f"  [{'OK' if match else 'MISMATCH'}] code:{f}")
        print("Re-running pipeline in memory (determinism proof)...", flush=True)
        out = run_pipeline(cfg, w01_start)
        live = {}
        for c in CANDS:
            live[f"cand{c}"] = logical_hash(out["cand"][c])
            live[f"sc{c}50"] = logical_hash(out[f"sc{c}50"])
            live[f"sc{c}10"] = logical_hash(out[f"sc{c}10"])
            live[f"ex{c}50"] = logical_hash(out[f"ex{c}50"])
            live[f"ex{c}10"] = logical_hash(out[f"ex{c}10"])
        for k, v in live.items():
            match = v == man["logical_hashes"][k]
            ok &= match
            print(f"  [{'OK' if match else 'MISMATCH'}] pipeline:{k} rows={v['rows']}")
        print("CHECK-ONLY: " + ("ALL MATCH — determinism proven." if ok else "FAILURES PRESENT."))
        sys.exit(0 if ok else 1)

    t0 = time.time()
    print(f"W01 start: {w01_start.date()} | dual economics ${RISK_RESEARCH_USD}/${RISK_PRODUCTION_USD}",
          flush=True)
    out = run_pipeline(cfg, w01_start)
    for c in CANDS:
        out["cand"][c].to_parquet(HERE / f"cand_ox64_{c}.parquet", index=False)
        out[f"sc{c}50"].to_csv(HERE / f"scorecard_ox64_{c}_50.csv", index=False)
        out[f"sc{c}10"].to_csv(HERE / f"scorecard_ox64_{c}_10.csv", index=False)
        out[f"ex{c}50"].to_parquet(HERE / f"exec_ox64_{c}_50.parquet", index=False)
        out[f"ex{c}10"].to_parquet(HERE / f"exec_ox64_{c}_10.parquet", index=False)

    man = {"program": "OX64 single-shot", "protocol": "docs/ox64_research/PROTOCOL.md",
           "evidence_grade": "EXPLORATORY-CONFIRMATORY HYBRID, program-selection outcome-informed (§1)",
           "economics": {"research_risk_usd": RISK_RESEARCH_USD,
                         "production_risk_usd": RISK_PRODUCTION_USD},
           "w01_start": str(w01_start.date()),
           "params": {"Q0_trading_day_min_bars": 10, "Q1_A_zero_flat": True,
                      "Q2_B_threshold_sigma_mult": 0.5, "Q3_C_mult_cap": [0.5, 2.0],
                      "Q4_R_ATR_mult": 1.5, "Q5_horizon_reason": 4, "friction_R": 0.08,
                      "A_formation_trading_days": 252, "B_hold_trading_days": 1,
                      "C_veto": 2.5, "C_fallback": 2.5, "C_cap": 3.5}}
    for c in CANDS:
        man[f"pool_{c}"] = pool_stats(out["cand"][c]) if len(out["cand"][c]) else {"n": 0}
        man[f"portfolio_{c}_50"] = out[f"pf{c}50"]
        man[f"portfolio_{c}_10"] = out[f"pf{c}10"]
        v50, v10 = verdict(out[f"pf{c}50"]), verdict(out[f"pf{c}10"])
        man[f"verdict_{c}_50"] = v50
        man[f"verdict_{c}_10"] = v10
        man[f"conjunction_{c}"] = {k: bool(v50[k] and v10[k]) for k in v50}
        man[f"all_pass_{c}"] = bool(all(man[f"conjunction_{c}"].values()))
    man["logical_hashes"] = {}
    for c in CANDS:
        man["logical_hashes"][f"cand{c}"] = logical_hash(out["cand"][c])
        man["logical_hashes"][f"sc{c}50"] = logical_hash(out[f"sc{c}50"])
        man["logical_hashes"][f"sc{c}10"] = logical_hash(out[f"sc{c}10"])
        man["logical_hashes"][f"ex{c}50"] = logical_hash(out[f"ex{c}50"])
        man["logical_hashes"][f"ex{c}10"] = logical_hash(out[f"ex{c}10"])
    man["artifact_sha256"] = {f: sha256_file(HERE / f) for f in ARTIFACTS}
    man["code_hashes"] = {f: sha256_file(HERE / f) for f in CODE_FILES}
    with open(man_path, "w") as f:
        json.dump(man, f, indent=1)

    for c in CANDS:
        for tag, pf in [("50", out[f"pf{c}50"]), ("10", out[f"pf{c}10"])]:
            print(f"{c}-{tag}: trades={pf['trades']} Sharpe={pf['sharpe']} PF={pf['profit_factor']} "
                  f"DD={pf['max_dd_pct']}% annual={pf['annual']} net={pf['net_pnl']:+,.2f}", flush=True)
    for c in ["A", "B", "C"]:
        print(f"conjunction-{c}: {man[f'conjunction_{c}']} ALL={man[f'all_pass_{c}']}", flush=True)
    print(f"OX64 COMPLETE | {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
