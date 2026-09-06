"""
================================================================================
REAL TICK FOOTPRINT ENGINE (100% EMPIRICAL AGGTRADES -> TABLE 2 FOOTPRINT LADDER)
================================================================================
Author: Quant Architecture Team
Standards: Andrej Karpathy Directives, Clean Code, Zero Synthetic Lookahead

Core Architecture:
1. Zero-Disk In-Memory Streaming:
   Downloads daily compressed aggTrades (.zip) from data.binance.vision directly
   into io.BytesIO in RAM. Extracts and parses CSV in memory with immediate
   buffer deallocation. Zero raw .zip or .csv files touch the local filesystem.

2. Fixed Institutional Merge Levels:
   Discretizes trade executions using deterministic, invariant price steps
   defined in schema.py (e.g. $25.00 BTC, $1.00 ETH) matching Exocharts and
   Sierra Chart standards. Prevents non-stationary dynamic bin distortion.

3. Complete Microstructure Metrics (13-Column Table 2):
   Computes exact taker bid/ask volume, net delta, total volume, trade counts,
   Point of Control (POC), 3:1 diagonal imbalances with dynamic notional floor,
   stacked imbalance clusters (>= 3 rungs), and 70% Value Area (VAH/VAL).

4. Edge Case Hardening:
   - Single-rung candle guard (High - Low < step in low-vol regimes): POC=1, imb=0.
   - Resumable monthly chunk caching: saves intermediate {symbol}-footprint-{YYYY-MM}.parquet
     to survive network drops across 2,000-day downloads without re-fetching.
   - Zero-synthetic fallback: if a day is 404 or unlisted, NO rungs are fabricated.
================================================================================
"""

from __future__ import annotations

import io
import os
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from ..core.schema import (
    BAR_MS,
    FIXED_MERGE_STEPS,
    LADDER_COLUMNS,
    LADDER_DTYPES,
)
from .http_client import FetchError, HttpClient

VISION_BASE_URL = "https://data.binance.vision/data/futures/um/daily/aggTrades"
IMBALANCE_RATIO = 3.0
STACK_MIN_RUN = 3
VALUE_AREA_PCT = 0.70

FOOTPRINT_SUMMARY_COLUMNS = [
    "open_time_ms",
    "fp_delta",
    "fp_poc_price",
    "fp_poc_vol_ratio",
    "fp_stacked_buy_imb",
    "fp_stacked_sell_imb",
    "fp_max_single_trade",
]


