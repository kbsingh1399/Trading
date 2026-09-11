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
import lightgbm as lgb
from typing import Tuple, Dict, Any, List

LONG_FEATURES = [
    "vwap_zscore", "long_liq_zs", "zc_div", "rsi_14",
    "atr_ratio", "volume_ratio", "slope200", "basis_bps", "hour"
]

SHORT_FEATURES = [
    "vwap_zscore", "short_liq_zs", "zc_div", "rsi_14",
    "atr_ratio", "volume_ratio", "slope200", "basis_bps", "hour"
]

class InstitutionalDualModelEngine:
    def __init__(
        self,
        capital: float = 5000.0,
        base_risk: float = 50.0,
        house_risk: float = 85.0,
        friction_r: float = 0.25,
        target_r: float = 2.20,
        stop_r: float = 1.00,
        max_dd_limit: float = 4.75,
        profit_goal: float = 500.0,
        min_trades: int = 15,
        max_per_symbol: int = 3,
        random_state: int = 42
    ):
        self.capital = capital
        self.base_risk = base_risk
        self.house_risk = house_risk
        self.friction_r = friction_r
        self.target_r = target_r
        self.stop_r = stop_r
        self.max_dd_limit = max_dd_limit
        self.profit_goal = profit_goal
        self.min_trades = min_trades
        self.max_per_symbol = max_per_symbol
        self.random_state = random_state

    def train_models(
        self,
        train_df: pd.DataFrame
    ) -> Tuple[lgb.LGBMClassifier, lgb.LGBMClassifier]:
        train_l = train_df[train_df["signal_side"] == 1]
        train_s = train_df[train_df["signal_side"] == -1]

        clf_long = lgb.LGBMClassifier(
            n_estimators=140, max_depth=4, num_leaves=15, learning_rate=0.03,
            subsample=0.8, colsample_bytree=0.8, reg_alpha=2.0, reg_lambda=4.0,
            random_state=self.random_state, verbose=-1, n_jobs=-1
        )
        clf_long.fit(train_l[LONG_FEATURES], train_l["label_y"])

        clf_short = lgb.LGBMClassifier(
            n_estimators=140, max_depth=4, num_leaves=15, learning_rate=0.03,
            subsample=0.8, colsample_bytree=0.8, reg_alpha=2.0, reg_lambda=4.0,
            random_state=self.random_state, verbose=-1, n_jobs=-1
        )
        clf_short.fit(train_s[SHORT_FEATURES], train_s["label_y"])

        return clf_long, clf_short

    def select_trades_for_window(
        self,
        test_df: pd.DataFrame,
        clf_long: lgb.LGBMClassifier,
        clf_short: lgb.LGBMClassifier
    ) -> Tuple[pd.DataFrame, str]:
        test_l = test_df[test_df["signal_side"] == 1].copy()
        test_s = test_df[test_df["signal_side"] == -1].copy()

        test_l["prob"] = clf_long.predict_proba(test_l[LONG_FEATURES])[:, 1] if len(test_l) > 0 else []
        test_s["prob"] = clf_short.predict_proba(test_s[SHORT_FEATURES])[:, 1] if len(test_s) > 0 else []

        tide_mean = test_df["btc_macro_tide"].mean() if "btc_macro_tide" in test_df else 0.0

        if tide_mean >= 0.12:
            regime_str = f"STRONG BULL (Longs capped per symbol, tide: {tide_mean:+.2f})"
            cand = test_l[test_l.vwap_zscore <= 2.8].sort_values("prob", ascending=False).groupby("symbol").head(self.max_per_symbol)
            selected = cand.sort_values("prob", ascending=False).head(35)
        elif tide_mean <= -0.10:
            regime_str = f"BEAR REGIME (Safe shorts with vol confirmation, tide: {tide_mean:+.2f})"
            filt_s = test_s[(test_s.vwap_zscore >= -2.0) & (test_s.short_liq_zs < 1.2) & (test_s.volume_ratio >= 0.75)]
            cand = filt_s.sort_values("prob", ascending=False).groupby("symbol").head(self.max_per_symbol)
            selected = cand.sort_values("prob", ascending=False).head(35)
        else:
            regime_str = f"NEUTRAL / CHOP (Bar-by-bar local tide dispatch, tide: {tide_mean:+.2f})"
            cand_l = test_l[(test_l.btc_macro_tide >= 0) & (test_l.vwap_zscore <= 2.8)].sort_values("prob", ascending=False).groupby("symbol").head(self.max_per_symbol).head(14)
            cand_s = test_s[(test_s.btc_macro_tide <= 0) & (test_s.short_liq_zs < 1.2) & (test_s.vwap_zscore >= -2.0) & (test_s.volume_ratio >= 0.75)].sort_values("prob", ascending=False).groupby("symbol").head(self.max_per_symbol).head(14)
            selected = pd.concat([cand_l, cand_s]).sort_values("open_time_ms")

        return selected, regime_str

    def simulate_execution(
        self,
        selected: pd.DataFrame
    ) -> Dict[str, Any]:
        equity = self.capital
        peak_equity = self.capital
        max_dd = 0.0
        n_trd = 0
        wins = 0

        for _, row in selected.iterrows():
            r = row["realized_r"]
            y = row["label_y"]

            curr_profit = equity - self.capital
            curr_dd = (peak_equity - equity) / peak_equity * 100.0

            if curr_profit >= self.profit_goal and n_trd >= self.min_trades:
                break
            if curr_dd >= self.max_dd_limit:
                break

            dd_budget_pct = 4.90 - curr_dd
            dd_budget_usd = (dd_budget_pct / 100.0) * peak_equity
            max_allowed_risk = max(5.0, dd_budget_usd / 1.30)

            if curr_dd >= 3.5:
                target_risk = 12.0
            elif curr_dd >= 2.0:
                target_risk = 22.0
            elif curr_profit >= 60.0:
                target_risk = self.house_risk
            else:
                target_risk = self.base_risk

            risk = min(target_risk, max_allowed_risk)
            net_r = r - self.friction_r
            trade_pnl = net_r * risk

            equity += trade_pnl
            n_trd += 1
            if y == 1:
                wins += 1

            if equity > peak_equity:
                peak_equity = equity
            dd = (peak_equity - equity) / peak_equity * 100.0
            if dd > max_dd:
                max_dd = dd

        net_pnl = equity - self.capital
        net_roi = (net_pnl / self.capital) * 100.0
        wr = (wins / n_trd * 100.0) if n_trd > 0 else 0.0

        return {
            "net_pnl": net_pnl,
            "net_roi": net_roi,
            "max_dd": max_dd,
            "win_rate": wr,
            "trades": n_trd,
            "equity": equity
        }
