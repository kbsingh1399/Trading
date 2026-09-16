"""
================================================================================
T1-ONLY OUT-OF-SAMPLE WALK-FORWARD RUNNER
================================================================================
Location: Engine/run_t1_oos.py

Replaces Engine/run_20_oos_dual_model.py. The S1 15m ML sleeve is RETIRED
(see S1_TEARDOWN.md): its gross expectancy was +0.0058 R with t=+0.85, p=0.40
across 52,252 candidates -- statistically indistinguishable from zero -- while
its 15m ATR-14 risk unit (0.527% of price) was smaller than a 41 bps round trip
(0.779 R). No selector can fix a null signal.

What this runner does NOT do, and the compute it saves:
  * does not compile the 15m candidate dataset (52,252 rows, 18 symbols)
  * does not train 18 LightGBM + 18 logistic models per window (63 windows)
  * does not import lightgbm or sklearn at all
The walk-forward now fits nothing. T1 is a rule-based sleeve; there is no model
to refit, so there is no per-window fitting cost and no in-sample contamination
surface.

Causal boundaries are unchanged: disjoint chronological window sets, 4h signals
that fill on the next bar's open, and a volatility-regime friction stress joined
on a grid keyed by 4h bar CLOSE.
================================================================================
"""

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from Engine.execution_costs import ROUND_TRIP_BPS
from Engine.strategy.t1_breakout import T1ExecutionEngine, load_t1_breakout_trades

WINDOWS_PATH = REPO_ROOT / "Engine" / "oos_windows_primary.json"
CRITERIA_PATH = REPO_ROOT / "Engine" / "target_oos_criteria.json"
CACHE_DIR = REPO_ROOT / "scratch" / "cache_multi_tf"


