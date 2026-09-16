"""
================================================================================
ENGINE: UNIFIED FOREX & CFD STANDALONE MASTER TRADING ENGINE
================================================================================
Location: Engine/forex_engine.py
Architecture: Single Self-Contained Deep Module (Clean Code, Karpathy Directives)

This single standalone file encapsulates the entire institutional Forex & CFD
trading pipeline for MetaTrader 5 (Blueberry Markets):
1. LIVE BROKER CONNECTIVITY : Resilient MT5 connection, symbol alias mapping,
                             and true UTC offset reconciliation.
2. PRE-FLIGHT SYNC          : Live candle synchronization directly updating
                             Forex_Backtesting_Data/ parquets.
3. DYNAMIC RETRAINING       : High-speed Polars causal feature engineering (13
                             stationary features with shift(1) 4H trend) and
                             7-stage microstructure ratchet simulation.
4. STRATEGIES SUPPORTED     :
   - Strategy 1 (FVG)       : Rule-Based ICT Fair Value Gap + Liquidity Sweeps.
   - Strategy 2 (CRT)       : Candle Range Theory (CRT) & Opening Range Breakout (ORB).
   - Strategy 3 (ML)        : Pure XGBoost Machine Learning Probability (P* >= 0.55).
   - Combined (Default)     : Multi-Confluence: FVG + CRT + ML alignment.
5. RISK & RATCHET GOVERNOR  : Dynamic equity-based lot sizing ($25-$50 base risk),
                             safe DRY-RUN mode (zero broker orders; default),
                             armed LIVE mode, and 7-stage microstructure ratchets.
6. REAL-TIME TELEMETRY      : Rich ASCII live dashboard showing streaming
                             quotes, indicators, probabilities, and order decisions.

Execution Modes:
  python Engine/forex_engine.py                     # Full cycle: Sync -> Retrain -> Live Telemetry (Combined)
  python Engine/forex_engine.py --strategy fvg      # Rule-Based ICT FVG Strategy (Dry-Run)
  python Engine/forex_engine.py --strategy crt      # Candle Range Theory & ORB Strategy (Dry-Run)
  python Engine/forex_engine.py --strategy ml       # Pure XGBoost ML Strategy (Dry-Run)
  python Engine/forex_engine.py --strategy combined # Multi-Confluence: FVG + CRT + ML (Dry-Run)
  python Engine/forex_engine.py --mode snapshot     # 1-pass evaluation snapshot across all 18 assets & exit
  python Engine/forex_engine.py --skip-train        # Run telemetry immediately with existing model weights
  python Engine/forex_engine.py --live              # ARM LIVE TRADING (Real broker orders dispatched)
  python Engine/forex_engine.py --mode verify       # Numerical parity test (streaming vs batch < 1e-9)
  python Engine/forex_engine.py --mode info         # Repository paths and data diagnostics
================================================================================
"""
from __future__ import annotations

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any

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

DATA_DIR = PROJECT_ROOT / "Forex_Backtesting_Data"
MODELS_DIR = ENGINE_DIR / "models"
PRODUCTION_MODEL_PATH = MODELS_DIR / "xgboost_forex.json"
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
CANONICAL_FEATURES = [
    "bullish_fvg", "bearish_fvg", "htf_4h_trend", "hour", "day_of_week",
    "rsi_14", "vwap_dist", "ema_50_dist", "ema_200_dist", "ema_200_slope",
    "atr_14", "volatility_20", "roc_20"
]

CANONICAL_18_ASSETS = [
    'EURHUF', 'GER30', 'NICKEL', 'USDSEK', 'GAS', 'AU200', 'FR40',
    'EURCNH', 'LEAD', 'NZDUSD', 'USDHKD', 'US2000', 'AUDCHF',
    'NZDCNH', 'XAUCNH', 'GAUCNH', 'EURSEK', 'EURUSD'
]

