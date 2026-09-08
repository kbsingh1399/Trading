from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Callable, Dict, Optional

from Engine.ml.institutional_meta_labeler import (
    InstitutionalMetaLabeler, BarrierConfig, CVConfig, ModelConfig
)
from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig


class MetaGatedStrategy:
    """
    Wraps any of the 8 strategy simulators:

        gated = MetaGatedStrategy(LiquidationCascadeSimulator(), threshold=0.55)
        result = gated.run_walk_forward(df_full, window_start, window_end)
    """

    def __init__(self, base_strategy,
                 labeler: Optional[InstitutionalMetaLabeler] = None,
                 threshold: float = 0.55,
                 train_lookback_days: int = 365):
        self.base = base_strategy
        self.threshold = threshold
        self.lookback = pd.Timedelta(days=train_lookback_days)
        self.labeler = labeler or InstitutionalMetaLabeler(
            barrier=BarrierConfig(),
            cv=CVConfig(),
            model=ModelConfig(),
            threshold=threshold,
        )

    # -- event mask: primary-model setup bars (y_prim == 1) --
    @staticmethod
    def _event_and_side(signals: pd.DataFrame) -> tuple:
        side_arr = signals["side"].to_numpy()
        mask = side_arr != 0
        side = np.where(mask, side_arr, 1).astype(np.int8)
        return mask, side

    def run_walk_forward(self, df: pd.DataFrame,
                         window_start: str, window_end: str,
                         training_mode: bool = False) -> Dict:
        # Ensure df index is DatetimeIndex
        if not isinstance(df.index, pd.DatetimeIndex):
            if "datetime_utc" in df.columns:
                df = df.set_index(pd.to_datetime(df["datetime_utc"]))
            else:
                df.index = pd.to_datetime(df.index)

        if df.index.tz is not None:
            df = df.tz_convert(None)

        ws = pd.Timestamp(window_start).tz_localize(None)
        we = pd.Timestamp(window_end).tz_localize(None)
        train_end = ws - pd.Timedelta(hours=72)          # mandatory 72h purge
        train_start = train_end - self.lookback

        df_train = df[(df.index >= train_start) & (df.index < train_end)]
        df_test = df[(df.index >= ws) & (df.index <= we)]
        if len(df_test) == 0:
            raise ValueError(f"Empty OOS window: {window_start} to {window_end}")

        # 1) Primary signals on training slice -> events for meta-labeling
        sig_train = self.base.generate_signals(df_train.copy())
        mask_tr, side_tr = self._event_and_side(sig_train)
        r_tr = sig_train["raw_r"].to_numpy()

        # 2) Fit meta-labeler (purged WF-CV inside training slice)
        fit_info = self.labeler.fit_evaluate(df_train, mask_tr, side_tr, r_tr)

        # 3) Inference on OOS slice: primary signals -> proba gate -> kernel
        sig_test = self.base.generate_signals(df_test.copy())
        mask_te, _ = self._event_and_side(sig_test)
        proba = self.labeler.predict_proba(df_test, mask_te)
        sig_gated = self.labeler.gate_signals(df_test, sig_test, proba, self.threshold)

        # 4) Execute with patched (causal) kernel
        kernel = getattr(self.base, "kernel", None) or ExecutionKernel()
        result = kernel.run(df_test, sig_gated, training_mode)
        raw_trades_count = int((sig_test["side"] != 0).sum())
        gated_trades_count = int((sig_gated["side"] != 0).sum())

        result["meta"] = {
            "mean_cv_auc": fit_info.get("mean_auc", 0.5),
            "n_train_events": fit_info.get("n_events", 0),
            "positive_rate": fit_info.get("positive_rate", 0.0),
            "gated_trades": gated_trades_count,
            "raw_trades": raw_trades_count,
        }
        return result
