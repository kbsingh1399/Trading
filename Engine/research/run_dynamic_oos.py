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

--------------------------------------------------------------------------------
AUDIT Ox_Alpha_36 (2026-09-18) -- CORRECTIONS APPLIED
--------------------------------------------------------------------------------
S-1  Winners were booked at a flat +2.5R via `WIN_R`, but `target == 1` only means
     `r_realized > 0`. A +0.15R break-even ratchet exit was therefore recorded as a
     full 2.5R win. Both constants are removed; PnL is now `r_realized`, which
     create_labels_ratchet already computes alongside `target`.
     Effect: break-even win rate moves from 28.57% to ~55.7%.

S-3a Drawdown was computed by concatenating each asset's trades one after another,
     so `max_dd` depended on pool iteration order rather than calendar time.
     Trades are now merged chronologically into a single portfolio equity curve.

S-3b `PASS` was `roi > 0 and dd <= 4.5`; Engine/target_oos_criteria.json was never
     loaded. The criteria file is now the gate, and per-window failing gates are
     recorded in the CSV.

S-3c calmar() returned the sentinel 999.0 on zero drawdown while the summary
     averaged only `calmar > 0`, mixing denominators. It now returns NaN and the
     mean is reported with an explicit window count.

KNOWN REMAINING GAP (not fixed here, requires a kernel change):
     MAX_CONCURRENT_POSITIONS is still not enforced, because create_labels_ratchet
     does not return the exit bar of each trade. To close this, have it emit an
     `exit_bar_offset` column (the loop variable `j` at break) so overlapping
     trades can be identified and capped. Until then this evaluation assumes
     unlimited concurrency and therefore OVERSTATES achievable capacity.
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
CRITERIA_FILE    = os.path.join(PROJECT_ROOT, 'Engine', 'target_oos_criteria.json')
OUTPUT_CSV       = os.path.join(SCRIPT_DIR, 'dynamic_oos_results.csv')

# -- Screening gate thresholds (same as asset_screener.py) --------------------
GATE_MIN_CALMAR       = 3.0    # loosened slightly since IS data is shorter per window
GATE_MIN_WIN_RATE     = 0.44
GATE_MIN_SIGNALS      = 3
GATE_MAX_HURST        = 0.62
GATE_MIN_HURST        = 0.20
GATE_MIN_YZ_VOL       = 1e-6
GATE_MAX_YZ_VOL       = 0.10
DYNAMIC_POOL_SIZE     = 12     # top-12 assets per window
PROB_THRESHOLD        = 0.54
PURGE_BARS            = 96     # 24h purge at each boundary
HARD_DD_STOP_PCT      = 4.5    # Tier-0 freeze; must also hold for a window to PASS

# S-1: WIN_R / LOSS_R deliberately removed. Do not reintroduce a constant payoff.

# -- Discover all 98 assets ---------------------------------------------------
ALL_ASSETS = sorted([f.replace('_15m_real.parquet','')
                     for f in os.listdir(DATA_DIR) if f.endswith('_15m_real.parquet')])
print(f'Assets available: {len(ALL_ASSETS)}')


def load_oos_windows():
    with open(OOS_WINDOWS_FILE) as f:
        return json.load(f)


def load_criteria() -> Dict:
    """S-3b: the acceptance bar now comes from the committed criteria file."""
    with open(CRITERIA_FILE) as f:
        return json.load(f)['target_criteria']


CRITERIA   = load_criteria()
RISK_USD   = float(CRITERIA['base_risk_usd'])        # 50.0 per the criteria file
CAPITAL    = float(CRITERIA['initial_capital_usd'])  # 5000.0


def simulate_pnl(r_realized, probs, threshold=PROB_THRESHOLD):
    """S-1: pay each fired trade its realised R, not a constant."""
    signals = probs >= threshold
    n = int(signals.sum())
    if n == 0:
        return np.array([0.0]), 0, 0.0, 0.0
    fired = r_realized[signals]
    eq = np.zeros(n+1); peak = 0.0; max_dd = 0.0; wins = 0
    for i, r in enumerate(fired):
        wins += int(r > 0)
        eq[i+1] = eq[i] + float(r)
        peak = max(peak, eq[i+1])
        max_dd = max(max_dd, peak - eq[i+1])
    return eq, n, wins/n, max_dd


