# 🗺️ SESSION CONTEXT MAP: INSTITUTIONAL MEMORY & MILESTONE REGISTRY
> **Token-Optimized Context Index**: Distilled from 1.54 MB (`.agents/memory/session_chat_history.md`).
> Read this file first on every conversation boot to eliminate context amnesia with minimal token spend.

---

## 1. Core Project Objective
- **System**: Quantitative Crypto Perpetual Trading Architecture (Engine 1: CoinGlass Real-Time Parity; Engine 2: Binance 18-Asset Multi-Sleeve Walk-Forward Engine).
- **Primary Goal**: Achieve robust, verified passes across **all 20 Out-Of-Sample (OOS) Walk-Forward Windows (2021–2026)** on 18 institutional Binance USDT-M contracts (3.46M 15m candles) under **one fixed causal risk configuration** with **zero lookahead bias, zero lookup tables, and zero external status references**.
- **The Pass Criteria per Window**:
  - ROI > 20.0%
  - Max Drawdown < 5.0%
  - Win Rate > 40.0%
  - Min Trades >= 6

---

## 2. Chronological Milestones & Strategic Evolution

### Phase 1: CoinGlass Scraping & Real-Time Parity Engine (Engine 1)
- **Problem**: CoinGlass WebSocket APIs are private/obfuscated; direct REST triggers Cloudflare / reCAPTCHA.
- **Solution**: Developed Chrome CDP (Chrome DevTools Protocol) attached to live authenticated browser tabs.
- **Key Discovery**: Captured real-time CVD, open interest, and liquidation prints via viewport listeners and accumulator diffs.

### Phase 2: 18-Asset Binance Historical Data Pipeline (Engine 2)
- **Dataset**: 18 institutional assets (`BTC, ETH, XRP, SOL, BNB, DOGE, ADA, TRX, LINK, AVAX, SUI, NEAR, DOT, LTC, BCH, APT, OP, ARB` per `schema.py`; replaces legacy draft list `PEPE, WIF, TIA, INJ`).
- **Structure**: 3,467,571 15m candles with strictly monotonic timestamps, 0 nulls, and clean zeroed zc_div on UNAVAILABLE spot bars.
- **Artifacts**: Stored in `Engine_2/binance_backtesting_data/` as master parquets and footprint ladder parquets.

### Phase 3: The 20 Walk-Forward OOS Windows
- **Span**: 5 years (March 2021 to April 2026) in non-overlapping 1-month test windows.
- **Purge Gap**: Strictly enforced 72-hour trade resolution purge boundary ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$) to prevent post-entry label leakage.
- **The Regimes**:
  - W01: Early Bull Run Expansion (March 2021)
  - W02: Post-May Liquidation Crash (June 2021)
  - W04: ATH Distribution & Macro Top (Dec 2021)
  - W06: LUNA / 3AC Deleveraging (June 2022)
  - W08: Post-FTX Despair Lows (Dec 2022)
  - W13: Pre-Halving ATH Euphoria (March 2024)
  - W15: Fed 50 bps Easing Pivot (Sept 2024)
  - W20: 2026 Regime Expansion (March 2026)

### Phase 4: Forensic Audit & The 4 Empirical Root Causes of Failure
1. **The 5R Retracement Trap**: In `simulate_single_trade_path`, the stop loss stayed frozen at -1.0R until price gained +2.5R. On 15m crypto, 50.15% of liquidation trades reach +1.0R and 32.98% reach +1.5R, but only 1.75% ever reach +5.0R. Because the stop never moved, 85.8% of winning trades retraced into full stop-outs, crushing raw win rate to 22.9%.
2. **Asymmetric Risk Sizing Lockout**: Setting `BASE_RISK = 75.0` on a $225 (4.5%) drawdown budget caused 3 consecutive losses to trip the circuit breaker (`cur_risk < 5.0`), locking out trading across 19/20 windows.
3. **Falling Knives Without Absorption**: Raw liquidation spikes without Spot CVD divergence catch falling knives with median MAE of 1.12R.
4. **In-Sample Label Poisoning**: Training LightGBM on labels produced by the broken 5R simulator yielded an out-of-sample AUC of 0.487 (zero predictive power) because 77% of labels were artificial retracement losses.

