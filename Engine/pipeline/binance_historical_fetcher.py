"""
================================================================================
BINANCE HISTORICAL ARCHIVE & REST FETCHER (USDT-M FUTURES + SPOT)
================================================================================
Streams
  1. Futures 15m klines      data.binance.vision monthly -> daily -> fapi REST tail
  2. Spot 15m klines         data.binance.vision monthly -> daily -> api  REST tail
  3. Futures official metrics (5m)  daily archives -> futures/data REST bridge
  4. Funding rate history    fapi /fapi/v1/fundingRate (paginated, incremental cache)

Design
  * Every archive object is cached as Parquet under ``cache_dir`` and never
    re-downloaded. 404s (pre-listing / archive lag) are memoised per process.
  * One shared ``HttpClient`` per fetcher: exponential backoff, 418/429 latch.
  * All timestamps are normalised to Unix **milliseconds** (newer archives ship
    microseconds) and every frame is de-duplicated + sorted on its key.
  * Only *closed* candles are ever returned (REST tail is filtered on
    ``close_time < now``).
================================================================================
"""

from __future__ import annotations

import io
import json
import os
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from ..core.canonical_indicators import nice_bin_step, session_day_index
from ..core.schema import FIXED_MERGE_STEPS, LADDER_COLUMNS, LADDER_DTYPES, RUNG_SOURCE_SYNTHETIC, RUNG_SOURCE_TICK
from .http_client import FetchError, HttpClient

BAR_MS = 900_000
DAY_MS = 86_400_000
MAX_RUNGS = 512
VISION = "https://data.binance.vision/data"
FAPI = "https://fapi.binance.com"
SAPI = "https://api.binance.com"

KLINE_COLS = [
    "open_time", "open", "high", "low", "close", "volume", "close_time",
    "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore",
]
KLINE_OUT = [
    "open_time", "open", "high", "low", "close", "volume", "close_time",
    "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume",
]
METRIC_COLS = [
    "timestamp_ms", "sum_open_interest", "sum_open_interest_value",
    "count_toptrader_long_short_ratio", "sum_toptrader_long_short_ratio",
    "count_long_short_ratio", "sum_taker_long_short_vol_ratio",
]
USDC_METRICS_FLOOR = "2023-03-01"   # USDC-margined perps did not exist before this

IMBALANCE_RATIO = 3.0
STACK_MIN_RUN = 3
VALUE_AREA_PCT = 0.70

SUMMARY_COLS = [
    "open_time_ms", "total_vol_coin", "max_single_trade_vol", "taker_buy_vol_coin",
    "taker_sell_vol_coin", "taker_buy_count", "taker_sell_count", "real_poc",
    "poc_vol_ratio", "stacked_buy_imbalances", "stacked_sell_imbalances",
    "bins_populated", "fp_effective_bps", "fp_delta", "fp_poc_price",
    "fp_poc_vol_ratio", "fp_stacked_buy_imb", "fp_stacked_sell_imb", "fp_max_single_trade",
]

FOOTPRINT_SUMMARY_COLUMNS = [
    "open_time_ms",
    "fp_delta",
    "fp_poc_price",
    "fp_poc_vol_ratio",
    "fp_stacked_buy_imb",
    "fp_stacked_sell_imb",
    "fp_max_single_trade",
]


def _session_bin_step(open_time_ms: np.ndarray, opens: np.ndarray) -> np.ndarray:
    day = session_day_index(open_time_ms)
    _, first_idx = np.unique(day, return_index=True)
    step_by_day = nice_bin_step(opens[first_idx])
    day_pos = np.searchsorted(day[first_idx], day)
    return step_by_day[day_pos]


def synthesize_causal_ladder(master: pd.DataFrame) -> pd.DataFrame:
    """Builds synthetic rungs for every row of master under 13-column Table 2 schema."""
    if master.empty:
        return pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)

    ot = master["open_time_ms"].to_numpy(np.int64)
    o = master["open"].to_numpy(np.float64)
    h = master["high"].to_numpy(np.float64)
    l = master["low"].to_numpy(np.float64)
    c = master["close"].to_numpy(np.float64)
    vb = master["volume_base"].to_numpy(np.float64)
    buy = master["taker_buy_vol_btc"].to_numpy(np.float64) if "taker_buy_vol_btc" in master else vb * 0.5
    sell = np.maximum(vb - buy, 0.0)
    tc = master["trade_count"].to_numpy(np.int64) if "trade_count" in master else np.zeros(len(master), dtype=np.int64)
    synthetic_bar = master["is_synthetic"].to_numpy() == 1 if "is_synthetic" in master else np.zeros(len(master), dtype=bool)

    step = _session_bin_step(ot, o)
    lo_bin = np.round(l / step).astype(np.int64)
    hi_bin = np.maximum(np.round(h / step).astype(np.int64), lo_bin)
    n_bins = hi_bin - lo_bin + 1
    too_wide = n_bins > MAX_RUNGS
    if too_wide.any():
        factor = np.ceil(n_bins[too_wide] / MAX_RUNGS)
        step[too_wide] = step[too_wide] * factor
        lo_bin[too_wide] = np.round(l[too_wide] / step[too_wide]).astype(np.int64)
        hi_bin[too_wide] = np.maximum(np.round(h[too_wide] / step[too_wide]).astype(np.int64), lo_bin[too_wide])
        n_bins = hi_bin - lo_bin + 1
    close_bin = np.clip(np.round(c / step).astype(np.int64), lo_bin, hi_bin)
    lo_bin = np.where(synthetic_bar, close_bin, lo_bin)
    hi_bin = np.where(synthetic_bar, close_bin, hi_bin)
    n_bins = hi_bin - lo_bin + 1

    total = int(n_bins.sum())
    bar_idx = np.repeat(np.arange(len(master)), n_bins)
    offsets = np.arange(total) - np.repeat(np.cumsum(n_bins) - n_bins, n_bins)
    bins = lo_bin[bar_idx] + offsets
    step_r = step[bar_idx]
    nb = n_bins[bar_idx].astype(np.float64)

    ask = buy[bar_idx] / nb
    bid = sell[bar_idx] / nb
    trades = np.floor(tc[bar_idx] / nb).astype(np.int64)
    remainder = tc - np.floor(tc / n_bins).astype(np.int64) * n_bins
    trades += (offsets < remainder[bar_idx]).astype(np.int64)

    ladder = pd.DataFrame({
        "open_time_ms": ot[bar_idx],
        "price_bin": np.round(bins * step_r, 8),
        "bid_vol_coin": bid,
        "ask_vol_coin": ask,
        "net_delta_coin": ask - bid,
        "total_vol_coin": ask + bid,
        "trade_count": trades,
        "is_poc": (bins == close_bin[bar_idx]).astype(np.int8),
        "is_buy_imbalance": np.zeros(total, dtype=np.int8),
        "is_sell_imbalance": np.zeros(total, dtype=np.int8),
        "is_stacked_buy_imb": np.zeros(total, dtype=np.int8),
        "is_stacked_sell_imb": np.zeros(total, dtype=np.int8),
        "is_value_area": np.zeros(total, dtype=np.int8),
    })
    return ladder[LADDER_COLUMNS].astype(LADDER_DTYPES)


