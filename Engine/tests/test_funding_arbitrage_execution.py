"""OX66 Mandate 4: funding-arbitrage execution verification (hermetic, no network).

Covers: delta cancellation, hysteresis gates, atomic state + corrupt recovery,
lot-size rounding, margin buffer math, leg-failure rollback, inversion exit.
Run: /home/user/ox61venv/bin/python -m unittest Engine.tests.test_funding_arbitrage_execution -v
"""
import json
import os
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from Engine.live.carry_policy import (CarryPolicyConfig, rotation_friction_usd,  # noqa: E402
                                      expected_accrual_usd, pair_notional_usd,
                                      should_replace, select_swaps)
from Engine.brokers.binance_broker import BinanceBroker  # noqa: E402
from Engine.live import binance_funding_arbitrage_bot as botmod  # noqa: E402

CFG = CarryPolicyConfig()
NOW = 1_789_000_000_000  # fixed test clock (ms)
H = 3_600_000


class FakeBroker:
    """Minimal recording broker implementing the executor's 3-method interface."""

    def __init__(self, fail_perp=False):
        self.fail_perp = fail_perp
        self.calls = []

    def set_isolated_1x(self, symbol):
        return True

    def place_spot_market(self, symbol, side, quantity, client_id, ref_price=None):
        self.calls.append(("spot", side, round(quantity, 8)))
        return {"symbol": symbol, "side": side, "qty": quantity,
                "fill_price": ref_price or 100.0, "status": "FILLED",
                "orderId": len(self.calls), "simulated": True}

    def place_perp_market(self, symbol, side, quantity, client_id,
                          ref_price=None, reduce_only=False):
        self.calls.append(("perp", side, round(quantity, 8)))
        if self.fail_perp and side == "SELL" and not reduce_only:
            return None
        return {"symbol": symbol, "side": side, "qty": quantity,
                "fill_price": ref_price or 100.0, "status": "FILLED",
                "orderId": len(self.calls), "simulated": True}


class TestDeltaMath(unittest.TestCase):
    def test_pair_notional_and_buffer(self):
        n = pair_notional_usd(5000.0, CFG)
        self.assertAlmostEqual(n, 5000 * 0.8 / 3 * 0.5, places=6)
        # 3 pairs x (spot + margin) == 80% deployed, 20% buffer
        self.assertAlmostEqual(3 * 2 * n, 5000 * 0.8, places=6)

    def test_delta_cancellation_on_open(self):
        ex = botmod.DualLegExecutor(FakeBroker(), CFG)
        book = {"bid": 99.9, "ask": 100.1}
        fill = ex.open_pair("BTCUSDT", 666.66, book, 100.05)
        self.assertIsNotNone(fill)
        self.assertAlmostEqual(fill["spot_qty"], fill["perp_qty"], places=8)
        # delta-0: equal and opposite notionals at their own fills
        spot_n = fill["spot_qty"] * fill["spot_fill"]
        perp_n = fill["perp_qty"] * fill["perp_fill"]
        self.assertAlmostEqual(spot_n, perp_n, delta=spot_n * 0.01)

    def test_perp_sized_to_spot_fill(self):
        ex = botmod.DualLegExecutor(FakeBroker(), CFG)
        fill = ex.open_pair("ETHUSDT", 500.0, {"bid": 10.0, "ask": 10.02}, 10.01)
        max_spot = max(q for v, s, q in ex.broker.calls if v == "spot" and s == "BUY")
        max_perp = max(q for v, s, q in ex.broker.calls if v == "perp" and s == "SELL")
        self.assertAlmostEqual(max_spot, max_perp, places=8)


class TestHysteresis(unittest.TestCase):
    def test_mandated_0001_does_not_rotate(self):
        ok, reason = should_replace(0.010, 0.011, 80.0, 1000.0, CFG)
        self.assertFalse(ok)
        self.assertEqual(reason, "hurdle")

    def test_cooldown_blocks(self):
        ok, reason = should_replace(0.001, 0.200, 71.9, 1000.0, CFG)
        self.assertFalse(ok)
        self.assertEqual(reason, "cooldown")

    def test_hurdle_plus_cost_benefit_passes(self):
        ok, reason = should_replace(0.001, 0.200, 72.0, 1000.0, CFG)
        self.assertTrue(ok)
        self.assertEqual(reason, "rotate")

    def test_cost_benefit_blocks_thin_edge(self):
        # hurdle cleared (0.005) but accrual << 2x friction at dust rates
        ok, reason = should_replace(0.002, 0.007, 72.0, 1000.0, CFG)
        self.assertFalse(ok)
        self.assertEqual(reason, "cost_benefit")

    def test_rotation_friction_single_count(self):
        # one open + one close (mandate's 2x applied by caller, not here)
        n = 1000.0
        expect = 2 * n * (CFG.fee_spot + CFG.half_spread_spot
                          + CFG.fee_perp + CFG.half_spread_perp)
        self.assertAlmostEqual(rotation_friction_usd(n, CFG), expect, places=9)

    def test_expected_accrual_math(self):
        self.assertAlmostEqual(expected_accrual_usd(1000.0, 0.01, 72.0),
                               1000 * 0.0001 * 9, places=9)


