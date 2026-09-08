# Engine/ml/pooled_meta_labeler.py
from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

try:
    from xgboost import XGBClassifier
    _BACKEND = "xgb"
except ImportError:
    from lightgbm import LGBMClassifier
    _BACKEND = "lgbm"


@dataclass(frozen=True)
class BarrierConfig:
    tp_r: float = 2.50
    sl_r: float = 1.00
    vertical_bars: int = 24
    min_terminal_r: float = 0.20


@dataclass(frozen=True)
class CVConfig:
    n_folds: int = 6
    purge_hours: int = 72      # 288 bars @15m
    embargo_hours: int = 24    # 96 bars @15m
    min_train_events: int = 100


@dataclass(frozen=True)
class ModelConfig:
    # Tuned for ~1,400 pooled events / 1yr: shallow enough to not overfit,
    # min_child_weight low enough to split while regularized.
    max_depth: int = 4
    min_child_weight: int = 8
    reg_alpha: float = 1.5
    reg_lambda: float = 3.5
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    learning_rate: float = 0.03
    n_estimators: int = 600
    random_state: int = 42


@dataclass(frozen=True)
class GateConfig:
    quantile_grid: Tuple[float, ...] = (0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80)
    min_trades_per_window: int = 6
    bars_per_month: int = 2880   # 30d * 96 bars @15m


