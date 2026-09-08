# RP2 ROUND 12 — Throughput-Calibrated Regime-Adaptive Engine

Status: **mechanically verified, 126/126 invariants. Real-data performance UNVALIDATED.**
The 2.2 GB corpus is unreachable from the authoring sandbox (egress blocked, MCP
contents API rejects files over 1 MB). Only the local run against
`Engine/binance_backtesting_data/` produces a scorecard. Nothing in this document
claims a pass.

---

## 1. The feasibility frontier (read this before tuning anything)

ROI > +20.0% on 5,000 USD requires +1,000 USD. Max DD < 5.0% caps the peak-to-trough
budget at 250 USD. The ratio of those two numbers is the governing constraint:

    n * E[R] / L_max  >  4.0

where `n` is trades per window, `E[R]` is net expectancy in R, and
`L_max = log(n(1-wr)) / log(1/(1-wr))` is the expected longest losing run.

| wr | tp | n | E[R] | L_max | ratio | verdict |
|----|----|---|------|-------|-------|---------|
| 0.40 | 4R | **15** | +0.90 | 4.3 | **3.14** | **INFEASIBLE** |
| 0.40 | 4R | 25 | +0.90 | 5.3 | 4.24 | feasible |
| 0.40 | 4R | 100 | +0.90 | 8.0 | 11.23 | feasible |
| 0.45 | 4R | 15 | +1.15 | 3.5 | 4.89 | feasible |

Monte Carlo (6,000 trials/cell, flat risk optimised), P(pass) per window and the
20-window conjunction:

| n | wr | risk | P(window) | P(all 20) |
|---|----|------|-----------|-----------|
| 15 | 0.40 | 1.30% | 27.97% | 8.6e-12 |
| 60 | 0.44 | 0.40% | 76.30% | 4.5e-03 |
| 100 | 0.40 | 0.40% | 83.63% | 2.8e-02 |
| 100 | 0.44 | 0.35% | 95.40% | 3.9e-01 |
| **100** | **0.48** | **0.35%** | **98.60%** | **7.5e-01** |

Three consequences drove every decision below.

1. **Trade count is the dominant lever.** `L_max` grows logarithmically while edge
   accumulates linearly. Moving 15 → 100 trades shifts the conjunction by ~10 orders
   of magnitude. **The 15-trade mandate floor sits BELOW the feasibility boundary
   (ratio 3.14). The design target is ~90-100 trades per window, not 15.**
2. **Optimal risk FALLS as trade count rises** (1.30% → 0.35%). Raising risk to reach
   +20% is exactly backwards — it breaches the DD cap long before it reaches the ROI.
3. **The ML overlay's only job is win rate.** 0.40 → 0.48 at n=100 moves P(all 20)
   from 2.8e-02 to 7.5e-01, a 27x gain — worth more than any sizing change. This is
   why lowering `min_train_events` is the highest-value directive in the brief.

---

## 2. THE ROUND 11 KILL SWITCH (root cause of 10 trades / 20 months)

Round 11 shipped `max_friction_r = 0.22`. The entry gate is:

    (rt_friction * entry) / r_unit  <=  max_friction_r

With 41 bps round-trip friction that demands `r_unit / entry >= 0.0041 / 0.22 =
1.864% of price` — on a **15-minute bar**.

Measured stop-distance distribution of actual emitted candidates:

| percentile | stop / price | friction cost |
|------------|--------------|---------------|
| p5   | 0.2120% | 1.934 R |
| p25  | 0.2920% | 1.404 R |
| p50  | 0.3888% | 1.055 R |
| p75  | 0.5314% | 0.771 R |
| p95  | 0.9229% | 0.444 R |
| p100 | 1.1146% | 0.368 R |

**Candidates satisfying the gate: 0 of 58.** Not a threshold that was too strict —
an unconditional kill switch. Entry-gate census before the fix:

    {'friction_reject': 58}     # 100% of candidates, every window

This is the dominant cause of Round 11's failure, and **none of the three root
causes in the Round 12 brief touch it.** No relaxation of `disp_atr_mult`,
`arm_expiry_bars` or `conf_min_score` could ever have reached it: those parameters
govern candidate *production*, and every candidate produced was destroyed downstream
at *consumption*.

### The derived fix

`max_friction_r` was re-derived, not fudged. Maximising `ratio = n * E_net / L_max`
with `E_net = E_gross - rt_friction/s`, throughput concurrency-bound at
`n = slots * 2880 / hold` and `hold ~ (tp*s/atr)^2`:

