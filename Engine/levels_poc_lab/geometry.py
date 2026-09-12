"""Geometry screen: certified-suite stop scales vs a tight-stop geometry.

Run with ``python -m Engine.levels_poc_lab.geometry``.

The certified suite's own pre-registered hypothesis family is
``stop_atr in (2.5, 3.0)`` with ``target_r in (2.0, 2.2)`` and
``max_hold_bars = 144`` (``s1_trend_following_suite.candidate_configs``), with a
hard floor ``stop = max(stop_atr * ATR, 1.2 % of price)``.  The lab has so far
always used a tight stop (0.5-1.25 ATR) with a 4R target, i.e. the same 5 ATR
price distance but stopped out by noise far more often and paying 2x the friction
per R.  This screen measures both families on identical events with the certified
41 bps friction.
"""
from __future__ import annotations

from pathlib import Path



import numpy as np
import pandas as pd

from .data import ALL_SYMBOLS, load_all
from .signals import _atr, default_specs, family_events, naked_poc_series
from .studies import batch_outcomes

FRICTION = 0.0041  # certified floor: 8 + 10 + 15 bps, floored at 41 bps round trip
FAMILIES = ["brk_ath", "x_ath_brk_lowvol", "brk_pwh", "brk_pmh", "brk_pwh_cascade",
            "brk_multi_lvl", "brk_pwh_retest"]
GEOMS = [(1.25, 4.0, 288), (2.0, 2.0, 288), (2.5, 2.0, 144), (3.0, 2.0, 144),
         (2.5, 2.2, 144), (2.5, 4.0, 288), (3.0, 4.0, 288)]


def main():
    syms = [s.strip() for s in (sys.argv[1].split(",") if len(sys.argv) > 1 else ALL_SYMBOLS)]
    data = load_all(syms)
    specs = {s.name: s for s in default_specs() if s.name in FAMILIES}
    rows = []
    for sym in syms:
        f = data[sym]
        t = f.open_time_ms.to_numpy(np.int64)
        day = t // 86_400_000
        naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                                 f.high.to_numpy(float), f.close.to_numpy(float))
        o = f.open.to_numpy(float); h = f.high.to_numpy(float)
        lo = f.low.to_numpy(float); c = f.close.to_numpy(float)
        atr = _atr(f); px = c
        for name, spec in specs.items():
            mask, side, _ = family_events(f, spec, naked=naked)
            idx = np.flatnonzero(mask)
            idx = idx[idx + 1 < len(c)]
            if len(idx) < 30:
                continue
            sd = side[idx]
            for k, tr, hz in GEOMS:
                dist = np.maximum(k * atr[idx], 0.012 * px[idx])
                gross = batch_outcomes(o, h, lo, c, idx, sd, dist, tr, hz)
                cost_r = FRICTION * px[idx] / dist
                net = gross - cost_r
                rows.append({
                    "sym": sym, "family": name, "stop_atr": k, "target_r": tr, "hold": hz,
                    "n": len(idx), "gross": float(np.mean(gross)), "cost_r": float(np.mean(cost_r)),
                    "netR": float(np.mean(net)), "win": float(np.mean(net > 0)),
                    "big": float(np.mean(net >= 2.0)),
                    "stop_bps": float(np.mean(dist / px[idx]) * 1e4)})
    df = pd.DataFrame(rows)
    df.to_csv(REPO_ROOT / "scratch" / "geom_screen.csv", index=False)
    g = df.groupby(["stop_atr", "target_r", "hold"]).apply(
        lambda d: pd.Series({
            "n": int(d.n.sum()), "grossR": float(np.average(d.gross, weights=d.n)),
            "costR": float(np.average(d.cost_r, weights=d.n)),
            "netR": float(np.average(d.netR, weights=d.n)),
            "win": float(np.average(d.win, weights=d.n)),
            "P(>=2R)": float(np.average(d.big, weights=d.n)),
            "stop_bps": float(np.average(d.stop_bps, weights=d.n))}), include_groups=False)
    print("pooled across families and symbols:")
    print(g.round(3).to_string())
    print("\nper family, best geometry by netR:")
    for fam in FAMILIES:
        d = df[df.family == fam]
        if d.empty:
            continue
        agg = d.groupby(["stop_atr", "target_r", "hold"]).apply(
            lambda x: pd.Series({"netR": float(np.average(x.netR, weights=x.n)),
                                 "win": float(np.average(x.win, weights=x.n))}),
            include_groups=False).sort_values("netR", ascending=False)
        best = agg.index[0]
        cur = agg.loc[(1.25, 4.0, 288)] if (1.25, 4.0, 288) in agg.index else None
        print(f"{fam:<22} best stop={best[0]} target={best[1]} hold={best[2]} "
              f"netR={agg.iloc[0].netR:+.3f} win={agg.iloc[0].win:.1%} | "
              f"lab geometry netR={cur.netR:+.3f} win={cur.win:.1%}" if cur is not None else "")


if __name__ == "__main__":
    main()
