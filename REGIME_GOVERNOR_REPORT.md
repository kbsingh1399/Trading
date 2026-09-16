# Regime Governor — Market-State Defensive Gating

**Branch:** `arena/01a0a5bf-trading` · **Commits:** `30755b8` (+ prior Bayesian work)
**Baseline:** +5,553.70 USD (674 trades, 10/20 PASS)

---

## Verdict

Tracking the market instead of the model **does** produce a real, consistently-signed effect —
but only for the one rule with an *a priori* pedigree, and even that is **not statistically
significant** at the available sample size.

| Configuration | Primary (selection set) | Holdout (18 unseen) | Pooled *t* | Significant? |
|---|---|---|---|---|
| **shock-only** (vol rank ≥ 0.88) | **+376.96** (n=2) | **+100.11** (n=2) | **+2.028** (df=3) | **no** (crit. 3.182) |
| vol-only (shock + elevated) | +359.99 (n=3) | +75.62 (n=5) | +1.485 (df=7) | no |
| full (shock + elevated + chop) | **−264.29** (n=4) | +111.79 (n=7) | −0.208 | no |

Absolute scores:

| Run | PnL | Trades | Pass |
|---|---|---|---|
| **Primary baseline / control** | **+5,553.70** | 674 | 10/20 |
| Primary, shock-only governor | **+5,930.67** | 640 | 10/20 |
| Primary, vol-only | +5,913.70 | 626 | 10/20 |
| Primary, full pre-registered design | +5,289.42 | 585 | 9/20 |
| **Holdout control** | **+137.94** | 431 | 3/20 |
| Holdout, shock-only | +238.04 | 401 | 3/20 |
| Holdout, vol-only | +213.56 | 386 | 3/20 |
| Holdout, full | +249.73 | 377 | 3/20 |

**The pre-registered design fails** (−264.29 on primary). **shock-only beats baseline on both
independent window sets and is positive in 4/4 activations** — but at n=4 that is a promising
candidate, not a proven enhancement.

---

## What was built

`Engine/strategy/regime_governor.py`. The Bayesian tracker is gone entirely — the two engine
files were restored to their pristine base state and rebuilt from there (verified: zero
`bayes` references, empty diff vs. `f132f5f`).

Causal snapshot taken at each window's start, from strictly prior data:

| Feature | Definition |
|---|---|
| `vol` | BTC trailing 30d ATR% |
| `vol_rank` | its percentile rank over the trailing **365d** of 4h bars |
| `tide` | EMA-20/50/200 stack → +1 bull / −1 bear / 0 chop |
| `disp_rank` | rolling-365d rank of cross-sectional dispersion (std of trailing 30d returns across the 11 assets) |

Rules, penalty-only, **max not sum** (so the penalty is bounded and cannot stack):

| Rule | Trigger | Δ threshold |
|---|---|---|
| `vol_shock` | vol_rank ≥ **0.88** | +0.04 |
| `vol_elevated` | vol_rank ≥ 0.70 | +0.02 |
| `dead_chop` | tide == 0 **and** disp_rank < 0.25 | +0.02 |

**Threshold provenance matters here.** The 0.88 percentile is *inherited* from the repo's own
existing bar-level convention (`fast_numba_oos_engine.py:321`, `is_shock = rv_rank >= 0.88`) —
not chosen by me. That turned out to be the single most important design decision.

---

## Two design errors caught before they cost anything

**1. An expanding rank can never fire.** My first cut ranked current vol against all available
history. The result: the maximum rank across all 20 windows was **0.737** — the 0.88 threshold
was unreachable, because the 2021–22 high-volatility era permanently anchors an expanding
distribution. The repo's own filter uses a **rolling** rank for exactly this reason. Switching
to rolling-365d made W20 register 1.000.

**2. My own economic hypothesis was wrong, and I tested it rather than trusting it.** After
`dead_chop` cost −624.28 on W10, I hypothesised it was conceptually backwards — that low
trailing dispersion precedes vol *expansion*, so the rule flags the calm before the storm.
I tested that against market data alone: **r = +0.2222** (n=20), *positive*. The hypothesis is
refuted — low dispersion does mildly predict continued quiet. So I had **no** principled
justification for dropping the rule, and dropping it on PnL grounds alone would have been the
exact OOS-fitting error that invalidated the Bayesian tracker.

---

## The holdout: what turned this from a guess into evidence

`Engine/oos_windows_20_random.json` sits in the repo and shares **only 2 of 20** windows with
the primary set — 18 genuinely unseen windows (2024-03 → 2026-07). That let me do proper
protocol: *select* on the primary set, *validate* on the holdout.

The decisive test was **sign consistency across the two independent sets**:

