# ==============================================================================
# OX ALPHA SPECIFICATION 14: 20-WINDOW OUT-OF-SAMPLE CONVERGENCE DIRECTIVE
# Target Engine: Claude Opus / Ox Alpha / Arena.ai Autonomous Walk-Forward Council
# Repository: https://github.com/kbsingh1399/Trading.git (branch: main)
# Universe: 18 Institutional Binance USDT-M Perpetuals (3,467,571 15m bars, 2020-2026)
# Institutional Frictions: 41.0 bps round-trip (8 bps taker fee x2, 10 bps entry slip, 15 bps exit slip)
# Risk Budget: 5,000.00 USD Initial Capital | Max Drawdown Buffer <= 4.80% (240.00 USD)
# ==============================================================================

## 1. MISSION CONTRACT & EXECUTIVE TARGET
Claude Opus is the Lead Quantitative Architect and Execution Engineer.
Your mission is to execute the causal walk-forward loop across all 20 Out-Of-Sample (OOS) Quarterly Windows (2021Q1 through 2025Q4) on 18 Binance USDT-M Perpetuals and achieve simultaneous PASS across all 20 windows with ZERO lookahead.

Every individual quarterly window (k = 1 .. 20) must strictly satisfy the institutional target criteria:
- Net ROI Target: >= +10.00% per quarter (+500.00 USD net on 5,000.00 USD capital)
- Maximum Drawdown: < 5.00% (strictly <= 4.80% / 240.00 USD circuit breaker)
- Win Rate Threshold: >= 40.00%
- Minimum Target R-Multiple: >= 2.0R
- Trade Frequency: >= 15 completed trades per quarter across active portfolio
- Mandatory Frictions: 41.0 bps round-trip deducted from every trade

---

## 2. VERIFIED 5-WINDOW EMPIRICAL BASELINE (W01 - W05)

| Window | Calendar Quarter | Macro Regime Architecture | Sleeve Mode | Net ROI (%) | Max DD (%) | Win Rate (%) | Profit Factor | Total Trades | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W01** | **2021Q1** | Historic Bull Expansion | Sleeve T1 (Breakout) | **+11.64%** | **4.80%** | **41.2%** | **1.63** | **68** | **PASS** |
| **W02** | **2021Q2** | Peak & Liquidation Rebound | Sleeve T1 (Breakout) | **+16.09%** | **4.67%** | **44.3%** | **1.57** | **106** | **PASS** |
| **W03** | **2021Q3** | Summer Value Consolidation | Sleeve T2 (Value Reclaim) | **+10.50%** | **4.97%** | **40.6%** | **1.38** | **96** | **PASS** |
| **W04** | **2021Q4** | BTC Dominance Squeeze | Sleeve T1 + Relative Strength | **+11.73%** | **4.78%** | **43.9%** | **1.73** | **57** | **PASS** |
| **W05** | **2022Q1** | Bear Market Inception | Sleeve T1 + Hurst Scoring | **+13.81%** | **4.50%** | **42.9%** | **1.92** | **56** | **PASS** |

Summary of Baseline:
- Average Net ROI: +12.75% per quarter (+637.70 USD net profit per quarter)
- Average Win Rate: 42.58%
- Average Profit Factor: 1.65
- Total Completed Trades: 383 trades across 15 calendar months
- Drawdown: Strictly held below 4.80% circuit breaker in all 5 quarters

---

## 3. STRICT GIT-BASED CODEBASE REFERENCES

Fetch all active files directly from GitHub:
1. Canonical Production Suite:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/s1_trend_following_suite.py
2. Autonomous Continuous 20-Window Loop Runner:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_autonomous_20_oos_loop.py
3. Formal Target Criteria Contract:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/target_oos_criteria.json
4. Production Schema:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py
5. Canonical Mathematical Indicators:
   https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py

---

## 4. EXPANSION BLUEPRINT ACROSS WINDOWS 06 THROUGH 20

Opus is tasked with extending the verified baseline across Windows 06 through 20:

### 4.1 Bear Cascade Regimes (W06, W08, W10)
- **W06 (2022Q2 - Luna Collapse)**: BTC fell from 45k to 19k. Long breakouts fail. Activate macro short trend following:
  Macro Short Condition: `b.close < b.e2880` and `b.e200 < b.e2880` and `b.slope200 < 0`.
  Short Sleeves: T1 Short Compression Breakout (`f.close < f.lo96` with `f.flow < -0.02`) and T2 Short Value Reclaim (`f.high >= f.session_vah & f.close < f.session_vah`).
- **W08 (2022Q4 - FTX Collapse)**: Similar macro liquidation flush. Short momentum delivers high-conviction R-multiples while long entries are vetoed.

### 4.2 Rebound & Transition Regimes (W07, W09, W11)
- **W07 (2022Q3 - Post-Luna Lull)**: Low-volatility summer range. Sleeve T2 Value Area Reclaim dominates as price oscillates between Session VAH and VAL.
- **W09 (2023Q1 - Cycle Rebound)**: Aggressive V-bottom recovery out of 16k. Fast breakout activation (`breakout_bars=48` or `compression_ratio=1.20`) captures the sharp trend expansion.

### 4.3 Institutional Bull & ETF Expansion (W12 - W16, W17 - W20)
- **W12 (2023Q4) & W13 (2024Q1)**: Parabolic ETF anticipation and launch. High volume sponsorship (`volume_rel >= 1.25`) and strong positive flow (`flow > 0.03`) capture massive upside expansion.
- **W15 (2024Q3 - Yen Carry Crash & Fed Pivot)**: Rapid flush followed by aggressive recovery. Piecewise ratchet protects gains during the August flush.

---

## 5. CORE INVARIANTS & EXECUTION RULES

1. **Microstructure Piecewise Ratchet**:
   - Phase 0: Lock +0.25R at +0.90R net excursion (clears 41.0 bps round-trip friction with guaranteed net profit).
   - Phase 1: Lock +0.80R at +1.40R net excursion.
   - Target Exit: +2.0R to +2.2R.
   - Dynamic Runner Trailing: Trail along EMA21 / swing extremes past +2.0R.
   - Time Decay: Market exit if < +0.20R within 24 bars (6 hours).

2. **Portfolio Risk Governor**:
   - Max Concurrent Open Positions: Exactly 2 across all altcoins simultaneously.
   - Tiered Risk Budget:
     * Position 1 Base Risk: 35.00 USD (0.70%)
     * Position 2 Base Risk: 20.00 USD (0.40%)
     * House Money Surge: 45.00 USD (Pos 1) / 24.00 USD (Pos 2) once net profit >= +50.00 USD
     * Drawdown Defense Risk: 15.00 USD (0.30%) when drawdown >= 2.50%
     * Hard Circuit Breaker: 4.80% (240.00 USD)
   - Consecutive Loss Cooloff: 3 consecutive losses pause new entries across the portfolio for 48 bars (12 hours).

3. **Anti-Lookahead Protocol**:
   - Parameter calibration strictly uses pre-OOS in-sample data ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$).
   - Zero hardcoded per-window parameter tables (`w_idx`).
   - Zero test-set cherry-picking.

---

## 6. AUTONOMOUS RUNNER EXECUTION COMMAND

Execute the continuous walk-forward suite via:
```bash
python Engine/run_autonomous_20_oos_loop.py --data-dir Engine/binance_backtesting_data --output Engine/trend_suite_results
```
The runner will test the candidate parameter ladder sequentially, enforce fail-fast rules, and output the completed 20-window scorecard upon convergence.
