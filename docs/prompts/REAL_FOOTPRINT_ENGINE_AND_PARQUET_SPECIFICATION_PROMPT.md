# ARCHITECTURAL AUDIT & PEER REVIEW BRIEF: 100% REAL TICK FOOTPRINT ENGINE & FIXED-LEVEL PARQUET ARCHITECTURE

> **Target Audience for Peer Review**: Frontier Quantitative Evaluators (Claude Opus 5, Claude Sonnet 4.6, OpenAI Codex / GPT-4o, GLM-5.3, Qwen 2.5/Max).
> **Context**: Institutional Quantitative Backtesting Infrastructure for Binance USDT-M Perpetuals across 18 assets (2020 – 2026).
> **Core Objective**: Evaluate the proposed mathematical, architectural, and storage specifications for building a 100% real tick-level Order Flow Footprint dataset using Binance `aggTrades` archives with fixed price merge levels ($25 for BTC, $1 for ETH, etc.) and continuous streaming in-memory raw file cleanup.

---

## 1. Executive Context & The Problem Statement

### 1.1 Why Synthetic Footprints Were Permanently Rejected
In earlier pipeline iterations, candles lacking granular trade archives had footprint ladders generated via causal synthetic decomposition (`synthesize_causal_ladder`): distributing bar volume uniformly across price steps and placing POC at close. 

**Adjudication Consensus**: All external review models (Codex, Sonnet 4.6, GLM-5.3) unanimously reached the verdict:
> *"REJECT for empirical footprint microstructure. Synthetic ladders with uniform volume distribution cannot reproduce empirical POC clustering, volume delta divergence, or diagonal imbalances. Imbalances must never be fabricated."*

**The New Mandate**:
1. **100% Real Trade Data**: Table 2 must be derived exclusively from empirical trade executions downloaded from Binance Public Vision Archive (`https://data.binance.vision/data/futures/um/daily/aggTrades/`).
2. **Zero Synthetic Interpolation**: If trade data does not exist for an asset prior to its futures listing, no rungs are generated.
3. **Deterministic Fixed Merge Levels**: Instead of daily-varying dynamic bin steps, enforce fixed price intervals ($25 for BTC, $1 for ETH) matching institutional order flow charting platforms (Exocharts, Sierra Chart, ATAS).
4. **Zero-Disk Bloat In-Memory Streaming**: Raw multi-gigabyte `.zip` and `.csv` trade archives must be processed in RAM streams and continuously cleaned up so local disk space never spikes.

---

## 2. Fixed Merge Level Calibration Across 18 Institutional Assets

### 2.1 The Merge Problem
At raw minimum tick sizes ($0.10 for BTC, $0.01 for ETH), a single volatile 15m candle with a $2,000 price range contains up to **20,000 rungs**. Over 5.5 years, raw ticks would generate hundreds of gigabytes per asset, mostly containing 0-volume noise rungs.

By merging into institutional price steps $\Delta P$, every 15m candle is condensed into a statistically dense profile of **15 to 60 rungs**, where volume nodes, Point of Control (POC), and diagonal imbalances reflect genuine liquidity absorption and aggressive market sweeps.

### 2.2 Proposed 18-Asset Merge Matrix

