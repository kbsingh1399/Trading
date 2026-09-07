"""
================================================================================
S1: LIQUIDATION CASCADE (ML-DRIVEN INSTITUTIONAL QUANT ARCHITECTURE)
================================================================================
Implements the exact invariants specified in ACTIVE_CONTEXT.md and AGENTS.md.
ML overlays are applied strictly out-of-sample on pure liquidation cascades.
================================================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Callable, List
from dataclasses import dataclass

@dataclass(frozen=True)
class RiskConfig:
    initial_capital: float = 5000.0
    base_risk: float = 25.0              # 0.50% base risk
    house_money_risk: float = 50.0       # 1.00% max 2x risk
    drawdown_defense_risk: float = 15.0  # 0.30% risk
    drawdown_limit: float = 0.045        # 4.5% ($225) hard drawdown stop

@dataclass(frozen=True)
class FrictionConfig:
    taker_fee: float = 0.0008            # 8 bps
    entry_slippage: float = 0.0010       # 10 bps
    exit_slippage: float = 0.0015        # 15 bps

@dataclass(frozen=True)
class RatchetConfig:
    arm0_r: float = 0.8
    lock0_r: float = 0.15
    arm1_r: float = 1.5
    lock1_r: float = 0.8
    min_target_r: float = 2.5
    time_decay_bars: int = 24
    time_decay_r: float = 0.20

class LiquidationCascadeSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = RatchetConfig()):
        self.risk = risk_cfg
        self.fric = fric_cfg
        self.ratchet = ratchet_cfg

    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> Dict:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        # Extract ML Alpha Invariants
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        delta_spot = df_test.get("delta_spot", pd.Series(np.zeros(T))).values
        delta_fut = df_test.get("delta_fut", pd.Series(np.zeros(T))).values
        rsi = df_test.get("rsi_14", pd.Series(np.full(T, 50.0))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        
        realized = self.risk.initial_capital
        peak = realized
        pos_side = 0
        pos_entry = 0.0
        pos_stop = 0.0
        pos_target = 0.0
        pos_qty = 0.0
        pos_risk = 0.0
        pos_bar = 0
        pos_max_r = 0.0
        pos_rr = 1.0
        
        # Removed SMC state tracking
        
        trades: List[Dict] = []
        equity_curve = np.full(T, realized)

        for t in range(self.ratchet.time_decay_bars, T):
            if pos_side != 0:
                o_, h_, l_, c_ = op[t], hi[t], lo[t], cl[t]
                exit_px = 0.0
                exit_reason = ""
                
                if pos_side == 1:
                    if o_ <= pos_stop: exit_px = o_ * (1.0 - self.fric.exit_slippage); exit_reason = "STOP_OPEN"
                    elif o_ >= pos_target: exit_px = o_; exit_reason = "TARGET_OPEN"
                    elif l_ <= pos_stop: exit_px = pos_stop * (1.0 - self.fric.exit_slippage); exit_reason = "STOP_BAR"
                    elif h_ >= pos_target: exit_px = pos_target; exit_reason = "TARGET_BAR"
                        
                elif pos_side == -1:
                    if o_ >= pos_stop: exit_px = o_ * (1.0 + self.fric.exit_slippage); exit_reason = "STOP_OPEN"
                    elif o_ <= pos_target: exit_px = o_; exit_reason = "TARGET_OPEN"
                    elif h_ >= pos_stop: exit_px = pos_stop * (1.0 + self.fric.exit_slippage); exit_reason = "STOP_BAR"
                    elif l_ <= pos_target: exit_px = pos_target; exit_reason = "TARGET_BAR"
                        
                # Microstructure Ratchet
                if exit_reason:
                    gross = pos_qty * (exit_px - pos_entry) if pos_side == 1 else pos_qty * (pos_entry - exit_px)
                    fees = pos_qty * (pos_entry + exit_px) * self.fric.taker_fee
                    net_pnl = gross - fees
                    realized += net_pnl
                    trades.append({
                        "entry_bar": pos_bar, "exit_bar": t,
                        "side": "LONG" if pos_side == 1 else "SHORT",
                        "entry": pos_entry, "exit": exit_px, "pnl": net_pnl,
                        "r": net_pnl / pos_risk if pos_risk > 0 else 0.0,
                        "max_r": pos_max_r,
                        "reason": exit_reason
                    })
                    pos_side = 0
                else:
                    r_gain = (hi[t] - pos_entry) / pos_rr if pos_side == 1 else (pos_entry - lo[t]) / pos_rr
                    if r_gain > pos_max_r: pos_max_r = r_gain
                    if pos_side == 1:
                        if pos_max_r >= self.ratchet.arm1_r:
                            pos_stop = max(pos_stop, pos_entry + self.ratchet.lock1_r * pos_rr)
                        elif pos_max_r >= self.ratchet.arm0_r:
                            pos_stop = max(pos_stop, pos_entry + self.ratchet.lock0_r * pos_rr)
                    elif pos_side == -1:
                        if pos_max_r >= self.ratchet.arm1_r:
                            pos_stop = min(pos_stop, pos_entry - self.ratchet.lock1_r * pos_rr)
                        elif pos_max_r >= self.ratchet.arm0_r:
                            pos_stop = min(pos_stop, pos_entry - self.ratchet.lock0_r * pos_rr)
                    
                    if (t - pos_bar) >= self.ratchet.time_decay_bars and pos_max_r < self.ratchet.time_decay_r: # time decay
                        pos_side = 0 # market exit
                        gross = pos_qty * (cl[t] - pos_entry) if pos_side == 1 else pos_qty * (pos_entry - cl[t])
                        fees = pos_qty * (pos_entry + cl[t]) * self.fric.taker_fee
                        net_pnl = gross - fees
                        realized += net_pnl
                        trades.append({
                            "entry_bar": pos_bar, "exit_bar": t,
                            "side": "LONG" if pos_side == 1 else "SHORT",
                            "entry": pos_entry, "exit": cl[t], "pnl": net_pnl,
                            "r": net_pnl / pos_risk if pos_risk > 0 else 0.0,
                            "max_r": pos_max_r,
                            "reason": "TIME_DECAY"
                        })
            
            unreal = 0.0
            if pos_side == 1: unreal = pos_qty * (cl[t] - pos_entry)
            elif pos_side == -1: unreal = pos_qty * (pos_entry - cl[t])
            equity = realized + unreal
            if equity > peak: peak = equity
            equity_curve[t] = equity
            
            if pos_side == 0 and t < T - 1:
                net_profit = realized - self.risk.initial_capital
                current_dd = (peak - equity) / peak if peak > 0 else 0.0
                
                if not training_mode and current_dd >= self.risk.drawdown_limit:
                    continue
                
                # Institutional Risk Sizing Logic
                if net_profit > 50.0:
                    trade_risk = min(self.risk.house_money_risk, equity * 0.01)
                elif current_dd > 0.025:
                    trade_risk = self.risk.drawdown_defense_risk
                else:
                    trade_risk = self.risk.base_risk
                    
                # Base Trigger for Liquidations
                sig_long = False
                sig_short = False
                
                # Enforce Canonical Confluence Signal (Z >= 1.2 per AGENTS.md)
                # Event-conditioned sampling: We relax hard constraints to allow the ML model to learn confluence.
                sig_long = (long_liq_zs[t] > 1.2) and (cl[t] > op[t])
                sig_short = (short_liq_zs[t] > 1.2) and (cl[t] < op[t])
                    
                # Filter using the XGBoost Model function if provided
                if filter_func is not None:
                    if sig_long and not filter_func(t, 'LONG'): sig_long = False
                    if sig_short and not filter_func(t, 'SHORT'): sig_short = False

                if sig_long:
                    px = cl[t] * (1.0 + self.fric.entry_slippage)
                    # Structural Stop Loss: 3.0x ATR below entry
                    stop_px = px - (atr[t] * 3.0)
                    r_ = px - stop_px
                    if r_ <= 0: r_ = px * 0.005 # Fallback
                    target_px = px + (r_ * self.ratchet.min_target_r)
                    
                    pos_side = 1; pos_entry = px; pos_stop = stop_px
                    pos_target = target_px
                    pos_risk = trade_risk; pos_qty = trade_risk / r_; pos_bar = t; pos_max_r = 0.0; pos_rr = r_
                    
                elif sig_short:
                    px = cl[t] * (1.0 - self.fric.entry_slippage)
                    # Structural Stop Loss: 3.0x ATR above entry
                    stop_px = px + (atr[t] * 3.0)
                    r_ = stop_px - px
                    if r_ <= 0: r_ = px * 0.005 # Fallback
                    target_px = px - (r_ * self.ratchet.min_target_r)
                    
                    pos_side = -1; pos_entry = px; pos_stop = stop_px
                    pos_target = target_px
                    pos_risk = trade_risk; pos_qty = trade_risk / r_; pos_bar = t; pos_max_r = 0.0; pos_rr = r_

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
            "roi_pct": roi,
            "max_dd_pct": max_dd,
            "win_rate_pct": wr,
            "trades": tot,
            "net_pnl": net_pnl,
            "trades_list": trades
        }
