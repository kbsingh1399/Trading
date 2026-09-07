"""
================================================================================
S1: LIQUIDATION CASCADE (ML-DRIVEN INSTITUTIONAL QUANT ARCHITECTURE)
================================================================================
Implements the exact invariants specified in ACTIVE_CONTEXT.md and AGENTS.md.
ML overlays are applied strictly out-of-sample on pure liquidation cascades.
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

class LiquidationCascadeSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)

    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        cl = df_test["close"].values
        
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        # Extract ML Alpha Invariants
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)

        # Iterate to generate signals
        for t in range(24, T):
            # Base Trigger for Liquidations (Z >= 1.2 per AGENTS.md)
            sig_long = (long_liq_zs[t] > 1.2) and (cl[t] > op[t])
            sig_short = (short_liq_zs[t] > 1.2) and (cl[t] < op[t])
                
            # Filter using the XGBoost Model function if provided
            if filter_func is not None:
                if sig_long and not filter_func(t, 'LONG'): sig_long = False
                if sig_short and not filter_func(t, 'SHORT'): sig_short = False

            if sig_long:
                signals[t] = 1
                r_ = atr[t] * 2.0
                if r_ <= 0: r_ = cl[t] * 0.005
                raw_r[t] = r_
                
            elif sig_short:
                signals[t] = -1
                r_ = atr[t] * 2.0
                if r_ <= 0: r_ = cl[t] * 0.005
                raw_r[t] = r_

        return pd.DataFrame({'side': signals, 'raw_r': raw_r}, index=df_test.index)

    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        return self.kernel.run(df_test, signals_df, training_mode)
