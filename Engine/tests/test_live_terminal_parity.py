"""OX66 Mandate 4: directional research<->live parity verification.

Covers: unified ATR floor, strict next-bar-open fills, stop-first
resolution, fill causality (truncation invariance), sleeve taxonomy,
governor caps, signal dedup/cooldown.
Run: /home/user/ox61venv/bin/python -m unittest Engine.tests.test_live_terminal_parity -v
"""
import inspect
import sys
import time
import unittest
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

import Engine.core.canonical_indicators as canon  # noqa: E402
import Engine.core.fast_numba_oos_engine as numba_eng  # noqa: E402
import Engine.strategy.s4_pivot_footprint_exhaustion as s4  # noqa: E402
import Engine.runners.run_live_terminal as term  # noqa: E402


def synth_ohlc(n=12, open_next=100.0, high_next=102.5, low_next=99.9,
               close_next=101.0, sig_idx=5, atr_val=1.0):
    c = np.full(n, 100.0)
    h = np.full(n, 100.5)
    lo = np.full(n, 99.5)
    o = np.full(n, 100.0)
    o[sig_idx + 1] = open_next
    h[sig_idx + 1] = high_next
    lo[sig_idx + 1] = low_next
    c[sig_idx + 1] = close_next  # differs from open: discriminates fill basis
    atr = np.full(n, atr_val)
    lc = np.zeros(n, bool)
    sc = np.zeros(n, bool)
    lc[sig_idx] = True
    return c, h, lo, o, atr, lc, sc


class TestAtrFloorParity(unittest.TestCase):
    def test_floor_math(self):
        out = canon.apply_atr_floor(np.array([0.1, 5.0]), np.array([100.0, 100.0]))
        self.assertAlmostEqual(out[0], 1.2)  # 1.2% of 100 binds
        self.assertAlmostEqual(out[1], 5.0)  # raw ATR above floor kept

    def test_single_source_of_truth(self):
        # all three engines must reference the SAME helper (parity tripwire)
        for mod in (numba_eng, s4, term):
            self.assertIn("apply_atr_floor", inspect.getsource(mod),
                          f"{mod.__name__} does not use apply_atr_floor")
        self.assertIs(numba_eng.apply_atr_floor, canon.apply_atr_floor)
        self.assertIs(s4.apply_atr_floor, canon.apply_atr_floor)


class TestNextOpenFills(unittest.TestCase):
    def test_numba_engine_next_open(self):
        c, h, lo, o, atr, lc, sc = synth_ohlc()
        is_c, side, lab, rr, bh = numba_eng.label_triple_barriers_numba.py_func(
            c, h, lo, o, atr, lc, sc, 4, 2.0, 0.75,
            be_trigger_r=99.0, be_lock_r=0.0, profit_trigger_r=99.0,
            profit_lock_r=0.0, friction_r=0.25,
            trail_trigger_r=99.0, trail_lock_r=0.0)
        self.assertTrue(is_c[5])
        self.assertEqual(side[5], 1)
        # entry=o[6]=100, fav=(102.5-100)/1=2.5 >= target 2.0 -> 2.0-0.25
        self.assertAlmostEqual(rr[5], 1.75, places=9)
        self.assertEqual(bh[5], 1)

    def test_s4_next_open(self):
        c, h, lo, o, atr, lc, sc = synth_ohlc(high_next=103.0)
        is_c, side, rr, bh = s4.label_exhaustion_trades_numba.py_func(
            c, h, lo, o, atr, lc, sc, 4, 2.8, 1.0,
            be_trigger_r=99.0, be_lock_r=0.0, profit_trigger_r=99.0,
            profit_lock_r=0.0, trail_trigger_r=99.0, trail_lock_r=0.0,
            friction_r=0.18)
        self.assertTrue(is_c[5])
        # entry=o[6]=100, fav=3.0 >= 2.8 -> 2.8-0.18 (next-CLOSE would differ)
        self.assertAlmostEqual(rr[5], 2.62, places=9)
        self.assertEqual(bh[5], 1)

    def test_stop_first_same_bar(self):
        c, h, lo, o, atr, lc, sc = synth_ohlc(high_next=105.0, low_next=98.0)
        _, _, _, rr, _ = numba_eng.label_triple_barriers_numba.py_func(
            c, h, lo, o, atr, lc, sc, 4, 2.0, 0.75,
            friction_r=0.25)
        self.assertAlmostEqual(rr[0 + 5], -0.75 - 0.25, places=9)

    def _run(self, arrs):
        c, h, lo, o, atr, lc, sc = arrs
        return numba_eng.label_triple_barriers_numba.py_func(
            c, h, lo, o, atr, lc, sc, 4, 2.0, 0.75, friction_r=0.25)

    def test_truncation_invariance(self):
        full = synth_ohlc(n=20)
        trunc = tuple(a[:12] for a in full)
        _, _, _, rr_f, _ = self._run(full)
        _, _, _, rr_t, _ = self._run(trunc)
        self.assertAlmostEqual(rr_f[5], rr_t[5], places=12)

    def test_future_perturbation_invariance(self):
        base = synth_ohlc(n=20)
        pert = [a.copy() for a in base]
        pert[1][15] *= 2.0  # corrupt a far-future bar
        pert[3][15] *= 0.5
        _, _, _, rr_b, _ = self._run(base)
        _, _, _, rr_p, _ = self._run(pert)
        self.assertAlmostEqual(rr_b[5], rr_p[5], places=12)


