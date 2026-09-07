import json
import time
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import optuna
from sklearn.metrics import f1_score, accuracy_score

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    from sklearn.ensemble import RandomForestClassifier
    HAS_XGB = False
from sklearn.metrics import precision_score, recall_score

from s1_liquidation_cascade import LiquidationCascadeSimulator, RiskConfig, FrictionConfig, RatchetConfig

def load_windows(config_path: str) -> list:
    with open(config_path, "r") as f:
        config = json.load(f)
    return config

def extract_features(df: pd.DataFrame, t: int) -> np.ndarray:
    # Features: RSI, VWAP Z-score, Liquidations, CVD, ATR, Vol Ratio
    return np.array([
        df["rsi_14"].iloc[t],
        df["vwap_zscore"].iloc[t],
        df["long_liq_roll"].iloc[t],
        df["short_liq_roll"].iloc[t],
        df["zc_div"].iloc[t],
        df["delta_spot"].iloc[t],
        df["delta_fut"].iloc[t],
        df["volume_ratio"].iloc[t],
        df["ls_ratio_global"].iloc[t] if "ls_ratio_global" in df.columns else 1.0,
        df["atr_14"].iloc[t] / df["close"].iloc[t] * 100.0, # ATR %
        (df["close"].iloc[t] - df["ema_200"].iloc[t]) / df["ema_200"].iloc[t] * 100.0 # EMA 200 Dist %
    ])

def train_model(simulator, df_train: pd.DataFrame):
    # Run the base simulation to collect raw trades on the training set
    train_res = simulator.run(df_train, training_mode=True)
    trades = train_res["trades_list"]
    
    X = []
    y = []
    for tr in trades:
        idx = tr["entry_bar"]
        features = extract_features(df_train, idx)
        X.append(features)
        
        # Target: 1 if trade hit at least 1.5R maximum excursion (explosive continuation), 0 otherwise
        max_r = tr.get("max_r", 0.0)
        if max_r >= 1.5:
            y.append(1)
        else:
            y.append(0)
            
    X = np.array(X)
    y = np.array(y)
    
    if len(y) < 20 or sum(y) < 5:
        return None
        
    # Time-series split (80/20) for Optuna objective
    split_idx = int(len(X) * 0.8)
    X_tr, y_tr = X[:split_idx], y[:split_idx]
    X_va, y_va = X[split_idx:], y[split_idx:]
    
    pos_weight = (len(y) - sum(y)) / sum(y) if sum(y) > 0 else 1.0
    
    def objective(trial):
        params = {
            'max_depth': trial.suggest_int('max_depth', 2, 6),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'reg_alpha': trial.suggest_float('reg_alpha', 0.1, 10.0, log=True),
            'reg_lambda': trial.suggest_float('reg_lambda', 0.1, 10.0, log=True),
            'scale_pos_weight': pos_weight,
            'random_state': 42,
            'verbosity': 0
        }
        
        if HAS_XGB:
            model = XGBClassifier(**params)
        else:
            # Fallback to random forest if xgboost missing
            model = RandomForestClassifier(n_estimators=params['n_estimators'], max_depth=params['max_depth'], random_state=42)
            
        model.fit(X_tr, y_tr)
        preds = model.predict(X_va)
        prec = precision_score(y_va, preds, zero_division=0)
        rec = recall_score(y_va, preds, zero_division=0)
        # F0.5 score: heavily weights precision over recall to avoid false positives
        return ((1 + 0.5**2) * prec * rec) / ((0.5**2 * prec) + rec) if (prec + rec) > 0 else 0.0
        
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30)
    
    best_params = study.best_params
    best_params['scale_pos_weight'] = pos_weight
    best_params['random_state'] = 42
    best_params['verbosity'] = 0
    
    if HAS_XGB:
        model = XGBClassifier(**best_params)
    else:
        model = RandomForestClassifier(n_estimators=best_params['n_estimators'], max_depth=best_params['max_depth'], random_state=42)
        
    model.fit(X, y)
    return model

