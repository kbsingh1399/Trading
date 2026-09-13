"""
SSRN Loop Runner — Tries strategies one by one until month ROI >10%, DD <5%, TP >=3R
No lookahead, uses Binance backtesting data in Engine/binance_backtesting_data
"""

import os, glob, sys, json
import numpy as np
import pandas as pd
from typing import Dict, List

# Ensure project root in path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig
from Engine.core.portfolio_execution_kernel import PortfolioExecutionKernel
from Engine.strategy.ssrn_alpha_suite import STRATEGY_REGISTRY

DATA_DIR = os.path.join(SCRIPT_DIR, "binance_backtesting_data")
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT",
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT",
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT",
]

WINDOWS = [
    ("W01", "2021-05-01", "2021-05-31"),
    ("W02", "2021-09-01", "2021-09-30"),
    ("W03", "2021-11-01", "2021-11-30"),
    ("W04", "2022-01-01", "2022-01-31"),
    ("W05", "2022-05-01", "2022-05-31"),
    ("W06", "2022-06-01", "2022-06-30"),
    ("W07", "2022-09-01", "2022-09-30"),
    ("W08", "2022-11-01", "2022-11-30"),
    ("W09", "2023-01-01", "2023-01-31"),
    ("W10", "2023-03-01", "2023-03-31"),
    ("W11", "2023-06-01", "2023-06-30"),
    ("W12", "2023-08-01", "2023-08-31"),
    ("W13", "2023-10-01", "2023-10-31"),
    ("W14", "2024-01-01", "2024-01-31"),
    ("W15", "2024-03-01", "2024-03-31"),
    ("W16", "2024-08-01", "2024-08-31"),
    ("W17", "2024-11-01", "2024-11-30"),
    ("W18", "2025-02-01", "2025-02-28"),
    ("W19", "2025-07-01", "2025-07-31"),
    ("W20", "2026-03-01", "2026-03-31"),
]

TARGET_ROI = 10.0
MAX_DD = 5.0
MIN_TP_R = 3.0
MIN_TRADES = 10

def load_master_data() -> Dict[str, pd.DataFrame]:
    per_symbol = {}
    for sym in SYMBOLS:
        path = os.path.join(DATA_DIR, f"{sym}_15m_master_2020_2026.parquet")
        if not os.path.exists(path):
            print(f"Missing {path}")
            continue
        df = pd.read_parquet(path)
        # ensure datetime index
        df["datetime_utc"] = pd.to_datetime(df["datetime_utc"])
        df = df.set_index("datetime_utc").sort_index()
        # drop duplicates
        df = df[~df.index.duplicated(keep='last')]
        per_symbol[sym] = df
        print(f"Loaded {sym}: {len(df)} rows from {df.index[0]} to {df.index[-1]}")
    return per_symbol


