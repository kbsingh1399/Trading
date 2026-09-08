# ARENA.AI RESEARCH AUDIT PROMPT: 18-ASSET BINANCE MASTER DATASET & QUANT EXECUTION ENGINE

> **SYSTEM DIRECTIVE FOR ARENA.AI QUANTITATIVE ARCHITECT & FORENSIC AUDITOR:**
> You are acting as an elite quantitative researcher and institutional high-frequency data auditor. 
> Your task is to perform an exhaustive, forensic review of the 18-asset Binance USDT-M perpetual historical dataset and quantitative execution infrastructure in the `kbsingh1399/Trading` repository.
>
> All source code and verification artifacts are live on GitHub:
> `https://github.com/kbsingh1399/Trading`

---

## 1. RAW GITHUB REFERENCES (FETCH DIRECTLY)

Please retrieve and inspect the following source files directly via their raw GitHub URLs:

1. **Dataset Verification Report (All 18 Assets Verified)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/verification_report.json`
2. **Canonical Data Pipeline & Indicator Computation Engine**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py`
3. **Continuous Pipeline & Data Append Logic**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/incremental_append.py`
4. **Data Integrity & Schema Verification Engine**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py`
5. **Single-Asset Execution Kernel (Causal Benchmark)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/execution_kernel.py`
6. **Multi-Asset Portfolio Execution Kernel (Max 2 Concurrent, Shared $5k Equity)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/portfolio_execution_kernel.py`
7. **Pooled Institutional Meta-Labeler (Lopez de Prado Secondary Layer)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/ml/pooled_meta_labeler.py`
8. **Multi-Asset 20-Window Walk-Forward Runner**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/runners/multi_asset_walk_forward_runner.py`
9. **Strategy 1: Liquidation Cascade Simulator**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/s1_liquidation_cascade.py`
10. **Target Out-of-Sample Validation Criteria**:
    `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/target_oos_criteria.json`
11. **20 Canonical Non-Overlapping Out-of-Sample Windows**:
    `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/oos_windows_20.json`

---

## 2. THE BACKTESTING DATASET SPECIFICATION

### Universe & Dimensions
- **18 Institutional Binance USDT-M Perpetual Assets**:
  `BTCUSDT, ETHUSDT, XRPUSDT, SOLUSDT, BNBUSDT, DOGEUSDT, ADAUSDT, TRXUSDT, LINKUSDT, AVAXUSDT, SUIUSDT, NEARUSDT, DOTUSDT, LTCUSDT, BCHUSDT, APTUSDT, OPUSDT, ARBUSDT`.
- **Temporal Depth**: September 1, 2020 through September 6, 2026 (~3,467,571 continuous 15-minute bars across the universe).
  - 14 assets provide complete 6-year historical coverage from September 2020.
  - 4 assets joined upon Binance listing: `OPUSDT` (June 2022), `APTUSDT` (October 2022), `ARBUSDT` (March 2023), `SUIUSDT` (May 2023).
- **Data Quality Invariants**:
  - 0 NaN / null values across all columns.
  - Strictly monotonic, contiguous 15m timestamps (`datetime_utc`).
  - Zero duplicate timestamps.
  - Triple-verified via 3 autonomous verification agents (Continuity, Microstructure, Schema) — all 18 assets received 100% PASS in `verification_report.json`.

### Dual-Table Partitioning Per Asset
Each asset is partitioned into two specialized Parquet files:
1. **Master Table (`{symbol}_15m_master_2020_2026.parquet`)** — 56 synchronous columns:
   - **OHLCV**: `open`, `high`, `low`, `close`, `volume_base`, `volume_quote`, `volume_sma9`, `trade_count`.
   - **Moving Averages & Oscillators**: `rsi_14`, `atr_14`, `atr_100`, `ema_8`, `ema_21`, `ema_50`, `ema_200`, `ema_800`.
   - **CVD Streams**: `future_cvd_15m` (bar delta), `future_cvd_session` (session cumsum), `future_cvd_lifetime`, `spot_cvd_15m`, `spot_cvd_session`, `spot_cvd_lifetime`.
   - **Macro & Derivatives Metrics**: `funding_rate_pct`, `basis_usd`, `open_interest_k`, `open_interest_usd`, `oi_change_pct`.
   - **Liquidation Engine**: `long_liq_usd`, `short_liq_usd`, `long_liq_zs` (rolling z-score), `short_liq_zs` (rolling z-score), `liq_imbalance_ratio`.
   - **Order Flow & Taker Flow**: `taker_buy_count`, `taker_sell_count`, `taker_buy_vol_btc`, `taker_sell_vol_btc`, `taker_volume_ratio`, `avg_trade_size_usd`, `whale_index`.
   - **Trader Positioning**: `ls_ratio_global`, `ls_ratio_top`, `top_account_ratio`.
   - **Session Profile**: `session_vah`, `session_val`, `session_vwap`, `vwap_zscore`, `prev_day_vah`, `prev_day_val`.
   - **Confluence Divergence**: `zc_div` (CVD vs price z-score divergence).
2. **Footprint Ladder Table (`{symbol}_15m_footprint_ladder.parquet`)**:
   - Order-book/tick-level execution aggregated into discrete price bins per 15m candle:
   - Columns: `open_time_ms`, `price_bin`, `bid_vol_coin`, `ask_vol_coin`, `delta_vol_coin`, `bid_trade_count`, `ask_trade_count`.

---

## 3. QUANTITATIVE EXECUTION & VALIDATION CONSTRAINTS

### Target Pass Criteria (`target_oos_criteria.json`)
The system evaluates strategies across **20 non-overlapping 1-month out-of-sample (OOS) windows (2021–2026)**.
To pass an OOS window, the strategy must satisfy simultaneously:
- **Min ROI**: `> 20.0%`
- **Max Drawdown**: `< 5.0%` (Hard circuit breaker triggers at `4.5%` / `$225` on `$5,000` capital)
- **Min Win Rate**: `> 40.0%`
- **Min Trade Count**: `>= 6` completed trades per window

### Institutional Execution Rigor
- **Causal Execution**: Signals calculated at bar $j$ close can only enter at `Open[j+1]`.
- **Friction Modeling**: 8 bps taker fee, 10 bps entry slippage, 15 bps exit/stop slippage (total round-trip friction: 33 bps).
- **Conservative Stop-First Resolution**: If both stop and target price levels fall within the high-low range of the same 15m candle, the stop is unconditionally executed first.
- **Microstructure Ratchet Suite**:
  - Arm at `+0.8R` $\to$ move stop to Breakeven (`Entry + 0.15R`).
  - Arm at `+1.5R` $\to$ move stop to Profit Lock (`Entry + 0.80R`).
  - Target exit: Fixed `+2.5R`.
  - Time decay: Exit at market if position fails to gain `+0.2R` within 24 bars (6 hours).
- **Portfolio Governors**: Max 2 concurrent positions across all 18 symbols simultaneously. Shared `$5,000` portfolio equity.

---

## 4. THE EMPIRICAL PROBLEM & AUDIT QUESTIONS

### Context: Window 1 (May 2021 Liquidation Crash) Diagnostic Results
When we executed Strategy 1 (Liquidation Cascade) across the pooled 18-asset dataset for Window 1 using the pooled XGBoost meta-labeler:
- **Pooled Training Set**: 1,886 events (Base positive rate: 38.7%).
- **Cross-Validation AUC**: `0.5015` (equivalent to a random coin flip!).
- **OOS Window 1 Performance**:
  - Total Trades: 25
  - Win Rate: 44.0% (Passed > 40%)
  - Max Drawdown: 4.71% (Passed < 5.0%)
  - PnL: -$84.58 (ROI: -1.69% $\to$ **FAILED target of > 20%**).

### Specific Questions for Arena.ai:

1. **Schema & Indicator Provenance Audit**:
   - In `run_historical_pipeline.py`, inspect how `long_liq_zs`, `short_liq_zs`, `future_cvd_15m`, `spot_cvd_15m`, and `vwap_zscore` are computed. Are there any lookahead biases, boundary leakage, or rolling window misalignments?
   - Is `spot_cvd_15m` truly a discrete 15-minute delta, or does it accumulate over session boundaries?

2. **The "Coin-Flip" Meta-Labeling Paradox (CV-AUC = 0.502)**:
   - Why did XGBoost achieve exactly 0.502 CV-AUC on 1,886 pooled liquidation events?
   - Our diagnostic revealed that signed features (`dist_to_vwap_zs`, `cvd_zs`, `body_ratio`, `ret_zs`) were fed into a single classifier predicting `y \in {0, 1}` (triple-barrier hit) across both Long and Short trades. When we tested direction-aligned features (`feature * side`), CV-AUC was still `0.486 - 0.504`.
   - Feature correlations with `y` were almost entirely near zero (between -0.03 and +0.03).
   - What features from the 56 master columns and footprint ladder table actually contain predictive power for post-liquidation mean-reversion versus liquidation continuation?

3. **Footprint Ladder Utilization**:
   - We currently store 15m footprint ladder files (`{symbol}_15m_footprint_ladder.parquet`) with bid/ask volume by price bin, but the current `PooledInstitutionalMetaLabeler` only uses the master table.
   - How can we extract high-signal order flow features from the footprint ladder (e.g. delta absorption, stacked imbalances, trapped traders, volume point of control migration) to boost CV-AUC above 0.58?

4. **Multi-Asset Concentration & Capital Allocation**:
   - In `portfolio_execution_kernel.py`, we enforce `max_positions = 2`.
   - With 18 symbols generating signals, how should signals competing for the 2 slots be ranked? Is cross-sectional probability ranking (`proba`) sufficient, or should we incorporate relative volatility scaling (ATR) and correlation-based exclusion (e.g., never hold BTC and ETH simultaneously if an alt setup has higher idiosyncratic delta)?

5. **Actionable Code Deliverables**:
   - Provide concrete, mathematically rigorous code improvements for:
     a) Feature engineering in `Engine/ml/pooled_meta_labeler.py`.
     b) Signal ranking and primary trigger conditions in `Engine/strategy/s1_liquidation_cascade.py`.
     c) Footprint ladder aggregation helper to extract trapped trader imbalances.

---
*Please deliver a comprehensive, mathematically rigorous quantitative review with concrete code updates.*
