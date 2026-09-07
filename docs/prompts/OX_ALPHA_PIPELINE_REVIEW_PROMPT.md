# ADVERSARIAL FORENSIC AUDIT & CODE REVIEW: BINANCE HISTORICAL 15M PIPELINE
# TARGET PLATFORM: OpenAI o1 / o3 / Frontier Reasoning Model (Ox Alpha)
# AUDIT TARGET: Engine/run_historical_pipeline.py & Core Pipeline Subsystem

================================================================================
EXECUTIVE REVIEW CONTEXT & ROLE SPECIFICATION
================================================================================
You are an elite quantitative systems architect, senior Python high-frequency infrastructure engineer, and forensic data auditor.
You are tasked with conducting an exhaustive, uncompromising, adversarial code review of this institutional-grade historical data pipeline for Binance USDT-M Perpetuals and Spot data.

The system builds and maintains a continuous 15-minute dual-table backtesting database across 18 institutional assets from 2020 through present (over 3.47 million bars), enforcing zero nulls, strictly monotonic timestamps, and zero data lookahead.

================================================================================
PRIMARY ARTIFACTS INCLUDED IN THIS AUDIT PACKAGE
================================================================================
Please inspect and cross-reference the following files:
1. `Engine/run_historical_pipeline.py` (Master Orchestrator, CLI, fast-skip probe, cache management, causal repair loop)
2. `Engine/pipeline/binance_historical_fetcher.py` (Async/parallel archive downloader, ZIP unpacker, REST fallback, gap repair)
3. `Engine/pipeline/historical_metrics_processor.py` (Timeline builder, vectorised CVD, spot matching, liquidation math, volume profile)
4. `Engine/pipeline/http_client.py` (Resilient HTTP client, rate-limit backoff, retry handling, Binance 418 protection)
5. `Engine/pipeline/parquet_exporter.py` (Atomic export, schema enforcement, manifest generation, SHA256 checksums)
6. `Engine/core/schema.py` (Canonical market data schema, column types, precision, listing dates, filename templates)
7. `Engine/core/canonical_indicators.py` (Prefix-invariant indicator math: EMAs, Wilder RSI/ATR, VWAP, session CVD, Z-scores)
8. `Engine/verification/verify_parquet_integrity.py` (3-agent verification council: Schema, Statistical, OrderFlow, and causal repair)

================================================================================
CORE OPERATIONAL REQUIREMENTS & INVESTIGATION QUESTIONS
================================================================================

### 1. Smart Skip & Incremental Append Verification
- Requirement: When restarting the pipeline, if an asset is already up to date through yesterday (UTC) with zero date or time gaps, it must skip in sub-second time without hitting the network.
- Requirement: Binance publishes daily archives on a T-1 day lag (yesterday). If an asset already has historical data (e.g., from 2020 to 2 days ago), the pipeline should NOT re-download all 84 months (6 years) from scratch. It must cleanly detect the last recorded timestamp, fetch ONLY the missing tail days from Binance Vision / REST, compute the indicators with proper continuous warm-up/seeding, append to the existing dataset, verify continuity (np.diff(open_time_ms) == 900_000), and write the updated parquet atomically.
- Audit Goal: Audit the existing implementation in `existing_output_is_current()` and `run_pipeline()`. Identify any potential bugs, race conditions, edge cases (such as month boundary transitions, timezone discrepancies, leap days), and propose the cleanest production pattern for incremental fetch and append.

### 2. Causality & Prefix-Invariance (Anti-Lookahead)
- Requirement: Every indicator and feature must satisfy prefix invariance: f(x[:n])[:k] == f(x)[:k] for all k <= n.
- Audit Goal: Scrutinize `compute_ema_series`, `compute_wilder_rsi_series`, `compute_wilder_atr_series`, `compute_session_cvd`, `compute_session_vwap`, and rolling Z-score calculations. Are there any forward-looking operations, backward indexing leaks, or unshifted future values in the pipeline?

### 3. Upstream Data Ingestion, Binance 418 & Archive Parsing
- Requirement: Binance Vision monthly and daily archive structures frequently have gaps, missing days, or archive publication lags.
- Audit Goal: Audit `BinanceHistoricalFetcher._fetch_klines`, `_fetch_metrics`, and `HttpClient`. How does the system handle HTTP 404s, 429 rate limits, and 418 IP bans? Does the REST fallback in `_rest_klines` and `_repair_gaps` correctly stitch boundary bars without introducing duplicates or off-by-one timestamp errors?

### 4. Mathematical Precision, Zero Nulls & Data Imputation
- Requirement: The output master parquet must contain exactly 62 canonical columns, 0 nulls, and enforce specific decimal precisions so sub-dollar assets (DOGE, TRX, ADA) never collapse.
- Audit Goal: Audit the imputation logic in `HistoricalMetricsProcessor` for periods where official metrics were halted or missing. Are imputed values explicitly tagged via `is_imputed_metrics`? Does the liquidation engine avoid non-physical negative or infinite values?

### 5. Footprint Ladder & Volume Conservation
- Requirement: Table 2 (Footprint Ladder) must conserve volume with Table 1 (Master): sum of ladder volume for candle t must equal candle t quote/base volume.
- Audit Goal: Audit `assemble_ladder()` and the footprint merger. Does it handle mixed regimes (real aggTrades footprint vs causal synthetic ladder) correctly?

### 6. Atomic Export, Disk Governance & Verification Council
- Requirement: Exports must be fail-closed. If verification council fails or disk space is below 5 GB, no corrupt parquet must remain.
- Audit Goal: Audit `ParquetExporter`, `causal_repair()`, and `run_council()`. Does `ParquetExporter` ensure atomic writes via temporary files?

================================================================================
DESIRED AUDIT OUTPUT STRUCTURE
================================================================================
Please structure your forensic review report into the following sections:

1. Executive Verdict & Risk Score (0-100)
2. Critical Vulnerabilities & High-Priority Findings (if any)
3. Incremental Append & Fast-Skip Architecture Review (detailed code critique and optimal drop-in implementation)
4. Mathematical & Causality Verification (Prefix-invariance, indicator recursion, CVD session resets)
5. Robustness & API Hardening (Binance Vision / REST edge cases, rate limits, network failures)
6. Concrete Surgical Code Patches (Provide exact, production-ready Python diffs or complete functions)