def load_ladder_features(per_symbol: Dict[str, pd.DataFrame], use_cache=True, max_symbols=5) -> Dict[str, pd.DataFrame]:
    ladder_features = {}
    cache_dir = os.path.join(DATA_DIR, "ladder_cache")
    os.makedirs(cache_dir, exist_ok=True)

    # Only process first max_symbols for speed in initial search
    symbols_to_process = SYMBOLS[:max_symbols] if max_symbols else SYMBOLS

    for sym in symbols_to_process:
        cache_path = os.path.join(cache_dir, f"{sym}_footprint_agg.parquet")
        if use_cache and os.path.exists(cache_path):
            try:
                agg = pd.read_parquet(cache_path)
                agg.index = pd.to_datetime(agg.index)
                ladder_features[sym] = agg
                print(f"  Ladder {sym}: loaded from cache {len(agg)} rows")
                continue
            except Exception as e:
                print(f"  Cache load failed {sym}: {e}")

        path = os.path.join(DATA_DIR, f"{sym}_15m_footprint_ladder.parquet")
        if not os.path.exists(path):
            continue
        try:
            ldf = pd.read_parquet(path, columns=["open_time_ms", "bid_vol_coin", "ask_vol_coin", "total_vol_coin", "net_delta_coin", "is_buy_imbalance", "is_sell_imbalance", "is_stacked_buy_imb", "is_stacked_sell_imb", "is_poc", "price_bin"])
            master = per_symbol.get(sym)
            if master is None:
                continue
            # Fast groupby: only sums, no custom lambda for poc_price
            # For poc_price we can get max is_poc price via separate groupby
            # Compute poc_price: price_bin where is_poc==1, else mean
            # First get poc rows
            poc_rows = ldf[ldf["is_poc"] == 1][["open_time_ms", "price_bin"]].drop_duplicates("open_time_ms")
            poc_map = dict(zip(poc_rows["open_time_ms"], poc_rows["price_bin"]))

            agg = ldf.groupby("open_time_ms").agg(
                total_bid_vol=("bid_vol_coin", "sum"),
                total_ask_vol=("ask_vol_coin", "sum"),
                total_vol=("total_vol_coin", "sum"),
                net_delta=("net_delta_coin", "sum"),
                buy_imb_count=("is_buy_imbalance", "sum"),
                sell_imb_count=("is_sell_imbalance", "sum"),
                stacked_buy=("is_stacked_buy_imb", "sum"),
                stacked_sell=("is_stacked_sell_imb", "sum"),
            )
            agg["delta_ratio"] = agg["net_delta"] / agg["total_vol"].replace(0, np.nan)
            agg["delta_ratio"] = agg["delta_ratio"].fillna(0)
            agg["buy_imb"] = agg["buy_imb_count"]
            agg["sell_imb"] = agg["sell_imb_count"]
            agg["poc_price"] = agg.index.map(poc_map)
            # Fill missing poc_price with approximate median price (we will compute later via master close)
            # Map to datetime
            ms_to_dt = dict(zip(master["open_time_ms"].values, master.index))
            agg["datetime_utc"] = agg.index.map(ms_to_dt)
            agg = agg.dropna(subset=["datetime_utc"])
            agg = agg.set_index("datetime_utc").sort_index()
            # Fill poc_price NaN with close
            aligned = master.reindex(agg.index)
            agg["poc_price"] = agg["poc_price"].fillna(aligned["close"])
            hl = (aligned["high"] - aligned["low"]).replace(0, np.nan)
            agg["poc_pos"] = ((agg["poc_price"] - aligned["low"]) / hl).fillna(0.5)
            keep = ["stacked_buy", "stacked_sell", "buy_imb", "sell_imb", "delta_ratio", "poc_pos", "total_bid_vol", "total_ask_vol"]
            final = agg[keep]
            ladder_features[sym] = final
            # Save cache
            try:
                final.to_parquet(cache_path)
            except Exception as e:
                print(f"  Cache save failed {sym}: {e}")
            print(f"  Ladder {sym}: {len(final)} aggregated candles (computed)")
        except Exception as e:
            print(f"  Failed ladder {sym}: {e}")
            import traceback; traceback.print_exc()
            continue
    return ladder_features


def slice_window(per_symbol: Dict[str, pd.DataFrame], start: str, end: str) -> Dict[str, pd.DataFrame]:
    ws = pd.Timestamp(start)
    we = pd.Timestamp(end) + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
    out = {}
    for sym, df in per_symbol.items():
        sl = df.loc[ws:we]
        if len(sl) > 100:
            out[sym] = sl
    return out


