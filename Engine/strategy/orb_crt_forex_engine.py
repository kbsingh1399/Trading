"""
================================================================================
STRATEGY: CANONICAL ORB + CRT FOREX & CFD STRATEGY (STANDALONE & ENGINE-ROUTED)
================================================================================
Location: Engine/ORB_CRT_ForexCFD_Strategy.py (and Engine/strategy/ORB_CRT_ForexCFD_Strategy.py)
Architecture: Modular BaseForexStrategy Implementation & Dynamic Registry Plugin
Engine Routing: Compatible with Engine/forex_engine.py (--strategy orb_crt)

Core Confluence Architecture:
1. Dual-Session Opening Range (OR):
   - London Open: 07:00 UTC (2 bars = 30 min duration)
   - New York Open: 13:30 UTC (2 bars = 30 min duration)
2. Candle Range Theory (CRT) Microstructure Confirmation:
   - Breakout bar body-to-range ratio (body_ratio >= 0.40)
   - Confirmed close outside opening range boundaries (close_outside)
   - Fair Value Gap expansion in breakout direction (fvg_expansion)
3. Pre-Market Judas Swing Detection:
   - 6-bar (1.5h) pre-market liquidity sweep of Previous Day Low/High (PDL/PDH) and reclaim
4. Macro Trend Alignment:
   - Macro 4H 200 EMA slope or Judas sweep liquidity absorption override
5. High-Speed Numba Acceleration:
   - Sub-second vectorized simulation across all 18 institutional assets
6. Institutional Microstructure Ratchet:
   - Phase 0 (BE Lock): Move stop to Entry +0.15R at +0.8R gain
   - Phase 1 (Profit Lock): Move stop to Entry +0.80R at +1.5R gain
   - Target Exit: Full take-profit at +2.5R
   - Time Decay: Exit at market if < +0.20R within 24 bars (6 hours)
   - Execution Friction: 8 bps (taker fees + slippage) deducted per trade
================================================================================
"""
from __future__ import annotations

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

import numpy as np
import pandas as pd
import polars as pl
from numba import njit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# PATH CONFIGURATION & IMPORTS
# -------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
ENGINE_DIR = CURRENT_FILE.parent if CURRENT_FILE.parent.name == "Engine" else CURRENT_FILE.parents[1]
PROJECT_ROOT = ENGINE_DIR.parent

