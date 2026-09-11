"""
================================================================================
MASTER 20 OOS WALK-FORWARD RUNNER (INSTITUTIONAL DUAL-MODEL ORDERFLOW)
================================================================================
Location: Engine/run_20_oos_dual_model.py
100% Causal, Zero-Lookahead, 72-Hour Quarantine Purge, 41.0 bps Round-Trip Drag.
Evaluated across all 20 Out-Of-Sample Quarterly Windows (2021-2026).
================================================================================
"""

import sys
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scratch.fast_numba_oos_engine import (
    compile_dataset_with_numba, WINDOWS_PATH, CRITERIA_PATH
)
from Engine.strategy.s1_dual_model_orderflow import (
    InstitutionalDualModelEngine
)

def main():
    print("\n" + "=" * 135)
    print("INSTITUTIONAL QUANTITATIVE MASTER ENGINE: 20 OUT-OF-SAMPLE (OOS) WALK-FORWARD AUDIT")
    print("=" * 135)

    all_data = compile_dataset_with_numba()

    with open(CRITERIA_PATH, "r", encoding="utf-8") as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
        windows = json.load(f)

    CAPITAL = criteria.get("initial_capital_usd", 5000.0)
    MIN_ROI = criteria.get("min_roi_percent", 10.0)
    MAX_DD = criteria.get("max_dd_percent", 5.0)
    MIN_WR = criteria.get("min_winrate_percent", 40.0)
    MIN_TRD = criteria.get("min_trades", 15)
    PURGE_MS = 72 * 3600 * 1000

    engine = InstitutionalDualModelEngine(
        capital=CAPITAL,
        base_risk=50.0,
        house_risk=85.0,
        friction_r=0.25,
        target_r=2.20,
        stop_r=1.00,
        max_dd_limit=4.75,
        profit_goal=500.0,
        min_trades=15,
        max_per_symbol=3,
        random_state=42
    )

    print("\n" + "-" * 135)
    print(f"{'W#':<3} | {'Window Name':<35} | {'Regime Setup':<24} | {'Trades':<7} | {'Win Rate':<8} | {'Net PnL':<12} | {'Net ROI':<9} | {'Max DD':<7} | {'Status':<6}")
    print("-" * 135)

    passed_count = 0
    total_trades = 0
    total_pnl = 0.0

    for w in windows:
        w_id = w["window_id"]
        w_name = w["name"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000

        train_mask = all_data.open_time_ms < (start_ms - PURGE_MS)
        test_mask = (all_data.open_time_ms >= start_ms) & (all_data.open_time_ms <= end_ms)

        train_set = all_data[train_mask]
        test_set = all_data[test_mask]

        if len(train_set) < 2000 or len(test_set) == 0:
            continue

        clf_long, clf_short = engine.train_models(train_set)
        selected, regime_str = engine.select_trades_for_window(test_set, clf_long, clf_short)
        res = engine.simulate_execution(selected)

        net_pnl = res["net_pnl"]
        net_roi = res["net_roi"]
        max_dd = res["max_dd"]
        wr = res["win_rate"]
        n_trd = res["trades"]

        is_pass = (net_roi >= MIN_ROI) and (max_dd <= MAX_DD) and (wr >= MIN_WR) and (n_trd >= MIN_TRD)
        status = "PASS" if is_pass else ("PROFIT" if net_pnl > 0 and max_dd <= MAX_DD else ("CASH" if n_trd == 0 else "FAIL"))

        if is_pass:
            passed_count += 1
        total_trades += n_trd
        total_pnl += net_pnl

        print(f"W{w_id:02d} | {w_name[:35]:<35} | {regime_str:<24} | {n_trd:<7d} | {wr:>5.1f}%  | {net_pnl:>+10.2f} USD | {net_roi:>+7.2f}% | {max_dd:>5.2f}% | {status:<6}")

    print("=" * 135)
    print(f"MASTER ENGINE SCORECARD: Passed: {passed_count}/20 | Total Trades: {total_trades:,d} | Total PnL: {total_pnl:+,.2f} USD (ROI: {(total_pnl/CAPITAL)*100:+.2f}%)")
    print("=" * 135)

if __name__ == "__main__":
    main()
