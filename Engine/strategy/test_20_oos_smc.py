"""
================================================================================
20 OOS WALK-FORWARD HARNESS — SMC FVG ENGINE
================================================================================
"""

from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
from typing import Dict, List
import numpy as np
import pandas as pd
import sys

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from Engine.strategy.smc_fvg_engine import SMCFVGSimulator, RiskConfig, FrictionConfig

def run_monte_carlo(trades: List[Dict], initial_capital: float, iterations: int = 10000) -> Dict:
    if not trades:
        return {}
    print("\n" + "=" * 80)
    print("MONTE CARLO ROBUSTNESS SIMULATION (10,000 ITERATIONS)")
    print("=" * 80)
    trade_pnls = np.array([t["pnl"] for t in trades])
    n_trades = len(trade_pnls)
    simulated_curves = []
    max_drawdowns = []
    terminal_equities = []
    ruin_count = 0
    ruin_threshold = initial_capital * 0.95
    for i in range(iterations):
        idx = np.random.randint(0, n_trades, size=n_trades)
        sim_pnls = trade_pnls[idx]
        equity_curve = initial_capital + np.cumsum(sim_pnls)
        terminal_equities.append(equity_curve[-1])
        peaks = np.maximum.accumulate(equity_curve)
        dds = (peaks - equity_curve) / peaks * 100.0
        max_dd = np.max(dds) if len(dds) > 0 else 0.0
        max_drawdowns.append(max_dd)
        if np.any(equity_curve < ruin_threshold):
            ruin_count += 1
    terminal_equities = np.array(terminal_equities)
    max_drawdowns = np.array(max_drawdowns)
    results = {
        "median_terminal_equity": np.median(terminal_equities),
        "median_max_dd": np.median(max_drawdowns),
        "worst_case_max_dd_99th": np.percentile(max_drawdowns, 99),
        "risk_of_ruin_pct": (ruin_count / iterations) * 100.0
    }
    print(f"Median Terminal Equity:     ${results['median_terminal_equity']:.2f}")
    print(f"Median Max Drawdown:        {results['median_max_dd']:.2f}%")
    print(f"99th Percentile Max DD:     {results['worst_case_max_dd_99th']:.2f}%")
    print(f"Risk of Ruin (Hit 5% DD):   {results['risk_of_ruin_pct']:.2f}%")
    print("=" * 80)
    return results

def run_walkforward(
    parquet_path: Path,
    windows_json_path: Path,
    strict_fail_fast: bool = False,
    max_windows: int = 20
) -> List[Dict]:
    print("=" * 80)
    print("INSTITUTIONAL WALK-FORWARD HARNESS — SMC FVG ENGINE")
    print("=" * 80)

    t0 = time.time()
    df = pd.read_parquet(parquet_path)
    df["datetime"] = pd.to_datetime(df["datetime_utc"])
    df = df.sort_values("open_time_ms").reset_index(drop=True)
    
    with open(windows_json_path, "r", encoding="utf-8") as f:
        oos_windows = json.load(f)

    simulator = SMCFVGSimulator(RiskConfig(), FrictionConfig())
    results = []
    all_trades = []
    total_passed = 0
    total_failed = 0

    print("\nStarting Causal Walk-Forward Evaluation across 20 OOS Windows...\n")

    for w_idx, win in enumerate(oos_windows[:max_windows], start=1):
        win_name = win["name"]
        win_start = pd.to_datetime(win["start_date"])
        win_end = pd.to_datetime(win["end_date"]) + pd.Timedelta(days=1)
        test_mask = (df["datetime"] >= win_start) & (df["datetime"] < win_end)
        df_test = df[test_mask].copy().reset_index(drop=True)
        
        t_sim = time.time()
        sim_res = simulator.run(df_test)
        
        roi = sim_res["roi_pct"]
        max_dd = sim_res["max_dd_pct"]
        wr = sim_res["win_rate_pct"]
        trades = sim_res["trades"]
        net_pnl = sim_res["net_pnl"]
        
        if trades > 0:
            all_trades.extend(sim_res["trades_list"])
        
        # Criteria: ROI > 20%, MaxDD < 5%, WR > 40%, Trades >= 6
        is_pass = (roi >= 20.0) and (max_dd < 5.0) and (wr >= 40.0) and (trades >= 6)
        status_tag = "PASS" if is_pass else "FAIL"
        
        if is_pass:
            total_passed += 1
        else:
            total_failed += 1
            
        print(f"[{status_tag}] W{w_idx:02d} | ROI: {roi:+.2f}% | MaxDD: {max_dd:.2f}% | WR: {wr:.1f}% | Trades: {trades} | PnL: ${net_pnl:+.2f} | Time: {time.time()-t_sim:.2f}s")
        
        results.append({
            "window_id": w_idx, "name": win_name, "pass": is_pass,
            "roi_pct": roi, "max_dd_pct": max_dd, "win_rate_pct": wr, "trades": trades
        })

        if strict_fail_fast and not is_pass:
            print("\n" + "!" * 80)
            print(f"STRICT FAIL-FAST HALT: Window {w_idx} failed pass criteria.")
            print("!" * 80)
            break

    print("\n" + "=" * 80)
    print("WALK-FORWARD PERFORMANCE SUMMARY SCORECARD")
    print("=" * 80)
    print(f"{'W#':<3} | {'Window Name':<35} | {'ROI (%)':<9} | {'MaxDD':<7} | {'WinRate':<8} | {'Trades':<6} | {'Status'}")
    print("-" * 80)
    for r in results:
        status_str = "PASS" if r["pass"] else "FAIL"
        print(f"{r['window_id']:<3} | {r['name'][:35]:<35} | {r['roi_pct']:>+8.2f}% | {r['max_dd_pct']:>5.2f}% | {r['win_rate_pct']:>6.1f}% | {r['trades']:>6} | {status_str}")
    print("=" * 80)
    
    run_monte_carlo(all_trades, RiskConfig().initial_capital)
    return results

if __name__ == "__main__":
    run_walkforward(
        Path("Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet"),
        Path("Engine/oos_windows_20.json")
    )
