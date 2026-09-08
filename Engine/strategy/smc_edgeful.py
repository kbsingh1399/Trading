"""
================================================================================
SMC EDGEFUL FVG ENGINE (15m FVG Mitigation)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Based on Edgeful FVG mechanics:
- Detects institutional displacement (FVG creation with volume/liquidation tail).
- Waits for retest/mitigation of the Fair Value Gap.
- Enforces structural invalidation stop loss and mean-reversion ratchet.
================================================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Callable, Dict
from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig

DEFAULT_RATCHET = RatchetConfig()

class SMCEdgefulSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        long_liq = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        vol_ratio = df_test.get("volume_ratio", pd.Series(np.ones(T))).values
        ema_200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        active_fvgs = []
        
        for t in range(24, T):
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
            
            # Age active FVGs
            for fvg in active_fvgs:
                fvg["age"] += 1
                
            # 1. Detect Institutional FVG Creation (Displacement with volume/liquidation tail)
            # Bullish FVG: candle t-1 jumped up leaving a gap between hi[t-2] and lo[t]
            if lo[t] > hi[t-2] and cl[t-1] > op[t-1] and (short_liq[t-1] > 0.8 or vol_ratio[t-1] > 1.3):
                active_fvgs.append({"top": lo[t], "bottom": hi[t-2], "type": 1, "age": 0})
                
            # Bearish FVG: candle t-1 plunged down leaving a gap between lo[t-2] and hi[t]
            if hi[t] < lo[t-2] and cl[t-1] < op[t-1] and (long_liq[t-1] > 0.8 or vol_ratio[t-1] > 1.3):
                active_fvgs.append({"top": lo[t-2], "bottom": hi[t], "type": -1, "age": 0})
                
            # Only keep unmitigated FVGs up to 36 bars old (9 hours)
            active_fvgs = [f for f in active_fvgs if f["age"] <= 36]
            
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            for fvg in active_fvgs:
                if fvg["age"] > 0:
                    # Bullish mitigation: price tests FVG top, holds bottom, and closes green in an uptrend
                    if fvg["type"] == 1 and trend_up:
                        if lo[t] <= fvg["top"] and cl[t] > fvg["bottom"] and cl[t] > op[t]:
                            sig_long = True
                            # Invalidation stop placed below FVG bottom + 0.2 ATR
                            s_dist = (cl[t] - fvg["bottom"]) + 0.2 * atr[t]
                            s_dist = max(s_dist, atr[t] * 1.5)
                            s_dist = min(s_dist, atr[t] * 2.5)
                            stop_dist = s_dist
                            fvg["age"] = 999
                            break
                    # Bearish mitigation: price tests FVG bottom, holds top, and closes red in a downtrend
                    elif fvg["type"] == -1 and trend_down:
                        if hi[t] >= fvg["bottom"] and cl[t] < fvg["top"] and cl[t] < op[t]:
                            sig_short = True
                            s_dist = (fvg["top"] - cl[t]) + 0.2 * atr[t]
                            s_dist = max(s_dist, atr[t] * 1.5)
                            s_dist = min(s_dist, atr[t] * 2.5)
                            stop_dist = s_dist
                            fvg["age"] = 999
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
        
    def run(self, df_test: pd.DataFrame, training_mode: bool = False,
            filter_func: Callable[[int, str], bool] = None, *, meta_labeler=None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        if meta_labeler is not None:
            if meta_labeler.kernel.ratchet != self.kernel.ratchet or meta_labeler.kernel.fric != self.kernel.fric:
                raise ValueError("Meta labels and execution require identical exit/friction policies")
            signals_df = meta_labeler.filter_signals(df_test, signals_df)
        return self.kernel.run(df_test, signals_df, training_mode)