class PooledInstitutionalMetaLabeler:
    """
    Cross-asset pooled meta-labeling (Lopez de Prado secondary layer).

    - Events from ALL symbols concatenated into one training matrix.
    - Features are cross-sectionally stationary (rank-based + unit-free ratios).
    - Grouped purged WF-CV: groups = (symbol, fold-time-block), purge/embargo
      applied in time so no label horizon leaks across the split.
    - Adaptive quantile gate: tau chosen on OOF probabilities to maximize
      expectancy (mean R) subject to trade-count feasibility.
    """

    def __init__(self,
                 barrier: BarrierConfig = BarrierConfig(),
                 cv: CVConfig = CVConfig(),
                 model: ModelConfig = ModelConfig(),
                 gate: GateConfig = GateConfig()):
        self.barrier = barrier
        self.cv_cfg = cv
        self.model_cfg = model
        self.gate = gate
        self.model_: Optional[object] = None
        self.oof_: Optional[pd.DataFrame] = None
        self.tau_: float = 0.50
        self.fold_aucs_: List[float] = []
        self.feat_cols_: List[str] = []

    # ==================================================================
    # FEATURES — cross-sectionally stationary, zero lookahead
    # ==================================================================
    def build_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        df: single-symbol OHLCV + microstructure columns, DatetimeIndex.
        All transforms are rolling/backward-looking; ratios are unit-free so
        they're comparable across BTC/DOGE price scales.
        """
        T = len(df)
        idx = df.index
        get = lambda n, d: df.get(n, pd.Series(d, index=idx)).astype(np.float64)

        cl = df["close"].astype(np.float64)
        atr = get("atr_14", cl * 0.002).clip(lower=1e-12)
        vol = get("volume_base", get("volume", pd.Series(np.ones(T), index=idx))).clip(lower=1e-12)

        F = pd.DataFrame(index=idx)

        # --- Footprint / taker delta ratio: (buy - sell) / (buy + sell) in [-1, 1] ---
        if "taker_buy_vol_btc" in df.columns and "taker_sell_vol_btc" in df.columns:
            tb = df["taker_buy_vol_btc"].astype(np.float64)
            ts = df["taker_sell_vol_btc"].astype(np.float64)
            F["fp_delta_ratio"] = ((tb - ts) / (tb + ts).clip(lower=1e-12)).rolling(12, min_periods=1).mean().fillna(0.0)
        elif "taker_buy_volume" in df.columns:
            tb = df["taker_buy_volume"].astype(np.float64)
            ts = (vol - tb).clip(lower=0.0)
            F["fp_delta_ratio"] = ((tb - ts) / (tb + ts).clip(lower=1e-12)).rolling(12, min_periods=1).mean().fillna(0.0)
        else:
            F["fp_delta_ratio"] = pd.Series(0.0, index=idx)

        # --- CVD rolling z-score (backward window, cross-asset comparable) ---
        cvd = get("future_cvd_15m", pd.Series(np.zeros(T), index=idx))
        d_cvd = cvd.diff().fillna(0.0)
        m = d_cvd.rolling(96, min_periods=1).mean()
        s = d_cvd.rolling(96, min_periods=1).std(ddof=0).clip(lower=1e-12).fillna(1.0)
        F["cvd_zs"] = ((d_cvd - m) / s).clip(-10, 10).fillna(0.0)

        # --- Liquidation z-scores (already z-scaled upstream; clip tails) ---
        F["long_liq_zs"] = get("long_liq_zs", np.zeros(T)).clip(-10, 10).fillna(0.0)
        F["short_liq_zs"] = get("short_liq_zs", np.zeros(T)).clip(-10, 10).fillna(0.0)

        # --- CVD/liquidation divergence (unit-free) ---
        zc = get("zc_div", pd.Series(np.zeros(T), index=idx))
        F["zc_div"] = zc.clip(-5, 5).fillna(0.0)

        # --- RSI centered/scaled ---
        rsi = get("rsi_14", pd.Series(np.full(T, 50.0), index=idx))
        F["rsi_c"] = ((rsi - 50.0) / 50.0).fillna(0.0)

        # --- VWAP distance (already a z-score) ---
        vwz = df.get("dist_to_vwap_zs", df.get("vwap_zscore", pd.Series(np.zeros(T), index=idx))).astype(np.float64)
        F["dist_to_vwap_zs"] = vwz.clip(-10, 10).fillna(0.0)

        # --- Normalized volatility level + its z-score ---
        atr_n = (atr / cl).clip(0, 0.05)
        F["atr_norm"] = atr_n.fillna(0.002)
        m2 = atr_n.rolling(96, min_periods=1).mean()
        s2 = atr_n.rolling(96, min_periods=1).std(ddof=0).clip(lower=1e-12).fillna(1.0)
        F["atr_norm_zs"] = ((atr_n - m2) / s2).clip(-10, 10).fillna(0.0)

        # --- Volume ratio (relative to own 96-bar baseline) ---
        vol_base = vol.rolling(96, min_periods=1).mean().clip(lower=1e-12)
        F["volume_ratio"] = (vol / vol_base).clip(0, 10).fillna(1.0)

        # --- Bar geometry (unit-free): body/range, close position ---
        rng = (df["high"] - df["low"]).clip(lower=1e-12)
        F["body_ratio"] = ((cl - df["open"]) / rng).clip(-1, 1).fillna(0.0)
        F["close_pos"] = ((cl - df["low"]) / rng * 2.0 - 1.0).clip(-1, 1).fillna(0.0)

        # --- Short-horizon momentum (log return z-score) ---
        r1 = np.log(cl.clip(lower=1e-12)).diff().fillna(0.0)
        m3 = r1.rolling(96, min_periods=1).mean()
        s3 = r1.rolling(96, min_periods=1).std(ddof=0).clip(lower=1e-12).fillna(1.0)
        F["ret_zs"] = ((r1 - m3) / s3).clip(-10, 10).fillna(0.0)

        return F

    # ==================================================================
    # TRIPLE-BARRIER LABELS (stop-first, causal, next-open entry)
    # ==================================================================
    def triple_barrier_labels(self, df: pd.DataFrame, event_mask: np.ndarray,
                              side: np.ndarray, r_dist: np.ndarray) -> pd.DataFrame:
        op, hi, lo, cl = (df[c].values for c in ("open", "high", "low", "close"))
        B = self.barrier
        events = np.flatnonzero(event_mask)
        n = len(df)
        y = np.zeros(len(events), dtype=np.int8)
        t_out = np.zeros(len(events), dtype=np.int64)
        exit_r = np.zeros(len(events), dtype=np.float64)

        for k, t in enumerate(events):
            entry = op[t + 1] if t + 1 < n else cl[t]
            d = max(r_dist[t], 1e-12)
            up = entry + side[t] * B.tp_r * d
            dn = entry - side[t] * B.sl_r * d
            end = min(t + B.vertical_bars, n - 1)
            hit, tout, xr = 0, end, 0.0
            for j in range(t + 1, end + 1):
                stop_hit = lo[j] <= dn if side[t] == 1 else hi[j] >= dn
                tgt_hit = hi[j] >= up if side[t] == 1 else lo[j] <= up
                if stop_hit:                       # conservative stop-first
                    hit, tout, xr = 0, j, -B.sl_r
                    break
                if tgt_hit:
                    hit, tout, xr = 1, j, B.tp_r
                    break
            else:
                xr = side[t] * (cl[end] - entry) / d
                hit = 1 if xr >= B.min_terminal_r else 0
            y[k], t_out[k], exit_r[k] = hit, tout, xr

        return pd.DataFrame({"y_meta": y, "t_out": t_out, "exit_r": exit_r}, index=events)

    # ==================================================================
    # POOL EVENTS ACROSS SYMBOLS
    # ==================================================================
    def pool_events(self, per_symbol: Dict[str, pd.DataFrame],
                    strategy, train_start: pd.Timestamp,
                    train_end: pd.Timestamp) -> pd.DataFrame:
        """
        For each symbol: primary signals on [train_start, train_end),
        triple-barrier labels, features -> one pooled event table.
        Rows: (symbol, bar_position). All strictly inside the training slice.
        """
        frames = []
        for sym, df_sym in per_symbol.items():
            sl = df_sym.loc[train_start:train_end]
            if len(sl) < self.barrier.vertical_bars + 48:
                continue
            sig = strategy.generate_signals(sl.copy())
            mask = sig["side"].to_numpy() != 0
            if mask.sum() < 5:
                continue
            side = np.where(mask, sig["side"].to_numpy(), 1).astype(np.int8)
            labels = self.triple_barrier_labels(sl, mask, side, sig["raw_r"].to_numpy())
            ev = labels.index.to_numpy()
            X = self.build_features(sl).iloc[ev]
            tab = X.reset_index(drop=True)
            tab["symbol"] = sym
            tab["bar_pos"] = ev
            tab["abs_bar"] = df_sym.index.get_indexer(sl.index)[ev]
            tab["y"] = labels["y_meta"].to_numpy()
            tab["t_out"] = labels["t_out"].to_numpy()
            tab["exit_r"] = labels["exit_r"].to_numpy()
            frames.append(tab)
        if not frames:
            raise RuntimeError("PooledMetaLabeler: zero events pooled across symbols.")
        pooled = pd.concat(frames, ignore_index=True)
        feat_cols = [c for c in pooled.columns if c not in ("symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r")]
        pooled[feat_cols] = pooled[feat_cols].clip(-15, 15)
        return pooled

    # ==================================================================
    # PURGED GROUPED WF-CV (grouped by time block, purged by label horizon)
    # ==================================================================
    def _cv_splits(self, pooled: pd.DataFrame) -> List[Tuple[np.ndarray, np.ndarray]]:
        C, B = self.cv_cfg, self.barrier
        purge = (C.purge_hours * 60) // 15
        embargo = (C.embargo_hours * 60) // 15
        # Split on global time (abs_bar) — groups all symbols in the same period
        edges = np.quantile(pooled["abs_bar"].to_numpy(),
                            np.linspace(0, 1, C.n_folds + 1)).astype(int)
        edges = np.unique(edges)
        splits = []
        for f in range(len(edges) - 2, -1, -1):   # expanding window: latest fold = test
            t0, t1 = edges[f], edges[f + 1]
            te = pooled.index[(pooled["abs_bar"] >= t0) & (pooled["abs_bar"] < t1)].to_numpy()
            tr = pooled.index[pooled["abs_bar"] < t0 - purge - embargo].to_numpy()
            # purge: drop train events whose horizon extends into [t0 - purge, t1)
            tr = tr[~((pooled.loc[tr, "abs_bar"] + B.vertical_bars >= t0 - purge))]
            if len(tr) >= C.min_train_events and len(te) >= 10:
                splits.append((tr, te))
        return splits

    def _make_model(self):
        m = self.model_cfg
        if _BACKEND == "xgb":
            return XGBClassifier(
                max_depth=m.max_depth, min_child_weight=m.min_child_weight,
                reg_alpha=m.reg_alpha, reg_lambda=m.reg_lambda,
                subsample=m.subsample, colsample_bytree=m.colsample_bytree,
                learning_rate=m.learning_rate, n_estimators=m.n_estimators,
                eval_metric="logloss", tree_method="hist",
                random_state=m.random_state, n_jobs=-1)
        return LGBMClassifier(
            max_depth=m.max_depth, min_child_weight=m.min_child_weight,
            reg_alpha=m.reg_alpha, reg_lambda=m.reg_lambda,
            subsample=m.subsample, colsample_bytree=m.colsample_bytree,
            learning_rate=m.learning_rate, n_estimators=m.n_estimators,
            random_state=m.random_state, n_jobs=-1, verbose=-1)

    # ==================================================================
    # FIT + ADAPTIVE QUANTILE GATE
    # ==================================================================
    def fit(self, pooled: pd.DataFrame) -> Dict:
        from sklearn.metrics import roc_auc_score
        feat_cols = [c for c in pooled.columns
                     if c not in ("symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r")]
        X_all = pooled[feat_cols].to_numpy(np.float64)
        y_all = pooled["y"].to_numpy(np.int8)
        r_all = pooled["exit_r"].to_numpy(np.float64)
        t_all = pooled["abs_bar"].to_numpy()

        oof = np.full(len(pooled), np.nan)
        self.fold_aucs_ = []
        for tr, te in self._cv_splits(pooled):
            mdl = self._make_model()
            mdl.fit(X_all[tr], y_all[tr])
            oof[te] = mdl.predict_proba(X_all[te])[:, 1]
            if len(np.unique(y_all[te])) > 1:
                self.fold_aucs_.append(float(roc_auc_score(y_all[te], oof[te])))

        valid = np.isfinite(oof)
        if valid.sum() > 20:
            self.tau_ = self._calibrate_tau(oof[valid], y_all[valid], r_all[valid])
        else:
            self.tau_ = 0.50

        # Deployed model: refit on full pooled training slice
        self.model_ = self._make_model()
        self.model_.fit(X_all, y_all)
        self.feat_cols_ = feat_cols

        self.oof_ = pd.DataFrame({
            "symbol": pooled["symbol"].to_numpy(), "abs_bar": t_all,
            "proba_oof": oof, "y": y_all, "exit_r": r_all})
        return {
            "n_events": int(len(pooled)),
            "positive_rate": float(y_all.mean()),
            "mean_cv_auc": float(np.mean(self.fold_aucs_)) if self.fold_aucs_ else 0.50,
            "fold_aucs": self.fold_aucs_,
            "calibrated_tau": self.tau_,
            "oof_expectancy_all": float(r_all[valid].mean()) if valid.sum() > 0 else 0.0,
        }

    def _calibrate_tau(self, p: np.ndarray, y: np.ndarray, r: np.ndarray) -> float:
        """
        Adaptive gate: choose smallest quantile cut whose OOF expectancy > 0
        and implied trade volume >= min per window; else return fallback.
        """
        best_tau, best_exp = 1.0, -np.inf
        for q in sorted(self.gate.quantile_grid):
            tau = float(np.quantile(p, q))
            sel = p >= tau
            n_sel = int(sel.sum())
            if n_sel < self.gate.min_trades_per_window:
                continue
            exp = float(r[sel].mean())
            monthly_events = len(p) / 12.0
            expected_trades = monthly_events * (1.0 - q)
            if exp > best_exp and expected_trades >= self.gate.min_trades_per_window:
                best_exp, best_tau = exp, tau

        if best_exp <= 0 or best_tau == 1.0:
            # Fallback to top 30% quantile
            return float(np.quantile(p, 0.70))
        return best_tau

    # ==================================================================
    # INFERENCE + GATE
    # ==================================================================
    def score_signals(self, df_sym: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
        """Score a single symbol's OOS signals with the pooled model and gate at tau."""
        out = signals.copy()
        mask = out["side"].to_numpy() != 0
        proba = np.full(len(out), np.nan)
        if mask.any() and self.model_ is not None:
            X = self.build_features(df_sym).iloc[np.flatnonzero(mask)][self.feat_cols_]
            ok = np.isfinite(X.to_numpy(np.float64)).all(axis=1)
            ev = np.flatnonzero(mask)[ok]
            if len(ev) > 0:
                proba[ev] = self.model_.predict_proba(
                    X.to_numpy(np.float64)[ok])[:, 1]
        keep = np.isfinite(proba) & (proba >= self.tau_)
        out.loc[:, "side"] = np.where(keep, out["side"].to_numpy(), 0)
        out.loc[out["side"] == 0, "raw_r"] = 0.0
        out["proba"] = proba
        return out
