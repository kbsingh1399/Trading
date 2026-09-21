"""
Engine/strategy/s4_pivot_footprint_exhaustion.py
================================================================================
STRUCTURAL PIVOT & FOOTPRINT DELTA EXHAUSTION STRATEGY (SLEEVE S4)
================================================================================
Transforms Footprint buyer/seller exhaustion at key liquidity pivots into a
systematic quantitative trading edge across 11 institutional crypto perpetuals.

Core Microstructure Principles:
1. Liquidity Sweeps at Causal Anchors (PDH/PDL, PWH/PWL, Session VAH/VAL).
2. Footprint Delta Absorption (Large volume flush absorbed by passive icebergs).
3. Convex 3-Stage Ratchet Execution (BE Lock @ +0.8R, Profit Lock @ +1.5R,
   Target @ +2.8R, Time-Decay Exit at 24 bars).
4. Strict Anti-Lookahead: Entry strictly at next-bar open (opens[j+1]).
================================================================================
"""
from __future__ import annotations

import json
import time
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numba import njit

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from Engine.core.canonical_indicators import (
    compute_structural_pivots_and_sweeps, apply_atr_floor)

DATA_DIR = REPO_ROOT / "binance_backtesting_data"
WINDOWS_PATH = REPO_ROOT / "Engine" / "oos_windows_20.json"
CRITERIA_PATH = REPO_ROOT / "Engine" / "target_oos_criteria.json"
ARTIFACT_DIR = REPO_ROOT / "reports" / "s4_exhaustion"  # OX66: repo-relative (was a Windows user path)

CAPITAL = 5000.0
BASE_RISK_USD = 36.0  # OX66: terminal parity (was 38.0)
MAX_CONCURRENT = 3  # OX66: terminal parity (was 2)
DD_STOP_PCT = 4.85
FRICTION_R = 0.18

CORE_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT",
    "ADAUSDT", "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT"
]

COLS_TO_LOAD = [
    "open_time_ms", "open", "high", "low", "close",
    "atr_14", "vwap_zscore", "long_liq_zs", "short_liq_zs",
    "zc_div", "volume_base", "volume_ratio", "ema_200",
    "session_vah", "session_val", "future_cvd_15m"
]

@njit(fastmath=True)
def label_exhaustion_trades_numba(
    c: np.ndarray,
    h: np.ndarray,
    lo: np.ndarray,
    o: np.ndarray,
    atr: np.ndarray,
    long_cond: np.ndarray,
    short_cond: np.ndarray,
    horizon_bars: int = 24,
    target_r: float = 2.8,
    stop_r: float = 1.0,
    be_trigger_r: float = 0.80,
    be_lock_r: float = 0.20,
    profit_trigger_r: float = 1.50,
    profit_lock_r: float = 0.80,
    trail_trigger_r: float = 2.00,
    trail_lock_r: float = 1.50,
    friction_r: float = 0.18,
):
    """Lightning-fast Numba 3-stage microstructure ratchet simulator."""
    n = len(c)
    is_cand = np.zeros(n, dtype=np.bool_)
    side = np.zeros(n, dtype=np.int8)
    realized_r = np.zeros(n, dtype=np.float64)
    bars_held = np.zeros(n, dtype=np.int16)

    for i in range(n - horizon_bars - 1):
        s = 0
        if long_cond[i]:
            s = 1
        elif short_cond[i]:
            s = -1
        else:
            continue

        is_cand[i] = True
        side[i] = s
        entry_p = o[i + 1]  # OX66 FIX (was c[i+1] = next-CLOSE lookahead): next-bar OPEN
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

            # Check stop loss hit
            if adverse_r <= cur_stop_r:
                exit_r = cur_stop_r
                hit = True
                hold_count = j - i
                break

            # Check target profit hit
            if favorable_r >= target_r:
                exit_r = target_r
                hit = True
                hold_count = j - i
                break

            # Ratchet arming
            if favorable_r >= trail_trigger_r:
                if trail_lock_r > cur_stop_r:
                    cur_stop_r = trail_lock_r
            elif favorable_r >= profit_trigger_r:
                if profit_lock_r > cur_stop_r:
                    cur_stop_r = profit_lock_r
            elif favorable_r >= be_trigger_r:
                if be_lock_r > cur_stop_r:
                    cur_stop_r = be_lock_r

            # Time decay at bar 24: exit if < +0.20R
            if (j - i) == 24:
                cur_r = (c[j] - entry_p) / dist if s == 1 else (entry_p - c[j]) / dist
                if cur_r < 0.20:
                    exit_r = cur_r
                    hit = True
                    hold_count = 24
                    break

        if not hit:
            exit_p = c[i + horizon_bars]
            exit_r = (exit_p - entry_p) / dist if s == 1 else (entry_p - exit_p) / dist
            hold_count = horizon_bars

        net_r = exit_r - friction_r
        realized_r[i] = net_r
        bars_held[i] = hold_count

    return is_cand, side, realized_r, bars_held


