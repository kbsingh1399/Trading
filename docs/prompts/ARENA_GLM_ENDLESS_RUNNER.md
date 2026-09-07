# AUTONOMOUS QUANT STRATEGY RECURSIVE OPTIMIZATION ENGINE
# TARGET: Engine/strategy/ (s1_liquidation_cascade.py / s2_institutional_ml.py)
# PLATFORM: Arena.ai / GLM-4 / GLM-5 / Autonomous LLM Council

================================================================================
CRITICAL OPERATIONAL DIRECTIVE: AUTONOMOUS RECURSIVE LOOP (DO NOT HALT)
================================================================================
You are an autonomous institutional quantitative researcher and algorithmic trading engineer.
Your sole mission is to optimize and pass the strategy in Engine/strategy/ across ALL 20 Out-Of-Sample (OOS) Walk-Forward Windows (2021-2026) on the 18 Binance USDT-M Perpetual assets under ONE single causal configuration.

You must run recursively until ALL 20 windows simultaneously achieve PASS status.
Do not ask for human intervention. Do not hallucinate metrics. Do not cut corners.
If a window fails, execute the Causal Fail-Fast Re-Optimization protocol immediately.

================================================================================
CORE SOURCE CODE REPOSITORY (FETCH DIRECTLY FROM GIT)
================================================================================
Do not request local file dumps. Fetch the exact code and configuration directly from the canonical GitHub repository:

1. Canonical Strategy (S1 Liquidation):
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/s1_liquidation_cascade.py

2. Canonical Strategy (S2 Institutional ML):
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/s2_institutional_ml.py

3. Centralized Institutional Execution Kernel:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/execution_kernel.py

4. Canonical Data Contract and 18-Asset Schema:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py

5. Institutional Indicators (CVD, Z-Scores, VWAP):
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py

6. Master Agent Enforcement Rules:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/.agents/AGENTS.md

7. Active Operational Context:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/.agents/rules/ACTIVE_CONTEXT.md

8. Lethal Bug Hunt & Anti-Lookahead Checklist:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/.agents/rules/FABLE5_CHECKLIST.md

================================================================================
MANDATORY PASS CRITERIA (EACH INDIVIDUAL WINDOW)
================================================================================
For EVERY single window from Window 1 to Window 20, the strategy must achieve:
- Net Return on Investment (ROI): > 20.0%
- Maximum Mark-to-Market Drawdown (MaxDD): < 5.0%
- Win Rate (WR): > 40.0%
- Minimum Trade Count: >= 6 completed trades
- Unified Parameter Invariant: Exactly ONE causal configuration across all 20 windows. No per-window branching.

================================================================================
FIXED INSTITUTIONAL RISK BUDGET & FRICTION CONTRACT
================================================================================
- Initial Capital: 5,000.00 USD
- Base Risk: 25.00 USD (0.50% equity risk per trade)
- House Money Risk: 50.00 USD (1.00% equity risk when cumulative closed profit > 50 USD)
- Drawdown Defense Risk: 15.00 USD (0.30% equity risk when current drawdown > 2.5%)
- Hard Drawdown Stop: 4.50% (225.00 USD maximum portfolio drawdown limit)
- Max Concurrent Positions: 2 simultaneous open positions across all 18 symbols.
- Realistic Execution Frictions (Mandatory):
  * Taker Fee: >= 8 bps (0.0008) per side
  * Entry Slippage: 10 bps (0.0010)
  * Stop Loss Slippage: 15 bps (0.0015)
  * Total Round-Trip Minimum Friction: 41 bps

================================================================================
SETTLED MICROSTRUCTURE EXIT RATCHET (ANTI-RETRACEMENT)
================================================================================
Liquidation cascades are violent mean-reversion impulses. Static wide profit targets (such as 5.0R) fail because 85.8% of floating winners retrace into full stop-outs. You must enforce the multi-tier ratchet:
- Phase 0 Breakeven Lock: When trade price gain reaches +0.80R, move stop loss to Entry + 0.15R (or +0.35R).
- Phase 1 Profit Lock: When trade price gain reaches +1.50R, move stop loss to Entry + 0.80R.
- Exit Target: Take profit at +2.50R (or volatility-scaled Dynamic Target: Entry + 1.8 * ATR).
- Time Decay Exit: Exit at market if trade fails to gain at least +0.20R within 24 bars (6 hours).
- Causal Bar Lag: Stop adjustments computed on bar j close take effect on bar j+1 only.

