"""Walk-forward geometry selection for T1 -- the "system with edge" attempt.

WHY THIS DESIGN
---------------
The economics are fixed and cannot be argued with:

    gross  +0.116439 R/trade
    friction 0.199042 R/trade   (41 bps, Shynkevich 2026 JFM: taker >=8 bps +
                                 entry slip 10 + stop slip 15. NOT negotiable.)
    net    -0.082603 R/trade

So the only honest lever is gross R per trade, and it must rise +70.9%.

The one structural fact established by T1_AUDIT.md is that the edge is
ENTIRELY the right tail: the +2.2R target row contributes +0.3293 R and
removing it makes the sleeve gross -0.2433 R. Clipping winners at +1.0R turns
gross +0.1164 into -0.0801.

t1_hypothesis_battery.py varied target (C1-C4) and horizon (C8-C10) ONE AT A
TIME. That is the gap: a 3.0R target under a 16-bar horizon times out before it
is reached (target-hit fell 16.6% -> 12.5%). Target and horizon must move
together. Separately, longs gross +0.1631 R against shorts +0.0870 R, and 61%
of trades are shorts.

So the configuration space is target x horizon x side -- 18 cells, all
mechanistically motivated by the right-tail finding, not a fishing grid.

WHY WALK-FORWARD AND NOT A HOLDOUT
----------------------------------
The develop/validate split was spent by the 32-hypothesis battery. Picking the
best of 18 cells on 2021-2026 and reporting that number would convert OOS into
in-sample. Instead: at each rebalance, choose the configuration using ONLY
trailing 12-month data, then apply it to the next 6 months. Nothing is ever
selected with knowledge of the period it is scored on. The stitched result is
the honest estimate of what this system would have done.

The 2020-09 -> 2021-04 window that no window set ever touched is used as the
warm-up, so it is consumed rather than peeked at.

OBJECTIVE
---------
Selection maximises mean NET R per trade over the trailing window (capital per
trade is fixed, so per-trade efficiency is the right statistic). Configurations
with < MIN_TRADES trailing trades are ineligible; if none qualifies, production
geometry is used.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(ROOT))

from scratch.build_t1_experiments import label_path  # noqa: E402

TABLE = ROOT / "scratch" / "t1_experiments.parquet"

TARGETS = [2.20, 3.00, 4.00]
HORIZONS = [16, 24, 32]
SIDES = ["both", "long"]
RATCHET = ((1.40, 0.85), (0.75, 0.35))

PROD = dict(target=2.20, horizon=16, side="both")

REBALANCE_MONTHS = 6
TRAIL_MONTHS = 12
MIN_TRADES = 50
N_BOOT = 4000
RNG = np.random.default_rng(20260916)


def relabel(d: pd.DataFrame, target: float, horizon: int) -> pd.DataFrame:
    """Re-run the exit geometry over the stored forward path."""
    g = np.full(len(d), np.nan)
    net = np.full(len(d), np.nan)
    fr = d.fric_r.to_numpy()
    for i, r in enumerate(d.itertuples(index=False)):
        # label_path(hi, lo, cl, side, r_dist, fill_px, stress_mult,
        #            horizon, target, stop, ratchet) -> (gross_R, bars)
        rr, _ = label_path(np.asarray(r.fwd_h), np.asarray(r.fwd_l), np.asarray(r.fwd_c),
                           int(r.side), float(r.r_dist), float(r.fill_px), 1.0,
                           horizon, target, 1.0, RATCHET)
        g[i] = rr
        net[i] = rr - fr[i]
    return pd.DataFrame({"gross": g, "net": net}, index=d.index)


def build_grid(d: pd.DataFrame) -> dict:
    """Pre-label every (target, horizon) once; side is just a row filter."""
    out = {}
    for t in TARGETS:
        for h in HORIZONS:
            out[(t, h)] = relabel(d, t, h)
    return out


def config_frame(grid: dict, d: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    lab = grid[(cfg["target"], cfg["horizon"])]
    m = np.ones(len(d), bool)
    if cfg["side"] == "long":
        m = (d.side.to_numpy() == 1)
    return pd.DataFrame({
        "t": d.t.to_numpy()[m],
        "symbol": d.symbol.to_numpy()[m],
        "gross": lab.gross.to_numpy()[m],
        "net": lab.net.to_numpy()[m],
    })


def main() -> None:
    d = pd.read_parquet(TABLE)
    d = d[d.emitted.astype(bool)].reset_index(drop=True)
    d["t"] = pd.to_datetime(d.t, utc=True)
    print("=" * 100)
    print("WALK-FORWARD GEOMETRY SELECTION  (T1)")
    print("=" * 100)
    print(f"  {len(d)} emitted trades | gross {d.gross_r.mean():+.6f} | "
          f"fric {d.fric_r.mean():.6f} | net {(d.gross_r - d.fric_r).mean():+.6f} R/trade")

    grid = build_grid(d, )
    frames = {(t, h, s): config_frame(grid, d, dict(target=t, horizon=h, side=s))
              for t in TARGETS for h in HORIZONS for s in SIDES}
    print(f"  {len(frames)} pre-labelled configurations "
          f"({len(TARGETS)} targets x {len(HORIZONS)} horizons x {len(SIDES)} sides)")

    start = d.t.min().normalize()
    end = d.t.max().normalize()
    rebal = pd.date_range(start + pd.DateOffset(months=TRAIL_MONTHS), end,
                          freq=f"{REBALANCE_MONTHS}MS")
    print(f"  walk-forward: {rebal[0].date()} -> {end.date()}, "
          f"{len(rebal)} rebalances, {TRAIL_MONTHS}m trailing / {REBALANCE_MONTHS}m forward\n")

    picks, oos = [], []
    for rb in rebal:
        nxt = rb + pd.DateOffset(months=REBALANCE_MONTHS)
        tr_lo = rb - pd.DateOffset(months=TRAIL_MONTHS)

        best, best_v = None, -np.inf
        for key, fr in frames.items():
            trm = (fr.t >= tr_lo) & (fr.t < rb)
            n = int(trm.sum())
            if n < MIN_TRADES:
                continue
            v = float(fr.net.to_numpy()[trm].mean())
            if v > best_v:
                best, best_v = key, v
        if best is None:
            best = (PROD["target"], PROD["horizon"], PROD["side"])
            best_v = np.nan

        om = (d.t >= rb) & (d.t < nxt)
        fr = frames[best]
        sel = fr[(fr.t >= rb) & (fr.t < nxt)]
        base = d[om]
        picks.append(dict(rebal=rb.date(), cfg=f"T{best[0]:.1f}/H{best[1]}/{best[2]}",
                          trail_net=best_v, n_trail=int(((frames[best].t >= tr_lo) &
                                                         (frames[best].t < rb)).sum()),
                          n_oos=len(sel)))
        oos.append(sel)

    P = pd.DataFrame(picks)
    print("  rebalance  config           trailing net R/trade   n_trail   n_oos")
    for _, r in P.iterrows():
        print(f"  {str(r.rebal):<11}{r.cfg:<17}{r.trail_net:>+10.4f}"
              f"{r.n_trail:>14}{r.n_oos:>10}")

    O = pd.concat(oos, ignore_index=True)
    days = O.t.dt.floor("D").astype("int64").to_numpy()
    uniq = np.unique(days)
    dmap = {k: i for i, k in enumerate(uniq)}
    idx = np.array([dmap[x] for x in days])
    obs = float(O.net.mean())

    boots = np.empty(N_BOOT)
    for b in range(N_BOOT):
        s = RNG.integers(0, len(uniq), len(uniq))
        m = np.isin(idx, s)
        boots[b] = O.net.to_numpy()[m].mean() if m.any() else 0.0
    p = float((boots <= 0).mean())

    print("\n" + "=" * 100)
    print("WALK-FORWARD RESULT vs PRODUCTION")
    print("=" * 100)
    prod_oos = d[(d.t >= rebal[0])]
    print(f"  {'':<34}{'n':>7}{'gross':>10}{'fric':>9}{'NET':>10}{'total R':>10}")
    print(f"  {'production geometry (fixed)':<34}{len(prod_oos):>7}"
          f"{prod_oos.gross_r.mean():>+10.4f}{prod_oos.fric_r.mean():>9.4f}"
          f"{(prod_oos.gross_r - prod_oos.fric_r).mean():>+10.4f}"
          f"{(prod_oos.gross_r - prod_oos.fric_r).sum():>+10.1f}")
    print(f"  {'WALK-FORWARD SELECTED':<34}{len(O):>7}{O.gross.mean():>+10.4f}"
          f"{(O.gross - O.net).mean():>9.4f}{obs:>+10.4f}{O.net.sum():>+10.1f}")
    print(f"\n  walk-forward net {obs:+.4f} R/trade | day-clustered bootstrap "
          f"P(net<=0) = {p:.4f}")
    print(f"  profitable: {'YES' if obs > 0 else 'NO'}")
    P.to_csv(ROOT / "scratch" / "wf_picks.csv", index=False)
    O.to_parquet(ROOT / "scratch" / "wf_oos.parquet", index=False)
    print("  -> scratch/wf_picks.csv, scratch/wf_oos.parquet")


if __name__ == "__main__":
    main()
