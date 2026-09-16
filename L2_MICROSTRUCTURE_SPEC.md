# L2 Microstructure Architecture — Specification

**Branch:** `arena/01a0a5bf-trading` · Companion to `DATA_EXPANSION_BLUEPRINT.md`

---

## 0. What we are actually building, and why

Two findings from the 18-symbol run define the target precisely:

1. **Every tail event is S1.** 15/15 of the worst trades on the 18-symbol
   ledger, 12/12 on the 11-symbol ledger, **zero T1 in either**. `strat==S1`
   scores 20.29× at p<0.0001 on the CVaR harness; `strat==T1` scores exactly
   0.00×.
2. **The tail is not a volatility phenomenon.** Only 4 of the 15 worst trades
   have `vol_rank ≥ 0.88`; **10 sit at 0.52**. That is why the volatility gate
   collapsed from 4.82× (11 symbols) to 1.84×, p=0.127 (18 symbols). We were
   trying to catch the tail with the wrong variable.

Adverse selection is the right variable, and it lives in the order book at the
**moment of entry**. S1 enters at 15m bar boundaries; the question is whether
the book state in the seconds before that boundary predicts an immediate
adverse move. That is a trade-level question with thousands of observations,
not a macro-regime question with eight.

**Scope decision:** this is a specification, not an implementation. Nothing
here can be built or tested until L2 data exists.

---

## 1. Exactly what to acquire

### Streams (Binance USDT-M futures, per symbol)

| stream | fields | purpose |
|---|---|---|
| **`depth@100ms`** (diff. book) | `e, E, T, s, U, u, pu, b[[p,q]…], a[[p,q]…]` | The core dataset. Reconstructs the book; `U/u/pu` are the sequence numbers that make gaps detectable |
| **`bookTicker`** | `u, s, b, B, a, A, E, T` | Best bid/ask price + resting size. Cheap, and sufficient for spread and L1 imbalance |
| **`aggTrade`** | `a, p, q, f, l, T, m` | `m` = is-buyer-maker gives trade direction without guessing |
| `depth20@100ms` (snapshot) | top-20 levels | Optional cross-check on the reconstructed book |
| `markPrice` / `fundingRate` | mark, index, funding | Already have 15m aggregates; 1s marks let us detect basis dislocations |

`b`/`a` arrays are `[price, quantity]` string pairs. Quantities are in base
asset. **Do not parse them as floats until they are Decimal** — cumulative
rounding across millions of updates will corrupt the book.

### The non-negotiable correctness requirement

Order-book reconstruction must be **sequence-validated**. Binance's own rule:
the first event after a snapshot must satisfy `U <= lastUpdateId+1 <= u`; every
subsequent event must have `pu == previous u` (futures) or `U == previous u+1`
(spot). On any violation: discard the book, re-fetch a snapshot, and **record
the gap**. A silently gapped book fabricates depth, and fabricated depth
produces exactly the fantasy-PnL error we spent three phases removing.

Every gap must be written to a sidecar log with symbol, timestamp, expected
sequence, received sequence. If a symbol's gap rate exceeds a threshold the
build fails rather than degrading quietly.

### Coverage

| source | depth | verified availability |
|---|---|---|
| Binance whitelist API | `S_Depth` snapshots (BTC only), `T_Depth` tick (all symbols) | **from January 2020**, requires a whitelisted futures account |
| Tardis.dev | `incremental_book_L2` | BTCUSDT spot from **2019-12-01**, paid |
| Bybit public | L2, 200 levels | ~2+ years |
| `data.binance.vision` bookTicker | — | **stale since 2024 — do not build on this** |

**Recommendation: start with ONE symbol (BTCUSDT), one year, from the Binance
whitelist.** 18 symbols × 6 years of tick L2 is a petabyte-scale project. A
one-symbol one-year pilot answers the only question that matters — *does book
state at entry predict S1's tail?* — for roughly 1/100th of the cost.

Also worth doing first and free: the Rajendran & Singaravelu processed feature
CSV (1 year, Bybit BTC/USDT) reportedly attached to SSRN 6344338. **I have not
verified this myself** — it comes from a third-party forum post. If it exists it
is the fastest possible prototype, because the features are already computed.

---

## 2. Storage architecture

Raw tick L2 is the dominant cost. Order of magnitude, **as an estimate to be
measured, not a figure to budget from**: BTCUSDT `depth@100ms` is on the order
of hundreds of millions of messages per year; compressed columnar, that is
tens to low-hundreds of GB per symbol-year. 18 symbols × 6 years is therefore
plausibly 1–10 TB compressed, and an order of magnitude larger uncompressed.

