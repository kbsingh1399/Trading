"""Run the event study for every geometric family over the 20 OOS windows.

Outputs
-------
``scratch/lpl_event_study.json``   full statistics per family (pooled, per side,
                                   per window)
``scratch/lpl_event_study.md``     human-readable tables

The event study is descriptive: nothing is fitted, so a family that shows a
positive mean net R here is a genuine (if not yet tradable) regularity.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import PURGE_MS
from .data import ALTCOINS, BTC, windows, window_bounds, load_all
from .signals import default_specs, family_events, naked_poc_series
from .studies import batch_outcomes, summarize

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = REPO_ROOT / "scratch" / "lpl_event_study.json"
OUT_MD = REPO_ROOT / "scratch" / "lpl_event_study.md"


def symbol_events(f: pd.DataFrame, specs) -> dict:
    """Compute pooled event indices / sides / distances for one symbol."""
    t = f.open_time_ms.to_numpy(np.int64)
    day = t // 86_400_000
    naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                             f.high.to_numpy(float), f.close.to_numpy(float))
    o = f.open.to_numpy(float)
    h = f.high.to_numpy(float)
    lo = f.low.to_numpy(float)
    c = f.close.to_numpy(float)
    out = {}
    for spec in specs:
        mask, side, dist = family_events(f, spec, naked=naked)
        idx = np.flatnonzero(mask & np.isfinite(dist) & (dist > 0))
        if len(idx) == 0:
            out[spec.name] = None
            continue
        r = batch_outcomes(o, h, lo, c, idx, side[idx], dist[idx], spec.target_r, spec.horizon_bars)
        out[spec.name] = {
            "index": idx,
            "side": side[idx],
            "r": r,
            "t": t[idx],
            "symbol": f.symbol.iloc[0],
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALTCOINS))
    ap.add_argument("--group", default=None, help="filter: level_break,level_sweep,poc,confluence")
    ap.add_argument("--target-r", type=float, default=None)
    ap.add_argument("--horizon", type=int, default=None)
    args = ap.parse_args()

    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    groups = args.group.split(",") if args.group else None
    specs = default_specs(groups)
    if args.target_r is not None:
        for s in specs:
            s.target_r = args.target_r
    if args.horizon is not None:
        for s in specs:
            s.horizon_bars = args.horizon

    data = load_all(syms)
    wins = windows()
    bounds = [window_bounds(w) for w in wins]

    # collect events per family across symbols
    pool: dict[str, list] = {s.name: [] for s in specs}
    for sym, f in data.items():
        ev = symbol_events(f, specs)
        for name, d in ev.items():
            if d is not None:
                pool[name].append(d)

    report = {"target_r": specs[0].target_r, "horizon_bars": specs[0].horizon_bars, "families": {}}
    rows = []
    for spec in specs:
        chunks = pool[spec.name]
        if not chunks:
            continue
        r = np.concatenate([c["r"] for c in chunks])
        side = np.concatenate([c["side"] for c in chunks])
        t = np.concatenate([c["t"] for c in chunks])
        stats = summarize(r)
        long_stats = summarize(r[side > 0])
        short_stats = summarize(r[side < 0])
        per_window = {}
        for w, (s_ms, e_ms) in zip(wins, bounds):
            m = (t >= s_ms) & (t <= e_ms)
            per_window[w["window_id"]] = summarize(r[m])
        report["families"][spec.name] = {
            "group": spec.group,
            "description": spec.description,
            "target_r": spec.target_r,
            "horizon_bars": spec.horizon_bars,
            "pooled": stats,
            "long": long_stats,
            "short": short_stats,
            "per_window": per_window,
        }
        rows.append({
            "family": spec.name,
            "group": spec.group,
            "n": stats["n"],
            "win%": stats["win_rate"],
            "meanR": stats["mean_r"],
            "t": stats["t_stat"],
            "long_n": long_stats["n"],
            "long_meanR": long_stats["mean_r"],
            "short_n": short_stats["n"],
            "short_meanR": short_stats["mean_r"],
            "windows_pos": sum(1 for k, v in per_window.items() if v["n"] >= 5 and (v["mean_r"] or 0) > 0),
            "windows_n": sum(1 for v in per_window.values() if v["n"] >= 5),
        })

    tag = f"tr{specs[0].target_r:.1f}_h{specs[0].horizon_bars}"
    out_json = OUT_JSON.with_name(f"lpl_event_study_{tag}.json")
    out_md = OUT_MD.with_name(f"lpl_event_study_{tag}.md")
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, default=float), encoding="utf-8")

    df = pd.DataFrame(rows).sort_values("meanR", ascending=False)
    lines = ["# Levels / POC event study (net R, target_r=%.1f, horizon=%d bars)" % (specs[0].target_r, specs[0].horizon_bars), "",
             "Net R is after the certified 41 bps round-trip friction. ``windows_pos`` counts the",
             "OOS windows (of those with >= 5 events) whose mean net R was positive.", "",
             "| family | group | n | win% | mean netR | t | long meanR | short meanR | windows_pos |",
             "|---|---|---|---|---|---|---|---|---|"]
    for _, r_ in df.iterrows():
        lines.append(
            f"| {r_['family']} | {r_['group']} | {int(r_['n'])} | {r_['win%']:.1f} | {r_['meanR']:+.3f} | "
            f"{r_['t'] if r_['t'] is None else round(r_['t'],2)} | "
            f"{'' if pd.isna(r_['long_meanR']) else format(r_['long_meanR'],'+.3f')} | "
            f"{'' if pd.isna(r_['short_meanR']) else format(r_['short_meanR'],'+.3f')} | {int(r_['windows_pos'])}/{int(r_['windows_n'])} |"
        )
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(df.to_string(index=False))
    print(f"\nwrote {out_md}")


if __name__ == "__main__":
    main()
