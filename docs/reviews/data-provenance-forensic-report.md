# Forensic data provenance report

Audit date: 2026-09-07. Workspace: C:/Users/SIGMA/Documents/Trading.

**Verdict: numerical integrity passed the checks described below; causal provenance is NOT certified. Do not scale optimization on these artifacts until the blocking repairs are verified.**

This report is based on source inspection, a fresh full master-row scan, manifest/hash verification, and small executable probes. Historical certification documents were treated as leads, not proof. No production pipeline, strategy source, or parquet was modified.

## 1. Scope and evidence

Reviewed run_historical_pipeline.py, historical_metrics_processor.py, binance_historical_fetcher.py, http_client.py, canonical_indicators.py, mathematical_liquidation_engine.py, schema.py, and parquet_exporter.py. Located and loaded both current ExtraTrees liquidation artifacts. Inspected all downloaded master rows; ladder review covered file metadata and hashes, not every rung or raw-trade conservation.

Fresh evidence:
- [Data scan and source hashes](C:/Users/SIGMA/Documents/Trading/docs/reviews/data-provenance-evidence.json).
- [Executed causal probes](C:/Users/SIGMA/Documents/Trading/docs/reviews/causal-probe-evidence.json).
- [Previous optimizer/execution review](C:/Users/SIGMA/Documents/Trading/docs/reviews/smc-oos-architecture-review.md), whose portfolio proposal is superseded by the user's individual-asset instruction.

The scan did not redownload raw exchange bytes or verify historical publication latency. It therefore cannot establish full raw-source provenance or certify exact-model lineage for each existing parquet.

## 2. Downloaded inventory

| Asset | Master rows | Imputed-metrics rows |
|---|---:|---:|
| ADA | 210,903 | 74,286 |
| BCH | 210,912 | 74,283 |
| BNB | 210,899 | 74,282 |
| BTC | 210,883 | 30,602 |
| DOGE | 210,901 | 74,286 |
| DOT | 210,910 | 74,279 |
| ETH | 210,889 | 74,284 |
| LINK | 210,905 | 74,285 |
| LTC | 210,911 | 74,277 |
| TRX | 210,905 | 74,277 |
| XRP | 210,895 | 74,185 |
| **Total** | **2,319,913** | **773,326** |

The named directory contains 11 masters, not 18. SOL, AVAX, SUI, NEAR, APT, OP and ARB are missing there. This finding does not assert that files are absent from every other disk location.

All scanned masters:
- Match the current 56-column canonical schema.
- Have zero nulls and zero non-finite numeric cells.
- Have strictly increasing, uninterrupted 15-minute timestamps.
- Have zero tested OHLC ordering/positive-low violations.
- Match their recorded manifest master hashes and row counts.
- Remained unchanged in size/mtime during the scan.
- Have accompanying ladders whose hashes match manifests; those ladders total 18,501,903 rows.

These checks establish internal consistency, not authenticity of every derived feature. Continuous timestamps can include reconstructed bars. The exporter drops their synthetic flags.

## 3. Pipeline path and availability boundary

The fetcher reads Binance Vision futures/spot kline archives, futures metrics archives, funding history, and optional aggTrades. REST fills recent tails and tries to repair archive gaps. The processor forms a continuous timeline, derives indicators, joins spot bars by open timestamp, joins metrics/funding backward as of candle close, invokes the liquidation model, slices away warm-up, finalizes values, and projects onto CANONICAL_COLUMNS. The exporter writes masters, ladders and manifests.

A candle is indexed by its open time, but its high, low, close, volume, CVD and most features become available only after the candle closes. Correct downstream use is close-of-bar decision and subsequent execution. Using a row's feature vector to trade at that row's open is lookahead.

The HTTP client distinguishes archive 404s from exhausted non-404 failures, which raise; parser errors also raise. That is useful fail-closed behavior. Raw timestamp ordering still does not prove publication-time availability of exchange statistics. A production contract needs event_time and available_at, or a documented conservative latency.

## 4. Confirmed lookahead and history-dependence findings

### P0 — Recent USDC availability changes earlier OI

[binance_historical_fetcher.py:719](C:/Users/SIGMA/Documents/Trading/Engine/pipeline/binance_historical_fetcher.py:719) probes only the final three requested USDC archive days. If any exists, it retrieves USDC history and adds USDC OI to the USDT series.

Executed probe: identical archive responses for the common historical date 2024-01-02 yielded OI 150 when the requested end was January 5, but OI 100 when extended to January 6. The later probe no longer contained the one available USDC day. No network or model fitting was involved.

This is genuine history dependence in the fetch stage. It also silently changes the meaning of a USDT symbol's OI to a multi-contract aggregate.

Repair: for this USDT-M task, retain USDT OI as its own field. If aggregate stablecoin OI is wanted later, expose separate USDT and USDC components, per-observation availability, an explicitly named aggregate, and a coverage rule independent of future archive availability. Verify identical historical outputs for common prefixes across requested end dates.

### P0 for trading use — Retrospective quality flag

