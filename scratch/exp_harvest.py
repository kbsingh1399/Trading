"""REX final experiments: trend-harvest candidates, raw per-window expectancy (no ML).

Candidates: trend-aligned bars thinned by per-symbol cooldown (no local-extreme
event filters). Longs only in up-tide, shorts only in down-tide.
Geometry variants include wide stop/target and ratchet-on/off.
"""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import json
import numpy as np
import pandas as pd
from numba import njit

from scratch.fast_numba_oos_engine import (
    DATA_DIR, WINDOWS_PATH, CORE_SYMBOLS, COLS_TO_LOAD,
    load_btc_macro_tide, warmup_numba,
)
from scratch.fast_numba_oos_engine_v2 import label_ratchet_decay_numba

with open(WINDOWS_PATH) as f:
    WINDOWS = json.load(f)


@njit(fastmath=True)
def thin_mask(cond: np.ndarray, cooldown: int) -> np.ndarray:
    """Keep a candidate only if `cooldown` bars passed since last kept one."""
    out = np.zeros(len(cond), dtype=np.bool_)
    last = -10 ** 9
    for i in range(len(cond)):
        if cond[i] and i - last >= cooldown:
            out[i] = True
            last = i
    return out


def main():
    warmup_numba()
    btc_tide = load_btc_macro_tide()

    per_window = {w["window_id"]: dict(name=w["name"], res={}) for w in WINDOWS}

    COMBOS = {
        # tag: (hz, target, stop, be_trig, be_lock, decay_bars, decay_min_r, cooldown)
        "C_wide96_s000":  (96, 3.0, 1.50, 9.99, 0.35, 48, 0.30, 32, 0.000),
        "C_wide96_s002":  (96, 3.0, 1.50, 9.99, 0.35, 48, 0.30, 32, 0.002),
        "C_wide96_s005":  (96, 3.0, 1.50, 9.99, 0.35, 48, 0.30, 32, 0.005),
        "D_drift48_s002": (48, 2.0, 1.25, 9.99, 0.35, 48, 0.00, 24, 0.002),
        "E_tide_wide":    (96, 3.0, 1.50, 9.99, 0.35, 96, 0.00, 48, 0.002),
    }

    for sym in CORE_SYMBOLS:
        p = DATA_DIR / f"{sym}_15m_master_2020_2026.parquet"
        if not p.exists():
            continue
        df = pd.read_parquet(p, columns=COLS_TO_LOAD)
        c, hh, lo = df.close.to_numpy(float), df.high.to_numpy(float), df.low.to_numpy(float)
        t = df.open_time_ms.to_numpy(np.int64)
        atr_raw = df["atr_14"].fillna(df["close"] * 0.01).to_numpy(float)
        atr = np.maximum(atr_raw, df["close"].to_numpy(float) * 0.012)
        atr_100 = df["atr_100"].fillna(df["close"] * 0.01).to_numpy(float)
        atr_ratio = np.clip(np.where(atr_100 > 0, atr / atr_100, 1.0), 0.2, 5.0)
        e200 = df["ema_200"].to_numpy(float)
        slope = ((df["ema_200"] - df["ema_200"].shift(12)) / df["close"]).fillna(0.0).to_numpy(float)
        tide = pd.Series(t).map(btc_tide).fillna(0.0).to_numpy(float)

        fin = np.isfinite(atr) & (atr > 0)
        win_id = pd.cut(pd.Series(t), bins=[-1] + [pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000 for w in WINDOWS], labels=False).to_numpy()

        for tag, (hz, tg, st, bt, bl, db, dmr, cd, slp) in COMBOS.items():
            long_base = (c > e200) & (slope > slp) & (tide >= 0) & (atr_ratio < 1.35) & fin
            short_base = (c < e200) & (slope < -slp) & (tide <= 0) & (atr_ratio < 1.35) & fin
            lc = thin_mask(long_base, cd)
            sc = thin_mask(short_base, cd)
            ic, sd, ly, rr, bh = label_ratchet_decay_numba(
                c, hh, lo, atr, lc, sc, hz, tg, st, bt, bl, 1.4, 0.8, db, dmr, 0.25)
            idx = np.where(ic)[0]
            if len(idx) == 0:
                continue
            tmp = pd.DataFrame({"t": t[idx], "r": rr[idx], "side": sd[idx]})
            for w in WINDOWS:
                start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
                end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
                sub = tmp[(tmp.t >= start_ms) & (tmp.t <= end_ms)]
                if len(sub) >= 5:
                    agg = per_window[w["window_id"]]["res"].setdefault(tag, {"n": 0, "sum_r": 0.0})
                    agg["n"] += len(sub)
                    agg["sum_r"] += float(sub.r.sum())

    print(f"{'W#':<4}{'window':<40}" + "".join(f"{tag:>18}" for tag in COMBOS))
    for w in WINDOWS:
        row = f"W{w['window_id']:<3} {w['name'][:38]:<40}"
        for tag in COMBOS:
            d = per_window[w["window_id"]]["res"].get(tag)
            if d and d["n"] >= 5:
                row += f"{d['n']:>5}x{d['sum_r']/d['n']:+.3f}R  "
            else:
                row += f"{'--':>18}"
        print(row)

    # Aggregate scoreboard: mean per-window expectancy
    print("\n=== AGGREGATE (sum of per-window mean_r across windows) ===")
    for tag in COMBOS:
        vals, ns = [], 0
        for w in WINDOWS:
            d = per_window[w["window_id"]]["res"].get(tag)
            if d and d["n"] >= 5:
                vals.append(d["sum_r"] / d["n"])
                ns += d["n"]
        vals = np.array(vals)
        print(f"{tag:<14}: windows_with_edge={int((vals>0).sum()):>2d}/20  avg_win_mean_r={vals.mean() if len(vals) else 0:+.4f}R  total_candidates={ns}")


if __name__ == "__main__":
    main()
