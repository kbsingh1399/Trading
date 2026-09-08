"""Event-conditioned, purged meta-labeling for a single asset and strategy.

Labels mean target reached under the actual ratcheted execution policy, not
merely positive PnL. The conditional 24-bar decay is not a maximum holding time.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
from xgboost import XGBClassifier

from Engine.core.execution_kernel import ExecutionKernel


class InstitutionalMetaLabeler:
    FEATURES = (
        "fp_delta_ratio", "zc_div", "long_liq_zs", "short_liq_zs",
        "rsi_14", "dist_to_vwap_zs", "atr_norm", "volume_ratio_sma20",
    )

    def __init__(self, kernel=None, *, threshold=0.5, n_splits=3,
                 min_events=60):
        if not 0 < threshold < 1 or n_splits < 2 or min_events < 20:
            raise ValueError("Invalid meta-labeler configuration")
        self.kernel = kernel or ExecutionKernel()
        self.threshold = float(threshold)
        self.n_splits = int(n_splits)
        self.min_events = int(min_events)
        self.purge = pd.Timedelta(hours=72)
        self.model = self.calibrator = None
        self.oos_start = None
        self.audit = {}

    @staticmethod
    def bar_times(df):
        if not df.index.is_unique:
            raise ValueError("Bar indexes must be unique")
        if "open_time_ms" in df:
            times = pd.DatetimeIndex(pd.to_datetime(df.open_time_ms, unit="ms", utc=True))
        elif "datetime_utc" in df:
            times = pd.DatetimeIndex(pd.to_datetime(df.datetime_utc, utc=True))
        elif isinstance(df.index, pd.DatetimeIndex):
            times = pd.DatetimeIndex(pd.to_datetime(df.index, utc=True))
        else:
            raise ValueError("Explicit UTC bar timestamps required")
        if times.hasnans or times.has_duplicates or not times.is_monotonic_increasing:
            raise ValueError("Bar timestamps must be unique and increasing")
        if len(times) > 1 and not np.all(times[1:] - times[:-1] == pd.Timedelta(minutes=15)):
            raise ValueError("Expected consecutive 15-minute bars")
        if "symbol" in df and df.symbol.nunique(dropna=False) != 1:
            raise ValueError("Fit and inference require exactly one asset")
        return times

    @classmethod
    def extract_features(cls, df):
        required = ["close", "atr_14", "volume_base", "zc_div",
                    "long_liq_zs", "short_liq_zs", "rsi_14", "vwap_zscore"]
        missing = [c for c in required if c not in df]
        if missing:
            raise ValueError(f"Missing meta features: {missing}")
        volume = df.volume_base.astype(float).where(df.volume_base > 0)
        close = df.close.astype(float).where(df.close > 0)
        if "fp_delta_ratio" in df:
            delta = df.fp_delta_ratio.astype(float)
        elif "future_cvd_15m" in df:
            # Aggregate taker delta / base volume, not a fabricated ladder feature.
            delta = df.future_cvd_15m / volume
        else:
            raise ValueError("Need fp_delta_ratio or actual futures per-bar delta")
        result = pd.DataFrame({
            "fp_delta_ratio": delta,
            # Canonical zc_div is a base-volume difference, not a z-score.
            "zc_div": df.zc_div / volume,
            "long_liq_zs": df.long_liq_zs,
            "short_liq_zs": df.short_liq_zs,
            "rsi_14": df.rsi_14 / 100.0,
            "dist_to_vwap_zs": df.vwap_zscore,
            "atr_norm": df.atr_14.where(df.atr_14 > 0) / close,
            "volume_ratio_sma20": volume / volume.shift(1).rolling(20, min_periods=20).mean(),
        }, index=df.index)
        return result.replace([np.inf, -np.inf], np.nan)

    @classmethod
    def event_features(cls, df, signals):
        if not df.index.equals(signals.index):
            raise ValueError("Signals and bars must have identical indexes")
        if not signals.side.isin([-1, 0, 1]).all():
            raise ValueError("Invalid primary direction")
        x = cls.extract_features(df)
        # Fold short setups into the same directional coordinate system.
        short = signals.side.eq(-1)
        for col in ("fp_delta_ratio", "zc_div", "dist_to_vwap_zs"):
            x.loc[short, col] *= -1
        x.loc[short, "rsi_14"] = 1.0 - x.loc[short, "rsi_14"]
        pair = x.loc[short, ["short_liq_zs", "long_liq_zs"]].to_numpy()
        x.loc[short, ["long_liq_zs", "short_liq_zs"]] = pair
        return x

    def label_events(self, df, signals):
        times = self.bar_times(df)
        x = self.event_features(df, signals)
        candidates = np.flatnonzero(
            signals.side.ne(0).to_numpy()
            & np.isfinite(x.to_numpy()).all(axis=1)
            & np.isfinite(signals.raw_r.to_numpy())
            & signals.raw_r.gt(0).to_numpy()
        )
        rows = []
        prices = self.kernel.prepare_prices(df)
        for t in candidates:
            trade = self.kernel.simulate_event(df, int(t), int(signals.side.iloc[t]),
                                               float(signals.raw_r.iloc[t]), prices=prices)
            if trade is None or trade["reason"] == "TERMINAL_SETTLEMENT":
                continue  # Right-censored is unknown, never a synthetic loss.
            rows.append({
                "bar": int(t), "start": times[t] + pd.Timedelta(minutes=15),
                "end": times[trade["exit_bar"]] + pd.Timedelta(minutes=15),
                "label": int(trade["reason"] in ("TARGET_BAR", "TARGET_OPEN")),
                "net_r": trade["r"], "reason": trade["reason"],
            })
        return pd.DataFrame(rows, columns=["bar", "start", "end", "label", "net_r", "reason"])

    @staticmethod
    def _new_model():
        return XGBClassifier(
            objective="binary:logistic", eval_metric="logloss", max_depth=3,
            learning_rate=0.03, n_estimators=120, subsample=0.8,
            colsample_bytree=0.8, reg_alpha=1.5, reg_lambda=3.5,
            min_child_weight=15, random_state=42, n_jobs=1, tree_method="hist",
        )

    @staticmethod
    def _logits(probability):
        p = np.clip(np.asarray(probability), 1e-6, 1 - 1e-6)
        return np.log(p / (1 - p)).reshape(-1, 1)

    def fit(self, df, signals, oos_start):
        self.model = self.calibrator = None
        self.audit = {}
        start = pd.Timestamp(oos_start)
        start = start.tz_localize("UTC") if start.tzinfo is None else start.tz_convert("UTC")
        times = self.bar_times(df)
        if not df.index.equals(signals.index):
            raise ValueError("Signals and bars must have identical indexes")
        cutoff = start - self.purge
        keep = times + pd.Timedelta(minutes=15) < cutoff
        history, primary = df.loc[keep].copy(), signals.loc[keep].copy()
        events = self.label_events(history, primary)
        if len(events) < self.min_events or events.label.nunique() < 2:
            raise ValueError("Insufficient resolved primary events or class support")
        x = self.event_features(history, primary).iloc[events.bar.to_numpy()].reset_index(drop=True)
        y = events.label.to_numpy(dtype=int)
        oof = np.full(len(events), np.nan)
        folds = []
        # Expanding training only: no later fold observations can enter training.
        for validation in np.array_split(np.arange(len(events)), self.n_splits + 1)[1:]:
            boundary = events.start.iloc[validation[0]] - self.purge
            train = np.flatnonzero((events.end < boundary).to_numpy())
            if len(train) < 20 or len(np.unique(y[train])) < 2:
                continue
            model = self._new_model()
            model.fit(x.iloc[train], y[train])
            oof[validation] = model.predict_proba(x.iloc[validation])[:, 1]
            folds.append({"train_end": str(events.end.iloc[train].max()),
                          "validation_start": str(events.start.iloc[validation[0]]),
                          "train_events": len(train), "validation_events": len(validation)})
        calibration_rows = np.flatnonzero(np.isfinite(oof))
        if len(calibration_rows) < 20 or len(np.unique(y[calibration_rows])) < 2:
            raise ValueError("Insufficient purged out-of-fold calibration support")
        calibrator = LogisticRegression(C=1.0, solver="lbfgs", random_state=42)
        calibrator.fit(self._logits(oof[calibration_rows]), y[calibration_rows])
        model = self._new_model()
        model.fit(x, y)
        self.model, self.calibrator, self.oos_start = model, calibrator, start
        self.audit = {
            "oos_start": str(start), "purge_cutoff": str(cutoff),
            "latest_label_end": str(events.end.max()), "events": len(events),
            "positive_events": int(y.sum()), "calibration_events": len(calibration_rows),
            "raw_oof_brier": float(brier_score_loss(y[calibration_rows], oof[calibration_rows])),
            "threshold": self.threshold, "folds": folds,
        }
        return self

    def filter_signals(self, df, signals):
        if self.model is None or self.calibrator is None:
            raise ValueError("Meta-labeler has not been fitted")
        times = self.bar_times(df)
        x = self.event_features(df, signals)
        active = signals.side.ne(0).to_numpy()
        if np.any(active & (times < self.oos_start)):
            raise ValueError("Inference candidates precede the frozen OOS boundary")
        valid = active & np.isfinite(x.to_numpy()).all(axis=1)
        out = signals.copy()
        out["meta_probability"] = np.nan
        out.loc[:, ["side", "raw_r"]] = 0
        positions = np.flatnonzero(valid)
        if len(positions):
            raw = self.model.predict_proba(x.iloc[positions])[:, 1]
            calibrated = self.calibrator.predict_proba(self._logits(raw))[:, 1]
            out.iloc[positions, out.columns.get_loc("meta_probability")] = calibrated
            accepted = positions[calibrated >= self.threshold]
            out.iloc[accepted, out.columns.get_indexer(["side", "raw_r"])] = signals.iloc[accepted][["side", "raw_r"]].to_numpy()
        return out
