# S1 TEARDOWN — Why the Engine Predicts Negative-Expectancy Entries

**Diagnostic only. No production code was changed. Nothing was "fixed".**

Scope: 52,252 S1 candidates, 18 symbols, 2020-09-01 → 2026-09-10, produced by
`label_triple_barriers_numba` exactly as `fast_numba_oos_engine.py:385` calls it.
Reproducer: `scratch/diag_s1_autopsy.py`; cached pool `scratch/diag_s1_pool.parquet`.

---

## 0. THE ONE-LINE ANSWER

**S1 is not picking losers. It is picking at random from a population with zero
gross edge, and every pick costs ~0.78 R to place.**

The entry signal's gross expectancy is **+0.0058 R** across 52,252 candidates
(t = +0.849, p = 0.396). Statistically, the signal is indistinguishable from a
coin flip. Transaction costs are **1.144 R per trade**. You are paying 197× the
size of the entire gross signal, every trade.

No model, gate, feature or regime filter can fix this. The ML layer was never
the problem, because there is nothing in these features to select.

---

## 1. MATHEMATICAL AUTOPSY OF THE BLEED

The labeler call is `(horizon=32, target=+3.0R, stop=−1.2R, ratchet 1.6→+0.35, 2.2→+1.4)`.
Decomposing all 52,252 candidates by their atomic exit:

| outcome | n | share | gross R | net R | net WR | contribution to mean |
|---|---|---|---|---|---|---|
| stop-out −1.20 | 29,765 | **56.96%** | −1.200 | −2.145 | 0.0% | **−1.2216** |
| be-lock +0.35 | 7,002 | 13.40% | +0.350 | **−0.605** | 7.4% | −0.0811 |
| profit-lock +1.40 | 7,255 | 13.88% | +1.400 | +0.457 | 85.1% | +0.0635 |
| target +3.00 | 7,657 | 14.65% | +3.000 | +2.029 | 98.1% | +0.2973 |
| horizon timeout | 573 | 1.10% | +0.772 | +0.016 | 50.3% | +0.0002 |
| **TOTAL** | **52,252** | 100% | **+0.0058** | **−1.1385** | **25.83%** | **−1.1385** |

Full decomposition of the mean:

```
mean gross exit_r        = +0.0058 R   <- the signal, cost-free
mean base friction 41bps = -0.9476 R
mean regime stress surch = -0.1967 R   <- the 1.5x / 3.0x multiplier
                       = -1.1385 R
```

Three things fall out of that table:

**(a) The bleed is not the stop.** 56.96% stop-outs contribute −1.22 R, but the
+3R target fires on 14.65% of trades and gives back +0.30 R. Gross, the grid
nets to zero. The loss is entirely the cost line.

