# ARENA.AI DATA QUALITY & CONTINUITY AUDIT PROMPT

> **SYSTEM DIRECTIVE FOR ARENA.AI QUANTITATIVE DATA ENGINEER & FORENSIC AUDITOR:**
> You are acting as a senior institutional quantitative data engineer and microstructure forensic auditor.
> Your task is to perform an exhaustive, independent review of the 18-asset Binance USDT-M perpetual backtesting dataset located in `Engine/binance_backtesting_data` in the `kbsingh1399/Trading` repository.
>
> Your objective is to verify whether this dataset is **clean, contiguous, monotonic, mathematically sound, and free of lookahead bias or data corruption**, satisfying Tier-1 quantitative standards for out-of-sample walk-forward backtesting (2020–2026).
>
> All source code, manifests, and verification reports are live on GitHub:
> `https://github.com/kbsingh1399/Trading`

---

## 1. RAW GITHUB REFERENCES (FETCH DIRECTLY)

Please retrieve and inspect the following source files and manifests directly via their raw GitHub URLs:

1. **Multi-Agent Dataset Verification Report (All 18 Assets)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/verification_report.json`
2. **Sample Asset Manifests (Provenance, Row Counts, SHA256 Hashes)**:
   - **BTC**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_dataset_manifest.json`
   - **ETH**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ETHUSDT_dataset_manifest.json`
   - **SOL**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SOLUSDT_dataset_manifest.json`
   - **DOGE**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOGEUSDT_dataset_manifest.json`
   - **SUI**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SUIUSDT_dataset_manifest.json`
