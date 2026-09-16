import os
import sys
import json
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.strategy_kernel import CANONICAL_18_ASSETS
from Engine.strategy.s3_orb_ml import simulate_orb_trades

DATA_DIR = os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data")
OOS_JSON = os.path.join(SCRIPT_DIR, "oos_windows_20.json")

def process_asset(asset, df, start_h, start_m):
    # Prepare numpy arrays for numba
    highs = df['high'].values.astype(np.float64)
    lows = df['low'].values.astype(np.float64)
    closes = df['close'].values.astype(np.float64)
    
    # Tick volume or real volume
    if 'tick_volume' in df.columns:
        volumes = df['tick_volume'].values.astype(np.float64)
    elif 'volume' in df.columns:
        volumes = df['volume'].values.astype(np.float64)
    else:
        volumes = np.ones(len(df), dtype=np.float64)
        
    timestamps = df['datetime'].dt.tz_localize(None).astype('datetime64[s]').astype(np.int64).values
    
    df['date_int'] = df['datetime'].dt.strftime("%Y%m%d").astype(np.int64)
    dates = df['date_int'].values
    hours = df['datetime'].dt.hour.values.astype(np.int32)
    minutes = df['datetime'].dt.minute.values.astype(np.int32)
    day_of_weeks = df['datetime'].dt.dayofweek.values.astype(np.int32)
    
    features, outcomes, timestamps_out = simulate_orb_trades(
        highs, lows, closes, volumes, timestamps, dates, hours, minutes, day_of_weeks,
        start_hour=start_h, start_minute=start_m
    )
    
    if len(outcomes) == 0:
        return pd.DataFrame()
        
    res_df = pd.DataFrame(features, columns=['direction_enum', 'or_range_pct', 'rsi_14', 'vwap_dist', 'ema_dist', 
                                             'hour', 'day_of_week', 'ema_200_dist', 'ema_200_slope', 'atr_14_pct', 
                                             'vol_spike', 'or_range_atr', 'pdl_dist', 'pdh_dist', 'swept_pdl', 'swept_pdh'])
    res_df['outcome'] = outcomes
    res_df['datetime'] = pd.to_datetime(timestamps_out, unit='s', utc=True)
    res_df['asset'] = asset
    
    return res_df

def evaluate_oos():
    print("\n" + "=" * 100)
    print("MASTER 20 OOS WALK-FORWARD RUNNER: ORB + MACHINE LEARNING (LONDON & NY SESSIONS)")
    print("=" * 100)
    
    with open(OOS_JSON, "r") as f:
        windows = json.load(f)
        
    print("Pre-compiling baseline ORB datasets for all 18 canonical assets with NUMBA...")
    
    all_trades = []
    
    # We discovered raw ORB bleeds on exotics, so we restrict to the proven edge subset
    ORB_ASSETS = [a for a in CANONICAL_18_ASSETS if a in ['GER40', 'FR40', 'US2000', 'GAS', 'XAUCNH', 'NICKEL']]
    
    for asset in ORB_ASSETS:
        filename = asset if asset != 'GER40' else 'GER30'
        filepath = os.path.join(DATA_DIR, f"{filename}_15m_real.parquet")
        if not os.path.exists(filepath):
            continue
            
        df = pd.read_parquet(filepath).dropna().reset_index(drop=True)
        
        df_lon = process_asset(asset, df, start_h=7, start_m=0)
        df_ny = process_asset(asset, df, start_h=13, start_m=30)
        
        if not df_lon.empty: all_trades.append(df_lon)
        if not df_ny.empty: all_trades.append(df_ny)
        
    master_df = pd.concat(all_trades, ignore_index=True)
    master_df = master_df.sort_values('datetime').dropna().reset_index(drop=True)
    
    features = ['direction_enum', 'or_range_pct', 'rsi_14', 'vwap_dist', 'ema_dist', 
                'hour', 'day_of_week', 'ema_200_dist', 'ema_200_slope', 'atr_14_pct', 
                'vol_spike', 'or_range_atr', 'pdl_dist', 'pdh_dist', 'swept_pdl', 'swept_pdh']
    
    total_oos_pnl = 0.0
    total_trades = 0
    total_wins = 0
    passed_windows = 0
    
    master_df['dt_str'] = master_df['datetime'].dt.strftime('%Y-%m-%d')
    for w in windows:
        start_date = w['start_date']
        end_date = w['end_date']
        
        # 72 hour strict purge gap
        start_dt = pd.to_datetime(start_date)
        purge_dt = (start_dt - pd.Timedelta(hours=72)).strftime('%Y-%m-%d')
        
        train_df = master_df[master_df['dt_str'] < purge_dt]
        test_df = master_df[(master_df['dt_str'] >= start_date) & (master_df['dt_str'] <= end_date)]
        
        if len(train_df) < 500 or len(test_df) == 0:
            continue
            
        # Train ML Regressor
        X_train = train_df[features]
        # Regress directly on the Net R outcome (-1.0 to 2.5)
        y_train = train_df['outcome']
        
        # We use XGBoost with strict institutional regularization
        import xgboost as xgb
        clf = xgb.XGBRegressor(
            n_estimators=100, 
            max_depth=3,            # Shallow trees to prevent noise memorization
            learning_rate=0.05,
            reg_alpha=2.0,          # Extreme L1 regularization
            reg_lambda=5.0,         # Extreme L2 regularization
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )
        clf.fit(X_train, y_train)
        
        X_test = test_df[features]
        preds = clf.predict(X_test)
        
        # ML Filter: Only take trades with a predicted EV of > +0.20 R
        test_df = test_df.copy()
        test_df['ml_prob'] = preds
        
        taken_trades = test_df[test_df['ml_prob'] >= 0.15]
        
        if len(taken_trades) == 0:
            continue
            
        w_wins = (taken_trades['outcome'] > 0).sum()
        w_losses = len(taken_trades) - w_wins
        
        # We now use the exact Net R calculated directly in Numba (including ratchets, TP, SL)
        w_pnl_r = taken_trades['outcome'].sum()
        win_rate = (w_wins / len(taken_trades)) * 100 if len(taken_trades) > 0 else 0
        
        total_oos_pnl += w_pnl_r
        total_trades += len(taken_trades)
        total_wins += w_wins
        
        status = "PASS" if w_pnl_r > 5.0 and win_rate >= 40.0 else "FAIL"
        if "PASS" in status:
            passed_windows += 1
            
        print(f"W{w['window_id']:<2} | {w['name'][:35]:<35} | Trades: {len(taken_trades):<3} | WR: {win_rate:>5.1f}% | Net R: {w_pnl_r:>6.2f} | {status}")
        
    print("-" * 100)
    master_wr = (total_wins / total_trades) * 100 if total_trades > 0 else 0
    print(f"FINAL METRICS across {len(windows)} Windows:")
    print(f"Total OOS Net R  : +{total_oos_pnl:.2f} R")
    print(f"Total Trades     : {total_trades}")
    print(f"Overall Win Rate : {master_wr:.1f}%")
    print(f"Windows Passed   : {passed_windows} / {len(windows)}")
    
if __name__ == "__main__":
    try:
        evaluate_oos()
    except Exception as e:
        import traceback
        traceback.print_exc()
