# Levels / POC research lab — results

**Question.** Do breaks of the previous week high/low, previous month high/low,
all-time high, and the several "perspectives" around the session Point of Control
(POC) produce tradable edge on Binance USDT-M 15m data — enough to pass all 20
pre-registered OOS windows under the certified execution contract?

**Answer (short).** Not yet, and the evidence says this rubric is not reachable
with this strategy class under this contract.

* The *long-side period-high break* effects are real but small: the best families
  carry **+0.20 to +0.27 R per event of gross edge over a random-entry control**,
  i.e. roughly **28–33 bps of price** per trade. The certified round-trip cost is
  **41 bps**, so on those terms every family is net negative.
* An ML meta-labeller trained only on pre-window data, a BTC-tide regime filter,
  carried-break candidates (a broken level stays actionable for up to 24 bars),
  count-based selection and an *expectancy* objective (`P(net_r > 1R)` instead of
  `P(net_r > 0)`) change the portfolio result from −42 % to **+29 %** over the
  20 windows — with **1/20–2/20** windows passing and the per-window ROI
  distribution still 5–10× short of the +10 %-every-window requirement.
* The POC *mean-reversion* perspectives (magnet, reclaim, rejection) carry no
  edge at all; the "liquidity sweep fade" is systematically on the wrong side;
  the shipped footprint ladder is a candle-level footprint too coarse to add
  anything (median 4 bins per candle).

Sections 3–5 give the measured arithmetic for why, and §6 gives the reproduce
commands.

---

## 1. Setup

| Item | Value |
|---|---|
| Universe | 17 altcoin USDT-M perpetuals (BTC used as macro context, per `protocol.json`) |
| Data | `Engine/binance_backtesting_data/*_15m_master_2020_2026.parquet` (contiguous 15m, 2020-09-01 → 2026-09) |
| Windows | the 20 pre-registered crash/trend/chop windows, `Engine/oos_windows_20.json` |
| Criteria | per window ROI ≥ +10 %, DD ≤ 5 %, WR ≥ 40 %, ≥ 15 trades, 4R target |
| Costs | 8 bps fee, 10 bps entry slip, 15 bps exit slip, 41 bps round-trip floor |
| Fills | signal on completed candle → next open; stop-first inside the bar |
| Families | 37 pre-registered geometries, fixed a-priori parameters (no per-window fitting) |
| ML | LightGBM meta-labeller trained only on events ending before `window_start − 72 h` |

Volume profiles are **reconstructed from OHLCV** (uniform-in-log-price intra-bar
distribution, 5 bp grid): the shipped ladder is certified
`poc_source = OHLC_APPROX` (see `docs/PIPELINE_CERTIFICATION_ROUND5.md`) and is
therefore not used as a feature. Reconstructed POC vs ladder POC: median relative
error 0.39 % (BTC), 0.54 % (ETH), 0.83 % (SOL), 0.71 % (DOGE); cross-check
artifacts in `scratch/lpl_*`.

---

## 2. Directional evidence (impulse study, 17 symbols, ATR units)

Mean forward return after the event, in ATR units. Positive = the event's
direction pays (longs: price up; shorts: price down).

