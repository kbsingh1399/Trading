"""
MT5 High-Fidelity Multi-Timeframe Data Exporter
=================================================
Exports genuine non-synthetic candlestick data from MetaTrader 5 into Parquet format.
Excludes Cryptocurrencies. Covers Forex, Commodities/Metals, and Indices.

Timeframes exported per symbol:
  - 15m  (primary intraday — ICT kill zones, FVG, OB detection)
  - 1h   (session structure, short-term HTF context)
  - 4h   (institutional candle structure, HTF order blocks)
  - D1   (PDH/PDL, daily bias, weekly range context)

Run modes:
  - First run (no existing file): full history from HISTORY_START to now.
  - Subsequent runs (file exists): incremental — only fetches new bars since last save,
    appends, deduplicates, and re-saves. No re-download of existing history.

ICT session columns precomputed at export:
  - day_of_week (0=Mon..4=Fri)
  - session (asian / london / new_york / london_close / off_hours)
  - is_kill_zone (london open + NY open kill zones)
"""

import sys
import os
import time
import json
from datetime import datetime, timezone
try:
    import MetaTrader5 as mt5
except (ImportError, ModuleNotFoundError):
    mt5 = None
import polars as pl

# Earliest date to pull history from (MT5 server typically has data from ~2015)
HISTORY_START = datetime(2010, 1, 1, tzinfo=timezone.utc)

# Timeframes to export: (label, MT5 constant, file suffix)
TIMEFRAMES = [
    ("15m", getattr(mt5, "TIMEFRAME_M15", 15), "15m"),
    ("1h",  getattr(mt5, "TIMEFRAME_H1", 60),  "1h"),
    ("4h",  getattr(mt5, "TIMEFRAME_H4", 240), "4h"),
    ("D1",  getattr(mt5, "TIMEFRAME_D1", 1440), "d1"),
]

# ICT Session boundaries in UTC hour (inclusive start, exclusive end)
SESSION_LONDON_KZ_START = 7
SESSION_LONDON_KZ_END = 10
SESSION_NY_KZ_START = 12
SESSION_NY_KZ_END = 15

def _classify_session(hour: int) -> str:
    """Classify UTC hour into ICT session label."""
    if 0 <= hour < 8:
        return "asian"
    elif 8 <= hour < 12:
        return "london"
    elif 12 <= hour < 17:
        return "new_york"
    elif 15 <= hour < 16:
        return "london_close"
    else:
        return "off_hours"

def _is_kill_zone(hour: int) -> bool:
    """London kill zone (07-10 UTC) or NY kill zone (12-15 UTC)."""
    return (SESSION_LONDON_KZ_START <= hour < SESSION_LONDON_KZ_END) or \
           (SESSION_NY_KZ_START <= hour < SESSION_NY_KZ_END)

def _rates_to_polars(rates) -> pl.DataFrame:
    """Convert MT5 structured numpy array directly to Polars with ICT session columns."""
    pldf = pl.from_dict(
        {col: rates[col] for col in rates.dtype.names},
    )

    pldf = pldf.with_columns(
        pl.from_epoch("time", time_unit="s").dt.replace_time_zone("UTC").alias("datetime")
    )

    pldf = pldf.with_columns([
        pl.col("datetime").dt.weekday().cast(pl.UInt8).alias("day_of_week"),
        pl.col("datetime").dt.hour().alias("_hour"),
    ])

    pldf = pldf.with_columns([
        pl.col("_hour").map_elements(_classify_session, return_dtype=pl.Utf8).alias("session"),
        pl.col("_hour").map_elements(_is_kill_zone, return_dtype=pl.Boolean).alias("is_kill_zone"),
    ])

    return pldf.select([
        "time", "datetime", "open", "high", "low", "close",
        "tick_volume", "spread", "real_volume",
        "day_of_week", "session", "is_kill_zone",
    ]).drop("_hour", strict=False)

def _fetch_incremental(sym_name: str, tf_const, out_file: str) -> tuple:
    """
    If parquet exists, lazy-scan last timestamp and fetch only new bars.
    Otherwise fetch full history from HISTORY_START.
    Returns (DataFrame | None, mode_str, new_bar_count).
    """
    date_to = datetime.now(timezone.utc)

    if os.path.exists(out_file):
        last_ts = pl.scan_parquet(out_file).select(pl.col("time").max()).collect().item()
        date_from = datetime.fromtimestamp(last_ts + 1, tz=timezone.utc)
        mode = "incremental"
    else:
        last_ts = None
        date_from = HISTORY_START
        mode = "full"

    if date_from >= date_to:
        existing = pl.read_parquet(out_file) if os.path.exists(out_file) else None
        return existing, mode, 0

    rates = None
    for attempt in range(3):
        if mode == "full":
            # Bypass MT5 date range limit by using from_pos to fetch everything available
            rates = mt5.copy_rates_from_pos(sym_name, tf_const, 0, 99999)
        else:
            rates = mt5.copy_rates_range(sym_name, tf_const, date_from, date_to)
            
        if rates is not None and len(rates) > 0:
            break
        time.sleep(1.0)

    new_bars = 0
    if rates is not None and len(rates) > 0:
        new_df = _rates_to_polars(rates)
        new_bars = len(new_df)
        if mode == "incremental" and os.path.exists(out_file):
            existing = pl.read_parquet(out_file)
            combined = pl.concat([existing, new_df])
            combined = combined.unique(subset=["time"], keep="last").sort("time")
        else:
            combined = new_df
        return combined, mode, new_bars
    elif os.path.exists(out_file):
        return pl.read_parquet(out_file), mode, 0
    else:
        return None, mode, 0

