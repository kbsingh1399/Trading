"""OX ALPHA 55 — functional verification of the 6 P0 remediation claims.
Runs against the origin/main tree (sparse checkout). Fails loudly (assert)
on any deviation from claimed behavior.
"""
import sys, tempfile
from pathlib import Path
from unittest.mock import MagicMock

VERIFY_ROOT = Path("/tmp/ox55_verify")
sys.path.insert(0, str(VERIFY_ROOT))

import numpy as np
import pandas as pd

RESULTS = []
def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    assert cond, f"{name}: {detail}"

# ---------------------------------------------------------------- TEST A
import Engine.forex_engine as FE
check("A1 forex_engine imports headless", FE.mt5 is None, f"mt5={FE.mt5}")
check("A2 sleeves auto-register", "fvg_ml" in FE.StrategyRegistry.list_strategies()
      and "orb_crt" in FE.StrategyRegistry.list_strategies(),
      f"keys={sorted(FE.StrategyRegistry.list_strategies())}")

from Engine.core.base_strategy import (
    ParallelForexStrategy, StrategySignal, EngineConfig, FOREX_CLUSTER_MAP)
from Engine.core.strategy_kernel import create_labels_ratchet

# ---------------------------------------------------------------- TEST B (governor)
tmp = Path(tempfile.mkdtemp()) / "live_state.json"
class StubConn:
    connected = False
om = FE.OrderManager.__new__(FE.OrderManager)
om.conn = StubConn(); om.dry_run = True; om.max_concurrent = 2
om.open_trades = {}; om.closed_trades = []; om.initial_balance = 5000.0
om.peak_equity = 5000.0; om.in_defense_mode = False; om.realized_pnl = 0.0
om.state_file = tmp
def eq_cash(pnl):
    om.realized_pnl = pnl
    return om.get_current_risk_budget()
r, lbl = eq_cash(600.0)   # equity 5600, peak 5600
check("B1 house-money accel", r == 65.0, f"risk={r}")
r, lbl = eq_cash(300.0)   # equity 5300 -> peak-DD 5.36% while net +300
check("B2 hard freeze in net profit (peak DD)", r == 0.0 and om.in_defense_mode,
      f"risk={r} lbl={lbl[:40]}")
r, lbl = eq_cash(420.0)   # equity 5420 -> DD 3.21% -> SEVERE 16.50
check("B3 severe defense", r == 16.50, f"risk={r}")
r, lbl = eq_cash(490.0)   # equity 5490 -> DD 1.96% -> MILD 27.50
check("B4 mild defense", r == 27.50, f"risk={r}")
r, lbl = eq_cash(500.0)   # equity 5500 -> DD 1.79% -> hysteresis HOLD 27.50
check("B5 hysteresis hold below 1.80", r == 27.50 and om.in_defense_mode, f"risk={r}")
r, lbl = eq_cash(530.0)   # equity 5530 -> DD 1.25% -> release; pnl>=80 but DD>=1.0 -> 50
check("B6 hysteresis release + flag reset",
      r == 50.0 and om.in_defense_mode is False, f"risk={r}")
check("B7 peak ratchets only up", om.peak_equity == 5600.0, f"peak={om.peak_equity}")
# pass-lock branch
om2 = FE.OrderManager.__new__(FE.OrderManager)
om2.conn = StubConn(); om2.dry_run = True; om2.max_concurrent = 2
om2.open_trades = {}; om2.closed_trades = [{"pnl": 1}] * 15
om2.initial_balance = 5000.0; om2.peak_equity = 5500.0
om2.in_defense_mode = False; om2.realized_pnl = 500.0; om2.state_file = tmp
r, lbl = om2.get_current_risk_budget()
check("B8 milestone pass-lock 7.50", r == 7.50, f"risk={r} lbl={lbl[:30]}")

# ---------------------------------------------------------------- TEST C (conflict path)
class StubSleeve:
    def __init__(self, name, sig):
        self.name = name; self._sig = sig
    def generate_signal(self, symbol, df, buf4h=None, **kwargs):
        s = StrategySignal(symbol=symbol, signal=self._sig, strategy_tag=self.name)
        return s
