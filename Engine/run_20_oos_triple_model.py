import sys
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
import os
import xgboost as xgb

REPO_ROOT = Path('.').resolve()
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / 'Engine'))

from scratch.fast_numba_oos_engine import compile_dataset_with_numba, WINDOWS_PATH, CRITERIA_PATH
from Engine.strategy.s1_dual_model_orderflow import InstitutionalDualModelEngine
from Engine.run_20_oos_vwap_ml import process_asset, VWAP_FEATURES

def main():
    print('=' * 135)
    print('INSTITUTIONAL QUANTITATIVE MASTER ENGINE: TRIPLE-MODEL (S1 + T1 + V1 VWAP)')
    print('=' * 135)
    
    with open(WINDOWS_PATH, 'r', encoding='utf-8') as f:
        windows = json.load(f)
        
    df_t1 = InstitutionalDualModelEngine.load_t1_breakout_trades()
    all_data = compile_dataset_with_numba()
    
    # 1. GENERATE VWAP MASTER SET
    print('Generating VWAP V1 Baseline...')
    all_v1_trades = []
    DATA_DIR = 'Engine/binance_backtesting_data'
    ALL_ASSETS = ['BTC', 'ETH', 'XRP', 'BNB', 'DOGE', 'ADA', 'TRX', 'LINK', 'DOT', 'LTC', 'BCH']
    for asset in ALL_ASSETS:
        filepath = os.path.join(DATA_DIR, f'{asset}USDT_15m_master_2020_2026.parquet')
        if not os.path.exists(filepath): continue
        df = pd.read_parquet(filepath).dropna(subset=['high', 'low', 'close', 'volume_base', 'datetime_utc']).reset_index(drop=True)
        df_res = process_asset(asset, df)
        if not df_res.empty: all_v1_trades.append(df_res)
    
    v1_master_df = pd.concat(all_v1_trades, ignore_index=True).sort_values('datetime').dropna().reset_index(drop=True)
    
    # Load BTC 4h for dynamic trailing volatility (S1 scaling)
    cache_dir = REPO_ROOT / "scratch" / "cache_multi_tf"
    df_btc = pd.read_parquet(cache_dir / "BTCUSDT_4h.parquet")
    df_btc['time'] = pd.to_datetime(df_btc['time'], utc=True)
    df_btc.sort_values('time', inplace=True)
    df_btc.reset_index(drop=True, inplace=True)
    df_btc['atr_pct'] = (df_btc['atr'] / df_btc['close']) * 100.0
    df_btc['trailing_30d_atr_pct'] = df_btc['atr_pct'].rolling(180).mean()

    engine = InstitutionalDualModelEngine(
        capital=5000.0,
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
    
    passed_count = 0
    total_trades = 0
    total_pnl = 0.0
    
    for w_id, w in enumerate(windows, 1):
        w_name = w['name']
        start_ms = int(pd.Timestamp(w['start_date'], tz='UTC').timestamp() * 1000)
        end_ms = int(pd.Timestamp(w['end_date'], tz='UTC').timestamp() * 1000)
        
        train_mask = (all_data['open_time_ms'] >= start_ms - int(180 * 86400 * 1000)) & (all_data['open_time_ms'] < start_ms)
        test_mask = (all_data['open_time_ms'] >= start_ms) & (all_data['open_time_ms'] <= end_ms)
        
        train_set = all_data[train_mask]
        test_set = all_data[test_mask]
        
        s_ts = pd.Timestamp(w["start_date"], tz="UTC")
        sub_btc = df_btc[df_btc['time'] < s_ts]
        trailing_vol = sub_btc['trailing_30d_atr_pct'].iloc[-1] if len(sub_btc) > 0 else 1.75
        
        # S1 Training & Scoring
        if len(train_set) >= 500 and len(test_set) > 0:
            ridge, clf, mu, sd, calib_thresh = engine.train_models(train_set)
            selected_s1 = engine.score_test_candidates(test_set, ridge, clf, mu, sd, calib_thresh, trailing_vol_pct=trailing_vol)
        else:
            selected_s1 = pd.DataFrame()
            
        # V1 (VWAP) Training & Scoring
        start_dt = pd.to_datetime(w['start_date'])
        end_dt = pd.to_datetime(w['end_date'])
        train_start = start_dt - pd.Timedelta(days=180)
        
        train_v1 = v1_master_df[(v1_master_df['datetime'] >= train_start) & (v1_master_df['datetime'] < start_dt)]
        test_v1 = v1_master_df[(v1_master_df['datetime'] >= start_dt) & (v1_master_df['datetime'] <= end_dt)]
        
        selected_v1_list = []
        if len(train_v1) >= 500 and len(test_v1) > 0:
            X_train = train_v1[VWAP_FEATURES]
            y_train = train_v1['outcome']
            v1_clf = xgb.XGBRegressor(
                n_estimators=100, max_depth=3, learning_rate=0.05, reg_alpha=2.0, reg_lambda=5.0,
                subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1
            )
            v1_clf.fit(X_train, y_train)
            
            X_test = test_v1[VWAP_FEATURES]
            preds = v1_clf.predict(X_test)
            test_v1 = test_v1.copy()
            test_v1['ml_prob'] = preds
            
            for idx in range(len(test_v1)):
                if test_v1['ml_prob'].iloc[idx] >= 0.15: # V1 Threshold
                    selected_v1_list.append({
                        'time': int(test_v1['datetime'].iloc[idx].timestamp() * 1000),
                        'strategy': 'V1',
                        'symbol': test_v1['asset'].iloc[idx] + 'USDT',
                        'r_gain': test_v1['outcome'].iloc[idx],
                        'prob': float(test_v1['ml_prob'].iloc[idx]),
                        'hold_bars': 24
                    })
        
        s1_events = []
        if not selected_s1.empty:
            sym_col = 'symbol' if 'symbol' in selected_s1.columns else 'asset'
            gain_col = 'outcome' if 'outcome' in selected_s1.columns else ('realized_r' if 'realized_r' in selected_s1.columns else 'r_gain')
            for idx in range(len(selected_s1)):
                s1_events.append({
                    'time': selected_s1['open_time_ms'].iloc[idx],
                    'strategy': 'S1',
                    'symbol': selected_s1[sym_col].iloc[idx],
                    'r_gain': selected_s1[gain_col].iloc[idx],
                    'prob': selected_s1['prob'].iloc[idx],
                    'hold_bars': selected_s1['bars_held'].iloc[idx] if 'bars_held' in selected_s1.columns else 24
                })
                
        t1_events = []
        if df_t1 is not None and not df_t1.empty:
            t1_time_col = 'time'
            df_t1_sub = df_t1[(df_t1[t1_time_col] >= start_ms) & (df_t1[t1_time_col] <= end_ms)]
            for idx in range(len(df_t1_sub)):
                t1_events.append({
                    'time': df_t1_sub[t1_time_col].iloc[idx],
                    'strategy': 'T1',
                    'symbol': df_t1_sub['symbol'].iloc[idx],
                    'r_gain': df_t1_sub['r_gain'].iloc[idx],
                    'prob': 0.55,
                    'hold_bars': df_t1_sub['hold_bars'].iloc[idx] if 'hold_bars' in df_t1_sub.columns else 24
                })
                
        combined = s1_events + t1_events + selected_v1_list
        combined.sort(key=lambda x: (x['time'], -x['prob']))
        
        equity = 5000.0
        peak_equity = equity
        s1_positions = []
        t1_positions = []
        v1_positions = []
        symbol_cooldown = {}
        
        w_s1_tr = 0
        w_t1_tr = 0
        w_v1_tr = 0
        w_wins = 0
        
        for ev in combined:
            if ((peak_equity - equity) / peak_equity) * 100.0 >= 4.5: continue
            
            t_entry = ev['time']
            strat = ev['strategy']
            sym = ev['symbol']
            r_gain = ev['r_gain']
            prob = ev['prob']
            hold_ms = int(ev['hold_bars']) * 15 * 60 * 1000
            
            s1_positions = [p for p in s1_positions if p[0] > t_entry]
            t1_positions = [p for p in t1_positions if p[0] > t_entry]
            v1_positions = [p for p in v1_positions if p[0] > t_entry]
            
            if sym in symbol_cooldown and t_entry < symbol_cooldown[sym]: continue
            
            current_profit = equity - 5000.0
            cur_peak_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
            cur_cap_dd = ((5000.0 - equity) / 5000.0) * 100.0 if equity < 5000.0 else 0.0
            
            if current_profit >= 180.0:
                cur_max_s1 = 3
                cur_max_tot = 4
            else:
                cur_max_s1 = 2
                cur_max_tot = 3
                
            if strat == 'S1':
                if len(s1_positions) >= cur_max_s1 or (len(s1_positions) + len(t1_positions) + len(v1_positions)) >= cur_max_tot: continue
                if cur_cap_dd >= 2.0 or cur_peak_dd >= 4.0: risk = 14.0
                else: risk = 54.0 * (1.35 if prob >= 0.46 else 1.0)
                if current_profit >= 50.0: risk = min(90.0, risk + current_profit * 0.05)
                
                trade_pnl = risk * r_gain
                equity += trade_pnl
                peak_equity = max(peak_equity, equity)
                s1_positions.append((t_entry + hold_ms, sym))
                w_s1_tr += 1
                if r_gain > 0: w_wins += 1
                
            elif strat == 'T1':
                if len(t1_positions) >= 2 or (len(s1_positions) + len(t1_positions) + len(v1_positions)) >= cur_max_tot: continue
                if cur_cap_dd >= 2.0 or cur_peak_dd >= 4.0: risk = 14.0
                else: risk = 42.0
                if current_profit >= 50.0: risk = min(60.0, risk + current_profit * 0.05)
                
                trade_pnl = risk * r_gain
                equity += trade_pnl
                peak_equity = max(peak_equity, equity)
                t1_positions.append((t_entry + hold_ms, sym))
                w_t1_tr += 1
                if r_gain > 0: w_wins += 1
                
            elif strat == 'V1':
                if len(v1_positions) >= 2 or (len(s1_positions) + len(t1_positions) + len(v1_positions)) >= cur_max_tot: continue
                if cur_cap_dd >= 2.0 or cur_peak_dd >= 4.0: risk = 14.0
                else: risk = 40.0
                if current_profit >= 50.0: risk = min(65.0, risk + current_profit * 0.05)
                
                trade_pnl = risk * r_gain
                equity += trade_pnl
                peak_equity = max(peak_equity, equity)
                v1_positions.append((t_entry + hold_ms, sym))
                w_v1_tr += 1
                if r_gain > 0: w_wins += 1
                
            symbol_cooldown[sym] = t_entry + hold_ms
            
        net_pnl = equity - 5000.0
        net_roi = (net_pnl / 5000.0) * 100.0
        max_dd = ((peak_equity - equity) / peak_equity) * 100.0
        n_trd = w_s1_tr + w_t1_tr + w_v1_tr
        wr = (w_wins / n_trd * 100.0) if n_trd > 0 else 0.0
        
        is_pass = (net_roi >= 10.0) and (max_dd <= 5.0) and (wr >= 40.0) and (n_trd >= 15)
        status = 'PASS' if is_pass else ('PROFIT' if net_pnl > 0 and max_dd <= 5.0 else ('CASH' if n_trd == 0 else 'FAIL'))
        
        if is_pass: passed_count += 1
        total_trades += n_trd
        total_pnl += net_pnl
        
        print(f'W{w_id:02d} | {w_name[:38]:<38} | {n_trd:<6d} | S:{w_s1_tr} T:{w_t1_tr} V:{w_v1_tr} | {wr:>5.1f}% | {net_pnl:>+10.2f} USD | {net_roi:>+7.2f}% | {max_dd:>5.2f}% | {status:<6}')

    print('=' * 135)
    print(f'MASTER MULTIVERSE SCORECARD: Passed: {passed_count}/20 | Total Trades: {total_trades:,d} | Total PnL: {total_pnl:+,.2f} USD')
    print('=' * 135)

if __name__ == '__main__':
    main()