def run_walkforward(parquet_path: Path, config_path: str, strict_fail_fast: bool, max_windows: int, verbose: bool = True):
    print("=" * 80)
    print("INSTITUTIONAL WALK-FORWARD ML HARNESS — S1 LIQUIDATION CASCADE")
    print("=" * 80)
    print(f"Data source:    {parquet_path}")
    print(f"Windows config: {config_path}")
    print(f"Strict halt:    {strict_fail_fast}")
    print("-" * 80)
    
    print("Loading BTCUSDT 15m Master Dataset...")
    t0 = time.time()
    df = pd.read_parquet(parquet_path)
    
    if "datetime_utc" in df.columns and pd.api.types.is_string_dtype(df["datetime_utc"]):
        df["datetime_utc"] = pd.to_datetime(df["datetime_utc"])
    elif "datetime" in df.columns and pd.api.types.is_string_dtype(df["datetime"]):
        df["datetime"] = pd.to_datetime(df["datetime"])
        df.rename(columns={"datetime": "datetime_utc"}, inplace=True)
    elif "datetime" in df.columns and pd.api.types.is_datetime64_any_dtype(df["datetime"]):
        df.rename(columns={"datetime": "datetime_utc"}, inplace=True)
        
    df = df.sort_values("datetime_utc").reset_index(drop=True)
    
    # Compute Rolling Features required for ML extraction
    df["long_liq_roll"] = df["long_liq_zs"].rolling(4).max().fillna(0)
    df["short_liq_roll"] = df["short_liq_zs"].rolling(4).max().fillna(0)
    df["delta_spot"] = df["spot_cvd_15m"].diff().fillna(0)
    df["delta_fut"] = df["future_cvd_15m"].diff().fillna(0)
    
    t1 = time.time()
    print(f"Loaded {len(df):,} bars from {df['datetime_utc'].iloc[0]} to {df['datetime_utc'].iloc[-1]} in {t1-t0:.2f}s\n")
    
    windows = load_windows(config_path)
    simulator = LiquidationCascadeSimulator(risk_cfg=RiskConfig(), fric_cfg=FrictionConfig(), ratchet_cfg=RatchetConfig())
    
    results = []
    
    print("Starting Causal ML Walk-Forward Evaluation across 20 OOS Windows...\n")
    
    for w_idx, win in enumerate(windows[:max_windows], 1):
        win_name = win["name"]
        start_str = win["start_date"]
        end_str = win["end_date"]
        win_regime = win.get("regime", "Unknown")
        
        win_start = pd.to_datetime(start_str)
        win_end = pd.to_datetime(end_str) + pd.Timedelta(days=1)
        
        # 1. Train Data: All data prior to this window (up to win_start - 72h)
        train_end = win_start - pd.Timedelta(hours=72)
        df_train = df[df["datetime_utc"] < train_end].copy().reset_index(drop=True)
        
        # 2. Test Data: The current window (+72h purge history)
        purge_start = win_start - pd.Timedelta(hours=72)
        test_mask = (df["datetime_utc"] >= purge_start) & (df["datetime_utc"] < win_end)
        df_test = df[test_mask].copy().reset_index(drop=True)
        
        n_test = len(df_test)
        
        print("-" * 80)
        print(f"WINDOW {w_idx:02d}/20: {win_name.upper()}")
        print(f"Period:        {start_str} -> {end_str} ({n_test} test bars)")
        print(f"Regime:        {win_regime}")
        
        if n_test < 100:
            print("ERROR: Not enough test bars found for window! Skipping.")
            continue
        
        t_eval = time.time()
        
        # Train ML Model
        model = None
        threshold = 0.50
        if len(df_train) > 1000:
            print(f"Training XGBoost on {len(df_train):,} prior causal bars...")
            model = train_model(simulator, df_train)
            if model:
                # Optimize threshold on the most recent 10k bars of the training set
                best_roi = -999
                best_th = 0.50
                for th in [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]:
                    def val_filter(t: int, side: str) -> bool:
                        X_t = extract_features(df_train[-10000:], t).reshape(1, -1)
                        prob = model.predict_proba(X_t)[0][1]
                        return prob >= th
                    
                    val_res = simulator.run(df_train[-10000:], filter_func=val_filter)
                    if val_res["roi_pct"] > best_roi and val_res["trades"] >= 5:
                        best_roi = val_res["roi_pct"]
                        best_th = th
                threshold = best_th
                print(f"Model trained successfully. Optimal threshold: {threshold:.2f}")
            else:
                print("Warning: Failed to train model (insufficient raw signals).")
        
        def ml_filter(t: int, side: str) -> bool:
            if model is None:
                return True
            X_t = extract_features(df_test, t).reshape(1, -1)
            prob = model.predict_proba(X_t)[0][1]
            return prob >= threshold
            
        sim_res = simulator.run(df_test, filter_func=ml_filter)
        eval_dur = time.time() - t_eval
        
        roi = sim_res["roi_pct"]
        max_dd = sim_res["max_dd_pct"]
        wr = sim_res["win_rate_pct"]
        trades = sim_res["trades"]
        
        passed = (roi >= 20.0) and (max_dd < 5.0) and (wr >= 40.0) and (trades >= 6)
        status_str = "PASS" if passed else "FAIL"
        
        results.append({
            "window": w_idx, "name": win_name, "roi": roi, "max_dd": max_dd,
            "wr": wr, "trades": trades, "passed": passed
        })
        
        print(f"\n[OUTCOME] WINDOW {w_idx:02d}: {status_str}")
        print(f"  ROI:        {roi:+.2f}%  (Target: >= +20.0%)")
        print(f"  Max DD:     {max_dd:.2f}%  (Target: < 5.0%)")
        print(f"  Win Rate:   {wr:.1f}%  (Target: >= 40.0%)")
        print(f"  Trades:     {trades}  (Target: >= 6)")
        print(f"  Net PnL:    ${sim_res['net_pnl']:+.2f}")
        print(f"  Compute:    Eval {eval_dur:.2f}s")
        
        for i, tr in enumerate(sim_res["trades_list"][:30], 1):
            print(f"    T{i:02d}: {tr['side']:<5} | Ent ${tr['entry']:8.1f} | Ext ${tr['exit']:8.1f} | PnL ${tr['pnl']:6.2f} | {tr['r']:+5.2f}R | {tr['reason']}")
            
        if strict_fail_fast and not passed:
            print(f"\n[FAIL-FAST] Window {w_idx:02d} failed. Halting Walk-Forward Evaluation.")
            break

    if verbose:
        print("=" * 80)
        print("WALK-FORWARD PERFORMANCE SUMMARY SCORECARD")
        print("=" * 80)
        print(f"Total Evaluated: {len(results)} Windows")
        print(f"Passed:          {sum(1 for r in results if r['passed'])}")
        print(f"Failed:          {sum(1 for r in results if not r['passed'])}")
        print("-" * 80)
        print("W#  | Window Name                         | ROI (%)   | MaxDD   | WinRate  | Trades | Status")
        print("-" * 80)
        for r in results:
            nm = (r["name"][:33] + "..") if len(r["name"]) > 35 else r["name"].ljust(35)
            st = "PASS" if r["passed"] else "FAIL"
            print(f"{r['window']:<3} | {nm} | {r['roi']:>+8.2f}% | {r['max_dd']:5.2f}% | {r['wr']:>5.1f}% | {r['trades']:>6} | {st}")
        print("=" * 80)

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=str, default="Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet")
    parser.add_argument("--windows", type=str, default="Engine/oos_windows_20.json")
    parser.add_argument("--strict-fail-fast", action="store_true")
    parser.add_argument("--max-windows", type=int, default=20)
    args = parser.parse_args()

    run_walkforward(Path(args.parquet), args.windows, args.strict_fail_fast, args.max_windows)

if __name__ == "__main__":
    main()
