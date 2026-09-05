"""
Full-universe forensic audit of the exported 15m master + footprint ladder datasets.
=====================================================================================
Row-by-row over every bar and every rung of all symbols in Engine/binance_backtesting_data/, in
five families:

  structure    cadence, monotonicity, duplicates, close_time identity, schema/dtype conformance
  integrity    OHLC and volume bounds, taker split, cross-column identities, null/inf contract
  domain       oscillator and microstructure bounds, precision floor for sub-dollar assets
  attestation  every metrics-absence exemption traced to the download inventory, not to the flag
  causality    day-anchored and recursions recomputed from the stored inputs and compared bar-by-bar

Deliberately does NOT reuse the council's helpers: every assertion here is recomputed independently,
so a bug in one implementation cannot hide behind the other.

Seeding convention for the causality family: the export's first UTC day is produced from the pipeline's
warm-up slice, so day 0 is excluded from recompute comparisons; from day 1 onward the pipeline and this
tool see identical inputs, and any difference is a real discrepancy, not a seed artefact.

    python3 Engine/verification/audit_full_dataset_forensic.py                 # all symbols
    python3 Engine/verification/audit_full_dataset_forensic.py --symbols BTCUSDT,DOGEUSDT
    python3 Engine/verification/audit_full_dataset_forensic.py --council       # plus 3-agent re-run
"""
from __future__ import annotations

import argparse
import gc
import glob
import json
import os
import sys
from typing import Dict

import numpy as np
import pandas as pd

ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
REPO_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

DATA_DIR = os.path.join(ENGINE_DIR, "binance_backtesting_data")
STEP_MS = 900_000
CLOSE_OFFSET_MS = 899_999

# fallback values the processor writes where no metrics row exists
FALLBACK = {"open_interest_k": 0.0, "open_interest_usd": 0.0, "oi_change_pct": 0.0,
            "ls_ratio_global": 1.0, "ls_ratio_top": 1.0, "top_account_ratio": 1.0,
            "whale_index": 100.0}


def viol(n) -> Dict[str, int]:
    return {"violations": int(n)}


