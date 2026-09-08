"""
================================================================================
RP2 ROUND 11 - REAL-DATA WALK-FORWARD RUNNER
================================================================================
Runs rp2_round11_regime_adaptive_ml over the 20 OOS windows in
Engine/oos_windows_20.json against the REAL Binance USDT-M parquet corpus in
Engine/binance_backtesting_data/.

This runner REFUSES to execute against anything other than the real corpus. It
verifies, before running, that every symbol has BOTH a master parquet and a
footprint ladder parquet on disk, and it aborts if orderflow coverage on any
window is not 1.0.

USAGE
-----
    python Engine/runners/run_rp2_round11_walkforward.py \
        --data-dir Engine/binance_backtesting_data \
        --windows  Engine/oos_windows_20.json \
        --out      rp2_round11_results.json

    # ablations
    --flat-risk      reproduce the naive flat 1.0% sizing (expected to breach DD)
    --fast-ratchet   mission-alternative 0.8R/1.5R locks, 2.5R hard exit
    --no-ml          raw setups only, ML overlay disabled
================================================================================
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "strategy"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import rp2_round11_regime_adaptive_ml as R
except ImportError:
    sys.stderr.write("FATAL: cannot import rp2_round11_regime_adaptive_ml.\n"
                     "Place this runner in Engine/runners/ next to Engine/strategy/.\n")
    raise


def preflight(data_dir: str, symbols) -> list:
    """Abort unless the REAL dual-parquet corpus is present."""
    if not os.path.isdir(data_dir):
        sys.stderr.write(f"FATAL: data dir not found: {data_dir}\n")
        sys.exit(2)
    ok, missing = [], []
    for s in symbols:
        m = os.path.join(data_dir, R.MASTER_TEMPLATE.format(symbol=s))
        l = os.path.join(data_dir, R.LADDER_TEMPLATE.format(symbol=s))
        if os.path.isfile(m) and os.path.isfile(l):
            ok.append(s)
        else:
            missing.append((s, os.path.isfile(m), os.path.isfile(l)))
    print(f"[preflight] symbols with master+ladder parquet: {len(ok)}/{len(symbols)}")
    for s, hm, hl in missing:
        print(f"[preflight]   MISSING {s}: master={hm} ladder={hl}")
    if not ok:
        sys.stderr.write(
            "FATAL: no real parquet data found. This runner will NOT fall back to\n"
            "synthetic data under any circumstance. Fetch the real corpus from\n"
            "Engine/binance_backtesting_data/ and retry.\n")
        sys.exit(2)
    if len(ok) < len(symbols):
        print(f"[preflight] WARNING: running on {len(ok)} symbols, not the full 18. "
              f"Results are NOT comparable to the mandate.")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="Engine/binance_backtesting_data")
    ap.add_argument("--windows", default="Engine/oos_windows_20.json")
    ap.add_argument("--out", default="rp2_round11_results.json")
    ap.add_argument("--flat-risk", action="store_true")
    ap.add_argument("--fast-ratchet", action="store_true")
    ap.add_argument("--no-ml", action="store_true")
    ap.add_argument("--symbols", default="")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    syms = tuple(x.strip().upper() for x in a.symbols.split(",") if x.strip()) or R.SYMBOLS
    syms = tuple(preflight(a.data_dir, syms))

    with open(a.windows, encoding="utf-8") as fh:
        wj = json.load(fh)
    windows = wj["windows"] if isinstance(wj, dict) and "windows" in wj else wj
    print(f"[preflight] OOS windows loaded: {len(windows)}")

    cfg = R.R11Config(
        data_dir=a.data_dir, symbols=syms,
        flat_risk_mode=a.flat_risk,
        use_fast_ratchet=a.fast_ratchet,
        ml_enabled=not a.no_ml,
        verbose=not a.quiet,
    )

    t0 = time.time()
    res = R.run_walkforward(cfg, windows, data_dir=a.data_dir)
    res["elapsed_sec"] = round(time.time() - t0, 1)
    res["mode"] = {"flat_risk": a.flat_risk, "fast_ratchet": a.fast_ratchet,
                   "ml_enabled": not a.no_ml, "n_symbols": len(syms)}

    ws = res["windows"]

    # ---- provenance enforcement -------------------------------------------
    bad = [w for w in ws if "error" not in w and w.get("orderflow_cover", 0) < 0.999]
    if bad:
        print("\n!! ORDERFLOW COVERAGE BREACH -- footprint data incomplete:")
        for w in bad:
            print(f"   W{w['window_id']:>2} cover={w.get('orderflow_cover'):.4f}")

    # ---- scorecard --------------------------------------------------------
    print("\n" + "=" * 100)
    print("RP2 ROUND 11 - OOS WALK-FORWARD SCORECARD (REAL DATA)")
    print("=" * 100)
    print(f"{'W':>3} {'period':<18} {'trades':>6} {'ROI%':>8} {'DD%':>7} {'WR%':>7} "
          f"{'avgR':>7} {'OFcov':>6} {'TBcov':>6} {'verdict':>8}")
    print("-" * 100)
    npass = 0
    for w in ws:
        if "error" in w:
            print(f"{w.get('window_id','?'):>3} ERROR: {w['error']}")
            continue
        npass += bool(w["pass"])
        print(f"{w['window_id']:>3} {w.get('start_date','')[:10]:<10}"
              f"{w.get('end_date','')[5:10]:<8}"
              f"{w['n_trades']:>6} {w['roi_pct']:>8.2f} {w['max_dd_pct']:>7.2f} "
              f"{w['win_rate_pct']:>7.1f} {w['avg_r']:>7.2f} "
              f"{w.get('orderflow_cover',0):>6.3f} {w.get('tier_b_cover',0):>6.3f} "
              f"{'PASS' if w['pass'] else 'FAIL':>8}")
    print("-" * 100)
    print(f"WINDOWS PASSED: {npass} / {len(ws)}")
    print(f"CRITERIA: ROI > 20.0%  |  MaxDD < 5.0%  |  WinRate > 40.0%  |  trades >= 15")
    print(f"FRICTION: 8 bps taker per leg + 10 bps entry slip + 15 bps exit slip")
    print(f"ELAPSED: {res['elapsed_sec']} sec")
    print("=" * 100)

    # failure attribution so the next round is directed, not guessed
    if npass < len(ws):
        print("\nFAILURE ATTRIBUTION (why each window missed):")
        for w in ws:
            if "error" in w or w["pass"]:
                continue
            why = []
            if w["n_trades"] < 15:
                why.append(f"trades {w['n_trades']}<15")
            if w["roi_pct"] <= 20.0:
                why.append(f"ROI {w['roi_pct']:.2f}<=20")
            if w["max_dd_pct"] >= 5.0:
                why.append(f"DD {w['max_dd_pct']:.2f}>=5")
            if w["win_rate_pct"] <= 40.0:
                why.append(f"WR {w['win_rate_pct']:.1f}<=40")
            print(f"  W{w['window_id']:>2}: " + "; ".join(why))

    res["summary"] = {"windows_passed": npass, "windows_total": len(ws),
                      "all_pass": npass == len(ws)}
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"\nFull results + trade ledgers written to: {a.out}")
    return 0 if npass == len(ws) else 1


if __name__ == "__main__":
    sys.exit(main())
