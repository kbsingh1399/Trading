"""Gate screen: model family x feature set, measured the way the mission scores.

For each OOS window this trains a candidate gate only on events that ended before
``window_start - 72h`` and reports the realised mean net R (and win rate, and
P(>= 2R)) of the top-k candidates it would have selected in that window.  That is
the quantity the scorecard ultimately rewards, and it is measurable far more
cheaply than a full portfolio run, so it is the right place to compare:

* gate kinds -- ``lgb`` (current), ``deep`` (deeper LightGBM), ``ens`` (LightGBM +
  ExtraTrees + histogram GBM + a small MLP, probability-averaged);
* feature sets -- ``base`` (geometry / POC / regime / positioning / flow / macro)
  and ``ctx`` (base + market context: BTC distance to its own ATH, market breadth,
  the symbol's return relative to the panel, hour of day).

Run: ``python -m Engine.levels_poc_lab.gate_screen --windows 7,11,14,17,18``
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from . import PURGE_MS
from .data import BTC, MKT_COLUMNS, attach_market_context, load_all, windows, window_bounds
from .ml_gate import FEATURE_COLUMNS, event_table, train_gate
from .run_ml import _auc
from . import signals as _signals
from .signals import default_specs

DEFAULT_SYMBOLS = ["ETHUSDT", "SOLUSDT", "DOGEUSDT", "LINKUSDT", "ADAUSDT", "XRPUSDT",
                   "BNBUSDT", "AVAXUSDT"]
ALIGNED_POOL = ["brk_ath", "x_ath_brk_lowvol", "brk_pmh", "brk_pml", "brk_multi_lvl"]


def build_events(symbols: list[str], stop_scale: float, pending: int,
                 pool: list[str], with_ctx: bool):
    import Engine.levels_poc_lab.ml_gate as mg

    data = load_all([BTC] + [s for s in symbols if s != BTC])
    if with_ctx:
        attach_market_context(data)
    _signals.ATR_STOP_SCALE = float(stop_scale)
    mg.FEATURE_COLUMNS = FEATURE_COLUMNS + (MKT_COLUMNS if with_ctx else [])
    specs = [s for s in default_specs() if s.name in pool]
    evs = []
    for sym, f in data.items():
        if sym == BTC:
            continue
        ev = event_table(f, specs, data[BTC], target_r=4.0, horizon=288,
                         pending=pending, pending_step=4)
        if len(ev):
            evs.append(ev)
    return pd.concat(evs, ignore_index=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(DEFAULT_SYMBOLS))
    ap.add_argument("--windows", default="7,11,14,17,18")
    ap.add_argument("--kinds", default="lgb,deep,ens")
    ap.add_argument("--features", default="base,ctx")
    ap.add_argument("--ks", default="25,40,60")
    ap.add_argument("--stop-scale", type=float, default=9.0)
    ap.add_argument("--pending", type=int, default=24)
    ap.add_argument("--pool", default=",".join(ALIGNED_POOL))
    ap.add_argument("--out", default="gate_screen.csv")
    a = ap.parse_args()

    syms = [s.strip() for s in a.symbols.split(",") if s.strip()]
    wids = [int(x) for x in a.windows.split(",")]
    kinds = [x.strip() for x in a.kinds.split(",") if x.strip()]
    ks = [int(x) for x in a.ks.split(",")]
    pool = [x.strip() for x in a.pool.split(",") if x.strip()]
    wins = {w["window_id"]: w for w in windows()}

    ev_cache = {}
    for feats in [x.strip() for x in a.features.split(",") if x.strip()]:
        ev_cache[feats] = build_events(syms, a.stop_scale, a.pending, pool,
                                       with_ctx=(feats == "ctx"))
    print(f"events: " + ", ".join(f"{k}={len(v):,}" for k, v in ev_cache.items()), flush=True)

    rows = []
    for window_id in wids:
        start_ms, end_ms = window_bounds(wins[window_id])
        cutoff = start_ms - PURGE_MS
        for feats, ev in ev_cache.items():
            cols = [c for c in FEATURE_COLUMNS + (MKT_COLUMNS if feats == "ctx" else [])
                    if c in ev.columns]
            tr = ev[ev.t < cutoff]
            te = ev[(ev.t >= start_ms) & (ev.t <= end_ms)]
            if len(tr) < 800 or len(te) < 40:
                print(f"W{window_id:02d} {feats}: skipped (train={len(tr)}, test={len(te)})")
                continue
            for kind in kinds:
                gate = train_gate(tr[cols + ["net_r", "label", "t"]], label_r=1.0, kind=kind)
                p = gate.predict(te[cols])
                order = np.argsort(-p)
                auc = _auc(te.label.to_numpy(), p)
                for k in ks:
                    sel = te.iloc[order[:k]]
                    rows.append({"window": window_id, "features": feats, "kind": kind, "k": k,
                                 "n_test": len(te), "auc": auc,
                                 "meanR": float(sel.net_r.mean()),
                                 "wr": float((sel.net_r > 0).mean()),
                                 "big": float((sel.net_r >= 2).mean()),
                                 "meanR_all": float(te.net_r.mean())})
                best = max(rows[-len(ks):], key=lambda r: r["meanR"])
                print(f"W{window_id:02d} {feats:<4} {kind:<5} AUC={auc:.3f} "
                      f"pool={te.net_r.mean():+.3f} | " +
                      " ".join(f"k{k}={r['meanR']:+.3f}" for k, r in
                               zip(ks, rows[-len(ks):])), flush=True)
    df = pd.DataFrame(rows)
    out = Path("scratch")
    out.mkdir(exist_ok=True)
    df.to_csv(out / a.out, index=False)
    print("\n--- mean net R of top-k, averaged over windows ---")
    piv = df.pivot_table(index=["features", "kind"], columns="k", values="meanR").round(3)
    print(piv.to_string())
    print("\n--- win rate of top-k ---")
    print(df.pivot_table(index=["features", "kind"], columns="k", values="wr").round(3).to_string())
    print("\n--- P(net R >= 2R) of top-k ---")
    print(df.pivot_table(index=["features", "kind"], columns="k", values="big").round(3).to_string())
    print("\n--- per-window top-k mean R (k=40) ---")
    print(df[df.k == 40].pivot_table(index="window", columns=["features", "kind"],
                                     values="meanR").round(3).to_string())


if __name__ == "__main__":
    main()
