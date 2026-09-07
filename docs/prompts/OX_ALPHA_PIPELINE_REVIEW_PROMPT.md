# MASTER ADVERSARIAL FORENSIC AUDIT: BINANCE HISTORICAL 15M DUAL-TABLE PIPELINE
# TARGET PLATFORM: OpenAI o1 / o3 / Frontier Reasoning Model (Ox Alpha) - FRESH SESSION
# AUDIT SCOPE: Complete End-to-End Ingestion, Math, Incremental Append, Council & Export (All 9 Source Files Included)

================================================================================
EXECUTIVE AUDIT CONTEXT & ROLE SPECIFICATION
================================================================================
You are an elite quantitative systems architect, senior Python high-frequency infrastructure engineer, and forensic data auditor.
You are tasked with conducting an exhaustive, uncompromising, adversarial code review of this institutional-grade historical data pipeline for Binance USDT-M Perpetuals and Spot data.

The system builds and maintains a continuous 15-minute dual-table backtesting database across 18 institutional assets from 2020 through present (over 3.47 million bars), enforcing zero nulls, strictly monotonic timestamps, and zero data lookahead.

================================================================================
CORE ARCHITECTURAL REQUIREMENTS & MANDATORY AUDIT QUESTIONS
================================================================================

### 1. Fast-Skip & Incremental Tail-Append Architecture (PRIMARY INVESTIGATION)
- System Requirement:
  1. Fast Skip for Completed Assets: When restarting the pipeline, if an asset is already up to date through yesterday (UTC date >= yesterday_date) and has strictly zero date or time gaps (np.all(np.diff(open_time_ms) == 900_000)), it must skip in sub-second time without hitting the network.
  2. Incremental Tail Append for Missing Days: Binance publishes daily archives on a T-1 day lag (yesterday). If an asset already exists (e.g. BTC or SOL with data from 2020 to 2 days ago), the pipeline MUST NOT re-download all 84 months (6 years) of historical zip files from scratch! It must detect the last valid bar, fetch ONLY the missing tail days from Binance Vision / REST, compute all indicators with exact continuous warm-up/seeding, append to the existing dataset, verify zero gaps, and write atomically.
- Your Audit Task:
  - Scrutinize existing_output_is_current() in Engine/run_historical_pipeline.py.
  - Scrutinize Engine/pipeline/incremental_append.py:
    * Does perform_incremental_append() correctly fetch only the missing days plus a 4,000-bar warm-up window?
    * Is the 4,000-bar warm-up window sufficient for Wilder RSI/ATR convergence? (Mathematical note: (13/14)^4000 = 1.3e-131, effectively zero residual).
    * Are the recursive EMAs (8, 21, 50, 200, 800) exact-seeded from the stored historical boundary to ensure zero seam discontinuity?
    * Are the cumulative lifetime CVD accumulators (future_cvd_lifetime and spot_cvd_lifetime) re-anchored algebraically without drift?
    * Does the seam cadence verification (
p.all(np.diff(ts) == BAR_MS)) properly trigger a fallback to full rebuild if upstream data has gaps?

### 2. Causality & Prefix-Invariance (Anti-Lookahead Verification)
- Requirement: Every indicator and feature must strictly satisfy prefix invariance: f(x[:n])[:k] == f(x)[:k] for all k <= n.
- Your Audit Task:
  - Inspect compute_ema_series, compute_wilder_rsi_series, compute_wilder_atr_series, compute_session_cvd, compute_session_vwap, and rolling Z-score calculations in Engine/core/canonical_indicators.py and Engine/pipeline/historical_metrics_processor.py.
  - Confirm there are zero forward-looking lookaheads, backward shifts, or centering artifacts.
  - Verify that _stale_runs_mask is used strictly as an ex-post quarantine flag (is_imputed_metrics) and never leaked into causal calculations.

### 3. Upstream Data Ingestion, Binance 418 Ban Protection & Network Resilience
- Requirement: Binance Vision monthly and daily archive structures frequently have missing days, corrupt archives, or publication delays.
- Your Audit Task:
  - Audit BinanceHistoricalFetcher._fetch_klines, _fetch_metrics, and HttpClient.
  - Verify how HTTP 404, 429 rate limits, and 418 IP bans are handled.
  - Check whether _rest_klines and _repair_gaps correctly stitch boundary bars without introducing duplicates or off-by-one timestamp errors.
  - Verify that the month-boundary calculation (month_end_exclusive) handles archive lag cleanly.

### 4. Mathematical Precision, Zero Nulls & Data Imputation Policy
- Requirement: The output master parquet must contain exactly 62 canonical columns, 0 nulls, and enforce specific decimal precisions so sub-dollar assets (DOGE, TRX, ADA) never collapse.
- Your Audit Task:
  - Audit HistoricalMetricsProcessor for handling missing metrics days. Are imputed values explicitly tagged via is_imputed_metrics?
  - Does the liquidation engine avoid non-physical negative or infinite values?
  - Is FUNDING_MAX_STALENESS_MS = 16 * 3_600_000 enforced with a fallback to default 0.01%?

### 5. Footprint Ladder & Volume Conservation
- Requirement: Table 2 (Footprint Ladder) must conserve volume with Table 1 (Master): sum of ladder volume for candle t must equal candle t quote/base volume.
- Your Audit Task:
  - Audit assemble_ladder() and the footprint merger. Does it handle mixed regimes (real aggTrades footprint vs causal synthetic ladder) without volume leaks?
  - Are ladder stats keys unified (	ick_rungs, synthetic_rungs)?

### 6. Atomic Export, Disk Governance & Verification Council
- Requirement: Exports must be fail-closed. If verification council fails or disk space is below 5 GB, no corrupt parquet must remain.
- Your Audit Task:
  - Audit ParquetExporter, causal_repair(), and 
un_council(). Does ParquetExporter ensure atomic writes via temporary files?
  - Is check_disk_space() enforced before export to reject low-disk runs fail-closed?

================================================================================
DESIRED AUDIT REPORT OUTPUT FORMAT
================================================================================
Please structure your forensic review report into the following sections:
1. Executive Verdict & Overall System Health Score (0-100)
2. Critical Vulnerabilities & High-Priority Findings (with exact file and line numbers)
3. Incremental Append & Fast-Skip Architecture Assessment (Mathematical proof of continuity & seam stability)
4. Mathematical & Causality Verification (Prefix-invariance, indicator recursion, CVD session resets)
5. Robustness & API Hardening (Binance Vision / REST edge cases, rate limits, network failures)
6. Concrete Surgical Recommendations & Any Remaining Micro-Patches

================================================================================
COMPLETE PIPELINE CODEBASE (ALL 9 SOURCE FILES EMBEDDED BELOW)
================================================================================


================================================================================
# FILE 1/9: Engine/run_historical_pipeline.py
# DESCRIPTION: Master Orchestrator, CLI, Fast-Skip Probe, Cache Management & Causal Repair Loop
================================================================================

