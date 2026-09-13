"""
Tuned search for 10% monthly ROI, DD <5%, TP >=3R
Focus on composite ensemble with parameter grid search
"""

import os, sys, json, itertools
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig
from Engine.core.portfolio_execution_kernel import PortfolioExecutionKernel

DATA_DIR = os.path.join(SCRIPT_DIR, "binance_backtesting_data")
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT",
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT",
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT",
]

WINDOWS = [
    ("W15", "2024-03-01", "2024-03-31"),
    ("W17", "2024-11-01", "2024-11-30"),
    ("W19", "2025-07-01", "2025-07-31"),
    ("W20", "2026-03-01", "2026-03-31"),
    ("W10", "2023-03-01", "2023-03-31"),
    ("W14", "2024-01-01", "2024-01-31"),
]

def load_data():
    per_symbol = {}
    for sym in SYMBOLS:
        path = os.path.join(DATA_DIR, f"{sym}_15m_master_2020_2026.parquet")
        if not os.path.exists(path):
            continue
        df = pd.read_parquet(path)
        df["datetime_utc"] = pd.to_datetime(df["datetime_utc"])
        df = df.set_index("datetime_utc").sort_index()
        df = df[~df.index.duplicated(keep='last')]
        per_symbol[sym] = df
    return per_symbol

def load_ladder(per_symbol, max_sym=5):
    cache_dir = os.path.join(DATA_DIR, "ladder_cache")
    os.makedirs(cache_dir, exist_ok=True)
    ladder = {}
    for sym in SYMBOLS[:max_sym]:
        cache_path = os.path.join(cache_dir, f"{sym}_footprint_agg.parquet")
        if os.path.exists(cache_path):
            try:
                agg = pd.read_parquet(cache_path)
                agg.index = pd.to_datetime(agg.index)
                ladder[sym] = agg
                continue
            except:
                pass
        # skip if not cached for speed
    return ladder

def _rolling_z(s, w=96):
    m = s.rolling(w, min_periods=20).mean()
    sd = s.rolling(w, min_periods=20).std(ddof=0).replace(0, np.nan)
    return ((s - m) / sd).fillna(0.0)

