"""OX61 attribution replay: rerun governor per window on a sleeve subset of cached candidates.
Usage: python docs/ox61_verification/replay_sleeve.py --sleeve ORB_CRT --out scorecard_orb_only.csv
       python docs/ox61_verification/replay_sleeve.py --sleeve FVG_ML --out scorecard_fvg_only.csv
"""
import sys, os, argparse
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from Engine.core.base_strategy import EngineConfig, ParallelForexStrategy

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sleeve", required=True, help="sleeve tag substring, e.g. ORB_CRT or FVG_ML (or ALL)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cand", default="candidates_baseline_head.parquet")
    args = ap.parse_args()

    cfg = EngineConfig.load()
    strat = ParallelForexStrategy(config=cfg)
    comb = pd.read_parquet(Path(__file__).parent / args.cand)
    print(f"Loaded {len(comb)} cached candidates; sleeves: {comb['sleeve'].unique().tolist()}")
    if args.sleeve != "ALL":
        comb = comb[comb["sleeve"].str.contains(args.sleeve)].copy()
    print(f"Replaying {len(comb)} candidates for sleeve filter '{args.sleeve}'")
    strat._cached_candidate_trades = comb.sort_values("datetime").reset_index(drop=True)

    rows = []
    for w in cfg.windows:
        res = strat.run_backtest(start_date=w.start_date, end_date=w.end_date, save_plot=False)
        res.window_id = w.window_id
        st = "PASS" if res.passed_criteria else "FAIL"
        print(f"W{w.window_id:02d} | trades={res.total_trades:>3} | WR={res.win_rate:>5.1f}% | "
              f"netR={res.net_r:>+7.2f} | PnL={res.net_pnl_usd:>+8.2f} | ROI={res.net_roi_pct:>+6.2f}% | "
              f"DD={res.max_dd_pct:>5.2f}% | {st}")
        rows.append({"window_id": w.window_id, "window": f"W{w.window_id:02d}", "name": w.name,
                     "trades": res.total_trades, "win_rate": res.win_rate, "net_r": res.net_r,
                     "pnl_usd": res.net_pnl_usd, "roi_pct": res.net_roi_pct, "max_dd_pct": res.max_dd_pct,
                     "status": st, "failures": "; ".join(res.failure_reasons)})
    df = pd.DataFrame(rows)
    df.to_csv(Path(__file__).parent / args.out, index=False)
    print(f"\n{args.sleeve}: {int((df['status']=='PASS').sum())}/20 PASS | PnL {df['pnl_usd'].sum():+,.2f} | maxDD {df['max_dd_pct'].max():.2f}%")

if __name__ == "__main__":
    main()
