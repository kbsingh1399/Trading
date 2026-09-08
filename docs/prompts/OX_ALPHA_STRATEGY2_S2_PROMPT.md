# Ox Alpha Strategy Review — Strategy 2: S2 Institutional ML Alpha
**Target:** Institutional Quantitative Review & Machine Learning Alpha Audit  
**Strategy File:** `Engine/strategy/s2_institutional_ml.py` & `Engine/core/execution_kernel.py`  
**Dataset Grounding:** Binance 15-Minute Dual-Table Master Dataset (Certified 98/100 by Ox Alpha)  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Archetype

### Dual-Sided Microstructure Order Flow & ML-Gated Alpha
In institutional cryptocurrency perpetuals, structural order flow imbalances between Spot and Perpetual Futures venues reveal informed market maker positioning:
1. **Spot vs. Futures CVD Divergence ($\text{zc\_div}$):**
   - **Bullish Absorption:** When Spot CVD rises ($\Delta\text{Spot} > 0$) while Futures CVD declines ($\Delta\text{Futures} < 0$), retail/leveraged short sellers are absorbed by institutional spot accumulation ($\text{zc\_div} > 0.3$).
   - **Bearish Distribution:** When Spot CVD falls ($\Delta\text{Spot} < 0$) while Futures CVD rallies ($\Delta\text{Futures} > 0$), retail FOMO buyers are distributed into by institutional spot sellers ($\text{zc\_div} < -0.3$).
2. **Liquidation Pressure Exhaustion:**
   - Long liquidations ($\text{long\_liq\_zs} > 1.2$) drive rapid distress selling into spot support zones.
   - Short liquidations ($\text{short\_liq\_zs} > 1.2$) ignite forced short covering into spot resistance.
3. **Statistical Invariants & Oscillator Exhaustion:**
   - Longs: $\text{vwap\_zscore} < -0.4 \;\land\; \text{RSI}_{14} < 45$.
   - Shorts: $\text{vwap\_zscore} > 0.4 \;\land\; \text{RSI}_{14} > 55$.
4. **Machine Learning Overlay Interface (`filter_func`):**
   - Microstructure confluence acts as an **event-conditioned sampling trigger** ($< 2\%$ of bars).
   - An auxiliary ML model (calibrated probability estimator or shallow XGBoost) gates entry:
     $$\text{Entry Fired} \iff \text{Confluence Trigger}_t \;\land\; \mathcal{M}_{\theta}(\mathbf{x}_t) \ge \tau_t$$
   - Decouples structural trade geometry from predictive probability scoring, preventing dimensionality explosion.

---

## 2. Quantitative Strategy Invariants

### 2.1 Signal Confluence Geometry (Dual-Sided)
Causal directional signals fired at bar $t$ close, executed strictly at bar $t+1$ open:

**Long Entry:**
$$\text{long\_liq\_zs}_t > 1.2 \;\land\; \text{zc\_div}_t > 0.3 \;\land\; \Delta\text{Spot}_t > 0 \;\land\; \Delta\text{Futures}_t < 0 \;\land\; \text{RSI}_t < 45 \;\land\; \text{VWAP Z}_t < -0.4$$

**Short Entry:**
$$\text{short\_liq\_zs}_t > 1.2 \;\land\; \text{zc\_div}_t < -0.3 \;\land\; \Delta\text{Spot}_t < 0 \;\land\; \Delta\text{Futures}_t > 0 \;\land\; \text{RSI}_t > 55 \;\land\; \text{VWAP Z}_t > 0.4$$

**Stop Distance:**
$$\text{Stop Distance} = 2.0 \times \text{ATR}_{14}(t), \quad \text{clipped at } \text{ATR} \ge 0.002 \times C_t$$