def generate_signals(per_symbol, ladder, params):
    """
    params: dict with thresholds
    """
    out = {}
    btc = per_symbol.get("BTCUSDT")
    btc_uptrend = None
    if btc is not None:
        btc_ema50 = btc["ema_50"].fillna(btc["close"])
        btc_ema200 = btc["ema_200"].fillna(btc["close"])
        btc_uptrend = (btc_ema50 > btc_ema200)

    for sym, df in per_symbol.items():
        atr = df["atr_14"].fillna(df["close"]*0.02)
        roll_low_20 = df["low"].rolling(20, min_periods=10).min().shift(1)
        roll_high_20 = df["high"].rolling(20, min_periods=10).max().shift(1)
        sweep_low = (df["low"] < roll_low_20) & (df["close"] > roll_low_20)
        sweep_high = (df["high"] > roll_high_20) & (df["close"] < roll_high_20)

        if sym in ladder:
            lf = ladder[sym].reindex(df.index).fillna(0)
            stacked_buy = lf.get("stacked_buy", pd.Series(0, index=df.index))
            stacked_sell = lf.get("stacked_sell", pd.Series(0, index=df.index))
            delta_ratio = lf.get("delta_ratio", pd.Series(0, index=df.index))
            poc_pos = lf.get("poc_pos", pd.Series(0.5, index=df.index))
        else:
            stacked_buy = pd.Series(0, index=df.index)
            stacked_sell = pd.Series(0, index=df.index)
            delta_ratio = pd.Series(0, index=df.index)
            poc_pos = pd.Series(0.5, index=df.index)

        long_liq = df["long_liq_zs"].fillna(0)
        short_liq = df["short_liq_zs"].fillna(0)
        zc_div = df["zc_div"].fillna(0)
        vwap_z = df["vwap_zscore"].fillna(0)
        rsi = df["rsi_14"].fillna(50)
        spot_cvd = df["spot_cvd_15m"].fillna(0)
        fut_cvd = df["future_cvd_15m"].fillna(0)
        vol_ratio = df["volume_ratio"].fillna(1)
        taker_ratio = df["taker_volume_ratio"].fillna(1)
        funding = df["funding_rate_pct"].fillna(0)
        basis = df["basis_usd"].fillna(0)

        # params
        liq_thr = params.get("liq_thr", 1.2)
        zc_thr = params.get("zc_thr", 0.5)
        vwap_thr = params.get("vwap_thr", 0.0)
        rsi_thr = params.get("rsi_thr", 52)
        stacked_thr = params.get("stacked_thr", 1)
        delta_thr = params.get("delta_thr", 0.12)
        opt_score_thr = params.get("opt_score_thr", 3)
        vol_thr = params.get("vol_thr", 1.2)

        if btc_uptrend is not None:
            btc_trend_aligned = btc_uptrend.reindex(df.index, method='ffill').fillna(True)
            btc_liq_aligned = btc["long_liq_zs"].fillna(0).reindex(df.index, method='ffill').fillna(0)
        else:
            btc_trend_aligned = pd.Series(True, index=df.index)
            btc_liq_aligned = pd.Series(0, index=df.index)

        liq_decel = long_liq.diff() < -0.3

        mandatory = (
            (long_liq > liq_thr) &
            (zc_div > zc_thr) &
            (spot_cvd > 0) &
            (vwap_z < vwap_thr) &
            (rsi < rsi_thr) &
            (sweep_low | (df["low"] <= roll_low_20*1.001))
        )

        optional_score = (
            (stacked_buy >= stacked_thr).astype(int) +
            (delta_ratio > delta_thr).astype(int) +
            (vol_ratio > vol_thr).astype(int) +
            (funding < 0.01).astype(int) +
            (basis < 0).astype(int) +
            (taker_ratio > 1.05).astype(int) +
            (btc_trend_aligned).astype(int) +
            (btc_liq_aligned > 1.0).astype(int) +
            (poc_pos < 0.4).astype(int) +
            (liq_decel).astype(int)
        )

        long_cond = mandatory & (optional_score >= opt_score_thr)

        # Short
        short_mandatory = (
            (short_liq > liq_thr) &
            (zc_div < -zc_thr) &
            (spot_cvd < 0) &
            (vwap_z > -vwap_thr) &
            (rsi > 100 - rsi_thr)
        )
        short_cond = short_mandatory & sweep_high & (stacked_sell >= stacked_thr)

        side = np.where(long_cond, 1, np.where(short_cond, -1, 0))

        # Stop distance
        atr_mult = params.get("atr_mult", 0.9)
        min_stop_pct = params.get("min_stop_pct", 0.012)
        max_stop_pct = params.get("max_stop_pct", 0.035)
        raw_r = (atr * atr_mult).values
        min_stop = df["close"].values * min_stop_pct
        max_stop = df["close"].values * max_stop_pct
        raw_r = np.clip(raw_r, min_stop, max_stop)

        out[sym] = pd.DataFrame({"side": side, "raw_r": raw_r}, index=df.index)

    return out

def slice_window(per_symbol, start, end):
    ws = pd.Timestamp(start)
    we = pd.Timestamp(end) + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
    out = {}
    for sym, df in per_symbol.items():
        sl = df.loc[ws:we]
        if len(sl) > 100:
            out[sym] = sl
    return out

