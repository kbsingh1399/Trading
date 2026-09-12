"""Causal price-level and volume-profile (POC) construction.

Two independent blocks:

``LEVELS``   prior-day / prior-week / prior-month / all-time highs and lows,
             period opens and "fresh break / sweep" events -- pure OHLC, no
             estimation error.

``PROFILE``  a *reconstructed* volume profile built from 15m OHLCV with a
             per-bar intra-bar volume distribution, giving the session Point of
             Control (POC), value-area high/low (VAH/VAL) and low-volume node
             (LVN), both *developing* (up to bar t) and *completed* (prior
             session).

Why reconstruct the profile instead of using the shipped ladder?
    ``docs/PIPELINE_CERTIFICATION_ROUND5.md`` establishes that the shipped
    ``*_15m_footprint_ladder.parquet`` rungs are ``poc_source = OHLC_APPROX``
    -- i.e. synthesised from the candle, not from a tick archive.  Deriving a
    "POC" straight off that ladder would be fitting a deterministic transform
    of OHLC.  ``validate_profile()`` measures the disagreement between the two
    so the assumption is auditable rather than assumed.

All profile maths is causal: the developing profile at bar *t* only ever sums
rungs of bars ``<= t`` inside the current session.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from numba import njit

from . import DAY_MS

# ----------------------------------------------------------------------------
# Point-in-time session / period keys
# ----------------------------------------------------------------------------


def session_key(open_time_ms: np.ndarray) -> np.ndarray:
    """UTC calendar day id of each 15m bar."""
    return (open_time_ms // DAY_MS).astype(np.int64)


def week_key(open_time_ms: np.ndarray) -> np.ndarray:
    """ISO-ish week id (Monday 00:00 UTC)."""
    # 1970-01-01 was a Thursday -> shift by 3 days so floor-division gives Monday.
    return ((open_time_ms + 3 * DAY_MS) // (7 * DAY_MS)).astype(np.int64)


def month_key(open_time_ms: np.ndarray) -> np.ndarray:
    dt = pd.to_datetime(open_time_ms, unit="ms", utc=True)
    return (dt.year.to_numpy(np.int64) * 12 + dt.month.to_numpy(np.int64) - 1)


def build_levels(master: pd.DataFrame) -> pd.DataFrame:
    """Add every prior-period level and level-event flag to a symbol frame."""
    f = master.reset_index(drop=True).copy()
    t = f.open_time_ms.to_numpy(np.int64)
    h = f.high.to_numpy(float)
    lo = f.low.to_numpy(float)
    c = f.close.to_numpy(float)
    o = f.open.to_numpy(float)

    day = session_key(t)
    week = week_key(t)
    month = month_key(t)

    # --- prior completed session -------------------------------------------
    d = pd.DataFrame({"k": day, "h": h, "l": lo, "t": t, "o": o, "c": c})
    da = d.groupby("k", sort=True).agg(pdh=("h", "max"), pdl=("l", "min"), pdc=("c", "last"))
    f["pdh"] = da.pdh.shift(1).reindex(day).to_numpy(float)
    f["pdl"] = da.pdl.shift(1).reindex(day).to_numpy(float)
    f["pdc"] = da.pdc.shift(1).reindex(day).to_numpy(float)
    day_open = d.groupby("k", sort=False)["o"].transform("first").to_numpy(float)
    f["day_open"] = day_open

    # --- prior completed ISO week / calendar month --------------------------
    wa = d.assign(k=week).groupby("k", sort=True).agg(pwh=("h", "max"), pwl=("l", "min"))
    f["pwh"] = wa.pwh.shift(1).reindex(week).to_numpy(float)
    f["pwl"] = wa.pwl.shift(1).reindex(week).to_numpy(float)
    ma = d.assign(k=month).groupby("k", sort=True).agg(pmh=("h", "max"), pml=("l", "min"))
    f["pmh"] = ma.pmh.shift(1).reindex(month).to_numpy(float)
    f["pml"] = ma.pml.shift(1).reindex(month).to_numpy(float)
    qa = d.assign(k=month // 3).groupby("k", sort=True).agg(pqh=("h", "max"), pql=("l", "min"))
    f["pqh"] = qa.pqh.shift(1).reindex(month // 3).to_numpy(float)
    f["pql"] = qa.pql.shift(1).reindex(month // 3).to_numpy(float)

    # --- week / month opens (anchored reference prices) ---------------------
    f["week_open"] = d.assign(k=week).groupby("k", sort=False)["o"].transform("first").to_numpy(float)
    f["month_open"] = d.assign(k=month).groupby("k", sort=False)["o"].transform("first").to_numpy(float)

    # --- all-time high (strictly prior bars, so bar 0 has no known ATH) -----
    ath_prev = np.maximum.accumulate(h)  # max up to and including i
    f["ath"] = np.concatenate([[np.nan], ath_prev[:-1]])
    new_ath = np.zeros(len(f), dtype=bool)
    new_ath[0] = False
    new_ath[1:] = h[1:] >= ath_prev[:-1]
    idx = np.arange(len(f))
    last = np.where(new_ath, idx, -1)
    f["bars_since_ath"] = idx - np.maximum.accumulate(last)
    f["ath_dist"] = (f["ath"].to_numpy(float) - c) / c

    # --- levels relative to ATR --------------------------------------------
    f["range_day"] = f.pdh - f.pdl
    return f


# ----------------------------------------------------------------------------
# Volume profile (reconstructed) -- numba kernels
# ----------------------------------------------------------------------------


@njit(cache=True, fastmath=True)
def _bar_distribution(lb: float, hb: float, bl: int, bh: int, out: np.ndarray, base: int) -> None:
    """Uniform-in-log-price spread of one bar's volume over its price range."""
    n = bh - bl + 1
    if n <= 1:
        out[bl - base] += 1.0
        return
    w = 1.0 / n
    for b in range(bl, bh + 1):
        out[b - base] += w


