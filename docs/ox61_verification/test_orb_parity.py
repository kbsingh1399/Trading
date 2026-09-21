"""OX61 unit tests: ORB correctness fixes on the pre-committed spec (OX61-B final).
Proves via synthetic arrays: sentinel/exited-flag fix, TP, gap slippage (unclamped),
Friday closeout + Friday entry veto, true hold bars. Plus real-data plumbing.
Usage: python docs/ox61_verification/test_orb_parity.py
"""
import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Engine.strategy.orb_crt_forex_engine import (
    simulate_session_orb, EXIT_SL, EXIT_TP, EXIT_FRIDAY, EXIT_TRUNC,
)

PASS = []
FAIL = []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

def mkday(n=60, start_h=7, start_m=0, dow=2, px=100.0):
    """Single synthetic day, flat px, 15-min bars from start_h:start_m."""
    o = np.full(n, px); h = np.full(n, px + 0.1); l = np.full(n, px - 0.1); c = np.full(n, px)
    v = np.ones(n)
    ts = np.arange(n, dtype=np.int64)
    dates = np.full(n, 20250101, dtype=np.int64)
    mins = (np.arange(n) * 15 + start_m) % 60
    hrs = (start_h + (np.arange(n) * 15 + start_m) // 60) % 24
    dows = np.full(n, dow, dtype=np.int64)
    return o, h, l, c, v, ts, dates, hrs.astype(np.int64), mins.astype(np.int64), dows

def mkor_long(o, h, l, c, or_lo=99.5, or_hi=100.5, brk=2, body_lo=100.0, body_hi=100.55):
    """OR on bars 0-1, long breakout on bar brk (body>=0.40, close>ema200)."""
    l[0] = or_lo; h[1] = or_hi
    o[brk] = body_lo; c[brk] = body_hi; h[brk] = body_hi + 0.05; l[brk] = body_lo - 0.05

def run(o, h, l, c, v, ts, dates, hrs, mns, dows, sh=7, sm=0):
    return simulate_session_orb(o, h, l, c, v, ts, dates, hrs, mns, dows,
                                start_hour=sh, start_minute=sm,
                                range_duration_bars=2, trade_duration_bars=24)

def test_sentinel_fix():
    # True -1.0R stop then late rally: recorded outcome must be -1.08, NOT rally MTM.
    o, h, l, c, v, ts, dates, hrs, mns, dows = mkday()
    mkor_long(o, h, l, c)
    o[3] = 100.55          # entry at open of bar 3
    l[3] = 99.4            # SL hit (sl=99.5) -> exactly -1.0R pre-friction
    c[25] = 105.0          # late rally (would corrupt via fallback under sentinel bug)
    sig, r, ep, sl, t, hold, rs = run(o, h, l, c, v, ts, dates, hrs, mns, dows)
    ok = (len(r) == 1 and abs(r[0] - (-1.08)) < 1e-9 and rs[0] == EXIT_SL and hold[0] == 0)
    check("U1 sentinel-fix-stop-exact", ok, f"r={r} rs={rs} hold={hold}")

def test_tp():
    o, h, l, c, v, ts, dates, hrs, mns, dows = mkday()
    mkor_long(o, h, l, c)
    o[3] = 100.55          # entry; r = 100.55-99.5 = 1.05; TP = 103.175
    h[5] = 103.2; l[5] = 102.0; c[5] = 102.5
    sig, r, ep, sl, t, hold, rs = run(o, h, l, c, v, ts, dates, hrs, mns, dows)
    ok = (len(r) == 1 and abs(r[0] - 2.42) < 1e-9 and rs[0] == EXIT_TP and hold[0] == 2)
    check("U2 TP-2.5R-minus-friction", ok, f"r={r} rs={rs} hold={hold}")

def test_gap_slippage():
    # Bar opens 1.5R beyond SL -> fills at open, unclamped (below old -1.15 floor).
    o, h, l, c, v, ts, dates, hrs, mns, dows = mkday()
    mkor_long(o, h, l, c)
    o[3] = 100.55          # entry; r=1.05
    o[4] = 97.9; h[4] = 98.0; l[4] = 97.8; c[4] = 97.9  # gap through SL 99.5
    sig, r, ep, sl, t, hold, rs = run(o, h, l, c, v, ts, dates, hrs, mns, dows)
    expect = (97.9 - 100.55) / 1.05 - 0.08
    ok = (len(r) == 1 and abs(r[0] - expect) < 1e-9 and r[0] < -1.15 and rs[0] == EXIT_SL)
    check("U3 gap-slippage-unclamped", ok, f"r={r} expect={expect:.4f} rs={rs}")

def test_friday_closeout():
    o, h, l, c, v, ts, dates, hrs, mns, dows = mkday()
    mkor_long(o, h, l, c)
    o[3] = 100.55
    dows[10] = 4; hrs[10] = 20; mns[10] = 30  # Friday 20:30 bar inside hold
    c[10] = 101.2; h[10] = 101.3; l[10] = 100.9
    sig, r, ep, sl, t, hold, rs = run(o, h, l, c, v, ts, dates, hrs, mns, dows)
    expect = (101.2 - 100.55) / 1.05 - 0.08
    ok = (len(r) == 1 and abs(r[0] - expect) < 1e-9 and rs[0] == EXIT_FRIDAY and hold[0] == 7)
    check("U4 friday-closeout", ok, f"r={r} expect={expect:.4f} rs={rs} hold={hold}")

def test_friday_entry_veto():
    # NY OR on Friday; breakouts only late -> entries >= 18:00 vetoed -> zero trades.
    o, h, l, c, v, ts, dates, hrs, mns, dows = mkday(n=60, start_h=13, start_m=30, dow=4)
    h[1] = 100.5; l[0] = 99.5   # OR 99.5..100.5 on bars 0-1 (13:30, 13:45)
    # suppress early breakouts: keep highs <= 100.5 until bar 17 (18:00 Fri entry => veto)
    for j in range(2, 17):
        h[j] = 100.4
    o[17] = 100.0; c[17] = 100.6; h[17] = 100.65; l[17] = 99.95  # breakout, entry bar 18 = 18:00 Fri
    o[19] = 100.0; c[19] = 100.7; h[19] = 100.75; l[19] = 99.95  # breakout, entry bar 20 = 18:30 Fri
    sig, r, *_ = run(o, h, l, c, v, ts, dates, hrs, mns, dows, sh=13, sm=30)
    check("U5a friday-entry-veto", len(r) == 0, f"n={len(r)}")
    # Control: identical setup on Wednesday -> trades fire.
    dows2 = np.full(60, 2, dtype=np.int64)
    sig2, r2, *_ = run(o, h, l, c, v, ts, dates, hrs, mns, dows2, sh=13, sm=30)
    check("U5b wednesday-control-fires", len(r2) >= 1, f"n={len(r2)}")

def test_integration():
    from Engine.strategy.orb_crt_forex_engine import ORBCRTForexCFDStrategy
    from Engine.core.base_strategy import EngineConfig
    s = ORBCRTForexCFDStrategy(config=EngineConfig.load())
    res = s.run_backtest(start_date="2025-12-01", end_date="2025-12-31", symbols=["EURUSD", "GAS"], save_plot=False)
    tdf = res.trades_df
    ok = (tdf is not None and len(tdf) > 0 and "hold_bars" in tdf.columns
          and "exit_reason" in tdf.columns and set(tdf["exit_reason"].unique()) <= {0, 1, 2, 3, 5}
          and (tdf["hold_bars"] >= 0).all() and (tdf["hold_bars"] <= 23).all())
    check("U6 plumbing", ok, f"n={0 if tdf is None else len(tdf)}")

if __name__ == "__main__":
    print("OX61-B ORB correctness unit tests (pre-committed spec + fixes):")
    test_sentinel_fix(); test_tp(); test_gap_slippage(); test_friday_closeout()
    test_friday_entry_veto(); test_integration()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