@njit(fastmath=True)
def simulate_portfolio_numba(
    event_times: np.ndarray,
    event_r_gains: np.ndarray,
    event_risks: np.ndarray,
    event_hold_ms: np.ndarray,
    event_syms: np.ndarray,
    capital: float = 5000.0,
    max_concurrent: int = 2,
    dd_stop_pct: float = 4.85,
    milestone_pnl: float = 500.0
):
    n = len(event_times)
    equity = capital
    peak_equity = capital
    max_dd_pct = 0.0

    pos_active = np.zeros(max_concurrent, dtype=np.bool_)
    pos_end_times = np.zeros(max_concurrent, dtype=np.int64)
    pos_syms = np.full(max_concurrent, -1, dtype=np.int64)

    tr_count = 0
    win_count = 0
    locked = False

    trade_pnls = np.zeros(n, dtype=np.float64)
    equity_curve = np.zeros(n + 1, dtype=np.float64)
    equity_times = np.zeros(n + 1, dtype=np.int64)
    equity_curve[0] = capital
    equity_times[0] = event_times[0] if n > 0 else 0

    for i in range(n):
        t = event_times[i]
        r = event_r_gains[i]
        base_r = event_risks[i]
        hold = event_hold_ms[i]
        sym = event_syms[i]

        for p in range(max_concurrent):
            if pos_active[p] and t >= pos_end_times[p]:
                pos_active[p] = False
                pos_syms[p] = -1

        if locked or max_dd_pct >= dd_stop_pct:
            locked = True
            continue

        active_count = 0
        slot = -1
        sym_already = False
        for p in range(max_concurrent):
            if pos_active[p]:
                active_count += 1
                if pos_syms[p] == sym:
                    sym_already = True
            elif slot == -1:
                slot = p

        if active_count >= max_concurrent or slot == -1 or sym_already:
            continue

        # Milestone lock
        if (peak_equity - capital) >= milestone_pnl and tr_count >= 15:
            floor_stop = max(capital + milestone_pnl, peak_equity - 120.0)
            if equity <= floor_stop:
                locked = True
                continue

        # Risk budget
        cur_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
        cur_profit = equity - capital
        is_milestone = (peak_equity - capital) >= milestone_pnl

        if is_milestone:
            cushion = max(0.0, equity - (capital + milestone_pnl))
            trade_risk = min(10.0, cushion * 0.20)  # OX66: terminal parity
            if trade_risk <= 0.0:
                locked = True
                continue
        elif cur_dd >= 2.0 or cur_profit < -50.0:
            trade_risk = min(base_r * 0.40, 14.0)  # OX66: terminal parity
        elif cur_profit >= 120.0:
            trade_risk = min(base_r * 1.35, 48.0)  # OX66: terminal parity
        else:
            trade_risk = min(base_r, 36.0)
        if (not is_milestone) and max_dd_pct >= 1.80:  # OX66: DD contraction parity
            trade_risk = trade_risk * 0.5

        pos_active[slot] = True
        pos_end_times[slot] = t + hold
        pos_syms[slot] = sym

        pnl = r * trade_risk
        equity += pnl
        if equity > peak_equity:
            peak_equity = equity
        dd = ((peak_equity - equity) / peak_equity) * 100.0
        if dd > max_dd_pct:
            max_dd_pct = dd

        trade_pnls[tr_count] = pnl
        tr_count += 1
        if r > 0:
            win_count += 1

        equity_curve[tr_count] = equity
        equity_times[tr_count] = t

    return equity - capital, max_dd_pct, tr_count, win_count, equity_curve[:tr_count+1], equity_times[:tr_count+1]


