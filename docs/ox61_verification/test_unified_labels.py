"""OX61 unit tests: unified live-spec kernel labeler (create_labels_unified).
Usage: python docs/ox61_verification/test_unified_labels.py
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Engine.core.strategy_kernel import create_labels_unified, create_labels_ratchet

PASS = []
FAIL = []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

def mkframe(n=60, start="2025-01-01 07:00", px=100.0):
    """Flat frame, Wed 2025-01-01 07:00 UTC by default, no setups."""
    dts = pd.date_range(start=start, periods=n, freq="15min", tz="UTC")
    df = pd.DataFrame({
        "datetime": dts,
        "open": np.full(n, px), "high": np.full(n, px + 0.05),
        "low": np.full(n, px - 0.05), "close": np.full(n, px),
        "sweep_pdl": np.zeros(n, dtype=np.int64), "sweep_pdh": np.zeros(n, dtype=np.int64),
        "bullish_fvg": np.zeros(n), "bearish_fvg": np.zeros(n),
        "htf_4h_trend": np.zeros(n),
        "local_low_20": np.full(n, px - 1.0), "local_high_20": np.full(n, px + 1.0),
        "atr_14": np.full(n, 0.5),
        "is_kill_zone": np.zeros(n, dtype=bool),
    })
    return df

def set_long(df, i, fvg=1.0, trend=1.0):
    df.loc[i, "is_kill_zone"] = True
    df.loc[i, "sweep_pdl"] = 1
    df.loc[i, "bullish_fvg"] = fvg
    df.loc[i, "htf_4h_trend"] = trend

def set_short(df, i, fvg=1.0, trend=-1.0):
    df.loc[i, "is_kill_zone"] = True
    df.loc[i, "sweep_pdh"] = 1
    df.loc[i, "bearish_fvg"] = fvg
    df.loc[i, "htf_4h_trend"] = trend

def test_reff_veto():
    df = mkframe()
    set_long(df, 5)
    df.loc[5, "local_low_20"] = 99.0    # r = 1.0 (floor 0.75)
    df.loc[6, "open"] = 100.0
    df.loc[5, "local_high_20"] = 101.5  # R_eff = 1.5 < 2.5 -> veto
    out = create_labels_unified(df)
    check("V1 reff-veto-NaN", bool(np.isnan(out.loc[5, "target"])), f"t={out.loc[5,'target']}")

def test_runner_tp35():
    df = mkframe()
    set_long(df, 5)
    df.loc[5, "local_low_20"] = 99.0
    df.loc[5, "local_high_20"] = 104.0   # R_eff=4 -> cap 3.5R -> TP=103.5
    df.loc[6, "open"] = 100.0
    df.loc[6, ["high", "close"]] = [100.9, 100.85]   # lock +0.15
    df.loc[7, ["open", "high", "low", "close"]] = [100.85, 101.6, 100.5, 101.5]  # lock +0.80
    df.loc[8, ["open", "high", "low", "close"]] = [101.5, 102.6, 101.4, 102.4]   # lock +2.30
    df.loc[9, ["open", "high", "low"]] = [102.4, 103.6, 102.8]                   # TP 3.5R
    out = create_labels_unified(df)
    r = out.loc[5, "r_realized"]
    check("V2 runner-TP-3.5R", abs(r - 3.42) < 1e-9 and out.loc[5, "target"] == 1
          and out.loc[5, "exit_reason"] == 1 and out.loc[5, "hold_bars"] == 3, f"r={r}")

def test_friday_closeout():
    df = mkframe(n=260)
    assert str(df.loc[246, "datetime"]) == "2025-01-03 20:30:00+00:00", df.loc[246, "datetime"]
    set_long(df, 5)
    df.loc[5, "local_low_20"] = 99.0
    df.loc[5, "local_high_20"] = 104.0
    df.loc[6, "open"] = 100.0
    df.loc[7, "high"] = 100.3  # +0.3R excursion defeats decay
    df.loc[246, ["high", "low", "close"]] = [101.3, 100.9, 101.2]
    out = create_labels_unified(df)
    r = out.loc[5, "r_realized"]
    expect = (101.2 - 100.0) / 1.0 - 0.08
    check("V3 friday-closeout", abs(r - expect) < 1e-9 and out.loc[5, "exit_reason"] == 3
          and out.loc[5, "hold_bars"] == 240, f"r={r} expect={expect}")

def test_friday_entry_veto():
    df = mkframe(n=60, start="2025-01-03 07:00")  # Friday
    assert str(df.loc[48, "datetime"]) == "2025-01-03 19:00:00+00:00"
    set_long(df, 48)
    df.loc[48, "local_low_20"] = 99.0
    df.loc[49, "open"] = 100.0
    out = create_labels_unified(df)
    check("V4 friday-entry-veto", bool(np.isnan(out.loc[48, "target"])), f"t={out.loc[48,'target']}")

def test_decay():
    df = mkframe()
    set_long(df, 5)
    df.loc[5, "local_low_20"] = 99.0
    df.loc[5, "local_high_20"] = 104.0
    df.loc[6, "open"] = 100.0
    df.loc[30, "close"] = 100.05  # bar e+24: decay fires (highest 0.05 < 0.2)
    out = create_labels_unified(df)
    check("V5a decay-at-24", out.loc[5, "exit_reason"] == 2 and out.loc[5, "hold_bars"] == 24,
          f"rs={out.loc[5,'exit_reason']} h={out.loc[5,'hold_bars']}")
    # excursion then late TP: survives past bar 24
    df2 = mkframe(n=80)
    set_long(df2, 5)
    df2.loc[5, "local_low_20"] = 99.0
    df2.loc[5, "local_high_20"] = 104.0
    df2.loc[6, "open"] = 100.0
    df2.loc[7, "high"] = 100.5   # +0.5R excursion
    df2.loc[7, "close"] = 100.4
    df2.loc[40, ["open", "high", "low"]] = [100.4, 103.6, 100.3]  # TP at bar 40
    out2 = create_labels_unified(df2)
    check("V5b excursion-survives-TP40", out2.loc[5, "exit_reason"] == 1 and out2.loc[5, "hold_bars"] == 34,
          f"rs={out2.loc[5,'exit_reason']} h={out2.loc[5,'hold_bars']}")

def test_same_bar_reversal():
    df = mkframe()
    set_long(df, 5)
    df.loc[5, "local_low_20"] = 99.0
    df.loc[5, "local_high_20"] = 104.0
    df.loc[6, "open"] = 100.0
    df.loc[6, ["high", "low", "close"]] = [101.6, 99.6, 100.0]  # lock +0.80, close below -> +0.80
    out = create_labels_unified(df)
    r = out.loc[5, "r_realized"]
    check("V6 same-bar-reversal", abs(r - 0.72) < 1e-9 and out.loc[5, "hold_bars"] == 0, f"r={r}")

def test_data_end_nan():
    df = mkframe(n=30)
    set_long(df, 26)
    df.loc[26, "local_low_20"] = 99.0
    df.loc[27, "open"] = 100.0
    out = create_labels_unified(df)
    check("V7 data-end-NaN", bool(np.isnan(out.loc[26, "target"])), f"t={out.loc[26,'target']}")

def test_gap():
    df = mkframe()
    set_long(df, 5)
    df.loc[5, "local_low_20"] = 99.0
    df.loc[5, "local_high_20"] = 104.0
    df.loc[6, "open"] = 100.0
    df.loc[7, ["open", "high", "low", "close"]] = [98.5, 98.7, 98.4, 98.6]
    out = create_labels_unified(df)
    r = out.loc[5, "r_realized"]
    check("V8 gap-unclamped", abs(r - (-1.58)) < 1e-9 and r < -1.15, f"r={r}")

def test_short_mirror():
    df = mkframe()
    set_short(df, 5)
    df.loc[5, "local_high_20"] = 101.0
    df.loc[5, "local_low_20"] = 96.0     # R_eff=4 -> cap 3.5R -> TP=96.5
    df.loc[6, "open"] = 100.0
    df.loc[7, ["open", "high", "low"]] = [100.0, 100.2, 96.4]
    out = create_labels_unified(df)
    r = out.loc[5, "r_realized"]
    check("V9 short-TP", abs(r - 3.42) < 1e-9 and out.loc[5, "target"] == 1, f"r={r}")

def test_precommitted_regression():
    df = mkframe(n=160)  # precommitted range(n-96) needs n > 96
    set_long(df, 5)
    df.loc[5, "local_low_20"] = 99.0
    df.loc[6, "open"] = 100.0
    out = create_labels_ratchet(df)
    ok = ("target" in out.columns and "r_realized" in out.columns
          and "hold_bars" not in out.columns and not bool(np.isnan(out.loc[5, "target"])))
    check("V10 precommitted-untouched", ok, f"t={out.loc[5,'target']}")

if __name__ == "__main__":
    print("OX61 unified-labeler unit tests:")
    test_reff_veto(); test_runner_tp35(); test_friday_closeout(); test_friday_entry_veto()
    test_decay(); test_same_bar_reversal(); test_data_end_nan(); test_gap()
    test_short_mirror(); test_precommitted_regression()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
