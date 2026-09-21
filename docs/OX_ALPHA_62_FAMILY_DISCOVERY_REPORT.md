# OX ALPHA 62 — STRATEGY-FAMILY DISCOVERY REPORT (pre-registered, honest)

**Date:** 2026-09-21 · **Protocol:** `docs/ox62_research/PROTOCOL.md` (written before any strategy
computation; 2 dated amendments) · **Result: best 1/20. No family passes. 20/20 REMAINS UNACHIEVED.**

## 1. DESIGN (why these numbers mean something)

Eight literature-prior rule-based entry families (Donchian, TSMOM, RSI-MR, MA-cross,
Keltner-cross, sweep-reclaim, KZ-drift, rule-FVG ablation) evaluated through the frozen verified
stack: shared live-spec exits (kernel `_ux_exit_*`), KZ + Friday gates, R_eff viability veto,
filed solo-sleeve replay at OX61 $50 economics. Families differ ONLY in entries.
- **PRIMARY:** single-shot full-20 at canonical params (zero selection DFs).
- **SECONDARY (pre-committed):** bidirectional 2-fold blocked-CV over registered 2-combo grids
  (fold A: select W01–W10 purged → score W11–W20; fold B mirrored). Every window scored unseen.
- Amendment 1: pre-window dev-gate infeasible (dense 15m begins ~W01; dev pool empty) → replaced
  by primary + CV. Amendment 2: 5-day fold-boundary purge for selection purity.
- 9/9 signal unit tests (trigger + no-lookahead + gates + F8/kernel equivalence) pass.

## 2. PRIMARY (single-shot, canonical params)

| Fam | Family | Pass | Pool n | Pool avgR | Pool WR% | PnL |
|---|---|---:|---:|---:|---:|---:|
| F1 | Donchian N=20 | 0/20 | 3,274 | −0.131 | 48.8 | −$2,479 |
| F2 | TSMOM K=60 | 0/20 | 27,096 | −0.005 | 55.8 | −$1,660 |
| F3 | RSI-MR X=30 | 0/20 | 57,952 | +0.002 | 56.6 | −$724 |
| F4 | MA-cross (12,48) | 0/20 | 283 | +0.013 | 55.5 | −$44 |
| F5 | Keltner k=2.0 | 0/20 | 1,396 | −0.112 | 49.6 | −$2,050 |
| F6 | Sweep-reclaim d=1.0 | **1/20** (W09) | 887 | −0.059 | 54.9 | +$198 |
| F7 | KZ-drift t=0.5 | 0/20 | 137 | −0.162 | 49.6 | −$634 |
| F8 | Rule-FVG (ablation) | 0/20 | 826 | −0.175 | 52.7 | −$2,172 |

## 3. SECONDARY (bidirectional CV; selection net-R in fold units)

| Fam | Fold-A sel → score W11–20 | Fold-B sel → score W01–10 | Total |
|---|---|---|---|
| F1 | N=55 → 0/10 | N=55 → 0/10 | 0/20 |
| F2 | K=20 → 0/10 | K=20 → **1/10** (W03) | **1/20** |
| F3 | X=30 → 0/10 | X=25 → 0/10 | 0/20 |
| F4 | (12,48) → 0/10 | (24,96) → 0/10 | 0/20 |
| F5 | k=2.5 → 0/10 | k=2.5 → 0/10 | 0/20 |
| F6 | d=1.0 → 0/10 | d=1.5 → 0/10 | 0/20 |
| F7 | t=0.5 → 0/10 | t=0.25 → 0/10 | 0/20 |
| F8 | — → 0/10 | — → 0/10 | 0/20 |

Folds agree on params in only 3/7 gridded families (instability = no persistent edge). F6's primary
W09 (+20.8R, 72.7% WR — a genuinely good window, not a grind artifact) does not replicate under
holdout. F2's CV pass (W03, K=20 selected on W11–W20, scored on W01–W10) is the lone honest
holdout pass in the program.

## 4. FINDINGS

1. **Pools cluster at ~zero-or-negative (−0.17R … +0.01R).** Nothing approaches the +0.3–0.5R/trade
   needed for 20/20. The live-spec stack (R_eff veto + far structural TPs + full-stop exits) grinds
   every entry family to dust: F7/F8 keep only ~1–8% of raw signals post-veto.
2. **Positive pool ≠ passing windows.** F3's pool is +91R over 58k trades yet scores 0/20 (−$724
   replay): the concurrency-throttled subset + freeze dynamics dominate. Expectancy without
   window-level robustness fails the criteria by design.
3. **Honest ML-lift measurement:** F8 full-setup pool (−0.175R) vs walk-forward ML subset (−0.118R):
   the ML gate adds ≈ +0.06R of honest lift inside the setup pool. Real, but far from enough.
4. **No 20/20 by luck is possible (p ~ 1e-16); none was found.** The two lone passes (F6/W09
   primary, F2/W03 CV) are consistent with chance across 8 families × 20 windows.

## 5. CONCLUSION + LEGITIMATE NEXT OPTIONS

Per the pre-registered failure policy: all scorecards published, no window iteration, program STOPPED.
Designing further rounds FROM these outcomes (e.g. "RSI-MR variants") would be test-tuning and is
explicitly out of bounds. Legitimate continuations, in honesty order:
  (a) **Future-data program** (recommended): collect post-window dense 15m, develop there, treat the
      20 windows as frozen validation. Only path to a credible 20/20 claim.
  (b) **Independently-justified round 2:** fresh literature priors (not window-inspired), new
      pre-registration, disclosed cumulative multiplicity. Expected value: low (see §4.1).
  (c) **Higher-timeframe ML** with 2015–2023 development data (new exit sim + verification battery
      required; honest trains would be small).
  (d) **Re-score under tip $10 economics** (expected 0/20 everywhere — the +10% ROI target is
      unscaled; documents the risk-calibration interaction, nothing more).
