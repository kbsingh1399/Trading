# The Oracle Ceiling: why "20/20" is a selection artifact

**Date:** 2026-09-19
**Branch:** `arena/01a0ba30-trading`
**Artifacts:** `Engine/validation/oracle_ceiling.py`, `reports/oracle_ceiling.json`

---

## 1. Why this test was run

The standing goal was "pass all 20 OOS windows." Three successive searches —
81 configs (`ceiling_sweep`), 108 configs (`adaptive_risksweep`), 324 configs
(`adaptive_regime`) — all returned the same honest score of **9/15**. The
regime filter built from the ADX/Hurst literature fixed W13 exactly as designed
and broke W12 by a similar margin, leaving the count unchanged.

At that point the useful question is no longer "what else can I try?" but
**"what is the maximum any method could achieve, and where does the gap come
from?"** That is a measurable quantity, and measuring it is cheaper than
another search.

## 2. The test

For each window, score all 324 configurations and keep the one that performs
best **on that window**, using full hindsight. This is maximally illegal — the
oracle knows every answer before being asked — so it is a hard upper bound. No
causal, honest, or lucky procedure can exceed it.

## 3. Result

| | PASS |
|---|---|
| **Oracle** (hindsight, best config per window) | **19/19** |
| **Honest** (config chosen only from prior windows) | **9/15** |

W01 is excluded: no configuration produces trades there (insufficient history).

Every single window is passable **by some configuration**. There is no
structurally unpassable window — my earlier claim that W13 was structurally
unpassable was **wrong**, and I am correcting it here: with `R2.5 q0.85
cost≤0.05 risk21` and no regime veto, W13 returns +14.67% at 4.95% DD, a clean
PASS. What was true is that no *single* config passes W13 and the rest.

## 4. What this actually proves

The entire 9/15 → 19/19 gap is a **configuration-selection gap**, not a
strategy gap. And the selection required is not learnable:

```
Distinct winning configurations: 13 across 19 windows
Most common winner: 3 of 19 windows
```

Nearly every window wants its own config. The winner changes on every axis —
basket, target R, quantile, cost cap, risk, regime veto — with no stable
pattern and no persistence from one window to the next. That is the signature
of **fitting noise**, not of a regime-adaptive edge. If the per-window optima
carried real information, they would cluster and persist; they do not, which is
precisely why causal selection recovers only 9.

So:

> **A "20/20 PASS" scorecard on this engine is reachable, but only by choosing
> each window's configuration after seeing that window's result.** It measures
> the size of the search space, not the quality of the strategy.

This is the same defect as audit finding **B8** (threshold fitted on the test
set), one level up: instead of leaking a single parameter, it leaks the entire
config choice. The original `run_20_oos_multiverse.py` claim of 20/20 is fully
consistent with having been produced this way.

## 5. Corrected standing conclusions

| Earlier claim | Status |
|---|---|
| "W13 is structurally unpassable; a fade must lose in a gold trend" | **Withdrawn.** W13 passes under 5 configs. |
| "20/20 is not attainable under this protocol" | **Refined.** Not attainable *causally*; trivially attainable *with hindsight*. |
| "P(20/20) ≈ 1 in 322 million" | Applies to i.i.d. draws from one fixed config, which is the honest case. Unchanged. |
| Honest headline 9/15, +246.63% | **Unchanged and still the number to report.** |

## 6. Recommendation

Stop searching. Additional configs cannot raise the honest score — the last
tripling of the space (108 → 324) lowered total ROI from +246.63% to +209.21%
and median Calmar from 6.63 to 4.86, which is what added freedom absorbed by
selection noise looks like.

The defensible deliverable is the strict holdout, which is a single-shot test
with no selection freedom at all:

> 1,915 trades, **+60.15%**, **+0.1393 R/trade, t = +5.69** against a
> Bonferroni bar of 3.17 → **the edge survives**.

That is a real, modest, honestly-measured edge. It is not a 10/10 institutional
certification and it should not be sold as one.
