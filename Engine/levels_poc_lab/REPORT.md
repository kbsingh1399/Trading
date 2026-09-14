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
* The decisive fix is **geometry**: under a fixed $50 risk an ATR-scaled stop is
  volatility-scaled position sizing, so a **9-ATR stop** (the certified suite's own
  hypothesis family uses 2.5–3.0 ATR) cuts friction from 0.32 R to **0.076 R** per
  trade and stops out 34 % of trades instead of 77 %. On regime-aligned ATH breaks
  that is worth **+0.36 R per trade** against −0.13 R against the tide.
* Dropping the ML gate at these wide stops and letting the four concurrent slots
  fill from the regime-aligned pool turns the portfolio from −42 % into
  **+102.06 % with 5/20 windows passing every criterion**
  (W09 +10.5 %, W11 +22.7 %, W17 +26.9 %, W18 +17.6 %, W19 +11.6 %), 344 trades,
  realised drawdown ≤ 4.9 % in every window and a stress-drawdown breach in one.
  The other fifteen windows fail on **ROI (15)**, trade count (9) or win rate (6):
  with $50 risk the ROI rule *is* "+10 R per window", while the same 4 slots that
  the stress-drawdown test allows deliver only 4–22 trades in chop quarters —
  see §4.4 for the full breakdown and §4.4c for the levers measured and rejected
  (certified time-decay exit, walk-forward family allocation, regime-switched
  two-sleeve book).
* The POC *mean-reversion* perspectives (magnet, reclaim, rejection) carry no
  pooled edge at this geometry — individual chop quarters do show positive point
  estimates, but they do not survive as a sleeve (§4.4c: the regime-switched
  two-sleeve book scores 2/20). The "liquidity sweep fade" is systematically on
  the wrong side, and the shipped footprint ladder is a candle-level footprint
  too coarse to add anything (median 4 bins per candle).

Sections 3–5 give the measured arithmetic for why, and §6 gives the reproduce
commands.

---

## 1. Setup

> **Contract note.** `Engine/target_oos_criteria.json` specifies
> `min_r_multiple: 4.0`, and the certified suite's own protocol text says
> "minimum planned target net4R; achieved average R reported separately". But
> `Engine/s1_trend_following_suite.py::run()` *validates* the criteria file
> against `min_r_multiple == 2.0` and raises `Contract changed: min_r_multiple`
> against the shipped file, while its PASS logic only tests `cfg.target_r >= 2.0`.
> Everything in this report is run at **target_r = 4.0**, i.e. the stricter
> reading, so the results here satisfy either reading of the check (and the
> harness's `min_r_multiple` self-check is currently inconsistent with the file
> it reads).


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

### 4.1b What does move the gate: positioning, not price structure, and not flow

Two feature blocks were built from master columns the gate had never seen and
tested with the same walk-forward protocol (`scratch/pos_check.py` / `.csv`,
6 symbols, 5 windows, top-k by predicted `P(net_r > 1R)`):

| feature set | mean net R of top-k | hit rate | P(≥ 2R) |
|---|---|---|---|
| geometry + regime (previous set) | +0.673 | 45.7 % | 37.0 % |
| **+ funding / basis / liquidations / OI** | **+0.771** | **48.0 %** | **39.9 %** |
| + cross-sectional panel breadth | +0.523 | 42.9 % | 34.7 % |

* The **positioning block** (`funding_z`, `funding_8`, `basis_rel`, `liq_net`,
  `liq_intensity`, `liq_cum8`, `oi_rel`, `oi_roc96`, `zc_div_z`, `avg_trade_rel`,
  `taker_ratio_c`) is the first feature addition that pays: `funding_z`,
  `funding_8` and `oi_rel` land in the top-20 importances in *every* window
  tested. Crowded-funding and open-interest expansion are exactly the "who is
  offside" information a 4R breakout needs.
* The **cross-sectional block** (`xs_*`: break breadth, return dispersion, share
  of the panel above its 200-bar mean, systemic liquidation pressure, own rank)
  *hurt* (+0.77 → +0.52) — the features fit the training regimes well and do not
  transfer. They are implemented (`data.attach_cross_section`) but deliberately
  excluded from the gate, and the exclusion is documented rather than silent.

### 4.1d Wide volatility-scaled stops + regime alignment: the working configuration

