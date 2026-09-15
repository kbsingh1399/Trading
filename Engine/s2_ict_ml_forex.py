import os
import json
import numpy as np
import pandas as pd
import polars as pl
from datetime import datetime, timedelta
import xgboost as xgb
from sklearn.metrics import classification_report

# -------------------------------------------------------------------------
# CONSTANTS & CONFIGURATION
# -------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data")
OOS_WINDOWS_FILE = os.path.join(PROJECT_ROOT, "Engine", "oos_windows_20_random.json")
TARGET_CRITERIA_FILE = os.path.join(PROJECT_ROOT, "Engine", "target_oos_criteria.json")

INITIAL_CAPITAL = 5000.0
BASE_RISK = 50.0 # 1.0%
MIN_R_MULTIPLE = 4.0

def engineer_features(symbol: str) -> pd.DataFrame:
    m15_file = os.path.join(DATA_DIR, f"{symbol}_15m_real.parquet")
    h4_file = os.path.join(DATA_DIR, f"{symbol}_4h_real.parquet")
    d1_file = os.path.join(DATA_DIR, f"{symbol}_d1_real.parquet")

    if not (os.path.exists(m15_file) and os.path.exists(h4_file) and os.path.exists(d1_file)):
        raise FileNotFoundError(f"Missing data files for {symbol}")

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
    
    # Calculate simple RSI (14 period)
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
    
    # Calculate rolling VWAP proxy (20 period typical price)
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
    
    # London (7-10 UTC) and NY (12-15 UTC) Kill Zones
    m15_df = m15_df.with_columns([
        ((pl.col("hour") >= 7) & (pl.col("hour") <= 10) | 
         (pl.col("hour") >= 12) & (pl.col("hour") <= 15)).alias("is_kill_zone")
    ])
    
    return m15_df.drop_nulls().to_pandas()

