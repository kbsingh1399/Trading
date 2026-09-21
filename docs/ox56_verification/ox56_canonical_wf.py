"""Canonical path: ForexEngine.run_walkforward('parallel', fail_fast=False).
ROOT env selects tree (/tmp/ox55_verify or /tmp/ox55_pre). PRE=1 stubs mt5."""
import sys, os
from pathlib import Path
ROOT = Path(os.environ.get("ROOT", "/tmp/ox55_verify"))
sys.path.insert(0, str(ROOT))
if os.environ.get("PRE") == "1":
    from unittest.mock import MagicMock
    sys.modules["MetaTrader5"] = MagicMock()
import logging
logging.disable(logging.CRITICAL)
import Engine.forex_engine as FE

eng = FE.ForexEngine()
print("windows:", len(eng.config.windows), "| path:", eng.config.windows_path)
strat = eng.load_strategy("parallel")
print("strategy:", strat.name, "| sleeves:", list(strat.sleeves.keys()))
strat.precompute_candidates()
print("cached candidates:", len(strat._cached_candidate_trades))
import pandas as pd
rows = []
for w in eng.config.windows:
    r = strat.run_backtest(start_date=w.start_date, end_date=w.end_date, save_plot=False)
    rows.append({"window_id": w.window_id, "name": w.name, "trades": r.total_trades,
                 "win_rate": round(r.win_rate, 2), "profit_factor": round(r.profit_factor, 3),
                 "net_r": round(r.net_r, 2), "pnl_usd": round(r.net_pnl_usd, 2),
                 "roi_pct": round(r.net_roi_pct, 2), "max_dd_pct": round(r.max_dd_pct, 2),
                 "passed": r.passed_criteria})
    print(f"W{w.window_id:02d} trades={r.total_trades:4d} WR={r.win_rate:5.1f}% PF={r.profit_factor:5.2f} "
          f"R={r.net_r:+8.1f} PnL=${r.net_pnl_usd:+9.2f} ROI={r.net_roi_pct:+6.2f}% "
          f"DD={r.max_dd_pct:5.2f}% {'PASS' if r.passed_criteria else 'FAIL'}", flush=True)
tag = "pre" if os.environ.get("PRE") == "1" else "post"
df = pd.DataFrame(rows)
df.to_csv(f"/tmp/ox55_tests/ox56_canonical_{tag}.csv", index=False)
print(f"\n[{tag}] passed: {df['passed'].sum()}/20 | PnL=${df.pnl_usd.sum():+.2f} | maxDD={df.max_dd_pct.max():.2f}%")
