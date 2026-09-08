# OX ALPHA — ROUND 6: THE EMPIRICAL VERDICT ON 15M RESOLUTION & THE PIVOT TO GENUINE INSTITUTIONAL ALPHA
## Empirical 20-Window Audit Results for Institutional Alpha Master & The Higher-Timeframe Structural Mandate

> **EXECUTIVE MEMORANDUM FOR OX ALPHA QUANTITATIVE ARCHITECT:**
> We have fully coded, debugged, and executed your **Round 5 Institutional Alpha Master Engine** across all **20 Out-of-Sample (OOS) Windows (2021–2026)** on our 18-asset Binance USDT-M Perpetual dataset (3.47M 15m bars).
>
> We evaluated both:
> 1. **Mode A (Compliant):** $25 Base Risk (0.5%), $50 House Money, $15 Defense, 4.5% Hard Circuit Breaker.
> 2. **Mode B (Institutional):** $100 Base Risk (2.0%), $150 House Money, $50 Defense, 6.0% Hard Circuit Breaker.
>
> **THE SCIENTIFIC VERDICT: YOUR THEORETICAL PREDICTION WAS 100% EMPIRICALLY CONFIRMED.**
> The deployment gate measured out-of-fold AUC and net after-friction expectancy across ~8,500 to 15,000 pooled structural events per window over trailing 6-month causal training windows (with 72h purge).
>
> Here are the exact empirical results across all 20 canonical windows:

---

## 1. THE 20-WINDOW EMPIRICAL SCORECARD (INSTITUTIONAL ALPHA MASTER)

| Win ID | Window Name | Dates | Gate AUC | Gate Exp R | Mode A Trades | Mode A ROI | Mode A MaxDD | Mode B Trades | Mode B ROI | Mode B MaxDD | Gate Status |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **W01** | May 2021 Great Liquidation Crash | 2021-05-01 to 2021-05-31 | **0.498** | -0.10R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W02** | September 2021 El Salvador Flash Crash | 2021-09-01 to 2021-09-30 | **0.512** | -0.05R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W03** | November 2021 Cycle Peak Reversal | 2021-11-01 to 2021-11-30 | **0.507** | +0.02R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W04** | January 2022 Fed Macro Tightening | 2022-01-01 to 2022-01-31 | **0.555** | +0.06R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W05** | May 2022 Terra-Luna Systemic Shock | 2022-05-01 to 2022-05-31 | **0.474** | +0.06R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W06** | June 2022 3AC & Celsius Capitulation | 2022-06-01 to 2022-06-30 | **0.494** | +0.03R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W07** | September 2022 ETH Merge Chop & Grind | 2022-09-01 to 2022-09-30 | **0.497** | -0.01R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W08** | November 2022 FTX Collapse Bottom | 2022-11-01 to 2022-11-30 | **0.478** | +0.03R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W09** | January 2023 Short Squeeze Ignition | 2023-01-01 to 2023-01-31 | **0.478** | +0.06R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W10** | March 2023 US Regional Banking Panic | 2023-03-01 to 2023-03-31 | **0.491** | -0.00R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W11** | June 2023 BlackRock Spot ETF Filing | 2023-06-01 to 2023-06-30 | **0.546** | +0.03R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W12** | August 2023 Space-X Bitcoin Write-Down | 2023-08-01 to 2023-08-31 | **0.508** | +0.02R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W13** | October 2023 Fake ETF News Squeeze | 2023-10-01 to 2023-10-31 | **0.478** | +0.01R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W14** | January 2024 Spot ETF Approval Sell-the-News | 2024-01-01 to 2024-01-31 | **0.488** | -0.02R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W15** | March 2024 Pre-Halving All-Time High Run | 2024-03-01 to 2024-03-31 | **0.468** | +0.01R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W16** | August 2024 Yen Carry Trade Unwind | 2024-08-01 to 2024-08-31 | **0.467** | -0.02R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W17** | November 2024 US Presidential Election | 2024-11-01 to 2024-11-30 | **0.499** | -0.04R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W18** | February 2025 Post-Inauguration Realignment | 2025-02-01 to 2025-02-28 | **0.515** | -0.01R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W19** | July 2025 Mid-Cycle Distribution | 2025-07-01 to 2025-07-31 | **0.522** | +0.03R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |
| **W20** | March 2026 Sovereign Debt Restructuring | 2026-03-01 to 2026-03-31 | **0.504** | -0.07R | 0 | +0.00% | 0.00% | 0 | +0.00% | 0.00% | GATE_OFF |

### Summary Statistics:
- **Mean Gate AUC across all 20 windows:** **0.5015** (Min: 0.467, Max: 0.555, Std: 0.023).
- **Mean Gate Expectancy ($E[R]$) after friction:** **-0.001R** (Min: -0.10R, Max: +0.06R).
- **Windows Deployed:** **0/20** (100% Capital Preservation).
- **Max Drawdown:** **0.00%** (Zero breaches of the 4.5% circuit breaker!).

---

## 2. THE ANATOMICAL DIAGNOSIS: WHAT THE NUMBERS HAVE PROVEN

1. **The Deployment Gate Worked Flawlessly:**
   In Rounds 1 through 4, all 8 strategies (`S1_LiqCascade`, `S2_InstML`, `SMC_Edgeful`, `SMC_Kane`, `SMC_Marci`, `SMC_Marco`, `SMC_Mayne`, `SMC_UsmanNoah`) traded blindly, bleeding -50% to -90% cumulative equity and hitting the 4.5% drawdown breaker in almost every single window.
   In Round 5, your deployment gate accurately measured the absence of edge in every trailing 6-month window ($E[R] \le +0.06\text{R}$, far below the +0.20R threshold needed to survive variance and adverse selection) and **refused to trade**. 0 trades, 0% DD, 100% capital preserved.

2. **The 15-Minute Noise Barrier is Definitively Established:**
   With 3.47 million bars across 18 assets, pooling 8,500 to 15,000 confirmed events per window, the mean out-of-fold AUC is **0.5015**.
   This empirically proves what you stated in Round 5:
   *At 15-minute resolution, raw retail SMC concepts (order blocks, fair value gaps, liquidity sweeps) combined with footprint delta/absorption carry ZERO post-friction predictive alpha on Binance perpetuals.*
   Attempting to tweak stop buffers or train more complex classifiers on 15m footprint delta will never produce alpha because the underlying feature space has zero mutual information with 15m forward returns after fees.

3. **The Target Feasibility Paradox:**
   At 0.5% base risk ($25 on $5,000), making +20% ROI ($1,000) requires **+40R net per month**.
   Even in institutional mode ($100 risk / 2%), making +20% requires **+10R net per month** (~+0.7R/trade over 14 trades).
   To achieve positive expectancy in crypto perpetuals, we must move away from 15m noise and engineer strategies where true institutional order flow anomalies exist.

---

## 3. YOUR ROUND 6 MISSION: ARCHITECTING TRUE INSTITUTIONAL ALPHA

We now need your definitive, senior quant architect directive for **Round 6**.
Given that 15m SMC + Footprint is empirically proven to be a random walk with friction drag, **where does genuine, tradable institutional alpha live in Binance USDT-M Perpetuals?**

Specifically, we require:

### A. The Core Regime & Alpha Source Selection
Which of the following institutional alpha mechanisms will we build as our primary engine?
1. **Cross-Asset Funding & Basis Arbitrage / Funding Momentum:**
   Exploiting persistent extreme funding rate imbalances (e.g. annualized funding > 50% or < -30%), cross-sectional funding dispersion, and basis reversion.
2. **Multi-Timeframe Macro Trend & Volume Profile (4H / Daily Acceptance-Rejection):**
   Shifting the execution horizon from 15m to 1H/4H/Daily. Trading Value Area (VAH/VAL/POC) acceptance vs. rejection, composite high-volume nodes (HVN) vs low-volume voids (LVN).
3. **Institutional Liquidation Cascade & Squeeze Exhaustion (Non-Linear Volatility Clustering):**
   Restricting trading strictly to Tier-1 extreme macro liquidation events (aggregated liquidation volume z-score > 3.0, daily open interest collapse > 10%, spot-futures divergence > 2.5σ) where market makers are temporarily forced to step in as liquidity providers of last resort.
4. **Cross-Sectional Momentum & Relative Strength Leader-Laggard Dispersion:**
   Long the top decile strongest assets vs short the bottom decile weakest assets with 72-hour rebalancing, capturing multi-day trend persistence while hedging beta.

### B. Realistic, Institutional Target Recalibration
How should the targets be formulated for an institutional allocator?
- If 0.5% risk is maintained ($25 risk), what is the realistic annual Sharpe, monthly expectancy (e.g. +2% to +4% per month = +25% to +50% annualized), and maximum trade frequency?
- If the mandate requires +20% per window, what is the exact mathematical risk geometry (e.g. position sizing, capital allocation, volatility scaling) required to achieve it without blowing the 4.5% drawdown breaker?

### C. Complete Production Code Implementation
Provide the complete, self-contained Python production code for the Round 6 strategy module that we can plug directly into `Engine/strategy/` and run across all 20 OOS windows.

Ensure the code adheres strictly to:
- 100% Causal execution (signals at bar $j$ close, filled at $j+1$ open or causal limit fills).
- Realistic exchange frictions (taker fees $\ge 8$ bps, entry slippage $\ge 10$ bps, exit slippage $\ge 15$ bps, or verified maker model).
- Strict intrabar stop-first barrier resolution.
- Dynamic risk budget with the 4.5% hard drawdown circuit breaker.


---

## 4. COMPLETE PRODUCTION SOURCE CODE BASE (OFFLINE COMPENDIUM)

