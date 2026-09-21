"""OX61 baseline driver: CURRENT-HEAD parallel walkforward, fail_fast=False.
Caches precomputed candidates to parquet for fast iteration.
Usage: python docs/ox61_verification/run_ox61_baseline.py [--recache] [--out NAME]
"""
import sys, os, argparse
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from Engine.core.base_strategy import EngineConfig, ParallelForexStrategy

CAND_CACHE = Path(__file__).parent / "candidates_baseline_head.parquet"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recache", action="store_true")
    ap.add_argument("--out", default="scorecard_baseline_head.csv")
    args = ap.parse_args()

    cfg = EngineConfig.load()
    strat = ParallelForexStrategy(config=cfg)

    if CAND_CACHE.exists() and not args.recache:
        print(f"Loading cached candidates from {CAND_CACHE}")
        strat._cached_candidate_trades = pd.read_parquet(CAND_CACHE)
    else:
        print("Precomputing candidates across full span (2023-09-01 -> 2026-03-31)...")
        comb = strat.precompute_candidates()
        print(f"Candidates: {len(comb)} rows")
        if len(comb):
            print(comb.groupby("sleeve").size())
            comb.to_parquet(CAND_CACHE, index=False)
            print(f"Cached to {CAND_CACHE}")

    rows = []
    for w in cfg.windows:
        res = strat.run_backtest(start_date=w.start_date, end_date=w.end_date, save_plot=False)
        res.window_id = w.window_id
        st = "PASS" if res.passed_criteria else "FAIL"
        print(f"W{w.window_id:02d} | trades={res.total_trades:>3} | WR={res.win_rate:>5.1f}% | "
              f"netR={res.net_r:>+7.2f} | PnL={res.net_pnl_usd:>+8.2f} | ROI={res.net_roi_pct:>+6.2f}% | "
              f"DD={res.max_dd_pct:>5.2f}% | PF={res.profit_factor:>5.2f} | {st} {res.failure_reasons}")
        rows.append({"window_id": w.window_id, "window": f"W{w.window_id:02d}", "name": w.name,
                     "trades": res.total_trades, "win_rate": res.win_rate, "profit_factor": res.profit_factor,
                     "net_r": res.net_r, "pnl_usd": res.net_pnl_usd, "roi_pct": res.net_roi_pct,
                     "max_dd_pct": res.max_dd_pct, "status": st,
                     "checks": str(res.criteria_checks), "failures": "; ".join(res.failure_reasons)})
    df = pd.DataFrame(rows)
    out = Path(__file__).parent / args.out
    df.to_csv(out, index=False)
    n_pass = int((df["status"] == "PASS").sum())
    print(f"\nBASELINE-HEAD: {n_pass}/20 PASS | PnL {df['pnl_usd'].sum():+,.2f} | maxDD {df['max_dd_pct'].max():.2f}%")
    print(f"Scorecard -> {out}")

if __name__ == "__main__":
    main()
