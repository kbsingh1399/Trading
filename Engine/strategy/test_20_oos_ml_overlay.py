"""
================================================================================
20 OOS WALK-FORWARD HARNESS — ML OVERLAY CLASSIFIER
================================================================================
Executes strictly causal walk-forward testing across the 20 strategic OOS windows
(April 2021 to August 2026) for BTCUSDT (15m timeframe).
Uses the ML Overlay Architecture logic from KIs.
================================================================================
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

# Add repo root to sys.path
_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from Engine.strategy.ml_overlay_liquidation_engine import (
    RiskConfig,
    FrictionConfig,
    RatchetConfig,
    MLOverlayFeatureExtractor,
    MLOverlayClassifier,
    CausalSMCMLSimulator,
)

def run_monte_carlo(trades: List[Dict], initial_capital: float, iterations: int = 10000) -> Dict:
    """Run Monte Carlo simulation on the trade sequence to assess Risk of Ruin and Expected Drawdown."""
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
    max_windows: int = 20,
    ml_threshold: float = 0.50,
    liq_threshold: float = 1.8
) -> List[Dict]:
    """Execute sequential causal walk-forward across the 20 OOS windows."""
    print("=" * 80)
    print("INSTITUTIONAL WALK-FORWARD HARNESS — ML OVERLAY CLASSIFIER")
    print("=" * 80)
    print(f"Data source:    {parquet_path}")
    print(f"Windows config: {windows_json_path}")
    print(f"Strict halt:    {strict_fail_fast}")
    print("-" * 80)

    # 1. Ingest Master Parquet
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet dataset not found at {parquet_path}")
    
    t0 = time.time()
    print("Loading BTCUSDT 15m Master Dataset...")
    df = pd.read_parquet(parquet_path)
    df["datetime"] = pd.to_datetime(df["datetime_utc"])
    df = df.sort_values("open_time_ms").reset_index(drop=True)
    
    # Check column names:
    if "future_cvd_15m" not in df.columns:
        if "futures_cvd_15m" in df.columns:
            df = df.rename(columns={"futures_cvd_15m": "future_cvd_15m"})
            
    print(f"Loaded {len(df):,} bars from {df['datetime'].iloc[0]} to {df['datetime'].iloc[-1]} in {time.time()-t0:.2f}s")
    
    # 2. Ingest 20 OOS Windows
    if not windows_json_path.exists():
        raise FileNotFoundError(f"Windows specification not found at {windows_json_path}")
    with open(windows_json_path, "r", encoding="utf-8") as f:
        oos_windows = json.load(f)

    # 3. Instantiate Engine & Simulator
    risk_cfg = RiskConfig()
    fric_cfg = FrictionConfig()
    ratchet_cfg = RatchetConfig()
    simulator = CausalSMCMLSimulator(risk_cfg=risk_cfg, fric_cfg=fric_cfg, ratchet_cfg=ratchet_cfg)

    results = []
    all_trades = []
    total_passed = 0
    total_failed = 0

    print("\nStarting Causal Walk-Forward Evaluation across 20 OOS Windows...\n")

    for w_idx, win in enumerate(oos_windows[:max_windows], start=1):
        win_name = win["name"]
        win_regime = win["regime"]
        start_str = win["start_date"]
        end_str = win["end_date"]
        
        win_start = pd.to_datetime(start_str)
        win_end = pd.to_datetime(end_str) + pd.Timedelta(days=1)
        train_cutoff = win_start - pd.Timedelta(hours=72)
        
        train_mask = df["datetime"] < train_cutoff
        test_mask = (df["datetime"] >= win_start) & (df["datetime"] < win_end)
        
        df_train = df[train_mask].copy().reset_index(drop=True)
        df_test = df[test_mask].copy().reset_index(drop=True)
        
        n_train = len(df_train)
        n_test = len(df_test)
        
        print("-" * 80)
        print(f"WINDOW {w_idx:02d}/20: {win_name.upper()}")
        print(f"Period:        {start_str} -> {end_str} ({n_test} test bars)")
        print(f"Regime:        {win_regime}")
        print(f"Causal Train:  {df_train['datetime'].iloc[0]} -> {df_train['datetime'].iloc[-1]} ({n_train:,} bars)")
        
        if n_test == 0:
            print("ERROR: Zero test bars found for window! Skipping.")
            continue

        t_fit = time.time()
        # Train ML overlay dynamically based on candidate signals identified within the training partition
        simulator.ml_classifier.model.random_state = 42 + w_idx
        simulator.train_overlay(df_train, liq_threshold=liq_threshold)
        fit_dur = time.time() - t_fit
        
        t_eval = time.time()
        # Execute causal backtest simulation filtering with ML overlay
        sim_res = simulator.run(df_test, ml_threshold=ml_threshold, liq_threshold=liq_threshold)
        
        roi = sim_res["roi_pct"]
        max_dd = sim_res["max_dd_pct"]
        wr = sim_res["win_rate_pct"]
        trades = sim_res["trades"]
        net_pnl = sim_res["net_pnl"]
        
        if trades > 0:
            all_trades.extend(sim_res["trades_list"])
        
        is_pass = (roi >= 20.0) and (max_dd < 5.0) and (wr >= 40.0) and (trades >= 6)
        
        status_tag = "PASS" if is_pass else "FAIL"
        if is_pass:
            total_passed += 1
        else:
            total_failed += 1
            
        print(f"\n[OUTCOME] WINDOW {w_idx:02d}: {status_tag}")
        print(f"  ROI:        {roi:+.2f}%  (Target: >= +20.0%)")
        print(f"  Max DD:     {max_dd:.2f}%  (Target: < 5.0%)")
        print(f"  Win Rate:   {wr:.1f}%  (Target: >= 40.0%)")
        print(f"  Trades:     {trades}  (Target: >= 6)")
        print(f"  Net PnL:    ${net_pnl:+.2f}")
        print(f"  Compute:    Fit {fit_dur:.2f}s | Eval {time.time()-t_eval:.2f}s")
        
        for tr_i, tr in enumerate(sim_res["trades_list"]):
            print(f"    T{tr_i+1:02d}: {tr['side']:5s} | Ent ${tr['entry']:8.1f} | Ext ${tr['exit']:8.1f} | PnL ${tr['pnl']:+6.2f} | {tr['r']:+5.2f}R | {tr['reason']}")
            
        results.append({
            "window_id": w_idx,
            "name": win_name,
            "regime": win_regime,
            "start_date": start_str,
            "end_date": end_str,
            "pass": is_pass,
            "roi_pct": roi,
            "max_dd_pct": max_dd,
            "win_rate_pct": wr,
            "trades": trades,
            "net_pnl": net_pnl
        })
        
        del df_train, df_test
        gc.collect()

        if strict_fail_fast and not is_pass:
            print("\n" + "!" * 80)
            print(f"STRICT FAIL-FAST HALT: Window {w_idx} failed pass criteria.")
            print("Halting sequential walk-forward per Part 10 protocol.")
            print("!" * 80)
            break

    print("\n" + "=" * 80)
    print("WALK-FORWARD PERFORMANCE SUMMARY SCORECARD")
    print("=" * 80)
    print(f"Total Evaluated: {len(results)} Windows")
    print(f"Passed:          {total_passed}")
    print(f"Failed:          {total_failed}")
    print("-" * 80)
    print(f"{'W#':<3} | {'Window Name':<35} | {'ROI (%)':<9} | {'MaxDD':<7} | {'WinRate':<8} | {'Trades':<6} | {'Status'}")
    print("-" * 80)
    for r in results:
        status_str = "PASS" if r["pass"] else "FAIL"
        print(f"{r['window_id']:<3} | {r['name'][:35]:<35} | {r['roi_pct']:>+8.2f}% | {r['max_dd_pct']:>5.2f}% | {r['win_rate_pct']:>6.1f}% | {r['trades']:>6} | {status_str}")
    print("=" * 80)
    
    run_monte_carlo(all_trades, risk_cfg.initial_capital)
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Walk-Forward Evaluation of ML Overlay Liquidation Engine.")
    parser.add_argument("--parquet", type=str, default="Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet")
    parser.add_argument("--windows", type=str, default="Engine/oos_windows_20.json")
    parser.add_argument("--strict-fail-fast", action="store_true", help="Halt immediately upon first window failure.")
    parser.add_argument("--max-windows", type=int, default=20, help="Maximum number of windows to evaluate.")
    parser.add_argument("--ml-threshold", type=float, default=0.50, help="Threshold for ML overlay probability.")
    parser.add_argument("--liq-threshold", type=float, default=1.8, help="Threshold for liquidation z-score.")
    args = parser.parse_args()

    run_walkforward(
        parquet_path=Path(args.parquet),
        windows_json_path=Path(args.windows),
        strict_fail_fast=args.strict_fail_fast,
        max_windows=args.max_windows,
        ml_threshold=args.ml_threshold,
        liq_threshold=args.liq_threshold
    )

if __name__ == "__main__":
    main()
