"""stage6_breadth.py — 'harvest' deployment: diversified tail-capture, no ML.

Rationale (evidence-backed): the weekly-trend pool's edge lives in its fat right
tail (+5..15R winners ~ 5-8% of trades). ML cherry-picking is anti-predictive on
this pool (RC: selection < random-ranking median). The robust monetization is
BREADTH: take every causally-gated candidate under a hard book/risk budget.

Policy (strictly causal):
  per window k:
    fam gate = trailing 60d train expectancy > 0 (fallback top-3 by trail mean)
    execute ALL gated candidates in time order
    book cap BOOK, one open position per symbol
    flat $40 risk; optional dd-defense $20 overlay (variant B)
  report per-window table AND continuous-equity (real live deployment) stats.

Null: per window, sample a random subset of the SAME candidate set (same count
as executed breadth trades) executed under identical policy; 300 sims.
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
sys.path.insert(0, str(REPO))

PROFILE = os.environ.get("PROFILE", "maker25")
BOOK = int(os.environ.get("BOOK", "5"))
UNION = REPO / "scratch" / f"union_pool_v2_{PROFILE}.parquet"
WINDOWS_PATH = REPO / "Engine" / "oos_windows_20.json"
OUT = REPO / "scratch" / "ml_reversal_results" / f"stage6_breadth_{PROFILE}_b{BOOK}.json"
PURGE_MS = 72 * 3600 * 1000
CAPITAL = 5000.0
TRAIL_DAYS = 60
GEOMIN = 2  # weekly/survivor families only (geo_id>=2)


def execute(sel_order, tt, rr, bars, syms, book, dd_defense=None, sides=None, dir_max=0):
    open_pos = []
    equity, peak, cur_dd = CAPITAL, CAPITAL, 0.0
    pnl = 0.0
    wins = 0
    n = 0
    curve = []
    taken_idx = []
    for k in sel_order:
        t_entry = tt[k]
        open_pos = [op for op in open_pos if op[0] > t_entry]
        if syms[k] in [op[1] for op in open_pos]:
            continue
        if len(open_pos) >= book:
            continue
        if dir_max and sides is not None:
            sd = sides[k]
            if sum(1 for op in open_pos if op[2] == sd) >= dir_max:
                continue
        open_pos.append((t_entry + int(bars[k]) * 900_000, syms[k], sides[k] if sides is not None else 0))
        risk = 20.0 if (dd_defense is not None and cur_dd >= dd_defense) else 40.0
        p = rr[k] * risk
        pnl += p
        equity += p
        peak = max(peak, equity)
        cur_dd = max(cur_dd, (peak - equity) / peak * 100)
        wins += int(rr[k] > 0)
        n += 1
        curve.append(p)
        taken_idx.append(k)
    roi = pnl / CAPITAL * 100
    wr = wins / n * 100 if n else 0.0
    return pnl, roi, cur_dd, n, wr, np.array(curve), np.array(taken_idx)


def window_frames(big):
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)
    frames = []
    for w in windows:
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        cutoff = start_ms - PURGE_MS
        trail0 = cutoff - TRAIL_DAYS * 86_400_000
        train = big[(big.t < cutoff)]
        tr_trail = train[train.t >= trail0]
        test = big[(big.t >= start_ms) & (big.t <= end_ms)].reset_index(drop=True)
        fam_mean = tr_trail.groupby("fam")["r"].mean()
        ok = set(fam_mean[fam_mean > 0].index)
        if len(ok) < 3:
            ok = set(fam_mean.sort_values(ascending=False).head(3).index)
        frames.append((w, test, ok))
    return frames


def run_breadth(frames, dd_defense=None):
    rows = []
    total = 0.0
    passes = 0
    all_taken = []
    for w, test, ok in frames:
        w_id, w_name = w["window_id"], w["name"]
        t2 = test[test.fam.isin(ok)].reset_index(drop=True)
        if len(t2) == 0:
            rows.append({"window_id": w_id, "name": w_name, "trades": 0, "win_rate": 0,
                         "pnl_usd": 0, "roi_pct": 0, "max_dd_pct": 0, "status": "CASH"})
            continue
        sel = np.argsort(t2["t"].to_numpy())
        pnl, roi, dd, n, wr, curve, taken = execute(sel, t2["t"].to_numpy(), t2["r"].to_numpy(),
                                                    t2["bars"].to_numpy(), t2["sym"].to_numpy(),
                                                    BOOK, dd_defense, t2["side"].to_numpy(), DIR_MAX)
        okpass = roi >= 10.0 and dd <= 5.0 and wr >= 40.0 and n >= 15
        passes += int(okpass)
        total += pnl
        all_taken.append((w_id, len(t2), taken))
        rows.append({"window_id": w_id, "name": w_name, "candidates": int(len(t2)),
                     "trades": n, "win_rate": wr, "pnl_usd": pnl, "roi_pct": roi,
                     "max_dd_pct": dd, "status": "PASS" if okpass else "FAIL",
                     "ok_fams": sorted(ok)})
    return rows, total, passes, all_taken


def continuous_run(big, frames):
    """Real live deployment: one continuous book across the whole OOS period."""
    segs = []
    for w, test, ok in frames:
        t2 = test[test.fam.isin(ok)]
        if len(t2):
            segs.append(t2)
    full = pd.concat(segs, ignore_index=True).sort_values("t").reset_index(drop=True)
    tt = full["t"].to_numpy()
    rr = full["r"].to_numpy()
    bars = full["bars"].to_numpy()
    syms = full["sym"].to_numpy()
    sel = np.arange(len(full))
    open_pos = []
    equity, peak, maxdd = CAPITAL, CAPITAL, 0.0
    pnl = 0.0
    n = 0
    wins = 0
    monthly = {}
    for k in sel:
        open_pos = [op for op in open_pos if op[0] > tt[k]]
        if syms[k] in [op[1] for op in open_pos]:
            continue
        if len(open_pos) >= BOOK:
            continue
        if DIR_MAX:
            sd = full["side"].to_numpy()[k]
            if sum(1 for op in open_pos if op[2] == sd) >= DIR_MAX:
                continue
        open_pos.append((tt[k] + int(bars[k]) * 900_000, syms[k], full["side"].to_numpy()[k]))
        p = rr[k] * 40.0
        pnl += p
        equity += p
        peak = max(peak, equity)
        maxdd = max(maxdd, (peak - equity) / peak * 100)
        wins += int(rr[k] > 0)
        n += 1
        m = pd.to_datetime(tt[k], unit="ms", utc=True).strftime("%Y-%m")
        monthly[m] = monthly.get(m, 0.0) + p
    return {"trades": n, "win_rate": wins / n * 100 if n else 0,
            "total_pnl": pnl, "total_roi_pct": pnl / CAPITAL * 100,
            "max_dd_pct": maxdd, "months": len(monthly),
            "avg_monthly_roi_pct": pnl / CAPITAL / max(len(monthly), 1) * 100,
            "positive_months": sum(1 for v in monthly.values() if v > 0)}


def null_sims(frames, exec_counts, sims=300, seed=99):
    rng = np.random.default_rng(seed)
    sim_total = np.empty(sims)
    for s in range(sims):
        tot = 0.0
        for (w, test, ok), cnt in zip(frames, exec_counts):
            t2 = test[test.fam.isin(ok)].reset_index(drop=True)
            if cnt == 0 or len(t2) == 0:
                continue
            idx = rng.choice(len(t2), size=min(cnt, len(t2)), replace=False)
            idx = idx[np.argsort(t2["t"].to_numpy()[idx])]
            pnl, roi, dd, n, wr, _, _ = execute(idx, t2["t"].to_numpy(), t2["r"].to_numpy(),
                                                t2["bars"].to_numpy(), t2["sym"].to_numpy(),
                                                BOOK, None)
            tot += pnl
        sim_total[s] = tot / CAPITAL * 100
    return sim_total


def btc_trend_series():
    df = pd.read_parquet(REPO / "Engine" / "binance_backtesting_data" / "BTCUSDT_15m_master_2020_2026.parquet",
                         columns=["open_time_ms", "close"])
    r = df["close"].pct_change(672)
    return pd.Series(r.to_numpy(), index=df["open_time_ms"].to_numpy())

def apply_tide_guard(test, btc_r672):
    """Causal beta overlay: longs only when BTC 7d-trend > 0, shorts only when < 0."""
    tr = np.sign(test["t"].map(btc_r672).fillna(0).to_numpy())
    keep = (test["side"].to_numpy() == np.where(tr >= 0, 1, -1))
    return test[keep].reset_index(drop=True)

TIDE_GUARD = int(os.environ.get("TIDE_GUARD", "0"))
DIR_MAX = int(os.environ.get("DIR_MAX", "0"))

def main():
    t0 = time.perf_counter()
    big = pd.read_parquet(UNION)
    big = big[big.geo_id >= GEOMIN].reset_index(drop=True)
    frames = window_frames(big)
    if TIDE_GUARD:
        btc = btc_trend_series()
        frames = [(w, apply_tide_guard(test, btc), ok) for (w, test, ok) in frames]
        cand = sum(len(t) for _, t, _ in frames)
        print(f"[guard] tide-overlay candidate total: {cand}", flush=True)

    rowsA, totalA, passA, takenA = run_breadth(frames, dd_defense=None)
    rowsB, totalB, passB, _ = run_breadth(frames, dd_defense=3.0)
    cont = continuous_run(big, frames)

    print(f"{'W#':<3} | {'cands':<6} | {'trades':<6} | {'WR':<6} | {'PnL':<11} | {'ROI':<8} | {'DD':<6} | {'st':<5}", flush=True)
    for r in rowsA:
        print(f"W{r['window_id']:02d} | {r.get('candidates', 0):<6d} | {r['trades']:<6d} | {r['win_rate']:>5.1f}% | {r['pnl_usd']:>+9.2f} USD | {r['roi_pct']:>+6.2f}% | {r['max_dd_pct']:>5.2f}% | {r['status']:<5}", flush=True)
    print(f"== BREADTH A (flat $40, no defense): total {totalA:+.2f} USD ({totalA/CAPITAL*100:+.2f}%) | pass {passA}/20")
    print(f"== BREADTH B (dd-defense 3% -> $20): total {totalB:+.2f} USD ({totalB/CAPITAL*100:+.2f}%) | pass {passB}/20")
    print(f"== CONTINUOUS live-equivalent: {json.dumps(cont, indent=1)}")
    cnts = [len(t) for _, _, t in takenA]
    sim_total = null_sims(frames, cnts)
    p_obs = float((sim_total >= totalA / CAPITAL * 100).mean())
    print(f"[Null matched-count x300] median {np.median(sim_total):+.2f}% | p95 {np.quantile(sim_total, 0.95):+.2f}% | P(null >= breadth {totalA/CAPITAL*100:+.2f}%) = {p_obs:.3f}")
    if not OUT.parent.exists():
        OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "profile": PROFILE, "book": BOOK, "breadth_rows": rowsA, "total_usd": totalA,
        "total_pct": totalA / CAPITAL * 100, "passes": passA,
        "breadthB": {"total_usd": totalB, "total_pct": totalB / CAPITAL * 100, "passes": passB},
        "continuous": cont,
        "null": {"median": float(np.median(sim_total)), "p95": float(np.quantile(sim_total, 0.95)),
                 "p05": float(np.quantile(sim_total, 0.05)), "P_null_ge_observed": p_obs},
    }, indent=2))
    print(f"wrote {OUT} in {time.perf_counter()-t0:.0f}s")


if __name__ == "__main__":
    main()
