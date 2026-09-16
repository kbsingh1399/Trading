# Phase 4A/4B — CVaR Harness + Regime-Dependent Friction Stress

**Branch:** `arena/01a0a5bf-trading`

---

## 1. Phase 4B — the CVaR99 harness

`Engine/strategy/cvar_gate_harness.py`, with `--dump-ledger` added to the runner and a
time-ordered trade ledger (`time`, `symbol`, `strat`, post-cost `r_gain`, `pnl`, `risk_usd`,
`vol_rank`, window id) returned from `simulate_execution`.

**Design.** CVaR_α is the mean of the worst `ceil((1-α)·n_FULL)` outcomes. The tail **count is
fixed from the full population** and reused for every subset, so a gate and a random control
that both drop *k* trades are scored identically. Recomputing the tail count on the shrunken
sample would let a gate look better merely by shrinking *n*.

**Sign convention — and the bug the tests caught.** CVaR on trade *returns* is negative, so an
improved tail is a *larger* number. My first implementation used `base - gated`, which made
every improvement negative and every efficiency ratio meaningless. The known-answer unit test
caught it. The convention is now `reduction = CVaR(S) - CVaR(FULL)`, positive == tail risk
reduced.

**A structural property worth knowing:** because the tail count is fixed and a veto only
*removes* trades, CVaR can never get worse. A veto that misses the tail scores **exactly 0.0**,
not negative. So the harness answers one question only: *what fraction of the tail does your
veto catch, relative to chance?*

**Verification — 8/8 unit checks pass.** CVaR against known answers (1.0 / 3.0 / 5.5 on 1..100);
`tail_count_for` (1058→11, 326→4, 50→1); empty gate → 0 reduction and undefined efficiency;
oracle gate → 99.9× at p=0.0000; off-tail gate → exactly 0.0; dropping the 5 *best* trades leaves
the worst-6 untouched → 0.0; partial gate lands strictly between 0 and the oracle; all five veto
spec parsers.

---

## 2. Phase 4A — regime-dependent friction stress

**The schedule was pre-registered before any backtest ran:**

| vol_rank | multiplier | bps |
|---|---|---|
| ≥ 0.88 | **3.0×** | 123.0 |
| ≥ 0.70 | **1.5×** | 61.5 |
| else | **1.0×** | 41.0 |

Thresholds are inherited from the regime governor so one definition of "high volatility"
governs the whole repository. The multiplier is applied in **both** numba kernels and in T1,
computed on the governor's own series (percentile rank of `trailing_30d_atr_pct` over trailing
365d of 4h bars).

**Zero lookahead, by construction:** the series is indexed by each 4h bar's **close** time
(`avail_time = open + 4h`), so an as-of join can only ever see a rank that was fully determined
before the joining bar opened.

**Defensive invariant:** `stress_multiplier()` returns ≥ 1.0 for every input including `None`,
`NaN`, non-numeric and negative values. Distribution over 13,200 4h bars: **78.77% at 1.0×,
13.19% at 1.5×, 8.05% at 3.0×**; blended average 50.3 bps.

**Control invariance passed:** with `STRESS_SCHEDULE` emptied, the primary set reproduces
**+315.90 / 326 trades / 3 passes** exactly. (Two failures along the way were mine: a stale
backup restore that clobbered my own fix, and a pandas-3.0 `datetime64[ms]` vs `[us]` merge-key
mismatch. Both fixed and re-verified.)

---

## 3. The fully-stressed baseline

| Window set | Trades | PnL | ROI | Pass | vs Phase 3 |
|---|---|---|---|---|---|
| Primary (20) | 359 | **+56.77** | +1.14% | 3/20 | −259.13 |
| Holdout (20) | 320 | **−953.39** | −19.07% | 1/20 | −865.36 |
| Expanded (25) | 456 | **−1,837.58** | −36.75% | 2/25 | **+320.91** |
| **POOLED (65)** | **1,135** | **−2,734.21** | — | **6/65** | **−803.59** |

Note the expanded set **improved** by 320.91 under a cost *increase*. That is not a paradox:
higher friction flips `realized_r` across zero, which changes labels, retrains the model, and
shifts selection and cooldown paths. It is the same non-monotonicity I found in the Phase-1
friction sweep, and it is a reason to distrust any single window set.

**Cumulative honesty ledger:**

| Stage | Pooled PnL |
|---|---|
| As originally reported | **+6,181.63** |
| + friction parity at 41 bps | −1,954.68 |
| + relief branch removed | −1,930.62 |
| **+ regime friction stress** | **−2,734.21** |