def evaluate(per_symbol_full, ladder_full, start, end, params, risk_cfg, ratchet_cfg):
    per_symbol = slice_window(per_symbol_full, start, end)
    if not per_symbol:
        return {"roi_pct": 0, "max_dd_pct": 0, "trades": 0, "win_rate_pct": 0, "net_pnl": 0}

    ladder_sliced = {}
    for sym, lf in ladder_full.items():
        if sym in per_symbol:
            sl = lf.loc[pd.Timestamp(start): pd.Timestamp(end) + pd.Timedelta(days=1)]
            ladder_sliced[sym] = sl

    signals = generate_signals(per_symbol, ladder_sliced, params)

    # align signals
    gated = {}
    for sym in per_symbol.keys():
        if sym in signals:
            s = signals[sym]
            s_aligned = s.reindex(per_symbol[sym].index).fillna({"side": 0, "raw_r": per_symbol[sym]["atr_14"].fillna(per_symbol[sym]["close"]*0.02)})
            s_aligned["side"] = s_aligned["side"].astype(int)
            gated[sym] = s_aligned
        else:
            gated[sym] = pd.DataFrame({"side": np.zeros(len(per_symbol[sym]), dtype=int),
                                       "raw_r": per_symbol[sym]["atr_14"].fillna(per_symbol[sym]["close"]*0.02).values},
                                      index=per_symbol[sym].index)

    kernel = PortfolioExecutionKernel(
        symbols=list(per_symbol.keys()),
        risk=risk_cfg,
        fric=FrictionConfig(),
        ratchet=ratchet_cfg,
        max_positions=2,
        dd_defense_thresh=0.025,
        dd_entry_buffer=0.038
    )
    result = kernel.run(per_symbol, gated, training_mode=False)
    return result

