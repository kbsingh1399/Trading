"""Dataset assembly for the levels / POC lab.

Loads the shipped Binance USDT-M 15m master tables, adds causal level and
volume-profile features, and caches the *derived* feature tables (not the raw
data) so that repeated research runs are cheap.

Paths are repository-relative: ``Engine/binance_backtesting_data``.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from . import BAR_MS
from .levels import build_levels, build_profile, ladder_poc_frame, validate_profile

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "Engine" / "binance_backtesting_data"
WINDOWS_PATH = REPO_ROOT / "Engine" / "oos_windows_20.json"
CRITERIA_PATH = REPO_ROOT / "Engine" / "target_oos_criteria.json"
CACHE_DIR = Path(os.environ.get("LPL_CACHE", "/tmp/lpl_cache"))

BTC = "BTCUSDT"
ALTCOINS = tuple(
    x + "USDT"
    for x in (
        "ETH", "XRP", "SOL", "BNB", "DOGE", "ADA", "TRX", "LINK", "AVAX",
        "SUI", "NEAR", "DOT", "LTC", "BCH", "APT", "OP", "ARB",
    )
)
ALL_SYMBOLS = (BTC,) + ALTCOINS

MASTER_COLUMNS = [
    "open_time_ms", "open", "high", "low", "close", "volume_base", "volume_quote",
    "trade_count", "rsi_14", "atr_14", "atr_100", "ema_21", "ema_50", "ema_200", "ema_800",
    "future_cvd_15m", "spot_cvd_15m", "funding_rate_pct", "basis_usd", "taker_volume_ratio",
    "long_liq_zs", "short_liq_zs", "zc_div", "volume_ratio", "open_interest_usd",
    "avg_trade_size_usd", "session_vah", "session_val", "prev_day_vah", "prev_day_val",
]

LEVEL_COLUMNS = [
    "pdh", "pdl", "pdc", "pwh", "pwl", "pmh", "pml", "pqh", "pql", "ath", "bars_since_ath",
    "ath_dist", "day_open", "week_open", "month_open",
    "dev_poc", "dev_vah", "dev_val", "dev_lvn", "dev_share", "poc_delta",
    "prior_poc", "prior_vah", "prior_val", "prior_poc_low", "prior_poc_high", "sess_vwap",
]


def master_path(symbol: str) -> Path:
    return DATA_DIR / f"{symbol}_15m_master_2020_2026.parquet"


def ladder_path(symbol: str) -> Path:
    return DATA_DIR / f"{symbol}_15m_footprint_ladder.parquet"


def _rma(values: pd.Series, period: int) -> pd.Series:
    """Wilder RMA, matching the pipeline's canonical kernel."""
    if len(values) <= period:
        return values.expanding().mean()
    head = values.iloc[: period - 1].expanding().mean()
    tail = values.iloc[period - 1:].copy()
    tail.iloc[0] = values.iloc[:period].mean()
    return pd.concat([head, tail.ewm(alpha=1 / period, adjust=False).mean()])


