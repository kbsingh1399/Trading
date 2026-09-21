# OX ALPHA 54 — Forensic Audit & Verification of the Master Forex & CFD Pipeline

**Auditor role:** Principal Quantitative Architect & Forensic Systems Auditor (isolated session; every finding reproduced from first principles)
**Repository:** `kbsingh1399/Trading` — branch `arena/01a0bf23-trading` @ `44c3bef`
**Engine under audit:** `Engine/forex_engine.py` (2,931 lines) + `Engine/core/base_strategy.py`, `Engine/core/strategy_kernel.py`, `Engine/FVG_ML_ForexCFD_Strategy.py`, `Engine/ORB_CRT_ForexCFD_Strategy.py`, `Engine/live/{run_forex_dry_run,order_manager,mt5_connection,inference_engine}.py`
**Audit date:** 2026-09-20 UTC
**Method:** line-by-line code inspection + live reproduction (installed `pyarrow/pandas/xgboost/polars/numba/matplotlib`; executed both sleeves across all 20 OOS windows)

---

## 0. Executive Verdict: **REVISE — NOT CERTIFIED. Do not deploy.**

The directive's empirical scorecard (§3: *"20/20 passes, +$16,420.50, peak DD 3.84%, W1: 106 trades / +$731.80 / DD 3.47%"*) is **irreproducible and contradicted by the repository's own code and filed results**. My independent reproduction of the actual strategy modules gives:

| Sleeve | My reproduction (true criteria: ROI≥10%, DD≤5%, WR≥40%, N≥15, R≥2.5) |
|---|---|
| ORB/CRT (rules-only, no ML) | **2/20 PASS** — DD breaches 5% in **18 of 20** windows (5.4%–12.0%, on DD accounting that *understates*); 555–1,423 trades/window; ROIs +117% to +457% per ~6-week window at flat $50 risk with zero concurrency limits |
| FVG/ML (production XGBoost) | **15/20 PASS — but IN-SAMPLE**: the production model was trained on all data including the test windows; fails W02/W03/W04 (DD −22.94%)/W06/W19 anyway; WRs of 70–90% vs walk-forward WR ~45–65% confirm overfit |

A dual-sleeve concatenation of the above cannot pass 20/20 with 3.84% peak DD — ORB alone breaches 5% in 18 windows with 10–100× the claimed trade counts. The cited evidence file `Engine/research/perfect_20_oos_dual_sleeve_results.csv` **does not exist**, and the filed CSVs that *do* exist (`oos_20_windows_forex_results.csv`, `dynamic_oos_results.csv`) show failures, DDs to 9.8–17%, and a lax `Status` definition (`ROI>0 & DD≤4.5` — not the institutional criteria).

Beyond the scorecard, I found **one critical live-safety bug** (drawdown measured from initial balance, not peak — the DD governor can never arm once profitable), **one live-crash bug** (`sig.side` AttributeError on sleeve conflict), **complete risk-parity breakdown** (four different risk regimes: directive fiction vs backtest flat-$50/unlimited vs live-engine 25/15/35/2-slot vs dry-run flat-$25/3-slot/no-governor), and **no bar-by-bar interleaved backtest anywhere** (the claimed `precompute_candidates` + chronological arbitration + `FOREX_CLUSTER_MAP` symbols: zero matches in the codebase).

**Ratings:** Architecture **5/10** · Causal Soundness **4/10** · Microstructure Realism **3/10** · Production Readiness **3/10**.

The system has a genuinely good kernel core (causal feature discipline, 4H/D1 shift handling, ORB next-bar-open fills, live operational safeguards). It needs a remediation cycle, not abandonment. Full backlog in §6.

---

## 1. Claim-vs-Evidence Forensics (directive claims vs repository reality)

