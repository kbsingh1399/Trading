"""
================================================================================
S2: INSTITUTIONAL ML ALPHA (PURE CONFLUENCE)
================================================================================
Implements the exact invariants specified in ACTIVE_CONTEXT.md and AGENTS.md.
Combines strict mathematical institutional confluence with XGBoost Percentile ML.
Now acts as a pure signal generator for the ExecutionKernel.
================================================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Callable
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

class S2InstitutionalMLSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)

    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        spot_cvd = df_test.get("spot_cvd_15m", pd.Series(np.zeros(T))).values
        fut_cvd = df_test.get("future_cvd_15m", pd.Series(np.zeros(T))).values
        rsi = df_test.get("rsi_14", pd.Series(np.full(T, 50.0))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        
        spot_cvd_delta = np.zeros(T)
        spot_cvd_delta[1:] = np.diff(spot_cvd)
        fut_cvd_delta = np.zeros(T)
        fut_cvd_delta[1:] = np.diff(fut_cvd)
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        for t in range(1, T):
            sig_long = (long_liq_zs[t] > 1.2) and (zc_div[t] > 0.3) and (spot_cvd_delta[t] > 0) and (fut_cvd_delta[t] < 0) and (rsi[t] < 45) and (vwap_z[t] < -0.4)
            sig_short = (short_liq_zs[t] > 1.2) and (zc_div[t] < -0.3) and (spot_cvd_delta[t] < 0) and (fut_cvd_delta[t] > 0) and (rsi[t] > 55) and (vwap_z[t] > 0.4)
                
            if filter_func is not None:
                if sig_long and not filter_func(t, 'LONG'): sig_long = False
                if sig_short and not filter_func(t, 'SHORT'): sig_short = False

            if sig_long:
                signals[t] = 1
                raw_r[t] = atr[t] * 2.0
            elif sig_short:
                signals[t] = -1
                raw_r[t] = atr[t] * 2.0
                
        return pd.DataFrame({'side': signals, 'raw_r': raw_r}, index=df_test.index)

    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        return self.kernel.run(df_test, signals_df, training_mode)
