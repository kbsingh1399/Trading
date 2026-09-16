"""T1 walk-forward geometry selection.

STATUS: NOT PROFITABLE. This module reduces T1's bleed; it does not give it
edge. Read EDGE_SYSTEM.md before using it. It exists so the measurement is
reproducible, not because it is deployable.

WHAT IT DOES
------------
Production T1 fixes its exit geometry forever: target +2.20R, horizon 16 bars,
both sides. This module instead re-selects (target, horizon, side) every
`rebalance_months` using ONLY the trailing `trail_months` of trades, maximising
mean net R per trade. Nothing is ever chosen with knowledge of the period it is
scored on.

WHY THE SPACE IS WHAT IT IS
---------------------------
T1_AUDIT.md established the edge is entirely the right tail: the +2.2R target
row contributes +0.3293 R and removing it makes the sleeve gross -0.2433 R.
The 32-hypothesis battery varied target (C1-C4) and horizon (C8-C10) one at a
time and found nothing. They must move together -- a 3.0R target under a 16-bar
horizon times out before it is reached. Side is included because longs gross
+0.1631 R against shorts +0.0870 R while 61% of trades are shorts.

Eighteen cells. All mechanistically motivated; none discovered by searching.

MEASURED RESULT (see EDGE_SYSTEM.md for the full accounting)
-----------------------------------------------------------
    production fixed geometry   net -0.0928 R/trade
    this module, 7 settings     net -0.1088 .. -0.0017, median -0.0432
    oracle best fixed config    net -0.0068 R/trade   (chosen with hindsight)

Six of seven settings beat production. NONE is positive. The best single
setting (-0.0017) is the maximum of seven and must not be quoted as the
expected result -- that is the selection bias this repository keeps falling into.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parent.parent.parent

# Exit-geometry search space. See module docstring for why these and not others.
TARGETS: tuple[float, ...] = (2.20, 3.00, 4.00)
HORIZONS: tuple[int, ...] = (16, 24, 32)
SIDES: tuple[str, ...] = ("both", "long")

# Production geometry, used as the fallback when nothing qualifies.
PRODUCTION = dict(target=2.20, horizon=16, side="both")

RATCHET = ((1.40, 0.85), (0.75, 0.35))
STOP_R = 1.00

# Walk-forward cadence. 12m/6m is the DEFAULT, not the optimum -- the optimum
# was -0.0017 R/trade and quoting it would be reporting the max of 7 settings.
TRAIL_MONTHS = 12
REBALANCE_MONTHS = 6
MIN_TRADES = 50


@dataclass(frozen=True)
class Config:
    target: float
    horizon: int
    side: str

    def __str__(self) -> str:
        return f"T{self.target:.1f}/H{self.horizon}/{self.side}"


def all_configs() -> list[Config]:
    return [Config(t, h, s) for t in TARGETS for h in HORIZONS for s in SIDES]


def select(trades: pd.DataFrame,
           net_by_config: dict,
           as_of: pd.Timestamp,
           trail_months: int = TRAIL_MONTHS,
           min_trades: int = MIN_TRADES) -> tuple[Config, float, int]:
    """Pick the best configuration using only trades strictly before `as_of`.

    `net_by_config` maps each Config to a net-R-per-trade array aligned row-for-
    row with `trades`. Selection needs the outcome under every candidate
    geometry, so the caller must pre-label; see scratch/walk_forward_geometry.py
    for the labeller, which asserts against production.

    Returns (config, trailing_net_r_per_trade, n_trailing_trades). Falls back to
    PRODUCTION when no configuration has enough history.
    """
    lo = as_of - pd.DateOffset(months=trail_months)
    m = ((trades.t >= lo) & (trades.t < as_of)).to_numpy()

    best, best_v, best_n = Config(**PRODUCTION), float("nan"), 0
    for cfg, net in net_by_config.items():
        sel = net[m]
        sel = sel[np.isfinite(sel)]
        if len(sel) < min_trades:
            continue
        v = float(sel.mean())
        if not np.isfinite(best_v) or v > best_v:
            best, best_v, best_n = cfg, v, len(sel)
    return best, best_v, best_n


def rebalance_dates(trades: pd.DataFrame,
                    trail_months: int = TRAIL_MONTHS,
                    rebalance_months: int = REBALANCE_MONTHS) -> pd.DatetimeIndex:
    start = trades.t.min().normalize()
    end = trades.t.max().normalize()
    return pd.date_range(start + pd.DateOffset(months=trail_months), end,
                         freq=f"{rebalance_months}MS")
