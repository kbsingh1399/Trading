# Certification Round 3 — A1 / A1b / A5 Mitigations and the BTCUSDT Re-Ingest

**Assessed tree:** `kbsingh1399/Trading@b344184` (`main`); code change in `e18c601`, data in the same commit
**Baseline document:** `docs/PIPELINE_REREVIEW_ADDENDUM.md` (findings A1, A1b, A2–A8)
**Date:** 2026-09-05

Method: `origin/main` fetched, Engine extracted **clean-room** (so nothing in my tree could bias the
result), then every claim checked against the shipped Parquet — including a **bar-by-bar diff of the
previous export against the new one**, which is the only test that distinguishes a real repair from a
relabelled one. No claim below is taken from the manifest; all were re-measured.

---

## 1. Verdict

> ### All three findings are genuinely closed. The pipeline is certified for the 18-asset batch run, subject to two pre-flight items.
>
> **A1 — CLOSED, and closed surgically.** The fix touched **exactly** the 160 bars I independently
> flagged: my impossible set 160, bars changed 160, intersection 160, **over-suppression 0**. Values are
> now a pure causal carry-forward (`new[i] == new[i-1]` on 160/160), exact-zero OI count went 67 → **0**,
> and — the number that matters — the **derived-feature contamination I measured last round collapsed
> from 100 artifacts out of 182 extreme events to 0 out of 2**. The new `oi_impossible_zero` council check
> is *live*, not decorative: it fires on an injected `open_interest_k == 0` with a correct
> bar/timestamp locator, stays silent when the condition is disclosed, and the fix does not regress the
> negative control. It is **hard-gated before export** (inside the council), so a bad asset cannot be written.
>
> **A1b — CLOSED as detection.** Quarantine coverage is **30,463 / 30,463** frozen bars; unflagged = 0.
> The extra 139 flagged bars reconcile exactly as the A1 episodes plus the 2024 outage
> (2021: 4, 2023: 5, 2024: 121 = 103 + 18, 2025: 9 — and 2022's 39 impossible bars are inside the
> frozen union). The tautology `is_imputed_metrics == (metrics_available == 0)` holds on all 210,792
> bars, and the manifest is now **honest about the cost** — `metrics_unavailable_fraction_by_year`
> reports `2022: 0.8656`, i.e. it no longer hides the quarantine behind a 0.0.
>
> **A5 — CLOSED.** Server `Retry-After` is honoured directly (30 → 30 s, 3600 → 3600 s), capped only at
> 7200 s, and the previous inflation of short waits (30 → 120 s) is gone. One residual, §4 R7.
>
> **What is not closed is not a defect in the data — it is the price of the single shared bit.** The
> quarantine marks `metrics_available = 0` across the frozen windows, but those windows are where
> **open interest was alive**: I measure **30,423 bars (14.43 % of the file, 99.4 % of everything now
> marked unavailable) where OI itself was valid and moving**. See §3 R1 — recoverable today, durable
> fix is one int8 column.

**Certified for `--all-symbols`, with the two pre-flight items in §5.** The remaining findings are
robustness and engineering-hygiene issues (R2–R8), none of which corrupts a file or misleads a
consumer who reads the flags — and, importantly, the flags now tell the truth.

---

## 2. Their claims, checked

