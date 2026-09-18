"""
================================================================================
ENGINE RESEARCH: HYBRID DYNAMIC ASSET SCREENER (GATE 1 -- HISTORICAL QUALITY)
================================================================================
PURPOSE:
    Nightly/weekly batch job that evaluates ALL 98 available Forex_Backtesting_Data
    assets against an institutional quality gate. Assets that pass are written to
    the APPROVED LIVE POOL JSON, which the Signal Auction and Live Dry-Run consume.

GATES:
    Gate 1a -- Minimum Calmar Ratio (trailing 90-day rolling OOS simulation)
    Gate 1b -- Minimum Win Rate on ratchet-labeled setups (>= 46%)
    Gate 1c -- Minimum Signal Frequency (>= 4 setups per 90-day window)
    Gate 1d -- Hurst Exponent regime check (0.25 <= H <= 0.60)
    Gate 1e -- Yang-Zhang Volatility range (sufficient but not excessive noise)

OUTPUT:
    Engine/research/approved_pool.json   -- approved assets ranked by Calmar
    Engine/research/screener_report.csv  -- full per-asset breakdown

ANTI-LOOKAHEAD GUARANTEE:
    - train window is strictly BEFORE eval window (causal split)
    - All features computed with backward-looking rolling operators only
    - eval_window = last EVAL_DAYS calendar days of available data
    - train_window = data strictly prior to eval_window start

--------------------------------------------------------------------------------
AUDIT Ox_Alpha_36 (2026-09-18) -- CORRECTION APPLIED
--------------------------------------------------------------------------------
S-1  simulate_ratchet_pnl() paid every `target == 1` a flat +2.5R. But
     create_labels_ratchet sets `target = 1 if r_realized > 0`, so a +0.15R
     break-even ratchet exit was admitted as a full 2.5R winner. Under the
     6-rung ratchet those scratch exits are the modal outcome, so Gate 1a
     (min Calmar) and the pool ranking were both computed on inflated PnL.
     The function now consumes `r_realized` directly.
     Effect: break-even win rate moves from 28.57% to ~55.7%. Expect the
     approved pool to shrink materially; that is the correct behaviour, not
     a regression.
================================================================================
"""
import os, sys, json, logging, warnings
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
warnings.filterwarnings('ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.strategy_kernel import (
    CANONICAL_FEATURES, engineer_features_polars, create_labels_ratchet)
from Engine.research.features.advanced_quant_math import (
    compute_yang_zhang_volatility, compute_hurst_exponent_fast)

DATA_DIR            = os.path.join(PROJECT_ROOT, 'Forex_Backtesting_Data')
APPROVED_POOL_PATH  = os.path.join(SCRIPT_DIR, 'approved_pool.json')
SCREENER_REPORT_PATH = os.path.join(SCRIPT_DIR, 'screener_report.csv')

GATE_MIN_CALMAR           = 5.0
GATE_MIN_WIN_RATE         = 0.46
GATE_MIN_SETUPS_PER_MONTH = 4
GATE_MAX_HURST            = 0.60
GATE_MIN_HURST            = 0.25
GATE_MIN_YZ_VOL           = 1e-5
GATE_MAX_YZ_VOL           = 0.08
EVAL_DAYS                 = 90
TRAIN_MIN_DAYS            = 120
APPROVED_POOL_SIZE        = 20
PROB_THRESHOLD            = 0.54

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
log = logging.getLogger('AssetScreener')


def discover_all_assets() -> List[str]:
    assets = []
    for f in sorted(os.listdir(DATA_DIR)):
        if f.endswith('_15m_real.parquet'):
            assets.append(f.replace('_15m_real.parquet', ''))
    return assets


def simulate_ratchet_pnl(r_realized, probs, threshold=PROB_THRESHOLD):
    """
    S-1 FIX: pay each fired trade its REALISED R-multiple.
    Previously signed as (y_true, probs, threshold, win_r=2.5, loss_r=-1.0) and
    booked a constant payoff off the binary label, which counted +0.15R
    break-even exits as full 2.5R wins.
    """
    signals = probs >= threshold
    n_trades = int(signals.sum())
    if n_trades == 0:
        return np.array([0.0]), 0, 0.0, 0.0
    fired = r_realized[signals]
    equity = np.zeros(n_trades + 1)
    peak, max_dd, wins = 0.0, 0.0, 0
    for i, r in enumerate(fired):
        wins += int(r > 0)
        equity[i+1] = equity[i] + float(r)
        peak = max(peak, equity[i+1])
        max_dd = max(max_dd, peak - equity[i+1])
    return equity, n_trades, wins/n_trades, max_dd


def compute_calmar(equity_curve, max_dd_r):
    net_pnl = equity_curve[-1]
    if net_pnl <= 0: return 0.0
    if max_dd_r <= 0: return 999.0
    return net_pnl / max_dd_r


def train_quick_xgboost(X_train, y_train):
    import xgboost as xgb
    if len(y_train) < 60: return None
    pos = int(y_train.sum()); neg = len(y_train) - pos
    pos_weight = neg / max(pos, 1)
    dtrain = xgb.DMatrix(X_train, label=y_train)
    params = {'objective': 'binary:logistic', 'max_depth': 4, 'learning_rate': 0.05,
              'reg_alpha': 1.0, 'reg_lambda': 3.0, 'subsample': 0.8, 'colsample_bytree': 0.8,
              'scale_pos_weight': pos_weight, 'eval_metric': 'logloss', 'seed': 42, 'verbosity': 0}
    return xgb.train(params, dtrain, num_boost_round=80)


