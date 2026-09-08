from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict

try:
    from xgboost import XGBClassifier
    _BACKEND = "xgb"
except ImportError:
    from lightgbm import LGBMClassifier
    _BACKEND = "lgbm"


@dataclass(frozen=True)
class BarrierConfig:
    tp_r: float = 2.50          # upper barrier in R multiples
    sl_r: float = 1.00          # lower barrier in R multiples
    vertical_bars: int = 24     # 6h on 15m
    min_terminal_r: float = 0.20  # vertical-barrier label=0 unless >= +0.2R


@dataclass(frozen=True)
class CVConfig:
    n_folds: int = 6
    purge_hours: int = 72                 # 288 bars on 15m
    embargo_hours: int = 24               # 96 bars, post-test embargo
    min_positive_per_fold: int = 20       # minimum events in fold


@dataclass(frozen=True)
class ModelConfig:
    max_depth: int = 4
    reg_alpha: float = 1.5
    reg_lambda: float = 3.5
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    learning_rate: float = 0.03
    n_estimators: int = 300
    min_child_weight: int = 15
    random_state: int = 42

@dataclass
class FoldResult:
    fold_id: int
    train_idx: np.ndarray
    test_idx: np.ndarray
    auc: float
    accuracy: float
    n_train: int
    n_test: int


FEATURE_COLUMNS: Tuple[str, ...] = (
    "fp_delta_ratio", "zc_div", "long_liq_zs", "short_liq_zs",
    "rsi_14", "dist_to_vwap_zs", "atr_norm",
)


