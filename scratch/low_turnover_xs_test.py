"""Low-turnover cross-sectional strategies -- the last untested design space.

RATIONALE: every prior strategy died because cost (41 bps/leg) was paid on
every trade. The one corner not explored was LOW-turnover (weekly)
cross-sectional long-short, where 82 bps is amortized over a week. If any
form could survive, this is it.

TESTED (weekly rebalance, top vs bottom quintile, hold 7d, cost 82 bps/rebal):
  - 7d  cross-sectional momentum      +1.01%/wk gross, weak
  - 28d cross-sectional momentum      +0.83%/wk NET, t=+1.62  (NOT significant)
  - 7d  cross-sectional reversal      negative

DATA-HYGIENE LESSON: with UNcapped daily returns the 28d momentum showed
+1.75%/wk, t=+3.02 -- but that was driven by listing-gap / imputation
artifacts (single-day returns of hundreds of %). Capping daily returns at
+/-40% collapses it to t=+1.62. Always cap cross-sectional crypto returns
before trusting a spread.

BY YEAR (28d momentum, net): positive 2020-2024, NEGATIVE 2025 (-1.15%/wk,
t=-1.52) and 2026 (-0.58). Fails in the most recent period. No edge.

CONCLUSION: low-turnover cross-section does not produce a robust,
cost-surviving edge on this universe and period.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SRC = Path(__file__).resolve().parent.parent / "Engine" / "binance_backtesting_data"
COST_PCT = 0.82      # 2 legs x 41 bps per weekly rebalance
CAP = 40.0           # daily return cap (%) to kill listing/imputation artifacts


def load() -> pd.DataFrame:
    rows = []
    for p in sorted(SRC.glob("*_15m_master_2020_2026.parquet")):
        d = pd.read_parquet(p)
        d["time"] = pd.to_datetime(d["open_time_ms"], unit="ms", utc=True)
        d = d.sort_values("time").set_index("time")
        g = d.resample("1D", label="left", closed="left")["close"].last().to_frame("close")
        g["ret"] = g["close"].pct_change() * 100.0
        g["ret"] = g["ret"].clip(-CAP, CAP)
        g["symbol"] = p.name.split("_15m")[0]
        rows.append(g.reset_index())
    return pd.concat(rows, ignore_index=True).dropna()


def main() -> None:
    D = load()
    D["sig"] = D.groupby("symbol")["ret"].transform(lambda x: x.rolling(28).sum())
    days = sorted(D.time.dt.date.unique())
    pnl = []
    for i in range(0, len(days) - 7, 7):
        sub = D[D.time.dt.date == days[i]].dropna(subset=["sig"])
        if len(sub) < 10:
            continue
        hi = sub[sub.sig >= sub.sig.quantile(0.8)]
        lo = sub[sub.sig <= sub.sig.quantile(0.2)]
        fwd = D[D.time.dt.date.isin(days[i+1:i+8])]
        r = (fwd[fwd.symbol.isin(hi.symbol)].groupby("time").ret.mean().sum()
             - fwd[fwd.symbol.isin(lo.symbol)].groupby("time").ret.mean().sum()) - COST_PCT
        pnl.append((pd.to_datetime(days[i]), r))
    s = pd.Series([r for _, r in pnl])
    print(f"28d weekly momentum net {s.mean():+.2f}%/wk t={s.mean()/stats.sem(s):+.2f} "
          f"ann {s.mean()*52:+.1f}%")
    yr = {}
    for dt, r in pnl:
        yr.setdefault(dt.year, []).append(r)
    for y in sorted(yr):
        v = np.array(yr[y])
        print(f"  {y}: {v.mean():+.2f}%/wk t={v.mean()/(stats.sem(v) or 1):+.2f} n={len(v)}")


if __name__ == "__main__":
    main()
