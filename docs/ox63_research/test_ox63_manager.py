"""OX63 unit tests: live/paper OrderManager 2-stage scaling + relaxed veto.
Usage: /home/user/ox61venv/bin/python docs/ox63_research/test_ox63_manager.py
"""
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class FakeMT5:
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1


sys.modules.setdefault("MetaTrader5", FakeMT5())

import Engine.forex_engine as fe  # noqa: E402

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")


class FakeConn:
    connected = False

    def __init__(self):
        self.quotes = {}

    def resolve_symbol(self, s):
        return s

    def get_last_tick(self, s):
        px = self.quotes.get(s, 100.0)
        return SimpleNamespace(bid=px, ask=px)


BAR_T = datetime(2026, 1, 5, 12, 0, tzinfo=timezone.utc)  # a Monday


def make_mgr():
    conn = FakeConn()
    mgr = fe.OrderManager(conn, dry_run=True)
    mgr.state_file = Path(tempfile.mkdtemp()) / "state.json"
    mgr.open_trades.clear()
    mgr.closed_trades.clear()
    mgr.realized_pnl = 0.0
    return mgr, conn


def inject(mgr, ticket=7, entry=100.0, sl=99.0, tp=102.5, risk=10.0, vol=1.0, typ=0):
    mgr.open_trades[ticket] = {
        "ticket": ticket, "symbol": "EURUSD", "real_symbol": "EURUSD", "type": typ,
        "action": "BUY" if typ == 0 else "SELL", "volume": vol, "entry": entry,
        "entry_price": entry, "cur_price": entry, "sl": sl, "tp": tp, "risk_usd": risk,
        "r_dist": abs(entry - sl), "entry_time": BAR_T, "bars_held": 0, "bars_elapsed": 0,
        "strategy": "TEST", "highest_r": 0.0, "lowest_r": 0.0, "current_r": 0.0,
        "running_pnl": 0.0, "ratchet_phase": 0, "ratchet_desc": "Base SL (-1.00R)",
        "last_evaluated_bar": None, "last_bar_time": None, "tp1_scaled": False,
    }


def test_tp1_partial_then_tp2():
    mgr, conn = make_mgr()
    inject(mgr)
    conn.quotes["EURUSD"] = 101.15
    mgr.manage_open_trades(BAR_T)
    t = mgr.open_trades.get(7)
    p = mgr.closed_trades[-1] if mgr.closed_trades else {}
    ok1 = (t is not None and abs(t["volume"] - 0.5) < 1e-9 and abs(t["risk_usd"] - 5.0) < 1e-9
           and abs(t["sl"] - 100.15) < 1e-9 and t["tp1_scaled"] is True and t["ratchet_phase"] == 1
           and p.get("reason", "").startswith("TP1 PARTIAL") and abs(p.get("realized_r", 0) - 0.55) < 1e-9
           and abs(p.get("realized_pnl", 0) - 5.50) < 1e-9)
    check("M1 tp1-partial", ok1, f"sl={t and t['sl']} risk={t and t['risk_usd']}")
    conn.quotes["EURUSD"] = 102.6
    mgr.manage_open_trades(BAR_T)
    c = mgr.closed_trades[-1]
    ok2 = (7 not in mgr.open_trades and abs(c.get("realized_r", 0) - 2.5) < 1e-9
           and abs(c.get("realized_pnl", 0) - 12.50) < 1e-9
           and abs(mgr.realized_pnl - 18.00) < 1e-9)
    check("M2 runner-tp2-total-1.80R", ok2, f"total_pnl={mgr.realized_pnl}")


