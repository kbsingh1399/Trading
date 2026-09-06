# 🏛️ OPUS 5 FINAL SUPREME AUDIT & DATASET CERTIFICATION BRIEF
## Definitive Quantitative Review: Patched Binance USDT-M Pipeline & Reference BTC Dataset

---

## ⛔ CRITICAL INGESTION DIRECTIVE FOR OPUS 5
You are the Supreme Quantitative Arbiter and Principal Microstructure Architect.
Before delivering your verdict, inspect the committed code, manifest, and verification reports directly from GitHub:

### Raw GitHub Source Files (Branch: `main`, Mirror: `arena/01a07263-trading`):
1. **Pipeline Processor**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py`
2. **Pipeline Runner**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py`
3. **Autonomous Council Verifier**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py`
4. **Canonical Indicators Math**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py`
5. **Schema Contract (72 cols)**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py`
6. **BTC Dataset Manifest (JSON)**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/BTCUSDT_dataset_manifest.json`
7. **Council Verification Report (JSON)**: `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/binance_backtesting_data/verification_report.json`
8. **BTC Master Parquet (Binary, 94.2 MB)**: `https://github.com/kbsingh1399/Trading/raw/main/Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet`
9. **BTC Footprint Ladder (Binary, 15.0 MB)**: `https://github.com/kbsingh1399/Trading/raw/main/Engine/binance_backtesting_data/BTCUSDT_15m_footprint_ladder.parquet`

---

## 1. CONTEXT & THE TRI-MODEL AUDIT PRECEDENT

Following Round 5 backtest preparations, three frontier models (Claude Sonnet 4.6, GLM-5.3, and Qwen 2.5/Max) audited the pipeline and raw datasets. Their findings triggered a code patch and a single-asset regeneration for **`BTCUSDT`** (2020-09-01 to 2026-09-06, 210,848 15m candles, 2,710,890 footprint rungs).

### What Was Patched in Code:
1. **`zc_div` False Positive Absorption Bug Fixed**:
   - *Pre-patch*: On bars where `spot_flow_source == "UNAVAILABLE"`, `spot_delta` was 0.0, resulting in `zc_div = 0.0 - fut_delta = -fut_delta`. Out of 93 UNAVAILABLE bars, 50 bars (53.8%) fired false `zc_div > 0.8` spot absorption signals.
   - *Patch*: In `historical_metrics_processor.py:380`:
     ```python
     out["zc_div"] = np.where(spot_exact, spot_delta - fut_delta, 0.0)
     ```
2. **Autonomous Council Hardening**:
   - `verify_parquet_integrity.py` was updated to check `zc_div_identity` strictly on valid spot bars (`~unavailable`), and added `zc_div_unavailable_zero` asserting zero non-zero values on unavailable bars.
3. **Fast-Skip Hardening**:
   - `run_historical_pipeline.py` now verifies manifest row counts, UTC epoch timestamps, and bidirectional timestamp inclusion (`np.isin(m_ts, l_ts).all() and np.isin(l_ts, m_ts).all()`).

---

## 2. THE THREE FRONTIER MODEL VERDICTS ON THE PATCH

### A. Claude Sonnet 4.6 (`Sonnet_4.6_2` Dashboard):
- **Verification Verdict**: **CONFIRMED CORRECT (Finding F-12)**. All 93 UNAVAILABLE bars have `zc_div == 0.0` strictly. 0 false-positive signals fired.
- **Microstructure Flags**:
  - `F-01 (Critical)`: The footprint ladder is 100% causal synthetic (`tick_exact_candles = 0`). Microstructure strategies must not trade footprint imbalance heuristics without raw tick data.
  - `F-02 (Critical)`: Cumulative CVD sums include the zeroed bars; recovery bars immediately following an outage do not reflect missing volume.
  - `F-03 (High)`: 86.56% of 2022 bars lack official metrics. Walk-forward testing must mask `is_imputed_metrics == 1`.

