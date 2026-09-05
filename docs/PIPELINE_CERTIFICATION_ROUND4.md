# Round 4 — Council Schema Calibration for Multi-Asset Coverage (ETHUSDT [2/18])

**Verifier:** Arena.ai Agent Mode, offline analysis of `kbsingh1399/Trading`
**Tree verified against:** `origin/main @ 9a33c23` (BTCUSDT [1/18] certified tree)
**Prompt answered:** `docs/prompts/ARENA_MULTI_ASSET_SCHEMA_CALIBRATION_PROMPT.md`
**Delivered as:** branch `arena/01a07263-trading` (patch `a83d022` + this doc), merged by you into `main @ 2241bbb`,
whose history was then re-initialised as a single squashed commit — the SHAs above no longer resolve, the content does
**Ground truth available here:** the real `BTCUSDT_15m_master_2020_2026.parquet` (210,792 bars, 98.7 MB).
No ETHUSDT artifact of any kind is in the repo — parquets were de-tracked in `b836aa0` — so every ETH
number below is either reproduced by construction from your log, or measured on BTCUSDT and labelled.

---

## 1. Verdict on the two proposed calibrations

| # | Your root cause | Verdict | Your proposed patch |
|---|---|---|---|
| A | `regime_dead_feature` year scan is unconditioned on `metrics_available`, so a legitimately pre-archive year reads as a frozen regime | **CONFIRMED — correct verbatim** | **Direction right, but unsafe as written.** Needs 3 amendments (§3) |
| B | `precision_collapse` compares a bounded cointegrated spread to `close_nu * 0.01` — a category error | **CONFIRMED** | **Rejected as written.** Absolute floors don't work; replaced with a collapse test (§4) |

### Code confirmation (Finding A)
`Engine/verification/verify_parquet_integrity.py` L403–415, as it stands at `9a33c23`:

```python
y_mask = (years == y)
if y_mask.sum() >= 500:                                   # <- calendar-year bar count only
    y_nu = master.loc[y_mask, col].nunique()              # <- not conditioned on availability
    total_nu = master[col].nunique()
    if y_nu <= 1 and total_nu > 1:                        # fires on any 100%-absent year
```

`metrics_available` appears nowhere in this block. Therefore **every** symbol in
`Engine/core/schema.SYMBOLS` whose USDⓈ-M metrics archive begins after the export window is
rejected deterministically — this is not ETH-specific and it will recur on most of the remaining
16 assets (any listing after 2020-09, e.g. the OP/APT/SUI/ARB class already known to have zero
warm-up history at the head). Fixing it is required, not optional, for `--all-symbols` to ever finish.

### Measurement (Finding B)
The test compares two quantities that have no common unit. `basis_usd` distinct values ≈
`(ask_band − bid_band) / tick`, independent of how many distinct prices `close` takes.

| file | distinct `close` | rule threshold (1 %) | distinct `basis_usd` | outcome |
|---|---|---|---|---|
| BTCUSDT (real, measured here) | 187,272 | 1,872.7 | **17,055** (9.11 % of close) | passes |
| ETHUSDT (your log) | 148,108 | 1,481.1 | **1,428** (0.964 % of close) | **rejected by 3.58 %** |

The ETH verdict flipped on a **3.6 % margin below an arbitrary cliff** that measures nothing about
data integrity — it measures the asset's tick size relative to its price range. Two further BTCUSDT
facts show why the test could never be about precision: a healthy spread concentrates nowhere —
modal-value share is 0.0598 % — and `basis == 0` occurs on 27 bars (0.0128 %), which is *fewer* than
the 93 bars whose spot source is `UNAVAILABLE`, so a zero count is not even a clean proxy for a
missing spot. Any rule keyed on "how many distinct values" or "how many zeros" is measuring the asset,
not the pipeline.

