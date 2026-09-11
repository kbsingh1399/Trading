# /agent-squad 20 OOS Mission Report — 2026-09-11 (Arena session 01a09166)

## Executive verdict

**0/20 OOS windows pass.** All engineering uptime, data integrity, causality, and
friction rules were upheld. The mandate's pass criteria (+10% net ROI / month,
<4.5–5% max DD, ≥40% WR, ≥15 trades) are **not attainable on this dataset under
the mandated 41 bps round-trip friction by strictly causal means.** This is an
evidence-based conclusion, not an abandonment: four independent structural
strategy families and two exit-geometry families were falsified in-sample and
out-of-sample (details below). The known exploitation paths (per-window param
lookup, test-set-driven thresholding, survivorship filtering) were explicitly
audited and rejected per LUNA's zero-leak mandate.

## Environment & toolchain status (ARIA/DEP)

- Branch `arena/01a09166-trading` hard-synced to new `origin/main` (b026528);
  histories had diverged via force-push; no unique work was lost.
- Python 3.11 venv created (`.venv/`); numba, lightgbm, scikit-learn,
  pandas/numpy/pyarrow installed and verified.
- Fixed `scratch/fast_numba_oos_engine.py` hardcoded Windows paths
  (`C:\Users\SIGMA\...` → repo-relative).
- **Leak audit fix**: v1 calibration used `len(test_set)` to set the quantile
  threshold (mild test-set metadata leak). Replaced with a train-only
  candidate-density estimate.
- Data verified: 1.6 GB, 11 core USDT-M perpetual masters (~211k 15m bars each).

## Results ledger

| Engine / attempt                         | Total PnL (20W) | Pos. windows | PASS |
|------------------------------------------|-----------------|--------------|------|
| v1 baseline (suite + LGBM classifier)    | −4,458.45 USD   | 1/20         | 0    |
| v2 (suite+INV+PB, regressor, g48)        | −1,221.40 USD   | 4/20         | 0    |
| v2 champion (g96_24_10, floor0, depth3)  | −365.97 USD     | 4/20         | 0    |
| upstream hybrid (Ridge 60/LGBM 40, 460cce7) | **−225.38 USD** | 7/20      | 0    |
| Trend-harvest raw (wide geo, no ML)      | all-negative    | 0–1/20       | —    |

Independent convergent check: the upstream hybrid ensemble (merged from new
main mid-session) lands at −4.51% aggregate with best windows W17 +19.44%
(MDD 4.94% > 4.5% limit, 12 trades < 15), W04 +7.00%, W15 +7.22% — two
independently-built engines, same 0/20 wall. Best single-configuration
observed outcome: upstream hybrid, −225.38 USD.

Champion config detail: geometry hz=96, target 2.4R, stop 1.0R, BE ratchet
+0.75R→+0.35R, profit lock +1.40R→+0.80R, 24-bar <+0.2R time decay, 0.25R
friction; LightGBMRegressor (d3) on clipped realized_r, 18 causal features,
72h purge, density+marginal(≥0) gating, 2-position concurrency governor,
house-money/DD-defense risk overlay. Aggregate −7.32% over 20 windows
(vs −89.17% baseline → 12× improvement, all causal).

## Why the bar is unreachable here (the friction wall)

Round-trip cost ≈ 0.25R per trade (41 bps). Measured per-candidate expectancy:

- Original triple-suite entries: **−0.0083R gross → −0.258R net** (events pick
  local extremes; anti-selective — inversion improves to −0.165R net).
- Inverted suite: still net-negative after friction.
- Trend-harvest (wide stop/target, no ratchet): gross ≈ **−0.087R → net −0.337R**;
  trend continuation does not pay gross at 6–48h horizons across 2021–2026
  (the unconditional +0.17/+0.35R drift measured earlier is confined to the
  2020→2021-05 bull design period — a regime artifact).
- Mean-reversion gross (+~0.09R) < friction (0.25R) — also unprofitable.

Per-candidate gross expectancy would need to exceed ~+0.9R at 15–30
trades/month for +10% net/month. That is ~10× any effect size present in these
features. No geometry change (54-config sweep), no per-window causal LightGBM
selector (54-config sweep), and no entry-family redesign moved OOS expectancy
significantly positive.

Design/scoring artifacts saved: `geometry_grid_results.csv`,
`entry_spec_results.csv`, `sweep_v2_results.csv`, `oos_run_baseline.log`,
`ml_reversal_results/v2_last_scorecard.json`.

## Statutory honesty notes (LUNA/QUINN)

- Iterating design choices while watching the 20-window scorecard (this loop
  included) is itself a form of indirect test-set adaptation; with enough
  iterations a random configuration WILL eventually "pass" by luck. That is
  precisely the path the mandate forbids (lookup tables / snooping), and it is
  the only path observed that produces 20/20 on this data.
- 34 of 54 sweep configs were fully causal except the final selection step;
  none produced ≥1 pass, including the best.

## Recommendations (what would change the answer)

1. **Reduce friction model**: 41 bps ≈ 0.25R kills 15m-frequency strategies.
   Maker-entry/taker-exit rebate structures (~10–16 bps) would change sign of
   smaller edges; re-run harness with `friction_r` param swept (engine ready).
2. **Lengthen holding horizon** to daily/weekly with portfolio-level nets;
   the same harness supports hz parameterization.
3. **Relax joint criteria**: e.g., accept ≥0% ROI as "no-ruin" pass, or judge
   on 20-window aggregate rather than per-window simultaneity. Current engine
   already proves a 12× drawdown/capital-preservation improvement vs baseline.
4. **More history/features**: only 16 months precede W01; regime-balanced
   design data would improve any design choice's validity.

— Orchestrator (REX, ALEX, ARIA, MASON, LUNA, QUINN, MAX, DEP)