def test_tp1_then_runner_stop():
    mgr, conn = make_mgr()
    inject(mgr)
    conn.quotes["EURUSD"] = 101.15
    mgr.manage_open_trades(BAR_T)
    conn.quotes["EURUSD"] = 100.10
    mgr.manage_open_trades(BAR_T)
    c = mgr.closed_trades[-1]
    ok = (c.get("reason", "").startswith("BE RATCHET")
          and abs(c.get("realized_r", 0) - 0.15) < 1e-9
          and abs(mgr.realized_pnl - 6.25) < 1e-9)
    check("M3 tp1-then-runner-stop-0.625R", ok, f"total_pnl={mgr.realized_pnl} reason={c.get('reason')}")


def test_pre_tp1_full_stop():
    mgr, conn = make_mgr()
    inject(mgr)
    conn.quotes["EURUSD"] = 98.9
    mgr.manage_open_trades(BAR_T)
    c = mgr.closed_trades[-1]
    ok = (c.get("reason", "").startswith("STOP LOSS") and abs(c.get("realized_r", 0) + 1.0) < 1e-9
          and abs(mgr.realized_pnl + 10.0) < 1e-9 and len(mgr.closed_trades) == 1)
    check("M4 pre-tp1-full-stop", ok, f"pnl={mgr.realized_pnl}")


def test_rollover_suppresses_tp1():
    mgr, conn = make_mgr()
    inject(mgr)
    conn.quotes["EURUSD"] = 101.15
    old = fe.is_broker_rollover_window
    fe.is_broker_rollover_window = lambda *a, **k: True
    try:
        mgr.manage_open_trades(BAR_T)
    finally:
        fe.is_broker_rollover_window = old
    t = mgr.open_trades.get(7)
    ok1 = (t is not None and t["tp1_scaled"] is False and len(mgr.closed_trades) == 0
           and abs(t["sl"] - 99.0) < 1e-9)
    check("M5a rollover-suppresses-tp1", ok1)
    mgr.manage_open_trades(BAR_T)  # real clock Monday: no rollover -> fires
    t = mgr.open_trades.get(7)
    ok2 = (t is not None and t["tp1_scaled"] is True and len(mgr.closed_trades) == 1)
    check("M5b tp1-retries-after-rollover", ok2)


def test_tp0_guard():
    mgr, conn = make_mgr()
    inject(mgr, tp=0.0)
    conn.quotes["EURUSD"] = 101.15
    mgr.manage_open_trades(BAR_T)
    t = mgr.open_trades.get(7)
    ok = (t is not None and t["tp1_scaled"] is False and len(mgr.closed_trades) == 0)
    check("M6 tp0-no-scale", ok)


def test_veto_boundary():
    kw = dict(symbol="EURUSD", is_long=True, entry=100.0, raw_sl=99.0,
              local_extreme=99.0, spread=0.0001, atr=0.01)
    r1 = fe.calculate_adaptive_sl_tp(**kw, tp_structural=101.19)
    r2 = fe.calculate_adaptive_sl_tp(**kw, tp_structural=101.20)
    r3 = fe.calculate_adaptive_sl_tp(**kw, tp_structural=103.50)
    r4 = fe.calculate_adaptive_sl_tp(**kw, tp_structural=104.00)
    r5 = fe.calculate_adaptive_sl_tp(**kw, tp_structural=None)
    ok = (r1[3] is False and "R_eff" in r1[4]
          and r2[3] is True and abs(r2[1] - 101.20) < 1e-9
          and r3[3] is True and abs(r3[1] - 103.50) < 1e-9
          and r4[3] is True and abs(r4[1] - 103.50) < 1e-9
          and r5[3] is True and abs(r5[1] - 102.50) < 1e-9)
    check("M7 veto-1.20-cap-3.50-fallback-2.5", ok, f"{r1[4]} | {r2[4]}")


if __name__ == "__main__":
    fe.is_friday_closeout_window = lambda *a, **k: False  # weekday-robust
    print("OX63 manager unit tests:")
    test_tp1_partial_then_tp2()
    test_tp1_then_runner_stop()
    test_pre_tp1_full_stop()
    test_rollover_suppresses_tp1()
    test_tp0_guard()
    test_veto_boundary()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
