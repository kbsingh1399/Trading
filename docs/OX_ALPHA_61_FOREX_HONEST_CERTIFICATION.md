# OX ALPHA 61 — HONEST CERTIFICATION REPORT (FOREX DUAL-SLEEVE)

**Date:** 2026-09-21 · **Branch:** `arena/01a0bf23-trading` · **Certification: PERFORMANCE EVIDENCE NEGATIVE — 1/20. Funded-live deployment WITHHELD.**

This report closes the OX61 mandate loop honestly. The 20/20 goal was **not achieved**, and every
legitimate avenue within the no-fabrication mandate has been exhausted. All scorecards below regenerate
**to the byte** from committed code (R4), and every historical claim was re-measured under causal,
walk-forward discipline (R6).

---

## 1. PINNED RESULT (R4 primary: live-spec dual, walk-forward, gate 0.55)

Generator: `docs/ox61_verification/run_ox61_r4.py` → `scorecard_r4_pinned.csv`
(`r4_manifest.json` pins commit, configs, library versions, seeds, and artifact sha256;
`run_ox61_r4.py --check-only` reproduces all artifacts **to the byte**.)

| W | Window | Trades | WR% | Net R | ROI% | DD% | Status |
|---|---|---:|---:|---:|---:|---:|:---:|
| 01 | Late 2023 Fed Higher-for-Longer Pause | 70 | 47.1 | −2.48 | −4.72 | 4.72 | FAIL |
| 02 | Q4 2023 Year-End Soft Landing Rally | 23 | 34.8 | −7.02 | −4.73 | 4.73 | FAIL |
| 03 | Q1 2024 Global Disinflation Surge | 27 | 51.9 | −0.76 | −1.41 | 4.41 | FAIL |
| 04 | Early 2024 Tech & Index Expansion | 27 | 37.0 | −3.92 | −2.13 | 4.59 | FAIL |
| 05 | Spring 2024 Geopolitical Energy Spike | 30 | 33.3 | −6.17 | −4.45 | 4.58 | FAIL |
| 06 | ECB Rate Cut Pivot & Dollar Strength | 17 | 29.4 | −4.18 | −2.82 | 4.57 | FAIL |
| 07 | Mid-2024 High-Beta Equity Distribution | 22 | 40.9 | −3.23 | −0.90 | 4.49 | FAIL |
| 08 | August 2024 Global Carry Trade Flash Unwind | 22 | 31.8 | −5.36 | −4.51 | 4.51 | FAIL |
| 09 | Fed 50bps Jumbo Rate Cut Ignition | 22 | 36.4 | −6.98 | −4.48 | 4.75 | FAIL |
| 10 | US Presidential Election Mega Breakout | 213 | 47.9 | +5.06 | +11.99 | 3.91 | **PASS** |
| 11 | Year-End Cross-Currency Flow Rebalancing | 10 | 20.0 | −7.96 | −4.51 | 4.51 | FAIL |
| 12 | Post-Inauguration Trade Policy Realignment | 22 | 45.5 | −3.14 | −1.41 | 4.48 | FAIL |
| 13 | Spring 2025 Precious Metals All-Time High | 13 | 38.5 | −7.01 | −3.71 | 4.47 | FAIL |
| 14 | Late-Cycle Yield Curve Steepening | 36 | 44.4 | −5.90 | −3.08 | 4.59 | FAIL |
| 15 | European Macro Slowdown & CNH Divergence | 24 | 45.8 | −1.60 | −0.01 | 4.33 | FAIL |
| 16 | Late-Summer Commodity Volatility Expansion | 17 | 23.5 | −5.86 | −4.51 | 4.51 | FAIL |
| 17 | Autumn 2025 Global Liquidity Injection | 52 | 44.2 | −4.95 | −3.33 | 4.69 | FAIL |
| 18 | Q4 2025 Industrial Metals & Indices Momentum | 95 | 50.5 | +2.78 | −4.40 | 4.76 | FAIL |
| 19 | Q1 2026 New Year Cross-Asset Range Shift | 30 | 33.3 | −5.84 | −4.78 | 4.78 | FAIL |
| 20 | March 2026 Modern Microstructure Shock | 27 | 29.6 | −7.37 | −4.82 | 4.82 | FAIL |

