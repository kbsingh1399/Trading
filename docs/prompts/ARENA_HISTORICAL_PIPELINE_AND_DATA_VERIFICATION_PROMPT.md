# ARENA.AI MASTER PROMPT: HISTORICAL DATA INTEGRITY AUDIT & PIPELINE REBUILD VERIFICATION

> **EXECUTIVE OBJECTIVE**: Conduct an exhaustive quantitative and architectural verification of the rebuilt Binance 15m historical pipeline. Evaluate whether the previously downloaded historical datasets in `binance_backtesting_data/` are flawed/invalid, verify whether the newly implemented mitigation architecture in `Engine/run_historical_pipeline.py` and its underlying modules completely resolves all identified vulnerabilities, and provide a formal institutional certification on whether the pipeline is mathematically sound, zero-lookahead, and production-ready for full historical regeneration across all 18 institutional assets.

---

## 1. REPOSITORY & DIRECT SOURCE CODE REFERENCES

To bypass context limits and inspect raw production code, fetch directly from the authoritative repository references:
- **Repository**: [https://github.com/kbsingh1399/Trading](https://github.com/kbsingh1399/Trading) (Branch: `main`)
- **Dual Parity Mirror**: [https://github.com/kbsingh1399/Engine_1_arena_PR](https://github.com/kbsingh1399/Engine_1_arena_PR) (Branch: `main`)

### Core Module Raw Links:
1. **Pre-Build Forensic Audit**:
   [`docs/PIPELINE_REBUILD_AUDIT.md`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/docs/PIPELINE_REBUILD_AUDIT.md)
2. **Master Pipeline Orchestrator**:
   [`Engine/run_historical_pipeline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py)
3. **Vectorised Indicator Kernels**:
   [`Engine/core/canonical_indicators.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py)
4. **Relational Schema & Precision Contracts**:
   [`Engine/core/schema.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py)
5. **Causal Historical Metrics & Spot Ingestion**:
   [`Engine/pipeline/historical_metrics_processor.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py)
6. **Resilient Binance HTTP Client**:
   [`Engine/pipeline/http_client.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/http_client.py)
7. **Binance Archive & REST Fetcher**:
   [`Engine/pipeline/binance_historical_fetcher.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/binance_historical_fetcher.py)
8. **Dual-Table Footprint Ladder Generator**:
   [`Engine/pipeline/footprint_ladder.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/footprint_ladder.py)
9. **Atomic Parquet Exporter & Manifest Engine**:
   [`Engine/pipeline/parquet_exporter.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/parquet_exporter.py)
10. **Autonomous 3-Agent Integrity Council**:
    [`Engine/verification/verify_parquet_integrity.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py)
11. **Offline End-to-End Test Suite (9 Suites)**:
    [`Engine/verification/test_pipeline_offline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/test_pipeline_offline.py)

---

## 2. VERIFICATION TASK 1: FORENSIC AUDIT OF PREVIOUSLY DOWNLOADED DATA

Perform a forensic assessment on the historical Parquet files shipped prior to this rebuild in `binance_backtesting_data/` (`{symbol}_15m_master_2020_2026.parquet` and `{symbol}_15m_footprint_ladder.parquet`).

Please evaluate and answer definitively:
1. **Sub-Dollar Precision Annihilation**:
   - The legacy processor rounded price-scale indicators (ATR, EMA, VAH, basis) to fixed 1–2 decimal places.
   - On shipped files, DOGE `atr_14 == 0` on **97.0%** of bars, TRX on **99.9%**, ADA on **67.9%**, and XRP on **58.5%**. DOGE had only 73 distinct `ema_8` values across 6 years.
   - **Question**: Does this make the previous data on sub-dollar assets fundamentally corrupted and invalid for backtesting volatility-scaled stops, ATR ratchets, and trend filters?
2. **Stale Spot CVD Backward-Reuse Bug**:
   - On missing spot bars, `merge_asof(direction="backward")` copied previous candle volumes as the current spot delta (68 of 93 `UNAVAILABLE` BTC bars carried stale non-zero `spot_cvd_15m`).
   - **Question**: What was the quantitative impact of this artifact on spot-futures delta divergence (`zc_div`) and order flow confluence signals?
3. **Event Stream Timestamp Lookahead & 15m Staleness**:
   - Funding and official metrics snapshots were aligned to `open_time_ms`.
   - **Question**: Does anchoring to bar open inject 15-minute stale data into trading decisions at bar close, and does resolving to `<= close_time_ms` causally fix this?
4. **Footprint Ladder Non-Parity**:
   - Table-2 lacked `rung_source` (`int8`), rendering it impossible to distinguish between exact aggTrades ticks and synthetic rungs, and emitted imbalance flags as `int64` rather than `int8`.
   - Omitted the 8 extended microstructure features: `spot_close`, `session_vwap`, `vwap_zscore`, `volume_ratio`, `zc_div`, `long_liq_zs`, `short_liq_zs`, `liq_imbalance_ratio`.
5. **Verdict**: Must the existing Parquet files be discarded or re-generated from scratch using the new pipeline?

---

## 3. VERIFICATION TASK 2: ARCHITECTURAL REVIEW OF MITIGATION CHANGES

Review the rebuilt codebase and verify if the mitigations are mathematically sound and robust:

1. **Indicator Kernels & Prefix Invariance** ([`Engine/core/canonical_indicators.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py)):
   - Have all Python `for` loops across 200k bars been eliminated in favor of vectorised NumPy/Pandas operations?
   - Does the Wilder RMA exactly-seeded EWM implementation guarantee bit-identical parity ($\max|\Delta| = 0.0$) with the textbook recursion?
   - Is prefix-invariance mathematically guaranteed ($f(x[:n])[:k] == f(x)[:k]$ for all $k \le n$) with zero future or intra-bar leakage?
2. **Sub-Dollar Precision Contract** ([`Engine/core/schema.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py)):
   - Does storing price-denominated features at 8 decimal places (Binance tick precision), USD notionals at 2 dp, and ratios at 6 dp resolve the sub-dollar truncation without breaking the 62 legacy column contract?
3. **Causal Ingestion Contract** ([`Engine/pipeline/historical_metrics_processor.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py)):
   - Does 1:1 spot joining on `open_time_ms` with zero delta on `UNAVAILABLE` bars eliminate volume duplication?
   - Does as-of joining on `close_time_ms` ($\le \text{close\_time\_ms}$) provide maximum public information at candle close with zero future lookahead?
4. **Resilience & Rate Limit Protection** ([`Engine/pipeline/http_client.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/http_client.py)):
   - Does the shared HTTP client properly implement exponential backoff + jitter, `Retry-After` header parsing, process-wide cooldown latching on HTTP 418/429, and 404 negative caching?
5. **Dual-Table Ladder Assembly** ([`Engine/pipeline/footprint_ladder.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/footprint_ladder.py)):
   - Does vectorised run-length clustering with daily bin steps derived from the day's first traded price prevent intra-day median price lookahead?
   - Does causal synthetic fallback (`rung_source = 1`) guarantee 100% ladder coverage for historical bars preceding tick archives?
6. **Autonomous 3-Agent Integrity Council** ([`Engine/verification/verify_parquet_integrity.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py)):
   - Are the checks performed by Agent 1 (cadence & continuity), Agent 2 (causal re-derivation of session VWAP/CVD and one-step recursions), and Agent 3 (zero nulls, schema contracts, dtype bounds) sufficient to reject any corrupt or lookahead-tainted export?

---

## 4. VERIFICATION TASK 3: IS `run_historical_pipeline.py` PRODUCTION-READY & "PERFECT"?

Provide an adversarial, senior quant engineering assessment of [`Engine/run_historical_pipeline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py):

1. **Edge Case Analysis**:
   - Are there any remaining failure modes around exchange downtime gaps, daylight savings, multi-threading race conditions on the shared HTTP client, or forming-candle boundary truncation?
2. **Warm-up & Ingestion Convergence**:
   - Does fetching from 2019/listing date and slicing to the requested start date guarantee that 800-period EMAs, 100-period ATRs, and RSI-14 are fully converged?
3. **Fast-Skip Integrity**:
   - Does the updated fast-skip logic prevent stale files from masquerading as valid exports?
4. **Execution Verdict**:
   - Is `Engine/run_historical_pipeline.py` certified as production-ready, or are further code adjustments required?

---

## 5. VERIFICATION TASK 4: OPERATIONAL REGENERATION DIRECTIVE

If you certify that the previously downloaded data is flawed and that the rebuilt pipeline is correct:
1. Provide the exact recommended terminal commands to execute full historical regeneration across all 18 institutional assets from 2020 to present.
2. Outline the expected runtime, CPU/RAM footprint, and disk storage requirements.
3. Detail how the 3-Agent Verification Council should be used to validate the final exports before deploying quantitative strategies across the 20 OOS windows.
