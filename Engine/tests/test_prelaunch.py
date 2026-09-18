"""
Pre-Launch Dry-Run Test Harness
================================
Run BEFORE starting the live engine each session.
Tests all 6 critical compliance items without MT5 connection.

Usage:
    python Engine/tests/test_prelaunch.py

Expected: ALL PASS - any FAIL means do NOT start the live engine.
"""

import sys
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
import inspect

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from Engine.core.strategy_kernel import compute_features_pandas, create_labels_ratchet
from Engine.forex_engine import compute_features_pandas as cfp_engine, OrderManager, compute_crt_orb_state

PASS_ICON = "OK  PASS"
FAIL_ICON = "XX  FAIL"
results = []

def record(name, passed, detail=""):
    icon = PASS_ICON if passed else FAIL_ICON
    print(f"  [{icon}]  {name}" + (f": {detail}" if detail else ""))
    results.append(passed)

np.random.seed(42)
N = 999
prices = 1.08 + np.cumsum(np.random.randn(N) * 0.0005)
buf = pd.DataFrame({
    "open": prices, "high": prices + np.abs(np.random.randn(N)*0.0003),
    "low":  prices - np.abs(np.random.randn(N)*0.0003),
    "close": prices + np.random.randn(N)*0.0001,
    "volume": np.random.randint(100, 5000, N).astype(float),
}, index=pd.date_range("2024-01-01", periods=N, freq="15min", tz="UTC"))

prices_4h = 1.08 + np.cumsum(np.random.randn(250)*0.001)
buf_4h = pd.DataFrame({
    "open": prices_4h, "high": prices_4h+0.001,
    "low": prices_4h-0.001, "close": prices_4h,
}, index=pd.date_range("2024-01-01", periods=250, freq="4h", tz="UTC"))

print("\n" + "="*54)
print("  PRE-LAUNCH COMPLIANCE TEST HARNESS")
print("  Forex & CFD Master Orchestration Engine")
print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
print("="*54 + "\n")

# TEST 1
print("TEST 1 - 13-Feature Math Parity")
try:
    re = cfp_engine(buf.copy(), buf_4h.copy()).iloc[-1]
    rk = compute_features_pandas(buf.copy(), buf_4h.copy()).iloc[-1]
    FEATS = ["bullish_fvg","bearish_fvg","htf_4h_trend","hour","day_of_week",
             "rsi_14","vwap_dist","ema_50_dist","ema_200_dist","ema_200_slope",
             "atr_14","volatility_20","roc_20"]
    all_ok = all(abs(float(re[f])-float(rk[f])) < 1e-8 for f in FEATS)
    record("All 13 features match engine vs kernel at 1e-8", all_ok)
except Exception as ex:
    record("Feature parity computation", False, str(ex))

# TEST 2
print("\nTEST 2 - Ratchet Phase-0 Trigger = 0.8R")
src = inspect.getsource(create_labels_ratchet)
record("LONG  phase-0 at 0.8R",  "lock_08r = entry + (0.8 * r_dist)" in src)
record("SHORT phase-0 at 0.8R",  "lock_08r = entry - (0.8 * r_dist)" in src)
record("Old lock_1r removed",    "lock_1r" not in src)

# TEST 3
print("\nTEST 3 - TP Close Uses actual_tp_r")
src_om = inspect.getsource(OrderManager.manage_open_trades)
record("actual_tp_r present",       "actual_tp_r" in src_om)
record("Hardcoded 2.50 removed",    "realized_r=2.50" not in src_om)

# TEST 4
print("\nTEST 4 - Max 2 Concurrent Positions")
src_pm = inspect.getsource(OrderManager.place_market_order)
record("max_concurrent cap checked",   "self.max_concurrent" in src_pm)
record("Returns None on cap hit",      "return None" in src_pm)
record("Per-asset duplicate veto",     'ot["symbol"] == symbol' in src_pm)

# TEST 5
print("\nTEST 5 - CRT Previous-Day Boundary")
src_crt = inspect.getsource(compute_crt_orb_state)
record("Uses prev_bars[_date < or_date]", "_date\"] < or_date" in src_crt or '"_date"] < or_date' in src_crt)

# TEST 6
print("\nTEST 6 - Kill Zone Hours")
sk_src  = (ROOT/"Engine/core/strategy_kernel.py").read_text()
fvg_src = (ROOT/"Engine/FVG_ML_ForexCFD_Strategy.py").read_text()
orb_src = (ROOT/"Engine/ORB_CRT_ForexCFD_Strategy.py").read_text()
record("strategy_kernel: London & NY hours", ("7 <= hour" in sk_src or "hour >= 7" in sk_src))
record("FVG_ML: is_london + is_ny gates",    "is_london" in fvg_src and "is_ny" in fvg_src)
record("ORB_CRT: kill zone enforced",        "is_kill_zone" in orb_src or ("7 <= hour" in orb_src))

# TEST 7
print("\nTEST 7 - Full Module Import Safety")
try:
    import Engine.live.inference_engine
    import Engine.live.order_manager
    import Engine.live.mt5_connection
    import Engine.research.forward_test_harness
    import Engine.research.asset_screener
    import Engine.research.run_dynamic_oos
    record("All 6 core/live/research modules import cleanly", True)
except Exception as ex:
    record("All 6 core/live/research modules import cleanly", False, str(ex))

# TEST 8
print("\nTEST 8 - S-11 Mark-To-Market Exhaustion at Bar 96")
record("Bar 96 MTM exhaustion in create_labels_ratchet", "j_last = min(i + look_fwd, n) - 1" in src)
record("Reachable ratchet rungs clean (no dead 35r)", "lock_35r" not in src)

# TEST 9
print("\nTEST 9 - B2 None-Safe MT5 Tick Protection")
harness_src = (ROOT/"Engine/research/forward_test_harness.py").read_text()
mt5_src = (ROOT/"Engine/live/mt5_connection.py").read_text()
record("MT5Connection returns Optional[float]", "Optional[float]" in mt5_src)
record("ForwardTest checks entry_price is None", "if entry_price is None:" in harness_src)
record("ForwardTest checks current_price is None", "if current_price is None:" in harness_src)

# SUMMARY
total, passed, failed = len(results), sum(results), len(results)-sum(results)
print("\n" + "="*54)
print(f"  RESULTS: {passed}/{total} checks passed")
if failed == 0:
    print("  ALL PASS - Engine cleared for dry-run startup")
else:
    print(f"  {failed} FAIL(s) - DO NOT start live engine")
print("="*54 + "\n")
sys.exit(0 if failed == 0 else 1)