class InstitutionalMetaLabeler:
    """
    Lopez de Prado secondary meta-labeling.

    Layer 1 (primary):    deterministic setup rule  -> y_prim in {0,1}, side in {-1,+1}
    Layer 2 (meta):       GBDT P(win | setup, features) trained only on y_prim==1 bars,
                          labeled by triple-barrier outcome (1 = hit +2.5R first).
    """

    def __init__(self, barrier: BarrierConfig = BarrierConfig(),
                 cv: CVConfig = CVConfig(),
                 model: ModelConfig = ModelConfig(),
                 threshold: float = 0.55):
        self.barrier = barrier
        self.cv_cfg = cv
        self.model_cfg = model
        self.threshold = threshold
        self.model_: Optional[object] = None
        self.fold_results_: List[FoldResult] = []
        self.feature_names_: List[str] = list(FEATURE_COLUMNS)
        self._train_mu_: Optional[pd.Series] = None
        self._train_sd_: Optional[pd.Series] = None

    # ------------------------------------------------------------------
    # 1) Triple-barrier labeling on event bars (causal, bar-by-bar scan)
    # ------------------------------------------------------------------
    def triple_barrier_labels(
        self,
        df: pd.DataFrame,
        event_mask: np.ndarray,
        side: np.ndarray,            # +1 long / -1 short on event bars
        r_distance: np.ndarray,      # 1R distance in price units on event bars
    ) -> pd.DataFrame:
        """
        Returns DataFrame indexed like df (event rows only):
            y_meta  : 1 if upper barrier hit first, else 0
            t_out   : exit bar index
            exit_r  : realized R at barrier touch
        Scan is strictly forward: barriers evaluated on bars t+1..t+V.
        """
        op = df["open"].values
        hi = df["high"].values
        lo = df["low"].values
        cl = df["close"].values
        B = self.barrier
        events = np.flatnonzero(event_mask)
        n = len(df)

        y = np.zeros(len(events), dtype=np.int8)
        t_out = np.zeros(len(events), dtype=np.int64)
        exit_r = np.zeros(len(events), dtype=np.float64)

        for k, t in enumerate(events):
            entry = op[t + 1] if t + 1 < n else cl[t]   # entry at next open (matches kernel)
            d = max(r_distance[t], 1e-12)
            
            # Target and stop levels in price space
            if side[t] == 1:
                up = entry + B.tp_r * d
                dn = entry - B.sl_r * d
            else:
                up = entry - B.tp_r * d
                dn = entry + B.sl_r * d

            end = min(t + B.vertical_bars, n - 1)
            hit = 0
            tout = end
            xr = 0.0

            for j in range(t + 1, end + 1):
                # conservative: stop checked before target on ambiguous bars
                stop_touched = (lo[j] <= dn) if side[t] == 1 else (hi[j] >= dn)
                tgt_touched = (hi[j] >= up) if side[t] == 1 else (lo[j] <= up)
                if stop_touched:
                    hit = 0
                    tout = j
                    xr = -B.sl_r
                    break
                if tgt_touched:
                    hit = 1
                    tout = j
                    xr = B.tp_r
                    break
            else:
                # vertical barrier: exit at close of last evaluated bar
                last = cl[end]
                xr = side[t] * (last - entry) / d
                hit = 1 if xr >= B.min_terminal_r else 0

            y[k] = hit
            t_out[k] = tout
            exit_r[k] = xr

        out = pd.DataFrame(index=events)
        out["y_meta"] = y
        out["t_out"] = t_out
        out["exit_r"] = exit_r
        return out

    # ------------------------------------------------------------------
    # 2) Stationary feature matrix (only stationary transforms)
    # ------------------------------------------------------------------
    def build_features(self, df: pd.DataFrame) -> pd.DataFrame:
        F = pd.DataFrame(index=df.index)
        T = len(df)
        get = lambda name, default: df.get(name, pd.Series(default, index=df.index)).astype(np.float64)

        cl = df["close"].astype(np.float64)
        atr = get("atr_14", cl * 0.002).clip(lower=1e-12)

        # delta ratio from footprint or taker volumes or cvd
        if "fp_delta_ratio" in df.columns:
            fp = df["fp_delta_ratio"].astype(np.float64)
        elif "taker_buy_vol_btc" in df.columns and "taker_sell_vol_btc" in df.columns:
            buy_v = df["taker_buy_vol_btc"].astype(np.float64)
            sell_v = df["taker_sell_vol_btc"].astype(np.float64)
            fp = (buy_v - sell_v) / (buy_v + sell_v + 1e-12)
        else:
            fp = get("future_cvd_15m", np.zeros(T))

        zc = get("zc_div", np.zeros(T))
        llq = get("long_liq_zs", np.zeros(T))
        slq = get("short_liq_zs", np.zeros(T))
        rsi = get("rsi_14", np.full(T, 50.0))
        vwz = df.get("dist_to_vwap_zs", df.get("vwap_zscore", pd.Series(np.zeros(T), index=df.index))).astype(np.float64)

        # stationary transforms: z-scores of levels, bounded values
        fp_mean = fp.rolling(96, min_periods=12).mean()
        fp_std = fp.rolling(96, min_periods=12).std().fillna(1.0)
        F["fp_delta_ratio"] = ((fp - fp_mean) / (fp_std + 1e-12)).fillna(0.0)

        F["zc_div"] = zc.fillna(0.0)
        F["long_liq_zs"] = llq.clip(upper=10.0).fillna(0.0)
        F["short_liq_zs"] = slq.clip(upper=10.0).fillna(0.0)
        F["rsi_14"] = ((rsi - 50.0) / 50.0).fillna(0.0)                     # -> [-1, 1]
        F["dist_to_vwap_zs"] = vwz.fillna(0.0)

        norm_atr = (atr / cl)
        atr_mean = norm_atr.rolling(96, min_periods=12).mean()
        atr_std = norm_atr.rolling(96, min_periods=12).std().fillna(1.0)
        F["atr_norm"] = ((norm_atr - atr_mean) / (atr_std + 1e-12)).fillna(0.0)
        return F

    # ------------------------------------------------------------------
    # 3) Purged & embargoed walk-forward CV
    # ------------------------------------------------------------------
    def _purged_wf_splits(self, event_positions: np.ndarray, t_out: np.ndarray) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Contiguous fold boundaries over EVENT index space, with time purge+embargo."""
        B, C = self.barrier, self.cv_cfg
        purge_bars = (C.purge_hours * 60) // 15
        embargo_bars = (C.embargo_hours * 60) // 15
        n_ev = len(event_positions)
        if n_ev < 30:
            return []

        edges = np.linspace(0, n_ev, C.n_folds + 1, dtype=int)

        splits = []
        for f in range(1, C.n_folds + 1):
            te = np.arange(edges[f - 1], edges[f])
            if len(te) < 5:
                continue
            tr = np.arange(0, edges[f - 1])
            if len(tr) < 15:
                continue

            # PURGE: drop train events whose label horizon overlaps the test period
            t_start_test = event_positions[te[0]]
            keep = (t_out[tr] < t_start_test - purge_bars)
            # EMBARGO: extra buffer before test start
            keep &= (event_positions[tr] < t_start_test - purge_bars - embargo_bars)
            tr = tr[keep]
            if len(tr) < C.min_positive_per_fold:
                continue
            splits.append((tr, te))
        return splits

    # ------------------------------------------------------------------
    # 4) Fit
    # ------------------------------------------------------------------
    def _make_model(self):
        if _BACKEND == "xgb":
            return XGBClassifier(
                max_depth=self.model_cfg.max_depth,
                reg_alpha=self.model_cfg.reg_alpha,
                reg_lambda=self.model_cfg.reg_lambda,
                subsample=self.model_cfg.subsample,
                colsample_bytree=self.model_cfg.colsample_bytree,
                learning_rate=self.model_cfg.learning_rate,
                n_estimators=self.model_cfg.n_estimators,
                min_child_weight=self.model_cfg.min_child_weight,
                eval_metric="logloss",
                tree_method="hist",
                random_state=self.model_cfg.random_state,
                n_jobs=-1,
            )
        return LGBMClassifier(
            max_depth=self.model_cfg.max_depth,
            reg_alpha=self.model_cfg.reg_alpha,
            reg_lambda=self.model_cfg.reg_lambda,
            subsample=self.model_cfg.subsample,
            colsample_bytree=self.model_cfg.colsample_bytree,
            learning_rate=self.model_cfg.learning_rate,
            n_estimators=self.model_cfg.n_estimators,
            min_child_weight=self.model_cfg.min_child_weight,
            random_state=self.model_cfg.random_state,
            n_jobs=-1,
            verbose=-1,
        )

    def _standardize_fit(self, X: pd.DataFrame) -> None:
        self._train_mu_ = X.mean()
        self._train_sd_ = X.std(ddof=0).replace(0.0, 1.0).fillna(1.0)

    def _standardize(self, X: pd.DataFrame) -> pd.DataFrame:
        if self._train_mu_ is None or self._train_sd_ is None:
            return X
        return (X - self._train_mu_) / self._train_sd_

    def fit_evaluate(self, df: pd.DataFrame, event_mask: np.ndarray,
                     side: np.ndarray, r_distance: np.ndarray) -> Dict:
        """Full purged WF-CV. Returns OOF probabilities + fold diagnostics."""
        from sklearn.metrics import roc_auc_score

        F = self.build_features(df)
        labels = self.triple_barrier_labels(df, event_mask, side, r_distance)
        events = labels.index.to_numpy()

        if len(events) == 0:
            return {
                "oof_proba": pd.Series(dtype=float),
                "y_meta": pd.Series(dtype=int),
                "fold_results": [],
                "mean_auc": 0.5,
                "positive_rate": 0.0,
                "n_events": 0,
            }

        X = F.iloc[events].reset_index(drop=True)
        y = labels["y_meta"].to_numpy()
        ev_pos = events
        t_out = labels["t_out"].to_numpy()

        valid = np.isfinite(X.to_numpy()).all(axis=1)
        X = X[valid].reset_index(drop=True)
        y = y[valid]
        ev_pos = ev_pos[valid]
        t_out = t_out[valid]

        splits = self._purged_wf_splits(ev_pos, t_out)
        oof = np.full(len(y), np.nan)
        self.fold_results_ = []

        for fold_id, (tr, te) in enumerate(splits):
            if len(np.unique(y[tr])) < 2:
                continue
            mdl = self._make_model()
            self._standardize_fit(X.iloc[tr])
            mdl.fit(self._standardize(X.iloc[tr]).to_numpy(), y[tr])
            p = mdl.predict_proba(self._standardize(X.iloc[te]).to_numpy())[:, 1]
            oof[te] = p
            auc = roc_auc_score(y[te], p) if len(np.unique(y[te])) > 1 else np.nan
            acc = float(((p >= self.threshold).astype(int) == y[te]).mean())
            self.fold_results_.append(FoldResult(
                fold_id, tr, te, auc, acc, len(tr), len(te)
            ))

        # Final model: refit on ALL events (deployed weights)
        if len(X) > 0 and len(np.unique(y)) > 1:
            self._standardize_fit(X)
            self.model_ = self._make_model()
            self.model_.fit(self._standardize(X).to_numpy(), y)
        else:
            self.model_ = None

        mean_auc = float(np.nanmean([f.auc for f in self.fold_results_])) if self.fold_results_ else 0.5
        pos_rate = float(y.mean()) if len(y) > 0 else 0.0

        return {
            "oof_proba": pd.Series(oof, index=ev_pos),
            "y_meta": pd.Series(y, index=ev_pos),
            "fold_results": self.fold_results_,
            "mean_auc": mean_auc,
            "positive_rate": pos_rate,
            "n_events": int(len(y)),
        }

    # ------------------------------------------------------------------
    # 5) Inference gate
    # ------------------------------------------------------------------
    def predict_proba(self, df: pd.DataFrame, event_mask: np.ndarray) -> np.ndarray:
        """P(success) per event bar; NaN where no model/events."""
        p = np.full(len(df), np.nan)
        if self.model_ is None:
            return p

        F = self.build_features(df)
        events = np.flatnonzero(event_mask)
        if len(events) == 0:
            return p

        X = self._standardize(F.iloc[events])
        ok = np.isfinite(X.to_numpy()).all(axis=1)
        if ok.any():
            p[events[ok]] = self.model_.predict_proba(X[ok].to_numpy())[:, 1]
        return p

    def gate_signals(self, df: pd.DataFrame, signals: pd.DataFrame,
                     proba: np.ndarray, threshold: Optional[float] = None) -> pd.DataFrame:
        """Zero out signals failing the confidence gate. Pure pass-through otherwise."""
        tau = threshold if threshold is not None else self.threshold
        s = signals.copy()
        m = s["side"].to_numpy() != 0
        if not m.any() or self.model_ is None:
            return s

        p = proba[m]
        # Keep signals only where proba is finite and >= tau
        keep = np.isfinite(p) & (p >= tau)
        new_side = np.where(keep, s.loc[m, "side"].to_numpy(), 0)
        s.loc[m, "side"] = new_side
        s.loc[s["side"] == 0, "raw_r"] = 0.0
        return s