def main():
    print("Loading data...")
    per_symbol_full = load_data()
    ladder_full = load_ladder(per_symbol_full, max_sym=5)

    risk_cfg = RiskConfig(initial_capital=5000.0, base_risk=50.0, house_money_risk=100.0,
                          drawdown_defense_risk=15.0, drawdown_limit=0.05)

    ratchet_cfgs = [
        RatchetConfig(arm0_r=0.8, lock0_r=0.15, arm1_r=1.5, lock1_r=0.8, arm2_r=2.5, lock2_r=1.5, min_target_r=3.0, time_decay_bars=48, time_decay_r=0.10),
        RatchetConfig(arm0_r=1.0, lock0_r=0.30, arm1_r=2.0, lock1_r=1.0, arm2_r=3.0, lock2_r=2.0, min_target_r=3.5, time_decay_bars=48, time_decay_r=0.10),
        RatchetConfig(arm0_r=1.0, lock0_r=0.20, arm1_r=2.0, lock1_r=1.0, arm2_r=3.0, lock2_r=2.0, min_target_r=4.0, time_decay_bars=64, time_decay_r=0.05),
        RatchetConfig(arm0_r=0.8, lock0_r=0.20, arm1_r=1.5, lock1_r=0.80, arm2_r=2.5, lock2_r=1.80, min_target_r=5.0, time_decay_bars=96, time_decay_r=0.0),
    ]

    # Parameter grid
    param_grid = [
        {"liq_thr": 0.8, "zc_thr": 0.3, "vwap_thr": 0.2, "rsi_thr": 55, "stacked_thr": 0, "delta_thr": 0.05, "opt_score_thr": 2, "vol_thr": 0.9, "atr_mult": 0.7, "min_stop_pct": 0.008, "max_stop_pct": 0.025},
        {"liq_thr": 1.0, "zc_thr": 0.4, "vwap_thr": 0.0, "rsi_thr": 52, "stacked_thr": 1, "delta_thr": 0.08, "opt_score_thr": 2, "vol_thr": 1.0, "atr_mult": 0.8, "min_stop_pct": 0.010, "max_stop_pct": 0.030},
        {"liq_thr": 1.2, "zc_thr": 0.5, "vwap_thr": 0.0, "rsi_thr": 50, "stacked_thr": 1, "delta_thr": 0.10, "opt_score_thr": 3, "vol_thr": 1.2, "atr_mult": 0.9, "min_stop_pct": 0.012, "max_stop_pct": 0.035},
        {"liq_thr": 0.8, "zc_thr": 0.3, "vwap_thr": 0.3, "rsi_thr": 60, "stacked_thr": 0, "delta_thr": 0.05, "opt_score_thr": 1, "vol_thr": 0.8, "atr_mult": 0.6, "min_stop_pct": 0.008, "max_stop_pct": 0.020},
        {"liq_thr": 1.0, "zc_thr": 0.3, "vwap_thr": 0.5, "rsi_thr": 60, "stacked_thr": 0, "delta_thr": 0.05, "opt_score_thr": 2, "vol_thr": 0.9, "atr_mult": 0.8, "min_stop_pct": 0.010, "max_stop_pct": 0.025},
        {"liq_thr": 0.5, "zc_thr": 0.2, "vwap_thr": 0.5, "rsi_thr": 65, "stacked_thr": 0, "delta_thr": 0.0, "opt_score_thr": 1, "vol_thr": 0.8, "atr_mult": 0.7, "min_stop_pct": 0.008, "max_stop_pct": 0.020},
        {"liq_thr": 1.5, "zc_thr": 0.6, "vwap_thr": -0.2, "rsi_thr": 48, "stacked_thr": 1, "delta_thr": 0.12, "opt_score_thr": 3, "vol_thr": 1.3, "atr_mult": 1.0, "min_stop_pct": 0.015, "max_stop_pct": 0.035},
        {"liq_thr": 0.8, "zc_thr": 0.2, "vwap_thr": 0.5, "rsi_thr": 55, "stacked_thr": 0, "delta_thr": 0.05, "opt_score_thr": 2, "vol_thr": 1.0, "atr_mult": 0.9, "min_stop_pct": 0.010, "max_stop_pct": 0.030},
        {"liq_thr": 1.0, "zc_thr": 0.5, "vwap_thr": 0.2, "rsi_thr": 55, "stacked_thr": 0, "delta_thr": 0.08, "opt_score_thr": 2, "vol_thr": 1.0, "atr_mult": 0.8, "min_stop_pct": 0.012, "max_stop_pct": 0.030},
        {"liq_thr": 0.8, "zc_thr": 0.4, "vwap_thr": 0.0, "rsi_thr": 52, "stacked_thr": 1, "delta_thr": 0.10, "opt_score_thr": 2, "vol_thr": 1.1, "atr_mult": 0.8, "min_stop_pct": 0.010, "max_stop_pct": 0.025},
    ]

    best = None
    all_results = []

    for ratchet in ratchet_cfgs:
        for params in param_grid:
            print(f"\n=== Testing TP {ratchet.min_target_r}R params {params} ===")
            for wid, ws, we in WINDOWS:
                res = evaluate(per_symbol_full, ladder_full, ws, we, params, risk_cfg, ratchet)
                print(f"  {wid} ROI {res['roi_pct']:.2f}% DD {res['max_dd_pct']:.2f}% Trades {res['trades']} WR {res['win_rate_pct']:.1f}%")
                entry = {"window": wid, "roi": res["roi_pct"], "dd": res["max_dd_pct"], "trades": res["trades"], "wr": res["win_rate_pct"], "tp": ratchet.min_target_r, "params": params}
                all_results.append(entry)
                if res["roi_pct"] > 10.0 and res["max_dd_pct"] < 5.0 and res["trades"] >= 10 and ratchet.min_target_r >= 3.0:
                    print(f"*** FOUND WINNER: {wid} ROI {res['roi_pct']:.2f}% DD {res['max_dd_pct']:.2f}% TP {ratchet.min_target_r}R ***")
                    if best is None or res["roi_pct"] > best["roi_pct"]:
                        best = {"window": wid, "roi_pct": res["roi_pct"], "max_dd_pct": res["max_dd_pct"], "trades": res["trades"], "win_rate": res["win_rate_pct"], "tp_r": ratchet.min_target_r, "params": params, "result": res}
                        # Save
                        with open(os.path.join(SCRIPT_DIR, "tuned_best.json"), "w") as f:
                            json.dump(best, f, indent=2, default=str)
                    # If we have found at least one winner, we can try to optimize further for that window
                    # But continue searching for higher ROI

    print("\n=== Search complete ===")
    if best:
        print(f"Best: {best}")
    else:
        # Find closest
        sorted_results = sorted(all_results, key=lambda x: x["roi"], reverse=True)
        print("Top 10 closest:")
        for r in sorted_results[:10]:
            print(r)
        with open(os.path.join(SCRIPT_DIR, "tuned_all_results.json"), "w") as f:
            json.dump(sorted_results[:100], f, indent=2, default=str)

if __name__ == "__main__":
    main()
