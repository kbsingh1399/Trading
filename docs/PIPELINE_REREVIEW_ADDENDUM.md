# Re-Review Addendum — Mitigation of §4.1 / §3.2 and BTCUSDT Canary Ingest

**Assessed tree:** `kbsingh1399/Trading@116619a` (`main`), baseline `161ef7f` → `ce535dd` (fixes) → `f6c75e4` (canary data)
**Prior report:** `docs/PIPELINE_VERIFICATION_CERTIFICATION.md`
**Date:** 2026-09-05

This addendum supersedes the two BLOCKER verdicts of the prior report and records a **new blocking
data-quality finding present in the shipped canary file itself**. Every statement below was
verified by execution against the real 94 MB `BTCUSDT` Parquet, not by reading the manifest.

---

## 1. Certification verdict

> ### The two prior blockers are genuinely closed. Two new blockers are opened by the data itself.
>
> **Headline: the verification infrastructure is sound, and the canary's manifest tells the truth
> about a file that is materially worse than it reports.** 14.45 % of the certified bars
> (30,463) carry frozen positioning data marked fresh, and 160 bars carry impossible open interest.
> Neither is detectable by any check currently in the council.
>
> **§3.2 (warm-up convergence): CLOSED, and closed well.** `is_warmup_converged` is correct, and I
> validated the 3,200-bar threshold *on real BTC closes* rather than accepting it (§2.2). The flag is
> honest, the manifest records it, and it is exempted from the dead-feature scan so a fully-converged
> file does not self-reject. No further action.
>
> **§4.1 (metrics fabrication): the mechanism is real but the gate is under-scoped — CLOSED for
> whole-calendar-year gaps only.** The `regime_dead_feature` scan fires for the right reason and my
> probe now exits 0 because of that scan, not an incidental failure (§2.1). But it is keyed to
> calendar-year granularity, and it is fed by an `is_imputed_metrics` column that is a **pure alias of
> `metrics_available == 0`** and therefore covers **1 of the 10 imputation sites** in the processor
> (§3, A2/A3). Two adversarial constructions reproduce the open path (§3.1).
>
> **New BLOCKER (A1b) — the larger one: 30,463 bars (14.45 % of the file) hold positioning data that
> sat bit-identical for up to 117 consecutive days while open interest moved on every single bar, and
> every one of them is marked fresh.** Four episodes, all but 134 bars inside 2022. `ls_ratio_global`
> stayed live across the same windows, so this is per-column staleness that a single OI-keyed
> availability bit cannot express — and `whale_index`, which is in the scanned list, *varies*
> precisely because it divides a frozen numerator by a live denominator. See §3 A1b.
>
> **New BLOCKER (A1): the canary file also ships 160 physically impossible open-interest bars, marked
> fresh, passing all three agents — and they are the majority of the file's extreme OI-change
> signal.** BTCUSDT perpetual OI has never been zero. 67 bars read exactly `0.0` and 93 more fall
> below 20 % of their own local median; **all 160 carry `metrics_available = 1` and
> `is_imputed_metrics = 0`**, and `100 of the 182` bars with `|oi_change_pct| ≥ 50 %` sit on them —
> i.e. **54.9 % of the strongest OI-contraction events in the entire 6-year file are artifacts**
> (§3, A1). Root cause is located and a one-line fix is given.
>
> **Do not run `--all-symbols` expecting OI/positioning features to be usable.** See §5.

**What I could not test, unchanged from last time:** there is still no egress to
`data.binance.vision` / `fapi` from this sandbox, so archive *coverage* claims remain
unverifiable here. That limitation is now largely moot for the specific question of whether the
2020 metrics hole exists, because the canary answers it empirically (§2.4): metrics are real and
dense from 2020-09-01 onward. That materially *upgrades* my prior assessment of the ingestion
layer, and it is why A1 is a bounded 160-bar problem rather than the 40 %-of-history fabrication I
feared. Credit where due: the fetcher did something right that I could not previously confirm.

