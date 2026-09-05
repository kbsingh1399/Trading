"""
================================================================================
TICK FOOTPRINT FETCHER (aggTrades -> 15m price ladder, Table 2 exact rungs)
================================================================================
Per UTC day:
  1. Download futures/um/daily/aggTrades/{symbol}/{symbol}-aggTrades-{date}.zip
  2. Bucket every trade into (open_time_ms, bin_idx) using a bin step derived
     causally from the FIRST trade price of the day (~3.5 bps).
  3. Aggregate bid (taker-sell) / ask (taker-buy) volume, trade counts, per-bar
     POC, diagonal imbalances (>= 3:1 against the strictly adjacent rung, with a
     notional floor) and contiguous stacked-imbalance clusters (>= 3 rungs).

Everything after the CSV parse is vectorised pandas/NumPy; there is no per-bar
loop. Both the per-bar summary and the per-rung ladder are cached as Parquet.
================================================================================
"""

from __future__ import annotations

import io
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Callable, List, Optional, Tuple

import numpy as np
import pandas as pd

from ..core.canonical_indicators import nice_bin_step
from ..core.schema import LADDER_COLUMNS, LADDER_DTYPES, RUNG_SOURCE_TICK
from .http_client import FetchError, HttpClient

BAR_MS = 900_000
VISION = "https://data.binance.vision/data/futures/um/daily/aggTrades"
IMBALANCE_RATIO = 3.0
STACK_MIN_RUN = 3
SUMMARY_COLS = [
    "open_time_ms", "total_vol_coin", "max_single_trade_vol", "taker_buy_vol_coin",
    "taker_sell_vol_coin", "taker_buy_count", "taker_sell_count", "real_poc",
    "poc_vol_ratio", "stacked_buy_imbalances", "stacked_sell_imbalances",
    "bins_populated", "fp_effective_bps",
]


def _count_stacked_runs(flag: np.ndarray, contiguous: np.ndarray, group: np.ndarray, min_run: int = STACK_MIN_RUN) -> pd.Series:
    """
    Counts, per group, runs of >= ``min_run`` consecutive rows where ``flag``
    is set AND each row is price-contiguous with the previous one. Vectorised
    run-length encoding: a run breaks when flag drops, adjacency breaks, or the
    group changes.
    """
    n = flag.size
    if n == 0:
        return pd.Series(dtype="int64")
    same_group = np.empty(n, dtype=bool)
    same_group[0] = False
    same_group[1:] = group[1:] == group[:-1]
    prev_flag = np.empty(n, dtype=bool)
    prev_flag[0] = False
    prev_flag[1:] = flag[:-1]
    continues = flag & prev_flag & contiguous & same_group
    run_start = flag & ~continues
    run_id = np.cumsum(run_start)
    run_len = np.bincount(run_id, weights=flag.astype(np.int64))
    is_last_of_run = flag & ~np.append(continues[1:], False)
    qualifying = is_last_of_run & (run_len[run_id] >= min_run)
    return pd.Series(qualifying.astype(np.int64)).groupby(group).sum()


