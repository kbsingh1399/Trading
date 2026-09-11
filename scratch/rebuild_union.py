import os, sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scratch.strategy_battery import get_store
from scratch.stage2_ensemble import augment_pools, REPO
PROFILE = os.environ.get("PROFILE", "maker25")
big = augment_pools(get_store())
big.to_parquet(REPO / "scratch" / f"union_pool_v2_{PROFILE}.parquet", index=False)
print("union rebuilt:", PROFILE, len(big))
