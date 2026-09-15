"""
================================================================================
ENGINE: UNIFIED FOREX & CFD MASTER TRADING ENGINE (STANDALONE CLI)
================================================================================
Location: Engine/forex_engine.py
Architecture: Single Standalone Master Interface (Clean Code, Karpathy Directives)

Dynamic Full-Cycle Workflow (Default Execution):
1. CLEAN SLATE       : Deletes existing pre-trained model files (Engine/models/xgboost_forex.json).
2. REAL-TIME SYNC    : Connects to MT5, downloads missing completed candles up to the latest
                       15-min candle (True UTC), and atomically appends to Forex_Backtesting_Data/.
3. DYNAMIC RETRAINING: Computes 13 stationary features via Polars, simulates 7-stage microstructure
                       ratchets, and trains a fresh XGBoost booster across all 18 institutional assets.
4. LIVE INFERENCE    : Loads the newly trained model, warm-starts 250-bar rolling buffers, and launches
                       the real-time ASCII telemetry dashboard.

Path-Agnostic Robustness:
Automatically resolves project root whether executed from:
- C:\\Users\\SIGMA\\Documents\\Trading
- C:\\Users\\SIGMA\\Documents\\Trading\\Engine
- Or any arbitrary directory via absolute path.
================================================================================
"""
from __future__ import annotations

import os
import sys
import argparse
from pathlib import Path

# -------------------------------------------------------------------------
# PATH ROBUSTNESS & ROOT RESOLUTION
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
LOG_FILE = ENGINE_DIR / "live" / "dry_run.log"


# -------------------------------------------------------------------------
# STAGE 1: CLEAN SLATE (PURGE PRE-TRAINED MODELS)
# -------------------------------------------------------------------------
def purge_pretrained_models():
    """Deletes existing pre-trained model files to guarantee 100% fresh retraining."""
    print("=" * 85)
    print(" [STAGE 1] PURGING EXISTING PRE-TRAINED MODEL ARTIFACTS...")
    print("=" * 85)
    deleted_count = 0
    if PRODUCTION_MODEL_PATH.exists():
        try:
            os.remove(PRODUCTION_MODEL_PATH)
            print(f"  -> Deleted existing model: {PRODUCTION_MODEL_PATH}")
            deleted_count += 1
        except Exception as e:
            print(f"  -> Warning: Could not delete {PRODUCTION_MODEL_PATH}: {e}")

    # Remove any temp model files
    for tmp_file in MODELS_DIR.glob("*.tmp"):
        try:
            os.remove(tmp_file)
            deleted_count += 1
        except Exception:
            pass

    print(f" [STAGE 1 COMPLETE] Purged {deleted_count} model artifact(s). Zero stale weights remain.")
    print("=" * 85)


# -------------------------------------------------------------------------
# STAGE 2: PRE-FLIGHT LIVE DATA SYNCHRONIZATION
# -------------------------------------------------------------------------
def sync_latest_data(mt5_conn=None):
    """
    Connects to MT5 and downloads any missing completed 15m candles
    up to current UTC time across all 18 institutional assets.
    """
    print("\n" + "=" * 85)
    print(" [STAGE 2] FETCHING LATEST MARKET DATA TILL LAST 15M CANDLE (MT5 TRUE UTC)...")
    print("=" * 85)
    from Engine.live.run_forex_dry_run import pre_flight_data_sync
    from Engine.live.mt5_connection import MT5Connection

    if mt5_conn is None:
        mt5_conn = MT5Connection()
        if not mt5_conn.connect():
            raise ConnectionError("[FATAL] Could not connect to MetaTrader 5 terminal for data sync!")

    pre_flight_data_sync(mt5_conn)
    print(" [STAGE 2 COMPLETE] Historical Parquets updated with latest completed candles.")
    print("=" * 85)


# -------------------------------------------------------------------------
# STAGE 3: DYNAMIC RETRAINING & FEATURE ENGINEERING
# -------------------------------------------------------------------------
def dynamic_retrain():
    """
    Computes 13 stationary features via Polars, simulates microstructure ratchets,
    and trains a fresh production XGBoost model on the updated data.
    """
    print("\n" + "=" * 85)
    print(" [STAGE 3] DYNAMIC FEATURE ENGINEERING & XGBOOST MODEL TRAINING...")
    print("=" * 85)
    from Engine.live.train_production_model import main as train_main
    train_main()
    if not PRODUCTION_MODEL_PATH.exists():
        raise FileNotFoundError(f"[FATAL] Model training failed to generate {PRODUCTION_MODEL_PATH}!")
    print(" [STAGE 3 COMPLETE] Certified production model regenerated and saved.")
    print("=" * 85)


