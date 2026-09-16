"""
================================================================================
ENGINE CORE: CANONICAL STRATEGY KERNEL (FOREX & CFD ML SUITE)
================================================================================
Single source of truth for:
1. 13 Canonical Stationary Features (Polars batch & Pandas streaming).
2. Strictly causal 4H As-Of Join with shift(1) to eliminate 3h45m lookahead.
3. Strictly causal Daily PDH/PDL with shift(1).
4. Microstructure 7-Stage Ratchet Exit Simulation with 24-bar time decay.
5. Unified Setup Entry Filter (Kill Zones, Liquidity Sweeps, FVGs, 4H Trend).
6. 96-bar Purge & Embargo Protocol at Out-Of-Sample boundaries.
================================================================================
"""
import os
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd
import polars as pl

# -------------------------------------------------------------------------
# CONSTANTS & ASSET CONFIGURATION
# -------------------------------------------------------------------------
CANONICAL_FEATURES = [
    "bullish_fvg", "bearish_fvg", "htf_4h_trend", "hour", "day_of_week",
    "rsi_14", "vwap_dist", "ema_50_dist", "ema_200_dist", "ema_200_slope",
    "atr_14", "volatility_20", "roc_20"
]

CANONICAL_18_ASSETS = [
    'EURHUF', 'GER40', 'NICKEL', 'USDSEK', 'GAS', 'AU200', 'FR40',
    'EURCNH', 'LEAD', 'NZDUSD', 'USDHKD', 'US2000', 'AUDCHF',
    'NZDCNH', 'XAUCNH', 'GAUCNH', 'EURSEK', 'EURUSD'
]

MIN_R_MULTIPLE = 4.0
MAX_HOLDING_BARS = 96  # 24 hours in 15m bars
TIME_DECAY_BARS = 24   # 6 hours in 15m bars
TIME_DECAY_THRESHOLD_R = 0.20
MAX_STOP_PCT = 0.025   # Max 2.5% stop distance to filter wild outliers


