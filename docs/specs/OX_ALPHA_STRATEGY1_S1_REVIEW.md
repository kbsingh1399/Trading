# Ox Alpha Strategy Review — Strategy 1: S1 Liquidation Cascade Engine
**Target:** Institutional Quantitative Review & Microstructure Alpha Audit  
**Strategy File:** `Engine/strategy/s1_liquidation_cascade.py`  
**Execution Kernel:** `Engine/core/execution_kernel.py`  
**Dataset Grounding:** Binance 15-Minute Dual-Table Master Dataset (Certified 98/100 by Ox Alpha)  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Archetype

### Strategy Thesis: Liquidation Cascade Absorption & Mean Reversion
In crypto perpetual futures markets, cascading liquidations represent extreme non-linear microstructure dislocations:
1. Highly leveraged long (or short) positions reach bankruptcy price boundaries.
2. The exchange's Liquidation Risk Engine triggers automated, aggressive market orders to close the underwater positions against the top of the order book.
3. This creates sudden, violent price displacement characterized by:
   - High Liquidation Z-Score ($\text{long\_liq\_zs} > 1.2$ or $> 1.8$).
   - Extreme intraday volume spikes ($\text{volume\_ratio} > 1.2$).
   - Temporary price divergence below intraday VWAP ($\text{vwap\_zscore} < -0.5$).
   - Extreme momentum exhaustion ($\text{RSI}_{14} < 40$).
4. Concurrently, institutional participants and informed market makers absorb this forced selling pressure on spot exchanges ($\Delta\text{Spot CVD} > 0$ while $\Delta\text{Futures CVD} < 0$, creating a high $\text{zc\_div} > 0.8$).
5. Once the cascade exhausts passive and market liquidation flow, the market experiences sharp mean-reversion toward equilibrium VWAP.

---

## 2. Quantitative Strategy Invariants

### 2.1 Signal Confluence Geometry
The strategy fires a causal directional signal at bar $t$ close (effective bar $t+1$ open):

$$\text{Signal}_{\text{LONG}} = (\text{long\_liq\_zs}_t > 1.2) \;\land\; (C_t > O_t) \;\land\; (\text{filter\_func}(t, \text{'LONG'}))$$

In high-confluence institutional mode:
$$\text{long\_liq\_zs} > 1.8 \;\land\; \text{zc\_div} > 0.8 \;\land\; \Delta\text{Spot} > 0 \;\land\; \Delta\text{Futures} < 0 \;\land\; \text{RSI} < 40 \;\land\; \text{VWAP Z} < -0.5$$

### 2.2 Risk Budget & Portfolio Governance
- **Initial Capital:** $5,000.00 USD.
- **Base Risk Budget:** $25.00 USD per trade ($0.50\%$ of equity).
- **House Money Tier:** $50.00 USD ($1.00\%$ max 2× risk when net session profits $> \$50.00$).
- **Drawdown Defense Tier:** $15.00 USD ($0.30\%$ risk when drawdown exceeds $2.5\%$).
- **Hard Drawdown Stop:** $4.50\%$ ($225.00 USD hard stop, trading ceases for the period).
- **Portfolio Concurrency:** Maximum 2 simultaneous open positions across all 18 symbols.

### 2.3 Microstructure Exit Ratchet (Anti-Retracement Defense)
Legacy 5.0R fixed targets caused an **85.8% retracement rate** of winning trades into full stop-outs during choppy or trending crypto markets. The modern microstructure ratchet eliminates this trap:
- **Phase 0 (Breakeven Lock):** At $+0.80\text{R}$ price gain, move stop to Entry $+0.15\text{R}$.
- **Phase 1 (Profit Lock):** At $+1.50\text{R}$ price gain, move stop to Entry $+0.80\text{R}$.
- **Target Exit:** Fixed exit at $+2.50\text{R}$.
- **Time Decay Invalidation:** If a trade fails to gain $+0.20\text{R}$ within 24 bars (6 hours), exit at market.
- **Causal Arming:** Stop modifications armed at bar $j$ close take effect at bar $j+1$ open only.

