# OPUS 5 MASTER DIRECTIVE: BUILD & WALK-FORWARD CONQUER ALL 20 OOS WINDOWS WITH CAUSAL ML OVERLAY

Opus, the target criteria in `Engine/target_oos_criteria.json` on GitHub (`kbsingh1399/Engine` commit `1a7f34c`) has been updated by the lead trader to institutional standards:
- **Min ROI per 1-Month Window**: `> +20.0%`
- **Max Drawdown**: `< 5.0%` (Hard circuit-breaker stop at `4.5%` / `$225` on `$5,000` capital)
- **Min Win Rate**: `> 40.0%`
- **Min Target R-Multiple**: `>= 4.0R` (Primary setups must aim for >= 4R payoff!)
- **Min Trades per Window**: `>= 15 trades` (Increased from 6 to 15 to ensure statistical significance!)
- **Universe**: 18 Binance USDT-M Perpetuals (3.47M 15m bars, 2020–2026)
- **Institutional Frictions**: Strict 33 bps round-trip (8 bps maker/taker fee in/out, 10 bps entry slippage, 15 bps stop slippage).

---

## 1. Why Static Rule Sets Hit a Ceiling & The ML Imperative
In Round 8 (`rp2_round8_convex_liquidation_leadlag.py`), you proved the execution physics:
- **Win Rate**: `58.06%` (18 wins / 31 trades) under full 33 bps frictions.
- **Capital Defense**: Max Drawdown held at `3.20%` during Bitcoin's violent 50% crash in May 2021.
- **The Failure Vector**: `liq_exhaust` took 0 trades because static thresholds (`oi_collapse_1h <= -0.10`, `liq_z >= 2.0`, `hl3 >= 2/3`) are brittle across shifting market regimes. Meanwhile, `funding_squeeze` produced a negative ROI (-2.16%) because winning trades were cut at ~1.15R while stop-outs took -1.0R.

To reliably clear **+20% ROI at <5% MaxDD with >=15 trades and >=4.0R targets across ALL 20 OOS windows**, you must now integrate **Adaptive Machine Learning Techniques**.

---

## 2. GitHub Assets Available to You via GitHub MCP
You have direct read/write access via GitHub MCP to `https://github.com/kbsingh1399/Engine`:
1. `Engine/target_oos_criteria.json`: Updated criteria (20% ROI, 5% DD, 40% WR, 4R target, 15 trades).
2. `Engine/oos_windows_20.json`: Canonical 20 windows (W01 May-2021 to W20 Mar-2026).
3. `Engine/strategy/rp2_round8_convex_liquidation_leadlag.py`: Your working Round 8 engine baseline.
4. `skills/`: **1,303 flattened institutional skill files** in `.md` format! Pull whatever you need directly:
   - `skills/training-machine-learning-models.md`
   - `skills/engineering-features-for-machine-learning.md`
   - `skills/evaluating-machine-learning-models.md`
   - `skills/agent-data-ml-model.md`
   - `skills/ml-best-practices.md`
   - `skills/building-automl-pipelines.md`

---

## 3. Mandatory ML Architecture & Engineering Directives

### A. Event-Conditioned Sampling & Meta-Labeling (Triple-Barrier Method)
- **Do NOT model generic 15m noise**: Trying to predict every 15m bar yields random AUC (~0.501).
- **Condition on Volatility & Structural Dislocation**: Sample candidate trade entries ONLY when:
  $$	ext{long\_liq\_zs} \ge 1.5 \quad \lor \quad |	ext{funding\_annualized}| \ge 50\% \quad \lor \quad |	ext{lead\_impulse\_z}| \ge 1.8 \quad \lor \quad 	ext{volume\_z} \ge 2.0$$
- **Triple-Barrier Horizon**: Label candidate events by whether price reaches **+4.0R** before hitting **-1.0R** or expiring after **24 bars (6 hours)**.

