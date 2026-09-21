# OX_ALPHA_51 — Institutional Architecture Audit & Live Production Readiness Verdict

**Directive:** Forensic Architecture Audit, Live Microstructure Failure Modes, Model Quantization Budget, Phased Production Deployment Roadmap
**Auditor role:** Chief Quantitative Architect (isolated session, zero prior memory; all findings from first-principles code + artifact inspection)
**Repository:** `kbsingh1399/Trading` — working branch `arena/01a0bf23-trading` (from `44c3bef`)
**Directive pins referenced:** `006283d` (data/commit pin), `f73acaa` (code pin for 6 source files)
**Audit date:** 2026-09-20 UTC
**Artifacts inspected:** `Engine/runners/run_23_oos_altcoin_suite.py` (609 lines), `Engine/core/canonical_indicators.py` (602), `Engine/core/fast_numba_oos_engine.py` (657), `Engine/oos_windows_20.json` (23 windows), `Engine/live/binance_live_monitor.py` (3,577), `Engine/live/inference_engine.py` (275), plus `Engine/run_23_oos_elite_suite.py`, `Engine/run_23_oos_altcoin_suite.py`, `Engine/strategy/s1_dual_model_orderflow.py`, `Engine/strategy/s3_orb_ml.py`, `Engine/core/execution_kernel.py`, `Engine/core/portfolio_execution_kernel.py`, `Engine/live/order_manager.py`, `reports/elite_23_oos_regime_scorecard.csv`, `reports/elite_23_oos_all_trades.parquet` (7,395 rows), `binance_backtesting_data/*_dataset_manifest.json` + live parquet metadata via `pyarrow` (all 18 master files: monotonicity, nulls, row counts).

---

## 0. Executive Verdict: CONDITIONAL NO-GO for live capital — 6 gating defects, all remediable

The system is a **serious, substantially causal research apparatus** with genuinely good bones (prefix-invariant indicator kernels with dedicated tests, 72-hour purge that mathematically covers the 8-hour label horizon, stop-first bar ambiguity, next-open execution in the T1/ORB sleeves and in the conservative elite-suite variant, regime routing, and a verified-monotonic tick-grade dataset). The reported 23/23 quarterly passes are arithmetically consistent with the filed scorecard and trade tape.

**However, it is not safe to deploy to live Binance USDT-M capital today.** The certification baseline (+$42,323.40 / +846.47%) was produced by the **signal-close entry variant**, ~89% of traded PnL rides on **one mean-reversion sleeve**, drawdown is **not mark-to-market**, and — most decisively — **no Binance execution bridge exists in this repository**: the live order path is MT5/forex-only and the Binance monitor is a read-only dashboard. Going live now would mean hand-trading model outputs or writing an execution layer under time pressure — both unacceptable.

| # | Gating defect (P0) | Severity | Remediation size |
|---|---|---|---|
| G1 | Certified PnL uses **signal-close entries** (`entry_p = closes[i]`) for sleeve 4 (~89% of trades). Non-executable in live trading; conservative next-open variant exists but is **not** the certified baseline | High | Re-run certification on next-open variant; publish delta |
| G2 | **No Binance futures execution path exists.** `order_manager.py` = MT5 (`mt5.positions_get`, forex correlation clusters, rollover/Friday lockouts). `inference_engine.py` = MT5/XGBoost forex (FVG strategy), not the LightGBM crypto suite. `binance_live_monitor.py` places zero orders (no `fapi/*/order`, no `python-binance`, `main()` runs dashboards only) | **Showstopper** | Build `Engine/live/binance_execution_gateway.py` + suite adapter |
| G3 | Reported MaxDD is **trade-close-sampled, not bar-level MTM**, and full-trade PnL is credited **at entry timestamp** (`equity += pnl` at event time `t` using final `r_gain`). Open-trade heat is invisible; true peak-to-trough DD is understated by construction | High | Re-score through `PortfolioExecutionKernel` (exists, correct, unused by suite) |
| G4 | **Single-sleeve concentration:** S2+S4 = 88.7% of trades / ~entire PnL; S1 10.2%, T1 0.6%, ORB 0.4%. "Orthogonal multi-sleeve" diversification claim is false; book is one mean-reversion bet | High | Either prove standalone S2+S4 robustness under stress overlays or rebalance/regime-gate |
| G5 | Pinned runner **does not import in this checkout**: `Engine.strategy.s1_liquidation_orderflow…` and `Engine.strategy.s3_orb_crt…` packages do not exist (flat `Engine/strategy/*.py` layout). Certified code ≠ runnable code at HEAD | Medium-High | Reconcile layouts; tag a runnable release commit; re-certify from it |
| G6 | 2022 microstructure features are **~86% imputed** (BTC manifest: `metrics_unavailable_fraction 2022: 0.8656`, 30,602 imputed bars). S1's W6–W8 inputs (liq/CVD/OI) are substantially synthetic in exactly the crisis windows cited as proof of robustness | Medium-High | Ablation: S1 ex-microstructure-features in 2022; disclose or bound |

