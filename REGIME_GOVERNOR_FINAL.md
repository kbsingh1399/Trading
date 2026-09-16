# Regime Governor — Final Verdict

**Branch:** `arena/01a0a5bf-trading` · **Commits:** `30755b8`, `f575241`, `6b161e7`
**Supersedes:** `REGIME_GOVERNOR_REPORT.md` (whose shock-only result is now void)

---

## Verdict: the shock-only governor does not work

Widening the suite did exactly what it was supposed to do — it broke the result. With the
regime measure computed correctly and a genuinely fresh 25-window sample added, the effect
**vanishes**:

| Window set | Control | shock-only | Δ | Activations |
|---|---|---|---|---|
| Primary (20) | +5,553.70 | +5,839.51 | **+285.81** | 1 |
| Holdout (20, 18 unseen) | +137.94 | +366.56 | **+228.62** | 2 |
| **Expanded (25 fresh)** | +489.99 | **−123.25** | **−613.24** | 6 |
| **Total** | | | **−98.81** | 9 |

Episode-clustered across all three sets:

```
episode 1: 2021-01 (+18.76), 2021-02 (-33.77)                 =>  -15.01
episode 2: 2021-06 (+109.36)                                  => +109.36
episode 3: 2022-07 (-294.66)                                  => -294.66
episode 4: 2024-02 (-346.42), 2024-04 (-66.50), 2024-05 (+22.91) => -390.02
episode 5: 2024-09 (+205.71)                                  => +205.71
episode 6: 2026-03 (+285.81)                                  => +285.81

n = 6 independent episodes, mean = -16.47, SE = 111.58, t = -0.148 (df=5)
critical |t| at p=0.05, df=5 = 2.571   ->  significant: NO
positive in 3/6 episodes
```

**t = −0.148.** Indistinguishable from zero, and the point estimate is slightly *negative*.
The set with the most activations — and therefore the most information — is the one that
loses the most.

**Do not ship this.**

---

## What went wrong: a bug in my own regime measure

This is the important part. `compute_regime_features()` was ranking the **instantaneous 4h
`atr_pct`** against a 365-day window of itself, not the **30-day smoothed** measure I had
documented and characterised. A single 4h bar's ATR% is far too noisy to define a volatility
regime, and the two measures diverge sharply:

| Window start | rank(instantaneous 4h ATR%) | rank(30d smoothed) |
|---|---|---|
| 2024-03-01 | **0.980** | 0.522 |
| 2026-02-01 | **0.950** | 0.373 |
| 2021-03-01 | **0.884** | 0.748 |
| 2026-03-01 | 0.897 | **1.000** |

The buggy path therefore fired on essentially arbitrary bars. It armed **entirely different
windows** than the corrected version — on the holdout it triggered W01/W16 instead of
W02/W06; on the primary set it triggered W15 and W20 instead of W20 alone.

That means the entire prior evidence base was an artefact:

| Claim (now void) | Corrected |
|---|---|
| "positive in 4/4 activations" | 3/6 episodes positive |
| "primary +376.96" | primary +285.81 |
| "holdout +100.11" | holdout +228.62 |
| "sign-consistent across both sets" | sign flips; net −98.81 |

The specific W15 "+91.15 win" I cited was purely the bug: 2024-03's true 30d vol rank is
0.522, nowhere near the 0.88 threshold. It only triggered because a noisy bar read 0.980.

**Widening n is what caught this.** At n=2 the bug looked like a consistent edge; at n=6 it
did not survive contact with the data. This is the strongest argument in the whole exercise
for the user's insistence on a larger sample.

---

## Significance is unreachable for this rule on this data

Separately from whether the effect is real: the 0.88 threshold fires so rarely that
statistical significance cannot be reached here at all.

Scanning **every** available month in the dataset (2021-01 → 2026-07, the full span):

```
months evaluated           : 68
months with vol_rank >= 0.88: 9   -> activation rate 13.2%
  2021-01, 2021-02, 2021-06, 2022-07, 2024-02, 2024-04, 2024-05, 2024-09, 2026-03

consecutive triggering months are ONE volatility episode:
  [2021-01, 2021-02] [2021-06] [2022-07] [2024-02, 2024-04, 2024-05] [2024-09] [2026-03]
  => 9 months collapse to 6 independent episodes
```

**6 episodes is the ceiling.** Every shock episode in the entire dataset is now measured.

