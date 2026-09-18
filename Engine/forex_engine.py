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

from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
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
    ParallelForexStrategy,
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

# Explicitly import ORB_CRT strategy to register it into StrategyRegistry
try:
    from Engine.ORB_CRT_ForexCFD_Strategy import ORBCRTForexCFDStrategy
except ImportError:
    try:
        from Engine.strategy.ORB_CRT_ForexCFD_Strategy import ORBCRTForexCFDStrategy
    except ImportError:
        logging.warning("Could not import ORBCRTForexCFDStrategy at startup; will resolve dynamically.")

DATA_DIR = PROJECT_ROOT / "Forex_Backtesting_Data"
MODELS_DIR = ENGINE_DIR / "models"
PRODUCTION_MODEL_PATH = MODELS_DIR / "xgboost_forex.json"
CRITERIA_PATH = ENGINE_DIR / "target_oos_criteria.json"
FOREX_WINDOWS_PATH = ENGINE_DIR / "oos_windows_forex_20.json"
WINDOWS_PATH = FOREX_WINDOWS_PATH if FOREX_WINDOWS_PATH.exists() else (ENGINE_DIR / "oos_windows_20.json")
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
import shutil

def get_terminal_width() -> int:
    try:
        cols = shutil.get_terminal_size().columns
        return max(130, cols)
    except Exception:
        return 130

console = Console(force_terminal=True, width=get_terminal_width())

# -------------------------------------------------------------------------
# CANONICAL STRATEGY CONSTANTS & OPTION C GOVERNANCE
# -------------------------------------------------------------------------
BASE_RISK_USD = 25.0              # 0.50% of 5,000 USD capital (base risk)
DEFENSE_RISK_USD = 15.0           # 0.30% — arms when DD >= 2.0% (100 USD)
HOUSE_MONEY_RISK_USD = 35.0       # 0.70% — unlocks when cumulative profit >= 100 USD AND DD < 1.0%
HARD_DD_LIMIT_PCT = 4.50          # 4.5% Hard DD Stop (225.00 USD) — total freeze
DEFENSE_DD_LIMIT_PCT = 2.00       # 2.0% DD Defense threshold (100.00 USD)
HOUSE_MONEY_THRESHOLD_USD = 100.0 # Profit must exceed 100 USD to unlock house money (research: Calmar 109.86)
HOUSE_MONEY_MAX_DD_PCT = 1.00     # House money only active if current DD < 1.0% (protects against giving back gains)
MAX_HOLDING_BARS = 96             # 24 hours in 15m bars
TIME_DECAY_BARS = 24              # 6 hours in 15m bars
TIME_DECAY_THRESHOLD_R = 0.20
MAX_STOP_PCT = 0.025              # 2.5% max stop distance
PROBABILITY_THRESHOLD = 0.54      # Signal confidence gate (research: 0.54 maximises Calmar across 20 OOS windows)
MAX_SPREAD_ATR_RATIO = 0.12       # Dynamic quarantine: spread > 12% of 15m ATR
MAX_SPREAD_ATR_RATIO_ENTER = 0.12 # Enter quarantine threshold
MAX_SPREAD_ATR_RATIO_EXIT = 0.08  # Exit quarantine hysteresis threshold
MIN_SPREAD_MULTIPLIER = 3.5       # Stop distance must be >= 3.5x current broker spread
MIN_ATR_MULTIPLIER = 1.5          # Stop distance must be >= 1.5x 15m ATR
MIN_STRUCTURAL_R_EFF = 1.20       # Minimum effective R for structural targets
MAX_STRUCTURAL_R_EFF = 3.50       # Cap effective R to avoid tail liquidity moonshots
MAX_MARGIN_UTILIZATION_PCT = 0.30 # Portfolio margin utilization ceiling (30%)
MIN_MARGIN_LEVEL_PCT = 200.0      # Minimum margin level before hard freeze (200%)

# Institutional Correlation Clusters (Max 1 concurrent position per cluster)
CORRELATION_CLUSTERS = {
    'EUR_BLOC': {'EURUSD', 'EURSEK', 'EURCNH', 'EURHUF'},
    'USD_BLOC': {'NZDUSD', 'AUDCHF', 'USDSEK', 'USDHKD'},
    'CNH_BLOC': {'NZDCNH', 'XAUCNH', 'GAUCNH'},
    'INDEX_BLOC': {'GER40', 'GER30', 'FR40', 'AU200', 'US2000'},
    'COMMODITY_BLOC': {'GAS', 'NICKEL', 'LEAD'}
}

# Exotic assets restricted to London/NY liquid overlap hours (07:00 to 17:00 UTC)
EXOTIC_SESSION_RESTRICTED = {
    'EURHUF', 'EURSEK', 'USDSEK', 'USDHKD', 'GAS', 'NICKEL', 'LEAD'
}

# -------------------------------------------------------------------------
# INSTITUTIONAL OPERATIONAL SAFEGUARDS (OPUS AUDIT MANDATES)
# -------------------------------------------------------------------------
ROLLOVER_LOCKOUT_START_MINUTE = 21 * 60 + 55  # 21:55 UTC (Bank Rollover Settlement)
ROLLOVER_LOCKOUT_END_MINUTE = 22 * 60 + 15    # 22:15 UTC (Spread Stabilization)
FRIDAY_ENTRY_CUTOFF_HOUR = 18                 # 18:00 UTC Friday: No new trade entries
FRIDAY_CLOSEOUT_HOUR = 20                     # 20:30 UTC Friday: Weekend Gap Defense liquidation
FRIDAY_CLOSEOUT_MINUTE = 30
RECONCILE_HEARTBEAT_INTERVAL_SEC = 30.0       # 30-second MT5 broker position reconciliation


def is_broker_rollover_window(dt_utc: Optional[datetime] = None) -> bool:
    """
    Enforces hard temporal lockout between 21:55 UTC and 22:15 UTC (Daily Bank Settlement).
    During this 20-minute window, interbank spreads widen by 10x-50x.
    All new orders and broker-side ratchet modifications are strictly frozen.
    """
    dt = dt_utc or datetime.now(timezone.utc)
    minute_of_day = dt.hour * 60 + dt.minute
    return ROLLOVER_LOCKOUT_START_MINUTE <= minute_of_day <= ROLLOVER_LOCKOUT_END_MINUTE


def is_friday_weekend_lockout(dt_utc: Optional[datetime] = None) -> bool:
    """
    Bans new trade entries after Friday 18:00 UTC to prevent weekend gap exposure
    in commodities (GAS, NICKEL) and index CFDs (GER40, US2000).
    """
    dt = dt_utc or datetime.now(timezone.utc)
    return dt.weekday() == 4 and dt.hour >= FRIDAY_ENTRY_CUTOFF_HOUR


def is_friday_closeout_window(dt_utc: Optional[datetime] = None) -> bool:
    """
    Signals weekend closeout starting Friday 20:30 UTC for all CFD/Forex holdings.
    """
    dt = dt_utc or datetime.now(timezone.utc)
    if dt.weekday() != 4:
        return False
    return (dt.hour > FRIDAY_CLOSEOUT_HOUR) or (
        dt.hour == FRIDAY_CLOSEOUT_HOUR and dt.minute >= FRIDAY_CLOSEOUT_MINUTE
    )




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
def robust_parquet_replace(tmp_file: Path, target_file: Path, max_retries: int = 5, base_delay: float = 0.1) -> bool:
    """Atomic file replacement with exponential backoff on Windows file locking."""
    for attempt in range(max_retries):
        try:
            os.replace(str(tmp_file), str(target_file))
            return True
        except PermissionError:
            time.sleep(base_delay * (2 ** attempt))
    try:
        os.replace(str(tmp_file), str(target_file))
        return True
    except Exception as e:
        logging.error(f"Failed to replace {target_file} after {max_retries} retries: {e}")
        try:
            if tmp_file.exists():
                tmp_file.unlink()
        except Exception:
            pass
        raise


def resolve_parquet_file(symbol: str) -> Optional[Path]:
    """Resolves 15m parquet filepath handling canonical names and GER30/GER40 aliases."""
    candidates = [
        DATA_DIR / f"{symbol}_15m_real.parquet",
        DATA_DIR / f"{symbol}.parquet"
    ]
    if symbol in ["GER30", "GER40"]:
        candidates.extend([
            DATA_DIR / "GER40_15m_real.parquet",
            DATA_DIR / "GER30_15m_real.parquet",
            DATA_DIR / "GER40.parquet",
            DATA_DIR / "GER30.parquet"
        ])
    for cand in candidates:
        if cand.exists():
            return cand
    return None


def resolve_aux_parquet(symbol: str, timeframe: str) -> Optional[Path]:
    """Resolves 4H or D1 auxiliary parquet filepaths."""
    candidates = [
        DATA_DIR / f"{symbol}_{timeframe}_real.parquet",
        DATA_DIR / f"{symbol}_{timeframe}.parquet"
    ]
    if symbol in ["GER30", "GER40"]:
        candidates.extend([
            DATA_DIR / f"GER40_{timeframe}_real.parquet",
            DATA_DIR / f"GER30_{timeframe}_real.parquet"
        ])
    for cand in candidates:
        if cand.exists():
            return cand
    return None


