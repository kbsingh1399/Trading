"""MAX grid: exit-geometry search on causal design period (pre-W01 only).

Scores each geometry by per-candidate net expectancy (friction inclusive),
profit factor, and quarter-robustness (min quarterly mean net r) so we do
not select a bull-only artifact.
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

PURGE_MS = 72 * 3600 * 1000
DESIGN_CUTOFF = pd.Timestamp("2021-05-01", tz="UTC").value // 1_000_000 - PURGE_MS

btc_tide = load_btc_macro_tide()


def build_conditions(df, btc_tide):
    c, h, lo = df.close.to_numpy(float), df.high.to_numpy(float), df.low.to_numpy(float)
    t = df.open_time_ms.to_numpy(np.int64)
    atr_raw = df["atr_14"].fillna(df["close"] * 0.01).to_numpy(float)
    atr = np.maximum(atr_raw, df["close"].to_numpy(float) * 0.012)
    atr_100 = df["atr_100"].fillna(df["close"] * 0.01).to_numpy(float)
    atr_ratio = np.clip(np.where(atr_100 > 0, atr / atr_100, 1.0), 0.2, 5.0)
    e200 = df["ema_200"].to_numpy(float)
    slope = ((df["ema_200"] - df["ema_200"].shift(12)) / df["close"]).fillna(0.0).to_numpy(float)
    tide = pd.Series(t).map(btc_tide).fillna(0.0).to_numpy(float)
    vwap_z = df["vwap_zscore"].fillna(0.0).to_numpy(float)
    vol_ratio = df["volume_ratio"].fillna(1.0).to_numpy(float)
    zc_norm = (df["zc_div"] / df["volume_base"].replace(0, 1.0)).clip(-3, 3).fillna(0).to_numpy(float)
    short_liq = df["short_liq_zs"].fillna(0.0).to_numpy(float)
    s_val = df["session_val"].fillna(df["low"]).to_numpy(float)
    s_vah = df["session_vah"].fillna(df["high"]).to_numpy(float)
    taker = df["taker_volume_ratio"].fillna(1.0).to_numpy(float)

    t1_l = (atr_ratio < 0.85) & (vol_ratio >= 1.6) & (slope > 0.05) & (c > e200) & (tide >= 0)
    t1_s = (atr_ratio < 0.85) & (vol_ratio >= 1.6) & (slope < -0.05) & (c < e200) & (tide <= 0)
    t2_l = (lo <= s_val) & (c > s_val) & (vwap_z < -0.5) & (zc_norm > 0.03) & (c > e200)
    t2_s = (h >= s_vah) & (c < s_vah) & (vwap_z > 0.5) & (zc_norm < -0.03) & (c < e200) & (short_liq < 1.0)
    t3_l = (taker >= 1.3) & (vol_ratio >= 1.5) & (zc_norm >= 0.06) & (slope > 0.08) & (tide >= 0)
    t3_s = (taker <= 0.7) & (vol_ratio >= 1.5) & (zc_norm <= -0.06) & (slope < -0.08) & (tide <= 0)

    lc = (t1_l | t2_l | t3_l)
    sc = (t1_s | t2_s | t3_s)
    lc = lc & ~sc
    sc = sc & ~lc
    return c, h, lo, atr, t, lc.astype(bool), sc.astype(bool)


def main():
    frames = {}
    for sym in CORE_SYMBOLS:
        p = DATA_DIR / f"{sym}_15m_master_2020_2026.parquet"
        if not p.exists():
            continue
        df = pd.read_parquet(p, columns=COLS_TO_LOAD)
        df = df[df.open_time_ms < DESIGN_CUTOFF].reset_index(drop=True)
        frames[sym] = build_conditions(df, btc_tide)

    results = []
    for hz in (24, 48, 96):
        for target in (1.5, 2.0, 2.5):
            for stop in (0.75, 1.0):
                for be_trig, be_lock in ((0.75, 0.35), (0.95, 0.45), (1.2, 0.6)):
                    all_r, all_t = [], []
                    for sym, (c, h, lo, atr, t, lc, sc) in frames.items():
                        ic, sd, ly, rr, bh = label_triple_barriers_numba(
                            c, h, lo, atr, lc, sc, hz, target, stop,
                            be_trig, be_lock, 1.40, 0.80, 0.25)
                        idx = np.where(ic)[0]
                        all_r.append(rr[idx])
                        all_t.append(t[idx])
                    r = np.concatenate(all_r)
                    tt = np.concatenate(all_t)
                    q = pd.to_datetime(tt, unit="ms").to_period("Q")
                    qs = pd.Series(r).groupby(q).mean()
                    gross_win = (r > 0).mean() * 100
                    pf = r[r > 0].sum() / max(-r[r < 0].sum(), 1e-9)
                    results.append({
                        "hz": hz, "target": target, "stop": stop,
                        "be_trig": be_trig, "be_lock": be_lock,
                        "n": len(r), "mean_r": r.mean(), "wr": gross_win,
                        "pf": pf, "min_q_r": qs.min(), "med_q_r": qs.median(),
                    })

    out = pd.DataFrame(results).sort_values("mean_r", ascending=False)
    pd.set_option("display.width", 200)
    print(out.round(4).to_string(index=False))
    out.to_csv("scratch/geometry_grid_results.csv", index=False)


if __name__ == "__main__":
    main()
