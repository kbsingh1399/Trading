"""OX63 unit tests: MSB anchor causality, F6R expansion, scaled-candidate veto/parity.
Usage: /home/user/ox61venv/bin/python docs/ox63_research/test_ox63_msb.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "ox62_research"))

from ox63_lib import add_msb_anchor, sig_F6R, generate_candidates_scaled  # noqa: E402
from ox62_lib import load_frame, add_harness_cols, generate_candidates  # noqa: E402
from ox62_families import sig_F6  # noqa: E402

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")


def test_msb_trigger():
    df = pd.DataFrame({"close_4h_asof": [100.0] * 20 + [101.0] + [101.0] * 5})
    add_msb_anchor(df)
    up = df["msb_up"].tolist()
    ok1 = up == [False] * 20 + [True] + [False] * 5
    check("S1 msb-break-exact-bar", ok1, f"{[i for i, v in enumerate(up) if v]}")
    df2 = pd.DataFrame({"close_4h_asof": [100.0] * 25})
    add_msb_anchor(df2)
    check("S1b equal-high-no-break", not df2["msb_up"].any())


def test_msb_bear_mirror():
    df = pd.DataFrame({"close_4h_asof": [100.0] * 20 + [99.0] + [99.0] * 5})
    add_msb_anchor(df)
    dn = df["msb_dn"].tolist()
    check("S2 msb-bear-mirror", dn == [False] * 20 + [True] + [False] * 5)


def test_causality():
    df = add_harness_cols(load_frame("EURUSD"))
    full = add_msb_anchor(df.copy())
    trunc = add_msb_anchor(df.iloc[:-100].copy())
    same = (full["msb_up"].iloc[:-100].values == trunc["msb_up"].values).all() and \
           (full["msb_dn"].iloc[:-100].values == trunc["msb_dn"].values).all()
    check("S3 anchor-causal-truncate", same)


def test_f6r_expansion():
    df = add_msb_anchor(add_harness_cols(load_frame("EURUSD")))
    f6l, f6s = sig_F6(df, {"d": 1.0})
    f6rl, f6rs = sig_F6R(df)
    f6l, f6s = np.asarray(f6l, bool), np.asarray(f6s, bool)
    f6rl, f6rs = np.asarray(f6rl, bool), np.asarray(f6rs, bool)
    ok = bool((~f6l | f6rl).all() and (~f6s | f6rs).all())
    check("S4 f6-implies-f6r", ok,
          f"F6={f6l.sum()}/{f6s.sum()} F6R={f6rl.sum()}/{f6rs.sum()}")


def synth_frame(n=30, start="2026-01-05 09:00"):
    dts = pd.date_range(start, periods=n, freq="15min", tz="UTC")
    return pd.DataFrame({"datetime": dts, "open": 100.0, "high": 100.05, "low": 99.95,
                         "close": 100.0, "local_low_20": 99.0, "local_high_20": 102.5,
                         "atr_14": 0.01, "is_kill_zone": False})


def masks(n, i):
    lm = np.zeros(n, bool)
    lm[i] = True
    return lm, np.zeros(n, bool)


def test_veto_boundary():
    base = synth_frame()
    base.loc[10, "is_kill_zone"] = True
    span = base["datetime"].iloc[0] - pd.Timedelta(days=1)
    a = base.copy()
    a.loc[10, "local_high_20"] = 101.19
    r119 = generate_candidates_scaled(a, *masks(30, 10), span)
    check("S5a veto-1.19-excluded", len(r119) == 0, f"rows={len(r119)}")
    b = base.copy()
    b.loc[10, "local_high_20"] = 101.20
    b.loc[12, "high"] = 101.30
    b.loc[12, "low"] = 100.50
    b.loc[12, "close"] = 101.25
    r120 = generate_candidates_scaled(b, *masks(30, 10), span)
    ok = (len(r120) == 1 and abs(r120["r_realized"].iloc[0] - 1.07) < 1e-9
          and r120["hold_bars"].iloc[0] == 1 and r120["exit_reason"].iloc[0] == 1
          and bool(r120["scaled"].iloc[0]) is True)
    check("S5b veto-1.20-admitted-tp1-tp2", ok,
          f"{r120[['r_realized', 'hold_bars', 'scaled']].to_dict('records') if len(r120) else []}")


def test_friday_and_dataend():
    fri = synth_frame(start="2026-01-09 15:15")  # bar 11 lands Fri 18:00 UTC
    fri.loc[10, "is_kill_zone"] = True
    span = fri["datetime"].iloc[0] - pd.Timedelta(days=1)
    r = generate_candidates_scaled(fri, *masks(30, 10), span)
    check("S6 friday-entry-veto", len(r) == 0, f"entry_bar={fri['datetime'].iloc[11]}")
    end = synth_frame()
    end.loc[29, "is_kill_zone"] = True
    span = end["datetime"].iloc[0] - pd.Timedelta(days=1)
    r2 = generate_candidates_scaled(end, *masks(30, 29), span)
    check("S7 data-end-truncation", len(r2) == 0)


def test_unscaled_parity():
    base = synth_frame()
    base.loc[10, "is_kill_zone"] = True
    base.loc[12, "low"] = 98.9  # straight to full SL, never near TP1
    span = base["datetime"].iloc[0] - pd.Timedelta(days=1)
    m = masks(30, 10)
    a = generate_candidates(base, *m, span)
    b = generate_candidates_scaled(base, *m, span)
    ok = (len(a) == 1 and len(b) == 1
          and abs(a["r_realized"].iloc[0] - b["r_realized"].iloc[0]) < 1e-12
          and abs(b["r_realized"].iloc[0] + 1.08) < 1e-9
          and bool(b["scaled"].iloc[0]) is False)
    check("S8a pre-tp1-stop-parity", ok, f"mono={a['r_realized'].tolist()} scaled={b['r_realized'].tolist()}")
    flat = synth_frame(n=40)
    flat.loc[10, "is_kill_zone"] = True
    span = flat["datetime"].iloc[0] - pd.Timedelta(days=1)
    m2 = masks(40, 10)
    a2 = generate_candidates(flat, *m2, span)
    b2 = generate_candidates_scaled(flat, *m2, span)
    ok2 = (len(a2) == 1 and len(b2) == 1
           and abs(a2["r_realized"].iloc[0] - b2["r_realized"].iloc[0]) < 1e-12
           and abs(b2["r_realized"].iloc[0] + 0.08) < 1e-9
           and b2["hold_bars"].iloc[0] == 24 and bool(b2["scaled"].iloc[0]) is False)
    check("S8b decay-parity", ok2, f"mono={a2['r_realized'].tolist()} scaled={b2['r_realized'].tolist()}")


if __name__ == "__main__":
    print("OX63 MSB/F6R/candidate unit tests:")
    test_msb_trigger()
    test_msb_bear_mirror()
    test_causality()
    test_f6r_expansion()
    test_veto_boundary()
    test_friday_and_dataend()
    test_unscaled_parity()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