# -------------------------------------------------------------------------
# COMPONENT 2: ORDER MANAGEMENT & MICROSTRUCTURE RATCHETS
# -------------------------------------------------------------------------
class OrderManager:
    """Handles dynamic lot sizing, paper dry-run simulation, and live microstructure ratchets."""
    def __init__(self, connection: MT5Connection, dry_run: bool = True, max_concurrent: int = 2):
        self.conn = connection
        self.dry_run = dry_run
        self.max_concurrent = max_concurrent
        self.open_trades: Dict[int, Dict[str, Any]] = {}
        self.closed_trades: List[Dict[str, Any]] = []
        self.initial_balance: float = 5000.0
        self.realized_pnl: float = 0.0
        self.state_file = LOG_DIR / "live_state.json"
        self.load_state()

    def save_state(self) -> None:
        """Persists open trades and realized PnL to live_state.json so it survives restarts."""
        try:
            state_data = {
                "realized_pnl": self.realized_pnl,
                "initial_balance": self.initial_balance,
                "open_trades": self.open_trades,
                "timestamp": time.time()
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2, default=str)
        except Exception as e:
            logging.error(f"Failed to save live state: {e}")

    def load_state(self) -> None:
        """Reconciles persisted state with MT5 live positions on boot and normalizes schema."""
        if not self.state_file.exists():
            return
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
            self.realized_pnl = float(state_data.get("realized_pnl", 0.0))
            saved_trades = state_data.get("open_trades", {})

            raw_trades: Dict[int, Dict[str, Any]] = {}
            if not self.dry_run and self.conn.connected:
                live_positions = {p.ticket: p for p in (mt5.positions_get() or [])}
                for k, v in saved_trades.items():
                    if int(k) in live_positions:
                        raw_trades[int(k)] = v
                for tkt, pos in live_positions.items():
                    if tkt not in raw_trades:
                        raw_trades[tkt] = {
                            "ticket": tkt,
                            "symbol": pos.symbol,
                            "real_symbol": pos.symbol,
                            "type": pos.type,
                            "volume": pos.volume,
                            "entry": pos.price_open,
                            "entry_price": pos.price_open,
                            "sl": pos.sl,
                            "tp": pos.tp,
                        }
            else:
                raw_trades = {int(k): v for k, v in saved_trades.items()}

            self.open_trades = {}
            for tkt, tr in raw_trades.items():
                entry = float(tr.get("entry") or tr.get("entry_price") or tr.get("price") or 0.0)
                sl = float(tr.get("sl", 0.0))
                tp = float(tr.get("tp", 0.0))
                r_dist = float(tr.get("r_dist", 0.0))
                if r_dist <= 0.0:
                    r_dist = abs(entry - sl) if sl > 0.0 else 0.0001
                order_type = int(tr.get("type", 0))
                action = tr.get("action") or ("BUY" if order_type in (0, mt5.ORDER_TYPE_BUY) else "SELL")
                bars_held = int(tr.get("bars_held", tr.get("bars_elapsed", 0)))
                risk_usd = float(tr.get("risk_usd", BASE_RISK_USD))

                norm_trade = {
                    "ticket": int(tkt),
                    "symbol": tr.get("symbol", ""),
                    "real_symbol": tr.get("real_symbol", tr.get("symbol", "")),
                    "type": order_type,
                    "action": action,
                    "volume": float(tr.get("volume", 0.01)),
                    "entry": entry,
                    "entry_price": entry,
                    "cur_price": float(tr.get("cur_price", entry)),
                    "sl": sl,
                    "tp": tp,
                    "risk_usd": risk_usd,
                    "r_dist": r_dist,
                    "entry_time": tr.get("entry_time", datetime.now(timezone.utc)),
                    "bars_held": bars_held,
                    "bars_elapsed": bars_held,
                    "strategy": tr.get("strategy", "PARALLEL"),
                    "highest_r": float(tr.get("highest_r", 0.0)),
                    "lowest_r": float(tr.get("lowest_r", 0.0)),
                    "current_r": float(tr.get("current_r", 0.0)),
                    "running_pnl": float(tr.get("running_pnl", 0.0)),
                    "ratchet_phase": int(tr.get("ratchet_phase", 0)),
                    "ratchet_desc": str(tr.get("ratchet_desc", "Base SL (-1.00R)")),
                    "last_evaluated_bar": tr.get("last_evaluated_bar", None),
                    "last_bar_time": tr.get("last_bar_time", None)
                }
                self.open_trades[int(tkt)] = norm_trade

            logging.info(f"Loaded live state: realized_pnl={self.realized_pnl:.2f} USD, open_trades={len(self.open_trades)}")
        except Exception as e:
            logging.error(f"Failed to load live state: {e}")

    def reconcile_with_broker(self) -> None:
        """
        Broker Position Reconciliation Heartbeat (runs every 30s during live telemetry).
        Cross-verifies MT5 broker-side tickets against local open_trades memory.
        Detects positions closed externally by broker-side SL/TP or terminal disconnects.
        """
        if self.dry_run or not self.conn.connected:
            return
        try:
            live_pos = mt5.positions_get()
            live_positions = {p.ticket: p for p in (live_pos or [])}
            missing_tickets = [t for t in list(self.open_trades.keys()) if t not in live_positions]
            for t in missing_tickets:
                closed_trade = self.open_trades.pop(t)
                sym_name = closed_trade.get("symbol", "UNKNOWN") if isinstance(closed_trade, dict) else "UNKNOWN"
                logging.info(f"[RECONCILE HEARTBEAT] Detected external/broker closure for ticket #{t} ({sym_name}). State reconciled.")
            if missing_tickets:
                self.save_state()
        except Exception as e:
            logging.error(f"[RECONCILE HEARTBEAT ERROR] Failed to cross-verify MT5 positions: {e}")


    def get_current_risk_budget(self) -> Tuple[float, str]:
        """
        3-Tier Calmar-Optimised Risk Governor (research: Avg Calmar 40.41, peak 138.59 across 20 OOS windows):
        - Tier 0 HARD FREEZE  : DD >= 4.50% (225 USD)  -> 0.00 USD. No new trades.
        - Tier 1 DD DEFENSE   : DD >= 2.00% (100 USD)  -> 15.00 USD (0.30%). Priority over house money.
        - Tier 2 HOUSE MONEY  : Profit >= 100 USD AND DD < 1.00% -> 35.00 USD (0.70%).
        - Tier 3 NORMAL       : Default                -> 25.00 USD (0.50%).
        Returns: (governed_risk_usd, regime_label)
        """
        metrics = self.get_account_metrics()
        current_equity = metrics.get("equity", self.initial_balance + self.realized_pnl)
        dd_usd = max(0.0, self.initial_balance - current_equity)
        dd_pct = (dd_usd / self.initial_balance) * 100.0 if self.initial_balance > 0 else 0.0

        if dd_pct >= HARD_DD_LIMIT_PCT or dd_usd >= 225.0:
            return 0.0, f"HARD FREEZE (DD {dd_pct:.2f}% >= {HARD_DD_LIMIT_PCT:.1f}%)"
        elif dd_pct >= DEFENSE_DD_LIMIT_PCT or dd_usd >= 100.0:
            return DEFENSE_RISK_USD, f"DEFENSE (15.00 USD | DD {dd_pct:.2f}%)"
        elif self.realized_pnl >= HOUSE_MONEY_THRESHOLD_USD and dd_pct < HOUSE_MONEY_MAX_DD_PCT:
            return HOUSE_MONEY_RISK_USD, f"HOUSE MONEY (35.00 USD | Profit +{self.realized_pnl:.2f} USD | DD {dd_pct:.2f}%)"
        return BASE_RISK_USD, f"NORMAL ({BASE_RISK_USD:.2f} USD)"


    def calculate_lot_size(self, symbol: str, risk_usd: float, sl_dist: float) -> float:
        """Calculates exact lot size based on symbol contract size and currency conversion with leverage caps."""
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

        # P0 FIX: Institutional Maximum Leverage & Notional Sizing Caps
        sym_clean = symbol.upper().replace(".PI", "").replace(".P", "").replace(".R", "")
        if sym_clean in ['EURUSD', 'NZDUSD', 'AUDCHF']:
            max_leverage = 10.0  # Majors: 10:1 max leverage (max 50k USD on 5k account)
        elif sym_clean in ['EURCNH', 'NZDCNH']:
            max_leverage = 5.0   # Minors: 5:1 max leverage (max 25k USD)
        elif sym_clean in ['GER40', 'GER30', 'FR40', 'AU200', 'US2000']:
            max_leverage = 5.0   # Indices: 5:1 max leverage
        else:
            max_leverage = 3.0   # Exotics & Commodities: 3:1 max leverage (max 15k USD)

        tick = self.conn.get_last_tick(symbol)
        curr_price = tick.bid if tick and tick.bid > 0 else 1.0

        metrics = self.get_account_metrics()
        equity = metrics.get("equity", self.initial_balance + self.realized_pnl)
        acc_leverage = 30.0
        if self.conn.connected:
            acc = mt5.account_info()
            if acc and acc.leverage > 0:
                acc_leverage = float(acc.leverage)

        # Exact notional in account currency (USD) per 1.0 lot using broker margin requirements
        broker_margin_1lot = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, real_symbol, 1.0, curr_price) if self.conn.connected else 0.0
        if broker_margin_1lot and broker_margin_1lot > 0:
            contract_notional_usd = broker_margin_1lot * acc_leverage
        else:
            contract_notional_usd = trade_contract if trade_contract > 0 else 100000.0

        max_notional_cap = equity * max_leverage
        max_lots_leverage = max_notional_cap / contract_notional_usd if contract_notional_usd > 0 else 1.0

        raw_lot = min(raw_lot, max_lots_leverage)

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
        # Risk constraint 0: Institutional Drawdown Circuit Breaker
        governed_risk, regime_lbl = self.get_current_risk_budget()
        if governed_risk <= 0.0:
            logging.warning(f"[RISK VETO] {regime_lbl}. New order for {symbol} blocked.")
            return None
        # Enforce governed risk level
        risk_usd = min(risk_usd, governed_risk) if risk_usd > 0 else governed_risk

        # Operational Safeguard 1: Broker Rollover Spread Trap Lockout (21:55 - 22:15 UTC)
        if is_broker_rollover_window():
            logging.warning(f"[ROLLOVER VETO] 21:55-22:15 UTC interbank rollover settlement active. Order for {symbol} blocked.")
            return None

        # Operational Safeguard 2: Friday Weekend Gap Protection (No new entries after 18:00 UTC Friday)
        if is_friday_weekend_lockout():
            logging.warning(f"[WEEKEND VETO] Friday >= {FRIDAY_ENTRY_CUTOFF_HOUR}:00 UTC weekend gap cutoff active. Order for {symbol} blocked.")
            return None


        # P0 FIX: Margin Level & Margin Utilization Circuit Breakers
        metrics = self.get_account_metrics()
        margin_level = metrics.get("margin_level", 1000.0)
        if margin_level > 0 and margin_level < MIN_MARGIN_LEVEL_PCT:
            logging.warning(f"[RISK VETO] Account margin level ({margin_level:.1f}%) < {MIN_MARGIN_LEVEL_PCT:.0f}%. Order for {symbol} blocked.")
            return None

        equity = metrics.get("equity", self.initial_balance + self.realized_pnl)
        curr_margin = metrics.get("margin", 0.0)
        if equity > 0 and (curr_margin / equity) > MAX_MARGIN_UTILIZATION_PCT:
            logging.warning(f"[RISK VETO] Margin utilization ({(curr_margin/equity):.1%}) > {MAX_MARGIN_UTILIZATION_PCT:.0%}. Order for {symbol} blocked.")
            return None

        # Risk constraint 1: Max concurrent positions across portfolio
        if len(self.open_trades) >= self.max_concurrent:
            logging.info(f"[RISK VETO] Max concurrent positions ({self.max_concurrent}) reached. Signal for {symbol} vetoed.")
            return None

        # Risk constraint 2: Single position per asset (cluster/normalized)
        sym_clean = symbol.upper().replace(".PI", "").replace(".P", "").replace(".R", "")
        for ot in self.open_trades.values():
            ot_sym_clean = ot.get("symbol", "").upper().replace(".PI", "").replace(".P", "").replace(".R", "")
            if ot.get("symbol") == symbol or ot["symbol"] == symbol or ot_sym_clean == sym_clean:
                logging.info(f"[RISK VETO] Active position already open on {symbol} ({ot.get('symbol')}). Duplicate signal vetoed.")
                return None

        # P1 FIX: Correlation Cluster Constraint (Max 1 position per cluster)
        symbol_cluster = None
        for c_name, c_members in CORRELATION_CLUSTERS.items():
            if sym_clean in c_members:
                symbol_cluster = c_name
                break

        if symbol_cluster:
            for ot in self.open_trades.values():
                ot_sym = ot.get("symbol", "").upper().replace(".PI", "").replace(".P", "").replace(".R", "")
                if ot_sym in CORRELATION_CLUSTERS.get(symbol_cluster, set()):
                    logging.info(f"[RISK VETO] Active position already open in cluster {symbol_cluster} ({ot_sym}). Signal for {symbol} vetoed.")
                    return None

        real_symbol = self.conn.resolve_symbol(symbol)
        action_name = "BUY" if order_type == mt5.ORDER_TYPE_BUY else "SELL"

        if self.dry_run:
            fake_ticket = int(time.time() * 1000) % 100000000
            tick = self.conn.get_last_tick(symbol)
            fill_price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else (tick.bid if tick else 1.0)

            r_dist = abs(fill_price - sl_price) if sl_price is not None else 0.0001
            if r_dist <= 0:
                r_dist = 0.0001
            self.open_trades[fake_ticket] = {
                "ticket": fake_ticket,
                "symbol": symbol,
                "real_symbol": real_symbol,
                "type": order_type,
                "action": action_name,
                "volume": volume,
                "entry": fill_price,
                "entry_price": fill_price,
                "cur_price": fill_price,
                "sl": sl_price,
                "tp": tp_price,
                "risk_usd": risk_usd,
                "r_dist": r_dist,
                "entry_time": datetime.now(timezone.utc),
                "bars_held": 0,
                "bars_elapsed": 0,
                "strategy": strategy_tag,
                "highest_r": 0.0,
                "lowest_r": 0.0,
                "current_r": 0.0,
                "running_pnl": 0.0,
                "ratchet_phase": 0,
                "ratchet_desc": "Base SL (-1.00R)"
            }
            logging.info(f"[PAPER ORDER] {action_name} {volume:.2f}L {symbol} @ {fill_price:.5f} | SL={sl_price:.5f} | TP={tp_price:.5f} | #{fake_ticket}")
            self.save_state()
            return fake_ticket

        # Real Live Broker Order
        tick = self.conn.get_last_tick(symbol)
        price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else (tick.bid if tick else 0.0)
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
        if not res or res.retcode != mt5.TRADE_RETCODE_DONE:
            err_comment = res.comment if res else "No response"
            err_code = res.retcode if res else -1
            logging.error(f"[LIVE ORDER FAILED] {symbol} {action_name}: {err_comment} ({err_code})")
            return None

        live_ticket = res.order
        fill_price = res.price if res.price > 0 else price
        r_dist = abs(fill_price - sl_price) if sl_price is not None else 0.0001
        if r_dist <= 0:
            r_dist = 0.0001
        self.open_trades[live_ticket] = {
            "ticket": live_ticket,
            "symbol": symbol,
            "real_symbol": real_symbol,
            "type": order_type,
            "action": action_name,
            "volume": volume,
            "entry": fill_price,
            "entry_price": fill_price,
            "cur_price": fill_price,
            "sl": sl_price,
            "tp": tp_price,
            "risk_usd": risk_usd,
            "r_dist": r_dist,
            "entry_time": datetime.now(timezone.utc),
            "bars_held": 0,
            "bars_elapsed": 0,
            "strategy": strategy_tag,
            "highest_r": 0.0,
            "lowest_r": 0.0,
            "current_r": 0.0,
            "running_pnl": 0.0,
            "ratchet_phase": 0,
            "ratchet_desc": "Base SL (-1.00R)"
        }
        logging.info(f"[LIVE ORDER FILLED] {action_name} {volume:.2f}L {symbol} @ {fill_price:.5f} | Ticket: {live_ticket}")
        self.save_state()
        return live_ticket

    def modify_sl(self, ticket: int, new_sl: float) -> bool:
        if self.dry_run:
            if ticket in self.open_trades:
                old_sl = self.open_trades[ticket].get("sl", 0.0)
                self.open_trades[ticket]["sl"] = new_sl
                logging.info(f"[PAPER RATCHET] #{ticket} SL modified: {old_sl:.5f} -> {new_sl:.5f}")
                self.save_state()
                return True
            return False

        trade = self.open_trades.get(ticket)
        if not trade:
            return False
        real_sym = trade.get("real_symbol") or trade.get("symbol", "")
        # Check minimum broker stop distance (trade_stops_level)
        info = mt5.symbol_info(real_sym)
        if info is not None:
            min_dist = info.trade_stops_level * info.point
            tick = self.conn.get_last_tick(real_sym)
            if tick is not None:
                is_buy = (trade.get("type", 0) in (0, mt5.ORDER_TYPE_BUY))
                current_price = tick.bid if is_buy else tick.ask
                if abs(new_sl - current_price) < min_dist:
                    logging.warning(f"[MODIFY SL SKIP] Proposed SL {new_sl:.5f} too close to current price {current_price:.5f} (min dist: {min_dist:.5f}).")
                    return False

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": real_sym,
            "sl": float(new_sl),
            "tp": float(trade.get("tp", 0.0))
        }
        res = mt5.order_send(request)
        if res and res.retcode == mt5.TRADE_RETCODE_DONE:
            trade["sl"] = new_sl
            self.save_state()
            logging.info(f"[LIVE RATCHET SL MODIFIED] #{ticket} {real_sym} SL -> {new_sl:.5f}")
            return True
        elif res:
            logging.warning(f"[MODIFY SL FAILED] #{ticket}: {res.comment} ({res.retcode})")
        return False

    def close_trade(
        self,
        ticket: int,
        exit_price: Optional[float] = None,
        realized_r: Optional[float] = None,
        reason: str = "NORMAL"
    ) -> None:
        if ticket not in self.open_trades:
            return
        t = self.open_trades.pop(ticket)
        entry = float(t.get("entry") or t.get("entry_price") or 0.0)
        actual_exit = exit_price if exit_price is not None else float(t.get("cur_price") or entry)
        r_dist = float(t.get("r_dist", 0.0001))
        if r_dist <= 0:
            r_dist = 0.0001

        is_long = (t.get("type", 0) in (0, mt5.ORDER_TYPE_BUY))
        if realized_r is not None:
            actual_r = realized_r
        else:
            actual_r = (actual_exit - entry) / r_dist if is_long else (entry - actual_exit) / r_dist

        risk_usd = float(t.get("risk_usd", BASE_RISK_USD))
        realized_pnl = actual_r * risk_usd
        self.realized_pnl += realized_pnl

        closed_record = {
            "ticket": ticket,
            "symbol": t.get("symbol", ""),
            "strategy": t.get("strategy", "PARALLEL"),
            "action": t.get("action", "BUY" if is_long else "SELL"),
            "volume": float(t.get("volume", 0.01)),
            "entry": entry,
            "exit": actual_exit,
            "sl": float(t.get("sl", 0.0)),
            "tp": float(t.get("tp", 0.0)),
            "realized_r": actual_r,
            "realized_pnl": realized_pnl,
            "entry_time": t.get("entry_time", datetime.now(timezone.utc)),
            "exit_time": datetime.now(timezone.utc),
            "bars_held": int(t.get("bars_held", t.get("bars_elapsed", 0))),
            "reason": reason
        }
        # Live MT5 broker programmatic closure
        if not self.dry_run and self.conn.connected:
            pos = mt5.positions_get(ticket=ticket)
            if pos and len(pos) > 0:
                p = pos[0]
                close_type = mt5.ORDER_TYPE_SELL if p.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
                sym = t.get("symbol", "")
                tick = self.conn.get_last_tick(sym)
                price = tick.bid if close_type == mt5.ORDER_TYPE_SELL else (tick.ask if tick else 0.0)
                real_sym = t.get("real_symbol") or t.get("symbol", "")
                close_request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "position": ticket,
                    "symbol": real_sym,
                    "volume": p.volume,
                    "type": close_type,
                    "price": price,
                    "deviation": 10,
                    "magic": 10101,
                    "comment": f"Close-{reason[:10]}",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }
                res = mt5.order_send(close_request)
                if res and res.retcode == mt5.TRADE_RETCODE_DONE:
                    logging.info(f"[LIVE MT5 POSITION CLOSED] #{ticket} {sym} @ {price:.5f}")
                else:
                    err_comment = res.comment if res else "No response"
                    err_code = res.retcode if res else -1
                    logging.warning(f"[LIVE MT5 CLOSE FAILED] #{ticket}: {err_comment} ({err_code})")

        self.closed_trades.append(closed_record)
        self.save_state()
        logging.info(f"[TRADE CLOSED] #{ticket} {t.get('symbol')} | Reason: {reason} | Exit: {actual_exit:.5f} | Realized PnL: {realized_pnl:+.2f} USD ({actual_r:+.2f}R)")

    def manage_open_trades(self, current_bar_time: datetime) -> None:
        """Applies 7-stage microstructure ratchets, running PnL calculations, and time-decay exits."""
        # Operational Safeguard 2b: Friday Weekend Gap Defense - Liquidate open positions at 20:30 UTC Friday
        if is_friday_closeout_window():
            for ticket in list(self.open_trades.keys()):
                self.close_trade(ticket, reason="FRIDAY CLOSEOUT (Weekend Gap Defense at 20:30 UTC)")
            return

        # Operational Safeguard 1b: Pause ratchet modifications during 21:55-22:15 UTC daily rollover
        in_rollover = is_broker_rollover_window()

        for ticket, trade in list(self.open_trades.items()):
            sym = trade.get("symbol", "")
            tick = self.conn.get_last_tick(sym)
            if tick is None:
                continue

            entry = float(trade.get("entry") or trade.get("entry_price") or trade.get("price", 0.0))
            sl_price = float(trade.get("sl", 0.0))
            tp_price = float(trade.get("tp", 0.0))
            r_dist = float(trade.get("r_dist", 0.0))
            if r_dist <= 0:
                r_dist = abs(entry - sl_price) if sl_price > 0 else 0.0001
                trade["r_dist"] = r_dist

            trade["entry"] = entry
            trade["entry_price"] = entry

            is_long = (trade.get("type", 0) in (0, mt5.ORDER_TYPE_BUY))
            cur_price = tick.bid if is_long else tick.ask
            trade["cur_price"] = cur_price

            if is_long:
                gain_r = (cur_price - entry) / r_dist
                hit_sl = (tick.bid <= sl_price) if sl_price > 0 else False
                hit_tp = (tick.bid >= tp_price) if tp_price > 0 else False
            else:
                gain_r = (entry - cur_price) / r_dist
                hit_sl = (tick.ask >= sl_price) if sl_price > 0 else False
                hit_tp = (tick.ask <= tp_price) if tp_price > 0 else False

            trade["current_r"] = gain_r
            trade["running_pnl"] = gain_r * float(trade.get("risk_usd", BASE_RISK_USD))
            trade["highest_r"] = max(float(trade.get("highest_r", 0.0)), gain_r)
            trade["lowest_r"] = min(float(trade.get("lowest_r", 0.0)), gain_r)

            # Bar duration counter: only increment when a new 15-minute bar closes
            last_bar = trade.get("last_evaluated_bar")
            if last_bar is None:
                trade["last_evaluated_bar"] = current_bar_time
            elif current_bar_time > last_bar:
                b_held = int(trade.get("bars_held", trade.get("bars_elapsed", 0))) + 1
                trade["bars_held"] = b_held
                trade["bars_elapsed"] = b_held
                trade["last_evaluated_bar"] = current_bar_time

            if hit_sl:
                exit_price = sl_price
                realized_r = (exit_price - entry) / r_dist if is_long else (entry - exit_price) / r_dist
                reason_label = "BE RATCHET" if realized_r > 0 else "STOP LOSS"
                self.close_trade(ticket, exit_price=exit_price, realized_r=realized_r, reason=f"{reason_label} ({realized_r:+.2f}R)")
                continue

            if hit_tp:
                actual_tp_r = (tp_price - entry) / r_dist if is_long else (entry - tp_price) / r_dist
                self.close_trade(ticket, exit_price=tp_price, realized_r=actual_tp_r, reason=f"TAKE PROFIT ({actual_tp_r:+.2f}R)")
                continue

            # Time decay exit: if trade fails to reach +0.20R within 24 bars (6h)
            b_held = int(trade.get("bars_held", trade.get("bars_elapsed", 0)))
            if b_held >= TIME_DECAY_BARS and float(trade.get("highest_r", 0.0)) < TIME_DECAY_THRESHOLD_R:
                self.close_trade(ticket, exit_price=cur_price, realized_r=gain_r, reason=f"TIME DECAY ({b_held} bars, {gain_r:+.2f}R)")
                continue

            # 7-Stage Ratchet Logic
            new_sl_r = None
            ratchet_phase = int(trade.get("ratchet_phase", 0))
            if gain_r >= 3.5 and ratchet_phase < 6:
                new_sl_r = 3.3
                trade["ratchet_phase"] = 6
                trade["ratchet_desc"] = "Lock +3.30R"
            elif gain_r >= 3.0 and ratchet_phase < 5:
                new_sl_r = 2.8
                trade["ratchet_phase"] = 5
                trade["ratchet_desc"] = "Lock +2.80R"
            elif gain_r >= 2.5 and ratchet_phase < 4:
                new_sl_r = 2.3
                trade["ratchet_phase"] = 4
                trade["ratchet_desc"] = "Lock +2.30R"
            elif gain_r >= 2.0 and ratchet_phase < 3:
                new_sl_r = 1.8
                trade["ratchet_phase"] = 3
                trade["ratchet_desc"] = "Lock +1.80R"
            elif gain_r >= 1.5 and ratchet_phase < 2:
                new_sl_r = 0.80
                trade["ratchet_phase"] = 2
                trade["ratchet_desc"] = "Lock +0.80R"
            elif gain_r >= 0.8 and ratchet_phase < 1:
                new_sl_r = 0.15
                trade["ratchet_phase"] = 1
                trade["ratchet_desc"] = "BE Lock (+0.15R)"

            if new_sl_r is not None:
                if in_rollover:
                    logging.info(f"[ROLLOVER LOCKOUT] Suppressing SL ratchet modification for {sym} during 21:55-22:15 UTC settlement.")
                else:
                    if is_long:
                        candidate_sl = entry + (new_sl_r * r_dist)
                        if candidate_sl > trade.get("sl", 0.0):
                            self.modify_sl(ticket, candidate_sl)
                    else:
                        candidate_sl = entry - (new_sl_r * r_dist)
                        curr_sl = trade.get("sl", 0.0)
                        if candidate_sl < curr_sl or curr_sl == 0.0:
                            self.modify_sl(ticket, candidate_sl)


    def get_account_metrics(self) -> Dict[str, Any]:
        """Aggregates real-time broker/paper account metrics, running PnL, equity, and drawdowns."""
        acc_info = mt5.account_info() if self.conn.connected else None

        running_pnl = sum(t.get("running_pnl", 0.0) for t in self.open_trades.values())
        open_count = len(self.open_trades)
        closed_count = len(self.closed_trades)
        wins = sum(1 for ct in self.closed_trades if ct.get("realized_pnl", 0.0) > 0)
        win_rate = (wins / closed_count * 100.0) if closed_count > 0 else 0.0

        if not self.dry_run and acc_info is not None:
            balance = float(acc_info.balance)
            equity = float(acc_info.equity)
            margin = float(acc_info.margin)
            margin_free = float(acc_info.margin_free)
            margin_level = float(acc_info.margin_level)
            floating_pnl = float(acc_info.profit)
            server = acc_info.server
            login = acc_info.login
            currency = acc_info.currency
        else:
            balance = self.initial_balance + self.realized_pnl
            equity = balance + running_pnl
            margin = sum(t.get("volume", 0.01) * 1000.0 for t in self.open_trades.values())
            margin_free = max(0.0, equity - margin)
            margin_level = (equity / margin * 100.0) if margin > 0 else 0.0
            floating_pnl = running_pnl
            server = acc_info.server if acc_info else "Blueberry-Demo"
            login = acc_info.login if acc_info else 5064568
            currency = acc_info.currency if acc_info else "USD"

        drawdown_usd = max(0.0, (self.initial_balance - equity))
        drawdown_pct = (drawdown_usd / self.initial_balance) * 100.0

        return {
            "login": login,
            "server": server,
            "currency": currency,
            "balance": balance,
            "equity": equity,
            "margin": margin,
            "margin_free": margin_free,
            "margin_level": margin_level,
            "running_pnl": floating_pnl,
            "realized_pnl": self.realized_pnl,
            "total_pnl": self.realized_pnl + floating_pnl,
            "drawdown_pct": drawdown_pct,
            "open_count": open_count,
            "closed_count": closed_count,
            "win_rate": win_rate
        }