| family | n | 24 bars (6h) | 96 bars (24h) | 288 bars (3d) |
|---|---|---|---|---|
| `x_ath_brk_lowvol` (new ATH, compressed vol) | 478 | **+0.93** (t=4.8) | **+2.49** (t=6.1) | **+3.19** |
| `brk_ath` (new all-time high) | 1 094 | **+0.56** (t=4.9) | **+2.24** (t=7.6) | **+9.69** (t=4.5) |
| `brk_pwh_cascade` (week high into month-high band) | 402 | +0.52 (t=3.1) | +1.36 (t=4.2) | +4.84 |
| `brk_pmh` (month high) | 2 170 | +0.39 (t=4.6) | +0.81 (t=5.1) | +6.95 |
| `brk_multi_lvl` (≥2 period highs in 8 bars) | 20 601 | +0.20 (t=8.2) | +0.59 (t=11.1) | — |
| `brk_pwh` (week high) | 5 243 | +0.21 (t=4.3) | +0.50 (t=4.7) | +4.63 |
| `brk_pdh` (prior day high) | 18 213 | +0.13 (t=4.6) | +0.29 (t=4.6) | +8.75 |
| `brk_pwl` / `brk_pdl` (shorts) | 4 783 / 16 599 | -0.03 / +0.04 | -0.26 / -0.18 | -0.73 / -0.50 |
| `swp_pwh` (fade week-high sweep) | 9 607 | **-0.07** | **-0.41** (t=-6.0) | -0.68 |
| `swp_ath` (fade ATH sweep) | 1 355 | -0.07 | **-2.08** (t=-8.0) | -3.96 |
| `poc_magnet` (≥2σ reversion to POC) | 133 182 | -0.01 (t=-2.1) | -0.10 (t=-5.2) | -0.38 (t=-10.6) |
| `poc_reclaim_up` (reclaim developing POC) | 136 790 | +0.02 | +0.05 | +0.32 |
| `poc_value_break_up` (acceptance above VA) | 48 712 | +0.03 | +0.14 | +0.65 |

Readings:

1. **Momentum at period highs is real and strongest at the ATH** — the only
   "resistance" that has no overhead supply history. It decays with horizon for
   the impulse but keeps paying at 3 days for ATH/cascade breaks.
2. **Short-side level breaks have no edge** (0 to -0.3 ATR at 24h). Crypto's
   downside breaks behave like liquidity events, not like continuation.
3. **Fading sweeps loses** (-0.41 to -2.08 ATR): what the practitioner literature
   calls a "stop hunt" behaves as a *breakout* at 15m on these venues. The
   "volume tell" does not rescue the fade.
4. **POC mean-reversion is negative or zero** across 133k–138k events — the
   Dalton-style "price returns to the POC" claim does not survive contact with
   this data at a tradable scale.

### 2.1 Random-entry control

2 % of volume-confirmed bars entered with the *same* stop/target geometry and no
costs: **long -0.028 R, short +0.075 R** gross per trade (n ≈ 15 600/side across
17 symbols). So the short-side "edges" of most POC/level families are just the
sample's negative alt drift; only the long period-high families add information
above the control (+0.19 R for `brk_ath`, +0.27 R for `x_ath_brk_lowvol`).

### 2.2 Conditional splits

Edge concentrates where the trend context agrees: `brk_ath` long in a BTC bull
macro tide +4.03 ATR at 24h (t=5.0, n=141) vs +2.24 unconditional; ATH breaks in
a compressed-vol regime (ATR z < 0.5) +2.49 ATR at 96h. Long high-breaks in a
bear macro tide are markedly weaker — the families are regime-conditional, not
universal.

---

## 3. Execution geometry: net R under the certified contract

Target 4R net, max hold 288 bars, stop = max(structural, 0.5–1 ATR, 1.2 % of
price). `gross` = friction-free; `41bps` = certified cost.

| family | n | mean stop % price | gross mean R | gross WR | net R @41bps | break-even friction |
|---|---|---|---|---|---|---|
| `x_ath_brk_lowvol` | 478 | 1.38 % | **+0.241** | 26.4 % | -0.072 | **31.5 bps** |
| `poc_migration_dn` | 7 191 | 1.28 % | +0.198 | 29.7 % | -0.132 | 24.6 bps |
| `brk_ath` | 1 094 | 1.68 % | **+0.167** | 24.2 % | -0.104 | **25.3 bps** |
| `brk_pml` | 1 972 | 1.44 % | +0.158 | 28.6 % | -0.161 | 20.3 bps |
| `x_pwh_sweep_at_poc` | 675 | 1.33 % | +0.122 | 32.3 % | -0.204 | 15.3 bps |
| `brk_pmh` | 2 170 | 1.43 % | +0.102 | 26.5 % | -0.213 | 13.2 bps |
| `brk_pwh_cascade` | 402 | 1.36 % | +0.080 | 27.4 % | -0.237 | 10.4 bps |
| `brk_pwh` | 5 243 | 1.36 % | +0.061 | 26.4 % | -0.261 | 7.8 bps |
| `poc_magnet` | 133 182 | 4.29 % | -0.020 | 43.6 % | -0.172 | -5.4 bps |
| `swp_ath` | 1 355 | 1.48 % | -0.063 | 19.8 % | -0.375 | -8.3 bps |

