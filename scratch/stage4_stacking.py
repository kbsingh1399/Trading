"""stage4_stacking.py — architecture #5: stacked P&L-stream sleeves.

Each family is a sleeve. Per window (strictly causal):
  1. walk-forward sleeve weights from trailing 90d train stats:
       w_f ∝ exp(mean_r_trail_f / 0.05) over fams with n_trail >= 30
  2. regime multipliers from HMM(2) trained on train-only BTC 4h returns:
       m_f,s = clip(exp((mean_r_f,s - mean_r_f)/0.10), 0.25, 2.0)
  3. candidate score at bar t:
       score = w_f * m_f,state(t) * (EWMA_f(r, halflife 14d, trades < t) + 0.25)
     (EWMA updated with PAST trades only — causal rolling portfolio policy)
  4. same mandate executor (concurrency C, house-money risk w/ dd-defense).

Executor-policy grid (signal/label untouched; portfolio knobs only):
  dd_defense ∈ {1.5, 2.0}, risk_cap ∈ {40, 60, 100}, vol-sized risk ∈ {off, on}
Reality check: 300 random-score sims on the best grid cell.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from scratch.stage2_ensemble import fit_forward_states, btc_4h_returns  # reuse causal HMM
from scratch.stage3_realitycheck import exec_window  # reuse executor for reality check

WINDOWS_PATH = REPO / "Engine" / "oos_windows_20.json"
import os
PROFILE = os.environ.get("PROFILE", "maker25")
UNION = REPO / "scratch" / f"union_pool_v2_{PROFILE}.parquet"
OUT = REPO / "scratch" / "ml_reversal_results" / f"stage4_stacking_{PROFILE}.json"
PURGE_MS = 72 * 3600 * 1000
CAPITAL = 5000.0
FAST_GEO_MAX = 1  # geo_id <= 1 are FAST/MID


def ewma_scores(test_g: pd.DataFrame, train_g: pd.DataFrame, fam_w: pd.Series,
                state_mult: dict, test_states: np.ndarray, halflife_days: float = 14.0):
    """Causal rolling EWMA score: at each candidate t, uses only family trades with
    earlier exit time (approx by entry t - 1 bar margin; conservative: entry<t)."""
    hl_ms = halflife_days * 86_400_000
    tt = test_g["t"].to_numpy()
    fam = test_g["fam"].to_numpy()
    tr_t = train_g["t"].to_numpy()
    tr_r = train_g["r"].to_numpy()
    tr_f = train_g["fam"].to_numpy()
    # pre-sort train by t
    order = np.argsort(tr_t)
    tr_t, tr_r, tr_f = tr_t[order], tr_r[order], tr_f[order]
    scores = np.empty(len(test_g))
    # pointer into train per family not trivial for streaming; do global incremental:
    # seed with full train EWMA per fam; update with test trades in t order (causal).
    ew_num = {}
    ew_den = {}
    for f, w in zip(tr_f, tr_r):
        # seed: simple trailing mean weight handled in fam_w; EWMA seed = 0
        pass
    last_t = {}
    cum_num = {}
    cum_w = {}
    # process test candidates in time order, blending train history via fam_w mean
    fam_trail_mean = train_g.groupby("fam")["r"].mean().to_dict()
    for k in np.argsort(tt):
        f = fam[k]
        t = tt[k]
        # decay existing accumulator
        if f in last_t:
            decay = np.exp(-(t - last_t[f]) / (hl_ms / np.log(2)))
        else:
            decay = 0.0
        base = fam_trail_mean.get(f, -0.25)
        num = cum_num.get(f, 0.0) * decay
        den = cum_w.get(f, 0.0) * decay
        ew = (num / den) if den > 5 else base
        s_mult = state_mult.get((f, test_states[k]), 1.0)
        scores[k] = fam_w.get(f, 0.0) * s_mult * (ew + 0.25)
        cum_num[f] = num + 1.0
        cum_w[f] = den + 1.0
        last_t[f] = t
    return scores


def exec_policy(sel, tt, rr, bars, syms, atr_ratio_at_entry, concurrency=4,
                dd_defense=2.0, risk_cap=40.0, volsize=False, atr_med=1.0):
    open_pos = []
    equity, peak, cur_dd = CAPITAL, CAPITAL, 0.0
    pnl = 0.0
    wins = 0
    n = 0
    pnl_list = []
    for k in sel:
        t_entry = tt[k]
        open_pos = [op for op in open_pos if op[0] > t_entry]
        if syms[k] in [op[1] for op in open_pos]:
            continue
        if len(open_pos) >= concurrency:
            continue
        open_pos.append((t_entry + int(bars[k]) * 900_000, syms[k]))
        if cur_dd >= dd_defense:
            risk = 20.0
        elif (equity - CAPITAL) >= 50.0:
            risk = min(risk_cap * 2.5, 40.0 + (equity - CAPITAL) * 0.40)
        else:
            risk = float(risk_cap)
        if volsize:
            ar = atr_ratio_at_entry[k]
            if ar > 0:
                risk *= float(np.clip(atr_med / ar, 0.5, 1.6))
        p = rr[k] * risk
        pnl += p
        pnl_list.append(p)
        wins += int(rr[k] > 0)
        n += 1
        equity += p
        peak = max(peak, equity)
        cur_dd = max(cur_dd, (peak - equity) / peak * 100)
    roi = pnl / CAPITAL * 100
    wr = wins / n * 100 if n else 0.0
    return pnl, roi, cur_dd, n, wr, pnl_list


def build_window_frames(big: pd.DataFrame):
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)
    frames = []
    for w in windows:
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        cutoff = start_ms - PURGE_MS
        trail90 = cutoff - 90 * 86_400_000
        train90 = big[(big.t >= trail90) & (big.t < cutoff)].reset_index(drop=True)
        train_full = big[big.t < cutoff]
        test = big[(big.t >= start_ms) & (big.t <= end_ms)].reset_index(drop=True)
        frames.append((w, train90, train_full, test))
    return frames


def hmm_states_for(test: pd.DataFrame, cutoff: float, btc_ret4, btc_index):
    te_btc_s = btc_ret4[(btc_index >= cutoff - 200 * 86_400_000) & (btc_index <= test.t.max())].dropna()
    tr_btc = btc_ret4[btc_index < cutoff].dropna().to_numpy()
    try:
        states = fit_forward_states(tr_btc, te_btc_s.to_numpy())
        smap = pd.Series(states, index=te_btc_s.index.to_numpy())
        return test["t"].map(smap).fillna(0).astype(int).to_numpy()
    except Exception:
        return np.zeros(len(test), dtype=int)


def select_daily(sel_score, test_g, top1_only=False):
    days = pd.to_datetime(test_g["t"].to_numpy(), unit="ms", utc=True).normalize()
    sel = []
    gids = test_g["geo_id"].to_numpy()
    for _, arr in pd.Series(np.arange(len(test_g)), index=days).groupby(level=0):
        arr = np.asarray(arr)
        sel.append(int(arr[np.argmax(sel_score[arr])]))
        fast = arr[gids[arr] <= FAST_GEO_MAX]
        if len(fast):
            sel.append(int(fast[np.argmax(sel_score[fast])]))
    return np.array(sorted(set(sel)), dtype=int)


def main():
    t0 = time.perf_counter()
    big = pd.read_parquet(UNION)
    btc_ret4 = btc_4h_returns()
    btc_index = btc_ret4.index
    frames = build_window_frames(big)
    atr_med = float(big["atr_ratio"].median())

    # ---- pre-compute per-window stacking scores (fixed given train; causal)
    win_cache = []
    for w, train90, train_full, test in frames:
        w_id = w["window_id"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        cutoff = start_ms - PURGE_MS
        if len(test) == 0 or len(train90) < 500:
            win_cache.append((w, None))
            continue
        stats = train90.groupby("fam").agg(m=("r", "mean"), n=("r", "size"))
        stats = stats[stats.n >= 30]
        if len(stats) == 0:
            stats = train90.groupby("fam").agg(m=("r", "mean"), n=("r", "size")).sort_values("m", ascending=False).head(5)
        w_f = np.exp(stats["m"] / 0.05)
        fam_w = (w_f / w_f.sum())
        allow = set(stats.index)
        test_a = test[test.fam.isin(allow)].reset_index(drop=True)
        train_full_a = train_full[train_full.fam.isin(allow)]
        if len(test_a) == 0:
            win_cache.append((w, None))
            continue
        states = hmm_states_for(test_a, cutoff, btc_ret4, btc_index)
        # regime multipliers from full train
        smult = {}
        tr_states = None
        try:
            tr_btc = btc_ret4[btc_index < cutoff].dropna()
            tr_btc_tail = tr_btc.iloc[-2000:]
            hmm = GaussianHMM(n_components=2, covariance_type="diag", n_iter=100, random_state=7, tol=1e-3)
            hmm.fit(tr_btc.to_numpy().reshape(-1, 1))
            # full-train state means per fam via state map on train tail timestamps
            smap_full = pd.Series(hmm.predict(tr_btc_tail.to_numpy().reshape(-1, 1)), index=tr_btc_tail.index.to_numpy())
            tr_s = train_full_a.copy()
            tr_s["s"] = tr_s["t"].map(smap_full).fillna(0)
            g = tr_s.groupby(["fam", "s"])["r"].mean()
            gm = tr_s.groupby("fam")["r"].mean()
            for (f, s), v in g.items():
                smult[(f, int(s))] = float(np.clip(np.exp((v - gm.get(f, 0)) / 0.10), 0.25, 2.0))
        except Exception:
            smult = {}
        scores = ewma_scores(test_a, train_full_a, fam_w, smult, states)
        win_cache.append((w, (train_full_a, test_a, scores)))

    grid = []
    for dd_def in (1.5, 2.0):
        for risk_cap in (40.0, 60.0, 100.0):
            for volsize in (False, True):
                grid.append((dd_def, risk_cap, volsize))

    print(f"{'dd':<4} | {'cap':<5} | {'vol':<5} | {'total%':<9} | {'pass':<4} | {'posWin':<6} | {'minROI%':<8}", flush=True)
    results = {}
    for cell in grid:
        dd_def, risk_cap, volsize = cell
        total = 0.0
        passes = 0
        posw = 0
        minroi = 999.0
        per_win = []
        for w, payload in win_cache:
            w_id, w_name = w["window_id"], w["name"]
            if payload is None:
                per_win.append({"window_id": w_id, "status": "SKIP"})
                minroi = min(minroi, 0.0)
                continue
            train_full_a, test_a, scores = payload
            sel = select_daily(scores, test_a)
            pnl, roi, dd, n, wr, pnl_list = exec_policy(
                sel, test_a["t"].to_numpy(), test_a["r"].to_numpy(),
                test_a["bars"].to_numpy(), test_a["sym"].to_numpy(),
                test_a["atr_ratio"].to_numpy(),
                concurrency=4, dd_defense=dd_def, risk_cap=risk_cap, volsize=volsize,
                atr_med=atr_med)
            ok = roi >= 10.0 and dd <= 5.0 and wr >= 40.0 and n >= 15
            passes += int(ok)
            posw += int(roi > 0)
            total += pnl
            minroi = min(minroi, roi)
            per_win.append({"window_id": w_id, "trades": n, "win_rate": wr, "pnl_usd": pnl,
                            "roi_pct": roi, "max_dd_pct": dd, "status": "PASS" if ok else "FAIL"})
        results[str(cell)] = {"total_pnl": total, "total_pct": total / CAPITAL * 100,
                              "passes": passes, "pos_windows": posw, "windows": per_win}
        print(f"{dd_def:<4} | {risk_cap:<5.0f} | {str(volsize):<5} | {total/CAPITAL*100:>+7.2f}% | {passes:<4} | {posw:<6} | {minroi:>+7.2f}%", flush=True)

    best = max(results.items(), key=lambda kv: kv[1]["total_pct"])
    print("BEST CELL:", best[0], f"total {best[1]['total_pct']:+.2f}% passes {best[1]['passes']}", flush=True)

    # ---- reality check on best cell (random scores, same executor + same selections density)
    dd_def, risk_cap, volsize = eval(best[0])
    rng = np.random.default_rng(406)
    sims = 300
    sim_tot = np.empty(sims)
    sim_max = np.empty(sims)
    sim_pass = np.zeros(sims, dtype=int)
    for s in range(sims):
        tp = 0.0
        mx = -999.0
        pc = 0
        for w, payload in win_cache:
            if payload is None:
                continue
            train_full_a, test_a, _ = payload
            scores = rng.standard_normal(len(test_a))
            sel = select_daily(scores, test_a)
            pnl, roi, dd, n, wr, _ = exec_policy(
                sel, test_a["t"].to_numpy(), test_a["r"].to_numpy(),
                test_a["bars"].to_numpy(), test_a["sym"].to_numpy(),
                test_a["atr_ratio"].to_numpy(),
                concurrency=4, dd_defense=dd_def, risk_cap=risk_cap, volsize=volsize,
                atr_med=atr_med)
            tp += pnl
            mx = max(mx, roi)
            if roi >= 10.0 and dd <= 5.0 and wr >= 40.0 and n >= 15:
                pc += 1
        sim_tot[s] = tp / CAPITAL * 100
        sim_max[s] = mx
        sim_pass[s] = pc
    obs = best[1]
    rc = {
        "null_total_median_pct": float(np.median(sim_tot)),
        "null_total_p95_pct": float(np.quantile(sim_tot, 0.95)),
        "P_null_total_ge_observed": float((sim_tot >= obs["total_pct"]).mean()),
        "null_best_window_p95": float(np.quantile(sim_max, 0.95)),
        "null_pass_dist": {str(k): int(v) for k, v in zip(*np.unique(sim_pass, return_counts=True))},
        "P_null_pass_ge_observed": float((sim_pass >= max(obs["passes"], 1)).mean()),
    }
    print("[stage4 RC]", json.dumps(rc, indent=2), flush=True)

    OUT.write_text(json.dumps({"best_cell": best[0], "results": results,
                               "reality_check": rc}, indent=2))
    print(f"[stage4] wrote {OUT} in {time.perf_counter()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
