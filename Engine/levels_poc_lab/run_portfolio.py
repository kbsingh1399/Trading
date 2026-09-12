"""Walk-forward portfolio scorecard for the levels / POC families.

For each of the 20 pre-registered OOS windows:

1. features are cut at the window start minus the 72 h quarantine;
2. optional causal filters are applied (family subset, BTC macro-tide filter);
3. signals inside the window are ranked cross-sectionally by score and executed
   by ``kernel.simulate`` with the certified cost model;
4. the repo's ``score_metrics`` decides PASS/FAIL against the mission criteria.

Nothing inside a window is fitted.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import PURGE_MS
from .data import ALTCOINS, BTC, load_all, windows, window_bounds
from .kernel import LabConfig, prepare_execution_frame, simulate
from .signals import FamilySpec, build_signal_frame, default_specs, naked_poc_series

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORE_DIR = REPO_ROOT / "scratch"


def build_symbol_signals(f: pd.DataFrame, specs: list[FamilySpec]) -> pd.DataFrame:
    t = f.open_time_ms.to_numpy(np.int64)
    day = t // 86_400_000
    naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                             f.high.to_numpy(float), f.close.to_numpy(float))
    sig = build_signal_frame(f, specs, naked=naked)
    return prepare_execution_frame(f, sig)


def make_macro_filter(data: dict[str, pd.DataFrame]):
    """Return f(symbol, frame, signal_frame) -> masked signal frame.

    Longs are only allowed while BTC trades above its 4h trend anchor; shorts only
    while it trades below.  The anchor is causal (EWM, evaluated at bar t).
    """
    btc = data[BTC].set_index("open_time_ms")
    tide = (btc.close > btc.e200_4h).astype(np.int8)

    def _apply(sym, f, sig):
        t = tide.reindex(f.open_time_ms).fillna(0).to_numpy(np.int8)
        bad = ((t == 1) & (sig.signal.to_numpy() < 0)) | ((t == 0) & (sig.signal.to_numpy() > 0))
        sig = sig.copy()
        sig.loc[bad, "signal"] = 0
        sig.loc[bad, "stop_distance"] = np.nan
        return sig

    return _apply


def score_windows(data: dict[str, pd.DataFrame], specs, cfg: LabConfig, wins,
                  pre=None, verbose: bool = True) -> dict:
    rows = []
    total_trades = 0
    total_pnl = 0.0
    passed = 0
    for w in wins:
        start_ms, end_ms = window_bounds(w)
        per_symbol = {}
        for sym, f in data.items():
            if sym == BTC:
                continue
            sig = build_symbol_signals(f, specs)
            if pre is not None:
                sig = pre(sym, f, sig)
            mask = (sig.open_time_ms >= start_ms - PURGE_MS) & (sig.open_time_ms <= end_ms)
            per_symbol[sym] = sig[mask].copy()
        res = simulate(per_symbol, start_ms, end_ms, cfg)
        m = res["metrics"]
        is_pass = m["verdict"] == "PASS"
        passed += int(is_pass)
        total_trades += m["total_trades"]
        total_pnl += m["net_profit_usd"]
        rows.append({
            "window_id": w["window_id"], "name": w["name"], "regime": w["regime"],
            "trades": m["total_trades"], "win_rate": m["win_rate_percent"],
            "roi": m["net_roi_percent"], "max_dd": m["max_dd_percent"],
            "adverse_dd": m["adverse_bound_max_dd_percent"],
            "profit_factor": m["profit_factor"], "avg_r": m["average_r"],
            "verdict": m["verdict"], "circuit": m["circuit_tripped"],
            "checks": m["checks"],
        })
        if verbose:
            print(f"W{w['window_id']:02d} {w['name'][:34]:<34} trades={m['total_trades']:>3} "
                  f"WR={m['win_rate_percent']:>5.1f}% ROI={m['net_roi_percent']:>+7.2f}% "
                  f"DD={m['max_dd_percent']:>4.2f}% ({m['adverse_bound_max_dd_percent']:>4.2f}%) "
                  f"pf={m['profit_factor'] if m['profit_factor'] is not None else float('nan'):>4.2f} "
                  f"{m['verdict']}")
    summary = {
        "windows_passed": passed, "windows_total": len(rows),
        "total_trades": total_trades, "total_pnl": total_pnl,
        "roi_total_pct": 100.0 * total_pnl / cfg.capital,
        "config": cfg.__dict__,
        "rows": rows,
    }
    if verbose:
        print(f"\nSCORECARD: passed {passed}/{len(rows)} | trades {total_trades} | "
              f"PnL {total_pnl:+.2f} USD ({100.0*total_pnl/cfg.capital:+.2f}%)")
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALTCOINS))
    ap.add_argument("--group", default="level_break,confluence,poc,level_sweep")
    ap.add_argument("--families", default=None, help="comma-separated family names to keep")
    ap.add_argument("--macro-filter", action="store_true")
    ap.add_argument("--target-r", type=float, default=4.0)
    ap.add_argument("--max-hold", type=int, default=288)
    ap.add_argument("--risk-usd", type=float, default=50.0)
    ap.add_argument("--risk-mode", default="flat")
    ap.add_argument("--max-positions", type=int, default=3)
    ap.add_argument("--cost-profile", default="certified")
    ap.add_argument("--out", default="lpl_portfolio")
    ap.add_argument("--first-window", type=int, default=1)
    args = ap.parse_args()

    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    data = load_all(list(dict.fromkeys([BTC] + syms)))
    specs = default_specs(args.group.split(",") if args.group else None)
    if args.families:
        keep = {x.strip() for x in args.families.split(",")}
        specs = [s for s in specs if s.name in keep]
        print(f"families kept: {[s.name for s in specs]}")
    wins = [w for w in windows() if w["window_id"] >= args.first_window]
    cfg = LabConfig(base_risk_usd=args.risk_usd, risk_mode=args.risk_mode,
                    target_r=args.target_r, max_hold_bars=args.max_hold,
                    max_positions=args.max_positions, cost_profile=args.cost_profile)
    pre = make_macro_filter(data) if args.macro_filter else None
    summary = score_windows(data, specs, cfg, wins, pre=pre)
    SCORE_DIR.mkdir(exist_ok=True)
    (SCORE_DIR / f"{args.out}.json").write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")
    print(f"wrote {SCORE_DIR / (args.out + '.json')}")


if __name__ == "__main__":
    main()