def create_labels(df: pd.DataFrame) -> pd.DataFrame:
    df['target'] = np.nan
    df['r_realized'] = 0.0
    
    lows = df['low'].values
    highs = df['high'].values
    closes = df['close'].values
    
    sweep_pdl = df['sweep_pdl'].values
    bullish_fvg = df['bullish_fvg'].values
    htf_4h = df['htf_4h_trend'].values
    local_low = df['local_low_20'].values
    
    if 'is_kill_zone' in df.columns:
        is_kz = df['is_kill_zone'].values
    else:
        is_kz = np.ones(len(df), dtype=bool)
        
    sweep_pdh = df['sweep_pdh'].values
    bearish_fvg = df['bearish_fvg'].values
    local_high = df['local_high_20'].values
    ema_50 = df['ema_50'].values
    ema_200 = df['ema_200'].values
    day_of_week = df['day_of_week'].values
    
    targets = np.full(len(df), np.nan)
    r_reals = np.zeros(len(df))
    
    look_fwd = 96 
    
    for i in range(len(df) - look_fwd):
        if is_kz[i] and sweep_pdl[i] == 1 and htf_4h[i] > 0:
            entry = closes[i]
            orig_sl = local_low[i]
            if entry <= orig_sl: continue
            r_dist = entry - orig_sl
            
            # Ratchet levels
            tp = entry + (MIN_R_MULTIPLE * r_dist)
            lock_1r = entry + (1.0 * r_dist)
            lock_15r = entry + (1.5 * r_dist)
            lock_20r = entry + (2.0 * r_dist)
            lock_25r = entry + (2.5 * r_dist)
            lock_30r = entry + (3.0 * r_dist)
            lock_35r = entry + (3.5 * r_dist)
            
            sl = orig_sl
            r_real = -1.0
            
            for j in range(i+1, min(i+look_fwd, len(df))):
                # Check Stop Loss hit
                if lows[j] <= sl:
                    if sl == orig_sl: r_real = -1.0
                    elif sl == entry + (0.15 * r_dist): r_real = 0.15
                    elif sl == entry + (1.0 * r_dist): r_real = 1.0
                    elif sl == entry + (1.8 * r_dist): r_real = 1.8
                    elif sl == entry + (2.3 * r_dist): r_real = 2.3
                    elif sl == entry + (2.8 * r_dist): r_real = 2.8
                    elif sl == entry + (3.3 * r_dist): r_real = 3.3
                    break
                    
                # Check Take Profit hit
                if highs[j] >= tp:
                    r_real = MIN_R_MULTIPLE
                    break
                    
                # Ratchet updates
                if highs[j] >= lock_35r and sl < entry + (3.3 * r_dist):
                    sl = entry + (3.3 * r_dist)
                elif highs[j] >= lock_30r and sl < entry + (2.8 * r_dist):
                    sl = entry + (2.8 * r_dist)
                elif highs[j] >= lock_25r and sl < entry + (2.3 * r_dist):
                    sl = entry + (2.3 * r_dist)
                elif highs[j] >= lock_20r and sl < entry + (1.8 * r_dist):
                    sl = entry + (1.8 * r_dist)
                elif highs[j] >= lock_15r and sl < entry + (1.0 * r_dist):
                    sl = entry + (1.0 * r_dist)
                elif highs[j] >= lock_1r and sl < entry + (0.15 * r_dist):
                    sl = entry + (0.15 * r_dist)
                    
                # Time Decay Rule: Exit at market if < +0.2R within 24 bars (6 hours)
                if j == i + 24 and closes[j] < entry + (0.2 * r_dist):
                    r_real = (closes[j] - entry) / r_dist
                    break
            
            # Label 1 if it didn't take a full loss
            targets[i] = 1 if r_real > 0 else 0
            r_reals[i] = r_real
            
        elif is_kz[i] and sweep_pdh[i] == 1 and htf_4h[i] < 0:
            entry = closes[i]
            orig_sl = local_high[i]
            if entry >= orig_sl: continue
            r_dist = orig_sl - entry
            # Ratchet levels
            tp = entry - (MIN_R_MULTIPLE * r_dist)
            lock_1r = entry - (1.0 * r_dist)
            lock_15r = entry - (1.5 * r_dist)
            lock_20r = entry - (2.0 * r_dist)
            lock_25r = entry - (2.5 * r_dist)
            lock_30r = entry - (3.0 * r_dist)
            lock_35r = entry - (3.5 * r_dist)
            
            sl = orig_sl
            r_real = -1.0
            
            for j in range(i+1, min(i+look_fwd, len(df))):
                # Check Stop Loss hit
                if highs[j] >= sl:
                    if sl == orig_sl: r_real = -1.0
                    elif sl == entry - (0.15 * r_dist): r_real = 0.15
                    elif sl == entry - (1.0 * r_dist): r_real = 1.0
                    elif sl == entry - (1.8 * r_dist): r_real = 1.8
                    elif sl == entry - (2.3 * r_dist): r_real = 2.3
                    elif sl == entry - (2.8 * r_dist): r_real = 2.8
                    elif sl == entry - (3.3 * r_dist): r_real = 3.3
                    break
                    
                # Check Take Profit hit
                if lows[j] <= tp:
                    r_real = MIN_R_MULTIPLE
                    break
                    
                # Ratchet updates
                if lows[j] <= lock_35r and sl > entry - (3.3 * r_dist):
                    sl = entry - (3.3 * r_dist)
                elif lows[j] <= lock_30r and sl > entry - (2.8 * r_dist):
                    sl = entry - (2.8 * r_dist)
                elif lows[j] <= lock_25r and sl > entry - (2.3 * r_dist):
                    sl = entry - (2.3 * r_dist)
                elif lows[j] <= lock_20r and sl > entry - (1.8 * r_dist):
                    sl = entry - (1.8 * r_dist)
                elif lows[j] <= lock_15r and sl > entry - (1.0 * r_dist):
                    sl = entry - (1.0 * r_dist)
                elif lows[j] <= lock_1r and sl > entry - (0.15 * r_dist):
                    sl = entry - (0.15 * r_dist)
                    
                # Time Decay Rule: Exit at market if < +0.2R within 24 bars (6 hours)
                if j == i + 24 and closes[j] > entry - (0.2 * r_dist):
                    r_real = (entry - closes[j]) / r_dist
                    break
                    
            # Label 1 if it didn't take a full loss
            targets[i] = 1 if r_real > 0 else 0
            r_reals[i] = r_real

    df['target'] = targets
    df['r_realized'] = r_reals
    return df