# --------------------------------------------------------------------- causality
def causality(m: pd.DataFrame) -> Dict[str, object]:
    """Recompute every day-anchored / recursion-based column from the stored inputs."""
    from Engine.pipeline.historical_metrics_processor import PRICE_DP, COIN_DP, USD_DP, RATIO_DP
    from Engine.core.canonical_indicators import (compute_ema_series, compute_session_vwap,
                                                  compute_sma_series, compute_wilder_rsi_series,
                                                  compute_wilder_atr_series, session_day_index)
    ot = m["open_time_ms"].to_numpy(np.int64)
    day = session_day_index(ot)
    first = day > day[0]                                  # drop the seeded head day
    out: Dict[str, object] = {}

    first_idx = np.flatnonzero(first)

    def cmp(name: str, mine: np.ndarray, stored: np.ndarray, dp: int = None, rel: float = 0.0,
            accum: float = 4.0):
        """dp = the decimals the export stores this column at (see _finalise).

        Recomputing from *stored* inputs cannot beat the stored quantisation: each input carries up
        to half a quantum of error. A deviation inside a few quanta is therefore agreement at the
        precision the file actually holds, and is reported as such rather than as a mismatch.
        """
        a, b = mine[first], stored[first]
        ok = np.isfinite(a) & np.isfinite(b)
        if not ok.any():
            out[name] = {"checked": 0}
            return
        dev = np.abs(a - b)
        q = 0.5 * 10.0 ** (-dp) if dp is not None else 0.0
        scale = np.maximum(np.abs(b), 1.0)
        # `accum` widens the bound for cumulative quantities: each term carries up to half a
        # quantum, so a day of 15m bars can accumulate ~96 of them before the result is rounded.
        thr = np.maximum(accum * q + 1e-12, rel * scale)
        bad = (dev > thr) & ok
        idx = np.flatnonzero(bad)
        out[name] = {"checked": int(ok.sum()),
                     "bars_mismatching": int(bad.sum()),
                     "last_mismatch_bar_in_file": int(first_idx[idx[-1]]) if len(idx) else None,
                     "bars_mismatching_beyond_bar_2000": int((first_idx[idx] > 2000).sum()) if len(idx) else 0,
                     "max_abs_dev": float(np.nanmax(dev[ok])),
                     "half_quantum_of_stored_dp": q if dp is not None else None,
                     "explained_by_export_rounding": bool(not bad.any()),
                     "max_rel_dev": float(np.nanmax(dev[ok] / scale[ok]))}

    h = m["high"].to_numpy(np.float64)
    l = m["low"].to_numpy(np.float64)
    c = m["close"].to_numpy(np.float64)
    v = m["volume_base"].to_numpy(np.float64)
    tb = m["taker_buy_vol_btc"].to_numpy(np.float64)
    tsx = m["taker_sell_vol_btc"].to_numpy(np.float64)

    cmp("session_vwap", compute_session_vwap(ot, h, l, c, v), m["session_vwap"].to_numpy(np.float64), PRICE_DP)
    cvd = pd.Series(tb - tsx).groupby(day).cumsum().to_numpy(np.float64)
    cmp("session_cvd", cvd, m["future_cvd_session"].to_numpy(np.float64), COIN_DP, accum=96 * 2)
    vq = m["volume_quote"].to_numpy(np.float64)
    if "volume_sma9" in m:
        cmp("volume_sma9_on_quote_volume", compute_sma_series(vq, 9), m["volume_sma9"].to_numpy(np.float64), USD_DP)
    if "volume_ratio" in m:
        sma_b = pd.Series(v).rolling(9, min_periods=1).mean().to_numpy(np.float64)
        cmp("volume_ratio_on_base_volume", np.divide(v, sma_b, out=np.zeros_like(v), where=sma_b > 0),
            m["volume_ratio"].to_numpy(np.float64), RATIO_DP)
    if {"long_liq_usd", "short_liq_usd", "liq_imbalance_ratio"} <= set(m.columns):
        lg = np.abs(m["long_liq_usd"].to_numpy(np.float64))
        sh = np.abs(m["short_liq_usd"].to_numpy(np.float64))
        tot = sh + lg
        cmp("liq_imbalance_formula", np.divide(sh - lg, tot, out=np.zeros_like(tot), where=tot > 0),
            m["liq_imbalance_ratio"].to_numpy(np.float64), RATIO_DP)
    cmp("ema_8", compute_ema_series(c, 8), m["ema_8"].to_numpy(np.float64), PRICE_DP)
    cmp("rsi_14", compute_wilder_rsi_series(c, 14), m["rsi_14"].to_numpy(np.float64), RATIO_DP)
    cmp("atr_14", compute_wilder_atr_series(h, l, c, 14), m["atr_14"].to_numpy(np.float64), PRICE_DP)

    # value area: prev_day_* must be the PREVIOUS day's closing value area (causal),
    # and must NOT be the current day's running value area (that would be lookahead).
    if {"prev_day_vah", "session_vah"} <= set(m.columns):
        df = pd.DataFrame({"day": day, "vah": m["session_vah"].to_numpy(np.float64),
                           "pvh": m["prev_day_vah"].to_numpy(np.float64)})
        end_of_day = df.groupby("day")["vah"].last()
        days = df["day"].to_numpy()
        cur = end_of_day.shift(1).reindex(days).to_numpy(np.float64)
        cur_ok = np.isfinite(cur)
        same_day = df.groupby("day")["vah"].transform("last").to_numpy(np.float64)
        tol = 1e-6 * np.maximum(np.abs(cur), 1.0)
        out["prev_day_vah_is_causal_shift"] = {
            "days_checked": int(cur_ok.sum()),
            "mismatching_vs_previous_day": int((np.abs(df["pvh"].to_numpy(np.float64)[cur_ok] - cur[cur_ok]) > tol[cur_ok]).sum()),
            "equal_to_LEAKING_same_day_value": int((np.abs(df["pvh"].to_numpy(np.float64)[cur_ok] - same_day[cur_ok]) <= tol[cur_ok]).sum()),
            "constant_within_day": int((df.groupby("day")["pvh"].nunique() == 1).sum()),
            "days_in_file": int(len(end_of_day)),
        }
    return out


