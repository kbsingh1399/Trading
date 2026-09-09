# ==================================================================================================
# INSTITUTIONAL TIME-SERIES FOUNDATION MODEL QUANTITATIVE STRATEGY MASTER PROMPT
# GOOGLE TIMESFM-3 INTEGRATION, VOLATILITY REGIME FORECASTING & 20-QUARTER WALK-FORWARD OOS DESIGN
# ==================================================================================================
# ROLE: LEAD QUANTITATIVE ARCHITECT & MACHINE LEARNING RESEARCH DIRECTOR
# TARGET RUNTIME: AUTONOMOUS QUANTITATIVE CODING AGENT / SPECIALIZED QUANT COUNCIL
# REPOSITORY: https://github.com/kbsingh1399/Trading.git (BRANCH: main)
# REPOSITORY RAW BASE: https://raw.githubusercontent.com/kbsingh1399/Trading/main/
# CAPITAL BASE: 5,000.00 USD (STRICT 4.50% / 225.00 USD HARD DRAWDOWN STOP)
# INSTITUTIONAL UNIVERSE: 11 GENUINE BINANCE USDT-M PERPETUALS (2020-2026)
# ==================================================================================================

====================================================================================================
SECTION 1: MISSION DIRECTIVE & SYSTEM OVERVIEW
====================================================================================================
You are an institutional Lead Quantitative Architect and Algorithmic Trading Systems Engineer.
Your mandate is to evaluate, integrate, benchmark, and deploy Google's open-weights time-series
foundation model — TimesFM 3.0 (`google/timesfm-3.0-pytorch`) — into a high-frequency, microstructure-driven
crypto perpetual trading framework.

The objective is clear:
1. Load and execute TimesFM 3.0 locally via native PyTorch (`timesfm.TimesFM3Forecaster`).
2. Design and deploy production quantitative trading strategies around TimesFM 3.0 that avoid naive
   retail price-prediction traps.
3. Validate all strategies across 20 non-overlapping Out-Of-Sample (OOS) quarterly windows from 2021
   through 2025 under realistic exchange frictions (41.0 bps round-trip taker friction) and strict portfolio
   risk controls.

You will not treat TimesFM 3.0 as an unexamined black box. You must understand where foundation models
provide genuine statistical edge (stationary volatility clustering, multi-horizon orderflow exhaustion,
and dynamic path quantile envelopes) versus where market microstructure and exchange fees destroy naive
directional price-level predictions.

====================================================================================================
SECTION 2: INSTITUTIONAL REPOSITORY & DATASET PROVENANCE
====================================================================================================
All backtesting, data pipelines, schema contracts, and indicator calculations are unified in the master
repository:
- Repository URL: https://github.com/kbsingh1399/Trading.git (branch: main)
- Schema & Universe Definition:
  https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py
- Canonical Mathematical Indicators:
  https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py
- Historical Metrics Data Pipeline:
  https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/pipeline/historical_metrics_processor.py
- Verification Council & Integrity Audits:
  https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py

Dataset Specifications:
1. Certified Genuine Universe (11 Institutional Binance USDT-M Perpetuals):
   `BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH`
   (Note: The 7 synthetic assets SUI, NEAR, AVAX, APT, OP, ARB, PEPE are quarantined due to lack of 2020-2022 depth).
2. Data Granularity:
   - Primary 15-minute bars: 3,467,571 continuous candles across 2020-2026, 0 missing rows, 0 nulls, strictly monotonic.
   - Macro 4-hour bars: 13,178 continuous bars per asset cached in `scratch/cache_4h/`.
3. Orderflow & Microstructure Features:
   - OHLCV + Taker Buy Base Volume, Quote Asset Volume, Number of Trades.
   - Spot CVD, Futures CVD, Spot-Futures CVD Divergence (`spot_cvd_diff3`).
   - Orderflow Imbalance Z-scores (`long_liq_zs`, `short_liq_zs`), Anchored VWAP and VWAP Z-score.
   - Footprint Tick-Level Aggregation: Stacked buy imbalances, stacked sell imbalances, delta ratios.

====================================================================================================
SECTION 3: GOOGLE TIMESFM 3.0 SPECIFICATIONS & FOUNDATION MODEL REALITIES
====================================================================================================
Google TimesFM (Time Series Foundation Model) 3.0 is a decoder-only transformer pretrained on over
100 billion real-world time-series data points spanning finance, energy, weather, and physical systems.

