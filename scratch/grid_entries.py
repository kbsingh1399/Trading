"""ALEX/MAX: test entry-condition variants + inversion on causal design period.

For each candidate entry spec we report per-candidate NET expectancy across a
small set of exit geometries. Design period only (pre-W01 + 72h purge).
"""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
import pandas as pd

from scratch.fast_numba_oos_engine import (
    DATA_DIR, CORE_SYMBOLS, COLS_TO_LOAD, label_triple_barriers_numba,
    load_btc_macro_tide,
)
from scratch.grid_geometry import build_conditions, DESIGN_CUTOFF

btc_tide = load_btc_macro_tide()

GEOS = [
    # (hz, target, stop, be_trig, be_lock) - friction 0.25 fixed
    (24, 2.0, 0.75, 0.95, 0.45),
    (48, 2.0, 1.00, 0.75, 0.35),
    (96, 2.0, 1.00, 0.95, 0.45),
]


def enrich(df):
    c = df.close.to_numpy(float)
    att_ = df["atr_14"].fillna(df["close"] * 0.01)
    atr = np.maximum(att_.to_numpy(float), c * 0.012)
    atr100 = df["atr_100"].fillna(df["close"] * 0.01).to_numpy(float)
    atr_ratio = np.clip(np.where(atr100 > 0, atr / atr100, 1.0), 0.2, 5.0)
    e200 = df["ema_200"].to_numpy(float)
    slope = ((df["ema_200"] - df["ema_200"].shift(12)) / df["close"]).fillna(0.0).to_numpy(float)
    t = df.open_time_ms.to_numpy(np.int64)
    tide = pd.Series(t).map(btc_tide).fillna(0.0).to_numpy(float)
    vwap_z = df["vwap_zscore"].fillna(0.0).to_numpy(float)
    vol_ratio = df["volume_ratio"].fillna(1.0).to_numpy(float)
    zc = (df["zc_div"] / df["volume_base"].replace(0, 1.0)).clip(-3, 3).fillna(0).to_numpy(float)
    sliq = df["short_liq_zs"].fillna(0.0).to_numpy(float)
    lliq = df["long_liq_zs"].fillna(0.0).to_numpy(float)
    s_val = df["session_val"].fillna(df["low"]).to_numpy(float)
    s_vah = df["session_vah"].fillna(df["high"]).to_numpy(float)
    taker = df["taker_volume_ratio"].fillna(1.0).to_numpy(float)
    rsi = df["rsi_14"].fillna(50.0).to_numpy(float)
    mom = (df["close"] / df["close"].shift(288) - 1.0).fillna(0.0).to_numpy(float)
    lo = df.low.to_numpy(float); h = df.high.to_numpy(float)
    e200dist = np.clip(c / e200 - 1.0, -0.2, 0.2)
    return dict(c=c, h=h, lo=lo, atr=atr, atr_ratio=atr_ratio, e200=e200, slope=slope,
                tide=tide, vwap_z=vwap_z, vol_ratio=vol_ratio, zc=zc, sliq=sliq, lliq=lliq,
                s_val=s_val, s_vah=s_vah, taker=taker, rsi=rsi, mom=mom, e200dist=e200dist)