def main(argv=None):
    ap = argparse.ArgumentParser(description="T1-only OOS walk-forward audit")
    ap.add_argument("--windows", type=str, default=str(WINDOWS_PATH),
                    help="Path to a window JSON (primary / holdout / expanded).")
    ap.add_argument("--out-json", type=str, default=None,
                    help="Optional path for the per-window scorecard JSON.")
    ap.add_argument("--dump-ledger", type=str, default=None,
                    help="Write the per-trade ledger (time, symbol, strat, r_gain, "
                         "risk_usd, window id, vol_rank) for the CVaR gate harness.")
    args = ap.parse_args(argv)

    print("\n" + "=" * 128)
    print("T1 QUIET-FLOW DONCHIAN BREAKOUT -- OUT-OF-SAMPLE WALK-FORWARD AUDIT (S1 RETIRED)")
    print("=" * 128)
    print(f"[Friction] round-trip drag = {ROUND_TRIP_BPS:.1f} bps of entry notional, plus 10 bps "
          f"explicit entry slippage in the fill price, stressed by the causal volatility regime.")

    with open(CRITERIA_PATH, "r", encoding="utf-8") as f:
        criteria = json.load(f)["target_criteria"]
    with open(args.windows, "r", encoding="utf-8") as f:
        windows = json.load(f)

    CAPITAL = criteria.get("initial_capital_usd", 5000.0)
    MIN_ROI = criteria.get("min_roi_percent", 10.0)
    MAX_DD = criteria.get("max_dd_percent", 5.0)
    MIN_WR = criteria.get("min_winrate_percent", 40.0)
    MIN_TRD = criteria.get("min_trades", 15)

    engine = T1ExecutionEngine(capital=CAPITAL)

    # Causal volatility-rank snapshot per window, used only for ledger tagging.
    from Engine.strategy.regime_governor import build_dispersion_series, compute_regime_features
    df_btc = pd.read_parquet(CACHE_DIR / "BTCUSDT_4h.parquet")
    df_btc["time"] = pd.to_datetime(df_btc["time"], utc=True)
    df_btc = df_btc.sort_values("time").reset_index(drop=True)
    # compute_regime_features reads these; they are trailing-only, so the
    # vol_rank written to the ledger cannot see the window it tags.
    df_btc["atr_pct"] = (df_btc["atr"] / df_btc["close"]) * 100.0
    df_btc["trailing_30d_atr_pct"] = df_btc["atr_pct"].rolling(180).mean()
    dispersion = build_dispersion_series(CACHE_DIR)

    t0 = time.perf_counter()
    print("\nGenerating T1 4h breakout signals across certified assets...")
    df_t1 = load_t1_breakout_trades(CACHE_DIR)
    print(f"Generated {len(df_t1):,d} T1 signals in {time.perf_counter() - t0:.2f}s "
          f"({df_t1['symbol'].nunique()} symbols). No model is fitted at any point.")
    print(f"  gross {df_t1['gross_r'].mean():+.4f} R | friction {df_t1['fric_r'].mean():.4f} R | "
          f"net {df_t1['r_gain'].mean():+.4f} R | stress>1.0x on {100*(df_t1['stress']>1).mean():.2f}% of entries")

    print("\n" + "-" * 128)
    print(f"{'W#':<3} | {'Window Name':<40} | {'Trades':<6} | {'Win Rate':<8} | {'Net PnL':<13} | "
          f"{'Net ROI':<9} | {'Max DD':<7} | {'Status':<6} | {'vol_rank':<8}")
    print("-" * 128)

    passed = 0
    ledger = []
    records = []
    total_trades = 0
    total_pnl = 0.0

    for w in windows:
        w_id = w["window_id"]
        w_name = w["name"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        s_ts = pd.Timestamp(w["start_date"], tz="UTC")

        features = compute_regime_features(df_btc, dispersion, s_ts)
        res = engine.simulate_execution(df_t1, start_ms=start_ms, end_ms=end_ms)

        n_trd = res["trades"]
        is_pass = (res["net_roi"] >= MIN_ROI and res["max_dd"] <= MAX_DD
                   and res["win_rate"] >= MIN_WR and n_trd >= MIN_TRD)
        status = "PASS" if is_pass else ("PROFIT" if res["net_pnl"] > 0 and res["max_dd"] <= MAX_DD
                                         else ("CASH" if n_trd == 0 else "FAIL"))
        if is_pass:
            passed += 1
        total_trades += n_trd
        total_pnl += res["net_pnl"]

        print(f"W{w_id:02d} | {w_name[:40]:<40} | {n_trd:<6d} | {res['win_rate']:>5.1f}%  | "
              f"{res['net_pnl']:>+11.2f} USD | {res['net_roi']:>+7.2f}% | {res['max_dd']:>5.2f}% | "
              f"{status:<6} | {features.get('vol_rank'):>7.3f}")

        for t in res["trade_ledger"]:
            ledger.append({"window_id": w_id, "window": w_name, "time": int(t["time"]),
                           "symbol": t["symbol"], "strat": t["strat"],
                           "r_gain": float(t["r_gain"]), "pnl": float(t["pnl"]),
                           "risk_usd": float(t["risk_usd"]),
                           "gross_r": t.get("gross_r"), "stress": t.get("stress"),
                           "vol_rank": features.get("vol_rank")})

        records.append({"window_id": w_id, "name": w_name, "start_date": w["start_date"],
                        "end_date": w["end_date"], "trades": n_trd, "s1_trades": 0,
                        "t1_trades": res["t1_trades"], "win_rate": res["win_rate"],
                        "net_pnl": res["net_pnl"], "net_roi": res["net_roi"],
                        "max_dd": res["max_dd"], "status": status,
                        "vol_rank": features.get("vol_rank"), "tide": features.get("tide")})

    print("=" * 128)
    print(f"T1 SCORECARD: Passed {passed}/{len(records)} | Trades {total_trades:,d} | "
          f"PnL {total_pnl:+,.2f} USD (ROI {(total_pnl/CAPITAL)*100:+.2f}%)")
    print("=" * 128)

    if args.out_json:
        out = Path(args.out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"sleeve": "T1", "capital": CAPITAL, "passed": passed,
                       "total_windows": len(records), "total_trades": total_trades,
                       "total_pnl": total_pnl, "total_roi": (total_pnl / CAPITAL) * 100.0,
                       "windows": records}, f, indent=2)
        print(f"[Scorecard] written to {out}")

    if args.dump_ledger:
        lp = Path(args.dump_ledger)
        lp.parent.mkdir(parents=True, exist_ok=True)
        with open(lp, "w", encoding="utf-8") as f:
            json.dump({"rows": ledger, "n_trades": len(ledger),
                       "total_pnl": sum(r["pnl"] for r in ledger)}, f)
        print(f"[Ledger] {len(ledger):,d} trades written to {lp}")


if __name__ == "__main__":
    main()
