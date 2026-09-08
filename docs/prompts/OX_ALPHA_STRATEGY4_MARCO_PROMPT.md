# Ox Alpha Strategy Review — Strategy 4: SMC Marco Trades Engine
**Target:** Institutional Quantitative Review & Liquidity Sweep / Trap Alpha Audit  
**Strategy File:** `Engine/strategy/smc_marco.py` & `Engine/core/execution_kernel.py`  
**Dataset Grounding:** Binance 15-Minute Dual-Table Master Dataset (Certified 98/100 by Ox Alpha)  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Archetype

### Liquidity Pool Sweeps, Trapped Market Orders & Mean Reversion
SMC Marco Trades exploits the microstructure mechanics of liquidity engineering around major swing extremes:
1. **Identification of Resting Liquidity Pools:**
   - Unmitigated swing highs and swing lows harbor retail stop-loss orders and breakout entry orders (liquidity pools).
   - Causal 8-bar center pivot rolling logic ($t \ge 16$, center at $t-8$ confirmed against 8 bars prior and 8 bars following up to $t-1$).
   - Active liquidity pools persist for up to 64 bars (16 hours).
2. **The Sweep and Trap Mechanism:**
   - **Sell-Side Sweep (Bullish Trap):** Price penetrates below an established swing low pool ($\text{Low}_t < \text{Pool}_{\text{low}}$), triggering retail long stops and breakout market orders. Informed buyers absorb this supply, forcing price to close back above the pool boundary ($\text{Close}_t > \text{Pool}_{\text{low}}$) on a green candle ($C_t > O_t$).
   - **Buy-Side Sweep (Bearish Trap):** Price spikes above a swing high pool ($\text{High}_t > \text{Pool}_{\text{high}}$), triggering short stops and buy breakouts, where passive limit sellers absorb flow, forcing a close back below the level ($\text{Close}_t < \text{Pool}_{\text{high}}$) on a red candle ($C_t < O_t$).
3. **Microstructure Absorption Confluence:**
   - Long sweeps require contemporaneous evidence of institutional absorption:
     $$\text{long\_liq\_zs}_t > 0.8 \;\lor\; \text{zc\_div}_t > 0.3 \;\lor\; \text{vwap\_zscore}_t < -0.5$$
   - Short sweeps require:
     $$\text{short\_liq\_zs}_t > 0.8 \;\lor\; \text{zc\_div}_t < -0.3 \;\lor\; \text{vwap\_zscore}_t > 0.5$$
4. **Structural Invalidation Stop:**
   - Pegged precisely outside the wick of the sweep candle:
     $$\text{Stop Distance}_{\text{LONG}} = (C_t - L_t) + 0.1 \times \text{ATR}_{14}(t)$$
     clamped strictly within $[0.006 \times C_t, \; 1.5 \times \text{ATR}_{14}]$.

---

## 2. Quantitative Strategy Invariants

### 2.1 Microstructure Exit Ratchet (Trap Scalp Geometry)
- **Phase 0:** At $+0.70\text{R}$ price gain, move stop to Entry $+0.20\text{R}$.
- **Phase 1:** At $+1.20\text{R}$ price gain, lock $+0.70\text{R}$ in profit.
- **Target Exit:** Fixed exit at $+1.80\text{R}$.
- **Time Decay Invalidation:** If trade fails to reach $+0.20\text{R}$ within 40 bars (10.0 hours), exit at market.
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
# Causal 8-bar center pivot liquidity pool identification
if t >= 16:
    center_hi = hi[t-8]; center_lo = lo[t-8]
    if all(center_hi > hi[t-8-i] and center_hi > hi[t-8+i] for i in range(1, 9)):
        liquidity_pools.append({"price": center_hi, "type": 1, "age": 0})
    if all(center_lo < lo[t-8-i] and center_lo < lo[t-8+i] for i in range(1, 9)):
        liquidity_pools.append({"price": center_lo, "type": -1, "age": 0})

# Sell-side liquidity sweep & trap re-entry
if pool["type"] == -1 and trend_up and has_absorption_l:
    if lo[t] < pool["price"] and cl[t] > pool["price"] and cl[t] > op[t]:
        signals[t] = 1
        raw_r[t] = np.clip((cl[t] - lo[t]) + 0.1*atr[t], cl[t]*0.006, 1.5*atr[t])
        swept_pools.append(i)

return kernel.run(df_test, signals_df, training_mode)
```

---

## 5. Specific Audit Questions for Ox Alpha

1. **Center-Pivot Causal Soundness:** The liquidity pool pivot uses an 8-bar forward/backward window evaluated at $t-8$. Since the evaluation occurs on candle $t$ using data strictly up to $t-1$, is this guarantee 100% causal and immune to future-candle leakage?
2. **Sweep Quality & Wick Distortion:** The entry triggers when the wick breaches the pool but the close re-enters the range. In high-volatility flash crashes, does sizing based on $(C_t - L_t) + 0.1 \times \text{ATR}$ lead to oversized stops that dilute the strategy's risk-reward ratio, or is the $1.5 \times \text{ATR}$ ceiling sufficient protection?
3. **Pool Consumption Protocol:** Once swept, the pool is immediately pruned (`liquidity_pools.pop(i)`). In fragmented crypto markets, do major liquidity levels experience multi-stage sweeps (double bottoms/tops), and should pools support a partial-mitigation state before complete deletion?
4. **Ratchet Geometry ($+0.7\text{R} \to +0.2\text{R}$, $+1.2\text{R} \to +0.7\text{R}$, $+1.8\text{R}$ Target):** Does an early breakeven lock at $+0.7\text{R}$ effectively insulate the strategy from false-trap whipsaws, or does it trigger premature stop-outs before full mean-reversion is realized?
