"""OX63 single-shot: F6R scaled candidates + dual-economics replay + portfolio grading.
Usage: /home/user/ox61venv/bin/python docs/ox63_research/run_ox63.py [--check-only]
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
os.chdir(PROJECT_ROOT)

import pandas as pd
from ox63_lib import (add_msb_anchor, sig_F6R, generate_candidates_scaled, replay_economics,
                      portfolio_metrics, HERE, RISK_RESEARCH_USD, RISK_PRODUCTION_USD,
                      INITIAL_CAPITAL_USD)
from ox62_lib import load_frame, add_harness_cols, generate_candidates, pool_stats
from Engine.core.strategy_kernel import (CANONICAL_18_ASSETS, UX_TP1_R, UX_TP1_FRAC,
                                         UX_TP1_LOCK_R, UX_MIN_R_EFF_SCALED, UX_MAX_R_EFF,
                                         MIN_R_MULTIPLE)
from Engine.core.base_strategy import EngineConfig

ARTIFACTS = ["cand_ox63_F6R.parquet", "cand_ox63_F6R_mono.parquet", "scorecard_ox63_50.csv",
             "scorecard_ox63_10.csv", "scorecard_ox63_mono50.csv", "exec_ox63_50.parquet",
             "exec_ox63_10.parquet", "exec_ox63_mono50.parquet"]
CODE_FILES = ["ox63_lib.py", "run_ox63.py", "test_ox63_scaled.py", "test_ox63_manager.py",
              "test_ox63_mirror.py", "test_ox63_msb.py", "PROTOCOL.md"]


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
    all_scaled, all_mono = [], []
    for sym in CANONICAL_18_ASSETS:
        df = add_msb_anchor(add_harness_cols(load_frame(sym)))
        lm, sm = sig_F6R(df)
        cs = generate_candidates_scaled(df, lm, sm, w01_start)
        if len(cs):
            cs["asset"] = sym
            all_scaled.append(cs)
        cm = generate_candidates(df, lm, sm, w01_start)  # P12: identical signals, mono 2.5R
        if len(cm):
            cm["asset"] = sym
            all_mono.append(cm)
    cand = pd.concat(all_scaled, ignore_index=True) if all_scaled else pd.DataFrame()
    mono = pd.concat(all_mono, ignore_index=True) if all_mono else pd.DataFrame()
    return cand, mono


def run_pipeline(cfg, w01_start):
    cand, mono = build_candidates(w01_start)
    out = {}
    out["cand"], out["mono"] = cand, mono
    out["sc50"], out["ex50"] = replay_economics(cand, cfg, "F6R", RISK_RESEARCH_USD)
    out["sc10"], out["ex10"] = replay_economics(cand, cfg, "F6R", RISK_PRODUCTION_USD)
    out["scm50"], out["exm50"] = replay_economics(mono, cfg, "F6R-MONO", RISK_RESEARCH_USD)
    out["pf50"] = portfolio_metrics(out["ex50"], "research-$50")
    out["pf10"] = portfolio_metrics(out["ex10"], "production-$10")
    out["pfm50"] = portfolio_metrics(out["exm50"], "counterfactual-mono-$50")
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
    man_path = HERE / "manifest_ox63.json"

    if check_only:
        man = json.load(open(man_path))
        ok = True
        for f, h in man["artifact_sha256"].items():
            actual = sha256_file(HERE / f)
            match = actual == h
            ok &= match
            print(f"  [{'OK' if match else 'MISMATCH'}] {f}")
        for f, h in man["code_hashes"].items():
            actual = sha256_file(HERE / f)
            match = actual == h
            ok &= match
            print(f"  [{'OK' if match else 'MISMATCH'}] code:{f}")
        print("Re-running pipeline in memory (determinism proof)...", flush=True)
        out = run_pipeline(cfg, w01_start)
        live = {"cand": logical_hash(out["cand"]), "mono": logical_hash(out["mono"]),
                "sc50": logical_hash(out["sc50"]), "sc10": logical_hash(out["sc10"]),
                "scm50": logical_hash(out["scm50"]), "ex50": logical_hash(out["ex50"]),
                "ex10": logical_hash(out["ex10"]), "exm50": logical_hash(out["exm50"])}
        for k, v in live.items():
            match = v == man["logical_hashes"][k]
            ok &= match
            print(f"  [{'OK' if match else 'MISMATCH'}] pipeline:{k} rows={v['rows']}")
        print("CHECK-ONLY: " + ("ALL MATCH — determinism proven." if ok else "FAILURES PRESENT."))
        sys.exit(0 if ok else 1)

    t0 = time.time()
    print(f"W01 start: {w01_start.date()} | dual economics ${RISK_RESEARCH_USD}/${RISK_PRODUCTION_USD} "
          f"| capital ${INITIAL_CAPITAL_USD}", flush=True)
    out = run_pipeline(cfg, w01_start)
    cand = out["cand"]
    if len(cand) == 0:
        print("F6R SCALED: NO CANDIDATES")
        sys.exit(1)
    cand.to_parquet(HERE / "cand_ox63_F6R.parquet", index=False)
    out["mono"].to_parquet(HERE / "cand_ox63_F6R_mono.parquet", index=False)
    out["sc50"].to_csv(HERE / "scorecard_ox63_50.csv", index=False)
    out["sc10"].to_csv(HERE / "scorecard_ox63_10.csv", index=False)
    out["scm50"].to_csv(HERE / "scorecard_ox63_mono50.csv", index=False)
    out["ex50"].to_parquet(HERE / "exec_ox63_50.parquet", index=False)
    out["ex10"].to_parquet(HERE / "exec_ox63_10.parquet", index=False)
    out["exm50"].to_parquet(HERE / "exec_ox63_mono50.parquet", index=False)

    ps = pool_stats(cand)
    ps["scaled_rate"] = round(float(cand["scaled"].mean()), 4)
    v50, v10 = verdict(out["pf50"]), verdict(out["pf10"])
    conj = {k: bool(v50[k] and v10[k]) for k in v50}
    man = {"program": "OX63 single-shot", "protocol": "docs/ox63_research/PROTOCOL.md",
           "evidence_grade": "EXPLORATORY-CONFIRMATORY HYBRID (protocol §1)",
           "economics": {"research_risk_usd": RISK_RESEARCH_USD,
                         "production_risk_usd": RISK_PRODUCTION_USD,
                         "initial_capital_usd": INITIAL_CAPITAL_USD},
           "w01_start": str(w01_start.date()),
           "params": {"TP1_R": UX_TP1_R, "TP1_FRAC": UX_TP1_FRAC, "TP1_LOCK_R": UX_TP1_LOCK_R,
                      "veto_R_eff": UX_MIN_R_EFF_SCALED, "cap_R_eff": UX_MAX_R_EFF,
                      "fallback_R": MIN_R_MULTIPLE, "friction_R": 0.08},
           "pool_scaled": ps, "pool_mono": pool_stats(out["mono"]),
           "portfolio_50": out["pf50"], "portfolio_10": out["pf10"],
           "portfolio_mono50": out["pfm50"],
           "verdict_50": v50, "verdict_10": v10, "conjunction": conj,
           "all_pass_conjunction": bool(all(conj.values())),
           "logical_hashes": {"cand": logical_hash(cand), "mono": logical_hash(out["mono"]),
                              "sc50": logical_hash(out["sc50"]), "sc10": logical_hash(out["sc10"]),
                              "scm50": logical_hash(out["scm50"]), "ex50": logical_hash(out["ex50"]),
                              "ex10": logical_hash(out["ex10"]), "exm50": logical_hash(out["exm50"])},
           "artifact_sha256": {f: sha256_file(HERE / f) for f in ARTIFACTS},
           "code_hashes": {f: sha256_file(HERE / f) for f in CODE_FILES}}
    with open(man_path, "w") as f:
        json.dump(man, f, indent=1)

    for tag, sc in [("50", out["sc50"]), ("10", out["sc10"]), ("mono50", out["scm50"])]:
        n_pass = int((sc["status"] == "PASS").sum())
        print(f"{tag}: {n_pass}/20 window-PASS (disclosure) | PnL {sc['pnl_usd'].sum():+,.2f} | "
              f"maxDD {sc['max_dd_pct'].max():.2f}%", flush=True)
    for tag, pf in [("50", out["pf50"]), ("10", out["pf10"]), ("mono50", out["pfm50"])]:
        print(f"portfolio-{tag}: trades={pf['trades']} Sharpe={pf['sharpe']} PF={pf['profit_factor']} "
              f"DD={pf['max_dd_pct']}% annual={pf['annual']} net={pf['net_pnl']:+,.2f}", flush=True)
    print(f"conjunction: {conj} | ALL={all(conj.values())} | {time.time()-t0:.0f}s", flush=True)
    print("OX63 COMPLETE")


if __name__ == "__main__":
    main()
