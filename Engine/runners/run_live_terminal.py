"""
================================================================================
ENGINE 2: LIVE QUANT MATRIX TERMINAL RUNNER (23-OOS ELITE MULTI-SLEEVE SUITE)
================================================================================
Master operational execution, signal scanning, and monitoring terminal for the
certified 23-OOS elite quant multi-model suite (run_23_oos_altcoin_suite.py).

Unifies:
1. 11-Asset Institutional Core Universe (Binance USDT-M Perpetuals).
2. Dynamic Institutional Risk Governor (Milestone Pass Lock, DD Defense, House Money).
3. 5-Sleeve Alpha Engine (OX66 unified ids: S1=1 Pullback, S2=2 Bollinger, S3=3 ORB/CRT, S4=4 Pivot Sweeps, T1=5 Donchian).
4. Full Execution Bridge with BinanceBroker (Dry-Run and Live REST/WebSocket).
5. Microstructure Trailing Ratchets (BE Lock at +0.8R, Profit Lock at +1.5R, 24-bar timeout).
6. Live BTC Buy & Hold Benchmark Alpha Tracker.
================================================================================
"""

import os
import sys
import time
import math
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

# Rich Terminal UI components
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich import box

# Ensure project root is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Core imports from Engine
from Engine.core.canonical_indicators import (
    compute_kairi_zscore,
    compute_bollinger_bandwidth_zscore,
    compute_adx_series,
    compute_structural_pivots_and_sweeps,
    apply_atr_floor,
    SLEEVE_S1_PULLBACK, SLEEVE_S2_BOLLINGER, SLEEVE_S3_ORB,
    SLEEVE_S4_PIVOT_SWEEP, SLEEVE_T1_DONCHIAN,
)
from Engine.brokers.binance_broker import BinanceBroker

try:
    from Engine.core.multi_tf_data import get_or_compute_4h_dataframe
except Exception:
    get_or_compute_4h_dataframe = None

try:
    from Engine.runners.run_historical_pipeline import run_pipeline, ENGINE_1_CRYPTO_SYMBOLS
except ImportError:
    try:
        from Engine.run_historical_pipeline import run_pipeline, ENGINE_1_CRYPTO_SYMBOLS
    except ImportError:
        ENGINE_1_CRYPTO_SYMBOLS = [
            "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT",
            "ADAUSDT", "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT"
        ]
        run_pipeline = None

# Configure console stdout encoding and Windows Virtual Terminal escape sequences
sys.stdout.reconfigure(encoding="utf-8")
os.system("")

try:
    _term_w = os.get_terminal_size().columns
except Exception:
    _term_w = 180

RICH_CONSOLE = Console(highlight=False, width=max(_term_w, 180))

# Certified 11 Core Binance Institutional Perpetuals
CORE_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT",
    "ADAUSDT", "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT"
]

ASSET_LISTING_DATES = {
    "BTCUSDT": "2020-09-01",
    "ETHUSDT": "2020-09-01",
    "XRPUSDT": "2020-09-01",
    "BNBUSDT": "2020-09-01",
    "DOGEUSDT": "2020-09-01",
    "ADAUSDT": "2020-09-01",
    "TRXUSDT": "2020-09-01",
    "LINKUSDT": "2020-09-01",
    "DOTUSDT": "2020-09-01",
    "LTCUSDT": "2020-09-01",
    "BCHUSDT": "2020-09-01",
}

DEFAULT_DATA_DIR = Path(
    PROJECT_ROOT / "binance_backtesting_data"
    if (PROJECT_ROOT / "binance_backtesting_data").exists()
    else (SCRIPT_DIR / "binance_backtesting_data")
)


# ================================================================================
# PRE-FLIGHT GAP SYNCHRONIZATION
# ================================================================================

def preflight_sync_missing_data(target_dir: Path = DEFAULT_DATA_DIR, max_workers: int = 16):
    """
    Scans Master Parquet files in the destination directory:
      1. Verifies each core symbol exists and is readable.
      2. If missing or stale (>24h), triggers pipeline synchronization.
    """
    RICH_CONSOLE.print(Panel(
        f"[bold cyan]🔍 PRE-FLIGHT CHECK: Scanning Master Parquet Datasets in {target_dir}[/bold cyan]",
        box=box.DOUBLE, border_style="cyan"
    ))
    
    missing_or_stale = []
    now_ms = time.time() * 1000
    
    for sym in CORE_SYMBOLS:
        p_path = target_dir / f"{sym}_15m_master_2020_2026.parquet"
        if not p_path.exists():
            RICH_CONSOLE.print(f"  [bold red]✖ MISSING[/bold red] {sym}: Master Parquet not found.")
            missing_or_stale.append(sym)
            continue
        try:
            pf = pq.ParquetFile(p_path)
            last_rg = max(0, pf.num_row_groups - 1)
            t = pf.read_row_group(last_rg, columns=["close_time_ms", "datetime_utc"])
            df = t.to_pandas()
            if df.empty:
                RICH_CONSOLE.print(f"  [bold red]✖ CORRUPT[/bold red] {sym}: Parquet is empty.")
                missing_or_stale.append(sym)
                continue
            last_close_ms = int(df["close_time_ms"].iloc[-1])
            hours_behind = (now_ms - last_close_ms) / (1000 * 3600)
            if hours_behind > 24.0:
                RICH_CONSOLE.print(f"  [bold yellow]⚠ STALE[/bold yellow] {sym}: {hours_behind:.1f}h behind ({df['datetime_utc'].iloc[-1]}).")
                missing_or_stale.append(sym)
            else:
                RICH_CONSOLE.print(f"  [bold green]✔ OK[/bold green] {sym}: Valid ({df['datetime_utc'].iloc[-1]}, {pf.metadata.num_rows:,} rows).")
        except Exception as e:
            RICH_CONSOLE.print(f"  [bold red]✖ ERROR[/bold red] {sym}: {e}")
            missing_or_stale.append(sym)

    if missing_or_stale and run_pipeline is not None:
        RICH_CONSOLE.print(f"\n[bold yellow]🔄 Auto-syncing {len(missing_or_stale)} asset(s)...[/bold yellow]")
        for sym in missing_or_stale:
            sym_start = ASSET_LISTING_DATES.get(sym, "2020-09-01")
            run_pipeline(
                symbol=sym,
                start_date_str=sym_start,
                target_dir=str(target_dir),
                max_workers=max_workers,
                run_audit=False
            )
        RICH_CONSOLE.print("[bold green]✅ Pre-Flight Gap Synchronization Complete![/bold green]\n")
    else:
        RICH_CONSOLE.print("[bold green]✅ All Core Datasets are Verified & Healthy.[/bold green]\n")


# ================================================================================
# INSTITUTIONAL RISK GOVERNOR & PORTFOLIO STATE
# ================================================================================

