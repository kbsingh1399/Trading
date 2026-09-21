# OX ALPHA 55 — FORENSIC VERIFICATION OF FOREX ENGINE P0 REMEDIATION

**Auditor:** Ox Alpha (Principal Quantitative Architect) · **Date:** 2026-09-20
**Directive:** `docs/prompts/Ox_Alpha_55_Forex_Engine_Remediation_Audit.txt` (commit `5d67a81`)
**Remediation commit:** `5d67a81` *"fix(forex): remediate P0 defects from Ox Alpha 54 audit"*
**Verification target:** `origin/main @ d99bb26` (HEAD; `d99bb26` is docs-only over `5d67a81`)
**Pre-remediation baseline:** `01c226a` (parent of `5d67a81`; backtest math ≡ `6be8343` — proven §6)
**Method:** sparse checkout of `origin/main` + pre-remediation file overlay; static inspection,
24 functional checks (all executed), and 7 full 20-window empirical sweeps (140 window-runs).
Artifacts + rerunnable scripts: `docs/ox55_verification/`.

> **Branch note.** The session branch `arena/01a0bf23-trading` is a stale snapshot (`44c3bef`)
> with history unrelated to `origin/main`, so it cannot be merged or fast-forwarded
> (`git merge` refuses: unrelated histories). All verification was executed against
> `origin/main @ d99bb26`, exactly as the directive permits ("branch … or `main`").
> The local snapshot additionally predates the `6be8343` engine reorganization, which
> materially affects §2 below. This report is filed on the session branch for the record.

---

## 1. VERDICT — CONDITIONAL CERTIFICATION

| Item | Verdict |
|---|---|
| The 6 claimed P0 fixes — present on main? | **YES, all 6 — functionally verified (24/24 checks pass)** |
| Headline "perfect 20/20" (`perfect_20_oos_dual_sleeve_results.csv`) — reproduced? | **NO. Best reproduction from committed code: 19/20. Canonical path post-remediation: 16/20** |
| Remediation effect (isolated, same-path pre→post) | Small and honest: **−$90 to −$153** (−0.6% to −1.1%), 0–1 windows |
| Certification | **CONDITIONAL — certified for paper / dry-run forward validation. Funded-live deployment remains blocked on the P1 backlog (§7), and the 20/20 claim is WITHDRAWN pending CSV regeneration from pinned code** |

**Updated scorecard (system on `main @ d99bb26`, post-remediation):**

| Axis | OX54 (snapshot `44c3bef`) | OX55 (main `d99bb26`) | Δ rationale |
|---|---|---|---|
| Architecture | 5 | **7** | Interleaved dual-sleeve engine + 5-regime governor exist and function (stale "missing" calls retracted, §2); −2 for backtest/live governor parity gaps + orphan CSV + span-sensitivity |
| Causal Soundness | 4 | **7** | Causal next-open fills, −0.08R friction, SL-first, peak-DD governor all verified live in code; −3 for the still-in-sample production model + threshold-boundary batch sensitivity |
| Microstructure Realism | 3 | **5** | SL-first both engines, ratchet exits, friction parity; − for synthetic dry-run pricing, 0.01-lot fallback, no spread/slippage model |
| Production Readiness | 3 | **5** | Headless research engine, working dry-run paper trading; − for unguarded live MT5 imports, `connect()` crash on `mt5=None`, unpersisted defense flag |
| **Verdict** | **REVISE — NOT CERTIFIED** | **CONDITIONAL CERTIFICATION** | P0s closed; P1 backlog + 20/20 withdrawal gate funded-live |

---

## 2. BASELINE CORRECTION — OX54 FINDINGS RETRACTED OR RESTATED

The OX54 audit ran against snapshot `44c3bef`, which predates main-line commits `6be8343`
(dual-sleeve interleave) and `d9cf116`/`9e16d53` (reorganization). The following OX54
findings were **snapshot artifacts** and are hereby retracted as stated against current main:

1. **"Claimed interleaving code does not exist" — RETRACTED.** `ParallelForexStrategy`
   with `FOREX_CLUSTER_MAP`, `precompute_candidates()`, and a full interleaved
   `run_backtest()` (max-2 concurrency, 1-per-cluster, 1-per-asset, dynamic-risk state
   machine) exists at `Engine/core/base_strategy.py` L370–L759 and **executes**
   (140 window-runs this session).
