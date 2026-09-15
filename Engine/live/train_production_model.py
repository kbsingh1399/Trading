"""
Train Full Production XGBoost Model for Forex Dry-Run / Live Execution.
Pulls from Forex_Backtesting_Data/, computes all 13 canonical features,
labels historical triple-barrier outcomes, and saves the trained model to:
Engine/models/xgboost_forex.json
"""
import os
import sys
import json
import logging
import pandas as pd
import numpy as np
import polars as pl
import xgboost as xgb

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data")
MODEL_PATH = os.path.join(PROJECT_ROOT, "Engine", "models", "xgboost_forex.json")

FEATURES = [
    "bullish_fvg", "bearish_fvg", "htf_4h_trend", "hour", "day_of_week", 
    "rsi_14", "vwap_dist", "ema_50_dist", "ema_200_dist", "ema_200_slope", 
    "atr_14", "volatility_20", "roc_20"
]

TOP_ASSETS = ['EURHUF', 'GER40', 'NICKEL', 'USDSEK', 'AU200', 'FR40', 'EURCNH', 'LEAD', 'NZDUSD', 'EURUSD']

def engineer_features(symbol: str) -> pd.DataFrame:
    m15_file = os.path.join(DATA_DIR, f"{symbol}_15m_real.parquet")
    h4_file = os.path.join(DATA_DIR, f"{symbol}_4h_real.parquet")
    d1_file = os.path.join(DATA_DIR, f"{symbol}_d1_real.parquet")

    if not (os.path.exists(m15_file) and os.path.exists(h4_file) and os.path.exists(d1_file)):
        return pd.DataFrame()

    d1_df = pl.read_parquet(d1_file).sort("datetime")
    d1_df = d1_df.with_columns([
        pl.col("high").shift(1).alias("prev_day_high"),
        pl.col("low").shift(1).alias("prev_day_low")
    ]).select(["datetime", "prev_day_high", "prev_day_low"]).drop_nulls()

    h4_df = pl.read_parquet(h4_file).sort("datetime")
    h4_df = h4_df.with_columns([
        pl.col("close").ewm_mean(span=200, adjust=False).alias("ema_200_4h")
    ]).with_columns([
        (pl.col("ema_200_4h") - pl.col("ema_200_4h").shift(5)).alias("htf_4h_trend")
    ]).select(["datetime", "ema_200_4h", "htf_4h_trend"]).drop_nulls()

    m15_df = pl.read_parquet(m15_file).sort("datetime")
    m15_df = m15_df.with_columns([
        pl.when(pl.col("low") > pl.col("high").shift(2)).then(pl.col("low") - pl.col("high").shift(2)).otherwise(0.0).alias("bullish_fvg"),
        pl.when(pl.col("high") < pl.col("low").shift(2)).then(pl.col("low").shift(2) - pl.col("high")).otherwise(0.0).alias("bearish_fvg"),
        pl.col("high").rolling_max(window_size=20).alias("local_high_20"),
        pl.col("low").rolling_min(window_size=20).alias("local_low_20"),
    ])

    m15_df = m15_df.join_asof(d1_df, on="datetime", strategy="backward")
    m15_df = m15_df.join_asof(h4_df, on="datetime", strategy="backward")

    m15_df = m15_df.with_columns([
        (pl.col("low") <= pl.col("prev_day_low")).cast(pl.Int8).alias("sweep_pdl"),
        (pl.col("high") >= pl.col("prev_day_high")).cast(pl.Int8).alias("sweep_pdh"),
        pl.col("datetime").dt.hour().alias("hour"),
        pl.col("datetime").dt.weekday().alias("day_of_week")
    ])
    
    # RSI (14)
    m15_df = m15_df.with_columns([
        pl.col("close").diff().alias("change")
    ]).with_columns([
        pl.when(pl.col("change") > 0).then(pl.col("change")).otherwise(0).alias("gain"),
        pl.when(pl.col("change") < 0).then(abs(pl.col("change"))).otherwise(0).alias("loss")
    ]).with_columns([
        pl.col("gain").ewm_mean(span=14, adjust=False).alias("avg_gain"),
        pl.col("loss").ewm_mean(span=14, adjust=False).alias("avg_loss")
    ]).with_columns([
        (100.0 - (100.0 / (1.0 + (pl.col("avg_gain") / pl.col("avg_loss"))))).alias("rsi_14")
    ])
    
    # VWAP (20) & Distances
    m15_df = m15_df.with_columns([
        ((pl.col("high") + pl.col("low") + pl.col("close")) / 3.0).alias("typical_price")
    ]).with_columns([
        (pl.col("typical_price").rolling_mean(window_size=20)).alias("vwap_20")
    ]).with_columns([
        ((pl.col("close") - pl.col("vwap_20")) / pl.col("vwap_20")).alias("vwap_dist"),
        pl.col("close").ewm_mean(span=50, min_periods=50).alias("ema_50"),
        pl.col("close").ewm_mean(span=200, min_periods=200).alias("ema_200"),
    ])
    
    m15_df = m15_df.with_columns([
        ((pl.col("close") - pl.col("ema_50")) / pl.col("ema_50")).alias("ema_50_dist"),
        ((pl.col("close") - pl.col("ema_200")) / pl.col("ema_200")).alias("ema_200_dist"),
        (pl.col("ema_200") - pl.col("ema_200").shift(12)).alias("ema_200_slope"),
        (pl.col("high") - pl.col("low")).rolling_mean(14).alias("atr_14"),
        (pl.col("close").rolling_std(20) / pl.col("close")).alias("volatility_20"),
        (pl.col("close") / pl.col("close").shift(20) - 1.0).alias("roc_20")
    ])
    
    m15_df = m15_df.with_columns([
        ((pl.col("hour") >= 7) & (pl.col("hour") <= 10) | 
         (pl.col("hour") >= 12) & (pl.col("hour") <= 15)).alias("is_kill_zone")
    ])
    
    return m15_df.drop_nulls().to_pandas()