**Your floor of ≥ 100 distinct values is not safe either.** It passes everywhere, including on
broken data — BTCUSDT's tightest year is 2022 with 3,681 distinct `basis_usd`, so no plausible
absolute floor separates a healthy asset from a frozen one. The bug this rule is supposed to catch is
`spot_close` fabricated as `close` ⇒ `basis_usd ≡ 0`, which is a *collapse*, not a low cardinality.
That is what the shipped patch tests (§4).

---

## 2. Two premises in your prompt that do not hold — please re-check before integrating

1. **"The precision_collapse fix for `ema_8`/`atr_14`/`session_vah` was already committed in `c0a62e5`."**
   `git diff --stat b344184..origin/main -- Engine/verification/verify_parquet_integrity.py` is **empty**:
   `c0a62e5` touched the processor, `http_client.py`, `run_historical_pipeline.py` and
   `test_pipeline_offline.py` — never the verifier. Both the `ema_8/atr_14/basis_usd` loop and the
   `session_vah` range/bucket rule come from the **initial commit `161ef7f`**. So: no partial fix exists,
   and `basis_usd` was never separately broken — it is on the original rule. (Your other four
   round-3 items **did** land and are correct: R3 `.ffill()` + `isnan`/`>1000` guard, R6 fail-closed
   audit with `run_audit=True` for `--all-symbols`, R7 `min_interval=0.05` and
   `cool = min(max(server_cool, 5.0), 7200.0)`.)
2. **The manifest fields you quoted as corroboration do not exist.**
   `write_manifest` emits `metrics_unavailable_fraction_by_year` (real — I confirmed it is computed on
   the master grid per calendar year, so your `{"2020": 1.0000}` is a trustworthy *coverage* figure),
   plus counts of tick/spot-exact and synthetic bars. It does **not** emit `metrics_start_date` or
   `spot_source_coverage`. If those two lines came from a manifest, something else wrote them; if they
   came from a paraphrase, they must not be treated as evidence in a calibration decision. This matters
   because the only honest anchor for "was it absent at the source?" is a *new* field (§3) — which is
   also what my patch adds.

At the time of writing, that ETH metrics begin 2021-12-01 was **not checkable from this sandbox** (no
egress to `data.binance.vision`, no committed ETH artifact): Binance documents only
`klines`/`aggTrades`/`trades` retention, not per-symbol metrics coverage, so Finding A was recorded as
"correct diagnosis of the code defect, plausible coverage premise" — and the patch was deliberately
built so the calibration **does not depend on the exact date**. §8 closes that caveat: the field my own
patch introduced now corroborates the premise independently, on the real asset.

---

## 3. Finding A — what shipped, and why your version as written is unsafe

Your patch conditions both masks on `metrics_available == 1`. That kills the false positive, and it is
necessary. It is not sufficient, for one reason:

> **`metrics_available` is the field the scan exists to audit.** Conditioning the audit on it makes the
> §4.1 defect class unfalsifiable: any region the pipeline fabricates *and* marks unavailable now passes
> silently. That is not hypothetical — it is exactly what `Engine/verification/audit_probe_metrics_coverage.py`
> is built from: a head whose metrics rows are absent, filled with the documented fallbacks, marked
> `metrics_available = 0`. It is *value-for-value identical* to ETHUSDT's legitimate 2020. No rule that
> reads only the export (values, flags, prefix-vs-interior) can separate them.

Empirically confirmed here, A/B on your own probe:

| verifier | probe exit | council |
|---|---|---|
| `9a33c23` (pre-patch) | **0** | `Agent3:Schema: FAIL (6)` → "fix verified in place" |
| your proposed patch (avail-conditioned only) | **1** | `Agent3:Schema: PASS` → **"BLIND SPOT REPRODUCED"** |
| shipped patch | **0** | `Agent3:Schema: FAIL (1)`, precise: `metrics_coverage_unattested` |