@njit(cache=True, fastmath=True)
def _value_area(cum_row: np.ndarray, nb: int, poc: int, va_frac: float):
    """Greedy TPO expansion from the POC until ``va_frac`` of volume is covered."""
    total = 0.0
    for b in range(nb):
        total += cum_row[b]
    if total <= 0.0:
        return poc, poc
    lo = poc
    hi = poc
    acc = cum_row[poc]
    target = va_frac * total
    while acc < target and (lo > 0 or hi < nb - 1):
        left = cum_row[lo - 1] if lo > 0 else -1.0
        right = cum_row[hi + 1] if hi < nb - 1 else -1.0
        if right >= left:
            hi += 1
            acc += right
        else:
            lo -= 1
            acc += left
    return lo, hi


@njit(cache=True, fastmath=True)
def _lvn(cum_row: np.ndarray, lo: int, hi: int, poc: int) -> int:
    """Lowest-volume node strictly inside the value area (excluding the POC)."""
    best = poc
    best_v = 1e30
    for b in range(lo, hi + 1):
        if b == poc:
            continue
        v = cum_row[b]
        if v < best_v:
            best_v = v
            best = b
    return best


@njit(cache=True, fastmath=True)
def profile_series(
    low: np.ndarray,
    high: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    day: np.ndarray,
    w: float,
    max_bins: int,
    va_frac: float,
):
    """Developing + completed session volume profile for every bar.

    Returns
    -------
    dev_poc, dev_vah, dev_val, dev_lvn : price arrays (per bar)
    dev_share      : volume at the developing POC / session volume so far
    sess_poc, sess_vah, sess_val : completed *current* session values at bar t
                    (they keep updating; the previous session's final values are
                    produced by the caller with a one-session shift)
    poc_delta      : signed distance the POC has migrated within the session,
                    in bin widths (positive = value migrating up)
    """
    n = len(low)
    dev_poc = np.full(n, np.nan)
    dev_vah = np.full(n, np.nan)
    dev_val = np.full(n, np.nan)
    dev_lvn = np.full(n, np.nan)
    dev_share = np.full(n, np.nan)
    sess_poc = np.full(n, np.nan)
    sess_vah = np.full(n, np.nan)
    sess_val = np.full(n, np.nan)
    poc_delta = np.zeros(n)

    cum = np.zeros((256, max_bins), np.float32)
    start = 0
    while start < n:
        end = start + 1
        while end < n and day[end] == day[start]:
            end += 1
        nbars = min(end - start, 256)
        lo_all = 1e30
        hi_all = -1e30
        for j in range(start, end):
            if low[j] < lo_all:
                lo_all = low[j]
            if high[j] > hi_all:
                hi_all = high[j]
        bl = int(np.floor(np.log(lo_all) / w))
        bh = int(np.ceil(np.log(hi_all) / w))
        nb = bh - bl + 1
        if nb > max_bins:
            nb = max_bins
            bh = bl + nb - 1
        for r in range(nbars):
            for b in range(nb):
                cum[r, b] = 0.0
        prev_poc = -1
        for r in range(nbars):
            j = start + r
            if volume[j] > 0.0 and high[j] > low[j] > 0.0:
                bbl = int(np.floor(np.log(low[j]) / w))
                bbh = int(np.ceil(np.log(high[j]) / w))
                if bbl < bl:
                    bbl = bl
                if bbh > bh:
                    bbh = bh
                if r > 0:
                    for b in range(nb):
                        cum[r, b] = cum[r - 1, b]
                _bar_distribution(low[j], high[j], bbl, bbh, cum[r], bl)
            elif r > 0:
                for b in range(nb):
                    cum[r, b] = cum[r - 1, b]
            tot = 0.0
            for b in range(nb):
                tot += cum[r, b]
            if tot <= 0.0:
                continue
            poc = 0
            bestv = -1.0
            for b in range(nb):
                if cum[r, b] > bestv:
                    bestv = cum[r, b]
                    poc = b
            vlo, vhi = _value_area(cum[r], nb, poc, va_frac)
            lvn = _lvn(cum[r], vlo, vhi, poc)
            dev_poc[j] = np.exp((bl + poc + 0.5) * w)
            dev_vah[j] = np.exp((bl + vhi + 0.5) * w)
            dev_val[j] = np.exp((bl + vlo + 0.5) * w)
            dev_lvn[j] = np.exp((bl + lvn + 0.5) * w)
            dev_share[j] = bestv / tot
            sess_poc[j] = dev_poc[j]
            sess_vah[j] = dev_vah[j]
            sess_val[j] = dev_val[j]
            if prev_poc >= 0:
                poc_delta[j] = float(poc - prev_poc)
            prev_poc = poc
        start = end
    return dev_poc, dev_vah, dev_val, dev_lvn, dev_share, sess_poc, sess_vah, sess_val, poc_delta