**If all six are remediated and the re-certification still passes 23/23 (or a pre-registered 21/23 with DD ≤ 5% on MTM accounting), my verdict flips to GO for the phased protocol in §7.** Nothing in the architecture is irredeemable; the indicator core and the conservative execution kernels are production-grade patterns.

---

## 1. Claim-vs-Evidence Forensics (what I verified, byte by byte)

| Certified claim | Forensic result |
|---|---|
| 11 assets, 3,467,571 15m bars, 0 nulls, monotonic | **PARTIALLY FALSE as stated.** Measured with `pyarrow`: 11-asset subset = **2,323,304** bars. The ~3.47M figure matches the **full 18-asset universe (3,475,005)**. Monotonic `open_time_ms` **verified TRUE on all 18 files**; 0 nulls + 0 duplicate timestamps verified on sampled OHLC/feature columns. Date range 2020-09-01 → 2026-09-09 (so W23, ending 09-19, is backtested on a **truncated window** — last ~10 days untested). |
| +$42,323.40 / +846.47% / 7,395 trades / 54.8% WR / 2.94% max DD / 23-23 | **Arithmetically reproduced** from `elite_23_oos_regime_scorecard.csv` + `elite_23_oos_all_trades.parquet` (ΣPnL = 42,323.40; 7,395 rows; sleeve counts match). WR 54.8% plausible from tape. **BUT:** (a) entries are signal-close (G1); (b) DD is not MTM (G3); (c) "846% ROI" is **Σ quarterly ROIs on reset $5k capital** (= 23 sequential $5k sleeves, i.e. $115k of sequential risk deployment), not growth of one $5k account — honest only if labeled as such. |
| Quarterly Sharpe 6.12 vs BTC 0.89 | **NOT REPRODUCED.** From the filed quarterly ROIs: mean 36.80%, σ 22.50% → Sharpe_q = **1.64**, Sharpe_ann ≈ **3.27**. Still excellent, but 6.12 is unverifiable from any filed artifact (possibly a trade-level or monthly-matrix computation — no formula filed). Treat 6.12 as **unsubstantiated** until the estimator is pinned. |
| BTC Buy & Hold +230.47% / 77.06% DD | Plausible for 2021-01 → 2026-09 BTC (not re-fetched; no independent price source in session). Methodology (quarterly-compounded from filed BTC closes) is sound. |
| "100% Causal: Next-Bar Open Fills (opens[j+1])" (top-level suite docstring) | **Overstatement.** True for T1 (`next_open` fill, verified) and ORB (`opens[entry_bar]`, verified). **False for S1** (labeler `entry_p = c[i]`, close-entry) and **false for certified S2/S4** (`entry_p = closes[i]` in runners/ variant). Only the *uncertified* top-level elite variant uses `opens[i+1]×(1±10bps)` for S2. |
| Bandwidth-Z / ADX / KRI enhancement | Present **only** in the runners/ variant (the certified one). Top-level elite has no S4/KRI/BW-Z/ADX code — confirming the certified tape came from the close-entry implementation (at `f73acaa`, where its imports resolved). |
| Prefix-invariant causal indicators | **Code-verified as causal** (all kernels use `min_periods`/expanding warm-up, `ewm(adjust=False)`, rolling windows — no `shift(-1)` or centered windows found). Dedicated tests exist (`verification/test_pipeline_offline.py::test_prefix_invariance`, `tests/test_kairi_indicators.py::test_kairi_prefix_invariance`). Not re-executed here (no `pandas`/`numba` in sandbox; `pip` PEP-668-blocked, venv used only for `pyarrow` audit). |
| 72-hour purge embargo | **Mathematically sufficient** for the stated purpose: max label horizon = 32 bars = 8h (S1), 24 bars = 6h (S2/S4) ≪ 72h. All train/test splits, regime features (`btc_prior < purge_ms`), trailing-vol lookbacks, and ORB/S1 model fits respect the embargo in code. The 384-bar (96h) `rv_rank` filter is past-only, so exceeding the purge length is harmless (it reads *older* history, never the future). |

