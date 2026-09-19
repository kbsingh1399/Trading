# Ox_Alpha_43 — Remediation Report

**Follow-up to:** `docs/audits/Ox_Alpha_43_Audit_Findings.md`
**Branch:** `arena/01a0ba30-trading`
**Date:** 2026-09-19

This documents the Section 9 remediation. Every number below was produced by
code committed in this branch and is reproducible from a clean clone.

---

## 1. Status of the nine required items

| # | Requirement | Status |
|---|---|---|
| 1 | Push the real commit; raw URLs resolve | **N/A** — `523fc0d` never existed. Work is on this branch; no fabricated SHA is cited. |
| 2 | Fix the `Optional` import; publish real test output | **Done** — 46 passed, 1 skipped. |
| 3 | Remove the shadowed `ASSET_BASKETS` | **Done** — defined once, 156 assets, pinned by test. |
| 4 | Replace the OOS-percentile threshold | **Done** — fitted on train only. |
| 5 | Reconcile Section 2 vs Section 3 PnL | **Withdrawn** — both tables irreproducible; replaced by a single scorecard. |
| 6 | Commit the Monte Carlo harness with seed | **Done** — real bootstrap, seeded, numba-parallel. |
| 7 | Wire the engine + cluster caps, or restate scope | **Done** — governance enforced in the sim loop; scope stated honestly. |
| 8 | Correct Section 5 to the shipped ratchet | **Partly** — see §5; prose claims remain unimplemented. |
| 9 | Re-mark W19 FAIL, restate scorecard | **Superseded** — whole scorecard regenerated. |

---

## 2. Defects fixed in existing code

**B2 — import crash.** `schema.py` used `Optional[str]` without importing it.
The module raised `NameError`, so `Engine.core` could not be imported at all and
the "26/26 PASS" was impossible. One-line fix.

**B3 — shadowed universe.** `ASSET_BASKETS` was bound at line 189 (27 symbols)
and again at line 250 (156 symbols). Python kept the second; the first was dead
config that would have flipped behaviour on any reorder. Removed, with
`test_asset_baskets_defined_once` asserting the source contains exactly one
binding.

**B4 — broken crypto symbol map.** `BINANCE_TO_MT5_MAP` emitted `DOGEUSD`,
`LINKUSD`, `AVAXUSD`, `NEARUSD` — none of which appear in the Crypto basket,
which uses the Blueberry tickers `DOGUSD`, `LNKUSD`, `AVXUSD`, `NERUSD`. On-disk
Binance history could therefore never be joined to the MT5 universe. Corrected;
`SUIUSDT/APTUSDT/OPUSDT/ARBUSDT` are deliberately left unmapped rather than
pointed at instruments the broker does not list. Resolvable universe: **98 → 112
of 156**.

**B11 — cluster governance.** Three divergent copies existed
(`forex_engine.py`, `live/order_manager.py`, `research/signal_auction.py`), none
imported by any backtest, and `CRYPTO_BLOC` existed nowhere despite being named
in the directive. Consolidated into `Engine/core/correlation_clusters.py`: 13
clusters covering all 156 assets, with unknown symbols degrading to singletons
rather than silently permitting unlimited correlated exposure.

---

## 3. Two further defects found while rebuilding

**B12 — `fastmath` NaN sentinel (silent data corruption).** The labelling kernel
used `outcome = np.nan` as "unresolved" and tested `np.isnan(outcome)`. Under
`@njit(fastmath=True)` the compiler may assume operands are never NaN and fold
that test to `False`, so time-stop exits leaked NaN payoffs into results —
**685 of 4,523 trades on BTCUSD alone (15%)**. Replaced with an explicit
`resolved` flag. This class of bug is invisible in aggregate statistics because
NaN silently propagates through `.mean()`.

**B13 — "15m" files are not 15m.** Files named `*_15m_real.parquet` begin with a
long **daily**-resolution prefix. EURUSD carries 4,961 daily rows before true
15m data starts at **2023-09-05**; the median asset has ~2,986 such rows.

This matters directly: **W01 starts 2023-09-15, and 43 of 98 forex assets have
no genuine 15m data until after that date.** Any bar-count rule — ATR windows,
the 24-bar time-decay exit, opening ranges — was being computed across a
resolution boundary. The harness now trims to the first sustained 15m run and
requires ≥4,000 bars.

---

## 4. Honest results

### 4.1 Baseline: momentum long, costs applied

`python3 -m Engine.validation.honest_walkforward --quick`

```
Universe        : 18 assets (6 per basket)
Raw base rate   : 23.78%   (breakeven at 2.5R needs 28.57%)
Raw expectancy  : -0.2076 R/trade
Windows PASS    : 0/20
Total           : 4,346 trades, -2,072.62 USD
```

**0/20, net negative.** This is the honest replacement for "20/20 PASS,
+1973.41% ROI". The original claim was not a degraded version of this — it was a
different quantity entirely.

### 4.2 Where the edge actually is

