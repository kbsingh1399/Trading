# OX ALPHA 58 — FORENSIC AUDIT: Altcoin Live Terminal Pipeline

**Audited tree:** `origin/main @ 15c5e21` (sandbox replica `/tmp/ox57_verify`; local checkout at `44c3bef` predates it)
**Data:** `binance_backtesting_data/` (18 masters, 3,475,005 bars) + `Forex_Backtesting_Data/` (symlinked into sandbox)
**Date:** 2026-09-20/21 · **Auditor:** Arena Agent Mode (OX58 track)
**Scope:** (1) broker/order-lifecycle · (2) research↔live parity · (3) risk budgeting · (4) scorecard + funded-deployment verdict
**Prior state:** OX57 certified a *different* (forex/paper) engine. OX58 is the first audit of the **23-OOS altcoin suite**
(`Engine/runners/run_23_oos_altcoin_suite.py`) and its **live terminal** (`Engine/runners/run_live_terminal.py`).

---

## VERDICT: ❌ NOT CERTIFIED for funded Binance Futures deployment

The claimed result — **23/23 quarters passed, +$23,872.73, 6,484 trades, DD 1.80–4.27%** — **reproduces bit-for-bit**
(independent rerun: 23/23, +$23,898.46, 6,484 trades; Δ+$25.73 = data refresh), **but is a proven artifact of a backtest
accounting bug.** With stops accounted honestly, the identical suite, identical signals, identical risk protocol scores
**0/23, −$4,895.53, 1,567 trades, win rates 7.7–38.7%**. Separately, the live terminal **never sends exits to the
exchange**, fires its 24-bar timeout after **~6 wall-clock minutes**, and trades off a **frozen parquet file** with no
live feed and no position reconciliation. Neither the research claim nor the live system is deployable.

| Experiment | Pass | Trades | Total PnL | Sleeve-4 (S2/S4) mean R |
|---|---|---|---|---|
| Unpatched (claimed) | **23/23** | 6,484 | **+$23,898.46** | **+0.44R** |
| Patched (honest stops, all else identical) | **0/23** | 1,567 | **−$4,895.53** | **−0.57R** |

> The bug flips sleeve-4 expectancy by **≈1.0R per trade**. Every other sleeve is flat-to-negative in *both* runs.

---

## F1 — S2/S4 STOP-ERASURE: 61.1% of stops overwritten with bar-24 MTM [P0 · causal violation]

**Location:** `run_23_oos_altcoin_suite.py` S2/S4 precompile loop (all 4 long/short legs).

```python
r_gain = -1.0
for j in range(i + 1, i + 25):
    if lows[j] <= stop_p: r_gain = -1.0; break      # stop hit, -1R booked...
    if highs[j] >= target_p: r_gain = 2.2; break
if r_gain == -1.0 and highs[min(i+24, n_bars-1)] > stop_p:   # ...then ERASED:
    r_gain = (closes[min(i+24, n_bars-1)] - entry_p) / dist  # rewrite with bar-24 MTM
```

The fallback was presumably meant for *true expiries* (neither barrier touched), but it keys on `r_gain == -1.0`,
which is also the stopped-out value. Any stopped trade whose **final bar merely touches back above the stop** (~always
after 24 bars) gets its −1R replaced by the bar-24 mark-to-market. This is **lookahead-by-rewrite**: information from
bar *i+24* overwrites an exit that physically occurred at bar *j ≤ i+24*.

**Quantification** (`docs/ox58_verification/ox58_erasure_quantify.py`, rerunnable):

- Pool: 49,480 S2/S4 candidates → 37,256 stopped (75.3%), 10,598 TP (21.4%), 1,626 true expiries (3.3%).
- **22,764 / 37,256 stops erased = 61.1%** (46.0% of *all* candidates).
- Mean inflation **+2.154R per overwritten stop**; **+49,037R phantom expectancy** across the pool.

**Decisive experiment:** a minimal patch (4× `stopped_out` flag; fallback gated on `not stopped_out`; signals,
frictions, risk protocol untouched — diff: `docs/ox58_verification/ox58_stopfix_and_tracing.diff`) collapses the
suite to **0/23, −$4,895.53**. Precompile counts are identical across runs (29,035 S2 / 20,445 S4 / 54,629 ORB /
35,388 S1), proving the patch changed *only* exit accounting. Full tables: `repro_unpatched.txt` vs `repro_patched.txt`.

**Attribution of the claimed +$23,898** (`ox58_trade_attribution.py` on the traced rerun, exact reproduction):

| Sleeve | Trades | PnL | mean R |
|---|---|---|---|
| S2_BB (bug) | 2,920 | +$13,030.87 | +0.44 |
| S4_KRI (bug) | 2,602 | +$11,302.61 | +0.44 |
| S1 | 756 | +$34.58 | −0.09 |
| S1_SHORT | 66 | −$292.59 | −0.40 |
| ORB | 61 | −$240.96 | −0.44 |
| T1 | 79 | +$63.95 | +0.07 |