**The frontier in one line:** the best concepts capture ~28–33 bps of price per
trade; the certified round trip charges 41 bps. Break-even sits at 25–32 bps, so
the mission fails on cost, not on signal existence.

Equivalent statement: with a typical 1.3–1.7 % stop, the 41 bps friction is
**0.25–0.32 R per trade** — a strategy must clear that hurdle before it earns
anything.

---

## 4. Portfolio walk-forward across all 20 windows

Certified kernel (`kernel.simulate`): next-open fills, stop-first bars,
adverse-bound drawdown, funding, 3× gross cap, 4.5 % circuit breaker, 3
concurrent positions, cross-sectional ranking.

| Run | Geometry | Cost | Passed | Trades | Net PnL | ROI |
|---|---|---|---|---|---|---|
| Geometric, no gate | 4R / 288 bars | 41 bps | **0/20** | 245 | -$2 076.73 | -41.5 % |
| ML gate | 4R / 288 bars | 41 bps | **0/20** | 184 | -$2 112.79 | -42.3 % |
| ML gate | 2R / 48 bars | 41 bps | **0/20** | 307 | -$2 109.07 | -42.2 % |
| ML gate | 4R / 288 bars | 15 bps (sensitivity) | **0/20** | 171 | -$1 998.42 | -40.0 % |
| ML gate | 4R / 288 bars | 0 bps (ceiling) | **0/20** | 176 | -$1 906.75 | -38.1 % |

Typical per-window profile (ML-gated run): 5–25 trades, win rate 0–67 %,
DD 2–5 %, ROI -5 % to +2 %; the 4.5 % circuit breaker trips in the losing
windows. Artifacts: `scratch/lpl_ml_all17.json`, `scratch/lpl_portfolio_baseline.json`.

### 4.1 ML gate diagnostics

* Out-of-sample AUC per window: **0.504 – 0.553** (mean 0.525) for the direction
  label. The features (level distances, POC geometry, volatility regime, BTC macro
  context) barely separate profitable from unprofitable candidates — but they
  *do* separate meaningfully better than the base rate once the model is asked
  the right question (below).
* The gate does what a weak model can do: it raises the *realized win rate* on
  selected trades (several windows 50–100 % on 5–25 trades) while cutting trade
  count below the mission minimum, and it cannot manufacture +0.6 R/trade.
* **Order-flow (footprint ladder) features add nothing.** Caching the shipped
  ladder into 21 causal per-candle order-flow features (`flow.py`: taker delta
  ratio, CVD, delta z-score, imbalance/stacked-imbalance densities, within-candle
  delta skew, true-bin POC/VA geometry) changes out-of-sample AUC by
  −0.005 to +0.004 and never enters the top-30 importances:

  | window | no-flow AUC | with flow | selected-set mean R (no-flow / flow) |
  |---|---|---|---|
  | W11 | 0.6227 | 0.6172 | −0.176 / −0.191 |
  | W14 | 0.5291 | 0.5279 | +0.362 / +0.266 |
  | W17 | 0.5453 | 0.5489 | +0.566 / +0.732 |

  The reason is visible in the data itself: the "footprint" is a *candle-level*
  footprint, not a session profile — per-candle `total_vol_coin` sums exactly to
  the master `volume_base` (ratio 1.000 for every one of 211,189 BTC candles),
  there is exactly **one** `is_poc` bin per candle, `is_value_area` spans ≈ the
  candle's own range, and with $50 bins on BTC a candle has a **median of 4 price
  bins** (mean 5.2). There is almost no within-candle structure to extract, and
  `ld_d_poc` is a close-strength measure, not "distance to the session POC"
  (median |Δ| vs the reconstructed session POC = 1.24 ATR).

### 4.2 The objective function matters more than the feature set

