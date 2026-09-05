# ARENA.AI POST-A1 / A1B / A5 VERIFICATION & BTCUSDT INGEST CERTIFICATION PROMPT

> **Directive**: Copy and paste the prompt below directly into Arena.ai to execute the adversarial audit and certification for the A1, A1b, and A5 resolutions.

---

```markdown
# ADVERSARIAL AUDIT & CERTIFICATION: MITIGATION OF A1, A1B, A5 & BTCUSDT 2020–2026 RE-INGEST

We have implemented surgical mitigations for the blockers and high-severity findings documented in `docs/PIPELINE_REREVIEW_ADDENDUM.md`:
1. **A1 (Impossible Open Interest)**: Eliminated coerced zero values in `fetch_metrics` and added causal outlier filtering.
2. **A1b (Frozen Positioning Ranges)**: Detected upstream 2022 static positioning runs via run-length analysis and quarantined all 30,463 bars with `metrics_available = 0` and `is_imputed_metrics = 1`.
3. **A5 (Retry-After Cooldown Truncation)**: Removed the 600s ceiling, honoring server-directed `Retry-After` headers up to 7200s (2h safety limit).
4. **Parquet Re-Ingest**: Deleted the existing `Engine/binance_backtesting_data/` directory and executed a fresh, clean ingest of the anchor canary asset (`BTCUSDT`, 2020-09-01 -> present: 210,792 candles, 2,710,633 ladder rungs).

All updated source code, the newly generated master and ladder Parquet files, manifest, and council reports are committed to `main` at `https://github.com/kbsingh1399/Trading`.

Please fetch the raw files via Git / HTTP, verify each claim and audit probe against the codebase and Parquet data, and provide your formal certification verdict.

---

## 1. Primary References (Raw GitHub URLs)

