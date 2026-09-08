# Engine/ml/footprint_confirmation.py
from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict


class FootprintConfirmation:
    """
    Binary confirmation gate evaluated at SMC event bars.
    Emits `conf_score` (0..6) and `is_confirmed` on the signal frame.
    """

    def __init__(self, min_score: int = 3):
        self.min_score = min_score

    @staticmethod
    def _zs(s: pd.Series, w: int = 96) -> np.ndarray:
        m = s.rolling(w, min_periods=1).mean()
        sd = s.rolling(w, min_periods=1).std(ddof=0).replace(0.0, np.nan).ffill().fillna(1.0)
        return ((s - m) / sd).fillna(0.0).clip(-5, 5).to_numpy()

    def confirm(self, df: pd.DataFrame, sig: pd.DataFrame,
                ladder_feats: pd.DataFrame) -> pd.DataFrame:
        """
        df: 15m master table.
        sig: output of SMCEventDetector.generate_signals (has `side`).
        ladder_feats: FootprintLadderFeatures.build_features output, same index.
        """
        out = sig.copy()
        T = len(df)
        lf = ladder_feats.reindex(df.index).fillna(0.0)

        wsa_z = self._zs(lf.get("wick_sell_absorb", pd.Series(0.0, index=df.index)))
        wbe_z = self._zs(lf.get("wick_buy_exhaust", pd.Series(0.0, index=df.index)))
        abs_ratio = lf.get("absorption_ratio", pd.Series(0.0, index=df.index)).to_numpy()
        absr_z = self._zs(pd.Series(abs_ratio, index=df.index))
        poc_z = self._zs(lf.get("poc_shift", pd.Series(0.0, index=df.index)))
        close_pos = lf.get("close_pos", pd.Series(0.0, index=df.index)).to_numpy()
        side = out["side"].to_numpy()

        stacked_buy = df.get("is_stacked_buy_imb",
                             pd.Series(np.zeros(T), index=df.index)).to_numpy().astype(bool)
        stacked_sell = df.get("is_stacked_sell_imb",
                              pd.Series(np.zeros(T), index=df.index)).to_numpy().astype(bool)
        # Backward-looking OR in last 2 bars
        sb2 = stacked_buy | np.concatenate([[False], stacked_buy[:-1]])
        ss2 = stacked_sell | np.concatenate([[False], stacked_sell[:-1]])

        score = np.zeros(T, dtype=np.int8)
        long_m = side == 1
        short_m = side == -1

        score += (long_m & (wsa_z >= 1.0)).astype(np.int8)
        score += (short_m & (wbe_z >= 1.0)).astype(np.int8)
        score += (long_m & (absr_z >= 0.5) & (abs_ratio > 0)).astype(np.int8)
        score += (short_m & (absr_z <= -0.5) & (abs_ratio < 0)).astype(np.int8)
        score += (long_m & (poc_z >= 0.3)).astype(np.int8)
        score += (short_m & (poc_z <= -0.3)).astype(np.int8)
        score += (long_m & (close_pos >= 0.3)).astype(np.int8)
        score += (short_m & (close_pos <= -0.3)).astype(np.int8)
        score += (long_m & sb2).astype(np.int8)
        score += (short_m & ss2).astype(np.int8)
        score = np.minimum(score, 6)

        out["conf_score"] = score
        out["is_confirmed"] = (score >= self.min_score) & (side != 0)
        out.loc[~out["is_confirmed"], "side"] = 0
        out.loc[out["side"] == 0, "raw_r"] = 0.0
        return out