---

## 2. Requested verification tasks — results

### 2.1 Probes and suites (all executed)

| Command | Claimed | Actual | Notes |
|---|---|---|---|
| `python -m Engine.verification.audit_probe_metrics_coverage` | exit 0 | **exit 0** ✅ | Rejects with `regime_dead_feature` × 6 (Agent 3, `FAIL (6)`) — *right reason*, not incidental |
| `python -m Engine.verification.audit_probe_indicator_parity` | 0 violations | **0 violations** ✅ | 145 prefixes; RMA `1.954e-14` (still nonzero), EMA exactly `0.0` |
| `python -m Engine.verification.test_pipeline_offline` | 9/9 | **9/9 PASS, 12.7 s** ✅ | pandas 3.0.5 / numpy 2.4.6 / pyarrow 25 / sklearn 1.9.0 |

**Caveat on the coverage probe (A5).** It exits 0 because its fixture places the gap at
`0.60 × N` of a 40,000-bar series that begins 2020-09-01 — which happens to align exactly with
**whole calendar years**. The probe is therefore a regression test for *year-aligned* gaps only, and
it will keep reporting "fix verified in place" while the sub-year path (§3.1) stays open. Move the
fixture boundary so a gap starts and ends inside one year, or add a second fixture.

### 2.2 The 3,200-bar threshold, measured rather than assumed

The flag's promise is "bars with ≥ 3,200 warm-up bars are safe to trust", so the only meaningful
error is the one that survives *inside* the trusted region. I re-seeded `ema_800` at five pretend
listing points on the **real** BTC close series:

| pretend listing index | error at first trusted bar | % of price | % of ATR-14 | max error over **trusted** bars | sign flips of `close > ema_800` |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.00000 | 0.0000 % | 0.00 % | 0.00000 | **0** |
| 20,000 | 0.34818 | 0.0006 % | 0.09 % | 0.34818 | **0** |
| 60,000 | 0.57554 | 0.0027 % | 0.30 % | 0.57554 | **0** |
| 120,000 | 0.26115 | 0.0004 % | 0.08 % | 0.26115 | **0** |
| 180,000 | 0.82786 | 0.0009 % | 0.27 % | 0.82786 | **0** |

Residual seed weight at 3,200 bars is `(1 − 2/801)^3200 = 3.355e-04`; raising the threshold to
9,200 drives it to `1e-10` but **changes nothing observable** — zero sign flips either way, so no
trend-filter or cross decision differs. **3,200 is empirically adequate.** Approving it.

Two honest caveats: the constant is bare rather than derived from the longest EMA period (adding a
`ema_2000` would silently invalidate the flag), and `warmup_bars` counts *grid positions* after
`build_continuous_timeline`, so gap-filled bars count toward convergence for a thinly-traded or
outage-prone asset. Neither affects the 18-asset universe materially.

### 2.3 Backward compatibility of the two new columns

Verified against the actual Parquet and the *old* manifest from `161ef7f`, not from memory:

* `columns == CANONICAL_COLUMNS` (names **and** order), all 72 — **PASS**
* `columns[:62] == LEGACY_COLUMNS` — **PASS**; and equal to the legacy manifest's 62 names in order — **PASS**
* new columns are exactly positions 71–72 (`is_imputed_metrics`, `is_warmup_converged`), both `int8` — **PASS**
* nulls `0`, non-finite `0` — **PASS**
* 5 string columns report pandas dtype `str` against the contract's `string`. **Not a defect**: the
  file stores `large_string` with `nullable=False` and Agent 3's allow-list accepts `str`. Flagged
  only because it will look alarming in any naive `str(dtype) == "string"` diff.

### 2.4 Canary manifest audit — every claim independently reproduced