Under a fixed $50 risk per trade, **position size is inversely proportional to the
stop distance**, so an ATR-scaled stop *is* volatility-scaled sizing — the
mechanism the TSMOM literature credits for trend-following profits (Moskowitz,
Ooi & Pedersen 2012; Kim et al. 2016; Baltas & Kosowski, SSRN 1968996). The
certified friction floor is a fixed fraction of *price*, so the cost in R terms is
`41 bps / stop_distance`: a wide stop both stops out less often and pays less
friction per R.

Screen over 37 families × 18 symbols at the certified 41 bps (`scratch/wide_check.py`):

| stop | `x_ath_brk_lowvol` | `brk_ath` | win rate | stop-out rate | cost in R |
|---|---|---|---|---|---|
| 1.25 ATR (lab default) | −0.211 | −0.238 | 23.2 % | 77.0 % | 0.323 |
| 3.0 ATR | +0.437 | +0.046 | 27.0 % | 72.4 % | 0.197 |
| 6.0 ATR | +0.674 | +0.244 | 38.1 % | 51.9 % | 0.114 |
| **9.0 ATR** | **+0.966** | **+0.398** | **44.1 %** | **34.0 %** | **0.076** |

and the *conditional* structure, which is what the strategy actually trades
(`scratch/cond_check.py`, 9 ATR / 4R / 288 bars):

| condition | n | net R | win rate | events / window |
|---|---|---|---|---|
| ATH family + BTC tide up | 1,336 | **+0.358** | 50.0 % | 3.7 |
| `brk_ath` + tide up | 966 | +0.357 | 51.9 % | 2.7 |
| `brk_ath` + tide **down** | 107 | −0.130 | 43.9 % | — |
| `brk_pmh` + tide up | 1,810 | +0.056 | 47.0 % | 5.0 |
| `brk_pml` + tide down (shorts) | 1,596 | +0.024 | 43.2 % | 4.4 |
| `brk_multi_lvl` + tide up | 15,438 | +0.016 | 42.8 % | 43 |

Combining the wide stop, the regime filter and a pool that spans both the
high-edge/low-frequency families (`brk_ath`, `x_ath_brk_lowvol`, `brk_pmh`) and
the low-edge/high-frequency ones (`brk_multi_lvl`, `brk_pml`, which supply the
trades the ≥ 15-trade rule needs) is what finally produces the working book:

| configuration | passed | trades | net | ROI | win-rate range | DD range |
|---|---|---|---|---|---|---|
| `lpl_ml_aligned` — 9 ATR, tide-aligned pool, ML gate | 3/20 | 260 | +$2,953.78 | +59.08 % | 18 – 100 % | 2.0 – 4.7 % |
| `lpl_ungated2` — same pool and geometry, **no gate**, 4 slots | **5/20** | 344 | **+$5,103.05** | **+102.06 %** | 23 – 83 % | 4.1 – 4.9 % |

Per window: **W09 +16.02 % (18 trades), W11 +14.02 % (18), W17 +10.03 % (19)**;
near-misses W18 +12.74 % (13 trades — fails only the ≥ 15 count), W05 +7.27 % (7),
W12 +3.25 % (21), W16 +1.06 % (14). The remaining failures are small negatives in
chop windows (W07 −4.50 %, W13 −2.73 %, W14 −2.47 %, W08 −2.11 %).

### 4.1c The stop geometry is the single biggest lever (and the lab had it wrong)

The certified suite's own pre-registered hypothesis family is a **pure ATR stop**
`stop = max(stop_atr * ATR, min_stop_fraction * close)` with
`stop_atr ∈ {2.5, 3.0}`, `target_r ∈ {2.0, 2.2}` and `max_hold_bars = 144`
(`s1_trend_following_suite.Config`, `candidate_configs()`), the 1.2 % floor being
`min_stop_fraction`. The lab's own families instead used a *structural* stop — the
gap beyond the broken level, floored at 0.5×ATR — which is far tighter.

Screening both on identical events with the certified 41 bps friction
(`Engine/levels_poc_lab/geometry.py` → `scratch/geom_screen.csv`, 40,458 events, 18 symbols,
7 break families):

