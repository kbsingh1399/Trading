r"""V2 Numba walk-forward engine.

Changes vs V1 (all causal, no test-set information used for design):
1. Candidate pool enriched: original T1/T2/T3 suite + inverted suite + trend-pullback
   sleeve (design-period evidence showed original entries anti-selective).
2. Geometry from causal design-period grid: hz=48, target=2.0R, stop=1.0R,
   BE ratchet +0.75R->lock +0.35R, profit lock +1.40R->+0.80R, friction 0.25R.
3. Time-decay exit: flat at 24 bars if unrealized < +0.20R (mandate rule).
4. Regression selection (predict clipped net realized_r) + in-sample margin:
   trade only when expected net r > calibrated margin AND prob.quantile gate.
5. Extra causal features: mom_3d (288-bar return), e200dist.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lightgbm as lgb
from numba import njit
import numpy as np
import pandas as pd

from scratch.fast_numba_oos_engine import (
    DATA_DIR, WINDOWS_PATH, CRITERIA_PATH, OUTPUT_DIR,
    CORE_SYMBOLS, COLS_TO_LOAD, load_btc_macro_tide, warmup_numba,
)

FEATURE_COLS = [
    "vwap_zscore", "long_liq_zs", "short_liq_zs", "zc_norm", "taker_ratio",
    "rsi_14", "atr_ratio", "volume_ratio", "slope200", "funding_rate_pct",
    "basis_index_bps", "vol_strain", "hour", "tide_align", "signal_side",
    "sleeve_id", "mom_3d", "e200dist", "btc_mom_3d", "rel_str_3d",
]

# Geometry (design-period grid selection)
HZ, TARGET, STOP = 48, 2.0, 1.0
BE_TRIG, BE_LOCK = 0.75, 0.35
P_TRIG, P_LOCK = 1.40, 0.80
DECAY_BARS, DECAY_MIN_R = 24, 0.20
FRICTION = 0.25

PURGE_MS = 72 * 3600 * 1000


@njit(fastmath=True)
def label_ratchet_decay_numba(
    c: np.ndarray, h: np.ndarray, lo: np.ndarray, atr: np.ndarray,
    long_cond: np.ndarray, short_cond: np.ndarray,
    horizon_bars: int, target_r: float, stop_r: float,
    be_trigger_r: float, be_lock_r: float,
    profit_trigger_r: float, profit_lock_r: float,
    decay_bars: int, decay_min_r: float, friction_r: float,
):
    """Two-stage ratchet + time-decay labeler. Causal j+1 arming."""
    n = len(c)
    is_candidate = np.zeros(n, dtype=np.bool_)
    side = np.zeros(n, dtype=np.int8)
    label_y = np.full(n, -1, dtype=np.int8)
    realized_r = np.zeros(n, dtype=np.float64)
    bars_held = np.zeros(n, dtype=np.int16)

    for i in range(n - horizon_bars):
        s = 0
        if long_cond[i]:
            s = 1
        elif short_cond[i]:
            s = -1
        else:
            continue
        is_candidate[i] = True
        side[i] = s
        entry_p = c[i]
        dist = atr[i]
        if dist <= 0:
            continue

        cur_stop_r = -stop_r
        exit_r = 0.0
        hit = False
        hold_count = horizon_bars

        for j in range(i + 1, i + 1 + horizon_bars):
            if s == 1:
                adverse_r = (lo[j] - entry_p) / dist
                favorable_r = (h[j] - entry_p) / dist
            else:
                adverse_r = (entry_p - h[j]) / dist
                favorable_r = (entry_p - lo[j]) / dist

            # 1. stop first (armed at j-1 close)
            if adverse_r <= cur_stop_r:
                exit_r = cur_stop_r
                hit = True
                hold_count = j - i
                break
            # 2. target
            if favorable_r >= target_r:
                exit_r = target_r
                hit = True
                hold_count = j - i
                break
            # 3. time decay at exactly decay_bars (no progress -> market exit)
            if j - i == decay_bars:
                cur_r = (c[j] - entry_p) / dist if s == 1 else (entry_p - c[j]) / dist
                if cur_r < decay_min_r:
                    exit_r = cur_r
                    hit = True
                    hold_count = j - i
                    break
            # 4. arm ratchets for j+1
            if favorable_r >= profit_trigger_r:
                if profit_lock_r > cur_stop_r:
                    cur_stop_r = profit_lock_r
            elif favorable_r >= be_trigger_r:
                if be_lock_r > cur_stop_r:
                    cur_stop_r = be_lock_r

        if not hit:
            exit_p = c[i + horizon_bars]
            exit_r = (exit_p - entry_p) / dist if s == 1 else (entry_p - exit_p) / dist
            hold_count = horizon_bars

        net_r = exit_r - friction_r
        realized_r[i] = net_r
        label_y[i] = 1 if net_r > 0 else 0
        bars_held[i] = hold_count

    return is_candidate, side, label_y, realized_r, bars_held


def compile_dataset_v2(horizon: int = HZ, target_r: float = TARGET, stop_r: float = STOP,
                       be_trig: float = BE_TRIG, be_lock: float = BE_LOCK,
                       p_trig: float = P_TRIG, p_lock: float = P_LOCK,
                       decay_bars: int = DECAY_BARS, decay_min_r: float = DECAY_MIN_R,
                       friction: float = FRICTION) -> pd.DataFrame:
    btc_tide = load_btc_macro_tide()
    # BTC 3-day momentum series for cross-asset relative strength (causal).
    btc_df = pd.read_parquet(DATA_DIR / "BTCUSDT_15m_master_2020_2026.parquet",
                             columns=["open_time_ms", "close"])
    btc_df["btc_mom_3d"] = btc_df["close"] / btc_df["close"].shift(288) - 1.0
    btc_mom = btc_df.set_index("open_time_ms")["btc_mom_3d"]
    frames = []
    t_start = time.perf_counter()

    print(f"\n[V2] Processing {len(CORE_SYMBOLS)} assets (suite + INV suite + PB pullback)...")
    for sym in CORE_SYMBOLS:
        p_path = DATA_DIR / f"{sym}_15m_master_2020_2026.parquet"
        if not p_path.exists():
            continue
        df = pd.read_parquet(p_path, columns=COLS_TO_LOAD)
        c, hh, lo = df.close.to_numpy(float), df.high.to_numpy(float), df.low.to_numpy(float)
        t = df.open_time_ms.to_numpy(np.int64)

        atr_raw = df["atr_14"].fillna(df["close"] * 0.01).to_numpy(float)
        atr = np.maximum(atr_raw, df["close"].to_numpy(float) * 0.012)
        atr_100 = df["atr_100"].fillna(df["close"] * 0.01).to_numpy(float)
        atr_ratio = np.clip(np.where(atr_100 > 0, atr / atr_100, 1.0), 0.2, 5.0)
        e200 = df["ema_200"].to_numpy(float)
        e200_s = df["ema_200"]
        slope = ((e200_s - e200_s.shift(12)) / df["close"]).fillna(0.0).to_numpy(float)
        tide = pd.Series(t).map(btc_tide).fillna(0.0).to_numpy(float)
        vwap_z = df["vwap_zscore"].fillna(0.0).to_numpy(float)
        vol_ratio = df["volume_ratio"].fillna(1.0).to_numpy(float)
        vol_base = df["volume_base"].replace(0, 1.0)
        zc_norm = (df["zc_div"] / vol_base).clip(-3.0, 3.0).fillna(0.0).to_numpy(float)
        long_liq = df["long_liq_zs"].fillna(0.0).to_numpy(float)
        short_liq = df["short_liq_zs"].fillna(0.0).to_numpy(float)
        s_val = df["session_val"].fillna(df["low"]).to_numpy(float)
        s_vah = df["session_vah"].fillna(df["high"]).to_numpy(float)
        taker_ratio = df["taker_volume_ratio"].fillna(1.0).to_numpy(float)
        fund_rate = df["funding_rate_pct"].fillna(0.0).to_numpy(float)
        basis_bps = df["basis_index_bps"].fillna(0.0).to_numpy(float)
        rsi = df["rsi_14"].fillna(50.0).to_numpy(float)
        vol_strain = np.clip(atr / np.maximum(c, 1e-6), 0.005, 0.10)
        hour = (t // (3600 * 1000)) % 24
        mom_3d = (df["close"] / df["close"].shift(288) - 1.0).fillna(0.0).to_numpy(float)
        e200dist = np.clip(c / np.maximum(e200, 1e-9) - 1.0, -0.2, 0.2)
        btc_mom_arr = pd.Series(t).map(btc_mom).fillna(0.0).to_numpy(float)
        rel_str_3d = mom_3d - btc_mom_arr

        # ---- Original triple suite (priority 1-3)
        t1_long = (atr_ratio < 0.85) & (vol_ratio >= 1.6) & (slope > 0.05) & (c > e200) & (tide >= 0)
        t1_short = (atr_ratio < 0.85) & (vol_ratio >= 1.6) & (slope < -0.05) & (c < e200) & (tide <= 0)
        t2_long = (lo <= s_val) & (c > s_val) & (vwap_z < -0.5) & (zc_norm > 0.03) & (c > e200)
        t2_short = (hh >= s_vah) & (c < s_vah) & (vwap_z > 0.5) & (zc_norm < -0.03) & (c < e200) & (short_liq < 1.0)
        t3_long = (taker_ratio >= 1.3) & (vol_ratio >= 1.5) & (zc_norm >= 0.06) & (slope > 0.08) & (tide >= 0)
        t3_short = (taker_ratio <= 0.7) & (vol_ratio >= 1.5) & (zc_norm <= -0.06) & (slope < -0.08) & (tide <= 0)

        # ---- Inverted suite (priority 11-13): flip sides of each condition
        i1_long, i1_short = t1_short.copy(), t1_long.copy()
        i2_long, i2_short = t2_short.copy(), t2_long.copy()
        i3_long, i3_short = t3_short.copy(), t3_long.copy()

        # ---- Trend-pullback sleeve (priority 4): rejoin prevailing trend
        pb_long = (c > e200) & (slope > 0.015) & (tide >= 0) & (rsi > 50) & (rsi < 85) & (atr_ratio < 1.30)
        pb_short = (c < e200) & (slope < -0.015) & (tide <= 0) & (rsi < 50) & (rsi > 15) & (atr_ratio < 1.30)

        fin = np.isfinite(atr) & (atr > 0)

        # Build (side, sleeve_priority) per bar with dedupe: at most one
        # candidate per bar (long OR short), highest-priority sleeve wins.
        cand_side = np.zeros(len(c), dtype=np.int8)
        cand_slv = np.zeros(len(c), dtype=np.int8)
        order = [
            (t1_long, t1_short, 1), (t2_long, t2_short, 2), (t3_long, t3_short, 3),
            (pb_long, pb_short, 4),
            (i1_long, i1_short, 11), (i2_long, i2_short, 12), (i3_long, i3_short, 13),
        ]
        occupied = np.zeros(len(c), dtype=np.bool_)
        for lg, sh, slv in order:
            lmask = lg & fin & ~occupied
            smask = sh & fin & ~occupied & ~lmask
            cand_side[lmask] = 1
            cand_side[smask] = -1
            cand_slv[lmask | smask] = slv
            occupied |= lmask | smask

        long_cond = (cand_side == 1)
        short_cond = (cand_side == -1)

        ic, sd, ly, rr, bh = label_ratchet_decay_numba(
            c, hh, lo, atr, long_cond, short_cond,
            horizon, target_r, stop_r, be_trig, be_lock, p_trig, p_lock,
            decay_bars, decay_min_r, friction,
        )

        idx = np.where(ic)[0]
        side_sel = sd[idx]
        tide_align = np.where(side_sel == 1, tide[idx], np.where(side_sel == -1, -tide[idx], 0.0))
        f_sub = pd.DataFrame({
            "open_time_ms": t[idx],
            "vwap_zscore": vwap_z[idx],
            "long_liq_zs": long_liq[idx],
            "short_liq_zs": short_liq[idx],
            "zc_norm": zc_norm[idx],
            "taker_ratio": taker_ratio[idx],
            "rsi_14": rsi[idx],
            "atr_ratio": atr_ratio[idx],
            "volume_ratio": vol_ratio[idx],
            "slope200": slope[idx],
            "funding_rate_pct": fund_rate[idx],
            "basis_index_bps": basis_bps[idx],
            "vol_strain": vol_strain[idx],
            "hour": hour[idx],
            "tide_align": tide_align,
            "signal_side": sd[idx],
            "sleeve_id": cand_slv[idx],
            "mom_3d": mom_3d[idx],
            "e200dist": e200dist[idx],
            "btc_mom_3d": btc_mom_arr[idx],
            "rel_str_3d": rel_str_3d[idx],
            "realized_r": rr[idx],
            "label_y": ly[idx],
            "bars_held": bh[idx],
            "symbol": sym,
        })
        frames.append(f_sub)
        print(f"  [{sym:<8}] {len(df):,d} bars -> {len(f_sub):,d} candidates")

    pool = pd.concat(frames, ignore_index=True)
    pool.sort_values("open_time_ms", inplace=True)
    pool.reset_index(drop=True, inplace=True)
    print(f"[V2] Total candidates: {len(pool):,d} in {time.perf_counter()-t_start:.2f}s")
    print(f"[V2] Pool mean net r: {pool.realized_r.mean():+.4f}R | wr: {(pool.realized_r>0).mean()*100:.2f}%")
    return pool


def run_walkforward_v2(all_data: pd.DataFrame, target_trades: float = 24.0,
                       max_depth: int = 3, margin_mode: str = "floor0",
                       defense_dd: float = 2.0, defense_risk: float = 20.0,
                       verbose: bool = True):
    t_wf = time.perf_counter()
    with open(CRITERIA_PATH, "r", encoding="utf-8") as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
        windows = json.load(f)

    CAPITAL = criteria.get("initial_capital_usd", 5000.0)
    BASE_RISK_USD = 40.0
    DEFENSE_RISK_USD = 20.0
    MIN_ROI = criteria.get("min_roi_percent", 10.0)
    MAX_DD = criteria.get("max_dd_percent", 5.0)
    MIN_WR = criteria.get("min_winrate_percent", 40.0)
    MIN_TRADES = criteria.get("min_trades", 15)

    print("=" * 128)
    print("V2 WALK-FORWARD (suite+INV+PB | regressor selection | ratchet+time-decay exits)")
    print("=" * 128)
    print(f"{'W#':<3} | {'Window Name':<38} | {'Cands':<7} | {'Trades':<6} | {'Win Rate':<8} | {'Net PnL':<11} | {'Net ROI':<9} | {'Max DD':<7} | {'Verdict':<6}")
    print("-" * 128)

    results, all_trades_dump = [], []
    total_trades, total_pnl, pass_count = 0, 0.0, 0

    for w in windows:
        w_id, w_name = w["window_id"], w["name"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000

        train_set = all_data[all_data.open_time_ms < (start_ms - PURGE_MS)]
        test_set = all_data[(all_data.open_time_ms >= start_ms) & (all_data.open_time_ms <= end_ms)]
        if len(train_set) < 500 or len(test_set) == 0:
            continue

        X_train = train_set[FEATURE_COLS]
        y_train = np.clip(train_set["realized_r"].to_numpy(), -1.25, 2.0)
        X_test = test_set[FEATURE_COLS]

        reg = lgb.LGBMRegressor(
            n_estimators=150, max_depth=max_depth, learning_rate=0.03,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=2.0, reg_lambda=4.0,
            random_state=42, verbose=-1, n_jobs=-1,
        )
        reg.fit(X_train, y_train)

        # Causal calibration: trade-density estimated from train only.
        train_pred = reg.predict(X_train)
        t_min, t_max = train_set["open_time_ms"].min(), train_set["open_time_ms"].max()
        train_months = max((t_max - t_min) / (30.4375 * 24 * 3600 * 1000), 1.0)
        est_cands = len(train_set) / train_months
        calib_q = max(0.50, min(0.92, 1.0 - (target_trades / max(est_cands, 1))))
        dens_thresh = float(np.quantile(train_pred, calib_q))
        if margin_mode == "floor0":
            thresh = max(dens_thresh, 0.0)
        elif margin_mode == "soft":
            thresh = max(dens_thresh, float(np.quantile(train_pred, 0.50)))
        else:
            thresh = dens_thresh

        test_pred = reg.predict(X_test)
        test_r = test_set["realized_r"].to_numpy()
        test_times = test_set["open_time_ms"].to_numpy()
        test_bars = test_set["bars_held"].to_numpy()
        test_syms = test_set["symbol"].to_numpy()

        sel = np.where(test_pred >= thresh)[0]

        open_positions = []  # (expiry_ms, symbol)
        executed = []
        equity, peak_equity, cur_max_dd_pct = CAPITAL, CAPITAL, 0.0
        for k in sel:
            t_entry = test_times[k]
            open_positions = [op for op in open_positions if op[0] > t_entry]
            if test_syms[k] in [op[1] for op in open_positions]:
                continue  # one open position per symbol
            if len(open_positions) < 2:
                hold_ms = int(test_bars[k]) * 15 * 60 * 1000
                open_positions.append((t_entry + hold_ms, test_syms[k]))
                r_gain = test_r[k]
                if cur_max_dd_pct >= defense_dd:
                    risk_amt = defense_risk
                elif (equity - CAPITAL) >= 50.0:
                    risk_amt = min(100.0, BASE_RISK_USD + (equity - CAPITAL) * 0.40)
                else:
                    risk_amt = BASE_RISK_USD
                pnl = r_gain * risk_amt
                executed.append({"time": t_entry, "r": r_gain,
                                 "win": 1 if r_gain > 0 else 0, "pnl": pnl})
                equity += pnl
                peak_equity = max(peak_equity, equity)
                dd_pct = ((peak_equity - equity) / peak_equity) * 100
                cur_max_dd_pct = max(cur_max_dd_pct, dd_pct)

        n_trades = len(executed)
        wr = (sum(x["win"] for x in executed) / n_trades * 100) if n_trades else 0.0
        pnl = sum(x["pnl"] for x in executed)
        roi = pnl / CAPITAL * 100

        is_pass = (roi >= MIN_ROI) and (cur_max_dd_pct <= MAX_DD) and (wr >= MIN_WR) and (n_trades >= MIN_TRADES)
        status = "PASS" if is_pass else ("FAIL" if n_trades else "CASH")
        pass_count += 1 if is_pass else 0
        total_trades += n_trades
        total_pnl += pnl

        if verbose:
            print(f"W{w_id:02d} | {w_name[:38]:<38} | {len(test_set):<7d} | {n_trades:<6d} | {wr:>6.1f}%  | {pnl:>+9.2f} USD | {roi:>+7.2f}% | {cur_max_dd_pct:>5.2f}% | {status:<6}")
        results.append({"window_id": w_id, "name": w_name, "trades": n_trades,
                        "win_rate": wr, "pnl_usd": pnl, "roi_pct": roi,
                        "max_dd_pct": cur_max_dd_pct, "status": status})
        all_trades_dump.extend([{**x, "window": w_id} for x in executed])

    print("=" * 128)
    print(f"V2 SUMMARY: time={time.perf_counter()-t_wf:.2f}s | trades={total_trades} | PnL={total_pnl:+,.2f} USD "
          f"(ROI {total_pnl/CAPITAL*100:+.2f}%) | PASSED {pass_count}/{len(results)}")
    print("=" * 128)

    json_dump = {"results": results, "total_pnl": total_pnl, "pass_count": pass_count,
                 "target_trades": target_trades, "margin_mode": margin_mode,
                 "max_depth": max_depth}
    (OUTPUT_DIR / "v2_last_scorecard.json").write_text(json.dumps(json_dump, indent=2))
    return pass_count, results


def main():
    warmup_numba()
    pool = compile_dataset_v2()
    pool.to_parquet("scratch/pool_v2.parquet", index=False)
    run_walkforward_v2(pool)


if __name__ == "__main__":
    main()
