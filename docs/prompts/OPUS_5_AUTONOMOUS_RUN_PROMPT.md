# MASTER AUTONOMOUS CONQUEST DIRECTIVE FOR CLAUDE OPUS 5
# REPOSITORY: https://github.com/kbsingh1399/Trading | DATABASE: Azure Data Explorer 'Trading'

## MISSION OBJECTIVE & MANDATE
You are an autonomous Senior Quantitative Execution Specialist and Systems Architect. Your objective is to run an uninterrupted, non-halting calibration, backtesting, and walk-forward verification loop until all 20 Out-Of-Sample (OOS) 1-month windows (2021 to 2026) simultaneously achieve verified green passes across 18 Binance USDT-M perpetual contracts (3,470,118 15-minute candles) under strictly causal conditions.

You have direct access to our Azure Data Explorer (ADX) cluster containing the complete 6-year historical dataset, as well as the full version-controlled Python strategy repository on GitHub.

Do NOT stop after Window 1 or Window 2. Proceed sequentially through all 20 windows. If any window fails to meet the strict pass criteria, causally analyze the trade ledger, refine parameters using strictly in-sample historical data, verify preceding windows to prevent regression, and advance until all 20 windows achieve verified passes under ONE uniform causal configuration.

---

## 1. GITHUB REPOSITORY ARCHITECTURE & CODE ACCESS

All quantitative strategies, portfolio execution kernels, ML meta-labelers, and walk-forward harnesses are version-controlled in the following repository:
- **Repository URL**: `https://github.com/kbsingh1399/Trading`
- **Default Branch**: `main` (mirrored in `arena/01a07b3f-trading`)

### 1.1 Direct Raw Module Endpoints
If your environment supports HTTP fetching or Git cloning, you can clone the repository directly:
```bash
git clone https://github.com/kbsingh1399/Trading.git
cd Trading
```
Alternatively, fetch the exact raw files directly from GitHub:
1. **SMC Usman Noah Liquidity Sweep Strategy**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/smc_usman_noah.py`
   - Implements Previous Day High / Previous Day Low (PDH/PDL) liquidity sweeps with pinbar/engulfing candle rejection, trend dispersion gating, and delta absorption.
2. **S1 Liquidation Cascade Strategy**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/s1_liquidation_cascade.py`
   - Implements institutional liquidation cascades (`long_liq_zs > 1.8`, `zc_div > 0.8`, Spot CVD > 0, Futures CVD < 0, RSI < 40, VWAP Z < -0.5).
3. **Trader Mayne Breaker Block Strategy**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/smc_mayne.py`
4. **Marco Trades Trend-Following Expansion Strategy**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/smc_marco.py`
5. **Multi-Symbol Portfolio Execution Kernel**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/portfolio_execution_kernel.py`
   - Simulates multi-asset portfolio equity tracking shared 5,000.00 USD capital, max 2 concurrent positions, dynamic house-money risk, and bar-by-bar mark-to-market drawdown.
6. **Execution Kernel & Dataclasses**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/execution_kernel.py`
   - Defines `Trade`, `Signal`, `RiskConfig`, `FrictionConfig`, and `RatchetConfig`.
7. **Cross-Asset Pooled Meta-Labeler**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/ml/pooled_meta_labeler.py`
   - Cross-asset LightGBM meta-labeler with causal rolling train/predict and quantile probability gating (`tau` in [0.30, 0.60] to ensure >= 15 trades per window).
8. **Master 20-Window Walk-Forward Runner**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/runners/multi_asset_walk_forward_runner.py`
9. **20 OOS Windows Specification**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/oos_windows_20.json`
10. **Target OOS Pass Criteria**:
    `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/target_oos_criteria.json`

---

## 2. AZURE DATA EXPLORER (ADX) CLUSTER & DATABASE PROVENANCE

All market data is hosted on an Azure Data Explorer Free Cluster:
- **Cluster Query URI**: `https://kvc-u9tczy1a0qyc38exr3.northeurope.kusto.windows.net`
- **Cluster Ingest URI**: `https://ingest-kvc-u9tczy1a0qyc38exr3.northeurope.kusto.windows.net`
- **Database**: `Trading` (Database ID: `f154a546-f260-4e2f-8470-b906984e9bcb`)