def build_exhaustion_dataset() -> pd.DataFrame:
    frames = []
    print("Building Structural Pivot & Footprint Exhaustion Dataset across 11 assets...")
    t0 = time.perf_counter()

    for sym in CORE_SYMBOLS:
        p_path = DATA_DIR / f"{sym}_15m_master_2020_2026.parquet"
        if not p_path.exists():
            continue
        df = pd.read_parquet(p_path, columns=COLS_TO_LOAD)
        c = df.close.to_numpy(float)
        h = df.high.to_numpy(float)
        lo = df.low.to_numpy(float)
        op = df.open.to_numpy(float)
        t = df.open_time_ms.to_numpy(np.int64)

        atr_raw = df["atr_14"].fillna(df["close"] * 0.01).to_numpy(float)
        atr = apply_atr_floor(atr_raw, df["close"].to_numpy(float))  # OX66 unified R

        e200 = df["ema_200"].to_numpy(float)
        vwap_z = df["vwap_zscore"].fillna(0.0).to_numpy(float)
        vol_ratio = df["volume_ratio"].fillna(1.0).to_numpy(float)
        vol_base = df["volume_base"].replace(0, 1.0)
        zc_norm = (df["zc_div"] / vol_base).clip(-3.0, 3.0).fillna(0.0).to_numpy(float)
        long_liq = df["long_liq_zs"].fillna(0.0).to_numpy(float)
        short_liq = df["short_liq_zs"].fillna(0.0).to_numpy(float)
        s_val = df["session_val"].fillna(df["low"]).to_numpy(float)
        s_vah = df["session_vah"].fillna(df["high"]).to_numpy(float)
        fut_delta = df["future_cvd_15m"].fillna(0.0).to_numpy(float)

        # 1. Structural Pivots
        (
            pdh, pdl, pwh, pwl, pmh, pml,
            pdl_dist, pdh_dist, pwl_dist, pwh_dist,
            pdl_sweep_bull, pdh_sweep_bear
        ) = compute_structural_pivots_and_sweeps(t, h, lo, c, fut_delta, vol_base, vol_ratio, atr)

        # 2. Causal Volatility Shock Filter
        ret = np.diff(np.log(np.maximum(c, 1e-9)), prepend=0.0)
        rv_96 = pd.Series(ret).rolling(96, min_periods=8).std().fillna(0.0).to_numpy(float)
        rv_rank = pd.Series(rv_96).rolling(384, min_periods=32).rank(pct=True).fillna(0.5).to_numpy(float)
        is_shock = rv_rank >= 0.88

        # 3. Seller Exhaustion at Lower Pivots (Bullish Reversal Setup):
        # - Price pierces PDL or session VAL
        # - Lower wick rejection >= 35% of total bar range
        # - Closes back above PDL/VAL
        # - Footprint CVD delta > 0 OR Spot-Futures Divergence zc_norm > 0.4
        # - Macro filter: c > e200 OR vwap_z < -0.8
        tot_range = np.maximum(h - lo, 1e-6)
        lower_wick = np.minimum(op, c) - lo
        is_lower_wick = (lower_wick / tot_range) >= 0.35

        seller_exhaustion = (
            ((lo < pdl) & (c > pdl)) | ((lo < s_val) & (c > s_val))
        ) & is_lower_wick & ((fut_delta > 0) | (zc_norm > 0.4)) & ((c > e200) | (vwap_z < -0.8)) & (~is_shock)

        # 4. Buyer Exhaustion at Upper Pivots (Bearish Reversal Setup):
        # - Price pierces PDH or session VAH
        # - Upper wick rejection >= 35% of total bar range
        # - Closes back below PDH/VAH
        # - Footprint CVD delta < 0
        # - Macro filter: c < e200 OR vwap_z > 0.8, veto if active short squeeze
        upper_wick = h - np.maximum(op, c)
        is_upper_wick = (upper_wick / tot_range) >= 0.35

        buyer_exhaustion = (
            ((h > pdh) & (c < pdh)) | ((h > s_vah) & (c < s_vah))
        ) & is_upper_wick & (fut_delta < 0) & ((c < e200) | (vwap_z > 0.8)) & (short_liq < 0.8) & (~is_shock)

        long_cond = seller_exhaustion & np.isfinite(atr) & (atr > 0)
        short_cond = buyer_exhaustion & np.isfinite(atr) & (atr > 0)
        long_cond = (long_cond & (~short_cond)).astype(bool)
        short_cond = (short_cond & (~long_cond)).astype(bool)

        is_cand, side, real_r, b_held = label_exhaustion_trades_numba(
            c, h, lo, op, atr, long_cond, short_cond, 24, 2.8, 1.0,
            be_trigger_r=0.80, be_lock_r=0.20,
            profit_trigger_r=1.50, profit_lock_r=0.80,
            trail_trigger_r=2.00, trail_lock_r=1.50,
            friction_r=FRICTION_R
        )

        cand_idx = np.where(is_cand)[0]
        f_sub = pd.DataFrame({
            "open_time_ms": t[cand_idx + 1],  # Next-bar open execution!
            "close": c[cand_idx + 1],
            "realized_r": real_r[cand_idx],
            "bars_held": b_held[cand_idx],
            "signal_side": side[cand_idx],
            "symbol": sym
        })
        frames.append(f_sub)

    pool = pd.concat(frames, ignore_index=True)
    pool.sort_values("open_time_ms", inplace=True)
    pool.reset_index(drop=True, inplace=True)
    print(f"Compiled {len(pool):,d} high-conviction exhaustion setups in {time.perf_counter() - t0:.2f}s!")
    return pool


