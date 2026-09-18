"""
================================================================================
ENGINE 2: PRODUCTION-READY FOREX ML LIVE DRY-RUN TERMINAL (RICH DASHBOARD)
================================================================================
Features:
1. RICH INSTITUTIONAL UI: Color-coded live telemetry table using the `rich` library.
2. TRANSPARENT DECISION TELEMETRY: Explicitly shows WHY trades are held
   (e.g., HOLD (Off-Hours), HOLD (No FVG), HOLD (P* < 0.54), or DRY-BUY / DRY-SELL).
3. 24/7 OVERRIDE (--ignore-kz): Allows testing signal triggers and order geometry
   outside standard London/NY kill zones.
4. ATOMIC PRE-FLIGHT SYNC: Zero file locking on Windows via temporary file replacement.
5. ZERO-TRADE SAFETY LOCKOUT: DRY_RUN = True is strictly enforced.
================================================================================
"""
import os
import sys
import time
import argparse
import logging
from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
import xgboost as xgb
import MetaTrader5 as mt5

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Local imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.live.mt5_connection import MT5Connection
from Engine.live.inference_engine import StatefulInferenceEngine
from Engine.live.order_manager import OrderManager, MAX_CONCURRENT_POSITIONS
from Engine.core.strategy_kernel import CANONICAL_FEATURES, CANONICAL_18_ASSETS
from Engine.forex_engine import (
    calculate_adaptive_sl_tp,
    BASE_RISK_USD,
    CORRELATION_CLUSTERS,
    EXOTIC_SESSION_RESTRICTED,
    RECONCILE_HEARTBEAT_INTERVAL_SEC
)