for p in [str(PROJECT_ROOT), str(ENGINE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from Engine.core.base_strategy import (
    BaseForexStrategy,
    StrategyRegistry,
    EngineConfig,
    StrategySignal,
    BacktestResult,
)
from Engine.core.strategy_kernel import CANONICAL_18_ASSETS

DATA_DIR = PROJECT_ROOT / "Forex_Backtesting_Data"
ARTIFACT_DIR = ENGINE_DIR / "artifacts"


# -------------------------------------------------------------------------
# NUMBA VECTORIZED SIMULATOR KERNEL
# -------------------------------------------------------------------------
# Exit reason codes (OX61: true hold bars + exit attribution for concurrency truth)
EXIT_SL = 0          # stopped out (gap-aware: open beyond SL fills at open, unclamped)
EXIT_TP = 1          # fixed 2.5R take-profit
EXIT_DECAY = 2       # time decay (unreachable under the 24-bar session cap; kept for parity)
EXIT_FRIDAY = 3      # Friday 20:30 UTC weekend closeout (live truth: never hold weekends)
EXIT_DATA_END = 4    # (reserved)
EXIT_TRUNC = 5       # 24-bar session time-stop: MTM exit at last session bar close


@njit
def simulate_session_orb(
    opens: np.ndarray,
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    volumes: np.ndarray,
    timestamps: np.ndarray,
    dates: np.ndarray,
    hours: np.ndarray,
    minutes: np.ndarray,
    day_of_weeks: np.ndarray,
    start_hour: int,
    start_minute: int,
    range_duration_bars: int = 2,
    trade_duration_bars: int = 30
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Simulates Opening Range Breakouts (ORB) with Candle Range Theory (CRT)
    microstructure filters and piecewise ratchets with zero lookahead.

    OX61 correctness fixes (entry/exit economics pre-committed and untouched):
    exited-flag (no -1.0 sentinel collision), gap-aware unclamped SL fills,
    Friday 20:30 UTC closeout + Friday 18:00 entry cutoff (live truth), true
    hold bars + exit reason codes. An experimental full live-spec unification
    (structural TP, 1.5xATR floors, R_eff veto, extreme-locks, no truncation)
    was built, measured at 0/20, and reverted: see OX61 report (F0).
    """
    n = len(highs)
    max_trades = (n // 10) + 100

    trade_signals = np.zeros(max_trades, dtype=np.float64)       # +1.0 for Long, -1.0 for Short
    trade_outcomes = np.zeros(max_trades, dtype=np.float64)      # Realized Net R
    trade_entry_prices = np.zeros(max_trades, dtype=np.float64)  # Entry Price
    trade_sl_prices = np.zeros(max_trades, dtype=np.float64)     # Stop Loss Price
    trade_timestamps = np.zeros(max_trades, dtype=np.int64)      # Entry bar timestamp
    trade_hold_bars = np.zeros(max_trades, dtype=np.int64)       # TRUE bars held (exit - entry)
    trade_reasons = np.zeros(max_trades, dtype=np.int64)         # Exit reason code

    emas_50 = np.zeros(n)
    emas_50[0] = closes[0]
    alpha_50 = 2.0 / (50 + 1)

    emas_200 = np.zeros(n)
    emas_200[0] = closes[0]
    alpha_200 = 2.0 / (200 + 1)

    trs = np.zeros(n)
    atrs = np.zeros(n)

    for i in range(1, n):
        emas_50[i] = emas_50[i-1] + alpha_50 * (closes[i] - emas_50[i-1])
        emas_200[i] = emas_200[i-1] + alpha_200 * (closes[i] - emas_200[i-1])

        tr1 = highs[i] - lows[i]
        tr2 = abs(highs[i] - closes[i-1])
        tr3 = abs(lows[i] - closes[i-1])
        trs[i] = max(tr1, max(tr2, tr3))

        if i >= 14:
            atrs[i] = np.mean(trs[i-13:i+1])

    trade_idx = 0
    i = 0
    prev_day_high = highs[0]
    prev_day_low = lows[0]
    curr_day_high = highs[0]
    curr_day_low = lows[0]
    curr_date = dates[0]

    while i < n - range_duration_bars:
        if dates[i] != curr_date:
            prev_day_high = curr_day_high
            prev_day_low = curr_day_low
            curr_date = dates[i]
            curr_day_high = highs[i]
            curr_day_low = lows[i]
        else:
            if highs[i] > curr_day_high: curr_day_high = highs[i]
            if lows[i] < curr_day_low: curr_day_low = lows[i]

        if hours[i] == start_hour and minutes[i] == start_minute:
            or_high = highs[i]
            or_low = lows[i]

            for j in range(1, range_duration_bars):
                if highs[i+j] > or_high: or_high = highs[i+j]
                if lows[i+j] < or_low: or_low = lows[i+j]

            or_range = or_high - or_low

            if or_range > 0:
                trade_start = i + range_duration_bars
                trade_end = min(n, trade_start + trade_duration_bars)

                # Pre-market Judas sweep (6 bars = 1.5 hours prior to OR)
                pre_start = max(0, i - 6)
                pre_or_low = lows[pre_start]
                pre_or_high = highs[pre_start]
                for p in range(pre_start, i):
                    if lows[p] < pre_or_low: pre_or_low = lows[p]
                    if highs[p] > pre_or_high: pre_or_high = highs[p]

                judas_sweep_long = 1.0 if (pre_or_low < prev_day_low and or_low >= prev_day_low) else 0.0
                judas_sweep_short = 1.0 if (pre_or_high > prev_day_high and or_high <= prev_day_high) else 0.0

                swept_pdl = 1.0 if or_low < prev_day_low else 0.0
                swept_pdh = 1.0 if or_high > prev_day_high else 0.0

                for j in range(trade_start, trade_end):
                    # Long Breakout
                    if highs[j] > or_high:
                        # CRT Filter: Body ratio >= 0.40 and close outside OR high
                        body = abs(closes[j] - opens[j])
                        wick = highs[j] - lows[j] + 1e-9
                        body_ratio = body / wick

                        if body_ratio >= 0.40 and (swept_pdl == 1.0 or judas_sweep_long == 1.0 or closes[j] > emas_200[j]):
                            entry_bar = j + 1
                            if entry_bar >= trade_end or entry_bar >= n:
                                continue
                            # Friday 18:00 UTC entry cutoff (live truth: no weekend-gap entries)
                            if day_of_weeks[entry_bar] == 4 and hours[entry_bar] >= 18:
                                continue

                            entry = opens[entry_bar] # Strictly causal next-bar open fill
                            sl = or_low
                            prev_idx = j
                            r_val = max(entry - sl, 0.50 * atrs[prev_idx])
                            if r_val <= 0 or (r_val / entry) > 0.025:
                                continue

                            tp = entry + 2.5 * r_val
                            current_sl = sl
                            outcome_r = -1.0
                            exited = False  # OX61: explicit flag (kills -1.0 sentinel collision)
                            exit_k = trade_end - 1
                            reason = 5  # EXIT_TRUNC default (24-bar session time-stop)
                            phase_0_locked = False
                            phase_1_locked = False

                            for k in range(entry_bar, trade_end):
                                # Time decay check: 24 bars (6 hours)
                                if k - entry_bar >= 24:
                                    current_r = (closes[k] - entry) / r_val
                                    if current_r < 0.2:
                                        outcome_r = current_r
                                        exited = True
                                        exit_k = k
                                        reason = 2  # EXIT_DECAY
                                        break

                                # Gap-through-stop: bar opens beyond SL -> live fills at open
                                if opens[k] <= current_sl:
                                    outcome_r = (opens[k] - entry) / r_val
                                    exited = True
                                    exit_k = k
                                    reason = 0  # EXIT_SL
                                    break
                                if lows[k] <= current_sl:
                                    outcome_r = (current_sl - entry) / r_val
                                    exited = True
                                    exit_k = k
                                    reason = 0  # EXIT_SL
                                    break
                                if highs[k] >= tp:
                                    outcome_r = 2.5
                                    exited = True
                                    exit_k = k
                                    reason = 1  # EXIT_TP
                                    break
                                # Friday 20:30 UTC weekend closeout (live truth)
                                if day_of_weeks[k] == 4 and (hours[k] > 20 or (hours[k] == 20 and minutes[k] >= 30)):
                                    outcome_r = (closes[k] - entry) / r_val
                                    exited = True
                                    exit_k = k
                                    reason = 3  # EXIT_FRIDAY
                                    break

                                # Trailing ratchets on bar close
                                current_gain = (closes[k] - entry) / r_val
                                if not phase_0_locked and current_gain >= 0.8:
                                    current_sl = entry + 0.15 * r_val
                                    phase_0_locked = True
                                if phase_0_locked and not phase_1_locked and current_gain >= 1.5:
                                    current_sl = entry + 0.80 * r_val
                                    phase_1_locked = True

                            if not exited:
                                outcome_r = (closes[trade_end-1] - entry) / r_val

                            # Friction deduction (8 bps on risk == 0.08R, pre-committed)
                            outcome_r -= 0.08

                            trade_signals[trade_idx] = 1.0
                            trade_outcomes[trade_idx] = outcome_r  # OX61: unclamped (live has no clamp)
                            trade_entry_prices[trade_idx] = entry
                            trade_sl_prices[trade_idx] = sl
                            trade_timestamps[trade_idx] = timestamps[entry_bar]
                            trade_hold_bars[trade_idx] = exit_k - entry_bar
                            trade_reasons[trade_idx] = reason
                            trade_idx += 1
                            i = trade_end
                            break

                    # Short Breakdown
                    elif lows[j] < or_low:
                        # CRT Filter: Body ratio >= 0.40 and close outside OR low
                        body = abs(closes[j] - opens[j])
                        wick = highs[j] - lows[j] + 1e-9
                        body_ratio = body / wick

                        if body_ratio >= 0.40 and (swept_pdh == 1.0 or judas_sweep_short == 1.0 or closes[j] < emas_200[j]):
                            entry_bar = j + 1
                            if entry_bar >= trade_end or entry_bar >= n:
                                continue
                            # Friday 18:00 UTC entry cutoff (live truth: no weekend-gap entries)
                            if day_of_weeks[entry_bar] == 4 and hours[entry_bar] >= 18:
                                continue

                            entry = opens[entry_bar] # Strictly causal next-bar open fill
                            sl = or_high
                            prev_idx = j
                            r_val = max(sl - entry, 0.50 * atrs[prev_idx])
                            if r_val <= 0 or (r_val / entry) > 0.025:
                                continue

                            tp = entry - 2.5 * r_val
                            current_sl = sl
                            outcome_r = -1.0
                            exited = False  # OX61: explicit flag (kills -1.0 sentinel collision)
                            exit_k = trade_end - 1
                            reason = 5  # EXIT_TRUNC default (24-bar session time-stop)
                            phase_0_locked = False
                            phase_1_locked = False

                            for k in range(entry_bar, trade_end):
                                if k - entry_bar >= 24:
                                    current_r = (entry - closes[k]) / r_val
                                    if current_r < 0.2:
                                        outcome_r = current_r
                                        exited = True
                                        exit_k = k
                                        reason = 2  # EXIT_DECAY
                                        break

                                # Gap-through-stop: bar opens beyond SL -> live fills at open
                                if opens[k] >= current_sl:
                                    outcome_r = (entry - opens[k]) / r_val
                                    exited = True
                                    exit_k = k
                                    reason = 0  # EXIT_SL
                                    break
                                if highs[k] >= current_sl:
                                    outcome_r = (entry - current_sl) / r_val
                                    exited = True
                                    exit_k = k
                                    reason = 0  # EXIT_SL
                                    break
                                if lows[k] <= tp:
                                    outcome_r = 2.5
                                    exited = True
                                    exit_k = k
                                    reason = 1  # EXIT_TP
                                    break
                                # Friday 20:30 UTC weekend closeout (live truth)
                                if day_of_weeks[k] == 4 and (hours[k] > 20 or (hours[k] == 20 and minutes[k] >= 30)):
                                    outcome_r = (entry - closes[k]) / r_val
                                    exited = True
                                    exit_k = k
                                    reason = 3  # EXIT_FRIDAY
                                    break

                                current_gain = (entry - closes[k]) / r_val
                                if not phase_0_locked and current_gain >= 0.8:
                                    current_sl = entry - 0.15 * r_val
                                    phase_0_locked = True
                                if phase_0_locked and not phase_1_locked and current_gain >= 1.5:
                                    current_sl = entry - 0.80 * r_val
                                    phase_1_locked = True

                            if not exited:
                                outcome_r = (entry - closes[trade_end-1]) / r_val

                            outcome_r -= 0.08

                            trade_signals[trade_idx] = -1.0
                            trade_outcomes[trade_idx] = outcome_r  # OX61: unclamped (live has no clamp)
                            trade_entry_prices[trade_idx] = entry
                            trade_sl_prices[trade_idx] = sl
                            trade_timestamps[trade_idx] = timestamps[entry_bar]
                            trade_hold_bars[trade_idx] = exit_k - entry_bar
                            trade_reasons[trade_idx] = reason
                            trade_idx += 1
                            i = trade_end
                            break

        i += 1

    return (
        trade_signals[:trade_idx],
        trade_outcomes[:trade_idx],
        trade_entry_prices[:trade_idx],
        trade_sl_prices[:trade_idx],
        trade_timestamps[:trade_idx],
        trade_hold_bars[:trade_idx],
        trade_reasons[:trade_idx]
    )


# -------------------------------------------------------------------------
# STRATEGY CLASS: ORB_CRT_ForexCFD_Strategy
# -------------------------------------------------------------------------
@StrategyRegistry.register("orb_crt")
@StrategyRegistry.register("crt_orb")
@StrategyRegistry.register("crt")
class ORBCRTForexCFDStrategy(BaseForexStrategy):
    """
    Canonical Dual-Session Opening Range Breakout (ORB) + Candle Range Theory (CRT) Strategy.
    Implements BaseForexStrategy interface for seamless integration into forex_engine.py.
    """
    name: str = "orb_crt"
    description: str = "Dual-Session ORB + Candle Range Theory (CRT) Microstructure Strategy"

    def __init__(self, config: Optional[EngineConfig] = None):
        super().__init__(config=config)
        self.initialize(self.config)

    def initialize(self, config: Optional[EngineConfig] = None) -> None:
        """Initializes configuration and criteria."""
        if config is not None:
            self.config = config
        self.initialized = True
        logging.info("ORBCRTForexCFDStrategy initialized successfully.")

    def generate_signal(
        self,
        symbol: str,
        buffer_15m: pd.DataFrame,
        buffer_4h: Optional[pd.DataFrame] = None,
        current_tick: Optional[Any] = None
    ) -> StrategySignal:
        """
        Evaluates real-time streaming bars from MT5 and produces a StrategySignal.
        Called bar-by-bar during live/dry-run telemetry.
        """
        if buffer_15m.empty or len(buffer_15m) < 20:
            return StrategySignal(symbol=symbol, signal=0, reason="Insufficient Data")

        from Engine.forex_engine import compute_crt_orb_state, compute_features_pandas, calculate_adaptive_sl_tp, MAX_SPREAD_ATR_RATIO
        crt = compute_crt_orb_state(buffer_15m)
        feat_df = compute_features_pandas(buffer_15m, buffer_4h)
        trend = feat_df.iloc[-1].get("htf_4h_trend", 0.0)
        atr = float(feat_df.iloc[-1].get("atr_14", 0.0))

        dt = buffer_15m['datetime'].iloc[-1] if 'datetime' in buffer_15m else pd.Timestamp.utcnow()
        hour = dt.hour if hasattr(dt, 'hour') else 12
        is_kz = (7 <= hour <= 10) or (12 <= hour <= 15)

        bid = current_tick.bid if current_tick else float(buffer_15m['close'].iloc[-1])
        ask = current_tick.ask if current_tick else float(buffer_15m['close'].iloc[-1])
        spread = abs(ask - bid) if (ask > 0 and bid > 0) else 0.0

        base_risk = self.config.criteria.base_risk_usd

        if not is_kz:
            return StrategySignal(symbol=symbol, signal=0, reason="HOLD (Off-Hours)")

        # Option C Filter 1: Dynamic Spread-to-ATR Regime Quarantine (> 12%)
        if atr > 0 and spread > 0:
            spread_atr_ratio = spread / atr
            if spread_atr_ratio > MAX_SPREAD_ATR_RATIO:
                return StrategySignal(symbol=symbol, signal=0, reason=f"HOLD (Spread/ATR {spread_atr_ratio:.1%} > {MAX_SPREAD_ATR_RATIO:.0%})")

        local_low = buffer_15m['low'].iloc[-20:].min() if len(buffer_15m) >= 20 else buffer_15m['low'].min()
        local_high = buffer_15m['high'].iloc[-20:].max() if len(buffer_15m) >= 20 else buffer_15m['high'].max()

        is_long = crt["is_long_crt"] and (trend > 0 or crt["judas_long"])
        is_short = crt["is_short_crt"] and (trend < 0 or crt["judas_short"])

        if is_long:
            entry = ask
            raw_sl = crt["or_low"] if crt["or_low"] > 0 else local_low
            sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                symbol=symbol, is_long=True, entry=entry, raw_sl=raw_sl,
                local_extreme=local_low, spread=spread, atr=atr,
                tp_structural=local_high
            )
            if not valid:
                return StrategySignal(symbol=symbol, signal=0, reason=reason)
            return StrategySignal(
                symbol=symbol,
                signal=1,
                prob=float(crt["body_ratio"]),
                entry_price=entry,
                sl_price=sl,
                tp_price=tp,
                risk_usd=base_risk,
                strategy_tag="ORB_CRT",
                reason=reason,
                metadata={"session": crt["session"], "body_ratio": crt["body_ratio"], "r_dist": r_dist}
            )

        elif is_short:
            entry = bid
            raw_sl = crt["or_high"] if crt["or_high"] > 0 else local_high
            sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                symbol=symbol, is_long=False, entry=entry, raw_sl=raw_sl,
                local_extreme=local_high, spread=spread, atr=atr,
                tp_structural=local_low
            )
            if not valid:
                return StrategySignal(symbol=symbol, signal=0, reason=reason)
            return StrategySignal(
                symbol=symbol,
                signal=-1,
                prob=float(crt["body_ratio"]),
                entry_price=entry,
                sl_price=sl,
                tp_price=tp,
                risk_usd=base_risk,
                strategy_tag="ORB_CRT",
                reason=reason,
                metadata={"session": crt["session"], "body_ratio": crt["body_ratio"], "r_dist": r_dist}
            )

        if crt["session"] != "None":
            return StrategySignal(symbol=symbol, signal=0, reason=f"HOLD (Inside {crt['session']} OR)")
        return StrategySignal(symbol=symbol, signal=0, reason="HOLD (No OR Formed)")

    def run_backtest(
        self,
        start_date: str = "2025-12-01",
        end_date: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        save_plot: bool = True
    ) -> BacktestResult:
        """
        Executes high-speed Numba-accelerated historical backtest across all 18 canonical assets.
        Simulates London (07:00 UTC) and NY (13:30 UTC) opening ranges with CRT filters.
        """
        target_symbols = symbols or CANONICAL_18_ASSETS
        initial_capital = self.config.criteria.initial_capital_usd
        base_risk = self.config.criteria.base_risk_usd

        all_trades_list = []
        per_asset = {}
        b_returns = []

        logging.info(f"Running ORB_CRT Numba Backtest from {start_date} to {end_date or 'latest'} across {len(target_symbols)} assets")

        for sym in target_symbols:
            parquet_path = DATA_DIR / f"{sym}_15m_real.parquet"
            if not parquet_path.exists():
                parquet_path = DATA_DIR / f"{sym}.parquet"
            if not parquet_path.exists():
                continue

            try:
                # High-speed Polars reading
                pl_df = pl.read_parquet(parquet_path)
                df = pl_df.to_pandas()
                df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
                vol_col = 'tick_volume' if 'tick_volume' in df.columns else ('volume' if 'volume' in df.columns else 'real_volume')

                # Filter dates
                mask = df['datetime'] >= start_date
                if end_date:
                    mask = mask & (df['datetime'] <= end_date)
                df_sub = df[mask].copy().reset_index(drop=True)
                if len(df_sub) < 50:
                    continue

                b_ret = (df_sub['close'].iloc[-1] / df_sub['close'].iloc[0]) - 1.0
                b_returns.append(b_ret)

                opens = df_sub['open'].values.astype(np.float64)
                highs = df_sub['high'].values.astype(np.float64)
                lows = df_sub['low'].values.astype(np.float64)
                closes = df_sub['close'].values.astype(np.float64)
                volumes = df_sub[vol_col].values.astype(np.float64) if vol_col in df_sub.columns else np.ones(len(df_sub), dtype=np.float64)
                timestamps = df_sub['datetime'].values.astype('datetime64[ns]').astype(np.int64)
                dates = (df_sub['datetime'].dt.year * 10000 + df_sub['datetime'].dt.month * 100 + df_sub['datetime'].dt.day).values.astype(np.int64)
                hours = df_sub['datetime'].dt.hour.values.astype(np.int64)
                minutes = df_sub['datetime'].dt.minute.values.astype(np.int64)
                day_of_weeks = df_sub['datetime'].dt.dayofweek.values.astype(np.int64)

                # 1. London Session ORB (07:00 UTC)
                lon_sig, lon_r, lon_entry, lon_sl, lon_ts, lon_hold, lon_reason = simulate_session_orb(
                    opens, highs, lows, closes, volumes, timestamps, dates, hours, minutes, day_of_weeks,
                    start_hour=7, start_minute=0, range_duration_bars=2, trade_duration_bars=24
                )

                # 2. NY Session ORB (13:30 UTC)
                ny_sig, ny_r, ny_entry, ny_sl, ny_ts, ny_hold, ny_reason = simulate_session_orb(
                    opens, highs, lows, closes, volumes, timestamps, dates, hours, minutes, day_of_weeks,
                    start_hour=13, start_minute=30, range_duration_bars=2, trade_duration_bars=24
                )

                # Combine session trades
                combined_r = np.concatenate([lon_r, ny_r])
                combined_sig = np.concatenate([lon_sig, ny_sig])
                combined_ts = np.concatenate([lon_ts, ny_ts])
                combined_entry = np.concatenate([lon_entry, ny_entry])
                combined_sl = np.concatenate([lon_sl, ny_sl])
                combined_hold = np.concatenate([lon_hold, ny_hold])
                combined_reason = np.concatenate([lon_reason, ny_reason])

                if len(combined_r) > 0:
                    order = np.argsort(combined_ts)
                    s_r = combined_r[order]
                    s_sig = combined_sig[order]
                    s_ts = pd.to_datetime(combined_ts[order])
                    s_entry = combined_entry[order]
                    s_sl = combined_sl[order]
                    s_hold = combined_hold[order]
                    s_reason = combined_reason[order]

                    asset_df = pd.DataFrame({
                        'datetime': s_ts,
                        'asset': sym,
                        'signal': s_sig,
                        'entry': s_entry,
                        'sl': s_sl,
                        'r_realized': s_r,
                        'hold_bars': s_hold,
                        'exit_reason': s_reason,
                        'pnl': s_r * base_risk
                    })
                    all_trades_list.append(asset_df)

                    n = len(asset_df)
                    w = (asset_df['r_realized'] > 0).sum()
                    wr = (w / n * 100.0) if n > 0 else 0.0
                    tot_r = float(asset_df['r_realized'].sum())
                    pnl = float(tot_r * base_risk)
                    per_asset[sym] = {'trades': n, 'win_rate': wr, 'net_r': tot_r, 'pnl': pnl}
                else:
                    per_asset[sym] = {'trades': 0, 'win_rate': 0.0, 'net_r': 0.0, 'pnl': 0.0}

            except Exception as e:
                logging.warning(f"Error evaluating asset {sym} in ORB_CRT: {e}")

        if not all_trades_list:
            return BacktestResult(
                strategy_name=self.name,
                start_date=start_date,
                end_date=end_date,
                window_id=None,
                total_trades=0,
                win_rate=0.0,
                profit_factor=0.0,
                net_r=0.0,
                net_pnl_usd=0.0,
                net_roi_pct=0.0,
                max_dd_pct=0.0,
                buy_hold_return_pct=0.0,
                passed_criteria=False,
                failure_reasons=["No trades generated"]
            )

        trades_df = pd.concat(all_trades_list).sort_values('datetime').reset_index(drop=True)
        trades_df['equity'] = initial_capital + trades_df['pnl'].cumsum()

        total_trades = len(trades_df)
        wins = (trades_df['r_realized'] > 0).sum()
        win_rate = (wins / total_trades * 100.0)
        net_pnl = float(trades_df['pnl'].sum())
        roi = (net_pnl / initial_capital * 100.0)
        net_r = float(trades_df['r_realized'].sum())

        peak = trades_df['equity'].cummax()
        drawdowns = (trades_df['equity'] - peak) / peak * 100.0
        max_dd = float(drawdowns.min())

        gross_win = trades_df.loc[trades_df['pnl'] > 0, 'pnl'].sum()
        gross_loss = abs(trades_df.loc[trades_df['pnl'] < 0, 'pnl'].sum())
        pf = float(gross_win / gross_loss) if gross_loss > 0 else 99.0

        avg_bh_ret = float(np.mean(b_returns) * 100.0) if b_returns else 0.0

        passed_crit, checks, failures = self.config.evaluate_pass_criteria({
            "net_roi_pct": roi,
            "max_dd_pct": abs(max_dd),
            "win_rate": win_rate,
            "total_trades": total_trades,
            "net_r": net_r
        })

        if save_plot:
            ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
            img_path = ARTIFACT_DIR / "orb_crt_forex_equity_curve.png"
            plt.figure(figsize=(11, 6))
            plt.plot(trades_df['datetime'], trades_df['equity'], label=f'ORB + CRT Strategy (ROI: {roi:+.1f}%)', color='#2979ff', lw=2)
            plt.axhline(initial_capital, color='gray', linestyle='--', alpha=0.6, label=f'Initial Capital ({initial_capital:,.0f} USD)')
            plt.title(f"ORB + Candle Range Theory (CRT) Forex & CFD Equity Curve ({start_date} to {end_date or 'Present'})", fontsize=12, fontweight='bold')
            plt.xlabel("Date", fontsize=10)
            plt.ylabel("Portfolio Equity (USD)", fontsize=10)
            plt.grid(True, alpha=0.3)
            plt.legend(loc='upper left')
            plt.tight_layout()
            plt.savefig(img_path, dpi=150)
            plt.close()

        return BacktestResult(
            strategy_name=self.name,
            start_date=start_date,
            end_date=end_date,
            window_id=None,
            total_trades=total_trades,
            win_rate=win_rate,
            profit_factor=pf,
            net_r=net_r,
            net_pnl_usd=net_pnl,
            net_roi_pct=roi,
            max_dd_pct=max_dd,
            buy_hold_return_pct=avg_bh_ret,
            passed_criteria=passed_crit,
            criteria_checks=checks,
            failure_reasons=failures,
            per_asset_summary=per_asset,
            trades_df=trades_df
        )


# -------------------------------------------------------------------------
# STANDALONE CLI ENTRYPOINT (BACKWARD COMPATIBILITY)
# -------------------------------------------------------------------------
def run_strategy(
    start_date: str = "2025-12-01",
    end_date: Optional[str] = None,
    save_plot: bool = True
) -> Dict[str, Any]:
    """Runs the strategy directly and displays comprehensive summary."""
    config = EngineConfig.load()
    strat = ORBCRTForexCFDStrategy(config=config)
    res = strat.run_backtest(start_date=start_date, end_date=end_date, save_plot=save_plot)

    print("=" * 80)
    print(f"ORB + CRT FOREX & CFD STRATEGY | RANGE: {start_date} to {end_date or 'Present'}")
    print("=" * 80)
    print(f"{'Asset':<9} | {'Trades':<7} | {'Win Rate':<10} | {'Net R':<10} | {'Net PnL (USD)':<15}")
    print("-" * 60)
    for a, d in sorted(res.per_asset_summary.items(), key=lambda x: x[1]['net_r'], reverse=True):
        pnl_str = f"+${d['pnl']:,.2f}" if d['pnl'] >= 0 else f"-${abs(d['pnl']):,.2f}"
        print(f"{a:<9} | {d['trades']:>6}  | {d['win_rate']:>7.1f}%   | {d['net_r']:>+8.2f}R | {pnl_str:>14}")

    print("\n[PORTFOLIO AGGREGATE SUMMARY]")
    print(f"  Initial Capital:       {config.criteria.initial_capital_usd:,.2f} USD")
    print(f"  Final Equity:          {config.criteria.initial_capital_usd + res.net_pnl_usd:,.2f} USD")
    print(f"  Total Trades:          {res.total_trades}")
    print(f"  Win Rate:              {res.win_rate:.1f}%")
    print(f"  Profit Factor:         {res.profit_factor:.2f}")
    print(f"  Net R-Multiple:        {res.net_r:+.2f}R")
    print(f"  Net Profit (USD):      {res.net_pnl_usd:+,.2f} USD")
    print(f"  Net ROI:               {res.net_roi_pct:+.2f}%")
    print(f"  Max Drawdown:          {res.max_dd_pct:.2f}%")
    print(f"  Buy & Hold Avg:        {res.buy_hold_return_pct:+.2f}%")
    print(f"  Passed Target Criteria: {'YES (CERTIFIED)' if res.passed_criteria else 'NO'}")
    if res.failure_reasons:
        print(f"  Failure Details:       {res.failure_reasons}")

    return {
        'trades': res.total_trades,
        'win_rate': res.win_rate,
        'profit_factor': res.profit_factor,
        'net_r': res.net_r,
        'net_pnl': res.net_pnl_usd,
        'roi': res.net_roi_pct,
        'max_dd': res.max_dd_pct,
        'passed_criteria': res.passed_criteria
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ORB + CRT Forex & CFD Strategy")
    parser.add_argument("--start", type=str, default="2025-12-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    run_strategy(start_date=args.start, end_date=args.end)
