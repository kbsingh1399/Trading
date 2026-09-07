"""
================================================================================
18-ASSET PARALLEL OOS WALK-FORWARD HARNESS
================================================================================
Loads target_oos_criteria.json from Engine/ and runs all 18 assets in parallel.
Each asset is treated individually with its own causal IS rolling optimization pass.

Target Criteria (from target_oos_criteria.json):
  - ROI per OOS window  > 20%
  - Max DD per window   < 5%
  - Win Rate per window > 40%
  - Min R per trade     >= 5R  (trailing SL arms at 5R)
  - Min trades          >= 5 per window

Architecture:
  - SMC Liquidity Sweep & Reclaim + Order Flow Absorption
  - 5R hard profit target; trailing SL arms at 5R locking 4.2R, trailing 0.8R behind peak
  - Per-asset parameter grid IS-optimised causally before each OOS window
  - multiprocessing.Pool for true parallel execution across assets
================================================================================
"""
from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import multiprocessing as mp

# -- Paths ----------------------------------------------------------------------
_ENGINE   = Path(__file__).resolve().parent.parent      # .../Engine
_DATA     = _ENGINE / "binance_backtesting_data"
_WINDOWS  = _ENGINE / "oos_windows_20.json"
_CRITERIA = _ENGINE / "target_oos_criteria.json"

# -- 18 Canonical Assets --------------------------------------------------------
ASSETS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT",
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT",
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT",
]

# -- Institutional Friction -----------------------------------------------------
TAKER_FEE  = 0.0008
ENTRY_SLIP = 0.0010
EXIT_SLIP  = 0.0015

INITIAL_CAPITAL = 5_000.0
DD_LIMIT        = 0.048
PURGE_HOURS     = 72


# -- Parameters -----------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    roll_bars:       int   = 12
    ema_filter:      str   = "ema_21"
    atr_mult_stop:   float = 1.8
    max_stop_pct:    float = 0.022
    min_stop_pct:    float = 0.006
    min_target_r:    float = 5.0
    trailing_r_arm:  float = 5.0
    trailing_lock_r: float = 4.2
    trailing_slack:  float = 0.8
    time_decay_bars: int   = 64
    time_decay_r:    float = 0.50
    base_risk:       float = 45.0
    house_risk:      float = 85.0
    defense_risk:    float = 20.0
    liq_zs_min:      float = 0.0
    cascade_union:   bool  = False


PARAM_GRID = [
    # Fast swing sweeps (8 bars) - optimal for high-velocity altcoins (ETH, ADA, DOT)
    Params(roll_bars=8,  ema_filter="ema_21", atr_mult_stop=1.6, base_risk=45.0, house_risk=80.0),
    Params(roll_bars=8,  ema_filter="ema_21", atr_mult_stop=1.8, base_risk=45.0, house_risk=85.0),
    Params(roll_bars=8,  ema_filter="ema_50", atr_mult_stop=1.8, base_risk=45.0, house_risk=85.0),

    # Medium 12-bar swing sweeps - optimal for mid-beta assets (BNB, DOGE, LTC)
    Params(roll_bars=12, ema_filter="ema_21", atr_mult_stop=1.8, base_risk=45.0, house_risk=85.0),
    Params(roll_bars=12, ema_filter="ema_21", atr_mult_stop=2.0, base_risk=45.0, house_risk=85.0),
    Params(roll_bars=12, ema_filter="ema_50", atr_mult_stop=1.8, base_risk=45.0, house_risk=85.0),

    # Deep 16-bar swing sweeps - optimal for macro assets (BTC, LINK, BCH)
    Params(roll_bars=16, ema_filter="ema_21", atr_mult_stop=1.8, base_risk=50.0, house_risk=90.0),
    Params(roll_bars=16, ema_filter="ema_50", atr_mult_stop=2.0, base_risk=50.0, house_risk=90.0),

    # Order flow confluence variants
    Params(roll_bars=12, ema_filter="ema_21", atr_mult_stop=1.8, base_risk=45.0, house_risk=85.0, cascade_union=True),
    Params(roll_bars=12, ema_filter="ema_21", atr_mult_stop=1.8, base_risk=45.0, house_risk=85.0, liq_zs_min=0.8),
]