ASSETS = CANONICAL_18_ASSETS
DATA_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data"))
LOG_FILE = os.path.join(SCRIPT_DIR, "dry_run.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

if sys.platform == "win32":
    os.system('chcp 65001 > nul 2>&1')
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import shutil

def get_terminal_width() -> int:
    try:
        return max(135, shutil.get_terminal_size().columns)
    except Exception:
        return 135

console = Console(force_terminal=True, width=get_terminal_width())
DRY_RUN = True
BASE_RISK_USD = 25.0  # 0.50% on 5,000 USD capital preservation


# ============================================================================
# PRE-FLIGHT DATA GAP SYNCHRONIZATION
# ============================================================================
def robust_parquet_replace(tmp_file, target_file, max_retries=5, base_delay=0.1):
    import time
    for attempt in range(max_retries):
        try:
            os.replace(tmp_file, target_file)
            return True
        except PermissionError:
            time.sleep(base_delay * (2 ** attempt))
    try:
        os.replace(tmp_file, target_file)
        return True
    except Exception as e:
        logging.error(f"Failed to replace {target_file} after {max_retries} retries: {e}")
        try:
            os.remove(tmp_file)
        except:
            pass
        raise

def pre_flight_data_sync(mt5_conn: MT5Connection, single_asset=None):
    """
    Checks each asset's parquet file in Forex_Backtesting_Data/ and appends
    any missing closed candles up to the current moment using true UTC time.
    """
    if single_asset is None:
        print("=" * 115)
        print(" [PRE-FLIGHT] Checking and synchronizing missing candles from MT5 server (True UTC)...")
        print("=" * 115)

    total_appended = 0
    now_utc = datetime.now(timezone.utc)
    broker_offset = mt5_conn.get_broker_utc_offset()

    assets_to_sync = [single_asset] if single_asset else ASSETS

    for asset in assets_to_sync:
        real_symbol = mt5_conn.resolve_symbol(asset)
        base_name = asset
        m15_file = os.path.join(DATA_DIR, f"{base_name}_15m_real.parquet")
        if not os.path.exists(m15_file) and base_name == "GER30":
            base_name = "GER40"
            m15_file = os.path.join(DATA_DIR, f"{base_name}_15m_real.parquet")
        elif not os.path.exists(m15_file) and base_name == "GER40":
            if os.path.exists(os.path.join(DATA_DIR, "GER30_15m_real.parquet")):
                base_name = "GER30"
                m15_file = os.path.join(DATA_DIR, "GER30_15m_real.parquet")

        if not os.path.exists(m15_file):
            continue

        try:
            df_existing = pd.read_parquet(m15_file)
            if 'datetime' in df_existing.columns:
                last_dt = pd.to_datetime(df_existing['datetime'].max())
                if last_dt.tzinfo is None:
                    last_dt = last_dt.tz_localize('UTC')
            elif 'time' in df_existing.columns:
                last_dt = pd.to_datetime(df_existing['time'].max(), unit='s', utc=True)
            else:
                continue

            fetch_from = last_dt + timedelta(seconds=1)
            fetch_from_broker = fetch_from + timedelta(seconds=broker_offset)
            cutoff_broker = now_utc + timedelta(seconds=broker_offset)

            rates = mt5.copy_rates_range(real_symbol, mt5.TIMEFRAME_M15, fetch_from_broker, cutoff_broker)

            if rates is not None and len(rates) > 0:
                df_new = pd.DataFrame(rates)
                df_new['time'] = df_new['time'] - broker_offset
                df_new['datetime'] = pd.to_datetime(df_new['time'], unit='s', utc=True)
                df_new = df_new[df_new['datetime'] + timedelta(minutes=15) <= now_utc]

                if len(df_new) > 0:
                    new_rows = pd.DataFrame()
                    new_rows['time'] = df_new['time'].values
                    new_rows['datetime'] = df_new['datetime'].values
                    new_rows['open'] = df_new['open'].values
                    new_rows['high'] = df_new['high'].values
                    new_rows['low'] = df_new['low'].values
                    new_rows['close'] = df_new['close'].values
                    new_rows['tick_volume'] = df_new['tick_volume'].astype(np.uint64).values
                    new_rows['spread'] = df_new['spread'].astype(np.int32).values
                    new_rows['real_volume'] = df_new['real_volume'].astype(np.uint64).values

                    df_combined = pd.concat([df_existing, new_rows], ignore_index=True)
                    df_combined = df_combined.drop_duplicates(subset=['time'], keep='first').sort_values('time').reset_index(drop=True)
                    tmp_file = m15_file + ".tmp"
                    df_combined.to_parquet(tmp_file, index=False)
                    robust_parquet_replace(tmp_file, m15_file)
                    
                    if single_asset is None:
                        print(f"  -> [{asset:<7}] Appended +{len(new_rows):>2} missing candles (Up to {df_combined['datetime'].iloc[-1].strftime('%Y-%m-%d %H:%M UTC')})")
                    else:
                        logging.info(f"[{asset}] Live telemetry appended +{len(new_rows)} candles to parquet.")
                    total_appended += len(new_rows)
                else:
                    if single_asset is None:
                        print(f"  -> [{asset:<7}] 100% Up-to-date (Last: {last_dt.strftime('%Y-%m-%d %H:%M UTC')})")
            else:
                if single_asset is None:
                    print(f"  -> [{asset:<7}] 100% Up-to-date (Last: {last_dt.strftime('%Y-%m-%d %H:%M UTC')})")
        except Exception as e:
            logging.error(f"Pre-flight sync error for {asset}: {e}")
            if single_asset is None:
                print(f"  -> [{asset:<7}] Sync Error: {e}")

    if single_asset is None:
        print(f"\n [PRE-FLIGHT COMPLETE] Total new bars appended: {total_appended}")
        print("=" * 115)
        time.sleep(0.5)


# ============================================================================
# MODEL MANAGEMENT
# ============================================================================
def load_production_model() -> xgb.Booster:
    model_path = os.path.join(PROJECT_ROOT, "Engine", "models", "xgboost_forex.json")
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"[FATAL] Production model not found at {model_path}. "
            f"Run 'python Engine/forex_engine.py --mode train' to generate valid weights!"
        )
    model = xgb.Booster()
    model.load_model(model_path)
    logging.info(f"Loaded certified production XGBoost model from {model_path} ({os.path.getsize(model_path):,} bytes)")
    return model


