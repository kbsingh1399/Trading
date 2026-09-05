# ARENA.AI MULTI-ASSET COUNCIL SCHEMA CALIBRATION & VERIFICATION PROMPT

> **Directive**: Copy and paste the prompt below directly into Arena.ai to review the live execution findings and calibrate Council Agent 3 for the 18-asset universe.

---

```markdown
# ADVERSARIAL AUDIT: MULTI-ASSET COUNCIL CALIBRATION ON LIVE RUN (ETHUSDT §4.3 FINDINGS)

We initiated the full historical pipeline batch run across the 18-asset institutional universe starting from `2020-09-01`:
`python -m Engine.run_historical_pipeline --all-symbols --start-date 2020-09-01 --workers 16 --clean-cache`

All source code and manifests are available on `main` at `https://github.com/kbsingh1399/Trading`.

---

## 1. Live Execution Results

### [1/18] BTCUSDT — 100% PASS
- **Candles**: 210,797 (2020-09-01 00:00:00 -> 2026-09-05 19:00:00 UTC)
- **Footprint Rungs**: 2,710,652
- **Autonomous Council**: Continuity=PASS | Microstructure=PASS | Schema=PASS
- **Audit Probe**: `audit_probe_metrics_validity` PASSED (0 impossible OI, 0 unflagged frozen runs)
- **Export**: `BTCUSDT_15m_master_2020_2026.parquet` (94.2 MB) + `BTCUSDT_15m_footprint_ladder.parquet` (15.0 MB) + `BTCUSDT_dataset_manifest.json` successfully written in 0.83 min.

### [2/18] ETHUSDT — COUNCIL REJECTED (7 Findings in Agent 3)
During the validation phase of `ETHUSDT`, the Autonomous 3-Agent Council refused export with 7 findings:
```
19:30:35 [COUNCIL] ETHUSDT: Continuity=PASS | Microstructure=PASS | Schema=FAIL (7)
19:30:35   -> [Agent3:Schema] regime_dead_feature: open_interest_k is constant (nunique=1) in year 2020 despite total nunique=166897 (partially fabricated metrics)
19:30:35   -> [Agent3:Schema] regime_dead_feature: ls_ratio_global is constant (nunique=1) in year 2020 despite total nunique=160337 (partially fabricated metrics)
19:30:35   -> [Agent3:Schema] regime_dead_feature: ls_ratio_top is constant (nunique=1) in year 2020 despite total nunique=131729 (partially fabricated metrics)
19:30:35   -> [Agent3:Schema] regime_dead_feature: top_account_ratio is constant (nunique=1) in year 2020 despite total nunique=133443 (partially fabricated metrics)
19:30:35   -> [Agent3:Schema] regime_dead_feature: whale_index is constant (nunique=1) in year 2020 despite total nunique=164775 (partially fabricated metrics)
19:30:35   -> [Agent3:Schema] regime_dead_feature: oi_change_pct is constant (nunique=1) in year 2020 despite total nunique=146914 (partially fabricated metrics)
19:30:35   -> [Agent3:Schema] precision_collapse: basis_usd has only 1428 distinct values vs 148108 distinct closes
19:30:35 [GATE] ETHUSDT: council FAILED -> causal repair round 1/2
19:30:35 [GATE] ETHUSDT: no applicable causal repair for ['precision_collapse', 'regime_dead_feature']
19:30:35 [REJECT] ETHUSDT: export refused. 7 finding(s)
```

---

## 2. Forensic Root Cause Analysis

### A. Finding 1: `regime_dead_feature` on Legitimate Historical Absence
- **Binance Vision Historical Coverage**: Binance official metrics for `ETHUSDT` (and most altcoins) did not begin on `2020-09-01`. For `ETHUSDT`, the first published metrics archive from Binance begins on `2021-12-01`.
- **Processor Behavior**: For the ~11,000 bars in 2020, `historical_metrics_processor.py` correctly flagged every row with `metrics_available = 0` and `is_imputed_metrics = 1`, and populated neutral fallback constants (OI=0, LS=1.0, Whale=100.0). The dataset manifest correctly records `metrics_unavailable_fraction_by_year: {"2020": 1.0000}`.
- **Council Bug**: In `verify_parquet_integrity.py` (`Agent3:Schema`), the regime dead feature check evaluates `master.loc[y_mask, col].nunique()` over the entire calendar year 2020 without conditioning on `metrics_available == 1`. Because the entire year has zero metrics published by Binance, `y_nu == 1` while the rest of the file has `total_nu > 1`, falsely triggering `regime_dead_feature` ("partially fabricated metrics").
- **Proposed Calibration**: The check should only evaluate calendar years where actual metrics were published:
  ```python
  avail_mask = y_mask & (master["metrics_available"].to_numpy() == 1)
  if avail_mask.sum() >= 500:
      for col in metric_cols:
          if col in master:
              y_nu = master.loc[avail_mask, col].nunique()
              total_nu = master.loc[master["metrics_available"] == 1, col].nunique()
              if y_nu <= 1 and total_nu > 1:
                  out.append(Finding(A, "regime_dead_feature", ...))
  ```

### B. Finding 2: `precision_collapse` on Cointegrated `basis_usd`
- **Math & Market Dynamics**: `basis_usd = close - spot_close`.
  In ETHUSDT, spot and futures prices cointegrate tightly. Across 2020–2026, the basis spread oscillates inside a bounded band ($\pm\$10\text{--}\$15$). With $\$0.01$ tick increments, this band contains ~1,400 to 2,000 distinct price points.
- **Council Bug**: In `verify_parquet_integrity.py` (`Agent3:Schema`):
  ```python
  for col in ("ema_8", "atr_14", "basis_usd"):
      if col in master and master[col].nunique() < max(50, close_nu * 0.01):
  ```
  ETH traded across 148,108 distinct closes (`close_nu`). The threshold `close_nu * 0.01` is `1,481.08`. ETH's `basis_usd` had 1,428 unique values, which is completely natural for a cointegrated spread, but triggered `precision_collapse`.
- **Proposed Calibration**: Grouping a spread difference (`basis_usd`) with trend price-level indicators (`ema_8`, `atr_14`) is mathematically invalid. `basis_usd` should either be checked against an absolute diversity floor (e.g. `nunique >= 100` when `spot_flow_source == 'SPOT_EXACT'`) or checked relative to the basis spread range rather than `close_nu * 0.01`.

---

## 3. Questions & Deliverables Requested from Arena.ai

1. **Adversarial Verification of Findings**:
   - Confirm whether `regime_dead_feature` should be conditioned on `metrics_available == 1` to accommodate assets whose Binance Vision metrics coverage started post-2020.
   - Confirm whether `basis_usd` should be separated from the `close_nu * 0.01` precision test.
2. **Code Patch Specification**:
   - Provide the exact, surgical patch for `Engine/verification/verify_parquet_integrity.py` to correctly distinguish legitimate pre-archive historical periods from actual fabricated data.
3. **Execution Model Guidance**:
   - Please state if your environment can directly execute the full 18-symbol live download (`run_historical_pipeline.py`) or if our local machine should execute the download once the Council criteria are calibrated.
```
