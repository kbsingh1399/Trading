"""Abstain rule on top of the walk-forward geometry selector.

PRE-DECLARED RULE (defensive only -- consistent with the standing constraint
that governors may only ever be penalty branches, never lower a threshold):

    If the best eligible configuration has NET R/trade <= 0 over the trailing
    12 months, take NO trades in the forward window.

Rationale that needs no data: a selector whose best available option lost money
over the last year has no edge to deploy. Trading anyway is not a strategy, it
is inertia.

HONESTY DISCLOSURE: this rule was added AFTER seeing that 3 of the 10 walk-
forward windows had negative trailing net. That is a post-hoc design choice.
It uses only trailing information, so the evaluation remains walk-forward, but
the decision to introduce it was informed by the output. Both variants are
reported and both are bootstrapped so the reader can discount accordingly.
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scratch.walk_forward_geometry import (  # noqa: E402
    TABLE, TARGETS, HORIZONS, SIDES, PROD, RATCHET,
    REBALANCE_MONTHS, TRAIL_MONTHS, MIN_TRADES, N_BOOT, RNG,
    build_grid, config_frame, relabel,
)


def clustered_p(net: np.ndarray, days: np.ndarray, n_boot: int = N_BOOT) -> float:
    """One-sided day-clustered bootstrap P(mean <= 0)."""
    uniq = np.unique(days)
    dmap = {k: i for i, k in enumerate(uniq)}
    idx = np.array([dmap[x] for x in days])
    obs = float(net.mean())
    boots = np.empty(n_boot)
    for b in range(n_boot):
        s = RNG.integers(0, len(uniq), len(uniq))
        m = np.isin(idx, s)
        boots[b] = net[m].mean() if m.any() else 0.0
    return obs, float((boots <= 0).mean()), boots.std()


def main() -> None:
    d = pd.read_parquet(TABLE)
    d = d[d.emitted.astype(bool)].reset_index(drop=True)
    d["t"] = pd.to_datetime(d.t, utc=True)

    grid = build_grid(d)
    frames = {(t, h, s): config_frame(grid, d, dict(target=t, horizon=h, side=s))
              for t in TARGETS for h in HORIZONS for s in SIDES}

    start, end = d.t.min().normalize(), d.t.max().normalize()
    rebal = pd.date_range(start + pd.DateOffset(months=TRAIL_MONTHS), end,
                          freq=f"{REBALANCE_MONTHS}MS")

    rows, oos_traded, oos_abstain = [], [], []
    for rb in rebal:
        nxt = rb + pd.DateOffset(months=REBALANCE_MONTHS)
        tr_lo = rb - pd.DateOffset(months=TRAIL_MONTHS)

        best, best_v = None, -np.inf
        for key, fr in frames.items():
            trm = (fr.t >= tr_lo) & (fr.t < rb)
            if int(trm.sum()) < MIN_TRADES:
                continue
            v = float(fr.net.to_numpy()[trm].mean())
            if v > best_v:
                best, best_v = key, v
        if best is None:
            best = (PROD["target"], PROD["horizon"], PROD["side"])
            best_v = np.nan

        fr = frames[best]
        sel = fr[(fr.t >= rb) & (fr.t < nxt)]
        trade = np.isfinite(best_v) and best_v > 0

        rows.append(dict(rebal=rb.date(), cfg=f"T{best[0]:.1f}/H{best[1]}/{best[2]}",
                         trail_net=best_v, n_oos=len(sel),
                         action="TRADE" if trade else "ABSTAIN",
                         oos_net=float(sel.net.mean()) if len(sel) else np.nan))
        oos_traded.append(sel)
        if trade:
            oos_abstain.append(sel)

    P = pd.DataFrame(rows)
    print("=" * 104)
    print("WALK-FORWARD GEOMETRY SELECTION + ABSTAIN RULE")
    print("=" * 104)
    print("  rebalance  config           trailing   n_oos  action    oos net R")
    for _, r in P.iterrows():
        print(f"  {str(r.rebal):<11}{r.cfg:<17}{r.trail_net:>+9.4f}{r.n_oos:>8}"
              f"  {r.action:<8}{r.oos_net:>+11.4f}")

    A = pd.concat(oos_traded, ignore_index=True)
    B = pd.concat(oos_abstain, ignore_index=True)
    prod = d[d.t >= rebal[0]]

    print("\n" + "=" * 104)
    print(f"  {'variant':<38}{'n':>7}{'gross':>10}{'fric':>9}{'NET':>10}{'total R':>10}"
          f"{'P(net<=0)':>11}")
    print("-" * 104)
    for name, df_, gc, fc, nc in [
        ("production geometry (fixed)", prod, prod.gross_r.to_numpy(),
         prod.fric_r.to_numpy(), (prod.gross_r - prod.fric_r).to_numpy()),
        ("walk-forward, always trade", A, A.gross.to_numpy(),
         (A.gross - A.net).to_numpy(), A.net.to_numpy()),
        ("walk-forward + ABSTAIN", B, B.gross.to_numpy(),
         (B.gross - B.net).to_numpy(), B.net.to_numpy()),
    ]:
        days = (df_.t.dt.floor("D").astype("int64").to_numpy())
        obs, p, sd = clustered_p(nc, days)
        print(f"  {name:<38}{len(df_):>7}{gc.mean():>+10.4f}{fc.mean():>9.4f}"
              f"{obs:>+10.4f}{nc.sum():>+10.1f}{p:>11.4f}")

    print()
    for name, df_ in [("always trade", A), ("+ ABSTAIN", B)]:
        yr = df_.t.dt.year
        print(f"  {name:<14} by year: " + "  ".join(
            f"{y}:{df_.net.to_numpy()[yr == y].mean():+.3f}({int((yr == y).sum())})"
            for y in sorted(yr.unique())))

    P.to_csv(ROOT / "scratch" / "wf_abstain_picks.csv", index=False)
    B.to_parquet(ROOT / "scratch" / "wf_abstain_oos.parquet", index=False)
    print("\n  -> scratch/wf_abstain_picks.csv, scratch/wf_abstain_oos.parquet")


if __name__ == "__main__":
    main()