def assemble_ladder(
    master: pd.DataFrame,
    tick_ladder: Optional[pd.DataFrame] = None,
    allow_synthetic: bool = False,
) -> Tuple[pd.DataFrame, dict]:
    """
    Combines exact tick rungs with master timeline. Under Zero-Synthetic Mandate,
    allow_synthetic defaults to False, strictly enforcing 100% empirical trade executions.
    """
    master_ts = master["open_time_ms"].to_numpy(np.int64)
    if tick_ladder is not None and not tick_ladder.empty:
        cols_to_keep = [c for c in LADDER_COLUMNS if c in tick_ladder.columns]
        tick = tick_ladder[tick_ladder["open_time_ms"].isin(master_ts)][cols_to_keep].copy()
        for c in LADDER_COLUMNS:
            if c not in tick.columns:
                tick[c] = np.zeros(len(tick), dtype=LADDER_DTYPES.get(c, "float64"))
        covered = np.isin(master_ts, tick["open_time_ms"].unique())
    else:
        tick = pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)
        covered = np.zeros(len(master), dtype=bool)

    if allow_synthetic and (~covered).any():
        synthetic = synthesize_causal_ladder(master.loc[~covered])
        ladder = pd.concat([tick[LADDER_COLUMNS], synthetic[LADDER_COLUMNS]], ignore_index=True)
        synthetic_cnt = int((~covered).sum())
        synthetic_rungs = int(len(synthetic))
    else:
        ladder = tick[LADDER_COLUMNS].copy() if not tick.empty else pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)
        synthetic_cnt = 0
        synthetic_rungs = 0

    if not ladder.empty:
        ladder = ladder.astype(LADDER_DTYPES)
        ladder = ladder.sort_values(["open_time_ms", "price_bin"], kind="stable").reset_index(drop=True)

    stats = {
        "candles": int(len(master)),
        "tick_exact_candles": int(covered.sum()),
        "synthetic_candles": synthetic_cnt,
        "tick_rungs": int(len(tick)),
        "synthetic_rungs": synthetic_rungs,
    }
    return ladder, stats


def compute_stacked_imbalances(flag: np.ndarray, bin_idx: np.ndarray, bar_ts: np.ndarray) -> np.ndarray:
    n = flag.size
    out = np.zeros(n, dtype=np.int8)
    if n < STACK_MIN_RUN:
        return out

    same_bar = np.empty(n, dtype=bool)
    same_bar[0] = False
    same_bar[1:] = bar_ts[1:] == bar_ts[:-1]

    active = flag == 1
    i = 0
    while i < n:
        if not active[i]:
            i += 1
            continue
        start = i
        while i + 1 < n and active[i + 1] and same_bar[i + 1] and (bin_idx[i + 1] - bin_idx[i] == 1):
            i += 1
        length = i - start + 1
        if length >= STACK_MIN_RUN:
            out[start : i + 1] = 1
        i += 1
    return out


def compute_value_area(ladder: pd.DataFrame) -> np.ndarray:
    n = len(ladder)
    out = np.zeros(n, dtype=np.int8)
    for _, group in ladder.groupby("open_time_ms", sort=False):
        idx = group.index.to_numpy()
        vols = group["total_vol_coin"].to_numpy(np.float64)
        target_vol = vols.sum() * VALUE_AREA_PCT

        poc_sub_idx = int(np.argmax(vols))
        current_vol = vols[poc_sub_idx]
        in_va = np.zeros(len(group), dtype=bool)
        in_va[poc_sub_idx] = True

        up = poc_sub_idx + 1
        dn = poc_sub_idx - 1

        while current_vol < target_vol and (up < len(group) or dn >= 0):
            v_up = vols[up] if up < len(group) else 0.0
            v_dn = vols[dn] if dn >= 0 else 0.0

            if v_up >= v_dn and up < len(group):
                in_va[up] = True
                current_vol += v_up
                up += 1
            elif dn >= 0:
                in_va[dn] = True
                current_vol += v_dn
                dn -= 1
            else:
                break

        out[idx[in_va]] = 1
    return out