The gate was fitting `label = (net_r > 0)`. Under a 4R-target / time-stop
geometry that label is dominated by tiny time-stop scratches: a selected set can
show a 58 % "win rate" and still average −0.19 R. Refitting the same features on
`label = (net_r > 1R)` — i.e. "did this become a *meaningful* win" — triples the
realized expectancy of the selected set (`scratch/label_check.csv`, 6 symbols,
5 windows, top-k by out-of-sample score):

| label | mean net R | hit rate | P(≥ 2R) |
|---|---|---|---|
| `net_r > 0` (direction) | +0.229 | 58.0 % | 10.4 % |
| **`net_r > 1R`** | **+0.673** | 45.7 % | **37.0 %** |
| `net_r > 2R` | +0.239 | 32.2 % | 31.0 % |
| regression on `net_r` | +0.480 | 50.2 % | 29.7 % |

+0.67 R/trade × 15 trades = +10 % ROI, exactly the mission threshold, so the
ranking side of the arithmetic is now *satisfiable*.

### 4.3 The execution side: three slots is the hard constraint

The certified contract fixes `max_positions ∈ {2, 3}`, `capital = $5,000` and
`risk_usd = $50` (`s1_trend_following_suite.Config` validation), so a window's
trade count is bounded by slot turnover, not by signal count. In the best
configuration 864 candidates cleared the gate but only 134 became trades (16 %),
and the ratios collapse exactly in the windows with the most candidates —
W05 158 → 5 trades, W15 126 → 5, W10 108 → 10 — because breakouts cluster in
time and three slots hold for up to three days.

Two changes follow from that arithmetic and are implemented here:

* `build_signal_frame(..., pending=K, pending_step=S)` — a broken level stays
  *actionable*: the break families re-emit candidates every `S` bars for up to
  `K` bars while price still holds the broken level (e.g. `brk_pwh_hold`). Labels
  are generated from those bars by the same triple-barrier machinery, so the gate
  learns *which* bar of a break is the best entry, and idle slots can be filled
  by still-valid breaks instead of waiting for the next one.
* `run_ml.py --sel-per-window N` — select the top-N candidates per window by gate
  rank rather than by an absolute probability cut, so probability-scale drift
  between train and test cannot silently loosen or tighten the gate.

### 4.4 Status against the criteria

**Not met: no configuration passes all 20 windows.** The best three, all
walk-forward (gate trained only on events ending before `window_start − 72 h`):

| configuration | passed | trades | net PnL | ROI | windows green |
|---|---|---|---|---|---|
| `lpl_ml_soft` — expectancy label, carried breaks, no hard tide filter | **1/20** | 204 | +$1,431.76 | **+28.64 %** | 8/20 |
| `lpl_ml_hold` — same + hard tide filter | **2/20** (W04, W11) | 193 | +$887.72 | +17.75 % | 9/20 |
| `lpl_ml_regime` — direction label, threshold selection, tide filter | 0/20 | 135 | +$767.98 | +15.36 % | **12/20** |

Per-window ROI (%, trades in brackets) for the best variant:

| W01 | W02 | W03 | W04 | W05 | W06 | W07 | W08 | W09 | W10 |
|---|---|---|---|---|---|---|---|---|---|
| −0.8 (12) | −0.5 (16) | +6.5 (20) | **+15.4 (17)** | −0.8 (8) | **+16.0 (13)** | −2.3 (20) | −4.0 (11) | −4.5 (5) | −2.8 (6) |

| W11 | W12 | W13 | W14 | W15 | W16 | W17 | W18 | W19 | W20 |
|---|---|---|---|---|---|---|---|---|---|
| +8.7 (15) | −2.6 (9) | −4.3 (6) | −0.3 (8) | −4.6 (5) | +4.6 (9) | −2.9 (5) | +3.2 (6) | +2.4 (6) | +2.4 (7) |

The picture is stable across every variant tried: the book makes money in
trending windows (+15 % in W04 and W06, +8.7 % in W11), loses 2–5 % in chop and
crash windows, and the *average* is positive while the *worst* window is not.
Passing 20/20 requires the median window to be +10 % with ≥ 15 trades; the
distribution above needs roughly a 5–10× improvement in per-window ROI, i.e. a
per-trade net edge of ≈ +0.6R where the measured best family gross edge is
+0.24R before friction.

