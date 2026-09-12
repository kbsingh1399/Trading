"""certify_bfield.py — certify a hunt champion on untouched B-field windows.

Usage: STUDY_TAG="_v3" .venv/bin/python -u scratch/certify_bfield.py

Loads the best trial of study "hunt20"+STUDY_TAG, evaluates it on every window in
Engine/oos_windows_bfield.json (months >15d clear of all W01-W20 windows; never
scored by any optimizer). Same rubric as validate_hunt.py: roi>=10, dd<=5, wr>=40, n>=15.
Every attempt is appended to scratch/hunt/certifications.jsonl (deflation log).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scratch"))

import optuna_driver as drv  # noqa: E402

BFIELD = REPO / "Engine" / "oos_windows_bfield.json"
STUDY_TAG = os.environ.get("STUDY_TAG", "")
PARAMS_ENV = os.environ.get("PARAMS_JSON", "")  # optional direct params JSON


def load_b_windows():
    ws = json.load(open(BFIELD))
    out = []
    for w in ws:
        s = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        e = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        out.append((w["window_id"], w["name"], s, e))
    return out


def champion():
    if PARAMS_ENV:
        d = json.load(open(PARAMS_ENV))
        return d["best_params"] if "best_params" in d else d, "params_file"
    db = "sqlite:///" + str(REPO / "scratch" / "hunt" / f"optuna_hunt{STUDY_TAG}.db")
    import optuna
    study = optuna.load_study(study_name="hunt20" + STUDY_TAG, storage=db)
    comp = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    best = max(comp, key=lambda t: t.value)
    return dict(best.params), f"hunt20{STUDY_TAG}#trial{best.number}"


def certify():
    params, src = champion()
    profile = params["profile"]
    b_wins = load_b_windows()
    df, per_w = drv.slices_for(profile, b_wins)
    print(f"[certify] {src} | profile={profile} mode={params.get('mode')} B windows={len(b_wins)}")
    mask_list = drv.apply_config(per_w, params)
    if mask_list is None:
        raise SystemExit("champion has <2 active tags")
    mode = params.get("mode", "breadth")
    trail_days = int(params.get("trail_days", 0))
    gate_min = float(params.get("gate_min", -0.05))
    fb_k = int(params.get("fb_k", 2))
    rows = []
    total = 0.0
    passes = 0
    for i, W in enumerate(per_w):
        m = mask_list[i].copy()
        w_s = b_wins[i][2]
        if trail_days:
            cutoff = w_s - drv.PURGE_MS
            t0 = cutoff - trail_days * 86_400_000
            tr = df[(df.t >= t0) & (df.t < cutoff)]
            if len(tr):
                kk = (tr["fam"] + "__" + tr["tag"])
                gm = tr.groupby(kk)["r"].mean()
                ok = set(gm[gm > gate_min].index)
                if len(ok) < fb_k:
                    ok = set(gm.sort_values(ascending=False).head(fb_k).index)
                m &= np.array([k in ok for k in W["keys"]])
        if mode == "ml" and m.sum() > 0:
            cutoff = w_s - drv.PURGE_MS
            pairset = set(zip(W["keys"][m], W["geo"][m]))
            kk = (df["fam"] + "__" + df["tag"]).to_numpy()
            gg = df["geo"].to_numpy()
            trm = (df.t.to_numpy() < cutoff) & np.array([(k, g) in pairset for k, g in zip(kk, gg)])
            trd = df[trm]
            if len(trd) > 25000:
                trd = trd.sample(12000, random_state=13)
            if len(trd) >= 800:
                try:
                    s_all = drv.ml_scores(trd, W)
                    q = float(np.quantile(s_all, float(params.get("ml_q", 0.65))))
                    idxm = np.flatnonzero(m)
                    keep = idxm[s_all[idxm] >= q]
                    nm = np.zeros_like(m)
                    nm[keep] = True
                    m = nm
                except Exception as e:
                    print("[certify] ml warn:", e)
        pnl, roi, dd, n, wr = drv.execute_window(W, m, params["book"], params["dir_max"],
                                                 params["daily_cap"], params["risk"], params["dd_def"])
        okpass = roi >= 10.0 and dd <= 5.0 and wr >= 40.0 and n >= 15
        passes += int(okpass)
        total += pnl
        rows.append({"wid": W["wid"], "start": pd.Timestamp(b_wins[i][2], unit="ms", tz="UTC").strftime("%Y-%m"),
                     "roi": round(roi, 2), "dd": round(dd, 2), "n": n, "wr": round(wr, 1), "pass": bool(okpass)})
        print(f"B{W['wid']:>2} {rows[-1]['start']}  roi {roi:+7.2f}%  dd {dd:5.2f}%  n {n:>3}  wr {wr:5.1f}%  {'PASS' if okpass else 'fail'}")
    res = {"source": src, "profile": profile, "mode": mode, "params": params,
           "passes": passes, "n_windows": len(b_wins),
           "total_pct": total / drv.CAPITAL * 100, "rows": rows}
    out = REPO / "scratch" / "hunt" / f"cert_bfield{STUDY_TAG or '_plain'}.json"
    out.write_text(json.dumps(res, indent=2))
    log = {"ts": time.time(), "source": src, "window_set": "B1-22",
           "passes": passes, "total_pct": res["total_pct"]}
    with open(REPO / "scratch" / "hunt" / "certifications.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")
    print(f"\n[certify] PASSES {passes}/{len(b_wins)} | total {res['total_pct']:+.1f}% | logged -> certifications.jsonl")


if __name__ == "__main__":
    certify()
