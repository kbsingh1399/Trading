# ARENA.AI MASTER PROMPT: HISTORICAL DATA PIPELINE CONSOLIDATION & ETH DATASET AUDIT

> **EXECUTIVE OBJECTIVE**: Conduct an exhaustive quantitative, mathematical, and architectural audit of the newly consolidated Binance 15m historical data pipeline (`Engine/pipeline/`) and the freshly generated **ETHUSDT** master dataset (`ETHUSDT_15m_master_2020_2026.parquet`). 
> Reviewers must verify that redundant modules were cleanly eliminated, that footprint ladder generation and in-memory streaming are mathematically lossless and causal, and provide a formal institutional pass/fail certification on whether the pipeline and the exported ETH historical data satisfy all institutional quant standards.

---

## 1. REPOSITORY & RAW GITHUB SOURCE CODE REFERENCES

To inspect production source code directly without character or context constraints, fetch from the authoritative repository:
- **Repository**: [https://github.com/kbsingh1399/Trading](https://github.com/kbsingh1399/Trading) (Branch: `main`)
- **Dual Parity Mirror**: [https://github.com/kbsingh1399/Engine_1_arena_PR](https://github.com/kbsingh1399/Engine_1_arena_PR) (Branch: `main`)

### Core Source Code Raw Links:
1. **Master Pipeline Runner**:
   [`Engine/run_historical_pipeline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py)
2. **Unified Binance Historical Fetcher & Footprint Engine**:
   [`Engine/pipeline/binance_historical_fetcher.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/binance_historical_fetcher.py)
3. **Causal Metrics & Spot Ingestion Processor**:
   [`Engine/pipeline/historical_metrics_processor.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py)
4. **Resilient Rate-Limited HTTP Client**:
   [`Engine/pipeline/http_client.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/http_client.py)
5. **Atomic Parquet Exporter & Manifest Engine**:
   [`Engine/pipeline/parquet_exporter.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/parquet_exporter.py)
6. **Package Initialization & Exports**:
   [`Engine/pipeline/__init__.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/__init__.py)
7. **Canonical Schema & Column Contract**:
   [`Engine/core/schema.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py)
8. **Autonomous 3-Agent Integrity Council**:
   [`Engine/verification/verify_parquet_integrity.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py)
9. **Offline Pipeline Test Suite (10 End-to-End Tests)**:
   [`Engine/verification/test_pipeline_offline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/test_pipeline_offline.py)
10. **Fail-Closed Gate Verification Suite (10/10 Assertions)**:
    [`Engine/verification/test_export_fail_closed.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/test_export_fail_closed.py)
11. **Metrics Validity & Quarantined Frozen-Run Audit Probe**:
    [`Engine/verification/audit_probe_metrics_validity.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/audit_probe_metrics_validity.py)

---

## 2. PIPELINE CONSOLIDATION & ARCHITECTURAL HIGHLIGHTS

Evaluate the following major architectural transitions executed in this iteration:

1. **Purge of Redundant Modules & 5-Module Canonical Enforcement**:
   - `real_footprint_engine.py`, `footprint_ladder.py`, and `tick_footprint_fetcher.py` were permanently deleted.
   - `Engine/pipeline/` now contains **strictly 5 canonical modules**:
     1. `__init__.py` (re-exports public interfaces)
     2. `binance_historical_fetcher.py` (fetching, in-memory decompressing, and ladder building)
     3. `historical_metrics_processor.py` (vectorized Table 1 feature calculation)
     4. `http_client.py` (connection pooling, exponential backoff, 418/429 protection)
     5. `parquet_exporter.py` (atomic multi-table exports + SHA-256 manifest)

2. **Unified Footprint & Ladder Engine Inside `binance_historical_fetcher.py`**:
   - Direct integration of `FIXED_MERGE_STEPS` for all 18 institutional assets (e.g. BTC $25, ETH $1.0, SOL $0.10).
   - Strict 13-column Table 2 schema compliance (`LADDER_COLUMNS`, `LADDER_DTYPES`).
   - Full vectorization of order flow geometry: `aggregate_trades_to_ladder`, `build_ladder_from_trades`, `assemble_ladder`, `synthesize_causal_ladder`, `compute_stacked_imbalances`, and `compute_value_area`.
   - In-memory ZIP streaming: `HttpClient.get_optional()` fetches compressed monthly/daily `aggTrades` archives into RAM without writing temporary archives to disk.

3. **Metrics Availability Contract Synchronization**:
   - Replaced legacy `metrics_available` flag with the canonical `is_imputed_metrics` column (`0 = official metrics available`, `1 = imputed/quarantined`).
   - Synchronized `_available_mask` in `verify_parquet_integrity.py` to evaluate `is_imputed_metrics == 0`, preventing false-positive `regime_dead_feature` rejections across historical periods where Binance Vision never published archives (e.g. ETH pre-Dec 2021).

4. **Continuous Cache Governance**:
   - `--clean-cache` operates automatically upon council certification: `cleanup_symbol_raw_cache()` wipes all raw staging `.csv`, `.zip`, and `.tmp` files from `Engine/data_cache/`, preventing storage bloat while guaranteeing atomic export isolation.

---

## 3. AUDIT OF THE SHIPPED ETHUSDT DUAL-TABLE VERIFICATION DATASET (JUNE 2026)

Evaluate the freshly generated dual-table verification dataset in `Engine/binance_backtesting_data/`:

* **Target Master Parquet (Table 1)**: `ETHUSDT_15m_master_2020_2026.parquet` (1.1 MB)
* **Target Footprint Ladder Parquet (Table 2)**: `ETHUSDT_15m_footprint_ladder.parquet` (0.9 MB)
* **Target Manifest**: `ETHUSDT_dataset_manifest.json`
* **Verification Report**: `verification_report.json`
* **Dataset Shapes & Properties**:
  * **Table 1 (Master)**: 2,879 rows × 56 canonical columns (0 nulls, 0 non-finites)
  * **Table 2 (Footprint Ladder)**: 26,540 rows × 13 canonical columns (0 nulls, 0 non-finites)
  * **Time Range**: `2026-06-01 00:00:00 UTC` -> `2026-06-30 23:30:00 UTC` (Monotonic 15-minute cadence)
  * **Candle Footprint Coverage**: Exactly 2,879/2,879 candles have empirical tick rungs (100% empirical, ZERO synthetic)
  * **Ladder Fixed Merge Step**: $1.0 price bin width for ETHUSDT
* **Council Verification Status (`verify_parquet_integrity.py`)**:
  * `Agent1:Continuity`: **PASS** (zero cadence breaks, 100% ladder coverage across all 2,879 master bars)
  * `Agent2:Microstructure`: **PASS** (volume conserved down to floating precision, `ladder volume == taker_buy + taker_sell == volume_base`, ask volume == `taker_buy_vol_btc`, delta identity verified, session and lifetime CVD verified)
  * `Agent3:Schema`: **PASS** (56/56 master columns and 13/13 ladder columns match schema dtypes, zero nulls)
* **Metrics Validity Probe (`audit_probe_metrics_validity.py`)**:
  * `0 impossible Open Interest values`
  * `0 unflagged frozen runs`
  * `All 2,879 bars carry authentic official derivatives positioning data`

---

## 4. FORMAL QUESTIONS FOR THE AUDITOR (OPUS)

Please answer the following targeted questions with high quantitative and architectural rigor:

### Question 1: Module Consolidation & Clean Architecture
Does consolidating footprint synthesis and streaming aggTrades directly into `binance_historical_fetcher.py` and deleting the 3 redundant modules achieve superior maintainability without introducing circular dependencies or violating the Single Responsibility Principle? Is the 5-module structure clean and complete?

### Question 2: Zero Lookahead & Causal Imputation
Does the 15m as-of join on `close_time_ms` ($\le \text{close\_time\_ms}$) strictly prevent post-close information leakage? Are the 14 upstream frozen metric runs and the 43,575 pre-archive bars correctly quarantined using `is_imputed_metrics == 1` so downstream ML strategies cannot accidentally trade on lookahead or fabricated features?

### Question 3: Fail-Closed Export Gate & Council Auditing
Inspect `verify_parquet_integrity.py` and `test_export_fail_closed.py`. Does the 3-agent council provide an ironclad guarantee that incomplete, corrupt, or uncertified datasets are immediately purged from disk if any assertion fails?

### Question 4: Dataset Integrity & Production Readiness
Based on the verification row count (2,879 master bars, 26,540 ladder rungs), column count (56 master / 13 ladder), zero nulls, monotonic timestamps, zero synthetic rungs, and the passing 3-agent council report, are the dual tables mathematically certified and ready for production backtesting?

---

## 5. REQUIRED OUTPUT FORMAT

Please structure your audit response as follows:
1. **Executive Verdict**: `[PASS]` or `[REVISE]`
2. **Architecture Scorecard**:
   - Module Consolidation & Directory Footprint (Score / 10)
   - Order Flow & Footprint Ladder Mathematics (Score / 10)
   - Causal Ingestion & Anti-Lookahead Guarantee (Score / 10)
   - Council Verification & Fail-Closed Gate (Score / 10)
   - Dataset Quality & Parity on ETHUSDT (Score / 10)
3. **Deep-Dive Technical Analysis**: Detailed assessment answering Questions 1 through 4.
4. **Institutional Recommendations**: Any edge-case optimizations or follow-up steps for the remaining 16 institutional assets.
