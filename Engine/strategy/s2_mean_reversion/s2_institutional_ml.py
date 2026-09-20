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

DEFAULT_RATCHET = RatchetConfig()

class S2InstitutionalMLSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)

    def generate_signals(
        self,
        df_test: pd.DataFrame,
        filter_func: Callable[[int, str], bool] = None,
    ) -> pd.DataFrame:
        columns = (
            "close", "atr_14", "long_liq_zs", "short_liq_zs",
            "zc_div", "spot_cvd_15m", "future_cvd_15m",
            "rsi_14", "vwap_zscore",
        )
        missing = [name for name in columns if name not in df_test]
        if missing:
            raise ValueError(f"Missing S2 inputs: {missing}")

        values = df_test.loc[:, list(columns)].to_numpy(dtype=np.float64)
        close, atr, long_z, short_z, div, spot, futures, rsi, vwap = values.T

        valid = (
            np.isfinite(values).all(axis=1)
            & (close > 0.0)
            & (atr > 0.0)
            & (rsi >= 0.0)
            & (rsi <= 100.0)
        )
        valid[:24] = False

        # These schema fields already contain per-bar volume deltas.
        longs = (
            valid
            & (long_z > 1.8)
            & (div > 0.8)
            & (spot > 0.0)
            & (futures < 0.0)
            & (rsi < 40.0)
            & (vwap < -0.5)
        )
        shorts = (
            valid
            & (short_z > 1.8)
            & (div < -0.8)
            & (spot < 0.0)
            & (futures > 0.0)
            & (rsi > 60.0)
            & (vwap > 0.5)
        )

        side = np.zeros(len(df_test), dtype=np.int8)
        side[longs] = 1
        side[shorts] = -1

        # Any model and threshold must be calibrated before OOS.
        if filter_func is not None:
            for t in np.flatnonzero(side):
                direction = "LONG" if side[t] == 1 else "SHORT"
                if not filter_func(int(t), direction):
                    side[t] = 0

        raw_r = np.zeros(len(df_test), dtype=np.float64)
        active = side != 0
        raw_r[active] = 2.0 * np.maximum(
            atr[active], close[active] * 0.002
        )

        # The kernel consumes signal t at open[t + 1].
        return pd.DataFrame(
            {"side": side, "raw_r": raw_r},
            index=df_test.index,
        )

    def run(self, df_test: pd.DataFrame, training_mode: bool = False,
            filter_func: Callable[[int, str], bool] = None, *, meta_labeler=None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        if meta_labeler is not None:
            if meta_labeler.kernel.ratchet != self.kernel.ratchet or meta_labeler.kernel.fric != self.kernel.fric:
                raise ValueError("Meta labels and execution require identical exit/friction policies")
            signals_df = meta_labeler.filter_signals(df_test, signals_df)
        return self.kernel.run(df_test, signals_df, training_mode)