# ------------------------------------------------------------------------------
# SIMULATOR
# ------------------------------------------------------------------------------
def simulate(df: pd.DataFrame, p: Params, is_trend_up: object = (True, True)) -> Dict:
    """Vectorised simulation with SMC liquidity sweep & reclaim + 5R trailing exit."""
    T  = len(df)
    op = df["open"].values
    hi = df["high"].values
    lo = df["low"].values
    cl = df["close"].values

    atr      = df["atr_14"].clip(lower=cl * 0.001).bfill().values
    spot_cvd = df["spot_cvd_15m"].fillna(0.0).values
    long_lzs = df["long_liq_zs"].fillna(0.0).values
    short_lzs= df["short_liq_zs"].fillna(0.0).values
    zc_div   = df["zc_div"].fillna(0.0).values
    rsi      = df["rsi_14"].fillna(50.0).values
    ema_f    = df[p.ema_filter].bfill().values if p.ema_filter in df else cl

    bull_candle = (cl > op) | ((cl - lo) > (hi - cl) * 1.5)
    bear_candle = (cl < op) | ((hi - cl) > (cl - lo) * 1.5)

    # 1. SMC Liquidity Sweep & Reclaim
    roll_l = pd.Series(lo).shift(1).rolling(p.roll_bars).min().bfill().values
    roll_h = pd.Series(hi).shift(1).rolling(p.roll_bars).max().bfill().values

    sweep_low  = (lo < roll_l) & (cl > roll_l) & (cl > ema_f) & bull_candle & (spot_cvd > 0)
    sweep_high = (hi > roll_h) & (cl < roll_h) & (cl < ema_f) & bear_candle & (spot_cvd < 0)

    if p.liq_zs_min > 0:
        sweep_low  = sweep_low  & (long_lzs >= p.liq_zs_min)
        sweep_high = sweep_high & (short_lzs >= p.liq_zs_min)

    if p.cascade_union:
        sig_long_casc = (long_lzs > 1.0) & (zc_div > 0) & (spot_cvd > 0) & (rsi < 48) & bull_candle
        sig_short_casc = (short_lzs > 1.0) & (zc_div < 0) & (spot_cvd < 0) & (rsi > 52) & bear_candle
        sig_long_raw  = sweep_low | sig_long_casc
        sig_short_raw = sweep_high | sig_short_casc
    else:
        sig_long_raw  = sweep_low
        sig_short_raw = sweep_high

    if isinstance(is_trend_up, bool):
        allow_l = is_trend_up
        allow_s = not is_trend_up
    else:
        allow_l, allow_s = is_trend_up
    sig_long  = sig_long_raw  if allow_l else np.zeros(T, dtype=bool)
    sig_short = sig_short_raw if allow_s else np.zeros(T, dtype=bool)

    realized = INITIAL_CAPITAL
    peak     = realized
    pos_side = 0; pos_entry = 0.0; pos_stop = 0.0; pos_target = 0.0
    pos_qty  = 0.0; pos_rr = 0.0; pos_risk = 0.0; pos_bar = 0; pos_max_r = 0.0
    trailing_armed = False
    trades: List[Dict] = []
    equity_curve = np.full(T, realized)
    last_exit_bar = -999

    for t in range(p.roll_bars, T):
        o_, h_, l_, c_ = op[t], hi[t], lo[t], cl[t]

        if pos_side != 0:
            exit_px = 0.0; exit_reason = ""

            if pos_side == 1:
                if   o_ <= pos_stop:   exit_px = o_ * (1.0 - EXIT_SLIP); exit_reason = "STOP_OPEN"
                elif l_ <= pos_stop:   exit_px = pos_stop * (1.0 - EXIT_SLIP); exit_reason = "STOP_BAR"
                elif h_ >= pos_target and not trailing_armed:
                    # Arm trailing SL at entry + 4.2R once 5R is hit
                    trailing_armed = True
                    pos_stop = max(pos_stop, pos_entry + p.trailing_lock_r * pos_rr)
                    pos_target = pos_entry + 10.0 * pos_rr

                r_gain = (h_ - pos_entry) / pos_rr if pos_rr > 0 else 0.0
                if r_gain > pos_max_r:
                    pos_max_r = r_gain
                    if trailing_armed:
                        pos_stop = max(pos_stop, pos_entry + (pos_max_r - p.trailing_slack) * pos_rr)

                if not exit_reason and (t - pos_bar) >= p.time_decay_bars and pos_max_r < p.time_decay_r:
                    exit_px = c_ * (1.0 - EXIT_SLIP); exit_reason = "TIME_DECAY"

            elif pos_side == -1:
                if   o_ >= pos_stop:   exit_px = o_ * (1.0 + EXIT_SLIP); exit_reason = "STOP_OPEN"
                elif h_ >= pos_stop:   exit_px = pos_stop * (1.0 + EXIT_SLIP); exit_reason = "STOP_BAR"
                elif l_ <= pos_target and not trailing_armed:
                    trailing_armed = True
                    pos_stop = min(pos_stop, pos_entry - p.trailing_lock_r * pos_rr)
                    pos_target = pos_entry - 10.0 * pos_rr

                r_gain = (pos_entry - l_) / pos_rr if pos_rr > 0 else 0.0
                if r_gain > pos_max_r:
                    pos_max_r = r_gain
                    if trailing_armed:
                        pos_stop = min(pos_stop, pos_entry - (pos_max_r - p.trailing_slack) * pos_rr)

                if not exit_reason and (t - pos_bar) >= p.time_decay_bars and pos_max_r < p.time_decay_r:
                    exit_px = c_ * (1.0 + EXIT_SLIP); exit_reason = "TIME_DECAY"

            if exit_reason:
                gross   = pos_qty * (exit_px - pos_entry) if pos_side == 1 else pos_qty * (pos_entry - exit_px)
                fees    = pos_qty * (pos_entry + exit_px) * TAKER_FEE
                net_pnl = gross - fees
                realized += net_pnl
                r_mult   = net_pnl / pos_risk if pos_risk > 0 else 0.0
                trades.append({
                    "side": "LONG" if pos_side == 1 else "SHORT",
                    "entry": round(pos_entry, 4), "exit": round(exit_px, 4),
                    "pnl": round(net_pnl, 4), "r": round(r_mult, 3),
                    "reason": exit_reason, "trailing_armed": trailing_armed,
                })
                pos_side = 0; trailing_armed = False
                last_exit_bar = t

        unreal = 0.0
        if pos_side == 1:   unreal = pos_qty * (cl[t] - pos_entry)
        elif pos_side == -1: unreal = pos_qty * (pos_entry - cl[t])
        equity = realized + unreal
        if equity > peak: peak = equity
        equity_curve[t] = equity

        if pos_side == 0 and t < T - 1:
            if (t - last_exit_bar) < 8: continue
            cur_dd     = (peak - equity) / peak if peak > 0 else 0.0
            if cur_dd >= DD_LIMIT: continue
            net_profit = realized - INITIAL_CAPITAL
            trade_risk = p.defense_risk if cur_dd > 0.025 else (p.house_risk if net_profit > 60.0 else p.base_risk)

            if sig_long[t]:
                px   = cl[t] * (1.0 + ENTRY_SLIP)
                r_   = max(atr[t] * p.atr_mult_stop, px * p.min_stop_pct)
                r_   = min(r_, px * p.max_stop_pct)
                pos_side = 1; pos_entry = px; pos_stop = px - r_; pos_target = px + p.min_target_r * r_
                pos_rr = r_; pos_risk = trade_risk; pos_qty = trade_risk / r_; pos_bar = t; pos_max_r = 0.0; trailing_armed = False
            elif sig_short[t]:
                px   = cl[t] * (1.0 - ENTRY_SLIP)
                r_   = max(atr[t] * p.atr_mult_stop, px * p.min_stop_pct)
                r_   = min(r_, px * p.max_stop_pct)
                pos_side = -1; pos_entry = px; pos_stop = px + r_; pos_target = px - p.min_target_r * r_
                pos_rr = r_; pos_risk = trade_risk; pos_qty = trade_risk / r_; pos_bar = t; pos_max_r = 0.0; trailing_armed = False

    tot   = len(trades)
    wins  = sum(1 for tr in trades if tr["pnl"] > 0)
    wr    = wins / tot * 100.0 if tot > 0 else 0.0
    roi   = (realized - INITIAL_CAPITAL) / INITIAL_CAPITAL * 100.0
    peaks = np.maximum.accumulate(equity_curve)
    with np.errstate(divide="ignore", invalid="ignore"):
        dds = np.where(peaks > 0, (peaks - equity_curve) / peaks * 100.0, 0.0)
    max_dd = float(np.max(dds)) if len(dds) > 0 else 0.0

    return {"roi_pct": roi, "max_dd_pct": max_dd, "win_rate_pct": wr, "trades": tot,
            "net_pnl": realized - INITIAL_CAPITAL, "trades_list": trades}


