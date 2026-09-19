# Plan: Unified 3-Basket Crypto, Forex & CFD Architecture

## 1. Goal & Scope
Incorporate MT5 crypto perpetual/CFD pairs directly into the institutional pipeline alongside Forex and CFD/Commodity assets.
Establish three decoupled baskets:
- **Crypto Basket:** `BTCUSD`, `ETHUSD`, `SOLUSD`, `XRPUSD`, `BNBUSD`, `LTCUSD`, `ADAUSD`, `DOTUSD`, `BCHUSD`
- **Forex Basket:** `EURUSD`, `NZDUSD`, `AUDCHF`, `EURHUF`, `USDSEK`, `EURSEK`, `USDHKD`, `EURCNH`, `NZDCNH`
- **CFD Basket (Indices & Commodities):** `GER40`, `AU200`, `FR40`, `US2000`, `GAS`, `NICKEL`, `LEAD`, `XAUCNH`, `GAUCNH`

For each basket, implement an automated dynamic ranking selector (`asset_selector.py`) that filters for the top performing assets (based on rolling win rate, Sharpe/Calmar, and net profit factor) to allocate active trading capital.

## 2. Architecture & Pipeline Changes
1. **MT5 Crypto Data Exporter (`Engine/pipeline/export_mt5_crypto.py`):**
   - Export historical `15m`, `1h`, `4h`, and `D1` candles directly from MT5 into `Forex_Backtesting_Data/`.
   - Ensure ICT session features (`day_of_week`, `session`, `is_kill_zone`) are precomputed with zero lookahead.
   - Atomic parquet writes with zstd compression.

2. **Unified Baskets Definition (`Engine/core/schema.py`):**
   - Add `ASSET_BASKETS = {"Crypto": [...], "Forex": [...], "CFD": [...]}`.
   - Map broker raw symbols (`.pi`, `.p`) to clean canonical symbols.

3. **Dynamic Asset Selector (`Engine/core/asset_selector.py`):**
   - Load recent window metrics / OOS performance.
   - Rank assets within each basket.
   - Expose `get_top_assets(basket_name, top_n)` and `get_active_multiverse_universe()`.

4. **Live & Backtest Integration:**
   - Integrate with `Engine/live/run_forex_dry_run.py` and `Engine/forex_engine.py`.

5. **Verification & Testing (`Engine/tests/test_baskets_and_crypto.py`):**
   - Verify crypto parquet existence, schema conformance, no nulls, monotonic timestamps.
   - Test basket ranking logic and fallback behavior.
   - Ensure zero regressions on existing 18 canonical assets.