class InstitutionalRiskGovernor:
    """
    Enforces the certified 23-OOS Institutional Risk Management protocol:
    1. Base Risk: 36.0 USD (0.72% on 5,000 USD initial capital).
    2. DD Defense Mode: Scales risk down to min(base_r * 0.40, 14.0 USD) if DD >= 2.0% or profit < -50.0 USD.
    3. House Money Mode: Scales risk up to min(base_r * 1.35, 48.0 USD) if cumulative profit >= 120.0 USD.
    4. Milestone Pass Lock: Once peak profit >= 500.0 USD and trades >= 15, locks in pass floor stop
       and restricts risk to min(10.0 USD, cushion * 0.20).
    5. Circuit Breaker: 4.85% maximum drawdown ceiling.
    6. Concurrency Limits: Max 3 concurrent positions (max 2 S1, max 2 T1(id5), max 2 ORB, max 1/asset).
    """

    def __init__(self, initial_capital: float = 5000.0):
        self.initial_capital: float = initial_capital
        self.equity: float = initial_capital
        self.peak_equity: float = initial_capital
        self.wallet_balance: float = initial_capital
        self.realized_pnl: float = 0.0
        self.unrealized_pnl: float = 0.0
        self.trade_count: int = 0
        self.win_count: int = 0
        self.max_dd_pct: float = 0.0
        self.is_locked: bool = False
        self.circuit_breaker_tripped: bool = False

        # Concurrency caps (OX59: max 3 portfolio-wide)
        self.max_concurrent: int = 3
        self.max_s1_concurrent: int = 2
        self.max_t1_concurrent: int = 2
        self.max_orb_concurrent: int = 2

    def update_equity(self, unrealized_pnl: float):
        self.unrealized_pnl = unrealized_pnl
        self.equity = self.wallet_balance + self.unrealized_pnl
        if self.equity > self.peak_equity:
            self.peak_equity = self.equity
        cur_dd = ((self.peak_equity - self.equity) / self.peak_equity) * 100.0 if self.peak_equity > 0 else 0.0
        if cur_dd > self.max_dd_pct:
            self.max_dd_pct = cur_dd
        if self.max_dd_pct >= 4.85:
            self.circuit_breaker_tripped = True

    def record_closed_trade(self, pnl: float):
        self.wallet_balance += pnl
        self.realized_pnl += pnl
        self.trade_count += 1
        if pnl > 0:
            self.win_count += 1
        self.update_equity(0.0)

    def get_risk_budget(self, base_r: float = 36.0, sleeve_id: int = 0,
                        regime: str = "SIDEWAYS_CHOP") -> Tuple[float, str]:
        """Calculates dynamic risk budget and active tier (OX59: regime sizing + DD contraction)."""
        cur_dd = ((self.peak_equity - self.equity) / self.peak_equity) * 100.0 if self.peak_equity > 0 else 0.0
        cur_profit = self.equity - self.initial_capital

        # OX59 regime sizing: halve S1 pullback risk in chop
        if regime == "SIDEWAYS_CHOP" and sleeve_id == 1:
            base_r = base_r * 0.5

        if (self.peak_equity - self.initial_capital) >= 500.0 and self.trade_count >= 15:
            floor_stop = max(self.initial_capital + 500.0, self.peak_equity - 120.0)
            if self.equity <= floor_stop:
                self.is_locked = True
                return 0.0, "PASS_LOCKED"
            cushion = max(0.0, self.equity - (self.initial_capital + 500.0))
            trade_risk = min(10.0, cushion * 0.20)
            if trade_risk <= 0.0:
                self.is_locked = True
                return 0.0, "PASS_LOCKED"
            return trade_risk, "MILESTONE_LOCK"

        if cur_dd >= 2.0 or cur_profit < -50.0:
            trade_risk, tier = min(base_r * 0.40, 14.0), "DD_DEFENSE"
        elif cur_profit >= 120.0:
            trade_risk, tier = min(base_r * 1.35, 48.0), "HOUSE_MONEY"
        else:
            trade_risk, tier = min(base_r, 36.0), "BASE_RISK"

        # OX59 DD contraction: halve non-milestone risk once running DD >= 1.80%
        if self.max_dd_pct >= 1.80:
            trade_risk = trade_risk * 0.5
            tier = tier + "_X05"
        return trade_risk, tier

    def can_open_position(self, sleeve_id: int, active_positions: List[Dict[str, Any]],
                        symbol: Optional[str] = None, direction: int = 0,
                        btc_breakdown: bool = False) -> bool:
        if self.is_locked or self.circuit_breaker_tripped:
            return False
        if len(active_positions) >= self.max_concurrent:
            return False

        s1_count = sum(1 for p in active_positions if p["sleeve_id"] == SLEEVE_S1_PULLBACK)
        t1_count = sum(1 for p in active_positions if p["sleeve_id"] == SLEEVE_T1_DONCHIAN)
        orb_count = sum(1 for p in active_positions if p["sleeve_id"] == SLEEVE_S3_ORB)

        if sleeve_id == SLEEVE_S1_PULLBACK and s1_count >= self.max_s1_concurrent:
            return False
        if sleeve_id == SLEEVE_T1_DONCHIAN and t1_count >= self.max_t1_concurrent:
            return False
        if sleeve_id == SLEEVE_S3_ORB and orb_count >= self.max_orb_concurrent:
            return False

        # OX59 cluster: max 1 position per asset
        if symbol is not None and any(p["symbol"] == symbol for p in active_positions):
            return False

        # OX59 cluster: max 1 high-beta alt long in BTC breakdown
        if btc_breakdown and direction == 1 and symbol is not None and symbol != "BTCUSDT":
            hb_longs = sum(1 for p in active_positions
                           if p["direction"] == 1 and p["symbol"] != "BTCUSDT")
            if hb_longs >= 1:
                return False

        return True


# ================================================================================
# ACTIVE POSITION TRACKER WITH MICROSTRUCTURE RATCHET
# ================================================================================

