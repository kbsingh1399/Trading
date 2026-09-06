# ADVERSARIAL PIPELINE & DATA QUALITY AUDIT
## Institutional Quantitative Backtesting Infrastructure — Fault-Finding Brief

---

## MISSION

You are an adversarial senior quant engineer. Your only job is to **find real faults, anomalies, and hidden biases** in this trading data pipeline and its exported datasets. Do not validate. Do not praise. Find problems. If something looks suspicious, call it out with evidence. If something is genuinely clean, say so briefly and move on.

Produce a structured report with:
- **CONFIRMED FAULT** — definitively broken, provable with data/code
- **SUSPECTED ANOMALY** — suspicious, warrants further investigation
- **DESIGN RISK** — not broken but architecturally fragile

---

## SYSTEM CONTEXT

This is a quantitative crypto perpetual trading backtesting pipeline. It downloads Binance futures + spot 15m OHLCV data, computes canonical microstructure indicators, exports dual-table parquets (master + footprint ladder), and runs a 3-agent verification council before exporting.

**The stated goal**: 20 out-of-sample walk-forward windows (2021-2026) on 18 institutional Binance USDT-M perpetuals, with **zero lookahead bias, zero null values, strictly monotonic timestamps**.

---

## ASSET UNIVERSE — READ THIS CAREFULLY

The AGENTS.md strategy invariants declare these **18 target symbols**:
```
BTC, ETH, SOL, BNB, XRP, DOGE, ADA, AVAX, LINK, SUI, NEAR, APT, PEPE, WIF, TIA, ARB, OP, INJ
```

The **actual exported parquet files** in `Engine/binance_backtesting_data/` are:
```
ADA, APT, ARB, AVAX, BCH, BNB, BTC, DOGE, DOT, ETH, LINK, LTC, NEAR, OP, SOL, SUI, TRX, XRP
```

WARNING: The data contains BCH, DOT, LTC, TRX — which are NOT in the strategy universe.
The strategy universe requires PEPE, WIF, TIA, INJ — which are completely absent from the data.
This is a potential blocking fault. Investigate and confirm.

---

## ACTUAL FILE INVENTORY (18 Symbols, 36 Parquets, 18 Manifests)

```
Engine/binance_backtesting_data/
  {SYMBOL}_15m_master_2020_2026.parquet    # 18 files
  {SYMBOL}_15m_footprint_ladder.parquet    # 18 files
  {SYMBOL}_dataset_manifest.json           # 18 files
  verification_report.json                 # 1 file
```

BTC example sizes: master=94.2 MB, ladder=15.0 MB
BTC date range: 2020-09-01 to 2026-09-05 (210,797 bars)

---

## MASTER PARQUET SCHEMA (72 columns, exact order)

```python
CANONICAL_COLUMNS = [
  'open_time_ms', 'close_time_ms', 'datetime_utc', 'symbol',
  'open', 'high', 'low', 'close', 'volume_base', 'volume_quote',
  'volume_sma9', 'trade_count',
  'rsi_14', 'atr_14', 'atr_100',
  'ema_8', 'ema_21', 'ema_50', 'ema_200', 'ema_800',
  'future_cvd_15m', 'future_cvd_session', 'future_cvd_lifetime',
  'spot_cvd_15m', 'spot_cvd_session', 'spot_cvd_lifetime',
  'funding_rate_pct', 'basis_usd',
  'open_interest_k', 'open_interest_usd', 'oi_change_pct',
  'long_liq_usd', 'short_liq_usd',
  'ls_ratio_global', 'ls_ratio_top', 'top_account_ratio',
  'whale_index', 'taker_volume_ratio',
  'fp_delta', 'fp_poc', 'fp_poc_vol_ratio',
  'fp_stacked_buy_imb', 'fp_stacked_sell_imb',
  'session_vah', 'session_val', 'prev_day_vah', 'prev_day_val',
  'taker_buy_count', 'taker_sell_count',
  'taker_buy_vol_btc', 'taker_sell_vol_btc',
  'max_trade_vol_btc', 'avg_trade_size_usd',
  'bid_depth_usd', 'ask_depth_usd', 'bid_depth_coin', 'ask_depth_coin',
  'future_flow_source', 'spot_flow_source', 'poc_source',
  'is_synthetic', 'metrics_available',
  'spot_close',
  'session_vwap', 'vwap_zscore', 'volume_ratio',
  'zc_div', 'long_liq_zs', 'short_liq_zs', 'liq_imbalance_ratio',
  'is_imputed_metrics', 'is_warmup_converged',
]
```

**BTC Live-Probe Facts**:
- Shape: (210,797, 72)
- Null count: 0
- is_imputed_metrics rows: 30,602 (14.5% of total bars)
- 2022 metrics unavailability: **86.56%** of that year is imputed

---

## BTC MANIFEST PROVENANCE (reference for cross-checking)

