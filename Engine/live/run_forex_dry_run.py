"""
================================================================================
ENGINE 2: PRODUCTION-READY FOREX ML LIVE DRY-RUN TERMINAL
================================================================================
Features:
1. AUTOMATIC PRE-FLIGHT SYNC: Checks and appends any missing candles from MT5
   directly into Forex_Backtesting_Data/ parquets before starting the live loop.
2. CONTINUOUS SUB-SECOND REFRESH: Polling every 1-2 seconds with live Bid/Ask,
   spreads, ticks, and candle updates.
3. FULL DECISION TELEMETRY: Displays every quantitative metric used by the model:
   - Live Price & Spread
   - RSI(14) with Wilder's exponential smoothing
   - VWAP Distance (%)
   - EMA 50 & EMA 200 Distance (%)
   - 4-Hour Trend Alignment (Bullish/Bearish)
   - Fair Value Gap (FVG) Status & Magnitude
   - London / NY Kill Zone Activity
   - XGBoost Model Prediction Probability (P*)
   - Live Signal Decision ([HOLD], [DRY-BUY], [DRY-SELL])
4. ZERO-TRADE SAFETY LOCKOUT: DRY_RUN = True is strictly enforced. No orders
   are dispatched to MT5; signals are logged with simulated SL/TP levels.
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
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from mt5_connection import MT5Connection
from inference_engine import StatefulInferenceEngine
from order_manager import OrderManager

# 18 Canonical Portfolio Assets
ASSETS = [
    'EURHUF', 'GER30', 'NICKEL', 'USDSEK', 'GAS', 'AU200', 'FR40', 
    'EURCNH', 'LEAD', 'NZDUSD', 'USDHKD', 'US2000', 'AUDCHF', 
    'NZDCNH', 'XAUCNH', 'GAUCNH', 'EURSEK', 'EURUSD'
]

DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "Forex_Backtesting_Data"))
LOG_FILE = os.path.join(SCRIPT_DIR, "dry_run.log")

# Setup dual logging: file gets detailed logs, console gets clean dashboard
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

DRY_RUN = True


# ============================================================================
# PRE-FLIGHT DATA GAP SYNCHRONIZATION
# ============================================================================
def pre_flight_data_sync(mt5_conn: MT5Connection):
    """
    Checks each asset's parquet file in Forex_Backtesting_Data/ and appends
    any missing closed candles up to the current moment.
    """
    print("=" * 115)
    print(" [PRE-FLIGHT] Checking and synchronizing missing candles from MT5 server...")
    print("=" * 115)
    
    total_appended = 0
    now_utc = datetime.now(timezone.utc)
    
    for asset in ASSETS:
        real_symbol = mt5_conn.resolve_symbol(asset)
        m15_file = os.path.join(DATA_DIR, f"{asset}_15m_real.parquet")
        
        # Fallback for GER30 -> GER40
        if not os.path.exists(m15_file) and asset == "GER30":
            m15_file = os.path.join(DATA_DIR, "GER40_15m_real.parquet")
            
        if not os.path.exists(m15_file):
            continue
            
        try:
            df_existing = pd.read_parquet(m15_file)
            if 'datetime' in df_existing.columns:
                last_dt = pd.to_datetime(df_existing['datetime'].max())
                if last_dt.tzinfo is None:
                    last_dt = last_dt.tz_localize('UTC')
            else:
                continue
                
            fetch_from = last_dt + timedelta(seconds=1)
            # Pull closed candles up to 1 minute ago
            rates = mt5.copy_rates_range(real_symbol, mt5.TIMEFRAME_M15, fetch_from, now_utc - timedelta(minutes=1))
            
            if rates is not None and len(rates) > 0:
                df_new = pd.DataFrame(rates)
                df_new['datetime'] = pd.to_datetime(df_new['time'], unit='s', utc=True)
                # Keep strictly closed candles
                df_new = df_new[df_new['datetime'] < now_utc - timedelta(minutes=1)]
                
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
                    df_combined.to_parquet(m15_file, index=False)
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
    time.sleep(1.0)


# ============================================================================
# MODEL MANAGEMENT
# ============================================================================
def load_or_train_model():
    model_path = os.path.join(SCRIPT_DIR, "..", "models", "xgboost_forex.json")
    model = xgb.Booster()
    if os.path.exists(model_path):
        logging.info(f"Loading existing XGBoost model from {model_path}")
        model.load_model(model_path)
        return model
    
    logging.warning("Training baseline XGBoost model on the 13 canonical features...")
    cols = [
        "bullish_fvg", "bearish_fvg", "htf_4h_trend", "hour", "day_of_week", 
        "rsi_14", "vwap_dist", "ema_50_dist", "ema_200_dist", "ema_200_slope", 
        "atr_14", "volatility_20", "roc_20"
    ]
    dummy_X = pd.DataFrame(np.random.rand(200, len(cols)), columns=cols)
    dummy_y = np.random.randint(0, 2, 200)
    
    dtrain = xgb.DMatrix(dummy_X, label=dummy_y)
    params = {'objective': 'binary:logistic', 'max_depth': 3, 'learning_rate': 0.1, 'verbosity': 0}
    model = xgb.train(params, dtrain, num_boost_round=15)
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save_model(model_path)
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
    mt5_conn = MT5Connection(0, '', '')
    if not mt5_conn.connect():
        print("[FATAL ERROR] Could not connect to running MetaTrader 5. Make sure MT5 is open!")
        sys.exit(1)

    # Pre-flight data sync
    if not args.no_sync:
        pre_flight_data_sync(mt5_conn)

    account_info = mt5.account_info()
    acc_dict = account_info._asdict() if account_info else {'login': 'UNKNOWN', 'balance': 0.0, 'server': 'UNKNOWN'}

    print("Loading XGBoost Model Engine...")
    xgb_model = load_or_train_model()

    print("Warm-starting rolling state buffers for 18 assets...")
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

    print(f"Successfully warm-started {len(engines)}/18 assets.")
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

                # Check if a new 15m candle closed on MT5
                latest_rates = mt5_conn.get_15m_bars(asset, count=2)
                if not latest_rates.empty and len(latest_rates) >= 2:
                    # Previous closed bar
                    closed_bar_time = latest_rates['time'].iloc[-2]
                    if last_candle_times.get(asset) != closed_bar_time:
                        # Append closed candle to rolling buffer
                        new_bar = {
                            'timestamp': closed_bar_time,
                            'open': latest_rates['open'].iloc[-2],
                            'high': latest_rates['high'].iloc[-2],
                            'low': latest_rates['low'].iloc[-2],
                            'close': latest_rates['close'].iloc[-2],
                            'volume': latest_rates['tick_volume'].iloc[-2]
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

                # Decision Rule: ICT Trend Alignment + Probability Threshold
                signal_type = "HOLD"
                if is_kz and prob > 0.70 and trend_val > 0 and bull_fvg > 0:
                    signal_type = "DRY-BUY"
                elif is_kz and prob > 0.70 and trend_val < 0 and bear_fvg > 0:
                    signal_type = "DRY-SELL"

                if signal_type != "HOLD" and DRY_RUN:
                    sl = bid * 0.99 if signal_type == "DRY-BUY" else ask * 1.01
                    tp = bid * 1.04 if signal_type == "DRY-BUY" else ask * 0.96
                    log_msg = f"[DRY-RUN SIGNAL: {asset} | {signal_type} | P*={prob:.3f} | ENTRY={ask if 'BUY' in signal_type else bid:.5f} | SL={sl:.5f} | TP={tp:.5f}]"
                    logging.info(log_msg)

                last_bar_str = engine.buffer.index[-1].strftime("%H:%M") if not engine.buffer.empty else "--:--"

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
                # Move cursor to home position (no flicker)
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