| stop % | friction_R | hold bars | n | E_net | ratio (wr=0.40) |
|--------|-----------|-----------|---|-------|-----------------|
| 0.35% | 1.171 | 16 | 240 | -0.171 | fail |
| 0.50% | 0.820 | 33 | 176 | +0.180 | 4.60 |
| **0.70%** | **0.586** | **64** | **90** | **+0.414** | **4.77** |
| 1.00% | 0.410 | 131 | 44 | +0.590 | 6.30 |
| 1.25% | 0.328 | 204 | 28 | +0.672 | 5.17 |

Sized on the **pessimistic** wr = 0.40, one configuration holds across the band:

    wr 0.40 -> n~90  E_net +0.414R  ratio  4.77  PASS
    wr 0.44 -> n~90  E_net +0.614R  ratio  8.18  PASS
    wr 0.48 -> n~90  E_net +0.814R  ratio 12.46  PASS

Shipped: `max_friction_r = 0.60` (stop floor 0.683% of price). The optimum is a
**plateau**, not a knife edge — ratio exceeds 4.0 for stops from 0.40% to 1.25%.

Second, and more important structurally: **a too-tight stop is now WIDENED to the
viable floor rather than discarding the setup.** Risk is unaffected — position size
is `qty = risk / r_unit`, so a wider stop simply buys fewer units. The setup
survives and friction is bounded by construction.

Ordering matters and is invariant-locked (11.11): `min_stop_atr/max_stop_atr` is a
**structure-quality** filter and is evaluated on the raw swing stop; the friction
floor is an **execution** constraint applied afterwards. Applying the floor first
caused the band to re-reject the very stops just repaired, losing 38 of 58
candidates. The ML feature vector keeps the *structural* stop distance so the model
sees setup geometry, not an execution artefact.

Result on the fixture, one 28-day window, 2 symbols:

    before: 58 candidates -> 0 admissible ->  0 trades
    after : 58 candidates -> 58 admissible -> 18 trades

---

## 3. Correction: house-money sizing is the drawdown killer

The brief directs retaining house-money (banked-profit) sizing. **The arithmetic
contradicts this.** At n=100, wr=0.44:

| sizing | P(pass) | p95 DD |
|--------|---------|--------|
| house money (0.35% base, kelly 0.42, cap 2.0%) | 0.02% | 28.40% |
| house money (kelly 0.18, cap 0.9%) | 13.92% | 12.87% |
| **flat 0.35%** | **95.40%** | **4.62%** |

Compounding risk into a hard drawdown cap is self-defeating: the mechanism scales
position size precisely when the equity high-water mark is highest, which is exactly
when the DD denominator is largest. **Resolution: the mechanism is retained and
switchable (`--house-money`), but `flat_risk_mode` defaults True.** This is an
arithmetic correction to the mandate, made explicitly and not silently.

---

## 4. Correction: `orderflow_cover` is NOT asset availability

The brief states the 0.72-0.78 cover figures are "just asset availability,
14/18 = 77.7%, safe to ignore." Every reported value is an **exact integer symbol
ratio**:

    11/14 = 0.7857 -> 0.786      12/16 = 0.7500 -> 0.750
    11/15 = 0.7333 -> 0.733      13/17 = 0.7647 -> 0.765
                                 13/18 = 0.7222 -> 0.722

All five distinct reported values match exactly. Cover is a per-bar mean averaged
across *loaded* symbols, so this means 3-5 symbols scored **precisely zero**.
Newly-listed symbols cannot explain it — they are excluded upstream by the row-count
guard and never enter the average. Manifests confirm the ladder files are ~100%
tick-complete (BTC 210,809 / 210,883). **The ladder join is failing silently.**

Accepting the brief's explanation would have left 4-5 symbols permanently dark —
every orderflow-gated setup on them unreachable — while the cover number looked
plausibly like listing history.

Two silent failure paths existed in `load_symbol`: a missing file, and a pyarrow
predicate-pushdown returning zero rows without raising. Rather than guess which,
Round 12 makes the loader **defensive and fully diagnostic**:

- `LADDER_ALIASES` + `_normalise_ladder_columns()` — alias mapping, datetime64→ms
  and seconds→ms coercion.
- Full-read fallback when pushdown returns empty.
- Merge row-count assertion and merge-hit check.
- Status recorded per symbol: `LADDER_OK`, `LADDER_FILE_MISSING`,
  `LADDER_EMPTY_IN_RANGE`, `LADDER_MERGE_MISS`, `LADDER_BAD_SCHEMA`.