---

## 2. Q1 — Modularity, Orthogonality & the Risk Budget

### 2.1 The "4 sleeves" are 1 sleeve with decoration

Filed tape attribution (7,395 trades):

- **Sleeve 4 (S2 BB + S4 KRI, sharing one concurrency bucket): 6,562 trades = 88.7%**
- S1 (ML pullback): 756 = 10.2% · T1 (Donchian): 46 = 0.6% · ORB: 31 = 0.4%

T1 fired in only 4 of 23 quarters; ORB never exceeded 10 trades/quarter. The suite's P&L is therefore the P&L of **15m Bollinger/KRI mean reversion with RSI 32/68 gating**, and every diversification/orthogonality claim must be discounted accordingly. Note S2 and S4 are not even separate risk buckets — both carry `sleeve_id=4` and draw from `max_s2_concurrent=2`.

### 2.2 Liquidity-freeze failure mode (the question asked: simultaneous S1/S2/S4 drawdown?)

**Yes — correlated long-into-weakness is the dominant tail.** Mechanics:

- S2 longs `close < lower_band & RSI < 32`; S4 longs `zKRI < −1.75 & RSI < 32`. In a liquidation cascade both conditions *improve* as price falls. The only brakes are the `zbw > 1.85` / `ADX > 32` vetoes (lagging: ADX-14 needs ~10–20 bars to cross 32; bandwidth-Z needs the expansion to be 1.85σ above its own 96-bar mean — by which time 2–4 tranches may already be aboard) and the 2-slot sleeve-4 concurrency cap (which rate-limits but does not de-correlate: both slots go the same direction).
- S1 simultaneously seeks "bull pullbacks" (`c > EMA200 & vwap_z < −0.4 & RSI < 45 & zc_norm > 0`) — in the early leg of a freeze, price is still above EMA200 while mean-reversion longs are already underwater, so S1 adds procyclical long exposure. The bear-contagion S1-short branch only arms on a strict 30-day regime filter (`ATH DD ≤ −35% AND 30d ≤ −10%`), i.e. **weeks** into the event.
- Net effect in a March-2020 / May-2021-intraday / FTX-week pattern: S2+S4 double down the first 6–12 hours, S1 joins on the pullback template, and the shared DD-defense throttle (risk → $6) is the *only* cross-sleeve governor. The filed W8 (+56.6%, DD 1.3%) shows the vetoes *can* work — but W8's DD is trade-close-sampled (G3), so the intraday path through Nov 9–10 2022 is unproven. **Required before live:** a bar-level MTM replay of W2/W6/W8 with open-trade heat curves, plus a synthetic stress overlay (×2 intraday range, −30% funding shock, 3× slippage) demonstrating DD ≤ 5% survives.

### 2.3 Is the shared risk budget (Hsieh–Barmish-style feedback) "mathematically optimal"?

**No — but it is a defensible safety controller, which is the right bar.** What the code actually implements (`simulate_elite_portfolio`) is gain-scheduled feedback, not optimal control:

- DD-defense: `risk = min(base×0.35, $6)` when `DD ≥ 1% or equity < capital` (≈0.12% risk — very conservative);
- House-money: `min(base×1.25, $26)` above +$150;
- Milestone: `min($10, cushion×0.15)` above +$500 with a hard floor-stop lock (`locked=True` halts the quarter).

 virtues: bounded portfolio heat (4 slots × ≤$26 ≈ $104 ≈ 2.1% of capital vs 4.85% breaker — coherent layering), fast de-risking,convex payoff profile that mechanically produces the filed low-DDs. Defects: (i) milestone-lock **halts the quarter**, so filed PnL embeds an idle-capital drag that flatters DD while understating opportunity cost — must be disclosed as a stopping rule, not alpha; (ii) no volatility targeting (a $22 risk means 0.44% in calm vs effectively multiples more in stress — risk is constant in *R*, not in *σ*); (iii) no Kelly/optimal-f derivation anywhere — the "Hsieh–Barmish" label is aspirational. **Recommendation:** keep this controller as the *safety layer* and add a *sizing layer* (fractional-Kelly capped at current bounds, volatility-scaled notionals). Do not market the current scheme as optimal.

---

## 3. Q2 — Causality & Lookahead Prevention

### 3.1 Sleeve-by-sleeve entry audit

| Sleeve | Signal bar → fill | Verdict |
|---|---|---|
| S1 (ML) | `entry_p = c[i]` (`label_triple_barriers_numba`), forward scan from `i+1`, ratchet armed causally (`j−1`), stop-checked before target | **Close-entry: optimistic by the close→next-open gap + spread.** Ratchet/stop logic itself is clean and conservative. Fix: re-label at `opens[i+1]` (the correct kernel already exists in `execution_kernel.py` — use it). |
| S2/S4 certified (runners/) | `entry_p = closes[i]` | **Same defect, ~89% of tape.** The uncertified top-level elite variant does it right (`opens[i+1]×(1±10bps)`). Expected haircut on re-certification: roughly half-spread + overnight-gap drift per trade; with 2.2R targets and ~30bps friction budget the edge likely survives but the +95% quarters (W10) will compress — re-run, don't assume. |
| T1 | `fill_px = next_open×(1±10bps)`, friction `(px×20.5bps)/R` | **Correct.** Institutional-grade. |
| ORB | `entry = opens[entry_bar]`, 24-bar cap, BE/profit ratchets | **Correct.** Institutional-grade. |

### 3.2 Indicators, purge, and the DD-sampling flaw

- **Indicators: PASS.** `canonical_indicators.py` is genuinely causal (verified by inspection: expanding warm-ups, `adjust=False` EWMs, trailing-only rollings; Ichimoku/BBW-Z/ADX/KRI all bar-`t`-measurable). The 72h purge covers the 8h label horizon 9× over; regime features, tide mapping (causal EMAs), and all model fits respect it. No `shift(-1)`/centered-window leakage found in the audited path.
- **DD accounting: FAIL (G3).** `simulate_elite_portfolio` credits each trade's *final* R at its *entry* timestamp with no intra-trade MTM. Consequences: (i) reported MaxDD cannot exceed what trade-close sampling sees — a −0.9R open excursion that recovers to +2.2R prints as **zero** drawdown; (ii) DD sequencing is time-distorted (PnL appears up to 8h early). The "2.94% max DD, 26× lower than BTC" comparison is therefore **backtest-accounting vs market-MTM — not like-for-like**. The fix is cheap: the repo already contains a correct bar-level MTM engine (`PortfolioExecutionKernel`: `Open[j+1]` fills, stop-first, per-bar equity marking, DD breaker). **Re-score the entire 23-quarter tape through it and re-certify; publish both DD series.**

---

## 4. Q3 — Live Microstructure Bridges

### 4.1 Maker-vs-taker: the policy must be taker-first at pilot, with measured migration

- Backtest assumes ~22–30bps all-in friction (0.18–0.25R at the 1.2% ATR stop floor) vs Binance VIP0 reality: 2bps maker / 5bps taker per side (+ spread + funding). The budget is *adequate for taker execution* — but only if entries move to next-open equivalents (marketable limit at touch + 10bps, as the T1 sleeve already models).
- **Do not launch with post-only maker entries.** Mean-reversion fills are adversely selected by construction (you get filled when price keeps falling through your bid). Unmodeled adverse selection on 88.7% of flow is a larger edge leak than the 3bps maker/taker spread differential. **Policy:** Stage 1–2 = marketable-limit taker execution, measured slippage vs backtest assumption per sleeve; Stage 3 = post-only maker *only* for exits (take-profit legs, which are positively selected) after a 30-day fill-rate/adverse-excursion study. Log `expected_px vs fill_px` on every fill; abort maker migration if 1-minute post-fill excursion < −2bps systematically.

