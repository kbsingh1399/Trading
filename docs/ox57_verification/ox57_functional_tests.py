"""OX ALPHA 57 — delta verification of the 4 residual fixes (commit 4806800).
Target: origin/main @ 9559471 (via /tmp/ox57_verify sandbox).
Fails loudly (assert) on any deviation.
"""
import sys, tempfile
from pathlib import Path
VERIFY_ROOT = Path("/tmp/ox57_verify")
sys.path.insert(0, str(VERIFY_ROOT))
assert "MetaTrader5" not in sys.modules

import numpy as np
import pandas as pd

RESULTS = []
def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    assert cond, f"{name}: {detail}"

import Engine.forex_engine as FE
from Engine.core.base_strategy import EngineConfig, ParallelForexStrategy

# ---------------------------------------------------------------- TEST J (backtest hysteresis)
def cands(rs, start="2024-02-01", step_h=30):
    base = pd.Timestamp(start, tz="UTC")
    return [{"datetime": base + pd.Timedelta(hours=k * step_h), "asset": "EURUSD",
             "cluster": "EUR", "sleeve": "FVG_ML", "r_realized": r,
             "outcome_r": r, "hold_bars": 24} for k, r in enumerate(rs)]

rs = [-1.0, -1.0, -1.0, +0.5, +0.5, +0.5, +0.5, -1.0, -1.0]
par = ParallelForexStrategy(config=EngineConfig())
par._cached_candidate_trades = pd.DataFrame(cands(rs))
res = par.run_backtest(start_date="2024-01-01", end_date="2024-12-31", save_plot=False)
risks = [round(v, 2) for v in res.trades_df["risk_usd"].values]
eq = [5000.0] + list(5000.0 + res.trades_df["pnl_usd"].cumsum().values)
pk = np.maximum.accumulate(np.array(eq))
pre_dd = [round((pk[i] - eq[i]) / pk[i] * 100, 3) for i in range(len(eq) - 1)]
check("J1 full risk sequence", risks == [50.0, 50.0, 27.5, 27.5, 27.5, 27.5, 27.5, 50.0, 27.5],
      f"risks={risks}")
check("J2 T7 evaluated inside hold band", 1.50 <= pre_dd[6] < 1.80, f"preDD={pre_dd[6]}")
check("J3 hysteresis HOLD at T7 (not 50)", risks[6] == 27.5, f"risk={risks[6]}")
check("J4 T8 evaluated below release", pre_dd[7] < 1.50, f"preDD={pre_dd[7]}")
check("J5 hysteresis RELEASE at T8", risks[7] == 50.0, f"risk={risks[7]}")
check("J6 defense RE-ENTRY at T9", risks[8] == 27.5 and pre_dd[8] >= 1.80,
      f"risk={risks[8]} preDD={pre_dd[8]}")

# J7: strict live/backtest parity on this non-monotonic path
class StubConn: connected = False
om = FE.OrderManager.__new__(FE.OrderManager)
om.conn = StubConn(); om.dry_run = True; om.max_concurrent = 2
om.open_trades = {}; om.closed_trades = []
om.initial_balance = 5000.0; om.peak_equity = 5000.0
om.in_defense_mode = False; om.realized_pnl = 0.0
om.state_file = Path("/tmp/ox57_tests/nonexistent_state.json")
live = []
for p in res.trades_df["pnl_usd"].values:
    live.append(round(om.get_current_risk_budget()[0], 2))
    om.realized_pnl += p
check("J7 live/backtest parity (non-monotonic)", live == risks, f"live={live}")

# ---------------------------------------------------------------- TEST K (connect/persist/docstring)
check("K1 engine connect() clean False", FE.MT5Connection().connect() is False)
check("K1b headless still clean", FE.mt5 is None)

def roundtrip(flag):
    tmp = Path(tempfile.mkdtemp()) / "live_state.json"
    a = FE.OrderManager.__new__(FE.OrderManager)
    a.conn = StubConn(); a.dry_run = True; a.max_concurrent = 2
    a.open_trades = {}; a.closed_trades = []
    a.initial_balance = 5000.0; a.peak_equity = 5120.0; a.realized_pnl = 120.0
    a.in_defense_mode = flag; a.state_file = tmp
    a.save_state()
    b = FE.OrderManager.__new__(FE.OrderManager)
    b.conn = StubConn(); b.dry_run = True; b.max_concurrent = 2
    b.open_trades = {}; b.closed_trades = []
    b.initial_balance = 5000.0; b.peak_equity = 5000.0; b.realized_pnl = 0.0
    b.in_defense_mode = (not flag); b.state_file = tmp
    b.load_state()
    return b
check("K2a defense=True survives restart", roundtrip(True).in_defense_mode is True)
check("K2b defense=False survives restart", roundtrip(False).in_defense_mode is False)
b = roundtrip(True)
check("K2c peak/pnl co-persisted", b.peak_equity == 5120.0 and b.realized_pnl == 120.0,
      f"peak={b.peak_equity} pnl={b.realized_pnl}")

lom_src = (VERIFY_ROOT / "Engine/live/order_manager.py").read_text()
check("K3 docstring synced to <= 2", "(<= 2)" in lom_src and "(<= 3)" not in lom_src)
bs_src = (VERIFY_ROOT / "Engine/core/base_strategy.py").read_text()
check("K4 friction comment units fixed", "8 bps on risk allocation" in bs_src
      and "8 bps real friction on notional" not in bs_src)

print(f"\nALL {len(RESULTS)} OX57 FUNCTIONAL CHECKS PASSED")
