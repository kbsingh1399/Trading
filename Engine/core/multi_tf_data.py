"""
Multi-Timeframe Data Helper
Provides 4H resampled data with canonical indicators for Binance USDT-M Perpetuals.
Auto-generates from 15m master parquets if local cache is absent.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
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


def get_or_compute_4h_dataframe(symbol: str, cache_dir: Optional[Path] = None) -> pd.DataFrame:
    """Get 4H dataframe for a symbol, either from disk cache or computed on the fly."""
    if cache_dir is not None and (Path(cache_dir) / f"{symbol}_4h.parquet").exists():
        df = pd.read_parquet(Path(cache_dir) / f"{symbol}_4h.parquet")
        df['time'] = pd.to_datetime(df['time'], utc=True)
        return df.sort_values('time').reset_index(drop=True)

    # Check scratch cache fallback if present
    scratch_cache = REPO_ROOT / "scratch" / "cache_multi_tf" / f"{symbol}_4h.parquet"
    if scratch_cache.exists():
        df = pd.read_parquet(scratch_cache)
        df['time'] = pd.to_datetime(df['time'], utc=True)
        return df.sort_values('time').reset_index(drop=True)

    # Compute dynamically from 15m master parquet
    p_15m = DATA_DIR / f"{symbol}_15m_master_2020_2026.parquet"
    if not p_15m.exists():
        return pd.DataFrame()

    raw_df = pd.read_parquet(p_15m)
    use_cols = [c for c in ['open_time_ms', 'open', 'high', 'low', 'close', 'volume_base', 'spot_cvd_15m', 'taker_buy_vol_btc'] if c in raw_df.columns]
    df = raw_df[use_cols].copy()
    df['time'] = pd.to_datetime(df['open_time_ms'], unit='ms', utc=True)
    agg_dict = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume_base': 'sum'}
    if 'spot_cvd_15m' in df.columns:
        agg_dict['spot_cvd_15m'] = 'sum'
    if 'taker_buy_vol_btc' in df.columns:
        agg_dict['taker_buy_vol_btc'] = 'sum'
    df_4h = df.set_index('time').resample('4h').agg(agg_dict).dropna().reset_index()

    tr = np.maximum(df_4h['high'] - df_4h['low'], np.maximum((df_4h['high'] - df_4h['close'].shift()).abs(), (df_4h['low'] - df_4h['close'].shift()).abs()))
    df_4h['atr'] = tr.rolling(14).mean()
    df_4h['donchian_high'] = df_4h['high'].shift(1).rolling(20).max()
    df_4h['donchian_low'] = df_4h['low'].shift(1).rolling(20).min()
    df_4h['ema_20'] = df_4h['close'].ewm(span=20, adjust=False).mean()
    df_4h['ema_50'] = df_4h['close'].ewm(span=50, adjust=False).mean()
    df_4h['ema_200'] = df_4h['close'].ewm(span=200, adjust=False).mean()
    df_4h['ema_200_slope'] = ((df_4h['ema_200'] - df_4h['ema_200'].shift(12)) / df_4h['atr']).fillna(0.0)
    if 'taker_buy_vol_btc' in df_4h.columns:
        df_4h['buy_vol_ratio'] = (df_4h['taker_buy_vol_btc'] / df_4h['volume_base'].replace(0, np.nan)).fillna(0.5)
    else:
        df_4h['buy_vol_ratio'] = 0.5
    if 'spot_cvd_15m' in df_4h.columns:
        cvd_cum = df_4h['spot_cvd_15m'].cumsum()
        df_4h['spot_cvd_slope'] = (cvd_cum - cvd_cum.shift(3)).fillna(0.0)
    else:
        df_4h['spot_cvd_slope'] = 0.0
    df_4h['next_open'] = df_4h['open'].shift(-1).fillna(df_4h['close'])
    return df_4h.sort_values('time').reset_index(drop=True)


def load_all_4h_data(symbols: Optional[List[str]] = None, cache_dir: Optional[Path] = None) -> Dict[str, pd.DataFrame]:
    """Load or compute 4H data for all specified symbols."""
    if symbols is None:
        symbols = CORE_SYMBOLS
    res = {}
    for sym in symbols:
        df = get_or_compute_4h_dataframe(sym, cache_dir)
        if len(df) > 0:
            res[sym] = df
    return res
