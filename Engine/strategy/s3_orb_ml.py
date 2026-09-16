import numpy as np
from numba import njit
import pandas as pd
from typing import Tuple

@njit
def simulate_orb_trades(
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    volumes: np.ndarray,
    timestamps: np.ndarray,
    dates: np.ndarray,
    hours: np.ndarray,
    minutes: np.ndarray,
    day_of_weeks: np.ndarray,
    start_hour: int,
    start_minute: int,
    range_duration_bars: int = 2,
    trade_duration_bars: int = 16
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Numba-accelerated ORB trade simulator.
    Returns:
       features: [trade_count, 7] -> [dir, range_pct, rsi, vwap_dist, ema_dist, hour, dow]
       outcomes: [trade_count] -> 1 (win) or 0 (loss)
       timestamps_out: [trade_count] -> the timestamp of the trade for time filtering
    """
    n = len(highs)
    
    # Pre-allocate output arrays safely (max 1 trade per day roughly, but varying session lengths)
    max_trades = (n // 10) + 100
    features = np.zeros((max_trades, 7), dtype=np.float64)
    outcomes = np.zeros(max_trades, dtype=np.float64)
    timestamps_out = np.zeros(max_trades, dtype=np.int64)
    
    # Simple arrays for technicals
    emas = np.zeros(n)
    emas[0] = closes[0]
    alpha = 2.0 / (50 + 1)
    
    vwaps = np.zeros(n)
    cum_vol = 0.0
    cum_vol_price = 0.0
    
    # Simple RSI computation
    gains = np.zeros(n)
    losses = np.zeros(n)
    rsis = np.zeros(n)
    
    for i in range(1, n):
        emas[i] = emas[i-1] + alpha * (closes[i] - emas[i-1])
        
        cum_vol += volumes[i]
        cum_vol_price += closes[i] * volumes[i]
        if cum_vol > 0:
            vwaps[i] = cum_vol_price / cum_vol
        else:
            vwaps[i] = closes[i]
            
        change = closes[i] - closes[i-1]
        if change > 0:
            gains[i] = change
        else:
            losses[i] = -change
            
        if i >= 14:
            avg_gain = np.mean(gains[i-13:i+1])
            avg_loss = np.mean(losses[i-13:i+1])
            if avg_loss == 0:
                rsis[i] = 100.0
            else:
                rs = avg_gain / avg_loss
                rsis[i] = 100.0 - (100.0 / (1.0 + rs))
    
    trade_idx = 0
    i = 0
    
    while i < n - range_duration_bars:
        # Find start of session
        if hours[i] == start_hour and minutes[i] == start_minute:
            # Found opening range
            or_high = highs[i]
            or_low = lows[i]
            
            for j in range(1, range_duration_bars):
                if highs[i+j] > or_high: or_high = highs[i+j]
                if lows[i+j] < or_low: or_low = lows[i+j]
                
            or_range = or_high - or_low
            
            if or_range > 0:
                trade_start = i + range_duration_bars
                trade_end = min(n, trade_start + trade_duration_bars)
                
                for j in range(trade_start, trade_end):
                    if highs[j] > or_high:
                        # Long breakout
                        direction = 1.0
                        entry = or_high
                        sl = or_low
                        tp = entry + 1.5 * or_range
                        
                        prev_idx = j - 1
                        v_dist = (closes[prev_idx] - vwaps[prev_idx]) / (closes[prev_idx] + 1e-9)
                        e_dist = (closes[prev_idx] - emas[prev_idx]) / (closes[prev_idx] + 1e-9)
                        
                        features[trade_idx, 0] = direction
                        features[trade_idx, 1] = or_range / (or_low + 1e-9)
                        features[trade_idx, 2] = rsis[prev_idx]
                        features[trade_idx, 3] = v_dist
                        features[trade_idx, 4] = e_dist
                        features[trade_idx, 5] = float(hours[prev_idx])
                        features[trade_idx, 6] = float(day_of_weeks[prev_idx])
                        
                        # Simulate forward
                        outcome = 0.0
                        for k in range(j, trade_end):
                            if lows[k] <= sl:
                                outcome = 0.0
                                break
                            if highs[k] >= tp:
                                outcome = 1.0
                                break
                        
                        outcomes[trade_idx] = outcome
                        timestamps_out[trade_idx] = timestamps[j]
                        trade_idx += 1
                        i = trade_end # Skip to end of window
                        break
                        
                    elif lows[j] < or_low:
                        # Short breakout
                        direction = -1.0
                        entry = or_low
                        sl = or_high
                        tp = entry - 1.5 * or_range
                        
                        prev_idx = j - 1
                        v_dist = (closes[prev_idx] - vwaps[prev_idx]) / (closes[prev_idx] + 1e-9)
                        e_dist = (closes[prev_idx] - emas[prev_idx]) / (closes[prev_idx] + 1e-9)
                        
                        features[trade_idx, 0] = direction
                        features[trade_idx, 1] = or_range / (or_low + 1e-9)
                        features[trade_idx, 2] = rsis[prev_idx]
                        features[trade_idx, 3] = v_dist
                        features[trade_idx, 4] = e_dist
                        features[trade_idx, 5] = float(hours[prev_idx])
                        features[trade_idx, 6] = float(day_of_weeks[prev_idx])
                        
                        outcome = 0.0
                        for k in range(j, trade_end):
                            if highs[k] >= sl:
                                outcome = 0.0
                                break
                            if lows[k] <= tp:
                                outcome = 1.0
                                break
                        
                        outcomes[trade_idx] = outcome
                        timestamps_out[trade_idx] = timestamps[j]
                        trade_idx += 1
                        i = trade_end
                        break
        i += 1
        
    return features[:trade_idx], outcomes[:trade_idx], timestamps_out[:trade_idx]