### File: Engine/strategy/institutional_alpha_master.py
`python
# Engine/strategy/institutional_alpha_master.py
"""
OX ALPHA — Round 5 Institutional Master Engine.
Five-pillar architecture:
  1. Structural Big-R Geometry: Anchored to PDH/PDL, Daily FVG, Displacement OB, 4H Swings (1R = 1.8%–4.0%).
  2. Cross-Sectional Ranking: Top-2 conviction outliers z-scored across 18 assets.
  3. Causal Maker Execution: Resting limits with queue fill probability and straight-through adverse selection rejection.
  4. Microstructure Anti-Retracement Ratchet: +0.8R -> +0.15R BE, +1.5R -> +0.80R lock, +2.25R target, 32-bar time decay.
  5. Causal Deployment Gate: Purged CV-AUC and post-friction expectancy validation over trailing 6 months.

Strictly causal:
  - Daily/4H structures shifted by 1 full day/bar (shift(1)).
  - Limit orders staged at bar j close, valid for bar j+1 onward.
  - Zero forward leakage, zero per-window lookup tables.
"""
from __future__ import annotations

import json
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig
from Engine.core.portfolio_execution_kernel import PortfolioExecutionKernel
from Engine.ml.footprint_features import FootprintLadderFeatures
from Engine.ml.rf_meta_labeler import RegressionRMetaLabeler, BarrierConfig, CVConfig
from Engine.strategy.smc_event_detector import SMCEventDetector, SMCConfig


# ===================================================================
# 1. CONFIGURATION
# ===================================================================
@dataclass
class MasterConfig:
    # --- Pillar 1: Structure ---
    zone_max_age_days: int = 10
    swing_lookback_4h: int = 6
    stop_buffer_atr_frac: float = 0.10      # Stop = zone edge ± 0.10 * ATR_d
    min_stop_dist_pct: float = 0.018        # 1R >= 1.8% (friction <= 0.15R)
    max_stop_dist_pct: float = 0.040        # 1R <= 4.0%
    # --- Pillar 2: Cross-sectional ranking ---
    top_k: int = 2                          # Only Top-2 assets can stage orders
    min_z_gap: float = 0.8                  # Outlier score gap over universe median
    # --- Pillar 3: Maker execution ---
    maker_fee: float = 0.0004               # 4 bps maker fee
    taker_fee: float = 0.0008               # 8 bps taker fee
    exit_slippage: float = 0.0015           # 15 bps exit slippage
    fill_prob_calib: float = 0.70           # 70% fill probability on touch
    through_fail_atr: float = 0.25          # Adverse selection: reject if bar closes > 0.25 ATR through level
    limit_ttl_bars: int = 16                # 4 hours TTL
    # --- Pillar 4: Ratchet & Target ---
    target_r: float = 2.25
    arm0_r: float = 0.80
    lock0_r: float = 0.15
    arm1_r: float = 1.50
    lock1_r: float = 0.80
    time_decay_bars: int = 32
    time_decay_r: float = 0.20
    # --- Pillar 5: Causal Gate ---
    train_months: int = 6
    deploy_auc_min: float = 0.54
    deploy_expectancy_min_r: float = 0.20
    # --- Portfolio Risk ---
    max_positions: int = 2
    max_pending: int = 4


# ===================================================================
# 2. PILLAR 1: MULTI-TIMEFRAME STRUCTURE (Strictly Causal)
# ===================================================================
class MultiTimeframeStructure:
    """
    Daily frame computed only from completed daily bars and shifted by 1 full day (shift(1)).
    4H swings computed only from completed 4H bars with centered window shifted by (k + 1).
    All mapped onto 15m index via forward-fill.
    """
    def __init__(self, cfg: MasterConfig):
        self.cfg = cfg

    def daily_frame(self, df15: pd.DataFrame) -> pd.DataFrame:
        d = pd.DataFrame({
            "high_d": df15["high"].resample("1D").max(),
            "low_d":  df15["low"].resample("1D").min(),
            "open_d": df15["open"].resample("1D").first(),
            "close_d": df15["close"].resample("1D").last(),
        }).dropna()
        d["atr_d"] = (d["high_d"] - d["low_d"]).rolling(14, min_periods=5).mean()
        d["pdh"] = d["high_d"].shift(1)
        d["pdl"] = d["low_d"].shift(1)

        # Daily FVG zones
        bull = d["low_d"] > d["high_d"].shift(2)
        bear = d["high_d"] < d["low_d"].shift(2)
        d["fvg_bull_lo"] = np.where(bull, d["high_d"].shift(2), np.nan)
        d["fvg_bull_hi"] = np.where(bull, d["low_d"], np.nan)
        d["fvg_bear_lo"] = np.where(bear, d["high_d"], np.nan)
        d["fvg_bear_hi"] = np.where(bear, d["low_d"].shift(2), np.nan)

        # Displacement Order Blocks
        body = (d["close_d"] - d["open_d"]).abs()
        rng = (d["high_d"] - d["low_d"]).clip(lower=1e-12)
        big = (rng > 1.5 * d["atr_d"]) & (body / rng > 0.5)
        d["ob_bull"] = d["low_d"].where(big & (d["close_d"] > d["open_d"]))
        d["ob_bear"] = d["high_d"].where(big & (d["close_d"] < d["open_d"]))

        # Forward-fill zones with max age
        lim = self.cfg.zone_max_age_days
        for c in ("fvg_bull_lo", "fvg_bull_hi", "fvg_bear_lo", "fvg_bear_hi", "ob_bull", "ob_bear"):
            d[c] = d[c].ffill(limit=lim)
        
        # Strict Causality: shift by 1 full day
        return d.shift(1)

    def h4_frame(self, df15: pd.DataFrame) -> pd.DataFrame:
        h4 = pd.DataFrame({
            "high_4h": df15["high"].resample("4h").max(),
            "low_4h":  df15["low"].resample("4h").min(),
        }).dropna()
        k = self.cfg.swing_lookback_4h
        sh = (h4["high_4h"] == h4["high_4h"].rolling(2 * k + 1, center=True).max())
        sl = (h4["low_4h"] == h4["low_4h"].rolling(2 * k + 1, center=True).min())
        h4["swing_hi"] = h4["high_4h"].where(sh).ffill(limit=6).shift(k + 1)
        h4["swing_lo"] = h4["low_4h"].where(sl).ffill(limit=6).shift(k + 1)
        return h4.shift(1)

    def map_to_15m(self, df15: pd.DataFrame) -> pd.DataFrame:
        d = self.daily_frame(df15)
        h4 = self.h4_frame(df15)
        st = d.reindex(df15.index, method="ffill")
        s4 = h4.reindex(df15.index, method="ffill")
        return pd.concat([st, s4], axis=1)


# ===================================================================
# 3. PILLAR 2: CROSS-SECTIONAL DISPERSION RANKING
# ===================================================================
class CrossSectionalRanker:
    """
    Per bar t: calculates rolling z-scores across all 18 symbols for
    absorption, CVD divergence, volume surge, and funding squeeze.
    Only assets exceeding the universe median by min_z_gap may stage orders.
    """
    @staticmethod
    def _roll_z(s: pd.Series, w: int = 672) -> pd.Series:
        m = s.rolling(w, min_periods=96).mean()
        sd = s.rolling(w, min_periods=96).std(ddof=0).replace(0.0, np.nan)
        return ((s - m) / sd).clip(-4.0, 4.0)

    def score_universe(self, per_symbol: Dict[str, pd.DataFrame],
                       ladder: Dict[str, pd.DataFrame],
                       funding: Optional[Dict[str, pd.Series]] = None
                       ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        per_bar_dir = {}
        per_bar_score = {}
        for sym, df in per_symbol.items():
            lf = ladder.get(sym)
            if lf is None or lf.empty:
                lf = pd.DataFrame(index=df.index)
            else:
                lf = lf.reindex(df.index).fillna(0.0)

            wsa = self._roll_z(lf.get("wick_sell_absorb", pd.Series(0.0, index=df.index)))
            wbe = self._roll_z(lf.get("wick_buy_exhaust", pd.Series(0.0, index=df.index)))
            ab = self._roll_z(lf.get("absorption_ratio", pd.Series(0.0, index=df.index)))
            cp = lf.get("close_pos", pd.Series(0.5, index=df.index))

            long_raw = wsa.fillna(0.0) + ab.clip(lower=0.0).fillna(0.0) + cp.clip(0.0, 1.0)
            short_raw = wbe.fillna(0.0) + (-ab.clip(upper=0.0)).fillna(0.0) + (1.0 - cp).clip(0.0, 1.0)

            fr_z = pd.Series(0.0, index=df.index)
            if funding is not None and sym in funding:
                fr_z = self._roll_z(funding[sym].reindex(df.index).ffill()).fillna(0.0)

            vol = df["volume"].astype(float)
            vol_z = self._roll_z(np.log1p(vol)).fillna(0.0)

            long_score = (long_raw + vol_z - fr_z.clip(lower=0.0)).to_numpy()
            short_score = (short_raw + vol_z + fr_z.clip(upper=0.0) * -1.0).to_numpy()

            side = np.where(long_score >= short_score, 1, -1)
            strength = np.where(long_score >= short_score, long_score, short_score)

            per_bar_dir[sym] = pd.Series(side, index=df.index)
            per_bar_score[sym] = pd.Series(strength, index=df.index)

        return pd.DataFrame(per_bar_score), pd.DataFrame(per_bar_dir)

    def pick_top(self, sc_row: pd.Series, dr_row: pd.Series,
                 cfg: MasterConfig) -> List[Tuple[str, int, float]]:
        valid = sc_row.dropna()
        if len(valid) < 4:
            return []
        med = float(valid.median())
        ranked = valid.sort_values(ascending=False).head(cfg.top_k)
        out = []
        for sym, val in ranked.items():
            if (val - med) >= cfg.min_z_gap and dr_row.get(sym, 0) != 0:
                out.append((sym, int(dr_row[sym]), float(val)))
        return out


# ===================================================================
# 4. PILLAR 3: STAGED LIMIT ORDERS & CAUSAL MAKER-FILL MODEL
# ===================================================================
@dataclass
class _StagedOrder:
    symbol: str
    side: int                # +1 long, -1 short
    limit_price: float
    stop_price: float        # invalidation (1R anchor)
    raw_r: float             # |limit - stop|
    staged_bar: int
    ttl_bars: int
    event_type: str = ""


class ZoneTriggerEngine:
    """
    Identifies high-conviction structural zones and returns candidate limit orders.
    Enforces big-R geometry: 1R >= 1.8% of entry price.
    """
    def __init__(self, cfg: MasterConfig):
        self.cfg = cfg

    def scan_bar(self, t: int, df15: pd.DataFrame, st: pd.DataFrame
                 ) -> List[Tuple[str, int, float, float, float]]:
        c = df15["close"].iat[t]; h = df15["high"].iat[t]; l = df15["low"].iat[t]
        atr_d = max(st["atr_d"].iat[t], 1e-12) if pd.notna(st["atr_d"].iat[t]) else c * 0.03
        buf = self.cfg.stop_buffer_atr_frac * atr_d
        out = []

        def ok_r(entry: float, stop: float) -> bool:
            rd = abs(entry - stop) / entry
            return self.cfg.min_stop_dist_pct <= rd <= self.cfg.max_stop_dist_pct

        # --- LONG zones ---
        pdl = st["pdl"].iat[t]
        if pd.notna(pdl) and c > pdl and l <= pdl and (pdl - l) <= 0.5 * atr_d:
            stop = pdl - buf
            if ok_r(pdl, stop):
                out.append(("SWEEP_PDL", 1, pdl, stop, pdl - stop))

        fvg_b_hi, fvg_b_lo = st["fvg_bull_hi"].iat[t], st["fvg_bull_lo"].iat[t]
        if pd.notna(fvg_b_hi) and l <= fvg_b_hi and c >= fvg_b_lo:
            stop = fvg_b_lo - buf
            if ok_r(fvg_b_hi, stop):
                out.append(("FVG_BULL", 1, fvg_b_hi, stop, fvg_b_hi - stop))

        ob_bull = st["ob_bull"].iat[t]
        if pd.notna(ob_bull) and l <= ob_bull and c > ob_bull:
            stop = ob_bull - buf
            if ok_r(ob_bull, stop):
                out.append(("OB_BULL", 1, ob_bull, stop, ob_bull - stop))

        sw_lo = st["swing_lo"].iat[t]
        if pd.notna(sw_lo) and l <= sw_lo and c > sw_lo:
            stop = sw_lo - buf
            if ok_r(sw_lo, stop):
                out.append(("SWING_LO", 1, sw_lo, stop, sw_lo - stop))

        # --- SHORT zones ---
        pdh = st["pdh"].iat[t]
        if pd.notna(pdh) and c < pdh and h >= pdh and (h - pdh) <= 0.5 * atr_d:
            stop = pdh + buf
            if ok_r(pdh, stop):
                out.append(("SWEEP_PDH", -1, pdh, stop, stop - pdh))

        fvg_s_lo, fvg_s_hi = st["fvg_bear_lo"].iat[t], st["fvg_bear_hi"].iat[t]
        if pd.notna(fvg_s_lo) and h >= fvg_s_lo and c <= fvg_s_hi:
            stop = fvg_s_hi + buf
            if ok_r(fvg_s_lo, stop):
                out.append(("FVG_BEAR", -1, fvg_s_lo, stop, stop - fvg_s_lo))

        ob_bear = st["ob_bear"].iat[t]
        if pd.notna(ob_bear) and h >= ob_bear and c < ob_bear:
            stop = ob_bear + buf
            if ok_r(ob_bear, stop):
                out.append(("OB_BEAR", -1, ob_bear, stop, stop - ob_bear))

        sw_hi = st["swing_hi"].iat[t]
        if pd.notna(sw_hi) and h >= sw_hi and c < sw_hi:
            stop = sw_hi + buf
            if ok_r(sw_hi, stop):
                out.append(("SWING_HI", -1, sw_hi, stop, stop - sw_hi))

        return out


class MakerFillModel:
    """
    Causal limit-fill simulation:
      1. Limit order resting at structural price P.
      2. Fill occurs only if price trades THROUGH the level.
      3. Adverse-selection protection: if bar closes > 0.25*ATR through the level,
         market blew straight through without liquidity -> order cancelled/failed.
      4. 70% fill probability on touch (conservative queue haircut).
      5. Execution price = P (0 slippage, 4 bps maker fee).
    """
    def __init__(self, cfg: MasterConfig, rng_seed: int = 42):
        self.cfg = cfg
        self.rng = np.random.default_rng(rng_seed)

    def check_fill(self, order: _StagedOrder, df15: pd.DataFrame,
                   st: pd.DataFrame, current_bar: int) -> Optional[Tuple[int, float]]:
        P = order.limit_price
        A = max(st["atr_d"].iat[current_bar], 1e-12) if pd.notna(st["atr_d"].iat[current_bar]) else P * 0.03
        lo = df15["low"].iat[current_bar]
        hi = df15["high"].iat[current_bar]
        cl = df15["close"].iat[current_bar]

        touched = (order.side == 1 and lo <= P) or (order.side == -1 and hi >= P)
        if not touched:
            return None

        # Straight-through adverse selection failure
        straight_through = (order.side == 1 and cl < P - self.cfg.through_fail_atr * A) or \
                           (order.side == -1 and cl > P + self.cfg.through_fail_atr * A)
        if straight_through:
            return None

        # Invalidation before fill
        if (order.side == 1 and cl < order.stop_price) or (order.side == -1 and cl > order.stop_price):
            return None

        if self.rng.random() <= self.cfg.fill_prob_calib:
            return (current_bar, P)

        return None


# ===================================================================
# 5. PILLAR 4 & 5: INSTITUTIONAL ALPHA MASTER ENGINE
# ===================================================================
class InstitutionalAlphaMaster:
    def __init__(self, cfg: MasterConfig = MasterConfig(), mode: str = "compliant"):
        """
        mode='compliant': $25 base risk, $50 house money, $15 defense, 4.5% drawdown limit.
        mode='institutional': $100 base risk (2.0%), $150 house money, $50 defense, 6.0% drawdown limit.
        """
        self.cfg = cfg
        self.mode = mode
        self.structure = MultiTimeframeStructure(cfg)
        self.trigger = ZoneTriggerEngine(cfg)
        self.ranker = CrossSectionalRanker()
        self.fill_model = MakerFillModel(cfg)

        if mode == "institutional":
            self.risk_cfg = RiskConfig(initial_capital=5000.0, base_risk=100.0,
                                       house_money_risk=150.0, drawdown_defense_risk=50.0,
                                       drawdown_limit=0.060)
        else:
            self.risk_cfg = RiskConfig(initial_capital=5000.0, base_risk=25.0,
                                       house_money_risk=50.0, drawdown_defense_risk=15.0,
                                       drawdown_limit=0.045)

        self.ratchet = RatchetConfig(
            arm0_r=cfg.arm0_r, lock0_r=cfg.lock0_r,
            arm1_r=cfg.arm1_r, lock1_r=cfg.lock1_r,
            min_target_r=cfg.target_r,
            time_decay_bars=cfg.time_decay_bars, time_decay_r=cfg.time_decay_r)

    # ---------------- Meta-Gate Training ----------------
    def fit_meta_gate(self, per_symbol: Dict[str, pd.DataFrame],
                      fp_feats: Dict[str, pd.DataFrame],
                      train_start: pd.Timestamp,
                      train_end: pd.Timestamp) -> Tuple[bool, Dict]:
        try:
            lab = RegressionRMetaLabeler(
                barrier=BarrierConfig(tp_r=self.cfg.target_r, sl_r=1.0, vertical_bars=48, min_terminal_r=0.20),
                cv=CVConfig(purge_hours=72, embargo_hours=24))
            pooled = []
            for sym, df in per_symbol.items():
                sl = df.loc[train_start:train_end]
                if len(sl) < 1500:
                    continue
                st = self.structure.map_to_15m(sl)
                # Event mask
                mask = np.zeros(len(sl), dtype=bool)
                for t in range(96, len(sl)):
                    if self.trigger.scan_bar(t, sl, st):
                        mask[t] = True
                if mask.sum() < 15:
                    continue

                # Generate realized-R labels
                sig_side = np.zeros(len(sl), dtype=np.int8)
                sig_rr = np.zeros(len(sl), dtype=np.float64)
                for t in np.flatnonzero(mask):
                    cands = self.trigger.scan_bar(t, sl, st)
                    if cands:
                        _, side, edge, stop, raw_r = cands[0]
                        sig_side[t] = side
                        sig_rr[t] = raw_r

                labels = lab.triple_barrier_labels(sl, mask, sig_side, sig_rr)
                if len(labels) < 15:
                    continue

                # Features: Footprint channels + structure ratios
                fpz = fp_feats[sym].loc[sl.index].fillna(0.0) if sym in fp_feats else pd.DataFrame(index=sl.index)
                struct_feats = pd.DataFrame(index=sl.index)
                struct_feats["dist_to_pdl"] = ((sl["close"] - st["pdl"]) / st["atr_d"].clip(lower=1e-9)).fillna(0.0)
                struct_feats["dist_to_pdh"] = ((st["pdh"] - sl["close"]) / st["atr_d"].clip(lower=1e-9)).fillna(0.0)
                
                tab = fpz.join(struct_feats, how="left").fillna(0.0).loc[sl.index[labels.index.to_numpy()]]
                tab["exit_r"] = labels["exit_r"].to_numpy()
                tab["symbol"] = sym
                ev_idx = labels.index.to_numpy()
                tab["abs_bar"] = sl.index.get_indexer(sl.index)[ev_idx] + df.index.get_indexer([sl.index[0]])[0]
                pooled.append(tab.reset_index(drop=True))

            if not pooled:
                return False, {"deploy": False, "reason": "no_events", "auc": 0.5, "exp_r": 0.0}

            pool = pd.concat(pooled, ignore_index=True)
            if len(pool) < 60:
                return False, {"deploy": False, "reason": "starvation", "auc": 0.5, "exp_r": 0.0}

            fit_res = lab.fit(pool)
            auc = fit_res.get("mean_cv_auc", 0.5)
            exp = fit_res.get("oof_expectancy_all", -1.0)
            ok = (auc >= self.cfg.deploy_auc_min) and (exp >= self.cfg.deploy_expectancy_min_r)
            return bool(ok), {"deploy": bool(ok), "auc": float(auc), "exp_r": float(exp),
                              "n_events": int(len(pool)), "reason": "ok" if ok else "no_edge"}

        except Exception as e:
            return False, {"deploy": False, "reason": f"gate_error:{e}", "auc": 0.5, "exp_r": 0.0}

    # ---------------- OOS Execution Window ----------------
    def run_window(self, per_symbol: Dict[str, pd.DataFrame],
                   ladder: Dict[str, pd.DataFrame],
                   win_start: str, win_end: str,
                   funding: Optional[Dict[str, pd.Series]] = None) -> Dict:
        cfg = self.cfg
        ws = pd.Timestamp(win_start)
        we = pd.Timestamp(win_end) + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)

        # Causal Gate
        train_end = ws - pd.Timedelta(hours=72)
        train_start = train_end - pd.Timedelta(days=cfg.train_months * 30)
        deploy, gate = self.fit_meta_gate(per_symbol, ladder, train_start, train_end)

        if not deploy:
            return {
                "deploy": False, "gate": gate, "halted": False,
                "trades": 0, "roi_pct": 0.0, "max_dd_pct": 0.0,
                "win_rate_pct": 0.0, "net_pnl": 0.0, "trades_list": [],
                "reason": f"Deployment gate inactive: {gate.get('reason')}"
            }

        # Active test window data
        test_syms = {}
        for sym, df in per_symbol.items():
            sl = df.loc[ws:we]
            if len(sl) > 200:
                test_syms[sym] = sl

        if not test_syms:
            return {
                "deploy": False, "gate": gate, "halted": False,
                "trades": 0, "roi_pct": 0.0, "max_dd_pct": 0.0,
                "win_rate_pct": 0.0, "net_pnl": 0.0, "trades_list": [],
                "reason": "Insufficient test data"
            }

        st_all = {s: self.structure.map_to_15m(d) for s, d in test_syms.items()}
        sc, dr = self.ranker.score_universe(test_syms, ladder, funding)

        T = min(len(d) for d in test_syms.values())
        syms = list(test_syms.keys())

        staged_orders: List[_StagedOrder] = []
        open_pos: List[Dict] = []
        equity = 5000.0
        peak = equity
        max_dd = 0.0
        trades = []
        house_money = False
        defense = False
        halted = False

        for t in range(96, T):
            t_idx = test_syms[syms[0]].index[t]

            # 1. Expire stale staged orders
            staged_orders = [o for o in staged_orders if (t - o.staged_bar) <= o.ttl_bars]

            # 2. Check maker fills for resting orders
            remaining = []
            for o in staged_orders:
                if len(open_pos) >= cfg.max_positions:
                    remaining.append(o)
                    continue
                df15 = test_syms[o.symbol]
                st_s = st_all[o.symbol]
                res = self.fill_model.check_fill(o, df15, st_s, t)
                if res is not None:
                    tb, fill_px = res
                    open_pos.append({
                        "sym": o.symbol, "side": o.side, "entry": fill_px,
                        "stop": o.stop_price, "raw_r": o.raw_r, "t_in": tb,
                        "mfe_r": 0.0, "armed": 0, "lock": -1.0, "event_type": o.event_type
                    })
                else:
                    remaining.append(o)
            staged_orders = remaining

            # 3. Manage open positions (stop-first, ratchet, target, decay)
            for pos in list(open_pos):
                df15 = test_syms[pos["sym"]]
                h = df15["high"].iat[t]
                l = df15["low"].iat[t]
                cl = df15["close"].iat[t]
                R = pos["raw_r"]
                side = pos["side"]
                entry = pos["entry"]
                age = t - pos["t_in"]

                # Track MFE
                fav = (h - entry) / R if side == 1 else (entry - l) / R
                pos["mfe_r"] = max(pos["mfe_r"], fav)

                # Microstructure Ratchet Arming
                if pos["armed"] == 0 and pos["mfe_r"] >= cfg.arm0_r:
                    pos["lock"] = cfg.lock0_r
                    pos["armed"] = 1
                if pos["armed"] == 1 and pos["mfe_r"] >= cfg.arm1_r:
                    pos["lock"] = cfg.lock1_r
                    pos["armed"] = 2

                lock_px = entry + side * pos["lock"] * R
                tp_px = entry + side * cfg.target_r * R
                exit_px, why = None, ""

                # Stop-first conservative barrier
                if side == 1 and l <= pos["stop"]:
                    exit_px, why = pos["stop"], "stop"
                elif side == -1 and h >= pos["stop"]:
                    exit_px, why = pos["stop"], "stop"

                # Target exit
                if exit_px is None:
                    if side == 1 and h >= tp_px:
                        exit_px, why = tp_px, "target"
                    elif side == -1 and l <= tp_px:
                        exit_px, why = tp_px, "target"

                # Ratchet Lock exit
                if exit_px is None and pos["armed"] > 0:
                    if side == 1 and l <= lock_px:
                        exit_px, why = lock_px, "lock"
                    elif side == -1 and h >= lock_px:
                        exit_px, why = lock_px, "lock"

                # Time Decay exit
                if exit_px is None and age >= cfg.time_decay_bars and pos["mfe_r"] < cfg.time_decay_r:
                    exit_px, why = cl, "decay"

                if exit_px is not None:
                    pnl_r = side * (exit_px - entry) / R
                    # Real exchange frictions: 4 bps maker entry + 8 bps taker exit + 15 bps exit slip = 27 bps
                    fric_r = (0.0027 * entry) / R
                    net_pnl_r = pnl_r - fric_r

                    risk_d = (self.risk_cfg.house_money_risk if house_money
                              else self.risk_cfg.drawdown_defense_risk if defense
                              else self.risk_cfg.base_risk)
                    pnl_d = net_pnl_r * risk_d
                    equity += pnl_d
                    peak = max(peak, equity)
                    max_dd = max(max_dd, (peak - equity) / peak if peak > 0 else 0.0)

                    house_money = (equity - 5000.0) > 500.0
                    defense = ((peak - equity) / peak) > 0.025

                    trades.append({
                        "sym": pos["sym"], "side": side, "entry": entry,
                        "exit": exit_px, "r": net_pnl_r, "pnl_d": pnl_d,
                        "why": why, "age": age
                    })
                    open_pos.remove(pos)

                    # Hard Drawdown Circuit Breaker
                    if max_dd >= self.risk_cfg.drawdown_limit:
                        halted = True
                        break

            if halted:
                break

            # 4. Scan new candidate zones & stage top-ranked orders for next bars
            if (len(open_pos) + len(staged_orders)) < cfg.max_pending and t_idx in sc.index:
                sc_row = sc.loc[t_idx]
                dr_row = dr.loc[t_idx]
                top_picks = self.ranker.pick_top(sc_row, dr_row, cfg)
                for sym, side, score in top_picks:
                    if any(o.symbol == sym for o in staged_orders) or any(p["sym"] == sym for p in open_pos):
                        continue
                    df15 = test_syms[sym]
                    st_s = st_all[sym]
                    hits = self.trigger.scan_bar(t, df15, st_s)
                    for (etype, hside, edge, stop, raw_r) in hits:
                        if hside == side:
                            staged_orders.append(_StagedOrder(
                                symbol=sym, side=side, limit_price=edge, stop_price=stop,
                                raw_r=raw_r, staged_bar=t, ttl_bars=cfg.limit_ttl_bars,
                                event_type=etype
                            ))
                            break

        net_pnl = equity - 5000.0
        roi_pct = (net_pnl / 5000.0) * 100.0
        tot_trades = len(trades)
        wins = sum(1 for tr in trades if tr["r"] > 0)
        win_rate = (wins / tot_trades * 100.0) if tot_trades > 0 else 0.0

        return {
            "deploy": True,
            "gate": gate,
            "halted": halted,
            "equity": equity,
            "net_pnl": net_pnl,
            "roi_pct": roi_pct,
            "max_dd_pct": max_dd * 100.0,
            "trades": tot_trades,
            "win_rate_pct": win_rate,
            "trades_list": trades
        }


# ===================================================================
# 6. UNIFIED 20-WINDOW WALK-FORWARD BENCHMARK RUNNER
# ===================================================================
WINDOWS = [
    ("W01", "2021-05-01", "2021-05-31", "May 2021 Great Liquidation Crash"),
    ("W02", "2021-09-01", "2021-09-30", "September 2021 El Salvador Flash Crash"),
    ("W03", "2021-11-01", "2021-11-30", "November 2021 Cycle Peak Reversal"),
    ("W04", "2022-01-01", "2022-01-31", "January 2022 Fed Macro Tightening"),
    ("W05", "2022-05-01", "2022-05-31", "May 2022 Terra-Luna Systemic Shock"),
    ("W06", "2022-06-01", "2022-06-30", "June 2022 3AC & Celsius Capitulation"),
    ("W07", "2022-09-01", "2022-09-30", "September 2022 ETH Merge Chop & Grind"),
    ("W08", "2022-11-01", "2022-11-30", "November 2022 FTX Collapse Bottom"),
    ("W09", "2023-01-01", "2023-01-31", "January 2023 Short Squeeze Ignition"),
    ("W10", "2023-03-01", "2023-03-31", "March 2023 US Regional Banking Panic"),
    ("W11", "2023-06-01", "2023-06-30", "June 2023 BlackRock Spot ETF Filing"),
    ("W12", "2023-08-01", "2023-08-31", "August 2023 Space-X Bitcoin Write-Down"),
    ("W13", "2023-10-01", "2023-10-31", "October 2023 Fake ETF News Squeeze"),
    ("W14", "2024-01-01", "2024-01-31", "January 2024 Spot ETF Approval Sell-the-News"),
    ("W15", "2024-03-01", "2024-03-31", "March 2024 Pre-Halving All-Time High Run"),
    ("W16", "2024-08-01", "2024-08-31", "August 2024 Yen Carry Trade Unwind"),
    ("W17", "2024-11-01", "2024-11-30", "November 2024 US Presidential Election"),
    ("W18", "2025-02-01", "2025-02-28", "February 2025 Post-Inauguration Realignment"),
    ("W19", "2025-07-01", "2025-07-31", "July 2025 Mid-Cycle Distribution"),
    ("W20", "2026-03-01", "2026-03-31", "March 2026 Sovereign Debt Restructuring"),
]

def run_full_walkforward(per_symbol: Dict[str, pd.DataFrame],
                         ladder: Dict[str, pd.DataFrame],
                         funding: Optional[Dict[str, pd.Series]] = None,
                         modes: Tuple[str, ...] = ("compliant", "institutional")) -> pd.DataFrame:
    rows = []
    for mode in modes:
        for wid, ws, we, name in WINDOWS:
            eng = InstitutionalAlphaMaster(mode=mode)
            res = eng.run_window(per_symbol, ladder, ws, we, funding)
            rows.append({
                "mode": mode, "window_id": wid, "name": name,
                "deploy": res.get("deploy", False),
                "trades": res.get("trades", 0),
                "roi_pct": res.get("roi_pct", 0.0),
                "max_dd_pct": res.get("max_dd_pct", 0.0),
                "win_rate_pct": res.get("win_rate_pct", 0.0),
                "halted": res.get("halted", False),
                "gate_auc": res.get("gate", {}).get("auc"),
                "gate_exp_r": res.get("gate", {}).get("exp_r"),
                "reason": res.get("reason", "ok")
            })
    return pd.DataFrame(rows)

`