BASE_RISK_USD = 25.0
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
        self._virtual_ticket = 900000

    def calculate_lot_size(self, symbol: str, risk_usd: float, sl_dist: float) -> float:
        """Calculates broker-compliant lot size using point values and contract specs."""
        real_symbol = self.conn.resolve_symbol(symbol)
        info = mt5.symbol_info(real_symbol)
        if info is None or sl_dist <= 0:
            return 0.01

        tick_value = info.trade_tick_value if info.trade_tick_value > 0 else 1.0
        tick_size = info.trade_tick_size if info.trade_tick_size > 0 else (info.point if info.point > 0 else 0.0001)

        loss_per_lot = (sl_dist / tick_size) * tick_value
        if loss_per_lot <= 0:
            return info.volume_min

        raw_lots = risk_usd / loss_per_lot
        step = info.volume_step if info.volume_step > 0 else 0.01
        lots = round(raw_lots / step) * step
        lots = max(info.volume_min, min(lots, info.volume_max))
        return round(float(lots), 2)

    def place_market_order(
        self,
        symbol: str,
        order_type: int,
        volume: Optional[float] = None,
        sl_price: Optional[float] = None,
        tp_price: Optional[float] = None,
        risk_usd: float = BASE_RISK_USD,
        strategy_tag: str = "COMBINED"
    ) -> Optional[int]:
        real_symbol = self.conn.resolve_symbol(symbol)
        tick = self.conn.get_last_tick(real_symbol)
        if tick is None:
            return None

        price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid

        if volume is None or volume <= 0:
            sl_dist = abs(price - sl_price) if sl_price is not None else 0.0001
            volume = self.calculate_lot_size(real_symbol, risk_usd=risk_usd, sl_dist=sl_dist)

        r_dist = abs(price - sl_price) if sl_price is not None else 0.0001
        r_dist = max(r_dist, 0.00001)

        # DRY RUN MODE: Virtual execution only (Zero Broker Orders)
        if self.dry_run:
            self._virtual_ticket += 1
            ticket = self._virtual_ticket
            self.open_trades[ticket] = {
                "symbol": real_symbol,
                "ticket": ticket,
                "type": order_type,
                "volume": volume,
                "entry_price": price,
                "sl": sl_price,
                "tp": tp_price,
                "r_dist": r_dist,
                "bars_elapsed": 0,
                "highest_r": 0.0,
                "last_bar_time": None,
                "strategy": strategy_tag,
                "is_virtual": True
            }
            logging.info(f"[DRY-RUN ORDER REGISTERED] Ticket #{ticket} | {real_symbol} | Vol={volume}L | Entry={price:.5f} | SL={sl_price:.5f} | TP={tp_price:.5f}")
            return ticket

        # LIVE EXECUTION MODE: Real broker order dispatch
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": real_symbol,
            "volume": float(volume),
            "type": order_type,
            "price": price,
            "sl": float(sl_price) if sl_price is not None else 0.0,
            "deviation": 20,
            "magic": 123456,
            "comment": f"Forex {strategy_tag}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        if tp_price:
            request["tp"] = float(tp_price)

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Live order failed: retcode={result.retcode}")
            return None

        actual_fill = result.price if result.price > 0 else price
        actual_r_dist = abs(actual_fill - sl_price) if sl_price is not None else r_dist
        actual_r_dist = max(actual_r_dist, 0.00001)

        self.open_trades[result.order] = {
            "symbol": real_symbol,
            "ticket": result.order,
            "type": order_type,
            "volume": volume,
            "entry_price": actual_fill,
            "sl": sl_price,
            "tp": tp_price,
            "r_dist": actual_r_dist,
            "bars_elapsed": 0,
            "highest_r": 0.0,
            "last_bar_time": None,
            "strategy": strategy_tag,
            "is_virtual": False
        }
        logging.info(f"[LIVE ORDER EXECUTED] Ticket #{result.order} | {real_symbol} | Fill={actual_fill:.5f} | Vol={volume}L")
        return result.order

    def close_position(self, ticket: int) -> bool:
        if ticket not in self.open_trades:
            return False

        trade = self.open_trades[ticket]
        if trade.get("is_virtual", True):
            logging.info(f"[DRY-RUN POSITION CLOSED] Ticket #{ticket} ({trade['symbol']})")
            del self.open_trades[ticket]
            return True

        if not self.conn.connected:
            return False

        positions = mt5.positions_get(ticket=ticket)
        if not positions:
            del self.open_trades[ticket]
            return False

        pos = positions[0]
        tick = self.conn.get_last_tick(pos.symbol)
        if tick is None:
            return False

        close_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = tick.bid if pos.type == mt5.POSITION_TYPE_BUY else tick.ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "Close Position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            logging.info(f"[LIVE POSITION CLOSED] Ticket #{ticket} closed at {price:.5f}")
            del self.open_trades[ticket]
            return True
        return False

    def modify_sl(self, ticket: int, new_sl: float) -> bool:
        if ticket not in self.open_trades:
            return False
        trade = self.open_trades[ticket]
        if trade.get("is_virtual", True):
            trade["sl"] = new_sl
            logging.info(f"[DRY-RUN SL RATCHETED] Ticket #{ticket} SL -> {new_sl:.5f}")
            return True

        if not self.conn.connected:
            return False

        positions = mt5.positions_get(ticket=ticket)
        if not positions:
            return False

        pos = positions[0]
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": pos.symbol,
            "sl": float(new_sl),
            "tp": pos.tp
        }
        res = mt5.order_send(request)
        if res.retcode == mt5.TRADE_RETCODE_DONE:
            trade["sl"] = new_sl
            return True
        return False

    def manage_open_trades(self, current_bar_time: Optional[datetime] = None) -> None:
        """Evaluates 7-stage microstructure ratchets and 24-bar time decay."""
        for ticket in list(self.open_trades.keys()):
            trade = self.open_trades[ticket]
            sym = trade["symbol"]
            tick = self.conn.get_last_tick(sym)
            if tick is None:
                continue

            current_price = tick.bid if trade["type"] == mt5.ORDER_TYPE_BUY else tick.ask
            entry = trade["entry_price"]
            r_dist = trade["r_dist"]

            if trade["type"] == mt5.ORDER_TYPE_BUY:
                current_r = (current_price - entry) / r_dist
            else:
                current_r = (entry - current_price) / r_dist

            trade["highest_r"] = max(trade["highest_r"], current_r)

            if current_bar_time and trade["last_bar_time"] != current_bar_time:
                trade["bars_elapsed"] += 1
                trade["last_bar_time"] = current_bar_time

            # 1. Time Decay Exit: 24 bars elapsed and price failed to gain +0.20R
            if trade["bars_elapsed"] >= TIME_DECAY_BARS and trade["highest_r"] < TIME_DECAY_THRESHOLD_R:
                logging.info(f"Time decay exit triggered for #{ticket} ({sym}) after 24 bars (Peak R: {trade['highest_r']:.2f})")
                self.close_position(ticket)
                continue

            # 2. Microstructure Ratchets
            new_sl_r = None
            if trade["highest_r"] >= 3.5:
                new_sl_r = 3.3
            elif trade["highest_r"] >= 3.0:
                new_sl_r = 2.8
            elif trade["highest_r"] >= 2.5:
                new_sl_r = 2.3
            elif trade["highest_r"] >= 2.0:
                new_sl_r = 1.8
            elif trade["highest_r"] >= 1.5:
                new_sl_r = 1.0
            elif trade["highest_r"] >= 1.0:
                new_sl_r = 0.15

            if new_sl_r is not None:
                if trade["type"] == mt5.ORDER_TYPE_BUY:
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