| claim | verdict |
|---|---|
| `.add(fill_value=0.0)` keeps NaN + NaN = NaN | **CONFIRMED** — executed the exact block on a frame straddling the floor: `NaN+missing → NaN`, `300+missing → 300`, `NaN+5 → 5` |
| USDC addition bounded to `timestamp_ms >= USDC_METRICS_FLOOR` | **CONFIRMED** — pre-floor rows byte-identical to input; `_ms`/`_utc`/`USDC_METRICS_FLOOR` all resolve at that call site |
| `audit_probe_metrics_validity` → 0 impossible OI bars | **CONFIRMED**, exit 0 |
| all 30,463 frozen bars have `metrics_available=0`, `is_imputed_metrics=1` | **CONFIRMED** — and it is 30,463 ∪ 139 = 30,602 total |
| contract `is_imputed == (avail==0)` strictly preserved | **CONFIRMED** on all 210,792 bars |
| 0 nulls, 0 NaN, 72 canonical columns, first 62 == `LEGACY_COLUMNS` | **CONFIRMED** — names, order and dtypes |
| 210,792 candles / 2,710,633 rungs | **CONFIRMED**, and the +4 rows vs last round are a legitimate later ingest edge (end `16:45 → 17:45`, export `18:10:38`) — the grid stays exact: every step 900,000 ms, `close_time == open + 899,999`, 0 dups, span row count == actual |
| 4 probes exit 0 / 9 suites pass | **CONFIRMED** — validity 0, coverage 0, parity 0 (0 violations / 145 prefixes), offline suite 0 (9 PASS, 12.2 s) |
| Council ALL PASS, 0 findings | **CONFIRMED** (my own independent `run_council`: passed, 0 findings) |
| `_stale_runs_mask` "matches the exact detection contract of the audit probe" | **CONFIRMED** — I ran my *original, unmodified* gate and it finds the same 14 runs / 30,463 bars, reporting `metrics_available=1 on 0, is_imputed=1 on 9,819` |

**Zero-lookahead, re-derived on the new file.** Correct method (recompute the kernel on the full series
and on each truncation; they must agree on the overlap — comparing to the *stored* column instead is
meaningless because the pipeline is seeded 23,520 bars earlier):

`ema_8` · `ema_200` · `ema_800` · `volume_sma9` · `atr_100` → **0 violations / 16 truncations**
(worst |Δ| = 0.00e+00); `rsi_14` → **0 violations / 6**. §1.3 stale-spot guard re-checked on the new
file: 93 `UNAVAILABLE` spot bars, **0** stale non-zero deltas; `basis_usd ≡ close − spot_close` to
1.34e-11. Ladder: exactly 1 POC per candle, 0 duplicate `(ts, price_bin)`, 100 % master coverage,
volume conservation `0.000000`.

---

## 3. Independent adversarial pass on the new quarantine

I pushed staleness patterns **through the real `process_master_dataset`** (9,000 bars) and measured how
much of each poisoned window the quarantine actually claims:

| injected defect | flagged inside window | verdict |
|---|---|---|
| **T1** L/S family entirely absent for 6 months *inside* 2021 (last round: 17,376 fabricated bars, **accepted**) | **6,300 / 6,300 (100 %)** | **CLOSED** |
| **T2** frozen values arriving in *fresh* timestamped rows — the actual 2022 shape | **6,300 / 6,300 (100 %)** | **CLOSED** |
| **T3** frozen + 1e-6 jitter every 200 bars | 0 / 6,300 (0 %) | not detected |
| **T4** stale in 287-bar blocks separated by one differing bar | 0 / 6,300 (0 %) | not detected |
| **T5** monotone 1e-9 drift, never exactly equal | 0 / 6,300 (0 %) | not detected |
| **T6** 30 literal `open_interest_k = 0.0` bars | 30 / 30 flagged | **CLOSED** |

Both bypasses I published last round are now closed at the source, and the OI path is closed too.
T3–T5 are the honest boundary of this technique: detection is *exact bit-equality over ≥ 288 bars*, so
anything that jitters, or that alternates at a period below the threshold, is invisible. I checked
whether real archives do this — **no evidence they do**: the actual BTC 2022 runs are bit-identical for
thousands of bars, which is precisely why value-constancy works here. So this is a robustness limit to
document, not a live hole. (I also looked for a better detector and rejected it: per-column
`_age_ms` staleness — already computed and unused for the ratio columns — cannot see this case either,
because the rows really are fresh; only their *values* are dead.)

---

## 4. Residual findings

