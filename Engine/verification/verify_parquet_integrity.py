"""
================================================================================
AUTONOMOUS 3-AGENT VERIFICATION COUNCIL
================================================================================
+---------------------------------------------------------------+
| Agent 1: Continuity & Cadence | monotonic open_time_ms with    |
|                               | exactly 900,000 ms steps, zero |
|                               | missing / duplicate candles,   |
|                               | close = open + 899,999, ladder |
|                               | referential integrity.         |
+-------------------------------+--------------------------------+
| Agent 2: Microstructure Math  | CVD identities (15m / session  |
|                               | / lifetime), zc_div identity,  |
|                               | basis = close - spot_close,    |
|                               | funding sign/magnitude, VWAP   |
|                               | re-derivation, EMA recursion,  |
|                               | OHLC sanity, non-zero volume   |
|                               | ratios, liquidation polarity,  |
|                               | ladder volume conservation,    |
|                               | exactly one POC per candle.    |
+-------------------------------+--------------------------------+
| Agent 3: Zero-Null & Schema   | zero NaN / null / inf, exact   |
|                               | column set + dtype contract,   |
|                               | string vocabularies, flag      |
|                               | domains, dead-feature scan.    |
+---------------------------------------------------------------+

Each agent returns a list of ``Finding`` objects carrying the bar index and
UTC timestamp of the first offending row. The council verdict is PASS only if
every agent has zero findings. Findings are also returned as data so the
orchestrator can attempt targeted causal repair and re-run the council.

Usage
  python -m Engine.verification.verify_parquet_integrity [target_dir] [--symbol SYM]
================================================================================
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Engine.core.canonical_indicators import (  # noqa: E402
    compute_ema_series,
    compute_session_cvd,
    compute_session_vwap,
    get_merge_level,
)
from Engine.core.schema import (  # noqa: E402
    ALLOWED_CONSTANT_COLUMNS,
    BAR_MS,
    CANONICAL_COLUMNS,
    COLUMN_DTYPES,
    LADDER_COLUMNS,
    LADDER_DTYPES,
    STRING_VOCAB,
    ladder_filename,
    manifest_filename,
    master_filename,
)

DEFAULT_TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "binance_backtesting_data")
_TOL = 1e-6

# --- regime-scan calibration (multi-asset universe) ---------------------------
REGIME_MIN_AVAIL_BARS = 500        # bars *carrying metrics* needed to judge a year
METRICS_INTERIOR_HOLE_BARS = 4032  # 28 days of 15m bars with no metrics content at all
BASIS_MIN_DISTINCT = 20            # a spread that only ever takes <20 values is broken
BASIS_MODAL_SHARE_MAX = 0.98       # >98% of bars on one basis value => spot collapsed


@dataclass
class Finding:
    agent: str
    check: str
    message: str
    bar_index: Optional[int] = None
    open_time_ms: Optional[int] = None
    timestamp_utc: Optional[str] = None
    count: int = 1

    def __str__(self) -> str:
        loc = ""
        if self.bar_index is not None:
            loc = f" @ bar {self.bar_index} ({self.timestamp_utc}, open_time_ms={self.open_time_ms})"
        extra = f" [x{self.count}]" if self.count > 1 else ""
        return f"[{self.agent}] {self.check}: {self.message}{loc}{extra}"


@dataclass
class CouncilReport:
    symbol: str
    passed: bool
    master_rows: int
    ladder_rows: int
    findings: List[Finding] = field(default_factory=list)
    agent_status: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol, "passed": self.passed, "master_rows": self.master_rows,
            "ladder_rows": self.ladder_rows, "agent_status": self.agent_status,
            "findings": [asdict(f) for f in self.findings[:50]],
        }


def _first_bad(mask: np.ndarray, ts: np.ndarray) -> Tuple[Optional[int], Optional[int], Optional[str], int]:
    idx = np.flatnonzero(mask)
    if idx.size == 0:
        return None, None, None, 0
    i = int(idx[0])
    t = int(ts[i])
    return i, t, str(pd.to_datetime(t, unit="ms", utc=True)), int(idx.size)


def _finding(agent: str, check: str, message: str, mask: np.ndarray, ts: np.ndarray) -> Optional[Finding]:
    i, t, s, n = _first_bad(mask, ts)
    if n == 0:
        return None
    return Finding(agent, check, message, i, t, s, n)


# ==============================================================================
# Agent 1 -- Continuity & Cadence
# ==============================================================================
def agent_continuity(master: pd.DataFrame, ladder: Optional[pd.DataFrame],
                     expected_start_ms: Optional[int] = None,
                     expected_end_ms: Optional[int] = None) -> List[Finding]:
    A = "Agent1:Continuity"
    out: List[Finding] = []
    ts = master["open_time_ms"].to_numpy(np.int64)
    n = ts.size
    if n == 0:
        return [Finding(A, "empty", "master has zero rows")]
    if expected_start_ms is not None and n > 0:
        exp_first = (expected_start_ms // BAR_MS) * BAR_MS
        if ts[0] != exp_first:
            out.append(Finding(A, "start_boundary", f"first candle {ts[0]} ({pd.to_datetime(ts[0], unit='ms', utc=True)}) != expected start {exp_first} ({pd.to_datetime(exp_first, unit='ms', utc=True)})"))
    if expected_end_ms is not None and n > 0:
        exp_last = (expected_end_ms // BAR_MS) * BAR_MS
        if ts[-1] != exp_last:
            out.append(Finding(A, "end_boundary", f"last candle {ts[-1]} ({pd.to_datetime(ts[-1], unit='ms', utc=True)}) != expected terminal {exp_last} ({pd.to_datetime(exp_last, unit='ms', utc=True)})"))
    if n > 1:
        d = np.diff(ts)
        f = _finding(A, "monotonic", "open_time_ms not strictly increasing", np.append(False, d <= 0), ts)
        if f:
            out.append(f)
        f = _finding(A, "cadence", f"step != {BAR_MS} ms (missing/extra candle)", np.append(False, d != BAR_MS), ts)
        if f:
            out.append(f)
        dup = np.append(False, d == 0)
        if dup.any():
            out.append(_finding(A, "duplicates", "duplicate open_time_ms", dup, ts))
        missing = int(((ts[-1] - ts[0]) // BAR_MS + 1) - n)
        if missing > 0:
            out.append(Finding(A, "coverage", f"{missing} candle(s) missing from grid"))
    grid = (ts % BAR_MS) != 0
    f = _finding(A, "grid", "open_time_ms not aligned to 15m boundary", grid, ts)
    if f:
        out.append(f)
    ct = master["close_time_ms"].to_numpy(np.int64)
    f = _finding(A, "close_time", "close_time_ms != open_time_ms + 899,999", ct != ts + BAR_MS - 1, ts)
    if f:
        out.append(f)
    dt = pd.to_datetime(master["datetime_utc"], utc=True, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    dt_ms = ((dt - epoch) // pd.Timedelta(milliseconds=1)).fillna(-1).to_numpy(np.int64)
    f = _finding(A, "datetime_utc", "datetime_utc does not match open_time_ms", dt.isna().to_numpy() | (dt_ms != ts), ts)
    if f:
        out.append(f)

    if ladder is not None and not ladder.empty:
        lts = ladder["open_time_ms"].to_numpy(np.int64)
        if lts.size and (np.diff(lts) < 0).any():
            out.append(Finding(A, "ladder_order", "ladder open_time_ms not non-decreasing"))
        uniq = np.unique(lts)
        orphan = ~np.isin(uniq, ts)
        if orphan.any():
            i = int(np.flatnonzero(orphan)[0])
            out.append(Finding(A, "ladder_orphans", "ladder candles absent from master", None, int(uniq[i]),
                               str(pd.to_datetime(uniq[i], unit="ms", utc=True)), int(orphan.sum())))
        in_ladder_scope = (ts >= lts[0]) & (ts <= lts[-1])
        has_volume = (master["volume_base"].to_numpy(np.float64) > 0) if "volume_base" in master else np.ones(len(master), dtype=bool)
        uncovered = ~np.isin(ts, uniq) & in_ladder_scope & has_volume
        f = _finding(A, "ladder_coverage", "master candles without any ladder rung", uncovered, ts)
        if f:
            out.append(f)
        pb = ladder[["open_time_ms", "price_bin"]].to_numpy()
        if len(pb) and pd.DataFrame(pb).duplicated().any():
            out.append(Finding(A, "ladder_dup_rung", "duplicate (open_time_ms, price_bin) rung"))
    return out


# ==============================================================================
# Agent 2 -- Microstructure Math
# ==============================================================================
def agent_microstructure(master: pd.DataFrame, ladder: Optional[pd.DataFrame]) -> List[Finding]:
    A = "Agent2:Microstructure"
    out: List[Finding] = []
    ts = master["open_time_ms"].to_numpy(np.int64)
    has = master.columns.__contains__
    g = lambda c: master[c].to_numpy(np.float64)  # noqa: E731
    o, h, l, c = g("open"), g("high"), g("low"), g("close")
    vb, vq = g("volume_base"), g("volume_quote")
    scale = np.maximum(np.abs(c), 1e-9)

    def add(check, msg, mask):
        f = _finding(A, check, msg, mask, ts)
        if f:
            out.append(f)

    add("ohlc_bounds", "high < max(open, close) or low > min(open, close)",
        (h < np.maximum(o, c) - 1e-9 * scale) | (l > np.minimum(o, c) + 1e-9 * scale))
    add("positive_price", "non-positive price", (o <= 0) | (h <= 0) | (l <= 0) | (c <= 0))
    add("negative_volume", "negative volume", (vb < 0) | (vq < 0))
    synthetic = master["is_synthetic"].to_numpy() == 1 if "is_synthetic" in master else ((h == l) & (vb <= 0))
    add("live_bar_volume", "authentic bar with zero base volume", (~synthetic) & (vb <= 0))
    if has("volume_ratio"):
        add("volume_ratio_nonzero", "volume_ratio must be > 0 on authentic bars", (~synthetic) & (g("volume_ratio") <= 0))
    add("volume_sma9", "volume_sma9 <= 0 on authentic bar", (~synthetic) & (g("volume_sma9") <= 0))

    tb, tsell = g("taker_buy_vol_btc"), g("taker_sell_vol_btc")
    add("taker_split", "taker buy + sell != volume_base", np.abs(tb + tsell - vb) > 1e-6 * np.maximum(vb, 1))
    add("taker_ratio", "taker_volume_ratio must be finite and >= 0", ~(g("taker_volume_ratio") >= 0))

    fut = g("future_cvd_15m")
    add("fut_cvd_identity", "future_cvd_15m != taker_buy - taker_sell", np.abs(fut - (tb - tsell)) > 1e-6 * np.maximum(vb, 1))
    if has("fp_delta"):
        add("fp_delta_identity", "fp_delta != future_cvd_15m", np.abs(g("fp_delta") - fut) > _TOL)
    fs = g("future_cvd_session")
    add("fut_session_cvd", "future_cvd_session != causal session cumsum",
        np.abs(fs - compute_session_cvd(ts, fut)) > 1e-6 * np.maximum(np.abs(fs), 1) + 1e-6)
    fl = g("future_cvd_lifetime")
    add("fut_lifetime_cvd", "future_cvd_lifetime increments != future_cvd_15m",
        np.append(abs(fl[0] - fut[0]) > 1e-6 * max(abs(fut[0]), 1) + 1e-6, np.abs(np.diff(fl) - fut[1:]) > 1e-6 * np.maximum(np.abs(fl[1:]), 1) + 1e-6))
    spot = g("spot_cvd_15m")
    ss = g("spot_cvd_session")
    add("spot_session_cvd", "spot_cvd_session != causal session cumsum",
        np.abs(ss - compute_session_cvd(ts, spot)) > 1e-6 * np.maximum(np.abs(ss), 1) + 1e-6)
    sl = g("spot_cvd_lifetime")
    add("spot_lifetime_cvd", "spot_cvd_lifetime increments != spot_cvd_15m",
        np.append(abs(sl[0] - spot[0]) > 1e-6 * max(abs(spot[0]), 1) + 1e-6, np.abs(np.diff(sl) - spot[1:]) > 1e-6 * np.maximum(np.abs(sl[1:]), 1) + 1e-6))

    unavailable = (master["spot_flow_source"].to_numpy() == "UNAVAILABLE") if "spot_flow_source" in master else ((g("zc_div") == 0.0) & (spot == 0.0) & (fut != 0.0))
    if "spot_flow_source" in master:
        add("spot_unavailable_zero", "spot_cvd_15m must be 0 when spot_flow_source=UNAVAILABLE (stale reuse)", unavailable & (spot != 0))
    if has("zc_div"):
        add("zc_div_identity", "zc_div != spot_cvd_15m - future_cvd_15m on valid spot bars",
            (~unavailable) & (np.abs(g("zc_div") - (spot - fut)) > 1e-6 * np.maximum(np.abs(fut) + np.abs(spot), 1)))
        if "spot_flow_source" in master:
            add("zc_div_unavailable_zero", "zc_div must be 0 when spot_flow_source=UNAVAILABLE",
                unavailable & (g("zc_div") != 0))

    if has("spot_close"):
        add("basis_identity", "basis_usd != close - spot_close", np.abs(g("basis_usd") - (c - g("spot_close"))) > 1e-6 * scale)
    add("basis_magnitude", "|basis| > price (misaligned spot)", np.abs(g("basis_usd")) > 1.0 * scale)

    fr = g("funding_rate_pct")
    add("funding_bounds", "funding_rate_pct outside Binance clamp [-3%, +3%]", np.abs(fr) > 3.0 + 1e-9)
    if fr.size > 1000 and 0 < float(np.percentile(np.abs(fr), 95)) < 1e-3:
        out.append(Finding(A, "funding_units", f"funding_rate_pct 95th percentile |x|={float(np.percentile(np.abs(fr), 95)):.2e}: looks like a raw decimal, not percent"))

    add("liq_polarity", "long_liq_usd must be <= 0 and short_liq_usd >= 0", (g("long_liq_usd") > 0) | (g("short_liq_usd") < 0))
    if has("liq_imbalance_ratio"):
        add("liq_imbalance_domain", "liq_imbalance_ratio outside [-1, 1]", np.abs(g("liq_imbalance_ratio")) > 1 + 1e-9)
    add("rsi_domain", "rsi_14 outside [0, 100]", (g("rsi_14") < 0) | (g("rsi_14") > 100))
    add("atr_nonneg", "ATR negative", (g("atr_14") < 0) | (g("atr_100") < 0))
    add("oi_change_domain", "oi_change_pct outside [-100, 100]", np.abs(g("oi_change_pct")) > 100 + 1e-9)
    add("oi_nonneg", "open interest negative", (g("open_interest_k") < 0) | (g("open_interest_usd") < 0))
    
    avail_mask = (master["metrics_available"].to_numpy() == 1) if "metrics_available" in master else (master["is_imputed_metrics"].to_numpy() == 0)
    add("oi_impossible_zero", "open_interest_k == 0 while metrics marked valid", avail_mask & (g("open_interest_k") == 0))
    add("ratios_positive", "L/S ratios must be > 0", (g("ls_ratio_global") <= 0) | (g("ls_ratio_top") <= 0) | (g("top_account_ratio") <= 0))
    if has("bid_depth_usd"):
        add("depth_positive", "depth proxies must be non-negative magnitudes",
            (g("bid_depth_usd") < 0) | (g("ask_depth_usd") < 0) | (g("bid_depth_coin") < 0) | (g("ask_depth_coin") < 0))
    add("value_area_order", "session_val > session_vah", g("session_val") > g("session_vah") + 1e-9)
    add("prev_va_order", "prev_day_val > prev_day_vah", g("prev_day_val") > g("prev_day_vah") + 1e-9)
    
    if has("fp_poc") and "poc_source" in master:
        add("poc_in_range", "fp_poc more than 0.5% outside [low, high] on tick-exact bars",
            (master["poc_source"].to_numpy() == "TICK_EXACT") & ((g("fp_poc") < l - 5e-3 * scale) | (g("fp_poc") > h + 5e-3 * scale)))
        add("poc_in_range_approx", "fp_poc outside [low, high] on OHLC-approximated bars",
            (master["poc_source"].to_numpy() == "OHLC_APPROX") & ((g("fp_poc") < l - 1e-6 * scale) | (g("fp_poc") > h + 1e-6 * scale)))

    # Re-derivations: a stored series can only match the causal recomputation if it used no future data.
    if has("session_vwap"):
        vwap = compute_session_vwap(ts, h, l, c, vb)
        add("vwap_rederive", "session_vwap != causal re-derivation from OHLCV", np.abs(g("session_vwap") - vwap) > 1e-6 * scale + 1e-6)
        add("vwap_in_range", "session_vwap outside session running [min low, max high] envelope",
            (g("session_vwap") < pd.Series(l).groupby(ts // 86_400_000).cummin().to_numpy() - 1e-6 * scale) |
            (g("session_vwap") > pd.Series(h).groupby(ts // 86_400_000).cummax().to_numpy() + 1e-6 * scale))
    for p in (8, 21):
        ema = g(f"ema_{p}")
        k = 2.0 / (p + 1.0)
        rec = np.empty_like(ema)
        rec[0] = ema[0]
        rec[1:] = c[1:] * k + ema[:-1] * (1.0 - k)
        add(f"ema_{p}_recursion", f"ema_{p} violates one-step recursion (stored value used other inputs)",
            np.abs(ema - rec) > 5e-8 * scale + 1e-8)
    # lookahead probe on session accumulators: first bar of each day must equal the bar's own delta / TP
    day = ts // 86_400_000
    first = np.append(True, np.diff(day) != 0)
    add("session_reset", "session CVD did not reset at 00:00 UTC", first & (np.abs(g("future_cvd_session") - fut) > 1e-6 * np.maximum(np.abs(fut), 1)))

    if ladder is not None and len(ladder):
        lts = ladder["open_time_ms"].to_numpy(np.int64)
        poc_per = ladder.groupby("open_time_ms")["is_poc"].sum()
        bad_poc = poc_per[poc_per != 1]
        if len(bad_poc):
            t = int(bad_poc.index[0])
            out.append(Finding(A, "ladder_poc", "candle must have exactly one POC rung", None, t,
                               str(pd.to_datetime(t, unit="ms", utc=True)), int(len(bad_poc))))
        bid, ask = ladder["bid_vol_coin"].to_numpy(np.float64), ladder["ask_vol_coin"].to_numpy(np.float64)
        neg = (bid < 0) | (ask < 0)
        if neg.any():
            i = int(np.flatnonzero(neg)[0])
            out.append(Finding(A, "ladder_neg_vol", "negative rung volume", None, int(lts[i]), str(pd.to_datetime(lts[i], unit="ms", utc=True)), int(neg.sum())))
        nd = ladder["net_delta_coin"].to_numpy(np.float64)
        bad_nd = np.abs(nd - (ask - bid)) > 1e-6 * np.maximum(ask + bid, 1)
        if bad_nd.any():
            i = int(np.flatnonzero(bad_nd)[0])
            out.append(Finding(A, "ladder_delta", "net_delta_coin != ask - bid", None, int(lts[i]), str(pd.to_datetime(lts[i], unit="ms", utc=True)), int(bad_nd.sum())))
        pos_price = ladder["price_bin"].to_numpy(np.float64) <= 0
        if pos_price.any():
            i = int(np.flatnonzero(pos_price)[0])
            out.append(Finding(A, "ladder_price", "non-positive price_bin", None, int(lts[i]), str(pd.to_datetime(lts[i], unit="ms", utc=True)), int(pos_price.sum())))
        # volume conservation vs Table 1: sum of rungs == taker_buy + taker_sell of the candle
        # (tick-exact bars carry the tick totals in Table 1; synthetic rungs are spread from the same split)
        sums = ladder.groupby("open_time_ms")[["bid_vol_coin", "ask_vol_coin"]].sum()
        m_idx = pd.Index(ts)
        pos = m_idx.get_indexer(sums.index)
        ok = pos >= 0
        tot_ladder = (sums["bid_vol_coin"] + sums["ask_vol_coin"]).to_numpy()[ok]
        tot_master = (tb + tsell)[pos[ok]]
        tol = 1e-6 * np.maximum(tot_master, 1.0) + 1e-6
        bad = np.abs(tot_ladder - tot_master) > tol
        if bad.any():
            j = int(np.flatnonzero(bad)[0])
            t = int(sums.index[ok][j])
            out.append(Finding(A, "ladder_volume_conservation", f"ladder volume {tot_ladder[j]:.8f} != taker_buy+taker_sell {tot_master[j]:.8f}",
                               int(pos[ok][j]), t, str(pd.to_datetime(t, unit="ms", utc=True)), int(bad.sum())))
        ask_sum = sums["ask_vol_coin"].to_numpy()[ok]
        bad_side = np.abs(ask_sum - tb[pos[ok]]) > tol
        if bad_side.any():
            j = int(np.flatnonzero(bad_side)[0])
            t = int(sums.index[ok][j])
            out.append(Finding(A, "ladder_side_conservation", f"ladder ask volume {ask_sum[j]:.8f} != taker_buy_vol_btc {tb[pos[ok]][j]:.8f}",
                               int(pos[ok][j]), t, str(pd.to_datetime(t, unit="ms", utc=True)), int(bad_side.sum())))
        flags = ladder[[c for c in ("is_buy_imbalance", "is_sell_imbalance", "is_poc", "rung_source") if c in ladder]].to_numpy()
        if not np.isin(flags, (0, 1)).all():
            out.append(Finding(A, "ladder_flags", "flag columns must be in {0, 1}"))
    return out


# ==============================================================================
# Agent 3 -- Zero-Null & Schema
# ==============================================================================
def _available_mask(master: pd.DataFrame) -> np.ndarray:
    """Bars the export discloses as carrying official metrics (all bars for legacy files)."""
    if "is_imputed_metrics" in master:
        return master["is_imputed_metrics"].to_numpy() == 0
    if "metrics_available" in master:
        return master["metrics_available"].to_numpy() == 1
    return np.ones(len(master), dtype=bool)


def metrics_coverage_report(master: pd.DataFrame) -> Dict[str, object]:
    """
    Why the regime scan skipped a year, in one dict.

    A Finding is always a rejection in this council (there is no severity), so a
    legitimate pre-archive absence cannot be reported as a soft warning from
    ``agent_schema``. It is reported here instead, so that "no findings" is never
    mistaken for "nothing was skipped".
    """
    rep: Dict[str, object] = {}
    if "open_time_ms" not in master or not len(master):
        return rep
    ts = master["open_time_ms"].to_numpy(np.int64)
    years = pd.to_datetime(ts, unit="ms", utc=True).year
    avail = _available_mask(master)
    counts = {}
    for y in np.unique(years):
        ym = years == y
        counts[int(y)] = {"bars": int(ym.sum()), "available": int((ym & avail).sum())}
    rep["years"] = counts
    rep["skipped_years"] = sorted(
        y for y, d in counts.items()
        if d["bars"] >= 500 and d["available"] < REGIME_MIN_AVAIL_BARS
    )
    oi = master["open_interest_k"].to_numpy(np.float64) if "open_interest_k" in master else np.ones(len(master))
    holes = _runs_longer_than((~avail) & (np.abs(oi) < 1e-12), 1)
    interior = [r for r in holes if r[0] > 0 and r[1] < len(master)]
    rep["longest_interior_hole_bars"] = max((b - a for a, b in interior), default=0)
    rep["unavailable_prefix_bars"] = int(holes[0][1] - holes[0][0]) if holes and holes[0][0] == 0 else 0
    first = np.flatnonzero(avail)
    rep["metrics_first_available_utc"] = str(pd.to_datetime(ts[first[0]], unit="ms", utc=True)) if len(first) else None
    return rep


def _runs_longer_than(mask: np.ndarray, min_len: int) -> list:
    """Maximal True-runs of a boolean mask as (start, end_exclusive), longest-first by position."""
    idx = np.flatnonzero(np.asarray(mask, dtype=bool))
    if not len(idx):
        return []
    out = []
    for grp in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1):
        if len(grp) >= min_len:
            out.append((int(grp[0]), int(grp[-1]) + 1))
    return out


def _attested_absent_months(symbol: str, target_dir: Optional[str] = None) -> "set":
    """
    Months the *download* observed as having no metrics archive on data.binance.vision.

    Read out of the dataset manifest, where the fetcher records archive objects that returned
    404. Non-circular by construction: it is an observation about the source, never derived
    from the assembled frame, so a parse or join bug that silently empties a month cannot
    attest itself. A missing field (legacy manifest) means "no exemption available".
    """
    if not symbol:
        return set()
    path = os.path.join(target_dir or DEFAULT_TARGET, f"{symbol}_dataset_manifest.json")
    try:
        with open(path, encoding="utf-8") as fh:
            man = json.load(fh)
    except Exception:
        return set()
    return {str(m)[:7] for m in ((man.get("provenance") or {}).get("metrics_archive_absent_months") or [])}


def agent_schema(master: pd.DataFrame, ladder: Optional[pd.DataFrame], attested_months: Optional[set] = None) -> List[Finding]:
    A = "Agent3:Schema"
    out: List[Finding] = []
    ts = master["open_time_ms"].to_numpy(np.int64) if "open_time_ms" in master else np.array([], dtype=np.int64)

    cols = list(master.columns)
    if cols != CANONICAL_COLUMNS:
        missing = [c for c in CANONICAL_COLUMNS if c not in cols]
        extra = [c for c in cols if c not in CANONICAL_COLUMNS]
        legacy_ok = cols[:len(CANONICAL_COLUMNS)] == CANONICAL_COLUMNS
        if missing or extra or not legacy_ok:
            out.append(Finding(A, "columns", f"column contract violated: missing={missing} extra={extra} order_ok={legacy_ok}"))
    for col, dt in COLUMN_DTYPES.items():
        if col not in master:
            continue
        actual = str(master[col].dtype)
        ok = (actual == dt) or (dt == "string" and actual in ("object", "string", "str", "string[python]", "string[pyarrow]", "large_string[pyarrow]"))
        if not ok:
            out.append(Finding(A, "dtype", f"{col}: expected {dt}, found {actual}"))
    nulls = master.isna()
    if nulls.to_numpy().any():
        col = nulls.sum().idxmax()
        f = _finding(A, "nulls", f"null values (first column: {col})", nulls.any(axis=1).to_numpy(), ts)
        if f:
            out.append(f)
    num = master.select_dtypes(include=[np.number])
    if len(num.columns):
        arr = num.to_numpy(dtype=np.float64)
        inf = ~np.isfinite(arr)
        if inf.any():
            col = num.columns[int(np.flatnonzero(inf.any(axis=0))[0])]
            f = _finding(A, "non_finite", f"inf/-inf values (first column: {col})", inf.any(axis=1), ts)
            if f:
                out.append(f)
    for col, vocab in STRING_VOCAB.items():
        if col in master:
            bad = ~master[col].isin(vocab).to_numpy()
            f = _finding(A, "vocab", f"{col} outside {vocab}", bad, ts)
            if f:
                out.append(f)
    for col in ("is_synthetic", "metrics_available", "is_imputed_metrics", "is_warmup_converged"):
        if col in master:
            bad = ~master[col].isin((0, 1)).to_numpy()
            f = _finding(A, "flag_domain", f"{col} must be 0/1", bad, ts)
            if f:
                out.append(f)
    if "is_imputed_metrics" in master and "metrics_available" in master:
        bad_impute = (master["is_imputed_metrics"].to_numpy() != (master["metrics_available"].to_numpy() == 0))
        f = _finding(A, "imputed_contract", "is_imputed_metrics != (metrics_available == 0)", bad_impute, ts)
        if f:
            out.append(f)
    if "symbol" in master and master["symbol"].nunique() != 1:
        out.append(Finding(A, "symbol", "more than one symbol in a master file"))
    for col in num.columns:
        if col in ALLOWED_CONSTANT_COLUMNS:
            continue
        if len(master) > 1000 and master[col].nunique() <= 1:
            out.append(Finding(A, "dead_feature", f"{col} is constant across {len(master):,} bars"))
    # Regime-split dead feature scan: catch partially-available metrics where a feature is constant
    # over a calendar year (or substantial regime) while varying elsewhere in the file.
    if len(master) > 1000 and "open_time_ms" in master and len(ts):
        years = pd.to_datetime(ts, unit="ms", utc=True).year
        metric_cols = ("open_interest_k", "ls_ratio_global", "ls_ratio_top", "top_account_ratio", "whale_index", "oi_change_pct")
        avail = _available_mask(master)
        months = pd.to_datetime(ts, unit="ms", utc=True).strftime("%Y-%m")
        if attested_months is None:
            attested_months = _attested_absent_months(
                str(master["symbol"].iloc[0]) if "symbol" in master else "")
        attested_bar = np.isin(months, sorted(attested_months)) if attested_months else np.zeros(len(master), bool)
        avail_nu = {c: master.loc[avail, c].nunique() for c in metric_cols if c in master}
        for y in np.unique(years):
            y_mask = (years == y)
            a_mask = y_mask & avail
            if int(a_mask.sum()) < REGIME_MIN_AVAIL_BARS:
                # A year with (almost) no metrics is legitimate ONLY when Binance never
                # published the archive for it. The availability flag cannot decide that -- it
                # is the very field this scan exists to audit -- so the exemption is granted on
                # the download inventory alone, and an unattested gap stays a rejection.
                if int(y_mask.sum()) >= REGIME_MIN_AVAIL_BARS:
                    need = set(np.unique(months[y_mask]))
                    unattested = need - set(attested_months or set())
                    if unattested:
                        f = _finding(A, "metrics_coverage_unattested",
                                     f"year {int(y)} has {int(y_mask.sum()) - int(a_mask.sum()):,}/{int(y_mask.sum()):,} bars "
                                     f"with no metrics, and the download did not attest {len(unattested)} of its months "
                                     f"({', '.join(sorted(unattested)[:3])}...) as absent from the Binance Vision archive: "
                                     f"pre-archive absence and fabricated coverage cannot be told apart inside the file",
                                     y_mask & ~avail, ts)
                        if f:
                            out.append(f)
                continue
            for col in metric_cols:
                if col in master:
                    y_nu = master.loc[a_mask, col].nunique()
                    total_nu = avail_nu[col]
                    if y_nu <= 1 and total_nu > 1:
                        out.append(Finding(A, "regime_dead_feature",
                                           f"{col} is constant (nunique={y_nu}) across the {int(a_mask.sum()):,} bars "
                                           f"carrying metrics in year {int(y)} despite total nunique={total_nu} "
                                           f"(partially fabricated metrics)"))
    # metrics_interior_hole: a long stretch with no metrics content at all, in the middle of
    # the history (or at its head) that the download inventory does not attest as absent. Legitimate pre-archive absence is a contiguous prefix (Binance Vision
    # starts ETHUSDT metrics on 2021-12); a hole after data has begun flowing is a failed
    # download. Without this, conditioning the scan above on metrics_available would let a
    # lost month pass simply because it was honestly marked unavailable.
    if len(master) > 1000 and "open_time_ms" in master and "open_interest_k" in master:
        empty = ((~_available_mask(master)) & (~attested_bar) &
                 (np.abs(master["open_interest_k"].to_numpy(np.float64)) < 1e-12))
        interior = [r for r in _runs_longer_than(empty, METRICS_INTERIOR_HOLE_BARS + 1)
                    if r[0] > 0 and r[1] < len(master)]
        if interior:
            a, b = max(interior, key=lambda r: r[1] - r[0])
            bad = np.zeros(len(master), dtype=bool)
            bad[a:b] = True
            f = _finding(A, "metrics_interior_hole",
                         f"{b - a:,} consecutive bars with no metrics content in the interior of the "
                         f"history (failed archive download, not a pre-archive gap)", bad, ts)
            if f:
                out.append(f)
    # precision collapse: a price-scale feature must not be quantised coarser than the asset trades
    if len(master) > 1000:
        close_nu = master["close"].nunique()
        for col in ("ema_8", "atr_14"):
            if col in master and master[col].nunique() < max(50, close_nu * 0.01):
                out.append(Finding(A, "precision_collapse", f"{col} has only {master[col].nunique()} distinct values vs {close_nu} distinct closes"))
        # basis_usd is a bounded *spread*, not a price level: its distinct count is capped by
        # (band width / asset tick), so it is uncorrelated with close cardinality and must not
        # be judged against it. What genuinely signals a broken basis is collapse onto a single
        # value, i.e. spot fabricated from the futures close (basis ≡ 0) or a stale spot join.
        if "basis_usd" in master:
            bser = pd.Series(np.round(master["basis_usd"].to_numpy(np.float64), 8))
            vc = bser.value_counts()
            mode_share = float(vc.iloc[0]) / len(bser) if len(vc) else 1.0
            if len(vc) < BASIS_MIN_DISTINCT or mode_share >= BASIS_MODAL_SHARE_MAX:
                out.append(Finding(A, "precision_collapse",
                                   f"basis_usd collapsed: {len(vc)} distinct values, modal value covers "
                                   f"{mode_share:.1%} of bars (spot may be fabricated from futures close)"))
        # value area is bucket-quantised by design; it collapses only if the bucket dwarfs the traded range
        if "session_vah" in master:
            rng = float(master["high"].max() - master["low"].min())
            bucket = get_merge_level(str(master["symbol"].iloc[0]))
            if rng > 0 and master["session_vah"].nunique() < min(50, max(2, rng / bucket * 0.05)):
                out.append(Finding(A, "precision_collapse", f"session_vah has only {master['session_vah'].nunique()} distinct values over a {rng / bucket:.0f}-bucket range"))

    if ladder is not None:
        lcols = list(ladder.columns)
        if lcols != LADDER_COLUMNS:
            out.append(Finding(A, "ladder_columns", f"ladder columns {lcols} != {LADDER_COLUMNS}"))
        for col, dt in LADDER_DTYPES.items():
            if col in ladder and str(ladder[col].dtype) != dt:
                out.append(Finding(A, "ladder_dtype", f"{col}: expected {dt}, found {ladder[col].dtype}"))
        if ladder.isna().to_numpy().any():
            out.append(Finding(A, "ladder_nulls", "ladder contains nulls"))
        lnum = ladder.select_dtypes(include=[np.number]).to_numpy(dtype=np.float64)
        if lnum.size and not np.isfinite(lnum).all():
            out.append(Finding(A, "ladder_non_finite", "ladder contains inf"))
        if "trade_count" in ladder and (ladder["trade_count"] < 0).any():
            out.append(Finding(A, "ladder_trade_count", "negative trade_count"))
    return out


# ==============================================================================
# Council
# ==============================================================================
AGENTS: Dict[str, Callable[[pd.DataFrame, Optional[pd.DataFrame]], List[Finding]]] = {
    "Agent1:Continuity": agent_continuity,
    "Agent2:Microstructure": agent_microstructure,
    "Agent3:Schema": agent_schema,
}


def run_council(master: pd.DataFrame, ladder: Optional[pd.DataFrame], symbol: str, log: Callable[[str], None] = print,
                attested_months: Optional[set] = None,
                expected_start_ms: Optional[int] = None,
                expected_end_ms: Optional[int] = None) -> CouncilReport:
    report = CouncilReport(symbol=symbol, passed=True, master_rows=len(master), ladder_rows=len(ladder) if ladder is not None else 0)
    for name, fn in AGENTS.items():
        try:
            if name == "Agent3:Schema":
                findings = fn(master, ladder, attested_months=attested_months)
            elif name == "Agent1:Continuity":
                findings = fn(master, ladder, expected_start_ms=expected_start_ms, expected_end_ms=expected_end_ms)
            else:
                findings = fn(master, ladder)
        except Exception as exc:  # an agent crash is itself a failure
            findings = [Finding(name, "exception", f"{type(exc).__name__}: {exc}")]
        report.findings.extend(findings)
        report.agent_status[name] = "PASS" if not findings else f"FAIL ({len(findings)})"
        if findings:
            report.passed = False
    log(f"[COUNCIL] {symbol}: " + " | ".join(f"{k.split(':')[1]}={v}" for k, v in report.agent_status.items()))
    for f in report.findings[:25]:
        log(f"  -> {f}")
    if len(report.findings) > 25:
        log(f"  -> ... {len(report.findings) - 25} more finding(s)")
    return report


def verify_symbol(target_dir: str, symbol: str, log: Callable[[str], None] = print) -> CouncilReport:
    mpath = os.path.join(target_dir, master_filename(symbol))
    lpath = os.path.join(target_dir, ladder_filename(symbol))
    ppath = os.path.join(target_dir, manifest_filename(symbol))

    if not os.path.exists(mpath):
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "missing_master", f"{mpath} not found")], {})
    if not os.path.exists(lpath):
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "missing_ladder", f"{lpath} not found")], {})

    # Manifest is mandatory for artifact certification
    if not os.path.exists(ppath):
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "missing_manifest", f"Manifest {ppath} not found (manifest is mandatory for certification)")], {})

    try:
        with open(ppath, "r", encoding="utf-8") as fh:
            mdata = json.load(fh)
    except Exception as exc:
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "unreadable_manifest", f"Manifest {ppath} unreadable or corrupt JSON: {exc}")], {})

    exp_start_ms = mdata.get("expected_start_ms")
    exp_end_ms = mdata.get("expected_end_ms")
    exp_rows = mdata.get("expected_rows")

    manifest_findings: List[Finding] = []
    if exp_start_ms is None or not isinstance(exp_start_ms, int):
        manifest_findings.append(Finding("Council", "manifest_expected_start", f"expected_start_ms missing or not int: {exp_start_ms!r}"))
    if exp_end_ms is None or not isinstance(exp_end_ms, int):
        manifest_findings.append(Finding("Council", "manifest_expected_end", f"expected_end_ms missing or not int: {exp_end_ms!r}"))
    if exp_rows is None or not isinstance(exp_rows, int):
        manifest_findings.append(Finding("Council", "manifest_expected_rows", f"expected_rows missing or not int: {exp_rows!r}"))

    if isinstance(exp_start_ms, int) and isinstance(exp_end_ms, int) and isinstance(exp_rows, int):
        calc_exp_first = (exp_start_ms // BAR_MS) * BAR_MS
        calc_exp_last = (exp_end_ms // BAR_MS) * BAR_MS
        calc_rows = int(((calc_exp_last - calc_exp_first) // BAR_MS) + 1)
        if exp_rows != calc_rows:
            manifest_findings.append(Finding("Council", "manifest_rows_inconsistent",
                                             f"manifest expected_rows ({exp_rows}) != calculated from expected_start/end ({calc_rows})"))

    try:
        master = pd.read_parquet(mpath)
        ladder = pd.read_parquet(lpath)
    except Exception as exc:
        return CouncilReport(symbol, False, 0, 0, [Finding("Council", "unreadable_parquet", f"Failed to read parquet: {exc}")], {})

    if isinstance(exp_rows, int) and len(master) != exp_rows:
        manifest_findings.append(Finding("Council", "master_rows_mismatch",
                                         f"master length ({len(master)}) != manifest expected_rows ({exp_rows})"))

    attested = _attested_absent_months(symbol, target_dir)
    report = run_council(master, ladder, symbol, log, attested_months=attested,
                         expected_start_ms=exp_start_ms if isinstance(exp_start_ms, int) else None,
                         expected_end_ms=exp_end_ms if isinstance(exp_end_ms, int) else None)

    if manifest_findings:
        report.findings.extend(manifest_findings)
        report.passed = False
        report.agent_status["Council:ManifestContract"] = f"FAIL ({len(manifest_findings)})"

    return report


def verify_all_parquets(target_dir: str = DEFAULT_TARGET, symbols: Optional[List[str]] = None, log: Callable[[str], None] = print) -> bool:
    log("=" * 96)
    log("AUTONOMOUS 3-AGENT VERIFICATION COUNCIL")
    log(f"Target: {target_dir}")
    log("=" * 96)
    if not os.path.isdir(target_dir):
        log(f"[FAIL] target directory missing: {target_dir}")
        return False
    if symbols is None:
        symbols = sorted(os.path.basename(p).split("_15m_master")[0] for p in glob.glob(os.path.join(target_dir, "*_15m_master_2020_2026.parquet")))
    if not symbols:
        log("[FAIL] no master parquet files found")
        return False
    all_ok, total_bars, total_rungs = True, 0, 0
    summary = {}
    for sym in symbols:
        rep = verify_symbol(target_dir, sym, log)
        total_bars += rep.master_rows
        total_rungs += rep.ladder_rows
        summary[sym] = rep.to_dict()
        all_ok &= rep.passed
        log(f"[{'PASS' if rep.passed else 'FAIL'}] {sym:<10} bars={rep.master_rows:>8,} rungs={rep.ladder_rows:>12,}")
    log("=" * 96)
    log(f"COUNCIL VERDICT: {'ALL DATASETS PASS' if all_ok else 'INTEGRITY FAILURES DETECTED'} | candles={total_bars:,} rungs={total_rungs:,}")
    log("=" * 96)
    with open(os.path.join(target_dir, "verification_report.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    return all_ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="3-Agent Parquet Verification Council")
    ap.add_argument("target_dir", nargs="?", default=DEFAULT_TARGET)
    ap.add_argument("--symbol", action="append", help="verify only this symbol (repeatable)")
    args = ap.parse_args()
    sys.exit(0 if verify_all_parquets(args.target_dir, args.symbol) else 1)