def screen_single_asset(symbol: str) -> Optional[Dict]:
    import xgboost as xgb
    try:
        df = engineer_features_polars(symbol, DATA_DIR)
    except Exception as e:
        log.debug(f'[{symbol}] Feature eng failed: {e}'); return None
    if df is None or len(df) < 200: return None

    df['_dt'] = pd.to_datetime(df['time'], unit='s', utc=True)
    t_max = df['_dt'].max()
    t_eval_start = t_max - timedelta(days=EVAL_DAYS)
    df_eval  = df[df['_dt'] >= t_eval_start].copy()
    df_train = df[df['_dt'] <  t_eval_start].copy()
    span_days = (df_train['_dt'].max() - df_train['_dt'].min()).days if len(df_train) > 0 else 0
    if span_days < TRAIN_MIN_DAYS: return None

    try:
        df_train_lbl = create_labels_ratchet(df_train)
        df_eval_lbl  = create_labels_ratchet(df_eval)
    except Exception as e:
        log.debug(f'[{symbol}] Label failed: {e}'); return None

    df_train_lbl = df_train_lbl.dropna(subset=CANONICAL_FEATURES + ['target'])
    df_eval_lbl  = df_eval_lbl.dropna(subset=CANONICAL_FEATURES + ['target'])
    if len(df_train_lbl) < 60 or len(df_eval_lbl) < 20: return None

    model = train_quick_xgboost(df_train_lbl[CANONICAL_FEATURES], df_train_lbl['target'].to_numpy().astype(int))
    if model is None: return None

    probs  = model.predict(xgb.DMatrix(df_eval_lbl[CANONICAL_FEATURES]))
    r_eval = df_eval_lbl['r_realized'].to_numpy(np.float64)   # S-1 FIX

    n_signals = int((probs >= PROB_THRESHOLD).sum())
    if n_signals < GATE_MIN_SETUPS_PER_MONTH: return None

    equity, n_trades, win_rate, max_dd_r = simulate_ratchet_pnl(r_eval, probs)
    if win_rate < GATE_MIN_WIN_RATE: return None

    calmar = compute_calmar(equity, max_dd_r)
    if calmar < GATE_MIN_CALMAR: return None

    close_p = df_eval['close'].to_numpy(np.float64)
    open_p  = df_eval['open'].to_numpy(np.float64)
    high_p  = df_eval['high'].to_numpy(np.float64)
    low_p   = df_eval['low'].to_numpy(np.float64)
    hurst_arr = compute_hurst_exponent_fast(close_p, window=60)
    hurst_med = float(np.nanmedian(hurst_arr[hurst_arr > 0]))
    yz_arr    = compute_yang_zhang_volatility(open_p, high_p, low_p, close_p, window=20)
    yz_med    = float(np.nanmedian(yz_arr[yz_arr > 0]))
    if not (GATE_MIN_HURST <= hurst_med <= GATE_MAX_HURST): return None
    if not (GATE_MIN_YZ_VOL <= yz_med <= GATE_MAX_YZ_VOL): return None

    log.info(f'[{symbol}] PASS | Calmar={calmar:.2f} | WR={win_rate:.1%} | Trades={n_trades} | Hurst={hurst_med:.3f}')
    return {
        'symbol': symbol, 'calmar': round(calmar, 4), 'win_rate': round(win_rate, 4),
        'n_trades': n_trades, 'n_signals': n_signals, 'net_pnl_r': round(float(equity[-1]), 3),
        'max_dd_r': round(max_dd_r, 3), 'hurst': round(hurst_med, 4), 'yz_vol': round(yz_med, 8),
        'eval_start': t_eval_start.isoformat(), 'train_span_days': span_days,
        'screened_at': datetime.now(timezone.utc).isoformat(), 'gate_pass': True,
    }


def run_screener(force_assets=None, pool_size=APPROVED_POOL_SIZE):
    assets = force_assets if force_assets else discover_all_assets()
    log.info(f'Screening {len(assets)} assets...')
    results, failed = [], []
    for sym in assets:
        r = screen_single_asset(sym)
        (results if r else failed).append(r if r else {'symbol': sym, 'calmar': 0, 'gate_pass': False})

    passing = [r for r in results if r and r.get('gate_pass')]
    passing.sort(key=lambda x: x['calmar'], reverse=True)
    top_pool = passing[:pool_size]

    pool_out = {
        'generated_at': datetime.now(timezone.utc).isoformat(), 'eval_days': EVAL_DAYS,
        'gate_thresholds': {'min_calmar': GATE_MIN_CALMAR, 'min_win_rate': GATE_MIN_WIN_RATE,
                            'min_signals': GATE_MIN_SETUPS_PER_MONTH, 'hurst_range': [GATE_MIN_HURST, GATE_MAX_HURST]},
        'pnl_accounting': 'r_realized',
        'approved_count': len(top_pool), 'screened_count': len(assets), 'assets': top_pool,
    }
    with open(APPROVED_POOL_PATH, 'w', encoding='utf-8') as f:
        json.dump(pool_out, f, indent=2)
    pd.DataFrame(results + [r for r in failed if isinstance(r, dict)]).to_csv(SCREENER_REPORT_PATH, index=False)
    log.info(f'DONE: {len(top_pool)} assets admitted. Pool -> {APPROVED_POOL_PATH}')
    for i, r in enumerate(top_pool[:10], 1):
        log.info(f'  {i:2d}. {r["symbol"]:<12s} Calmar={r["calmar"]:>7.2f} WR={r["win_rate"]:.1%} Hurst={r["hurst"]:.3f}')
    return top_pool


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--assets', nargs='+')
    ap.add_argument('--pool-size', type=int, default=APPROVED_POOL_SIZE)
    args = ap.parse_args()
    run_screener(force_assets=args.assets, pool_size=args.pool_size)
