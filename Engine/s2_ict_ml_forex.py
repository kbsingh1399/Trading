"""
================================================================================
ENGINE 2: ICT MACHINE LEARNING FOREX BACKTEST (UNIFIED STRATEGY KERNEL)
================================================================================
1. Evaluates the 18 Canonical Institutional Forex & CFD assets.
2. Uses Engine.core.strategy_kernel as single source of truth:
   - Causal 4H trend with shift(1) (zero lookahead).
   - Microstructure 7-stage ratchet exit logic.
   - 96-bar purge & embargo at OOS boundaries.
3. Computes trades, win rate, net PnL, and max drawdown per window.
================================================================================
"""
import os
import sys
import json
from typing import Optional, List, Dict, Any
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import xgboost as xgb

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.strategy_kernel import (
    CANONICAL_FEATURES,
    CANONICAL_18_ASSETS,
    engineer_features_polars,
    create_labels_ratchet,
    get_causal_train_test_split,
)

DATA_DIR = os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data")
OOS_WINDOWS_FILE = os.path.join(PROJECT_ROOT, "Engine", "oos_windows_20_random.json")
RESULTS_FILE = os.path.join(PROJECT_ROOT, "Engine", "forex_oos_results.json")

INITIAL_CAPITAL = 5000.0
BASE_RISK = 50.0  # 1.0%


def train_model(train_df: pd.DataFrame, features: list) -> Optional[xgb.XGBClassifier]:
    """Fits causal XGBoost classifier with inverse class weighting."""
    X = train_df[features]
    y = train_df['target']

    if y.sum() < 2 or (len(y) - y.sum()) < 2:
        return None

    pos_weight = (len(y) - y.sum()) / max(1.0, float(y.sum()))

    clf = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        reg_lambda=3.0,
        reg_alpha=1.0,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=pos_weight,
        random_state=42,
        eval_metric="logloss",
        n_jobs=-1
    )
    clf.fit(X, y)
    return clf


def run_walk_forward_backtest(symbol: str, df: pd.DataFrame) -> list:
    """Executes walk-forward backtest across the 20 random OOS windows with 96-bar purge."""
    with open(OOS_WINDOWS_FILE, "r") as f:
        windows = json.load(f)

    capital = INITIAL_CAPITAL
    peak_capital = capital
    max_dd = 0.0
    results = []

    for w in windows:
        start_date = pd.to_datetime(w["start_date"]).tz_localize("UTC") if pd.to_datetime(w["start_date"]).tzinfo is None else pd.to_datetime(w["start_date"])
        end_date = pd.to_datetime(w["end_date"]).tz_localize("UTC") if pd.to_datetime(w["end_date"]).tzinfo is None else pd.to_datetime(w["end_date"])

        # Strict 96-bar purge & embargo: training set ends 24 hours before window start
        train_df, oos_df = get_causal_train_test_split(df, start_date, end_date, look_fwd_bars=96)

        if len(train_df) < 50 or len(oos_df) == 0:
            continue

        model = train_model(train_df, CANONICAL_FEATURES)
        if model is None:
            continue

        # In-sample probability calibration (causal p* target)
        X_train = train_df[CANONICAL_FEATURES]
        train_probs = model.predict_proba(X_train)[:, 1]

        total_train_days = max(1, (train_df['datetime'].max() - train_df['datetime'].min()).days)
        quarters_in_train = max(1.0, total_train_days / 90.0)
        target_total_trades = int(35 * quarters_in_train)

        sorted_probs = np.sort(train_probs)[::-1]
        if target_total_trades < len(sorted_probs):
            p_star = sorted_probs[target_total_trades]
        else:
            p_star = 0.50

        p_star = max(0.40, min(p_star, 0.85))

        # Evaluate OOS setups
        setup_mask = oos_df['target'].notna()
        if not setup_mask.any():
            continue

        X_oos = oos_df.loc[setup_mask, CANONICAL_FEATURES]
        probs = model.predict_proba(X_oos)[:, 1]
        oos_df.loc[setup_mask, 'ml_prob'] = probs

        # Execute trades above calibrated threshold
        trade_mask = setup_mask & (oos_df['ml_prob'] > p_star)
        trades = oos_df[trade_mask]

        trade_count = len(trades)
        wins = int((trades['r_realized'] > 0).sum()) if trade_count > 0 else 0
        r_sum = float(trades['r_realized'].sum()) if trade_count > 0 else 0.0
        pnl = r_sum * BASE_RISK
        capital += pnl

        # Track drawdown
        if capital > peak_capital:
            peak_capital = capital
        current_dd = (peak_capital - capital) / peak_capital * 100.0 if peak_capital > 0 else 0.0
        if current_dd > max_dd:
            max_dd = current_dd

        win_rate = (wins / trade_count * 100.0) if trade_count > 0 else 0.0

        results.append({
            "window": w["name"],
            "start_date": w["start_date"],
            "end_date": w["end_date"],
            "trades": trade_count,
            "wins": wins,
            "win_rate": round(win_rate, 1),
            "pnl": round(pnl, 2),
            "capital": round(capital, 2),
            "max_dd_pct": round(max_dd, 2)
        })

    return results


def main():
    print(f"Starting Causal OOS ML Backtest on Canonical {len(CANONICAL_18_ASSETS)} Assets...")

    all_results = {}

    for sym in CANONICAL_18_ASSETS:
        try:
            print(f"  -> Processing {sym:<7}...", end=" ", flush=True)
            df = engineer_features_polars(sym, DATA_DIR)
            df = create_labels_ratchet(df)
            res = run_walk_forward_backtest(sym, df)
            all_results[sym] = res

            total_trades = sum(r['trades'] for r in res)
            final_pnl = sum(r['pnl'] for r in res)
            avg_wr = np.mean([r['win_rate'] for r in res if r['trades'] > 0]) if any(r['trades'] > 0 for r in res) else 0.0
            print(f"Done ({len(res)} windows) | Trades: {total_trades:>3} | Win Rate: {avg_wr:>4.1f}% | Net PnL: ${final_pnl:>8.2f}")
        except Exception as e:
            print(f"Failed: {e}")

    with open(RESULTS_FILE, "w") as f:
        json.dump(all_results, f, indent=4)

    print(f"\nSaved certified clean results to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
