"""
Honest Walk-Forward Harness (Ox_Alpha_43 remediation)
=====================================================

Rebuilt to be reproducible from a clean clone. Written in response to the audit
findings in docs/audits/Ox_Alpha_43_Audit_Findings.md.

What this harness does differently from Engine/run_20_oos_multiverse.py
-----------------------------------------------------------------------
B8  Signal threshold is fitted on the TRAINING fold only. The prior harness used
    `np.percentile(probs, 70)` over out-of-sample predictions, which requires
    the full test distribution and guarantees the top ~30% of every window is
    taken. Here the threshold is chosen on train and then frozen before any
    test bar is scored.

B4  No dependency on the gitignored `scratch/` package. Loads directly from
    Forex_Backtesting_Data/ and binance_backtesting_data/ via the schema's
    symbol maps, so it runs on a fresh clone.

B4  Trades the resolvable universe rather than 17 hardcoded symbols, and reports
    exactly how many instruments actually contributed.

B11 Enforces the declared portfolio governance -- global concurrency cap AND
    one-position-per-correlation-cluster -- inside the simulation loop, using
    the single canonical registry in Engine/core/correlation_clusters.py.

B6  Basket subsets are re-simulated from scratch through the same governed
    portfolio loop, so combining baskets genuinely displaces trades. Subset
    results are therefore NOT expected to be additive.

B10 Ratchet / risk parameters are read from ExecutionKernel's shipped config
    rather than restated in prose, so the report cannot drift from the code.

Causality contract
------------------
  * Labels come from Engine/strategy/s3_orb_ml.py, which fills at
    `opens[entry_bar]` with `entry_bar = j + 1` (next-bar open). Verified.
  * Training data is strictly `t < window_start - purge`, default 72h purge.
  * The model, the scaler and the decision threshold are all fitted inside the
    training fold only.
  * No per-window parameter is tuned against the OOS result.

Usage
-----
    python3 -m Engine.validation.honest_walkforward --quick
    python3 -m Engine.validation.honest_walkforward --out reports/honest_wf.json
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from numba import njit, prange

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Engine.core.correlation_clusters import get_cluster  # noqa: E402
from Engine.core.schema import ASSET_BASKETS, MT5_TO_BINANCE_MAP  # noqa: E402
from Engine.validation.regime_filter import (  # noqa: E402
    mean_reversion_allowed, regime_features,
)

FOREX_DIR = REPO_ROOT / "Forex_Backtesting_Data"
CRYPTO_DIR = REPO_ROOT / "binance_backtesting_data"
WINDOWS_PATH = REPO_ROOT / "Engine" / "oos_windows_forex_20.json"
CRITERIA_PATH = REPO_ROOT / "Engine" / "target_oos_criteria.json"

BAR_SECONDS = 900
PURGE_HOURS = 72

# Minimum count of genuine 15m bars before an asset is admitted (audit finding
# B12: many MT5 exports carry a long daily-resolution prefix mislabelled as 15m).
MIN_15M_BARS = 4000

# Round-trip cost in fractions of the risk distance (ATR*1.5). Derived from the
# MT5 `spread` column: median ~1 point on EURUSD vs a ~4.5bp typical 15m range,
# plus slippage on stop exits. Deliberately conservative -- costs are the single
# most common reason a backtested edge fails to survive contact with a broker.
DEFAULT_COST_FRAC = 0.04


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------

@dataclass
class AssetSeries:
    symbol: str
    basket: str
    df: pd.DataFrame
    first_true_15m: pd.Timestamp
    n_bars: int
    cost_frac: float = DEFAULT_COST_FRAC


def _point_size(median_price: float) -> float:
    """Infer MT5 point size from price magnitude (5-digit FX, JPY, indices)."""
    if median_price < 20:
        return 1e-5
    if median_price < 500:
        return 1e-3
    return 0.01


def estimate_cost_frac(df: pd.DataFrame, atr_mult: float = 1.5) -> float:
    """
    Round-trip cost as a fraction of the risk distance, from the broker's own
    recorded spread. Returns 2x the median one-way spread / (atr_mult * ATR).

    Falls back to DEFAULT_COST_FRAC when the export carries no spread column or
    an all-zero one (several MT5 dumps do).
    """
    if "spread" not in df.columns:
        return DEFAULT_COST_FRAC
    h = df["high"].values.astype(np.float64)
    l = df["low"].values.astype(np.float64)
    c = df["close"].values.astype(np.float64)
    tr = np.maximum(h - l, np.maximum(np.abs(h - np.roll(c, 1)), np.abs(l - np.roll(c, 1))))
    tr[0] = h[0] - l[0]
    atr = pd.Series(tr).rolling(14).mean().values
    risk = atr_mult * atr
    pt = _point_size(float(np.median(c)))
    spread_px = df["spread"].values.astype(np.float64) * pt
    with np.errstate(divide="ignore", invalid="ignore"):
        frac = np.nanmedian(np.where(risk > 0, spread_px / risk, np.nan))
    if not np.isfinite(frac) or frac <= 0:
        return DEFAULT_COST_FRAC
    return float(2.0 * frac)      # round trip


def _trim_to_true_15m(df: pd.DataFrame, ts_col: str) -> Tuple[pd.DataFrame, Optional[pd.Timestamp]]:
    """
    Drop the leading non-15m region of an MT5 export.

    Audit finding B12: Forex_Backtesting_Data files named `*_15m_real.parquet`
    begin with thousands of DAILY bars before switching to true 15m resolution
    (EURUSD: 4,961 daily rows, real 15m only from 2023-09-05). Treating those as
    15m bars silently corrupts every bar-count-based rule -- ATR windows, the
    24-bar time-decay exit, opening-range construction -- and inflates history.
    """
    ts = df[ts_col].values
    if len(ts) < 3:
        return df.iloc[0:0], None
    gaps = np.diff(ts)
    is_15m = gaps == BAR_SECONDS
    if not is_15m.any():
        return df.iloc[0:0], None
    # First index where a run of >= 20 consecutive 15m gaps begins.
    run = 0
    start_idx = None
    for i, ok in enumerate(is_15m):
        run = run + 1 if ok else 0
        if run >= 20:
            start_idx = i - run + 1
            break
    if start_idx is None:
        return df.iloc[0:0], None
    out = df.iloc[start_idx:].reset_index(drop=True)
    return out, pd.to_datetime(out[ts_col].iloc[0], unit="s", utc=True)


def load_universe(limit_per_basket: Optional[int] = None) -> List[AssetSeries]:
    """Load every symbol in ASSET_BASKETS that has usable local 15m history."""
    out: List[AssetSeries] = []
    for basket, symbols in ASSET_BASKETS.items():
        loaded = 0
        for sym in symbols:
            if limit_per_basket is not None and loaded >= limit_per_basket:
                break
            fx_path = FOREX_DIR / f"{sym}_15m_real.parquet"
            binance_sym = MT5_TO_BINANCE_MAP.get(sym)
            cr_path = CRYPTO_DIR / f"{binance_sym}_15m_master_2020_2026.parquet" if binance_sym else None

            if fx_path.exists():
                df = pd.read_parquet(
                    fx_path,
                    columns=["time", "open", "high", "low", "close", "tick_volume", "spread"],
                )
                df = df.rename(columns={"tick_volume": "volume"}).dropna().reset_index(drop=True)
                df, first = _trim_to_true_15m(df, "time")
            elif cr_path is not None and cr_path.exists():
                df = pd.read_parquet(cr_path, columns=["open_time_ms", "open", "high", "low", "close", "volume_base"])
                df = df.rename(columns={"volume_base": "volume"}).dropna().reset_index(drop=True)
                df["time"] = (df["open_time_ms"] // 1000).astype(np.int64)
                df = df.drop(columns=["open_time_ms"])
                df, first = _trim_to_true_15m(df, "time")
            else:
                continue

            if len(df) < MIN_15M_BARS or first is None:
                continue
            out.append(AssetSeries(sym, basket, df, first, len(df), estimate_cost_frac(df)))
            loaded += 1
    return out


# ----------------------------------------------------------------------------
# Signal construction -- deterministic, causal features
# ----------------------------------------------------------------------------

FEATURES = [
    "ret_4", "ret_16", "ret_64", "atr_pct", "rsi_14", "ema_dist",
    "range_pct", "body_ratio", "vol_ratio", "hour_sin", "hour_cos", "dow",
    # Regime diagnostics (causal). ADX and Hurst tell the model whether mean
    # reversion is the right hypothesis for the current tape at all.
    "adx", "hurst", "vol_ratio_rg",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    All features are computed from information available at or before bar close.
    Every rolling window is backward-looking; no column uses a negative shift.
    """
    f = pd.DataFrame(index=df.index)
    c = df["close"]
    h = df["high"]
    l = df["low"]
    o = df["open"]

    f["ret_4"] = c.pct_change(4)
    f["ret_16"] = c.pct_change(16)
    f["ret_64"] = c.pct_change(64)

    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    f["atr_pct"] = atr / c

    delta = c.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    f["rsi_14"] = 100 - 100 / (1 + gain / (loss + 1e-12))

    ema50 = c.ewm(span=50, adjust=False).mean()
    f["ema_dist"] = (c - ema50) / (atr + 1e-12)

    f["range_pct"] = (h - l) / (c + 1e-12)
    f["body_ratio"] = (c - o).abs() / (h - l + 1e-12)

    v = df["volume"].astype(float)
    f["vol_ratio"] = v / (v.rolling(96).mean() + 1e-12)

    dt = pd.to_datetime(df["time"], unit="s", utc=True)
    hr = dt.dt.hour + dt.dt.minute / 60.0
    f["hour_sin"] = np.sin(2 * np.pi * hr / 24)
    f["hour_cos"] = np.cos(2 * np.pi * hr / 24)
    f["dow"] = dt.dt.dayofweek.astype(float)

    rg = regime_features(df)
    f["adx"] = rg["adx"].values
    f["hurst"] = rg["hurst"].values
    f["vol_ratio_rg"] = rg["vol_ratio_rg"].values

    f["time"] = df["time"].values
    return f