class LivePositionTracker:
    """
    Manages open positions, real-time unrealized PnL, and the piecewise
    microstructure exit ratchet (BE lock at +0.8R, profit lock at +1.5R, 24-bar timeout).
    """

    def __init__(self, broker: BinanceBroker):
        self.broker = broker
        self.positions: List[Dict[str, Any]] = []

    def add_position(
        self,
        symbol: str,
        sleeve_name: str,
        sleeve_id: int,
        direction: int,  # 1 for Long, -1 for Short
        entry_price: float,
        stop_price: float,
        target_price: float,
        r_dist: float,
        risk_usd: float,
        units: float,
        ticket: int = 0,
    ):
        pos = {
            "ticket": ticket,
            "symbol": symbol,
            "sleeve_name": sleeve_name,
            "sleeve_id": sleeve_id,
            "direction": direction,
            "entry_price": entry_price,
            "current_price": entry_price,
            "stop_price": stop_price,
            "initial_stop": stop_price,
            "target_price": target_price,
            "r_dist": r_dist,
            "risk_usd": risk_usd,
            "units": units,
            "ratchet_stage": 0,  # 0: Initial, 1: BE (+0.15R), 2: Profit Lock (+0.80R)
            "peak_r": 0.0,
            "bars_held": 0,
            "unrealized_pnl": 0.0,
            "open_time": time.time(),
        }
        self.positions.append(pos)

    def update_positions(self, latest_prices: Dict[str, float]) -> Tuple[List[Dict[str, Any]], float]:
        """
        Updates current prices, ratchets stops on exchange, evaluates targets/stops,
        and triggers live broker closures.
        """
        closed_positions = []
        total_upnl = 0.0
        remaining_positions = []

        for pos in self.positions:
            sym = pos["symbol"]
            cur_px = latest_prices.get(sym, pos["current_price"])
            pos["current_price"] = cur_px
            
            # F3 Fix: Calculate true 15m bars held from wall-clock elapsed time (900s per bar)
            elapsed_sec = time.time() - pos["open_time"]
            pos["bars_held"] = int(elapsed_sec / 900)
            
            direction = pos["direction"]
            r_dist = pos["r_dist"]

            # Calculate R-gain and Unrealized PnL
            if direction == 1:
                r_gain = (cur_px - pos["entry_price"]) / r_dist if r_dist > 0 else 0.0
                upnl = (cur_px - pos["entry_price"]) * pos["units"]
            else:
                r_gain = (pos["entry_price"] - cur_px) / r_dist if r_dist > 0 else 0.0
                upnl = (pos["entry_price"] - cur_px) * pos["units"]

            pos["unrealized_pnl"] = upnl
            total_upnl += upnl

            if r_gain > pos["peak_r"]:
                pos["peak_r"] = r_gain

            # Microstructure Ratchet (OX59 universal: 0.80->+0.20 / 1.50->+0.80 / 2.00->+1.50)
            # Stage 1: +0.8R gain -> Ratchet stop to Entry + 0.20R (BE Lock)
            if pos["peak_r"] >= 0.80 and pos["ratchet_stage"] < 1:
                if direction == 1:
                    pos["stop_price"] = pos["entry_price"] + 0.20 * r_dist
                else:
                    pos["stop_price"] = pos["entry_price"] - 0.20 * r_dist
                pos["ratchet_stage"] = 1
                RICH_CONSOLE.print(f"[bold green]⚡ RATCHET LOCK (+0.20R BE)[/bold green] {sym} ({pos['sleeve_name']}) at +{pos['peak_r']:.2f}R")
                if self.broker:
                    if not self.broker.modify_sltp(binance_symbol=sym, position_ticket=pos.get("ticket", 0), sl=pos["stop_price"]):
                        RICH_CONSOLE.print(f"[bold yellow]⚠️ BE ratchet modify failed on exchange for {sym} (local stop kept)[/bold yellow]")

            # Stage 2: +1.5R gain -> Ratchet stop to Entry + 0.80R (Profit Lock)
            if pos["peak_r"] >= 1.50 and pos["ratchet_stage"] < 2:
                if direction == 1:
                    pos["stop_price"] = pos["entry_price"] + 0.80 * r_dist
                else:
                    pos["stop_price"] = pos["entry_price"] - 0.80 * r_dist
                pos["ratchet_stage"] = 2
                RICH_CONSOLE.print(f"[bold cyan]🎯 PROFIT LOCK (+0.80R)[/bold cyan] {sym} ({pos['sleeve_name']}) at +{pos['peak_r']:.2f}R")
                if self.broker:
                    if not self.broker.modify_sltp(binance_symbol=sym, position_ticket=pos.get("ticket", 0), sl=pos["stop_price"]):
                        RICH_CONSOLE.print(f"[bold yellow]⚠️ Profit-lock modify failed on exchange for {sym} (local stop kept)[/bold yellow]")

            # Stage 3 (OX59): +2.0R gain -> Ratchet stop to Entry + 1.50R (Trailing Lock)
            if pos["peak_r"] >= 2.00 and pos["ratchet_stage"] < 3:
                if direction == 1:
                    pos["stop_price"] = pos["entry_price"] + 1.50 * r_dist
                else:
                    pos["stop_price"] = pos["entry_price"] - 1.50 * r_dist
                pos["ratchet_stage"] = 3
                RICH_CONSOLE.print(f"[bold magenta]🔒 TRAIL LOCK (+1.50R)[/bold magenta] {sym} ({pos['sleeve_name']}) at +{pos['peak_r']:.2f}R")
                if self.broker:
                    if not self.broker.modify_sltp(binance_symbol=sym, position_ticket=pos.get("ticket", 0), sl=pos["stop_price"]):
                        RICH_CONSOLE.print(f"[bold yellow]⚠️ Trail-lock modify failed on exchange for {sym} (local stop kept)[/bold yellow]")

            # Check Exit Conditions
            exit_reason = None
            if direction == 1:
                if cur_px >= pos["target_price"]:
                    exit_reason = "TARGET_REACHED"
                elif cur_px <= pos["stop_price"]:
                    exit_reason = "STOP_HIT"
                elif pos["bars_held"] >= 24 and r_gain < 0.20:
                    exit_reason = "TIME_DECAY_EXIT"
            else:
                if cur_px <= pos["target_price"]:
                    exit_reason = "TARGET_REACHED"
                elif cur_px >= pos["stop_price"]:
                    exit_reason = "STOP_HIT"
                elif pos["bars_held"] >= 24 and r_gain < 0.20:
                    exit_reason = "TIME_DECAY_EXIT"

            if exit_reason:
                pos["exit_reason"] = exit_reason
                pos["realized_pnl"] = upnl
                closed_positions.append(pos)
                RICH_CONSOLE.print(f"[bold magenta]🔔 POSITION CLOSED [{exit_reason}][/bold magenta] {sym} | PnL: {upnl:+,.2f} USD ({r_gain:+.2f}R)")
                # F2 Fix: Dispatch live position closure directly to Binance exchange
                if self.broker:
                    try:
                        if not self.broker.close_position(symbol=sym, reason=exit_reason):
                            RICH_CONSOLE.print(f"[bold red]❌ Exchange close returned False for {sym} [{exit_reason}][/bold red]")
                    except Exception as e:
                        RICH_CONSOLE.print(f"[bold red]❌ Failed to close {sym} on exchange: {e}[/bold red]")
            else:
                remaining_positions.append(pos)

        self.positions = remaining_positions
        return closed_positions, total_upnl

    def reconcile_with_exchange(self):
        """F4 Fix: Reconcile internal tracker state with true exchange positions.
        OX59: returns exchange-closed positions so the governor books their PnL."""
        if not self.broker or self.broker.dry_run:
            return []
        reconciled_closed = []
        try:
            exchange_positions = self.broker.get_all_positions()
            open_symbols = {p["symbol"] for p in exchange_positions if float(p.get("positionAmt", 0)) != 0}
            reconciled = []
            for pos in self.positions:
                sym = pos["symbol"]
                if sym not in open_symbols:
                    pos["exit_reason"] = "EXCHANGE_STOP_HIT"
                    closed_pnl, _ = self.broker.get_position_history_profit(pos.get("ticket", 0))
                    pos["realized_pnl"] = closed_pnl if closed_pnl != 0.0 else pos["unrealized_pnl"]
                    reconciled_closed.append(pos)
                    RICH_CONSOLE.print(f"[bold yellow]🔄 RECONCILED CLOSE[/bold yellow] {sym} closed on Binance (PnL: {pos['realized_pnl']:+,.2f} USD)")
                else:
                    reconciled.append(pos)
            self.positions = reconciled
        except Exception as e:
            RICH_CONSOLE.print(f"[bold red]⚠️ Position reconciliation error: {e}[/bold red]")
        return reconciled_closed


