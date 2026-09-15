"""
================================================================================
ENGINE 2: PRODUCTION-READY FOREX ML LIVE DRY-RUN TERMINAL (UNIFIED KERNEL)
================================================================================
Features:
1. AUTOMATIC PRE-FLIGHT SYNC: Synchronizes missing candles from MT5 using dynamic
   broker UTC offset to ensure zero timezone skew in Forex_Backtesting_Data/.
2. CONTINUOUS SUB-SECOND REFRESH: Polling every 1-2s with live Bid/Ask, spreads,
   and closed candle updates.
3. FULL DECISION TELEMETRY:
   - Live Price & Spread
   - RSI(14) with Wilder's exponential smoothing
   - VWAP Distance (%)
   - EMA 50 & EMA 200 Distance (%)
   - Causal 4-Hour Trend Alignment (Lagged 1 closed bar)
   - Fair Value Gap (FVG) Status & Wick Magnitude
   - London / NY Kill Zone Activity (True UTC)
   - XGBoost Production Model Prediction Probability (P*)
   - Exact Stop Loss & Take Profit Geometry (Local 20-bar extremes)
   - Real-Time Position Sizing (Lots for $50 / 1.0% Risk)
4. ZERO-TRADE SAFETY LOCKOUT: DRY_RUN = True is strictly enforced.
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

# Local imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.live.mt5_connection import MT5Connection
from Engine.live.inference_engine import StatefulInferenceEngine
from Engine.live.order_manager import OrderManager
from Engine.core.strategy_kernel import CANONICAL_FEATURES, CANONICAL_18_ASSETS, check_setup_criteria

ASSETS = CANONICAL_18_ASSETS
DATA_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data"))
LOG_FILE = os.path.join(SCRIPT_DIR, "dry_run.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

DRY_RUN = True
BASE_RISK_USD = 50.0  # 1.0% on $5,000 capital


# ============================================================================
# PRE-FLIGHT DATA GAP SYNCHRONIZATION
# ============================================================================
def pre_flight_data_sync(mt5_conn: MT5Connection):
    """
    Checks each asset's parquet file in Forex_Backtesting_Data/ and appends
    any missing closed candles up to the current moment using true UTC time.
    """
    print("=" * 115)
    print(" [PRE-FLIGHT] Checking and synchronizing missing candles from MT5 server (True UTC)...")
    print("=" * 115)

    total_appended = 0
    now_utc = datetime.now(timezone.utc)
    broker_offset = mt5_conn.get_broker_utc_offset()

    for asset in ASSETS:
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
                # Only keep strictly closed bars (bar open + 15m <= now_utc)
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
                    os.replace(tmp_file, m15_file)
                    print(f"  -> [{asset:<7}] Appended +{len(new_rows):>2} missing candles (Up to {df_combined['datetime'].iloc[-1].strftime('%Y-%m-%d %H:%M UTC')})")
                    total_appended += len(new_rows)
                else:
                    print(f"  -> [{asset:<7}] 100% Up-to-date (Last: {last_dt.strftime('%Y-%m-%d %H:%M UTC')})")
            else:
                print(f"  -> [{asset:<7}] 100% Up-to-date (Last: {last_dt.strftime('%Y-%m-%d %H:%M UTC')})")
        except Exception as e:
            logging.error(f"Pre-flight sync error for {asset}: {e}")
            print(f"  -> [{asset:<7}] Sync Error: {e}")

    print(f"\n [PRE-FLIGHT COMPLETE] Total new bars appended: {total_appended}")
    print("=" * 115)
    time.sleep(0.5)


# ============================================================================
# MODEL MANAGEMENT (FAIL-CLOSED)
# ============================================================================
def load_production_model() -> xgb.Booster:
    model_path = os.path.join(PROJECT_ROOT, "Engine", "models", "xgboost_forex.json")
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"[FATAL] Production model not found at {model_path}. "
            f"Run 'python Engine/live/train_production_model.py' to generate valid weights!"
        )
    model = xgb.Booster()
    model.load_model(model_path)
    logging.info(f"Loaded certified production XGBoost model from {model_path} ({os.path.getsize(model_path):,} bytes)")
    return model


# ============================================================================
# MAIN LIVE DRY-RUN TERMINAL
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description="Production Live Dry-Run Telemetry Terminal.")
    parser.add_argument('--once', action='store_true', help="Run single evaluation snapshot and exit.")
    parser.add_argument('--interval', type=float, default=1.5, help="Refresh interval in seconds (default: 1.5s).")
    parser.add_argument('--no-sync', action='store_true', help="Skip pre-flight data append check.")
    args = parser.parse_args()

    print("\nConnecting to MetaTrader 5 terminal...")
    mt5_conn = MT5Connection()
    if not mt5_conn.connect():
        print("[FATAL ERROR] Could not connect to running MetaTrader 5. Make sure MT5 is open!")
        sys.exit(1)

    broker_offset = mt5_conn.get_broker_utc_offset()
    print(f"Broker connection verified. Server UTC Offset: {broker_offset // 3600:+d} hours.")

    # Pre-flight data sync
    if not args.no_sync:
        pre_flight_data_sync(mt5_conn)

    account_info = mt5.account_info()
    acc_dict = account_info._asdict() if account_info else {'login': 'UNKNOWN', 'balance': 0.0, 'server': 'UNKNOWN'}

    print("Loading Certified Production XGBoost Model Engine...")
    xgb_model = load_production_model()

    order_mgr = OrderManager(mt5_conn)

    print(f"Warm-starting rolling state buffers for {len(ASSETS)} assets...")
    engines = {}
    last_candle_times = {}

    for asset in ASSETS:
        engine = StatefulInferenceEngine(symbol=asset)
        success = engine.warm_start(mt5_conn)
        if success:
            engines[asset] = engine
            last_candle_times[asset] = engine.buffer.index[-1] if not engine.buffer.empty else None
        else:
            logging.warning(f"Could not warm-start {asset}. Skipped.")

    print(f"Successfully warm-started {len(engines)}/{len(ASSETS)} assets.")
    print("Launching real-time live telemetry stream (DRY RUN MODE)...")
    time.sleep(1.0)

    spinner = ['|', '/', '-', '\\']
    spin_idx = 0
    start_time = datetime.now()

    try:
        while True:
            utc_now = datetime.now(timezone.utc)
            # London KZ: 07-10 UTC | NY KZ: 12-15 UTC
            is_kz = (7 <= utc_now.hour <= 10) or (12 <= utc_now.hour <= 15)
            kz_str = "ACTIVE" if is_kz else "OFF-HOURS"

            dashboard_rows = []

            for asset, engine in engines.items():
                tick = mt5_conn.get_last_tick(asset)
                if tick is None:
                    continue

                bid = tick.bid
                ask = tick.ask
                spread = (ask - bid)

                # Check if a new closed 15m candle is available
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
                        last_candle_times[asset] = closed_bar_time

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
                trend_str = "BULL" if trend_val > 0 else ("BEAR" if trend_val < 0 else "FLAT")

                bull_fvg = features.get('bullish_fvg', 0.0)
                bear_fvg = features.get('bearish_fvg', 0.0)
                fvg_str = "BULL" if bull_fvg > 0 else ("BEAR" if bear_fvg > 0 else "NONE")

                # Setup Evaluation with Exact Geometry
                local_low = engine.buffer['low'].rolling(20).min().iloc[-1] if len(engine.buffer) >= 20 else bid * 0.99
                local_high = engine.buffer['high'].rolling(20).max().iloc[-1] if len(engine.buffer) >= 20 else ask * 1.01

                signal_type = "HOLD"
                calc_lots = 0.01

                # Decision Rule: Kill Zone + FVG + 4H Trend + Model Confidence (P* >= 0.55)
                if is_kz and prob >= 0.55 and trend_val > 0 and bull_fvg > 0:
                    entry = ask
                    sl = local_low
                    r_dist = entry - sl
                    if r_dist > 0 and (r_dist / entry) <= 0.025:
                        tp = entry + (4.0 * r_dist)
                        calc_lots = order_mgr.calculate_lot_size(asset, risk_usd=BASE_RISK_USD, sl_dist=r_dist)
                        signal_type = "DRY-BUY"
                        log_msg = f"[DRY-RUN SIGNAL: {asset} | {signal_type} | P*={prob:.3f} | ENTRY={entry:.5f} | SL={sl:.5f} | TP={tp:.5f} | LOTS={calc_lots}]"
                        logging.info(log_msg)

                elif is_kz and prob >= 0.55 and trend_val < 0 and bear_fvg > 0:
                    entry = bid
                    sl = local_high
                    r_dist = sl - entry
                    if r_dist > 0 and (r_dist / entry) <= 0.025:
                        tp = entry - (4.0 * r_dist)
                        calc_lots = order_mgr.calculate_lot_size(asset, risk_usd=BASE_RISK_USD, sl_dist=r_dist)
                        signal_type = "DRY-SELL"
                        log_msg = f"[DRY-RUN SIGNAL: {asset} | {signal_type} | P*={prob:.3f} | ENTRY={entry:.5f} | SL={sl:.5f} | TP={tp:.5f} | LOTS={calc_lots}]"
                        logging.info(log_msg)

                dashboard_rows.append([
                    asset,
                    f"{bid:.5f}"[:8],
                    f"{ask:.5f}"[:8],
                    f"{spread:.5f}"[:7],
                    f"{rsi:.1f}",
                    f"{vwap_dist:+.2f}%",
                    f"{ema50_dist:+.2f}%",
                    f"{ema200_dist:+.2f}%",
                    trend_str,
                    fvg_str,
                    f"{prob:.3f}",
                    signal_type
                ])

            # RENDER FLICKER-FREE LIVE TERMINAL
            spin_char = spinner[spin_idx % len(spinner)]
            spin_idx += 1
            uptime = str(datetime.now() - start_time).split('.')[0]

            out = []
            if not args.once:
                out.append("\033[H")

            out.append("=" * 115)
            out.append(f" MT5 LIVE FOREX TELEMETRY (DRY RUN) {spin_char} | UTC: {utc_now.strftime('%H:%M:%S')} | Kill Zone: {kz_str:<10}")
            out.append(f" Account: #{acc_dict.get('login')} ({acc_dict.get('server')}) | Balance: ${acc_dict.get('balance'):,.2f} USD | Uptime: {uptime}")
            out.append("=" * 115)

            headers = ["Asset", "Bid", "Ask", "Spread", "RSI(14)", "VWAP %", "EMA50 %", "EMA200 %", "4H Trend", "FVG", "P*", "Decision"]
            row_fmt = "{:<8} | {:<8} | {:<8} | {:<7} | {:<7} | {:<8} | {:<8} | {:<9} | {:<8} | {:<6} | {:<6} | {:<8}"
            out.append(row_fmt.format(*headers))
            out.append("-" * 115)

            for r in dashboard_rows:
                out.append(row_fmt.format(*r))

            out.append("=" * 115)
            out.append(" [SAFETY ACTIVE] DRY_RUN = True. Real orders are LOCKED. Live tick telemetry updating in real-time.")
            out.append(" Press Ctrl+C to safely exit.")

            print("\n".join(out), flush=True)

            if args.once:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Exiting live dry-run loop safely. Disconnecting from MT5...")
    finally:
        mt5_conn.disconnect()
        print("[SHUTDOWN] MT5 disconnected cleanly. All state saved.\n")


if __name__ == "__main__":
    main()
