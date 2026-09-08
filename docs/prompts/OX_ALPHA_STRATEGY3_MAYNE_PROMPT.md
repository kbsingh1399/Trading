# Ox Alpha Strategy Review — Strategy 3: SMC Trader Mayne Engine
**Target:** Institutional Quantitative Review & Smart Money Concepts (SMC) Alpha Audit  
**Strategy File:** `Engine/strategy/smc_mayne.py` & `Engine/core/execution_kernel.py`  
**Dataset Grounding:** Binance 15-Minute Dual-Table Master Dataset (Certified 98/100 by Ox Alpha)  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Archetype

### HTF Trend Alignment & Breaker Block Mitigation Mechanics
SMC Trader Mayne models institutional order flow dynamics through structural interactions between Higher-Timeframe (HTF) trend regimes and Lower-Timeframe (LTF) Breaker Blocks:
1. **Trend & Macro Regime Governance:**
   - Bullish regime: $\text{EMA}_{200}(t) \ge \text{EMA}_{200}(t-12)$ (positive 3-hour slope).
   - Bearish regime: $\text{EMA}_{200}(t) \le \text{EMA}_{200}(t-12)$ (negative 3-hour slope).
2. **Breaker Block Formation Mechanics:**
   - **Bullish Breaker:** A swing high is formed in $[t-12, t-4]$. Price conducts a stop run below the prior swing low in $[t-4, t-1]$, trapping retail short sellers. A high-displacement candle then breaks cleanly above the swing high ($C_{t-1} > \text{SwingHigh}$) with volume expansion ($\text{volume\_ratio} > 1.2$) or short liquidation distress ($\text{short\_liq\_zs} > 0.8$). The former resistance zone flips into institutional support.
   - **Bearish Breaker:** A swing low is formed in $[t-12, t-4]$. Price sweeps liquidity above prior swing highs in $[t-4, t-1]$, followed by an aggressive breakdown below the swing low ($C_{t-1} < \text{SwingLow}$) with volume expansion or long liquidation distress. Former support flips into institutional resistance.
3. **Mitigation & Retest Entry:**
   - Entry triggers upon pullback to retest the Breaker Block zone within 48 bars (12 hours).
   - Confirmation requires candle color alignment (green close for longs, red for shorts) alongside contemporaneous microstructure absorption ($\text{long\_liq\_zs} > 0.8$, $\text{zc\_div} > 0.3$, $\text{vwap\_zscore} < -0.4$, or $\text{volume\_ratio} > 1.2$).
4. **Structural Invalidation Stop:**
   - Stops are pegged outside the structural Breaker Block boundary:
     $$\text{Stop Distance}_{\text{LONG}} = (C_t - \text{Breaker}_{\text{bottom}}) + 0.2 \times \text{ATR}_{14}(t)$$
     clamped strictly within $[1.5 \times \text{ATR}_{14}, \; 2.5 \times \text{ATR}_{14}]$.

---

## 2. Quantitative Strategy Invariants

### 2.1 Microstructure Exit Ratchet
- **Phase 0 (Aggressive Lock):** At $+0.85\text{R}$ price gain, lock $+0.45\text{R}$ in profit.
- **Phase 1 (Extended Lock):** At $+1.25\text{R}$ price gain, lock $+0.85\text{R}$ in profit.
- **Target Exit:** Fixed exit at $+1.75\text{R}$.
- **Time Decay Invalidation:** If trade fails to reach $+0.20\text{R}$ within 36 bars (9.0 hours), exit at market.
- **Causal Execution:** Stops armed at bar $j$ close take effect at bar $j+1$ open only.

### 2.2 Risk Budget & Portfolio Governance
- **Initial Capital:** $5,000.00 USD.
- **Base Risk Budget:** $25.00 USD per trade ($0.50\%$ of equity).
- **House Money Tier:** $50.00 USD ($1.00\%$ max 2× risk when net session profits $> \$50.00$).
- **Drawdown Defense Tier:** $15.00 USD ($0.30\%$ risk when drawdown exceeds $2.5\%$).
- **Hard Drawdown Stop:** $4.50\%$ ($225.00 USD hard stop, trading ceases for the period).
- **Portfolio Concurrency:** Maximum 2 simultaneous open positions across all 18 symbols.