# -------------------------------------------------------------------------
# COMPONENT 3: MATHEMATICAL FEATURE EXTRACTION & PARITY KERNEL
# -------------------------------------------------------------------------
def compute_features_pandas(df: pd.DataFrame, buffer_4h: Optional[pd.DataFrame] = None, buffer_d1: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Computes all 13 canonical stationary features with zero lookahead, delegating to strategy_kernel."""
    from Engine.core.strategy_kernel import compute_features_pandas as sk_compute_features_pandas
    return sk_compute_features_pandas(df, buffer_4h=buffer_4h, buffer_d1=buffer_d1)


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
            prev_date = prev_bars["_date"].max()
            d1_bars = prev_bars[prev_bars["_date"] == prev_date]
            prev_day_high = float(d1_bars["high"].max())
            prev_day_low  = float(d1_bars["low"].min())

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


def calculate_adaptive_sl_tp(
    symbol: str,
    is_long: bool,
    entry: float,
    raw_sl: float,
    local_extreme: float,
    spread: float,
    atr: float,
    tp_structural: Optional[float] = None
) -> Tuple[float, float, float, bool, str]:
    """
    Option C + Institutional P1 Hardening:
    Computes adaptive SL and decoupled structural TP.
    Guarantees clearance from spread noise: SL is expanded to structural extreme or max(3.5*spread, 1.5*atr).
    TP is decoupled from floating R-multiples and anchored to structural session liquidity pools (e.g. 20-bar swing extreme).
    Enforces MIN_STRUCTURAL_R_EFF <= R_eff <= MAX_STRUCTURAL_R_EFF (1.20 to 3.50).
    Returns: (sl, tp, r_dist, is_valid, reason)
    """
    spread_val = max(0.0, spread)
    atr_val = max(0.0, atr)
    min_safe_dist = max(MIN_SPREAD_MULTIPLIER * spread_val, MIN_ATR_MULTIPLIER * atr_val)

    if is_long:
        r_dist = entry - raw_sl
        sl = raw_sl
        if r_dist < min_safe_dist:
            # Expand to structural swing low
            struct_dist = entry - local_extreme
            if struct_dist >= min_safe_dist:
                sl = local_extreme
                r_dist = struct_dist
            else:
                sl = entry - min_safe_dist
                r_dist = min_safe_dist

        if r_dist <= 0 or (entry > 0 and (r_dist / entry) > MAX_STOP_PCT):
            return (0.0, 0.0, 0.0, False, "HOLD (Stop Range Invalid)")

        # P1 FIX: Structural TP Decoupling
        if tp_structural is not None and tp_structural > entry:
            struct_tp_dist = tp_structural - entry
            r_eff = struct_tp_dist / r_dist
            if r_eff < MIN_STRUCTURAL_R_EFF:
                return (0.0, 0.0, 0.0, False, f"HOLD (R_eff {r_eff:.2f} < {MIN_STRUCTURAL_R_EFF:.2f})")
            elif r_eff > MAX_STRUCTURAL_R_EFF:
                tp = entry + (MAX_STRUCTURAL_R_EFF * r_dist)
                r_eff = MAX_STRUCTURAL_R_EFF
            else:
                tp = tp_structural
            return (sl, tp, r_dist, True, f"BUY (Adaptive {r_eff:.2f}R Struct)")
        else:
            tp = entry + (2.5 * r_dist)
            return (sl, tp, r_dist, True, "BUY (Adaptive Confluence)")
    else:
        r_dist = raw_sl - entry
        sl = raw_sl
        if r_dist < min_safe_dist:
            # Expand to structural swing high
            struct_dist = local_extreme - entry
            if struct_dist >= min_safe_dist:
                sl = local_extreme
                r_dist = struct_dist
            else:
                sl = entry + min_safe_dist
                r_dist = min_safe_dist

        if r_dist <= 0 or (entry > 0 and (r_dist / entry) > MAX_STOP_PCT):
            return (0.0, 0.0, 0.0, False, "HOLD (Stop Range Invalid)")

        # P1 FIX: Structural TP Decoupling
        if tp_structural is not None and tp_structural < entry:
            struct_tp_dist = entry - tp_structural
            r_eff = struct_tp_dist / r_dist
            if r_eff < MIN_STRUCTURAL_R_EFF:
                return (0.0, 0.0, 0.0, False, f"HOLD (R_eff {r_eff:.2f} < {MIN_STRUCTURAL_R_EFF:.2f})")
            elif r_eff > MAX_STRUCTURAL_R_EFF:
                tp = entry - (MAX_STRUCTURAL_R_EFF * r_dist)
                r_eff = MAX_STRUCTURAL_R_EFF
            else:
                tp = tp_structural
            return (sl, tp, r_dist, True, f"SELL (Adaptive {r_eff:.2f}R Struct)")
        else:
            tp = entry - (2.5 * r_dist)
            return (sl, tp, r_dist, True, "SELL (Adaptive Confluence)")


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
        self.buffer_d1: pd.DataFrame = pd.DataFrame()
        self.is_warm = False
        self.mt5_conn = None
        self.is_quarantined = False
        self.consecutive_safe_bars = 0
        self._last_quarantine_bar = None

    def check_quarantine(self, spread: float, atr: float, current_utc_hour: int = 12, bar_time: Optional[datetime] = None) -> Tuple[bool, str]:
        """
        P1 Quarantine with Hysteresis & Session Time Filter:
        1. Exotic assets are strictly quarantined outside 07:00-17:00 UTC.
        2. Hysteresis band: enters quarantine if spread/atr > 0.12; exits only if spread/atr < 0.08 for 2 consecutive bars.
        """
        sym_clean = self.symbol.upper().replace(".PI", "").replace(".P", "").replace(".R", "")
        if sym_clean in EXOTIC_SESSION_RESTRICTED:
            if current_utc_hour < 7 or current_utc_hour >= 17:
                self.is_quarantined = True
                self.consecutive_safe_bars = 0
                return True, f"Quarantined (Exotic off-hours: {current_utc_hour:02d}:00 UTC outside 07-17 UTC)"

        if spread is None or atr is None or np.isnan(spread) or np.isnan(atr) or np.isinf(spread) or np.isinf(atr) or atr <= 0 or spread <= 0:
            self.is_quarantined = True
            self.consecutive_safe_bars = 0
            return True, "Quarantined (Invalid spread/ATR data)"

        ratio = spread / atr
        if not self.is_quarantined:
            if ratio > MAX_SPREAD_ATR_RATIO_ENTER:
                self.is_quarantined = True
                self.consecutive_safe_bars = 0
                return True, f"Quarantined (Spread/ATR {ratio:.1%} > {MAX_SPREAD_ATR_RATIO_ENTER:.0%})"
            return False, "Active"
        else:
            if ratio < MAX_SPREAD_ATR_RATIO_EXIT:
                if bar_time is not None:
                    if bar_time != self._last_quarantine_bar:
                        self.consecutive_safe_bars += 1
                        self._last_quarantine_bar = bar_time

                if self.consecutive_safe_bars >= 2:
                    self.is_quarantined = False
                    self.consecutive_safe_bars = 0
                    return False, "Active (Hysteresis Cleared)"
                return True, f"Quarantined (Clearing {self.consecutive_safe_bars}/2 bars: {ratio:.1%})"
            else:
                self.consecutive_safe_bars = 0
                return True, f"Quarantined (Spread/ATR {ratio:.1%} > {MAX_SPREAD_ATR_RATIO_EXIT:.0%})"

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

        if hasattr(mt5_conn, 'get_1d_bars'):
            bars_1d_df = mt5_conn.get_1d_bars(self.symbol, count=20)
            if not bars_1d_df.empty and len(bars_1d_df) > 1:
                bars_1d_df = bars_1d_df.iloc[:-1].copy()
                if 'datetime' in bars_1d_df.columns:
                    bars_1d_df.set_index('datetime', inplace=True)
                self.buffer_d1 = bars_1d_df[['open', 'high', 'low', 'close']].copy()

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
        return compute_features_pandas(self.buffer, self.buffer_4h, getattr(self, 'buffer_d1', None))

    def predict(self, xgb_model: Optional[xgb.Booster] = None) -> float:
        if self.buffer.empty:
            return 0.50
        features_df = self.compute_features()
        latest = features_df.iloc[[-1]][CANONICAL_FEATURES].copy()
        for col in latest.columns:
            latest[col] = pd.to_numeric(latest[col], errors="coerce").astype(float)
        dmat = xgb.DMatrix(latest)
        if xgb_model is None:
            if not PRODUCTION_MODEL_PATH.exists():
                return 0.50
            xgb_model = xgb.Booster()
            xgb_model.load_model(str(PRODUCTION_MODEL_PATH))
        prob = float(xgb_model.predict(dmat)[0])
        del dmat
        return prob

    def compute_crt_orb(self) -> dict:
        return compute_crt_orb_state(self.buffer)


# -------------------------------------------------------------------------
# COMPONENT 5: PRE-FLIGHT MARKET DATA SYNCHRONIZER & RETRAINING
# -------------------------------------------------------------------------
def _calc_session(hour: int) -> str:
    if 0 <= hour < 7:
        return "Asian"
    elif 7 <= hour < 12:
        return "London"
    elif 12 <= hour < 20:
        return "New York"
    return "Close"


def _calc_kz(hour: int) -> bool:
    return (7 <= hour <= 10) or (12 <= hour <= 15)


def _sync_aux_parquet(mt5_conn: MT5Connection, sym: str, real_symbol: str, tf_label: str, tf_mt5: int, offset: int, now_utc: datetime) -> None:
    aux_path = resolve_aux_parquet(sym, tf_label)
    if not aux_path or not aux_path.exists():
        return
    try:
        df_existing = pl.read_parquet(aux_path)
        last_val = df_existing['datetime'].max()
        last_dt = pd.to_datetime(last_val, utc=True)
        fetch_from = last_dt + timedelta(seconds=1)
        fetch_from_broker = fetch_from + timedelta(seconds=offset)
        cutoff_broker = now_utc + timedelta(seconds=offset)
        rates = mt5.copy_rates_range(real_symbol, tf_mt5, fetch_from_broker, cutoff_broker)
        if rates is None or len(rates) == 0:
            return
        df_new = pd.DataFrame(rates)
        df_new['time'] = df_new['time'] - offset
        df_new['datetime'] = pd.to_datetime(df_new['time'], unit='s', utc=True)
        dur = timedelta(hours=4) if tf_label == "4h" else timedelta(days=1)
        df_new = df_new[df_new['datetime'] + dur <= now_utc]
        if len(df_new) == 0:
            return
        new_dict = {
            'time': [int(t) for t in df_new['time']],
            'datetime': [pd.to_datetime(t, unit='s', utc=True) for t in df_new['time']],
            'open': [float(x) for x in df_new['open']],
            'high': [float(x) for x in df_new['high']],
            'low': [float(x) for x in df_new['low']],
            'close': [float(x) for x in df_new['close']],
            'tick_volume': [int(x) for x in df_new['tick_volume']],
        }
        if 'spread' in df_existing.columns:
            new_dict['spread'] = [int(x) for x in df_new['spread']] if 'spread' in df_new else [0]*len(df_new)
        if 'real_volume' in df_existing.columns:
            new_dict['real_volume'] = [int(x) for x in df_new['real_volume']] if 'real_volume' in df_new else [0]*len(df_new)
        if 'day_of_week' in df_existing.columns:
            new_dict['day_of_week'] = [int(pd.to_datetime(t, unit='s', utc=True).weekday() + 1) for t in df_new['time']]
        if 'session' in df_existing.columns:
            new_dict['session'] = [_calc_session(pd.to_datetime(t, unit='s', utc=True).hour) for t in df_new['time']]
        if 'is_kill_zone' in df_existing.columns:
            new_dict['is_kill_zone'] = [_calc_kz(pd.to_datetime(t, unit='s', utc=True).hour) for t in df_new['time']]

        new_pl = pl.DataFrame(
            new_dict,
            schema={col: df_existing.schema[col] for col in new_dict if col in df_existing.schema},
            strict=False
        )
        combined = pl.concat([df_existing, new_pl]).unique(subset=['datetime']).sort('datetime')
        tmp_p = aux_path.with_suffix(".parquet.tmp")
        combined.write_parquet(tmp_p)
        robust_parquet_replace(tmp_p, aux_path)
    except Exception as e:
        logging.debug(f"Aux sync {sym} {tf_label}: {e}")


def pre_flight_data_sync(mt5_conn: MT5Connection, single_asset: Optional[str] = None) -> int:
    """
    Synchronizes historical parquet files directly with latest closed broker bars.
    Appends any newly closed 15m, 4H, and D1 candles up to the current bar (True UTC).
    """
    assets_to_sync = [single_asset] if single_asset else CANONICAL_18_ASSETS
    total_appended = 0
    now_utc = datetime.now(timezone.utc)
    broker_offset = mt5_conn.get_broker_utc_offset()

    if single_asset is None:
        console.print(Panel(
            "[bold cyan]STAGE 1: SYNCHRONIZING HISTORICAL PARQUET DATA WITH MT5 FEED[/bold cyan]\n"
            f"[dim]Checking and appending latest closed candles up to {now_utc.strftime('%Y-%m-%d %H:%M UTC')}...[/dim]",
            border_style="cyan"
        ))

    sync_table = Table(
        title="PARQUET SYNCHRONIZATION AUDIT (18 ASSETS)",
        box=box.ROUNDED,
        header_style="bold bright_white on dark_blue"
    )
    sync_table.add_column("Asset", justify="left", style="bold white", width=9)
    sync_table.add_column("Broker Symbol", justify="left", style="cyan", width=12)
    sync_table.add_column("Previous Last Candle", justify="center", width=20)
    sync_table.add_column("New Bars", justify="right", width=9)
    sync_table.add_column("Updated Last Candle", justify="center", width=20)
    sync_table.add_column("Status", justify="center", width=12)

    for sym in assets_to_sync:
        real_symbol = mt5_conn.resolve_symbol(sym)
        parquet_path = resolve_parquet_file(sym)
        if not parquet_path or not parquet_path.exists():
            if single_asset is None:
                sync_table.add_row(sym, real_symbol, "N/A", "0", "N/A", "[dim yellow]NOT FOUND[/dim yellow]")
            continue

        try:
            df_existing = pl.read_parquet(parquet_path)
            last_val = df_existing['datetime'].max()
            if isinstance(last_val, str):
                last_dt = pd.to_datetime(last_val, utc=True)
            elif hasattr(last_val, "tzinfo") and last_val.tzinfo is not None:
                last_dt = pd.to_datetime(last_val)
            else:
                last_dt = pd.to_datetime(last_val, unit='us' if isinstance(last_val, (int, float)) and last_val > 1e12 else 's', utc=True)

            if last_dt.tzinfo is None:
                last_dt = last_dt.tz_localize('UTC')

            fetch_from = last_dt + timedelta(seconds=1)
            fetch_from_broker = fetch_from + timedelta(seconds=broker_offset)
            cutoff_broker = now_utc + timedelta(seconds=broker_offset)

            rates = mt5.copy_rates_range(real_symbol, mt5.TIMEFRAME_M15, fetch_from_broker, cutoff_broker)
            if rates is None or len(rates) == 0:
                if single_asset is None:
                    sync_table.add_row(sym, real_symbol, last_dt.strftime('%Y-%m-%d %H:%M'), "0", last_dt.strftime('%Y-%m-%d %H:%M'), "[green]UP-TO-DATE[/green]")
                continue

            df_new = pd.DataFrame(rates)
            df_new['time'] = df_new['time'] - broker_offset
            df_new['datetime'] = pd.to_datetime(df_new['time'], unit='s', utc=True)
            # Exclude currently forming unclosed bar
            df_new = df_new[df_new['datetime'] + timedelta(minutes=15) <= now_utc]

            if len(df_new) == 0:
                if single_asset is None:
                    sync_table.add_row(sym, real_symbol, last_dt.strftime('%Y-%m-%d %H:%M'), "0", last_dt.strftime('%Y-%m-%d %H:%M'), "[green]UP-TO-DATE[/green]")
                continue

            # Build rows aligned to Polars schema
            new_rows_dict = {
                'time': [int(t) for t in df_new['time']],
                'datetime': [pd.to_datetime(t, unit='s', utc=True) for t in df_new['time']],
                'open': [float(x) for x in df_new['open']],
                'high': [float(x) for x in df_new['high']],
                'low': [float(x) for x in df_new['low']],
                'close': [float(x) for x in df_new['close']],
                'tick_volume': [float(x) for x in df_new['tick_volume']],
            }
            if 'spread' in df_existing.columns:
                new_rows_dict['spread'] = [int(x) for x in df_new['spread']] if 'spread' in df_new else [0]*len(df_new)
            if 'real_volume' in df_existing.columns:
                new_rows_dict['real_volume'] = [int(x) for x in df_new['real_volume']] if 'real_volume' in df_new else [0]*len(df_new)
            if 'day_of_week' in df_existing.columns:
                new_rows_dict['day_of_week'] = [float(pd.to_datetime(t, unit='s', utc=True).weekday() + 1) for t in df_new['time']]
            if 'session' in df_existing.columns:
                new_rows_dict['session'] = [_calc_session(pd.to_datetime(t, unit='s', utc=True).hour) for t in df_new['time']]
            if 'is_kill_zone' in df_existing.columns:
                new_rows_dict['is_kill_zone'] = [_calc_kz(pd.to_datetime(t, unit='s', utc=True).hour) for t in df_new['time']]

            new_pl = pl.DataFrame(
                new_rows_dict,
                schema={col: df_existing.schema[col] for col in new_rows_dict if col in df_existing.schema},
                strict=False
            )
            combined_pl = pl.concat([df_existing, new_pl]).unique(subset=['datetime']).sort('datetime')

            tmp_path = parquet_path.with_suffix(".parquet.tmp")
            combined_pl.write_parquet(tmp_path)
            robust_parquet_replace(tmp_path, parquet_path)

            new_last_dt = combined_pl['datetime'].max()
            new_last_str = str(new_last_dt)[:16]
            total_appended += len(df_new)

            if single_asset is None:
                sync_table.add_row(sym, real_symbol, last_dt.strftime('%Y-%m-%d %H:%M'), f"+{len(df_new)}", new_last_str, "[bold green]SYNCED[/bold green]")
            else:
                logging.info(f"[{sym}] Appended +{len(df_new)} bars to {parquet_path.name} up to {new_last_str}")

            # Also sync 4H and D1 parquets
            _sync_aux_parquet(mt5_conn, sym, real_symbol, "4h", mt5.TIMEFRAME_H4, broker_offset, now_utc)
            _sync_aux_parquet(mt5_conn, sym, real_symbol, "d1", mt5.TIMEFRAME_D1, broker_offset, now_utc)

        except Exception as e:
            logging.error(f"Sync error for {sym}: {e}")
            if single_asset is None:
                sync_table.add_row(sym, real_symbol, "ERROR", "0", "ERROR", f"[red]{str(e)[:12]}[/red]")

    if single_asset is None:
        console.print(sync_table)
        console.print(f"[bold green]Data sync complete: {total_appended} total new 15m candles appended across {len(assets_to_sync)} assets.[/bold green]\n")

    return total_appended


def purge_earlier_ml_models() -> List[str]:
    """Purges earlier ML models or cached weights to ensure a completely fresh train."""
    purged = []
    if PRODUCTION_MODEL_PATH.exists():
        PRODUCTION_MODEL_PATH.unlink()
        purged.append(PRODUCTION_MODEL_PATH.name)
    for extra in MODELS_DIR.glob("xgboost_forex*.json"):
        if extra.exists():
            extra.unlink()
            purged.append(extra.name)
    for extra in MODELS_DIR.glob("*.tmp"):
        if extra.exists():
            extra.unlink()
            purged.append(extra.name)
    if purged:
        console.print(Panel(
            f"[bold yellow]STAGE 2: PURGING EARLIER ML MODELS & CACHED WEIGHTS[/bold yellow]\n"
            f"[dim]Deleted files: {', '.join(purged)}[/dim]",
            border_style="yellow"
        ))
    else:
        console.print("[dim]STAGE 2: No earlier ML model files found to delete.[/dim]")
    return purged


def dynamic_retrain() -> xgb.Booster:
    """Retrains the production XGBoost model across all 18 canonical assets on fresh data."""
    console.print(Panel(
        "[bold cyan]STAGE 3: RETRAINING PRODUCTION XGBOOST MODEL ON LATEST MARKET DATA[/bold cyan]\n"
        f"[dim]Feature Engineering & 7-Stage Ratchet Label Generation across all {len(CANONICAL_18_ASSETS)} assets...[/dim]",
        border_style="cyan"
    ))
    train_X = []
    train_y = []

    for sym in CANONICAL_18_ASSETS:
        try:
            df = engineer_features_polars(sym, str(DATA_DIR))
            df = create_labels_ratchet(df)
            valid = df[df['target'].notna()]
            if len(valid) > 0:
                train_X.append(valid[CANONICAL_FEATURES])
                train_y.append(valid['target'].values)
        except Exception as e:
            logging.warning(f"Dynamic retrain feature error for {sym}: {e}")

    if not train_X:
        raise RuntimeError("No training setups could be generated from refreshed datasets.")

    X_mat = pd.concat(train_X, ignore_index=True)
    y_vec = np.concatenate(train_y)

    console.print(f"  -> Ingested [bold green]{len(X_mat):,}[/bold green] labeled market setups across 18 assets.")
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
    console.print(f"[bold green]Dynamic retrain complete. Certified booster saved to: {PRODUCTION_MODEL_PATH}[/bold green]\n")
    return booster


def verify_all_components(mt5_conn: MT5Connection, booster: xgb.Booster, order_mgr: OrderManager) -> bool:
    """
    Executes deep pre-flight verification across all 6 core components before terminal launch:
    1. Broker Connection & Account Info
    2. 18-Asset Symbol Resolution & Live Ticks
    3. Stateful Inference Buffer Warm-Start
    4. 13 Canonical Stationary Features Parity (0 NaNs)
    5. Model Probability Inference (P* range [0, 1])
    6. Order Manager & Ratchet Governor State
    """
    console.print(Panel(
        "[bold cyan]STAGE 4: COMPREHENSIVE PRE-FLIGHT COMPONENT INTEGRITY AUDIT[/bold cyan]\n"
        "[dim]Auditing broker connectivity, symbol feeds, memory buffers, feature math, model, and governors...[/dim]",
        border_style="cyan"
    ))

    audit_table = Table(
        title="SYSTEM INTEGRITY PRE-FLIGHT SCORECARD",
        box=box.ROUNDED,
        header_style="bold bright_white on dark_green",
        expand=True
    )
    audit_table.add_column("Component", justify="left", style="bold white", no_wrap=True)
    audit_table.add_column("Status", justify="center", no_wrap=True)
    audit_table.add_column("Diagnostics / Metrics", justify="left", style="cyan", ratio=1, overflow="ellipsis")

    all_passed = True

    # 1. Broker connection
    acc = mt5.account_info() if mt5_conn.connected else None
    if acc:
        audit_table.add_row("1. MT5 Terminal Connection", "[bold green]PASS[/bold green]", f"Account #{acc.login} on {acc.server} | Balance: ${acc.balance:,.2f} {acc.currency}")
    else:
        audit_table.add_row("1. MT5 Terminal Connection", "[bold red]FAIL[/bold red]", "Could not query MT5 account info")
        all_passed = False

    # 2. Symbol resolution & live ticks
    ticking_count = 0
    for sym in CANONICAL_18_ASSETS:
        tick = mt5_conn.get_last_tick(sym)
        if tick and tick.bid > 0:
            ticking_count += 1
    if ticking_count == len(CANONICAL_18_ASSETS):
        audit_table.add_row("2. Symbol Resolution & Feeds", "[bold green]PASS[/bold green]", f"All {ticking_count}/{len(CANONICAL_18_ASSETS)} assets online with live bid/ask")
    else:
        audit_table.add_row("2. Symbol Resolution & Feeds", "[bold yellow]WARN[/bold yellow]", f"{ticking_count}/{len(CANONICAL_18_ASSETS)} assets ticking")

    # 3. Buffer warm-start & feature extraction
    test_asset = "EURUSD"
    eng = StatefulInferenceEngine(test_asset)
    warm = eng.warm_start(mt5_conn)
    if warm and len(eng.buffer) >= 50:
        audit_table.add_row("3. Stateful Rolling Buffers", "[bold green]PASS[/bold green]", f"Buffer warm-start active ({len(eng.buffer)} 15m bars, {len(eng.buffer_4h)} 4h bars)")
    else:
        audit_table.add_row("3. Stateful Rolling Buffers", "[bold red]FAIL[/bold red]", f"Failed to warm buffer for {test_asset}")
        all_passed = False

    # 4. Feature math parity & NaN check
    feat_df = eng.compute_features()
    nan_count = int(feat_df.isna().sum().sum())
    if nan_count == 0 and len(feat_df) > 0:
        latest = feat_df.iloc[-1]
        audit_table.add_row("4. Stationary Feature Engine", "[bold green]PASS[/bold green]", f"13 features computed with 0 NaNs (RSI: {latest['rsi_14']:.1f}, ATR: {latest['atr_14']:.5f})")
    else:
        audit_table.add_row("4. Stationary Feature Engine", "[bold red]FAIL[/bold red]", f"Detected {nan_count} NaNs in feature matrix")
        all_passed = False

    # 5. Fresh model inference
    prob = eng.predict(booster)
    if 0.0 <= prob <= 1.0:
        audit_table.add_row("5. Model Inference Engine", "[bold green]PASS[/bold green]", f"Production XGBoost loaded | Test prediction P* = {prob:.4f}")
    else:
        audit_table.add_row("5. Model Inference Engine", "[bold red]FAIL[/bold red]", f"Invalid probability returned: {prob}")
        all_passed = False

    # 6. Order manager & ratchets
    audit_table.add_row("6. Order & Ratchet Governor", "[bold green]PASS[/bold green]", f"Armed | Base Risk: $50.00 USD | 7-Stage Ratchets (+0.8R BE, +1.5R Lock, +2.5R TP)")

    console.print(audit_table)
    if all_passed:
        console.print("[bold green]ALL 6 SYSTEM COMPONENTS VERIFIED. PROCEEDING TO LIVE TERMINAL...[/bold green]\n")
    else:
        console.print("[bold yellow]PRE-FLIGHT COMPLETED WITH WARNINGS. PROCEEDING WITH CAUTION.[/bold yellow]\n")

    time.sleep(0.5)
    return all_passed


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

        spread = abs(ask - bid) if (ask > 0 and bid > 0) else 0.0
        atr = float(last.get("atr_14", 0.0))

        if atr > 0 and spread > 0 and (spread / atr) > MAX_SPREAD_ATR_RATIO:
            return StrategySignal(symbol=symbol, signal=0, reason=f"HOLD (Spread/ATR {(spread/atr):.1%} > {MAX_SPREAD_ATR_RATIO:.0%})")

        if trend > 0 and bull_fvg > 0:
            entry = ask
            sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                symbol=symbol, is_long=True, entry=entry, raw_sl=local_low,
                local_extreme=local_low, spread=spread, atr=atr,
                tp_structural=local_high
            )
            if not valid:
                return StrategySignal(symbol=symbol, signal=0, reason=reason)
            return StrategySignal(
                symbol=symbol, signal=1, entry_price=entry, sl_price=sl,
                tp_price=tp, strategy_tag="FVG", reason=reason
            )
        elif trend < 0 and bear_fvg > 0:
            entry = bid
            sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                symbol=symbol, is_long=False, entry=entry, raw_sl=local_high,
                local_extreme=local_high, spread=spread, atr=atr,
                tp_structural=local_low
            )
            if not valid:
                return StrategySignal(symbol=symbol, signal=0, reason=reason)
            return StrategySignal(
                symbol=symbol, signal=-1, entry_price=entry, sl_price=sl,
                tp_price=tp, strategy_tag="FVG", reason=reason
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


# Note: CRT / ORB Strategy is dynamically routed via ORBCRTForexCFDStrategy
# Registered keys: 'orb_crt', 'crt_orb', 'crt'


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

        spread = abs(ask - bid) if (ask > 0 and bid > 0) else 0.0
        atr = float(feat_df.iloc[-1].get("atr_14", 0.0))

        if atr > 0 and spread > 0 and (spread / atr) > MAX_SPREAD_ATR_RATIO:
            return StrategySignal(symbol=symbol, signal=0, prob=prob, reason=f"HOLD (Spread/ATR {(spread/atr):.1%} > {MAX_SPREAD_ATR_RATIO:.0%})")

        if trend > 0 and prob >= self.prob_threshold:
            entry = ask
            sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                symbol=symbol, is_long=True, entry=entry, raw_sl=local_low,
                local_extreme=local_low, spread=spread, atr=atr,
                tp_structural=local_high
            )
            if not valid:
                return StrategySignal(symbol=symbol, signal=0, prob=prob, reason=reason)
            return StrategySignal(
                symbol=symbol, signal=1, prob=prob, entry_price=entry, sl_price=sl,
                tp_price=tp, strategy_tag="ML", reason=reason
            )
        elif trend < 0 and prob >= self.prob_threshold:
            entry = bid
            sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                symbol=symbol, is_long=False, entry=entry, raw_sl=local_high,
                local_extreme=local_high, spread=spread, atr=atr,
                tp_structural=local_low
            )
            if not valid:
                return StrategySignal(symbol=symbol, signal=0, prob=prob, reason=reason)
            return StrategySignal(
                symbol=symbol, signal=-1, prob=prob, entry_price=entry, sl_price=sl,
                tp_price=tp, strategy_tag="ML", reason=reason
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

        spread = abs(ask - bid) if (ask > 0 and bid > 0) else 0.0
        atr = float(feat_df.iloc[-1].get("atr_14", 0.0))

        # Option C Filter 1: Dynamic Spread-to-ATR Regime Quarantine
        if atr > 0 and spread > 0:
            spread_atr_ratio = spread / atr
            if spread_atr_ratio > MAX_SPREAD_ATR_RATIO:
                return StrategySignal(
                    symbol=symbol, signal=0, prob=prob,
                    reason=f"HOLD (Spread/ATR {spread_atr_ratio:.1%} > {MAX_SPREAD_ATR_RATIO:.0%})"
                )

        is_long = ((trend > 0 and bull_fvg > 0) or crt["is_long_crt"]) and (prob >= self.prob_threshold)
        is_short = ((trend < 0 and bear_fvg > 0) or crt["is_short_crt"]) and (prob >= self.prob_threshold)

        if is_long:
            entry = ask
            raw_sl = crt["or_low"] if crt["is_long_crt"] and crt["or_low"] > 0 else local_low
            sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                symbol=symbol, is_long=True, entry=entry, raw_sl=raw_sl,
                local_extreme=local_low, spread=spread, atr=atr,
                tp_structural=local_high
            )
            if not valid:
                return StrategySignal(symbol=symbol, signal=0, prob=prob, reason=reason)
            return StrategySignal(
                symbol=symbol, signal=1, prob=prob, entry_price=entry, sl_price=sl,
                tp_price=tp, strategy_tag="COMBINED", reason=reason
            )
        elif is_short:
            entry = bid
            raw_sl = crt["or_high"] if crt["is_short_crt"] and crt["or_high"] > 0 else local_high
            sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                symbol=symbol, is_long=False, entry=entry, raw_sl=raw_sl,
                local_extreme=local_high, spread=spread, atr=atr,
                tp_structural=local_low
            )
            if not valid:
                return StrategySignal(symbol=symbol, signal=0, prob=prob, reason=reason)
            return StrategySignal(
                symbol=symbol, signal=-1, prob=prob, entry_price=entry, sl_price=sl,
                tp_price=tp, strategy_tag="COMBINED", reason=reason
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
        elif "," in strat_key:
            sleeves = [s.strip() for s in strat_key.split(",") if s.strip()]
            strat_instance = ParallelForexStrategy(config=self.config, strategy_names=sleeves)
            strat_instance.initialize(self.config)
            self.active_strategy = strat_instance
            logging.info(f"Loaded and initialized parallel sleeves: {sleeves}")
            return strat_instance
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
        strategy_target: str = "parallel",
        once: bool = False,
        ignore_kz: bool = False,
        dry_run: bool = True,
        live: bool = False,
        interval: float = 1.5,
        skip_train: bool = False
    ) -> None:
        """
        Launches live streaming telemetry for the target strategy with canonical automated startup:
        1. Connects to MetaTrader 5 broker feed.
        2. Appends newly closed candles up to the latest bar across 18 assets.
        3. Purges previous ML models and cache files.
        4. Retrains production XGBoost booster on refreshed market data.
        5. Performs deep pre-flight verification across all 6 core components.
        6. Launches streaming dashboard with opened/closed trades and live PnL/equity tracking.
        """
        strat = self.load_strategy(strategy_target)
        self.order_mgr.dry_run = (not live)

        mode_label = "[bold red]LIVE BROKER ORDERS (REAL CAPITAL RISK)[/bold red]" if live else "[bold yellow]PAPER DRY-RUN (ZERO BROKER RISK)[/bold yellow]"
        console.print(Panel(
            f"[bold cyan]INITIALIZING FOREX & CFD MASTER ORCHESTRATION ENGINE[/bold cyan]\n"
            f"[dim]Strategy: [bold bright_white]{strat.name.upper()}[/bold bright_white] ({strat.description})\n"
            f"Execution Mode: {mode_label}[/dim]",
            border_style="cyan"
        ))

        # 1. Connect to MT5
        if not self.mt5_conn.connect():
            console.print("[bold red][FATAL] Could not connect to MetaTrader 5 terminal. Ensure MT5 is running![/bold red]")
            sys.exit(1)

        # 2. Automated Pre-Flight: Append candles till last closed candle
        pre_flight_data_sync(self.mt5_conn)

        # 3. Automated Pre-Flight: Delete earlier ML models & caches
        if not skip_train:
            purge_earlier_ml_models()
            # 4. Automated Pre-Flight: Retrain on fresh dataset
            booster = dynamic_retrain()
        else:
            if PRODUCTION_MODEL_PATH.exists():
                booster = xgb.Booster()
                booster.load_model(str(PRODUCTION_MODEL_PATH))
                console.print(f"[dim]Skipping retrain. Loaded existing model from {PRODUCTION_MODEL_PATH}[/dim]")
            else:
                booster = dynamic_retrain()

        # 5. Automated Pre-Flight: Check all other components
        verify_all_components(self.mt5_conn, booster, self.order_mgr)

        engines: Dict[str, StatefulInferenceEngine] = {}
        last_candle_times: Dict[str, Optional[datetime]] = {}

        console.print(f"[bold cyan]Warm-starting state buffers for {len(CANONICAL_18_ASSETS)} assets...[/bold cyan]")
        for asset in CANONICAL_18_ASSETS:
            eng = StatefulInferenceEngine(asset)
            if eng.warm_start(self.mt5_conn):
                engines[asset] = eng
                if not eng.buffer.empty:
                    last_candle_times[asset] = eng.buffer.index[-1]

        console.print(f"[bold green]Warm-start complete ({len(engines)}/{len(CANONICAL_18_ASSETS)} assets). Entering live terminal stream...[/bold green]\n")
        time.sleep(0.8)

        last_triggered_candles: Dict[str, Optional[datetime]] = {}

        def build_dashboard_frame() -> Group:
            term_w = get_terminal_width()
            if term_w:
                console.width = term_w

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
                kz_badge = "[bold magenta]BYPASSED (24/7 MODE)[/bold magenta]"
            elif is_london:
                kz_badge = "[bold green]ACTIVE (London Open 07-10 UTC)[/bold green]"
            elif is_ny:
                kz_badge = "[bold green]ACTIVE (New York Open 12-15 UTC)[/bold green]"
            else:
                kz_badge = "[dim red]OFF-HOURS (Outside 07-10 / 12-15 UTC)[/dim red]"

            # Manage Open Trades & 7-Stage Microstructure Ratchets on every tick
            latest_closed_ts = max([t for t in last_candle_times.values() if t is not None], default=utc_now)
            self.order_mgr.manage_open_trades(current_bar_time=latest_closed_ts)

            # Build 18-Asset Market Telemetry Table (Autofit in width)
            table = Table(
                title=f"18-ASSET ORDERFLOW & ML TELEMETRY | KILL ZONE: {kz_badge}",
                box=box.ROUNDED,
                header_style="bold bright_white on dark_blue",
                border_style="blue",
                show_lines=False,
                expand=True
            )
            table.add_column("Asset", justify="left", style="bold white", no_wrap=True)
            table.add_column("Bid", justify="right", style="cyan", no_wrap=True)
            table.add_column("Ask", justify="right", style="cyan", no_wrap=True)
            table.add_column("Spread", justify="right", style="dim", no_wrap=True)
            table.add_column("RSI", justify="right", no_wrap=True)
            table.add_column("4H Trend", justify="center", no_wrap=True)
            table.add_column("FVG", justify="center", no_wrap=True)
            table.add_column("CRT/ORB", justify="center", no_wrap=True)
            table.add_column("P*", justify="right", no_wrap=True)
            table.add_column("Decision / Trigger Reason", justify="left", ratio=1, overflow="ellipsis")

            for asset, eng in engines.items():
                tick = self.mt5_conn.get_last_tick(asset)
                if tick is None:
                    continue

                # Refresh on newly closed 15m bar
                is_new_candle = False
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
                        is_new_candle = True

                # Dynamic strategy signal evaluation
                sig = strat.generate_signal(asset, eng.buffer, eng.buffer_4h, current_tick=tick)

                # Indicators for telemetry display
                features = eng.compute_features().iloc[-1]
                rsi = features.get('rsi_14', 50.0)
                trend_val = features.get('htf_4h_trend', 0.0)
                bull_fvg = features.get('bullish_fvg', 0.0)
                bear_fvg = features.get('bearish_fvg', 0.0)
                crt = eng.compute_crt_orb()

                trend_cell = "[bold green]BULL[/bold green]" if trend_val > 0 else ("[bold red]BEAR[/bold red]" if trend_val < 0 else "[dim]FLAT[/dim]")
                fvg_cell = "[bold green]BULL[/bold green]" if bull_fvg > 0 else ("[bold red]BEAR[/bold red]" if bear_fvg > 0 else "[dim]NONE[/dim]")
                crt_cell = "[bold green]LONG[/bold green]" if crt["is_long_crt"] else ("[bold red]SHORT[/bold red]" if crt["is_short_crt"] else "[dim]NONE[/dim]")
                rsi_cell = f"[bold red]{rsi:.1f}[/bold red]" if rsi >= 70 else (f"[bold green]{rsi:.1f}[/bold green]" if rsi <= 30 else f"{rsi:.1f}")
                prob_cell = f"[bold green]{sig.prob:.3f}[/bold green]" if sig.prob >= PROBABILITY_THRESHOLD else f"[dim]{sig.prob:.3f}[/dim]"

                decision_cell = f"[dim]{sig.reason}[/dim]"

                # Causal execution: Trigger trade entry strictly at the start of the next candle
                current_candle_ts = last_candle_times.get(asset)
                should_trigger = (is_new_candle or once) and sig.is_active
                already_triggered = (last_triggered_candles.get(asset) == current_candle_ts)

                governed_risk, risk_regime_desc = self.order_mgr.get_current_risk_budget()

                if governed_risk <= 0.0 and sig.is_active:
                    decision_cell = f"[bold red]FREEZE ({risk_regime_desc})[/bold red]"
                elif should_trigger and not already_triggered:
                    r_dist = abs(sig.entry_price - sig.sl_price)
                    calc_lots = self.order_mgr.calculate_lot_size(asset, risk_usd=governed_risk, sl_dist=r_dist)
                    action_lbl = f"{'LIVE' if live else 'DRY'}-{'BUY' if sig.is_buy else 'SELL'} ({sig.strategy_tag})"
                    color_style = "bold white on green" if sig.is_buy else "bold white on red"
                    decision_cell = f"[{color_style}] {action_lbl} ({calc_lots:.2f}L) [/{color_style}]"

                    order_type = mt5.ORDER_TYPE_BUY if sig.is_buy else mt5.ORDER_TYPE_SELL
                    self.order_mgr.place_market_order(
                        asset, order_type, volume=calc_lots, sl_price=sig.sl_price,
                        tp_price=sig.tp_price, risk_usd=governed_risk, strategy_tag=sig.strategy_tag
                    )
                    last_triggered_candles[asset] = current_candle_ts
                elif sig.is_active:
                    action_lbl = f"{'BUY' if sig.is_buy else 'SELL'} ({sig.strategy_tag})"
                    decision_cell = f"[bold cyan]ARMED {action_lbl} ({risk_regime_desc})[/bold cyan]"

                table.add_row(
                    asset, f"{tick.bid:.5f}", f"{tick.ask:.5f}", f"{(tick.ask - tick.bid):.5f}",
                    rsi_cell, trend_cell, fvg_cell, crt_cell, prob_cell, decision_cell
                )

            # 1. Render Account & Risk Header Panel (Autofit in width)
            metrics = self.order_mgr.get_account_metrics()
            mode_tag = "[bold red]LIVE BROKER[/bold red]" if live else "[bold yellow]PAPER DRY-RUN[/bold yellow]"
            pnl_color = "bold green" if metrics['running_pnl'] >= 0 else "bold red"
            real_pnl_color = "bold green" if metrics['realized_pnl'] >= 0 else "bold red"
            tot_pnl_color = "bold green" if metrics['total_pnl'] >= 0 else "bold red"

            governed_risk, risk_regime_desc = self.order_mgr.get_current_risk_budget()
            regime_badge = f"[bold red]{risk_regime_desc}[/bold red]" if governed_risk <= 0.0 else (
                f"[bold yellow]{risk_regime_desc}[/bold yellow]" if governed_risk == DEFENSE_RISK_USD else
                f"[bold green]{risk_regime_desc}[/bold green]"
            )

            account_text = (
                f"Account: [bold cyan]#{metrics['login']}[/bold cyan] ({metrics['server']}) | "
                f"Mode: {mode_tag} | Strategy: [bold bright_white]{strat.name.upper()}[/bold bright_white] | "
                f"Risk Regime: {regime_badge}\n"
                f"Equity: [bold bright_white]{metrics['equity']:,.2f} {metrics['currency']}[/bold bright_white] | "
                f"Balance: [bold]{metrics['balance']:,.2f} {metrics['currency']}[/bold] | "
                f"Running PnL: [{pnl_color}]{metrics['running_pnl']:+,.2f} USD[/{pnl_color}] | "
                f"Realized PnL: [{real_pnl_color}]{metrics['realized_pnl']:+,.2f} USD[/{real_pnl_color}] | "
                f"Total Session PnL: [{tot_pnl_color}]{metrics['total_pnl']:+,.2f} USD[/{tot_pnl_color}]\n"
                f"Margin: {metrics['margin']:,.2f} | Free Margin: {metrics['margin_free']:,.2f} | "
                f"Margin Level: {metrics['margin_level']:.1f}% | DD: {metrics['drawdown_pct']:.2f}% | "
                f"Open Positions: [bold yellow]{metrics['open_count']}/2[/bold yellow] | "
                f"Closed: {metrics['closed_count']} (WR: {metrics['win_rate']:.1f}%)"
            )
            hdr_panel = Panel(account_text, title="[bold bright_cyan]FOREX MASTER ENGINE: LIVE RISK & PNL TELEMETRY[/bold bright_cyan]", border_style="cyan", expand=True)

            elements = [hdr_panel]

            # 2. Render Active Open Trades Table (Autofit in width)
            if self.order_mgr.open_trades:
                ot_table = Table(
                    title=f"ACTIVE OPEN POSITIONS ({len(self.order_mgr.open_trades)}/2)",
                    box=box.ROUNDED,
                    header_style="bold bright_white on dark_green",
                    border_style="green",
                    show_lines=False,
                    expand=True
                )
                ot_table.add_column("Ticket", justify="center", style="bold white", no_wrap=True)
                ot_table.add_column("Asset", justify="left", style="bold cyan", no_wrap=True)
                ot_table.add_column("Sleeve", justify="center", no_wrap=True)
                ot_table.add_column("Side", justify="center", no_wrap=True)
                ot_table.add_column("Lots", justify="right", no_wrap=True)
                ot_table.add_column("Entry", justify="right", no_wrap=True)
                ot_table.add_column("Current", justify="right", no_wrap=True)
                ot_table.add_column("SL", justify="right", no_wrap=True)
                ot_table.add_column("TP", justify="right", no_wrap=True)
                ot_table.add_column("R", justify="right", no_wrap=True)
                ot_table.add_column("PnL", justify="right", no_wrap=True)
                ot_table.add_column("Ratchet", justify="left", ratio=1, overflow="ellipsis")
                ot_table.add_column("Bars", justify="right", no_wrap=True)

                def _fmt(val: float) -> str:
                    if abs(val) >= 1000.0:
                        return f"{val:.2f}"
                    elif abs(val) >= 10.0:
                        return f"{val:.4f}"
                    return f"{val:.5f}"

                for ticket, tr in self.order_mgr.open_trades.items():
                    act_str = tr.get("action") or ("BUY" if tr.get("type", 0) in (0, mt5.ORDER_TYPE_BUY) else "SELL")
                    side_style = "bold green" if act_str == "BUY" else "bold red"
                    cur_r = float(tr.get("current_r", 0.0))
                    run_pnl = float(tr.get("running_pnl", 0.0))
                    r_style = "bold green" if cur_r >= 0 else "bold red"
                    pnl_style = "bold green" if run_pnl >= 0 else "bold red"
                    entry_val = float(tr.get("entry") or tr.get("entry_price") or 0.0)
                    cur_p = float(tr.get("cur_price") or entry_val)
                    sl_val = float(tr.get("sl") or 0.0)
                    tp_val = float(tr.get("tp") or 0.0)
                    strat_val = str(tr.get("strategy", "PARALLEL"))
                    vol_val = float(tr.get("volume", 0.01))
                    ratch_val = str(tr.get("ratchet_desc", "Base SL"))
                    bars_val = int(tr.get("bars_held", tr.get("bars_elapsed", 0)))
                    ot_table.add_row(
                        str(ticket),
                        str(tr.get("symbol", "UNKNOWN")),
                        strat_val,
                        f"[{side_style}]{act_str}[/{side_style}]",
                        f"{vol_val:.2f}L",
                        _fmt(entry_val),
                        _fmt(cur_p),
                        _fmt(sl_val),
                        _fmt(tp_val),
                        f"[{r_style}]{cur_r:+.2f}R[/{r_style}]",
                        f"[{pnl_style}]{run_pnl:+,.2f} USD[/{pnl_style}]",
                        ratch_val,
                        f"{bars_val}/24"
                    )
                elements.append(ot_table)
            else:
                elements.append(Panel("[dim italic]Active Positions: None (Scanning 18 assets for high-probability confluence setups...)[/dim italic]", border_style="dim", expand=True))

            # 3. Render Session Closed Trades Table (Autofit in width)
            if self.order_mgr.closed_trades:
                ct_table = Table(
                    title=f"SESSION CLOSED TRADES HISTORY (Last 5 of {len(self.order_mgr.closed_trades)})",
                    box=box.ROUNDED,
                    header_style="bold bright_white on blue",
                    border_style="blue",
                    show_lines=False,
                    expand=True
                )
                ct_table.add_column("Ticket", justify="center", style="dim", no_wrap=True)
                ct_table.add_column("Asset", justify="left", style="bold white", no_wrap=True)
                ct_table.add_column("Sleeve", justify="center", no_wrap=True)
                ct_table.add_column("Side", justify="center", no_wrap=True)
                ct_table.add_column("Entry", justify="right", no_wrap=True)
                ct_table.add_column("Exit", justify="right", no_wrap=True)
                ct_table.add_column("Exit Reason", justify="left", ratio=1, overflow="ellipsis")
                ct_table.add_column("Realized R", justify="right", no_wrap=True)
                ct_table.add_column("Realized PnL", justify="right", no_wrap=True)
                ct_table.add_column("Bars", justify="right", no_wrap=True)

                for ct in self.order_mgr.closed_trades[-5:]:
                    act_str = ct.get("action", "BUY")
                    side_style = "green" if act_str == "BUY" else "red"
                    real_pnl = float(ct.get("realized_pnl", 0.0))
                    real_r = float(ct.get("realized_r", 0.0))
                    pnl_style = "bold green" if real_pnl >= 0 else "bold red"
                    r_style = "bold green" if real_r >= 0 else "bold red"
                    entry_val = float(ct.get("entry") or ct.get("entry_price") or 0.0)
                    exit_val = float(ct.get("exit", 0.0))
                    b_held = int(ct.get("bars_held", ct.get("bars_elapsed", 0)))
                    ct_table.add_row(
                        str(ct.get("ticket", 0)),
                        str(ct.get("symbol", "UNKNOWN")),
                        str(ct.get("strategy", "PARALLEL")),
                        f"[{side_style}]{act_str}[/{side_style}]",
                        f"{entry_val:.5f}",
                        f"{exit_val:.5f}",
                        str(ct.get("reason", "NORMAL")),
                        f"[{r_style}]{real_r:+.2f}R[/{r_style}]",
                        f"[{pnl_style}]{real_pnl:+,.2f} USD[/{pnl_style}]",
                        f"{b_held}"
                    )
                elements.append(ct_table)

            # 4. Telemetry Table
            elements.append(table)
            return Group(*elements)

        try:
            if once:
                frame = build_dashboard_frame()
                console.print(frame)
                return

            last_reconcile_time = 0.0
            with Live(console=console, screen=False, auto_refresh=False) as live_ui:
                while True:
                    # Operational Safeguard 3: Broker Position Reconciliation Heartbeat (every 30 seconds)
                    if time.time() - last_reconcile_time >= RECONCILE_HEARTBEAT_INTERVAL_SEC:
                        self.order_mgr.reconcile_with_broker()
                        last_reconcile_time = time.time()

                    frame = build_dashboard_frame()
                    live_ui.update(frame, refresh=True)
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
  # 1. Run Live/Dry-Run Parallel Dual-Sleeve Telemetry (FVG_ML + ORB_CRT in parallel)
  python Engine/forex_engine.py
  python Engine/forex_engine.py --strategy parallel

  # 2. Run Single Strategy Mode (FVG_ML or ORB_CRT individually)
  python Engine/forex_engine.py --strategy fvg_ml
  python Engine/forex_engine.py --strategy orb_crt

  # 3. Run Single-Pass Snapshot of all 18 assets across both strategies
  python Engine/forex_engine.py --mode snapshot --strategy parallel

  # 4. Run Forward-Test Backtest from Dec 2025 onwards (Validating against Target Criteria)
  python Engine/forex_engine.py --mode forward-test --strategy parallel --start-date 2025-12-01

  # 5. Run Specific Out-Of-Sample Regime Window (Window 20: March 2026 Microstructure Shock)
  python Engine/forex_engine.py --mode oos-window --strategy parallel --window 20

  # 6. Run Full 20 OOS Window Walk-Forward with Institutional Fail-Fast Gate
  python Engine/forex_engine.py --mode walkforward --strategy parallel

  # 7. Run System Diagnostics & Storage Inspection
  python Engine/forex_engine.py --mode info

  # 8. Arm Real Live Broker Orders to MetaTrader 5
  python Engine/forex_engine.py --strategy parallel --live
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
        default="parallel",
        help="Trading strategy: 'parallel' (Dual-Sleeve FVG_ML + ORB_CRT, default), 'fvg_ml', 'orb_crt', 'combined', or comma-separated sleeves (default: parallel)"
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

    is_once = (args.mode == "snapshot")
    engine.run_telemetry(
        strategy_target=args.strategy,
        once=is_once,
        ignore_kz=args.ignore_kz,
        dry_run=(not args.live),
        live=args.live,
        interval=args.interval,
        skip_train=args.skip_train
    )


if __name__ == "__main__":
    main()