```json
{
  "tick_exact_bars": 0,
  "spot_exact_bars": 210704,
  "synthetic_bars": 15,
  "metrics_available_bars": 180195,
  "imputed_metrics_bars": 30602,
  "warmup_unconverged_bars": 0,
  "metrics_unavailable_fraction_by_year": {
    "2020": 0.0, "2021": 0.0039, "2022": 0.8656,
    "2023": 0.0001, "2024": 0.0034, "2025": 0.0003, "2026": 0.0
  }
}
```

---

## PIPELINE ARCHITECTURE SUMMARY

`run_historical_pipeline.py` (382 lines) orchestrates per-symbol:

```
1. FETCH     BinanceHistoricalFetcher: futures klines, spot klines, metrics, funding, aggTrades
2. PROCESS   HistoricalMetricsProcessor: 72 canonical causal indicators
3. SLICE     Discard warmup bars AFTER computing indicators (warm-up from 2019/listing date)
4. LADDER    assemble_ladder(): exact tick rungs + causal synthetic rungs
5. COUNCIL   run_council(): 3-agent verify (Continuity, Microstructure, Schema)
             On failure: causal_repair() then re-verify. MAX_REPAIR_ROUNDS = 2.
             Export ONLY on PASS (fail-closed architecture)
6. EXPORT    atomic dual-table Parquet + manifest JSON
```

**Causal repair logic** (lines 119-164):
- nulls/non_finite: forward-fill from prior bar, fill 0 if none exists
- spot_unavailable_zero: zero stale spot delta on UNAVAILABLE bars, recompute session CVD + zc_div
- liq_polarity: enforce long_liq_usd < 0, short_liq_usd > 0
- ladder issues: rebuild full ladder from scratch

---

## SIGNAL CONFLUENCE FORMULA (Strategy Entry — all 6 columns must pass)

```
long_liq_zs > 1.8
AND zc_div > 0.8
AND spot_cvd_15m delta > 0     (spot buying pressure)
AND future_cvd_15m delta < 0   (futures selling pressure)
AND rsi_14 < 40
AND vwap_zscore < -0.5
```

Any lookahead bias or imputation contamination in these 6 columns directly corrupts all backtest results.

---

## 27 ADVERSARIAL AUDIT TASKS

### A. SYMBOL UNIVERSE INTEGRITY

**Task 1.** Confirm the mismatch: data has BCH/DOT/LTC/TRX but strategy needs PEPE/WIF/TIA/INJ. Is this intentional? Check Engine/core/schema.py SYMBOLS list. Does it match AGENTS.md? Are there three conflicting universe definitions?

**Task 2.** Are the BCH/DOT/LTC/TRX parquets genuinely unusable dead data, or is AGENTS.md outdated and these ARE the correct 18 symbols?

**Task 3.** If the AGENTS.md universe is correct, PEPE, WIF, TIA, INJ have no parquets. The backtest cannot run on them. This is a blocking fault.

---

### B. LOOKAHEAD BIAS IN DERIVED FEATURES

**Task 4.** session_vwap: does the session reset at midnight UTC? Is bar t computed using only bars 0..t of that day, or the full day total? Full-day VWAP = pure lookahead.

**Task 5.** vwap_zscore: what rolling window? If it uses a centered window (bars t-N/2 to t+N/2) instead of trailing (bars t-N to t), that is lookahead.

**Task 6.** long_liq_zs / short_liq_zs: what is the lookback window for mean/std? Rolling trailing window using only past data, or computed over the full dataset?

**Task 7.** zc_div = spot_cvd_15m minus future_cvd_15m. Confirm this is a per-bar subtraction, not a multi-bar average that bleeds future bars.

**Task 8.** future_cvd_session / spot_cvd_session: does the cumsum reset to 0 at the FIRST bar of each new session, or carry over from prior session? Carryover is not lookahead but is an incorrect session boundary.

**Task 9.** volume_ratio: trailing 9-bar SMA (fine) or centered SMA including future bars (lookahead)?

**Task 10.** ema_800: with warmup from 2019, is it genuinely converged by 2020-09-01? The manifest says warmup_unconverged_bars=0 but this flag could be set by logic that never actually checks convergence.

---

### C. IMPUTATION INTEGRITY

**Task 11.** For is_imputed_metrics=1 bars: what exact values do long_liq_usd, short_liq_usd, open_interest_usd, ls_ratio_global carry? Forward-fill from prior bar, or zeroed?

**Task 12.** The strategy signal uses long_liq_zs > 1.8. If forward-filled from a real liquidation spike, imputed bars days later could trigger false signals. Quantify: how many signal triggers occur on imputed bars vs. valid bars?

**Task 13.** 2022 has 86.56% imputed bars for BTC. Walk-forward windows W5 (Q1 2022) and W6 (Q2 2022) are almost entirely imputed data. Does the strategy explicitly skip trading on is_imputed_metrics=1 bars? If not, W5/W6 results are noise.

**Task 14.** When spot_flow_source=UNAVAILABLE, what is future_flow_source? If both are simultaneously unavailable, the repair sets zc_div = 0 - stale_future, producing a spurious non-zero divergence signal.

---