```
l2/raw/{sym}/{stream}/{YYYY-MM-DD}.zst        immutable, hashed, append-only
l2/books/{sym}/{YYYY-MM-DD}/                  reconstructed snapshots, optional
l2/features/{sym}/micro_features_1s.parquet   the artefact the engine consumes
l2/features/{sym}/micro_features_15m.parquet  bar-aligned rollup
l2/logs/gaps_{sym}.jsonl                      every sequence discontinuity
l2/manifest/{sym}.json                        per-file hashes, coverage, gap rate
```

Two hard rules:

1. **The engine never reads raw L2.** It reads `micro_features_15m.parquet`,
   which is small, schema-stable and joins to the existing master by
   `open_time_ms`. This keeps backtests fast and reproducible and means a raw
   re-download cannot silently change a published number.
2. **Raw is retained, features are rebuildable.** Feature definitions will
   change; raw must survive so features can be recomputed.

Practical compromise for the pilot: store 1-second **snapshots** (top 20 levels
+ best bid/ask + trade aggregates) rather than every delta. That is ~86,400
rows/day/symbol — trivially small — and captures everything Rajendran's 21
features need. Retain raw deltas only for the pilot window so the snapshot
pipeline can be audited against them.

---

## 3. Feature derivation

Mapping onto the 21 features in Rajendran & Singaravelu, marking what becomes
available that we do not have today:

| group | features | status today | with L2 |
|---|---|---|---|
| **Spread state** | `ob_spread`, `ob_spread_pct`, `ob_spread_z_30`, `ob_thin_book_flag` | **absent** | ✅ from `bookTicker` |
| **Order flow imbalance** | `ob_imbalance_l1`, `ob_ofi_proxy`, `ob_ofi_z_30` | **absent** (our CVD is *trade* imbalance, not *quote* imbalance) | ✅ from depth deltas |
| **Passive retreat** | `ob_net_passive_z_30`, `ob_upd_imb` | **absent** | ✅ from add/cancel events |
| Volatility | `ob_rv_30`, `ob_impact_pressure` | rv yes at 15m; impact_pressure no | ✅ both |
| Trade flow | `tr_vol_imbalance_1s`, `tr_count_imbalance_1s`, `tr_tick_imbalance_1s`, `tr_flow_mean_30s`, `tr_flow_autocorr_30s`, `tr_rv_30s`, `tr_volume_z_30s` | ~5 of 7 at 15m | ✅ all 7 at 1s |
| Activity | `tr_log_volume`, `tr_log_trade_count`, `tr_no_trade_flag` | ✅ | ✅ |

The three groups we are missing are the three that carry the adverse-selection
information. That is the entire case for acquiring the data.

**The label.** Rajendran's `tox_A` marks seconds where strong directional flow
is followed by sustained price continuation over a 5-second horizon, with
adaptive rolling-quantile thresholds on a 1-hour lookback (regime-aware, so the
base rate does not drift with volatility). We should reproduce it exactly
rather than invent our own, so results are comparable to a published baseline.

**Honest expectation, from their paper:** at the 0.1% gate their precision is
**6.07%** and recall **1.99%** (F1 0.030), mean daily ROC-AUC 0.799. The value
is **tail concentration**, not classification accuracy. Their ablation also puts
the VPIN proxy at **0.30×, below random** — consistent with our own VPIN
falsification, so we should not expect a simple toxicity index to work.

---

## 4. Integration into the 15m/4h engine

### Join point

`micro_features_15m.parquet` carries one row per `(symbol, open_time_ms)`,
left-joined onto the existing 15m master. Because S1 enters at the *open* of a
bar, the features for bar *t* must be computed from data **strictly before**
`t` — i.e. from the seconds ending at the previous bar's close. This mirrors
the `avail_time = open + 4h` convention already used for the friction-stress
series, and must be enforced by the same kind of as-of join.

```python
# Engine/execution_costs.py already does this for the stress series:
#   _stress["avail_time"] = (time + 4h)            # indexed by bar CLOSE
#   pd.merge_asof(..., direction="backward")       # can only see completed bars
# The microstructure features use the identical pattern at 15m resolution.
```

### Two integration modes — build the veto first

**Mode A: hard entry veto (build this first).**

```
skip the S1 entry if toxicity_score(t) >= threshold
```

Reasons to start here:
- It is **interpretable** — one number, one threshold, one reason for each skip.
- It **does not require retraining**, so it cannot contaminate the model.
- It is **directly measurable** by the harness we already built: drop the
  vetoed trades, compute CVaR99 efficiency against a random equal-size control.
- It targets the tail specifically, which is where all the damage is.

**Mode B: model features (only after A is validated).** Add the book features
to the S1 LightGBM feature set and let the model learn the relationship. More
powerful but far less interpretable, and — critically — it interacts with the
cross-sectional training defect described in §5.

### Where it plugs in

