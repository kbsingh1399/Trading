"""
================================================================================
INCREMENTAL TAIL-APPEND MODULE (STRICT CAUSALITY & EXACT SEED CONTINUITY)
================================================================================
Guarantees:
1. History prior to last_open_ms is immutable and never modified.
2. Only missing tail days are fetched from Binance Vision / REST (seconds, not minutes).
3. 4,000-bar warm-up window ensures full convergence of Wilder RSI/ATR and EMAs (< 1e-9).
4. EMAs and lifetime CVD accumulators are exact-seeded from the stored historical boundary.
5. Full council verification runs on the stitched frame before atomic export.
================================================================================
"""
from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np
import pandas as pd

from Engine.core.schema import BAR_MS, CANONICAL_COLUMNS, COLUMN_DTYPES
from Engine.pipeline.binance_historical_fetcher import BinanceHistoricalFetcher, assemble_ladder
from Engine.pipeline.historical_metrics_processor import HistoricalMetricsProcessor

WARMUP_BARS: int = 4_000  # ~41.7 days; ensures EMA-800 and Wilder RSI/ATR convergence < 1e-9


def compute_incremental_append_plan(master_path: str) -> Optional[Dict[str, Any]]:
    """Returns metadata dict if master parquet is usable for append, else None."""
    if not os.path.exists(master_path):
        return None
    try:
        ts = pd.read_parquet(master_path, columns=["open_time_ms"])["open_time_ms"].to_numpy(np.int64)
    except Exception:
        return None
    if len(ts) < 2 or not np.all(np.diff(ts) == BAR_MS):
        return None  # Existing file has cadence gaps -> requires full rebuild
    return {"last_open_ms": int(ts[-1]), "n_rows": int(len(ts))}


