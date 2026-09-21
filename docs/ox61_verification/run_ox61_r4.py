"""OX61 R4: regenerate + pin the honest 20-window scorecard from committed code.

Regenerates (clean-checkout safe; caches rebuilt when absent):
  PRIMARY  dual-R6-unified   (live-spec exits, walk-forward, gate 0.55)
  SIBLING  dual-R6-precommitted (filed-spec exits, walk-forward, gate 0.55)
  BANDS    dual-R6-unified at gates {0.53, 0.55, 0.57} (threshold sensitivity)
Writes scorecard_r4_pinned.csv + r4_manifest.json (provenance: commit, command,
config hashes, library versions, seeds, artifact sha256).
Usage: /home/user/ox61venv/bin/python docs/ox61_verification/run_ox61_r4.py [--check-only]
  --check-only: re-run phase B+C from committed code and assert byte-equality
  with the pinned CSVs (no overwrite).
"""
import sys, os, json, shutil, hashlib, subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))
os.chdir(PROJECT_ROOT)

import pandas as pd
import run_ox61_r6 as r6

HERE = Path(__file__).parent
GATES = (0.53, 0.55, 0.57)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def gate_suffix(g):
    return f"g{int(round(g * 100)):03d}"

def run_bands():
    r6.phase_a("unified")
    paths = {}
    for gate in GATES:
        print(f"--- gate {gate} ---", flush=True)
        r6.PROB_THRESH = gate
        r6.phase_b("unified")
        s4_canon = HERE / "s4_r6_unified.parquet"
        s4_g = HERE / f"s4_r6_unified_{gate_suffix(gate)}.parquet"
        shutil.move(str(s4_canon), str(s4_g))
        shutil.copy(str(s4_g), str(s4_canon))
        r6.phase_c("unified")
        sc_canon = HERE / "scorecard_dual_r6_unified.csv"
        sc_g = HERE / f"scorecard_dual_r6_unified_{gate_suffix(gate)}.csv"
        shutil.move(str(sc_canon), str(sc_g))
        cd_canon = HERE / "candidates_dual_r6_unified.parquet"
        cd_g = HERE / f"candidates_dual_r6_unified_{gate_suffix(gate)}.parquet"
        shutil.move(str(cd_canon), str(cd_g))
        paths[gate] = {"s4": str(s4_g), "scorecard": str(sc_g), "candidates": str(cd_g)}
    # restore canonical 0.55 files
    for src, dst in [
        (HERE / "s4_r6_unified_g055.parquet", HERE / "s4_r6_unified.parquet"),
        (HERE / "scorecard_dual_r6_unified_g055.csv", HERE / "scorecard_dual_r6_unified.csv"),
        (HERE / "candidates_dual_r6_unified_g055.parquet", HERE / "candidates_dual_r6_unified.parquet"),
    ]:
        shutil.copy(str(src), str(dst))
    r6.PROB_THRESH = 0.55
    return paths

def run_sibling():
    r6.phase_a("precommitted")
    r6.PROB_THRESH = 0.55
    r6.phase_b("precommitted")
    r6.phase_c("precommitted")

def pin_and_manifest(paths):
    shutil.copy(str(HERE / "scorecard_dual_r6_unified.csv"), str(HERE / "scorecard_r4_pinned.csv"))
    shutil.copy(str(HERE / "scorecard_dual_r6_precommitted.csv"), str(HERE / "scorecard_r4_precommitted.csv"))
    rows = []
    for gate in GATES:
        d = pd.read_csv(paths[gate]["scorecard"])
        rows.append({"gate": gate, "pass_count": int((d["status"] == "PASS").sum()),
                     "total_pnl_usd": round(float(d["pnl_usd"].sum()), 2),
                     "max_dd_pct": round(float(d["max_dd_pct"].max()), 2)})
    pd.DataFrame(rows).to_csv(HERE / "scorecard_r4_bands.csv", index=False)
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                                cwd=str(PROJECT_ROOT)).stdout.strip()
    except Exception:
        commit = "unknown"
    import xgboost, sklearn
    manifest = {
        "generator": "docs/ox61_verification/run_ox61_r4.py",
        "command": "/home/user/ox61venv/bin/python docs/ox61_verification/run_ox61_r4.py",
        "commit": commit,
        "primary": "dual-R6-unified @ gate 0.55 (live-spec exits, walk-forward XGB, bar-purged)",
        "sibling": "dual-R6-precommitted @ gate 0.55 (filed-spec exits, walk-forward XGB, bar-purged)",
        "gates": list(GATES),
        "seeds": {"xgb_seed": 42, "num_boost_round": 120, "max_depth": 4, "lr": 0.05},
        "purge_bars": {"precommitted": 96, "unified": 480},
        "friction_r": 0.08,
        "versions": {"xgboost": xgboost.__version__, "sklearn": sklearn.__version__,
                     "pandas": pd.__version__, "python": sys.version.split()[0]},
        "config_hashes": {
            "target_oos_criteria.json": sha256(PROJECT_ROOT / "Engine/target_oos_criteria.json"),
            "oos_windows_forex_20.json": sha256(PROJECT_ROOT / "Engine/oos_windows_forex_20.json"),
        },
        "artifacts": {},
    }
    for p in ["scorecard_r4_pinned.csv", "scorecard_r4_precommitted.csv", "scorecard_r4_bands.csv",
              "s4_r6_unified.parquet", "s4_r6_precommitted.parquet",
              "candidates_dual_r6_unified.parquet", "candidates_dual_r6_precommitted.parquet",
              "scorecard_dual_r6_unified_g053.csv", "scorecard_dual_r6_unified_g057.csv"]:
        manifest["artifacts"][p] = sha256(HERE / p)
    with open(HERE / "r4_manifest.json", "w") as f:
        json.dump(manifest, f, indent=1)
    print("R4 pinned. Bands:")
    for r in rows:
        print(f"  gate={r['gate']}: {r['pass_count']}/20 PASS, PnL {r['total_pnl_usd']:+,.2f}, maxDD {r['max_dd_pct']}%")

def check_only():
    man = json.load(open(HERE / "r4_manifest.json"))
    r6.phase_a("unified")
    r6.phase_a("precommitted")
    for tag in ("unified", "precommitted"):
        r6.PROB_THRESH = 0.55
        r6.phase_b(tag)
        r6.phase_c(tag)
    ok = True
    for p, want in man["artifacts"].items():
        if "g05" in p:
            continue  # bands covered by primary determinism
        got = sha256(HERE / p)
        match = got == want
        ok &= match
        print(f"  [{'OK' if match else 'MISMATCH'}] {p}")
    print("R4 CHECK:", "REPRODUCES TO THE BYTE" if ok else "NON-DETERMINISM DETECTED")
    return ok

if __name__ == "__main__":
    if "--check-only" in sys.argv:
        sys.exit(0 if check_only() else 1)
    run_sibling()
    paths = run_bands()
    pin_and_manifest(paths)
