# Ox Alpha Strategy Review — Strategy 5: SMC Trader Kane Engine
**Target:** Institutional Quantitative Review & Power of 3 (PO3) Alpha Audit  
**Strategy File:** `Engine/strategy/smc_kane.py`  
**Execution Kernel:** `Engine/core/execution_kernel.py`  
**Dataset Grounding:** Binance 15-Minute Dual-Table Master Dataset (Certified 98/100 by Ox Alpha)  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Archetype

### Strategy Thesis: Power of 3 (PO3: Accumulation, Manipulation, Distribution)
SMC Trader Kane implements the classic institutional manipulation lifecycle:
1. **Accumulation Range Phase:**
   - Over a rolling 24-bar window ($t-24 \dots t-1$, 6.0 hours), the market establishes a defined consolidation range:
     $$\text{Acc}_{\text{high}} = \max_{i=1 \dots 24} H_{t-i}, \quad \text{Acc}_{\text{low}} = \min_{i=1 \dots 24} L_{t-i}$$
2. **Manipulation Phase (The Judas Swing):**
   - **Bullish Manipulation:** Price aggressively plunges below $\text{Acc}_{\text{low}}$ ($L_t < \text{Acc}_{\text{low}}$), sweeping sell-side liquidity and triggering retail breakout short orders.
   - Institutional limit buyers absorb the forced selling, driving price to close back inside the accumulation boundary ($C_t > \text{Acc}_{\text{low}}$) with a bullish hammer / pinbar configuration ($C_t > O_t$ and $C_t > \frac{H_t + L_t}{2}$).
   - **Bearish Manipulation:** Price spikes above $\text{Acc}_{\text{high}}$ ($H_t > \text{Acc}_{\text{high}}$), sweeping buy-side liquidity, absorbed by institutional sellers, and closing back below the high ($C_t < \text{Acc}_{\text{high}}$) with a shooting star rejection ($C_t < O_t$ and $C_t < \frac{H_t + L_t}{2}$).
3. **Microstructure Confluence:**
   - Long manipulation requires contemporaneous evidence of exhaustion:
     $$\text{long\_liq\_zs}_t > 0.8 \;\lor\; \text{zc\_div}_t > 0.3 \;\lor\; \text{vwap\_zscore}_t < -0.5$$
     coupled with higher-timeframe trend alignment ($\text{EMA}_{200}(t) \ge \text{EMA}_{200}(t-12)$).
   - Short manipulation requires:
     $$\text{short\_liq\_zs}_t > 0.8 \;\lor\; \text{zc\_div}_t < -0.3 \;\lor\; \text{vwap\_zscore}_t > 0.5$$
     coupled with downtrend alignment ($\text{EMA}_{200}(t) \le \text{EMA}_{200}(t-12)$).
4. **Distribution Phase & Structural Invalidation Stop:**
   - Distribution leg drives price toward the opposite range boundary.
   - Stop-loss is placed strictly below the manipulation extreme:
     $$\text{Stop Distance}_{\text{LONG}} = (C_t - L_t) + 0.2 \times \text{ATR}_{14}(t)$$
     clamped within $[1.5 \times \text{ATR}_{14}, \; 2.5 \times \text{ATR}_{14}]$.

---

## 2. Quantitative Strategy Invariants

### 2.1 Risk Budget & Portfolio Governance
- **Initial Capital:** $5,000.00 USD.
- **Base Risk Budget:** $25.00 USD per trade ($0.50\%$ of equity).
- **House Money Tier:** $50.00 USD ($1.00\%$ max 2× risk when net session profits $> \$50.00$).
- **Drawdown Defense Tier:** $15.00 USD ($0.30\%$ risk when drawdown exceeds $2.5\%$).
- **Hard Drawdown Stop:** $4.50\%$ ($225.00 USD hard stop, trading ceases for the period).
- **Portfolio Concurrency:** Maximum 2 simultaneous open positions across all 18 symbols.

### 2.2 Microstructure Exit Ratchet
- **Phase 0:** At $+0.85\text{R}$ price gain, lock $+0.45\text{R}$ in profit.
- **Phase 1:** At $+1.25\text{R}$ price gain, lock $+0.85\text{R}$ in profit.
- **Target Exit:** Fixed exit at $+1.75\text{R}$.
- **Time Decay Invalidation:** If trade fails to reach $+0.20\text{R}$ within 36 bars (9.0 hours), exit at market.

### 2.3 Transaction Frictions & Execution Realism
- **Taker Fees:** 8 basis points ($0.08\%$) on both entry and exit.
- **Entry Slippage:** 10 basis points ($0.10\%$) against trade direction.
- **Exit Slippage (Stop / Market):** 15 basis points ($0.15\%$) against trade direction.
- **Conservative Intrabar Fills:** Stop-first resolution if OHLC range breaches both stop and target within the same 15m bar.