def build_profile(
    master: pd.DataFrame, bin_width: float = 0.0005, va_frac: float = 0.70, max_bins: int = 2048
) -> pd.DataFrame:
    """Attach reconstructed volume-profile features (all causal)."""
    f = master.reset_index(drop=True).copy()
    t = f.open_time_ms.to_numpy(np.int64)
    day = session_key(t)
    out = profile_series(
        f.low.to_numpy(float),
        f.high.to_numpy(float),
        f.close.to_numpy(float),
        f.volume_base.to_numpy(float),
        day,
        bin_width,
        max_bins,
        va_frac,
    )
    (f["dev_poc"], f["dev_vah"], f["dev_val"], f["dev_lvn"], f["dev_share"],
     f["sess_poc"], f["sess_vah"], f["sess_val"], f["poc_delta"]) = out

    # Previous *completed* session's final profile (one full session shift).
    last = pd.DataFrame({"day": day, "poc": f.sess_poc, "vah": f.sess_vah, "val": f.sess_val}).groupby("day", sort=True).last()
    f["prior_poc"] = last.poc.shift(1).reindex(day).to_numpy(float)
    f["prior_vah"] = last.vah.shift(1).reindex(day).to_numpy(float)
    f["prior_val"] = last.val.shift(1).reindex(day).to_numpy(float)

    # Prior-day bucket extremes of the *profile* (POC range of yesterday).
    pmin = pd.DataFrame({"day": day, "p": f.sess_poc}).groupby("day", sort=True).min()
    pmax = pd.DataFrame({"day": day, "p": f.sess_poc}).groupby("day", sort=True).max()
    f["prior_poc_low"] = pmin.p.shift(1).reindex(day).to_numpy(float)
    f["prior_poc_high"] = pmax.p.shift(1).reindex(day).to_numpy(float)

    # Session-anchored VWAP (causal, resets each session).
    pv = (f.high + f.low + f.close) / 3.0 * f.volume_base
    f["sess_vwap"] = pv.groupby(day).cumsum() / f.volume_base.groupby(day).cumsum().replace(0, np.nan)
    return f


