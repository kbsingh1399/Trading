"""
================================================================================
ENGINE: UNIFIED FOREX & CFD MASTER ORCHESTRATION ENGINE
================================================================================
Location: Engine/forex_engine.py
Architecture: Modular SRP, Central Strategy Routing & Extensible Engine Architecture
Guidelines: Karpathy Directives (Simplicity, Surgical, Verifiable, Goal-Driven)

This module serves as the central orchestration engine for Forex & CFD algorithmic trading:
1. DYNAMIC STRATEGY ROUTING : Automatically discovers, loads, and initializes trading
                              strategies via BaseForexStrategy & StrategyRegistry.
2. CONFIG & CRITERIA INGEST : Robustly ingests and validates:
                              - Engine/target_oos_criteria.json
                              - Engine/oos_windows_20.json
3. LIVE BROKER CONNECTIVITY : Resilient MT5 connection, symbol alias mapping,
                              and true UTC offset reconciliation.
4. ORDER & RATCHET GOVERNOR : Dynamic lot sizing ($25-$50 base risk), paper dry-run simulation,
                              live order execution, and 7-stage microstructure ratchets.
5. MULTI-REGIME HARNESS     : Forward-testing, single-window OOS backtesting, and 20 OOS
                              window walk-forward validation with institutional fail-fast gates.
6. STREAMING TELEMETRY      : Rich ASCII terminal dashboard with synchronous and
                              asynchronous/event-loop execution support.
================================================================================
"""
from __future__ import annotations

import os
import sys
import time
import json
import asyncio
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any, Type

import numpy as np
import pandas as pd
import polars as pl
import xgboost as xgb
import MetaTrader5 as mt5

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# -------------------------------------------------------------------------
# PATH ROBUSTNESS & ENVIRONMENT SETUP
# -------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
ENGINE_DIR = CURRENT_FILE.parent
PROJECT_ROOT = ENGINE_DIR.parent

for path_entry in [str(PROJECT_ROOT), str(ENGINE_DIR)]:
    if path_entry not in sys.path:
        sys.path.insert(0, path_entry)

os.environ["PROJECT_ROOT"] = str(PROJECT_ROOT)
os.environ["ENGINE_DIR"] = str(ENGINE_DIR)

from Engine.core.base_strategy import (
    BaseForexStrategy,
    StrategyRegistry,
    EngineConfig,
    StrategySignal,
    BacktestResult,
    TargetCriteria,
    OOSWindow,
)
from Engine.core.strategy_kernel import (
    CANONICAL_FEATURES,
    CANONICAL_18_ASSETS,
    engineer_features_polars,
    create_labels_ratchet,
)

# Explicitly import FVG_ML strategy to register it into StrategyRegistry
try:
    from Engine.FVG_ML_ForexCFD_Strategy import FVGMLForexCFDStrategy
except ImportError:
    try:
        from Engine.strategy.FVG_ML_ForexCFD_Strategy import FVGMLForexCFDStrategy
    except ImportError:
        logging.warning("Could not import FVGMLForexCFDStrategy at startup; will resolve dynamically.")

DATA_DIR = PROJECT_ROOT / "Forex_Backtesting_Data"
MODELS_DIR = ENGINE_DIR / "models"
PRODUCTION_MODEL_PATH = MODELS_DIR / "xgboost_forex.json"
CRITERIA_PATH = ENGINE_DIR / "target_oos_criteria.json"
WINDOWS_PATH = ENGINE_DIR / "oos_windows_20.json"
LOG_DIR = ENGINE_DIR / "live"
LOG_FILE = LOG_DIR / "dry_run.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

console = Console()

# -------------------------------------------------------------------------
# CANONICAL STRATEGY CONSTANTS
# -------------------------------------------------------------------------
BASE_RISK_USD = 50.0
MAX_HOLDING_BARS = 96      # 24 hours in 15m bars
TIME_DECAY_BARS = 24       # 6 hours in 15m bars
TIME_DECAY_THRESHOLD_R = 0.20
MAX_STOP_PCT = 0.025       # 2.5% max stop distance
PROBABILITY_THRESHOLD = 0.55


# -------------------------------------------------------------------------
# COMPONENT 1: METATRADER 5 RESILIENT BROKER CONNECTION
# -------------------------------------------------------------------------
class MT5Connection:
    """Manages resilient MT5 terminal session, symbol aliases, and UTC offsets."""
    def __init__(self, login: Optional[int] = None, password: Optional[str] = None, server: Optional[str] = None):
        self.login = login
        self.password = password
        self.server = server
        self.connected = False
        self._cached_utc_offset = None
        self._last_offset_fetch = 0.0

    def connect(self) -> bool:
        if not mt5.initialize():
            logging.error(f"MT5 initialize() failed, error code: {mt5.last_error()}")
            return False

        if self.login and self.password and self.server:
            authorized = mt5.login(self.login, password=self.password, server=self.server)
            if not authorized:
                logging.error(f"Failed to login account #{self.login}: {mt5.last_error()}")
                return False
            logging.info(f"Connected to MT5 account #{self.login} on {self.server}")
        else:
            logging.info("Connected to active MT5 terminal instance.")

        self.connected = True
        return True

    def disconnect(self) -> None:
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logging.info("Disconnected from MT5 cleanly.")

    def resolve_symbol(self, symbol: str) -> str:
        """Resolves broker symbol name and suffix (.pi for Forex, .p for CFDs, aliases)."""
        aliases = {
            "GER30": "GER40.p",
            "GER30.p": "GER40.p",
            "GER40": "GER40.p",
            "DE40": "GER40.p",
        }
        if symbol in aliases:
            target = aliases[symbol]
            mt5.symbol_select(target, True)
            return target

        info = mt5.symbol_info(symbol)
        if info is not None:
            if not info.visible:
                mt5.symbol_select(symbol, True)
            return symbol

        for suffix in [".pi", ".p", ".r", ".m", ""]:
            cand = symbol + suffix
            info = mt5.symbol_info(cand)
            if info is not None:
                if not info.visible:
                    mt5.symbol_select(cand, True)
                return cand

        logging.warning(f"Could not resolve exact broker symbol for: {symbol}")
        return symbol

    def get_broker_utc_offset(self) -> int:
        """Calculates broker server time offset from UTC in seconds."""
        if self._cached_utc_offset is not None and (time.time() - self._last_offset_fetch < 3600):
            return self._cached_utc_offset

        if not self.connected:
            return 3 * 3600  # Default Blueberry summer offset: UTC+3

        for check_sym in ["EURUSD.pi", "EURUSD", "EURUSD.p"]:
            tick = mt5.symbol_info_tick(check_sym)
            if tick is not None:
                now_utc_ts = datetime.now(timezone.utc).timestamp()
                offset = int(round((tick.time - now_utc_ts) / 3600.0) * 3600)
                self._cached_utc_offset = offset
                self._last_offset_fetch = time.time()
                return offset

        return 3 * 3600

    def get_last_tick(self, symbol: str) -> Optional[Any]:
        if not self.connected:
            return None
        real_symbol = self.resolve_symbol(symbol)
        return mt5.symbol_info_tick(real_symbol)

    def get_15m_bars(self, symbol: str, count: int = 250) -> pd.DataFrame:
        if not self.connected:
            return pd.DataFrame()
        real_symbol = self.resolve_symbol(symbol)
        rates = mt5.copy_rates_from_pos(real_symbol, mt5.TIMEFRAME_M15, 0, count)
        if rates is None or len(rates) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(rates)
        offset = self.get_broker_utc_offset()
        df['time_broker'] = df['time']
        df['time'] = df['time'] - offset
        df['datetime'] = pd.to_datetime(df['time'], unit='s', utc=True)
        return df

    def get_4h_bars(self, symbol: str, count: int = 250) -> pd.DataFrame:
        if not self.connected:
            return pd.DataFrame()
        real_symbol = self.resolve_symbol(symbol)
        rates = mt5.copy_rates_from_pos(real_symbol, mt5.TIMEFRAME_H4, 0, count)
        if rates is None or len(rates) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(rates)
        offset = self.get_broker_utc_offset()
        df['time_broker'] = df['time']
        df['time'] = df['time'] - offset
        df['datetime'] = pd.to_datetime(df['time'], unit='s', utc=True)
        return df