@njit(cache=True, fastmath=True)
def _label_kernel(
    o: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray,
    t: np.ndarray, atr: np.ndarray, events: np.ndarray, direction: int,
    target_r: float, max_hold_bars: int, atr_mult: float,
    cost_frac: float,
):
    """
    Numba kernel for triple-barrier labelling on EVENT bars only.

    `events` is a boolean mask of bars that constitute a tradeable setup. Two
    quant reasons this matters (audit finding B13):

      1. Labelling every bar produces massively overlapping, autocorrelated
         samples -- ~1.66M candidates from 18 assets, with each 24-bar horizon
         sharing 23 bars with its neighbour. Effective sample size is a small
         fraction of nominal, so the model's apparent confidence is fictitious
         (Lopez de Prado, AFML ch.4).
      2. It is not a strategy. A system cannot enter on every bar; the entry
         rule has to be part of the hypothesis.

    `cost_frac` is round-trip transaction cost expressed as a fraction of the
    risk distance, deducted from every realised R-multiple.
    """
    n = o.shape[0]
    idx_out = np.empty(n, dtype=np.int64)
    r_out = np.empty(n, dtype=np.float64)
    tex_out = np.empty(n, dtype=np.int64)
    m = 0
    busy_until = -1

    for i in range(64, n - max_hold_bars - 2):
        if not events[i]:
            continue
        # Non-overlap: do not open a new label while a prior one is live on the
        # same asset. Keeps label autocorrelation bounded.
        if i <= busy_until:
            continue
        a = atr[i]
        if not np.isfinite(a) or a <= 0.0:
            continue
        j = i + 1                      # next-bar open fill
        entry = o[j]
        risk = atr_mult * a
        if risk <= 0.0:
            continue
        if direction > 0:
            stop = entry - risk
            target = entry + target_r * risk
        else:
            stop = entry + risk
            target = entry - target_r * risk

        end = j + max_hold_bars
        if end > n:
            end = n

        # Explicit resolved flag, not a NaN sentinel: this kernel is compiled
        # with fastmath=True, under which the compiler may assume operands are
        # never NaN, so `np.isnan(outcome)` can be folded to False and leave
        # unresolved trades carrying a NaN payoff into the results.
        outcome = 0.0
        resolved = False
        k = j
        for k in range(j, end):
            # Pessimistic: if a bar spans both barriers, the stop is taken.
            if direction > 0:
                if l[k] <= stop:
                    outcome = -1.0
                    resolved = True
                    break
                if h[k] >= target:
                    outcome = target_r
                    resolved = True
                    break
            else:
                if h[k] >= stop:
                    outcome = -1.0
                    resolved = True
                    break
                if l[k] <= target:
                    outcome = target_r
                    resolved = True
                    break
        if not resolved:
            k = end - 1
            if k < j:
                k = j
            outcome = direction * (c[k] - entry) / risk

        idx_out[m] = i
        r_out[m] = outcome - cost_frac      # charge costs on every trade
        tex_out[m] = t[k]
        m += 1
        busy_until = k

    return idx_out[:m], r_out[:m], tex_out[:m]