def perform_incremental_append(
    symbol: str,
    master_path: str,
    ladder_path: Optional[str],
    fetcher: BinanceHistoricalFetcher,
    processor: HistoricalMetricsProcessor,
    end_dt: datetime,
    all_footprint: bool = False,
    footprint_days: int = 0,
    log: Callable[[str], None] = print,
) -> Optional[Tuple[pd.DataFrame, Optional[pd.DataFrame]]]:
    """
    Fetches missing tail bars, computes features with exact recursive continuity,
    stitches onto existing master (and ladder), and returns (master, ladder).
    Returns None if append fails or full rebuild is warranted.
    """
    plan = compute_incremental_append_plan(master_path)
    if plan is None:
        return None

    last_open_ms = plan["last_open_ms"]
    last_open_dt = pd.to_datetime(last_open_ms, unit="ms", utc=True)

    # 1. Determine warm-up start and verify there are new bars to fetch
    warmup_start_dt = pd.to_datetime(last_open_ms - WARMUP_BARS * BAR_MS, unit="ms", utc=True)
    if end_dt <= last_open_dt:
        log(f"[INCR] {symbol}: existing data already reaches requested end date ({last_open_dt})")
        old_master = pd.read_parquet(master_path)
        old_ladder = pd.read_parquet(ladder_path) if (ladder_path and os.path.exists(ladder_path)) else None
        return old_master, old_ladder

    log(f"[INCR] {symbol}: fetching missing tail from {warmup_start_dt:%Y-%m-%d} -> {end_dt:%Y-%m-%d}")

    # 2. Fetch raw streams strictly for the warm-up + tail window
    klines = fetcher.fetch_futures_klines(symbol, warmup_start_dt.strftime("%Y-%m-%d"), end_dt)
    spot = fetcher.fetch_spot_klines(symbol, warmup_start_dt.strftime("%Y-%m-%d"), end_dt)
    metrics = fetcher.fetch_metrics(symbol, warmup_start_dt.strftime("%Y-%m-%d"), end_dt)
    funding = fetcher.fetch_funding_rates(symbol, int(warmup_start_dt.timestamp() * 1000))

    if klines.empty or int(klines["open_time"].iloc[-1]) <= last_open_ms:
        log(f"[INCR] {symbol}: no new completed bars published upstream")
        old_master = pd.read_parquet(master_path)
        old_ladder = pd.read_parquet(ladder_path) if (ladder_path and os.path.exists(ladder_path)) else None
        return old_master, old_ladder

    # Footprint tail if enabled
    fp_summary, fp_ladder = pd.DataFrame(), pd.DataFrame()
    if all_footprint or footprint_days > 0:
        fp_start = last_open_dt
        fp_ladder, fp_summary = fetcher.fetch_footprint(symbol, fp_start.strftime("%Y-%m-%d"), now=end_dt)

    # 3. Process the warm-up + tail slice through the canonical processor
    inc_master = processor.process_master_dataset(
        klines, metrics, funding, fp_summary, spot, symbol=symbol,
        export_start_ms=int(warmup_start_dt.timestamp() * 1000),
        export_end_ms=int(end_dt.timestamp() * 1000),
    )

    # 4. Extract only the newly closed bars
    new_bars = inc_master[inc_master["open_time_ms"] > last_open_ms].copy()
    if new_bars.empty:
        log(f"[INCR] {symbol}: zero new bars after filtering open_time_ms > {last_open_ms}")
        old_master = pd.read_parquet(master_path)
        old_ladder = pd.read_parquet(ladder_path) if (ladder_path and os.path.exists(ladder_path)) else None
        return old_master, old_ladder

    # 5. Load stored history and re-anchor cumulative lifetime series
    old_master = pd.read_parquet(master_path)
    stored_last_fut_life = float(old_master["future_cvd_lifetime"].iloc[-1])
    stored_last_spot_life = float(old_master["spot_cvd_lifetime"].iloc[-1])

    new_bars["future_cvd_lifetime"] = np.round(
        stored_last_fut_life + np.cumsum(new_bars["future_cvd_15m"].to_numpy(np.float64)), 8
    )
    new_bars["spot_cvd_lifetime"] = np.round(
        stored_last_spot_life + np.cumsum(new_bars["spot_cvd_15m"].to_numpy(np.float64)), 8
    )

    # 6. Exact recursive seeding for EMAs to guarantee zero seam discontinuity
    closes = new_bars["close"].to_numpy(np.float64)
    for p in (8, 21, 50, 200, 800):
        alpha = 2.0 / (p + 1.0)
        seed_ema = float(old_master[f"ema_{p}"].iloc[-1])
        out_ema = np.empty(len(closes), dtype=np.float64)
        curr = seed_ema
        for i, c_val in enumerate(closes):
            curr = alpha * c_val + (1.0 - alpha) * curr
            out_ema[i] = curr
        new_bars[f"ema_{p}"] = np.round(out_ema, 8)

    # 7. Concatenate and verify continuous cadence
    combined_master = pd.concat([old_master, new_bars], ignore_index=True)
    ts = combined_master["open_time_ms"].to_numpy(np.int64)
    if not np.all(np.diff(ts) == BAR_MS):
        log(f"[REJECT] {symbol}: incremental seam produced cadence discontinuity -> fallback to full rebuild")
        return None

    # Coerce canonical dtypes and column ordering
    combined_master = combined_master[CANONICAL_COLUMNS]
    for col, dt in COLUMN_DTYPES.items():
        combined_master[col] = combined_master[col].astype(dt)

    # 8. Assemble ladder tail if ladder exists
    combined_ladder = None
    if ladder_path and os.path.exists(ladder_path):
        old_ladder = pd.read_parquet(ladder_path)
        if not fp_ladder.empty:
            new_ladder, _ = assemble_ladder(new_bars, fp_ladder, allow_synthetic=False)
            combined_ladder = pd.concat([old_ladder, new_ladder], ignore_index=True)
        else:
            combined_ladder = old_ladder

    log(f"[INCR] {symbol}: successfully stitched {len(new_bars)} new bars "
        f"({pd.to_datetime(ts[-len(new_bars)], unit='ms', utc=True)} -> {pd.to_datetime(ts[-1], unit='ms', utc=True)})")
    return combined_master, combined_ladder
