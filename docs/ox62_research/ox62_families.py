"""OX62 entry families: exact protocol §3 formulas. Signal bar i uses bars ≤ i only."""
import numpy as np
import pandas as pd

CANONICAL = {"F1": {"N": 20}, "F2": {"K": 60}, "F3": {"X": 30}, "F4": {"f": 12, "s": 48},
             "F5": {"k": 2.0}, "F6": {"d": 1.0}, "F7": {"t": 0.5}, "F8": {}}
GRIDS = {"F1": [{"N": 20}, {"N": 55}], "F2": [{"K": 20}, {"K": 60}],
         "F3": [{"X": 25}, {"X": 30}], "F4": [{"f": 12, "s": 48}, {"f": 24, "s": 96}],
         "F5": [{"k": 1.5}, {"k": 2.5}], "F6": [{"d": 1.0}, {"d": 1.5}],
         "F7": [{"t": 0.25}, {"t": 0.5}], "F8": [{}]}
NAMES = {"F1": "Donchian", "F2": "TSMOM", "F3": "RSI-MR", "F4": "MA-cross",
         "F5": "Keltner-cross", "F6": "Sweep-reclaim", "F7": "KZ-drift", "F8": "Rule-FVG"}


def _b(x):
    return pd.Series(np.asarray(x, dtype=bool), index=getattr(x, "index", None))


def sig_F1(df, p):
    n = p["N"]
    return (_b(df["close"] > df[f"hh_{n}"]), _b(df["close"] < df[f"ll_{n}"]))


def sig_F2(df, p):
    k = p["K"]
    ret = df["close"] / df["close"].shift(k) - 1.0
    return (_b(ret > 0), _b(ret < 0))


def sig_F3(df, p):
    x = p["X"]
    return (_b(df["rsi_14"] < x), _b(df["rsi_14"] > 100 - x))


def sig_F4(df, p):
    f, s = df[f"ema_{p['f']}"], df[f"ema_{p['s']}"]
    return (_b((f > s) & (f.shift(1) <= s.shift(1))), _b((f < s) & (f.shift(1) >= s.shift(1))))


def sig_F5(df, p):
    mid, atr = df["ema_20"], df["atr_14"]
    up, lo = mid + p["k"] * atr, mid - p["k"] * atr
    c = df["close"]
    return (_b((c > up) & (c.shift(1) <= up.shift(1))), _b((c < lo) & (c.shift(1) >= lo.shift(1))))


def sig_F6(df, p):
    d = p["d"]
    disp = (df["high"] - df["low"]) > d * df["atr_14"]
    l = _b((df["sweep_pdl"] == 1) & (df["close"] > df["pdl"]) & disp & (df["htf_4h_trend"] > 0))
    s = _b((df["sweep_pdh"] == 1) & (df["close"] < df["pdh"]) & disp & (df["htf_4h_trend"] < 0))
    return (l, s)


def sig_F7(df, p):
    at1030 = (df["_hh"] == 10) & (df["_mn"] == 45)
    drift = df["close"] - df["_sess_open"]
    thr = p["t"] * df["atr_14"]
    return (_b(at1030 & (drift > thr)), _b(at1030 & (drift < -thr)))


def sig_F8(df, p):
    # Exact vectorization of check_setup_criteria (col-first, hour-fallback).
    kz_col = df["is_kill_zone"].values if "is_kill_zone" in df.columns else np.zeros(len(df), bool)
    hh = df["hour"].values if "hour" in df.columns else df["_hh"].values
    kz = kz_col | np.isin(hh, [7, 8, 9, 10, 12, 13, 14, 15])
    l = _b(kz & (df["sweep_pdl"].values == 1) & (df["bullish_fvg"].values > 0) & (df["htf_4h_trend"].values > 0))
    s = _b(kz & (df["sweep_pdh"].values == 1) & (df["bearish_fvg"].values > 0) & (df["htf_4h_trend"].values < 0))
    return (l, s)


SIG = {"F1": sig_F1, "F2": sig_F2, "F3": sig_F3, "F4": sig_F4,
       "F5": sig_F5, "F6": sig_F6, "F7": sig_F7, "F8": sig_F8}
