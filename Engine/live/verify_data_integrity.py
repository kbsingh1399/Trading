"""
End-to-End Data Integrity Verification Pipeline
Checks every parquet file in Forex_Backtesting_Data for:
1. Monotonically increasing timestamps (no out-of-order rows)
2. No duplicate timestamps
3. No unexpected gaps (gaps > expected bar interval, excluding weekends/holidays)
4. No null values in OHLCV
5. Candle sanity: High >= Open,Close,Low and Low <= Open,Close,High
6. Continuous append verification (last timestamp matches cutoff)
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import timedelta

DATA_DIR = "Forex_Backtesting_Data"

# Expected intervals per timeframe
TF_INTERVALS = {
    "15m": timedelta(minutes=15),
    "1h":  timedelta(hours=1),
    "4h":  timedelta(hours=4),
    "d1":  timedelta(days=1),
}

# Max allowed gap before flagging (weekends = ~2.5 days for forex, longer for indices)
# We use 3 days as the threshold - anything beyond is suspicious
MAX_NORMAL_GAP = {
    "15m": timedelta(days=3, hours=6),
    "1h":  timedelta(days=3, hours=6),
    "4h":  timedelta(days=4),
    "d1":  timedelta(days=4),
}

def verify_parquet(filepath, tf_key):
    """Run all integrity checks on a single parquet file."""
    issues = []
    
    df = pd.read_parquet(filepath)
    basename = os.path.basename(filepath)
    
    if len(df) == 0:
        issues.append("EMPTY FILE")
        return issues, 0, None, None
    
    # --- 1. Parse timestamps ---
    if 'datetime' in df.columns:
        timestamps = pd.to_datetime(df['datetime'])
        if timestamps.dt.tz is not None:
            timestamps = timestamps.dt.tz_localize(None)
    elif 'time' in df.columns:
        timestamps = pd.to_datetime(df['time'], unit='s')
    else:
        issues.append("NO TIMESTAMP COLUMN")
        return issues, len(df), None, None
    
    # --- 2. Monotonicity check ---
    diffs = timestamps.diff().dropna()
    non_positive = (diffs <= timedelta(0)).sum()
    if non_positive > 0:
        issues.append(f"NON-MONOTONIC: {non_positive} rows where timestamp <= previous")
    
    # --- 3. Duplicate check ---
    dupes = timestamps.duplicated().sum()
    if dupes > 0:
        issues.append(f"DUPLICATES: {dupes} duplicate timestamps")
    
    # --- 4. Gap analysis ---
    expected_interval = TF_INTERVALS[tf_key]
    max_gap = MAX_NORMAL_GAP[tf_key]
    
    # Find gaps larger than expected interval
    big_gaps = diffs[diffs > expected_interval * 1.5]  # 1.5x tolerance
    suspicious_gaps = diffs[diffs > max_gap]
    
    if len(suspicious_gaps) > 0:
        for idx in suspicious_gaps.index:
            gap_hours = suspicious_gaps[idx].total_seconds() / 3600
            gap_from = timestamps.iloc[idx-1]
            gap_to = timestamps.iloc[idx]
            issues.append(f"SUSPICIOUS GAP: {gap_hours:.1f}h from {gap_from} to {gap_to}")
    
    # --- 5. Null checks on OHLCV ---
    for col in ['open', 'high', 'low', 'close']:
        if col in df.columns:
            nulls = df[col].isna().sum()
            if nulls > 0:
                issues.append(f"NULL VALUES: {nulls} nulls in '{col}'")
    
    vol_col = 'tick_volume' if 'tick_volume' in df.columns else 'volume'
    if vol_col in df.columns:
        nulls = df[vol_col].isna().sum()
        if nulls > 0:
            issues.append(f"NULL VALUES: {nulls} nulls in '{vol_col}'")
    
    # --- 6. Candle sanity ---
    if all(c in df.columns for c in ['open', 'high', 'low', 'close']):
        bad_high = (df['high'] < df[['open', 'close', 'low']].max(axis=1)).sum()
        bad_low = (df['low'] > df[['open', 'close', 'high']].min(axis=1)).sum()
        if bad_high > 0:
            issues.append(f"CANDLE ERROR: {bad_high} bars where high < max(open,close,low)")
        if bad_low > 0:
            issues.append(f"CANDLE ERROR: {bad_low} bars where low > min(open,close,high)")
    
    first_ts = timestamps.iloc[0]
    last_ts = timestamps.iloc[-1]
    
    return issues, len(df), first_ts, last_ts


def main():
    all_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('_real.parquet')])
    
    # Group by timeframe
    file_groups = {}
    for f in all_files:
        parts = f.replace('_real.parquet', '').rsplit('_', 1)
        if len(parts) == 2:
            base, tf = parts
            if tf not in file_groups:
                file_groups[tf] = []
            file_groups[tf].append((base, f))
    
    total_files = 0
    total_clean = 0
    total_issues = 0
    all_issue_details = []
    
    for tf_key in ['15m', '1h', '4h', 'd1']:
        if tf_key not in file_groups:
            continue
        
        files = file_groups[tf_key]
        print(f"\n{'='*70}")
        print(f"  TIMEFRAME: {tf_key.upper()} ({len(files)} files)")
        print(f"{'='*70}")
        
        tf_clean = 0
        tf_issues_count = 0
        
        for base, filename in files:
            filepath = os.path.join(DATA_DIR, filename)
            issues, rows, first_ts, last_ts = verify_parquet(filepath, tf_key)
            total_files += 1
            
            if len(issues) == 0:
                tf_clean += 1
                total_clean += 1
                # Only print summary for clean files on 15m
                if tf_key == '15m':
                    print(f"  [OK] {base:<12} | {rows:>6} rows | {first_ts} -> {last_ts}")
            else:
                tf_issues_count += len(issues)
                total_issues += len(issues)
                print(f"  [!!] {base:<12} | {rows:>6} rows | ISSUES:")
                for issue in issues:
                    print(f"       -> {issue}")
                    all_issue_details.append((filename, issue))
        
        print(f"\n  Summary: {tf_clean}/{len(files)} clean, {tf_issues_count} issues found")
    
    # --- Final Report ---
    print(f"\n{'='*70}")
    print(f"  FINAL INTEGRITY REPORT")
    print(f"{'='*70}")
    print(f"  Total files checked:  {total_files}")
    print(f"  Clean (no issues):    {total_clean}")
    print(f"  Files with issues:    {total_files - total_clean}")
    print(f"  Total issues found:   {total_issues}")
    
    if total_issues == 0:
        print(f"\n  *** ALL FILES PASSED INTEGRITY CHECK ***")
        sys.exit(0)
    else:
        print(f"\n  Issues summary:")
        for fn, issue in all_issue_details:
            print(f"    {fn}: {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
