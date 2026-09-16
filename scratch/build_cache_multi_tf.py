"""Rebuild the 4h multi-timeframe cache from the 15m master parquets.

RECONSTRUCTED 2026-09-16 after a sandbox re-clone destroyed both this script and
scratch/cache_multi_tf/. The feature definitions are taken from the surviving
consumers, which are the only ground truth available:

  Engine/strategy/t1_breakout.py      -- gate + labeler (lines 85-200)
  Engine/execution_costs.py           -- build_stress_series (lines 93-130)
  scratch/build_t1_experiments.py     -- experiment table (lines 96-120)

Required 4h columns, and where each is pinned down:
  time            bar OPEN time, datetime64[ms, UTC].  t1_breakout.py:96 comments
                  that the cache stores ms, and .astype("int64") must yield
                  MILLISECONDS for the stress join to work.
  open/high/low/close   4h resample of the 15m bars.
  next_open       open.shift(-1)   -- t1_breakout.py:120 falls back to exactly
                  this when the column is absent, so the definition is pinned.
  atr             ATR(14) on 4h.
  donchian_high   high.rolling(20).max().shift(1)   -- "prior-20-bar Donchian",
  donchian_low    low.rolling(20).min().shift(1)       causal via shift(1).
  ema_20/50/200   EMA on 4h close.
  ema_200_slope   ema_200.diff(12)   -- 12 x 4h = 48h.
  buy_vol_ratio   taker buy fraction over the bar, in [0,1]. The gate at
                  t1_breakout.py:139 tests `buy_vol > 0.51` / `< 0.49`, so this
                  MUST be a fraction, not the master's taker_volume_ratio
                  (whose median is 1.00374, i.e. a buy/sell ratio).
  spot_cvd_slope  spot_cvd.rolling(3).sum() / volume_base.rolling(3).sum().
                  The gate tests `cvd_slope > 0` / `< 0`, so only the sign is
                  load-bearing; the volume normalisation keeps it comparable
                  across coins.
  volume_base     sum of 15m volume_base over the bar.

CAUSALITY: donchian uses .shift(1) so a bar never sees its own high/low;
ema_200_slope uses .diff(12) on completed bars; next_open is the *next* bar's
open, used only as the fill price for a signal confirmed on the current bar's
close. Nothing here peeks forward into the bar being labelled.

The builder makes NO claim of bit-identity with the lost cache. Run
`python3 scratch/verify_cache_rebuild.py` to test whether load_t1_breakout_trades()
still reproduces the audited 2,972 trades / +0.116439 R gross.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Engine" / "binance_backtesting_data"
OUT = ROOT / "scratch" / "cache_multi_tf"
OUT.mkdir(parents=True, exist_ok=True)

RULE = "4h"
DONCHIAN = 20
ATR_N = 14
CVD_WIN = 3
SLOPE_LAG = 12


def wilder_atr(h: pd.Series, l: pd.Series, c: pd.Series, n: int = ATR_N) -> pd.Series:
    """Wilder's smoothed ATR -- the convention behind every atr_* column in the
    15m masters, which carry atr_14 / atr_100."""
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def build_one(path: Path) -> pd.DataFrame:
    d = pd.read_parquet(path)
    d["time"] = pd.to_datetime(d["open_time_ms"], unit="ms", utc=True)
    d = d.sort_values("time").reset_index(drop=True)

    g = d.set_index("time")
    ohlc = g.resample(RULE, label="left", closed="left").agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume_base=("volume_base", "sum"),
        taker_buy=("taker_buy_vol_btc", "sum"),
        taker_sell=("taker_sell_vol_btc", "sum"),
        spot_cvd=("spot_cvd_15m", "sum"),
    ).dropna(subset=["open", "high", "low", "close"])

    # taker buy FRACTION, not ratio -- see module docstring.
    tv = (ohlc["taker_buy"] + ohlc["taker_sell"]).replace(0.0, np.nan)
    ohlc["buy_vol_ratio"] = (ohlc["taker_buy"] / tv).fillna(0.5)

    ohlc["atr"] = wilder_atr(ohlc["high"], ohlc["low"], ohlc["close"])
    ohlc["donchian_high"] = ohlc["high"].rolling(DONCHIAN).max().shift(1)
    ohlc["donchian_low"] = ohlc["low"].rolling(DONCHIAN).min().shift(1)

    for span in (20, 50, 200):
        ohlc[f"ema_{span}"] = ohlc["close"].ewm(span=span, adjust=False).mean()
    ohlc["ema_200_slope"] = ohlc["ema_200"].diff(SLOPE_LAG)

    vsum = ohlc["volume_base"].rolling(CVD_WIN).sum().replace(0.0, np.nan)
    ohlc["spot_cvd_slope"] = (ohlc["spot_cvd"].rolling(CVD_WIN).sum() / vsum).fillna(0.0)

    ohlc["next_open"] = ohlc["open"].shift(-1)

    out = ohlc[["open", "high", "low", "close", "volume_base", "atr",
                "donchian_high", "donchian_low", "ema_20", "ema_50", "ema_200",
                "ema_200_slope", "buy_vol_ratio", "spot_cvd_slope",
                "next_open"]].copy()
    # The consumers do pd.to_datetime(df["time"], utc=True) then .astype("int64")
    # and REQUIRE milliseconds. datetime64[ms] is what makes that true.
    out.index = out.index.astype("datetime64[ms, UTC]")
    out.index.name = "time"
    return out.reset_index()


def main() -> None:
    srcs = sorted(SRC.glob("*_15m_master_2020_2026.parquet"))
    assert srcs, f"no 15m masters under {SRC}"
    total = 0
    for p in srcs:
        sym = p.name.split("_15m")[0]
        df = build_one(p)
        df.to_parquet(OUT / f"{sym}_4h.parquet", index=False)
        total += len(df)
        print(f"  {sym:<10} {len(df):>6} bars  {df.time.min()} .. {df.time.max()}")
    print(f"\n  {len(srcs)} symbols, {total:,} 4h bars -> {OUT}")

    chk = pd.read_parquet(OUT / "BTCUSDT_4h.parquet")
    print(f"  time dtype: {chk.time.dtype}")
    print(f"  ms check  : {int(chk.time.astype('int64').iloc[200])} "
          f"-> {pd.to_datetime(int(chk.time.astype('int64').iloc[200]), unit='ms', utc=True)}")


if __name__ == "__main__":
    main()
