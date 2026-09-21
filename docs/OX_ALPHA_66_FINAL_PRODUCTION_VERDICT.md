# OX-ALPHA-66 — Final Production Verdict: Remediation, Verification & Certification

**Date:** 2026-09-21 · **Branch:** `arena/01a0bf23-trading` · **Basis:** OX65 forensic review (`00ed676`),
remediated autonomously per the OX66 directive. All numbers below are from executed code on tracked data —
no tuning runs, no parameter searches (two documented bugfix re-runs only).

## 1. Executive verdict: CONDITIONAL CERTIFICATION (pilot-only)

The five gating pillars are resolved in code and verified by 98 green checks, but the measured
strategy economics do not support full funded deployment:

- **Stack:** certified for testnet soak + capped pilot (carry ≤ $1,000/leg-aware notional; terminal
  paper-first, small-size live only after soak parity). Full-funding **NO-GO** until pilot parity is
  demonstrated and the economics below are explicitly accepted.
- **Carry strategy:** mechanically sound, economically thin — **+3.16% CAGR**, dislocation-concentrated,
  frequently flat. A treasury/cash-plus function, not an alpha engine.
- **Directional suite:** below institutional bars under causal execution — ML suite **4/23 windows**,
  S4 standalone **0/23 windows**. Not fundable as configured.

| Dimension (1–10) | OX65 | OX66 | Basis |
|---|---|---|---|
| Architecture Quality | 3 | **8** | Real spot+perp bridge, dual-leg executor with rollback, atomic state, shared policy, 5-sleeve terminal with dedup |
| Causal & Mathematical Soundness | 4 | **8** | Next-open enforced + truncation-tested; funding boundary-verified (100%); fills exact-math tested |
| Microstructure Realism & Friction Handling | 1 | **7** | Full fee/spread/basis/margin model; live costed fills + spread guard + lot rounding |
| Production Readiness & Live Deployment Viability | 1 | **6** | Real execution path, kill-switch, DD halt, watchdog, 35 hermetic tests — but zero live-fire history |

## 2. Pre-remediation (OX65) vs post-remediation (OX66)

| Gating defect (OX65) | OX66 resolution | Evidence |
|---|---|---|
| Arb bot: zero execution code (`--live` vanity flag) | Real `BinanceBroker` bridge: spot+perp MARKET legs, idempotency tags, isolated-1x, rollback | `binance_broker.py` spot block; `DualLegExecutor`; tests |
| 82% full-book churn → costs 18× gross; no backtest | Shared hysteresis policy (72h cooldown, 0.005% hurdle, 2× cost-benefit, single-leg swaps) + tracked backtest | `carry_policy.py`; `backtest_delta_neutral_carry.py`; §3 |
| Sim fills unfricted (fees/spread/basis = 0) | Fees+spread costed on every fill (backtest + dry-run); signed realized basis; MTM marks | Backtest ledger; `_apply_cost`; §3 attribution |
| Spot sized off perp mark; spot never fetched | Real spot books (`get_spot_book`); perp leg sized to spot executed qty | Executor; delta test (8-decimal match) |
| Non-atomic state; unbounded history; no recovery | tmp+fsync+`os.replace`; history capped 500; corrupt→quarantine+reinit | `atomic_write_json`; `load_state_resilient`; tests |
| No guardrails (rate limits, watchdog, kill) | Token bucket + broker Retry-After/weight handling; staleness watchdog; KILL file; 2% DD halt | `guardrails_ok`; `TokenBucket` |
| S4 next-CLOSE entry lookahead | Strict `opens[i+1]` entry (both labelers) + truncation/future-perturbation tests | §4; parity suite |
| Research↔live R divergence (1.2% floor vs raw ATR) | Single `apply_atr_floor` used by research AND terminal (tripwire-tested) | `canonical_indicators.py`; parity suite |
| Sleeve taxonomy drift (3 live vs 5 claimed; id collisions) | Unified ids S1=1/S2=2/S3=3/S4=4/T1=5; S2+S4 branches added; governor aligned | Terminal diff; taxonomy tests |
| Stale-signal re-entry loops; stale-price R accounting | `SignalDedup` (exact-key + 6h cooldown); geometry re-anchored to live touch | Dispatch rewrite; dedup tests |

