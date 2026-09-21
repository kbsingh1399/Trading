"""Elite Quant 23 OOS Regime-Routed Suite.
Combining: S1 Liquidity Pullbacks + T1 Donchian Breakout + S3 Crypto ORB/CRT.
Dynamic Risk Scaling: base 36 / DD-defense min(base*0.40, 14) / house min(base*1.35, 48) /
milestone cushion*0.20 / 4.85% DD stop.
OX59: universal 3-stage ratchets (0.80->+0.20 / 1.50->+0.80 / 2.00->+1.50) + 24-bar decay;
regime sizing (S1 halved in chop); DD contraction x0.5 at 1.80%; max 3 concurrent;
1 position/asset; max 1 HB-alt long in BTC 4H breakdown; bear ORB-long zc>1.2 gate.
"""
import json
from pathlib import Path
import sys
import time
import numpy as np
import pandas as pd
import numba as nb
from numba import njit
import lightgbm as lgb

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from Engine.core.canonical_indicators import (
    compute_kairi_zscore,
    compute_bollinger_bandwidth_zscore,
    compute_adx_series
)
from Engine.core.fast_numba_oos_engine import (
    compile_dataset_with_numba, WINDOWS_PATH, CRITERIA_PATH, FEATURE_COLS, CAPITAL,
    MIN_ROI, MAX_DD, MIN_WR, MIN_TRADES, DATA_DIR, CORE_SYMBOLS
)
from Engine.strategy.s1_liquidation_orderflow.s1_dual_model_orderflow import InstitutionalDualModelEngine
from Engine.runners.run_20_oos_multiverse import load_cross_asset_orb_crt_pool, FEATURES as ORB_FEATURES