def calmar(eq, max_dd):
    net = eq[-1]
    if net <= 0:
        return 0.0
    if max_dd <= 0:
        return float('nan')   # S-3c: undefined, not a 999 sentinel
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
            except Exception:
                continue

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

            r_val   = df_val['r_realized'].to_numpy(np.float64)   # S-1
            probs   = model.predict(xgb.DMatrix(df_val[CANONICAL_FEATURES]))
            n_sig   = int((probs >= PROB_THRESHOLD).sum())
            if n_sig < GATE_MIN_SIGNALS: continue

            eq, n_tr, wr, max_dd_r = simulate_pnl(r_val, probs)
            if wr < GATE_MIN_WIN_RATE: continue
            cal = calmar(eq, max_dd_r)
            if not np.isnan(cal) and cal < GATE_MIN_CALMAR: continue

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
        except Exception:
            pass
    results.sort(key=lambda x: (-1.0 if np.isnan(x['calmar']) else x['calmar']), reverse=True)
    return results[:DYNAMIC_POOL_SIZE]


def eval_oos_window(pool_assets, t_oos_start, t_oos_end, t_is_start):
    """
    Train on full IS data for the admitted pool assets, evaluate on the OOS window.
    S-3a: trades from every asset are merged CHRONOLOGICALLY before the portfolio
    equity curve and drawdown are computed.
    """
    import xgboost as xgb
    trades: List[Tuple[np.datetime64, float]] = []

    for asset_info in pool_assets:
        sym = asset_info['symbol']
        try:
            df = engineer_features_polars(sym, DATA_DIR)
            if df is None: continue
            df['_dt'] = pd.to_datetime(df['time'], unit='s', utc=True)

            # Full IS for training (with purge)
            t_purge = t_oos_start - timedelta(minutes=15 * PURGE_BARS)
            df_is  = df[(df['_dt'] >= t_is_start) & (df['_dt'] < t_purge)].copy()
            df_oos = df[(df['_dt'] >= t_oos_start) & (df['_dt'] < t_oos_end)].copy()
            if len(df_is) < 80 or len(df_oos) < 15: continue

            try:
                df_is  = create_labels_ratchet(df_is)
                df_oos = create_labels_ratchet(df_oos)
            except Exception:
                continue

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

            probs   = model.predict(xgb.DMatrix(df_oos[CANONICAL_FEATURES]))
            signals = probs >= PROB_THRESHOLD
            if int(signals.sum()) == 0: continue

            fired_dt = df_oos.loc[signals, '_dt'].to_numpy()
            fired_r  = df_oos.loc[signals, 'r_realized'].to_numpy(np.float64)  # S-1
            trades.extend(zip(fired_dt, fired_r))
        except Exception:
            pass

    if not trades:
        return {'n_trades': 0, 'win_rate': 0.0, 'net_r': 0.0,
                'roi_pct': 0.0, 'max_dd_pct': 0.0, 'calmar': 0.0}

    trades.sort(key=lambda t: t[0])                      # S-3a
    eq = [0.0]; peak = 0.0; max_dd = 0.0; wins = 0
    for _dt, r in trades:
        wins += int(r > 0)
        eq.append(eq[-1] + float(r))
        peak = max(peak, eq[-1])
        max_dd = max(max_dd, peak - eq[-1])

    eq_arr  = np.array(eq)
    total_n = len(trades)
    net_r   = float(eq_arr[-1])
    wr      = wins / total_n
    cal     = calmar(eq_arr, max_dd)
    # Flat-risk mapping using the criteria file's own risk unit (50 USD on 5000 USD).
    roi_pct    = net_r  * RISK_USD / CAPITAL * 100.0
    max_dd_pct = max_dd * RISK_USD / CAPITAL * 100.0
    return {'n_trades': total_n, 'win_rate': wr, 'net_r': net_r,
            'roi_pct': roi_pct, 'max_dd_pct': max_dd_pct, 'calmar': cal}


def grade_window(roi, dd, wr, n) -> Tuple[str, str]:
    """S-3b: acceptance is Engine/target_oos_criteria.json, not `roi > 0`."""
    checks = {
        'roi':    roi      >= CRITERIA['min_roi_percent'],
        'dd':     dd       <= CRITERIA['max_dd_percent'],
        'wr':     wr*100.0 >= CRITERIA['min_winrate_percent'],
        'trades': n        >= CRITERIA['min_trades'],
        'freeze': dd       <= HARD_DD_STOP_PCT,
    }
    failed = ','.join(k for k, v in checks.items() if not v)
    if all(checks.values()):
        return 'PASS', ''
    return ('PROFIT' if roi > 0 else 'FAIL'), failed