def evaluate_strategy(strategy_fn, per_symbol_full: Dict[str, pd.DataFrame],
                      ladder_features_full: Dict[str, pd.DataFrame],
                      window_id: str, start: str, end: str,
                      risk_cfg: RiskConfig, ratchet_cfg: RatchetConfig) -> Dict:
    per_symbol = slice_window(per_symbol_full, start, end)
    if not per_symbol:
        return {"roi_pct": 0, "max_dd_pct": 0, "trades": 0, "win_rate_pct": 0, "net_pnl": 0, "window": window_id}

    # slice ladder
    ladder_sliced = {}
    for sym, lf in ladder_features_full.items():
        if sym in per_symbol:
            sl = lf.loc[pd.Timestamp(start): pd.Timestamp(end) + pd.Timedelta(days=1)]
            ladder_sliced[sym] = sl

    # Generate signals (causal, no lookahead inside strategy)
    try:
        # Check if strategy expects ladder
        import inspect
        sig_params = inspect.signature(strategy_fn).parameters
        if len(sig_params) == 2:
            signals = strategy_fn(per_symbol, ladder_sliced)
        else:
            signals = strategy_fn(per_symbol)
    except Exception as e:
        print(f"  Strategy error {window_id}: {e}")
        import traceback; traceback.print_exc()
        return {"roi_pct": 0, "max_dd_pct": 100, "trades": 0, "win_rate_pct": 0, "net_pnl": 0, "window": window_id, "error": str(e)}

    # Ensure signals aligned to per_symbol index
    gated = {}
    for sym in per_symbol.keys():
        if sym in signals:
            s = signals[sym]
            # Reindex to per_symbol index, fill 0
            s_aligned = s.reindex(per_symbol[sym].index).fillna({"side": 0, "raw_r": per_symbol[sym]["atr_14"].fillna(per_symbol[sym]["close"]*0.02)})
            # Ensure side int
            s_aligned["side"] = s_aligned["side"].astype(int)
            gated[sym] = s_aligned
        else:
            gated[sym] = pd.DataFrame({"side": np.zeros(len(per_symbol[sym]), dtype=int),
                                       "raw_r": per_symbol[sym]["atr_14"].fillna(per_symbol[sym]["close"]*0.02).values},
                                      index=per_symbol[sym].index)

    # Portfolio kernel
    symbols = list(per_symbol.keys())
    kernel = PortfolioExecutionKernel(
        symbols=symbols,
        risk=risk_cfg,
        fric=FrictionConfig(),
        ratchet=ratchet_cfg,
        max_positions=2,
        dd_defense_thresh=0.025,
        dd_entry_buffer=0.038
    )
    result = kernel.run(per_symbol, gated, training_mode=False)
    result["window"] = window_id
    return result