2. **"Directive §4 paths invalid / files absent" — RETRACTED.** The packaged sleeves
   `Engine/strategy/s4_fvg_ml/s4_fvg_ml_forex_engine.py` and
   `Engine/strategy/orb_crt_forex_engine.py` exist on main (the flat files only ever
   existed in the snapshot era).
3. **"50/65/27.5/16.5/7.5 + milestone lock exists nowhere" — RETRACTED.**
   The 5-regime machine + pass-lock predates the remediation on main
   (`get_current_risk_budget`, `Engine/forex_engine.py` L533+); the snapshot's 3-tier
   governor was the stale copy.
4. **`perfect_20_oos_dual_sleeve_results.csv` "absent" — RETRACTED as absent.**
   It exists on main (committed by `6be8343`). It is, however, **irreproducible**
   from committed code (§6) — the substance of the concern stands in stronger form.
5. **"THREE risk regimes + directive fiction" — RESTATED.** Current main has TWO
   governed paths (live/engine `OrderManager` with freeze + hysteresis; backtest
   interleave with 1.8%/3.0% scaling but **no 4.5% freeze and no hysteresis**) plus
   ungoverned sleeve-level runs. The parity gap between backtest and live governors
   is real and filed as P1-R1.

OX54 findings that **replicate on main** and stand: in-sample production model
(`train_production_model.py`, 108 lines, zero split/purge — confirmed unchanged),
"8 bps" unit mislabel (still at `base_strategy.py` L622), `s4` docstring/target
inconsistencies (`target_r = 4.0` vs labeler `MIN_R_MULTIPLE = 2.5`), dual
`MT5Connection` classes.

---

## 3. CLAIM-BY-CLAIM VERIFICATION (all 6 CONFIRMED)

### Claim 1 — Peak-to-trough DD governor + hysteresis — ✅ CONFIRMED (functional)
- `OrderManager.__init__`: `self.peak_equity = 5000.0` (`forex_engine.py` L411);
  persisted/restored across restarts (L421/L440).
- `get_current_risk_budget()` (L533–L570): peak ratchet L547, peak-DD computation,
  HARD FREEZE at ≥4.5% (or $225), SEVERE ≥3.0% → $16.50, MILD ≥1.8% → $27.50 with
  hysteresis hold while `in_defense_mode and dd ≥ 1.50`, house-money $65, baseline $50,
  pass-lock $7.50. `get_account_metrics()` (L1041+) feeds live equity into the peak (L1073).
- **Functional B1–B8:** hard freeze fires at 5.36% peak-DD **while the account is +$300
  net** (the exact OX54 blind spot); hysteresis holds $27.50 at 1.79% and releases at
  1.25% with flag reset; peak never ratchets down; pass-lock returns $7.50 at +$500/15 trades.

### Claim 2 — `sig.side` → `sig.signal` conflict telemetry — ✅ CONFIRMED (functional)
- `base_strategy.py` L500–507: `s1_dir = "BUY" if sig1.signal > 0 else "SELL"` (same s2).
- **Functional C1–C3:** opposing stub sleeves return
  `CONFLICT VETO: fvg_ml(BUY) vs orb_crt(SELL)` with no exception; `StrategySignal`
  confirmed to expose no `.side` (fix premise valid). Residual: only the first two
  active signals are compared (P2-R7).

### Claim 3 — Causal FVG fills (`opens[i+1]`) + −0.08R friction — ✅ CONFIRMED (functional)
- `create_labels_ratchet()` (`strategy_kernel.py` L349–L490): `entry = opens[i+1]`
  both sides (L≈380/434), SL-before-TP intra-bar both sides, `r_real −= 0.08` both sides.
- **Functional D1–D3** (synthetic tape): gap-open entry proves next-open fill;
  TP path nets exactly 2.42; ambiguous SL+TP bar books −1.08 (SL-first).
- **Empirical:** FVG sleeve W01 post-remediation = 36 trades, +$834.20 — exactly **−$144.00
  (−0.08R × 36 × $50)** vs the pre-friction figure: friction accounting verified to the cent.
- Precision note: the intra-bar SL-first ordering in the *labeler* predates the fix
  (verified in `01c226a`); the genuine labeler changes are entry + friction.

### Claim 4 — SL-first in `run_standard_backtest` — ✅ CONFIRMED (functional)
- `forex_engine.py` L2120 (long: `low_c <= sl_price` break precedes TP) and L2134
  (short mirror), then `realized_r −= 0.08` friction (L2148).
