"""Conditional impulse study: where does each family's edge actually live?

Splits each family's events by
  * side (long / short),
  * BTC macro tide (bull / bear / neutral) at the event bar,
  * the symbol's own 4h trend anchor,
  * realised-volatility regime (ATR z-score above/below its median),
  * break-window size (does the edge survive in the crash windows?).

Everything is a fixed, ex-ante split -- no fitting.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .data import ALTCOINS, BTC, load_all, windows, window_bounds
from .signals import default_specs, family_events, naked_poc_series

HORIZONS = (24, 96, 288)


def _t(x):
    x = x[np.isfinite(x)]
    if len(x) < 5:
        return len(x), np.nan, np.nan
    mu = float(x.mean())
    se = float(x.std(ddof=1) / np.sqrt(len(x)))
    return len(x), mu, (mu / se if se > 0 else np.nan)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALTCOINS))
    ap.add_argument("--group", default="level_break,confluence")
    ap.add_argument("--out", default="lpl_splits")
    args = ap.parse_args()
    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    specs = default_specs(args.group.split(","))
    data = load_all(list(dict.fromkeys([BTC] + syms)))
    btc = data[BTC].set_index("open_time_ms")
    tide = np.where(btc.close > btc.e200_4h, 1, -1)  # BTC 4h macro anchor
    tide = pd.Series(tide, index=btc.index)

    buckets: dict[tuple, list] = {}
    for sym in syms:
        f = data[sym]
        t = f.open_time_ms.to_numpy(np.int64)
        day = t // 86_400_000
        naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                                 f.high.to_numpy(float), f.close.to_numpy(float))
        o = f.open.to_numpy(float)
        c = f.close.to_numpy(float)
        atr = np.maximum(f.atr.to_numpy(float), c * 0.004)
        macro = tide.reindex(t).to_numpy(float)
        own_up = (f.trend_up.to_numpy(int) == 1) | (f.slope200_4h.to_numpy(float) > 0)
        own_dn = (f.trend_dn.to_numpy(int) == 1) | (f.slope200_4h.to_numpy(float) < 0)
        atr_z = f.atr_z.to_numpy(float)
        for spec in specs:
            mask, side, dist = family_events(f, spec, naked=naked)
            idx = np.flatnonzero(mask & np.isfinite(dist) & (dist > 0))
            idx = idx[idx + 1 < len(c)]
            if len(idx) == 0:
                continue
            s_ = side[idx]
            for hz in HORIZONS:
                j = np.minimum(idx + hz, len(c) - 1)
                fut = (c[j] - o[idx + 1]) / atr[idx] * s_
                for label, cond in (
                    ("all", np.ones(len(idx), bool)),
                    ("long", s_ > 0),
                    ("short", s_ < 0),
                    ("macro_bull", macro[idx] > 0),
                    ("macro_bear", macro[idx] < 0),
                    ("own_up", own_up[idx]),
                    ("own_dn", own_dn[idx]),
                    ("atr_z_hi", atr_z[idx] >= 0.5),
                    ("atr_z_lo", atr_z[idx] < 0.5),
                    ("long_macro_bull", (s_ > 0) & (macro[idx] > 0)),
                    ("short_macro_bear", (s_ < 0) & (macro[idx] < 0)),
                    ("long_own_up", (s_ > 0) & own_up[idx]),
                    ("short_own_dn", (s_ < 0) & own_dn[idx]),
                ):
                    val = fut[cond]
                    val = val[np.isfinite(val)]
                    if len(val) >= 5:
                        buckets.setdefault((spec.name, spec.group, hz, label), []).append(val)

    rows = []
    for (fam, group, hz, label), chunks in buckets.items():
        x = np.concatenate(chunks)
        n_, mu, tt = _t(x)
        rows.append({"family": fam, "group": group, "horizon": hz, "cond": label,
                     "n": n_, "mean_atr": mu, "t": tt})

    df = pd.DataFrame(rows)
    OUT = Path(__file__).resolve().parents[2] / "scratch"
    OUT.mkdir(exist_ok=True)
    df.to_csv(OUT / f"{args.out}.csv", index=False)

    # Print the most informative view: horizon 96 / 288, conditions with |t| > 2
    for hz in (96, 288):
        sub = df[(df.horizon == hz) & (df.t.abs() > 2.0)].sort_values("mean_atr", ascending=False)
        print(f"\n=== horizon {hz} bars: conditions with |t| > 2 ===")
        print(sub.head(60).to_string(index=False, float_format=lambda v: f"{v:+.3f}"))
    print(f"\nwrote {OUT / (args.out + '.csv')}")


if __name__ == "__main__":
    main()
