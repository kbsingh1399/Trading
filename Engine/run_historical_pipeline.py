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
from typing import Callable, Dict, List, Optional

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
from Engine.pipeline.binance_historical_fetcher import BinanceHistoricalFetcher  # noqa: E402
from Engine.pipeline.footprint_ladder import assemble_ladder  # noqa: E402
from Engine.pipeline.historical_metrics_processor import HistoricalMetricsProcessor  # noqa: E402
from Engine.pipeline.http_client import HttpClient  # noqa: E402
from Engine.pipeline.parquet_exporter import ParquetExporter, SchemaError  # noqa: E402
from Engine.pipeline.tick_footprint_fetcher import TickFootprintFetcher  # noqa: E402
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
def existing_output_is_current(target_dir: str, symbol: str, max_age_hours: float) -> bool:
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
            expected_rows = manifest_data.get("total_rows")
    except Exception:
        return False
    try:
        mf = pq.ParquetFile(mpath)
        if mf.schema_arrow.names != CANONICAL_COLUMNS:
            return False
        has_ladder = os.path.exists(lpath)
        if has_ladder:
            lf = pq.ParquetFile(lpath)
            if lf.schema_arrow.names != LADDER_COLUMNS:
                return False
        if expected_rows is not None and mf.metadata.num_rows != expected_rows:
            return False
        last = mf.read_row_group(mf.num_row_groups - 1, columns=["close_time_ms"]).column(0).to_numpy()
        now_utc_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        age_h = max(0.0, (now_utc_ms - int(last[-1])) / 3_600_000)
        if age_h > max_age_hours:
            return False
        m_ts = pd.read_parquet(mpath, columns=["open_time_ms"])["open_time_ms"].to_numpy()
        if has_ladder:
            l_ts = pd.read_parquet(lpath, columns=["open_time_ms"])["open_time_ms"].unique()
            if not (np.isin(m_ts, l_ts).all() and np.isin(l_ts, m_ts).all()):
                return False
        return bool(m_ts.size > 1000)
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
    for root, _, files in os.walk(cache_dir):
        for f in files:
            f_lower = f.lower()
            if sym_lower in f_lower or sym_upper in f or f.endswith(".tmp"):
                p = os.path.join(root, f)
                try:
                    os.remove(p)
                    removed += 1
                except OSError:
                    pass
    if removed > 0:
        log(f"[CLEANUP] continuous raw cleanup: removed {removed} intermediate cache files for {symbol} from {cache_dir}")
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

    if {"ladder_coverage", "ladder_orphans", "ladder_poc", "ladder_dup_rung", "ladder_volume_conservation"} & checks:
        ladder, stats = assemble_ladder(m, ladder[ladder["rung_source"] == 0] if "rung_source" in ladder else None)
        # candles whose exact rungs failed conservation/POC are rebuilt synthetically
        bad_ts = {f.open_time_ms for f in report.findings if f.check in ("ladder_poc", "ladder_volume_conservation") and f.open_time_ms}
        if bad_ts:
            keep = ladder[~ladder["open_time_ms"].isin(bad_ts)]
            ladder, stats = assemble_ladder(m, keep[keep["rung_source"] == 0] if "rung_source" in keep else None)
        changed = True
        log(f"  [REPAIR] ladder re-assembled: {stats}")

    return m, ladder, changed