def aggregate_trades_to_ladder(
    trades: pd.DataFrame,
    merge_step: float,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Vectorized grouping and order flow feature calculation.
    Returns (ladder, summary) conforming to Table 2 (13 columns) and master summary specs.
    """
    if trades.empty:
        return pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES), pd.DataFrame(columns=SUMMARY_COLS)

    t_time = trades["transact_time"].to_numpy(np.int64)
    price = trades["price"].to_numpy(np.float64)
    qty = trades["quantity"].to_numpy(np.float64)
    sell_flag = trades["is_buyer_maker"].to_numpy(bool)

    bar_ts = (t_time // BAR_MS) * BAR_MS
    bin_idx = np.round(price / merge_step).astype(np.int64)

    t = pd.DataFrame({
        "open_time_ms": bar_ts,
        "bin_idx": bin_idx,
        "qty": qty,
        "sell_qty": np.where(sell_flag, qty, 0.0),
        "buy_qty": np.where(~sell_flag, qty, 0.0),
    })

    ladder = (
        t.groupby(["open_time_ms", "bin_idx"], sort=True)
        .agg(
            ask_vol_coin=("buy_qty", "sum"),
            bid_vol_coin=("sell_qty", "sum"),
            total_vol_coin=("qty", "sum"),
            trade_count=("qty", "size"),
        )
        .reset_index()
    )
    ladder["price_bin"] = np.round(ladder["bin_idx"] * merge_step, 8)
    ladder["net_delta_coin"] = ladder["ask_vol_coin"] - ladder["bid_vol_coin"]

    bar_agg = (
        t.groupby("open_time_ms", sort=True)
        .agg(
            total_vol_coin=("qty", "sum"),
            max_single_trade_vol=("qty", "max"),
            taker_buy_vol_coin=("buy_qty", "sum"),
            taker_sell_vol_coin=("sell_qty", "sum"),
            trade_count=("qty", "size"),
            taker_sell_count=("sell_qty", lambda s: int((s > 0).sum())),
        )
        .reset_index()
    )
    bar_agg["taker_buy_count"] = bar_agg["trade_count"] - bar_agg["taker_sell_count"]
    bar_agg["total_bar_vol"] = bar_agg["total_vol_coin"]
    bar_agg["max_single_trade"] = bar_agg["max_single_trade_vol"]
    bar_agg["total_net_delta"] = bar_agg["taker_buy_vol_coin"] - bar_agg["taker_sell_vol_coin"]

    order = ladder.sort_values(["open_time_ms", "total_vol_coin", "bin_idx"], ascending=[True, False, True])
    poc_rungs = order.drop_duplicates("open_time_ms")[["open_time_ms", "bin_idx", "total_vol_coin", "price_bin"]].rename(
        columns={"bin_idx": "poc_bin_idx", "total_vol_coin": "poc_vol", "price_bin": "poc_price"}
    )
    poc_rungs["real_poc"] = poc_rungs["poc_price"]

    ladder = ladder.merge(bar_agg[["open_time_ms", "total_bar_vol"]], on="open_time_ms", how="left")
    ladder = ladder.merge(poc_rungs[["open_time_ms", "poc_bin_idx"]], on="open_time_ms", how="left")
    ladder["is_poc"] = (ladder["bin_idx"] == ladder["poc_bin_idx"]).astype(np.int8)

    ladder = ladder.sort_values(["open_time_ms", "bin_idx"]).reset_index(drop=True)
    g = ladder.groupby("open_time_ms", sort=False)

    diff_below = g["bin_idx"].diff(1)
    diff_above = -g["bin_idx"].diff(-1)
    bid_below = g["bid_vol_coin"].shift(1).where(diff_below == 1, 0.0).fillna(0.0)
    ask_above = g["ask_vol_coin"].shift(-1).where(diff_above == 1, 0.0).fillna(0.0)

    p_rung = ladder["price_bin"].to_numpy(np.float64)
    notional_floor = np.maximum(
        ladder["total_bar_vol"].to_numpy(np.float64) * 0.005,
        50.0 / np.maximum(p_rung, 1e-9),
    )

    ask_vol = ladder["ask_vol_coin"].to_numpy(np.float64)
    bid_vol = ladder["bid_vol_coin"].to_numpy(np.float64)

    buy_imb = (
        (ask_vol >= IMBALANCE_RATIO * np.maximum(bid_below.to_numpy(), 1e-9))
        & (ask_vol >= notional_floor)
        & (diff_below.to_numpy() == 1)
    )
    sell_imb = (
        (bid_vol >= IMBALANCE_RATIO * np.maximum(ask_above.to_numpy(), 1e-9))
        & (bid_vol >= notional_floor)
        & (diff_above.to_numpy() == 1)
    )

    ladder["is_buy_imbalance"] = buy_imb.astype(np.int8)
    ladder["is_sell_imbalance"] = sell_imb.astype(np.int8)

    rung_counts = g["bin_idx"].transform("size").to_numpy()
    single_rung_mask = rung_counts < 2
    if single_rung_mask.any():
        ladder.loc[single_rung_mask, "is_poc"] = 1
        ladder.loc[single_rung_mask, "is_buy_imbalance"] = 0
        ladder.loc[single_rung_mask, "is_sell_imbalance"] = 0

    ladder["is_stacked_buy_imb"] = compute_stacked_imbalances(
        ladder["is_buy_imbalance"].to_numpy(np.int8),
        ladder["bin_idx"].to_numpy(np.int64),
        ladder["open_time_ms"].to_numpy(np.int64),
    )
    ladder["is_stacked_sell_imb"] = compute_stacked_imbalances(
        ladder["is_sell_imbalance"].to_numpy(np.int8),
        ladder["bin_idx"].to_numpy(np.int64),
        ladder["open_time_ms"].to_numpy(np.int64),
    )
    ladder["is_value_area"] = compute_value_area(ladder)

    final_ladder = ladder[LADDER_COLUMNS].astype(LADDER_DTYPES).copy()

    stacked_buy_counts = ladder.groupby("open_time_ms")["is_stacked_buy_imb"].max().reset_index()
    stacked_sell_counts = ladder.groupby("open_time_ms")["is_stacked_sell_imb"].max().reset_index()

    summary = bar_agg.merge(poc_rungs[["open_time_ms", "poc_price", "poc_vol", "real_poc"]], on="open_time_ms", how="left")
    summary["poc_vol_ratio"] = summary["poc_vol"] / np.maximum(summary["total_vol_coin"], 1e-12)
    summary["fp_poc_vol_ratio"] = summary["poc_vol_ratio"]
    summary["fp_delta"] = summary["total_net_delta"]
    summary["fp_poc_price"] = summary["poc_price"]
    summary["fp_max_single_trade"] = summary["max_single_trade_vol"]
    summary["stacked_buy_imbalances"] = summary["open_time_ms"].map(stacked_buy_counts.set_index("open_time_ms")["is_stacked_buy_imb"]).fillna(0).astype(np.int64)
    summary["stacked_sell_imbalances"] = summary["open_time_ms"].map(stacked_sell_counts.set_index("open_time_ms")["is_stacked_sell_imb"]).fillna(0).astype(np.int64)
    summary["fp_stacked_buy_imb"] = summary["stacked_buy_imbalances"]
    summary["fp_stacked_sell_imb"] = summary["stacked_sell_imbalances"]
    summary["bins_populated"] = summary["open_time_ms"].map(ladder.groupby("open_time_ms").size()).fillna(0).astype(np.int64)
    first_price = float(trades["price"].iloc[0])
    summary["fp_effective_bps"] = round(merge_step / max(first_price, 1e-12) * 10_000.0, 4)

    return final_ladder, summary[SUMMARY_COLS].copy()


def build_ladder_from_trades(trades: pd.DataFrame, bin_step: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Trades columns: transact_time (ms), price, quantity, is_buyer_maker (bool).
    Returns (summary, ladder) matching test suite contract with 13-column Table 2.
    """
    if trades.empty:
        return pd.DataFrame(columns=SUMMARY_COLS), pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)
    ladder, summary = aggregate_trades_to_ladder(trades, bin_step)
    return summary, ladder