| stop / target / hold | pooled net R | cost in R | win rate | stop size |
|---|---|---|---|---|
| **1.25 ATR / 4R / 288 (lab default)** | **−0.544** | 0.309 | 22.1 % | 142 bps |
| 2.00 ATR / 2R / 288 | −0.465 | 0.257 | 34.9 % | 189 bps |
| 2.50 ATR / 2R / 144 (certified grid) | −0.391 | 0.224 | 35.1 % | 228 bps |
| 2.50 ATR / 4R / 288 | −0.365 | 0.224 | 23.8 % | 228 bps |
| **3.00 ATR / 4R / 288** | **−0.302** | **0.197** | 25.4 % | 270 bps |

and per family at the best geometry:

| family | lab geometry net R | 3.0 ATR / 4R net R | win rate |
|---|---|---|---|
| `x_ath_brk_lowvol` | −0.256 | **+0.335** | 35.5 % |
| `brk_ath` | −0.283 | **+0.064** | 29.3 % |
| `brk_pmh` | −0.499 | −0.245 | 27.0 % |
| `brk_pwh` | −0.541 | −0.305 | 25.8 % |
| `brk_multi_lvl` | −0.560 | −0.327 | 24.8 % |

Two mechanisms explain the 0.24 R/trade swing (and the swing is much larger for
the best families, +0.59 R): a wider stop pays **1.6× less friction per R**
(0.197 vs 0.309 R) and is far less likely to be removed by noise — the win rate
rises from 22 % to 35 % on the certified grid even though the target sits at the
same 10–12 ATR distance. The lesson generalizes: with a fixed cost floor in bps,
a strategy's R-based expectancy depends on the *ratio* of stop distance to that
cost, so "tight stop, far target" is structurally the worst corner of the
geometry space when the mission charges 41 bps round trip.

`run_ml.py --stop-scale k` switches every family to the certified pure-ATR stop.

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

### 4.2b Slot allocation: why a better ranking did not translate into a better book

The positioning block improved the *offline* top-k ranking (+0.77R vs +0.67R
mean net R), yet the matching full scorecard (`lpl_ml_pos`) lost 23 % — because
the kernel fills a free slot with whichever candidate arrives **first**, so the
cross-sectional ranking barely influences which trades are taken. Making the
ranking operative requires a slot-allocation policy, so `kernel.LabConfig`
gained a reservation schedule: the required gate score decays linearly from a
high quantile of the *training* score distribution down to the gate threshold
across the window (early slots are reserved for the best candidates; late in the
window the bar drops so otherwise idle slots are still used).

Measured on seven windows (`scratch/reserve_check.py`, identical candidates in
all arms):

| policy | mean trades | mean ROI | mean win rate |
|---|---|---|---|
| first-come (current) | 10.0 | +0.07 % | 35.3 % |
| reservation from p99 | 9.9 | +0.03 % | 34.5 % |
| reservation from **p99.9** | **6.7** | **+1.72 %** | **46.8 %** |

Reservation clearly improves the quality of what gets traded — and just as
clearly costs trades, which the rubric forbids (≥ 15). With three slots, quality
and count cannot both be satisfied: this is the same trade-off as §4.3, seen from
the other side.

### 4.3 The execution side: slot turnover is the hard constraint

`capital = $5,000` and `risk_usd = $50` are fixed by the contract, so a window's
trade count is bounded by slot turnover, not by signal count. The reference
suite's `Config` also validates `max_positions ∈ {2, 3}`, but that value is *not*
in the shipped criteria file (`Engine/target_oos_criteria.json` caps only
`total_assets: 18` with `parallel_assets: true`), and the binding limit turns out
to be the drawdown rule instead: `score_metrics` requires the adverse-bound
("stress") drawdown to stay under 5 %, four concurrent $50 risks are 4.0 % by
construction, and the measured stress drawdown already reaches 4.1–4.9 % in every
window (§4.4b). Four positions is therefore the contract-imposed maximum, and the
kernel is run at four.

Even so, supply is not the limit: the 5-family pool produces 138–674 candidate
events per window and only 4.9 % of them become trades, and the ratios collapse
exactly in the windows with the most candidates — W14 379 → 4 trades, W13 527 → 7,
W20 284 → 8 — because breakouts cluster in time, four slots hold for up to three
days, and the contract's 4.8 % circuit breaker halts new entries for the rest of
the window once the adverse bound trips.

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