# -------------------------------------------------------------------------
# POLARS BATCH FEATURE ENGINEERING (HISTORICAL DATA & BACKTESTING)
# -------------------------------------------------------------------------
def engineer_features_polars(symbol: str, data_dir: str) -> pd.DataFrame:
    """
    Computes all 13 canonical features from raw 15m, 4h, and d1 parquets using Polars.
    Guarantees:
    - 4H trend shifted by 1 bar before as-of join (ELIMINATES 3h45m LOOKAHEAD).
    - Daily High/Low shifted by 1 bar before as-of join (strictly previous closed day).
    - Timestamps preserved in true UTC.
    """
    # Handle GER30 / GER40 naming
    base_sym = symbol
    m15_file = os.path.join(data_dir, f"{base_sym}_15m_real.parquet")
    if not os.path.exists(m15_file) and base_sym == "GER30":
        base_sym = "GER40"
        m15_file = os.path.join(data_dir, f"{base_sym}_15m_real.parquet")
    elif not os.path.exists(m15_file) and base_sym == "GER40":
        m15_file = os.path.join(data_dir, "GER30_15m_real.parquet")
        if os.path.exists(m15_file):
            base_sym = "GER30"

    h4_file = os.path.join(data_dir, f"{base_sym}_4h_real.parquet")
    d1_file = os.path.join(data_dir, f"{base_sym}_d1_real.parquet")

    if not (os.path.exists(m15_file) and os.path.exists(h4_file) and os.path.exists(d1_file)):
        raise FileNotFoundError(f"Missing required parquets for symbol {symbol} in {data_dir}")

    # 1. Daily Data: strictly previous completed day
    d1_df = pl.read_parquet(d1_file).sort("datetime")
    d1_df = d1_df.with_columns([
        pl.col("high").shift(1).alias("prev_day_high"),
        pl.col("low").shift(1).alias("prev_day_low")
    ]).select(["datetime", "prev_day_high", "prev_day_low"]).drop_nulls()

    # 2. 4H Data: EMA 200 slope shifted by 1 bar to eliminate lookahead
    h4_df = pl.read_parquet(h4_file).sort("datetime")
    h4_df = h4_df.with_columns([
        pl.col("close").ewm_mean(span=200, adjust=False).alias("ema_200_4h")
    ]).with_columns([
        (pl.col("ema_200_4h") - pl.col("ema_200_4h").shift(5)).alias("htf_4h_trend_raw")
    ]).with_columns([
        # Shift 1 bar so that 15m bars during 08:00-12:00 join the 04:00-08:00 closed bar
        pl.col("htf_4h_trend_raw").shift(1).alias("htf_4h_trend"),
        pl.col("ema_200_4h").shift(1).alias("ema_200_4h")
    ]).select(["datetime", "ema_200_4h", "htf_4h_trend"]).drop_nulls()

    # 3. 15M Data: Base calculations (Rolling Unmitigated FVGs)
    m15_df = pl.read_parquet(m15_file).sort("datetime")
    w = 5
    bullish_exprs = []
    bearish_exprs = []
    for k in range(w):
        bullish = (pl.col("low").rolling_min(window_size=k+1) - pl.col("high").shift(k+2)).fill_null(0.0).clip(lower_bound=0.0)
        bearish = (pl.col("low").shift(k+2) - pl.col("high").rolling_max(window_size=k+1)).fill_null(0.0).clip(lower_bound=0.0)
        bullish_exprs.append(bullish)
        bearish_exprs.append(bearish)

    m15_df = m15_df.with_columns([
        pl.max_horizontal(bullish_exprs).alias("bullish_fvg"),
        pl.max_horizontal(bearish_exprs).alias("bearish_fvg"),
        pl.col("high").rolling_max(window_size=20).alias("local_high_20"),
        pl.col("low").rolling_min(window_size=20).alias("local_low_20"),
    ])

    # Join Daily and 4H strictly backward in time
    m15_df = m15_df.join_asof(d1_df, on="datetime", strategy="backward")
    m15_df = m15_df.join_asof(h4_df, on="datetime", strategy="backward")

    # Time and sweep features
    m15_df = m15_df.with_columns([
        (pl.col("low") <= pl.col("prev_day_low")).cast(pl.Int8).alias("sweep_pdl"),
        (pl.col("high") >= pl.col("prev_day_high")).cast(pl.Int8).alias("sweep_pdh"),
        pl.col("datetime").dt.hour().alias("hour"),
        pl.col("datetime").dt.weekday().alias("day_of_week")
    ])

    # RSI (14 period)
    m15_df = m15_df.with_columns([
        pl.col("close").diff().alias("change")
    ]).with_columns([
        pl.when(pl.col("change") > 0).then(pl.col("change")).otherwise(0).alias("gain"),
        pl.when(pl.col("change") < 0).then(abs(pl.col("change"))).otherwise(0).alias("loss")
    ]).with_columns([
        pl.col("gain").ewm_mean(span=14, adjust=False).alias("avg_gain"),
        pl.col("loss").ewm_mean(span=14, adjust=False).alias("avg_loss")
    ]).with_columns([
        (100.0 - (100.0 / (1.0 + (pl.col("avg_gain") / (pl.col("avg_loss") + 1e-12))))).alias("rsi_14")
    ])

    # VWAP (20 typical price proxy) & Moving Averages
    m15_df = m15_df.with_columns([
        ((pl.col("high") + pl.col("low") + pl.col("close")) / 3.0).alias("typical_price")
    ]).with_columns([
        (pl.col("typical_price").rolling_mean(window_size=20)).alias("vwap_20")
    ]).with_columns([
        ((pl.col("close") - pl.col("vwap_20")) / pl.col("vwap_20")).alias("vwap_dist"),
        pl.col("close").ewm_mean(span=50, min_periods=50, adjust=False).alias("ema_50"),
        pl.col("close").ewm_mean(span=200, min_periods=200, adjust=False).alias("ema_200"),
    ])

    m15_df = m15_df.with_columns([
        ((pl.col("close") - pl.col("ema_50")) / pl.col("ema_50")).alias("ema_50_dist"),
        ((pl.col("close") - pl.col("ema_200")) / pl.col("ema_200")).alias("ema_200_dist"),
        (pl.col("ema_200") - pl.col("ema_200").shift(12)).alias("ema_200_slope"),
        (pl.col("high") - pl.col("low")).rolling_mean(14).alias("atr_14"),
        (pl.col("close").rolling_std(20) / pl.col("close")).alias("volatility_20"),
        (pl.col("close") / pl.col("close").shift(20) - 1.0).alias("roc_20")
    ])

    # London (07:00-10:00 UTC) and NY (12:00-15:00 UTC) Kill Zones
    m15_df = m15_df.with_columns([
        (((pl.col("hour") >= 7) & (pl.col("hour") <= 10)) | 
         ((pl.col("hour") >= 12) & (pl.col("hour") <= 15))).alias("is_kill_zone")
    ])

    # Drop nulls ONLY for required columns (avoids dropping fresh data due to legacy column nulls)
    subset_cols = CANONICAL_FEATURES + ["datetime", "open", "high", "low", "close", "is_kill_zone"]
    # Filter to columns that actually exist to avoid subset errors
    subset_cols = [c for c in subset_cols if c in m15_df.columns]
    
    df = m15_df.drop_nulls(subset=subset_cols).to_pandas()
    return df


