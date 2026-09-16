import numpy as np
from numba import njit
import pandas as pd
from typing import Tuple

@njit
def simulate_orb_trades(
    opens: np.ndarray,
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
    trade_duration_bars: int = 30
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(highs)
    
    max_trades = (n // 10) + 100
    
    features = np.zeros((max_trades, 20), dtype=np.float64)
    outcomes = np.zeros(max_trades, dtype=np.float64) # This will now hold exact Net R instead of 1/0
    timestamps_out = np.zeros(max_trades, dtype=np.int64)
    
    emas_50 = np.zeros(n)
    emas_50[0] = closes[0]
    alpha_50 = 2.0 / (50 + 1)
    
    emas_200 = np.zeros(n)
    emas_200[0] = closes[0]
    alpha_200 = 2.0 / (200 + 1)
    
    vwaps = np.zeros(n)
    cum_vol = 0.0
    cum_vol_price = 0.0
    
    gains = np.zeros(n)
    losses = np.zeros(n)
    rsis = np.zeros(n)
    
    trs = np.zeros(n)
    atrs = np.zeros(n)
    
    vol_sma_20 = np.zeros(n)
    
    for i in range(1, n):
        emas_50[i] = emas_50[i-1] + alpha_50 * (closes[i] - emas_50[i-1])
        emas_200[i] = emas_200[i-1] + alpha_200 * (closes[i] - emas_200[i-1])
        
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
            
        tr1 = highs[i] - lows[i]
        tr2 = abs(highs[i] - closes[i-1])
        tr3 = abs(lows[i] - closes[i-1])
        trs[i] = max(tr1, max(tr2, tr3))
            
        if i >= 14:
            avg_gain = np.mean(gains[i-13:i+1])
            avg_loss = np.mean(losses[i-13:i+1])
            if avg_loss == 0:
                rsis[i] = 100.0
            else:
                rs = avg_gain / avg_loss
                rsis[i] = 100.0 - (100.0 / (1.0 + rs))
                
            atrs[i] = np.mean(trs[i-13:i+1])
            
        if i >= 20:
            vol_sma_20[i] = np.mean(volumes[i-19:i+1])
            if vol_sma_20[i] == 0:
                vol_sma_20[i] = 1.0
                
    trade_idx = 0
    i = 0
    
    prev_day_high = highs[0]
    prev_day_low = lows[0]
    curr_day_high = highs[0]
    curr_day_low = lows[0]
    curr_date = dates[0]
    
    while i < n - range_duration_bars:
        
        if dates[i] != curr_date:
            prev_day_high = curr_day_high
            prev_day_low = curr_day_low
            curr_date = dates[i]
            curr_day_high = highs[i]
            curr_day_low = lows[i]
        else:
            if highs[i] > curr_day_high: curr_day_high = highs[i]
            if lows[i] < curr_day_low: curr_day_low = lows[i]
            
        if hours[i] == start_hour and minutes[i] == start_minute:
            or_high = highs[i]
            or_low = lows[i]
            
            for j in range(1, range_duration_bars):
                if highs[i+j] > or_high: or_high = highs[i+j]
                if lows[i+j] < or_low: or_low = lows[i+j]
                
            or_range = or_high - or_low
            
            pdl_dist = (or_low - prev_day_low) / (prev_day_low + 1e-9)
            pdh_dist = (prev_day_high - or_high) / (prev_day_high + 1e-9)
            
            swept_pdl = 1.0 if or_low < prev_day_low else 0.0
            swept_pdh = 1.0 if or_high > prev_day_high else 0.0
            
            if or_range > 0:
                trade_start = i + range_duration_bars
                trade_end = min(n, trade_start + trade_duration_bars)
                
                min_prior_low = lows[i]
                max_prior_high = highs[i]
                for p in range(i, trade_start):
                    if lows[p] < min_prior_low: min_prior_low = lows[p]
                    if highs[p] > max_prior_high: max_prior_high = highs[p]
                
                for j in range(trade_start, trade_end):
                    if highs[j] > or_high:
                        # LONG FILTER
                        if swept_pdl == 1.0 or closes[j-1] > emas_200[j-1]:
                            direction = 1.0
                            entry = or_high
                            sl = or_low
                            
                            prev_idx = j - 1
                            r_val = max(or_range, 0.50 * atrs[prev_idx])
                            tp = entry + 2.5 * r_val
                            current_sl = sl
                            
                            v_dist = (closes[prev_idx] - vwaps[prev_idx]) / (closes[prev_idx] + 1e-9)
                            e50_dist = (closes[prev_idx] - emas_50[prev_idx]) / (closes[prev_idx] + 1e-9)
                            e200_dist = (closes[prev_idx] - emas_200[prev_idx]) / (closes[prev_idx] + 1e-9)
                            
                            e200_slope = 0.0
                            if prev_idx >= 10:
                                e200_slope = (emas_200[prev_idx] - emas_200[prev_idx-10]) / (emas_200[prev_idx-10] + 1e-9)
                                
                            atr_pct = atrs[prev_idx] / (closes[prev_idx] + 1e-9)
                            vol_spike = volumes[j] / (vol_sma_20[prev_idx] + 1e-9)
                            range_atr = or_range / (atrs[prev_idx] + 1e-9)
                            
                            # CRT Features
                            body_ratio = abs(closes[j] - opens[j]) / (highs[j] - lows[j] + 1e-9)
                            close_outside = 1.0 if closes[j] > or_high else 0.0
                            fvg_expansion = 1.0 if (j >= 2 and lows[j] > highs[j-2]) else 0.0
                            judas_sweep = 1.0 if min_prior_low < or_low else 0.0
                            
                            features[trade_idx, 0] = direction
                            features[trade_idx, 1] = or_range / (or_low + 1e-9)
                            features[trade_idx, 2] = rsis[prev_idx]
                            features[trade_idx, 3] = v_dist
                            features[trade_idx, 4] = e50_dist
                            features[trade_idx, 5] = float(hours[prev_idx])
                            features[trade_idx, 6] = float(day_of_weeks[prev_idx])
                            features[trade_idx, 7] = e200_dist
                            features[trade_idx, 8] = e200_slope
                            features[trade_idx, 9] = atr_pct
                            features[trade_idx, 10] = vol_spike
                            features[trade_idx, 11] = range_atr
                            features[trade_idx, 12] = pdl_dist
                            features[trade_idx, 13] = pdh_dist
                            features[trade_idx, 14] = swept_pdl
                            features[trade_idx, 15] = swept_pdh
                            features[trade_idx, 16] = body_ratio
                            features[trade_idx, 17] = close_outside
                            features[trade_idx, 18] = fvg_expansion
                            features[trade_idx, 19] = judas_sweep
                            
                            outcome_r = -1.0 # Default loss
                            phase_0_locked = False
                            phase_1_locked = False
                            
                            for k in range(j, trade_end):
                                # Time decay check: 24 bars
                                if k - j >= 24:
                                    current_r = (closes[k] - entry) / r_val
                                    if current_r < 0.2:
                                        outcome_r = current_r
                                        break
                                
                                # Check stops and TPs
                                if lows[k] <= current_sl:
                                    outcome_r = (current_sl - entry) / r_val
                                    break
                                if highs[k] >= tp:
                                    outcome_r = 2.5
                                    break
                                    
                                # Check ratchets based on bar close
                                current_gain = (closes[k] - entry) / r_val
                                if not phase_0_locked and current_gain >= 0.8:
                                    current_sl = entry + 0.15 * r_val
                                    phase_0_locked = True
                                if phase_0_locked and not phase_1_locked and current_gain >= 1.5:
                                    current_sl = entry + 0.80 * r_val
                                    phase_1_locked = True
                                    
                            if outcome_r == -1.0:
                                outcome_r = (closes[trade_end-1] - entry) / r_val
                                
                            outcomes[trade_idx] = max(-1.15, min(2.5, outcome_r))
                            timestamps_out[trade_idx] = timestamps[j]
                            trade_idx += 1
                        i = trade_end
                        break
                        
                    elif lows[j] < or_low:
                        # SHORT FILTER
                        if swept_pdh == 1.0 or closes[j-1] < emas_200[j-1]:
                            direction = -1.0
                            entry = or_low
                            sl = or_high
                            
                            prev_idx = j - 1
                            r_val = max(or_range, 0.50 * atrs[prev_idx])
                            tp = entry - 2.5 * r_val
                            current_sl = sl
                            
                            v_dist = (closes[prev_idx] - vwaps[prev_idx]) / (closes[prev_idx] + 1e-9)
                            e50_dist = (closes[prev_idx] - emas_50[prev_idx]) / (closes[prev_idx] + 1e-9)
                            e200_dist = (closes[prev_idx] - emas_200[prev_idx]) / (closes[prev_idx] + 1e-9)
                            
                            e200_slope = 0.0
                            if prev_idx >= 10:
                                e200_slope = (emas_200[prev_idx] - emas_200[prev_idx-10]) / (emas_200[prev_idx-10] + 1e-9)
                                
                            atr_pct = atrs[prev_idx] / (closes[prev_idx] + 1e-9)
                            vol_spike = volumes[j] / (vol_sma_20[prev_idx] + 1e-9)
                            range_atr = or_range / (atrs[prev_idx] + 1e-9)
                            
                            # CRT Features
                            body_ratio = abs(closes[j] - opens[j]) / (highs[j] - lows[j] + 1e-9)
                            close_outside = 1.0 if closes[j] < or_low else 0.0
                            fvg_expansion = 1.0 if (j >= 2 and highs[j] < lows[j-2]) else 0.0
                            judas_sweep = 1.0 if max_prior_high > or_high else 0.0
                            
                            features[trade_idx, 0] = direction
                            features[trade_idx, 1] = or_range / (or_low + 1e-9)
                            features[trade_idx, 2] = rsis[prev_idx]
                            features[trade_idx, 3] = v_dist
                            features[trade_idx, 4] = e50_dist
                            features[trade_idx, 5] = float(hours[prev_idx])
                            features[trade_idx, 6] = float(day_of_weeks[prev_idx])
                            features[trade_idx, 7] = e200_dist
                            features[trade_idx, 8] = e200_slope
                            features[trade_idx, 9] = atr_pct
                            features[trade_idx, 10] = vol_spike
                            features[trade_idx, 11] = range_atr
                            features[trade_idx, 12] = pdl_dist
                            features[trade_idx, 13] = pdh_dist
                            features[trade_idx, 14] = swept_pdl
                            features[trade_idx, 15] = swept_pdh
                            features[trade_idx, 16] = body_ratio
                            features[trade_idx, 17] = close_outside
                            features[trade_idx, 18] = fvg_expansion
                            features[trade_idx, 19] = judas_sweep
                            
                            outcome_r = -1.0
                            phase_0_locked = False
                            phase_1_locked = False
                            
                            for k in range(j, trade_end):
                                if k - j >= 24:
                                    current_r = (entry - closes[k]) / r_val
                                    if current_r < 0.2:
                                        outcome_r = current_r
                                        break
                                
                                if highs[k] >= current_sl:
                                    outcome_r = (entry - current_sl) / r_val
                                    break
                                if lows[k] <= tp:
                                    outcome_r = 2.5
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
                            
                            outcomes[trade_idx] = max(-1.15, min(2.5, outcome_r))
                            timestamps_out[trade_idx] = timestamps[j]
                            trade_idx += 1
                        i = trade_end
                        break
        i += 1
        
    return features[:trade_idx], outcomes[:trade_idx], timestamps_out[:trade_idx]
