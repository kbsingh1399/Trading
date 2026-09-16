# WILLIAMS %R ON T1 — Tested Four Ways

Reproducer: `scratch/diag_williams_r.py`, pool cached to
`scratch/diag_wr_pool.parquet` (4,051 gate-passing bars, 2,972 emitted trades).

**Protocol, pre-registered before any validation number was read:**
develop = primary (2021-05-01 → 2023-02-28), validate = holdout + expanded
(2023-03-01 → 2026-08-31). Full search grid printed so the multiple-testing
exposure is visible.

**Short answer: Williams %R does not work on T1.** It fails as a filter, as an
ML feature, and as a standalone entry. One narrow pattern survives directionally
and is worth a clean test, but it is not confirmed and I am not proposing it.

---

## 0. FIRST PROBLEM: AT SHORT LOOKBACKS %R IS THE GATE REWRITTEN

`%R(n) = −100 × (HH_n − C) / (HH_n − LL_n)`

T1's long trigger is `close > prior-20-bar Donchian high`. At n=20 that pins %R
near zero by construction:

| n | mean %R at T1 long entries | sd | P(%R > −20) |
|---|---|---|---|
| 14 | −8.25 | 6.70 | 95.5% |
| 20 | −7.32 | 6.15 | **97.1%** |
| 50 | −12.82 | 14.53 | 77.2% |
| 100 | −19.02 | 20.23 | 62.7% |
| 200 | −26.22 | 25.01 | 52.2% |

At n=14/20 %R is a deterministic function of the entry condition — no
information. Only the long lookbacks measure something the gate does not: where
the break sits inside a *wider* range.

And even those are not independent of T1's existing inputs:

| lookback | corr with `buy_vol_ratio` | corr with gross_r |
|---|---|---|
| 14 | +0.8448 | +0.0308 |
| 20 | +0.8479 | +0.0314 |
| 50 | +0.8317 | +0.0200 |
| 100 | +0.8196 | +0.0118 |
| 200 | +0.8188 | +0.0159 |

**%R correlates 0.82–0.85 with a feature T1 already gates on**, and ≤0.031 with
the outcome it would need to predict.

---

## 1. AS A T1 FILTER — 40-cell grid, does not replicate

Rule: keep a trade if `sgn × %R_n ≥ thr` (sgn = +1 long, −1 short).
Develop baseline: n=950, gross **+0.0547 R**, net −0.0928 R.

**2 of 40 cells qualified** (beat develop baseline gross, keep ≥40% of trades).
Best by gross t-stat: **n=100, thr=−30**, develop gross +0.0557 R (t=+1.49,
p=0.136), keeps 99.3%.

Validation, scored once with parameters frozen:

```
UNGATED validate : n=1,886  gross +0.1358 R (t=+5.08)  net -0.0929 R
GATED            : n=1,824  gross +0.1306 R (t=+4.80)  net -0.0952 R
  gated - ungated = -0.0052 R    Welch t = -0.137    p = 0.8912
  the 62 dropped trades grossed +0.2893 R  <-- the filter removed GOOD trades
  gross captured: 93.0%
```

**VERDICT: DOES NOT REPLICATE.** It is slightly worse than doing nothing.

Note also that the obvious "don't chase extended moves" filter (`thr=0`, keeps
77.1%) *reduces* develop gross from +0.0547 to +0.0338 R. The classic Williams %R
intuition runs backwards on this sleeve.

---

## 2. AS AN ML FEATURE — LightGBM walk-forward

Features: `%R` at all 5 lookbacks + `buy_vol_ratio`, `spot_cvd_slope`,
`ema_200_slope`, `atr`, `r_pct`, `side`, `stress`. Trained on the develop
gate-passing pool (1,422 rows), scored on validate (2,629 rows).

```
in-sample AUC = 0.8934
OOS       AUC = 0.5523        (0.5 = no discrimination)
```