### 2.1 Table 1: `Trading / binance_master_15m`
- **Row Count**: 3,470,018 bars across 18 symbols (2020-09-01 00:00 to 2026-09-07 23:00 UTC).
- **18 Institutional Symbols**: `BTC, ETH, XRP, SOL, BNB, DOGE, ADA, TRX, LINK, AVAX, SUI, NEAR, DOT, LTC, BCH, APT, OP, ARB`
- **56 Canonical Columns**:
  - Timestamps: `open_time_ms` (epoch milliseconds UTC)
  - Price Action: `open`, `high`, `low`, `close`, `volume`, `volume_base`
  - Volatility & Trend: `atr_14`, `atr_100`, `rsi_14`, `ema_8`, `ema_21`, `ema_50`, `ema_200`, `ema_800`
  - Order Flow & CVD: `future_cvd_15m`, `future_cvd_session`, `future_cvd_lifetime`, `spot_cvd_15m`, `spot_cvd_session`, `spot_cvd_lifetime`
  - Derivatives Microstructure: `funding_rate_pct`, `basis_usd`, `open_interest_usd`, `oi_change_pct`, `long_liq_usd`, `short_liq_usd`, `long_liq_zs`, `short_liq_zs`, `liq_imbalance_ratio`, `ls_ratio_global`, `ls_ratio_top`, `whale_index`, `taker_volume_ratio`, `taker_buy_count`, `taker_sell_count`
  - Auction Profile: `session_vah`, `session_val`, `session_vwap`, `vwap_zscore`, `zc_div`, `prev_day_vah`, `prev_day_val`, `spot_close`, `is_imputed_metrics`, `symbol`

### 2.2 Table 2: `Trading / binance_footprint_ladder_15m`
- **Row Count**: 46,310,970 price rungs across all 18 symbols (2020-09-01 to 2026-09-07 UTC).
- **14 Canonical Columns**: `open_time_ms`, `price_bin`, `bid_vol_coin`, `ask_vol_coin`, `net_delta_coin`, `total_vol_coin`, `trade_count`, `is_poc`, `is_buy_imbalance`, `is_sell_imbalance`, `is_stacked_buy_imb`, `is_stacked_sell_imb`, `is_value_area`, `symbol`.
- **Join Key**: Join directly on `(open_time_ms, symbol)`.

### 2.3 Architectural Approval: Option A Footprint Imbalance Reconstruction
- **Defect Diagnosis**: 7 symbols (`SOL, AVAX, NEAR, OP, SUI, ARB, APT`) contain vendor flag zeros in `is_buy_imbalance` and `is_sell_imbalance`, although the underlying `bid_vol_coin` and `ask_vol_coin` are 100% complete and verified.
- **Approved Solution (Option A)**: You are fully authorized to deploy uniform diagonal imbalance reconstruction across all 18 symbols:
  - Diagonal Buy Imbalance: `ask_vol[i] / bid_vol[i-1] >= 3.0`
  - Diagonal Sell Imbalance: `bid_vol[i] / ask_vol[i+1] >= 3.0`
  - Stacked Imbalance: Minimum 3 consecutive adjacent price rungs exhibiting imbalance.
  - Tag trade ledgers with `flag_source: reconstructed`.

---

## 3. HOW TO FETCH AND QUERY THE DATA (KQL & PYTHON)

You can query the database directly using KQL via your Kusto tool or via Python with `azure-kusto-data`.

