"""
MT5 High-Fidelity Crypto Multi-Timeframe Data Exporter
======================================================
Exports genuine crypto candlestick data from MetaTrader 5 into Parquet format.
Target Crypto Basket:
  - BTCUSD (.pi / .p)
  - ETHUSD (.pi / .p)
  - SOLUSD (.pi / .p)
  - XRPUSD (.pi / .p)
  - BNBUSD (.pi / .p)
  - LTCUSD (.pi / .p)
  - ADAUSD (.pi / .p)
  - DOTUSD (.pi / .p)
  - BCHUSD (.pi / .p)

Timeframes exported per symbol:
  - 15m  (primary intraday — ICT kill zones, FVG, OB detection)
  - 1h   (session structure, short-term HTF context)
  - 4h   (institutional candle structure, HTF order blocks)
  - D1   (PDH/PDL, daily bias, weekly range context)

Output Directory: Forex_Backtesting_Data/
File naming: {clean_name}_{tf_suffix}_real.parquet (e.g. BTCUSD_15m_real.parquet)

ICT session columns precomputed at export:
  - day_of_week (0=Mon..6=Sun for Crypto 24/7)
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

# Earliest date to pull history from
HISTORY_START = datetime(2015, 1, 1, tzinfo=timezone.utc)

# Timeframes to export: (label, MT5 constant, file suffix)
TIMEFRAMES = [
    ("15m", getattr(mt5, "TIMEFRAME_M15", 15), "15m"),
    ("1h",  getattr(mt5, "TIMEFRAME_H1", 60),  "1h"),
    ("4h",  getattr(mt5, "TIMEFRAME_H4", 240), "4h"),
    ("D1",  getattr(mt5, "TIMEFRAME_D1", 1440), "d1"),
]

# Target crypto base pairs and expected raw symbols
TARGET_CRYPTO_BASE = [
    "BTCUSD", "ETHUSD", "SOLUSD", "XRPUSD", "BNBUSD",
    "LTCUSD", "ADAUSD", "DOTUSD", "BCHUSD"
]

CANDIDATE_SUFFIXES = [".pi", ".p", "", "_i", ".m"]

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
        try:
            last_ts = pl.scan_parquet(out_file).select(pl.col("time").max()).collect().item()
            if last_ts is not None:
                date_from = datetime.fromtimestamp(last_ts + 1, tz=timezone.utc)
                mode = "incremental"
            else:
                last_ts = None
                date_from = HISTORY_START
                mode = "full"
        except Exception:
            last_ts = None
            date_from = HISTORY_START
            mode = "full"
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
            rates = mt5.copy_rates_from_pos(sym_name, tf_const, 0, 99999)
            if rates is None or len(rates) == 0:
                rates = mt5.copy_rates_range(sym_name, tf_const, date_from, date_to)
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
            try:
                existing = pl.read_parquet(out_file)
                combined = pl.concat([existing, new_df])
                combined = combined.unique(subset=["time"], keep="last").sort("time")
            except Exception:
                combined = new_df
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

def resolve_crypto_symbols() -> dict[str, str]:
    """
    Map clean base name (e.g. BTCUSD) to detected MT5 raw symbol name (e.g. BTCUSD.pi).
    """
    all_symbols = mt5.symbols_get()
    if not all_symbols:
        return {}

    available_names = {s.name: s for s in all_symbols}
    resolved = {}

    for base in TARGET_CRYPTO_BASE:
        # Check specific candidates first
        found = False
        for suffix in CANDIDATE_SUFFIXES:
            cand = f"{base}{suffix}"
            if cand in available_names:
                resolved[base] = cand
                found = True
                break
        
        # If not found, fuzzy match symbol whose clean name matches
        if not found:
            for name in available_names:
                clean = name.split(".")[0].upper()
                if clean == base.upper():
                    resolved[base] = name
                    found = True
                    break

    return resolved

def export_all_mt5_crypto(output_dir: str = "Forex_Backtesting_Data"):
    if not mt5.initialize():
        print(f"[ERROR] Failed to initialize MT5: {mt5.last_error()}", file=sys.stderr)
        return False

    account = mt5.account_info()
    print("=" * 70)
    print(f"MT5 Connected: {account.company if account else 'Unknown'} | Server: {account.server if account else 'Unknown'}")
    print(f"Target Crypto Assets: {', '.join(TARGET_CRYPTO_BASE)}")
    print(f"Timeframes: {', '.join(label for label, _, _ in TIMEFRAMES)}")
    print("=" * 70)

    resolved_map = resolve_crypto_symbols()
    print(f"Detected {len(resolved_map)} / {len(TARGET_CRYPTO_BASE)} Crypto Assets:")
    for base, raw in resolved_map.items():
        print(f"  - {base:8} -> {raw}")

    missing = set(TARGET_CRYPTO_BASE) - set(resolved_map.keys())
    if missing:
        print(f"[WARN] Missing crypto assets on MT5 server: {missing}")

    os.makedirs(output_dir, exist_ok=True)

    manifest_crypto = {
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "broker": account.company if account else "Unknown",
        "server": account.server if account else "Unknown",
        "timeframes": [label for label, _, _ in TIMEFRAMES],
        "history_start": HISTORY_START.isoformat(),
        "ict_session_columns": ["day_of_week", "session", "is_kill_zone"],
        "assets_count": 0,
        "symbols": {}
    }

    successful = 0
    failed = 0
    start_all = time.time()

    for idx, (clean_name, raw_symbol) in enumerate(resolved_map.items(), 1):
        sym_info = mt5.symbol_info(raw_symbol)
        mt5.symbol_select(raw_symbol, True)

        sym_manifest = {
            "raw_symbol": raw_symbol,
            "category": "Crypto",
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
            pldf, mode, new_bars = _fetch_incremental(raw_symbol, tf_const, out_file)

            if pldf is None or len(pldf) == 0:
                sym_manifest["timeframes"][tf_label] = {"status": "FAIL", "bars": 0}
                continue

            if not (mode == "incremental" and new_bars == 0 and os.path.exists(out_file)):
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
                "mode": mode,
                "file_path": out_file
            }
            sym_ok = True

        elapsed = time.time() - t0
        manifest_crypto["symbols"][clean_name] = sym_manifest

        if sym_ok:
            successful += 1
            bars_summary = " | ".join(
                f"{tf}: {sym_manifest['timeframes'].get(tf, {}).get('bars', 0)}"
                for tf, _, _ in TIMEFRAMES
            )
            print(f"[{idx:02d}/{len(resolved_map):02d}] {clean_name:8} ({raw_symbol:12}) -> {bars_summary} [{elapsed:4.1f}s]")
        else:
            failed += 1
            print(f"[{idx:02d}/{len(resolved_map):02d}] {clean_name:8} ({raw_symbol:12}) | FAIL: No data [{elapsed:4.1f}s]")

    mt5.shutdown()
    total_time = time.time() - start_all

    manifest_crypto["assets_count"] = successful
    manifest_crypto["total_export_time_seconds"] = round(total_time, 2)

    manifest_path = os.path.join(output_dir, "manifest_crypto.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_crypto, f, indent=2)

    print("=" * 70)
    print(f"CRYPTO EXPORT COMPLETE: {successful} ok, {failed} failed in {total_time:.1f}s")
    print(f"Manifest: {manifest_path}")
    print("=" * 70)
    return successful > 0

if __name__ == "__main__":
    export_all_mt5_crypto()