Williams %R takes **48.88% of feature importance** — but that is five collinear
columns splitting gain among themselves, and importance is not predictive value.

On the 1,902 emitted validate trades, by model-probability decile:

| decile | n | gross R | t |
|---|---|---|---|
| **0 (lowest prob)** | 191 | **+0.2756** | **+3.27** |
| 1 | 190 | −0.0425 | −0.54 |
| 6 | 190 | +0.1903 | +2.20 |
| 7 | 190 | +0.2336 | +2.77 |
| **9 (highest prob)** | 191 | +0.1593 | +1.86 |

**The ranking is not monotone — the lowest-probability decile is the best.**

```
top decile : gross +0.1593 R (t=+1.86)  net -0.0205 R
all        : gross +0.1344 R            net -0.0940 R
top vs all : Welch t = +0.277   p = 0.7818
```

Same failure mode as S1: 0.89 in-sample, 0.55 out. Memorisation, not
discrimination.

---

## 3. AS A STANDALONE ENTRY — significantly *negative*

Its classic use: long when `%R ≤ −80` (oversold), short when `%R ≥ −20`
(overbought). Same 4h grid, same 18 symbols, same barrier geometry and friction.

| n | period | n trades | gross R | t | net R |
|---|---|---|---|---|---|
| 14 | develop | 20,590 | −0.0141 | −1.96 | −0.1635 |
| 14 | validate | 48,924 | −0.0430 | **−9.23** | −0.2778 |
| 50 | validate | 46,957 | −0.0493 | **−10.28** | −0.2799 |
| 100 | validate | 46,337 | −0.0256 | **−5.27** | −0.2462 |
| 200 | validate | 45,927 | −0.0193 | −3.96 | −0.2355 |

**Negative at every lookback, in both periods.** Mean reversion at 4h on crypto
perps has negative gross expectancy — which is consistent with trend being the
correct direction here, exactly what T1 already does.

(Caveat in T1's favour: these fire ~697 times per symbol per year on a 64h
horizon, so they overlap almost completely and the t-stats are optimistic. The
sign is not in doubt; the magnitude is.)

**Inverted** (i.e. used as momentum), it grosses +0.015 to +0.049 R against
0.15–0.17 R of friction. It recovers at most a third of one round trip. Dead.

---

## 4. THE ONE PATTERN THAT SURVIVES — and why I am not proposing it

Splitting shorts by `−%R_100` terciles, the **bottom tercile loses money in both
periods**:

| | develop | validate |
|---|---|---|
| low tercile | **−0.1021 R** (t=−1.62) | **−0.0506 R** (t=−1.00) |
| mid | +0.2363 (t=+3.08) | +0.2336 (t=+3.84) |
| high | −0.0328 (t=−0.44) | +0.1878 (t=+2.87) |

As a filter, with the threshold taken from develop only (33rd percentile of
`−%R_100` among develop shorts = 87.20, i.e. drop a short when `%R_100 > −87.20`):

| | develop | validate |
|---|---|---|
| ungated gross | +0.0547 (t=+1.47) | +0.1358 (t=+5.08) |
| **gated gross** | **+0.1089 (t=+2.42)** | **+0.1841 (t=+5.93)** |
| ungated net | −0.0928 | −0.0929 |
| **gated net** | **−0.0329** | **−0.0384** |
| dropped trades gross | −0.1021 | −0.0505 |
| trades kept | 74.3% | 79.4% |
| target-hit rate | 15.16% → 17.56% | 16.60% → 18.96% |
| **Welch t on the delta** | **+0.929, p=0.353** | **+1.178, p=0.239** |

Directionally consistent, economically coherent, **statistically insignificant in
both periods**. The economic story: a T1 short triggers on `close < prior-20-bar
low`, and `%R_100 > −87.2` means close sits in the top ~13% of the 100-bar range.
Both can only hold if the range has compressed — so these are shorts out of a
tight consolidation near range highs, i.e. shorting into a squeeze. Those lose.

