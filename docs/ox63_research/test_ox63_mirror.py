"""OX63 unit tests: live/order_manager TP1 mirror (dry-run).
Usage: /home/user/ox61venv/bin/python docs/ox63_research/test_ox63_mirror.py
"""
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class FakeMT5:
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1
    POSITION_TYPE_BUY = 0


sys.modules.setdefault("MetaTrader5", FakeMT5())

import Engine.live.order_manager as lom  # noqa: E402

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")


class FakeConn:
    connected = True

    def __init__(self):
        self.quotes = {}

    def resolve_symbol(self, s):
        return s

    def get_last_tick(self, s):
        px = self.quotes.get(s, 100.0)
        return SimpleNamespace(bid=px, ask=px)


def make_mgr():
    conn = FakeConn()
    mgr = lom.OrderManager(connection=conn, dry_run=True,
                           state_file=Path(tempfile.mkdtemp()) / "dry.json")
    mgr.open_trades.clear()
    return mgr, conn


def inject(mgr, ticket=7, entry=100.0, sl=99.0, tp=102.5, risk=10.0, vol=1.0):
    mgr.open_trades[ticket] = {
        "ticket": ticket, "symbol": "EURUSD", "real_symbol": "EURUSD", "type": 0,
        "action": "BUY", "volume": vol, "entry": entry, "entry_price": entry,
        "cur_price": entry, "sl": sl, "tp": tp, "risk_usd": risk,
        "r_dist": abs(entry - sl), "bars_held": 0, "bars_elapsed": 0,
        "strategy": "TEST", "highest_r": 0.0, "lowest_r": 0.0, "current_r": 0.0,
        "running_pnl": 0.0, "ratchet_phase": 0, "ratchet_desc": "Base SL (-1.00R)",
        "last_bar_time": None, "tp1_scaled": False, "partial_pnl": 0.0,
    }


def test_tp1_then_tp2():
    mgr, conn = make_mgr()
    inject(mgr)
    conn.quotes["EURUSD"] = 101.15
    mgr.manage_open_trades()
    t = mgr.open_trades.get(7)
    ok1 = (t is not None and abs(t["partial_pnl"] - 5.50) < 1e-9
           and abs(t["volume"] - 0.5) < 1e-9 and abs(t["risk_usd"] - 5.0) < 1e-9
           and abs(t["sl"] - 100.15) < 1e-9 and t["tp1_scaled"] is True
           and t["ratchet_desc"].startswith("TP1 Scaled"))
    check("L1 mirror-tp1-partial", ok1, f"sl={t and t['sl']} desc={t and t['ratchet_desc']}")
    conn.quotes["EURUSD"] = 102.6
    mgr.manage_open_trades()
    check("L2 mirror-runner-tp2-closes", 7 not in mgr.open_trades)


def test_gap_over_both():
    mgr, conn = make_mgr()
    inject(mgr)
    calls = []
    orig = mgr.close_partial
    mgr.close_partial = lambda *a, **k: (calls.append((a, k)), orig(*a, **k))[1]
    conn.quotes["EURUSD"] = 102.6  # single tick over TP1 AND TP2
    mgr.manage_open_trades()
    ok = (7 not in mgr.open_trades and len(calls) == 1
          and abs(calls[0][1].get("exit_price", 0) - 101.1) < 1e-9)
    check("L3 gap-banks-tp1-then-tp2", ok, f"tp1_exit={calls and calls[0][1].get('exit_price')}")


def test_pre_tp1_stop():
    mgr, conn = make_mgr()
    inject(mgr)
    conn.quotes["EURUSD"] = 98.9
    mgr.manage_open_trades()
    check("L4 pre-tp1-stop-no-partial", 7 not in mgr.open_trades)


def test_tp0_guard():
    mgr, conn = make_mgr()
    inject(mgr, tp=0.0)
    conn.quotes["EURUSD"] = 101.15
    mgr.manage_open_trades()
    t = mgr.open_trades.get(7)
    ok = (t is not None and t["tp1_scaled"] is False and abs(t["partial_pnl"]) < 1e-9)
    check("L5 tp0-no-scale", ok)


def test_rollover_suppresses():
    mgr, conn = make_mgr()
    inject(mgr)
    conn.quotes["EURUSD"] = 101.15
    old = lom.is_broker_rollover_window
    lom.is_broker_rollover_window = lambda *a, **k: True
    try:
        mgr.manage_open_trades()
    finally:
        lom.is_broker_rollover_window = old
    t = mgr.open_trades.get(7)
    ok = (t is not None and t["tp1_scaled"] is False and abs(t["partial_pnl"]) < 1e-9)
    check("L6 rollover-suppresses-tp1", ok)


if __name__ == "__main__":
    lom.is_friday_closeout_window = lambda *a, **k: False  # weekday-robust
    print("OX63 live-mirror unit tests:")
    test_tp1_then_tp2()
    test_gap_over_both()
    test_pre_tp1_stop()
    test_tp0_guard()
    test_rollover_suppresses()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