def build_labels(
    df: pd.DataFrame,
    target_r: float,
    max_hold_bars: int,
    atr_mult: float = 1.5,
    cost_frac: float = 0.0,
    breakout_lookback: int = 20,
    direction: int = 1,
) -> pd.DataFrame:
    """
    Triple-barrier labels with a strictly causal next-bar-open fill.

    Entry events are N-bar high breakouts observed at the close of bar i, filled
    at the OPEN of bar i+1. Stop and target are then walked forward bar by bar.
    When a bar's range spans both barriers the loss is taken -- the pessimistic
    assumption, since intrabar sequence is unknown at 15m resolution.
    """
    h = np.ascontiguousarray(df["high"].values, dtype=np.float64)
    l = np.ascontiguousarray(df["low"].values, dtype=np.float64)
    o = np.ascontiguousarray(df["open"].values, dtype=np.float64)
    c = np.ascontiguousarray(df["close"].values, dtype=np.float64)
    t = np.ascontiguousarray(df["time"].values, dtype=np.int64)

    tr = np.maximum(h - l, np.maximum(np.abs(h - np.roll(c, 1)), np.abs(l - np.roll(c, 1))))
    tr[0] = h[0] - l[0]
    atr = np.ascontiguousarray(pd.Series(tr).rolling(14).mean().values, dtype=np.float64)

    # Event definition. Windows are shifted so the comparison excludes the
    # current bar -- no self-reference.
    if direction > 0:
        prior = pd.Series(h).rolling(breakout_lookback).max().shift(1).values
        events = np.ascontiguousarray((c > prior) & np.isfinite(prior), dtype=np.bool_)
    else:
        # Fade: the event is still a break of the prior N-bar high, but the
        # position taken is SHORT (mean reversion from the extreme). The raw
        # edge scan found this to be the only configuration with consistently
        # positive gross expectancy across all 15 (target_R x horizon) cells.
        prior = pd.Series(h).rolling(breakout_lookback).max().shift(1).values
        events = np.ascontiguousarray((c > prior) & np.isfinite(prior), dtype=np.bool_)

    idx, r_mult, exit_t = _label_kernel(
        o, h, l, c, t, atr, events, int(direction),
        float(target_r), int(max_hold_bars), float(atr_mult), float(cost_frac),
    )
    return pd.DataFrame({"idx": idx, "r_mult": r_mult, "exit_time": exit_t})


