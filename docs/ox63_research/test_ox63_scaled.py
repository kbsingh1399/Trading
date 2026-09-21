"""OX63 unit tests: 2-stage scaling exit engine + 4H as-of column.
Usage: /home/user/ox61venv/bin/python docs/ox63_research/test_ox63_scaled.py
"""
import inspect
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Engine.core.strategy_kernel import (
    _ux_exit_scaled_long, _ux_exit_scaled_short, _ux_exit_long,
    UX_TP1_R, UX_TP1_FRAC, UX_MIN_R_EFF_SCALED,
)

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

def mk(n=10):
    return {"opens": np.full(n, 100.0), "highs": np.full(n, 100.05), "lows": np.full(n, 99.95),
            "closes": np.full(n, 100.0), "dows": np.zeros(n, dtype=int),
            "hrs": np.zeros(n, dtype=int), "mns": np.zeros(n, dtype=int)}

def run_long(a, e, entry, sl0, tp2, r):
    n = len(a["opens"])
    return _ux_exit_scaled_long(a["opens"], a["highs"], a["lows"], a["closes"],
                                a["dows"], a["hrs"], a["mns"], n, e, entry, sl0, tp2, r)

def run_short(a, e, entry, sl0, tp2, r):
    n = len(a["opens"])
    return _ux_exit_scaled_short(a["opens"], a["highs"], a["lows"], a["closes"],
                                 a["dows"], a["hrs"], a["mns"], n, e, entry, sl0, tp2, r)

def test_tp1_runner_tp2():
    a = mk()
    a["highs"][1] = 101.2; a["lows"][1] = 100.2; a["closes"][1] = 101.0  # TP1, runner survives
    a["opens"][2] = 101.0; a["highs"][2] = 102.6; a["lows"][2] = 101.8   # TP2 102.5
    r, j, rs, sc = run_long(a, 1, 100.0, 99.0, 102.5, 1.0)
    check("X1 tp1-bank-runner-tp2", abs(r - 1.80) < 1e-9 and j == 2 and rs == 1 and sc is True, f"r={r}")

def test_same_bar_runner_stop():
    a = mk()
    a["highs"][1] = 101.2; a["lows"][1] = 99.9  # TP1 then collapse through fresh +0.15R lock
    r, j, rs, sc = run_long(a, 1, 100.0, 99.0, 102.5, 1.0)
    check("X2 same-bar-runner-stop", abs(r - 0.625) < 1e-9 and j == 1 and rs == 0 and sc is True, f"r={r}")

def test_pre_tp1_full_stop():
    a = mk()
    a["highs"][1] = 100.5; a["lows"][1] = 98.9
    r, j, rs, sc = run_long(a, 1, 100.0, 99.0, 102.5, 1.0)
    check("X3 pre-tp1-full-stop", abs(r + 1.0) < 1e-9 and rs == 0 and sc is False, f"r={r}")

def test_gap_no_surplus():
    # ladder stage is (2.0 -> 1.8): hr=2.1 ratchets to 101.8 then same-bar reversal exits
    a = mk()
    a["opens"][2] = 102.0; a["highs"][2] = 102.1; a["lows"][2] = 101.5  # gap over TP1
    r_gap, _, _, _ = run_long(a, 1, 100.0, 99.0, 102.5, 1.0)
    b = mk()
    b["opens"][2] = 100.5; b["highs"][2] = 102.1; b["lows"][2] = 100.4  # touch, no gap
    r_tch, _, _, _ = run_long(b, 1, 100.0, 99.0, 102.5, 1.0)
    check("X4 gap-banks-at-tp1-exact", abs(r_gap - 1.45) < 1e-9 and abs(r_tch - r_gap) < 1e-12,
          f"gap={r_gap} touch={r_tch}")

