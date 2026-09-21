# OX62 — HONEST STRATEGY-FAMILY DISCOVERY PROTOCOL (pre-registered)

**Objective:** find a strategy family passing all 20 OOS windows (ROI≥+10%, R≥+2.5R, WR≥40%,
trades≥15, DD≤5%) under rules that make any success *mean* something.
**Status:** written BEFORE any development-data computation. Deviations require a dated amendment.

## 1. HONESTY ARCHITECTURE

1. **Pre-registration:** families, exact formulas, param grids, dev-span rule, selection metric,
   and eval procedure are fixed in this file before results exist.
2. **Development data = pre-window only.** Per-asset dev span (rule, data-driven):
   `dense_start` = first timestamp of the first 30-calendar-day window containing ≥2000 15m bars;
   dev = [dense_start, W01_start − 5 days]. Asset in dev pool iff span ≥ 60 days.
   The 5-day purge covers the max live-spec hold (~4.5d); belt-and-braces for rule-based code.
3. **Single-shot evaluation.** Locked params → one candidate generation over [W01_start, data_end]
   → one replay per window. No iteration on windows, no re-entry, no peeking-then-fixing.
4. **Frozen mechanics.** Replay = filed `ParallelForexStrategy` path (max-2 concurrent, cluster
   limits, freeze, risk multipliers). Exits = verified live-spec sim (kernel `_ux_exit_*`,
   shared by all families). Families differ ONLY in entries. Solo-sleeve eval (no dual combos).
5. **Full reporting.** All 8 families reported win-or-lose. F8 is graded ABLATION (its components
   were observed on windows inside S4); F1–F7 are graded CLEAN (literature priors + dev gate).
6. **Multiple testing.** 8 families × 1 shot. P(20/20 | zero edge) ~ 1e-16 per family — any 20/20
   is statistically significant; the dev gate + tiny grids + full reporting control researcher DFs.
7. **Known contamination vector (disclosed):** the researcher's memory of 2023–2026 regimes is
   implicit lookahead. Mitigations: literature priors, dev-gate, ≤2 combos/family, full reporting.
8. **Economics:** evaluate at OX61 economics (base_risk_usd=50, per MANDATE 2's 4-tier budget the
   replay was designed for). The tip criteria ($10, unscaled +10% ROI target) is incoherent for
   discovery (needs +50R/window); the override is recorded in the manifest. Any winner is ALSO
   shown at $10 for disclosure.

## 2. SHARED ENTRY/EXIT SPEC (all families)

- Signal bar `i` uses bars ≤ `i` only; entry at `opens[i+1]`; KZ required on signal bar
  (hour 7–10 / 12–15 UTC); Friday entry veto on entry bar (Fri & hour ≥ 18, per live lockout).
- Raw SL anchor: trailing 20-bar extreme incl. signal bar (kernel `local_low/high_20`, = live
  `buffer[-20:]`); `r = max(|entry − anchor|, 1.5 × ATR14[i])`; 2.5% cap; structural TP from the
  opposite 20-bar extreme with R_eff ∈ [2.5, 3.5], viability veto below 2.5, 2.5R fallback.
- Exits: kernel `_ux_exit_long/_ux_exit_short` (6-lock ratchet on extremes, highest-R decay @24,
  Friday 20:30 closeout, gap-aware unclamped stops, same-bar reversal). Friction 0.08R.
  Data-end truncation → NO candidate (boundary discipline).
- Features reused causally from `engineer_features_polars`: OHLC, ATR14, RSI14, htf_4h_trend
  (shifted), sweep flags (shifted), KZ. EMAs/Donchian/Keltner computed trailing-only in-harness.
- Universe: canonical 18 (pre-existing; no asset selection).

## 3. FAMILIES (exact formulas; HH_N/LL_N exclude current bar)

- **F1 Donchian:** LONG if C[i] > max(H[i−N:i]); SHORT if C[i] < min(L[i−N:i]). Level-based.
  Grid: N ∈ {20, 55}.
- **F2 TSMOM:** retK = C[i]/C[i−K] − 1. LONG if retK > 0; SHORT if retK < 0. K ∈ {20, 60}.
- **F3 RSI-MR:** LONG if RSI14[i] < X; SHORT if RSI14[i] > 100 − X. X ∈ {25, 30}.
- **F4 MA-cross:** LONG event if EMA_f[i] > EMA_s[i] and EMA_f[i−1] ≤ EMA_s[i−1]; SHORT mirror.
  (f,s) ∈ {(12,48), (24,96)}.
