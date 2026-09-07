"""
================================================================================
SMC TRADER MAYNE ENGINE (HTF POI + LTF Breaker Block)
================================================================================
Institutional quantitative strategy for BTCUSDT (15m timeframe).
Uses HTF structure sweeps and LTF Breaker Blocks with institutional confluence.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, List, Callable
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

class SMCMayneSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), stop_atr: float = 4.0, rsi_long: float = 40.0, rsi_short: float = 60.0, liq_thresh: float = 1.8, zc_thresh: float = 0.8, vwap_thresh: float = 0.5):
        self.risk = risk_cfg
        self.fric = fric_cfg
        self.stop_atr = stop_atr
        self.rsi_long = rsi_long
        self.rsi_short = rsi_short
        self.liq_thresh = liq_thresh
        self.zc_thresh = zc_thresh
        self.vwap_thresh = vwap_thresh
        
    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> Dict:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        # Parse timestamp to detect day changes
        dt = pd.to_datetime(df_test["datetime_utc"])
        days = dt.dt.date.values
        long_liq_zs = df_test["long_liq_zs"].values
        short_liq_zs = df_test["short_liq_zs"].values
        long_liq_roll = pd.Series(long_liq_zs).rolling(4).max().fillna(0).values
        short_liq_roll = pd.Series(short_liq_zs).rolling(4).max().fillna(0).values
        zc_div = df_test["zc_div"].values
        spot_cvd = df_test["spot_cvd_15m"].values
        fut_cvd = df_test["future_cvd_15m"].values
        rsi = df_test["rsi_14"].values
        vwap_z = df_test["vwap_zscore"].values
        oi_change_pct = df_test["oi_change_pct"].values
        
        # HTF Trend Proxy
        ema_200 = df_test["ema_200"].values
        ema_800 = df_test["ema_800"].values
        
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
        
        # Removed active_breakers tracking
        for t in range(24, T):
            if pos_side != 0:
                o_, h_, l_, c_ = op[t], hi[t], lo[t], cl[t]
                exit_px = 0.0
                exit_reason = ""
                
                if pos_side == 1:
                    if o_ <= pos_stop: exit_px = o_ * (1.0 - self.fric.exit_slippage); exit_reason = "STOP_OPEN"
                    elif o_ >= pos_target: exit_px = o_; exit_reason = "TARGET_OPEN"
                    elif l_ <= pos_stop: exit_px = pos_stop * (1.0 - self.fric.exit_slippage); exit_reason = "STOP_BAR"
                    elif h_ >= pos_target: exit_px = pos_target; exit_reason = "TARGET_BAR"
                    
                    r_gain = (h_ - pos_entry) / pos_rr
                    if r_gain > pos_max_r: pos_max_r = r_gain
                    if not exit_reason and (t - pos_bar) >= 24 and pos_max_r < 0.2:
                        exit_px = c_ * (1.0 - self.fric.exit_slippage); exit_reason = "TIME_DECAY"
                        
                elif pos_side == -1:
                    if o_ >= pos_stop: exit_px = o_ * (1.0 + self.fric.exit_slippage); exit_reason = "STOP_OPEN"
                    elif o_ <= pos_target: exit_px = o_; exit_reason = "TARGET_OPEN"
                    elif h_ >= pos_stop: exit_px = pos_stop * (1.0 + self.fric.exit_slippage); exit_reason = "STOP_BAR"
                    elif l_ <= pos_target: exit_px = pos_target; exit_reason = "TARGET_BAR"
                    
                    r_gain = (pos_entry - l_) / pos_rr
                    if r_gain > pos_max_r: pos_max_r = r_gain
                    if not exit_reason and (t - pos_bar) >= 24 and pos_max_r < 0.2:
                        exit_px = c_ * (1.0 + self.fric.exit_slippage); exit_reason = "TIME_DECAY"
                        
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
                        "reason": exit_reason, "rr": pos_rr
                    })
                    pos_side = 0
                else:
                    if pos_side == 1:
                        if pos_max_r >= 1.5:
                            pos_stop = max(pos_stop, pos_entry + 0.80 * pos_rr)
                        elif pos_max_r >= 0.8:
                            pos_stop = max(pos_stop, pos_entry + 0.15 * pos_rr)
                    elif pos_side == -1:
                        if pos_max_r >= 1.5:
                            pos_stop = min(pos_stop, pos_entry - 0.80 * pos_rr)
                        elif pos_max_r >= 0.8:
                            pos_stop = min(pos_stop, pos_entry - 0.15 * pos_rr)
            
            unreal = 0.0
            if pos_side == 1: unreal = pos_qty * (cl[t] - pos_entry)
            elif pos_side == -1: unreal = pos_qty * (pos_entry - cl[t])
            equity = realized + unreal
            if equity > peak: peak = equity
            equity_curve[t] = equity
            
            if pos_side == 0 and t < T - 1:
                net_profit = realized - self.risk.initial_capital
                current_dd = (peak - equity) / peak if peak > 0 else 0.0
                
                if current_dd >= self.risk.drawdown_limit and not training_mode:
                    continue
                elif current_dd > 0.025:
                    trade_risk = self.risk.drawdown_defense_risk
                elif net_profit > 50.0:
                    trade_risk = self.risk.house_money_risk
                else:
                    trade_risk = self.risk.base_risk
                    
                delta_spot = spot_cvd[t]
                delta_fut = fut_cvd[t]
                
                # Invariant Alpha Confluence (Liquidity Sweep)
                # Ensure we are trading in the direction of the HTF trend (ema_800)
                # But allowing mean reversion if the dip sweeps below ema_200
                long_sweep = (long_liq_roll[t] > self.liq_thresh and zc_div[t] > self.zc_thresh and rsi[t] < self.rsi_long and vwap_z[t] < -self.vwap_thresh and delta_spot > 0 and delta_fut < 0)
                short_sweep = (short_liq_roll[t] > self.liq_thresh and zc_div[t] < -self.zc_thresh and rsi[t] > self.rsi_short and vwap_z[t] > self.vwap_thresh and delta_spot < 0 and delta_fut > 0)
                
                # HTF Trend alignment (15m ema_800 is 200-hour EMA)
                trend_up = cl[t] > ema_800[t]
                trend_down = cl[t] < ema_800[t]
                
                sig_long = long_sweep and trend_up
                sig_short = short_sweep and trend_down
                
                if filter_func is not None:
                    if sig_long and not filter_func(t, "LONG"): sig_long = False
                    if sig_short and not filter_func(t, "SHORT"): sig_short = False
                            
                if sig_long and not sig_short:
                    px = cl[t] * (1.0 + self.fric.entry_slippage)
                    
                    r_ = atr[t] * self.stop_atr
                    
                    # Mathematical friction boundary
                    min_r = px * 0.005
                    if r_ < min_r: r_ = min_r
                    
                    if r_ <= px * 0.06: # Reject trades with excessively wide stops (>6%)
                        # Fixed 2.5R target (ACTIVE_CONTEXT invariant)
                        tp_dist = 2.5 * r_
                        
                        pos_side = 1; pos_entry = px; pos_stop = px - r_
                        pos_target = px + tp_dist 
                        
                        # Adjust qty for friction so gross loss + friction = trade_risk
                        loss_per_unit = (px - pos_stop*(1.0 - self.fric.exit_slippage)) + px*self.fric.taker_fee + pos_stop*(1.0 - self.fric.exit_slippage)*self.fric.taker_fee
                        pos_qty = trade_risk / loss_per_unit
                        
                        pos_risk = trade_risk; pos_bar = t; pos_max_r = 0.0; pos_rr = r_
                
                elif sig_short and not sig_long:
                    px = cl[t] * (1.0 - self.fric.entry_slippage)
                    
                    r_ = atr[t] * self.stop_atr
                    
                    min_r = px * 0.005
                    if r_ < min_r: r_ = min_r
                    
                    if r_ <= px * 0.06: 
                        tp_dist = 2.5 * r_
                        
                        pos_side = -1; pos_entry = px; pos_stop = px + r_
                        pos_target = px - tp_dist
                        
                        loss_per_unit = (pos_stop*(1.0 + self.fric.exit_slippage) - px) + px*self.fric.taker_fee + pos_stop*(1.0 + self.fric.exit_slippage)*self.fric.taker_fee
                        pos_qty = trade_risk / loss_per_unit
                        
                        pos_risk = trade_risk; pos_bar = t; pos_max_r = 0.0; pos_rr = r_

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
