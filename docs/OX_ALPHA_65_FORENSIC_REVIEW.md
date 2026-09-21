# OX-ALPHA-65 — Institutional Forensic Review: Funding-Arbitrage Daemon & Directional Suite

**Reviewer:** Arena.ai agent (session `arena/01a0bf23-trading`) · **Date:** 2026-09-21
**Pinned commit audited:** `a33a5c8` (+ `8ea3bc0` directive doc) · **Method:** static audit of all 7 pinned
files + independent empirical measurement on the repo's own tracked data. No code was modified for this review
(research/read-only except this report).

## 0. VERDICT (read first)

**The Delta-Neutral Arbitrage Daemon is NOT APPROVED for live funded execution on Binance.**

| Dimension (1–10) | Score | One-line justification |
|---|---|---|
| Architecture Quality | **3** | Tidy scanner/dashboard; but "dual-mode live" is a label — no order path exists |
| Causal & Mathematical Soundness | **4** | 1×/1× neutrality math correct in principle; sizing uses wrong-leg price; economics math absent |
| Microstructure Realism & Friction Handling | **1** | Zero fees/spread/margin/lot-size; full-book rotation on 82%-churn sets |
| Production Readiness & Live Deployment Viability | **1** | Cannot execute anything; `--live` changes only a dashboard string |

The three load-bearing claims of the directive each fail against the pinned commit:
1. **"Live execution daemon"** — the module contains zero execution code (no signed requests, no orders,
   no API keys, no leverage/liquidation handling). `--live` flips `dry_run=False`, which alters nothing
   except the dashboard banner. The program is a paper-trading monitor, not a daemon capable of trading.
2. **"23/23 quarters, +227.46% net, 0.15% DD, 22,116 intervals"** — no backtest code, report, or runnable
   artifact for the delta-neutral strategy exists anywhere in the repo (only the live bot matches
   "delta-neutral" in code search). The cited `funding_basis_carry.py` is a *directional* contrarian
   strategy, not cash-and-carry. The interval count 22,116 is irreconcilable with the data
   (6,600 8h-intervals/asset; 72,600 panel total). The repo's own data implies ~10%/yr *gross* top-3
   harvest at the bot's 50% deployment vs the ~22%/yr *net* claimed — the magnitude fails even pre-cost.
3. **"5-sleeve live terminal incl. S4 footprint engine"** — the terminal implements 3 signal sleeves
   (S1/T1/S3); S2 and S4 compute indicators but emit no signals. The S4 module and the meta-labeling
   pipeline are not imported or called by the terminal. S4's backtest has a fatal next-bar-close
   entry lookahead (§5.2).

## 1. Premise verification (what was actually audited)

- `a33a5c8` ("live 24/7 delta-neutral funding arbitrage daemon & structural orderflow sweep engine")
  exists on both `main` and `arena/01a0bf23-trading`; all 7 pinned paths verified present via
  `git cat-file -e a33a5c8:<path>`. Local branch fast-forwarded `ef307bc → 8ea3bc0` (strict descendant,
  clean tree) to audit the pinned code.
- `binance_backtesting_data/*_15m_master_2020_2026.parquet` ARE git-tracked at `a33a5c8` and contain
  `funding_rate_pct` + `basis_index_bps` columns (100% populated, 2020-09-01 → 2026-09-09/10).
  Data for a funding backtest exists; the backtest does not.
- `Engine/oos_windows_20.json` contains **23** windows (2021-01-01 → 2026-09-19); "20" in the filename
  and several docstrings is stale. Window-count claims of 23 are consistent with the file.

## 2. Delta-neutral architecture audit (directive §3.1)

Target: `Engine/live/binance_funding_arbitrage_bot.py` (321 lines) + `funding_arbitrage_state.json`.

**What the code is.** A 15-second polling loop: fetch `premiumIndex` (public REST) → rank 11 symbols by
`lastFundingRate` → hold top-K (K=3) with `rate ≥ 0.002%` → simulate accrual when wall-clock passes each
position's `next_time_ms` → render Rich dashboard → persist JSON state. Genuine engineering exists in the
telemetry, the inversion veto at entry, and the park-to-USDT fallback when nothing is eligible.

