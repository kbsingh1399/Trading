# ASTRA AI PROMPT: PRINT FULL UNABRIDGED SOURCE CODE IN CHAT
**From:** Antigravity Quant Desk  
**To:** Astra AI (Azure Data Explorer / Kusto Specialist)  
**Subject:** Print Full Source Code Directly in Chat (No ZIP / No Sandbox Links)  
**Target Path:** `C:\Users\SIGMA\Downloads\Astra_Request_Code_In_Chat.txt`

---

## 1. Directive & Delivery Method

Astra, do **NOT** package or deliver a ZIP file or sandbox download links. Sandbox links can expire or fail across sessions.

**Print the full, unabridged, copy-paste-ready source code for all components directly in your chat response inside markdown code blocks.**

---

## 2. Unabridged Components Required

Please output the complete code for the following three files in sequence:

### Component 1: `orderflow_production_engine.py`
Must be completely self-contained and ready to run:
- **Numba Simulation Loop (`fast_numba_simulation`)**:
  * Correct variable scoping: `stop_next = 0.0` and `armed_phase0 = armed_phase1 = False` reset at the top of each trade.
  * Causal Bar $j+1$ Ratchet Progression: Ratchet triggers armed on bar $j$ close take effect strictly at bar $j+1$ open.
  * Explicit `break` on time decay exit (at bar 24).
  * Global Portfolio Concurrency Governor: Maximum 2 concurrent open positions across all 18 perpetual symbols.
- **Dynamic Risk Distance Floor**:
  * `risk_distance = max(atr_14, entry * 0.012)` to prevent ATR compression from creating oversized notional.
  * Size bounded by total loss distance including the 41 bps friction.
- **Footprint Ladder Integration**:
  * Ingestion and join from `Binance_Footprint_15min` on `open_time_ms` requiring `is_stacked_buy_imb >= 1`.
  * Combined with `volume_ratio >= 1.20`.

### Component 2: `orderflow_ml_overlay.py`
Must contain the complete ready-to-train causal walk-forward ML pipeline:
- **Stationary Feature Matrix**:
  * Extraction of `[zc_div, long_liq_zs, short_liq_zs, vwap_zscore, volume_ratio, rsi_14, spot_cvd_15m]`.
- **Causal Forward-Horizon Labeler (Zero Lookahead)**:
  * For every candidate bar $t$: simulate forward path between $t+1$ and $t+25$.
  * Label $y = 1$ if path reaches $+2.50\text{R}$ before hitting $-1.00\text{R}$ stop or 24-bar decay (net of 41 bps friction).
  * Label $y = 0$ otherwise.
- **Walk-Forward In-Sample Training**:
  * Causal 72-hour quarantine purge ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$) before any evaluation window.
  * Model: `GradientBoostingClassifier(n_estimators=200, max_depth=4)`.
- **Probability Gating**:
  * `gate_signals(df, threshold=0.55)` method to suppress false liquidity flushes.

### Component 3: `config.yaml`
- Synchronized configuration with capital (5,000 USD), base risk (40 USD), friction (0.0041), max concurrent (2), ratchet levels (+0.8R BE lock, +1.8R lock, +3.0R TP), and symbol universe.

---

## 3. Strict Formatting Mandate
- **No Truncation**: Never write `# ... rest of function remains same ...` or `# ... implement here ...`. Output 100% of the working code.
- **Clean Imports & Type Hints**: Standard Python libraries (Polars, NumPy, Numba, Scikit-Learn, PyYAML).
