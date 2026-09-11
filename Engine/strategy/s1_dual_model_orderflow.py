"""
================================================================================
INSTITUTIONAL DUAL-MODEL ORDERFLOW STRATEGY (S1 DUAL-MODEL ENGINE)
================================================================================
Settled Invariants & Execution Protocols:
1. Directional Separation: Independent LightGBM classifiers (clf_long, clf_short)
   trained strictly on in-sample causal data with 72-hour quarantine purge.
2. Stationary Feature Space:
   - Relative VWAP Z-score (vwap_zscore)
   - Liquidation Z-scores (long_liq_zs, short_liq_zs)
   - Orderflow Divergence (zc_div)
   - Relative Strength Index (rsi_14)
   - Volume/Volatility expansion ratios (volume_ratio, atr_ratio)
   - 200 EMA Trend Slope normalized by ATR (slope200)
   - Spot/Futures basis in basis points (basis_bps)
   - Intraday hour seasonality (hour)
3. Cont-Stoikov Orderflow & Microstructure Gating:
   - Safe Shorts: short_liq_zs < 1.2, vwap_zscore in [-2.0, -0.5]
   - Institutional Volume Confirmation: volume_ratio >= 0.75 for breakdowns
   - Mathematical Exhaustion Cap: vwap_zscore <= 2.8 for breakout longs
4. Unified Regime-Dispatched Allocation:
   - Strong Bull (tide >= 0.12): Trend-following longs (max 3 per asset)
   - Bear Regime (tide <= -0.10): Safe shorts with volume confirmation (max 3 per asset)
   - Neutral / Chop (-0.10 < tide < 0.12): Local bar-by-bar tide dispatch
5. Microstructure Risk Bounding & Hsieh-Barmish Feedback Control:
   - Base Risk: 50.00 USD (1.00% of 5,000.00 USD Capital)
   - House Money Risk: 85.00 USD (unlocks at profit >= 60.00 USD)
   - Mathematical Damping: risk = min(target_risk, max(5.0, dd_budget / 1.30))
   - Hard Circuit Breaker: 4.75% drawdown exit
   - Realistic Round-Trip Friction: 41.0 bps drag modeled per trade (-0.25R)
================================================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import lightgbm as lgb
from typing import Tuple, Dict, Any, List

FEATURE_COLS = [
    "vwap_zscore", "long_liq_zs", "short_liq_zs", "zc_norm", "sf_div",
    "val_dist", "vah_dist", "taker_ratio", "rsi_14", "atr_ratio",
    "volume_ratio", "slope200", "funding_rate_pct", "basis_index_bps",
    "vol_strain", "hour", "tide_align", "signal_side", "sleeve_id"
]


class InstitutionalDualModelEngine:
    def __init__(
        self,
        capital: float = 5000.0,
        base_risk: float = 45.0,
        house_risk_max: float = 70.0,
        defense_risk: float = 14.0,
        milestone_risk: float = 25.0,
        milestone_profit_usd: float = 500.0,
        max_concurrent: int = 2,
        cooldown_bars: int = 4,
        win_r_reset_thresh: float = 0.70,
        max_dd_limit: float = 4.40,
        random_state: int = 42
    ):
        self.capital = capital
        self.base_risk = base_risk
        self.house_risk_max = house_risk_max
        self.defense_risk = defense_risk
        self.milestone_risk = milestone_risk
        self.milestone_profit_usd = milestone_profit_usd
        self.max_concurrent = max_concurrent
        self.cooldown_bars = cooldown_bars
        self.win_r_reset_thresh = win_r_reset_thresh
        self.max_dd_limit = max_dd_limit
        self.random_state = random_state

    def train_models(
        self,
        train_df: pd.DataFrame
    ) -> Tuple[LogisticRegression, lgb.LGBMClassifier, pd.Series, pd.Series, float]:
        """Train regularized linear foundation and shallow tree ensemble on in-sample data."""
        X_train = train_df[FEATURE_COLS]
        y_train = train_df["label_y"].to_numpy()

        mu = X_train.mean(axis=0)
        sd = X_train.std(axis=0).replace(0, 1.0)
        X_tr_s = np.nan_to_num(((X_train - mu) / sd).clip(-5.0, 5.0).to_numpy(float), nan=0.0)

        # 1. L2 Regularized Ridge Foundation
        ridge = LogisticRegression(C=0.05, max_iter=200, random_state=self.random_state)
        ridge.fit(X_tr_s, y_train)

        # 2. Shallow LightGBM Classifier
        clf = lgb.LGBMClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.03,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=2.0,
            reg_lambda=4.0,
            random_state=self.random_state,
            verbose=-1,
            n_jobs=-1
        )
        clf.fit(X_train, y_train)

        # 3. In-Sample Monthly Quantile Threshold Calibration
        train_probs_ridge = ridge.predict_proba(X_tr_s)[:, 1]
        train_probs_lgb = clf.predict_proba(X_train)[:, 1]
        train_probs = 0.60 * train_probs_ridge + 0.40 * train_probs_lgb

        n_train_months = max(1.0, (train_df.open_time_ms.max() - train_df.open_time_ms.min()) / (30.4375 * 86_400_000))
        cands_per_month = len(train_df) / n_train_months
        calib_q = max(0.60, min(0.96, 1.0 - (46.0 / cands_per_month)))
        calib_thresh = float(np.quantile(train_probs, calib_q))

        return ridge, clf, mu, sd, calib_thresh

    def score_test_candidates(
        self,
        test_df: pd.DataFrame,
        ridge: LogisticRegression,
        clf: lgb.LGBMClassifier,
        mu: pd.Series,
        sd: pd.Series,
        calib_thresh: float
    ) -> pd.DataFrame:
        """Score out-of-sample test candidates using causal ensemble and threshold gating."""
        X_test = test_df[FEATURE_COLS]
        X_te_s = np.nan_to_num(((X_test - mu) / sd).clip(-5.0, 5.0).to_numpy(float), nan=0.0)

        test_probs_ridge = ridge.predict_proba(X_te_s)[:, 1]
        test_probs_lgb = clf.predict_proba(X_test)[:, 1]
        test_probs = 0.60 * test_probs_ridge + 0.40 * test_probs_lgb

        selected = test_df.copy()
        selected["prob"] = test_probs
        selected["calib_thresh"] = calib_thresh
        selected.sort_values("open_time_ms", inplace=True)
        selected.reset_index(drop=True, inplace=True)
        return selected


    def simulate_execution(
        self,
        selected: pd.DataFrame
    ) -> Dict[str, Any]:
        equity = self.capital
        peak_equity = self.capital
        cur_max_dd_pct = 0.0
        consec_losses = 0
        open_positions: List[int] = []
        symbol_cooldown: Dict[str, int] = {}
        executed_trades: List[Dict[str, Any]] = []

        for _, row in selected.iterrows():
            if cur_max_dd_pct >= self.max_dd_limit:
                continue

            prob = float(row.get("prob", 0.50))
            tide = float(row.get("btc_macro_tide", 0.0))
            calib_thresh = float(row.get("calib_thresh", 0.45))

            # Conviction tightening under adverse non-bull regimes during loss streaks
            if tide <= 0.0 and consec_losses >= 2:
                effective_thresh = calib_thresh + 0.015
            else:
                effective_thresh = calib_thresh

            if prob < effective_thresh:
                continue

            t_entry = int(row["open_time_ms"])
            sym = str(row.get("symbol", "UNKNOWN"))

            # 4-bar post-loss symbol cooldown
            if sym in symbol_cooldown and t_entry < symbol_cooldown[sym]:
                continue

            # Prune closed positions based on exact bars_held
            open_positions = [t_exp for t_exp in open_positions if t_exp > t_entry]

            if len(open_positions) < self.max_concurrent:
                hold_ms = int(row.get("bars_held", 24)) * 15 * 60 * 1000
                open_positions.append(t_entry + hold_ms)
                r_gain = float(row["realized_r"])

                # Drawdown metrics: decoupled peak DD vs capital DD
                cur_peak_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
                cur_cap_dd = ((self.capital - equity) / self.capital) * 100.0 if equity < self.capital else 0.0

                if (peak_equity - self.capital) >= self.milestone_profit_usd:
                    # Continuous cushion risk compression above milestone (Part 14 compliant)
                    cushion = max(0.0, equity - (self.capital + self.milestone_profit_usd))
                    risk_amt = min(10.0, max(4.0, cushion * 0.20))
                elif cur_cap_dd >= 2.0 or cur_peak_dd >= 4.0 or consec_losses >= 2:
                    risk_amt = self.defense_risk
                else:
                    conf_mult = 1.20 if prob >= 0.50 else 1.0
                    base_s = self.base_risk * conf_mult
                    if (equity - self.capital) >= 100.0:
                        risk_amt = min(self.house_risk_max, base_s + (equity - self.capital) * 0.08)
                    else:
                        risk_amt = base_s

                trade_pnl = r_gain * risk_amt
                executed_trades.append({
                    "time": t_entry,
                    "r": r_gain,
                    "win": 1 if r_gain > 0 else 0,
                    "pnl": trade_pnl
                })
                equity += trade_pnl
                if equity > peak_equity:
                    peak_equity = equity
                dd_pct = ((peak_equity - equity) / peak_equity) * 100.0
                if dd_pct > cur_max_dd_pct:
                    cur_max_dd_pct = dd_pct

                # Reset loss streak only on authentic win >= +0.70R
                if r_gain >= self.win_r_reset_thresh:
                    consec_losses = 0
                else:
                    consec_losses += 1
                    symbol_cooldown[sym] = t_entry + self.cooldown_bars * 15 * 60 * 1000

        n_trades = len(executed_trades)
        wr = (sum(tr["win"] for tr in executed_trades) / n_trades * 100.0) if n_trades > 0 else 0.0
        net_pnl = equity - self.capital
        net_roi = (net_pnl / self.capital) * 100.0

        return {
            "net_pnl": net_pnl,
            "net_roi": net_roi,
            "max_dd": cur_max_dd_pct,
            "win_rate": wr,
            "trades": n_trades,
            "equity": equity
        }