- **F5 Keltner-cross:** mid=EMA(C,20); upper/lower = mid ± k·ATR14. LONG event on close crossing
  above upper; SHORT mirror below lower. k ∈ {1.5, 2.5}.
- **F6 Sweep-reclaim:** PDL/PDH[i] = prior-calendar-day extremes (causal groupby-shift(1)).
  LONG if sweep_pdl[i]==1 and C[i] > PDL[i] and (H[i]−L[i]) > d·ATR14[i] and htf[i] > 0; SHORT
  mirror. d ∈ {1.0, 1.5}.
- **F7 KZ-drift:** on the last hour-10 bar of each day: drift = C[i] − O[first hour-7 bar same day]
  (skip day if absent). LONG if drift > t·ATR14[i]; SHORT if drift < −t·ATR14[i]. t ∈ {0.25, 0.5}.
- **F8 Rule-FVG (ABLATION):** `check_setup_criteria(row)` → LONG/SHORT. No grid.

## 4. SELECTION, LOCK, EVAL

- **Dev metric:** pooled dev net-R (Σ r_realized, all dev assets); tiebreak: Sharpe of daily dev R.
- **Lock:** best combo per family → `LOCK.json` (params + code/data hashes). No other dev use.
- **Eval:** per family, candidates on [W01_start, data_end] → solo replay × 20 windows → scorecard.
- **Success battery (any 20/20):** (a) behavioral causality tests for its signal code; (b) byte
  determinism rerun; (c) ±1-notch param sensitivity (reported, not selected); (d) boundary audit;
  (e) live-parity review. Then R4-style pin.
- **Failure policy:** publish all scorecards; no window iteration; recommend future-data program. STOP.

## 5. AMENDMENTS

**Amendment 2 (2026-09-21, before any CV computation):** fold-boundary purge for the §(ii)
secondary. T_mid = W11 start. Fold-A selection set = signals in [W01_start, T_mid − 5d)
(the 5d trailing purge keeps exit realization from importing fold-B prices into the selection
metric); scored on W11–W20. Fold-B selection = signals ≥ T_mid (exits run forward, never touch
fold-A dates — no purge needed); scored on W01–W10. Selection metric per fold = Σ r_realized
over the selection set (tiebreak: Sharpe of daily fold R). Scoring via the frozen replay's own
window-date filter. Single-combo F8 is re-sliced, not re-selected.

**Amendment 1 (2026-09-21, before any strategy computation):** the §1.2 dev-gate is INFEASIBLE.
Measured per the registered rule: dense 15m coverage begins ~2023-09-05 (EURUSD/NZDUSD/AUDCHF),
2023-09-11/12 (EURHUF/USDSEK/USDHKD/EURSEK), or mid-2024 (8 assets); NICKEL/LEAD never reach
2000 bars/30d. Dev pool under the ≥60-day rule = EMPTY (W01 starts 2023-09-15). §4 SELECTION is
replaced with:
  (i) **PRIMARY:** single-shot full-20 evaluation at canonical literature-default params
      (zero data-driven selection, zero selection DFs). Canonical: F1 N=20 (trade-viability
      under the 15-trade criterion); F2 K=60 (~1 session-day); F3 X=30 (Wilder); F4 (12,48);
      F5 k=2.0 (Keltner midpoint); F6 d=1.0; F7 t=0.5; F8 as-is.
  (ii) **SECONDARY (pre-committed, runs regardless):** bidirectional 2-fold blocked-CV using the
      registered §3 grids. Fold A: select on W01–W10 (pooled fold net-R) → score W11–W20. Fold B:
      select on W11–W20 → score W01–W10. Each window is scored by params that never saw it;
      combined 20/20 = full coverage under holdout. Claims graded PROCEDURE (family + rule).
- Data-boundary rule: signal datetimes clipped to ≤ 2026-03-31 (max window end); XAUCNH shows
  post-span timestamps (data quirk, excluded by the clip; flagged for audit).
- All else (§1.3–1.8, §2, §3 formulas, §4 lock/eval mechanics, §5 battery/failure policy) FROZEN.
