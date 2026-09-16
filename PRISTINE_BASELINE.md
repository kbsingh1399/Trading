# Pristine Baseline — Leaks Plugged, Training Decoupled

**Branch:** `arena/01a0a5bf-trading`

---

## 1. Holdout leakage fixed

`scratch/build_disjoint_windows.py` regenerates all three sets from **one
contiguous calendar-month grid**, partitioned into chronological blocks. It
**refuses to write output** if any two windows in any two sets overlap by even
a single day, and independently asserts that every calendar month is assigned
to exactly one set.

| set | file | windows | span |
|---|---|---|---|
| Primary | `Engine/oos_windows_primary.json` | 22 | 2021-05-01 → 2023-02-28 |
| Holdout | `Engine/oos_windows_holdout.json` | 22 | 2023-03-01 → 2024-12-31 |
| Expanded | `Engine/oos_windows_expanded.json` | 20 | 2025-01-01 → 2026-08-31 |

**64 months, zero overlap, verified two independent ways.**

Two deliberate changes beyond disjointness:

1. **Contiguous, not event-selected.** The old primary set was 20 hand-picked
   crisis months ("May 2021 Great Liquidation Crash", "FTX Collapse Bottom").
   Choosing evaluation windows because they were dramatic is a selection bias
   in the test set itself. The new grid tests ordinary months as well as
   crises.
2. **Chronological.** Primary is the earliest block and Expanded the most
   recent, so later sets have strictly more training history — standard
   walk-forward, and no set can peek at another.

---

## 2. Cross-sectional training coupling fixed

`run_20_oos_dual_model.py` previously did:

```python
train_set = all_data[train_mask]                     # ALL symbols pooled
ridge, clf, mu, sd, calib_thresh = engine.train_models(train_set)
```

Now it fits **one model per symbol on that symbol's own history** via
`train_models_by_symbol` / `score_test_candidates_by_symbol`. Symbols below
`min_train_rows_per_symbol` (500), or with only one class present in the
training window, are **skipped entirely** rather than silently borrowing a
pooled model.

### The invariant is proven, not asserted

`scratch/test_symbol_decoupling.py` fits models on the full universe and again
on an 11-symbol subset, then compares predictions for the 11 common symbols on
identical test rows:

```
PASS  all common symbols produce bit-identical probabilities -- 11/11, worst diff 0.000e+00
PASS  max |delta prob| across every common symbol is exactly 0.0 -- 0.000e+00
PASS  the set of SELECTED candidates for the 11 common symbols is unchanged -- 128 vs 128
```

Dropping 7 symbols now changes the other 11 by **exactly zero**. Before this
change the same operation moved them by +3,203.83 USD.

---

## 3. The pristine baseline

Governor disabled, 41.0 bps + regime stress, 18 symbols, per-symbol models,
disjoint windows:

| set | windows | trades | PnL | ROI | pass |
|---|---|---|---|---|---|
| Primary (2021-05 → 2023-02) | 21 | 222 | **−3,610.30** | −72.21% | **0/21** |
| Holdout (2023-03 → 2024-12) | 22 | 271 | **−3,917.50** | −78.35% | **0/22** |
| Expanded (2025-01 → 2026-08) | 20 | 242 | **−3,561.55** | −71.23% | **0/20** |
| **POOLED** | **63** | **735** | **−11,089.36** | — | **0/63** |

**Not one of 63 windows passes.** The three sets now agree with each other,
which is itself new: previously primary and holdout moved in opposite
directions under the same change, the signature of a tuned configuration.

The first window (2021-05) is skipped: no symbol clears 500 training rows with
both classes before it, since data starts 2020-09-01.

### Cumulative honesty ledger

| stage | pooled PnL |
|---|---|
| as originally reported | **+6,181.63** |
| + friction parity at 41 bps | −1,954.68 |
| + relief branch removed | −1,930.62 |
| + regime friction stress | −2,734.21 |
| + 18 symbols (contaminated, cross-sectional model) | −269.91 |
| **+ disjoint windows + per-symbol models** | **−11,089.36** |

The last step is the largest single revision, and it is the only one that
removed *information leakage* rather than added cost realism.

---

## 4. What decoupling cost, stated plainly

Per-symbol training is **much worse** than the pooled model:

| | pooled model (contaminated) | per-symbol (clean) |
|---|---|---|
| sleeve mix | T1 65% / S1 35% | **S1 84% / T1 16%** |
| win rate | ~50% | **31.5% / 35.1% / 33.9%** |
| mean r | ~−0.09 | **−0.71 / −0.75 / −0.82** |

This is a real trade-off, not a bug. The pooled model borrowed statistical
strength across 18 correlated symbols — each per-symbol model sees roughly
1/18th of the training rows. **But the pooled model's better numbers were never
evidence of edge**; they were evidence that a model fitted on 18 symbols
generalises slightly better to those same 18 symbols, while making attribution
impossible and letting any universe change rewrite history.

A middle path exists (hierarchical / partial pooling), but it reintroduces
exactly the coupling we just removed. That is a decision for you, not a
measurement, so I have not made it.

---

## 5. CVaR harness on the pristine ledger

n=735, tail_count=8, CVaR99 = **−4.4155 R**:

| veto | drops | efficiency | p |
|---|---|---|---|
| Oracle (drop all 488 losers) | 66.39% | 5.77× | — |
| `vol_rank >= 0.88` | 33 (4.49%) | 5.61× | **0.0999 — not significant** |
| `strat == T1` | 115 (15.65%) | **0.00×** | 1.0000 |
| `strat == S1` | 620 (84.35%) | 2.55× | 0.0000 |

**Confirmed a third time: all 8 worst trades are S1, zero T1.** (12/12 on the
11-symbol ledger, 15/15 on the contaminated 18-symbol ledger, 8/8 here.)

**`vol_rank` fails again** — 5.61× but p=0.0999. Across three universes it has
now scored p=0.0098, p=0.127 and p=0.0999. A result that only appears once is
noise, and this one has now failed to replicate twice.

And the mechanism is visible: **only 1 of the 8 tail trades has
`vol_rank ≥ 0.88`.** The tail is simply not a high-volatility event, so no
volatility gate can catch it. That is now established across every
configuration we have built.

---

## 6. Verification

| suite | assertions | failures |
|---|---|---|
| `scratch/test_friction_parity.py` | 39 | 0 |
| `scratch/test_cvar_harness.py` | 22 | 0 |
| `scratch/test_symbol_decoupling.py` | 6 | 0 |
| `scratch/build_disjoint_windows.py` | refuses to write on any overlap | — |

The disjointness proof runs inside the generator, so a future regeneration
cannot silently reintroduce leakage.

## 7. What I have not verified

- Whether per-symbol models are the *right* architecture, only that they are
  **clean**. They are demonstrably worse on this data. Partial pooling may
  recover performance without reintroducing contamination; I have not tested it.
- The 2021-05 window is skipped for insufficient per-symbol history, so the
  primary set is 21 windows, not 22.
- With 0/63 passes, the strategy has no positive expectancy under any
  configuration we have tested. I have not attempted to tune it back to
  profitability, and doing so on these same 63 windows would convert them to
  in-sample.
