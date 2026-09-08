# Ox Alpha Strategy Review — Strategy 8: SMC Marci Engine
**Target:** Institutional Quantitative Review & Bollinger Bands / Pullback Break Alpha Audit  
**Strategy File:** `Engine/strategy/smc_marci.py`  
**Execution Kernel:** `Engine/core/execution_kernel.py`  
**Dataset Grounding:** Binance 15-Minute Dual-Table Master Dataset (Certified 98/100 by Ox Alpha)  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Archetype

### Strategy Thesis: Bollinger Bands Oversold / Overbought Pullback & Structural Fractal Reclaim
SMC Marci captures trend-continuation re-entries after shallow or deep mean-reversion counter-trend pullbacks:
1. **Macro Trend Identification:**
   - Evaluates higher-timeframe momentum via 200-period Exponential Moving Average direction:
     $$\text{Trend}_{\text{UP}} = \text{EMA}_{200}(t) \ge \text{EMA}_{200}(t-12)$$
     $$\text{Trend}_{\text{DOWN}} = \text{EMA}_{200}(t) \le \text{EMA}_{200}(t-12)$$
2. **Dynamic Volatility Bands (Bollinger Bands 20, 2):**
   - 20-period rolling mean and 2-standard-deviation bands:
     $$\text{BB}_{\text{Mid}} = \text{SMA}_{20}(C), \quad \text{BB}_{\text{Upper}} = \text{BB}_{\text{Mid}} + 2\sigma, \quad \text{BB}_{\text{Lower}} = \text{BB}_{\text{Mid}} - 2\sigma$$
   - In an uptrend, pullbacks that pierce the Lower Band ($\text{Low} \le \text{BB}_{\text{Lower}}$) or create extreme VWAP stretch ($\text{vwap\_zscore} < -0.6$) represent discount liquidity pricing.
3. **Institutional Absorption & Liquidation Exhaustion:**
   - Pullback must show evidence of retail stop liquidation or spot market absorption:
     $$\text{long\_liq\_zs} > 0.8 \quad \lor \quad \text{zc\_div} > 0.3$$
4. **Fractal Swing Low Reclaim & Momentum Trigger:**
   - Validates that the selling momentum has terminated:
     - Swing low formed at $t-1$: $\text{Low}_{t-1} < \text{Low}_{t-2}$
     - Current bar reclaims swing high and closes bullish: $\text{Close}_t > \text{High}_{t-1} \;\land\; \text{Close}_t > \text{Open}_t$
5. **Dynamic Structural Invalidation Stop:**
   $$\text{Stop Distance}_{\text{LONG}} = (\text{Close}_t - \text{Low}_{t-1}) + 0.1 \times \text{ATR}_{14}(t)$$
   Clamped between $[0.6\% \times \text{Price}, \; 1.5 \times \text{ATR}_{14}]$.

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
- **Phase 0:** At $+0.70\text{R}$ price gain, lock $+0.20\text{R}$ in profit.
- **Phase 1:** At $+1.20\text{R}$ price gain, lock $+0.70\text{R}$ in profit.
- **Target Exit:** Fixed exit at $+1.80\text{R}$.
- **Time Decay Invalidation:** If trade fails to reach $+0.20\text{R}$ within 40 bars (10.0 hours), exit at market.

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
- **Zero Lookahead Mandate:** No lookup tables, no in-run test parameter searches.

---

## 4. Unabridged Source Code

