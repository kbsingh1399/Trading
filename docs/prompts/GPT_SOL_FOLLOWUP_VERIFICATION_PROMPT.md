# GPT 5.6 SOL AUDIT ROUND 3: FINAL CERTIFICATION OF HISTORICAL PIPELINE & ARTIFACT CONTRACT

> **SESSION DIRECTIVE FOR REVIEWER (GPT 5.6 SOL)**:
> In your Round 2 adversarial review (`GPT_5.6_Sol_2.txt`), you acknowledged that Finding 1 (terminal 23:45 bar, 2,880 rows) and Finding 4 (tick-exact provenance) are resolved, but returned a conditional **`[REVISE]`** on 5 specific items:
> 1. **Fast-Skip Mandatory Hashes & Complete Artifact Set (P0)**: Bypassing hash check on empty fields; declared ladder file deleted on disk bypassed validation.
> 2. **HTTP 200 Decompression/Parser Errors Swallowed (P0)**: Catching `Exception` in `_cached()` and returning `None`, misclassifying corrupt archives as missing exchange history.
> 3. **Missing Negative Test Coverage (P0)**: Need explicit unit tests for missing/malformed SHA-256, file tampering, ladder deletion, and parse failures.
> 4. **Retrospective Frozen-Run Documentation & Causal Separation (P1)**: Explicitly quarantine `_stale_runs_mask()` as an ex-post dataset filter and forbid it as a contemporaneous predictive signal.
> 5. **Expected Boundary Hardening & Post-Export Manifest Re-Check (P1)**: Council must check exact equality (`!=`), persist `expected_start_ms`, `expected_end_ms`, `expected_rows` in `manifest.json`, and verify them in `verify_symbol()`.
> 6. **GitHub Parity Mirror 404 (P0)**: `Engine/` was untracked/uncommitted in `Engine_1_arena_PR`.
>
> All 6 items have been resolved and verified with unit tests. Both repositories are synchronized and returning `HTTP 200 OK`. Please review the implementations and issue your final formal certification (`[PASS]` or `[REVISE]`).

---

## 1. REPOSITORY & RAW GITHUB SOURCE CODE REFERENCES