| To reach | Needs | Available |
|---|---|---|
| n=10 independent activations | ~76 monthly windows = 6.3 years | 5.7 years |
| n=20 | ~151 windows = 12.6 years | 5.7 years |
| n=30 | ~227 windows = 18.9 years | 5.7 years |

Even a *perfect* tail-risk governor could not be shown significant at this threshold on this
dataset. The binding constraint is the activation rate, not the window count — generating
more windows cannot manufacture independent volatility episodes that did not occur.

**Clustering matters here.** Treating 9 activations as independent would have given
t = −0.158 (n=9); episode clustering gives t = −0.148 (n=6). Both are null, but the naive
count would have overstated the evidence by 50% had the effect been positive. The 365-day
rolling trigger is autocorrelated by construction, so adjacent months are never independent.

---

## Expanded window set

`Engine/oos_windows_expanded_2021_2024.json` — 25 monthly windows, 2021-01 → 2024-04.

Of the 48 months in 2021–2024, **17 were excluded** (already in the primary selection set)
and **8 more** (already in the random holdout set), leaving a genuinely untouched third
sample. This matters: the shock-only design was *selected* using primary + random, so
reusing either would not have been independent evidence.

---

## Where this leaves the strategy

Across the full investigation, three governance mechanisms were proposed and all three failed
under proper testing:

| Mechanism | Fate | Decisive evidence |
|---|---|---|
| Cumulative Beta-Binomial win-rate tracker | **Falsified** | r = +0.032 vs next window's win rate; models refit per window |
| Decaying Beta-Binomial + penalty-only | **Falsified** | every activated decay setting lost money; argmax = tracker inert |
| Regime governor (vol shock / elevated / chop) | **Falsified** | t = −0.148 on 6 independent episodes; `dead_chop` sign-flips, `vol_elevated` consistently negative |

**The +5,553.70 USD baseline remains the gold standard.** No enhancement tested has survived
out-of-sample scrutiny, and two of the three looked positive before proper validation.

The recurring failure mode is worth naming: each mechanism produced a plausible positive
number on a small sample, and each positive number was an artefact — of a non-stationary
tracked quantity, of a threshold tuned to the test set, or of a noisy input measure. The
things that caught them were (a) measuring the signal's own predictive power, (b) validating
on genuinely unseen windows, and (c) increasing n until the effect had to survive.

### If you want to keep pursuing tail-risk protection

The one durable observation is qualitative, not statistical: in the 2026-03 shock window the
governor cut drawdown from 4.46% to 1.85% and avoided a loss. That is a **risk** benefit, and
it is being measured with a **PnL** metric on n=6, which is the wrong instrument. A defensible
version of this work would:

1. Target **drawdown and tail loss**, not PnL — e.g. worst-window loss, 5th-percentile window
   return, or max DD across the suite.
2. Accept a lower threshold (e.g. 0.75) to raise the activation rate, so the test has power —
   while pre-committing to the threshold before looking at results.
3. Pre-register the design, then evaluate once on untouched windows.

What should not happen is another round of threshold selection against these same 65 windows.

---

## Verification performed

- **Baseline controls re-run and unchanged** after the bugfix: +5,553.70 / +137.94 /
  +489.99 on the three sets — the fix touches only the governor path.
- **Bug isolated by measurement**, not inspection: the monthly vol-rank scan disagreed with
  the runner's triggers, which is what surfaced the wrong input column.
- **9 full suite runs** this phase (3 window sets × control/shock-only, plus the expanded
  pair), all through the real runner entry point.
- **Episode clustering** applied with a 2-calendar-month gap rule; duplicate months appearing
  in more than one set (2024-03 is in both primary and random) de-duplicated before clustering.

## Reproduction

```bash
python3 scratch/generate_expanded_windows.py                                   # 25 fresh windows
python3 Engine/run_20_oos_dual_model.py --rules shock                          # primary
python3 Engine/run_20_oos_dual_model.py --windows Engine/oos_windows_20_random.json --rules shock
python3 Engine/run_20_oos_dual_model.py --windows Engine/oos_windows_expanded_2021_2024.json --rules shock
python3 Engine/run_20_oos_dual_model.py --disable-governor                     # control == baseline
```

Scorecards in `scratch/fix_*.json` (gitignored — `scratch/` is a build directory).