def build_symbol_features(symbol: str, bin_width: float = 0.0005) -> pd.DataFrame:
    """Causal level + profile + regime features for one symbol."""
    cols = [c for c in MASTER_COLUMNS]
    f = pq.read_table(master_path(symbol), columns=cols).to_pandas()
    f = f.sort_values("open_time_ms").reset_index(drop=True)
    t = f.open_time_ms.to_numpy(np.int64)
    if len(t) > 1 and not np.all(np.diff(t) == BAR_MS):
        # Binance listings occasionally miss bars; reindex onto the full grid so
        # that "previous period" logic stays honest, then forward-fill nothing.
        raise ValueError(f"{symbol}: master timestamps are not a contiguous 15m grid")

    f = build_levels(f)
    f = build_profile(f, bin_width=bin_width)

    c = f.close
    h, lo = f.high, f.low
    tr = pd.concat([h - lo, (h - c.shift()).abs(), (lo - c.shift()).abs()], axis=1).max(axis=1)
    f["atr"] = _rma(tr, 14)
    f["atr100"] = _rma(tr, 100)
    f["atr_ratio"] = (f.atr / f.atr100.replace(0, np.nan)).clip(0.2, 5.0)

    v = f.volume_base
    f["volume_rel"] = (v / v.shift(1).rolling(96, min_periods=48).mean()).fillna(1.0)
    f["flow"] = f.future_cvd_15m.fillna(0.0)
    f["flow_ratio"] = (f.flow / v.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    f["flow4"] = f.flow.rolling(4, min_periods=1).sum() / v.rolling(4, min_periods=1).sum().replace(0, np.nan)
    f["flow4"] = f.flow4.fillna(0.0)
    f["e200"] = f.ema_200
    f["slope200"] = (f.e200 - f.e200.shift(96)) / f.atr.replace(0, np.nan)
    f["e200_4h"] = c.ewm(span=3200, adjust=False).mean()
    f["slope200_4h"] = (f.e200_4h - f.e200_4h.shift(64)) / f.atr.replace(0, np.nan)
    f["trend_up"] = ((f.ema_50 > f.ema_200) & (f.e200 > f.ema_800)).astype(np.int8)
    f["trend_dn"] = ((f.ema_50 < f.ema_200) & (f.e200 < f.ema_800)).astype(np.int8)
    f["ret_96"] = c.pct_change(96).fillna(0.0)
    f["ret_672"] = c.pct_change(672).fillna(0.0)

    # Realised-volatility regime (annualised, 24h window) and ATR z-score.
    r = np.log(c).diff()
    f["rv_24h"] = (r.rolling(96, min_periods=48).std() * np.sqrt(96 * 365)).fillna(0.0)
    av = (f.atr / c).fillna(0.0)
    prior = av.shift(1).rolling(1920, min_periods=480)
    f["atr_z"] = ((av - prior.mean()) / prior.std(ddof=0).replace(0, np.nan)).fillna(0.0)

    # Distance of price to each level, normalised by ATR (dimensionless).
    for name in ("pdh", "pdl", "pwh", "pwl", "pmh", "pml", "pqh", "pql", "ath",
                 "dev_poc", "dev_vah", "dev_val", "prior_poc", "prior_vah", "prior_val",
                 "prior_poc_low", "prior_poc_high", "sess_vwap", "week_open", "month_open",
                 "dev_lvn", "pdc"):
        f[f"d_{name}"] = (c - f[name]) / f.atr.replace(0, np.nan)

    # Level events, all evaluated on the completed candle.
    f["brk_pwh"] = ((c > f.pwh) & (c.shift(1) <= f.pwh.shift(1))).astype(np.int8)
    f["brk_pwl"] = ((c < f.pwl) & (c.shift(1) >= f.pwl.shift(1))).astype(np.int8)
    f["brk_pmh"] = ((c > f.pmh) & (c.shift(1) <= f.pmh.shift(1))).astype(np.int8)
    f["brk_pml"] = ((c < f.pml) & (c.shift(1) >= f.pml.shift(1))).astype(np.int8)
    f["brk_pdh"] = ((c > f.pdh) & (c.shift(1) <= f.pdh.shift(1))).astype(np.int8)
    f["brk_pdl"] = ((c < f.pdl) & (c.shift(1) >= f.pdl.shift(1))).astype(np.int8)
    f["brk_ath"] = ((c > f.ath) & (c.shift(1) <= f.ath.shift(1))).astype(np.int8)
    f["sweep_pwh"] = ((h > f.pwh) & (c < f.pwh)).astype(np.int8)
    f["sweep_pwl"] = ((lo < f.pwl) & (c > f.pwl)).astype(np.int8)
    f["sweep_pmh"] = ((h > f.pmh) & (c < f.pmh)).astype(np.int8)
    f["sweep_pml"] = ((lo < f.pml) & (c > f.pml)).astype(np.int8)
    f["sweep_pdh"] = ((h > f.pdh) & (c < f.pdh)).astype(np.int8)
    f["sweep_pdl"] = ((lo < f.pdl) & (c > f.pdl)).astype(np.int8)
    f["sweep_ath"] = ((h > f.ath) & (c < f.ath)).astype(np.int8)

    # POC interaction events (completed candle crossing the developing POC).
    above = c > f.dev_poc
    f["poc_reclaim_up"] = (above & (~above.shift(1).fillna(False).astype(bool))).astype(np.int8)
    f["poc_reclaim_dn"] = ((~above) & (above.shift(1).fillna(False).astype(bool))).astype(np.int8)
    f["in_value_area"] = ((c <= f.dev_vah) & (c >= f.dev_val)).astype(np.int8)
    f["above_vah"] = (c > f.dev_vah).astype(np.int8)
    f["below_val"] = (c < f.dev_val).astype(np.int8)
    f["poc_mig_up"] = ((f.poc_delta > 0) & (c > f.dev_poc)).astype(np.int8)
    f["poc_mig_dn"] = ((f.poc_delta < 0) & (c < f.dev_poc)).astype(np.int8)

    # Causal rolling z-score of distance to the developing POC.
    dz = f["d_dev_poc"]
    m = dz.rolling(192, min_periods=48).mean()
    s = dz.rolling(192, min_periods=48).std(ddof=0).replace(0, np.nan)
    f["z_dev_poc"] = ((dz - m) / s).fillna(0.0)
    f["symbol"] = symbol
    return f


def load_all(symbols=ALL_SYMBOLS, cache: bool = True, rebuild: bool = False,
             bin_width: float = 0.0005) -> dict[str, pd.DataFrame]:
    """Load (and cache) derived feature tables per symbol."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    out: dict[str, pd.DataFrame] = {}
    tag = f"bw{bin_width:.5f}"
    for s in symbols:
        path = CACHE_DIR / f"{s}_{tag}.parquet"
        if cache and path.exists() and not rebuild:
            f = pd.read_parquet(path)
        else:
            f = build_symbol_features(s, bin_width=bin_width)
            if cache:
                keep = f.copy()
                for col in keep.columns:
                    if keep[col].dtype == np.float64:
                        keep[col] = keep[col].astype(np.float32)
                keep.to_parquet(path, index=False)
        f = attach_flow(f, s)
        out[s] = f
    return out


def attach_flow(f: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Merge the (optional) order-flow feature table onto a symbol's feature frame.

    ``flow.load_flow`` caches one small parquet per symbol built from the shipped
    footprint ladder; if it has not been built yet the frame is returned unchanged
    so every existing code path keeps working.
    """
    from .flow import FLOW_COLUMNS, flow_path

    if not flow_path(symbol).exists() or FLOW_COLUMNS[0] in f.columns:
        return f
    flow = pd.read_parquet(flow_path(symbol))
    if len(flow) == len(f) and np.array_equal(flow.open_time_ms.to_numpy(), f.open_time_ms.to_numpy()):
        out = f.copy()
        for c in FLOW_COLUMNS:
            out[c] = flow[c].to_numpy("float32")
        return out
    return f.merge(flow, on="open_time_ms", how="left")


def windows() -> list[dict]:
    with open(WINDOWS_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def criteria() -> dict:
    with open(CRITERIA_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)["target_criteria"]


def window_bounds(w: dict) -> tuple[int, int]:
    start = int(pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000)
    end = int(pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000)
    return start, end


def profile_validation(symbols=("BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT"), bin_width=0.0005) -> dict:
    """Audit the reconstructed profile against the shipped ladder POC."""
    rep = {}
    for s in symbols:
        m = pq.read_table(
            master_path(s), columns=["open_time_ms", "high", "low", "close", "volume_base"]
        ).to_pandas()
        rep[s] = validate_profile(m, ladder_path(s), bin_width=bin_width)
    return rep


if __name__ == "__main__":
    rep = profile_validation()
    print(json.dumps(rep, indent=2))
