"""OX64 unit tests: daily plumbing, A/B/C signals, causality, availability gates.
Usage: /home/user/ox61venv/bin/python docs/ox64_research/test_ox64_signals.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "ox62_research"))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "ox63_research"))

from ox64_lib import (daily_bars, add_trailing_stats, generate_candidates_A,  # noqa: E402
                      generate_candidates_B, generate_candidates_C, HORIZON_REASON)
from ox62_lib import load_frame, add_harness_cols, generate_candidates  # noqa: E402
from ox63_lib import add_msb_anchor, sig_F6R  # noqa: E402

PASS, FAIL = [], []
W01 = pd.Timestamp("2023-09-15", tz="UTC")

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")


def synth_15m(days, start="2023-01-02", bpd=20, close_fn=None, kz_all=True):
    base = pd.Timestamp(start, tz="UTC")
    frames = []
    for i in range(days):
        dts = pd.date_range(base + pd.Timedelta(days=i), periods=bpd, freq="15min")
        c = close_fn(i) if close_fn else 100.0
        n = len(dts)
        frames.append(pd.DataFrame({"datetime": dts, "open": c, "high": c + 0.5,
                                    "low": c - 0.5, "close": c,
                                    "is_kill_zone": np.ones(n, bool) if kz_all else np.zeros(n, bool)}))
    return pd.concat(frames, ignore_index=True)


def test_daily_resample():
    df = synth_15m(3, bpd=12)
    df = df.drop(df.index[12:19]).reset_index(drop=True)  # day2 -> 5 bars (<10)
    d = daily_bars(df)
    t = add_trailing_stats(d)
    ok = (len(d) == 3 and d["trading"].tolist() == [True, False, True]
          and abs(d["day_high"].iloc[0] - 100.5) < 1e-9 and len(t) == 2
          and abs(t["day_ret"].iloc[1] - 0.0) < 1e-9)
    check("T1 daily-resample+Q0-gate", ok, f"trading={d['trading'].tolist()}")


def test_A_formation_and_mechanics():
    df = synth_15m(300, close_fn=lambda i: 100.0 * (1 + 0.0004 * i))
    t = add_trailing_stats(daily_bars(df))
    span = df["datetime"].iloc[0].floor("D")
    A = generate_candidates_A(df, t, span)
    first = t["_day"].iloc[252]
    ok_gate = len(A) > 0 and (A["datetime"] >= first).all()
    r0 = A.iloc[0]
    # hand calc: R = 1.5 * ATR20; ATR20 = mean daily range = 1.0 + drift effect...
    S = t[t["_day"] == r0["datetime"]].iloc[0]
    R = 1.5 * S["atr20"]
    entry = df["open"].iloc[int(S["last_idx"]) + 1]  # all-KZ: next bar
    # exit = next month-end close: recompute independently
    ym = S["_day"].strftime("%Y-%m")
    ym_next = (S["_day"] + pd.offsets.MonthBegin(1)).strftime("%Y-%m")
    E = t[t["_day"].dt.strftime("%Y-%m") == ym_next].iloc[-1]
    exit_c = df["close"].iloc[int(E["last_idx"])]
    expect = round((exit_c - entry) / R - 0.08, 4)  # LONG (up-trend)
    ok_math = (r0["signal"] == 1 and abs(r0["r_realized"] - expect) < 1e-9
               and r0["hold_bars"] == int(E["last_idx"]) - (int(S["last_idx"]) + 1)
               and r0["exit_reason"] == 4)
    check("T2 A-formation-gate", ok_gate, f"n={len(A)} first={A['datetime'].min().date()}")
    check("T3 A-entry-exit-math", ok_math, f"r={r0['r_realized']} expect={expect}")


def test_B_threshold():
    def cf(i):
        if i < 21:
            return 100.0 * (1 + (0.001 if i % 2 else -0.001) * 1)
        if i == 25:
            return 101.0
        if i == 26:
            return 99.0
        return 100.0
    df = synth_15m(35, close_fn=cf)
    t = add_trailing_stats(daily_bars(df))
    span = df["datetime"].iloc[0].floor("D")
    B = generate_candidates_B(df, t, span)
    sig = {pd.Timestamp(d).date(): s for d, s in zip(B["datetime"], B["signal"])}
    d25 = (df["datetime"].iloc[0] + pd.Timedelta(days=25)).date()
    d26 = (df["datetime"].iloc[0] + pd.Timedelta(days=26)).date()
    ok = (sig.get(d25) == -1 and sig.get(d26) == 1
          and (B["exit_reason"] == 4).all() and (B["hold_bars"] >= 1).all())
    check("T4 B-threshold-fade", ok, f"signals={sig}")


def test_C_property():
    df = add_msb_anchor(add_harness_cols(load_frame("EURUSD")))
    t = add_trailing_stats(daily_bars(df))
    lm, sm = sig_F6R(df)
    mono = generate_candidates(df, lm, sm, W01)
    C = generate_candidates_C(df, t, W01)
    keys = (mono[["datetime", "signal", "hold_bars", "exit_reason"]].reset_index(drop=True)
            == C[["datetime", "signal", "hold_bars", "exit_reason"]].reset_index(drop=True)).all().all()
    expect_r = round((mono["r_realized"] + 0.08) / C["mult"] - 0.08, 4)
    r_ok = (abs(C["r_realized"] - expect_r) < 1e-3).all()
    mult_ok = ((C["mult"] >= 0.5) & (C["mult"] <= 2.0)).all()
    check("T5 C-geometry-identical-r-rescaled", len(mono) == len(C) and keys and r_ok and mult_ok,
          f"n={len(C)} mult_range=({C['mult'].min():.2f},{C['mult'].max():.2f})")
    Cs = generate_candidates_C(df, t, W01, scaled=True)
    check("T5b C-scaled-schema", len(Cs) > 0 and "scaled" in Cs.columns and "mult" in Cs.columns,
          f"n={len(Cs)}")


def test_causality():
    df = load_frame("EURUSD")
    cut = df["datetime"].max() - pd.Timedelta(days=70)
    full15, trunc15 = df, df[df["datetime"] < cut].copy()
    for tag, frame in [("full", full15), ("trunc", trunc15)]:
        h = add_msb_anchor(add_harness_cols(frame.copy()))
        tt = add_trailing_stats(daily_bars(frame))
        A = generate_candidates_A(frame, tt, W01)
        B = generate_candidates_B(frame, tt, W01)
        C = generate_candidates_C(h, tt, W01)
        if tag == "full":
            fA, fB, fC = A, B, C
        else:
            tA, tB, tC = A, B, C
    mA = fA["datetime"] < (cut - pd.Timedelta(days=45))
    mB = fB["datetime"] < (cut - pd.Timedelta(days=6))
    mC = fC["datetime"] < (cut - pd.Timedelta(days=6))
    def same(f, tt, m):
        a = f[m].set_index("datetime")["r_realized"]
        b = tt[tt["datetime"].isin(a.index)].set_index("datetime")["r_realized"]
        return len(a) > 0 and len(a) == len(b) and (abs(a - b) < 1e-9).all()
    check("T6 causality-truncate", same(fA, tA, mA) and same(fB, tB, mB) and same(fC, tC, mC),
          f"A={mA.sum()} B={mB.sum()} C={mC.sum()}")


def test_kz_entry_and_gates():
    df = load_frame("EURUSD")
    t = add_trailing_stats(daily_bars(df))
    A = generate_candidates_A(df, t, W01)
    B = generate_candidates_B(df, t, W01)
    kz = df["is_kill_zone"].values
    dts = df["datetime"]
    ok = True
    for cand in (A, B):
        for _, r in cand.iterrows():
            e_last = dts[dts <= r["datetime"]].index.max()  # approx signal-day end
            j = e_last + 1
            while j < len(df) and not bool(kz[j]):
                j += 1
            if not bool(kz[j]):
                ok = False
    check("T7 AB-kz-entries", ok and HORIZON_REASON == 4, f"A={len(A)} B={len(B)}")
    gx = load_frame("XAUCNH")
    tx = add_trailing_stats(daily_bars(gx))
    Ax = generate_candidates_A(gx, tx, W01)
    ok8 = len(Ax) == 0 or (Ax["datetime"].min() > pd.Timestamp("2023-12-31", tz="UTC"))
    check("T8 A-availability-gate-XAUCNH", ok8,
          f"n={len(Ax)} first={Ax['datetime'].min() if len(Ax) else '-'}")
    check("T8b A-nonempty-EURUSD", len(A) > 0, f"first={A['datetime'].min().date()}")


if __name__ == "__main__":
    print("OX64 signal unit tests:")
    test_daily_resample()
    test_A_formation_and_mechanics()
    test_B_threshold()
    test_C_property()
    test_causality()
    test_kz_entry_and_gates()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
