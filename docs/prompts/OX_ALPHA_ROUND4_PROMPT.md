# OX ALPHA — ROUND 4: CONQUERING THE 20 OOS WINDOWS VIA TIMEFRAME EXPANSION & SMC ENSEMBLE

> **BRIEFING FOR OX ALPHA QUANTITATIVE STRATEGIST:**
> We have completed empirical testing of Round 3 and received a Tier-1 "A-" audit verdict from Arena.ai on our 18-asset dataset.
> Here are the exact empirical results, the verified data properties, and the core structural hurdles we must solve to achieve the **+20% ROI / <5% DD per window target** across the 20 Out-of-Sample (OOS) windows.

---

## 1. EMPIRICAL RESULTS & VALIDATIONS FROM ROUND 3

### 1.1 Arena.ai Dataset Forensic Audit (Grade: A- / Tier-1 Pass)
- **Scale:** 3,470,018 rows across 18 Binance USDT-M perpetual contracts (2020–2026).
- **Contiguity:** 0 missing bars, 0 duplicate timestamps, strictly monotonic 15m intervals ($t_{i+1} - t_i = 900,000\text{ ms}$).
- **Referential Integrity:** Ladder total volume matches Master volume bit-perfectly to machine epsilon ($4.4 \times 10^{-16}$).
- **Causality:** 0 lookahead leaks; daily session boundary resets verified across 8,776 session starts.
- **Epistemic Disclosure:** Early derivatives metrics (2020–2021 for ETH/DOGE/SOL) use default-anchored forward-fill (flagged by `is_imputed_metrics = 1`).

### 1.2 Empirical Execution of S1v2 (Flush -> Reclaim State Machine)
We implemented your Deliverable 2 (`FootprintLadderFeatures`), Deliverable 3 (`RegressionRMetaLabeler`), and Deliverable 4 (`S1LiquidationCascadeV2`).
1. **Signal De-Clustering:** We eliminated consecutive-bar multi-fire signals during reclaims, reducing 45,025 correlated bar rows to **8,615 clean, distinct cascade events** across the 18 symbols.
2. **Order Flow Alpha Lift (Feature Probe on Clean Events):**
   - `reclaim_mid`: AUC = **0.5298** ($|\text{AUC} - 0.5| = 0.030$)
   - `close_pos`: AUC = **0.5268**
   - `poc_shift`: AUC = **0.5266**
   - `ret_zs`: AUC = **0.5256**
   - `sell_impact`: AUC = **0.5238**
   - Top Pair (`reclaim_mid + poc_shift`): AUC = **0.5308**
3. **Multivariate XGBoost / LightGBM CV-AUC:**
   - 5-fold Purged Grouped Time-Split CV-AUC: **0.5255** (Fold 0: 0.546, Fold 1: 0.508, Fold 2: 0.536, Fold 3: 0.542, Fold 4: 0.496).
   - Out-of-fold expectancy: $E[R] = -0.065\text{R}$.
4. **Decision Tree Enforcement:**
   - Because mean CV-AUC ($0.5255$) $< 0.55$ and $E[R] < 0$, your gate strictly evaluated to **`DEPLOY = FALSE` (0 trades, 0.0% PnL, 0.0% DD)**.
   - **The gate worked as designed: it prevented capital loss.**

### 1.3 The 8-Strategy Raw Benchmark Across All 20 OOS Windows
When tested under real frictions (8 bps fee, 10 bps entry slippage, 15 bps exit slippage = 33 bps round trip), ALL 8 raw strategies without higher-timeframe filters lose capital over 20 windows:
- `S1_LiqCascade`: 172 trades, ROI: -36.02%, Max DD: 3.29%, Win Rate: 19.8%
- `S2_InstML`: 398 trades, ROI: -61.32%, Max DD: 4.74%, Win Rate: 38.9%
- `SMC_Edgeful`: 465 trades, ROI: -90.03%, Max DD: 4.78%, Win Rate: 26.7%
- `SMC_Kane`: 479 trades, ROI: -85.24%, Max DD: 4.60%, Win Rate: 29.2%
- `SMC_Marci`: 314 trades, ROI: -52.21%, Max DD: 4.53%, Win Rate: 23.9%
- `SMC_Marco`: 431 trades, ROI: -86.63%, Max DD: 4.67%, Win Rate: 19.0%
- `SMC_Mayne`: 464 trades, ROI: -88.08%, Max DD: 4.77%, Win Rate: 25.4%
- `SMC_UsmanNoah`: 76 trades, ROI: -18.52%, Max DD: 3.22%, Win Rate: 25.0%

---

## 2. THE MATHEMATICAL BOTTLENECK: THE 15-MINUTE FRICTION TRAP

The core obstacle preventing ANY 15-minute strategy from hitting +20% ROI with <5% DD is **Friction Drag relative to Stop Distance**:
- On 15m bars, a structural stop is typically 0.50% to 0.70% away ($1\text{R} \approx 0.6\%$).
- 33 bps round-trip friction = $0.33\% / 0.60\% = \mathbf{0.55\text{R}}$ **loss per trade before price moves!**
- With a 44% win rate and 2.0R target:
  $$E[R] = (0.44 \times 2.0\text{R}) - (0.56 \times 1.0\text{R}) - 0.55\text{R} = 0.88 - 0.56 - 0.55 = \mathbf{-0.23\text{R}}$$
- Friction consumes more than half of the risk budget per trade.

---

## 3. CORE QUESTIONS & BLUEPRINT REQUEST FOR ROUND 4

We need Ox Alpha's concrete architecture and code to break through this mathematical ceiling:

### Question 1: Geometric Stop Expansion (1H / 4H Anchors)
If we anchor our entry stop to the **1-Hour or 4-Hour structural swing low** (where $1\text{R} \approx 2.0\% - 2.5\%$) while using the 15m footprint ladder for precision entry timing:
- Friction drops from $0.55\text{R}$ down to **$0.13\text{R}$** ($0.33\% / 2.5\%$).
- How should the S1v2 reclaim state machine anchor its stop to HTF swing lows instead of the single 15m flush bar?

### Question 2: Higher-Timeframe (HTF) Regime & Trend Conditioning
Post-liquidation bounces in a macro 4H bear market often stall at VWAP ($+0.5\text{R}$ to $+1.0\text{R}$) before cascading to new lows.
- How should we causally condition the trade direction?
  - E.g., Longs only when 4-Hour VWAP slope $> 0$ or price is below Daily VAL / Key D1 Liquidity Low?
  - Shorts enabled when 4-Hour market structure breaks bearish?

### Question 3: Deploying the Meta-Labeler on SMC Playbooks
Among the SMC playbooks, `smc_usman_noah.py` and `smc_marci.py` showed the lowest baseline drawdown (-18% and -52% vs -90% for others) and generate swing signals based on Fair Value Gaps and Breaker Blocks.
- How can we plug our `RegressionRMetaLabeler` and `FootprintLadderFeatures` as a secondary gate on top of SMC structure signals?
- What are the exact filter conditions to ensure trade count stays $\ge 6$ per 1-month window while boosting win rate $> 50\%$?

### Question 4: Portfolio Allocation & Capital Scaling Across 18 Assets
With a fixed \$5,000 capital, max 2 concurrent positions, and a 4.5% hard drawdown stop (\$225):
- How should risk per trade be dynamically sized (e.g., base risk \$50 vs house money \$75) to achieve +20% net ROI (\$1,000 profit = +20R net) within the 4.5% drawdown constraint?
- Provide concrete Python code for the multi-timeframe S1/SMC integration, the revised barrier configuration, and the portfolio allocation logic.
