# OX63 — INSTITUTIONAL MICROSTRUCTURE PROTOCOL (pre-registered)

**Objective:** implement the mandated 2-stage scaling engine + F6R refinement and grade it against
institutional portfolio standards (Sharpe ≥ 1.50, PF ≥ 1.35, DD ≤ 10%, positive completed-year PnL).
**Status:** written BEFORE any OX63 computation. Deviations require a dated amendment.

## 1. EVIDENCE GRADING (honesty)

F6 was selected for refinement because of its OX62 W09 (+20.8R) — outcome-informed selection, and
OX62-CV showed it does not replicate (0/20). OX63 evidence is therefore graded
**EXPLORATORY-CONFIRMATORY HYBRID**: the refinements are structural priors (scaling mechanics,
MSB doctrine), evaluated single-shot with full reporting. Portfolio metrics are the claim;
per-window tables are disclosure. **Funded-live still requires future-data validation.**

## 2. FROZEN (certified — must stay green)

- Kernel: `create_labels_ratchet`, `create_labels_unified`, `_ux_exit_*`, `UX_RATCHET`,
  `MIN_R_MULTIPLE` (2.50), all existing cols/joins. Additive-only changes permitted.
- Suites: 35 ox61 + 9 ox62 + 8 execution-safety. `test_prelaunch` baseline: TEST 1–5 green,
  TEST 6 crashes pre-existing (missing legacy root files) — must not newly break.
- R4 byte pins must still reproduce (`run_ox61_r4.py --check-only`) after kernel changes.

## 3. IMPLEMENTER'S PRE-COMMITMENTS (values the mandate left open)

- **P1 (TP1):** TP1_R = 1.10 (mandate range 1.00–1.20 → midpoint), TP1_FRAC = 0.50,
  post-TP1 SL lock Entry ± 0.15R (mandated).
- **P2 (friction):** stays 0.08R/trade (split closes move the same total volume; no new constant).
- **P3 (MSB):** 20-bar 4H-close Donchian break on the shifted as-of series
  (`close_4h[i] > max(close_4h[i-20:i])`, NaN → False). Canonical 20-bar horizon.
- **P4 (viability):** veto R_eff < 1.20 (mandated); cap 3.50 kept; fallback 2.5R kept;
  floor/cap/Friday-entry/KZ rules unchanged.
- **P5 (scaled-sim bar order):** gap-SL → SL(state-dependent) → TP1 → runner-SL(new lock) →
  TP2 → Friday (full remainder) → decay (remainder) → ratchet locks → same-bar reversal.
  SL-first conservative doctrine throughout. Gap through TP1 banks at TP1 exactly (no surplus).
- **P6 (decay):** unchanged rule (highest < 0.2 @ ≥24 bars) applied to the remainder
  (full pre-TP1, runner post-TP1); highest = position-highest.
- **P7 (ratchet):** post-TP1 phase starts at 1; schedule continues on position-highest.
- **P8 (R accounting):** R = 0.5×1.10 + 0.5×runner_R − 0.08. Pre-TP1 full exits: certified math.
- **P9 (live managers):** per-trade `scaled`/`banked_r` (+ derived `tp1_price`), `.get` defaults
  for old states. TP1 evaluated on tick gain_r ≥ 1.10 BEFORE the ratchet block: `close_partial(0.5)`
  (new, dry_run/live branches), set scaled/banked, and the EXISTING ratchet cascade moves SL to
  +0.15R same-tick (highest ≥ 1.1 ≥ 0.8 ⇒ phase 1; rollover-rollback fix covers suppression).
  TP1 suppressed during rollover (10–50× spreads invalidate limit math) with retry. Applies to
  BOTH managers (forex_engine + live/order_manager) for backtest/live parity.
- **P10 (4H col):** kernel adds `close_4h_asof` (shift(1) + backward-asof, existing pattern).
- **P11 (F6R):** F6{d:1.0} with `htf>0` → `(htf>0 | msb_bull)` (long), mirror short. Else identical.
- **P12 (decomposition):** monolithic-2.5R sim vs scaled sim on IDENTICAL F6R signals (counterfactual
  labeled, never selected).
- **P13 (portfolio):** continuous equity from concatenated per-window executed trades (filed replays,
  no mechanics change). Sharpe = daily-resample, rf=0, ×√252. PF = gross+/gross−. maxDD on
  continuous equity. Annual PnL: 2024 + 2025 completed; 2023-Q4 + 2026-Q1 disclosed partials.
  Survivability: (a) liveness after any 4.5% window, (b) portfolio maxDD ≤ 10%.
- **P14 (verdict):** conjunction — standards must hold under BOTH $50 research AND $10 production
  economics. Single-shot; no bands; reruns only for the determinism proof.
- **P15 (repro):** `run_ox63.py` + `manifest_ox63.json` + `--check-only` byte proof.
- **P16/P17:** §2 green + R4 pins reproduce.

## 4. MANDATE-1 TARGET REPLACEMENT (scope note)

The portfolio standards REPLACE the per-window +10% criterion for OX63 grading only. The
`target_oos_criteria.json` window thresholds stay untouched (other owners' calibration); per-window
PASS/FAIL is reported as disclosure. No window-iteration is performed under any criterion.

## 5. AMENDMENTS

- **A1 (2026-09-21, pre-compute clarification):** P13 Sharpe = Mon–Fri daily returns only
  (Sat/Sun excluded: no market, no weekend holds via Friday closeout), rf = 0, ×√252, on
  running start-of-day equity. Annual PnL = calendar-year sums of filed executed pnl
  (2024/2025 completed years gated; 2023/2026 disclosed partials). Union rule: windows are
  contiguous and non-overlapping (verified: W01 2023-09-15 → W20 2026-03-31, each starts the
  day after the prior ends), so the portfolio stream is the global time-sort of filed
  per-window executions with no dedup needed; each candidate executes in exactly one window.
- **A2 (2026-09-21, pre-compute clarification):** P9 implementation sets the TP1 SL lock
  (+0.15R) by direct assignment plus a phase floor of 1, rather than relying on the existing
  ratchet cascade to derive it same-tick. Economically identical (same SL price, same phase,
  same tick); chosen for determinism. Rollover suppression + retry preserved. Applies to both
  managers. The live mirror additionally skips the redundant stage-1 cascade re-fire
  post-TP1 (lock already at +0.15R).
