"""
S2 Bollinger Bands Mean Reversion Strategy Module
=================================================
Microstructure mean-reversion sleeve designed for range-bound and mean-reverting regimes.
Authentic causal execution:
- Signal evaluated at bar close i.
- Order filled at next-bar open opens[i+1].
- Evaluates barriers over horizon_bars with adverse stop checked before profit target.
- Friction deducted from realized R-multiple.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "binance_backtesting_data"
if not DATA_DIR.exists():
    DATA_DIR = REPO_ROOT / "Engine" / "binance_backtesting_data"

CORE_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT",
    "ADAUSDT", "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT"
]


def generate_s2_bollinger_trades(
    symbols: Optional[List[str]] = None,
    data_dir: Optional[Path] = None,
    bb_window: int = 96,
    bb_std: float = 2.0,
    rsi_oversold: float = 32.0,
    rsi_overbought: float = 68.0,
    target_r: float = 2.2,
    stop_r: float = 1.0,
    horizon_bars: int = 24,
    friction_r: float = 0.25,
    risk_usd: float = 22.0
) -> pd.DataFrame:
    """Generate causal S2 Bollinger Bands Mean Reversion trade events across assets.
    
    Returns a DataFrame with columns:
        ['time', 'exit_time', 'r_gain', 'hold_bars', 'hold_ms', 'symbol',
         'strategy', 'prob', 'sleeve_id', 'risk', 'side', 'entry_price']
    """
    if symbols is None:
        symbols = CORE_SYMBOLS
    if data_dir is None:
        data_dir = DATA_DIR

    s2_trades: List[Dict] = []

    for sym in symbols:
        p = data_dir / f"{sym}_15m_master_2020_2026.parquet"
        if not p.exists():
            continue

        df = pd.read_parquet(
            p,
            columns=["open_time_ms", "open", "high", "low", "close", "rsi_14", "atr_14"]
        ).dropna().reset_index(drop=True)

        n = len(df)
        if n < bb_window + horizon_bars + 2:
            continue

        opens = df["open"].to_numpy(dtype=np.float64)
        highs = df["high"].to_numpy(dtype=np.float64)
        lows = df["low"].to_numpy(dtype=np.float64)
        closes = df["close"].to_numpy(dtype=np.float64)
        rsis = df["rsi_14"].to_numpy(dtype=np.float64)
        atrs = df["atr_14"].to_numpy(dtype=np.float64)
        times = df["open_time_ms"].to_numpy(dtype=np.int64)

        roll_mean = pd.Series(closes).rolling(bb_window).mean().to_numpy()
        roll_std = pd.Series(closes).rolling(bb_window).std().to_numpy()
        bb_upper = roll_mean + bb_std * roll_std
        bb_lower = roll_mean - bb_std * roll_std

        for i in range(bb_window, n - horizon_bars - 1):
            dist = atrs[i]
            if dist <= 0 or not np.isfinite(dist):
                continue

            # Long mean reversion signal: price breaks lower band & RSI oversold
            if closes[i] < bb_lower[i] and rsis[i] < rsi_oversold:
                # Causal entry at next bar open
                entry_bar = i + 1
                entry_p = opens[entry_bar]
                entry_time = times[entry_bar]
                target_p = entry_p + target_r * dist
                stop_p = entry_p - stop_r * dist
                exit_r = 0.0
                bars_held = horizon_bars
                hit = False

                for j in range(entry_bar, entry_bar + horizon_bars):
                    # Check adverse stop first
                    if lows[j] <= stop_p:
                        exit_r = -stop_r
                        hit = True
                        bars_held = j - entry_bar + 1
                        break
                    if highs[j] >= target_p:
                        exit_r = target_r
                        hit = True
                        bars_held = j - entry_bar + 1
                        break

                if not hit:
                    exit_bar = min(entry_bar + horizon_bars, n - 1)
                    exit_r = (closes[exit_bar] - entry_p) / dist
                    bars_held = horizon_bars

                net_r = exit_r - friction_r
                exit_time = entry_time + bars_held * 15 * 60 * 1000

                s2_trades.append({
                    "time": int(entry_time),
                    "exit_time": int(exit_time),
                    "r_gain": float(net_r),
                    "hold_bars": int(bars_held),
                    "hold_ms": int(bars_held * 15 * 60 * 1000),
                    "symbol": sym,
                    "strategy": "S2_BB",
                    "prob": 0.55,
                    "sleeve_id": 4,
                    "risk": float(risk_usd),
                    "side": 1,
                    "entry_price": float(entry_p)
                })

            # Short mean reversion signal: price breaks upper band & RSI overbought
            elif closes[i] > bb_upper[i] and rsis[i] > rsi_overbought:
                entry_bar = i + 1
                entry_p = opens[entry_bar]
                entry_time = times[entry_bar]
                target_p = entry_p - target_r * dist
                stop_p = entry_p + stop_r * dist
                exit_r = 0.0
                bars_held = horizon_bars
                hit = False

                for j in range(entry_bar, entry_bar + horizon_bars):
                    # Check adverse stop first
                    if highs[j] >= stop_p:
                        exit_r = -stop_r
                        hit = True
                        bars_held = j - entry_bar + 1
                        break
                    if lows[j] <= target_p:
                        exit_r = target_r
                        hit = True
                        bars_held = j - entry_bar + 1
                        break

                if not hit:
                    exit_bar = min(entry_bar + horizon_bars, n - 1)
                    exit_r = (entry_p - closes[exit_bar]) / dist
                    bars_held = horizon_bars

                net_r = exit_r - friction_r
                exit_time = entry_time + bars_held * 15 * 60 * 1000

                s2_trades.append({
                    "time": int(entry_time),
                    "exit_time": int(exit_time),
                    "r_gain": float(net_r),
                    "hold_bars": int(bars_held),
                    "hold_ms": int(bars_held * 15 * 60 * 1000),
                    "symbol": sym,
                    "strategy": "S2_BB",
                    "prob": 0.55,
                    "sleeve_id": 4,
                    "risk": float(risk_usd),
                    "side": -1,
                    "entry_price": float(entry_p)
                })

    df_res = pd.DataFrame(s2_trades)
    if len(df_res) > 0:
        df_res.sort_values("time", inplace=True)
        df_res.reset_index(drop=True, inplace=True)
    return df_res
