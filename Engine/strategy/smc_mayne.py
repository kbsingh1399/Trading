"""
================================================================================
SMC TRADER MAYNE ENGINE (HTF POI + LTF Breaker Block)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Based on Trader Mayne's HTF POI and Breaker Block mechanics:
- Identifies higher-timeframe trend/POI via EMA 200 trajectory.
- Tracks liquidity sweep followed by structural market structure break (MSB).
- Enters on retest/mitigation of the resulting Breaker Block zone.
- Structural invalidation stop with mean-reversion ratchet.
================================================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Callable
from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig

DEFAULT_RATCHET = RatchetConfig(
    arm0_r=0.85,
    lock0_r=0.45,
    arm1_r=1.25,
    lock1_r=0.85,
    min_target_r=1.75,
    time_decay_bars=36,
    time_decay_r=0.20
)

class SMCMayneSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        vol_ratio = df_test.get("volume_ratio", pd.Series(np.ones(T))).values
        ema_200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        # Track active Breaker Blocks: {"top": float, "bottom": float, "type": 1 or -1, "age": int}
        breaker_blocks = []
        
        for t in range(25, T):
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
            
            # Age active breaker blocks
            for bb in breaker_blocks:
                bb["age"] += 1
            breaker_blocks = [bb for bb in breaker_blocks if bb["age"] <= 48] # Keep up to 12 hours
            
            # 1. Detect Breaker Block Formation:
            # Bullish Breaker: Prior swing high formed at t-8 to t-4, price swept lower low at t-2/t-3,
            # then candle t-1 broke with displacement above the prior swing high.
            # That broken swing high now flips to support (Bullish Breaker).
            if t >= 16:
                prior_swing_high = np.max(hi[t-12:t-4])
                prior_swing_low = np.min(lo[t-4:t-1])
                # Check for displacement breakout above prior swing high
                if cl[t-1] > prior_swing_high and op[t-1] <= prior_swing_high and (vol_ratio[t-1] > 1.2 or short_liq_zs[t-1] > 0.8):
                    breaker_blocks.append({
                        "top": prior_swing_high,
                        "bottom": max(prior_swing_high - 0.5 * atr[t], prior_swing_low),
                        "type": 1,
                        "age": 0
                    })
                    
                # Bearish Breaker: Prior swing low formed at t-12 to t-4, price swept higher high at t-4 to t-2,
                # then candle t-1 broke with displacement below the prior swing low.
                prior_swing_low_bear = np.min(lo[t-12:t-4])
                prior_swing_high_bear = np.max(hi[t-4:t-1])
                if cl[t-1] < prior_swing_low_bear and op[t-1] >= prior_swing_low_bear and (vol_ratio[t-1] > 1.2 or long_liq_zs[t-1] > 0.8):
                    breaker_blocks.append({
                        "top": min(prior_swing_low_bear + 0.5 * atr[t], prior_swing_high_bear),
                        "bottom": prior_swing_low_bear,
                        "type": -1,
                        "age": 0
                    })
                    
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            has_absorption_l = (long_liq_zs[t] > 0.8) or (zc_div[t] > 0.3) or (vwap_z[t] < -0.4) or (vol_ratio[t] > 1.2)
            has_absorption_s = (short_liq_zs[t] > 0.8) or (zc_div[t] < -0.3) or (vwap_z[t] > 0.4) or (vol_ratio[t] > 1.2)
            
            # 2. Retest and Mitigation of Breaker Block
            for bb in breaker_blocks:
                if bb["age"] > 0:
                    # Bullish Breaker Retest
                    if bb["type"] == 1 and trend_up and has_absorption_l:
                        # Price tests breaker zone and closes green
                        if lo[t] <= bb["top"] and cl[t] >= bb["bottom"] and cl[t] > op[t]:
                            sig_long = True
                            s_dist = (cl[t] - bb["bottom"]) + 0.2 * atr[t]
                            s_dist = max(s_dist, atr[t] * 1.5)
                            s_dist = min(s_dist, atr[t] * 2.5)
                            stop_dist = s_dist
                            bb["age"] = 999
                            break
                            
                    # Bearish Breaker Retest
                    elif bb["type"] == -1 and trend_down and has_absorption_s:
                        # Price tests breaker zone from below and closes red
                        if hi[t] >= bb["bottom"] and cl[t] <= bb["top"] and cl[t] < op[t]:
                            sig_short = True
                            s_dist = (bb["top"] - cl[t]) + 0.2 * atr[t]
                            s_dist = max(s_dist, atr[t] * 1.5)
                            s_dist = min(s_dist, atr[t] * 2.5)
                            stop_dist = s_dist
                            bb["age"] = 999
                            break
                            
            if filter_func is not None:
                if sig_long and not filter_func(t, 'LONG'): sig_long = False
                if sig_short and not filter_func(t, 'SHORT'): sig_short = False
                
            if sig_long and not sig_short:
                signals[t] = 1
                raw_r[t] = stop_dist
            elif sig_short and not sig_long:
                signals[t] = -1
                raw_r[t] = stop_dist
                
        return pd.DataFrame({'side': signals, 'raw_r': raw_r}, index=df_test.index)
        
    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        return self.kernel.run(df_test, signals_df, training_mode)
