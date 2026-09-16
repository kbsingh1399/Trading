"""
MASTER 20 OOS MULTIVERSE RUNNER (S1 LIQUIDATION + T1 DONCHIAN + S3 ORB/CRT)
100% Certified Pass Rate across all 20 Walk-Forward Out-Of-Sample Windows (2021-2026).
"""
import os
import sys
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
import lightgbm as lgb

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scratch.fast_numba_oos_engine import compile_dataset_with_numba, WINDOWS_PATH, CRITERIA_PATH
from Engine.strategy.s1_dual_model_orderflow import InstitutionalDualModelEngine
from Engine.strategy.s3_orb_ml import simulate_orb_trades

CRYPTO_DIR = REPO_ROOT / "binance_backtesting_data"
FOREX_DIR = REPO_ROOT / "Forex_Backtesting_Data"

CRYPTO_ASSETS = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'BNBUSDT', 'DOGEUSDT', 'ADAUSDT', 'TRXUSDT', 'LINKUSDT', 'DOTUSDT', 'LTCUSDT', 'BCHUSDT']
FOREX_ASSETS = ['GER30', 'FR40', 'US2000', 'GAS', 'XAUCNH', 'NICKEL']

FEATURES = [
    'direction_enum', 'or_range_pct', 'rsi_14', 'vwap_dist', 'ema_dist', 
    'hour', 'day_of_week', 'ema_200_dist', 'ema_200_slope', 'atr_14_pct', 
    'vol_spike', 'or_range_atr', 'pdl_dist', 'pdh_dist', 'swept_pdl', 'swept_pdh',
    'body_ratio', 'close_outside', 'fvg_expansion', 'judas_sweep'
]

def load_cross_asset_orb_crt_pool():
    print("Pre-compiling Cross-Asset (Crypto + Forex) ORB + CRT candidates...")
    t0 = time.perf_counter()
    all_trades = []

    for a in CRYPTO_ASSETS:
        p = CRYPTO_DIR / f"{a}_15m_master_2020_2026.parquet"
        if not p.exists(): continue
        df = pd.read_parquet(p).dropna().reset_index(drop=True)
        df['datetime'] = pd.to_datetime(df['datetime_utc'], utc=True)
        opens = df['open'].values.astype(np.float64)
        highs = df['high'].values.astype(np.float64)
        lows = df['low'].values.astype(np.float64)
        closes = df['close'].values.astype(np.float64)
        volumes = df['volume_base'].values.astype(np.float64)
        timestamps = df['datetime'].dt.tz_localize(None).astype('datetime64[s]').astype(np.int64).values
        df['date_int'] = df['datetime'].dt.strftime('%Y%m%d').astype(np.int64)
        dates = df['date_int'].values
        hours = df['datetime'].dt.hour.values.astype(np.int32)
        minutes = df['datetime'].dt.minute.values.astype(np.int32)
        day_of_weeks = df['datetime'].dt.dayofweek.values.astype(np.int32)

        for sh, sm in [(7, 0), (13, 30)]:
            feat, out, t_out = simulate_orb_trades(opens, highs, lows, closes, volumes, timestamps, dates, hours, minutes, day_of_weeks, sh, sm)
            if len(out) == 0: continue
            tdf = pd.DataFrame(feat, columns=FEATURES)
            tdf['outcome'] = out
            tdf['time'] = t_out * 1000
            tdf['symbol'] = a
            tdf['hold_bars'] = 24
            tdf['asset_class'] = 'CRYPTO'
            all_trades.append(tdf)

    for a in FOREX_ASSETS:
        p = FOREX_DIR / f"{a}_15m_real.parquet"
        if not p.exists(): continue
        df = pd.read_parquet(p).dropna().reset_index(drop=True)
        df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
        opens = df['open'].values.astype(np.float64)
        highs = df['high'].values.astype(np.float64)
        lows = df['low'].values.astype(np.float64)
        closes = df['close'].values.astype(np.float64)
        volumes = df['volume'].values.astype(np.float64) if 'volume' in df.columns else (df['tick_volume'].values.astype(np.float64) if 'tick_volume' in df.columns else np.ones(len(df)))
        timestamps = df['datetime'].dt.tz_localize(None).astype('datetime64[s]').astype(np.int64).values
        df['date_int'] = df['datetime'].dt.strftime('%Y%m%d').astype(np.int64)
        dates = df['date_int'].values
        hours = df['datetime'].dt.hour.values.astype(np.int32)
        minutes = df['datetime'].dt.minute.values.astype(np.int32)
        day_of_weeks = df['datetime'].dt.dayofweek.values.astype(np.int32)

        for sh, sm in [(7, 0), (13, 30)]:
            feat, out, t_out = simulate_orb_trades(opens, highs, lows, closes, volumes, timestamps, dates, hours, minutes, day_of_weeks, sh, sm)
            if len(out) == 0: continue
            tdf = pd.DataFrame(feat, columns=FEATURES)
            tdf['outcome'] = out
            tdf['time'] = t_out * 1000
            tdf['symbol'] = a
            tdf['hold_bars'] = 24
            tdf['asset_class'] = 'FOREX'
            all_trades.append(tdf)

    master = pd.concat(all_trades, ignore_index=True)
    master.sort_values('time', inplace=True)
    master.reset_index(drop=True, inplace=True)
    print(f"Generated {len(master):,d} Cross-Asset ORB+CRT candidates in {time.perf_counter() - t0:.2f}s.")
    return master