def test_runner_ratchet_reversal():
    a = mk()
    a["highs"][1] = 101.2; a["lows"][1] = 100.2; a["closes"][1] = 101.0
    a["opens"][2] = 101.0; a["highs"][2] = 102.6; a["lows"][2] = 101.8; a["closes"][2] = 102.0
    r, j, rs, sc = run_long(a, 1, 100.0, 99.0, 103.5, 1.0)
    check("X5 runner-ratchet-reversal", abs(r - 1.70) < 1e-9 and rs == 0 and sc is True, f"r={r}")

def test_decay_pre_tp1():
    a = mk(n=40)
    r, j, rs, sc = run_long(a, 1, 100.0, 99.0, 102.5, 1.0)
    check("X6 decay-pre-tp1", abs(r - 0.0) < 1e-9 and j == 25 and rs == 2 and sc is False, f"r={r} j={j}")

def test_friday_runner_close():
    a = mk(n=6)
    a["highs"][0] = 101.2; a["lows"][0] = 100.2; a["closes"][0] = 101.0  # TP1
    a["lows"][1:3] = 100.2; a["highs"][1:3] = 100.4  # flat above runner lock
    a["opens"][1:3] = 101.0; a["closes"][1:3] = 101.0  # opens must clear the +0.15R lock
    a["dows"][:] = 3
    a["dows"][3] = 4; a["hrs"][3] = 20; a["mns"][3] = 30
    a["opens"][3] = 101.0; a["highs"][3] = 101.6; a["lows"][3] = 100.9; a["closes"][3] = 101.5
    r, j, rs, sc = run_long(a, 0, 100.0, 99.0, 103.0, 1.0)
    check("X7 friday-runner-close", abs(r - 1.30) < 1e-9 and j == 3 and rs == 3 and sc is True, f"r={r}")

def test_short_mirror():
    a = mk()
    a["lows"][1] = 98.9; a["highs"][1] = 99.8  # TP1 98.9, survives lock 99.85
    a["opens"][2] = 99.0; a["closes"][2] = 99.0  # open must clear the runner lock 99.85
    a["lows"][2] = 97.4; a["highs"][2] = 99.5
    r, j, rs, sc = run_short(a, 1, 100.0, 101.0, 97.5, 1.0)
    check("X8 short-mirror", abs(r - 1.80) < 1e-9 and j == 2 and rs == 1 and sc is True, f"r={r}")

def test_data_end():
    a = mk(n=3)
    res = run_long(a, 0, 100.0, 99.0, 102.5, 1.0)
    check("X9 data-end-none", res is None)

def test_consts_and_frozen():
    ok = UX_TP1_R == 1.10 and UX_TP1_FRAC == 0.50 and UX_MIN_R_EFF_SCALED == 1.20
    frozen = "scaled" not in inspect.getsource(_ux_exit_long) and "tp1" not in inspect.getsource(_ux_exit_long).lower()
    check("X10 consts+frozen-monolithic", ok and frozen)

def test_4h_asof():
    from Engine.core.strategy_kernel import engineer_features_polars
    df = engineer_features_polars("EURUSD", str(PROJECT_ROOT / "Forex_Backtesting_Data"))
    has = "close_4h_asof" in df.columns and bool(df["close_4h_asof"].notna().all())
    g = pd.to_datetime(df["datetime"], utc=True).dt.floor("4h")
    big = None
    for _, idx in df.groupby(g).groups.items():
        if len(idx) >= 10:
            big = idx
            break
    const = df.loc[big, "close_4h_asof"].nunique() == 1 if big is not None else False
    updates = df["close_4h_asof"].nunique() > 100
    src = (PROJECT_ROOT / "Engine/core/strategy_kernel.py").read_text()
    shifted = 'pl.col("close").shift(1).alias("close_4h_asof")' in src
    check("X11 4h-asof-col", has and const and updates and shifted)

if __name__ == "__main__":
    print("OX63 scaled-engine unit tests:")
    test_tp1_runner_tp2(); test_same_bar_runner_stop(); test_pre_tp1_full_stop(); test_gap_no_surplus()
    test_runner_ratchet_reversal(); test_decay_pre_tp1(); test_friday_runner_close(); test_short_mirror()
    test_data_end(); test_consts_and_frozen(); test_4h_asof()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
