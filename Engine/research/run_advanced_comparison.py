"""
================================================================================
ENGINE RESEARCH: MULTI-MODEL QUANT BENCHMARK & COMPARISON SUITE
================================================================================
Runs comparative evaluation:
1. Baseline: Production XGBoost (13 Canonical Features).
2. Quant-Enhanced XGBoost: 13 Canonical + 4 Advanced Quant Features (Yang-Zhang, OU Half-Life, Hurst).
3. Quant-Enhanced CatBoost: Advanced Quant Features + Oblivious Decision Trees.
4. Quant-Enhanced LightGBM: Advanced Quant Features + Fast Leaf-wise Gradient Boosting.
5. Quant-Enhanced Stacking Ensemble: Blended Probabilities with L2 Meta-Logistic Learner.

Evaluated across Out-Of-Sample regimes with:
- Accuracy, Log-Loss, ROC-AUC, Brier Score
- Simulated PnL, Win Rate, Expected Gain per Setup
- Lopez de Prado (2026) Non-IID Sharpe Ratio, PSR, and MinTRL
================================================================================
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, log_loss, brier_score_loss, accuracy_score

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
from Engine.research.features.advanced_quant_math import (
    compute_yang_zhang_volatility,
    compute_ornstein_uhlenbeck_halflife,
    compute_hurst_exponent_fast,
    RESEARCH_QUANT_FEATURES
)
from Engine.research.models.model_zoo import ModelZoo
from Engine.research.eval.institutional_metrics import (
    compute_moments_and_sharpe,
    compute_psr,
    compute_min_trl,
    compute_deflated_sharpe_ratio
)

DATA_DIR = os.path.join(PROJECT_ROOT, "Forex_Backtesting_Data")


def augment_with_quant_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adds strictly causal higher-order quant features to the DataFrame."""
    open_p = df['open'].to_numpy(dtype=np.float64)
    high_p = df['high'].to_numpy(dtype=np.float64)
    low_p = df['low'].to_numpy(dtype=np.float64)
    close_p = df['close'].to_numpy(dtype=np.float64)

    # 1. Yang-Zhang Realized Volatility
    yz_vol = compute_yang_zhang_volatility(open_p, high_p, low_p, close_p, window=20)
    df['yang_zhang_vol'] = yz_vol

    # 2. Ornstein-Uhlenbeck Half-Life and Theta on VWAP deviations
    vwap_dist = df['vwap_dist'].to_numpy(dtype=np.float64)
    ou_hl, ou_th = compute_ornstein_uhlenbeck_halflife(vwap_dist, window=40)
    df['ou_halflife'] = ou_hl
    df['ou_theta'] = ou_th

    # 3. Hurst Exponent
    hurst = compute_hurst_exponent_fast(close_p, window=60)
    df['hurst_exp'] = hurst

    # 4. Volatility Asymmetry
    df['vol_asymmetry'] = np.where(df['atr_14'] > 1e-6, yz_vol / (df['atr_14'] / close_p), 1.0)
    df['vol_asymmetry'] = np.clip(df['vol_asymmetry'], 0.1, 10.0)

    return df