The two bug-carrying sleeves contribute **+$24,333.48 (>100% of the total)**; everything else nets **−$435**.
The flagship S1 dual-model sleeve loses on a per-trade basis (meanR −0.09) *even inside the rigged run*.

**Other sleeves' exits were audited and are SAFE:** S1 labels with a hit flag ✓; T1 uses a `t_exit == −1` expiry flag ✓;
ORB computes stop outcomes as `(sl−entry)/(r+1e−9)`, which is never *exactly* `−1.0`, so its identical-looking fallback
only fires on true expiries (instrumented BTC run: 4,300 trades, **0 overwrites**, 143 expiries) — safe **by float
accident**, flagged as fragile-by-construction (P3).

---

## F2 — LIVE EXITS NEVER REACH THE EXCHANGE [P0 · blocks deployment]

**Location:** `run_live_terminal.py` main loop §3 + `LivePositionTracker.update_positions`.

```python
closed, total_upnl = tracker.update_positions(latest_prices)
for c in closed:
    risk_gov.record_closed_trade(c.get("realized_pnl", 0.0))   # local books only
```

`broker.close_position()` and `broker.modify_sltp()` are **never called anywhere in the live terminal**
(repo-wide grep confirms zero call sites). Consequences in LIVE mode:

- `TARGET_REACHED` / `TIME_DECAY_EXIT` / local `STOP_HIT` mark the trade closed and book PnL locally while the
  **real position stays open** on Binance guarded only by the *initial* stop (ratchets are local-only too).
- A +2.2R "win" on screen can simultaneously be a −1R real loss if price reverses — **the terminal's PnL and the
  account's PnL are decoupled by construction**.
- `execute_trade` intentionally places **NO take-profit on the exchange** (Fable5-2.3 comment), citing a "no hard TP"
  backtest — but *this* suite's backtests assume hard 2.2/2.0/2.2/3R targets. The comment references a different sim
  (`run_all_6`); against the 23-OOS suite the no-TP choice **inverts the validated exit model**.
- `UNVERIFIED_OPEN_POSITION` (naked-guard failure) returns a truthy dict → the terminal books a position at *signal*
  prices with unknown exchange state and never reconciles.

## F3 — 24-BAR TIMEOUT FIRES AFTER ~6 MINUTES [P0]

`pos["bars_held"] += 1` executes **per 15-second poll**, not per 15-minute bar. `TIME_DECAY_EXIT` at `bars_held >= 24`
triggers after **~6 wall-clock minutes** instead of the researched 6 hours — every slow-burn position is "closed"
locally (and, per F2, left open on the exchange) minutes after entry.

## F4 — NO LIVE FEED, NO RECONCILIATION [P0]

- `latest_prices` are read from the **static parquet** (`load_recent_bars`, last close) every poll — no WebSocket, no
  REST kline/ticker fetch in the terminal. Demonstrated: `--once` headless run priced BTC at **$78,210.60 = the last
  parquet close (11 days stale)**, and opened a dry-run S1 long on BCH at a stale print.
- Entries are partly shielded: `execute_trade` anchors GTX limits to **live bookTicker** and rejects drift > 0.35% —
  good design, and it means stale signals usually *fail to fill* rather than fill badly. But the tracker books
  `entry_price` at the stale signal price, so uPnL basis is wrong from bar one.
- The terminal **never syncs with exchange state** (`get_position_state`/`get_all_positions` exist but are never
  called). An exchange-side stop fill leaves the terminal showing the position open; a later local "close" books
  phantom PnL. `broker.connect()` failure is silently ignored (return value unchecked), and `ensure_connected()` is a
  hardcoded-`True` stub.

## F5 — RESEARCH↔LIVE PARITY GAPS (all confirmed by code + numeric test)

| # | Research (23-OOS suite) | Live terminal | Severity |
|---|---|---|---|
| S1 model | Per-window Ridge+LGBM 60/40, calibrated threshold, tide gates | Hardcoded rules (`prob` 0.59/0.62), no ML | P1 — different strategy |
| S1 zc_div gate | Normalized `zc_div/vol_base`, clipped ±3 (P(>0.8)≈0.001%) | **Raw** `zc_div` dollars vs 0.8 (P≈50% — coin flip) | P2 — vacuous gate |
| S3/ORB | 5th sleeve, LGBM top-30% filter | **Absent** (4 of 5 sleeves trade) | P1 |
| T1 | 4H Donchian-20 + EMA/slope/volume/CVD gates, SL-first ratchets 0.35@0.75/0.85@1.40, 2.2R target, 20.5 bps/r_dist friction | 96×15m-bar high only, no gates, tracker ratchets 0.15@0.8/0.8@1.5, 2.5R target | P1 — ~zero parity |
| Fills | Next-bar open ±10 bps (S2/S4/T1) | Signal close, zero slippage | P2 |
| S2/S4 exits | Hold to TP/stop/24-bar, no ratchet | BE/profit ratchets + 6-minute decay | P1 |
| Base risk cap | `min(base, 18)` | `min(base, 24)` — **+33% live risk** (all other tiers match bit-for-bit) | P2 |
| Concurrency | 4 slots, no symbol constraint | 4 slots + one-position-per-symbol (fewer live trades) | P2 |
| S4 sleeve id | 4 | 5 (governor caps {4,5} jointly — benign) | P3 |

