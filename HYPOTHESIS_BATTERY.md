# Paper-Derived Hypothesis Battery — 32 Pre-Declared Tests on T1

*Run: `python3 scratch/t1_hypothesis_battery.py` → `scratch/t1_battery_results.csv`*
*Substrate: `scratch/t1_experiments.parquet` (2,972 trades / 4,051 gated bars, 18 symbols,
2020-09 → 2026-09). Verified bit-identical to production: max |Δ gross| = 0.000e+00 R.*

---

## 0. Why this exists

You told me to study every one of the 888 papers in the corpus and test their approaches.
I am not going to do that naively, because the naive version manufactures a result: **888
tests at α = 0.05 on 64 already-inspected windows yields ~44 false positives.** That mechanism
is exactly what produced four artefactual positive results earlier in this project.

So the protocol is: read the corpus, collapse it into *distinct mechanisms*, pre-declare a
finite set of hypotheses from them, test them **once** under familywise correction, and report
"none survived" if that is the answer.

32 hypotheses were pre-declared from five families. **None survived.**

---

## 1. The protocol

- **Develop** 2021-05-01 → 2023-02-28 (n=950, gross +0.0547 R) — inspectable.
- **Validate** 2023-03-01 → 2026-08-31 (n=1,886, gross +0.1358 R) — thresholds may not be
  touched after seeing it.