**2.1 No execution path (certification-blocking).** Grep over the module for
`signed|hmac|api_key|secret|/fapi/v1/order|place_order|execute_trade|leverage|liquidation` returns
**zero hits**. There is no order placement, no position reconciliation, no margin accounting, no
lot-size/tick-size handling, and no liquidation-price monitor. `BINANCE_SPOT_BASE` (line 41) is defined
and never used: the spot leg price is never fetched — spot quantity is sized off the **perp mark price**
(`qty = spot_notional / mark_price`), so entry basis is ignored in both sizing and economics.
Docstring claims of "REST/WebSocket" (REST-only), "Dual-Mode … Live Execution", "simulated/live margin
accrual", and "atomic JSON state persistence" (plain `open/write`, no tmp+rename; a crash mid-write
corrupts state, and `history` grows unbounded) are all contradicted by the code.

**2.2 Inversion veto: correct at entry, unprotected in hold.** Eligibility gating (`rate_8h_pct ≥ 0.002`,
`rebalance_dry_run`) plus set-change-triggered rebuild means an inverted holding is exited — indirectly,
only when the eligible *set* changes, with no hysteresis band, no minimum hold, and no rotation-cost
hurdle. Critically, **any** set change liquidates and re-establishes the **entire** 3-pair book
(`rebalance_dry_run`, full `new_positions` rebuild), not just the rotated leg.

**2.3 The churn arithmetic (measured, §7).** On the repo's own funding panel, the top-3 set changes in
**82% of 8h periods** (~2.5 full-book rotations/day as coded). Per full rotation: 3 pairs × ~(2×15bps
taker + spread + 2×basis) on 1/6-equity notionals each ≈ **~21bps of equity per event**, i.e. ~50bps/day
(≈190%/yr) drag against a measured top-3-mean gross harvest of **~10.4%/yr** on equity. Costs exceed
gross by roughly **18×**. The strategy's core assumption (persistence, P(next>0|now>0)=88.7%) is real,
but the coded rebalance policy converts it into a guaranteed bleed. No…and no backtest demonstrates
otherwise…hysteresis, cooldown, or expected-accrual-vs-cost gate exists anywhere in the module.

**2.4 Resilience gaps.** Fetch failure → return `[]` → silent skip until next poll: no retry/backoff,
no staleness alarm, no circuit breaker on repeated failures, no settlement-miss catch-up beyond
one-step-per-poll accrual. No kill-switch, no alerting, no tests. Acceptable for a monitor; not for
"24/7 production."

**2.5 State-file forensics.** The committed `funding_arbitrage_state.json` is a genuine dry-run snapshot
(2026-09-21 11:12 UTC, BNB/XRP/LINK at plausible live rates, `next_time_ms` = 16:00 UTC settlement
boundary ✓). No settlements collected, no history — consistent with a freshly started paper session,
not a live track record.

## 3. Microstructure & execution realism (directive §3.2)

| Assumption required | Daemon status |
|---|---|
| Taker fees (Binance VIP0: 10bps spot / 5bps perp) | **Absent** — accrual is `notional × rate`, no fee deduction anywhere |
| Bid/ask spread on 4 legs per pair rotation | Absent (fills at mark exactly) |
| Entry/exit basis (measured median −4bps; p99 +17–25bps) | Displayed, never gated or costed |
| Settlement timing (00/08/16 UTC) | Correctly consumed via `nextFundingTime` ✓ |
| Margin/leverage/liquidation on perp short | Absent (1× implied by 50/50 split, unenforced, unmonitored) |
| Min notional / lot & tick rounding | Absent |
| Spot/perp execution asynchrony (leg-slippage) | Absent (atomic sim fills) |
| `lastFundingRate` as next-rate forecast | Used silently; persistence measured at 88.7% (supportive but unhedged — no cap on single-name concentration beyond 1/3, no rate-collapse exit except via rank change) |

The directive's "8 bps" fee figure matches neither Binance VIP0 schedule (10bps spot / 5bps perp taker)
nor the daemon (0bps). The yield math is therefore overstated three ways: no fees, no rotation costs,
mark-price fills.

## 4. Directional multi-sleeve terminal (directive §3.3, first half)

Target: `Engine/runners/run_live_terminal.py` (1018 lines) + `Engine/brokers/binance_broker.py` (live path).

**The terminal is the more production-serious of the two systems**: it has a real signed-REST broker
(`_request(signed=True)`, `execute_trade`/`close_position`/`modify_sltp`), a genuine risk governor
(base $36 / DD-defense / house-money / milestone-pass-lock / 4.85% circuit breaker / concurrency +
cluster caps), exchange reconciliation (`reconcile_with_exchange`), and a 3-stage ratchet with
exchange SL modification + local fallback. This is real live-trading plumbing, categorically ahead
of the arb bot's simulator.