| # | Asset | Typical Price | Fixed Merge Step ($\Delta P$) | Typical 15m ATR | Resulting Rungs / Bar | Rationale & Platform Standard |
|---|---|---|---|---|---|---|
| 1 | **BTCUSDT** | $20k - $100k+ | **$25.00** | $300 - $1,000 | 12 - 40 | Standard Exocharts / Sierra Chart 25-tick |
| 2 | **ETHUSDT** | $1,000 - $5,000 | **$1.00** | $15 - $60 | 15 - 60 | Standard Exocharts / Sierra Chart $1 bucket |
| 3 | **SOLUSDT** | $20 - $300 | **$0.10** | $1.50 - $6.00 | 15 - 60 | 10-cent microstructure resolution |
| 4 | **BNBUSDT** | $200 - $800 | **$0.50** | $4.00 - $15.00 | 8 - 30 | Half-dollar institutional bucket |
| 5 | **DOGEUSDT** | $0.05 - $0.40 | **$0.0005** | $0.003 - $0.015 | 6 - 30 | 5-pip bucket (dense clustering) |
| 6 | **XRPUSDT** | $0.30 - $2.50 | **$0.0010** | $0.015 - $0.080 | 15 - 80 | 10-pip bucket |
| 7 | **ADAUSDT** | $0.25 - $3.00 | **$0.0005** | $0.010 - $0.050 | 20 - 100 | 5-pip bucket |
| 8 | **TRXUSDT** | $0.05 - $0.30 | **$0.0001** | $0.001 - $0.005 | 10 - 50 | 1-pip bucket |
| 9 | **LINKUSDT** | $5.00 - $50.00 | **$0.02** | $0.20 - $1.00 | 10 - 50 | 2-cent bucket |
| 10 | **AVAXUSDT** | $10.00 - $150.00 | **$0.05** | $0.50 - $3.00 | 10 - 60 | 5-cent bucket |
| 11 | **SUIUSDT** | $0.50 - $5.00 | **$0.005** | $0.05 - $0.25 | 10 - 50 | Half-cent bucket |
| 12 | **NEARUSDT** | $1.00 - $20.00 | **$0.01** | $0.10 - $0.60 | 10 - 60 | 1-cent bucket |
| 13 | **DOTUSDT** | $3.00 - $55.00 | **$0.01** | $0.15 - $0.80 | 15 - 80 | 1-cent bucket |
| 14 | **LTCUSDT** | $50.00 - $400.00 | **$0.10** | $1.50 - $8.00 | 15 - 80 | 10-cent bucket |
| 15 | **BCHUSDT** | $100.00 - $1,500 | **$0.50** | $5.00 - $30.00 | 10 - 60 | Half-dollar bucket |
| 16 | **APTUSDT** | $3.00 - $20.00 | **$0.01** | $0.15 - $0.70 | 15 - 70 | 1-cent bucket |
| 17 | **OPUSDT** | $0.80 - $5.00 | **$0.005** | $0.04 - $0.20 | 8 - 40 | Half-cent bucket |
| 18 | **ARBUSDT** | $0.40 - $2.50 | **$0.002** | $0.02 - $0.10 | 10 - 50 | 2-tenth cent bucket |

---

## 3. Order Flow Microstructure Mathematics & Contract

### 3.1 Raw Trade Ingestion
From Binance `aggTrades` record: `[transact_time, price, quantity, is_buyer_maker]`:
- Candle alignment: $t_{\text{bar}} = \lfloor \text{transact\_time} / 900{,}000 \rfloor \times 900{,}000$ (Unix epoch ms).
- Rung assignment: $P_{\text{bin}} = \text{round}(p / \Delta P) \times \Delta P$.
- Aggressive side classification:
  - `is_buyer_maker == True` $\implies$ Taker Sell into Bid $\implies$ `bid_vol_coin += quantity`
  - `is_buyer_maker == False` $\implies$ Taker Buy into Ask $\implies$ `ask_vol_coin += quantity`

### 3.2 Microstructure Indicators
1. **Delta**: $\text{net\_delta} = \text{ask\_vol} - \text{bid\_vol}$.
2. **POC (Point of Control)**: The unique price bin with the absolute maximum `total_vol` ($\text{ask\_vol} + \text{bid\_vol}$) in the 15m bar. Ties broken deterministically by lowest price.
3. **Diagonal Imbalance (Bid/Ask Order Flow Footprint)**:
   - Evaluated strictly across diagonally adjacent price rungs:
     - **Diagonal Buy Imbalance**: $\text{ask\_vol}(P) \ge 3.0 \times \text{bid\_vol}(P - \Delta P)$
     - **Diagonal Sell Imbalance**: $\text{bid\_vol}(P) \ge 3.0 \times \text{ask\_vol}(P + \Delta P)$
   - **Notional Noise Floor**: To prevent low-volume top-of-candle dust from triggering false imbalances:
     $$\text{floor} = \max\left(0.005 \times V_{\text{candle}}, \frac{\$50.00}{P}\right)$$
     An imbalance is only flagged if the aggressive volume exceeds this floor.
4. **Stacked Imbalance Clusters**:
   - $\ge 3$ consecutive adjacent rungs displaying diagonal imbalances in the same direction.
   - Represents institutional market order sweeps that absorbed all resting liquidity.
5. **Value Area (VAH / VAL)**:
   - The contiguous price band containing 70% of the total 15m candle volume, centered around the POC.

---

## 4. Parquet Storage Architecture & Strict Zero-Disk Bloat

### 4.1 Table 2 Parquet Schema (`{symbol}_15m_footprint_ladder.parquet`)

