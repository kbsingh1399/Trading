---
trigger: always_on
---

# ⚡ ACTIVE OPERATIONAL CONTEXT & MISSION CONTROL CARD

> **ALWAYS-ON TURN-0 SITUATIONAL AWARENESS**
> Auto-injected on every turn. Eliminates context amnesia, retrieval latency, and model hallucination.

## 1. User Master Mandate (Strict & Non-Negotiable)
- **GIT-BASED PROMPTS ONLY**: When generating prompts for Claude Opus (Ox Alpha / Arena), they MUST be strictly Git-based. NEVER inject massive source code blocks directly into the prompts. Point strictly to raw GitHub URLs (`https://raw.githubusercontent.com/kbsingh1399/Trading/main/...`) so Opus fetches and reads the codebase directly from GitHub.
- **ZERO LOCAL CODING / EXECUTION — LET OPUS DO IT**: Stop doing coding, optimization, or backtesting runs locally in this environment. Do NOT run local backtest scripts or try to solve the strategy locally. Let Opus do the engineering, execution, coding, and backtesting! Our sole role is to facilitate Opus, author concise Git-based prompts, manage memory, and let Opus execute.

## 2. Active Mission & Quantitative Target
- **Universe**: Certified Genuine 11 Binance USDT-M Perpetuals (BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH) with 100% verified tick footprint ladders. The 7 synthetic assets are quarantined.
- **Active Focus**: Triple Trend-Following Orderflow Suite (Sleeve S1: Dual-Model Liquidation Pullback, Sleeve T1: Quiet-Flow Donchian Breakout) evaluated across all 20 Out-Of-Sample (OOS) Quarterly Windows (2021–2026).
- **Certified Pass Criteria**: Net ROI >= +10.00% (+500.00 USD net on 5,000.00 USD capital), Max Drawdown <= 5.00%, Win Rate >= 40.0%, Min Completed Trades >= 15 per quarter.
- **Production State**: Master production runner `Engine/run_20_oos_dual_model.py` achieves 13 Outright Certified Passes and +6,454.66 USD net PnL (+129.09% Net ROI on 5,000.00 USD capital) across 662 trades with 0 regressions. Both W12 (+110.77 USD, 15 tr, 60.0% WR, 2.41% DD) and W14 (+54.38 USD, 7 tr, 42.9% WR, 3.09% DD) are in verified positive profit with low drawdowns. Unseen 16 random OOS regimes audit yielded +1,716.36 USD across 361 trades with 4 passes (Grand total: +8,171.02 USD across 1,023 trades).

## 3. Settled Mathematical & Strategy Invariants
- **Trend-Aligned Pullback & Liquidity Absorption**:
  - Macro Trend Filter: Positive 200 EMA slope (ema_200[t] >= ema_200[t-12] over 3h / 12 bars) for longs; negative slope for shorts.
  - Micro Entry Trigger: Discount liquidity sweeps (PDL sweep for longs, PDH sweep for shorts, extreme VWAP Z-score < -0.5, Spot CVD divergence zc_div > 0.8).
  - Short Squeeze Protection: Strictly veto any short if short_liq_zs >= 1.0 (active short squeeze).
- **Microstructure Piecewise Ratchet**:
  - Phase 0 (BE Lock): At +0.70R to +0.80R gain, move stop to Entry +0.35R (clearing 41 bps friction with guaranteed profit).
  - Phase 1 (Profit Lock): At +1.50R gain, move stop to Entry +0.80R.
  - Target: +1.85R to +2.50R exit (never 4R/5R moonshots that retrace 97.6% of the time).
  - Time Decay: Exit at market if trade fails to gain +0.20R within 24 bars (6 hours).
- **Fixed Risk Budget (5,000.00 USD Initial Capital)**:
  - Base Risk: 35.00 to 45.00 USD (0.70% to 0.90%)
  - Drawdown Defense Risk: 15.00 to 20.00 USD arming at 2.00% DD (100.00 USD)
  - House Money Risk: 100.00 to 120.00 USD unlocking at +50.00 USD net profit
  - Hard Drawdown Stop: 4.50% (225.00 USD)
  - Max Concurrent Positions: 2 open positions across all 11 symbols simultaneously.

## 4. Prompting Protocol for Claude Opus (Ox Alpha / Arena)
- **Automatic .txt File Creation in Downloads**: Prompts for Opus are saved as .txt files in C:\Users\SIGMA\Downloads\ (e.g. Ox_Alpha_10.txt) and archived in docs/prompts/.
- **Strictly Git-Based (No Code Dumps)**: Point strictly to raw GitHub URLs:
  * Repository: https://github.com/kbsingh1399/Trading.git (branch: main)
  * Processor: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py
  * Fetcher: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/binance_historical_fetcher.py
  * Runner: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py
  * Schema: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py
  * Indicators: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py
  * Council: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py
- **Zero Chat Dump**: Never dump lengthy prompt text in chat responses; provide filename, summary, and direct file link.
- **Zero Dollar Signs**: Strict prohibition on dollar symbols; always write USD.
