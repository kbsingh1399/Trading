# Live Terminal Pipeline Upgrade Plan: 23-OOS Elite Multi-Sleeve Suite Integration

## 1. Task Objective
Upgrade `Engine/runners/run_live_terminal.py` from a basic single-asset terminal monitor wrapper into the master operational execution and monitoring runner for the entire 23-OOS elite quant pipeline (`Engine/runners/run_23_oos_altcoin_suite.py`), unifying multi-asset signal scanning (11 core Binance USDT-M perpetuals), dynamic institutional risk budgeting, `BinanceBroker` execution bridge, and live BTC buy-and-hold benchmark tracking.

---

## 2. Multi-Agent Orchestration Team
| Agent Persona | Focus Area | Mandate |
|---|---|---|
| **Project Planner & Quant Architect** | Pipeline & Alpha Architecture | Align signal calculation and causal next-bar open execution with `run_23_oos_altcoin_suite.py` across S1, S2, S3, S4, and T1 sleeves. |
| **Senior Execution Engineer** | Broker Gateway & Risk Governance | Wire up `BinanceBroker` (dry-run & live REST execution), place-then-cancel trailing ratchets, native stops, and dynamic institutional risk scaling. |
| **QA & Verification Engineer** | Pre-Flight & Test Automation | Validate headless `--once` execution, CLI flag parity, parquet integrity checks, and error-handling resilience. |

---

## 3. Detailed Component Architecture

### A. Core Universe & Pre-Flight Sync
- **11 Core Institutional Assets**: `BTCUSDT, ETHUSDT, XRPUSDT, BNBUSDT, DOGEUSDT, ADAUSDT, TRXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, BCHUSDT`.
- **Pre-Flight Parquet Gap Verification**: Scans datasets in `binance_backtesting_data/`, checks for data freshness within 24 hours, and triggers `run_pipeline()` if missing or stale bars are detected.

### B. Multi-Sleeve Alpha Signal Engine
- **S1 (Liquidity Pullbacks)**: Discount sweeps (PDL/PDH), VWAP Z-score < -0.5, Spot CVD divergence > 0.8.
- **S2 (Bollinger Mean Reversion)**: 96-bar BB, 2.0 std, filtered by `zbw <= 1.85` and `adx <= 32.0`, RSI < 32 (long) / RSI > 68 (short) with EMA 200 trend guard.
- **S3 (Cross-Asset ORB/CRT)**: London (09:00 UTC) and New York (13:30 UTC) session opening range breakouts.
- **S4 (Kairi Disparity)**: 20-period Kairi Z-score (`zkri_20 < -1.75` for longs, `zkri_20 > 1.75` for shorts with EMA 200 trend guard).
- **T1 (Donchian Breakouts)**: 10d/15d channel breakouts with Spot CVD volume confirmation and Squeeze Momentum gating.

### C. Institutional Dynamic Risk Governor
- **Base Capital**: 5,000.00 USD.
- **Concurrency**: Maximum 4 simultaneous positions across all symbols (max 2 S1, max 1 T1, max 2 S2/S4, max 2 ORB).
- **Dynamic Risk Sizing**:
  - Base Risk: 24.00 USD (0.48% on 5,000 USD).
  - DD Defense Mode: When DD >= 1.0% or equity < capital, scale risk down to 6.00 USD.
  - House Money Mode: When cumulative profit >= 150.00 USD, scale risk to 26.00 USD.
  - Milestone Profit Lock: When profit >= 500.00 USD with >= 15 trades, lock in floor stop at `max(capital + 500, peak_equity - 120)`.
  - Circuit Breaker: 4.85% max drawdown ceiling.

### D. BinanceBroker Execution Bridge
- **Dual Mode**:
  - `--dry-run`: Default paper trading mode with realistic balance, margin, and order fills.
  - `--live`: Real orders placed on Binance USDT-M Futures via `https://fapi.binance.com` using HMAC-SHA256 authentication.
- **Execution & Ratchet Mechanics**:
  - Causal next-bar open fill simulation with 10 bps slippage.
  - Native exchange `STOP_MARKET` conditional orders (`workingType=MARK_PRICE`, `closePosition=true`).
  - Place-Then-Cancel zero-naked-window trailing ratchet (`modify_sltp`).
  - Automatic emergency market exit if stop order placement fails 3 retries.

### E. Rich Terminal Dashboard & Benchmark Tracker
- **Header**: Live BTC price, macro regime (`BULL_EXPANSION`, `BEAR_CONTAGION`, `CHOP`), portfolio equity, open PnL, current drawdown, active risk tier.
- **Signal Matrix**: 11 symbols showing price, RSI, ATR, BB Width Z, KRI Z, ADX, Spot CVD, and active sleeve signals.
- **Active Positions Table**: Symbol, sleeve, entry price, current price, stop loss level, ratchet stage, unrealized PnL, duration.
- **Benchmark Alpha**: Strategy Equity vs BTC Buy & Hold comparison.
- **Headless Mode**: `--once` flag for automated CI test passes.

---

## 4. Verification & Testing Plan
1. `python -m py_compile Engine/runners/run_live_terminal.py` -> 0 syntax errors.
2. `python Engine/runners/run_live_terminal.py --help` -> Clean CLI help menu.
3. `python Engine/runners/run_live_terminal.py --once --dry-run --skip-sync` -> Headless single-pass scan across all 11 core symbols, signal evaluation across all 5 sleeves, and portfolio rendering with exit code 0.