@njit(fastmath=True)
def simulate_elite_portfolio(
    event_times: np.ndarray,
    event_r_gains: np.ndarray,
    event_risks: np.ndarray,
    event_hold_ms: np.ndarray,
    event_sleeve_ids: np.ndarray,  # 1=S1, 2=T1, 3=ORB
    event_syms: np.ndarray,      # OX59: factorized symbol id (0=BTCUSDT)
    event_sides: np.ndarray,     # OX59: +1 long / -1 short
    event_hb: np.ndarray,        # OX59: 1 if high-beta-alt long (non-BTC, side=+1)
    event_btcbd: np.ndarray,     # OX59: 1 if BTC in 4H breakdown at event time
    regime_id: int = 0,          # OX59: 0=SIDEWAYS_CHOP, 1=BULL_EXPANSION, 2=BEAR_CONTAGION
    capital: float = 5000.0,
    max_concurrent: int = 3,
    max_s1_concurrent: int = 2,
    max_t1_concurrent: int = 2,
    max_orb_concurrent: int = 2,
    milestone_pnl: float = 500.0,
    dd_stop_pct: float = 4.85
):
    n = len(event_times)
    equity = capital
    peak_equity = capital
    max_dd_pct = 0.0
    
    pos_end_times = np.zeros(max_concurrent, dtype=np.int64)
    pos_sleeves = np.zeros(max_concurrent, dtype=np.int8)
    pos_active = np.zeros(max_concurrent, dtype=np.bool_)
    pos_syms = np.zeros(max_concurrent, dtype=np.int64)   # OX59: 1 position/asset
    pos_hb = np.zeros(max_concurrent, dtype=np.int8)      # OX59: hb-alt-long flag
    
    trade_pnls = np.zeros(n, dtype=np.float64)
    trade_times = np.zeros(n, dtype=np.int64)
    trade_sleeves = np.zeros(n, dtype=np.int8)
    trade_evidx = np.zeros(n, dtype=np.int64)  # OX59 tracing (no economic effect)
    
    tr_count = 0
    win_count = 0
    s1_tr = 0
    t1_tr = 0
    orb_tr = 0
    locked = False

    for i in range(n):
        t = event_times[i]
        r = event_r_gains[i]
        base_r = event_risks[i]
        hold = event_hold_ms[i]
        slv = event_sleeve_ids[i]
        sym = event_syms[i]
        hb = event_hb[i]
        btcbd = event_btcbd[i]

        # Release closed positions
        for p in range(max_concurrent):
            if pos_active[p] and pos_end_times[p] <= t:
                pos_active[p] = False

        if locked or max_dd_pct >= dd_stop_pct:
            continue

        # Count active positions per sleeve
        s1_active = 0
        t1_active = 0
        orb_active = 0
        hb_active = 0
        active_count = 0
        slot = -1
        sym_already = False

        for p in range(max_concurrent):
            if pos_active[p]:
                active_count += 1
                if pos_sleeves[p] == 1: s1_active += 1
                elif pos_sleeves[p] == 2: t1_active += 1
                elif pos_sleeves[p] == 3: orb_active += 1
                if pos_hb[p] == 1: hb_active += 1
                if pos_syms[p] == sym: sym_already = True
            elif slot == -1:
                slot = p

        if active_count >= max_concurrent or slot == -1:
            continue

        # Concurrency limits
        if slv == 1 and s1_active >= max_s1_concurrent: continue
        if slv == 2 and t1_active >= max_t1_concurrent: continue
        if slv == 3 and orb_active >= max_orb_concurrent: continue

        # OX59 cluster filter: max 1 position per asset
        if sym_already: continue
        # OX59 cluster filter: max 1 high-beta alt long in BTC breakdown
        if hb == 1 and btcbd == 1 and hb_active >= 1: continue

        # Milestone lock
        if (peak_equity - capital) >= milestone_pnl and tr_count >= 15:
            floor_stop = max(capital + milestone_pnl, peak_equity - 120.0)
            if equity <= floor_stop:
                locked = True
                continue

        # Dynamic Institutional Risk Budgeting (Quant-Developers-Resources / Risk Management)
        cur_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
        cur_profit = equity - capital

        # OX59 regime sizing: halve S1 pullback risk in SIDEWAYS_CHOP (prioritizes ORB/T1 relatively)
        if regime_id == 0 and slv == 1:
            base_r = base_r * 0.5

        is_milestone = (peak_equity - capital) >= milestone_pnl
        if is_milestone:
            cushion = max(0.0, equity - (capital + milestone_pnl))
            trade_risk = min(10.0, cushion * 0.20)
            if trade_risk <= 0.0:
                locked = True
                continue
        elif cur_dd >= 2.0 or cur_profit < -50.0:
            trade_risk = min(base_r * 0.40, 14.0)
        elif cur_profit >= 120.0:
            trade_risk = min(base_r * 1.35, 48.0)
        else:
            trade_risk = min(base_r, 36.0)

        # OX59 DD contraction: halve non-milestone risk once intra-window DD >= 1.80%
        if (not is_milestone) and max_dd_pct >= 1.80:
            trade_risk = trade_risk * 0.5

        # Open position
        pos_active[slot] = True
        pos_end_times[slot] = t + hold
        pos_sleeves[slot] = slv
        pos_syms[slot] = sym
        pos_hb[slot] = hb

        pnl = r * trade_risk
        equity += pnl
        if equity > peak_equity:
            peak_equity = equity
        dd = ((peak_equity - equity) / peak_equity) * 100.0
        if dd > max_dd_pct:
            max_dd_pct = dd

        trade_pnls[tr_count] = pnl
        trade_times[tr_count] = t
        trade_sleeves[tr_count] = slv
        trade_evidx[tr_count] = i

        tr_count += 1
        if r > 0: win_count += 1
        if slv == 1: s1_tr += 1
        elif slv == 2: t1_tr += 1
        elif slv == 3: orb_tr += 1

    return equity - capital, max_dd_pct, tr_count, win_count, s1_tr, t1_tr, orb_tr, trade_pnls[:tr_count], trade_times[:tr_count], trade_sleeves[:tr_count], trade_evidx[:tr_count]

