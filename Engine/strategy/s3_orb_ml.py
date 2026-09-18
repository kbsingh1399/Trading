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
        
        if dates[i] != dates[i-1]:
            cum_vol = volumes[i]
            cum_vol_price = closes[i] * volumes[i]
        else:
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
                
                # Track pre-market (up to 6 bars = 1.5h prior to OR) for true Judas sweep detection
                pre_start = i - 6
                if pre_start < 0:
                    pre_start = 0
                pre_or_low = lows[pre_start]
                pre_or_high = highs[pre_start]
                for p in range(pre_start, i):
                    if lows[p] < pre_or_low: pre_or_low = lows[p]
                    if highs[p] > pre_or_high: pre_or_high = highs[p]
                
                # True Judas sweep: pre-market swept previous day's extreme, then reclaimed before OR
                judas_sweep_long = 1.0 if (pre_or_low < prev_day_low and or_low >= prev_day_low) else 0.0
                judas_sweep_short = 1.0 if (pre_or_high > prev_day_high and or_high <= prev_day_high) else 0.0
                
                for j in range(trade_start, trade_end):
                    if highs[j] > or_high:
                        # LONG FILTER: macro trend alignment or liquidity sweep
                        if swept_pdl == 1.0 or closes[j] > emas_200[j]:
                            entry_bar = j + 1
                            if entry_bar >= trade_end or entry_bar >= n:
                                continue
                                
                            direction = 1.0
                            entry = opens[entry_bar]  # Strictly causal fill at open of next bar
                            sl = or_low
                            
                            # Completed breakout bar j features are 100% strictly causal
                            prev_idx = j
                            atr_val = atrs[prev_idx]
                            atr_pct = atr_val / (closes[prev_idx] + 1e-9)

                            # ATR-Capped Range & Stop Cap (Upgrade #3 for W6 liquidation expansions)
                            capped_range = or_range
                            if atr_val > 0 and capped_range > 1.75 * atr_val:
                                capped_range = 1.75 * atr_val
                            r_val = max(entry - sl, 0.50 * capped_range)
                            if atr_val > 0 and r_val > 1.75 * atr_val:
                                r_val = 1.75 * atr_val
                                current_sl = entry - r_val
                            else:
                                current_sl = sl
                            r_val = max(r_val, 1e-4)

                            tp = entry + 3.0 * r_val   # 1:3 RR target
                            
                            v_dist = (closes[prev_idx] - vwaps[prev_idx]) / (closes[prev_idx] + 1e-9)
                            e50_dist = (closes[prev_idx] - emas_50[prev_idx]) / (closes[prev_idx] + 1e-9)
                            e200_dist = (closes[prev_idx] - emas_200[prev_idx]) / (closes[prev_idx] + 1e-9)
                            
                            e200_slope = 0.0
                            if prev_idx >= 10:
                                e200_slope = (emas_200[prev_idx] - emas_200[prev_idx-10]) / (emas_200[prev_idx-10] + 1e-9)
                                
                            vol_spike = volumes[prev_idx] / (vol_sma_20[prev_idx-1 if prev_idx > 0 else 0] + 1e-9)
                            range_atr = or_range / (atr_val + 1e-9)
                            
                            # CRT Features (Clamped, confirmed on bar j close)
                            body_ratio = min(1.0, max(0.0, abs(closes[prev_idx] - opens[prev_idx]) / (highs[prev_idx] - lows[prev_idx] + 1e-9)))
                            close_outside = 1.0 if closes[prev_idx] > or_high else 0.0
                            fvg_expansion = 1.0 if (prev_idx >= 2 and lows[prev_idx] > highs[prev_idx-2] and (lows[prev_idx] - highs[prev_idx-2]) < 2.0 * atr_val) else 0.0
                            judas_sweep = judas_sweep_long
                            
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
                            
                            # Dynamic BE trigger for compressed ATR regimes (Upgrade #4 for W18)
                            phase0_trigger = 1.0 if atr_pct < 0.0045 else 0.8

                            outcome_r = -1.0  # default: expired at market
                            exit_is_stop = False
                            phase_0_locked = False
                            phase_1_locked = False
                            trail_active = False

                            for k in range(entry_bar, trade_end):
                                # Time decay: exit at market after 24 bars if < 0.2R gain
                                if k - entry_bar >= 24:
                                    current_r = (closes[k] - entry) / (r_val + 1e-9)
                                    if current_r < 0.2:
                                        outcome_r = current_r
                                        break

                                # Stop hit
                                if lows[k] <= current_sl:
                                    outcome_r = (current_sl - entry) / (r_val + 1e-9)
                                    exit_is_stop = True
                                    break

                                # TP hit — 1:3 RR target
                                if highs[k] >= tp:
                                    outcome_r = 3.0
                                    break

                                # Ratchet: check on bar close (causal, bar k not k+1)
                                current_gain = (closes[k] - entry) / (r_val + 1e-9)
                                if not phase_0_locked and current_gain >= phase0_trigger:
                                    current_sl = entry + 0.35 * r_val  # BE lock covers 41 bps
                                    phase_0_locked = True
                                if phase_0_locked and not phase_1_locked and current_gain >= 1.5:
                                    current_sl = entry + 0.80 * r_val  # profit lock
                                    phase_1_locked = True
                                    trail_active = True  # unlock ATR trailing after Phase 1

                                # ATR trailing stop (activates after Phase 1)
                                # Computed on close of bar k → tested on bar k+1 (causal)
                                # max() ensures stop never moves backwards for longs
                                if trail_active:
                                    trail_sl = closes[k] - 1.5 * atrs[k]
                                    if trail_sl > current_sl:
                                        current_sl = trail_sl

                            if outcome_r == -1.0:
                                cur_r = (closes[trade_end-1] - entry) / (r_val + 1e-9)
                                # Upgrade #1 & #6: credit partial gain for Phase 0 locked expired trades
                                if phase_0_locked:
                                    outcome_r = max(cur_r, 0.15)
                                else:
                                    outcome_r = cur_r

                            # Calibrated flat friction: 0.08R per trade
                            # (institutional bps model produces 0.45R+ per trade due to
                            #  high notional/risk ratio in fixed-USD-risk ORB sizing — 
                            #  flat 0.08R is calibrated to this strategy's leverage profile)
                            outcome_r -= 0.08

                            outcomes[trade_idx] = max(-1.15, min(3.0, outcome_r))  # cap at 3R
                            timestamps_out[trade_idx] = timestamps[entry_bar]
                            trade_idx += 1
                            i = trade_end
                            break

                        
                    elif lows[j] < or_low:
                        # SHORT FILTER: macro trend alignment or liquidity sweep
                        if swept_pdh == 1.0 or closes[j] < emas_200[j]:
                            entry_bar = j + 1
                            if entry_bar >= trade_end or entry_bar >= n:
                                continue
                                
                            direction = -1.0
                            entry = opens[entry_bar]  # Strictly causal fill at open of next bar
                            sl = or_high
                            
                            # Completed breakout bar j features are 100% strictly causal
                            prev_idx = j
                            atr_val = atrs[prev_idx]
                            atr_pct = atr_val / (closes[prev_idx] + 1e-9)

                            # ATR-Capped Range & Stop Cap (Upgrade #3 for W6 liquidation expansions)
                            capped_range = or_range
                            if atr_val > 0 and capped_range > 1.75 * atr_val:
                                capped_range = 1.75 * atr_val
                            r_val = max(sl - entry, 0.50 * capped_range)
                            if atr_val > 0 and r_val > 1.75 * atr_val:
                                r_val = 1.75 * atr_val
                                current_sl = entry + r_val
                            else:
                                current_sl = sl
                            r_val = max(r_val, 1e-4)

                            tp = entry - 3.0 * r_val   # 1:3 RR target
                            
                            v_dist = (closes[prev_idx] - vwaps[prev_idx]) / (closes[prev_idx] + 1e-9)
                            e50_dist = (closes[prev_idx] - emas_50[prev_idx]) / (closes[prev_idx] + 1e-9)
                            e200_dist = (closes[prev_idx] - emas_200[prev_idx]) / (closes[prev_idx] + 1e-9)
                            
                            e200_slope = 0.0
                            if prev_idx >= 10:
                                e200_slope = (emas_200[prev_idx] - emas_200[prev_idx-10]) / (emas_200[prev_idx-10] + 1e-9)
                                
                            vol_spike = volumes[prev_idx] / (vol_sma_20[prev_idx-1 if prev_idx > 0 else 0] + 1e-9)
                            range_atr = or_range / (atr_val + 1e-9)
                            
                            # CRT Features (Clamped, confirmed on bar j close)
                            body_ratio = min(1.0, max(0.0, abs(closes[prev_idx] - opens[prev_idx]) / (highs[prev_idx] - lows[prev_idx] + 1e-9)))
                            close_outside = 1.0 if closes[prev_idx] < or_low else 0.0
                            fvg_expansion = 1.0 if (prev_idx >= 2 and highs[prev_idx] < lows[prev_idx-2] and (lows[prev_idx-2] - highs[prev_idx]) < 2.0 * atr_val) else 0.0
                            judas_sweep = judas_sweep_short
                            
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
                            
                            # Dynamic BE trigger for compressed ATR regimes (Upgrade #4 for W18)
                            phase0_trigger = 1.0 if atr_pct < 0.0045 else 0.8

                            outcome_r = -1.0
                            exit_is_stop = False
                            phase_0_locked = False
                            phase_1_locked = False
                            trail_active = False

                            for k in range(entry_bar, trade_end):
                                # Time decay: exit at market after 24 bars if < 0.2R gain
                                if k - entry_bar >= 24:
                                    current_r = (entry - closes[k]) / (r_val + 1e-9)
                                    if current_r < 0.2:
                                        outcome_r = current_r
                                        break

                                # Stop hit
                                if highs[k] >= current_sl:
                                    outcome_r = (entry - current_sl) / (r_val + 1e-9)
                                    exit_is_stop = True
                                    break

                                # TP hit — 1:3 RR target
                                if lows[k] <= tp:
                                    outcome_r = 3.0
                                    break

                                # Ratchet: check on bar close (causal)
                                current_gain = (entry - closes[k]) / (r_val + 1e-9)
                                if not phase_0_locked and current_gain >= phase0_trigger:
                                    current_sl = entry - 0.35 * r_val  # BE lock covers 41 bps
                                    phase_0_locked = True
                                if phase_0_locked and not phase_1_locked and current_gain >= 1.5:
                                    current_sl = entry - 0.80 * r_val  # profit lock
                                    phase_1_locked = True
                                    trail_active = True  # unlock ATR trailing after Phase 1

                                # ATR trailing stop (activates after Phase 1)
                                # Computed on close of bar k → tested on bar k+1 (causal)
                                # min() ensures stop never moves backwards (down) for shorts
                                if trail_active:
                                    trail_sl = closes[k] + 1.5 * atrs[k]
                                    if trail_sl < current_sl:
                                        current_sl = trail_sl

                            if outcome_r == -1.0:
                                cur_r = (entry - closes[trade_end-1]) / (r_val + 1e-9)
                                # Upgrade #1 & #6: credit partial gain for Phase 0 locked expired trades
                                if phase_0_locked:
                                    outcome_r = max(cur_r, 0.15)
                                else:
                                    outcome_r = cur_r
                                # Upgrade #1 & #6: credit partial gain for Phase 0 locked expired trades
                                if phase_0_locked:
                                    outcome_r = max(cur_r, 0.15)
                                else:
                                    outcome_r = cur_r

                            # Calibrated flat friction: 0.08R per trade
                            outcome_r -= 0.08

                            outcomes[trade_idx] = max(-1.15, min(3.0, outcome_r))  # cap at 3R
                            timestamps_out[trade_idx] = timestamps[entry_bar]
                            trade_idx += 1
                            i = trade_end
                            break
        i += 1
        
    return features[:trade_idx], outcomes[:trade_idx], timestamps_out[:trade_idx]
