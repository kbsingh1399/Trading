"""build_variant_pools.py — merge augmented features across geo-override runs into
one variant parquet per fee profile: rows for every (fam, tag, geo) combination
available (SURV_W/M defaults + SURV_L + SURV_XL).
"""
import os
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scratch.strategy_battery import get_store
import scratch.stage2_ensemble as st2


def main():
    profile = os.environ.get("PROFILE", "taker41")
    out = REPO / "scratch" / f"variant_pool_{profile}.parquet"
    store = get_store()
    frames = []
    dirs = [REPO / "scratch" / f"battery_pools_v2_{profile}"]
    for gg in ("SURV_L", "SURV_XL"):
        d = REPO / "scratch" / f"battery_pools_v2_{profile}_{gg}"
        if d.exists():
            dirs.append(d)
    for d in dirs:
        st2.POOL_DIR = d
        big = st2.augment_pools(store)
        big["geo"] = big["geo"].astype(str)
        frames.append(big)
        gg = d.name.rsplit("_", 1)[-1]
        print(f"[variant] {d.name}: {len(big):,d} rows", flush=True)
    allv = pd.concat(frames, ignore_index=True)
    allv.to_parquet(out, index=False)
    print(f"[variant] wrote {out} rows={len(allv):,d}")


if __name__ == "__main__":
    main()