[historical_metrics_processor.py:63](C:/Users/SIGMA/Documents/Trading/Engine/pipeline/historical_metrics_processor.py:63) marks the entire frozen run only after its length reaches 288 and its full-run OI-motion condition is known.

Executed probe: 287 constant observations produced zero flags; adding observation 288 changed all preceding 287 flags. The source explicitly calls this retrospective, and schema.py describes is_imputed_metrics accordingly.

It may be retained for forensic annotation. Using it to skip historical entries, prune an OOS universe, change position size, or select training records for a historical as-of fit leaks later information. The current optimizer's feature list excludes it, so its mere presence is not proof that the optimizer directly consumes this leakage.

Repair: separate retrospective quality annotations from causal source_available, age_ms and trailing stale counters. Test that appending or changing future data never changes the causal flags of earlier rows.

## 5. MathematicalLiquidationModel: unresolved upstream training leakage

[mathematical_liquidation_engine.py:5](C:/Users/SIGMA/Documents/Trading/Engine/core/mathematical_liquidation_engine.py:5) claims calibration using June–August 2026 observations. Its constructor loads global long/short ExtraTrees artifacts without a cutoff check. Both artifacts loaded successfully in this audit; the loaded feature set has 38 current-bar or lagged variables. No training-cutoff metadata was present among inspected estimator attributes. No training dataset/split manifest was located in the searched source, scratch and model-artifact locations.

The model's per-row computation passed a 287-of-400 synthetic prefix test: extending the input did not change earlier predictions. That proves only a limited property of inference with frozen weights. It does NOT establish that the weights were available before historical OOS windows.

If the header's calibration dates describe these fitted weights, applying them to 2021–March 2026 windows introduces future-trained feature generation. The downstream 72-hour purge does not repair this. Existing parquet manifests omit liquidation-model hashes, training periods and source classifications; the exact artifact-to-parquet relationship remains unproved.

Repair paths:
1. Recover the training source, target observations, timestamps, splits, dependency versions and artifact hashes; require upstream fit cutoffs to precede every dependent validation/test interval.
2. Fit historical feature generators only on then-available data, with nested fitting inside training validation when applicable.
3. Use a documented causal proxy as a research feature when historical observed liquidations cannot be recovered. Do not label it exchange-reported liquidation ground truth. The fallback's calibrated constants also need provenance; disabling the model alone does not certify them.

Require inference mode, artifact hash and cutoff to be recorded per generated partition. An environment-dependent switch from ML to fallback must fail loudly or create a distinct dataset version.

The formula uses max(price, 1.0) in percentage denominators. For sub-dollar assets this differs from a true relative-price move. Review its intended units before using it uniformly across the universe.

## 6. CVD and divergence contracts

[historical_metrics_processor.py:186](C:/Users/SIGMA/Documents/Trading/Engine/pipeline/historical_metrics_processor.py:186) derives futures flow from aggressive buy minus sell base-asset quantity, using tick summaries where available and kline taker volume otherwise. Spot flow is joined on the same 15-minute open timestamp and computed in the same native-asset quantity units.

[historical_metrics_processor.py:383](C:/Users/SIGMA/Documents/Trading/Engine/pipeline/historical_metrics_processor.py:383) defines zc_div as spot_delta minus futures_delta on observed spot bars; it is zero when spot is missing. This is a raw flow difference, not a z-score. The fixed 0.8 threshold means 0.8 native asset units, so its economic scale differs across symbols.

Fresh scan:
- Futures delta matches taker-buy minus taker-sell quantity on all rows at the declared numerical tolerance.
- zc_div matches spot-minus-futures on rows with nonzero observed spot delta.
- There are 1,023 rows, 93 per asset, with spot_delta=0, zc_div=0 and nonzero futures delta. This matches the missing-spot sentinel convention, but the exported files omit the source flag needed to distinguish missing flow from an observed zero.
- Both session-CVD increment identities passed the tested tolerances.
- Twenty lifetime-CVD differences exceed the initial fixed tolerance. Maximum investigated residual was 0.00006104 native units. DOGE/TRX differences fit a floating-point spacing/rounding bound; XRP has smaller residuals that exceed that simple bound and needs reanchoring/accumulation reconciliation. This is not evidence of future lookup.

A synthetic missing-spot probe confirms that flow becomes zero while spot_close is forward-filled. This is temporal-causal but is not fresh observed spot data. Preserve spot_flow_source and age; prevent missing-flow sentinels from masquerading as measured neutrality.

For the fixed-confluence baseline, retain the user's exact rule and document its current units. Any conversion to normalized flow or a standardized divergence is a separately versioned signal change. Add normalized features for ML only with strictly trailing or training-fitted transforms.

## 7. Missing-data robustness defects

### P1 — Entirely absent metrics crash the processor

[historical_metrics_processor.py:327](C:/Users/SIGMA/Documents/Trading/Engine/pipeline/historical_metrics_processor.py:327) enters the empty-metrics branch without defining is_valid_metrics; line 350 then references it. A synthetic execution reproduced UnboundLocalError. Initialize the availability array explicitly and test empty, partial, stale and recovered streams.

### P1 — Required provenance disappears at export

