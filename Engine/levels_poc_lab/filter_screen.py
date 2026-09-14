"""Per-window conditional-edge screen for hard filters.

The ungated portfolio (wide stops, regime filter, 4 slots) now passes 4/20 windows,
and its two remaining failure modes are visible in the scorecard:

* ten windows execute fewer than 15 trades -- the candidate pool is too thin in
  those quarters, so widening the family pool is the fix; and
* eight chop/reversal quarters lose 2-4 % -- the book takes breaks that fail.

Both are questions about *which conditions the events should be allowed in*, and
that can be measured directly and cheaply at the event level, per window, instead
of by running a full portfolio simulation for every idea.  This module builds the
candidate events once, then reports for each OOS window and each filter set:
number of candidates, mean barrier net R (certified 41 bps) and win rate.

Filters tested (all causal, all computable at the signal bar):

* ``tide``      -- the trade side agrees with the BTC 4h macro tide;
* ``cusum``     -- a CUSUM structural-move event fired in the trade direction
                   within the last ``cusum_bars`` bars (see cusum.py);
* ``breadth``   -- market breadth confirmes the side (share of the panel above its
                   200-bar mean >= 0.5 for longs, <= 0.5 for shorts);
* ``lowvol``    -- the symbol is not in a volatility spike (``atr_z < 1.0``).

Run: ``python -m Engine.levels_poc_lab.filter_screen``
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
WIDE_POOL = ["brk_ath", "x_ath_brk_lowvol", "brk_pmh", "brk_pml", "brk_multi_lvl",
             "brk_pdh", "brk_pdl", "x_brk_pwh_out_of_value", "x_pwh_sweep_at_poc", "swp_pwl"]


def build_event_panel(symbols, pool, stop_scale, target_r, hold, pending_step=4):
    _signals.ATR_STOP_SCALE = float(stop_scale)
    data = load_all(list(dict.fromkeys([BTC] + [s for s in symbols if s != BTC])))
    btc = data[BTC]
    btc_idx = pd.Index(btc.open_time_ms.to_numpy())
    tide = pd.Series(np.where(btc.close.to_numpy(float) > btc.e200_4h.to_numpy(float), 1, -1),
                     index=btc_idx)
    specs = [s for s in default_specs() if s.name in pool]
    # panel breadth for the market-regime filter
    frames = []
    for s, f in data.items():
        if s == BTC:
            continue
        frames.append(pd.DataFrame({"open_time_ms": f.open_time_ms.to_numpy(),
                                    "above": (f.close > f.e200).astype("float32").to_numpy()}))
    breadth = pd.concat(frames).groupby("open_time_ms")["above"].mean()

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
        cs_up = f.cs_up_age.to_numpy(float)
        cs_dn = f.cs_dn_age.to_numpy(float)
        az = f.atr_z.to_numpy(float)
        for spec in specs:
            mask, side, _ = family_events(f, spec, naked=naked)
            idx = np.flatnonzero(mask)
            idx = idx[idx + 1 < len(c)]
            if len(idx) < 20:
                continue
            sd = side[idx]
            dist = np.maximum(stop_scale * atr[idx], 0.012 * c[idx])
            net = (batch_outcomes(o, h, lo, c, idx, sd, dist, target_r, hold)
                   - FRICTION * c[idx] / dist)
            rows.append(pd.DataFrame({
                "symbol": sym, "family": spec.name, "t": t[idx], "side": sd, "net_r": net,
                "tide_ok": (np.where(sd > 0, tide.reindex(t[idx]).to_numpy(float), -tide.reindex(t[idx]).to_numpy(float)) > 0),
                "cs_up": cs_up[idx], "cs_dn": cs_dn[idx],
                "atr_z": az[idx],
                "breadth": breadth.reindex(t[idx]).to_numpy(float),
            }))
    ev = pd.concat(rows, ignore_index=True)
    ev["side_ok"] = np.where(ev.side > 0, ev.breadth >= 0.5, ev.breadth <= 0.5)
    return ev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALL_SYMBOLS))
    ap.add_argument("--pool", default=",".join(WIDE_POOL))
    ap.add_argument("--stop-scale", type=float, default=9.0)
    ap.add_argument("--target-r", type=float, default=4.0)
    ap.add_argument("--hold", type=int, default=288)
    ap.add_argument("--cusum-bars", type=int, default=48)
    ap.add_argument("--out", default="filter_screen.csv")
    a = ap.parse_args()
    syms = [s.strip() for s in a.symbols.split(",") if s.strip()]
    ev = build_event_panel(syms, [p.strip() for p in a.pool.split(",")], a.stop_scale,
                           a.target_r, a.hold)
    print(f"events {len(ev):,} | overall mean net R {ev.net_r.mean():+.3f}\n")

    cusum = np.where(ev.side > 0, ev.cs_up <= a.cusum_bars, ev.cs_dn <= a.cusum_bars)
    filters = {
        "none": np.ones(len(ev), bool),
        "tide": ev.tide_ok.to_numpy(),
        "tide+cusum": ev.tide_ok.to_numpy() & cusum,
        "tide+breadth": ev.tide_ok.to_numpy() & ev.side_ok.to_numpy(),
        "tide+lowvol": ev.tide_ok.to_numpy() & (ev.atr_z.to_numpy() < 1.0),
        "tide+cusum+breadth": ev.tide_ok.to_numpy() & cusum & ev.side_ok.to_numpy(),
        "tide+cusum+lowvol": ev.tide_ok.to_numpy() & cusum & (ev.atr_z.to_numpy() < 1.0),
    }
    wins = windows()
    bounds = {w["window_id"]: window_bounds(w) for w in wins}
    ev["window"] = 0
    for wid, (s0, s1) in bounds.items():
        ev.loc[(ev.t >= s0) & (ev.t <= s1), "window"] = wid

    tables = []
    for name, m in filters.items():
        m = np.asarray(m, bool)
        sub = ev[m]
        per = sub.groupby("window").agg(n=("net_r", "size"), meanR=("net_r", "mean"),
                                        wr=("net_r", lambda x: (x > 0).mean()))
        per["filter"] = name
        tables.append(per.reset_index())
    df = pd.concat(tables, ignore_index=True)
    out = Path("scratch")
    out.mkdir(exist_ok=True)
    df.to_csv(out / a.out, index=False)

    print("=== per-window mean net R by filter set ===")
    print(df.pivot_table(index="window", columns="filter", values="meanR").round(3).to_string())
    print("\n=== per-window candidate count by filter set ===")
    print(df.pivot_table(index="window", columns="filter", values="n").astype("Int64").to_string())
    print("\n=== summary: windows with meanR >= 0.25 and n >= 60 (both constraints feasible) ===")
    for name in filters:
        s = df[(df["filter"] == name)]
        ok = s[(s.meanR >= 0.25) & (s.n >= 60)]
        neg = s[s.meanR < 0]
        print(f"{name:<20} feasible={len(ok):>2}/20  negative-edge windows={len(neg):>2}  "
              f"pooled meanR={ev[filters[name]].net_r.mean():+.3f}  n={int(filters[name].sum())}")


if __name__ == "__main__":
    main()