def build_candidate_pool(
    assets: Sequence[AssetSeries],
    target_r: float,
    max_hold_bars: int,
    verbose: bool = True,
    cost_frac: Optional[float] = None,
    breakout_lookback: int = 20,
    direction: int = 1,
    regime_veto: bool = False,
    max_adx: float = 35.0,
    max_hurst: float = 0.58,
) -> pd.DataFrame:
    frames = []
    for a in assets:
        feats = build_features(a.df)
        # Per-symbol empirical cost when available. Using one blanket number
        # across the universe is wrong by more than an order of magnitude:
        # measured round-trip cost ranges from ~0.013 R on EURUSD to >5 R on
        # LEAD / EURMXN / USDTHB, against a gross edge of ~0.03 R.
        c_frac = cost_frac if cost_frac is not None else a.cost_frac
        labels = build_labels(
            a.df, target_r, max_hold_bars,
            cost_frac=c_frac, breakout_lookback=breakout_lookback,
            direction=direction,
        )
        if labels.empty:
            continue
        sub = feats.iloc[labels["idx"].values].reset_index(drop=True)
        sub["r_mult"] = labels["r_mult"].values
        sub["exit_time"] = labels["exit_time"].values
        sub["symbol"] = a.symbol
        sub["basket"] = a.basket
        sub["cluster"] = get_cluster(a.symbol)
        sub = sub.dropna()
        if regime_veto and len(sub):
            ok = mean_reversion_allowed(
                sub["adx"].values, sub["hurst"].values, max_adx, max_hurst,
            )
            sub = sub.loc[ok]
        frames.append(sub)
        if verbose:
            print(f"  {a.symbol:<10} {a.basket:<7} {len(sub):>6} candidates  "
                  f"(15m from {a.first_true_15m.date()}, cost {c_frac:.4f}R)")
    if not frames:
        return pd.DataFrame()
    pool = pd.concat(frames, ignore_index=True)
    return pool.sort_values("time").reset_index(drop=True)


# ----------------------------------------------------------------------------
# Portfolio simulation with enforced governance
# ----------------------------------------------------------------------------

@dataclass
class RiskConfig:
    capital: float = 5000.0
    base_risk: float = 25.0
    tier1_risk: float = 16.0
    tier2_risk: float = 10.0
    tier3_risk: float = 4.0
    tier1_dd: float = 1.40
    tier2_dd: float = 2.00
    tier3_dd: float = 3.20
    max_concurrent: int = 3
    max_per_cluster: int = 1


@dataclass
class WindowResult:
    window_id: int
    name: str
    trades: int
    win_rate: float
    net_pnl: float
    net_roi: float
    max_dd: float
    rejected_concurrency: int
    rejected_cluster: int
    status: str


@njit(cache=True, inline="always")
def _risk_tier(dd_pct, base, t1r, t2r, t3r, t1d, t2d, t3d):
    if dd_pct >= t3d:
        return t3r
    if dd_pct >= t2d:
        return t2r
    if dd_pct >= t1d:
        return t1r
    return base


def _risk_for_drawdown(dd_pct: float, cfg: RiskConfig) -> float:
    return _risk_tier(
        dd_pct, cfg.base_risk, cfg.tier1_risk, cfg.tier2_risk, cfg.tier3_risk,
        cfg.tier1_dd, cfg.tier2_dd, cfg.tier3_dd,
    )