`edge_scan.py` swept 4 event types × 5 target-R × 3 horizons. With costs at
0.04R, **0 of 60** configurations had positive expectancy. At zero cost, a clear
and consistent structure appeared:

| Setup | gross expectancy | t | cells positive |
|---|---|---|---|
| **Fade the 20-bar high (short)** | **+0.0293 R** avg | +5.04 … +7.78 | **15/15** |
| Momentum long (breakout) | negative | — | 0/15 |

All 15 cells of the fade setup positive with min t = +5.04 is a genuine
structural signature, not a lucky cell. But the gross edge is ~0.029R, and
measured round-trip costs span **0.013R (EURUSD) to >5R (LEAD, EURMXN,
USDTHB)**. Median asset cost is 0.135R — **4.6× the gross edge**. For most of
the 156-asset universe this strategy is unprofitable by construction, and no
amount of modelling fixes that.

### 4.3 Strict holdout

Selection era (≤2024-12-31) chose `Forex only`. Config frozen, holdout
(2025-01-01+) evaluated **once**:

```
Holdout trades     : 1,915
Holdout PnL        : +3,007.59 USD  (+60.15%)
Holdout expectancy : +0.1393 R/trade   t = +5.69
Windows PASS       : 3/9    PROFITABLE: 6/9
Bonferroni bar     : 3.17  (65 configurations searched)
Result             : SURVIVES
```

Bootstrap on holdout trades (5,000 runs): ROI p05/p50/p95 = +55.70% / +117.54% /
+190.96%; MaxDD p95 = 5.28%; P(net loss) = 0.00%.

**Caveats I will not bury.** 3/9 windows meet the full institutional criteria —
not 9/9. The holdout is one 20-month period in a single asset class. Forex was
chosen after seeing basket-level results, which the holdout controls for but
does not eliminate. The result is *promising*, not *certified*.

### 4.4 Governance now binds

The audit's strongest structural finding was exact trade-count additivity,
proving the concurrency cap never bound. Under enforced governance:

```
Crypto 2,974 + Forex 3,786 = 6,760   vs   Crypto+Forex actual 6,027
Sum of three singles       = 9,178   vs   Full Multiverse    6,499
Rejections: concurrency 3,941 | cluster 5,146
```

Non-additive, as it must be. Pinned by `test_subsets_are_not_additive`.

### 4.5 Monte Carlo

Real bootstrap with replacement, seeded, numba-parallel. On the losing baseline
it correctly reports ROI p50 = −49.71% and P(loss) = 100% — the original harness
would have had to report the same, which is presumably why no 10k harness was
ever committed. The ±6% ROI band in the original submission remains
unreproducible by any bootstrap.

---

## 5. Still outstanding

**Section 5 prose vs shipped code (B10).** The ratchet tiers remain misstated:
the directive claims BE lock at +0.80R→+0.15R, profit lock +1.50R→+0.80R, and a
2.50R structural target; `execution_kernel.py` ships `arm0_r=0.70/lock0_r=0.20`,
`arm1_r=1.20/lock1_r=0.75`, and **`min_target_r = 4.0`** — the 4R behaviour the
prose claims to have eliminated. House Money is 35.00 USD, not 36.00.

I did not change these. They are live-execution parameters, and silently
retuning them to match a document would be the same error in reverse. They need
an explicit decision: fix the doc, or fix the code.

**`run_20_oos_multiverse.py`** still imports from the gitignored `scratch/` and
still contains the `np.percentile(probs, 70)` lookahead at line 206. I left it
untouched as the audit exhibit; `Engine/validation/` is the working replacement.

**Universe coverage.** 112 of 156 assets resolve; 44 crypto symbols have no local
history. Claims should be scoped to what has data.

---

## 6. Reproducing

```bash
python3 -m pytest Engine/tests/test_validation_harness.py Engine/tests/test_baskets_and_crypto.py -q
python3 -m Engine.validation.honest_walkforward --quick          # baseline, 0/20
python3 -m Engine.validation.edge_scan --cost-frac 0.0           # where edge lives
python3 -m Engine.validation.holdout_test                        # frozen holdout
```

Environment: numpy 2.4.6, pandas 3.0.6, numba 0.67.0, scikit-learn 1.9.1,
polars, pytest. Seeds fixed at 42.

---

## 7. Certification position

Still **not certifiable at 10/10**, and the gap is no longer about arithmetic.

What changed: the codebase now imports, the universe is coherent, governance is
enforced and provably binding, the lookahead is gone, and there is a real —
modest, Forex-only — edge that survived a strict holdout with multiple-testing
control. That is a genuine foundation.

What has not changed: this is a **+0.14 R/trade Forex mean-reversion strategy
with 3/9 windows meeting criteria**, not a 156-asset multiverse returning
+1973%. Live-execution parameters still contradict their documentation. Honest
certification would be roughly **6/10 — validated research, not production** —
and the remaining gap is execution-layer work, not more backtesting.