Key Technical Specifications:
- Architecture: Patch-based Transformer Decoder (PatchTST variant).
- Pretrained Weights: `google/timesfm-3.0-pytorch` on Hugging Face (1.26 GB safetensors).
- Context Window: Supports up to 2,048 input time steps.
- Horizon: Efficiently forecasts from 1 to 512 forward steps zero-shot.
- Multi-Quantile Distribution: Produces point forecasts (`output.forecast`) as well as full quantile
  prediction intervals (`output.quantiles`, e.g., 10th, 50th, 90th percentiles).
- Local Execution: Native PyTorch API (`timesfm.TimesFM3Forecaster`), runs locally on CPU and CUDA.

----------------------------------------------------------------------------------------------------
QUANTITATIVE TRUTH: WHERE FOUNDATION MODELS SUCCEED VS WHERE THEY FAIL
----------------------------------------------------------------------------------------------------
1. The Directional Price Trap ($\hat{P}_{t+H}$)
   - Price returns of liquid crypto assets approximate a martingale:
     $$E[R_{t+1} \mid \mathcal{F}_t] \approx 0$$
   - A zero-shot model predicting whether the next bar closes higher or lower achieves at best 50.5% to 52.0%
     directional accuracy.
   - Under real exchange friction of 41.0 bps round-trip, trading raw price forecasts is mathematically
     guaranteed to deplete capital.

2. The Stationary Microstructure Edge
   TimesFM 3.0 must NEVER be deployed to predict raw price levels. Instead, it must forecast
   **stationary, autocorrelated microstructure dynamics**:
   - Volatility Clustering & Expansion ($\hat{\sigma}_{t+H}$): Volatility exhibits persistent long memory.
     TimesFM 3.0 accurately forecasts whether rolling ATR will expand by >30% over the next 6-12 bars,
     identifying volatility breakouts before explosive price moves occur.
   - Orderflow Exhaustion ($\hat{\Delta}_{CVD, t+H}$): Cumulative Volume Delta divergences reflect structural
     inventory imbalances. TimesFM 3.0 forecasts whether aggressive taker momentum will sustain or exhaust.
   - Dynamic Path Quantiles ($\text{Upper\_Band}_{t+H}$, $\text{Lower\_Band}_{t+H}$): Using 10th and 90th
     percentiles to adapt asymmetric targets (+1.35R to +2.50R) and stops to expected price dispersion.

====================================================================================================
SECTION 4: FOUR CONCRETE STRATEGY ARCHITECTURES POWERED BY TIMESFM-3
====================================================================================================

----------------------------------------------------------------------------------------------------
STRATEGY 1: TIMESFM-3 REGIME-GATED VOLATILITY EXPANSION (TFM-VOL)
----------------------------------------------------------------------------------------------------
- Problem Solved: Eliminates the "Narrow Range Friction Trap" where breakout strategies trigger in dormant
  regimes and exchange fees consume 45% of the bar range.
- TimesFM-3 Role: Upstream Volatility Predictor.
  * Input Context: Past 128 bars of rolling normalized ATR:
    $$x_t = \frac{\text{ATR}_{14}(t)}{\text{SMA}(\text{ATR}_{14}, 100)}$$
  * Forecast Horizon: 6 bars forward ($H=6$).
  * Forecast Condition: If TimesFM 3.0 predicts $\hat{x}_{t+6} > 1.30 \times x_t$ (impending +30% volatility
    expansion from a contracted base), arm the Breakout Engine (Sleeve T1).
  * Filter Out Chop: If TimesFM 3.0 predicts $\hat{x}_{t+6} \le 1.05 \times x_t$, veto all breakout trades
    and switch to Mean-Reversion / Liquidity Absorption (Sleeve T2).
- Entry Rules:
  * Long: In an armed expansion regime, bar closes above 20-period Donchian Upper Channel, with positive
    Spot CVD divergence (`zc_div > 0.8`).
  * Short: In an armed expansion regime, bar closes below 20-period Donchian Lower Channel, with negative
    Spot CVD divergence and short liquidation Z-score `< 1.0` (avoiding short squeezes).
- Microstructure Exit Ratchet:
  * Initial Stop: 1.20× ATR.
  * Phase 0 (BE Lock): At +0.80R gain, move stop to Entry +0.20R.
  * Phase 1 (Profit Lock): At +1.50R gain, move stop to Entry +0.80R.
  * Target Exit: +2.20R. Time Decay: 24 bars (6 hours).