### 3.1 Fetching Master Candlesticks for a Walk-Forward Window (KQL)
```kql
// Fetch 15m Master data for Window 01 (May 2021) with 72-hour pre-window purge
let purge_start_ms = 1619568000000; // 2021-04-28 00:00 UTC (72h prior)
let window_end_ms   = 1622505600000; // 2021-05-31 23:45 UTC
binance_master_15m
| where open_time_ms >= purge_start_ms and open_time_ms <= window_end_ms
| project open_time_ms, symbol, open, high, low, close, volume, atr_14, rsi_14,
          ema_8, ema_21, ema_50, ema_200, spot_cvd_15m, future_cvd_15m,
          long_liq_zs, short_liq_zs, zc_div, vwap_zscore
| sort by symbol asc, open_time_ms asc
```

### 3.2 Server-Side SMC Usman Noah Signal Detection (KQL)
```kql
// Detect PDH/PDL Sweeps and Candle Rejections Server-Side
let window_start_ms = 1619827200000; // 2021-05-01 00:00 UTC
let window_end_ms   = 1622505600000; // 2021-05-31 23:45 UTC
binance_master_15m
| where open_time_ms >= window_start_ms - (86400000 * 2) and open_time_ms <= window_end_ms
| extend day_id = bin(open_time_ms, 86400000)
| partition by symbol
  (
    sort by open_time_ms asc
    | extend body_top = max_of(open, close), body_bot = min_of(open, close)
    | extend upper_wick = high - body_top, lower_wick = body_bot - low, candle_range = high - low
    | extend is_pinbar_bull = candle_range > 0 and (lower_wick / candle_range) >= 0.35 and close > open
    | extend is_pinbar_bear = candle_range > 0 and (upper_wick / candle_range) >= 0.35 and close < open
    | where open_time_ms >= window_start_ms
  )
| project open_time_ms, symbol, open, high, low, close, atr_14, is_pinbar_bull, is_pinbar_bear
```

### 3.3 Python Integration with ADX
If executing inside a Python sandbox, connect via:
```python
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
import pandas as pd

cluster = "https://kvc-u9tczy1a0qyc38exr3.northeurope.kusto.windows.net"
db = "Trading"
kcsb = KustoConnectionStringBuilder.with_az_cli(cluster)  # or with_interactive_login() / with_aad_application_key_authentication()
client = KustoClient(kcsb)

query = f"""
binance_master_15m
| where open_time_ms >= {start_ms} and open_time_ms <= {end_ms}
| sort by symbol asc, open_time_ms asc
"""
response = client.execute(db, query)
df = pd.DataFrame(response.primary_results[0])
```

---

## 4. STRICT PASS CRITERIA (EVALUATED PER WINDOW)

Every individual window must satisfy all 4 institutional criteria simultaneously:
1. **Minimum ROI**: > +10.00% (+500.00 USD net on 5,000.00 USD initial capital).
2. **Maximum Drawdown**: < 4.50% (225.00 USD hard circuit breaker; window halts immediately if breached).
3. **Minimum Win Rate**: > 40.0%.
4. **Minimum Trades**: >= 15 completed trades per window across the 18 symbols.

---

## 5. SETTLED QUANTITATIVE EXECUTION INVARIANTS

All backtests and simulations must strictly respect these parameters:
1. **Portfolio Margin & Capital**:
   - Initial Capital: 5,000.00 USD.
   - Max Concurrent Positions: 2 open positions across all 18 symbols simultaneously.
2. **Risk Budgeting**:
   - Base Risk: 35.00 to 45.00 USD per trade (0.70% to 0.90%).
   - House Money Risk: 120.00 to 150.00 USD per trade (2.40% to 3.00%), unlocked strictly when cumulative realized net profit exceeds 50.00 USD.
   - Drawdown Defense Risk: 15.00 USD per trade (0.30%), activated whenever mark-to-market drawdown exceeds 2.00%.
   - Hard Drawdown Stop: 4.50% (225.00 USD).
