---
trigger: always_on
---

# ⚡ ACTIVE OPERATIONAL CONTEXT & MISSION CONTROL CARD

> **ALWAYS-ON TURN-0 SITUATIONAL AWARENESS**
> Auto-injected on every turn. Eliminates context amnesia, retrieval latency, and model hallucination.

## 1. User Master Mandate (Strict & Non-Negotiable)
- **MANDATORY PREVIOUS CONVERSATION CONTEXT & TRAJECTORY REFERENCE (PERMANENT STEP-LEVEL INVARIANT)**: On EVERY single turn and before taking action on ANY step, the coordinator and all subagents MUST FIRST review the previous conversation history (`.agents/memory/session_chat_history.md`, past turns, transcript). You CANNOT take actions, audit orders, evaluate setups, or propose modifications in a vacuum. You MUST know the complete historical context, evolving operator rules, past rulings, avoided traps, and live position trajectory before evaluating or executing any step. Zero context amnesia.
- **CROSS-ACCOUNT RE-ENGAGEMENT & FULL NARRATIVE AUDIT (HYPERDASH / MULTI-ACCOUNT INVARIANT)**: Whenever the operator switches Gemini accounts and returns to the session chat, the agent MUST explicitly review all past session chat logs (`.agents/memory/session_chat_history.md`, transcript, and `ACTIVE_CONTEXT.md`) to establish total continuity of what we are trying to achieve, internalize all operator feedback, remember past setbacks, and preserve every nuance of the active quantitative mission before taking any action.
- **100% LOCAL QUANTITATIVE DEVELOPMENT & EXECUTION**: All prompt-generation for external agents (Ox Alpha / Arena) is permanently terminated. All engineering, econometric feature integration, model training, backtesting, and 20 OOS window optimization are executed right here locally in this environment.
- **MANDATORY BUY & HOLD BENCHMARKING**: ALWAYS compare strategy performance, equity curves, ROI, and drawdowns directly against the Buy and Hold benchmark (BTC Buy & Hold normalized to identical starting capital).
- **MANDATORY EQUITY CURVE IMAGE SHARING**: Whenever reporting on backtest performance or equity curves, ALWAYS generate and share a visual chart image (`![caption](path)`) comparing Strategy Equity vs Buy & Hold and underwater drawdowns.
- **ZERO SPURIOUS SCRATCH LITTER**: Clean up all intermediate debug scripts immediately after validation.