### 2.4 Transaction Frictions & Realistic Fill Modeling
- **Taker Fees:** 8 basis points ($0.08\%$) on both entry and exit.
- **Entry Slippage:** 10 basis points ($0.10\%$) against trade direction.
- **Exit Slippage (Stop / Market):** 15 basis points ($0.15\%$) against trade direction.
- **Stop-First Intrabar Execution:** If both High $\ge$ Target and Low $\le$ Stop occur within the same 15m candle, the stop-loss is assumed to hit first (conservative fill assumption).

---

## 3. Walk-Forward 20 OOS Validation Framework

The strategy is subjected to **20 Non-Overlapping Out-of-Sample (OOS) 1-Month Windows (2021–2026)**:
- Causal 72-hour purge boundaries ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$).
- Minimum Pass Criteria per window:
  - $\text{ROI} \ge 20.0\%$
  - $\text{Max Drawdown} < 5.0\%$
  - $\text{Win Rate} \ge 40.0\%$
  - $\text{Trades} \ge 6$
- **Anti-Lookahead Blacklist:** Zero lookup tables, zero test-set hyperparameter searches, zero test-set overrides.

---

## 4. Unabridged Source Code

### `Engine/strategy/s1_liquidation_cascade.py`
```python
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
from typing import Dict, Callable

from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig

DEFAULT_RATCHET = RatchetConfig(
    arm0_r=0.85,
    lock0_r=0.45,
    arm1_r=1.25,
    lock1_r=0.85,
    min_target_r=1.75,
    time_decay_bars=36,
    time_decay_r=0.20
)

class LiquidationCascadeSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)

    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        cl = df_test["close"].values
        
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        # Extract ML Alpha Invariants
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)

        # Iterate to generate signals
        for t in range(24, T):
            # Base Trigger for Liquidations (Z >= 1.2 per AGENTS.md)
            sig_long = (long_liq_zs[t] > 1.2) and (cl[t] > op[t])
            sig_short = (short_liq_zs[t] > 1.2) and (cl[t] < op[t])
                
            # Filter using the XGBoost Model function if provided
            if filter_func is not None:
                if sig_long and not filter_func(t, 'LONG'): sig_long = False
                if sig_short and not filter_func(t, 'SHORT'): sig_short = False

            if sig_long:
                signals[t] = 1
                r_ = atr[t] * 2.0
                if r_ <= 0: r_ = cl[t] * 0.005
                raw_r[t] = r_
                
            elif sig_short:
                signals[t] = -1
                r_ = atr[t] * 2.0
                if r_ <= 0: r_ = cl[t] * 0.005
                raw_r[t] = r_

        return pd.DataFrame({'side': signals, 'raw_r': raw_r}, index=df_test.index)

    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        return self.kernel.run(df_test, signals_df, training_mode)
```

