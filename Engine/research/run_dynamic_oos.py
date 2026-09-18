"""
================================================================================
ENGINE RESEARCH: DYNAMIC ASSET SELECTION ACROSS 20 OOS WINDOWS
================================================================================
For each OOS window:
  1. Load ALL 98 assets' in-sample data (strictly before window start - 96 bar purge).
  2. Screen each asset with the 5 institutional gates (calibrated on IS data only).
  3. Admit the top-N by Calmar into the window-specific pool.
  4. Train a per-window XGBoost on the admitted assets' IS data.
  5. Evaluate on the OOS window, compute Calmar, WR, ROI, MaxDD.

Contrast: canonical 18-asset static list vs dynamic top-N selection.
Output: Engine/research/dynamic_oos_results.csv
================================================================================
"""
import os, sys, json, warnings
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
warnings.filterwarnings('ignore')

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.strategy_kernel import (
    CANONICAL_FEATURES, CANONICAL_18_ASSETS,
    engineer_features_polars, create_labels_ratchet)
from Engine.research.features.advanced_quant_math import (
    compute_yang_zhang_volatility, compute_hurst_exponent_fast)

DATA_DIR         = os.path.join(PROJECT_ROOT, 'Forex_Backtesting_Data')
OOS_WINDOWS_FILE = os.path.join(PROJECT_ROOT, 'Engine', 'oos_windows_forex_20.json')
OUTPUT_CSV       = os.path.join(SCRIPT_DIR, 'dynamic_oos_results.csv')

# ── Screening gate thresholds (same as asset_screener.py) ────────────────
GATE_MIN_CALMAR       = 3.0    # loosened slightly since IS data is shorter per window
GATE_MIN_WIN_RATE     = 0.44
GATE_MIN_SIGNALS      = 3
GATE_MAX_HURST        = 0.62
GATE_MIN_HURST        = 0.20
GATE_MIN_YZ_VOL       = 1e-6
GATE_MAX_YZ_VOL       = 0.10
DYNAMIC_POOL_SIZE     = 12     # top-12 assets per window
PROB_THRESHOLD        = 0.54
WIN_R                 = 2.5
LOSS_R                = 1.0
PURGE_BARS            = 96     # 24h purge at each boundary

# ── Discover all 98 assets ───────────────────────────────────────────────
ALL_ASSETS = sorted([f.replace('_15m_real.parquet','')
                     for f in os.listdir(DATA_DIR) if f.endswith('_15m_real.parquet')])
print(f'Assets available: {len(ALL_ASSETS)}')


def load_oos_windows():
    with open(OOS_WINDOWS_FILE) as f:
        return json.load(f)


def simulate_pnl(y_true, probs, threshold=PROB_THRESHOLD):
    signals = probs >= threshold
    n = int(signals.sum())
    if n == 0:
        return np.array([0.0]), 0, 0.0, 0.0
    fired = y_true[signals]
    eq = np.zeros(n+1); peak = 0.0; max_dd = 0.0; wins = 0
    for i, lbl in enumerate(fired):
        pnl = WIN_R if lbl == 1 else -LOSS_R
        wins += int(lbl == 1)
        eq[i+1] = eq[i] + pnl
        peak = max(peak, eq[i+1])
        max_dd = max(max_dd, peak - eq[i+1])
    return eq, n, wins/n, max_dd


def calmar(eq, max_dd):
    net = eq[-1]
    if net <= 0: return 0.0
    if max_dd <= 0: return min(net / 0.001, 999.0)
    return net / max_dd


