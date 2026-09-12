"""Order-flow features from the shipped Binance footprint ladder.

The master tables only carry aggregate taker flow (``future_cvd_15m``).  The
shipped footprint ladder resolves *each 15m candle into price bins* with
``bid_vol_coin`` / ``ask_vol_coin`` / ``net_delta_coin`` plus Binance's own
imbalance and stacked-imbalance flags and the true value-area / POC flags.

That is genuinely new information for the meta-labelling gate, which to date has
only seen OHLC-derived geometry (out-of-sample AUC ~0.52).  This module reduces
the ladder to one causal row per 15m candle and caches it as a small parquet so
``data.load_all`` can merge it without rebuilding the heavy feature frames.

All features are computed from the **completed** candle (bar close), so merging
them onto the signal bar introduces no look-ahead.

Notes
-----
* ``ladder_poc`` / ``ladder_vah`` / ``ladder_val`` come from Binance's own
  per-candle value-area flags, i.e. the exchange's binning, not our OHLC
  approximation (validated in ``levels.validate_profile``).
* A bar can straddle a row-group / batch boundary; per-batch aggregates are
  re-reduced by ``open_time_ms`` so sums and extrema stay exact.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from .data import CACHE_DIR, ladder_path

LADDER_COLUMNS = [
    "open_time_ms", "price_bin", "bid_vol_coin", "ask_vol_coin", "net_delta_coin",
    "total_vol_coin", "is_poc", "is_buy_imbalance", "is_sell_imbalance",
    "is_stacked_buy_imb", "is_stacked_sell_imb", "is_value_area",
]

RAW_COLUMNS = [
    "ld_delta", "ld_tv", "ld_buy_imb", "ld_sell_imb", "ld_stack_buy", "ld_stack_sell",
    "ld_bins", "ld_poc", "ld_val", "ld_vah",
    "ld_delta_hi", "ld_delta_lo", "ld_vol_hi", "ld_vol_lo", "ld_buyimb_hi", "ld_bins_hi",
]

FLOW_COLUMNS = [
    "ld_delta_rel", "ld_cvd_4", "ld_cvd_8", "ld_cvd_32", "ld_delta_z",
    "ld_imb_net", "ld_imb_net_8", "ld_stack_net",
    "ld_d_poc", "ld_d_vah", "ld_d_val", "ld_va_width", "ld_va_pos",
    "ld_bins_rel", "ld_rel_vol",
    # within-candle structure (top vs bottom third of the candle's range)
    "ld_delta_hi_rel", "ld_delta_lo_rel", "ld_delta_skew", "ld_poc_range_pos",
    "ld_buyimb_hi_frac",
]


def _reduce_batch(df: pd.DataFrame, rng: pd.DataFrame | None = None) -> pd.DataFrame:
    """Collapse one row-batch of the ladder to per-candle raw aggregates.

    ``rng`` maps ``open_time_ms`` -> ``rng_lo``/``rng_hi`` (the candle's own low/high
    from the master table) and lets us split each candle's bins into thirds, so we
    can tell aggressive buying *at the highs* (continuation) from aggressive buying
    *at the lows* (absorption / fade).
    """
    for c in ("net_delta_coin", "total_vol_coin", "bid_vol_coin", "ask_vol_coin", "price_bin"):
        df[c] = df[c].astype("float32")
    if rng is not None:
        idx = df["open_time_ms"].to_numpy()
        lo = rng["rng_lo"].reindex(idx).to_numpy(np.float32)
        hi = rng["rng_hi"].reindex(idx).to_numpy(np.float32)
        span = np.where(hi > lo, hi - lo, np.nan)
        pos = (df["price_bin"].to_numpy(np.float32) - lo) / span
        pos = np.clip(pos, 0.0, 1.0)
        df["_hi"] = (pos >= 2.0 / 3.0).astype(np.float32)
        df["_lo"] = (pos <= 1.0 / 3.0).astype(np.float32)
        df["_dhi"] = df["net_delta_coin"] * df["_hi"]
        df["_dlo"] = df["net_delta_coin"] * df["_lo"]
        df["_vhi"] = df["total_vol_coin"] * df["_hi"]
        df["_vlo"] = df["total_vol_coin"] * df["_lo"]
        df["_bhi"] = df["is_buy_imbalance"].astype(np.float32) * df["_hi"]
        df["_nhi"] = df["_hi"]
    g = df.groupby("open_time_ms", sort=True)
    base = dict(
        ld_delta=("net_delta_coin", "sum"),
        ld_tv=("total_vol_coin", "sum"),
        ld_buy_imb=("is_buy_imbalance", "sum"),
        ld_sell_imb=("is_sell_imbalance", "sum"),
        ld_stack_buy=("is_stacked_buy_imb", "sum"),
        ld_stack_sell=("is_stacked_sell_imb", "sum"),
        ld_bins=("price_bin", "size"),
        ld_val=("price_bin", "min"),
        ld_vah=("price_bin", "max"),
    )
    if rng is not None:
        base.update(
            ld_delta_hi=("_dhi", "sum"), ld_delta_lo=("_dlo", "sum"),
            ld_vol_hi=("_vhi", "sum"), ld_vol_lo=("_vlo", "sum"),
            ld_buyimb_hi=("_bhi", "sum"), ld_bins_hi=("_nhi", "sum"),
        )
    agg = g.agg(**base)
    poc = df.loc[df.is_poc.to_numpy() == 1].groupby("open_time_ms")["price_bin"].min()
    agg["ld_poc"] = poc.reindex(agg.index).astype("float32")
    return agg


def load_ladder_raw(symbol: str, rng: pd.DataFrame | None = None,
                    batch_size: int = 1_500_000) -> pd.DataFrame:
    """Per-candle ladder aggregates, re-reduced across batches."""
    pf = pq.ParquetFile(ladder_path(symbol))
    parts = []
    for batch in pf.iter_batches(batch_size=batch_size, columns=LADDER_COLUMNS):
        parts.append(_reduce_batch(batch.to_pandas(), rng=rng))
    r = pd.concat(parts)
    if len(parts) > 1:
        g = r.groupby(level=0, sort=True)
        r = g.agg(
            ld_delta=("ld_delta", "sum"), ld_tv=("ld_tv", "sum"),
            ld_buy_imb=("ld_buy_imb", "sum"), ld_sell_imb=("ld_sell_imb", "sum"),
            ld_stack_buy=("ld_stack_buy", "sum"), ld_stack_sell=("ld_stack_sell", "sum"),
            ld_bins=("ld_bins", "sum"), ld_val=("ld_val", "min"), ld_vah=("ld_vah", "max"),
            ld_poc=("ld_poc", "min"),
            **({"ld_delta_hi": ("ld_delta_hi", "sum"), "ld_delta_lo": ("ld_delta_lo", "sum"),
                "ld_vol_hi": ("ld_vol_hi", "sum"), "ld_vol_lo": ("ld_vol_lo", "sum"),
                "ld_buyimb_hi": ("ld_buyimb_hi", "sum"), "ld_bins_hi": ("ld_bins_hi", "sum")}
               if rng is not None else {}),
        )
    r = r.reset_index()
    r["ld_bins"] = r["ld_bins"].astype("float32")
    return r


def _derive(r: pd.DataFrame, f: pd.DataFrame) -> pd.DataFrame:
    """Turn raw per-candle ladder aggregates into model features (with ATR/vol scaling)."""
    out = r.copy()
    tv = out.ld_tv.replace(0, np.nan)
    delta = out.ld_delta
    out["ld_delta_rel"] = (delta / tv).fillna(0.0).clip(-1.0, 1.0)

    d8 = delta.rolling(8, min_periods=4).sum()
    v8 = tv.rolling(8, min_periods=4).sum()
    out["ld_cvd_8"] = (d8 / v8).fillna(0.0).clip(-1.0, 1.0)
    out["ld_cvd_4"] = (delta.rolling(4, min_periods=2).sum()
                       / tv.rolling(4, min_periods=2).sum()).fillna(0.0).clip(-1.0, 1.0)
    out["ld_cvd_32"] = (delta.rolling(32, min_periods=8).sum()
                        / tv.rolling(32, min_periods=8).sum()).fillna(0.0).clip(-1.0, 1.0)

    prior = out.ld_delta_rel.shift(1).rolling(1920, min_periods=480)
    out["ld_delta_z"] = ((out.ld_delta_rel - prior.mean())
                         / prior.std(ddof=0).replace(0, np.nan)).fillna(0.0).clip(-6, 6)

    bins = out.ld_bins.replace(0, np.nan)
    out["ld_imb_net"] = ((out.ld_buy_imb - out.ld_sell_imb) / bins).fillna(0.0)
    out["ld_stack_net"] = ((out.ld_stack_buy - out.ld_stack_sell) / bins).fillna(0.0)
    out["ld_imb_net_8"] = out.ld_imb_net.rolling(8, min_periods=4).mean().fillna(0.0)

    # Within-candle structure: aggression at the highs vs the lows.
    if "ld_delta_hi" in out.columns:
        out["ld_delta_hi_rel"] = (out.ld_delta_hi / out.ld_vol_hi.replace(0, np.nan)
                                  ).fillna(0.0).clip(-1.0, 1.0)
        out["ld_delta_lo_rel"] = (out.ld_delta_lo / out.ld_vol_lo.replace(0, np.nan)
                                  ).fillna(0.0).clip(-1.0, 1.0)
        out["ld_delta_skew"] = (out.ld_delta_hi_rel - out.ld_delta_lo_rel).clip(-2.0, 2.0)
        out["ld_buyimb_hi_frac"] = (out.ld_buyimb_hi / out.ld_bins_hi.replace(0, np.nan)
                                    ).fillna(0.0).clip(0.0, 1.0)
        span = (out.ld_vah - out.ld_val).replace(0, np.nan)
        out["ld_poc_range_pos"] = ((out.ld_poc - out.ld_val) / span).fillna(0.5).clip(0.0, 1.0)
    else:
        for c in ("ld_delta_hi_rel", "ld_delta_lo_rel", "ld_delta_skew",
                  "ld_poc_range_pos", "ld_buyimb_hi_frac"):
            out[c] = 0.0

    out["ld_bins_rel"] = (out.ld_bins / out.ld_bins.shift(1).rolling(192, min_periods=48)
                          .mean().replace(0, np.nan)).fillna(1.0).clip(0.0, 10.0)
    out["ld_rel_vol"] = (out.ld_tv / out.ld_tv.shift(1).rolling(96, min_periods=48)
                         .mean().replace(0, np.nan)).fillna(1.0).clip(0.0, 50.0)

    # Position of the close inside the *true* footprint value area (ATR units).
    a = f["atr"].to_numpy(np.float64)
    r_ = out.set_index("open_time_ms")
    fidx = pd.Index(f["open_time_ms"].to_numpy())
    close = pd.Series(f["close"].to_numpy(np.float64), index=fidx)
    atr = pd.Series(np.where(a > 0, a, np.nan), index=fidx)
    for src, dst, op in (("ld_poc", "ld_d_poc", "sub"), ("ld_vah", "ld_d_vah", "sub"),
                         ("ld_val", "ld_d_val", "sub")):
        s = pd.Series(r_[src].to_numpy(np.float64), index=pd.Index(r_.index.to_numpy()))
        d = pd.Series(np.nan, index=fidx)
        common = d.index.intersection(s.dropna().index)
        d.loc[common] = (close.loc[common] - s.loc[common]) / atr.loc[common]
        out[dst] = d.reindex(pd.Index(r_.index)).to_numpy()
    width = (r_.ld_vah - r_.ld_val) / atr.reindex(pd.Index(r_.index)).to_numpy()
    out["ld_va_width"] = np.asarray(width, dtype=float)
    mid = (r_.ld_vah + r_.ld_val) / 2.0
    rng = (r_.ld_vah - r_.ld_val).replace(0, np.nan)
    pos = (close.reindex(pd.Index(r_.index)).to_numpy() - mid.to_numpy()) / rng.to_numpy()
    out["ld_va_pos"] = np.clip(np.nan_to_num(pos), -3, 3)

    for c in FLOW_COLUMNS:
        out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0.0).astype("float32")
    return out[["open_time_ms"] + FLOW_COLUMNS]


def build_flow_features(symbol: str) -> pd.DataFrame:
    """Per-candle flow features for one symbol (raw ladder reduce + derive)."""
    from .data import build_symbol_features

    # We only need atr/close/high/low for scaling; the derived cache makes this cheap.
    mpath = CACHE_DIR / f"{symbol}_bw0.00050.parquet"
    cols = ["open_time_ms", "close", "atr", "high", "low"]
    if mpath.exists():
        f = pd.read_parquet(mpath, columns=cols)
    else:
        f = build_symbol_features(symbol)[cols]
    rng = f[["open_time_ms", "low", "high"]].rename(
        columns={"low": "rng_lo", "high": "rng_hi"}).set_index("open_time_ms")
    raw = load_ladder_raw(symbol, rng=rng.dropna())
    return _derive(raw, f)


def flow_path(symbol: str) -> Path:
    return CACHE_DIR / f"{symbol}_flow.parquet"


def load_flow(symbol: str, cache: bool = True, rebuild: bool = False) -> pd.DataFrame:
    p = flow_path(symbol)
    if cache and p.exists() and not rebuild:
        return pd.read_parquet(p)
    f = build_flow_features(symbol)
    if cache:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        f.to_parquet(p, index=False)
    return f


def main():
    from .data import ALL_SYMBOLS

    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALL_SYMBOLS))
    ap.add_argument("--rebuild", action="store_true")
    a = ap.parse_args()
    for s in [x.strip() for x in a.symbols.split(",") if x.strip()]:
        try:
            f = load_flow(s, rebuild=a.rebuild)
            print(f"{s}: {len(f):,} bars | " + " ".join(
                f"{c}={f[c].mean():+.3f}" for c in ("ld_delta_rel", "ld_imb_net", "ld_d_poc")))
        except Exception as exc:  # noqa: BLE001
            print(f"{s}: FAILED {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
