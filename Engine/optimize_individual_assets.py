import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR.parent) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import argparse
import json
import pandas as pd
import numpy as np
from numba import njit
import xgboost as xgb

from strategy.s1_liquidation_cascade import LiquidationCascadeSimulator
from strategy.smc_mayne import SMCMayneSimulator
from strategy.smc_kane import SMCKaneSimulator
from strategy.smc_marci import SMCMarciSimulator
from strategy.smc_marco import SMCMarcoSimulator
from strategy.smc_edgeful import SMCEdgefulSimulator
from strategy.smc_usman_noah import SMCUsmanNoahSimulator
from strategy.s2_institutional_ml import S2InstitutionalMLSimulator

from strategy.s2_institutional_ml import FrictionConfig, RatchetConfig

@njit
def generate_execution_labels(op, hi, lo, cl, atr, taker_fee, entry_slippage, exit_slippage, 
                              arm0_r, lock0_r, arm1_r, lock1_r, min_target_r, time_decay_bars, time_decay_r, 
                              forward_bars=96):
    T = len(op)
    labels_long = np.zeros(T, dtype=np.int32)
    labels_short = np.zeros(T, dtype=np.int32)
    
    for i in range(T - forward_bars - 1):
        # ENTRY ON NEXT OPEN
        px_long = op[i+1] * (1.0 + entry_slippage)
        raw_r_long = atr[i] * 2.0
        if raw_r_long <= 0: raw_r_long = px_long * 0.005
        
        stop_px_long = px_long - raw_r_long
        target_px_long = px_long + (raw_r_long * min_target_r)
        
        pos_stop_long = stop_px_long
        pos_target_long = target_px_long
        pos_max_r_long = 0.0
        
        long_pass = False
        
        for j in range(i+1, i+1+forward_bars):
            o_, h_, l_, c_ = op[j], hi[j], lo[j], cl[j]
            exit_px = 0.0
            
            if o_ <= pos_stop_long: exit_px = o_ * (1.0 - exit_slippage)
            elif o_ >= pos_target_long: exit_px = o_
            elif l_ <= pos_stop_long: exit_px = pos_stop_long * (1.0 - exit_slippage)
            elif h_ >= pos_target_long: exit_px = pos_target_long
            
            if exit_px > 0:
                gross = (exit_px - px_long)
                fees = (px_long + exit_px) * taker_fee
                if gross - fees > 0: long_pass = True
                break
                
            r_gain = (h_ - px_long) / raw_r_long
            if r_gain > pos_max_r_long: pos_max_r_long = r_gain
            if pos_max_r_long >= arm1_r:
                pos_stop_long = max(pos_stop_long, px_long + lock1_r * raw_r_long)
            elif pos_max_r_long >= arm0_r:
                pos_stop_long = max(pos_stop_long, px_long + lock0_r * raw_r_long)
                
            if (j - (i+1)) >= time_decay_bars and pos_max_r_long < time_decay_r:
                exit_px = c_
                gross = (exit_px - px_long)
                fees = (px_long + exit_px) * taker_fee
                if gross - fees > 0: long_pass = True
                break
                
        if long_pass: labels_long[i] = 1
        
        # SHORT
        px_short = op[i+1] * (1.0 - entry_slippage)
        raw_r_short = atr[i] * 2.0
        if raw_r_short <= 0: raw_r_short = px_short * 0.005
        
        stop_px_short = px_short + raw_r_short
        target_px_short = px_short - (raw_r_short * min_target_r)
        
        pos_stop_short = stop_px_short
        pos_target_short = target_px_short
        pos_max_r_short = 0.0
        
        short_pass = False
        
        for j in range(i+1, i+1+forward_bars):
            o_, h_, l_, c_ = op[j], hi[j], lo[j], cl[j]
            exit_px = 0.0
            
            if o_ >= pos_stop_short: exit_px = o_ * (1.0 + exit_slippage)
            elif o_ <= pos_target_short: exit_px = o_
            elif h_ >= pos_stop_short: exit_px = pos_stop_short * (1.0 + exit_slippage)
            elif l_ <= pos_target_short: exit_px = pos_target_short
            
            if exit_px > 0:
                gross = (px_short - exit_px)
                fees = (px_short + exit_px) * taker_fee
                if gross - fees > 0: short_pass = True
                break
                
            r_gain = (px_short - l_) / raw_r_short
            if r_gain > pos_max_r_short: pos_max_r_short = r_gain
            if pos_max_r_short >= arm1_r:
                pos_stop_short = min(pos_stop_short, px_short - lock1_r * raw_r_short)
            elif pos_max_r_short >= arm0_r:
                pos_stop_short = min(pos_stop_short, px_short - lock0_r * raw_r_short)
                
            if (j - (i+1)) >= time_decay_bars and pos_max_r_short < time_decay_r:
                exit_px = c_
                gross = (px_short - exit_px)
                fees = (px_short + exit_px) * taker_fee
                if gross - fees > 0: short_pass = True
                break
                
        if short_pass: labels_short[i] = 1
            
    return labels_long, labels_short