[historical_metrics_processor.py:407](C:/Users/SIGMA/Documents/Trading/Engine/pipeline/historical_metrics_processor.py:407) projects onto the 56-column schema. spot_flow_source, is_synthetic and metrics_available do not survive. The executed processor probe confirmed all three were absent.

[parquet_exporter.py:153](C:/Users/SIGMA/Documents/Trading/Engine/pipeline/parquet_exporter.py:153) counts non-null spot_close values as spot_exact_bars, although missing spot prices have already been filled or replaced. That count cannot certify observed spot coverage.

Repair: export causal source/quality fields and distinguish measured, reconstructed, missing and retrospective flags. Count exact coverage from source flags before imputation. Version the schema and update its consumers together.

### P1 — Zero-filling hides invalid data

[historical_metrics_processor.py:436](C:/Users/SIGMA/Documents/Trading/Engine/pipeline/historical_metrics_processor.py:436) replaces every non-finite float with zero. A probe changed a missing RSI into RSI=0, a valid-looking extreme signal. The later exporter finiteness check cannot detect what was erased.

run_historical_pipeline.py:226 also applies generic forward fill to non-finite numeric columns. Forward fill is backward-looking in time, but forwarding flow, trade counts or technical indicators without reconstructing their dependencies is not a sound universal repair.

Repair per field: carry price/state only within documented bounds; set missing flow to a flagged unavailable state; recompute indicators from corrected raw inputs; reject unrepairable rows or datasets. Do not manufacture prices, metrics or neutrality to satisfy a zero-null gate.

### P1 — Stale/default values lack enforceable freshness contracts

OI freshness is examined, but repaired values can remain forward-filled through outages. Funding is backward joined with a default 0.01%, and FUNDING_MAX_STALENESS_MS is declared without enforcement in the funding calculation. Individual ratio ages are computed but not consistently enforced.

Repair: explicit maximum ages per field, availability flags, conservative handling of startup gaps, and inference abstention when mandatory inputs are unavailable. Future funding settlements must not be used as known forecast features; realized funding cashflows belong in trade accounting at settlement.

### P2 — Raw-source reproducibility and export lifecycle

Default clean_cache removes intermediate parsed/downloaded material after export. Manifests hash outputs but do not retain full source URL/content hashes, transformation versions, model cutoffs or dependency versions. Preserve an immutable raw snapshot or a source-byte ledger with recoverable content.

Master, ladder and manifest writes are individually atomic, not one atomic bundle. A failed replacement can remove newly written paths rather than restore the previous complete version. Prefer generation directories and a final atomic manifest pointer; do not overwrite certified datasets in place.

## 8. What passed causal checks

Backward joins did not select future observations in the boundary probe. Timeline gap repair used the prior close and zero volume. A 287-row processor run matched the common prefix of a 400-row run for all numeric output fields in a synthetic non-frozen case, with the liquidation generator stubbed to isolate transformations. EMA/ATR/RSI, rolling scores, developing session VWAP and value-area implementation use causal recursions/prefix accumulation in the inspected code.

The fetcher's shift(-1) used for diagonal footprint imbalance is across adjacent price rungs within a candle, not across future candles. Such footprint information is available only once that candle's trades have completed.

These are bounded positive checks, not an exhaustive proof over every input and upstream artifact.

## 9. Required certification gates

1. Inventory all 18 contracts and exact listing timestamps; distinguish missing download from pre-listing nonexistence.
2. Freeze raw inputs, source hashes, code/config/dependency hashes and model provenance.
3. Remove future-dependent USDC routing and quarantine retrospective flags from decisions.
4. Repair missing-metrics handling, source-flag export, freshness and invalid-value policy.
5. Resolve or replace future-trained liquidation features; regenerate all dependent rolling features.
6. Run prefix and future-suffix perturbation tests at gaps, funding/metrics boundaries, day changes, month changes, frozen runs, warm-up boundaries and artifact switches.
7. Verify raw-to-master price/volume/CVD on independent archived samples and all ladder-to-master conservation checks.
8. Verify listing-aware UTC coverage and no forming candles; report synthetic bars and unavailable inputs by asset/window.
9. Publish per-partition certification with exact checked scope. Certification requires all blocking findings to close; zero nulls alone is insufficient.

## 10. Boot, orchestration and limits

Canonical router, active context, ML training/feature skills and systematic-debugging skill were loaded. Previously read checklist/memory/directives were retained; targeted graph/history queries ran. Graphify found the liquidation dependency graph. Corrected DeepSeek configuration check exited zero, and Gemini models health check passed. Neither is a strategy-validation pass.

Three specialist tasks were dispatched as the router requires. They returned partial findings before account usage limits stopped them; the coordinator independently completed the tests and synthesis. This is not represented as three completed independent certifications.

The earlier automatic-review rejection of broad cross-repository synchronization remains in force; no bypass or repeat synchronization was attempted. Full parity and broad process-killing memory cleanup are not certified. CPU throttling was not established. No optimizer sweep, full strategy walk-forward run, external raw-data redownload, or security/lint certification is claimed.


