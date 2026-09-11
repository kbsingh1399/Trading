"""stage5_oracle.py — ORACLE feasibility bound (NON-TRADABLE, lookahead by design).

Per window: rank candidates by REALIZED net r, greedily fill the mandate book
(concurrency 4, one-per-symbol) with the top trades until 25 are taken; apply
mandate risk sizing (no dd-defense; risk = base and house-money variant).

If even this perfect-foresight upper bound fails the joint criteria in many
windows, then NO causal selection method can reach 20/20: the criteria are
capacity-infeasible for this pool, independent of modeling skill.

Also reports: oracle mean net r of top-25, and the required mean (~+0.5R) for
+10%/month at $40 risk over 25 trades.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
WINDOWS_PATH = REPO / "Engine" / "oos_windows_20.json"
UNION = REPO / "scratch" / "union_pool_v2.parquet"
OUT = REPO / "scratch" / "ml_reversal_results" / "stage5_oracle.json"
CAPITAL = 5000.0


def oracle_window(test: pd.DataFrame, base_risk: float, max_trades: int = 25,
                  concurrency: int = 4):
    tt = test["t"].to_numpy()
    rr = test["r"].to_numpy()
    bars = test["bars"].to_numpy()
    syms = test["sym"].to_numpy()
    order = np.argsort(-rr)  # perfect foresight
    open_pos = []
    equity, peak, dd = CAPITAL, CAPITAL, 0.0
    pnl = 0.0
    wins = 0
    n = 0
    taken_r = []
    for k in order:
        if n >= max_trades:
            break
        t_entry = tt[k]
        open_pos = [op for op in open_pos if op[0] > t_entry]
        if syms[k] in [op[1] for op in open_pos]:
            continue
        if len(open_pos) >= concurrency:
            continue
        open_pos.append((t_entry + int(bars[k]) * 900_000, syms[k]))
        risk = base_risk if (equity - CAPITAL) < 50 else min(base_risk * 2.5, base_risk + (equity - CAPITAL) * 0.4)
        p = rr[k] * risk
        pnl += p
        taken_r.append(rr[k])
        wins += int(rr[k] > 0)
        n += 1
        equity += p
        peak = max(peak, equity)
        dd = max(dd, (peak - equity) / peak * 100)
    roi = pnl / CAPITAL * 100
    wr = wins / n * 100 if n else 0.0
    return pnl, roi, dd, n, wr, float(np.mean(taken_r)) if taken_r else 0.0


def main():
    big = pd.read_parquet(UNION)
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)
    print(f"{'W#':<3} | {'pool':>6} | {'risk':>4} | {'oracle trades':<5} | {'meanR(top25)':<13} | {'WR':<6} | {'ROI':<8} | {'DD':<6} | {'oracle PASS?':<6}", flush=True)
    rows = []
    for risk in (40.0, 100.0):
        npass = 0
        for w in windows:
            start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
            end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
            test = big[(big.t >= start_ms) & (big.t <= end_ms)]
            if len(test) == 0:
                continue
            pnl, roi, dd, n, wr, mean_r = oracle_window(test.reset_index(drop=True), risk)
            ok = roi >= 10.0 and dd <= 5.0 and wr >= 40.0 and n >= 15
            npass += int(ok)
            print(f"W{w['window_id']:02d} | {len(test):>6d} | {risk:>4.0f} | {n:<13d} | {mean_r:>+12.4f} | {wr:>5.1f}% | {roi:>+6.2f}% | {dd:>4.2f}% | {'YES' if ok else 'no':<6}", flush=True)
            rows.append({"window_id": w["window_id"], "risk": risk, "trades": n,
                         "mean_r_top25": mean_r, "wr": wr, "roi": roi, "dd": dd, "pass": bool(ok)})
        print(f"--> risk {risk:.0f}: ORACLE passes {npass}/20 windows", flush=True)
    OUT.write_text(json.dumps({"rows": rows}, indent=2))
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
