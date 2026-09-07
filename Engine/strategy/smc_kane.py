"""
================================================================================
SMC TRADER KANE ENGINE (Power of 3: Accumulation, Manipulation, Distribution)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Based on Trader Kane's PO3 Framework:
- Identifies 24-bar accumulation range.
- Detects the manipulation leg (liquidity sweep of the range boundary).
- Enforces institutional absorption (liquidations / orderflow divergence / rejection).
- Sizing based on structural sweep invalidation with mean-reversion ratchet.
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

class SMCKaneSimulator:
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
        
        for t in range(24, T):
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
            
            # Accumulation uses completed bars (t-24 to t-1)
            acc_high = np.max(hi[t-24:t])
            acc_low = np.min(lo[t-24:t])
            
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            # Long Manipulation: Price sweeps below accumulation low, absorbs liquidity,
            # and reclaims back inside the range with a bullish pinbar / hammer close
            is_liq_or_stretch = (long_liq_zs[t] > 0.8) or (zc_div[t] > 0.3) or (vwap_z[t] < -0.5)
            if lo[t] < acc_low and cl[t] > acc_low and cl[t] > op[t] and cl[t] > (hi[t] + lo[t])/2.0:
                if is_liq_or_stretch and trend_up:
                    sig_long = True
                    # Structural stop placed right below the manipulation wick + 0.2 ATR
                    s_dist = (cl[t] - lo[t]) + 0.2 * atr[t]
                    s_dist = max(s_dist, atr[t] * 1.5)
                    s_dist = min(s_dist, atr[t] * 2.5)
                    stop_dist = s_dist
                    
            # Short Manipulation: Price sweeps above accumulation high, absorbs buy-side liquidity,
            # and rejects back inside the range with a bearish pinbar / shooting star close
            is_short_liq_or_stretch = (short_liq_zs[t] > 0.8) or (zc_div[t] < -0.3) or (vwap_z[t] > 0.5)
            if hi[t] > acc_high and cl[t] < acc_high and cl[t] < op[t] and cl[t] < (hi[t] + lo[t])/2.0:
                if is_short_liq_or_stretch and trend_down:
                    sig_short = True
                    s_dist = (hi[t] - cl[t]) + 0.2 * atr[t]
                    s_dist = max(s_dist, atr[t] * 1.5)
                    s_dist = min(s_dist, atr[t] * 2.5)
                    stop_dist = s_dist
                    
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