def screen_assets_is(assets, t_is_start, t_is_end, min_train_days=90):
    """
    For each asset: load IS data, quick-train XGBoost, evaluate on last 30d of IS,
    apply 5 gates, return ranked list with per-asset IS calmar.
    """
    import xgboost as xgb
    results = []
    for sym in assets:
        try:
            df = engineer_features_polars(sym, DATA_DIR)
            if df is None or len(df) < 150: continue
            df['_dt'] = pd.to_datetime(df['time'], unit='s', utc=True)
            df_is = df[(df['_dt'] >= t_is_start) & (df['_dt'] < t_is_end)].copy()
            if len(df_is) < 100: continue

            # inner split: train on first 70%, validate on last 30%
            split = int(len(df_is) * 0.70)
            df_tr  = df_is.iloc[:split].copy()
            df_val = df_is.iloc[split:].copy()

            try:
                df_tr  = create_labels_ratchet(df_tr)
                df_val = create_labels_ratchet(df_val)
            except: continue

            df_tr  = df_tr.dropna(subset=CANONICAL_FEATURES+['target'])
            df_val = df_val.dropna(subset=CANONICAL_FEATURES+['target'])
            if len(df_tr) < 40 or len(df_val) < 10: continue

            pos = int(df_tr['target'].sum()); neg = len(df_tr) - pos
            if pos == 0: continue
            dtrain = xgb.DMatrix(df_tr[CANONICAL_FEATURES], label=df_tr['target'].to_numpy().astype(int))
            params = {'objective':'binary:logistic','max_depth':4,'learning_rate':0.05,
                      'reg_alpha':1.0,'reg_lambda':3.0,'subsample':0.8,'colsample_bytree':0.8,
                      'scale_pos_weight': neg/max(pos,1),'eval_metric':'logloss','seed':42,'verbosity':0}
            model = xgb.train(params, dtrain, num_boost_round=80)

            y_val   = df_val['target'].to_numpy().astype(int)
            probs   = model.predict(xgb.DMatrix(df_val[CANONICAL_FEATURES]))
            n_sig   = int((probs >= PROB_THRESHOLD).sum())
            if n_sig < GATE_MIN_SIGNALS: continue

            eq, n_tr, wr, max_dd_r = simulate_pnl(y_val, probs)
            if wr < GATE_MIN_WIN_RATE: continue
            cal = calmar(eq, max_dd_r)
            if cal < GATE_MIN_CALMAR: continue

            close_p = df_val['close'].to_numpy(np.float64)
            open_p  = df_val['open'].to_numpy(np.float64)
            high_p  = df_val['high'].to_numpy(np.float64)
            low_p   = df_val['low'].to_numpy(np.float64)
            h_arr   = compute_hurst_exponent_fast(close_p, window=40)
            h_med   = float(np.nanmedian(h_arr[h_arr > 0])) if (h_arr > 0).any() else 0.5
            yz_arr  = compute_yang_zhang_volatility(open_p, high_p, low_p, close_p, window=20)
            yz_med  = float(np.nanmedian(yz_arr[yz_arr > 0])) if (yz_arr > 0).any() else 0.01
            if not (GATE_MIN_HURST <= h_med <= GATE_MAX_HURST): continue
            if not (GATE_MIN_YZ_VOL <= yz_med <= GATE_MAX_YZ_VOL): continue

            results.append({'symbol':sym,'calmar':cal,'win_rate':wr,'n_trades':n_tr,
                             'hurst':h_med,'yz_vol':yz_med,'model':model, 'df_is': df_is})
        except Exception as e:
            pass
    results.sort(key=lambda x: x['calmar'], reverse=True)
    return results[:DYNAMIC_POOL_SIZE]


def eval_oos_window(pool_assets, t_oos_start, t_oos_end, t_is_start):
    """
    Train on full IS data for the admitted pool assets, evaluate on the OOS window.
    Returns aggregated metrics across all pool assets.
    """
    import xgboost as xgb
    all_eq = [0.0]; total_n = 0; all_wins = 0; peak = 0.0; max_dd = 0.0

    for asset_info in pool_assets:
        sym = asset_info['symbol']
        try:
            df = engineer_features_polars(sym, DATA_DIR)
            if df is None: continue
            df['_dt'] = pd.to_datetime(df['time'], unit='s', utc=True)

            # Full IS for training (with purge)
            t_purge = t_oos_start - timedelta(hours=24)  # 96-bar purge
            df_is  = df[(df['_dt'] >= t_is_start) & (df['_dt'] < t_purge)].copy()
            df_oos = df[(df['_dt'] >= t_oos_start) & (df['_dt'] < t_oos_end)].copy()
            if len(df_is) < 80 or len(df_oos) < 15: continue

            try:
                df_is  = create_labels_ratchet(df_is)
                df_oos = create_labels_ratchet(df_oos)
            except: continue

            df_is  = df_is.dropna(subset=CANONICAL_FEATURES+['target'])
            df_oos = df_oos.dropna(subset=CANONICAL_FEATURES+['target'])
            if len(df_is) < 40 or len(df_oos) < 5: continue

            pos = int(df_is['target'].sum()); neg = len(df_is)-pos
            if pos == 0: continue
            dtrain = xgb.DMatrix(df_is[CANONICAL_FEATURES], label=df_is['target'].to_numpy().astype(int))
            params = {'objective':'binary:logistic','max_depth':4,'learning_rate':0.05,
                      'reg_alpha':1.0,'reg_lambda':3.0,'subsample':0.8,'colsample_bytree':0.8,
                      'scale_pos_weight': neg/max(pos,1),'eval_metric':'logloss','seed':42,'verbosity':0}
            model = xgb.train(params, dtrain, num_boost_round=80)

            y_oos  = df_oos['target'].to_numpy().astype(int)
            probs  = model.predict(xgb.DMatrix(df_oos[CANONICAL_FEATURES]))
            signals = probs >= PROB_THRESHOLD
            n = int(signals.sum())
            if n == 0: continue
            fired = y_oos[signals]
            for lbl in fired:
                pnl = WIN_R if lbl==1 else -LOSS_R
                all_wins += int(lbl==1)
                total_n += 1
                all_eq.append(all_eq[-1] + pnl)
                peak = max(peak, all_eq[-1])
                max_dd = max(max_dd, peak - all_eq[-1])
        except: pass

    eq_arr = np.array(all_eq)
    net_r  = eq_arr[-1]
    wr     = all_wins / max(total_n, 1)
    cal    = calmar(eq_arr, max_dd)
    # Estimate ROI% and MaxDD% (map R to USD: 1R = 25 USD on 5000 USD cap)
    roi_pct   = net_r * 25.0 / 5000.0 * 100.0
    max_dd_pct= max_dd * 25.0 / 5000.0 * 100.0
    return {'n_trades': total_n, 'win_rate': wr, 'net_r': net_r,
            'roi_pct': roi_pct, 'max_dd_pct': max_dd_pct, 'calmar': cal}


