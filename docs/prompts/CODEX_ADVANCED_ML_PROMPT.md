# MASTER CODEX DIRECTIVE: INSTITUTIONAL ML CRACKER FOR ALL 8 STRATEGIES

> **OPERATIONAL CONSTRAINT: STRICT PLUS-PLAN TOKEN EFFICIENCY**
> Codex/Astra: Output ONLY pure, production-grade Python code and mathematical architectures. Zero conversational filler, zero restating instructions, zero disclaimers, zero speculative brute-force sweeps.

---

## 🎯 THE MISSION & SETTLED OOS TARGETS
You must upgrade and optimize **ALL 8 STRATEGIES** in the Trading Engine to simultaneously pass the 20 Out-Of-Sample (OOS) Windows protocol on the 18 master Binance USDT-M Perpetual assets (3.46M 15m candles in `c:\Users\SIGMA\Documents\Trading\Engine\binance_backtesting_data\`).

Every strategy must satisfy the exact institutional thresholds defined in:
- `c:\Users\SIGMA\Documents\Trading\Engine\target_oos_criteria.json`:
  - **ROI per window:** > 20.0%
  - **Max Drawdown:** < 5.0%
  - **Win Rate:** > 40.0%
  - **Exit Target:** Strictly +2.5R (Purged 5R fantasy)
  - **Minimum Trades:** >= 6 trades per window
- `c:\Users\SIGMA\Documents\Trading\Engine\oos_windows_20.json` (All 20 non-overlapping historical stress regimes from 2021 to 2026).

---

## 📂 THE 8 TARGET STRATEGY FILES (READ DIRECTLY VIA TOOLING)
You must apply the unified ML & microstructure framework to these exact 8 strategy files:

### Quant & Microstructure Engines:
1. `c:\Users\SIGMA\Documents\Trading\Engine\strategy\s1_liquidation_cascade.py` (Liquidation Cascades & Z-Score Exhaustion)
2. `c:\Users\SIGMA\Documents\Trading\Engine\strategy\s2_institutional_ml.py` (Stationary Microstructure & CVD Divergence)

### Institutional SMC (Smart Money Concepts) Playbooks:
3. `c:\Users\SIGMA\Documents\Trading\Engine\strategy\smc_edgeful.py` (Edgeful Premium/Discount & Liquidity Sweeps)
4. `c:\Users\SIGMA\Documents\Trading\Engine\strategy\smc_kane.py` (Kane Order Block Mitigations & CHoCH)
5. `c:\Users\SIGMA\Documents\Trading\Engine\strategy\smc_marci.py` (Marci Breaker Blocks & Fair Value Gaps)
6. `c:\Users\SIGMA\Documents\Trading\Engine\strategy\smc_marco.py` (Marco Session Range Sweeps & Turtle Soup)
7. `c:\Users\SIGMA\Documents\Trading\Engine\strategy\smc_mayne.py` (Mayne Higher-Timeframe Key Level Rebalances)
8. `c:\Users\SIGMA\Documents\Trading\Engine\strategy\smc_usman_noah.py` (Usman Noah Volumetric Imbalances & Institutional Wicks)

---

## ⚡ STEP 1: FIX THE CORE EXECUTION KERNEL (ZERO LOOKAHEAD)
File: `c:\Users\SIGMA\Documents\Trading\Engine\core\execution_kernel.py`
- **Issue:** Retroactive open-price execution on candle $j$ and skipping entry-bar stop loss evaluation introduces lethal lookahead bias.
- **Requirement:** Refactor the core bar simulation loop to strictly enforce causal execution at the **`Open` of bar $j+1$**, while allowing stop-loss and ratchet evaluations to trigger on the entry bar's High/Low. Output the exact drop-in method replacement.

---

## 🧠 STEP 2: WORLD-CLASS ADVANCED ML OVERLAY (LOPEZ DE PRADO META-LABELING)
Do not use naive end-to-end black-box models that overfit high-frequency noise. Implement the institutional standard: **Secondary ML Meta-Labeling (Advances in Financial Machine Learning)**.

### Architecture:
1. **Primary Model (Rule / Concept Domain):**
   - Each of the 8 strategies generates candidate directional trade events ($y_{prim} \in \{+1, 0\}$) based on its native edge (e.g. Liquidation Z-score > 1.8 for S1, Turtle Soup sweep for Marco, Order Block mitigation for Kane).
2. **Secondary ML Classifier (Meta-Model):**
   - Conditioned strictly on bars where $y_{prim} == 1$. Discards the 98% irrelevant zero-class noise.
   - Predicts the binary outcome: **Will this specific setup reach the +2.5R target before hitting the -1.0R stop or the 24-bar time decay?**
3. **Triple-Barrier Labeling Scheme:**
   - Upper Barrier: Entry $+ 2.5 \times \text{ATR}$ (or $+2.5R$) $\to$ Label = 1
   - Lower Barrier: Entry $- 1.0 \times \text{ATR}$ (or $-1.0R$) $\to$ Label = 0
   - Vertical Barrier: 24 bars (6 hours) $\to$ Label = 0 if unrealized PnL $< +0.2R$
4. **Causal Cross-Validation:**
   - Purged & Embargoed Walk-Forward CV with a strictly causal 72-hour purge window ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$) to eliminate information leakage across overlapping trade horizons.
5. **Regularized GBDT Specification:**
   - Classifier: `XGBClassifier` or `LGBMClassifier`
   - Hyperparameters: `max_depth=3` or `4`, `learning_rate=0.03`, `n_estimators=120`, `subsample=0.8`, `colsample_bytree=0.8`, `reg_alpha=1.5`, `reg_lambda=3.5`, `min_child_weight=15`.
6. **Stationary Microstructure Feature Vector:**
   - `fp_delta_ratio`, `zc_div`, `long_liq_zs`, `short_liq_zs`, `rsi_14`, `dist_to_vwap_zs`, `atr_norm`, `volume_ratio_sma20`.

---

## 🛡️ STEP 3: UNIFIED MICROSTRUCTURE EXIT RATCHET
Every strategy must run this deterministic ratchet in its execution phase:
- **Phase 0 (Breakeven Lock):** At `+0.8R` gain $\to$ Move stop to `Entry + 0.15R`.
- **Phase 1 (Profit Lock):** At `+1.5R` gain $\to$ Move stop to `Entry + 0.80R`.
- **Hard Take-Profit:** Exit at `+2.5R`.
- **Time Decay:** Exit at market if unrealized PnL $< +0.2R$ after 24 bars.

---

## 📝 OUTPUT DELIVERABLES REQUIRED:
1. **The Causal Execution Kernel Patch** for `c:\Users\SIGMA\Documents\Trading\Engine\core\execution_kernel.py`.
2. **The Reusable `InstitutionalMetaLabeler` Python Class** (feature extraction, triple-barrier labeling, purged walk-forward training, probability calibration, and signal filtering).
3. **The Strategy Integration Recipe** showing how `InstitutionalMetaLabeler` wraps `s1_liquidation_cascade.py` and the 6 SMC playbooks to crack all 8 files and guarantee passing `target_oos_criteria.json`.