**But its advertised edge is not what the code trades, and research↔live parity is broken:**

- **3 sleeves, not 5.** `scan_asset_signals` emits S1 (id 1), T1 (id 2), S3 (id 3) only. S2 inputs
  (`zbw`, `adx`) and S4/KRI input (`zkri`) are computed and displayed but have **no signal branch**.
- **S4 + meta-labeler orphaned.** Zero references to `s4_pivot`, `footprint`, or the calibrate pipeline
  in the terminal. The "structural orderflow sweep engine" of the commit message never reaches production.
- **R-geometry mismatch (the big one).** Research (`fast_numba_oos_engine`, `s4_*`) floors R at
  **1.2% of price** (`max(atr_14, close×0.012)`); the terminal uses **raw 15m ATR** (~0.1–0.2% for BTC).
  Backtest stops/targets/ratchets are ~6–10× wider than live ones, and research friction (0.18R on the
  inflated R ≈ 22bps) does not describe live costs either. OOS numbers generated under research geometry
  do not describe the terminal's behavior. Sleeve taxonomies also differ (research sleeve 3 = PDL sweeps;
  terminal sleeve 3 = ORB), as do horizons/targets (32/3.0/1.2 vs 24/2.2–2.5/1.0–1.2) and several governor
  constants across the three portfolio sims (36/14/48/10 vs 38/16/48–52/12).
- **Stale-signal churn loop.** Signals are computed from parquet bars (preflight tolerates 24h staleness)
  while fills/marks use live prices: `entry_price` recorded in the tracker is a stale bar close, so live
  R accounting is wrong whenever the market moved since the last sync — and after any close, the *same*
  stale signal re-fires on the next 15s poll (no signal ID, no traded-bar memory, no cooldown), allowing
  immediate re-entry loops. There is also no entry/exit slippage model in the tracker (`realized_pnl`
  from sampled-tick marks).
- **Research-side caveats (for the OOS claims behind the terminal):** fixed Optuna-baked hyperparameters
  ("Trial #24641 Champion" — massive selection), trade-close-based DD (intraday equity unseen),
  entry-at-signal-close fills (optimistic,291), `tide_align` side-encoding in meta features, and
  `roc_auc`/`brier` imported-but-unused ("calibration" unmeasured). The walkforward skeleton itself
  (expanding train, 72h purge, per-window refit, train-only quantile thresholds) is correctly causal —
  the rot is in geometry parity and selection, not in the CV plumbing.

## 5. Pinned supporting modules (directive items 4–7)

- **S4 pivot/footprint engine (510 lines): fatal lookahead.** `label_exhaustion_trades_numba` receives
  closes and sets `entry_p = c[i+1]` — the **next bar's close** — while the docstring claims
  "Entry strictly at next-bar open" and the frame annotates `"open_time_ms": t[+1]  # Next-bar open
  execution!"`. Timestamp says next-open; price is next-close. All S4 backtest figures are invalid.
  Secondary: `ARTIFACT_DIR` hardcodes a Windows path (`C:\Users\SIGMA\…`) → benchmark crashes on Linux;
  ATR floor repeats the 1.2% anomaly; pass gates (ROI≥10/DD≤5/WR≥40/n≥15) are fine but applied to
  close-based DD. (Fairness notes: `future_cvd_15m` = *futures-market* CVD, concurrent-bar — the name is
  alarming, the semantics are causal; session VAH/VAL is a genuinely causal developing profile; pivots are
  correctly previous-period anchored; stop-before-target same-bar resolution is the conservative choice.)
- **Canonical indicators (689 lines): sound.** Causal rolling/Wilder/EMA implementations, correct
  Monday-anchored weeks, prefix-invariant value area. The strongest file in the package; no findings
  beyond warmup seeding (negligible).
- **Fast Numba OOS engine (702 lines):** causal CV skeleton; entry-at-signal-close (optimistic, not
  lookahead);-invalidated as a *terminal* backtest by the geometry/taxonomy mismatches in §4.
- **Meta-labeling pipeline (369 lines):** legitimate per-window train/purge/gate discipline; tau from
  train-only quantiles ✓; side/sleeve correctly excluded from features. Orphaned (nothing consumes it),
  small-sample per-class fits, "calibration" unmeasured, simulator risk-tiers match the terminal but
  inherit the geometry break.