def run_benchmark():
    print("=" * 80)
    print(" ADVANCED QUANT & MULTI-MODEL OUT-OF-SAMPLE BENCHMARK (ISOLATED ENGINE)")
    print("=" * 80)

    all_dfs = []
    print("Loading datasets and engineering advanced quant signatures...")
    
    # Process assets
    for sym in CANONICAL_18_ASSETS:
        try:
            df = engineer_features_polars(sym, DATA_DIR)
            df = create_labels_ratchet(df)
            valid = df[df['target'].notna()].copy()
            if len(valid) > 20:
                valid = augment_with_quant_features(valid)
                valid['asset'] = sym
                all_dfs.append(valid)
                print(f"  + {sym:<8}: {len(valid):>4} labeled setups (Win Rate: {valid['target'].mean()*100:.1f}%)")
        except Exception as e:
            print(f"  - {sym:<8}: Error {e}")

    if not all_dfs:
        print("[ERROR] No data available for benchmark.")
        return

    full_df = pd.concat(all_dfs, ignore_index=True)
    full_df.sort_values(by='time', inplace=True)
    full_df.reset_index(drop=True, inplace=True)

    total_setups = len(full_df)
    split_idx = int(total_setups * 0.70)
    train_df = full_df.iloc[:split_idx].copy()
    test_df = full_df.iloc[split_idx:].copy()

    print("-" * 80)
    print(f"Total Setups: {total_setups:,} | In-Sample Train: {len(train_df):,} | Out-Of-Sample Test: {len(test_df):,}")
    print(f"In-Sample Date Range:  {train_df['time'].min()} to {train_df['time'].max()}")
    print(f"Out-Of-Sample Test:   {test_df['time'].min()} to {test_df['time'].max()}")
    print("-" * 80)

    y_train = train_df['target'].to_numpy(dtype=int)
    y_test = test_df['target'].to_numpy(dtype=int)

    pos_count = int(y_train.sum())
    neg_count = len(y_train) - pos_count
    pos_weight = float(neg_count) / max(1.0, float(pos_count))

    # Feature sets
    X_train_baseline = train_df[CANONICAL_FEATURES].copy()
    X_test_baseline = test_df[CANONICAL_FEATURES].copy()

    ENHANCED_FEATURES = CANONICAL_FEATURES + RESEARCH_QUANT_FEATURES
    X_train_quant = train_df[ENHANCED_FEATURES].copy()
    X_test_quant = test_df[ENHANCED_FEATURES].copy()

    # Fill any NaNs
    X_train_baseline.fillna(0.0, inplace=True)
    X_test_baseline.fillna(0.0, inplace=True)
    X_train_quant.fillna(0.0, inplace=True)
    X_test_quant.fillna(0.0, inplace=True)

    print("Training Candidate Models on In-Sample Data...")
    zoo = ModelZoo(seed=42)

    # 1. Baseline XGBoost (13 Canonical features only)
    print("  -> Training Baseline XGBoost (13 Canonical Features)...")
    zoo.train_xgboost(X_train_baseline, y_train, pos_weight)
    pred_baseline = zoo.models['xgboost'].predict(import_xgb().DMatrix(X_test_baseline))

    # 2. Enhanced Quant XGBoost (13 Canonical + 5 Quant features)
    print("  -> Training Quant-Enhanced XGBoost (18 Features)...")
    zoo_quant = ModelZoo(seed=42)
    zoo_quant.train_xgboost(X_train_quant, y_train, pos_weight)
    pred_quant_xgb = zoo_quant.models['xgboost'].predict(import_xgb().DMatrix(X_test_quant))

    # 3. Quant-Enhanced CatBoost
    print("  -> Training Quant-Enhanced CatBoost (18 Features)...")
    zoo_quant.train_catboost(X_train_quant, y_train, pos_weight)
    pred_quant_cb = zoo_quant.models['catboost'].predict_proba(X_test_quant)[:, 1]

    # 4. Quant-Enhanced LightGBM
    print("  -> Training Quant-Enhanced LightGBM (18 Features)...")
    zoo_quant.train_lightgbm(X_train_quant, y_train, pos_weight)
    pred_quant_lgb = zoo_quant.models['lightgbm'].predict(X_test_quant)

    # 5. Quant-Enhanced Stacking Ensemble
    print("  -> Training Quant-Enhanced Stacking Ensemble...")
    zoo_quant.train_stacking_ensemble(X_train_quant, y_train, pos_weight)
    pred_quant_stack = zoo_quant.predict_probs(X_test_quant)['stacking']

    candidates = {
        "Baseline XGBoost (13 Feat)": pred_baseline,
        "Quant XGBoost (18 Feat)": pred_quant_xgb,
        "Quant CatBoost": pred_quant_cb,
        "Quant LightGBM": pred_quant_lgb,
        "Quant Stacking Ensemble": pred_quant_stack
    }

    results = []
    threshold = 0.55

    for name, p_prob in candidates.items():
        auc = roc_auc_score(y_test, p_prob)
        brier = brier_score_loss(y_test, p_prob)
        loss = log_loss(y_test, p_prob)
        p_bin = (p_prob >= threshold).astype(int)

        # Evaluate trade execution stats for signals >= 0.55
        signal_mask = p_prob >= threshold
        n_signals = int(signal_mask.sum())
        if n_signals > 0:
            sub_y = y_test[signal_mask]
            win_rate = float(sub_y.mean()) * 100.0
            # Returns: +2.0R on win (net of frictions), -1.0R on loss
            trade_returns = np.where(sub_y == 1, 2.0, -1.0)
            tot_r = float(trade_returns.sum())
            exp_r = float(trade_returns.mean())
            moments = compute_moments_and_sharpe(trade_returns)
            sr = moments['sharpe']
            psr = compute_psr(sr, 0.0, n_signals, moments['skew'], moments['kurt'])
            min_trl = compute_min_trl(sr, 0.0, moments['skew'], moments['kurt'])
        else:
            win_rate = 0.0
            tot_r = 0.0
            exp_r = 0.0
            sr = 0.0
            psr = 0.0
            min_trl = float('inf')

        results.append({
            "Model": name,
            "AUC": auc,
            "Brier": brier,
            "LogLoss": loss,
            "Signals": n_signals,
            "WinRate%": win_rate,
            "Tot_R": tot_r,
            "Expectancy_R": exp_r,
            "Sharpe_R": sr,
            "PSR": psr,
            "MinTRL": min_trl
        })

    res_df = pd.DataFrame(results)

    # Compute Deflated Sharpe Ratio (DSR) across all candidates
    all_srs = res_df['Sharpe_R'].to_numpy()
    dsrs = []
    for i, row in res_df.iterrows():
        if row['Signals'] > 5:
            dsr_val = compute_deflated_sharpe_ratio(row['Sharpe_R'], all_srs, row['Signals'], -0.5, 3.5)
        else:
            dsr_val = 0.0
        dsrs.append(dsr_val)
    res_df['DSR'] = dsrs

    print("\n" + "=" * 95)
    print(" OUT-OF-SAMPLE MODEL EVALUATION & INSTITUTIONAL LEADERBOARD")
    print("=" * 95)
    print(res_df.to_string(index=False))
    print("=" * 95)

    # Save leaderboard
    out_path = os.path.join(PROJECT_ROOT, "Engine", "research", "oos_leaderboard.csv")
    res_df.to_csv(out_path, index=False)
    print(f"\nSaved Out-Of-Sample Leaderboard to: {out_path}")
    return res_df


def import_xgb():
    import xgboost as xgb
    return xgb


if __name__ == "__main__":
    run_benchmark()