class TestTaxonomyAndGovernor(unittest.TestCase):
    def test_unified_ids(self):
        self.assertEqual(term.SLEEVE_S1_PULLBACK, 1)
        self.assertEqual(term.SLEEVE_S2_BOLLINGER, 2)
        self.assertEqual(term.SLEEVE_S3_ORB, 3)
        self.assertEqual(term.SLEEVE_S4_PIVOT_SWEEP, 4)
        self.assertEqual(term.SLEEVE_T1_DONCHIAN, 5)

    def _pos(self, sleeve_id, symbol="BTCUSDT"):
        return {"sleeve_id": sleeve_id, "symbol": symbol, "direction": 1}

    def test_t1_cap_on_id5(self):
        g = term.InstitutionalRiskGovernor()
        act = [self._pos(5, "BTCUSDT"), self._pos(5, "ETHUSDT")]
        self.assertFalse(g.can_open_position(5, act))
        self.assertTrue(g.can_open_position(2, []))  # S2 unconstrained by T1 cap

    def test_s1_and_orb_caps(self):
        g = term.InstitutionalRiskGovernor()
        self.assertFalse(g.can_open_position(
            1, [self._pos(1, "A"), self._pos(1, "B")]))
        self.assertFalse(g.can_open_position(
            3, [self._pos(3, "A"), self._pos(3, "B")]))

    def test_portfolio_cap(self):
        g = term.InstitutionalRiskGovernor()
        act = [self._pos(1, "A"), self._pos(4, "B"), self._pos(5, "C")]
        self.assertFalse(g.can_open_position(2, act))


class TestDedup(unittest.TestCase):
    def test_exact_duplicate_blocked(self):
        d = term.SignalDedup(cooldown_sec=3600)
        s = {"symbol": "BTCUSDT", "sleeve_id": 1, "direction": 1, "bar_ms": 999}
        self.assertFalse(d.is_duplicate(s))
        d.mark(s)
        self.assertTrue(d.is_duplicate(dict(s)))

    def test_cooldown_blocks_new_bar(self):
        d = term.SignalDedup(cooldown_sec=3600)
        d.mark({"symbol": "ETHUSDT", "sleeve_id": 4, "direction": -1, "bar_ms": 100})
        self.assertTrue(d.is_duplicate(
            {"symbol": "ETHUSDT", "sleeve_id": 4, "direction": -1, "bar_ms": 200}))

    def test_cooldown_expiry_allows(self):
        d = term.SignalDedup(cooldown_sec=0.01)
        s = {"symbol": "XRPUSDT", "sleeve_id": 2, "direction": 1, "bar_ms": 100}
        d.mark(s)
        time.sleep(0.02)
        s2 = dict(s, bar_ms=200)
        self.assertFalse(d.is_duplicate(s2))

    def test_other_sleeve_allowed(self):
        d = term.SignalDedup(cooldown_sec=3600)
        d.mark({"symbol": "BTCUSDT", "sleeve_id": 1, "direction": 1, "bar_ms": 100})
        self.assertFalse(d.is_duplicate(
            {"symbol": "BTCUSDT", "sleeve_id": 4, "direction": 1, "bar_ms": 100}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