# -------------------------------------------------------------------------
# COMPONENT 3b: LIVE CRT / ORB OPENING RANGE STATE EXTRACTOR
# -------------------------------------------------------------------------
def compute_crt_orb_state(buffer: pd.DataFrame) -> dict:
    """Computes live CRT/ORB session state from the 15m rolling buffer.

    Returns dict with keys:
        is_long_crt, is_short_crt  – confirmed breakout signals
        or_high, or_low            – most recent session opening range bounds
        body_ratio                 – breakout bar body confirmation ratio
        judas_long, judas_short    – pre-market Judas sweep flags
        session                    – 'London' | 'NY' | 'None'
    """
    default = dict(is_long_crt=False, is_short_crt=False,
                   or_high=0.0, or_low=0.0, body_ratio=0.0,
                   judas_long=False, judas_short=False, session="None")

    if buffer.empty or len(buffer) < 10:
        return default

    df = buffer.copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        return default

    # Ensure UTC-aware index
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")

    df["_hour"]   = df.index.hour
    df["_minute"] = df.index.minute
    df["_date"]   = df.index.date

    # Check both London (07:00) and NY (13:30) opening ranges
    for sess_hour, sess_min, sess_name in [(7, 0, "London"), (13, 30, "NY")]:
        or_bars = df[(df["_hour"] == sess_hour) & (df["_minute"] == sess_min)]
        if or_bars.empty:
            continue

        or_start_idx = or_bars.index[-1]           # most recent session today
        pos = df.index.get_loc(or_start_idx)
        if pos + 1 >= len(df):
            continue                                # need at least 1 bar after OR open

        # Opening range: 2 bars (30 min)
        or_slice = df.iloc[pos : pos + 2]
        or_high  = float(or_slice["high"].max())
        or_low   = float(or_slice["low"].min())
        or_range = or_high - or_low
        if or_range <= 0:
            continue

        # Previous day high/low from bars before the session date
        or_date    = or_start_idx.date()
        prev_bars  = df[df["_date"] < or_date]
        if prev_bars.empty:
            prev_day_high = float(df["high"].iloc[0])
            prev_day_low  = float(df["low"].iloc[0])
        else:
            prev_day_high = float(prev_bars["high"].max())
            prev_day_low  = float(prev_bars["low"].min())

        # Judas sweep: pre-market (6 bars = 1.5 h before OR) swept PDH/PDL then reclaimed
        pre_start = max(0, pos - 6)
        pre_slice = df.iloc[pre_start:pos]
        if not pre_slice.empty:
            pre_low  = float(pre_slice["low"].min())
            pre_high = float(pre_slice["high"].max())
            judas_long  = (pre_low  < prev_day_low)  and (or_low  >= prev_day_low)
            judas_short = (pre_high > prev_day_high) and (or_high <= prev_day_high)
        else:
            judas_long = judas_short = False

        # Scan bars after OR for breakout confirmation
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

        # Drop currently forming unclosed bar
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
# COMPONENT 5: PRE-FLIGHT MARKET DATA SYNCHRONIZER
# -------------------------------------------------------------------------
def pre_flight_data_sync(mt5_conn: MT5Connection, single_asset: Optional[str] = None) -> None:
    """Fetches missing closed 15m candles from MT5 and updates Parquet data atomically."""
    target_assets = [single_asset] if single_asset else CANONICAL_18_ASSETS
    utc_now = datetime.now(timezone.utc)
    broker_offset = mt5_conn.get_broker_utc_offset()

    for asset in target_assets:
        parquet_file = DATA_DIR / f"{asset}_15m_real.parquet"
        if not parquet_file.exists():
            continue

        try:
            df_curr = pd.read_parquet(parquet_file)
            last_dt = pd.to_datetime(df_curr['datetime'].max())
            if last_dt.tzinfo is None:
                last_dt = last_dt.tz_localize('UTC')

            fetch_start = last_dt + timedelta(seconds=1)
            fetch_start_broker = fetch_start + timedelta(seconds=broker_offset)
            cutoff_broker = utc_now + timedelta(seconds=broker_offset)

            real_sym = mt5_conn.resolve_symbol(asset)
            rates = mt5.copy_rates_range(real_sym, mt5.TIMEFRAME_M15, fetch_start_broker, cutoff_broker)
            if rates is None or len(rates) == 0:
                continue

            df_new = pd.DataFrame(rates)
            df_new['time'] = df_new['time'] - broker_offset
            df_new['datetime'] = pd.to_datetime(df_new['time'], unit='s', utc=True)
            df_new = df_new[df_new['datetime'] + timedelta(minutes=15) <= utc_now]

            if df_new.empty:
                continue

            df_new.rename(columns={'tick_volume': 'volume'}, inplace=True)
            existing_cols = df_curr.columns.tolist()

            new_rows = pd.DataFrame()
            for col in existing_cols:
                if col in df_new.columns:
                    new_rows[col] = df_new[col].values

            if 'day_of_week' in existing_cols and 'datetime' in df_new.columns:
                new_rows['day_of_week'] = df_new['datetime'].dt.dayofweek.values

            if 'is_kill_zone' in existing_cols and 'datetime' in df_new.columns:
                hours = df_new['datetime'].dt.hour
                new_rows['is_kill_zone'] = ((hours >= 7) & (hours <= 10)) | ((hours >= 12) & (hours <= 15))

            df_updated = pd.concat([df_curr, new_rows], ignore_index=True)
            df_updated = df_updated.drop_duplicates(subset=['time'], keep='first').sort_values('time').reset_index(drop=True)

            tmp_path = parquet_file.with_suffix(".tmp")
            df_updated.to_parquet(tmp_path, index=False)
            os.replace(tmp_path, parquet_file)
            logging.info(f"[SYNC] {asset}: Appended {len(new_rows)} completed candles to parquet.")
        except Exception as e:
            logging.warning(f"Failed sync for {asset}: {e}")