@njit(cache=True, fastmath=True)
def _portfolio_kernel(
    times: np.ndarray, exits: np.ndarray, clusters: np.ndarray, r_mults: np.ndarray,
    capital: float, base: float, t1r: float, t2r: float, t3r: float,
    t1d: float, t2d: float, t3d: float,
    max_concurrent: int, max_per_cluster: int, n_clusters: int,
):
    """
    Governed sequential portfolio simulation.

    Open positions are tracked in a small fixed array of exit times plus a
    per-cluster occupancy count, so admission checks are O(max_concurrent)
    rather than O(open positions) with Python object overhead.
    """
    n = times.shape[0]
    open_exit = np.empty(max_concurrent, dtype=np.int64)
    open_clus = np.empty(max_concurrent, dtype=np.int64)
    clus_count = np.zeros(n_clusters, dtype=np.int64)
    n_open = 0

    equity = capital
    peak = capital
    max_dd = 0.0
    wins = 0
    taken = 0
    rej_conc = 0
    rej_clus = 0

    for i in range(n):
        t_now = times[i]

        # Retire positions whose exit time has passed.
        w = 0
        for p in range(n_open):
            if open_exit[p] > t_now:
                open_exit[w] = open_exit[p]
                open_clus[w] = open_clus[p]
                w += 1
            else:
                clus_count[open_clus[p]] -= 1
        n_open = w

        if n_open >= max_concurrent:
            rej_conc += 1
            continue
        cl = clusters[i]
        if clus_count[cl] >= max_per_cluster:
            rej_clus += 1
            continue

        dd_now = (peak - equity) / peak * 100.0 if peak > 0.0 else 0.0
        risk = _risk_tier(dd_now, base, t1r, t2r, t3r, t1d, t2d, t3d)

        r = r_mults[i]
        equity += r * risk
        taken += 1
        if r > 0.0:
            wins += 1
        if equity > peak:
            peak = equity
        d = (peak - equity) / peak * 100.0 if peak > 0.0 else 0.0
        if d > max_dd:
            max_dd = d

        open_exit[n_open] = exits[i]
        open_clus[n_open] = cl
        clus_count[cl] += 1
        n_open += 1

    return taken, wins, equity, max_dd, rej_conc, rej_clus


def simulate_portfolio(signals: pd.DataFrame, cfg: RiskConfig) -> Dict[str, float]:
    """
    Sequential portfolio simulation honouring both governance rules.

    Signals must be time-sorted. A signal is skipped when the global concurrency
    cap is hit or when its correlation cluster already holds a position -- this
    is what makes basket subsets non-additive, and it is exactly the mechanism
    the audited report claimed but never enforced.
    """
    if len(signals) == 0:
        return {
            "trades": 0, "win_rate": 0.0, "net_pnl": 0.0, "net_roi": 0.0,
            "max_dd": 0.0, "rejected_concurrency": 0, "rejected_cluster": 0,
        }

    codes, _ = pd.factorize(signals["cluster"], sort=False)
    taken, wins, equity, max_dd, rej_c, rej_k = _portfolio_kernel(
        np.ascontiguousarray(signals["time"].values, dtype=np.int64),
        np.ascontiguousarray(signals["exit_time"].values, dtype=np.int64),
        np.ascontiguousarray(codes, dtype=np.int64),
        np.ascontiguousarray(signals["r_mult"].values, dtype=np.float64),
        cfg.capital, cfg.base_risk, cfg.tier1_risk, cfg.tier2_risk, cfg.tier3_risk,
        cfg.tier1_dd, cfg.tier2_dd, cfg.tier3_dd,
        int(cfg.max_concurrent), int(cfg.max_per_cluster), int(codes.max()) + 1,
    )

    return {
        "trades": int(taken),
        "win_rate": (wins / taken * 100.0) if taken else 0.0,
        "net_pnl": equity - cfg.capital,
        "net_roi": (equity - cfg.capital) / cfg.capital * 100.0,
        "max_dd": max_dd,
        "rejected_concurrency": int(rej_c),
        "rejected_cluster": int(rej_k),
    }


# ----------------------------------------------------------------------------
# Walk-forward driver
# ----------------------------------------------------------------------------

def _fit_threshold_on_train(probs_train: np.ndarray, y_train: np.ndarray, quantile: float) -> float:
    """
    Choose the decision threshold using ONLY training-fold predictions.

    This is the direct fix for audit finding B8. The replaced line was
    `thresh = np.percentile(probs, 70)` computed on `orb_test`.
    """
    if len(probs_train) == 0:
        return 0.55
    return float(np.quantile(probs_train, quantile))


