# Ox Alpha Strategy Review — Strategy 1: S1 Liquidation Cascade Engine
**Target:** Institutional Quantitative Review & Microstructure Alpha Audit  
**Strategy Module:** `Engine/strategy/s1_liquidation_cascade.py` & `Engine/core/execution_kernel.py`  
**Universe:** 18 Institutional Binance USDT-M Perpetuals (3.47M 15m Candles, 0 Nulls, Monotonic)  

---

## 1. Executive Summary & Strategy Thesis

### Liquidation Cascade Absorption & Mean Reversion
In crypto perpetual futures markets, cascading liquidations represent extreme non-linear microstructure dislocations:
1. Highly leveraged long (or short) positions hit bankruptcy price boundaries.
2. The exchange's Liquidation Risk Engine executes automated, aggressive market orders into the thin book.
3. This creates sudden price displacement characterized by:
   - High Liquidation Z-Score ($\text{long\_liq\_zs} > 1.2$ or $> 1.8$).
   - Extreme intraday volume expansion ($\text{volume\_ratio} > 1.2$).
   - Sharp deviation below VWAP ($\text{vwap\_zscore} < -0.5$).
   - Momentum exhaustion ($\text{RSI}_{14} < 40$).
4. Institutional market makers absorb this forced selling on spot exchanges ($\Delta\text{Spot CVD} > 0$ vs $\Delta\text{Futures CVD} < 0$, high $\text{zc\_div} > 0.8$).
5. Once forced order flow exhausts, price mean-reverts aggressively toward equilibrium VWAP.

---

## 2. Quantitative Strategy Invariants

### 2.1 Signal Confluence Geometry
Causal directional signal fired at bar $t$ close, effective bar $t+1$ open:
$$\text{Signal}_{\text{LONG}} = (\text{long\_liq\_zs}_t > 1.2) \;\land\; (C_t > O_t) \;\land\; (\text{filter\_func}(t, \text{'LONG'}))$$

In high-confluence institutional mode:
$$\text{long\_liq\_zs} > 1.8 \;\land\; \text{zc\_div} > 0.8 \;\land\; \Delta\text{Spot} > 0 \;\land\; \Delta\text{Futures} < 0 \;\land\; \text{RSI} < 40 \;\land\; \text{VWAP Z} < -0.5$$

### 2.2 Risk Budget & Portfolio Governance
- **Initial Capital:** $5,000.00 USD.
- **Base Risk Budget:** $25.00 USD per trade ($0.50\%$ of equity).
- **House Money Tier:** $50.00 USD ($1.00\%$ max 2× risk when net session profit $> \$50.00$).
- **Drawdown Defense Tier:** $15.00 USD ($0.30\%$ risk when drawdown exceeds $2.5\%$).
- **Hard Drawdown Stop:** $4.50\%$ ($225.00 USD hard stop, trading ceases for the period).
- **Portfolio Concurrency:** Maximum 2 simultaneous open positions across all 18 symbols.

### 2.3 Microstructure Exit Ratchet (Anti-Retracement Defense)
Legacy 5.0R fixed targets caused an 85.8% retracement of winning trades into stop-outs. Modern ratchet geometry:
- **Phase 0 (Breakeven Lock):** At $+0.80\text{R}$ price gain, move stop to Entry $+0.15\text{R}$.
- **Phase 1 (Profit Lock):** At $+1.50\text{R}$ price gain, move stop to Entry $+0.80\text{R}$.
- **Target Exit:** Fixed exit at $+2.50\text{R}$.
- **Time Decay Invalidation:** If trade fails to gain $+0.20\text{R}$ within 24 bars (6 hours), exit at market.
- **Causal Arming:** Stop modifications armed at bar $j$ close take effect at bar $j+1$ open only.

### 2.4 Transaction Frictions & Fill Assumptions
- **Taker Fees:** 8 basis points ($0.08\%$) on both entry and exit.
- **Entry Slippage:** 10 basis points ($0.10\%$) against trade direction.
- **Exit Slippage (Stop / Market):** 15 basis points ($0.15\%$) against trade direction.
- **Stop-First Intrabar Execution:** If both High $\ge$ Target and Low $\le$ Stop occur within the same 15m bar, the stop-loss is assumed to hit first (conservative fill).

---

## 3. Walk-Forward 20 OOS Validation Framework

Subjected to **20 Non-Overlapping Out-of-Sample (OOS) 1-Month Windows (2021–2026)**:
- Causal 72-hour purge boundaries ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$).
- Minimum Pass Criteria per window: $\text{ROI} \ge 20.0\%$, $\text{MaxDD} < 5.0\%$, $\text{Win Rate} \ge 40.0\%$, $\text{Trades} \ge 6$.
- **Anti-Lookahead Blacklist:** Zero lookup tables, zero test-set hyperparameter searches, zero test-set overrides.

---

## 4. Core Implementation Architecture

```python
# Causal signal generation and centralized execution kernel
for t in range(24, T):
    # Microstructure cascade trigger at bar t close
    sig_long = (long_liq_zs[t] > 1.2) and (close[t] > open[t])
    if sig_long and (filter_func is None or filter_func(t, 'LONG')):
        signals[t] = 1
        raw_r[t] = max(atr_14[t] * 2.0, close[t] * 0.005)

# Execution: fills at bar t+1 open with 10 bps slippage
entry_px = open[t] * (1.0 + 0.0010)
pos_qty = risk_budget / raw_r[t-1]
stop_px = entry_px - raw_r[t-1]
target_px = entry_px + 2.5 * raw_r[t-1]

# Trailing ratchet evaluation bar-by-bar
if cur_r >= 1.50:
    stop_px = max(stop_px, entry_px + 0.80 * raw_r[t-1])
elif cur_r >= 0.80:
    stop_px = max(stop_px, entry_px + 0.15 * raw_r[t-1])

# Time decay exit at market with 15 bps slippage if < 0.2R after 24 bars
if bars_held >= 24 and max_favorable_r < 0.20:
    exit_at_market(bar=t, reason="TIME_DECAY")
```

---

## 5. Specific Audit Questions for Ox Alpha

1. **Microstructure Edge Evaluation:** Does liquidation cascade absorption exhibit genuine non-linear statistical persistence in cryptocurrency perpetuals when conditioning on $Z > 1.2$ or $Z > 1.8$, or does adverse selection (trend continuation through the cascade) dominate during structural regime breaks?
2. **Ratchet Geometry Optimization:** What is your quantitative assessment of the two-stage ratchet ($+0.8\text{R} \to +0.15\text{R}$ BE, $+1.5\text{R} \to +0.8\text{R}$ lock, $+2.5\text{R}$ take-profit, 24-bar time decay)? Does the breakeven move at $+0.8\text{R}$ prematurely truncate fat-tailed upside in volatile liquidation recoveries?
3. **Execution Realism:** Are the modeled taker fees ($8\text{ bps}$) and asymmetric slippages ($10\text{ bps}$ entry, $15\text{ bps}$ stop) mathematically conservative enough to prevent backtest overfitting across both high-liquidity (BTC, ETH) and mid-cap (SUI, NEAR, APT) assets?
4. **Walk-Forward Survival Recommendations:** What specific feature engineering or ML overlay architectures (e.g. XGBoost shallow trees with L1/L2 regularization vs regime classification) do you recommend to guarantee stable pass rates across all 20 Out-of-Sample windows?