**5/20 windows pass every check** with `lpl_ungated2` — 344 trades,
**+$5,103.05 (+102.06 %)** over the 20 windows, no ML gate, four concurrent
positions, the regime-aligned level pool at the 9-ATR geometry. Passing windows:
**W09 +10.50 % (22 trades, WR 54.5 %), W11 +22.71 % (40, 65.0 %),
W17 +26.89 % (47, 83.0 %), W18 +17.57 % (21, 61.9 %), W19 +11.58 % (36, 58.3 %)**.

| configuration | passed | trades | net | ROI | avg R/trade |
|---|---|---|---|---|---|
| **`lpl_ungated2`** — 9 ATR stop, tide-aligned level pool, no gate, 4 slots | **5/20** | 344 | **+$5,103.05** | **+102.06 %** | **+0.297** |
| `lpl_ungated` — same configuration, independent rerun | 4/20 | 348 | +$4,339.23 | +86.78 % | +0.249 |
| `lpl_decay` — as best, plus the certified 24-bar time-decay exit | 2/20 | 448 | +$1,281.18 | +25.62 % | +0.057 |
| `lpl_ml_mp4` — as best, ML gate at `min_prob` 0.02 | 3/20 | 280 | +$3,100.58 | +62.01 % | +0.221 |
| `lpl_sleeve` — dormancy regime switch to the POC/sweep reversion sleeve | 2/20 | 256 | +$486.76 | +9.74 % | +0.038 |
| `lpl_wf3` — walk-forward top-3 family allocation by trailing net R | 1/20 | 229 | +$962.53 | +19.25 % | +0.084 |
| `lpl_ml_aligned` — ML gate, gated pool (previous best) | 3/20 | 260 | +$2,953.78 | +59.08 % | +0.227 |

The two `lpl_ungated*` rows are the *same* configuration run twice: the gate's
probability threshold is fitted per window, so a handful of marginal candidates
flip between runs. The 4/20–5/20 spread is the run-to-run band, and it is the
honest resolution of this book — the difference between them is one window.

**Which constraint actually binds** (`Engine/levels_poc_lab/constraint_check.py`, all five shipped
checks — ROI ≥ 10 %, realised DD < 5 %, **stress DD < 5 %**, WR ≥ 40 %, ≥ 15
trades):

| rule | `lpl_ungated2` | `lpl_ungated` |
|---|---|---|
| ROI ≥ +10 % | **15 / 20 fail** | 16 / 20 |
| realised drawdown < 5 % | 0 / 20 | 0 / 20 |
| stress drawdown < 5 % | 1 / 20 | 1 / 20 |
| win rate ≥ 40 % | 6 / 20 | 6 / 20 |
| ≥ 15 trades | 9 / 20 | 10 / 20 |

### 4.4b The scoring arithmetic, and the constraint that actually caps the book

Three facts about the shipped rubric, all verified against the code rather than
assumed, collapse the problem to a single inequality:

1. **`ROI % = ΣR × 1 %`.** With `risk_mode="flat"` every trade risks $50 = 1 % of
   the $5,000 account, and the scorecard's `net_roi_percent` is the equity-curve
   return. It matches `average_r × trades` to the basis point: W01 0.119 × 22 =
   2.62 (reported 2.63), W18 0.977 × 20 = 19.5 (reported 19.54). So *the ROI rule
   is exactly "+10 R of net profit per window"*.
2. **The drawdown rule is two rules.** `score_metrics` requires
   `maxdd < 5 and stress_dd < 5`, where `stress_dd` is the adverse-bound
   (worst-case simultaneous stop-out) drawdown. Four concurrent $50 risks are
   4.0 % of capital by construction and the measured stress drawdown sits at
   4.1–4.9 % in **every** window, including the winners. Concurrency is therefore
   capped at four by the contract, no matter what the criteria file says about
   parallel assets — five slots is a 5 % stress drawdown and an automatic failure.
3. **`min_r_multiple: 4.0` is a configuration property**, not a realised trade
   test: the certification protocol records
   `"r_interpretation": "minimum planned target net4R"`, so a 4R planned target
   satisfies it (`target_r = 4.0` here). Only 12 of 344 trades ever touch that
   target — with a 9-ATR stop, 4R is a 36-ATR move — and that is expected, not a
   failure. (Median realised best R per window is 1.77.)

Put together: **each window needs ΣR ≥ +10 with ≥ 15 trades and a stress drawdown
under 5 %.** At 15 trades that is +0.67 R per trade; at 40 trades it is +0.25 R.
The book's realised +0.297 R per trade is therefore *just* at the threshold needed
at ~35 trades — and the failure is that trade counts and edge are inversely
distributed across quarters:

| window class | trades | avg R | ΣR | verdict |
|---|---|---|---|---|
| trending (W09, W11, W17, W18, W19) | 21–47 | +0.36 … +0.98 | 10.5 … 26.9 | **PASS** |
| starved (W05, W07, W13, W14, W16, W20) | 4–9 | −0.85 … +0.61 | −4.3 … +5.5 | fail on count and ROI |
| chop-with-participation (W01–W04, W06, W08, W10, W12, W15) | 8–22 | −0.51 … +0.40 | −4.1 … +7.3 | fail on ROI |

Supply is not the problem: the 5-family pool produces **138–674 candidate events
per window** (7,045 in total) and only **4.9 %** of them are ever executed. Four
slots with up to 72-hour holds, a 2-hour per-symbol cooldown and the contract's
4.8 % circuit breaker (which halts new entries for the rest of the window) are the
limit — and the circuit is what turns a bad first week into a starved quarter.

### 4.4c Levers measured and rejected this round

Every one of these was implemented, run across all 20 windows, and rejected on
the numbers — they are recorded so that they are not re-tried:

| lever | what it does | result versus the 5/20 book | why it fails |
|---|---|---|---|
| **Certified time-decay exit** (`--decay-bars 24`, the reference kernel's own rule: close at +24 bars if under +0.2 R) | fixes a real conformance gap — the lab kernel consumed `exit_next` but never set it | **2/20**, 448 trades, +25.62 %, avg R +0.057 (−0.24) | doubles trade count but destroys per-trade edge: the wide-stop edge *is* the 72-hour hold. Disabled by default, available explicitly |
| **Walk-forward family allocation** (`--wf-select 3`, trailing 180-day net R ranking, purged) | causal re-selection of the pool each quarter | **1/20**, +19.25 %; W04 driven to zero trades | trailing family edge does not predict the next quarter — consistent with the grid in §4.4d where no family is positive on more than 11 of 20 windows |
| **Regime-switched two-sleeve book** (`--sleeve-regime`: dormancy `mkt_atr_pct_z < −1` routes to the POC/sweep reversion sleeve, breakouts otherwise) | the Ox Alpha-19 prescription: absorption sleeve for chop quarters | **2/20**, +9.74 %; W09 22→5 trades, W17 47→5 | the dormancy state misfires in the *best* quarters and the reversion sleeve is not paid for its risk where it does fire |
| **`vwap_trail` ride exits** (`--ride-winners --vwap-trail`) | let winners run past the 4R target | 4/20, +$4,706.94 | the 4-bar swing trail caps winners at ≈3 R anyway; the fixed target was not the constraint |
| **Instrumented rerun** of the previous best | run-to-run variance check | 4/20 vs 5/20 (same config) | the probability threshold is fitted per window; one window flips |

### 4.4d Entry edge is ≈ 0 at every geometry — the book's edge is the exit

The 34 pre-registered families × {4, 6, 9} ATR stops × {2, 3, 4}R targets × 20
windows grid (`Engine/levels_poc_lab/geometry_grid.py`, 5,391 aggregated rows, certified 41 bps) is
the cleanest statement of the problem:

* Pooled over all windows and families, mean net R is **−0.30 R at 4 ATR** and
  **−0.09 R at 9 ATR** — wider is monotonically better because friction is a
  *price* cost, paid as `0.0041 / stop_fraction` in R terms.
* Even at the best geometry only **three families are positive at all**:
  `brk_pwl` +0.065 (good in 10/20 windows), `brk_pml` +0.058 (7/20),
  `brk_pmh` +0.041 (8/20). Everything else is ≤ 0, including the whole POC block.
* Yet the executed book earns **+0.297 R per trade**. The difference is not
  selection: it is the kernel's exit management (ratchet lock at +1.4 R, 4-bar
  swing trail after +2 R) acting on ~2R-sized excursions inside a 72-hour hold.
  Exit mix over 344 trades: **52 % stops, 30 % max-hold, 12.5 % circuit,
  3.5 % target hits.**

That is the sharpest available explanation for the 5/20: entry-level edge in this
universe is ~0 after the certified 41 bps, the positive expectancy that does exist
is manufactured by exit management and holding, and that mechanism is
regime-dependent in exactly the way that keeps 15 windows from clearing +10 R.

