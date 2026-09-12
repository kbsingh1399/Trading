"""Levels / Point-of-Control research lab (Engine).

Purpose
-------
Causal, walk-forward research on price-level strategies for Binance USDT-M
perpetual futures:

* previous **week** high/low        (PWH / PWL)
* previous **month** high/low       (PMH / PML)
* all-time high                     (ATH)
* prior **day** high/low            (PDH / PDL)
* session **Point of Control** + value area, and several POC perspectives

Everything is evaluated on the 20 pre-registered OOS windows in
``Engine/oos_windows_20.json`` against the pass criteria in
``Engine/target_oos_criteria.json`` (per window: ROI >= 10 %, max DD <= 5 %,
win rate >= 40 %, >= 15 trades, target >= 4R net).

Design rules (non-negotiable, inherited from ``Engine/s1_trend_following_suite.py``):

1. A signal is formed from a *completed* candle and filled at the **next open**
   (plus slippage).
2. Every feature at bar *t* uses only bars ``<= t``. Sessions/weeks/months are
   only used once they are *complete* (prior-period levels).
3. For ML, the model for window *w* is trained only on bars strictly before
   ``window_start - 72h`` (quarantine purge).
4. Costs are identical to the certified contract: 8 bps taker fee, 10 bps entry
   slip, 15 bps exit slip and a 41 bps round-trip friction floor.
"""
from __future__ import annotations

BAR_MS = 900_000
DAY_MS = 86_400_000
WEEK_MS = 7 * DAY_MS
PURGE_MS = 72 * 3_600_000
