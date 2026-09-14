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
from collections import Counter
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from . import PURGE_MS
from .data import ALTCOINS, BTC, attach_cross_section, load_all, windows, window_bounds
from .kernel import LabConfig, prepare_execution_frame, simulate
from .ml_gate import FEATURE_COLUMNS, event_table, train_gate
from . import signals as _signals
from .signals import build_signal_frame, default_specs, naked_poc_series

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORE_DIR = REPO_ROOT / "scratch"


# Sleeve membership for the regime switch.  Momentum/breakout families are the
# level-break family (previous week/month high-low, ATH, multi-level, value-area
# break); reversion families are the liquidity-sweep / Point-of-Control reversion
# family that has to carry the chop quarters, where breakout count collapses and
# the book currently bleeds (see REPORT.md sections 4.1c/4.4).
MOMENTUM_FAMILIES = ("brk_pwh", "brk_pwl", "brk_pmh", "brk_pml", "brk_ath", "brk_pdh",
                     "brk_pdl", "brk_pwh_cascade", "brk_pwh_retest", "brk_multi_lvl",
                     "x_brk_pwh_out_of_value", "x_ath_brk_lowvol",
                     "poc_value_break_up", "poc_value_break_dn",
                     "poc_migration", "poc_migration_dn", "poc_naked_up", "poc_naked_dn")
REVERSION_FAMILIES = ("swp_pwh", "swp_pwl", "swp_pmh", "swp_pml", "swp_pdh", "swp_pdl",
                      "swp_ath", "x_pwh_sweep_at_poc", "x_pwl_sweep_at_poc",
                      "poc_prior_reject_up", "poc_prior_reject_dn", "poc_prior_reclaim_up",
                      "poc_reclaim_up", "poc_reclaim_dn", "poc_rotate_from_lvn", "poc_magnet")