**Totals: 1/20 PASS · PnL −$2,636.00 · maxDD 4.82%.** Criteria: ROI ≥ +10%, Net R ≥ +2.5R,
WR ≥ 40%, Trades ≥ 15, DD ≤ 5%. Drawdown never binds; ROI/Net-R bind everywhere except W10.

Threshold-sensitivity bands (R4 criterion 2): gate 0.53 → 1/20 (−$1,756); 0.55 → 1/20 (−$2,636);
0.57 → 1/20 (−$2,003). The single pass (W10) is gate-stable; totals move only via S4/ORB
concurrency-crowding. The 0.54-vs-0.55 gate ambiguity (prompt/engine-class vs sleeve/live) is
retired as immaterial: no gate in [0.53, 0.57] changes the verdict.

---

## 2. HONEST SCOREBOARD (all configurations, same 20 windows, same replay)

| Configuration | Pass | PnL | Pool edge | Verdict |
|---|---:|---:|---:|---|
| Dual, live-spec + walk-forward (R4 PRIMARY) | 1/20 | −$2,636 | — | fails |
| Dual, filed-spec + walk-forward (R4 sibling) | 0/20 | −$2,672 | — | fails |
| ORB-only, corrected sim | 0/20 | −$2,655 | −0.121R | fails |
| S4-only, filed-spec + walk-forward | 1/20 | +$147 | −0.056R | fails |
| S4-only, live-spec + walk-forward | 0/20 | netR −32.4 | −0.118R | fails |
| Dual, in-sample S4 (VOID reference) | 0/20 | −$2,086 | — | void (contaminated) |
| Legacy `perfect_20_oos_dual_sleeve_results.csv` | 20/20 | +$13k | — | **VOID: orphan, irreproducible, superseded by R4** |

Every honest configuration fails 19–20 windows by hard freeze (−4.4% to −4.8% DD everywhere).
Pools need +0.2–0.4R of honest selection lift for 20/20; demonstrated honest lift is ~0
(filed AUC 0.50–0.54; walk-forward fit-AUC decays 1.00 → 0.80/0.97 as trains grow).

---

## 3. WHAT WAS PROVEN (voids filed evidence)

1. **Sentinel fabrication (ORB edge entirely fake).** Joining the filed ORB cache against the
   corrected sim on asset+datetime (18,778 matched): 8,867 exact-stop trades were scored −0.2308R
   instead of −1.08R (+0.8492R each = **+7,529.7R fabricated**). Pool swings +0.2979R → −0.1211R
   (Δ +0.419R closes exactly). TP/truncation outcomes are bit-identical (rewrite verified).
2. **Production XGB is test-contaminated.** Its ~5,400-label train set sits ~98% inside the 20
   windows (only ~8 months of dense pre-window 15m exist; pre-2023 bars are ~260/yr daily
   snapshots). Filed 70–90% WRs = memorization. Walk-forward retrain (R6, bar-purged, seed 42)
   is the only honest ML measurement: WR collapses to 54%, pools go negative.
3. **Live-spec FVG sleeve barely trades — by live's own rule.** Live `calculate_adaptive_sl_tp`
   enforces R_eff ≥ 2.50 (verified constant; docstring "1.20" is stale). Entries sitting on swept
   extremes yield median R_eff ≈ 0.8 → **~88% of ML setups are vetoed live**, a gate the filed
   backtest (fixed 2.5R TP) never applied. Survivors hold far targets that almost never fill:
   97% stopped, pool −0.118R.
4. **The W10 pass is an ORB-subset timing interaction, not S4 alpha.** W10 dual-unified executes
   208 ORB + 5 FVG trades (vs 81 ORB under placeholder S4 holds). S4-unified-alone scores 0/20;
   W10 ROI *rises* as S4 signals *fall* across gates (less crowding → more of W10's winning ORB
   subset taken). Deterministic and reproducible — but fragile interaction, not edge.
