"""
================================================================================
AUDIT PROBE: METRICS VALIDITY GATE
   catches the two defect classes the year-granular scan structurally cannot see
   (docs/PIPELINE_REREVIEW_ADDENDUM.md, findings A1 and A1b)
================================================================================
Both checks found real, shipped data in
`Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet`, and the file
passes all three council agents with zero findings while carrying them.

  (A1)  IMPOSSIBLE VALUES. `open_interest_k == 0` on a USD-M perpetual is not a
        market state -- BTCUSDT open interest has never been zero. `metrics_available`
        tests *staleness* (age <= 6h), not validity, and `oi_nonneg` accepts 0, so a
        fabricated zero flows through as a fresh observation. `oi_change_pct` is then
        clipped to exactly +-100, which also silences `oi_change_domain`.

  (A1b) FROZEN STALE RANGES. A contiguous run of >= 3 days in which a positioning
        column is bit-identical while `open_interest_k` changes on ~every bar. That
        rules out a market halt, and the value preceding the run differs from the
        frozen value, so it is not an as-of carry-forward either -- it is a stale
        upstream range. The OI-keyed staleness bound cannot see a column that is
        frozen while OI is live, and per-year nunique stays huge, so
        `regime_dead_feature` stays silent too.

Why year granularity is the wrong axis: the canary's minimum per-year nunique is
11,612 for the affected columns, so any constancy test over a calendar year passes by
construction. Only a run-length test over the *whole* series sees a 38-bar or 9,819-bar
hole.

funding_rate_pct is deliberately NOT scanned for frozen runs: Binance's default funding
rate is exactly 0.01 % and legitimately persists for weeks, and 0.01 is also the
missing-data sentinel (`0.0001 * 100`) -- the two are indistinguishable in this column.
Fix that by exporting NaN plus an explicit flag instead of a sentinel.

Usage
  python3 -m Engine.verification.audit_probe_metrics_validity [target_dir] [--symbol S]...
Exit 0 = clean. Exit 1 = unflagged impossible or frozen-stale metrics present.
================================================================================
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

DEFAULT_TARGET = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "binance_backtesting_data"
)
MASTER_SUFFIX = "_15m_master_2020_2026.parquet"

ROLL_WINDOW = 201          # ~2 days of 15m bars, centred, for a robust local OI level
FRAC_OF_LOCAL = 0.20       # below this share of its own local median is not physical
MIN_LOCAL_K = 1.0          # ignore assets whose OI genuinely trades near zero (k units)

# Columns that must not sit bit-identical for days while open interest is moving.
STALE_RUN_COLS = ("ls_ratio_global", "ls_ratio_top", "top_account_ratio",
                  "whale_index", "taker_volume_ratio")
STALE_RUN_BARS = 288       # 3 days of 15m bars
OI_MUST_BE_MOVING = 0.90   # else the whole tape was down and a frozen ratio is expected
QUANT = 8                  # dp used to decide "bit-identical"


def _runs_of_equal_values(values: np.ndarray, threshold: int) -> List[List[int]]:
    """Contiguous runs of >= threshold identical values -> [[start, length], ...]."""
    v = np.round(values.astype(np.float64), QUANT)
    v = np.where(np.isnan(v), np.inf, v)          # NaN runs collapse onto each other
    change = np.flatnonzero(np.diff(v) != 0)
    starts = np.concatenate(([0], change + 1))
    lengths = np.diff(np.concatenate((starts, [len(v)])))
    return [[int(s), int(L)] for s, L in zip(starts, lengths) if L >= threshold]


def check_symbol(master_path: str) -> Optional[Dict]:
    import pyarrow.parquet as pq

    arrow_cols = set(pq.ParquetFile(master_path).schema_arrow.names)
    need = {"open_time_ms", "open_interest_k", "oi_change_pct", "metrics_available",
            "is_imputed_metrics", "open_interest_usd", *STALE_RUN_COLS}
    missing = need - arrow_cols
    if missing:
        print(f"  [skip] {os.path.basename(master_path)}: lacks {sorted(missing)}")
        return None

    m = pd.read_parquet(master_path, columns=sorted(need))
    n = len(m)
    oi = m["open_interest_k"].to_numpy(np.float64)
    avail = m["metrics_available"].to_numpy(np.int8)
    imputed = m["is_imputed_metrics"].to_numpy(np.int8)
    dt = pd.to_datetime(m["open_time_ms"].to_numpy(np.int64), unit="ms", utc=True)

    out: Dict = {"rows": n, "zero": [], "frozen": []}

    # ---- A1: impossible values -------------------------------------------------
    local = pd.Series(oi).rolling(ROLL_WINDOW, center=True, min_periods=50).median().to_numpy()
    suspect = (oi == 0.0) | ((oi < FRAC_OF_LOCAL * local) & (local > MIN_LOCAL_K))
    if suspect.any():
        chg = m["oi_change_pct"].to_numpy(np.float64)
        extreme = np.abs(chg) >= 50.0
        idx = np.flatnonzero(suspect)
        runs = np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1)
        out["zero"] = {
            "bars": int(suspect.sum()),
            "exact_zero": int((oi == 0.0).sum()),
            "episodes": len(runs),
            "longest": max(len(r) for r in runs),
            "unflagged": int((suspect & (imputed == 0)).sum()),
            "marked_available": int((suspect & (avail == 1)).sum()),
            "extreme_total": int(extreme.sum()),
            "extreme_on_suspect": int((extreme & suspect).sum()),
            "span": (str(dt[idx[0]]), str(dt[idx[-1]])),
            "by_year": {int(k): int(v) for k, v in
                        pd.Series(dt[suspect].year).value_counts().sort_index().items()},
        }

    # ---- A1b: frozen stale ranges ---------------------------------------------
    oi_moves = np.diff(oi) != 0
    for col in STALE_RUN_COLS:
        arr = m[col].to_numpy(np.float64)
        for start, length in _runs_of_equal_values(arr, STALE_RUN_BARS):
            moving = float(oi_moves[start:min(start + length, n - 1)].mean()) if n > 1 else 0.0
            if moving < OI_MUST_BE_MOVING:
                continue                      # tape was down: a frozen ratio is legitimate
            out["frozen"].append({
                "col": col, "start": start, "len": length, "value": float(arr[start]),
                "prev": float(arr[start - 1]) if start > 0 else float("nan"),
                "oi_moving": moving,
                "carry_forward": bool(start > 0 and arr[start - 1] == arr[start]),
                "available": int(avail[start:start + length].sum()),
                "imputed": int(imputed[start:start + length].sum()),
                "start_ts": str(dt[start]),
                "end_ts": str(dt[min(start + length - 1, n - 1)]),
            })
    return out


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Reject Parquet exports carrying impossible or silently-frozen metrics.")
    ap.add_argument("target_dir", nargs="?", default=DEFAULT_TARGET)
    ap.add_argument("--symbol", action="append", default=None,
                    help="limit to these symbols (repeatable)")
    ap.add_argument("--max-print", type=int, default=12, help="frozen runs shown per file")
    args = ap.parse_args(argv)

    files = sorted(glob.glob(os.path.join(args.target_dir, f"*{MASTER_SUFFIX}")))
    if args.symbol:
        want = set(args.symbol)
        files = [f for f in files if os.path.basename(f).split("_15m_master")[0] in want]
    if not files:
        print(f"[FAIL] no `{MASTER_SUFFIX}` file under {args.target_dir}")
        return 1

    print("=" * 100)
    print("METRICS VALIDITY GATE -- impossible values (A1) and silently-frozen ranges (A1b)")
    print("=" * 100)
    bad = 0
    for path in files:
        sym = os.path.basename(path).split("_15m_master")[0]
        res = check_symbol(path)
        if res is None:
            continue
        z, fz = res["zero"], res["frozen"]
        unflagged_fz = [f for f in fz if f["available"] > 0 or f["imputed"] < f["len"]]
        if not z and not unflagged_fz:
            q_msg = f", {len(fz)} upstream frozen runs quarantined (metrics_available=0, is_imputed=1)" if fz else ""
            print(f"  [{sym}] PASS -- {res['rows']:,} rows, no impossible or unflagged frozen metrics{q_msg}")
            if fz:
                mask = np.zeros(res["rows"], bool)
                for f in fz:
                    mask[f["start"]:f["start"] + f["len"]] = True
                tot = int(mask.sum())
                print(f"        quarantined upstream stale positioning: {len(fz)} runs, {tot:,} unique bars ({100.0 * tot / res['rows']:.2f}% of file)")
            continue
        bad += 1
        print(f"  [{sym}] ** REJECT ** {res['rows']:,} rows")

        if z:
            print(f"    A1  impossible open interest: {z['bars']:,} bars "
                  f"({z['exact_zero']:,} exactly 0.0, "
                  f"{z['bars'] - z['exact_zero']:,} below {FRAC_OF_LOCAL:.0%} of local median)")
            print(f"        is_imputed_metrics marks only {z['bars'] - z['unflagged']:,} of them; "
                  f"{z['unflagged']:,} pass as fresh ({z['marked_available']:,} with metrics_available=1)")
            print(f"        {z['episodes']:,} episodes, longest {z['longest']:,} bars, "
                  f"{z['span'][0]} .. {z['span'][1]}")
            print(f"        by year: {z['by_year']}")
            if z["extreme_total"]:
                share = 100.0 * z["extreme_on_suspect"] / z["extreme_total"]
                print(f"        derived contamination: {z['extreme_on_suspect']:,}/{z['extreme_total']:,} "
                      f"bars with |oi_change_pct| >= 50% sit on impossible-OI rows ({share:.1f}% of the "
                      f"file's largest OI events are artifacts)")

        if unflagged_fz:
            # Report the UNION of affected unflagged bars
            mask = np.zeros(res["rows"], bool)
            for f in unflagged_fz:
                mask[f["start"]:f["start"] + f["len"]] = True
            tot = int(mask.sum())
            per_col: Dict[str, int] = {}
            for f in unflagged_fz:
                per_col[f["col"]] = per_col.get(f["col"], 0) + f["len"]
            episodes = int((np.diff(mask.astype(np.int8)) == 1).sum() + (1 if mask[0] else 0))
            print(f"    A1b silently-frozen ranges (>= {STALE_RUN_BARS} bars with OI moving "
                  f">= {OI_MUST_BE_MOVING:.0%}): {len(unflagged_fz)} unflagged column-runs over {episodes} distinct "
                  f"episode(s), {tot:,} unique bars ({100.0 * tot / res['rows']:.2f}% of the file)")
            print(f"        per column (bars, before de-duplication): "
                  + ", ".join(f"{k}={v:,}" for k, v in
                              sorted(per_col.items(), key=lambda x: -x[1])))
            for f in sorted(unflagged_fz, key=lambda x: -x["len"])[: args.max_print]:
                origin = ("carry-forward" if f["carry_forward"] else "UPSTREAM STALE (not a fill)")
                print(f"        {f['col']:20} {f['len']:>6,} bars {f['start_ts'][:16]} -> "
                      f"{f['end_ts'][:16]} value={f['value']:.6f}")
                print(f"        {'':20} OI moved on {f['oi_moving']:.1%} of bars, "
                  f"prev={f['prev']:.6f} -> {origin}; "
                  f"metrics_available=1 on {f['available']:,}, is_imputed=1 on {f['imputed']:,}")
            if len(unflagged_fz) > args.max_print:
                print(f"        ... {len(unflagged_fz) - args.max_print} further runs")

    print("=" * 100)
    if bad:
        print(f"VERDICT: {bad} file(s) fail the metrics validity gate.")
        print("Root cause of A1 is in fetch_metrics, where a missing primary OI is coerced to a literal")
        print("0.0 before the processor can mark it unavailable:")
        print("    primary['sum_open_interest'].fillna(0.0) + primary['_oi_usdc'].fillna(0.0)")
        print("Use `.add(other, fill_value=0.0)` (NaN+NaN stays NaN) and bound the merge to post-floor rows.")
        print("Then gate validity, not just freshness:")
        print("    available = (~np.isnan(oi_coin)) & (oi_coin > 0) & (oi_age <= METRICS_MAX_STALENESS_MS)")
        print("A1b additionally requires per-column staleness: key is_imputed_metrics on each imputation")
        print("site, not on the single OI-derived metrics_available bit.")
        return 1
    print("VERDICT: all files pass the metrics validity gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