---

## 3. Walk-Forward 20 OOS Validation Framework

Evaluated across **20 Non-Overlapping Out-of-Sample (OOS) 1-Month Windows (2021–2026)** with causal 72h purge boundaries ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$).

**Institutional Pass Criteria per Window:**
- $\text{ROI} \ge 20.0\%$
- $\text{Max Drawdown} < 5.0\%$
- $\text{Win Rate} \ge 40.0\%$
- $\text{Trades} \ge 6$

---

## 4. Unabridged Source Code

### `Engine/strategy/smc_kane.py`
```python
"""
================================================================================
SMC TRADER KANE ENGINE (Power of 3: Accumulation, Manipulation, Distribution)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Based on Trader Kane's PO3 Framework:
- Identifies 24-bar accumulation range.
- Detects the manipulation leg (liquidity sweep of the range boundary).
- Enforces institutional absorption (liquidations / orderflow divergence / rejection).
- Sizing based on structural sweep invalidation with mean-reversion ratchet.
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

class SMCKaneSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        ema_200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        for t in range(24, T):
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
            
            # Accumulation uses completed bars (t-24 to t-1)
            acc_high = np.max(hi[t-24:t])
            acc_low = np.min(lo[t-24:t])
            
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            # Long Manipulation: Price sweeps below accumulation low, absorbs liquidity,
            # and reclaims back inside the range with a bullish pinbar / hammer close
            is_liq_or_stretch = (long_liq_zs[t] > 0.8) or (zc_div[t] > 0.3) or (vwap_z[t] < -0.5)
            if lo[t] < acc_low and cl[t] > acc_low and cl[t] > op[t] and cl[t] > (hi[t] + lo[t])/2.0:
                if is_liq_or_stretch and trend_up:
                    sig_long = True
                    # Structural stop placed right below the manipulation wick + 0.2 ATR
                    s_dist = (cl[t] - lo[t]) + 0.2 * atr[t]
                    s_dist = max(s_dist, atr[t] * 1.5)
                    s_dist = min(s_dist, atr[t] * 2.5)
                    stop_dist = s_dist
                    
            # Short Manipulation: Price sweeps above accumulation high, absorbs buy-side liquidity,
            # and rejects back inside the range with a bearish pinbar / shooting star close
            is_short_liq_or_stretch = (short_liq_zs[t] > 0.8) or (zc_div[t] < -0.3) or (vwap_z[t] > 0.5)
            if hi[t] > acc_high and cl[t] < acc_high and cl[t] < op[t] and cl[t] < (hi[t] + lo[t])/2.0:
                if is_short_liq_or_stretch and trend_down:
                    sig_short = True
                    s_dist = (hi[t] - cl[t]) + 0.2 * atr[t]
                    s_dist = max(s_dist, atr[t] * 1.5)
                    s_dist = min(s_dist, atr[t] * 2.5)
                    stop_dist = s_dist
                    
            if filter_func is not None:
                if sig_long and not filter_func(t, 'LONG'): sig_long = False
                if sig_short and not filter_func(t, 'SHORT'): sig_short = False
                
            if sig_long and not sig_short:
                signals[t] = 1
                raw_r[t] = stop_dist
            elif sig_short and not sig_long:
                signals[t] = -1
                raw_r[t] = stop_dist
                
        return pd.DataFrame({'side': signals, 'raw_r': raw_r}, index=df_test.index)
        
    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        return self.kernel.run(df_test, signals_df, training_mode)
```

---

## 5. Specific Audit Questions for Ox Alpha

1. **Fixed Window vs Dynamic Consolidation:** The accumulation phase uses a static 24-bar (6-hour) window. Does crypto perpetual market microstructure benefit from volatility-adaptive accumulation windows (e.g. Bollinger Band Width or ATR compression filters) to distinguish true range-bound accumulation from trending momentum pauses?
2. **Judas Swing False Breakout Invalidation:** Kane's PO3 relies heavily on the single-candle reclaim ($C_t > \text{Acc}_{\text{low}}$ and $C_t > \frac{H_t + L_t}{2}$). In cascading sell-offs, does this rule create premature entries into multi-leg liquidation spills? What additional order book absorption filters are recommended?
3. **Target Selection ($+1.75\text{R}$ vs Opposite Range Boundary):** In discretionary PO3 trading, the target is often set to the opposite side of the accumulation range ($\text{Acc}_{\text{high}}$). S5 instead enforces a $+1.75\text{R}$ statistical target with a 2-stage ratchet. Does this fixed R:R geometry offer superior statistical stability across the 20 OOS windows?
4. **Time Decay Parameters:** S5 invalidates trades if $+0.20\text{R}$ is not achieved in 36 bars (9 hours). Is 9 hours appropriate for the distribution phase to mature in 15m crypto perpetuals?
