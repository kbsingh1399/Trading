import os
import sys
import pandas as pd
import numpy as np
import xgboost as xgb
from typing import Dict, Any, Optional
import logging

# Ensure Engine core is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.strategy_kernel import CANONICAL_FEATURES, compute_features_pandas


class StatefulInferenceEngine:
    def __init__(self, symbol: str, max_bars: int = 250):
        self.symbol = symbol
        self.max_bars = max_bars
        self.buffer: pd.DataFrame = pd.DataFrame()
        self.buffer_4h: pd.DataFrame = pd.DataFrame()
        self.is_warm = False
        self.mt5_connection = None
        self.features_order = CANONICAL_FEATURES

    def warm_start(self, mt5_connection) -> bool:
        """
        Seeds rolling buffers with last closed 15m and 4H bars in true UTC.
        """
        self.mt5_connection = mt5_connection
        logging.info(f"[{self.symbol}] Warm-starting 15m buffer with last {self.max_bars} bars from MT5...")

        bars_df = mt5_connection.get_15m_bars(self.symbol, count=self.max_bars)
        if bars_df.empty or len(bars_df) < 50:
            logging.error(f"[{self.symbol}] Warm start 15m FAILED")
            return False

        # Drop the current forming bar (last row) to keep strictly closed bars
        bars_df = bars_df.iloc[:-1].copy()

        # Ensure index is datetime in UTC
        if 'datetime' in bars_df.columns:
            bars_df.set_index('datetime', inplace=True)
        elif 'time' in bars_df.columns:
            bars_df['datetime'] = pd.to_datetime(bars_df['time'], unit='s', utc=True)
            bars_df.set_index('datetime', inplace=True)

        col_map = {'tick_volume': 'volume'}
        bars_df.rename(columns={k: v for k, v in col_map.items() if k in bars_df.columns}, inplace=True)

        self.buffer = bars_df[['open', 'high', 'low', 'close', 'volume']].copy()

        logging.info(f"[{self.symbol}] Warm-starting 4h buffer with last 250 bars from MT5...")
        bars_4h_df = mt5_connection.get_4h_bars(self.symbol, count=250)

        if bars_4h_df.empty or len(bars_4h_df) < 205:
            logging.warning(f"[{self.symbol}] Warm start 4h warning: not enough bars for EMA200.")

        if not bars_4h_df.empty:
            bars_4h_df = bars_4h_df.iloc[:-1].copy()
            if 'datetime' in bars_4h_df.columns:
                bars_4h_df.set_index('datetime', inplace=True)
            elif 'time' in bars_4h_df.columns:
                bars_4h_df['datetime'] = pd.to_datetime(bars_4h_df['time'], unit='s', utc=True)
                bars_4h_df.set_index('datetime', inplace=True)
            self.buffer_4h = bars_4h_df[['open', 'high', 'low', 'close']].copy()

        self.is_warm = True
        logging.info(f"[{self.symbol}] Buffer warm-started successfully.")
        return True

    def update_bar(self, new_bar: Dict[str, float]) -> None:
        """Appends a new closed bar to the rolling buffer."""
        new_df = pd.DataFrame([new_bar])
        if 'datetime' in new_df.columns:
            new_df.set_index('datetime', inplace=True)
        elif 'timestamp' in new_df.columns:
            new_df['datetime'] = pd.to_datetime(new_df['timestamp'], unit='s', utc=True) if isinstance(new_df['timestamp'].iloc[0], (int, float)) else pd.to_datetime(new_df['timestamp'], utc=True)
            new_df.set_index('datetime', inplace=True)

        if self.buffer.empty:
            self.buffer = new_df
        else:
            self.buffer = pd.concat([self.buffer, new_df])
            if len(self.buffer) > self.max_bars:
                self.buffer = self.buffer.iloc[-self.max_bars:].copy()

    def refresh_4h_buffer(self) -> None:
        """Periodically refreshes 4H buffer from MT5 to keep trend current."""
        if self.mt5_connection and self.mt5_connection.connected:
            bars_4h_df = self.mt5_connection.get_4h_bars(self.symbol, count=250)
            if not bars_4h_df.empty and len(bars_4h_df) >= 205:
                bars_4h_df = bars_4h_df.iloc[:-1].copy()
                if 'datetime' in bars_4h_df.columns:
                    bars_4h_df.set_index('datetime', inplace=True)
                elif 'time' in bars_4h_df.columns:
                    bars_4h_df['datetime'] = pd.to_datetime(bars_4h_df['time'], unit='s', utc=True)
                    bars_4h_df.set_index('datetime', inplace=True)
                self.buffer_4h = bars_4h_df[['open', 'high', 'low', 'close']].copy()

    def compute_features(self) -> pd.DataFrame:
        """Delegates feature calculation to canonical strategy kernel."""
        return compute_features_pandas(self.buffer, self.buffer_4h)

    def predict(self, xgb_model: xgb.Booster) -> float:
        """Formats latest features into DMatrix and runs inference."""
        if self.buffer.empty:
            raise ValueError("Buffer is empty. Cannot predict.")

        features_df = self.compute_features()
        latest_features = features_df.iloc[[-1]].copy()

        # Force float64 exactly
        for col in latest_features.columns:
            latest_features[col] = pd.to_numeric(latest_features[col], errors="coerce").astype(float)

        dmatrix = xgb.DMatrix(latest_features)
        prediction = xgb_model.predict(dmatrix)
        
        # Prevent C-level memory leak in high-frequency loops
        del dmatrix
        
        return float(prediction[0])
