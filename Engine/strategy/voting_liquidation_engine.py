"""
================================================================================
ENSEMBLE VOTING LIQUIDATION ENGINE
================================================================================
Institutional quantitative strategy for BTCUSDT (15m timeframe).
Uses an ensemble of LightGBM and XGBoost Classifiers.
Removes the ultra-restrictive 6-condition confluence filter that starved the 
previous CatBoost model of trades. Instead, uses a minimal threshold filter 
and delegates decision-making entirely to the ML Voting Ensemble.
================================================================================
"""
from __future__ import annotations

import gc
import json
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import VotingClassifier

@dataclass(frozen=True)
class RiskConfig:
    initial_capital: float = 5000.0
    base_risk: float = 25.0
    house_money_risk: float = 50.0
    drawdown_defense_risk: float = 15.0
    drawdown_limit: float = 0.045
    max_positions: int = 1

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


class FeatureExtractor:
    @staticmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        f = pd.DataFrame(index=df.index)
        c = df["close"]
        atr = df["atr_14"].clip(lower=c * 0.002)
        
        f["long_liq_zs"] = df["long_liq_zs"].fillna(0.0)
        f["short_liq_zs"] = df["short_liq_zs"].fillna(0.0)
        f["liq_imb"] = df["liq_imbalance_ratio"].fillna(0.0)
        
        vb = df["volume_base"].clip(lower=1e-5)
        f["spot_cvd_pct"] = (df["spot_cvd_15m"] / vb).clip(-5.0, 5.0).fillna(0.0)
        f["fut_cvd_pct"] = (df["future_cvd_15m"] / vb).clip(-5.0, 5.0).fillna(0.0)
        f["zc_div_pct"] = (df["zc_div"] / vb).clip(-5.0, 5.0).fillna(0.0)
        
        f["vwap_zs"] = df["vwap_zscore"].clip(-4.0, 4.0).fillna(0.0)
        f["dist_val_atr"] = ((c - df["session_val"]) / atr).clip(-5.0, 5.0).fillna(0.0)
        f["dist_vah_atr"] = ((c - df["session_vah"]) / atr).clip(-5.0, 5.0).fillna(0.0)
        f["dist_vwap_atr"] = ((c - df["session_vwap"]) / atr).clip(-5.0, 5.0).fillna(0.0)
        
        f["rsi_14"] = (df["rsi_14"] - 50.0) / 25.0
        f["dist_ema8_atr"] = ((c - df["ema_8"]) / atr).clip(-4.0, 4.0).fillna(0.0)
        f["dist_ema21_atr"] = ((c - df["ema_21"]) / atr).clip(-4.0, 4.0).fillna(0.0)
        f["dist_ema200_atr"] = ((c - df["ema_200"]) / atr).clip(-8.0, 8.0).fillna(0.0)
        
        f["funding_pct"] = (df["funding_rate_pct"] * 100.0).clip(-5.0, 5.0).fillna(0.0)
        f["basis_pct"] = (df["basis_usd"] / c * 100.0).clip(-5.0, 5.0).fillna(0.0)
        f["oi_change_pct"] = df["oi_change_pct"].clip(-10.0, 10.0).fillna(0.0)
        
        f["ret_1"] = (c.pct_change(1) * 100.0).clip(-10.0, 10.0).fillna(0.0)
        f["ret_4"] = (c.pct_change(4) * 100.0).clip(-15.0, 15.0).fillna(0.0)
        f["atr_pct"] = (atr / c * 100.0).clip(0.1, 10.0).fillna(1.0)
        
        # Add a few interactions
        f["liq_vwap_inter"] = f["long_liq_zs"] * f["vwap_zs"]
        
        return f

class TripleBarrierLabeler:
    @staticmethod
    def label(df: pd.DataFrame, horizon: int = 24, min_tp_r: float = 2.5, sl_r: float = 1.0) -> np.ndarray:
        c = df["close"].values
        hi = df["high"].values
        lo = df["low"].values
        atr = df["atr_14"].clip(lower=c * 0.002).values
        n = len(c)
        labels = np.zeros(n, dtype=np.int32)
        
        for i in range(n - horizon):
            px = c[i]
            r_ = max(atr[i] * 2.0, px * 0.008) # Min 0.8% stop to absorb 33 bps friction
            
            stop_long = px - r_ * sl_r
            tp_long = px + r_ * min_tp_r
            hit_long = 0
            for j in range(i+1, i+horizon):
                if lo[j] <= stop_long: break
                if hi[j] >= tp_long: hit_long = 1; break
                
            stop_short = px + r_ * sl_r
            tp_short = px - r_ * min_tp_r
            hit_short = 0
            for j in range(i+1, i+horizon):
                if hi[j] >= stop_short: break
                if lo[j] <= tp_short: hit_short = 1; break
                
            if hit_long == 1 and hit_short == 0: labels[i] = 1
            elif hit_short == 1 and hit_long == 0: labels[i] = -1
            
        return labels

