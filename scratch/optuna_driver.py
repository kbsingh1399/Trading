"""optuna_driver.py — 8h self-terminating Optuna hunt for the 20-window criteria.

DISCIPLINE: objective uses DESIGN windows W01..W16 ONLY. W17..W20 never touch
the study. Holdout evaluation lives in validate_hunt.py (run after the hunt).
Causality: 72h purge inside ML mode; trailing-window family gates; no snooping.

Rounds: 50,100,200,400,800,... until HUNT_SECONDS elapses (default 8h).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

WINDOWS_PATH = REPO / "Engine" / "oos_windows_20.json"
CAPITAL = 5000.0
PURGE_MS = 72 * 3600 * 1000
HUNT_SECONDS = int(float(os.environ.get("HUNT_HOURS", "8")) * 3600)
HUNT_DIR = REPO / "scratch" / os.environ.get("HUNT_DIR_NAME", "hunt")
DB = "sqlite:///" + str(HUNT_DIR / "optuna_hunt.db")

GEOS_SURV = ["SURV_W", "SURV_L", "SURV_XL"]
TAGS = ["T1__donchW_tide", "T1__donchW_free", "T2__tsmom7d", "T2__tsmom7d_hi15",
        "T3__pullback_M", "T3__pullback_W", "T6__xs_decile"]
FAM_OF = {"T1__donchW_tide": "T1", "T1__donchW_free": "T1", "T2__tsmom7d": "T2",
          "T2__tsmom7d_hi15": "T2", "T3__pullback_M": "T3M", "T3__pullback_W": "T3W",
          "T6__xs_decile": "T6"}
GEO_CHOICE_FAMS = ["T1", "T2", "T3W", "T6"]
ML_FEATS = ["vwap_zscore", "rsi_14", "atr_ratio", "volume_ratio", "tide", "hour",
            "dow", "mom_3d", "ret_672", "dist90hi", "ret_1344", "r7_z", "xs_rank",
            "side", "geo_id"]

WINDOWS = []


def load_windows():
    global WINDOWS
    with open(WINDOWS_PATH) as f:
        ws = json.load(f)
    out = []
    for w in ws:
        s = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        e = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        out.append((w["window_id"], w["name"], s, e))
    WINDOWS = out
    return out


def slices_for(profile, windows):
    df = pd.read_parquet(REPO / "scratch" / f"variant_pool_{profile}.parquet")
    df = df[df.geo.isin(GEOS_SURV + ["SURV_M"])].reset_index(drop=True)
    keys = (df["fam"] + "__" + df["tag"]).to_numpy()
    geo = df["geo"].to_numpy()
    t = df["t"].to_numpy()
    r = df["r"].to_numpy()
    bars = df["bars"].to_numpy()
    side = df["side"].to_numpy().astype(np.int8)
    sym_codes, _ = pd.factorize(df["sym"])
    btc = pd.read_parquet(REPO / "Engine" / "binance_backtesting_data" / "BTCUSDT_15m_master_2020_2026.parquet",
                          columns=["open_time_ms", "close"])
    bidx = btc["open_time_ms"].to_numpy()
    bclose = btc["close"].to_numpy(dtype=float)
    btc_r672 = bclose / np.roll(bclose, 672) - 1.0
    btc_r672[:672] = np.nan
    btc_sig = btc_r672.copy()
    roll = pd.Series(btc_r672).rolling(672 * 4, min_periods=672).std().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        btc_sig = btc_r672 / roll
    per_w = []
    for (wid, name, s, e) in windows:
        m = (t >= s) & (t <= e)
        bt = btc_r672
        pos = np.searchsorted(bidx, t[m], side="right") - 1
        ok = pos >= 0
        pos = np.clip(pos, 0, len(bt) - 1)
        bv = np.where(ok, bt[pos], 0.0)
        bs = btc_sig
        bv2 = np.where(ok, bs[pos], 0.0)
        bv2 = np.where(np.isnan(bv2), 0.0, bv2)
        bv = np.where(np.isnan(bv), 0.0, bv)
        mlcols = {c: df[c].to_numpy()[m] for c in ML_FEATS}
        per_w.append(dict(wid=wid, t=t[m], r=r[m], bars=bars[m], side=side[m],
                          sym=sym_codes[m], keys=keys[m], geo=geo[m],
                          btc_r=bv, btc_sig=bv2, ml=mlcols))
    return df, per_w


def apply_config(per_w, params):
    active = {}
    for tg in TAGS:
        if params.get("on_" + tg, 1):
            active[tg] = params["geo_" + FAM_OF[tg]] if FAM_OF[tg] in GEO_CHOICE_FAMS else "SURV_M"
    if len(active) < 2:
        return None
    allowed = set(active.items())
    tide_on = params.get("tide_on", 1)
    tide_min = params.get("tide_min_sig", 0.0)
    out = []
    for W in per_w:
        m = np.array([(k, g) in allowed for k, g in zip(W["keys"], W["geo"])])
        if tide_on:
            bs = W["btc_sig"]
            tr = np.where(bs >= tide_min, 1, np.where(bs <= -tide_min, -1, 0))
            m &= (W["side"] == tr)
        out.append(m)
    return out


def execute_window(W, mask, book, dir_max, daily_cap, risk, dd_def):
    idx = np.flatnonzero(mask)
    if len(idx) == 0:
        return 0.0, 0.0, 0.0, 0, 0.0
    tt = W["t"][idx]
    rr = W["r"][idx]
    bars = W["bars"][idx]
    side = W["side"][idx]
    sym = W["sym"][idx]
    order = np.arange(len(idx))
    if daily_cap:
        days = tt // 86_400_000
        seen = {}
        keep = []
        for k in order:
            d = int(days[k])
            c = seen.get(d, 0)
            if c < daily_cap:
                keep.append(k)
                seen[d] = c + 1
        order = np.array(sorted(keep))
    open_t = []
    open_s = []
    open_d = []
    equity = CAPITAL
    peak = CAPITAL
    dd = 0.0
    pnl = 0.0
    wins = 0
    n = 0
    for k in order:
        live = [i2 for i2 in range(len(open_t)) if open_t[i2] > tt[k]]
        open_t = [open_t[i2] for i2 in live]
        open_s = [open_s[i2] for i2 in live]
        open_d = [open_d[i2] for i2 in live]
        if sym[k] in open_s:
            continue
        if len(open_t) >= book:
            continue
        if dir_max and sum(1 for d in open_d if d == side[k]) >= dir_max:
            continue
        open_t.append(int(tt[k]) + int(bars[k]) * 900_000)
        open_s.append(int(sym[k]))
        open_d.append(int(side[k]))
        rk = 20.0 if (dd_def and dd >= dd_def) else float(risk)
        p = float(rr[k]) * rk
        pnl += p
        equity += p
        peak = max(peak, equity)
        dd = max(dd, (peak - equity) / peak * 100.0)
        wins += int(rr[k] > 0)
        n += 1
    roi = pnl / CAPITAL * 100.0
    wr = wins / n * 100.0 if n else 0.0
    return pnl, roi, dd, n, wr


def ml_scores(trd, W):
    import lightgbm as lgb
    from sklearn.ensemble import ExtraTreesClassifier
    Xtr = trd[ML_FEATS]
    yreg = np.clip(trd["r"].to_numpy(), -1.6, 8.0)
    ycls = (trd["r"] > 0).astype(int)
    reg = lgb.LGBMRegressor(n_estimators=120, max_depth=3, learning_rate=0.05,
                            subsample=0.8, colsample_bytree=0.8, random_state=13,
                            verbose=-1, n_jobs=2)
    clf = lgb.LGBMClassifier(n_estimators=120, max_depth=3, learning_rate=0.05,
                             subsample=0.8, colsample_bytree=0.8, random_state=13,
                             verbose=-1, n_jobs=2)
    et = ExtraTreesClassifier(n_estimators=80, max_depth=6, n_jobs=2, random_state=13)
    reg.fit(Xtr, yreg)
    clf.fit(Xtr, ycls)
    et.fit(Xtr, ycls)
    Xte = pd.DataFrame({c: W["ml"][c] for c in ML_FEATS})
    z = (reg.predict(Xte) - reg.predict(Xtr).mean()) / (reg.predict(Xtr).std() + 1e-9)
    return z + 1.5 * (clf.predict_proba(Xte)[:, 1] - 0.5) + 1.5 * (et.predict_proba(Xte)[:, 1] - 0.5)


def objective_factory(df_by, wins_by, design_ids):
    def objective(trial):
        profile = trial.suggest_categorical("profile", ["taker41", "maker25"])
        mode = trial.suggest_categorical("mode", ["breadth", "ml"])
        for tg in TAGS:
            trial.suggest_categorical("on_" + tg, [0, 1])
        if sum(trial.params["on_" + tg] for tg in TAGS) < 2:
            raise optuna.TrialPruned("need >=2 tags")
        for f in GEO_CHOICE_FAMS:
            trial.suggest_categorical("geo_" + f, GEOS_SURV)
        trial.suggest_categorical("tide_on", [0, 1])
        trial.suggest_categorical("tide_min_sig", [0.0, 0.25, 0.5])
        trail_days = trial.suggest_categorical("trail_days", [0, 30, 60, 90])
        gate_min = trial.suggest_categorical("gate_min", [-0.05, 0.0, 0.02])
        fb_k = trial.suggest_categorical("fb_k", [2, 3, 4])
        book = trial.suggest_categorical("book", [4, 5, 6, 8])
        dir_max = trial.suggest_categorical("dir_max", [0, 1, 2, 3])
        daily_cap = trial.suggest_categorical("daily_cap", [0, 1, 2])
        risk = trial.suggest_categorical("risk", [40.0, 50.0, 60.0])
        dd_def = trial.suggest_categorical("dd_def", [0.0, 1.5, 2.5, 3.5])
        ml_q = None
        if mode == "ml":
            ml_q = trial.suggest_categorical("ml_q", [0.55, 0.65, 0.75, 0.85])

        df = df_by[profile]
        per_w = wins_by[profile]
        mask_list = apply_config(per_w, trial.params)
        if mask_list is None:
            raise optuna.TrialPruned("no tags")

        total = 0.0
        passes = 0
        rois = []
        dd_pen = 0.0
        posw = 0
        for i, W in enumerate(per_w):
            if W["wid"] not in design_ids:
                continue
            m = mask_list[i].copy()
            w_s = WINDOWS[W["wid"] - 1][2]
            if trail_days:
                cutoff = w_s - PURGE_MS
                t0 = cutoff - trail_days * 86_400_000
                tr = df[(df.t >= t0) & (df.t < cutoff)]
                if len(tr):
                    kk = (tr["fam"] + "__" + tr["tag"])
                    gm = tr.groupby(kk)["r"].mean()
                    ok = set(gm[gm > gate_min].index)
                    if len(ok) < fb_k:
                        ok = set(gm.sort_values(ascending=False).head(fb_k).index)
                    m &= np.array([k in ok for k in W["keys"]])
            if m.sum() == 0:
                rois.append(0.0)
                continue
            if mode == "ml":
                cutoff = w_s - PURGE_MS
                pairset = set(zip(W["keys"][m], W["geo"][m]))
                kk = (df["fam"] + "__" + df["tag"]).to_numpy()
                gg = df["geo"].to_numpy()
                trm = (df.t.to_numpy() < cutoff) & np.array([(k, g) in pairset for k, g in zip(kk, gg)])
                trd = df[trm]
                if len(trd) > 40000:
                    trd = trd.sample(40000, random_state=13)
                if len(trd) >= 800:
                    try:
                        s_all = ml_scores(trd, W)
                        q = float(np.quantile(s_all, ml_q))
                        idxm = np.flatnonzero(m)
                        keep = idxm[s_all[idxm] >= q]
                        nm = np.zeros_like(m)
                        nm[keep] = True
                        m = nm
                    except Exception:
                        pass
            pnl, roi, dd, n, wr = execute_window(W, m, book, dir_max, daily_cap, risk, dd_def)
            total += pnl
            rois.append(min(roi, 15.0))
            dd_pen += max(0.0, dd - 8.0)
            posw += int(roi > 0)
            if roi >= 10.0 and dd <= 5.0 and wr >= 40.0 and n >= 15:
                passes += 1
        score = 100.0 * passes + 0.5 * (total / CAPITAL * 100) + 0.25 * float(np.mean(rois)) + 0.05 * posw - 0.25 * dd_pen
        trial.set_user_attr("design_passes", passes)
        trial.set_user_attr("design_total_pct", total / CAPITAL * 100)
        trial.set_user_attr("design_pos_windows", posw)
        return score
    return objective


def main():
    HUNT_DIR.mkdir(parents=True, exist_ok=True)
    start_file = HUNT_DIR / "start_ts.txt"
    if start_file.exists():
        t_start = float(start_file.read_text().strip())
    else:
        t_start = time.time()
        start_file.write_text(str(t_start))
    deadline = t_start + HUNT_SECONDS
    print(f"[hunt] deadline in {(deadline - time.time()) / 3600:.2f}h", flush=True)

    wins = load_windows()
    design_ids = [w[0] for w in wins if w[0] <= 16]
    print(f"[hunt] design {len(design_ids)} windows; holdout sealed: {[w[0] for w in wins if w[0] > 16]}", flush=True)

    df_by = {}
    wins_by = {}
    for prof in ("taker41", "maker25"):
        df, per_w = slices_for(prof, wins)
        df_by[prof] = df
        wins_by[prof] = per_w
        print(f"[hunt] {prof}: {len(df):,d} rows", flush=True)

    obj = objective_factory(df_by, wins_by, design_ids)
    study = optuna.create_study(study_name="hunt20", storage=DB, direction="maximize",
                                load_if_exists=True,
                                sampler=optuna.samplers.TPESampler(seed=2026, multivariate=True))
    rnd = 0
    budget = 50
    while True:
        remaining = deadline - time.time()
        if remaining < 60:
            break
        print(f"[hunt] round {rnd}: {budget} trials | elapsed {(time.time() - t_start) / 3600:.2f}h", flush=True)
        try:
            study.optimize(obj, n_trials=budget, timeout=remaining, gc_after_trial=True, show_progress_bar=False)
        except Exception as e:
            print(f"[hunt] round {rnd} error: {e}", flush=True)
        comp = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
        if comp:
            best = study.best_trial
            snap = {"round": rnd, "trials": len(comp), "best_value": best.value,
                    "best_params": best.params,
                    "design_passes": best.user_attrs.get("design_passes"),
                    "design_total_pct": best.user_attrs.get("design_total_pct"),
                    "elapsed_h": (time.time() - t_start) / 3600}
            (HUNT_DIR / "best_snapshot.json").write_text(json.dumps(snap, indent=2))
            print(f"[hunt] r{rnd}: best {best.value:.2f} | passes {snap['design_passes']} | total {len(comp)}", flush=True)
        rnd += 1
        budget *= 2
    comp_total = len([t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE])
    (HUNT_DIR / "DONE").write_text(f"finished {time.ctime()} after {comp_total} trials")
    print(f"[hunt] DEADLINE reached — {comp_total} trials. Run validate_hunt.py", flush=True)


if __name__ == "__main__":
    main()