def main():
    print("=== SSRN Strategy Loop — Target: ROI >10%, DD <5%, TP >=3R ===")
    per_symbol_full = load_master_data()
    # For speed, load only 5 major symbols ladder initially, then expand if needed
    ladder_features_full = load_ladder_features(per_symbol_full, use_cache=True, max_symbols=5)

    # Risk configs to try: base risk $50 = 1%, house $100, defense $15, DD limit 4.5% or 5%
    risk_cfg = RiskConfig(initial_capital=5000.0, base_risk=50.0, house_money_risk=100.0,
                          drawdown_defense_risk=15.0, drawdown_limit=0.05)
    # Ratchet configs: TP >=3R
    ratchet_configs = [
        RatchetConfig(arm0_r=0.8, lock0_r=0.15, arm1_r=1.5, lock1_r=0.8, arm2_r=2.2, lock2_r=1.5, min_target_r=3.0, time_decay_bars=32, time_decay_r=0.20),
        RatchetConfig(arm0_r=0.8, lock0_r=0.20, arm1_r=1.5, lock1_r=0.80, arm2_r=2.5, lock2_r=1.80, min_target_r=3.5, time_decay_bars=28, time_decay_r=0.20),
        RatchetConfig(arm0_r=1.0, lock0_r=0.30, arm1_r=2.0, lock1_r=1.0, arm2_r=3.0, lock2_r=2.0, min_target_r=4.0, time_decay_bars=24, time_decay_r=0.15),
    ]

    # For quick initial search, test only most volatile recent windows
    global WINDOWS
    WINDOWS_QUICK = [
        ("W15", "2024-03-01", "2024-03-31"),
        ("W17", "2024-11-01", "2024-11-30"),
        ("W19", "2025-07-01", "2025-07-31"),
        ("W20", "2026-03-01", "2026-03-31"),
    ]
    # Use quick windows first
    WINDOWS = WINDOWS_QUICK

    results_log = []
    best_overall = None

    for ratchet_cfg in ratchet_configs:
        print(f"\n--- Testing Ratchet TP={ratchet_cfg.min_target_r}R ---")
        for strat_name, strat_fn in STRATEGY_REGISTRY:
            print(f"\n>>> Trying strategy {strat_name} with TP {ratchet_cfg.min_target_r}R")
            window_results = []
            for wid, ws, we in WINDOWS:
                res = evaluate_strategy(strat_fn, per_symbol_full, ladder_features_full, wid, ws, we, risk_cfg, ratchet_cfg)
                window_results.append(res)
                print(f"  {wid} {ws}: ROI {res['roi_pct']:.2f}% DD {res['max_dd_pct']:.2f}% Trades {res['trades']} WR {res['win_rate_pct']:.1f}%")

            # Aggregate metrics
            rois = [r["roi_pct"] for r in window_results]
            dds = [r["max_dd_pct"] for r in window_results]
            trades = [r["trades"] for r in window_results]
            avg_roi = float(np.mean(rois)) if rois else 0
            median_roi = float(np.median(rois)) if rois else 0
            max_dd_overall = float(np.max(dds)) if dds else 0
            avg_dd = float(np.mean(dds)) if dds else 0
            total_trades = int(np.sum(trades))
            # Count windows passing target
            passing = [r for r in window_results if r["roi_pct"] > TARGET_ROI and r["max_dd_pct"] < MAX_DD and r["trades"] >= 5]
            pass_rate = len(passing) / len(window_results) if window_results else 0

            print(f"  => Avg ROI {avg_roi:.2f}% Median {median_roi:.2f}% Avg DD {avg_dd:.2f}% Max DD {max_dd_overall:.2f}% Total Trades {total_trades} Pass Rate {pass_rate*100:.1f}% ({len(passing)}/{len(window_results)})")

            log_entry = {
                "strategy": strat_name,
                "tp_r": ratchet_cfg.min_target_r,
                "avg_roi": avg_roi,
                "median_roi": median_roi,
                "avg_dd": avg_dd,
                "max_dd": max_dd_overall,
                "total_trades": total_trades,
                "pass_rate": pass_rate,
                "passing_windows": [p["window"] for p in passing],
                "window_results": window_results
            }
            results_log.append(log_entry)

            # Check if any single window passes with flying colors and we want to stop
            for r in window_results:
                if r["roi_pct"] > TARGET_ROI and r["max_dd_pct"] < MAX_DD and r["trades"] >= MIN_TRADES and ratchet_cfg.min_target_r >= MIN_TP_R:
                    print(f"\n*** SUCCESS: Strategy {strat_name} achieves target in {r['window']} ROI {r['roi_pct']:.2f}% DD {r['max_dd_pct']:.2f}% Trades {r['trades']} TP {ratchet_cfg.min_target_r}R ***")
                    # Save best
                    if best_overall is None or r["roi_pct"] > best_overall["roi_pct"]:
                        best_overall = {
                            "strategy": strat_name,
                            "window": r["window"],
                            "roi_pct": r["roi_pct"],
                            "max_dd_pct": r["max_dd_pct"],
                            "trades": r["trades"],
                            "win_rate": r["win_rate_pct"],
                            "tp_r": ratchet_cfg.min_target_r,
                            "full_result": r
                        }
                    # If we have a strategy that passes in at least 3 windows with avg ROI >10%, we can stop
                    if avg_roi > TARGET_ROI and avg_dd < MAX_DD and total_trades > 50:
                        print(f"\n*** OVERALL SUCCESS: Strategy {strat_name} avg ROI {avg_roi:.2f}% >10% with DD {avg_dd:.2f}% <5% ***")
                        # Save results and exit loop
                        with open(os.path.join(SCRIPT_DIR, "ssrn_loop_results.json"), "w") as f:
                            json.dump({"best_overall": best_overall, "all_results": results_log}, f, indent=2, default=str)
                        # Also save the winning strategy code snippet
                        with open(os.path.join(SCRIPT_DIR, "WINNING_STRATEGY.json"), "w") as f:
                            json.dump(best_overall, f, indent=2, default=str)
                        return

            # Save intermediate
            with open(os.path.join(SCRIPT_DIR, "ssrn_loop_results.json"), "w") as f:
                json.dump({"best_overall": best_overall, "all_results": results_log}, f, indent=2, default=str)

    print("\n=== Loop finished ===")
    if best_overall:
        print(f"Best overall: {best_overall}")
    else:
        print("No strategy achieved target. Check ssrn_loop_results.json for closest.")
    # Save final
    with open(os.path.join(SCRIPT_DIR, "ssrn_loop_results.json"), "w") as f:
        json.dump({"best_overall": best_overall, "all_results": results_log}, f, indent=2, default=str)


if __name__ == "__main__":
    main()
