# Quantitative & Architectural Verification — Binance 15m Historical Pipeline

**Assessment scope:** `kbsingh1399/Trading@161ef7f` (`main`)
**Method:** independent re-derivation of every quantitative claim against source, plus executable probes
(`Engine/verification/audit_probe_indicator_parity.py`, `Engine/verification/audit_probe_metrics_coverage.py`).
**No production module was modified by this review.**
**Date:** 2026-09-05

---

## 0. Certification statement

> **The pipeline is NOT certified as production-ready for full 2020→present regeneration across all 18 assets.**
>
> The indicator core, precision contract, causal join design, ladder assembly and export/atomicity layers are
> **correct, sound and verified**. Two issues block certification, and both are in the *ingestion/verification*
> layer rather than the mathematics:
>
> 1. **Blocking — silent fabrication of unavailable metrics, which the council cannot detect.** When the
>    official-metrics archive does not cover a date range (which is certain for 2020→late-2021; see §4.1), the
>    processor writes `open_interest=0`, `ls_ratio=1.0`, `whale_index=100.0`, `oi_change_pct=0` — values that are
>    numerically legal and **pass all three agents**. Reproduced in §4.1 with `CouncilReport.passed == True`.
> 2. **Blocking — the "fully converged warm-up" guarantee is false for 3 of 18 assets** (SUI, ARB, OP), whose
>    listing date equals the export start date, so `ema_800`/`atr_100`/`rsi_14` are unconverged on the first
>    ~2,400–3,200 exported bars with no flag and no NaN.
>
> The legacy datasets in `binance_backtesting_data/` are **invalid and must be regenerated** — that verdict is
> unconditional and is *not* contingent on resolving the two blockers above.

**Correction to the brief's premise (material to Task 1):** no Parquet files exist anywhere in the repository.
`Engine/binance_backtesting_data/` contains 19 JSON files (18 manifests + `verification_report.json`), 80 KB total;
`.gitignore` excludes `*.parquet`-scale payloads by omission. The brief's paths (`binance_backtesting_data/` at repo
root) do not exist — data lives at `Engine/binance_backtesting_data/`.

---

## 1. Task 1 — Forensic audit of the previously downloaded data

### 1.1 Evidence actually available

The claimed corruption statistics **cannot be independently reproduced**, because the files they were measured on
are not in the repo. They are asserted only by `docs/PIPELINE_REBUILD_AUDIT.md`.

There is, however, one piece of *primary* evidence: `Engine/binance_backtesting_data/verification_report.json`, a
real council output run against the shipped BTCUSDT export. It is decisive on its own:

| Field | Value |
|---|---|
| `passed` | **false** |
| `Agent1:Continuity` | PASS |
| `Agent2:Microstructure` | **FAIL (6)** |
| `Agent3:Schema` | **FAIL (5)** |
| `master_rows` | 210,613 |
| `ladder_rows` | 2,992,918 |

Findings, with occurrence counts:

| check | count | significance |
|---|---:|---|
| `ema_21_recursion` | 112,834 | 53.6 % of bars violate the one-step recursion |
| `ema_8_recursion` | 109,707 | 52.1 % of bars violate the recursion |
| `fut_cvd_identity` | 108,103 | 51.3 % of bars: `future_cvd_15m ≠ taker_buy − taker_sell` |
| `oi_change_domain` | 69 | `oi_change_pct` outside [−100, 100] |
| **`spot_unavailable_zero`** | **68** | **stale spot CVD reuse — exact match to the brief's claim** |
| `ladder_dtype` | 3 | flags emitted as `int64`, not `int8` |
| `fut_lifetime_cvd` | 1 | lifetime accumulator does not start at `delta[0]` |
| `columns` | 1 | 62-column file vs the 70-column contract |
| `ladder_columns` | 1 | `rung_source` absent |
| **total** | **330,787** | |

Two independent conclusions follow:

* The `spot_unavailable_zero` count of exactly **68** corroborates the brief's "68 of 93 `UNAVAILABLE` BTC bars
  carried stale non-zero `spot_cvd_15m`". The bug is documented by the shipped artifacts themselves.
* `ladder_columns` + `ladder_dtype` (4 findings) are precisely the Table-2 non-parity defects of Task 1.4. They
  are not theoretical — they were measured.

**Caveat on the report's coverage:** it contains exactly one key, `BTCUSDT`. It is an 18-asset *directory* holding a
1-asset *verdict*. Any claim about DOGE/TRX/ADA/XRP rests solely on the prose in the audit doc.

### 1.2 Sub-dollar precision annihilation — verdict: fatal, confirmed by mechanism

Mechanism: the legacy path rounded price-scale features to 1–2 dp. For an asset trading at \$0.085 with a 15m ATR
of ~5e-4, a 2-dp representation is **0.00 by arithmetic**, not by data. So:

* **`atr_14 == 0` on 97 % of DOGE bars** ⇒ every volatility-scaled stop is `entry ± 0×mult`. ATR ratchets never
  advance, so the "trailing stop" degenerates to a fixed-price stop, and every "did the ratchet move?" event
  disappears. Position sizing keyed to `1/ATR` either explodes or divides to zero.
* **73 distinct `ema_8` values over 210,613 bars** ⇒ the trend filter is a 73-level step function on a series with
  ~40,000 distinct closes. Cross-signal `ema_8 > ema_21` collapses to a near-constant, and the *time in a regime*
  distribution is meaningless. Reported Sharpe and turnover on such a filter are not estimates of anything.
* **`session_vah` with 6–8 distinct values** ⇒ value-area acceptance/rejection logic reads one of ~7 prices for six
  years; VA-based entries are a fixed price grid.
* **Basis at 2 dp** ⇒ on sub-dollar assets the whole funding/basis signal is quantised to zero, i.e. the *most*
  informative feature for perp-vs-spot strategies is deleted.

**Answer: yes — fundamentally corrupted and invalid, for ATR-scaled stops, ATR ratchets and trend filters
specifically, and additionally for any basis, VA and volatility-normalised z-score usage.** Not "noisy" — the
information is absent, so no reweighting, no robust estimator and no OOS split can recover it. This class of defect
is *unrecoverable by modelling* and only fixable at the storage contract.

### 1.3 Stale spot CVD backward-reuse — quantitative impact

Mechanism: `merge_asof(direction="backward")` on missing spot bars copies bar *t−1*'s taker volumes into bar *t*,
so `spot_cvd_15m[t] = spot_cvd_15m[t−1]` (a non-zero duplicate) instead of 0.

Impact on `zc_div = spot_cvd_15m − future_cvd_15m`:

1. **A spurious, autocorrelated spike.** The error term is `+spot_delta[t−1]` added to `zc_div[t]`. Since
   `spot_delta[t−1]` is itself large in magnitude by construction (it was the previous bar's flow), the divergence
   series gains a one-bar echo of its own lagged input. That inflates lag-1 autocorrelation of `zc_div` — the exact
   statistic any momentum/persistence rule keys on.
2. **Adverse selection in *when* it occurs.** The 68 contaminated bars are not a random sample: spot candles go
   missing during volatility spikes, halts, and liquidity crises. So the artefact concentrates precisely on the
   extreme bars that dominate any tail statistic (95th-percentile divergence, "flow blowout" triggers). A rule
   conditioned on `|zc_div| > k·σ` will therefore fire on the artefact, not the flow.
3. **Sign inversion.** `zc_div` measures spot *versus* futures aggression. On a missing-spot bar the truth is
   "no information" (delta 0, divergence = −futures delta). The bug reports "spot printed last bar's aggression",
   which can flip the sign of the divergence relative to the correct zero-fill. Any long/short asymmetry in a
   confluence rule inherits that flip.
4. **Lifetime/session contamination is persistent, not transient.** `spot_cvd_session` and `spot_cvd_lifetime` are
   cumulative sums of the per-bar delta, so a single stale value biases **every subsequent bar in that session and
   for the entire remaining sample**. A one-bar defect becomes a permanent offset. This is the most serious part
   of the bug and it is not addressed by the raw bar count of 68/93 (73 % of all unavailable bars).

**Answer: the impact is a persistent, non-random, sign-unreliable contamination of the divergence family,
concentrated on stress bars, with cumulative amplification into session and lifetime CVD.** Any published edge for
an order-flow-confluence strategy on the legacy files is unattributable.

### 1.4 Event-stream timestamp anchoring — verdict: yes to both parts

* **Yes, anchoring to `open_time_ms` injects staleness.** Binance settles funding and stamps metrics snapshots at
  instants inside/after the bar they describe. An as-of join with `direction="backward"` keyed on the bar's *open*
  returns the last snapshot at or before `open_time` — up to a full 15-minute period, and one additional bar of
  latency relative to the decision point. At a bar-close decision, the bar is labelled with data from the *previous*
  bar's window. This is not lookahead; it is **one-bar lag presented as same-bar information**, which is worse for
  backtest validity because it silently deflates the measured edge of fast signals and inflates it for slow ones
  (a systematic, horizon-dependent bias, not noise).
* **Yes, `<= close_time_ms` is the correct causal fix.** It is the maximum-information *non-anticipating*
  alignment: any observation with `ts <= close_time` is public at the decision instant; `ts > close_time` is not.
  The rebuilt `_asof_backward` uses `direction="backward", allow_exact_matches=True`, which is exactly
  `{ts : ts <= close_time}`. Verified in `test_event_join_uses_close_time` (passes here).
* **One implementation detail worth confirming, and it is correct:** `close_time_ms = open_time_ms + 899_999`, not
  `+900_000`. Had it been `+900_000`, an event stamped exactly at the *next* bar's open (00:00:00.000 funding
  settlement) would be admitted into bar `t` — a one-millisecond lookahead leak into the closing bar of every UTC
  day. The 899_999 convention forecloses that, and Agent 1's `close_time` check enforces it on every exported row.

### 1.5 Footprint-ladder non-parity — verdict: disqualifying

Confirmed against the shipped artifacts (`ladder_columns`, `ladder_dtype` findings in §1.1).

* **Missing `rung_source`.** Synthetic rungs are volume-uniform profiles derived from OHLCV; exact rungs are real
  aggTrades clusters. Stored identically, a consumer cannot avoid training on fabricated microstructure. Worse,
  the mix is *regime-dependent* — tick archives exist only for recent/limited windows — so the model learns "ladder
  shape" whose statistical properties change mid-sample for reasons unobservable to it. This is a hidden
  covariate shift, the single hardest class of backtest error to detect downstream.
* **`int64` vs `int8` imbalance flags.** Not merely 8× bytes-per-column: any consumer casting, comparing dtypes or
  relying on a canonical schema (as `existing_output_is_current` now does) treats the files as foreign, and the
  parity failure is exactly what makes "which files are trustworthy" unanswerable.
* **The 8 extended features** (`spot_close`, `session_vwap`, `vwap_zscore`, `volume_ratio`, `zc_div`,
  `long_liq_zs`, `short_liq_zs`, `liq_imbalance_ratio`) being absent means the shipped Table 1 cannot express the
  VWAP-anchoring, divergence and liquidation-imbalance constructs the current strategy layer expects; recomputing
  them by hand on legacy values is impossible because the inputs were already destroyed by §1.2's rounding.

### 1.6 Verdict

**Discard and regenerate from scratch.** This is not a judgement call — it is the only available action:

1. Every manifest declares `column_count: 62` and lists no `EXTENDED_COLUMNS`. The rebuilt exporter writes 70
   columns and the fast-skip probe (`existing_output_is_current`) requires
   `schema_arrow.names == CANONICAL_COLUMNS`. **The legacy files fail the contract and will be rebuilt even with
   `--force` omitted.** The old pipeline cannot be "patched forward"; its files are already inadmissible.
2. The only surviving primary evidence, `verification_report.json`, says `passed: false` with 330,787 findings.
   That file's own header states the export was never accepted.
3. The corruption is in the stored values (§1.2), the join semantics (§1.3) and the schema (§1.5) — three
   independent axes, no two of which can be repaired without re-deriving the third.

The 18 manifests and `verification_report.json` are themselves stale: they reference files that are not present
(`master_file: BTCUSDT_15m_master_2020_2026.parquet`, `master_size_mb: 54.03`) and carry `exported_at_utc`
2026-09-03 from the pre-rebuild run. They document the legacy export only and should be treated as the "before"
evidence, not as current state.

---

## 2. Task 2 — Architectural review of the mitigations

Environment used for all execution below: Python 3.11, pandas 3.0.5, numpy 2.4.6, pyarrow 25.0.1,
scikit-learn 1.9.0. Full suite: `python3 -m Engine.verification.test_pipeline_offline` → **9/9 PASS in 11.7 s**
against pandas/numpy versions *newer* than those the suite was authored under, which is itself a useful robustness
signal.

### 2.1 Indicator kernels — sound; one documentation claim is false

| Claim | Verdict |
|---|---|
| All Python bar-loops eliminated | **TRUE** |
| EMA bit-identical to textbook recursion (`max\|Δ\|=0.0`) | **TRUE** — verified exactly 0.0 for spans 8/200/800 |
| Wilder RMA bit-identical (`max\|Δ\|=0.0`) | **FALSE** — worst `max\|Δ\| = 1.954e-14` over 120 trials × periods {2,14,100} |
| Prefix invariance `f(x[:n])[:k] == f(x)[:k]` | **TRUE, and stronger than tested** |

**On RMA parity.** `compute_wilder_rma_series` seeds `expanding[period-1]` then applies
`ewm(alpha=1/period, adjust=False)`. Mathematically that *is* `y_t = y_{t-1} + (x_t − y_{t-1})/period`. In IEEE
754, pandas accumulates in a different order than the scalar recursion, so results differ in the last bits. Measured
non-zero. The repo's own test only asserts `< 1e-9`, and the audit doc upgrades that to "bit-identical". At 1e-14
this is analytically irrelevant (a relative error ~1e-16 on ATR cannot move a stop), but **the certification-grade
claim as written is untrue** and should read "numerically equivalent to 1e-14, tolerance-tested at 1e-9". Do not
put "bit-identical" in an audit exhibit.

**On prefix invariance.** The property is *architecturally* guaranteed here, not merely tested: every kernel is
`cumsum`, `rolling`, `ewm(adjust=False)` or `groupby(day).cumsum/cummin/cummax`, all of which are prefix-homomorphic.
I went beyond the suite's 5 cut points:

* `session_value_area` (the greedy expansion — the only kernel with a plausible hidden global dependency, since POC
  selection and bucket bounds could in principle depend on later bars): **0 violations across 103 prefixes** of a
  6,000-bar sub-dollar series. The guard that makes it work is `run_lo/run_hi = cummin/cummax` per session — the
  expansion is bounded by the range *traded so far*, not the day's final range. That is the correct design, and it
  is easy to get wrong (the legacy version did, per audit item 7).
* `session_vwap`, `session_cvd`, `atr_14`, `rsi_14`, `sma9`: **0 violations, worst |Δ| = 0.000e+00 exactly**, dense
  sweep of ~140 cut points each.

Residual caution for the record: `test_prefix_invariance` truncates `spot`/`funding`/`metrics` streams at
`cut_ms + BAR_MS − 1`, i.e. it faithfully mirrors the close-time anchor. It samples 5 cuts of ~4,300 synthetic bars.
Prefix invariance is a *universal* quantifier over `k, n`; this is evidence, not proof. The construction argument
above is what actually carries the guarantee.

### 2.2 Sub-dollar precision contract — resolves the defect; no 62-column break

`_finalise` applies `PRICE_DP=8` / `COIN_DP=8` / `USD_DP=2` / `RATIO_DP=6` / `PCT_DP=6` to explicit column tuples.
Measured on 40,000 DOGE-scale bars (price ≈ 0.085):

| feature | legacy | rebuilt (measured) |
|---|---:|---:|
| `atr_14` distinct values | ~3 % non-zero (73 for `ema_8`) | **32,728** |
| `ema_8` distinct values | 73 / 210,613 | **39,912** |
| `basis_usd` distinct values | ≈ 0 | **6,364** |
| fraction `atr_14 == 0` | 67–99.9 % | **0.00 %** |
| min \|`atr_14`\| | 0 | 3.7e-04 |

Contract compatibility: `LEGACY_COLUMNS` is exactly 62 entries, verified by count; `EXTENDED_COLUMNS` appends 8
after `metrics_available`; `CANONICAL_COLUMNS = 70`. `COLUMN_DTYPES.setdefault(c, "float64")` covers all 70, with
names, order and dtypes of the first 62 preserved. Downstream readers that slice positionally or by name remain
valid. **Answer: yes to both halves** — truncation resolved, 62-column contract intact.

Two honest qualifications:

* Rounding to `dp` is a *normalisation*, not a precision limit — the columns are `float64`, so 8 dp discards
  information the format could carry. That is fine and arguably desirable (reproducibility, stable hashes), but the
  mechanism is "we chose to quantise at Binance tick precision", not "float64 cannot do better".
* **Latent edge case, not triggered by the current 18 assets.** Agent 2's `basis_identity` tolerance is
  `1e-6 * max(|close|, 1e-9)`. At a price of 1e-4 the 8-dp quantisation step (1e-8) is the same order as that
  tolerance, so a genuinely correct rounded series can fail the check. My first probe reported 25 % violations at
  price ≈ 1e-4; re-running with the pipeline's actual rounding order (round inputs, then difference) gave **0
  violations at 1e-4, 0.085 and 30,000** — I withdrew that finding as my own artifact. Recorded here because the
  margin is thin: adding a SHIB-scale or 1e-5-priced asset to the universe would require widening the tolerance or
  raising `PRICE_DP`. All 18 current assets sit ≥ 1e-4 with headroom.

### 2.3 Causal ingestion contract — correct as specified

* **1:1 spot join: volume duplication eliminated by construction.** The spot frame is deduplicated
  (`drop_duplicates("open_time", keep="last")`) *before* a `how="left"` merge onto the futures grid, so the merge is
  a key-aligned projection and cannot fan out rows. `spot_delta = np.where(spot_exact, s_buy − max(s_vol−s_buy,0),
  0.0)` — the `else` branch is a hard 0, which is exactly the invariant Agent 2 now enforces
  (`spot_unavailable_zero`, the check that caught the legacy data). Session/lifetime CVD are cumsums of that same
  zero-filled delta, so the §1.3 cumulative-amplification path is closed at the source rather than patched
  downstream. Confirmed correct.
* **`<= close_time_ms` as-of: maximum public information, zero lookahead.** `_asof_backward` returns
  `_age_ms = _ts − ts_col` and callers gate on it (`METRICS_MAX_STALENESS_MS = 6 h` for
  `metrics_available`, `FUNDING_MAX_STALENESS_MS = 16 h` for two missed settlements). Carrying *age* as a first-class
  value rather than silently ffilling is the right choice and is what makes `metrics_available` meaningful.
  Each metric column is as-of joined **independently** (`for col in cols: sub = m[["timestamp_ms", col]].dropna()`),
  so a sparse column does not poison a dense one — a real improvement over a single frame-wide join.
* **One genuine defect, deferred to §4.1:** the *fill* used when an as-of lookup finds nothing is a fabricated legal
  constant, not a null and not a flag. That is the blocking issue.

### 2.4 HTTP resilience — three of four claims hold; one is overstated

| Claim | Verdict |
|---|---|
| Exponential backoff + full jitter | **TRUE** — `random.uniform(0, min(max_delay, base·2^attempt))` |
| `Retry-After` parsed | **TRUE**, with a caveat below |
| 404 negative caching | **TRUE** — memoised per process, `_not_found` consulted before any attempt |
| "Process-wide cooldown latch" | **OVERSTATED — the latch is per-`HttpClient` instance** |

The latch (`_cooldown_until`, guarded by `self._lock`, read by `_sleep_for_cooldown()` at the top of every attempt)
is genuinely correct *within* a client: one 429 pauses all 16 worker threads sharing that client, instead of 16
threads each discovering the ban. That is the design the audit describes.

But `run_pipeline()` executes `http = HttpClient()` **inside the per-symbol function**, and `main()` loops symbols
sequentially in one process. Consequences:

1. Within one symbol: correct.
2. Across symbols: the cooldown does **not** carry over. Symbol *n* starting after symbol *n−1* was banned at 16 h
   will re-probe Binance immediately.
3. The docstring's "*every* worker thread pauses" is true only of threads sharing that instance. If anyone
   parallelises symbols across processes (the obvious optimisation for an 18-asset batch, and the natural reading of
   "process-wide"), 18 clients × 16 workers = **288 concurrent request streams with 18 independent cooldown
   latches** — the precise IP-ban scenario the audit lists as the item-5 fix.

Additional real nits, in descending importance:

* `cool = max(retry_after, cooldown) * (attempt + 1)` is applied to `Retry-After` **without** the `max_delay` cap
  that `_backoff` respects. A pathological or adversarial `Retry-After: 86400` makes the client sleep a day,
  multiplied by attempt count. Add `min(max_delay, …)` or an explicit ceiling.
* `min_interval=0.0` by default: there is **no proactive pacing at all**. Protection is purely reactive — the client
  discovers a ban rather than avoiding one. For a 6-year × 18-asset backfill this maximises the chance of hitting
  418 early. Set `min_interval≈0.05–0.1 s` for the archive host.
* `stats["requests"] += 1` etc. are unlocked read-modify-writes from 16 threads — benign (log-only) but the printed
  `http={...}` undercounts, so it must not be used as an audit figure.