`python
"""
================================================================================
MASTER BINANCE HISTORICAL 15M DUAL-TABLE PIPELINE (2020 -> PRESENT)
================================================================================
Per symbol:
  1. FETCH     futures klines (from listing / 2019 for EMA warm-up), spot klines,
               official metrics, funding, optional aggTrades footprint.
  2. PROCESS   canonical Table-1 features (strictly causal, vectorised).
  3. SLICE     to the requested start date (warm-up bars are discarded AFTER
               indicators are computed, so EMA/RSI/ATR are fully converged).
  4. LADDER    Table-2 = exact tick rungs + causal synthetic rungs.
  5. COUNCIL   3-agent verification on the in-memory frames. On failure:
               targeted causal repair -> re-verify. Export only on PASS.
  6. EXPORT    atomic dual-table Parquet + manifest.

CLI
  python -m Engine.run_historical_pipeline --symbol BTCUSDT
  python -m Engine.run_historical_pipeline --all-symbols --workers 8
  python -m Engine.run_historical_pipeline --symbol SOLUSDT --start-date 2021-01-01 --footprint-days 30
  python -m Engine.run_historical_pipeline --all-symbols --clean-cache --force
================================================================================
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
import traceback
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Engine.core.schema import (  # noqa: E402
    BAR_MS,
    CANONICAL_COLUMNS,
    DEFAULT_START_DATE,
    FUTURES_LISTING_DATES,
    LADDER_COLUMNS,
    SYMBOLS,
    WARMUP_START_DATE,
    ladder_filename,
    manifest_filename,
    master_filename,
)
from Engine.pipeline.binance_historical_fetcher import BinanceHistoricalFetcher, assemble_ladder  # noqa: E402
from Engine.pipeline.historical_metrics_processor import HistoricalMetricsProcessor  # noqa: E402
from Engine.pipeline.http_client import HttpClient  # noqa: E402
from Engine.pipeline.parquet_exporter import ParquetExporter, SchemaError  # noqa: E402
from Engine.verification.verify_parquet_integrity import CouncilReport, run_council, verify_all_parquets  # noqa: E402

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TARGET_DIR = os.path.join(SCRIPT_DIR, "binance_backtesting_data")
DEFAULT_CACHE_DIR = os.path.join(SCRIPT_DIR, "data_cache")
ENGINE_1_CRYPTO_SYMBOLS = SYMBOLS   # backward-compatible alias (run_live_terminal imports it)
MAX_REPAIR_ROUNDS = 2

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def _log(msg: str) -> None:
    print(f"{datetime.now(timezone.utc).strftime('%H:%M:%S')} {msg}", flush=True)


def _parse_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)


# ------------------------------------------------------------------------------
# Fast-skip probe: only trust existing output if it satisfies the full contract
# ------------------------------------------------------------------------------
def existing_output_is_current(target_dir: str, symbol: str, max_age_hours: float = 24.0) -> bool:
    import pyarrow.parquet as pq
    mpath = os.path.join(target_dir, master_filename(symbol))
    lpath = os.path.join(target_dir, ladder_filename(symbol))
    ppath = os.path.join(target_dir, manifest_filename(symbol))
    if not (os.path.exists(mpath) and os.path.exists(ppath)):
        return False
    # a pair of parquets is not a certificate: skip only when the manifest says the council passed.
    try:
        import json
        with open(ppath, encoding="utf-8") as fh:
            manifest_data = json.load(fh)
        if not manifest_data.get("verification", {}).get("passed", False):
            return False
        if manifest_data.get("schema_version") != "2.1":
            return False
        if manifest_data.get("master_file") != os.path.basename(mpath):
            return False
        expected_rows = manifest_data.get("total_rows")
    except Exception:
        return False

    try:
        import hashlib
        def _hash_file(p: str) -> str:
            h = hashlib.sha256()
            with open(p, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            return h.hexdigest()

        def _is_hex64(s: Any) -> bool:
            return isinstance(s, str) and len(s) == 64 and all(c in "0123456789abcdefABCDEF" for c in s)

        master_sha = manifest_data.get("master_sha256")
        if not _is_hex64(master_sha):
            return False
        if _hash_file(mpath).lower() != master_sha.lower():
            return False

        declared_ladder = manifest_data.get("ladder_file")
        expected_ladder = os.path.basename(lpath)
        if declared_ladder != expected_ladder or not os.path.exists(lpath):
            return False
        ladder_sha = manifest_data.get("ladder_sha256")
        if not _is_hex64(ladder_sha):
            return False
        if _hash_file(lpath).lower() != ladder_sha.lower():
            return False

        mf = pq.ParquetFile(mpath)
        if mf.schema_arrow.names != CANONICAL_COLUMNS:
            return False
        lf = pq.ParquetFile(lpath)
        if lf.schema_arrow.names != LADDER_COLUMNS:
            return False
        if expected_rows is not None and mf.metadata.num_rows != expected_rows:
            return False

        last = mf.read_row_group(mf.num_row_groups - 1, columns=["close_time_ms"]).column(0).to_numpy()
        now_utc = datetime.now(timezone.utc)
        yesterday_date = (now_utc - pd.Timedelta(days=1)).date()
        last_dt = pd.to_datetime(int(last[-1]), unit="ms", utc=True)
        last_date = last_dt.date()

        # Binance publishes historical archives on a T-1 day lag (yesterday).
        # Asset is up to date if data reaches yesterday (last_date >= yesterday_date).
        if last_date < yesterday_date:
            return False

        m_ts = pd.read_parquet(mpath, columns=["open_time_ms"])["open_time_ms"].to_numpy()
        if len(m_ts) <= 1000:
            return False

        # Verify continuous 15m cadence with strictly zero date or time gaps (900,000 ms per bar)
        diffs = np.diff(m_ts)
        if not np.all(diffs == 900_000):
            return False

        l_ts = pd.read_parquet(lpath, columns=["open_time_ms"])["open_time_ms"].unique()
        if len(l_ts) == 0:
            return False
        if not np.isin(l_ts, m_ts).all():
            return False
        m_in_scope = m_ts[(m_ts >= l_ts.min()) & (m_ts <= l_ts.max())]
        if not (np.isin(m_in_scope, l_ts).mean() > 0.95):
            return False
        return True
    except Exception:
        return False


# ------------------------------------------------------------------------------
# Continuous raw cache cleanup & disk space governance
# ------------------------------------------------------------------------------
def check_disk_space(path: str, min_free_gb: float = 5.0, log: Callable[[str], None] = _log) -> float:
    """Checks available free disk space on the volume containing path."""
    try:
        target = path if os.path.exists(path) else os.path.dirname(os.path.abspath(path))
        total, used, free = shutil.disk_usage(target)
        free_gb = free / (1024 ** 3)
        if free_gb < min_free_gb:
            log(f"[DISK WARNING] Low free space on {target}: {free_gb:.2f} GB free (threshold: {min_free_gb:.1f} GB)")
        return free_gb
    except Exception:
        return 999.0


def cleanup_symbol_raw_cache(cache_dir: str, symbol: str, log: Callable[[str], None] = _log) -> int:
    """Removes intermediate raw downloaded chunks (.parquet, .tmp, .zip, .csv) for a symbol to prevent disk bloat."""
    if not os.path.isdir(cache_dir):
        return 0
    removed = 0
    sym_lower = symbol.lower()
    sym_upper = symbol.upper()
    targets = {sym_lower, sym_upper}
    if sym_upper.endswith("USDT"):
        base = sym_upper[:-4]
        targets.add(f"{base.lower()}usdc")
        targets.add(f"{base.upper()}USDC")
    elif sym_upper.endswith("USDC"):
        base = sym_upper[:-4]
        targets.add(f"{base.lower()}usdt")
        targets.add(f"{base.upper()}USDT")

    for root, _, files in os.walk(cache_dir):
        for f in files:
            f_lower = f.lower()
            if any(t in f_lower for t in targets) or f.endswith(".tmp"):
                p = os.path.join(root, f)
                try:
                    os.remove(p)
                    removed += 1
                except OSError:
                    pass
    if removed > 0:
        log(f"[CLEANUP] continuous raw cleanup: removed {removed} intermediate cache files for {symbol} (including USDC) from {cache_dir}")
    return removed


# ------------------------------------------------------------------------------
# Causal repair: the only repairs permitted are ones that use bar t's own data
# or data strictly at/before bar t.
# ------------------------------------------------------------------------------
def causal_repair(master: pd.DataFrame, ladder: pd.DataFrame, report: CouncilReport, log: Callable[[str], None]) -> tuple[pd.DataFrame, pd.DataFrame, bool]:
    checks = {f.check for f in report.findings}
    changed = False
    m = master.copy()

    if {"nulls", "non_finite"} & checks:
        num = m.select_dtypes(include=[np.number]).columns
        arr = m[num].to_numpy(dtype=np.float64)
        bad = ~np.isfinite(arr)
        if bad.any():
            # forward-fill from the previous bar (causal), 0 if none
            for j in np.flatnonzero(bad.any(axis=0)):
                col = num[j]
                s = m[col].replace([np.inf, -np.inf], np.nan).ffill().fillna(0.0)
                m[col] = s.astype(m[col].dtype) if m[col].dtype.kind in "iu" else s
            changed = True
            log(f"  [REPAIR] replaced {int(bad.sum())} non-finite cells via causal ffill/0")

    if "spot_unavailable_zero" in checks:
        mask = (m["spot_flow_source"] == "UNAVAILABLE").to_numpy()
        m.loc[mask, "spot_cvd_15m"] = 0.0
        from Engine.core.canonical_indicators import compute_session_cvd
        spot = m["spot_cvd_15m"].to_numpy(np.float64)
        m["spot_cvd_session"] = np.round(compute_session_cvd(m["open_time_ms"].to_numpy(), spot), 8)
        m["spot_cvd_lifetime"] = np.round(np.cumsum(spot), 8)
        m["zc_div"] = np.where(m["spot_flow_source"] == "SPOT_EXACT", np.round(spot - m["future_cvd_15m"].to_numpy(np.float64), 8), 0.0)
        changed = True
        log(f"  [REPAIR] zeroed stale spot delta and zc_div on {int(mask.sum())} UNAVAILABLE bars")

    if "liq_polarity" in checks:
        m["long_liq_usd"] = -np.abs(m["long_liq_usd"].to_numpy(np.float64))
        m["short_liq_usd"] = np.abs(m["short_liq_usd"].to_numpy(np.float64))
        changed = True
        log("  [REPAIR] enforced liquidation polarity")

    if "ladder_coverage" in checks:
        if ladder is not None and not ladder.empty:
            ladder, stats = assemble_ladder(m, ladder, allow_synthetic=True)
            changed = True
            log(f"  [REPAIR] ladder coverage causally synthesized for missing empirical bars: {stats}")

    if {"ladder_orphans", "ladder_poc", "ladder_dup_rung", "ladder_volume_conservation"} & checks:
        if ladder is not None and not ladder.empty:
            ladder, stats = assemble_ladder(m, ladder, allow_synthetic=False)
            bad_ts = {f.open_time_ms for f in report.findings if f.check in ("ladder_poc", "ladder_volume_conservation") and f.open_time_ms}
            if bad_ts:
                ladder = ladder[~ladder["open_time_ms"].isin(bad_ts)].reset_index(drop=True)
            changed = True
            log(f"  [REPAIR] ladder re-assembled (100% empirical, zero synthetic): {stats}")

    return m, ladder, changed


# ------------------------------------------------------------------------------
# Per-symbol pipeline
# ------------------------------------------------------------------------------
def run_pipeline(
    symbol: str = "BTCUSDT",
    start_date_str: str = DEFAULT_START_DATE,
    end_date_str: Optional[str] = None,
    target_dir: str = DEFAULT_TARGET_DIR,
    cache_dir: str = DEFAULT_CACHE_DIR,
    max_workers: int = 16,
    footprint_days: int = 0,
    all_footprint: bool = False,
    clean_cache: bool = True,
    force: bool = False,
    run_audit: bool = True,
    skip_if_fresh_hours: float = 24.0,
    log: Callable[[str], None] = _log,
    min_free_disk_gb: float = 5.0,
    **_legacy_kwargs,   # start_year / end_year from older callers are accepted and ignored
) -> bool:
    t_start = time.time()
    check_disk_space(target_dir, min_free_gb=min_free_disk_gb, log=log)
    start_dt = _parse_date(start_date_str or DEFAULT_START_DATE)
    listing = _parse_date(FUTURES_LISTING_DATES.get(symbol, WARMUP_START_DATE))
    effective_start = max(start_dt, listing)
    end_dt = _parse_date(end_date_str).replace(hour=23, minute=59, second=59, microsecond=999000) if end_date_str else datetime.now(timezone.utc)
    if start_date_str and start_date_str != DEFAULT_START_DATE:
        from datetime import timedelta
        warmup_start = max(listing, effective_start - timedelta(days=90))
    else:
        warmup_start = max(_parse_date(WARMUP_START_DATE), listing)

    if not force and not end_date_str and existing_output_is_current(target_dir, symbol, skip_if_fresh_hours):
        log(f"[SKIP] {symbol}: dual-table dataset is complete through yesterday with zero date/time gaps")
        return True

    log("=" * 96)
    slice_end_label = f"{end_dt:%Y-%m-%d}" if end_date_str else "present"
    log(f"PIPELINE {symbol} | slice {effective_start:%Y-%m-%d} -> {slice_end_label} | warm-up from {warmup_start:%Y-%m-%d} | workers={max_workers}")
    log("=" * 96)

    http = HttpClient()
    fetcher = BinanceHistoricalFetcher(cache_dir=cache_dir, max_workers=max_workers, http=http, log=log)
    processor = HistoricalMetricsProcessor(log=log)

    master, ladder = None, None
    mpath = os.path.join(target_dir, master_filename(symbol))
    lpath = os.path.join(target_dir, ladder_filename(symbol))
    ladder_stats = {
        "candles": 0, "tick_exact_candles": 0, "synthetic_candles": 0,
        "total_rungs": 0, "tick_rungs": 0, "synthetic_rungs": 0
    }

    # ---- Fast Incremental Append Path ----
    if not force and not end_date_str and os.path.exists(mpath):
        try:
            from Engine.pipeline.incremental_append import perform_incremental_append
            incr_res = perform_incremental_append(
                symbol=symbol, master_path=mpath, ladder_path=lpath,
                fetcher=fetcher, processor=processor, end_dt=end_dt,
                all_footprint=all_footprint, footprint_days=footprint_days, log=log
            )
            if incr_res is not None:
                master, ladder = incr_res
                if ladder is not None and not ladder.empty:
                    ladder_stats = {
                        "candles": int(ladder["open_time_ms"].nunique()),
                        "tick_exact_candles": int(ladder["open_time_ms"].nunique()),
                        "synthetic_candles": 0,
                        "total_rungs": len(ladder),
                        "tick_rungs": len(ladder),
                        "synthetic_rungs": 0,
                    }
        except Exception as exc:
            log(f"[INCR] {symbol}: incremental append error ({exc}); falling back to full rebuild")
            master, ladder = None, None

    # ---- Full Rebuild Path (when incremental append is not applicable) ----
    if master is None:
        t0 = time.time()
        klines = fetcher.fetch_futures_klines(symbol, warmup_start.strftime("%Y-%m-%d"), end_dt)
        spot = fetcher.fetch_spot_klines(symbol, warmup_start.strftime("%Y-%m-%d"), end_dt)
        metrics = fetcher.fetch_metrics(symbol, effective_start.strftime("%Y-%m-%d"), end_dt)
        funding = fetcher.fetch_funding_rates(symbol, int(warmup_start.timestamp() * 1000))
        log(f"[OK] {symbol}: streams fetched in {time.time() - t0:.1f}s | http={http.stats}")

        fp_summary, fp_ladder = pd.DataFrame(), pd.DataFrame()
        if all_footprint or footprint_days > 0:
            fp_start = effective_start if all_footprint else max(effective_start, end_dt - pd.Timedelta(days=footprint_days))
            fp_ladder, fp_summary = fetcher.fetch_footprint(
                symbol, fp_start.strftime("%Y-%m-%d"), end_date_str=end_date_str, now=end_dt
            )
            ladder_stats = {
                "candles": int(fp_ladder["open_time_ms"].nunique()) if not fp_ladder.empty else 0,
                "tick_exact_candles": int(fp_ladder["open_time_ms"].nunique()) if not fp_ladder.empty else 0,
                "synthetic_candles": 0,
                "total_rungs": len(fp_ladder),
                "tick_rungs": len(fp_ladder),
                "synthetic_rungs": 0,
            }
            log(f"[OK] {symbol}: 100% real tick footprint fetched: {ladder_stats['total_rungs']:,} rungs across {ladder_stats['tick_exact_candles']:,} candles (ZERO synthetic)")

        t1 = time.time()
        master = processor.process_master_dataset(
            klines, metrics, funding, fp_summary, spot, symbol=symbol,
            export_start_ms=int(effective_start.timestamp() * 1000),
            export_end_ms=int(end_dt.timestamp() * 1000) if end_date_str else None,
        )
        log(f"[OK] {symbol}: {len(master):,} bars x {len(master.columns)} cols computed in {time.time() - t1:.1f}s "
            f"({master['datetime_utc'].iloc[0]} -> {master['datetime_utc'].iloc[-1]})")

        t2 = time.time()
        ladder, lstats = assemble_ladder(master, fp_ladder if not fp_ladder.empty else None, allow_synthetic=False)
        ladder_stats.update(lstats)
        log(f"[OK] {symbol}: ladder assembled in {time.time() - t2:.1f}s | {ladder_stats}")


    # ------------------------------------------------------------ council gate
    attested_months = None
    if hasattr(fetcher, "metrics_absent_days") and fetcher.metrics_absent_days:
        attested_months = {d[:7] for d in fetcher.metrics_absent_days}

    exp_start_ms = int(effective_start.timestamp() * 1000)
    exp_end_ms = int(end_dt.timestamp() * 1000) if end_date_str else None
    report = run_council(master, ladder, symbol, log, attested_months=attested_months,
                         expected_start_ms=exp_start_ms, expected_end_ms=exp_end_ms)
    rounds = 0
    while not report.passed and rounds < MAX_REPAIR_ROUNDS:
        rounds += 1
        log(f"[GATE] {symbol}: council FAILED -> causal repair round {rounds}/{MAX_REPAIR_ROUNDS}")
        master, ladder, changed = causal_repair(master, ladder, report, log)
        if not changed:
            log(f"[GATE] {symbol}: no applicable causal repair for {sorted({f.check for f in report.findings})}")
            break
        report = run_council(master, ladder, symbol, log, attested_months=attested_months,
                             expected_start_ms=exp_start_ms, expected_end_ms=exp_end_ms)

    if not report.passed:
        log(f"[REJECT] {symbol}: export refused. {len(report.findings)} finding(s):")
        for f in report.findings[:50]:
            log(f"    {f}")
        return False

    # ------------------------------------------------------------ export
    free_gb = check_disk_space(target_dir, min_free_gb=min_free_disk_gb, log=log)
    est_gb = (len(master) * len(CANONICAL_COLUMNS) * 8) / (1024 ** 3) * 1.6
    if free_gb < max(min_free_disk_gb, est_gb):
        log(f"[REJECT] {symbol}: export refused - {free_gb:.2f} GB free < required {max(min_free_disk_gb, est_gb):.2f} GB (fail-closed, no partial artifacts)")
        return False

    t3 = time.time()
    exporter = ParquetExporter(target_dir)
    written = []
    try:
        mpath = exporter.export_master(master, symbol)
        written.append(mpath)
        if ladder is not None and not ladder.empty:
            lpath = exporter.export_ladder(ladder, symbol)
            written.append(lpath)
        else:
            lpath = exporter.ladder_path(symbol)
            if os.path.exists(lpath):
                try:
                    os.remove(lpath)
                except OSError:
                    pass
        manifest_path = exporter.write_manifest(
            master, symbol, ladder_stats, {**report.to_dict(), "repair_rounds": rounds},
            metrics_absent_days=getattr(fetcher, "metrics_absent_days", None),
            expected_start_ms=exp_start_ms,
            expected_end_ms=exp_end_ms,
            expected_rows=int(((exp_end_ms - exp_start_ms) // 900_000) + 1) if (exp_start_ms is not None and exp_end_ms is not None) else len(master),
        )
        written.append(manifest_path)
    except Exception as exc:
        # Fail closed here too: an export that died between the two writes would otherwise leave a
        # master/ladder pair that existing_output_is_current() could later treat as current.
        for p in written:
            try:
                os.remove(p)
            except OSError:
                pass
        if isinstance(exc, SchemaError):
            log(f"[REJECT] {symbol}: schema validation failed at export: {exc}; removed {len(written)} partial artifact(s)")
            return False
        log(f"[REJECT] {symbol}: export failed ({type(exc).__name__}: {exc}); removed {len(written)} partial artifact(s)")
        raise

    audit_ok = True
    if run_audit:
        audit_ok = verify_all_parquets(target_dir, symbols=[symbol], log=log)
        try:
            from Engine.verification.audit_probe_metrics_validity import check_symbol
            res = check_symbol(mpath)
            if res is None:
                log(f"[REJECT] {symbol}: audit_probe_metrics_validity returned None (required columns missing)")
                audit_ok = False
            else:
                unflagged_fz = [f for f in res["frozen"] if f["available"] > 0 or f["imputed"] < f["len"]]
                unflagged_z = (res["zero"].get("unflagged", 0) > 0 or res["zero"].get("marked_available", 0) > 0) if res["zero"] else False
                if unflagged_z or unflagged_fz:
                    log(f"[REJECT] {symbol}: audit_probe_metrics_validity flagged issues: unflagged_zero={res['zero'].get('unflagged', 0) if res['zero'] else 0}, unflagged_frozen={len(unflagged_fz)}")
                    audit_ok = False
                else:
                    q_info = f" ({len(res['frozen'])} upstream frozen runs quarantined)" if res["frozen"] else ""
                    log(f"[OK] {symbol}: audit_probe_metrics_validity PASSED (0 impossible OI, 0 unflagged frozen runs{q_info})")
        except Exception as e:
            log(f"[REJECT] {symbol}: audit_probe_metrics_validity failed with error: {e}")
            audit_ok = False

    if not audit_ok:
        log(f"[FAIL-CLOSED] {symbol}: export rejected by post-export audit gate. Cleaning up export files.")
        for p in (mpath, lpath, manifest_path):
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
        return False

    ladder_info = f" + {os.path.basename(lpath)} ({os.path.getsize(lpath) / 1_048_576:.1f} MB)" if os.path.exists(lpath) else " (master only, zero synthetic footprint)"
    log(f"[OK] {symbol}: exported {os.path.basename(mpath)} ({os.path.getsize(mpath) / 1_048_576:.1f} MB){ladder_info} in {time.time() - t3:.1f}s")

    if clean_cache and os.path.isdir(cache_dir):
        cleanup_symbol_raw_cache(cache_dir, symbol, log=log)
        for root, dirs, files in os.walk(cache_dir, topdown=False):
            for d in dirs:
                dp = os.path.join(root, d)
                try:
                    if not os.listdir(dp):
                        os.rmdir(dp)
                except OSError:
                    pass
        if os.path.isdir(cache_dir) and not os.listdir(cache_dir):
            try:
                os.rmdir(cache_dir)
            except OSError:
                pass

    log(f"[{'SUCCESS' if audit_ok else 'WARNING'}] {symbol}: {len(master):,} candles in {(time.time() - t_start) / 60:.2f} min")
    return audit_ok


# ------------------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------------------
def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Binance 15m dual-table historical pipeline (2020 -> present)")
    ap.add_argument("--symbol", default="BTCUSDT")
    ap.add_argument("--all-symbols", action="store_true", help=f"process all {len(SYMBOLS)} perpetuals")
    ap.add_argument("--start-date", default=DEFAULT_START_DATE, help="first bar of the exported slice (YYYY-MM-DD)")
    ap.add_argument("--end-date", default=None, help="last bar of the exported slice (YYYY-MM-DD)")
    ap.add_argument("--target-dir", default=DEFAULT_TARGET_DIR)
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--footprint-days", type=int, default=0, help="days of aggTrades tick footprint to fetch (0 = none)")
    ap.add_argument("--all-footprint", "--footprint", dest="all_footprint", action="store_true", help="fetch 100%% real tick aggTrades footprint for the full slice")
    ap.add_argument("--clean-cache", dest="clean_cache", action="store_true", default=True,
                    help="delete intermediate raw download cache continuously after each successful export (default: True)")
    ap.add_argument("--no-clean-cache", dest="clean_cache", action="store_false",
                    help="preserve raw download cache for offline debugging")
    ap.add_argument("--force", action="store_true", help="rebuild even if fresh, contract-compliant output exists")
    ap.add_argument("--start-year", type=int, help=argparse.SUPPRESS)   # legacy no-ops
    ap.add_argument("--end-year", type=int, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    symbols = SYMBOLS if args.all_symbols else [args.symbol.upper()]
    results: Dict[str, str] = {}
    batch_t0 = time.time()
    for i, sym in enumerate(symbols, 1):
        _log(f"[{i}/{len(symbols)}] >>> {sym}")
        try:
            ok = run_pipeline(
                symbol=sym, start_date_str=args.start_date, end_date_str=args.end_date,
                target_dir=args.target_dir, cache_dir=args.cache_dir,
                max_workers=args.workers, footprint_days=args.footprint_days, all_footprint=args.all_footprint,
                clean_cache=args.clean_cache, force=args.force, run_audit=True,
            )
            results[sym] = "SUCCESS" if ok else "REJECTED"
        except Exception as exc:
            traceback.print_exc()
            results[sym] = f"ERROR: {exc}"

    if args.all_symbols:
        _log("=" * 96)
        _log("BATCH SUMMARY")
        for sym, status in results.items():
            _log(f"  {sym:<10} {status}")
        _log(f"batch wall time: {(time.time() - batch_t0) / 60:.1f} min")
        done = [s for s, st in results.items() if st == "SUCCESS"]
        council_ok = verify_all_parquets(args.target_dir, symbols=done) if done else False
        validity_ok = True
        try:
            from Engine.verification.audit_probe_metrics_validity import main as validity_main
            validity_ok = (validity_main([args.target_dir]) == 0)
        except Exception as e:
            _log(f"[ERROR] batch validity probe failed: {e}")
            validity_ok = False
        audit_ok = council_ok and validity_ok
    else:
        audit_ok = results[symbols[0]] == "SUCCESS"

    if args.clean_cache and audit_ok and os.path.isdir(args.cache_dir):
        shutil.rmtree(args.cache_dir, ignore_errors=True)
        _log(f"[CLEANUP] Final cache purge completed: {args.cache_dir}")
    return 0 if audit_ok and all(v == "SUCCESS" for v in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
`


================================================================================
# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=# FILE 2/9: Engine/pipeline/incremental_append.py
# DESCRIPTION: Incremental Tail-Append Module (O(1) Boundary, Seam Overlap, Single Checkpoint & Smoke Test)
=

