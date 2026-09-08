# OX ALPHA — ROUND 4: UNIFYING SMC STRUCTURAL SETUPS WITH FOOTPRINT ORDER FLOW & ML META-LABELING

> **EXECUTIVE BRIEFING & SYSTEM SPECIFICATION FOR OX ALPHA QUANTITATIVE ARCHITECT:**
> We have completed empirical testing of Round 3 and received a Tier-1 "A-" audit verdict from Arena.ai on our 18-asset Binance perpetual dataset (3.47M continuous 15m bars, 0 nulls, 0 lookahead leaks, bit-perfect volume conservation).
>
> Our empirical backtests revealed two foundational insights:
> 1. **The 15m Pure Mean-Reversion Bottleneck:** High-frequency 15m cascade entries suffer from severe friction drag (33 bps fee/slippage consumes ~0.55R on tight 0.5% stops) and lack higher-timeframe trend context.
> 2. **The SMC Structure Opportunity:** Our Smart Money Concepts (SMC) playbooks (`smc_usman_noah.py`, `smc_marci.py`, `smc_marco.py`, `smc_edgeful.py`) trade higher-timeframe structural levels (Previous Day High/Low sweeps, Daily Fair Value Gaps, and Breaker Blocks) where structural stops are 1.5%–2.5% away — **slashing friction drag from 0.55R down to 0.13R–0.18R**. However, when traded raw/blindly, they suffer from 20%–38% win rates because price frequently blows through unconfirmed levels.
>
> **The Core Mandate:** We want to build the **Unified Quantitative Architecture** that combines:
> **[Raw SMC Macro Structure] $\longrightarrow$ [Footprint Order Flow Confirmation] $\longrightarrow$ [ML Continuous R-Meta-Labeling] $\longrightarrow$ [Causal Portfolio Execution]**

---

## 1. RAW GITHUB REPOSITORY REFERENCES (FETCH DIRECTLY)

All active production source files and manifests are committed and accessible via GitHub:
`https://github.com/kbsingh1399/Trading`

Key files to inspect:
1. **Footprint Feature Extractor (Vectorized Order Flow Engine)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/ml/footprint_features.py`
2. **Continuous R-Regression Meta-Labeler**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/ml/rf_meta_labeler.py`
3. **Cross-Asset Pooled Base Meta-Labeler**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/ml/pooled_meta_labeler.py`
4. **SMC Usman Noah Engine (PDH/PDL Sweep + Reclaim)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/smc_usman_noah.py`
5. **SMC Marci Engine (Bollinger Band Pullback + Market Structure Shift)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/smc_marci.py`
6. **Multi-Asset Portfolio Execution Kernel (Max 2 Concurrent, Shared $5k Capital)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/portfolio_execution_kernel.py`
7. **Round 3 Walk-Forward Runner**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/runners/round3_runner.py`
8. **Target Out-of-Sample Validation Criteria**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/target_oos_criteria.json`

---

## 2. EMPIRICAL BENCHMARKS & BASELINE NUMBERS

### 2.1 Raw SMC Performance (BTCUSDT, 20 OOS Windows, 33 bps Frictions, No Confirmation):
When traded blindly on 15m klines without footprint confirmation or ML gating:
- `SMC_UsmanNoah`: 76 trades | Cum ROI: -18.52% | Max DD: 3.22% | Win Rate: 25.0%
- `SMC_Marci`: 314 trades | Cum ROI: -52.21% | Max DD: 4.53% | Win Rate: 23.9%
- `SMC_Edgeful`: 465 trades | Cum ROI: -90.03% | Max DD: 4.78% | Win Rate: 26.7%
- `SMC_Marco`: 431 trades | Cum ROI: -86.63% | Max DD: 4.67% | Win Rate: 19.0%

### 2.2 Footprint Order Flow Probe Results (from Round 3 Clean Event Slices):
When we joined `{symbol}_15m_footprint_ladder.parquet` order flow metrics, individual feature discrimination jumped:
- `reclaim_mid`: AUC = **0.5298** ($|\text{AUC} - 0.5| = 0.030$)
- `poc_shift`: AUC = **0.5266**
- `close_pos`: AUC = **0.5268**
- `sell_impact`: AUC = **0.5238**
- Best pair (`reclaim_mid + poc_shift`): AUC = **0.5308**