5. **No honest ML-development path exists on this data.** Honest early trains are tiny
   (W01 = 118 precommitted / 10 unified labels); iterating on the 20 windows = test-tuning.
   Certification math + density audit are in §2 and the session record.

---

## 4. LIVE FIXES (post-scoring, mandated pair — tested, no behavior change to scoring)

- **FIX 1 — ratchet rollover-drop** (`Engine/forex_engine.py` OrderManager): the phase gate was
  pre-advanced before the 21:55–22:15 UTC rollover lockout, so a lock triggered during rollover
  (or a failed `modify_sl`) was **dropped forever** while state claimed it applied. Fix: roll
  `ratchet_phase`/`ratchet_desc` back on suppression or failure so the lock retries. Tests
  F1a/b/c PASS.
- **FIX 2 — S4 sweep** (`Engine/strategy/s4_fvg_ml/*.py`, both copies): streaming `generate_signal`
  omitted the liquidity-sweep leg its own docstring, backtest, labeler, and live dry-run require.
  Fix: delegate to canonical `check_setup_criteria` (KZ+sweep+FVG+trend) + `HOLD (No Sweep)` reason.
  Tests F2a/b PASS (F2a yields `BUY (Adaptive 2.68R Struct)`).

---

## 5. VERIFICATION TALLIES

- MANDATE 1 causality (12/12): next-bar-open entries behavioral (both labelers) + ORB source;
  D1/H4 shift(1) + backward-asof source; streaming 4H availability-boundary behavioral
  (transition exactly at bar-close+4h); daily-shift discriminator behavioral; no static caches;
  generators pinned for every artifact; R6 480-bar embargo exact on W01/W10/W20.
- MANDATE 3 ratchet parity: trigger/lock schedule identical across kernel + both order managers
  (C5). **Known residual:** trigger variable differs (kernel: bar extreme; engine: current gain_r;
  live: highest_r) — disclosed, out of mandate, flagged for follow-up.
- Exit-sim units: ORB parity U1–U6 (7/7), unified labeler V1–V10 (11/11), live fixes F1–F2 (5/5).
- R4: `--check-only` reproduces all pinned artifacts **to the byte**. R6: walk-forward with
  pre-committed hyperparams (depth 4 / lr 0.05 / 120 rounds / seed 42), 96/480-bar purge.

---

## 6. R4/R6 CLOSURE + SUPERSESSION

- **R4 CLOSED:** generator committed (`run_ox61_r4.py`, delegates to `run_ox61_r6.py` A/B/C);
  pinned CSVs + threshold bands + manifest committed; legacy
  `Engine/research/perfect_20_oos_dual_sleeve_results.csv` **deleted in the same commit**
  (no competing artifacts).
- **R6 CLOSED:** per-window walk-forward retrain published for both specs; production-model
  in-sample contamination documented and quarantined from all honest scorecards.

## 7. KNOWN RESIDUALS (disclosed, out of mandate — do not affect the verdict)

Gain-vs-highest trigger divergence (§5); 0.54 vs 0.55 gate constants (§1, retired by bands);
`ICTFVGStrategy`/`CombinedStrategy` sweep-less predicates (legacy paths, not in filed dual);
dry-run has no ORB-sleeve path (live/paper vs backtest scope gap); risk-machine path sensitivity
(W18: +2.78R → −4.40% ROI; W10-precommitted: +7.05R → +0.59% ROI); midnight-exclusive window-end
semantic (legitimate reading, kept).

## 8. RECOMMENDATION

**Funded-live deployment remains WITHHELD.** Code mechanics are certified; performance evidence is
negative under every honest configuration. The only legitimate forward path is new research on
future (post-window) data: re-collect dense 15m, re-train out-of-sample, and re-certify against
these same frozen windows — which must then be treated as *validation*, never as development data.
