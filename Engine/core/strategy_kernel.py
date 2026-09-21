"""
================================================================================
ENGINE CORE: CANONICAL STRATEGY KERNEL (FOREX & CFD ML SUITE)
================================================================================
Single source of truth for:
1. 13 Canonical Stationary Features (Polars batch & Pandas streaming).
2. Strictly causal 4H As-Of Join with shift(1) to eliminate 3h45m lookahead.
3. Strictly causal Daily PDH/PDL with shift(1).
4. Microstructure 3-Phase Ratchet Exit Simulation with 24-bar time decay and MTM exhaustion.
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

MIN_R_MULTIPLE = 2.5
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
def compute_features_pandas(buffer_15m: pd.DataFrame, buffer_4h: Optional[pd.DataFrame] = None, buffer_d1: Optional[pd.DataFrame] = None) -> pd.DataFrame:
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

    # Calculate sweeps
    if buffer_d1 is not None and not buffer_d1.empty and isinstance(df.index, pd.DatetimeIndex):
        # buffer_d1 contains completed daily bars.
        # Each completed day T-1 is available at start of day T (00:00:00 UTC of next day).
        # We index by availability time (index + 1 day) so merge_asof direction='backward'
        # causally joins each 15m bar with the most recently completed day's high/low without double-lag!
        bd = buffer_d1.copy()
        if 'datetime' in bd.columns:
            bd.set_index('datetime', inplace=True)
        bd = bd.sort_index()
        
        # Availability time = start of next day (00:00 UTC of next day)
        bd_avail = pd.DataFrame(index=bd.index + pd.Timedelta(days=1))
        bd_avail['prev_day_high'] = bd['high'].values
        bd_avail['prev_day_low'] = bd['low'].values
        
        # Backward join — normalize datetime resolution to avoid MergeError
        left = df.reset_index()
        left_dt_col = [c for c in left.columns if c not in df.columns][0]  # whatever reset_index named it
        left = left.rename(columns={left_dt_col: '_dt'})
        left['_dt'] = pd.to_datetime(left['_dt'], utc=True).astype('datetime64[us, UTC]')
        right = bd_avail.reset_index()
        right_dt_col = [c for c in right.columns if c not in bd_avail.columns][0]
        right = right.rename(columns={right_dt_col: '_dt'})
        right['_dt'] = pd.to_datetime(right['_dt'], utc=True).astype('datetime64[us, UTC]')
        merged = pd.merge_asof(
            left, right,
            on='_dt',
            direction='backward'
        )
        merged.set_index('_dt', inplace=True)
        merged.index.name = df.index.name  # restore original index name
        
        df['sweep_pdl'] = (df['low'] <= merged['prev_day_low']).astype(int)
        df['sweep_pdh'] = (df['high'] >= merged['prev_day_high']).astype(int)
    elif isinstance(df.index, pd.DatetimeIndex):
        daily = df.groupby(df.index.date).agg({'high': 'max', 'low': 'min'}).shift(1)
        dates = df.index.date
        prev_highs = pd.Series(dates, index=df.index).map(daily['high']).ffill()
        prev_lows = pd.Series(dates, index=df.index).map(daily['low']).ffill()
        df['sweep_pdl'] = (df['low'] <= prev_lows).astype(int)
        df['sweep_pdh'] = (df['high'] >= prev_highs).astype(int)
    else:
        df['sweep_pdl'] = 0
        df['sweep_pdh'] = 0

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
    if buffer_4h is not None and not buffer_4h.empty and len(buffer_4h) >= 205 and isinstance(df.index, pd.DatetimeIndex):
        b4h = buffer_4h.copy()
        if 'datetime' in b4h.columns:
            b4h.set_index('datetime', inplace=True)
        b4h = b4h.sort_index()
        b4h['ema_200_4h'] = b4h['close'].ewm(span=200, adjust=False).mean()
        b4h['htf_4h_trend'] = b4h['ema_200_4h'] - b4h['ema_200_4h'].shift(5)
        
        # Availability time = start of next 4H window (+4 hours)
        b4h_avail = pd.DataFrame(index=b4h.index + pd.Timedelta(hours=4))
        b4h_avail['htf_4h_trend'] = b4h['htf_4h_trend'].values
        # Normalize datetime resolution to avoid MergeError
        left_4h = df.reset_index()
        left_4h_dt_col = [c for c in left_4h.columns if c not in df.columns][0]
        left_4h = left_4h.rename(columns={left_4h_dt_col: '_dt'})
        left_4h['_dt'] = pd.to_datetime(left_4h['_dt'], utc=True).astype('datetime64[us, UTC]')
        right_4h = b4h_avail.reset_index()
        right_4h_dt_col = [c for c in right_4h.columns if c not in b4h_avail.columns][0]
        right_4h = right_4h.rename(columns={right_4h_dt_col: '_dt'})
        right_4h['_dt'] = pd.to_datetime(right_4h['_dt'], utc=True).astype('datetime64[us, UTC]')
        merged_4h = pd.merge_asof(
            left_4h, right_4h,
            on='_dt',
            direction='backward'
        )
        merged_4h.set_index('_dt', inplace=True)
        merged_4h.index.name = df.index.name
        df['htf_4h_trend'] = merged_4h['htf_4h_trend'].fillna(0.0)
    elif buffer_4h is not None and not buffer_4h.empty and len(buffer_4h) >= 205:
        b4h = buffer_4h.copy()
        b4h['ema_200_4h'] = b4h['close'].ewm(span=200, adjust=False).mean()
        b4h['htf_4h_trend'] = b4h['ema_200_4h'] - b4h['ema_200_4h'].shift(5)
        valid_trends = b4h['htf_4h_trend'].dropna()
        df['htf_4h_trend'] = float(valid_trends.iloc[-1]) if len(valid_trends) > 0 else 0.0
    else:
        df['htf_4h_trend'] = 0.0

    df.fillna(0.0, inplace=True)
    return df


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
    Simulates the exact 3-phase microstructure ratchet exit on all valid setups:
    - Target: +2.5R (MIN_R_MULTIPLE)
    - Phase 0: Lock +0.15R at +0.8R gain (BE lock)
    - Phase 1: Lock +0.80R at +1.5R gain (Profit lock)
    - Phase 2: Lock +1.80R at +2.0R gain
    - Time Decay: Exit at market if < +0.20R at bar 24 (6 hours)
    - Exhaustion: Mark-to-market at bar 96 if neither SL nor TP is hit
    - Labels: target = 1 if r_realized > 0 else 0
    """
    n = len(df)
    targets = np.full(n, np.nan)
    r_reals = np.zeros(n)

    lows = df['low'].values
    highs = df['high'].values
    closes = df['close'].values
    opens = df['open'].values
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
            if i + 1 >= n:
                continue
            entry = opens[i + 1]
            orig_sl = local_low[i]
            r_dist = entry - orig_sl
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                continue

            tp = entry + (min_r * r_dist)
            lock_08r = entry + (0.8 * r_dist)  # Phase-0 BE lock trigger (matches live manage_open_trades)
            lock_15r = entry + (1.5 * r_dist)
            lock_20r = entry + (2.0 * r_dist)

            sl = orig_sl
            r_real = -1.0
            exited = False

            for j in range(i + 1, min(i + look_fwd, n)):
                # Check Stop Loss hit first (conservative microstructure)
                if lows[j] <= sl:
                    r_real = round((sl - entry) / r_dist, 4)
                    exited = True
                    break

                # Check Take Profit hit
                if highs[j] >= tp:
                    r_real = min_r
                    exited = True
                    break

                # Ratchet updates
                if highs[j] >= lock_20r and sl < entry + (1.8 * r_dist):
                    sl = entry + (1.8 * r_dist)
                elif highs[j] >= lock_15r and sl < entry + (0.80 * r_dist):
                    sl = entry + (0.80 * r_dist)
                elif highs[j] >= lock_08r and sl < entry + (0.15 * r_dist):
                    sl = entry + (0.15 * r_dist)

                # Time Decay Rule: Exit at market if < +0.2R within 24 bars
                if j == i + TIME_DECAY_BARS and closes[j] < entry + (TIME_DECAY_THRESHOLD_R * r_dist):
                    r_real = round((closes[j] - entry) / r_dist, 4)
                    exited = True
                    break

            if not exited:
                # S-11 FIX: Mark-to-market exit on holding exhaustion (bar 96)
                j_last = min(i + look_fwd, n) - 1
                mtm_r = (closes[j_last] - entry) / r_dist
                locked_r = (sl - entry) / r_dist
                r_real = round(min(min_r, max(mtm_r, locked_r)), 4)

            # Deduct -0.08R transaction friction
            r_real = round(r_real - 0.08, 4)
            targets[i] = 1 if r_real > 0 else 0
            r_reals[i] = r_real

        # 2. SHORT SETUP
        elif is_kz[i] and sweep_pdh[i] == 1 and bearish_fvg[i] > 0 and htf_4h[i] < 0:
            if i + 1 >= n:
                continue
            entry = opens[i + 1]
            orig_sl = local_high[i]
            r_dist = orig_sl - entry
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                continue

            tp = entry - (min_r * r_dist)
            lock_08r = entry - (0.8 * r_dist)  # Phase-0 BE lock trigger (matches live manage_open_trades)
            lock_15r = entry - (1.5 * r_dist)
            lock_20r = entry - (2.0 * r_dist)

            sl = orig_sl
            r_real = -1.0
            exited = False

            for j in range(i + 1, min(i + look_fwd, n)):
                # Check Stop Loss hit first (conservative microstructure)
                if highs[j] >= sl:
                    r_real = round((entry - sl) / r_dist, 4)
                    exited = True
                    break

                # Check Take Profit hit
                if lows[j] <= tp:
                    r_real = min_r
                    exited = True
                    break

                # Ratchet updates
                if lows[j] <= lock_20r and sl > entry - (1.8 * r_dist):
                    sl = entry - (1.8 * r_dist)
                elif lows[j] <= lock_15r and sl > entry - (0.80 * r_dist):
                    sl = entry - (0.80 * r_dist)
                elif lows[j] <= lock_08r and sl > entry - (0.15 * r_dist):
                    sl = entry - (0.15 * r_dist)

                # Time Decay Rule: Exit at market if < +0.2R within 24 bars
                if j == i + TIME_DECAY_BARS and closes[j] > entry - (TIME_DECAY_THRESHOLD_R * r_dist):
                    r_real = round((entry - closes[j]) / r_dist, 4)
                    exited = True
                    break

            if not exited:
                # S-11 FIX: Mark-to-market exit on holding exhaustion (bar 96)
                j_last = min(i + look_fwd, n) - 1
                mtm_r = (entry - closes[j_last]) / r_dist
                locked_r = (entry - sl) / r_dist
                r_real = round(min(min_r, max(mtm_r, locked_r)), 4)

            # Deduct -0.08R transaction friction
            r_real = round(r_real - 0.08, 4)
            targets[i] = 1 if r_real > 0 else 0
            r_reals[i] = r_real

    df['target'] = targets
    df['r_realized'] = r_reals
    return df