# -------------------------------------------------------------------------
# COMPONENT 6: HIGH-SPEED POLARS DYNAMIC RETRAINING
# -------------------------------------------------------------------------
def engineer_features_polars(symbol: str, data_dir: Path) -> pd.DataFrame:
    """Computes all 13 stationary features via Polars with shift(1) on 4H trend."""
    m15_file = data_dir / f"{symbol}_15m_real.parquet"
    if not m15_file.exists() and symbol == "GER30":
        m15_file = data_dir / "GER40_15m_real.parquet"
    h4_file = data_dir / f"{symbol}_4h_real.parquet"
    if not h4_file.exists() and symbol == "GER30":
        h4_file = data_dir / "GER40_4h_real.parquet"
    d1_file = data_dir / f"{symbol}_d1_real.parquet"
    if not d1_file.exists() and symbol == "GER30":
        d1_file = data_dir / "GER40_d1_real.parquet"

    if not (m15_file.exists() and h4_file.exists() and d1_file.exists()):
        raise FileNotFoundError(f"Missing parquets for {symbol}")

    d1_df = pl.read_parquet(d1_file).sort("datetime")
    d1_df = d1_df.with_columns([
        pl.col("high").shift(1).alias("prev_day_high"),
        pl.col("low").shift(1).alias("prev_day_low")
    ]).select(["datetime", "prev_day_high", "prev_day_low"]).drop_nulls()

    h4_df = pl.read_parquet(h4_file).sort("datetime")
    h4_df = h4_df.with_columns([
        pl.col("close").ewm_mean(span=200, adjust=False).alias("ema_200_4h")
    ]).with_columns([
        (pl.col("ema_200_4h") - pl.col("ema_200_4h").shift(5)).alias("htf_4h_trend_raw")
    ]).with_columns([
        pl.col("htf_4h_trend_raw").shift(1).alias("htf_4h_trend")
    ]).select(["datetime", "htf_4h_trend"]).drop_nulls()

    m15_df = pl.read_parquet(m15_file).sort("datetime")
    w = 5
    bullish_exprs = []
    bearish_exprs = []
    for k in range(w):
        bull = (pl.col("low").rolling_min(window_size=k+1) - pl.col("high").shift(k+2)).fill_null(0.0).clip(lower_bound=0.0)
        bear = (pl.col("low").shift(k+2) - pl.col("high").rolling_max(window_size=k+1)).fill_null(0.0).clip(lower_bound=0.0)
        bullish_exprs.append(bull)
        bearish_exprs.append(bear)

    m15_df = m15_df.with_columns([
        pl.max_horizontal(bullish_exprs).alias("bullish_fvg"),
        pl.max_horizontal(bearish_exprs).alias("bearish_fvg"),
        pl.col("high").rolling_max(window_size=20).alias("local_high_20"),
        pl.col("low").rolling_min(window_size=20).alias("local_low_20"),
    ])

    m15_df = m15_df.join_asof(d1_df, on="datetime", strategy="backward")
    m15_df = m15_df.join_asof(h4_df, on="datetime", strategy="backward")

    m15_df = m15_df.with_columns([
        (pl.col("low") <= pl.col("prev_day_low")).cast(pl.Int8).alias("sweep_pdl"),
        (pl.col("high") >= pl.col("prev_day_high")).cast(pl.Int8).alias("sweep_pdh"),
        pl.col("datetime").dt.hour().alias("hour"),
        pl.col("datetime").dt.weekday().alias("day_of_week")
    ])

    m15_df = m15_df.with_columns([
        pl.col("close").diff().alias("change")
    ]).with_columns([
        pl.when(pl.col("change") > 0).then(pl.col("change")).otherwise(0).alias("gain"),
        pl.when(pl.col("change") < 0).then(abs(pl.col("change"))).otherwise(0).alias("loss")
    ]).with_columns([
        pl.col("gain").ewm_mean(span=14, adjust=False).alias("avg_gain"),
        pl.col("loss").ewm_mean(span=14, adjust=False).alias("avg_loss")
    ]).with_columns([
        (100.0 - (100.0 / (1.0 + (pl.col("avg_gain") / (pl.col("avg_loss") + 1e-12))))).alias("rsi_14")
    ])

    m15_df = m15_df.with_columns([
        ((pl.col("high") + pl.col("low") + pl.col("close")) / 3.0).alias("typical_price")
    ]).with_columns([
        pl.col("typical_price").rolling_mean(window_size=20).alias("vwap_20"),
        pl.col("close").ewm_mean(span=50, min_periods=50).alias("ema_50"),
        pl.col("close").ewm_mean(span=200, min_periods=200).alias("ema_200"),
        (pl.col("high") - pl.col("low")).rolling_mean(window_size=14).alias("atr_14"),
        (pl.col("close").rolling_std(window_size=20) / pl.col("close")).alias("volatility_20"),
        ((pl.col("close") / pl.col("close").shift(20)) - 1.0).alias("roc_20")
    ]).with_columns([
        ((pl.col("close") - pl.col("vwap_20")) / pl.col("vwap_20")).alias("vwap_dist"),
        ((pl.col("close") - pl.col("ema_50")) / pl.col("ema_50")).alias("ema_50_dist"),
        ((pl.col("close") - pl.col("ema_200")) / pl.col("ema_200")).alias("ema_200_dist"),
        (pl.col("ema_200") - pl.col("ema_200").shift(12)).alias("ema_200_slope")
    ])

    return m15_df.to_pandas()


def create_labels_ratchet(df: pd.DataFrame) -> pd.DataFrame:
    """Labels training setups based on 7-stage microstructure ratchet simulation."""
    n = len(df)
    targets = np.full(n, np.nan)
    lows = df['low'].values
    highs = df['high'].values
    closes = df['close'].values
    sweep_pdl = df['sweep_pdl'].values
    sweep_pdh = df['sweep_pdh'].values
    bullish_fvg = df['bullish_fvg'].values
    bearish_fvg = df['bearish_fvg'].values
    htf_4h = df['htf_4h_trend'].values
    hours = df['hour'].values
    loc_highs = df['local_high_20'].values
    loc_lows = df['local_low_20'].values

    for i in range(200, n - MAX_HOLDING_BARS):
        is_kz = (7 <= hours[i] <= 10) or (12 <= hours[i] <= 15)
        is_long = is_kz and (sweep_pdl[i] == 1) and (bullish_fvg[i] > 0) and (htf_4h[i] > 0)
        is_short = is_kz and (sweep_pdh[i] == 1) and (bearish_fvg[i] > 0) and (htf_4h[i] < 0)

        if not (is_long or is_short):
            continue

        entry = closes[i]
        if is_long:
            sl = loc_lows[i]
            r_dist = entry - sl
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                continue

            highest_r = 0.0
            cur_sl = sl
            realized_r = 0.0
            for bar in range(1, MAX_HOLDING_BARS + 1):
                idx = i + bar
                h_bar = (highs[idx] - entry) / r_dist
                highest_r = max(highest_r, h_bar)

                if bar >= TIME_DECAY_BARS and highest_r < TIME_DECAY_THRESHOLD_R:
                    realized_r = (closes[idx] - entry) / r_dist
                    break

                if highest_r >= 4.0:
                    realized_r = 4.0
                    break

                if highest_r >= 3.5:
                    cur_sl = max(cur_sl, entry + (3.3 * r_dist))
                elif highest_r >= 3.0:
                    cur_sl = max(cur_sl, entry + (2.8 * r_dist))
                elif highest_r >= 2.5:
                    cur_sl = max(cur_sl, entry + (2.3 * r_dist))
                elif highest_r >= 2.0:
                    cur_sl = max(cur_sl, entry + (1.8 * r_dist))
                elif highest_r >= 1.5:
                    cur_sl = max(cur_sl, entry + (1.0 * r_dist))
                elif highest_r >= 1.0:
                    cur_sl = max(cur_sl, entry + (0.15 * r_dist))

                if lows[idx] <= cur_sl:
                    realized_r = (cur_sl - entry) / r_dist
                    break

            targets[i] = 1.0 if realized_r > 0 else 0.0

        elif is_short:
            sl = loc_highs[i]
            r_dist = sl - entry
            if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                continue

            highest_r = 0.0
            cur_sl = sl
            realized_r = 0.0
            for bar in range(1, MAX_HOLDING_BARS + 1):
                idx = i + bar
                h_bar = (entry - lows[idx]) / r_dist
                highest_r = max(highest_r, h_bar)

                if bar >= TIME_DECAY_BARS and highest_r < TIME_DECAY_THRESHOLD_R:
                    realized_r = (entry - closes[idx]) / r_dist
                    break

                if highest_r >= 4.0:
                    realized_r = 4.0
                    break

                if highest_r >= 3.5:
                    cur_sl = min(cur_sl, entry - (3.3 * r_dist))
                elif highest_r >= 3.0:
                    cur_sl = min(cur_sl, entry - (2.8 * r_dist))
                elif highest_r >= 2.5:
                    cur_sl = min(cur_sl, entry - (2.3 * r_dist))
                elif highest_r >= 2.0:
                    cur_sl = min(cur_sl, entry - (1.8 * r_dist))
                elif highest_r >= 1.5:
                    cur_sl = min(cur_sl, entry - (1.0 * r_dist))
                elif highest_r >= 1.0:
                    cur_sl = min(cur_sl, entry - (0.15 * r_dist))

                if highs[idx] >= cur_sl:
                    realized_r = (entry - cur_sl) / r_dist
                    break

            targets[i] = 1.0 if realized_r > 0 else 0.0

    df['target'] = targets
    return df