`score_test_candidates` in `Engine/strategy/s1_dual_model_orderflow.py` already
receives a per-candidate DataFrame and applies threshold gating. The veto is a
boolean column on that frame, applied alongside — **penalty-only**, consistent
with the standing defensive-only rule. It can only remove entries, never add
them or lower a threshold.

---

## 5. A defect that must be fixed before Mode B

Found while running the 18-symbol expansion:

```python
train_set = all_data[train_mask]      # run_20_oos_dual_model.py:161
```

`all_data` is pooled across **every symbol**, so the model is trained
cross-sectionally. Adding 7 symbols moved the *original 11 symbols'* pooled PnL
by **+3,203.83** (from −2,734.21 to +469.62) while the new symbols themselves
contributed **−739.53**.

**The symbol universe is therefore a hyperparameter that silently rewrites every
historical result.** Consequences:

- The 11-symbol and 18-symbol baselines are **not comparable**, and the pooled
  "improvement" to −269.91 is a retraining artefact, not diversification.
- Any future feature addition (including Mode B) will retrain the shared model
  and change every symbol's history. We will not be able to attribute an
  improvement to the feature rather than to the retrain.

**Fix before Mode B:** either train per-symbol models, or freeze the universe
and treat any universe change as a new project with a fresh baseline. Mode A
(the veto) is immune to this because it does not touch the model — one more
reason to build it first.

---

## 6. Validation requirements

Every gate is a hard fail:

| gate | test |
|---|---|
| book integrity | sequence continuity; gap rate per symbol logged and bounded |
| book sanity | `best_bid < best_ask` on 100% of snapshots; quantities > 0; price within ±X% of last trade |
| reconstruction fidelity | reconstructed top-of-book matches `bookTicker` to the tick on ≥ 99.9% of snapshots |
| **no lookahead** | features for bar *t* recompute identically using only data `< t` |
| trade reconciliation | `aggTrade` volume matches the 15m master `volume_base` within tolerance |
| coverage | no missing days; gap days explicitly listed, never silently forward-filled |
| **label reproducibility** | our `tox_A` base rate matches the published rate on the same venue/period |
| **episode/day clustering** | standard errors clustered by day; report the effective n |
| **cost reconciliation** | realised bps still equals `ROUND_TRIP_BPS` |

### Statistical protocol

1. **Walk-forward exactly as published:** train on the 21 most recent days
   containing at least one positive label, predict the next day.
2. **Pre-register the threshold** before looking at any scorecard, as we did
   for the 3.0×/1.5× friction schedule.
3. **Score by CVaR99 efficiency vs a random equal-size control** using
   `Engine/strategy/cvar_gate_harness.py`. Never by PnL.
4. **Report the width sweep.** Their efficiency decays from 25.85× at a 0.1%
   gate to 3.50× at 5%; the signal is concentrated in the extreme tail, so the
   gate width is a first-order parameter, not a detail.
5. **Cluster by day.** Thousands of trades is *not* thousands of independent
   observations. With 360 test days the effective n for a daily-regime claim is
   ~360, and for a volatility-regime claim it is still ~8.
6. **Fix the holdout first.** `oos_windows_20_random.json` spans 2024-03 →
   2026-07, entirely inside the primary span 2021-05 → 2026-03, with two
   literally overlapping window pairs and 76 double-counted trades. A genuine
   holdout must be **temporally disjoint**. Until that is fixed, no
   "out-of-sample" claim in this repository is one.

---

## 7. Success criterion, stated in advance

The pilot succeeds if, on BTCUSDT alone, a pre-registered book-state veto
achieves **CVaR99 efficiency ≥ 2× at p < 0.05 against a random equal-size
control**, on trades clustered by day, and does so **consistently across at
least two disjoint time periods**.

If it does not clear that bar, we stop and do not scale to 18 symbols. The
vol_rank lesson is fresh: a pooled p=0.0098 evaporated to p=0.127 when the
universe changed. Anything we cannot reproduce across a universe or time split
is not a finding.

---

## 8. What I have not verified

- Binance L2 whitelist terms, current pricing, retention, and the
  January-2020 start date — sourced from a 2022 Stack Overflow answer.
- Whether the Rajendran & Singaravelu feature CSV is actually downloadable —
  a third-party forum claim about the SSRN listing.
- All storage size figures are order-of-magnitude estimates, not measurements.
- Whether Bybit or Tardis data is comparable to Binance for our symbols; books
  differ materially by venue, and a model trained on Bybit BTC may not
  transfer to Binance alt books.
- Whether adverse selection is predictable at **15m entry granularity**. The
  published work operates at 1-second resolution; aggregating to 15m destroyed
  VPIN, and it could destroy this too. **This is the single largest risk in the
  entire plan, and it is why the pilot must precede any large data purchase.**