cfg = EngineConfig()
par = ParallelForexStrategy.__new__(ParallelForexStrategy)
par.config = cfg
par.sleeves = {"fvg_ml": StubSleeve("fvg_ml", 1), "orb_crt": StubSleeve("orb_crt", -1)}
dummy = pd.DataFrame({"close": [1.0] * 30})
out = par.generate_signal("EURUSD", dummy)   # must not raise AttributeError
check("C1 conflict veto no crash", out.signal == 0 and "CONFLICT VETO" in out.reason,
      f"reason={out.reason}")
check("C2 conflict names both sides",
      "fvg_ml(BUY)" in out.reason and "orb_crt(SELL)" in out.reason, f"reason={out.reason}")
try:
    _ = StrategySignal(symbol="X", signal=1).side
    check("C3 StrategySignal has no .side", False, "unexpected .side attr")
except AttributeError:
    check("C3 StrategySignal has no .side (fix premise valid)", True)

# ---------------------------------------------------------------- TEST D (labeler unit)
n = 140
df = pd.DataFrame({
    "datetime": pd.date_range("2024-01-01", periods=n, freq="15min", tz="UTC"),
    "open": np.full(n, 100.0), "high": np.full(n, 100.5),
    "low": np.full(n, 99.5), "close": np.full(n, 100.0),
    "sweep_pdl": np.zeros(n, dtype=int), "sweep_pdh": np.zeros(n, dtype=int),
    "bullish_fvg": np.zeros(n), "bearish_fvg": np.zeros(n),
    "htf_4h_trend": np.ones(n, dtype=int),
    "local_low_20": np.full(n, 99.0), "local_high_20": np.full(n, 101.0),
    "is_kill_zone": np.ones(n, dtype=bool),
})
i = 40
df.loc[i, ["sweep_pdl", "bullish_fvg"]] = [1, 1.0]
df.loc[i, "close"] = 100.0
df.loc[i + 1, "open"] = 100.30          # gap up: only opens[i+1] fill sees this
df.loc[i + 1, ["high", "low", "close"]] = [100.40, 100.20, 100.35]
df.loc[i + 2, ["open", "high", "low", "close"]] = [100.35, 100.45, 98.50, 98.60]  # SL smash
out = create_labels_ratchet(df.copy())
# entry=100.30, sl=99.0, r_dist=1.30 -> SL hit bar i+2: r=-1.0-0.08=-1.08
check("D1 next-open entry + SL-first + friction",
      abs(out.loc[i, "r_realized"] - (-1.08)) < 1e-6 and out.loc[i, "target"] == 0,
      f"r={out.loc[i, 'r_realized']}")
# close-fill counterfactual would be entry=100.0, r_dist=1.0 -> -1.08 too; disambiguate:
# friction proof: TP-only case. bar i+1 low must stay above sl.
df2 = df.copy()
df2.loc[i + 2, ["open", "high", "low", "close"]] = [100.35, 104.00, 100.20, 103.90]  # TP smash, no SL touch
out2 = create_labels_ratchet(df2)
# tp = 100.30+2.5*1.30 = 103.55 -> hit: r = 2.5-0.08 = 2.42
check("D2 TP path nets 2.42 after friction",
      abs(out2.loc[i, "r_realized"] - 2.42) < 1e-6 and out2.loc[i, "target"] == 1,
      f"r={out2.loc[i, 'r_realized']}")
# both-touched bar: SL-first must win even when TP also in range
df3 = df.copy()
df3.loc[i + 2, ["open", "high", "low", "close"]] = [100.35, 104.00, 98.50, 100.00]
out3 = create_labels_ratchet(df3)
check("D3 labeler SL-before-TP same bar", abs(out3.loc[i, "r_realized"] - (-1.08)) < 1e-6,
      f"r={out3.loc[i, 'r_realized']}")