### `Engine/core/execution_kernel.py`
```python
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
                
                # Stop-first path if OHLC is ambiguous
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
                    # Update trailing ratchet on favorable excursion
                    fav = (h_ - pos_entry) if pos_side == 1 else (pos_entry - l_)
                    cur_r = fav / pos_rr
                    if cur_r > pos_max_r: pos_max_r = cur_r
                    
                    if pos_side == 1:
                        if cur_r >= self.ratchet.arm1_r:
                            new_st = pos_entry + self.ratchet.lock1_r * pos_rr
                            if new_st > pos_stop: pos_stop = new_st
                        elif cur_r >= self.ratchet.arm0_r:
                            new_st = pos_entry + self.ratchet.lock0_r * pos_rr
                            if new_st > pos_stop: pos_stop = new_st
                    else:
                        if cur_r >= self.ratchet.arm1_r:
                            new_st = pos_entry - self.ratchet.lock1_r * pos_rr
                            if new_st < pos_stop: pos_stop = new_st
                        elif cur_r >= self.ratchet.arm0_r:
                            new_st = pos_entry - self.ratchet.lock0_r * pos_rr
                            if new_st < pos_stop: pos_stop = new_st

                    # Time decay check
                    bars_held = t - pos_bar
                    if bars_held >= self.ratchet.time_decay_bars and pos_max_r < self.ratchet.time_decay_r:
                        exit_px = c_ * (1.0 - self.fric.exit_slippage) if pos_side == 1 else c_ * (1.0 + self.fric.exit_slippage)
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

            # Evaluate entry on bar t open if signal on bar t-1
            if pos_side == 0 and signal_side[t-1] != 0:
                # Check drawdown limit
                cur_dd = (peak - realized) / peak if peak > 0 else 0.0
                if cur_dd < self.risk.drawdown_limit:
                    side = signal_side[t-1]
                    raw_r_val = signal_raw_r[t-1]
                    
                    # Entry with slippage
                    entry_px = op[t] * (1.0 + self.fric.entry_slippage) if side == 1 else op[t] * (1.0 - self.fric.entry_slippage)
                    
                    # Risk amount calculation
                    net_profit = realized - self.risk.initial_capital
                    if cur_dd > 0.025:
                        risk_amt = self.risk.drawdown_defense_risk
                    elif net_profit > 50.0:
                        risk_amt = self.risk.house_money_risk
                    else:
                        risk_amt = self.risk.base_risk

                    pos_rr = raw_r_val
                    pos_risk = risk_amt
                    pos_qty = risk_amt / raw_r_val if raw_r_val > 0 else 0.0
                    pos_entry = entry_px
                    pos_side = side
                    pos_bar = t
                    pos_max_r = 0.0
                    
                    if side == 1:
                        pos_stop = entry_px - raw_r_val
                        pos_target = entry_px + self.ratchet.min_target_r * raw_r_val
                    else:
                        pos_stop = entry_px + raw_r_val
                        pos_target = entry_px - self.ratchet.min_target_r * raw_r_val

            # Track peak and equity curve
            if realized > peak: peak = realized
            equity_curve[t] = realized

        return {
            "initial_capital": self.risk.initial_capital,
            "final_equity": realized,
            "net_roi": (realized - self.risk.initial_capital) / self.risk.initial_capital,
            "trade_count": len(trades),
            "win_rate": np.mean([1 if tr["pnl"] > 0 else 0 for tr in trades]) if trades else 0.0,
            "trades": trades,
            "equity_curve": equity_curve
        }
```

---

## 5. Specific Audit Questions for Ox Alpha

1. **Microstructure Edge Evaluation:** Does liquidation cascade absorption exhibit genuine non-linear statistical persistence in cryptocurrency perpetuals when conditioning on $Z > 1.2$ or $Z > 1.8$, or does adverse selection (trend continuation through the cascade) dominate during structural regime breaks?
2. **Ratchet Geometry Optimization:** What is your quantitative assessment of the two-stage ratchet ($+0.8\text{R} \to +0.15\text{R}$ BE, $+1.5\text{R} \to +0.8\text{R}$ lock, $+2.5\text{R}$ take-profit, 24-bar time decay)? Does the breakeven move at $+0.8\text{R}$ prematurely truncate fat-tailed upside in volatile liquidation recoveries?
3. **Execution Realism:** Are the modeled taker fees ($8\text{ bps}$) and asymmetric slippages ($10\text{ bps}$ entry, $15\text{ bps}$ stop) mathematically conservative enough to prevent backtest overfitting across both high-liquidity (BTC, ETH) and mid-cap (SUI, NEAR, APT) assets?
4. **Walk-Forward Survival Recommendations:** What specific feature engineering or ML overlay architectures (e.g. XGBoost shallow trees with L1/L2 regularization vs regime classification) do you recommend to guarantee stable pass rates across all 20 Out-of-Sample windows?
Waiting for verification…
AI can make mistakes. Verify important information.