### B. GLM-5.3 (`GLM_5.3_0609_2`):
- **Epistemic Debate (Finding #23)**: Argues that setting `zc_div = 0.0` is a "fabricated value" (asserts no divergence where divergence is unknown) and breaks the formula identity `zc_div == spot - fut`. Recommends `NaN` + masking, or having downstream strategies gate on `spot_flow_source == 'SPOT_EXACT'`.
- **Polarity Query (Finding #6)**: Questioned whether negative `long_liq_usd` values cause `long_liq_zs` to invert.

### C. Qwen 2.5 / Max (`Qwen_0609_2`):
- Audited against an un-invalidated pre-push GitHub cache. Demanded 4 mandatory actions:
  1. Set `out["zc_div"] = np.where(~spot_exact, 0.0, spot_delta - fut_delta)` $\to$ **Already committed 1:1**.
  2. Add `zc_div_unavailable_zero` to Council $\to$ **Already committed 1:1**.
  3. Re-run pipeline for BTC $\to$ **Already exported**.
  4. Gate strategy on `is_imputed_metrics == 0` $\to$ **Agreed by all models**.

---

## 3. LIVE EMPIRICAL PROBE PROOFS (ON THE REAL BTCUSDT PARQUET)

Run this Python verification script to confirm the exact physical properties of the dataset:

```python
import pandas as pd, numpy as np

df = pd.read_parquet("https://github.com/kbsingh1399/Trading/raw/main/Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet")

# 1. UNAVAILABLE Spot Integrity
un = df[df['spot_flow_source'] == 'UNAVAILABLE']
print("UNAVAILABLE bars count:", len(un))  # Exactly 93
print("UNAVAILABLE non-zero zc_div:", (un['zc_div'] != 0.0).sum())  # Exactly 0
print("UNAVAILABLE non-zero spot_cvd_15m:", (un['spot_cvd_15m'] != 0.0).sum())  # Exactly 0

# 2. SPOT_EXACT Divergence Identity
ex = df[df['spot_flow_source'] == 'SPOT_EXACT']
diff = np.abs(ex['zc_div'] - (ex['spot_cvd_15m'] - ex['future_cvd_15m'])).max()
print("SPOT_EXACT max identity error:", diff)  # 0.00e+00 (< 1e-6)

# 3. Bar Cadence & Boundary Continuity
gaps = df['open_time_ms'].diff().dropna()
print("Non-15m gaps (must be 0):", (gaps != 900_000).sum())  # Exactly 0
print("Bad close_time_ms:", (df['close_time_ms'] != df['open_time_ms'] + 899_999).sum())  # Exactly 0

# 4. Session VWAP Identity (Typical Price (H+L+C)/3 * Volume)
tp = (df['high'] + df['low'] + df['close']) / 3.0
day = df['open_time_ms'] // 86_400_000
pv = (tp * df['volume_base']).groupby(day).cumsum()
cv = df['volume_base'].groupby(day).cumsum()
expected_vwap = np.where(cv > 1e-9, pv / cv, df['close'])
print("Session VWAP mismatches:", (np.abs(df['session_vwap'] - expected_vwap) > 1e-6).sum())  # Exactly 0

# 5. Liquidation Polarity Proof (Addressing GLM Finding #6)
corr_signed = np.corrcoef(df['long_liq_usd'], df['long_liq_zs'])[0, 1]
corr_abs = np.corrcoef(np.abs(df['long_liq_usd']), df['long_liq_zs'])[0, 1]
print("Corr(signed long_liq_usd, long_liq_zs):", round(corr_signed, 4))  # -0.6903
print("Corr(|long_liq_usd|, long_liq_zs):", round(corr_abs, 4))          # +0.6903
spike = df[df['long_liq_zs'] > 1.8]
normal = df[df['long_liq_zs'] <= 1.8]
print(f"Mean liquidation at Z > 1.8:  ${np.abs(spike['long_liq_usd']).mean():,.2f}")  # $1,734,207.01
print(f"Mean liquidation at Z <= 1.8: ${np.abs(normal['long_liq_usd']).mean():,.2f}") # $120,362.88
print("Spike surge ratio:", round(np.abs(spike['long_liq_usd']).mean() / np.abs(normal['long_liq_usd']).mean(), 2), "x") # 14.41x

# 6. Signals on UNAVAILABLE Bars
signals = (
    (df['long_liq_zs'] > 1.8) & (df['zc_div'] > 0.8) &
    (df['rsi_14'] < 40) & (df['vwap_zscore'] < -0.5)
)
print("Total long cascade signals:", signals.sum())
print("Signals on UNAVAILABLE bars:", (signals & (df['spot_flow_source'] == 'UNAVAILABLE')).sum())  # Exactly 0
```

---

## 4. THE FOUR QUESTIONS FOR OPUS 5 (FINAL ARBITRATION)

As Supreme Quant Arbiter, provide your structured judgment on these 4 questions:

### Question 1: Data Contract vs Strategy Gating (`zc_div`)
In a zero-null parquet contract (no NaNs permitted), is setting `zc_div = 0.0` when `spot_flow_source == 'UNAVAILABLE'` mathematically and architecturally sound, provided `spot_flow_source` is explicitly stored? Should downstream backtests enforce an explicit `spot_flow_source == 'SPOT_EXACT'` gate, or is the `zc_div = 0.0` clamp sufficient?

### Question 2: The 2022 Imputation Regime (W5 & W6)
All models confirmed that 86.56% of 2022 bars carry imputed metrics (`is_imputed_metrics == 1`). 
Should our Walk-Forward Optimization engine (`Engine/s1_liquidation_cascade.py`):
- Option A: Explicitly gate entry signals with `is_imputed_metrics == 0`?
- Option B: Drop W5 (Q1 2022) and W6 (Q2 2022) from the 20-window walk-forward suite?
- Option C: Fall back to metric-neutral price/volume-only alpha during imputed regimes?

### Question 3: Footprint Ladder Scope
Given that the footprint ladder is 100% causal synthetic geometry (`tick_exact_candles = 0`), does this invalidate OHLCV/CVD strategy invariants, or does it strictly restrict footprint-specific imbalance features (`fp_stacked_buy_imb`, `fp_poc`)?

### Question 4: Go/No-Go Decision for 18-Asset Regeneration
Based on the live code, manifest, and probe metrics:
Does this single reference `BTCUSDT` dataset meet institutional hedge-fund standards to greenlight the full batch pipeline run across the remaining 17 assets?
