"""
Production 23-Quarter OOS Altcoin-Only ML Suite with Causal BTC Macro Gating
=============================================================================
Universe: 10 Institutional Altcoins (ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH)
Benchmark / Reference: BTCUSDT (Macro Tide, Trend, Volatility Regime - 0 trades on BTC)
Indicators: Canonical KRI (96-period), Spot CVD Divergence, VWAP Z-scores, Liquidation Z-scores
ML Models: Causal Ridge + Regularized LightGBM Ensemble with 72h Quarantine Purge
Execution: 100% Causal: Next-Bar Open Fills (opens[j+1]), Adverse Stop Loss First, 41 bps Drag
Evaluation: All 23 Walk-Forward OOS Quarterly Windows (2021-2026)
"""
import json
import time
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.linear_model import LogisticRegression

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from Engine.core.fast_numba_oos_engine import (
    compile_dataset_with_numba, WINDOWS_PATH, CRITERIA_PATH, CAPITAL, FEATURE_COLS
)
from Engine.core.canonical_indicators import compute_kairi_relative_index
from Engine.strategy.s1_dual_model_orderflow import InstitutionalDualModelEngine
from Engine.strategy.s3_orb_ml import simulate_orb_trades
from Engine.core.multi_tf_data import get_or_compute_4h_dataframe

ALTCOIN_SYMBOLS = [
    "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT", "ADAUSDT",
    "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT"
]

DATA_DIR = REPO_ROOT / "binance_backtesting_data"
if not DATA_DIR.exists():
    DATA_DIR = REPO_ROOT / "Engine" / "binance_backtesting_data"

def load_altcoin_orb_pool():
    all_trades = []
    for a in ALTCOIN_SYMBOLS:
        p = DATA_DIR / f"{a}_15m_master_2020_2026.parquet"
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
            tdf = pd.DataFrame(feat, columns=[
                'direction_enum', 'or_range_pct', 'rsi_14', 'vwap_dist', 'ema_dist', 
                'hour', 'day_of_week', 'ema_200_dist', 'ema_200_slope', 'atr_14_pct', 
                'vol_spike', 'or_range_atr', 'pdl_dist', 'pdh_dist', 'swept_pdl', 'swept_pdh',
                'body_ratio', 'close_outside', 'fvg_expansion', 'judas_sweep'
            ])
            tdf['outcome'] = out
            tdf['time'] = t_out * 1000
            tdf['symbol'] = a
            tdf['hold_bars'] = 24
            all_trades.append(tdf)

    master = pd.concat(all_trades, ignore_index=True)
    master.sort_values('time', inplace=True)
    master.reset_index(drop=True, inplace=True)
    return master

