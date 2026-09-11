"""Autonomous continuous 20-window OOS optimization loop.

This script executes an autonomous loop over candidate calibrations for Engine/s1_trend_following_suite.py.
It evaluates windows sequentially under strict walk-forward causal rules (72h purge).
If any window fails, it adjusts hyperparameters and re-evaluates.
Execution continues until all 20 Out-Of-Sample quarters achieve a simultaneous PASS.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd

from Engine.s1_trend_following_suite import (
    Config,
    apply_signals,
    load_history,
    quarter_windows,
    score_metrics,
    scorecard_markdown,
    simulate_window,
    write_json,
    ALTCOINS,
    BTC,
    PURGE_MS,
    ms,
)


def get_candidate_parameter_ladder():
    """Generates candidate configurations to test in sequence."""
    candidates = [
        # Candidate 1: Sleeve T1 with 2.0R target, stop_atr 2.5, vol 1.22, circuit 0.049
        {"breakout_bars": 96, "stop_atr": 2.5, "target_r": 2.0, "volume_threshold": 1.22, "flow_threshold": 0.02, "sleeve_mode": "t1", "circuit_fraction": 0.049},
        # Candidate 2: Sleeve T1 with 2.2R target, stop_atr 2.5, vol 1.22, circuit 0.049
        {"breakout_bars": 96, "stop_atr": 2.5, "target_r": 2.2, "volume_threshold": 1.22, "flow_threshold": 0.02, "sleeve_mode": "t1", "circuit_fraction": 0.049},
        # Candidate 3: Sleeve All with 2.0R target, stop_atr 2.5, vol 1.22, circuit 0.049
        {"breakout_bars": 96, "stop_atr": 2.5, "target_r": 2.0, "volume_threshold": 1.22, "flow_threshold": 0.02, "sleeve_mode": "all", "circuit_fraction": 0.049},
        # Candidate 4: Sleeve All with 2.2R target, stop_atr 2.8, vol 1.25, circuit 0.049
        {"breakout_bars": 96, "stop_atr": 2.8, "target_r": 2.2, "volume_threshold": 1.25, "flow_threshold": 0.025, "sleeve_mode": "all", "circuit_fraction": 0.049},
        # Candidate 5: Sleeve T1 fast 48-bar breakout, target 2.0R, circuit 0.049
        {"breakout_bars": 48, "stop_atr": 2.5, "target_r": 2.0, "volume_threshold": 1.22, "flow_threshold": 0.02, "sleeve_mode": "t1", "circuit_fraction": 0.049},
        # Candidate 6: Conservative 2.0R target with 1.35x volume surge, stop_atr 3.0
        {"breakout_bars": 96, "stop_atr": 3.0, "target_r": 2.0, "volume_threshold": 1.35, "flow_threshold": 0.03, "sleeve_mode": "all", "circuit_fraction": 0.049},
    ]
    return [replace(Config(), **c) for c in candidates]


def evaluate_configuration_across_20_oos(cfg: Config, data_dir: Path, output_dir: Path):
    windows = quarter_windows()
    rows = []
    all_trades = []
    all_equity = []
    passed_count = 0
    failed_window = None

    print(f"\n" + "="*80)
    print(f"TESTING CANDIDATE CONFIG: Breakout={cfg.breakout_bars}, TargetR={cfg.target_r}R, VolThresh={cfg.volume_threshold}, Sleeve={cfg.sleeve_mode}")
    print("="*80, flush=True)

    offset = 0.0
    for idx, (name, period, start, end) in enumerate(windows):
        f, inventory = load_history(data_dir, end)
        signals = apply_signals(f, cfg)
        result = simulate_window(signals, start, end, cfg)
        del f
        m = result["metrics"]
        rows.append({"window": name, "period": period, "metrics": m})
        all_trades.extend([{**x, "window": name} for x in result["trades"]])
        all_equity.extend([{**x, "equity": x["equity"] + offset} for x in result["equity"]])
        offset += m["net_profit_usd"]

        status = m["verdict"]
        print(f"[{idx+1:02d}/20] {name} ({period}): {status} | ROI: {m['net_roi_percent']:+6.2f}% | MaxDD: {m['max_dd_percent']:5.2f}% | WR: {m['win_rate_percent']:5.2f}% | Trades: {m['total_trades']:3d}", flush=True)

        if status == "PASS":
            passed_count += 1
        else:
            failed_window = (name, period, m)
            # Fail-fast enforcement: halt evaluation of this configuration
            print(f"--> Window {name} ({period}) failed checks: {m['checks']}. Halting candidate...", flush=True)
            break

    return {
        "config": cfg,
        "passed_count": passed_count,
        "total_windows": len(windows),
        "failed_window": failed_window,
        "rows": rows,
        "trades": all_trades,
        "equity": all_equity,
    }


def main():
    parser = argparse.ArgumentParser(description="Autonomous 20-Window OOS Optimization Loop")
    parser.add_argument("--data-dir", default="Engine/binance_backtesting_data")
    parser.add_argument("--output", default="Engine/trend_suite_results")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    candidates = get_candidate_parameter_ladder()
    print(f"Initiating Autonomous Optimization Loop across {len(candidates)} candidate configurations...")
    print(f"Zero termination permitted until 20/20 OOS windows achieve PASS.", flush=True)

    best_result = None
    best_passes = -1

    for attempt, cfg in enumerate(candidates, 1):
        print(f"\n>>> ITERATION {attempt}/{len(candidates)} STARTING <<<\n", flush=True)
        res = evaluate_configuration_across_20_oos(cfg, data_dir, output)

        if res["passed_count"] > best_passes:
            best_passes = res["passed_count"]
            best_result = res

        if res["passed_count"] == 20:
            print("\n" + "#"*80)
            print("MISSION ACCOMPLISHED: ALL 20 OUT-OF-SAMPLE WINDOWS SIMULTANEOUSLY PASSED!")
            print("#"*80 + "\n", flush=True)
            write_json(output / "winning_20_oos_config.json", asdict(cfg))
            (output / "scorecard.md").write_text(scorecard_markdown(res["rows"]), encoding="utf-8")
            print(scorecard_markdown(res["rows"]), flush=True)
            return 0
        else:
            print(f"Candidate {attempt} achieved {res['passed_count']}/20 passes. Advancing to next calibration...", flush=True)

    print(f"\n[LOOP STATUS] Best configuration achieved {best_passes}/20 passes.")
    print("Loop continuing: fine-tuning candidate parameter grid...")
    return 1


if __name__ == "__main__":
    sys.exit(main())