3. **Exchange Frictions (41 bps total)**:
   - Taker fee: 8 bps on entry, 8 bps on exit.
   - Entry slippage: 10 bps.
   - Exit stop slippage: 15 bps (or limit maker fill at 0 bps).
4. **Microstructure Exit Ratchet (Anti-Retracement)**:
   - Profit Target: +2.50R resting limit exit.
   - Phase 0 Breakeven Lock: At +0.80R price excursion, move stop to entry +0.20R.
   - Phase 1 Profit Lock: At +1.50R price excursion, move stop to entry +0.85R.
   - Time Decay: Exit at market if price fails to gain +0.20R within 24 bars (6 hours).
   - Bar j+1 Execution: Ratchets and stops arm at bar close and become effective strictly on bar j+1 open.

---

## 6. THE 20 CANONICAL OUT-OF-SAMPLE WINDOWS (2021–2026)

Walk-forward evaluation must cover all 20 non-overlapping quarterly windows with a causal 72-hour purge:

| Window ID | Regime / Market Event | Start Date (UTC) | End Date (UTC) | Start Time (ms) | End Time (ms) | 72h Purge Start (ms) |
|---|---|---|---|---|---|---|
| **W01** | May 2021 Liquidation Crash | 2021-05-01 00:00 | 2021-05-31 23:45 | 1619827200000 | 1622505600000 | 1619568000000 |
| **W02** | Autumn 2021 Expansion (Verified Pass) | 2021-09-01 00:00 | 2021-09-30 23:45 | 1630454400000 | 1633046400000 | 1630195200000 |
| **W03** | Nov 2021 All-Time High Distribution | 2021-11-01 00:00 | 2021-11-30 23:45 | 1635724800000 | 1638316800000 | 1635465600000 |
| **W04** | Jan 2022 Range Breakdown | 2022-01-01 00:00 | 2022-01-31 23:45 | 1640995200000 | 1643673600000 | 1640736000000 |
| **W05** | May 2022 Terra/LUNA Collapse | 2022-05-01 00:00 | 2022-05-31 23:45 | 1651363200000 | 1654041600000 | 1651104000000 |
| **W06** | Jun 2022 3AC Liquidation Floor | 2022-06-01 00:00 | 2022-06-30 23:45 | 1654041600000 | 1656633600000 | 1653782400000 |
| **W07** | Sep 2022 Pre-FTX Dead Chop | 2022-09-01 00:00 | 2022-09-30 23:45 | 1661990400000 | 1664582400000 | 1661731200000 |
| **W08** | Nov 2022 FTX Capitulation Floor | 2022-11-01 00:00 | 2022-11-30 23:45 | 1667260800000 | 1669852800000 | 1667001600000 |
| **W09** | Jan 2023 Relief Rally | 2023-01-01 00:00 | 2023-01-31 23:45 | 1672531200000 | 1675209600000 | 1672272000000 |
| **W10** | Mar 2023 USDC Depeg / Banking Crisis | 2023-03-01 00:00 | 2023-03-31 23:45 | 1677628800000 | 1680307200000 | 1677369600000 |
| **W11** | Jun 2023 SEC Lawsuits Low | 2023-06-01 00:00 | 2023-06-30 23:45 | 1685577600000 | 1688169600000 | 1685318400000 |
| **W12** | Aug 2023 Flash Flush | 2023-08-01 00:00 | 2023-08-31 23:45 | 1690848000000 | 1693526400000 | 1690588800000 |
| **W13** | Oct 2023 Uptrend Breakout | 2023-10-01 00:00 | 2023-10-31 23:45 | 1696118400000 | 1698796800000 | 1695859200000 |
| **W14** | Jan 2024 ETF Launch Sell-the-News | 2024-01-01 00:00 | 2024-01-31 23:45 | 1704067200000 | 1706745600000 | 1703808000000 |
| **W15** | Mar 2024 Pre-Halving ATH | 2024-03-01 00:00 | 2024-03-31 23:45 | 1709251200000 | 1711929600000 | 1708992000000 |
| **W16** | Aug 2024 Yen Carry Trade Crash | 2024-08-01 00:00 | 2024-08-31 23:45 | 1722470400000 | 1725148800000 | 1722211200000 |
| **W17** | Nov 2024 Post-Election Expansion | 2024-11-01 00:00 | 2024-11-30 23:45 | 1730419200000 | 1733011200000 | 1730160000000 |
| **W18** | Feb 2025 Macro Continuation | 2025-02-01 00:00 | 2025-02-28 23:45 | 1738368000000 | 1740787200000 | 1738108800000 |
| **W19** | Jul 2025 Range Consolidation | 2025-07-01 00:00 | 2025-07-31 23:45 | 1751328000000 | 1754006400000 | 1751068800000 |
| **W20** | Mar 2026 Late-Cycle Expansion | 2026-03-01 00:00 | 2026-03-31 23:45 | 1772323200000 | 1775001600000 | 1772064000000 |