# ============================================================================
# MAIN LIVE DRY-RUN TERMINAL (RICH UI)
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description="Production Live Forex & CFD Telemetry Terminal (Rich UI).")
    parser.add_argument("--interval", type=float, default=1.5, help="Polling interval in seconds (default: 1.5)")
    parser.add_argument("--once", action="store_true", help="Run a single evaluation pass across all assets and exit.")
    parser.add_argument("--ignore-kz", action="store_true", help="Bypass the London/NY kill zone filter for 24/7 dry-run signal testing.")
    parser.add_argument(
        "--strategy",
        choices=["fvg", "ml", "combined"],
        default="combined",
        help="Strategy logic to execute: 'fvg' (Rule-Based ICT FVG), 'ml' (Pure XGBoost Probability), 'combined' (Dual Confluence: FVG + ML)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Run in paper dry-run mode without sending real orders to broker (default: True)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Arm real live market execution mode in MetaTrader 5"
    )
    args = parser.parse_args()
    
    is_dry_run = not args.live
    strat_mode = args.strategy

    console.print(Panel("[bold cyan]INITIALIZING INSTITUTIONAL MT5 DRY-RUN TERMINAL[/bold cyan]\n[dim]Connecting to MetaTrader 5 broker feed...[/dim]", border_style="cyan"))

    mt5_conn = MT5Connection()
    if not mt5_conn.connect():
        console.print("[bold red][FATAL] Could not connect to MetaTrader 5 terminal. Ensure MT5 is running![/bold red]")
        sys.exit(1)

    # Pre-flight data sync
    pre_flight_data_sync(mt5_conn)

    # Load Model
    xgb_model = load_production_model()

    # Initialize Order Manager (Strictly pass dry_run flag)
    order_mgr = OrderManager(mt5_conn, dry_run=is_dry_run)

    # Warm-start Stateful Inference Engines
    engines = {}
    last_candle_times = {}
    console.print("[bold cyan]Warm-starting rolling state buffers for 18 assets...[/bold cyan]")
    for asset in ASSETS:
        engine = StatefulInferenceEngine(asset)
        if engine.warm_start(mt5_conn):
            engines[asset] = engine
            if not engine.buffer.empty:
                last_candle_times[asset] = engine.buffer.index[-1]
        else:
            logging.warning(f"Could not warm-start {asset}. Skipped.")

    console.print(f"[bold green]Successfully warm-started {len(engines)}/{len(ASSETS)} assets.[/bold green]")
    console.print("[bold yellow]Launching real-time live telemetry stream (DRY RUN MODE)...[/bold yellow]\n")
    time.sleep(1.0)

    start_time = datetime.now()
    signals_count = 0
    last_reconcile_time = 0.0

    try:
        while True:
            # Operational Safeguard 3: Broker Position Reconciliation Heartbeat (every 30 seconds)
            if time.time() - last_reconcile_time >= RECONCILE_HEARTBEAT_INTERVAL_SEC:
                order_mgr.reconcile_with_broker()
                last_reconcile_time = time.time()

            # Reconnection logic & dynamic account updates

            acc = mt5.account_info()
            if acc is None:
                logging.warning("MT5 connection lost in telemetry loop. Attempting to reconnect...")
                if not mt5_conn.connect():
                    time.sleep(5)
                    continue
                acc = mt5.account_info()
            
            acc_dict = acc._asdict() if acc is not None else {"login": "UNKNOWN", "server": "UNKNOWN", "balance": 0.0, "equity": 0.0}

            # Manage active positions: microstructure ratchets & 24-bar decay
            first_candle_time = list(last_candle_times.values())[0] if last_candle_times else None
            order_mgr.manage_open_trades(current_bar_time=first_candle_time)

            utc_now = datetime.now(timezone.utc)
            # London KZ: 07-10 UTC | NY KZ: 12-15 UTC
            # Use the hour of the last closed bar to prevent wall-clock race conditions
            last_closed_hour = utc_now.hour
            if last_candle_times:
                first_asset = list(last_candle_times.keys())[0]
                if last_candle_times[first_asset] is not None:
                    last_closed_hour = last_candle_times[first_asset].hour

            is_london = (7 <= last_closed_hour <= 10)
            is_ny = (12 <= last_closed_hour <= 15)
            is_natural_kz = is_london or is_ny
            is_kz = True if args.ignore_kz else is_natural_kz

            if args.ignore_kz:
                kz_display = "[bold magenta]BYPASSED (24/7 TEST)[/bold magenta]"
            elif is_london:
                kz_display = "[bold green]ACTIVE (London Open)[/bold green]"
            elif is_ny:
                kz_display = "[bold green]ACTIVE (NY Open)[/bold green]"
            else:
                kz_display = "[dim red]OFF-HOURS[/dim red]"

            console.width = get_terminal_width()
            # Build Rich Table
            table = Table(
                title=f"MT5 LIVE FOREX & CFD TELEMETRY | UTC: {utc_now.strftime('%H:%M:%S')}",
                header_style="bold bright_white on blue",
                border_style="blue",
                show_lines=False,
                expand=True
            )

            table.add_column("Asset", style="bold cyan", no_wrap=True)
            table.add_column("Bid", justify="right")
            table.add_column("Ask", justify="right")
            table.add_column("Spread", justify="right", style="yellow")
            table.add_column("RSI", justify="right")
            table.add_column("VWAP%", justify="right")
            table.add_column("EMA50%", justify="right")
            table.add_column("EMA200%", justify="right")
            table.add_column("4H Trend", justify="center")
            table.add_column("FVG", justify="center")
            table.add_column("P*", justify="right")
            table.add_column("Decision / Trigger Reason", justify="left", ratio=2)

            eval_data = {}
            candidates = []

            for asset, engine in engines.items():
                tick = mt5_conn.get_last_tick(asset)
                if tick is None:
                    continue

                bid = tick.bid
                ask = tick.ask
                spread = (ask - bid)

                # Check for new closed 15m candle
                latest_rates = mt5_conn.get_15m_bars(asset, count=2)
                if not latest_rates.empty and len(latest_rates) >= 2:
                    closed_bar = latest_rates.iloc[-2]
                    closed_bar_time = closed_bar['datetime']
                    if last_candle_times.get(asset) != closed_bar_time:
                        new_bar = {
                            'datetime': closed_bar_time,
                            'open': closed_bar['open'],
                            'high': closed_bar['high'],
                            'low': closed_bar['low'],
                            'close': closed_bar['close'],
                            'volume': closed_bar['tick_volume']
                        }
                        engine.update_bar(new_bar)
                        engine.refresh_4h_buffer()
                        last_candle_times[asset] = closed_bar_time
                        
                        # Append closed candle to persistent parquet storage immediately
                        pre_flight_data_sync(mt5_conn, single_asset=asset)

                # Compute features & probability
                try:
                    prob = engine.predict(xgb_model)
                    features = engine.compute_features().iloc[-1]
                except Exception as e:
                    logging.error(f"Inference error for {asset}: {e}")
                    continue

                rsi = features.get('rsi_14', 50.0)
                vwap_dist = features.get('vwap_dist', 0.0) * 100.0
                ema50_dist = features.get('ema_50_dist', 0.0) * 100.0
                ema200_dist = features.get('ema_200_dist', 0.0) * 100.0

                trend_val = features.get('htf_4h_trend', 0.0)
                if trend_val > 0:
                    trend_cell = "[bold green]BULL[/bold green]"
                elif trend_val < 0:
                    trend_cell = "[bold red]BEAR[/bold red]"
                else:
                    trend_cell = "[dim]FLAT[/dim]"

                bull_fvg = features.get('bullish_fvg', 0.0)
                bear_fvg = features.get('bearish_fvg', 0.0)
                if bull_fvg > 0:
                    fvg_cell = "[bold green]BULL[/bold green]"
                elif bear_fvg > 0:
                    fvg_cell = "[bold red]BEAR[/bold red]"
                else:
                    fvg_cell = "[dim]NONE[/dim]"

                # Format RSI styling
                if rsi >= 70:
                    rsi_cell = f"[bold red]{rsi:.1f}[/bold red]"
                elif rsi <= 30:
                    rsi_cell = f"[bold green]{rsi:.1f}[/bold green]"
                else:
                    rsi_cell = f"{rsi:.1f}"

                # Format P* styling
                if prob >= 0.54:
                    prob_cell = f"[bold green]{prob:.3f}[/bold green]"
                else:
                    prob_cell = f"[dim]{prob:.3f}[/dim]"

                # Setup Evaluation with Exact Geometry
                local_low = engine.buffer['low'].rolling(20).min().iloc[-1] if len(engine.buffer) >= 20 else bid * 0.99
                local_high = engine.buffer['high'].rolling(20).max().iloc[-1] if len(engine.buffer) >= 20 else ask * 1.01

                decision_cell = "[dim]HOLD[/dim]"

                # Determine long/short conditions based on selected strategy
                is_long_sig = False
                is_short_sig = False
                strat_tag = "DUAL"

                if strat_mode == "fvg":
                    strat_tag = "FVG"
                    is_long_sig = (trend_val > 0 and bull_fvg > 0)
                    is_short_sig = (trend_val < 0 and bear_fvg > 0)
                elif strat_mode == "ml":
                    strat_tag = "ML"
                    is_long_sig = (trend_val > 0 and prob >= 0.54)
                    is_short_sig = (trend_val < 0 and prob >= 0.54)
                else:  # combined (dual confluence)
                    strat_tag = "DUAL"
                    is_long_sig = (trend_val > 0 and bull_fvg > 0 and prob >= 0.54)
                    is_short_sig = (trend_val < 0 and bear_fvg > 0 and prob >= 0.54)

                atr = float(features.get('atr_14', 0.0))
                current_utc_hour = datetime.now(timezone.utc).hour

                # P1 Check: Spread/ATR Hysteresis Quarantine & Exotic Session Filter
                completed_bar_time = last_candle_times.get(asset)
                is_quarantined, q_reason = engine.check_quarantine(spread, atr, current_utc_hour, bar_time=completed_bar_time)

                # 1. GATING LOGIC FIRST
                if is_quarantined:
                    decision_cell = f"[dim red]{q_reason}[/dim red]"
                elif not is_kz:
                    decision_cell = "[dim yellow]HOLD (Off-Hours)[/dim yellow]"

                # 2. EVALUATE LONG SETUP
                elif is_long_sig:
                    entry = ask
                    sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                        symbol=asset,
                        is_long=True,
                        entry=entry,
                        raw_sl=local_low,
                        local_extreme=local_low,
                        spread=spread,
                        atr=atr,
                        tp_structural=local_high
                    )
                    if not valid:
                        decision_cell = f"[dim red]{reason}[/dim red]"
                    else:
                        candidates.append({
                            'asset': asset,
                            'is_long': True,
                            'entry': entry,
                            'sl': sl,
                            'tp': tp,
                            'r_dist': r_dist,
                            'strat_tag': strat_tag,
                            'prob': prob,
                            'reason': reason
                        })
                        decision_cell = "[bold green]SIGNAL (Pending Queue)[/bold green]"

                # 3. EVALUATE SHORT SETUP
                elif is_short_sig:
                    entry = bid
                    sl, tp, r_dist, valid, reason = calculate_adaptive_sl_tp(
                        symbol=asset,
                        is_long=False,
                        entry=entry,
                        raw_sl=local_high,
                        local_extreme=local_high,
                        spread=spread,
                        atr=atr,
                        tp_structural=local_low
                    )
                    if not valid:
                        decision_cell = f"[dim red]{reason}[/dim red]"
                    else:
                        candidates.append({
                            'asset': asset,
                            'is_long': False,
                            'entry': entry,
                            'sl': sl,
                            'tp': tp,
                            'r_dist': r_dist,
                            'strat_tag': strat_tag,
                            'prob': prob,
                            'reason': reason
                        })
                        decision_cell = "[bold red]SIGNAL (Pending Queue)[/bold red]"

                # 4. DIAGNOSTIC REASON FOR NO SIGNAL
                else:
                    if strat_mode == "fvg":
                        if bull_fvg == 0 and bear_fvg == 0:
                            decision_cell = "[dim]HOLD (No FVG)[/dim]"
                        elif (trend_val > 0 and bear_fvg > 0) or (trend_val < 0 and bull_fvg > 0):
                            decision_cell = "[dim yellow]HOLD (Trend Opposed)[/dim yellow]"
                        else:
                            decision_cell = "[dim]HOLD[/dim]"
                    elif strat_mode == "ml":
                        if prob < 0.54:
                            decision_cell = f"[dim]HOLD (P*={prob:.2f}<0.54)[/dim]"
                        elif trend_val == 0:
                            decision_cell = "[dim yellow]HOLD (Flat Trend)[/dim yellow]"
                        else:
                            decision_cell = "[dim]HOLD[/dim]"
                    else:
                        if bull_fvg == 0 and bear_fvg == 0:
                            decision_cell = "[dim]HOLD (No FVG)[/dim]"
                        elif prob < 0.54:
                            decision_cell = f"[dim]HOLD (P*={prob:.2f}<0.54)[/dim]"
                        elif (trend_val > 0 and bear_fvg > 0) or (trend_val < 0 and bull_fvg > 0):
                            decision_cell = "[dim yellow]HOLD (Trend Opposed)[/dim yellow]"
                        else:
                            decision_cell = "[dim]HOLD[/dim]"

                eval_data[asset] = {
                    'bid_str': f"{bid:.5f}",
                    'ask_str': f"{ask:.5f}",
                    'spread_str': f"{spread:.5f}",
                    'rsi_cell': rsi_cell,
                    'vwap_str': f"{vwap_dist:+.2f}%",
                    'ema50_str': f"{ema50_dist:+.2f}%",
                    'ema200_str': f"{ema200_dist:+.2f}%",
                    'trend_cell': trend_cell,
                    'fvg_cell': fvg_cell,
                    'prob_cell': prob_cell,
                    'decision_cell': decision_cell
                }

            # ====================================================================
            # CANDIDATE ARBITRATION: HIGHEST PROBABILITY (P*) FIRST
            # ====================================================================
            candidates.sort(key=lambda c: c['prob'], reverse=True)

            for cand in candidates:
                asset = cand['asset']
                can_open, veto_reason = order_mgr.can_open_trade(asset)
                calc_lots = order_mgr.calculate_lot_size(asset, risk_usd=BASE_RISK_USD, sl_dist=cand['r_dist'])

                if not can_open:
                    eval_data[asset]['decision_cell'] = f"[dim yellow]HOLD ({veto_reason})[/dim yellow]"
                else:
                    is_long = cand['is_long']
                    strat_tag = cand['strat_tag']
                    prob = cand['prob']
                    entry = cand['entry']
                    sl = cand['sl']
                    tp = cand['tp']
                    action_label = f"DRY-{'BUY' if is_long else 'SELL'} ({strat_tag})" if is_dry_run else f"LIVE-{'BUY' if is_long else 'SELL'} ({strat_tag})"
                    style_tag = "bold white on green" if is_long else "bold white on red"
                    eval_data[asset]['decision_cell'] = f"[{style_tag}] {action_label} ({calc_lots:.2f}L) [/{style_tag}]"
                    signals_count += 1
                    log_msg = f"[{'DRY-RUN' if is_dry_run else 'LIVE'} SIGNAL: {asset} | {'BUY' if is_long else 'SELL'} ({strat_tag}) | P*={prob:.3f} | ENTRY={entry:.5f} | SL={sl:.5f} | TP={tp:.5f} | LOTS={calc_lots} | REASON={cand['reason']}]"
                    logging.info(log_msg)
                    if not is_dry_run:
                        order_type = mt5.ORDER_TYPE_BUY if is_long else mt5.ORDER_TYPE_SELL
                        order_mgr.place_market_order(asset, order_type, volume=calc_lots, sl_price=sl, tp_price=tp, risk_usd=BASE_RISK_USD)

            # Mark active open positions directly in scanner decision cell
            for ticket, trade_info in order_mgr.open_trades.items():
                sym_clean = trade_info["symbol"].upper().replace(".PI", "").replace(".P", "").replace(".R", "")
                for asset in ASSETS:
                    if asset.upper() == sym_clean and asset in eval_data:
                        direction = "BUY" if trade_info["type"] == 0 else "SELL"
                        pos_mt5 = mt5.positions_get(ticket=ticket)
                        profit_usd = pos_mt5[0].profit if (pos_mt5 and len(pos_mt5) > 0) else 0.0
                        pnl_sign = "+" if profit_usd >= 0 else ""
                        eval_data[asset]['decision_cell'] = f"[bold white on blue] ACTIVE TRADE: {direction} {trade_info['volume']}L ({pnl_sign}{profit_usd:.2f} USD) [/bold white on blue]"

            # Build Table Rows in canonical asset order
            for asset in ASSETS:
                if asset not in eval_data:
                    continue
                ed = eval_data[asset]
                table.add_row(
                    asset,
                    ed['bid_str'],
                    ed['ask_str'],
                    ed['spread_str'],
                    ed['rsi_cell'],
                    ed['vwap_str'],
                    ed['ema50_str'],
                    ed['ema200_str'],
                    ed['trend_cell'],
                    ed['fvg_cell'],
                    ed['prob_cell'],
                    ed['decision_cell']
                )

            # Build Live Open Positions Table if positions exist
            pos_table = None
            if order_mgr.open_trades:
                pos_table = Table(
                    title=f"LIVE ACTIVE BROKER POSITIONS ({len(order_mgr.open_trades)} / {MAX_CONCURRENT_POSITIONS} Max)",
                    header_style="bold black on bright_green",
                    border_style="bright_green",
                    expand=True
                )
                pos_table.add_column("Ticket", style="bold cyan", justify="center")
                pos_table.add_column("Asset", style="bold white", justify="left")
                pos_table.add_column("Type", justify="center")
                pos_table.add_column("Lots", justify="right")
                pos_table.add_column("Entry Price", justify="right")
                pos_table.add_column("Current Price", justify="right")
                pos_table.add_column("PnL (USD)", justify="right")
                pos_table.add_column("Current R", justify="right")
                pos_table.add_column("Stop Loss", justify="right")
                pos_table.add_column("Take Profit", justify="right")
                pos_table.add_column("Decay Bars", justify="center")
                pos_table.add_column("Ratchet Status", justify="left")

                for ticket, trade_info in order_mgr.open_trades.items():
                    pos_mt5 = mt5.positions_get(ticket=ticket)
                    if pos_mt5 and len(pos_mt5) > 0:
                        p = pos_mt5[0]
                        current_p = p.price_current
                        profit_usd = p.profit
                    else:
                        current_p = trade_info["entry_price"]
                        profit_usd = 0.0

                    direction = "BUY" if trade_info["type"] == 0 else "SELL"
                    dir_style = "[bold green]BUY[/bold green]" if trade_info["type"] == 0 else "[bold red]SELL[/bold red]"
                    pnl_style = f"[bold green]{profit_usd:+.2f} USD[/bold green]" if profit_usd >= 0 else f"[bold red]{profit_usd:+.2f} USD[/bold red]"
                    
                    r_dist = trade_info.get("r_dist", 0.0001)
                    if trade_info["type"] == 0:
                        curr_r = (current_p - trade_info["entry_price"]) / r_dist if r_dist > 0 else 0.0
                    else:
                        curr_r = (trade_info["entry_price"] - current_p) / r_dist if r_dist > 0 else 0.0
                    r_style = f"[bold green]{curr_r:+.2f}R[/bold green]" if curr_r >= 0 else f"[bold red]{curr_r:+.2f}R[/bold red]"

                    high_r = trade_info.get("highest_r", 0.0)
                    ratchet_label = "Base SL"
                    if high_r >= 3.5:
                        ratchet_label = "[bold bright_green]Lock 3.3R[/bold bright_green]"
                    elif high_r >= 3.0:
                        ratchet_label = "[bold bright_green]Lock 2.8R[/bold bright_green]"
                    elif high_r >= 2.5:
                        ratchet_label = "[bold green]Lock 2.3R[/bold green]"
                    elif high_r >= 2.0:
                        ratchet_label = "[bold green]Lock 1.8R[/bold green]"
                    elif high_r >= 1.5:
                        ratchet_label = "[bold cyan]Lock 1.0R[/bold cyan]"
                    elif high_r >= 1.0:
                        ratchet_label = "[bold cyan]BE Lock (+0.15R)[/bold cyan]"

                    pos_table.add_row(
                        str(ticket),
                        trade_info["symbol"],
                        dir_style,
                        f"{trade_info['volume']:.2f}",
                        f"{trade_info['entry_price']:.5f}",
                        f"{current_p:.5f}",
                        pnl_style,
                        r_style,
                        f"{trade_info['sl']:.5f}",
                        f"{trade_info['tp']:.5f}",
                        f"{trade_info.get('bars_elapsed', 0)}/24",
                        ratchet_label
                    )

            # Header info panel
            uptime = str(datetime.now() - start_time).split('.')[0]
            safety_label = "[bold green]DRY-RUN MODE (Zero Real Orders)[/bold green]" if is_dry_run else "[bold red]LIVE EXECUTION MODE (REAL ORDERS ARMED)[/bold red]"
            strat_label = f"[bold cyan]{strat_mode.upper()}[/bold cyan] ({'Rule-Based ICT FVG' if strat_mode == 'fvg' else ('Pure XGBoost ML' if strat_mode == 'ml' else 'Dual Confluence: FVG + ML')})"
            header_text = (
                f"[bold white]Account:[/bold white] #{acc_dict.get('login')} ({acc_dict.get('server')})  |  "
                f"[bold white]Balance:[/bold white] {acc_dict.get('balance'):,.2f} USD  |  "
                f"[bold white]Equity:[/bold white] {acc_dict.get('equity'):,.2f} USD\n"
                f"[bold white]Strategy:[/bold white] {strat_label}  |  "
                f"[bold white]Kill Zone:[/bold white] {kz_display}  |  "
                f"[bold white]Signals Logged:[/bold white] {signals_count}  |  "
                f"[bold white]Mode:[/bold white] {safety_label}"
            )
            header_panel = Panel(header_text, title="[bold bright_cyan]ENGINE: UNIFIED FOREX & CFD MASTER TERMINAL[/bold bright_cyan]", border_style="cyan", expand=True)

            # Clear screen for live loop
            if not args.once:
                console.clear()

            console.print(header_panel)
            if pos_table is not None:
                console.print(pos_table)
            console.print(table)
            console.print("[dim]Press Ctrl+C to safely disconnect and exit.[/dim]\n")

            if args.once:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        console.print("\n\n[bold yellow][SHUTDOWN] Exiting live dry-run loop safely. Disconnecting from MT5...[/bold yellow]")
    finally:
        mt5_conn.disconnect()
        console.print("[bold green][SHUTDOWN] MT5 disconnected cleanly. All state saved.[/bold green]\n")


if __name__ == "__main__":
    main()
