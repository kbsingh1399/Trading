# T1 AUDIT — The 4-Hour Sleeve, and the S1 Removal

S1 is retired. This document audits T1 with the same gross-vs-net teardown that
killed S1, reports a **live bug found and fixed** in T1's friction model, and
gives the T1-only out-of-sample scorecard.

Reproducers: `scratch/diag_t1_autopsy.py` (signal autopsy, cached to
`scratch/diag_t1_pool.parquet`), `Engine/run_t1_oos.py` (OOS runner).

---

## 0. HEADLINE

**T1 has real gross edge. S1 never did.**

| | S1 (15m ML) | **T1 (4h breakout)** |
|---|---|---|
| median 1R | 0.527% of price | **2.884%** of price |
| friction | 0.779 R (64.9% of stop) | **0.199 R (19.9% of stop)** |
| **GROSS expectancy** | +0.0058 R, t=+0.85, **p=0.396** | **+0.1164 R, t=+5.47, p<1e-7** |
| net expectancy | −1.1385 R | **−0.0826 R** |
| verdict | mathematically unwinnable | **~41% of a cost reduction from break-even** |

T1's edge is statistically robust, survives leave-one-year-out and
leave-one-symbol-out, and passes a distribution-free sign test. It does not yet
survive friction. **That is a solvable problem. S1's was not.**

---

## 1. A LIVE BUG, FOUND AND FIXED

While auditing T1's friction I found that **0 of 2,972 T1 trades carried the
Phase 4A volatility-regime stress**, against 21.4% of S1's candidates. My first
explanation — that T1's trend gate excludes high-volatility bars — was **wrong**,
and I disproved it before reporting it. The merge itself was broken.

**Root cause, `s1_dual_model_orderflow.py:311` (now `t1_breakout.py:104`):**

```
4h cache 'time' dtype after to_datetime : datetime64[ms, UTC]   <-- [ms], not [ns]
.astype('int64') therefore yields       : MILLISECONDS  e.g. 1598918400000
pd.to_datetime(that, utc=True) assumes  : NANOSECONDS -> 1970-01-01 00:26:38
correct call                            : 2020-09-01 00:00:00
```

The `merge_asof` searched 1970-01-01 00:26 against a stress grid starting
2020-09-01, matched **0.00% of 13,200 bars**, returned NaN for all of them, and
the `np.where(np.isfinite(sm), sm, 1.0)` fallback silently converted every NaN to
1.0×. **T1 has never been stressed since Phase 4A was threaded in.** The S1 path
at `fast_numba_oos_engine.py:329` passes `unit="ms"` correctly, which is why only
T1 was affected.

| | match rate | mult distribution |
|---|---|---|
| before | 0.00% | `{1.0: 13,200}` |
| after | **99.99%** | `{1.0: 10,397, 1.5: 1,741, 3.0: 1,062}` |

Cost of the fix: **0.0316 R per trade**. T1's net expectancy moves from
−0.0510 R (as previously measured) to **−0.0826 R**. The fix makes T1 *worse*,
which is the correct direction for an honesty ledger.

A guard now raises instead of degrading:

```python
if _match_rate < 0.99:
    raise RuntimeError("T1 friction-stress join matched only ...% ... "
                       "This is the 1970-epoch unit bug returning -- "
                       "fix the join, do not paper over it.")
```

`scratch/test_friction_parity.py` section `[8]` tests this behaviourally, not
just textually — it asserts the stressed share exceeds 15%, so a silent
regression to all-1.0× fails the suite.

---

## 2. T1 STRUCTURE AUDIT — is 1R big enough to carry 41 bps?

```
1R = r_dist = 1.15 * max(4h ATR, 0.500% of price)
the 0.5% floor is STILL PRESENT in T1 (it was removed from S1 in Phase 2)
the floor binds on only 0.27% of T1 entries -> the 4h ATR is genuinely large,
the floor is not doing the work here
```

| 1R as % of price | value |
|---|---|
| p05 | 1.162% |
| p25 | 2.059% |
| **p50** | **2.884%** |
| p75 | 3.830% |
| p95 | 5.988% |

| friction, in R | p05 | p50 | p95 |
|---|---|---|---|
| base (41 bps) | 0.068 | 0.142 | 0.353 |
| stressed | 0.074 | 0.161 | 0.445 |