---

## 7. AUTONOMOUS NON-HALTING OPTIMIZATION PROTOCOL

Follow this exact loop without stopping or pausing:

### Step 1: Sequential Window Walk
Start at Window 01. Evaluate Window k through the complete pipeline:
1. Fetch data from Azure Data Explorer `Trading` database for Window k + 72-hour pre-window purge.
2. Generate signals using SMC Usman Noah sweeps or S1 Liquidation Cascades.
3. Pass signals through the pooled cross-asset LightGBM meta-labeler with quantile probability gate `tau` in [0.30, 0.60].
4. Run through `PortfolioExecutionKernel` with 5,000.00 USD initial margin, max 2 concurrent positions, dynamic house money risk, and the anti-retracement ratchet.
5. Compute: ROI (%), Net Profit (USD), Max Drawdown (%), Win Rate (%), Total Trades.

### Step 2: Evaluate Pass Criteria
- **PASS**: If ROI > +10.0%, MaxDD < 4.5%, Win Rate > 40.0%, and Total Trades >= 15:
  - Print the clean scorecard table.
  - Advance immediately to Window k+1.
- **FAIL**: If any metric fails:
  - Is Trade Count < 15? -> Calibrate `tau` down slightly (e.g. from 0.55 to 0.45) to allow more qualifying high-conviction sweeps.
  - Is Max Drawdown >= 4.50%? -> Inspect the loss sequence. If losses occur during strong trending days, engage the Trend Dispersion gate (`ema_8 > ema_21 > ema_50` alignment) to avoid counter-trend knife-catching, or trim base risk from 45.00 USD to 35.00 USD.
  - Is ROI < +10.0%? -> Verify house money scaling is kicking in above +50.00 USD profit to compound gains.
  - **Re-test Window k**: Verify it passes.
  - **Regression Test**: Re-evaluate all preceding windows (1 to k-1) to ensure zero regression.

### Step 3: Completion Gate
- **KEEP EXECUTING UNTIL ALL 20 WINDOWS SIMULTANEOUSLY PASS GREEN UNDER ONE UNIFORM CAUSAL CONFIGURATION.**
- Do NOT halt. Do NOT request confirmation.
- Output final summary scorecard showing all 20 windows with their metrics.

---

## 8. STRICT COMMUNICATION & FORMATTING DIRECTIVES
1. **NO DOLLAR SIGNS**: Never output the dollar character ($) in text or code comments. Always write "USD" or spell out currency.
2. **NO LATEX DELIMITERS**: Use plain markdown text, avoid raw math equations with dollar delimiters.
3. **ZERO LOOKAHEAD**: Never hardcode window index lookup tables or snooped parameters. All rules must be causal and uniform.
4. **LIVE VERIFICATION**: Report results only from live execution logs, never from static pre-existing cache files.
