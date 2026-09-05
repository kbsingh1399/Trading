# Historical Pipeline Rebuild — Pre-Build Audit of Reference Implementation

Audit performed against `main@de866f4` before rewriting the pipeline. Every item below is
addressed by the rebuilt modules.

| # | Severity | Location (reference) | Finding | Rebuild resolution |
|---|----------|----------------------|---------|--------------------|
| 1 | **HIGH** | `historical_metrics_processor.py` (EMA/ATR/VAH/basis rounding to 1–2 dp) | Fixed-decimal rounding destroys sub-dollar assets. Measured on shipped data: DOGE `atr_14 == 0` on **97.0 %** of bars, TRX **99.9 %**, ADA 67.9 %, XRP 58.5 %; DOGE has only 73 distinct `ema_8` values over 6 years; `session_vah` has 6–8 distinct values. | Price-denominated features are stored at 8 dp (Binance max tick precision); USD notionals at 2 dp; ratios at 6 dp. No information loss on any of the 18 assets. |
| 2 | **HIGH** | `process_master_dataset` spot join (`merge_asof(direction="backward")`) | When a spot candle is missing, the *previous* spot candle's taker volumes are re-used as the current bar's spot delta (68 of 93 `UNAVAILABLE` BTC bars carry stale non-zero `spot_cvd_15m`). | Spot is joined strictly 1:1 on `open_time_ms`. Missing spot bar ⇒ `spot_cvd_15m = 0`, `spot_flow_source = UNAVAILABLE`, basis forward-filled (causal). |
| 3 | **MED** | Metrics / funding `merge_asof` anchored on `open_time_ms` | Event streams were aligned to bar *open*, so a bar carried a 15-minute-stale snapshot even though later snapshots were already public at bar close. | All event streams (funding, OI, L/S ratios, taker ratio) are as-of joined on `close_time_ms` — the last observation whose timestamp is `<= close_time_ms`. Never `>`. Zero lookahead, minimum staleness. |
| 4 | **MED** | `canonical_indicators.py` | EMA, RMA, RSI, ATR, SMA-9, session CVD and value area were Python `for` loops over every bar (SMA-9 alone: 0.8 s / 200 k bars; value area: minutes per asset). | Fully vectorised NumPy/Pandas kernels. RMA is an exactly-seeded EWM (bit-identical to the loop — verified `max|Δ| = 0.0`). Value area uses a dense per-day-block prefix-sum profile. |
| 5 | **MED** | `binance_historical_fetcher._fetch_url` | 3 fixed retries, 0.3 s linear sleep; HTTP 418/429 treated like any other error; no global cooldown — a thread pool of 16 would hammer Binance straight into an IP ban. | Shared `HttpClient` with exponential backoff + jitter, `Retry-After` honouring, process-wide cooldown latch on 418/429, permanent-404 negative caching. |
| 6 | **MED** | `run_historical_pipeline.py` fast-skip | Skips a symbol if files merely exist with ≥ 95 % ladder coverage — never checks schema, so stale/legacy files are silently kept. | Skip only if both files pass a schema + coverage probe (all canonical columns present, `rung_source` present, 100 % ladder coverage). Otherwise rebuild. |
| 7 | **LOW** | `tick_footprint_fetcher.py` | Stacked-imbalance clustering was a per-bar Python loop with `groupby` iteration. Daily bin step used the *whole day's* median price (intra-day lookahead on bin geometry). | Vectorised run-length clustering; bin step derived from the day's first traded price (causal). |
| 8 | **LOW** | `verify_parquet_integrity.py` | Single monolithic pass; no lookahead probe; missing bars reported only as a count. | Three independent agents; failures report bar index + UTC timestamp; Agent 2 re-derives session VWAP / session CVD / CVD divergence from raw columns and asserts equality (a stored value can only match if it used no future data). |
| 9 | **LOW** | Ladder export | Flag columns emitted as `int64` in 10 of 18 shipped files and `int8` in 8; `rung_source` absent from all 18. | Canonical ladder schema enforced by the exporter (`int8` flags, `rung_source` mandatory). |

## Schema evolution (backward compatible)

All 62 legacy Table-1 columns are preserved with identical names and dtypes, in the same order.
New columns are **appended** after `metrics_available`:

`spot_close`, `session_vwap`, `vwap_zscore`, `volume_ratio`, `zc_div`, `long_liq_zs`,
`short_liq_zs`, `liq_imbalance_ratio`

Table-2 gains `rung_source` (`int8`: 0 = exact tick, 1 = causal synthetic).

File names are unchanged: `{symbol}_15m_master_2020_2026.parquet`, `{symbol}_15m_footprint_ladder.parquet`.

## Deliberate semantic choices

* `volume_sma9` remains the 9-bar SMA of **quote** volume (legacy contract, mirrored by the live
  monitor). `volume_ratio` is `volume_base / SMA9(volume_base)` so it is dimensionless.
* `zc_div` follows the specification literally: `Δ Spot CVD − Δ Futures CVD` per bar (coin units).
  Downstream z-scoring (window 20) stays in the strategy layer.
* `liq_imbalance_ratio = (|short_liq| − |long_liq|) / (|short_liq| + |long_liq|)` ∈ [−1, 1];
  positive ⇒ short-liquidation dominated bar.
* `metrics_available = 1` only when the most recent official metrics snapshot is ≤ 6 h old at bar close.
* The standalone `{symbol}_15m_ladder_synthetic.parquet` side-file is no longer written; synthetic
  rungs live inside the main ladder tagged `rung_source = 1`.

## Verification performed in this sandbox (no Binance egress available)

`python3 -m Engine.verification.test_pipeline_offline` — 9 tests, ~15 s:

| Test | What it proves |
|---|---|
| kernels | vectorised EMA/RMA/RSI/ATR/SMA/VWAP bit-identical to the reference loops |
| clean pipeline | 4,320 synthetic bars → council PASS, Parquet round-trip identical |
| sub-dollar precision | DOGE-scale prices keep full precision on price-scale features |
| prefix invariance | every numeric feature is identical when the history is truncated at 5 cut points (zero lookahead) |
| close_time join | event streams (OI, funding, spot) join with `≤ close_time` semantics |
| negative controls | gap, duplicate, NaN, stale spot, missing POC, shifted EMA, centred VWAP are each rejected with bar index + timestamp |
| orchestrator end-to-end | warm-up slice, dual-table export, manifest, contract-aware fast-skip |
| repair gate | stale spot repaired causally → PASS; missing candle stays REJECTED |
| mock Binance server | real fetcher against a local server emulating data.binance.vision + fapi: header/no-header CSVs, µs→ms timestamps, monthly→daily→REST stitching, missing-day REST repair, exchange-downtime tagging, HTTP 429 `Retry-After` latch, forming-candle exclusion, negative cache, cache hits on re-run |

Scale benchmark (210,600 bars ≈ 6 years of 15 m, 2 CPUs / 3 GB): process 3.4 s, ladder 0.5 s
(3.1 M rungs), council 1.4 s, export 1.5 s, peak RSS 1.25 GB.

Downstream compatibility: `quant_strategy_suite.build_features` and
`trend_orderflow_features.extract_trend_orderflow_features` run unchanged on the new master file; the
first 62 columns match the legacy files in name, order and dtype.