I hit this with the availability-conditioned version first and wrote it up here because it is the one
thing that would have been lost in review: had you integrated your snippet as proposed, the change would
have looked like a clean 4-line win, the §4.1 gate would have gone red for a reason nobody would have
connected to it, and the tempting repair would have been to edit the probe.

**Fix: move the exemption off the export and onto the download inventory.**
`HistoricalDataFetcher._cached()` returns `None` *only* when the archive object does not exist on the
host — an observation about Binance, never derived from the assembled frame. A parse bug, a join bug or
a dropped month produces an empty frame, not a `None`, so it cannot attest itself. The patch threads that
inventory to the council:

1. `binance_historical_fetcher.py` — `fetch_metrics` records `metrics_absent_days` (days whose archive
   returned `None`), one log line.
2. `parquet_exporter.py` / `run_historical_pipeline.py` — manifest gains
   `provenance.metrics_archive_absent_months` (month-normalised).
3. `verify_parquet_integrity.py` — the year scan judges `avail == 1` bars with the denominator over the
   same subset; a year with `< 500` available bars is exempt **iff every month of it in the file span is
   attested**, else `metrics_coverage_unattested`. No manifest field ⇒ no exemption (fail-closed).

Amendments of mine that your snippet lacked, both required:

* **`metrics_interior_hole`** (new finding): a run of `> 28 days` of bars with no metrics content
  (`avail == 0` **and** `open_interest_k == 0`, i.e. the fallback signature — not merely flagged) that the
  source did not attest, rejected wherever it sits. This is the non-circular complement to the exemption:
  it is why an interior hole from a failed month cannot pass just because it was honestly marked. It
  **cannot** fire on the certified BTCUSDT 2022 quarantine, because quarantined bars keep live open
  interest (4,711 of 35,040 bars in 2022 carry metrics ⇒ the year is judged normally, exactly as before).
* **Skipped years must be reported, not silently passed.** `Finding` has no severity field (any finding
  rejects), so a soft note cannot live inside `agent_schema`. It is exposed as
  `metrics_coverage_report(master)` → `skipped_years`, `unavailable_prefix_bars`,
  `longest_interior_hole_bars`, `metrics_first_available_utc`, so "0 findings" is never mistaken for
  "nothing was skipped".
* **The §4.1 class is not weakened.** Fabricated sentinels with `metrics_available = 1` still fail:
  6 × `regime_dead_feature` + `oi_impossible_zero` in Agent 4, asserted in both directions by
  `Engine/verification/test_schema_calibration.py` (18 assertions).

---

## 4. Finding B — what shipped

`ema_8` / `atr_14` keep the close-cardinality rule (they are float recursions that inherit `close`
cardinality, so the ratio is meaningful for them). `basis_usd` leaves that rule and gains a collapse test:

```python
vc = pd.Series(np.round(master["basis_usd"].to_numpy(np.float64), 8)).value_counts()
mode_share = float(vc.iloc[0]) / len(bser)
if len(vc) < BASIS_MIN_DISTINCT or mode_share >= BASIS_MODAL_SHARE_MAX:   # <20 distinct, or >=98% on one value
    out.append(Finding(A, "precision_collapse", f"basis_usd collapsed: ..."))
```

* ETHUSDT (1,428 distinct, real spread) → **accepted**.
* `basis_usd ≡ 0` from a fabricated spot join → **rejected** (verified).
* A 2022-style *near*-freeze where 90 % of bars share one value → now **caught**, whereas the old rule
  would have passed it (90 % of 35,040 bars still leaves thousands of distinct values). This is a net
  strengthening, not just a relaxation — the direction your floor-based version could not go.

---

## 5. How to unblock [2/18] — and what to expect on [3/18]…[18/18]

Pull the branch and re-run **only** ETHUSDT. **`--clean-cache` is not needed and costs you the run:**
for days whose archive does not exist nothing is cached, so a warm-cache run still re-observes every 404
and rebuilds the attestation, while 404s latch in `HttpClient._global_not_found` and cost one pass.