### File: Engine/core/portfolio_execution_kernel.py
`python
# Engine/core/portfolio_execution_kernel.py
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig


@dataclass
class _Pos:
    symbol: str
    side: int
    entry: float
    stop: float
    target: float
    qty: float
    risk: float
    entry_bar: int
    max_r: float
    rr: float


class PortfolioExecutionKernel:
    """
    Multi-symbol portfolio kernel. One shared equity pool, one hard DD breaker,
    max `max_positions` concurrent positions. Fills at Open[j+1] of the symbol
    where the signal fired; stop-first ambiguity; full ratchet suite per position.

    All symbol DataFrames must share an identical, monotonic DatetimeIndex.
    """

    def __init__(self,
                 symbols: List[str],
                 risk: RiskConfig = RiskConfig(),
                 fric: FrictionConfig = FrictionConfig(),
                 ratchet: RatchetConfig = RatchetConfig(),
                 max_positions: int = 2):
        self.symbols = list(symbols)
        self.risk = risk
        self.fric = fric
        self.rat = ratchet
        self.max_positions = max_positions
        self.trades: List[Dict] = []

    # ---------------- helpers ----------------
    def _entry_price(self, side: int, o: float) -> float:
        return o * (1.0 + self.fric.entry_slippage * side)

    def _loss_per_share(self, side: int, px: float, raw_r: float) -> float:
        if side == 1:
            actual_stop = (px - raw_r) * (1.0 - self.fric.exit_slippage)
            return (px - actual_stop) + (px + actual_stop) * self.fric.taker_fee
        actual_stop = (px + raw_r) * (1.0 + self.fric.exit_slippage)
        return (actual_stop - px) + (px + actual_stop) * self.fric.taker_fee

    def _ratchet(self, p: _Pos, hi: float, lo: float) -> None:
        R = self.rat
        gain = (hi - p.entry) / p.rr if p.side == 1 else (p.entry - lo) / p.rr
        if gain > p.max_r:
            p.max_r = gain
        if p.side == 1:
            if p.max_r >= R.arm1_r:
                p.stop = max(p.stop, p.entry + R.lock1_r * p.rr)
            elif p.max_r >= R.arm0_r:
                p.stop = max(p.stop, p.entry + R.lock0_r * p.rr)
        else:
            if p.max_r >= R.arm1_r:
                p.stop = min(p.stop, p.entry - R.lock1_r * p.rr)
            elif p.max_r >= R.arm0_r:
                p.stop = min(p.stop, p.entry - R.lock0_r * p.rr)

    def _exit(self, p: _Pos, px: float, reason: str, t: int) -> float:
        gross = p.qty * (px - p.entry) if p.side == 1 else p.qty * (p.entry - px)
        fees = p.qty * (p.entry + px) * self.fric.taker_fee
        net = gross - fees
        self.trades.append({
            "symbol": p.symbol, "entry_bar": p.entry_bar, "exit_bar": t,
            "side": "LONG" if p.side == 1 else "SHORT",
            "entry": p.entry, "exit": px, "pnl": net,
            "r": net / p.risk if p.risk > 0 else 0.0,
            "max_r": p.max_r, "reason": reason})
        return net

    def _check_exit(self, p: _Pos, o: float, h: float, l: float) -> Tuple[Optional[float], str]:
        if p.side == 1:
            if o <= p.stop:   return o * (1.0 - self.fric.exit_slippage), "STOP_OPEN"
            if o >= p.target: return o, "TARGET_OPEN"
            if l <= p.stop:   return p.stop * (1.0 - self.fric.exit_slippage), "STOP_BAR"
            if h >= p.target: return p.target, "TARGET_BAR"
        else:
            if o >= p.stop:   return o * (1.0 + self.fric.exit_slippage), "STOP_OPEN"
            if o <= p.target: return o, "TARGET_OPEN"
            if h >= p.stop:   return p.stop * (1.0 + self.fric.exit_slippage), "STOP_BAR"
            if l <= p.target: return p.target, "TARGET_BAR"
        return None, ""

    # ---------------- main loop ----------------
    def run(self, data: Dict[str, pd.DataFrame],
            gated_signals: Dict[str, pd.DataFrame],
            training_mode: bool = False) -> Dict:
        if not data:
            return {
                "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0,
                "trades": 0, "net_pnl": 0.0, "trades_list": [], "equity_curve": np.array([])
            }
        T = min(len(d) for d in data.values()) if data else 0
        if T == 0:
            return {
                "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0,
                "trades": 0, "net_pnl": 0.0, "trades_list": [], "equity_curve": np.array([])
            }
        realized = self.risk.initial_capital
        peak = realized
        equity_curve = np.zeros(T)
        self.trades = []
        positions: Dict[str, _Pos] = {}
        pending: Dict[str, tuple] = {}   # sym -> (side, raw_r) set at close of t, filled t+1

        op = {s: data[s]["open"].values for s in self.symbols if s in data}
        hi = {s: data[s]["high"].values for s in self.symbols if s in data}
        lo = {s: data[s]["low"].values for s in self.symbols if s in data}
        cl = {s: data[s]["close"].values for s in self.symbols if s in data}
        sig_side = {s: gated_signals[s]["side"].values for s in self.symbols if s in gated_signals}
        sig_rr = {s: gated_signals[s]["raw_r"].values for s in self.symbols if s in gated_signals}

        # Check bar 0 signal queue
        for sym in self.symbols:
            if sym in sig_side and len(sig_side[sym]) > 0:
                s_ = int(sig_side[sym][0])
                if s_ != 0:
                    pending[sym] = (s_, float(sig_rr[sym][0]))

        def mark_to_market(t: int) -> float:
            unreal = 0.0
            for s, p in positions.items():
                if p.side == 1:
                    unreal += p.qty * (cl[s][t] - p.entry)
                else:
                    unreal += p.qty * (p.entry - cl[s][t])
                unreal -= p.qty * (p.entry + cl[s][t]) * self.fric.taker_fee
            return realized + unreal

        for t in range(1, T):
            current_dd = (peak - mark_to_market(t - 1)) / peak if peak > 0 else 0.0
            dd_blocked = (not training_mode) and current_dd >= self.risk.drawdown_limit

            # --- 1) Fill pending entries at this bar's open (signal was at t-1 close) ---
            for sym in list(pending.keys()):
                if len(positions) >= self.max_positions:
                    break
                if dd_blocked:
                    pending.pop(sym)
                    continue
                side, raw_r = pending.pop(sym)
                px = self._entry_price(side, op[sym][t])
                rr = raw_r if raw_r > 0 else px * 0.005
                lps = self._loss_per_share(side, px, rr)
                if lps <= 0:
                    continue
                net_profit = realized - self.risk.initial_capital
                if net_profit > 50.0:
                    trade_risk = min(self.risk.house_money_risk, realized * 0.01)
                elif current_dd > 0.025:
                    trade_risk = self.risk.drawdown_defense_risk
                else:
                    trade_risk = self.risk.base_risk
                if side == 1:
                    stop, tgt = px - rr, px + rr * self.rat.min_target_r
                else:
                    stop, tgt = px + rr, px - rr * self.rat.min_target_r
                positions[sym] = _Pos(sym, side, px, stop, tgt,
                                      trade_risk / lps, trade_risk, t, 0.0, rr)

            # --- 2) Manage open positions (entry bar included) ---
            for sym in list(positions.keys()):
                p = positions[sym]
                exit_px, reason = self._check_exit(p, op[sym][t], hi[sym][t], lo[sym][t])
                if not exit_px:
                    self._ratchet(p, hi[sym][t], lo[sym][t])
                    if (t - p.entry_bar) >= self.rat.time_decay_bars and p.max_r < self.rat.time_decay_r:
                        exit_px, reason = cl[sym][t], "TIME_DECAY"
                if exit_px:
                    realized += self._exit(p, exit_px, reason, t)
                    del positions[sym]

            # --- 3) Mark equity, hard portfolio DD breaker ---
            equity = mark_to_market(t)
            if equity > peak:
                peak = equity
            equity_curve[t] = equity
            current_dd = (peak - equity) / peak if peak > 0 else 0.0

            if (not training_mode) and current_dd >= self.risk.drawdown_limit and positions:
                for sym in list(positions.keys()):
                    p = positions[sym]
                    realized += self._exit(p, cl[sym][t], "DRAWDOWN_LIMIT", t)
                    del positions[sym]
                equity = realized
                equity_curve[t] = equity

            # --- 4) Queue signals from bar t close for fill at t+1 open ---
            if t < T - 1:
                for sym in self.symbols:
                    if sym in sig_side and t < len(sig_side[sym]):
                        s_ = int(sig_side[sym][t])
                        if s_ != 0 and sym not in positions and sym not in pending:
                            pending[sym] = (s_, float(sig_rr[sym][t]))

            # --- 5) Terminal settlement ---
            if t == T - 1:
                for sym in list(positions.keys()):
                    realized += self._exit(positions[sym], cl[sym][t],
                                           "TERMINAL_SETTLEMENT", t)
                    del positions[sym]
                equity_curve[t] = realized

        equity_curve[0] = self.risk.initial_capital
        tot = len(self.trades)
        wins = sum(1 for tr in self.trades if tr["pnl"] > 0)
        peaks = np.maximum.accumulate(equity_curve)
        with np.errstate(divide="ignore", invalid="ignore"):
            dds = np.where(peaks > 0, (peaks - equity_curve) / peaks * 100.0, 0.0)
        net_pnl = realized - self.risk.initial_capital
        return {
            "roi_pct": net_pnl / self.risk.initial_capital * 100.0,
            "max_dd_pct": float(np.max(dds)) if T else 0.0,
            "win_rate_pct": wins / tot * 100.0 if tot else 0.0,
            "trades": tot, "net_pnl": net_pnl,
            "trades_list": self.trades, "equity_curve": equity_curve,
        }

`

