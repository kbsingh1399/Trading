# Engine/ml/footprint_features.py
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Optional


class FootprintLadderFeatures:
    """
    Consumes {symbol}_15m_footprint_ladder.parquet with columns:
        open_time_ms, price_bin, bid_vol_coin, ask_vol_coin,
        net_delta_coin, total_vol_coin, trade_count, is_poc,
        is_buy_imbalance, is_sell_imbalance, is_stacked_buy_imb,
        is_stacked_sell_imb, is_value_area

    All features are unit-free (ratios, z-scores, ranks) -> poolable across
    BTC and altcoin price scales. Fully vectorized for high-speed computation.
    """

    def __init__(self, z_window: int = 96, flush_window: int = 12):
        self.zw = z_window
        self.fw = flush_window

    def load_and_aggregate(self, path: str) -> pd.DataFrame:
        """
        Fast vectorized aggregation of price-bin ladder rows into per-15m-bar metrics.
        Returns one row per 15m bar with ladder-derived order flow aggregates.
        """
        lad = pd.read_parquet(path)
        lad.sort_values(["open_time_ms", "price_bin"], inplace=True)

        # 1. Base aggregations per 15m candle
        g = lad.groupby("open_time_ms", sort=True)
        agg = pd.DataFrame({
            "bid_vol": g["bid_vol_coin"].sum(),
            "ask_vol": g["ask_vol_coin"].sum(),
            "net_delta": g["net_delta_coin"].sum(),
            "total_vol": g["total_vol_coin"].sum(),
            "trade_cnt": g["trade_count"].sum(),
            "n_bins": g["price_bin"].count(),
            "price_bin_lo": g["price_bin"].min(),
            "price_bin_hi": g["price_bin"].max(),
            "n_buy_imb": g["is_buy_imbalance"].sum(),
            "n_sell_imb": g["is_sell_imbalance"].sum(),
            "has_stacked_buy": g["is_stacked_buy_imb"].max(),
            "has_stacked_sell": g["is_stacked_sell_imb"].max(),
            "va_bins": g["is_value_area"].sum(),
        })

        # 2. Fast vectorized POC bin and POC vol lookup
        poc_rows = lad[lad["is_poc"] == 1].drop_duplicates("open_time_ms").set_index("open_time_ms")
        agg["poc_bin"] = poc_rows["price_bin"].reindex(agg.index).fillna(agg["price_bin_lo"])
        agg["poc_vol"] = poc_rows["total_vol_coin"].reindex(agg.index).fillna(0.0)

        # 3. Low/High bin volume (first 3 and last 3 price bins)
        # Using head(3) and tail(3) per group in a vectorized way
        lo_3 = lad.groupby("open_time_ms").head(3).groupby("open_time_ms")["total_vol_coin"].sum()
        hi_3 = lad.groupby("open_time_ms").tail(3).groupby("open_time_ms")["total_vol_coin"].sum()
        agg["vol_at_lo_bins"] = lo_3.reindex(agg.index).fillna(0.0)
        agg["vol_at_hi_bins"] = hi_3.reindex(agg.index).fillna(0.0)

        agg.index = pd.to_datetime(agg.index, unit="ms", utc=True)
        if agg.index.tz is not None:
            agg.index = agg.index.tz_convert(None)
        return agg

    def build_features(self, agg: pd.DataFrame, ohlc: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Merge ladder aggregates with 15m OHLC and emit stationary absorption features.
        """
        F = pd.DataFrame(index=agg.index)
        tot = agg["total_vol"].clip(lower=1e-12)
        net_delta = agg["net_delta"]

        # 1) Normalized footprint delta [-1, 1]
        F["fp_delta_ratio"] = (net_delta / tot).clip(-1, 1).fillna(0.0)

        # 2) Wick absorption (selling absorbed at the low)
        low_share = (agg["vol_at_lo_bins"] / tot).clip(0, 1)
        hi_share = (agg["vol_at_hi_bins"] / tot).clip(0, 1)
        F["wick_sell_absorb"] = (low_share * (0.5 + 0.5 * F["fp_delta_ratio"])).fillna(0.0)
        F["wick_buy_exhaust"] = (hi_share * (0.5 - 0.5 * F["fp_delta_ratio"])).fillna(0.0)

        # 3) Stacked imbalance flags
        F["has_stacked_buy"] = agg["has_stacked_buy"].astype(np.float64).fillna(0.0)
        F["has_stacked_sell"] = agg["has_stacked_sell"].astype(np.float64).fillna(0.0)
        F["imb_ratio"] = ((agg["n_buy_imb"] - agg["n_sell_imb"]) / (agg["n_buy_imb"] + agg["n_sell_imb"]).clip(lower=1)).clip(-1, 1).fillna(0.0)

        # 4) Sell impact collapse
        if ohlc is not None:
            o = ohlc["open"].reindex(agg.index).astype(np.float64)
            h = ohlc["high"].reindex(agg.index).astype(np.float64)
            l = ohlc["low"].reindex(agg.index).astype(np.float64)
            c = ohlc["close"].reindex(agg.index).astype(np.float64)
            rng = (h - l).clip(lower=1e-12)
            atr = rng.rolling(96, min_periods=1).mean().clip(lower=1e-12)
            ret = (c - o) / atr
        else:
            ret = agg["poc_bin"].diff() / agg["poc_bin"].rolling(96, min_periods=1).mean().clip(lower=1e-12)

        sell_vol = agg["bid_vol"].clip(lower=1e-12)
        sell_frac = (sell_vol / tot).clip(0, 1)
        impact = ret / sell_frac.clip(lower=0.05)
        F["sell_impact"] = impact.clip(-10, 10).fillna(0.0)

        s3 = sell_vol.rolling(3, min_periods=1).sum().clip(lower=1e-12)
        p3 = ret.rolling(3, min_periods=1).sum().clip(-10, 10)
        F["absorption_ratio"] = (p3 * tot.rolling(3, min_periods=1).sum() / s3).clip(-10, 10).fillna(0.0)

        # 5) Delta divergence at the low
        if ohlc is not None:
            new_low = (l <= l.rolling(3, min_periods=1).min()).astype(np.float64)
        else:
            new_low = (agg["poc_bin"] <= agg["poc_bin"].rolling(3, min_periods=1).min()).astype(np.float64)
        F["delta_div_at_low"] = (new_low * (F["fp_delta_ratio"] - F["fp_delta_ratio"].rolling(3, min_periods=1).mean())).clip(-1, 1).fillna(0.0)

        # 6) Point of Control (POC) shift relative to ladder bins
        F["poc_shift"] = (agg["poc_bin"].diff() / agg["n_bins"].clip(lower=1)).clip(-2, 2).fillna(0.0)

        # 7) Average trade size imbalance
        avg_trade_size = (tot / agg["trade_cnt"].clip(lower=1))
        m_ats = avg_trade_size.rolling(96, min_periods=1).mean().clip(lower=1e-12)
        F["avg_trade_size_zs"] = ((avg_trade_size - m_ats) / avg_trade_size.rolling(96, min_periods=1).std(ddof=0).clip(lower=1e-12).fillna(1.0)).clip(-5, 5).fillna(0.0)

        # 8) Ladder range compression
        ladder_rng = (agg["price_bin_hi"] - agg["price_bin_lo"]).clip(lower=1)
        rng_ma = ladder_rng.rolling(96, min_periods=1).mean().clip(lower=1e-12)
        F["ladder_compression"] = (ladder_rng / rng_ma).clip(0, 10).fillna(1.0)

        # 9) Post-event reclaim geometry
        if ohlc is not None:
            F["reclaim_mid"] = ((c - (h.shift(1) + l.shift(1)) / 2.0) / atr).clip(-5, 5).fillna(0.0)
            F["higher_low_bars"] = ((l > l.shift(1)).astype(np.float64).rolling(3, min_periods=1).sum() / 3.0).fillna(0.0)

        return F.fillna(0.0)
