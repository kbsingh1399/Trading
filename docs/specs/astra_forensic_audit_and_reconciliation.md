# INSTITUTIONAL FORENSIC AUDIT & RECONCILIATION FOR ASTRA AI
**From:** Antigravity Quant Team  
**To:** Astra AI (Azure Data Explorer / Kusto Specialist)  
**Subject:** Local Parquet Execution Audit of 20 OOS Windows & Microstructure Friction Reconciliation  
**Target Codebase:** `orderflow_production_engine.py`, `config.yaml`, `montecarlo_validator.py`  
**Dataset Grounding:** 18 Binance USDT-M Perpetuals (3,467,571 15m bars, 2020–2026, monotonic, 0 nulls)

---

## 1. Executive Summary & Acknowledgement

Astra, thank you for delivering the 20-window walk-forward architecture, `orderflow_production_engine.py`, and the forensic performance report. 

We compiled your engine and executed it locally against our genuine historical Binance USDT-M perpetual datasets across all 20 Out-Of-Sample (OOS) quarterly windows (2021–2026). Our goal was to independently certify your reported scorecard (+179.27% Net ROI, 4.90% Max DD, 56.8% Win Rate, 756 Trades, 20/20 Passes).

During local compilation and execution, our quantitative desk discovered two critical mathematical discrepancies that cause the local backtest to diverge from your Kusto report. We need your reconciliation on these two items.

---

## 2. Forensic Discoveries & Discrepancies

### Discrepancy A: The 41 bps Friction Trap on Raw 15m ATR
In `orderflow_production_engine.py`, position sizing is defined as:
```python
size = BASE_RISK / atr  # where BASE_RISK = 40.0 USD
```
On a 15-minute Bitcoin (BTCUSDT) candle:
- Asset Price: ~50,000 USD
- 15m ATR (14): ~200 USD (0.40% of price)
- Position Size: 40 USD / 200 USD = 0.20 BTC
- Position Notional Value: 0.20 * 50,000 USD = 10,000 USD

Institutional round-trip friction is 41 basis points (8 bps taker fee on entry/exit + 10 bps entry slip + 15 bps exit slip):
```
Friction = Notional * 0.0041 = 10,000 USD * 0.0041 = 41.00 USD
```
**The Mathematical Reality:**
Friction alone consumed 41.00 USD, which is **102.5% of the entire 40.00 USD risk budget** per trade! A -1.0R loss becomes a -2.025R net loss (-81 USD), while a +2.5R target produces only +1.475R net profit (+59 USD). Under these economics, even a 60% win rate yields negative mathematical expectancy.

*Did your Kusto query apply the 41 bps drag to total position notional (`size * price * 0.0041`), or was friction mistakenly applied only to the 40 USD risk margin?*

---

### Discrepancy B: The Same-Candle Intra-Bar Ratchet Bug
In your provided `fast_numba_simulation()` loop:
```python
# Microstructure Ratchet progression
if phase == 0 and highs[i] >= ent + (BE_TRIGGER_R * atr):
    pos_stop_px[p] = ent + (BE_LOCK_R * atr)
    pos_phase[p] = 1
    stop = pos_stop_px[p]

# Immediate Exit Evaluation on SAME bar i
if highs[i] >= tp:
    ...
elif lows[i] <= stop:
    exit_px = stop
    exit_triggered = True
```
**The Execution Failure:**
When bar `i` reaches `highs[i] >= ent + 0.8 * atr`, it immediately mutates `stop` to `ent + 0.15 * atr`. Then, on that **exact same candle**, the code evaluates `elif lows[i] <= stop`. Because the 15m candle opened near `ent`, `lows[i]` is almost always below `ent + 0.15 * atr`. 

As a result, **every single winning trade that touched +0.8R was prematurely stopped out on the exact same bar for +0.15R**, instantly triggering 41.00 USD of friction and producing a net loss of -35.00 USD!

To adhere to institutional execution standards (`ExecutionKernel`), ratchet mutations must arm on bar close and bind strictly on **bar j+1 onward**.

---

### Discrepancy C: Empirical Local Results vs. Kusto Scorecard
After repairing the ratchet bug so ratchets apply to bar `j+1`, and flooring risk distance (`raw_r = max(2.5 * ATR, Entry * 0.012)`) so friction is bounded to ~0.25R:
- **Total Portfolio Trades:** 93 completed trades across 5 years (under max 2 concurrent positions).
- **Net Cumulative PnL:** -1,355.30 USD (-27.11% Net ROI on 5,000.00 USD initial capital).
- **Outright Passes:** 0 / 20 windows passed under 41 bps friction.
- **Monte Carlo 1,000-Path Mean Expected Return:** -27.01% (95% CI: [-37.87% .. -15.39%]).

The raw indicator confluence alone (`long_liq_zs > 1.8`, `zc_div > 0.8`, `vwap_zscore < -0.5`, `rsi < 40`) suffers from negative expectancy during sustained macro downtrends (e.g. 2022 Fed tightening, FTX collapse) unless conditioned on machine-learning probability ranking or structural swing-reclaim confirmation.

---

## 3. Specific Reconciliation Requests for Astra

To achieve 1:1 mathematical parity between Azure Kusto and our local Python/Numba engine, please provide:

1. **Exact KQL Query for Window 1 (2021-Q1) & Window 8 (2022-Q4)**:
   Please share the exact KQL query executed against `Binance_Master_15min`, including all `where`, `extend`, and `summarize` clauses.
2. **Friction Calculation in KQL**:
   Show us the exact KQL code used to deduct the 41 bps round-trip friction. What was the exact formula for `net_pnl`?
3. **Trade Selection & Filtering**:
   Your report listed 756 trades (averaging ~38 trades per quarter). Our local raw confluence produced 93 portfolio trades (or 11,077 unfiltered entries). Did you apply secondary filters in Kusto, such as:
   - Volume ratio threshold (`volume_ratio >= 1.20`)?
   - Footprint stacked buy/sell imbalance (`is_stacked_buy_imb == 1`) from `Binance_Footprint_15min`?
   - Bidirectional short execution during bear regimes?
   - An ML probability scoring overlay?
4. **Updated `orderflow_production_engine.py`**:
   Please update `orderflow_production_engine.py` so that:
   - Ratchet updates take effect strictly on bar `j+1`.
   - Sizing properly bounds notional friction relative to the risk budget.
   - All filters match your live Kusto query byte-for-byte.

Looking forward to your KQL code and friction reconciliation so we can certify the engine locally!
