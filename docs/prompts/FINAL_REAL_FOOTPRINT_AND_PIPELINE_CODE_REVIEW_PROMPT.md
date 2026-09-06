# MASTER ARCHITECTURAL & CODE REVIEW BRIEF: 100% REAL FOOTPRINT & PIPELINE ORCHESTRATOR

> **Target Audience for Peer Review**: Frontier Quantitative Evaluators (Claude Opus 5, Claude Sonnet 4.6, OpenAI Codex / GPT-4o, GLM-5.3, Qwen 2.5 / Max)  
> **Repository Target**: `Engine/run_historical_pipeline.py`, `Engine/pipeline/real_footprint_engine.py`, `Engine/core/schema.py`  
> **Review Objective**: Adversarial audit and validation of the unified, dual-table Binance historical pipeline before executing multi-year backfill downloads.

---

## 1. Executive Summary & Intent

Previous pipeline versions were conditionally accepted for Table 1 (Master 15m OHLCV + CVD + liquidations) but **formally rejected** by Codex and Sonnet 4.6 for Table 2 (Footprint Ladder) because missing periods were filled using causal synthetic heuristics (`synthesize_causal_ladder`). 

We have completely overhauled the architecture to enforce a **Strict Zero-Synthetic Mandate**:
1. **Master Orchestrator Entrypoint**: `Engine/run_historical_pipeline.py` is the unified CLI entrypoint that drives both Table 1 (Master) and Table 2 (Footprint Ladder).
2. **100% Real Tick Data**: Table 2 is strictly built from raw `aggTrades` downloaded from `data.binance.vision`. If trades do not exist (e.g. prior to an asset's futures listing), **zero rungs are generated**. No fake uniform distributions or synthetic profiles.
3. **Fixed Institutional Merge Matrix**: Discards volatile, day-to-day dynamic tick sizing in favor of deterministic, fixed price intervals matching Exocharts, Sierra Chart, and ATAS standards ($25.00 for BTC, $1.00 for ETH, $0.10 for SOL, etc.).
4. **Zero-Disk In-Memory Streaming**: Daily `.zip` archives from Binance Vision stream directly into an in-memory `io.BytesIO` buffer, decompress in RAM, vectorize into fixed price rungs, and immediately deallocate memory. Peak local disk and RAM footprint remain strictly `< 1 GB`.
5. **Resumable Monthly Chunking**: Ingests and saves intermediate monthly chunks (`{symbol}_ladder_{YYYY-MM}.parquet`) so network drops over a 2,000-day / 160 GB wire pull resume seamlessly without re-downloading.
6. **Continuous Raw Cleanup & Disk Governor**: Enforces a 5 GB disk headroom check and automatically purges all intermediate raw downloads on export.

---

## 2. Settled Mathematical & Order Flow Invariants

### 2.1 Fixed Price Discretization
For each trade execution $(p_i, q_i, t_i, \text{sell}_i)$ in Binance `aggTrades`:
- **Bar Assignment**: $t_{\text{bar}} = \lfloor t_i / 900{,}000 \rfloor \times 900{,}000$ (15m UTC epoch).
- **Price Rung**: $P_{\text{bin}} = \text{round}(p_i / \Delta P) \times \Delta P$, where $\Delta P$ is the asset's invariant merge step.
- **Taker Volume Split**:
  $$\text{bid\_vol} = \sum_{i \in \text{bin}, \text{sell}_i = \text{True}} q_i \quad (\text{Aggressive Market Sell into Bid})$$
  $$\text{ask\_vol} = \sum_{i \in \text{bin}, \text{sell}_i = \text{False}} q_i \quad (\text{Aggressive Market Buy into Ask})$$

### 2.2 18-Asset Fixed Merge Step Matrix (`schema.py`)
```python
FIXED_MERGE_STEPS = {
    "BTCUSDT": 25.0,        # Exocharts standard ($25 bucket)
    "ETHUSDT": 1.0,         # Exocharts standard ($1 bucket)
    "SOLUSDT": 0.10,        # 10-cent bucket
    "BNBUSDT": 0.50,        # Half-dollar bucket
    "DOGEUSDT": 0.0005,     # 5-pip bucket
    "XRPUSDT": 0.0010,      # 10-pip bucket
    "ADAUSDT": 0.0005,      # 5-pip bucket
    "TRXUSDT": 0.0001,      # Single pip bucket
    "LINKUSDT": 0.02,       # 2-cent bucket
    "AVAXUSDT": 0.05,       # 5-cent bucket
    "SUIUSDT": 0.005,       # Half-cent bucket
    "NEARUSDT": 0.01,       # 1-cent bucket
    "DOTUSDT": 0.01,        # 1-cent bucket
    "LTCUSDT": 0.10,        # 10-cent bucket
    "BCHUSDT": 0.50,        # Half-dollar bucket
    "APTUSDT": 0.01,        # 1-cent bucket
    "OPUSDT": 0.005,        # Half-cent bucket
    "ARBUSDT": 0.002,       # 2-tenth cent bucket
}
```

### 2.3 Microstructure Features & Edge Case Hardening
1. **Point of Control (POC)**: Rung with $\max(\text{total\_vol})$ per 15m candle (lowest price break on volume tie).
2. **Diagonal Imbalances (3:1)**:
   - **Buy Imbalance**: $\text{ask\_vol}(P) \ge 3.0 \times \text{bid\_vol}(P - \Delta P)$ and $\text{ask\_vol}(P) \ge \text{floor}$.
   - **Sell Imbalance**: $\text{bid\_vol}(P) \ge 3.0 \times \text{ask\_vol}(P + \Delta P)$ and $\text{bid\_vol}(P) \ge \text{floor}$.
   - **Dynamic Notional Floor**: $\text{floor} = \max(0.005 \times V_{\text{candle}}, \frac{\$50.00}{P})$. Eliminates dust trade false positives near candle wicks.
3. **Single-Rung Low-Volatility Guard**:
   - In tight consolidation candles where $\text{High} - \text{Low} < \Delta P$, $N_{\text{rungs}} = 1$.
   - Explicitly handled: $\text{is\_poc} = 1$, $\text{is\_buy\_imbalance} = 0$, $\text{is\_sell\_imbalance} = 0$.
4. **Stacked Imbalance Clusters**: Set to 1 when $\ge 3$ consecutive adjacent rungs exhibit diagonal imbalances in the same direction.
5. **70% Value Area**: Dual-sided symmetric volume expansion around the POC until 70% of total candle volume is captured.

---

## 3. Parquet Contract & Schema Definitions

### 3.1 Table 2: Footprint Ladder Contract (13 Columns)
```python
LADDER_COLUMNS = [
    "open_time_ms",        # int64  FK -> Table 1 15m candle timestamp
    "price_bin",           # float64 fixed price rung (e.g. 65000.0, 65025.0)
    "bid_vol_coin",        # float64 aggressive sell volume into bid
    "ask_vol_coin",        # float64 aggressive buy volume into ask
    "net_delta_coin",      # float64 ask_vol - bid_vol
    "total_vol_coin",      # float64 ask_vol + bid_vol
    "trade_count",         # int64  trade count executed at this rung
    "is_poc",              # int8   1 if Point of Control of this 15m candle, else 0
    "is_buy_imbalance",    # int8   1 if diagonal buy imbalance >= 3:1 with notional floor
    "is_sell_imbalance",   # int8   1 if diagonal sell imbalance >= 3:1 with notional floor
    "is_stacked_buy_imb",  # int8   1 if part of >= 3 stacked buy imbalance cluster
    "is_stacked_sell_imb", # int8   1 if part of >= 3 stacked sell cluster
    "is_value_area",       # int8   1 if within 70% Value Area (VAH to VAL)
]
```

### 3.2 Table 1: Master Contract (56 Canonical Columns)
Reduced from 72 to 56 columns by purging dead audit strings and constant flags (`future_flow_source`, `spot_flow_source`, `poc_source`, `is_synthetic`, `is_warmup_converged`), while preserving `is_imputed_metrics` (1-bit mask) to quarantine the 2022 Binance outage.

---

## 4. Key Code Implementation

### 4.1 Orchestrator Ingestion Flow (`Engine/run_historical_pipeline.py`)
```python
    fp_summary, fp_ladder = pd.DataFrame(), pd.DataFrame()
    ladder_stats = {"candles": 0, "tick_exact_candles": 0, "synthetic_candles": 0, "total_rungs": 0}
    if all_footprint or footprint_days > 0:
        fp_start = effective_start if all_footprint else max(effective_start, now - pd.Timedelta(days=footprint_days))
        # Bounded worker pool for footprint processing to prevent RAM spikes
        fp_workers = max(1, min(max_workers // 2, 6))
        fpe = RealFootprintEngine(cache_dir=cache_dir, max_workers=fp_workers, http=http, log=log)
        fp_ladder, fp_summary = fpe.fetch_footprint(symbol, fp_start.strftime("%Y-%m-%d"), now=now)
        ladder_stats = {
            "candles": int(fp_ladder["open_time_ms"].nunique()) if not fp_ladder.empty else 0,
            "tick_exact_candles": int(fp_ladder["open_time_ms"].nunique()) if not fp_ladder.empty else 0,
            "synthetic_candles": 0,
            "total_rungs": len(fp_ladder),
        }
        log(f"[OK] {symbol}: 100% real tick footprint fetched: {ladder_stats['total_rungs']:,} rungs across {ladder_stats['tick_exact_candles']:,} candles (ZERO synthetic)")

    t1 = time.time()
    processor = HistoricalMetricsProcessor(log=log)
    master = processor.process_master_dataset(
        klines, metrics, funding, fp_summary, spot, symbol=symbol,
        export_start_ms=int(effective_start.timestamp() * 1000),
    )

    t2 = time.time()
    ladder, ladder_stats = assemble_ladder(master, fp_ladder if not fp_ladder.empty else None, allow_synthetic=False)
```

### 4.2 In-Memory Streaming & Vectorized Grouping (`Engine/pipeline/real_footprint_engine.py`)
* `_download_day_trades_in_memory()`: Streams `.zip` via HTTP GET into `io.BytesIO(resp.content)`, unzips CSV in memory, and returns `pd.DataFrame` with zero filesystem footprint.
* `_aggregate_trades_to_ladder()`: Buckets trades into 15m bars and fixed price rungs, vectorizes POC, diagonal 3:1 imbalances, stacked clusters, and 70% Value Area.
* `fetch_and_process_month()`: Caches monthly chunks (`{symbol}_ladder_{YYYY-MM}.parquet`) to ensure seamless resume upon network disconnect.

---

## 5. Specific Questions for Peer Reviewers

1. **Deterministic Merge Step Geometry**:
   * Does the fixed merge matrix ($25 BTC, $1 ETH, $0.10 SOL) sufficiently balance high-resolution order flow visibility with parquet compression density across bull and bear volatility regimes?
2. **Zero Synthetic Lookahead & Downtime Handling**:
   * If Binance Public Vision aggTrades data is absent for an unlisted day or historical outage, the engine leaves that bar with zero footprint rungs. Is this fail-closed behavior preferable to synthetic rung interpolation?
3. **Volume Conservation & Precision**:
   * What floating-point tolerance should be enforced by the Autonomous Council when checking $\sum \text{rung\_total\_vol} \equiv \text{candle\_volume\_base}$? (We propose $< 0.1\%$ relative tolerance to account for Binance exchange millisecond trade boundary cuts).
4. **Disk & Memory Scalability**:
   * Does the combination of in-memory `io.BytesIO` streaming, bounded worker concurrency (`min(workers // 2, 6)`), and monthly interim checkpointing satisfy institutional safety against OOM and disk overflow on a 16-worker workstation?
