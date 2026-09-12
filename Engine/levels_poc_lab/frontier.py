"""The cost frontier: gross edge vs certified friction.

For each family and exit geometry this computes

* gross mean R (no friction) -- the raw predictive content of the level / POC event,
* net mean R at a ladder of round-trip frictions (10/20/30/41/60 bps),
* the friction level (bps) at which net expectancy crosses zero.

This is the honest answer to "why does nothing pass": if the gross edge per event
is smaller than the round-trip cost, no amount of ML filtering can turn the
concept into a profitable portfolio.
"""
from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from numba import njit

from .data import ALTCOINS, load_all
from .signals import default_specs, family_events, naked_poc_series

REPO_ROOT = None


@njit(cache=True, fastmath=True)
def _one_outcome(o, h, lo, c, i, side, dist, target_r, horizon, friction_frac):
    """Net R of one event with an arbitrary round-trip friction (fraction of price)."""
    n = len(c)
    if i + 1 >= n:
        return np.nan
    entry = o[i + 1]
    if not (dist > 0.0) or not np.isfinite(dist) or not np.isfinite(entry):
        return np.nan
    tgt = entry + side * target_r * dist
    stp = entry - side * dist
    end = min(i + 1 + horizon, n)
    exit_r = 0.0
    closed = False
    for j in range(i + 1, end):
        if side == 1:
            if lo[j] <= stp:
                exit_r = -1.0
                closed = True
                break
            if h[j] >= tgt:
                exit_r = target_r
                closed = True
                break
        else:
            if h[j] >= stp:
                exit_r = -1.0
                closed = True
                break
            if lo[j] <= tgt:
                exit_r = target_r
                closed = True
                break
    if not closed:
        last = end - 1
        exit_r = (c[last] - entry) / dist if side == 1 else (entry - c[last]) / dist
    return exit_r - friction_frac * entry / dist


def outcomes(o, h, lo, c, idx, side, dist, target_r, horizon, friction_frac):
    out = np.empty(len(idx), np.float64)
    for k in range(len(idx)):
        out[k] = _one_outcome(o, h, lo, c, idx[k], side[k], dist[k], target_r, horizon, friction_frac)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALTCOINS))
    ap.add_argument("--group", default=None)
    ap.add_argument("--target-r", type=float, default=4.0)
    ap.add_argument("--horizon", type=int, default=288)
    ap.add_argument("--frictions", default="0,10,20,30,41,60")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    specs = default_specs(args.group.split(",") if args.group else None)
    frictions = [float(x) for x in args.frictions.split(",")]
    data = load_all(syms)

    rows = []
    for spec in specs:
        nets = {f: [] for f in frictions}
        n_events = 0
        stop_rel = []
        for sym in syms:
            f = data[sym]
            t = f.open_time_ms.to_numpy(np.int64)
            day = t // 86_400_000
            naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                                     f.high.to_numpy(float), f.close.to_numpy(float))
            mask, side, dist = family_events(f, spec, naked=naked)
            idx = np.flatnonzero(mask & np.isfinite(dist) & (dist > 0))
            idx = idx[idx + 1 < len(f)]
            if len(idx) == 0:
                continue
            o = f.open.to_numpy(float)
            h = f.high.to_numpy(float)
            lo = f.low.to_numpy(float)
            c = f.close.to_numpy(float)
            for fr in frictions:
                nets[fr].append(outcomes(o, h, lo, c, idx, side[idx], dist[idx],
                                         spec.target_r, spec.horizon_bars, fr / 10_000.0))
            stop_rel.append(dist[idx] / o[idx + 1])
            n_events += len(idx)
        if n_events == 0:
            continue
        row = {"family": spec.name, "group": spec.group, "n": int(n_events),
               "mean_stop_pct": float(np.mean(np.concatenate(stop_rel)) * 100)}
        for fr in frictions:
            r = np.concatenate(nets[fr])
            r = r[np.isfinite(r)]
            row[f"netR_f{int(fr)}"] = float(r.mean())
            if fr == 0.0:
                row["win_rate_gross_pct"] = float((r > 0).mean() * 100)
                row["t_gross"] = float(r.mean() / (r.std(ddof=1) / np.sqrt(len(r))))
        f0 = row.get("netR_f0", np.nan)
        f41 = row.get("netR_f41", np.nan)
        row["breakeven_friction_bps"] = (41.0 * f0 / (f0 - f41)) if np.isfinite(f0) and np.isfinite(f41) and f0 != f41 else np.nan
        rows.append(row)

    df = pd.DataFrame(rows).sort_values("netR_f0", ascending=False)
    from pathlib import Path
    out = Path(args.out) if args.out else Path(__file__).resolve().parents[2] / "scratch" / f"lpl_frontier_tr{args.target_r:.0f}_h{args.horizon}.csv"
    out.parent.mkdir(exist_ok=True, parents=True)
    df.to_csv(out, index=False)
    print(df.to_string(index=False, float_format=lambda v: f"{v:+.3f}"))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
