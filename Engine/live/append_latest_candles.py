"""
Append latest candles from MT5 live server to existing Forex_Backtesting_Data parquets.
Brings every parquet file up to the last closed 15m candle.
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
try:
    import MetaTrader5 as mt5
except (ImportError, ModuleNotFoundError):
    mt5 = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data")

# Target cutoff: 14:15 IST Sep 15 2026 = 08:45 UTC Sep 15 2026
IST = timezone(timedelta(hours=5, minutes=30))
CUTOFF_IST = datetime(2026, 9, 15, 14, 15, 0, tzinfo=IST)
CUTOFF_UTC = CUTOFF_IST.astimezone(timezone.utc)
print(f"Target cutoff: {CUTOFF_IST.strftime('%Y-%m-%d %H:%M IST')} = {CUTOFF_UTC.strftime('%Y-%m-%d %H:%M UTC')}")

# Timeframe map
TF_MAP = {
    "15m": getattr(mt5, "TIMEFRAME_M15", 15),
    "1h":  getattr(mt5, "TIMEFRAME_H1", 60),
    "4h":  getattr(mt5, "TIMEFRAME_H4", 240),
    "d1":  getattr(mt5, "TIMEFRAME_D1", 1440),
}

def get_mt5_symbol(parquet_name):
    """Map parquet base name (e.g. EURHUF) to MT5 symbol (e.g. EURHUF.pi)"""
    for suffix in ['.pi', '.p', '']:
        sym = parquet_name + suffix
        info = mt5.symbol_info(sym)
        if info is not None:
            if not info.visible:
                mt5.symbol_select(sym, True)
            return sym
    return None

def get_broker_utc_offset():
    """Calculates broker server time offset from UTC in seconds."""
    tick = mt5.symbol_info_tick("EURUSD.pi") or mt5.symbol_info_tick("EURUSD") or mt5.symbol_info_tick("EURUSD.p")
    if tick is None:
        return 3 * 3600
    now_utc_ts = datetime.now(timezone.utc).timestamp()
    return int(round((tick.time - now_utc_ts) / 3600.0) * 3600)

TF_DELTA = {
    "15m": timedelta(minutes=15),
    "1h":  timedelta(hours=1),
    "4h":  timedelta(hours=4),
    "d1":  timedelta(days=1),
}

def append_candles_for_file(parquet_path, mt5_symbol, tf_key, cutoff_utc):
    """Read existing parquet, fetch new bars from MT5, append, save."""
    tf_mt5 = TF_MAP[tf_key]
    tf_delta = TF_DELTA[tf_key]
    broker_offset = get_broker_utc_offset()
    
    df_existing = pd.read_parquet(parquet_path)
    
    if 'datetime' in df_existing.columns:
        last_dt = pd.to_datetime(df_existing['datetime'].max())
        if last_dt.tzinfo is None:
            last_dt = last_dt.tz_localize('UTC')
    elif 'time' in df_existing.columns:
        last_ts = df_existing['time'].max()
        last_dt = pd.to_datetime(last_ts, unit='s', utc=True)
    else:
        print(f"  [SKIP] No datetime/time column in {parquet_path}")
        return 0
    
    fetch_from = last_dt + timedelta(seconds=1)
    # Query MT5 in broker server time
    fetch_from_broker = fetch_from + timedelta(seconds=broker_offset)
    cutoff_broker = cutoff_utc + timedelta(seconds=broker_offset)
    
    rates = mt5.copy_rates_range(mt5_symbol, tf_mt5, fetch_from_broker, cutoff_broker)
    
    if rates is None or len(rates) == 0:
        return 0
    
    df_new = pd.DataFrame(rates)
    # Convert broker server timestamp to true UTC
    df_new['time'] = df_new['time'] - broker_offset
    df_new['datetime'] = pd.to_datetime(df_new['time'], unit='s', utc=True)
    
    # Strictly enforce: bar open + duration <= cutoff (only fully completed bars)
    df_new = df_new[df_new['datetime'] + tf_delta <= cutoff_utc]
    
    if len(df_new) == 0:
        return 0
    
    existing_cols = df_existing.columns.tolist()
    
    new_rows = pd.DataFrame()
    new_rows['time'] = df_new['time'].values
    new_rows['datetime'] = df_new['datetime'].values
    new_rows['open'] = df_new['open'].values
    new_rows['high'] = df_new['high'].values
    new_rows['low'] = df_new['low'].values
    new_rows['close'] = df_new['close'].values
    new_rows['tick_volume'] = df_new['tick_volume'].astype(np.uint64).values
    new_rows['spread'] = df_new['spread'].astype(np.int32).values
    new_rows['real_volume'] = df_new['real_volume'].astype(np.uint64).values
    
    if 'day_of_week' in existing_cols:
        new_rows['day_of_week'] = df_new['datetime'].dt.dayofweek.astype(np.uint8).values
    
    if 'session' in existing_cols:
        hours = df_new['datetime'].dt.hour
        sessions = []
        for h in hours:
            if 0 <= h < 7:
                sessions.append('asian')
            elif 7 <= h < 12:
                sessions.append('london')
            elif 12 <= h < 17:
                sessions.append('new_york')
            else:
                sessions.append('off_hours')
        new_rows['session'] = sessions
    
    if 'is_kill_zone' in existing_cols:
        hours = df_new['datetime'].dt.hour
        new_rows['is_kill_zone'] = ((hours >= 7) & (hours <= 10)) | ((hours >= 12) & (hours <= 15))
    
    for col in new_rows.columns:
        if col in df_existing.columns:
            try:
                new_rows[col] = new_rows[col].astype(df_existing[col].dtype)
            except (ValueError, TypeError):
                pass
    
    new_rows = new_rows[[c for c in existing_cols if c in new_rows.columns]]
    
    df_combined = pd.concat([df_existing, new_rows], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=['time'], keep='first')
    df_combined = df_combined.sort_values('time').reset_index(drop=True)
    
    df_combined.to_parquet(parquet_path, index=False)
    
    return len(new_rows)


def main():
    if not mt5.initialize():
        print(f"MT5 initialize failed: {mt5.last_error()}")
        sys.exit(1)
    
    print(f"MT5 connected: {mt5.account_info().server}")
    print(f"Account: {mt5.account_info().name}")
    print()
    
    all_files = [f for f in os.listdir(DATA_DIR) if f.endswith('_real.parquet')]
    
    symbols_seen = set()
    file_groups = []
    for f in sorted(all_files):
        parts = f.replace('_real.parquet', '').rsplit('_', 1)
        if len(parts) == 2:
            base, tf = parts
            file_groups.append((base, tf, f))
            symbols_seen.add(base)
    
    print(f"Found {len(file_groups)} parquet files across {len(symbols_seen)} symbols")
    print()
    
    symbol_map = {}
    not_found = []
    for base in sorted(symbols_seen):
        mt5_sym = get_mt5_symbol(base)
        if mt5_sym:
            symbol_map[base] = mt5_sym
        else:
            not_found.append(base)
    
    print(f"Mapped {len(symbol_map)} symbols to MT5. Not found: {len(not_found)}")
    if not_found:
        print(f"  Missing: {not_found[:20]}")
    print()
    
    total_appended = 0
    total_files = 0
    errors = []
    
    for base, tf, filename in file_groups:
        if base not in symbol_map:
            continue
        
        mt5_sym = symbol_map[base]
        parquet_path = os.path.join(DATA_DIR, filename)
        
        try:
            count = append_candles_for_file(parquet_path, mt5_sym, tf, CUTOFF_UTC)
            if count > 0:
                print(f"  [APPENDED] {filename}: +{count} new bars")
                total_appended += count
                total_files += 1
            else:
                print(f"  [UP-TO-DATE] {filename}")
        except Exception as e:
            errors.append((filename, str(e)))
            print(f"  [ERROR] {filename}: {e}")
    
    print()
    print(f"{'='*60}")
    print(f"DONE: Appended {total_appended} total bars across {total_files} files")
    if errors:
        print(f"Errors: {len(errors)}")
        for fn, err in errors:
            print(f"  {fn}: {err}")
    print(f"{'='*60}")
    
    mt5.shutdown()


if __name__ == "__main__":
    main()