| field | manifest | re-measured from file | |
|---|---|---|---|
| `total_rows` | 210,788 | 210,788 | ✅ |
| `column_count` | 72 | 72 | ✅ |
| `master_size_mb` | 94.17 | 94.17 | ✅ |
| `ladder_size_mb` | 14.97 | 14.97 | ✅ |
| `warmup_unconverged_bars` | 0 | 0 | ✅ |
| `imputed_metrics_bars` | 18 | 18 | ✅ |
| `synthetic_bars` | 15 | 15 | ✅ |
| ladder `synthetic_rungs` | 2,710,609 | 2,710,609 | ✅ |
| `verification.passed` | true | true (my own council run, 0 findings, 1.48 s) | ✅ |
| grid completeness | — | expected 210,788 = actual; **every** step exactly 900,000 ms; 0 duplicates; `close_time == open + 899,999` | ✅ |

`is_imputed_metrics == (metrics_available == 0)` holds on **all** 210,788 bars. The 18 flagged bars
are a single 2024 outage episode and are *correctly* flagged (their `ls_ratio_global` is `0.629012`
and `open_interest_k` is `90.659557` — real values, genuinely stale, properly marked).

**Metrics are real, dense and varying across the whole window** — 2020 has 11,703 distinct
`open_interest_k` over 11,712 bars, 11,612 distinct `ls_ratio_global`, mean 1.3666; no year is
constant anywhere. My prior §4.1 concern (a large fabricated 2020–2021 block) is **disconfirmed for
this asset**: the vision archives do reach back through the export window. `open_interest_k == 0`
occurs on 67 bars only — a data *quality* problem (§3 A1), not the coverage cliff I predicted.
I also checked the funding sentinel suspicion and it does **not** fire as a defect:
`median|funding| = 0.008840 %`, 4,062 distinct values, spread over all 7 years, consistent with the
genuine Binance default rather than the `0.0001` fallback — though see A7, the collision is real.

**Legacy purge is complete and correct:** `git ls-tree origin/main` on the data dir returns exactly
4 objects (2 Parquets, 1 manifest, `verification_report.json`); all 17 stale legacy manifests and the
old 330,787-finding report are gone. `verification_report.json` now holds only
`{"BTCUSDT": passed: true, findings: []}` — consistent with the manifest.

### 2.5 Zero-lookahead, re-derived from the shipped file

Recomputing each kernel from the file's own OHLCV and truncating its prefix (16 prefixes to 210,788
bars; 8 for value area) — **0 prefix violations on every feature**, `worst |Δ| = 0.000e+00`:
`ema_8/200/800`, `atr_14/100`, `rsi_14`, `volume_sma9`, `session_vwap`, `future_cvd_session`,
`session_vah/val`. Identities on real data: `zc_div` `3.638e-12`, `basis_usd == close − spot_close`
`1.339e-11`, `session_vwap` re-derivation `5.006e-09`, one-step `ema_800` recursion `9.975e-09`
(8-dp rounding noise). **The stored series are exactly what a causal kernel produces from this
candle set.**

Note `stored_vs_recomputed` for `ema_800` is `6.317e+01` — that is *not* a leak. My recomputation
seeds at the file's first bar; the export was seeded 23,520 bars earlier, during warm-up. The gap
**is the warm-up working**, and it is corroborated by `ema_800[0] = 11,578.8301 ≠ close[0] =
11,642.0000`: with no pre-history the two would be identical. So the "fetch from listing, slice
afterwards" design is verifiably real in the shipped bytes, which is precisely what §3.2 asked for.

### 2.6 The §1.3 stale-spot fix, tested on the same 93 bars that broke the legacy data

| | legacy (per `verification_report.json`) | canary |
|---|---|---|
| `spot_flow_source == UNAVAILABLE` bars | 93 | **93** |
| of those, stale non-zero `spot_cvd_15m` | **68** | **0** |

Same 93 bars, same outage, zero stale reuse. The 1:1 join with a hard `0.0` else-branch works on
real gaps. Ladder integrity is likewise exact: one POC per candle (min = max = 1), 0 duplicate
`(ts, price_bin)`, 0 uncovered master bars, volume conservation `0.000000`, `dtypes` all conform.