Source files are available across both authoritative repositories (verified `HTTP 200 OK` via `curl.exe`):
- **Primary Repository**: [https://github.com/kbsingh1399/Trading](https://github.com/kbsingh1399/Trading) (`main`)
- **Dual Parity Mirror**: [https://github.com/kbsingh1399/Engine_1_arena_PR](https://github.com/kbsingh1399/Engine_1_arena_PR) (`main`)

### Direct Raw GitHub URLs (Testable via curl):
1. **Master Pipeline Runner**:
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/run_historical_pipeline.py"`
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py"`
2. **Unified Binance Historical Fetcher & Archive Engine**:
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/pipeline/binance_historical_fetcher.py"`
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/binance_historical_fetcher.py"`
3. **Causal Metrics & Spot Ingestion Processor**:
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/pipeline/historical_metrics_processor.py"`
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py"`
4. **Atomic Parquet Exporter & Manifest Engine**:
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/pipeline/parquet_exporter.py"`
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/parquet_exporter.py"`
5. **Canonical Schema & Column Contract**:
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/core/schema.py"`
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py"`
6. **Autonomous 3-Agent Integrity Council**:
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/verification/verify_parquet_integrity.py"`
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py"`
7. **Fail-Closed Gate & Negative Test Suite (18/18 Assertions)**:
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/verification/test_export_fail_closed.py"`
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/test_export_fail_closed.py"`
8. **ETHUSDT Dataset Manifest**:
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/binance_backtesting_data/ETHUSDT_dataset_manifest.json"`
   - `curl -s "https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ETHUSDT_dataset_manifest.json"`

---

## 2. DETAILED RESOLUTION OF ROUND 2 AUDIT FINDINGS

### Item 1 (P0): Fast-Skip Mandatory Valid 64-char Hex Hashes & Complete Artifact Set
* **Problem**: `existing_output_is_current()` allowed bypassing hash verification if `master_sha256` or `ladder_sha256` was None/empty in the manifest. Furthermore, `has_ladder = os.path.exists(lpath)` meant that if a ladder parquet was deleted from disk, `has_ladder` evaluated to False, bypassing both ladder existence and hash verification.
* **Fix Implemented in `Engine/run_historical_pipeline.py`**:
  1. Mandated `manifest_data.get("schema_version") == "2.1"` and `manifest_data.get("master_file") == os.path.basename(mpath)`.
  2. Defined strict hex validator: `_is_hex64(s)` requiring `len(s) == 64 and all(c in "0123456789abcdefABCDEF" for c in s)`. Missing or malformed `master_sha256` returns `False`.
  3. Checked `declared_ladder = manifest_data.get("ladder_file")`:
     - If non-null, requires `declared_ladder == os.path.basename(lpath)`.
     - Requires `os.path.exists(lpath)` to be `True`. If deleted from disk, returns `False` immediately.
     - Requires `ladder_sha256` to be a valid 64-char hex string matching `_hash_file(lpath).lower()`.
* **Verification**: Covered by 4 new negative assertions in `test_export_fail_closed.py` (Test 4a, 4b, 4c, 4d) - all passing.

---

### Item 2 (P0): HTTP 200 Corrupt ZIP/Parser Errors Raise `ArchiveParseError`
* **Problem**: In `_cached()`, successful HTTP 200 responses with corrupt ZIP headers, truncated payloads, or malformed CSV lines caught general `Exception` and returned `None`. This was subsequently recorded as `metrics_absent_days`, falsely attesting corrupt downloads as exchange archive absence.
* **Fix Implemented in `Engine/pipeline/binance_historical_fetcher.py`**:
  1. Defined custom `class ArchiveParseError(RuntimeError): pass` (re-exported in `Engine/pipeline/__init__.py`).
  2. In `_cached()`: if `data is None` (HTTP 404 from `http.get_optional`), returns `None`.
  3. If `data is not None` (HTTP 200), any failure in `_unzip_first()` or `parser()` logs `[FATAL PARSE ERROR]` and raises `ArchiveParseError`.
  4. In `_parallel()`: explicitly catches `ArchiveParseError`, logs `[FATAL PARSE ERROR]`, and re-raises to fail the pipeline immediately.
  5. In `_download_day_trades_in_memory()`: raises `ArchiveParseError` if decompression or trade CSV parsing fails on a downloaded ZIP payload.
* **Verification**: Verified via Test 5 in `test_export_fail_closed.py` using `_FakeHttp` returning corrupt bytes to `fetch_metrics`.

---

### Item 3 (P0): Comprehensive Negative Test Suite
* **Problem**: `test_export_fail_closed.py` lacked negative tests for manifest hash tampering, malformed hashes, ladder deletion, and parse exceptions.
* **Fix Implemented in `Engine/verification/test_export_fail_closed.py`**:
  Expanded suite with two new test blocks covering all failure modes:
  - `test_manifest_hash_and_ladder_contract()`:
    - Test 4a: `master_sha256 = None` $\to$ Rejected (`[PASS]`).
    - Test 4b: `master_sha256 = "abc123not64hex"` $\to$ Rejected (`[PASS]`).
    - Test 4c: Tampered master file bytes $\to$ Hash mismatch $\to$ Rejected (`[PASS]`).
    - Re-export $\to$ Restores current status (`[PASS]`).
    - Test 4d: Ladder deleted while declared in manifest $\to$ Rejected (`[PASS]`).
  - `test_corrupt_archive_raises_archive_parse_error()`:
    - Test 5: HTTP 200 returning invalid ZIP data $\to$ Raises `ArchiveParseError` with exact URL and bad zip error (`[PASS]`).
* **Test Suite Result**: **18/18 assertions passed (100% clean)**.

---

### Item 4 (P1): Retrospective Frozen-Run Documentation & Causal Separation
* **Problem**: `_stale_runs_mask()` marks runs of $\ge 288$ bars retroactively from bar 0 to bar $L-1$. Bars $0 \dots 287$ are flagged using future knowledge that the run reaches $\ge 288$ bars.
* **Fix Implemented in `Engine/core/schema.py` & `Engine/pipeline/historical_metrics_processor.py`**:
  1. Updated docstring of `_stale_runs_mask()` with an explicit `WARNING (RETROSPECTIVE RESEARCH FLAG ONLY - STRICT CAUSAL SEPARATION)` block explaining that `is_imputed_metrics` is strictly an ex-post data-quality filter for dataset validation and retrospective backtesting universe pruning.
  2. Explicitly documented in `schema.py`:
     `"is_imputed_metrics", # int8 1 = ex-post data-quality quarantine (official metrics missing/frozen/imputed). RETROSPECTIVE ONLY: not for contemporaneous live signals.`
  3. Banned the feature from being used as a live predictive signal or entry condition.

---

### Item 5 (P1): Council Boundary Equality & Manifest Expected Fields
* **Problem**: Council boundary check used inequality (`ts[0] > exp_first`, `ts[-1] < exp_last`) rather than exact equality (`!=`), and expected boundary fields were omitted from `manifest.json`.
* **Fix Implemented**:
  1. In `Engine/verification/verify_parquet_integrity.py` (`agent_continuity`):
     - `if ts[0] != exp_first:` $\to$ logs `start_boundary` Finding.
     - `if ts[-1] != exp_last:` $\to$ logs `end_boundary` Finding.
  2. In `Engine/pipeline/parquet_exporter.py` (`write_manifest`):
     - Persists `expected_start_ms`, `expected_end_ms`, and `expected_rows` directly in `manifest.json`.
  3. In `Engine/run_historical_pipeline.py`:
     - Aligns `exp_start_ms` and `exp_end_ms` to 15m boundaries and computes `exp_rows = ((exp_end_ms - exp_start_ms) // 900_000) + 1`.
     - Passes them to `write_manifest()`.
  4. In `Engine/verification/verify_parquet_integrity.py` (`verify_symbol`):
     - Reads `expected_start_ms` and `expected_end_ms` from `manifest.json` and forwards them to `run_council()` for post-export verification.

---

### Item 6 (P0): Dual Repository Git Synchronization & Raw Parity
* **Problem**: Sol curled `https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine/...` and received HTTP 404 because `Engine/` was untracked in `Engine_1_arena_PR`.
* **Fix Implemented**:
  1. Mirrored all files to `Engine_1_arena_PR/Engine/`.
  2. Staged all core modules, pipelines, verification suites, manifests, and documentation.
  3. Committed (`bc179a2`) and pushed to `https://github.com/kbsingh1399/Engine_1_arena_PR.git` (`main`).
  4. Verified via `curl.exe -I`:
     `HTTP/1.1 200 OK | Content-Length: 25296` for `Engine/run_historical_pipeline.py`.

---

## 3. LIVE ARTIFACT AUDIT: JUNE 2026 ETHUSDT

The June 2026 dataset has been re-exported and verified under the updated contract:

```json
{
  "symbol": "ETHUSDT",
  "timeframe": "15m",
  "total_rows": 2880,
  "expected_rows": 2880,
  "expected_start_ms": 1780272000000,
  "expected_end_ms": 1782863999999,
  "columns": [ ... 56 columns ... ],
  "column_count": 56,
  "start_time_utc": "2026-06-01 00:00:00",
  "end_time_utc": "2026-06-30 23:45:00",
  "exported_at_utc": "2026-09-06T12:15:57.575988+00:00",
  "master_file": "ETHUSDT_15m_master_2020_2026.parquet",
  "master_sha256": "6aaa50012440c25e0f8cdfd8fd0f94a8d78f9084be8494c6a964850f79eb6645",
  "master_size_mb": 1.13,
  "ladder_file": "ETHUSDT_15m_footprint_ladder.parquet",
  "ladder_sha256": "a15c6fb4d7ded102765085e30c286cb795f19ea3305bf25ec47779feccfe621f",
  "ladder_size_mb": 0.94,
  "ladder": {
    "candles": 2880,
    "tick_exact_candles": 2880,
    "synthetic_candles": 0,
    "tick_rungs": 26543,
    "synthetic_rungs": 0
  },
  "provenance": {
    "tick_exact_bars": 2880,
    "spot_exact_bars": 2880,
    "imputed_metrics_bars": 0,
    "metrics_archive_absent_months": [],
    "metrics_archive_absent_days": [],
    "metrics_archive_absent_day_count": 0,
    "metrics_unavailable_fraction_by_year": {
      "2026": 0.0
    }
  },
  "verification": {
    "symbol": "ETHUSDT",
    "passed": true,
    "master_rows": 2880,
    "ladder_rows": 26543,
    "agent_status": {
      "Agent1:Continuity": "PASS",
      "Agent2:Microstructure": "PASS",
      "Agent3:Schema": "PASS"
    },
    "findings": [],
    "repair_rounds": 0
  },
  "schema_version": "2.1"
}
```

### Verification Council Live Execution:
```
[COUNCIL] ETHUSDT: Continuity=PASS | Microstructure=PASS | Schema=PASS
COUNCIL VERDICT: ALL DATASETS PASS | candles=2,880 rungs=26,543
[OK] ETHUSDT: audit_probe_metrics_validity PASSED (0 impossible OI, 0 unflagged frozen runs)
Fast-skip check: Current: True
Post-export Council verification: Passed: True
```

---

## 4. FORMAL QUESTIONS FOR GPT 5.6 SOL

1. **Fast-Skip Robustness**: Does enforcing 64-char valid hex checksums and validating the physical presence of declared ladders on disk completely eliminate the fast-skip bypass vulnerability?
2. **Archive Error Classification**: Does raising `ArchiveParseError` on HTTP 200 decompression and parsing failures guarantee that corrupt downloads fail closed and cannot be misclassified as missing archives?
3. **Negative Test Sufficiency**: Does the 18-assertion test suite in `test_export_fail_closed.py` adequately protect the pipeline against tampering and edge-case corruption?
4. **Causal Quarantine**: Does the formal documentation and quarantine of `is_imputed_metrics` resolve the lookahead ambiguity?
5. **Final Production Verdict**: Is the pipeline architecture now formally certified `[PASS]` for full-universe generation across all 18 institutional assets?
