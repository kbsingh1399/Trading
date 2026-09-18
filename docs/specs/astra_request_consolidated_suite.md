# ASTRA AI SPECIFICATION: CONSOLIDATED PRODUCTION SUITE & ML PIPELINE
**From:** Antigravity Quant Desk  
**To:** Astra AI (Azure Data Explorer / Kusto Specialist)  
**Subject:** Request for Consolidated ZIP (`orderflow_production_suite_v2.zip`) & Embedded Causal ML Training Pipeline  
**Target Path:** `C:\Users\SIGMA\Downloads\Astra_Request_Consolidated_Zip_and_ML_Train.txt`

---

## 1. Directive & Core Choice

Astra, we received your `orderflow_ml_overlay.py` and reviewed the GradientBoostingClassifier architecture.

In response to your query:
> **"Do you also want me to embed a ready-to-train ML pipeline (feature prep + sample labels) in the ML overlay file, or should I generate institutional_forensic_report.pdf with updated charts and reconciled math next? Or deliver a single consolidated ZIP including all repaired code + ML + config + doc for compliance?"**

### Our Direct Answer:
**Deliver the SINGLE CONSOLIDATED ZIP (`orderflow_production_suite_v2.zip`) containing BOTH the embedded ready-to-train ML pipeline AND the updated compliance report (`institutional_forensic_report.pdf`)!**

---

## 2. Technical Specifications for the Embedded ML Training Pipeline

Inside `orderflow_ml_overlay.py`, please embed the complete self-contained training and inference lifecycle:

1. **Stationary Feature Matrix (7 Core Signals)**:
   - `zc_div` (Spot vs Futures CVD divergence)
   - `long_liq_zs` & `short_liq_zs` (Liquidation Z-scores)
   - `vwap_zscore` (Distance to session VWAP normalized by standard deviation)
   - `volume_ratio` (Volume relative to rolling 96-bar mean)
   - `rsi_14` (Relative Strength Index)
   - `spot_cvd_15m` (15m Spot Cumulative Volume Delta)

2. **Causal Forward-Horizon Labeling (Zero-Lookahead)**:
   - For every candidate bar $t$ satisfying the base orderflow condition:
     * Label $y = 1$ (Win): If forward excursion reaches $+2.50\text{R}$ before hitting $-1.00\text{R}$ stop or 24-bar time decay (net of 41 bps friction).
     * Label $y = 0$ (Loss): If forward path hits stop loss or expires with $< +0.20\text{R}$ gain.
   - Forward simulation uses only price path between $t+1$ and $t+25$.

3. **Walk-Forward In-Sample Training with 72-Hour Purge**:
   - For any Out-Of-Sample test quarter starting at $t_{\text{start}}$, training data must strictly terminate at $t_{\text{purge}} = t_{\text{start}} - 72\text{h}$.
   - Zero test data snooping or leakage across window boundaries.

4. **Footprint Imbalance Integration**:
   - Include the join from `Binance_Footprint_15min` on `open_time_ms` to require `is_stacked_buy_imb >= 1` (or pass as a binary feature).

---

## 3. Manifest for `orderflow_production_suite_v2.zip`

Please compile and deliver the ZIP with:
1. `orderflow_production_engine.py` (Numba-accelerated, ATR floor `max(atr, entry*0.012)`, bar $j+1$ ratchets, max 2 concurrent positions).
2. `orderflow_ml_overlay.py` (Complete with embedded training pipeline, feature prep, and causal labeler).
3. `config.yaml` (Synchronized parameter definitions).
4. `institutional_forensic_report.pdf` (Updated executive report with reconciled math and charts).

Looking forward to downloading the consolidated ZIP!