- Median friction **0.142 R = 14.2%** of the 1.0R stop (S1: 64.9% of a 1.2R stop).
- Mean stressed friction **0.199 R = 19.9%** of the stop.
- T1's risk unit is **5.47× S1's**, so the same 41 bps costs **3.91× less** of it.

**Conservative by construction:** `fill_px = open * (1 + side * 0.0010)` adds 10
bps of explicit entry slippage on top of `ROUND_TRIP_BPS = 41.0`, which already
contains ~25 bps of slippage. **T1 models ~51 bps per round trip, not 41.** That
overstates cost and therefore cannot inflate T1's result.

---

## 3. THE T1 AUTOPSY — gross vs net

n = 2,972 trades, 18 symbols, 16-bar (64 h) horizon.
Geometry: stop −1.0R / target +2.2R / ratchet (max_fav ≥1.40 → +0.85R, ≥0.75 → +0.35R).

```
mean gross exit_r = +0.116439 R     sd = 1.1602     n = 2,972
standard error    = 0.021283        t = +5.471      two-sided p < 1e-7
95% CI            = [+0.0747, +0.1582] R
```

**VERDICT: gross expectancy is significantly positive.** (S1, for comparison:
+0.0058 R, t = +0.849, p = 0.396 — a null.)

| outcome | n | share | gross R | net R | net WR | contributes |
|---|---|---|---|---|---|---|
| stop-out −1.00 | 1,313 | 44.18% | −1.000 | −1.201 | 0.0% | −0.5307 |
| be-lock +0.35 | 762 | 25.64% | +0.350 | +0.144 | 87.3% | +0.0369 |
| profit-lock +0.85 | 377 | 12.69% | +0.850 | +0.655 | 100.0% | +0.0831 |
| **target +2.20** | **486** | **16.35%** | **+2.200** | **+2.014** | **100.0%** | **+0.3293** |
| horizon timeout | 34 | 1.14% | +0.080 | −0.108 | 32.4% | −0.0012 |
| **TOTAL** | **2,972** | 100% | **+0.1164** | **−0.0826** | **51.8%** | **−0.0826** |

```
mean gross +0.1164 R  -  base friction 0.1674 R  -  stress surcharge 0.0316 R
                     =  -0.0826 R
```

Unlike S1, the ratchet here does not manufacture losing "winners": the be-lock
row is **+0.144 R net**, positive. The 1.0R stop is large enough that the 0.35R
lock clears friction. That is the whole structural difference between the sleeves.

### The edge is entirely the right tail

**Clip winners at +1.0R and gross expectancy goes from +0.1164 R to −0.0801 R
(t = −5.13).** Remove the +2.2R target row and the sleeve grosses −0.2433 R.

T1 is a convexity trade. The +2.2R target is not a tuning choice — **it is the
edge.** Any change that caps the upside destroys it. This is the single most
important constraint on future work here.

### Robustness — the tests we have been burned by before

| test | result |
|---|---|
| leave-one-year-out (7 fits) | never below **+0.0922 R**, t never below **+4.05** |
| leave-one-symbol-out (18 fits) | never below **+0.1095 R**, t never below **+4.90** |
| sign test (distribution-free) | 1641/2972 = **55.22%** positive, binomial **p < 1e-6** |
| median gross_r | **+0.3500 R** — not a few big winners |
| by side | LONG +0.1631 R (t=+4.58); SHORT +0.0870 R (t=+3.29) — both significant |
| per-symbol \|t\|>1.96 | 4/18 vs 0.9 expected by chance — broad, not concentrated |

By year individually: 2020 t=+2.38, 2021 t=+0.44, 2022 t=+1.36, 2023 t=+4.36,
2024 t=+3.44, 2025 t=+2.23, **2026 t=+0.49**. Four of seven years are
individually significant; the most recent year is not. The pooled result is
robust, but the edge is not uniform across time and **2026 shows none**.

---

## 4. WHAT WOULD IT TAKE TO BREAK EVEN