---

## 3. Adversarial findings

### A1 — **BLOCKER.** 160 impossible OI bars in the shipped canary, marked fresh, invisible to all three agents

`open_interest_k` reads exactly `0.0` on 67 bars (22 episodes, longest **38 consecutive bars**,
2021-05-22 → 2025-07-21) and is below 20 % of its own local median on 93 more. BTC perpetual OI
has no zero state. Every one of these 160 bars is `metrics_available = 1`, `is_imputed_metrics = 0`,
and the file passes the council with 0 findings.

Why each guard lets it through:

* `metrics_available` tests *staleness* (`age ≤ 6 h`), not validity — a fresh `0` passes;
* `oi_nonneg` accepts `0` (it checks `< 0`);
* `oi_change_domain` checks `|Δ| > 100` — but the value was **clipped to exactly ±100** first, so it
  lands on the boundary and passes. The legacy file failed this check with 69 findings; the fix made
  it *invisibly pass*, converting a loud rejection into a silent plausible signal;
* the new `regime_dead_feature` scan needs a whole year to go constant — 2022 has 34,988 distinct
  OI values alongside its 39 zero bars.

Measured blast radius: `oi_change_pct` on these bars is `-100.0 %` at each episode entry and
`0.0 %` on the recovery (because `where=prev_oi > 0` suppresses the return), so the derived feature
is not merely noisy but **asymmetrically lobotomised** — the drop is recorded, the unwind back is not.
100 of the file's 182 `|oi_change_pct| ≥ 50 %` bars are these artifacts.

**Most likely root cause — located, and it is one line.** In `fetch_metrics`, the USDC aggregation is
*itself* an imputation site that destroys `NaN`:

```python
primary["sum_open_interest"] = primary["sum_open_interest"].fillna(0.0) + primary["_oi_usdc"].fillna(0.0)
```

Verified semantics: `NaN + missing → 0.0`, i.e. "no data" becomes "exactly zero OI", which then
satisfies `~np.isnan(oi_coin)` downstream. Fix — preserve NaN through the addition:

```python
primary["sum_open_interest"] = primary["sum_open_interest"].add(primary["_oi_usdc"], fill_value=0.0)
primary["sum_open_interest_value"] = primary["sum_open_interest_value"].add(primary["_oiv_usdc"], fill_value=0.0)
```

I executed the replacement: `NaN + NaN → NaN` ✅, `100 + missing → 100` ✅, `300 + 5 → 305` ✅. It is
also applied to the **whole frame** rather than only post-`USDC_METRICS_FLOOR` rows, so a `NaN` from
2020 is destroyed too; and the left-merge means USDC-missing rows silently become "USDT-only" with no
flag. `USDC_METRICS_FLOOR = 2023-03-01` should bound the *addition*, not merely the download.

Caveat on attribution: most of these dates (2022-03-07/08, 2023-06-06, 2024-07, 2025-01-08,
2025-04-11, 2025-07-21) are known Binance *degradation* windows, so the upstream archive may
genuinely contain zero rows independent of the merge. Either way the pipeline must not launder a zero
into a fresh observation. I therefore also recommend the validity gate, which is source-agnostic:

```python
available = (~np.isnan(oi_coin)) & (oi_coin > 0) & (oi_age <= METRICS_MAX_STALENESS_MS)
```

and a matching Agent 2 check rejecting `open_interest_k == 0` while `metrics_available == 1`.

**Reusable gate added:** `Engine/verification/audit_probe_metrics_validity.py` — exits 1 on this file with
the counts, episode structure, per-year spread and the derived-feature contamination above. It now checks both A1 and A1b, reports the
union of affected bars rather than a double-counted per-column sum, and distinguishes a carry-forward
fill from genuinely stale upstream data. Runtime 0.7 s per asset; needs no re-ingest.