# -------------------------------------------------------------------------
# COMPONENT 2: ORDER MANAGEMENT & MICROSTRUCTURE RATCHETS
# -------------------------------------------------------------------------
class OrderManager:
    """Handles dynamic lot sizing, paper dry-run simulation, and live microstructure ratchets."""
    def __init__(self, connection: MT5Connection, dry_run: bool = True):
        self.conn = connection
        self.dry_run = dry_run
        self.open_trades: Dict[int, Dict[str, Any]] = {}

    def calculate_lot_size(self, symbol: str, risk_usd: float, sl_dist: float) -> float:
        """Calculates exact lot size based on symbol contract size and currency conversion."""
        if not self.conn.connected or sl_dist <= 0:
            return 0.01

        real_symbol = self.conn.resolve_symbol(symbol)
        sym_info = mt5.symbol_info(real_symbol)
        if sym_info is None:
            return 0.01

        vol_min = sym_info.volume_min
        vol_step = sym_info.volume_step
        trade_contract = sym_info.trade_contract_size
        point = sym_info.point

        tick_val = sym_info.trade_tick_value
        tick_sz = sym_info.trade_tick_size

        if tick_sz > 0 and tick_val > 0:
            loss_per_lot = (sl_dist / tick_sz) * tick_val
        else:
            loss_per_lot = sl_dist * trade_contract

        if loss_per_lot <= 0:
            return vol_min

        raw_lot = risk_usd / loss_per_lot
        steps = round((raw_lot - vol_min) / vol_step)
        calc_lot = vol_min + (steps * vol_step)
        return float(np.clip(calc_lot, vol_min, sym_info.volume_max))

    def place_market_order(
        self,
        symbol: str,
        order_type: int,
        volume: float,
        sl_price: float,
        tp_price: float,
        risk_usd: float,
        strategy_tag: str = "COMBINED"
    ) -> Optional[int]:
        real_symbol = self.conn.resolve_symbol(symbol)
        action_name = "BUY" if order_type == mt5.ORDER_TYPE_BUY else "SELL"

        if self.dry_run:
            fake_ticket = int(time.time() * 1000) % 100000000
            tick = self.conn.get_last_tick(symbol)
            fill_price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid if tick else 1.0

            r_dist = abs(fill_price - sl_price)
            self.open_trades[fake_ticket] = {
                "ticket": fake_ticket,
                "symbol": symbol,
                "real_symbol": real_symbol,
                "type": order_type,
                "action": action_name,
                "volume": volume,
                "entry": fill_price,
                "sl": sl_price,
                "tp": tp_price,
                "risk_usd": risk_usd,
                "r_dist": r_dist,
                "entry_time": datetime.now(timezone.utc),
                "bars_held": 0,
                "strategy": strategy_tag,
                "highest_r": 0.0,
                "lowest_r": 0.0,
                "ratchet_phase": 0
            }
            logging.info(f"[PAPER ORDER] {action_name} {volume:.2f}L {symbol} @ {fill_price:.5f} | SL={sl_price:.5f} | TP={tp_price:.5f} | #{fake_ticket}")
            return fake_ticket

        # Real Live Broker Order
        tick = self.conn.get_last_tick(symbol)
        price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": real_symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": sl_price,
            "tp": tp_price,
            "deviation": 10,
            "magic": 10101,
            "comment": f"Auto-{strategy_tag}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        res = mt5.order_send(request)
        if res.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"[LIVE ORDER FAILED] {symbol} {action_name}: {res.comment} ({res.retcode})")
            return None

        logging.info(f"[LIVE ORDER FILLED] {action_name} {volume:.2f}L {symbol} @ {price:.5f} | Ticket: {res.order}")
        return res.order

    def modify_sl(self, ticket: int, new_sl: float) -> bool:
        if self.dry_run:
            if ticket in self.open_trades:
                old_sl = self.open_trades[ticket]["sl"]
                self.open_trades[ticket]["sl"] = new_sl
                logging.info(f"[PAPER RATCHET] #{ticket} SL modified: {old_sl:.5f} -> {new_sl:.5f}")
                return True
            return False

        trade = self.open_trades.get(ticket)
        if not trade:
            return False
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": trade["real_symbol"],
            "sl": new_sl,
            "tp": trade["tp"]
        }
        res = mt5.order_send(request)
        return (res.retcode == mt5.TRADE_RETCODE_DONE)

    def close_trade(self, ticket: int, reason: str = "NORMAL") -> None:
        if ticket not in self.open_trades:
            return
        t = self.open_trades.pop(ticket)
        logging.info(f"[TRADE CLOSED] #{ticket} {t['symbol']} | Reason: {reason}")

    def manage_open_trades(self, current_bar_time: datetime) -> None:
        """Applies 7-stage microstructure ratchets and time-decay exits."""
        for ticket, trade in list(self.open_trades.items()):
            sym = trade["symbol"]
            tick = self.conn.get_last_tick(sym)
            if tick is None:
                continue

            entry = trade["entry"]
            r_dist = trade["r_dist"]
            if r_dist <= 0:
                continue

            is_long = (trade["type"] == mt5.ORDER_TYPE_BUY)
            cur_price = tick.bid if is_long else tick.ask

            if is_long:
                gain_r = (cur_price - entry) / r_dist
                hit_sl = (tick.bid <= trade["sl"])
                hit_tp = (tick.bid >= trade["tp"])
            else:
                gain_r = (entry - cur_price) / r_dist
                hit_sl = (tick.ask >= trade["sl"])
                hit_tp = (tick.ask <= trade["tp"])

            trade["highest_r"] = max(trade["highest_r"], gain_r)
            trade["bars_held"] += 1

            if hit_sl:
                self.close_trade(ticket, reason=f"STOP LOSS (R={gain_r:.2f}R)")
                continue
            if hit_tp:
                self.close_trade(ticket, reason=f"TAKE PROFIT (R={gain_r:.2f}R)")
                continue

            # Time decay exit
            if trade["bars_held"] >= TIME_DECAY_BARS and trade["highest_r"] < TIME_DECAY_THRESHOLD_R:
                self.close_trade(ticket, reason=f"TIME DECAY EXIT (Bars: {trade['bars_held']}, R={gain_r:.2f}R)")
                continue

            # 7-Stage Ratchet Logic
            new_sl_r = None
            if gain_r >= 3.5:
                new_sl_r = 3.3
            elif gain_r >= 3.0:
                new_sl_r = 2.8
            elif gain_r >= 2.5:
                new_sl_r = 2.3
            elif gain_r >= 2.0:
                new_sl_r = 1.8
            elif gain_r >= 1.5:
                new_sl_r = 1.0
            elif gain_r >= 1.0:
                new_sl_r = 0.15

            if new_sl_r is not None:
                if is_long:
                    candidate_sl = entry + (new_sl_r * r_dist)
                    if candidate_sl > trade["sl"]:
                        self.modify_sl(ticket, candidate_sl)
                else:
                    candidate_sl = entry - (new_sl_r * r_dist)
                    if candidate_sl < trade["sl"] or trade["sl"] == 0:
                        self.modify_sl(ticket, candidate_sl)


