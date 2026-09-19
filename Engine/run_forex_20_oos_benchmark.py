import os
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Engine.core.strategy_kernel import (
    CANONICAL_18_ASSETS,
    CANONICAL_FEATURES,
    engineer_features_polars,
    create_labels_ratchet
)
from Engine.research.features.advanced_quant_math import (
    compute_yang_zhang_volatility,
    compute_ornstein_uhlenbeck_halflife,
    compute_hurst_exponent_fast,
    RESEARCH_QUANT_FEATURES
)
from Engine.research.models.model_zoo import ModelZoo

DATA_DIR = str(PROJECT_ROOT / "Forex_Backtesting_Data")

def augment_with_quant_features(df: pd.DataFrame) -> pd.DataFrame:
    open_p = df['open'].to_numpy(dtype=np.float64)
    high_p = df['high'].to_numpy(dtype=np.float64)
    low_p = df['low'].to_numpy(dtype=np.float64)
    close_p = df['close'].to_numpy(dtype=np.float64)

    yz_vol = compute_yang_zhang_volatility(open_p, high_p, low_p, close_p, window=20)
    df['yang_zhang_vol'] = yz_vol

    vwap_dist = df['vwap_dist'].to_numpy(dtype=np.float64)
    ou_hl, ou_th = compute_ornstein_uhlenbeck_halflife(vwap_dist, window=40)
    df['ou_halflife'] = ou_hl
    df['ou_theta'] = ou_th

    hurst = compute_hurst_exponent_fast(close_p, window=60)
    df['hurst_exp'] = hurst

    df['vol_asymmetry'] = np.where(df['atr_14'] > 1e-6, yz_vol / (df['atr_14'] / close_p), 1.0)
    df['vol_asymmetry'] = np.clip(df['vol_asymmetry'], 0.1, 10.0)
    return df


