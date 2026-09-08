import numpy as np
import pandas as pd
from typing import Dict, List, Optional
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
    lock1_r: float = 0.80
    min_target_r: float = 2.5
    time_decay_bars: int = 24
    time_decay_r: float = 0.20


class ExecutionKernel:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(),
                 fric_cfg: FrictionConfig = FrictionConfig(),
                 ratchet_cfg: RatchetConfig = RatchetConfig()):
        self.risk = risk_cfg
        self.fric = fric_cfg
        self.ratchet = ratchet_cfg

        # position state
        self._pos_side = 0
        self._pos_entry = 0.0
        self._pos_stop = 0.0
        self._pos_target = 0.0
        self._pos_qty = 0.0
        self._pos_risk = 0.0
        self._pos_bar = -1
        self._pos_max_r = 0.0
        self._pos_rr = 1.0

    # ---------- helpers ----------
    def _close_trade(self, t: int, exit_px: float, reason: str, realized: float, trades: List[Dict]) -> float:
        pos_side, pos_qty = self._pos_side, self._pos_qty
        gross = pos_qty * (exit_px - self._pos_entry) if pos_side == 1 else pos_qty * (self._pos_entry - exit_px)
        fees = pos_qty * (self._pos_entry + exit_px) * self.fric.taker_fee
        net = gross - fees
        realized += net
        trades.append({
            "entry_bar": self._pos_bar,
            "exit_bar": t,
            "side": "LONG" if pos_side == 1 else "SHORT",
            "entry": self._pos_entry,
            "exit": exit_px,
            "pnl": net,
            "r": net / self._pos_risk if self._pos_risk > 0 else 0.0,
            "max_r": self._pos_max_r,
            "reason": reason
        })
        self._pos_side = 0
        return realized

    def _apply_ratchet(self, hi: float, lo: float) -> None:
        """Update trailing stop from intrabar extremes (bar j+1 onward, never entry bar open)."""
        rr = self._pos_rr
        if self._pos_side == 1:
            r_gain = (hi - self._pos_entry) / rr
            if r_gain > self._pos_max_r:
                self._pos_max_r = r_gain
            if self._pos_max_r >= self.ratchet.arm1_r:
                self._pos_stop = max(self._pos_stop, self._pos_entry + self.ratchet.lock1_r * rr)
            elif self._pos_max_r >= self.ratchet.arm0_r:
                self._pos_stop = max(self._pos_stop, self._pos_entry + self.ratchet.lock0_r * rr)
        elif self._pos_side == -1:
            r_gain = (self._pos_entry - lo) / rr
            if r_gain > self._pos_max_r:
                self._pos_max_r = r_gain
            if self._pos_max_r >= self.ratchet.arm1_r:
                self._pos_stop = min(self._pos_stop, self._pos_entry - self.ratchet.lock1_r * rr)
            elif self._pos_max_r >= self.ratchet.arm0_r:
                self._pos_stop = min(self._pos_stop, self._pos_entry - self.ratchet.lock0_r * rr)

    # ---------- main loop ----------
    def run(self, df: pd.DataFrame, signals: pd.DataFrame, training_mode: bool = False) -> Dict:
        """
        Runs the centralized causal execution engine.
        df: Price data with open, high, low, close.
        signals: DataFrame containing 'side' (1 for LONG, -1 for SHORT, 0 for None),
                 'raw_r' (the un-slippaged risk geometry in price terms).
        """
        T = len(df)
        if T == 0:
            return {
                "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0,
                "trades": 0, "net_pnl": 0.0, "trades_list": [], "equity_curve": np.array([])
            }

        op = df["open"].values
        hi = df["high"].values
        lo = df["low"].values
        cl = df["close"].values
        signal_side = signals["side"].values
        signal_raw_r = signals["raw_r"].values

        realized = self.risk.initial_capital
        peak = realized
        equity_curve = np.full(T, realized)
        trades: List[Dict] = []

        # position state
        self._pos_side = 0
        self._pos_entry = 0.0
        self._pos_stop = 0.0
        self._pos_target = 0.0
        self._pos_qty = 0.0
        self._pos_risk = 0.0
        self._pos_bar = -1
        self._pos_max_r = 0.0
        self._pos_rr = 1.0

        pending_side = 0
        pending_raw_r = 0.0   # signal set on bar j, filled on j+1

        if signal_side[0] != 0:
            pending_side = int(signal_side[0])
            pending_raw_r = float(signal_raw_r[0])

        # FIX C-1/C-2: pending_sig[j] -> fill at Open[j+1], evaluate SL/TP on the SAME bar j+1
        for t in range(1, T):
            # ---- 1) Fill pending signal at this bar's open ----
            if pending_side != 0:
                net_profit = realized - self.risk.initial_capital
                current_dd = (peak - realized) / peak if peak > 0 else 0.0

                if (not training_mode) and current_dd >= self.risk.drawdown_limit:
                    pending_side = 0  # blocked by hard DD limit
                else:
                    px = op[t] * (1.0 + self.fric.entry_slippage * pending_side)
                    raw_r = pending_raw_r if pending_raw_r > 0 else px * 0.005

                    if pending_side == 1:
                        stop_px = px - raw_r
                        target_px = px + raw_r * self.ratchet.min_target_r
                        actual_stop = stop_px * (1.0 - self.fric.exit_slippage)
                        loss_per_share = (px - actual_stop) + (px + actual_stop) * self.fric.taker_fee
                    else:
                        stop_px = px + raw_r
                        target_px = px - raw_r * self.ratchet.min_target_r
                        actual_stop = stop_px * (1.0 + self.fric.exit_slippage)
                        loss_per_share = (actual_stop - px) + (px + actual_stop) * self.fric.taker_fee

                    if net_profit > 50.0:
                        trade_risk = min(self.risk.house_money_risk, realized * 0.01)
                    elif current_dd > 0.025:
                        trade_risk = self.risk.drawdown_defense_risk
                    else:
                        trade_risk = self.risk.base_risk

                    self._pos_side = pending_side
                    self._pos_entry = px
                    self._pos_stop = stop_px
                    self._pos_target = target_px
                    self._pos_risk = trade_risk
                    self._pos_qty = trade_risk / loss_per_share if loss_per_share > 0 else 0.0
                    self._pos_bar = t
                    self._pos_max_r = 0.0
                    self._pos_rr = raw_r

                pending_side = 0
                pending_raw_r = 0.0

            # ---- 2) Intrabar exit evaluation (INCLUDES entry bar = FIX C-2) ----
            if self._pos_side != 0:
                o_, h_, l_, c_ = op[t], hi[t], lo[t], cl[t]
                exit_px = 0.0
                exit_reason = ""

                if self._pos_side == 1:
                    if o_ <= self._pos_stop:
                        exit_px = o_ * (1.0 - self.fric.exit_slippage)
                        exit_reason = "STOP_OPEN"
                    elif o_ >= self._pos_target:
                        exit_px = o_
                        exit_reason = "TARGET_OPEN"
                    elif l_ <= self._pos_stop:  # STOP-FIRST on ambiguity
                        exit_px = self._pos_stop * (1.0 - self.fric.exit_slippage)
                        exit_reason = "STOP_BAR"
                    elif h_ >= self._pos_target:
                        exit_px = self._pos_target
                        exit_reason = "TARGET_BAR"
                else:
                    if o_ >= self._pos_stop:
                        exit_px = o_ * (1.0 + self.fric.exit_slippage)
                        exit_reason = "STOP_OPEN"
                    elif o_ <= self._pos_target:
                        exit_px = o_
                        exit_reason = "TARGET_OPEN"
                    elif h_ >= self._pos_stop:  # STOP-FIRST on ambiguity
                        exit_px = self._pos_stop * (1.0 + self.fric.exit_slippage)
                        exit_reason = "STOP_BAR"
                    elif l_ <= self._pos_target:
                        exit_px = self._pos_target
                        exit_reason = "TARGET_BAR"

                if exit_reason:
                    realized = self._close_trade(t, exit_px, exit_reason, realized, trades)
                else:
                    # ratchet updates AFTER exit check -> lock levels bind bar t+1 onward
                    self._apply_ratchet(h_, l_)
                    if (t - self._pos_bar) >= self.ratchet.time_decay_bars and self._pos_max_r < self.ratchet.time_decay_r:
                        realized = self._close_trade(t, c_, "TIME_DECAY", realized, trades)

            # ---- 3) Mark-to-market equity & DD gate ----
            if self._pos_side == 1:
                unreal = self._pos_qty * (cl[t] - self._pos_entry) - self._pos_qty * (self._pos_entry + cl[t]) * self.fric.taker_fee
            elif self._pos_side == -1:
                unreal = self._pos_qty * (self._pos_entry - cl[t]) - self._pos_qty * (self._pos_entry + cl[t]) * self.fric.taker_fee
            else:
                unreal = 0.0

            equity = realized + unreal
            if equity > peak:
                peak = equity
            equity_curve[t] = equity
            current_dd = (peak - equity) / peak if peak > 0 else 0.0

            if (not training_mode) and current_dd >= self.risk.drawdown_limit and self._pos_side != 0:
                realized = self._close_trade(t, cl[t], "DRAWDOWN_LIMIT", realized, trades)
                equity = realized
                equity_curve[t] = equity
                current_dd = (peak - equity) / peak if peak > 0 else 0.0

            # ---- 4) Signal on bar t becomes PENDING for bar t+1 (FIX C-1) ----
            if t < T - 1 and self._pos_side == 0:
                sig = signal_side[t]
                if sig != 0:
                    pending_side = int(sig)
                    pending_raw_r = float(signal_raw_r[t])

            # ---- 5) Terminal settlement ----
            if t == T - 1 and self._pos_side != 0:
                realized = self._close_trade(t, cl[t], "TERMINAL_SETTLEMENT", realized, trades)
                equity_curve[t] = realized

        tot = len(trades)
        wins = sum(1 for tr in trades if tr["pnl"] > 0)
        wr = (wins / tot * 100.0) if tot > 0 else 0.0
        net_pnl = realized - self.risk.initial_capital
        roi = (net_pnl / self.risk.initial_capital * 100.0)
        peaks = np.maximum.accumulate(equity_curve)
        with np.errstate(divide='ignore', invalid='ignore'):
            dds = np.where(peaks > 0, (peaks - equity_curve) / peaks * 100.0, 0.0)
        max_dd = float(np.max(dds)) if len(dds) > 0 else 0.0

        return {
            "roi_pct": roi, "max_dd_pct": max_dd, "win_rate_pct": wr,
            "trades": tot, "net_pnl": net_pnl,
            "trades_list": trades, "equity_curve": equity_curve
        }