def run_optimization(asset: str):
    print(f"Starting ML-Driven Walk-Forward optimization for {asset}...")
    base_dir = Path(__file__).resolve().parent
    
    oos_file = base_dir / "oos_windows_20.json"
    with open(oos_file, "r") as f:
        windows = json.load(f)
        
    parquet_path = base_dir / "binance_backtesting_data" / f"{asset}USDT_15m_master_2020_2026.parquet"
    if not parquet_path.exists():
        print(f"Error: Could not find {parquet_path}")
        return
        
    print(f"Loading data from {parquet_path.name}...")
    df_full = pd.read_parquet(parquet_path)
    df_full['datetime_utc'] = pd.to_datetime(df_full['datetime_utc'])
    # Ensure tz-naive for comparisons
    if df_full['datetime_utc'].dt.tz is not None:
        df_full['datetime_utc'] = df_full['datetime_utc'].dt.tz_convert(None)
    
    simulators = {
        "LiquidationCascade": LiquidationCascadeSimulator(),
        "SMCMayne": SMCMayneSimulator(),
        "SMCKane": SMCKaneSimulator(),
        "SMCMarci": SMCMarciSimulator(),
        "SMCMarco": SMCMarcoSimulator(),
        "SMCEdgeful": SMCEdgefulSimulator(),
        "SMCUsmanNoah": SMCUsmanNoahSimulator(),
        "S2InstitutionalML": S2InstitutionalMLSimulator()
    }
    
    report = {}
    
    ml_features = [
        'rsi_14', 'vwap_zscore', 'volume_ratio', 'zc_div', 
        'long_liq_zs', 'short_liq_zs', 'liq_imbalance_ratio', 
        'oi_change_pct', 'funding_rate_pct', 'basis_usd', 
        'ls_ratio_global', 'ls_ratio_top', 'top_account_ratio', 
        'whale_index', 'taker_volume_ratio'
    ]
    
    for sim_name, sim in simulators.items():
        print(f"\n--- Running {sim_name} (ML Filter) ---")
        sim_results = []
        passes = 0
        
        for w in windows:
            w_name = w["name"]
            t_start = pd.to_datetime(w["start_date"]).tz_localize(None)
            t_end = pd.to_datetime(w["end_date"]).tz_localize(None)
            
            t_end = t_end + pd.Timedelta(days=1, milliseconds=-1)
            
            # 72h Purge between IS and OOS
            t_purge = t_start - pd.Timedelta(hours=72)
            
            df_is = df_full[df_full['datetime_utc'] < t_purge].copy()
            df_oos = df_full[(df_full['datetime_utc'] >= t_start) & (df_full['datetime_utc'] <= t_end)].copy()
            
            if len(df_is) < 1000 or len(df_oos) < 100:
                print(f"  [{w_name}] Skipping, insufficient data.")
                continue
                
            # Compute Labels for In-Sample
            op = df_is['open'].values
            hi = df_is['high'].values
            lo = df_is['low'].values
            cl = df_is['close'].values
            atr = df_is['atr_14'].clip(lower=df_is['close'] * 0.002).values
            
            fric = FrictionConfig()
            ratchet = RatchetConfig(
                arm0_r=0.85,
                lock0_r=0.45,
                arm1_r=1.25,
                lock1_r=0.85,
                min_target_r=1.75,
                time_decay_bars=36,
                time_decay_r=0.20
            )
            
            ll, ls = generate_execution_labels(
                op, hi, lo, cl, atr, 
                fric.taker_fee, fric.entry_slippage, fric.exit_slippage,
                ratchet.arm0_r, ratchet.lock0_r, ratchet.arm1_r, ratchet.lock1_r,
                ratchet.min_target_r, ratchet.time_decay_bars, ratchet.time_decay_r
            )
            df_is['label_long'] = ll
            df_is['label_short'] = ls
            
            # Event-conditioned sampling (Z > 1.2 per AGENTS.md), removed close vs open mismatch
            df_is_long = df_is[(df_is['long_liq_zs'] > 1.2)].dropna(subset=ml_features)
            df_is_short = df_is[(df_is['short_liq_zs'] > 1.2)].dropna(subset=ml_features)
            
            scale_pos_weight_long = (len(df_is_long) - df_is_long['label_long'].sum()) / max(1, df_is_long['label_long'].sum())
            scale_pos_weight_short = (len(df_is_short) - df_is_short['label_short'].sum()) / max(1, df_is_short['label_short'].sum())

            xgb_params_base = {
                'objective': 'binary:logistic',
                'max_depth': 4,
                'learning_rate': 0.05,
                'reg_alpha': 1.0,
                'reg_lambda': 3.0,
                'n_estimators': 100,
                'random_state': 42,
                'n_jobs': -1
            }
            
            xgb_params_long = xgb_params_base.copy()
            xgb_params_long['scale_pos_weight'] = scale_pos_weight_long
            xgb_params_short = xgb_params_base.copy()
            xgb_params_short['scale_pos_weight'] = scale_pos_weight_short
            
            model_long = xgb.XGBClassifier(**xgb_params_long)
            model_short = xgb.XGBClassifier(**xgb_params_short)
            
            long_ready = False
            if len(df_is_long) > 50 and df_is_long['label_long'].nunique() > 1:
                model_long.fit(df_is_long[ml_features], df_is_long['label_long'])
                long_ready = True
                
            short_ready = False
            if len(df_is_short) > 50 and df_is_short['label_short'].nunique() > 1:
                model_short.fit(df_is_short[ml_features], df_is_short['label_short'])
                short_ready = True
                
            df_oos_feat = df_oos[ml_features].ffill().fillna(0)
            
            preds_long = model_long.predict_proba(df_oos_feat)[:, 1] if long_ready else np.zeros(len(df_oos))
            preds_short = model_short.predict_proba(df_oos_feat)[:, 1] if short_ready else np.zeros(len(df_oos))
            
            # Dynamic Percentile Thresholding (75th percentile) calculated on IS data to avoid OOS lookahead!
            if long_ready and len(df_is_long) > 0:
                is_preds_long = model_long.predict_proba(df_is_long[ml_features])[:, 1]
                long_thresh = np.percentile(is_preds_long, 75)
            else:
                long_thresh = 0.5
                
            if short_ready and len(df_is_short) > 0:
                is_preds_short = model_short.predict_proba(df_is_short[ml_features])[:, 1]
                short_thresh = np.percentile(is_preds_short, 75)
            else:
                short_thresh = 0.5
            
            # Avoid extreme low thresholds if model is completely unconfident
            long_thresh = max(long_thresh, 0.1)
            short_thresh = max(short_thresh, 0.1)
            
            pred_l_bool = preds_long >= long_thresh
            pred_s_bool = preds_short >= short_thresh
            
            def ml_filter(idx: int, side: str) -> bool:
                if side == 'LONG': return pred_l_bool[idx]
                if side == 'SHORT': return pred_s_bool[idx]
                return False
                
            res = sim.run(df_oos, training_mode=False, filter_func=ml_filter)
            
            roi = res.get("roi_pct", 0)
            max_dd = res.get("max_dd_pct", 0)
            win_rate = res.get("win_rate_pct", 0)
            trades = res.get("trades", 0)
            
            is_pass = (roi > 20.0) and (max_dd < 12.0) and (win_rate > 40.0) and (trades >= 6)
            if is_pass:
                passes += 1
                
            sim_results.append({
                "window": w_name,
                "roi": float(roi),
                "max_dd": float(max_dd),
                "win_rate": float(win_rate),
                "trades": int(trades),
                "pass": bool(is_pass)
            })
            
            print(f"  [{w_name}] ROI: {roi:.2f}% | MaxDD: {max_dd:.2f}% | WR: {win_rate:.1f}% | Trades: {trades} | Pass: {is_pass}")
            
        print(f"{sim_name} passed {passes}/20 windows.")
        report[sim_name] = {
            "passes": passes,
            "windows": sim_results
        }
        
    out_file = base_dir / f"{asset}_optimization_report.json"
    with open(out_file, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"\nOptimization complete. Report saved to {out_file.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", type=str, required=True, help="Asset ticker (e.g. ETH)")
    args = parser.parse_args()
    
    run_optimization(args.asset.upper())
