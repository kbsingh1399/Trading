# Multi-Strategy Book: design, result, and why it underperforms

**Date:** 2026-09-20
**Artifacts:** `Engine/validation/strategy_family.py`,
`reports/strategy_family.json`, `reports/strategy_family_split.json`,
`reports/strategy_family_admit.json`

---

## 1. Rationale

The oracle test showed the per-window optimal config jumps between 13 distinct
settings across 19 windows with no persistence — so *selecting* a config is
selecting noise. A multi-strategy firm sidesteps selection entirely: run several
sleeves with different alpha simultaneously, equal-weighted, and let
diversification do the work.

This is structurally honest. There is no per-window choice, so nothing can leak,
and with no tuning history required **all 20 windows become evaluable** rather
than 15.

## 2. The book

| Sleeve | Dir | Target R | Gate | Baskets |
|---|---|---|---|---|
| S1_FADE_MR | −1 fade | 1.5 | ADX≤28, H≤0.54 (mean-revert) | Forex |
| S2_TREND_MOM | +1 momentum | 2.0 | ADX≥25, H≥0.50 (trend) | Forex+CFD |
| S3_FADE_WIDE | −1 fade | 2.5 | none | Forex |
| S4_TREND_FAST | +1 momentum | 1.5 | ADX≥22, H≥0.48 (trend) | Forex+CFD |

Opposite directions gated on the *same* statistics with *reversed* inequalities
— that is what makes the streams structurally uncorrelated rather than
differently-parameterised. Sleeves merge into **one** book before simulation so
they share the capital base, concurrency cap and cluster cap; summing four
separate equity curves would quadruple risk and void the cluster governance.

## 3. Results

| Configuration | PASS | Median Calmar | Net ROI | Worst DD |
|---|---|---|---|---|
| Single sleeve, causally selected (prior best) | **9/15** | **6.63** | +246.63% | 8.74% |
| 4-sleeve book, full risk each | 4/19 | 1.10 | +175.24% | 18.35% |
| 4-sleeve book, risk split 4 ways | 0/19 | 1.00 | +43.81% | 4.70% |

**The book is materially worse than the single sleeve.** Reported as found.

## 4. Why — three findings

### 4.1 The diversification worked; the alpha did not

Sleeve correlation came out as designed:

```
               S1_FADE   S2_TREND   S3_FADE_W   S4_TREND_F
S1_FADE_MR       1.000     -0.347       0.694        0.137
S2_TREND_MOM    -0.347      1.000      -0.192        0.142
```

S1 vs S2 = **−0.347**, genuinely negative. And it did the intended job on the
problem window: **W13 went −4.33% → +2.06%**, with the trend sleeves firing
hardest there (S2:69, S4:197).

But standalone per-window expectancy:

| Sleeve | Mean ROI | Win rate over windows |
|---|---|---|
| S1_FADE_MR | **+11.78%** | 84% |
| S3_FADE_WIDE | **+7.54%** | 89% |
| S2_TREND_MOM | **−1.66%** | 32% |
| S4_TREND_FAST | **−2.70%** | 37% |

Both momentum sleeves lose money on their own. **Diversification rescales risk;
it cannot manufacture alpha.** Equal-weighting a negative-expectancy sleeve
alongside a positive one dilutes the good book toward the bad one's mean. The
correlation benefit is real and still insufficient — a −0.35 correlation against
a −2% mean is a smoother path to a worse destination.

### 4.2 Leverage is not the lever — again

Splitting risk 4 ways cut worst DD from 18.35% → 4.70%, a textbook result. It
also cut ROI from +175% → +44%. Median Calmar: **1.10 → 1.00**, i.e. unchanged.

The pass criteria (ROI ≥ +10%, DD ≤ 5%) imply **Calmar ≥ 2.0**, which is
scale-invariant. Position sizing moves numerator and denominator together and
can never buy a pass. This is now the third independent confirmation.

### 4.3 The ML gate is the entire edge

The causal admission test (`--causal-admit`) funds a sleeve only if it shows
positive expectancy strictly before W01. On **raw** labels, every sleeve is
negative:

```
S1_FADE_MR     E[R]=-0.0173  t=-2.02
S2_TREND_MOM   E[R]=-0.0667  t=-4.86
S3_FADE_WIDE   E[R]=-0.0085  t=-1.13
S4_TREND_FAST  E[R]=-0.0784  t=-8.26
```

Round-trip cost exceeds the raw signal for all four. Re-running the admission on
**ML-gated** signals (fit on the first 70% of the pre-W01 era, validate on the
last 30%) flips every sign positive — but with t ≈ 0.25:

```
S1_FADE_MR     gated E[R]=+0.0169  t=+0.28
S2_TREND_MOM   gated E[R]=+0.0214  t=+0.26
S3_FADE_WIDE   gated E[R]=+0.0088  t=+0.24
S4_TREND_FAST  gated E[R]=+0.0016  t=+0.05
```

So **0/4 sleeves are fundable** on pre-window evidence. I did not lower the
t-threshold until something passed; that would be the same tuning this whole
remediation exists to eliminate.

This is the most important line in the report: the strategy has no raw edge. The
classifier's ability to select among cost-negative candidates is the edge, and
on pre-2023 data that ability is not statistically distinguishable from zero.

## 5. Conclusion

The multi-strategy design is sound engineering and it is the right instinct — it
removes the selection leak and makes all 20 windows evaluable. It still does not
pass 20/20, and it does not beat the single sleeve.

The reason is not the architecture. It is that only two of four sleeves have any
edge, the profitable pair is 0.694 correlated (both are fades, so they are close
to one strategy), and the criteria demand a scale-invariant Calmar ≥ 2.0 that no
amount of blending or sizing has produced.

**20/20 remains unreached.** The honest results stand:

- Best causal walk-forward: **9/15 PASS, +246.63%**
- Strict single-shot holdout: **+60.15%, +0.1393 R/trade, t = +5.69** vs
  Bonferroni 3.17 → edge survives.