### Phase 5: The Winning Mathematical Confluence Formula
- **Signal Condition**:
  $$\text{long\_liq\_zs} > 1.8 \quad \land \quad \text{zc\_div} > 0.8 \quad \land \quad \Delta\text{Spot} > 0 \quad \land \quad \Delta\text{Futures} < 0 \quad \land \quad \text{RSI} < 40 \quad \land \quad \text{VWAP Z} < -0.5$$
- **Microstructure Exit Management**:
  - Breakeven Ratchet: Move stop to entry + 0.15R at +0.8R price gain.
  - Profit Lock: Move stop to entry + 0.80R at +1.5R price gain.
  - Target: +2.5R exit.
  - Time decay: If trade fails to gain +0.2R within 24 bars (6 hours), exit at market.
- **Empirical Validation**: 18,456 trades across all 18 assets produced **54.6% Win Rate and +146.2R Net Profit**.

### Phase 6: Arena.ai External Forensic Audit & Quarantine
- **Result**: `Engine_2/s1_liquidation_cascade.py` was officially audited and verified `[CLEAN - ZERO LOOKAHEAD VERIFIED]`.
- **Quarantine**: `verify_sequential_w1_w20.py` was rejected as `[LEAKAGE DETECTED]` due to researcher selection leakage (hand-picked strategies per window, per-window risk scaling, and test-set nlargest overrides). It was permanently purged.
- **The 8 Remediation Directives (R-1 to R-8)**:
  - R-1: Quarantine manual verifiers.
  - R-2: Fix denominator defect in `s1_liquidation_cascade.py`.
  - R-3: Net-of-fee labeling (8 bps roundtrip).
  - R-4: Bar-by-bar unrealized PnL marking.
  - R-5: Portfolio-level annualized risk budgeting (Base Risk $25, House Money $50, Drawdown Limit 4.5%).

### Phase 7: Tooling & Graphify Native Integration
- **Video 1 (Mikuel)**: Configured Antigravity "Always Proceed" workflow and live phase tracking.
- **Video 2 (Graphify)**: Built `.agents/rules/graphify.md`, `/graphify`, and AST knowledge graph (7,403 nodes, 8,676 edges, 591 communities) with git post-commit hooks.
- **Dedicated Repo**: `Engine_2` isolated into its own independent GitHub repository (`https://github.com/kbsingh1399/Engine_2.git`) with full `.agents/` framework and historical backtesting datasets.

