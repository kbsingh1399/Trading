"""OX61 R6: walk-forward retrained FVG candidates (bar-purged, pre-committed hyperparams).
Phase A: per-asset labeled frames (labeler selectable) -> labels_{tag}/{asset}.parquet
Phase B: per-window causal retrain (XGB depth4/lr0.05/120r/seed42) -> s4_r6_{tag} candidates
Phase C: merge with cached final ORB + replay dual + S4-only.
Usage: python docs/ox61_verification/run_ox61_r6.py --tag precommitted [--skip-a]
"""
import sys, os, argparse, json, time
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from Engine.core.base_strategy import EngineConfig, ParallelForexStrategy, FOREX_CLUSTER_MAP
from Engine.core.strategy_kernel import (
    CANONICAL_FEATURES, CANONICAL_18_ASSETS, engineer_features_polars, create_labels_ratchet,
)

HERE = Path(__file__).parent
DATA_DIR = str(PROJECT_ROOT / "Forex_Backtesting_Data")
PURGE_BARS = {"precommitted": 96, "unified": 480}
PROB_THRESH = 0.55  # pre-committed gate (no tuning)

def get_labeler(tag):
    if tag == "precommitted":
        return create_labels_ratchet
    elif tag == "unified":
        from Engine.core.strategy_kernel import create_labels_unified
        return create_labels_unified
    raise ValueError(tag)

def phase_a(tag):
    labeler = get_labeler(tag)
    outdir = HERE / f"labels_{tag}"
    outdir.mkdir(exist_ok=True)
    for sym in CANONICAL_18_ASSETS:
        out = outdir / f"{sym}.parquet"
        if out.exists():
            print(f"  {sym}: cached", flush=True)
            continue
        t0 = time.time()
        df = engineer_features_polars(sym, DATA_DIR)
        df = labeler(df)
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        keep = ["datetime", "open", "high", "low", "close", "is_kill_zone",
                "sweep_pdl", "sweep_pdh", "htf_4h_trend", "bullish_fvg", "bearish_fvg",
                "target", "r_realized"] + [c for c in CANONICAL_FEATURES
                if c not in ("htf_4h_trend", "bullish_fvg", "bearish_fvg")]
        keep += [c for c in ("hold_bars", "exit_reason") if c in df.columns]
        df[keep].to_parquet(out, index=False)
        nv = int(df["target"].notna().sum())
        print(f"  {sym}: {len(df)} bars, {nv} labeled ({time.time()-t0:.0f}s)", flush=True)

def phase_b(tag):
    import xgboost as xgb
    from sklearn.metrics import roc_auc_score
    outdir = HERE / f"labels_{tag}"
    purge = PURGE_BARS[tag]
    cfg = EngineConfig.load()
    frames = {}
    for sym in CANONICAL_18_ASSETS:
        p = outdir / f"{sym}.parquet"
        if p.exists():
            d = pd.read_parquet(p)
            d["datetime"] = pd.to_datetime(d["datetime"], utc=True)
            frames[sym] = d.reset_index(drop=True)
    all_cand = []
    diag = []
    for w in cfg.windows:
        t0 = time.time()
        ws = pd.Timestamp(w.start_date, tz="UTC")
        we = pd.Timestamp(w.end_date, tz="UTC")  # baseline-identical: midnight-exclusive end
        Xtrs, ytrs, tests = [], [], []
        for sym, d in frames.items():
            dt = d["datetime"].values
            k0 = int(np.searchsorted(dt, ws.to_datetime64()))
            k1 = int(np.searchsorted(dt, we.to_datetime64(), side="right")) - 1
            k0 = max(k0, 0); k1 = min(k1, len(d) - 1)
            tr = d.iloc[:max(0, k0 - purge)]
            tr = tr[tr["target"].notna()]
            if len(tr):
                Xtrs.append(tr[CANONICAL_FEATURES].values)
                ytrs.append(tr["target"].values.astype(int))
            if k1 >= k0:
                te = d.iloc[k0:k1 + 1]
                te = te[te["target"].notna()].copy()
                if len(te):
                    te["asset"] = sym
                    tests.append(te)
        Xtr = np.vstack(Xtrs); ytr = np.concatenate(ytrs)
        dtrain = xgb.DMatrix(Xtr, label=ytr)
        params = {"objective": "binary:logistic", "max_depth": 4, "learning_rate": 0.05,
                  "eval_metric": "logloss", "seed": 42}
        booster = xgb.train(params, dtrain, num_boost_round=120)
        fit_auc = roc_auc_score(ytr, booster.predict(dtrain))
        n_sig = 0
        for te in tests:
            te["prob"] = booster.predict(xgb.DMatrix(te[CANONICAL_FEATURES].values))
            long_m = ((te["prob"] >= PROB_THRESH) & (te["htf_4h_trend"] > 0)
                      & (te["bullish_fvg"] > 0) & te["is_kill_zone"])
            short_m = ((te["prob"] >= PROB_THRESH) & (te["htf_4h_trend"] < 0)
                       & (te["bearish_fvg"] > 0) & te["is_kill_zone"])
            te["signal"] = 0
            te.loc[long_m, "signal"] = 1
            te.loc[short_m, "signal"] = -1
            sig = te[te["signal"] != 0]
            n_sig += len(sig)
            if len(sig):
                cols = ["datetime", "asset", "signal", "prob", "r_realized", "target"] \
                    + [c for c in ("hold_bars", "exit_reason") if c in sig.columns]
                all_cand.append(sig[cols].copy())
        pos = float(ytr.mean())
        diag.append({"window": w.window_id, "n_train": len(ytr), "pos_rate": round(pos, 4),
                     "fit_auc": round(float(fit_auc), 4), "n_sig": n_sig})
        print(f"W{w.window_id:02d}: train={len(ytr)} pos={pos:.3f} fitAUC={fit_auc:.4f} sig={n_sig} ({time.time()-t0:.0f}s)", flush=True)
    cand = pd.concat(all_cand, ignore_index=True) if all_cand else pd.DataFrame()
    cand.to_parquet(HERE / f"s4_r6_{tag}.parquet", index=False)
    with open(HERE / f"r6_{tag}_diag.json", "w") as f:
        json.dump(diag, f, indent=1)
    print(f"S4-R6-{tag} candidates: {len(cand)}")