# -------------------------------------------------------------------------
# UNIFIED LIVE-SPEC LABELING (OX61: single-shot principle-driven MANDATE 3 test)
# -------------------------------------------------------------------------
# Exit reason codes (shared convention with the ORB sleeve)
UX_SL = 0
UX_TP = 1
UX_DECAY = 2
UX_FRIDAY = 3

# Live 7-stage ratchet schedule: (gain trigger R, locked SL R) — mirrors
# OrderManager.manage_open_trades exactly (elif cascade takes highest stage).
UX_RATCHET = ((0.8, 0.15), (1.5, 0.80), (2.0, 1.80), (2.5, 2.30), (3.0, 2.80), (3.5, 3.30))
UX_MAX_R_EFF = 3.5


def _ux_exit_long(opens, highs, lows, closes, dows, hrs, mns, n, e, entry, sl0, tp, r):
    """Live-spec LONG exit. Returns (r_pre_friction, exit_j, reason) or None at data-end."""
    sl = sl0
    phase = 0
    highest = -1e9
    for j in range(e, n):
        o = opens[j]
        h = highs[j]
        low = lows[j]
        c = closes[j]
        if o <= sl:
            return (o - entry) / r, j, UX_SL
        if low <= sl:
            return (sl - entry) / r, j, UX_SL
        if h >= tp:
            return (tp - entry) / r, j, UX_TP
        if dows[j] == 4 and (hrs[j] > 20 or (hrs[j] == 20 and mns[j] >= 30)):
            return (c - entry) / r, j, UX_FRIDAY
        hr_now = (h - entry) / r
        if hr_now > highest:
            highest = hr_now
        if (j - e) >= TIME_DECAY_BARS and highest < TIME_DECAY_THRESHOLD_R:
            return (c - entry) / r, j, UX_DECAY
        upgraded = False
        for stage in range(6, 0, -1):
            trig, lock = UX_RATCHET[stage - 1]
            if hr_now >= trig and phase < stage:
                sl = entry + lock * r
                phase = stage
                upgraded = True
                break
        if upgraded and c < sl:
            return (sl - entry) / r, j, UX_SL
    return None