This is consistent with the repository's own history: `rp2_round12_results.json`
0/20, `Engine/oos_18asset_results.json` and `Engine/s1_trend_following_suite.py`
scorecards also fail out-of-sample.

Caveat on method, stated plainly: the 20 windows are *out of sample for the gate*
(every model is fitted only on prior data), but the handful of design choices made
late — expectancy label vs direction, carried breaks, hard tide filter or not,
`--sel-per-window` — were compared on these same 20 windows, so the pass counts
above are optimistic relative to a truly untouched holdout. The comparison across
runs is still informative because each run's trades are genuine walk-forward
decisions, but a 2/20 or 1/20 result should not be read as "3 % from passing".

---

## 5. What to do with this

1. **Keep the level engine, drop the POC reversion block.** `brk_ath`,
   `x_ath_brk_lowvol`, `brk_pwh_cascade`, `brk_pmh`, `brk_multi_lvl` are the only
   families with edge above the control. They belong in the meta-label ensemble
   as *features* (distance to ATH / period highs, bars-since-ATH, low-vol
   compression flags) rather than as standalone strategies.
2. **Costs, not alpha, are the binding constraint.** On a realistic retail
   taker assumption (≈15 bps) `brk_ath` (+0.101 R) and `x_ath_brk_lowvol`
   (+0.164 R) turn positive per trade. If the mandate's 41 bps floor is meant as
   a safety margin rather than a forecast, it should be re-derived from actual
   fills; if it is the contract, no geometric family can pass.
3. **Fix the geometry.** A 4R net target with a ≥1.2 % stop needs a ~5 % move;
   the measured impulse has decayed by 24 h for everything except ATH/cascade
   breaks. Either widen the horizon for those two families (288–672 bars, where
   gross R is largest) or accept a lower target with more trades.
4. **The ML gate needs different labels/features.** Predicting "profitable under
   a 4R barrier" yields AUC ≈ 0.52 because the label is dominated by whether a
   large move happened at all. Better targets: predict the *path* (MFE/MAE ratio
   within N bars), predict `P(MFE ≥ 2R | MAE ≤ 1R)`, or model the cross-section
   (rank which symbol breaks out) instead of the time series.
5. **Regime conditioning is mandatory.** Long high-break families are positive
   in bull macro tides and roughly flat/negative in bear tides; a book that is
   long-only through May 2021, Jan 2022, May/June 2022, Nov 2022 and Aug 2024
   pays the DD budget for nothing.

## 6. Reproducing

```bash
python -m Engine.levels_poc_lab.data                       # profile validation audit
python -m Engine.levels_poc_lab.impulse                    # directional impulse study
python -m Engine.levels_poc_lab.splits                     # regime-conditional splits
python -m Engine.levels_poc_lab.run_study --target-r 4 --horizon 288   # barrier net R per family
python -m Engine.levels_poc_lab.frontier                   # cost frontier / break-even friction
python -m Engine.levels_poc_lab.run_portfolio              # geometric scorecard, 20 windows
python -m Engine.levels_poc_lab.flow                       # footprint-ladder flow features
python -m Engine.levels_poc_lab.run_ml --cost-profile certified   # ML-gated scorecard
python -m Engine.levels_poc_lab.run_ml --cost-profile zero        # cost-free ceiling
python -m Engine.levels_poc_lab.run_ml --macro-filter --label-r 1.0 --cands-per-month 60 \
    --out lpl_ml_regime        # expectancy-labelled gate + tide filter
python -m Engine.levels_poc_lab.run_ml --label-r 1.0 --sel-per-window 60 --pending 24 \
    --out lpl_ml_soft          # best net result: carried breaks, count-based selection
python scratch/label_check.py   # objective-function comparison (direction vs expectancy)
python scratch/auc_check.py     # order-flow feature check (with/without ladder features)
```

Outputs are written to `scratch/lpl_*.{json,csv,md}` (git-ignored, run artifacts).
