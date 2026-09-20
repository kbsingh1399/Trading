import numpy as np
from numba import njit
import pandas as pd
from typing import Tuple

@njit
def simulate_vwap_reversion_trades(
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    volumes: np.ndarray,
    timestamps: np.ndarray,
    dates: np.ndarray,
    hours: np.ndarray,
    minutes: np.ndarray,
    day_of_weeks: np.ndarray,
    trade_duration_bars: int = 30,
    vwap_z_threshold: float = 1.8
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(highs)
    
    max_trades = (n // 10) + 100
    
    features = np.zeros((max_trades, 7), dtype=np.float64)
    outcomes = np.zeros(max_trades, dtype=np.float64)
    timestamps_out = np.zeros(max_trades, dtype=np.int64)
    
    emas_200 = np.zeros(n)
    emas_200[0] = closes[0]
    alpha_200 = 2.0 / (200 + 1)
    
    vwaps = np.zeros(n)
    cum_vol = 0.0
    cum_vol_price = 0.0
    
    # We will use rolling 24-bar (6 hour) VWAP deviation standard deviation instead of the buggy EMA of variance
    vwap_devs = np.zeros(n)
    
    trs = np.zeros(n)
    atrs = np.zeros(n)
    
    for i in range(1, n):
        emas_200[i] = emas_200[i-1] + alpha_200 * (closes[i] - emas_200[i-1])
        
        # Reset VWAP daily
        if dates[i] != dates[i-1]:
            cum_vol = 0.0
            cum_vol_price = 0.0
            
        cum_vol += volumes[i]
        cum_vol_price += closes[i] * volumes[i]
        
        if cum_vol > 0:
            vwaps[i] = cum_vol_price / cum_vol
        else:
            vwaps[i] = closes[i]
            
        vwap_devs[i] = closes[i] - vwaps[i]
            
        tr1 = highs[i] - lows[i]
        tr2 = abs(highs[i] - closes[i-1])
        tr3 = abs(lows[i] - closes[i-1])
        trs[i] = max(tr1, max(tr2, tr3))
            
        if i >= 14:
            atrs[i] = np.mean(trs[i-13:i+1])
                
    trade_idx = 0
    i = 24
    
    while i < n - trade_duration_bars:
        
        # Calculate standard deviation of the last 24 bars of VWAP deviations
        std_dev = np.std(vwap_devs[i-23:i+1])
        if std_dev == 0:
            std_dev = 1e-9
            
        z_score = vwap_devs[i] / std_dev
        
        # MEAN REVERSION: Fade extreme moves
        if z_score < -vwap_z_threshold: # Price is way below VWAP -> BUY
            
            direction = 1.0
            entry = closes[i]
            
            # Target VWAP, stop is 1 ATR
            r_val = atrs[i] * 1.5
            sl = entry - r_val
            tp = entry + r_val * 2.0
            
            current_sl = sl
            
            features[trade_idx, 0] = direction
            features[trade_idx, 1] = z_score
            features[trade_idx, 2] = (entry - emas_200[i]) / (entry + 1e-9)
            features[trade_idx, 3] = float(hours[i])
            features[trade_idx, 4] = float(day_of_weeks[i])
            features[trade_idx, 5] = atrs[i] / (entry + 1e-9)
            features[trade_idx, 6] = volumes[i] / (np.mean(volumes[i-10:i+1]) + 1e-9)
            
            outcome_r = -1.0
            phase_0_locked = False
            phase_1_locked = False
            
            trade_end = min(n, i + trade_duration_bars)
            for k in range(i+1, trade_end):
                if k - i >= 24:
                    current_r = (closes[k] - entry) / r_val
                    if current_r < 0.2:
                        outcome_r = current_r
                        break
                
                if lows[k] <= current_sl:
                    outcome_r = (current_sl - entry) / r_val
                    break
                if highs[k] >= tp:
                    outcome_r = 2.0
                    break
                    
                current_gain = (closes[k] - entry) / r_val
                if not phase_0_locked and current_gain >= 0.8:
                    current_sl = entry + 0.15 * r_val
                    phase_0_locked = True
                if phase_0_locked and not phase_1_locked and current_gain >= 1.5:
                    current_sl = entry + 0.80 * r_val
                    phase_1_locked = True
                    
            if outcome_r == -1.0:
                outcome_r = (closes[trade_end-1] - entry) / r_val
                
            outcomes[trade_idx] = outcome_r
            timestamps_out[trade_idx] = timestamps[i]
            trade_idx += 1
            i += 10 # cooldown
            
        elif z_score > vwap_z_threshold: # Price is way above VWAP -> SELL
            
            direction = -1.0
            entry = closes[i]
            
            r_val = atrs[i] * 1.5
            sl = entry + r_val
            tp = entry - r_val * 2.0
            
            current_sl = sl
            
            features[trade_idx, 0] = direction
            features[trade_idx, 1] = z_score
            features[trade_idx, 2] = (entry - emas_200[i]) / (entry + 1e-9)
            features[trade_idx, 3] = float(hours[i])
            features[trade_idx, 4] = float(day_of_weeks[i])
            features[trade_idx, 5] = atrs[i] / (entry + 1e-9)
            features[trade_idx, 6] = volumes[i] / (np.mean(volumes[i-10:i+1]) + 1e-9)
            
            outcome_r = -1.0
            phase_0_locked = False
            phase_1_locked = False
            
            trade_end = min(n, i + trade_duration_bars)
            for k in range(i+1, trade_end):
                if k - i >= 24:
                    current_r = (entry - closes[k]) / r_val
                    if current_r < 0.2:
                        outcome_r = current_r
                        break
                
                if highs[k] >= current_sl:
                    outcome_r = (entry - current_sl) / r_val
                    break
                if lows[k] <= tp:
                    outcome_r = 2.0
                    break
                    
                current_gain = (entry - closes[k]) / r_val
                if not phase_0_locked and current_gain >= 0.8:
                    current_sl = entry - 0.15 * r_val
                    phase_0_locked = True
                if phase_0_locked and not phase_1_locked and current_gain >= 1.5:
                    current_sl = entry - 0.80 * r_val
                    phase_1_locked = True
                    
            if outcome_r == -1.0:
                outcome_r = (entry - closes[trade_end-1]) / r_val
                
            outcomes[trade_idx] = outcome_r
            timestamps_out[trade_idx] = timestamps[i]
            trade_idx += 1
            i += 10 # cooldown
            
        else:
            i += 1
        
    return features[:trade_idx], outcomes[:trade_idx], timestamps_out[:trade_idx]