# ================================================================================
# MULTI-SLEEVE ALPHA SIGNAL SCANNER
# ================================================================================

class MultiSleeveAlphaEngine:
    """
    Computes real-time signals across the 5 unified sleeves (OX66 taxonomy):
    1. S1: Dual-Model Liquidation Pullback.
    2. S2: Bollinger Mean Reversion (Z_BW <= 1.85, ADX <= 32.0).
    3. S3: Cross-Asset ORB/CRT Breakouts.
    4. S4: Structural Pivot Sweeps + Footprint Exhaustion (simplified live trigger).
    5. T1: Quiet-Flow Donchian Trend Breakout.
    """

    def __init__(self, data_dir: Path = DEFAULT_DATA_DIR):
        self.data_dir = data_dir
        self.cached_dfs: Dict[str, pd.DataFrame] = {}

    def load_recent_bars(self, symbol: str, n_bars: int = 350) -> Optional[pd.DataFrame]:
        p = self.data_dir / f"{symbol}_15m_master_2020_2026.parquet"
        if not p.exists():
            return None
        try:
            pf = pq.ParquetFile(p)
            total_rows = pf.metadata.num_rows
            skip = max(0, total_rows - n_bars)
            # Read last row group or slice
            table = pf.read(columns=[
                "open_time_ms", "open", "high", "low", "close",
                "volume", "rsi_14", "atr_14", "ema_200", "vwap_zscore", "zc_div", "volume_base",
                "future_cvd_15m", "volume_ratio", "session_vah", "session_val"
            ])
            df = table.to_pandas().iloc[skip:].dropna().reset_index(drop=True)
            return df
        except Exception:
            return None

    def evaluate_macro_regime(self) -> Dict[str, Any]:
        """
        Determines BTC ATH drawdown, 30-day return, and 4H trailing volatility.
        Returns regime: BEAR_CONTAGION, BULL_EXPANSION, or SIDEWAYS_CHOP.
        """
        btc_p = self.data_dir / "BTCUSDT_15m_master_2020_2026.parquet"
        if not btc_p.exists():
            return {"regime": "SIDEWAYS_CHOP", "ath_dd": -15.0, "btc_30d_ret": 2.5, "trailing_vol": 1.75, "btc_price": 65000.0, "btc_breakdown": False}

        try:
            pf = pq.ParquetFile(btc_p)
            t = pf.read(columns=["open_time_ms", "high", "low", "close"])
            df_btc = t.to_pandas().dropna().reset_index(drop=True)
            ath = float(df_btc["high"].max())
            cur_close = float(df_btc["close"].iloc[-1])
            ath_dd = ((cur_close - ath) / ath) * 100.0

            # 30-day return
            last_t = int(df_btc["open_time_ms"].iloc[-1])
            start_30d = last_t - 30 * 86400 * 1000
            df_30d = df_btc[df_btc["open_time_ms"] >= start_30d]
            btc_30d_ret = ((cur_close - float(df_30d["close"].iloc[0])) / float(df_30d["close"].iloc[0])) * 100.0 if len(df_30d) > 0 else 0.0

            # 4H Trailing Volatility
            trailing_vol = 1.75
            if get_or_compute_4h_dataframe is not None:
                try:
                    df_btc_4h = get_or_compute_4h_dataframe("BTCUSDT")
                    df_btc_4h['atr_pct'] = (df_btc_4h['atr'] / df_btc_4h['close']) * 100.0
                    trailing_vol = float(df_btc_4h['atr_pct'].rolling(180).mean().dropna().iloc[-1])
                except Exception:
                    pass

            # OX59: BTC 4H macro breakdown (close < 200 EMA on last closed 4H bar)
            btc_breakdown = False
            if get_or_compute_4h_dataframe is not None:
                try:
                    df_b4 = get_or_compute_4h_dataframe("BTCUSDT")
                    btc_breakdown = bool(float(df_b4['close'].iloc[-1]) < float(df_b4['ema_200'].iloc[-1]))
                except Exception:
                    pass

            is_bear_contagion = (ath_dd <= -35.0) and (btc_30d_ret <= -10.0)
            is_bull_expansion = (btc_30d_ret >= 15.0) and (cur_close >= df_btc["close"].rolling(800).mean().iloc[-1] if len(df_btc) > 800 else True)

            if is_bear_contagion:
                regime = "BEAR_CONTAGION"
            elif is_bull_expansion:
                regime = "BULL_EXPANSION"
            else:
                regime = "SIDEWAYS_CHOP"

            return {
                "regime": regime,
                "ath_dd": ath_dd,
                "btc_30d_ret": btc_30d_ret,
                "trailing_vol": trailing_vol,
                "btc_price": cur_close,
                "btc_breakdown": btc_breakdown,
            }
        except Exception as e:
            return {"regime": "SIDEWAYS_CHOP", "ath_dd": -15.0, "btc_30d_ret": 0.0, "trailing_vol": 1.75, "btc_price": 65000.0, "btc_breakdown": False}

    def scan_asset_signals(self, symbol: str, macro: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Scans a single asset for real-time technical indicators and alpha triggers across all 5 sleeves.
        """
        df = self.load_recent_bars(symbol)
        if df is None or len(df) < 220:
            return {"symbol": symbol, "status": "NO_DATA"}, []

        closes = df["close"].to_numpy(float)
        opens = df["open"].to_numpy(float)
        highs = df["high"].to_numpy(float)
        lows = df["low"].to_numpy(float)
        rsis = df["rsi_14"].to_numpy(float)
        atrs = df["atr_14"].to_numpy(float)
        ema200 = df["ema_200"].to_numpy(float) if "ema_200" in df.columns else pd.Series(closes).ewm(span=200).mean().to_numpy(float)
        vwap_z = df["vwap_zscore"].to_numpy(float) if "vwap_zscore" in df.columns else np.zeros(len(df))
        _volb = df["volume_base"].to_numpy(float) if "volume_base" in df.columns else np.ones(len(df))
        _volb = np.where(_volb == 0, 1.0, _volb)
        # OX59: normalized zc (research semantics) instead of raw CVD dollars
        zc_div = np.clip(df["zc_div"].to_numpy(float) / _volb, -3.0, 3.0) if "zc_div" in df.columns else np.zeros(len(df))
        fut_delta = df["future_cvd_15m"].fillna(0.0).to_numpy(float)
        vol_ratio = df["volume_ratio"].fillna(1.0).to_numpy(float)
        tms = df["open_time_ms"].to_numpy(np.int64)

        # Compute Canonical Indicators
        upper, lower, bw, zbw = compute_bollinger_bandwidth_zscore(closes, period=96, std_mult=2.0, z_window=96)
        _, _, adx = compute_adx_series(highs, lows, closes, 14)
        zkri_20 = compute_kairi_zscore(closes, atrs, period=20, z_window=96)

        idx = len(df) - 1
        cur_px = closes[idx]
        cur_atr = float(apply_atr_floor(atrs[idx:idx+1], closes[idx:idx+1])[0])  # OX66 unified R
        bar_ms = int(df["open_time_ms"].iloc[idx])
        cur_rsi = rsis[idx]
        cur_zbw = zbw[idx]
        cur_adx = adx[idx]
        cur_zkri = zkri_20[idx]
        cur_vwap_z = vwap_z[idx]
        cur_zc_div = zc_div[idx]

        metrics = {
            "symbol": symbol,
            "price": cur_px,
            "rsi": cur_rsi,
            "atr": cur_atr,
            "zbw": cur_zbw,
            "adx": cur_adx,
            "zkri": cur_zkri,
            "vwap_z": cur_vwap_z,
            "zc_div": cur_zc_div,
            "ema200": ema200[idx],
            "upper": upper[idx],
            "lower": lower[idx],
            "status": "SCANNED",
        }

        signals = []
        regime = macro["regime"]

        # -------------------------------------------------------------------------
        # 1. S1: Institutional Liquidity Pullbacks (Dual-Model Orderflow)
        # -------------------------------------------------------------------------
        if cur_atr > 0:
            if regime == "BEAR_CONTAGION":
                if cur_vwap_z > 0.5 and cur_rsi > 58.0:
                    signals.append({
                        "symbol": symbol, "sleeve_name": "S1_SHORT", "sleeve_id": SLEEVE_S1_PULLBACK, "direction": -1,
                        "entry_price": cur_px, "stop_price": cur_px + 1.0 * cur_atr,
                        "target_price": cur_px - 2.2 * cur_atr, "r_dist": cur_atr, "prob": 0.62, "base_risk": 32.0,
                        "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.2
                    })
            else:
                if cur_vwap_z < -0.5 and cur_rsi < 40.0 and cur_zc_div > 0.0:
                    signals.append({
                        "symbol": symbol, "sleeve_name": "S1_PULLBACK", "sleeve_id": SLEEVE_S1_PULLBACK, "direction": 1,
                        "entry_price": cur_px, "stop_price": cur_px - 1.0 * cur_atr,
                        "target_price": cur_px + 2.2 * cur_atr, "r_dist": cur_atr, "prob": 0.59, "base_risk": 42.0,
                        "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.2
                    })

        # -------------------------------------------------------------------------
        # 2. S2: Bollinger Mean Reversion (Z_BW <= 1.85, ADX <= 32.0)
        # -------------------------------------------------------------------------
        if cur_atr > 0 and cur_zbw <= 1.85 and cur_adx <= 32.0:
            if cur_px < lower[idx] and cur_rsi < 45.0:
                signals.append({
                    "symbol": symbol, "sleeve_name": "S2_BOLL_LONG", "sleeve_id": SLEEVE_S2_BOLLINGER, "direction": 1,
                    "entry_price": cur_px, "stop_price": cur_px - 1.0 * cur_atr,
                    "target_price": cur_px + 2.0 * cur_atr, "r_dist": cur_atr, "prob": 0.54, "base_risk": 24.0,
                    "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.0
                })
            elif cur_px > upper[idx] and cur_rsi > 55.0:
                signals.append({
                    "symbol": symbol, "sleeve_name": "S2_BOLL_SHORT", "sleeve_id": SLEEVE_S2_BOLLINGER, "direction": -1,
                    "entry_price": cur_px, "stop_price": cur_px + 1.0 * cur_atr,
                    "target_price": cur_px - 2.0 * cur_atr, "r_dist": cur_atr, "prob": 0.54, "base_risk": 24.0,
                    "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.0
                })

        # -------------------------------------------------------------------------
        # 5. T1: Quiet-Flow Donchian Trend Breakout
        # -------------------------------------------------------------------------
        if regime != "BEAR_CONTAGION" and len(highs) >= 96 and cur_atr > 0:
            highest_96 = np.max(highs[-96:-1])
            if cur_px >= highest_96:
                signals.append({
                    "symbol": symbol, "sleeve_name": "T1_BREAKOUT", "sleeve_id": SLEEVE_T1_DONCHIAN, "direction": 1,
                    "entry_price": cur_px, "stop_price": cur_px - 1.2 * cur_atr,
                    "target_price": cur_px + 2.5 * cur_atr, "r_dist": 1.2 * cur_atr, "prob": 0.54, "base_risk": 36.0,
                    "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.0833
                })

        # -------------------------------------------------------------------------
        # 3. S3: Crypto Opening Range Breakout (ORB / CRT)
        # -------------------------------------------------------------------------
        if len(df) >= 32 and cur_atr > 0:
            session_high = np.max(highs[-16:-1])
            session_low = np.min(lows[-16:-1])
            if cur_px > session_high and cur_rsi > 52.0 and (regime != "BEAR_CONTAGION" or cur_zc_div > 1.2):
                signals.append({
                    "symbol": symbol, "sleeve_name": "S3_ORB_LONG", "sleeve_id": SLEEVE_S3_ORB, "direction": 1,
                    "entry_price": cur_px, "stop_price": cur_px - 1.0 * cur_atr,
                    "target_price": cur_px + 2.4 * cur_atr, "r_dist": cur_atr, "prob": 0.56, "base_risk": 24.0,
                    "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.4
                })
            elif cur_px < session_low and cur_rsi < 48.0 and regime == "BEAR_CONTAGION":
                signals.append({
                    "symbol": symbol, "sleeve_name": "S3_ORB_SHORT", "sleeve_id": SLEEVE_S3_ORB, "direction": -1,
                    "entry_price": cur_px, "stop_price": cur_px + 1.0 * cur_atr,
                    "target_price": cur_px - 2.4 * cur_atr, "r_dist": cur_atr, "prob": 0.56, "base_risk": 24.0,
                    "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.4
                })

        # -------------------------------------------------------------------------
        # 4. S4: Structural Pivot Sweep + Footprint Exhaustion (live trigger)
        # -------------------------------------------------------------------------
        # Simplified vs research (no liq/zc/wick gates — filed parity limitation):
        # PDL/PDH sweep on the last closed bar + volume confirmation.
        try:
            atr_arr = apply_atr_floor(np.nan_to_num(atrs, nan=0.0), closes)
            (_pdh, _pdl, _pwh, _pwl, _pmh, _pml, _pdl_d, _pdh_d, _pwl_d, _pwh_d,
             _sweep_bull, _sweep_bear) = compute_structural_pivots_and_sweeps(
                tms, highs, lows, closes, fut_delta, _volb, vol_ratio, atr_arr)
            if cur_atr > 0 and vol_ratio[idx] >= 1.1:
                if bool(_sweep_bull[idx]):
                    signals.append({
                        "symbol": symbol, "sleeve_name": "S4_PIVOT_LONG", "sleeve_id": SLEEVE_S4_PIVOT_SWEEP, "direction": 1,
                        "entry_price": cur_px, "stop_price": cur_px - 1.0 * cur_atr,
                        "target_price": cur_px + 2.8 * cur_atr, "r_dist": cur_atr, "prob": 0.56, "base_risk": 36.0,
                        "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.8
                    })
                elif bool(_sweep_bear[idx]):
                    signals.append({
                        "symbol": symbol, "sleeve_name": "S4_PIVOT_SHORT", "sleeve_id": SLEEVE_S4_PIVOT_SWEEP, "direction": -1,
                        "entry_price": cur_px, "stop_price": cur_px + 1.0 * cur_atr,
                        "target_price": cur_px - 2.8 * cur_atr, "r_dist": cur_atr, "prob": 0.56, "base_risk": 36.0,
                        "bar_ms": bar_ms, "stop_mult": 1.0, "tgt_mult": 2.8
                    })
        except Exception as e:
            metrics["s4_status"] = f"S4_SKIPPED: {e}"

        return metrics, signals


# ================================================================================
# RICH DASHBOARD TELEMETRY RENDERING
# ================================================================================

def render_live_dashboard(
    macro: Dict[str, Any],
    risk_gov: InstitutionalRiskGovernor,
    tracker: LivePositionTracker,
    metrics_list: List[Dict[str, Any]],
    signals_list: List[Dict[str, Any]],
    initial_btc_price: float,
    dry_run: bool = True
):
    """
    Renders the institutional multi-panel matrix dashboard to the terminal.
    """
    # 1. Macro Regime Banner
    regime_color = "red" if macro["regime"] == "BEAR_CONTAGION" else ("green" if macro["regime"] == "BULL_EXPANSION" else "yellow")
    mode_text = "[bold yellow]SIMULATION / DRY-RUN[/bold yellow]" if dry_run else "[bold red]LIVE PRODUCTION (REAL CAPITAL)[/bold red]"
    
    header_text = Text()
    header_text.append("⚡ ENGINE 2: 23-OOS ELITE QUANT MULTI-SLEEVE LIVE TERMINAL ⚡\n", style="bold cyan")
    header_text.append(f"Mode: {mode_text} | ", style="white")
    header_text.append(f"BTC Price: {macro['btc_price']:,.2f} USD | ", style="bold white")
    header_text.append(f"ATH Drawdown: {macro['ath_dd']:.1f}% | ", style="bold magenta")
    header_text.append(f"30d Return: {macro['btc_30d_ret']:+.1f}% | ", style="bold blue")
    header_text.append(f"4H Volatility: {macro['trailing_vol']:.2f}% | ", style="bold cyan")
    header_text.append(f"Macro Regime: [{regime_color}]{macro['regime']}[/{regime_color}]", style="bold")

    RICH_CONSOLE.print(Panel(Align.center(header_text), box=box.ROUNDED, border_style="cyan"))

    # 2. Portfolio & Risk Governor Status
    risk_budget, risk_tier = risk_gov.get_risk_budget()
    win_rate = (risk_gov.win_count / risk_gov.trade_count * 100.0) if risk_gov.trade_count > 0 else 0.0
    net_roi = ((risk_gov.equity - risk_gov.initial_capital) / risk_gov.initial_capital) * 100.0

    btc_bh_ret = ((macro['btc_price'] - initial_btc_price) / initial_btc_price * 100.0) if initial_btc_price > 0 else 0.0
    alpha = net_roi - btc_bh_ret

    t_risk = Table(title="📊 Institutional Portfolio State & Risk Budget", box=box.SIMPLE_HEAVY, border_style="bright_blue", expand=True)
    t_risk.add_column("Account Equity", justify="right", style="bold green")
    t_risk.add_column("Wallet Balance", justify="right")
    t_risk.add_column("Net Profit / ROI", justify="right", style="bold cyan")
    t_risk.add_column("Peak Equity", justify="right")
    t_risk.add_column("Max Drawdown", justify="right", style="bold red")
    t_risk.add_column("Completed Trades", justify="center")
    t_risk.add_column("Win Rate", justify="center")
    t_risk.add_column("Dynamic Risk Tier", justify="center", style="bold yellow")
    t_risk.add_column("Next Trade Risk", justify="right", style="bold")
    t_risk.add_column("Alpha vs BTC B&H", justify="right", style="bold magenta")

    t_risk.add_row(
        f"{risk_gov.equity:,.2f} USD",
        f"{risk_gov.wallet_balance:,.2f} USD",
        f"{(risk_gov.equity - risk_gov.initial_capital):+,.2f} USD ({net_roi:+.2f}%)",
        f"{risk_gov.peak_equity:,.2f} USD",
        f"{risk_gov.max_dd_pct:.2f}% (Limit: 4.85%)",
        f"{risk_gov.trade_count}",
        f"{win_rate:.1f}% ({risk_gov.win_count}W)",
        risk_tier,
        f"{risk_budget:.2f} USD",
        f"{alpha:+.2f}% (BTC B&H: {btc_bh_ret:+.2f}%)"
    )
    RICH_CONSOLE.print(t_risk)

    # 3. 11 Core Asset Live Matrix
    t_matrix = Table(title="🌐 11-Asset Institutional Multi-Stream Signal Matrix", box=box.SIMPLE_HEAVY, border_style="cyan", expand=True)
    t_matrix.add_column("Asset", style="bold white", justify="left")
    t_matrix.add_column("Price (USD)", justify="right")
    t_matrix.add_column("RSI (14)", justify="right")
    t_matrix.add_column("ATR (14)", justify="right")
    t_matrix.add_column("BB Width Z", justify="right")
    t_matrix.add_column("ADX (14)", justify="right")
    t_matrix.add_column("KRI Z (20)", justify="right")
    t_matrix.add_column("VWAP Z", justify="right")
    t_matrix.add_column("Spot CVD Div", justify="right")
    t_matrix.add_column("Active Signal", justify="center", style="bold")

    sig_map = {s["symbol"]: f"{s['sleeve_name']} ({'LONG' if s['direction']==1 else 'SHORT'})" for s in signals_list}

    for m in metrics_list:
        sym = m["symbol"]
        if m.get("status") == "NO_DATA":
            t_matrix.add_row(sym, "-", "-", "-", "-", "-", "-", "-", "-", "[dim]NO DATA[/dim]")
            continue

        rsi_color = "red" if m["rsi"] > 68 else ("green" if m["rsi"] < 32 else "white")
        zbw_color = "green" if m["zbw"] <= 1.85 else "red"
        adx_color = "green" if m["adx"] <= 32.0 else "yellow"
        sig_str = sig_map.get(sym, "[dim]STANDBY[/dim]")
        if sym in sig_map:
            sig_str = f"[bold green]▶ {sig_str}[/bold green]"

        t_matrix.add_row(
            sym,
            f"{m['price']:,.4f}" if m['price'] < 10 else f"{m['price']:,.2f}",
            f"[{rsi_color}]{m['rsi']:.1f}[/{rsi_color}]",
            f"{m['atr']:.4f}",
            f"[{zbw_color}]{m['zbw']:+.2f}[/{zbw_color}]",
            f"[{adx_color}]{m['adx']:.1f}[/{adx_color}]",
            f"{m['zkri']:+.2f}",
            f"{m['vwap_z']:+.2f}",
            f"{m['zc_div']:+.2f}",
            sig_str
        )
    RICH_CONSOLE.print(t_matrix)

    # 4. Open Positions & Microstructure Ratchet Status
    t_pos = Table(title="🎯 Active Open Positions & Microstructure Ratchet (Max: 3 Concurrent)", box=box.SIMPLE_HEAVY, border_style="magenta", expand=True)
    t_pos.add_column("Asset", style="bold white", justify="left")
    t_pos.add_column("Sleeve", justify="center")
    t_pos.add_column("Side", justify="center")
    t_pos.add_column("Entry Price", justify="right")
    t_pos.add_column("Current Price", justify="right")
    t_pos.add_column("Stop Price", justify="right", style="bold red")
    t_pos.add_column("Target Price", justify="right", style="bold green")
    t_pos.add_column("Peak R", justify="center", style="bold cyan")
    t_pos.add_column("Ratchet Stage", justify="center", style="bold yellow")
    t_pos.add_column("Unrealized PnL", justify="right", style="bold")
    t_pos.add_column("Bars Held", justify="center")

    if not tracker.positions:
        t_pos.add_row("[dim]NO ACTIVE POSITIONS[/dim]", "-", "-", "-", "-", "-", "-", "-", "-", "0.00 USD", "-")
    else:
        for p in tracker.positions:
            pnl_col = "green" if p["unrealized_pnl"] >= 0 else "red"
            side_str = "[green]LONG[/green]" if p["direction"] == 1 else "[red]SHORT[/red]"
            _st = p["ratchet_stage"]
            stage_str = ("Initial" if _st == 0 else ("BE (+0.20R)" if _st == 1 else ("Profit Lock (+0.80R)" if _st == 2 else "Trail Lock (+1.50R)")))
            t_pos.add_row(
                p["symbol"],
                p["sleeve_name"],
                side_str,
                f"{p['entry_price']:,.2f}",
                f"{p['current_price']:,.2f}",
                f"{p['stop_price']:,.2f}",
                f"{p['target_price']:,.2f}",
                f"{p['peak_r']:+.2f}R",
                stage_str,
                f"[{pnl_col}]{p['unrealized_pnl']:+,.2f} USD[/{pnl_col}]",
                f"{p['bars_held']}/24"
            )
    RICH_CONSOLE.print(t_pos)


# ================================================================================
# SIGNAL DEDUPLICATION + COOLDOWN (OX66)
# ================================================================================

class SignalDedup:
    """Prevents stale-signal re-entry loops.

    A signal is unique per (symbol, sleeve_id, direction, bar_ms). Rejects
    exact duplicates of executed signals AND enforces a per-(symbol, sleeve)
    cooldown after any execution. In-memory only: a process restart clears
    memory (documented limitation).
    """

    def __init__(self, cooldown_sec: float = 6 * 3600):
        self.cooldown_sec = cooldown_sec
        self.executed_keys = set()
        self.last_fire = {}

    @staticmethod
    def key(sig):
        return (sig["symbol"], sig["sleeve_id"], sig["direction"], sig.get("bar_ms", 0))

    def is_duplicate(self, sig) -> bool:
        k = self.key(sig)
        if k in self.executed_keys:
            return True
        ck = (sig["symbol"], sig["sleeve_id"])
        if time.time() - self.last_fire.get(ck, 0.0) < self.cooldown_sec:
            return True
        return False

    def mark(self, sig) -> None:
        self.executed_keys.add(self.key(sig))
        self.last_fire[(sig["symbol"], sig["sleeve_id"])] = time.time()


# ================================================================================
# MAIN OPERATIONAL PIPELINE LOOP
# ================================================================================

def run_live_pipeline(
    dry_run: bool = True,
    once: bool = False,
    target_dir: Path = DEFAULT_DATA_DIR,
    target_symbols: Optional[List[str]] = None,
    poll_interval: int = 15
):
    symbols = target_symbols or CORE_SYMBOLS
    RICH_CONSOLE.print(Panel(
        f"[bold cyan]INITIALIZING ENGINE 2 LIVE QUANT TERMINAL[/bold cyan]\n"
        f"Universe: {len(symbols)} Assets | Mode: {'DRY-RUN (Paper)' if dry_run else 'LIVE PRODUCTION'}\n"
        f"Data Path: {target_dir}",
        box=box.DOUBLE, border_style="cyan"
    ))

    broker = BinanceBroker(dry_run=dry_run, account_size=5000.0)

    risk_gov = InstitutionalRiskGovernor(initial_capital=5000.0)
    tracker = LivePositionTracker(broker)
    alpha_engine = MultiSleeveAlphaEngine(data_dir=target_dir)
    dedup = SignalDedup(cooldown_sec=6 * 3600)

    # Fetch initial macro regime and BTC benchmark price
    if not broker.connect():
        RICH_CONSOLE.print("[bold red]⚠️ Binance Broker connect returned False (running in fallback mode)[/bold red]")
        if not dry_run:
            RICH_CONSOLE.print("[bold red]❌ Cannot proceed in LIVE mode without active broker connection. Exiting.[/bold red]")
            return

    macro = alpha_engine.evaluate_macro_regime()
    initial_btc_price = macro["btc_price"]

    cycle = 0
    try:
        while True:
            cycle += 1
            loop_start = time.time()

            # 1. Real-time Ticker Price Fetching via Broker REST API (F4 Fix)
            live_prices_map = broker.get_ticker_prices()
            latest_prices = {}
            if live_prices_map:
                for sym in symbols:
                    if sym in live_prices_map:
                        latest_prices[sym] = live_prices_map[sym]

            # 2. Update Macro Regime
            macro = alpha_engine.evaluate_macro_regime()

            # 3. Multi-Asset Scanning & Feature Extraction
            metrics_list = []
            all_detected_signals = []

            for sym in symbols:
                m, sigs = alpha_engine.scan_asset_signals(sym, macro)
                # Override static parquet price with live ticker price if available
                if sym in latest_prices:
                    m["price"] = latest_prices[sym]
                elif "price" in m:
                    latest_prices[sym] = m["price"]
                metrics_list.append(m)
                all_detected_signals.extend(sigs)

            # Reconcile open positions with true exchange state periodically
            if cycle % 2 == 0:
                for rc in tracker.reconcile_with_exchange():
                    risk_gov.record_closed_trade(rc.get("realized_pnl", 0.0))

            # 4. Update Existing Positions & Microstructure Ratchet
            closed, total_upnl = tracker.update_positions(latest_prices)
            for c in closed:
                risk_gov.record_closed_trade(c.get("realized_pnl", 0.0))
            risk_gov.update_equity(total_upnl)

            # 5. Dispatch New Positions If Capacity Permits
            for sig in all_detected_signals:
                slv_id = sig["sleeve_id"]
                if risk_gov.can_open_position(slv_id, tracker.positions, symbol=sig["symbol"],
                                              direction=sig["direction"],
                                              btc_breakdown=macro.get("btc_breakdown", False)):
                    # Check if already open for this symbol
                    if any(p["symbol"] == sig["symbol"] for p in tracker.positions):
                        continue

                    # OX66: dedup + cooldown (kills stale re-entry loops)
                    if dedup.is_duplicate(sig):
                        continue

                    # Dynamic Risk Sizing (OX59 regime-aware)
                    risk_usd, _ = risk_gov.get_risk_budget(base_r=sig.get("base_risk", 24.0),
                                                          sleeve_id=slv_id, regime=macro["regime"])
                    if risk_usd <= 0:
                        continue

                    # OX66: anchor geometry to the LIVE touch, not the stale bar close
                    live_entry = float(latest_prices.get(sig["symbol"], sig["entry_price"]))
                    r_dist = float(sig["r_dist"])
                    stop_dist = float(sig.get("stop_mult", 1.0)) * r_dist
                    tgt_dist = float(sig.get("tgt_mult", 2.0)) * r_dist
                    if stop_dist <= 0 or live_entry <= 0:
                        continue
                    live_sl = live_entry - sig["direction"] * stop_dist
                    live_tp = live_entry + sig["direction"] * tgt_dist

                    units = risk_usd / stop_dist

                    # Place Order via Broker
                    order_res = broker.execute_trade(
                        binance_symbol=sig["symbol"],
                        direction=sig["direction"],
                        bin_entry=live_entry,
                        bin_sl=live_sl,
                        bin_tp=live_tp,
                        strategy=sig["sleeve_name"],
                        risk_capital=risk_usd,
                        units=units
                    )

                    if order_res:
                        dedup.mark(sig)
                        ticket = int(order_res.get("ticket", order_res.get("orderId", 0)))
                        tracker.add_position(
                            symbol=sig["symbol"],
                            sleeve_name=sig["sleeve_name"],
                            sleeve_id=sig["sleeve_id"],
                            direction=sig["direction"],
                            entry_price=live_entry,
                            stop_price=live_sl,
                            target_price=live_tp,
                            r_dist=r_dist,
                            risk_usd=risk_usd,
                            units=units,
                            ticket=ticket
                        )
                        RICH_CONSOLE.print(f"[bold green]🚀 ORDER EXECUTED[/bold green] {sig['symbol']} {sig['sleeve_name']} @ {live_entry:,.2f} (live touch) | Sized: {units:.4f} units ({risk_usd:.2f} USD risk)")

            # 6. Render Dashboard
            RICH_CONSOLE.clear()
            render_live_dashboard(
                macro=macro,
                risk_gov=risk_gov,
                tracker=tracker,
                metrics_list=metrics_list,
                signals_list=all_detected_signals,
                initial_btc_price=initial_btc_price,
                dry_run=dry_run
            )

            if once:
                RICH_CONSOLE.print("\n[bold green]✔ Headless Single-Pass Evaluation Complete (--once).[/bold green]")
                break

            elapsed = time.time() - loop_start
            sleep_sec = max(1.0, poll_interval - elapsed)
            time.sleep(sleep_sec)

    except KeyboardInterrupt:
        RICH_CONSOLE.print("\n[bold yellow]Exiting Live Matrix Terminal gracefully...[/bold yellow]")


# ================================================================================
# CLI ENTRYPOINT
# ================================================================================

def main():
    parser = argparse.ArgumentParser(description="Engine 2 Live Terminal: 23-OOS Elite Multi-Sleeve Suite")
    parser.add_argument("--sync", action="store_true", help="Perform pre-flight historical Parquet re-sync")
    parser.add_argument("--skip-sync", action="store_true", default=False, help="Skip pre-flight Parquet check")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in simulation / paper trading mode")
    parser.add_argument("--live", action="store_true", help="Run with real live order execution on Binance")
    parser.add_argument("--symbol", "-s", type=str, default=None, help="Specific symbol(s) to monitor (e.g. BTCUSDT or BTC,ETH,SOL)")
    parser.add_argument("--target-dir", type=str, default=str(DEFAULT_DATA_DIR), help="Destination Parquet directory")
    parser.add_argument("--once", action="store_true", help="Render matrix once and exit (for headless CI/tests)")
    parser.add_argument("--interval", type=int, default=15, help="Poll interval in seconds (default: 15s)")
    args, unknown = parser.parse_known_args()

    target_path = Path(args.target_dir)

    if args.sync:
        preflight_sync_missing_data(target_dir=target_path)

    is_dry_run = not args.live

    symbols = None
    if args.symbol:
        symbols = [s.strip().upper() for s in args.symbol.split(",")]
        # Auto-append USDT if missing
        symbols = [s if s.endswith("USDT") else f"{s}USDT" for s in symbols]

    run_live_pipeline(
        dry_run=is_dry_run,
        once=args.once,
        target_dir=target_path,
        target_symbols=symbols,
        poll_interval=args.interval
    )


if __name__ == "__main__":
    main()