----------------------------------------------------------------------------------------------------
STRATEGY 2: TIMESFM-3 ORDERFLOW EXHAUSTION & CASCADE REVERSAL (TFM-CVD)
----------------------------------------------------------------------------------------------------
- Concept: Captures institutional absorption when aggressive market orders fail to push price further.
- TimesFM-3 Role: Spot-Futures Delta Divergence Forecaster.
  * Input Context: Past 96 bars of 3-period Spot CVD divergence (`spot_cvd_diff3`) and Price VWAP Z-score.
  * Forecast Horizon: 4 bars forward ($H=4$).
  * Divergence Condition:
    - Bullish Reversal: Price is making a lower low ($P_t < P_{t-4}$), but TimesFM 3.0 forecasts an upward
      surge in Spot CVD ($\hat{\Delta}_{Spot, t+4} > 0$ and $\hat{\Delta}_{Futures, t+4} < 0$). This forecasts
      that spot accumulation will absorb futures selling.
    - Bearish Reversal: Price is making a higher high, but TimesFM 3.0 forecasts aggressive spot distribution
      while retail chases in futures.
- Entry Trigger:
  * Long: Extreme discount liquidity sweep (Price < Prior Day Low or VWAP Z < -0.8), confirmed by TimesFM 3.0
    bullish divergence forecast.
  * Short: Premium liquidity sweep (Price > Prior Day High or VWAP Z > +0.8), confirmed by TimesFM 3.0 bearish
    divergence forecast.
- Target & Risk:
  * Stop: Low of the sweep candle minus 0.5× ATR.
  * Target: +1.85R (mean reversion back to VWAP).

----------------------------------------------------------------------------------------------------
STRATEGY 3: TIMESFM-3 FOUNDATION EMBEDDINGS + HYBRID GBDT ENSEMBLE (TFM-GBDT)
----------------------------------------------------------------------------------------------------
- Concept: Combines the broad temporal representation of TimesFM 3.0 with the discrete thresholding
  precision of Gradient Boosted Decision Trees (XGBoost + LightGBM).
- Pipeline:
  1. TimesFM 3.0 acts as a Feature Generator:
     - Multi-horizon forecast quantiles for ATR: $\hat{\sigma}_{p10}, \hat{\sigma}_{p50}, \hat{\sigma}_{p90}$.
     - Forecasted expected volatility skew: $\text{Skew} = (\hat{\sigma}_{p90} - \hat{\sigma}_{p50}) / (\hat{\sigma}_{p50} - \hat{\sigma}_{p10})$.
     - Forecasted cumulative delta momentum over 4, 8, and 12 bars.
  2. Downstream GBDT Classifier:
     - Features: TimesFM 3.0 forecasts + Raw Orderflow (`long_liq_zs`, `zc_div`, `spot_cvd_diff3`, `buy_vol_ratio`).
     - Objective: Binary classification predicting whether a trade achieves +1.50R before hitting -1.00R.
     - Training: Strictly causal walk-forward training on past 90 days with 72h purge.
     - Inference: Only execute trades when Blended Probability $> 0.58$.

----------------------------------------------------------------------------------------------------
STRATEGY 4: TIMESFM-3 DYNAMIC ASYMMETRIC QUANTILE EXIT ENVELOPE (TFM-EXIT)
----------------------------------------------------------------------------------------------------
- Concept: Eliminates fixed-R exit bottlenecks. Fixed +2.50R targets truncate runners in trending regimes
  and get stopped out prematurely in choppy regimes.
- TimesFM-3 Role: Dynamic Path Envelope Estimator.
  * For every open trade, TimesFM 3.0 generates 12-bar forward price quantile bands:
    $$\text{Upper Band}_t = \text{TimesFM}_{p90}(P, t+12), \quad \text{Lower Band}_t = \text{TimesFM}_{p10}(P, t+12)$$
  * Dynamic Profit Lock: Exit Long immediately if price exceeds the 90th percentile forecast, or if
    the median forecast (`output.forecast`) begins sloping downward for 2 consecutive bars.

====================================================================================================
SECTION 5: INSTITUTIONAL WALK-FORWARD PROTOCOL (ALL 20 OOS WINDOWS)
====================================================================================================
Every strategy must be evaluated across all 20 canonical non-overlapping Out-Of-Sample (OOS) quarterly
windows spanning five full calendar years (2021-2025):

