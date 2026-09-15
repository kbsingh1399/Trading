"""
================================================================================
ENGINE LIVE: TRAIN PRODUCTION XGBOOST MODEL (UNIFIED KERNEL)
================================================================================
Uses Engine.core.strategy_kernel as the single source of truth:
1. 13 Canonical stationary features computed via Polars with shift(1) on 4H trend (zero lookahead).
2. Microstructure 7-stage ratchet exit simulation for exact labeling parity.
3. Saves production model to Engine/models/xgboost_forex.json.
================================================================================
"""
import os
import sys
import logging
import pandas as pd
import numpy as np
import xgboost as xgb

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.strategy_kernel import (
    CANONICAL_FEATURES,
    CANONICAL_18_ASSETS,
    engineer_features_polars,
    create_labels_ratchet,
)

DATA_DIR = os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data")
MODEL_PATH = os.path.join(PROJECT_ROOT, "Engine", "models", "xgboost_forex.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def main():
    all_X = []
    all_y = []

    print("=" * 75)
    print(" TRAINING REAL PRODUCTION XGBOOST MODEL ON UNIFIED STRATEGY KERNEL")
    print("=" * 75)

    for sym in CANONICAL_18_ASSETS:
        try:
            print(f"  -> Engineering causal features & ratchet labels for {sym:<7}...", end=" ", flush=True)
            df = engineer_features_polars(sym, DATA_DIR)
            df = create_labels_ratchet(df)

            valid = df[df['target'].notna()]
            if len(valid) > 0:
                win_pct = valid['target'].mean() * 100.0
                print(f"Found {len(valid):>4} setups | Win Rate: {win_pct:.1f}%")
                all_X.append(valid[CANONICAL_FEATURES])
                all_y.append(valid['target'].values)
            else:
                print("0 valid setups.")
        except Exception as e:
            print(f"Error: {e}")

    if not all_X:
        print("\n[ERROR] No valid setups found across assets!")
        sys.exit(1)

    X_mat = pd.concat(all_X, ignore_index=True)
    y_vec = np.concatenate(all_y)

    print("-" * 75)
    print(f" Total Setups Labeled: {len(X_mat):,} across {len(all_X)} assets")
    pos_count = int(y_vec.sum())
    neg_count = len(y_vec) - pos_count
    pos_weight = float(neg_count) / max(1.0, float(pos_count))
    print(f" Class Distribution: {pos_count} Wins, {neg_count} Losses (Scale Pos Weight: {pos_weight:.2f})")

    dtrain = xgb.DMatrix(X_mat, label=y_vec)
    params = {
        'objective': 'binary:logistic',
        'max_depth': 4,
        'learning_rate': 0.05,
        'reg_alpha': 1.0,
        'reg_lambda': 3.0,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'scale_pos_weight': pos_weight,
        'eval_metric': 'logloss',
        'seed': 42
    }

    print(" Training XGBoost booster...")
    model = xgb.train(params, dtrain, num_boost_round=80)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save_model(MODEL_PATH)

    print(f"\n SUCCESS: Production model saved to {MODEL_PATH}")
    print(f" Model size: {os.path.getsize(MODEL_PATH):,} bytes")

    # Feature Importance
    importance = model.get_score(importance_type='gain')
    sorted_imp = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    print("\n Top Feature Importances (Gain):")
    for f, score in sorted_imp[:10]:
        print(f"   {f:<16}: {score:.2f}")
    print("=" * 75)


if __name__ == "__main__":
    main()
