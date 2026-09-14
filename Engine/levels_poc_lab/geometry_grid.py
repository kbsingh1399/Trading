"""Window x family x geometry screen: does any (family, geometry) have edge?

Run: ``python -m Engine.levels_poc_lab.geometry_grid``

Friction is a *price* cost, so in R terms it is 0.0041/stop_distance: a 1-ATR stop
pays ~0.3R in costs, a 9-ATR stop ~0.07R.  That is why every working configuration
in this lab uses wide volatility-scaled stops.  What this script asks is the next
question: holding the stop wide (so costs stay small), does any (family, target)
pair have positive expectation in each OOS window -- in particular in the chop
quarters (W07, W15) where nothing positive showed up at 9 ATR / 4R?
"""
from __future__ import annotations
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from .data import ALL_SYMBOLS, BTC, load_all, windows, window_bounds
from .signals import default_specs, family_events, naked_poc_series, _atr
from .studies import batch_outcomes
from . import signals as _signals

FRICTION = 0.0041
STOPS = [4.0, 6.0, 9.0]
TARGETS = [2.0, 3.0, 4.0]
HOLD = 288

syms = [s.strip() for s in ",".join(ALL_SYMBOLS).split(",") if s.strip()]
data = load_all(list(dict.fromkeys([BTC] + [s for s in syms if s != BTC])))
print(f"symbols loaded: {len(data)}", file=sys.stderr)
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
        tt = t[idx]
        wid_arr = np.zeros(len(idx), np.int16)
        for wid, s0, s1 in bounds:
            wid_arr[(tt >= s0) & (tt <= s1)] = wid
        for stop, targ in itertools.product(STOPS, TARGETS):
            dist = np.maximum(stop * atr[idx], 0.012 * c[idx])
            net = (batch_outcomes(o, h, lo, c, idx, sd, dist, targ, HOLD)
                   - FRICTION * c[idx] / dist)
            df = pd.DataFrame({"window": wid_arr, "net_r": net})
            g = df[df.window > 0].groupby("window")["net_r"].agg(["size", "mean"])
            for w, r in g.iterrows():
                rows.append({"symbol": sym, "family": spec.name, "stop": stop, "target": targ,
                             "window": int(w), "n": int(r["size"]), "meanR": float(r["mean"])})

df = pd.DataFrame(rows)
agg = df.groupby(["window", "family", "stop", "target"]).apply(
    lambda d: pd.Series({"n": int(d.n.sum()), "meanR": float(np.average(d.meanR, weights=d.n))}),
    include_groups=False).reset_index()
agg.to_csv(Path("scratch") / "geom_grid_agg.csv", index=False)
print(f"aggregate rows {len(agg):,}")
prob = [7, 8, 10, 12, 13, 14, 15, 20]
print("\n=== best (family, geometry) per window, min n = 150 ===")
for w in range(1, 21):
    s = agg[(agg.window == w) & (agg.n >= 150)].sort_values("meanR", ascending=False).head(3)
    flag = "  <-- problem" if w in prob else ""
    print(f"W{w:02d}: " + " | ".join(f"{r.family} s{r.stop:g} t{r.target:g} {r.meanR:+.3f} (n{r.n})"
                                     for r in s.itertuples()) + flag)
print("\n=== for the problem windows: all rows with meanR > 0.1 and n >= 150 ===")
s = agg[(agg.window.isin(prob)) & (agg.n >= 150) & (agg.meanR > 0.10)].sort_values(
    ["window", "meanR"], ascending=[True, False])
print(s.head(40).round(3).to_string(index=False))