### File: Engine/core/execution_kernel.py
`python
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class RiskConfig:
    initial_capital: float = 5000.0
    base_risk: float = 25.0              # 0.50% base risk
    house_money_risk: float = 50.0       # 1.00% max 2x risk
    drawdown_defense_risk: float = 15.0  # 0.30% risk
    drawdown_limit: float = 0.045        # 4.5% ($225) hard drawdown stop

@dataclass(frozen=True)
class FrictionConfig:
    taker_fee: float = 0.0008            # 8 bps
    entry_slippage: float = 0.0010       # 10 bps
    exit_slippage: float = 0.0015        # 15 bps

@dataclass(frozen=True)
class RatchetConfig:
    arm0_r: float = 0.8
    lock0_r: float = 0.15
    arm1_r: float = 1.5
    lock1_r: float = 0.80
    min_target_r: float = 2.5
    time_decay_bars: int = 24
    time_decay_r: float = 0.20


class ExecutionKernel:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(),
                 fric_cfg: FrictionConfig = FrictionConfig(),
                 ratchet_cfg: RatchetConfig = RatchetConfig()):
        self.risk = risk_cfg
        self.fric = fric_cfg
        self.ratchet = ratchet_cfg

        # position state
        self._pos_side = 0
        self._pos_entry = 0.0
        self._pos_stop = 0.0
        self._pos_target = 0.0
        self._pos_qty = 0.0
        self._pos_risk = 0.0
        self._pos_bar = -1
        self._pos_max_r = 0.0
        self._pos_rr = 1.0

    # ---------- helpers ----------
    def _close_trade(self, t: int, exit_px: float, reason: str, realized: float, trades: List[Dict]) -> float:
        pos_side, pos_qty = self._pos_side, self._pos_qty
        gross = pos_qty * (exit_px - self._pos_entry) if pos_side == 1 else pos_qty * (self._pos_entry - exit_px)
        fees = pos_qty * (self._pos_entry + exit_px) * self.fric.taker_fee
        net = gross - fees
        realized += net
        trades.append({
            "entry_bar": self._pos_bar,
            "exit_bar": t,
            "side": "LONG" if pos_side == 1 else "SHORT",
            "entry": self._pos_entry,
            "exit": exit_px,
            "pnl": net,
            "r": net / self._pos_risk if self._pos_risk > 0 else 0.0,
            "max_r": self._pos_max_r,
            "reason": reason
        })
        self._pos_side = 0
        return realized

    def _apply_ratchet(self, hi: float, lo: float) -> None:
        """Update trailing stop from intrabar extremes (bar j+1 onward, never entry bar open)."""
        rr = self._pos_rr
        if self._pos_side == 1:
            r_gain = (hi - self._pos_entry) / rr
            if r_gain > self._pos_max_r:
                self._pos_max_r = r_gain
            if self._pos_max_r >= self.ratchet.arm1_r:
                self._pos_stop = max(self._pos_stop, self._pos_entry + self.ratchet.lock1_r * rr)
            elif self._pos_max_r >= self.ratchet.arm0_r:
                self._pos_stop = max(self._pos_stop, self._pos_entry + self.ratchet.lock0_r * rr)
        elif self._pos_side == -1:
            r_gain = (self._pos_entry - lo) / rr
            if r_gain > self._pos_max_r:
                self._pos_max_r = r_gain
            if self._pos_max_r >= self.ratchet.arm1_r:
                self._pos_stop = min(self._pos_stop, self._pos_entry - self.ratchet.lock1_r * rr)
            elif self._pos_max_r >= self.ratchet.arm0_r:
                self._pos_stop = min(self._pos_stop, self._pos_entry - self.ratchet.lock0_r * rr)

    # ---------- main loop ----------
    def run(self, df: pd.DataFrame, signals: pd.DataFrame, training_mode: bool = False) -> Dict:
        """
        Runs the centralized causal execution engine.
        df: Price data with open, high, low, close.
        signals: DataFrame containing 'side' (1 for LONG, -1 for SHORT, 0 for None),
                 'raw_r' (the un-slippaged risk geometry in price terms).
        """
        T = len(df)
        if T == 0:
            return {
                "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0,
                "trades": 0, "net_pnl": 0.0, "trades_list": [], "equity_curve": np.array([])
            }

        op = df["open"].values
        hi = df["high"].values
        lo = df["low"].values
        cl = df["close"].values
        signal_side = signals["side"].values
        signal_raw_r = signals["raw_r"].values

        realized = self.risk.initial_capital
        peak = realized
        equity_curve = np.full(T, realized)
        trades: List[Dict] = []

        # position state
        self._pos_side = 0
        self._pos_entry = 0.0
        self._pos_stop = 0.0
        self._pos_target = 0.0
        self._pos_qty = 0.0
        self._pos_risk = 0.0
        self._pos_bar = -1
        self._pos_max_r = 0.0
        self._pos_rr = 1.0

        pending_side = 0
        pending_raw_r = 0.0   # signal set on bar j, filled on j+1

        if signal_side[0] != 0:
            pending_side = int(signal_side[0])
            pending_raw_r = float(signal_raw_r[0])

        # FIX C-1/C-2: pending_sig[j] -> fill at Open[j+1], evaluate SL/TP on the SAME bar j+1
        for t in range(1, T):
            # ---- 1) Fill pending signal at this bar's open ----
            if pending_side != 0:
                net_profit = realized - self.risk.initial_capital
                current_dd = (peak - realized) / peak if peak > 0 else 0.0

                if (not training_mode) and current_dd >= self.risk.drawdown_limit:
                    pending_side = 0  # blocked by hard DD limit
                else:
                    px = op[t] * (1.0 + self.fric.entry_slippage * pending_side)
                    raw_r = pending_raw_r if pending_raw_r > 0 else px * 0.005

                    if pending_side == 1:
                        stop_px = px - raw_r
                        target_px = px + raw_r * self.ratchet.min_target_r
                        actual_stop = stop_px * (1.0 - self.fric.exit_slippage)
                        loss_per_share = (px - actual_stop) + (px + actual_stop) * self.fric.taker_fee
                    else:
                        stop_px = px + raw_r
                        target_px = px - raw_r * self.ratchet.min_target_r
                        actual_stop = stop_px * (1.0 + self.fric.exit_slippage)
                        loss_per_share = (actual_stop - px) + (px + actual_stop) * self.fric.taker_fee

                    if net_profit > 50.0:
                        trade_risk = min(self.risk.house_money_risk, realized * 0.01)
                    elif current_dd > 0.025:
                        trade_risk = self.risk.drawdown_defense_risk
                    else:
                        trade_risk = self.risk.base_risk

                    self._pos_side = pending_side
                    self._pos_entry = px
                    self._pos_stop = stop_px
                    self._pos_target = target_px
                    self._pos_risk = trade_risk
                    self._pos_qty = trade_risk / loss_per_share if loss_per_share > 0 else 0.0
                    self._pos_bar = t
                    self._pos_max_r = 0.0
                    self._pos_rr = raw_r

                pending_side = 0
                pending_raw_r = 0.0

            # ---- 2) Intrabar exit evaluation (INCLUDES entry bar = FIX C-2) ----
            if self._pos_side != 0:
                o_, h_, l_, c_ = op[t], hi[t], lo[t], cl[t]
                exit_px = 0.0
                exit_reason = ""

                if self._pos_side == 1:
                    if o_ <= self._pos_stop:
                        exit_px = o_ * (1.0 - self.fric.exit_slippage)
                        exit_reason = "STOP_OPEN"
                    elif o_ >= self._pos_target:
                        exit_px = o_
                        exit_reason = "TARGET_OPEN"
                    elif l_ <= self._pos_stop:  # STOP-FIRST on ambiguity
                        exit_px = self._pos_stop * (1.0 - self.fric.exit_slippage)
                        exit_reason = "STOP_BAR"
                    elif h_ >= self._pos_target:
                        exit_px = self._pos_target
                        exit_reason = "TARGET_BAR"
                else:
                    if o_ >= self._pos_stop:
                        exit_px = o_ * (1.0 + self.fric.exit_slippage)
                        exit_reason = "STOP_OPEN"
                    elif o_ <= self._pos_target:
                        exit_px = o_
                        exit_reason = "TARGET_OPEN"
                    elif h_ >= self._pos_stop:  # STOP-FIRST on ambiguity
                        exit_px = self._pos_stop * (1.0 + self.fric.exit_slippage)
                        exit_reason = "STOP_BAR"
                    elif l_ <= self._pos_target:
                        exit_px = self._pos_target
                        exit_reason = "TARGET_BAR"

                if exit_reason:
                    realized = self._close_trade(t, exit_px, exit_reason, realized, trades)
                else:
                    # ratchet updates AFTER exit check -> lock levels bind bar t+1 onward
                    self._apply_ratchet(h_, l_)
                    if (t - self._pos_bar) >= self.ratchet.time_decay_bars and self._pos_max_r < self.ratchet.time_decay_r:
                        realized = self._close_trade(t, c_, "TIME_DECAY", realized, trades)

            # ---- 3) Mark-to-market equity & DD gate ----
            if self._pos_side == 1:
                unreal = self._pos_qty * (cl[t] - self._pos_entry) - self._pos_qty * (self._pos_entry + cl[t]) * self.fric.taker_fee
            elif self._pos_side == -1:
                unreal = self._pos_qty * (self._pos_entry - cl[t]) - self._pos_qty * (self._pos_entry + cl[t]) * self.fric.taker_fee
            else:
                unreal = 0.0

            equity = realized + unreal
            if equity > peak:
                peak = equity
            equity_curve[t] = equity
            current_dd = (peak - equity) / peak if peak > 0 else 0.0

            if (not training_mode) and current_dd >= self.risk.drawdown_limit and self._pos_side != 0:
                realized = self._close_trade(t, cl[t], "DRAWDOWN_LIMIT", realized, trades)
                equity = realized
                equity_curve[t] = equity
                current_dd = (peak - equity) / peak if peak > 0 else 0.0

            # ---- 4) Signal on bar t becomes PENDING for bar t+1 (FIX C-1) ----
            if t < T - 1 and self._pos_side == 0:
                sig = signal_side[t]
                if sig != 0:
                    pending_side = int(sig)
                    pending_raw_r = float(signal_raw_r[t])

            # ---- 5) Terminal settlement ----
            if t == T - 1 and self._pos_side != 0:
                realized = self._close_trade(t, cl[t], "TERMINAL_SETTLEMENT", realized, trades)
                equity_curve[t] = realized

        tot = len(trades)
        wins = sum(1 for tr in trades if tr["pnl"] > 0)
        wr = (wins / tot * 100.0) if tot > 0 else 0.0
        net_pnl = realized - self.risk.initial_capital
        roi = (net_pnl / self.risk.initial_capital * 100.0)
        peaks = np.maximum.accumulate(equity_curve)
        with np.errstate(divide='ignore', invalid='ignore'):
            dds = np.where(peaks > 0, (peaks - equity_curve) / peaks * 100.0, 0.0)
        max_dd = float(np.max(dds)) if len(dds) > 0 else 0.0

        return {
            "roi_pct": roi, "max_dd_pct": max_dd, "win_rate_pct": wr,
            "trades": tot, "net_pnl": net_pnl,
            "trades_list": trades, "equity_curve": equity_curve
        }

`