def _ux_exit_short(opens, highs, lows, closes, dows, hrs, mns, n, e, entry, sl0, tp, r):
    """Live-spec SHORT exit (mirror of long)."""
    sl = sl0
    phase = 0
    highest = -1e9
    for j in range(e, n):
        o = opens[j]
        h = highs[j]
        low = lows[j]
        c = closes[j]
        if o >= sl:
            return (entry - o) / r, j, UX_SL
        if h >= sl:
            return (entry - sl) / r, j, UX_SL
        if low <= tp:
            return (entry - tp) / r, j, UX_TP
        if dows[j] == 4 and (hrs[j] > 20 or (hrs[j] == 20 and mns[j] >= 30)):
            return (entry - c) / r, j, UX_FRIDAY
        hr_now = (entry - low) / r
        if hr_now > highest:
            highest = hr_now
        if (j - e) >= TIME_DECAY_BARS and highest < TIME_DECAY_THRESHOLD_R:
            return (entry - c) / r, j, UX_DECAY
        upgraded = False
        for stage in range(6, 0, -1):
            trig, lock = UX_RATCHET[stage - 1]
            if hr_now >= trig and phase < stage:
                sl = entry - lock * r
                phase = stage
                upgraded = True
                break
        if upgraded and c > sl:
            return (entry - sl) / r, j, UX_SL
    return None


