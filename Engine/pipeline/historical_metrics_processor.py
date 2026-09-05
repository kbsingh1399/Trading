"""
================================================================================
HISTORICAL METRICS & CANONICAL FEATURE PROCESSOR (TABLE 1)
================================================================================
Turns the raw streams (futures klines, spot klines, official metrics, funding,
optional tick footprint) into the canonical master frame.

Causality contract
------------------
* Bar t may use any raw observation whose timestamp is <= close_time_ms[t].
  Event streams (funding, OI, L/S ratios, taker ratio) are as-of joined on
  ``close_time_ms`` with ``direction="backward"`` and ``allow_exact_matches=True``.
* Spot klines are joined strictly 1:1 on ``open_time_ms``; a missing spot bar
  yields zero spot delta (never a stale copy) and a forward-filled basis.
* Gaps in the futures timeline (exchange downtime) are reconstructed with a
  flat bar at the last close, zero volume, ``is_synthetic = 1``.
* Every rolling / recursive feature uses only bars <= t (see
  core.canonical_indicators). No ``bfill``, no centred windows, no full-sample
  statistics anywhere in this module.
================================================================================
"""

from __future__ import annotations

from typing import Callable, Optional

import numpy as np
import pandas as pd

from ..core.canonical_indicators import (
    compute_ema_series,
    compute_rolling_zscore,
    compute_session_cvd,
    compute_session_value_area,
    compute_session_vwap,
    compute_sma_series,
    compute_vwap_zscore,
    compute_wilder_atr_series,
    compute_wilder_rsi_series,
    estimate_depth_from_volatility,
    get_merge_level,
)
from ..core.mathematical_liquidation_engine import MathematicalLiquidationModel
from ..core.schema import (
    BAR_MS,
    CANONICAL_COLUMNS,
    COIN_DP,
    COLUMN_DTYPES,
    PCT_DP,
    PRICE_DP,
    RATIO_DP,
    USD_DP,
)

LIQ_Z_WINDOW = 96
VWAP_Z_WINDOW = 24
METRICS_MAX_STALENESS_MS = 6 * 3_600_000
FUNDING_MAX_STALENESS_MS = 16 * 3_600_000   # two missed 8h settlements


def build_continuous_timeline(klines: pd.DataFrame) -> pd.DataFrame:
    """
    Re-indexes raw klines onto an unbroken 15m grid. Missing bars become flat
    zero-volume bars at the previous close (causal ffill) tagged is_synthetic=1.
    """
    df = klines.drop_duplicates("open_time", keep="last").sort_values("open_time").reset_index(drop=True)
    if df.empty:
        raise ValueError("empty kline frame")
    df["open_time"] = df["open_time"].astype(np.int64)
    grid = np.arange(int(df["open_time"].iloc[0]), int(df["open_time"].iloc[-1]) + BAR_MS, BAR_MS, dtype=np.int64)
    df = df.set_index("open_time").reindex(grid)
    df.index.name = "open_time"
    synthetic = df["close"].isna().to_numpy()
    df["close"] = df["close"].ffill()
    for c in ("open", "high", "low"):
        df[c] = df[c].fillna(df["close"])
    for c in ("volume", "quote_volume", "taker_buy_volume", "taker_buy_quote_volume"):
        df[c] = df[c].fillna(0.0)
    df["count"] = df["count"].fillna(0).astype(np.int64)
    df["close_time"] = df.index.to_numpy() + (BAR_MS - 1)
    df = df.reset_index()
    degenerate = ((df["high"] == df["low"]) & ((df["volume"] <= 0.0) | (df["count"] <= 0))).to_numpy()
    df["is_synthetic"] = (synthetic | degenerate).astype(np.int8)
    return df


def _asof_backward(left_ts: np.ndarray, right: pd.DataFrame, ts_col: str, cols) -> pd.DataFrame:
    """Last observation with right[ts_col] <= left_ts (causal); NaN when none."""
    left = pd.DataFrame({"_ts": left_ts.astype(np.int64)})
    r = right[[ts_col] + list(cols)].dropna(subset=[ts_col]).copy()
    r[ts_col] = r[ts_col].astype(np.int64)
    r = r.drop_duplicates(ts_col, keep="last").sort_values(ts_col)
    merged = pd.merge_asof(left, r, left_on="_ts", right_on=ts_col, direction="backward", allow_exact_matches=True)
    merged["_age_ms"] = merged["_ts"] - merged[ts_col]
    return merged