---

## 3. ARCHITECTURAL BLUEPRINT REQUESTED FROM OX ALPHA

We need Ox Alpha's concrete mathematical specifications, feature transformations, and Python code to execute this 3-tier synthesis:

### Deliverable 1: The SMC Structure Event Generator (`SMCEventDetector`)
Design a unified SMC event detector that consumes our 15m Master Table (56 columns) and identifies high-probability structural setups:
- **Usman Noah PDH/PDL Liquidity Sweeps:** Price sweeps the Previous Day High (PDH) or Previous Day Low (PDL) and prints an initial reaction.
- **Fair Value Gap (FVG) / Imbalance Retest:** 3-bar price displacement leaves an unmitigated FVG; price re-enters the FVG zone.
- **Order Block (OB) / Breaker Mitigation:** Price pulls back into the origin of a displacement wave.
- **Output:** Emits candidate coordinate `(timestamp, symbol, side, structural_level, invalidation_price, raw_r_dist)` where `raw_r_dist >= 1.5%` (ensuring friction $< 0.20\text{R}$).

### Deliverable 2: The Footprint Order Flow Confirmation Gate (`FootprintConfirmation`)
At the exact moment the SMC structural level is tested, how does the Footprint Ladder (`{symbol}_15m_footprint_ladder.parquet`) confirm that institutional absorption and trapped traders exist?
- What are the exact thresholds on:
  - `wick_sell_absorb` / `wick_buy_exhaust` (resting limit orders absorbing market aggressive flow at the extreme)?
  - `poc_shift` (volume Point of Control migrating away from the sweep)?
  - `sell_impact` / `absorption_ratio` (market selling expanding while price refuses to drop)?
  - Stacked Imbalances (`is_stacked_buy_imb`, `is_stacked_sell_imb`)?
- Emit a composite order flow confirmation score: `is_confirmed = True/False`.

### Deliverable 3: Cross-Asset Pooled ML Meta-Labeling (`SMCRegressionMetaLabeler`)
Fit our `RegressionRMetaLabeler` on the SMC-confirmed events across all 18 Binance assets:
- **Feature Set:** Stationarized combination of SMC geometry (`dist_to_pdl_atr`, `fvg_depth_pct`, `reclaim_strength`), footprint order flow (`wick_sell_absorb`, `poc_shift`, `sell_impact`), and macro confluence (`zc_div`, `funding_rate_pct`, `vwap_zscore`).
- **Target Variable:** Realized $R$-multiple under friction-adjusted barriers (`tp_r = 2.0R to 2.5R, sl_r = 1.0R + friction_R`).
- **Causal WF-CV:** 72h purged / 24h embargoed grouped cross-validation.
- **Expectancy Cut:** Calibration of $\tau_R$ such that $E[R \mid \hat{R} \ge \tau_R] - \text{friction}_R \ge +0.25\text{R}$.

### Deliverable 4: Microstructure Exit Ratchet & Multi-Asset Portfolio Kernel
For an SMC swing setup with $1\text{R} \approx 1.8\% - 2.5\%$:
- Provide the optimal `RatchetConfig` (breakeven lock, profit lock, trail, and time decay) that avoids the 22.9% win-rate retracement trap while giving the trade room to reach $+2.0\text{R}$ to $+2.5\text{R}$.
- Specify the risk sizing per trade (e.g. Base Risk \$50 vs House Money \$75-\$100) under the \$5,000 capital and 4.5% (\$225) hard drawdown constraint to hit **$+20.0\%$ net ROI per 1-month window** with $\ge 6$ trades.

### Deliverable 5: End-to-End Walk-Forward Integration Code
Provide a drop-in runner module (`Engine/runners/smc_footprint_runner.py`) that wires the SMC event detector, footprint confirmation, regression meta-labeler, and portfolio execution kernel into a unified walk-forward pipeline ready to run across all 20 OOS windows.