# ---------------------------------------------------------------- TEST E (run_standard_backtest SL-first)
from Engine.core.base_strategy import BaseForexStrategy
LONG = {"fire": True}
class OneShotLong(BaseForexStrategy):
    name = "oneshot"
    def initialize(self, config=None):
        self.initialized = True
    def run_backtest(self, *a, **k):
        raise NotImplementedError
    def generate_signal(self, symbol, df_slice):
        if LONG["fire"]:
            LONG["fire"] = False
            px = float(df_slice["close"].iloc[-1])
            return StrategySignal(symbol=symbol, signal=1, sl_price=px - 1.0,
                                  tp_price=px + 2.5, strategy_tag="oneshot")
        return StrategySignal(symbol=symbol, signal=0, strategy_tag="oneshot")
mkt = pd.DataFrame({
    "datetime": pd.date_range("2024-01-01", periods=80, freq="15min", tz="UTC"),
    "open": np.full(80, 100.0), "high": np.full(80, 100.2),
    "low": np.full(80, 99.8), "close": np.full(80, 100.0),
})
# signal fires at i=25 -> entry bar 26 open=100, sl=99, tp=102.5; bar 27 touches BOTH
mkt.loc[27, ["open", "high", "low", "close"]] = [100.0, 103.0, 98.5, 100.0]
orig_eng = FE.engineer_features_polars
FE.engineer_features_polars = lambda sym, dd: mkt.copy()
try:
    res = FE.run_standard_backtest(OneShotLong(config=EngineConfig()),
                                   start_date="2024-01-01", end_date="2024-02-01",
                                   symbols=["SYNTH"], save_plot=False)
finally:
    FE.engineer_features_polars = orig_eng
check("E1 exactly one trade", res.total_trades == 1, f"n={res.total_trades}")
rr = float(res.trades_df["realized_r"].iloc[0]) if "realized_r" in res.trades_df.columns \
    else float(res.trades_df["r_realized"].iloc[0])
check("E2 SL-first: ambiguous bar books loss", abs(rr - (-1.08)) < 1e-6, f"r={rr}")

# ---------------------------------------------------------------- TEST F (live OM dry-run w/ stubbed MT5)
stub_mt5 = MagicMock()
stub_mt5.account_info.return_value = None
sys.modules["MetaTrader5"] = stub_mt5
for mod in [m for m in list(sys.modules) if m.startswith("Engine.live")]:
    del sys.modules[mod]
sys.path.insert(0, str(VERIFY_ROOT / "Engine" / "live"))
import order_manager as LOM
LOM.is_broker_rollover_window = lambda: False
LOM.is_friday_weekend_lockout = lambda: False
check("F1 live OM MAX_CONCURRENT=2", LOM.MAX_CONCURRENT_POSITIONS == 2,
      f"v={LOM.MAX_CONCURRENT_POSITIONS}")
check("F2 live clusters == engine clusters (4-bloc)",
      LOM.CORRELATION_CLUSTERS == FE.CORRELATION_CLUSTERS,
      f"live={sorted(LOM.CORRELATION_CLUSTERS.keys())}")
lom = LOM.OrderManager(connection=None, dry_run=True,
                       state_file=str(Path(tempfile.mkdtemp()) / "dry.json"))
t = lom.place_market_order("EURUSD", "BUY", sl_price=1.0950, risk_usd=25.0)
check("F3 dry-run place_market_order opens position",
      t is not None and t in lom.open_trades,
      f"ticket={t} n_open={len(lom.open_trades)}")
check("F3b dry-run records risk/size/ratchet state",
      lom.open_trades[t]["risk_usd"] == 25.0 and lom.open_trades[t]["volume"] == 0.01
      and lom.open_trades[t]["ratchet_phase"] == 0,
      f"{ {k: lom.open_trades[t][k] for k in ('risk_usd','volume','ratchet_phase')} }")
ok = lom.modify_sl(t, 1.0980)
check("F4 dry-run modify_sl reachable (no broker lookup)",
      ok is True and abs(lom.open_trades[t]["sl"] - 1.0980) < 1e-9,
      f"ok={ok} sl={lom.open_trades.get(t, {}).get('sl')}")
okc = lom.close_position(t)
check("F5 dry-run close_position releases slot", okc is True and t not in lom.open_trades,
      f"ok={okc} n_open={len(lom.open_trades)}")

print(f"\nALL {len(RESULTS)} FUNCTIONAL CHECKS PASSED")