**(b) The ratchet manufactures losing "winners".** 13.40% of trades exit at
+0.35 R gross — booked as a *win* by the geometry, a *loss* of −0.605 R after
friction. It takes +1.6 R of favourable excursion to lock +0.35 R, and friction
eats the lock entirely. (`label_y` itself is computed on `net_r > 0`, so the
label is honest — the *geometry* is what's broken.)

**(c) The asymmetry is inverted from what it looks like.** One stop-out
(−2.145 R net) erases 4.7 profit-lock wins or 3.5 be-lock wins.

**Per-symbol — is any symbol carrying it?** 9 of 18 have positive gross
expectancy; **2 of 18 clear |t| > 1.96, with opposite signs** (TRX +3.77,
ETH −2.25). At 18 unpre-specified tests that is multiple-testing noise. And the
clincher: **TRXUSDT has the only nominally significant positive gross expectancy
(+0.1235 R, t = +3.77) and a net expectancy of −1.9401 R — one of the worst in
the universe — because its friction is 1.6685 R.** Even where the signal is
real, it cannot pay for itself.

---

## 2. LABEL AUDIT — the grid is calibrated to a fair coin

You asked whether the profit targets are too tight or too loose versus the stop.
Neither. **The grid is tuned almost exactly to zero gross expectancy.**

- Naive grid arithmetic (TP 3.0 / SL 1.2) implies break-even win rate **28.57%**.
- The ratchet collapses the payoff, so the *realised* break-even is **42.61%**.
- The realised gross win rate is **42.82%**.

Those two numbers are 0.21 points apart. A barrier grid that lands within a
fifth of a point of its own break-even across 52,252 draws is not a mis-set
grid — it is a grid applied to a price series that behaves like a martingale on
this horizon. The labels are therefore **a 42.6%-biased coin**, and `label_y`
after friction is a 25.8%-biased coin.

**The 72-hour purge is adequate** (label horizon 32 × 15m = 8.0 h, so 64 h of
buffer) and **`FEATURE_COLS` contains no label column**. There is no label
leakage.

---

## 3. FEATURE AUDIT — no leakage, and almost no information

### 3a. Leakage: clean

| vector | test | verdict |
|---|---|---|
| `future_cvd_15m` (suspicious name) | corr with *previous* 1h return **+0.4111**; corr with *next* 1h return **−0.0077** | "future" = futures market, not future time. **CAUSAL** |
| `session_vah` / `session_val` | equals full-day max/min on only **0.17% / 0.43%** of rows; at 00:00–02:00 bars it already equals the day's final extreme on 0.10% / 0.44% | expanding anchor. **CAUSAL** |
| purge vs horizon | 72 h purge, 8 h label reach | **ADEQUATE** |
| label columns in `FEATURE_COLS` | none | **CLEAN** |

**No leakage. The features are honest.** That is the bad news, not the good news.

### 3b. Two of the 19 features are one feature

`corr(zc_norm, sf_div) = 0.99983` across all BTC 15m bars, and **1.0000 on the
candidate subset** (where the `clip(-3, 3)` saturates both). They are distinct
raw columns (`zc_div` vs `spot_cvd_15m − future_cvd_15m`, max deviation 2,880),
but after division by the same `volume_base` they are numerically
indistinguishable — median absolute deviation between the raw pair is 0.0. The
ridge sees two copies of one direction; LightGBM sees two of 19 splittable
columns. **One of the 19 feature slots is wasted, and the "21-feature orderflow
space" is really 18.**

### 3c. One feature is non-stationary in a way that corrupts the entry filter

`vwap_zscore` is an **expanding session z-score**, so its scale grows through
the day:

| hour | mean &#124;z&#124; | sd(z) | P(z < −0.4) |
|---|---|---|---|
| 00 | 0.377 | 0.540 | 16.2% |
| 04 | 0.810 | 1.079 | 31.5% |
| 08 | 1.647 | 2.040 | 41.6% |
| 16 | 1.897 | 2.336 | 43.2% |
| 23 | 2.655 | 3.415 | 42.0% |

The entry filter `vwap_z < −0.4` is therefore **not a stationary threshold** —
it admits 16% of bars at midnight and 42% by mid-session. The candidate
population is skewed accordingly (06:00–12:00 supplies 34.40% of candidates vs
13.94% for 18:00–24:00, against 25% uniform). It is causal, but it is not the
"discount pullback" detector the header docstring claims; it is partly a
time-of-day sampler.

### 3d. Stationarity across the train/test cut

Train (pre-2023-03) vs test (2023-03+), two-sample KS:

```
vol_strain        0.2596   <- worst
basis_index_bps   0.2151
funding_rate_pct  0.1907
taker_ratio       0.0986
... all 15 others  < 0.08
```

**No feature exceeds KS = 0.30.** Non-stationarity is real but mild, and it is
not the cause of the failure. (For completeness: three columns — `vol_strain`,
`basis_index_bps`, `funding_rate_pct` — are the *only* ones drifting materially,
and `basis_index_bps` has flipped sign: train mean +1.12 → test mean −2.86.)

### 3e. Informativeness — the actual finding

Point-biserial correlation against the label, and against the *gross* outcome:

| feature | IS r vs y | OOS r vs y | IS r vs **gross** R | OOS r vs **gross** R |
|---|---|---|---|---|
| **vol_strain** | **+0.1027** | **+0.0837** | **+0.0142** | **−0.0100** |
| atr_ratio | +0.0298 | +0.0707 | −0.0093 | −0.0079 |
| short_liq_zs | −0.0222 | −0.0041 | −0.0154 | +0.0074 |
| vah_dist | −0.0217 | −0.0141 | +0.0085 | +0.0165 |
| basis_index_bps | +0.0201 | +0.0142 | −0.0194 | −0.0061 |
| *(14 others)* | \|r\| < 0.017 | \|r\| < 0.03 | \|r\| < 0.02 | \|r\| < 0.02 |

Strongest feature in the set: **r = 0.1027**, i.e. it explains **1.05%** of
label variance. Against the *gross* outcome, **every feature is at or below
r = 0.02** — including `vol_strain`. Nothing in this space predicts direction.

---

## 4. THE ONE THING THE MODEL ACTUALLY LEARNED

This is the sharpest result in the audit.

```
vol_strain = atr_14 / close
fric_r     = 0.0041 * close / atr_14  =  0.0041 / vol_strain
```

`vol_strain` is the **mathematical inverse of the transaction cost expressed in
R**. Measured:

| | r vs `label_y` | r vs `fric_r` | r vs **`exit_r`** (gross) |
|---|---|---|---|
| train | +0.1027 | **−0.4865** | +0.0142 |
| test | +0.0837 | **−0.3761** | **−0.0100** |

The model's single best feature carries **zero** information about whether the
trade wins — and strong information about whether the trade is *cheap*. It has
learned the cost function, not the market. High-volatility bars have a large ATR,
so 41 bps is a smaller fraction of R, so `net_r > 0` is likelier — without the
trade being any more likely to work.

That is why the model degrades exactly as observed: it correctly ranks cost,
which buys a little, and cannot rank edge, which is everything.

---

## 5. THE UNIT PROBLEM — 1R is barely bigger than one round trip

This is the structural disease, and it is upstream of the ML entirely.

```
1R          = 15m ATR-14 = median 0.527% of price   (candidate bars)
round trip  = 41.0 bps   = 0.410% of price
cost / 1R   = 0.779       median base friction = 0.779 R

nominal stop = 1.20 R ->  64.9% of the stop distance is consumed by
                          friction before the price moves at all
   at 1.5x stress ->  97.3%
   at 3.0x stress -> 194.7%   (the trade cannot win at any price)
```

For friction to be a tolerable 10% of 1R, 1R would have to be **4.100% of
price** — an ATR **7.8× larger** than the 15m ATR-14 that currently defines it.
That is roughly a 2-hour ATR, not a 15-minute one.

**Phase 2 made this worse, and I should have caught it then.** Removing
`np.maximum(atr_14, close * 0.012)` was correct in principle — a constant floor
made the barrier grid fixed-percentage rather than ATR-adaptive. But that floor
was binding on **90.33%** of all 15m bars, and it was doing one job that
mattered:

| | median 1R | friction in R | fric / stop |
|---|---|---|---|
| with floor (pre-Phase 2) | 1.245% | 0.329 | 27.4% |
| without floor (current) | 0.682% | 0.602 | **50.1%** |

Removing the floor raised the round-trip cost **1.83×** in R units with no
change to alpha logic. **This is not an argument to restore the floor** — it
restores the original defect. The real conclusion is that a 15m ATR-14 is the
wrong *unit* to trade against 41 bps, and the floor had been masking that.

---

## 6. MODEL AUDIT — memorisation, not discrimination

Per-symbol, trained pre-2023-03, scored 2023-03+ (14 symbols clear the 500-row
and two-class minimums):

```
mean in-sample AUC  = 0.8592
mean out-of-sample  = 0.5217      <- 0.5 is a coin flip
mean decay          = 0.3375
```

Per symbol the OOS AUC runs 0.4846 (LTC) to 0.5741 (BTC). **Not one symbol
holds discrimination out of sample.**

Calibration, pooled OOS, 25,888 scored candidates, base rate 22.44%:

| prob bucket | n | actual P(y=1) |
|---|---|---|
| [0.00, 0.30) | 17,671 | 21.14% |
| [0.30, 0.40) | 7,414 | 24.44% |
| [0.40, 0.46) | 655 | 32.67% |
| [0.46, 0.50) | 91 | 26.37% |
| [0.50, 0.55) | 50 | 38.00% |
| [0.55, 0.65) | 7 | 42.86% |

The ranking is monotone-ish but the population above threshold is tiny (148 of
25,888), and the lift is exactly what you would expect from a feature set whose
strongest member is a cost proxy. Note also `num_leaves=1023` with
`max_depth=4` — the leaf count is capped at 2⁴ = 16, so that hyperparameter is
inert. "Trial #24641 Champion: 10 Passes, +4,629.28 USD" in the comment is a
fitted artefact of exactly the kind we have already falsified four times.

---

## 7. VERDICT — what this rules in and out

**The question was "why is the model picking losers 69% of the time?" The answer
is that it isn't.**

| | R/trade |
|---|---|
| take every candidate | −1.1385 |
| **model-selected, OOS (the ledger)** | **−0.71 to −0.82** |
| perfect oracle | +1.3470 |

The model *does* improve on random — −1.14 → −0.75 — which is precisely what an
OOS AUC of 0.52 should buy. It is working correctly. **It is selecting well from
a set that contains nothing.**

Break-even requires a **59.80%** net win rate (avg winner +1.347 R, avg loser
−2.004 R). The delivered win rate is 31.5% / 35.1% / 33.9%. The gap is
**25.9 percentage points**, and it cannot be closed by selection, because
closing it requires OOS AUC approaching 1.0 on features that correlate ≤ 0.02
with the gross outcome.

**Ruled out by this audit — do not spend time here:**
- Label leakage. Purge is 72 h against an 8 h horizon; no label column in the feature set.
- Feature lookahead. `future_cvd_15m` is futures CVD; `session_vah/val` are expanding.
- Gross non-stationarity. No feature exceeds KS = 0.30 across the cut.
- Stop/TP mis-tuning. The grid sits 0.21 points from its own break-even — it is a fair coin, not a badly set grid.
- Model hyperparameters. OOS AUC 0.52 is what this feature space contains; retuning buys nothing.
- Per-symbol vs pooled training. Pooling changed the *number*, not the edge.
- Tail-risk / L2 microstructure work. The tail is 8 trades; the average trade loses 0.78 R. Confirms your decision to freeze the L2 pipeline.

**Ruled in, in descending order of consequence:**
1. **The R unit is wrong.** A 15m ATR-14 makes 41 bps equal to 0.78 R. Any
   strategy denominated in this unit pays 65–195% of its stop in friction.
2. **There is no directional edge in this feature set at this horizon.** Gross
   expectancy +0.0058 R, p = 0.396, over 52,252 draws and 5.7 years.
3. **The ratchet converts 13.4% of trades into net losers** and gives back 0.08 R.
4. **`vwap_z < −0.4` is a time-of-day filter**, not a discount filter.
5. **Two feature slots are one feature** (`zc_norm` / `sf_div`, r = 0.9998).

---

## 8. VERIFICATION, AND TWO ERRORS OF MINE CORRECTED IN FLIGHT

`python3 scratch/diag_s1_autopsy.py` runs the full pipeline end to end: it
imports the real `label_triple_barriers_numba` and `load_btc_macro_tide`,
regenerates all 52,252 candidates for all 18 symbols through the actual
entry-condition code, and fits the actual `InstitutionalDualModelEngine`
per symbol. Every number above is read off that run or off
`scratch/diag_s1_pool.parquet`, which it writes. The code paths exercised are
`label_triple_barriers_numba`, `build_stress_series`, `train_models`, and
`score_test_candidates` — the same functions the production runner calls.

Two claims I made mid-audit and then disproved with my own measurements:

1. **"99.97% of trades exit on horizon timeout; the stop never fires."** False.
   I had subtracted base friction in both labeler passes, so my "gross" series
   was net, and the atomic-outcome buckets landed nowhere near the grid.
   Recomputing `exit_r = realized_r + fric_r` gives the true picture: the stop
   fires on **56.96%** of candidates and the +3R target on 14.65%. The corrected
   table is §1.
2. **"`zc_div` is literally `spot_cvd_15m − future_cvd_15m`."** False. Maximum
   absolute deviation is 2,880.1; my first check used `fillna(0)`, which
   manufactured the apparent match on NaN rows. They are distinct raw columns
   that become indistinguishable (r = 0.9998) only after dividing by
   `volume_base`. I also printed "both are ~1e-4 in magnitude" — wrong; the
   median magnitude is 9.5e-2. The finding is collinearity, not scale.

Not verified: nothing in this audit touches the live runner, so the pristine
baseline (−11,089.36 / 0 of 63) is unchanged and was not re-run.