# ------------------------------------------------------------------------------
# Per-symbol pipeline
# ------------------------------------------------------------------------------
def run_pipeline(
    symbol: str = "BTCUSDT",
    start_date_str: str = DEFAULT_START_DATE,
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
    warmup_start = max(_parse_date(WARMUP_START_DATE), listing)
    now = datetime.now(timezone.utc)

    if not force and existing_output_is_current(target_dir, symbol, skip_if_fresh_hours):
        log(f"[SKIP] {symbol}: existing dual-table output satisfies contract and is < {skip_if_fresh_hours:.0f}h old")
        return True

    log("=" * 96)
    log(f"PIPELINE {symbol} | slice from {effective_start:%Y-%m-%d} | warm-up from {warmup_start:%Y-%m-%d} | workers={max_workers}")
    log("=" * 96)

    http = HttpClient()
    fetcher = BinanceHistoricalFetcher(cache_dir=cache_dir, max_workers=max_workers, http=http, log=log)

    t0 = time.time()
    klines = fetcher.fetch_futures_klines(symbol, warmup_start.strftime("%Y-%m-%d"), now)
    spot = fetcher.fetch_spot_klines(symbol, warmup_start.strftime("%Y-%m-%d"), now)
    metrics = fetcher.fetch_metrics(symbol, effective_start.strftime("%Y-%m-%d"), now)
    funding = fetcher.fetch_funding_rates(symbol, int(warmup_start.timestamp() * 1000))
    log(f"[OK] {symbol}: streams fetched in {time.time() - t0:.1f}s | http={http.stats}")

    fp_summary, fp_ladder = pd.DataFrame(), pd.DataFrame()
    if all_footprint or footprint_days > 0:
        fp_start = effective_start if all_footprint else max(effective_start, now - pd.Timedelta(days=footprint_days))
        fpf = TickFootprintFetcher(cache_dir=cache_dir, max_workers=max(1, max_workers // 2), log=log)
        fp_summary, fp_ladder = fpf.fetch_footprint(symbol, fp_start.strftime("%Y-%m-%d"), now=now)

    t1 = time.time()
    processor = HistoricalMetricsProcessor(log=log)
    master = processor.process_master_dataset(
        klines, metrics, funding, fp_summary, spot, symbol=symbol,
        export_start_ms=int(effective_start.timestamp() * 1000),
    )
    log(f"[OK] {symbol}: {len(master):,} bars x {len(master.columns)} cols computed in {time.time() - t1:.1f}s "
        f"({master['datetime_utc'].iloc[0]} -> {master['datetime_utc'].iloc[-1]})")

    t2 = time.time()
    ladder, ladder_stats = assemble_ladder(master, fp_ladder if not fp_ladder.empty else None)
    log(f"[OK] {symbol}: ladder assembled in {time.time() - t2:.1f}s | {ladder_stats}")

    # ------------------------------------------------------------ council gate
    attested_months = None
    if hasattr(fetcher, "metrics_absent_days") and fetcher.metrics_absent_days:
        attested_months = {d[:7] for d in fetcher.metrics_absent_days}

    report = run_council(master, ladder, symbol, log, attested_months=attested_months)
    rounds = 0
    while not report.passed and rounds < MAX_REPAIR_ROUNDS:
        rounds += 1
        log(f"[GATE] {symbol}: council FAILED -> causal repair round {rounds}/{MAX_REPAIR_ROUNDS}")
        master, ladder, changed = causal_repair(master, ladder, report, log)
        if not changed:
            log(f"[GATE] {symbol}: no applicable causal repair for {sorted({f.check for f in report.findings})}")
            break
        report = run_council(master, ladder, symbol, log, attested_months=attested_months)

    if not report.passed:
        log(f"[REJECT] {symbol}: export refused. {len(report.findings)} finding(s):")
        for f in report.findings[:50]:
            log(f"    {f}")
        return False

    # ------------------------------------------------------------ export
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
        manifest_path = exporter.write_manifest(master, symbol, ladder_stats, {**report.to_dict(), "repair_rounds": rounds},
                                                metrics_absent_days=getattr(fetcher, "metrics_absent_days", None))
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
    ap.add_argument("--target-dir", default=DEFAULT_TARGET_DIR)
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--footprint-days", type=int, default=0, help="days of aggTrades tick footprint to fetch (0 = none)")
    ap.add_argument("--all-footprint", action="store_true", help="fetch aggTrades for the full slice")
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
                symbol=sym, start_date_str=args.start_date, target_dir=args.target_dir, cache_dir=args.cache_dir,
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
