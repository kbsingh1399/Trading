import os
import sys
import pandas as pd
import numpy as np
import xgboost as xgb
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone
import logging

# Ensure Engine core is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.strategy_kernel import CANONICAL_FEATURES, compute_features_pandas, check_setup_criteria

MAX_SPREAD_ATR_RATIO_ENTER = 0.12  # Enter quarantine if spread > 12% of ATR
MAX_SPREAD_ATR_RATIO_EXIT = 0.08   # Exit quarantine only if spread < 8% of ATR
EXOTIC_SESSION_RESTRICTED = {
    'EURHUF', 'EURSEK', 'USDSEK', 'USDHKD', 'GAS', 'NICKEL', 'LEAD'
}


class StatefulInferenceEngine:
    def __init__(self, symbol: str, max_bars: int = 800):
        self.symbol = symbol
        self.max_bars = max_bars
        self.buffer: pd.DataFrame = pd.DataFrame()
        self.buffer_4h: pd.DataFrame = pd.DataFrame()
        self.buffer_d1: pd.DataFrame = pd.DataFrame()
        self.is_warm = False
        self.mt5_connection = None
        self.features_order = CANONICAL_FEATURES
        self.is_quarantined = False
        self.consecutive_safe_bars = 0

    def check_quarantine(self, spread: float, atr: float, current_utc_hour: int = 12) -> Tuple[bool, str]:
        """
        P1 Quarantine with Hysteresis & Session Time Filter:
        1. Exotic assets are strictly quarantined outside 07:00-17:00 UTC.
        2. Hysteresis band: enters quarantine if spread/atr > 0.12; exits only if spread/atr < 0.08 for 2 consecutive bars.
        """
        sym_clean = self.symbol.upper().replace(".PI", "").replace(".P", "").replace(".R", "")
        if sym_clean in EXOTIC_SESSION_RESTRICTED:
            if current_utc_hour < 7 or current_utc_hour >= 17:
                self.is_quarantined = True
                self.consecutive_safe_bars = 0
                return True, f"Quarantined (Exotic off-hours: {current_utc_hour:02d}:00 UTC outside 07-17 UTC)"

        if atr <= 0 or spread <= 0:
            return True, "Quarantined (Invalid spread/ATR <= 0)"

        ratio = spread / atr
        if not self.is_quarantined:
            if ratio > MAX_SPREAD_ATR_RATIO_ENTER:
                self.is_quarantined = True
                self.consecutive_safe_bars = 0
                return True, f"Quarantined (Spread/ATR {ratio:.1%} > {MAX_SPREAD_ATR_RATIO_ENTER:.0%})"
            return False, "Active"
        else:
            if ratio < MAX_SPREAD_ATR_RATIO_EXIT:
                self.consecutive_safe_bars += 1
                if self.consecutive_safe_bars >= 2:
                    self.is_quarantined = False
                    self.consecutive_safe_bars = 0
                    return False, "Active (Hysteresis Cleared)"
                return True, f"Quarantined (Clearing {self.consecutive_safe_bars}/2 bars: {ratio:.1%})"
            else:
                self.consecutive_safe_bars = 0
                return True, f"Quarantined (Spread/ATR {ratio:.1%} > {MAX_SPREAD_ATR_RATIO_EXIT:.0%})"

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

        # Warm-start 1D buffer for exact previous day high/low parity
        if hasattr(mt5_connection, 'get_1d_bars'):
            bars_1d_df = mt5_connection.get_1d_bars(self.symbol, count=20)
            if not bars_1d_df.empty:
                bars_1d_df = bars_1d_df.iloc[:-1].copy()
                if 'datetime' in bars_1d_df.columns:
                    bars_1d_df.set_index('datetime', inplace=True)
                elif 'time' in bars_1d_df.columns:
                    bars_1d_df['datetime'] = pd.to_datetime(bars_1d_df['time'], unit='s', utc=True)
                    bars_1d_df.set_index('datetime', inplace=True)
                self.buffer_d1 = bars_1d_df[['open', 'high', 'low', 'close']].copy()

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
        """Periodically refreshes 4H and 1D buffer from MT5 to keep trend and daily levels current."""
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

            if hasattr(self.mt5_connection, 'get_1d_bars'):
                bars_1d_df = self.mt5_connection.get_1d_bars(self.symbol, count=20)
                if not bars_1d_df.empty:
                    bars_1d_df = bars_1d_df.iloc[:-1].copy()
                    if 'datetime' in bars_1d_df.columns:
                        bars_1d_df.set_index('datetime', inplace=True)
                    elif 'time' in bars_1d_df.columns:
                        bars_1d_df['datetime'] = pd.to_datetime(bars_1d_df['time'], unit='s', utc=True)
                        bars_1d_df.set_index('datetime', inplace=True)
                    self.buffer_d1 = bars_1d_df[['open', 'high', 'low', 'close']].copy()

    def compute_features(self) -> pd.DataFrame:
        """Delegates feature calculation to canonical strategy kernel."""
        return compute_features_pandas(self.buffer, self.buffer_4h, self.buffer_d1)

    def predict(self, xgb_model: xgb.Booster) -> float:
        """Formats latest features into DMatrix and runs inference."""
        if self.buffer.empty:
            raise ValueError("Buffer is empty. Cannot predict.")

        features_df = self.compute_features()
        latest_features = features_df.iloc[[-1]][CANONICAL_FEATURES].copy()

        # Force float64 exactly
        for col in latest_features.columns:
            latest_features[col] = pd.to_numeric(latest_features[col], errors="coerce").astype(float)

        dmatrix = xgb.DMatrix(latest_features)
        prediction = xgb_model.predict(dmatrix)
        
        # Prevent C-level memory leak in high-frequency loops
        del dmatrix
        
        return float(prediction[0])

    def infer_next_bar(self, model: xgb.Booster, conn) -> Optional[Tuple[datetime, str, float, float, float]]:
        """
        Polls for newly closed 15m bar, updates rolling buffer, computes features,
        evaluates setup criteria, and returns (bar_time, direction, prob, spread, atr).
        """
        if not conn or not getattr(conn, 'connected', False):
            return None

        bars_df = conn.get_15m_bars(self.symbol, count=5)
        if bars_df.empty or len(bars_df) < 2:
            return None

        # The last completed closed bar is iloc[-2] (since iloc[-1] is the forming bar)
        closed_bar = bars_df.iloc[-2]
        if 'datetime' in closed_bar:
            bar_time = closed_bar['datetime']
        elif 'time' in closed_bar:
            bar_time = pd.to_datetime(closed_bar['time'], unit='s', utc=True)
        else:
            bar_time = datetime.now(timezone.utc)

        # Check if this bar is already in buffer
        if not self.buffer.empty and self.buffer.index[-1] == bar_time:
            pass
        else:
            bar_dict = {
                'datetime': bar_time,
                'open': float(closed_bar['open']),
                'high': float(closed_bar['high']),
                'low': float(closed_bar['low']),
                'close': float(closed_bar['close']),
                'volume': float(closed_bar.get('tick_volume', closed_bar.get('volume', 0.0)))
            }
            self.update_bar(bar_dict)

        if len(self.buffer) < 50:
            return None

        features_df = self.compute_features()
        if features_df.empty:
            return None

        latest_row = features_df.iloc[-1]
        trend = float(latest_row.get("htf_4h_trend", 0.0))
        bull_fvg = float(latest_row.get("bullish_fvg", 0.0))
        bear_fvg = float(latest_row.get("bearish_fvg", 0.0))

        prob = self.predict(model)

        dt = self.buffer.index[-1] if isinstance(self.buffer.index, pd.DatetimeIndex) else bar_time
        hour = dt.hour if hasattr(dt, 'hour') else 12
        is_kz = (7 <= hour <= 10) or (12 <= hour <= 15)

        tick = conn.get_last_tick(self.symbol)
        spread = float(tick.ask - tick.bid) if tick else 0.0
        atr = float(latest_row.get("atr_14", 0.001))

        # Check quarantine
        is_quarantined, _ = self.check_quarantine(spread, atr, current_utc_hour=hour)
        if is_quarantined:
            return bar_time, "HOLD", prob, spread, atr

        direction = "HOLD"
        is_long, is_short = check_setup_criteria(latest_row.to_dict())
        if is_long:
            direction = "BUY"
        elif is_short:
            direction = "SELL"

        return bar_time, direction, prob, spread, atr
