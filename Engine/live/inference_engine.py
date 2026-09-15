import pandas as pd
import numpy as np
import xgboost as xgb
from typing import Dict, Any, Optional
import logging

class StatefulInferenceEngine:
    def __init__(self, symbol: str, max_bars: int = 250):
        self.symbol = symbol
        self.max_bars = max_bars
        self.buffer: pd.DataFrame = pd.DataFrame()
        self.buffer_4h: pd.DataFrame = pd.DataFrame()
        self.is_warm = False
        self.mt5_connection = None
        self.features_order = [
            "bullish_fvg", "bearish_fvg", "htf_4h_trend", "hour", "day_of_week",
            "rsi_14", "vwap_dist", "ema_50_dist", "ema_200_dist", "ema_200_slope",
            "atr_14", "volatility_20", "roc_20"
        ]
        
    def warm_start(self, mt5_connection) -> bool:
        """
        CRITICAL: Seeds the rolling buffer with the last `max_bars` CLOSED 15m bars
        and fetches 4H bars for htf_4h_trend.
        """
        self.mt5_connection = mt5_connection
        logging.info(f"[{self.symbol}] Warm-starting 15m buffer with last {self.max_bars} bars from MT5...")
        
        bars_df = mt5_connection.get_15m_bars(self.symbol, count=self.max_bars)
        
        if bars_df.empty or len(bars_df) < 50:
            logging.error(f"[{self.symbol}] Warm start 15m FAILED")
            return False
        
        bars_df = bars_df.iloc[:-1]
        
        if 'time' in bars_df.columns:
            bars_df = bars_df.rename(columns={'time': 'timestamp'})
        if 'timestamp' in bars_df.columns:
            bars_df.set_index('timestamp', inplace=True)
            
        col_map = {'tick_volume': 'volume'}
        bars_df.rename(columns={k: v for k, v in col_map.items() if k in bars_df.columns}, inplace=True)
        
        self.buffer = bars_df[['open', 'high', 'low', 'close', 'volume']].copy()
        
        logging.info(f"[{self.symbol}] Warm-starting 4h buffer with last 250 bars from MT5...")
        bars_4h_df = mt5_connection.get_4h_bars(self.symbol, count=250)
        
        if bars_4h_df.empty or len(bars_4h_df) < 205:
            logging.warning(f"[{self.symbol}] Warm start 4h warning: not enough bars for EMA200.")
            
        if not bars_4h_df.empty:
            bars_4h_df = bars_4h_df.iloc[:-1]
            if 'time' in bars_4h_df.columns:
                bars_4h_df = bars_4h_df.rename(columns={'time': 'timestamp'})
            if 'timestamp' in bars_4h_df.columns:
                bars_4h_df.set_index('timestamp', inplace=True)
            self.buffer_4h = bars_4h_df.copy()
        
        self.is_warm = True
        logging.info(f"[{self.symbol}] Buffer warm-started successfully.")
        return True
        
    def update_bar(self, new_bar: Dict[str, float]) -> None:
        new_df = pd.DataFrame([new_bar])
        if 'timestamp' in new_df.columns:
            new_df.set_index('timestamp', inplace=True)
            
        if self.buffer.empty:
            self.buffer = new_df
        else:
            self.buffer = pd.concat([self.buffer, new_df])
            if len(self.buffer) > self.max_bars:
                self.buffer = self.buffer.iloc[-self.max_bars:]
                
    def compute_features(self) -> pd.DataFrame:
        df = self.buffer.copy()
        
        if len(df) == 0:
            return df
            
        # 1. EMAs
        df['ema_50'] = df['close'].ewm(span=50, min_periods=1, adjust=False).mean()
        df['ema_200'] = df['close'].ewm(span=200, min_periods=1, adjust=False).mean()
        
        # 2. RSI (14) - matching polars formula
        delta = df['close'].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, abs(delta), 0)
        gain_s = pd.Series(gain, index=df.index).ewm(span=14, adjust=False).mean()
        loss_s = pd.Series(loss, index=df.index).ewm(span=14, adjust=False).mean()
        
        # Avoid division by zero
        rs = np.where(loss_s == 0, np.inf, gain_s / loss_s)
        df['rsi_14'] = 100.0 - (100.0 / (1.0 + rs))
        df['rsi_14'] = df['rsi_14'].replace(np.inf, 100.0)
        
        # 3. VWAP (20) - matching s2_ict_ml_forex (simple rolling mean of typical price)
        typical_price = (df['high'] + df['low'] + df['close']) / 3.0
        vwap_20 = typical_price.rolling(window=20).mean()
        df['vwap_dist'] = (df['close'] - vwap_20) / vwap_20
        
        # 4. ICT Features: FVGs (Gap magnitude, NOT binary)
        df['prev_2_high'] = df['high'].shift(2)
        df['prev_2_low'] = df['low'].shift(2)
        
        df['bullish_fvg'] = np.where(df['low'] > df['prev_2_high'], df['low'] - df['prev_2_high'], 0.0)
        df['bearish_fvg'] = np.where(df['high'] < df['prev_2_low'], df['prev_2_low'] - df['high'], 0.0)
        
        # 5. Distances & Slopes
        df['ema_50_dist'] = (df['close'] - df['ema_50']) / df['ema_50']
        df['ema_200_dist'] = (df['close'] - df['ema_200']) / df['ema_200']
        df['ema_200_slope'] = df['ema_200'] - df['ema_200'].shift(12)
        
        # 6. ATR & Volatility
        df['atr_14'] = (df['high'] - df['low']).rolling(window=14).mean()
        df['volatility_20'] = df['close'].rolling(window=20).std() / df['close']
        df['roc_20'] = (df['close'] / df['close'].shift(20)) - 1.0
        
        # 7. Time Features (Polars dt.weekday() is 1-7, Pandas is 0-6)
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek + 1
        
        # 8. HTF 4H Trend
        htf_4h_trend_val = 0.0
        if self.mt5_connection and self.mt5_connection.connected:
            bars_4h_df = self.mt5_connection.get_4h_bars(self.symbol, count=250)
            if not bars_4h_df.empty:
                bars_4h_df = bars_4h_df.iloc[:-1]
                bars_4h_df['ema_200_4h'] = bars_4h_df['close'].ewm(span=200, adjust=False).mean()
                bars_4h_df['htf_4h_trend'] = bars_4h_df['ema_200_4h'] - bars_4h_df['ema_200_4h'].shift(5)
                htf_4h_trend_val = bars_4h_df['htf_4h_trend'].iloc[-1]
                self.buffer_4h = bars_4h_df
        else:
            if not self.buffer_4h.empty:
                self.buffer_4h['ema_200_4h'] = self.buffer_4h['close'].ewm(span=200, adjust=False).mean()
                self.buffer_4h['htf_4h_trend'] = self.buffer_4h['ema_200_4h'] - self.buffer_4h['ema_200_4h'].shift(5)
                htf_4h_trend_val = self.buffer_4h['htf_4h_trend'].iloc[-1]
                
        df['htf_4h_trend'] = htf_4h_trend_val
        
        # Cleanup
        df.drop(columns=['ema_50', 'ema_200', 'prev_2_high', 'prev_2_low'], inplace=True, errors='ignore')
        
        # Fill NaNs
        df.fillna(0.0, inplace=True)
        
        return df[self.features_order]

    def predict(self, xgb_model: xgb.Booster) -> float:
        if self.buffer.empty:
            raise ValueError("Buffer is empty. Cannot predict.")
            
        features_df = self.compute_features()
        latest_features = features_df.iloc[[-1]].copy()
        
        # Force float64 exactly
        for col in latest_features.columns:
            latest_features[col] = pd.to_numeric(latest_features[col], errors="coerce").astype(float)
        
        dmatrix = xgb.DMatrix(latest_features)
        prediction = xgb_model.predict(dmatrix)
        
        return float(prediction[0])