### 2.3 Transaction Frictions & Execution Realism
- **Taker Fees:** 8 basis points ($0.08\%$) on both entry and exit.
- **Entry Slippage:** 10 basis points ($0.10\%$) against trade direction.
- **Exit Slippage (Stop / Market):** 15 basis points ($0.15\%$) against trade direction.
- **Conservative Intrabar Fills:** Stop-first resolution if OHLC range breaches both stop and target within the same 15m bar.

---

## 3. Walk-Forward 20 OOS Validation Framework

Evaluated across **20 Non-Overlapping Out-of-Sample (OOS) Windows (2021–2026)**:
- Windows 1–4 (2021), 5–8 (2022), 9–12 (2023), 13–16 (2024), 17–20 (2025).
- Causal 72h purge boundary: $t_{\text{purge}} = t_{\text{start}} - 72\text{h}$.
- **Pass Criteria per Window:** $\text{ROI} \ge 20.0\%$, $\text{MaxDD} < 5.0\%$, $\text{Win Rate} \ge 40.0\%$, $\text{Trades} \ge 6$.
- **Anti-Lookahead Blacklist:** Zero lookup tables, zero test-set parameter sweeps, zero test-set overrides.

---

## 4. Core Implementation Architecture

```python
# Breaker block detection and retest logic
for t in range(24, T):
    # Bullish Breaker detection
    sw_hi = np.max(hi[t-12:t-4]); sw_lo = np.min(lo[t-4:t-1])
    if cl[t-1] > sw_hi and op[t-1] <= sw_hi and (vol_ratio[t-1] > 1.2 or short_liq_zs[t-1] > 0.8):
        breaker_blocks.append({"top": sw_hi, "bottom": max(sw_hi - 0.5*atr[t], sw_lo), "type": 1, "age": 0})
    
    # Retest and mitigation within 48 bars
    for bb in breaker_blocks:
        if bb["age"] > 0 and bb["type"] == 1 and trend_up and has_absorption_l:
            if lo[t] <= bb["top"] and cl[t] >= bb["bottom"] and cl[t] > op[t]:
                signals[t] = 1
                raw_r[t] = np.clip((cl[t] - bb["bottom"]) + 0.2*atr[t], 1.5*atr[t], 2.5*atr[t])
                bb["age"] = 999; break

return kernel.run(df_test, signals_df, training_mode)
```

---

## 5. Specific Audit Questions for Ox Alpha

1. **Breaker Block Mathematical Formulation:** Does tracking swing highs/lows over rolling $[t-12, t-4]$ and $[t-4, t-1]$ windows accurately capture true institutional market structure breaks (MSB) on 15-minute crypto futures, or does it generate excessive false positives during choppy consolidation?
2. **Breaker Expiration & Zone Lifetime:** Active Breaker Blocks are aged up to 48 bars (12 hours). From a microstructure and order book liquidity perspective, does an unmitigated breaker block retain significant institutional resting liquidity after 12 hours, or should the half-life be dynamically scaled by volatility/volume turnover?
3. **Stop Calibration Dynamics:** Invalidation stops are anchored to $\text{Breaker}_{\text{boundary}} + 0.2 \times \text{ATR}$, clamped within $[1.5, 2.5] \times \text{ATR}$. Does this dynamic structural stop provide superior risk-adjusted return compared to purely volatility-based (ATR) stops?
4. **Walk-Forward Regime Adaptation:** In volatile bull run phases (e.g. Q1/Q4 2021, Q1 2024), does the $\text{EMA}_{200}$ trend requirement cause lag or missed reversals during parabolic blow-off tops? What adjustments do you advise for regime agility?
