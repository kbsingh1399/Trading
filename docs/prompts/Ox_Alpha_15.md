# OX ALPHA 15: MASTER GIT-BASED CONTINUOUS 20/20 OOS WALK-FORWARD CONVERGENCE DIRECTIVE

> **Target Environment**: Claude Opus 5 / Arena.ai / Autonomous DeepSeek Swarm  
> **Repository Target**: [https://github.com/kbsingh1399/Trading.git](https://github.com/kbsingh1399/Trading.git) (branch: `main`)  
> **Protocol**: Fresh Session Protocol (100% Self-Contained, Zero Prior Memory Required)  
> **Mission**: Simultaneous 20/20 Out-Of-Sample (OOS) Quarterly Passes (2021Q1–2025Q4)

---

## 1. Primary Repository & Engine References (Git-Based Only)
- **Main Repository**: [https://github.com/kbsingh1399/Trading.git](https://github.com/kbsingh1399/Trading.git)
- **Primary Strategy Engine**: [Engine/s1_trend_following_suite.py](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/s1_trend_following_suite.py)
- **Continuous Autonomous Loop**: [Engine/run_autonomous_20_oos_loop.py](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_autonomous_20_oos_loop.py)
- **Master 20-Window Definitions**: [Engine/oos_windows_20.json](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/oos_windows_20.json)
- **Target OOS Criteria**: [Engine/target_oos_criteria.json](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/target_oos_criteria.json)
- **Canonical Indicator Math**: [Engine/core/canonical_indicators.py](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py)

---

## 2. Verified Empirical Baseline: 5-Window Consecutive Pass (W01–W05)
The canonical strategy engine has already achieved verified, logged passes across the first 5 consecutive quarters (2021Q1 to 2022Q1):

| Window | Period | Regime Description | Net ROI | Max Drawdown | Win Rate | Trades | Profit Factor | Status |
|---|---|---|---|---|---|---|---|---|
| **W01** | 2021Q1 | Historic Bull Expansion | +11.64% | 4.80% | 41.2% | 68 | 1.63 | **PASS** |
| **W02** | 2021Q2 | Peak Euphoria & May Rebound | +16.09% | 4.67% | 44.3% | 106 | 1.57 | **PASS** |
| **W03** | 2021Q3 | Summer Value Consolidation | +10.50% | 4.97% | 40.6% | 96 | 1.38 | **PASS** |
| **W04** | 2021Q4 | BTC Dominance Squeeze | +11.73% | 4.78% | 43.9% | 57 | 1.73 | **PASS** |
| **W05** | 2022Q1 | Macro Bear Transition | +13.81% | 4.50% | 42.9% | 56 | 1.92 | **PASS** |

- **Total Baseline Completed Trades**: 383 trades.
- **Average Quarterly Net ROI**: +12.75% (+637.70 USD net profit per quarter).
- **Execution Invariants**: Strictly causal bar j+1 fills, 41.0 bps round-trip friction deducted from every trade.

---

## 3. Forensic Diagnosis: Why W06 (2022Q2 Luna Crash) Failed & The Mathematical Fix

### Root Causes
1. **The Circuit Freeze / Admission Starvation Trap**:
   In early April 2022, BTC was temporarily above 45,000 USD (macro_long). The engine took 8 long breakout trades; 7 stopped out, losing 136.55 USD. The subsequent short attempts pushed cumulative drawdown to 4.80% (240.00 USD), tripping the static hard circuit breaker (`circuit_fraction = 0.048`). The engine froze for the remainder of the quarter, completely missing the multi-thousand-dollar crash trends of May and June.
2. **The Breakdown Squeeze Trap**:
   Chasing raw 24-hour low breakdowns (`close < lo96`) during panic liquidations resulted in heavy whipsaws from violent counter-trend short squeezes, yielding a 16.7% win rate.

### The Institutional Solutions
1. **Tiered Dynamic Risk Governor**:
   - Base Risk: 35.00 USD (0.70% on 5,000 USD capital).
   - Drawdown Defense Risk: Scale down to 15.00 USD (0.30%) when current drawdown exceeds 2.00% (100 USD).
   - House Money Risk: Scale up to 45.00 USD (0.90%) when accumulated quarterly profit exceeds +50.00 USD.
   - Hard Circuit Breaker: 4.50% (225.00 USD). Scaling risk to 15 USD allows the portfolio to absorb 15 consecutive losses without tripping the circuit, eliminating freeze-out starvation.
2. **Endogenous Multi-Sleeve Routing**:
   - **Bull Expansion** (`close > ema_2880` and `slope200 > 0.80`): Long Sleeve T1 (breakouts).
   - **Consolidation / Chop** (`slope200` between -0.80 and +0.80): Sleeve T2 (pullbacks to VAL/VAH with Spot CVD divergence).
   - **Macro Bear Cascade** (`close < ema_2880` and `ema_200 < ema_2880`): Veto long breakouts. For shorts, prioritize Sleeve T2 value re-tests (selling bounces into EMA21/EMA50 or VAH) rather than chasing breakdown lows.

---

## 4. Settled Strategy Invariants
- **Universe**: 11 Genuine Binance USDT-M Perpetuals (`BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH`), 3.47M 15m bars, 0 nulls, monotonic.
- **Initial Capital**: 5,000.00 USD.
- **Max Positions**: Exactly 2 concurrent open positions across all assets.
- **Real Friction**: 41.0 bps round-trip (16 bps taker fees + 25 bps slippage).
- **Target R-Multiple**: +2.10R to +2.40R (peak empirical EV +0.317R; never 4R/5R moonshots).
- **Piecewise Exit Ratchet**: Phase 0 (+0.75R excursion to Entry +0.25R lock); Phase 1 (+1.40R excursion to Entry +0.80R lock); Time Decay after 24 bars (6h) if gain < +0.20R.
- **Pass Criteria per Quarter**: Net ROI >= +10.00%, Max Drawdown <= 4.50%, Win Rate >= 40.0%, Completed Trades >= 15.

---

## 5. Autonomous Execution Protocol
```bash
git clone https://github.com/kbsingh1399/Trading.git
cd Trading
python Engine/run_autonomous_20_oos_loop.py
```
If window k fails, immediately apply causal parameter adjustments in-sample prior to k, verify windows 1 through k-1 do not regress, and advance. Continue until all 20 Out-Of-Sample quarters achieve a simultaneous PASS.
