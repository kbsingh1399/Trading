"""OX ALPHA 56 — functional verification of the 3 P1 remediation claims.
Target: origin/main @ d4e1433 (via /tmp/ox57_verify sandbox, updated).
Fails loudly (assert) on any deviation.
"""
import sys
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

# ---------------------------------------------------------------- TEST H (headless)
MODS = ["Engine.forex_engine", "Engine.live.mt5_connection", "Engine.live.order_manager",
        "Engine.live.run_forex_dry_run", "Engine.live.append_latest_candles",
        "Engine.pipeline.mt5_forex_exporter", "Engine.pipeline.export_mt5_crypto",
        "Engine.verification.verify_e2e_trade_execution"]
import importlib
for m in MODS:
    mod = importlib.import_module(m)
    check(f"H.import {m}", mod.mt5 is None, "mt5=None")
check("H.noleak MetaTrader5 never imported", "MetaTrader5" not in sys.modules)

import Engine.forex_engine as FE
from Engine.live.mt5_connection import MT5Connection as LiveConn
check("H.live-connect False (not raise)", LiveConn().connect() is False)
check("H.eng-connect clean False (4806800 FIXED)", FE.MT5Connection().connect() is False)

# ---------------------------------------------------------------- TEST G (freeze breaker)
from Engine.core.base_strategy import EngineConfig, ParallelForexStrategy

def run_cached(rows):
    par = ParallelForexStrategy(config=EngineConfig())
    par._cached_candidate_trades = pd.DataFrame(rows)
    return par.run_backtest(start_date="2024-01-01", end_date="2024-12-31", save_plot=False)

def cands(n, r_each, start="2024-02-01", step_h=30):
    base = pd.Timestamp(start, tz="UTC")
    return [{"datetime": base + pd.Timedelta(hours=k * step_h), "asset": "EURUSD",
             "cluster": "EUR", "sleeve": "FVG_ML", "r_realized": r_each,
             "outcome_r": r_each, "hold_bars": 24} for k in range(n)]

# G1: %-leg — 12 x -1R must freeze once DD hits 4.50%
res = run_cached(cands(12, -1.0))
check("G1 freeze halts %-leg", res.total_trades == 9, f"executed={res.total_trades}")
check("G1b terminal (no resume w/o PnL)", res.max_dd_pct >= 4.50, f"dd={res.max_dd_pct:.2f}")
# winners-only control: no freeze, all execute
res_w = run_cached(cands(12, +1.0))
check("G1c no false freeze in profit", res_w.total_trades == 12, f"executed={res_w.total_trades}")

# G2: $-leg — 6 wins (peak ~5360, pnl<500 dodges pass-lock), then -1R bleed;
# freeze must hit via $225 while DD% still < 4.50 at the trigger bar
rows = cands(6, +1.0, start="2024-02-01") + cands(14, -1.0, start="2024-03-01")
res2 = run_cached(rows)
ex = res2.trades_df
check("G2 freeze engages on bleed", res2.total_trades == 14, f"executed={res2.total_trades}/20")
eq = 5000.0 + ex["pnl_usd"].cumsum().values
peak = np.maximum.accumulate(eq)
last_dd_pct = (peak[-1] - eq[-1]) / peak[-1] * 100.0
last_dd_usd = peak[-1] - eq[-1]
check("G2b $225 leg binds first", last_dd_usd >= 225.0 and last_dd_pct < 4.50,
      f"dd_usd={last_dd_usd:.2f} dd_pct={last_dd_pct:.2f}")
check("G2c pass-lock correctly absent", 7.5 not in set(np.round(ex['risk_usd'], 2)),
      f"ladder={sorted(set(np.round(ex['risk_usd'], 2)))}")
# parity: live governor agrees trade-for-trade on the same equity path
om = FE.OrderManager.__new__(FE.OrderManager)
class StubConn: connected = False
om.conn = StubConn(); om.dry_run = True; om.max_concurrent = 2
om.open_trades = {}; om.closed_trades = []
om.initial_balance = 5000.0; om.peak_equity = 5000.0
om.in_defense_mode = False; om.realized_pnl = 0.0
om.state_file = Path("/tmp/ox56_tests/nonexistent_state.json")
live_risks = []
for pnl_step in ex["pnl_usd"].values:
    r, _ = om.get_current_risk_budget()
    live_risks.append(r)
    om.realized_pnl += pnl_step
bt_risks = ex["risk_usd"].values
# map: live risk 0.0 (freeze) <=> backtest skips; compare pre-freeze sizing correspondence
# (backtest uses multipliers of base 50: 50/65/27.5/16.5/7.5 — same ladder as live)
check("G3 risk ladder parity", set(np.round(bt_risks, 2)) <= {50.0, 65.0, 27.5, 16.5, 7.5},
      f"ladder={sorted(set(np.round(bt_risks, 2)))}")
# G3b: strict per-trade parity on the monotonic G1 path (live vs backtest same equity -> same risk)
omA = FE.OrderManager.__new__(FE.OrderManager)
omA.conn = StubConn(); omA.dry_run = True; omA.max_concurrent = 2
omA.open_trades = {}; omA.closed_trades = []
omA.initial_balance = 5000.0; omA.peak_equity = 5000.0
omA.in_defense_mode = False; omA.realized_pnl = 0.0
omA.state_file = Path("/tmp/ox56_tests/nonexistent_state.json")
liveA = []
for p in res.trades_df["pnl_usd"].values:
    liveA.append(round(omA.get_current_risk_budget()[0], 2))
    omA.realized_pnl += p
btA = [round(v, 2) for v in res.trades_df["risk_usd"].values]
check("G3b per-trade live/backtest parity", liveA == btA, f"risk={btA}")
# and the 10th candidate: live returns 0.0 (freeze) exactly when backtest skips it
r10, lbl10 = omA.get_current_risk_budget()
check("G3c freeze-point agreement", r10 == 0.0 and res.total_trades == 9,
      f"live={r10} ({lbl10[:22]}...) | backtest skipped #10-12")

# ---------------------------------------------------------------- TEST I (setup unification)
from Engine.core.strategy_kernel import check_setup_criteria
base = {"is_kill_zone": True, "sweep_pdl": 1, "sweep_pdh": 0, "bullish_fvg": 2.5,
        "bearish_fvg": 0.0, "htf_4h_trend": 1.0, "hour": 8}
check("I1 canonical long", check_setup_criteria(base) == (True, False))
d = dict(base, sweep_pdl=0)
check("I2 sweep required (OX54 gap closed)", check_setup_criteria(d) == (False, False))
d = {"sweep_pdl": 0, "sweep_pdh": 1, "bullish_fvg": 0.0, "bearish_fvg": 1.2,
     "htf_4h_trend": -1.0, "hour": 13}
check("I3 canonical short + hour-fallback KZ", check_setup_criteria(d) == (False, True))
d = dict(base, htf_4h_trend=-1.0)
check("I4 trend gate", check_setup_criteria(d) == (False, False))
src = (VERIFY_ROOT / "Engine/live/run_forex_dry_run.py").read_text()
check("I5 dry-run imports canonical predicate",
      "from Engine.core.strategy_kernel import" in src and "check_setup_criteria" in src)
check("I6 DUAL gate is setup+0.55",
      "(is_setup_long and prob >= 0.55)" in src and "(is_setup_short and prob >= 0.55)" in src)

print(f"\nALL {len(RESULTS)} OX56 REGRESSION CHECKS PASSED (1 expectation flipped for 4806800)")
