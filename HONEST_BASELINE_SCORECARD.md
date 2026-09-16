# Honest Baseline Scorecard — Phase 1 + Phase 2

**Branch:** `arena/01a0a5bf-trading` · **Fix commit:** `15fabb7`
**All figures below were produced by running `Engine/run_20_oos_dual_model.py --disable-governor` on this checkout.**

---

## Correction to my own prior statement

I reported last turn that `papers/Master_Batch_1/` does not exist. **That was true of my
checkout and is no longer true of the repository.** `origin/main` carries commit `453ff9b`
("force-add all 883 research papers"), which lands **897 files** under `papers/` —
**883 PDFs**, of which **543** are in `Master_Batch_1/`. My branch is one commit behind
`origin/main` and so did not contain them when I looked. The audit's corpus claims were
correct; my "does not exist" finding was an artefact of reading a stale tree.

---

## The two corrections

**Phase 1 — friction parity.** Friction was a flat fraction of R on S1 (0.18R ≈ 25.9 bps) and
a flat bps charge on T1 (20.5 bps), while both docstrings claimed 41.0 bps. Neither sleeve was
charged the documented cost and they disagreed with each other. Charging in R units was the
deeper error: R is volatility-scaled, so a flat-R fee charges almost nothing in calm markets.
Cost is now charged on **entry notional** — `Engine/execution_costs.py` holds
`ROUND_TRIP_BPS = 41.0` as the single source of truth, and `friction_r` has been deleted from
every signature (`label_triple_barriers_numba`, `simulate_microstructure_ratchet_numba`,
`compile_dataset_with_numba`) plus the `--friction-r` runner flag, so it cannot drift again.

**Phase 2 — ATR floor removed.** `np.maximum(atr_14, close * 0.012)` bound on **92.45%** of
bars across all 11 symbols, pinning R to a constant 1.440% of price. Pure `atr_14` now drives
the geometry. R is genuinely adaptive again:

| Symbol | R p10 | R p50 | R p90 |
|---|---|---|---|
| BTCUSDT | 0.196% | 0.422% | 0.852% |
| ETHUSDT | 0.280% | 0.563% | 1.090% |
| XRPUSDT | 0.325% | 0.620% | 1.434% |
| DOGEUSDT | 0.367% | 0.713% | 1.587% |
| TRXUSDT | 0.154% | 0.345% | 1.019% |

---

## Verification

`scratch/test_friction_parity.py` — **20/20 assertions pass.** The S1 charge is recovered from
the *real* kernel's `realized_r` in a flat market (where `exit_r == 0`, so `realized_r == -fric_r`
exactly) and reads **41.0000000000 bps** at four different price/ATR scales. The ratchet
simulator is checked the same way. T1 is asserted arithmetically identical to S1, and the charge
is shown regime-invariant across five volatility regimes.

A runtime probe confirms both live modules bind `ROUND_TRIP_FRAC = 0.0041` and that the old
`0.00205` literal is gone from T1.

**Control-invariance check:** checking out the pre-fix files reproduces **+5,553.70 / 674 trades
/ 10 passes** exactly, so the Phase 1 refactor changed nothing except the cost. (An earlier
control attempt of mine returned +4,283.55 — that was my own patching error, having reverted
S1's fee while leaving T1 at 41 bps. It is not a refactor artefact.)

---

## The honest scorecard

| Window set | Trades | PnL | ROI | Pass |
|---|---|---|---|---|
| Primary (20) | 326 | **+291.84** | +5.84% | **3/20** |
| Holdout (20 random) | 288 | **−88.03** | −1.76% | **1/20** |
| Expanded (25, 2021-24) | 444 | **−2,158.49** | −43.17% | **1/25** |
| **Pooled** | **1,058** | **−1,954.68** | — | **5/65** |

Previously reported: +5,553.70 (10/20), +137.94 (3/20), +489.99 (2/25).

---

## Attribution — which correction did the damage

I measured the full 2×2 rather than inferring it. Config C is pre-fix friction on **both**
sleeves with only the ATR floor removed.

| Config | Friction | ATR floor | Primary | Holdout | Expanded |
|---|---|---|---|---|---|
| **A** as reported | S1 25.9 bps / T1 20.5 bps | ON (binds 92.45%) | +5,553.70 | +137.94 | +489.99 |
| **C** Phase 2 only | same as A | **OFF** | +2,033.02 | +1,504.13 | +18.61 |
| **D** honest (shipped) | **41.0 bps both** | **OFF** | **+291.84** | **−88.03** | **−2,158.49** |

**Phase 1, friction (C → D):** primary −1,741.18, holdout −1,592.16, expanded −2,177.10.
**Consistent in sign and magnitude on every set.** This is the real correction: the strategy
was being charged roughly half to two-thirds of its true round-trip cost, and it does not
survive the difference.

**Phase 2, ATR floor (A → C):** primary −3,520.68, holdout **+1,366.19**, expanded −471.38.
**Inconsistent in sign.** Removing the floor was not systematically flattering the backtest —
it helped the holdout substantially. So the floor was not the source of the headline edge; it
was simply a different geometry. Its removal is a correctness fix (the strategy now behaves as
documented), not a haircut.

**Total (A → D):** primary −5,261.86, holdout −225.97, expanded −2,648.48. Pooled
+6,181.63 → **−1,954.68**.

---

## What this means

Once honestly costed and made genuinely ATR-adaptive, **the strategy has no positive
expectancy.** It is marginally positive on the primary windows (+291.84 over 20 monthly
windows, 3 passes) and negative on both the holdout and expanded sets. The pooled result is
negative.

Two readings, both uncomfortable:

1. **The +5,553.70 was never real.** It was a fixed-percentage grid charged fantasy fees. That
   the primary and holdout sets move in opposite directions under Phase 2 (+5.5k → +2.0k vs
   +0.14k → +1.5k) is itself evidence the configuration was tuned to the primary windows.
2. **The cost model was the binding constraint, not the alpha.** A 15–20 bps per-side error is
   enough to move every window set negative. Any strategy whose verdict flips on a fee
   assumption that small is not deployable, regardless of how the alpha search goes.

This is the honest foundation you asked for. The number to beat is no longer +5,553.70 — it is
**−1,954.68 pooled**, and the primary-set reference is **+291.84**.

---

## Open items

- **The 883 papers are now available.** My literature review last turn was done on 74 markdown
  summaries plus 5 PDFs, and I should redo it against the real corpus. That is a separate
  piece of work — reading 883 PDFs is not a one-pass task, and I would want to triage by
  relevance to microstructure/execution cost first.
- **The pre-existing threshold accelerator is still live.** `score_test_candidates` lowers the
  threshold by 0.025 when `trailing_vol_pct < 0.92` (visible as `eff_thr` drifting
  0.4507 → 0.3308 across windows where `Δthresh = +0.000`). That is a *relief* branch, and it
  is in tension with the defensive-only rule you set. It was not part of Phase 1/2 so I have
  left it alone, but it is now the largest remaining realism gap.
- **The regime governor remains disabled** (`--disable-governor`) for all figures above, since
  it was falsified. All three honest numbers are the ungoverned engine.
