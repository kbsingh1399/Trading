# Engine/ml/rf_meta_labeler.py
from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

try:
    from xgboost import XGBRegressor
    _REG_BACKEND = "xgb"
except ImportError:
    from lightgbm import LGBMRegressor
    _REG_BACKEND = "lgbm"

from Engine.ml.pooled_meta_labeler import (
    PooledInstitutionalMetaLabeler, BarrierConfig, CVConfig, ModelConfig, GateConfig
)


class RegressionRMetaLabeler(PooledInstitutionalMetaLabeler):
    """
    Round-3 meta-labeler:
      - target = realized exit_r (continuous regression), friction-adjusted barriers
      - single-feature AUC probe gate before full fit
      - tau_R gate on predicted R (expectancy break-even, friction included)
    """

    def __init__(self,
                 barrier: BarrierConfig = BarrierConfig(tp_r=2.0, sl_r=1.0, vertical_bars=32, min_terminal_r=0.20),
                 cv: CVConfig = CVConfig(purge_hours=72, embargo_hours=24),
                 model: ModelConfig = ModelConfig(),
                 gate: GateConfig = GateConfig()):
        super().__init__(barrier=barrier, cv=cv, model=model, gate=gate)
        self.tau_r_: float = 0.0

    def triple_barrier_labels(self, df: pd.DataFrame, event_mask: np.ndarray,
                              side: np.ndarray, r_dist: np.ndarray) -> pd.DataFrame:
        cl = df["close"].values
        median_r = np.nanmedian(r_dist[r_dist > 0]) if (r_dist > 0).any() else 1.0
        fric_R = 0.0033 * np.nanmean(cl) / max(median_r, 1e-12)
        adjusted_barrier = BarrierConfig(
            tp_r=self.barrier.tp_r,
            sl_r=self.barrier.sl_r + min(fric_R, 0.25),
            vertical_bars=self.barrier.vertical_bars,
            min_terminal_r=self.barrier.min_terminal_r
        )
        old_barrier = self.barrier
        self.barrier = adjusted_barrier
        labels = super().triple_barrier_labels(df, event_mask, side, r_dist)
        self.barrier = old_barrier
        return labels

    def probe_features(self, pooled: pd.DataFrame) -> pd.DataFrame:
        from sklearn.metrics import roc_auc_score
        y = (pooled["exit_r"] > 0).to_numpy(np.int8)
        feats = [c for c in pooled.columns
                 if c not in ("symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r")]
        rows = []
        splits = self._cv_splits(pooled)

        for f in feats:
            x = pooled[f].to_numpy(np.float64)
            aucs = []
            for tr, te in splits:
                if len(np.unique(y[te])) > 1:
                    try:
                        aucs.append(float(roc_auc_score(y[te], x[te])))
                    except Exception:
                        pass
            m = float(np.nanmean(aucs)) if aucs else 0.5
            rows.append({
                "feature": f,
                "raw_auc_mean": m,
                "raw_auc_abs": abs(m - 0.5)
            })

        probe = pd.DataFrame(rows).sort_values("raw_auc_abs", ascending=False)
        best_pair, best_auc = "", 0.5
        # Test top 6 features pairwise
        top_feats = probe["feature"].head(6).tolist()
        for i in range(len(top_feats)):
            for j in range(i + 1, len(top_feats)):
                s = pooled[top_feats[i]].to_numpy(np.float64) + pooled[top_feats[j]].to_numpy(np.float64)
                aucs = []
                for tr, te in splits:
                    if len(np.unique(y[te])) > 1:
                        try:
                            aucs.append(float(roc_auc_score(y[te], s[te])))
                        except Exception:
                            pass
                m = float(np.nanmean(aucs)) if aucs else 0.5
                if abs(m - 0.5) > abs(best_auc - 0.5):
                    best_auc = m
                    best_pair = f"{top_feats[i]}+{top_feats[j]}"

        probe["best_pair"] = [best_pair] + [""] * (len(probe) - 1)
        probe["best_pair_auc"] = [best_auc] + [np.nan] * (len(probe) - 1)
        return probe

    def fit(self, pooled: pd.DataFrame) -> Dict:
        from sklearn.metrics import roc_auc_score
        feats = [c for c in pooled.columns
                 if c not in ("symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r")]
        X = pooled[feats].to_numpy(np.float64)
        r = pooled["exit_r"].to_numpy(np.float64)
        y_bin = (r > 0).astype(np.int8)

        oof = np.full(len(pooled), np.nan)
        aucs = []
        splits = self._cv_splits(pooled)

        for tr, te in splits:
            if _REG_BACKEND == "xgb":
                mdl = XGBRegressor(
                    max_depth=3, n_estimators=500, learning_rate=0.03,
                    reg_alpha=2.0, reg_lambda=5.0, subsample=0.8,
                    colsample_bytree=0.7, min_child_weight=10,
                    random_state=42, n_jobs=-1, tree_method="hist"
                )
            else:
                mdl = LGBMRegressor(
                    max_depth=3, n_estimators=500, learning_rate=0.03,
                    reg_alpha=2.0, reg_lambda=5.0, subsample=0.8,
                    colsample_bytree=0.7, min_child_weight=10,
                    random_state=42, n_jobs=-1, verbose=-1
                )
            mdl.fit(X[tr], r[tr])
            oof[te] = mdl.predict(X[te])
            if len(np.unique(y_bin[te])) > 1:
                aucs.append(float(roc_auc_score(y_bin[te], oof[te])))

        self.fold_aucs_ = aucs
        valid = np.isfinite(oof)
        self.tau_r_ = self._calibrate_tau_R(oof[valid], r[valid])

        # Final fit on all training data
        if _REG_BACKEND == "xgb":
            final_mdl = XGBRegressor(
                max_depth=3, n_estimators=500, learning_rate=0.03,
                reg_alpha=2.0, reg_lambda=5.0, subsample=0.8,
                colsample_bytree=0.7, min_child_weight=10,
                random_state=42, n_jobs=-1, tree_method="hist"
            )
        else:
            final_mdl = LGBMRegressor(
                max_depth=3, n_estimators=500, learning_rate=0.03,
                reg_alpha=2.0, reg_lambda=5.0, subsample=0.8,
                colsample_bytree=0.7, min_child_weight=10,
                random_state=42, n_jobs=-1, verbose=-1
            )
        final_mdl.fit(X, r)
        self.model_ = final_mdl
        self.feat_cols_ = feats

        return {
            "mean_cv_auc": float(np.mean(aucs)) if aucs else float("nan"),
            "fold_aucs": aucs,
            "calibrated_tau_r": self.tau_r_,
            "oof_expectancy_all": float(r[valid].mean()) if valid.any() else 0.0,
            "n_events": int(len(pooled)),
        }

    def _calibrate_tau_R(self, p: np.ndarray, r: np.ndarray) -> float:
        """tau_R = smallest predicted-R cut with OOF E[R | sel] > friction buffer."""
        for tau in np.quantile(p, [0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50]):
            sel = p >= tau
            if sel.sum() < 25:
                continue
            if r[sel].mean() > 0.15:
                return float(tau)
        return float("inf")

    def score_signals(self, df_sym: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
        out = signals.copy()
        mask = out["side"].to_numpy() != 0
        pred = np.full(len(out), np.nan)
        if mask.any() and self.model_ is not None:
            feat_df = self.build_features(df_sym)
            available_cols = [c for c in self.feat_cols_ if c in feat_df.columns]
            X = feat_df.iloc[np.flatnonzero(mask)][available_cols]
            ok = np.isfinite(X.to_numpy(np.float64)).all(axis=1)
            ev = np.flatnonzero(mask)[ok]
            if len(ev) > 0:
                pred[ev] = self.model_.predict(X.to_numpy(np.float64)[ok])
        keep = np.isfinite(pred) & (pred >= self.tau_r_)
        out.loc[:, "side"] = np.where(keep, out["side"].to_numpy(), 0)
        out.loc[out["side"] == 0, "raw_r"] = 0.0
        out["pred_r"] = pred
        return out
