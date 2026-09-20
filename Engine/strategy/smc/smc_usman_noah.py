"""
================================================================================
SMC USMAN NOAH ENGINE (PDH/PDL Sweep + Reclaim)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Based on Usman Noah's ICT Daily Liquidity Framework:
- Dynamically tracks Previous Day High (PDH) and Previous Day Low (PDL).
- Detects false breakout liquidity sweeps beyond PDH/PDL.
- Enters on structural reclaim with institutional volume/liquidation confirmation.
- Structural invalidation stop with mean-reversion ratchet.
================================================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Callable
from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig

DEFAULT_RATCHET = RatchetConfig()

class SMCUsmanNoahSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        if T == 0:
            return pd.DataFrame({"side": pd.Series(dtype=int), "raw_r": pd.Series(dtype=float)}, index=df_test.index)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        # Parse timestamp to track daily boundaries
        dt = pd.to_datetime(df_test.get("datetime_utc", df_test.get("datetime", pd.Series(df_test.index))))
        if hasattr(dt, 'dt') and hasattr(dt.dt, 'date'):
            days = dt.dt.date.values
        else:
            days = np.arange(T) // 96 # Fallback to 96 bars per 24h
            
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        vol_ratio = df_test.get("volume_ratio", pd.Series(np.ones(T))).values
        ema_200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        ema_50 = df_test.get("ema_50", pd.Series(cl)).values
        dispersion = np.abs(ema_50 - ema_200) / np.maximum(cl, 1e-6)
        vol_pct = atr / np.maximum(cl, 1e-6)
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        pdh, pdl = -1.0, float('inf')
        current_dh, current_dl = hi[0], lo[0]
        
        swept_pdl_bar = -1
        swept_pdh_bar = -1
        
        for t in range(1, T):
            
            # Day change detection
            if days[t] != days[t-1]:
                pdh = current_dh
                pdl = current_dl
                current_dh = hi[t]
                current_dl = lo[t]
                swept_pdl_bar = -1
                swept_pdh_bar = -1
            else:
                if hi[t] > current_dh: current_dh = hi[t]
                if lo[t] < current_dl: current_dl = lo[t]

            if t < 25:
                continue
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
                
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            has_absorption_l = (long_liq_zs[t] > 0.8) or (zc_div[t] > 0.3) or (vwap_z[t] < -0.4) or (vol_ratio[t] > 1.2)
            has_absorption_s = (short_liq_zs[t] > 0.8) or (zc_div[t] < -0.3) or (vwap_z[t] > 0.4) or (vol_ratio[t] > 1.2)
            
            if pdh != -1.0 and pdl != float('inf'):
                # PDL Sweep detection
                if lo[t] < pdl:
                    swept_pdl_bar = t
                # PDH Sweep detection
                if hi[t] > pdh:
                    swept_pdh_bar = t
                    
                # Bullish PDL Reclaim: Swept PDL within last 8 bars, now reclaims above PDL
                if swept_pdl_bar != -1 and (t - swept_pdl_bar) <= 8 and (t - swept_pdl_bar) >= 0:
                    if cl[t] > pdl and cl[t] > op[t] and trend_up and has_absorption_l:
                        sig_long = True
                        lowest_sweep = np.min(lo[swept_pdl_bar:t+1])
                        s_dist = (cl[t] - lowest_sweep) + 0.2 * atr[t]
                        s_dist = max(s_dist, atr[t] * 1.5)
                        s_dist = min(s_dist, atr[t] * 2.5)
                        stop_dist = s_dist
                        swept_pdl_bar = -1
                        
                # Bearish PDH Reclaim: Swept PDH within last 8 bars, now rejects back below PDH
                if swept_pdh_bar != -1 and (t - swept_pdh_bar) <= 8 and (t - swept_pdh_bar) >= 0:
                    if cl[t] < pdh and cl[t] < op[t] and trend_down and has_absorption_s:
                        sig_short = True
                        highest_sweep = np.max(hi[swept_pdh_bar:t+1])
                        s_dist = (highest_sweep - cl[t]) + 0.2 * atr[t]
                        s_dist = max(s_dist, atr[t] * 1.5)
                        s_dist = min(s_dist, atr[t] * 2.5)
                        stop_dist = s_dist
                        swept_pdh_bar = -1
                        
            if sig_long or sig_short:
                if dispersion[t] < 0.003 and vol_pct[t] < 0.008:
                    sig_long = False
                    sig_short = False
                elif sig_short and cl[t] > ema_200[t] and ema_50[t] > ema_200[t] * 1.01:
                    sig_short = False
                elif sig_long and cl[t] < ema_200[t] and ema_50[t] < ema_200[t] * 0.99:
                    sig_long = False

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
        
    def run(self, df_test: pd.DataFrame, training_mode: bool = False,
            filter_func: Callable[[int, str], bool] = None, *, meta_labeler=None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        if meta_labeler is not None:
            if meta_labeler.kernel.ratchet != self.kernel.ratchet or meta_labeler.kernel.fric != self.kernel.fric:
                raise ValueError("Meta labels and execution require identical exit/friction policies")
            signals_df = meta_labeler.filter_signals(df_test, signals_df)
        return self.kernel.run(df_test, signals_df, training_mode)
