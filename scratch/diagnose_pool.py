"""REX diagnostic: analyze the labeled candidate pool before any tuning."""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
import pandas as pd

from scratch.fast_numba_oos_engine import compile_dataset_with_numba

pool = compile_dataset_with_numba()

print("\n" + "="*80)
print("POOL-LEVEL DIAGNOSTICS (realized_r is NET of 0.25R friction-equivalent)")
print("="*80)
print(f"Total candidates: {len(pool):,d}")
print(f"Overall mean net r : {pool.realized_r.mean():+.4f}R")
print(f"Overall win rate   : {(pool.realized_r > 0).mean()*100:.2f}%")

print("\n--- By sleeve ---")
print(pool.groupby("sleeve_id").agg(
    n=("realized_r", "size"),
    mean_r=("realized_r", "mean"),
    wr=("realized_r", lambda x: (x > 0).mean()*100),
).round(4).to_string())

print("\n--- By side ---")
print(pool.groupby("signal_side").agg(
    n=("realized_r", "size"),
    mean_r=("realized_r", "mean"),
    wr=("realized_r", lambda x: (x > 0).mean()*100),
).round(4).to_string())

print("\n--- By sleeve x side ---")
print(pool.groupby(["sleeve_id", "signal_side"]).agg(
    n=("realized_r", "size"),
    mean_r=("realized_r", "mean"),
    wr=("realized_r", lambda x: (x > 0).mean()*100),
).round(4).to_string())

print("\n--- By symbol ---")
print(pool.groupby("symbol").agg(
    n=("realized_r", "size"),
    mean_r=("realized_r", "mean"),
).round(4).sort_values("mean_r").to_string())

# Gross-of-friction exploration: what raw exit_r distribution looks like
print("\n--- realized_r deciles ---")
print(pd.qcut(pool.realized_r, 10).value_counts().sort_index().to_string())

# Time-of-day edge
print("\n--- By hour bucket ---")
pool["hourb"] = (pool["hour"] // 4) * 4
print(pool.groupby("hourb").agg(n=("realized_r","size"), mean_r=("realized_r","mean")).round(4).to_string())

# Save pool for fast re-analysis without reloading data
out = Path("scratch/pool_cache.parquet")
pool.to_parquet(out, index=False)
print(f"\nSaved pool cache -> {out}")