class VotingLiquidationModel:
    def __init__(self, random_state: int = 42, **kwargs):
        self.random_state = random_state
        
        xgb_l = XGBClassifier(scale_pos_weight=9.0, max_depth=3, learning_rate=0.05, n_estimators=150, subsample=0.8, colsample_bytree=0.8, random_state=random_state, n_jobs=4)
        lgb_l = LGBMClassifier(is_unbalance=True, max_depth=3, learning_rate=0.05, n_estimators=150, subsample=0.8, colsample_bytree=0.8, random_state=random_state, n_jobs=4, verbose=-1)
        
        xgb_s = XGBClassifier(scale_pos_weight=9.0, max_depth=3, learning_rate=0.05, n_estimators=150, subsample=0.8, colsample_bytree=0.8, random_state=random_state, n_jobs=4)
        lgb_s = LGBMClassifier(is_unbalance=True, max_depth=3, learning_rate=0.05, n_estimators=150, subsample=0.8, colsample_bytree=0.8, random_state=random_state, n_jobs=4, verbose=-1)
        
        self.voting_long = VotingClassifier(estimators=[('xgb', xgb_l), ('lgb', lgb_l)], voting='soft')
        self.voting_short = VotingClassifier(estimators=[('xgb', xgb_s), ('lgb', lgb_s)], voting='soft')
        
    def fit(self, X: pd.DataFrame, y: np.ndarray, event_mask: Optional[np.ndarray] = None) -> VotingLiquidationModel:
        print("Training Dual Voting Classifiers (Long/Short)...")
        if event_mask is not None:
            idx = np.where(event_mask)[0]
            X_train = X.iloc[idx]
            y_train = y[idx]
        else:
            X_train = X
            y_train = y
            
        y_long = (y_train == 1).astype(int)
        y_short = (y_train == -1).astype(int)
        
        if y_long.sum() > 10: self.voting_long.fit(X_train, y_long)
        if y_short.sum() > 10: self.voting_short.fit(X_train, y_short)
        
        return self
        
    def predict_probabilities(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        X_val = X.copy()
        
        p_long = np.zeros(len(X))
        p_short = np.zeros(len(X))
        
        if hasattr(self.voting_long, "estimators_"):
            p_long = self.voting_long.predict_proba(X_val)[:, 1]
             
        if hasattr(self.voting_short, "estimators_"):
            p_short = self.voting_short.predict_proba(X_val)[:, 1]
             
        p_neutral = np.ones_like(p_long) - p_long - p_short
        return p_neutral, p_long, p_short


class CausalVotingSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = RatchetConfig()):
        self.risk = risk_cfg
        self.fric = fric_cfg
        self.ratchet = ratchet_cfg
        
    def run(self, df_test: pd.DataFrame, p_long: np.ndarray, p_short: np.ndarray, class_threshold: float = 0.55) -> Dict:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        long_liq_zs = df_test["long_liq_zs"].fillna(0.0).values
        short_liq_zs = df_test["short_liq_zs"].fillna(0.0).values
        vwap_zscore = df_test["vwap_zscore"].fillna(0.0).values
        rsi_14 = df_test["rsi_14"].fillna(50.0).values
        
        swing_hi = df_test["high"].rolling(20, min_periods=5).max().values
        swing_lo = df_test["low"].rolling(20, min_periods=5).min().values
        
        # VERY RELAXED BASE FILTERS - Let ML do the heavy lifting
        # We just want to make sure there's SOME volatility or deviation
        base_filter_long = (long_liq_zs > 0.5) | (vwap_zscore < -0.5) | (rsi_14 < 45)
        base_filter_short = (short_liq_zs > 0.5) | (vwap_zscore > 0.5) | (rsi_14 > 55)
        
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
                    
                sig_long = False
                sig_short = False
                
                if base_filter_long[t] and p_long[t] >= class_threshold: sig_long = True
                if base_filter_short[t] and p_short[t] >= class_threshold: sig_short = True
                        
                if sig_long and not sig_short:
                    px = cl[t] * (1.0 + self.fric.entry_slippage)
                    r_ = max(atr[t] * 2.0, px * 0.008) 
                    tp_dist = max((swing_hi[t] - px), self.ratchet.min_target_r * r_)
                    pos_side = 1; pos_entry = px; pos_stop = px - r_; pos_target = px + tp_dist
                    pos_rr = r_; pos_risk = trade_risk; pos_qty = trade_risk / r_; pos_bar = t; pos_max_r = 0.0
                elif sig_short and not sig_long:
                    px = cl[t] * (1.0 - self.fric.entry_slippage)
                    r_ = max(atr[t] * 2.0, px * 0.008)
                    tp_dist = max((px - swing_lo[t]), self.ratchet.min_target_r * r_)
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
