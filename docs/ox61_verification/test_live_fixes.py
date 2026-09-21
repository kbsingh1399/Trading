"""OX61 regression tests: live fixes (ratchet rollover-drop + S4 sweep).
Usage: /home/user/ox61venv/bin/python docs/ox61_verification/test_live_fixes.py
"""
import sys
from pathlib import Path
from datetime import datetime, timezone
from types import SimpleNamespace

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import Engine.forex_engine as fe

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

# ---------------------------------------------------------------- F1: rollover-drop
class FakeConn:
    connected = True
    def __init__(self, bid, ask):
        self._bid, self._ask = bid, ask
    def get_last_tick(self, sym):
        return SimpleNamespace(bid=self._bid, ask=self._ask)

def make_mgr(bid=101.0, ask=101.02):
    mgr = fe.OrderManager.__new__(fe.OrderManager)
    mgr.conn = FakeConn(bid, ask)
    mgr.dry_run = True
    mgr.max_concurrent = 2
    mgr.open_trades = {}
    mgr.closed_trades = []
    mgr.initial_balance = 5000.0
    mgr.peak_equity = 5000.0
    mgr.in_defense_mode = False
    mgr.realized_pnl = 0.0
    mgr.state_file = Path("/tmp/ox61_test_state.json")
    mgr.save_state = lambda: None  # never touch live state
    return mgr

def seed_long(mgr, ticket=7, entry=100.0, sl=99.0, tp=103.5):
    mgr.open_trades[ticket] = {
        "symbol": "EURUSD", "real_symbol": "EURUSD", "ticket": ticket, "type": 0,
        "action": "BUY", "volume": 0.01, "entry": entry, "entry_price": entry,
        "sl": sl, "tp": tp, "r_dist": entry - sl, "risk_usd": 50.0,
        "strategy": "FVG_ML", "bars_elapsed": 0, "bars_held": 0,
        "highest_r": 0.0, "lowest_r": 0.0, "current_r": 0.0, "running_pnl": 0.0,
        "ratchet_phase": 0, "ratchet_desc": "Base SL (-1.00R)",
        "last_evaluated_bar": None,
    }

def test_rollover_drop():
    real_mt5, real_roll, real_fri = fe.mt5, fe.is_broker_rollover_window, fe.is_friday_closeout_window
    fe.mt5 = SimpleNamespace(ORDER_TYPE_BUY=0, ORDER_TYPE_SELL=1)
    try:
        bar = datetime(2025, 1, 8, 12, 0, tzinfo=timezone.utc)  # Wednesday noon
        # F1a: trigger during rollover -> phase held, SL untouched
        mgr = make_mgr(bid=101.0, ask=101.02)  # gain +1.0R -> phase-1 trigger
        seed_long(mgr)
        fe.is_friday_closeout_window = lambda *a, **k: False
        fe.is_broker_rollover_window = lambda *a, **k: True
        mgr.manage_open_trades(bar)
        t = mgr.open_trades[7]
        check("F1a rollover-holds-phase", t["ratchet_phase"] == 0 and abs(t["sl"] - 99.0) < 1e-9,
              f"phase={t['ratchet_phase']} sl={t['sl']}")
        # F1b: post-rollover retry applies the lock (would be dropped pre-fix)
        fe.is_broker_rollover_window = lambda *a, **k: False
        mgr.manage_open_trades(bar)
        t = mgr.open_trades[7]
        check("F1b post-rollover-retry", t["ratchet_phase"] == 1 and abs(t["sl"] - 100.15) < 1e-9,
              f"phase={t['ratchet_phase']} sl={t['sl']}")
        # F1c: failed modification rolls back phase (retry next tick)
        mgr2 = make_mgr()
        seed_long(mgr2)
        mgr2.modify_sl = lambda ticket, new_sl: False
        mgr2.manage_open_trades(bar)
        t2 = mgr2.open_trades[7]
        check("F1c fail-rolls-back", t2["ratchet_phase"] == 0 and abs(t2["sl"] - 99.0) < 1e-9,
              f"phase={t2['ratchet_phase']} sl={t2['sl']}")
    finally:
        fe.mt5, fe.is_broker_rollover_window, fe.is_friday_closeout_window = real_mt5, real_roll, real_fri

