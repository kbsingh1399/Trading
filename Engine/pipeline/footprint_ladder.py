"""
================================================================================
TABLE 2 ASSEMBLY: EXACT TICK RUNGS + CAUSAL SYNTHETIC RUNGS
================================================================================
Every Table-1 candle must own >= 1 rung in Table 2. Where aggTrades archives
were fetched the rungs are exact (``rung_source = 0``). For every remaining
candle a synthetic profile is generated **strictly from that candle's own
OHLCV** plus a session-anchored bin step (``rung_source = 1``):

  * bin step   : nice_bin_step(open of the first bar of the UTC day) -- known
                 before any bar of the day closes, identical geometry rule to
                 the tick fetcher (first print of the day).
  * rungs      : round(low/step) .. round(high/step), capped at MAX_RUNGS by
                 widening the step for that single bar.
  * volumes    : taker-buy / taker-sell split spread uniformly over the rungs.
  * POC        : rung containing the close (uniform profile => convention).
  * imbalances : 0 (cannot be inferred without ticks; never fabricated).
  * downtime   : is_synthetic bars emit one zero-volume rung at the close.

No full-sample statistic (median price, global step, etc.) is used anywhere.
================================================================================
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

from ..core.canonical_indicators import nice_bin_step, session_day_index
from ..core.schema import LADDER_COLUMNS, LADDER_DTYPES, RUNG_SOURCE_SYNTHETIC

MAX_RUNGS = 512


def _session_bin_step(open_time_ms: np.ndarray, opens: np.ndarray) -> np.ndarray:
    day = session_day_index(open_time_ms)
    _, first_idx = np.unique(day, return_index=True)
    step_by_day = nice_bin_step(opens[first_idx])
    day_pos = np.searchsorted(day[first_idx], day)
    return step_by_day[day_pos]


def synthesize_causal_ladder(master: pd.DataFrame) -> pd.DataFrame:
    """Builds synthetic rungs for every row of ``master`` (already filtered to the candles that need them)."""
    if master.empty:
        return pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)

    ot = master["open_time_ms"].to_numpy(np.int64)
    o = master["open"].to_numpy(np.float64)
    h = master["high"].to_numpy(np.float64)
    l = master["low"].to_numpy(np.float64)
    c = master["close"].to_numpy(np.float64)
    vb = master["volume_base"].to_numpy(np.float64)
    buy = master["taker_buy_vol_btc"].to_numpy(np.float64) if "taker_buy_vol_btc" in master else vb * 0.5
    sell = np.maximum(vb - buy, 0.0)
    tc = master["trade_count"].to_numpy(np.int64) if "trade_count" in master else np.zeros(len(master), dtype=np.int64)
    synthetic_bar = master["is_synthetic"].to_numpy() == 1 if "is_synthetic" in master else np.zeros(len(master), dtype=bool)

    step = _session_bin_step(ot, o)
    lo_bin = np.round(l / step).astype(np.int64)
    hi_bin = np.maximum(np.round(h / step).astype(np.int64), lo_bin)
    n_bins = hi_bin - lo_bin + 1
    too_wide = n_bins > MAX_RUNGS
    if too_wide.any():
        factor = np.ceil(n_bins[too_wide] / MAX_RUNGS)
        step[too_wide] = step[too_wide] * factor
        lo_bin[too_wide] = np.round(l[too_wide] / step[too_wide]).astype(np.int64)
        hi_bin[too_wide] = np.maximum(np.round(h[too_wide] / step[too_wide]).astype(np.int64), lo_bin[too_wide])
        n_bins = hi_bin - lo_bin + 1
    close_bin = np.clip(np.round(c / step).astype(np.int64), lo_bin, hi_bin)
    # downtime bars: single rung at the close
    lo_bin = np.where(synthetic_bar, close_bin, lo_bin)
    hi_bin = np.where(synthetic_bar, close_bin, hi_bin)
    n_bins = hi_bin - lo_bin + 1

    total = int(n_bins.sum())
    bar_idx = np.repeat(np.arange(len(master)), n_bins)
    offsets = np.arange(total) - np.repeat(np.cumsum(n_bins) - n_bins, n_bins)
    bins = lo_bin[bar_idx] + offsets
    step_r = step[bar_idx]
    nb = n_bins[bar_idx].astype(np.float64)

    ask = buy[bar_idx] / nb
    bid = sell[bar_idx] / nb
    trades = np.floor(tc[bar_idx] / nb).astype(np.int64)
    # distribute the remainder of trade_count so per-candle sums are exact
    remainder = tc - np.floor(tc / n_bins).astype(np.int64) * n_bins
    trades += (offsets < remainder[bar_idx]).astype(np.int64)

    ladder = pd.DataFrame({
        "open_time_ms": ot[bar_idx],
        "price_bin": np.round(bins * step_r, 8),
        "bid_vol_coin": bid,
        "ask_vol_coin": ask,
        "net_delta_coin": ask - bid,
        "is_buy_imbalance": np.zeros(total, dtype=np.int8),
        "is_sell_imbalance": np.zeros(total, dtype=np.int8),
        "is_poc": (bins == close_bin[bar_idx]).astype(np.int8),
        "trade_count": trades,
        "rung_source": np.full(total, RUNG_SOURCE_SYNTHETIC, dtype=np.int8),
    })
    return ladder[LADDER_COLUMNS].astype(LADDER_DTYPES)


def assemble_ladder(
    master: pd.DataFrame,
    tick_ladder: pd.DataFrame | None,
    allow_synthetic: bool = False,
) -> Tuple[pd.DataFrame, dict]:
    """
    Combines exact tick rungs with optional synthetic rungs for uncovered candles.
    Under the Zero-Synthetic Mandate, allow_synthetic defaults to False, ensuring
    100% of generated rungs represent empirical trade executions.
    """
    master_ts = master["open_time_ms"].to_numpy(np.int64)
    if tick_ladder is not None and not tick_ladder.empty:
        # Align columns to LADDER_COLUMNS if present
        cols_to_keep = [c for c in LADDER_COLUMNS if c in tick_ladder.columns]
        tick = tick_ladder[tick_ladder["open_time_ms"].isin(master_ts)][cols_to_keep].copy()
        for c in LADDER_COLUMNS:
            if c not in tick.columns:
                tick[c] = np.zeros(len(tick), dtype=LADDER_DTYPES.get(c, "float64"))
        covered = np.isin(master_ts, tick["open_time_ms"].unique())
    else:
        tick = pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)
        covered = np.zeros(len(master), dtype=bool)

    if allow_synthetic and (~covered).any():
        synthetic = synthesize_causal_ladder(master.loc[~covered])
        ladder = pd.concat([tick[LADDER_COLUMNS], synthetic[LADDER_COLUMNS]], ignore_index=True)
        synthetic_cnt = int((~covered).sum())
        synthetic_rungs = int(len(synthetic))
    else:
        ladder = tick[LADDER_COLUMNS].copy() if not tick.empty else pd.DataFrame(columns=LADDER_COLUMNS).astype(LADDER_DTYPES)
        synthetic_cnt = 0
        synthetic_rungs = 0

    if not ladder.empty:
        ladder = ladder.astype(LADDER_DTYPES)
        ladder = ladder.sort_values(["open_time_ms", "price_bin"], kind="stable").reset_index(drop=True)

    stats = {
        "candles": int(len(master)),
        "tick_exact_candles": int(covered.sum()),
        "synthetic_candles": synthetic_cnt,
        "tick_rungs": int(len(tick)),
        "synthetic_rungs": synthetic_rungs,
    }
    return ladder, stats

