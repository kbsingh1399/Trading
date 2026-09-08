# OX ALPHA — ROUND 5: THE EXTREME INSTITUTIONAL-GRADE QUANTITATIVE MASTER ENGINE
## Empirical Audit of All 8 Strategies Across All 20 OOS Windows & Complete Source Code Implementation

> **CRITICAL EXECUTIVE BRIEFING FOR OX ALPHA QUANTITATIVE ARCHITECT:**
> We have completed the full 20-window walk-forward empirical audit across **ALL 8 STRATEGIES** (`S1_LiqCascade`, `S2_InstML`, `SMC_Edgeful`, `SMC_Kane`, `SMC_Marci`, `SMC_Marco`, `SMC_Mayne`, `SMC_UsmanNoah`) on our 18-asset Binance USDT-M Perpetual dataset (3.47M 15m bars, Tier-1 "A-" audit verified by Arena.ai).
>
> We evaluated both:
> 1. **Single-Asset BTCUSDT Benchmark** across all 20 Out-of-Sample (OOS) windows (2021–2026).
> 2. **18-Asset Multi-Symbol Institutional Portfolio** (shared $5,000 capital, max 2 concurrent positions, 4.5% hard drawdown breaker, 33 bps real taker frictions: 8 bps fee, 10 bps entry slippage, 15 bps exit slippage).
>
> **THE UNVARNISHED EMPIRICAL REALITY: ALL 8 STRATEGIES FAILED ALL 20 WINDOWS (0/20 PASSES).**
> Not a single strategy passed a single window under real frictions and institutional risk sizing.
> We need an **extreme institutional-level solution that definitely will work** to achieve the target pass criteria:
> - **Net ROI > +20.0%** per 1-month window ($1,000 net profit on $5,000 capital).
> - **Max Drawdown < 5.0%** (Hard circuit breaker stop at 4.5% / $225).
> - **Win Rate > 40.0%**.
> - **Min Trades >= 6** completed trades per window.
> - **Causal Execution:** Signal at bar $j$ close -> filled at Open[j+1]. Conservative stop-first intrabar checking.
>
> **NOTE ON OFFLINE EXECUTION:** All our production source code files are embedded in full directly in Section 5 below. You have immediate offline access to the complete code base.

---

## 1. THE 20-WINDOW EMPIRICAL BENCHMARK SCORECARD (ALL 8 STRATEGIES)

### 1.1 BTCUSDT Single-Asset Benchmark (All 20 OOS Windows, 33 bps Frictions):
| Strategy | Windows Passed | Total Trades | Net PnL ($) | Cum ROI (%) | Max DD (%) | Win Rate (%) | Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `S1_LiqCascade` | **0/20** | 180 | $-1,908.18 | -38.16% | 3.80% | 19.4% | FAIL |
| `S2_InstML` | **0/20** | 408 | $-3,148.04 | -62.96% | 4.74% | 38.7% | FAIL |
| `SMC_Edgeful` | **0/20** | 465 | $-4,501.61 | -90.03% | 4.78% | 26.7% | FAIL |
| `SMC_Kane` | **0/20** | 484 | $-4,284.31 | -85.69% | 4.60% | 29.3% | FAIL |
| `SMC_Marci` | **0/20** | 321 | $-2,620.65 | -52.41% | 4.53% | 24.3% | FAIL |
| `SMC_Marco` | **0/20** | 436 | $-4,394.43 | -87.89% | 4.67% | 18.8% | FAIL |
| `SMC_Mayne` | **0/20** | 464 | $-4,404.22 | -88.08% | 4.77% | 25.4% | FAIL |
| `SMC_UsmanNoah` | **0/20** | 82 | $-922.24 | -18.44% | 3.22% | 29.3% | FAIL |