# -------------------------------------------------------------------------
# COMPONENT 3: MATHEMATICAL FEATURE EXTRACTION & PARITY KERNEL
# -------------------------------------------------------------------------
def compute_features_pandas(df: pd.DataFrame, buffer_4h: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Computes all 13 canonical stationary features with zero lookahead."""
    df = df.copy()

    # 1. Moving Averages
    df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()

    # 2. VWAP (Typical Price proxy)
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3.0
    df['vwap_20'] = df['typical_price'].rolling(window=20, min_periods=20).mean()
    df['vwap_dist'] = (df['close'] - df['vwap_20']) / df['vwap_20']

    # 3. RSI (14 periods)
    delta = df['close'].diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(span=14, adjust=False).mean()
    avg_loss = loss.ewm(span=14, adjust=False).mean()
    rs = avg_gain / (avg_loss + 1e-12)
    df['rsi_14'] = 100.0 - (100.0 / (1.0 + rs))

    # 4. Fair Value Gaps (Rolling Unmitigated Lookback w=5)
    w = 5
    bullish_fvgs = []
    bearish_fvgs = []
    for k in range(w):
        bull = (df['low'].rolling(k+1, min_periods=k+1).min() - df['high'].shift(k+2)).fillna(0.0).clip(lower=0.0)
        bear = (df['low'].shift(k+2) - df['high'].rolling(k+1, min_periods=k+1).max()).fillna(0.0).clip(lower=0.0)
        bullish_fvgs.append(bull)
        bearish_fvgs.append(bear)

    df['bullish_fvg'] = pd.concat(bullish_fvgs, axis=1).max(axis=1).fillna(0.0)
    df['bearish_fvg'] = pd.concat(bearish_fvgs, axis=1).max(axis=1).fillna(0.0)

    # 5. Distances & Slopes
    df['ema_50_dist'] = (df['close'] - df['ema_50']) / df['ema_50']
    df['ema_200_dist'] = (df['close'] - df['ema_200']) / df['ema_200']
    df['ema_200_slope'] = df['ema_200'] - df['ema_200'].shift(12)

    # 6. ATR & Volatility
    df['atr_14'] = (df['high'] - df['low']).rolling(window=14).mean()
    df['volatility_20'] = df['close'].rolling(window=20).std() / df['close']
    df['roc_20'] = (df['close'] / df['close'].shift(20)) - 1.0

    # 7. Time Features (UTC)
    if isinstance(df.index, pd.DatetimeIndex):
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek + 1
    else:
        df['hour'] = 0
        df['day_of_week'] = 1

    # 8. 4H Trend Alignment (Causal: from previous closed 4H bar)
    htf_4h_trend_val = 0.0
    if buffer_4h is not None and not buffer_4h.empty and len(buffer_4h) >= 205:
        b4h = buffer_4h.copy()
        b4h['ema_200_4h'] = b4h['close'].ewm(span=200, adjust=False).mean()
        b4h['htf_4h_trend'] = b4h['ema_200_4h'] - b4h['ema_200_4h'].shift(5)
        b4h['htf_4h_trend_causal'] = b4h['htf_4h_trend'].shift(1)
        valid = b4h['htf_4h_trend_causal'].dropna()
        if len(valid) > 0:
            htf_4h_trend_val = float(valid.iloc[-1])

    df['htf_4h_trend'] = htf_4h_trend_val
    for col in CANONICAL_FEATURES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    return df[CANONICAL_FEATURES]


def compute_crt_orb_state(buffer: pd.DataFrame) -> dict:
    """Computes live CRT/ORB session state from the 15m rolling buffer."""
    default = dict(is_long_crt=False, is_short_crt=False,
                   or_high=0.0, or_low=0.0, body_ratio=0.0,
                   judas_long=False, judas_short=False, session="None")

    if buffer.empty or len(buffer) < 10:
        return default

    df = buffer.copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        return default

    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")

    df["_hour"]   = df.index.hour
    df["_minute"] = df.index.minute
    df["_date"]   = df.index.date

    for sess_hour, sess_min, sess_name in [(7, 0, "London"), (13, 30, "NY")]:
        or_bars = df[(df["_hour"] == sess_hour) & (df["_minute"] == sess_min)]
        if or_bars.empty:
            continue

        or_start_idx = or_bars.index[-1]
        pos = df.index.get_loc(or_start_idx)
        if pos + 1 >= len(df):
            continue

        or_slice = df.iloc[pos : pos + 2]
        or_high  = float(or_slice["high"].max())
        or_low   = float(or_slice["low"].min())
        or_range = or_high - or_low
        if or_range <= 0:
            continue

        or_date    = or_start_idx.date()
        prev_bars  = df[df["_date"] < or_date]
        if prev_bars.empty:
            prev_day_high = float(df["high"].iloc[0])
            prev_day_low  = float(df["low"].iloc[0])
        else:
            prev_day_high = float(prev_bars["high"].max())
            prev_day_low  = float(prev_bars["low"].min())

        pre_start = max(0, pos - 6)
        pre_slice = df.iloc[pre_start:pos]
        if not pre_slice.empty:
            pre_low  = float(pre_slice["low"].min())
            pre_high = float(pre_slice["high"].max())
            judas_long  = (pre_low  < prev_day_low)  and (or_low  >= prev_day_low)
            judas_short = (pre_high > prev_day_high) and (or_high <= prev_day_high)
        else:
            judas_long = judas_short = False

        post_slice = df.iloc[pos + 2:]
        for _, bar in post_slice.iterrows():
            body = abs(bar["close"] - bar["open"])
            wick = bar["high"] - bar["low"] + 1e-9
            body_ratio = min(1.0, body / wick)

            if bar["close"] > or_high and body_ratio >= 0.40:
                return dict(is_long_crt=True, is_short_crt=False,
                            or_high=or_high, or_low=or_low,
                            body_ratio=body_ratio,
                            judas_long=judas_long, judas_short=judas_short,
                            session=sess_name)

            if bar["close"] < or_low and body_ratio >= 0.40:
                return dict(is_long_crt=False, is_short_crt=True,
                            or_high=or_high, or_low=or_low,
                            body_ratio=body_ratio,
                            judas_long=judas_long, judas_short=judas_short,
                            session=sess_name)

    return default


# -------------------------------------------------------------------------
# COMPONENT 4: STATEFUL INFERENCE ENGINE
# -------------------------------------------------------------------------
class StatefulInferenceEngine:
    """Maintains rolling buffer of closed 15m and 4H bars for real-time inference."""
    def __init__(self, symbol: str, max_bars: int = 1000):
        self.symbol = symbol
        self.max_bars = max_bars
        self.buffer: pd.DataFrame = pd.DataFrame()
        self.buffer_4h: pd.DataFrame = pd.DataFrame()
        self.is_warm = False
        self.mt5_conn = None

    def warm_start(self, mt5_conn: MT5Connection) -> bool:
        self.mt5_conn = mt5_conn
        bars_df = mt5_conn.get_15m_bars(self.symbol, count=self.max_bars)
        if bars_df.empty or len(bars_df) < 50:
            return False

        bars_df = bars_df.iloc[:-1].copy()
        if 'datetime' in bars_df.columns:
            bars_df.set_index('datetime', inplace=True)
        elif 'time' in bars_df.columns:
            bars_df['datetime'] = pd.to_datetime(bars_df['time'], unit='s', utc=True)
            bars_df.set_index('datetime', inplace=True)

        bars_df.rename(columns={'tick_volume': 'volume'}, inplace=True)
        self.buffer = bars_df[['open', 'high', 'low', 'close', 'volume']].copy()

        bars_4h_df = mt5_conn.get_4h_bars(self.symbol, count=250)
        if not bars_4h_df.empty and len(bars_4h_df) > 1:
            bars_4h_df = bars_4h_df.iloc[:-1].copy()
            if 'datetime' in bars_4h_df.columns:
                bars_4h_df.set_index('datetime', inplace=True)
            self.buffer_4h = bars_4h_df[['open', 'high', 'low', 'close']].copy()

        self.is_warm = True
        return True

    def update_bar(self, new_bar: Dict[str, float]) -> None:
        new_df = pd.DataFrame([new_bar])
        if 'datetime' in new_df.columns:
            new_df.set_index('datetime', inplace=True)
        elif 'time' in new_df.columns:
            new_df['datetime'] = pd.to_datetime(new_df['time'], unit='s', utc=True)
            new_df.set_index('datetime', inplace=True)

        if self.buffer.empty:
            self.buffer = new_df
        else:
            self.buffer = pd.concat([self.buffer, new_df])
            if len(self.buffer) > self.max_bars:
                self.buffer = self.buffer.iloc[-self.max_bars:].copy()

    def refresh_4h_buffer(self) -> None:
        if self.mt5_conn and self.mt5_conn.connected:
            bars_4h_df = self.mt5_conn.get_4h_bars(self.symbol, count=250)
            if not bars_4h_df.empty and len(bars_4h_df) >= 205:
                bars_4h_df = bars_4h_df.iloc[:-1].copy()
                if 'datetime' in bars_4h_df.columns:
                    bars_4h_df.set_index('datetime', inplace=True)
                self.buffer_4h = bars_4h_df[['open', 'high', 'low', 'close']].copy()

    def compute_features(self) -> pd.DataFrame:
        return compute_features_pandas(self.buffer, self.buffer_4h)

    def predict(self, xgb_model: xgb.Booster) -> float:
        if self.buffer.empty:
            return 0.50
        features_df = self.compute_features()
        latest = features_df.iloc[[-1]].copy()
        for col in latest.columns:
            latest[col] = pd.to_numeric(latest[col], errors="coerce").astype(float)
        dmat = xgb.DMatrix(latest)
        prob = float(xgb_model.predict(dmat)[0])
        del dmat
        return prob

    def compute_crt_orb(self) -> dict:
        return compute_crt_orb_state(self.buffer)


# -------------------------------------------------------------------------
# COMPONENT 5: PRE-FLIGHT MARKET DATA SYNCHRONIZER & RETRAINING
# -------------------------------------------------------------------------
def pre_flight_data_sync(mt5_conn: MT5Connection, single_asset: Optional[str] = None) -> None:
    """Synchronizes historical parquet files directly with latest broker bars."""
    target_assets = [single_asset] if single_asset else CANONICAL_18_ASSETS
    for sym in target_assets:
        parquet_path = DATA_DIR / f"{sym}.parquet"
        if not parquet_path.exists():
            continue

        try:
            existing_df = pl.read_parquet(parquet_path)
            last_ts = existing_df['datetime'].max()
            if isinstance(last_ts, str):
                last_dt = pd.to_datetime(last_ts, utc=True)
            else:
                last_dt = pd.to_datetime(last_ts, unit='ms', utc=True)

            rates = mt5_conn.get_15m_bars(sym, count=300)
            if rates.empty:
                continue

            new_rates = rates[rates['datetime'] > last_dt].copy()
            if new_rates.empty:
                continue

            new_rates.rename(columns={'tick_volume': 'volume'}, inplace=True)
            new_pl = pl.DataFrame({
                'datetime': new_rates['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S').to_list(),
                'open': new_rates['open'].to_list(),
                'high': new_rates['high'].to_list(),
                'low': new_rates['low'].to_list(),
                'close': new_rates['close'].to_list(),
                'volume': new_rates['volume'].to_list()
            })

            combined_pl = pl.concat([existing_df, new_pl]).unique(subset=['datetime']).sort('datetime')
            combined_pl.write_parquet(parquet_path)
        except Exception as e:
            logging.warning(f"Failed sync for {sym}: {e}")


def dynamic_retrain() -> None:
    """Retrains the production XGBoost model across all 18 canonical assets."""
    console.print("[bold cyan]Executing dynamic retrain across 18 canonical assets...[/bold cyan]")
    train_X = []
    train_y = []

    for sym in CANONICAL_18_ASSETS:
        try:
            df = engineer_features_polars(sym, DATA_DIR)
            df = create_labels_ratchet(df)
            valid = df[df['target'].notna()]
            if len(valid) > 0:
                train_X.append(valid[CANONICAL_FEATURES])
                train_y.append(valid['target'].values)
        except Exception as e:
            logging.warning(f"Dynamic retrain feature error for {sym}: {e}")

    if not train_X:
        raise RuntimeError("No training setups could be generated.")

    X_mat = pd.concat(train_X, ignore_index=True)
    y_vec = np.concatenate(train_y)

    dtrain = xgb.DMatrix(X_mat, label=y_vec)
    params = {
        'objective': 'binary:logistic',
        'max_depth': 4,
        'learning_rate': 0.05,
        'eval_metric': 'logloss',
        'seed': 42
    }
    booster = xgb.train(params, dtrain, num_boost_round=120)
    booster.save_model(str(PRODUCTION_MODEL_PATH))
    console.print(f"[bold green]Dynamic retrain complete. Saved to {PRODUCTION_MODEL_PATH}[/bold green]")


# -------------------------------------------------------------------------
# COMPONENT 6: BUILT-IN STRATEGY PLUGINS
# -------------------------------------------------------------------------
@StrategyRegistry.register("fvg")
class ICTFVGStrategy(BaseForexStrategy):
    """Rule-based ICT Fair Value Gap + Liquidity Sweep Strategy."""
    name: str = "fvg"
    description: str = "Rule-based ICT FVG and PDL/PDH Liquidity Sweep Strategy"

    def initialize(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig.load()
        self.initialized = True

    def generate_signal(
        self,
        symbol: str,
        buffer_15m: pd.DataFrame,
        buffer_4h: Optional[pd.DataFrame] = None,
        current_tick: Optional[Any] = None
    ) -> StrategySignal:
        if buffer_15m.empty or len(buffer_15m) < 25:
            return StrategySignal(symbol=symbol, signal=0, reason="Insufficient Data")

        feat_df = compute_features_pandas(buffer_15m, buffer_4h)
        last = feat_df.iloc[-1]
        trend = last.get("htf_4h_trend", 0.0)
        bull_fvg = last.get("bullish_fvg", 0.0)
        bear_fvg = last.get("bearish_fvg", 0.0)

        dt = buffer_15m['datetime'].iloc[-1] if 'datetime' in buffer_15m else pd.Timestamp.utcnow()
        hour = dt.hour if hasattr(dt, 'hour') else 12
        is_kz = (7 <= hour <= 10) or (12 <= hour <= 15)

        local_low = buffer_15m['low'].iloc[-20:].min()
        local_high = buffer_15m['high'].iloc[-20:].max()
        bid = current_tick.bid if current_tick else float(buffer_15m['close'].iloc[-1])
        ask = current_tick.ask if current_tick else float(buffer_15m['close'].iloc[-1])

        if not is_kz:
            return StrategySignal(symbol=symbol, signal=0, reason="HOLD (Off-Hours)")

        if trend > 0 and bull_fvg > 0:
            entry = ask
            sl = local_low
            r_dist = entry - sl
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                return StrategySignal(symbol=symbol, signal=0, reason="HOLD (Stop Range Invalid)")
            return StrategySignal(
                symbol=symbol, signal=1, entry_price=entry, sl_price=sl,
                tp_price=entry + (2.5 * r_dist), strategy_tag="FVG", reason="BUY (ICT FVG)"
            )
        elif trend < 0 and bear_fvg > 0:
            entry = bid
            sl = local_high
            r_dist = sl - entry
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                return StrategySignal(symbol=symbol, signal=0, reason="HOLD (Stop Range Invalid)")
            return StrategySignal(
                symbol=symbol, signal=-1, entry_price=entry, sl_price=sl,
                tp_price=entry - (2.5 * r_dist), strategy_tag="FVG", reason="SELL (ICT FVG)"
            )

        return StrategySignal(symbol=symbol, signal=0, reason="HOLD (No FVG Setup)")

    def run_backtest(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        save_plot: bool = True
    ) -> BacktestResult:
        # Standard backtest delegation
        return run_standard_backtest(self, start_date, end_date, symbols, save_plot)


@StrategyRegistry.register("crt")
class CRTStrategy(BaseForexStrategy):
    """Candle Range Theory & Opening Range Breakout Strategy."""
    name: str = "crt"
    description: str = "Candle Range Theory & London/NY Opening Range Breakout Strategy"

    def initialize(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig.load()
        self.initialized = True

    def generate_signal(
        self,
        symbol: str,
        buffer_15m: pd.DataFrame,
        buffer_4h: Optional[pd.DataFrame] = None,
        current_tick: Optional[Any] = None
    ) -> StrategySignal:
        if buffer_15m.empty or len(buffer_15m) < 25:
            return StrategySignal(symbol=symbol, signal=0, reason="Insufficient Data")

        feat_df = compute_features_pandas(buffer_15m, buffer_4h)
        trend = feat_df.iloc[-1].get("htf_4h_trend", 0.0)
        crt = compute_crt_orb_state(buffer_15m)

        dt = buffer_15m['datetime'].iloc[-1] if 'datetime' in buffer_15m else pd.Timestamp.utcnow()
        hour = dt.hour if hasattr(dt, 'hour') else 12
        is_kz = (7 <= hour <= 10) or (12 <= hour <= 15)

        bid = current_tick.bid if current_tick else float(buffer_15m['close'].iloc[-1])
        ask = current_tick.ask if current_tick else float(buffer_15m['close'].iloc[-1])

        if not is_kz:
            return StrategySignal(symbol=symbol, signal=0, reason="HOLD (Off-Hours)")

        is_long = crt["is_long_crt"] and (trend > 0 or crt["judas_long"])
        is_short = crt["is_short_crt"] and (trend < 0 or crt["judas_short"])

        if is_long:
            entry = ask
            sl = crt["or_low"] if crt["or_low"] > 0 else buffer_15m['low'].iloc[-20:].min()
            r_dist = entry - sl
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                return StrategySignal(symbol=symbol, signal=0, reason="HOLD (Stop Range Invalid)")
            return StrategySignal(
                symbol=symbol, signal=1, entry_price=entry, sl_price=sl,
                tp_price=entry + (2.5 * r_dist), strategy_tag="CRT", reason="BUY (CRT/ORB Breakout)"
            )
        elif is_short:
            entry = bid
            sl = crt["or_high"] if crt["or_high"] > 0 else buffer_15m['high'].iloc[-20:].max()
            r_dist = sl - entry
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                return StrategySignal(symbol=symbol, signal=0, reason="HOLD (Stop Range Invalid)")
            return StrategySignal(
                symbol=symbol, signal=-1, entry_price=entry, sl_price=sl,
                tp_price=entry - (2.5 * r_dist), strategy_tag="CRT", reason="SELL (CRT/ORB Breakdown)"
            )

        return StrategySignal(symbol=symbol, signal=0, reason="HOLD (No CRT Breakout)")

    def run_backtest(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        save_plot: bool = True
    ) -> BacktestResult:
        return run_standard_backtest(self, start_date, end_date, symbols, save_plot)


@StrategyRegistry.register("ml")
class MLStrategy(BaseForexStrategy):
    """Pure XGBoost Machine Learning Probability Strategy."""
    name: str = "ml"
    description: str = "Pure XGBoost Machine Learning Probability Classifier Strategy"

    def __init__(self, config: Optional[EngineConfig] = None):
        super().__init__(config)
        self.model = None
        self.prob_threshold = PROBABILITY_THRESHOLD
        self.initialize(self.config)

    def initialize(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig.load()
        if PRODUCTION_MODEL_PATH.exists():
            self.model = xgb.Booster()
            self.model.load_model(str(PRODUCTION_MODEL_PATH))
        self.initialized = True

    def generate_signal(
        self,
        symbol: str,
        buffer_15m: pd.DataFrame,
        buffer_4h: Optional[pd.DataFrame] = None,
        current_tick: Optional[Any] = None
    ) -> StrategySignal:
        if buffer_15m.empty or len(buffer_15m) < 25 or self.model is None:
            return StrategySignal(symbol=symbol, signal=0, reason="Engine Not Ready")

        feat_df = compute_features_pandas(buffer_15m, buffer_4h)
        trend = feat_df.iloc[-1].get("htf_4h_trend", 0.0)

        dmat = xgb.DMatrix(feat_df[CANONICAL_FEATURES].iloc[[-1]])
        prob = float(self.model.predict(dmat)[0])

        dt = buffer_15m['datetime'].iloc[-1] if 'datetime' in buffer_15m else pd.Timestamp.utcnow()
        hour = dt.hour if hasattr(dt, 'hour') else 12
        is_kz = (7 <= hour <= 10) or (12 <= hour <= 15)

        bid = current_tick.bid if current_tick else float(buffer_15m['close'].iloc[-1])
        ask = current_tick.ask if current_tick else float(buffer_15m['close'].iloc[-1])
        local_low = buffer_15m['low'].iloc[-20:].min()
        local_high = buffer_15m['high'].iloc[-20:].max()

        if not is_kz:
            return StrategySignal(symbol=symbol, signal=0, prob=prob, reason="HOLD (Off-Hours)")

        if trend > 0 and prob >= self.prob_threshold:
            entry = ask
            sl = local_low
            r_dist = entry - sl
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                return StrategySignal(symbol=symbol, signal=0, prob=prob, reason="HOLD (Stop Range Invalid)")
            return StrategySignal(
                symbol=symbol, signal=1, prob=prob, entry_price=entry, sl_price=sl,
                tp_price=entry + (2.5 * r_dist), strategy_tag="ML", reason="BUY (ML Signal)"
            )
        elif trend < 0 and prob >= self.prob_threshold:
            entry = bid
            sl = local_high
            r_dist = sl - entry
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                return StrategySignal(symbol=symbol, signal=0, prob=prob, reason="HOLD (Stop Range Invalid)")
            return StrategySignal(
                symbol=symbol, signal=-1, prob=prob, entry_price=entry, sl_price=sl,
                tp_price=entry - (2.5 * r_dist), strategy_tag="ML", reason="SELL (ML Signal)"
            )

        return StrategySignal(symbol=symbol, signal=0, prob=prob, reason="HOLD (Low Probability)")

    def run_backtest(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        save_plot: bool = True
    ) -> BacktestResult:
        return run_standard_backtest(self, start_date, end_date, symbols, save_plot)


@StrategyRegistry.register("combined")
class CombinedStrategy(BaseForexStrategy):
    """Multi-confluence FVG + CRT + Machine Learning Strategy."""
    name: str = "combined"
    description: str = "Multi-Confluence: ICT FVG or CRT aligned with Causal XGBoost ML"

    def __init__(self, config: Optional[EngineConfig] = None):
        super().__init__(config)
        self.model = None
        self.prob_threshold = PROBABILITY_THRESHOLD
        self.initialize(self.config)

    def initialize(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig.load()
        if PRODUCTION_MODEL_PATH.exists():
            self.model = xgb.Booster()
            self.model.load_model(str(PRODUCTION_MODEL_PATH))
        self.initialized = True

    def generate_signal(
        self,
        symbol: str,
        buffer_15m: pd.DataFrame,
        buffer_4h: Optional[pd.DataFrame] = None,
        current_tick: Optional[Any] = None
    ) -> StrategySignal:
        if buffer_15m.empty or len(buffer_15m) < 25 or self.model is None:
            return StrategySignal(symbol=symbol, signal=0, reason="Engine Not Ready")

        feat_df = compute_features_pandas(buffer_15m, buffer_4h)
        trend = feat_df.iloc[-1].get("htf_4h_trend", 0.0)
        bull_fvg = feat_df.iloc[-1].get("bullish_fvg", 0.0)
        bear_fvg = feat_df.iloc[-1].get("bearish_fvg", 0.0)
        crt = compute_crt_orb_state(buffer_15m)

        dmat = xgb.DMatrix(feat_df[CANONICAL_FEATURES].iloc[[-1]])
        prob = float(self.model.predict(dmat)[0])

        dt = buffer_15m['datetime'].iloc[-1] if 'datetime' in buffer_15m else pd.Timestamp.utcnow()
        hour = dt.hour if hasattr(dt, 'hour') else 12
        is_kz = (7 <= hour <= 10) or (12 <= hour <= 15)

        bid = current_tick.bid if current_tick else float(buffer_15m['close'].iloc[-1])
        ask = current_tick.ask if current_tick else float(buffer_15m['close'].iloc[-1])
        local_low = buffer_15m['low'].iloc[-20:].min()
        local_high = buffer_15m['high'].iloc[-20:].max()

        if not is_kz:
            return StrategySignal(symbol=symbol, signal=0, prob=prob, reason="HOLD (Off-Hours)")

        is_long = ((trend > 0 and bull_fvg > 0) or crt["is_long_crt"]) and (prob >= self.prob_threshold)
        is_short = ((trend < 0 and bear_fvg > 0) or crt["is_short_crt"]) and (prob >= self.prob_threshold)

        if is_long:
            entry = ask
            sl = crt["or_low"] if crt["is_long_crt"] and crt["or_low"] > 0 else local_low
            r_dist = entry - sl
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                return StrategySignal(symbol=symbol, signal=0, prob=prob, reason="HOLD (Stop Range Invalid)")
            return StrategySignal(
                symbol=symbol, signal=1, prob=prob, entry_price=entry, sl_price=sl,
                tp_price=entry + (2.5 * r_dist), strategy_tag="COMBINED", reason="BUY (Multi-Confluence)"
            )
        elif is_short:
            entry = bid
            sl = crt["or_high"] if crt["is_short_crt"] and crt["or_high"] > 0 else local_high
            r_dist = sl - entry
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                return StrategySignal(symbol=symbol, signal=0, prob=prob, reason="HOLD (Stop Range Invalid)")
            return StrategySignal(
                symbol=symbol, signal=-1, prob=prob, entry_price=entry, sl_price=sl,
                tp_price=entry - (2.5 * r_dist), strategy_tag="COMBINED", reason="SELL (Multi-Confluence)"
            )

        return StrategySignal(symbol=symbol, signal=0, prob=prob, reason="HOLD (No Multi-Confluence)")

    def run_backtest(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        save_plot: bool = True
    ) -> BacktestResult:
        return run_standard_backtest(self, start_date, end_date, symbols, save_plot)


def run_standard_backtest(
    strategy: BaseForexStrategy,
    start_date: str,
    end_date: Optional[str] = None,
    symbols: Optional[List[str]] = None,
    save_plot: bool = True
) -> BacktestResult:
    """Generic backtesting runner for rule-based and combined strategies."""
    target_symbols = symbols or CANONICAL_18_ASSETS
    initial_cap = strategy.config.criteria.initial_capital_usd
    base_risk = strategy.config.criteria.base_risk_usd

    all_trades = []
    per_asset = {}
    b_returns = []

    for sym in target_symbols:
        try:
            df = engineer_features_polars(sym, DATA_DIR)
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            mask = df['datetime'] >= start_date
            if end_date:
                mask = mask & (df['datetime'] <= end_date)
            df_oos = df[mask].copy().reset_index(drop=True)
            if len(df_oos) < 50:
                continue

            b_ret = (df_oos['close'].iloc[-1] / df_oos['close'].iloc[0]) - 1.0
            b_returns.append(b_ret)

            # Evaluate each bar sequentially using strategy signal
            trades = []
            n_bars = len(df_oos)
            i = 25
            while i < n_bars - 10:
                sub_slice = df_oos.iloc[max(0, i-250):i+1].copy()
                sub_slice.set_index('datetime', inplace=True)
                sig = strategy.generate_signal(sym, sub_slice)
                if not sig.is_active:
                    i += 1
                    continue

                entry_bar = i + 1
                if entry_bar >= n_bars:
                    break
                entry_price = df_oos['open'].iloc[entry_bar]
                sl_price = sig.sl_price
                r_dist = abs(entry_price - sl_price)
                if r_dist <= 0:
                    i += 1
                    continue

                is_long = sig.is_buy
                exit_idx = entry_bar
                realized_r = 0.0

                for b in range(1, MAX_HOLDING_BARS + 1):
                    c_idx = entry_bar + b
                    if c_idx >= n_bars:
                        break
                    high_c = df_oos['high'].iloc[c_idx]
                    low_c = df_oos['low'].iloc[c_idx]
                    close_c = df_oos['close'].iloc[c_idx]

                    if is_long:
                        h_r = (high_c - entry_price) / r_dist
                        if b >= TIME_DECAY_BARS and h_r < TIME_DECAY_THRESHOLD_R:
                            realized_r = (close_c - entry_price) / r_dist
                            exit_idx = c_idx
                            break
                        if h_r >= 2.5:
                            realized_r = 2.5
                            exit_idx = c_idx
                            break
                        if low_c <= sl_price:
                            realized_r = (sl_price - entry_price) / r_dist
                            exit_idx = c_idx
                            break
                    else:
                        h_r = (entry_price - low_c) / r_dist
                        if b >= TIME_DECAY_BARS and h_r < TIME_DECAY_THRESHOLD_R:
                            realized_r = (entry_price - close_c) / r_dist
                            exit_idx = c_idx
                            break
                        if h_r >= 2.5:
                            realized_r = 2.5
                            exit_idx = c_idx
                            break
                        if high_c >= sl_price:
                            realized_r = (entry_price - sl_price) / r_dist
                            exit_idx = c_idx
                            break

                realized_r -= 0.08  # friction
                trades.append({
                    'datetime': df_oos['datetime'].iloc[entry_bar],
                    'asset': sym,
                    'signal': sig.signal,
                    'r_realized': realized_r,
                    'pnl': realized_r * base_risk
                })
                i = exit_idx + 1

            if trades:
                tdf = pd.DataFrame(trades)
                all_trades.append(tdf)
                n = len(tdf)
                wr = float((tdf['r_realized'] > 0).mean() * 100.0)
                tot_r = float(tdf['r_realized'].sum())
                per_asset[sym] = {'trades': n, 'win_rate': wr, 'net_r': tot_r, 'pnl': tot_r * base_risk}
            else:
                per_asset[sym] = {'trades': 0, 'win_rate': 0.0, 'net_r': 0.0, 'pnl': 0.0}

        except Exception as e:
            logging.warning(f"Error backtesting {sym}: {e}")

    if not all_trades:
        return BacktestResult(
            strategy_name=strategy.name,
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

    comb_trades = pd.concat(all_trades).sort_values('datetime').reset_index(drop=True)
    comb_trades['equity'] = initial_cap + comb_trades['pnl'].cumsum()

    tot_trades = len(comb_trades)
    win_rate = float((comb_trades['r_realized'] > 0).mean() * 100.0)
    net_pnl = float(comb_trades['pnl'].sum())
    roi = (net_pnl / initial_cap * 100.0)
    net_r = float(comb_trades['r_realized'].sum())

    peak = comb_trades['equity'].cummax()
    dd = (comb_trades['equity'] - peak) / peak * 100.0
    max_dd = float(dd.min())

    wins = comb_trades.loc[comb_trades['pnl'] > 0, 'pnl'].sum()
    losses = abs(comb_trades.loc[comb_trades['pnl'] < 0, 'pnl'].sum())
    pf = float(wins / losses) if losses > 0 else 99.0

    avg_bh = float(np.mean(b_returns) * 100.0) if b_returns else 0.0

    passed_crit, checks, failures = strategy.config.evaluate_pass_criteria({
        "net_roi_pct": roi, "max_dd_pct": abs(max_dd), "win_rate": win_rate,
        "total_trades": tot_trades, "net_r": net_r
    })

    return BacktestResult(
        strategy_name=strategy.name,
        start_date=start_date,
        end_date=end_date,
        window_id=None,
        total_trades=tot_trades,
        win_rate=win_rate,
        profit_factor=pf,
        net_r=net_r,
        net_pnl_usd=net_pnl,
        net_roi_pct=roi,
        max_dd_pct=max_dd,
        buy_hold_return_pct=avg_bh,
        passed_criteria=passed_crit,
        criteria_checks=checks,
        failure_reasons=failures,
        per_asset_summary=per_asset,
        trades_df=comb_trades
    )


# -------------------------------------------------------------------------
# COMPONENT 7: CENTRAL FOREX ORCHESTRATION ENGINE
# -------------------------------------------------------------------------
class ForexEngine:
    """
    Central orchestration engine for Forex & CFD algorithmic trading.
    Dynamically routes strategies, coordinates MT5 feeds, manages telemetry,
    and executes walk-forward OOS evaluations.
    """
    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig.load()
        self.mt5_conn = MT5Connection()
        self.order_mgr = OrderManager(self.mt5_conn, dry_run=True)
        self.active_strategy: Optional[BaseForexStrategy] = None

    def load_strategy(self, strategy_target: str) -> BaseForexStrategy:
        """Dynamically loads and initializes a strategy from registry or filepath."""
        strat_key = strategy_target.lower()
        if strat_key in StrategyRegistry.list_strategies():
            strat_cls = StrategyRegistry.get(strat_key)
        else:
            path = Path(strategy_target)
            if path.exists() and path.suffix == ".py":
                strat_cls = StrategyRegistry.load_from_module(path)
            else:
                available = ", ".join(StrategyRegistry.list_strategies())
                raise ValueError(f"Strategy '{strategy_target}' not found. Available keys: [{available}]")

        strat_instance = strat_cls(config=self.config)
        strat_instance.initialize(self.config)
        self.active_strategy = strat_instance
        logging.info(f"Loaded and initialized strategy: '{strat_instance.name}' ({strat_instance.description})")
        return strat_instance

    def run_telemetry(
        self,
        strategy_target: str = "fvg_ml",
        once: bool = False,
        ignore_kz: bool = False,
        dry_run: bool = True,
        live: bool = False,
        interval: float = 1.5
    ) -> None:
        """Launches live streaming telemetry for the target strategy."""
        strat = self.load_strategy(strategy_target)
        self.order_mgr.dry_run = (not live)

        console.print(Panel(
            f"[bold cyan]LAUNCHING FOREX MASTER ORCHESTRATION ENGINE[/bold cyan]\n"
            f"[dim]Active Strategy: [bold bright_white]{strat.name.upper()}[/bold bright_white] ({strat.description})\n"
            f"Execution Mode: [{'bold green]LIVE BROKER ORDERS' if live else 'bold yellow]PAPER DRY-RUN'}[/bold][/dim]",
            border_style="cyan"
        ))

        if not self.mt5_conn.connect():
            console.print("[bold red][FATAL] Could not connect to MetaTrader 5 terminal. Ensure MT5 is running![/bold red]")
            sys.exit(1)

        pre_flight_data_sync(self.mt5_conn)

        engines: Dict[str, StatefulInferenceEngine] = {}
        last_candle_times: Dict[str, Optional[datetime]] = {}

        console.print(f"[bold cyan]Warm-starting state buffers for {len(CANONICAL_18_ASSETS)} assets...[/bold cyan]")
        for asset in CANONICAL_18_ASSETS:
            eng = StatefulInferenceEngine(asset)
            if eng.warm_start(self.mt5_conn):
                engines[asset] = eng
                if not eng.buffer.empty:
                    last_candle_times[asset] = eng.buffer.index[-1]

        console.print(f"[bold green]Ready. Streaming live market telemetry...[/bold green]")
        time.sleep(0.5)

        try:
            while True:
                utc_now = datetime.now(timezone.utc)
                last_closed_hour = utc_now.hour
                if last_candle_times:
                    first_k = list(last_candle_times.keys())[0]
                    if last_candle_times[first_k] is not None:
                        last_closed_hour = last_candle_times[first_k].hour

                is_london = (7 <= last_closed_hour <= 10)
                is_ny = (12 <= last_closed_hour <= 15)
                is_kz = True if ignore_kz else (is_london or is_ny)

                latest_closed_ts = max([t for t in last_candle_times.values() if t is not None], default=utc_now)
                self.order_mgr.manage_open_trades(current_bar_time=latest_closed_ts)

                table = Table(
                    title=f"MT5 LIVE TELEMETRY | STRATEGY: {strat.name.upper()} | UTC: {utc_now.strftime('%H:%M:%S')}",
                    box=box.ROUNDED,
                    header_style="bold bright_white on blue",
                    show_lines=False,
                    expand=True
                )
                table.add_column("Asset", justify="left", style="bold white", width=9)
                table.add_column("Bid", justify="right", style="cyan", width=11)
                table.add_column("Ask", justify="right", style="cyan", width=11)
                table.add_column("Spread", justify="right", style="dim", width=9)
                table.add_column("RSI", justify="right", width=7)
                table.add_column("4H Trend", justify="center", width=10)
                table.add_column("FVG", justify="center", width=7)
                table.add_column("P*", justify="right", width=8)
                table.add_column("Decision / Trigger Reason", justify="left", width=25)

                for asset, eng in engines.items():
                    tick = self.mt5_conn.get_last_tick(asset)
                    if tick is None:
                        continue

                    # Refresh on newly closed 15m bar
                    recent_bars = self.mt5_conn.get_15m_bars(asset, count=3)
                    if not recent_bars.empty and len(recent_bars) >= 2:
                        closed_bar = recent_bars.iloc[-2]
                        closed_bar_time = closed_bar['datetime']
                        if last_candle_times.get(asset) is None or closed_bar_time > last_candle_times[asset]:
                            eng.update_bar({
                                'datetime': closed_bar_time,
                                'open': closed_bar['open'],
                                'high': closed_bar['high'],
                                'low': closed_bar['low'],
                                'close': closed_bar['close'],
                                'volume': closed_bar['tick_volume']
                            })
                            eng.refresh_4h_buffer()
                            last_candle_times[asset] = closed_bar_time
                            pre_flight_data_sync(self.mt5_conn, single_asset=asset)

                    # Dynamic strategy signal evaluation
                    sig = strat.generate_signal(asset, eng.buffer, eng.buffer_4h, current_tick=tick)

                    # Indicators for telemetry display
                    features = eng.compute_features().iloc[-1]
                    rsi = features.get('rsi_14', 50.0)
                    trend_val = features.get('htf_4h_trend', 0.0)
                    bull_fvg = features.get('bullish_fvg', 0.0)
                    bear_fvg = features.get('bearish_fvg', 0.0)

                    trend_cell = "[bold green]BULL[/bold green]" if trend_val > 0 else ("[bold red]BEAR[/bold red]" if trend_val < 0 else "[dim]FLAT[/dim]")
                    fvg_cell = "[bold green]BULL[/bold green]" if bull_fvg > 0 else ("[bold red]BEAR[/bold red]" if bear_fvg > 0 else "[dim]NONE[/dim]")
                    rsi_cell = f"[bold red]{rsi:.1f}[/bold red]" if rsi >= 70 else (f"[bold green]{rsi:.1f}[/bold green]" if rsi <= 30 else f"{rsi:.1f}")
                    prob_cell = f"[bold green]{sig.prob:.3f}[/bold green]" if sig.prob >= PROBABILITY_THRESHOLD else f"[dim]{sig.prob:.3f}[/dim]"

                    decision_cell = f"[dim]{sig.reason}[/dim]"
                    if sig.is_active:
                        r_dist = abs(sig.entry_price - sig.sl_price)
                        calc_lots = self.order_mgr.calculate_lot_size(asset, risk_usd=sig.risk_usd, sl_dist=r_dist)
                        action_lbl = f"{'LIVE' if live else 'DRY'}-{'BUY' if sig.is_buy else 'SELL'} ({sig.strategy_tag})"
                        color_style = "bold white on green" if sig.is_buy else "bold white on red"
                        decision_cell = f"[{color_style}] {action_lbl} ({calc_lots:.2f}L) [/{color_style}]"

                        order_type = mt5.ORDER_TYPE_BUY if sig.is_buy else mt5.ORDER_TYPE_SELL
                        self.order_mgr.place_market_order(
                            asset, order_type, volume=calc_lots, sl_price=sig.sl_price,
                            tp_price=sig.tp_price, risk_usd=sig.risk_usd, strategy_tag=sig.strategy_tag
                        )

                    table.add_row(
                        asset, f"{tick.bid:.5f}", f"{tick.ask:.5f}", f"{(tick.ask - tick.bid):.5f}",
                        rsi_cell, trend_cell, fvg_cell, prob_cell, decision_cell
                    )

                console.clear()
                console.print(table)

                if once:
                    break
                time.sleep(interval)

        except KeyboardInterrupt:
            console.print("[yellow]Telemetry stopped by user.[/yellow]")
        finally:
            self.mt5_conn.disconnect()

    async def run_telemetry_async(
        self,
        strategy_target: str = "fvg_ml",
        interval: float = 1.5,
        **kwargs
    ) -> None:
        """Asynchronous execution wrapper for event-loop integration."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: self.run_telemetry(strategy_target, interval=interval, **kwargs))

    def run_forward_test(
        self,
        strategy_target: str = "fvg_ml",
        start_date: str = "2025-12-01",
        end_date: Optional[str] = None
    ) -> BacktestResult:
        """Executes out-of-sample forward test simulation and validates against criteria."""
        strat = self.load_strategy(strategy_target)
        console.print(Panel(
            f"[bold bright_cyan]FORWARD TEST SIMULATION | STRATEGY: {strat.name.upper()}[/bold bright_cyan]\n"
            f"[dim]Start Date: {start_date} | End Date: {end_date or 'Present'} | Assets: {len(CANONICAL_18_ASSETS)}[/dim]",
            border_style="cyan"
        ))

        res = strat.run_backtest(start_date=start_date, end_date=end_date)
        self._display_backtest_report(res)
        return res

    def run_oos_window(self, strategy_target: str, window_id: int) -> BacktestResult:
        """Executes backtest for a specific OOS window from oos_windows_20.json."""
        w = self.config.get_window(window_id)
        if not w:
            raise ValueError(f"Window ID {window_id} not found in {self.config.windows_path}")

        console.print(Panel(
            f"[bold bright_cyan]OOS WINDOW {w.window_id}: {w.name.upper()}[/bold bright_cyan]\n"
            f"[dim]Dates: {w.start_date} to {w.end_date} | Regime: {w.regime}\n"
            f"Description: {w.description}[/dim]",
            border_style="cyan"
        ))

        strat = self.load_strategy(strategy_target)
        res = strat.run_backtest(start_date=w.start_date, end_date=w.end_date)
        res.window_id = window_id
        self._display_backtest_report(res)
        return res

    def run_walkforward(self, strategy_target: str, fail_fast: bool = True) -> List[BacktestResult]:
        """Runs sequential walk-forward evaluation across all 20 OOS windows with fail-fast enforcement."""
        strat = self.load_strategy(strategy_target)
        results = []

        console.print(Panel(
            f"[bold bright_cyan]SEQUENTIAL 20 OOS WINDOW WALK-FORWARD VALIDATION[/bold bright_cyan]\n"
            f"[dim]Strategy: {strat.name.upper()} | Institutional Fail-Fast: {fail_fast}[/dim]",
            border_style="bright_magenta"
        ))

        for w in self.config.windows:
            console.print(f"\n[bold yellow]>>> Evaluating Window {w.window_id}/{len(self.config.windows)}: {w.name} ({w.start_date} to {w.end_date})...[/bold yellow]")
            res = strat.run_backtest(start_date=w.start_date, end_date=w.end_date, save_plot=False)
            res.window_id = w.window_id
            results.append(res)

            status_color = "green" if res.passed_criteria else "red"
            console.print(f"[{status_color}]Result: Net ROI: {res.net_roi_pct:+.2f}% | Max DD: {res.max_dd_pct:.2f}% | Win Rate: {res.win_rate:.1f}% | Trades: {res.total_trades} | Passed: {res.passed_criteria}[/{status_color}]")

            if fail_fast and not res.passed_criteria:
                console.print(f"[bold red]FAIL-FAST HALT: Strategy failed Window {w.window_id} ({w.name}). Halting execution as mandated by Part 10 invariant.[/bold red]")
                break

        return results

    def _display_backtest_report(self, res: BacktestResult) -> None:
        """Renders comprehensive terminal report."""
        table = Table(
            title=f"PER-ASSET METRICS: {res.strategy_name.upper()} ({res.start_date} to {res.end_date or 'Present'})",
            box=box.ROUNDED,
            header_style="bold bright_white on blue"
        )
        table.add_column("Asset", justify="left", style="bold white", width=9)
        table.add_column("Trades", justify="right", width=8)
        table.add_column("Win Rate", justify="right", width=10)
        table.add_column("Net R", justify="right", width=12)
        table.add_column("Net PnL (USD)", justify="right", style="bold", width=15)

        for a, d in sorted(res.per_asset_summary.items(), key=lambda x: x[1]['net_r'], reverse=True):
            pnl_style = "green" if d['pnl'] >= 0 else "red"
            table.add_row(
                a, str(d['trades']), f"{d['win_rate']:.1f}%", f"{d['net_r']:+.2f}R",
                f"[{pnl_style}]${d['pnl']:+,.2f}[/{pnl_style}]"
            )
        console.print(table)

        tc = self.config.criteria
        pass_status = "[bold green]YES (ALL CRITERIA SATISFIED)[/bold green]" if res.passed_criteria else "[bold red]NO (TARGET CRITERIA BREACHED)[/bold red]"

        summary_text = (
            f"Strategy Name:       {res.strategy_name.upper()}\n"
            f"Out-Of-Sample Range: {res.start_date} to {res.end_date or 'Present'}\n"
            f"Initial Capital:     {tc.initial_capital_usd:,.2f} USD\n"
            f"Final Equity:        {tc.initial_capital_usd + res.net_pnl_usd:,.2f} USD\n"
            f"Total Trades:        {res.total_trades} (Min Target: {tc.min_trades})\n"
            f"Win Rate:            {res.win_rate:.1f}% (Min Target: {tc.min_winrate_percent:.1f}%)\n"
            f"Profit Factor:       {res.profit_factor:.2f}\n"
            f"Net R-Multiple:      {res.net_r:+.2f}R (Min Target: {tc.min_r_multiple:+.2f}R)\n"
            f"Net Profit (USD):    {res.net_pnl_usd:+,.2f} USD\n"
            f"Net ROI:             {res.net_roi_pct:+.2f}% (Min Target: {tc.min_roi_percent:+.2f}%)\n"
            f"Max Drawdown:        {res.max_dd_pct:.2f}% (Max Allowed: {tc.max_dd_percent:.2f}%)\n"
            f"Buy & Hold Return:   {res.buy_hold_return_pct:+.2f}%\n"
            f"Criteria Evaluation: {pass_status}"
        )
        if res.failure_reasons:
            summary_text += f"\nFailure Details:     {', '.join(res.failure_reasons)}"

        console.print(Panel(
            summary_text,
            title="[bold bright_cyan]PORTFOLIO PERFORMANCE & CRITERIA SCORECARD[/bold bright_cyan]",
            border_style="green" if res.passed_criteria else "red"
        ))

    def show_info(self) -> None:
        """Displays full architecture diagnostics, loaded criteria, and registered strategies."""
        print("=" * 85)
        print(" FOREX & CFD MASTER ORCHESTRATION ENGINE DIAGNOSTICS")
        print("=" * 85)
        print(f" [Project Root]       : {PROJECT_ROOT}")
        print(f" [Engine Directory]   : {ENGINE_DIR}")
        print(f" [Criteria File]      : {self.config.criteria_path} (Exists: {self.config.criteria_path.exists() if self.config.criteria_path else False})")
        print(f" [Windows File]       : {self.config.windows_path} (Exists: {self.config.windows_path.exists() if self.config.windows_path else False})")
        print(f" [Target Criteria]    : ROI >= {self.config.criteria.min_roi_percent}%, MaxDD <= {self.config.criteria.max_dd_percent}%, WinRate >= {self.config.criteria.min_winrate_percent}%, MinTrades >= {self.config.criteria.min_trades}")
        print(f" [OOS Windows Loaded] : {len(self.config.windows)} regimes (2021 - 2026)")
        print(f" [Registered Strats]  : {StrategyRegistry.list_strategies()}")
        print(f" [Historical Parquets]: {DATA_DIR} ({len(list(DATA_DIR.glob('*.parquet')))} assets)")
        print(f" [Production Model]   : {PRODUCTION_MODEL_PATH} ({'EXISTS' if PRODUCTION_MODEL_PATH.exists() else 'NOT FOUND'})")
        print(f" [Telemetry Log]      : {LOG_FILE}")
        print("=" * 85)


# -------------------------------------------------------------------------
# COMPONENT 8: NUMERICAL PARITY VERIFICATION HARNESS
# -------------------------------------------------------------------------
def run_verify() -> None:
    """Verifies numerical parity between streaming and batch feature calculation."""
    console.print("[bold cyan]Running numerical parity assertions (< 1e-9 error)...[/bold cyan]")
    test_asset = "EURUSD"
    parquet_path = DATA_DIR / f"{test_asset}.parquet"
    if not parquet_path.exists():
        console.print(f"[bold yellow]Test asset {test_asset} parquet not found, using first available...[/bold yellow]")
        parquets = list(DATA_DIR.glob("*.parquet"))
        if not parquets:
            console.print("[bold red]No parquet files found for verification.[/bold red]")
            return
        parquet_path = parquets[0]
        test_asset = parquet_path.stem

    df = pl.read_parquet(parquet_path).tail(250).to_pandas()
    df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
    df.set_index('datetime', inplace=True)

    batch_feat = compute_features_pandas(df)

    eng = StatefulInferenceEngine(test_asset)
    eng.buffer = df.copy()
    stream_feat = eng.compute_features()

    diff = (batch_feat.iloc[-1] - stream_feat.iloc[-1]).abs().max()
    if diff < 1e-9:
        console.print(f"[bold green]PASS: Feature parity verified! Max difference: {diff:.2e}[/bold green]")
    else:
        console.print(f"[bold red]FAIL: Feature mismatch detected! Max difference: {diff:.2e}[/bold red]")


# -------------------------------------------------------------------------
# CLI ENTRYPOINT
# -------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Unified Master Forex & CFD Orchestration Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Standard Execution Examples:
  # 1. Run Live/Dry-Run Streaming Telemetry with FVG_ML strategy
  python Engine/forex_engine.py --strategy fvg_ml

  # 2. Run Single-Pass Snapshot of all 18 assets
  python Engine/forex_engine.py --mode snapshot --strategy fvg_ml

  # 3. Run Forward-Test Backtest from Dec 2025 onwards (Validating against Target Criteria)
  python Engine/forex_engine.py --mode forward-test --strategy fvg_ml --start-date 2025-12-01

  # 4. Run Specific Out-Of-Sample Regime Window (Window 20: March 2026 Microstructure Shock)
  python Engine/forex_engine.py --mode oos-window --strategy fvg_ml --window 20

  # 5. Run Full 20 OOS Window Walk-Forward with Institutional Fail-Fast Gate
  python Engine/forex_engine.py --mode walkforward --strategy fvg_ml

  # 6. Run System Diagnostics & Storage Inspection
  python Engine/forex_engine.py --mode info

  # 7. Arm Real Live Broker Orders to MetaTrader 5
  python Engine/forex_engine.py --strategy fvg_ml --live
        """
    )
    parser.add_argument(
        "--mode",
        choices=["telemetry", "dry-run", "snapshot", "forward-test", "oos-window", "walkforward", "train", "verify", "info"],
        default="telemetry",
        help="Execution mode (default: telemetry)"
    )
    parser.add_argument(
        "--strategy",
        default="fvg_ml",
        help="Trading strategy: 'fvg_ml' (Canonical FVG + XGBoost), 'combined', 'fvg', 'crt', 'ml', or path to .py file (default: fvg_ml)"
    )
    parser.add_argument(
        "--start-date",
        default="2025-12-01",
        help="Out-of-sample forward test start date (default: 2025-12-01)"
    )
    parser.add_argument(
        "--end-date",
        default=None,
        help="Out-of-sample forward test end date (optional)"
    )
    parser.add_argument(
        "--window",
        type=int,
        default=20,
        help="Window ID (1 to 20) for --mode oos-window (default: 20)"
    )
    parser.add_argument(
        "--criteria",
        type=str,
        default=str(CRITERIA_PATH),
        help="Path to criteria JSON file (default: Engine/target_oos_criteria.json)"
    )
    parser.add_argument(
        "--windows",
        type=str,
        default=str(WINDOWS_PATH),
        help="Path to 20 OOS windows JSON file (default: Engine/oos_windows_20.json)"
    )
    parser.add_argument(
        "--live",
        dest="live",
        action="store_true",
        default=False,
        help="ARM LIVE TRADING: Send actual orders to MetaTrader 5 (Real capital risk)"
    )
    parser.add_argument(
        "--skip-train",
        action="store_true",
        help="Skip retraining; run immediately with existing model weights."
    )
    parser.add_argument(
        "--ignore-kz",
        action="store_true",
        help="Bypass the London/NY kill zone filter for 24/7 signal testing."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.5,
        help="Telemetry refresh interval in seconds (default: 1.5)"
    )

    args = parser.parse_args()

    # Ingest Config & Criteria
    engine_config = EngineConfig.load(criteria_path=args.criteria, windows_path=args.windows)
    engine = ForexEngine(config=engine_config)

    if args.mode == "info":
        engine.show_info()
        return

    if args.mode == "verify":
        run_verify()
        return

    if args.mode == "train":
        dynamic_retrain()
        return

    if args.mode == "forward-test":
        engine.run_forward_test(strategy_target=args.strategy, start_date=args.start_date, end_date=args.end_date)
        return

    if args.mode == "oos-window":
        engine.run_oos_window(strategy_target=args.strategy, window_id=args.window)
        return

    if args.mode == "walkforward":
        engine.run_walkforward(strategy_target=args.strategy, fail_fast=True)
        return

    # Retrain if model missing and not skipped
    if not args.skip_train and not PRODUCTION_MODEL_PATH.exists():
        dynamic_retrain()

    is_once = (args.mode == "snapshot")
    engine.run_telemetry(
        strategy_target=args.strategy,
        once=is_once,
        ignore_kz=args.ignore_kz,
        dry_run=(not args.live),
        live=args.live,
        interval=args.interval
    )


if __name__ == "__main__":
    main()