class HistoricalMetricsProcessor:
    def __init__(self, log: Callable[[str], None] = print) -> None:
        self.log = log
        self.liq_model = MathematicalLiquidationModel()

    def process_master_dataset(
        self,
        klines_df: pd.DataFrame,
        metrics_df: Optional[pd.DataFrame],
        funding_df: Optional[pd.DataFrame],
        footprint_df: Optional[pd.DataFrame] = None,
        spot_df: Optional[pd.DataFrame] = None,
        symbol: str = "BTCUSDT",
        export_start_ms: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        ``export_start_ms``: first bar to keep. Indicators are computed on the
        full (warm-up) history first; the slice is applied afterwards and the
        lifetime CVD accumulators are re-anchored so lifetime[0] == delta[0].
        """
        log = self.log
        log(f"[PROCESSOR] {symbol}: building continuous timeline")
        df = build_continuous_timeline(klines_df)
        n = len(df)
        synth_n = int(df["is_synthetic"].sum())
        if synth_n:
            log(f"[PROCESSOR] {symbol}: {synth_n} synthetic/downtime bars tagged")

        out = pd.DataFrame(index=df.index)
        out["open_time_ms"] = df["open_time"].to_numpy(np.int64)
        out["close_time_ms"] = df["close_time"].to_numpy(np.int64)
        out["datetime_utc"] = pd.to_datetime(out["open_time_ms"], unit="ms", utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
        out["symbol"] = symbol

        o = df["open"].to_numpy(np.float64)
        h = df["high"].to_numpy(np.float64)
        l = df["low"].to_numpy(np.float64)
        c = df["close"].to_numpy(np.float64)
        vb = df["volume"].to_numpy(np.float64)
        vq = df["quote_volume"].to_numpy(np.float64)
        tc = df["count"].to_numpy(np.int64)
        ot = out["open_time_ms"].to_numpy()
        ct = out["close_time_ms"].to_numpy()

        out["open"], out["high"], out["low"], out["close"] = o, h, l, c
        out["volume_base"] = vb
        out["volume_quote"] = vq
        out["volume_sma9"] = compute_sma_series(vq, 9)
        out["trade_count"] = tc

        log(f"[PROCESSOR] {symbol}: momentum, volatility, EMAs")
        out["rsi_14"] = compute_wilder_rsi_series(c, 14)
        out["atr_14"] = compute_wilder_atr_series(h, l, c, 14)
        out["atr_100"] = compute_wilder_atr_series(h, l, c, 100)
        for p in (8, 21, 50, 200, 800):
            out[f"ema_{p}"] = compute_ema_series(c, p)

        # ---------------------------------------------------------------- flow
        log(f"[PROCESSOR] {symbol}: order flow & CVD")
        kl_buy = df["taker_buy_volume"].to_numpy(np.float64)
        kl_sell = np.maximum(vb - kl_buy, 0.0)
        buy_share = np.divide(kl_buy, vb, out=np.full(n, 0.5), where=vb > 0)
        kl_buy_cnt = np.round(tc * buy_share).astype(np.int64)
        kl_sell_cnt = tc - kl_buy_cnt

        fp = footprint_df if footprint_df is not None and not footprint_df.empty else None
        if fp is not None:
            fpm = pd.DataFrame({"open_time_ms": ot}).merge(fp.drop_duplicates("open_time_ms"), on="open_time_ms", how="left")
            exact = fpm["taker_buy_vol_coin"].notna().to_numpy()
            buy = np.where(exact, fpm["taker_buy_vol_coin"].to_numpy(np.float64), kl_buy)
            sell = np.where(exact, fpm["taker_sell_vol_coin"].to_numpy(np.float64), kl_sell)
            buy_cnt = np.where(exact, fpm["taker_buy_count"].fillna(0).to_numpy(np.int64), kl_buy_cnt)
            sell_cnt = np.where(exact, fpm["taker_sell_count"].fillna(0).to_numpy(np.int64), kl_sell_cnt)
            max_trade = np.where(exact, fpm["max_single_trade_vol"].fillna(0.0).to_numpy(np.float64), vb * 0.05)
            real_poc = fpm["real_poc"].to_numpy(np.float64) if "real_poc" in fpm else np.full(n, np.nan)
            poc_ratio = fpm["poc_vol_ratio"].fillna(0.0).to_numpy(np.float64) if "poc_vol_ratio" in fpm else np.zeros(n)
            st_buy = fpm["stacked_buy_imbalances"].fillna(0.0).to_numpy(np.float64) if "stacked_buy_imbalances" in fpm else np.zeros(n)
            st_sell = fpm["stacked_sell_imbalances"].fillna(0.0).to_numpy(np.float64) if "stacked_sell_imbalances" in fpm else np.zeros(n)
            log(f"[PROCESSOR] {symbol}: {int(exact.sum()):,} bars with tick-exact footprint")
        else:
            exact = np.zeros(n, dtype=bool)
            buy, sell, buy_cnt, sell_cnt = kl_buy, kl_sell, kl_buy_cnt, kl_sell_cnt
            max_trade = vb * 0.05
            real_poc = np.full(n, np.nan)
            poc_ratio = np.zeros(n)
            st_buy = np.zeros(n)
            st_sell = np.zeros(n)

        fut_delta = buy - sell
        out["future_cvd_15m"] = fut_delta
        out["future_cvd_session"] = compute_session_cvd(ot, fut_delta)
        out["future_cvd_lifetime"] = np.cumsum(fut_delta)

        # ---------------------------------------------------------------- spot (strict 1:1)
        spot_close = np.full(n, np.nan)
        spot_delta = np.zeros(n)
        spot_exact = np.zeros(n, dtype=bool)
        if spot_df is not None and not spot_df.empty:
            s = spot_df.drop_duplicates("open_time", keep="last")
            sm = pd.DataFrame({"open_time_ms": ot}).merge(
                s.rename(columns={"open_time": "open_time_ms"}), on="open_time_ms", how="left")
            spot_exact = sm["spot_close"].notna().to_numpy()
            spot_close = sm["spot_close"].to_numpy(np.float64)
            s_vol = sm["spot_volume"].fillna(0.0).to_numpy(np.float64)
            s_buy = sm["spot_taker_buy_volume"].fillna(0.0).to_numpy(np.float64)
            spot_delta = np.where(spot_exact, s_buy - np.maximum(s_vol - s_buy, 0.0), 0.0)
            log(f"[PROCESSOR] {symbol}: spot matched on {int(spot_exact.sum()):,}/{n:,} bars")
        else:
            log(f"[WARN] {symbol}: no spot stream; spot CVD = 0, basis = 0")
        out["spot_cvd_15m"] = spot_delta
        out["spot_cvd_session"] = compute_session_cvd(ot, spot_delta)
        out["spot_cvd_lifetime"] = np.cumsum(spot_delta)
        spot_close_ff = pd.Series(spot_close).ffill().to_numpy()
        basis = np.where(np.isnan(spot_close_ff), 0.0, c - spot_close_ff)
        out["basis_usd"] = basis
        out["spot_close"] = np.where(np.isnan(spot_close_ff), c, spot_close_ff)
        out["spot_flow_source"] = np.where(spot_exact, "SPOT_EXACT", "UNAVAILABLE")

        # ---------------------------------------------------------------- funding (as-of close)
        log(f"[PROCESSOR] {symbol}: funding")
        if funding_df is not None and not funding_df.empty:
            fm = _asof_backward(ct, funding_df, "fundingTime", ["fundingRate"])
            fr = fm["fundingRate"].to_numpy(np.float64)
            fr = np.where(np.isnan(fr), 0.0001, fr)
            out["funding_rate_pct"] = fr * 100.0
        else:
            out["funding_rate_pct"] = 0.01

        # ---------------------------------------------------------------- official metrics (as-of close)
        log(f"[PROCESSOR] {symbol}: open interest & positioning")
        fallback_taker = np.divide(buy, np.maximum(sell, 1e-9))
        if metrics_df is not None and not metrics_df.empty:
            cols = ["sum_open_interest", "sum_open_interest_value", "count_long_short_ratio",
                    "sum_toptrader_long_short_ratio", "count_toptrader_long_short_ratio", "sum_taker_long_short_vol_ratio"]
            m = metrics_df.copy()
            for col in cols:
                if col not in m.columns:
                    m[col] = np.nan
            # each metric column independently: last non-null value at or before close
            merged = {}
            for col in cols:
                sub = m[["timestamp_ms", col]].dropna()
                if sub.empty:
                    merged[col] = np.full(n, np.nan)
                    merged[col + "_age"] = np.full(n, np.inf)
                    continue
                mm = _asof_backward(ct, sub, "timestamp_ms", [col])
                merged[col] = mm[col].to_numpy(np.float64)
                merged[col + "_age"] = mm["_age_ms"].to_numpy(np.float64)
            oi_coin = merged["sum_open_interest"]
            oi_age = merged["sum_open_interest_age"]
            available = (~np.isnan(oi_coin)) & (oi_age <= METRICS_MAX_STALENESS_MS)
            oi_coin = np.where(np.isnan(oi_coin), 0.0, oi_coin)
            oi_usd = merged["sum_open_interest_value"]
            oi_usd = np.where(np.isnan(oi_usd), oi_coin * c, oi_usd)
            ls_glob = np.where(np.isnan(merged["count_long_short_ratio"]), 1.0, merged["count_long_short_ratio"])
            ls_top = np.where(np.isnan(merged["sum_toptrader_long_short_ratio"]), 1.0, merged["sum_toptrader_long_short_ratio"])
            top_acc = merged["count_toptrader_long_short_ratio"]
            top_acc = np.where(np.isnan(top_acc), ls_glob, top_acc)
            taker_ratio = merged["sum_taker_long_short_vol_ratio"]
            taker_ratio = np.where(np.isnan(taker_ratio), fallback_taker, taker_ratio)
            out["metrics_available"] = available.astype(np.int8)
        else:
            log(f"[WARN] {symbol}: no official metrics stream")
            oi_coin = np.zeros(n)
            oi_usd = np.zeros(n)
            ls_glob = np.ones(n)
            ls_top = np.ones(n)
            top_acc = np.ones(n)
            taker_ratio = fallback_taker
            out["metrics_available"] = np.zeros(n, dtype=np.int8)

        out["open_interest_k"] = oi_coin / 1000.0
        out["open_interest_usd"] = oi_usd
        prev_oi = np.empty(n)
        prev_oi[0] = oi_coin[0] if n else 0.0
        prev_oi[1:] = oi_coin[:-1]
        oi_chg = np.divide(oi_coin - prev_oi, prev_oi, out=np.zeros(n), where=prev_oi > 0) * 100.0
        out["oi_change_pct"] = np.clip(oi_chg, -100.0, 100.0)
        out["ls_ratio_global"] = ls_glob
        out["ls_ratio_top"] = ls_top
        out["top_account_ratio"] = top_acc
        top_long_p = ls_top / (1.0 + ls_top)
        glob_long_p = ls_glob / (1.0 + ls_glob)
        out["whale_index"] = top_long_p / np.maximum(glob_long_p, 1e-4) * 100.0
        out["taker_volume_ratio"] = np.clip(taker_ratio, 0.0, 1e6)

        # ---------------------------------------------------------------- footprint / value area
        log(f"[PROCESSOR] {symbol}: footprint & session value area")
        out["fp_delta"] = fut_delta
        ohlc_poc = (h + l + 2.0 * c) / 4.0
        out["fp_poc"] = np.where(np.isnan(real_poc), ohlc_poc, real_poc)
        out["poc_source"] = np.where(np.isnan(real_poc), "OHLC_APPROX", "TICK_EXACT")
        out["fp_poc_vol_ratio"] = poc_ratio
        out["fp_stacked_buy_imb"] = st_buy
        out["fp_stacked_sell_imb"] = st_sell
        svah, sval, pvah, pval = compute_session_value_area(ot, h, l, c, vb, bucket_size=get_merge_level(symbol))
        out["session_vah"], out["session_val"] = svah, sval
        out["prev_day_vah"], out["prev_day_val"] = pvah, pval
        out["taker_buy_count"] = buy_cnt.astype(np.int64)
        out["taker_sell_count"] = sell_cnt.astype(np.int64)
        out["taker_buy_vol_btc"] = buy
        out["taker_sell_vol_btc"] = sell
        out["max_trade_vol_btc"] = max_trade
        out["avg_trade_size_usd"] = np.divide(vq, np.maximum(tc, 1))
        out["future_flow_source"] = np.where(exact, "TICK_EXACT", "KLINE_APPROX")

        b_usd, a_usd, b_coin, a_coin = estimate_depth_from_volatility(c, out["atr_14"].to_numpy(), vb)
        out["bid_depth_usd"], out["ask_depth_usd"] = b_usd, a_usd
        out["bid_depth_coin"], out["ask_depth_coin"] = b_coin, a_coin
        out["is_synthetic"] = df["is_synthetic"].to_numpy(np.int8)

        # ---------------------------------------------------------------- liquidations
        log(f"[PROCESSOR] {symbol}: liquidation cascade engine")
        liq_in = pd.DataFrame({
            "open": o, "high": h, "low": l, "close": c, "volume_quote": vq, "volume_base": vb,
            "trade_count": tc, "taker_buy_quote_volume": df["taker_buy_quote_volume"].to_numpy(np.float64),
            "future_cvd_15m": fut_delta, "open_interest_k": out["open_interest_k"].to_numpy(),
            "ls_ratio_global": ls_glob, "funding_rate_pct": out["funding_rate_pct"].to_numpy(),
        })
        long_liq, short_liq = self.liq_model.compute_vectorized(liq_in)
        long_liq = -np.abs(np.nan_to_num(long_liq, nan=0.0, posinf=0.0, neginf=0.0))
        short_liq = np.abs(np.nan_to_num(short_liq, nan=0.0, posinf=0.0, neginf=0.0))
        out["long_liq_usd"], out["short_liq_usd"] = long_liq, short_liq

        # ---------------------------------------------------------------- extended features
        log(f"[PROCESSOR] {symbol}: VWAP, z-scores, divergence")
        vwap = compute_session_vwap(ot, h, l, c, vb)
        out["session_vwap"] = vwap
        out["vwap_zscore"] = compute_vwap_zscore(c, vwap, VWAP_Z_WINDOW)
        sma9_base = compute_sma_series(vb, 9)
        out["volume_ratio"] = np.divide(vb, sma9_base, out=np.zeros(n), where=sma9_base > 0)
        out["zc_div"] = spot_delta - fut_delta
        out["long_liq_zs"] = compute_rolling_zscore(np.abs(long_liq), LIQ_Z_WINDOW)
        out["short_liq_zs"] = compute_rolling_zscore(short_liq, LIQ_Z_WINDOW)
        tot = short_liq + np.abs(long_liq)
        out["liq_imbalance_ratio"] = np.divide(short_liq - np.abs(long_liq), tot, out=np.zeros(n), where=tot > 0)

        if export_start_ms is not None:
            keep = out["open_time_ms"].to_numpy() >= int(export_start_ms)
            if not keep.any():
                raise ValueError(f"{symbol}: no bars at/after {pd.to_datetime(export_start_ms, unit='ms', utc=True)}")
            first = int(np.flatnonzero(keep)[0])
            out = out.iloc[first:].reset_index(drop=True)
            if first > 0:
                for life, delta in (("future_cvd_lifetime", "future_cvd_15m"), ("spot_cvd_lifetime", "spot_cvd_15m")):
                    out[life] = out[life].to_numpy() - (out[life].iloc[0] - out[delta].iloc[0])
                log(f"[PROCESSOR] {symbol}: dropped {first:,} warm-up bars; lifetime CVD re-anchored")

        final = self._finalise(out[CANONICAL_COLUMNS].copy())
        log(f"[PROCESSOR] {symbol}: {len(final):,} rows x {len(final.columns)} cols")
        return final

    # ------------------------------------------------------------------ finalise
    @staticmethod
    def _finalise(df: pd.DataFrame) -> pd.DataFrame:
        price_cols = ("open", "high", "low", "close", "atr_14", "atr_100", "ema_8", "ema_21", "ema_50", "ema_200",
                      "ema_800", "basis_usd", "fp_poc", "session_vah", "session_val", "prev_day_vah", "prev_day_val",
                      "spot_close", "session_vwap")
        coin_cols = ("volume_base", "future_cvd_15m", "future_cvd_session", "future_cvd_lifetime", "spot_cvd_15m",
                     "spot_cvd_session", "spot_cvd_lifetime", "open_interest_k", "fp_delta", "taker_buy_vol_btc",
                     "taker_sell_vol_btc", "max_trade_vol_btc", "bid_depth_coin", "ask_depth_coin", "zc_div")
        usd_cols = ("volume_quote", "volume_sma9", "open_interest_usd", "long_liq_usd", "short_liq_usd",
                    "avg_trade_size_usd", "bid_depth_usd", "ask_depth_usd")
        ratio_cols = ("rsi_14", "ls_ratio_global", "ls_ratio_top", "top_account_ratio", "whale_index",
                      "taker_volume_ratio", "fp_poc_vol_ratio", "vwap_zscore", "volume_ratio", "long_liq_zs",
                      "short_liq_zs", "liq_imbalance_ratio")
        pct_cols = ("funding_rate_pct", "oi_change_pct")
        for cols, dp in ((price_cols, PRICE_DP), (coin_cols, COIN_DP), (usd_cols, USD_DP), (ratio_cols, RATIO_DP), (pct_cols, PCT_DP)):
            for col in cols:
                df[col] = np.round(df[col].to_numpy(np.float64), dp)
        for col in ("fp_stacked_buy_imb", "fp_stacked_sell_imb"):
            df[col] = df[col].astype(np.float64)
        num_cols = [c for c in df.columns if COLUMN_DTYPES[c] == "float64"]
        arr = df[num_cols].to_numpy(np.float64)
        bad = ~np.isfinite(arr)
        if bad.any():
            arr[bad] = 0.0
            df[num_cols] = arr
        for col, dt in COLUMN_DTYPES.items():
            if dt in ("int64", "int8"):
                df[col] = df[col].astype(dt)
            elif dt == "string":
                df[col] = df[col].astype(str)
        return df.reset_index(drop=True)