### B. Machine Learning Classifiers
- Train an adaptive causal classifier (e.g. Ridge Logistic Ensemble, LightGBM/XGBoost, or regularized shallow tree classifier):
  - `max_depth <= 4`, `min_samples_leaf >= 20` to prevent overfitting.
  - Strong L1/L2 regularization (`reg_alpha >= 1.0`, `reg_lambda >= 3.0`).
  - Calibrated probability output: Trade only when model confidence $P(	ext{Hit } +4.0	ext{R}) \ge p^*_{	ext{dynamic}}$.

### C. Feature Engineering (Stationary & Microstructure)
- Stationary transformations only:
  - Z-scores of liquidation impulses (`long_liq_zs`, `short_liq_zs`).
  - Multi-horizon Open Interest collapse: 1h, 4h, and 12h percentage delta (`oi_delta_1h`, `oi_delta_4h`).
  - Funding rate spread and velocity: `funding_rate - rolling_mean(funding_rate, 24)`.
  - Lead-Lag cross-asset spillover: Alt lag ratio against BTC/ETH impulse.
  - Normalized candle geometry: Reclaim ratio `(close - low) / (high - low + 1e-9)`, body-to-range ratio.

### D. Asymmetric Payoff Geometry (Target >= 4.0R)
- **Stop**: Placed at flush extreme $\mp 0.20 	imes 	ext{ATR}_{14}$.
- **Target**: Set to **4.0R** (or 6.0R on extreme liquidation cascades).
- **Anti-Retracement Microstructure Ratchet**:
  - Gain $\ge +0.8	ext{R} 	o$ Stop moved to Entry $+0.15	ext{R}$ (Breakeven Lock).
  - Gain $\ge +1.5	ext{R} 	o$ Stop moved to Entry $+0.80	ext{R}$ (Profit Lock).
  - Gain $\ge +2.5	ext{R} 	o$ Stop moved to Entry $+2.00	ext{R}$.
  - Time decay: If price $< +0.2	ext{R}$ after 24 bars (6 hours), exit at market.

### E. Dynamic House-Money / Non-linear Position Sizing
- Base Risk: `$25.00` (0.50% of `$5,000`).
- House Money Sizing: $	ext{Risk} = \$25 + 0.35 	imes \max(0, 	ext{Realized Profit})$, capped at `$200`.
- Hard Capital Protection Floor: Never risk capital if $	ext{Equity} - 	ext{Open Risk} \le \$4,775$ (4.5% drawdown limit).
- Max 2 concurrent open positions across all 18 symbols.

---

## 4. The 20-Window Walk-Forward Execution Protocol
1. **Strictly Causal Sequential Training**:
   - For Window $k$, train the ML model and fit thresholds strictly on in-sample data prior to Window $k$ with a **72-hour purge** ($t \le t_{	ext{start}} - 72	ext{h}$).
2. **Immediate Fail-Fast Halt**:
   - If Window $k$ fails ANY criteria (ROI < 20.0%, MaxDD >= 5.0%, WR < 40.0%, Trades < 15, R < 4.0):
   - **Immediately halt at Window $k$**. Diagnose the exact failure mode (low trade count, regime mismatch, stop geometry).
   - Causally adapt parameters / retrain strictly on $t < t_{	ext{start}} - 72	ext{h}$.
   - Re-test Window $k$ and verify windows $1 \dots k-1$ do not regress before advancing to $k+1$.
3. **Target Deliverable**:
   - Deliver the complete, drop-in Python script `rp2_round9_ml_convex_engine.py` (or update `rp2_round8_convex_liquidation_leadlag.py`).
   - Standard numpy/pandas/scipy/sklearn only (zero exotic dependencies).
   - Execute the walk-forward simulation across all 20 windows and present the consolidated 20-window scorecard.

Opus, the repository is ready. Build the ML-driven convex engine, run the causal walk-forward loop, and let's conquer all 20 windows!