**R1 — MEDIUM/HIGH (usability, not correctness): 30,423 bars of valid OI discarded by the shared bit.**
`metrics_available` is one column describing six, so quarantining frozen *ratios* also declares
*open interest* unavailable — 99.4 % of the newly-flagged population, 14.43 % of the file, concentrated
in 2022 (30,289 of 30,423). Verified: inside that set OI changes on 99.7 % of bars and is non-zero.
This is the A2 architecture point cashing in: with one bit, the fix had to choose between lying about
staleness (last round) and destroying good OI (this round). Durable fix, ~0 bytes of storage:

```python
out["oi_available"]        = (available).astype(np.int8)        # OI truth, unchanged by ratio state
out["positioning_available"] = (available & ~frozen_mask).astype(np.int8)
out["metrics_available"]   = out["positioning_available"]        # keep legacy bit as the AND
```
until then, the documented recovery rule for OI work on this file is
`is_imputed_metrics == 0 | (metrics_available == 0 & ~frozen_union)` — i.e. do **not** drop all 30,602
bars when the task only consumes `open_interest_k` / `oi_change_pct`.

**R2 — MEDIUM: the flag is retrospective; it must never be a feature.** `_stale_runs_mask` marks a run
only once it is known to reach 288 bars, so a bar's flag depends on up to 288 *future* bars. Measured:
truncating the same series at +100 and +287 bars into a run yields **different flags on the identical
prefix** (0 vs 100, 0 vs 287), agreeing only at ≥ 288. That is fine as a provenance annotation and fine
for sample selection, but as a *signal* it leaks the future ("the ratio will still be dead in 3 days").
The docstring should say so, and the schema comment for `is_imputed_metrics` should carry it.

**R3 — LOW/MEDIUM: one genuine (if bounded) causality violation in code whose contract is "strictly
causal".** `causal_med = s_raw.rolling(201, min_periods=20).median().bfill()` — the `.bfill()` back-fills
bars 0–18 from a median computed at bar ~19. Verified harmless on this export (all head bars are
available, and for post-2020 assets those bars sit inside `is_warmup_converged == 0` anyway), but
`bfill` in a causal path is a latent trap for a thinly-traded first day. Use the NaN as-is
(`NaN` ⇒ not impossible), or `.ffill()`-only.

**R4 — MEDIUM: no regression test for any of it.** `test_pipeline_offline.py` is **unchanged** in this
commit — zero matches for `_stale_runs_mask`, `STALE_RUN_BARS`, `oi_impossible_zero`, `is_impossible`.
Three non-trivial invariants (exact-set match with the probe, the tautology, "pre-floor rows untouched")
are protected only by the canary happening to be clean. A 20-line synthetic test — inject a 400-bar
frozen run, assert `is_imputed_metrics == 1` across exactly those bars; inject a zero-OI episode, assert
`oi_impossible_zero` fires — would lock all three.

**R5 — LOW: the coverage probe still proves a weaker statement than it appears to.** Its fixture is
still `METRICS_FRACTION = 0.60` of a series that starts 2020-09-01, i.e. the gap aligns with whole
calendar years, which is exactly the case the year-granular `regime_dead_feature` scan can see. It exits
0 for the right reason, but it is a regression test for year-aligned gaps only; the sub-year shapes it
cannot see are now handled upstream by R1's mask, so keep both.

**R6 — LOW/MEDIUM: the batch gate is soft and fail-open.** In `run_pipeline` the validity probe runs
*after* `exporter.write_manifest`, so an asset with unflagged frozen runs is still written (and would
still be committed) with only a `[WARNING]` and exit code. A1 is properly hard-gated inside the council;
A1b is not. And the block is wrapped in a blanket `except Exception: log("[WARN] could not run ...")`,
so if `check_symbol` raises for some asset — e.g. a file lacking `taker_volume_ratio`, which
`check_symbol` requires — **the gate silently reports nothing and the run proceeds**. Narrow the catch
to `FileNotFoundError` and treat any other exception as a failure.