def build_ladder_from_trades(trades: pd.DataFrame, bin_step: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    ``trades`` columns: transact_time (ms), price, quantity, is_buyer_maker (bool).
    Returns (per-bar summary, per-rung ladder) for the trades supplied.
    """
    if trades.empty:
        return pd.DataFrame(columns=SUMMARY_COLS), pd.DataFrame(columns=LADDER_COLUMNS)

    t = pd.DataFrame({
        "open_time_ms": (trades["transact_time"].to_numpy(np.int64) // BAR_MS) * BAR_MS,
        "bin_idx": np.round(trades["price"].to_numpy(np.float64) / bin_step).astype(np.int64),
        "qty": trades["quantity"].to_numpy(np.float64),
        "sell": trades["is_buyer_maker"].to_numpy(bool),
    })
    t["buy_qty"] = np.where(t["sell"], 0.0, t["qty"])
    t["sell_qty"] = np.where(t["sell"], t["qty"], 0.0)

    ladder = (t.groupby(["open_time_ms", "bin_idx"], sort=True)
                .agg(ask_vol_coin=("buy_qty", "sum"), bid_vol_coin=("sell_qty", "sum"), trade_count=("qty", "size"))
                .reset_index())
    ladder["total"] = ladder["ask_vol_coin"] + ladder["bid_vol_coin"]

    bar = (t.groupby("open_time_ms", sort=True)
             .agg(total_vol_coin=("qty", "sum"), max_single_trade_vol=("qty", "max"),
                  taker_buy_vol_coin=("buy_qty", "sum"), taker_sell_vol_coin=("sell_qty", "sum"),
                  taker_sell_count=("sell", "sum"), trade_count=("qty", "size"))
             .reset_index())
    bar["taker_buy_count"] = bar["trade_count"] - bar["taker_sell_count"]
    bar = bar.drop(columns="trade_count")

    # POC: max-volume rung per bar (ties -> lowest price, deterministic)
    order = ladder.sort_values(["open_time_ms", "total", "bin_idx"], ascending=[True, False, True])
    poc = order.drop_duplicates("open_time_ms")[["open_time_ms", "bin_idx", "total"]].rename(
        columns={"bin_idx": "poc_bin_idx", "total": "poc_volume"})
    bar = bar.merge(poc, on="open_time_ms", how="left")
    bar["real_poc"] = bar["poc_bin_idx"] * bin_step
    bar["poc_vol_ratio"] = bar["poc_volume"] / np.maximum(bar["total_vol_coin"], 1e-12)

    # Diagonal imbalances against strictly adjacent rungs
    ladder = ladder.merge(bar[["open_time_ms", "total_vol_coin"]], on="open_time_ms", how="left")
    ladder = ladder.merge(poc[["open_time_ms", "poc_bin_idx"]], on="open_time_ms", how="left")
    g = ladder.groupby("open_time_ms", sort=False)
    diff_below = g["bin_idx"].diff(1)
    diff_above = -g["bin_idx"].diff(-1)
    bid_below = g["bid_vol_coin"].shift(1).where(diff_below == 1, 0.0).fillna(0.0)
    ask_above = g["ask_vol_coin"].shift(-1).where(diff_above == 1, 0.0).fillna(0.0)
    price = ladder["bin_idx"].to_numpy(np.float64) * bin_step
    floor = np.maximum(ladder["total_vol_coin"].to_numpy() * 0.005, 50.0 / np.maximum(price, 1e-9))
    buy_imb = ((ladder["ask_vol_coin"] >= IMBALANCE_RATIO * np.maximum(bid_below, 1e-9)) &
               (ladder["ask_vol_coin"] >= floor) & (diff_below == 1)).to_numpy()
    sell_imb = ((ladder["bid_vol_coin"] >= IMBALANCE_RATIO * np.maximum(ask_above, 1e-9)) &
                (ladder["bid_vol_coin"] >= floor) & (diff_above == 1)).to_numpy()
    contiguous = (diff_below == 1).fillna(False).to_numpy()
    groups = ladder["open_time_ms"].to_numpy()
    stacked_buy = _count_stacked_runs(buy_imb, contiguous, groups)
    stacked_sell = _count_stacked_runs(sell_imb, contiguous, groups)
    bins_populated = ladder.groupby("open_time_ms").size()

    bar["stacked_buy_imbalances"] = bar["open_time_ms"].map(stacked_buy).fillna(0).astype(np.int64)
    bar["stacked_sell_imbalances"] = bar["open_time_ms"].map(stacked_sell).fillna(0).astype(np.int64)
    bar["bins_populated"] = bar["open_time_ms"].map(bins_populated).fillna(0).astype(np.int64)
    first_price = float(trades["price"].iloc[0])
    bar["fp_effective_bps"] = round(bin_step / max(first_price, 1e-12) * 10_000.0, 4)
    bar = bar.drop(columns=["poc_bin_idx", "poc_volume"])

    out = pd.DataFrame({
        "open_time_ms": ladder["open_time_ms"].to_numpy(np.int64),
        "price_bin": price,
        "bid_vol_coin": ladder["bid_vol_coin"].to_numpy(np.float64),
        "ask_vol_coin": ladder["ask_vol_coin"].to_numpy(np.float64),
        "net_delta_coin": (ladder["ask_vol_coin"] - ladder["bid_vol_coin"]).to_numpy(np.float64),
        "is_buy_imbalance": buy_imb.astype(np.int8),
        "is_sell_imbalance": sell_imb.astype(np.int8),
        "is_poc": (ladder["bin_idx"] == ladder["poc_bin_idx"]).to_numpy().astype(np.int8),
        "trade_count": ladder["trade_count"].to_numpy(np.int64),
        "rung_source": np.full(len(ladder), RUNG_SOURCE_TICK, dtype=np.int8),
    })
    return bar[SUMMARY_COLS], out[LADDER_COLUMNS].astype(LADDER_DTYPES)


def parse_aggtrades_csv(text: str) -> pd.DataFrame:
    first = text.split("\n", 1)[0]
    has_header = first.lower().startswith("agg_trade_id")
    names = ["agg_trade_id", "price", "quantity", "first_trade_id", "last_trade_id", "transact_time", "is_buyer_maker"]
    df = pd.read_csv(io.StringIO(text), header=0 if has_header else None, names=None if has_header else names,
                     usecols=[1, 2, 5, 6], dtype={1: np.float64, 2: np.float64})
    df.columns = ["price", "quantity", "transact_time", "is_buyer_maker"]
    tt = pd.to_numeric(df["transact_time"], errors="coerce")
    df = df[tt.notna()].copy()
    tt = tt[tt.notna()]
    df["transact_time"] = tt.where(tt <= 2_000_000_000_000, tt // 1000).astype(np.int64)
    ibm = df["is_buyer_maker"]
    if ibm.dtype != bool:
        df["is_buyer_maker"] = ibm.astype(str).str.strip().str.lower().isin(("true", "1", "t"))
    df["price"] = df["price"].astype(np.float64)
    df["quantity"] = df["quantity"].astype(np.float64)
    return df.sort_values("transact_time", kind="stable").reset_index(drop=True)


class TickFootprintFetcher:
    def __init__(self, cache_dir: str = "./data_cache", max_workers: int = 8, http: Optional[HttpClient] = None,
                 log: Callable[[str], None] = print) -> None:
        self.cache_dir = os.path.abspath(cache_dir)
        self.fp_dir = os.path.join(self.cache_dir, "footprint_15m")
        self.max_workers = max(1, max_workers)
        self.http = http or HttpClient(timeout=120.0)
        self.log = log
        os.makedirs(self.fp_dir, exist_ok=True)

    def _process_day(self, symbol: str, ymd: str) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        summary_path = os.path.join(self.fp_dir, f"{symbol}-footprint-15m-{ymd}.parquet")
        ladder_path = os.path.join(self.fp_dir, f"{symbol}-ladder-15m-{ymd}.parquet")
        if os.path.exists(summary_path) and os.path.exists(ladder_path):
            try:
                lad = pd.read_parquet(ladder_path)
                if "rung_source" in lad.columns:
                    return pd.read_parquet(summary_path), lad
            except Exception:
                pass
        data = self.http.get_optional(f"{VISION}/{symbol}/{symbol}-aggTrades-{ymd}.zip")
        if data is None:
            return None, None
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            text = zf.read(zf.namelist()[0]).decode("utf-8")
        trades = parse_aggtrades_csv(text)
        if trades.empty:
            return None, None
        bin_step = float(nice_bin_step(np.array([trades["price"].iloc[0]]))[0])   # causal: first print of the day
        summary, ladder = build_ladder_from_trades(trades, bin_step)
        for path, frame in ((summary_path, summary), (ladder_path, ladder)):
            tmp = path + ".tmp"
            frame.to_parquet(tmp, index=False)
            os.replace(tmp, path)
        return summary, ladder

    def fetch_footprint(self, symbol: str, start_date: str, end_date: Optional[str] = None,
                        now: Optional[datetime] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
        now = now or datetime.now(timezone.utc)
        start = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end = (datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc) if end_date
               else now.replace(hour=0, minute=0, second=0, microsecond=0))
        days: List[str] = []
        d = start
        while d < end:
            days.append(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)
        self.log(f"[FOOTPRINT] {symbol}: aggTrades for {len(days)} day(s) from {start_date}")
        summaries, ladders = [], []
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futs = {pool.submit(self._process_day, symbol, day): day for day in days}
            done = 0
            for fut in as_completed(futs):
                day = futs[fut]
                try:
                    s, l = fut.result()
                except FetchError as exc:
                    self.log(f"  [ERROR] aggTrades {symbol} {day}: {exc}")
                    s, l = None, None
                except Exception as exc:
                    self.log(f"  [WARN] aggTrades {symbol} {day}: {exc!r}")
                    s, l = None, None
                if s is not None and not s.empty:
                    summaries.append(s)
                if l is not None and not l.empty:
                    ladders.append(l)
                done += 1
                if done % 30 == 0 or done == len(days):
                    self.log(f"  [FOOTPRINT] {symbol}: {done}/{len(days)} days")
        if not summaries:
            return pd.DataFrame(columns=SUMMARY_COLS), pd.DataFrame(columns=LADDER_COLUMNS)
        summary = (pd.concat(summaries, ignore_index=True).drop_duplicates("open_time_ms")
                     .sort_values("open_time_ms").reset_index(drop=True))
        ladder = (pd.concat(ladders, ignore_index=True).drop_duplicates(["open_time_ms", "price_bin"])
                    .sort_values(["open_time_ms", "price_bin"]).reset_index(drop=True))
        self.log(f"[FOOTPRINT] {symbol}: {len(summary):,} tick-exact bars, {len(ladder):,} rungs")
        return summary, ladder