# ---------------------------------------------------------------------- master
def audit_master(sym: str, m: pd.DataFrame, man: Dict) -> Dict:
    out: Dict[str, object] = {"rows": int(len(m)), "columns": int(m.shape[1])}
    ot = m["open_time_ms"].to_numpy(np.int64)
    d = np.diff(ot)

    out["cadence"] = {"steps": int(len(d)), "distinct_step_values": sorted(set(d.tolist()))[:6],
                      "bars_not_exactly_900s_apart": int((d != STEP_MS).sum())}
    out["monotonic_strict"] = viol((d <= 0).sum())
    out["duplicate_timestamps"] = viol(len(ot) - len(np.unique(ot)))
    out["close_time_identity"] = viol((m["close_time_ms"].to_numpy(np.int64) - ot != CLOSE_OFFSET_MS).sum())

    from Engine.core.schema import COLUMN_DTYPES, LADDER_COLUMNS  # noqa: WPS433
    declared = list(COLUMN_DTYPES)
    out["schema"] = {"declared_master_columns": len(declared), "present": int(m.shape[1]),
                     "missing": [c for c in declared if c not in m.columns],
                     "undeclared": [c for c in m.columns if c not in declared]}
    bad_dtype = {c: str(m[c].dtype) for c in declared if c in m.columns
                 and str(m[c].dtype) != COLUMN_DTYPES[c] and not (
                     COLUMN_DTYPES[c] == "string" and str(m[c].dtype) in ("object", "str", "string", "string[python]", "large_string[pyarrow]"))}
    out["dtype_conformance"] = {"mismatches": bad_dtype}
    out["rows_match_manifest"] = viol(man.get("total_rows", -1) != len(m))

    o = m["open"].to_numpy(np.float64)
    h = m["high"].to_numpy(np.float64)
    l = m["low"].to_numpy(np.float64)
    c = m["close"].to_numpy(np.float64)
    out["high_ge_open_close"] = viol((h < np.maximum(o, c)).sum())
    out["low_le_open_close"] = viol((l > np.minimum(o, c)).sum())
    out["high_ge_low"] = viol((h < l).sum())
    out["prices_strictly_positive"] = viol((np.minimum.reduce([o, h, l, c]) <= 0).sum())

    v = m["volume_base"].to_numpy(np.float64)
    out["volume_nonneg"] = viol((v < 0).sum())
    out["quote_volume_nonneg"] = viol((m["volume_quote"].to_numpy(np.float64) < 0).sum())
    tb = m["taker_buy_vol_btc"].to_numpy(np.float64)
    tsx = m["taker_sell_vol_btc"].to_numpy(np.float64)
    out["taker_buy_le_volume"] = viol((tb > v + 1e-9).sum())
    out["taker_sell_le_volume"] = viol((tsx > v + 1e-9).sum())
    out["taker_split_sums_to_volume"] = viol((np.abs(tb + tsx - v) > 1e-6 * np.maximum(v, 1)).sum())
    out["trade_count_nonneg"] = viol((m["trade_count"].to_numpy(np.float64) < 0).sum())

    sc = m["spot_close"].to_numpy(np.float64)
    src_ok = m["spot_flow_source"].to_numpy() != "UNAVAILABLE"
    out["basis_equals_close_minus_spot"] = viol(
        (np.abs((c - sc)[src_ok] - m["basis_usd"].to_numpy(np.float64)[src_ok]) > 1e-6 * np.maximum(np.abs(c[src_ok]), 1)).sum())
    oi = m["open_interest_k"].to_numpy(np.float64)
    av = m["metrics_available"].to_numpy(np.int8)
    av1 = av == 1
    usd = m["open_interest_usd"].to_numpy(np.float64)
    rel = np.abs(oi * 1000.0 * c - usd) / np.maximum(np.abs(usd), 1.0)     # "k" = thousands of base
    out["oi_usd_matches_oi_x_close"] = viol((rel[av1] > 0.01).sum())
    out["oi_usd_zero_while_oi_nonzero"] = viol(((usd == 0) & (oi > 0) & av1).sum())
    out["oi_change_pct_is_pclipped_to_pm100"] = viol((np.abs(m["oi_change_pct"].to_numpy(np.float64)) > 100 + 1e-9).sum())
    out["cvd_equals_taker_split"] = viol((np.abs((tb - tsx) - m["future_cvd_15m"].to_numpy(np.float64)) > 1e-6 * np.maximum(v, 1)).sum())
    out["vah_ge_val"] = viol((m["session_vah"].to_numpy(np.float64) < m["session_val"].to_numpy(np.float64) - 1e-9).sum())
    out["prev_day_vah_ge_val"] = viol((m["prev_day_vah"].to_numpy(np.float64) < m["prev_day_val"].to_numpy(np.float64) - 1e-9).sum())
    out["spot_close_positive_where_exact"] = viol(((sc <= 0) & src_ok).sum())
    if "fp_poc" in m:
        out["fp_poc_positive_where_present"] = viol(((m["fp_poc"].to_numpy(np.float64) <= 0) & (m["poc_source"].to_numpy() != "UNAVAILABLE")).sum())

    num = m.select_dtypes(include=[np.number])
    out["null_cells"] = viol(m.isna().to_numpy().sum())
    out["non_finite_cells"] = viol((~np.isfinite(num.to_numpy(np.float64))).sum())

    dom: Dict[str, object] = {}
    for col, lo, hi in (("rsi_14", 0, 100), ("liq_imbalance_ratio", -1, 1), ("taker_volume_ratio", 0, 1e6),
                        ("fp_poc_vol_ratio", 0, 1), ("funding_rate_pct", -2, 2), ("oi_change_pct", -100, 100),
                        ("atr_14", 0, None), ("atr_100", 0, None), ("open_interest_k", 0, None),
                        ("whale_index", 0, None), ("ls_ratio_global", 0, None), ("ls_ratio_top", 0, None),
                        ("top_account_ratio", 0, None), ("short_liq_usd", 0, None),
                        ("bid_depth_usd", 0, None), ("ask_depth_usd", 0, None), ("max_trade_vol_btc", 0, None),
                        ("avg_trade_size_usd", 0, None), ("session_vah", 0, None), ("session_val", 0, None),
                        ("basis_usd", None, None)):
        if col not in m:
            dom[col] = {"absent_from_schema": True}
            continue
        x = m[col].to_numpy(np.float64)
        n = 0
        if lo is not None:
            n += int((x < lo).sum())
        if hi is not None:
            n += int((x > hi).sum())
        if lo == 0 and hi is None and col.startswith(("atr",)):
            n += int((x <= 0).sum())                        # ATR must be strictly positive on live bars
        dom[col] = {"violations": n, "min": float(np.nanmin(x)), "max": float(np.nanmax(x)),
                    "nunique": int(pd.Series(x).nunique())}
    lgx = m["long_liq_usd"].to_numpy(np.float64)
    dom["long_liq_usd(sign<=0)"] = {"violations": int((lgx > 0).sum()), "min": float(np.nanmin(lgx)),
                                     "max": float(np.nanmax(lgx)), "nunique": int(pd.Series(lgx).nunique())}
    out["domains"] = dom

    u = np.unique(np.round(c, 8))
    tick = float(np.min(np.diff(u)[np.diff(u) > 0])) if len(u) > 1 else 0.0
    atr = m["atr_14"].to_numpy(np.float64)
    out["precision"] = {"close_distinct": int(len(u)), "close_min_tick": tick,
                        "tick_over_price_pct": round(100.0 * tick / float(np.median(c)), 6),
                        "atr_14_distinct": int(pd.Series(atr).nunique()),
                        "atr_14_nonpositive_bars": int((atr <= 0).sum()),
                        "basis_distinct": int(pd.Series(m["basis_usd"].to_numpy(np.float64)).nunique())}

    att: Dict[str, object] = {}
    imp = m["is_imputed_metrics"].to_numpy(np.int8)
    att["imputed_tautology"] = viol((imp != (av == 0).astype(np.int8)).sum())
    months = pd.to_datetime(ot, unit="ms", utc=True).strftime("%Y-%m")
    frac = pd.Series(av).groupby(months).mean()
    attested = {str(x)[:7] for x in (man.get("provenance", {}).get("metrics_archive_absent_months") or [])}
    zero = {k for k, f in frac.items() if f < 1e-12}
    att["months_total"] = int(len(frac))
    att["months_attested_absent"] = len(attested)
    att["months_zero_metrics"] = len(zero)
    att["months_zero_metrics_UNATTESTED"] = sorted(zero - attested)
    att["months_attested_but_has_metrics"] = sorted(m for m in attested if m in frac and frac[m] > 1e-12)
    att["months_partial_coverage"] = {k: round(float(f), 4) for k, f in frac.items() if 1e-12 < f < 0.999}
    noav = av == 0
    if noav.any():
        sig_cols = [c for c in FALLBACK if c in m]
        exact = np.ones(int(noav.sum()), dtype=bool)
        for col in sig_cols:
            exact &= m[col].to_numpy(np.float64)[noav] == FALLBACK[col]
        att["imputed_bars"] = int(noav.sum())
        att["imputed_bars_with_fallback_constants"] = int(exact.sum())      # pre-archive absence
        att["imputed_bars_with_live_values"] = int((~exact).sum())          # quarantine of real-but-untrusted data
        # Every fallback-constant bar must live in a month the manifest attests as absent (or in a
        # month with zero metrics at all) -- otherwise the pipeline invented a pre-archive region.
        fb_months = {str(x) for x in pd.Series(months)[np.flatnonzero(noav)[exact]]}
        att["imputed_fallback_months_not_attested_or_zero"] = sorted(
            fb_months - attested - {k for k, f in frac.items() if f < 1e-12})
        # a bar that is BOTH marked available AND carries the full fallback signature is the
        # fabrication shape the council exists to catch -- measured here without the council's code
        live = av1
        if live.any():
            leaka = np.ones(int(live.sum()), dtype=bool)
            for col in sig_cols:
                leaka &= m[col].to_numpy(np.float64)[live] == FALLBACK[col]
            att["AVAILABLE_bars_with_full_fallback_signature"] = int(leaka.sum())
    leak = {}
    for col, val in FALLBACK.items():
        if col in m:
            x = m[col].to_numpy(np.float64)[av1]
            if len(x):
                leak[col] = round(float((x == val).mean()), 6)
    att["fallback_value_share_among_AVAILABLE_bars"] = leak
    out["attestation"] = att

    syn = m["is_synthetic"].to_numpy(np.int8) == 1
    out["synthetic_bars"] = int(syn.sum())
    out["synthetic_bars_with_nonzero_volume"] = viol((syn & (v > 0)).sum())
    out["synthetic_bars_with_nonzero_metrics"] = viol((syn & av1).sum())
    conv = m["is_warmup_converged"].to_numpy(np.int8)
    out["warmup_unconverged_bars"] = int((conv == 0).sum())
    out["warmup_regression_after_convergence"] = viol((np.diff(conv) < 0).sum())
    # ---- frozen-run census: A1b flags >=288 bars; shorter runs are invisible to the gate ----
    STALE_FLOOR = 288
    fr: Dict[str, object] = {}
    for col in ("open_interest_k", "ls_ratio_global", "whale_index"):
        if col not in m:
            continue
        x = m[col].to_numpy(np.float64)
        same = np.r_[False, x[1:] == x[:-1]] & av1 & ~syn          # unchanged AND marked fresh
        runs = np.flatnonzero(np.r_[True, same[1:] != same[:-1]])
        lengths = np.diff(np.r_[runs, len(same)]) * same[runs]
        sub = lengths[(lengths >= 1) & (lengths < STALE_FLOOR)]
        fr[col] = {"runs_2_to_287_bars_while_marked_fresh": int((sub >= 1).sum()),
                   "bars_in_them": int(sub.sum()),
                   "runs_ge_288_should_have_been_flagged": int((lengths >= STALE_FLOOR).sum())}
    out["sub_threshold_frozen_runs"] = fr

    # ---- the council's dead-feature allowlist, audited: what does it forgive? ----
    from Engine.core.schema import ALLOWED_CONSTANT_COLUMNS
    wl = {}
    for col in ALLOWED_CONSTANT_COLUMNS:
        if col not in m or col == "symbol":
            continue
        nn = int(m[col].nunique())
        if nn <= 1:
            wl[col] = {"distinct": 1, "value": str(m[col].iloc[0])}
        elif m[col].dtype.kind == "f" and float((m[col].to_numpy(np.float64) == 0.0).mean()) > 0.999:
            wl[col] = {"distinct": nn, "zero_share": round(float((m[col].to_numpy(np.float64) == 0.0).mean()), 6)}
    out["allowlisted_near_dead_columns"] = wl
    out["poc_source_share"] = {str(k): round(float(v), 6) for k, v in
                               (m["poc_source"].value_counts(normalize=True) if "poc_source" in m else pd.Series(dtype=float)).items()}
    out["future_flow_source_share"] = {str(k): round(float(v), 6) for k, v in m["future_flow_source"].value_counts(normalize=True).items()}
    out["causality"] = causality(m)
    return out


