"""Replication of ssrn-5020002 (Alexia 2024, 'Order Flow and Cryptocurrency
Returns') cross-sectional mechanism on our data.

The paper: world order flow predicts the cross-section of crypto returns;
daily long-short (P5-P1) sorted on ML order-flow forecasts returns 0.17-0.79%
/day, Sharpe up to 3.63, on Feb 2020 - Jun 2022 (a bull sample), pre-cost,
daily rebalanced.

Our testable analog: per-symbol daily taker order-flow imbalance
(buy-sell)/(buy+sell); yesterday's OF predicts today's return; long top
tercile / short bottom tercile, rebalanced daily, over the FULL period
2020-09 -> 2026-09 (bull AND bear). Cost = 2 legs x 41 bps = 82 bps/day at
full daily turnover.

RESULT (this run): gross spread +9.6 bps/day (t=+1.90). Far below the paper's
claim and an order of magnitude below the 82 bps/day cost. Net -72.4 bps/day.
The orderflow cross-section is real but not tradeable at 41 bps -- consistent
with every other orderflow test in this repository.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SRC = Path(__file__).resolve().parent.parent / "Engine" / "binance_backtesting_data"
ROUND_TRIP_BPS = 41.0


def main() -> None:
    rows = []
    for p in sorted(SRC.glob("*_15m_master_2020_2026.parquet")):
        d = pd.read_parquet(p)
        d["time"] = pd.to_datetime(d["open_time_ms"], unit="ms", utc=True)
        d = d.sort_values("time").set_index("time")
        g = d.resample("1D", label="left", closed="left").agg(
            close=("close", "last"),
            tb=("taker_buy_vol_btc", "sum"),
            ts=("taker_sell_vol_btc", "sum"))
        g["ret"] = g["close"].pct_change()
        g["of"] = (g["tb"] - g["ts"]) / (g["tb"] + g["ts"])
        g["sig"] = g["of"].shift(1)
        g["symbol"] = p.name.split("_15m")[0]
        rows.append(g[["ret", "sig", "symbol"]].reset_index())
    D = pd.concat(rows, ignore_index=True).dropna()

    spread = []
    for dt in sorted(D.time.dt.date.unique()):
        sub = D[D.time.dt.date == dt]
        if len(sub) < 8:
            continue
        spread.append(sub.ret[sub.sig >= sub.sig.quantile(2/3)].mean()
                      - sub.ret[sub.sig <= sub.sig.quantile(1/3)].mean())
    s = pd.Series(spread)
    gbps = s.mean() * 10000
    cost = 2 * ROUND_TRIP_BPS
    print(f"daily long-highOF/short-lowOF gross = {gbps:+.1f} bps/day "
          f"(t={s.mean()/stats.sem(s):+.2f}, n={len(s)})")
    print(f"cost 2x{ROUND_TRIP_BPS:.0f} bps = {cost:.0f} bps/day; "
          f"NET {gbps-cost:+.1f} bps/day; annualised {(gbps-cost)*365/100:+.1f}%")


if __name__ == "__main__":
    main()
