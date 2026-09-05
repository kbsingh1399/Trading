# ARENA.AI MASTER PROMPT: ARCHITECTURAL REBUILD OF THE BINANCE 15M HISTORICAL DATA PIPELINE

> **EXECUTIVE OBJECTIVE**: Rebuild the master production historical data ingestion and indicator processing pipeline (`run_historical_pipeline.py` and its underlying modules) from first principles. Deliver a robust, 100% causal, zero-lookahead, institutional-grade dual-table Parquet generation engine across all 18 Binance USDT-M Perpetuals (2020 -> 2026), complete with automated multi-agent verification checks.

---

## 1. REPOSITORY & ARCHITECTURE CONTEXT

- **Repository**: [https://github.com/kbsingh1399/Engine_1_arena_PR](https://github.com/kbsingh1399/Engine_1_arena_PR) (Branch: `main`)
- **Reference Pipeline Implementation**:
  - Main Orchestrator: [`Engine_2/run_historical_pipeline.py`](https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine_2/run_historical_pipeline.py)
  - Historical Fetcher: [`Engine_2/pipeline/binance_historical_fetcher.py`](https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine_2/pipeline/binance_historical_fetcher.py)
  - Metrics Processor: [`Engine_2/pipeline/historical_metrics_processor.py`](https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine_2/pipeline/historical_metrics_processor.py)
  - Footprint Fetcher: [`Engine_2/pipeline/tick_footprint_fetcher.py`](https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine_2/pipeline/tick_footprint_fetcher.py)
  - Parquet Exporter: [`Engine_2/pipeline/parquet_exporter.py`](https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine_2/pipeline/parquet_exporter.py)
  - Parquet Integrity Verifier: [`Engine_2/verification/verify_parquet_integrity.py`](https://raw.githubusercontent.com/kbsingh1399/Engine_1_arena_PR/main/Engine_2/verification/verify_parquet_integrity.py)

---

## 2. THE 18-ASSET INSTITUTIONAL UNIVERSE
The rebuilt pipeline must ingest, align, compute, and verify the continuous 15-minute history across all 18 institutional perpetual contracts:
```python
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT", 
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT", 
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT", 
    "APTUSDT", "OPUSDT", "ARBUSDT"
]
```
- **Timeline Coverage**: 2020-09-01 (or asset listing date) through 2026-present.
- **Bar Interval**: 15 minutes (strictly 900,000 ms monotonic step, zero missing bars, zero duplicate timestamps).

---

## 3. CORE ARCHITECTURAL INVARIANTS & MULTI-STREAM INGESTION

### Stream 1: Binance USDT-M Futures 15m Klines
- Must fetch full history from 2019/2020 for EMA warmup.
- Schema: `open_time_ms`, `close_time_ms`, `datetime_utc`, `symbol`, `open`, `high`, `low`, `close`, `volume_base`, `volume_quote`, `trade_count`, `taker_buy_vol_btc`, `taker_sell_vol_btc`.

### Stream 2: Binance Spot 15m Klines (Dual-Market Alignment)
- Spot klines matched 1:1 on `open_time_ms` to calculate:
  1. **Cash-and-Carry Basis USD**: $\text{Basis} = \text{Futures Close} - \text{Spot Close}$.
  2. **Spot CVD**: Cumulative Volume Delta of Spot trades ($\text{Taker Buy Vol} - \text{Taker Sell Vol}$).
  3. **CVD Divergence (`zc_div`)**: $\Delta\text{Spot CVD} - \Delta\text{Futures CVD}$.

### Stream 3: Binance Futures Official Metrics (5m/15m Resampled)
- Concurrently fetched from Binance Data API:
  - `open_interest_usd`, `open_interest_k`, `oi_change_pct`
  - `top_account_ratio` (Long/Short ratio of top trader accounts)
  - `top_position_ratio` (Long/Short ratio of top trader positions)
  - `ls_ratio_global` (Global account long/short ratio)
  - `taker_volume_ratio` (Buy/Sell taker volume ratio)

### Stream 4: Funding Rate History
- 8-hour funding events aligned causally to the 15m candle close without future leakage (forward-filled until next settlement).

### Stream 5: Dual-Table Microstructure Footprint Ladder (Table 2)
- High-resolution aggTrades tick clustering by price bins:
  - `bid_vol_coin`, `ask_vol_coin`, `net_delta_coin`, `is_buy_imbalance`, `is_sell_imbalance`, `is_poc`.
- For historical periods before tick archive availability: Causal synthetic ladder synthesis derived strictly per-bar (no full-sample lookahead) tagged with `rung_source = 1` (Synthetic) vs `rung_source = 0` (Exact Tick).

---

## 4. CANONICAL INDICATOR & FEATURE COMPUTATION (TABLE 1)
The processor must compute all 28-37 indicators strictly on causal data:
1. **Trend & Volatility**:
   - EMAs: 8, 21, 50, 200, 800 (with warm-up from 2019/2020 history).
   - ATR: 14 and 100 periods.
   - RSI: 14 periods.
   - Volume SMA: 9 periods.
2. **VWAP & Order Flow Confluence**:
   - Session VWAP calculated daily from 00:00 UTC.
   - VWAP Z-score: `(Close - VWAP) / rolling_std(Close - VWAP, 24)`.
   - Volume Ratio: `volume_base / volume_sma9`.
3. **Non-Linear Liquidation Cascade Engine**:
   - Estimated liquidation volume (USD) for Longs and Shorts.
   - Rolling 96-bar Z-scores: `long_liq_zs`, `short_liq_zs`.
   - Liquidation imbalance ratio.

---

## 5. MANDATORY MULTI-AGENT VERIFICATION SYSTEM
The rebuilt architecture must include an integrated **Autonomous 3-Agent Verification Gate** executed prior to finalizing any Parquet export:

```
+---------------------------------------------------------------+
|             AUTONOMOUS 3-AGENT VERIFICATION COUNCIL           |
+-------------------------------+-------------------------------+
| Agent 1: Continuity & Cadence | Verifies 100% monotonic time  |
|                               | with exactly 900,000 ms steps |
|                               | and ZERO missing candles.     |
+-------------------------------+-------------------------------+
| Agent 2: Microstructure Math  | Verifies CVD divergence,      |
|                               | basis alignment, funding sign,|
|                               | and non-zero volume ratios.   |
+-------------------------------+-------------------------------+
| Agent 3: Zero-Null & Station  | Verifies ZERO NaNs/nulls,     |
|                               | finite values, and valid      |
|                               | schema type constraints.      |
+-------------------------------+-------------------------------+
```

If ANY check fails, the pipeline must reject the export, log the specific bar index and timestamp error, and trigger causal repair.

---

## 6. DELIVERABLE SPECIFICATION FOR ARENA.AI

Please generate the complete, production-ready, self-contained architecture:
1. **`run_historical_pipeline.py`**: Clean, modular orchestrator supporting CLI flags (`--symbol`, `--all-symbols`, `--start-date`, `--workers`, `--clean-cache`).
2. **`pipeline/binance_historical_fetcher.py`**: Async/threaded fetcher with Binance rate-limit handling (exponential backoff on HTTP 429/418).
3. **`pipeline/historical_metrics_processor.py`**: Fully vectorized, NumPy/Pandas accelerated indicator engine (all 28 features, zero loops).
4. **`pipeline/parquet_exporter.py`**: Relational dual-table exporter (Table 1 Master Parquet, Table 2 Footprint Ladder Parquet) with schema validation.
5. **`verification/verify_parquet_integrity.py`**: Complete implementation of the Autonomous 3-Agent Verification Council.

**CRITICAL CONSTRAINT**: Maintain 100% backward compatibility with the existing schema and filename conventions (`{symbol}_15m_master_2020_2026.parquet` and `{symbol}_15m_footprint_ladder.parquet`).