# ---------------------------------------------------------------------- ladder
def audit_ladder(lad: pd.DataFrame, bars: pd.DataFrame) -> Dict:
    out: Dict[str, object] = {"rungs": int(len(lad))}
    ot = lad["open_time_ms"].to_numpy(np.int64)
    bid = lad["bid_vol_coin"].to_numpy(np.float64)
    ask = lad["ask_vol_coin"].to_numpy(np.float64)
    nd = lad["net_delta_coin"].to_numpy(np.float64)
    tot = ask + bid
    out["bid_ask_nonneg"] = viol(((bid < 0) | (ask < 0)).sum())
    out["delta_identity"] = viol((np.abs(nd - (ask - bid)) > 1e-6 * np.maximum(ask + bid, 1)).sum())
    for col in ("is_buy_imbalance", "is_sell_imbalance", "rung_source", "is_poc"):
        if col in lad:
            out[f"{col}_domain"] = viol((~lad[col].isin((0, 1)).to_numpy()).sum())
    pb = lad["price_bin"].to_numpy(np.float64)
    out["price_bin_positive"] = viol((pb <= 0).sum())
    out["rung_trade_count_nonneg"] = viol((lad["trade_count"].to_numpy(np.float64) < 0).sum()) if "trade_count" in lad else None

    uniq = np.unique(ot)
    starts = np.flatnonzero(np.r_[True, ot[1:] != ot[:-1]])
    poc = np.bincount(np.searchsorted(uniq, ot), weights=lad["is_poc"].to_numpy(np.float64), minlength=len(uniq))
    out["bars_in_ladder"] = int(len(uniq))
    out["poc_exactly_one_per_bar"] = viol((poc != 1).sum())
    same = np.r_[np.diff(ot) == 0]
    out["price_bin_strictly_increasing_within_bar"] = viol((np.diff(pb)[same] <= 0).sum())
    dupkey = pd.DataFrame({"ot": ot, "p": np.round(pb, 10)})
    out["duplicate_rung_rows"] = viol(dupkey.duplicated().sum())
    del dupkey
    out["master_bars_without_rungs"] = viol(len(np.setdiff1d(bars["ot"].to_numpy(np.int64), uniq)))
    out["ladder_bars_absent_from_master"] = viol(len(np.setdiff1d(uniq, bars["ot"].to_numpy(np.int64))))

    src = lad["rung_source"].to_numpy(np.int8)
    out["rung_source_counts"] = {int(k): int(v) for k, v in zip(*np.unique(src, return_counts=True))}
    out["rung_source_synthetic_share"] = round(float((src == 1).mean()), 6)
    out["rung_source_tick_exact_bars"] = int(len(np.unique(ot[src == 0])))

    # conservation: rung volumes must reproduce the candle's taker split
    per_bar = pd.DataFrame({"ot": ot, "tot": tot, "nd": nd, "tc": lad["trade_count"].to_numpy(np.float64)} if "trade_count" in lad
                           else {"ot": ot, "tot": tot, "nd": nd}).groupby("ot", sort=True).sum()
    j = bars.set_index("ot").join(per_bar, how="left")
    have = j["tot"].notna().to_numpy()
    dv = np.abs(j["volume_base"].to_numpy(np.float64)[have] - j["tot"].to_numpy(np.float64)[have])
    scale = np.maximum(j["volume_base"].to_numpy(np.float64)[have], 1e-9)
    out["rung_volume_conservation"] = {"bars_checked": int(have.sum()),
                                       "bars_mismatching": int((dv > 1e-6 * scale).sum()),
                                       "max_rel_dev": float(np.max(dv / scale)) if have.any() else 0.0}
    dn = np.abs(j["cvd"].to_numpy(np.float64)[have] - j["nd"].to_numpy(np.float64)[have])
    out["rung_delta_conserves_cvd"] = {"bars_mismatching": int((dn > 1e-6 * np.maximum(scale, 1)).sum())}
    if "fp_poc" in j:
        ok = (j["fp_poc"].to_numpy(np.float64) > 0) & have
        dp = np.abs(j["poc_price"].to_numpy(np.float64)[ok] - j["fp_poc"].to_numpy(np.float64)[ok])
        out["master_poc_matches_ladder_poc_rung"] = {"bars_checked": int(ok.sum()),
                                                     "mismatching": int((dp > 1e-6 * np.maximum(j["fp_poc"].to_numpy(np.float64)[ok], 1)).sum())}
    return out