From +6,181.63 to −2,734.21 — a swing of **8,915.84 USD** — with no change to the alpha logic
whatsoever. Every dollar of it was cost-model and governance realism.

---

## 4. What the harness says — and why the headline p-value must be rejected

Pooled, n=1,135, tail_count=12, CVaR99 = **−3.2556 R**:

| Veto | Drops | CVaR99 → | Efficiency | p |
|---|---|---|---|---|
| **Oracle** (drop all 592 losers) | 52.16% | +0.0115 | 6.11× | — |
| `vol_rank >= 0.88` | 180 (15.86%) | −2.5522 | **4.82×** | **0.0098** |
| `vol_rank >= 0.70` | 265 (23.35%) | −2.5418 | 3.20× | 0.0303 |
| `strat == T1` | 750 (66.08%) | −3.2556 | **0.00×** | 1.0000 |
| `strat == S1` | 385 (33.92%) | −1.5748 | 5.13× | 0.0000 |

Three facts worth stating plainly:

**a) All tail risk lives in S1.** Every one of the 12 worst trades is S1 (0 T1). T1's 4h
Donchian geometry caps its losses; S1's 15m triple-barrier does not. Any tail-risk work should
target S1.

**b) The `vol_rank` veto is not a sleeve proxy.** It drops 41.7% S1 against a 33.9% base rate
(1.23× enrichment), and it **survives the S1-only control at 5.06×, p=0.0216**.

**c) It is robust to the tail width.** CVaR95 → 2.52× (p=0.0116); CVaR90 → 2.07× (p=0.0123).
Not an artefact of a 12-observation tail.

### But the per-set decomposition destroys it

| Set | n | tail | drops | Efficiency | p |
|---|---|---|---|---|---|
| Primary | 359 | 4 | **7** | 16.89× | 0.0394 |
| Holdout | 320 | 4 | 29 | **0.00×** | **1.0000** |
| Expanded | 456 | 5 | 144 | 3.01× | 0.0515 |

**The holdout shows literally zero effect.** The veto catches none of its tail. The pooled
p=0.0098 is carried entirely by primary and expanded, and the primary figure rests on **7
dropped trades against a 4-trade tail**.

**And the effective sample is 6, not 180.** Applying the 60-day gap rule, the 180 vetoed trades
fall into 6 temporal episodes:

```
2021-01..02 (64)   2021-06 (27)   2022-07 (3)   2024-02..05 (53)   2024-09 (26)   2026-03 (7)
```

These are **the same six volatility episodes** the regime governor was falsified on. The dataset
ceiling has not moved: n=6.

### Verdict

The harness worked exactly as intended. It produced a seductive pooled result (4.82×,
p=0.0098) and then, on decomposition, showed it resting on 2 of 3 window sets and 6 independent
episodes — with one set at exactly zero. **This is not an established effect and must not be
shipped.** It is the same trap as the Bayesian tracker and the governor, and the pooled p-value
was the thing that would have fooled us.

The correct conclusion is narrower and more useful: **tail risk is concentrated in S1, it is
partially predictable from the volatility regime, and this dataset cannot resolve the question
either way.** Settling it needs more independent volatility episodes than 5.7 years of data
contains.

---

## 5. Verification performed

- `scratch/test_friction_parity.py` — 30 assertions, 0 failures (friction parity, ATR floor
  removal, relief-branch removal).
- CVaR harness — 8 unit checks including known-answer CVaR values and the oracle/off-tail/
  perverse-gate boundary cases.
- Control invariance — stress disarmed reproduces +315.90 / 326 / 3 exactly.
- Both numba kernels and T1 confirmed charging the stressed cost; `stress_multiplier` ≥ 1.0 for
  all degenerate inputs.
- Full three-set re-run with per-trade ledgers; all harness numbers computed from
  `scratch/led_pooled.json` (1,135 rows).

## 6. Not verified

- The 6-episode ceiling means **no** tail-risk claim in this document is statistically
  established. I am reporting them as descriptive, not as evidence.
- Tripathi's 3× multiplier is his calibration for a different strategy and asset mix. I adopted
  it because it is the only published figure available, not because it is calibrated to ours.
- `scratch/led_pooled.json` totals −2,734.21 vs −2,734.20 summed from the three scorecards;
  the 1-cent difference is floating-point accumulation order, not a discrepancy.