- **Re-Review Addendum Baseline**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/docs/PIPELINE_REREVIEW_ADDENDUM.md`
- **Binance Historical Fetcher (A1 fix)**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/binance_historical_fetcher.py`
- **Historical Metrics Processor (A1 / A1b fixes)**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py`
- **HTTP Client (A5 fix)**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/http_client.py`
- **Verification Council (Agent 2 `oi_impossible_zero` check)**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py`
- **Metrics Validity Audit Probe**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/audit_probe_metrics_validity.py`
- **Offline Pipeline Test Suite**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/test_pipeline_offline.py`
- **Indicator Parity Probe**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/audit_probe_indicator_parity.py`
- **Metrics Coverage Probe**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/audit_probe_metrics_coverage.py`
- **Pipeline Orchestrator**:
  `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py`
- **Ingested BTCUSDT Manifest & Parquets**:
  - `BTCUSDT_dataset_manifest.json`: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_dataset_manifest.json`
  - `verification_report.json`: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/verification_report.json`
  - `BTCUSDT_15m_master_2020_2026.parquet`: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet`
  - `BTCUSDT_15m_footprint_ladder.parquet`: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_15m_footprint_ladder.parquet`

---

## 2. Surgical Mitigations Implemented

### A. Blocker A1: Impossible Open Interest Values
1. **Fetcher Addition Fix (`Engine/pipeline/binance_historical_fetcher.py`)**:
   - In `fetch_metrics`, replaced `primary['sum_open_interest'].fillna(0.0) + primary['_oi_usdc'].fillna(0.0)` with `.add(other, fill_value=0.0)`. NaN + NaN now remains NaN instead of being coerced to a synthetic 0.0.
   - Bounded the USDC addition strictly to `timestamp_ms >= USDC_METRICS_FLOOR` (`2023-03-01`).
2. **Processor Causal Outlier Imputation (`Engine/pipeline/historical_metrics_processor.py`)**:
   - Added causal rolling median outlier filter detecting bars where `oi_coin_raw < 0.20 * causal_med` (when local median > 1,000 BTC).
   - Applied causal forward-filling across impossible episodes, preserving continuity without lookahead.
3. **Council Agent 2 Rejection Rule (`Engine/verification/verify_parquet_integrity.py`)**:
   - Added check `oi_impossible_zero`: flags and rejects any bar with `(open_interest_k == 0) & (metrics_available == 1)`.
4. **Empirical Result**:
   - Running `audit_probe_metrics_validity.py` confirms **0 impossible OI bars** (`zero=False`). Exact 0.0 count is 0, below-median count is 0.

### B. Blocker A1b: Silently-Frozen Positioning Ranges
1. **Upstream Frozen Runs Detection (`Engine/pipeline/historical_metrics_processor.py`)**:
   - Implemented `_stale_runs_mask` helper detecting runs of $\ge 288$ bars (3 days) with identical values while `open_interest_k` changes on $\ge 90\%$ of bars.
   - Scans `ls_ratio_global`, `ls_ratio_top`, `top_account_ratio`, `taker_volume_ratio`, and derived `whale_index`.
2. **Explicit Quarantining (`is_imputed_metrics=1`, `metrics_available=0`)**:
   - Across all 30,463 bars in the 14 upstream static runs in 2022:
     - `metrics_available` is forced to `0`.
     - `is_imputed_metrics` is set to `1`.
   - The contract `is_imputed_metrics == (metrics_available == 0)` is strictly preserved across all 210,792 bars.
3. **Audit Gate Alignment (`Engine/verification/audit_probe_metrics_validity.py`)**:
   - Aligned the gate to check for *unflagged* frozen runs (`available > 0` or `imputed < len`).
   - Quarantined upstream frozen runs pass transparently with logged diagnostics: `PASS -- 210,792 rows, no impossible or unflagged frozen metrics, 14 upstream frozen runs quarantined (metrics_available=0, is_imputed=1)`. Exit code: **0**.

### C. Blocker A5: Retry-After Cooldown Truncation
1. **HTTP Client Fix (`Engine/pipeline/http_client.py`)**:
   - In `_trip_cooldown`, if the server sends a valid `Retry-After` header, it is honored directly up to a 7200s (2h) sanity ceiling, eliminating premature reconnects during Binance server cooldowns.

---

## 3. Local Verification Results

All 4 local verification probes and test suites execute cleanly:
- `python -m Engine.verification.test_pipeline_offline`: **ALL 9 SUITES PASSED in 20.2s**.
- `python -m Engine.verification.audit_probe_indicator_parity`: **0 VIOLATIONS** across 145 prefixes.
- `python -m Engine.verification.audit_probe_metrics_coverage`: **EXIT 0** ("Council now rejects partially-fabricated metrics -> fix verified in place").
- `python -m Engine.verification.audit_probe_metrics_validity`: **EXIT 0** (0 impossible OI bars, 14 upstream runs quarantined).
- Autonomous 3-Agent Council on fresh `BTCUSDT`: **ALL PASS** (Continuity=PASS, Microstructure=PASS, Schema=PASS).

---

## 4. Requested Verification Tasks

1. **Verify Source Code Changes**:
   - Inspect the diffs in `binance_historical_fetcher.py`, `historical_metrics_processor.py`, `http_client.py`, and `verify_parquet_integrity.py`.
   - Confirm that the A1, A1b, and A5 mitigations are strictly causal, robust, and free of side effects.
2. **Verify Dataset Parquets & Manifest**:
   - Inspect `BTCUSDT_15m_master_2020_2026.parquet` and `BTCUSDT_dataset_manifest.json`:
     - Confirm 0 nulls, 0 NaNs in numeric columns, 72 canonical columns.
     - Confirm that all 160 previously impossible OI bars now have valid, causally imputed values.
     - Confirm that all 30,463 bars in the 2022 frozen positioning episodes have `metrics_available == 0` and `is_imputed_metrics == 1`.
3. **Execute All Audit Probes**:
   - Run `python -m Engine.verification.audit_probe_metrics_validity` and verify exit code 0.
   - Run `python -m Engine.verification.test_pipeline_offline` and verify exit code 0.
4. **Final Certification**:
   - Provide your formal verdict on whether the pipeline is certified for the full 18-asset batch execution (`--all-symbols`).
```
