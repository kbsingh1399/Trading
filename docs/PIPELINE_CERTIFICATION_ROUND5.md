# Pipeline Certification — Round 5: Full-Dataset Forensic Audit (All 18 Assets)

**Mandate:** every row of every exported file audited for mathematical soundness, temporal continuity,
causal integrity (zero lookahead) and compliance with the 3-Agent Council and the Metrics Validity Gates —
plus fail-closed export architecture, `.bfill()` elimination, session-VWAP UTC reset and retry/backoff.
**Auditor stance:** adversarial. Nothing in §1–§3 is reproduced from the pipeline's own expectations;
every numeric assertion is recomputed independently from the stored row and compared to the stored value.

## 0. Verdict

| Claim | Result |
|---|---|
| 3,467,571 candle rows | **3,467,571 measured** — exact |
| 70,934,532 footprint rungs | **70,934,532 measured** — exact |
| Row-by-row violation count | **0** across all §3.1–§3.3 structural/integrity/precision assertions and all 18 files |
| Domain violations (§3.4, after correcting the brief's field names) | **0** |
| Imputation-flag violations (§3.5) | **0**; `is_imputed_metrics == (metrics_available == 0)` exactly, all files |
| Ladder invariants (§3.6) | **0 violations**; identities hold to 2.9e-16 relative rung/candle conservation |
| Independent re-run of `verify_parquet_integrity.check_symbol` | **18/18 PASS** (Agents 1+2+3), 0 findings |
| Lookahead (Mandate 2) | **None.** See §4.2 |
| Fail-closed export (Mandate 2) | **DEFECT FOUND AND FIXED** — F1, §4.1 |
| `.bfill()` | **Eliminated** (0 occurrences in `Engine/pipeline/`) |
| 418/429 backoff + `Retry-After` floor | **Verified**; one robustness gap, F5 |
| Pre-archive attestation | **DEFECT FOUND** — F7: rolled up to months, over-excuses 17/18 |

## 1. Per-Asset Validation Scorecard (all 18 symbols, every bar and every rung)

Every figure is measured directly from the committed parquets in this run by
`Engine/verification/audit_full_dataset_forensic.py --council`, and reconciles to `verification_report.json` and to
all 18 manifests. Column legend — **struct**: 25 structural/OHLCV assertions (§3.1–3.2); **integrity**: 0-null /
0-non-finite sweep over all 72 columns plus exact indicator recompute (§3.3); **domains**: 21 domain-range checks
(§3.4); **ladder**: 14 ladder invariants (§3.6); **causal**: bars where a from-scratch recomputation of
`session_vwap`, `session_cvd`, `ema_8`, `volume_sma9`, `volume_ratio`, `liq_imbalance_ratio`, `rsi_14`, `atr_14`
disagrees with the stored column beyond the export's own rounding quantum **and** past bar 2000 (§4.2);
**council**: my independent re-run of the 3-agent gate (`verify_parquet_integrity.check_symbol`), not the
pipeline's log; **imputed**: `metrics_available == 0` bars (≡ `is_imputed_metrics == 1`); **pre-archive**: of
those, the bars carrying the exact fallback-constant signature (§3.5); **unm. months**: interior months with zero
metrics that no manifest attests; **synth**: `is_synthetic` bars; **OI-USD=0**: F2 bars (`open_interest_usd == 0`
while `open_interest_k > 0` and metrics marked available). The five `fp_*`/flow columns that would expose
tick-level reconstruction are constant 0.0 / single-valued in **0.00 % violation-free** fashion on every asset —
i.e. they never fail a bounds check, which is precisely why the gate cannot see them (F3).

| symbol | bars | rungs | struct | integrity | domains | ladder | causal | council | imputed | pre-archive | unm. months | synth | OI-USD=0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ADAUSDT | 210,801 | 4,522,519 | 0 | 0 | 0 | 0 | 0 | PASS | 74,286 | 43,776 | 7 | 10 | 4 |
| APTUSDT | 136,107 | 3,016,809 | 0 | 0 | 0 | 0 | 0 | PASS | 5,465 | 0 | 2 | 4 | 4 |
| ARBUSDT | 121,176 | 2,560,290 | 0 | 0 | 0 | 0 | 0 | PASS | 35 | 0 | 0 | 4 | 4 |
| AVAXUSDT | 208,661 | 5,091,966 | 0 | 0 | 0 | 0 | 0 | PASS | 72,135 | 41,636 | 7 | 10 | 4 |
| BCHUSDT | 210,804 | 4,026,393 | 0 | 0 | 0 | 0 | 0 | PASS | 74,283 | 43,776 | 7 | 10 | 4 |
| BNBUSDT | 210,803 | 3,245,742 | 0 | 0 | 0 | 0 | 0 | PASS | 74,282 | 43,776 | 7 | 10 | 4 |
| BTCUSDT | 210,797 | 2,710,652 | 0 | 0 | 0 | 0 | 0 | PASS | 30,602 | 0 | 7 | 15 | 5 |
| DOGEUSDT | 210,804 | 4,889,889 | 0 | 0 | 0 | 0 | 0 | PASS | 74,286 | 43,776 | 7 | 10 | 4 |
| DOTUSDT | 210,802 | 4,578,021 | 0 | 0 | 0 | 0 | 0 | PASS | 74,279 | 43,776 | 7 | 10 | 4 |
| ETHUSDT | 210,800 | 3,478,600 | 0 | 0 | 0 | 0 | 0 | PASS | 74,284 | 43,776 | 7 | 10 | 4 |
| LINKUSDT | 210,801 | 4,682,806 | 0 | 0 | 0 | 0 | 0 | PASS | 74,285 | 43,776 | 7 | 10 | 4 |
| LTCUSDT | 210,802 | 4,017,553 | 0 | 0 | 0 | 0 | 0 | PASS | 74,277 | 43,776 | 7 | 10 | 5 |
| NEARUSDT | 206,546 | 5,589,367 | 0 | 0 | 0 | 0 | 0 | PASS | 70,100 | 39,520 | 7 | 10 | 4 |
| OPUSDT | 149,500 | 3,717,836 | 0 | 0 | 0 | 0 | 0 | PASS | 16,379 | 0 | 4 | 4 | 4 |
| SOLUSDT | 209,527 | 5,090,130 | 0 | 0 | 0 | 0 | 0 | PASS | 73,009 | 42,500 | 7 | 10 | 4 |
| SUIUSDT | 117,236 | 2,742,669 | 0 | 0 | 0 | 0 | 0 | PASS | 109 | 0 | 0 | 4 | 0 |
| TRXUSDT | 210,804 | 2,749,584 | 0 | 0 | 0 | 0 | 0 | PASS | 74,277 | 43,776 | 7 | 10 | 4 |
| XRPUSDT | 210,800 | 4,223,706 | 0 | 0 | 0 | 0 | 0 | PASS | 74,185 | 43,776 | 6 | 10 | 4 |
| **total (18)** | **3,467,571** | **70,934,532** | **0** | **0** | **0** | **0** | **0** | **18/18 PASS** | **1,010,558** | **561,416** | **103** | **161** | **70** |

Universe census: **3,467,571 candles / 70,934,532 rungs** — identical to the mandate and to
`verification_report.json` (36 row/rung counts checked, 0 discrepancies). Cadence: **one distinct step value,
900,000 ms, across all 3,467,553 intra-file steps** — zero breaks, zero duplicates, zero non-monotonic steps.
Imputed bars 1,010,558 (29.1 % of the universe): 561,416 carry the documented fallback
constants (legitimate, attested pre-archive absence) and 449,142 carry live-but-untrusted values (2022 quarantine).
Two measured non-defects, recorded so they are not re-litigated: `open_interest_usd` differs from
`open_interest_k x 1000 x close` by >1 % on 7,370 bars (0.21 %) because Binance's own USD figure
uses their interval mark price; and 3,079 bars sit in metric runs of 2-287 bars that are frozen while marked
fresh, below the 288-bar floor of `_stale_runs_mask` (finding F3).
(0.00 % on every column of every asset. "Imputed" = `is_imputed_metrics==1` (fallback-constant bars from
attested pre-archive gaps + quarantine bars); "flagged-frozen" = runs ≥ 288 bars the gate quarantines;
"sub-288 frozen" = frozen runs below the gate's detection floor, reported for completeness (§4.7, F6).)

**Per-asset distinct cadence values: exactly one for all 18 files, `900000 ms`.**

## 2. Corrections to the Brief Itself (found while implementing, not data defects)

The brief's field names predate the council schema. Each was adjudicated against the producing code and
`Engine/core/schema.py` before any assertion was kept:

| Brief | Reality in this repo | Consequence |
|---|---|---|
| "62 columns" | master is **72** columns | §3.3 sweeps all 72 × 18 = 5,184 (col, file) pairs |
| `volume`, `quote_volume`, `trades` | `volume_base`, `volume_quote`, `trade_count` | renamed |
| `funding_rate ∈ [-1.0, 1.0]` | column is `funding_rate_pct` in **percent**; universe spans **[−2.000, +0.559]** | the ±1.0 bound would have **falsely rejected 72 genuine SOLUSDT bars** at the exchange's ±2 % funding cap (2022-11-09/11, FTX cascade); verified as source values — `historical_metrics_processor.py:246` scales `fr*100` and never clips |
| `open_interest ≥ 0` | `open_interest_k` (thousands of contracts) and `open_interest_usd` | both checked; `open_interest_usd == 1000·k·close` to 1e-9 |
| `mfi_14`, `adx_14` | **do not exist** (no MFI/ADX in the council schema) | cannot be asserted; `rsi_14`, `atr_14` checked, both in [0,100] / > 0 everywhere |
| `taker_buy_volume`, `taker_buy_quote_volume ≤ quote_volume` | `taker_buy_vol_btc`/`taker_sell_vol_btc`; **no taker-buy *quote* column exists** | the volume inequality is verified (`buy+sell == volume` exactly, `buy+sell ≤ volume` vacuous-but-true); the quote inequality is **unverifiable by construction** and is reported as such, not as a pass |
| `is_imputed == 1` | `is_imputed_metrics` | renamed |
| ladder `ask_qty/bid_qty/delta/total_qty/imbalance_buy/imbalance_sell` | `ask_vol_coin/bid_vol_coin/net_delta_coin/` (no `total_qty`)/`is_buy_imbalance/is_sell_imbalance` | `total` tested as `ask+bid` (sum-of-volumes semantics documented in `schema.LADDER_COLUMNS`) |
| `dee695d`, `Engine_2/s1_liquidation_cascade.py` | history was re-initialised to a single squashed root commit (`4250cf1`), and **no `Engine_2/` exists in the repo** | see §5 |

## 3. Row-by-Row Results

### 3.1 Temporal continuity and cadence — PASS (0 violations × 18)
One single distinct `Δt` per file = 900,000 ms over all 3,467,553 intra-file steps; 0 duplicates, 0
non-monotonic steps, 0 `close_time_ms != open_time_ms + 899,999` (that identity holds on **every** row).
Timeline conformance: every file starts exactly at `max(FUTURES_LISTING_DATES, 2020-09-01)`, including
the hour-of-listing (APT 02:00, SUI 16:00, ARB 15:00, OP 14:00, NEAR 08:00, AVAX/SOL 07:00) — **no
fabricated pre-listing history**. Apparent −12…−76-bar shortfalls vs a naive full grid are exactly the
in-progress final UTC day; therefore 0 unaccounted gaps. Cross-asset panel note: last bars differ per asset
(BTC 19:00, 11 assets 20:45) because exports were taken at different times — a panel must align to the
earliest end, else the tail silently mixes different horizons.

### 3.2 Mathematical integrity of OHLCV — PASS (0 violations)
`high ≥ max(o,c)`, `low ≤ min(o,c)`, `low > 0`, `high > 0`, all volumes/`trade_count` ≥ 0,
`taker_buy + taker_sell == volume_base` **exactly** on every bar, `basis_usd == close − spot_close` exactly,
`vwap == 0` allowed only where the exporter's documented zero-fill applies. 3,467,571 rows checked
individually per asset, vectorised but row-exact.

### 3.3 Precision / null safety — PASS
**0 nulls and 0 non-finite cells** across all 72 columns × all rows of all 18 files (null + isfinite +
inf/nan sweep per column). Sub-dollar tick preservation: `atr_14` min 2.55e-06; distinct `close` minimum tick
ADA 1e-5, DOGE **1e-6**, TRX 1e-5, XRP/AVAX 1e-4 — no collapse to 0.0; `is_imputed_metrics` ∈ {0,1}
(int8) everywhere; float32↔float64 cast-invariance holds to the quantised `_finalise` precision
(PRICE_DP/COIN_DP=8, USD_DP=2, RATIO_DP/PCT_DP=6), so no column lost precision to the parquet round trip.

### 3.4 Domain bounds — PASS after §2 corrections
`rsi_14 ∈ [0.0, 100.0]` (observed min 0.0, max 100.0 at the bounds legitimately); `atr_14 > 0` on
3,467,571/3,467,571 bars (`atr_14_nonpositive_bars == 0` for all 18); `funding_rate_pct ∈ [−2.0, +2.0]`
with the 72 SOL bars at the −2 % cap explained above; `open_interest_k ≥ 0` and `open_interest_usd ≥ 0`
everywhere, and 0 bars violate the gate's impossible-OI shape (`k == 0 ⟹ usd == 0`) — the *reverse* shape is
the real one and is finding F2 (70 bars); funding cadence was probed directly, since funding is an 8-hourly
event forward-filled onto 96 bars/day: median **3.0 funding changes per day** for 17/18 assets, exactly the
print cadence, while BNBUSDT never prints the 0.01 % default at all (0.00 % of its bars) at 2.0 changes/day,
which proves the column is live rather than constant. That matters because the frame-level no-data fallback
for funding *is* 0.01 (`historical_metrics_processor.py:248`) and collides with the modal real value
(31–48 % of bars in 17/18 assets; longest pinned run: LTCUSDT 4,064 bars ≈ 42 days), so a partial funding
outage would be indistinguishable from a calm market and no `funding_source` column exists (only
spot/future/POC source flags) — recorded as a flagging gap, not corruption; no asset shows the outage
signature itself (2,229–4,303 distinct values per file); `whale_index` 45.0…235.9 — the documented index scale (median 100), not
a bounded percentage; `oi_change_pct` |x| > 25 % on 4,131–4,854 bars per asset, i.e. 6-year real extremes,
not an overflow.

### 3.5 Imputation policy (3.5a) — PASS, with the quarantine era correctly classified
`is_imputed_metrics == (metrics_available == 0)` **exactly** in all 18 files; 0 bars carry live-looking
metrics on a pre-archive date; 0 frozen runs ≥ 288 bars are unflagged (I re-ran the gate itself:
`unflagged_zero_count == 0` and `unflagged_frozen_count == 0` for **every** asset, 204 frozen runs correctly
quarantined); **`AVAILABLE_bars_with_full_fallback_signature == 0` for all 18** — the fabricated-head class
(head bars wrongly promoted to `metrics_available=1`) is dead, verified with the attested months derived
from each file's own manifest (not from the exporter's default list). Per-asset reference points:
BTCUSDT has 30,602 unavailable bars, all of them live-valued (0 fallback-constant, because BTC's archive
coverage starts before its export window), and its longest pinned-funding run is 2,240 bars ≈ 23 days. 1,010,558 imputed bars decompose
without residue into 561,416 attested pre-archive (fallback constants) + 449,142 live-but-untrusted
(2022 quarantine) = 1,010,558 ✓. 103 interior months with zero metrics remain **unattested** in manifests
— legal under the gate (they are quarantine, not absence), listed per asset in §1.

### 3.6 Ladder consistency — PASS (0 violations × 18)
`bid_vol_coin ≥ 0`, `ask_vol_coin ≥ 0`, `net_delta_coin == ask − bid` **exactly**, `ask + bid ≥ 0`,
`rung_source ∈ {0,1}` and `is_buy_imbalance`/`is_sell_imbalance` ∈ {0,1} int8 with **0 co-occurrence**;
ladder bars are 15m-aligned and unique; every ladder bar has a master row and 100 % of master bars have a
ladder row; exactly one POC per bar; rung POC price ∈ [low, high] of its candle; `sum(rungs)/sum(candles)`
per asset equals `fp_total_rungs` to 2.9e-16 relative; `fp_poc` == ladder POC price on every bar.

## 4. Adversarial Bug Hunt — Findings

### 4.1 F1 (BLOCKER, fixed by this audit): fail-open export boundary
`run_historical_pipeline.py` wrapped `export_master`/`export_ladder` in `except (SchemaError, Exception)`
that only *logged and returned* — so a failure after the first `to_parquet` left a **complete-looking,
certificate-less parquet**; and `existing_output_is_current()` skipped a run on the mere existence of the
two parquets, never consulting the `verification.passed` certificate its own validator had written.
Verified with a new deterministic harness, `Engine/verification/test_export_fail_closed.py` (6 checks):
injected failure at master export, at ladder export (master left behind), and at manifest write → after the
fix **no `.parquet` survives on disk** in any case; control run writes both files + `verification.passed=true`.
**Fix shipped:** the export block now tracks every path it writes, removes them on any exception, returns
`False` for `SchemaError` (skip the symbol) and re-raises anything else; `existing_output_is_current()` now
requires master + ladder + **manifest with `verification.passed is true`**, so an incomplete/corrupt/absent
certificate is unusable. 5 of 7 offline tests pass pre-patch too (no regression); full suite green (§6).

### 4.2 Lookahead — no finding, by two independent proofs
* **Structural grep:** 0 `.bfill(` and 0 `.ffill(` in `Engine/pipeline/`; `shift(-1)` only at
  `tick_footprint_fetcher.py:116` with a documented intra-bar (next-rung-within-the-same-15m-candle)
  justification — never across bars; `center=True` only in (a) the *auditor's own* 288-bar rolling median
  (`verify_parquet_integrity.py:103`, not exported data) and (b) the deliberate negative control
  (`test_pipeline_offline.py:277`); the sole temporal join is
  `merge_asof(..., on="close_time_ms", direction="backward", allow_exact_matches=True)` — the mandated
  `≤ close_time_ms` alignment. Session VWAP is built by `cumsum(Δt·tp)/cumsum(Δt·v)` reset on
  `session_day_index` (`core/canonical_indicators.py:220`), and the exporter recomputes
  `session_vwap/vah/val` via `_canonicalise_session_stats()` so the ladder can never overwrite the UTC reset.
* **Data-side (the only proof that matters):** recomputed from stored inputs — `session_vwap` (day-cumulative
  tp/vol), `ema_8` (recursive from the first bar), `volume_sma9`, `volume_ratio`, `liq_imbalance`,
  `oi_change_pct` — **0 mismatching bars out of 3,467,571** for all 18 assets after the exporter's own
  quantisation; `prev_day_vah` == the prior day's final `session_vah` exactly (0 mismatches), so the session
  boundary is real. `rsi_14`/`atr_14` differ from my seeded Wilder recomputation on 1,353/842 bars
  **universe-wide**, and every difference lies in the warm-up head (worst file: bar 233, bar 276 of 8,206);
  **0 bars beyond bar 2000 in any asset** — the 14-period Wilder seeding difference, not lookahead.
  A leak would place differences at the file's tail; the tail matches bit-for-bit.
* **Adversarial control:** the pipeline's own negative control (centered rolling VWAP + `.bfill()`) is
  **rejected by the gate with a non-zero exit**, so the causality test is not vacuously passing.

### 4.3 F2 — `open_interest_usd == 0` while `open_interest_k > 0` on live bars (open, needs their fix)
Exactly **70 bars** in the whole universe, and they are **not scattered**: 15 of 18 assets carry the identical
four timestamps — 2023-04-10 08:45, 09:00, 09:15, 09:30 UTC — and only BTCUSDT and LTCUSDT add a fifth
(08:15); SUIUSDT has none (15×4 + 2×5 = 70 ✓). That
synchrony across 17 independent assets points at one shared upstream Vision-metrics event rather than 17
coincidences, and the pipeline's own reconstruction is what leaves the row inconsistent: the USD series is
rebuilt causally (`historical_metrics_processor.py:286` `oi_usd_ff`, and the median-ratio path) and can settle
at 0 while `available` stays 1, because `available` is gated on `oi_coin > 0` only (`:283`). Nothing then
catches it: the gate that exists for impossible OI is
`verify_parquet_integrity.py:264` → `oi_impossible_zero`, defined as **`open_interest_k == 0` while
`metrics_available == 1`** — the opposite direction — so these 70 bars are never quarantined. Effect: every
USD-denominated OI feature (`open_interest_usd`, `oi_usd_sma20`, `oi_usd_std20`, `oi_imbalance`) reads 0 or
−100 % on those bars. Recommendation: quarantine those four timestamps (or add the symmetric
`usd == 0 & k > 0` check to `HistoricalMetricsProcessor.validate()`).

### 4.4 F3 — 108 `is_synthetic` bars flagged `metrics_available == 1` (open, flag semantics)
**161** bars across all 18 assets are gap-fill reconstructions; **108 of them carry `metrics_available == 1`**
and 53 carry 0 (BTCUSDT 14 of 15; ADA/AVAX/BCH/BNB/DOGE/DOT/ETH/LINK/LTC/NEAR/SOL/TRX/XRP 6 of 10;
ARB/OP/SUI/APT 4 of 4). My first read — "metrics carried forward from the previous bar" — is **measurably
false**: only **2 of the 108** repeat all eight probed metric columns (`open_interest_k`, `open_interest_usd`,
`oi_change_pct`, `funding_rate_pct`, `ls_ratio_global`, `whale_index`, `cvd`, `taker_buy_vol_btc`) from the bar
before, so these bars hold varied, reconstructed values rather than stale copies. The schema does not forbid
the combination either (the gate asserts only `is_imputed_metrics == (metrics_available == 0)`, which holds on
every one of the 3,467,571 rows), so this is **not** a rule violation. The residual risk is narrow but real: a
caller gating solely on `metrics_available` consumes reconstructed values as live, and `basis_usd` on such a
bar is stale close − real spot. Either mark synthetic bars `metrics_available = 0` or add a `metric_source`
column. The scorecard counts them as flagged-imputed so they are not double-reported.

### 4.5 F4 — the entire footprint ladder is reconstructed, and the gate is structurally blind to it
`rung_source == 1` on **100.00 % of 70,934,532 rungs** and `tick_exact_bars == 0` for all 18 assets: every bid/ask
rung is synthesised from the 15m candle, not read from tick archives, and `poc_source` / `future_flow_source` are
`OHLC_APPROX` / `KLINE_APPROX` on every bar. Consistent with that, `fp_poc_vol_ratio`, `fp_stacked_buy_imb` and
`fp_stacked_sell_imb` are **constant 0.0 in every column of every asset** — and they never trip a check, because
`Engine/core/schema.py::ALLOWED_CONSTANT_COLUMNS` whitelists exactly those five columns and
`verify_parquet_integrity.py:476` skips the `dead_feature` check for whitelisted ones. The whitelist is documented
and deliberate (there is no tick history to price), so this is **not** a rule violation; it is a scope fact with
consequences: any strategy that fits on the stacked-imbalance or POC-share features is fitting noise, which is why
§5 withholds microstructure certification. Certified anyway, because they are recomputable from the ladder:
`fp_poc` (== ladder POC price on every bar), `fp_bid_vol_total`, `fp_ask_vol_total`, `fp_imbalance_ratio`.

### 4.6 F5 — `Retry-After` parsing is not robust to non-integer forms (minor)
`_wait_time()` does `int(headers.get("Retry-After"))` inside `try/except ValueError`, so a
**fractional** `Retry-After` (allowed by RFC 9110 for 4xx/5xx in some gateways) or a multi-value header
falls through to `min(2**retry, 60)` rather than the intended 5.0 s floor — with 418 (rate-limit ban) the
retry could then fire *sooner* than Binance asked, which is exactly how a temporary ban becomes a longer one.
Already-correct parts, verified not assumed: shared `_http` client with `Retry(5, status_forcelist=[418,429,500,502,503,504], backoff_factor=1.0)` **plus jitter**,
per-asset `threading.Lock`-guarded cooldowns honouring `Retry-After`, `max(5.0, ...)` floor, and
`time.sleep(min(wait,45))` backoff at 418/429/5xx in the month loop. Fix: parse `Retry-After` as float
(and also handle the HTTP-date form), keeping the 5.0 s floor.

### 4.7 F6 — sub-threshold frozen runs the gate structurally cannot see (documented, not fixed)
**3,079 (column, bar) pairs** sit in frozen runs of 2–287 bars below the gate's 288-bar
`_stale_runs_mask` floor — 0.089 % of the universe; worst asset BTCUSDT at 0.318 % (671 pairs), best
ETHUSDT/DOGEUSDT/XRPUSDT ≈ 0.04 %. Reproduced identically in two independent full-dataset runs. They are real: the metric genuinely
did not move for up to a day, typically around OI/large-order-flow gaps. Not a defect in the gate (the
threshold is a deliberate false-positive defence), but a **modeling caveat**: those runs are legitimate
training targets for "stale" detectors and legitimate noise for `*_change_pct` features.

### 4.8 F7 — pre-archive attestation is rolled up to months, so it over-excuses (open)
`binance_historical_fetcher.py:333` correctly records the *days* whose Vision object the host does not serve
(`_cached` → `None`: the only evidence about the *source* in this pipeline), but `parquet_exporter.py:140`
wrote only `{d[:7] for d in absent_days}` and `verify_parquet_integrity.py:419` grants the council's
pre-archive exemption **on that month field alone** — so one absent day attests an entire month.
Measured consequence: 17 of 18 manifests attest the in-progress month **2026-09** as absent although data for
it is present (BTCUSDT is the sole exception), and NEARUSDT/SUIUSDT attest **2023-12** although **97.55 %** of
that month's bars carry live metrics — a vanished week of OI inside that month would have been certified as
legitimate pre-archive absence. Fix: let the gate excuse days, not months (or gate the month exemption on
`coverage(month) < ε`). **Shipped with this audit** (additive, no behaviour change): the manifest now also
carries `metrics_archive_absent_days` and `metrics_archive_absent_day_count`, so the day-accurate rule can be
adopted without re-downloading anything.

The exemption is not abused in the other direction either: `imputed_fallback_months_not_attested_or_zero` is
**empty for all 18 assets** — every one of the 561,416 fallback-constant bars lies in a month the source
genuinely did not serve, i.e. no pre-archive region was fabricated to hide a gap.

### 4.9 Rejected suspicions (recorded so no one re-litigates them)
Each of these was my own audit expectation, and each was **wrong** — adjudicated against the producing code
before being withdrawn: `open_interest_usd != k·close` (it is *thousands* of contracts ⇒ `1000·k·close`;
residual > 1 % deviations on 7,370 bars = Binance's own mark price, not a computation error); `volume_sma9`
"mismatch on every bar" (it is the SMA of **quote** volume, `:169`, and my own comparator's rounding — it
matches the exporter's `USD_DP=2` quantisation, e.g. the 0.0078 ETH delta is exactly 9 terms × 0.005);
`taker_volume_ratio` "domain violations" (clipped to `[0, 1e6]`, `:368`); `long_liq_usd < 0` on every bar
(signed convention `:339-340`: shorts positive, longs negative); 5.0e-7 ratio "mismatches" (half the
`RATIO_DP=6` quantum); `session_cvd` 1.94e-7 (a *cumulative* column accumulates rounding, so a per-column
bound is the wrong model — with `accum = 96 × 2` quanta/day, mismatches → 0);
`fp_*`/`poc_source`/`future_flow_source` constants (documented approximation without tick data, whitelisted);
`funding_rate_pct == 0.01` on 35.7 % of bars — the exchange's default 8-hourly rate, forward-filled; the
quantified cadence and the fallback-collision consequence live in §3.4, and it is a *flagging* gap, not
corruption.

## 5. Certification for the 20 OOS Walk-Forward Windows — **cannot be granted as specified**

`Engine_2/s1_liquidation_cascade.py` **does not exist in this repository** (no `Engine_2/` at all; history is
one squashed root commit `4250cf1`, so the brief's `dee695d` cannot be checked out). There is therefore no
harness present for me to certify windows against, and I will not certify a file I cannot read.

What I *can* certify, and do:

* **The data are fit to be certified as the input set** for institutional out-of-sample research: 0 violations
  on every structural, mathematical, precision, domain, imputation-policy and ladder invariant in §3, 18/18
  PASS on the council's own independent gate, and zero lookahead in the strict prefix sense (§4.2). Cadence
  and OHLCV are certified **exactly**; indicators are certified to the exporter's documented quantisation;
  and the four residual classes (F2, F3, F6, and the `taker_buy_quote_volume` unverifiability) are named,
  quantified and excluded by count where a strategy depends on them.
* **Not certified:** tick-level microstructure. `rung_source == 1` on **100.00 % of 70,934,532 rungs** and
  `tick_exact_bars == 0` for all 18 assets, i.e. the footprint is OHLC-reconstructed, and
  `fp_poc_vol_ratio`, `fp_stacked_buy_imb`, `fp_stacked_sell_imb` are **constant 0.0 in every column of every
  asset** — and `poc_source`/`future_flow_source` are 100 % `OHLC_APPROX`/`KLINE_APPROX`. Because
  `Engine/core/schema.py::ALLOWED_CONSTANT_COLUMNS` deliberately whitelists exactly those five columns, the
  gate's `dead_feature` check is **structurally unable to report them** (`verify_parquet_integrity.py:476`).
  A liquidation-cascade study that consumes those fields would be fitting noise, so if
  `s1_liquidation_cascade.py` touches any `fp_stacked_*`/`fp_poc_vol_ratio`, the answer is: **not certified,
  and cannot be** until real tick archives feed the ladder. `fp_poc`, `fp_bid_vol_total`, `fp_ask_vol_total`,
  `fp_imbalance_ratio`, `cvd`-family and POC *price* are certified (all recomputed from the ladder and matched).
* **Pre-conditions to certify the harness** (do these, then re-run §6): commit `s1_liquidation_cascade.py`;
  drop the five whitelisted constant columns from `ALLOWED_CONSTANT_COLUMNS` so `dead_feature` fires on
  them (F4); quarantine the 70 F2 bars; resolve the F3 flag semantics; make attestation day-accurate (F7);
  add `funding_source`/`metric_source` per §3.4/§4.4; then the 20 windows are certifiable
  against a data set whose only remaining approximation is disclosed and bounded.

## 6. Reproduction

```bash
python3 Engine/verification/audit_full_dataset_forensic.py --council --out /tmp/forensic_all.json   # 74 s, all 18
python3 Engine/verification/test_export_fail_closed.py                                             # 6 checks
python3 Engine/verification/test_pipeline_offline.py                                               # 7 tests
```
Per-asset `--json` artefacts are in `Engine/verification/forensic_results/` (kept out of git: regenerable,
~2 kB each × 18, machine-local paths inside). Environment note: this sandbox runs **pandas 3.0.5**, newer
than the repo's pinned set; every finding was cross-checked against the producing code so none depends on
a version-specific behaviour, but the `frozen-run`/`center=True` greps above are the authoritative record of
what was actually executed.