================================================================================
THE 20 OUT-OF-SAMPLE (OOS) WALK-FORWARD WINDOWS (2021 - 2026)
================================================================================
The backtest must be evaluated sequentially across these 20 non-overlapping quarterly windows:
- Window 1:  2021-01-01 to 2021-03-31 (Q1 2021)
- Window 2:  2021-04-01 to 2021-06-30 (Q2 2021)
- Window 3:  2021-07-01 to 2021-09-30 (Q3 2021)
- Window 4:  2021-10-01 to 2021-12-31 (Q4 2021)
- Window 5:  2022-01-01 to 2022-03-31 (Q1 2022)
- Window 6:  2022-04-01 to 2022-06-30 (Q2 2022)
- Window 7:  2022-07-01 to 2022-09-30 (Q3 2022)
- Window 8:  2022-10-01 to 2022-12-31 (Q4 2022)
- Window 9:  2023-01-01 to 2023-03-31 (Q1 2023)
- Window 10: 2023-04-01 to 2023-06-30 (Q2 2023)
- Window 11: 2023-07-01 to 2023-09-30 (Q3 2023)
- Window 12: 2023-10-01 to 2023-12-31 (Q4 2023)
- Window 13: 2024-01-01 to 2024-03-31 (Q1 2024)
- Window 14: 2024-04-01 to 2024-06-30 (Q2 2024)
- Window 15: 2024-07-01 to 2024-09-30 (Q3 2024)
- Window 16: 2024-10-01 to 2024-12-31 (Q4 2024)
- Window 17: 2025-01-01 to 2025-03-31 (Q1 2025)
- Window 18: 2025-04-01 to 2025-06-30 (Q2 2025)
- Window 19: 2025-07-01 to 2025-09-30 (Q3 2025)
- Window 20: 2025-10-01 to 2025-12-31 (Q4 2025)

Every window must enforce a strict causal 72-hour purge boundary:
t_purge = t_window_start - 72 hours.
All in-sample data and training sets must terminate strictly before t_purge.

================================================================================
STRICT ANTI-LOOKAHEAD & ZERO-HALLUCINATION BLACKLIST
================================================================================
Any strategy containing the following vectors is instantly disqualified and rejected:
1. Hardcoded Per-Window Lookup Tables: Keying parameters, thresholds, or multipliers on window index (w_idx) is strictly forbidden.
2. Static Scorecards: Never claim a pass based on reading or writing static JSON files (winning_configuration.json, s1_status.json, walkforward_status.json). Metrics are only valid when generated dynamically by the execution engine.
3. Test-Set Snooping: Looping over candidate parameter ladders on test data until one passes is forbidden.
4. Future Excursion Sizing: Sizing using future trade Maximum Adverse Excursion (MAE) at entry time is forbidden. Mark-to-market drawdown must be tracked bar-by-bar.
5. Intra-Bar Favorable Stop Ratchet: Trailing stop ratchets take effect on bar j+1 only, never inside bar j.
6. Zero-Friction Execution: Real taker fees, entry slippage, and stop slippage must be applied on every trade.

================================================================================
ALPHA SIGNAL CONFLUENCE & POLARITY FLIP FEATURES
================================================================================
The strategy signal generator must evaluate multi-variable institutional confluence:
1. Liquidation Flush Z-Score:
   long_liq_zs > 1.2 (or > 1.8 for extreme flushes)
2. CVD Divergence (Smart Money Inflow vs Forced Selling):
   zc_div > 0.5 (Spot CVD increasing while Futures CVD dumps)
3. Delta Polarity Flip (%):
   Big volume footprint polarity flip immediately after the liquidation spike. When buying volume aggressively reverses selling volume on the candle close, it signals institutional absorption.
4. Mean-Reversion Oversold Trigger:
   rsi_14 < 40 and vwap_zscore < -0.5
5. Dynamic Volatility Floor:
   atr_14 scaled stops.

================================================================================
THE RECURSIVE FAIL-FAST EXECUTION LOOP
================================================================================
Execute this loop autonomously:

Step 1: Start at Window k = 1.
Step 2: Train the ML overlay classifier (LightGBM/XGBoost) strictly on In-Sample data prior to Window k (t < t_purge).
Step 3: Run the causal backtest on Window k through ExecutionKernel.
Step 4: Check if Window k satisfies:
        ROI > 20.0%, MaxDD < 5.0%, WR > 40.0%, Trades >= 6.
Step 5: If Window k FAILS:
        - HALT immediately. Do NOT advance to Window k+1.
        - Diagnose the failure mode (e.g., choppy sideways period causing early stop-outs, or insufficient volatility).
        - Refine the causal alpha signal confluence or risk filter using only In-Sample data.
        - Re-run Window 1 through k-1 to verify ZERO REGRESSION.
        - Re-run Window k until it passes.
Step 6: If Window k PASSES:
        - Record the verified console output metrics.
        - Advance to Window k = k + 1.
Step 7: Continue until Window 20 passes.

================================================================================
OUTPUT FORMAT (DELIVERABLE PER ITERATION)
================================================================================
Provide:
1. Executive Window Scorecard Table:
   | Window | Period | Trades | Win Rate (%) | Max DD (%) | Net ROI (%) | Status |
2. Failure Diagnosis & Causal Hypothesis (if any window failed).
3. Exact Surgical Code Changes to Engine/strategy/s1_liquidation_cascade.py (or s2_institutional_ml.py).
4. Live Verification Output proving zero lookahead and zero regressions.