### 4.2 Funding, margin, liquidation engine, ADL (currently: unmodeled — G-grade gap for live)

- **Funding:** never deducted in backtest (it's only an ML feature + veto). Quantify: typical notional per trade ≈ $20 risk / 1.2% stop ≈ **$1,600–1,800 notional** (~0.35× leverage on $5k — small, good). Typical funding 0.01%/8h → ~$0.17/hold — negligible. **Stress funding (0.3–0.75%/8h, seen in 2021/2024 squeezes) → $5–13/trade = 25–65% of the risk budget**, and holds up to 32 bars (8h) guarantee funding crosses. With 4 concurrent positions through a 3-interval squeeze weekend, funding alone can print −$50–150 (−1–3% of capital) with zero price movement. **Fix:** deduct interval funding from paper/live PnL using the filed `funding_rate_pct` series (backtest) and `markPrice` stream `r` (live — the monitor already ingests it); add a funding veto (skip longs when predicted 8h funding > 0.15%, symmetric for shorts).
- **Margin/liquidation/ADL:** notional sizing implies isolated-margin, ≤2× effective leverage — exchange liquidation of the *account* is near-impossible, but per-position stops must still be **server-side** (`STOP_MARKET`/`TAKE_PROFIT_MARKET` with `reduceOnly`, `workingType=MARK_PRICE`) because a WS disconnect during a cascade with only local stops = unprotected exposure. ADL risk at this size is nil, but the gateway must still handle `ADL` feed flags and `forceOrder` stream halts by freezing entries (the monitor already parses `@forceOrder` — wire it to the entry gate). **Missing and required:** `set_leverage`, `set_margin_type=ISOLATED`, `positionSide` (one-way vs hedge — pick ONE-WAY to match backtest netting), listen-key refresh, `recvWindow` + clock-skew guard, idempotent `newClientOrderId` (deterministic: `OXA51-{signal_bar_ms}-{symbol}-{sleeve}`), and a **dead-man's switch** (cancel-all + flatten on heartbeat loss > 60s).

### 4.3 Feed & state failure modes the monitor handles well vs gaps

- **Strengths (real):** sequence-validated L2 book, liquidation-state aggregation, CVD/footprint reconstruction, REST gap-fill with checkpointing, token-bucket rate limiting, 8-stream fan-in. This is above-average retail infra.
- **Gaps for autonomous trading:** no staleness kill-switch wired to order gating (add: halt entries if any required stream lags > 5s or book `lastUpdateId` gap unresolved); no deterministic bar-close handshake (partial `kline` updates must never trigger inference — gate strictly on `k.x == true` + exchange `T` timestamp, not local clock); 4h-reference refetch is synchronous REST (move off the signal path — cache, refresh async).

---

## 5. Q4 — Model Quantization & the 100ms Latency Budget

**Verdict: no quantization is required; the 100ms budget is satisfiable with plain CPython + preloaded models. Quantization would add operational risk for zero needed gain.**

Budget decomposition per 15-minute close (11 assets, ≤ ~11 candidates — one signal evaluation per asset per bar):

| Stage | Measured/estimated cost | Notes |
|---|---|---|
| Kline-close detection (`k.x==true`) → dispatch | 1–5 ms | WS-driven, no polling in steady state |
| Incremental indicator update (800-bar pandas buffer, vectorized rolling) | 3–15 ms/asset → **~30–60 ms sequential, ~10 ms parallel** | Dominant cost is *pandas recompute*, not ML. Precompute on websocket tick; at close only finalize the bar |
| Ridge (19-feature dot) + LightGBM (160 trees, depth 4, 15 leaves) per candidate | **< 1 ms/candidate** | ~11 candidates → < 10 ms total; LightGBM `predict` releases the GIL |
| Regime/threshold gating + risk checks | < 1 ms | Pure Python scalars |
| Order dispatch (async REST, non-blocking) | 0 ms on signal path (fire-and-forget with callback) | Exchange ACK 50–300 ms happens *after* the decision; does not consume the 100ms budget |
| **Total decision latency** | **p50 ~20 ms, p99 < 80 ms sequential; < 30 ms with fan-out** | Exchange fill occurs next-tick — consistent with next-open backtest fills |

- **GIL:** non-issue. Inference is microseconds of Python + GIL-released native code; 11 assets sequential is fine. Use one `asyncio` loop + threadpool for the pandas tail, or precompute features incrementally per tick.
- **Treelite/ONNX INT8/FP16:** explicitly **not recommended** for this workload — LightGBM trees are already branch-efficient; INT8 buys nothing at 11 inferences/15min and introduces score-parity drift vs the certified booster (any re-certification would have to be redone on quantized scores). **Do this instead:** (1) serialize the exact certified booster + `mu/sd`/threshold bundle per window-regime with SHA256 pinning; (2) add a live-vs-backtest score-parity probe (log every live `prob`; nightly KS-test vs backtest distribution; alert on drift > 0.02); (3) keep ONNX in the backlog only if the universe scales past ~100 assets or below 1-minute bars.
- **Real latency risks (ranked):** (i) cold-start indicator warm-up (800+ bars × 11 assets on restart — pre-warm from parquet, then WS-top-up); (ii) synchronous 4h REST refetch on the signal path (move async); (iii) pandas full-buffer recompute per tick (switch to incremental tail update); (iv) GC pauses (preallocate, avoid per-tick DataFrame churn).

---

## 6. Additional Findings (outside the five questions, material to safety)

1. **Regime-label sanity:** W2 (May-2021 crash quarter) is labeled `BULL_EXPANSION` and traded with T1 breakouts enabled. The 30-day trailing classifier is slow by design (that's fine — it's causal), but the label set in the scorecard describes *trailing* state, not the quarter's realized regime. Rename to `trailing_regime_at_entry` to prevent misreading robustness evidence.
2. **W15 fragility marker:** 36 trades, +12.6% ROI, 44.4% WR — the thinnest pass, closest to the 15-trade / 10% boundaries. Any re-certification haircut lands here first. Pre-register W15 as the canary window.
3. **W23 truncation:** dataset ends 2026-09-09; W23 runs to 09-19. Re-run W23 when data is complete; do not cite it as a full-quarter pass.
4. **Monthly matrix has gaps** (`--` months in 2021–2024) while quarterly scorecard shows continuous trading — reconcile the monthly attribution before citing monthly Sharpe/consistency.
5. **Pre-launch tests are forex-only** (`test_prelaunch.py`, `test_execution_safety.py` target MT5 flows). A Binance-suite pre-launch harness does not exist — it is on the P0 backlog (§8).
6. **Good patterns worth preserving:** T1/ORB next-open discipline; stop-first ambiguity everywhere; causal EWM/rolling discipline; token-bucket REST discipline; deterministic-ID-ready order flow (to be built); the unused-but-correct `execution_kernel`/`portfolio_execution_kernel` pair — the fastest path to a credible re-certification is routing the suite through these.

---

## 7. Phased Go-Live Protocol (exact operational gates)

**Entry condition: all P0 remediations (§8) merged, re-certification run from a tagged release commit, artifacts filed.**

### Stage 0 — Remediation & re-certification (no capital, ~2–3 weeks)
- Route S1/S2/S4 labeling through next-open fills; re-score all 23 windows through `PortfolioExecutionKernel` with bar-level MTM; deduct interval funding + VIP0 taker fees per fill.
- **Promotion gate:** ≥ 21/23 quarters pass (ROI ≥ 10%, **MTM** DD ≤ 5%, WR ≥ 40%, ≥ 15 trades); W15 must pass; no quarter with MTM DD > 6%. File both close-entry and next-open tapes with deltas explained.

### Stage 1 — 14-day paper dry-run (shadow, $0 risk)
- Live WS → full signal path → order *intents* logged with `expected_px`; no REST order submission (gateway in `DRY_RUN`, enforced by config + missing API secret).
- **Parity gates (all must hold):** signal parity vs offline replay ≥ 99.5%; feature parity (|live−offline| ≤ 1e-6 on OHLC-derived, ≤ 1% on flow-derived); score parity (nightly KS p > 0.05); p99 decision latency < 100ms; zero unhandled stream gaps > 5s without entry-halt. **Abort:** any gate red on 2 consecutive days → back to Stage 0.

### Stage 2 — 30-day micro-pilot ($500 capital, 10% risk = divide all USD risk bounds by 10)
- Taker-only marketable limits; isolated margin; account leverage cap 3× (effective will be ~0.35×); server-side `STOP_MARKET`/`TAKE_PROFIT_MARKET` `reduceOnly` on every position; dead-man's switch armed; max 2 concurrent (not 4); funding veto active; kill-switch: **halt week if MTM DD ≥ 2.5%**; halt pilot if MTM DD ≥ 4% or funding drag > 15% of gross.
- **Promotion gate:** ≥ 20 fills; measured slippage within 1.5× of backtest assumption per sleeve; live-vs-backtest expectancy overlap (live mean-R within backtest 95% CI); zero dead-man's triggers unexplained; reconciliation (exchange vs local ledger) exact to the cent daily.

### Stage 3 — Full production ($5,000, full risk budget)
- Restore 4-slot concurrency; keep taker-first for entries; maker-migration for exits only after §4.1 study; weekly model-health review (calibration drift, regime-threshold hit rates); monthly re-certification of trailing quarter; **standing circuit breakers:** daily loss halt −2%, weekly DD halt −3.5%, account DD halt −4.5% (flatten + human review); funding-squeeze auto-derisk (halve size when trailing-24h funding > 0.3%); black-swan protocol (book-feed gap > 30s or `forceOrder` rate > 50× baseline → cancel-all, tighten stops to breakeven, freeze entries 4h).

---

## 8. Remediation Backlog (file-level)

**P0 (gating):**
1. `Engine/core/fast_numba_oos_engine.py` — S1 labeler: fill at `opens[i+1]` (+10bps adverse), keep stop-first/ratchet; re-run `compile_dataset_with_numba`.
2. `Engine/runners/run_23_oos_altcoin_suite.py` — S2/S4: fill at `opens[i+1]×(1±10bps)` (mirror top-level elite lines 221–247); reconcile with `Engine/run_23_oos_elite_suite.py` into ONE canonical runner; delete or repair the broken duplicate imports.
3. New: route suite scoring through `Engine/core/portfolio_execution_kernel.py` (bar-level MTM, funding + fee deduction); re-file scorecard + trade tape + heat curves for W2/W6/W8/W15.
4. New: `Engine/live/binance_execution_gateway.py` (testnet → mainnet, isolated margin, server-side stops, idempotent IDs, dead-man's switch, funding/ADL guards) + `Engine/live/crypto_suite_adapter.py` (LightGBM bundle loader, warm buffers, `k.x==true` gating) + `Engine/tests/test_binance_prelaunch.py`.
5. Tag release commit (e.g. `ox51-rc1`); re-certify exclusively from it; archive booster/SHA256 bundle.
6. S1 2022 ablation (ex-imputed-features) + W23 completion re-run; publish.

**P1 (pre-pilot):** funding deduction + veto; taker-slippage measurement harness; score/feature parity probes; staleness kill-switch wiring; 4h-cache async refactor; monthly-matrix reconciliation; Sharpe methodology note (retract or derive 6.12).
**P2 (production hardening):** maker-exit study; fractional-Kelly sizing layer; 4-slot → volatility-scaled concurrency; multi-instance/health verification for the gateway (`verify_live_terminal_health.py` pattern exists — extend it).

---

## 9. Bottom Line

This is **above-average quant research infrastructure with a below-threshold live-readiness state**. The indicator mathematics, purge discipline, and conservative kernels show genuine institutional literacy; the backtest headline (+846%, 23/23) is arithmetically honest but **structurally flattered** (close-entry fills, non-MTM drawdown, single-sleeve concentration, reset-capital ROI presentation, imputed 2022 microstructure, unverifiable Sharpe). The live stack, as filed, **cannot place a Binance trade at all**.

**Recommendation:** **NO-GO on live capital today → conditional GO through §7 once P0 items clear and MTM re-certification passes.** Estimated path: 2–3 weeks remediation + 14-day paper + 30-day micro-pilot before any $5,000 deployment. The system is worth that investment — the bones are good enough that a clean re-certification has a genuine chance of holding.
