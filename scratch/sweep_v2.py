"""Sweep harness: caches labeled pools per geometry, sweeps selection knobs."""
from __future__ import annotations
from pathlib import Path
import sys
import itertools

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd

from scratch.fast_numba_oos_engine import warmup_numba
import scratch.fast_numba_oos_engine_v2 as v2

GEOS = [
    # (hz, target, stop, tag)
    (48, 2.0, 1.0, "g48_20_10"),
    (96, 2.4, 1.0, "g96_24_10"),
    (96, 2.0, 1.0, "g96_20_10"),
]

def get_pool(geo):
    hz, tg, st, tag = geo
    cache = Path(f"scratch/pool_v2_{tag}.parquet")
    if cache.exists():
        return pd.read_parquet(cache)
    pool = v2.compile_dataset_v2(horizon=hz, target_r=tg, stop_r=st)
    pool.to_parquet(cache, index=False)
    return pool

def main():
    warmup_numba()
    rows = []
    for geo in GEOS:
        pool = get_pool(geo)
        for tt, mm, md in itertools.product((20, 28, 36), ("none", "soft", "floor0"), (3, 4)):
            pass_count, results = v2.run_walkforward_v2(
                pool, target_trades=tt, max_depth=md, margin_mode=mm, verbose=False)
            pnl = sum(r["pnl_usd"] for r in results)
            pos = sum(1 for r in results if r["pnl_usd"] > 0)
            trades = sum(r["trades"] for r in results)
            wr_all = [r for r in results if r["trades"] >= 10]
            med_pnl = sorted([r["pnl_usd"] for r in results])[10]
            rows.append({"geo": geo[3], "tt": tt, "mm": mm, "md": md,
                         "pass": pass_count, "pos_win": pos, "pnl": round(pnl, 1),
                         "med_pnl": round(med_pnl, 1), "trades": trades})
            print(f"{geo[3]:<11} tt={tt:<3} mm={mm:<6} md={md} -> pass={pass_count:2d}/20 posWin={pos:2d} pnl={pnl:+8.1f} med={med_pnl:+7.1f} trades={trades}", flush=True)

    df = pd.DataFrame(rows).sort_values(["pass", "pos_win", "pnl"], ascending=False)
    print("\n=== TOP 12 CONFIGS ===")
    print(df.head(12).to_string(index=False))
    df.to_csv("scratch/sweep_v2_results.csv", index=False)

if __name__ == "__main__":
    main()
