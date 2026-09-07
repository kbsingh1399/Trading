"""
================================================================================
SMC MARCI ENGINE (Bollinger Bands + Trendline / Pullback Break)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Uses Bollinger Bands and fractal pullbacks to resume primary trend:
- Identifies primary trend via EMA 200 direction.
- Detects oversold/overbought pullback into Bollinger Bands + VWAP stretch.
- Waits for fractal swing low/high confirmation and momentum reclaim.
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

class SMCMarciSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        ema200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        long_liq = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        
        # Calculate Bollinger Bands (20, 2)
        close_series = pd.Series(cl)
        bb_mid = close_series.rolling(window=20).mean().values
        bb_std = close_series.rolling(window=20).std(ddof=0).values
        bb_upper = bb_mid + (2 * bb_std)
        bb_lower = bb_mid - (2 * bb_std)
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        for t in range(25, T):
            trend_up = ema200[t] >= ema200[t-12]
            trend_down = ema200[t] <= ema200[t-12]
            
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            # Long Setup:
            # 1. Primary trend is UP
            # 2. Pullback dipped below or touched lower BB (or oversold vwap_z < -0.6) within past 3 bars
            # 3. Trapped liquidations or divergence: long_liq > 0.8 or zc_div > 0.3
            # 4. Swing low formed at t-1 (lo[t-1] < lo[t-2]) and current candle reclaims (cl[t] > hi[t-1] and cl[t] > op[t])
            was_oversold = (lo[t-1] <= bb_lower[t-1]) or (lo[t-2] <= bb_lower[t-2]) or (vwap_z[t-1] < -0.6)
            has_absorption_l = (long_liq[t-1] > 0.8) or (long_liq[t] > 0.8) or (zc_div[t] > 0.3)
            
            if trend_up and was_oversold and has_absorption_l:
                if lo[t-1] < lo[t-2] and cl[t] > hi[t-1] and cl[t] > op[t]:
                    sig_long = True
                    s_dist = (cl[t] - lo[t-1]) + 0.1 * atr[t]
                    s_dist = max(s_dist, cl[t] * 0.006)
                    s_dist = min(s_dist, atr[t] * 1.5)
                    stop_dist = s_dist
                    
            # Short Setup:
            # 1. Primary trend is DOWN
            # 2. Rally reached upper BB or overbought vwap_z > 0.6
            # 3. Trapped short liquidations or negative divergence
            # 4. Swing high formed at t-1 and current candle breaks lower
            was_overbought = (hi[t-1] >= bb_upper[t-1]) or (hi[t-2] >= bb_upper[t-2]) or (vwap_z[t-1] > 0.6)
            has_absorption_s = (short_liq[t-1] > 0.8) or (short_liq[t] > 0.8) or (zc_div[t] < -0.3)
            
            if trend_down and was_overbought and has_absorption_s:
                if hi[t-1] > hi[t-2] and cl[t] < lo[t-1] and cl[t] < op[t]:
                    sig_short = True
                    s_dist = (hi[t-1] - cl[t]) + 0.1 * atr[t]
                    s_dist = max(s_dist, cl[t] * 0.006)
                    s_dist = min(s_dist, atr[t] * 1.5)
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