def phase_c(tag, orb_cache="candidates_orbparity_full.parquet"):
    cfg = EngineConfig.load()
    s4 = pd.read_parquet(HERE / f"s4_r6_{tag}.parquet")
    s4["sleeve"] = "FVG_ML"
    if "hold_bars" not in s4.columns:
        s4["hold_bars"] = 24  # pre-committed default (kernel emits no holds; unified tag emits true holds)
    s4["cluster"] = s4["asset"].map(lambda x: FOREX_CLUSTER_MAP.get(x, "OTHER"))
    orb = pd.read_parquet(HERE / orb_cache)
    orb = orb[orb["sleeve"] == "ORB_CRT"].copy()
    print(f"S4-R6: {len(s4)} + ORB-final: {len(orb)}")
    comb = pd.concat([s4, orb], ignore_index=True)
    comb["datetime"] = pd.to_datetime(comb["datetime"], utc=True)
    comb = comb.sort_values("datetime").reset_index(drop=True)
    comb.to_parquet(HERE / f"candidates_dual_r6_{tag}.parquet", index=False)
    # Dual replay
    strat = ParallelForexStrategy(config=cfg)
    strat._cached_candidate_trades = comb
    rows = []
    for w in cfg.windows:
        res = strat.run_backtest(start_date=w.start_date, end_date=w.end_date, save_plot=False)
        st = "PASS" if res.passed_criteria else "FAIL"
        print(f"W{w.window_id:02d} | trades={res.total_trades:>3} | WR={res.win_rate:>5.1f}% | "
              f"netR={res.net_r:>+7.2f} | ROI={res.net_roi_pct:>+6.2f}% | DD={res.max_dd_pct:>5.2f}% | {st}")
        rows.append({"window_id": w.window_id, "window": f"W{w.window_id:02d}", "name": w.name,
                     "trades": res.total_trades, "win_rate": res.win_rate, "net_r": res.net_r,
                     "pnl_usd": res.net_pnl_usd, "roi_pct": res.net_roi_pct, "max_dd_pct": res.max_dd_pct,
                     "status": st, "failures": "; ".join(res.failure_reasons)})
    df = pd.DataFrame(rows)
    df.to_csv(HERE / f"scorecard_dual_r6_{tag}.csv", index=False)
    print(f"\nDUAL-R6-{tag}: {int((df['status']=='PASS').sum())}/20 PASS | PnL {df['pnl_usd'].sum():+,.2f} | maxDD {df['max_dd_pct'].max():.2f}%")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="precommitted")
    ap.add_argument("--skip-a", action="store_true")
    ap.add_argument("--only-c", action="store_true")
    args = ap.parse_args()
    if not args.only_c:
        if not args.skip_a:
            print("=== Phase A: labeled frames ===")
            phase_a(args.tag)
        print("=== Phase B: walk-forward retrain ===")
        phase_b(args.tag)
    print("=== Phase C: merge + replay ===")
    phase_c(args.tag)