### 2.2 S2 Microstructure Exit Ratchet (High-Turnover Geometry)
Optimized for high-turnover dual-sided mean-reversion flows:
- **Phase 0 (Aggressive Lock):** At $+0.85\text{R}$ price gain, lock $+0.45\text{R}$ in profit.
- **Phase 1 (Extended Lock):** At $+1.25\text{R}$ price gain, lock $+0.85\text{R}$ in profit.
- **Target Exit:** Fixed exit at $+1.75\text{R}$ (mean-reversion equilibrium target).
- **Time Decay Invalidation:** Exit at market if price fails to reach $+0.20\text{R}$ within 36 bars (9.0 hours).
- **Causal Arming:** Stop modifications armed at bar $j$ close take effect on bar $j+1$ open only.

### 2.3 Risk Budget & Portfolio Governance
- **Initial Capital:** $5,000.00 USD.
- **Base Risk Budget:** $25.00 USD per trade ($0.50\%$ of equity).
- **House Money Tier:** $50.00 USD ($1.00\%$ max 2× risk when net session profits $> \$50.00$).
- **Drawdown Defense Tier:** $15.00 USD ($0.30\%$ risk when drawdown exceeds $2.5\%$).
- **Hard Drawdown Stop:** $4.50\%$ ($225.00 USD hard stop, trading ceases for the period).
- **Portfolio Concurrency:** Maximum 2 simultaneous open positions across all 18 symbols.

### 2.4 Transaction Frictions & Execution Realism
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
- **Anti-Lookahead Blacklist:** Zero lookup tables, zero test-set parameter optimization, zero test-set overrides.

---

## 4. Core Implementation Architecture

```python
# Causal signal generation in S2InstitutionalMLSimulator
for t in range(1, T):
    sig_long = (long_liq_zs[t] > 1.2) and (zc_div[t] > 0.3) and (spot_cvd_delta[t] > 0) and \
               (fut_cvd_delta[t] < 0) and (rsi[t] < 45) and (vwap_z[t] < -0.4)
    sig_short = (short_liq_zs[t] > 1.2) and (zc_div[t] < -0.3) and (spot_cvd_delta[t] < 0) and \
                (fut_cvd_delta[t] > 0) and (rsi[t] > 55) and (vwap_z[t] > 0.4)
        
    if filter_func is not None:
        if sig_long and not filter_func(t, 'LONG'): sig_long = False
        if sig_short and not filter_func(t, 'SHORT'): sig_short = False

    if sig_long:
        signals[t] = 1; raw_r[t] = atr[t] * 2.0
    elif sig_short:
        signals[t] = -1; raw_r[t] = atr[t] * 2.0

# Handed off to decoupled ExecutionKernel
return kernel.run(df_test, signals_df, training_mode)
```

---

## 5. Specific Audit Questions for Ox Alpha

1. **Dual-Sided Microstructure Asymmetry:** Does conditioning on spot CVD divergence ($\text{zc\_div}$) and liquidation bursts produce symmetric edge on both the long and short side in crypto perpetuals, or do positive funding rate drift and structural upward market skew make short mean-reversion significantly more hazardous during aggressive bull regimes (e.g. Q1/Q4 2021, Q1 2024)?
2. **High-Turnover Ratchet (+0.85R $\to$ +0.45R, +1.25R $\to$ +0.85R, +1.75R Target):** How does this tighter take-profit geometry compare to Strategy 1's $+2.50\text{R}$ target? In high-frequency 15m rebalancing, does locking profit early at $+0.45\text{R}$ maximize Sharpe ratio and suppress drawdown, or does it incur excessive fee drag under $8\text{ bps}$ taker fees?
3. **ML Overlay Architecture & Training Protocols:** When training an XGBoost overlay for `filter_func(t, side)`:
   - What feature representations provide maximum stationary generalization across the 20 OOS windows (e.g., rolling z-scores vs footprint ladder imbalances)?
   - How should class imbalance be managed given that raw confluence triggers occur on $< 2\%$ of all bars?
4. **Decoupled Architecture Verification:** Does S2's decoupled architecture (pure signal generator returning `signals_df` to `ExecutionKernel`) eliminate all vectors of lookahead or information leakage between signal discovery and portfolio risk execution?
