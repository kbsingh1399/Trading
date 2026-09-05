# ARENA.AI POST-REBUILD VERIFICATION & BTCUSDT INGEST CERTIFICATION PROMPT

> **Directive**: Copy and paste the prompt below directly into Arena.ai to execute the final audit and certification.

---

```markdown
# ADVERSARIAL AUDIT & CERTIFICATION: MITIGATION OF §4.1 / §3.2 & BTCUSDT 2020–2026 INGEST

We have implemented surgical mitigations for the two blocking findings identified in your audit report (`docs/PIPELINE_VERIFICATION_CERTIFICATION.md`), purged all legacy corrupted Parquet data from `Engine/binance_backtesting_data/`, and successfully executed the live historical pipeline for the anchor canary asset (`BTCUSDT`, 2020-09-01 -> present).

All updated source code and the newly generated dataset manifest are committed to `main` at `https://github.com/kbsingh1399/Trading`.

Please fetch the raw files via Git / HTTP, verify the fixes adversarially, inspect the `BTCUSDT` dataset manifest, and provide your formal certification verdict.

---

## 1. Primary References (Raw GitHub URLs)

- **Audit & Certification Baseline**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/docs/PIPELINE_VERIFICATION_CERTIFICATION.md`
- **Canonical Schema & Column Dtypes**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py`
- **Historical Metrics Processor**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py`
- **HTTP Client & Process-Wide Cooldown Latch**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/http_client.py`
- **Parquet Exporter & Dataset Manifest Writer**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/parquet_exporter.py`
- **Autonomous 3-Agent Verification Council**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py`
- **Pipeline Orchestrator & Causal Repair**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py`
- **Audit Probes**:
  - Indicator Parity Probe: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/audit_probe_indicator_parity.py`
  - Metrics Coverage Blind-Spot Probe: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/audit_probe_metrics_coverage.py`
- **Ingested BTCUSDT Live Manifest & Council Verification Report**:
  - `BTCUSDT_dataset_manifest.json`: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_dataset_manifest.json`
  - `verification_report.json`: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/verification_report.json`
  - `BTCUSDT_15m_master_2020_2026.parquet`: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet`
  - `BTCUSDT_15m_footprint_ladder.parquet`: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_15m_footprint_ladder.parquet`

---

## 2. Implemented Mitigations for Review

### A. Blocker §4.1: Metrics Imputation Blind Spot & Regime Dead-Feature Scan
1. **Schema Extension (`Engine/core/schema.py`)**:
   - Added `is_imputed_metrics` (`int8`) to `EXTENDED_COLUMNS` (column 71) and `COLUMN_DTYPES`.
   - Populated `is_imputed_metrics = (metrics_available == 0).astype(np.int8)` in `historical_metrics_processor.py`.
2. **Council Regime-Split Dead-Feature Scan (`Engine/verification/verify_parquet_integrity.py`)**:
   - Agent 3 now segments the series by calendar year (`pd.to_datetime(ts, unit='ms', utc=True).year`).
   - For each year with $\ge 500$ bars, scans `open_interest_k`, `ls_ratio_global`, `ls_ratio_top`, `top_account_ratio`, `whale_index`, and `oi_change_pct`. If `nunique <= 1` within any year while total `nunique > 1`, flags `regime_dead_feature` and rejects the file.
   - Enforces `is_imputed_metrics != (metrics_available == 0)` consistency.
   - **Verification**: `python -m Engine.verification.audit_probe_metrics_coverage` now detects the fabricated head, rejects the dataset, and exits with **code 0** ("Council now rejects partially-fabricated metrics -> fix verified in place").
3. **Dataset Manifest Provenance**:
   - Added `imputed_metrics_bars` and `metrics_unavailable_fraction_by_year` breakdown to `provenance` in `BTCUSDT_dataset_manifest.json`.

### B. Blocker §3.2 / §4.2: Warm-up Convergence on Post-2020 Assets
1. **Schema Extension (`Engine/core/schema.py`)**:
   - Added `is_warmup_converged` (`int8`) to `EXTENDED_COLUMNS` (column 72) and `COLUMN_DTYPES`.
2. **Convergence Tracker (`historical_metrics_processor.py`)**:
   - Computes `warmup_bars = first_warmup + np.arange(len(out))`.
   - Flags `is_warmup_converged = (warmup_bars >= 3200).astype(np.int8)`.
   - Assets starting in 2020 with pre-2020 warm-up (BTC, ETH, etc., where `first_warmup = 23,520`) are 100% converged from bar 0.
   - Post-2020 listed assets (OP, SUI, ARB, APT) transparently flag their first 3,200 bars as unconverged (`is_warmup_converged == 0`).
   - Manifest explicitly records `warmup_unconverged_bars: 0` for BTCUSDT.

### C. HTTP Resilience (§2.4): Process-Wide Cooldown Latch
1. **Global Process-Wide Latch (`Engine/pipeline/http_client.py`)**:
   - Implemented class-level attributes `_global_cooldown_until: float`, `_global_lock: threading.Lock`, and `_global_not_found: Set[str]` on `HttpClient`.
   - Any rate-limit code (418/429) sets the global cooldown timestamp, which is respected across all `HttpClient` instances and threads.
   - Bounded back-off cooldown to `min(self.max_delay * 10, raw_cool)` to prevent unbounded stalls on pathological `Retry-After`.
   - Thread-safe shared 404 cache prevents redundant probes across threads and symbol iterations.

---

## 3. Verification Tasks Requested from Arena.ai

1. **Verify Blocker Resolutions**:
   - Confirm that the regime-split dead feature scan in `verify_parquet_integrity.py` correctly closes the §4.1 blind spot.
   - Confirm that `is_imputed_metrics` and `is_warmup_converged` correctly preserve backward compatibility (the first 62 legacy columns remain untouched in name, order, and dtype).
2. **Execute Audit Probes**:
   - Run `python -m Engine.verification.audit_probe_metrics_coverage` and verify exit code 0.
   - Run `python -m Engine.verification.audit_probe_indicator_parity` and verify 0 violations.
   - Run `python -m Engine.verification.test_pipeline_offline` and verify all 9 suites pass.
3. **Audit the Ingested BTCUSDT Manifest & Council Report**:
   - Inspect `BTCUSDT_dataset_manifest.json`:
     - Rows: `210,788` (2020-09-01 00:00:00 -> 2026-09-05 16:45:00 UTC).
     - Master size: `94.17 MB`, Ladder size: `14.97 MB`.
     - Columns: `72`.
     - `warmup_unconverged_bars`: `0`.
     - `metrics_unavailable_fraction_by_year`: all 0.0 except 0.0005 in 2024.
     - `verification.passed`: `true`, `repair_rounds`: `0`, findings: `0`.
4. **Final Certification**:
   - Provide your formal recommendation: is the pipeline certified for the full 18-asset universe batch run (`--all-symbols`)?
```