- Window 1:  2021-01-01 to 2021-03-31 (Q1 2021 - Bull Market Runup)
- Window 2:  2021-04-01 to 2021-06-30 (Q2 2021 - Historic May Crash)
- Window 3:  2021-07-01 to 2021-09-30 (Q3 2021 - Summer Recovery)
- Window 4:  2021-10-01 to 2021-12-31 (Q4 2021 - All-Time Highs & Blowoff)
- Window 5:  2022-01-01 to 2022-03-31 (Q1 2022 - Bear Market Inception)
- Window 6:  2022-04-01 to 2022-06-30 (Q2 2022 - Terra/Luna & 3AC Liquidation Cascade)
- Window 7:  2022-07-01 to 2022-09-30 (Q3 2022 - Mid-Bear Compression)
- Window 8:  2022-10-01 to 2022-12-31 (Q4 2022 - FTX Collapse & Macro Trough)
- Window 9:  2023-01-01 to 2023-03-31 (Q1 2023 - US Banking Crisis & Rebound)
- Window 10: 2023-04-01 to 2023-06-30 (Q2 2023 - Regulatory Summer Chop)
- Window 11: 2023-07-01 to 2023-09-30 (Q3 2023 - Low Volatility Drift)
- Window 12: 2023-10-01 to 2023-12-31 (Q4 2023 - Spot ETF Pre-Approval Momentum)
- Window 13: 2024-01-01 to 2024-03-31 (Q1 2024 - Bitcoin ETF Inflows & ATH Breakout)
- Window 14: 2024-04-01 to 2024-06-30 (Q2 2024 - Post-Halving Grind)
- Window 15: 2024-07-01 to 2024-09-30 (Q3 2024 - August Yen Carry Trade Flush)
- Window 16: 2024-10-01 to 2024-12-31 (Q4 2024 - Global Liquidity Expansion)
- Window 17: 2025-01-01 to 2025-03-31 (Q1 2025 - Institutional Maturation)
- Window 18: 2025-04-01 to 2025-06-30 (Q2 2025 - Mid-Cycle Volatility)
- Window 19: 2025-07-01 to 2025-09-30 (Q3 2025 - Summer Equilibrium)
- Window 20: 2025-10-01 to 2025-12-31 (Q4 2025 - Year-End Expiries)

Pass Criteria per Quarter:
1. Net ROI > +10.00% (+500.00 USD net profit on 5,000.00 USD starting capital).
2. Max Drawdown < 4.50% (225.00 USD hard circuit breaker — ANY window breaching 4.50% is an instant FAIL).
3. Win Rate > 40.0%.
4. Minimum Completed Trades >= 15 per quarter across all 11 assets.
5. Profit Factor >= 1.35.

Execution Frictions & Risk Rules:
- Strict 41.0 bps round-trip taker friction applied to EVERY trade:
  * 8.0 bps taker fee on entry.
  * 10.0 bps adverse slippage on entry market order.
  * 8.0 bps taker fee on exit.
  * 15.0 bps adverse slippage on exit stop/market execution.
- Fixed Portfolio Risk Budget (5,000.00 USD Capital):
  * Base Risk per trade: 35.00 to 45.00 USD (0.70% to 0.90%).
  * Drawdown Defense: Risk drops to 15.00 to 20.00 USD if equity drawdown reaches 2.00% (100.00 USD).
  * House Money: Risk expands to 100.00 to 120.00 USD once net profit exceeds +50.00 USD.
  * Max Concurrent Positions: 2 open trades across all 11 assets simultaneously.
- Zero Lookahead:
  * All TimesFM 3.0 inference runs strictly on information available up to bar $j$ close.
  * Orders execute strictly on bar $j+1$ open.
  * Trailing ratchets take effect on bar $j+1$ only.
  * 72-hour purge ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$) to eliminate state leakage between windows.

====================================================================================================
SECTION 6: VERIFIED PRODUCTION PYTHON ENGINE
====================================================================================================
Below is the verified, native TimesFM 3.0 implementation module using the official PyTorch API:

```python
import os
import time
import numpy as np
import pandas as pd
import timesfm

class TimesFM3QuantEngine:
    def __init__(self, model_name="google/timesfm-3.0-pytorch", device="cpu"):
        print(f"[TimesFM-3] Loading weights from {model_name} onto {device}...")
        t0 = time.time()
        self.forecaster = timesfm.TimesFM3Forecaster.from_pretrained(model_name, device=device)
        print(f"[TimesFM-3] Initialized successfully in {time.time() - t0:.2f}s")
        self.context_len = 128
        self.horizon = 12

    def forecast_volatility_regime(self, atr_series: np.ndarray) -> dict:
        """
        Forecasts forward ATR trajectory and returns expansion metrics.
        """
        if len(atr_series) < self.context_len:
            pad = np.repeat(atr_series[0], self.context_len - len(atr_series))
            atr_series = np.concatenate([pad, atr_series])
        
        ctx = atr_series[-self.context_len:].astype(np.float32)
        # Standardize context to scale-invariant ratio
        mean_val = np.mean(ctx) + 1e-8
        norm_ctx = ctx / mean_val
        
        # Zero-shot forecast using TimesFM 3.0
        output = self.forecaster.predict(norm_ctx, horizon=self.horizon, return_quantiles=True)
        denorm_preds = output.forecast * mean_val
        
        current_atr = atr_series[-1]
        mean_forecast_atr = np.mean(denorm_preds[:6])
        expansion_ratio = mean_forecast_atr / (current_atr + 1e-8)
        
        # Extract 10th and 90th percentile quantile bands
        p10 = output.quantiles[..., 0] * mean_val if output.quantiles is not None else denorm_preds * 0.9
        p90 = output.quantiles[..., -1] * mean_val if output.quantiles is not None else denorm_preds * 1.1
        
        return {
            "current_atr": current_atr,
            "forecast_atr_6b": mean_forecast_atr,
            "expansion_ratio": expansion_ratio,
            "is_expansion": expansion_ratio >= 1.25,
            "is_compression": expansion_ratio <= 0.95,
            "p10_atr": p10,
            "p90_atr": p90
        }

    def forecast_cvd_divergence(self, spot_cvd: np.ndarray, fut_cvd: np.ndarray) -> dict:
        """
        Forecasts spot vs futures orderflow momentum to catch absorption.
        """
        ctx_spot = spot_cvd[-self.context_len:].astype(np.float32)
        ctx_fut = fut_cvd[-self.context_len:].astype(np.float32)
        
        batch_out = list(self.forecaster.predict_batch([ctx_spot, ctx_fut], horizon=4))
        spot_pred = batch_out[0].forecast
        fut_pred = batch_out[1].forecast
        
        spot_slope = spot_pred[-1] - ctx_spot[-1]
        fut_slope = fut_pred[-1] - ctx_fut[-1]
        
        return {
            "predicted_spot_slope": spot_slope,
            "predicted_fut_slope": fut_slope,
            "bullish_absorption": spot_slope > 0 and fut_slope < 0,
            "bearish_distribution": spot_slope < 0 and fut_slope > 0
        }
```

====================================================================================================
SECTION 7: ACTION PLAN & DELIVERABLES
====================================================================================================
Execute the investigation through the following structured milestones:

1. Milestone 1: Zero-Shot Foundation Benchmarking
   - Benchmark inference speed (seconds per 1,000 bars) across CPU and CUDA.
   - Validate whether batching multi-asset series (`[BTC_atr, ETH_atr, SOL_atr, ...]`) reduces per-bar
     latency below 1.5 milliseconds.
   - Evaluate TimesFM 3.0 point forecasts vs quantile bands (p10, p50, p90) on historical Binance 4h data.

2. Milestone 2: Causal Walk-Forward Backtest Across All 20 Quarters
   - Run Strategy 1 (TFM-VOL) and Strategy 3 (TFM-GBDT Hybrid) across all 20 non-overlapping OOS quarters.
   - Compare performance against the baseline (unfiltered Crabel NR7 and baseline GBDT without TimesFM).
   - Log the empirical scorecard for every single quarter: Net ROI (USD), Max Drawdown (%), Win Rate (%),
     Trade Count, and Profit Factor.

3. Milestone 3: Synthesize Findings & Deliver Unified Strategy Engine
   - Synthesize the optimal parameter bounds (horizon $H$, expansion ratio cutoff, GBDT probability gate).
   - Provide the complete, unabridged single-module strategy implementation ready to deploy.
   - Record all architectural conclusions in the system documentation.

====================================================================================================
END OF TIME-SERIES FOUNDATION MODEL QUANTITATIVE SUITE MASTER PROMPT
====================================================================================================