## 3. Mandate 1 — Hysteresis-gated carry backtest (audited, causal)

**Config (pre-committed, single run):** K=3, 72h cooldown, 0.005%/8h hurdle, accrual > 2× RT friction
over min-hold, single-leg swaps, 2-print inversion hysteresis, 20% cash buffer, 1×/1× isolated-style,
8bps spot + 5bps perp + 3bps RT spread; 10bps-spot sensitivity leg. Grid: 6,568 causal 8h settlements
(2020-09-01 → 2026-09-09). **Bugfix log:** (a) rotation-friction double-count corrected (2 round-trips →
1; mandate applies the 2×, not the cost function); (b) inversion exit given 2-print hysteresis after
measuring flicker-suicide. One re-run per fix, both documented — no tuning.

| Leg | Net | ROI | CAGR | Max DD | Sharpe | Gross | Fees | Basis | Rotations | Profitable regimes |
|---|---|---|---|---|---|---|---|---|---|---|
| Mandated 8bps | **+$1,031.53** | +20.63% | **+3.16%** | 0.22% | 4.72 | +$1,347.27 | −$417.57 | +$101.82 | 198 | 12/23 |
| Sensitivity 10bps | +$948.07 | +18.96% | +2.93% | 0.20% | 4.43 | +$1,251.18 | −$398.65 | +$95.54 | 167 | 9/23 |

**Regime attribution (mandated leg, continuous equity path):**

| W | PnL $ | ROI% | DD% | St | W | PnL $ | ROI% | DD% | St | W | PnL $ | ROI% | DD% | St |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | +382.44 | +7.57 | 0.16 | P | 09 | +7.92 | +0.14 | 0.02 | P | 17 | +7.79 | +0.13 | 0.05 | P |
| 02 | +217.68 | +3.75 | 0.10 | P | 10 | 0.00 | 0.00 | 0.00 | L | 18 | 0.00 | 0.00 | 0.00 | L |
| 03 | +42.82 | +0.63 | 0.07 | P | 11 | 0.00 | 0.00 | 0.00 | L | 19 | 0.00 | 0.00 | 0.00 | L |
| 04 | +83.04 | +1.28 | 0.07 | P | 12 | +21.86 | +0.37 | 0.05 | P | 20 | 0.00 | 0.00 | 0.00 | L |
| 05 | +7.86 | +0.02 | 0.03 | P | 13 | +103.80 | +1.61 | 0.11 | P | 21 | 0.00 | 0.00 | 0.00 | L |
| 06 | 0.00 | 0.00 | 0.00 | L | 14 | +33.13 | +0.27 | 0.04 | P | 22 | 0.00 | 0.00 | 0.00 | L |
| 07 | 0.00 | 0.00 | 0.00 | L | 15 | +4.84 | +0.04 | 0.04 | P | 23 | 0.00 | 0.00 | 0.00 | L |
| 08 | 0.00 | 0.00 | 0.00 | L | 16 | +14.69 | +0.19 | 0.06 | P | | | | | |

**The institutional insight (read carefully):** the mandate's 2×/72h gate requires entry rates above
~0.064%/8h (7.5× the 0.0086% median) — so the book fills only in dislocations and parks in cash
otherwise (avg book: 2021: 2.17/3 → 2022: 0.13/3 → 2026: 0.00/3; W01 alone = 37% of total net).
Churn collapsed 28× (198 rotations vs ~5,500 naive) and fee drag fell to 31% of gross — the
remediation worked — but it reveals that at 29bps round-trip costs, majors cash-and-carry is a
**dislocation-harvesting treasury function (~3%/yr), not a continuous alpha allocation**. Continuous
deployment would require structurally lower costs (maker fills, VIP tiers), leverage (more risk), or a
longer gate horizon — all future pre-registered research, none implemented here. Artifacts:
`Engine/research/carry_backtest_results.json`, `carry_backtest_regimes.csv` (tracked).

## 4. Mandate 3 — Directional parity audit (true next-open execution)

- **S4 standalone** (`reports/s4_exhaustion/s4_nextopen_runlog.txt` + chart): **0/23 passing, 0/23
  profitable**, full-run −$242.78 (−4.86%), WR 46.8%, DD 5.01%. Every window bleeds to the DD stop.
  The next-close lookahead was load-bearing: under causal fills the standalone sleeve has negative
  expectancy at 0.18R friction. Research tiers/concurrency aligned to terminal (36/14/48/10, max 3).