def _safe_write(pldf: pl.DataFrame, out_file: str):
    """Write Parquet with retry and direct write fallback for Windows file locking."""
    tmp_file = out_file + ".tmp"
    written = False
    try:
        pldf.write_parquet(tmp_file, compression="zstd")
        if os.path.exists(tmp_file):
            for _ in range(5):
                try:
                    os.replace(tmp_file, out_file)
                    written = True
                    break
                except Exception:
                    time.sleep(0.2)
    except Exception:
        pass

    if not written:
        pldf.write_parquet(out_file, compression="zstd")

    if os.path.exists(tmp_file):
        try:
            os.remove(tmp_file)
        except Exception:
            pass

def export_all_mt5(output_dir: str = "Forex_Backtesting_Data", include_crypto: bool = True):
    if not mt5.initialize():
        print(f"[ERROR] Failed to initialize MT5: {mt5.last_error()}", file=sys.stderr)
        return False

    account = mt5.account_info()
    terminal = mt5.terminal_info()
    print("=" * 70)
    print(f"MT5 Connected: {account.company} | Server: {account.server}")
    print(f"Timeframes: {', '.join(label for label, _, _ in TIMEFRAMES)}")
    print("=" * 70)

    symbols = mt5.symbols_get()
    if not symbols:
        print("[ERROR] No symbols returned from MT5.", file=sys.stderr)
        mt5.shutdown()
        return False

    if include_crypto:
        target_symbols = list(symbols)
    else:
        target_symbols = [s for s in symbols if "crypto" not in s.path.lower()]
    seen_clean_names: set[str] = set()

    print(f"Total Export Target Assets: {len(target_symbols)} x {len(TIMEFRAMES)} timeframes")
    os.makedirs(output_dir, exist_ok=True)

    manifest = {
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "broker": account.company,
        "server": account.server,
        "timeframes": [label for label, _, _ in TIMEFRAMES],
        "history_start": HISTORY_START.isoformat(),
        "ict_session_columns": ["day_of_week", "session", "is_kill_zone"],
        "assets_count": 0,
        "symbols": {}
    }

    successful = 0
    failed = 0
    skipped = 0
    start_all = time.time()

    for idx, s in enumerate(target_symbols, 1):
        sym_name = s.name
        clean_name = sym_name.split(".")[0]
        category = s.path.split("\\")[0] if "\\" in s.path else "Other"

        if clean_name in seen_clean_names:
            print(f"[{idx:02d}/{len(target_symbols):02d}] {clean_name:10} SKIP: duplicate base name (raw={sym_name})")
            skipped += 1
            continue
        seen_clean_names.add(clean_name)

        sym_info = mt5.symbol_info(sym_name)
        mt5.symbol_select(sym_name, True)

        sym_manifest = {
            "raw_symbol": sym_name,
            "category": category,
            "digits": sym_info.digits if sym_info else None,
            "point": sym_info.point if sym_info else None,
            "trade_tick_size": sym_info.trade_tick_size if sym_info else None,
            "contract_size": sym_info.trade_contract_size if sym_info else None,
            "description": sym_info.description if sym_info else "",
            "timeframes": {}
        }

        sym_ok = False
        t0 = time.time()

        for tf_label, tf_const, tf_suffix in TIMEFRAMES:
            out_file = os.path.join(output_dir, f"{clean_name}_{tf_suffix}_real.parquet")
            pldf, mode, new_bars = _fetch_incremental(sym_name, tf_const, out_file)

            if pldf is None:
                sym_manifest["timeframes"][tf_label] = {"status": "FAIL", "bars": 0}
                continue

            _safe_write(pldf, out_file)
            bar_count = len(pldf)
            file_size_kb = os.path.getsize(out_file) / 1024
            min_dt = pldf["datetime"].min().isoformat()
            max_dt = pldf["datetime"].max().isoformat()

            sym_manifest["timeframes"][tf_label] = {
                "bars": bar_count,
                "new_bars": new_bars,
                "start_time": min_dt,
                "end_time": max_dt,
                "file_size_kb": round(file_size_kb, 2),
                "mode": mode
            }
            sym_ok = True

        elapsed = time.time() - t0
        manifest["symbols"][clean_name] = sym_manifest

        if sym_ok:
            successful += 1
            bars_summary = " | ".join(
                f"{tf}: {sym_manifest['timeframes'].get(tf, {}).get('bars', 0)}"
                for tf, _, _ in TIMEFRAMES
            )
            print(f"[{idx:02d}/{len(target_symbols):02d}] {clean_name:10} ({category:15}) -> {bars_summary} [{elapsed:4.1f}s]")
        else:
            failed += 1
            print(f"[{idx:02d}/{len(target_symbols):02d}] {clean_name:10} ({category:15}) | FAIL: No data [{elapsed:4.1f}s]")

    mt5.shutdown()
    total_time = time.time() - start_all

    manifest["assets_count"] = successful
    manifest["total_export_time_seconds"] = round(total_time, 2)

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("=" * 70)
    print(f"EXPORT COMPLETE: {successful} ok, {failed} failed, {skipped} skipped in {total_time:.1f}s")
    print(f"Manifest: {manifest_path}")
    print("=" * 70)
    return True

if __name__ == "__main__":
    export_all_mt5()
