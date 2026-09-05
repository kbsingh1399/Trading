# ARENA.AI MASTER PROMPT: 18-ASSET DATASET INTEGRITY & PRODUCTION PIPELINE FINAL AUDIT

> **EXECUTIVE OBJECTIVE**: Conduct an adversarial, forensic audit of the completed 18-asset historical backtesting dataset dumped in `Engine/binance_backtesting_data/` and the master production orchestrator `Engine/run_historical_pipeline.py`. Verify whether all 18 institutional assets are mathematically sound, continuous, causal (zero-lookahead), and fully compliant with the 3-Agent Integrity Council and Metrics Validity Gates before beginning Walk-Forward Optimization across the 20 Out-Of-Sample (OOS) Windows (2021–2026).

---

## 1. REPOSITORY & DIRECT GIT REFERENCES

To bypass context caps and review production code and dataset manifests directly, fetch from the authoritative repository:
- **Repository**: [https://github.com/kbsingh1399/Trading](https://github.com/kbsingh1399/Trading) (Branch: `main`)
- **Dual Mirror**: [https://github.com/kbsingh1399/Trading/tree/arena%2F01a07263-trading](https://github.com/kbsingh1399/Trading/tree/arena%2F01a07263-trading)
- **Active Commit**: `21909f836a6c1ba0aa6800d9ff9fcda7b3decddf`

### Core Source Code Raw Links:
1. **Pipeline Orchestrator**:
   [`Engine/run_historical_pipeline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py)
2. **Causal Metrics Processor**:
   [`Engine/pipeline/historical_metrics_processor.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py)
3. **Binance Archive & REST Ingest**:
   [`Engine/pipeline/binance_historical_fetcher.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/binance_historical_fetcher.py)
4. **Dual-Table Footprint Ladder Generator**:
   [`Engine/pipeline/footprint_ladder.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/footprint_ladder.py)
5. **Atomic Parquet Exporter**:
   [`Engine/pipeline/parquet_exporter.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/parquet_exporter.py)
6. **Resilient Rate-Limited HTTP Client**:
   [`Engine/pipeline/http_client.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/http_client.py)
7. **Autonomous 3-Agent Integrity Council**:
   [`Engine/verification/verify_parquet_integrity.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py)
8. **Metrics Validity Gate**:
   [`Engine/verification/audit_probe_metrics_validity.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/audit_probe_metrics_validity.py)
9. **Offline Unit & Integration Test Suite**:
   [`Engine/verification/test_pipeline_offline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/test_pipeline_offline.py)

### Dataset Manifests & Audit Reports:
- **Council Master Report**:
  [`Engine/binance_backtesting_data/verification_report.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/verification_report.json)
- **Individual Asset Manifests**:
  - BTC: [`BTCUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_dataset_manifest.json)
  - ETH: [`ETHUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ETHUSDT_dataset_manifest.json)
  - SOL: [`SOLUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SOLUSDT_dataset_manifest.json)
  - BNB: [`BNBUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BNBUSDT_dataset_manifest.json)
  - XRP: [`XRPUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/XRPUSDT_dataset_manifest.json)
  - DOGE: [`DOGEUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOGEUSDT_dataset_manifest.json)
  - ADA: [`ADAUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ADAUSDT_dataset_manifest.json)
  - TRX: [`TRXUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/TRXUSDT_dataset_manifest.json)
  - LINK: [`LINKUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/LINKUSDT_dataset_manifest.json)
  - AVAX: [`AVAXUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/AVAXUSDT_dataset_manifest.json)
  - SUI: [`SUIUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SUIUSDT_dataset_manifest.json)
  - NEAR: [`NEARUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/NEARUSDT_dataset_manifest.json)
  - DOT: [`DOTUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOTUSDT_dataset_manifest.json)
  - LTC: [`LTCUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/LTCUSDT_dataset_manifest.json)
  - BCH: [`BCHUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BCHUSDT_dataset_manifest.json)
  - APT: [`APTUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/APTUSDT_dataset_manifest.json)
  - OP: [`OPUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/OPUSDT_dataset_manifest.json)
  - ARB: [`ARBUSDT_dataset_manifest.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ARBUSDT_dataset_manifest.json)

---

## 2. AUDIT MANDATE 1: FORENSIC VERIFICATION OF THE DUMPED DATASETS

Examine the 18 dataset manifests and `verification_report.json`. Answer the following forensic questions:

1. **Universe Completeness & Bar Coverage**:
   - The master backtest files cover `2020-09-01` to `2026-09-05` (totaling 3,467,571 15-minute bars and 70,934,532 order-book footprint ladder rungs across 18 symbols).
   - Symbols listed post-2020 (`APTUSDT` 2022-10, `OPUSDT` 2022-06, `ARBUSDT` 2023-03, `SUIUSDT` 2023-05) start cleanly at their respective contract listing dates.
   - **Question**: Are there any internal bar cadence gaps, non-monotonic timestamps, or missing 15-minute intervals in any of the 18 master parquets?
2. **Pre-Archive Absent Metrics Contract (§4.1 / A5 Resolution)**:
   - Binance Vision did not publish official metrics (`metrics_` tables) for altcoins during late 2020 / early 2021.
   - The pipeline captures non-circularly attested 404 observations into `provenance.metrics_archive_absent_months` and passes them to `verify_parquet_integrity.py` and `audit_probe_metrics_validity.py`.
   - **Question**: Does this attestation contract strictly prevent synthetic data fabrication while properly allowing authentic pre-archive periods to be marked as `is_imputed = 1`?
3. **Quarantined Upstream Frozen Positioning & Zero Open Interest**:
   - Upstream Binance anomalies (14 frozen snapshot runs on legacy assets, and pre-archive zero OI) are explicitly quarantined with `is_imputed = 1` and `open_interest = 0.0`.
   - **Question**: Does this ensure that strategy indicators (such as `oi_change` or `long_liq_zs`) do not fire spurious liquidation signals during exchange data outages or pre-archive windows?
4. **Order Book Footprint Ladder Dual-Table Integrity**:
   - `*_15m_footprint_ladder.parquet` files contain exact `rung_source = 0` (aggTrades ticks) and causal `rung_source = 1` (synthetic rungs from OHLCV).
   - **Question**: Is the daily dynamic price binning causal (derived from the day's first traded price rather than intraday lookahead), and are imbalance flags correctly cast as `int8`?
5. **Sub-Dollar Precision Contract**:
   - Price-denominated indicators on sub-dollar assets (`DOGE`, `TRX`, `ADA`, `XRP`) are stored at 8 decimal places rather than truncated to 2 dp.
   - **Question**: Are ATR, EMA, and VWAP bands preserved with high precision, completely eliminating the 0.0 ATR truncation bug?

---

## 3. AUDIT MANDATE 2: ADVERSARIAL REVIEW OF `run_historical_pipeline.py`

Perform an adversarial architectural review of [`Engine/run_historical_pipeline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py) and its pipeline modules:

1. **Fail-Closed Verification Gate Sequencing**:
   - The manifest is written immediately after exporting parquets, followed by synchronous execution of `verify_all_parquets()`.
   - If verification fails, the pipeline purges all generated files for that symbol and raises a hard exception.
   - **Question**: Does this guarantee that no corrupted or unverified dataset can ever persist on disk or be loaded into backtesting?
2. **Strict Causality & Zero-Lookahead Guarantees**:
   - `historical_metrics_processor.py` joins spot and metrics using `<= close_time_ms` as-of logic, with zero backward filling on missing delta bars (`.bfill()` strictly eliminated).
   - **Question**: Is there any possibility of future bar information bleeding into previous bars?
3. **Resilience & Rate-Limiting**:
   - `http_client.py` enforces exponential backoff, jitter, a 5.0-second floor on `Retry-After`, and process-wide latched cooldowns on HTTP 418/429.
   - **Question**: Are concurrent downloads (up to 16 workers) protected against IP ban or connection starvation?
4. **Idempotence & Multi-Process Concurrency**:
   - Fast-skip logic validates schema, bar count, and manifest checksum before skipping already-processed assets.
   - **Question**: Does the pipeline operate deterministically across re-runs?

---

## 4. AUDIT MANDATE 3: FORMAL INSTITUTIONAL CERTIFICATION

Provide a clear, definitive institutional certification report with:
1. **Per-Asset Audit Verdict**: A summary table of all 18 assets assessing:
   - Data Continuity & Row Counts
   - Microstructure & Footprint Ladder Integrity
   - Schema & Precision Compliance
   - Metrics Validity & Quarantine Verification
2. **Pipeline Architecture Verdict**:
   - Is `Engine/run_historical_pipeline.py` approved as an institutional-grade, zero-lookahead pipeline?
3. **Readiness for Walk-Forward Optimization**:
   - Are these 18 master datasets certified for the 20 Out-Of-Sample (OOS) regime backtests in `Engine_2/s1_liquidation_cascade.py`?
