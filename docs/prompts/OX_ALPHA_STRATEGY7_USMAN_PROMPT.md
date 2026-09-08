# Ox Alpha Strategy Review — Strategy 7: SMC Usman Noah Engine
**Target:** Institutional Quantitative Review & Daily High/Low (PDH/PDL) Liquidity Sweep Alpha Audit  
**Strategy File:** `Engine/strategy/smc_usman_noah.py`  
**Execution Kernel:** `Engine/core/execution_kernel.py`  
**Dataset Grounding:** Binance 15-Minute Dual-Table Master Dataset (Certified 98/100 by Ox Alpha)  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Archetype

### Strategy Thesis: Previous Day High / Low (PDH/PDL) Liquidity Sweeps & Structural Reclaims
SMC Usman Noah capitalizes on the liquidity distribution surrounding daily session boundaries:
1. **Daily Liquidity Anchors (PDH & PDL):**
   - The Previous Day High (PDH) and Previous Day Low (PDL) represent the single most heavily watched liquidity reference levels across global institutional and retail order books.
   - Buy stops accumulate above PDH; sell stops accumulate below PDL.
2. **False Breakout Sweep Dynamics:**
   - Price temporarily exceeds PDH or drops below PDL during high-volatility session opens (London / New York turnover).
   - Rather than continuing directionally, aggressive market orders trigger retail liquidity, allowing informed market makers to fill counter-trend inventory.
3. **The 8-Bar Structural Reclaim Window:**
   - Once a sweep occurs ($\text{Low}_t < \text{PDL}$ or $\text{High}_t > \text{PDH}$), the market must validate the trap by reclaiming back inside the prior day's range within 8 bars (2.0 hours):
     - **Bullish PDL Reclaim:** $\text{Close}_t > \text{PDL}$ and $C_t > O_t$, accompanied by institutional absorption ($\text{long\_liq\_zs}_t > 0.8$, $\text{zc\_div}_t > 0.3$, $\text{vwap\_zscore}_t < -0.4$, or $\text{volume\_ratio}_t > 1.2$) and HTF trend alignment ($\text{EMA}_{200}(t) \ge \text{EMA}_{200}(t-12)$).
     - **Bearish PDH Reclaim:** $\text{Close}_t < \text{PDH}$ and $C_t < O_t$, accompanied by absorption ($\text{short\_liq\_zs}_t > 0.8$, $\text{zc\_div}_t < -0.3$, $\text{vwap\_zscore}_t > 0.4$, or $\text{volume\_ratio}_t > 1.2$) and downtrend alignment.
4. **Structural Invalidation Stop:**
   - Stop-loss is positioned beyond the extreme of the sweep:
     $$\text{Stop Distance}_{\text{LONG}} = (C_t - \min_{\text{sweep}} L) + 0.2 \times \text{ATR}_{14}(t)$$
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

### `Engine/strategy/smc_usman_noah.py`
```python
"""
================================================================================
SMC USMAN NOAH ENGINE (PDH/PDL Sweep + Reclaim)
================================================================================
Institutional quantitative strategy for Binance USDT-M Perpetuals (15m).
Based on Usman Noah's ICT Daily Liquidity Framework:
- Dynamically tracks Previous Day High (PDH) and Previous Day Low (PDL).
- Detects false breakout liquidity sweeps beyond PDH/PDL.
- Enters on structural reclaim with institutional volume/liquidation confirmation.
- Structural invalidation stop with mean-reversion ratchet.
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

class SMCUsmanNoahSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        # Parse timestamp to track daily boundaries
        dt = pd.to_datetime(df_test.get("datetime_utc", df_test.get("datetime", pd.Series(df_test.index))))
        if hasattr(dt, 'dt') and hasattr(dt.dt, 'date'):
            days = dt.dt.date.values
        else:
            days = np.arange(T) // 96 # Fallback to 96 bars per 24h
            
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        vol_ratio = df_test.get("volume_ratio", pd.Series(np.ones(T))).values
        ema_200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        pdh, pdl = -1.0, float('inf')
        current_dh, current_dl = hi[0], lo[0]
        
        swept_pdl_bar = -1
        swept_pdh_bar = -1
        
        for t in range(25, T):
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
            
            # Day change detection
            if days[t] != days[t-1]:
                pdh = current_dh
                pdl = current_dl
                current_dh = hi[t]
                current_dl = lo[t]
                swept_pdl_bar = -1
                swept_pdh_bar = -1
            else:
                if hi[t] > current_dh: current_dh = hi[t]
                if lo[t] < current_dl: current_dl = lo[t]
                
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            has_absorption_l = (long_liq_zs[t] > 0.8) or (zc_div[t] > 0.3) or (vwap_z[t] < -0.4) or (vol_ratio[t] > 1.2)
            has_absorption_s = (short_liq_zs[t] > 0.8) or (zc_div[t] < -0.3) or (vwap_z[t] > 0.4) or (vol_ratio[t] > 1.2)
            
            if pdh != -1.0 and pdl != float('inf'):
                # PDL Sweep detection
                if lo[t] < pdl:
                    swept_pdl_bar = t
                # PDH Sweep detection
                if hi[t] > pdh:
                    swept_pdh_bar = t
                    
                # Bullish PDL Reclaim: Swept PDL within last 8 bars, now reclaims above PDL
                if swept_pdl_bar != -1 and (t - swept_pdl_bar) <= 8 and (t - swept_pdl_bar) >= 0:
                    if cl[t] > pdl and cl[t] > op[t] and trend_up and has_absorption_l:
                        sig_long = True
                        lowest_sweep = np.min(lo[swept_pdl_bar:t+1])
                        s_dist = (cl[t] - lowest_sweep) + 0.2 * atr[t]
                        s_dist = max(s_dist, atr[t] * 1.5)
                        s_dist = min(s_dist, atr[t] * 2.5)
                        stop_dist = s_dist
                        swept_pdl_bar = -1
                        
                # Bearish PDH Reclaim: Swept PDH within last 8 bars, now rejects back below PDH
                if swept_pdh_bar != -1 and (t - swept_pdh_bar) <= 8 and (t - swept_pdh_bar) >= 0:
                    if cl[t] < pdh and cl[t] < op[t] and trend_down and has_absorption_s:
                        sig_short = True
                        highest_sweep = np.max(hi[swept_pdh_bar:t+1])
                        s_dist = (highest_sweep - cl[t]) + 0.2 * atr[t]
                        s_dist = max(s_dist, atr[t] * 1.5)
                        s_dist = min(s_dist, atr[t] * 2.5)
                        stop_dist = s_dist
                        swept_pdh_bar = -1
                        
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

1. **Daily Session Boundary Definition:** In crypto markets operating 24/7/365, UTC midnight (00:00 UTC) is used as the daily boundary. Do specific assets exhibit stronger liquidity sweep dynamics around traditional traditional financial market session closes (e.g. New York 5:00 PM EST / 21:00 UTC or CME futures open)?
2. **Reclaim Horizon (8 bars / 2.0 hours):** S7 allows up to 8 bars after a sweep for the price to reclaim the level. Does a prolonged sweep (> 4 bars) below PDL indicate genuine institutional expansion rather than a liquidity trap, increasing adverse selection?
3. **Multi-Day Levels (PWH / PWL):** Would incorporating Previous Week High (PWH) and Previous Week Low (PWL) as higher-tier liquidity pools provide better regime stability during strong multi-week trends?
4. **Walk-Forward Invariance & Overfitting:** Because PDH/PDL are deterministic calendar-based levels requiring 0 fitted parameters, does S7 present the lowest risk of parameter overfitting across the 20 OOS windows?