def main():
    print("=" * 140)
    print("PRODUCTION 23-QUARTER OOS ALTCOIN-ONLY ML SUITE (BTC AS REFERENCE ONLY)")
    print("=" * 140)

    all_data = compile_dataset_with_numba()
    alt_mask = all_data["symbol"].isin(ALTCOIN_SYMBOLS)
    alt_data = all_data[alt_mask].copy().reset_index(drop=True)

    # Vectorize KRI for Altcoins
    print("Vectorizing Kairi Relative Index (96-period) across Altcoins...")
    t0_kri = time.perf_counter()
    kri_dict = {}
    for sym in ALTCOIN_SYMBOLS:
        p = DATA_DIR / f"{sym}_15m_master_2020_2026.parquet"
        if p.exists():
            df_sym = pd.read_parquet(p, columns=["open_time_ms", "close"]).dropna().reset_index(drop=True)
            kri = compute_kairi_relative_index(df_sym["close"].to_numpy(float), period=96)
            s_kri = pd.Series(kri, index=df_sym["open_time_ms"].to_numpy(np.int64))
            kri_dict[sym] = s_kri

    alt_data["kri_96"] = 0.0
    for sym in ALTCOIN_SYMBOLS:
        if sym in kri_dict:
            sym_mask = alt_data["symbol"] == sym
            alt_data.loc[sym_mask, "kri_96"] = alt_data.loc[sym_mask, "open_time_ms"].map(kri_dict[sym]).fillna(0.0)
    print(f"KRI vectorized in {time.perf_counter() - t0_kri:.2f}s.")

    df_t1_all = InstitutionalDualModelEngine.load_t1_breakout_trades()
    df_t1 = df_t1_all[df_t1_all["symbol"].isin(ALTCOIN_SYMBOLS)].copy().reset_index(drop=True)
    orb_pool = load_altcoin_orb_pool()

    df_btc = get_or_compute_4h_dataframe("BTCUSDT")
    df_btc['atr_pct'] = (df_btc['atr'] / df_btc['close']) * 100.0
    df_btc['trailing_30d_atr_pct'] = df_btc['atr_pct'].rolling(180).mean()
    btc_bull = (df_btc['close'] > df_btc['ema_50']) & (df_btc['ema_50'] > df_btc['ema_200'])
    btc_bear = (df_btc['close'] < df_btc['ema_50']) & (df_btc['ema_50'] < df_btc['ema_200'])
    btc_tide_series = pd.Series(np.where(btc_bull, 1, np.where(btc_bear, -1, 0)), index=df_btc['time'].astype('int64'))

    alt_data['btc_macro_tide'] = alt_data['open_time_ms'].map(btc_tide_series).fillna(0)

    with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
        windows = json.load(f)

    PURGE_MS = 72 * 3600 * 1000

    base_risk = 34.0
    t1_risk = 40.0
    def_risk = 8.0
    dd_trigger = 1.8
    house_mult = 0.08
    min_milestone = 505.0

    passed_count = 0
    total_trades = 0
    total_pnl = 0.0
    all_equity_records = []

    print("\n" + "-" * 140)
    print(f"{'W#':<3} | {'Window Name':<38} | {'Trades':<6} | {'S1 Tr':<6} | {'T1 Tr':<6} | {'ORB Tr':<6} | {'WR':<6} | {'Net PnL':<12} | {'Net ROI':<9} | {'Max DD':<7} | {'Status':<6}")
    print("-" * 140)

    for w in windows:
        w_id = w["window_id"]
        s_ts = pd.Timestamp(w["start_date"], tz="UTC")
        start_ms = s_ts.value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000

        sub_btc = df_btc[df_btc['time'] < s_ts]
        trailing_vol = sub_btc['trailing_30d_atr_pct'].iloc[-1] if len(sub_btc) > 0 else 1.75
        btc_4h_slope = sub_btc['ema_200_slope'].iloc[-1] if len(sub_btc) > 0 else 0.0

        train_mask = alt_data.open_time_ms < (start_ms - PURGE_MS)
        test_mask = (alt_data.open_time_ms >= start_ms) & (alt_data.open_time_ms <= end_ms)

        train_set = alt_data[train_mask]
        test_set = alt_data[test_mask]

        if len(train_set) < 500 or len(test_set) == 0: continue

        X_train = train_set[FEATURE_COLS]
        y_train = train_set["label_y"].to_numpy()

        mu = X_train.mean(axis=0)
        sd = X_train.std(axis=0).replace(0, 1.0)
        X_tr_s = np.nan_to_num(((X_train - mu) / sd).clip(-5.0, 5.0).to_numpy(float), nan=0.0)

        ridge = LogisticRegression(C=0.03, max_iter=200, random_state=42)
        ridge.fit(X_tr_s, y_train)

        clf = lgb.LGBMClassifier(
            n_estimators=160, max_depth=4, num_leaves=15, learning_rate=0.04,
            subsample=0.8, colsample_bytree=0.8, reg_alpha=2.0, reg_lambda=0.5,
            random_state=42, verbose=-1, n_jobs=2
        )
        clf.fit(X_train, y_train)

        train_probs = 0.60 * ridge.predict_proba(X_tr_s)[:, 1] + 0.40 * clf.predict_proba(X_train)[:, 1]
        cands_per_month = len(train_set) / max(1.0, (train_set.open_time_ms.max() - train_set.open_time_ms.min()) / (30.4375 * 86_400_000))
        calib_q = max(0.65, min(0.96, 1.0 - (38.0 / cands_per_month)))
        calib_thresh = float(np.quantile(train_probs, calib_q))
        if trailing_vol < 0.92:
            calib_thresh -= 0.020

        X_test = test_set[FEATURE_COLS]
        X_te_s = np.nan_to_num(((X_test - mu) / sd).clip(-5.0, 5.0).to_numpy(float), nan=0.0)
        te_probs = 0.60 * ridge.predict_proba(X_te_s)[:, 1] + 0.40 * clf.predict_proba(X_test)[:, 1]

        scored_s1 = test_set.copy()
        scored_s1["prob"] = te_probs

        s1_events = []
        for idx in range(len(scored_s1)):
            prob = float(scored_s1["prob"].iloc[idx])
            tide = float(scored_s1["btc_macro_tide"].iloc[idx])
            side = int(scored_s1["signal_side"].iloc[idx])
            funding = float(scored_s1["funding_rate_pct"].iloc[idx])
            slope = float(scored_s1["slope200"].iloc[idx])
            kri_val = float(scored_s1["kri_96"].iloc[idx])

            if side == -1 and tide > 0.0: continue
            if side == -1 and slope > 0.40: continue
            if side == 1 and tide < 0.0 and kri_val > -5.5 and prob < (calib_thresh + 0.045): continue
            if side == 1 and (funding >= 0.035) and (slope < 0.25): continue

            if prob >= calib_thresh:
                s1_events.append({
                    "time": int(scored_s1["open_time_ms"].iloc[idx]),
                    "prob": prob,
                    "r_gain": float(scored_s1["realized_r"].iloc[idx]),
                    "hold_bars": int(scored_s1["bars_held"].iloc[idx]),
                    "symbol": str(scored_s1["symbol"].iloc[idx]),
                    "strategy": "S1",
                    "tide": tide,
                    "side": side
                })

        is_t1_bear_chop = (trailing_vol > 2.10 and btc_4h_slope < 0.0)
        cur_t1 = df_t1[(df_t1['time'] >= start_ms) & (df_t1['time'] <= end_ms)].copy()

        t1_events = []
        if not is_t1_bear_chop:
            t1_events = cur_t1.to_dict('records')

        orb_tr_mask = orb_pool['time'] < (start_ms - PURGE_MS)
        orb_te_mask = (orb_pool['time'] >= start_ms) & (orb_pool['time'] <= end_ms)
        orb_train = orb_pool[orb_tr_mask]
        orb_test = orb_pool[orb_te_mask]

        orb_events = []
        if len(orb_train) >= 300 and len(orb_test) > 0 and start_ms >= pd.Timestamp("2021-07-01", tz="UTC").value // 1_000_000:
            X_o_tr = orb_train[[
                'direction_enum', 'or_range_pct', 'rsi_14', 'vwap_dist', 'ema_dist', 
                'hour', 'day_of_week', 'ema_200_dist', 'ema_200_slope', 'atr_14_pct', 
                'vol_spike', 'or_range_atr', 'pdl_dist', 'pdh_dist', 'swept_pdl', 'swept_pdh',
                'body_ratio', 'close_outside', 'fvg_expansion', 'judas_sweep'
            ]]
            y_o_tr = (orb_train['outcome'] > 0).astype(int)
            orb_model = lgb.LGBMClassifier(
                n_estimators=100, max_depth=3, learning_rate=0.04,
                num_leaves=7, min_child_samples=30, reg_alpha=1.5,
                reg_lambda=3.0, random_state=42, n_jobs=-1, verbose=-1
            )
            orb_model.fit(X_o_tr, y_o_tr)
            probs_tr = orb_model.predict_proba(X_o_tr)[:, 1]
            thresh = float(np.percentile(probs_tr, 75)) if len(probs_tr) > 10 else 0.56
            probs = orb_model.predict_proba(orb_test[[
                'direction_enum', 'or_range_pct', 'rsi_14', 'vwap_dist', 'ema_dist', 
                'hour', 'day_of_week', 'ema_200_dist', 'ema_200_slope', 'atr_14_pct', 
                'vol_spike', 'or_range_atr', 'pdl_dist', 'pdh_dist', 'swept_pdl', 'swept_pdh',
                'body_ratio', 'close_outside', 'fvg_expansion', 'judas_sweep'
            ]])[:, 1]
            orb_cand = orb_test.copy()
            orb_cand['prob'] = probs
            orb_passed = orb_cand[orb_cand['prob'] >= max(0.56, thresh)].copy()

            for _, row in orb_passed.iterrows():
                orb_events.append({
                    'time': int(row['time']),
                    'r_gain': float(row['outcome']),
                    'hold_bars': int(row['hold_bars']),
                    'symbol': str(row['symbol']),
                    'prob': float(row['prob']),
                    'strategy': 'ORB'
                })

        combined = s1_events + t1_events + orb_events
        combined.sort(key=lambda x: (x["time"], -x["prob"]))

        equity = CAPITAL
        peak_equity = CAPITAL
        cur_max_dd_pct = 0.0
        consec_losses_s1 = 0
        s1_positions = []
        t1_positions = []
        orb_positions = []
        symbol_cooldown = {}
        executed = []
        s1_tr = 0
        t1_tr = 0
        orb_tr = 0

        for ev in combined:
            cur_peak_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
            cur_cap_dd = ((CAPITAL - equity) / CAPITAL) * 100.0 if equity < CAPITAL else 0.0
            strat = ev["strategy"]
            if cur_cap_dd >= 4.40 or cur_peak_dd >= 4.70:
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
            if (len(s1_positions) + len(t1_positions) + len(orb_positions)) >= 4: continue

            if (peak_equity - CAPITAL) >= min_milestone:
                cushion = max(0.0, equity - (CAPITAL + min_milestone))
                risk_amt = min(6.0, max(2.0, cushion * 0.15))
            elif cur_cap_dd >= dd_trigger or cur_peak_dd >= (dd_trigger + 1.2):
                risk_amt = def_risk
            elif current_profit >= 50.0:
                risk_amt = min(75.0, base_risk + current_profit * house_mult)
            else:
                conf = 1.20 if prob >= 0.48 else 1.0
                risk_amt = base_risk * conf

            if strat == "S1":
                if len(s1_positions) >= 2: continue
                if consec_losses_s1 >= 2 and (cur_cap_dd >= 1.0 or cur_peak_dd >= 2.0):
                    risk_amt = def_risk

                s1_positions.append((t_entry + hold_ms, risk_amt))
                pnl = r_gain * risk_amt
                equity += pnl
                if equity > peak_equity: peak_equity = equity
                dd = ((peak_equity - equity) / peak_equity) * 100.0
                if dd > cur_max_dd_pct: cur_max_dd_pct = dd

                if r_gain >= 0.80: consec_losses_s1 = 0
                else:
                    consec_losses_s1 += 1
                    symbol_cooldown[sym] = t_entry + 4 * 15 * 60 * 1000

                executed.append({"win": 1 if r_gain > 0 else 0, "pnl": pnl, "strat": "S1", "time": t_entry, "equity": equity})
                s1_tr += 1

            elif strat == "T1":
                if len(t1_positions) >= 2: continue
                t1_r = t1_risk if (cur_cap_dd < dd_trigger and cur_peak_dd < (dd_trigger + 1.2)) else def_risk
                if (peak_equity - CAPITAL) >= min_milestone:
                    t1_r = min(6.0, max(2.0, cushion * 0.15))
                elif current_profit >= 50.0:
                    t1_r = min(75.0, t1_risk + current_profit * house_mult)

                t1_positions.append((t_entry + hold_ms, t1_r))
                pnl = r_gain * t1_r
                equity += pnl
                if equity > peak_equity: peak_equity = equity
                dd = ((peak_equity - equity) / peak_equity) * 100.0
                if dd > cur_max_dd_pct: cur_max_dd_pct = dd

                executed.append({"win": 1 if r_gain > 0 else 0, "pnl": pnl, "strat": "T1", "time": t_entry, "equity": equity})
                t1_tr += 1

            elif strat == "ORB":
                if len(orb_positions) >= 2: continue
                orb_r = 16.0 if (cur_cap_dd < dd_trigger and cur_peak_dd < (dd_trigger + 1.2)) else def_risk
                if (peak_equity - CAPITAL) >= min_milestone:
                    orb_r = min(4.0, max(1.5, cushion * 0.15))

                orb_positions.append((t_entry + hold_ms, orb_r))
                pnl = r_gain * orb_r
                equity += pnl
                if equity > peak_equity: peak_equity = equity
                dd = ((peak_equity - equity) / peak_equity) * 100.0
                if dd > cur_max_dd_pct: cur_max_dd_pct = dd

                if r_gain < 0.50:
                    symbol_cooldown[sym] = t_entry + 4 * 15 * 60 * 1000

                executed.append({"win": 1 if r_gain > 0 else 0, "pnl": pnl, "strat": "ORB", "time": t_entry, "equity": equity})
                orb_tr += 1

        n_trd = len(executed)
        wr = (sum(tr["win"] for tr in executed) / n_trd * 100.0) if n_trd > 0 else 0.0
        net_pnl = equity - CAPITAL
        net_roi = (net_pnl / CAPITAL) * 100.0
        max_dd = cur_max_dd_pct

        is_pass = (net_roi >= 10.0) and (max_dd <= 5.0) and (wr >= 40.0) and (n_trd >= 15)
        status = "PASS" if is_pass else ("PROFIT" if net_pnl > 0 and max_dd <= 5.0 else ("CASH" if n_trd == 0 else "FAIL"))

        if is_pass: passed_count += 1
        total_trades += n_trd
        total_pnl += net_pnl
        all_equity_records.extend(executed)

        print(f"W{w_id:02d} | {w['name'][:38]:<38} | {n_trd:<6d} | S:{s1_tr:<2d}   | T:{t1_tr:<2d}   | O:{orb_tr:<2d}    | {wr:>5.1f}% | {net_pnl:>+10.2f} USD | {net_roi:>+7.2f}% | {max_dd:>5.2f}% | {status:<6}")

    print("=" * 140)
    print(f"PRODUCTION ALTCOIN SCORECARD: Passed: {passed_count}/{len(windows)} | Total Trades: {total_trades:,d} | Total Net PnL: {total_pnl:+,.2f} USD (ROI: {(total_pnl/CAPITAL)*100:+.2f}%)")
    print("=" * 140)

    # Save trades to parquet for benchmarking & plotting
    if len(all_equity_records) > 0:
        df_exec = pd.DataFrame(all_equity_records)
        df_exec.to_parquet(REPO_ROOT / "reports" / "altcoin_suite_executed_trades.parquet")

if __name__ == "__main__":
    main()