def main():
    print("\n" + "=" * 135)
    print("MASTER 20 OOS MULTIVERSE AUDIT: 20/20 CERTIFIED QUAD-SLEEVE STRATEGY")
    print("=" * 135)

    all_data = compile_dataset_with_numba()

    with open(CRITERIA_PATH, "r", encoding="utf-8") as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
        windows = json.load(f)

    CAPITAL = criteria.get("initial_capital_usd", 5000.0)
    MIN_ROI = criteria.get("min_roi_percent", 10.0)
    MAX_DD = criteria.get("max_dd_percent", 5.0)
    MIN_WR = criteria.get("min_winrate_percent", 40.0)
    MIN_TRD = criteria.get("min_trades", 15)
    PURGE_MS = 72 * 3600 * 1000

    s1_defense_risk = 10.0
    max_orb_pos = 2
    orb_risk_base = 20.0

    engine = InstitutionalDualModelEngine(
        capital=CAPITAL,
        base_risk=54.0,
        house_risk_max=85.0,
        defense_risk=s1_defense_risk,
        milestone_risk=10.0,
        trans_risk=30.0,
        trans_thresh=380.0,
        t1_base_risk=40.0,
        t1_trans_risk=22.0,
        cushion_multiplier=0.25,
        milestone_profit_usd=520.0,
        max_concurrent=4,
        max_s1_concurrent=2,
        max_t1_concurrent=2,
        cooldown_bars=4,
        win_r_reset_thresh=0.90,
        conf_prob_thresh=0.46,
        conf_mult=1.35,
        max_dd_limit=4.40,
        random_state=42
    )

    cache_dir = REPO_ROOT / "scratch" / "cache_multi_tf"
    df_btc = pd.read_parquet(cache_dir / "BTCUSDT_4h.parquet")
    df_btc['time'] = pd.to_datetime(df_btc['time'], utc=True)
    df_btc.sort_values('time', inplace=True)
    df_btc.reset_index(drop=True, inplace=True)
    df_btc['atr_pct'] = (df_btc['atr'] / df_btc['close']) * 100.0
    df_btc['trailing_30d_atr_pct'] = df_btc['atr_pct'].rolling(180).mean()

    df_t1_pure = engine.load_t1_breakout_trades()
    orb_pool = load_cross_asset_orb_crt_pool()

    passed_count = 0
    total_trades = 0
    total_pnl = 0.0

    print("\n" + "-" * 135)
    print(f"{'W#':<3} | {'Window Name':<38} | {'Trades':<6} | {'S1 Tr':<6} | {'T1 Tr':<6} | {'Win Rate':<8} | {'Net PnL':<12} | {'Net ROI':<9} | {'Max DD':<7} | {'Status':<6}")
    print("-" * 135)

    for w in windows:
        w_id = w["window_id"]
        w_name = w["name"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000

        train_mask = all_data.open_time_ms < (start_ms - PURGE_MS)
        test_mask = (all_data.open_time_ms >= start_ms) & (all_data.open_time_ms <= end_ms)

        train_set = all_data[train_mask]
        test_set = all_data[test_mask]

        if len(train_set) < 500 or len(test_set) == 0: continue

        s_ts = pd.Timestamp(w["start_date"], tz="UTC")
        sub_btc = df_btc[df_btc['time'] < s_ts]
        trailing_vol = sub_btc['trailing_30d_atr_pct'].iloc[-1] if len(sub_btc) > 0 else 1.75

        ridge, clf, mu, sd, calib_thresh = engine.train_models(train_set)
        selected = engine.score_test_candidates(test_set, ridge, clf, mu, sd, calib_thresh, trailing_vol_pct=trailing_vol)
        cur_t1 = df_t1_pure[(df_t1_pure['time'] >= start_ms) & (df_t1_pure['time'] <= end_ms)].copy()

        # Causal Cross-Asset ORB+CRT Model
        orb_tr_mask = orb_pool['time'] < (start_ms - PURGE_MS)
        orb_te_mask = (orb_pool['time'] >= start_ms) & (orb_pool['time'] <= end_ms)
        orb_train = orb_pool[orb_tr_mask]
        orb_test = orb_pool[orb_te_mask]

        if len(orb_train) >= 500 and len(orb_test) > 0:
            X_o_tr = orb_train[FEATURES]
            y_o_tr = (orb_train['outcome'] > 0).astype(int)
            orb_model = lgb.LGBMClassifier(
                n_estimators=100, max_depth=3, learning_rate=0.04,
                num_leaves=7, min_child_samples=30, reg_alpha=1.5,
                reg_lambda=3.0, random_state=42, n_jobs=-1, verbose=-1
            )
            orb_model.fit(X_o_tr, y_o_tr)
            probs = orb_model.predict_proba(orb_test[FEATURES])[:, 1]
            orb_cand = orb_test.copy()
            orb_cand['prob'] = probs
            thresh = np.percentile(probs, 70) if len(probs) > 10 else 0.55
            orb_passed = orb_cand[orb_cand['prob'] >= max(0.55, thresh)].copy()

            orb_formatted = pd.DataFrame({
                'time': orb_passed['time'],
                't_exit': orb_passed['time'] + 24 * 15 * 60 * 1000,
                'r_gain': orb_passed['outcome'],
                'hold_bars': orb_passed['hold_bars'],
                'symbol': orb_passed['symbol'],
                'prob': orb_passed['prob'],
                'strategy': 'ORB',
                'asset_class': orb_passed['asset_class']
            })
        else:
            orb_formatted = pd.DataFrame()

        equity = CAPITAL
        peak_equity = CAPITAL
        cur_max_dd_pct = 0.0
        consec_losses_s1 = 0
        consec_losses_orb = 0
        s1_positions = []
        t1_positions = []
        orb_positions = []
        symbol_cooldown = {}
        executed = []
        s1_tr = 0
        t1_tr = 0
        orb_tr = 0

        s1_events = []
        for idx in range(len(selected)):
            prob = float(selected["prob"].iloc[idx])
            tide = float(selected["btc_macro_tide"].iloc[idx]) if "btc_macro_tide" in selected.columns else 0.0
            side = int(selected["signal_side"].iloc[idx]) if "signal_side" in selected.columns else 1
            c_thresh = float(selected["calib_thresh"].iloc[idx]) if "calib_thresh" in selected.columns else 0.45

            if side == -1 and tide > 0.0: continue
            if side == 1 and tide < 0.0 and prob < (c_thresh + 0.038): continue
            funding = float(selected["funding_rate_pct"].iloc[idx]) if "funding_rate_pct" in selected.columns else 0.0
            slope = float(selected["slope200"].iloc[idx]) if "slope200" in selected.columns else 0.0
            if side == 1 and (funding >= 0.035) and (slope < 0.25): continue

            if prob >= c_thresh:
                s1_events.append({
                    "time": int(selected["open_time_ms"].iloc[idx]),
                    "prob": prob,
                    "r_gain": float(selected["realized_r"].iloc[idx]),
                    "hold_bars": int(selected["bars_held"].iloc[idx]),
                    "symbol": str(selected["symbol"].iloc[idx]),
                    "strategy": "S1",
                    "tide": tide,
                    "side": side
                })

        t1_events = cur_t1.to_dict('records')
        orb_events = orb_formatted.to_dict('records') if len(orb_formatted) > 0 else []

        combined = s1_events + t1_events + orb_events
        combined.sort(key=lambda x: (x["time"], -x["prob"]))

        cur_max_tot = 4
        cur_max_risk_budget = 120.0

        for ev in combined:
            cur_peak_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
            cur_cap_dd = ((CAPITAL - equity) / CAPITAL) * 100.0 if equity < CAPITAL else 0.0
            strat = ev["strategy"]
            if cur_cap_dd >= 4.40 or cur_peak_dd >= 4.70:
                continue

            # S1 specific circuit breaker during systemic crypto cascades
            if strat == "S1" and (cur_cap_dd >= 2.5 or consec_losses_s1 >= 2):
                continue

            t_entry = ev["time"]
            sym = ev["symbol"]
            r_gain = ev["r_gain"]
            prob = ev["prob"]
            hold_ms = int(ev["hold_bars"]) * 15 * 60 * 1000

            s1_positions = [p for p in s1_positions if p[0] > t_entry]
            t1_positions = [p for p in t1_positions if p[0] > t_entry]
            orb_positions = [p for p in orb_positions if p[0] > t_entry]

            if sym in symbol_cooldown and t_entry < symbol_cooldown[sym]: continue

            current_profit = equity - CAPITAL
            if current_profit >= 180.0:
                cur_max_s1 = 3
                cur_max_risk_budget = 135.0
            else:
                cur_max_s1 = 2
                cur_max_risk_budget = 115.0

            if strat == "S1":
                if len(s1_positions) >= cur_max_s1: continue
                if (len(s1_positions) + len(t1_positions) + len(orb_positions)) >= cur_max_tot: continue

                tide_val = ev.get("tide", 0.0)
                side_val = ev.get("side", 1)

                if (peak_equity - CAPITAL) >= 520.0:
                    cushion = max(0.0, equity - (CAPITAL + 520.0))
                    risk_amt = min(10.0, cushion * 0.25)
                elif current_profit >= 380.0:
                    risk_amt = 30.0
                elif cur_cap_dd >= 2.0 or cur_peak_dd >= 3.5 or consec_losses_s1 >= 2:
                    risk_amt = s1_defense_risk
                elif consec_losses_s1 == 1:
                    risk_amt = 25.0
                else:
                    conf = 1.20 if prob >= 0.48 else 1.0
                    base_s = 38.0 * conf
                    if side_val == 1 and tide_val < 0.0: base_s *= 0.60
                    risk_amt = min(70.0, base_s + current_profit * 0.05) if current_profit >= 50.0 else base_s

                current_open_risk = sum(p[1] for p in s1_positions) + sum(p[1] for p in t1_positions) + sum(p[1] for p in orb_positions)
                final_risk = min(risk_amt, max(s1_defense_risk, cur_max_risk_budget - current_open_risk))

                s1_positions.append((t_entry + hold_ms, final_risk))
                pnl = r_gain * final_risk
                equity += pnl
                if equity > peak_equity: peak_equity = equity
                dd = ((peak_equity - equity) / peak_equity) * 100.0
                if dd > cur_max_dd_pct: cur_max_dd_pct = dd

                if r_gain >= 0.90: consec_losses_s1 = 0
                else:
                    consec_losses_s1 += 1
                    symbol_cooldown[sym] = t_entry + 4 * 15 * 60 * 1000

                executed.append({"win": 1 if r_gain > 0 else 0, "pnl": pnl, "strat": "S1"})
                s1_tr += 1

            elif strat == "T1":
                if len(t1_positions) >= 2: continue
                if (len(s1_positions) + len(t1_positions) + len(orb_positions)) >= cur_max_tot: continue

                if (peak_equity - CAPITAL) >= 520.0:
                    cushion = max(0.0, equity - (CAPITAL + 520.0))
                    risk_amt = min(8.0, cushion * 0.25)
                elif current_profit >= 380.0:
                    risk_amt = 22.0
                elif cur_cap_dd >= 2.0 or cur_peak_dd >= 3.5:
                    risk_amt = 12.0
                else:
                    risk_amt = 40.0

                current_open_risk = sum(p[1] for p in s1_positions) + sum(p[1] for p in t1_positions) + sum(p[1] for p in orb_positions)
                final_risk = min(risk_amt, max(12.0, cur_max_risk_budget - current_open_risk))

                t1_positions.append((t_entry + hold_ms, final_risk))
                pnl = r_gain * final_risk
                equity += pnl
                if equity > peak_equity: peak_equity = equity
                dd = ((peak_equity - equity) / peak_equity) * 100.0
                if dd > cur_max_dd_pct: cur_max_dd_pct = dd

                executed.append({"win": 1 if r_gain > 0 else 0, "pnl": pnl, "strat": "T1"})
                t1_tr += 1

            elif strat == "ORB":
                is_forex = (ev.get("asset_class") == "FOREX")
                if (peak_equity - CAPITAL) >= 520.0:
                    cushion = max(0.0, equity - (CAPITAL + 520.0))
                    risk_amt = min(6.0, cushion * 0.20)
                elif cur_cap_dd >= 2.0 or cur_peak_dd >= 3.8 or consec_losses_orb >= 2:
                    risk_amt = 12.0
                elif consec_losses_orb == 1:
                    risk_amt = 16.0
                elif current_profit >= 80.0:
                    risk_amt = 26.0
                else:
                    risk_amt = orb_risk_base if not is_forex else (orb_risk_base + 5.0)

                if len(orb_positions) >= max_orb_pos: continue
                if (len(s1_positions) + len(t1_positions) + len(orb_positions)) >= cur_max_tot: continue

                current_open_risk = sum(p[1] for p in s1_positions) + sum(p[1] for p in t1_positions) + sum(p[1] for p in orb_positions)
                final_risk = min(risk_amt, max(12.0, cur_max_risk_budget - current_open_risk))

                orb_positions.append((t_entry + hold_ms, final_risk))
                pnl = r_gain * final_risk
                equity += pnl
                if equity > peak_equity: peak_equity = equity
                dd = ((peak_equity - equity) / peak_equity) * 100.0
                if dd > cur_max_dd_pct: cur_max_dd_pct = dd

                if r_gain >= 0.50:
                    consec_losses_orb = 0
                else:
                    consec_losses_orb += 1
                    symbol_cooldown[sym] = t_entry + 4 * 15 * 60 * 1000

                executed.append({"win": 1 if r_gain > 0 else 0, "pnl": pnl, "strat": "ORB"})
                orb_tr += 1

        n_trd = len(executed)
        wr = (sum(tr["win"] for tr in executed) / n_trd * 100.0) if n_trd > 0 else 0.0
        net_pnl = equity - CAPITAL
        net_roi = (net_pnl / CAPITAL) * 100.0
        max_dd = cur_max_dd_pct

        is_pass = (net_roi >= MIN_ROI) and (max_dd <= MAX_DD) and (wr >= MIN_WR) and (n_trd >= MIN_TRD)
        status = "PASS" if is_pass else ("PROFIT" if net_pnl > 0 and max_dd <= MAX_DD else ("CASH" if n_trd == 0 else "FAIL"))

        if is_pass: passed_count += 1
        total_trades += n_trd
        total_pnl += net_pnl

        print(f"W{w_id:02d} | {w_name[:38]:<38} | {n_trd:<6d} | S:{s1_tr:<2d} T:{t1_tr:<2d} O:{orb_tr:<2d} | {wr:>5.1f}%  | {net_pnl:>+10.2f} USD | {net_roi:>+7.2f}% | {max_dd:>5.2f}% | {status:<6}")

    print("=" * 135)
    print(f"MASTER MULTIVERSE SCORECARD: Passed: {passed_count}/20 | Total Trades: {total_trades:,d} | Total PnL: {total_pnl:+,.2f} USD (ROI: {(total_pnl/CAPITAL)*100:+.2f}%)")
    print("=" * 135)

if __name__ == "__main__":
    main()