* `_not_found.add(url)` mutates a plain `set` outside `self._lock`. Safe under CPython, not contractually.
* 418 and 429 differ only by the constant (`ban_cooldown=120` vs `rate_limit_cooldown=30`) and share the `(attempt+1)`
  multiplier, so a 418 — the *hard* ban — escalates from only 120 s. Binance 418 typically warrants a much longer,
  non-multiplicative back-off.

### 2.5 Dual-table ladder assembly — correct and causal

* **Vectorised run-length clustering:** confirmed no per-bar loop. The only Python loops in
  `compute_session_value_area` are over session-chunks (~2k) and over expansion steps (bounded by bucket count),
  never over bars — as claimed.
* **Daily bin step from the day's first traded price:** `_, first_idx = np.unique(day, return_index=True)` then
  `nice_bin_step(opens[first_idx])`, broadcast back via `searchsorted`. `nice_bin_step` is a pure elementwise
  function of one price (verified: 1e-4→1e-6, 0.085→3e-5, 0.5→1.75e-4, 12→0.0042, 3e4→10, 1e5→35), so bar *t*
  cannot see bar *t+1*. **The intra-day median-price lookahead is genuinely eliminated.** Note it uses the day's
  first *open*, so it is knowable before any bar of that day closes — strictly causal, and consistent with the tick
  fetcher's "first print of the day" rule, which is what makes exact and synthetic rungs geometrically comparable.
* **100 % coverage: TRUE but tautological.** `assemble_ladder` synthesises for `master.loc[~covered]` and every
  master row yields ≥ 1 rung (downtime bars emit one rung at the close). Coverage is therefore guaranteed by the
  generator and is **not** evidence of validity. This matters for audit item 6: the legacy fast-skip's "≥ 95 %
  ladder coverage" heuristic was weak, and the *replacement's* "100 % coverage" clause is weak in the same way. The
  real gate is `schema_arrow.names == CANONICAL_COLUMNS` plus the 24 h freshness test; the coverage conjunct should
  be understood as decoration.