**Why I am not proposing it:**

1. **Not significant.** p=0.353 and p=0.239. The mean improves but the
   *difference* does not clear noise, because the filter discards 20–26% of
   trades.
2. **The protocol is contaminated.** I looked at the validate terciles in the
   diagnostic that found this, before fixing the threshold. The threshold value
   is develop-only, but I have seen the validate shape. **This is not a clean
   out-of-sample result.**
3. **It is one cell out of 30 inspected** (5 lookbacks × 2 sides × 3 terciles).
4. **It does not reach profitability anyway.** Gated net is still −0.033 to
   −0.038 R.

It is recorded so the observation is not lost. Confirming it requires a period
nobody has looked at.

---

## 5. THE BIGGER THING THIS EXPOSED

While setting up the develop/validate split I found that **T1's develop period
has no edge at all**:

| period | n | gross R | t | p |
|---|---|---|---|---|
| develop 2021-05→2023-02 | 950 | +0.0547 | +1.47 | **0.142** |
| validate 2023-03→2026-08 | 1,886 | +0.1358 | +5.08 | 0.0000 |
| all | 2,972 | +0.1164 | +5.47 | 0.0000 |

By year:

| year | n | gross R | t | p |
|---|---|---|---|---|
| 2020 | 63 | +0.3611 | +2.25 | 0.028 |
| 2021 | 347 | +0.0305 | +0.49 | **0.624** |
| 2022 | 596 | +0.0625 | +1.36 | **0.173** |
| 2023 | 436 | +0.2577 | +4.36 | 0.0000 |
| 2024 | 474 | +0.1867 | +3.40 | 0.0007 |
| 2025 | 620 | +0.1019 | +2.27 | 0.024 |
| 2026 | 436 | +0.0263 | +0.49 | **0.627** |

**Three of the last seven years have no detectable edge, including 2026.** This
matters more than Williams %R: any filter developed on 2021–2022 is being fitted
to the period where there is no signal to find, and the two most recent years
(2025 decaying, 2026 null) suggest the edge may be decaying rather than stable.

That was already visible in `T1_AUDIT.md` §3; this split makes it unavoidable.

---

## 6. VERDICT

| use | result |
|---|---|
| T1 filter (40-cell grid, pre-registered split) | **does not replicate**, p=0.891, slightly worse than nothing |
| ML feature (LightGBM walk-forward) | OOS AUC **0.5523**, top decile p=0.782, decile ranking non-monotone |
| standalone mean-reversion entry | **significantly negative** at all 5 lookbacks |
| inverted (momentum) | +0.015…+0.049 R gross vs 0.15–0.17 R friction. Dead |
| short-side range position (n=100) | directionally consistent, **not significant**, protocol contaminated |

**Williams %R does not add to T1.** The mechanical reason is in §0: at the
lookbacks where it is not a restatement of the Donchian gate, it correlates
0.82–0.85 with a feature T1 already uses and ≤0.031 with the outcome. There is
nothing in it that the gate has not already extracted.

T1's binding constraint remains what `T1_AUDIT.md` §4 identified: gross +0.1164 R
against 0.1990 R of friction, i.e. 51 bps → 29.8 bps. **No oscillator closes a
0.083 R gap.** The candidate levers are execution cost, and the year-level
instability in §5 — the second of which is the more urgent, because if the edge
is decaying, cheaper execution only loses money more slowly.

---

## 7. VERIFICATION

`python3 scratch/diag_williams_r.py` replays T1's real entry scan, re-applies the
production exit geometry, asserts the stress join matches at >99%, and computes
Williams %R on the causal rolling window ending at the signal bar. The emitted
trade set reproduces the production sleeve (2,972 trades) and the develop/validate
gross means reconcile with `T1_AUDIT.md`. No production code was changed by this
investigation.

One formatting bug of mine (a `%` in a printf-style string inside a docstring
line) aborted the §4 run on first attempt; re-run with f-strings, output above.