- **Functional E1–E2:** a synthetic bar straddling both SL ($99) and TP ($102.50)
  books exactly −1.08R. This was a real ordering fix (TP-first pre-remediation).

### Claim 5 — MT5 lazy import (headless Linux/CI) — ✅ CONFIRMED **for the research engine only**
- `forex_engine.py` L40–45: `try: import MetaTrader5 … except (ImportError,
  ModuleNotFoundError): mt5 = None`. **Functional A1–A2:** headless import succeeds,
  `mt5 is None`, all 11 registry keys (incl. `fvg_ml`, `orb_crt`, `parallel`) auto-load.
- **Scope limitation (P1-R2):** the live stack still hard-requires MT5 —
  `live/order_manager.py`, `live/mt5_connection.py`, `live/run_forex_dry_run.py`,
  `live/append_latest_candles.py` all `import MetaTrader5` unguarded and **fail to
  import headless** (proven this session). Claim 5's "Linux/CI compatibility" does not
  extend to live code. Related P1-R3: `MT5Connection.connect()` (L230–231) calls
  `mt5.initialize()` unguarded → `AttributeError` (not clean `False`) when `mt5=None`.

### Claim 6 — Unified limits + dry-run paper trading — ✅ CONFIRMED (functional)
- `MAX_CONCURRENT_POSITIONS = 2` (`live/order_manager.py` L16); engine OM default
  `max_concurrent=2` (L404) — unified. `CORRELATION_CLUSTERS` **identical 4-bloc**
  (EUR/PACIFIC/COMMODITY/EQUITY) engine↔live (**F2**, dict-equality).
- `run_forex_dry_run.py`: `place_market_order(...)` now called unconditionally (L586),
  `manage_open_trades(...)` exercised per loop (L300/L621). `close_position` (L440) and
  `modify_sl` (L490) test `dry_run` **before** any broker lookup.
- **Functional F1–F5** (stubbed MT5, `conn=None`): dry-run opens a position with
  recorded risk/size/ratchet state, SL modify applies without broker, close releases
  the slot. Residuals: dry-run entry is synthetic (`sl + 0.0020`), lots fall back to
  0.01, dry-run close books **no PnL** (P2-R6); `can_open_trade` docstring still says
  "≤ 3" (stale comment, code is 2).

---

## 4. FUNCTIONAL SUITE RESULT — 24/24 PASS

`docs/ox55_verification/ox55_functional_tests.py` — A(headless+registry) 2 · B(governor)
8 · C(conflict) 3 · D(labeler) 3 · E(SL-first) 2 · F(live dry-run) 6. All assertions
execute real code paths (synthetic tapes, stub sleeves/MT5); no mocks of logic under test.

---

## 5. EMPIRICAL REPRODUCTION — THE 20/20 CLAIM DOES NOT REPRODUCE

Matrix (all runs: committed code + committed model blob `d5362fc…` + committed data):

| # | Code | Invocation path | Pass | Total PnL | maxDD |
|---|---|---|---|---|---|
| 0 | — (committed `perfect_20_oos_dual_sleeve_results.csv`) | unknown, no generator in repo | **20/20** | **+$15,448.20** | 4.96% |
| 1 | PRE (`01c226a` ≡ `6be8343` math) | per-window sleeve runs | 16/20 | +$13,891.78 | 6.36% |
| 2 | PRE | canonical walkforward, default span | 17/20 | +$15,095.28 | 5.44% |
| 3 | PRE | canonical walkforward, full-history span | 19/20 | +$14,930.58 | 4.75% |
| 4 | **POST (`d99bb26`)** | per-window sleeve runs | **16/20** | **+$13,739.04** | 6.36% |
| 5 | **POST** | **canonical walkforward, default span** | **16/20** | **+$15,005.21** | 5.46% |
| 6 | POST | canonical walkforward, full-history span | 19/20 | +$15,041.30 | 5.15% |

Post-remediation canonical failures (run 5): **W02** (ROI +3.52%, DD 5.46%),
**W13** (ROI +8.12%, DD 5.07%), **W15** (DD 5.30%), **W19** (DD 5.13%).

Isolated remediation effect (same path, PRE→POST): run 1→4 **−$152.74** (16→16);
run 2→5 **−$90.07** (17→16); run 3→6 **+$110.72** (19→19, non-monotonic — friction
perturbed interleave selection favorably). FVG sleeve level: 15/20 (OX54) → **12/20**
post, +$36.3k at flat $50/trade unbounded (sleeve accounting, not portfolio-governed).