# -------------------------------------------------------------------------
# ML TRAINING & WALK-FORWARD OOS BACKTEST
# -------------------------------------------------------------------------
def train_model(train_df, features):
    X = train_df[features]
    y = train_df['target']
    
    if y.sum() < 2:
        return None
        
    try:
        pos_weight = (len(y) - y.sum()) / y.sum()
    except ZeroDivisionError:
        pos_weight = 1.0
        
    clf = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        reg_lambda=3.0,
        reg_alpha=1.0,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=pos_weight,
        random_state=42,
        eval_metric="logloss",
        n_jobs=-1
    )
    clf.fit(X, y)
    return clf

def run_walk_forward_backtest(symbol: str, df: pd.DataFrame):
    with open(OOS_WINDOWS_FILE, "r") as f:
        windows = json.load(f)
        
    features = ["bullish_fvg", "bearish_fvg", "htf_4h_trend", "hour", "day_of_week", "rsi_14", "vwap_dist", "ema_50_dist", "ema_200_dist", "ema_200_slope", "atr_14", "volatility_20", "roc_20"]
    
    capital = INITIAL_CAPITAL
    results = []
    
    for w in windows:
        start_date = pd.to_datetime(w["start_date"]).tz_localize("UTC")
        end_date = pd.to_datetime(w["end_date"]).tz_localize("UTC")
        
        train_mask = (df["datetime"] < start_date) & df["target"].notna()
        train_df = df[train_mask]
        
        oos_mask = (df["datetime"] >= start_date) & (df["datetime"] <= end_date)
        oos_df = df[oos_mask].copy()
        
        if len(train_df) < 50 or len(oos_df) == 0:
            continue
            
        model = train_model(train_df, features)
        if model is None:
            continue
            
        train_setup_mask = train_df['target'].notna()
        if not train_setup_mask.any():
            continue
            
        X_train_setups = train_df.loc[train_setup_mask, features]
        train_probs = model.predict_proba(X_train_setups)[:, 1]
        
        # Calculate how many setups per quarter we have in train
        total_train_days = (train_df['datetime'].max() - train_df['datetime'].min()).days
        if total_train_days == 0: total_train_days = 1
        quarters_in_train = total_train_days / 90.0
        
        # We want ~35 high-confidence trades per quarter in sample to ensure volume
        target_total_trades = int(35 * quarters_in_train)
        
        # Find the threshold p* that gives us target_total_trades in train
        sorted_probs = np.sort(train_probs)[::-1]
        if target_total_trades < len(sorted_probs):
            p_star = sorted_probs[target_total_trades]
        else:
            p_star = 0.50 # fallback
            
        # Target must be >= 1.0R to survive 40% WR, base rate is lower, so p_star floor must be lower!
        p_star = max(0.35, min(p_star, 0.90))
            
        setup_mask = oos_df['target'].notna()
        if not setup_mask.any():
            continue
            
        X_oos = oos_df.loc[setup_mask, features]
        probs = model.predict_proba(X_oos)[:, 1]
        oos_df.loc[setup_mask, 'ml_prob'] = probs
        
        # Execute Trades where prob > p_star (causally calibrated)
        trade_mask = setup_mask & (oos_df['ml_prob'] > p_star)
        trades = oos_df[trade_mask]
        
        # PnL logic based on actual realized R
        r_sum = trades['r_realized'].sum()
        pnl = r_sum * BASE_RISK
        capital += pnl
        
        results.append({
            "window": w["name"],
            "trades": len(trades),
            "wins": len(trades[trades['r_realized'] > 0]),
            "pnl": pnl,
            "capital": capital
        })
        
    return results

if __name__ == "__main__":
    files = os.listdir(DATA_DIR)
    symbols = sorted(list(set([f.split('_')[0] for f in files if f.endswith('.parquet') and "15m" in f])))
    
    print(f"Starting exhaustive OOS ML Backtest on {len(symbols)} symbols...")
    
    all_results = {}
    
    for sym in symbols:
        try:
            df = engineer_features(sym)
            df = create_labels(df)
            res = run_walk_forward_backtest(sym, df)
            all_results[sym] = res
            
            # Print a quick summary of this symbol
            total_trades = sum(r['trades'] for r in res)
            final_pnl = sum(r['pnl'] for r in res)
            print(f"[{sym}] Completed 20 Windows | Total Trades: {total_trades} | Net PnL: ${final_pnl:.2f}")
        except Exception as e:
            print(f"[{sym}] Failed: {str(e)}")
            
    with open("Engine/forex_oos_results.json", "w") as f:
        json.dump(all_results, f, indent=4)
        
    print("Saved massive exhaustive results to Engine/forex_oos_results.json")