class RealFootprintEngine:
    """
    Production-grade order flow engine for downloading and processing 100% real
    tick footprint data from Binance Public Vision.
    """

    def __init__(
        self,
        cache_dir: str,
        max_workers: int = 4,
        http: Optional[HttpClient] = None,
        log: Optional[Callable[[str], None]] = None,
    ):
        self.cache_dir = cache_dir
        self.footprint_cache_dir = os.path.join(cache_dir, "footprint_monthly")
        os.makedirs(self.footprint_cache_dir, exist_ok=True)
        self.max_workers = max(1, max_workers)
        self.http = http or HttpClient()
        self.log = log or (lambda msg: None)

    def get_merge_step(self, symbol: str) -> float:
        """Retrieves the fixed institutional merge step for the given asset."""
        if symbol in FIXED_MERGE_STEPS:
            return float(FIXED_MERGE_STEPS[symbol])
        # Fallback conservative rule for unindexed assets (10 bps)
        return 0.01

    def fetch_and_process_month(
        self,
        symbol: str,
        year: int,
        month: int,
        start_dt: datetime,
        end_dt: datetime,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Processes a single calendar month of aggTrades.
        Checks local monthly parquet cache first; if absent, downloads all valid days in RAM,
        processes rungs, saves monthly cache, and returns (ladder_df, summary_df).
        """
        month_str = f"{year:04d}-{month:02d}"
        cache_ladder_path = os.path.join(self.footprint_cache_dir, f"{symbol}_ladder_{month_str}.parquet")
        cache_summary_path = os.path.join(self.footprint_cache_dir, f"{symbol}_summary_{month_str}.parquet")

        # Fast-skip if monthly chunk is already processed
        if os.path.exists(cache_ladder_path) and os.path.exists(cache_summary_path):
            try:
                ladder_df = pd.read_parquet(cache_ladder_path)
                summary_df = pd.read_parquet(cache_summary_path)
                return ladder_df, summary_df
            except Exception as e:
                self.log(f"  [FOOTPRINT] corrupted monthly cache {month_str} ({e}); re-processing")

        # Determine daily date range for this month
        first_day = datetime(year, month, 1, tzinfo=timezone.utc)
        if month == 12:
            next_month = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            next_month = datetime(year, month + 1, 1, tzinfo=timezone.utc)

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

        # Download and process days in parallel (bounded worker pool to prevent RAM spike)
        def _fetch_day(d_str: str) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
            trades = self._download_day_trades_in_memory(symbol, d_str)
            if trades is None or trades.empty:
                return None
            return self._aggregate_trades_to_ladder(trades, merge_step)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
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

        if not daily_ladders:
            empty_ladder = pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)
            empty_summary = pd.DataFrame(columns=FOOTPRINT_SUMMARY_COLUMNS)
            return empty_ladder, empty_summary

        month_ladder = pd.concat(daily_ladders, ignore_index=True).sort_values(["open_time_ms", "price_bin"]).reset_index(drop=True)
        month_summary = pd.concat(daily_summaries, ignore_index=True).sort_values("open_time_ms").reset_index(drop=True)

        # Cache monthly chunk to ensure resumability
        try:
            month_ladder.to_parquet(cache_ladder_path, compression="zstd", index=False)
            month_summary.to_parquet(cache_summary_path, compression="zstd", index=False)
        except Exception as e:
            self.log(f"  [FOOTPRINT] failed to write monthly cache for {month_str}: {e}")

        return month_ladder, month_summary

    def _download_day_trades_in_memory(self, symbol: str, date_str: str) -> Optional[pd.DataFrame]:
        """
        Streams daily aggTrades zip from Binance Vision directly into RAM via BytesIO.
        Returns parsed trades DataFrame: ['transact_time', 'price', 'quantity', 'is_buyer_maker'].
        Zero files written to disk.
        """
        url = f"{VISION_BASE_URL}/{symbol}/{symbol}-aggTrades-{date_str}.zip"
        try:
            resp = self.http.get(url, timeout=30.0)
            if resp.status_code == 404:
                # Expected when dates precede asset futures listing
                return None
            if resp.status_code != 200 or not resp.content:
                return None

            with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
                csv_names = [name for name in zf.namelist() if name.endswith(".csv")]
                if not csv_names:
                    return None
                with zf.open(csv_names[0]) as csv_file:
                    # Binance aggTrades CSV format:
                    # agg_trade_id, price, quantity, first_trade_id, last_trade_id, transact_time, is_buyer_maker
                    # Some files have a header row, others do not.
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

        except FetchError:
            return None
        except Exception as e:
            self.log(f"  [FOOTPRINT] error streaming aggTrades for {symbol} {date_str}: {e}")
            return None

    def _aggregate_trades_to_ladder(
        self,
        trades: pd.DataFrame,
        merge_step: float,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Vectorized grouping and order flow feature calculation.
        Enforces:
        - Fixed price binning: P_bin = round(p / step) * step
        - Single-rung guard for tight consolidation candles
        - 3:1 diagonal imbalances with dynamic notional floor
        - Stacked imbalance clusters (>= 3 rungs)
        - 70% Value Area around POC
        """
        if trades.empty:
            return pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES), pd.DataFrame(columns=FOOTPRINT_SUMMARY_COLUMNS)

        t_time = trades["transact_time"].to_numpy(np.int64)
        price = trades["price"].to_numpy(np.float64)
        qty = trades["quantity"].to_numpy(np.float64)
        sell_flag = trades["is_buyer_maker"].to_numpy(bool)

        # 15-minute bar bucketing
        bar_ts = (t_time // BAR_MS) * BAR_MS
        # Fixed institutional price rung binning
        bin_idx = np.round(price / merge_step).astype(np.int64)

        t = pd.DataFrame({
            "open_time_ms": bar_ts,
            "bin_idx": bin_idx,
            "qty": qty,
            "sell_qty": np.where(sell_flag, qty, 0.0),
            "buy_qty": np.where(~sell_flag, qty, 0.0),
        })

        # Group by (bar, price_bin)
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

        # Bar-level aggregates
        bar_agg = (
            t.groupby("open_time_ms", sort=True)
            .agg(
                total_bar_vol=("qty", "sum"),
                max_single_trade=("qty", "max"),
                total_net_delta=("buy_qty", "sum"),
                taker_sell_tot=("sell_qty", "sum"),
            )
            .reset_index()
        )
        bar_agg["total_net_delta"] -= bar_agg["taker_sell_tot"]
        bar_agg = bar_agg.drop(columns=["taker_sell_tot"])

        # Determine Point of Control (POC): max volume rung in each 15m candle
        order = ladder.sort_values(["open_time_ms", "total_vol_coin", "bin_idx"], ascending=[True, False, True])
        poc_rungs = order.drop_duplicates("open_time_ms")[["open_time_ms", "bin_idx", "total_vol_coin", "price_bin"]].rename(
            columns={"bin_idx": "poc_bin_idx", "total_vol_coin": "poc_vol", "price_bin": "poc_price"}
        )

        # Merge bar volume and POC metadata into ladder
        ladder = ladder.merge(bar_agg[["open_time_ms", "total_bar_vol"]], on="open_time_ms", how="left")
        ladder = ladder.merge(poc_rungs[["open_time_ms", "poc_bin_idx"]], on="open_time_ms", how="left")
        ladder["is_poc"] = (ladder["bin_idx"] == ladder["poc_bin_idx"]).astype(np.int8)

        # ----------------------------------------------------------------------
        # Diagonal Imbalances & Value Area
        # ----------------------------------------------------------------------
        ladder = ladder.sort_values(["open_time_ms", "bin_idx"]).reset_index(drop=True)
        g = ladder.groupby("open_time_ms", sort=False)

        diff_below = g["bin_idx"].diff(1)
        diff_above = -g["bin_idx"].diff(-1)
        bid_below = g["bid_vol_coin"].shift(1).where(diff_below == 1, 0.0).fillna(0.0)
        ask_above = g["ask_vol_coin"].shift(-1).where(diff_above == 1, 0.0).fillna(0.0)

        # Dynamic notional floor: max(0.5% candle volume, $50 / price)
        p_rung = ladder["price_bin"].to_numpy(np.float64)
        notional_floor = np.maximum(
            ladder["total_bar_vol"].to_numpy(np.float64) * 0.005,
            50.0 / np.maximum(p_rung, 1e-9),
        )

        # Buy imbalance: ask_vol(P) >= 3 * bid_vol(P - 1) and ask_vol >= floor
        ask_vol = ladder["ask_vol_coin"].to_numpy(np.float64)
        bid_vol = ladder["bid_vol_coin"].to_numpy(np.float64)

        buy_imb = (
            (ask_vol >= IMBALANCE_RATIO * np.maximum(bid_below.to_numpy(), 1e-9))
            & (ask_vol >= notional_floor)
            & (diff_below.to_numpy() == 1)
        )
        # Sell imbalance: bid_vol(P) >= 3 * ask_vol(P + 1) and bid_vol >= floor
        sell_imb = (
            (bid_vol >= IMBALANCE_RATIO * np.maximum(ask_above.to_numpy(), 1e-9))
            & (bid_vol >= notional_floor)
            & (diff_above.to_numpy() == 1)
        )

        ladder["is_buy_imbalance"] = buy_imb.astype(np.int8)
        ladder["is_sell_imbalance"] = sell_imb.astype(np.int8)

        # Single-rung candle guard (Sonnet Suggestion 1):
        # If a candle has only 1 rung, imbalances are strictly 0 and POC is 1.
        rung_counts = g["bin_idx"].transform("size").to_numpy()
        single_rung_mask = rung_counts < 2
        if single_rung_mask.any():
            ladder.loc[single_rung_mask, "is_poc"] = 1
            ladder.loc[single_rung_mask, "is_buy_imbalance"] = 0
            ladder.loc[single_rung_mask, "is_sell_imbalance"] = 0

        # Stacked Imbalances: >= 3 contiguous rungs with imbalances
        ladder["is_stacked_buy_imb"] = self._compute_stacked_imbalances(ladder["is_buy_imbalance"].to_numpy(np.int8), ladder["bin_idx"].to_numpy(np.int64), ladder["open_time_ms"].to_numpy(np.int64))
        ladder["is_stacked_sell_imb"] = self._compute_stacked_imbalances(ladder["is_sell_imbalance"].to_numpy(np.int8), ladder["bin_idx"].to_numpy(np.int64), ladder["open_time_ms"].to_numpy(np.int64))

        # 70% Value Area calculation per 15m candle
        ladder["is_value_area"] = self._compute_value_area(ladder)

        # Final Table 2 formatting
        final_ladder = ladder[LADDER_COLUMNS].copy()

        # Build Bar-Level Summary DataFrame for Table 1 enrichment
        stacked_buy_counts = ladder.groupby("open_time_ms")["is_stacked_buy_imb"].max().reset_index().rename(columns={"is_stacked_buy_imb": "fp_stacked_buy_imb"})
        stacked_sell_counts = ladder.groupby("open_time_ms")["is_stacked_sell_imb"].max().reset_index().rename(columns={"is_stacked_sell_imb": "fp_stacked_sell_imb"})

        summary = bar_agg.merge(poc_rungs[["open_time_ms", "poc_price", "poc_vol"]], on="open_time_ms", how="left")
        summary["fp_poc_vol_ratio"] = summary["poc_vol"] / np.maximum(summary["total_bar_vol"], 1e-12)
        summary = summary.merge(stacked_buy_counts, on="open_time_ms", how="left")
        summary = summary.merge(stacked_sell_counts, on="open_time_ms", how="left")
        summary = summary.rename(columns={
            "total_net_delta": "fp_delta",
            "poc_price": "fp_poc_price",
            "max_single_trade": "fp_max_single_trade",
        })

        final_summary = summary[FOOTPRINT_SUMMARY_COLUMNS].copy()
        return final_ladder, final_summary

    def _compute_stacked_imbalances(self, flag: np.ndarray, bin_idx: np.ndarray, bar_ts: np.ndarray) -> np.ndarray:
        """Vectorized detection of >= STACK_MIN_RUN contiguous rungs with active imbalances."""
        n = flag.size
        out = np.zeros(n, dtype=np.int8)
        if n < STACK_MIN_RUN:
            return out

        same_bar = np.empty(n, dtype=bool)
        same_bar[0] = False
        same_bar[1:] = bar_ts[1:] == bar_ts[:-1]

        contiguous = np.empty(n, dtype=bool)
        contiguous[0] = False
        contiguous[1:] = (bin_idx[1:] - bin_idx[:-1]) == 1

        active = flag == 1
        valid_step = active & same_bar & contiguous

        # Find contiguous clusters
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

    def _compute_value_area(self, ladder: pd.DataFrame) -> np.ndarray:
        """
        Computes the 70% Value Area (VAH to VAL) centered on POC for each 15m candle.
        Rungs accumulating 70% of total candle volume receive is_value_area = 1.
        """
        n = len(ladder)
        out = np.zeros(n, dtype=np.int8)
        # Iterate per candle for exact dual-side expansion standard (Market Profile)
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

    def fetch_footprint(
        self,
        symbol: str,
        start_date_str: str,
        end_date_str: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Main entrypoint for fetching and assembling the multi-month footprint ladder.
        Streams month-by-month, checking local monthly parquet chunks.
        Returns:
            (consolidated_ladder_df, consolidated_summary_df)
        """
        now = now or datetime.now(timezone.utc)
        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc) if end_date_str else now

        # Generate list of (year, month) pairs
        curr = datetime(start_dt.year, start_dt.month, 1, tzinfo=timezone.utc)
        months_to_process: List[Tuple[int, int]] = []
        while curr <= end_dt:
            months_to_process.append((curr.year, curr.month))
            if curr.month == 12:
                curr = datetime(curr.year + 1, 1, 1, tzinfo=timezone.utc)
            else:
                curr = datetime(curr.year, curr.month + 1, 1, tzinfo=timezone.utc)

        self.log(f"[FOOTPRINT] {symbol}: fetching real tick aggTrades across {len(months_to_process)} months "
                 f"({start_dt:%Y-%m-%d} -> {end_dt:%Y-%m-%d}) | step=${self.get_merge_step(symbol)}")

        ladder_chunks: List[pd.DataFrame] = []
        summary_chunks: List[pd.DataFrame] = []

        for y, m in months_to_process:
            t0 = time.time()
            m_ladder, m_summary = self.fetch_and_process_month(symbol, y, m, start_dt, end_dt)
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
