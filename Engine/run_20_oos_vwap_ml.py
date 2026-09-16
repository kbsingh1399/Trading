import os
import glob
import pandas as pd
import numpy as np
import warnings
from strategy.s4_vwap_reversion import simulate_vwap_reversion_trades
import json

warnings.filterwarnings('ignore')

ALL_ASSETS = ['BTC', 'ETH', 'XRP', 'SOL', 'BNB', 'DOGE', 'ADA', 'TRX', 'LINK', 'AVAX', 'SUI', 'NEAR', 'DOT', 'LTC', 'BCH', 'APT', 'OP', 'ARB']

OOS_WINDOWS = [
    ("2021-01-01", "2021-03-31", "Q1 2021 Retail Mania Kickoff"),
    ("2021-04-01", "2021-06-30", "Q2 2021 May Crash & Chop"),
    ("2021-07-01", "2021-09-30", "Q3 2021 Re-accumulation"),
    ("2021-10-01", "2021-12-31", "Q4 2021 Blow-off Top"),
    ("2022-01-01", "2022-03-31", "Q1 2022 Bear Market Start"),
    ("2022-04-01", "2022-06-30", "Q2 2022 Luna Collapse Liquidation"),
    ("2022-07-01", "2022-09-30", "Q3 2022 Bear Market Chop"),
    ("2022-10-01", "2022-12-31", "Q4 2022 FTX Collapse"),
    ("2023-01-01", "2023-03-31", "Q1 2023 Early Recovery"),
    ("2023-04-01", "2023-06-30", "Q2 2023 SVB Crisis & Chop"),
    ("2023-07-01", "2023-09-30", "Q3 2023 Deep Summer Doldrums"),
    ("2023-10-01", "2023-12-31", "Q4 2023 ETF Narrative Rally"),
    ("2024-01-01", "2024-03-31", "Q1 2024 Pre-Halving Euphoria"),
    ("2024-04-01", "2024-06-30", "Q2 2024 Post-Halving Distribution"),
    ("2024-07-01", "2024-09-30", "Q3 2024 Late Summer Consolidation"),
    ("2024-10-01", "2024-12-31", "Q4 2024 Year-End Breakouts"),
    ("2025-01-01", "2025-03-31", "Q1 2025 Institutional Flow Surge"),
    ("2025-04-01", "2025-06-30", "Q2 2025 Altcoin Rotations"),
    ("2025-07-01", "2025-09-30", "Q3 2025 Mid-Year Volatility Expansion"),
    ("2025-10-01", "2025-12-31", "Q4 2025 Late-Cycle Microstructures")
]
DATA_DIR = 'Engine/binance_backtesting_data'

VWAP_FEATURES = [
    "direction", "z_score", "e200_dist", "hour", "day_of_week", "atr_pct", "vol_spike"
]

def process_asset(asset, df):
    highs = df['high'].values
    lows = df['low'].values
    closes = df['close'].values
    volumes = df['volume_base'].values
    dt = pd.to_datetime(df['datetime_utc'])
    timestamps = (dt - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    timestamps = timestamps.values
    dates = dt.dt.date.astype(str).str.replace('-', '').astype(np.int64).values
    hours = dt.dt.hour.values
    minutes = dt.dt.minute.values
    day_of_weeks = dt.dt.dayofweek.values
    
    feats, outcomes, ts = simulate_vwap_reversion_trades(
        highs, lows, closes, volumes, timestamps, dates, hours, minutes, day_of_weeks
    )
    
    if len(ts) == 0:
        return pd.DataFrame()
        
    res = pd.DataFrame(feats, columns=VWAP_FEATURES)
    res['outcome'] = outcomes
    res['datetime'] = pd.to_datetime(ts, unit='s')
    res['asset'] = asset
    
    return res

def evaluate_oos():
    print("\n" + "=" * 100)
    print("MASTER 20 OOS WALK-FORWARD RUNNER: VWAP REVERSION + MACHINE LEARNING")
    print("=" * 100)
    
    windows = []
    for w in OOS_WINDOWS:
        windows.append({'start_date': w[0], 'end_date': w[1], 'name': w[2]})
        
    print("Pre-compiling baseline datasets for all 18 canonical assets with NUMBA...")
    all_trades = []
    
    for asset in ALL_ASSETS:
        filepath = os.path.join(DATA_DIR, f"{asset}USDT_15m_master_2020_2026.parquet")
        if not os.path.exists(filepath):
            continue
            
        df = pd.read_parquet(filepath).dropna(subset=['high', 'low', 'close', 'volume_base', 'datetime_utc']).reset_index(drop=True)
        
        df_res = process_asset(asset, df)
        if not df_res.empty:
            all_trades.append(df_res)
            
    master_df = pd.concat(all_trades, ignore_index=True)
    master_df = master_df.sort_values('datetime').dropna().reset_index(drop=True)
    
    total_oos_pnl = 0.0
    total_trades = 0
    windows_passed = 0
    total_wins = 0
    
    for idx, w in enumerate(windows):
        start = pd.to_datetime(w['start_date'])
        end = pd.to_datetime(w['end_date'])
        
        train_start = start - pd.Timedelta(days=180)
        
        train_df = master_df[(master_df['datetime'] >= train_start) & (master_df['datetime'] < start)]
        test_df = master_df[(master_df['datetime'] >= start) & (master_df['datetime'] <= end)]
        
        if len(train_df) < 500 or len(test_df) == 0:
            continue
            
        X_train = train_df[VWAP_FEATURES]
        y_train = train_df['outcome']
        
        import xgboost as xgb
        clf = xgb.XGBRegressor(
            n_estimators=100, 
            max_depth=3,
            learning_rate=0.05,
            reg_alpha=2.0,
            reg_lambda=5.0,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )
        clf.fit(X_train, y_train)
        
        X_test = test_df[VWAP_FEATURES]
        preds = clf.predict(X_test)
        
        test_df = test_df.copy()
        test_df['ml_prob'] = preds
        
        taken_trades = test_df[test_df['ml_prob'] >= 0.15]
        
        print(f"DEBUG: W{idx+1} raw trades: {len(test_df)}, max pred: {test_df['ml_prob'].max():.3f}, min pred: {test_df['ml_prob'].min():.3f}")
        
        if len(taken_trades) == 0:
            continue
            
        w_wins = (taken_trades['outcome'] > 0).sum()
        w_losses = len(taken_trades) - w_wins
        w_pnl_r = taken_trades['outcome'].sum()
        win_rate = (w_wins / len(taken_trades)) * 100
        
        total_oos_pnl += w_pnl_r
        total_trades += len(taken_trades)
        total_wins += w_wins
        
        status = "PASS" if w_pnl_r > 5.0 and win_rate >= 40.0 else "FAIL"
        if status == "PASS":
            windows_passed += 1
            
        print(f"W{idx+1:<2} | {w['name']:<35} | Trades: {len(taken_trades):<3} | WR: {win_rate:>5.1f}% | Net R: {w_pnl_r:>6.2f} | {status}")
        
    print("-" * 100)
    print("FINAL METRICS across 20 Windows:")
    print(f"Total OOS Net R  : +{total_oos_pnl:.2f} R")
    print(f"Total Trades     : {total_trades}")
    
    overall_wr = (total_wins / total_trades * 100) if total_trades > 0 else 0
    print(f"Overall Win Rate : {overall_wr:.1f}%")
    print(f"Windows Passed   : {windows_passed} / 20")
    
if __name__ == "__main__":
    evaluate_oos()