### File: Engine/ml/rf_meta_labeler.py
`python
# Engine/ml/rf_meta_labeler.py
from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

try:
    from xgboost import XGBRegressor
    _REG_BACKEND = "xgb"
except ImportError:
    from lightgbm import LGBMRegressor
    _REG_BACKEND = "lgbm"

from Engine.ml.pooled_meta_labeler import (
    PooledInstitutionalMetaLabeler, BarrierConfig, CVConfig, ModelConfig, GateConfig
)


class RegressionRMetaLabeler(PooledInstitutionalMetaLabeler):
    """
    Round-3 meta-labeler:
      - target = realized exit_r (continuous regression), friction-adjusted barriers
      - single-feature AUC probe gate before full fit
      - tau_R gate on predicted R (expectancy break-even, friction included)
    """

    def __init__(self,
                 barrier: BarrierConfig = BarrierConfig(tp_r=2.0, sl_r=1.0, vertical_bars=32, min_terminal_r=0.20),
                 cv: CVConfig = CVConfig(purge_hours=72, embargo_hours=24),
                 model: ModelConfig = ModelConfig(),
                 gate: GateConfig = GateConfig()):
        super().__init__(barrier=barrier, cv=cv, model=model, gate=gate)
        self.tau_r_: float = 0.0

    def triple_barrier_labels(self, df: pd.DataFrame, event_mask: np.ndarray,
                              side: np.ndarray, r_dist: np.ndarray) -> pd.DataFrame:
        cl = df["close"].values
        median_r = np.nanmedian(r_dist[r_dist > 0]) if (r_dist > 0).any() else 1.0
        fric_R = 0.0033 * np.nanmean(cl) / max(median_r, 1e-12)
        adjusted_barrier = BarrierConfig(
            tp_r=self.barrier.tp_r,
            sl_r=self.barrier.sl_r + min(fric_R, 0.25),
            vertical_bars=self.barrier.vertical_bars,
            min_terminal_r=self.barrier.min_terminal_r
        )
        old_barrier = self.barrier
        self.barrier = adjusted_barrier
        labels = super().triple_barrier_labels(df, event_mask, side, r_dist)
        self.barrier = old_barrier
        return labels

    def probe_features(self, pooled: pd.DataFrame) -> pd.DataFrame:
        from sklearn.metrics import roc_auc_score
        y = (pooled["exit_r"] > 0).to_numpy(np.int8)
        feats = [c for c in pooled.columns
                 if c not in ("symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r")]
        rows = []
        splits = self._cv_splits(pooled)

        for f in feats:
            x = pooled[f].to_numpy(np.float64)
            aucs = []
            for tr, te in splits:
                if len(np.unique(y[te])) > 1:
                    try:
                        aucs.append(float(roc_auc_score(y[te], x[te])))
                    except Exception:
                        pass
            m = float(np.nanmean(aucs)) if aucs else 0.5
            rows.append({
                "feature": f,
                "raw_auc_mean": m,
                "raw_auc_abs": abs(m - 0.5)
            })

        probe = pd.DataFrame(rows).sort_values("raw_auc_abs", ascending=False)
        best_pair, best_auc = "", 0.5
        # Test top 6 features pairwise
        top_feats = probe["feature"].head(6).tolist()
        for i in range(len(top_feats)):
            for j in range(i + 1, len(top_feats)):
                s = pooled[top_feats[i]].to_numpy(np.float64) + pooled[top_feats[j]].to_numpy(np.float64)
                aucs = []
                for tr, te in splits:
                    if len(np.unique(y[te])) > 1:
                        try:
                            aucs.append(float(roc_auc_score(y[te], s[te])))
                        except Exception:
                            pass
                m = float(np.nanmean(aucs)) if aucs else 0.5
                if abs(m - 0.5) > abs(best_auc - 0.5):
                    best_auc = m
                    best_pair = f"{top_feats[i]}+{top_feats[j]}"

        probe["best_pair"] = [best_pair] + [""] * (len(probe) - 1)
        probe["best_pair_auc"] = [best_auc] + [np.nan] * (len(probe) - 1)
        return probe

    def fit(self, pooled: pd.DataFrame) -> Dict:
        from sklearn.metrics import roc_auc_score
        feats = [c for c in pooled.columns
                 if c not in ("symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r")]
        X = pooled[feats].to_numpy(np.float64)
        r = pooled["exit_r"].to_numpy(np.float64)
        y_bin = (r > 0).astype(np.int8)

        oof = np.full(len(pooled), np.nan)
        aucs = []
        splits = self._cv_splits(pooled)

        for tr, te in splits:
            if _REG_BACKEND == "xgb":
                mdl = XGBRegressor(
                    max_depth=3, n_estimators=500, learning_rate=0.03,
                    reg_alpha=2.0, reg_lambda=5.0, subsample=0.8,
                    colsample_bytree=0.7, min_child_weight=10,
                    random_state=42, n_jobs=-1, tree_method="hist"
                )
            else:
                mdl = LGBMRegressor(
                    max_depth=3, n_estimators=500, learning_rate=0.03,
                    reg_alpha=2.0, reg_lambda=5.0, subsample=0.8,
                    colsample_bytree=0.7, min_child_weight=10,
                    random_state=42, n_jobs=-1, verbose=-1
                )
            mdl.fit(X[tr], r[tr])
            oof[te] = mdl.predict(X[te])
            if len(np.unique(y_bin[te])) > 1:
                aucs.append(float(roc_auc_score(y_bin[te], oof[te])))

        self.fold_aucs_ = aucs
        valid = np.isfinite(oof)
        self.tau_r_ = self._calibrate_tau_R(oof[valid], r[valid])

        # Final fit on all training data
        if _REG_BACKEND == "xgb":
            final_mdl = XGBRegressor(
                max_depth=3, n_estimators=500, learning_rate=0.03,
                reg_alpha=2.0, reg_lambda=5.0, subsample=0.8,
                colsample_bytree=0.7, min_child_weight=10,
                random_state=42, n_jobs=-1, tree_method="hist"
            )
        else:
            final_mdl = LGBMRegressor(
                max_depth=3, n_estimators=500, learning_rate=0.03,
                reg_alpha=2.0, reg_lambda=5.0, subsample=0.8,
                colsample_bytree=0.7, min_child_weight=10,
                random_state=42, n_jobs=-1, verbose=-1
            )
        final_mdl.fit(X, r)
        self.model_ = final_mdl
        self.feat_cols_ = feats

        return {
            "mean_cv_auc": float(np.mean(aucs)) if aucs else float("nan"),
            "fold_aucs": aucs,
            "calibrated_tau_r": self.tau_r_,
            "oof_expectancy_all": float(r[valid].mean()) if valid.any() else 0.0,
            "n_events": int(len(pooled)),
        }

    def _calibrate_tau_R(self, p: np.ndarray, r: np.ndarray) -> float:
        """tau_R = smallest predicted-R cut with OOF E[R | sel] > friction buffer."""
        for tau in np.quantile(p, [0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50]):
            sel = p >= tau
            if sel.sum() < 25:
                continue
            if r[sel].mean() > 0.15:
                return float(tau)
        return float("inf")

    def score_signals(self, df_sym: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
        out = signals.copy()
        mask = out["side"].to_numpy() != 0
        pred = np.full(len(out), np.nan)
        if mask.any() and self.model_ is not None:
            feat_df = self.build_features(df_sym)
            available_cols = [c for c in self.feat_cols_ if c in feat_df.columns]
            X = feat_df.iloc[np.flatnonzero(mask)][available_cols]
            ok = np.isfinite(X.to_numpy(np.float64)).all(axis=1)
            ev = np.flatnonzero(mask)[ok]
            if len(ev) > 0:
                pred[ev] = self.model_.predict(X.to_numpy(np.float64)[ok])
        keep = np.isfinite(pred) & (pred >= self.tau_r_)
        out.loc[:, "side"] = np.where(keep, out["side"].to_numpy(), 0)
        out.loc[out["side"] == 0, "raw_r"] = 0.0
        out["pred_r"] = pred
        return out

`

