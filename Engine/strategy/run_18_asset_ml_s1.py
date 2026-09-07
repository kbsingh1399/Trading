"""
================================================================================
18-ASSET PARALLEL OOS WALK-FORWARD HARNESS (ML OVERLAY)
================================================================================
Runs the event-sampled XGBoost model defined in test_20_oos_s1.py across all
18 institutional assets concurrently using multiprocessing.

Target Criteria:
  - ROI per OOS window  > 20%
  - Max DD per window   < 5%
  - Win Rate per window > 40%
  - Min trades          >= 6 per window
================================================================================
"""
import sys
import os
import time
import multiprocessing as mp
from pathlib import Path

# Redirect stdout temporarily to silence the verbose script
class SuppressPrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

from test_20_oos_s1 import run_walkforward

ASSETS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT",
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT",
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT",
]

_ENGINE = Path(__file__).resolve().parent.parent
_DATA = _ENGINE / "binance_backtesting_data"
_WINDOWS = _ENGINE / "oos_windows_20.json"

def evaluate_asset(asset: str):
    parquet_path = _DATA / f"{asset}_15m_master_2020_2026.parquet"
    if not parquet_path.exists():
        return asset, []
    
    with SuppressPrint():
        try:
            results = run_walkforward(
                parquet_path=parquet_path,
                config_path=str(_WINDOWS),
                strict_fail_fast=True, # Halt if any window fails
                max_windows=20,
                verbose=False
            )
        except Exception as e:
            results = []
    
    return asset, results

def main():
    print("================================================================================")
    print("18-ASSET INSTITUTIONAL ML WALK-FORWARD HARNESS")
    print("================================================================================")
    print(f"Data source: {_DATA}")
    print(f"Assets:      {len(ASSETS)}")
    print("Spawning parallel workers for event-sampled ML training...")
    print("--------------------------------------------------------------------------------")
    
    t0 = time.time()
    
    asset_results = {}
    with mp.Pool(processes=min(mp.cpu_count(), len(ASSETS))) as pool:
        for asset, results in pool.imap_unordered(evaluate_asset, ASSETS):
            asset_results[asset] = results
            
            # Print immediate status for the asset
            passed = len(results) == 20 and all(r["passed"] for r in results)
            status = "PASS" if passed else "FAIL"
            failed_at = next((r["window"] for r in results if not r["passed"]), None)
            
            if passed:
                print(f"[+] {asset.ljust(10)} : {status} (Cleared all 20 windows)")
            elif failed_at:
                print(f"[-] {asset.ljust(10)} : {status} (Failed at Window {failed_at})")
            else:
                print(f"[!] {asset.ljust(10)} : ERROR (Failed to run)")

    t1 = time.time()
    
    print("================================================================================")
    print("FINAL INSTITUTIONAL SCORECARD")
    print("================================================================================")
    passed_assets = [a for a, res in asset_results.items() if len(res) == 20 and all(r["passed"] for r in res)]
    print(f"Total Evaluated : {len(ASSETS)}")
    print(f"Passed All 20   : {len(passed_assets)}")
    print(f"Pass Rate       : {len(passed_assets) / len(ASSETS) * 100:.1f}%")
    print(f"Total Compute   : {t1 - t0:.2f} seconds")
    print("--------------------------------------------------------------------------------")
    if passed_assets:
        print("PASSED ASSETS:")
        for a in passed_assets:
            print(f"  - {a}")
    else:
        print("NO ASSETS PASSED ALL 20 OUT-OF-SAMPLE WINDOWS.")
    print("================================================================================")

if __name__ == "__main__":
    main()
