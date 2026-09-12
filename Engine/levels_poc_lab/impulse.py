"""Impulse response of level / POC events.

Barrier studies mix three things: direction, barrier geometry and costs.  This
module measures *direction only*: the mean forward return after an event, in ATR
units, over several horizons, with t-statistics and a split by volatility regime.
It answers the question "does the level event predict anything at all?" before
portfolio machinery and friction enter the picture.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .data import ALTCOINS, load_all, windows, window_bounds
from .signals import default_specs, family_events, naked_poc_series

HORIZONS = (4, 24, 96, 288)

REPO_ROOT = Path(__file__).resolve().parents[2]


def impulse_for_symbol(f: pd.DataFrame, specs, horizons=HORIZONS):
    t = f.open_time_ms.to_numpy(np.int64)
    day = t // 86_400_000
    naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                             f.high.to_numpy(float), f.close.to_numpy(float))
    o = f.open.to_numpy(float)
    c = f.close.to_numpy(float)
    atr = np.maximum(f.atr.to_numpy(float), c * 0.004)
    out = {}
    for spec in specs:
        mask, side, dist = family_events(f, spec, naked=naked)
        idx = np.flatnonzero(mask & np.isfinite(dist) & (dist > 0))
        if len(idx) == 0:
            continue
        idx = idx[idx + 1 < len(c)]
        if len(idx) == 0:
            continue
        rec = {"index": idx, "side": side[idx], "t": t[idx], "symbol": f.symbol.iloc[0]}
        for hz in horizons:
            j = np.minimum(idx + hz, len(c) - 1)
            fut = (c[j] - o[idx + 1]) / atr[idx] * side[idx]
            rec[f"fwd_{hz}"] = fut
        out[spec.name] = rec
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALTCOINS))
    ap.add_argument("--group", default=None)
    args = ap.parse_args()
    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    specs = default_specs(args.group.split(",") if args.group else None)
    data = load_all(syms)
    pool: dict[str, list] = {s.name: [] for s in specs}
    for sym, f in data.items():
        for name, rec in impulse_for_symbol(f, specs).items():
            pool[name].append(rec)

    wins = windows()
    bounds = [window_bounds(w) for w in wins]
    rows = []
    detail = {}
    for spec in specs:
        chunks = pool[spec.name]
        if not chunks:
            continue
        def cat(key):
            return np.concatenate([c[key] for c in chunks])
        v = {f"fwd_{h}": cat(f"fwd_{h}") for h in HORIZONS}
        t = cat("t")
        sign = cat("side")
        row = {"family": spec.name, "group": spec.group, "n": len(t)}
        for h in HORIZONS:
            x = v[f"fwd_{h}"]
            m = np.isfinite(x)
            mu = float(np.mean(x[m])) if m.any() else np.nan
            se = float(np.std(x[m], ddof=1) / np.sqrt(m.sum())) if m.sum() > 1 else np.nan
            row[f"fwd{h}"] = mu
            row[f"t{h}"] = mu / se if se and np.isfinite(se) and se > 0 else np.nan
        # regime split at 96 bars
        x = v["fwd_96"]
        detail[spec.name] = {"n": int(len(t)), "per_window_96": {}}
        for w, (s_ms, e_ms) in zip(wins, bounds):
            m = (t >= s_ms) & (t <= e_ms) & np.isfinite(x)
            detail[spec.name]["per_window_96"][w["window_id"]] = {
                "n": int(m.sum()), "mean_fwd96": float(np.mean(x[m])) if m.any() else None,
            }
        rows.append(row)
    df = pd.DataFrame(rows).sort_values("fwd96", ascending=False)
    OUT = REPO_ROOT / "scratch"
    OUT.mkdir(exist_ok=True)
    tag = args.group.replace(",", "-") if args.group else "all"
    (OUT / f"lpl_impulse_{tag}.json").write_text(json.dumps(detail, indent=2), encoding="utf-8")
    df.to_csv(OUT / f"lpl_impulse_{tag}.csv", index=False)
    print(df.to_string(index=False, float_format=lambda v: f"{v:+.3f}"))


if __name__ == "__main__":
    main()