| Directive claim | Forensic result |
|---|---|
| `Engine/strategy/s4_fvg_ml/s4_fvg_ml_forex_engine.py`, `Engine/strategy/orb_crt_forex_engine.py` | **DO NOT EXIST.** Real files: `Engine/FVG_ML_ForexCFD_Strategy.py`, `Engine/ORB_CRT_ForexCFD_Strategy.py` |
| `precompute_candidates()` + bar-by-bar chronological interleaving in `forex_engine.py` | **DOES NOT EXIST** (zero grep matches). Backtests delegate per-sleeve; `ParallelForexStrategy.run_backtest` merely concatenates trade lists. No concurrency/cluster enforcement in any backtest path |
| `FOREX_CLUSTER_MAP`, 4 clusters (EUR/Pacific/Indices/Commodities+USDSEK) | **Symbol does not exist.** Actual: `CORRELATION_CLUSTERS`, **5** blocs, different membership (USDSEK∈USD_BLOC; XAUCNH/GAUCNH∈CNH_BLOC) |
| 5-tier risk: base $50, house $65 @+$80, mild $27.50 @1.8%, severe $16.50 @3%, milestone lock $7.50 @+$500/15tr | **FICTION.** Live engine: base $25, defense $15 @2%, house $35 @+$100 & DD<1%, hard freeze @4.5%, **no milestone lock anywhere**. Backtests: flat $50, no tiers. Dry-run: flat $25, no governor at all |
| Max 2 concurrent (backtest claim) | Backtests enforce **zero** concurrency control (ORB: 1,423 overlapping trades/window). Live engine: 2. Dry-run manager: **3** |
| `Engine/research/perfect_20_oos_dual_sleeve_results.csv`, `perfect_20_oos_dual_sleeve_equity_curve.png` | **DO NOT EXIST.** Filed results show failures (see §1.1) |
| W1: 106 trades, 62.3% WR, +45.63R, +$731.80, DD 3.47% | **Reproduced instead:** ORB W1 = 597 trades, +$8,691, DD −9.92% (FAIL); FVG W1 = 36 trades (in-sample), +$978, DD −1.65%. Combined ≈ 633 trades, DD breach. Claimed figures match nothing |
| 20/20, +$16,420.50 (+328.41%), peak DD 3.84%, avg 120.5 trades/qtr | **Contradicted.** ORB alone fails 18/20 on DD with 555–1,423 trades per ~45-day window (not "quarterly" — windows average 46 days) |
| Fill strictly at `opens[j+1]` | True for ORB only. **FVG labeler fills at signal-bar close** (`entry = closes[i]`, `strategy_kernel.py:390,438`) |
| Spread + 8bps friction deducted | ORB/`run_standard_backtest`: flat **−0.08R** (≈$4/trade — units mislabeled, it's R not bps). **FVG: zero friction.** No backtest uses the spread column (live-only) |
| 96-bar purge & embargo protocol | Helper `get_causal_train_test_split` defined but **never called** (dead code). Windows are contiguous (no gaps). Production model trained on all data → OOS backtests are in-sample for the ML filter |
| `dynamic_oos_results.csv` pools | Different universe (HK50/CHINAH/JP225/…), DDs to 17% — irrelevant to the 18-asset claim |
| Leaderboard AUCs | 0.504–0.536 — model is barely above coin-flip; filed WRs of 70–90% are inconsistent with this except via in-sample overfit |

### 1.1 What the filed walk-forward benchmark actually says (`oos_20_windows_forex_results.csv`)

Proper per-window retraining + 24h purge, but: uses an 18-feature stacking ensemble (not production XGBoost), credits flat **±2.0R/−1.0R** instead of real exit prices, lax `Status`. Under **true** criteria: W01 fails ROI (3.9%); W02 fails ROI+DD(9.57%)+WR; W03 catastrophic (−8.9%, WR 13.3%); W04 fails DD (6.3%); W05 fails ROI. Even this flattering harness passes only ~15/20.

---

## 2. Directive 1 — Lookahead & Information Leakage Audit

### 2.1 PASS (with credit): feature engineering causality
- 15m features (RSI/EMA/VWAP/FVG/ATR/vol/ROC): trailing-only, causal. FVG expressions reference bars ≤ i only.
- **4H join:** Polars path shifts 4H EMA200-slope by 1 bar before backward as-of; Pandas streaming path uses availability-time (+4h) merge_asof — both yield the last *closed* 4H bar. Equivalent (verified by construction). The `shift(1)` + asof is single-lag, not double-lag — correct.
- **D1 PDH/PDL:** shift(1) / availability-time (+1d) — previous closed day only. Correct.
- RSI/ATR are ewm/range-mean variants rather than Wilder — nonstandard but **self-consistent** across batch/streaming paths (parity harness `run_verify` asserts <1e-9; design is sound).

### 2.2 FAIL: FVG close-fill (`strategy_kernel.py`, `create_labels_ratchet`)
`entry = closes[i]` on the signal bar. Live cannot transact the close after observing it. Every FVG backtest trade carries close→next-open optimism (gap + spread). ORB does it correctly (`opens[entry_bar]`). **Fix:** FVG entry at `opens[i+1]` ± half-spread from the filed spread column.

### 2.3 FAIL (critical): in-sample production model reused as OOS filter
`dynamic_retrain()` and `train_production_model.py` train on **all history, no date split, no purge**. `FVGMLForexCFDStrategy.run_backtest` loads this booster and scores every OOS window with it. The 24h-purge benchmark (`run_forex_20_oos_benchmark.py`) retrains per window properly — but evaluates a *different* model (stacking ensemble, 18 features, binary ±R outcomes), so **no filed artifact evaluates the production model out-of-sample**. The 70–90% FVG win rates vs 0.52 leaderboard AUC are the fingerprint of this leak.

### 2.4 FAIL: TP-before-SL ordering in `run_standard_backtest` (`forex_engine.py`)
Intra-bar check order: time-decay → **TP (2.5R) → SL**. Same-bar SL+TP ambiguity resolves to TP (favorable). Must be SL-first (as the ORB kernel and labeler correctly do).

### 2.5 MARGINAL: same-bar ratchet activation in the FVG labeler
SL-hit is checked before TP (good), but the ratchet locks intra-bar excursion (`highs[j]`) effective for bar j+1 — assumes the high preceded any reversal within bar j. Live (tick-level) can genuinely do this, so parity is *approximate*, not broken — but the conservative choice is next-bar activation. Recommend sensitivity run.

### 2.6 Note: EMA warmup in ORB backtest
EMAs seed at the window's first close (sliced before simulation) — first ~200 bars/window have unsettled EMA200 trend filter. Mild; fix by prepending 500-bar warmup (data starts 2015–2020, plenty available).

---

## 3. Directive 2 — Portfolio Interleaving & Concurrency: **the claimed system does not exist**

- **No `precompute_candidates`, no chronological bar-by-bar portfolio loop, no `FOREX_CLUSTER_MAP` exist in the codebase** (verified by exhaustive grep). §1's "HIGH-THROUGHPUT EXECUTION & PORTFOLIO INTERLEAVING" describes unfiled code.
- What exists: per-sleeve independent backtests + `pd.concat` + sort-by-datetime. Consequences, all empirically demonstrated:
  - **Unbounded portfolio heat:** every setup takes full $50 risk simultaneously (ORB W18: 1,423 concurrent-overlapping trades; theoretical concurrent heat in the thousands of percent).
  - **DD computed on closed-trade equity only** (no intra-trade MTM) in all three backtest paths — structurally understates drawdown; ORB still breaches 5% in 18/20.
  - Live vetoes (2–3 slots, 1/asset, 1/cluster, rollover/Friday, quarantine, margin) bind **zero** backtest trades.
- **Deterministic arbitration: untestable** — the arbitration code is live-only (`place_market_order` vetoes, dry-run prob-sorted queue). The live vetoes themselves are correctly ordered (rollover → Friday → margin → slots → duplicate → cluster) and deterministic for simultaneous signals (Python dict order + prob sort). That logic is fine; it simply has no backtest counterpart, so **no filed number estimates live fill rates**.

---

## 4. Directive 3 — Dynamic Risk State Machine: **four mutually inconsistent regimes, one safety-critical bug**

| Regime | Base | Defense | House | Freeze | Milestone lock | Concurrency |
|---|---|---|---|---|---|---|
| Directive §2 (claimed) | $50 | $27.50@1.8% / $16.50@3% | $65@+$80 | 4.5% | $7.50@+$500/15tr | 2 |
| Backtests (actual) | **$50 flat** | none | none | none | none | **∞** |
| Live engine (actual) | $25 | $15@2% | $35@+$100&DD<1% | 4.5% | **none** | 2 |
| Dry-run manager (actual) | **$25 flat** | none | none | **none** | none | **3** |

- **Milestone lock (§2.1): does not exist.** No trigger, no throttle, no test. The question "does it freeze trading entirely" is moot — there is nothing to freeze.
- **CRITICAL BUG — DD measured from initial balance, not peak** (`forex_engine.py:1051-1052`, mirrored in `get_current_risk_budget`): `drawdown_usd = max(0, initial_balance − equity)`. Once equity exceeds $5,000, **no subsequent giveback ever registers as drawdown**. Example: equity $5,000→$5,600→$5,300 (true peak-to-trough DD 5.4%, past the hard freeze) reports DD **0.0%**; DD-defense never arms; house-money stays on; hard freeze never fires. **The entire risk governor is defeated in exactly the state (profitable-then-reversing) it exists to catch.** Must be `peak − equity` with a tracked running peak.
- **No recovery hysteresis anywhere** (defense arms/disarms on the same threshold — risk flickers bar-to-bar at the boundary). Add ±0.3pp hysteresis + minimum 24-bar regime persistence.
- Backtest/live sizing mismatch is 2× ($50 vs $25) *before* concurrency differences — backtest PnL must be at least halved for any live comparison, and much more after fill-rate vetoes.

---

## 5. Directive 4 — Production Readiness & MT5 Compatibility

### 5.1 What is genuinely production-minded (credit where due)
Rollover lockout (21:55–22:15 UTC) + ratchet suppression; Friday entry cutoff (18:00) + Friday closeout liquidation (20:30); 30s broker reconciliation heartbeat (fail-safe on `None`); spread/ATR quarantine with hysteresis + exotic session filter (07–17 UTC); leverage/notional caps per asset class (10:1 majors, 5:1 minors/indices, 3:1 exotics); broker `trade_stops_level` guard on SL modifies; volume-step floor rounding that never exceeds risk budget (live manager); atomic parquet sync; idempotent warm-start dropping the forming bar.

### 5.2 Parity failures (live ≠ backtest, each verified)
1. **Setup definition differs 3 ways:** labeler/backtest effective = KZ + sweep + FVG + 4H trend + prob≥0.55; dry-run main loop = KZ + FVG + trend + prob≥0.54 (**no sweep**); `infer_next_bar` = `check_setup_criteria` (**with sweep**). Live trades a different (wider) setup distribution than the model was trained/validated on.
2. **ORB trend filter differs:** backtest uses 15m EMA200 *level*; live uses 4H EMA200 *slope* (+ Judas override). Different trades.
3. **TP differs:** backtest fixed 2.5R (FVG) / 2.5R (ORB); live TP is **structural** via `calculate_adaptive_sl_tp` (R_eff 1.2–3.5, else 2.5R). Live exits differ from validated exits.
4. **Holding differs:** backtest FVG holds to 96 bars MTM; ORB backtest expires at session+24 bars (time-decay branch is **dead code**: `k−entry ≥ 24` unreachable since `trade_end−trade_start = 24`); live holds to 96 with Friday 20:30 liquidation — **backtests hold through weekends; live doesn't** (and ORB clamps losses at −1.15R, hiding gap-through-stop tails on GAS/NICKEL/indices).
5. **Spread quarantine is live-only** — backtests take trades the live engine would veto.
6. **Dry-run does not paper-trade**: `place_market_order` is gated by `if not is_dry_run`, so `open_trades` stays empty, ratchets/decay never simulate, PnL never accrues. It is a signal monitor, not a harness — it cannot validate backtest math. (Related: live `modify_sl`'s dry-run branch is unreachable for mock tickets — broker lookup fails first.)
7. **Duplicate implementations drift:** 2× `MT5Connection`, 2× `OrderManager`, 2× `StatefulInferenceEngine`, 2× `pre_flight_data_sync`, 2× `robust_parquet_replace`, 2× quarantine constants — the live copies already disagree on max slots (3 vs 2) and risk governance (none vs 3-tier).

### 5.3 Live-crash bug (high severity)
`ParallelForexStrategy.generate_signal` conflict branch references `sig1.side` / `sig2.side` (`base_strategy.py`) — **`StrategySignal` has no `.side` attribute** (verified against the dataclass). Any bar where both sleeves fire opposite directions raises `AttributeError` inside the telemetry loop, which has no handler there → **telemetry crash, position management (`manage_open_trades`) stops with it**. Trigger condition is rare but precisely the high-volatility moment you most need the loop alive. One-line fix (`sig.signal`), plus wrap the per-asset evaluation in try/except.

### 5.4 Platform & operability notes
- `forex_engine.py` imports `MetaTrader5` at module top → **backtests cannot run on Linux/headless CI at all** (verified: ImportError; my reproductions bypassed it via the strategy modules). Lazy-import MT5.
- `verify_all_components` advertises "Base Risk: $50.00" while the governor enforces $25 — cosmetic but symptomatic of spec drift.
- GER30 **and** GER40 parquets both exist and both appear in dynamic pools — duplicate DAX exposure; canonicalize to one.
- GAUCNH history starts 2025-01-23 (W1–W11 run on 17 assets); XAUCNH from 2023-01-20. "18-asset" coverage is period-dependent — disclose per-window universes.

---

## 6. Remediation Backlog (ordered, file-level)

**P0 — safety & validity (gating):**
1. `forex_engine.py:1051` + `get_current_risk_budget` — peak-to-trough DD with running peak; add hysteresis; regression-test the profitable-then-reversing path.
2. `base_strategy.py` — fix `sig.side` → `sig.signal`; wrap telemetry per-asset evaluation in try/except; add conflict-path unit test.
3. `strategy_kernel.py` — FVG entry at `opens[i+1]` + half-spread cost from filed spread column; add −0.08R friction to FVG labels (parity with ORB); SL-first ordering already OK, keep.
4. Walk-forward discipline — per-window model training with 24–96h purge (extend `run_forex_20_oos_benchmark.py` to use real `r_realized`, production 13-feature XGBoost, true criteria); retire in-sample `xgboost_forex.json` from all OOS reporting; wire `get_causal_train_test_split` in or delete it.
5. Build the missing system **or** retract the claim: either implement the interleaved portfolio backtest (2 slots, 1/asset, 1/cluster, governed risk, MTM DD, Friday closeout, spread veto) or remove §1/§2 interleaving + milestone-lock claims from all specs. No middle ground — current numbers estimate nothing deployable.
6. `forex_engine.py` — SL-first ordering in `run_standard_backtest`; lazy-import MT5.

**P1 — parity (pre-pilot):** unify setup definition (sweep in/out — pick one, retrain, relabel); unify ORB trend filter; unify TP rule; unify risk tiers + slot count across backtest/engine/dry-run (single `RiskConfig`); make dry-run actually paper-trade (remove `if not is_dry_run` gate, fix mock-ticket SL modify); reconcile GER30/GER40; per-window universe disclosure; ORB warmup prepend; unclamp or gap-model ORB tails (−1.15R clamp → explicit gap distribution).
**P2 — hardening:** dedupe MT5Connection/OrderManager/InferenceEngine into single imports; hysteresis on all regime switches; kill-zone boundary audit (hour ≤10/≤15 vs nominal); `Engine/tests/test_prelaunch.py` extension to cover P0 regressions; Linux CI job running the ORB+FVG 20-window reproduction in this report as a gate.

---

## 7. Scores & Sign-off

| Dimension | Score | Rationale |
|---|---|---|
| Architecture | **5/10** | Clean kernel/registry separation and genuinely good live-safeguard breadth — undermined by duplicated managers, dead-code protocols, and spec/code drift (fictional module paths, fictional risk tiers) |
| Causal Soundness | **4/10** | Feature/4H/D1 causality is careful and correct; ORB fills are causal — but FVG close-fill, in-sample production model in OOS tests, dead purge helper, and TP-first ordering in the standard backtest are material leaks |
| Microstructure Realism | **3/10** | Live tick-level ratchets, spread quarantine, leverage caps are real — but backtests ignore spread/concurrency/clusters/Friday/margin, use closed-trade-only DD, clamp gap tails, and run 2× live size |
| Production Readiness | **3/10** | Real MT5 plumbing (reconcile, rollover, Friday defense) — but the DD governor is defeated by construction (initial-balance DD), a crash bug sits in the conflict path, dry-run doesn't trade, and no filed backtest represents live behavior |

**Verdict: REVISE.** The claimed 20/20 certification is not supported by the repository — reproduction shows ORB failing 18/20 on drawdown and FVG failing 5/20 even in-sample. Fix P0, re-run the 20-window reproduction protocol in this report from a tagged commit, and file the resulting (honest) scorecard; I will re-audit against that. The kernel core is worth the investment — the system is one disciplined remediation cycle from a credible pilot, but it is not one today.