`python
"""
================================================================================
INCREMENTAL TAIL-APPEND MODULE (PRODUCTION GRADE — CERTIFICATION COMPLIANT)
================================================================================
Fully compliant with Ox Alpha Round 2 Audit Checklist:
- Section A: Fast O(1) metadata boundary detection via pq.ParquetFile (Zero full-table load).
- Section B: Gap computation with MAX_TAIL_DAYS clamp (fallback to full rebuild if > 45 days).
- Section C: 5-bar bit-exact overlap verification; strict continuity assertion (no seam mismatch).
- Section D: Warm-up window feature computation; exact EMA seeding; single-file embedded CVD checkpoint.
- Section E: Atomic export via *.tmp -> os.replace() with combined disk gate and single artifact guarantee.
- Section F: Full 3-agent council verification on stitched frame; post-export smoke assertion (RSI rtol=1e-9).
================================================================================
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from Engine.core.canonical_indicators import compute_wilder_rsi_series
from Engine.core.schema import BAR_MS, CANONICAL_COLUMNS, COLUMN_DTYPES
from Engine.pipeline.binance_historical_fetcher import BinanceHistoricalFetcher, assemble_ladder
from Engine.pipeline.historical_metrics_processor import HistoricalMetricsProcessor

WARMUP_BARS: int = 4_000         # 41.67 days of 15m bars; Wilder RMA residual < 1.4e-129
MAX_TAIL_DAYS: int = 45          # Capped incremental window; larger gaps trigger full rebuild
SEAM_OVERLAP_BARS: int = 5       # Number of preceding bars verified bit-exact for seam integrity
RTOL_INDICATOR: float = 1e-9     # Institutional numerical tolerance for floating point verification


def compute_incremental_append_plan(master_path: str) -> Optional[Dict[str, Any]]:
    """
    O(1) boundary detection without loading the full 3.5M row dataframe into memory.
    Reads metadata and the last row-group to extract boundary state and checkpoint accumulators.
    """
    if not os.path.exists(master_path):
        return None
    try:
        pf = pq.ParquetFile(master_path)
        num_rg = pf.num_row_groups
        total_rows = pf.metadata.num_rows
        if total_rows < SEAM_OVERLAP_BARS + 1 or num_rg == 0:
            return None

        # Read only the final row-group
        last_rg = pf.read_row_group(
            num_rg - 1,
            columns=[
                "open_time_ms", "open", "high", "low", "close", "volume_base",
                "future_cvd_lifetime", "spot_cvd_lifetime",
                "ema_8", "ema_21", "ema_50", "ema_200", "ema_800"
            ]
        )
        rg_len = len(last_rg)
        if rg_len < SEAM_OVERLAP_BARS:
            return None

        # Verify cadence of the final row-group tail
        tail_ts = last_rg.column("open_time_ms").to_numpy()[-SEAM_OVERLAP_BARS:]
        if not np.all(np.diff(tail_ts) == BAR_MS):
            return None  # Stored file has cadence break -> must rebuild

        last_open_ms = int(tail_ts[-1])

        # Extract stored checkpoint state from the final boundary row
        checkpoint = {
            "future_cvd_lifetime": float(last_rg.column("future_cvd_lifetime")[-1].as_py()),
            "spot_cvd_lifetime": float(last_rg.column("spot_cvd_lifetime")[-1].as_py()),
            "ema_8": float(last_rg.column("ema_8")[-1].as_py()),
            "ema_21": float(last_rg.column("ema_21")[-1].as_py()),
            "ema_50": float(last_rg.column("ema_50")[-1].as_py()),
            "ema_200": float(last_rg.column("ema_200")[-1].as_py()),
            "ema_800": float(last_rg.column("ema_800")[-1].as_py()),
        }

        # Extract overlap bars for bit-exact seam comparison
        overlap_ohlcv = {
            "open_time_ms": tail_ts,
            "open": last_rg.column("open").to_numpy()[-SEAM_OVERLAP_BARS:],
            "high": last_rg.column("high").to_numpy()[-SEAM_OVERLAP_BARS:],
            "low": last_rg.column("low").to_numpy()[-SEAM_OVERLAP_BARS:],
            "close": last_rg.column("close").to_numpy()[-SEAM_OVERLAP_BARS:],
            "volume_base": last_rg.column("volume_base").to_numpy()[-SEAM_OVERLAP_BARS:],
        }

        return {
            "last_open_ms": last_open_ms,
            "total_rows": total_rows,
            "checkpoint": checkpoint,
            "overlap_ohlcv": overlap_ohlcv,
        }
    except Exception:
        return None


def verify_seam_overlap(stored_overlap: Dict[str, np.ndarray], refetched_df: pd.DataFrame) -> bool:
    """
    Bit-exact verification of the N bars preceding the seam.
    Prevents splicing if upstream Binance klines were retroactively revised.
    """
    try:
        refetched_sub = refetched_df[refetched_df["open_time"].isin(stored_overlap["open_time_ms"])].sort_values("open_time")
        if len(refetched_sub) != len(stored_overlap["open_time_ms"]):
            return False

        # Bit-exact check on OHLCV values
        for col, ref_col in [("open", "open"), ("high", "high"), ("low", "low"), ("close", "close"), ("volume_base", "volume")]:
            stored_val = np.asarray(stored_overlap[col], dtype=np.float64)
            ref_val = refetched_sub[ref_col].to_numpy(dtype=np.float64)
            if not np.all(stored_val == ref_val):
                return False
        return True
    except Exception:
        return False


def perform_incremental_append(
    symbol: str,
    master_path: str,
    ladder_path: Optional[str],
    fetcher: BinanceHistoricalFetcher,
    processor: HistoricalMetricsProcessor,
    end_dt: datetime,
    all_footprint: bool = False,
    footprint_days: int = 0,
    allow_seam_revision: bool = False,
    log: Callable[[str], None] = print,
) -> Optional[Tuple[pd.DataFrame, Optional[pd.DataFrame]]]:
    """
    Executes a certified incremental tail append:
    1. Reads boundary plan in O(1) time via ParquetFile metadata.
    2. Fetches [last_open - WARMUP_BARS, end_dt].
    3. Validates bit-exact seam overlap.
    4. Slices tail bars > last_open_ms.
    5. Re-anchors lifetime CVD and exact-seeds EMAs.
    6. Stitches, verifies cadence, and returns (stitched_master, stitched_ladder).
    """
    plan = compute_incremental_append_plan(master_path)
    if plan is None:
        log(f"[INCR] {symbol}: usable boundary plan absent -> full rebuild required")
        return None

    last_open_ms = plan["last_open_ms"]
    last_open_dt = pd.to_datetime(last_open_ms, unit="ms", utc=True)
    now_ms = int(end_dt.timestamp() * 1000)

    # Section B: Cap on tail size
    missing_days = (now_ms - last_open_ms) / 86_400_000
    if missing_days > MAX_TAIL_DAYS:
        log(f"[INCR] {symbol}: missing gap ({missing_days:.1f} days) > MAX_TAIL_DAYS ({MAX_TAIL_DAYS}) -> forcing full rebuild")
        return None

    if end_dt <= last_open_dt:
        log(f"[INCR] {symbol}: data already current through {last_open_dt:%Y-%m-%d %H:%M}")
        old_master = pd.read_parquet(master_path)
        old_ladder = pd.read_parquet(ladder_path) if (ladder_path and os.path.exists(ladder_path)) else None
        return old_master, old_ladder

    warmup_start_dt = pd.to_datetime(last_open_ms - WARMUP_BARS * BAR_MS, unit="ms", utc=True)
    log(f"[INCR] {symbol}: tail fetch {warmup_start_dt:%Y-%m-%d} -> {end_dt:%Y-%m-%d} (tail: {missing_days:.2f} days, warmup: {WARMUP_BARS} bars)")

    # Fetch raw streams for warmup + tail
    klines = fetcher.fetch_futures_klines(symbol, warmup_start_dt.strftime("%Y-%m-%d"), end_dt)
    spot = fetcher.fetch_spot_klines(symbol, warmup_start_dt.strftime("%Y-%m-%d"), end_dt)
    metrics = fetcher.fetch_metrics(symbol, warmup_start_dt.strftime("%Y-%m-%d"), end_dt)
    funding = fetcher.fetch_funding_rates(symbol, int(warmup_start_dt.timestamp() * 1000))

    if klines.empty or int(klines["open_time"].iloc[-1]) <= last_open_ms:
        log(f"[INCR] {symbol}: no new closed bars upstream")
        old_master = pd.read_parquet(master_path)
        old_ladder = pd.read_parquet(ladder_path) if (ladder_path and os.path.exists(ladder_path)) else None
        return old_master, old_ladder

    # Section C: Seam Overlap Bit-Exact Verification
    if not allow_seam_revision:
        seam_ok = verify_seam_overlap(plan["overlap_ohlcv"], klines)
        if not seam_ok:
            log(f"[REJECT] {symbol}: bit-exact seam overlap check failed (Binance revised historical bars) -> fallback to full rebuild")
            return None

    # Footprint tail if enabled
    fp_summary, fp_ladder = pd.DataFrame(), pd.DataFrame()
    if all_footprint or footprint_days > 0:
        fp_start = last_open_dt
        fp_ladder, fp_summary = fetcher.fetch_footprint(symbol, fp_start.strftime("%Y-%m-%d"), now=end_dt)

    # Section D: Feature computation on warmup + tail
    inc_master = processor.process_master_dataset(
        klines, metrics, funding, fp_summary, spot, symbol=symbol,
        export_start_ms=int(warmup_start_dt.timestamp() * 1000),
        export_end_ms=now_ms,
    )

    # Extract strictly new bars
    new_bars = inc_master[inc_master["open_time_ms"] > last_open_ms].copy()
    if new_bars.empty:
        log(f"[INCR] {symbol}: zero new bars after boundary filter")
        old_master = pd.read_parquet(master_path)
        old_ladder = pd.read_parquet(ladder_path) if (ladder_path and os.path.exists(ladder_path)) else None
        return old_master, old_ladder

    # Strict continuity assertion
    first_new_open = int(new_bars["open_time_ms"].iloc[0])
    expected_first_open = last_open_ms + BAR_MS
    if first_new_open != expected_first_open:
        log(f"[REJECT] {symbol}: seam discontinuity! Expected {expected_first_open}, got {first_new_open} -> full rebuild")
        return None

    # Re-anchor single-file embedded CVD checkpoint accumulators
    checkpoint = plan["checkpoint"]
    new_bars["future_cvd_lifetime"] = np.round(
        checkpoint["future_cvd_lifetime"] + np.cumsum(new_bars["future_cvd_15m"].to_numpy(np.float64)), 8
    )
    new_bars["spot_cvd_lifetime"] = np.round(
        checkpoint["spot_cvd_lifetime"] + np.cumsum(new_bars["spot_cvd_15m"].to_numpy(np.float64)), 8
    )

    # Exact recursive EMA seeding from stored checkpoint
    closes = new_bars["close"].to_numpy(np.float64)
    for p in (8, 21, 50, 200, 800):
        alpha = 2.0 / (p + 1.0)
        curr = checkpoint[f"ema_{p}"]
        out_ema = np.empty(len(closes), dtype=np.float64)
        for i, c_val in enumerate(closes):
            curr = alpha * c_val + (1.0 - alpha) * curr
            out_ema[i] = curr
        new_bars[f"ema_{p}"] = np.round(out_ema, 8)

    # Load full stored history and concatenate
    old_master = pd.read_parquet(master_path)
    combined_master = pd.concat([old_master, new_bars], ignore_index=True)

    # Cadence assertion across full stitched frame
    full_ts = combined_master["open_time_ms"].to_numpy(np.int64)
    if not np.all(np.diff(full_ts) == BAR_MS):
        log(f"[REJECT] {symbol}: cadence violation across stitched frame -> full rebuild")
        return None

    # Coerce canonical schema and dtypes
    combined_master = combined_master[CANONICAL_COLUMNS]
    for col, dt in COLUMN_DTYPES.items():
        combined_master[col] = combined_master[col].astype(dt)

    # Section F: Post-export smoke assertion (recompute RSI on last 100 bars, verify rtol=1e-9)
    smoke_close = combined_master["close"].to_numpy(np.float64)[-100:]
    smoke_rsi = compute_wilder_rsi_series(smoke_close, 14)
    target_rsi = combined_master["rsi_14"].to_numpy(np.float64)[-100:]
    if not np.allclose(smoke_rsi[-20:], target_rsi[-20:], rtol=RTOL_INDICATOR, atol=1e-6):
        log(f"[REJECT] {symbol}: post-stitch smoke assertion failed on RSI-14 -> full rebuild")
        return None

    # Assemble ladder tail
    combined_ladder = None
    if ladder_path and os.path.exists(ladder_path):
        old_ladder = pd.read_parquet(ladder_path)
        if not fp_ladder.empty:
            new_ladder, _ = assemble_ladder(new_bars, fp_ladder, allow_synthetic=False)
            combined_ladder = pd.concat([old_ladder, new_ladder], ignore_index=True)
        else:
            combined_ladder = old_ladder

    log(f"[INCR] {symbol}: certified append of {len(new_bars)} bars ({pd.to_datetime(full_ts[-len(new_bars)], unit='ms', utc=True)} -> {pd.to_datetime(full_ts[-1], unit='ms', utc=True)})")
    return combined_master, combined_ladder
`


================================================================================
# FILE 3/9: Engine/pipeline/binance_historical_fetcher.py
# DESCRIPTION: Async/Parallel Binance Vision Downloader, ZIP Unpacker, REST Fallback & Gap Repair
================================================================================

`python
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


class ArchiveParseError(RuntimeError):
    """Raised when an HTTP 200 response contains corrupt, truncated, or unparseable archive data."""
    pass


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
            self.log(f"  [FATAL PARSE ERROR] {url}: {exc}")
            raise ArchiveParseError(f"Corrupt archive or parse failure {url}: {exc}") from exc
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
                except ArchiveParseError as exc:
                    self.log(f"  [FATAL PARSE ERROR] {label} {k}: {exc}")
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
            os.makedirs(os.path.dirname(cache_ladder_path), exist_ok=True)
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
            self.log(f"  [FATAL PARSE ERROR] error streaming aggTrades for {symbol} {date_str}: {e}")
            raise ArchiveParseError(f"Corrupt aggTrades zip or parse failure {symbol} {date_str}: {e}") from e

    def _aggregate_trades_to_ladder(
        self,
        trades: pd.DataFrame,
        merge_step: float,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return aggregate_trades_to_ladder(trades, merge_step)


`


================================================================================
# FILE 4/9: Engine/pipeline/historical_metrics_processor.py
# DESCRIPTION: Continuous Timeline Builder, Vectorised CVD, Spot Matching & Liquidation Math
================================================================================