* **Honest zeroing:** synthetic `is_buy_imbalance/is_sell_imbalance` are hard 0 ("cannot be inferred without ticks;
  never fabricated") and `net_delta_coin = ask − bid` holds by construction. POC as the close-containing rung under a
  uniform profile is a stated convention, not a measurement. `MAX_RUNGS=512` widening is per-bar and uses only that
  bar's own H/L — causal.
* **Consequence to surface for strategy authors:** with `footprint_days=0` (the CLI default), *every* rung is
  `rung_source=1`, so `fp_stacked_buy_imb`/`fp_stacked_sell_imb` are identically 0 across the entire 2020→present
  export, and `poc_source` is `OHLC_APPROX` everywhere. The schema's `ALLOWED_CONSTANT_COLUMNS` explicitly exempts
  both imbalance columns from the `dead_feature` scan — a defensible choice (they *are* legitimately constant when
  no tick archive exists), but it means the council is configured not to complain about two features being dead.
  Any stacked-imbalance strategy has zero historical support unless `--all-footprint` is run.

### 2.6 The 3-Agent Council — necessary, well-built, and **not sufficient**

Individual checks are high quality: every finding carries `bar_index`, `open_time_ms` and a UTC timestamp (the
audit's item-8 promise, delivered), agents are isolated by `try/except` so an agent crash is itself a failure rather
than a silent pass, `run_council` sets `passed=False` on *any* finding, and the negative-control suite confirms gap,
duplicate, NaN, stale spot, missing POC, shifted EMA and centred VWAP are each rejected.

The structural limitation is the one the brief asks about directly, and the honest answer is **no, not sufficient**:

1. **Re-derivation is only as strong as its inputs.** Agent 2 recomputes `session_vwap`, `session_cvd`, `zc_div`,
   `basis` and the EMA recursions *from the same stored columns the generator consumed*. For an export produced by
   this pipeline, those checks are close to tautological — they verify internal self-consistency and catch
   storage/rounding damage (which is exactly what they caught in the legacy files, where the values had been
   externally rounded). They **cannot** detect a value that is self-consistent but fabricated, nor an input that was
   itself lookahead-contaminated at the source. The audit's framing ("a stored value can only match if it used no
   future data") is true of the *stored* series relative to the *stored* inputs; it does not extend to the raw
   ingestion layer above.
2. **Agent 1's cadence check passes trivially** for this pipeline, because `build_continuous_timeline` re-indexes
   onto an unbroken grid *before* export. Missing bars cannot appear as cadence violations; they reappear as
   `is_synthetic=1` flat bars. The check therefore validates the *reconstruction*, not the *market*.
3. **The dead-feature scan is a whole-column test and misses regime splits.** This is the mechanism behind the
   blocking defect in §4.1.
4. No agent verifies that a column's *values came from the exchange* rather than from a fallback constant. There is
   no `source`/`is_imputed` column, and the only provenance flags (`future_flow_source`, `spot_flow_source`,
   `poc_source`, `metrics_available`) cover flow and staleness — not OI, L/S ratios, whale index or taker ratio,
   which is where the fabrication lives.

---

## 3. Task 3 — Adversarial assessment of `run_historical_pipeline.py`

### 3.1 Edge-case analysis

| Area | Verdict |
|---|---|
| **Daylight savings** | **Immune — verified.** All time arithmetic is epoch-ms (`open_time_ms`, `close_time_ms = +899_999`, `// DAY_MS` for sessions); `datetime_utc` is built with `utc=True` and `strftime`. No local-tz conversion exists on any path. Sessions are 00:00 UTC-anchored, so the 23/25-hour DST days are handled correctly by construction. |
| **Exchange-downtime gaps** | Handled, with one silent bound. `_repair_gaps` attempts REST repair for `gap_idx[:200]` — gaps beyond 200 are *never attempted* and fall through to flat synthetic bars, only logged as `residual gaps after repair`. Correct output, but a hard, undocumented cap: a symbol with 400 gaps gets 200 REST repairs and 200 fabricated flat bars, indistinguishable downstream. Then `build_continuous_timeline` additionally tags `(high==low) & (volume<=0 | count<=0)` as synthetic, so genuine no-trade bars and downtime bars share one flag. |
| **Multi-threading on the shared HTTP client** | Safe within a client, **wrong across symbols** (§2.4). No lock-free correctness bug in the fetch path: each cache key maps to a distinct file, temp+`os.replace` everywhere, `_parallel` collects via futures. Only `stats` and `_not_found` are racy, both cosmetic. |
| **Forming-candle boundary truncation** | **Correct — verified.** `_rest_klines` filters `part["close_time"] < now_ms` with `now_ms` re-read at call time, and archives only contain completed days. Combined with `close_time = open + 899_999`, a still-forming bar cannot be emitted. The suite's mock-server test asserts exclusion, including the header/no-header CSV variants. |
| **µs vs ms timestamps** | `_norm_ms` uses `v.where(v <= 2e12, v // 1000)`. Correct for the 2025+ spot microsecond convention (documented by Binance) and safe for ms, since 2e12 ms is 2033-05. |

Additional findings from reading the orchestrator itself:

* **`run_audit=not args.all_symbols`** — in single-symbol mode the post-export `verify_all_parquets` runs per
  symbol; in batch mode it is deferred to one pass over `done` at the end. Defensible, but note the *export* already
  happened and `os.replace`d over the previous file before the batch audit runs, so a batch never leaves you with
  "audited but unexported" — it leaves you with "exported then audited". Acceptable only because the gate before
  export (`run_council`) is the authoritative one. The second audit is redundant re-derivation on read-back; its
  real value is catching Parquet round-trip damage, which is exactly what the legacy files suffered.
* **`existing_output_is_current` is slow and partially redundant.** It reads the full master
  `open_time_ms` column **and** the full ladder `open_time_ms` column (a 3 M+ row scan, multi-GB ladder file) to
  evaluate `np.isin(m_ts, l_ts).all()` — a check the generator guarantees (§2.5) — on every symbol, every run. On a
  warm cache this can dominate wall-clock. Prefer the manifest's `ladder.synthetic_candles == 0` + freshness +
  schema check, which is O(1).
* **It does not check that the council ever passed.** A hand-corrected file with the right schema, full coverage and
  a fresh last bar is accepted. Low risk given `run_council`-before-export, but the manifest already contains
  `verification.passed` and `repair_rounds` — reading them is free and would make the fast-skip a real gate.
* **`causal_repair` ladder branch can raise.** `ladder[ladder["rung_source"] == 0]` is guarded by
  `"rung_source" in ladder`, but the follow-on `keep[keep["rung_source"] == 0]` inside the `bad_ts` branch is not
  independently guarded, and `stats` is bound only inside the first `if`. On a non-canonical ladder this is an
  `AttributeError`/`UnboundLocalError` inside the repair path rather than a clean rejection. Practically unreachable
  (the exporter enforces the schema) but it is the kind of thing that turns a recoverable failure into a crash
  mid-batch. Also note `bad_ts` uses `f.open_time_ms` from findings whose `open_time_ms` is `Optional[int]`;
  the `and f.open_time_ms` filter covers `None`, but also silently drops bar `0`.
* **`run_pipeline(clean_cache=...)` is dead from the CLI.** `main()` hardcodes `clean_cache=False` in the per-symbol
  call and does the rmtree post-batch only `if audit_ok` — which is the *correct* behaviour (never delete the cache
  before a successful export). The parameter's per-symbol effect is unreachable. Harmless; worth noting so nobody
  "fixes" it into a data-losing order.
* **`**_legacy_kwargs` silently ignores `start_year`/`end_year`**, and those flags are `argparse.SUPPRESS`-ed. An
  operator who passes `--end-year 2024` expecting a truncated build gets a full build. The `action="store_true"`
  help strings should say so, or the flags should error.

### 3.2 Warm-up and ingestion convergence — **guarantee does not hold**

The mechanism is right: indicators are computed on `warmup_start → now`, and the
`open_time_ms >= export_start_ms` slice is applied **afterwards**, with lifetime CVD re-anchored so
`lifetime[0] == delta[0]`. Discarding warm-up bars after computation is the correct order, and the re-anchor is a
detail most implementations miss.

But `warmup_start = max(2019-09-01, listing)` and `effective_start = max(2020-09-01, listing)`:

| asset | listing | warm-up bars before slice | span-800 convergence |
|---|---|---:|---|
| BTC, ETH, XRP, ADA, TRX, LINK, LTC, BCH, BNB, DOT, DOGE | ≤ 2020-08 | ~150 k–210 k | **converged** (~0.99999 weight decayed; seed influence < 1e-40) |
| SOL (2020-09-14), AVAX (2020-09-23), NEAR (2020-10-15) | ≈ export start | ~0 (listing ≈ start) | **unconverged at slice head** |
| **OP (2022-06-01), APT (2022-10-19), SUI (2023-05-03), ARB (2023-03-23)** | after start | **exactly 0** | **unconverged** |

For those, `effective_start == warmup_start == listing`, so bar 0 of the export is bar 0 of the EMA seed. Consequences:
`ema_800[0] = close[0]` exactly; `atr_100` uses the expanding mean for its first 99 bars; `rsi_14` for its first 13;
`ema_200` needs ~800–1,600 bars to shed its seed and `ema_800` roughly 4×800 ≈ 3,200 bars ≈ 33 days. Because Wilder
RSI/ATR here use *expanding-mean* warm-up rather than NaN, **nothing marks these bars**: no null, no flag, no
council finding (Agent 3's `nulls` check requires nulls; the values are finite and legal). A walk-forward that
starts at an asset's listing silently trains on a different indicator definition than one starting in 2021.

Two mitigating notes in the pipeline's favour: (a) the audit's own comment says EMAs are "seeded from the first
warm-up bar", so the deviation is a *stated convention*, consistently applied, not an accident; (b) the
prefix-invariance property means the unconverged head is *stable* — re-running later does not silently rewrite
history. Both are worth more than in most pipelines and neither fixes the bias.

**Required before batch export (any one):** emit NaN for `t < 4·period` and let the strategy layer handle it; or add
a `warmup_bars_remaining`/`is_converged` column to the schema; or refuse `effective_start < warmup_start + 3200`
and let late-listed assets start later; or (cheapest) record the condition in the manifest and exclude the first
3,200 bars of any post-2020-listing asset from OOS window construction. **Do not rely on the current behaviour.**

### 3.3 Fast-skip integrity — **yes, the stated goal is achieved**

`existing_output_is_current` requires, conjunctively: both files exist; `schema_arrow.names == CANONICAL_COLUMNS`
(exact list, exact order — all 70); `lf.schema_arrow.names == LADDER_COLUMNS` (all 10, so `rung_source` must be
present and flags must be `int8`); last row group's final `close_time_ms` within `max_age_hours=24`; full master→ladder
bar coverage; `> 1000` rows; and any exception collapses to `False` (rebuild).

Against the legacy artifacts this is a **hard rejection on three independent grounds**: `columns` finding (62 ≠ 70),
`ladder_columns` (no `rung_source`), `ladder_dtype` (`int64`). So the item-6 vulnerability is genuinely closed, and
stale files cannot masquerade as valid. Verified by the orchestrator end-to-end suite ("contract-aware fast-skip").

Gaps, in order of importance: (1) no `verification.passed` check from the manifest, (2) the coverage conjunct is
unverifying-by-construction and costs a full ladder scan (§3.1), (3) `age_h` uses the *data* horizon, not
`exported_at_utc` — so a complete-but-stale-cache rebuild is never skipped, which is safe but slow, and conversely a
file whose last bar is recent passes regardless of when it was built.

### 3.4 Execution verdict

**Not certified. Two code adjustments are required before a full 18-asset regeneration** (§4.1, §3.2). The
mathematical core is certified sound: vectorised kernels, prefix invariance, 8-dp precision, close-time causal
joins, causal ladder geometry, atomic schema-validated export, DST immunity, forming-candle exclusion. Documentation
claims must also be corrected (RMA bit-identity, "process-wide" latch, "100 % coverage" as evidence of validity, and
the audit's provenance anchor `main@de866f4`, which **does not exist in this repository** — the repo contains
exactly two commits, `161ef7f` and `22f09b5`).

---

## 4. Findings requiring code change

### 4.1 BLOCKER — fabricated defaults for unavailable metrics pass the council

`historical_metrics_processor.py` replaces "no data" with legal constants:

```
oi_coin   = np.where(np.isnan(oi_coin), 0.0, oi_coin)          # OI := 0
oi_usd    = np.where(np.isnan(oi_usd),  oi_coin * c, oi_usd)   # := coin × price
ls_glob   = np.where(np.isnan(...), 1.0, ...)                  # neutral := 1.0
ls_top    = np.where(np.isnan(...), 1.0, ...)
top_acc   = np.where(np.isnan(...), ls_glob, ...)              # -> whale_index := 100.0
taker_ratio = np.where(np.isnan(...), fallback_taker, ...)
fr        = np.where(np.isnan(fr), 0.0001, fr)                 # funding := 0.0001
basis     = np.where(np.isnan(spot_close_ff), 0.0, c - spot_close_ff)
```

**Why it matters for the target window:** the metrics archive is the only source for `2020-09 → present`; the REST
bridge `_rest_metrics_bridge` requests `period=15m&limit=500` with **no `startTime` and no pagination**, and Binance
documents that only the latest 30 days of `/futures/data/*` is available. So `futures/data` cannot backfill 2020, and
the whole 2020–2021 coverage question rests on `data.binance.vision/data/futures/um/daily/metrics/`. Community
reporting indicates those long/short-ratio series begin materially later than the kline archives. **This is the
single highest-value pre-flight check in this entire plan and it is 30 seconds of work:**

```bash
for y in 2020 2021 2022 2023; do
  for m in 01 06 12; do
    code=$(curl -s -o /dev/null -w '%{http_code}' \
      "https://data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/BTCUSDT-metrics-$y-$m-15.zip")
    echo "$y-$m-15 -> $code"
  done
done
```

Any `404` in 2020/2021 confirms the gap. **Reproduce the false negative** (`Engine/verification/audit_probe_metrics_coverage.py`,
committed; exits 1 while the blind spot is present). 40,000 DOGE-scale bars, metrics archive
covering only the last 40 % of the sample:

```
bars with NO metrics: 24,000/40,000  (60.0 %)
  open_interest_k     head: mean=      0.0000 nunique=  1 | tail nunique= 15,999
  ls_ratio_global     head: mean=      1.0000 nunique=  1 | tail nunique= 15,883
  whale_index         head: mean=    100.0000 nunique=  1 | tail nunique= 15,990
  oi_change_pct       head: mean=      0.0000 nunique=  1 | tail nunique= 15,994
COUNCIL VERDICT: passed=True  {'Agent1:Continuity': 'PASS', 'Agent2:Microstructure': 'PASS', 'Agent3:Schema': 'PASS'}
BLIND SPOT REPRODUCED
```

60 % of the file is fabricated and **all three agents pass**. The `dead_feature` scan tests `nunique() <= 1` on the
*whole column*, so a series that is constant in one regime and rich in another is invisible to it.

Note the same test at a *fully* absent archive does get caught — 100 % coverage ⇒ `nunique==1` ⇒ 8 `dead_feature`
findings and rejection. So the council's ability to detect fabrication is entirely an artefact of whether the
contamination is total. A partially-covered stream is the dangerous case and it is the realistic one.

`metrics_available=0` *does* mark these bars, so the information is recoverable by a careful consumer — but the
z-score features derived from them (`long_liq_zs`, `short_liq_zs`, `vwap_zscore` unaffected, `open_interest_usd`) are
computed on the fabricated inputs, `_finalise` zeroes non-finite values so nothing survives as null, and nothing in
the pipeline *forces* a downstream filter on `metrics_available`.

**Required fix (either, and both are small):**
1. In `_finalise`, replace `arr[bad] = 0.0` + constant-fills with NaN where the domain allows, and add an
   `is_imputed_metrics` int8 column (or extend `metrics_available`'s contract to be authoritative); **and**
2. Add a council check for regime-split fabrication, e.g. per-year `nunique` of the metric columns, and a
   "unavailable-fraction" gate that reports `mean(metrics_available == 0)` by calendar year into the manifest so a
   60 %-fabricated series cannot be silently traded.

Until (1)+(2), a strategy consuming `open_interest_k`, `oi_change_pct`, `ls_ratio_*`, `whale_index`,
`taker_volume_ratio` or `funding_rate_pct` over 2020–2021 is measuring Binance's archive coverage window, not the
market.

### 4.2 BLOCKER — warm-up convergence guarantee (§3.2), fix per §3.2

### 4.3 Should fix

* **ML liquidation synthesis is on by default and unverifiable in-repo.** `MathematicalLiquidationModel` loads
  `Engine/core/trained_models/extra_trees_long_liq.joblib` + `..._short_liq.joblib` (both present, 25.6 MB + 22.5 MB)
  and, when load succeeds, `long_liq_usd`/`short_liq_usd` — hence `long_liq_zs`, `short_liq_zs`,
  `liq_imbalance_ratio` — are **model predictions, not exchange-reported liquidations**. The header claims
  "Calibrated against 7,234 Ground-Truth 15m CoinGlass Liquidations (June–Aug 2026) … >97 % Linear Parity (R² > 94 %)"
  with no training script, dataset, split or evaluation code anywhere in the repo. Three independent problems:
  (a) **no reproducibility** — the artifacts are opaque blobs and the claim is unauditable; (b) **scikit-learn
  version skew** — every run emits `InconsistentVersionWarning: unpickle estimator ExtraTreesRegressor from version
  1.8.0 when using version 1.9.0 … might lead to breaking code or invalid results`; unpickling estimators across
  major versions is explicitly unsupported and can silently change predictions, so the exports are not
  byte-reproducible across environments; (c) **leakage risk by construction** — the pipeline applies a model
  "calibrated" on June–Aug 2026 data to bars from 2020 onward, so if calibration was global rather than
  strictly pre-2020-trained, every feature derived from liquidations carries forward-informed bias, and **no
  council check can see it** (Agent 2 only asserts polarity and the [−1,1] domain, both of which a prediction
  satisfies). Binance does not publish historical liquidation archives, so *some* model is unavoidable — the defect
  is that the export does not say so. **Add `liq_source` (`MODEL_V4`/`EXCHANGE`) to the schema**, pin `scikit-learn`
  exactly, and ship the evaluation script or delete the parity claim.
* **USDC OI aggregation injects an undocumented level shift.** `fetch_metrics(include_usdc=True)` sums
  `{BASE}USDC` OI into the `{BASE}USDT` series — a deliberate, defensible economic choice (margin is shared) that
  makes `open_interest_k` mean something other than what the symbol key says, with **no provenance flag**, no
  manifest field, and `USDC_METRICS_FLOOR = 2023-03-01` producing a discontinuity in the OI *level* on that date.
  `oi_change_pct` will show a spurious jump there (capped at ±100, so the `oi_change_domain` check stays green), and
  any OI-magnitude-based feature inherits a structural break mid-sample. Also the probe is `usdc_days[-3:]` against
  `{BASE}USDC` perps that were mostly delisted in 2023 — so it typically returns 404s (negative-cached, so no
  repeated cost, but 3 wasted requests per symbol) while `{BASE}USDC` klines/metrics for the *pre-delisting* period
  are silently ignored. **Record `usdc_oi_aggregated: true/false` in the manifest and gate `include_usdc` on the
  floor date being inside the export window.**
* **`oi_change_pct` on the 0→first-real-OI bar.** `where=prev_oi > 0` forces the change to 0.0 on exactly the
  regime-transition bar instead of marking it unavailable, and the true first bar of OI data is then indistinguishable
  from a genuinely flat book.
* **`build_continuous_timeline` marks genuine zero-trade bars `is_synthetic=1`.** `degenerate = (high==low) &
  ((volume<=0) | (count<=0))` conflates exchange downtime with a quiet minute where the exchange was up. The
  ladder then emits a single zero-volume rung for those, so a genuine no-trade bar becomes indistinguishable from a
  halt — the wrong distinction for a liquidity or gap study. `synthetic` and `degenerate` should be separate flags.

### 4.4 Minor / cosmetic

`run_pipeline` logs `master['datetime_utc'].iloc[0]` before checking `len(master) > 0`; `nice_bin_step` returns
`max(step, 1e-6)`, which for a 1e-4-priced asset makes the floor a meaningful share of the price; `get_merge_level`
matches on `s.startswith("BTC")` (fine for the fixed universe, silently `0.0001` for anything else);
`estimate_depth_from_volatility` returns `depth_usd, depth_usd.copy(), depth_coin, depth_coin.copy()`, so bid and
ask are *distinct arrays with identical values* and the bid/ask asymmetry is 0 by construction — a proxy whose implied spread is identically 0; verified on the shipped canary: bid==ask on all 210,788 bars (see REREVIEW_ADDENDUM A6); `MAX_RUNGS` widening mutates `step` in place on the slice used later for
`price_bin` (correct here, fragile); `_coerce`'s `np.isfinite` backstop is unreachable for master because
`_finalise` pre-zeroes.

---

## 5. Verification-of-the-verifier: what I did and did not confirm

**Confirmed by execution** (this environment): 9/9 offline suites pass; RMA parity measured (`1.954e-14`); EMA
parity measured (exactly `0.0`); prefix invariance measured over 103 + ~140 prefixes with 0 violations; precision
table measured on 40 k DOGE-scale bars; council false-negative on 60 % fabricated metrics reproduced; `basis_identity`
margin checked at three price scales; `nice_bin_step` causality and ladder geometry checked; scale benchmark
reproduced — **210,600 bars: process 3.0 s, ladder 0.3 s (2.85 M rungs), council 1.1 s, export 0.8 s, peak RSS
1.15 GB** vs the audit's claimed 3.4/0.5/1.4/1.5 s at 1.25 GB on 2 CPU/3 GB, i.e. **the audit's performance
numbers are honest and slightly conservative**. Master parquet measured at **99.2 MB** for 70 columns, against the
legacy 62-column manifest's 54.03 MB.

**Not confirmable in this sandbox, explicitly:** no outbound network to `data.binance.vision`/`fapi` (TLS handshake
blocked), so archive coverage (§4.1), the 800-EMA convergence on *real* BTC data, `Retry-After` behaviour against a
live 429, and the 18-asset `atr_14==0` percentages all remain the audit's assertions. The mock-Binance-server suite
tests the fetcher's *parsing and stitching* against a Binance-shaped server, which is valuable and not nothing — but
it is self-referential on coverage questions, and it is the reason §4.1's one-line `curl` loop is the highest-value
remaining action.

**Also not at parity:** the "dual parity mirror" `kbsingh1399/Engine_1_arena_PR` is a different tree (`Engine_2/`,
not `Engine/`), and all five compared files differ (`canonical_indicators.py` is 263 lines there vs 357 here), while
`Engine_2/pipeline/` lacks `footprint_ladder.py` and `http_client.py` entirely. **Do not treat it as a second
copy of the audited code**; it is an earlier revision and cross-referencing it will produce spurious conclusions.

---

## 6. Operational regeneration directive

### 6.1 Commands

Because of §4.1 and §3.2, do **not** start with `--all-symbols`. Sequence:

```bash
# 0. PRE-FLIGHT (do this first; gates everything) — metrics archive coverage back-fill feasibility
for y in 2020 2021 2022 2023; do for m in 01 06 12; do
  printf "%s-%s -> %s\n" "$y" "$m" "$(curl -s -o /dev/null -w '%{http_code}' \
    "https://data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/BTCUSDT-metrics-$y-$m-15.zip")"
done; done

# 1. Reclone from the branch carrying this audit + the engine (see §6.4)
git clone git@github.com:kbsingh1399/Trading.git && cd Trading
python3 -m venv .venv && . .venv/bin/activate
pip install "pandas>=2.2" "numpy>=1.26" "pyarrow>=15" "scikit-learn==1.8.0" joblib   # pin 1.8.0: the models were
                                                                                      # pickled under it; see §4.3

# 2. SINGLE CANARY, one old asset + one late-listed asset, no footprint, forced rebuild
python3 -m Engine.run_historical_pipeline --symbol BTCUSDT --start-date 2020-09-01 --workers 8 --force
python3 -m Engine.run_historical_pipeline --symbol SUIUSDT --start-date 2020-09-01 --workers 8 --force   # §3.2 case

# 3. Inspect the two manifests before proceeding
python3 - <<'PY'
import json
for s in ("BTCUSDT","SUIUSDT"):
    d=json.load(open(f"Engine/binance_backtesting_data/{s}_dataset_manifest.json"))
    v=d["verification"]; l=d.get("ladder",{})
    print(f"{s:9} passed={v['passed']} rounds={v.get('repair_rounds')} cols={d['column_count']} "
          f"rows={d['total_rows']:,} synthetic={d['provenance']['synthetic_bars']:,} "
          f"metrics_ok={d['provenance']['metrics_available_bars']:,}/{d['total_rows']:,} "
          f"tick_exact={d['provenance']['tick_exact_bars']:,} laddersyn={l.get('synthetic_candles')}")
PY

# 4. Independent council re-read from disk (the authoritative gate)
python3 -m Engine.verification.verify_parquet_integrity Engine/binance_backtesting_data --symbol BTCUSDT
python3 -m Engine.verification.verify_parquet_integrity Engine/binance_backtesting_data --symbol SUIUSDT

# 5. Fabrication gate that the council does NOT implement (§4.1) — must be added to CI/launch checklist
python3 - <<'PY'
import pandas as pd, numpy as np
for s in ("BTCUSDT","SUIUSDT"):
    m=pd.read_parquet(f"Engine/binance_backtesting_data/{s}_15m_master_2020_2026.parquet",
                      columns=["datetime_utc","open_interest_k","ls_ratio_global","metrics_available"])
    m["y"]=m.datetime_utc.str[:4]
    g=m.groupby("y").agg(bars=("y","size"), oi_zero=("open_interest_k",lambda x:(x==0).mean()),
                         ls_flat=("ls_ratio_global",lambda x:x.nunique()), met_avail=("metrics_available","mean"))
    print(s); print(g.to_string(float_format=lambda v:f"{v:.3f}"))
    print("  >>> UNTRUSTWORTHY YEAR RANGE:", list(g.index[g.oi_zero>0.05]) or "none", "\n")
PY
```

Only after steps 0–5 are clean (and §4.1/§3.2 are patched, or the affected years/features are excluded by policy):

```bash
# 6. Full batch, sequential, warm cache, no tick footprint
python3 -m Engine.run_historical_pipeline --all-symbols --start-date 2020-09-01 \
        --workers 16 --footprint-days 0 --force 2>&1 | tee logs/pipeline_$(date +%Y%m%d).log

# 7. Council over the whole universe; exit code is the gate
python3 -m Engine.verification.verify_parquet_integrity Engine/binance_backtesting_data
echo "council exit=$?"

# 8. Tick-exact ladder, ONLY if stacked-imbalance features are actually traded — budget separately (§6.2)
python3 -m Engine.run_historical_pipeline --symbol BTCUSDT --footprint-days 14 --force
```

`--all-footprint` is **not recommended**: 6 years of aggTrades for 18 symbols is O(50–120) GB/day·symbol compressed
for the majors, i.e. many terabytes of download and an order-of-magnitude-longer runtime, for rungs that are exact
only where Binance publishes them.

### 6.2 Runtime, CPU/RAM, disk

Measured/computed per symbol (210,613 bars) on 2 vCPU, scaled linearly where noted:

| stage | measured |
|---|---|
| fetch (cold cache) | **network-bound: 8–25 min/symbol** — 72 monthly futures + 72 monthly spot + ~2,190 daily metrics + ~160 funding pages ≈ 2,500 objects |
| process (Table 1, 70 cols) | **3.0 s** |
| ladder (2.85 M rungs, synthetic) | **0.3 s** |
| council | **1.1 s** |
| export master (99.2 MB) | **0.8 s** |
| peak RSS | **1.15 GB** (audit claims 1.25 GB — consistent) |

* **Compute:** ~5 s/symbol ⇒ ~90 s for 18 assets. Negligible.
* **Wall clock:** dominated by download. `--workers 16` with `min_interval=0` on data.binance.vision: **expect
  2.5–7.5 h for the 18-asset cold run**, with 429/418 latch stalls as the variance source. Warm cache (re-runs):
  **~3–6 min total**. Sequential batching is correct here — do not parallelise symbols (§2.4: 18 independent
  cooldown latches ⇒ 288 streams ⇒ ban).
* **CPU:** 2 vCPU suffices (parallelism is I/O-bound and inside per-symbol thread pools); 4 vCPU removes the
  16-worker contention tail.
* **RAM:** **peak ~1.5 GB per symbol** → a 4 GB instance is comfortable, 8 GB has headroom for value-area dense
  tensors on wide-range days (`max_cells_per_chunk=4e6` bounds it). Never run symbols in parallel processes at
  1.15 GB each without a cgroup limit.
* **Disk, final outputs:** master 70-col ≈ 60–100 MB × 18 ⇒ **~1.8 GB**. Ladder: BTC legacy was 2,992,918 rows;
  synthetic-only for sub-dollar assets with `bucket=1e-4` can reach ~3–5 M rows ⇒ ~0.3–1.2 GB each ⇒
  **~5–18 GB**. Total **~7–20 GB**.
* **Disk, cache (the real number):** futures+spot monthly klines ≈ 0.1–0.3 GB/symbol; daily metrics ≈ 0.5–1.5
  GB/symbol; funding ≈ 2 MB. **~12–32 GB** for all 18. Budget **60 GB** for cache+outputs together. With
  `--footprint-days N` add ~0.15–0.4 GB/day/symbol (14 days × 18 ⇒ +40–100 GB).

### 6.3 Council protocol before deploying on the 20 OOS windows

Gate **the data**, then gate **each window**, then gate **the feature contract**:

1. **Data gate (once).** `verify_parquet_integrity` over the directory must exit 0. Require *all three* of:
   `agent_status` all `PASS`; `manifest.column_count == 70`; `manifest.ladder.synthetic_candles == 0` **only if**
   exact ladders were fetched — otherwise assert `rung_source==0` fraction is documented as 0 and *forbid*
   imbalance features. Additionally run §6.1 step 5: any year with `oi_zero > 0.05` is excluded from OOS windows
   that use OI/L-S/whale/taker/funding until §4.1 is patched.
2. **Continuity gate.** Assert `total_rows` matches the elapsed-time expectation (`(end−start)/15min + 1`), and
   that `start_time_utc`/`end_time_utc` bracket the requested slice per symbol — this catches the fast-skip hole
   where freshness is data-derived (§3.3). Log `synthetic_bars / total_rows` per symbol; a value above ~0.5 %
   indicates the 200-gap repair cap was hit (§3.1) and needs a manual look.
3. **Per-window leakage gate (the decisive one for OOS).** For each of the 20 windows, extract the window *and*
   re-run Agent 2's re-derivation on the isolated slice, requiring bitwise equality with the full-history slice.
   Prefix invariance (§2.1) is exactly the property that makes this a *strong* test: any feature that depends on
   post-window data — a centred window, a full-sample z-score, a whole-day median bin step — must differ, and the
   test will say so. A window that passes is causally clean *given* clean inputs. Then assert
   `close_time_ms[window_last] < window_start_of_first_future_order` for the executor's assumed fill model.
4. **Warm-up gate.** For any window on an asset listed after 2020-09-01, drop the first `max(4·800, 4·100, 4·14)`
   = 3,200 bars, or require a `is_converged` flag (§3.2). This is currently on you, not the pipeline.
5. **Feature-contract gate.** Assert `fp_stacked_*_imb` are excluded from any model trained on `footprint_days=0`
   exports (§2.5), and that `long_liq_*`/`liq_imbalance_ratio` are only used with the `liq_source` disclosure in
   place (§4.3). Any `scikit-learn` version mismatch during the rebuild means the liquidation columns are not
   reproducible and the run must be redone with the pinned version.

### 6.4 Git state of this review

All artifacts are committed and pushed to the session branch (no production module was modified):

```bash
git clone git@github.com:kbsingh1399/Trading.git && cd Trading
git fetch origin arena/01a07263-trading
git checkout arena/01a07263-trading          # full tree: Engine/ at main@161ef7f + this audit + the two probes
# or, onto an existing main checkout:
git fetch origin arena/01a07263-trading && git checkout -b verify main && git merge --ff-only origin/arena/01a07263-trading
```

---

## 7. One-paragraph verdict

The rebuild is real engineering, not a patch: the sub-dollar annihilation, the stale-spot backward-reuse, the
open-time staleness, the loop-bound kernels, the whole-day-median bin step, the `int64` flag drift and the missing
`rung_source` are all genuinely addressed, and every one of those claims survived my attempt to break it — including
a dense prefix-invariance sweep that went beyond what the test suite itself asserts. The legacy datasets are invalid
on three independent grounds and must be regenerated; that is already forced mechanically, since the 62-column files
fail the new contract's fast-skip probe. But **certification is withheld**: the pipeline can fabricate a majority of the
open-interest and positioning series in a way that passes all three agents because the fabrication is piecewise-constant
rather than null or constant (reproduced, `passed=True`), and it silently exports an unconverged `ema_800` head for
every post-2020 listing; and its supporting documentation overstates two properties I could measure
("bit-identical" RMA at a true `1.954e-14`, "process-wide" cooldown that is per-client), treats a generator-guaranteed
"100 % ladder coverage" as evidence of validity, and anchors its audit to a commit (`de866f4`) absent from the
repository. Fix §4.1 and §3.2, correct the claims in §2, run the one `curl` pre-flight in §6.1, and this becomes a
certifiable pipeline.