# ----------------------------------------------------------------------------
# Validation against the shipped ladder (documented approximation)
# ----------------------------------------------------------------------------


def validate_profile(master: pd.DataFrame, ladder_path, bin_width: float = 0.0005) -> dict:
    """Compare our reconstructed session POC with the shipped ladder's POC.

    The ladder carries exactly one ``is_poc`` rung per candle, which is itself an
    OHLC approximation (``poc_source = OHLC_APPROX``).  Agreement is therefore
    only weak evidence; disagreement is informative because it bounds how much
    of a ladder-POC edge could be an artefact.
    """
    import pyarrow.parquet as pq

    l = pq.read_table(ladder_path, columns=["open_time_ms", "price_bin", "is_poc"]).to_pandas()
    l = l[l.is_poc == 1][["open_time_ms", "price_bin"]].rename(columns={"price_bin": "ladder_poc"})
    m = master[["open_time_ms", "high", "low", "close", "volume_base"]].copy()
    m["day"] = session_key(m.open_time_ms.to_numpy(np.int64))
    daily = l.merge(m, on="open_time_ms", how="inner")
    daily = daily.groupby("day").agg(
        ladder_poc=("ladder_poc", "mean"), close=("close", "last")
    )
    prof = build_profile(master, bin_width=bin_width)
    prof["day"] = session_key(prof.open_time_ms.to_numpy(np.int64))
    prof_daily = prof.groupby("day").last()[["sess_poc"]]
    j = daily.join(prof_daily, how="inner").dropna()
    rel = ((j.sess_poc - j.ladder_poc).abs() / j.close).to_numpy(float)
    return {
        "sessions": int(len(j)),
        "median_rel_error": float(np.median(rel)),
        "p90_rel_error": float(np.quantile(rel, 0.9)),
        "within_25bp": float((rel <= 0.0025).mean()),
    }


def ladder_poc_frame(ladder_path, chunk: str = "POC") -> pd.DataFrame:
    """Load the shipped ladder's per-candle POC / value-area flags (reference only)."""
    import pyarrow.parquet as pq

    l = pq.read_table(ladder_path, columns=["open_time_ms", "price_bin", "is_poc", "is_value_area"]).to_pandas()
    if chunk == "POC":
        l = l[l.is_poc == 1][["open_time_ms", "price_bin"]].rename(columns={"price_bin": "ladder_poc"})
    else:
        g = l[l.is_value_area == 1].groupby("open_time_ms")["price_bin"].agg(["min", "max"])
        l = g.rename(columns={"min": "ladder_val", "max": "ladder_vah"}).reset_index()
    return l