def _utc(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def _ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def _norm_ms(values: pd.Series) -> pd.Series:
    v = pd.to_numeric(values, errors="coerce")
    v = v.where(v <= 2_000_000_000_000, v // 1000)   # microseconds -> milliseconds
    return v.astype("int64")


def _month_keys(start: datetime, end_exclusive: datetime) -> List[str]:
    keys, y, m = [], start.year, start.month
    while datetime(y, m, 1, tzinfo=timezone.utc) < end_exclusive:
        keys.append(f"{y}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return keys


def _day_keys(start: datetime, end_exclusive: datetime) -> List[str]:
    days, d = [], start.replace(hour=0, minute=0, second=0, microsecond=0)
    while d < end_exclusive:
        days.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=1)
    return days


def _unzip_first(data: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        return zf.read(zf.namelist()[0]).decode("utf-8")


def parse_kline_csv(text: str) -> pd.DataFrame:
    """Parses a Binance Vision kline CSV (with or without header row)."""
    first = text.split("\n", 1)[0]
    has_header = first.lower().startswith("open_time")
    df = pd.read_csv(io.StringIO(text), header=0 if has_header else None)
    df.columns = KLINE_COLS[: len(df.columns)]
    df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()].copy()
    if df.empty:
        return pd.DataFrame(columns=KLINE_OUT)
    df["open_time"] = _norm_ms(df["open_time"])
    df["close_time"] = _norm_ms(df["close_time"])
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype("int64")
    for c in ("open", "high", "low", "close", "volume", "quote_volume", "taker_buy_volume", "taker_buy_quote_volume"):
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")
    return df[KLINE_OUT]


def parse_kline_rest(rows: Sequence[Sequence]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=KLINE_OUT)
    df = pd.DataFrame(rows, columns=KLINE_COLS)
    df["open_time"] = _norm_ms(df["open_time"])
    df["close_time"] = _norm_ms(df["close_time"])
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype("int64")
    for c in ("open", "high", "low", "close", "volume", "quote_volume", "taker_buy_volume", "taker_buy_quote_volume"):
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")
    return df[KLINE_OUT]


def parse_metrics_csv(text: str) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(text))
    if "create_time" not in df.columns:
        return pd.DataFrame(columns=METRIC_COLS)
    ts = pd.to_datetime(df["create_time"], utc=True, errors="coerce")
    df = df[ts.notna()].copy()
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    df["timestamp_ms"] = ((ts[ts.notna()] - epoch) // pd.Timedelta(milliseconds=1)).astype("int64")
    for c in METRIC_COLS[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce") if c in df.columns else np.nan
    return df[METRIC_COLS]


class BinanceHistoricalFetcher:
    def __init__(self, cache_dir: str = "./data_cache", max_workers: int = 16, http: Optional[HttpClient] = None,
                 log: Callable[[str], None] = print) -> None:
        self.cache_dir = os.path.abspath(cache_dir)
        self.max_workers = max(1, max_workers)
        self.metrics_absent_days: List[str] = []
        self.http = http or HttpClient()
        self.log = log
        self.dirs = {
            "fut_klines": os.path.join(self.cache_dir, "klines_15m"),
            "spot_klines": os.path.join(self.cache_dir, "spot_klines_15m"),
            "metrics": os.path.join(self.cache_dir, "metrics_daily"),
            "funding": os.path.join(self.cache_dir, "funding_rates"),
            "footprint": os.path.join(self.cache_dir, "footprint_monthly"),
        }

        for d in self.dirs.values():
            os.makedirs(d, exist_ok=True)

    # ------------------------------------------------------------------ cache
    def _cached(self, kind: str, key: str, url: str, parser: Callable[[str], pd.DataFrame]) -> Optional[pd.DataFrame]:
        """Returns parsed archive frame; ``None`` when the object does not exist."""
        path = os.path.join(self.dirs[kind], f"{key}.parquet")
        if os.path.exists(path):
            try:
                return pd.read_parquet(path)
            except Exception as exc:  # corrupt cache -> refetch
                self.log(f"  [CACHE] unreadable {path} ({exc}); refetching")
                os.remove(path)
        data = self.http.get_optional(url)
        if data is None:
            return None
        try:
            df = parser(_unzip_first(data))
        except Exception as exc:
            self.log(f"  [WARN] parse failure {url}: {exc}")
            return None
        tmp = path + ".tmp"
        df.to_parquet(tmp, index=False)
        os.replace(tmp, path)
        return df

    def _parallel(self, fn: Callable[[str], Optional[pd.DataFrame]], keys: Sequence[str], label: str) -> Dict[str, Optional[pd.DataFrame]]:
        out: Dict[str, Optional[pd.DataFrame]] = {}
        if not keys:
            return out
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futs = {pool.submit(fn, k): k for k in keys}
            done = 0
            for fut in as_completed(futs):
                k = futs[fut]
                try:
                    out[k] = fut.result()
                except FetchError as exc:
                    self.log(f"  [FATAL TRANSPORT ERROR] {label} {k}: {exc}")
                    raise
                done += 1
                if done % 200 == 0 or done == len(keys):
                    self.log(f"  [FETCHER] {label}: {done}/{len(keys)}")
        return out

    # ------------------------------------------------------------------ klines
    def _fetch_klines(self, market: str, symbol: str, start: datetime, now: datetime) -> pd.DataFrame:
        kind = "fut_klines" if market == "futures" else "spot_klines"
        base = f"{VISION}/futures/um" if market == "futures" else f"{VISION}/spot"
        rest = (f"{FAPI}/fapi/v1/klines" if market == "futures" else f"{SAPI}/api/v3/klines")

        def monthly(ym: str) -> Optional[pd.DataFrame]:
            return self._cached(kind, f"{symbol}-15m-{ym}", f"{base}/monthly/klines/{symbol}/15m/{symbol}-15m-{ym}.zip", parse_kline_csv)

        def daily(ymd: str) -> Optional[pd.DataFrame]:
            return self._cached(kind, f"{symbol}-15m-{ymd}", f"{base}/daily/klines/{symbol}/15m/{symbol}-15m-{ymd}.zip", parse_kline_csv)

        live_now = datetime.now(timezone.utc)
        live_cur_month_start = datetime(live_now.year, live_now.month, 1, tzinfo=timezone.utc)
        next_month_start = datetime(now.year + (now.month == 12), 1 if now.month == 12 else now.month + 1, 1, tzinfo=timezone.utc)
        if now >= next_month_start - timedelta(seconds=1) and next_month_start <= live_cur_month_start:
            month_end_exclusive = next_month_start
        else:
            month_end_exclusive = min(datetime(now.year, now.month, 1, tzinfo=timezone.utc), live_cur_month_start)

        months = _month_keys(start, month_end_exclusive)
        monthly_res = self._parallel(monthly, months, f"{symbol} {market} monthly klines")
        frames = [df for df in monthly_res.values() if df is not None and not df.empty]

        # months missing from the monthly archive (listing gaps, archive lag) -> daily objects
        # Months before listing 404 on both monthly and daily objects; only probe
        # daily objects from the month preceding the first available monthly
        # archive onwards (plus the two most recent months for archive lag).
        first_ok = next((i for i, ym in enumerate(months) if monthly_res.get(ym) is not None), None)
        daily_keys: List[str] = []
        for i, ym in enumerate(months):
            if monthly_res.get(ym) is not None:
                continue
            near_recent = i >= len(months) - 2
            after_listing = first_ok is not None and i >= first_ok - 1
            if near_recent or after_listing:
                y, m = int(ym[:4]), int(ym[5:])
                m_start = datetime(y, m, 1, tzinfo=timezone.utc)
                m_end = datetime(y + (m == 12), 1 if m == 12 else m + 1, 1, tzinfo=timezone.utc)
                daily_keys += _day_keys(max(m_start, start), min(m_end, now))
        end_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if (now.hour >= 23 and now.minute >= 45) and end_day < live_now.replace(hour=0, minute=0, second=0, microsecond=0):
            end_day += timedelta(days=1)
        daily_keys += _day_keys(max(month_end_exclusive, start), end_day)
        daily_res = self._parallel(daily, daily_keys, f"{symbol} {market} daily klines")
        frames += [df for df in daily_res.values() if df is not None and not df.empty]

        df = self._merge_klines(frames)
        last_ms = int(df["open_time"].iloc[-1]) if not df.empty else _ms(start) - BAR_MS
        tail = self._rest_klines(rest, symbol, last_ms + BAR_MS, _ms(now))
        if not tail.empty:
            df = self._merge_klines([df, tail])
        df = self._repair_gaps(df, rest, symbol, now)
        return df

    def _rest_klines(self, endpoint: str, symbol: str, start_ms: int, end_ms: int) -> pd.DataFrame:
        """Closed candles in [start_ms, end_ms); the candle still forming at ``end_ms`` is never returned."""
        frames: List[pd.DataFrame] = []
        cur = start_ms
        now_ms = min(end_ms, _ms(datetime.now(timezone.utc)))
        while cur < end_ms:
            url = f"{endpoint}?symbol={symbol}&interval=15m&startTime={cur}&endTime={end_ms}&limit=1500"
            raw = self.http.get_optional(url)
            if raw is None:
                break
            rows = json.loads(raw.decode("utf-8"))
            if not isinstance(rows, list) or not rows:
                break
            part = parse_kline_rest(rows)
            part = part[part["close_time"] < now_ms]       # never emit the forming candle
            if part.empty:
                break
            frames.append(part)
            nxt = int(part["open_time"].iloc[-1]) + BAR_MS
            if nxt <= cur or len(rows) < 1500:
                break
            cur = nxt
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=KLINE_OUT)

    @staticmethod
    def _merge_klines(frames: List[pd.DataFrame]) -> pd.DataFrame:
        frames = [f for f in frames if f is not None and not f.empty]
        if not frames:
            return pd.DataFrame(columns=KLINE_OUT)
        df = pd.concat(frames, ignore_index=True)
        df = df[df["open_time"] % BAR_MS == 0]
        df = df.drop_duplicates("open_time", keep="last").sort_values("open_time").reset_index(drop=True)
        return df

    def _repair_gaps(self, df: pd.DataFrame, endpoint: str, symbol: str, now: datetime) -> pd.DataFrame:
        if len(df) < 2:
            return df
        ot = df["open_time"].to_numpy()
        gap_idx = np.where(np.diff(ot) > BAR_MS)[0]
        if gap_idx.size == 0:
            return df
        self.log(f"  [FETCHER] {symbol}: {gap_idx.size} archive gap(s); attempting REST repair")
        patches = []
        for i in gap_idx[:200]:
            patches.append(self._rest_klines(endpoint, symbol, int(ot[i]) + BAR_MS, int(ot[i + 1]) + BAR_MS - 1))
        repaired = self._merge_klines([df] + patches)
        residual = int((np.diff(repaired["open_time"].to_numpy()) > BAR_MS).sum())
        self.log(f"  [FETCHER] {symbol}: residual gaps after repair = {residual} (exchange downtime; reconstructed downstream)")
        return repaired

    def fetch_futures_klines(self, symbol: str, start_date: str, now: Optional[datetime] = None) -> pd.DataFrame:
        now = now or datetime.now(timezone.utc)
        self.log(f"[FETCHER] {symbol}: futures 15m klines from {start_date}")
        df = self._fetch_klines("futures", symbol, _utc(start_date), now)
        if df.empty:
            raise RuntimeError(f"no futures klines retrieved for {symbol}")
        self.log(f"[FETCHER] {symbol}: {len(df):,} futures bars "
                 f"({pd.to_datetime(df['open_time'].iloc[0], unit='ms', utc=True)} -> {pd.to_datetime(df['open_time'].iloc[-1], unit='ms', utc=True)})")
        return df

    def fetch_spot_klines(self, symbol: str, start_date: str, now: Optional[datetime] = None) -> pd.DataFrame:
        now = now or datetime.now(timezone.utc)
        self.log(f"[FETCHER] {symbol}: spot 15m klines from {start_date}")
        df = self._fetch_klines("spot", symbol, _utc(start_date), now)
        if df.empty:
            self.log(f"[WARN] {symbol}: no spot klines available")
            return pd.DataFrame(columns=["open_time", "spot_close", "spot_volume", "spot_taker_buy_volume"])
        out = df[["open_time", "close", "volume", "taker_buy_volume"]].rename(
            columns={"close": "spot_close", "volume": "spot_volume", "taker_buy_volume": "spot_taker_buy_volume"})
        self.log(f"[FETCHER] {symbol}: {len(out):,} spot bars")
        return out.reset_index(drop=True)

    # ------------------------------------------------------------------ metrics
    def fetch_metrics(self, symbol: str, start_date: str, now: Optional[datetime] = None, include_usdc: bool = True) -> pd.DataFrame:
        now = now or datetime.now(timezone.utc)
        start = _utc(start_date)
        self.log(f"[FETCHER] {symbol}: official futures metrics from {start_date}")
        days = _day_keys(start, now)

        def daily(sym: str) -> Callable[[str], Optional[pd.DataFrame]]:
            def _f(ymd: str) -> Optional[pd.DataFrame]:
                return self._cached("metrics", f"{sym}-metrics-{ymd}",
                                    f"{VISION}/futures/um/daily/metrics/{sym}/{sym}-metrics-{ymd}.zip", parse_metrics_csv)
            return _f

        res = self._parallel(daily(symbol), days, f"{symbol} metrics")
        # Coverage inventory: days whose archive object does not exist on the host at all.
        # Recorded here, at the fetch site, because it is the only evidence about the *source*
        # in this pipeline: a frame can come up empty through a parse or join bug, but a None
        # from _cached means Binance published no metrics archive for that day. The council
        # (verify_parquet_integrity.agent_schema) uses it to tell legitimate pre-archive
        # absence apart from fabricated coverage, so it must not be derived from the frame.
        absent = sorted(d for d, df in res.items() if df is None or df.empty)
        self.metrics_absent_days = absent
        if absent:
            self.log(f"[FETCHER] {symbol}: metrics archive absent for {len(absent)} day(s) "
                     f"({absent[0]} .. {absent[-1]})")
        frames = [df for df in res.values() if df is not None and not df.empty]
        primary = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=METRIC_COLS)
        primary = primary.drop_duplicates("timestamp_ms").sort_values("timestamp_ms").reset_index(drop=True)

        usdc_symbol = symbol[:-4] + "USDC" if symbol.endswith("USDT") else None
        if include_usdc and usdc_symbol:
            usdc_days = [d for d in days if d >= USDC_METRICS_FLOOR]
            probe = self._parallel(daily(usdc_symbol), usdc_days[-3:], f"{usdc_symbol} probe") if usdc_days else {}
            if any(v is not None for v in probe.values()):
                ures = self._parallel(daily(usdc_symbol), usdc_days, f"{usdc_symbol} metrics")
                uframes = [df for df in ures.values() if df is not None and not df.empty]
                if uframes:
                    usdc = pd.concat(uframes, ignore_index=True).drop_duplicates("timestamp_ms")
                    usdc = usdc[["timestamp_ms", "sum_open_interest", "sum_open_interest_value"]].rename(
                        columns={"sum_open_interest": "_oi_usdc", "sum_open_interest_value": "_oiv_usdc"})
                    primary = primary.merge(usdc, on="timestamp_ms", how="left")
                    # Bound addition strictly to post-floor rows and use .add(fill_value=0.0) so NaN+NaN remains NaN
                    usdc_floor_ms = _ms(_utc(USDC_METRICS_FLOOR))
                    mask = primary["timestamp_ms"] >= usdc_floor_ms
                    primary.loc[mask, "sum_open_interest"] = primary.loc[mask, "sum_open_interest"].add(
                        primary.loc[mask, "_oi_usdc"], fill_value=0.0
                    )
                    primary.loc[mask, "sum_open_interest_value"] = primary.loc[mask, "sum_open_interest_value"].add(
                        primary.loc[mask, "_oiv_usdc"], fill_value=0.0
                    )
                    primary = primary.drop(columns=["_oi_usdc", "_oiv_usdc"])
                    self.log(f"[FETCHER] {symbol}: aggregated stablecoin OI with {usdc_symbol}")

        bridge = self._rest_metrics_bridge(symbol)
        if not bridge.empty:
            last = int(primary["timestamp_ms"].max()) if not primary.empty else 0
            new = bridge[bridge["timestamp_ms"] > last]
            if not new.empty:
                primary = pd.concat([primary, new], ignore_index=True).sort_values("timestamp_ms").reset_index(drop=True)
                self.log(f"[FETCHER] {symbol}: bridged {len(new)} recent metric rows via REST")
        self.log(f"[FETCHER] {symbol}: {len(primary):,} metric snapshots")
        return primary[METRIC_COLS]

    def _rest_metrics_bridge(self, symbol: str) -> pd.DataFrame:
        endpoints = {
            "oi": (f"{FAPI}/futures/data/openInterestHist", {"sumOpenInterest": "sum_open_interest", "sumOpenInterestValue": "sum_open_interest_value"}),
            "gls": (f"{FAPI}/futures/data/globalLongShortAccountRatio", {"longShortRatio": "count_long_short_ratio"}),
            "tpos": (f"{FAPI}/futures/data/topLongShortPositionRatio", {"longShortRatio": "sum_toptrader_long_short_ratio"}),
            "tacc": (f"{FAPI}/futures/data/topLongShortAccountRatio", {"longShortRatio": "count_toptrader_long_short_ratio"}),
            "tk": (f"{FAPI}/futures/data/takerlongshortRatio", {"buySellRatio": "sum_taker_long_short_vol_ratio"}),
        }
        merged: Optional[pd.DataFrame] = None
        for _, (url, rename) in endpoints.items():
            raw = self.http.get_optional(f"{url}?symbol={symbol}&period=15m&limit=500")
            if raw is None:
                continue
            try:
                rows = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            if not isinstance(rows, list) or not rows:
                continue
            part = pd.DataFrame(rows).rename(columns={"timestamp": "timestamp_ms", **rename})
            keep = ["timestamp_ms"] + list(rename.values())
            part = part[[c for c in keep if c in part.columns]].copy()
            part["timestamp_ms"] = _norm_ms(part["timestamp_ms"])
            for c in rename.values():
                if c in part.columns:
                    part[c] = pd.to_numeric(part[c], errors="coerce")
            merged = part if merged is None else merged.merge(part, on="timestamp_ms", how="outer")
        if merged is None or "sum_open_interest" not in merged.columns:
            return pd.DataFrame(columns=METRIC_COLS)
        for c in METRIC_COLS:
            if c not in merged.columns:
                merged[c] = np.nan
        return merged[METRIC_COLS].sort_values("timestamp_ms").reset_index(drop=True)

    # ------------------------------------------------------------------ funding
    def fetch_funding_rates(self, symbol: str, start_time_ms: int) -> pd.DataFrame:
        cache = os.path.join(self.dirs["funding"], f"{symbol}_funding_rates.parquet")
        cached = pd.DataFrame(columns=["fundingTime", "fundingRate"])
        if os.path.exists(cache):
            try:
                cached = pd.read_parquet(cache)
            except Exception:
                cached = pd.DataFrame(columns=["fundingTime", "fundingRate"])
        cur = start_time_ms
        if not cached.empty:
            cur = max(cur, int(cached["fundingTime"].max()) + 1)
        rows: List[dict] = []
        self.log(f"[FETCHER] {symbol}: funding rates from {pd.to_datetime(cur, unit='ms', utc=True)}")
        while True:
            raw = self.http.get_optional(f"{FAPI}/fapi/v1/fundingRate?symbol={symbol}&startTime={cur}&limit=1000")
            if raw is None:
                break
            data = json.loads(raw.decode("utf-8"))
            if not isinstance(data, list) or not data:
                break
            rows += [{"fundingTime": int(d["fundingTime"]), "fundingRate": float(d["fundingRate"])} for d in data if d.get("fundingRate") not in (None, "")]
            if len(data) < 1000:
                break
            cur = int(data[-1]["fundingTime"]) + 1
        df = pd.concat([cached, pd.DataFrame(rows)], ignore_index=True) if rows else cached
        if df.empty:
            self.log(f"[WARN] {symbol}: no funding history")
            return pd.DataFrame(columns=["fundingTime", "fundingRate"])
        df["fundingTime"] = df["fundingTime"].astype("int64")
        df["fundingRate"] = df["fundingRate"].astype("float64")
        df = df.drop_duplicates("fundingTime").sort_values("fundingTime").reset_index(drop=True)
        tmp = cache + ".tmp"
        df.to_parquet(tmp, index=False)
        os.replace(tmp, cache)
        self.log(f"[FETCHER] {symbol}: {len(df):,} funding events")
        return df[df["fundingTime"] >= start_time_ms].reset_index(drop=True)

    # ------------------------------------------------------------------ footprint (100% real aggTrades)
    def get_merge_step(self, symbol: str) -> float:
        """Retrieves the fixed institutional merge step for the given asset."""
        if symbol in FIXED_MERGE_STEPS:
            return float(FIXED_MERGE_STEPS[symbol])
        return 0.01

    def fetch_footprint(
        self,
        symbol: str,
        start_date_str: str,
        end_date_str: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Streams and aggregates 100% real tick aggTrades into Table 2 footprint ladder.
        Streams month-by-month with zero filesystem footprint for raw CSV/ZIP files,
        using monthly interim parquet chunks to ensure full resumability.
        """
        now = now or datetime.now(timezone.utc)
        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc) if end_date_str else now

        curr = datetime(start_dt.year, start_dt.month, 1, tzinfo=timezone.utc)
        months_to_process: List[Tuple[int, int]] = []
        while curr <= end_dt:
            months_to_process.append((curr.year, curr.month))
            if curr.month == 12:
                curr = datetime(curr.year + 1, 1, 1, tzinfo=timezone.utc)
            else:
                curr = datetime(curr.year, curr.month + 1, 1, tzinfo=timezone.utc)

        self.log(f"[FOOTPRINT] {symbol}: fetching real tick aggTrades across {len(months_to_process)} months "
                 f"({start_dt:%Y-%m-%d} -> {end_dt:%Y-%m-%d}) | fixed step=${self.get_merge_step(symbol)}")

        ladder_chunks: List[pd.DataFrame] = []
        summary_chunks: List[pd.DataFrame] = []

        for y, m in months_to_process:
            t0 = time.time()
            m_ladder, m_summary = self.fetch_and_process_footprint_month(symbol, y, m, start_dt, end_dt)
            elapsed = time.time() - t0
            if not m_ladder.empty:
                rungs_cnt = len(m_ladder)
                bars_cnt = len(m_summary)
                self.log(f"  [FOOTPRINT] {symbol} {y:04d}-{m:02d}: {rungs_cnt:,} rungs across {bars_cnt:,} candles ({elapsed:.1f}s)")
                ladder_chunks.append(m_ladder)
                summary_chunks.append(m_summary)
            else:
                self.log(f"  [FOOTPRINT] {symbol} {y:04d}-{m:02d}: 0 trades (unlisted or archive gap)")

        if not ladder_chunks:
            self.log(f"[FOOTPRINT] {symbol}: zero tick rungs found across requested date range")
            return pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES), pd.DataFrame(columns=FOOTPRINT_SUMMARY_COLUMNS)

        full_ladder = pd.concat(ladder_chunks, ignore_index=True).sort_values(["open_time_ms", "price_bin"]).reset_index(drop=True)
        full_summary = pd.concat(summary_chunks, ignore_index=True).sort_values("open_time_ms").reset_index(drop=True)

        return full_ladder, full_summary

    def fetch_and_process_footprint_month(
        self,
        symbol: str,
        year: int,
        month: int,
        start_dt: datetime,
        end_dt: datetime,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        month_str = f"{year:04d}-{month:02d}"
        cache_ladder_path = os.path.join(self.dirs["footprint"], f"{symbol}_ladder_{month_str}.parquet")
        cache_summary_path = os.path.join(self.dirs["footprint"], f"{symbol}_summary_{month_str}.parquet")

        if os.path.exists(cache_ladder_path) and os.path.exists(cache_summary_path):
            try:
                ladder_df = pd.read_parquet(cache_ladder_path)
                summary_df = pd.read_parquet(cache_summary_path)
                return ladder_df, summary_df
            except Exception as e:
                self.log(f"  [FOOTPRINT] corrupted monthly cache {month_str} ({e}); re-processing")

        first_day = datetime(year, month, 1, tzinfo=timezone.utc)
        next_month = datetime(year + 1, 1, 1, tzinfo=timezone.utc) if month == 12 else datetime(year, month + 1, 1, tzinfo=timezone.utc)
        day_cursor = max(first_day, start_dt)
        month_end = min(next_month - timedelta(days=1), end_dt)

        dates_to_fetch: List[str] = []
        while day_cursor <= month_end:
            dates_to_fetch.append(day_cursor.strftime("%Y-%m-%d"))
            day_cursor += timedelta(days=1)

        if not dates_to_fetch:
            return pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES), pd.DataFrame(columns=FOOTPRINT_SUMMARY_COLUMNS)

        merge_step = self.get_merge_step(symbol)
        daily_ladders: List[pd.DataFrame] = []
        daily_summaries: List[pd.DataFrame] = []

        def _fetch_day(d_str: str) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
            trades = self._download_day_trades_in_memory(symbol, d_str)
            if trades is None or trades.empty:
                return None
            return self._aggregate_trades_to_ladder(trades, merge_step)

        # Bound concurrency to prevent RAM exhaustion on large trade zip decompression
        fp_workers = max(1, min(self.max_workers // 2, 6))
        with ThreadPoolExecutor(max_workers=fp_workers) as executor:
            future_to_date = {executor.submit(_fetch_day, d): d for d in dates_to_fetch}
            for future in as_completed(future_to_date):
                d_str = future_to_date[future]
                try:
                    res = future.result()
                    if res is not None:
                        d_ladder, d_summary = res
                        if not d_ladder.empty:
                            daily_ladders.append(d_ladder)
                            daily_summaries.append(d_summary)
                except Exception as exc:
                    self.log(f"  [FOOTPRINT] {symbol} {d_str} processing error: {exc}")
                    raise

        if not daily_ladders:
            empty_ladder = pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)
            empty_summary = pd.DataFrame(columns=FOOTPRINT_SUMMARY_COLUMNS)
            return empty_ladder, empty_summary

        month_ladder = pd.concat(daily_ladders, ignore_index=True).sort_values(["open_time_ms", "price_bin"]).reset_index(drop=True)
        month_summary = pd.concat(daily_summaries, ignore_index=True).sort_values("open_time_ms").reset_index(drop=True)

        try:
            month_ladder.to_parquet(cache_ladder_path, compression="zstd", index=False)
            month_summary.to_parquet(cache_summary_path, compression="zstd", index=False)
        except Exception as e:
            self.log(f"  [FOOTPRINT] failed to write monthly cache for {month_str}: {e}")

        return month_ladder, month_summary

    def _download_day_trades_in_memory(self, symbol: str, date_str: str) -> Optional[pd.DataFrame]:
        url = f"https://data.binance.vision/data/futures/um/daily/aggTrades/{symbol}/{symbol}-aggTrades-{date_str}.zip"
        try:
            data = self.http.get_optional(url, timeout=30.0)
            if data is None or len(data) == 0:
                return None

            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                csv_names = [name for name in zf.namelist() if name.endswith(".csv")]
                if not csv_names:
                    return None
                with zf.open(csv_names[0]) as csv_file:
                    first_line = csv_file.readline().decode("utf-8")
                    has_header = "price" in first_line.lower() or "transact_time" in first_line.lower()
                    csv_file.seek(0)
                    header_opt = 0 if has_header else None
                    names = None if has_header else ["agg_trade_id", "price", "quantity", "first_trade_id", "last_trade_id", "transact_time", "is_buyer_maker"]

                    df = pd.read_csv(
                        csv_file,
                        header=header_opt,
                        names=names,
                        usecols=["price", "quantity", "transact_time", "is_buyer_maker"],
                        dtype={
                            "price": "float64",
                            "quantity": "float64",
                            "transact_time": "int64",
                            "is_buyer_maker": "bool",
                        },
                    )
                    return df
        except FetchError as e:
            self.log(f"  [FATAL TRANSPORT ERROR] {symbol} {date_str} aggTrades: {e}")
            raise
        except Exception as e:
            self.log(f"  [FOOTPRINT] error streaming aggTrades for {symbol} {date_str}: {e}")
            return None

    def _aggregate_trades_to_ladder(
        self,
        trades: pd.DataFrame,
        merge_step: float,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return aggregate_trades_to_ladder(trades, merge_step)