Also verified: suite settles PnL **instantly at entry bar** (njit credits full 24-bar outcome at `t`, using `hold`
only for slot occupancy) — reported MaxDD is *trade-sequence* DD, not time-series DD; true simultaneous-open DD can
exceed it. Methodology caveat, P2.

## F6 — FOREX CONTAMINATION OF THE ORB POOL [P2 latent · 0 realized]

`load_cross_asset_orb_crt_pool` emits 11 crypto + 6 forex symbols (GER30/FR40/US2000/GAS/XAUCNH/NICKEL); the suite
filters by **time only**. Measured: **7,144/54,629 pool rows = 13.1% forex**. The traced rerun proves **0 forex trades
executed** (ORB ML filter admitted only crypto; 61/61 crypto) and no non-crypto symbol appears anywhere in 6,484
trades — so realized P&L is clean, but there is **no guardrail**: pool composition, training labels, and any future
threshold/window can admit index/commodity/nickel trades into an "11-asset altcoin" backtest. The [−1.15, 3.0] clamp
additionally hides forex weekend-gap tails.

## F7 — `modify_sltp` CRASHES ON THE FAILURE IT WAS BUILT TO HANDLE [P1 latent]

`binance_broker.py` place-then-cancel: if `_place_algo_conditional` returns `None` (any placement failure), the
`elif ("algoId" in new_sl_res …)` line raises **`TypeError: argument of type 'NoneType' is not iterable`** —
demonstrated by mock (`ox58_broker_mocks.py` T1). The Step-5 naked-guard emergency-close sits *after* the crash line
and never runs. Currently unreachable from the live terminal (F2 — nothing calls it), so latent; any future ratchet
wiring detonates it. (Secondary: the `algoId != 0` guard is ineffective — `sl_placed` was already set `True` by the
identical condition four lines earlier.)

## F8 — BROKER HTTP/ORDER LAYER: CORRECT ✅ (verified by mock, T2/T3)

429 → honors `Retry-After` → retries; 418 → sleeps `min(Retry-After, 60)` → returns `None`, no retry; −1021 → resync +
single retry; 5xx/408 → backoff retries; 1-min weight circuit breaker (>1000/1200 → 1.5 s throttle). Order path:
idempotent `clientAlgoId` SL keys, GTX cancel-*then*-status-check (no double-fill race), anti-double-fill order query,
tick/step/minQty rounding, spread + drift 0.35% rejects, leverage enforcement, min-profit gate, SL 3-attempt naked
guard with emergency close. Genuinely well-built — it is the *terminal's non-use* of it (F2/F4) that fails.

## F9 — DATA LAYER: CLEAN ✅ (verified)

- 11 masters: 2,323,304 bars, 0 nulls, monotonic 15m cadence, 2020-09-01→2026-09-09/10, all suite columns present.
  (`volume` absent in all 18 masters, but nothing downstream reads it; pyarrow-25 silently drops it — cross-version
  fragility P3, not a defect.)
- RSI-14/ATR-14 recomputed from OHLC match stored columns **exactly** (Wilder trailing, post-warmup diff 0.0);
  EMA-200/VWAP-Z trailing-causal. No indicator lookahead.
- `run_historical_pipeline.py` (633L): atomic staged export, SHA-256 manifest chain, 3-agent council gate with
  causal-only repair, fail-closed disk/audit gates, quarantine-on-corruption. The strongest component in the repo.
- Hygiene notes: directive's "3,467,571 bars across 11 perpetuals" ≈ the **18-asset** total (measured 3,475,005;
  universe conflation + stale snapshot, P3); `target_oos_criteria.json` gates (ROI≥10/DD≤5/WR≥40/≥15 trades) match the
  suite; its `"total_assets": 18` confirms the 11/18 conflation.

## F10 — MISC (confirmed, lower severity)

- `--sync` is **dead**: `--skip-sync` defaults `True`, so `if args.sync and not args.skip_sync` is always `False`.
- Live S2-short ema guard matches suite ✓; regime math matches suite ✓; milestone/DD/hous
...[truncated 3401 chars]