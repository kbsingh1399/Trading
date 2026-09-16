"""Orderflow-derived gates for T1 -- corpus-informed, data-bounded test.

The corpus holds ~270 funding/carry papers, ~39 liquidation papers and ~219
trade-imbalance papers. The 15m masters carry the trade-level aggregates those
mechanisms need (we have NO L2 book, so book-microstructure signals are out of
scope and already recorded as dead ends):

    funding_rate_pct                    perpetual carry / crowdedness
    long/short_liq_usd, liq_imbalance   liquidation cascades
    zc_div                              spot vs futures CVD divergence
    oi_change_pct                       OI-price divergence
    avg_trade_size_usd                  large-player activity
    taker buy/sell vol                  taker imbalance beyond the existing gate

Each feature is reduced to 4h and converted to a CAUSAL trailing z-score
(270 x 4h = 45 days). z is vectorised (rolling mean/std) so the build is fast,
and the current bar's aggregate is known at the bar close when the signal is
generated, so including it is causal.

Gates are pre-declared and direction-aware: the sign comes from the mechanism
(carry says the crowded side underperforms; a squeeze fuels the opposite side),
NOT from this data. Tested as kept-vs-dropped gross-R contrasts with the
day-clustered bootstrap, Holm-corrected across the family.

This is a SELECTION gate on the improved geometry -- NOT a new 15m-frequency
strategy (41 bps kills those; Sleeve C liquidation absorption was -786.30 R).
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SRC = ROOT / "Engine" / "binance_backtesting_data"
TABLE = ROOT / "scratch" / "t1_experiments.parquet"
WIN = 270                       # 270 x 4h = 45 days
Q = 0.674                       # ~75th percentile of a normal
N_BOOT = 4000
RNG = np.random.default_rng(20260917)


def feat4h(path: Path) -> pd.DataFrame:
    d = pd.read_parquet(path)
    d["time"] = pd.to_datetime(d["open_time_ms"], unit="ms", utc=True)
    d = d.sort_values("time").set_index("time")
    g = d.resample("4h", label="left", closed="left").agg(
        funding=("funding_rate_pct", "mean"),
        liq_long=("long_liq_usd", "sum"),
        liq_short=("short_liq_usd", "sum"),
        zc=("zc_div", "mean"),
        oi_chg=("oi_change_pct", "sum"),
        whale=("avg_trade_size_usd", "mean"),
        tb=("taker_buy_vol_btc", "sum"),
        ts=("taker_sell_vol_btc", "sum"),
    )
    g["liq_imb"] = ((g["liq_short"] - g["liq_long"]) /
                    (g["liq_short"] + g["liq_long"] + 1e-9)).clip(-1, 1)
    g["tk_imb"] = ((g["tb"] - g["ts"]) / (g["tb"] + g["ts"])).clip(-1, 1)
    g = g[["funding", "liq_imb", "zc", "oi_chg", "whale", "tk_imb"]]
    for c in g.columns:
        mu = g[c].rolling(WIN, min_periods=60).mean()
        sd = g[c].rolling(WIN, min_periods=60).std().replace(0.0, np.nan)
        g[c] = ((g[c] - mu) / sd).fillna(0.0).clip(-5, 5)
    return g


def holm(p):
    p = np.asarray(p, float); n = len(p); order = np.argsort(p)
    adj = np.empty(n); runmax = 0.0
    for rank, i in enumerate(order):
        runmax = max(runmax, (n - rank) * p[i])
        adj[i] = min(runmax, 1.0)
    return adj


def cluster_p(a, b, days_a, days_b, nb=N_BOOT):
    yy = np.concatenate([days_a, days_b])
    aa = np.concatenate([a, np.full(len(b), np.nan)])
    bb = np.concatenate([np.full(len(a), np.nan), b])
    uniq = np.unique(yy); dm = {k: i for i, k in enumerate(uniq)}
    idx = np.array([dm[x] for x in yy])
    obs = float(a.mean() - b.mean())
    cnt = 0
    for _ in range(nb):
        s = RNG.integers(0, len(uniq), len(uniq)); m = np.isin(idx, s)
        xa, xb = aa[m], bb[m]
        xa, xb = xa[np.isfinite(xa)], xb[np.isfinite(xb)]
        if len(xa) and len(xb):
            cnt += (xa.mean() - xb.mean()) <= 0.0
    return obs, cnt / nb


def main() -> None:
    exp = pd.read_parquet(TABLE)
    exp = exp[exp.emitted.astype(bool)].reset_index(drop=True)
    exp["t"] = pd.to_datetime(exp.t, utc=True)

    feats = []
    for p in sorted(SRC.glob("*_15m_master_2020_2026.parquet")):
        f = feat4h(p).reset_index().rename(columns={"time": "t"})
        f["symbol"] = p.name.split("_15m")[0]
        feats.append(f)
    F = pd.concat(feats, ignore_index=True)

    m = exp.merge(F, on=["symbol", "t"], how="left")
    print(f"join coverage: {m.funding.notna().mean()*100:.2f}% of {len(m)} trades")

    S = m.side.to_numpy()
    gates = [
        # carry: crowded longs (funding very positive) underperform -> drop them
        ("G1 drop crowded-long longs",  ~((S == 1) & (m.funding.to_numpy() > Q))),
        ("G2 drop crowded-short shorts", ~((S == -1) & (m.funding.to_numpy() < -Q))),
        # liquidation fuel: squeeze of one side supports the opposite side
        ("G3 longs need short-liq fuel", ~((S == 1) & (m.liq_imb.to_numpy() < 0))),
        ("G4 shorts need long-liq fuel", ~((S == -1) & (m.liq_imb.to_numpy() > 0))),
        # spot CVD leading futures up supports longs
        ("G5 longs when spot leads",     ~((S == 1) & (m.zc.to_numpy() < 0))),
        # falling OI with a long = weak -> drop
        ("G6 drop longs on falling OI",  ~((S == 1) & (m.oi_chg.to_numpy() < -Q))),
        # large players active -> prefer
        ("G7 keep whale-active",         (m.whale.to_numpy() > 0) | np.isnan(m.whale.to_numpy())),
        # taker imbalance beyond the 0.51 gate
        ("G8 keep strong taker side",
         ((S == 1) & (m.tk_imb.to_numpy() > 0)) | ((S == -1) & (m.tk_imb.to_numpy() < 0))),
    ]

    rows = []
    for name, keep in gates:
        keep = keep.astype(bool)
        g = m.gross_r.to_numpy()
        a, b = g[keep], g[~keep]
        if len(a) < 30 or len(b) < 30:
            continue
        da = m.t.dt.floor("D").astype("int64").to_numpy()[keep]
        db = m.t.dt.floor("D").astype("int64").to_numpy()[~keep]
        obs, p = cluster_p(a, b, da, db)
        rows.append(dict(gate=name, n_keep=len(a), n_drop=len(b),
                         keep_gross=a.mean(), drop_gross=b.mean(),
                         delta=obs, p_raw=p))
    R = pd.DataFrame(rows)
    R["p_holm"] = holm(R.p_raw.to_numpy())

    print("\n" + "=" * 112)
    print("ORDERFLOW GATES ON T1  (kept-vs-dropped gross R, day-clustered bootstrap, Holm)")
    print("=" * 112)
    print(f"{'gate':<32}{'n_keep':>7}{'n_drop':>7}{'keep':>9}{'drop':>9}"
          f"{'delta':>8}{'p raw':>8}{'p holm':>8}")
    for _, r in R.sort_values("p_raw").iterrows():
        print(f"{r.gate[:31]:<32}{r.n_keep:>7}{r.n_drop:>7}{r.keep_gross:>+9.4f}"
              f"{r.drop_gross:>+9.4f}{r.delta:>+8.4f}{r.p_raw:>8.4f}{r.p_holm:>8.4f}")
    surv = R[(R.p_holm < 0.05) & (R.delta > 0)]
    print(f"\n  surviving (Holm p<0.05 and delta>0): {len(surv)} of {len(R)}")
    R.to_csv(ROOT / "scratch" / "orderflow_gate_results.csv", index=False)
    print("  -> scratch/orderflow_gate_results.csv")


if __name__ == "__main__":
    main()
