# Levels and Point-of-Control strategies — literature and design rationale

Scope: causal, walk-forward research on **prior week / month high-low, all-time
high, prior-day high-low, and volume-profile Point of Control (POC)** strategies
for Binance USDT-M perpetuals (15m), evaluated on the 20 pre-registered OOS
windows in `Engine/oos_windows_20.json`.

Code: `Engine/levels_poc_lab/` (data, geometry, event study, execution kernel,
ML gate). Results: `Engine/levels_poc_lab/REPORT.md`.

---

## 1. What the literature claims

### 1.1 Reference-price levels (previous highs)

| Source | Claim | Relevance |
|---|---|---|
| George & Hwang (2004), *The 52-Week High and Momentum Investing*, J. Finance | Nearness to the 52-week high **dominates** past-return momentum as a return predictor; the effect is a *reference-price/anchor* effect and does **not** reverse long-run | Justifies testing breaks of period highs as a distinct concept from trend momentum |
| Marquette working paper, *Momentum Crashes and the 52-Week High* | Nearness-to-high explains momentum crashes; stocks *far* from highs outperform during rebounds | Warns that "high-break" signals behave asymmetrically across regimes — must be conditioned on market state |
| Practitioner literature (52-week-high breakout) | Durable breakouts share: volume above average, base/consolidation before the break, close near the bar high; false breakouts show thin volume and immediate reversal | Defines the volume + close-location confirmations used here |

### 1.2 Volume profile / POC

Market-profile theory (Steidlmayer; Dalton, *Markets in Profile*) treats the
session volume distribution as the market's search for value:

* **POC** — price with the most traded volume; "fair value" and a magnet;
* **Value area (VAH/VAL)** — ~70 % of volume; edges act as support/resistance;
* **HVN / LVN** — acceptance vs rejection zones; price traverses LVNs quickly;
* **Naked POC** — an untested prior-session POC is often treated as a magnet;
* **POC migration** — a rising/falling POC is read as bullish/bearish rotation.

Practitioner statistics often quoted (e.g. Dalton: prior-day POC is revisited in
~80 % of sessions; Axia Futures 2020 ES study: value-edge→POC reversion 62 % win
rate over 800 trades; CBOT: non-overlapping value areas precede trend days 71 %
of the time). These are **not peer-reviewed**, and they are the exact claims this
study tests rather than assumes.

### 1.3 Liquidity sweeps / false breakouts

ICT/SMC-style literature and practitioner research describe a *sweep* (stop run)
where price briefly violates a level, triggers clustered stops, then reverses.
Reported fakeout rates are high (BTC futures ~65 %, gold ~62 %, EURUSD ~58 %,
ES ~54 %), with the "volume tell" that a break printing < 1.5–2× the 20-period
average volume is more likely a sweep than genuine expansion.

This predicts that *fading* swept period highs/lows is the profitable side. The
empirical result in this repository is the opposite (Section 4.3 of REPORT.md).

---

### 1.4 Meta-labelling: the prediction target is a design choice

The literature on side-prediction is not the same as the literature on
*expectancy* prediction. Under a barrier geometry (fixed R target, structural stop,
time stop) the classifier label `net_r > 0` is dominated by time-stop scratches:
in our event pool a set with a 58 % "win rate" still averages −0.19 R, because
most wins are tiny and the losses are full stops. Refitting the identical feature
set on `net_r > 1R` ("did this become a meaningful win") lifts the realized mean
net R of the selected candidates from +0.23 R to +0.67 R and the share of ≥ 2 R
outcomes from 10 % to 37 % (≈ +10 % ROI at 15 trades and 1 % risk). This is the
meta-labelling framing of Lopez de Prado (2018, *Advances in Financial Machine
Learning*, ch. 3): a primary model proposes events, a secondary model learns the
*conditional payoff*, and the label threshold encodes the trading objective
rather than the sign of the move. Two corollaries used in this lab: (i) never
judge a gate by AUC against the sign label alone — judge it by the realized R of
what it selects; (ii) with a hard concurrency cap (the certified contract allows
2–3 concurrent positions), ranking quality matters more than signal count, since
only the best-ranked candidates can occupy a slot.

## 2. Data reality check

The repo ships `*_15m_footprint_ladder.parquet` with one `is_poc` rung per 15m
candle. The repository's own audits
(`docs/PIPELINE_CERTIFICATION_ROUND5.md`, `docs/PIPELINE_REREVIEW_ADDENDUM.md`)
certify that the ladder rungs are **synthesised from the candle**
(`poc_source = OHLC_APPROX`), i.e. the ladder POC is a deterministic transform of
OHLC rather than a tick-exact volume profile.

Consequences adopted in this lab:

1. The ladder POC is **not** used as a feature. A session volume profile is
   **reconstructed** from the 15m OHLCV bars using a uniform-in-log-price
   intra-bar distribution on a 5 bp price grid (`levels.profile_series`), which
   also yields developing VAH/VAL/LVN and POC migration.
2. `levels.validate_profile()` quantifies the disagreement with the shipped
   ladder POC as an audit (median relative error 0.39 % BTC, 0.54 % ETH,
   0.83 % SOL, 0.71 % DOGE; 18–37 % of sessions within 25 bp). The two
   estimators disagree materially, so POC results must be read as
   *reconstruction-conditional*.
3. `fp_poc_vol_ratio`, `fp_stacked_*` (constant 0.0) and the ladder POC share
   are excluded from every feature set.