### D. FOOTPRINT LADDER INTEGRITY

**Task 15.** BTC manifest: tick_exact_candles=0, synthetic_candles=210,797. The entire ladder is synthetic — zero real aggTrade data. If the strategy uses fp_delta, fp_poc, fp_stacked_buy_imb etc., it is trading on made-up microstructure. Is this a known and accepted limitation?

**Task 16.** Synthetic rung generation: does it use bar t+1 data (next bar open/close) to retroactively set bar t rung levels? That would be a single-bar lookahead in footprint features.

**Task 17.** The fast-skip check verifies all master timestamps exist in ladder (np.isin direction). It does NOT verify the reverse. Orphaned ladder rows for non-existent master bars would pass silently.

---

### E. PIPELINE LOGIC FLAWS

**Task 18.** Fast-skip race condition: if a parquet write is interrupted after manifest write (manifest says PASS) but before the parquet is complete, skip logic trusts a corrupt file. Is the export atomic (write to temp file then rename)?

**Task 19.** MAX_REPAIR_ROUNDS=2: after 2 failed repair rounds, what happens? Exports anyway (dangerous), skips silently (silent data loss), or raises a hard error?

**Task 20.** liq_polarity repair sets long_liq_usd = -abs(long_liq_usd) (negative values). Does long_liq_zs z-score computation correctly handle negative inputs, or does it produce inverted signals?

**Task 21.** existing_output_is_current computes age using wall-clock time vs last close_time_ms. Clock drift, NTP correction, or DST changes corrupt this comparison.

---

### F. CROSS-SYMBOL CONSISTENCY

**Task 22.** For symbols with different listing dates (BTC 2019, SUI 2023, NEAR 2020), verify is_warmup_converged is actually False for early bars. An always-True flag masks indicator instability in the first 800 bars.

**Task 23.** Do all 18 parquets have identical column ordering? Any code that reads by column index (not name) would silently read wrong values if ordering varies.

**Task 24.** oi_change_pct at listing: prior OI=0 causes division by zero. Verify it is handled, not NaN.

---

### G. DATA INTEGRITY EDGE CASES

**Task 25.** Verify close_time_ms = open_time_ms + 900000 - 1 for every row of every parquet. Any deviation indicates a gap fill, shard merge error, or timezone boundary issue.

**Task 26.** Verify the warmup slice uses >= 2020-09-01 (inclusive), not > 2020-09-01 (which silently drops the first bar).

**Task 27.** funding_rate_pct is published every 8 hours on Binance. For the 31 non-event 15m bars between each publication, what value is stored? Forward-fill of last known rate? Zero? Misrepresentation biases P&L.

---

## DELIVERABLE FORMAT

```
FINDING #N
Type: CONFIRMED FAULT | SUSPECTED ANOMALY | DESIGN RISK
Location: <file / column / line reference>
Description: <what is wrong>
Evidence: <data or code excerpt>
Impact: <how this corrupts backtest validity>
Fix: <correct behavior>
```

---

## PYTHON PROBE SNIPPETS (copy-paste ready)

```python
import pandas as pd, numpy as np

df = pd.read_parquet("Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet")

# Task 25: bar spacing
gaps = df['open_time_ms'].diff().dropna()
print("Non-standard gaps:", (gaps != 900_000).sum())
print("Gap counts:", gaps.value_counts().head(5))

# Task 4: session_vwap causality
df['day'] = df['open_time_ms'] // 86_400_000
df['expected_vwap'] = (
    df.groupby('day', group_keys=False)
    .apply(lambda g: (g['close'] * g['volume_base']).cumsum() / g['volume_base'].cumsum())
)
mismatch = (df['session_vwap'] - df['expected_vwap']).abs() > 1e-6
print("session_vwap lookahead mismatches:", mismatch.sum())

# Task 12: signals on imputed bars
signal = (
    (df['long_liq_zs'] > 1.8) & (df['zc_div'] > 0.8) &
    (df['rsi_14'] < 40) & (df['vwap_zscore'] < -0.5)
)
imputed_signals = signal & (df['is_imputed_metrics'] == 1)
print("Total signals:", signal.sum())
print("Imputed signals:", imputed_signals.sum())
print("Imputed signal pct:", round(imputed_signals.sum() / signal.sum() * 100, 1), "%")

# Task 13: 2022 imputation depth
y2022 = df[df['open_time_ms'].between(1640995200000, 1672531199000)]
print("2022 imputed pct:", round(y2022['is_imputed_metrics'].mean() * 100, 1), "%")

# Task 20: liq polarity
print("long_liq_usd range:", df['long_liq_usd'].min(), "to", df['long_liq_usd'].max())
print("short_liq_usd range:", df['short_liq_usd'].min(), "to", df['short_liq_usd'].max())

# Task 25: close_time_ms
bad_close = (df['close_time_ms'] != df['open_time_ms'] + 899_999).sum()
print("close_time_ms violations:", bad_close)
```

---

*Generated 2026-09-06 from live data probes. All column names, filenames, row counts, and statistics are exact production values.*