### 1.2 18-Asset Multi-Asset Institutional Portfolio (Shared $5k, Max 2 Concurrent Positions, 4.5% Breaker):
| Portfolio Strategy | Windows Passed | Total Trades | Net PnL ($) | Cum ROI (%) | Max DD (%) | Win Rate (%) | Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Portfolio S1_LiqCascade` | **0/20** | 599 | $-4,232.48 | -84.65% | 5.08% | 28.9% | FAIL |
| `Portfolio S2_InstML` | **0/20** | 624 | $-3,848.49 | -76.97% | 4.73% | 26.3% | FAIL |
| `Portfolio SMC_Edgeful` | **0/20** | 600 | $-4,001.88 | -80.04% | 4.78% | 25.7% | FAIL |
| `Portfolio SMC_Kane` | **0/20** | 551 | $-4,279.37 | -85.59% | 4.94% | 23.6% | FAIL |
| `Portfolio SMC_Marci` | **0/20** | 545 | $-4,186.13 | -83.72% | 4.86% | 22.0% | FAIL |
| `Portfolio SMC_Marco` | **0/20** | 480 | $-4,386.52 | -87.73% | 4.83% | 19.0% | FAIL |
| `Portfolio SMC_Mayne` | **0/20** | 557 | $-3,893.16 | -77.86% | 4.95% | 25.9% | FAIL |
| `Portfolio SMC_UsmanNoah` | **0/20** | 657 | $-3,280.00 | -65.60% | 4.76% | 32.3% | FAIL |

### 1.3 Window-by-Window Historical Breakdown (BTCUSDT, Windows 1 to 20):
| Win ID | Window Name | Dates | Usman Noah | S1 Cascade | S2 InstML | Marci | Marco | Edgeful | Kane | Mayne |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| W01 | May 2021 Great Liquidation Crash | 2021-05-01 to 2021-05-31 | -0.92% | -2.48% | -3.92% | -1.00% | -4.67% | -4.53% | -4.42% | -4.50% |
| W02 | September 2021 El Salvador Flash Crash | 2021-09-01 to 2021-09-30 | +1.78% | -2.97% | -3.12% | -3.89% | -4.65% | -4.78% | -3.84% | -4.58% |
| W03 | November 2021 Cycle Peak Reversal | 2021-11-01 to 2021-11-30 | -1.34% | -2.85% | -4.56% | -3.18% | -4.18% | -4.50% | -3.71% | -3.97% |
| W04 | January 2022 Fed Macro Tightening | 2022-01-01 to 2022-01-31 | -0.41% | -3.22% | -1.33% | -1.12% | -4.51% | -4.51% | -4.60% | -4.77% |
| W05 | May 2022 Terra-Luna Systemic Shock | 2022-05-01 to 2022-05-31 | -0.39% | -3.17% | -2.83% | -1.63% | -3.06% | -4.55% | -4.52% | -4.49% |
| W06 | June 2022 3AC & Celsius Capitulation | 2022-06-01 to 2022-06-30 | +0.00% | -2.30% | -3.50% | -1.79% | -4.33% | -4.55% | -2.94% | -4.54% |
| W07 | September 2022 ETH Merge Chop & Grind | 2022-09-01 to 2022-09-30 | -0.98% | -2.77% | -4.51% | -2.15% | -4.27% | -4.61% | -3.95% | -4.51% |
| W08 | November 2022 FTX Collapse Bottom | 2022-11-01 to 2022-11-30 | -2.50% | -2.96% | -3.96% | -0.05% | -4.60% | -4.51% | -4.08% | -4.57% |
| W09 | January 2023 Bullish Short Squeeze Recovery | 2023-01-01 to 2023-01-31 | +0.60% | -1.40% | -3.03% | -3.84% | -4.62% | -4.62% | -4.59% | -4.54% |
| W10 | March 2023 SVB Bank Run & USDC Depeg | 2023-03-01 to 2023-03-31 | -2.39% | +0.70% | -0.63% | -3.06% | -4.17% | -4.52% | -4.17% | -4.56% |
| W11 | June 2023 BlackRock Spot ETF Momentum | 2023-06-01 to 2023-06-30 | +0.09% | -2.98% | -4.50% | -1.47% | -4.29% | -4.53% | -4.54% | -4.30% |
| W12 | August 2023 Mid-Summer Flash Liquidation | 2023-08-01 to 2023-08-31 | -1.82% | +1.46% | -4.74% | -4.51% | -4.51% | -4.46% | -4.57% | -4.59% |
| W13 | October 2023 Uptober Spot ETF Ignition | 2023-10-01 to 2023-10-31 | -2.52% | -0.86% | -1.64% | -4.26% | -4.57% | -4.51% | -4.18% | -4.63% |
| W14 | January 2024 Spot ETF Approval Shakeout | 2024-01-01 to 2024-01-31 | -0.74% | +0.26% | -3.83% | -4.17% | -4.63% | -3.86% | -4.38% | -4.57% |
| W15 | March 2024 Pre-Halving All-Time High Run | 2024-03-01 to 2024-03-31 | -0.59% | -2.06% | -1.47% | -4.52% | -4.63% | -4.58% | -4.53% | -4.10% |
| W16 | August 2024 Global Carry Trade Liquidation | 2024-08-01 to 2024-08-31 | -3.22% | -0.97% | -3.83% | -0.42% | -4.54% | -4.35% | -4.58% | -3.36% |
| W17 | November 2024 US Election Mega Breakout | 2024-11-01 to 2024-11-30 | -1.03% | -2.15% | -0.15% | -1.60% | -4.48% | -4.50% | -4.58% | -4.49% |
| W18 | February 2025 Post-Inauguration Consolidation | 2025-02-01 to 2025-02-28 | -1.01% | -2.41% | -3.10% | -2.31% | -4.55% | -4.58% | -4.37% | -4.18% |
| W19 | July 2025 Mid-Year Volatility Expansion | 2025-07-01 to 2025-07-31 | -0.04% | -3.80% | -4.28% | -3.82% | -4.58% | -4.53% | -4.60% | -4.51% |
| W20 | March 2026 Late-Cycle Microstructure Shock | 2026-03-01 to 2026-03-31 | -1.00% | -1.25% | -4.04% | -3.63% | -4.05% | -4.44% | -4.53% | -4.33% |

---

## 2. THE ANATOMICAL ROOT CAUSE OF FAILURE

### 2.1 The 15-Minute Taker Friction Tax (0.55R Drag)
- On a 15-minute chart, stops are 0.50% to 0.70% away (1R ≈ 0.60%).
- Paying 33 bps round-trip (8 bps taker fee + 10 bps entry slippage + 15 bps exit slippage) consumes 0.40R to 0.66R on EVERY trade before price moves 1 pip.
- Mathematically, at a 30% win rate and 2.5R target:
  E[R] = (0.30 * 2.5R) - (0.70 * 1.0R) - 0.55R = 0.75 - 0.70 - 0.55 = -0.50R
- Every trade is fundamentally negative expectancy. No classifier or stop loss can save a strategy bleeding 0.50R on entry.

### 2.2 Unfiltered Event Churn (Over-Trading the Noise)
- In the 18-asset portfolio, strategies generated between 480 and 657 trades over the 20 months (~25 to 33 trades per month).
- Because each trade had negative expectancy under taker frictions, taking 30 trades in a 30-day month guaranteed triggering the 4.5% ($225) hard drawdown breaker.

### 2.3 The Single-Bar Confirmation Trap (Event Starvation)
- In our Round 4 prototype, requiring a sweep + reclaim AND >= 3/6 footprint conditions on that exact 15m bar reduced events to only ~0.8 per asset per month, leading to sample starvation and 0 trades in slow regimes.

---

## 3. WHAT WE DEMAND FROM OX ALPHA: AN EXTREME INSTITUTIONAL LEVEL SOLUTION

We need an elite quantitative architect solution that solves these structural math problems permanently. We demand the following 5 institutional pillars:

### Pillar 1: Multi-Timeframe Structural Geometry (1R >= 1.8% - 3.0%)
- Invalidation stops MUST anchor to 4H / Daily swing extremes (PDH/PDL sweeps, 4H Order Blocks, Daily Fair Value Gaps).
- At a 2.2% stop distance, 33 bps round-trip = 0.15R friction drag (slashing drag by 73% compared to 0.55R).
- With 1R = 2.2%, reaching a +2.2R target requires a +4.84% trend expansion — completely natural during volatility shocks.

### Pillar 2: Cross-Sectional Dispersion & Relative Strength Ranking
- Do NOT evaluate symbols in isolation.
- At each bar j, compute a cross-sectional score across all 18 assets:
  Score_i = z(Footprint Absorption) + z(CVD Divergence) + z(Volume Surge) + z(Funding Squeeze)
- Only permit entries on the Top 1 or 2 highest-conviction outliers across the entire 18-asset universe. Filter out 90% of mediocre chop.

### Pillar 3: Passive Limit Order Execution Geometry (Maker vs Taker)
- Institutional desks do not buy market into liquidity flushes. They place resting limit orders inside the sweep zone / FVG retest.
- How do we causally model passive limit fills at P_limit with realistic execution probabilities and zero entry slippage (saving 10 bps)?

### Pillar 4: Anti-Retracement Microstructure Exit Ratchet
- In crypto perp shocks, 85% of winning moves retrace after reaching +1.0R to +1.5R.
- Provide the exact RatchetConfig:
  - Breakeven lock (+0.15R) at +0.8R.
  - Profit lock (+0.80R) at +1.5R.
  - Target exit at +2.2R - +2.5R.
  - Time decay exit: close at market if trade fails to gain +0.2R within 24–36 bars.

### Pillar 5: Complete Production Master Engine (Engine/strategy/institutional_alpha_master.py)
- Provide the complete, drop-in Python source code for the Master Engine.
- Must import from our existing production codebase:
  - from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig
  - from Engine.core.portfolio_execution_kernel import PortfolioExecutionKernel
  - from Engine.ml.footprint_features import FootprintLadderFeatures
  - from Engine.ml.rf_meta_labeler import RegressionRMetaLabeler
- Must include a clean, unified walk-forward runner that runs across all 20 windows and definitively passes them.

---

## 4. CODE REPOSITORY INTERFACES & FORMAT SPECIFICATION

Your response should follow the exact interfaces established in Rounds 1–4:
- All features must be backward-looking (shift(1) for daily bars, zero forward leakage).
- All fills must execute strictly at Open[j+1].
- Risk sizing: Base Risk $25.00 (0.50%), House Money $50.00 (1.00%), Defense Risk $15.00 (0.30%), Hard DD Breaker 4.5% ($225), Max 2 Concurrent Positions across 18 assets.
- Provide clean, robust, vectorized Python code that we can immediately save and run.

---

## 5. FULL SOURCE CODE IMPLEMENTATIONS (OFFLINE SELF-CONTAINED)

To ensure you have 100% offline access to all our active modules, the complete production files are provided below:

### 5.1 `Engine/core/execution_kernel.py`
```python
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
        pending_raw_r = 0.0

        if signal_side[0] != 0:
            pending_side = int(signal_side[0])
            pending_raw_r = float(signal_raw_r[0])

        for t in range(1, T):
            # 1) Fill pending signal at this bar's open
            if pending_side != 0:
                net_profit = realized - self.risk.initial_capital
                current_dd = (peak - realized) / peak if peak > 0 else 0.0

                if (not training_mode) and current_dd >= self.risk.drawdown_limit:
                    pending_side = 0
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

            # 2) Intrabar exit evaluation
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
                    elif l_ <= self._pos_stop:
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
                    elif h_ >= self._pos_stop:
                        exit_px = self._pos_stop * (1.0 + self.fric.exit_slippage)
                        exit_reason = "STOP_BAR"
                    elif l_ <= self._pos_target:
                        exit_px = self._pos_target
                        exit_reason = "TARGET_BAR"

                if exit_reason:
                    realized = self._close_trade(t, exit_px, exit_reason, realized, trades)
                else:
                    self._apply_ratchet(h_, l_)
                    if (t - self._pos_bar) >= self.ratchet.time_decay_bars and self._pos_max_r < self.ratchet.time_decay_r:
                        realized = self._close_trade(t, c_, "TIME_DECAY", realized, trades)

            # 3) Mark-to-market equity & DD gate
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

            # 4) Signal on bar t becomes PENDING for bar t+1
            if t < T - 1 and self._pos_side == 0:
                sig = signal_side[t]
                if sig != 0:
                    pending_side = int(sig)
                    pending_raw_r = float(signal_raw_r[t])

            # 5) Terminal settlement
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
```

---

### 5.2 `Engine/core/portfolio_execution_kernel.py`
```python
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
        pending: Dict[str, tuple] = {}

        op = {s: data[s]["open"].values for s in self.symbols if s in data}
        hi = {s: data[s]["high"].values for s in self.symbols if s in data}
        lo = {s: data[s]["low"].values for s in self.symbols if s in data}
        cl = {s: data[s]["close"].values for s in self.symbols if s in data}
        sig_side = {s: gated_signals[s]["side"].values for s in self.symbols if s in gated_signals}
        sig_rr = {s: gated_signals[s]["raw_r"].values for s in self.symbols if s in gated_signals}

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

            if t < T - 1:
                for sym in self.symbols:
                    if sym in sig_side and t < len(sig_side[sym]):
                        s_ = int(sig_side[sym][t])
                        if s_ != 0 and sym not in positions and sym not in pending:
                            pending[sym] = (s_, float(sig_rr[sym][t]))

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
```

---

### 5.3 `Engine/strategy/smc_event_detector.py`
```python
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
    COLS = ("side", "raw_r", "structural_level", "invalidation_price", "event_type")

    def __init__(self, cfg: SMCConfig = SMCConfig()):
        self.cfg = cfg

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

        # Daily FVG
        d["fvg_bull_lo"] = d["high_d"].shift(2)
        d["fvg_bull_hi"] = np.where(d["low_d"] > d["fvg_bull_lo"], d["low_d"], np.nan)
        d["fvg_bear_lo"] = np.where(d["high_d"] < d["low_d"].shift(2), d["high_d"], np.nan)
        d["fvg_bear_hi"] = d["low_d"].shift(2)

        # Displacement OB
        body = (d["close_d"] - d["open_d"]).abs()
        rng = (d["high_d"] - d["low_d"]).clip(lower=1e-12)
        big = (rng > 1.5 * d["atr_d"]) & (body / rng > 0.5)
        d["ob_bull_level"] = d["low_d"].where(big & (d["close_d"] > d["open_d"]))
        d["ob_bear_level"] = d["high_d"].where(big & (d["close_d"] < d["open_d"]))

        for z in ("fvg_bull", "fvg_bear"):
            d[f"{z}_lo_f"] = d[f"{z}_lo"].ffill(limit=self.cfg.fvg_max_age_days)
            d[f"{z}_hi_f"] = d[f"{z}_hi"].ffill(limit=self.cfg.fvg_max_age_days)

        return d.shift(1)  # Shift entire daily frame by 1 day for strict causality

    def generate_signals(self, df: pd.DataFrame, structure: Optional[pd.DataFrame] = None) -> pd.DataFrame:
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

        swept_low = (l < pdl) & ((pdl - l) <= C.sweep_max_penetr_atr * atr_d) & (c > pdl) & np.isfinite(pdl)
        swept_high = (h > pdh) & ((h - pdh) <= C.sweep_max_penetr_atr * atr_d) & (c < pdh) & np.isfinite(pdh)

        fvg_b_hi = st["fvg_bull_hi_f"].to_numpy()
        fvg_b_lo = st["fvg_bull_lo_f"].to_numpy()
        in_bull_fvg = (l <= fvg_b_hi) & (c >= fvg_b_lo) & np.isfinite(fvg_b_lo)

        fvg_s_lo = st["fvg_bear_lo_f"].to_numpy()
        fvg_s_hi = st["fvg_bear_hi_f"].to_numpy()
        in_bear_fvg = (h >= fvg_s_lo) & (c <= fvg_s_hi) & np.isfinite(fvg_s_hi)

        ob_bull = st["ob_bull_level"].ffill(limit=C.ob_max_pullback_bars // 96).to_numpy()
        ob_bear = st["ob_bear_level"].ffill(limit=C.ob_max_pullback_bars // 96).to_numpy()
        tap_ob_bull = (l <= ob_bull) & (c > ob_bull) & np.isfinite(ob_bull)
        tap_ob_bear = (h >= ob_bear) & (c < ob_bear) & np.isfinite(ob_bear)

        buffer = C.stop_buffer_atr_frac * atr_d

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
```

---

### 5.4 `Engine/ml/footprint_confirmation.py`
```python
import numpy as np
import pandas as pd

class FootprintConfirmation:
    def __init__(self, min_score: int = 3):
        self.min_score = min_score

    @staticmethod
    def _zs(s: pd.Series, w: int = 96) -> np.ndarray:
        m = s.rolling(w, min_periods=1).mean()
        sd = s.rolling(w, min_periods=1).std(ddof=0).replace(0.0, np.nan).ffill().fillna(1.0)
        return ((s - m) / sd).fillna(0.0).clip(-5, 5).to_numpy()

    def confirm(self, df: pd.DataFrame, sig: pd.DataFrame,
                ladder_feats: pd.DataFrame) -> pd.DataFrame:
        out = sig.copy()
        T = len(df)
        lf = ladder_feats.reindex(df.index).fillna(0.0)

        wsa_z = self._zs(lf.get("wick_sell_absorb", pd.Series(0.0, index=df.index)))
        wbe_z = self._zs(lf.get("wick_buy_exhaust", pd.Series(0.0, index=df.index)))
        abs_ratio = lf.get("absorption_ratio", pd.Series(0.0, index=df.index)).to_numpy()
        absr_z = self._zs(pd.Series(abs_ratio, index=df.index))
        poc_z = self._zs(lf.get("poc_shift", pd.Series(0.0, index=df.index)))
        close_pos = lf.get("close_pos", pd.Series(0.0, index=df.index)).to_numpy()
        side = out["side"].to_numpy()

        stacked_buy = df.get("is_stacked_buy_imb",
                             pd.Series(np.zeros(T), index=df.index)).to_numpy().astype(bool)
        stacked_sell = df.get("is_stacked_sell_imb",
                              pd.Series(np.zeros(T), index=df.index)).to_numpy().astype(bool)
        sb2 = stacked_buy | np.concatenate([[False], stacked_buy[:-1]])
        ss2 = stacked_sell | np.concatenate([[False], stacked_sell[:-1]])

        score = np.zeros(T, dtype=np.int8)
        long_m = side == 1
        short_m = side == -1

        score += (long_m & (wsa_z >= 1.0)).astype(np.int8)
        score += (short_m & (wbe_z >= 1.0)).astype(np.int8)
        score += (long_m & (absr_z >= 0.5) & (abs_ratio > 0)).astype(np.int8)
        score += (short_m & (absr_z <= -0.5) & (abs_ratio < 0)).astype(np.int8)
        score += (long_m & (poc_z >= 0.3)).astype(np.int8)
        score += (short_m & (poc_z <= -0.3)).astype(np.int8)
        score += (long_m & (close_pos >= 0.3)).astype(np.int8)
        score += (short_m & (close_pos <= -0.3)).astype(np.int8)
        score += (long_m & sb2).astype(np.int8)
        score += (short_m & ss2).astype(np.int8)
        score = np.minimum(score, 6)

        out["conf_score"] = score
        out["is_confirmed"] = (score >= self.min_score) & (side != 0)
        out.loc[~out["is_confirmed"], "side"] = 0
        out.loc[out["side"] == 0, "raw_r"] = 0.0
        return out
```

---

### 5.5 `Engine/ml/smc_meta_labeler.py`
```python
import numpy as np
import pandas as pd
from typing import Dict, List, Optional

from Engine.ml.rf_meta_labeler import RegressionRMetaLabeler, BarrierConfig, CVConfig
from Engine.strategy.smc_event_detector import SMCEventDetector
from Engine.ml.footprint_confirmation import FootprintConfirmation

class SMCRegressionMetaLabeler(RegressionRMetaLabeler):
    NON_FEATURE = (
        "symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r",
        "side", "raw_r", "structural_level", "invalidation_price",
        "event_type", "conf_score", "is_confirmed", "prio"
    )

    PRIO = {
        "SWEEP_PDL": 0, "SWEEP_PDH": 0,
        "FVG_BULL": 1, "FVG_BEAR": 1,
        "OB_BULL": 2, "OB_BEAR": 2
    }

    def __init__(self, min_conf_score: int = 3):
        super().__init__(
            barrier=BarrierConfig(tp_r=2.25, sl_r=1.00, vertical_bars=48, min_terminal_r=0.20),
            cv=CVConfig(purge_hours=72, embargo_hours=24)
        )
        self.detector = SMCEventDetector()
        self.confirmer = FootprintConfirmation(min_score=min_conf_score)

    def build_smc_features(self, df: pd.DataFrame, sig: pd.DataFrame) -> pd.DataFrame:
        geo = self.detector.event_features(df, sig)
        macro = pd.DataFrame(index=df.index)
        macro["zc_div"] = df.get("zc_div", pd.Series(0.0, index=df.index)).clip(-5, 5).fillna(0.0)
        fr = df.get("funding_rate_pct", pd.Series(0.0, index=df.index))
        macro["funding_rate_pct"] = fr.clip(-0.5, 0.5).fillna(0.0)
        macro["vwap_zscore"] = df.get("vwap_zscore", pd.Series(0.0, index=df.index)).clip(-10, 10).fillna(0.0)
        macro["conf_score"] = sig.get("conf_score", pd.Series(0.0, index=df.index)).astype(np.float64).fillna(0.0)
        return geo.join(macro, how="outer").fillna(0.0)

    def pool_smc(self, per_symbol: Dict[str, pd.DataFrame],
                 ladder_feats: Dict[str, pd.DataFrame],
                 train_start: pd.Timestamp, train_end: pd.Timestamp) -> pd.DataFrame:
        frames = []
        for sym, df_sym in per_symbol.items():
            sl = df_sym.loc[train_start:train_end]
            if len(sl) < 200:
                continue
            sig = self.detector.generate_signals(sl.copy())
            if sym in ladder_feats:
                sig = self.confirmer.confirm(sl, sig, ladder_feats[sym].loc[sl.index])
            else:
                continue

            active_mask = sig["side"].to_numpy() != 0
            if active_mask.sum() < 5:
                continue

            dedup = sig[active_mask].copy()
            dedup["prio"] = dedup["event_type"].map(self.PRIO).fillna(9)
            dedup = dedup.sort_values(["prio", "conf_score"], ascending=[True, False])
            dedup = dedup[~dedup.index.duplicated(keep="first")]

            sig_clean = pd.DataFrame({
                "side": np.zeros(len(sl), dtype=np.int8),
                "raw_r": np.zeros(len(sl), dtype=np.float64)
            }, index=sl.index)
            sig_clean.loc[dedup.index, "side"] = dedup["side"].astype(np.int8)
            sig_clean.loc[dedup.index, "raw_r"] = dedup["raw_r"].astype(np.float64)

            event_mask = sig_clean["side"].to_numpy() != 0
            side_arr = sig_clean["side"].to_numpy()
            raw_r_arr = sig_clean["raw_r"].to_numpy()

            labels = self.triple_barrier_labels(sl, event_mask, side_arr, raw_r_arr)
            ev = labels.index.to_numpy()
            X = self.build_smc_features(sl, sig).iloc[ev]
            tab = X.reset_index(drop=True)
            tab["symbol"] = sym
            tab["abs_bar"] = sl.index.get_indexer(sl.index)[ev] + df_sym.index.get_indexer([sl.index[0]])[0]
            tab["y"] = (labels["exit_r"].to_numpy() > 0).astype(np.int8)
            tab["exit_r"] = labels["exit_r"].to_numpy()
            frames.append(tab)

        if not frames:
            raise RuntimeError("SMCRegressionMetaLabeler: zero confirmed events pooled.")
        return pd.concat(frames, ignore_index=True)
```

---

### 5.6 `Engine/strategy/smc_usman_noah.py`
```python
import numpy as np
import pandas as pd
from typing import Dict, Callable
from Engine.core.execution_kernel import ExecutionKernel, RiskConfig, FrictionConfig, RatchetConfig

DEFAULT_RATCHET = RatchetConfig(
    arm0_r=0.85,
    lock0_r=0.45,
    arm1_r=1.25,
    lock1_r=0.85,
    min_target_r=1.75,
    time_decay_bars=36,
    time_decay_r=0.20
)

class SMCUsmanNoahSimulator:
    def __init__(self, risk_cfg: RiskConfig = RiskConfig(), fric_cfg: FrictionConfig = FrictionConfig(), ratchet_cfg: RatchetConfig = DEFAULT_RATCHET):
        self.kernel = ExecutionKernel(risk_cfg, fric_cfg, ratchet_cfg)
        
    def generate_signals(self, df_test: pd.DataFrame, filter_func: Callable[[int, str], bool] = None) -> pd.DataFrame:
        T = len(df_test)
        op = df_test["open"].values
        hi = df_test["high"].values
        lo = df_test["low"].values
        cl = df_test["close"].values
        atr = df_test["atr_14"].clip(lower=cl * 0.002).values
        
        dt = pd.to_datetime(df_test.get("datetime_utc", df_test.get("datetime", pd.Series(df_test.index))))
        if hasattr(dt, 'dt') and hasattr(dt.dt, 'date'):
            days = dt.dt.date.values
        else:
            days = np.arange(T) // 96
            
        long_liq_zs = df_test.get("long_liq_zs", pd.Series(np.zeros(T))).values
        short_liq_zs = df_test.get("short_liq_zs", pd.Series(np.zeros(T))).values
        zc_div = df_test.get("zc_div", pd.Series(np.zeros(T))).values
        vwap_z = df_test.get("vwap_zscore", pd.Series(np.zeros(T))).values
        vol_ratio = df_test.get("volume_ratio", pd.Series(np.ones(T))).values
        ema_200 = df_test.get("ema_200", pd.Series(np.zeros(T))).values
        
        signals = np.zeros(T, dtype=int)
        raw_r = np.zeros(T, dtype=float)
        
        pdh, pdl = -1.0, float('inf')
        current_dh, current_dl = hi[0], lo[0]
        
        swept_pdl_bar = -1
        swept_pdh_bar = -1
        
        for t in range(25, T):
            trend_up = ema_200[t] >= ema_200[t-12]
            trend_down = ema_200[t] <= ema_200[t-12]
            
            if days[t] != days[t-1]:
                pdh = current_dh
                pdl = current_dl
                current_dh = hi[t]
                current_dl = lo[t]
                swept_pdl_bar = -1
                swept_pdh_bar = -1
            else:
                if hi[t] > current_dh: current_dh = hi[t]
                if lo[t] < current_dl: current_dl = lo[t]
                
            sig_long = False
            sig_short = False
            stop_dist = 0.0
            
            has_absorption_l = (long_liq_zs[t] > 0.8) or (zc_div[t] > 0.3) or (vwap_z[t] < -0.4) or (vol_ratio[t] > 1.2)
            has_absorption_s = (short_liq_zs[t] > 0.8) or (zc_div[t] < -0.3) or (vwap_z[t] > 0.4) or (vol_ratio[t] > 1.2)
            
            if pdh != -1.0 and pdl != float('inf'):
                if lo[t] < pdl:
                    swept_pdl_bar = t
                if hi[t] > pdh:
                    swept_pdh_bar = t
                    
                if swept_pdl_bar != -1 and (t - swept_pdl_bar) <= 8 and (t - swept_pdl_bar) >= 0:
                    if cl[t] > pdl and cl[t] > op[t] and trend_up and has_absorption_l:
                        sig_long = True
                        lowest_sweep = np.min(lo[swept_pdl_bar:t+1])
                        s_dist = (cl[t] - lowest_sweep) + 0.2 * atr[t]
                        s_dist = max(s_dist, atr[t] * 1.5)
                        s_dist = min(s_dist, atr[t] * 2.5)
                        stop_dist = s_dist
                        swept_pdl_bar = -1
                        
                if swept_pdh_bar != -1 and (t - swept_pdh_bar) <= 8 and (t - swept_pdh_bar) >= 0:
                    if cl[t] < pdh and cl[t] < op[t] and trend_down and has_absorption_s:
                        sig_short = True
                        highest_sweep = np.max(hi[swept_pdh_bar:t+1])
                        s_dist = (highest_sweep - cl[t]) + 0.2 * atr[t]
                        s_dist = max(s_dist, atr[t] * 1.5)
                        s_dist = min(s_dist, atr[t] * 2.5)
                        stop_dist = s_dist
                        swept_pdh_bar = -1
                        
            if filter_func is not None:
                if sig_long and not filter_func(t, 'LONG'): sig_long = False
                if sig_short and not filter_func(t, 'SHORT'): sig_short = False
                
            if sig_long and not sig_short:
                signals[t] = 1
                raw_r[t] = stop_dist
            elif sig_short and not sig_long:
                signals[t] = -1
                raw_r[t] = stop_dist
                
        return pd.DataFrame({'side': signals, 'raw_r': raw_r}, index=df_test.index)
        
    def run(self, df_test: pd.DataFrame, training_mode: bool = False, filter_func: Callable[[int, str], bool] = None) -> dict:
        signals_df = self.generate_signals(df_test, filter_func)
        return self.kernel.run(df_test, signals_df, training_mode)
```
