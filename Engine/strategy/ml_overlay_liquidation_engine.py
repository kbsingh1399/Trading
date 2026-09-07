"""
================================================================================
INSTITUTIONAL SMC PLAYBOOK & ML OVERLAY CLASSIFIER (XGBOOST)
================================================================================
Implements the Trader Mayne Playbook with an Asymmetric ML Overlay Classifier.
Enforces Part 14 Institutional Anti-Lookahead Directives.
================================================================================
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from xgboost import XGBClassifier

@dataclass(frozen=True)
class RiskConfig:
    initial_capital: float = 5000.0
    base_risk: float = 25.0
    house_money_risk: float = 50.0
    drawdown_defense_risk: float = 15.0
    drawdown_limit: float = 0.045

@dataclass(frozen=True)
class FrictionConfig:
    taker_fee: float = 0.0008
    entry_slippage: float = 0.0010
    exit_slippage: float = 0.0015

@dataclass(frozen=True)
class RatchetConfig:
    arm0_r: float = 0.8
    lock0_r: float = 0.15
    arm1_r: float = 1.5
    lock1_r: float = 0.80
    min_target_r: float = 2.5
    time_decay_bars: int = 24
    time_decay_r: float = 0.20


class MLOverlayFeatureExtractor:
    @staticmethod
    def extract_at_indices(df: pd.DataFrame, indices: np.ndarray) -> pd.DataFrame:
        """Extracts stationary features specifically at trade entry candidate indices."""
        f = pd.DataFrame(index=indices)
        
        # We assume indices are valid bounds
        f["rsi_14"] = df["rsi_14"].iloc[indices].values
        f["vwap_zscore"] = df["vwap_zscore"].iloc[indices].values
        
        # Using 4-bar rolling max for liquidations as per architecture
        long_liq_roll = df["long_liq_zs"].rolling(4, min_periods=1).max().fillna(0.0)
        short_liq_roll = df["short_liq_zs"].rolling(4, min_periods=1).max().fillna(0.0)
        
        f["long_liq_roll"] = long_liq_roll.iloc[indices].values
        f["short_liq_roll"] = short_liq_roll.iloc[indices].values
        
        f["zc_div"] = df["zc_div"].iloc[indices].values
        
        vb = df["volume_base"].clip(lower=1e-5)
        spot_cvd_pct = (df["spot_cvd_15m"] / vb).clip(-5.0, 5.0).fillna(0.0)
        fut_cvd_pct = (df["future_cvd_15m"] / vb).clip(-5.0, 5.0).fillna(0.0)
        
        f["delta_spot"] = spot_cvd_pct.iloc[indices].values
        f["delta_fut"] = fut_cvd_pct.iloc[indices].values
        
        vol_sma20 = df["volume_base"].rolling(20, min_periods=1).mean().clip(lower=1e-5)
        f["volume_ratio"] = (df["volume_base"] / vol_sma20).iloc[indices].values
        
        f["ls_ratio_global"] = df["ls_ratio_global"].iloc[indices].fillna(1.0).values
        
        c = df["close"].iloc[indices].values
        atr = df["atr_14"].iloc[indices].clip(lower=c * 0.002).values
        f["atr_pct"] = (atr / c) * 100.0
        
        ema_50 = df["close"].ewm(span=50, adjust=False).mean()
        ema_200 = df["close"].ewm(span=200, adjust=False).mean()
        f["trend_50_200"] = (ema_50 / ema_200).iloc[indices].values
        f["roc_10"] = df["close"].pct_change(10).fillna(0.0).iloc[indices].values * 100.0
        f["dist_ema200"] = (df["close"] / ema_200).iloc[indices].values
        
        return f


from sklearn.ensemble import RandomForestClassifier, VotingClassifier

class MLOverlayClassifier:
    def __init__(self, random_state: int = 42):
        # Strictly enforced regularization & anti-overfitting parameters
        xgb_model = XGBClassifier(
            max_depth=4,
            reg_alpha=1.0,
            reg_lambda=3.0,
            subsample=0.8,
            colsample_bytree=0.8,
            learning_rate=0.05,
            n_estimators=100,
            eval_metric="logloss",
            random_state=random_state,
            n_jobs=2
        )
        
        rf_model = RandomForestClassifier(
            max_depth=4,
            n_estimators=100,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=2
        )
        
        self.model = VotingClassifier(
            estimators=[('xgb', xgb_model), ('rf', rf_model)],
            voting='soft'
        )
        self.is_fitted = False
        
    def fit(self, X: pd.DataFrame, y: np.ndarray):
        if len(y) >= 3 and np.sum(y) >= 1 and np.sum(y == 0) >= 1:
            # Dynamically calculate scale_pos_weight for XGBoost
            pos_count = np.sum(y)
            neg_count = len(y) - pos_count
            scale_weight = float(neg_count) / pos_count if pos_count > 0 else 1.0
            self.model.estimators[0][1].set_params(scale_pos_weight=scale_weight)
            
            self.model.fit(X, y)
            self.is_fitted = True
        else:
            print(f"Warning: ML Overlay could not fit. Insufficient classes (Total: {len(y)}, Pos: {np.sum(y)}).")
            self.is_fitted = False
            
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or len(X) == 0:
            return np.ones(len(X)) # Fallback to 1.0 probability if un-fitted
        return self.model.predict_proba(X)[:, 1]


class CausalSMCMLSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = RatchetConfig()):
        self.risk = risk_cfg
        self.fric = fric_cfg
        self.ratchet = ratchet_cfg
        self.ml_classifier = MLOverlayClassifier()
        
    def generate_candidate_signals(self, df: pd.DataFrame, liq_threshold: float = 1.8) -> Tuple[np.ndarray, np.ndarray]:
        """Trader Mayne Playbook core logic."""
        long_liq_zs = df["long_liq_zs"].fillna(0.0)
        short_liq_zs = df["short_liq_zs"].fillna(0.0)
        zc_div = df["zc_div"].fillna(0.0)
        
        vb = df["volume_base"].clip(lower=1e-5)
        spot_cvd_pct = (df["spot_cvd_15m"] / vb).clip(-5.0, 5.0).fillna(0.0)
        fut_cvd_pct = (df["future_cvd_15m"] / vb).clip(-5.0, 5.0).fillna(0.0)
        
        rsi_14 = df["rsi_14"].fillna(50.0)
        vwap_zscore = df["vwap_zscore"].fillna(0.0)
        
        liq_a_l = long_liq_zs.rolling(4, min_periods=1).max().fillna(0).values > liq_threshold
        zc_a_l = zc_div.rolling(4, min_periods=1).max().fillna(0).values > 0.8
        spot_a_l = spot_cvd_pct.rolling(4, min_periods=1).max().fillna(0).values > 0.0
        fut_a_l = fut_cvd_pct.rolling(4, min_periods=1).min().fillna(0).values < 0.0
        rsi_a_l = rsi_14.rolling(4, min_periods=1).min().fillna(50.0).values < 40.0
        vwap_a_l = vwap_zscore.rolling(4, min_periods=1).min().fillna(0.0).values < -0.5
        
        sig_long = liq_a_l & zc_a_l & spot_a_l & fut_a_l & rsi_a_l & vwap_a_l

        liq_a_s = short_liq_zs.rolling(4, min_periods=1).max().fillna(0).values > liq_threshold
        zc_a_s = zc_div.rolling(4, min_periods=1).min().fillna(0).values < -0.8
        spot_a_s = spot_cvd_pct.rolling(4, min_periods=1).min().fillna(0).values < 0.0
        fut_a_s = fut_cvd_pct.rolling(4, min_periods=1).max().fillna(0).values > 0.0
        rsi_a_s = rsi_14.rolling(4, min_periods=1).max().fillna(50.0).values > 60.0
        vwap_a_s = vwap_zscore.rolling(4, min_periods=1).max().fillna(0.0).values > 0.5
        
        sig_short = liq_a_s & zc_a_s & spot_a_s & fut_a_s & rsi_a_s & vwap_a_s
        
        return sig_long, sig_short

    def simulate_trade_outcomes(self, df: pd.DataFrame, entry_indices: np.ndarray, sides: np.ndarray) -> np.ndarray:
        """Simulate trades for the training set to label y=1 if R >= 1.0 before SL."""
        y = np.zeros(len(entry_indices), dtype=np.int32)
        hi = df["high"].values
        lo = df["low"].values
        op = df["open"].values
        cl = df["close"].values
        atr_arr = df["atr_14"].clip(lower=df["close"] * 0.002).values
        
        swing_hi = df["high"].rolling(50, min_periods=10).max().values
        swing_lo = df["low"].rolling(50, min_periods=10).min().values
        
        T = len(df)
        
        for k, (i, side) in enumerate(zip(entry_indices, sides)):
            px = cl[i]
            r_ = max(atr_arr[i] * 2.0, px * 0.008)
            
            if side == 1:
                pos_stop = px * (1.0 + self.fric.entry_slippage) - r_
                pos_entry = px * (1.0 + self.fric.entry_slippage)
                r_dist = r_
            else:
                pos_stop = px * (1.0 - self.fric.entry_slippage) + r_
                pos_entry = px * (1.0 - self.fric.entry_slippage)
                r_dist = r_
                
            hit_target = False
            hit_stop = False
            
            # Simulate forward
            for j in range(i+1, min(i + self.ratchet.time_decay_bars, T)):
                o_, h_, l_ = op[j], hi[j], lo[j]
                if side == 1:
                    if l_ <= pos_stop: hit_stop = True; break
                    if (h_ - pos_entry) / r_dist >= 2.0: hit_target = True; break
                else:
                    if h_ >= pos_stop: hit_stop = True; break
                    if (pos_entry - l_) / r_dist >= 2.0: hit_target = True; break
            
            if hit_target:
                y[k] = 1
                
        return y
        
    def train_overlay(self, df_train: pd.DataFrame, liq_threshold: float = 1.8):
        """Train the ML overlay on candidate signals from the causal training partition."""
        sig_long, sig_short = self.generate_candidate_signals(df_train, liq_threshold)
        
        # Consolidate candidates
        long_indices = np.where(sig_long & ~sig_short)[0]
        short_indices = np.where(sig_short & ~sig_long)[0]
        
        all_indices = np.concatenate([long_indices, short_indices])
        all_sides = np.concatenate([np.ones(len(long_indices)), -np.ones(len(short_indices))])
        
        if len(all_indices) == 0:
            print("No training candidates found.")
            return
            
        # Sort chronologically
        sort_idx = np.argsort(all_indices)
        all_indices = all_indices[sort_idx]
        all_sides = all_sides[sort_idx]
        
        # Simulate outcomes for labels
        y_train = self.simulate_trade_outcomes(df_train, all_indices, all_sides)
        
        # Extract features
        X_train = MLOverlayFeatureExtractor.extract_at_indices(df_train, all_indices)
        
        print(f"Overlay training samples: {len(y_train)} (Positive: {np.sum(y_train)})")
        self.ml_classifier.fit(X_train, y_train)
        
    def run(self, df_test: pd.DataFrame, ml_threshold: float = 0.50, liq_threshold: float = 1.8) -> Dict:
        """Run the walk-forward simulation using base signals filtered by the ML overlay."""
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        swing_hi = df_test["high"].rolling(50, min_periods=10).max().values
        swing_lo = df_test["low"].rolling(50, min_periods=10).min().values
        
        sig_long, sig_short = self.generate_candidate_signals(df_test, liq_threshold)
        
        realized = self.risk.initial_capital
        peak = realized
        pos_side = 0; pos_entry = 0.0; pos_stop = 0.0; pos_target = 0.0; pos_qty = 0.0
        pos_rr = 0.0; pos_risk = 0.0; pos_bar = 0; pos_max_r = 0.0
        
        trades: List[Dict] = []
        equity_curve = np.full(T, realized)

        for t in range(self.ratchet.time_decay_bars, T):
            if pos_side != 0:
                o_, h_, l_, c_ = op[t], hi[t], lo[t], cl[t]
                exit_px = 0.0; exit_reason = ""
                
                if pos_side == 1:
                    if o_ <= pos_stop: exit_px = o_ * (1.0 - self.fric.exit_slippage); exit_reason = "STOP_OPEN"
                    elif o_ >= pos_target: exit_px = o_; exit_reason = "TARGET_OPEN"
                    elif l_ <= pos_stop: exit_px = pos_stop * (1.0 - self.fric.exit_slippage); exit_reason = "STOP_BAR"
                    elif h_ >= pos_target: exit_px = pos_target; exit_reason = "TARGET_BAR"
                    
                    r_gain = (h_ - pos_entry) / pos_rr
                    if r_gain > pos_max_r: pos_max_r = r_gain
                    if not exit_reason and (t - pos_bar) >= self.ratchet.time_decay_bars and pos_max_r < self.ratchet.time_decay_r:
                        exit_px = c_ * (1.0 - self.fric.exit_slippage); exit_reason = "TIME_DECAY"
                        
                elif pos_side == -1:
                    if o_ >= pos_stop: exit_px = o_ * (1.0 + self.fric.exit_slippage); exit_reason = "STOP_OPEN"
                    elif o_ <= pos_target: exit_px = o_; exit_reason = "TARGET_OPEN"
                    elif h_ >= pos_stop: exit_px = pos_stop * (1.0 + self.fric.exit_slippage); exit_reason = "STOP_BAR"
                    elif l_ <= pos_target: exit_px = pos_target; exit_reason = "TARGET_BAR"
                    
                    r_gain = (pos_entry - l_) / pos_rr
                    if r_gain > pos_max_r: pos_max_r = r_gain
                    if not exit_reason and (t - pos_bar) >= self.ratchet.time_decay_bars and pos_max_r < self.ratchet.time_decay_r:
                        exit_px = c_ * (1.0 + self.fric.exit_slippage); exit_reason = "TIME_DECAY"
                        
                if exit_reason:
                    gross = pos_qty * (exit_px - pos_entry) if pos_side == 1 else pos_qty * (pos_entry - exit_px)
                    fees = pos_qty * (pos_entry + exit_px) * self.fric.taker_fee
                    net_pnl = gross - fees
                    realized += net_pnl
                    trades.append({
                        "entry_bar": pos_bar, "exit_bar": t, "side": "LONG" if pos_side == 1 else "SHORT",
                        "entry": pos_entry, "exit": exit_px, "pnl": net_pnl,
                        "r": net_pnl / pos_risk if pos_risk > 0 else 0.0, "reason": exit_reason
                    })
                    pos_side = 0
                else:
                    if pos_side == 1:
                        if pos_max_r >= self.ratchet.arm1_r: pos_stop = max(pos_stop, pos_entry + self.ratchet.lock1_r * pos_rr)
                        elif pos_max_r >= self.ratchet.arm0_r: pos_stop = max(pos_stop, pos_entry + self.ratchet.lock0_r * pos_rr)
                    elif pos_side == -1:
                        if pos_max_r >= self.ratchet.arm1_r: pos_stop = min(pos_stop, pos_entry - self.ratchet.lock1_r * pos_rr)
                        elif pos_max_r >= self.ratchet.arm0_r: pos_stop = min(pos_stop, pos_entry - self.ratchet.lock0_r * pos_rr)

            unreal = 0.0
            if pos_side == 1: unreal = pos_qty * (cl[t] - pos_entry)
            elif pos_side == -1: unreal = pos_qty * (pos_entry - cl[t])
            equity = realized + unreal
            if equity > peak: peak = equity
            equity_curve[t] = equity
            
            if pos_side == 0 and t < T - 1:
                net_profit = realized - self.risk.initial_capital
                current_dd = (peak - equity) / peak if peak > 0 else 0.0
                
                if current_dd >= self.risk.drawdown_limit: continue
                elif current_dd > 0.025: trade_risk = self.risk.drawdown_defense_risk
                elif net_profit > 50.0: trade_risk = self.risk.house_money_risk
                else: trade_risk = self.risk.base_risk
                    
                is_long_cand = sig_long[t] and not sig_short[t]
                is_short_cand = sig_short[t] and not sig_long[t]
                
                if is_long_cand or is_short_cand:
                    # ML Overlay Prediction
                    idx_arr = np.array([t])
                    X_cand = MLOverlayFeatureExtractor.extract_at_indices(df_test, idx_arr)
                    p_success = self.ml_classifier.predict_proba(X_cand)[0]
                    
                    if p_success >= ml_threshold:
                        if is_long_cand:
                            px = cl[t] * (1.0 + self.fric.entry_slippage)
                            r_ = max(atr[t] * 2.0, px * 0.008)
                            tp_dist = self.ratchet.min_target_r * r_
                            pos_side = 1; pos_entry = px; pos_stop = px - r_; pos_target = px + tp_dist
                            pos_rr = r_; pos_risk = trade_risk; pos_qty = trade_risk / r_; pos_bar = t; pos_max_r = 0.0
                        elif is_short_cand:
                            px = cl[t] * (1.0 - self.fric.entry_slippage)
                            r_ = max(atr[t] * 2.0, px * 0.008)
                            tp_dist = self.ratchet.min_target_r * r_
                            pos_side = -1; pos_entry = px; pos_stop = px + r_; pos_target = px - tp_dist
                            pos_rr = r_; pos_risk = trade_risk; pos_qty = trade_risk / r_; pos_bar = t; pos_max_r = 0.0

        tot = len(trades)
        wins = [tr for tr in trades if tr["pnl"] > 0]
        wr = len(wins) / tot * 100.0 if tot > 0 else 0.0
        net_pnl = realized - self.risk.initial_capital
        roi = net_pnl / self.risk.initial_capital * 100.0
        peaks = np.maximum.accumulate(equity_curve)
        with np.errstate(divide='ignore', invalid='ignore'):
            dds = np.where(peaks > 0, (peaks - equity_curve) / peaks * 100.0, 0.0)
        max_dd = np.max(dds) if len(dds) > 0 else 0.0
        
        return {
            "roi_pct": roi, "max_dd_pct": max_dd, "win_rate_pct": wr,
            "trades": tot, "net_pnl": net_pnl, "equity_final": realized, "trades_list": trades
        }
