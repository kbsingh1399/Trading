"""OX59-E1: Unit verification of the upgraded portfolio engine + S1 labeler.

U1-U7: simulate_elite_portfolio — chop S1 halving, bull full size, DD-defense
       tier, DD contraction x0.5 @ 1.80%, 1-position-per-asset, HB-alt-long cap
       in/out of BTC breakdown.
L1-L4: label_triple_barriers_numba — BE lock 0.80->+0.20, 24-bar decay exit,
       3R target preserved, phase-2 trail lock 2.00->+1.50.

Usage:  python ox59_unit_tests.py [REPO_ROOT]   (exits non-zero on any failure)
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from Engine.runners.run_23_oos_altcoin_suite import simulate_elite_portfolio
from Engine.core.fast_numba_oos_engine import label_triple_barriers_numba

fails = []


def check(name, got, exp):
    ok = abs(got - exp) < 1e-9
    print(f"{name}: got {got} expect {exp} -> {'OK' if ok else 'FAIL'}")
    if not ok:
        fails.append(name)


def run_portfolio(regime_id, r, risks, holds, sleeves, syms, btcbd=None):
    n = len(r)
    kw = dict(event_times=np.arange(1, n + 1) * 1000, event_r_gains=np.array(r, float),
              event_risks=np.array(risks, float), event_hold_ms=np.array(holds),
              event_sleeve_ids=np.array(sleeves, np.int8), event_syms=np.array(syms),
              event_sides=np.ones(n, np.int8), event_hb=np.ones(n, np.int8),
              event_btcbd=np.array(btcbd if btcbd else [0] * n, np.int8),
              regime_id=regime_id, capital=5000.0, max_concurrent=3,
              max_s1_concurrent=2, max_t1_concurrent=2, max_orb_concurrent=2,
              milestone_pnl=500.0, dd_stop_pct=4.85)
    return simulate_elite_portfolio(**kw)


o = dict(r=[1.0], risks=[36.0], holds=[100], sleeves=[1], syms=[1])
check("U1 chop S1 halved", run_portfolio(0, **o)[0], 18.0)
check("U2 bull S1 full", run_portfolio(1, **o)[0], 36.0)
r = run_portfolio(1, r=[-1.0] * 4 + [1.0], risks=[36.0] * 5, holds=[100] * 5,
                  sleeves=[2] * 5, syms=[1, 2, 3, 4, 5])
check("U7 contraction (-36-36-14-14+7)", r[0], -93.0)
check("U7 maxDD", round(r[1], 6), 2.0)
r = run_portfolio(1, r=[1.0, 1.0], risks=[36.0] * 2, holds=[10000] * 2,
                  sleeves=[1, 2], syms=[5, 5])
check("U4 1-per-asset count", r[2], 1)
r = run_portfolio(1, r=[1.0, 1.0], risks=[36.0] * 2, holds=[10000] * 2,
                  sleeves=[1, 2], syms=[5, 6], btcbd=[1, 1])
check("U5 breakdown hb cap", r[2], 1)
r = run_portfolio(1, r=[1.0, 1.0], risks=[36.0] * 2, holds=[10000] * 2,
                  sleeves=[1, 2], syms=[5, 6], btcbd=[0, 0])
check("U6 no-breakdown both fill", r[2], 2)

RAT = dict(be_trigger_r=0.80, be_lock_r=0.20, profit_trigger_r=1.50,
           profit_lock_r=0.80, friction_r=0.18,
           trail_trigger_r=2.0, trail_lock_r=1.5)


def run_label(c, h, lo):
    n = len(c)
    atr = np.full(n, 1.0)
    lc = np.zeros(n, bool); lc[10] = True
    return label_triple_barriers_numba(c, h, lo, atr, lc, np.zeros(n, bool),
                                       32, 3.0, 1.2, **RAT)


n = 60
c = np.full(n, 100.0); h = c.copy(); lo = c.copy()
c[11] = h[11] = 100.9; lo[12] = 99.5
_, _, _, rr, bh = run_label(c, h, lo)
check("L1 BE-lock r", round(float(rr[10]), 4), 0.02)
check("L1 bars", int(bh[10]), 2)
c = np.full(n, 100.0); h = c.copy(); lo = c.copy()
c[10:] = h[10:] = 100.1; lo[10:] = 100.0
_, _, _, rr, bh = run_label(c, h, lo)
check("L2 decay r", round(float(rr[10]), 4), -0.18)
check("L2 bars", int(bh[10]), 24)
c = np.full(n, 100.0); h = c.copy(); lo = c.copy()
h[15] = 103.2; c[15:] = 103.2; lo[15:] = 102.0
_, _, _, rr, bh = run_label(c, h, lo)
check("L3 target r", round(float(rr[10]), 4), 2.82)
check("L3 bars", int(bh[10]), 5)
c = np.full(n, 100.0); h = c.copy(); lo = c.copy()
h[11] = c[11] = 102.1; lo[11] = 100.5; c[12] = h[12] = 101.0; lo[12] = 100.0
_, _, _, rr, bh = run_label(c, h, lo)
check("L4 trail r", round(float(rr[10]), 4), 1.32)
check("L4 bars", int(bh[10]), 2)

print("FAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)