def build_all(data: dict, specs, target_r: float, horizon: int,
              pending: int = 0, pending_step: int = 4):
    # NOTE: cross-sectional panel features are deliberately NOT attached here: they
    # were measured to hurt out-of-sample ranking (scratch/pos_check.csv) and they
    # cost ~120 MB across the panel.  `data.attach_cross_section` is kept for the
    # record.  Symbol frames are released as soon as their signals/events exist so
    # the full 18-symbol panel fits in memory.
    signals = {}
    events = []
    for sym in list(data):
        f = data[sym]
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
        del data[sym]          # free the wide feature frame; signals carry what the kernel needs
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
    ap.add_argument("--families", default=None,
                    help="comma-separated family names (overrides --group)")
    ap.add_argument("--target-r", type=float, default=4.0)
    ap.add_argument("--horizon", type=int, default=288)
    ap.add_argument("--max-hold", type=int, default=288)
    ap.add_argument("--cands-per-month", type=float, default=30.0)
    ap.add_argument("--risk-usd", type=float, default=50.0)
    ap.add_argument("--risk-mode", default="flat")

    ap.add_argument("--min-train-events", type=int, default=3000)
    ap.add_argument("--min-prob", type=float, default=0.30)
    ap.add_argument("--label-r", type=float, default=None,
                    help="gate label: P(net_r > label_r) instead of P(net_r > 0)")
    ap.add_argument("--regressor", action="store_true",
                    help="rank candidates by predicted expected net R")
    ap.add_argument("--stop-scale", type=float, default=None,
                    help="use the certified pure-ATR stop max(k*ATR, 1.2%% of price)")
    ap.add_argument("--pending", type=int, default=0,
                    help="bars a break stays actionable after the breakout")
    ap.add_argument("--pending-step", type=int, default=4)
    ap.add_argument("--sel-per-window", type=int, default=0,
                    help="select the top-N scoring candidates per window (0=threshold)")
    ap.add_argument("--max-positions", type=int, default=3,
                    help="concurrent positions (criteria file caps nothing; suite reference asserts 2-3)")
    ap.add_argument("--risk-frac", type=float, default=0.04,
                    help="max total open risk as a fraction of capital")
    ap.add_argument("--wf-select", type=int, default=0,
                    help="walk-forward: trade only the N families with the best "
                         "realised net R over the trailing --wf-lookback-days window "
                         "(outcomes resolved before the window starts; causal)")
    ap.add_argument("--wf-lookback-days", type=float, default=180.0)
    ap.add_argument("--wf-min-events", type=int, default=300,
                    help="minimum trailing events for a family to be rankable")
    ap.add_argument("--wf-exclude-neg", type=float, default=None, metavar="MARGIN",
                    help="walk-forward: drop families whose trailing mean net R is "
                         "below MARGIN (e.g. 0.0 keeps only non-negative families)")
    ap.add_argument("--cusum-filter", type=int, default=0,
                    help="require a CUSUM structural-move event within N bars in the trade direction")
    ap.add_argument("--reserve", action="store_true",
                    help="reserve scarce slots for top-ranked candidates: required score "
                         "decays from a high quantile to the gate threshold across the window")
    ap.add_argument("--reserve-q", type=float, default=0.999)
    ap.add_argument("--cost-profile", default="certified")
    ap.add_argument("--macro-filter", action="store_true")
    ap.add_argument("--ride-winners", action="store_true")
    ap.add_argument("--vwap-trail", action="store_true")
    ap.add_argument("--trail-after-r", type=float, default=2.0)
    ap.add_argument("--sleeve-regime", action="store_true",
                    help="regime switch: trade the reversion sleeve when the universe "
                         "ATR%% z-score is below --dormancy-z (dormant/chop), the "
                         "breakout sleeve otherwise (with the tide veto on breakouts)")
    ap.add_argument("--dormancy-z", type=float, default=-1.0)
    ap.add_argument("--decay-bars", type=int, default=0,
                    help="certified time-decay exit: close a position that has not "
                         "reached --decay-min-r net after this many bars")
    ap.add_argument("--decay-min-r", type=float, default=0.2)
    ap.add_argument("--out", default="lpl_ml")
    args = ap.parse_args()

    if args.stop_scale:
        _signals.ATR_STOP_SCALE = float(args.stop_scale)
        print(f"stop geometry: certified pure-ATR, stop = max({args.stop_scale}*ATR, 1.2% of price)")
    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    data = load_all(list(dict.fromkeys([BTC] + syms)))
    specs = default_specs(args.group.split(",") if args.group else None)
    if args.families:
        keep = {x.strip() for x in args.families.split(",") if x.strip()}
        specs = [s for s in specs if s.name in keep]
        print(f"family pool: {[s.name for s in specs]}")
    print(f"building candidate events for {len(syms)} symbols ...")
    signals, ev_all = build_all(data, specs, args.target_r, args.horizon,
                                pending=args.pending, pending_step=args.pending_step)
    print(f"candidates: {len(ev_all):,} (base win rate {ev_all.label.mean():.3f})")

    wins = windows()
    cfg = LabConfig(base_risk_usd=args.risk_usd, risk_mode=args.risk_mode,
                    max_concurrent_risk_frac=args.risk_frac,
                    target_r=args.target_r, max_hold_bars=args.max_hold,
                    max_positions=args.max_positions, cost_profile=args.cost_profile,
                    ride_winners=args.ride_winners, vwap_trail=args.vwap_trail,
                    trail_after_r=args.trail_after_r,
                    decay_bars=args.decay_bars, decay_min_r=args.decay_min_r)
    rows = []
    passed = total_trades = 0
    cf_passed = 0
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
        is_mom = None
        if args.sleeve_regime:
            fam_v = test.family.to_numpy()
            is_mom = np.isin(fam_v, MOMENTUM_FAMILIES)
            is_rev = np.isin(fam_v, REVERSION_FAMILIES)
            if "mkt_atr_pct_z" not in test.columns:
                raise SystemExit("--sleeve-regime needs the mkt_atr_pct_z feature; "
                                 "rebuild the feature cache (Engine/levels_poc_lab/bootstrap.sh)")
            z_univ = test.mkt_atr_pct_z.to_numpy(float)
            dormant = z_univ < args.dormancy_z
            sel = sel & ((dormant & is_rev) | (~dormant & is_mom))
        if args.macro_filter:
            side_v = test.side.to_numpy()
            tide_v = test.btc_tide.to_numpy()
            agree = ((side_v > 0) & (tide_v > 0)) | ((side_v < 0) & (tide_v < 0))
            if args.sleeve_regime:
                # The macro tide is a directional veto for breakouts; the reversion
                # sleeve exists precisely for the quarters where that tide is absent
                # or flipping, so it is not vetoed by it.
                sel = sel & (agree | ~is_mom)
            else:
                sel = sel & agree
        if args.cusum_filter and "cs_up_age" in test.columns:
            n_bars = args.cusum_filter
            side_v = test.side.to_numpy()
            up = test.cs_up_age.to_numpy(float) <= n_bars
            dn = test.cs_dn_age.to_numpy(float) <= n_bars
            sel = sel & np.where(side_v > 0, up, dn)
        # Count-based selection is applied *after* every eligibility filter, so the
        # N best eligible candidates are kept (ranking the raw pool first would
        # discard a window's entire eligible set, e.g. when the tide filter is on).
        if args.sel_per_window > 0:
            elig = np.flatnonzero(sel)
            if len(elig) > args.sel_per_window:
                keep = elig[np.argsort(-prob[elig])[: args.sel_per_window]]
                sel = np.zeros(len(prob), bool)
                sel[keep] = True
        wf_kept = None
        if args.wf_select > 0 or args.wf_exclude_neg is not None:
            # Causal meta-allocation across pre-registered families: rank by realised
            # net R over the trailing lookback, using only events whose full barrier
            # window resolved before this window opens (t < train_cut, i.e. purge).
            lb = int(args.wf_lookback_days * 86_400_000)
            hist = ev_all[(ev_all.t >= start_ms - lb) & (ev_all.t < train_cut)]
            stats = hist.groupby("family").net_r.agg(["size", "mean"])
            stats = stats[stats["size"] >= args.wf_min_events].sort_values("mean", ascending=False)
            if args.wf_select > 0:
                keep_fams = list(stats.index[: args.wf_select])
            else:
                keep_fams = list(stats[stats["mean"] > args.wf_exclude_neg].index)
            sel = sel & test.family.isin(keep_fams).to_numpy()
            wf_kept = {f: round(float(stats.loc[f, "mean"]), 3) for f in keep_fams}
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
        cfg_w = cfg
        if args.reserve:
            p_tr = gate.predict(train)
            hi = float(np.quantile(p_tr, args.reserve_q))
            lo = float(gate.threshold)
            if hi > lo:
                cfg_w = replace(cfg, reserve=True, reserve_hi=hi, reserve_lo=lo)
        res = simulate(per_symbol, start_ms, end_ms, cfg_w)
        m = res["metrics"]
        # Criteria-file faithfulness: Engine/target_oos_criteria.json requires
        # min_r_multiple 4.0, which the certification protocol defines as the
        # *planned* target ("minimum planned target net4R; achieved average R
        # reported separately"), so the binding test is target_r >= 4.0 -- a
        # configuration property, not a realised-trade property.  The realised
        # best R is still reported for transparency.
        tr_w = res["trades"]
        best_r = max((t["net_r"] for t in tr_w), default=0.0)
        win_rs = sorted((t["net_r"] for t in tr_w if t["net_r"] > 0), reverse=True)
        reasons = Counter(t["exit_reason"] for t in tr_w)
        cf_pass = (m["net_roi_percent"] >= 10.0 and m["max_dd_percent"] <= 5.0
                   and m["win_rate_percent"] >= 40.0 and m["total_trades"] >= 15
                   and cfg.target_r >= 4.0)
        cf_passed += int(cf_pass)
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
            "best_r": float(best_r), "top3_r": [float(x) for x in win_rs[:3]],
            "exit_reasons": dict(reasons), "cf_pass": bool(cf_pass),
            "circuit_tripped": bool(m.get("circuit_tripped", False)),
            "max_concurrent": int(m.get("max_concurrent_positions", 0)),
            "avg_winner_r": m.get("average_winner_r"),
            "long_share": (None if not m.get("long") else m["long"].get("trades", 0)),
            "first_trade_roi_hint": None,
            "wf_families": wf_kept,
        })
        if wf_kept is not None:
            print(f"      walk-forward families: {wf_kept}")
        print(f"W{w['window_id']:02d} {w['name'][:32]:<32} cand={int(sel.sum()):>4}/{len(test):>5} "
              f"AUC={auc if auc is None else round(auc,3)} trades={m['total_trades']:>3} "
              f"WR={m['win_rate_percent']:>5.1f}% ROI={m['net_roi_percent']:>+7.2f}% "
              f"DD={m['max_dd_percent']:>4.2f}% pf={m['profit_factor'] if m['profit_factor'] is None else round(m['profit_factor'],2)} "
              f"bestR={best_r:>5.2f} {'CF-PASS' if cf_pass else m['verdict']}")

    summary = {"windows_passed": passed, "cf_windows_passed": cf_passed,
               "windows_total": len(rows),
               "total_trades": total_trades, "total_pnl": total_pnl,
               "roi_total_pct": 100.0 * total_pnl / cfg.capital,
               "config": {**cfg.__dict__, "cands_per_month": args.cands_per_month,
                          "target_r": args.target_r, "horizon": args.horizon,
                          "label_r": args.label_r, "regressor": args.regressor,
                          "pending": args.pending, "stop_scale": args.stop_scale,
                          "sel_per_window": args.sel_per_window,
                          "families": args.families,
                          "max_positions": args.max_positions,
                          "risk_frac": args.risk_frac, "cusum_filter": args.cusum_filter,
                          "wf_select": args.wf_select, "wf_lookback_days": args.wf_lookback_days,
                          "wf_exclude_neg": args.wf_exclude_neg,
                          "wf_min_events": args.wf_min_events,
                          "decay_bars": args.decay_bars,
                          "sleeve_regime": args.sleeve_regime,
                          "dormancy_z": args.dormancy_z,
                          "decay_min_r": args.decay_min_r},
               "rows": rows}
    SCORE_DIR.mkdir(exist_ok=True)
    (SCORE_DIR / f"{args.out}.json").write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")
    print(f"\nSCORECARD (ML gate): passed {passed}/{len(rows)} | trades {total_trades} | "
          f"PnL {total_pnl:+,.2f} USD ({100.0*total_pnl/cfg.capital:+.2f}%)")


if __name__ == "__main__":
    main()