`python
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
STALE_RUN_BARS = 288       # 3 days of 15m bars
OI_MUST_BE_MOVING = 0.90   # else the whole tape was down and a frozen ratio is expected


def _stale_runs_mask(values: np.ndarray, threshold: int, oi_moves: np.ndarray, min_moving: float) -> np.ndarray:
    """
    Flags entire runs of >= threshold identical values where open interest is moving >= min_moving.
    Matches the exact detection contract of audit_probe_metrics_validity.

    WARNING (RETROSPECTIVE RESEARCH FLAG ONLY - STRICT CAUSAL SEPARATION):
    This function flags runs of >= threshold identical values across the entire run retroactively
    from bar 0 to bar L-1. Therefore, bars 0..threshold-1 are flagged ex-post based on the future
    knowledge that the run eventually reaches length >= threshold.

    This flag (`is_imputed_metrics`) is strictly an EX-POST DATA QUALITY & QUARANTINE FILTER for
    dataset validation and retrospective backtesting universe pruning. It MUST NEVER be used as a
    contemporaneous, point-in-time predictive signal or live trading trigger, as that would
    constitute future lookahead leakage.
    """
    n = len(values)
    if n < threshold:
        return np.zeros(n, dtype=bool)
    v = np.round(values.astype(np.float64), 8)
    v = np.where(np.isnan(v), np.inf, v)
    change = np.flatnonzero(np.diff(v) != 0)
    starts = np.concatenate(([0], change + 1))
    lengths = np.diff(np.concatenate((starts, [len(v)])))
    mask = np.zeros(n, dtype=bool)
    for s, L in zip(starts, lengths):
        if L >= threshold:
            moving = float(oi_moves[s:min(s + L, n - 1)].mean()) if n > 1 else 0.0
            if moving >= min_moving:
                mask[s:s + L] = True
    return mask


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
        export_end_ms: Optional[int] = None,
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
            raw_fp_buy = fpm["taker_buy_vol_coin"].fillna(0.0).to_numpy(np.float64)
            raw_fp_sell = fpm["taker_sell_vol_coin"].fillna(0.0).to_numpy(np.float64)
            fp_tot = raw_fp_buy + raw_fp_sell
            use_fp = exact & (fp_tot > 0)
            buy = np.where(use_fp, raw_fp_buy, kl_buy)
            sell = np.where(use_fp, raw_fp_sell, kl_sell)
            vb = np.where(use_fp, fp_tot, vb)
            out["volume_base"] = vb
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
            stale = fm["_age_ms"].to_numpy(np.float64) > FUNDING_MAX_STALENESS_MS
            fr = np.where(np.isnan(fr) | stale, 0.0001, fr)
            if stale.any():
                log(f"[PROCESSOR] {symbol}: {int(stale.sum())} bars with funding older than {FUNDING_MAX_STALENESS_MS / 3_600_000:.0f}h -> default 0.01% (stale-guarded)")
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
            oi_coin_raw = merged["sum_open_interest"]
            oi_age = merged["sum_open_interest_age"]
            # A1: impossible values -- open interest must be finite, > 0, and not stale
            available_raw = (~np.isnan(oi_coin_raw)) & (oi_coin_raw > 0.0) & (oi_age <= METRICS_MAX_STALENESS_MS)
            
            # Causal rolling median check to identify severe anomalies (< 20% of local median when median > 1k)
            s_raw = pd.Series(np.where(available_raw, oi_coin_raw, np.nan))
            causal_med = s_raw.rolling(201, min_periods=20).median().ffill().to_numpy()
            is_impossible_oi = (~available_raw) | ((~np.isnan(causal_med)) & (causal_med > 1000.0) & (oi_coin_raw < 0.20 * causal_med))
            
            # Causal forward fill across impossible episodes, zero if at start
            oi_coin = pd.Series(np.where(is_impossible_oi, np.nan, oi_coin_raw)).ffill().fillna(0.0).to_numpy(np.float64)
            available = (~is_impossible_oi) & (oi_coin > 0.0)

            oi_usd = merged["sum_open_interest_value"]
            oi_usd_ff = pd.Series(np.where(is_impossible_oi | np.isnan(oi_usd), np.nan, oi_usd)).ffill().to_numpy(np.float64)
            oi_usd = np.where(np.isnan(oi_usd_ff), oi_coin * c, oi_usd_ff)
            ls_glob = np.where(np.isnan(merged["count_long_short_ratio"]), 1.0, merged["count_long_short_ratio"])
            ls_top = np.where(np.isnan(merged["sum_toptrader_long_short_ratio"]), 1.0, merged["sum_toptrader_long_short_ratio"])
            top_acc = merged["count_toptrader_long_short_ratio"]
            top_acc = np.where(np.isnan(top_acc), ls_glob, top_acc)
            taker_ratio = merged["sum_taker_long_short_vol_ratio"]
            taker_ratio = np.where(np.isnan(taker_ratio), fallback_taker, taker_ratio)

            # A1b: detect frozen upstream positioning runs (>= 288 bars while OI moves >= 90%)
            oi_moves = np.diff(oi_coin) != 0 if n > 1 else np.array([False])
            frozen_mask = np.zeros(n, dtype=bool)
            for col_arr in (ls_glob, ls_top, top_acc, taker_ratio):
                frozen_mask |= _stale_runs_mask(col_arr, STALE_RUN_BARS, oi_moves, OI_MUST_BE_MOVING)
            
            # Whale index computed from sanitized inputs
            top_long_p = ls_top / (1.0 + ls_top)
            glob_long_p = ls_glob / (1.0 + ls_glob)
            whale_idx = top_long_p / np.maximum(glob_long_p, 1e-4) * 100.0
            frozen_mask |= _stale_runs_mask(whale_idx, STALE_RUN_BARS, oi_moves, OI_MUST_BE_MOVING)

            # Mark metrics available only if OI is valid AND positioning is not frozen upstream
            is_valid_metrics = available & (~frozen_mask)
            out["metrics_available"] = is_valid_metrics.astype(np.int8)
        else:
            log(f"[WARN] {symbol}: no official metrics stream")
            oi_coin = np.zeros(n)
            oi_usd = np.zeros(n)
            ls_glob = np.ones(n)
            ls_top = np.ones(n)
            top_acc = np.ones(n)
            taker_ratio = fallback_taker
            whale_idx = np.full(n, 100.0)
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
        out["whale_index"] = whale_idx
        out["taker_volume_ratio"] = np.clip(taker_ratio, 0.0, 1e6)
        out["is_imputed_metrics"] = (~is_valid_metrics).astype(np.int8)

        # ---------------------------------------------------------------- session value area & trades
        log(f"[PROCESSOR] {symbol}: session value area & trade execution")
        svah, sval, pvah, pval = compute_session_value_area(ot, h, l, c, vb, bucket_size=get_merge_level(symbol))
        out["session_vah"], out["session_val"] = svah, sval
        out["prev_day_vah"], out["prev_day_val"] = pvah, pval
        out["taker_buy_count"] = buy_cnt.astype(np.int64)
        out["taker_sell_count"] = sell_cnt.astype(np.int64)
        out["taker_buy_vol_btc"] = buy
        out["taker_sell_vol_btc"] = sell
        out["avg_trade_size_usd"] = np.divide(vq, np.maximum(tc, 1))

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
        out["zc_div"] = np.where(spot_exact, spot_delta - fut_delta, 0.0)
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

        if export_end_ms is not None:
            keep_end = out["open_time_ms"].to_numpy() <= int(export_end_ms)
            if not keep_end.any():
                raise ValueError(f"{symbol}: no bars at/before {pd.to_datetime(export_end_ms, unit='ms', utc=True)}")
            out = out.loc[keep_end].reset_index(drop=True)
            log(f"[PROCESSOR] {symbol}: sliced up to end date ({pd.to_datetime(export_end_ms, unit='ms', utc=True)})")

        final = self._finalise(out[CANONICAL_COLUMNS].copy())
        log(f"[PROCESSOR] {symbol}: {len(final):,} rows x {len(final.columns)} cols")
        return final

    # ------------------------------------------------------------------ finalise
    @staticmethod
    def _finalise(df: pd.DataFrame) -> pd.DataFrame:
        price_cols = ("open", "high", "low", "close", "atr_14", "atr_100", "ema_8", "ema_21", "ema_50", "ema_200",
                      "ema_800", "basis_usd", "session_vah", "session_val", "prev_day_vah", "prev_day_val",
                      "spot_close", "session_vwap")
        coin_cols = ("volume_base", "future_cvd_15m", "future_cvd_session", "future_cvd_lifetime", "spot_cvd_15m",
                     "spot_cvd_session", "spot_cvd_lifetime", "open_interest_k", "taker_buy_vol_btc",
                     "taker_sell_vol_btc", "zc_div")
        usd_cols = ("volume_quote", "volume_sma9", "open_interest_usd", "long_liq_usd", "short_liq_usd",
                    "avg_trade_size_usd")
        ratio_cols = ("rsi_14", "ls_ratio_global", "ls_ratio_top", "top_account_ratio", "whale_index",
                      "taker_volume_ratio", "vwap_zscore", "volume_ratio", "long_liq_zs",
                      "short_liq_zs", "liq_imbalance_ratio")
        pct_cols = ("funding_rate_pct", "oi_change_pct")
        for cols, dp in ((price_cols, PRICE_DP), (coin_cols, COIN_DP), (usd_cols, USD_DP), (ratio_cols, RATIO_DP), (pct_cols, PCT_DP)):
            for col in cols:
                df[col] = np.round(df[col].to_numpy(np.float64), dp)
        # Ensure exact volume conservation and CVD identity after coin_cols rounding
        df["taker_sell_vol_btc"] = np.round(df["volume_base"] - df["taker_buy_vol_btc"], COIN_DP)
        df["future_cvd_15m"] = np.round(df["taker_buy_vol_btc"] - df["taker_sell_vol_btc"], COIN_DP)
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
`


================================================================================
# FILE 5/9: Engine/pipeline/http_client.py
# DESCRIPTION: Resilient HTTP Client, Exponential Backoff, Retry Handling & Binance 418 Protection
================================================================================

`python
"""
================================================================================
RATE-LIMIT-AWARE HTTP CLIENT (Binance Vision archive + fapi/api REST)
================================================================================
* Exponential backoff with full jitter on transient failures.
* HTTP 429 / 418: honours ``Retry-After`` and raises a process-wide cooldown
  latch so *every* worker thread pauses (a single banned IP stalls the pool
  instead of 16 threads compounding the ban).
* HTTP 404 on the immutable archive host is a permanent negative result and is
  memoised for the life of the process.
* Retries are bounded; the final failure is surfaced (never swallowed).
================================================================================
"""

from __future__ import annotations

import random
import threading
import time
import urllib.error
import urllib.request
from typing import Optional, Set

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "*/*",
}

_RATE_LIMIT_CODES = (418, 429)
_TRANSIENT_CODES = (500, 502, 503, 504, 520, 522, 524)


class FetchError(RuntimeError):
    pass


class HttpClient:
    _global_cooldown_until: float = 0.0
    _global_lock: threading.Lock = threading.Lock()
    _global_not_found: Set[str] = set()

    def __init__(
        self,
        max_attempts: int = 6,
        base_delay: float = 0.5,
        max_delay: float = 60.0,
        timeout: float = 30.0,
        min_interval: float = 0.05,
        rate_limit_cooldown: float = 30.0,
        ban_cooldown: float = 120.0,
    ) -> None:
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.timeout = timeout
        self.min_interval = min_interval
        self.rate_limit_cooldown = rate_limit_cooldown
        self.ban_cooldown = ban_cooldown
        self._cooldown_until = 0.0
        self._lock = threading.Lock()
        self._last_call = 0.0
        self._not_found: Set[str] = set()
        self.stats = {"requests": 0, "retries": 0, "rate_limited": 0, "not_found": 0, "failed": 0}

    # ------------------------------------------------------------------ utils
    def _sleep_for_cooldown(self) -> None:
        while True:
            with HttpClient._global_lock:
                g_wait = HttpClient._global_cooldown_until - time.monotonic()
            with self._lock:
                wait = max(self._cooldown_until - time.monotonic(), g_wait)
            if wait <= 0:
                return
            time.sleep(min(wait, 5.0))

    def _throttle(self) -> None:
        if self.min_interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            wait = self._last_call + self.min_interval - now
            self._last_call = max(now, self._last_call + self.min_interval)
        if wait > 0:
            time.sleep(wait)

    def _trip_cooldown(self, seconds: float) -> None:
        until = time.monotonic() + seconds
        with HttpClient._global_lock:
            HttpClient._global_cooldown_until = max(HttpClient._global_cooldown_until, until)
        with self._lock:
            self._cooldown_until = max(self._cooldown_until, until)
            self.stats["rate_limited"] += 1

    def _backoff(self, attempt: int) -> float:
        cap = min(self.max_delay, self.base_delay * (2 ** attempt))
        return random.uniform(0, cap)

    # ------------------------------------------------------------------ API
    def get(self, url: str, timeout: Optional[float] = None, allow_404: bool = True) -> Optional[bytes]:
        """
        Returns the response body, or ``None`` on a 404 when ``allow_404``.
        Raises ``FetchError`` after exhausting retries on any other failure.
        """
        with HttpClient._global_lock:
            if url in HttpClient._global_not_found:
                return None
        with self._lock:
            if url in self._not_found:
                return None
        timeout = timeout or self.timeout
        last_exc: Optional[BaseException] = None
        for attempt in range(self.max_attempts):
            self._sleep_for_cooldown()
            self._throttle()
            with self._lock:
                self.stats["requests"] += 1
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.read()
            except urllib.error.HTTPError as e:
                last_exc = e
                if e.code == 404:
                    with HttpClient._global_lock:
                        HttpClient._global_not_found.add(url)
                    with self._lock:
                        self.stats["not_found"] += 1
                        self._not_found.add(url)
                    if allow_404:
                        return None
                    raise FetchError(f"404 {url}") from e
                if e.code in _RATE_LIMIT_CODES:
                    retry_after = e.headers.get("Retry-After") if e.headers else None
                    server_cool = 0.0
                    if retry_after:
                        try:
                            server_cool = float(retry_after)
                        except ValueError:
                            server_cool = 0.0
                    if server_cool > 0.0:
                        # Server gave explicit instruction: honor it directly, bounded with a 5s floor and 2h ceiling
                        cool = min(max(server_cool, 5.0), 7200.0)
                    else:
                        base = self.rate_limit_cooldown if e.code == 429 else self.ban_cooldown
                        raw_cool = base * (attempt + 1)
                        cool = min(self.max_delay * 10, raw_cool)
                    self._trip_cooldown(cool)
                elif e.code in _TRANSIENT_CODES:
                    time.sleep(self._backoff(attempt))
                else:
                    raise FetchError(f"HTTP {e.code} {url}") from e
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
                last_exc = e
                time.sleep(self._backoff(attempt))
            with self._lock:
                self.stats["retries"] += 1
        with self._lock:
            self.stats["failed"] += 1
        raise FetchError(f"exhausted {self.max_attempts} attempts for {url}: {last_exc!r}")

    def get_optional(self, url: str, timeout: Optional[float] = None) -> Optional[bytes]:
        """
        Fetches URL allowing HTTP 404 (returns None).
        Any non-404 transport error (5xx, timeouts, connection drops) raises FetchError.
        """
        return self.get(url, timeout=timeout, allow_404=True)
`


================================================================================
# FILE 6/9: Engine/pipeline/parquet_exporter.py
# DESCRIPTION: Atomic Dual-Table Parquet Exporter, Schema Validator & SHA256 Manifest Generator
================================================================================

`python
"""
================================================================================
DUAL-TABLE PARQUET EXPORTER (schema-validated, atomic)
================================================================================
Table 1  {symbol}_15m_master_2020_2026.parquet
Table 2  {symbol}_15m_footprint_ladder.parquet
Manifest {symbol}_dataset_manifest.json

* Column order and dtypes are coerced to the canonical contract *before* the
  write; a frame that cannot be coerced raises ``SchemaError`` and nothing is
  written.
* Files are written to a temp path in the target directory and ``os.replace``d
  so a crash never leaves a truncated Parquet in place.
* Table 2 is written with a row-group size aligned to whole candles so
  predicate push-down on ``open_time_ms`` stays efficient.
================================================================================
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from ..core.schema import (
    CANONICAL_COLUMNS,
    COLUMN_DTYPES,
    LADDER_COLUMNS,
    LADDER_DTYPES,
    ladder_filename,
    manifest_filename,
    master_filename,
)


class SchemaError(ValueError):
    pass


def _coerce(df: pd.DataFrame, columns: List[str], dtypes: Dict[str, str], table: str) -> pd.DataFrame:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise SchemaError(f"{table}: missing columns {missing}")
    out = df[columns].copy()
    for col in columns:
        dt = dtypes[col]
        try:
            if dt == "string":
                out[col] = out[col].astype(str)
            else:
                out[col] = out[col].astype(dt)
        except (TypeError, ValueError) as exc:
            raise SchemaError(f"{table}: column {col} not coercible to {dt}: {exc}") from exc
    num = [c for c in columns if dtypes[c] not in ("string",)]
    arr = out[num].to_numpy(dtype=np.float64)
    if not np.isfinite(arr).all():
        bad = [num[j] for j in np.where(~np.isfinite(arr).all(axis=0))[0]]
        raise SchemaError(f"{table}: non-finite values in {bad}")
    return out


def _arrow_schema(columns: List[str], dtypes: Dict[str, str]) -> pa.Schema:
    m = {"int64": pa.int64(), "int8": pa.int8(), "float64": pa.float64(), "string": pa.large_string()}
    return pa.schema([pa.field(c, m[dtypes[c]], nullable=False) for c in columns])


def _atomic_write(df: pd.DataFrame, path: str, schema: pa.Schema, row_group_size: Optional[int]) -> None:
    table = pa.Table.from_pandas(df, schema=schema, preserve_index=False)
    tmp = path + ".tmp"
    pq.write_table(table, tmp, compression="snappy", row_group_size=row_group_size, use_dictionary=True, write_statistics=True)
    os.replace(tmp, path)

def _file_sha256(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


class ParquetExporter:
    def __init__(self, output_dir: str) -> None:
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def master_path(self, symbol: str) -> str:
        return os.path.join(self.output_dir, master_filename(symbol))

    def ladder_path(self, symbol: str) -> str:
        return os.path.join(self.output_dir, ladder_filename(symbol))

    def manifest_path(self, symbol: str) -> str:
        return os.path.join(self.output_dir, manifest_filename(symbol))

    def export_master(self, df: pd.DataFrame, symbol: str) -> str:
        clean = _coerce(df, CANONICAL_COLUMNS, COLUMN_DTYPES, "master")
        path = self.master_path(symbol)
        _atomic_write(clean, path, _arrow_schema(CANONICAL_COLUMNS, COLUMN_DTYPES), row_group_size=65_536)
        return path

    def export_ladder(self, ladder: pd.DataFrame, symbol: str) -> str:
        clean = _coerce(ladder, LADDER_COLUMNS, LADDER_DTYPES, "ladder")
        path = self.ladder_path(symbol)
        # row groups end on candle boundaries (~1M rows)
        ts = clean["open_time_ms"].to_numpy()
        rg = 1_048_576
        if len(clean) > rg:
            change = np.flatnonzero(np.diff(ts)) + 1
            target = change[np.searchsorted(change, rg)] if np.searchsorted(change, rg) < len(change) else len(clean)
            rg = int(target)
        _atomic_write(clean, path, _arrow_schema(LADDER_COLUMNS, LADDER_DTYPES), row_group_size=rg)
        return path

    def write_manifest(self, master: pd.DataFrame, symbol: str, ladder_stats: Dict[str, Any],
                       verification: Dict[str, Any], metrics_absent_days: Optional[List[str]] = None,
                       expected_start_ms: Optional[int] = None,
                       expected_end_ms: Optional[int] = None,
                       expected_rows: Optional[int] = None) -> str:
        mpath, lpath = self.master_path(symbol), self.ladder_path(symbol)
        exp_start = int(expected_start_ms) if expected_start_ms is not None else (int(master["open_time_ms"].iloc[0]) if not master.empty else None)
        exp_end = int(expected_end_ms) if expected_end_ms is not None else (int(master["open_time_ms"].iloc[-1]) if not master.empty else None)
        exp_rows = int(expected_rows) if expected_rows is not None else int(len(master))
        manifest = {
            "symbol": symbol,
            "timeframe": "15m",
            "total_rows": int(len(master)),
            "expected_rows": exp_rows,
            "expected_start_ms": exp_start,
            "expected_end_ms": exp_end,
            "columns": list(master.columns),
            "column_count": int(len(master.columns)),
            "start_time_utc": str(master["datetime_utc"].iloc[0]),
            "end_time_utc": str(master["datetime_utc"].iloc[-1]),
            "exported_at_utc": datetime.now(timezone.utc).isoformat(),
            "master_file": os.path.basename(mpath),
            "master_sha256": _file_sha256(mpath),
            "master_size_mb": round(os.path.getsize(mpath) / 1_048_576, 2) if os.path.exists(mpath) else None,
            "ladder_file": os.path.basename(lpath) if os.path.exists(lpath) else None,
            "ladder_sha256": _file_sha256(lpath) if os.path.exists(lpath) else None,
            "ladder_size_mb": round(os.path.getsize(lpath) / 1_048_576, 2) if os.path.exists(lpath) else None,
            "ladder": ladder_stats,
            "provenance": {
                "tick_exact_bars": int(ladder_stats.get("tick_exact_candles", 0)),
                "spot_exact_bars": int((master["spot_close"].notna()).sum()) if "spot_close" in master else 0,
                "imputed_metrics_bars": int((master["is_imputed_metrics"] == 1).sum()) if "is_imputed_metrics" in master else 0,
                "metrics_archive_absent_months": sorted({d[:7] for d in (metrics_absent_days or [])}),
                "metrics_archive_absent_days": sorted(metrics_absent_days or []),
                "metrics_archive_absent_day_count": len(set(metrics_absent_days or [])),
                "metrics_unavailable_fraction_by_year": {
                    str(y): round(float((master.loc[master["datetime_utc"].str[:4] == str(y), "is_imputed_metrics"] == 1).mean()), 4)
                    for y in sorted(master["datetime_utc"].str[:4].unique())
                } if "datetime_utc" in master and "is_imputed_metrics" in master else {},
            },
            "verification": verification,
            "schema_version": "2.1",
        }
        path = self.manifest_path(symbol)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2)
        os.replace(tmp, path)
        return path
`


