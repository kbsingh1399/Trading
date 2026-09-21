"""OX61-A: regenerate ORB candidates with live-parity sim; reuse cached S4 (unchanged code).
Saves candidates_orbparity_full.parquet (ORB fresh + S4 from baseline cache).
Usage: python docs/ox61_verification/gen_orb_parity_candidates.py
"""
import sys, os
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from Engine.core.base_strategy import EngineConfig, FOREX_CLUSTER_MAP
from Engine.strategy.orb_crt_forex_engine import ORBCRTForexCFDStrategy

HERE = Path(__file__).parent

def main():
    cfg = EngineConfig.load()
    old = pd.read_parquet(HERE / "candidates_baseline_head.parquet")
    s4 = old[old["sleeve"] == "FVG_ML"].copy()
    print(f"S4 rows reused: {len(s4)}")

    orb_strat = ORBCRTForexCFDStrategy(config=cfg)
    print("Running fresh ORB precompute (2023-09-01 -> 2026-03-31) with live-parity exits...")
    res = orb_strat.run_backtest(start_date="2023-09-01", end_date="2026-03-31", save_plot=False)
    tdf = res.trades_df.copy()
    tdf["sleeve"] = "ORB_CRT"
    tdf["cluster"] = tdf["asset"].map(lambda x: FOREX_CLUSTER_MAP.get(x, "OTHER"))
    print(f"ORB rows fresh: {len(tdf)}")
    print("ORB exit reasons:", tdf["exit_reason"].value_counts().to_dict())
    print(f"ORB hold_bars: median={tdf['hold_bars'].median()} max={tdf['hold_bars'].max()} mean={tdf['hold_bars'].mean():.1f}")
    print(f"ORB r range: [{tdf['r_realized'].min():.2f}, {tdf['r_realized'].max():.2f}]")

    comb = pd.concat([s4, tdf], ignore_index=True)
    comb["datetime"] = pd.to_datetime(comb["datetime"], utc=True)
    comb = comb.sort_values("datetime").reset_index(drop=True)
    out = HERE / "candidates_orbparity_full.parquet"
    comb.to_parquet(out, index=False)
    print(f"Saved {len(comb)} rows -> {out}")

if __name__ == "__main__":
    main()