## 2. Active Mission & Quantitative Target
- **Universe**: Certified Genuine 11 Binance USDT-M Perpetuals (BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH) with 100% verified tick footprint ladders. The 7 synthetic assets are quarantined.
- **Active Focus**: Triple Trend-Following Orderflow Suite (Sleeve S1: Dual-Model Liquidation Pullback, Sleeve T1: Quiet-Flow Donchian Breakout) evaluated across all 20 Out-Of-Sample (OOS) Quarterly Windows (2021–2026).
- **Certified Pass Criteria**: Net ROI >= +10.00% (+500.00 USD net on 5,000.00 USD capital), Max Drawdown <= 5.00%, Win Rate >= 40.0%, Min Completed Trades >= 15 per quarter.
- **Production State**: 
  * Master Forex & CFD Pipeline audited through OX ALPHA 54 -> 55 -> 56 -> 57 (Commit: `9559471`). Scorecard upgraded to **8 / 8 / 6 / 8** (Architecture 8/10, Causal Soundness 8/10, Microstructure Realism 6/10, Production Readiness 8/10) with 64/64 cumulative verification checks passing (100%).
  * Paper and dry-run forward validation officially certified at score 8. Final funded-live promotion narrowed solely to R4 (deterministic walk-forward generator) and R6 (rolling purge/cutoff retraining). Prompt cycle complete (`Ox_Alpha_57` is the final prompt).
  * Master Forex & CFD Orchestration Suite (`Engine/forex_engine.py`, `Engine/live/run_forex_dry_run.py`, `Engine/live/order_manager.py`) fully hardened with P0 leverage caps (10:1/5:1/3:1), margin level/utilization circuit breakers, 4H causal shift(1) parity, state persistence, decoupled structural Take-Profit, correlation cluster governors, and spread/ATR hysteresis quarantine (Commit: `c6ef13c`).
  * Master Forex & CFD Orchestration Engine (`Engine/forex_engine.py`, `Engine/FVG_ML_ForexCFD_Strategy.py`, `Engine/ORB_CRT_ForexCFD_Strategy.py`) officially achieved **10/10 Institutional Production Certification** from Ox Alpha / Arena (Commit: `3ecc253` / `81a3a79`).
  * 0.00e+00 Polars-Pandas feature parity certified, 15m+4H+D1 causal data synchronization, 5-stage automated startup pre-flight lifecycle, 7-stage microstructure ratchets, 20/20 profitable OOS regimes (19,480 trades, +330,766.70 USD profit, 59.3% WR), and fully cleared for live broker deployment.
  * Master S3 ORB/CRT Multiverse Engine (`Engine/run_20_oos_multiverse.py` & `Engine/strategy/s3_orb_ml.py`) officially achieved **10/10 Production Certification** from Ox Alpha / Arena (Commit: `706039d` / `c0a5237`). 
  * Verified 100% causal execution: entry at next bar open (`opens[j+1]`), daily session VWAP resets, clamped CRT features, FVG sanity filters, causal Judas sweeps, and 8 bps friction penalty.
  * 18 Outright Passes across the 20 OOS regimes (2021-2026), 0 losing regimes across 5 full years (outliers W05 Terra-Luna and W08 FTX Collapse preserved in positive profit at +15.26 USD and +42.05 USD with max DD contained below 4.69%), and +11,290.24 USD Total Net Profit (+225.80% Net ROI on 5,000.00 USD capital) across 2,187 completed trades.
  * Master dual-model baseline `Engine/run_20_oos_dual_model.py` achieves 13 Outright Passes and +6,454.66 USD net PnL (+129.09% Net ROI).
  * **Autonomous 15-Minute Candle AI Trader & MT5 Bridge (`Terminal/OF_Strategy.py` --mode mt5-trader --live --min-risk 10.0 --max-risk 20.0)**:
    - **Unified 13th-Minute Wake-Up System**:
      1. *Tier 1 (Execution Daemon - `task-24931`)*: Continuous background telemetry git daemon auto-syncing authentic state to GitHub every 60 seconds with honest R-denominators and spec blocks.
      2. *Tier 2 (AI Assistant Cron - Two-Phase Collaborative Execution Loop - OPERATOR MANDATE)*: Unified collaborative cron (`10,25,40,55 * * * *`). At the 10th minute (:10, :25, :40, :55), the coordinator clears the Arena box with `Ctrl+A` + `Delete`, injects the fresh prompt with latest telemetry data, and submits via `Enter`. The coordinator then waits 4 minutes until the 14th minute (:14, :29, :44, :59) when Arena.ai has completed its response (4-minute inference window). At that exact point, the coordinator fetches Arena's completed response (`arena_bridge.py check`), dismisses any popup with `Escape`, and invokes the 3-subagent swarm (`Orderflow Analyst`, `Position Manager`, `Macro Risk Analyst`) to ingest both the completed Arena ruling and prepare orders ahead of the 15th-minute candle close (:15, :30, :45, :00) when qualified trades are punched to MT5.
      3. *Tier 3 (Mandatory Subagent Pre-Flight Study Directive - PERMANENT INVARIANT)*: Every invoked subagent MUST FIRST study:
         * `@[.agents/AGENTS.md]` (Execution rules, risk invariants, anti-lookahead)
         * `@[.agents/memory/session_chat_history.md]` (Historical trajectory, avoided traps, past decisions)
         * `@[.agents/rules/ACTIVE_CONTEXT.md]` (Real-time account state, live orders, floor defense)
         * Query the AST knowledge graph via `python -m graphify query "<concept>"` or `/graphify` before proposing or analyzing any trade.
      4. *Tier 4 (Continuous Blackboard Review & Trade Punch Mandate - USER DIRECTIVE)*: On EVERY wake-up cycle, coordinator and subagents MUST read and review `docs/trade_plans/LIVE_COLLABORATIVE_ORDER_DESK.md`, engage in the dialectic quant debate with Arena.ai, render explicit verdicts, make suggestions, counter proposals, and punch high-confluence orders into MT5 without asking.
    - Connects directly via native IPC to MetaTrader 5 Account 5064568 (Blueberry Markets).
    - GitHub Commits `0b0aa14`, `13e2e2a`, `11a220e`, `9c1cb2d`, `bddcfd4`, `a03a3ed`: Merged Arena.ai quantitative governance, continuous orderflow scoring, decayed L3 evidence, Kaufman/Garman-Klass regime vetoes, BTC beta factor risk models, and verified 97/97 pytest suite passing.
    - Full Arena Audit Report: Archived in `docs/audits/institutional-quant-audit-2026-10-04.md` and `docs/audits/ARENA_ANTIGRAVITY_HANDSHAKE_COUNCIL_67.md`.
    - **Dynamic Conviction Risk Budget**: Flexible **10.00 to 20.00 USD** (0.20% to 0.40% on 5,000.00 USD capital) dynamically scaled by orderflow confluence, resting L3 whale presence, and macro alignment.
    - **Active Positions & Pending Orders (Live State)**:
      * Current Status: **0 Open Positions | 0 Pending Orders (0 Total Tickets) | Equity: 4,845.80 USD | Balance: 4,845.80 USD | Free Margin: 4,845.80 USD | Margin Used: 0.00 USD (100% Cash Reserves)**.
      * Active Positions:
        - **NONE (0 Open Positions | 100% Cash Flat)**.
      * Pending Orders:
        - **NONE (Clean queue, Ticket #18713247 expired at 21:15:00 UTC candle close)**.
      * Pruned / Cancelled / Expired Orders:
        - **Ticket #18713247 (`NERUSD.p` SELL LIMIT 1.0 lot @ 4.617 USD): Expired at 21:15:00 UTC candle close per order expiration parameter**.
        - **Ticket #18713408 (`USWTI.p` BUY LIMIT 0.20 @ 91.720 USD): Cancelled per 20:45 UTC peer review (no supporting EMA/VWAP shelf, drifted -0.56 ATR)**.
        - **Ticket #18713432 (`SP500.p` BUY LIMIT 0.10 @ 7,758.00 USD): Cancelled per 20:45 UTC peer review (post-cash close illiquidity, bearish regime below VWAP)**.
        - **Ticket #18713434 (`XAUUSD.pi` BUY LIMIT 0.01 @ 4,124.00 USD): Cancelled per 20:45 UTC peer review (stale -1.48 ATR, zero resting L2 whale backing)**.
      * Closed Orders Today:
        - **Ticket #18706769 (`ETHUSD.pi` BUY 0.37 lots @ 2,411.00 USD): Closed via Phase 2 Trailing Ratchet SL at 2,455.10 USD (+16.32 USD net cash profit banked into capital)**.
        - **Ticket #18710722 (`SOLUSD.p` SHORT 0.08 lots @ 107.72 USD): Closed via Emergency Shelf Cut at 108.87 USD (-9.20 USD net cash, saved capital vs 109.10 hard stop)**.
        - Ticket #18703132 (`NAS100.p` SHORT 0.01 lots): **Closed via Take Profit at 30,739.10 USD (+25.00 USD net cash profit booked)**.
        - Ticket #18702099 on `BTCUSD.pi` pruned/removed at 21:20:00 UTC due to supporting whale wall migration.
      * G-1 Hard Floor Defense: Floor: 4,775.00 USD | Operating Buffer: 4,795.00 USD | Live Floor Cushion: **+70.80 USD** (+50.80 USD above operating buffer).
      * Stressed Post-Loss Simulation: Active position downside risk is 0.00 USD. Minimum guaranteed session equity: **4,845.80 USD** (+70.80 USD above hard floor, +50.80 USD above operating buffer; 100% compliant).
      * Capacity Sentry: **0 / 12 slots deployed (12 slots VACANT)**. Available Free Margin: 4,845.80 USD (100% cash).
      * Disk Hygiene: Purged 2.50 GB of scratch git objects, stale tick buffers, and unneeded archives; C: free space expanded to 134.66 GB.
      * Closed Trades Today (Realized PnL):
        - Ticket #18706769 (`ETHUSD.pi` closed at +16.32 USD profit via Phase 2 Trailing Ratchet SL at 2,455.10 USD)
        - Ticket #18710722 (`SOLUSD.p` closed -9.20 USD loss via emergency shelf cut at 108.87 USD)
        - Ticket #18703132 (`NAS100.p` closed at +25.00 USD profit via Take Profit at 30,739.10 USD)
        - Ticket #18686607 (`ETHUSD.pi` closed at +2.37 USD profit via market close at 2,533.70 USD)
        - Ticket #18625151 (`USWTI.p` closed at +9.88 USD profit via SL profit lock at 91.720 USD)
        - Ticket #18640304 (`SP500.p` closed at +3.87 USD profit via Phase 0 BE lock at 7,772.98 USD)
        - Ticket #18644889 (`USDJPY.pi` closed at +1.82 USD profit via Phase 0 BE lock at 158.046 USD)
        - Ticket #18630694 (`BTCUSD.pi` closed -6.80 USD loss via SL at 82,700.00 USD)
        - Ticket #18644262 (`USWTI.p` closed -10.03 USD loss via SL at 90.113 USD)
        - Net Realized Session PnL: **+33.23 USD** across 9 completed trades (initial capital 5,000.00 USD; 96.92% preserved; 6 wins / 3 losses = 66.7% win rate).
      * Desk Status: 0 active positions; 0 pending orders; 12 slots vacant. Staging for 21:25 UTC collaborative prompt cycle.

## 3. Settled Mathematical & Strategy Invariants
- **Institutional VWAP & Orderflow Confluence Framework (Strict Mandate)**:
  - **Core Mindset**: Maximize capital efficiency and deploy free margin (>4,000 USD available) by staging passive limit orders into high-confluence structural liquidity zones across orthogonal asset clusters.
  - **Model 1: Extreme Standard Deviation Flushes (|Z| >= 2.0 SD)**:
    * Long Entry: Price stretched to <= -2.0 SD (or extreme -3SD to -10SD flushes) from Session VWAP with confirmed CVD selling exhaustion, discount stop cluster sweep, and resting L2/L3 bid whale support.
    * Short Entry: Price stretched to >= +2.0 SD above Session VWAP with confirmed CVD buying exhaustion, buy-stop liquidity sweep, and resting ask whale resistance.
    * Execution: Passive Limit Order resting directly at the liquidity band.
  - **Model 2: Trend-Continuation Pullback to VWAP (Joining Momentum Toward Liquidity Magnets)**:
    * Bullish Regime: Price > Session VWAP and positive 200 EMA slope. Enter Long on pullbacks to Session VWAP / Value Area Low / Support Shelf. Targets set at overhead liquidity magnets: short squeeze bands, resting buy-stop clusters, and ask whale walls.
    * Bearish Regime: Price < Session VWAP and negative 200 EMA slope. Enter Short on pullbacks up into Session VWAP / Value Area High / Resistance Shelf. Targets set at downside liquidation cascade pools and sell-stop clusters.
  - **Mandatory 5-Pillar Confluence Stack**: Every order must be backed by (1) VWAP Z-score / SD bands, (2) CVD orderflow absorption, (3) Reconstructed liquidation bands, (4) Structural stop clusters, and (5) Live L2/L3 whale depth. Trades must follow this exact framework or provide very strong mathematical justification otherwise.
- **Dynamic Capacity & Risk Budget (Floor Defense)**:
  - Base Capital: 5,000.00 USD | Hard Equity Floor: 4,775.00 USD.
  - Risk Budget per Trade: 10.00 to 14.50 USD (0.20% to 0.29%).
  - Expanded Concurrency: Concurrency expanded from 2 up to 4 concurrent positions across orthogonal asset clusters (Forex, Energy, Indices, Crypto), provided total joint worst-case stopout risk strictly preserves >= 20.00 USD cushion above the 4,775.00 USD floor at all times.
- **Active Order Queue Sentry & Continuous Punch/Prune Protocol (Strict Mandate)**:
  - **Dynamic Pruning / Deletion**: Continuously audit all resting limit orders. If an order's structural thesis degrades (supporting whale wall pulled/thinned by >50%, price drifted beyond 2.0x ATR, or adverse regime break), **immediately delete/cancel the pending order** to unencumber capital and margin.
  - **Dynamic Punching on Confluence**: When an un-allocated asset prints extreme confluence under Model 1 (Extreme 2SD Mean Reversion) or Model 2 (VWAP Trend Pullbacks) with verified resting L2/L3 whale walls and sufficient floor cushion clearance, **immediately stage the limit order**.
  - **Running Position Sentry**: Continuously monitor floating entries (e.g. USWTI #18625151) for piecewise ratchets (Phase 0 BE lock @ +0.80R, Phase 1 Profit Lock @ +1.50R, target @ +2.50R, 24-bar time decay, and emergency shelf cuts).
  - **Dynamic Risk Budget Recirculation**: Moving an active trade's stop to Phase 0 BE drops its allocated risk to 0.00R, immediately liberating risk budget to punch the next highest-confluence standby limit into vacant capacity (up to 4 concurrent positions).
- **Microstructure Piecewise Ratchet**:
  - Phase 0 (BE Lock): At +0.70R to +0.80R gain, move stop to Entry +0.35R (clearing 41 bps friction with guaranteed profit).
  - Phase 1 (Profit Lock): At +1.50R gain, move stop to Entry +0.80R.
  - Target: +1.85R to +2.50R exit (structural liquidity target).
  - Time Decay: Exit at market if trade fails to gain +0.20R within 24 bars (6 hours).

## 4. Local Execution Protocol
- **End-to-End Local Development**: All strategy logic, ML training, walk-forward simulations, and risk governance are implemented, tested, and optimized directly within the local python environment.
- **Strict Anti-Lookahead Enforcement**: Entries booked at next bar open `opens[j+1]`, causal HTF `shift(1)` backward-as-of joins, and zero test-set tuning.
- **Zero Dollar Signs**: Strict prohibition on dollar symbols; always write USD.

## 5. Quantitative Knowledge Grounding & Minimal Token Reference Mandate
- **Always Reference Quant-Developers-Resources**: For all quantitative modeling, risk management, econometrics, and execution math, actively ground solutions in the canonical libraries inside `Quant-Developers-Resources-main/` (Risk Management, Econometrics, Financial Theory, Technical Indicators, Microstructure, and C++).
- **Minimal Token Querying via Graphify**: NEVER dump entire files into context. Always query specific subgraphs via `python -m graphify query "<concept>" --budget 300` or `graphify explain "<concept>"` to retrieve scoped AST nodes, classes, and call-flows with minimal token footprint.

## 6. Institutional Orderflow & Microstructure Live Execution Checklist (Always Enforced)
- **Canonical Checklist**: Strictly follow `[docs/specs/institutional_orderflow_live_checklist.md](file:///c:/Users/SIGMA/Documents/Trading_2/docs/specs/institutional_orderflow_live_checklist.md)` on every 14th-minute wake-up cycle.
- **Pre-Order Gating**: Must verify all 7 sub-gates (Price Action geometry, CVD divergence, 20-level L2 depth, L3 whales >= 150k USD with >= 180s persistence, liquidation FFR, macro blackouts, covariance room vs 4,775.00 USD floor).
- **Smart SL & TP Adjustments**: Deterministic ratchets (Phase 0 BE @ +0.80R, Phase 1 Profit Lock @ +1.50R, Phase 2 Trailing Lock @ +2.00R). TP extensions into orderbook liquidity vacuums require simultaneous Phase 2 SL profit lock.