### A1b — **BLOCKER (larger than A1).** 30,463 bars (14.45 %) of frozen positioning data, marked fresh

Found by a run-length scan I wrote to double-check A1, not by anything in the pipeline. A **contiguous
run of ≥ 3 days in which a positioning column is bit-identical while `open_interest_k` changes on
~100 % of those bars** cannot be a market state, and it is not the pipeline's fault in the way A1 is:

| column | bars in run(s) | longest run | note |
|---|---:|---:|---|
| `ls_ratio_top` | 30,463 (14.45 %) | **9,819 bars = 102 days** | 5 runs |
| `top_account_ratio` | 30,463 (14.45 %) | 9,819 | same windows as above |
| `taker_volume_ratio` | 12,347 (5.86 %) | 9,429 | 2 runs |
| `ls_ratio_global` | 1,915 (0.91 %) | 1,915 | 1 run |
| `whale_index` | 1,915 (0.91 %) | 1,915 | 1 run |

De-duplicated union: **30,463 unique bars in 4 episodes, longest 11,200 bars (117 days)**,
concentrated in 2022 (2021Q4: 134, 2022Q1: 8,545, Q2: 5,793, Q3: 8,825, Q4: 7,166). Worst single
episode: `ls_ratio_top` pinned to `1.073470` from **2022-09-03 08:45 to 2022-12-14 15:15**.

Three things make this dispositive rather than merely suspicious, and I checked each:

1. **Not a market halt.** Inside the same windows `ls_ratio_global` takes **28,363 distinct values**
   over 30,463 bars, and `open_interest_k` moves on 100 % of bars. The exchange was publishing live
   global ratios while the top-trader family sat dead.
2. **Not an as-of carry-forward.** For every run the value *immediately preceding* it differs from
   the frozen value (e.g. `1.073833 → 1.073470`, `1.128144 → 1.127957`). A `merge_asof` fill would
   have repeated the previous observation exactly. So the flatness is **upstream in the metrics
   archive**, which is why `oi_age <= 6 h` stays satisfied — the *rows* are fresh, the *column* is dead.
3. **Not flagged.** `metrics_available = 1` on **30,463/30,463**; `is_imputed_metrics = 1` on **0**.

Why the certification apparatus cannot see it, and structurally cannot:

* `regime_dead_feature` needs a whole calendar year to go constant. 2022 still has 34,988 distinct
  `open_interest_k` values and 4,404 distinct `ls_ratio_top` values, so it is silent by construction;
* `whale_index` **is** in the scanned column list, and it *varies* (28,540 distinct values inside the
  frozen union) because it is `ls_top / ls_glob × 100` with one frozen input and one live input — a
  derived feature that launders a dead input into a moving output;
* the manifest's `metrics_unavailable_fraction_by_year` reports 0.0 for 2022 and is therefore **not a
  proxy for data quality**, only for the flag, which is the thing under suspicion.

Impact on consumers: any feature built on the top-trader family (`ls_ratio_top`, `top_account_ratio`,
`whale_index`) is constant for 14.45 % of the file, so z-scores, percentiles and any
regime-classifier trained on it will treat "the exchange stopped reporting" as "positioning was
perfectly stable for four months", which is exactly the inference a crowding/short-squeeze signal
must not make. This is the *same* defect class as the original §4.1, arriving through a different
mechanism — not missing data replaced by a sentinel, but present-but-dead data replacing live data.

Required fix (the year-granularity scan cannot be tuned into it; per-column state is the only
representation that fits):

Vectorised, per column, after the as-of join — and I ran this against the canary to confirm it
reproduces the run-length scan rather than just looking plausible:

