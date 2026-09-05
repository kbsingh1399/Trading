# ARENA.AI MASTER PROMPT: 18-ASSET ROW-BY-ROW DATASET AUDIT & PRODUCTION PIPELINE CERTIFICATION

> **EXECUTIVE OBJECTIVE**: Conduct an adversarial, forensic row-by-row audit across all 18 institutional asset datasets dumped in `Engine/binance_backtesting_data/` and the master pipeline orchestrator `Engine/run_historical_pipeline.py`. Verify that every row across all 3,467,571 candles and 70,934,532 footprint rungs is mathematically sound, continuous, causal (zero-lookahead), and fully compliant with the 3-Agent Council and Metrics Validity Gates.

---

## 1. REPOSITORY & DIRECT GIT REFERENCES

Both branches are byte-for-byte mirrors on GitHub at commit `dee695ddfe3fad96fb2d17e6ace5481ec3ac70e8`:
- **Repository**: [https://github.com/kbsingh1399/Trading](https://github.com/kbsingh1399/Trading) (Branch: `main`)
- **Dual Mirror**: [https://github.com/kbsingh1399/Trading/tree/arena%2F01a07263-trading](https://github.com/kbsingh1399/Trading/tree/arena%2F01a07263-trading)
- **Active Commit**: `dee695ddfe3fad96fb2d17e6ace5481ec3ac70e8`

### Core Source Code Links:
1. **Pipeline Orchestrator**:
   [`Engine/run_historical_pipeline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py)
2. **Causal Metrics Processor**:
   [`Engine/pipeline/historical_metrics_processor.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py)
3. **Binance Archive & REST Ingest**:
   [`Engine/pipeline/binance_historical_fetcher.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/binance_historical_fetcher.py)
4. **Dual-Table Footprint Ladder Generator**:
   [`Engine/pipeline/footprint_ladder.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/footprint_ladder.py)
5. **Atomic Parquet Exporter**:
   [`Engine/pipeline/parquet_exporter.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/parquet_exporter.py)
6. **Autonomous 3-Agent Integrity Council**:
   [`Engine/verification/verify_parquet_integrity.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py)
7. **Metrics Validity Gate**:
   [`Engine/verification/audit_probe_metrics_validity.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/audit_probe_metrics_validity.py)
8. **Master Verification Report**:
   [`Engine/binance_backtesting_data/verification_report.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/verification_report.json)

---

## 2. THE 18 INSTITUTIONAL ASSET COMPLETE FILE INVENTORY (ALL 55 FILES)

All 36 parquet files (18 15m Master + 18 Footprint Ladder), all 18 dataset manifests, and the council report are live on GitHub under `Engine/binance_backtesting_data/`:

| Symbol | Listing / Bars | 15m Master Parquet | 15m Footprint Ladder Parquet | Dataset Manifest JSON |
|---|---|---|---|---|
| **BTCUSDT** | 2020-09-01 (210,797) | [BTC Master (94.2 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet) | [BTC Ladder (15.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_15m_footprint_ladder.parquet) | [BTC Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_dataset_manifest.json) |
| **ETHUSDT** | 2020-09-01 (210,800) | [ETH Master (91.4 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ETHUSDT_15m_master_2020_2026.parquet) | [ETH Ladder (17.0 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ETHUSDT_15m_footprint_ladder.parquet) | [ETH Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ETHUSDT_dataset_manifest.json) |
| **SOLUSDT** | 2020-09-14 (209,527) | [SOL Master (83.9 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SOLUSDT_15m_master_2020_2026.parquet) | [SOL Ladder (17.0 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SOLUSDT_15m_footprint_ladder.parquet) | [SOL Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SOLUSDT_dataset_manifest.json) |
| **BNBUSDT** | 2020-09-01 (210,803) | [BNB Master (84.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BNBUSDT_15m_master_2020_2026.parquet) | [BNB Ladder (15.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BNBUSDT_15m_footprint_ladder.parquet) | [BNB Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BNBUSDT_dataset_manifest.json) |
| **XRPUSDT** | 2020-09-01 (210,800) | [XRP Master (85.3 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/XRPUSDT_15m_master_2020_2026.parquet) | [XRP Ladder (18.0 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/XRPUSDT_15m_footprint_ladder.parquet) | [XRP Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/XRPUSDT_dataset_manifest.json) |
| **DOGEUSDT**| 2020-09-01 (210,804) | [DOGE Master (84.8 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOGEUSDT_15m_master_2020_2026.parquet) | [DOGE Ladder (17.6 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOGEUSDT_15m_footprint_ladder.parquet) | [DOGE Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOGEUSDT_dataset_manifest.json) |
| **ADAUSDT** | 2020-09-01 (210,801) | [ADA Master (83.6 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ADAUSDT_15m_master_2020_2026.parquet) | [ADA Ladder (17.5 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ADAUSDT_15m_footprint_ladder.parquet) | [ADA Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ADAUSDT_dataset_manifest.json) |
| **TRXUSDT** | 2020-09-01 (210,804) | [TRX Master (80.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/TRXUSDT_15m_master_2020_2026.parquet) | [TRX Ladder (15.3 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/TRXUSDT_15m_footprint_ladder.parquet) | [TRX Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/TRXUSDT_dataset_manifest.json) |
| **LINKUSDT**| 2020-09-01 (210,801) | [LINK Master (84.2 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/LINKUSDT_15m_master_2020_2026.parquet) | [LINK Ladder (17.3 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/LINKUSDT_15m_footprint_ladder.parquet) | [LINK Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/LINKUSDT_dataset_manifest.json) |
| **AVAXUSDT**| 2020-09-23 (208,661) | [AVAX Master (80.6 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/AVAXUSDT_15m_master_2020_2026.parquet) | [AVAX Ladder (16.3 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/AVAXUSDT_15m_footprint_ladder.parquet) | [AVAX Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/AVAXUSDT_dataset_manifest.json) |
| **SUIUSDT** | 2023-05-03 (117,236) | [SUI Master (49.4 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SUIUSDT_15m_master_2020_2026.parquet) | [SUI Ladder (10.2 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SUIUSDT_15m_footprint_ladder.parquet) | [SUI Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/SUIUSDT_dataset_manifest.json) |
| **NEARUSDT**| 2020-10-15 (206,546) | [NEAR Master (79.9 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/NEARUSDT_15m_master_2020_2026.parquet) | [NEAR Ladder (17.3 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/NEARUSDT_15m_footprint_ladder.parquet) | [NEAR Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/NEARUSDT_dataset_manifest.json) |
| **DOTUSDT** | 2020-09-01 (210,802) | [DOT Master (82.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOTUSDT_15m_master_2020_2026.parquet) | [DOT Ladder (16.4 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOTUSDT_15m_footprint_ladder.parquet) | [DOT Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/DOTUSDT_dataset_manifest.json) |
| **LTCUSDT** | 2020-09-01 (210,802) | [LTC Master (84.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/LTCUSDT_15m_master_2020_2026.parquet) | [LTC Ladder (16.1 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/LTCUSDT_15m_footprint_ladder.parquet) | [LTC Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/LTCUSDT_dataset_manifest.json) |
| **BCHUSDT** | 2020-09-01 (210,804) | [BCH Master (84.9 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BCHUSDT_15m_master_2020_2026.parquet) | [BCH Ladder (16.3 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BCHUSDT_15m_footprint_ladder.parquet) | [BCH Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BCHUSDT_dataset_manifest.json) |
| **APTUSDT** | 2022-10-19 (136,107) | [APT Master (56.5 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/APTUSDT_15m_master_2020_2026.parquet) | [APT Ladder (11.0 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/APTUSDT_15m_footprint_ladder.parquet) | [APT Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/APTUSDT_dataset_manifest.json) |
| **OPUSDT**  | 2022-06-01 (149,500) | [OP Master (61.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/OPUSDT_15m_master_2020_2026.parquet) | [OP Ladder (13.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/OPUSDT_15m_footprint_ladder.parquet) | [OP Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/OPUSDT_dataset_manifest.json) |
| **ARBUSDT** | 2023-03-23 (121,176) | [ARB Master (49.7 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ARBUSDT_15m_master_2020_2026.parquet) | [ARB Ladder (10.1 MB)](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ARBUSDT_15m_footprint_ladder.parquet) | [ARB Manifest JSON](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/ARBUSDT_dataset_manifest.json) |

- **Master Council Report**: [`verification_report.json`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/verification_report.json)

---

## 3. AUDIT MANDATE 1: ROW-BY-ROW DATA INTEGRITY VERIFICATION RECIPES

Execute or simulate the following row-by-row mathematical assertions on the 18 master datasets:

### 3.1 Strict Cadence & Monotonic Continuity
For each consecutive row pair $(i, i+1)$ in every master parquet:
$$\Delta t = \text{open\_time\_ms}[i+1] - \text{open\_time\_ms}[i] \equiv 900{,}000\text{ ms (exactly 15 minutes)}$$
$$\text{close\_time\_ms}[i] = \text{open\_time\_ms}[i] + 899{,}999\text{ ms}$$
- **Assertion**: Are there exactly 0 timestamp breaks, 0 duplicate timestamps, and 0 non-monotonic steps across all 3,467,571 bars?

### 3.2 Row-by-Row Price & Volume Invariants
On every individual row:
- $\text{high} \ge \max(\text{open}, \text{close})$
- $\text{low} \le \min(\text{open}, \text{close})$
- $\text{low} > 0$ and $\text{high} > 0$
- $\text{volume} \ge 0$, $\text{quote\_volume} \ge 0$, $\text{trades} \ge 0$
- $\text{taker\_buy\_volume} \le \text{volume}$
- $\text{taker\_buy\_quote\_volume} \le \text{quote\_volume}$

### 3.3 Zero-Null and Finite Value Contract
- Check every column across all 62 relational schema fields.
- **Assertion**: Are there exactly 0 nulls, 0 NaNs, and 0 infinities in any column for all 18 symbols?

### 3.4 Bounded Microstructure Oscillators & Indicators
Verify row-by-row value domain constraints:
- $0.0 \le \text{rsi\_14} \le 100.0$
- $0.0 \le \text{mfi\_14} \le 100.0$
- $0.0 \le \text{adx\_14} \le 100.0$
- $\text{atr\_14} > 0$ (Verify that sub-dollar assets DOGE, TRX, ADA, XRP preserve 8 decimal places and do NOT collapse to 0.0)
- $-1.0 \le \text{funding\_rate} \le 1.0$
- $\text{open\_interest} \ge 0.0$

### 3.5 Causal Attestation & Metrics Quarantine Verification
- Where Binance Vision historical archives have authentic pre-archive gaps (attested in the dataset manifest under `provenance.metrics_archive_absent_months`):
  - Does the dataset set $\text{open\_interest} = 0.0$ and explicitly tag $\text{is\_imputed} = 1$?
  - Does the Metrics Validity Gate confirm 0 unflagged frozen ranges and 0 impossible open interest values?

### 3.6 Footprint Ladder Row-by-Row Integrity (`*_15m_footprint_ladder.parquet`)
For every rung row:
- $\text{ask\_qty} \ge 0$ and $\text{bid\_qty} \ge 0$
- $\text{delta} \equiv \text{ask\_qty} - \text{bid\_qty}$
- $\text{total\_qty} \equiv \text{ask\_qty} + \text{bid\_qty}$
- $\text{rung\_source} \in \{0, 1\}$ (0 = authentic aggTrades tick cluster, 1 = causal synthetic fallback)
- $\text{imbalance\_buy} \in \{0, 1\}$ and $\text{imbalance\_sell} \in \{0, 1\}$ (stored as `int8`)

---

## 4. AUDIT MANDATE 2: ADVERSARIAL PIPELINE ARCHITECTURE REVIEW

Audit [`Engine/run_historical_pipeline.py`](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py) against senior institutional quantitative standards:

1. **Fail-Closed Execution Gate**:
   - Verify that manifests are exported and verified *before* acceptance, and that any failure triggers immediate file cleanup and abort.
2. **Zero-Lookahead Guarantee**:
   - Verify that metrics alignment uses strictly $\le \text{close\_time\_ms}$, that backward filling (`.bfill()`) has been completely eliminated, and that session VWAP daily resets occur strictly at 00:00 UTC.
3. **Concurrency & Rate-Limiting Protection**:
   - Verify that the shared HTTP client enforces 418/429 exponential backoff with jitter and a 5.0-second floor on `Retry-After`.

---

## 5. REQUIRED AUDIT DELIVERABLES

Please return a structured audit report answering:
1. **Per-Asset Row-by-Row Scorecard**: Confirmation for each of the 18 assets that bar counts, rungs, continuity, precision, and bounds pass 100%.
2. **Adversarial Bug Hunt Findings**: Any residual mathematical, structural, or lookahead defects identified.
3. **Formal Institutional Certification**: A definitive verdict on whether these datasets are certified for the 20 Out-Of-Sample (OOS) Walk-Forward Windows in `Engine_2/s1_liquidation_cascade.py`.