# ---------------------------------------------------------------- F2: S4 sweep
class FakeModel:
    def __init__(self, prob):
        self._p = prob
    def predict(self, dmat):
        return np.array([self._p])

def build_s4_buffer(last_o=100.9, last_h=101.5, last_l=99.9, last_c=101.2):
    """110 bars Tue 07:00 -> Wed 10:15; Tue flat ~100 (PDL 99.95, PDH 100.1);
    Wed selloff then rally; last bar crafted per test (KZ hour 10)."""
    n_tue, n_wed = 68, 42
    idx_tue = pd.date_range("2024-12-31 07:00", periods=n_tue, freq="15min", tz="UTC")
    idx_wed = pd.date_range("2025-01-01 00:00", periods=n_wed, freq="15min", tz="UTC")
    idx = idx_tue.append(idx_wed)
    o = np.full(110, 100.0); h = np.full(110, 100.1); l = np.full(110, 99.95); c = np.full(110, 100.0)
    # Wed selloff 00:00-06:30 (26 bars, idx 68..93): 100 -> 98.9 (stop must clear 2.5% cap)
    for k in range(26):
        px = 100.0 - (k + 1) * (1.1 / 26)
        o[68 + k], h[68 + k], l[68 + k], c[68 + k] = px + 0.05, px + 0.1, px - 0.05, px
    # Bridge 06:45-08:45 (idx 94..102): 98.9 -> 99.4
    for k in range(9):
        px = 98.9 + (k + 1) * (0.5 / 9)
        o[94 + k], h[94 + k], l[94 + k], c[94 + k] = px - 0.05, px + 0.05, px - 0.1, px
    # Structural liquidity spike (idx 96): 20-bar high for R_eff viability (live truth)
    h[96] = 107.5
    # Dip + rip (idx 103..108): FVG k=3 window vs high[104]=99.75
    dip = [(99.7, 99.8, 99.5, 99.6), (99.6, 99.75, 99.55, 99.7),
           (99.7, 100.1, 99.65, 100.0), (100.0, 100.4, 99.95, 100.3),
           (100.3, 100.7, 100.2, 100.6), (100.6, 101.0, 100.5, 100.9)]
    for k, (bo, bh, bl, bc) in enumerate(dip):
        o[103 + k], h[103 + k], l[103 + k], c[103 + k] = bo, bh, bl, bc
    # Last bar idx 109 (Wed 10:15, KZ)
    o[109], h[109], l[109], c[109] = last_o, last_h, last_l, last_c
    df = pd.DataFrame({"open": o, "high": h, "low": l, "close": c,
                       "datetime": idx}, index=idx)
    return df

def build_4h_buffer():
    idx = pd.date_range("2024-11-20 00:00", periods=210, freq="4h", tz="UTC")
    ramp = np.linspace(90.0, 110.0, 210)
    return pd.DataFrame({"open": ramp - 0.1, "high": ramp + 0.2,
                         "low": ramp - 0.2, "close": ramp}, index=idx)

def test_s4_sweep():
    from Engine.strategy.s4_fvg_ml.s4_fvg_ml_forex_engine import FVGMLForexCFDStrategy
    from Engine.core.base_strategy import EngineConfig
    strat = FVGMLForexCFDStrategy(config=EngineConfig.load())
    strat.model = FakeModel(0.90)
    buf4h = build_4h_buffer()
    # F2a: full setup (sweep 99.9 <= PDL 99.95, FVG+, trend+, KZ) -> LONG signal
    buf = build_s4_buffer()
    sig = strat.generate_signal("EURUSD", buf, buf4h)
    check("F2a setup-with-sweep-signals", sig.signal == 1, f"sig={sig.signal} reason={sig.reason}")
    # F2b: same structure minus any sweep (low 99.96 > PDL, high 100.05 < PDH) -> HOLD (No Sweep)
    buf2 = build_s4_buffer(last_o=100.0, last_h=100.05, last_l=99.96, last_c=100.0)
    sig2 = strat.generate_signal("EURUSD", buf2, buf4h)
    check("F2b no-sweep-holds", sig2.signal == 0 and "No Sweep" in sig2.reason,
          f"sig={sig2.signal} reason={sig2.reason}")

if __name__ == "__main__":
    print("OX61 live-fix regression tests:")
    test_rollover_drop()
    test_s4_sweep()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
