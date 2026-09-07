import numpy as np
import pandas as pd
from typing import Dict, Callable, List, Optional
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

class ExecutionKernel:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = RatchetConfig()):
        self.risk = risk_cfg
        self.fric = fric_cfg
        self.ratchet = ratchet_cfg

    def run(self, df: pd.DataFrame, signals: pd.DataFrame, training_mode: bool = False) -> Dict:
        """
        Runs the centralized execution engine.
        df: Price data with open, high, low, close.
        signals: DataFrame containing 'side' (1 for LONG, -1 for SHORT, 0 for None),
                 'raw_r' (the un-slippaged risk geometry in price terms).
        """
        T = len(df)
        op = df["open"].values
        hi = df["high"].values
        lo = df["low"].values
        cl = df["close"].values
        
        signal_side = signals["side"].values
        signal_raw_r = signals["raw_r"].values
        
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
        
        trades: List[Dict] = []
        equity_curve = np.full(T, realized)

        for t in range(1, T):
            if pos_side != 0:
                o_, h_, l_, c_ = op[t], hi[t], lo[t], cl[t]
                exit_px = 0.0
                exit_reason = ""
                
                # B5: Stop-first path if OHLC is ambiguous. We check if open hits stop/target first,
                # then if low hits stop (for long), then high hits target.
                
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
                    
                    if (t - pos_bar) >= self.ratchet.time_decay_bars and pos_max_r < self.ratchet.time_decay_r:
                        exit_px = cl[t]
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
                            "reason": "TIME_DECAY"
                        })
                        pos_side = 0
            
            # Terminal settlement at end of data (B8)
            if t == T - 1 and pos_side != 0:
                exit_px = cl[t]
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
                    "reason": "TERMINAL_SETTLEMENT"
                })
                pos_side = 0
                unreal = 0.0

            if pos_side == 1:
                unreal = pos_qty * (cl[t] - pos_entry) - pos_qty * (pos_entry + cl[t]) * self.fric.taker_fee
            elif pos_side == -1:
                unreal = pos_qty * (pos_entry - cl[t]) - pos_qty * (pos_entry + cl[t]) * self.fric.taker_fee
            else: 
                unreal = 0.0
                
            equity = realized + unreal
            if equity > peak: peak = equity
            equity_curve[t] = equity
            
            current_dd = (peak - equity) / peak if peak > 0 else 0.0

            # Force exit if DD limit breached while in position
            if not training_mode and current_dd >= self.risk.drawdown_limit and pos_side != 0:
                exit_px = cl[t]
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
                    "reason": "DRAWDOWN_LIMIT"
                })
                pos_side = 0
                unreal = 0.0
                equity = realized
                equity_curve[t] = equity
                current_dd = (peak - equity) / peak if peak > 0 else 0.0
            
            # Entry logic
            # Signals at t-1 are executed at the open of t (B3)
            sig_side = signal_side[t-1]
            raw_r = signal_raw_r[t-1]

            if pos_side == 0 and t < T - 1 and sig_side != 0:
                net_profit = realized - self.risk.initial_capital
                
                if not training_mode and current_dd >= self.risk.drawdown_limit:
                    continue
                
                if net_profit > 50.0:
                    trade_risk = min(self.risk.house_money_risk, equity * 0.01)
                elif current_dd > 0.025:
                    trade_risk = self.risk.drawdown_defense_risk
                else:
                    trade_risk = self.risk.base_risk
                    
                if sig_side == 1:
                    # B3: execute at open of t
                    px = op[t] * (1.0 + self.fric.entry_slippage)
                    if raw_r <= 0: raw_r = px * 0.005
                    stop_px = px - raw_r
                    target_px = px + (raw_r * self.ratchet.min_target_r)
                    
                    # B4: Size from all-in expected stop loss
                    actual_stop = stop_px * (1.0 - self.fric.exit_slippage)
                    loss_per_share = (px - actual_stop) + (px * self.fric.taker_fee) + (actual_stop * self.fric.taker_fee)
                    
                    pos_side = 1; pos_entry = px; pos_stop = stop_px
                    pos_target = target_px
                    pos_risk = trade_risk; pos_qty = trade_risk / loss_per_share; pos_bar = t; pos_max_r = 0.0; pos_rr = raw_r
                    
                elif sig_side == -1:
                    # B3: execute at open of t
                    px = op[t] * (1.0 - self.fric.entry_slippage)
                    if raw_r <= 0: raw_r = px * 0.005
                    stop_px = px + raw_r
                    target_px = px - (raw_r * self.ratchet.min_target_r)
                    
                    # B4: Size from all-in expected stop loss
                    actual_stop = stop_px * (1.0 + self.fric.exit_slippage)
                    loss_per_share = (actual_stop - px) + (px * self.fric.taker_fee) + (actual_stop * self.fric.taker_fee)
                    
                    pos_side = -1; pos_entry = px; pos_stop = stop_px
                    pos_target = target_px
                    pos_risk = trade_risk; pos_qty = trade_risk / loss_per_share; pos_bar = t; pos_max_r = 0.0; pos_rr = raw_r

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
            "trades_list": trades,
            "equity_curve": equity_curve
        }
