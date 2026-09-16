"""Funding-carry strategy test -- the largest corpus family (270 papers).

WHY THIS WAS WORTH TESTING
--------------------------
Carry is structurally different from every directional strategy tested before:
it EARNS the perpetual funding payment and holds for days/weeks, so the 41 bps
round trip is amortized over many funding accruals instead of being paid on
every trade. If any strategy form could survive 41 bps, this is it.

THE BUG THIS FILE DOCUMENTS
---------------------------
funding_rate_pct in the 15m masters is a per-8h rate STAMPED ON EVERY 15m BAR.
Summing it over a calendar day therefore counts each of the 3 daily payments
32x, inflating the carry term ~32x. A naive first run reported +1.3..+2.0%/day
(t=+16) -- a completely spurious "edge". The correct daily funding is the sum
over the 3 eight-hour payment timestamps only (open_time_ms % 8h == 0).

CORRECTED RESULT (this file)
----------------------------
Cross-sectional carry: each rebalance, short the top tercile of funding
(earn their funding), long the bottom tercile, dollar-neutral, hold H days.

    hold   funding  price   fric    NET      t      annualised
     1d    +0.062   +0.113  0.820   -0.645   -10.7   -235%
     3d    +0.020   +0.084  0.273   -0.170    -2.9    -62%
     7d    +0.009   +0.089  0.117   -0.019    -0.3     -7%
    14d    +0.005   +0.079  0.059   +0.026    +0.4     +9%   (t=0.41, no edge)

The funding spread mean-reverts fast (0.062 at 1d -> 0.005 at 14d), so holding
long enough to amortize friction leaves almost no carry. The residual price
term (long-low/short-high funding as a contrarian) is +0.08%/d but at 14d the
whole thing nets +0.026%/d with t=0.41 -- not significant.

CONCLUSION: funding carry does NOT produce edge net of 41 bps once the
accounting is correct. The corpus's 270 carry papers describe a payment that
is real but, on this universe and period, too small and too mean-reverting to
survive realistic costs.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SRC = Path(__file__).resolve().parent.parent / "Engine" / "binance_backtesting_data"
ROUND_TRIP_BPS = 41.0
EIGHT_H = 8 * 3600000


def load() -> pd.DataFrame:
    rows = []
    for p in sorted(SRC.glob("*_15m_master_2020_2026.parquet")):
        d = pd.read_parquet(p)
        d["time"] = pd.to_datetime(d["open_time_ms"], unit="ms", utc=True)
        d = d.sort_values("time").set_index("time")
        pay = d[d["open_time_ms"] % EIGHT_H == 0]          # one row per payment
        g = pay.resample("1D", label="left", closed="left")["funding_rate_pct"].sum()
        g = g.to_frame("funding")
        g["close"] = d.resample("1D", label="left", closed="left")["close"].last()
        g["ret"] = g["close"].pct_change() * 100.0
        g["symbol"] = p.name.split("_15m")[0]
        rows.append(g.reset_index())
    return pd.concat(rows, ignore_index=True).dropna()


def main() -> None:
    D = load()
    days = sorted(D.time.dt.date.unique())
    print(f"{'hold':>4}{'fund':>8}{'price':>8}{'fric':>7}{'NET':>9}{'t':>7}{'ann':>9}")
    for hold in (1, 3, 7, 14):
        pnl, fund, pr = [], [], []
        for i in range(0, len(days) - hold, hold):
            sub = D[D.time.dt.date == days[i]]
            if len(sub) < 8:
                continue
            top = sub[sub.funding >= sub.funding.quantile(2/3)]
            bot = sub[sub.funding <= sub.funding.quantile(1/3)]
            f = (top.funding.mean() - bot.funding.mean()) / hold
            fwd = D[D.time.dt.date.isin(days[i+1:i+1+hold])]
            p_ = (fwd[fwd.symbol.isin(bot.symbol)].groupby("time").ret.mean().sum()
                  - fwd[fwd.symbol.isin(top.symbol)].groupby("time").ret.mean().sum()) / hold
            fr = 2 * ROUND_TRIP_BPS / 100.0 / hold
            fund.append(f); pr.append(p_); pnl.append(f + p_ - fr)
        s = pd.Series(pnl)
        print(f"{hold:>4}{np.mean(fund):>+8.4f}{np.mean(pr):>+8.4f}"
              f"{2*ROUND_TRIP_BPS/100/hold:>7.4f}{s.mean():>+9.4f}"
              f"{s.mean()/stats.sem(s):>+7.2f}{s.mean()*365:>+9.1f}")


if __name__ == "__main__":
    main()
