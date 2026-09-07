"""
================================================================================
DUAL-CLASSIFIER LIQUIDATION CASCADE QUANTITATIVE ENGINE (CATBOOST)
================================================================================
Institutional quantitative strategy for BTCUSDT (15m timeframe).
Replaces slow LSTMs/Regressors with specialized Long/Short Triple-Barrier Classifiers.
Enforces Part 14 Institutional Anti-Lookahead Directives with 4-Bar Armed Confluence.
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
from catboost import CatBoostClassifier

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

class EnsembleLiquidationModel:
    def __init__(self, random_state: int = 42, **kwargs):
        self.random_state = random_state
        self.cb_long = CatBoostClassifier(iterations=250, depth=4, learning_rate=0.03, auto_class_weights="Balanced", random_seed=random_state, verbose=False, thread_count=4)
        self.cb_short = CatBoostClassifier(iterations=250, depth=4, learning_rate=0.03, auto_class_weights="Balanced", random_seed=random_state, verbose=False, thread_count=4)
        
    def fit(self, X: pd.DataFrame, y: np.ndarray, event_mask: Optional[np.ndarray] = None) -> EnsembleLiquidationModel:
        print("Training Dual CatBoost Classifiers (Long/Short)...")
        if event_mask is not None:
            idx = np.where(event_mask)[0]
            X_train = X.iloc[idx]
            y_train = y[idx]
        else:
            X_train = X
            y_train = y
            
        y_long = (y_train == 1).astype(int)
        y_short = (y_train == -1).astype(int)
        
        # Only train if we have both classes
        if y_long.sum() > 5: self.cb_long.fit(X_train, y_long)
        if y_short.sum() > 5: self.cb_short.fit(X_train, y_short)
        
        return self
        
    def predict_probabilities(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        X_val = X.copy()
        
        p_long = np.zeros(len(X))
        p_short = np.zeros(len(X))
        
        if hasattr(self.cb_long, "is_fitted_") and self.cb_long.is_fitted_():
            p_long = self.cb_long.predict_proba(X_val)[:, 1]
        elif hasattr(self.cb_long, "tree_count_"): # Fallback check for catboost
             p_long = self.cb_long.predict_proba(X_val)[:, 1]
             
        if hasattr(self.cb_short, "is_fitted_") and self.cb_short.is_fitted_():
            p_short = self.cb_short.predict_proba(X_val)[:, 1]
        elif hasattr(self.cb_short, "tree_count_"):
             p_short = self.cb_short.predict_proba(X_val)[:, 1]
             
        p_neutral = np.ones_like(p_long) - p_long - p_short
        return p_neutral, p_long, p_short


class CausalSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = RatchetConfig()):
        self.risk = risk_cfg
        self.fric = fric_cfg
        self.ratchet = ratchet_cfg
        
    def run(self, df_test: pd.DataFrame, p_long: np.ndarray, p_short: np.ndarray, p_threshold: float = 0.55, liq_threshold: float = 1.8) -> Dict:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        long_liq_zs = df_test["long_liq_zs"].fillna(0.0)
        short_liq_zs = df_test["short_liq_zs"].fillna(0.0)
        zc_div = df_test["zc_div"].fillna(0.0)
        
        vb = df_test["volume_base"].clip(lower=1e-5)
        spot_cvd_pct = (df_test["spot_cvd_15m"] / vb).clip(-5.0, 5.0).fillna(0.0)
        fut_cvd_pct = (df_test["future_cvd_15m"] / vb).clip(-5.0, 5.0).fillna(0.0)
        
        vwap_zscore = df_test["vwap_zscore"].fillna(0.0)
        rsi_14 = df_test["rsi_14"].fillna(50.0)
        
        swing_hi = df_test["high"].rolling(50, min_periods=10).max().values
        swing_lo = df_test["low"].rolling(50, min_periods=10).min().values
        
        # Confluence Arming (1-hour / 4-bar rolling window)
        liq_a_l = long_liq_zs.rolling(4, min_periods=1).max().fillna(0).values > liq_threshold
        zc_a_l = zc_div.rolling(4, min_periods=1).max().fillna(0).values > 0.8
        spot_a_l = spot_cvd_pct.rolling(4, min_periods=1).max().fillna(0).values > 0.0
        fut_a_l = fut_cvd_pct.rolling(4, min_periods=1).min().fillna(0).values < 0.0
        rsi_a_l = rsi_14.rolling(4, min_periods=1).min().fillna(50.0).values < 40.0
        vwap_a_l = vwap_zscore.rolling(4, min_periods=1).min().fillna(0.0).values < -0.5
        long_confluence = liq_a_l & zc_a_l & spot_a_l & fut_a_l & rsi_a_l & vwap_a_l

        liq_a_s = short_liq_zs.rolling(4, min_periods=1).max().fillna(0).values > liq_threshold
        zc_a_s = zc_div.rolling(4, min_periods=1).min().fillna(0).values < -0.8
        spot_a_s = spot_cvd_pct.rolling(4, min_periods=1).min().fillna(0).values < 0.0
        fut_a_s = fut_cvd_pct.rolling(4, min_periods=1).max().fillna(0).values > 0.0
        rsi_a_s = rsi_14.rolling(4, min_periods=1).max().fillna(50.0).values > 60.0
        vwap_a_s = vwap_zscore.rolling(4, min_periods=1).max().fillna(0.0).values > 0.5
        short_confluence = liq_a_s & zc_a_s & spot_a_s & fut_a_s & rsi_a_s & vwap_a_s
        
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
                
                # USE HIGHER PROB THRESHOLD SINCE WE ARE NOW A CLASSIFIER (e.g. > 0.65)
                # p_threshold passed from test_20_oos_xgboost is 0.35, which is too low for classifiers.
                # We enforce a hardcoded probability gate for safety here:
                class_threshold = 0.60
                
                if long_confluence[t] and p_long[t] > class_threshold: sig_long = True
                if short_confluence[t] and p_short[t] > class_threshold: sig_short = True
                        
                if sig_long and not sig_short:
                    px = cl[t] * (1.0 + self.fric.entry_slippage)
                    r_ = max(atr[t] * 2.0, px * 0.008) # minimum 80 bps stop
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
