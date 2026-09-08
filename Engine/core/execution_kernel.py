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
    """Single-position OHLC simulator with next-open entries and stop-first paths.

    Newly armed ratchets bind on the next bar. Intrabar ordering is otherwise
    unknowable from OHLC; no same-bar favorable-high then raised-stop assumption.
    """
    def __init__(self, risk_cfg=RiskConfig(), fric_cfg=FrictionConfig(),
                 ratchet_cfg=RatchetConfig()):
        self.risk, self.fric, self.ratchet = risk_cfg, fric_cfg, ratchet_cfg
        if ratchet_cfg != RatchetConfig():
            raise ValueError('Execution requires the fixed institutional ratchet')
        if not (risk_cfg.initial_capital > 0 and risk_cfg.base_risk > 0
                and 0 < risk_cfg.drawdown_limit < 1):
            raise ValueError('Invalid risk configuration')
        if any(not np.isfinite(x) or not 0 <= x < 1 for x in
               (fric_cfg.taker_fee, fric_cfg.entry_slippage, fric_cfg.exit_slippage)):
            raise ValueError('Invalid friction configuration')

    @staticmethod
    def prepare_prices(df):
        prices = df.loc[:, ['open', 'high', 'low', 'close']].to_numpy(dtype=float)
        if not np.isfinite(prices).all() or np.any(prices <= 0):
            raise ValueError('OHLC must be positive and finite')
        if len(prices) and (np.any(prices[:, 1] < prices[:, [0, 2, 3]].max(axis=1))
                            or np.any(prices[:, 2] > prices[:, [0, 1, 3]].min(axis=1))):
            raise ValueError('Invalid OHLC geometry')
        return prices

    def _position(self, t, side, raw_r, open_price, budget):
        entry = open_price * (1 + side * self.fric.entry_slippage)
        stop = entry - side * raw_r
        target = entry + side * raw_r * 2.5
        if not np.isfinite(raw_r) or raw_r <= 0 or min(stop, target) <= 0:
            return None
        stop_fill = stop * (1 - side * self.fric.exit_slippage)
        loss = side * (entry - stop_fill) + self.fric.taker_fee * (entry + stop_fill)
        if loss <= 0 or budget <= 0:
            return None
        return dict(side=side, entry=entry, stop=stop, target=target,
                    qty=budget / loss, risk=budget, bar=t, rr=raw_r, max_r=0.)

    def _pnl(self, pos, price):
        return pos['qty'] * (pos['side'] * (price - pos['entry'])
                            - self.fric.taker_fee * (pos['entry'] + price))

    def _trade(self, pos, t, price, reason):
        pnl = self._pnl(pos, price)
        return dict(entry_bar=pos['bar'], exit_bar=t,
                    side='LONG' if pos['side'] == 1 else 'SHORT',
                    entry=pos['entry'], exit=price, pnl=pnl, r=pnl / pos['risk'],
                    max_r=pos['max_r'], reason=reason)

    def _advance_bar(self, pos, t, bar, account_floor=None, realized=0.):
        o, h, l, c = bar
        side, stop = pos['side'], pos['stop']
        reason_stop = 'STOP'
        # Price at which all-in liquidation equity reaches the account floor.
        # The floor uses only already-observed equity, never this bar's high.
        if account_floor is not None:
            coefficient = (side - self.fric.taker_fee) * (1 - side * self.fric.exit_slippage)
            dd_stop = ((account_floor - realized) / pos['qty']
                       + (side + self.fric.taker_fee) * pos['entry']) / coefficient
            if side * (dd_stop - stop) > 0:
                stop, reason_stop = dd_stop, 'DRAWDOWN_LIMIT'
        if side * (o - stop) <= 0:
            return self._trade(pos, t, o * (1 - side * self.fric.exit_slippage),
                               'STOP_OPEN' if reason_stop == 'STOP' else reason_stop)
        if side * (o - pos['target']) >= 0:
            pos['max_r'] = max(pos['max_r'], 2.5)
            return self._trade(pos, t, pos['target'], 'TARGET_OPEN')
        adverse = l if side == 1 else h
        favorable = h if side == 1 else l
        if side * (adverse - stop) <= 0:
            return self._trade(pos, t, stop * (1 - side * self.fric.exit_slippage),
                               'STOP_BAR' if reason_stop == 'STOP' else reason_stop)
        if side * (favorable - pos['target']) >= 0:
            pos['max_r'] = max(pos['max_r'], 2.5)
            return self._trade(pos, t, pos['target'], 'TARGET_BAR')
        pos['max_r'] = max(pos['max_r'], side * (favorable - pos['entry']) / pos['rr'])
        current_r = side * (c - pos['entry']) / pos['rr']
        if t - pos['bar'] + 1 >= 24 and current_r < 0.2:
            return self._trade(pos, t, c * (1 - side * self.fric.exit_slippage), 'TIME_DECAY')
        # These mutations occur only after the current bar's exit checks.
        if pos['max_r'] >= 1.5:
            proposed = pos['entry'] + side * 0.80 * pos['rr']
        elif pos['max_r'] >= 0.8:
            proposed = pos['entry'] + side * 0.15 * pos['rr']
        else:
            return None
        pos['stop'] = max(stop, proposed) if side == 1 else min(stop, proposed)
        return None

    def simulate_event(self, df, signal_bar, side, raw_r, *, prices=None):
        """Independent setup outcome; terminal settlement is right-censored.

        Pass prepare_prices(df) once via prices for bulk candidate labeling.
        Account-level trading halts do not redefine the setup's target label.
        """
        prices = self.prepare_prices(df) if prices is None else prices
        if side not in (-1, 1) or signal_bar < 0 or signal_bar + 1 >= len(prices):
            return None
        t0 = signal_bar + 1
        pos = self._position(t0, side, raw_r, prices[t0, 0], self.risk.base_risk)
        if pos is None:
            return None
        for t in range(t0, len(prices)):
            trade = self._advance_bar(pos, t, prices[t])
            if trade is not None:
                return trade
        return self._trade(pos, len(prices) - 1,
                           prices[-1, 3] * (1 - side * self.fric.exit_slippage),
                           'TERMINAL_SETTLEMENT')

    def run(self, df, signals, training_mode=False):
        if not df.index.equals(signals.index):
            raise ValueError('Signals and prices must have identical indexes')
        prices = self.prepare_prices(df)
        sides = signals.side.to_numpy()
        distances = signals.raw_r.to_numpy(dtype=float)
        if not np.isin(sides, [-1, 0, 1]).all():
            raise ValueError('Invalid signal direction')
        active = sides != 0
        if np.any(~np.isfinite(distances[active])) or np.any(distances[active] <= 0):
            raise ValueError('Active signals require finite positive raw_r')
        realized = peak = self.risk.initial_capital
        equity_curve = np.full(len(df), realized)
        trades, pos, halted = [], None, False
        max_dd = 0.

        def mark(equity):
            nonlocal peak, max_dd
            peak = max(peak, equity)
            dd = (peak - equity) / peak
            max_dd = max(max_dd, dd)
            return dd

        for t in range(1, len(prices)):
            # Decide at open using state surviving the PREVIOUS bar only.
            # Exits later in this bar cannot retroactively free an entry slot.
            if pos is None and not halted and sides[t - 1] != 0:
                dd = (peak - realized) / peak
                budget = self.risk.base_risk
                if dd > 0.025:
                    budget = min(budget, self.risk.drawdown_defense_risk)
                floor = peak - min(peak * self.risk.drawdown_limit,
                                   self.risk.initial_capital * self.risk.drawdown_limit)
                budget = min(budget, max(0., realized - floor))
                pos = self._position(t, int(sides[t - 1]), distances[t - 1], prices[t, 0], budget)
            if pos is not None:
                open_mark = prices[t, 0]
                if pos['side'] * (open_mark - pos['target']) >= 0:
                    open_mark = pos['target']
                mark(realized + self._pnl(pos, open_mark))
                floor = peak - min(peak * self.risk.drawdown_limit,
                                   self.risk.initial_capital * self.risk.drawdown_limit)
                trade = self._advance_bar(pos, t, prices[t], floor, realized)
                # Adverse excursion before exit; stop-first conservative path.
                if trade is not None and (trade['reason'].startswith('STOP') or
                                          trade['reason'] in ('DRAWDOWN_LIMIT', 'TARGET_OPEN')):
                    mark(realized + trade['pnl'])
                else:
                    adverse = prices[t, 2] if pos['side'] == 1 else prices[t, 1]
                    mark(realized + self._pnl(pos, adverse))
                if trade is None and t == len(prices) - 1:
                    trade = self._trade(pos, t, prices[t, 3] * (1 - pos['side'] * self.fric.exit_slippage),
                                        'TERMINAL_SETTLEMENT')
                if trade is not None:
                    realized += trade['pnl']
                    trades.append(trade)
                    if trade['reason'] == 'DRAWDOWN_LIMIT':
                        halted = True
                    pos = None
            equity = realized if pos is None else realized + self._pnl(pos, prices[t, 3])
            dd = mark(equity)
            equity_curve[t] = equity
            if dd >= self.risk.drawdown_limit or peak - equity >= self.risk.initial_capital * self.risk.drawdown_limit:
                halted = True
        net = realized - self.risk.initial_capital
        return dict(roi_pct=100 * net / self.risk.initial_capital,
                    max_dd_pct=100 * max_dd,
                    win_rate_pct=100 * sum(tr['pnl'] > 0 for tr in trades) / len(trades) if trades else 0.,
                    trades=len(trades), net_pnl=net, trades_list=trades,
                    equity_curve=equity_curve, halted=halted)