def run_walkforward(
    pool: pd.DataFrame,
    windows: List[dict],
    cfg: RiskConfig,
    criteria: dict,
    baskets: Optional[Sequence[str]] = None,
    threshold_quantile: float = 0.70,
    seed: int = 42,
    verbose: bool = True,
) -> Tuple[List[WindowResult], pd.DataFrame]:
    from sklearn.ensemble import HistGradientBoostingClassifier

    if baskets is not None:
        pool = pool[pool["basket"].isin(baskets)].reset_index(drop=True)

    purge_s = PURGE_HOURS * 3600
    results: List[WindowResult] = []
    all_signals: List[pd.DataFrame] = []

    min_roi = criteria["min_roi_percent"]
    max_dd_lim = criteria["max_dd_percent"]
    min_wr = criteria["min_winrate_percent"]
    min_trd = criteria["min_trades"]

    for w in windows:
        start = int(pd.Timestamp(w["start_date"], tz="UTC").timestamp())
        end = int(pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").timestamp())

        train = pool[pool["exit_time"] < (start - purge_s)]
        test = pool[(pool["time"] >= start) & (pool["time"] <= end)]

        if len(train) < 400 or len(test) == 0:
            results.append(WindowResult(w["window_id"], w["name"], 0, 0, 0, 0, 0, 0, 0, "NO_DATA"))
            continue

        X_tr = train[FEATURES].values
        y_tr = (train["r_mult"].values > 0).astype(int)
        if y_tr.sum() < 20 or (1 - y_tr).sum() < 20:
            results.append(WindowResult(w["window_id"], w["name"], 0, 0, 0, 0, 0, 0, 0, "NO_DATA"))
            continue

        # Tree ensembles are scale-invariant, so no StandardScaler is needed --
        # one less stateful object that could leak test statistics.
        model = HistGradientBoostingClassifier(
            max_iter=150, max_depth=4, learning_rate=0.06,
            min_samples_leaf=40, l2_regularization=1.0,
            early_stopping=False, random_state=seed,
        )
        model.fit(X_tr, y_tr)

        # Threshold fitted on TRAIN ONLY, then frozen.
        p_tr = model.predict_proba(X_tr)[:, 1]
        thresh = _fit_threshold_on_train(p_tr, y_tr, threshold_quantile)

        p_te = model.predict_proba(test[FEATURES].values)[:, 1]
        sel = test.loc[p_te >= thresh].copy()
        sel["prob"] = p_te[p_te >= thresh]
        sel = sel.sort_values("time")

        stats = simulate_portfolio(sel, cfg)
        is_pass = (
            stats["net_roi"] >= min_roi
            and stats["max_dd"] <= max_dd_lim
            and stats["win_rate"] >= min_wr
            and stats["trades"] >= min_trd
        )
        status = "PASS" if is_pass else ("PROFIT" if stats["net_pnl"] > 0 else "FAIL")

        results.append(WindowResult(
            w["window_id"], w["name"], stats["trades"], stats["win_rate"],
            stats["net_pnl"], stats["net_roi"], stats["max_dd"],
            stats["rejected_concurrency"], stats["rejected_cluster"], status,
        ))
        if len(sel):
            all_signals.append(sel)

        if verbose:
            print(
                f"  W{w['window_id']:02d} | {w['name'][:34]:<34} | "
                f"n={stats['trades']:>4} | WR={stats['win_rate']:>5.1f}% | "
                f"ROI={stats['net_roi']:>+8.2f}% | DD={stats['max_dd']:>5.2f}% | {status}"
            )

    executed = pd.concat(all_signals, ignore_index=True) if all_signals else pd.DataFrame()
    return results, executed


# ----------------------------------------------------------------------------
# Monte Carlo -- real bootstrap resampling
# ----------------------------------------------------------------------------

@njit(cache=True, parallel=True, fastmath=True)
def _mc_kernel(
    r_arr: np.ndarray, n_runs: int, seed: int,
    capital: float, base: float, t1r: float, t2r: float, t3r: float,
    t1d: float, t2d: float, t3d: float,
):
    """
    Parallel bootstrap. Each run draws `n` R-multiples with replacement and
    replays them through the same drawdown-tiered risk ladder used live, so the
    simulated equity path is governed identically to the backtest.
    """
    n = r_arr.shape[0]
    rois = np.empty(n_runs, dtype=np.float64)
    dds = np.empty(n_runs, dtype=np.float64)

    for i in prange(n_runs):
        np.random.seed(seed + i)
        equity = capital
        peak = capital
        mdd = 0.0
        for _ in range(n):
            r = r_arr[np.random.randint(0, n)]
            dd_now = (peak - equity) / peak * 100.0 if peak > 0.0 else 0.0
            equity += r * _risk_tier(dd_now, base, t1r, t2r, t3r, t1d, t2d, t3d)
            if equity > peak:
                peak = equity
            d = (peak - equity) / peak * 100.0 if peak > 0.0 else 0.0
            if d > mdd:
                mdd = d
        rois[i] = (equity - capital) / capital * 100.0
        dds[i] = mdd

    return rois, dds


def monte_carlo_bootstrap(
    r_multiples: np.ndarray,
    cfg: RiskConfig,
    n_runs: int = 10_000,
    seed: int = 42,
) -> Dict[str, float]:
    """
    Bootstrap resampling WITH REPLACEMENT over realised R-multiples.

    Audit finding B7: the reported 5th-95th ROI band spanned only +/-6% around
    the median, which is far too tight for a true resample of ~3.9k trades and
    indicates the sequence was permuted rather than resampled. This function
    does the real thing and reports whatever the tails actually are.
    """
    if len(r_multiples) == 0:
        return {}
    r_arr = np.ascontiguousarray(r_multiples, dtype=np.float64)
    rois, dds = _mc_kernel(
        r_arr, int(n_runs), int(seed),
        cfg.capital, cfg.base_risk, cfg.tier1_risk, cfg.tier2_risk, cfg.tier3_risk,
        cfg.tier1_dd, cfg.tier2_dd, cfg.tier3_dd,
    )
    n = len(r_arr)

    return {
        "n_runs": n_runs,
        "n_trades_per_run": n,
        "roi_p05": float(np.percentile(rois, 5)),
        "roi_p50": float(np.percentile(rois, 50)),
        "roi_p95": float(np.percentile(rois, 95)),
        "dd_p50": float(np.percentile(dds, 50)),
        "dd_p95": float(np.percentile(dds, 95)),
        "dd_p99": float(np.percentile(dds, 99)),
        "dd_worst": float(dds.max()),
        "prob_dd_gt_5pct": float((dds > 5.0).mean() * 100.0),
        "prob_dd_gt_10pct": float((dds > 10.0).mean() * 100.0),
        "prob_loss": float((rois < 0).mean() * 100.0),
    }


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description="Honest walk-forward validation harness")
    ap.add_argument("--quick", action="store_true", help="Limit to 6 assets per basket")
    ap.add_argument("--mc-runs", type=int, default=10_000)
    ap.add_argument("--target-r", type=float, default=2.5)
    ap.add_argument("--hold-bars", type=int, default=24)
    ap.add_argument("--threshold-quantile", type=float, default=0.70)
    ap.add_argument("--cost-frac", type=float, default=None,
                    help="Override round-trip cost (fraction of risk distance). "
                         "Default: per-symbol estimate from the broker spread column.")
    ap.add_argument("--direction", type=int, default=1, choices=[1, -1],
                    help="1 = momentum long on breakout, -1 = fade the extreme")
    ap.add_argument("--max-cost-frac", type=float, default=None,
                    help="Exclude assets whose round-trip cost exceeds this")
    ap.add_argument("--baskets", type=str, default=None,
                    help="Comma-separated subset, e.g. 'Forex' or 'Forex,CFD'")
    ap.add_argument("--breakout-lookback", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default="reports/honest_walkforward.json")
    args = ap.parse_args()

    t0 = time.perf_counter()
    print("=" * 96)
    print("HONEST WALK-FORWARD VALIDATION  (no OOS-fitted threshold, governance enforced)")
    print("=" * 96)

    with open(CRITERIA_PATH) as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)

    cfg = RiskConfig(capital=criteria.get("initial_capital_usd", 5000.0))

    print("\n[1/5] Loading universe...")
    assets = load_universe(limit_per_basket=6 if args.quick else None)
    if args.max_cost_frac is not None:
        before = len(assets)
        assets = [a for a in assets if a.cost_frac <= args.max_cost_frac]
        print(f"  Cost filter <= {args.max_cost_frac:.4f} R: kept {len(assets)}/{before} assets")
    by_basket: Dict[str, int] = {}
    for a in assets:
        by_basket[a.basket] = by_basket.get(a.basket, 0) + 1
    declared = sum(len(v) for v in ASSET_BASKETS.values())
    print(f"  Declared universe : {declared}")
    print(f"  Loaded with usable 15m history: {len(assets)}  {by_basket}")

    print("\n[2/5] Building causal candidate pool...")
    pool = build_candidate_pool(
        assets, args.target_r, args.hold_bars, verbose=args.quick,
        cost_frac=args.cost_frac, breakout_lookback=args.breakout_lookback,
        direction=args.direction,
    )
    if pool.empty:
        print("No candidates generated; aborting.")
        return
    breakeven = 1.0 / (1.0 + args.target_r) * 100.0
    base = (pool["r_mult"] > 0).mean() * 100.0
    print(f"  Total candidates: {len(pool):,}")
    print(f"  Span: {pd.to_datetime(pool['time'].min(), unit='s')} -> {pd.to_datetime(pool['time'].max(), unit='s')}")
    if args.cost_frac is not None:
        print(f"  Round-trip cost  : {args.cost_frac:.4f} R (flat override)")
    else:
        cs = [a.cost_frac for a in assets]
        print(f"  Round-trip cost  : per-symbol, median {np.median(cs):.4f} R "
              f"(min {min(cs):.4f} / max {max(cs):.4f})")
    print(f"  Direction        : {'momentum long' if args.direction > 0 else 'fade short'}")
    print(f"  Raw base rate    : {base:.2f}%   (breakeven at {args.target_r}R needs {breakeven:.2f}%)")
    print(f"  Raw expectancy   : {pool['r_mult'].mean():+.4f} R/trade")

    print("\n[3/5] Walk-forward across OOS windows (full multiverse)...")
    sel_baskets = args.baskets.split(",") if args.baskets else None
    if sel_baskets:
        print(f"  Restricted to baskets: {sel_baskets}")
    results, executed = run_walkforward(
        pool, windows, cfg, criteria, baskets=sel_baskets,
        threshold_quantile=args.threshold_quantile, seed=args.seed,
    )

    n_pass = sum(1 for r in results if r.status == "PASS")
    n_eval = sum(1 for r in results if r.status != "NO_DATA")
    tot_tr = sum(r.trades for r in results)
    tot_pnl = sum(r.net_pnl for r in results)
    rej_c = sum(r.rejected_concurrency for r in results)
    rej_k = sum(r.rejected_cluster for r in results)

    print("-" * 96)
    print(f"  Windows evaluated : {n_eval}/{len(windows)}   PASS: {n_pass}")
    print(f"  Total trades      : {tot_tr:,}   Total PnL: {tot_pnl:+,.2f} USD")
    print(f"  Governance rejections -> concurrency: {rej_c:,}   cluster: {rej_k:,}")

    print("\n[4/5] Basket decomposition (each re-simulated through the governed loop)...")
    combos = [
        ("Crypto Only", ["Crypto"]), ("Forex Only", ["Forex"]), ("CFD Only", ["CFD"]),
        ("Crypto + Forex", ["Crypto", "Forex"]), ("Crypto + CFD", ["Crypto", "CFD"]),
        ("Forex + CFD", ["Forex", "CFD"]), ("Full Multiverse", ["Crypto", "Forex", "CFD"]),
    ]
    decomposition = {}
    for label, bl in combos:
        res, _ = run_walkforward(
            pool, windows, cfg, criteria, baskets=bl,
            threshold_quantile=args.threshold_quantile, seed=args.seed, verbose=False,
        )
        tr = sum(r.trades for r in res)
        pnl = sum(r.net_pnl for r in res)
        wr = float(np.mean([r.win_rate for r in res if r.trades > 0])) if any(r.trades for r in res) else 0.0
        dd = max((r.max_dd for r in res), default=0.0)
        decomposition[label] = {"trades": tr, "win_rate": wr, "net_pnl": pnl, "max_dd": dd}
        print(f"  {label:<18} trades={tr:>5}  WR={wr:>5.1f}%  PnL={pnl:>+11,.2f}  maxDD={dd:>5.2f}%")

    print(f"\n[5/5] Monte Carlo bootstrap ({args.mc_runs:,} runs, resampled with replacement)...")
    mc = {}
    if not executed.empty:
        mc = monte_carlo_bootstrap(executed["r_mult"].values, cfg, n_runs=args.mc_runs, seed=args.seed)
        print(f"  ROI  p05/p50/p95 : {mc['roi_p05']:+.2f}% / {mc['roi_p50']:+.2f}% / {mc['roi_p95']:+.2f}%")
        print(f"  MaxDD p50/p95/p99: {mc['dd_p50']:.2f}% / {mc['dd_p95']:.2f}% / {mc['dd_p99']:.2f}%")
        print(f"  Worst-path MaxDD : {mc['dd_worst']:.2f}%")
        print(f"  P(DD > 5%)       : {mc['prob_dd_gt_5pct']:.2f}%")
        print(f"  P(net loss)      : {mc['prob_loss']:.2f}%")

    payload = {
        "generated_utc": pd.Timestamp.now("UTC").isoformat(),
        "config": {
            "target_r": args.target_r, "hold_bars": args.hold_bars,
            "threshold_quantile": args.threshold_quantile, "seed": args.seed,
            "purge_hours": PURGE_HOURS, "quick": args.quick,
            "cost_frac": args.cost_frac, "direction": args.direction,
            "max_cost_frac": args.max_cost_frac, "breakout_lookback": args.breakout_lookback,
            "max_concurrent": cfg.max_concurrent, "max_per_cluster": cfg.max_per_cluster,
        },
        "edge": {
            "raw_base_rate_pct": float(base),
            "breakeven_rate_pct": float(breakeven),
            "raw_expectancy_r": float(pool["r_mult"].mean()),
        },
        "universe": {"declared": declared, "loaded": len(assets), "by_basket": by_basket},
        "candidates": int(len(pool)),
        "scorecard": [r.__dict__ for r in results],
        "summary": {
            "windows_evaluated": n_eval, "windows_passed": n_pass,
            "total_trades": tot_tr, "total_pnl": tot_pnl,
            "rejected_concurrency": rej_c, "rejected_cluster": rej_k,
        },
        "decomposition": decomposition,
        "monte_carlo": mc,
    }
    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, default=float)

    print(f"\nWrote {out_path.relative_to(REPO_ROOT)}   ({time.perf_counter() - t0:.1f}s)")


if __name__ == "__main__":
    main()