```python
def _stale_mask(x: np.ndarray, k: int = 288) -> np.ndarray:
    """True where column x has not changed for >= k bars (15m => k=288 is 3 days)."""
    x = np.asarray(x, dtype=np.float64)
    changed = np.r_[True, np.diff(x) != 0]
    idx = np.flatnonzero(changed)
    last = np.searchsorted(idx, np.arange(len(x)), side="right") - 1
    bars_since = np.arange(len(x)) - idx[last]
    return bars_since >= k
```

Measured on the canary: `ls_ratio_global` 1,819 bars, `ls_ratio_top` / `top_account_ratio` 30,139,
`whale_index` 1,819, `taker_volume_ratio` 12,155 — union **30,235 bars (14.34 %)**, versus 30,463
(14.45 %) from the run-length scan. The 0.11 pp gap is simply that the mask starts counting *after*
the k-bar threshold while the run method attributes the whole run, so the two agree to within 4 % and
either can be used as the gate. Wire it as `is_imputed_metrics |= _stale_mask(col)` for each of the
five positioning columns, and add the equivalent Agent-2 rejection: *a scanned metrics column holding
one value for ≥ 288 consecutive bars while `open_interest_k` changes on ≥ 90 % of them is a fail.*
That rule fires on this file today, needs no re-ingest, and cannot be bypassed by the gap's position
in the calendar.

### A2 — **HIGH.** `is_imputed_metrics` is a tautology and covers 1 of 10 imputation sites

```python
out["is_imputed_metrics"] = (out["metrics_available"].to_numpy() == 0).astype(np.int8)
```

It carries no information that `metrics_available` does not already carry, and the new
`imputed_contract` check *enforces* that equality — so the column can never widen coverage. But the
processor has **ten** independent `np.where(np.isnan(...))` substitutions, and `metrics_available`
keys on OI alone:

| line | imputation | covered by the flag? |
|---|---|---|
| 250 | `oi_coin → 0.0` | ✅ yes — the only one |
| 252 | `oi_usd → oi_coin * close` | ❌ no |
| 253/254 | `ls_ratio_global`, `ls_ratio_top → 1.0` | ❌ no |
| 256 | `top_account_ratio → ls_glob` | ❌ no |
| 258 | `taker_volume_ratio → fallback_taker` | ❌ no |
| 221 | `funding_rate → 0.0001` | ❌ no |
| 211/213 | `basis_usd → 0`, `spot_close → close` | ❌ no |
| 290 | `fp_poc → (h+l+2c)/4` | ⚠️ separately flagged by `poc_source` |
| — | ML liquidation engine | ❌ no |

Per-column as-of joins mean **each column has its own availability**. The design correctly keeps a
sparse column from poisoning a dense one, but the single `metrics_available` bit then cannot describe
that per-column state — and `is_imputed_metrics` inherits the blindness. Build the flag as a
conjunction over the columns a consumer actually needs (or add a bitmask), otherwise the name will be
trusted beyond its content.

### A3 — **HIGH.** Two reproductions of the still-open path