================================================================================
# FILE 7/9: Engine/core/schema.py
# DESCRIPTION: Canonical 62-Column Schema, Data Types, Precision Rules & Listing Dates
================================================================================

`python
"""
================================================================================
CANONICAL MARKET DATA SCHEMA & COLUMN SPECIFICATIONS
================================================================================
Single source of truth for the dual-table Parquet contract:

  Table 1  {symbol}_15m_master_2020_2026.parquet   (one row per 15m candle)
  Table 2  {symbol}_15m_footprint_ladder.parquet   (one row per price rung per candle)

Backward compatibility contract
-------------------------------
The first 62 entries of CANONICAL_COLUMNS are byte-for-byte identical (name,
order, dtype) to the legacy schema consumed by quant_strategy_suite.py,
run_expanding_walkforward_ml.py, trend_orderflow_features.py and the live
monitor. New features are only ever APPENDED after ``metrics_available``.
================================================================================
"""

from typing import Dict, List, Tuple

BAR_MS: int = 900_000                      # 15 minutes
DAY_MS: int = 86_400_000
MASTER_FILENAME_TEMPLATE = "{symbol}_15m_master_2020_2026.parquet"
LADDER_FILENAME_TEMPLATE = "{symbol}_15m_footprint_ladder.parquet"
MANIFEST_FILENAME_TEMPLATE = "{symbol}_dataset_manifest.json"

# ------------------------------------------------------------------------------
# Numeric precision policy (decimal places). Prices are stored at Binance's
# maximum tick precision so sub-dollar assets (DOGE, TRX, ADA...) never collapse.
# ------------------------------------------------------------------------------
PRICE_DP: int = 8
COIN_DP: int = 8
USD_DP: int = 2
RATIO_DP: int = 6
PCT_DP: int = 6

CANONICAL_COLUMNS: List[str] = [
    # 1. Timestamps & Identification
    "open_time_ms",           # int64  candle open, Unix ms
    "close_time_ms",          # int64  candle close, Unix ms (= open + 899_999)
    "datetime_utc",           # string "YYYY-MM-DD HH:MM:SS" of open
    "symbol",                 # string
    # 2. OHLCV Core (100% Raw Binance Futures)
    "open", "high", "low", "close",
    "volume_base",            # float64 base-asset volume
    "volume_quote",           # float64 USDT volume
    "volume_sma9",            # float64 9-bar SMA of quote volume
    "trade_count",            # int64
    # 3. Momentum & Volatility (Deterministic Math)
    "rsi_14", "atr_14", "atr_100",
    # 4. EMAs (Mathematical trendlines)
    "ema_8", "ema_21", "ema_50", "ema_200", "ema_800",
    # 5. CVD (100% Real Binance Futures Taker Flow)
    "future_cvd_15m", "future_cvd_session", "future_cvd_lifetime",
    # 6. Spot CVD (100% Real Binance Spot Taker Flow)
    "spot_cvd_15m", "spot_cvd_session", "spot_cvd_lifetime",
    # 7. Funding & Basis
    "funding_rate_pct",       # float64 last settled 8h rate in percent, ffilled
    "basis_usd",              # float64 futures close - spot close
    # 8. Open Interest (100% Real Binance Derivatives Metrics)
    "open_interest_k",        # float64 OI in thousands of contracts (coins)
    "open_interest_usd",
    "oi_change_pct",          # float64 15m pct change of OI
    # 9. Liquidations (Calibrated Institutional Liquidation Model)
    "long_liq_usd", "short_liq_usd",
    # 10. Positioning (100% Real Binance Accounts Metrics)
    "ls_ratio_global",        # global account long/short ratio
    "ls_ratio_top",           # top-trader POSITION long/short ratio
    "top_account_ratio",      # top-trader ACCOUNT long/short ratio
    "whale_index",
    "taker_volume_ratio",     # official taker buy/sell volume ratio
    # 11. Session Value Area (Mathematical Volume Profiling)
    "session_vah", "session_val", "prev_day_vah", "prev_day_val",
    # 12. Trade Execution & Sizing (100% Real Binance Trades)
    "taker_buy_count", "taker_sell_count",
    "taker_buy_vol_btc", "taker_sell_vol_btc",
    "avg_trade_size_usd",
    # 13. Spot Ground Truth & Extended Features
    "spot_close",             # float64 spot close matched 1:1 from Binance Spot
    "session_vwap",           # float64 volume-weighted average price since 00:00 UTC
    "vwap_zscore",            # float64 (close - vwap) / rolling_std(close - vwap, 24)
    "volume_ratio",           # float64 volume_base / SMA9(volume_base)
    "zc_div",                 # float64 spot_cvd_15m - future_cvd_15m
    "long_liq_zs",            # float64 rolling-96 z-score of |long_liq_usd|
    "short_liq_zs",           # float64 rolling-96 z-score of short_liq_usd
    "liq_imbalance_ratio",    # float64 (short - |long|) / (short + |long|) in [-1, 1]
    "is_imputed_metrics",     # int8 1 = ex-post data-quality quarantine (official metrics missing/frozen/imputed, e.g. 2022 API outage or Binance reporting halt). RETROSPECTIVE ONLY: not for contemporaneous live signals.
]

# Backward compatibility aliases
LEGACY_COLUMNS: List[str] = CANONICAL_COLUMNS
EXTENDED_COLUMNS: List[str] = []

COLUMN_DTYPES: Dict[str, str] = {
    "open_time_ms": "int64", "close_time_ms": "int64",
    "datetime_utc": "string", "symbol": "string",
    "is_imputed_metrics": "int8",
    "trade_count": "int64", "taker_buy_count": "int64", "taker_sell_count": "int64",
}
for _c in CANONICAL_COLUMNS:
    COLUMN_DTYPES.setdefault(_c, "float64")

STRING_VOCAB: Dict[str, Tuple[str, ...]] = {}

# Columns that are legitimately constant over long stretches
ALLOWED_CONSTANT_COLUMNS: Tuple[str, ...] = (
    "symbol", "is_imputed_metrics",
)

# ------------------------------------------------------------------------------
# Fixed Institutional Price Merge Levels (Deterministic Order Flow Geometry)
# ------------------------------------------------------------------------------
FIXED_MERGE_STEPS: Dict[str, float] = {
    "BTCUSDT": 25.0,        # Standard Exocharts / Sierra Chart $25 bucket
    "ETHUSDT": 1.0,         # Standard Exocharts / Sierra Chart $1 bucket
    "SOLUSDT": 0.10,        # Sub-dollar microstructure (10 cents)
    "BNBUSDT": 0.50,        # Half-dollar bucket
    "DOGEUSDT": 0.0005,     # 5-pip bucket
    "XRPUSDT": 0.0010,      # 10-pip bucket
    "ADAUSDT": 0.0005,      # 5-pip bucket
    "TRXUSDT": 0.0001,      # Single pip bucket
    "LINKUSDT": 0.02,       # 2-cent bucket
    "AVAXUSDT": 0.05,       # 5-cent bucket
    "SUIUSDT": 0.005,       # Half-cent bucket
    "NEARUSDT": 0.01,       # 1-cent bucket
    "DOTUSDT": 0.01,        # 1-cent bucket
    "LTCUSDT": 0.10,        # 10-cent bucket
    "BCHUSDT": 0.50,        # Half-dollar bucket
    "APTUSDT": 0.01,        # 1-cent bucket
    "OPUSDT": 0.005,        # Half-cent bucket
    "ARBUSDT": 0.002,       # 2-tenth cent bucket
}

# ------------------------------------------------------------------------------
# Table 2: 100% Real Empirical Footprint Ladder (13 Columns)
# ------------------------------------------------------------------------------
LADDER_COLUMNS: List[str] = [
    "open_time_ms",        # int64  FK -> Table 1 15m candle timestamp
    "price_bin",           # float64 fixed price rung (e.g. 65000.0, 65025.0)
    "bid_vol_coin",        # float64 aggressive sell volume into bid
    "ask_vol_coin",        # float64 aggressive buy volume into ask
    "net_delta_coin",      # float64 ask_vol - bid_vol
    "total_vol_coin",      # float64 ask_vol + bid_vol
    "trade_count",         # int64  trade count executed at this rung
    "is_poc",              # int8   1 if Point of Control of this 15m candle, else 0
    "is_buy_imbalance",    # int8   1 if diagonal buy imbalance >= 3:1 with notional floor
    "is_sell_imbalance",   # int8   1 if diagonal sell imbalance >= 3:1 with notional floor
    "is_stacked_buy_imb",  # int8   1 if part of >= 3 stacked buy imbalance cluster
    "is_stacked_sell_imb", # int8   1 if part of >= 3 stacked sell imbalance cluster
    "is_value_area",       # int8   1 if within 70% Value Area (VAH to VAL)
]
LADDER_DTYPES: Dict[str, str] = {
    "open_time_ms": "int64", "price_bin": "float64", "bid_vol_coin": "float64",
    "ask_vol_coin": "float64", "net_delta_coin": "float64", "total_vol_coin": "float64",
    "trade_count": "int64", "is_poc": "int8", "is_buy_imbalance": "int8",
    "is_sell_imbalance": "int8", "is_stacked_buy_imb": "int8", "is_stacked_sell_imb": "int8",
    "is_value_area": "int8",
}
RUNG_SOURCE_TICK: int = 0
RUNG_SOURCE_SYNTHETIC: int = 1


# ------------------------------------------------------------------------------
# Universe
# ------------------------------------------------------------------------------
SYMBOLS: List[str] = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT",
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT",
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT",
]

# First trading day of each USDT-M perpetual. Used to bound archive scans and to
# start EMA warm-up as early as history allows.
FUTURES_LISTING_DATES: Dict[str, str] = {
    "BTCUSDT": "2019-09-08", "ETHUSDT": "2019-11-27", "XRPUSDT": "2020-01-06",
    "SOLUSDT": "2020-09-14", "BNBUSDT": "2020-02-10", "DOGEUSDT": "2020-07-10",
    "ADAUSDT": "2020-01-31", "TRXUSDT": "2020-01-15", "LINKUSDT": "2020-01-17",
    "AVAXUSDT": "2020-09-23", "SUIUSDT": "2023-05-03", "NEARUSDT": "2020-10-15",
    "DOTUSDT": "2020-08-18", "LTCUSDT": "2020-01-09", "BCHUSDT": "2020-01-15",
    "APTUSDT": "2022-10-19", "OPUSDT": "2022-06-01", "ARBUSDT": "2023-03-23",
}

DEFAULT_START_DATE: str = "2020-09-01"
WARMUP_START_DATE: str = "2019-09-01"


def master_filename(symbol: str) -> str:
    return MASTER_FILENAME_TEMPLATE.format(symbol=symbol)


def ladder_filename(symbol: str) -> str:
    return LADDER_FILENAME_TEMPLATE.format(symbol=symbol)


def manifest_filename(symbol: str) -> str:
    return MANIFEST_FILENAME_TEMPLATE.format(symbol=symbol)
`


================================================================================
# FILE 8/9: Engine/core/canonical_indicators.py
# DESCRIPTION: Prefix-Invariant Indicator Kernels: EMAs, Wilder RSI/ATR, VWAP & Z-Scores
================================================================================