---

## 3. Pre-registered families (nothing is fitted)

37 families in four groups (`signals.default_specs`). Parameters are fixed
a priori from the literature, not optimised per window:

* **level_break (10)** — close breaks PWH/PWL, PMH/PML, PQH, ATH, PDH/PDL with
  volume ≥ 1.2× the 96-bar mean and a close in the strongest 45 % of the bar's
  range; plus week-high cascade (week break inside the month-high band), retest,
  and multi-level cascade variants.
* **level_sweep (7)** — sweep-and-reclaim of PWH/PWL/PMH/PML/PDH/PDL/ATH: pierce
  the level, close back inside, stop 0.25 ATR beyond the sweep extreme.
* **poc (13)** — reclaim/loss of the developing POC, prior-POC reclaim and
  rejection (both directions), ≥2σ POC magnet reversion, value-area breakouts,
  POC migration, naked-POC approaches, LVN reclaim.
* **confluence (4)** — week-high sweep at value, week-low sweep at value,
  week-high break outside value, ATH break in a compressed volatility regime.

Execution geometry (certified contract): stop = max(structural distance, 0.5–1.0
ATR, 1.2 % of price); target = 4R **net** of costs; max hold 288 bars (3 days);
41 bps round-trip friction floor; next-open fills; stop-first bar handling.

---

## 4. Method summary

1. **Impulse study** (`impulse.py`) — mean forward return after each event at
   4/24/96/288 bars, in ATR units, with t-statistics. Measures *direction only*.
2. **Conditional splits** (`splits.py`) — the same, conditioned on side, BTC
   4h macro tide, the symbol's own trend anchor, and ATR regime.
3. **Barrier event study** (`run_study.py`) — net R of the exact execution
   geometry per family, per OOS window.
4. **Random-entry control** — 2 % of volume-confirmed bars entered with the same
   stop/target geometry, to separate *level* information from generic drift.
5. **Cost frontier** (`frontier.py`) — gross mean R, net mean R at 0/10/20/30/41/
   60 bps, and the break-even friction per family.
6. **Portfolio walk-forward** (`run_portfolio.py`) — the certified event loop
   (next-open fills, stop-first bars, adverse-bound DD, funding, 3× gross cap,
   4.5 % circuit breaker) over all 20 windows.
7. **ML meta-labelling** (`run_ml.py`, `ml_gate.py`) — LightGBM probability that
   a candidate reaches a profitable exit, trained **only** on events ending
   before `window_start − 72 h`, threshold calibrated to a target candidate
   count per month, used as the cross-sectional ranking score.

## 5. What would have to be true for the mission to pass

Per window the criteria require +10 % ROI, ≤ 5 % DD, ≥ 40 % win rate, ≥ 15
trades and a ≥ 4R target. With 1 % risk per trade that is **+10R per month** at a
≥ 40 % hit rate on 4R targets — i.e. roughly +0.6R per trade with a 15-trade
month. Section 5 of REPORT.md shows the measured per-event edge in *price* terms
is 5–33 bps against a 41 bps cost, which is the binding constraint.

The walk-forward work since the first draft sharpened this into three separate
arithmetic constraints, all measured rather than assumed:

1. **Per-trade edge.** The best *gross* mean R of any of the 37 pre-registered
   families under the certified geometry is +0.241R (`x_ath_brk_lowvol`), and net
   of the 41 bps friction the whole family set is between −0.07R and −0.38R. The
   mission needs ≈ +0.6R net per trade. Re-weighting, re-thresholding or
   re-training the same 37 families cannot multiply a 0.24R gross edge by four;
   it needs information that isn't in the price/level/POC feature set. Adding
   every order-flow feature the shipped footprint ladder supports moved
   out-of-sample AUC by −0.005 to +0.004 (README §4.1), i.e. the exchange's own
   footprint is too coarse (median 4 bins per candle) to be that information.
2. **Trade count.** The certified contract fixes 2–3 concurrent positions and
   $50 risk per trade (`s1_trend_following_suite.Config` raises otherwise), so
   ≥ 15 trades per window requires slots to turn over roughly every two to three
   days *and* a still-valid candidate to be waiting whenever a slot frees.
   Measured execution ratios in the best configurations are 16 % (864 gated
   candidates → 134 trades), collapsing to 3–4 % in windows where breakouts
   cluster (W05 158 → 5). Carried-break candidates (`pending=24`) and
   count-based selection (`--sel-per-window`) attack exactly this constraint and
   are what moved the best configuration from 0/20 to 2/20 individual passes.
3. **Every window, not on average.** Even taking the top-15 gate-ranked
   candidates, out-of-sample mean net R is +2.7R in a trending window (W11) and
   −0.9R in a chop window (W07) with the *same* model and features. A 20/20
   requirement is a requirement that the ranking be positive in all 20 regimes;
   the measured per-window spread says it is not.

Conclusion: within the certified cost contract, the fixed $50 risk, the 2–3
position cap and a ≥ 4R target, the 20-window rubric is not jointly satisfiable
by level-break / sweep / POC strategies on this dataset. The honest levers are
(i) re-derive the 41 bps friction floor from actual fills (~15 bps retail taker
makes `brk_ath` and `x_ath_brk_lowvol` positive per trade), (ii) relax the
concurrency cap to let a diversified book hold more than three positions, or
(iii) restate the target as ≥ 2R with a matching hit-rate requirement, which is
the only region where the measured edge survives costs.