| test | fabrication | council | `is_imputed_metrics` |
|---|---|---|---|
| **T1** — L/S columns missing 6 months *inside* 2021, OI present | **17,376 bars (43.4 %)**, `nunique = 1` throughout | **ACCEPTED, 0 findings** | **0** |
| **T2** — same gap crossing a year boundary | 2,079 bars (5.2 %) | **ACCEPTED, 0 findings** | **0** |
| **T3** — `oi_usd` fabricated as `oi_coin × close` | 40,000 distinct values | **ACCEPTED, 0 findings** | 0 |
| control — whole-year gap (my fixture's shape) | 24,000 bars (60 %) | **REJECTED** (`regime_dead_feature`) | 18 |

T1 is the important one: a mid-year hole is invisible to a scan that aggregates by calendar year.
T3 is a class no constancy test can ever catch, because the substitution is *derived from live data*
and so varies legitimately — `taker_volume_ratio` falling back to a kline-derived ratio is the same
shape of bug and it is **not even in the scanned column list**. Any fix must flag imputation at the
point of substitution (A2), not infer it from a constancy pattern after the fact.

### A4 — **MEDIUM.** `prev_day_vah/val` zero-hazard: **investigated and cleared.** My prior report
predicted a fresh-listing first day would export `NaN → 0.0` fake price levels. It does not:
`compute_session_value_area` overwrites day 0 with the day's own developing value area, and the real
file has **0** zero-valued `prev_day_vah`/`prev_day_val` bars. Recording this as checked-and-clean so
it is not re-litigated.

### A5 — **MEDIUM.** Retry-After is now *truncated* rather than bounded (regression introduced by fix C)

`cool = min(self.max_delay * 10, raw_cool)` caps at 600 s. Measured against a real Binance ban:

```
server Retry-After=  30s -> waits  120s
server Retry-After= 600s -> waits  600s
server Retry-After=3600s -> waits  600s   <== resumes while still banned
server Retry-After=86400s-> waits  600s   <== resumes while still banned
```

Capping the *computed* backoff is right; capping the *server's instruction* is counterproductive —
a 418 ban re-probed every 10 minutes extends the ban and, across a 6-year backfill, converts a
cooldown into a data gap that `build_continuous_timeline` then silently fills with flat synthetic
bars. Exempt `Retry-After` from the cap (bound it at, say, 2 h) or fail loudly. Unchanged from last
time: `min_interval` still defaults to `0.0`, so protection remains purely reactive.

**Fix C itself is verified working**, and this is the only defect I found in it: the latch is now
genuinely shared across independent instances in a process — `b._sleep_for_cooldown()` blocked
3.00 s after an unrelated instance `a` tripped a 3 s cooldown — and the global 404 cache is shared.
The `stats` counters and `_not_found.add` are now correctly lock-guarded, closing the lost-update
race I flagged. `causal_repair`'s unguarded `keep["rung_source"]` is fixed as suggested.

### A6 — **MEDIUM.** The extended microstructure features still carry no exchange information

The canary ladder is **100 % synthetic**: `rung_source == 0` on 0 of 2,710,609 rungs,
`tick_exact_candles: 0`, `fp_stacked_buy_imb`/`_sell_imb` `nunique = 1`, imbalance flag sums `0`,
`poc_source = OHLC_APPROX` everywhere, and `fp_poc == (h+l+2c)/4` exactly. `fp_delta ==
future_cvd_15m` identically, and the ladder adds no volume information beyond the Table-1 taker split.
So `session_vah/val`, `fp_poc`, `fp_delta` and both imbalance features are **relabelings of
`high/low/close/volume`**, not microstructure — and `bid/ask_depth_*` are the ATR elasticity proxy
(on all 210,788 bars `bid_depth_usd == ask_depth_usd` and `bid_depth_coin == ask_depth_coin`; the helper returns a `.copy()`, so they are distinct arrays with identical values), and the implied depth spread is therefore exactly 0 by construction. Honest and correctly
tagged, but a strategy must not treat Table 2 as evidence about the tape. The liquidation columns
remain model outputs (sklearn 1.8→1.9 `InconsistentVersionWarning` on every run) with no `liq_source`
column — **still unaddressed** from my §4.3.

### A7 — **LOW.** Sentinel/value collisions that no check can resolve

`funding_rate_pct` missing → `0.0001 × 100 = 0.01`, and 68,416 bars (32.5 %) are exactly `0.01`.
The sentinel is indistinguishable from a legitimate default rate, so "no funding data" cannot be
audited post-hoc; prefer `NaN` + an explicit flag. Likewise `whale_index = 100.0` and
`ls_ratio = 1.0` are both plausible market values *and* fabrication sentinels.

### A8 — **LOW (operational).** 94 MB Parquet committed to Git

`BTCUSDT_15m_master_2020_2026.parquet` is 94.17 MB — **6.2 % below GitHub's 100 MB hard block**, and
`.git` is already 125 MB. My own 70-column synthetic benchmark produced 99.2 MB for a comparable
series, so several of the 18 assets (SOL, DOGE, and high-tick-count ladders) are likely to **exceed
100 MB and be rejected at push time**, and the full set is ≈ 1.66 GB. Move these to LFS or object
storage before the batch, or the run will fail at the commit step rather than the pipeline step.

---

## 4. Corrections to the prior report

Self-review, so the record stays usable:

1. **Overstated:** the feared 2020–2021 metrics coverage cliff. The canary shows real, dense,
   varying metrics from the first exported bar (§2.4). The blocker was correctly raised as a
   *risk requiring measurement* and is now bounded to 160 bars.
2. **Withdrawn (unchanged):** the `basis_identity` sub-dollar tolerance concern — 0 violations at
   1e-4, 0.085 and 30,000 once the pipeline's rounding order is respected.
3. **Still open from last time, unchanged:** `liq_source` provenance; USDC level-shift disclosure
   (now additionally implicated in A1); `is_synthetic` conflating downtime with quiet bars; the
   200-gap REST-repair cap; the 18-asset `verification_report.json` coverage gap (it is now 1 of 18
   by design, since only BTC has been regenerated).

---

## 5. Recommendation

**Not certified for `--all-symbols` with OI/positioning features enabled. Certified for everything
else, and the remaining work is small and precisely scoped.**

The core is now demonstrably sound on real data: causal kernels with zero prefix violations over
210,788 bars, verified warm-up seeding, an exact grid, honest 8-dp precision, and the stale-spot bug
fixed on the very bars that exposed it. Both prior blockers were addressed with real engineering
rather than paper, and the canary's manifest matches its bytes on all nine fields I checked.

Before the batch:

1. **Apply the A1 fix** (`.add(..., fill_value=0.0)`, bound the merge to post-floor rows, and
   `oi_coin > 0` in `available`) then **re-ingest BTCUSDT** — the canary must be regenerated after the
   fix, not merely re-verified, since the 160 bars are already in the shipped file. The same re-ingest must be checked against A1b, since the frozen ranges are upstream data and may re-arrive identical — if they do, the flag, not the fetch, is the deliverable. Add the
   `open_interest_k == 0 && metrics_available == 1` rejection to Agent 2.
2. **Fix A1b by giving each metrics column its own staleness state** (per-column run-length mask above, plus the Agent-2 rejection rule). This is the change that makes the manifest's availability fraction meaningful; nothing else in the pipeline can express it. Then re-derive 2022 and, for any strategy already trained on the top-trader family, treat 2022Q1–Q4 as suspect.
3. **Close A2/A3 at the source:** build `is_imputed_metrics` from the ten per-column imputations
   (or a bitmask), and replace the year-granularity scan with a run-length scan (`max run of constant
   values >= 100 bars`), which catches T1 and T2. Keep `audit_probe_metrics_validity` in the checklist.
4. **Uncap `Retry-After`** (A5) and set `min_interval ≈ 0.05 s` before an 18-asset cold run.
5. **Move the Parquet out of Git** (A8) before the run produces files you cannot push.
6. Then run, per symbol, and gate each asset on *both* the council and the OI validity probe:

```bash
python3 -m Engine.run_historical_pipeline --all-symbols --start-date 2020-09-01 \
        --workers 16 --footprint-days 0 --force 2>&1 | tee logs/pipeline_$(date +%Y%m%d).log
python3 -m Engine.verification.verify_parquet_integrity Engine/binance_backtesting_data
python3 -m Engine.verification.audit_probe_metrics_validity Engine/binance_backtesting_data
```

Assets listed after 2020 (SUI, ARB, OP, APT) additionally require excluding the bars where
`is_warmup_converged == 0` — the flag now exists and is correct, so this is a one-line filter, not a
re-ingest. Expect `--footprint-days 0` to leave `fp_*` and both imbalance features informationless
(A6); if the strategy set trades them, budget tick archives separately rather than assuming the
batch will supply them.
