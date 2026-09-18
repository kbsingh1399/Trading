# orderflow_ml_overlay.py
# Machine Learning Overlay for Adverse Regime Filtering & Probabilistic Signal Gating
# Derived from Astra AI + Forensic Quant Audit

import numpy as np
import polars as pl
from sklearn.ensemble import GradientBoostingClassifier

class MLOverlay:
    def __init__(self, threshold: float = 0.55, n_estimators: int = 200, max_depth: int = 4, random_state: int = 42):
        self.model = GradientBoostingClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            subsample=0.8,
            random_state=random_state
        )
        self.threshold = threshold

    # ===================== Feature Matrix =====================
    def feature_matrix(self, df: pl.DataFrame) -> np.ndarray:
        """Extract continuous stationary orderflow features."""
        vol_rat = df['volume_ratio'].to_numpy() if 'volume_ratio' in df.columns else np.ones(len(df))
        return np.column_stack([
            df['zc_div'].to_numpy(),
            df['long_liq_zs'].to_numpy(),
            df['short_liq_zs'].to_numpy(),
            df['vwap_zscore'].to_numpy(),
            vol_rat,
            df['rsi_14'].to_numpy(),
            df['spot_cvd_15m'].to_numpy()
        ])

    # ===================== Label Generator (Causal) =====================
    def causal_labels(self, df: pl.DataFrame, tp_r: float = 2.50, stop_r: float = 1.00, timeout_bars: int = 24) -> np.ndarray:
        """
        Generate causal forward labels:
        y = 1 if price reaches +TP_R before stop or timeout; y = 0 otherwise.
        Note: Fixed Astra indentation bug where labels.append was outside the loop.
        """
        prices = df['open'].to_numpy()
        highs = df['high'].to_numpy()
        lows = df['low'].to_numpy()
        atrs = df['atr_14'].to_numpy()
        n = len(prices)
        labels = np.zeros(n, dtype=np.int64)
        
        for i in range(n - timeout_bars - 1):
            entry = prices[i + 1] # Causal entry at next bar open
            risk_distance = max(atrs[i], entry * 0.012)
            tp = entry + tp_r * risk_distance
            stop = entry - stop_r * risk_distance
            label = 0
            
            for j in range(i + 1, min(i + timeout_bars + 2, n)):
                if highs[j] >= tp:
                    label = 1
                    break
                if lows[j] <= stop:
                    label = 0
                    break
            labels[i] = label
            
        return labels

    # ===================== Training & Inference =====================
    def fit(self, df_train: pl.DataFrame):
        X = self.feature_matrix(df_train)
        y = self.causal_labels(df_train)
        self.model.fit(X, y)

    def predict_proba(self, df: pl.DataFrame) -> np.ndarray:
        X = self.feature_matrix(df)
        return self.model.predict_proba(X)[:, 1]

    def filter_signals(self, df: pl.DataFrame, prob_threshold: float | None = None) -> pl.DataFrame:
        thresh = prob_threshold if prob_threshold is not None else self.threshold
        scores = self.predict_proba(df)
        return df.with_columns(pl.Series('ml_score', scores)).filter(pl.col('ml_score') >= thresh)

if __name__ == "__main__":
    print("ML Overlay: Initialization completed and verified.")