| Column | Arrow Dtype | Description |
|---|---|---|
| `open_time_ms` | `int64` | 15m candle start timestamp (Unix ms) |
| `price_bin` | `float64` | Merged price rung ($P_{\text{bin}}$) |
| `bid_vol_coin` | `float64` | Aggressive sell volume executed at bid |
| `ask_vol_coin` | `float64` | Aggressive buy volume executed at ask |
| `net_delta_coin` | `float64` | `ask_vol_coin - bid_vol_coin` |
| `total_vol_coin` | `float64` | `ask_vol_coin + bid_vol_coin` |
| `trade_count` | `int32` | Number of distinct trades at this rung |
| `is_poc` | `int8` | 1 if Point of Control of the candle, else 0 |
| `is_buy_imbalance` | `int8` | 1 if diagonal buy imbalance $\ge 3:1$, else 0 |
| `is_sell_imbalance`| `int8` | 1 if diagonal sell imbalance $\ge 3:1$, else 0 |
| `is_stacked_buy_imb` | `int8` | 1 if member of $\ge 3$ stacked buy cluster |
| `is_stacked_sell_imb`| `int8` | 1 if member of $\ge 3$ stacked sell cluster |
| `is_value_area` | `int8` | 1 if within 70% volume Value Area (VAH-VAL) |

### 4.2 Mathematical Conservation Laws (Integrity Council Gates)
Every exported footprint ladder file must strictly satisfy these mathematical identities against the Table 1 Master candle:
1. **Volume Conservation**:
   $$\left| \sum_{\text{rungs} \in \text{bar}} \text{total\_vol\_coin} - \text{volume\_base}_{\text{master}} \right| < 10^{-4} \times \text{volume\_base}_{\text{master}}$$
2. **Delta Conservation**:
   $$\left| \sum_{\text{rungs} \in \text{bar}} \text{net\_delta\_coin} - \left(\text{taker\_buy\_vol} - \text{taker\_sell\_vol}\right) \right| < 10^{-4}$$
3. **POC Uniqueness**: Exactly 1 rung per 15m candle has `is_poc == 1`.
4. **Boundary Invariant**: All rungs in candle $t$ must satisfy:
   $$\text{low}_{\text{candle}} - \Delta P \le \text{price\_bin} \le \text{high}_{\text{candle}} + \Delta P$$

---

## 5. Streaming Download Architecture (Continuous Cleanup)

To eliminate any possibility of disk space exhaustion during multi-year downloads (where raw archives would exceed 2 Terabytes):
1. **In-Memory Streaming**:
   - HTTP GET fetches `https://data.binance.vision/data/futures/um/daily/aggTrades/{symbol}/{symbol}-aggTrades-{YYYY-MM-DD}.zip`.
   - The `.zip` is read directly from memory into `zipfile.ZipFile(io.BytesIO(data))`.
   - Trades are parsed in RAM using vectorized Polars / PyArrow.
2. **Instant Buffer Eviction**:
   - As soon as the daily trades are bucketed into 15m rungs, raw trade records and `.zip` memory buffers are deallocated immediately (`del trades; gc.collect()`).
   - No `.zip` or uncompressed `.csv` file is ever written to the local hard drive.
3. **Per-Symbol Final Parquet Assembly**:
   - Rung aggregations are written directly to parquet.
   - Peak temporary disk space during the entire 2020-2026 process: **< 1.0 GB**.

---

## 6. Questions for Peer Review & Adjudication

We request all inspecting models (Opus 5, Sonnet 4.6, Codex / GPT-4o, GLM-5.3) to provide direct, adversarial critique on the following 4 engineering questions:

1. **Merge Level Precision**:
   - Are the proposed fixed merge levels ($25 for BTC, $1 for ETH, $0.10 for SOL, $0.50 for BNB) optimal for backtesting 15m order flow strategies, or should they be wider/narrower?
2. **Diagonal Imbalance Parameters**:
   - Is a $3.0\times$ (300%) diagonal imbalance ratio with a $0.5\%$ candle volume noise floor the quantitative industry standard, or do you recommend dynamic ratio scaling (e.g. $4.0\times$ or ATR-scaled)?
3. **Conservation Invariants**:
   - Does the requirement that $\sum \text{rung\_total\_vol} \equiv \text{volume\_base}$ and $\sum \text{rung\_delta} \equiv \text{future\_cvd\_15m}$ provide sufficient mathematical proof to prevent lookahead or data corruption?
4. **Storage & Execution Scalability**:
   - Storing Table 2 as a separate `{symbol}_15m_footprint_ladder.parquet` file indexed by `open_time_ms` vs flattening summary metrics into Table 1 Master: is this dual-table architecture optimal for performance?
