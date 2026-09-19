# OX_ALPHA_46 — Forensic Audit of the C1–C13 Remediation

**Target:** `kbsingh1399/Trading` @ `main` (`4159134`)
**Auditor:** Arena.ai agent · **Date:** 2026-09-20
**Verdict: 3/10. NOT CERTIFIED for live deployment.**

Real engineering happened here — this is a genuine improvement over `182845a`,
and several fixes are correct and verified below. But the headline claim is
**refuted by running the pinned code**, and 4 of the 13 findings are reported
resolved when they are not.

A note on independence: this audit reviews remediation of *my own* OX_ALPHA_45
findings, and the harness being validated is code I wrote. I have therefore
weighted execution evidence over code-reading, and the most damaging finding
below is one **against** my own prior result.

---

## Part 1 — The headline claim is refuted

The directive's primary benchmark:

> 1,924 trades, +2,857.10 USD, +0.1085 R/trade, **t = +4.46** vs Bonferroni
> 3.17 → **SURVIVES**

I executed `Engine/validation/holdout_test.py` unmodified from `main`:

```
  Holdout trades     : 3,455
  Holdout PnL        : +1,194.21 USD  (+23.88%)
  Holdout expectancy : +0.0217 R/trade   t = +1.56
  Windows PASS/PROFIT: 1/9  |  3/9
  Bonferroni t-bar at alpha=0.05 : 3.17
  Observed holdout t             : +1.56  -> DOES NOT SURVIVE
  Bootstrap: ROI p05/p50/p95 -3.83% / +16.60% / +54.63%
             MaxDD p95/p99   14.31% / 17.96%
             P(net loss)     10.96%
```

**The edge does not survive Bonferroni correction.** t = +1.56, less than half
the claimed +4.46 and well under the 3.17 bar. P(net loss) is 10.96%, not 0.04%.
Max DD p95 is 14.31%, not 5.97%.

### Provenance of the three different numbers

| | Trades | PnL | R/trade | t | Verdict |
|---|---|---|---|---|---|
| **A** My original (12-feature model, `bdbe31b`) | 1,915 | +3,007.59 | +0.1393 | **+5.69** | survives |
| **B** Directive OX_ALPHA_46 claim | 1,924 | +2,857.10 | +0.1085 | +4.46 | claimed survives |
| **C** **What `main` actually produces** | 3,455 | +1,194.21 | +0.0217 | **+1.56** | **does not survive** |

`holdout_test.py` is byte-identical between `main` and my branch, so the harness
is not the cause. The cause is upstream: `main` merged my later ADX/Hurst regime
features into `FEATURES`, changing the model from 12 to 15 inputs. That shifted
config selection from `Forex only` to `Full Multiverse` (crypto included), which
is why trade count jumps 1,915 → 3,455 and expectancy collapses.

**B is reproducible from neither state.** It sits near A but matches nothing.

### This invalidates the holdout as a statistical instrument

A strict holdout is a **single-shot** test. It has now been evaluated at least
three times (A, B, C) across changing feature sets. Each re-evaluation consumes
its validity; the Bonferroni correction for 65 configs no longer covers the true
search. **This applies to my own result A as much as to the directive's B** —
I am retracting A as a certifiable number. It was honestly produced, but the
holdout it relied on is now spent.

---

## Part 2 — Finding-by-finding scorecard

| # | Finding | Claim | Verified status |
|---|---|---|---|
| C1 | Missing numba engine | RESOLVED | ✅ **Genuinely fixed** |
| C2 | Untracked S2 sleeve | RESOLVED | ⚠️ **Partial — file exists, is dead code, has a bug** |
| C3 | Result beats hindsight oracle | RESOLVED | ⚠️ Claims purged from docs, `20/20` strings persist in code |
| C4 | Cosmetic regime routing | RESOLVED | ✅ Real governance exists (my harness) |
| C5 | Purge boundary leakage | RESOLVED | ❌ **NOT FIXED — still `open_time_ms`** |
| C6 | Per-window tuning comments | RESOLVED | ❌ **NOT FIXED — all 4 sites intact** |
| C7 | Bar count overstated | RESOLVED | ✅ Corrected to 2,323,304 |
| C8 | 17-digit hyperparameters | RESOLVED | ✅ **Genuinely fixed** (`num_leaves=15`) |
| C9 | Non-compounding capital | RESOLVED | ✅ Disclosed |
| C10 | S3 intrabar + profit floor | RESOLVED | ✅ **Genuinely fixed** |
| C11 | Test suite | 56/56 | ⚠️ 54 passed, 1 skipped, 1 file uncollectable |
| C12 | Implied gross edge | — | ✅ Superseded; real edge now measured at +0.0217 R |
| C13 | W23 "Live Production" | — | ❌ Label still present |