class TestSelectSwaps(unittest.TestCase):
    def test_inversion_liquidates_after_two_prints(self):
        ranked = [("BTCUSDT", 0.01), ("ETHUSDT", -0.05)]
        holdings = {"ETHUSDT": {"rate_pct": 0.01, "entry_ms": NOW - 1 * H,
                                "neg_streak": 2}}
        exits, _ = select_swaps(ranked, holdings, NOW, CFG)
        self.assertIn("ETHUSDT", exits)

    def test_single_flicker_held(self):
        ranked = [("BTCUSDT", 0.01), ("ETHUSDT", -0.05)]
        holdings = {"ETHUSDT": {"rate_pct": 0.01, "entry_ms": NOW - 1 * H,
                                "neg_streak": 1}}
        exits, _ = select_swaps(ranked, holdings, NOW, CFG)
        self.assertNotIn("ETHUSDT", exits)

    def test_cooldown_freezes_book(self):
        ranked = [("BTCUSDT", 0.50), ("ETHUSDT", 0.01), ("XRPUSDT", 0.01),
                  ("BNBUSDT", 0.01)]
        # full book, all inside cooldown -> no rotation; empty-slot fill N/A
        holdings = {s: {"rate_pct": 0.01, "entry_ms": NOW - 1 * H}
                    for s in ["ETHUSDT", "XRPUSDT", "BNBUSDT"]}
        exits, entries = select_swaps(ranked, holdings, NOW, CFG)
        self.assertEqual((exits, entries), ([], []))

    def test_bounded_churn_never_full_rebuild(self):
        ranked = [("A", 0.50), ("B", 0.40), ("C", 0.30),
                  ("X", 0.01), ("Y", 0.01), ("Z", 0.01)]
        old = NOW - 100 * H
        holdings = {s: {"rate_pct": 0.01, "entry_ms": old} for s in ["X", "Y", "Z"]}
        exits, entries = select_swaps(ranked, holdings, NOW, CFG)
        self.assertLessEqual(len(exits), CFG.top_k)
        self.assertLessEqual(len(entries), CFG.top_k)
        self.assertEqual(len(exits), len(entries))  # single-leg swaps pair up

    def test_fill_empty_slot(self):
        ranked = [("BTCUSDT", 0.20), ("ETHUSDT", 0.15)]
        exits, entries = select_swaps(ranked, {}, NOW, CFG)
        self.assertEqual(exits, [])
        self.assertEqual(len(entries), 2)


class TestAtomicState(unittest.TestCase):
    def test_atomic_write_no_tmp_left(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "state.json"
            botmod.atomic_write_json(target, {"a": 1})
            self.assertEqual(json.loads(target.read_text()), {"a": 1})
            self.assertEqual(list(Path(td).glob("*.tmp")), [])

    def test_corrupt_state_quarantined(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            fake = Path(td) / "funding_arbitrage_state.json"
            fake.write_text("{corrupt!!!")
            orig = botmod.STATE_FILE
            botmod.STATE_FILE = fake
            try:
                st = botmod.load_state_resilient(5000.0)
                self.assertEqual(st["current_equity_usd"], 5000.0)
                self.assertEqual(st["active_positions"], {})
                self.assertEqual(len(list(Path(td).glob("*.corrupt.*.json"))), 1)
            finally:
                botmod.STATE_FILE = orig


class TestBrokerSim(unittest.TestCase):
    def test_dry_run_places_without_network_or_keys(self):
        os.environ.pop("BINANCE_API_KEY", None)
        b = BinanceBroker(dry_run=True)
        f1 = b.place_spot_market("BTCUSDT", "BUY", 0.01, "cid1", ref_price=50000.0)
        f2 = b.place_perp_market("BTCUSDT", "SELL", 0.01, "cid2", ref_price=50010.0)
        self.assertTrue(f1["simulated"] and f2["simulated"])
        self.assertEqual(f1["fill_price"], 50000.0)
        self.assertEqual(f2["fill_price"], 50010.0)

    def test_live_blocked_without_credentials(self):
        os.environ.pop("BINANCE_API_KEY", None)
        os.environ.pop("BINANCE_SECRET_KEY", None)
        b = BinanceBroker(dry_run=False)
        self.assertIsNone(b.place_spot_market("BTCUSDT", "BUY", 0.01, "x", ref_price=1.0))
        self.assertIsNone(b.place_perp_market("BTCUSDT", "SELL", 0.01, "x", ref_price=1.0))

    def test_qty_floor_and_min_reject(self):
        b = BinanceBroker(dry_run=True)
        b.symbol_rules["TSTUSDT"] = {"qty_prec": 3, "step_size": 0.001, "min_qty": 0.002}
        self.assertAlmostEqual(b._format_qty("TSTUSDT", 0.0019), 0.0)  # below min
        self.assertAlmostEqual(b._format_qty("TSTUSDT", 0.0029), 0.002)  # floored
        b.spot_rules["TSTUSDT"] = {"qty_prec": 3, "step_size": 0.001, "min_qty": 0.002}
        self.assertAlmostEqual(b._format_spot_qty("TSTUSDT", 0.0029), 0.002)


class TestRollback(unittest.TestCase):
    def test_perp_failure_unwinds_spot(self):
        ex = botmod.DualLegExecutor(FakeBroker(fail_perp=True), CFG)
        out = ex.open_pair("BTCUSDT", 600.0, {"bid": 99.9, "ask": 100.1}, 100.05)
        self.assertIsNone(out)
        sides = [(v, s) for v, s, q in ex.broker.calls]
        self.assertIn(("spot", "BUY"), sides)
        self.assertIn(("spot", "SELL"), sides)  # rollback unwind
        buy_q = max(q for v, s, q in ex.broker.calls if (v, s) == ("spot", "BUY"))
        rb_q = max(q for v, s, q in ex.broker.calls if (v, s) == ("spot", "SELL"))
        self.assertAlmostEqual(buy_q, rb_q, places=8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
