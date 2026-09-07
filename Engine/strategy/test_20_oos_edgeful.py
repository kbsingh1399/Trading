import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add the parent directory to the path so we can import the Engine modules
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from Engine.strategy.smc_edgeful import SMCEdgefulSimulator, RiskConfig, FrictionConfig
import json
import time

def run_walkforward(parquet_path: Path, windows_json: Path):
    print("=" * 80)
    print("INSTITUTIONAL WALK-FORWARD HARNESS – SMC EDGEFUL ENGINE")
    print("=" * 80)
    
    with open(windows_json, "r") as f:
        windows = json.load(f)
        
    df = pd.read_parquet(parquet_path)
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"])
    
    simulator = SMCEdgefulSimulator(
        risk_cfg=RiskConfig(),
        fric_cfg=FrictionConfig()
    )
    
    results = []
    
    print("\nStarting Causal Walk-Forward Evaluation across 20 OOS Windows...\n")
    
    for w_idx, w in enumerate(windows, start=1):
        w_name = w["name"]
        win_start = pd.to_datetime(w["start_date"])
        win_end = pd.to_datetime(w["end_date"]) + pd.Timedelta(days=1)
        
        # Causal purge: start 72 hours early to build indicator history/context
        purge_start = win_start - pd.Timedelta(hours=72)
        
        df_test = df[(df["datetime_utc"] >= purge_start) & (df["datetime_utc"] < win_end)].copy().reset_index(drop=True)
        
        if len(df_test) < 100:
            print(f"Skipping W{w_idx:02d} (Not enough data)")
            continue
            
        t0 = time.time()
        sim_res = simulator.run(df_test)
        t1 = time.time()
        
        roi = sim_res["roi_pct"]
        mdd = sim_res["max_dd_pct"]
        wr = sim_res["win_rate_pct"]
        trds = sim_res["trades"]
        pnl = sim_res["net_pnl"]
        
        status = "PASS" if (roi > 20.0 and mdd < 5.0 and wr > 40.0 and trds >= 6) else "FAIL"
        
        print(f"[{status}] W{w_idx:02d} | ROI: {roi:+.2f}% | MaxDD: {mdd:.2f}% | WR: {wr:.1f}% | Trades: {trds} | PnL: ${pnl:+.2f} | Time: {t1-t0:.2f}s")
        
        results.append({
            "w_idx": w_idx,
            "name": w_name,
            "roi": roi,
            "mdd": mdd,
            "wr": wr,
            "trades": trds,
            "status": status
        })
        
        if status == "FAIL" and "--strict-fail-fast" in sys.argv:
            print("\n[!] STRICT FAIL-FAST TRIGGERED. Halting optimization.")
            break
            
    print("\n" + "=" * 80)
    print("WALK-FORWARD PERFORMANCE SUMMARY SCORECARD")
    print("=" * 80)
    print(f"{'W#':<4} | {'Window Name':<35} | {'ROI (%)':>9} | {'MaxDD':>7} | {'WinRate':>9} | {'Trades':>6} | Status")
    print("-" * 80)
    for r in results:
        print(f"{r['w_idx']:<4} | {r['name']:<35} | {r['roi']:>+8.2f}% | {r['mdd']:>5.2f}% | {r['wr']:>6.1f}% | {r['trades']:>6} | {r['status']}")
    print("=" * 80)
    
    # Simple Monte Carlo
    print("\n" + "=" * 80)
    print("MONTE CARLO ROBUSTNESS SIMULATION (10,000 ITERATIONS)")
    print("=" * 80)
    
    all_trades = []
    for w in windows:
        win_start = pd.to_datetime(w["start_date"])
        win_end = pd.to_datetime(w["end_date"]) + pd.Timedelta(days=1)
        purge_start = win_start - pd.Timedelta(hours=72)
        df_test = df[(df["datetime_utc"] >= purge_start) & (df["datetime_utc"] < win_end)].copy().reset_index(drop=True)
        if len(df_test) > 100:
            res = simulator.run(df_test)
            all_trades.extend(res["trades_list"])
            
    if not all_trades:
        print("No trades to simulate.")
        sys.exit(1 if any(r["status"] == "FAIL" for r in results) else 0)
        
    pnl_array = np.array([t["pnl"] for t in all_trades])
    n_trades = len(pnl_array)
    
    mc_results = []
    mc_dds = []
    
    for _ in range(10000):
        idx = np.random.randint(0, n_trades, size=n_trades)
        sample_pnls = pnl_array[idx]
        eq = 5000.0 + np.cumsum(sample_pnls)
        peaks = np.maximum.accumulate(eq)
        with np.errstate(divide='ignore', invalid='ignore'):
            dds = np.where(peaks > 0, (peaks - eq) / peaks * 100.0, 0.0)
        mc_results.append(eq[-1])
        mc_dds.append(np.max(dds) if len(dds) > 0 else 0.0)
        
    print(f"Median Terminal Equity:     ${np.median(mc_results):.2f}")
    print(f"Median Max Drawdown:        {np.median(mc_dds):.2f}%")
    print(f"99th Percentile Max DD:     {np.percentile(mc_dds, 99):.2f}%")
    print(f"Risk of Ruin (Hit 5% DD):   {np.mean(np.array(mc_dds) >= 5.0)*100:.2f}%")
    print("=" * 80)

    if any(r["status"] == "FAIL" for r in results):
        sys.exit(1)

if __name__ == "__main__":
    run_walkforward(
        Path("Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet"),
        Path("Engine/oos_windows_20.json")
    )