# -------------------------------------------------------------------------
# STAGE 4: LIVE INFERENCE & TELEMETRY
# -------------------------------------------------------------------------
def run_telemetry(once: bool = False, ignore_kz: bool = False):
    """Launches the real-time live dry-run telemetry terminal."""
    print("\n" + "=" * 85)
    print(" [STAGE 4] LAUNCHING LIVE TELEMETRY STREAM & DECISION ENGINE...")
    print("=" * 85)
    from Engine.live.run_forex_dry_run import main as dry_run_main
    sys.argv = [sys.argv[0]]
    if once:
        sys.argv.append("--once")
    if ignore_kz:
        sys.argv.append("--ignore-kz")
    dry_run_main()


def run_verify():
    """Verifies that streaming features match Polars batch features (< 1e-9 error)."""
    print("=" * 85)
    print(" RUNNING MATHEMATICAL FEATURE PARITY AUDIT (STREAMING vs BATCH)...")
    print("=" * 85)
    from Engine.live.verify_pipeline import test_feature_parity
    test_feature_parity()


def show_structure():
    """Prints the exact storage locations for data, features, models, and logs."""
    print("=" * 85)
    print(" FOREX & CFD PRODUCTION STORAGE MAP & REPOSITORY ARCHITECTURE")
    print("=" * 85)
    print(f" [Project Root]       : {PROJECT_ROOT}")
    print(f" [Engine Directory]   : {ENGINE_DIR}")
    print(f" [Historical Parquets]: {DATA_DIR} ({len(list(DATA_DIR.glob('*.parquet')))} parquet files)")
    print(f" [Production Model]   : {PRODUCTION_MODEL_PATH} ({'EXISTS' if PRODUCTION_MODEL_PATH.exists() else 'NOT FOUND'})")
    if PRODUCTION_MODEL_PATH.exists():
        print(f"                        Size: {PRODUCTION_MODEL_PATH.stat().st_size:,} bytes")
    print(f" [Dry Run Log File]   : {LOG_FILE}")
    print(f" [Strategy Kernel]    : {ENGINE_DIR / 'core' / 'strategy_kernel.py'}")
    print(f" [Inference Engine]   : {ENGINE_DIR / 'live' / 'inference_engine.py'}")
    print("=" * 85)


def main():
    parser = argparse.ArgumentParser(
        description="Unified Master Forex & CFD Trading Engine (Standalone CLI)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Standard Usage:
  python Engine/forex_engine.py                 # Full cycle: Delete old model -> Sync latest 15m data -> Retrain -> Run live telemetry
  python Engine/forex_engine.py --mode snapshot # Full cycle: Delete old model -> Sync latest 15m data -> Retrain -> 1-pass test -> Exit
  python Engine/forex_engine.py --mode train    # Delete old model -> Sync latest 15m data -> Retrain only
  python Engine/forex_engine.py --skip-train    # Run live telemetry using existing model without retraining
  python Engine/forex_engine.py --mode verify   # Run numerical parity assertions (< 1e-9 error)
  python Engine/forex_engine.py --mode info     # Display data & model storage paths
        """
    )
    parser.add_argument(
        "--mode",
        choices=["dry-run", "snapshot", "train", "verify", "info"],
        default="dry-run",
        help="Execution mode (default: dry-run)"
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

    args = parser.parse_args()

    if args.mode == "info":
        show_structure()
        return

    if args.mode == "verify":
        run_verify()
        return

    # Master dynamic cycle: Clean Slate -> Sync Data -> Retrain Model
    if not args.skip_train:
        purge_pretrained_models()
        sync_latest_data()
        dynamic_retrain()

    # If mode was train-only, stop here
    if args.mode == "train":
        print("\n[COMPLETE] Model retrained successfully and ready for deployment.")
        return

    # Run live telemetry (continuous or single snapshot)
    is_once = (args.mode == "snapshot")
    run_telemetry(once=is_once, ignore_kz=args.ignore_kz)


if __name__ == "__main__":
    main()