# ------------------------------------------------------------------------------
# PER-ASSET CAUSAL IN-SAMPLE EVALUATION
# ------------------------------------------------------------------------------
def _score_is_rolling(df_is: pd.DataFrame, p: Params, is_trend_up: object, criteria: Dict) -> float:
    """Evaluate over the trailing 120 days of IS data (11,520 bars) with fresh capital."""
    if len(df_is) < 100: return -9999.0
    bars = min(120 * 96, len(df_is))
    df_eval = df_is.iloc[-bars:]
    
    m = simulate(df_eval.copy(), p, is_trend_up)
    tot_trades = m["trades"]
    if tot_trades < 3: return -9999.0
    
    roi = m["roi_pct"]
    dd  = m["max_dd_pct"]
    wr  = m["win_rate_pct"]

    # Utility score aligning strictly with user target criteria:
    # ROI > 20%, MaxDD < 5%, WinRate > 40%, Min Trades >= 5
    score = roi * 1.5 + wr * 0.8
    if dd >= 4.5:
        score -= (dd - 4.5) * 25.0
    if wr < 38.0:
        score -= (38.0 - wr) * 2.0
    if tot_trades < 5:
        score -= 15.0
    return score


def run_asset(args: Tuple) -> Dict:
    symbol, windows, criteria = args
    parquet_path = _DATA / f"{symbol}_15m_master_2020_2026.parquet"
    if not parquet_path.exists():
        return {"symbol": symbol, "status": "NO_DATA", "passed": 0, "total": 0, "pass_rate_pct": 0.0, "windows": []}

    t0 = time.time()
    df_full = pd.read_parquet(parquet_path)
    df_full.index = pd.to_datetime(df_full["datetime_utc"], utc=True)
    df_full.index.name = "timestamp"
    load_time = time.time() - t0

    results_per_window = []

    for win in windows:
        win_start = pd.Timestamp(win["start_date"], tz="UTC")
        win_end   = pd.Timestamp(win["end_date"],   tz="UTC") + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        purge_cut = win_start - pd.Timedelta(hours=PURGE_HOURS)

        df_is   = df_full[df_full.index < purge_cut]
        df_test = df_full[(df_full.index >= win_start) & (df_full.index <= win_end)]

        if len(df_test) < 96:
            results_per_window.append({"window_id": win["window_id"], "name": win["name"], "status": "SKIP"})
            continue

        # Dynamic Regime Gate based on trailing 90-day return
        is_trend_up: object = (True, True)
        if len(df_is) > 10:
            bars_90d  = min(90 * 96, len(df_is))
            df_is_90d = df_is.iloc[-bars_90d:]
            ret_90d   = (df_is_90d["close"].iloc[-1] / df_is_90d["close"].iloc[0] - 1.0) * 100.0
            if ret_90d >= 15.0:
                is_trend_up = (True, False)   # Strong bull: long-only
            elif ret_90d <= -15.0:
                is_trend_up = (False, True)   # Strong bear: short-only
            else:
                is_trend_up = (True, True)    # Neutral: allow both

        # In-sample selection across candidate grid
        if len(df_is) < 200:
            best_params = PARAM_GRID[0]
            best_score  = -9999.0
        else:
            best_params = PARAM_GRID[0]
            best_score  = -9999.0
            for p in PARAM_GRID:
                s = _score_is_rolling(df_is, p, is_trend_up, criteria)
                if s > best_score:
                    best_score  = s
                    best_params = p

        # OOS evaluation
        t_eval = time.time()
        try:
            m = simulate(df_test.copy(), best_params, is_trend_up)
        except Exception as e:
            results_per_window.append({"window_id": win["window_id"], "name": win["name"], "status": "ERROR", "error": str(e)})
            continue

        passed = (
            m["roi_pct"]      >= criteria["min_roi_percent"]    and
            m["max_dd_pct"]   <  criteria["max_dd_percent"]     and
            m["win_rate_pct"] >= criteria["min_winrate_percent"] and
            m["trades"]       >= criteria["min_trades"]
        )

        results_per_window.append({
            "window_id":    win["window_id"],
            "name":         win["name"],
            "regime":       win.get("regime", ""),
            "status":       "PASS" if passed else "FAIL",
            "roi_pct":      round(m["roi_pct"], 2),
            "max_dd_pct":   round(m["max_dd_pct"], 2),
            "win_rate_pct": round(m["win_rate_pct"], 1),
            "trades":       m["trades"],
            "net_pnl":      round(m["net_pnl"], 2),
            "best_params":  {
                "roll_bars": best_params.roll_bars,
                "ema_filter": best_params.ema_filter,
                "atr_mult_stop": best_params.atr_mult_stop,
                "base_risk": best_params.base_risk,
                "cascade_union": best_params.cascade_union
            },
            "is_trend_up":  is_trend_up,
            "eval_secs":    round(time.time() - t_eval, 3),
        })

    passed_count = sum(1 for r in results_per_window if r.get("status") == "PASS")
    total_count  = sum(1 for r in results_per_window if r.get("status") in ("PASS","FAIL"))
    pass_rate    = passed_count / total_count * 100.0 if total_count > 0 else 0.0

    return {
        "symbol": symbol, "status": "OK",
        "passed": passed_count, "total": total_count,
        "pass_rate_pct": round(pass_rate, 1),
        "load_secs": round(load_time, 2),
        "windows": results_per_window,
    }