- The runner **refuses to report performance when any symbol is dark** unless
  `--allow-dark` is passed deliberately.

---

## 5. Three structural state-machine defects

None are addressed by the brief's parameter directives.

- **Defect A — one global arm slot per symbol.** `arm_side` was a single scalar.
  While any setup was armed, the symbol was blind for up to
  `arm_expiry_bars + 24 = 36` bars — including to the opposite side.
  Fix: multi-arm (`max_active_arms = 4`, `allow_dual_side_arms = True`).
- **Defect B — arm destroyed on the first confirmation miss.** Both reclaim branches
  ended in unconditional `arm_side = 0`. Throughput was `p` instead of `1-(1-p)^k`;
  at p=0.30, k=3 that is 0.30 vs 0.657 — a **2.2x loss, multiplicative with
  Defect A**. Fix: `reclaim_max_attempts = 3`.
- **Defect C — no re-arm on the disarm bar** (every disarm path ended in `continue`).
  Fix: arming is attempted on the same bar as a disarm.

**Concurrency capacity was binding.** Capacity = `max_concurrent * 2880 / hold_bars`.
At 2 slots: 36 bars → 160 trades, 60 → 96, 150 → 38, 300 → 19. Round 11's 672-bar cap
admitted at most ~19 trades/window even with infinite signal. Shipped:
`hold_max_bars = 288`, `chop_hold_max_bars = 144` (both exceed the 64-bar implied
time-to-target at the stop floor, invariant 11.18). `max_concurrent` stays at 2 per
mandate.

---

## 6. Calibration delta (Round 11 → Round 12)

| parameter | R11 | R12 | rationale |
|-----------|-----|-----|-----------|
| `max_friction_r` | 0.22 | **0.60** | derived; 0.22 rejected 100% of candidates |
| `widen_tight_stops` | — | **True** | widen, don't discard |
| `flat_risk_mode` | False | **True** | house money breaches the DD cap |
| `flat_risk_pct` | — | **0.0035** | frontier optimum |
| `kelly_frac` | 0.42 | 0.18 | retained but de-fanged |
| `risk_cap_pct` | 0.020 | 0.009 | |
| `disp_atr_mult` | 1.45 | 1.10 | per brief |
| `arm_expiry_bars` | 12 | 32 | per brief |
| `conf_min_score` | 3.0 | 2.0 | per brief |
| `min_train_events` | 300 | **70** | ML was 100% silenced; now trains |
| `hold_max_bars` | 672 | 288 | concurrency capacity |
| `chop_hold_max_bars` | 192 | 144 | |
| `max_active_arms` | 1 | 4 | Defect A |
| `reclaim_max_attempts` | 1 | 3 | Defect B |
| `pullback_min/max_atr` | 0.25/1.30 | 0.20/1.60 | |

ML confirmed active on the fixture: `train_events 74`, `reason ok`, `AUC 0.929`
(Round 11: silenced in every window).

---

## 7. Funnel telemetry contract

Round 11 produced 10 trades with no way to locate the loss. Round 12 emits a funnel
per window. Sequential chain (`armed → pullback_seen → reclaim_trigger →
confirm_pass → stop_viable → trades`) is chained and the **binding constraint** —
the steepest survival drop — is named. Terminal counters (`confirm_fail`,
`stop_reject`, `expired`, `structure_disarm`, `depth_disarm`) are reported separately
and never chained. A `candidates > 0 but trades == 0` condition raises an explicit
alarm pointing at the entry gate — the exact Round 11 signature.

---

## 8. Anti-lookahead compliance

Unchanged from Round 11 and re-verified: all features shifted 1 bar; 72-hour purge
before `window_start`; GBDT bin edges and Ridge mean/std fitted on train only and
immutable at test; no per-window lookup tables; entries fill at the **next** bar's
open; stop resolved before target intrabar; drawdown marked worst-case intrabar with
exit slippage and fee.

## 9. Verification

    python Engine/verification/verify_rp2_round12.py     # 126/126, no perf metrics
    python Engine/runners/run_rp2_round12_walkforward.py \
        --data-dir Engine/binance_backtesting_data \
        --windows  Engine/oos_windows_20.json \
        --out      rp2_round12_results.json

The verifier prints **no** performance metric by design (invariant 9.1). The runner
is the only route to a scorecard, and it will abort rather than report performance
over dark symbols.