def run_strategy_benchmark():
    t_start = time.perf_counter()
    pool = build_exhaustion_dataset()

    core_syms = sorted(pool["symbol"].unique())
    sym_map = {s: i for i, s in enumerate(core_syms)}
    pool["sym_id"] = pool["symbol"].map(sym_map)

    with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
        windows = json.load(f)

    results = []
    passing_windows = 0
    profitable_windows = 0

    print("\n" + "=" * 115)
    print("STRUCTURAL PIVOT FOOTPRINT EXHAUSTION STRATEGY (23 OOS WINDOWS, 2021-2026)")
    print("=" * 115)
    print(f"{'W#':<3} | {'Window Name':<38} | {'Trades':<7} | {'Win Rate':<8} | {'Net PnL':<11} | {'Net ROI':<9} | {'Max DD':<7} | {'Status':<6}")
    print("-" * 115)

    all_strat_curves = []
    total_strat_pnl = 0.0

    for w in windows:
        w_id = w["window_id"]
        w_name = w["name"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000

        sub = pool[(pool["open_time_ms"] >= start_ms) & (pool["open_time_ms"] <= end_ms)]
        if len(sub) == 0:
            continue

        pnl, dd, tr, win, eq_curve, eq_times = simulate_portfolio_numba(
            sub["open_time_ms"].to_numpy(np.int64),
            sub["realized_r"].to_numpy(np.float64),
            np.full(len(sub), BASE_RISK_USD, dtype=np.float64),
            (sub["bars_held"].to_numpy(np.int64) * 15 * 60 * 1000),
            sub["sym_id"].to_numpy(np.int64),
            capital=CAPITAL, max_concurrent=MAX_CONCURRENT, dd_stop_pct=DD_STOP_PCT, milestone_pnl=500.0
        )

        roi = (pnl / CAPITAL) * 100.0
        wr = (win / tr * 100.0) if tr > 0 else 0.0
        is_pass = (roi >= 10.0) and (dd <= 5.0) and (wr >= 40.0) and (tr >= 15)
        status = "PASS" if is_pass else ("PROFIT" if pnl > 0 and dd <= 5.0 else "FAIL")

        if is_pass:
            passing_windows += 1
        if pnl > 0 and dd <= 5.0:
            profitable_windows += 1

        total_strat_pnl += pnl

        print(f"W{w_id:02d} | {w_name[:38]:<38} | {tr:<7d} | {wr:>5.1f}%   | {pnl:>+8.2f} USD | {roi:>+7.2f}%  | {dd:>5.2f}% | {status:<6}")
        results.append({
            "window_id": w_id, "name": w_name, "trades": tr, "win_rate": wr,
            "pnl": pnl, "roi": roi, "dd": dd, "status": status
        })

    res_df = pd.DataFrame(results)

    # -------------------------------------------------------------------------
    # Full Portfolio Backtest & Benchmark Comparison against BTC Buy & Hold
    # -------------------------------------------------------------------------
    pnl_full, dd_full, tr_full, win_full, eq_curve_full, eq_times_full = simulate_portfolio_numba(
        pool["open_time_ms"].to_numpy(np.int64),
        pool["realized_r"].to_numpy(np.float64),
        np.full(len(pool), BASE_RISK_USD, dtype=np.float64),
        (pool["bars_held"].to_numpy(np.int64) * 15 * 60 * 1000),
        pool["sym_id"].to_numpy(np.int64),
        capital=CAPITAL, max_concurrent=MAX_CONCURRENT, dd_stop_pct=DD_STOP_PCT, milestone_pnl=999999.0
    )

    # Load BTC Master Data for Buy & Hold Benchmark
    btc_path = DATA_DIR / "BTCUSDT_15m_master_2020_2026.parquet"
    btc_df = pd.read_parquet(btc_path, columns=["open_time_ms", "close"])
    b_t = btc_df["open_time_ms"].to_numpy(np.int64)
    b_c = btc_df["close"].to_numpy(np.float64)

    # Align starting point
    t_start_sim = eq_times_full[0]
    b_mask = b_t >= t_start_sim
    b_t_sim = b_t[b_mask]
    b_c_sim = b_c[b_mask]
    btc_equity = (b_c_sim / b_c_sim[0]) * CAPITAL
    btc_peak = np.maximum.accumulate(btc_equity)
    btc_dd = ((btc_peak - btc_equity) / btc_peak) * 100.0

    strat_df = pd.DataFrame({"time_ms": eq_times_full, "strat_equity": eq_curve_full}).drop_duplicates("time_ms")
    aligned = pd.merge_asof(
        pd.DataFrame({"time_ms": b_t_sim, "btc_equity": btc_equity, "btc_dd": btc_dd}),
        strat_df,
        on="time_ms",
        direction="backward"
    ).ffill()

    aligned["strat_peak"] = np.maximum.accumulate(aligned["strat_equity"])
    aligned["strat_dd"] = ((aligned["strat_peak"] - aligned["strat_equity"]) / aligned["strat_peak"]) * 100.0
    aligned["datetime"] = pd.to_datetime(aligned["time_ms"], unit="ms", utc=True)

    # Plot Visual Equity Curve & Drawdown Chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), gridspec_kw={"height_ratios": [2.2, 1.0]}, sharex=True)
    plt.style.use("seaborn-v0_8-darkgrid" if "seaborn-v0_8-darkgrid" in plt.style.available else "default")

    ax1.plot(aligned["datetime"], aligned["strat_equity"], label="S4 Pivot Footprint Exhaustion Strategy", color="#00C853", linewidth=2.0)
    ax1.plot(aligned["datetime"], aligned["btc_equity"], label="BTC Buy & Hold Benchmark (Normalized to 5,000 USD)", color="#FFA000", linewidth=1.5, linestyle="--")
    ax1.set_title("Institutional Sleeve S4: Pivot Footprint Exhaustion vs BTC Benchmark (2020-2026)", fontsize=14, fontweight="bold", pad=12)
    ax1.set_ylabel("Portfolio Value (USD)", fontsize=11, fontweight="bold")
    ax1.legend(loc="upper left", frameon=True, fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.6)

    ax2.plot(aligned["datetime"], -aligned["strat_dd"], label="Strategy Drawdown (%)", color="#D50000", linewidth=1.5)
    ax2.plot(aligned["datetime"], -aligned["btc_dd"], label="BTC Buy & Hold Drawdown (%)", color="#757575", linewidth=1.2, linestyle="--", alpha=0.7)
    ax2.set_ylabel("Underwater Drawdown (%)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Date (UTC)", fontsize=11, fontweight="bold")
    ax2.axhline(0, color="black", linestyle="-", linewidth=0.8)
    ax2.axhline(-DD_STOP_PCT, color="red", linestyle=":", label="Hard DD Stop (4.85%)")
    ax2.legend(loc="lower left", frameon=True, fontsize=9)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    chart_path = ARTIFACT_DIR / "pivot_footprint_exhaustion_equity_vs_benchmark.png"
    plt.savefig(chart_path, dpi=180)
    plt.close()
    print(f"\nEquity Curve Chart saved successfully to: {chart_path}")

    print("\n" + "=" * 115)
    print("STRATEGY PERFORMANCE SUMMARY (11 ASSETS, 2020-2026)")
    print("=" * 115)
    print(f"Total Cumulative Trades       : {tr_full:,d} trades (~{tr_full / 23:.1f} trades / quarter)")
    print(f"Overall Win Rate              : {win_full / tr_full * 100:.2f}%")
    print(f"Total Net PnL                 : {pnl_full:>+10.2f} USD")
    print(f"Total Strategy Net ROI        : {(pnl_full / CAPITAL) * 100:>+10.2f}%")
    print(f"Max Peak-to-Trough Drawdown   : {aligned['strat_dd'].max():.2f}% (vs BTC Max DD: {aligned['btc_dd'].max():.2f}%)")
    print(f"Passing Windows (Outright)    : {passing_windows} / 23")
    print(f"Profitable Windows (PnL > 0)  : {profitable_windows} / 23")
    print(f"Execution Time                : {time.perf_counter() - t_start:.2f} seconds")
    print("=" * 115)


if __name__ == "__main__":
    run_strategy_benchmark()