def run_elite_suite():
    t_start = time.perf_counter()
    print("=" * 140)
    print("ELITE QUANT 23 OOS REGIME-ROUTED STRATEGY SUITE (QUANT-DEVELOPERS-RESOURCES + SSRN-4647103)")
    print("Multi-Sleeve Confluence: S1 Liquidity Pullbacks + T1 Donchian Breakout + S3 Crypto ORB/CRT")
    print("=" * 140)

    all_data = compile_dataset_with_numba()

    with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
        windows = json.load(f)

    PURGE_MS = 72 * 3600 * 1000

    engine = InstitutionalDualModelEngine(
        capital=CAPITAL, base_risk=36.0, house_risk_max=50.0, defense_risk=14.0,
        milestone_risk=10.0, trans_risk=25.0, trans_thresh=380.0, t1_base_risk=36.0,
        t1_trans_risk=20.0, cushion_multiplier=0.20, milestone_profit_usd=500.0,
        max_concurrent=4, max_s1_concurrent=2, max_t1_concurrent=2, cooldown_bars=4,
        win_r_reset_thresh=0.90, conf_prob_thresh=0.46, conf_mult=1.35, max_dd_limit=4.85,
        random_state=42
    )

    from Engine.core.multi_tf_data import get_or_compute_4h_dataframe
    df_btc_4h = get_or_compute_4h_dataframe("BTCUSDT")
    df_btc_4h['atr_pct'] = (df_btc_4h['atr'] / df_btc_4h['close']) * 100.0
    df_btc_4h['trailing_30d_atr_pct'] = df_btc_4h['atr_pct'].rolling(180).mean()

    btc_df = pd.read_parquet(DATA_DIR / "BTCUSDT_15m_master_2020_2026.parquet", columns=["open_time_ms", "funding_rate_pct", "close", "high", "low"])
    btc_df["time"] = pd.to_datetime(btc_df["open_time_ms"], unit="ms", utc=True)
    btc_df.sort_values("time", inplace=True)
    btc_df.reset_index(drop=True, inplace=True)

    df_t1_pure = engine.load_t1_breakout_trades()
    orb_pool = load_cross_asset_orb_crt_pool(crypto_only=True)

    # ---- OX59 precomputes: symbol ids, BTC 4H breakdown state, per-symbol zc_norm ----
    SYM_ID = {"BTCUSDT": 0}
    for _k, _s in enumerate(sorted(CORE_SYMBOLS), start=1):
        if _s != "BTCUSDT":
            SYM_ID[_s] = _k
    BTC4H_MS = df_btc_4h['time'].astype('int64').to_numpy() // 1_000_000
    BTC4H_BD = (df_btc_4h['close'].to_numpy(float) < df_btc_4h['ema_200'].to_numpy(float))
    ZC_DB = {}
    for _s in CORE_SYMBOLS:
        _p = DATA_DIR / f"{_s}_15m_master_2020_2026.parquet"
        if _p.exists():
            _z = pd.read_parquet(_p, columns=["open_time_ms", "zc_div", "volume_base"])
            _vb = _z["volume_base"].replace(0, 1.0).to_numpy(float)
            _zn = np.clip(_z["zc_div"].to_numpy(float) / _vb, -3.0, 3.0)
            ZC_DB[_s] = (_z["open_time_ms"].to_numpy(np.int64), np.nan_to_num(_zn, nan=0.0))

    def _zc_at(_sym, _t_ms):
        _db = ZC_DB.get(_sym)
        if _db is None:
            return 0.0
        _i = int(np.searchsorted(_db[0], _t_ms, side="right")) - 1
        return float(_db[1][_i]) if _i >= 0 else 0.0

    print("\n" + "-" * 140)
    print(f"{'W#':<3} | {'Window Name':<38} | {'Regime':<18} | {'Trades':<6} | {'Sleeves':<14} | {'Win Rate':<8} | {'Net PnL':<12} | {'Net ROI':<9} | {'Max DD':<7} | {'Status':<6}")
    print("-" * 140)

    passed_count = 0
    total_trades = 0
    total_pnl = 0.0
    scorecard_rows = []
    all_executed_trades = []

    for w in windows:
        w_id = w["window_id"]
        w_name = w["name"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        purge_ms = start_ms - PURGE_MS

        train_mask = all_data.open_time_ms < purge_ms
        test_mask = (all_data.open_time_ms >= start_ms) & (all_data.open_time_ms <= end_ms)
        train_set = all_data[train_mask]
        test_set = all_data[test_mask]

        if len(train_set) < 500 or len(test_set) == 0: continue

        btc_prior = btc_df[btc_df.open_time_ms < purge_ms]
        ath = btc_prior["high"].max()
        cur_close = btc_prior["close"].iloc[-1]
        ath_dd = ((cur_close - ath) / ath) * 100.0

        trailing_30d_start = purge_ms - 30 * 86400 * 1000
        btc_30d = btc_df[(btc_df.open_time_ms >= trailing_30d_start) & (btc_df.open_time_ms < purge_ms)]
        btc_30d_ret = ((btc_30d["close"].iloc[-1] - btc_30d["close"].iloc[0]) / btc_30d["close"].iloc[0]) * 100.0 if len(btc_30d) > 0 else 0.0

        s_ts = pd.Timestamp(w["start_date"], tz="UTC")
        sub_btc_4h = df_btc_4h[df_btc_4h['time'] < s_ts]
        trailing_vol = sub_btc_4h['trailing_30d_atr_pct'].iloc[-1] if len(sub_btc_4h) > 0 else 1.75

        is_bear_contagion = (ath_dd <= -35.0) and (btc_30d_ret <= -10.0)
        is_bull_expansion = (btc_30d_ret >= 15.0) and (cur_close >= btc_prior["close"].rolling(200*4).mean().iloc[-1] if len(btc_prior) > 800 else True)
        is_chop_regime = not is_bear_contagion and not is_bull_expansion

        if is_bear_contagion: regime_label = "BEAR_CONTAGION"
        elif is_bull_expansion: regime_label = "BULL_EXPANSION"
        else: regime_label = "SIDEWAYS_CHOP"
        regime_id = 2 if is_bear_contagion else (1 if is_bull_expansion else 0)

        # 1. S1 Model
        ridge, clf, mu, sd, calib_thresh = engine.train_models(train_set)
        selected = engine.score_test_candidates(test_set, ridge, clf, mu, sd, calib_thresh, trailing_vol_pct=trailing_vol)

        s1_events = []
        train_short_mask = (train_set["signal_side"] == -1).to_numpy()
        X_train_s = np.nan_to_num(((train_set[FEATURE_COLS] - mu) / sd).clip(-5.0, 5.0).to_numpy(float), nan=0.0)
        train_probs_ridge = ridge.predict_proba(X_train_s)[:, 1]
        train_probs_lgb = clf.predict_proba(train_set[FEATURE_COLS])[:, 1]
        train_probs = 0.60 * train_probs_ridge + 0.40 * train_probs_lgb
        thresh_short = float(np.quantile(train_probs[train_short_mask], 0.60)) if train_short_mask.sum() > 50 else calib_thresh

        for idx in range(len(selected)):
            prob = float(selected["prob"].iloc[idx])
            tide = float(selected["btc_macro_tide"].iloc[idx]) if "btc_macro_tide" in selected.columns else 0.0
            side = int(selected["signal_side"].iloc[idx]) if "signal_side" in selected.columns else 1

            if is_bear_contagion:
                if side == -1 and tide == -1.0 and prob >= thresh_short:
                    s1_events.append({
                        "time": int(selected["open_time_ms"].iloc[idx]), "r_gain": float(selected["realized_r"].iloc[idx]),
                        "hold_ms": int(selected["bars_held"].iloc[idx]) * 15 * 60 * 1000, "symbol": str(selected["symbol"].iloc[idx]),
                        "strategy": "S1_SHORT", "prob": prob, "sleeve_id": 1, "risk": 32.0,
                        "side": side
                    })
            else:
                if side == -1 and tide > 0.0: continue
                if side == 1 and tide < 0.0 and prob < (calib_thresh + 0.038): continue
                if prob >= calib_thresh:
                    s1_events.append({
                        "time": int(selected["open_time_ms"].iloc[idx]), "r_gain": float(selected["realized_r"].iloc[idx]),
                        "hold_ms": int(selected["bars_held"].iloc[idx]) * 15 * 60 * 1000, "symbol": str(selected["symbol"].iloc[idx]),
                        "strategy": "S1", "prob": prob, "sleeve_id": 1, "risk": 30.0 if prob < 0.48 else 42.0,
                        "side": side
                    })

        # 2. T1 Breakout Events
        t1_events = []
        cur_t1 = df_t1_pure[(df_t1_pure['time'] >= start_ms) & (df_t1_pure['time'] <= end_ms)].copy()
        if not is_bear_contagion:
            for idx in range(len(cur_t1)):
                t1_events.append({
                    "time": int(cur_t1["time"].iloc[idx]), "r_gain": float(cur_t1["r_gain"].iloc[idx]),
                    "hold_ms": 16 * 4 * 3600 * 1000, "symbol": str(cur_t1["symbol"].iloc[idx]),
                    "strategy": "T1", "prob": float(cur_t1["prob"].iloc[idx]), "sleeve_id": 2, "risk": 36.0,
                    "side": int(cur_t1["side"].iloc[idx]) if "side" in cur_t1.columns else 1
                })

        # 3. S3 ORB/CRT
        orb_events = []
        orb_tr_mask = orb_pool['time'] < purge_ms
        orb_te_mask = (orb_pool['time'] >= start_ms) & (orb_pool['time'] <= end_ms)
        orb_train = orb_pool[orb_tr_mask]
        orb_test = orb_pool[orb_te_mask]

        if len(orb_train) >= 500 and len(orb_test) > 0:
            X_o_tr = orb_train[ORB_FEATURES]
            y_o_tr = (orb_train['outcome'] > 0).astype(int)
            orb_model = lgb.LGBMClassifier(
                n_estimators=100, max_depth=3, learning_rate=0.04, num_leaves=7,
                min_child_samples=30, reg_alpha=1.5, reg_lambda=3.0, random_state=42, n_jobs=-1, verbose=-1
            )
            orb_model.fit(X_o_tr, y_o_tr)
            probs = orb_model.predict_proba(orb_test[ORB_FEATURES])[:, 1]
            orb_cand = orb_test.copy()
            orb_cand['prob'] = probs
            thresh = np.percentile(probs, 70) if len(probs) > 10 else 0.55
            orb_passed = orb_cand[orb_cand['prob'] >= max(0.55, thresh)].copy()

            for idx in range(len(orb_passed)):
                o_side = 1 if float(orb_passed['direction_enum'].iloc[idx]) > 0 else -1
                o_sym = str(orb_passed['symbol'].iloc[idx])
                o_time = int(orb_passed['time'].iloc[idx])
                if is_bear_contagion and o_side == 1:
                    # OX59 BEAR: suppress non-trend longs unless extreme spot CVD divergence
                    # (causal: zc of the completed breakout bar, 15 min before entry).
                    if _zc_at(o_sym, o_time - 900_000) <= 1.2:
                        continue
                orb_events.append({
                    "time": o_time, "r_gain": float(orb_passed['outcome'].iloc[idx]),
                    "hold_ms": 24 * 15 * 60 * 1000, "symbol": o_sym,
                    "strategy": "ORB", "prob": float(orb_passed['prob'].iloc[idx]), "sleeve_id": 3, "risk": 24.0,
                    "side": o_side
                })

        combined = s1_events + t1_events + orb_events
        combined.sort(key=lambda x: (x["time"], -x["prob"]))

        if len(combined) == 0: continue

        ev_times = np.array([x["time"] for x in combined], dtype=np.int64)
        ev_rgains = np.array([x["r_gain"] for x in combined], dtype=np.float64)
        ev_risks = np.array([x["risk"] for x in combined], dtype=np.float64)
        ev_holds = np.array([x["hold_ms"] for x in combined], dtype=np.int64)
        ev_sleeves = np.array([x["sleeve_id"] for x in combined], dtype=np.int8)
        ev_syms = np.array([SYM_ID[x["symbol"]] for x in combined], dtype=np.int64)
        ev_sides = np.array([x["side"] for x in combined], dtype=np.int8)
        ev_hb = ((ev_sides == 1) & (ev_syms != 0)).astype(np.int8)
        btc_idx = np.searchsorted(BTC4H_MS, ev_times, side="right") - 1
        ev_btcbd = np.where(btc_idx >= 0, BTC4H_BD[np.maximum(btc_idx, 0)], False).astype(np.int8)

        net_pnl, max_dd, tr_count, win_count, s1_tr, t1_tr, orb_tr, tr_pnls, tr_times, tr_sleeves, tr_evidx = simulate_elite_portfolio(
            ev_times, ev_rgains, ev_risks, ev_holds, ev_sleeves,
            ev_syms, ev_sides, ev_hb, ev_btcbd, regime_id,
            capital=CAPITAL, max_concurrent=3, max_s1_concurrent=2, max_t1_concurrent=2,
            max_orb_concurrent=2, milestone_pnl=500.0, dd_stop_pct=4.85
        )

        wr = (win_count / tr_count * 100.0) if tr_count > 0 else 0.0
        net_roi = (net_pnl / CAPITAL) * 100.0
        is_pass = (net_roi >= MIN_ROI) and (max_dd <= MAX_DD) and (wr >= MIN_WR) and (tr_count >= MIN_TRADES)
        status = "PASS" if is_pass else ("PROFIT" if net_pnl > 0 and max_dd <= MAX_DD else ("CASH" if tr_count == 0 else "FAIL"))

        if is_pass: passed_count += 1
        total_trades += tr_count
        total_pnl += net_pnl

        eq_curve = (CAPITAL + np.cumsum(np.insert(tr_pnls, 0, 0.0))).tolist()

        for tp, tt, ts, te in zip(tr_pnls, tr_times, tr_sleeves, tr_evidx):
            _ev = combined[int(te)]
            all_executed_trades.append({
                "window_id": w_id, "time": int(tt), "pnl": float(tp), "sleeve": int(ts),
                "symbol": str(_ev["symbol"]), "strategy": str(_ev["strategy"]),
                "r_gain": float(_ev["r_gain"]), "risk": float(_ev["risk"]), "prob": float(_ev["prob"])
            })

        sleeve_summary = f"S1:{s1_tr} T1:{t1_tr} ORB:{orb_tr}"
        print(f"W{w_id:02d} | {w_name[:38]:<38} | {regime_label:<18} | {tr_count:<6d} | {sleeve_summary:<14} | {wr:>5.1f}%  | {net_pnl:>+10.2f} USD | {net_roi:>+7.2f}% | {max_dd:>5.2f}% | {status:<6}")

        scorecard_rows.append({
            "window_id": w_id, "name": w_name, "regime": regime_label, "trades": tr_count,
            "s1_trades": s1_tr, "t1_trades": t1_tr, "orb_trades": orb_tr,
            "win_rate_pct": wr, "net_pnl_usd": net_pnl, "net_roi_pct": net_roi, "max_dd_pct": max_dd,
            "status": status, "equity_curve": eq_curve
        })

    print("=" * 140)
    print(f"ELITE 23-QUARTER SCORECARD: Passed: {passed_count}/{len(windows)} | Total Trades: {total_trades:,d} | Total Net PnL: {total_pnl:+,.2f} USD (ROI: {(total_pnl/CAPITAL)*100:+.2f}%)")
    print(f"Total Execution Time: {time.perf_counter() - t_start:.2f} seconds")
    print("=" * 140)

    # Save Results
    reports_dir = REPO / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    res_df = pd.DataFrame(scorecard_rows)
    res_df.drop(columns=["equity_curve"], errors="ignore").to_csv(reports_dir / "elite_23_oos_regime_scorecard.csv", index=False)
    with open(reports_dir / "elite_23_oos_regime_results.json", "w", encoding="utf-8") as f:
        json.dump(scorecard_rows, f, indent=2)

    if all_executed_trades:
        df_trades = pd.DataFrame(all_executed_trades)
        df_trades.to_parquet(reports_dir / "elite_23_oos_all_trades.parquet", index=False)
        print(f"Saved {len(df_trades):,d} executed trades to: {reports_dir / 'elite_23_oos_all_trades.parquet'}")

    plot_elite_performance(scorecard_rows, windows, btc_df)

def plot_elite_performance(scorecard_rows, windows, btc_df):
    reports_dir = REPO / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_png = reports_dir / "elite_23_oos_equity_vs_benchmark.png"
    brain_png = Path(r"C:\Users\SIGMA\.gemini\antigravity\brain\ffa08070-c9a9-49d2-a394-b72ce2e0971d\elite_23_oos_equity_vs_benchmark.png")

    df_sc = pd.DataFrame(scorecard_rows)
    n = len(df_sc)

    # Strategy cumulative equity
    strat_cum_pnl = df_sc["net_pnl_usd"].cumsum().to_numpy()
    strat_equity = np.insert(CAPITAL + strat_cum_pnl, 0, CAPITAL)

    # Benchmark: BTC Buy & Hold normalized to CAPITAL
    btc_returns = []
    btc_df_t = btc_df.set_index("time").sort_index()
    for w in windows:
        s = pd.Timestamp(w["start_date"], tz="UTC")
        e = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC")
        sub = btc_df_t.loc[s:e]
        if len(sub) < 2:
            btc_returns.append(0.0)
        else:
            ret = (sub["close"].iloc[-1] / sub["close"].iloc[0] - 1.0) * 100.0
            btc_returns.append(ret)

    bh_equity = [CAPITAL]
    cur = CAPITAL
    for r in btc_returns:
        cur = cur * (1.0 + r / 100.0)
        bh_equity.append(cur)
    bh_equity = np.array(bh_equity)

    # Underwater drawdowns
    def calc_dd(eq):
        peak = np.maximum.accumulate(eq)
        return ((peak - eq) / peak) * 100.0

    strat_dd = calc_dd(strat_equity)
    btc_dd = calc_dd(bh_equity)

    fig = plt.figure(figsize=(20, 14), facecolor="#0d1117")
    fig.suptitle(
        "ELITE QUANT 23-QUARTER OOS MULTI-SLEEVE SUITE VS BTC BUY & HOLD\nS1 Liquidity Pullback + T1 Donchian Breakout + S3 Crypto ORB/CRT",
        fontsize=16, color="white", fontweight="bold", y=0.98
    )

    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1], hspace=0.35)

    x = np.arange(n + 1)
    labels = ["Start"] + [f"W{r['window_id']:02d}" for r in scorecard_rows]

    # Subplot 1: Equity Curves
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(x, strat_equity, color="#00ffcc", linewidth=3.0, label=f"Strategy Suite (Final: {strat_equity[-1]:+,.2f} USD | ROI: {((strat_equity[-1]-CAPITAL)/CAPITAL)*100:+.1f}%)")
    ax1.plot(x, bh_equity, color="#ffaa00", linewidth=2.0, linestyle="--", label=f"BTC Buy & Hold (Final: {bh_equity[-1]:+,.2f} USD | ROI: {((bh_equity[-1]-CAPITAL)/CAPITAL)*100:+.1f}%)")
    ax1.axhline(CAPITAL, color="#888888", linestyle=":", alpha=0.7)
    ax1.fill_between(x, CAPITAL, strat_equity, color="#00ffcc", alpha=0.15)
    ax1.set_facecolor("#161b22")
    ax1.tick_params(colors="white")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, color="white", fontsize=9)
    ax1.set_ylabel("Account Equity (USD)", color="white", fontsize=11)
    ax1.legend(loc="upper left", facecolor="#161b22", labelcolor="white")
    ax1.grid(True, color="#30363d", alpha=0.5)

    # Subplot 2: Underwater Drawdown
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(x, -strat_dd, color="#00ffcc", linewidth=2.0, label=f"Strategy Max DD ({np.max(strat_dd):.2f}%)")
    ax2.plot(x, -btc_dd, color="#ff5555", linewidth=1.8, linestyle="--", label=f"BTC Max DD ({np.max(btc_dd):.2f}%)")
    ax2.axhline(-5.0, color="#ff0055", linestyle=":", label="5% DD Limit")
    ax2.fill_between(x, 0, -strat_dd, color="#00ffcc", alpha=0.2)
    ax2.fill_between(x, 0, -btc_dd, color="#ff5555", alpha=0.1)
    ax2.set_facecolor("#161b22")
    ax2.tick_params(colors="white")
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=45, color="white", fontsize=9)
    ax2.set_ylabel("Drawdown (%)", color="white", fontsize=11)
    ax2.legend(loc="lower left", facecolor="#161b22", labelcolor="white")
    ax2.grid(True, color="#30363d", alpha=0.5)

    # Subplot 3: Per-Window Net ROI (%)
    ax3 = fig.add_subplot(gs[2])
    bar_x = np.arange(1, n + 1)
    rois = [r["net_roi_pct"] for r in scorecard_rows]
    passes = [r["status"] == "PASS" for r in scorecard_rows]
    bar_colors = ["#2ecc71" if p else "#e74c3c" for p in passes]
    bars = ax3.bar(bar_x, rois, color=bar_colors, width=0.65, edgecolor="#ffffff", alpha=0.85)
    ax3.axhline(10.0, color="#2ecc71", linestyle="--", label="Pass Target (+10% ROI)")
    ax3.set_facecolor("#161b22")
    ax3.tick_params(colors="white")
    ax3.set_xticks(bar_x)
    ax3.set_xticklabels([f"W{r['window_id']:02d}" for r in scorecard_rows], rotation=45, color="white", fontsize=9)
    ax3.set_ylabel("Net ROI (%)", color="white", fontsize=11)
    ax3.grid(True, color="#30363d", alpha=0.5)
    ax3.legend(loc="upper right", facecolor="#161b22", labelcolor="white")

    plt.tight_layout()
    plt.savefig(out_png, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Equity curve chart saved to: {out_png}")

    if brain_png.parent.exists():
        shutil.copy(out_png, brain_png)
        print(f"Chart copied to conversation artifacts: {brain_png}")

if __name__ == "__main__":
    run_elite_suite()
