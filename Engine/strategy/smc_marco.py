"""
================================================================================
SMC MARCO TRADES ENGINE (Liquidity Sweep & Trap)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Based on Marco Trade's Liquidity Playbook:
- Identifies key HTF swing highs/lows (liquidity pools).
- Waits for a stop-run sweep of the pool.
- Enforces institutional absorption and trap close back inside the level.
- Structural invalidation stop with mean-reversion ratchet.
================================================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Callable
from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig

DEFAULT_RATCHET = RatchetConfig(
    arm0_r=0.7,
    lock0_r=0.20,
    arm1_r=1.2,
    lock1_r=0.70,
    min_target_r=1.8,
    time_decay_bars=40,
    time_decay_r=0.20
)

class SMCMarcoSimulator:
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
        ema_200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        # Track active liquidity pools
        liquidity_pools = []
        
        for t in range(25, T):
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
            
            # 1. Identify Liquidity Pools (8-bar center pivot to maintain freshness without lookahead)
            if t >= 16:
                center_hi = hi[t-8]
                center_lo = lo[t-8]
                is_swing_high = True
                is_swing_low = True
                for i in range(1, 9):
                    if center_hi <= hi[t-8-i] or center_hi <= hi[t-8+i]:
                        is_swing_high = False
                    if center_lo >= lo[t-8-i] or center_lo >= lo[t-8+i]:
                        is_swing_low = False
                        
                if is_swing_high:
                    liquidity_pools.append({"price": center_hi, "type": 1, "age": 0})
                if is_swing_low:
                    liquidity_pools.append({"price": center_lo, "type": -1, "age": 0})
                    
            for pool in liquidity_pools:
                pool["age"] += 1
                
            # Prune pools older than 64 bars (16 hours)
            liquidity_pools = [p for p in liquidity_pools if p["age"] <= 64]
            
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            swept_pools = []
            
            has_absorption_l = (long_liq_zs[t] > 0.8) or (zc_div[t] > 0.3) or (vwap_z[t] < -0.5)
            has_absorption_s = (short_liq_zs[t] > 0.8) or (zc_div[t] < -0.3) or (vwap_z[t] > 0.5)
            
            for i, pool in enumerate(liquidity_pools):
                # Sell-side liquidity sweep (Trap below lows)
                if pool["type"] == -1 and trend_up and has_absorption_l:
                    if lo[t] < pool["price"] and cl[t] > pool["price"] and cl[t] > op[t]:
                        sig_long = True
                        s_dist = (cl[t] - lo[t]) + 0.1 * atr[t]
                        s_dist = max(s_dist, cl[t] * 0.006)
                        s_dist = min(s_dist, atr[t] * 1.5)
                        stop_dist = s_dist
                        swept_pools.append(i)
                        break
                # Buy-side liquidity sweep (Trap above highs)
                elif pool["type"] == 1 and trend_down and has_absorption_s:
                    if hi[t] > pool["price"] and cl[t] < pool["price"] and cl[t] < op[t]:
                        sig_short = True
                        s_dist = (hi[t] - cl[t]) + 0.1 * atr[t]
                        s_dist = max(s_dist, cl[t] * 0.006)
                        s_dist = min(s_dist, atr[t] * 1.5)
                        stop_dist = s_dist
                        swept_pools.append(i)
                        break
                        
            for i in sorted(swept_pools, reverse=True):
                if i < len(liquidity_pools):
                    liquidity_pools.pop(i)
                    
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
