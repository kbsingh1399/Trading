"""Walk-forward ML-gated scorecard.

Pipeline per OOS window:

1. build every geometric candidate event (one per symbol/bar, family-resolved);
2. train a LightGBM meta-labeller on events that **ended before**
   ``window_start - 72h`` (all symbols pooled);
3. keep only window candidates whose predicted probability exceeds a threshold
   calibrated on the training set to a target candidate count per month;
4. execute them with the certified kernel, ranked cross-sectionally by probability.

The reported AUC is on the window (out-of-sample), so it is an honest measure of
whether the gate generalises.
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
from .ml_gate import FEATURE_COLUMNS, event_table, train_gate
from .signals import build_signal_frame, default_specs, naked_poc_series

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORE_DIR = REPO_ROOT / "scratch"


def build_all(data: dict, specs, target_r: float, horizon: int,
              pending: int = 0, pending_step: int = 4):
    signals = {}
    events = []
    for sym, f in data.items():
        if sym == BTC:
            continue
        t = f.open_time_ms.to_numpy(np.int64)
        day = t // 86_400_000
        naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                                 f.high.to_numpy(float), f.close.to_numpy(float))
        sig = prepare_execution_frame(f, build_signal_frame(
            f, specs, naked=naked, pending=pending, pending_step=pending_step))
        signals[sym] = sig
        ev = event_table(f, specs, data[BTC], target_r=target_r, horizon=horizon,
                        pending=pending, pending_step=pending_step)
        if len(ev):
            events.append(ev)
    ev_all = pd.concat(events, ignore_index=True) if events else pd.DataFrame()
    return signals, ev_all


def _auc(y: np.ndarray, p: np.ndarray) -> float | None:
    y = np.asarray(y)
    if len(np.unique(y)) < 2:
        return None
    order = np.argsort(p)
    ranks = np.empty(len(p), float)
    ranks[order] = np.arange(1, len(p) + 1)
    pos = y == 1
    n1, n0 = pos.sum(), (~pos).sum()
    return float((ranks[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(ALTCOINS))
    ap.add_argument("--group", default=None)
    ap.add_argument("--target-r", type=float, default=4.0)
    ap.add_argument("--horizon", type=int, default=288)
    ap.add_argument("--max-hold", type=int, default=288)
    ap.add_argument("--cands-per-month", type=float, default=30.0)
    ap.add_argument("--risk-usd", type=float, default=50.0)
    ap.add_argument("--risk-mode", default="flat")
    ap.add_argument("--max-positions", type=int, default=3)
    ap.add_argument("--min-train-events", type=int, default=3000)
    ap.add_argument("--min-prob", type=float, default=0.30)
    ap.add_argument("--label-r", type=float, default=None,
                    help="gate label: P(net_r > label_r) instead of P(net_r > 0)")
    ap.add_argument("--regressor", action="store_true",
                    help="rank candidates by predicted expected net R")
    ap.add_argument("--pending", type=int, default=0,
                    help="bars a break stays actionable after the breakout")
    ap.add_argument("--pending-step", type=int, default=4)
    ap.add_argument("--sel-per-window", type=int, default=0,
                    help="select the top-N scoring candidates per window (0=threshold)")
    ap.add_argument("--cost-profile", default="certified")
    ap.add_argument("--macro-filter", action="store_true")
    ap.add_argument("--ride-winners", action="store_true")
    ap.add_argument("--vwap-trail", action="store_true")
    ap.add_argument("--trail-after-r", type=float, default=2.0)
    ap.add_argument("--out", default="lpl_ml")
    args = ap.parse_args()

    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    data = load_all(list(dict.fromkeys([BTC] + syms)))
    specs = default_specs(args.group.split(",") if args.group else None)
    print(f"building candidate events for {len(syms)} symbols ...")
    signals, ev_all = build_all(data, specs, args.target_r, args.horizon,
                                pending=args.pending, pending_step=args.pending_step)
    print(f"candidates: {len(ev_all):,} (base win rate {ev_all.label.mean():.3f})")

    wins = windows()
    cfg = LabConfig(base_risk_usd=args.risk_usd, risk_mode=args.risk_mode,
                    target_r=args.target_r, max_hold_bars=args.max_hold,
                    max_positions=args.max_positions, cost_profile=args.cost_profile,
                    ride_winners=args.ride_winners, vwap_trail=args.vwap_trail,
                    trail_after_r=args.trail_after_r)
    rows = []
    passed = total_trades = 0
    total_pnl = 0.0
    for w in wins:
        start_ms, end_ms = window_bounds(w)
        train_cut = start_ms - PURGE_MS
        train = ev_all[ev_all.t < train_cut]
        test = ev_all[(ev_all.t >= start_ms) & (ev_all.t <= end_ms)]
        if len(train) < args.min_train_events or len(test) == 0:
            print(f"W{w['window_id']:02d} skipped (train={len(train)}, test={len(test)})")
            continue
        gate = train_gate(train, target_cands_per_month=args.cands_per_month,
                          min_prob=args.min_prob, label_r=args.label_r,
                          regressor=args.regressor)
        prob = gate.predict(test)
        sel = prob >= gate.threshold
        if args.macro_filter:
            side_v = test.side.to_numpy()
            tide_v = test.btc_tide.to_numpy()
            agree = ((side_v > 0) & (tide_v > 0)) | ((side_v < 0) & (tide_v < 0))
            sel = sel & agree
        # Count-based selection is applied *after* every eligibility filter, so the
        # N best eligible candidates are kept (ranking the raw pool first would
        # discard a window's entire eligible set, e.g. when the tide filter is on).
        if args.sel_per_window > 0:
            elig = np.flatnonzero(sel)
            if len(elig) > args.sel_per_window:
                keep = elig[np.argsort(-prob[elig])[: args.sel_per_window]]
                sel = np.zeros(len(prob), bool)
                sel[keep] = True
        auc = _auc(test.label.to_numpy(), prob)
        fam_counts = test.loc[sel, "family"].value_counts().to_dict()

        # build the gated execution frames for this window
        per_symbol = {}
        sel_keys = set(zip(test.loc[sel, "symbol"], test.loc[sel, "open_time_ms"]))
        prob_map = {(s, t): p for s, t, p in zip(test.symbol, test.open_time_ms, prob)}
        for sym, sig in signals.items():
            m = (sig.open_time_ms >= start_ms - PURGE_MS) & (sig.open_time_ms <= end_ms)
            sub = sig[m].copy()
            keep = np.array([((sym, int(tt)) in sel_keys) for tt in sub.open_time_ms], dtype=bool)
            sub.loc[~keep, "signal"] = 0
            sub.loc[~keep, "stop_distance"] = np.nan
            sub["score"] = [prob_map.get((sym, int(tt)), 0.0) for tt in sub.open_time_ms]
            per_symbol[sym] = sub
        res = simulate(per_symbol, start_ms, end_ms, cfg)
        m = res["metrics"]
        is_pass = m["verdict"] == "PASS"
        passed += int(is_pass)
        total_trades += m["total_trades"]
        total_pnl += m["net_profit_usd"]
        rows.append({
            "window_id": w["window_id"], "name": w["name"], "trades": m["total_trades"],
            "win_rate": m["win_rate_percent"], "roi": m["net_roi_percent"],
            "max_dd": m["max_dd_percent"], "adverse_dd": m["adverse_bound_max_dd_percent"],
            "profit_factor": m["profit_factor"], "avg_r": m["average_r"],
            "verdict": m["verdict"], "auc": auc, "threshold": gate.threshold,
            "candidates": int(len(test)), "selected": int(sel.sum()),
            "train_events": int(len(train)), "families": fam_counts,
        })
        print(f"W{w['window_id']:02d} {w['name'][:32]:<32} cand={int(sel.sum()):>4}/{len(test):>5} "
              f"AUC={auc if auc is None else round(auc,3)} trades={m['total_trades']:>3} "
              f"WR={m['win_rate_percent']:>5.1f}% ROI={m['net_roi_percent']:>+7.2f}% "
              f"DD={m['max_dd_percent']:>4.2f}% pf={m['profit_factor'] if m['profit_factor'] is None else round(m['profit_factor'],2)} "
              f"{m['verdict']}")

    summary = {"windows_passed": passed, "windows_total": len(rows),
               "total_trades": total_trades, "total_pnl": total_pnl,
               "roi_total_pct": 100.0 * total_pnl / cfg.capital,
               "config": {**cfg.__dict__, "cands_per_month": args.cands_per_month,
                          "target_r": args.target_r, "horizon": args.horizon,
                          "label_r": args.label_r, "regressor": args.regressor,
                          "pending": args.pending,
                          "sel_per_window": args.sel_per_window},
               "rows": rows}
    SCORE_DIR.mkdir(exist_ok=True)
    (SCORE_DIR / f"{args.out}.json").write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")
    print(f"\nSCORECARD (ML gate): passed {passed}/{len(rows)} | trades {total_trades} | "
          f"PnL {total_pnl:+,.2f} USD ({100.0*total_pnl/cfg.capital:+.2f}%)")


if __name__ == "__main__":
    main()
