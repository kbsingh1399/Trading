"""strategy_battery.py v2 — research-driven candidate generation, trend-weekly upgrade.

Rebuild after workspace revert + NEW core hypothesis: weekly-hold trailing-stop
trend following (the only regime where academic TSMOM edge can amortize 0.25R
friction into the mandated +0.75R/trade gross bar).

Families (causal, shift-invariant):
  T1 donchian 4d breakout in 20d tide          (SURV_W)
  T2 7d time-series momentum sign / strong      (SURV_W)
  T3 pullback in tide                           (SURV_M / SURV_W)
  T4 NR7 compression continuation (retained best fast spec from v1 battery)
  T5 funding-carry timing                       (MID)
  T6 cross-sectional 7d momentum deciles        (SURV_W)
  T7 UTC open-range breakout                    (FAST)
  T8 BTC-lead / alt-lag                         (FAST)
  T9 OI-expansion continuation                  (FAST)

Unified numba labeler: initial 1R stop, one-way BE ratchet, optional time
decay, optional R-trail, horizon exit; 0.25R friction. All exits causal (armed
on bar j, evaluated from j onwards; entry at close of signal bar i).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from numba import njit

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "Engine" / "binance_backtesting_data"
CACHE = REPO / "scratch" / "cache_battery_v2.pkl"
POOL_DIR = REPO / "scratch" / "battery_pools_v2"
RESULTS_CSV = REPO / "scratch" / "battery_stage1_results_v2.csv"

FRICTION_R = 0.25

GEOS = {
    # name: (horizon, be_arm, be_lock, decay_bars, decay_min, trail_arm, trail_k, cooldown, r_scale_bars)
    # r_scale_bars: R-unit = atr_pct * sqrt(r_scale/14) so a 1R stop spans that
    # horizon's noise, not one 15m bar. FAST=1bar, MID=4h, SURV_M=16h, SURV_W=64h.
    "FAST":   (48,   0.75, 0.35, 24, 0.20, -1.0, 1.0, 16, 14.0),
    "MID":    (96,   0.75, 0.35, 96, 0.30, -1.0, 1.0, 48, 224.0),
    "SURV_M": (672,  0.90, 0.10, 0,  0.0,   1.0, 1.5, 48, 896.0),
    "SURV_W": (1344, 1.00, 0.15, 0,  0.0,   1.2, 1.8, 96, 3584.0),
    "SURV_WD": (1344, 1.00, 0.15, 672, 0.50, 1.2, 1.8, 96, 3584.0),
}


@njit(cache=True)
def label_candidates_numba(close, high, low, atr_pct, idx, side,
                           horizon, be_arm, be_lock, decay_bars, decay_min,
                           trail_arm, trail_k, friction):
    n = len(idx)
    out_r = np.empty(n, dtype=np.float64)
    out_b = np.empty(n, dtype=np.int32)
    m = len(close)
    for k in range(n):
        i = idx[k]
        s = side[k]
        entry = close[i]
        a = atr_pct[i]
        if a <= 0 or i + 1 >= m:
            out_r[k] = 0.0
            out_b[k] = 0
            continue
        stop_r = -1.0
        best_r = 0.0
        j_end = i + horizon
        if j_end >= m:
            j_end = m - 1
        r_out = 0.0
        b_out = 0
        for j in range(i + 1, j_end + 1):
            # adverse extreme first (conservative fill at stop price)
            stop_px = entry * (1.0 + s * stop_r * a)
            hit = (low[j] <= stop_px) if s > 0 else (high[j] >= stop_px)
            move = s * (close[j] - entry) / entry / a
            if hit:
                r_out = stop_r - friction
                b_out = j - i
                break
            if move > best_r:
                best_r = move
            # one-way BE ratchet
            if be_arm > 0 and best_r >= be_arm and be_lock > stop_r:
                stop_r = be_lock
            # R-trail
            if trail_arm > 0 and best_r >= trail_arm:
                ts = best_r - trail_k
                if ts > stop_r:
                    stop_r = ts
            # time decay at exactly decay_bars with no progress
            if decay_bars > 0 and (j - i) == decay_bars and best_r + (move - best_r) < decay_min and move < decay_min:
                r_out = move - friction
                b_out = j - i
                break
            if j == j_end:
                r_out = move - friction
                b_out = j - i
                break
        out_r[k] = r_out
        out_b[k] = b_out
    return out_r, out_b


def _z(s: pd.Series, win: int = 672) -> pd.Series:
    mu = s.rolling(win, min_periods=win // 2).mean().shift(1)
    sd = s.rolling(win, min_periods=win // 2).std().shift(1)
    return (s - mu) / sd.replace(0, np.nan)


def build_store() -> dict:
    store = {}
    frames = {}
    paths = sorted(DATA_DIR.glob("*_15m_master_2020_2026.parquet"))
    syms = [p.name.split("_15m_master")[0] for p in paths]
    print(f"[battery] symbols: {syms}", flush=True)
    btc_close = None
    for sym, p in zip(syms, paths):
        df = pd.read_parquet(p)
        df = df.sort_values("open_time_ms").reset_index(drop=True)
        c, h, l = df["close"], df["high"], df["low"]
        df["atr_pct"] = (df["atr_14"] / c).replace(0, np.nan)
        for k in (4, 16, 96, 288, 672, 1344):
            df[f"ret_{k}"] = c.pct_change(k)
        df["donch_hi_384"] = h.rolling(384).max().shift(1)
        df["donch_lo_384"] = l.rolling(384).min().shift(1)
        df["dist90hi"] = c / c.rolling(8640, min_periods=4320).max().shift(1) - 1.0
        df["tide"] = np.where(c > df["ema_800"], 1, -1)
        df["vol_sig_672"] = df["atr_pct"] * np.sqrt(672)  # ~weekly vol in pct
        df["r7_z"] = df["ret_672"] / df["vol_sig_672"]
        df["fund_z"] = _z(df["funding_rate_pct"].fillna(0.0))
        df["basis_z"] = _z(df["basis_index_bps"].fillna(0.0))
        df["oi_z"] = _z(df["oi_change_pct"].fillna(0.0))
        df["lst_z"] = _z(df["ls_ratio_top"].fillna(50.0))
        nr6 = (h.rolling(6).max() - l.rolling(6).min()) / c
        df["nr_flag"] = (nr6 <= nr6.rolling(672, min_periods=200).min().shift(1)).fillna(False)
        df["atr_ratio"] = (df["atr_14"] / df["atr_100"].replace(0, np.nan)).fillna(1.0)
        ts = pd.to_datetime(df["open_time_ms"], unit="ms", utc=True)
        df["hour"] = ts.dt.hour
        df["dow"] = ts.dt.dayofweek
        df["day"] = ts.dt.normalize()
        df["bar_of_day"] = df.groupby("day").cumcount()
        df["mom_3d"] = df["ret_288"]
        # prev day return (strictly prior day)
        dclose = df.groupby("day")["close"].last()
        df["prev_day_ret"] = df["day"].map(dclose.pct_change().shift(1))
        # ORB: first 4 bars of day, available from bar 4 onward
        orb = df[df.bar_of_day < 4].groupby("day").agg(orb_hi=("high", "max"), orb_lo=("low", "min"))
        df["orb_hi"] = df["day"].map(orb["orb_hi"])
        df["orb_lo"] = df["day"].map(orb["orb_lo"])
        df.loc[df.bar_of_day < 4, ["orb_hi", "orb_lo"]] = np.nan
        df[["orb_hi", "orb_lo"]] = df.groupby("day")[["orb_hi", "orb_lo"]].ffill()
        if sym == "BTCUSDT":
            btc_close = df[["open_time_ms", "close"]].rename(columns={"close": "btc_close"})
        frames[sym] = df
    if btc_close is not None:
        btc_close = btc_close.sort_values("open_time_ms")
        btc_close["btc_ret_288"] = btc_close["btc_close"].pct_change(288)
        bc = btc_close[["open_time_ms", "btc_ret_288"]].dropna()
        for sym in syms:
            df = frames[sym]
            m = pd.merge_asof(df[["open_time_ms"]], bc, on="open_time_ms", direction="backward")
            df["btc_ret_288"] = m["btc_ret_288"].to_numpy()
    # cross-sectional 7d momentum rank (causal, per timestamp)
    print("[battery] cross-sectional ranks...", flush=True)
    xr = pd.DataFrame({sym: frames[sym].set_index("open_time_ms")["ret_672"] for sym in syms})
    xrank = xr.rank(axis=1, pct=True)
    for sym in syms:
        df = frames[sym]
        df["xs_rank"] = df["open_time_ms"].map(xrank[sym])
        # imputation guard: exclude flagged-if-any (keep feature, drop in pool)
        store[sym] = df
    return store


def get_store() -> dict:
    if CACHE.exists():
        print("[battery] loading cache", flush=True)
        return pd.read_pickle(CACHE)
    store = build_store()
    pd.to_pickle(store, CACHE)
    return store


def thin_mask(t: np.ndarray, cooldown_bars: int) -> np.ndarray:
    keep = np.zeros(len(t), dtype=bool)
    last = -(1 << 62)
    cool = cooldown_bars * 900_000
    for k in range(len(t)):
        if t[k] - last >= cool:
            keep[k] = True
            last = t[k]
    return keep


def spec_list():
    """(fam, tag, geo_key) — signal logic lives in spec_candidates()."""
    return [
        ("T1", "donchW_tide", "SURV_W"),
        ("T1", "donchW_free", "SURV_W"),
        ("T2", "tsmom7d",      "SURV_W"),
        ("T2", "tsmom7d_hi15", "SURV_W"),
        ("T3", "pullback_M",   "SURV_M"),
        ("T3", "pullback_W",   "SURV_W"),
        ("T4", "nr7_fast",     "FAST"),
        ("T5", "fund_carry",   "MID"),
        ("T6", "xs_decile",    "SURV_W"),
        ("T7", "orb_fast",     "FAST"),
        ("T8", "btc_lead",     "FAST"),
        ("T9", "oi_break",     "FAST"),
    ]


def spec_signals(fam: str, tag: str, df: pd.DataFrame):
    """Return boolean mask + side array (±1) for raw (pre-cooldown) candidates."""
    if fam == "T1":
        up = df["close"] > df["donch_hi_384"]
        dn = df["close"] < df["donch_lo_384"]
        if tag == "donchW_tide":
            up &= df["tide"] == 1
            dn &= df["tide"] == -1
        mask = (up | dn).fillna(False)
        side = np.where(up, 1, -1)
    elif fam == "T2":
        if tag == "tsmom7d":
            up = df["ret_672"] > 0
            dn = df["ret_672"] < 0
        else:  # hi15
            up = df["r7_z"] > 1.5
            dn = df["r7_z"] < -1.5
        mask = (up | dn).fillna(False)
        side = np.where(up, 1, -1)
    elif fam == "T3":
        up = (df["tide"] == 1) & (df["ret_96"] <= -0.015)
        dn = (df["tide"] == -1) & (df["ret_96"] >= 0.015)
        mask = (up | dn).fillna(False)
        side = np.where(up, 1, -1)
    elif fam == "T4":
        side = np.sign(df["ret_16"].fillna(0).to_numpy())
        side = np.where(side == 0, 1, side)
        mask = df["nr_flag"].fillna(False)
    elif fam == "T5":
        up = df["fund_z"] < -1.0
        dn = df["fund_z"] > 1.0
        mask = (up | dn).fillna(False)
        side = np.where(up, 1, -1)
    elif fam == "T6":
        up = df["xs_rank"] > 0.89
        dn = df["xs_rank"] < 0.11
        mask = (up | dn).fillna(False)
        side = np.where(up, 1, -1)
    elif fam == "T7":
        cond = df["bar_of_day"].between(4, 10)
        up = cond & (df["close"] > df["orb_hi"])
        dn = cond & (df["close"] < df["orb_lo"])
        mask = (up | dn).fillna(False)
        side = np.where(up, 1, -1)
    elif fam == "T8":
        up = (df["btc_ret_288"] > 0.01) & (df["ret_288"] < 0)
        dn = (df["btc_ret_288"] < -0.01) & (df["ret_288"] > 0)
        mask = (up | dn).fillna(False)
        side = np.where(up, 1, -1)
    elif fam == "T9":
        up = (df["oi_z"] > 1.5) & (df["ret_16"] > 0)
        dn = (df["oi_z"] > 1.5) & (df["ret_16"] < 0)
        mask = (up | dn).fillna(False)
        side = np.where(up, 1, -1)
    else:
        raise ValueError(fam)
    return mask, side.astype(np.int8)


NEEDS_METRIC = {"T5", "T9"}  # signal inputs are ancillary metrics; synthetic-imputed rows must not trade

def spec_candidates(store: dict, fam: str, tag: str) -> pd.DataFrame:
    geo_key = dict(((f, t), g) for f, t, g in spec_list())[(fam, tag)]
    horizon, be_arm, be_lock, decay_bars, decay_min, trail_arm, trail_k, cd, r_scale = GEOS[geo_key]
    r_mult = float(np.sqrt(r_scale / 14.0))
    parts = []
    for sym, df in store.items():
        mask, side = spec_signals(fam, tag, df)
        if fam in NEEDS_METRIC:
            mask = mask & (~df["is_imputed_metrics"].fillna(False))
        idx = np.flatnonzero(mask.to_numpy())
        if len(idx) == 0:
            continue
        t = df["open_time_ms"].to_numpy()[idx]
        keep = thin_mask(t, cd)
        idx = idx[keep]
        if len(idx) == 0:
            continue
        r, bars = label_candidates_numba(
            df["close"].to_numpy(), df["high"].to_numpy(), df["low"].to_numpy(),
            (df["atr_pct"].fillna(0) * r_mult).to_numpy().astype(np.float64),
            idx.astype(np.int64), side[idx].astype(np.int64),
            horizon, be_arm, be_lock, decay_bars, decay_min,
            trail_arm, trail_k, FRICTION_R)
        parts.append(pd.DataFrame({"t": df["open_time_ms"].to_numpy()[idx],
                                   "r": r, "side": side[idx], "bars": bars, "sym": sym}))
    if not parts:
        return pd.DataFrame(columns=["t", "r", "side", "bars", "sym"])
    return pd.concat(parts, ignore_index=True).sort_values("t").reset_index(drop=True)


def main():
    t_all = time.perf_counter()
    store = get_store()
    # warm JIT once on BTC
    df0 = store["BTCUSDT"]
    label_candidates_numba(df0["close"].to_numpy()[:2000], df0["high"].to_numpy()[:2000],
                           df0["low"].to_numpy()[:2000],
                           df0["atr_pct"].fillna(0).to_numpy()[:2000].astype(np.float64),
                           np.array([100, 500], dtype=np.int64), np.array([1, -1], dtype=np.int64),
                           48, 0.75, 0.35, 24, 0.2, -1.0, 1.0, FRICTION_R)
    rows = []
    POOL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{'FAM':<4} | {'tag':<13} | {'geo':<7} | {'n':>7} | {'netR':>8} | {'grossR':>8} | {'WR%':>6} | {'pf_net':>7} | {'avgbars':>8}", flush=True)
    for fam, tag, geo_key in spec_list():
        pool = spec_candidates(store, fam, tag)
        pool.to_parquet(POOL_DIR / f"{fam}__{tag}.parquet", index=False)
        n = len(pool)
        wr = (pool.r > 0).mean() * 100 if n else 0
        net = pool.r.mean() if n else 0
        gross = net + FRICTION_R
        gains = pool.loc[pool.r > 0, "r"].sum()
        losses = -pool.loc[pool.r <= 0, "r"].sum()
        pf = gains / losses if losses > 0 else np.nan
        print(f"{fam:<4} | {tag:<13} | {geo_key:<7} | {n:>7d} | {net:>+8.4f} | {gross:>+8.4f} | {wr:>5.1f}% | {pf:>7.3f} | {pool.bars.mean() if n else 0:>8.0f}", flush=True)
        rows.append({"fam": fam, "tag": tag, "geo": geo_key, "n": n, "net_r": net,
                     "gross_r": gross, "wr": wr, "pf": pf, "avg_bars": pool.bars.mean() if n else 0})
    res = pd.DataFrame(rows).sort_values("net_r", ascending=False)
    res.to_csv(RESULTS_CSV, index=False)
    print(res.to_string(index=False), flush=True)
    print(f"[battery] done in {time.perf_counter()-t_all:.0f}s → {POOL_DIR}", flush=True)


if __name__ == "__main__":
    main()