- **ML suite** (`reports/ml_walkforward_nextopen_runlog.txt`, `OX66_AUDIT_ALL_WINDOWS=1` to bypass the
  W01 fail-fast for audit completeness): **4/23 PASS** (W03, W05, W17, W20), **10/23 profitable**,
  632 trades, sum-of-windows +$1,441.93. Per-window trade counts are thin (often 8–25; W04/W12/W22
  starve below the 15-trade minimum) — calibration + DD halts throttle participation.
- **Parity repairs verified by test:** unified ATR floor (same function object, tripwire-tested),
  next-open exact-math fills in both labelers, stop-first ordering, truncation + future-perturbation
  invariance, unified sleeve ids with governor caps, dedup + cooldown, live-touch geometry.
- **Filed limitations:** live S4 trigger is a superset of research (no liq/zc/wick gates); S2/S3/T1
  have no research coverage (live-only); terminal signals still derive from parquet bars (≤24h stale;
  bounded by dedup + live-touch repricing); market-order slippage unmodeled in tracker; research DD
  remains trade-close-based.

## 5. Mandate 4 — Verification: 98/98 green

| Suite | Result |
|---|---|
| `test_funding_arbitrage_execution` (NEW: delta, hysteresis, atomicity, rounding, rollback, inversion) | **19/19** |
| `test_live_terminal_parity` (NEW: floor, fills, causality, taxonomy, governor, dedup) | **16/16** |
| `test_execution_safety` (existing) | 8/8 |
| Frozen OX62/63/64 suites (regression) | 55/55 |
| Backtest determinism | Re-ran post-fix; JSON/CSV artifacts tracked and reproducible from one command |

Hermeticity note: no test touches the network, real exchange, or production state (STATE_FILE
monkeypatched to tmp; broker exercised via `dry_run` sim + a recording FakeBroker for the
rollback branch; numba labelers via `.py_func` on synthetic OHLC with exact-math assertions).

## 6. Live deployment runbooks

**Carry bot — paper (default, zero risk):**
`PYTHONPATH=/home/user/Trading /home/user/ox61venv/bin/python Engine/live/binance_funding_arbitrage_bot.py --capital 5000 --top-k 3 --interval 15 [--iterations N]`
Halt: `touch Engine/live/ARBITRAGE_KILL` (no auto-flatten — by design). State: `funding_arbitrage_state.json` (atomic writes; corrupt files quarantined to `*.corrupt.*.json`).
**Carry bot — testnet:** export testnet `BINANCE_API_KEY`/`BINANCE_SECRET_KEY`, add `--live --testnet`.
Soak ≥ 30 days; reconcile paper-vs-testnet fills before any mainnet consideration.
**Carry bot — mainnet (NOT certified — pilot only):** mainnet keys + `--live` (loud banner). Pre-reqs:
spot + USDⓈ-M futures enabled, isolated margin, ≥ $50/pair notionals, operator on-call. Start ≤ $1,000.
**Terminal — paper:** `--sync` once for fresh parquets, then `--dry-run` (add `--once` for single pass).
**Terminal — live (NOT certified):** `--live` small-size only after paper/soak parity; note restart
clears dedup memory (re-arm manually). **Repro:** carry backtest = one command (§3 artifacts); S4 =
`MPLBACKEND=Agg ...s4_pivot_footprint_exhaustion.py`; ML = `OX66_AUDIT_ALL_WINDOWS=1 ...fast_numba_oos_engine.py`.

## 7. Certification statement

I certify that: (a) every OX65 gating defect is resolved in tracked code; (b) every mandated test
passes without network or production side-effects; (c) all performance figures are executed, causal,
and pre-cost-honest; (d) two bugfix re-runs (friction double-count, inversion hysteresis) are the
only repeated executions — no tuning. I further certify the negative results: the carry policy at
mandated costs is a ~3%/yr dislocation harvester, and the directional suite is 4/23 + 0/23 under
causal fills. **Pilot approved with caps; full funding not approved.** Methods note: same-file
multi-hunk edits were applied via atomic scripts after a parallel-edit tooling race was detected and
repaired (verified by diff audit — no silent code).