**R7 — LOW: `Retry-After` is now honoured without a floor.** `min(server_cool, 7200.0)` fixes the
truncation, but a misconfigured proxy sending `Retry-After: 1` now yields a 1-second poll loop — last
round's `ban_cooldown` floor protected against that direction too. Prefer
`cool = min(max(server_cool, 5.0), 7200.0)`. `min_interval` still defaults to `0.0`, so an 18-asset cold
run remains unpaced and purely reactive; 18 assets × `--workers` on shared IP weight is the main
ban driver, and a `FetchError` after exhausted retries still yields a `None` month → flat synthetic
bars, which the council permits.

**R8 — UNCHANGED operational blocker: 94.17 MB in Git.** The re-ingest grew the master to 98,742,751 B;
headroom to GitHub's 100 MB hard limit is **5.83 MB (6.2 %)** and 18 assets extrapolate to **≈1.66 GB**.
The canary fits; several of the 17 others (any asset whose masters are 6 % larger, and every high-tick
ladder) will be **rejected at push time**, after hours of fetch work. Solve storage *before* the batch,
not after.

**Deliberately not reported, checked and cleared:** the value-area step looked pathological in my
harness (0.26 s/bar) — that was my own artifact, pairing $11,000 prices with `get_merge_level` fallback
0.0001 → 1.1e8 bins; measured realistically it is **1.4 s for a full 210,792-bar BTC export**, and even
the four assets on the fallback bucket (XRP, DOGE, ADA, TRX) cost **0.5–2.8 s**, so bucket selection is
not a batch risk. Also unchanged and expected: `fp_delta == future_cvd_15m` bitwise, `fp_poc ==
(h+l+2c)/4`, ladder 100 % synthetic (`--footprint-days 0`), and the `funding_rate_pct` 0.01
sentinel/default collision.

---

## 5. Recommendation

**Certified for the full 18-asset `--all-symbols` batch run**, with two pre-flight items and one
per-asset acceptance rule.

Pre-flight (both cheap, both before spending hours on fetches):
1. **Move Parquet out of Git** (R8) — LFS or object storage. Without this the batch fails at the commit,
   not the pipeline, and you lose the run.
2. **Make the batch gate fail-closed** (R6) — run the validity probe *before* `write_manifest`, and stop
   swallowing every exception.

Then, per asset, accept only if all of these hold:

```bash
python3 -m Engine.run_historical_pipeline --all-symbols --start-date 2020-09-01 \
        --workers 16 --footprint-days 0 --force 2>&1 | tee logs/pipeline_$(date +%Y%m%d).log
python3 -m Engine.verification.verify_parquet_integrity  Engine/binance_backtesting_data
python3 -m Engine.verification.audit_probe_metrics_validity Engine/binance_backtesting_data
```

* council `passed: true` **and** validity probe exit 0 for that asset;
* `min_interval` set to ≈ 0.05 s and `--workers` conservative for the first pass across 18 symbols (R7);
* `metrics_unavailable_fraction_by_year` read per asset, not assumed — for the four late-listed assets
  (SUI, ARB, OP, APT) exclude `is_warmup_converged == 0` bars, and expect a large unavailable fraction
  wherever the archive is genuinely sparse (a 2022-like 0.87 is now *visible*, which is the point);
* per-symbol metrics archive start dates are still unverifiable from this sandbox (no
  `data.binance.vision` egress), so treat each asset's first-year metrics density as unproven until its
  own manifest is inspected. This is the one thing that keeps the batch "certified to run" rather than
  "certified to trust blindly".

Consumer guidance for this canary, to be pasted into the dataset README: filter `is_imputed_metrics == 0`
for anything touching `ls_ratio_*`, `top_account_ratio`, `whale_index`, `taker_volume_ratio`; for OI-only
work you may retain the 30,423 collateral bars in 2022 (R1); and never promote
`metrics_available` / `is_imputed_metrics` into a feature — they are retrospective (R2).

After the batch, the two follow-ups worth doing are R1 (per-column availability bits — it converts a
14.43 % data loss into nothing) and R4 (the synthetic regression tests).