| Rule | Primary | Holdout | Sign consistent? |
|---|---|---|---|
| `vol_shock` (≥0.88) | **+376.96** (n=2) | **+100.11** (n=2) | **YES** |
| `vol_elevated` (≥0.70) | −16.97 (n=1) | −24.49 (n=3) | YES — but consistently *negative* |
| `dead_chop` | −624.28 (n=1) | +36.17 (n=2) | **NO — noise** |

This is the cleanest result in the whole exercise:

- **`vol_shock` is positive on both sets, 4/4 activations.** It is also the rule whose
  threshold came from the repo's existing convention rather than from me.
- **`vol_elevated` is consistently negative** — 0.70 is too trigger-happy and catches benign
  windows. It should be dropped, and this conclusion is *consistent*, so it is not OOS-fitting.
- **`dead_chop` flips sign** — pure noise on 1–2 observations. Drop it for lack of evidence.

`shock-only` is therefore not "the variant that scored best"; it is the only rule that
survived a consistency test across independent data.

### Primary-set scorecard, shock-only (+5,930.67)

Only two windows differ from baseline; the other 18 are bit-identical:

| W# | Window | Regime | Δ | Baseline | shock-only | Change | Status |
|---|---|---|---|---|---|---|---|
| W15 | March 2024 Pre-Halving ATH Run | vol_shock | +0.040 | +500.59 | +591.74 | **+91.15** | PASS → PASS |
| W20 | March 2026 Late-Cycle Microstructure Shock | vol_shock | +0.040 | −223.19 | +62.62 | **+285.81** | **FAIL → PROFIT** |

W20 is the governor doing precisely its designed job: a genuine vol shock (rank 1.000) drove
S1 entries to zero, capped drawdown at 1.85% instead of 4.46%, and turned the worst window in
the suite into a small profit.

---

## Honest limits

1. **Not statistically significant.** shock-only pooled: n=4, mean +119.27, SE 58.80,
   **t = +2.028 on df=3**; the critical value at p=0.05 is 3.182. Four activations across
   40 windows cannot establish an edge.
2. **The primary set is now contaminated.** I used it to select among variants, so the
   +376.96 there is a selection-set number. The holdout's **+100.11 on 2 activations** is the
   honest estimate — small.
3. **The holdout is a different era.** It spans 2024-03 → 2026-07 only, and the control makes
   just +137.94 there versus +5,553.70 on the primary set. It is a much lower-edge regime, so
   +100.11 is large *relative* to that period and modest in absolute terms.
4. **`disp_rank` never earned its place.** It fired twice on the holdout (+36.17) and once on
   primary (−624.28). No evidence either way.

---

## Recommendation

**Ship `vol_shock` only; keep it under observation.** It is the one rule that is positive on
two independent window sets, positive in every activation, and whose threshold is inherited
from existing repo convention rather than fitted here. Concretely:

```
--rules shock        # +0.04 threshold penalty when rolling-365d BTC vol rank >= 0.88
```

Drop `vol_elevated` (consistently negative) and `dead_chop` (sign-inconsistent). Do **not**
present the +5,930.67 primary figure as a result — quote the holdout.

To actually establish significance you need more activations, not more tuning: the 0.88
threshold fires in ~2 windows per 20. Either widen the suite to more windows/years, or accept
that this is a risk-reducing overlay whose real merit is the W20-style drawdown cap rather
than a PnL claim.

---

## Verification performed

- **Baseline control:** `--disable-governor` reproduces +5,553.70 / 674 trades / 10 PASS
  exactly — the governor plumbing is side-effect-free.
- **Pristine restore:** the two engine files diff empty against `f132f5f`; zero `bayes` refs.
- **Governor unit tests:** 10 hand cases (boundaries at 0.88 / 0.879, max-not-sum, NaN
  handling, no-history) all pass; **min delta = +0.000 over 20,000 random regimes** — the
  governor provably never loosens an entry.
- **Bugs found and fixed:** `np.where` returns an ndarray, so `.iloc[-1]` raised
  `AttributeError` in `compute_regime_features`; a `build_dispension_series` typo.
- **Regime features characterised blind to PnL** (`scratch/characterise_regimes.py`) before
  any backtest was consulted.
- **8 full suite runs** across 2 window sets × 4 configurations, all via the real runner
  entry point.

## Reproduction

```bash
python3 Engine/run_20_oos_dual_model.py --disable-governor          # control == baseline
python3 Engine/run_20_oos_dual_model.py --rules shock               # recommended
python3 Engine/run_20_oos_dual_model.py                             # full pre-registered
python3 Engine/run_20_oos_dual_model.py --windows Engine/oos_windows_20_random.json --rules shock
```

JSON scorecards in `scratch/*.json`, regime features in `scratch/regime_features.json`
(gitignored — `scratch/` is a build directory).
