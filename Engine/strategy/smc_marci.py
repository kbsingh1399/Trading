"""
================================================================================
SMC MARCI ENGINE (Bollinger Bands + Trendline / Pullback Break)
================================================================================
Institutional quantitative strategy for BTCUSDT (15m timeframe).
Uses Bollinger Bands and fractal pullbacks to resume primary trend.
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

class SMCMarciSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig()):
        self.risk = risk_cfg
        self.fric = fric_cfg
        
    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> Dict:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        ema200 = df_test["ema_200"].values
        long_liq_zs = df_test["long_liq_zs"].values
        short_liq_zs = df_test["short_liq_zs"].values
        zc_div = df_test["zc_div"].values
        spot_cvd = df_test["spot_cvd_15m"].values
        fut_cvd = df_test["future_cvd_15m"].values
        rsi = df_test["rsi_14"].values
        vwap_z = df_test["vwap_zscore"].values
        
        # Calculate Bollinger Bands (20, 2)
        close_series = pd.Series(cl)
        bb_mid = close_series.rolling(window=20).mean().values
        bb_std = close_series.rolling(window=20).std(ddof=0).values
        bb_upper = bb_mid + (2 * bb_std)
        bb_lower = bb_mid - (2 * bb_std)
        
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
        
        # Local fractal trackers
        for t in range(5, T):
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
                        "reason": exit_reason
                    })
                    pos_side = 0
                else:
                    r_gain = (hi[t] - pos_entry) / pos_rr if pos_side == 1 else (pos_entry - lo[t]) / pos_rr
                    if r_gain > pos_max_r: pos_max_r = r_gain
                    if pos_side == 1:
                        if pos_max_r >= 1.5:
                            pos_stop = max(pos_stop, pos_entry + 0.8 * pos_rr)
                        elif pos_max_r >= 0.8:
                            pos_stop = max(pos_stop, pos_entry + 0.15 * pos_rr)
                    elif pos_side == -1:
                        if pos_max_r >= 1.5:
                            pos_stop = min(pos_stop, pos_entry - 0.8 * pos_rr)
                        elif pos_max_r >= 0.8:
                            pos_stop = min(pos_stop, pos_entry - 0.15 * pos_rr)
                    
                    if (t - pos_bar) >= 24 and pos_max_r < 0.2: # time decay
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
                
                if current_dd >= self.risk.drawdown_limit:
                    continue
                elif current_dd > 0.025:
                    trade_risk = self.risk.drawdown_defense_risk
                elif net_profit > 50.0:
                    trade_risk = self.risk.house_money_risk
                else:
                    trade_risk = self.risk.base_risk
                
                sig_long = False
                sig_short = False
                
                # Marci Logic - Longs
                # Uptrend confirmation: EMA200 sloping up (roughly) and price above it
                if cl[t] > ema200[t] and ema200[t] > ema200[t-5]:
                    # Identify pullback to the lower BB or mid BB
                    if lo[t-2] < bb_lower[t-2] or lo[t-2] < bb_mid[t-2]:
                        # A 3-bar swing low formed at t-2
                        if lo[t-2] < lo[t-3] and lo[t-2] < lo[t-1]:
                            # "Trendline Break" proxy: Momentum resumes, t closes above t-1 high
                            if cl[t] > hi[t-1] and cl[t] > op[t]:
                                # Institutional Confluence Overlay
                                if (long_liq_zs[t] > 0.5 or short_liq_zs[t] > 0.5) and zc_div[t] > -0.5:
                                    sig_long = True
                                
                # Marci Logic - Shorts
                # Downtrend confirmation: EMA200 sloping down (roughly) and price below it
                if cl[t] < ema200[t] and ema200[t] < ema200[t-5]:
                    # Identify pullback to the upper BB or mid BB
                    if hi[t-2] > bb_upper[t-2] or hi[t-2] > bb_mid[t-2]:
                        # A 3-bar swing high formed at t-2
                        if hi[t-2] > hi[t-3] and hi[t-2] > hi[t-1]:
                            # "Trendline Break" proxy: Momentum resumes, t closes below t-1 low
                            if cl[t] < lo[t-1] and cl[t] < op[t]:
                                # Institutional Confluence Overlay
                                if (long_liq_zs[t] > 0.5 or short_liq_zs[t] > 0.5) and zc_div[t] > -0.5:
                                    sig_short = True
                
                if filter_func is not None:
                    if sig_long and not filter_func(t, 'LONG'): sig_long = False
                    if sig_short and not filter_func(t, 'SHORT'): sig_short = False

                if sig_long:
                    px = cl[t] * (1.0 + self.fric.entry_slippage)
                    # Stop below the fractal swing low
                    stop_level = lo[t-2]
                    r_ = px - stop_level
                    if r_ < atr[t] * 0.2: r_ = atr[t] * 0.2
                    
                    pos_side = 1; pos_entry = px; pos_stop = stop_level - (atr[t]*0.2)
                    pos_target = px + (r_ * 2.5) # 2.5R target (Marci recommends projecting distance)
                    pos_risk = trade_risk; pos_qty = trade_risk / r_; pos_bar = t; pos_max_r = 0.0; pos_rr = r_
                
                elif sig_short:
                    px = cl[t] * (1.0 - self.fric.entry_slippage)
                    stop_level = hi[t-2]
                    r_ = stop_level - px
                    if r_ < atr[t] * 0.2: r_ = atr[t] * 0.2
                    
                    pos_side = -1; pos_entry = px; pos_stop = stop_level + (atr[t]*0.2)
                    pos_target = px - (r_ * 2.5)
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
