# Engine/core/portfolio_execution_kernel.py
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig


@dataclass
class _Pos:
    symbol: str
    side: int
    entry: float
    stop: float
    target: float
    qty: float
    risk: float
    entry_bar: int
    max_r: float
    rr: float


class PortfolioExecutionKernel:
    """
    Multi-symbol portfolio kernel. One shared equity pool, one hard DD breaker,
    max `max_positions` concurrent positions. Fills at Open[j+1] of the symbol
    where the signal fired; stop-first ambiguity; full ratchet suite per position.

    All symbol DataFrames must share an identical, monotonic DatetimeIndex.
    """

    def __init__(self,
                 symbols: List[str],
                 risk: RiskConfig = RiskConfig(),
                 fric: FrictionConfig = FrictionConfig(),
                 ratchet: RatchetConfig = RatchetConfig(),
                 max_positions: int = 2,
                 dd_defense_thresh: float = 0.018,
                 dd_entry_buffer: Optional[float] = None):
        self.symbols = list(symbols)
        self.risk = risk
        self.fric = fric
        self.rat = ratchet
        self.max_positions = max_positions
        self.dd_defense_thresh = dd_defense_thresh
        self.dd_entry_buffer = dd_entry_buffer if dd_entry_buffer is not None else getattr(risk, "drawdown_entry_buffer", 0.038)
        self.trades: List[Dict] = []

    # ---------------- helpers ----------------
    def _entry_price(self, side: int, o: float) -> float:
        return o * (1.0 + self.fric.entry_slippage * side)

    def _loss_per_share(self, side: int, px: float, raw_r: float) -> float:
        if side == 1:
            actual_stop = (px - raw_r) * (1.0 - self.fric.exit_slippage)
            return (px - actual_stop) + (px + actual_stop) * self.fric.taker_fee
        actual_stop = (px + raw_r) * (1.0 + self.fric.exit_slippage)
        return (actual_stop - px) + (px + actual_stop) * self.fric.taker_fee

    def _ratchet(self, p: _Pos, hi: float, lo: float) -> None:
        R = self.rat
        gain = (hi - p.entry) / p.rr if p.side == 1 else (p.entry - lo) / p.rr
        if gain > p.max_r:
            p.max_r = gain
        arm2 = getattr(R, "arm2_r", 1.80)
        lock2 = getattr(R, "lock2_r", 1.40)
        if p.side == 1:
            if p.max_r >= arm2:
                p.stop = max(p.stop, p.entry + lock2 * p.rr)
            elif p.max_r >= R.arm1_r:
                p.stop = max(p.stop, p.entry + R.lock1_r * p.rr)
            elif p.max_r >= R.arm0_r:
                p.stop = max(p.stop, p.entry + R.lock0_r * p.rr)
        else:
            if p.max_r >= arm2:
                p.stop = min(p.stop, p.entry - lock2 * p.rr)
            elif p.max_r >= R.arm1_r:
                p.stop = min(p.stop, p.entry - R.lock1_r * p.rr)
            elif p.max_r >= R.arm0_r:
                p.stop = min(p.stop, p.entry - R.lock0_r * p.rr)

    def _exit(self, p: _Pos, px: float, reason: str, t: int) -> float:
        gross = p.qty * (px - p.entry) if p.side == 1 else p.qty * (p.entry - px)
        fees = p.qty * (p.entry + px) * self.fric.taker_fee
        net = gross - fees
        self.trades.append({
            "symbol": p.symbol, "entry_bar": p.entry_bar, "exit_bar": t,
            "side": "LONG" if p.side == 1 else "SHORT",
            "entry": p.entry, "exit": px, "pnl": net,
            "r": net / p.risk if p.risk > 0 else 0.0,
            "max_r": p.max_r, "reason": reason})
        return net

    def _check_exit(self, p: _Pos, o: float, h: float, l: float) -> Tuple[Optional[float], str]:
        if p.side == 1:
            if o <= p.stop:   return o * (1.0 - self.fric.exit_slippage), "STOP_OPEN"
            if o >= p.target: return o, "TARGET_OPEN"
            if l <= p.stop:   return p.stop * (1.0 - self.fric.exit_slippage), "STOP_BAR"
            if h >= p.target: return p.target, "TARGET_BAR"
        else:
            if o >= p.stop:   return o * (1.0 + self.fric.exit_slippage), "STOP_OPEN"
            if o <= p.target: return o, "TARGET_OPEN"
            if h >= p.stop:   return p.stop * (1.0 + self.fric.exit_slippage), "STOP_BAR"
            if l <= p.target: return p.target, "TARGET_BAR"
        return None, ""

    # ---------------- main loop ----------------
    def run(self, data: Dict[str, pd.DataFrame],
            gated_signals: Dict[str, pd.DataFrame],
            training_mode: bool = False) -> Dict:
        if not data:
            return {
                "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0,
                "trades": 0, "net_pnl": 0.0, "trades_list": [], "equity_curve": np.array([])
            }
        T = min(len(d) for d in data.values()) if data else 0
        if T == 0:
            return {
                "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0,
                "trades": 0, "net_pnl": 0.0, "trades_list": [], "equity_curve": np.array([])
            }
        realized = self.risk.initial_capital
        peak = realized
        equity_curve = np.zeros(T)
        self.trades = []
        positions: Dict[str, _Pos] = {}
        pending: Dict[str, tuple] = {}   # sym -> (side, raw_r) set at close of t, filled t+1

        op = {s: data[s]["open"].values for s in self.symbols if s in data}
        hi = {s: data[s]["high"].values for s in self.symbols if s in data}
        lo = {s: data[s]["low"].values for s in self.symbols if s in data}
        cl = {s: data[s]["close"].values for s in self.symbols if s in data}
        sig_side = {s: gated_signals[s]["side"].values for s in self.symbols if s in gated_signals}
        sig_rr = {s: gated_signals[s]["raw_r"].values for s in self.symbols if s in gated_signals}

        # Check bar 0 signal queue
        for sym in self.symbols:
            if sym in sig_side and len(sig_side[sym]) > 0:
                s_ = int(sig_side[sym][0])
                if s_ != 0:
                    pending[sym] = (s_, float(sig_rr[sym][0]))

        def mark_to_market(t: int) -> float:
            unreal = 0.0
            for s, p in positions.items():
                if p.side == 1:
                    unreal += p.qty * (cl[s][t] - p.entry)
                else:
                    unreal += p.qty * (p.entry - cl[s][t])
                unreal -= p.qty * (p.entry + cl[s][t]) * self.fric.taker_fee
            return realized + unreal

        for t in range(1, T):
            current_dd = (peak - mark_to_market(t - 1)) / peak if peak > 0 else 0.0
            entry_limit = self.dd_entry_buffer if self.dd_entry_buffer is not None else self.risk.drawdown_limit
            dd_blocked = (not training_mode) and current_dd >= entry_limit

            # --- 1) Fill pending entries at this bar's open (signal was at t-1 close) ---
            for sym in list(pending.keys()):
                if len(positions) >= self.max_positions:
                    break
                if dd_blocked:
                    pending.pop(sym)
                    continue
                side, raw_r = pending.pop(sym)
                px = self._entry_price(side, op[sym][t])
                rr = raw_r if raw_r > 0 else px * 0.005
                lps = self._loss_per_share(side, px, rr)
                if lps <= 0:
                    continue
                net_profit = realized - self.risk.initial_capital
                if current_dd > self.dd_defense_thresh:
                    trade_risk = self.risk.drawdown_defense_risk
                elif net_profit > 50.0:
                    trade_risk = self.risk.house_money_risk
                else:
                    trade_risk = self.risk.base_risk
                if side == 1:
                    stop, tgt = px - rr, px + rr * self.rat.min_target_r
                else:
                    stop, tgt = px + rr, px - rr * self.rat.min_target_r
                positions[sym] = _Pos(sym, side, px, stop, tgt,
                                      trade_risk / lps, trade_risk, t, 0.0, rr)

            # --- 2) Manage open positions (entry bar included) ---
            for sym in list(positions.keys()):
                p = positions[sym]
                exit_px, reason = self._check_exit(p, op[sym][t], hi[sym][t], lo[sym][t])
                if not exit_px:
                    self._ratchet(p, hi[sym][t], lo[sym][t])
                    if (t - p.entry_bar) >= self.rat.time_decay_bars and p.max_r < self.rat.time_decay_r:
                        exit_px, reason = cl[sym][t], "TIME_DECAY"
                if exit_px:
                    realized += self._exit(p, exit_px, reason, t)
                    del positions[sym]

            # --- 3) Mark equity, hard portfolio DD breaker ---
            equity = mark_to_market(t)
            if equity > peak:
                peak = equity
            equity_curve[t] = equity
            current_dd = (peak - equity) / peak if peak > 0 else 0.0

            if (not training_mode) and current_dd >= self.risk.drawdown_limit and positions:
                for sym in list(positions.keys()):
                    p = positions[sym]
                    realized += self._exit(p, cl[sym][t], "DRAWDOWN_LIMIT", t)
                    del positions[sym]
                equity = realized
                equity_curve[t] = equity

            # --- 4) Queue signals from bar t close for fill at t+1 open ---
            if t < T - 1:
                for sym in self.symbols:
                    if sym in sig_side and t < len(sig_side[sym]):
                        s_ = int(sig_side[sym][t])
                        if s_ != 0 and sym not in positions and sym not in pending:
                            pending[sym] = (s_, float(sig_rr[sym][t]))

            # --- 5) Terminal settlement ---
            if t == T - 1:
                for sym in list(positions.keys()):
                    realized += self._exit(positions[sym], cl[sym][t],
                                           "TERMINAL_SETTLEMENT", t)
                    del positions[sym]
                equity_curve[t] = realized

        equity_curve[0] = self.risk.initial_capital
        tot = len(self.trades)
        wins = sum(1 for tr in self.trades if tr["pnl"] > 0)
        peaks = np.maximum.accumulate(equity_curve)
        with np.errstate(divide="ignore", invalid="ignore"):
            dds = np.where(peaks > 0, (peaks - equity_curve) / peaks * 100.0, 0.0)
        net_pnl = realized - self.risk.initial_capital
        return {
            "roi_pct": net_pnl / self.risk.initial_capital * 100.0,
            "max_dd_pct": float(np.max(dds)) if T else 0.0,
            "win_rate_pct": wins / tot * 100.0 if tot else 0.0,
            "trades": tot, "net_pnl": net_pnl,
            "trades_list": self.trades, "equity_curve": equity_curve,
        }