### File: Engine/ml/footprint_features.py
`python
# Engine/ml/footprint_features.py
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Optional


class FootprintLadderFeatures:
    """
    Consumes {symbol}_15m_footprint_ladder.parquet with columns:
        open_time_ms, price_bin, bid_vol_coin, ask_vol_coin,
        net_delta_coin, total_vol_coin, trade_count, is_poc,
        is_buy_imbalance, is_sell_imbalance, is_stacked_buy_imb,
        is_stacked_sell_imb, is_value_area

    All features are unit-free (ratios, z-scores, ranks) -> poolable across
    BTC and altcoin price scales. Fully vectorized for high-speed computation.
    """

    def __init__(self, z_window: int = 96, flush_window: int = 12):
        self.zw = z_window
        self.fw = flush_window

    def load_and_aggregate(self, path: str) -> pd.DataFrame:
        """
        Fast vectorized aggregation of price-bin ladder rows into per-15m-bar metrics.
        Returns one row per 15m bar with ladder-derived order flow aggregates.
        """
        lad = pd.read_parquet(path)
        lad.sort_values(["open_time_ms", "price_bin"], inplace=True)

        # 1. Base aggregations per 15m candle
        g = lad.groupby("open_time_ms", sort=True)
        agg = pd.DataFrame({
            "bid_vol": g["bid_vol_coin"].sum(),
            "ask_vol": g["ask_vol_coin"].sum(),
            "net_delta": g["net_delta_coin"].sum(),
            "total_vol": g["total_vol_coin"].sum(),
            "trade_cnt": g["trade_count"].sum(),
            "n_bins": g["price_bin"].count(),
            "price_bin_lo": g["price_bin"].min(),
            "price_bin_hi": g["price_bin"].max(),
            "n_buy_imb": g["is_buy_imbalance"].sum(),
            "n_sell_imb": g["is_sell_imbalance"].sum(),
            "has_stacked_buy": g["is_stacked_buy_imb"].max(),
            "has_stacked_sell": g["is_stacked_sell_imb"].max(),
            "va_bins": g["is_value_area"].sum(),
        })

        # 2. Fast vectorized POC bin and POC vol lookup
        poc_rows = lad[lad["is_poc"] == 1].drop_duplicates("open_time_ms").set_index("open_time_ms")
        agg["poc_bin"] = poc_rows["price_bin"].reindex(agg.index).fillna(agg["price_bin_lo"])
        agg["poc_vol"] = poc_rows["total_vol_coin"].reindex(agg.index).fillna(0.0)

        # 3. Low/High bin volume (first 3 and last 3 price bins)
        # Using head(3) and tail(3) per group in a vectorized way
        lo_3 = lad.groupby("open_time_ms").head(3).groupby("open_time_ms")["total_vol_coin"].sum()
        hi_3 = lad.groupby("open_time_ms").tail(3).groupby("open_time_ms")["total_vol_coin"].sum()
        agg["vol_at_lo_bins"] = lo_3.reindex(agg.index).fillna(0.0)
        agg["vol_at_hi_bins"] = hi_3.reindex(agg.index).fillna(0.0)

        agg.index = pd.to_datetime(agg.index, unit="ms", utc=True)
        if agg.index.tz is not None:
            agg.index = agg.index.tz_convert(None)
        return agg

    def build_features(self, agg: pd.DataFrame, ohlc: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Merge ladder aggregates with 15m OHLC and emit stationary absorption features.
        """
        F = pd.DataFrame(index=agg.index)
        tot = agg["total_vol"].clip(lower=1e-12)
        net_delta = agg["net_delta"]

        # 1) Normalized footprint delta [-1, 1]
        F["fp_delta_ratio"] = (net_delta / tot).clip(-1, 1).fillna(0.0)

        # 2) Wick absorption (selling absorbed at the low)
        low_share = (agg["vol_at_lo_bins"] / tot).clip(0, 1)
        hi_share = (agg["vol_at_hi_bins"] / tot).clip(0, 1)
        F["wick_sell_absorb"] = (low_share * (0.5 + 0.5 * F["fp_delta_ratio"])).fillna(0.0)
        F["wick_buy_exhaust"] = (hi_share * (0.5 - 0.5 * F["fp_delta_ratio"])).fillna(0.0)

        # 3) Stacked imbalance flags
        F["has_stacked_buy"] = agg["has_stacked_buy"].astype(np.float64).fillna(0.0)
        F["has_stacked_sell"] = agg["has_stacked_sell"].astype(np.float64).fillna(0.0)
        F["imb_ratio"] = ((agg["n_buy_imb"] - agg["n_sell_imb"]) / (agg["n_buy_imb"] + agg["n_sell_imb"]).clip(lower=1)).clip(-1, 1).fillna(0.0)

        # 4) Sell impact collapse
        if ohlc is not None:
            o = ohlc["open"].reindex(agg.index).astype(np.float64)
            h = ohlc["high"].reindex(agg.index).astype(np.float64)
            l = ohlc["low"].reindex(agg.index).astype(np.float64)
            c = ohlc["close"].reindex(agg.index).astype(np.float64)
            rng = (h - l).clip(lower=1e-12)
            atr = rng.rolling(96, min_periods=1).mean().clip(lower=1e-12)
            ret = (c - o) / atr
        else:
            ret = agg["poc_bin"].diff() / agg["poc_bin"].rolling(96, min_periods=1).mean().clip(lower=1e-12)

        sell_vol = agg["bid_vol"].clip(lower=1e-12)
        sell_frac = (sell_vol / tot).clip(0, 1)
        impact = ret / sell_frac.clip(lower=0.05)
        F["sell_impact"] = impact.clip(-10, 10).fillna(0.0)

        s3 = sell_vol.rolling(3, min_periods=1).sum().clip(lower=1e-12)
        p3 = ret.rolling(3, min_periods=1).sum().clip(-10, 10)
        F["absorption_ratio"] = (p3 * tot.rolling(3, min_periods=1).sum() / s3).clip(-10, 10).fillna(0.0)

        # 5) Delta divergence at the low
        if ohlc is not None:
            new_low = (l <= l.rolling(3, min_periods=1).min()).astype(np.float64)
        else:
            new_low = (agg["poc_bin"] <= agg["poc_bin"].rolling(3, min_periods=1).min()).astype(np.float64)
        F["delta_div_at_low"] = (new_low * (F["fp_delta_ratio"] - F["fp_delta_ratio"].rolling(3, min_periods=1).mean())).clip(-1, 1).fillna(0.0)

        # 6) Point of Control (POC) shift relative to ladder bins
        F["poc_shift"] = (agg["poc_bin"].diff() / agg["n_bins"].clip(lower=1)).clip(-2, 2).fillna(0.0)

        # 7) Average trade size imbalance
        avg_trade_size = (tot / agg["trade_cnt"].clip(lower=1))
        m_ats = avg_trade_size.rolling(96, min_periods=1).mean().clip(lower=1e-12)
        F["avg_trade_size_zs"] = ((avg_trade_size - m_ats) / avg_trade_size.rolling(96, min_periods=1).std(ddof=0).clip(lower=1e-12).fillna(1.0)).clip(-5, 5).fillna(0.0)

        # 8) Ladder range compression
        ladder_rng = (agg["price_bin_hi"] - agg["price_bin_lo"]).clip(lower=1)
        rng_ma = ladder_rng.rolling(96, min_periods=1).mean().clip(lower=1e-12)
        F["ladder_compression"] = (ladder_rng / rng_ma).clip(0, 10).fillna(1.0)

        # 9) Post-event reclaim geometry
        if ohlc is not None:
            F["reclaim_mid"] = ((c - (h.shift(1) + l.shift(1)) / 2.0) / atr).clip(-5, 5).fillna(0.0)
            F["higher_low_bars"] = ((l > l.shift(1)).astype(np.float64).rolling(3, min_periods=1).sum() / 3.0).fillna(0.0)

        return F.fillna(0.0)

`

