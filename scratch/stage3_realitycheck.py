"""stage3_realitycheck.py — multiple-testing deflation for the whole campaign.

Null model: identical executor & density policy (daily top-2, concurrency 4,
house-money risk) but candidate RANKING REPLACED BY RANDOM SCORES — i.e., "no
selection ability" benchmark over the same union pool, per the same 20 windows.
S sims → distribution of (a) total 20-window PnL, (b) max single-window ROI.

Compares against observed campaign results:
  v1 ensemble: W16 +10.49% window ROI (1/20 pass), total -54.25%
  v2 ensemble: W19 +12.93% window ROI (0/20),      total -41.41%

If max-window ROI under the null commonly exceeds +12.9%, the observed best
windows are attributable to chance within this pool, and the campaign's zero
passes are not evidence of an edge anywhere.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
WINDOWS_PATH = REPO / "Engine" / "oos_windows_20.json"
UNION = REPO / "scratch" / "union_pool_v2.parquet"
OUT = REPO / "scratch" / "ml_reversal_results" / "stage3_realitycheck.json"

CAPITAL = 5000.0
SIMS = 200


def exec_window(test_g, score, capital=CAPITAL):
    days = pd.to_datetime(test_g["t"].to_numpy(), unit="ms", utc=True).normalize()
    sel = []
    gids = test_g["geo_id"].to_numpy()
    for _, arr in pd.Series(np.arange(len(test_g)), index=days).groupby(level=0):
        arr = np.asarray(arr)
        sel.append(int(arr[np.argmax(score[arr])]))
        fast = arr[gids[arr] <= 1]
        if len(fast):
            sel.append(int(fast[np.argmax(score[fast])]))
    sel = np.array(sorted(set(sel)), dtype=int)
    tt = test_g["t"].to_numpy()
    rr = test_g["r"].to_numpy()
    bars = test_g["bars"].to_numpy()
    syms = test_g["sym"].to_numpy()
    open_pos = []
    equity, peak, cur_dd = capital, capital, 0.0
    pnl = 0.0
    wins = 0
    n = 0
    for k in sel:
        t_entry = tt[k]
        open_pos = [op for op in open_pos if op[0] > t_entry]
        if syms[k] in [op[1] for op in open_pos]:
            continue
        if len(open_pos) >= 4:
            continue
        open_pos.append((t_entry + int(bars[k]) * 900_000, syms[k]))
        r_gain = rr[k]
        if cur_dd >= 2.0:
            risk = 20.0
        elif (equity - capital) >= 50.0:
            risk = min(100.0, 40.0 + (equity - capital) * 0.40)
        else:
            risk = 40.0
        p = r_gain * risk
        pnl += p
        wins += int(r_gain > 0)
        n += 1
        equity += p
        peak = max(peak, equity)
        cur_dd = max(cur_dd, (peak - equity) / peak * 100)
    return pnl, pnl / capital * 100, cur_dd, n, (wins / n * 100 if n else 0.0)


def main():
    t0 = time.perf_counter()
    big = pd.read_parquet(UNION)
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)
    # pre-slice windows
    win_data = []
    for w in windows:
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        test = big[(big.t >= start_ms) & (big.t <= end_ms)]
        win_data.append(test.reset_index(drop=True))
    rng = np.random.default_rng(2026)
    totals = np.empty(SIMS)
    max_rois = np.empty(SIMS)
    pass_counts = np.zeros(SIMS, dtype=int)
    for s in range(SIMS):
        tp = 0.0
        mx = -999.0
        pc = 0
        for test in win_data:
            if len(test) == 0:
                continue
            score = rng.standard_normal(len(test))
            pnl, roi, dd, n, wr = exec_window(test, score)
            tp += pnl
            mx = max(mx, roi)
            if roi >= 10.0 and dd <= 5.0 and wr >= 40.0 and n >= 15:
                pc += 1
        totals[s] = tp
        max_rois[s] = mx
        pass_counts[s] = pc
    summary = {
        "sims": SIMS,
        "null_total_pnl_pct": {
            "median": float(np.median(totals / CAPITAL * 100)),
            "p05": float(np.quantile(totals / CAPITAL * 100, 0.05)),
            "p95": float(np.quantile(totals / CAPITAL * 100, 0.95)),
        },
        "null_max_window_roi": {
            "median": float(np.median(max_rois)),
            "p95": float(np.quantile(max_rois, 0.95)),
            "p99": float(np.quantile(max_rois, 0.99)),
            "max": float(max_rois.max()),
        },
        "null_pass_count_distribution": {str(k): int(v) for k, v in zip(*np.unique(pass_counts, return_counts=True))},
        "observed": {
            "v1_total_pct": -54.25, "v1_best_window_roi": 10.49,
            "v2_total_pct": -41.41, "v2_best_window_roi": 12.93,
        },
        "interpretation": None,
    }
    p_best = float((max_rois >= 12.93).mean())
    p_10_49 = float((max_rois >= 10.49).mean())
    summary["P(null max-window ROI >= observed v1 10.49%)"] = p_10_49
    summary["P(null max-window ROI >= observed v2 12.93%)"] = p_best
    summary["P(null total <= v2 observed -41.41%)"] = float((totals / CAPITAL * 100 <= -41.41).mean())
    summary["P(null total <= v1 observed -54.25%)"] = float((totals / CAPITAL * 100 <= -54.25).mean())
    OUT.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print(f"[rc] done in {time.perf_counter()-t0:.0f}s")


if __name__ == "__main__":
    main()