### ✅ C1 — Genuinely fixed

`Engine/core/fast_numba_oos_engine.py` is tracked. The runner imports
`from Engine.core.fast_numba_oos_engine import ...`. It executes and compiles
real data:

```
Completed Multi-Asset Numba Compilation: 35,388 candidates in 7.00 seconds!
```

This was the single worst finding in OX_ALPHA_45 and it is properly resolved.

### ✅ C8, C10 — Genuinely fixed

`num_leaves=15` now matches `max_depth=4`; `C=0.03`, `learning_rate=0.04`,
`reg_alpha=2.0` — the 17-digit optimizer output is gone, as is the
`Trial #24641 Champion` comment.

In `s3_orb_ml.py`, both loops now read `for k in range(entry_bar + 1, trade_end)`
(lines 228, 358), the stop is checked before the target, and
`outcome_r = max(cur_r, 0.15)` is **absent from the file**. Correctly done.

### ❌ C5 — NOT FIXED (directive states the opposite)

The directive says: *"Training data masks across all models now filter strictly
on trade completion: `exit_time_ms < start_ms - PURGE_MS`."*

`Engine/run_20_oos_multiverse.py` line 171, on `main` today:

```python
train_mask = all_data.open_time_ms < (start_ms - PURGE_MS)
```

Unchanged from `182845a`. Training trades that open before the cutoff but close
inside the OOS window still leak. (My `honest_walkforward.py` does purge
correctly on `exit_time` at line 675 — but that is my file, not the runner.)

### ❌ C6 — NOT FIXED (directive states the opposite)

The directive says these were *"purged from production code."* They are at four
live sites in `Engine/strategy/s3_orb_ml.py`:

```
167: # ATR-Capped Range & Stop Cap (Upgrade #3 for W6 liquidation expansions)
219: # Dynamic BE trigger for compressed ATR regimes (Upgrade #4 for W18)
297: # ATR-Capped Range & Stop Cap (Upgrade #3 for W6 liquidation expansions)
349: # Dynamic BE trigger for compressed ATR regimes (Upgrade #4 for W18)
```

W6 and W18 are OOS windows. The parameters they describe are still in the code.

### ⚠️ C2 — S2 exists but is dead code with the C10 bug

`Engine/strategy/s2_mean_reversion.py` (186 lines) is tracked and well built:
next-bar open fill (`entry_bar = i + 1; entry_p = opens[entry_bar]`), adverse
stop checked before target, real `exit_time`, friction deducted.

Two problems:

1. **Nothing imports it.** `grep -rln "s2_mean_reversion" --include=*.py Engine/`
   returns nothing. The runner does not reference it. The sleeve that accounted
   for 88.1% of the original claimed book is present but never executed.
2. **It carries the exact bug C10 fixed in S3.** Lines 99 and 146:
   `for j in range(entry_bar, entry_bar + horizon_bars)` — starting *at*
   `entry_bar`, whose open is the fill price, so that bar's own high/low can
   trigger an exit. S3 was fixed to `entry_bar + 1`; S2 was written with the
   defect intact.

### 🔴 NEW — N1: the runner still crashes, and T1 is structurally dead

`python3 Engine/run_20_oos_multiverse.py` from a clean tree:

```
Completed Multi-Asset Numba Compilation: 35,388 candidates in 7.00 seconds!
Traceback (most recent call last):
  File "Engine/run_20_oos_multiverse.py", line 154, in main
    df_t1_pure = engine.load_t1_breakout_trades()
  File "Engine/strategy/s1_dual_model_orderflow.py", line 306
    df_t1 = pd.DataFrame(all_t1_trades).sort_values("time")
KeyError: 'time'
```

`all_t1_trades` is empty, so the DataFrame has no columns. Root cause in the
**newly promoted** `Engine/core/multi_tf_data.py`, lines 60–61:

```python
df_4h['buy_vol_ratio'] = 1.0
df_4h['spot_cvd_slope'] = 0.0
```