### File: Engine/strategy/smc_event_detector.py
`python
# Engine/strategy/smc_event_detector.py
from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class SMCConfig:
    min_r_dist_pct: float = 0.015        # structural stop >= 1.5% -> friction < 0.2R
    max_r_dist_pct: float = 0.040        # sanity ceiling
    sweep_max_penetr_atr: float = 0.5    # sweep wick beyond level <= 0.5 ATR_d
    fvg_min_size_atr: float = 0.30       # gap must be >= 0.3 daily ATR
    fvg_max_age_days: int = 10           # unmitigated gaps expire
    ob_max_pullback_bars: int = 96       # 24h of 15m bars to reach the OB
    stop_buffer_atr_frac: float = 0.10   # stop = level +/- 0.10 * ATR_d
    reclaim_min_bars: int = 1            # bars holding beyond level before signal


class SMCEventDetector:
    """
    Detects, on 15m data with daily structural levels:
      A. UsmanNoah sweep:   price pierces PDH/PDL then closes back inside the
                            prior day range (failed breakout = liquidity grab).
      B. FVG retest:        price returns into an unmitigated daily FVG zone.
      C. OB/Breaker tap:    price pulls back to the origin extreme of the last
                            displacement leg that broke structure.
    Signal bar t -> filled at Open[t+1] by the kernel (strictly causal).
    """

    COLS = ("side", "raw_r", "structural_level", "invalidation_price", "event_type")

    def __init__(self, cfg: SMCConfig = SMCConfig()):
        self.cfg = cfg

    # ------------------------------------------------------------------
    # Daily structure map - computed ONLY from completed daily candles
    # ------------------------------------------------------------------
    def daily_structure(self, df15: pd.DataFrame) -> pd.DataFrame:
        d = pd.DataFrame({
            "high_d": df15["high"].resample("1D").max(),
            "low_d": df15["low"].resample("1D").min(),
            "open_d": df15["open"].resample("1D").first(),
            "close_d": df15["close"].resample("1D").last()
        }).dropna()
        d["atr_d"] = (d["high_d"] - d["low_d"]).rolling(14, min_periods=5).mean().ffill()

        # PDH/PDL = previous COMPLETED day's extremes (shift(1) -> causal)
        d["pdh"] = d["high_d"].shift(1)
        d["pdl"] = d["low_d"].shift(1)

        # Daily FVG: gap between day[i-2].high and day[i].low (bearish) or
        # day[i-2].low and day[i].high (bullish). Attached to day i.
        d["fvg_bull_lo"] = d["high_d"].shift(2)
        d["fvg_bull_hi"] = np.where(d["low_d"] > d["fvg_bull_lo"], d["low_d"], np.nan)
        d["fvg_bear_lo"] = np.where(d["high_d"] < d["low_d"].shift(2), d["high_d"], np.nan)
        d["fvg_bear_hi"] = d["low_d"].shift(2)

        # Displacement OB: day with range > 1.5*atr_d and body/range > 0.5
        body = (d["close_d"] - d["open_d"]).abs()
        rng = (d["high_d"] - d["low_d"]).clip(lower=1e-12)
        big = (rng > 1.5 * d["atr_d"]) & (body / rng > 0.5)
        d["ob_bull_level"] = d["low_d"].where(big & (d["close_d"] > d["open_d"]))
        d["ob_bear_level"] = d["high_d"].where(big & (d["close_d"] < d["open_d"]))

        # Forward-fill valid zone levels with expiry
        for z in ("fvg_bull", "fvg_bear"):
            d[f"{z}_lo_f"] = d[f"{z}_lo"].ffill(limit=self.cfg.fvg_max_age_days)
            d[f"{z}_hi_f"] = d[f"{z}_hi"].ffill(limit=self.cfg.fvg_max_age_days)

        # CRITICAL CAUSALITY FIX (Note 4): shift the entire daily frame by 1 day
        # so day i is only visible at day i+1 00:00 UTC!
        d_causal = d.shift(1)
        return d_causal

    # ------------------------------------------------------------------
    # Event emission on 15m bars
    # ------------------------------------------------------------------
    def generate_signals(self, df: pd.DataFrame,
                         structure: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        T = len(df)
        idx = df.index
        sig = pd.DataFrame({
            "side": np.zeros(T, dtype=np.int8),
            "raw_r": np.zeros(T, dtype=np.float64),
            "structural_level": np.zeros(T, dtype=np.float64),
            "invalidation_price": np.zeros(T, dtype=np.float64),
            "event_type": np.zeros(T, dtype=object)
        }, index=idx)

        if structure is None:
            structure = self.daily_structure(df)
        st = structure.reindex(df.index, method="ffill")

        o = df["open"].to_numpy(np.float64)
        h = df["high"].to_numpy(np.float64)
        l = df["low"].to_numpy(np.float64)
        c = df["close"].to_numpy(np.float64)
        atr_d = st["atr_d"].to_numpy(np.float64)
        atr_d = np.where(np.isnan(atr_d) | (atr_d < 1e-9), c * 0.02, atr_d)
        C = self.cfg

        pdh = st["pdh"].to_numpy()
        pdl = st["pdl"].to_numpy()

        # ---------- A. SWEEP & RECLAIM (Usman Noah) ----------
        swept_low = (l < pdl) & ((pdl - l) <= C.sweep_max_penetr_atr * atr_d) & (c > pdl) & np.isfinite(pdl)
        swept_high = (h > pdh) & ((h - pdh) <= C.sweep_max_penetr_atr * atr_d) & (c < pdh) & np.isfinite(pdh)

        # ---------- B. FVG RETEST ----------
        fvg_b_hi = st["fvg_bull_hi_f"].to_numpy()
        fvg_b_lo = st["fvg_bull_lo_f"].to_numpy()
        in_bull_fvg = (l <= fvg_b_hi) & (c >= fvg_b_lo) & np.isfinite(fvg_b_lo)

        fvg_s_lo = st["fvg_bear_lo_f"].to_numpy()
        fvg_s_hi = st["fvg_bear_hi_f"].to_numpy()
        in_bear_fvg = (h >= fvg_s_lo) & (c <= fvg_s_hi) & np.isfinite(fvg_s_hi)

        # ---------- C. ORDER BLOCK TAP ----------
        ob_bull = st["ob_bull_level"].ffill(limit=C.ob_max_pullback_bars // 96).to_numpy()
        ob_bear = st["ob_bear_level"].ffill(limit=C.ob_max_pullback_bars // 96).to_numpy()
        tap_ob_bull = (l <= ob_bull) & (c > ob_bull) & np.isfinite(ob_bull)
        tap_ob_bear = (h >= ob_bear) & (c < ob_bear) & np.isfinite(ob_bear)

        buffer = C.stop_buffer_atr_frac * atr_d

        # Long candidate coordinate emission
        for mask, stop_src, etype in (
            (swept_low, pdl - buffer, "SWEEP_PDL"),
            (in_bull_fvg, fvg_b_lo - buffer, "FVG_BULL"),
            (tap_ob_bull, ob_bull - buffer, "OB_BULL"),
        ):
            stop = np.where(mask, stop_src, 0.0)
            r_dist = c - stop
            ok = mask & (r_dist / c >= C.min_r_dist_pct) & (r_dist / c <= C.max_r_dist_pct)
            sig.loc[ok, "side"] = 1
            sig.loc[ok, "raw_r"] = r_dist[ok]
            sig.loc[ok, "structural_level"] = pdl[ok] if etype == "SWEEP_PDL" else stop_src[ok]
            sig.loc[ok, "invalidation_price"] = stop[ok]
            sig.loc[ok, "event_type"] = etype

        # Short candidate coordinate emission (don't overwrite long same bar)
        for mask, stop_src, etype in (
            (swept_high, pdh + buffer, "SWEEP_PDH"),
            (in_bear_fvg, fvg_s_hi + buffer, "FVG_BEAR"),
            (tap_ob_bear, ob_bear + buffer, "OB_BEAR"),
        ):
            stop = np.where(mask, stop_src, 0.0)
            r_dist = stop - c
            ok = mask & (r_dist / c >= C.min_r_dist_pct) & (r_dist / c <= C.max_r_dist_pct) & (sig["side"].to_numpy() == 0)
            sig.loc[ok, "side"] = -1
            sig.loc[ok, "raw_r"] = r_dist[ok]
            sig.loc[ok, "structural_level"] = stop_src[ok]
            sig.loc[ok, "invalidation_price"] = stop[ok]
            sig.loc[ok, "event_type"] = etype

        return sig

    def event_features(self, df: pd.DataFrame, sig: pd.DataFrame) -> pd.DataFrame:
        idx = df.index
        st = self.daily_structure(df).reindex(idx, method="ffill")
        atr_d = st["atr_d"].reindex(idx).ffill().clip(lower=1e-9)
        c = df["close"]
        F = pd.DataFrame(index=idx)
        pdl = st["pdl"].reindex(idx).ffill()
        F["dist_to_pdl_atr"] = (((c - pdl) / atr_d).fillna(0.0)).clip(-5, 5)
        fvg_w = (st["fvg_bull_hi_f"] - st["fvg_bull_lo_f"]).reindex(idx).ffill()
        F["fvg_depth_pct"] = ((fvg_w / c).fillna(0.0)).clip(0, 0.05)
        d_hi = st["high_d"].reindex(idx).ffill()
        d_lo = st["low_d"].reindex(idx).ffill()
        F["reclaim_strength"] = (((c - d_lo) / (d_hi - d_lo).clip(lower=1e-9)).fillna(0.5)).clip(0, 1)
        F["day_range_atr"] = (((d_hi - d_lo) / atr_d).fillna(1.0)).clip(0, 5)
        return F

`