def create_labels(df: pd.DataFrame) -> pd.DataFrame:
    df['target'] = np.nan
    lows = df['low'].values
    highs = df['high'].values
    closes = df['close'].values
    
    sweep_pdl = df['sweep_pdl'].values
    bullish_fvg = df['bullish_fvg'].values
    htf_4h = df['htf_4h_trend'].values
    local_low = df['local_low_20'].values
    
    sweep_pdh = df['sweep_pdh'].values
    bearish_fvg = df['bearish_fvg'].values
    local_high = df['local_high_20'].values
    is_kz = df['is_kill_zone'].values
    
    targets = np.full(len(df), np.nan)
    look_fwd = 96 # 24 hours max holding
    
    for i in range(len(df) - look_fwd):
        # Long Setup: Sweep PDL + Bullish FVG + 4H Bullish Trend + Kill Zone
        if sweep_pdl[i] == 1 and bullish_fvg[i] > 0 and htf_4h[i] > 0 and is_kz[i]:
            entry = closes[i]
            orig_sl = local_low[i]
            r_dist = entry - orig_sl
            if r_dist <= 0 or (r_dist / entry) > 0.02: 
                continue
            tp = entry + (4.0 * r_dist)
            
            won = False
            for j in range(i+1, min(i+look_fwd, len(df))):
                if lows[j] <= orig_sl:
                    won = False
                    break
                if highs[j] >= tp:
                    won = True
                    break
            targets[i] = 1 if won else 0
            
        # Short Setup: Sweep PDH + Bearish FVG + 4H Bearish Trend + Kill Zone
        elif sweep_pdh[i] == 1 and bearish_fvg[i] > 0 and htf_4h[i] < 0 and is_kz[i]:
            entry = closes[i]
            orig_sl = local_high[i]
            r_dist = orig_sl - entry
            if r_dist <= 0 or (r_dist / entry) > 0.02: 
                continue
            tp = entry - (4.0 * r_dist)
            
            won = False
            for j in range(i+1, min(i+look_fwd, len(df))):
                if highs[j] >= orig_sl:
                    won = False
                    break
                if lows[j] <= tp:
                    won = True
                    break
            targets[i] = 1 if won else 0
            
    df['target'] = targets
    return df


def main():
    all_X = []
    all_y = []
    
    print("=" * 70)
    print(" TRAINING REAL PRODUCTION XGBOOST MODEL ON HISTORICAL DATA")
    print("=" * 70)
    
    for sym in TOP_ASSETS:
        print(f"  -> Processing features and trade labels for {sym}...")
        df = engineer_features(sym)
        if df.empty:
            continue
        df = create_labels(df)
        
        valid = df[df['target'].notna()]
        if len(valid) > 0:
            print(f"     Found {len(valid)} labeled ICT setups (Win rate: {valid['target'].mean()*100:.1f}%)")
            all_X.append(valid[FEATURES])
            all_y.append(valid['target'].values)
            
    if not all_X:
        print("No valid setups found!")
        sys.exit(1)
        
    X_mat = pd.concat(all_X, ignore_index=True)
    y_vec = np.concatenate(all_y)
    
    print("-" * 70)
    print(f" Total Setups: {len(X_mat)} across {len(TOP_ASSETS)} institutional assets")
    print(f" Positive Class Weight: {(len(y_vec) - y_vec.sum()) / max(1, y_vec.sum()):.2f}")
    
    pos_weight = (len(y_vec) - y_vec.sum()) / max(1, y_vec.sum())
    
    dtrain = xgb.DMatrix(X_mat, label=y_vec)
    params = {
        'objective': 'binary:logistic',
        'max_depth': 4,
        'learning_rate': 0.05,
        'reg_alpha': 1.0,
        'reg_lambda': 3.0,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'scale_pos_weight': pos_weight,
        'eval_metric': 'logloss',
        'seed': 42
    }
    
    print(" Training XGBoost booster...")
    model = xgb.train(params, dtrain, num_boost_round=80)
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save_model(MODEL_PATH)
    
    print(f" SUCCESS: Production model saved to {MODEL_PATH}")
    print(f" Model size: {os.path.getsize(MODEL_PATH):,} bytes")
    
    # Feature Importance
    importance = model.get_score(importance_type='gain')
    sorted_imp = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    print("\n Top Feature Importances (Gain):")
    for f, score in sorted_imp[:8]:
        print(f"   {f:<15}: {score:.2f}")
    print("=" * 70)

if __name__ == "__main__":
    main()
