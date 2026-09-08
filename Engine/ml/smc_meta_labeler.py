# Engine/ml/smc_meta_labeler.py
from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, List, Optional

from Engine.ml.rf_meta_labeler import RegressionRMetaLabeler, BarrierConfig, CVConfig
from Engine.strategy.smc_event_detector import SMCEventDetector
from Engine.ml.footprint_confirmation import FootprintConfirmation


class SMCRegressionMetaLabeler(RegressionRMetaLabeler):
    """
    Round-4 Meta-Labeler for Unified SMC + Footprint Architecture:
      - Fits continuous R-multiple regression on confirmed SMC events
      - Evaluates with 2.25R target / 1.00R stop + friction
      - Causal purged & embargoed grouped WF-CV
      - Expectancy gate tau_R >= 0.25R net
    """

    NON_FEATURE = (
        "symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r",
        "side", "raw_r", "structural_level", "invalidation_price",
        "event_type", "conf_score", "is_confirmed", "prio"
    )

    PRIO = {
        "SWEEP_PDL": 0, "SWEEP_PDH": 0,
        "FVG_BULL": 1, "FVG_BEAR": 1,
        "OB_BULL": 2, "OB_BEAR": 2
    }

    def __init__(self, min_conf_score: int = 3):
        super().__init__(
            barrier=BarrierConfig(tp_r=2.25, sl_r=1.00, vertical_bars=48, min_terminal_r=0.20),
            cv=CVConfig(purge_hours=72, embargo_hours=24)
        )
        self.detector = SMCEventDetector()
        self.confirmer = FootprintConfirmation(min_score=min_conf_score)

    def build_smc_features(self, df: pd.DataFrame, sig: pd.DataFrame) -> pd.DataFrame:
        geo = self.detector.event_features(df, sig)
        macro = pd.DataFrame(index=df.index)
        macro["zc_div"] = df.get("zc_div", pd.Series(0.0, index=df.index)).clip(-5, 5).fillna(0.0)
        fr = df.get("funding_rate_pct", pd.Series(0.0, index=df.index))
        macro["funding_rate_pct"] = fr.clip(-0.5, 0.5).fillna(0.0)
        macro["vwap_zscore"] = df.get("vwap_zscore", pd.Series(0.0, index=df.index)).clip(-10, 10).fillna(0.0)
        macro["conf_score"] = sig.get("conf_score", pd.Series(0.0, index=df.index)).astype(np.float64).fillna(0.0)
        return geo.join(macro, how="outer").fillna(0.0)

    def pool_smc(self, per_symbol: Dict[str, pd.DataFrame],
                 ladder_feats: Dict[str, pd.DataFrame],
                 train_start: pd.Timestamp, train_end: pd.Timestamp) -> pd.DataFrame:
        frames = []
        for sym, df_sym in per_symbol.items():
            sl = df_sym.loc[train_start:train_end]
            if len(sl) < 200:
                continue
            sig = self.detector.generate_signals(sl.copy())
            if sym in ladder_feats:
                sig = self.confirmer.confirm(sl, sig, ladder_feats[sym].loc[sl.index])
            else:
                continue

            # Priority de-duplication (Note 3): SWEEP > FVG > OB
            active_mask = sig["side"].to_numpy() != 0
            if active_mask.sum() < 5:
                continue

            dedup = sig[active_mask].copy()
            dedup["prio"] = dedup["event_type"].map(self.PRIO).fillna(9)
            dedup = dedup.sort_values(["prio", "conf_score"], ascending=[True, False])
            dedup = dedup[~dedup.index.duplicated(keep="first")]

            # Create clean aligned arrays matching length of sl
            sig_clean = pd.DataFrame({
                "side": np.zeros(len(sl), dtype=np.int8),
                "raw_r": np.zeros(len(sl), dtype=np.float64)
            }, index=sl.index)
            sig_clean.loc[dedup.index, "side"] = dedup["side"].astype(np.int8)
            sig_clean.loc[dedup.index, "raw_r"] = dedup["raw_r"].astype(np.float64)

            event_mask = sig_clean["side"].to_numpy() != 0
            side_arr = sig_clean["side"].to_numpy()
            raw_r_arr = sig_clean["raw_r"].to_numpy()

            labels = self.triple_barrier_labels(sl, event_mask, side_arr, raw_r_arr)
            ev = labels.index.to_numpy()
            X = self.build_smc_features(sl, sig).iloc[ev]
            tab = X.reset_index(drop=True)
            tab["symbol"] = sym
            tab["abs_bar"] = sl.index.get_indexer(sl.index)[ev] + df_sym.index.get_indexer([sl.index[0]])[0]
            tab["y"] = (labels["exit_r"].to_numpy() > 0).astype(np.int8)
            tab["exit_r"] = labels["exit_r"].to_numpy()
            frames.append(tab)

        if not frames:
            raise RuntimeError("SMCRegressionMetaLabeler: zero confirmed events pooled.")
        return pd.concat(frames, ignore_index=True)

    def _calibrate_tau_R(self, p: np.ndarray, r: np.ndarray,
                         friction_r: float = 0.18) -> float:
        for tau in np.quantile(p, [0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50]):
            sel = p >= tau
            if sel.sum() < 25:
                continue
            if r[sel].mean() - friction_r >= 0.25:
                return float(tau)
        return float("inf")

    def score_smc(self, df_sym: pd.DataFrame, ladder_feats: pd.DataFrame,
                  sig: pd.DataFrame) -> pd.DataFrame:
        out = self.confirmer.confirm(df_sym, sig, ladder_feats)
        mask = out["side"].to_numpy() != 0
        pred = np.full(len(out), np.nan)
        if mask.any() and self.model_ is not None:
            X_all = self.build_smc_features(df_sym, out)
            cols = [c for c in self.feat_cols_ if c in X_all.columns]
            X = X_all.iloc[np.flatnonzero(mask)].reindex(columns=self.feat_cols_, fill_value=0.0)
            ok = np.isfinite(X.to_numpy(np.float64)).all(axis=1)
            ev = np.flatnonzero(mask)[ok]
            if len(ev) > 0:
                pred[ev] = self.model_.predict(X.to_numpy(np.float64)[ok])
        keep = np.isfinite(pred) & (pred >= self.tau_r_)
        out.loc[:, "side"] = np.where(keep, out["side"].to_numpy(), 0)
        out.loc[out["side"] == 0, "raw_r"] = 0.0
        out["pred_r"] = pred
        return out