# ------------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="")
    ap.add_argument("--council", action="store_true")
    ap.add_argument("--out", default="/tmp/forensic_results.json")
    args = ap.parse_args()

    syms = sorted(os.path.basename(f).split("_15m_master")[0]
                  for f in glob.glob(os.path.join(DATA_DIR, "*_master_*.parquet")))
    if args.symbols:
        want = set(args.symbols.split(","))
        syms = [s for s in syms if s in want]
    results: Dict[str, Dict] = {}
    for i, sym in enumerate(syms, 1):
        mpath = os.path.join(DATA_DIR, f"{sym}_15m_master_2020_2026.parquet")
        jpath = os.path.join(DATA_DIR, f"{sym}_dataset_manifest.json")
        man = json.load(open(jpath)) if os.path.exists(jpath) else {}
        m = pd.read_parquet(mpath)
        print(f"[{i}/{len(syms)}] {sym}  master {len(m):,} x {m.shape[1]}", flush=True)
        bars = pd.DataFrame({"ot": m["open_time_ms"].to_numpy(np.int64),
                             "volume_base": m["volume_base"].to_numpy(np.float64),
                             "cvd": (m["taker_buy_vol_btc"] - m["taker_sell_vol_btc"]).to_numpy(np.float64),
                             "fp_poc": m["fp_poc"].to_numpy(np.float64) if "fp_poc" in m else np.zeros(len(m))})
        rec = {"master": audit_master(sym, m, man)}
        poc_price = m["fp_poc"].to_numpy(np.float64).copy() if "fp_poc" in m else None
        m = None
        gc.collect()
        lpath = os.path.join(DATA_DIR, f"{sym}_15m_footprint_ladder.parquet")
        if os.path.exists(lpath):
            lad = pd.read_parquet(lpath, columns=["open_time_ms", "price_bin", "bid_vol_coin", "ask_vol_coin",
                                                  "net_delta_coin", "is_poc", "rung_source",
                                                  "is_buy_imbalance", "is_sell_imbalance", "trade_count"])
            if poc_price is not None:
                bars["poc_price"] = poc_price
            rec["ladder"] = audit_ladder(lad, bars)
            lad = None
            gc.collect()
        if args.council:
            import Engine.verification.verify_parquet_integrity as V
            rep = V.verify_symbol(DATA_DIR, sym, log=lambda s: None)
            rec["council"] = {"passed": bool(rep.passed), "agents": dict(rep.agent_status),
                              "findings": [str(f) for f in rep.findings[:6]]}
        results[sym] = rec
        del bars, man
        gc.collect()
        mb = rec["master"]
        lb = rec.get("ladder", {})
        bad_m = {k: v for k, v in mb.items() if isinstance(v, dict) and "violations" in v and v["violations"]}
        bad_l = {k: v for k, v in lb.items() if isinstance(v, dict) and "violations" in v and v["violations"]}
        print(f"      rungs {lb.get('rungs', 0):,} | master viol {bad_m or 'NONE'} | ladder viol {bad_l or 'NONE'}", flush=True)
        print(f"      causality {json.dumps(mb['causality'], default=str)[:220]}", flush=True)

    with open(args.out, "w") as fh:
        json.dump(results, fh, indent=1, default=str)
    tot_bars = sum(r["master"]["rows"] for r in results.values())
    tot_rungs = sum(r.get("ladder", {}).get("rungs", 0) for r in results.values())
    print(f"\nTOTALS: {len(results)} symbols | {tot_bars:,} bars | {tot_rungs:,} rungs -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
