"""Per-window constraint breakdown for scorecards, against the shipped criteria.

Usage: ``python -m Engine.levels_poc_lab.constraint_check lpl_ungated2``

Engine/target_oos_criteria.json does not only cap ROI/win-rate/trade count: the
certification contract's score_metrics requires

    checks["max_dd"] = maxdd < 5 and stress_dd < 5

i.e. **both** the realised equity-curve drawdown and the adverse-bound (stress)
drawdown must stay under 5 %.  This checker therefore tests all of:

    roi >= 10 %, max_dd < 5 %, stress_dd < 5 %, win_rate >= 40 %, trades >= 15

`min_r_multiple` 4.0 is *not* a realised-trade test: the protocol records
"r_interpretation: minimum planned target net4R; achieved average R reported
separately", so it is a configuration property (target_r >= 4) and is satisfied by
construction; the realised best R is printed for transparency only.
"""
import json
import sys
from pathlib import Path

# Scorecards are written to the repo-level scratch/ directory (git-ignored run
# artifacts); accept either a bare scorecard name or an explicit path.
S = Path(__file__).resolve().parents[2] / "scratch"


def main():
    for name in sys.argv[1:]:
        f = S / f"{name}.json" if not name.endswith(".json") else S / name
        d = json.loads(f.read_text())
        print(f"\n=== {f.stem}: {d['windows_passed']}/{d['windows_total']} pass, "
              f"{d['total_trades']} trades, {d['total_pnl']:+.2f} USD "
              f"({d['roi_total_pct']:+.2f} %) ===")
        counts = {"roi": 0, "dd_realised": 0, "dd_stress": 0, "wr": 0, "n": 0}
        passed = 0
        for r in d["rows"]:
            fails = []
            if r["roi"] < 10.0:
                fails.append(f"roi({r['roi']:+.1f})")
                counts["roi"] += 1
            if r["max_dd"] >= 5.0:
                fails.append(f"dd({r['max_dd']:.1f})")
                counts["dd_realised"] += 1
            if r.get("adverse_dd", 0.0) >= 5.0:
                fails.append(f"stress({r['adverse_dd']:.1f})")
                counts["dd_stress"] += 1
            if r["win_rate"] < 40.0:
                fails.append(f"wr({r['win_rate']:.0f})")
                counts["wr"] += 1
            if r["trades"] < 15:
                fails.append(f"n({r['trades']})")
                counts["n"] += 1
            if fails:
                print(f"  W{r['window_id']:02d} " + " ".join(fails))
            else:
                passed += 1
        print(f"  failing each rule: {counts}")
        print(f"  windows passing all five checks: {passed}/20 "
              f"(scorecard verdict counted {d['windows_passed']})")
        if "best_r" in d["rows"][0]:
            br = [r["best_r"] for r in d["rows"]]
            aw = [r.get("avg_winner_r") for r in d["rows"] if r.get("avg_winner_r")]
            print(f"  realised best R per window: min {min(br):.2f} / median "
                  f"{sorted(br)[len(br)//2]:.2f} / max {max(br):.2f}"
                  + (f" | mean winner R {sum(aw)/len(aw):.2f}" if aw else ""))


if __name__ == "__main__":
    main()