**Reading:** the remediation is small, honest, and correctly signed at sleeve level.
But §6 shows the 20/20 was never reproducible from committed code — the shortfall is
not "caused" by the fix.

---

## 6. FORENSIC FINDINGS

**F-A. The perfect CSV is an orphan artifact with unrecoverable provenance (P1-R4).**
No committed code writes it (`git grep` hits: only memory/prompt docs). Model blob,
data blobs, kernel, sleeves, and interleave logic are all identical between `6be8343`
and the verified PRE overlay (only `multi_tf_data.py`, unused by this path, differs) —
yet three distinct invocation paths yield 16, 17, and 19/20, none matching the CSV's
per-window figures (e.g. CSV W02 ROI +13.68% vs best repro +10.69%). The CSV most
likely came from an uncommitted working tree. It is *near* the reproduction envelope,
not wildly fabricated — but as a certification artifact it is void. **Remedy:**
regenerate from a pinned commit + documented invocation and commit the generator.**

**F-B. Results are precompute-span-sensitive: 16→19/20 from a runtime parameter (P1-R5).**
Identical committed code over different precompute spans changes pass count by 3
windows and totals by ±$1.1k. Mechanism: span changes XGBoost predict batching
(probabilities near the 0.55 threshold flip on floating-point batching differences)
and indicator warmup; the path-dependent interleave then cascades single-trade flips
into different concurrency occupancy downstream. A 3-window swing from batching alone
means several PASS/FAIL calls sit on knife-edges (e.g. pre-run W13 fails by 0.01% ROI).
**Remedy:** deterministic fixed-batch inference, full-history warmup standard, and a
threshold-sensitivity band (±0.02) reported alongside every scorecard.**

**F-C. Pre-remediation code cannot run headless at all — the OX54 P0 in vivo.**
The PRE overlay fails at `import MetaTrader5` before any backtest line executes;
the PRE sweeps in §5 required a `sys.modules` MT5 stub. This independently confirms
both the original defect and the remediation's necessity.

---

## 7. RESIDUAL BACKLOG (funded-live gates starred ★)

**P1 (must-close before funded deployment):**
- **R1** ★ Backtest/live governor parity — the interleave (`base_strategy.py` L605–620)
  omits the 4.5% hard freeze and the 1.50% hysteresis release that live enforces;
  backtests are structurally more risk-tolerant than live will be.
- **R2** ★ Live-stack headless hardening — guard the 4 unguarded MT5 imports or
  document Windows-only live ops; CI cannot import the live path today.
- **R3** ★ `connect()` must return `False` (not raise `AttributeError`) when `mt5=None`.
- **R4** ★ Regenerate + pin the 20-window scorecard from committed code with a
  committed generator; withdraw 20/20 until then (best pinned result: 19/20).
- **R5** Deterministic inference + warmup standard; publish threshold-sensitivity bands.
- **R6** ★ Quarantine the in-sample production model: retrain per-window (walk-forward)
  or restrict the XGBoost filter to post-training windows; every FVG figure in §5 is
  partially in-sample (carried from OX54, unremediated by design scope).
- **R7** Persist `in_defense_mode` (or recompute hysteresis from timestamped DD) so
  restarts in the 1.50–1.80% band don't resume full size.

**P2 (correctness/hygiene):** dry-run close books no PnL + synthetic entry/lots (no
session-PnL validation possible); conflict path ignores 3rd+ sleeves; stale "≤ 3"
comment; `s4 target_r 4.0` vs labeler 2.5R vs docstring +4.0R; "8 bps on notional" is
8 bps of *risk*; pass-lock keys on realized (not total) PnL; ratchet-phase advance
without rollback on modify failure (carried from OX54).

---

## 8. CERTIFICATION CONDITIONS

1. The 6 P0 remediations are **accepted and closed** — each verified present on main
   and behaviorally correct under functional test.
2. The system is **certified for paper-trading / dry-run forward validation** with
   the live `OrderManager` governor (peak-DD + hysteresis + freeze) as the enforced
   capital-protection layer — itself verified in §3.1.
3. The **"perfect 20/20" claim is withdrawn**: pinned-code reproductions span 16–19/20
   (§5); the committed CSV is irreproducible (§6 F-A) and must be regenerated.
4. **Funded-live certification is withheld** pending P1-R1…R4, R6, R7.

*Ox Alpha, 2026-09-20 — verification-first: every number above was executed, not read.*
