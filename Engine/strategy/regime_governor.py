r"""
================================================================================
REGIME GOVERNOR -- DEFENSIVE GATING ON PERSISTENT MARKET STATE
================================================================================
Motivation. A Beta-Binomial tracker of the strategy's own win rate was measured
to have Pearson r = +0.032 against the next window's realised win rate, because
the ML models are refitted from scratch every window: the quantity being tracked
belongs to a different model each period and does not persist. This governor
instead gates on properties of the MARKET, which survive refits and therefore
carry genuine information forward across window boundaries.

Regime state is computed STRICTLY CAUSALLY at each window's start, using only
data available before that timestamp:

  vol       BTC trailing 30d ATR%%            (the gauge the runner already derives)
  vol_rank  its percentile rank over the trailing 365d of 4h bars
  tide      BTC macro tide, EMA-20/50/200 stack   (+1 bull / -1 bear / 0 chop)
  disp_rank percentile rank of cross-sectional dispersion -- the std of trailing
            30d returns across the 11 certified assets -- over the trailing 365d

Threshold provenance. The 0.88 volatility-shock percentile is INHERITED from the
repository's existing bar-level convention (fast_numba_oos_engine.py:321,
`is_shock = rv_rank >= 0.88`), not chosen here. A rolling (not expanding) rank is
used for the same reason: an expanding rank is permanently anchored by the
2021-22 high-volatility era, so no later window can ever register a shock -- with
an expanding window the maximum observed rank across all 20 windows is 0.737.

Defensive only. The governor can raise the entry probability threshold or veto
entries. It never lowers a threshold: an accelerator that loosened entries after
a favourable streak was measured to flip W04 from +736.83 to -111.99.

CAVEAT ON INFERENCE. The suite contains 20 windows and this governor activates in
a handful of them. A single walk-forward run at n=20 cannot separate skill from
luck, and selecting the best of several governor designs on these same 20 windows
would be exactly the out-of-sample-fitting error this module exists to avoid.
Thresholds below are fixed a priori on economic reasoning and repo convention.
================================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd

CORE_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT",
    "ADAUSDT", "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
]

BARS_4H_PER_30D = 180
BARS_4H_PER_365D = 2190
MIN_HISTORY_BARS = 60


def compute_regime_features(
    btc_4h: pd.DataFrame,
    dispersion: pd.Series,
    as_of: pd.Timestamp,
) -> Dict[str, Any]:
    """Causal regime snapshot as of `as_of`, using strictly prior data.

    `btc_4h` must carry: time, close, atr, ema_50, ema_200.
    `dispersion` is a time-indexed series of cross-sectional 30d-return dispersion.
    """
    prior = btc_4h[btc_4h["time"] < as_of]
    if len(prior) == 0:
        return {"available": False, "vol": np.nan, "vol_rank": np.nan,
                "tide": 0, "disp_rank": np.nan}

    # Rank the SMOOTHED 30-day volatility measure, not the instantaneous 4h ATR%.
    # A single 4h bar's ATR% is far too noisy to define a regime: at 2024-03-01 the
    # instantaneous rank reads 0.980 while the 30d-measure rank reads 0.522.
    vol_col = "trailing_30d_atr_pct" if "trailing_30d_atr_pct" in prior.columns else "atr_pct"
    vol_series = prior[vol_col].dropna()
    vol = float(vol_series.iloc[-1]) if len(vol_series) else np.nan

    hist = vol_series.iloc[-BARS_4H_PER_365D:]
    vol_rank = float((hist <= vol).mean()) if len(hist) >= MIN_HISTORY_BARS else np.nan

    bull = (prior["close"] > prior["ema_50"]) & (prior["ema_50"] > prior["ema_200"])
    bear = (prior["close"] < prior["ema_50"]) & (prior["ema_50"] < prior["ema_200"])
    # np.where yields an ndarray, so index with [-1] rather than .iloc
    tide = int(np.where(bull.to_numpy(), 1, np.where(bear.to_numpy(), -1, 0))[-1])

    d_prior = dispersion[dispersion.index < as_of].dropna()
    d_hist = d_prior.iloc[-BARS_4H_PER_365D:]
    disp_rank = (
        float((d_hist <= d_prior.iloc[-1]).mean())
        if len(d_hist) >= MIN_HISTORY_BARS else np.nan
    )

    return {"available": True, "vol": vol, "vol_rank": vol_rank,
            "tide": tide, "disp_rank": disp_rank}


def build_dispersion_series(
    cache_dir: Path | str, symbols: List[str] = CORE_SYMBOLS
) -> pd.Series:
    """Cross-sectional std of trailing 30d log-return across the certified assets."""
    cache_dir = Path(cache_dir)
    ret30 = {}
    for sym in symbols:
        p = cache_dir / f"{sym}_4h.parquet"
        if not p.exists():
            continue
        d = pd.read_parquet(p, columns=["time", "close"])
        d["time"] = pd.to_datetime(d["time"], utc=True)
        d = d.sort_values("time").set_index("time")
        ret30[sym] = np.log(d["close"] / d["close"].shift(BARS_4H_PER_30D))
    if not ret30:
        return pd.Series(dtype=float)
    return pd.DataFrame(ret30).std(axis=1)


@dataclass
class RegimeVerdict:
    """The governor's decision for one window."""
    delta: float = 0.0
    veto: bool = False
    label: str = "benign"
    vol: float = np.nan
    vol_rank: float = np.nan
    tide: int = 0
    disp_rank: float = np.nan

    def effective_threshold(self, base: float) -> float:
        return base + self.delta


@dataclass
class RegimeGovernor:
    """Penalty-only regime gate. `delta` is always >= 0.

    Rules are evaluated independently and the MOST SEVERE applies (max, not sum),
    so the penalty is bounded by `shock_penalty` and cannot stack without limit.
    """

    # Volatility shock percentile inherited from fast_numba_oos_engine.py:321.
    vol_shock_rank: float = 0.88
    vol_elevated_rank: float = 0.70
    shock_penalty: float = 0.04
    elevated_penalty: float = 0.02

    # Dead chop: no directional tide AND no cross-sectional dispersion to trade.
    chop_tide: int = 0
    chop_disp_rank: float = 0.25
    chop_penalty: float = 0.02

    def assess(self, features: Dict[str, Any]) -> RegimeVerdict:
        if not features.get("available", False):
            return RegimeVerdict(label="no_history")

        vol = features["vol"]
        vol_rank = features["vol_rank"]
        tide = int(features["tide"])
        disp_rank = features["disp_rank"]

        candidates: List[tuple] = []  # (delta, label)

        if vol_rank == vol_rank and vol_rank >= self.vol_shock_rank:
            candidates.append((self.shock_penalty, "vol_shock"))
        if vol_rank == vol_rank and vol_rank >= self.vol_elevated_rank:
            candidates.append((self.elevated_penalty, "vol_elevated"))

        dead_chop = (
            tide == self.chop_tide
            and disp_rank == disp_rank
            and disp_rank < self.chop_disp_rank
        )
        if dead_chop:
            candidates.append((self.chop_penalty, "dead_chop"))

        if not candidates:
            return RegimeVerdict(delta=0.0, label="benign", vol=vol,
                                 vol_rank=vol_rank, tide=tide, disp_rank=disp_rank)

        delta, label = max(candidates, key=lambda c: c[0])
        return RegimeVerdict(delta=delta, label=label, vol=vol,
                             vol_rank=vol_rank, tide=tide, disp_rank=disp_rank)
