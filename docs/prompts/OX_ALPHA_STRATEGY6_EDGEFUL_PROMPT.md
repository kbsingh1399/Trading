# Ox Alpha Strategy Review — Strategy 6: SMC Edgeful FVG Engine
**Target:** Institutional Quantitative Review & Fair Value Gap (FVG) Alpha Audit  
**Strategy File:** `Engine/strategy/smc_edgeful.py`  
**Execution Kernel:** `Engine/core/execution_kernel.py`  
**Dataset Grounding:** Binance 15-Minute Dual-Table Master Dataset (Certified 98/100 by Ox Alpha)  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Archetype

### Strategy Thesis: Institutional Displacement & Fair Value Gap (FVG) Mitigation
SMC Edgeful models high-momentum order flow imbalances through 3-candle Fair Value Gap mechanics:
1. **Institutional Displacement & Imbalance Creation:**
   - Sudden aggressive institutional buying or selling creates an execution void where continuous two-sided liquidity was not matched.
   - **Bullish FVG (Buy-Side Imbalance):** The low of candle $t$ remains strictly higher than the high of candle $t-2$ ($L_t > H_{t-2}$), creating an unmitigated vacuum between $H_{t-2}$ (bottom) and $L_t$ (top). The intermediate candle $t-1$ represents an expansion candle confirmed by volume expansion ($\text{volume\_ratio}_{t-1} > 1.3$) or short liquidation panic ($\text{short\_liq\_zs}_{t-1} > 0.8$).
   - **Bearish FVG (Sell-Side Imbalance):** The high of candle $t$ remains strictly lower than the low of candle $t-2$ ($H_t < L_{t-2}$), leaving a vacuum between $H_t$ (bottom) and $L_{t-2}$ (top), confirmed by volume expansion ($\text{volume\_ratio}_{t-1} > 1.3$) or long liquidation distress ($\text{long\_liq\_zs}_{t-1} > 0.8$).
2. **Fair Value Gap Mitigation Phase:**
   - Active FVGs are tracked for up to 36 bars (9.0 hours).
   - Entry triggers upon the first retest / pullback into the gap:
     - **Long Mitigation:** In an uptrend ($\text{EMA}_{200}(t) \ge \text{EMA}_{200}(t-12)$), price dips into the gap ($L_t \le \text{FVG}_{\text{top}}$), respects the boundary ($C_t > \text{FVG}_{\text{bottom}}$), and closes green ($C_t > O_t$).
     - **Short Mitigation:** In a downtrend ($\text{EMA}_{200}(t) \le \text{EMA}_{200}(t-12)$), price rallies into the gap ($H_t \ge \text{FVG}_{\text{bottom}}$), respects the boundary ($C_t < \text{FVG}_{\text{top}}$), and closes red ($C_t < O_t$).
3. **Structural Invalidation Stop:**
   - Stop-loss is positioned strictly behind the originating boundary of the imbalance:
     $$\text{Stop Distance}_{\text{LONG}} = (C_t - \text{FVG}_{\text{bottom}}) + 0.2 \times \text{ATR}_{14}(t)$$
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

### `Engine/strategy/smc_edgeful.py`
```python
"""
================================================================================
SMC EDGEFUL FVG ENGINE (15m FVG Mitigation)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Based on Edgeful FVG mechanics:
- Detects institutional displacement (FVG creation with volume/liquidation tail).
- Waits for retest/mitigation of the Fair Value Gap.
- Enforces structural invalidation stop loss and mean-reversion ratchet.
================================================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Callable, Dict
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

class SMCEdgefulSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        long_liq = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        vol_ratio = df_test.get("volume_ratio", pd.Series(np.ones(T))).values
        ema_200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        active_fvgs = []
        
        for t in range(24, T):
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
            
            # Age active FVGs
            for fvg in active_fvgs:
                fvg["age"] += 1
                
            # 1. Detect Institutional FVG Creation (Displacement with volume/liquidation tail)
            # Bullish FVG: candle t-1 jumped up leaving a gap between hi[t-2] and lo[t]
            if lo[t] > hi[t-2] and cl[t-1] > op[t-1] and (short_liq[t-1] > 0.8 or vol_ratio[t-1] > 1.3):
                active_fvgs.append({"top": lo[t], "bottom": hi[t-2], "type": 1, "age": 0})
                
            # Bearish FVG: candle t-1 plunged down leaving a gap between lo[t-2] and hi[t]
            if hi[t] < lo[t-2] and cl[t-1] < op[t-1] and (long_liq[t-1] > 0.8 or vol_ratio[t-1] > 1.3):
                active_fvgs.append({"top": lo[t-2], "bottom": hi[t], "type": -1, "age": 0})
                
            # Only keep unmitigated FVGs up to 36 bars old (9 hours)
            active_fvgs = [f for f in active_fvgs if f["age"] <= 36]
            
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            for fvg in active_fvgs:
                if fvg["age"] > 0:
                    # Bullish mitigation: price tests FVG top, holds bottom, and closes green in an uptrend
                    if fvg["type"] == 1 and trend_up:
                        if lo[t] <= fvg["top"] and cl[t] > fvg["bottom"] and cl[t] > op[t]:
                            sig_long = True
                            # Invalidation stop placed below FVG bottom + 0.2 ATR
                            s_dist = (cl[t] - fvg["bottom"]) + 0.2 * atr[t]
                            s_dist = max(s_dist, atr[t] * 1.5)
                            s_dist = min(s_dist, atr[t] * 2.5)
                            stop_dist = s_dist
                            fvg["age"] = 999
                            break
                    # Bearish mitigation: price tests FVG bottom, holds top, and closes red in a downtrend
                    elif fvg["type"] == -1 and trend_down:
                        if hi[t] >= fvg["bottom"] and cl[t] < fvg["top"] and cl[t] < op[t]:
                            sig_short = True
                            s_dist = (fvg["top"] - cl[t]) + 0.2 * atr[t]
                            s_dist = max(s_dist, atr[t] * 1.5)
                            s_dist = min(s_dist, atr[t] * 2.5)
                            stop_dist = s_dist
                            fvg["age"] = 999
                            break
                            
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

1. **FVG Gap Threshold & Minimum Width:** Currently, any gap where $L_t > H_{t-2}$ is classified as an FVG if volume ratio $> 1.3$ or liquidation $Z > 0.8$. In low-volatility regimes, does this generate micro-gaps that lack institutional resting interest? Should a minimum gap width (e.g. $\ge 0.5 \times \text{ATR}$) be required?
2. **Mitigation Depth (Touch vs Consequent Encroachment):** S6 triggers entry upon touch of the FVG outer boundary ($L_t \le \text{FVG}_{\text{top}}$). In institutional order flow, does entry at Consequent Encroachment (the $50\%$ midpoint of the FVG) significantly improve entry price and reduce stop distance without causing excessive missed trades?
3. **FVG Invalidation vs Inversion:** When an FVG fails to hold and is cleanly breached ($C_t < \text{FVG}_{\text{bottom}}$), it is aged out (`fvg['age'] = 999`). Should failed FVGs flip into Inversion Fair Value Gaps (IFVGs) to capture trend continuation?
4. **Walk-Forward Regime Performance:** How does FVG mitigation perform during structural regime shifts (e.g. high-volatility bear market crashes in 2022 vs choppy ranges in 2023)?
