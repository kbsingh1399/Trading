"""REX/MAX diagnostic round 2: causal design exploration restricted to pre-W01 data.

All analysis below uses ONLY candidates with open_time_ms < 2021-05-01 - 72h,
i.e. data that is in-sample for every OOS window. Design decisions frozen from
this block are walk-forward legitimate.
"""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
import pandas as pd
from numba import njit

from scratch.fast_numba_oos_engine import (
    compile_dataset_with_numba, DATA_DIR, CORE_SYMBOLS, COLS_TO_LOAD,
    label_triple_barriers_numba,
)

PURGE_MS = 72 * 3600 * 1000
W01_START_MS = pd.Timestamp("2021-05-01", tz="UTC").value // 1_000_000
DESIGN_CUTOFF = W01_START_MS - PURGE_MS

pool = compile_dataset_with_numba()
design = pool[pool.open_time_ms < DESIGN_CUTOFF].copy()
print(f"\nDesign pool (pre-W01, causal): {len(design):,d} candidates")
print(f"Design mean net r: {design.realized_r.mean():+.4f}R  (gross: {design.realized_r.mean()+0.25:+.4f}R)")

# ---------------------------------------------------------------------------
# 1. Directional forward-return edge by feature bucket (geometry-independent)
# ---------------------------------------------------------------------------
print("\n" + "="*90)
print("1. RAW DIRECTIONAL EDGE ACROSS UNIVERSE (all bars, design period) by feature")
print("   gross_fwd_r = side-consistent move fwd N bars in ATR units, mean reversion = inverted")
print("="*90)

@njit(fastmath=True)
def fwd_r(c, atr, horizon):
    n = len(c)
    out = np.zeros(n)
    for i in range(n - horizon):
        out[i] = (c[i+horizon] - c[i]) / atr[i]
    return out

rows = []
for sym in CORE_SYMBOLS:
    p = DATA_DIR / f"{sym}_15m_master_2020_2026.parquet"
    if not p.exists():
        continue
    df = pd.read_parquet(p, columns=COLS_TO_LOAD)
    df = df[df.open_time_ms < DESIGN_CUTOFF]
    if len(df) < 1000:
        continue
    c = df.close.to_numpy(float)
    atr_raw = df["atr_14"].fillna(df["close"]*0.01).to_numpy(float)
    atr = np.maximum(atr_raw, df["close"].to_numpy(float)*0.012)
    for hz in (8, 24, 48):
        r = fwd_r(c, atr, hz)
        sub = pd.DataFrame({
            "r_long": r,
            "taker": df["taker_volume_ratio"].fillna(1.0).to_numpy(float),
            "zc": (df["zc_div"]/df["volume_base"].replace(0,1.0)).clip(-3,3).fillna(0).to_numpy(float),
            "volr": df["volume_ratio"].fillna(1.0).to_numpy(float),
            "vwap_z": df["vwap_zscore"].fillna(0.0).to_numpy(float),
            "rsi": df["rsi_14"].fillna(50.0).to_numpy(float),
            "e200dist": (df["close"]/df["ema_200"]-1.0).clip(-0.2,0.2).fillna(0.0).to_numpy(float),
        })
        sub["hz"] = hz
        rows.append(sub)

big = pd.concat(rows, ignore_index=True)

def bucket_report(df, col, bins, label):
    g = df.groupby(pd.cut(df[col], bins), observed=True)["r_long"]
    stats = g.agg(["size", "mean"])
    out = []
    for iv, row in stats.iterrows():
        if row["size"] >= 500:
            out.append(f"{str(iv):>22}: n={int(row['size']):>7,d}  trend={row['mean']:+.4f}R  mr={-row['mean']:+.4f}R")
    print(f"\n  [{label}]")
    print("\n".join(out) if out else "   (no buckets with n>=500)")

for hz in (8, 24, 48):
    d = big[big.hz == hz]
    print(f"\n--- Horizon {hz} bars ({hz*15} min) | n={len(d):,d} | overall: trend={d.r_long.mean():+.4f}R mr={-d.r_long.mean():+.4f}R")
    bucket_report(d, "taker", [0, 0.7, 0.85, 0.95, 1.05, 1.15, 1.3, 5], "taker_ratio")
    bucket_report(d, "zc", [-3, -0.10, -0.03, 0.03, 0.10, 3], "zc_norm")
    bucket_report(d, "vwap_z", [-10, -2, -1, -0.5, 0.5, 1, 2, 10], "vwap_zscore")
    bucket_report(d, "rsi", [0, 25, 40, 60, 75, 100], "rsi_14")
    bucket_report(d, "e200dist", [-0.2, -0.03, 0.0, 0.03, 0.2], "close vs ema200")