def run():
    windows = load_oos_windows()
    print(f'Running dynamic OOS eval across {len(windows)} windows with top-{DYNAMIC_POOL_SIZE} dynamic pool...')
    print('='*80)

    rows = []
    # Global IS start (first data available, use 2022 as safe earliest IS)
    global_is_start = datetime(2022, 1, 1, tzinfo=timezone.utc)

    for w in windows:
        wid  = w['window_id']
        name = w['name'][:30]
        t_start = datetime.fromisoformat(w['start_date']).replace(tzinfo=timezone.utc)
        t_end   = datetime.fromisoformat(w['end_date']).replace(tzinfo=timezone.utc) + timedelta(days=1)

        print(f'\nW{wid:02d} [{w["start_date"]} -> {w["end_date"]}] {name}')

        # IS data = everything before this window (with purge)
        t_is_end = t_start - timedelta(hours=24)

        # ── Gate 1: Screen assets on IS data ─────────────────────────────
        pool = screen_assets_is(ALL_ASSETS, global_is_start, t_is_end)
        pool_syms = [a['symbol'] for a in pool]
        print(f'  Pool ({len(pool_syms)}): {pool_syms[:8]}...' if len(pool_syms)>8 else f'  Pool ({len(pool_syms)}): {pool_syms}')

        if not pool:
            print(f'  [SKIP] No assets passed IS gate')
            rows.append({'window': f'W{wid:02d}', 'name': name,
                         'n_trades':0,'win_rate':0,'roi_pct':0,'max_dd_pct':0,'calmar':0,'status':'SKIP',
                         'pool_size':0, 'pool_assets':''})
            continue

        # ── Gate 2: Evaluate on OOS window ───────────────────────────────
        metrics = eval_oos_window(pool, t_start, t_end, global_is_start)
        n  = metrics['n_trades']
        wr = metrics['win_rate']
        roi= metrics['roi_pct']
        dd = metrics['max_dd_pct']
        cal= metrics['calmar']

        # Status: PASS = ROI>0 and DD<=4.5%; PROFIT = ROI>0 but DD>4.5%
        if roi > 0 and dd <= 4.5:
            status = 'PASS'
        elif roi > 0:
            status = 'PROFIT'
        else:
            status = 'FAIL'

        print(f'  Trades={n} | WR={wr:.1%} | ROI={roi:+.1f}% | MaxDD={dd:.2f}% | Calmar={cal:.2f} | {status}')

        rows.append({
            'window': f'W{wid:02d}', 'name': name,
            'n_trades': n, 'win_rate': round(wr*100,1),
            'roi_pct': round(roi,1), 'max_dd_pct': round(dd,2),
            'calmar': round(cal,2), 'status': status,
            'pool_size': len(pool_syms),
            'pool_assets': ','.join(pool_syms),
        })

    # ── Summary ───────────────────────────────────────────────────────────
    df_out = pd.DataFrame(rows)
    df_out.to_csv(OUTPUT_CSV, index=False)
    print('\n' + '='*80)
    print('DYNAMIC OOS SUMMARY')
    print('='*80)
    passed   = len(df_out[df_out['status']=='PASS'])
    profited = len(df_out[df_out['status']=='PROFIT'])
    failed   = len(df_out[df_out['status']=='FAIL'])
    avg_cal  = df_out[df_out['calmar']>0]['calmar'].mean()
    avg_roi  = df_out['roi_pct'].mean()
    avg_dd   = df_out['max_dd_pct'].mean()
    print(f'PASS: {passed}/20 | PROFIT: {profited}/20 | FAIL: {failed}/20')
    print(f'Avg ROI: {avg_roi:+.1f}% | Avg MaxDD: {avg_dd:.2f}% | Avg Calmar: {avg_cal:.2f}')
    print(f'Results -> {OUTPUT_CSV}')
    print()
    print(f'{"Win":>4} {"Name":30} {"Trades":>7} {"WR%":>6} {"ROI%":>7} {"DD%":>6} {"Calmar":>8} Status')
    print('-'*80)
    for _, r in df_out.iterrows():
        print(f'{r["window"]:>4} {r["name"]:30} {r["n_trades"]:>7} {r["win_rate"]:>5.1f}% {r["roi_pct"]:>+6.1f}% {r["max_dd_pct"]:>5.2f}% {r["calmar"]:>8.2f} {r["status"]}')

    return df_out


if __name__ == '__main__':
    run()