def run():
    windows = load_oos_windows()
    print(f'Running dynamic OOS eval across {len(windows)} windows with top-{DYNAMIC_POOL_SIZE} dynamic pool...')
    print(f'Acceptance criteria: {CRITERIA}')
    print('WARNING: concurrency cap is NOT enforced (see module docstring) -- capacity is overstated.')
    print('='*80)

    rows = []
    global_is_start = datetime(2022, 1, 1, tzinfo=timezone.utc)

    for w in windows:
        wid  = w['window_id']
        name = w['name'][:30]
        t_start = datetime.fromisoformat(w['start_date']).replace(tzinfo=timezone.utc)
        t_end   = datetime.fromisoformat(w['end_date']).replace(tzinfo=timezone.utc) + timedelta(days=1)

        print(f'\nW{wid:02d} [{w["start_date"]} -> {w["end_date"]}] {name}')

        t_is_end = t_start - timedelta(minutes=15 * PURGE_BARS)

        pool = screen_assets_is(ALL_ASSETS, global_is_start, t_is_end)
        pool_syms = [a['symbol'] for a in pool]
        print(f'  Pool ({len(pool_syms)}): {pool_syms[:8]}...' if len(pool_syms)>8 else f'  Pool ({len(pool_syms)}): {pool_syms}')

        if not pool:
            print('  [SKIP] No assets passed IS gate')
            rows.append({'window': f'W{wid:02d}', 'name': name,
                         'n_trades':0,'win_rate':0,'net_r':0,'roi_pct':0,'max_dd_pct':0,
                         'calmar':float('nan'),'status':'SKIP','failed_gates':'no_pool',
                         'pool_size':0, 'pool_assets':''})
            continue

        metrics = eval_oos_window(pool, t_start, t_end, global_is_start)
        n, wr = metrics['n_trades'], metrics['win_rate']
        roi, dd, cal = metrics['roi_pct'], metrics['max_dd_pct'], metrics['calmar']
        status, failed = grade_window(roi, dd, wr, n)

        print(f'  Trades={n} | WR={wr:.1%} | NetR={metrics["net_r"]:+.2f} | ROI={roi:+.1f}% | '
              f'MaxDD={dd:.2f}% | Calmar={cal:.2f} | {status}'
              + (f' (failed: {failed})' if failed else ''))

        rows.append({
            'window': f'W{wid:02d}', 'name': name,
            'n_trades': n, 'win_rate': round(wr*100,1), 'net_r': round(metrics['net_r'],3),
            'roi_pct': round(roi,1), 'max_dd_pct': round(dd,2),
            'calmar': round(cal,2) if not np.isnan(cal) else float('nan'),
            'status': status, 'failed_gates': failed,
            'pool_size': len(pool_syms), 'pool_assets': ','.join(pool_syms),
        })

    df_out = pd.DataFrame(rows)
    df_out.to_csv(OUTPUT_CSV, index=False)
    print('\n' + '='*80)
    print('DYNAMIC OOS SUMMARY (post-audit accounting)')
    print('='*80)
    n_win    = len(df_out)
    passed   = int((df_out['status']=='PASS').sum())
    profited = int((df_out['status']=='PROFIT').sum())
    failed_n = int((df_out['status']=='FAIL').sum())
    skipped  = int((df_out['status']=='SKIP').sum())
    avg_roi  = df_out['roi_pct'].mean()
    avg_dd   = df_out['max_dd_pct'].mean()
    avg_cal  = df_out['calmar'].mean(skipna=True)
    n_cal    = int(df_out['calmar'].notna().sum())
    print(f'PASS: {passed}/{n_win} | PROFIT: {profited}/{n_win} | FAIL: {failed_n}/{n_win} | SKIP: {skipped}/{n_win}')
    print(f'Avg ROI: {avg_roi:+.1f}% | Avg MaxDD: {avg_dd:.2f}% | Avg Calmar: {avg_cal:.2f} over {n_cal}/{n_win} windows')
    print(f'NOTE: SKIP windows are included in the ROI/DD denominators. Any comparison against the')
    print(f'      fixed-18 arm must use the same denominator on both sides.')
    print(f'Results -> {OUTPUT_CSV}')
    print()
    print(f'{"Win":>4} {"Name":30} {"Trades":>7} {"WR%":>6} {"ROI%":>7} {"DD%":>6} {"Calmar":>8} Status / failed gates')
    print('-'*100)
    for _, r in df_out.iterrows():
        cal_s = f'{r["calmar"]:>8.2f}' if pd.notna(r['calmar']) else f'{"n/a":>8}'
        print(f'{r["window"]:>4} {r["name"]:30} {r["n_trades"]:>7} {r["win_rate"]:>5.1f}% '
              f'{r["roi_pct"]:>+6.1f}% {r["max_dd_pct"]:>5.2f}% {cal_s} {r["status"]}'
              + (f' ({r["failed_gates"]})' if r['failed_gates'] else ''))

    return df_out


if __name__ == '__main__':
    run()