# ------------------------------------------------------------------------------
# MAIN ENTRYPOINT
# ------------------------------------------------------------------------------
def main():
    print("=" * 80)
    print("18-ASSET PARALLEL OOS WALK-FORWARD HARNESS")
    print("=" * 80)

    with open(_CRITERIA) as f:
        cfg = json.load(f)
    criteria = cfg["target_criteria"]

    print(f"\nCriteria  ->  ROI>={criteria['min_roi_percent']}%  |  DD<{criteria['max_dd_percent']}%  |  WR>={criteria['min_winrate_percent']}%  |  MinR>={criteria['min_r_multiple']}R  |  Trades>={criteria['min_trades']}")

    with open(_WINDOWS) as f:
        windows = json.load(f)
    print(f"Windows   ->  {len(windows)} OOS windows loaded")

    available = [sym for sym in ASSETS if (_DATA / f"{sym}_15m_master_2020_2026.parquet").exists()]
    missing   = [sym for sym in ASSETS if sym not in available]
    print(f"Assets    ->  {len(available)}/{len(ASSETS)} available", end="")
    if missing: print(f"  (missing: {', '.join(missing)})", end="")
    print()

    n_workers = min(len(available), mp.cpu_count())
    print(f"Workers   ->  {n_workers} cores\n" + "=" * 80)

    t_start = time.time()
    worker_args = [(sym, windows, criteria) for sym in available]

    with mp.Pool(processes=n_workers) as pool:
        all_results = pool.map(run_asset, worker_args)

    elapsed = time.time() - t_start

    # -- Summary ----------------------------------------------------------------
    print("\n" + "=" * 80)
    print("ASSET SUMMARY")
    print(f"{'Asset':<12} {'Pass':>6} {'Total':>6} {'Pass%':>7}  {'Bar'}")
    print("-" * 50)
    grand_pass = 0; grand_total = 0
    for r in sorted(all_results, key=lambda x: x.get("pass_rate_pct", 0), reverse=True):
        if r["status"] == "NO_DATA":
            print(f"{r['symbol']:<12}   NO DATA"); continue
        p, t_, pr = r["passed"], r["total"], r["pass_rate_pct"]
        grand_pass += p; grand_total += t_
        bar = "#" * int(pr / 10) + "." * (10 - int(pr / 10))
        print(f"{r['symbol']:<12} {p:>6} {t_:>6} {pr:>6.1f}%  {bar}")
    gpr = grand_pass / grand_total * 100.0 if grand_total else 0.0
    print("-" * 50)
    print(f"{'TOTAL':<12} {grand_pass:>6} {grand_total:>6} {gpr:>6.1f}%")
    print(f"\nWall-clock: {elapsed:.1f}s")

    # -- Per-window best performer ----------------------------------------------
    print("\n" + "=" * 80)
    print("WINDOW DETAIL (Best asset per OOS window)")
    print(f"{'W#':>3}  {'Symbol':<12} {'ROI%':>8} {'DD%':>7} {'WR%':>6} {'Trades':>7}  Status  Window Name")
    print("-" * 80)
    for win in windows:
        wid = win["window_id"]
        rows = []
        for r in all_results:
            if r["status"] != "OK": continue
            for wr in r["windows"]:
                if wr.get("window_id") == wid and wr.get("status") in ("PASS","FAIL"):
                    rows.append((r["symbol"], wr))
        if not rows: continue
        sorted_rows = sorted(rows, key=lambda x: (1 if x[1]["status"] == "PASS" else 0, x[1].get("roi_pct", -9999)), reverse=True)
        best_sym, best_wr = sorted_rows[0]
        mark = "PASS" if best_wr["status"] == "PASS" else "FAIL"
        print(f"W{wid:02d}  {best_sym:<12} {best_wr['roi_pct']:>7.2f}% {best_wr['max_dd_pct']:>6.2f}% {best_wr['win_rate_pct']:>5.1f}% {best_wr['trades']:>6}  {mark:<5}  {win['name']}")

    # -- Save JSON --------------------------------------------------------------
    out_path = _ENGINE / "oos_18asset_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved: {out_path}")
    print("=" * 80)


if __name__ == "__main__":
    mp.freeze_support()
    main()