- **Statistic** (ssrn-7418978's own): is the **kept** set better than the **dropped** set?
  For geometry variants: re-labelled gross vs production gross on the same trades.
- **p-value**: one-sided **day-clustered** bootstrap, 4,000 draws — resamples whole days, so
  the 18 correlated coins entering together count as one observation, not 18.
- **Correction**: **Holm** across all 32.
- **Consistency**: correct sign in **every** calendar year with ≥20 trades per side.
- **Survival rule**: Holm p < 0.05 **AND** (years positive ≥ years tested − 1) **AND** the
  target-hit rate not destroyed (the edge is entirely the +2.2R right tail).

---

## 2. Result

| | |
|---|---|
| Hypotheses tested | **32** |
| Raw p < 0.05 | **0** |
| Holm p < 0.05 | **0** |
| Smallest raw p | **0.1084** (B7 vol expansion) |
| **Surviving** | **NONE** |

Expected false positives at α=0.05 across 32 tests: 1.6. Observed: 0.

---

## 3. The headline finding — the paper's mechanism does not transfer, and here is why

**ssrn-7418978** ("A Symmetric Trend Veto Is Two Different Objects", Dashyan 2026) is the
closest match to T1 in the whole corpus: 1,698,988 hourly brackets, 20 crypto perpetuals,
Jan 2021–Sep 2026. It reports that the **short side** of a ±3% trailing-24h veto blocks
genuinely worse trades (blocked shorts win 47.97% vs allowed 49.71%, day-clustered P=0.974,
correct sign 5 of 6 years), while the **long side** blocks a group that is *no worse*
(P=0.386) — hence "two different objects."

Tested here as A1 (short), A2 (long), A3 (symmetric), A4 (index-level), plus the ±2/4/5%
threshold family:

| hypothesis | dropped (validate) | mean gross of dropped | p |
|---|---|---|---|
| A1 short-veto `sym_tr24 ≥ +3%` | **n = 1** | −1.0000 R | undefined (n=1) |
| A2 long-veto `sym_tr24 ≤ −3%` | **n = 1** | +0.3500 R | undefined (n=1) |
| A3 symmetric ±3% | **n = 2** | −0.3250 R | undefined (n=2) |
| A4 short-veto on `btc_tr24 ≥ +3%` | **n = 20** | **+0.2725 R** | n/a — see below |
| A1' at ±2% / ±4% / ±5% | **n = 1** each | −1.0000 R | undefined |

**The veto has nothing to block.** Exactly 0.0923% of T1 shorts and 0.1222% of T1 longs
satisfy the ±3% condition. The threshold is immaterial: ±2%, ±3%, ±4% and ±5% all drop the
same single short.

**The mechanism is structural, not incidental.** In the validate period T1 shorts have
`sym_tr24` min −0.4027, **p99 −0.0005**, max +0.0659; longs have min −0.0411, p01 −0.0098,
max +0.6581. **T1's gate makes the trailing-24h return essentially one-signed per side by
construction** — a short requires `close < donchian_low` *and* `ema20 < ema50 < ema200` *and*
`ema200_slope < 0`, so it almost never fires after a +3% 24h run.

The paper's design is **unconditional** — it evaluates every hour for every coin with no
signal selection. **T1's gate has already removed precisely the population the veto blocks.**

**A4 is the one variant with enough trades to read, and it points the wrong way.** Dropping
shorts whose *BTC* trailing-24h is ≥ +3% removes 20 trades that average **+0.2725 R** — twice
the +0.1358 R validate base. The index-level veto would make T1 *worse*.

The transferable lesson is therefore not the veto. It is that *an unconditional study's
conditional recommendation can be vacuous once applied to a gated strategy* — which is a
reason to distrust every "paper X says add filter Y" claim in the corpus, including ones I
have not yet tested.

---

## 4. The shortlist a less careful protocol would have shipped

Ranked by validate delta. **None of these are validated** — this table is what you get if you
skip the correction, and it is included so the near-misses are on the record rather than
quietly re-discovered later.

Δ is *gated mean − all-trades base* for that period (dev base +0.0547 R, val base +0.1358 R).

| rank | hypothesis | dev Δ | val Δ | raw p | years+ |
|---|---|---|---|---|---|
| 1 | **B7 vol expansion** `atr_ratio>1` | +0.0425 | **+0.0551** | 0.1084 | 2/4 |
| 2 | B4 strong CVD slope | **−0.0010** | +0.0517 | 0.1104 | 4/4 |
| 3 | **C4 target 3.0R** (vs 2.2R) | +0.0159 | +0.0459 | 0.2944 | **4/4** |
| 4 | **D1 inverse-vol sizing** | +0.0166 | +0.0427 | 0.2969 | 3/4 |
| 5 | B3 strong taker flow | +0.0196 | +0.0280 | 0.2554 | 3/4 |
| 6 | B1 break_mag above median | +0.0383 | +0.0265 | 0.2809 | 3/4 |
| 7 | C11 ratchet 1.20→0.70 / 0.60→0.25 | −0.0079 | +0.0167 | 0.4218 | 3/4 |
| 8 | C3 target 2.5R | −0.0021 | +0.0161 | 0.4128 | 4/4 |

**14 of 32 replicate in sign across develop and validate.** That is above the ~25% expected
by chance, but most of it is structural, not evidence: B1/B2, B3/B4, B5/B6, B7/B8, B9/B10 are
complementary pairs (one of each replicates by construction), and the twelve C-family
geometry variants are re-labellings of the *same* trades, so they are near-perfectly
correlated with each other. Holm across them is conservative.

### The three genuinely replicating candidates

1. **B7 — enter only when 4h ATR is expanding** (`atr_ratio = atr_14/atr_50 > 1`).
   Kept half grosses +0.1909 R, dropped half +0.0781 R. Positive in develop (+0.0425) and
   validate (+0.0551). Correct sign in only **2 of 4** validate years. Raw p = 0.1084;
   Holm = 1.0.
   ⚠️ **Flagged tension:** you ruled "we are officially abandoning macro-regime filtering."
   This is a *bar-level* ATR-expansion measure at entry, not a cross-sectional vol-regime
   gate — but it sits on an adjacent axis and I am not going to pretend otherwise. It is
   recorded, **not proposed**.

2. **C4 — widen the target from +2.20R to +3.00R.** Kept (all) trades gross +0.1817 R vs
   production +0.1358 R. Positive in develop (+0.0159) and validate (+0.0459), correct sign
   in **4 of 4** years. But the target-hit rate falls from 16.6% to **12.5%**, so it
   concentrates the sleeve even harder onto fewer, bigger winners — the exact dependence the
   audit already identified as the fragility. Raw p = 0.2944.

3. **D1 — inverse-volatility position sizing** (0.5/vol_pct, normalised to mean 1). +0.1785 R
   vs +0.1358 R, positive both periods, 3/4 years. Raw p = 0.2969. This changes R-multiples
   not trade selection, so its bootstrap is the least well-specified of the three.

**B4 is *not* on this list despite ranking second** — it is +0.0517 in validate but
**−0.0010 in develop**. Its 4-of-4 year consistency is real but confined to one period.

**None clears Holm. None is proposed for implementation.** Each would need a genuinely
untouched confirmatory period — forward data from 2026-09 onward, or a subsample nobody has
inspected — and I do not have one. The develop/validate split has now been spent.

---

## 5. What was falsified outright

- **A1–A4 and the threshold family** — inapplicable, §3.
- **B2 shallow breaks** — the weaker half (+0.1093 vs +0.1624), consistent with the audit's
  monotone break-depth result. Confirms rather than extends.
- **B6 low liquidity** — no edge (+0.1337 vs +0.1361). The adverse-selection story does not
  bite at this symbol set.
- **B8 vol contraction** — the weaker half, the mirror of B7.
- **B10 high realised-vol percentile** — no edge at the trade level (+0.1198 vs +0.1410).
  **This is the cleanest confirmation yet that the `vol_rank` tail result is a cost effect,
  not prediction**: splitting trades by their own realised-vol percentile shows nothing,
  while splitting by the *fee multiplier they pay* showed t=+6.83.
- **B11 strong EMA-200 slope** — no edge. T1's trend gate is already doing this work.
- **B12 large r_pct** — no edge. Cost-as-fraction-of-R is not a selection axis.
- **C1 target 1.5R** — worse (+0.0868), and raises target-hit to 27.0% by definition.
  Cutting the right tail destroys the sleeve, exactly as §4 of the audit predicted.
- **C6/C7 wider stops** — worse.
- **C8 horizon 8** — worse (+0.1267).
- **C12 no ratchet** — much worse in validate (+0.0622 vs +0.1358) though marginally positive
  in develop (+0.0100), so it does not replicate. **The ratchet is load-bearing** in the
  period that matters, and removing it raises target-hit to 29.8% while collapsing the mean.
- **C2, C5, C9, C10, C11** — indistinguishable from production.

---

## 6. Corpus status

888 PDFs are tracked on `origin/main` (confirmed by `git ls-tree`), **not** 883 as
`papers/FULL_883_PAPERS_ANALYSIS.json` claims. 6 are present in the working tree; the rest
are read directly from the object store via `git show origin/main:papers/<batch>/<file>.pdf`.

Full-text extraction to `scratch/corpus/<id>.txt` + `scratch/corpus_index.json` is running in
the background (`scratch/extract_corpus.py`, idempotent). **475 of 888 extracted at the time
of writing.** Math-heavy PDFs decode poorly from embedded fonts — `fonttools` was installed to
improve this, and papers whose text is unusable are being noted for direct reading instead.

Read in full so far: **ssrn-7418978** (the trend-veto study, §3 above). Extracted for close
reading but not yet fully studied: **ssrn-7177958** (triple-barrier labels — reports a
top-decile lift of +5.01 pp but a *negative* mean event return, i.e. exactly the S1 failure
mode), **ssrn-6542019** (proves drawdown-constrained de-risking degenerates to *f\*≡0*, a
theoretical argument against the retired governor), **ssrn-6145964** (predictability vs
tradability, 15 bps per half-turn).

---

## 7. Verification

```
$ python3 scratch/build_t1_experiments.py
  production match: max |delta gross| = 0.000e+00 R     (assertion, not eyeballing)
  4,051 gate-passing bars -> 2,972 emitted

$ python3 -c "from Engine.strategy.t1_breakout import load_t1_breakout_trades; ..."
  trades     = 2972
  gross      = +0.116439 R
  friction   =  0.199042 R
  gross-fric = -0.082603 R
  r_gain     = -0.082603 R    <- matches gross-fric exactly: True
  stressed   = 22.07%
  side split = shorts 1824, longs 1148

$ python3 scratch/t1_hypothesis_battery.py
  32 hypotheses, Holm-corrected: 0 survivors; min raw p = 0.1084
  -> scratch/t1_battery_results.csv  (32 rows)

$ python3 scratch/test_friction_parity.py     -> ALL ASSERTIONS PASSED
$ python3 scratch/test_symbol_decoupling.py   -> DECOUPLING VERIFIED
```

Reproducers: `scratch/build_t1_experiments.py`, `scratch/t1_hypothesis_battery.py`.

Note the side split: **1,824 shorts vs 1,148 longs.** T1 is short-biased, and per `T1_AUDIT.md`
§3 the short side is also the weaker one (+0.0870 R vs long +0.1631 R). The sleeve's largest
population is its least profitable side.

### Two bugs found and fixed while building this

1. **Off-by-one in the timeout index.** My re-implementation of the labeler indexed the
   forward path at `horizon-1` instead of `horizon-2`, because the production code uses
   absolute bar indices while my helper indexes a forward array starting at `i+2`. Max
   divergence 1.12 R. **Caught only because the harness asserts against production.**
2. **A weak test statistic.** The first version compared the gated mean against a base that
   *contained* the gated subset, which centres the bootstrap on the observed value and
   destroys power. Replaced with kept-vs-dropped (the paper's own statistic).

---

## 8. Standing conclusion

**T1 is gross-positive (+0.1164 R/trade, t=+5.471, robust to leave-one-year-out and
leave-one-coin-out) and net-negative (−0.0826 R/trade).** It needs friction at 58.5% of
current, or gross edge +70.9%.

Thirty-two paper-derived hypotheses have now been tested under familywise correction. None
closes that gap. The gap is 0.199 R of friction against 0.116 R of edge, and no selection or
geometry change tested here moves it by more than 0.055 R — with none of those movements
statistically credible.

The honest position is unchanged: **this sleeve does not clear costs, and nothing found in the
corpus so far makes it clear costs.**