def create_labels_unified(df: pd.DataFrame) -> pd.DataFrame:
    """Labels setups with live-spec exits (FVG swing stops are compatible).

    Entry predicate pre-committed and untouched. Exits mirror live exactly:
    swing-extreme SL with 1.5xATR floor (spread term provably dominated under
    the 12% live quarantine), structural TP with R_eff in [2.5, 3.5] + viability
    veto below 2.5, 6-lock ratchet on extremes, highest-R decay at 24 bars,
    Friday 20:30 closeout + Friday 18:00 entry veto, gap-aware unclamped stops,
    no bar-cap (data-end truncation yields NO label: boundary discipline).
    Emits target / r_realized / hold_bars / exit_reason (-1 = unlabeled).
    """
    n = len(df)
    targets = np.full(n, np.nan)
    r_reals = np.zeros(n)
    holds = np.zeros(n, dtype=np.int64)
    reasons = np.full(n, -1, dtype=np.int64)

    opens = df['open'].values
    highs = df['high'].values
    lows = df['low'].values
    closes = df['close'].values
    sweep_pdl = df['sweep_pdl'].values
    sweep_pdh = df['sweep_pdh'].values
    bullish_fvg = df['bullish_fvg'].values
    bearish_fvg = df['bearish_fvg'].values
    htf_4h = df['htf_4h_trend'].values
    local_low = df['local_low_20'].values
    local_high = df['local_high_20'].values
    atr14 = df['atr_14'].values
    is_kz = df['is_kill_zone'].values if 'is_kill_zone' in df.columns else np.ones(n, dtype=bool)
    dts = pd.to_datetime(df['datetime'])
    dows = dts.dt.weekday.values
    hrs = dts.dt.hour.values
    mns = dts.dt.minute.values

    for i in range(n):
        is_long = is_kz[i] and sweep_pdl[i] == 1 and bullish_fvg[i] > 0 and htf_4h[i] > 0
        is_short = is_kz[i] and sweep_pdh[i] == 1 and bearish_fvg[i] > 0 and htf_4h[i] < 0
        if not (is_long or is_short):
            continue
        e = i + 1
        if e >= n:
            continue
        if dows[e] == 4 and hrs[e] >= 18:
            continue  # Friday 18:00 UTC entry cutoff (live truth)
        entry = opens[e]
        if is_long:
            sl0 = local_low[i]
            r = entry - sl0
            floor = 1.5 * atr14[i]
            if r < floor:
                r = floor  # SL0 already structural; floor widens directly
                sl0 = entry - r
            if r <= 0 or (r / entry) > MAX_STOP_PCT:
                continue
            tp_struct = local_high[i]
            if tp_struct > entry:
                r_eff = (tp_struct - entry) / r
                if r_eff < MIN_R_MULTIPLE:
                    continue  # live viability veto
                tp = entry + min(r_eff, UX_MAX_R_EFF) * r
            else:
                tp = entry + MIN_R_MULTIPLE * r
            res = _ux_exit_long(opens, highs, lows, closes, dows, hrs, mns, n, e, entry, sl0, tp, r)
        else:
            sl0 = local_high[i]
            r = sl0 - entry
            floor = 1.5 * atr14[i]
            if r < floor:
                r = floor
                sl0 = entry + r
            if r <= 0 or (r / entry) > MAX_STOP_PCT:
                continue
            tp_struct = local_low[i]
            if tp_struct < entry:
                r_eff = (entry - tp_struct) / r
                if r_eff < MIN_R_MULTIPLE:
                    continue  # live viability veto
                tp = entry - min(r_eff, UX_MAX_R_EFF) * r
            else:
                tp = entry - MIN_R_MULTIPLE * r
            res = _ux_exit_short(opens, highs, lows, closes, dows, hrs, mns, n, e, entry, sl0, tp, r)
        if res is None:
            continue  # data-end truncation: NO label (boundary discipline)
        r_pre, exit_j, reason = res
        r_real = round(r_pre - 0.08, 4)
        targets[i] = 1 if r_real > 0 else 0
        r_reals[i] = r_real
        holds[i] = exit_j - e
        reasons[i] = reason

    df['target'] = targets
    df['r_realized'] = r_reals
    df['hold_bars'] = holds
    df['exit_reason'] = reasons
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