Both are hardcoded stubs. The T1 entry condition requires
`cvd_slope > 0` (long) or `< 0` (short), and `buy_vol > 0.51` / `< 0.49`. With
`spot_cvd_slope ≡ 0.0` and `buy_vol_ratio ≡ 1.0`, **no T1 trade can ever
trigger.** Verified empirically: `spot_cvd_slope` nonzero count = 0/13,200.

So "zero scratch dependency" was achieved by replacing a missing module with one
that returns constants. Fresh-clone reproducibility (mandate item 1) **fails.**

### ⚠️ C11 — 54 passed, 1 skipped; claim of 56/56 not reproducible

```
54 passed, 1 skipped in 3.33s   (with test_prelaunch.py excluded)
```

- `test_prelaunch.py` — the claimed "1 passed / 18 compliance sub-checks" —
  **cannot be collected on Linux**: it imports `Engine.forex_engine`, which
  imports `MetaTrader5`, a Windows-only package.
- Collection also required manually installing `polars`, `xgboost`, `lightgbm`.
  **There is no `requirements.txt` in the repo.**

Contradicts "executes self-contained from a clean git clone."

### ❌ C3, C13 — residual strings

```
Engine/run_20_oos_multiverse.py:105  "MASTER 20 OOS MULTIVERSE AUDIT: 20/20 CERTIFIED QUAD-SLEEVE STRATEGY"
Engine/generate_institutional_pdf_report.py:24  "Windows Passed": "20/20"
Engine/oos_windows_20.json:180  "Q3 2026 Live Production Regime"
```

A report generator still emits "20/20" as a certified figure.

---

## Part 3 — Answers to the audit checklist

**1. Clean git clone execution — FAIL.** The numba engine is tracked (real
progress), but the runner crashes at `load_t1_breakout_trades()`, no
`requirements.txt` exists, four packages needed manual install, and one test file
is uncollectable on Linux.

**2. Causality & anti-lookahead — MIXED.** S3 entry/exit causality is correct and
verified. `honest_walkforward.py` fits thresholds train-only and purges on
`exit_time`. But the runner's purge is still on `open_time_ms` (C5), and the new
S2 module ships the intrabar bug.

**3. Microstructure frictions — ADEQUATE in the validated path.** The honest
harness uses measured per-symbol costs (median 0.135 R; EURUSD 0.013 R to
USDTHB 28.1 R), which is the correct treatment and far better than a blanket
figure. S2 deducts a flat 0.25 R, defensible for perpetuals.

**4. Statistical integrity — FAIL.** t = +1.56 against a 3.17 bar. The edge does
not survive. Separately, the holdout has been consumed by repeated evaluation
and is no longer a valid single-shot instrument for *any* party, including me.

**5. Certification score — 3/10.**

Points awarded: C1 (the critical blocker) genuinely fixed; C8 and C10 correctly
fixed; per-symbol cost modelling sound; the team engaged honestly with adverse
findings and removed the inflated claims from documentation.

Points withheld: the headline benchmark is refuted by its own code; C5 and C6 are
reported fixed but are not; the runner does not run; T1 is silently disabled by
stub features; S2 is dead code carrying a known bug.

---

## Part 4 — What is actually true about this system

Stripped of claims, running today's `main`:

- **Holdout: +0.0217 R/trade, t = +1.56 → not significant.**
- 1 PASS / 9 windows; 3 profitable.
- Bootstrap P(net loss) 10.96%; MaxDD p95 14.31%.

My own previously-reported +0.1393 R / t = +5.69 was measured on a 12-feature
model that `main` no longer runs, and on a holdout since re-used. **I am
withdrawing it as a certifiable result.**

The defensible summary is: *no statistically significant edge has been
demonstrated on untouched data.*

## Part 5 — Required before re-audit

1. Fix C5 for real: `exit_time_ms < start_ms - PURGE_MS` in the runner.
2. Delete the four "Upgrade for W6/W18" parameters, or declare those windows
   in-sample.
3. Implement `buy_vol_ratio` / `spot_cvd_slope` or delete T1 — do not ship stubs
   that silently disable a sleeve.
4. Fix S2's loop bound to `entry_bar + 1`, and either wire S2 into the runner or
   state that it is unused.
5. Add `requirements.txt`; make `test_prelaunch.py` skip cleanly without
   `MetaTrader5`.
6. Remove the residual `20/20` strings from the runner and PDF generator.
7. **Do not re-report the holdout t-statistic.** That dataset is spent. Reserve a
   genuinely untouched period (e.g. 2026-Q3 onward), pre-register the config and
   the metric, and evaluate exactly once.