def main():
    print("=" * 85)
    print(" 20 OUT-OF-SAMPLE (OOS) WALK-FORWARD BENCHMARK (18 CANONICAL ASSETS)")
    print("=" * 85)

    with open(PROJECT_ROOT / 'Engine' / 'oos_windows_forex_20.json', 'r', encoding='utf-8') as f:
        windows = json.load(f)

    # 1. Load and engineer features for all 18 canonical assets
    all_dfs = []
    print("Engineering features across 18 canonical assets...")
    for sym in CANONICAL_18_ASSETS:
        try:
            df = engineer_features_polars(sym, DATA_DIR)
            df = create_labels_ratchet(df)
            valid = df[df['target'].notna()].copy()
            if len(valid) > 20:
                valid = augment_with_quant_features(valid)
                valid['asset'] = sym
                all_dfs.append(valid)
                print(f"  Loaded {sym:<8}: {len(valid):>4} labeled setups")
        except Exception as e:
            print(f"  Failed {sym}: {e}")

    full_df = pd.concat(all_dfs, ignore_index=True)
    full_df['dt'] = pd.to_datetime(full_df['time'], unit='s')
    full_df.sort_values(by='time', inplace=True)
    full_df.reset_index(drop=True, inplace=True)

    print(f"\nTotal labeled setups across 18 assets: {len(full_df):,}")
    print(f"Historical span: {full_df['dt'].min().date()} to {full_df['dt'].max().date()}")

    # Sequential walk-forward evaluation across all 20 windows
    window_results = []
    tot_trades = 0
    tot_wins = 0
    tot_r_all = 0.0

    print("\nRunning Causal Walk-Forward Evaluation across 20 OOS Windows...")

    for w in windows:
        w_id = w['window_id']
        w_name = w['name']
        s_date = w['start_date']
        e_date = w['end_date']
        w_start = pd.Timestamp(s_date)
        w_end = pd.Timestamp(e_date) + pd.Timedelta(days=1)

        # Causal in-sample training data strictly prior to w_start (with 24h purge)
        purge_time = w_start - pd.Timedelta(hours=24)
        train_sub = full_df[full_df['dt'] < purge_time]

        test_sub = full_df[(full_df['dt'] >= w_start) & (full_df['dt'] <= w_end)].copy()

        if len(train_sub) < 100 or len(test_sub) == 0:
            window_results.append({
                'Window': f'W{w_id:02d}',
                'Regime Name': w_name[:26],
                'Date Range': f"{s_date} to {e_date}",
                'Trades': 0,
                'WinRate%': 0.0,
                'Net_R': 0.0,
                'Net_ROI%': 0.0,
                'MaxDD%': 0.0,
                'Calmar': 0.0,
                'Status': 'PURGED'
            })
            continue

        y_train = train_sub['target'].to_numpy(dtype=int)
        pos_weight = float(len(y_train) - y_train.sum()) / max(1.0, float(y_train.sum()))

        X_train = train_sub[CANONICAL_FEATURES + RESEARCH_QUANT_FEATURES].fillna(0.0)
        X_test = test_sub[CANONICAL_FEATURES + RESEARCH_QUANT_FEATURES].fillna(0.0)

        zoo = ModelZoo(seed=42)
        zoo.train_stacking_ensemble(X_train, y_train, pos_weight)
        test_sub['prob'] = zoo.predict_probs(X_test)['stacking']

        # High-Calmar threshold P* >= 0.54
        sig_sub = test_sub[test_sub['prob'] >= 0.54]
        n_trades = len(sig_sub)

        if n_trades == 0:
            window_results.append({
                'Window': f'W{w_id:02d}',
                'Regime Name': w_name[:26],
                'Date Range': f"{s_date} to {e_date}",
                'Trades': 0,
                'WinRate%': 0.0,
                'Net_R': 0.0,
                'Net_ROI%': 0.0,
                'MaxDD%': 0.0,
                'Calmar': 0.0,
                'Status': 'FLAT'
            })
            continue

        y_sub = sig_sub['target'].to_numpy(dtype=int)
        wr = float(y_sub.mean()) * 100.0
        trade_r = np.where(y_sub == 1, 2.0, -1.0)
        tot_trades += n_trades
        tot_wins += int(y_sub.sum())
        tot_r_all += float(trade_r.sum())

        # High-Calmar Dynamic Risk Budget Simulation
        cap = 5000.0
        eq = cap
        peak = cap
        eq_curve = [eq]

        for r_val in trade_r:
            curr_dd = (peak - eq) / peak * 100.0 if peak > 0 else 0.0
            risk = 25.0
            if curr_dd >= 2.0:
                risk = 15.0
            elif (eq - cap) >= 100.0 and curr_dd < 1.0:
                risk = 35.0
            eq += r_val * risk
            if eq > peak:
                peak = eq
            eq_curve.append(eq)

        eq_arr = np.array(eq_curve)
        peaks = np.maximum.accumulate(eq_arr)
        dds = (peaks - eq_arr) / peaks * 100.0
        mdd = float(np.max(dds))
        tot_roi = float((eq - cap) / cap * 100.0)
        calmar = tot_roi / max(0.01, mdd)

        status = 'PASS' if tot_roi > 0 and mdd <= 4.50 else ('PROFIT' if tot_roi > 0 else 'DEFENSE')

        window_results.append({
            'Window': f'W{w_id:02d}',
            'Regime Name': w_name[:26],
            'Date Range': f"{s_date} to {e_date}",
            'Trades': n_trades,
            'WinRate%': round(wr, 1),
            'Net_R': round(float(trade_r.sum()), 1),
            'Net_ROI%': round(tot_roi, 2),
            'MaxDD%': round(mdd, 2),
            'Calmar': round(calmar, 2),
            'Status': status
        })
        print(f"  {f'W{w_id:02d}':<5} | Trades={n_trades:>3} | WR={wr:>5.1f}% | ROI={tot_roi:>+6.2f}% | MaxDD={mdd:>4.2f}% | Calmar={calmar:>6.2f} | {status}")

    w_df = pd.DataFrame(window_results)
    print("\n" + "=" * 110)
    print(w_df.to_string(index=False))
    print("=" * 110)

    out_file = PROJECT_ROOT / 'Engine' / 'research' / 'oos_20_windows_forex_results.csv'
    w_df.to_csv(out_file, index=False)
    print(f"\nLeaderboard successfully saved to: {out_file}")

if __name__ == '__main__':
    main()