```
mean gross            = +0.1164 R
mean friction (fixed) =  0.1990 R      (19.9% of the 1.0R stop)
mean net              = -0.0826 R

friction must fall to 0.1164 R = 58.5% of current
  => 51 bps -> 29.8 bps break-even     (a 41.5% cost reduction)
or gross edge must rise 70.9%          (+0.1164 -> +0.1990 R)
```

**By regime — and this is where the actionable structure is:**

| stress | n | share | gross | friction | **net** | net WR |
|---|---|---|---|---|---|---|
| 1.0× | 2,316 | 77.9% | +0.1760 | 0.1749 | **+0.0011** | 54.8% |
| 1.5× | 428 | 14.4% | −0.0082 | 0.2126 | −0.2209 | 50.7% |
| 3.0× | 228 | 7.7% | **−0.2542** | 0.4189 | −0.6731 | 23.2% |

**In calm conditions T1 is already break-even.** The entire loss is concentrated
in the 22.1% of trades entered at ≥1.5× stress — and note the gross expectancy
there is *negative*, so it is not purely a cost problem: the breakout signal
genuinely reverses in volatility shocks (Welch t = +6.83 between the 1.0× and
3.0× groups on gross, p < 1e-6).

---

## 5. S1 REMOVED — what it was worth

Removed: `Engine/run_20_oos_dual_model.py` (deleted), `Engine/local_engine.py`
and `Engine/strategy/s1_dual_model_orderflow.py` (retired to `_retired_*`, still
importable so `scratch/diag_s1_autopsy.py` and the committed ledgers stay
reproducible). Added: `Engine/strategy/t1_breakout.py` (canonical T1) and
`Engine/run_t1_oos.py`.

**The new runner fits nothing.** No dataset compile (52,252 rows), no 18
LightGBM + 18 logistic models per window across 63 windows, no lightgbm or
sklearn import. T1 is rule-based, so there is no per-window fitting cost and no
in-sample contamination surface.

Both moves were verified rather than assumed:

- **Signal extraction:** old vs new `load_t1_breakout_trades`, 2,972 trades
  matched 1:1, **max \|Δr_gain\| = 0.000e+00**.
- **Executor:** T1-only vs the dual engine's T1 branch with an empty S1 list,
  8/8 windows **bit-identical PnL** (e.g. May 2021 +90.5432 both).

### T1-only OOS scorecard — disjoint windows, governor off, 41 bps + regime stress

| set | windows | passed | trades | PnL | ROI |
|---|---|---|---|---|---|
| Primary 2021-05→2023-02 | 22 | 1 | 386 | −1,233.98 | −24.68% |
| **Holdout 2023-03→2024-12** | 22 | 1 | 393 | **+97.75** | **+1.96%** |
| Expanded 2025-01→2026-08 | 20 | 1 | 373 | −783.08 | −15.66% |
| **POOLED** | **64** | **3** | **1,152** | **−1,919.30** | **−38.39%** |

Against the pristine dual-sleeve baseline of **−11,089.36 / 735 trades / 0 of
63**: removing S1 moved pooled PnL by **+9,170.06 USD with zero change to T1's
logic**.

Trade-level: mean net −0.0616 R, net win rate 51.22%, mean gross +0.1466 R on
1,152 executed trades at ~33 USD of risk each. **A −0.06 R/trade bleed, versus
S1's −0.71 to −0.82 R/trade.** Different disease entirely.

**The holdout is positive.** I want to be careful about what that does and does
not mean: it is the first positive number in this project that survives the
disjoint-window and per-symbol-decoupling repairs, and T1's gross edge is
independently significant at t=+5.47. But **1 of 22 windows passes**, the pooled
result is still negative, and the per-year table shows no edge in 2026. This is
not deployable and I am not presenting it as near-deployable.

---

## 6. THE OBVIOUS NEXT MOVE, TESTED AND REJECTED

The §4 regime table makes a `vol_rank` veto look irresistible. I tested it
against the bar you set in `L2_MICROSTRUCTURE_SPEC.md` §7 rather than proposing it.

| veto | drops | CVaR99 reduction | efficiency | p | tail improves |
|---|---|---|---|---|---|
| `vol_rank>=0.88` | 123 (10.7%) | +0.03289 | 2.40× | 0.1062 | 2/3 sets |
| `vol_rank>=0.80` | 157 (13.6%) | +0.06768 | 4.41× | **0.0067** | **3/3 sets** |
| `vol_rank>=0.70` | 245 (21.3%) | +0.16698 | 4.41× | **0.0000** | **3/3 sets** |

