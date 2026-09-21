"""OX ALPHA 55 — empirical reproduction on origin/main tree.
Mode 'parallel': ParallelForexStrategy.run_backtest x 20 windows -> vs perfect CSV.
Mode 'fvg': FVG sleeve run_backtest x 20 windows -> label-change impact vs OX54.
Writes results CSV + prints comparison table.
"""
import sys, json, time
from pathlib import Path
VERIFY_ROOT = Path("/tmp/ox55_verify")
sys.path.insert(0, str(VERIFY_ROOT))
import logging
logging.disable(logging.CRITICAL)
import pandas as pd

mode = sys.argv[1] if len(sys.argv) > 1 else "parallel"
windows = json.load(open(VERIFY_ROOT / "Engine/oos_windows_forex_20.json"))

import Engine.forex_engine  # noqa: F401  (side-effect: registry population)
from Engine.core.base_strategy import EngineConfig, StrategyRegistry

if mode == "parallel":
    strat = StrategyRegistry.get("parallel")(config=EngineConfig())
    out_csv = "/tmp/ox55_tests/ox56_parallel_perwindow.csv"
else:
    strat = StrategyRegistry.get("fvg_ml")(config=EngineConfig())
    out_csv = "/tmp/ox55_tests/ox55_fvg_20w.csv"

rows = []
t0 = time.time()
for w in windows:
    wid = w["window_id"]
    r = strat.run_backtest(start_date=w["start_date"], end_date=w["end_date"], save_plot=False)
    rows.append({"window_id": wid, "name": w["name"], "trades": r.total_trades,
                 "win_rate": round(r.win_rate, 2), "profit_factor": round(r.profit_factor, 3),
                 "net_r": round(r.net_r, 2), "pnl_usd": round(r.net_pnl_usd, 2),
                 "roi_pct": round(r.net_roi_pct, 2), "max_dd_pct": round(r.max_dd_pct, 2),
                 "passed": r.passed_criteria, "failures": ";".join(r.failure_reasons or [])})
    print(f"W{wid:02d} trades={r.total_trades:4d} WR={r.win_rate:5.1f}% PF={r.profit_factor:5.2f} "
          f"R={r.net_r:+8.1f} PnL=${r.net_pnl_usd:+9.2f} ROI={r.net_roi_pct:+6.2f}% "
          f"DD={r.max_dd_pct:5.2f}% {'PASS' if r.passed_criteria else 'FAIL'}", flush=True)
df = pd.DataFrame(rows)
df.to_csv(out_csv, index=False)
print(f"\n[{mode}] windows passed: {df['passed'].sum()}/20 | total PnL=${df.pnl_usd.sum():+.2f} | "
      f"total R={df.net_r.sum():+.1f} | max DD={df.max_dd_pct.max():.2f}% | elapsed={time.time()-t0:.0f}s")
print(f"wrote {out_csv}")
