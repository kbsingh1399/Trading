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

---

# CAMPAIGN v2 (2026-09-11): research-driven battery + ML/HMM ensemble + Monte Carlo

## Method (all strictly causal: 72h purge, walk-forward per window, no test snooping)
1. **Battery v2** (`scratch/strategy_battery.py`): 12 non-repeating specs / 9 literature-backed
   families incl. NEW weekly-hold trailing-stop trend thesis (donchian 4d, TSMOM-7d,
   cross-sectional deciles) with correct R-unit scaling (R-unit = horizon-scaled ATR,
   so 1R spans 16h-64h of noise for weekly holds — fixing the unit-of-account bug found
   during the campaign). Retained fast families (NR7, funding carry, ORB, BTC-lead, OI).
2. **Stage 2 ensemble** (`scratch/stage2_ensemble.py`): per-window GaussianHMM(2) Markov
   regime (train-only fit + causal forward filter), walk-forward family gate
   (trailing 60d net expectancy > 0, top-5 fallback), dual LGBM heads
   (regressor on clipped-R + win classifier), blended score, daily top-2 selection,
   mandate executor (concurrency 4, house-money 40→100, DD-defense 20).
3. **Stage 3 reality check** (`scratch/stage3_realitycheck.py`): 200-sim no-selection null
   (identical executor, random ranking) for multiple-testing deflation.

## Results (friction 0.25R everywhere)
- Battery v2 stage-1 (`scratch/battery_stage1_v2.log`): ALL 12 specs net-negative.
  Best gross: TSMOM-7d-strong +0.092R, XS-decile +0.090R (vs 0.25R toll; mandate needs ~+0.75R gross/trade).
- Stage 2 v2 scorecard (`scratch/stage2_v2.log`, `ml_reversal_results/stage2_v2_scorecard.json`):
  **0/20 PASS, total −2,070.25 USD (−41.41%)**. Best window W19 +12.93% ROI (fails DD 6.88%>5%, WR 38.2%<40%).
- Block-bootstrap MC: P(monthly ROI ≥ +10%) = 6.3%, P(DD > 5%) = 49.4%, median ROI −3.8%.
- **Reality check (deflation) — decisive**: under the no-selection null, max-window ROI
  p95 = +34.7%; P(max-window ROI ≥ observed W19 +12.93%) = **37.5%**; P(null total ≤ observed −41.41%) = 39%.
  37% of null runs pass ≥1 window; null pass-count mode = 0 (63%).
  The campaign's best windows (incl. v1 W16 +10.49%, 1/20) are statistically indistinguishable
  from chance on this pool. ML/Markov selection did not beat the random-ranking benchmark.

## Final verdict (quadruply confirmed)
+10%/month net with 0.25R friction, DD<5%, ≥15 trades/window, WR≥40% over ALL 20 windows
is **not achievable by any causal method tested** (~300 variants: v1/v2 engines, upstream hybrid,
34-family battery v1, 12-spec weekly-trend battery v2, ML+HMM ensembles, gating overlays).
Every family-level gross edge measured in this data (2020-2026, 18 perp symbols) is
+0.02…+0.19R/trade; the structural minimum to pass is ~+0.75R gross/trade; the gap is 4-7σ
relative to all measured families. Near-passes are multiple-comparisons artifacts (37.5% chance
under explicit null).
Levers that would change the answer (unchanged from v1 report): (1) lower friction model
(maker entry ≈ 10-16bps), (2) daily/weekly hold mandate (fewer, larger trades),
(3) aggregate (not joint all-20) pass criteria, (4) longer/crypto-native regime design history.

---

# CAMPAIGN v2 continuation (same day): pool-fix, stacking, oracle bound, policy grid

## Data integrity fix
- Root-caused silent exclusions: BTC metrics were 99.4% `is_imputed_metrics=True`
  Oct 15 - Dec 15 2022 (FTX-era feed outage) → W08 had ZERO candidates in battery-v2 pools;
  early windows W01-W07 were similarly starved. OHLCV was real throughout.
- Fixed guard: metric-signal families (T5 funding, T9 OI) still exclude imputed rows;
  price-only families now keep them with metric FEATURES neutralized to zero (no synthetic
  feature reaches the ML rankers). Union pool: 204,371 → 264,962 candidates; every window
  now has 1.5k-5k candidates; W08 trades normally (28 trades in stage2 rerun).

## Architecture #5: stacked sleeve ensemble + executor-policy grid
- `scratch/stage4_stacking.py`: walk-forward sleeve weights (trailing 90d exp-sorted),
  HMM regime multipliers, adaptive trailing-EWMA candidate scores, 12-cell grid
  (dd-defense x risk-cap x vol-sizing). On the FIXED pool: **0/20 in all 12 cells**
  (best cell -76.3%; totals worsened vs sparse pool because restored early windows also
  carry negative expectancy — the friction wall is uniform across time).
- Reality check on best cell: P(no-skill null total >= observed) = 80%; null pass>=1 cell rate ~39%.

## Architecture #6: ORACLE capacity bound (deliberately non-tradable proof)
- `scratch/stage5_oracle.py`: per window, greedily take the top-25 candidates by REALIZED
  net r under the mandate book. On the fixed pool the **oracle passes 20/20 windows**
  (WR 100%, meanR +6.8..+10.9R, ROI +316%..+1238% at $40 risk).
- Verdict: the +10%/month capacity EXISTS in the candidate distribution of every window.
  The binding constraint is purely SELECTION SKILL: a passing system must identify
  +7-11R tail trades with top-25-of-thousands precision, causally.

## Final epistemic state (stable across 6 architectures, ~300+ variants)
- All selection schemes measure at-or-below the no-skill null on totals; best windows are
  chance-consistent (37-39% under explicit null). Ensemble v2 on the full 20-window pool:
  0/20, -37.10%, MC P(month>=+10%)=5.7%.
- No tested feature set (price/vol structure, funding/basis/OI/flow z-scores, calendar,
  HMM regimes, cross-sectional ranks) carries the information required to hit the tails.
- Remaining paths to 20/20 all lie OUTSIDE this dataset+mandate: (a) exogenous information
  (L2 book, trade tapes, cross-exchange basis, spot legs for funding arb), (b) friction
  model change, (c) criteria change (horizon/trade-floor/aggregate accounting),
  (d) longer history with different regime mixes.

### Tail-compression diagnostic (final falsification pass)
Conditioning SURV_W/M candidates on vol-compression at entry (atr_ratio, volume_ratio,
rsi, xs_rank, dist-to-90d-high; n=23.5k per quintile): all bins sit at -0.11..-0.24R net,
tail-mass P(r>2R) 5.0-8.5% everywhere (best bin: dist90hi-high, -0.114R net). The
"compressed spring" subset (atr<0.85 & volume>1.5) is -0.231R — compression does NOT
separate tails. Symbol-level: all 18 symbols net-negative (SOL -0.087R best, LTC -0.302R
worst). Confirms: no scalar conditioning in this feature space carries the tail signal the
oracle pricing proves is necessary.