### `Engine/strategy/smc_marci.py`
```python
\"\"\"
================================================================================
SMC MARCI ENGINE (Bollinger Bands + Trendline / Pullback Break)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Uses Bollinger Bands and fractal pullbacks to resume primary trend:
- Identifies primary trend via EMA 200 direction.
- Detects oversold/overbought pullback into Bollinger Bands + VWAP stretch.
- Waits for fractal swing low/high confirmation and momentum reclaim.
- Structural invalidation stop with mean-reversion ratchet.
================================================================================
\"\"\"

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Callable
from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig

DEFAULT_RATCHET = RatchetConfig(
    arm0_r=0.7,
    lock0_r=0.20,
    arm1_r=1.2,
    lock1_r=0.70,
    min_target_r=1.8,
    time_decay_bars=40,
    time_decay_r=0.20
)

class SMCMarciSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        ema200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        long_liq = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        
        # Calculate Bollinger Bands (20, 2)
        close_series = pd.Series(cl)
        bb_mid = close_series.rolling(window=20).mean().values
        bb_std = close_series.rolling(window=20).std(ddof=0).values
        bb_upper = bb_mid + (2 * bb_std)
        bb_lower = bb_mid - (2 * bb_std)
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        for t in range(25, T):
            trend_up = ema200[t] >= ema200[t-12]
            trend_down = ema200[t] <= ema200[t-12]
            
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            # Long Setup:
            # 1. Primary trend is UP
            # 2. Pullback dipped below or touched lower BB (or oversold vwap_z < -0.6) within past 3 bars
            # 3. Trapped liquidations or divergence: long_liq > 0.8 or zc_div > 0.3
            # 4. Swing low formed at t-1 (lo[t-1] < lo[t-2]) and current candle reclaims (cl[t] > hi[t-1] and cl[t] > op[t])
            was_oversold = (lo[t-1] <= bb_lower[t-1]) or (lo[t-2] <= bb_lower[t-2]) or (vwap_z[t-1] < -0.6)
            has_absorption_l = (long_liq[t-1] > 0.8) or (long_liq[t] > 0.8) or (zc_div[t] > 0.3)
            
            if trend_up and was_oversold and has_absorption_l:
                if lo[t-1] < lo[t-2] and cl[t] > hi[t-1] and cl[t] > op[t]:
                    sig_long = True
                    s_dist = (cl[t] - lo[t-1]) + 0.1 * atr[t]
                    s_dist = max(s_dist, cl[t] * 0.006)
                    s_dist = min(s_dist, atr[t] * 1.5)
                    stop_dist = s_dist
                    
            # Short Setup:
            # 1. Primary trend is DOWN
            # 2. Rally reached upper BB or overbought vwap_z > 0.6
            # 3. Trapped short liquidations or negative divergence
            # 4. Swing high formed at t-1 and current candle breaks lower
            was_overbought = (hi[t-1] >= bb_upper[t-1]) or (hi[t-2] >= bb_upper[t-2]) or (vwap_z[t-1] > 0.6)
            has_absorption_s = (short_liq[t-1] > 0.8) or (short_liq[t] > 0.8) or (zc_div[t] < -0.3)
            
            if trend_down and was_overbought and has_absorption_s:
                if hi[t-1] > hi[t-2] and cl[t] < lo[t-1] and cl[t] < op[t]:
                    sig_short = True
                    s_dist = (hi[t-1] - cl[t]) + 0.1 * atr[t]
                    s_dist = max(s_dist, cl[t] * 0.006)
                    s_dist = min(s_dist, atr[t] * 1.5)
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

1. **Statistical Edge of Bollinger Band Pullback Reclaims:** Does entering upon the reclaim of a swing point following a Bollinger Band or VWAP puncture yield a genuine predictive edge in crypto perpetuals, or is the edge predominantly concentrated during strong trend regimes?
2. **Ratchet Geometry ($+0.7\text{R} \to +0.2\text{R}$, $+1.2\text{R} \to +0.7\text{R}$, $+1.8\text{R}$ TP):** Given the pullback nature of Marci setups, is a tighter $+1.8\text{R}$ target mathematically superior to wider $+2.5\text{R}$ targets for maximizing Sharpe ratio and minimizing time in market?
3. **Absorption Confluence Thresholds:** Are `long_liq > 0.8` or `zc_div > 0.3` sufficient to filter false breakouts, or should footprint delta imbalances (e.g. `is_stacked_buy_imb`) be enforced as mandatory confluence?
4. **Walk-Forward Invariance:** Across the 20 OOS windows (ranging from 2021 bull runs to 2022 deleveraging and 2024 ATHs), what specific regime-conditioning filters would you add to avoid adverse selection in choppy consolidation regimes?
