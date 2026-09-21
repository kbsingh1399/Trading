"""OX62 signal unit tests: trigger + no-lookahead per family, uniform gates, F8 equivalence.
Usage: /home/user/ox61venv/bin/python docs/ox62_research/test_ox62_signals.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))

from ox62_lib import add_harness_cols, generate_candidates
from ox62_families import SIG
from Engine.core.strategy_kernel import check_setup_criteria

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

def mkframe(n=80, start="2025-01-01 07:00", px=100.0):
    dts = pd.date_range(start=start, periods=n, freq="15min", tz="UTC")
    df = pd.DataFrame({"datetime": dts, "open": np.full(n, px), "high": np.full(n, px + 0.05),
                       "low": np.full(n, px - 0.05), "close": np.full(n, px)})
    df = add_harness_cols(df)
    df["hour"] = df["_hh"]
    df["rsi_14"] = 50.0
    df["htf_4h_trend"] = 0.0
    df["sweep_pdl"] = 0
    df["sweep_pdh"] = 0
    df["bullish_fvg"] = 0.0
    df["bearish_fvg"] = 0.0
    df["atr_14"] = 1.0
    df["local_low_20"] = px - 1.0
    df["local_high_20"] = px + 4.0
    df["is_kill_zone"] = df["_hh"].isin([7, 8, 9, 10, 12, 13, 14, 15]).values
    return df

def test_F1():
    df = mkframe()
    df.loc[20, "close"] = 101.0  # 12:00 bar breaks 20-bar high 100.05
    l, s = SIG["F1"](df, {"N": 20})
    ok_trig = bool(l.iloc[20]) and not bool(l.iloc[19])
    df2 = df.copy()
    df2.loc[21, ["open", "high", "low", "close"]] = [200.0, 201.0, 199.0, 200.0]
    df2 = add_harness_cols(df2[["datetime", "open", "high", "low", "close"]])
    l2, _ = SIG["F1"](df2, {"N": 20})
    check("S1 donchian-trigger+future-blind", ok_trig and bool(l2.iloc[20]) and not bool(l2.iloc[19]))

def test_F2():
    df = mkframe(n=120)
    df.loc[60, "close"] = 110.0  # 60-bar return +10%
    l, s = SIG["F2"](df, {"K": 60})
    ok = bool(l.iloc[60]) and not bool(s.iloc[60])
    df.loc[61, "close"] = 50.0  # future crash must not flip bar-60 signal
    l2, _ = SIG["F2"](df, {"K": 60})
    check("S2 tsmom-trigger+future-blind", ok and bool(l2.iloc[60]))

def test_F3():
    df = mkframe()
    df.loc[8, "rsi_14"] = 22.0
    df.loc[9, "rsi_14"] = 30.0  # boundary: strict < required
    l, s = SIG["F3"](df, {"X": 30})
    check("S3 rsi-threshold+boundary", bool(l.iloc[8]) and not bool(l.iloc[9]) and not bool(s.iloc[8]))

def test_F4():
    df = mkframe()
    df.loc[7, ["ema_12", "ema_48"]] = [99.0, 100.0]
    df.loc[8, ["ema_12", "ema_48"]] = [101.0, 100.0]
    l, s = SIG["F4"](df, {"f": 12, "s": 48})
    ok = bool(l.iloc[8]) and not bool(l.iloc[7])
    df.loc[9, ["ema_12", "ema_48"]] = [50.0, 200.0]
    l2, _ = SIG["F4"](df, {"f": 12, "s": 48})
    check("S4 macross-event+future-blind", ok and bool(l2.iloc[8]) and not bool(l2.iloc[9]))

def test_F5():
    df = mkframe()
    df.loc[7, ["close", "ema_20", "atr_14"]] = [101.0, 100.0, 1.0]
    df.loc[8, ["close", "ema_20", "atr_14"]] = [103.0, 100.0, 1.0]  # cross above 102
    l, s = SIG["F5"](df, {"k": 2.0})
    check("S5 keltner-cross", bool(l.iloc[8]) and not bool(l.iloc[7]))

def test_F6():
    df = mkframe(n=140, start="2024-12-31 07:00")  # Tue->Wed; Wed 09:00 = idx 104
    assert str(df.loc[104, "datetime"]) == "2025-01-01 09:00:00+00:00"
    df.loc[104, "sweep_pdl"] = 1
    df.loc[104, ["close", "high", "low"]] = [100.0, 101.0, 99.0]
    df.loc[104, "htf_4h_trend"] = 0.5
    assert abs(df.loc[104, "pdl"] - 99.95) < 1e-9  # Tue low, causal
    l, s = SIG["F6"](df, {"d": 1.0})
    ok = bool(l.iloc[104])
    df2 = df.copy()
    df2.loc[105, "low"] = 50.0  # future dip must not alter bar-104 pdl/signal
    df2 = add_harness_cols(df2[["datetime", "open", "high", "low", "close"]])
    df2["sweep_pdl"] = df["sweep_pdl"].values
    df2["sweep_pdh"] = df["sweep_pdh"].values
    df2["htf_4h_trend"] = df["htf_4h_trend"].values
    df2["atr_14"] = 1.0
    l2, _ = SIG["F6"](df2, {"d": 1.0})
    pdl_same = abs(df2.loc[104, "pdl"] - 99.95) < 1e-9
    check("S6 sweep-reclaim+future-blind", ok and bool(l2.iloc[104]) and pdl_same)

def test_F7():
    df = mkframe()
    assert str(df.loc[15, "datetime"]) == "2025-01-01 10:45:00+00:00"
    df.loc[15, "close"] = 101.0  # drift +1.0 over session open 100.0, thr 0.5
    l, s = SIG["F7"](df, {"t": 0.5})
    n_sig = int(l.sum() + s.sum())
    check("S7 kz-drift-once-per-day", bool(l.iloc[15]) and n_sig == 1, f"nsig={n_sig}")

def test_F8():
    df = mkframe()
    df.loc[8, "sweep_pdl"] = 1
    df.loc[8, "bullish_fvg"] = 1.0
    df.loc[8, "htf_4h_trend"] = 1.0
    l, s = SIG["F8"](df, {})
    ok_trig = bool(l.iloc[8])
    rng = np.random.default_rng(7)
    rows = []
    for _ in range(200):
        rows.append({"is_kill_zone": bool(rng.integers(0, 2)), "hour": int(rng.integers(0, 24)),
                     "sweep_pdl": int(rng.integers(0, 2)), "sweep_pdh": int(rng.integers(0, 2)),
                     "bullish_fvg": float(rng.integers(0, 2)), "bearish_fvg": float(rng.integers(0, 2)),
                     "htf_4h_trend": float(rng.integers(-1, 2))})
    t = pd.DataFrame(rows)
    kz = t["is_kill_zone"] | t["hour"].isin([7, 8, 9, 10, 12, 13, 14, 15])
    lv = (kz & (t["sweep_pdl"] == 1) & (t["bullish_fvg"] > 0) & (t["htf_4h_trend"] > 0)).tolist()
    sv = (kz & (t["sweep_pdh"] == 1) & (t["bearish_fvg"] > 0) & (t["htf_4h_trend"] < 0)).tolist()
    ref = [check_setup_criteria(r) for r in rows]
    equiv = all((a == r[0] and b == r[1]) for a, b, r in zip(lv, sv, ref))
    check("S8 rule-fvg-trigger+kernel-equiv", ok_trig and equiv)

def test_gates():
    df = mkframe(n=60)
    # idx 8 (09:00 KZ) valid long setup -> candidate; idx 36 (16:00 off-hours) -> gated
    df.loc[8, "local_low_20"] = 99.0
    df.loc[8, "local_high_20"] = 104.0
    df.loc[9, "open"] = 100.0
    df.loc[10, ["open", "high", "low"]] = [100.0, 104.2, 99.9]
    lm = pd.Series(False, index=df.index)
    sm = pd.Series(False, index=df.index)
    lm.iloc[8] = True
    lm.iloc[36] = True
    out = generate_candidates(df, lm, sm, df["datetime"].iloc[0])
    ok_kz = len(out) == 1 and out["datetime"].iloc[0] == df["datetime"].iloc[8]
    # Friday entry veto: frame Fri 07:00; bar 48 entry Fri 19:15 -> veto; bar 32 (15:00 KZ) -> ok
    f = mkframe(n=60, start="2025-01-03 07:00")
    f.loc[32, "local_low_20"] = 99.0
    f.loc[32, "local_high_20"] = 104.0
    f.loc[33, "open"] = 100.0
    f.loc[34, ["open", "high", "low"]] = [100.0, 104.2, 99.9]
    f.loc[48, "local_low_20"] = 99.0
    f.loc[49, "open"] = 100.0
    lm2 = pd.Series(False, index=f.index)
    lm2.iloc[32] = True
    lm2.iloc[48] = True
    out2 = generate_candidates(f, lm2, sm.iloc[:60] & False, f["datetime"].iloc[0])
    ok_fri = len(out2) == 1 and out2["datetime"].iloc[0] == f["datetime"].iloc[32]
    check("S9 kz-gate+friday-veto", ok_kz and ok_fri, f"kz_n={len(out)} fri_n={len(out2)}")

if __name__ == "__main__":
    print("OX62 signal unit tests:")
    test_F1(); test_F2(); test_F3(); test_F4(); test_F5(); test_F6(); test_F7(); test_F8(); test_gates()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
