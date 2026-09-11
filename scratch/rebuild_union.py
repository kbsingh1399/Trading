import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scratch.strategy_battery import get_store
from scratch.stage2_ensemble import augment_pools, REPO
big = augment_pools(get_store())
big.to_parquet(REPO / "scratch" / "union_pool_v2.parquet", index=False)
print("union rebuilt:", len(big))