### Phase 8: Second Brain v3.0 & Complete YouTube Crux Architecture (Token-Saving Protocol)
- **Knowledge Base Expansion**: Expanded `trading_knowledge_base.md` to 23 Structured Nodes (47.6 KB) encompassing:
  - Complete verbatim transcript cruxes, setup rules, and quantitative translations for all **24 YouTube videos (208,961 characters)**.
  - Institutional Financial Machine Learning (Marcos López de Prado: Triple Barrier Method, Meta-Labeling secondary classification, CPCV with 72h Embargo, Fractional Differentiation $d^* \in (0, 1)$, Deflated Sharpe Ratio).
  - High-Frequency Microstructure & Toxicity (Kyle's Lambda price impact, Amihud illiquidity, VPIN toxicity > 0.8, Order Flow Imbalance OFI).
  - Binance Liquidation Engine Architecture (MMR tier brackets, Bankruptcy vs Liquidation price spread, Insurance Fund buffer, ADL priority queue).
  - Cross-Sectional Lead-Lag & Spillovers (BTC cascade transmission delay to 17 altcoins, relative Spot Delta alpha, beta-adjusted volatility scaling).
- **Sub-Millisecond Token-Saving Engine**: Upgraded `second_brain.py` with 4-layer instant recall (Graph Memory + Executive Milestones + Session Chat + Knowledge Base/Video Cruxes) returning targeted <600-character dossiers to eliminate token waste and context rot.

### Phase 9: Top 100 YouTube Videos & 100+ Institutional Quant Articles (Second Brain v4.0)
- **100-Video Swarm Ingestion**:
  - Pillar 1 (1-25): Order Flow, Footprint Imbalances, CVD Delta Divergence, Absorption vs Exhaustion.
  - Pillar 2 (26-50): Liquidation Cascades, Heatmaps, Binance Engine Architecture, ADL Queue Priority.
  - Pillar 3 (51-75): Financial Machine Learning, Marcos López de Prado, LightGBM vs Deep Learning, CPCV.
  - Pillar 4 (76-100): Fixed Portfolio Risk Budgeting, Anchored VWAP Bands, Walk-Forward Analysis, Deflated Sharpe Ratio.
- **100+ Institutional Articles & Social Media Quant Insights**:
  - Synthesized Reddit r/algotrading, r/quant, LinkedIn Quant Research (AQR, Two Sigma, Wintermute, FalconX, Jump Trading), and Substack newsletters into dedicated Node 29.
- **Lifecycle Integrity**: Temporary staging folder (`.agents/memory/captions_temp/`) created, processed, and 100% purged automatically upon distillation.
- **Master Knowledge Base v4.0**: Expanded to **29 Nodes (68.1 KB, 779 lines)**. Fully indexed in `second_brain.py`.

### Phase 10: 18-Asset Production Parquet Ingestion, Verification Council 100% Pass, and Arena.ai Audit Deployment
- **Dataset Rebuild**: Clean restart and regeneration from 2020-09-01 across all 18 institutional assets (3,467,571 15m bars, 71,134,532 footprint rungs, 0 nulls, strictly monotonic timestamps).
- **Dual-Gate Certification**:
  - Autonomous 3-Agent Integrity Council (`verify_parquet_integrity.py`): 18/18 PASS (Continuity=PASS, Microstructure=PASS, Schema=PASS, 0 findings).
  - Metrics Validity Gate (`audit_probe_metrics_validity.py`): 18/18 PASS (0 impossible OI, 0 unflagged frozen metrics, authentic pre-archive gaps quarantined with `is_imputed=1`).
- **Complete GitHub Inventory**: All 55 artifacts (18 master parquets, 18 ladder parquets, 18 manifests, 1 verification report) uploaded and tracked on GitHub across both `main` and `arena/01a07263-trading` mirrors.
- **Arena Audit Suite**: Authored [`docs/prompts/ARENA_18_ASSET_AND_PIPELINE_COMPLETE_AUDIT_PROMPT.md`](file:///c:/Users/SIGMA/Documents/Trading/docs/prompts/ARENA_18_ASSET_AND_PIPELINE_COMPLETE_AUDIT_PROMPT.md) equipped with direct raw GitHub asset URLs, row-by-row mathematical verification recipes, and fail-closed architecture mandates ready for external adversarial certification.

### Phase 11: Arena Round 5 Formal Certification & Zero-Lookahead Approval
- **Adversarial Audit Verdict**: External forensic review by Arena.ai published in [`docs/PIPELINE_CERTIFICATION_ROUND5.md`](file:///c:/Users/SIGMA/Documents/Trading/docs/PIPELINE_CERTIFICATION_ROUND5.md) and [`Engine/verification/forensic_audit_all18.json`](file:///c:/Users/SIGMA/Documents/Trading/Engine/verification/forensic_audit_all18.json).
- **Audit Findings & Quant Invariants**:
  - Exactly 3,467,571 master bars and 70,934,532 footprint rungs verified across all 18 assets.
  - 0 structural, 0 integrity (72 columns x 18 files finite/null-free), 0 domain, 0 ladder, and 0 causal lookahead violations.
  - Zero lookahead verified across all features: session VWAP, session CVD, EMA8, volume SMA9, volume ratio, and liq imbalance ratio match independent from-scratch recomputations to 5e-9.
  - 18/18 independent 3-Agent Council PASS (`verify_parquet_integrity.py`).
- **Fail-Closed Hardening**: Merged Arena's fail-closed export hardening (`Engine/pipeline/parquet_exporter.py`, `Engine/run_historical_pipeline.py`, `Engine/verification/test_export_fail_closed.py` 3/3 PASS).
- **Test Suite Perfection**: Offline pipeline tests (`python -m Engine.verification.test_pipeline_offline`) passed 10/10 in 31.2s; independent local forensic tool (`audit_full_dataset_forensic.py --council`) verified 18/18 PASS.
- **Remote Parity**: Commits `929b6c8` and `25e7055` merged and pushed with 100% byte-for-byte dual mirror parity on GitHub.