def suite_specs(F):
    """Return dict of spec_name -> (long_mask, short_mask)."""
    specs = {}
    c, h, lo = F["c"], F["h"], F["lo"]
    e200, slope, tide = F["e200"], F["slope"], F["tide"]
    vz, vr, zc, tk, rsi = F["vwap_z"], F["vol_ratio"], F["zc"], F["taker"], F["rsi"]
    ar, mom, e2d = F["atr_ratio"], F["mom"], F["e200dist"]

    # ORIGINAL suite
    c1, h1, lo1, atr1, t1, lc, sc = None, None, None, None, None, None, None
    specs["ORIG_suite"] = None  # filled by caller via grid_geometry.build_conditions

    # INVERTED suite is also filled by caller.

    # E1: plain trend-pullback long / trend-rally short (no flow conditions)
    specs["E1_trend_pullback"] = (
        (c > e200) & (slope > 0.02) & (tide >= 0) & (rsi > 55) & (vz > 0.5) & (ar < 1.10),
        (c < e200) & (slope < -0.02) & (tide <= 0) & (rsi < 45) & (vz < -0.5) & (ar < 1.10),
    )
    # E2: E1 + moderate momentum confirmation
    specs["E2_trend_mom"] = (
        (c > e200) & (slope > 0.02) & (tide >= 0) & (rsi > 55) & (mom > 0.0) & (e2d > 0.01),
        (c < e200) & (slope < -0.02) & (tide <= 0) & (rsi < 45) & (mom < 0.0) & (e2d < -0.01),
    )
    # E3: quiet-flow compression long (T1 loosened, tide-gated)
    specs["E3_quietflow"] = (
        (ar < 0.85) & (vr >= 1.4) & (slope > 0.02) & (c > e200) & (tide >= 0) & (rsi > 50),
        (ar < 0.85) & (vr >= 1.4) & (slope < -0.02) & (c < e200) & (tide <= 0) & (rsi < 50),
    )
    # E4: deep pullback in uptrend (mean-reversion rejoin)
    specs["E4_dip_rejoin"] = (
        (c > e200) & (slope > 0.02) & (tide >= 0) & (vz < -1.0) & (rsi < 45) & (F["lliq"] > 0.5),
        (c < e200) & (slope < -0.02) & (tide <= 0) & (vz > 1.0) & (rsi > 55) & (F["sliq"] > 0.5),
    )
    # E5: T2 original (sweep reclaim)
    specs["E5_t2_sweep"] = (
        (lo <= F["s_val"]) & (c > F["s_val"]) & (vz < -0.5) & (zc > 0.03) & (c > e200) & (tide >= 0),
        (h >= F["s_vah"]) & (c < F["s_vah"]) & (vz > 0.5) & (zc < -0.03) & (c < e200) & (tide <= 0) & (F["sliq"] < 1.0),
    )
    return specs


def main():
    frames = {}
    for sym in CORE_SYMBOLS:
        p = DATA_DIR / f"{sym}_15m_master_2020_2026.parquet"
        if not p.exists():
            continue
        df = pd.read_parquet(p, columns=COLS_TO_LOAD)
        df = df[df.open_time_ms < DESIGN_CUTOFF].reset_index(drop=True)
        frames[sym] = df

    rows = []
    for sym, df in frames.items():
        F = enrich(df)
        c, h, lo, atr, t, olc, osc = build_conditions(df, btc_tide)
        specs = suite_specs(F)
        specs["ORIG_suite"] = (olc, osc)
        specs["INV_suite"] = (osc.copy(), olc.copy())

        for name, masks in specs.items():
            lc, sc = masks
            lc = np.asarray(lc, bool) & ~np.asarray(sc, bool)
            sc = np.asarray(sc, bool) & ~np.asarray(lc, bool)
            if lc.sum() + sc.sum() < 30:
                continue
            for (hz, tg, st, bt, bl) in GEOS:
                ic, sd, ly, rr, bh = label_triple_barriers_numba(
                    c, h, lo, atr, lc, sc, hz, tg, st, bt, bl, 1.4, 0.8, 0.25)
                idx = np.where(ic)[0]
                if len(idx) < 30:
                    continue
                r = rr[idx]
                wins = r[r > 0]
                rows.append({
                    "spec": name, "hz": hz, "tg": tg, "st": st,
                    "n": len(r), "mean_r": r.mean(),
                    "wr": (r > 0).mean() * 100,
                    "pf": wins.sum() / max(-r[r < 0].sum(), 1e-9),
                })

    d = pd.DataFrame(rows)
    agg = d.groupby("spec").agg(
        n=("n", "sum"), mean_r=("mean_r", "mean"), wr=("wr", "mean"), pf=("pf", "mean")
    ).round(4).sort_values("mean_r", ascending=False)
    print("=== PER-SPEC AVERAGES (design period, net of 0.25R friction) ===")
    print(agg.to_string())
    print("\n=== TOP 15 SPEC x GEOMETRY ===")
    print(d.sort_values("mean_r", ascending=False).head(15).round(4).to_string(index=False))
    d.to_csv("scratch/entry_spec_results.csv", index=False)


if __name__ == "__main__":
    main()