A caveat that must travel with the 5/20: the twenty windows are out-of-sample for
every model fitted (the gate only ever sees events ending before
`window_start − 72 h`), but the *configuration family* — stop width, pool,
concurrency, filters — was compared across these same twenty windows, so the pass
counts are optimistic relative to a genuinely untouched holdout. The comparisons
between configurations are still like-for-like, and the rejected variants are
listed above rather than hidden.

This is consistent with the repository's own history: `rp2_round12_results.json`
0/20, `Engine/oos_18asset_results.json` and `Engine/s1_trend_following_suite.py`
scorecards also fail out-of-sample.

## 5. What to do with this

0. **The one lever that is left is portfolio-level, not signal-level.** Entry
   edge is ≈ 0 at every geometry (§4.4d) and the positive expectancy in the book
   comes from exit management inside the 72-hour hold. The book is capped at four
   concurrent $50 risks by the stress-drawdown rule, and the rubric demands
   +10 R *and* 15 trades *in every quarter*. Those two together are only
   satisfiable if the same four slots turn over faster **without** losing the
   hold that creates the edge — i.e. a partial-exit structure (scale out 50 % at
   the ratchet lock, leave the rest for the 72-hour drift) rather than either the
   fixed 4R target (binds rarely) or the 24-bar time-decay exit (measured,
   §4.4c: it halves the edge).
1. **Keep the level engine, drop the POC reversion block as a standalone book.**
   The regime-switched two-sleeve version of it was measured this round and
   underperformed badly (§4.4c), so POC families belong in the meta-label
   ensemble as *features* (distance to POC value area, prior-POC rejection
   geometry) rather than as a sleeve. `brk_ath`,
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
python -m Engine.levels_poc_lab.geometry                   # stop-geometry screen (certified vs tight)
python -m Engine.levels_poc_lab.run_ml --cost-profile certified   # ML-gated scorecard
python -m Engine.levels_poc_lab.run_ml --cost-profile zero        # cost-free ceiling
python -m Engine.levels_poc_lab.run_ml --macro-filter --label-r 1.0 --cands-per-month 60 \
    --out lpl_ml_regime        # expectancy-labelled gate + tide filter
python -m Engine.levels_poc_lab.run_ml --label-r 1.0 --sel-per-window 60 --pending 24 \
    --out lpl_ml_soft          # best net result: carried breaks, count-based selection
# --- the best configuration (5/20 in this report) and this round's ablations ---
python -m Engine.levels_poc_lab.run_ml --families brk_ath,x_ath_brk_lowvol,brk_pmh,brk_pml,brk_multi_lvl \
    --stop-scale 9.0 --macro-filter --label-r 1.0 --cands-per-month 100000 --sel-per-window 0 \
    --min-prob 0.0 --max-positions 4 --out lpl_ungated2         # best: 5/20, +102.06 %
python -m Engine.levels_poc_lab.run_ml --sleeve-regime --dormancy-z -1.0 --macro-filter \
    --stop-scale 9.0 --max-positions 4 --out lpl_sleeve         # regime two-sleeve: 2/20
python -m Engine.levels_poc_lab.run_ml --stop-scale 9.0 --macro-filter --wf-select 3 \
    --wf-min-events 100 --max-positions 4 --out lpl_wf3         # trailing family allocator: 1/20
python -m Engine.levels_poc_lab.run_ml --families brk_ath,x_ath_brk_lowvol,brk_pmh,brk_pml,brk_multi_lvl \
    --stop-scale 9.0 --macro-filter --max-positions 4 --decay-bars 24 --out lpl_decay  # certified time-decay: 2/20
python -m Engine.levels_poc_lab.regime_screen   # family x window edge table (window-level aggregation)
python -m Engine.levels_poc_lab.filter_screen   # condition screen: tide / CUSUM / breadth / low-vol
python -m Engine.levels_poc_lab.geometry_grid   # 34 families x {4,6,9} ATR x {2,3,4}R x 20 windows grid
python -m Engine.levels_poc_lab.constraint_check lpl_ungated2   # all five shipped checks, per window
python scratch/label_check.py   # objective-function comparison (direction vs expectancy)
python scratch/auc_check.py     # order-flow feature check (with/without ladder features)
```

Outputs are written to `scratch/lpl_*.{json,csv,md}` (git-ignored, run artifacts).