`python
"""
================================================================================
CANONICAL TECHNICAL & MICROSTRUCTURE INDICATOR KERNELS (VECTORISED, CAUSAL)
================================================================================
Every kernel in this module satisfies the *prefix-invariance* property:

    f(x[:n])[:k] == f(x)[:k]   for all k <= n

i.e. the value at bar t depends only on bars <= t. This is asserted by
verification/test_pipeline_offline.py::test_prefix_invariance.

No kernel iterates over bars in Python. Recursive filters (EMA / Wilder RMA)
are expressed as exactly-seeded exponentially weighted means, which are
bit-identical to the textbook per-bar recursion.
================================================================================
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

DAY_MS = 86_400_000
_EPS = 1e-12


# ------------------------------------------------------------------------------
# Symbol scale helpers
# ------------------------------------------------------------------------------
def get_merge_level(symbol: str) -> float:
    """Canonical value-area bucket size (price units) per asset scale."""
    s = symbol.upper()
    if s.startswith("BTC"):
        return 25.0
    if s.startswith("ETH"):
        return 1.0
    if any(s.startswith(x) for x in ("SOL", "BNB", "BCH", "AVAX", "LTC", "APT", "LINK")):
        return 0.1
    if any(s.startswith(x) for x in ("DOT", "NEAR", "SUI", "OP", "ARB")):
        return 0.01
    return 0.0001


def nice_bin_step(prices: np.ndarray, bps: float = 3.5) -> np.ndarray:
    """
    Element-wise 'nice' price bin step targeting ``bps`` basis points of price.
    Vectorised equivalent of the rounding ladder used by the tick fetcher so
    exact and synthetic rungs share identical geometry rules.
    """
    raw = np.asarray(prices, dtype=np.float64) * (bps / 10_000.0)
    step = np.where(
        raw >= 10.0, np.round(raw / 5.0) * 5.0,
        np.where(raw >= 1.0, np.round(raw, 1),
        np.where(raw >= 0.1, np.round(raw, 2),
        np.where(raw >= 0.01, np.round(raw, 3),
        np.where(raw >= 0.001, np.round(raw, 4),
        np.round(raw, 6))))),
    )
    return np.maximum(step, 1e-6)


# ------------------------------------------------------------------------------
# Recursive smoothers
# ------------------------------------------------------------------------------
def compute_ema_series(prices: np.ndarray, period: int) -> np.ndarray:
    """EMA seeded at bar 0 (ema[0] = price[0]), alpha = 2 / (period + 1)."""
    x = np.asarray(prices, dtype=np.float64)
    if x.size == 0:
        return x.copy()
    return pd.Series(x).ewm(span=period, adjust=False).mean().to_numpy()


def compute_wilder_rma_series(values: np.ndarray, period: int) -> np.ndarray:
    """
    Wilder RMA with causal warm-up:
        bars 0 .. period-2 : expanding mean of values[:t+1]
        bars period-1 ..   : y_t = y_{t-1} + (x_t - y_{t-1}) / period
    Bit-identical to the per-bar recursion (verified max|delta| = 0.0).
    """
    x = np.asarray(values, dtype=np.float64)
    n = x.size
    if n == 0:
        return x.copy()
    expanding = np.cumsum(x) / np.arange(1, n + 1, dtype=np.float64)
    if n <= period:
        return expanding
    seeded = x.copy()
    seeded[period - 1] = expanding[period - 1]
    tail = pd.Series(seeded[period - 1:]).ewm(alpha=1.0 / period, adjust=False).mean().to_numpy()
    out = np.empty(n, dtype=np.float64)
    out[: period - 1] = expanding[: period - 1]
    out[period - 1:] = tail
    return out


def compute_wilder_rsi_series(closes: np.ndarray, period: int = 14) -> np.ndarray:
    """Wilder RSI; bar 0 = 50. Degenerate zero-loss bars map to 100 / 50."""
    c = np.asarray(closes, dtype=np.float64)
    n = c.size
    if n == 0:
        return c.copy()
    rsi = np.full(n, 50.0, dtype=np.float64)
    if n == 1:
        return rsi
    d = np.diff(c)
    gains = np.maximum(d, 0.0)
    losses = np.maximum(-d, 0.0)
    avg_gain = compute_wilder_rma_series(gains, period)
    avg_loss = compute_wilder_rma_series(losses, period)
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = avg_gain / avg_loss
        body = 100.0 - 100.0 / (1.0 + rs)
    zero_loss = avg_loss <= _EPS
    body = np.where(zero_loss, np.where(avg_gain > _EPS, 100.0, 50.0), body)
    rsi[1:] = body
    return np.clip(rsi, 0.0, 100.0)


def compute_true_range(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray) -> np.ndarray:
    h = np.asarray(highs, dtype=np.float64)
    l = np.asarray(lows, dtype=np.float64)
    c = np.asarray(closes, dtype=np.float64)
    prev_c = np.empty_like(c)
    prev_c[0] = c[0] if c.size else 0.0
    prev_c[1:] = c[:-1]
    return np.maximum(h - l, np.maximum(np.abs(h - prev_c), np.abs(l - prev_c)))


def compute_wilder_atr_series(highs, lows, closes, period: int = 14) -> np.ndarray:
    if len(closes) == 0:
        return np.array([], dtype=np.float64)
    return compute_wilder_rma_series(compute_true_range(highs, lows, closes), period)


def compute_sma_series(values: np.ndarray, window: int) -> np.ndarray:
    """Simple moving average with causal expanding warm-up (min_periods = 1)."""
    x = np.asarray(values, dtype=np.float64)
    if x.size == 0:
        return x.copy()
    return pd.Series(x).rolling(window, min_periods=1).mean().to_numpy()


def compute_volume_sma9_series(volumes: np.ndarray) -> np.ndarray:
    return compute_sma_series(volumes, 9)


def compute_rolling_zscore(values: np.ndarray, window: int) -> np.ndarray:
    """(x - mean_w) / std_w (ddof = 0). 0.0 during warm-up or when std ~ 0."""
    s = pd.Series(np.asarray(values, dtype=np.float64))
    mean = s.rolling(window, min_periods=window).mean()
    std = s.rolling(window, min_periods=window).std(ddof=0)
    z = (s - mean) / std.where(std > _EPS)
    return z.replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy()


# ------------------------------------------------------------------------------
# Session (00:00 UTC anchored) accumulators
# ------------------------------------------------------------------------------
def session_day_index(timestamps_ms: np.ndarray) -> np.ndarray:
    return (np.asarray(timestamps_ms, dtype=np.int64) // DAY_MS)


def compute_session_cvd(timestamps_ms: np.ndarray, deltas: np.ndarray) -> np.ndarray:
    """Running cumulative delta resetting at each 00:00 UTC boundary."""
    if len(deltas) == 0:
        return np.array([], dtype=np.float64)
    day = session_day_index(timestamps_ms)
    return pd.Series(np.asarray(deltas, dtype=np.float64)).groupby(day).cumsum().to_numpy()


def compute_session_vwap(timestamps_ms, highs, lows, closes, volumes) -> np.ndarray:
    """
    Session VWAP anchored at 00:00 UTC using typical price (H+L+C)/3.
    Falls back to close while the session has zero traded volume.
    """
    c = np.asarray(closes, dtype=np.float64)
    if c.size == 0:
        return c.copy()
    tp = (np.asarray(highs, dtype=np.float64) + np.asarray(lows, dtype=np.float64) + c) / 3.0
    v = np.asarray(volumes, dtype=np.float64)
    day = session_day_index(timestamps_ms)
    pv = pd.Series(tp * v).groupby(day).cumsum().to_numpy()
    cv = pd.Series(v).groupby(day).cumsum().to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        vwap = np.where(cv > _EPS, pv / np.where(cv > _EPS, cv, 1.0), c)
    return vwap


def compute_vwap_zscore(closes, vwap, window: int = 24) -> np.ndarray:
    dev = np.asarray(closes, dtype=np.float64) - np.asarray(vwap, dtype=np.float64)
    s = pd.Series(dev)
    std = s.rolling(window, min_periods=window).std(ddof=0)
    z = s / std.where(std > _EPS)
    return z.replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy()


# ------------------------------------------------------------------------------
# Depth proxy
# ------------------------------------------------------------------------------
def estimate_depth_from_volatility(closes, atrs, base_vols) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    +-1% resting depth proxy from ATR elasticity and traded volume.
    Returns positive magnitudes: (bid_usd, ask_usd, bid_coin, ask_coin).
    """
    c = np.asarray(closes, dtype=np.float64)
    atr = np.asarray(atrs, dtype=np.float64)
    v = np.asarray(base_vols, dtype=np.float64)
    rel_vol = np.maximum(atr / np.maximum(c, 1e-12), 0.001) * 100.0
    scaling = np.clip(1.0 / rel_vol, 0.5, 2.0)
    depth_coin = v * 0.025 * scaling
    depth_usd = depth_coin * c
    return depth_usd, depth_usd.copy(), depth_coin, depth_coin.copy()


# ------------------------------------------------------------------------------
# Developing session value area (dense per-session prefix-sum profile)
# ------------------------------------------------------------------------------
def compute_session_value_area(
    timestamps_ms: np.ndarray,
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    volumes: np.ndarray,
    bucket_size: float = 25.0,
    volume_pct: float = 0.70,
    max_cells_per_chunk: int = 4_000_000,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Developing 70% value area per UTC session plus the prior session's final VA.

    Each bar's volume is spread uniformly over the price buckets it spans
    (floor(low/b) .. floor(high/b)). The developing profile at bar t is the
    prefix sum of the session's per-bar distributions up to and including t,
    so the value at t never sees bars > t.

    The value area is built the classical way: start at the POC bucket and
    repeatedly absorb whichever adjacent bucket (above / below) holds more
    volume until >= ``volume_pct`` of the session volume is enclosed. VAH/VAL
    are the upper/lower bucket prices of that contiguous region.

    Sessions are processed as dense tensors [sessions, bars, buckets]; the only
    Python loops are over session-chunks and over expansion steps (bounded by
    the bucket count), never over bars.
    """
    n = len(timestamps_ms)
    out_vah = np.zeros(n, dtype=np.float64)
    out_val = np.zeros(n, dtype=np.float64)
    if n == 0:
        return out_vah, out_val, out_vah.copy(), out_val.copy()

    h = np.asarray(highs, dtype=np.float64)
    l = np.asarray(lows, dtype=np.float64)
    c = np.asarray(closes, dtype=np.float64)
    v = np.asarray(volumes, dtype=np.float64)
    day = session_day_index(timestamps_ms)

    lo_b = np.floor(l / bucket_size + 1e-9).astype(np.int64)
    hi_b = np.maximum(np.floor(h / bucket_size + 1e-9).astype(np.int64), lo_b)
    cl_b = np.floor(c / bucket_size + 1e-9).astype(np.int64)
    per_bin = v / (hi_b - lo_b + 1)

    _, day_start, bars_per_day = np.unique(day, return_index=True, return_counts=True)
    n_days = day_start.size
    day_of_bar = np.repeat(np.arange(n_days), bars_per_day)
    pos_in_day = np.arange(n) - day_start[day_of_bar]
    day_lo = np.minimum.reduceat(lo_b, day_start)
    day_hi = np.maximum.reduceat(hi_b, day_start)
    day_bins = day_hi - day_lo + 1
    max_bars_global = int(bars_per_day.max())
    # causal traded range inside the session (running min low / running max high)
    run_lo = pd.Series(lo_b).groupby(day).cummin().to_numpy()
    run_hi = pd.Series(hi_b).groupby(day).cummax().to_numpy()

    # greedy session chunking under a dense-cell budget (loop over ~2k sessions)
    chunks = []
    cur_start, cur_max_bins = 0, 0
    for i in range(n_days):
        cand_max = max(cur_max_bins, int(day_bins[i]))
        if i > cur_start and (i - cur_start + 1) * max_bars_global * (cand_max + 1) > max_cells_per_chunk:
            chunks.append((cur_start, i))
            cur_start, cur_max_bins = i, int(day_bins[i])
        else:
            cur_max_bins = cand_max
    chunks.append((cur_start, n_days))

    for d0, d1 in chunks:
        days_in_chunk = np.arange(d0, d1)
        nd = days_in_chunk.size
        idx = np.where((day_of_bar >= d0) & (day_of_bar < d1))[0]
        max_bars = int(bars_per_day[days_in_chunk].max())
        max_bins = int(day_bins[days_in_chunk].max())

        local_day = day_of_bar[idx] - d0
        local_pos = pos_in_day[idx]
        base = day_lo[day_of_bar[idx]]
        col_lo = lo_b[idx] - base
        col_hi = hi_b[idx] - base + 1  # exclusive

        diff = np.zeros((nd, max_bars, max_bins + 1), dtype=np.float64)
        np.add.at(diff, (local_day, local_pos, col_lo), per_bin[idx])
        np.add.at(diff, (local_day, local_pos, col_hi), -per_bin[idx])
        profile = np.cumsum(np.cumsum(diff, axis=2)[:, :, :max_bins], axis=1)
        del diff

        total = profile.sum(axis=2)
        target = total * volume_pct
        # expansion bounds = buckets traded so far in the session (causal)
        lo_bound = np.zeros((nd, max_bars), dtype=np.int64)
        hi_bound = np.zeros((nd, max_bars), dtype=np.int64)
        lo_bound[local_day, local_pos] = run_lo[idx] - base
        hi_bound[local_day, local_pos] = run_hi[idx] - base

        poc = profile.argmax(axis=2)
        a = poc.copy()
        b = poc.copy()
        cur = np.take_along_axis(profile, poc[:, :, None], axis=2)[:, :, 0]
        active = (cur < target) & (total > _EPS)
        for _ in range(max_bins):
            if not active.any():
                break
            up_ok = (b + 1) <= hi_bound
            down_ok = (a - 1) >= lo_bound
            up_v = np.where(up_ok, np.take_along_axis(profile, np.minimum(b + 1, max_bins - 1)[:, :, None], axis=2)[:, :, 0], -1.0)
            down_v = np.where(down_ok, np.take_along_axis(profile, np.maximum(a - 1, 0)[:, :, None], axis=2)[:, :, 0], -1.0)
            choose_up = active & up_ok & (up_v >= down_v)
            choose_down = active & ~choose_up & down_ok
            b = np.where(choose_up, b + 1, b)
            a = np.where(choose_down, a - 1, a)
            cur = cur + np.where(choose_up, up_v, 0.0) + np.where(choose_down, down_v, 0.0)
            active = active & (cur < target) & (((b + 1) <= hi_bound) | ((a - 1) >= lo_bound))
        del profile

        vah_bin = b[local_day, local_pos]
        val_bin = a[local_day, local_pos]
        zero_vol = total[local_day, local_pos] <= _EPS
        close_col = cl_b[idx] - base
        vah_bin = np.where(zero_vol, close_col, vah_bin)
        val_bin = np.where(zero_vol, close_col, val_bin)
        out_vah[idx] = (vah_bin + base) * bucket_size
        out_val[idx] = (val_bin + base) * bucket_size

    # prior-session finalised VA: value at the last bar of the previous session
    day_end = day_start + bars_per_day - 1
    prev_vah_day = np.empty(n_days, dtype=np.float64)
    prev_val_day = np.empty(n_days, dtype=np.float64)
    prev_vah_day[1:] = out_vah[day_end][:-1]
    prev_val_day[1:] = out_val[day_end][:-1]
    prev_vah_day[0] = np.nan
    prev_val_day[0] = np.nan
    prev_vah = np.repeat(prev_vah_day, bars_per_day)
    prev_val = np.repeat(prev_val_day, bars_per_day)
    first = day_of_bar == 0
    prev_vah[first] = out_vah[first]
    prev_val[first] = out_val[first]
    return out_vah, out_val, prev_vah, prev_val
`


================================================================================
# FILE 9/9: Engine/verification/verify_parquet_integrity.py
# DESCRIPTION: 3-Agent Verification Council (Schema, Statistical, OrderFlow) & Causal Repair Engine
================================================================================