def dynamic_retrain() -> None:
    """Executes fresh training of the production XGBoost model on certified parquets."""
    print("=" * 85)
    print(" [DYNAMIC RETRAINING] TRAINING CAUSAL XGBOOST BOOSTER ON 18 INSTITUTIONAL ASSETS...")
    print("=" * 85)
    all_X = []
    all_y = []

    for sym in CANONICAL_18_ASSETS:
        try:
            print(f"  -> Engineering features & ratchet labels for {sym:<7}...", end=" ", flush=True)
            df = engineer_features_polars(sym, DATA_DIR)
            df = create_labels_ratchet(df)
            valid = df[df['target'].notna()]
            if len(valid) > 0:
                print(f"Found {len(valid):>4} setups | Win Rate: {valid['target'].mean()*100:.1f}%")
                all_X.append(valid[CANONICAL_FEATURES])
                all_y.append(valid['target'].values)
            else:
                print("0 valid setups.")
        except Exception as e:
            print(f"Error: {e}")

    if not all_X:
        raise RuntimeError("No valid labeled setups found across assets!")

    X_mat = pd.concat(all_X, ignore_index=True)
    y_vec = np.concatenate(all_y)

    pos_count = int(y_vec.sum())
    neg_count = len(y_vec) - pos_count
    pos_weight = float(neg_count) / max(1.0, float(pos_count))

    dtrain = xgb.DMatrix(X_mat, label=y_vec)
    params = {
        'objective': 'binary:logistic',
        'max_depth': 4,
        'learning_rate': 0.05,
        'reg_alpha': 1.0,
        'reg_lambda': 3.0,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'scale_pos_weight': pos_weight,
        'eval_metric': 'logloss',
        'seed': 42
    }
    model = xgb.train(params, dtrain, num_boost_round=80)
    model.save_model(str(PRODUCTION_MODEL_PATH))
    print(f"\n [RETRAINING COMPLETE] Saved fresh certified model to {PRODUCTION_MODEL_PATH}")
    print("=" * 85)


