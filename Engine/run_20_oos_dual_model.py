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
        base_risk=54.0,
        house_risk_max=90.0,
        defense_risk=14.0,
        milestone_risk=10.0,
        trans_risk=35.0,
        trans_thresh=480.0,
        t1_base_risk=42.0,
        t1_trans_risk=22.0,
        cushion_multiplier=0.25,
        milestone_profit_usd=500.0,
        max_concurrent=3,
        max_s1_concurrent=2,
        max_t1_concurrent=2,
        cooldown_bars=4,
        win_r_reset_thresh=0.90,
        conf_prob_thresh=0.46,
        conf_mult=1.35,
        max_dd_limit=4.40,
        random_state=42
    )

    cache_dir = REPO_ROOT / "scratch" / "cache_multi_tf"
    df_btc = pd.read_parquet(cache_dir / "BTCUSDT_4h.parquet")
    df_btc['time'] = pd.to_datetime(df_btc['time'], utc=True)
    df_btc.sort_values('time', inplace=True)
    df_btc.reset_index(drop=True, inplace=True)
    df_btc['atr_pct'] = (df_btc['atr'] / df_btc['close']) * 100.0
    df_btc['trailing_30d_atr_pct'] = df_btc['atr_pct'].rolling(180).mean()

    print("Generating Pure T1 Quiet-Flow Breakout signals across certified assets...")
    t0 = time.perf_counter()
    df_t1 = engine.load_t1_breakout_trades()
    print(f"Generated {len(df_t1):,d} T1 signals in {time.perf_counter() - t0:.2f}s.")

    print("\n" + "-" * 135)
    print(f"{'W#':<3} | {'Window Name':<38} | {'Trades':<6} | {'S1 Tr':<6} | {'T1 Tr':<6} | {'Win Rate':<8} | {'Net PnL':<12} | {'Net ROI':<9} | {'Max DD':<7} | {'Status':<6}")
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

        if len(train_set) < 500 or len(test_set) == 0:
            continue

        s_ts = pd.Timestamp(w["start_date"], tz="UTC")
        sub_btc = df_btc[df_btc['time'] < s_ts]
        trailing_vol = sub_btc['trailing_30d_atr_pct'].iloc[-1] if len(sub_btc) > 0 else 1.75

        ridge, clf, mu, sd, calib_thresh = engine.train_models(train_set)
        selected = engine.score_test_candidates(test_set, ridge, clf, mu, sd, calib_thresh, trailing_vol_pct=trailing_vol)
        res = engine.simulate_execution(selected, t1_df=df_t1, start_ms=start_ms, end_ms=end_ms)

        net_pnl = res["net_pnl"]
        net_roi = res["net_roi"]
        max_dd = res["max_dd"]
        wr = res["win_rate"]
        n_trd = res["trades"]
        s1_tr = res["s1_trades"]
        t1_tr = res["t1_trades"]

        is_pass = (net_roi >= MIN_ROI) and (max_dd <= MAX_DD) and (wr >= MIN_WR) and (n_trd >= MIN_TRD)
        status = "PASS" if is_pass else ("PROFIT" if net_pnl > 0 and max_dd <= MAX_DD else ("CASH" if n_trd == 0 else "FAIL"))

        if is_pass:
            passed_count += 1
        total_trades += n_trd
        total_pnl += net_pnl

        print(f"W{w_id:02d} | {w_name[:38]:<38} | {n_trd:<6d} | {s1_tr:<6d} | {t1_tr:<6d} | {wr:>5.1f}%  | {net_pnl:>+10.2f} USD | {net_roi:>+7.2f}% | {max_dd:>5.2f}% | {status:<6}")

    print("=" * 135)
    print(f"MASTER MULTIVERSE SCORECARD: Passed: {passed_count}/20 | Total Trades: {total_trades:,d} | Total PnL: {total_pnl:+,.2f} USD (ROI: {(total_pnl/CAPITAL)*100:+.2f}%)")
    print("=" * 135)

if __name__ == "__main__":
    main()