```bash
git merge arena/01a07263-trading            # or cherry-pick a83d022
python3 Engine/run_historical_pipeline.py --symbol ETHUSDT --start-date 2020-09-01 --workers 16
python3 Engine/verification/test_schema_calibration.py     # auto-upgrades to the real ETHUSDT parquet
python3 Engine/verification/audit_probe_metrics_coverage.py
python3 Engine/verification/verify_parquet_integrity.py --dir Engine/binance_backtesting_data
```

Expected: `[FETCHER] ETHUSDT: metrics archive absent for ~450 day(s) (2020-09-01 .. 2021-11-30)`, then
`Agent3:Schema: PASS`. The manifest must carry `provenance.metrics_archive_absent_months` non-empty — if
it is `[]` while 2020 has zero available bars, **do not** relax the check: that means the metrics months
did *download* and were lost downstream, i.e. the defect you suspected, and `metrics_coverage_unattested`
is the correct verdict.

For the remaining 16 assets: any symbol listed after 2020-09 takes the same path, no per-symbol tuning
needed. Where a symbol's history genuinely starts late, consider `--start-date` at its listing date — it
cuts wall time and avoids a head of absent months in every downstream join. Two things my patch does
**not** cover, so watch for them:

* **Sub-month holes** (a few days of fallback constants inside an otherwise healthy year) stay invisible
  to the year scan by design; `is_imputed_metrics` filtering is still the consumer-side defence, and
  `_stale_runs_mask` catches frozen ranges where the tape is live.
* **Pre-listing heads** (no klines at all, not just no metrics) fail in Agent 1 continuity, not here.

---

## 6. Answer to your third question

**No. This environment cannot run the 18-symbol download — it must run on your machine.**
Re-tested immediately before writing this, all three hosts fail at the TLS handshake
(`curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL` for `data.binance.vision`, `fapi.binance.com`,
`api.binance.futures.binance.com`). GitHub and PyPI are reachable, so this is a Binance-specific
egress block, not a general outage. Consequences, precisely scoped:

* I cannot fetch, cannot reproduce your `[2/18]` run, cannot confirm the ETH metrics start date, and
  cannot attest anything about per-symbol coverage — hence the design in §3, which moves that judgement
  to *your* HTTP layer instead of mine.
* The fetcher/exporter half of the patch is therefore the only part **not** exercised against live
  Binance here: it is covered by `test_pipeline_offline.py`'s mock-server test, which does produce
  404s (`not_found: 1`) and passes, but the first real `metrics_archive_absent_months` write is yours.
* What I *can* and did run offline on the patched `9a33c23` tree: `test_pipeline_offline.py` (ALL TESTS
  PASSED, 18.3 s), `audit_probe_metrics_coverage.py` (exit 0), `audit_probe_metrics_validity.py`
  (exit 0), `test_schema_calibration.py` (18/18 against the real 210,792-bar BTCUSDT export).
* After the batch, per-symbol claims are unverifiable here unless you commit the small artifacts: the
  two JSONs per symbol are enough for the coverage/attestation checks (`metrics_archive_absent_months`,
  `metrics_unavailable_fraction_by_year`) without the 100 MB parquets.

## 7. Residual items carried forward

* **R5 (open, unchanged):** `audit_probe_metrics_coverage.py` still asserts on a year-aligned
  `METRICS_FRACTION = 0.60` while the pipeline records month-aligned availability. My patch adds
  month-granular attestation; the probe's own threshold should follow it.
* **New, minor:** `_attested_absent_months` resolves the manifest via the module-level `DEFAULT_TARGET`,
  so `verify_symbol(target_dir=...)` on a non-default directory cannot see a sibling manifest and will
  fail closed (safe, but it will look like a false positive if you verify a copied tree in isolation).
  Thread `target_dir` into `agent_schema` if that workflow matters.