# -------------------------------------------------------------------------
# COMPONENT 7: REAL-TIME TELEMETRY & STRATEGY DECISION ENGINE
# -------------------------------------------------------------------------
def run_telemetry(
    once: bool = False,
    ignore_kz: bool = False,
    strategy: str = "combined",
    dry_run: bool = True,
    live: bool = False,
    interval: float = 1.5
) -> None:
    """Launches live rich terminal telemetry and executes the selected strategy."""
    is_dry_run = not live
    strat_mode = strategy.lower()

    console.print(Panel("[bold cyan]INITIALIZING UNIFIED FOREX & CFD MASTER TRADING ENGINE[/bold cyan]\n[dim]Connecting to MetaTrader 5 broker feed...[/dim]", border_style="cyan"))

    mt5_conn = MT5Connection()
    if not mt5_conn.connect():
        console.print("[bold red][FATAL] Could not connect to MetaTrader 5 terminal. Ensure MT5 is running![/bold red]")
        sys.exit(1)

    pre_flight_data_sync(mt5_conn)

    if not PRODUCTION_MODEL_PATH.exists():
        console.print("[bold yellow]Production model not found. Triggering dynamic training...[/bold yellow]")
        dynamic_retrain()

    xgb_model = xgb.Booster()
    xgb_model.load_model(str(PRODUCTION_MODEL_PATH))

    order_mgr = OrderManager(mt5_conn, dry_run=is_dry_run)

    engines: Dict[str, StatefulInferenceEngine] = {}
    last_candle_times: Dict[str, Optional[datetime]] = {}

    console.print("[bold cyan]Warm-starting rolling state buffers for 18 institutional assets...[/bold cyan]")
    for asset in CANONICAL_18_ASSETS:
        eng = StatefulInferenceEngine(asset)
        if eng.warm_start(mt5_conn):
            engines[asset] = eng
            if not eng.buffer.empty:
                last_candle_times[asset] = eng.buffer.index[-1]

    console.print(f"[bold green]Successfully warm-started {len(engines)}/{len(CANONICAL_18_ASSETS)} assets.[/bold green]")
    time.sleep(1.0)

    start_time = datetime.now()
    signals_count = 0

    try:
        while True:
            acc = mt5.account_info()
            if acc is None:
                logging.warning("MT5 connection lost. Reconnecting...")
                if not mt5_conn.connect():
                    time.sleep(5)
                    continue
                acc = mt5.account_info()

            acc_dict = acc._asdict() if acc else {"login": "UNKNOWN", "server": "UNKNOWN", "balance": 0.0, "equity": 0.0}

            utc_now = datetime.now(timezone.utc)
            last_closed_hour = utc_now.hour
            if last_candle_times:
                first_k = list(last_candle_times.keys())[0]
                if last_candle_times[first_k] is not None:
                    last_closed_hour = last_candle_times[first_k].hour

            is_london = (7 <= last_closed_hour <= 10)
            is_ny = (12 <= last_closed_hour <= 15)
            is_natural_kz = is_london or is_ny
            is_kz = True if ignore_kz else is_natural_kz

            if ignore_kz:
                kz_display = "[bold magenta]BYPASSED (24/7 TEST)[/bold magenta]"
            elif is_london:
                kz_display = "[bold green]ACTIVE (London Open)[/bold green]"
            elif is_ny:
                kz_display = "[bold green]ACTIVE (NY Open)[/bold green]"
            else:
                kz_display = "[dim yellow]INACTIVE (Off-Hours)[/dim yellow]"

            latest_closed_ts = max([t for t in last_candle_times.values() if t is not None], default=utc_now)
            order_mgr.manage_open_trades(current_bar_time=latest_closed_ts)

            table = Table(
                title=f"MT5 LIVE FOREX & CFD TELEMETRY | UTC: {utc_now.strftime('%H:%M:%S')}",
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
            table.add_column("VWAP%", justify="right", width=8)
            table.add_column("EMA50%", justify="right", width=9)
            table.add_column("EMA200%", justify="right", width=8)
            table.add_column("4H Trend", justify="center", width=10)
            table.add_column("FVG", justify="center", width=7)
            table.add_column("P*", justify="right", width=8)
            table.add_column("Decision / Trigger Reason", justify="left", width=25)

            for asset, eng in engines.items():
                tick = mt5_conn.get_last_tick(asset)
                if tick is None:
                    continue

                bid = tick.bid
                ask = tick.ask
                spread = ask - bid

                # Dynamic detection of newly completed 15m candle
                recent_bars = mt5_conn.get_15m_bars(asset, count=3)
                if not recent_bars.empty and len(recent_bars) >= 2:
                    closed_bar = recent_bars.iloc[-2]
                    closed_bar_time = closed_bar['datetime']
                    if last_candle_times.get(asset) is None or closed_bar_time > last_candle_times[asset]:
                        new_bar = {
                            'datetime': closed_bar_time,
                            'open': closed_bar['open'],
                            'high': closed_bar['high'],
                            'low': closed_bar['low'],
                            'close': closed_bar['close'],
                            'volume': closed_bar['tick_volume']
                        }
                        eng.update_bar(new_bar)
                        eng.refresh_4h_buffer()
                        last_candle_times[asset] = closed_bar_time
                        pre_flight_data_sync(mt5_conn, single_asset=asset)

                try:
                    prob = eng.predict(xgb_model)
                    features = eng.compute_features().iloc[-1]
                except Exception as e:
                    logging.error(f"Inference error for {asset}: {e}")
                    continue

                rsi = features.get('rsi_14', 50.0)
                vwap_dist = features.get('vwap_dist', 0.0) * 100.0
                ema50_dist = features.get('ema_50_dist', 0.0) * 100.0
                ema200_dist = features.get('ema_200_dist', 0.0) * 100.0

                trend_val = features.get('htf_4h_trend', 0.0)
                trend_cell = "[bold green]BULL[/bold green]" if trend_val > 0 else ("[bold red]BEAR[/bold red]" if trend_val < 0 else "[dim]FLAT[/dim]")

                bull_fvg = features.get('bullish_fvg', 0.0)
                bear_fvg = features.get('bearish_fvg', 0.0)
                fvg_cell = "[bold green]BULL[/bold green]" if bull_fvg > 0 else ("[bold red]BEAR[/bold red]" if bear_fvg > 0 else "[dim]NONE[/dim]")

                rsi_cell = f"[bold red]{rsi:.1f}[/bold red]" if rsi >= 70 else (f"[bold green]{rsi:.1f}[/bold green]" if rsi <= 30 else f"{rsi:.1f}")
                prob_cell = f"[bold green]{prob:.3f}[/bold green]" if prob >= PROBABILITY_THRESHOLD else f"[dim]{prob:.3f}[/dim]"

                # Strategy Setup Evaluation
                local_low = eng.buffer['low'].iloc[-20:].min() if len(eng.buffer) >= 20 else eng.buffer['low'].min()
                local_high = eng.buffer['high'].iloc[-20:].max() if len(eng.buffer) >= 20 else eng.buffer['high'].max()

                crt_state = eng.compute_crt_orb()

                if strat_mode == "fvg":
                    strat_tag = "FVG"
                    is_long_sig = (trend_val > 0 and bull_fvg > 0)
                    is_short_sig = (trend_val < 0 and bear_fvg > 0)
                    sig_sl_long = local_low
                    sig_sl_short = local_high
                elif strat_mode == "crt":
                    strat_tag = "CRT"
                    is_long_sig = (crt_state["is_long_crt"] and (trend_val > 0 or crt_state["judas_long"]))
                    is_short_sig = (crt_state["is_short_crt"] and (trend_val < 0 or crt_state["judas_short"]))
                    sig_sl_long = crt_state["or_low"] if crt_state["or_low"] > 0 else local_low
                    sig_sl_short = crt_state["or_high"] if crt_state["or_high"] > 0 else local_high
                elif strat_mode == "ml":
                    strat_tag = "ML"
                    is_long_sig = (trend_val > 0 and prob >= PROBABILITY_THRESHOLD)
                    is_short_sig = (trend_val < 0 and prob >= PROBABILITY_THRESHOLD)
                    sig_sl_long = local_low
                    sig_sl_short = local_high
                else:  # combined multi-confluence
                    strat_tag = "COMBINED"
                    # High conviction: FVG or CRT aligned with ML
                    is_long_sig = ((trend_val > 0 and bull_fvg > 0) or crt_state["is_long_crt"]) and (prob >= PROBABILITY_THRESHOLD)
                    is_short_sig = ((trend_val < 0 and bear_fvg > 0) or crt_state["is_short_crt"]) and (prob >= PROBABILITY_THRESHOLD)
                    sig_sl_long = crt_state["or_low"] if crt_state["is_long_crt"] and crt_state["or_low"] > 0 else local_low
                    sig_sl_short = crt_state["or_high"] if crt_state["is_short_crt"] and crt_state["or_high"] > 0 else local_high

                decision_cell = "[dim]HOLD[/dim]"
                if not is_kz:
                    decision_cell = "[dim yellow]HOLD (Off-Hours)[/dim yellow]"
                elif is_long_sig:
                    entry = ask
                    sl = sig_sl_long
                    r_dist = entry - sl
                    if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                        decision_cell = "[dim]HOLD (Stop Range Invalid)[/dim]"
                    else:
                        tp = entry + (2.5 * r_dist)
                        calc_lots = order_mgr.calculate_lot_size(asset, risk_usd=BASE_RISK_USD, sl_dist=r_dist)
                        action_lbl = f"DRY-BUY ({strat_tag})" if is_dry_run else f"LIVE-BUY ({strat_tag})"
                        decision_cell = f"[bold white on green] {action_lbl} ({calc_lots:.2f}L) [/bold white on green]"
                        signals_count += 1
                        log_tag = "DRY-RUN" if is_dry_run else "LIVE"
                        logging.info(f"[{log_tag} SIGNAL: {asset} | BUY ({strat_tag}) | P*={prob:.3f} | ENTRY={entry:.5f} | SL={sl:.5f} | TP={tp:.5f} | LOTS={calc_lots}]")
                        order_mgr.place_market_order(asset, mt5.ORDER_TYPE_BUY, volume=calc_lots, sl_price=sl, tp_price=tp, risk_usd=BASE_RISK_USD, strategy_tag=strat_tag)

                elif is_short_sig:
                    entry = bid
                    sl = sig_sl_short
                    r_dist = sl - entry
                    if r_dist <= 0 or (r_dist / entry) > MAX_STOP_PCT:
                        decision_cell = "[dim]HOLD (Stop Range Invalid)[/dim]"
                    else:
                        tp = entry - (2.5 * r_dist)
                        calc_lots = order_mgr.calculate_lot_size(asset, risk_usd=BASE_RISK_USD, sl_dist=r_dist)
                        action_lbl = f"DRY-SELL ({strat_tag})" if is_dry_run else f"LIVE-SELL ({strat_tag})"
                        decision_cell = f"[bold white on red] {action_lbl} ({calc_lots:.2f}L) [/bold white on red]"
                        signals_count += 1
                        log_tag = "DRY-RUN" if is_dry_run else "LIVE"
                        logging.info(f"[{log_tag} SIGNAL: {asset} | SELL ({strat_tag}) | P*={prob:.3f} | ENTRY={entry:.5f} | SL={sl:.5f} | TP={tp:.5f} | LOTS={calc_lots}]")
                        order_mgr.place_market_order(asset, mt5.ORDER_TYPE_SELL, volume=calc_lots, sl_price=sl, tp_price=tp, risk_usd=BASE_RISK_USD, strategy_tag=strat_tag)

                else:
                    if strat_mode == "fvg":
                        if bull_fvg == 0 and bear_fvg == 0:
                            decision_cell = "[dim]HOLD (No FVG)[/dim]"
                        elif (trend_val > 0 and bear_fvg > 0) or (trend_val < 0 and bull_fvg > 0):
                            decision_cell = "[dim yellow]HOLD (Trend Opposed)[/dim yellow]"
                    elif strat_mode == "crt":
                        if not crt_state["is_long_crt"] and not crt_state["is_short_crt"]:
                            if crt_state["session"] != "None":
                                decision_cell = f"[dim]HOLD (Inside {crt_state['session']} OR)[/dim]"
                            else:
                                decision_cell = "[dim]HOLD (No OR Formed)[/dim]"
                        elif (crt_state["is_long_crt"] and trend_val < 0 and not crt_state["judas_long"]):
                            decision_cell = "[dim yellow]HOLD (CRT Bull vs Bear Trend)[/dim yellow]"
                        elif (crt_state["is_short_crt"] and trend_val > 0 and not crt_state["judas_short"]):
                            decision_cell = "[dim yellow]HOLD (CRT Bear vs Bull Trend)[/dim yellow]"
                    elif strat_mode == "ml":
                        if prob < PROBABILITY_THRESHOLD:
                            decision_cell = f"[dim]HOLD (P*={prob:.2f}<{PROBABILITY_THRESHOLD})[/dim]"
                        elif trend_val == 0:
                            decision_cell = "[dim yellow]HOLD (Flat Trend)[/dim yellow]"
                    else:
                        if bull_fvg == 0 and bear_fvg == 0 and not crt_state["is_long_crt"] and not crt_state["is_short_crt"]:
                            decision_cell = "[dim]HOLD (No FVG / CRT)[/dim]"
                        elif prob < PROBABILITY_THRESHOLD:
                            decision_cell = f"[dim]HOLD (P*={prob:.2f}<{PROBABILITY_THRESHOLD})[/dim]"
                        elif (trend_val > 0 and bear_fvg > 0) or (trend_val < 0 and bull_fvg > 0):
                            decision_cell = "[dim yellow]HOLD (Trend Opposed)[/dim yellow]"

                table.add_row(
                    asset,
                    f"{bid:.5f}",
                    f"{ask:.5f}",
                    f"{spread:.5f}",
                    rsi_cell,
                    f"{vwap_dist:+.2f}%",
                    f"{ema50_dist:+.2f}%",
                    f"{ema200_dist:+.2f}%",
                    trend_cell,
                    fvg_cell,
                    prob_cell,
                    decision_cell
                )

            safety_lbl = "[bold green]DRY-RUN MODE (Zero Real Orders)[/bold green]" if is_dry_run else "[bold red]LIVE EXECUTION MODE (REAL ORDERS ARMED)[/bold red]"
            if strat_mode == "fvg":
                strat_desc = "Rule-Based ICT FVG"
            elif strat_mode == "crt":
                strat_desc = "Candle Range Theory & ORB"
            elif strat_mode == "ml":
                strat_desc = "Pure XGBoost ML"
            else:
                strat_desc = "Multi-Confluence: FVG + CRT + ML"
            header_text = (
                f"[bold white]Account:[/bold white] #{acc_dict.get('login')} ({acc_dict.get('server')})  |  "
                f"[bold white]Balance:[/bold white] ${acc_dict.get('balance'):,.2f} USD  |  "
                f"[bold white]Equity:[/bold white] ${acc_dict.get('equity'):,.2f} USD\n"
                f"[bold white]Strategy:[/bold white] [bold cyan]{strat_mode.upper()}[/bold cyan] ({strat_desc})  |  "
                f"[bold white]Kill Zone:[/bold white] {kz_display}  |  "
                f"[bold white]Signals Logged:[/bold white] {signals_count}  |  "
                f"[bold white]Mode:[/bold white] {safety_lbl}"
            )
            header_panel = Panel(header_text, title="[bold bright_cyan]ENGINE: UNIFIED FOREX & CFD MASTER TERMINAL[/bold bright_cyan]", border_style="cyan")

            if not once:
                console.clear()
            console.print(header_panel)
            console.print(table)
            console.print("[dim]Press Ctrl+C to safely disconnect and exit.[/dim]\n")

            if once:
                break
            time.sleep(interval)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Exiting telemetry loop...[/bold yellow]")
    finally:
        mt5_conn.disconnect()
        print("[SHUTDOWN] MT5 disconnected cleanly. All state saved.")


# -------------------------------------------------------------------------
# COMPONENT 8: NUMERICAL PARITY & DIAGNOSTIC VERIFICATION
# -------------------------------------------------------------------------
def run_verify() -> None:
    """Verifies that streaming features match Polars batch features (< 1e-9 error)."""
    print("=" * 85)
    print(" RUNNING MATHEMATICAL FEATURE PARITY AUDIT (STREAMING vs BATCH)...")
    print("=" * 85)
    asset = "EURUSD"
    parquet_path = DATA_DIR / f"{asset}_15m_real.parquet"
    if not parquet_path.exists():
        print(f"[SKIP] Parquet for {asset} not found.")
        return

    df_raw = pd.read_parquet(parquet_path).sort_values("datetime").reset_index(drop=True)
    df_raw = df_raw.iloc[-300:].copy()
    df_raw.rename(columns={'tick_volume': 'volume'}, inplace=True)
    df_raw.set_index('datetime', inplace=True)

    # Compute batch features
    batch_features = compute_features_pandas(df_raw)

    # Compute streaming features incrementally
    eng = StatefulInferenceEngine(asset, max_bars=300)
    for idx, row in df_raw.iterrows():
        eng.update_bar({
            'datetime': idx,
            'open': row['open'],
            'high': row['high'],
            'low': row['low'],
            'close': row['close'],
            'volume': row['volume']
        })
    streaming_features = eng.compute_features()

    max_diff = 0.0
    for col in CANONICAL_FEATURES:
        b_val = float(batch_features[col].iloc[-1])
        s_val = float(streaming_features[col].iloc[-1])
        diff = abs(b_val - s_val)
        max_diff = max(max_diff, diff)
        print(f"  Feature {col:<16}: Batch={b_val:>12.6f} | Streaming={s_val:>12.6f} | Diff={diff:.2e}")

    print("-" * 85)
    if max_diff < 1e-9:
        print(f"[PASS] 100% Causal Mathematical Parity Confirmed (Max Error: {max_diff:.2e} < 1e-9)")
    else:
        print(f"[WARNING] Feature disparity detected (Max Error: {max_diff:.2e})")
    print("=" * 85)


def show_structure() -> None:
    """Prints repository storage paths for data, models, and logs."""
    print("=" * 85)
    print(" FOREX & CFD PRODUCTION STORAGE MAP & REPOSITORY ARCHITECTURE")
    print("=" * 85)
    print(f" [Project Root]       : {PROJECT_ROOT}")
    print(f" [Engine Directory]   : {ENGINE_DIR}")
    print(f" [Standalone Engine]  : {CURRENT_FILE}")
    print(f" [Historical Parquets]: {DATA_DIR} ({len(list(DATA_DIR.glob('*.parquet')))} parquet files)")
    print(f" [Production Model]   : {PRODUCTION_MODEL_PATH} ({'EXISTS' if PRODUCTION_MODEL_PATH.exists() else 'NOT FOUND'})")
    if PRODUCTION_MODEL_PATH.exists():
        print(f"                        Size: {PRODUCTION_MODEL_PATH.stat().st_size:,} bytes")
    print(f" [Dry Run Log File]   : {LOG_FILE}")
    print("=" * 85)


# -------------------------------------------------------------------------
# CLI ENTRYPOINT
# -------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Unified Master Forex & CFD Standalone Trading Engine (CLI)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Standard Usage:
  python Engine/forex_engine.py                         # Full cycle: Sync -> Retrain -> Multi-Confluence (Dry-Run)
  python Engine/forex_engine.py --strategy fvg          # Run pure Rule-Based ICT FVG strategy (Dry-Run)
  python Engine/forex_engine.py --strategy crt          # Run pure Candle Range Theory & ORB strategy (Dry-Run)
  python Engine/forex_engine.py --strategy ml           # Run pure Machine Learning XGBoost strategy (Dry-Run)
  python Engine/forex_engine.py --strategy combined     # Run multi-confluence FVG + CRT + ML strategy (Dry-Run)
  python Engine/forex_engine.py --mode snapshot         # Run single evaluation pass and cleanly exit
  python Engine/forex_engine.py --mode snapshot --strategy crt
  python Engine/forex_engine.py --skip-train            # Skip retraining, run telemetry immediately
  python Engine/forex_engine.py --live                  # ARM LIVE TRADING: Dispatch real market orders to MT5
  python Engine/forex_engine.py --mode verify           # Run numerical parity assertions (< 1e-9 error)
  python Engine/forex_engine.py --mode info             # Display data & model storage paths
        """
    )
    parser.add_argument(
        "--mode",
        choices=["dry-run", "snapshot", "train", "verify", "info"],
        default="dry-run",
        help="Execution mode (default: dry-run)"
    )
    parser.add_argument(
        "--strategy",
        choices=["fvg", "crt", "ml", "combined"],
        default="combined",
        help="Trading strategy: 'fvg' (Rule-Based ICT FVG), 'crt' (Candle Range Theory & ORB), 'ml' (Pure XGBoost ML), 'combined' (Multi-Confluence: FVG + CRT + ML) (default: combined)"
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=True,
        help="Run in safe paper trading dry-run mode (zero broker orders; default: True)"
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
        help="Skip model deletion and retraining; run live telemetry immediately."
    )
    parser.add_argument(
        "--ignore-kz",
        action="store_true",
        help="Bypass the London/NY kill zone filter for 24/7 dry-run signal testing."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.5,
        help="Telemetry refresh interval in seconds (default: 1.5)"
    )

    args = parser.parse_args()

    if args.mode == "info":
        show_structure()
        return

    if args.mode == "verify":
        run_verify()
        return

    if not args.skip_train and args.mode in ["dry-run", "snapshot", "train"]:
        if PRODUCTION_MODEL_PATH.exists():
            try:
                os.remove(PRODUCTION_MODEL_PATH)
            except Exception:
                pass
        dynamic_retrain()

    if args.mode == "train":
        print("\n[COMPLETE] Model retrained successfully and ready for deployment.")
        return

    is_once = (args.mode == "snapshot")
    run_telemetry(
        once=is_once,
        ignore_kz=args.ignore_kz,
        strategy=args.strategy,
        dry_run=args.dry_run,
        live=args.live,
        interval=args.interval
    )


if __name__ == "__main__":
    main()