On the surface `vol_rank>=0.70` clears everything: 3/3 disjoint sets, p<0.0001
against a **day-clustered** random equal-size control. **It does not survive
inspection, and I am not proposing it.** Four reasons:

1. **The threshold is post-hoc.** I picked 0.70 after seeing the stress
   decomposition. `vol_rank>=0.88` — the pre-registered one — fails at p=0.1062,
   and has now failed three times (p = 0.0098, 0.1269, 0.0999, 0.1062).
2. **It is cost avoidance, not prediction.** The decisive test:

   | split at 0.70 | n | GROSS | net | mean fric |
   |---|---|---|---|---|
   | dropped | 245 | +0.0245 (t=+0.36) | −0.2400 | 0.2645 |
   | kept | 907 | +0.1796 (t=+4.48) | −0.0135 | 0.1931 |

   Welch t on **friction** = +6.37, p<1e-6. Welch t on **gross** = −1.95,
   **p=0.052** — marginal. The veto mostly avoids expensive trades rather than
   predicting bad ones, and `vol_rank` is by construction what sets the friction
   multiplier. It is the same trap as S1's `vol_strain`.
3. **It sits on the axis you formally abandoned.** You closed macro-regime
   filtering. This is macro-regime filtering with a better p-value.
4. **It does not reach profitability.** Pooled PnL: −1,919.30 → −740.76 (0.88),
   **−467.30** (0.80), −602.67 (0.70). Still negative at every threshold.

**Verdict: real, and still not good enough.** It is recorded here so the
measurement is not lost, not as a proposal.

---

## 7. WHAT THIS RULES IN

1. **T1 is the engine.** It is the only component in this repository with a
   statistically robust gross expectancy, and it is 5.47× better capitalised in
   risk units than the sleeve that was getting all the attention.
2. **The binding constraint is cost, not signal.** 51 → 29.8 bps, or +70.9% gross
   edge. Both are concrete targets; neither requires predicting anything new.
3. **The convexity is load-bearing.** The +2.2R target contributes +0.3293 of the
   +0.1164 R gross. Anything that caps upside — tighter targets, earlier
   profit-taking, volatility-based de-risking that shrinks the tail — destroys
   the edge. This constrains every future proposal.
4. **22.1% of entries are the whole problem**, and their *gross* expectancy is
   negative, not just their net.
5. **2026 has no edge** (t=+0.49, n=436). Whatever changed recently is worth
   understanding before any capital decision.

## 8. WHAT I DID NOT DO

- No tuning. The +2.2R target, the 1.15 ATR multiplier, the 0.5% floor, the
  ratchet levels, the six entry gates and the 4-bar spacing are all exactly as
  found. Every number here is a measurement of the existing engine.
- No gate proposed. §6 tested the obvious one and it failed the bar.
- The regime governor remains disabled and falsified (t = −0.148).

---

## 9. VERIFICATION

| check | result |
|---|---|
| `scratch/test_friction_parity.py` | **ALL ASSERTIONS PASSED**, sections [1]–[8], incl. 9 new T1 guards |
| `scratch/test_symbol_decoupling.py` | passes (now against the frozen S1 module) |
| signal extraction equivalence | 2,972 trades, max \|Δr_gain\| **0.000e+00** |
| executor equivalence | 8/8 windows bit-identical PnL |
| stress join match rate | **0.00% → 99.99%** |
| `diag_t1_autopsy` grid validation | 98.86% of trades land exactly on {−1.0, +0.35, +0.85, +2.2}; the 34 that do not are all horizon timeouts |

Code paths executed: `load_t1_breakout_trades`, `build_stress_series`,
`stress_multiplier`, `T1ExecutionEngine.simulate_execution`, and the full
`Engine/run_t1_oos.py` walk-forward across all 64 windows.

Two of my own claims were wrong this turn and are corrected above rather than
deleted: (a) that T1's zero stressed trades were a property of its trend gate —
it was a broken merge; (b) an initial `pd.cut` pooling that collapsed all three
window sets into one because window_ids repeat across files. The corrected
per-set table is in §5.
