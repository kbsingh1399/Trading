"""validate_hunt.py — SEALED HOLDOUT validation for the Optuna hunt.

Reads the finished study, takes the top-K trials by DESIGN score (dedup by
param signature), evaluates each on holdout W17..W20 (passes, totals, DD),
then full-20 scorecard + matched-count null (300 sims) for the best-by-design
champion. Also emits the multiple-testing deflation summary: top-design score
distribution vs holdout outcome (selection-bias read).

Run ONLY after scratch/hunt/DONE exists.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import optuna

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
optuna.logging.set_verbosity(optuna.logging.WARNING)

import scratch.optuna_driver as drv

OUT = REPO / "scratch" / "hunt" / "holdout_validation.json"
K_TOP = 10


def eval_config(params, df_by, wins_by, design_ids, window_ids=None):
    mask_list = drv.apply_config(wins_by[params["profile"]], params)
    if mask_list is None:
        return None
    df = df_by[params["profile"]]
    per_w = wins_by[params["profile"]]
    rows = []
    total = 0.0
    passes = 0
    for i, W in enumerate(per_w):
        if window_ids is not None and W["wid"] not in window_ids:
            continue
        m = mask_list[i].copy()
        w_s = drv.WINDOWS[W["wid"] - 1][2]
        if params.get("trail_days"):
            cutoff = w_s - drv.PURGE_MS
            t0 = cutoff - params["trail_days"] * 86_400_000
            tr = df[(df.t >= t0) & (df.t < cutoff)]
            if len(tr):
                kk = (tr["fam"] + "__" + tr["tag"])
                gm = tr.groupby(kk)["r"].mean()
                ok = set(gm[gm > params["gate_min"]].index)
                if len(ok) < params["fb_k"]:
                    ok = set(gm.sort_values(ascending=False).head(params["fb_k"]).index)
                m &= np.array([k in ok for k in W["keys"]])
        if params["mode"] == "ml" and m.sum() > 0:
            cutoff = w_s - drv.PURGE_MS
            pairset = set(zip(W["keys"][m], W["geo"][m]))
            kk = (df["fam"] + "__" + df["tag"]).to_numpy()
            gg = df["geo"].to_numpy()
            trm = (df.t.to_numpy() < cutoff) & np.array([(k, g) in pairset for k, g in zip(kk, gg)])
            trd = df[trm]
            if len(trd) > 40000:
                trd = trd.sample(40000, random_state=13)
            if len(trd) >= 800:
                try:
                    s_all = drv.ml_scores(trd, W)
                    q = float(np.quantile(s_all, params["ml_q"]))
                    idxm = np.flatnonzero(m)
                    keep = idxm[s_all[idxm] >= q]
                    nm = np.zeros_like(m)
                    nm[keep] = True
                    m = nm
                except Exception:
                    pass
        pnl, roi, dd, n, wr = drv.execute_window(W, m, params["book"], params["dir_max"],
                                                 params["daily_cap"], params["risk"], params["dd_def"])
        okpass = roi >= 10.0 and dd <= 5.0 and wr >= 40.0 and n >= 15
        passes += int(okpass)
        total += pnl
        rows.append({"wid": W["wid"], "roi": roi, "dd": dd, "n": n, "wr": wr, "pass": okpass})
    return {"rows": rows, "total_pct": total / drv.CAPITAL * 100, "passes": passes,
            "counts": [r["n"] for r in rows]}


def main():
    import pandas as pd
    done = REPO / "scratch" / "hunt" / "DONE"
    if not done.exists():
        print("hunt not finished; abort"); return
    wins = drv.load_windows()
    design_ids = [w[0] for w in wins if w[0] <= 16]
    hold_ids = [w[0] for w in wins if w[0] > 16]
    df_by, wins_by = {}, {}
    for prof in ("taker41", "maker25"):
        df, per_w = drv.slices_for(prof, wins)
        df_by[prof] = df
        wins_by[prof] = per_w

    study = optuna.load_study(study_name="hunt20", storage=drv.DB)
    comp = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    print(f"trials: {len(comp)}")
    dpass = [t.user_attrs.get("design_passes", 0) for t in comp]
    dvals = [t.value for t in comp if t.value is not None]
    design_dist = {"n": len(dpass),
                   "passes_max": int(max(dpass)) if dpass else 0,
                   "passes_ge1": int(sum(1 for d in dpass if d >= 1)),
                   "passes_ge2": int(sum(1 for d in dpass if d >= 2)),
                   "passes_ge3": int(sum(1 for d in dpass if d >= 3)),
                   "passes_ge4": int(sum(1 for d in dpass if d >= 4)),
                   "passes_ge5": int(sum(1 for d in dpass if d >= 5)),
                   "passes_ge6": int(sum(1 for d in dpass if d >= 6)),
                   "value_median": float(np.median(dvals)) if dvals else 0.0,
                   "value_p95": float(np.quantile(dvals, 0.95)) if dvals else 0.0,
                   "value_p99": float(np.quantile(dvals, 0.99)) if dvals else 0.0}
    print("design dist:", design_dist, flush=True)

    # dedupe by param signature
    seen = {}
    for t in sorted(comp, key=lambda t: -(t.value or 0)):
        sig = json.dumps(t.params, sort_keys=True)
        if sig not in seen:
            seen[sig] = t
        if len(seen) >= K_TOP:
            break
    top = list(seen.values())

    results = []
    for t in top:
        params = dict(t.params)
        ho = eval_config(params, df_by, wins_by, design_ids, window_ids=hold_ids)
        if ho is None:
            continue
        results.append({
            "design_value": t.value,
            "design_passes": t.user_attrs.get("design_passes"),
            "design_total_pct": t.user_attrs.get("design_total_pct"),
            "holdout": {"passes": ho["passes"], "total_pct": ho["total_pct"],
                        "rows": ho["rows"]},
            "params": params,
        })
        print(f"design {t.value:.1f} (passes {t.user_attrs.get('design_passes')}) -> holdout passes {ho['passes']} total {ho['total_pct']:+.2f}%", flush=True)

    results.sort(key=lambda r: -(r["design_value"] or 0))
    champion = results[0] if results else None
    champ_full = None
    if champion:
        full = eval_config(champion["params"], df_by, wins_by, design_ids, window_ids=None)
        print("\nCHAMPION full-20 scorecard:")
        for r in full["rows"]:
            print(f"  W{r['wid']:02d} roi {r['roi']:+7.2f}% dd {r['dd']:5.2f}% n {r['n']:>3d} wr {r['wr']:5.1f}% {'PASS' if r['pass'] else ''}")
        print(f"  TOTAL {full['total_pct']:+.2f}% | passes {full['passes']}/20")
        # null: matched counts random subsets at champion gates
        full_counts = full["counts"]
        rng = np.random.default_rng(31337)
        sims = np.empty(300)
        params = champion["params"]
        for s in range(300):
            tot = 0.0
            mask_list = drv.apply_config(wins_by[params["profile"]], params)
            for i, W in enumerate(wins_by[params["profile"]]):
                m = mask_list[i]
                cnt = full_counts[i]
                idx = np.flatnonzero(m)
                if len(idx) == 0 or cnt == 0:
                    continue
                pick = rng.choice(idx, size=min(cnt, len(idx)), replace=False)
                m2 = np.zeros_like(m)
                m2[pick] = True
                pnl, roi, dd, n, wr = drv.execute_window(W, m2, params["book"], params["dir_max"],
                                                         params["daily_cap"], params["risk"], params["dd_def"])
                tot += pnl
            sims[s] = tot / drv.CAPITAL * 100
        p_ge = float((sims >= full["total_pct"]).mean())
        print(f"[champion null] median {np.median(sims):+.2f}% p95 {np.quantile(sims,0.95):+.2f}% P(null>=champ)= {p_ge:.3f}")
        champ_full = {"rows": full["rows"], "total_pct": full["total_pct"],
                      "passes": full["passes"],
                      "null": {"median": float(np.median(sims)),
                               "p95": float(np.quantile(sims, 0.95)),
                               "P_null_ge_observed": p_ge}}
    OUT.write_text(json.dumps({"design_dist": design_dist, "top_design": results,
                               "champion_full": champ_full}, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