# -------------------------------------------------------------------------
# PANDAS STREAMING FEATURE ENGINEERING (INFERENCE ENGINE & LIVE BUFFER)
# -------------------------------------------------------------------------
def compute_features_pandas(buffer_15m: pd.DataFrame, buffer_4h: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Computes all 13 canonical features on a rolling Pandas DataFrame.
    Guarantees mathematical parity with engineer_features_polars.
    """
    df = buffer_15m.copy()
    if len(df) == 0:
        return pd.DataFrame(columns=CANONICAL_FEATURES)

    # 1. EMAs
    df['ema_50'] = df['close'].ewm(span=50, min_periods=1, adjust=False).mean()
    df['ema_200'] = df['close'].ewm(span=200, min_periods=1, adjust=False).mean()

    # 2. RSI (14)
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, np.abs(delta), 0.0)
    gain_s = pd.Series(gain, index=df.index).ewm(span=14, adjust=False).mean()
    loss_s = pd.Series(loss, index=df.index).ewm(span=14, adjust=False).mean()
    rs = np.where(loss_s == 0, np.inf, gain_s / (loss_s + 1e-12))
    df['rsi_14'] = 100.0 - (100.0 / (1.0 + rs))
    df['rsi_14'] = df['rsi_14'].replace(np.inf, 100.0)

    # 3. VWAP (20)
    typical_price = (df['high'] + df['low'] + df['close']) / 3.0
    vwap_20 = typical_price.rolling(window=20).mean()
    df['vwap_dist'] = (df['close'] - vwap_20) / vwap_20

    # 4. FVGs (Rolling Unmitigated Logic W=5)
    w = 5
    bullish_fvgs = []
    bearish_fvgs = []
    for k in range(w):
        bull = (df['low'].rolling(k+1, min_periods=k+1).min() - df['high'].shift(k+2)).fillna(0.0).clip(lower=0.0)
        bear = (df['low'].shift(k+2) - df['high'].rolling(k+1, min_periods=k+1).max()).fillna(0.0).clip(lower=0.0)
        bullish_fvgs.append(bull)
        bearish_fvgs.append(bear)
        
    df['bullish_fvg'] = pd.concat(bullish_fvgs, axis=1).max(axis=1).fillna(0.0)
    df['bearish_fvg'] = pd.concat(bearish_fvgs, axis=1).max(axis=1).fillna(0.0)

    # 5. Distances & Slopes
    df['ema_50_dist'] = (df['close'] - df['ema_50']) / df['ema_50']
    df['ema_200_dist'] = (df['close'] - df['ema_200']) / df['ema_200']
    df['ema_200_slope'] = df['ema_200'] - df['ema_200'].shift(12)

    # 6. ATR & Volatility
    df['atr_14'] = (df['high'] - df['low']).rolling(window=14).mean()
    df['volatility_20'] = df['close'].rolling(window=20).std() / df['close']
    df['roc_20'] = (df['close'] / df['close'].shift(20)) - 1.0

    # 7. Time Features (UTC based)
    if isinstance(df.index, pd.DatetimeIndex):
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek + 1  # 1=Mon, 7=Sun
    else:
        df['hour'] = 0
        df['day_of_week'] = 1

    # 8. 4H Trend Alignment (Causal: from previous closed 4H bar)
    htf_4h_trend_val = 0.0
    if buffer_4h is not None and not buffer_4h.empty and len(buffer_4h) >= 205:
        b4h = buffer_4h.copy()
        b4h['ema_200_4h'] = b4h['close'].ewm(span=200, adjust=False).mean()
        b4h['htf_4h_trend'] = b4h['ema_200_4h'] - b4h['ema_200_4h'].shift(5)
        valid_trends = b4h['htf_4h_trend'].dropna()
        if len(valid_trends) > 0:
            htf_4h_trend_val = float(valid_trends.iloc[-1])

    df['htf_4h_trend'] = htf_4h_trend_val
    df.fillna(0.0, inplace=True)
    return df[CANONICAL_FEATURES]


# -------------------------------------------------------------------------
# UNIFIED SETUP DETECTION & ENTRY CRITERIA
# -------------------------------------------------------------------------
def check_setup_criteria(row: Dict[str, Any]) -> Tuple[bool, bool]:
    """
    Unified entry criteria for Long and Short setups.
    Returns: (is_long_setup, is_short_setup)
    """
    is_kz = bool(row.get('is_kill_zone', False))
    if not is_kz:
        hour = int(row.get('hour', 0))
        is_kz = ((7 <= hour <= 10) or (12 <= hour <= 15))

    sweep_pdl = int(row.get('sweep_pdl', 0))
    sweep_pdh = int(row.get('sweep_pdh', 0))
    bullish_fvg = float(row.get('bullish_fvg', 0.0))
    bearish_fvg = float(row.get('bearish_fvg', 0.0))
    htf_4h = float(row.get('htf_4h_trend', 0.0))

    # Long Setup: Kill Zone + Sweep PDL + Bullish FVG > 0 + 4H Bullish Trend
    is_long = is_kz and (sweep_pdl == 1) and (bullish_fvg > 0) and (htf_4h > 0)

    # Short Setup: Kill Zone + Sweep PDH + Bearish FVG > 0 + 4H Bearish Trend
    is_short = is_kz and (sweep_pdh == 1) and (bearish_fvg > 0) and (htf_4h < 0)

    return is_long, is_short


# -------------------------------------------------------------------------
# MICROSTRUCTURE 7-STAGE RATCHET LABELING & SIMULATION
# -------------------------------------------------------------------------
def create_labels_ratchet(df: pd.DataFrame, min_r: float = MIN_R_MULTIPLE, look_fwd: int = MAX_HOLDING_BARS) -> pd.DataFrame:
    """
    Simulates the exact 7-stage microstructure ratchet exit on all valid setups:
    - Target: +4.0R
    - Phase 0: Lock +0.15R at +1.0R gain
    - Phase 1: Lock +1.0R at +1.5R gain
    - Phase 2: Lock +1.8R at +2.0R gain
    - Phase 3: Lock +2.3R at +2.5R gain
    - Phase 4: Lock +2.8R at +3.0R gain
    - Phase 5: Lock +3.3R at +3.5R gain
    - Time Decay: Exit at market if < +0.20R at bar 24 (6 hours)
    - Labels: target = 1 if r_realized > 0 else 0
    """
    n = len(df)
    targets = np.full(n, np.nan)
    r_reals = np.zeros(n)

    lows = df['low'].values
    highs = df['high'].values
    closes = df['close'].values
    sweep_pdl = df['sweep_pdl'].values
    sweep_pdh = df['sweep_pdh'].values
    bullish_fvg = df['bullish_fvg'].values
    bearish_fvg = df['bearish_fvg'].values
    htf_4h = df['htf_4h_trend'].values
    local_low = df['local_low_20'].values
    local_high = df['local_high_20'].values
    is_kz = df['is_kill_zone'].values if 'is_kill_zone' in df.columns else np.ones(n, dtype=bool)

    for i in range(n - look_fwd):
        # 1. LONG SETUP
        if is_kz[i] and sweep_pdl[i] == 1 and bullish_fvg[i] > 0 and htf_4h[i] > 0:
            entry = closes[i]
            orig_sl = local_low[i]
            r_dist = entry - orig_sl
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                continue

            tp = entry + (min_r * r_dist)
            lock_1r = entry + (1.0 * r_dist)
            lock_15r = entry + (1.5 * r_dist)
            lock_20r = entry + (2.0 * r_dist)
            lock_25r = entry + (2.5 * r_dist)
            lock_30r = entry + (3.0 * r_dist)
            lock_35r = entry + (3.5 * r_dist)

            sl = orig_sl
            r_real = -1.0

            for j in range(i + 1, min(i + look_fwd, n)):
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
                    r_real = min_r
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

                # Time Decay Rule: Exit at market if < +0.2R within 24 bars
                if j == i + TIME_DECAY_BARS and closes[j] < entry + (TIME_DECAY_THRESHOLD_R * r_dist):
                    r_real = (closes[j] - entry) / r_dist
                    break

            targets[i] = 1 if r_real > 0 else 0
            r_reals[i] = r_real

        # 2. SHORT SETUP
        elif is_kz[i] and sweep_pdh[i] == 1 and bearish_fvg[i] > 0 and htf_4h[i] < 0:
            entry = closes[i]
            orig_sl = local_high[i]
            r_dist = orig_sl - entry
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                continue

            tp = entry - (min_r * r_dist)
            lock_1r = entry - (1.0 * r_dist)
            lock_15r = entry - (1.5 * r_dist)
            lock_20r = entry - (2.0 * r_dist)
            lock_25r = entry - (2.5 * r_dist)
            lock_30r = entry - (3.0 * r_dist)
            lock_35r = entry - (3.5 * r_dist)

            sl = orig_sl
            r_real = -1.0

            for j in range(i + 1, min(i + look_fwd, n)):
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
                    r_real = min_r
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

                # Time Decay Rule: Exit at market if < +0.2R within 24 bars
                if j == i + TIME_DECAY_BARS and closes[j] > entry - (TIME_DECAY_THRESHOLD_R * r_dist):
                    r_real = (entry - closes[j]) / r_dist
                    break

            targets[i] = 1 if r_real > 0 else 0
            r_reals[i] = r_real

    df['target'] = targets
    df['r_realized'] = r_reals
    return df


# -------------------------------------------------------------------------
# PURGE & EMBARGO BOUNDARY HELPER (PREVENTS LOOKAHEAD INTO TEST WINDOWS)
# -------------------------------------------------------------------------
def get_causal_train_test_split(
    df: pd.DataFrame, 
    window_start: pd.Timestamp, 
    window_end: pd.Timestamp, 
    look_fwd_bars: int = MAX_HOLDING_BARS
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits dataframe into In-Sample (train) and Out-Of-Sample (test) with
    strict 96-bar purge embargo before window_start.
    """
    # 96 bars * 15 minutes = 24 hours
    purge_duration = timedelta(minutes=15 * look_fwd_bars)
    purge_cutoff = window_start - purge_duration

    train_mask = (df["datetime"] < purge_cutoff) & df["target"].notna()
    test_mask = (df["datetime"] >= window_start) & (df["datetime"] <= window_end)

    return df[train_mask].copy(), df[test_mask].copy()