3. **Master Production Ingest & Pipeline Orchestrator**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py`
4. **Canonical Data Contracts & Column Schema**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/schema.py`
5. **Technical & Microstructure Indicator Engine**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/indicators.py`
6. **Automated Parquet Integrity Verification Script**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py`
7. **Incremental Append & Continuity Updater**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/incremental_append.py`

---

## 2. DATASET ARCHITECTURE & SPECIFICATIONS

### The 18-Asset Institutional Universe
- **18 Binance USDT-M Perpetual Contracts**:
  `BTCUSDT, ETHUSDT, XRPUSDT, SOLUSDT, BNBUSDT, DOGEUSDT, ADAUSDT, TRXUSDT, LINKUSDT, AVAXUSDT, SUIUSDT, NEARUSDT, DOTUSDT, LTCUSDT, BCHUSDT, APTUSDT, OPUSDT, ARBUSDT`.
- **Temporal Horizon**: September 1, 2020 00:00:00 UTC through September 6, 2026 16:30:00 UTC.
- **Total Depth**: 3,467,571 15-minute bars across the 18 symbols.
  - 14 assets provide complete 6-year continuous coverage (210,883 to 210,912 bars each).
  - 4 newer assets begin at their verified Binance perpetual listing date:
    - `OPUSDT`: June 1, 2022 (148,000+ bars)
    - `APTUSDT`: October 19, 2022 (136,296 bars)
    - `ARBUSDT`: March 23, 2023 (121,364 bars)
    - `SUIUSDT`: May 3, 2023 (116,928 bars)

### Dual-Table Partitioning Per Symbol
1. **Master Table (`{symbol}_15m_master_2020_2026.parquet`)** — 56 synchronous columns:
   - **OHLCV**: `open`, `high`, `low`, `close`, `volume_base`, `volume_quote`, `volume_sma9`, `trade_count`.
   - **Moving Averages & Oscillators**: `rsi_14`, `atr_14`, `atr_100`, `ema_8`, `ema_21`, `ema_50`, `ema_200`, `ema_800`.
   - **CVD Streams**: `future_cvd_15m` (discrete bar delta), `future_cvd_session` (daily session cumsum), `future_cvd_lifetime`, `spot_cvd_15m`, `spot_cvd_session`, `spot_cvd_lifetime`.
   - **Derivatives & Macro Metrics**: `funding_rate_pct`, `basis_usd`, `open_interest_k`, `open_interest_usd`, `oi_change_pct`.
   - **Liquidation Engine**: `long_liq_usd`, `short_liq_usd`, `long_liq_zs`, `short_liq_zs`, `liq_imbalance_ratio`.
   - **Taker & Order Flow Metrics**: `taker_buy_count`, `taker_sell_count`, `taker_buy_vol_btc`, `taker_sell_vol_btc`, `taker_volume_ratio`, `avg_trade_size_usd`, `whale_index`.
   - **Trader Positioning**: `ls_ratio_global`, `ls_ratio_top`, `top_account_ratio`.
   - **Session Profile**: `session_vah`, `session_val`, `session_vwap`, `vwap_zscore`, `prev_day_vah`, `prev_day_val`.
   - **Confluence Divergence**: `zc_div` (CVD vs price divergence z-score).
2. **Footprint Ladder Table (`{symbol}_15m_footprint_ladder.parquet`)**:
   - Intra-candle price ladder bins capturing order flow distribution:
   - Columns: `open_time_ms`, `price_bin`, `bid_vol_coin`, `ask_vol_coin`, `net_delta_coin`, `total_vol_coin`, `trade_count`, `is_poc`, `is_buy_imbalance`, `is_sell_imbalance`, `is_stacked_buy_imb`, `is_stacked_sell_imb`, `is_value_area`.

---

## 3. AUDIT SCOPE & QUESTIONS FOR ARENA.AI

Please conduct a rigorous, line-by-line forensic assessment addressing the following 6 dimensions:

### Dimension 1: Continuity, Contiguity & Monotonicity
- Are the timestamps (`open_time_ms` and `datetime_utc`) strictly monotonic with zero backward jumps?
- Is there any missing candle gap (where $t_{i+1} - t_i \ne 900,000\text{ ms}$)?
- Are there duplicate timestamps anywhere in the master or footprint tables?
- Does the transition across Binance API maintenance periods or leap seconds maintain contiguity?

### Dimension 2: Missingness, Nulls & Extreme Value Sanity
- Are there any NaN, null, None, or infinite values in any of the 56 columns across the 3.47M rows?
- Do the volume, high/low, and close columns obey physical invariants:
  - `high >= max(open, close)` and `low <= min(open, close)`?
  - `volume_base >= 0` and `trade_count >= 0`?
  - `bid_vol_coin + ask_vol_coin == total_vol_coin` in the footprint ladder?

### Dimension 3: Lookahead Bias & Causal Rolling Operators
- In `Engine/pipeline/indicators.py`, inspect the rolling calculations (EMA, ATR, RSI, VWAP z-score, liquidation z-scores):
  - Do all rolling windows use strictly backward-looking slices (`.rolling(W)` with no negative shifts)?
  - Is `session_vwap` and `session_vah / session_val` cleanly reset at 00:00:00 UTC every day, or does any future session information leak into the current day's bars?
  - In `zc_div`, is the price-CVD divergence calculated purely from causal historical data?

### Dimension 4: Liquidation & Derivatives Imputation Hygiene
- Binance Historical Archive occasionally experiences gaps in derivatives metrics (e.g. open interest or liquidation reports during early 2022).
- Inspect the imputation logic in `run_historical_pipeline.py` (flagged by `is_imputed_metrics`):
  - Is the forward-fill / causal imputation methodology valid?
  - Does it introduce synthetic lookahead or distort indicator z-scores?

### Dimension 5: Footprint Ladder Order Flow Quality
- Inspect `{symbol}_15m_footprint_ladder.parquet`:
  - Are price bins sized appropriately per asset tick-size (e.g., $0.10 for BTC, $0.0001 for DOGE)?
  - Are the Point of Control (`is_poc`) and stacked imbalance flags (`is_stacked_buy_imb`, `is_stacked_sell_imb`) logically consistent?
  - Is the order flow data sufficient for computing institutional absorption signatures (`wick_sell_absorb`, `sell_impact`, `poc_shift`) without binning artifacts?

### Dimension 6: Final Institutional Verdict & Recommendations
- Does this dataset pass Tier-1 quantitative standards for institutional research, multi-symbol portfolio backtesting, and machine learning meta-labeling?
- Are there any remaining data risks, hidden pitfalls, or recommended feature enhancements before running full 20-window walk-forward evaluations?

---

*Please structure your response with an Executive Scorecard (Pass/Fail per Dimension), Detailed Forensic Findings, and Actionable Data Recommendations.*