* **Unchanged from round 3, still your decision:** R1 (shared bit-discards 30,423 valid-OI bars),
  R2 (`_stale_runs_mask` is retrospective — never consume it as a feature), and the standing consumer
  rule: filter `is_imputed_metrics == 0` for ratio features.

**Standing verdict, restated for the multi-asset case:** *certified to run, not certified to trust
blindly.* The council now has the right question to ask when coverage is missing ("does the source attest
this gap?") instead of the wrong one ("is this column constant this year?").

---

## 8. Post-merge verification against the real ETHUSDT export

After the batch landed, `Engine/binance_backtesting_data/ETHUSDT_dataset_manifest.json` is committed, so
Finding A's premise — the one thing §2 had to leave as an assumption — is now measurable rather than
argued. 210,800 bars, `2020-09-01 → 2026-09-05`, council `Agent1/2/3 = PASS`, `verification.passed = true`:

| field (ETHUSDT, real) | value | reading |
|---|---|---|
| `provenance.metrics_archive_absent_months` | `2020-09 … 2021-11` + `2026-09` | **confirms the premise**: 15 contiguous months of genuine 404s, i.e. Vision's ETH metrics really do begin 2021-12-01; the trailing `2026-09` is the not-yet-published current month, correctly attested rather than rejected |
| `metrics_unavailable_fraction_by_year` | 2020 **1.0000**, 2021 0.9189, 2022 0.8656, 2023 0.0001, 2024 0.0009, 2025 0.0002, 2026 0.0 | 2020 is skipped (attested); **2021 is not** — ≈2.8 k available bars clear the 500 floor, so it is judged normally. A year-level patch that exempted "mostly absent" years instead of "unattested" years would have hidden 2021's partial data |
| `metrics_available_bars` / `imputed_metrics_bars` | 136,516 / 74,284 (35.2 %) | the honest figure the exemption trades a rejection for; consumers must filter `is_imputed_metrics == 0` |

Your integration is correct in the places where it could have gone wrong:

* `run_council(..., attested_months=...)` now receives the inventory **in-process** from
  `fetcher.metrics_absent_days` (and is re-used after each `causal_repair` round), which is strictly better
  than reading it back out of the manifest — and it retires the `DEFAULT_TARGET` residual in §7. The
  `hasattr(...) and fetcher.metrics_absent_days` guard means a run with no inventory falls back to
  `None` → manifest → **fail closed**, so caching can never manufacture an exemption.
* `oi_impossible_zero` is untouched (`avail == 1` **and** `open_interest_k == 0`), so the A1 hard gate
  still does not consult `is_imputed_metrics`. `audit_probe_metrics_validity` now reporting
  "pre-archive zero OI bars quarantined (`is_imputed=1`)" as accepted is therefore safe *only because*
  the council still rejects an unattested gap of that shape — the probe alone would accept a failed
  interior download that the pipeline marked honestly. Keep the probe behind the council, not beside it.

One number to notice, because it is data for **R1** rather than a new defect: ETH's 2022 unavailability
is **0.8656 — the same value as BTCUSDT's** (4 d.p., ~30.4 k of 35,040 bars). Two independent assets
losing the same bars to the same day-granularity is what the shared staleness bit looks like from the
outside. Per-column bits (R1) would decorrelate them; until then, any 2022 cross-symbol study on these
files is comparing one quarantine to itself.

Not re-run here: this sandbox arrived with the repo and no Python environment (`import numpy` fails), so
the offline suites could not be executed against the merged tree — this section is inspection plus your
committed artifacts. On my side the last green state was `test_pipeline_offline` (ALL TESTS PASSED),
`audit_probe_metrics_coverage` (exit 0), `audit_probe_metrics_validity` (exit 0),
`test_schema_calibration` (18/18), all on `9a33c23` + the patch. Worth one clean run of
`test_schema_calibration.py` on your machine, where the real ETHUSDT parquet now makes case 2 assert
directly on ETH rather than on the emulation.
