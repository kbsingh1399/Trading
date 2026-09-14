"""Which families carry edge in *which* windows, at the working geometry.

The scorecard is judged per window, so what matters is not the pooled edge of a
family but its edge inside each particular quarter.  The ungated breakout book
passes four windows and loses 2-4 % in eight chop/reversal quarters; filtering
those windows down does not help (a window with no trades still fails), so the
only useful question is *which family is positive there*.

This module measures, for every pre-registered family, the certified barrier net R
at the working geometry (wide volatility-scaled stop, 4R target, 288-bar cap,
41 bps friction) split by OOS window, so a regime-conditional family allocation
can be built from pre-window evidence rather than guessed.

Run: ``python -m Engine.levels_poc_lab.regime_screen``
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .data import ALL_SYMBOLS, BTC, load_all, windows, window_bounds
from .signals import default_specs, family_events, naked_poc_series, _atr
from .studies import batch_outcomes
from . import signals as _signals

FRICTION = 0.0041


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALL_SYMBOLS))
    ap.add_argument("--stop-scale", type=float, default=9.0)
    ap.add_argument("--target-r", type=float, default=4.0)
    ap.add_argument("--hold", type=int, default=288)
    ap.add_argument("--min-n", type=int, default=25)
    ap.add_argument("--out", default="regime_screen.csv")
    a = ap.parse_args()
    syms = [s.strip() for s in a.symbols.split(",") if s.strip()]
    _signals.ATR_STOP_SCALE = float(a.stop_scale)
    data = load_all(list(dict.fromkeys([BTC] + [s for s in syms if s != BTC])))
    wins = windows()
    bounds = [(w["window_id"],) + window_bounds(w) for w in wins]
    specs = default_specs()
    rows = []
    for sym, f in data.items():
        if sym == BTC:
            continue
        t = f.open_time_ms.to_numpy(np.int64)
        day = t // 86_400_000
        naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                                 f.high.to_numpy(float), f.close.to_numpy(float))
        o = f.open.to_numpy(float); h = f.high.to_numpy(float)
        lo = f.low.to_numpy(float); c = f.close.to_numpy(float)
        atr = _atr(f)
        for spec in specs:
            mask, side, _ = family_events(f, spec, naked=naked)
            idx = np.flatnonzero(mask)
            idx = idx[idx + 1 < len(c)]
            if len(idx) < 50:
                continue
            sd = side[idx]
            dist = np.maximum(a.stop_scale * atr[idx], 0.012 * c[idx])
            net = (batch_outcomes(o, h, lo, c, idx, sd, dist, a.target_r, a.hold)
                   - FRICTION * c[idx] / dist)
            tt = t[idx]
            for wid, s0, s1 in bounds:
                m = (tt >= s0) & (tt <= s1)
                if m.sum() < a.min_n:
                    continue
                rows.append({"window": wid, "family": spec.name, "group": spec.group,
                             "n": int(m.sum()), "meanR": float(net[m].mean()),
                             "wr": float((net[m] > 0).mean())})
    df = pd.DataFrame(rows)
    out = Path("scratch")
    out.mkdir(exist_ok=True)
    df.to_csv(out / a.out, index=False)
    print(f"rows {len(df):,} (family x window with n >= {a.min_n})\n")

    # Aggregate to one row per (window, family) across symbols *before* judging:
    # judging per symbol-instance produces multiple-comparison artefacts (with ~17
    # symbols a family looks "positive in 8/8 windows" while being negative pooled).
    agg = df.groupby(["window", "family"]).apply(
        lambda d: pd.Series({"n": int(d.n.sum()),
                             "meanR": float(np.average(d.meanR, weights=d.n))}),
        include_groups=False).reset_index()
    agg.to_csv(out / a.out.replace(".csv", "_agg.csv"), index=False)
    problem = [7, 8, 10, 12, 13, 14, 15, 20]
    print("=== window-level: families with aggregate mean R > 0 (n >= 100), problem windows ===")
    for w in problem:
        s = agg[(agg.window == w) & (agg.n >= 100) & (agg.meanR > 0)].sort_values("meanR", ascending=False)
        print(f"W{w:02d}: " + (", ".join(f"{r.family}({r.meanR:+.2f},n{r.n})"
                                         for r in s.head(4).itertuples()) if not s.empty else "none"))
    print("\n=== consistency at window level: positive in >= 6 of 8 problem windows ===")
    prob = agg[agg.window.isin(problem) & (agg.n >= 50)]
    pos = prob[prob.meanR > 0].groupby("family").agg(
        windows_positive=("window", "nunique"), meanR=("meanR", "mean"), med_n=("n", "median"))
    if len(pos):
        print(pos.sort_values(["windows_positive", "meanR"], ascending=False).round(3).to_string())
    print("\n=== every family: pooled and problem-window aggregate (window-level) ===")
    summ = agg.groupby("family").apply(lambda d: pd.Series({
        "pooled_meanR": float(np.average(d.meanR, weights=d.n)), "pooled_n": int(d.n.sum()),
        "problem_meanR": float(np.average(d[d.window.isin(problem)].meanR,
                                          weights=d[d.window.isin(problem)].n))
        if (d.window.isin(problem)).any() else np.nan,
        "problem_n": int(d[d.window.isin(problem)].n.sum()),
        "problem_windows_pos": int((d[d.window.isin(problem)].meanR > 0).sum())}),
        include_groups=False)
    print(summ.sort_values("problem_meanR", ascending=False).head(20).round(3).to_string())


if __name__ == "__main__":
    main()