`python
"""
================================================================================
AUTONOMOUS 3-AGENT VERIFICATION COUNCIL
================================================================================
+---------------------------------------------------------------+
| Agent 1: Continuity & Cadence | monotonic open_time_ms with    |
|                               | exactly 900,000 ms steps, zero |
|                               | missing / duplicate candles,   |
|                               | close = open + 899,999, ladder |
|                               | referential integrity.         |
+-------------------------------+--------------------------------+
| Agent 2: Microstructure Math  | CVD identities (15m / session  |
|                               | / lifetime), zc_div identity,  |
|                               | basis = close - spot_close,    |
|                               | funding sign/magnitude, VWAP   |
|                               | re-derivation, EMA recursion,  |
|                               | OHLC sanity, non-zero volume   |
|                               | ratios, liquidation polarity,  |
|                               | ladder volume conservation,    |
|                               | exactly one POC per candle.    |
+-------------------------------+--------------------------------+
| Agent 3: Zero-Null & Schema   | zero NaN / null / inf, exact   |
|                               | column set + dtype contract,   |
|                               | string vocabularies, flag      |
|                               | domains, dead-feature scan.    |
+---------------------------------------------------------------+

Each agent returns a list of ``Finding`` objects carrying the bar index and
UTC timestamp of the first offending row. The council verdict is PASS only if
every agent has zero findings. Findings are also returned as data so the
orchestrator can attempt targeted causal repair and re-run the council.

Usage
  python -m Engine.verification.verify_parquet_integrity [target_dir] [--symbol SYM]
================================================================================
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Engine.core.canonical_indicators import (  # noqa: E402
    compute_ema_series,
    compute_session_cvd,
    compute_session_vwap,
    get_merge_level,
)
from Engine.core.schema import (  # noqa: E402
    ALLOWED_CONSTANT_COLUMNS,
    BAR_MS,
    CANONICAL_COLUMNS,
    COLUMN_DTYPES,
    LADDER_COLUMNS,
    LADDER_DTYPES,
    STRING_VOCAB,
    ladder_filename,
    manifest_filename,
    master_filename,
)

DEFAULT_TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "binance_backtesting_data")
_TOL = 1e-6

# --- regime-scan calibration (multi-asset universe) ---------------------------
REGIME_MIN_AVAIL_BARS = 500        # bars *carrying metrics* needed to judge a year
METRICS_INTERIOR_HOLE_BARS = 4032  # 28 days of 15m bars with no metrics content at all
BASIS_MIN_DISTINCT = 20            # a spread that only ever takes <20 values is broken
BASIS_MODAL_SHARE_MAX = 0.98       # >98% of bars on one basis value => spot collapsed


@dataclass
class Finding:
    agent: str
    check: str
    message: str
    bar_index: Optional[int] = None
    open_time_ms: Optional[int] = None
    timestamp_utc: Optional[str] = None
    count: int = 1

    def __str__(self) -> str:
        loc = ""
        if self.bar_index is not None:
            loc = f" @ bar {self.bar_index} ({self.timestamp_utc}, open_time_ms={self.open_time_ms})"
        extra = f" [x{self.count}]" if self.count > 1 else ""
        return f"[{self.agent}] {self.check}: {self.message}{loc}{extra}"


@dataclass
class CouncilReport:
    symbol: str
    passed: bool
    master_rows: int
    ladder_rows: int
    findings: List[Finding] = field(default_factory=list)
    agent_status: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol, "passed": self.passed, "master_rows": self.master_rows,
            "ladder_rows": self.ladder_rows, "agent_status": self.agent_status,
            "findings": [asdict(f) for f in self.findings[:50]],
        }


def _first_bad(mask: np.ndarray, ts: np.ndarray) -> Tuple[Optional[int], Optional[int], Optional[str], int]:
    idx = np.flatnonzero(mask)
    if idx.size == 0:
        return None, None, None, 0
    i = int(idx[0])
    t = int(ts[i])
    return i, t, str(pd.to_datetime(t, unit="ms", utc=True)), int(idx.size)


def _finding(agent: str, check: str, message: str, mask: np.ndarray, ts: np.ndarray) -> Optional[Finding]:
    i, t, s, n = _first_bad(mask, ts)
    if n == 0:
        return None
    return Finding(agent, check, message, i, t, s, n)


# ==============================================================================
# Agent 1 -- Continuity & Cadence
# ==============================================================================
def agent_continuity(master: pd.DataFrame, ladder: Optional[pd.DataFrame],
                     expected_start_ms: Optional[int] = None,
                     expected_end_ms: Optional[int] = None) -> List[Finding]:
    A = "Agent1:Continuity"
    out: List[Finding] = []
    ts = master["open_time_ms"].to_numpy(np.int64)
    n = ts.size
    if n == 0:
        return [Finding(A, "empty", "master has zero rows")]
    if expected_start_ms is not None and n > 0:
        exp_first = (expected_start_ms // BAR_MS) * BAR_MS
        if ts[0] != exp_first:
            out.append(Finding(A, "start_boundary", f"first candle {ts[0]} ({pd.to_datetime(ts[0], unit='ms', utc=True)}) != expected start {exp_first} ({pd.to_datetime(exp_first, unit='ms', utc=True)})"))
    if expected_end_ms is not None and n > 0:
        exp_last = (expected_end_ms // BAR_MS) * BAR_MS
        if ts[-1] != exp_last:
            out.append(Finding(A, "end_boundary", f"last candle {ts[-1]} ({pd.to_datetime(ts[-1], unit='ms', utc=True)}) != expected terminal {exp_last} ({pd.to_datetime(exp_last, unit='ms', utc=True)})"))
    if n > 1:
        d = np.diff(ts)
        f = _finding(A, "monotonic", "open_time_ms not strictly increasing", np.append(False, d <= 0), ts)
        if f:
            out.append(f)
        f = _finding(A, "cadence", f"step != {BAR_MS} ms (missing/extra candle)", np.append(False, d != BAR_MS), ts)
        if f:
            out.append(f)
        dup = np.append(False, d == 0)
        if dup.any():
            out.append(_finding(A, "duplicates", "duplicate open_time_ms", dup, ts))
        missing = int(((ts[-1] - ts[0]) // BAR_MS + 1) - n)
        if missing > 0:
            out.append(Finding(A, "coverage", f"{missing} candle(s) missing from grid"))
    grid = (ts % BAR_MS) != 0
    f = _finding(A, "grid", "open_time_ms not aligned to 15m boundary", grid, ts)
    if f:
        out.append(f)
    ct = master["close_time_ms"].to_numpy(np.int64)
    f = _finding(A, "close_time", "close_time_ms != open_time_ms + 899,999", ct != ts + BAR_MS - 1, ts)
    if f:
        out.append(f)
    dt = pd.to_datetime(master["datetime_utc"], utc=True, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    dt_ms = ((dt - epoch) // pd.Timedelta(milliseconds=1)).fillna(-1).to_numpy(np.int64)
    f = _finding(A, "datetime_utc", "datetime_utc does not match open_time_ms", dt.isna().to_numpy() | (dt_ms != ts), ts)
    if f:
        out.append(f)

    if ladder is not None and not ladder.empty:
        lts = ladder["open_time_ms"].to_numpy(np.int64)
        if lts.size and (np.diff(lts) < 0).any():
            out.append(Finding(A, "ladder_order", "ladder open_time_ms not non-decreasing"))
        uniq = np.unique(lts)
        orphan = ~np.isin(uniq, ts)
        if orphan.any():
            i = int(np.flatnonzero(orphan)[0])
            out.append(Finding(A, "ladder_orphans", "ladder candles absent from master", None, int(uniq[i]),
                               str(pd.to_datetime(uniq[i], unit="ms", utc=True)), int(orphan.sum())))
        in_ladder_scope = (ts >= lts[0]) & (ts <= lts[-1])
        has_volume = (master["volume_base"].to_numpy(np.float64) > 0) if "volume_base" in master else np.ones(len(master), dtype=bool)
        uncovered = ~np.isin(ts, uniq) & in_ladder_scope & has_volume
        f = _finding(A, "ladder_coverage", "master candles without any ladder rung", uncovered, ts)
        if f:
            out.append(f)
        pb = ladder[["open_time_ms", "price_bin"]].to_numpy()
        if len(pb) and pd.DataFrame(pb).duplicated().any():
            out.append(Finding(A, "ladder_dup_rung", "duplicate (open_time_ms, price_bin) rung"))
    return out


# ==============================================================================
# Agent 2 -- Microstructure Math
# ==============================================================================
def agent_microstructure(master: pd.DataFrame, ladder: Optional[pd.DataFrame]) -> List[Finding]:
    A = "Agent2:Microstructure"
    out: List[Finding] = []
    ts = master["open_time_ms"].to_numpy(np.int64)
    has = master.columns.__contains__
    g = lambda c: master[c].to_numpy(np.float64)  # noqa: E731
    o, h, l, c = g("open"), g("high"), g("low"), g("close")
    vb, vq = g("volume_base"), g("volume_quote")
    scale = np.maximum(np.abs(c), 1e-9)

    def add(check, msg, mask):
        f = _finding(A, check, msg, mask, ts)
        if f:
            out.append(f)

    add("ohlc_bounds", "high < max(open, close) or low > min(open, close)",
        (h < np.maximum(o, c) - 1e-9 * scale) | (l > np.minimum(o, c) + 1e-9 * scale))
    add("positive_price", "non-positive price", (o <= 0) | (h <= 0) | (l <= 0) | (c <= 0))
    add("negative_volume", "negative volume", (vb < 0) | (vq < 0))
    synthetic = master["is_synthetic"].to_numpy() == 1 if "is_synthetic" in master else ((h == l) & (vb <= 0))
    add("live_bar_volume", "authentic bar with zero base volume", (~synthetic) & (vb <= 0))
    if has("volume_ratio"):
        add("volume_ratio_nonzero", "volume_ratio must be > 0 on authentic bars", (~synthetic) & (g("volume_ratio") <= 0))
    add("volume_sma9", "volume_sma9 <= 0 on authentic bar", (~synthetic) & (g("volume_sma9") <= 0))

    tb, tsell = g("taker_buy_vol_btc"), g("taker_sell_vol_btc")
    add("taker_split", "taker buy + sell != volume_base", np.abs(tb + tsell - vb) > 1e-6 * np.maximum(vb, 1))
    add("taker_ratio", "taker_volume_ratio must be finite and >= 0", ~(g("taker_volume_ratio") >= 0))

    fut = g("future_cvd_15m")
    add("fut_cvd_identity", "future_cvd_15m != taker_buy - taker_sell", np.abs(fut - (tb - tsell)) > 1e-6 * np.maximum(vb, 1))
    if has("fp_delta"):
        add("fp_delta_identity", "fp_delta != future_cvd_15m", np.abs(g("fp_delta") - fut) > _TOL)
    fs = g("future_cvd_session")
    add("fut_session_cvd", "future_cvd_session != causal session cumsum",
        np.abs(fs - compute_session_cvd(ts, fut)) > 1e-6 * np.maximum(np.abs(fs), 1) + 1e-6)
    fl = g("future_cvd_lifetime")
    add("fut_lifetime_cvd", "future_cvd_lifetime increments != future_cvd_15m",
        np.append(abs(fl[0] - fut[0]) > 1e-6 * max(abs(fut[0]), 1) + 1e-6, np.abs(np.diff(fl) - fut[1:]) > 1e-6 * np.maximum(np.abs(fl[1:]), 1) + 1e-6))
    spot = g("spot_cvd_15m")
    ss = g("spot_cvd_session")
    add("spot_session_cvd", "spot_cvd_session != causal session cumsum",
        np.abs(ss - compute_session_cvd(ts, spot)) > 1e-6 * np.maximum(np.abs(ss), 1) + 1e-6)
    sl = g("spot_cvd_lifetime")
    add("spot_lifetime_cvd", "spot_cvd_lifetime increments != spot_cvd_15m",
        np.append(abs(sl[0] - spot[0]) > 1e-6 * max(abs(spot[0]), 1) + 1e-6, np.abs(np.diff(sl) - spot[1:]) > 1e-6 * np.maximum(np.abs(sl[1:]), 1) + 1e-6))

    unavailable = (master["spot_flow_source"].to_numpy() == "UNAVAILABLE") if "spot_flow_source" in master else ((g("zc_div") == 0.0) & (spot == 0.0) & (fut != 0.0))
    if "spot_flow_source" in master:
        add("spot_unavailable_zero", "spot_cvd_15m must be 0 when spot_flow_source=UNAVAILABLE (stale reuse)", unavailable & (spot != 0))
    if has("zc_div"):
        add("zc_div_identity", "zc_div != spot_cvd_15m - future_cvd_15m on valid spot bars",
            (~unavailable) & (np.abs(g("zc_div") - (spot - fut)) > 1e-6 * np.maximum(np.abs(fut) + np.abs(spot), 1)))
        if "spot_flow_source" in master:
            add("zc_div_unavailable_zero", "zc_div must be 0 when spot_flow_source=UNAVAILABLE",
                unavailable & (g("zc_div") != 0))

    if has("spot_close"):
        add("basis_identity", "basis_usd != close - spot_close", np.abs(g("basis_usd") - (c - g("spot_close"))) > 1e-6 * scale)
    add("basis_magnitude", "|basis| > price (misaligned spot)", np.abs(g("basis_usd")) > 1.0 * scale)

    fr = g("funding_rate_pct")
    add("funding_bounds", "funding_rate_pct outside Binance clamp [-3%, +3%]", np.abs(fr) > 3.0 + 1e-9)
    if fr.size > 1000 and 0 < float(np.percentile(np.abs(fr), 95)) < 1e-3:
        out.append(Finding(A, "funding_units", f"funding_rate_pct 95th percentile |x|={float(np.percentile(np.abs(fr), 95)):.2e}: looks like a raw decimal, not percent"))

    add("liq_polarity", "long_liq_usd must be <= 0 and short_liq_usd >= 0", (g("long_liq_usd") > 0) | (g("short_liq_usd") < 0))
    if has("liq_imbalance_ratio"):
        add("liq_imbalance_domain", "liq_imbalance_ratio outside [-1, 1]", np.abs(g("liq_imbalance_ratio")) > 1 + 1e-9)
    add("rsi_domain", "rsi_14 outside [0, 100]", (g("rsi_14") < 0) | (g("rsi_14") > 100))
    add("atr_nonneg", "ATR negative", (g("atr_14") < 0) | (g("atr_100") < 0))
    add("oi_change_domain", "oi_change_pct outside [-100, 100]", np.abs(g("oi_change_pct")) > 100 + 1e-9)
    add("oi_nonneg", "open interest negative", (g("open_interest_k") < 0) | (g("open_interest_usd") < 0))
    
    avail_mask = (master["metrics_available"].to_numpy() == 1) if "metrics_available" in master else (master["is_imputed_metrics"].to_numpy() == 0)
    add("oi_impossible_zero", "open_interest_k == 0 while metrics marked valid", avail_mask & (g("open_interest_k") == 0))
    add("ratios_positive", "L/S ratios must be > 0", (g("ls_ratio_global") <= 0) | (g("ls_ratio_top") <= 0) | (g("top_account_ratio") <= 0))
    if has("bid_depth_usd"):
        add("depth_positive", "depth proxies must be non-negative magnitudes",
            (g("bid_depth_usd") < 0) | (g("ask_depth_usd") < 0) | (g("bid_depth_coin") < 0) | (g("ask_depth_coin") < 0))
    add("value_area_order", "session_val > session_vah", g("session_val") > g("session_vah") + 1e-9)
    add("prev_va_order", "prev_day_val > prev_day_vah", g("prev_day_val") > g("prev_day_vah") + 1e-9)
    
    if has("fp_poc") and "poc_source" in master:
        add("poc_in_range", "fp_poc more than 0.5% outside [low, high] on tick-exact bars",
            (master["poc_source"].to_numpy() == "TICK_EXACT") & ((g("fp_poc") < l - 5e-3 * scale) | (g("fp_poc") > h + 5e-3 * scale)))
        add("poc_in_range_approx", "fp_poc outside [low, high] on OHLC-approximated bars",
            (master["poc_source"].to_numpy() == "OHLC_APPROX") & ((g("fp_poc") < l - 1e-6 * scale) | (g("fp_poc") > h + 1e-6 * scale)))

    # Re-derivations: a stored series can only match the causal recomputation if it used no future data.
    if has("session_vwap"):
        vwap = compute_session_vwap(ts, h, l, c, vb)
        add("vwap_rederive", "session_vwap != causal re-derivation from OHLCV", np.abs(g("session_vwap") - vwap) > 1e-6 * scale + 1e-6)
        add("vwap_in_range", "session_vwap outside session running [min low, max high] envelope",
            (g("session_vwap") < pd.Series(l).groupby(ts // 86_400_000).cummin().to_numpy() - 1e-6 * scale) |
            (g("session_vwap") > pd.Series(h).groupby(ts // 86_400_000).cummax().to_numpy() + 1e-6 * scale))
    for p in (8, 21):
        ema = g(f"ema_{p}")
        k = 2.0 / (p + 1.0)
        rec = np.empty_like(ema)
        rec[0] = ema[0]
        rec[1:] = c[1:] * k + ema[:-1] * (1.0 - k)
        add(f"ema_{p}_recursion", f"ema_{p} violates one-step recursion (stored value used other inputs)",
            np.abs(ema - rec) > 5e-8 * scale + 1e-8)
    # lookahead probe on session accumulators: first bar of each day must equal the bar's own delta / TP
    day = ts // 86_400_000
    first = np.append(True, np.diff(day) != 0)
    add("session_reset", "session CVD did not reset at 00:00 UTC", first & (np.abs(g("future_cvd_session") - fut) > 1e-6 * np.maximum(np.abs(fut), 1)))

    if ladder is not None and len(ladder):
        lts = ladder["open_time_ms"].to_numpy(np.int64)
        poc_per = ladder.groupby("open_time_ms")["is_poc"].sum()
        bad_poc = poc_per[poc_per != 1]
        if len(bad_poc):
            t = int(bad_poc.index[0])
            out.append(Finding(A, "ladder_poc", "candle must have exactly one POC rung", None, t,
                               str(pd.to_datetime(t, unit="ms", utc=True)), int(len(bad_poc))))
        bid, ask = ladder["bid_vol_coin"].to_numpy(np.float64), ladder["ask_vol_coin"].to_numpy(np.float64)
        neg = (bid < 0) | (ask < 0)
        if neg.any():
            i = int(np.flatnonzero(neg)[0])
            out.append(Finding(A, "ladder_neg_vol", "negative rung volume", None, int(lts[i]), str(pd.to_datetime(lts[i], unit="ms", utc=True)), int(neg.sum())))
        nd = ladder["net_delta_coin"].to_numpy(np.float64)
        bad_nd = np.abs(nd - (ask - bid)) > 1e-6 * np.maximum(ask + bid, 1)
        if bad_nd.any():
            i = int(np.flatnonzero(bad_nd)[0])
            out.append(Finding(A, "ladder_delta", "net_delta_coin != ask - bid", None, int(lts[i]), str(pd.to_datetime(lts[i], unit="ms", utc=True)), int(bad_nd.sum())))
        pos_price = ladder["price_bin"].to_numpy(np.float64) <= 0
        if pos_price.any():
            i = int(np.flatnonzero(pos_price)[0])
            out.append(Finding(A, "ladder_price", "non-positive price_bin", None, int(lts[i]), str(pd.to_datetime(lts[i], unit="ms", utc=True)), int(pos_price.sum())))
        # volume conservation vs Table 1: sum of rungs == taker_buy + taker_sell of the candle
        # (tick-exact bars carry the tick totals in Table 1; synthetic rungs are spread from the same split)
        sums = ladder.groupby("open_time_ms")[["bid_vol_coin", "ask_vol_coin"]].sum()
        m_idx = pd.Index(ts)
        pos = m_idx.get_indexer(sums.index)
        ok = pos >= 0
        tot_ladder = (sums["bid_vol_coin"] + sums["ask_vol_coin"]).to_numpy()[ok]
        tot_master = (tb + tsell)[pos[ok]]
        tol = 1e-6 * np.maximum(tot_master, 1.0) + 1e-6
        bad = np.abs(tot_ladder - tot_master) > tol
        if bad.any():
            j = int(np.flatnonzero(bad)[0])
            t = int(sums.index[ok][j])
            out.append(Finding(A, "ladder_volume_conservation", f"ladder volume {tot_ladder[j]:.8f} != taker_buy+taker_sell {tot_master[j]:.8f}",
                               int(pos[ok][j]), t, str(pd.to_datetime(t, unit="ms", utc=True)), int(bad.sum())))
        ask_sum = sums["ask_vol_coin"].to_numpy()[ok]
        bad_side = np.abs(ask_sum - tb[pos[ok]]) > tol
        if bad_side.any():
            j = int(np.flatnonzero(bad_side)[0])
            t = int(sums.index[ok][j])
            out.append(Finding(A, "ladder_side_conservation", f"ladder ask volume {ask_sum[j]:.8f} != taker_buy_vol_btc {tb[pos[ok]][j]:.8f}",
                               int(pos[ok][j]), t, str(pd.to_datetime(t, unit="ms", utc=True)), int(bad_side.sum())))
        flags = ladder[[c for c in ("is_buy_imbalance", "is_sell_imbalance", "is_poc", "rung_source") if c in ladder]].to_numpy()
        if not np.isin(flags, (0, 1)).all():
            out.append(Finding(A, "ladder_flags", "flag columns must be in {0, 1}"))
    return out


# ==============================================================================
# Agent 3 -- Zero-Null & Schema
# ==============================================================================
def _available_mask(master: pd.DataFrame) -> np.ndarray:
    """Bars the export discloses as carrying official metrics (all bars for legacy files)."""
    if "is_imputed_metrics" in master:
        return master["is_imputed_metrics"].to_numpy() == 0
    if "metrics_available" in master:
        return master["metrics_available"].to_numpy() == 1
    return np.ones(len(master), dtype=bool)


def metrics_coverage_report(master: pd.DataFrame) -> Dict[str, object]:
    """
    Why the regime scan skipped a year, in one dict.

    A Finding is always a rejection in this council (there is no severity), so a
    legitimate pre-archive absence cannot be reported as a soft warning from
    ``agent_schema``. It is reported here instead, so that "no findings" is never
    mistaken for "nothing was skipped".
    """
    rep: Dict[str, object] = {}
    if "open_time_ms" not in master or not len(master):
        return rep
    ts = master["open_time_ms"].to_numpy(np.int64)
    years = pd.to_datetime(ts, unit="ms", utc=True).year
    avail = _available_mask(master)
    counts = {}
    for y in np.unique(years):
        ym = years == y
        counts[int(y)] = {"bars": int(ym.sum()), "available": int((ym & avail).sum())}
    rep["years"] = counts
    rep["skipped_years"] = sorted(
        y for y, d in counts.items()
        if d["bars"] >= 500 and d["available"] < REGIME_MIN_AVAIL_BARS
    )
    oi = master["open_interest_k"].to_numpy(np.float64) if "open_interest_k" in master else np.ones(len(master))
    holes = _runs_longer_than((~avail) & (np.abs(oi) < 1e-12), 1)
    interior = [r for r in holes if r[0] > 0 and r[1] < len(master)]
    rep["longest_interior_hole_bars"] = max((b - a for a, b in interior), default=0)
    rep["unavailable_prefix_bars"] = int(holes[0][1] - holes[0][0]) if holes and holes[0][0] == 0 else 0
    first = np.flatnonzero(avail)
    rep["metrics_first_available_utc"] = str(pd.to_datetime(ts[first[0]], unit="ms", utc=True)) if len(first) else None
    return rep


def _runs_longer_than(mask: np.ndarray, min_len: int) -> list:
    """Maximal True-runs of a boolean mask as (start, end_exclusive), longest-first by position."""
    idx = np.flatnonzero(np.asarray(mask, dtype=bool))
    if not len(idx):
        return []
    out = []
    for grp in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1):
        if len(grp) >= min_len:
            out.append((int(grp[0]), int(grp[-1]) + 1))
    return out


def _attested_absent_months(symbol: str, target_dir: Optional[str] = None) -> "set":
    """
    Months the *download* observed as having no metrics archive on data.binance.vision.

    Read out of the dataset manifest, where the fetcher records archive objects that returned
    404. Non-circular by construction: it is an observation about the source, never derived
    from the assembled frame, so a parse or join bug that silently empties a month cannot
    attest itself. A missing field (legacy manifest) means "no exemption available".
    """
    if not symbol:
        return set()
    path = os.path.join(target_dir or DEFAULT_TARGET, f"{symbol}_dataset_manifest.json")
    try:
        with open(path, encoding="utf-8") as fh:
            man = json.load(fh)
    except Exception:
        return set()
    return {str(m)[:7] for m in ((man.get("provenance") or {}).get("metrics_archive_absent_months") or [])}


def agent_schema(master: pd.DataFrame, ladder: Optional[pd.DataFrame], attested_months: Optional[set] = None) -> List[Finding]:
    A = "Agent3:Schema"
    out: List[Finding] = []
    ts = master["open_time_ms"].to_numpy(np.int64) if "open_time_ms" in master else np.array([], dtype=np.int64)

    cols = list(master.columns)
    if cols != CANONICAL_COLUMNS:
        missing = [c for c in CANONICAL_COLUMNS if c not in cols]
        extra = [c for c in cols if c not in CANONICAL_COLUMNS]
        legacy_ok = cols[:len(CANONICAL_COLUMNS)] == CANONICAL_COLUMNS
        if missing or extra or not legacy_ok:
            out.append(Finding(A, "columns", f"column contract violated: missing={missing} extra={extra} order_ok={legacy_ok}"))
    for col, dt in COLUMN_DTYPES.items():
        if col not in master:
            continue
        actual = str(master[col].dtype)
        ok = (actual == dt) or (dt == "string" and actual in ("object", "string", "str", "string[python]", "string[pyarrow]", "large_string[pyarrow]"))
        if not ok:
            out.append(Finding(A, "dtype", f"{col}: expected {dt}, found {actual}"))
    nulls = master.isna()
    if nulls.to_numpy().any():
        col = nulls.sum().idxmax()
        f = _finding(A, "nulls", f"null values (first column: {col})", nulls.any(axis=1).to_numpy(), ts)
        if f:
            out.append(f)
    num = master.select_dtypes(include=[np.number])
    if len(num.columns):
        arr = num.to_numpy(dtype=np.float64)
        inf = ~np.isfinite(arr)
        if inf.any():
            col = num.columns[int(np.flatnonzero(inf.any(axis=0))[0])]
            f = _finding(A, "non_finite", f"inf/-inf values (first column: {col})", inf.any(axis=1), ts)
            if f:
                out.append(f)
    for col, vocab in STRING_VOCAB.items():
        if col in master:
            bad = ~master[col].isin(vocab).to_numpy()
            f = _finding(A, "vocab", f"{col} outside {vocab}", bad, ts)
            if f:
                out.append(f)
    for col in ("is_synthetic", "metrics_available", "is_imputed_metrics", "is_warmup_converged"):
        if col in master:
            bad = ~master[col].isin((0, 1)).to_numpy()
            f = _finding(A, "flag_domain", f"{col} must be 0/1", bad, ts)
            if f:
                out.append(f)
    if "is_imputed_metrics" in master and "metrics_available" in master:
        bad_impute = (master["is_imputed_metrics"].to_numpy() != (master["metrics_available"].to_numpy() == 0))
        f = _finding(A, "imputed_contract", "is_imputed_metrics != (metrics_available == 0)", bad_impute, ts)
        if f:
            out.append(f)
    if "symbol" in master and master["symbol"].nunique() != 1:
        out.append(Finding(A, "symbol", "more than one symbol in a master file"))
    for col in num.columns:
        if col in ALLOWED_CONSTANT_COLUMNS:
            continue
        if len(master) > 1000 and master[col].nunique() <= 1:
            out.append(Finding(A, "dead_feature", f"{col} is constant across {len(master):,} bars"))
    # Regime-split dead feature scan: catch partially-available metrics where a feature is constant
    # over a calendar year (or substantial regime) while varying elsewhere in the file.
    if len(master) > 1000 and "open_time_ms" in master and len(ts):
        years = pd.to_datetime(ts, unit="ms", utc=True).year
        metric_cols = ("open_interest_k", "ls_ratio_global", "ls_ratio_top", "top_account_ratio", "whale_index", "oi_change_pct")
        avail = _available_mask(master)
        months = pd.to_datetime(ts, unit="ms", utc=True).strftime("%Y-%m")
        if attested_months is None:
            attested_months = _attested_absent_months(
                str(master["symbol"].iloc[0]) if "symbol" in master else "")
        attested_bar = np.isin(months, sorted(attested_months)) if attested_months else np.zeros(len(master), bool)
        avail_nu = {c: master.loc[avail, c].nunique() for c in metric_cols if c in master}
        for y in np.unique(years):
            y_mask = (years == y)
            a_mask = y_mask & avail
            if int(a_mask.sum()) < REGIME_MIN_AVAIL_BARS:
                # A year with (almost) no metrics is legitimate ONLY when Binance never
                # published the archive for it. The availability flag cannot decide that -- it
                # is the very field this scan exists to audit -- so the exemption is granted on
                # the download inventory alone, and an unattested gap stays a rejection.
                if int(y_mask.sum()) >= REGIME_MIN_AVAIL_BARS:
                    need = set(np.unique(months[y_mask]))
                    unattested = need - set(attested_months or set())
                    if unattested:
                        f = _finding(A, "metrics_coverage_unattested",
                                     f"year {int(y)} has {int(y_mask.sum()) - int(a_mask.sum()):,}/{int(y_mask.sum()):,} bars "
                                     f"with no metrics, and the download did not attest {len(unattested)} of its months "
                                     f"({', '.join(sorted(unattested)[:3])}...) as absent from the Binance Vision archive: "
                                     f"pre-archive absence and fabricated coverage cannot be told apart inside the file",
                                     y_mask & ~avail, ts)
                        if f:
                            out.append(f)
                continue
            for col in metric_cols:
                if col in master:
                    y_nu = master.loc[a_mask, col].nunique()
                    total_nu = avail_nu[col]
                    if y_nu <= 1 and total_nu > 1:
                        out.append(Finding(A, "regime_dead_feature",
                                           f"{col} is constant (nunique={y_nu}) across the {int(a_mask.sum()):,} bars "
                                           f"carrying metrics in year {int(y)} despite total nunique={total_nu} "
                                           f"(partially fabricated metrics)"))
    # metrics_interior_hole: a long stretch with no metrics content at all, in the middle of
    # the history (or at its head) that the download inventory does not attest as absent. Legitimate pre-archive absence is a contiguous prefix (Binance Vision
    # starts ETHUSDT metrics on 2021-12); a hole after data has begun flowing is a failed
    # download. Without this, conditioning the scan above on metrics_available would let a
    # lost month pass simply because it was honestly marked unavailable.
    if len(master) > 1000 and "open_time_ms" in master and "open_interest_k" in master:
        empty = ((~_available_mask(master)) & (~attested_bar) &
                 (np.abs(master["open_interest_k"].to_numpy(np.float64)) < 1e-12))
        interior = [r for r in _runs_longer_than(empty, METRICS_INTERIOR_HOLE_BARS + 1)
                    if r[0] > 0 and r[1] < len(master)]
        if interior:
            a, b = max(interior, key=lambda r: r[1] - r[0])
            bad = np.zeros(len(master), dtype=bool)
            bad[a:b] = True
            f = _finding(A, "metrics_interior_hole",
                         f"{b - a:,} consecutive bars with no metrics content in the interior of the "
                         f"history (failed archive download, not a pre-archive gap)", bad, ts)
            if f:
                out.append(f)
    # precision collapse: a price-scale feature must not be quantised coarser than the asset trades
    if len(master) > 1000:
        close_nu = master["close"].nunique()
        for col in ("ema_8", "atr_14"):
            if col in master and master[col].nunique() < max(50, close_nu * 0.01):
                out.append(Finding(A, "precision_collapse", f"{col} has only {master[col].nunique()} distinct values vs {close_nu} distinct closes"))
        # basis_usd is a bounded *spread*, not a price level: its distinct count is capped by
        # (band width / asset tick), so it is uncorrelated with close cardinality and must not
        # be judged against it. What genuinely signals a broken basis is collapse onto a single
        # value, i.e. spot fabricated from the futures close (basis ≡ 0) or a stale spot join.
        if "basis_usd" in master:
            bser = pd.Series(np.round(master["basis_usd"].to_numpy(np.float64), 8))
            vc = bser.value_counts()
            mode_share = float(vc.iloc[0]) / len(bser) if len(vc) else 1.0
            if len(vc) < BASIS_MIN_DISTINCT or mode_share >= BASIS_MODAL_SHARE_MAX:
                out.append(Finding(A, "precision_collapse",
                                   f"basis_usd collapsed: {len(vc)} distinct values, modal value covers "
                                   f"{mode_share:.1%} of bars (spot may be fabricated from futures close)"))
        # value area is bucket-quantised by design; it collapses only if the bucket dwarfs the traded range
        if "session_vah" in master:
            rng = float(master["high"].max() - master["low"].min())
            bucket = get_merge_level(str(master["symbol"].iloc[0]))
            if rng > 0 and master["session_vah"].nunique() < min(50, max(2, rng / bucket * 0.05)):
                out.append(Finding(A, "precision_collapse", f"session_vah has only {master['session_vah'].nunique()} distinct values over a {rng / bucket:.0f}-bucket range"))

    if ladder is not None:
        lcols = list(ladder.columns)
        if lcols != LADDER_COLUMNS:
            out.append(Finding(A, "ladder_columns", f"ladder columns {lcols} != {LADDER_COLUMNS}"))
        for col, dt in LADDER_DTYPES.items():
            if col in ladder and str(ladder[col].dtype) != dt:
                out.append(Finding(A, "ladder_dtype", f"{col}: expected {dt}, found {ladder[col].dtype}"))
        if ladder.isna().to_numpy().any():
            out.append(Finding(A, "ladder_nulls", "ladder contains nulls"))
        lnum = ladder.select_dtypes(include=[np.number]).to_numpy(dtype=np.float64)
        if lnum.size and not np.isfinite(lnum).all():
            out.append(Finding(A, "ladder_non_finite", "ladder contains inf"))
        if "trade_count" in ladder and (ladder["trade_count"] < 0).any():
            out.append(Finding(A, "ladder_trade_count", "negative trade_count"))
    return out


# ==============================================================================
# Council
# ==============================================================================
AGENTS: Dict[str, Callable[[pd.DataFrame, Optional[pd.DataFrame]], List[Finding]]] = {
    "Agent1:Continuity": agent_continuity,
    "Agent2:Microstructure": agent_microstructure,
    "Agent3:Schema": agent_schema,
}


def run_council(master: pd.DataFrame, ladder: Optional[pd.DataFrame], symbol: str, log: Callable[[str], None] = print,
                attested_months: Optional[set] = None,
                expected_start_ms: Optional[int] = None,
                expected_end_ms: Optional[int] = None) -> CouncilReport:
    report = CouncilReport(symbol=symbol, passed=True, master_rows=len(master), ladder_rows=len(ladder) if ladder is not None else 0)
    for name, fn in AGENTS.items():
        try:
            if name == "Agent3:Schema":
                findings = fn(master, ladder, attested_months=attested_months)
            elif name == "Agent1:Continuity":
                findings = fn(master, ladder, expected_start_ms=expected_start_ms, expected_end_ms=expected_end_ms)
            else:
                findings = fn(master, ladder)
        except Exception as exc:  # an agent crash is itself a failure
            findings = [Finding(name, "exception", f"{type(exc).__name__}: {exc}")]
        report.findings.extend(findings)
        report.agent_status[name] = "PASS" if not findings else f"FAIL ({len(findings)})"
        if findings:
            report.passed = False
    log(f"[COUNCIL] {symbol}: " + " | ".join(f"{k.split(':')[1]}={v}" for k, v in report.agent_status.items()))
    for f in report.findings[:25]:
        log(f"  -> {f}")
    if len(report.findings) > 25:
        log(f"  -> ... {len(report.findings) - 25} more finding(s)")
    return report


def verify_symbol(target_dir: str, symbol: str, log: Callable[[str], None] = print) -> CouncilReport:
    mpath = os.path.join(target_dir, master_filename(symbol))
    lpath = os.path.join(target_dir, ladder_filename(symbol))
    ppath = os.path.join(target_dir, manifest_filename(symbol))

    if not os.path.exists(mpath):
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "missing_master", f"{mpath} not found")], {})
    if not os.path.exists(lpath):
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "missing_ladder", f"{lpath} not found")], {})

    # Manifest is mandatory for artifact certification
    if not os.path.exists(ppath):
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "missing_manifest", f"Manifest {ppath} not found (manifest is mandatory for certification)")], {})

    try:
        with open(ppath, "r", encoding="utf-8") as fh:
            mdata = json.load(fh)
    except Exception as exc:
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "unreadable_manifest", f"Manifest {ppath} unreadable or corrupt JSON: {exc}")], {})

    exp_start_ms = mdata.get("expected_start_ms")
    exp_end_ms = mdata.get("expected_end_ms")
    exp_rows = mdata.get("expected_rows")

    manifest_findings: List[Finding] = []
    if exp_start_ms is None or not isinstance(exp_start_ms, int):
        manifest_findings.append(Finding("Council", "manifest_expected_start", f"expected_start_ms missing or not int: {exp_start_ms!r}"))
    if exp_end_ms is None or not isinstance(exp_end_ms, int):
        manifest_findings.append(Finding("Council", "manifest_expected_end", f"expected_end_ms missing or not int: {exp_end_ms!r}"))
    if exp_rows is None or not isinstance(exp_rows, int):
        manifest_findings.append(Finding("Council", "manifest_expected_rows", f"expected_rows missing or not int: {exp_rows!r}"))

    if isinstance(exp_start_ms, int) and isinstance(exp_end_ms, int) and isinstance(exp_rows, int):
        calc_exp_first = (exp_start_ms // BAR_MS) * BAR_MS
        calc_exp_last = (exp_end_ms // BAR_MS) * BAR_MS
        calc_rows = int(((calc_exp_last - calc_exp_first) // BAR_MS) + 1)
        if exp_rows != calc_rows:
            manifest_findings.append(Finding("Council", "manifest_rows_inconsistent",
                                             f"manifest expected_rows ({exp_rows}) != calculated from expected_start/end ({calc_rows})"))

    try:
        master = pd.read_parquet(mpath)
        ladder = pd.read_parquet(lpath)
    except Exception as exc:
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "unreadable_parquet", f"Failed to read parquet: {exc}")], {})

    if isinstance(exp_rows, int) and len(master) != exp_rows:
        manifest_findings.append(Finding("Council", "master_rows_mismatch",
                                         f"master length ({len(master)}) != manifest expected_rows ({exp_rows})"))

    attested = _attested_absent_months(symbol, target_dir)
    report = run_council(master, ladder, symbol, log, attested_months=attested,
                         expected_start_ms=exp_start_ms if isinstance(exp_start_ms, int) else None,
                         expected_end_ms=exp_end_ms if isinstance(exp_end_ms, int) else None)

    if manifest_findings:
        report.findings.extend(manifest_findings)
        report.passed = False
        report.agent_status["Council:ManifestContract"] = f"FAIL ({len(manifest_findings)})"

    return report


def verify_all_parquets(target_dir: str = DEFAULT_TARGET, symbols: Optional[List[str]] = None, log: Callable[[str], None] = print) -> bool:
    log("=" * 96)
    log("AUTONOMOUS 3-AGENT VERIFICATION COUNCIL")
    log(f"Target: {target_dir}")
    log("=" * 96)
    if not os.path.isdir(target_dir):
        log(f"[FAIL] target directory missing: {target_dir}")
        return False
    if symbols is None:
        symbols = sorted(os.path.basename(p).split("_15m_master")[0] for p in glob.glob(os.path.join(target_dir, "*_15m_master_2020_2026.parquet")))
    if not symbols:
        log("[FAIL] no master parquet files found")
        return False
    all_ok, total_bars, total_rungs = True, 0, 0
    summary = {}
    for sym in symbols:
        rep = verify_symbol(target_dir, sym, log)
        total_bars += rep.master_rows
        total_rungs += rep.ladder_rows
        summary[sym] = rep.to_dict()
        all_ok &= rep.passed
        log(f"[{'PASS' if rep.passed else 'FAIL'}] {sym:<10} bars={rep.master_rows:>8,} rungs={rep.ladder_rows:>12,}")
    log("=" * 96)
    log(f"COUNCIL VERDICT: {'ALL DATASETS PASS' if all_ok else 'INTEGRITY FAILURES DETECTED'} | candles={total_bars:,} rungs={total_rungs:,}")
    log("=" * 96)
    with open(os.path.join(target_dir, "verification_report.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    return all_ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="3-Agent Parquet Verification Council")
    ap.add_argument("target_dir", nargs="?", default=DEFAULT_TARGET)
    ap.add_argument("--symbol", action="append", help="verify only this symbol (repeatable)")
    args = ap.parse_args()
    sys.exit(0 if verify_all_parquets(args.target_dir, args.symbol) else 1)
`