## 6. Allocation recommendation (directive §3.3, second half)

**Neither 100% delta-neutral nor an 80/20 hybrid is recommendable.** That framing presumes two validated
legs; there are zero: the arbitrage leg has no backtest and cannot execute, and the directional leg's
live behavior is undescribed by its research. Allocating between an unproven simulator and a
parity-broken live system is not diversification — it is two independent unquantified risks.

- *If forced to sequence development capital:* the funding-arbitrage **thesis** (persistent retail
  funding premium + measured 88.7% sign persistence) is the more structurally grounded edge, but it is
  currently the *least* built (no execution, no cost model). The terminal is the closest to production
  plumbing but its edge must be re-proven under live geometry.
- *Funded-capital recommendation:* **0% to both** until the gates in §8 pass. The honest next dollar goes
  to (a) a cost-aware, hysteresis-gated funding backtest reproduced from the tracked parquets, and
  (b) a parity repair + paper track record for the terminal.

## 7. Empirical annex (independent measurements, repo data @ a33a5c8)

Funding panel: 11 assets × ~6,600 8h-sampled intervals (2020-09-01 → 2026-09-09).

| Check | Result |
|---|---|
| Positive-rate share (directive: ">86%") | **BTC 86.0%, ETH 84.9%** ✓ (pooled 72.2%; TRX 61.4% — the inversion anecdote is real) |
| Sign persistence P(next>0 \| now>0) | **88.7%** ✓ (thesis mechanism supported) |
| Top-3 set stability across 8h steps | Overlap 57%; **full-book rotation event 82%** (bot rebuilds all 3 pairs each time) |
| Top-3 mean rate vs all-asset mean | 0.0190% vs 0.0082% (2.31×) → **~10.4%/yr gross on equity** at bot's 50% deployment |
| Claimed 22,116 intervals | Matches nothing (6,600/asset; 72,600 panel; 19,800 naive top-3 slots) ✗ |
| Claimed +227.46% (~21.9%/yr net) | Exceeds measured **gross** harvest by ~2×, pre-cost ✗ |
| Basis (entry/exit friction) | Median −3.6…−5.1bps (adverse at typical entry); p99 +17…+25bps |
| Rotation cost vs harvest (as coded) | ~190%/yr drag vs ~10%/yr gross — costs ≈ **18×** gross |

## 8. Conditional path to approval (all gates required, in order)

**Arbitrage daemon:**
1. Publish the cost-aware delta-neutral backtest (tracked code + config + seed): top-K + inversion veto +
   hysteresis/min-hold + rotation hurdle (expected accrual > k× rotation cost), VIP0 fees (10/5bps),
   spread, measured basis, margin/leverage accounting — reproduced from the tracked parquets with
   interval counts that reconcile (6,600/asset).
2. Rebuild the live loop around the *backtested* policy (no full-book rebuilds; delta-rebalance only;
   spot-price fetching; lot/tick rounding; min-notional; leg-failure rollback).
3. Add liquidation monitor, settlement watchdog, staleness circuit breaker, kill-switch + alerting,
   atomic state writes, and a test suite (incl. fee/parity tests vs the backtest).
4. 90-day paper parity record (daemon paper PnL vs backtest-implied, tracking error bounded), then
   capped-capital live pilot with independent reconciliation.
5. Reconcile or retract the +227.46%/23-23/0.15% figures; disclose leverage/deployment assumptions.

**Directional terminal (before any allocation):** unify R geometry research↔live (one ATR definition,
one floor policy); reconcile sleeve taxonomy; wire or remove S2/S4/meta claims; add live-bar signal
evaluation (or bound staleness) + signal deduplication/cooldown + slippage accounting; re-run OOS under
live geometry with tuned-hyperparameter quarantine; paper record.

## 9. Reproducibility of this review

All pinned files read in full at `a33a5c8` (bot 321, terminal 1018, S4 510, indicators 689 incl.
value-area/pivots, numba engine key sections, meta pipeline 369, carry engine 431, broker live-path
spot-check). Code-search claims via `grep` (execution tokens, delta-neutral references, terminal
imports). Numbers in §7 from direct parquet measurement (`[::32]` 8h sampling; churn/overlap/persistence
stats). No engine or strategy file was modified; this report is the only new artifact.
