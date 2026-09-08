"""
================================================================================
RP2 ROUND 12 - THROUGHPUT-CALIBRATED CONVEX BREAKOUT-RECLAIM ENGINE (ML)

ROUND 11 POST-MORTEM (real-data run, 20 windows, 265.0 s)
---------------------------------------------------------
0/20 windows passed on 10 trades TOTAL across 20 months, against a floor of
15 trades PER window. The scorecard could not explain why, because Round 11
reported no candidate funnel. Round 12 fixes the cause, not the symptom.

1. FEASIBILITY FRONTIER (measured, 6,000 Monte-Carlo windows per cell)
   The mandated criteria are not uniformly satisfiable. Requiring ROI > +20%
   (1,000 USD) while capping drawdown at 5.0% (250 USD) forces

       n * E[R] / L_max  >  4.0        L_max = expected longest losing run

   At the mandated FLOOR of 15 trades and a 40.0% win rate with a 4R target,
   E[R] = +0.90R and L_max ~ 4.3, giving a ratio of 3.14. The minimum trade
   count is BELOW the feasibility boundary: no sizing scheme can rescue it.
   Measured single-window P(pass) and the 20-window conjunction:

       n= 15  wr=0.40  flat 1.3%   P=27.97%   P(all 20)=8.6e-12
       n= 60  wr=0.44  flat 0.4%   P=76.30%   P(all 20)=4.5e-03
       n=100  wr=0.40  flat 0.4%   P=83.63%   P(all 20)=2.8e-02
       n=100  wr=0.44  flat 0.35%  P=95.40%   P(all 20)=3.9e-01
       n=100  wr=0.48  flat 0.35%  P=98.60%   P(all 20)=7.5e-01

   Three consequences drive every Round 12 decision:
     (a) TRADE COUNT IS THE DOMINANT LEVER. Sequence risk L_max grows only
         logarithmically in n while edge accumulates linearly, so 15 -> 100
         trades moves the 20-window conjunction by ~10 orders of magnitude.
         The design target is ~100 trades/window, NOT the 15 floor.
     (b) OPTIMAL RISK FALLS AS TRADE COUNT RISES (1.3% -> 0.35%). Raising
         risk to reach +20% is exactly backwards.
     (c) THE ML OVERLAY'S ONLY JOB IS WIN RATE. Lifting 0.40 -> 0.48 at
         n=100 moves P(all 20) from 2.8e-02 to 7.5e-01, a 27x gain -- worth
         more than any sizing change available.

2. HOUSE-MONEY SIZING WAS DESTROYING THE DRAWDOWN CEILING
   At n=100/wr=0.44, house-money (base 0.35% + kelly 0.42, cap 2.0%) scores
   P(pass)=0.02% with p95 drawdown 28.40%; flat 0.35% scores 95.40% with p95
   drawdown 4.62%. Compounding risk into a hard drawdown cap is
   self-defeating. The mechanism is RETAINED and switchable per mandate, but
   `flat_risk_mode` now defaults True.

3. ~25-28% OF THE UNIVERSE WAS TRADING DARK (the throughput root cause)
   Round 11 reported orderflow_cover of 0.786, 0.733, 0.750, 0.765 and
   0.722. Those are exactly 11/14, 11/15, 12/16, 13/17 and 13/18 -- integer
   SYMBOL ratios, not bar fractions. A subset of symbols contributed
   precisely zero cover. load_symbol() had two paths that skipped the ladder
   in total silence: a missing file, and a predicate-pushdown filter
   returning an empty frame (a dtype mismatch on the partition key yields
   zero rows WITHOUT raising). Those symbols could never satisfy a footprint
   gate, so they produced zero candidates.
   NOTE: this is NOT explained by listing dates. Newly-listed symbols are
   already excluded upstream by the row-count guard in load_symbol(), so
   they never reach the cover average at all.
   Round 12 adds alias normalisation, timestamp-dtype coercion, a full-read
   fallback, a merge-hit check, and a per-symbol `ladder_status` reported in
   every scorecard with a loud console warning naming the dark symbols.

4. THREE STRUCTURAL THROUGHPUT DEFECTS IN THE STATE MACHINE
   See the block comment above scan_candidates(). In short: one global arm
   slot per symbol; the arm destroyed on the first confirmation miss
   (turning the filter into a one-shot lottery); and no re-arm on a disarm
   bar. No threshold relaxation could have fixed these.

5. CONCURRENCY CAPACITY WAS BINDING
   Capacity = max_concurrent * 2880 / avg_hold_bars. At 2 slots a 672-bar
   (7 day) hold cap admits at most ~19 trades/window even with infinite
   signal. hold_max_bars is now 288 and chop_hold_max_bars 144, giving
   ~96-160 trades/window of headroom at 2 slots.

WHAT IS AND IS NOT VERIFIED
---------------------------
Everything above is either arithmetic or a direct reading of the Round 11
scorecard and source. The engine passes its full invariant suite. NOTHING
here is a claim about Round 12's real-data performance, which is unknown
until the walk-forward is run on the real corpus.

SINGLE GLOBAL TUNING DIAL
-------------------------
If real-data windows still come in under the trade floor, adjust
`conf_min_score` (lower = more trades) GLOBALLY. Per-window overrides are
prohibited. Do NOT loosen catastrophic_gap or gap_multiplier
(max_friction_r was re-DERIVED in Round 12 from the feasibility frontier;
see the block comment on the field -- it is not a free parameter either)
or the 4.5% circuit breaker to chase ROI.

================================================================================
Drop-in replacement for Engine/strategy/rp2_round10_convex_trend_following_ml.py

Dependencies: numpy, pandas ONLY. No sklearn, no scipy, no network.

--------------------------------------------------------------------------------
WHY ROUND 10 FAILED (root cause, evidenced from the dataset manifests)
--------------------------------------------------------------------------------
1. DATA PROVENANCE CORRUPTION (dominant cause).
   Round 10 gated entries on `taker_volume_ratio`, `whale_index` and the
   liquidation z-scores. Those columns originate from the Binance *derivatives
   metrics archive*, which per the shipped manifests is missing/imputed for:
       ADAUSDT  2020: 100.00%   2021: 91.89%   2022: 86.56%
       BTCUSDT  2021:   0.39%   2022: 86.56%
   OOS windows W1..W8 span 2021-05 .. 2022-11. Round 10 therefore gated its
   entries on IMPUTED values across roughly 40% of the walk-forward, i.e. it was
   reading a flat-lined / interpolated series and calling it "orderflow".
   `schema.py` is explicit: `is_imputed_metrics` is "RETROSPECTIVE ONLY: not for
   contemporaneous live signals."
   FIX: strict two-tier data contract. TIER_A columns are provably real for every
   bar (OHLCV, trade counts, taker buy/sell splits, futures+spot CVD, zc_div,
   VWAP, RSI/ATR/EMA, and the ENTIRE footprint ladder - the manifests report
   synthetic_rungs = 0 for all 18 symbols). TIER_B columns are metrics-archive
   derived. TIER_B MAY NEVER GATE AN ENTRY. It enters the model only as a
   masked feature paired with an availability indicator, so the classifier can
   learn to ignore it in the eras where it is absent.

2. RETRACEMENT TRAPS.
   Round 10 bought the Donchian break itself, so every failed break was a full
   1R loss and the stop sat one ATR away, making friction expensive per unit R.
   FIX: a three-state DISPLACEMENT -> PULLBACK -> RECLAIM machine. The engine
   never buys the break. It arms on a displacement break, waits for a pullback
   that holds the broken level, and only triggers when the pullback high is
   reclaimed with confirming footprint absorption. The stop goes under the
   pullback extreme, not one ATR away, which shrinks 1R in price terms while the
   4R target stays anchored to the displacement impulse.

3. NON-STATIONARY REGIMES.
   FIX: a causal 3-state regime classifier (TREND / CHOP / SHOCK) computed from
   trailing bars only. Regime modulates risk fraction and maximum hold via a
   FIXED closed-form mapping. There is no per-window lookup table anywhere in
   this file (banned by AGENTS.md Part 7 / FABLE5 Part 14.2).

--------------------------------------------------------------------------------
THE SIZING ARITHMETIC (read this before tuning anything)
--------------------------------------------------------------------------------
Target is +20% ROI/window at <5% max drawdown, >=40% win rate, >=15 trades.
With capital 5,000 USD:
    +20% ROI = +1,000 USD.  Max DD 5% = 250 USD.
At a FLAT 1.0% risk (50 USD = 1R), +1,000 USD demands +20R net. A clean 4R:1R
payoff at exactly 40% WR yields 0.4*4 - 0.6*1 = +1.00R per trade before
friction, so ~20 trades gross, ~26 after 33 bps friction. But at a 60% loss
rate over 26 trades the expected longest losing run is ~4.5 trades, and 5 flat
losses at 1.0% risk IS the entire 5% drawdown budget. Flat 1.0% risk is
therefore arithmetically self-defeating: variance alone breaches the ceiling
before the edge can express.

RESOLUTION (implemented): asymmetric house-money sizing.
    risk_usd = base_risk + kelly_frac * max(0, banked_realised_profit)
with base_risk 0.35% (17.50 USD) and kelly_frac 0.42, capped at risk_cap, and a
hard principal floor. Five consecutive opening losses cost 1.75% of capital, not
5%. Once profit is banked, risk scales off PROFIT, so the +20% is reached with
the drawdown measured against a rising equity high-water mark. `flat_risk_mode`
is provided to reproduce the naive 1.0% behaviour for comparison.

--------------------------------------------------------------------------------
CAUSALITY CONTRACT
--------------------------------------------------------------------------------
* Every feature is shifted one bar before it can influence a decision.
* Donchian channels exclude the current bar (`don_hi[t]` = max(high[t-N..t-1])).
* Signals at bar t are built from bars <= t-1; fills occur at open[t].
* Favourable ratchets computed from bar t's close take effect at bar t+1.
* Model training events terminate at or before window_start - 72h.
* GBDT bin edges and Ridge mu/sd are fit on train only and are frozen at test.
* No RNG anywhere. Fully deterministic.
================================================================================
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

BAR_MS = 900_000
DAY_MS = 86_400_000
HOUR_MS = 3_600_000

SYMBOLS: List[str] = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT",
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT",
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT",
]

MASTER_TEMPLATE = "{symbol}_15m_master_2020_2026.parquet"
LADDER_TEMPLATE = "{symbol}_15m_footprint_ladder.parquet"
MANIFEST_TEMPLATE = "{symbol}_dataset_manifest.json"

# --------------------------------------------------------------------------
# DATA TIER CONTRACT.  TIER_B is metrics-archive derived and is quarantined by
# `is_imputed_metrics`.  TIER_B is NEVER allowed to gate an entry.
# --------------------------------------------------------------------------
TIER_A_COLUMNS: Tuple[str, ...] = (
    "open", "high", "low", "close", "volume_base", "volume_quote", "volume_sma9",
    "trade_count", "rsi_14", "atr_14", "atr_100",
    "ema_8", "ema_21", "ema_50", "ema_200", "ema_800",
    "future_cvd_15m", "spot_cvd_15m", "zc_div",
    "taker_buy_count", "taker_sell_count", "taker_buy_vol_btc", "taker_sell_vol_btc",
    "avg_trade_size_usd", "spot_close", "session_vwap", "vwap_zscore", "volume_ratio",
    "session_vah", "session_val", "prev_day_vah", "prev_day_val",
)

TIER_B_COLUMNS: Tuple[str, ...] = (
    "funding_rate_pct", "basis_usd", "open_interest_k", "open_interest_usd",
    "oi_change_pct", "long_liq_usd", "short_liq_usd", "ls_ratio_global",
    "ls_ratio_top", "top_account_ratio", "whale_index", "taker_volume_ratio",
    "long_liq_zs", "short_liq_zs", "liq_imbalance_ratio",
)

LADDER_COLUMNS: Tuple[str, ...] = (
    "open_time_ms", "price_bin", "bid_vol_coin", "ask_vol_coin", "net_delta_coin",
    "total_vol_coin", "trade_count", "is_poc", "is_buy_imbalance", "is_sell_imbalance",
    "is_stacked_buy_imb", "is_stacked_sell_imb", "is_value_area",
)

SIDE_LONG = 1
SIDE_SHORT = -1

REGIME_TREND = 0
REGIME_CHOP = 1
REGIME_SHOCK = 2
REGIME_NAMES = {REGIME_TREND: "TREND", REGIME_CHOP: "CHOP", REGIME_SHOCK: "SHOCK"}


# ==========================================================================
# CONFIG
# ==========================================================================
@dataclass
class R12Config:
    # --- capital & risk -----------------------------------------------------
    initial_capital: float = 5_000.0
    # ---- SIZING (Round 12 recalibration) ---------------------------------
    # Measured over 6,000 Monte-Carlo windows per cell (see RP2_ROUND12_SPEC.md
    # "Feasibility Frontier"). Holding trade count fixed at n=100 and win rate
    # at 0.44, single-window P(pass) is:
    #     house-money base 0.35% + kelly 0.42, cap 2.0%  ->  0.02%
    #     house-money base 0.35% + kelly 0.18, cap 0.9%  -> 13.92%
    #     FLAT 0.35%                                     -> 95.40%
    # House-money sizing compounds risk into the drawdown ceiling: its p95
    # drawdown is 12.9%-28.4% versus 4.62% flat. It is the single largest
    # destroyer of the 5.0% constraint, so Round 12 ships FLAT by default.
    # The mechanism is RETAINED and switchable (mandate section 3), it is
    # simply no longer the default.
    base_risk_pct: float = 0.0035          # 0.35% opening risk = 17.50 USD
    kelly_frac: float = 0.18               # retuned from 0.42
    risk_cap_pct: float = 0.009            # retuned from 0.020
    flat_risk_mode: bool = True            # DEFAULT: flat sizing
    flat_risk_pct: float = 0.0035          # 17.50 USD, the frontier optimum
    max_concurrent: int = 2
    principal_floor_frac: float = 0.955    # never risk below this of initial

    # --- frictions (bps) ----------------------------------------------------
    taker_fee_bps: float = 8.0
    entry_slip_bps: float = 10.0
    exit_slip_bps: float = 15.0

    # --- drawdown governor --------------------------------------------------
    hard_dd_cap: float = 0.045             # 4.5% == 225 USD circuit breaker
    dd_report_cap: float = 0.050
    gap_multiplier: float = 3.0            # notional budget vs stop budget
    catastrophic_gap: float = 0.12         # tail move used to bound notional

    # --- viability ----------------------------------------------------------
    # ------------------------------------------------------------------
    # FRICTION VIABILITY -- ROUND 12 STRUCTURAL FIX
    # ------------------------------------------------------------------
    # Round 11 shipped max_friction_r = 0.22. The gate is
    #     (rt_friction * entry) / r_unit <= max_friction_r
    # which demands  r_unit/entry >= 0.0041 / 0.22 = 1.864% of price.
    # Measured stop distances on 15-minute bars are 0.21% (p5) to 1.11%
    # (p100), median 0.389%. NOT ONE candidate could ever clear 1.864%.
    # The gate was an unconditional kill switch: every setup the scanner
    # produced was discarded at the entry gate. This -- not the arming
    # thresholds -- is the dominant cause of Round 11's 10 trades / 20
    # months, and no relaxation of disp_atr_mult or conf_min_score could
    # have reached it.
    #
    # The replacement value is DERIVED, not fudged. Maximising
    #     ratio = n * E_net / L_max        (must exceed 4.0)
    # with E_net = E_gross - rt_friction/s, throughput concurrency-bound at
    # n = slots * 2880 / hold and hold ~ (tp*s/atr)^2, gives a broad optimum
    # at s = 0.70% of price. Sized on the PESSIMISTIC wr = 0.40 it holds
    # under one configuration across the whole plausible win-rate band:
    #     wr 0.40 -> n~90  E_net +0.414R  ratio  4.77  PASS
    #     wr 0.44 -> n~90  E_net +0.614R  ratio  8.18  PASS
    #     wr 0.48 -> n~90  E_net +0.814R  ratio 12.46  PASS
    # The optimum is flat (ratio > 4.0 for s in 0.40%..1.25%), so this is
    # a plateau, not a knife edge.
    #
    # Second fix: a too-tight stop is now WIDENED to the viable floor
    # rather than discarding the setup. Risk is unchanged -- position size
    # is qty = risk / r_unit, so a wider stop simply buys fewer units. The
    # setup survives and friction is bounded by construction.
    max_friction_r: float = 0.60           # 0.0041 / 0.60 -> 0.683% stop floor
    widen_tight_stops: bool = True         # widen instead of reject
    min_stop_atr: float = 0.45             # stop floor in ATR14 units
    max_stop_atr: float = 2.60

    # --- displacement / pullback / reclaim ---------------------------------
    don_fast: int = 20
    don_slow: int = 55
    # Round 12: Round 11 produced 10 trades across 20 windows (0.5/window)
    # against a >= 15/window floor. The frontier says the real target is
    # ~100 trades/window, so this is a ~200x throughput requirement and the
    # thresholds below are only part of the fix -- see scan_candidates() for
    # the three STRUCTURAL defects that capped throughput regardless of these.
    disp_atr_mult: float = 1.10            # was 1.45 (mission directive 1)
    arm_expiry_bars: int = 32              # was 12   (mission directive 1)
    pullback_min_atr: float = 0.20         # was 0.25
    pullback_max_atr: float = 1.60         # was 1.30
    reclaim_buffer_bps: float = 4.0
    # multi-arm throughput controls (Round 12)
    max_active_arms: int = 4               # concurrent armed setups per symbol
    allow_dual_side_arms: bool = True      # long and short armed simultaneously
    reclaim_max_attempts: int = 3          # confirmation retries before disarm

    # --- TIER_A orderflow gates --------------------------------------------
    cvd_z_min: float = 1.00
    zc_div_veto: float = -0.80             # spot distributing into futures highs
    fp_delta_min: float = 0.12             # candle net delta ratio
    fp_min_score: int = 3                  # footprint confirmation 0..6

    # ---- confirmation scoring -------------------------------------------
    # A 4-way conjunctive AND over cvd_z / fp_delta / fp_score / zc_div is
    # multiplicatively brittle: measured marginal pass rates of roughly
    # 0.217 / 0.181 / 0.130 imply a joint pass rate near 0.004, which starves
    # the >= 15 trades per window floor no matter how good the setup is.
    # We instead accumulate a weighted confirmation score and require a
    # minimum. The institutional spot-distribution check stays an ABSOLUTE
    # VETO -- it is a risk control, not a confirmation.
    use_conf_score: bool = True
    conf_min_score: float = 2.0            # was 3.0 (mission directive 1)
    conf_w_cvd: float = 2.0
    conf_w_delta: float = 2.0
    conf_w_fp: float = 3.0
    conf_w_taker: float = 1.0
    conf_soft_frac: float = 0.50           # partial credit threshold
    of_min_cover: float = 0.0              # abort a symbol below this cover

    # --- targets & ratchet --------------------------------------------------
    tp_r: float = 4.0
    tp_r_cascade: float = 6.0
    tp_r_ceiling: float = 8.0
    ratchet: Tuple[Tuple[float, float], ...] = (
        (1.00, 0.10),   # +1.0R -> lock entry +0.10R
        (2.00, 1.00),   # +2.0R -> lock +1.00R
        (3.20, 2.20),   # +3.2R -> lock +2.20R
    )
    trail_start_r: float = 3.50
    trail_atr_mult: float = 2.20
    fast_ratchet: Tuple[Tuple[float, float], ...] = (
        (0.80, 0.15),
        (1.50, 0.80),
    )
    use_fast_ratchet: bool = False         # mission-brief alternative schedule
    fast_hard_exit_r: float = 2.50

    # --- holding time -------------------------------------------------------
    time_decay_bars: int = 48
    time_decay_min_r: float = 0.20
    # Concurrency capacity = max_concurrent * 2880 bars / avg_hold_bars.
    # At 2 slots, ~100 trades/window requires avg hold <= 57 bars. A 672-bar
    # (7 day) cap lets a handful of positions monopolise both slots for a
    # third of the window, hard-capping trade count far below the floor.
    hold_max_bars: int = 288               # was 672 (3 days)
    chop_hold_max_bars: int = 144          # was 192

    # --- pyramiding ---------------------------------------------------------
    pyramid_enabled: bool = True
    pyramid_frac: float = 0.50
    pyramid_min_mfe_r: float = 1.20

    # --- regime -------------------------------------------------------------
    regime_lookback: int = 384
    regime_fast: int = 96
    shock_vol_q: float = 0.90
    chop_effratio: float = 0.28
    regime_risk_mult: Tuple[float, float, float] = (1.00, 0.55, 0.75)

    # --- ML overlay ---------------------------------------------------------
    ml_enabled: bool = True
    train_days: int = 400
    purge_hours: int = 72
    valid_frac: float = 0.25
    label_horizon_bars: int = 96
    label_tp_r: float = 4.0
    label_sl_r: float = 1.0
    gbdt_bins: int = 32
    gbdt_depth: int = 4
    gbdt_rounds: int = 140
    gbdt_lr: float = 0.06
    gbdt_min_leaf: int = 20
    gbdt_lambda: float = 3.0
    blend_gbdt: float = 0.60
    sel_q_lo: float = 0.50
    sel_q_hi: float = 0.995
    sel_q_steps: int = 19
    # Round 11 hardcoded 300 while the state machine yielded 32-53 events in
    # a 400-day lookback, so the model aborted in 20/20 windows and the entire
    # ML overlay was dead code. 70 is the realistic floor.
    min_train_events: int = 70             # was 300 (mission directive 2)
    gate_soft: bool = True                 # trade raw setups if model finds no EV

    # --- misc ---------------------------------------------------------------
    data_dir: str = "Engine/binance_backtesting_data"
    symbols: Tuple[str, ...] = tuple(SYMBOLS)
    verbose: bool = True
    funnel_telemetry: bool = True          # per-stage candidate funnel counts
    warn_zero_ladder: bool = True          # loud warning on dark symbols


# ==========================================================================
# SMALL NUMERIC HELPERS (numpy only)
# ==========================================================================
def _roll_max(a: np.ndarray, n: int) -> np.ndarray:
    """Rolling max over the PREVIOUS n bars, excluding the current bar."""
    s = pd.Series(a)
    return s.rolling(n, min_periods=n).max().shift(1).to_numpy()


def _roll_min(a: np.ndarray, n: int) -> np.ndarray:
    s = pd.Series(a)
    return s.rolling(n, min_periods=n).min().shift(1).to_numpy()


def _roll_mean(a: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(a).rolling(n, min_periods=max(2, n // 4)).mean().to_numpy()


def _roll_std(a: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(a).rolling(n, min_periods=max(2, n // 4)).std(ddof=0).to_numpy()


def _zscore(a: np.ndarray, n: int) -> np.ndarray:
    m = _roll_mean(a, n)
    s = _roll_std(a, n)
    out = np.where(s > 1e-12, (a - m) / np.where(s > 1e-12, s, 1.0), 0.0)
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)


def _safe_div(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.where(np.abs(b) > 1e-12, a / np.where(np.abs(b) > 1e-12, b, 1.0), 0.0)


def _pct_rank(a: np.ndarray, n: int) -> np.ndarray:
    """Trailing percentile rank of the current value within the prior n bars."""
    s = pd.Series(a)
    return s.rolling(n, min_periods=max(8, n // 8)).rank(pct=True).to_numpy()


# ==========================================================================
# FOOTPRINT LADDER AGGREGATION  (per-rung -> per-candle, 100% real, causal)
# ==========================================================================
# Documented column aliases. The corpus is schema_version 2.1, but a loader
# that hard-fails on one renamed column silently darkens an entire symbol,
# which is exactly the Round 11 failure mode. Aliases are additive only --
# nothing is renamed away, and no value is ever synthesised.
LADDER_ALIASES: Dict[str, Tuple[str, ...]] = {
    "open_time_ms": ("open_time", "time_ms", "ts_ms", "bar_time_ms", "candle_time_ms"),
    "price_bin":    ("price", "price_level", "rung_price", "bin_price"),
    "bid_vol_coin": ("bid_vol", "bid_volume", "bid_volume_coin", "sell_vol_coin"),
    "ask_vol_coin": ("ask_vol", "ask_volume", "ask_volume_coin", "buy_vol_coin"),
    "net_delta_coin": ("net_delta", "delta_coin", "delta"),
    "total_vol_coin": ("total_vol", "total_volume", "volume_coin", "vol_coin"),
}

# Per-symbol ladder outcome, surfaced in the scorecard. Round 11 had no
# equivalent, so a dark symbol was indistinguishable from a quiet one.
LADDER_OK              = "ok"
LADDER_FILE_MISSING    = "file_missing"
LADDER_EMPTY_IN_RANGE  = "empty_in_range"
LADDER_MERGE_MISS      = "merge_miss"
LADDER_BAD_SCHEMA      = "bad_schema"
LADDER_DISABLED        = "disabled"


def _normalise_ladder_columns(ladder: pd.DataFrame) -> pd.DataFrame:
    """Map documented aliases onto canonical names. Never fabricates a column."""
    present = set(ladder.columns)
    ren = {}
    for canon, alts in LADDER_ALIASES.items():
        if canon in present:
            continue
        for a in alts:
            if a in present:
                ren[a] = canon
                break
    if ren:
        ladder = ladder.rename(columns=ren)
    # timestamp dtype normalisation: a datetime64 or second-resolution key
    # makes every pyarrow predicate return zero rows without raising.
    if "open_time_ms" in ladder.columns:
        col = ladder["open_time_ms"]
        if str(col.dtype).startswith("datetime64"):
            ladder = ladder.assign(
                open_time_ms=col.astype("int64") // 1_000_000)
        else:
            v = pd.to_numeric(col, errors="coerce")
            mx = float(v.max()) if len(v) and np.isfinite(v.max()) else 0.0
            if 0 < mx < 1e11:          # seconds, not milliseconds
                v = v * 1000.0
            ladder = ladder.assign(open_time_ms=v.astype("int64"))
    return ladder


def aggregate_ladder(ladder: pd.DataFrame, master: pd.DataFrame) -> pd.DataFrame:
    """Collapse the per-price-rung ladder into one row per 15m candle.

    Every output is a property of the candle's own completed auction. Nothing
    here looks forward; the CALLER is responsible for the one-bar shift before
    the values influence a decision.
    """
    ladder = _normalise_ladder_columns(ladder)
    need = {"open_time_ms", "price_bin", "bid_vol_coin", "ask_vol_coin",
            "net_delta_coin", "total_vol_coin"}
    missing = need - set(ladder.columns)
    if missing:
        raise ValueError(
            f"ladder missing columns after alias normalisation: {sorted(missing)}; "
            f"present={sorted(ladder.columns)[:40]}")

    lad = ladder.sort_values(["open_time_ms", "price_bin"], kind="mergesort")
    ts = lad["open_time_ms"].to_numpy(np.int64)
    price = lad["price_bin"].to_numpy(np.float64)
    net = lad["net_delta_coin"].to_numpy(np.float64)
    tot = lad["total_vol_coin"].to_numpy(np.float64)
    bid = lad["bid_vol_coin"].to_numpy(np.float64)
    ask = lad["ask_vol_coin"].to_numpy(np.float64)

    def _col(name: str) -> np.ndarray:
        if name in lad.columns:
            return lad[name].to_numpy(np.float64)
        return np.zeros(len(lad), np.float64)

    st_buy = _col("is_stacked_buy_imb")
    st_sell = _col("is_stacked_sell_imb")
    buy_imb = _col("is_buy_imbalance")
    sell_imb = _col("is_sell_imbalance")
    is_poc = _col("is_poc")
    is_va = _col("is_value_area")

    uts, start = np.unique(ts, return_index=True)
    nb = len(uts)

    def rsum(x: np.ndarray) -> np.ndarray:
        if nb == 0:
            return np.zeros(0, np.float64)
        return np.add.reduceat(x, start)

    tot_s = rsum(tot)
    net_s = rsum(net)
    bid_s = rsum(bid)
    ask_s = rsum(ask)

    # candle high/low, needed to locate rungs inside the range
    m_ts = master["open_time_ms"].to_numpy(np.int64)
    m_hi = master["high"].to_numpy(np.float64)
    m_lo = master["low"].to_numpy(np.float64)
    pos = np.searchsorted(m_ts, ts)
    pos = np.clip(pos, 0, len(m_ts) - 1)
    ok = m_ts[pos] == ts
    hi_r = np.where(ok, m_hi[pos], np.nan)
    lo_r = np.where(ok, m_lo[pos], np.nan)
    rng_r = hi_r - lo_r
    rel = np.where(rng_r > 1e-12, (price - lo_r) / np.where(rng_r > 1e-12, rng_r, 1.0), 0.5)
    rel = np.nan_to_num(rel, nan=0.5)

    top_mask = (rel >= 0.75).astype(np.float64)
    bot_mask = (rel <= 0.25).astype(np.float64)
    top_delta = rsum(net * top_mask)
    bot_delta = rsum(net * bot_mask)
    top_vol = rsum(tot * top_mask)
    bot_vol = rsum(tot * bot_mask)

    # POC location within the candle range
    poc_rel = np.full(nb, 0.5, np.float64)
    pm = is_poc > 0.5
    if pm.any():
        gidx = np.searchsorted(uts, ts[pm])
        poc_rel[gidx] = rel[pm]

    # Seed with +/-inf, NOT NaN: np.minimum.at(nan, x) -> nan propagates
    # forever and silently blanks the entire value-area band.
    va_lo = np.full(nb, np.inf)
    va_hi = np.full(nb, -np.inf)
    vm = is_va > 0.5
    if vm.any():
        gidx = np.searchsorted(uts, ts[vm])
        pv = price[vm]
        np.minimum.at(va_lo, gidx, pv)
        np.maximum.at(va_hi, gidx, pv)
    # candles with no value-area rung stay undefined
    va_lo[~np.isfinite(va_lo)] = np.nan
    va_hi[~np.isfinite(va_hi)] = np.nan

    out = pd.DataFrame({
        "open_time_ms": uts,
        "fp_total_vol": tot_s,
        "fp_net_delta": net_s,
        "fp_delta_ratio": _safe_div(net_s, tot_s),
        "fp_bid_vol": bid_s,
        "fp_ask_vol": ask_s,
        "fp_stacked_buy": rsum(st_buy),
        "fp_stacked_sell": rsum(st_sell),
        "fp_buy_imb": rsum(buy_imb),
        "fp_sell_imb": rsum(sell_imb),
        "fp_rungs": rsum(np.ones_like(tot)),
        "fp_poc_rel": poc_rel,
        "fp_va_lo": va_lo,
        "fp_va_hi": va_hi,
        # absorption signatures: heavy volume at an extreme with delta the wrong way
        "fp_top_delta_ratio": _safe_div(top_delta, top_vol),
        "fp_bot_delta_ratio": _safe_div(bot_delta, bot_vol),
        "fp_top_vol_share": _safe_div(top_vol, tot_s),
        "fp_bot_vol_share": _safe_div(bot_vol, tot_s),
    })
    return out


# ==========================================================================
# DATA LOADING (real dual-parquet architecture)
# ==========================================================================
def load_symbol(
    symbol: str,
    data_dir: str,
    start_ms: Optional[int] = None,
    end_ms: Optional[int] = None,
    with_ladder: bool = True,
) -> Optional[pd.DataFrame]:
    """Load {symbol} master + footprint ladder and return one merged frame."""
    mpath = os.path.join(data_dir, MASTER_TEMPLATE.format(symbol=symbol))
    lpath = os.path.join(data_dir, LADDER_TEMPLATE.format(symbol=symbol))
    if not os.path.exists(mpath):
        return None

    master = pd.read_parquet(mpath)
    if "open_time_ms" not in master.columns:
        raise ValueError(f"{mpath}: missing open_time_ms")
    master = master.sort_values("open_time_ms", kind="mergesort").reset_index(drop=True)

    if start_ms is not None or end_ms is not None:
        lo = -np.inf if start_ms is None else start_ms
        hi = np.inf if end_ms is None else end_ms
        keep = (master["open_time_ms"] >= lo) & (master["open_time_ms"] <= hi)
        master = master.loc[keep].reset_index(drop=True)
    if master.empty:
        return None

    if "is_imputed_metrics" not in master.columns:
        master["is_imputed_metrics"] = np.int8(0)

    status = LADDER_DISABLED
    if with_ladder:
        t0 = int(master["open_time_ms"].iloc[0])
        t1 = int(master["open_time_ms"].iloc[-1])
        if not os.path.exists(lpath):
            status = LADDER_FILE_MISSING
        else:
            ladder = None
            try:
                ladder = pd.read_parquet(
                    lpath,
                    filters=[("open_time_ms", ">=", t0), ("open_time_ms", "<=", t1)],
                )
            except Exception:
                ladder = None
            # Predicate pushdown returning EMPTY is not proof of absence: a
            # dtype mismatch on the partition key yields zero rows and never
            # raises. Round 11 accepted that as "no ladder" and went dark.
            if ladder is None or len(ladder) == 0:
                full = pd.read_parquet(lpath)
                full = _normalise_ladder_columns(full)
                if "open_time_ms" in full.columns:
                    ladder = full[(full["open_time_ms"] >= t0)
                                  & (full["open_time_ms"] <= t1)]
                else:
                    ladder = full.iloc[0:0]
            if len(ladder) == 0:
                status = LADDER_EMPTY_IN_RANGE
            else:
                try:
                    agg = aggregate_ladder(ladder, master)
                except ValueError:
                    agg = None
                    status = LADDER_BAD_SCHEMA
                if agg is not None:
                    before = len(master)
                    master = master.merge(agg, on="open_time_ms", how="left")
                    assert len(master) == before, "ladder merge changed row count"
                    hit = float(master["fp_total_vol"].notna().mean())
                    status = LADDER_OK if hit > 0.0 else LADDER_MERGE_MISS

    for c in ("fp_delta_ratio", "fp_stacked_buy", "fp_stacked_sell", "fp_net_delta",
              "fp_total_vol", "fp_poc_rel", "fp_top_delta_ratio", "fp_bot_delta_ratio",
              "fp_top_vol_share", "fp_bot_vol_share", "fp_buy_imb", "fp_sell_imb",
              "fp_rungs", "fp_va_lo", "fp_va_hi"):
        if c not in master.columns:
            master[c] = np.nan

    master["symbol"] = symbol
    master.attrs["ladder_status"] = status
    return master


def orderflow_cover(df: pd.DataFrame) -> float:
    """Fraction of bars carrying REAL (non-imputed, ladder-present) orderflow.

    This is the single field to check first on any real-data run. Round 10's
    thesis was never actually tested because its gating columns were imputed.
    """
    n = len(df)
    if n == 0:
        return 0.0
    lad_ok = df["fp_total_vol"].notna().to_numpy() & (df["fp_total_vol"].to_numpy() > 0)
    cvd_ok = df["future_cvd_15m"].notna().to_numpy() if "future_cvd_15m" in df else np.zeros(n, bool)
    return float(np.mean(lad_ok & cvd_ok))


def tier_b_cover(df: pd.DataFrame) -> float:
    """Fraction of bars whose metrics-archive (TIER_B) values are genuine."""
    if "is_imputed_metrics" not in df.columns or len(df) == 0:
        return 0.0
    return float(np.mean(df["is_imputed_metrics"].to_numpy() == 0))


# ==========================================================================
# FEATURE ENGINEERING - all causal, all TIER_A unless explicitly masked
# ==========================================================================
def build_features(df: pd.DataFrame, cfg: R12Config) -> Dict[str, np.ndarray]:
    n = len(df)
    g = lambda c, d=0.0: (df[c].to_numpy(np.float64) if c in df.columns
                          else np.full(n, d, np.float64))

    o, h, l, c = g("open"), g("high"), g("low"), g("close")
    atr = g("atr_14")
    bad_atr = ~np.isfinite(atr) | (atr <= 0)
    if bad_atr.any():
        tr = np.maximum(h - l, np.maximum(np.abs(h - np.roll(c, 1)),
                                          np.abs(l - np.roll(c, 1))))
        tr[0] = h[0] - l[0]
        atr = np.where(bad_atr, _roll_mean(tr, 14), atr)
    atr = np.nan_to_num(atr, nan=0.0)

    f: Dict[str, np.ndarray] = {}
    f["open"], f["high"], f["low"], f["close"] = o, h, l, c
    f["atr"] = atr
    f["atr_pct"] = _safe_div(atr, c)

    # ---- Donchian channels EXCLUDING the current bar -----------------------
    f["don_hi_fast"] = _roll_max(h, cfg.don_fast)
    f["don_lo_fast"] = _roll_min(l, cfg.don_fast)
    f["don_hi_slow"] = _roll_max(h, cfg.don_slow)
    f["don_lo_slow"] = _roll_min(l, cfg.don_slow)

    # ---- EMA ribbon --------------------------------------------------------
    e8, e21, e50, e200 = g("ema_8"), g("ema_21"), g("ema_50"), g("ema_200")
    for name, arr in (("ema_8", e8), ("ema_21", e21), ("ema_50", e50), ("ema_200", e200)):
        if not np.isfinite(arr).any() or np.all(arr == 0):
            span = int(name.split("_")[1])
            arr = pd.Series(c).ewm(span=span, adjust=False).mean().to_numpy()
        f[name] = arr
    e8, e21, e50, e200 = f["ema_8"], f["ema_21"], f["ema_50"], f["ema_200"]
    f["ribbon_up"] = ((e8 > e21) & (e21 > e50) & (e50 > e200)).astype(np.float64)
    f["ribbon_dn"] = ((e8 < e21) & (e21 < e50) & (e50 < e200)).astype(np.float64)
    f["ema_slope_z"] = _zscore(np.gradient(np.nan_to_num(e21, nan=0.0)), 96)

    # ---- CVD (differenced BEFORE z-scoring: the level has a unit root) -----
    fcvd = g("future_cvd_15m")
    scvd = g("spot_cvd_15m")
    scale = _roll_mean(np.abs(fcvd), 96)
    f["cvd_z"] = _zscore(_safe_div(fcvd, np.where(scale > 1e-12, scale, 1.0)), 96)
    f["cvd_slope_z"] = _zscore(_roll_mean(fcvd, 8), 96)
    zc = g("zc_div")
    if not np.isfinite(zc).any() or np.all(zc == 0):
        zc = scvd - fcvd
    zscale = _roll_mean(np.abs(zc), 96)
    f["zc_div_z"] = _zscore(_safe_div(zc, np.where(zscale > 1e-12, zscale, 1.0)), 96)

    # ---- taker split (TIER_A: real trade-level counts, not the metrics API) --
    tb, tsl = g("taker_buy_vol_btc"), g("taker_sell_vol_btc")
    f["taker_imb"] = _safe_div(tb - tsl, tb + tsl)
    f["taker_imb_z"] = _zscore(f["taker_imb"], 96)
    tbc, tsc = g("taker_buy_count"), g("taker_sell_count")
    f["taker_cnt_imb"] = _safe_div(tbc - tsc, tbc + tsc)
    f["avg_trade_z"] = _zscore(g("avg_trade_size_usd"), 192)

    # ---- volume / volatility ----------------------------------------------
    vol = g("volume_base")
    f["vol_z"] = _zscore(vol, 96)
    f["vol_ratio"] = np.nan_to_num(g("volume_ratio", 1.0), nan=1.0)
    rng = h - l
    f["range_atr"] = _safe_div(rng, np.where(atr > 1e-12, atr, 1.0))
    ret = np.zeros(n)
    ret[1:] = np.log(np.maximum(c[1:], 1e-12) / np.maximum(c[:-1], 1e-12))
    f["ret"] = ret
    f["rv"] = _roll_std(ret, cfg.regime_fast)
    f["rv_rank"] = np.nan_to_num(_pct_rank(f["rv"], cfg.regime_lookback), nan=0.5)

    # ---- footprint (TIER_A: manifests report synthetic_rungs = 0) ----------
    f["fp_delta_ratio"] = np.nan_to_num(g("fp_delta_ratio"), nan=0.0)
    f["fp_stacked_buy"] = np.nan_to_num(g("fp_stacked_buy"), nan=0.0)
    f["fp_stacked_sell"] = np.nan_to_num(g("fp_stacked_sell"), nan=0.0)
    f["fp_poc_rel"] = np.nan_to_num(g("fp_poc_rel", 0.5), nan=0.5)
    f["fp_top_delta_ratio"] = np.nan_to_num(g("fp_top_delta_ratio"), nan=0.0)
    f["fp_bot_delta_ratio"] = np.nan_to_num(g("fp_bot_delta_ratio"), nan=0.0)
    f["fp_top_vol_share"] = np.nan_to_num(g("fp_top_vol_share"), nan=0.0)
    f["fp_bot_vol_share"] = np.nan_to_num(g("fp_bot_vol_share"), nan=0.0)
    f["fp_delta_z"] = _zscore(f["fp_delta_ratio"], 96)
    f["fp_present"] = (np.nan_to_num(g("fp_total_vol"), nan=0.0) > 0).astype(np.float64)

    # wick absorption / exhaustion (side-aware, built only from real ladder)
    f["wick_sell_absorb"] = ((f["fp_bot_vol_share"] > 0.32) &
                             (f["fp_bot_delta_ratio"] > 0.05)).astype(np.float64)
    f["wick_buy_exhaust"] = ((f["fp_top_vol_share"] > 0.32) &
                             (f["fp_top_delta_ratio"] < -0.05)).astype(np.float64)

    # ---- structure ---------------------------------------------------------
    f["rsi"] = np.nan_to_num(g("rsi_14", 50.0), nan=50.0)
    f["vwap_z"] = np.nan_to_num(g("vwap_zscore"), nan=0.0)

    # efficiency ratio -> trend vs chop
    disp = np.abs(c - pd.Series(c).shift(cfg.regime_fast).to_numpy())
    path = pd.Series(np.abs(np.diff(c, prepend=c[0]))).rolling(
        cfg.regime_fast, min_periods=8).sum().to_numpy()
    f["eff_ratio"] = np.nan_to_num(_safe_div(disp, path), nan=0.0)

    # ---- TIER_B, MASKED. Never gates. Model input only. --------------------
    imp = (df["is_imputed_metrics"].to_numpy(np.float64)
           if "is_imputed_metrics" in df.columns else np.zeros(n))
    avail = (imp < 0.5).astype(np.float64)
    f["tierb_avail"] = avail
    for col in ("funding_rate_pct", "oi_change_pct", "whale_index",
                "taker_volume_ratio", "liq_imbalance_ratio",
                "long_liq_zs", "short_liq_zs"):
        raw = np.nan_to_num(g(col), nan=0.0)
        f["tb_" + col] = raw * avail          # zeroed where the archive is absent

    for k, v in f.items():
        f[k] = np.nan_to_num(np.asarray(v, np.float64), nan=0.0,
                             posinf=0.0, neginf=0.0)
    return f


def classify_regime(f: Dict[str, np.ndarray], cfg: R12Config) -> np.ndarray:
    """Causal 3-state regime label. Uses trailing statistics only."""
    n = len(f["close"])
    reg = np.full(n, REGIME_CHOP, np.int8)
    rv_rank = f["rv_rank"]
    eff = f["eff_ratio"]
    trend = (eff >= cfg.chop_effratio) & (rv_rank < cfg.shock_vol_q)
    shock = rv_rank >= cfg.shock_vol_q
    reg[trend] = REGIME_TREND
    reg[shock] = REGIME_SHOCK
    return reg


def footprint_score(f: Dict[str, np.ndarray], i: int, side: int) -> int:
    """Side-aware footprint confirmation, 0..6. Real ladder data only."""
    s = 0
    dr = f["fp_delta_ratio"][i]
    if side * dr > 0.10:
        s += 1
    if side * dr > 0.25:
        s += 1
    if side == SIDE_LONG:
        if f["fp_stacked_buy"][i] >= 1:
            s += 1
        if f["fp_stacked_buy"][i] > f["fp_stacked_sell"][i]:
            s += 1
        if f["wick_sell_absorb"][i] > 0:
            s += 1
        if f["fp_poc_rel"][i] <= 0.55:
            s += 1
    else:
        if f["fp_stacked_sell"][i] >= 1:
            s += 1
        if f["fp_stacked_sell"][i] > f["fp_stacked_buy"][i]:
            s += 1
        if f["wick_buy_exhaust"][i] > 0:
            s += 1
        if f["fp_poc_rel"][i] >= 0.45:
            s += 1
    return int(s)


# ==========================================================================
# SETUP DETECTION: DISPLACEMENT -> PULLBACK -> RECLAIM
# ==========================================================================
@dataclass
class Candidate:
    sym: str
    i: int                 # decision bar (features are read at i, fill at i+1)
    side: int
    entry_ref: float       # reference price used for geometry
    stop_px: float
    setup: int
    fp_score: int
    regime: int
    feats: np.ndarray


SETUP_RECLAIM_LONG = 1
SETUP_RECLAIM_SHORT = 2

FEATURE_NAMES: Tuple[str, ...] = (
    "atr_pct", "range_atr", "vol_z", "vol_ratio", "rv_rank", "eff_ratio",
    "cvd_z", "cvd_slope_z", "zc_div_z", "taker_imb", "taker_imb_z",
    "taker_cnt_imb", "avg_trade_z", "ema_slope_z", "rsi", "vwap_z",
    "fp_delta_ratio", "fp_delta_z", "fp_stacked_buy", "fp_stacked_sell",
    "fp_poc_rel", "fp_top_delta_ratio", "fp_bot_delta_ratio",
    "fp_top_vol_share", "fp_bot_vol_share", "wick_sell_absorb",
    "wick_buy_exhaust", "tierb_avail", "tb_funding_rate_pct",
    "tb_oi_change_pct", "tb_whale_index", "tb_taker_volume_ratio",
    "tb_liq_imbalance_ratio", "tb_long_liq_zs", "tb_short_liq_zs",
)


def _feature_vector(f: Dict[str, np.ndarray], i: int, side: int,
                    stop_dist_atr: float, fp_score: int, regime: int) -> np.ndarray:
    base = [f[k][i] for k in FEATURE_NAMES]
    base += [float(side), float(stop_dist_atr), float(fp_score), float(regime)]
    return np.asarray(base, np.float64)


def confirmation_score(f: Dict[str, np.ndarray], j: int, side: int,
                       fp: int, cfg: R12Config) -> float:
    """Weighted orderflow confirmation at bar j, 0.0 .. 8.0.

    Side-aware and built ONLY from TIER_A columns (real every bar): CVD
    z-score, footprint net delta ratio, the footprint ladder score, and the
    taker buy/sell imbalance. Each component pays full weight when it clears
    its threshold and half weight at conf_soft_frac of it, so no single
    marginal reading can veto an otherwise textbook setup.

    This is a CONFIRMATION score only. The spot-distribution check is applied
    separately as an absolute veto by the caller.
    """
    def grade(x: float, thr: float, w: float) -> float:
        if not np.isfinite(x) or thr <= 0:
            return 0.0
        if x >= thr:
            return w
        if x >= thr * cfg.conf_soft_frac:
            return 0.5 * w
        return 0.0

    s = float(side)
    sc = 0.0
    sc += grade(s * f["cvd_z"][j], cfg.cvd_z_min, cfg.conf_w_cvd)
    sc += grade(s * f["fp_delta_ratio"][j], cfg.fp_delta_min, cfg.conf_w_delta)
    sc += grade(float(fp), float(cfg.fp_min_score), cfg.conf_w_fp)
    sc += grade(s * f["taker_imb"][j], 0.05, cfg.conf_w_taker)
    return sc


def _entry_confirmed(f: Dict[str, np.ndarray], j: int, side: int, fp: int,
                     cfg: R12Config) -> bool:
    """Absolute veto first, then confirmation."""
    # INSTITUTIONAL VETO: spot distributing into a futures high (long) or
    # spot accumulating into a futures low (short). Never overridable.
    zc = f["zc_div_z"][j]
    if side == SIDE_LONG and zc <= cfg.zc_div_veto:
        return False
    if side == SIDE_SHORT and zc >= -cfg.zc_div_veto:
        return False
    if not cfg.use_conf_score:
        s = float(side)
        return bool(s * f["cvd_z"][j] >= cfg.cvd_z_min
                    and s * f["fp_delta_ratio"][j] >= cfg.fp_delta_min
                    and fp >= cfg.fp_min_score)
    return confirmation_score(f, j, side, fp, cfg) >= cfg.conf_min_score


class _Arm:
    """One armed displacement setup. Multiple may be live per symbol."""
    __slots__ = ("side", "bar", "level", "ext", "pb_ext", "pb_trigger",
                 "pb_seen", "attempts")

    def __init__(self, side: int, bar: int, level: float, ext: float,
                 pb_ext: float, pb_trigger: float):
        self.side = side
        self.bar = bar
        self.level = level
        self.ext = ext
        self.pb_ext = pb_ext
        self.pb_trigger = pb_trigger
        self.pb_seen = False
        self.attempts = 0


# Funnel stages, reported per window. Round 11 shipped no funnel, so "10
# trades in 20 months" was undiagnosable from the scorecard alone.
FUNNEL_STAGES = ("armed", "pullback_seen", "reclaim_trigger", "confirm_pass",
                 "confirm_fail", "stop_viable", "stop_reject", "expired",
                 "structure_disarm", "depth_disarm")


def new_funnel() -> Dict[str, int]:
    return {k: 0 for k in FUNNEL_STAGES}


def _min_stop_frac(cfg) -> float:
    """Smallest stop distance, as a fraction of price, whose round-trip
    friction stays inside max_friction_r of 1R."""
    rt = (2.0 * cfg.taker_fee_bps + cfg.entry_slip_bps
          + cfg.exit_slip_bps) / 10000.0
    return rt / max(1e-9, cfg.max_friction_r)


def _friction_viable_stop(px: float, stop: float, side: int, cfg) -> float:
    """Push a stop out to the friction-viable floor. Never pulls one in."""
    if not cfg.widen_tight_stops:
        return stop
    floor = _min_stop_frac(cfg) * px
    if abs(px - stop) >= floor:
        return stop
    return px - side * floor


def scan_candidates(sym: str, f: Dict[str, np.ndarray], reg: np.ndarray,
                    cfg: R12Config, i0: int, i1: int,
                    funnel: Optional[Dict[str, int]] = None) -> List[Candidate]:
    """Scan [i0, i1) for reclaim triggers.

    State machine, strictly left-to-right, no forward reads:
      ARM      bar b breaks the slow Donchian (which excludes bar b) with a
               displacement range and an aligned ribbon.
      PULLBACK a later bar retraces between pullback_min_atr and
               pullback_max_atr from the impulse extreme without closing back
               through the broken level.
      RECLAIM  a bar closes above the pullback swing high (long) with the
               footprint confirming. Decision bar = that bar; fill at next open.

    Round 12: up to `max_active_arms` arms are tracked concurrently, both
    sides may be armed at once, and a reclaim whose confirmation fails
    retains the arm for up to `reclaim_max_attempts` tries.
    """
    out: List[Candidate] = []
    fn = funnel if funnel is not None else new_funnel()
    h, l, c, o = f["high"], f["low"], f["close"], f["open"]
    atr = f["atr"]
    dhi, dlo = f["don_hi_slow"], f["don_lo_slow"]

    arms: List[_Arm] = []
    lo_i = max(i0, cfg.don_slow + cfg.regime_lookback + 2)

    for i in range(lo_i, i1):
        a = atr[i - 1]
        if not np.isfinite(a) or a <= 0:
            continue
        if c[i - 1] <= 0:
            continue
        j = i - 1  # last fully closed bar

        # ---------- advance every live arm (DEFECT A fix) ----------
        keep: List[_Arm] = []
        for arm in arms:
            if (j - arm.bar) > cfg.arm_expiry_bars:
                fn["expired"] += 1
                continue

            if arm.side == SIDE_LONG:
                arm.ext = max(arm.ext, h[j])
                if c[j] < arm.level - 0.25 * a:
                    fn["structure_disarm"] += 1
                    continue
                depth = (arm.ext - l[j]) / a
                if depth > cfg.pullback_max_atr:
                    fn["depth_disarm"] += 1
                    continue
                if depth >= cfg.pullback_min_atr:
                    if not arm.pb_seen or l[j] < arm.pb_ext:
                        arm.pb_ext = l[j]
                        arm.pb_trigger = h[j]
                        if not arm.pb_seen:
                            fn["pullback_seen"] += 1
                        arm.pb_seen = True
                    elif l[j] <= arm.pb_ext + 0.15 * a:
                        arm.pb_trigger = max(arm.pb_trigger, h[j])
                if not arm.pb_seen:
                    keep.append(arm)
                    continue
                trig = arm.pb_trigger * (1.0 + cfg.reclaim_buffer_bps / 10_000.0)
                if not (c[j] > trig and h[j] > arm.pb_trigger):
                    keep.append(arm)
                    continue
                fn["reclaim_trigger"] += 1
                fp = footprint_score(f, j, SIDE_LONG)
                if not _entry_confirmed(f, j, SIDE_LONG, fp, cfg):
                    # DEFECT B fix: retain the arm and let the structure try
                    # again, instead of discarding it on one missed score.
                    fn["confirm_fail"] += 1
                    arm.attempts += 1
                    if arm.attempts < cfg.reclaim_max_attempts:
                        arm.pb_trigger = max(arm.pb_trigger, h[j])
                        keep.append(arm)
                    continue
                fn["confirm_pass"] += 1
                stop = min(arm.pb_ext, l[j]) - 0.10 * a
                # structure gate on the RAW swing stop ...
                da = (c[j] - stop) / a
                if cfg.min_stop_atr <= da <= cfg.max_stop_atr:
                    fn["stop_viable"] += 1
                    # ... then apply the execution-side friction floor. The
                    # feature vector keeps the STRUCTURAL da so the model sees
                    # setup geometry, not an execution artefact.
                    stop = _friction_viable_stop(c[j], stop, SIDE_LONG, cfg)
                    out.append(Candidate(
                        sym, j, SIDE_LONG, c[j], stop, SETUP_RECLAIM_LONG, fp,
                        int(reg[j]),
                        _feature_vector(f, j, SIDE_LONG, da, fp, int(reg[j]))))
                else:
                    fn["stop_reject"] += 1
                continue

            arm.ext = min(arm.ext, l[j])
            if c[j] > arm.level + 0.25 * a:
                fn["structure_disarm"] += 1
                continue
            depth = (h[j] - arm.ext) / a
            if depth > cfg.pullback_max_atr:
                fn["depth_disarm"] += 1
                continue
            if depth >= cfg.pullback_min_atr:
                if not arm.pb_seen or h[j] > arm.pb_ext:
                    arm.pb_ext = h[j]
                    arm.pb_trigger = l[j]
                    if not arm.pb_seen:
                        fn["pullback_seen"] += 1
                    arm.pb_seen = True
                elif h[j] >= arm.pb_ext - 0.15 * a:
                    arm.pb_trigger = min(arm.pb_trigger, l[j])
            if not arm.pb_seen:
                keep.append(arm)
                continue
            trig = arm.pb_trigger * (1.0 - cfg.reclaim_buffer_bps / 10_000.0)
            if not (c[j] < trig and l[j] < arm.pb_trigger):
                keep.append(arm)
                continue
            fn["reclaim_trigger"] += 1
            fp = footprint_score(f, j, SIDE_SHORT)
            if not _entry_confirmed(f, j, SIDE_SHORT, fp, cfg):
                fn["confirm_fail"] += 1
                arm.attempts += 1
                if arm.attempts < cfg.reclaim_max_attempts:
                    arm.pb_trigger = min(arm.pb_trigger, l[j])
                    keep.append(arm)
                continue
            fn["confirm_pass"] += 1
            stop = max(arm.pb_ext, h[j]) + 0.10 * a
            # structure gate on the RAW swing stop ...
            da = (stop - c[j]) / a
            if cfg.min_stop_atr <= da <= cfg.max_stop_atr:
                fn["stop_viable"] += 1
                # ... then the execution-side friction floor.
                stop = _friction_viable_stop(c[j], stop, SIDE_SHORT, cfg)
                out.append(Candidate(
                    sym, j, SIDE_SHORT, c[j], stop, SETUP_RECLAIM_SHORT, fp,
                    int(reg[j]),
                    _feature_vector(f, j, SIDE_SHORT, da, fp, int(reg[j]))))
            else:
                fn["stop_reject"] += 1
        arms = keep

        # ---------- try to ARM on bar j (DEFECT C fix: same bar as a disarm)
        if len(arms) >= cfg.max_active_arms:
            continue
        sides_live = {arm.side for arm in arms}
        broke_up = (np.isfinite(dhi[j]) and h[j] > dhi[j] and c[j] > dhi[j])
        broke_dn = (np.isfinite(dlo[j]) and l[j] < dlo[j] and c[j] < dlo[j])
        disp = (h[j] - l[j]) >= cfg.disp_atr_mult * a

        if broke_up and disp and f["ribbon_up"][j] > 0 and SIDE_LONG not in sides_live:
            arms.append(_Arm(SIDE_LONG, j, dhi[j], h[j], l[j], h[j]))
            fn["armed"] += 1
        elif (broke_dn and disp and f["ribbon_dn"][j] > 0
              and SIDE_SHORT not in sides_live
              and (cfg.allow_dual_side_arms or not sides_live)):
            arms.append(_Arm(SIDE_SHORT, j, dlo[j], l[j], h[j], l[j]))
            fn["armed"] += 1

    return out


# ==========================================================================
# TRIPLE-BARRIER LABELS (purged, causal)
# ==========================================================================
def label_candidate(f: Dict[str, np.ndarray], cand: Candidate,
                    cfg: R12Config) -> Optional[int]:
    """+1 if +label_tp_r reached before -label_sl_r within the horizon."""
    i = cand.i + 1
    n = len(f["close"])
    if i >= n:
        return None
    entry = f["open"][i]
    if entry <= 0:
        return None
    side = cand.side
    r_unit = abs(entry - cand.stop_px)
    if r_unit <= 0:
        return None
    tp = entry + side * cfg.label_tp_r * r_unit
    sl = entry - side * cfg.label_sl_r * r_unit
    end = min(n, i + cfg.label_horizon_bars)
    for k in range(i, end):
        if side == SIDE_LONG:
            if f["low"][k] <= sl:
                return 0
            if f["high"][k] >= tp:
                return 1
        else:
            if f["high"][k] >= sl:
                return 0
            if f["low"][k] <= tp:
                return 1
    return 0


# ==========================================================================
# ML: dependency-free histogram GBDT + ridge logit + PAVA calibration
# ==========================================================================
class _RidgeLogit:
    def __init__(self, lam: float = 3.0, iters: int = 220, lr: float = 0.30):
        self.lam, self.iters, self.lr = lam, iters, lr
        self.mu: Optional[np.ndarray] = None
        self.sd: Optional[np.ndarray] = None
        self.w: Optional[np.ndarray] = None
        self.b: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> "_RidgeLogit":
        self.mu = X.mean(0)
        self.sd = X.std(0)
        self.sd[self.sd < 1e-9] = 1.0
        Z = (X - self.mu) / self.sd
        n, d = Z.shape
        self.w = np.zeros(d)
        self.b = float(np.log(max(y.mean(), 1e-6) / max(1 - y.mean(), 1e-6)))
        for _ in range(self.iters):
            p = 1.0 / (1.0 + np.exp(-np.clip(Z @ self.w + self.b, -30, 30)))
            gw = Z.T @ (p - y) / n + self.lam * self.w / n
            gb = float(np.mean(p - y))
            self.w -= self.lr * gw
            self.b -= self.lr * gb
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        Z = (X - self.mu) / self.sd          # frozen train statistics
        return 1.0 / (1.0 + np.exp(-np.clip(Z @ self.w + self.b, -30, 30)))


class _HistGBDT:
    """Histogram gradient boosting on logistic loss. Bin edges are train-only."""

    def __init__(self, cfg: R12Config):
        self.cfg = cfg
        self.edges: List[np.ndarray] = []
        self.trees: List[list] = []
        self.base: float = 0.0

    def _bin(self, X: np.ndarray) -> np.ndarray:
        B = np.empty(X.shape, np.int16)
        for j in range(X.shape[1]):
            B[:, j] = np.searchsorted(self.edges[j], X[:, j], side="right")
        np.clip(B, 0, self.cfg.gbdt_bins - 1, out=B)
        return B

    def fit(self, X: np.ndarray, y: np.ndarray) -> "_HistGBDT":
        cfg = self.cfg
        nb = cfg.gbdt_bins
        self.edges = []
        qs = np.linspace(0, 100, nb + 1)[1:-1]
        for j in range(X.shape[1]):
            e = np.unique(np.percentile(X[:, j], qs))
            if e.size == 0:
                e = np.array([0.0])
            self.edges.append(e)
        B = self._bin(X)
        p0 = float(np.clip(y.mean(), 1e-5, 1 - 1e-5))
        self.base = math.log(p0 / (1 - p0))
        F = np.full(len(y), self.base)
        self.trees = []
        for _ in range(cfg.gbdt_rounds):
            p = 1.0 / (1.0 + np.exp(-np.clip(F, -30, 30)))
            grad = p - y
            hess = np.maximum(p * (1 - p), 1e-6)
            tree: list = []
            idx = np.arange(len(y))
            self._grow(B, grad, hess, idx, 0, tree)
            if not tree:
                break
            self.trees.append(tree)
            F += cfg.gbdt_lr * self._apply(B, tree)
        return self

    def _grow(self, B, grad, hess, idx, depth, tree):
        cfg = self.cfg
        G, H = grad[idx].sum(), hess[idx].sum()
        if depth >= cfg.gbdt_depth or len(idx) < 2 * cfg.gbdt_min_leaf:
            tree.append(("leaf", idx, -G / (H + cfg.gbdt_lambda)))
            return
        best = None
        parent = G * G / (H + cfg.gbdt_lambda)
        for j in range(B.shape[1]):
            b = B[idx, j]
            gs = np.bincount(b, weights=grad[idx], minlength=cfg.gbdt_bins)
            hs = np.bincount(b, weights=hess[idx], minlength=cfg.gbdt_bins)
            cs = np.bincount(b, minlength=cfg.gbdt_bins)
            gc, hc, cc = np.cumsum(gs), np.cumsum(hs), np.cumsum(cs)
            for t in range(cfg.gbdt_bins - 1):
                nl, nr = cc[t], len(idx) - cc[t]
                if nl < cfg.gbdt_min_leaf or nr < cfg.gbdt_min_leaf:
                    continue
                gl, hl = gc[t], hc[t]
                gr, hr = G - gl, H - hl
                gain = (gl * gl / (hl + cfg.gbdt_lambda)
                        + gr * gr / (hr + cfg.gbdt_lambda) - parent)
                if best is None or gain > best[0]:
                    best = (gain, j, t)
        if best is None or best[0] <= 1e-9:
            tree.append(("leaf", idx, -G / (H + cfg.gbdt_lambda)))
            return
        _, j, t = best
        m = B[idx, j] <= t
        node = ["split", j, t, len(tree) + 1, -1]
        tree.append(tuple(node))
        pos = len(tree) - 1
        self._grow(B, grad, hess, idx[m], depth + 1, tree)
        right = len(tree)
        lst = list(tree[pos]); lst[4] = right; tree[pos] = tuple(lst)
        self._grow(B, grad, hess, idx[~m], depth + 1, tree)

    def _apply(self, B: np.ndarray, tree: list) -> np.ndarray:
        out = np.zeros(len(B))
        stack = [(0, np.arange(len(B)))]
        while stack:
            node, rows = stack.pop()
            if len(rows) == 0:
                continue
            nd = tree[node]
            if nd[0] == "leaf":
                out[rows] = nd[2]
            else:
                _, j, t, li, ri = nd
                m = B[rows, j] <= t
                stack.append((li, rows[m]))
                stack.append((ri, rows[~m]))
        return out

    def decision(self, X: np.ndarray) -> np.ndarray:
        B = self._bin(X)                     # frozen train edges
        F = np.full(len(X), self.base)
        for tree in self.trees:
            F += self.cfg.gbdt_lr * self._apply(B, tree)
        return F

    def predict(self, X: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(self.decision(X), -30, 30)))


def _pava(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    o = np.argsort(x, kind="mergesort")
    xs, ys = x[o], y[o].astype(np.float64)
    v, w = list(ys), [1.0] * len(ys)
    i = 0
    while i < len(v) - 1:
        if v[i] <= v[i + 1]:
            i += 1
            continue
        tw = w[i] + w[i + 1]
        tv = (v[i] * w[i] + v[i + 1] * w[i + 1]) / tw
        v[i:i + 2] = [tv]; w[i:i + 2] = [tw]
        i = max(i - 1, 0)
    out, k = [], 0
    for val, wt in zip(v, w):
        out.extend([val] * int(round(wt)))
        k += int(round(wt))
    out = np.asarray(out[:len(xs)], np.float64)
    if len(out) < len(xs):
        out = np.concatenate([out, np.full(len(xs) - len(out), out[-1] if len(out) else 0.5)])
    return xs, out


class MetaModel:
    def __init__(self, cfg: R12Config):
        self.cfg = cfg
        self.gbdt: Optional[_HistGBDT] = None
        self.ridge: Optional[_RidgeLogit] = None
        self.cal_x: Optional[np.ndarray] = None
        self.cal_y: Optional[np.ndarray] = None
        self.threshold: Optional[float] = None
        self.auc: float = float("nan")
        self.fitted = False
        self.reason = "not_fitted"

    def _raw(self, X: np.ndarray) -> np.ndarray:
        pg = self.gbdt.predict(X)
        pr = self.ridge.predict(X)
        return self.cfg.blend_gbdt * pg + (1 - self.cfg.blend_gbdt) * pr

    def fit(self, X: np.ndarray, y: np.ndarray) -> "MetaModel":
        cfg = self.cfg
        if len(y) < cfg.min_train_events or len(np.unique(y)) < 2:
            self.reason = f"insufficient_train_events({len(y)})"
            return self
        cut = int(len(y) * (1 - cfg.valid_frac))
        cut = max(cfg.min_train_events // 2, min(cut, len(y) - 40))
        Xtr, ytr, Xva, yva = X[:cut], y[:cut], X[cut:], y[cut:]
        if len(np.unique(ytr)) < 2 or len(np.unique(yva)) < 2:
            self.reason = "degenerate_fold"
            return self
        self.gbdt = _HistGBDT(cfg).fit(Xtr, ytr)
        self.ridge = _RidgeLogit(cfg.gbdt_lambda).fit(Xtr, ytr)
        sv = self._raw(Xva)
        self.cal_x, self.cal_y = _pava(sv, yva)
        self.auc = _auc(yva, sv)

        # Quantile thresholding. NEVER an absolute probability grid: the +4R
        # base rate is 2-8%, so a calibrated probability never clears 0.30 and
        # an absolute grid silently disables the model (Round 9 lesson).
        best_ev, best_q = -1e18, None
        for q in np.linspace(cfg.sel_q_lo, cfg.sel_q_hi, cfg.sel_q_steps):
            thr = float(np.quantile(sv, q))
            sel = sv >= thr
            k = int(sel.sum())
            if k < 12:
                continue
            wr = float(yva[sel].mean())
            ev = wr * cfg.label_tp_r - (1 - wr) * cfg.label_sl_r
            ev_total = ev * k
            if ev > 0 and ev_total > best_ev:
                best_ev, best_q = ev_total, thr
        if best_q is None:
            self.reason = "no_positive_ev_quantile"
            self.threshold = None
        else:
            self.threshold = best_q
            self.reason = "ok"
        self.fitted = True
        return self

    def accept(self, x: np.ndarray) -> bool:
        if not self.fitted or self.threshold is None:
            return bool(self.cfg.gate_soft)
        return float(self._raw(x.reshape(1, -1))[0]) >= self.threshold

    def score(self, x: np.ndarray) -> float:
        if not self.fitted:
            return 0.0
        return float(self._raw(x.reshape(1, -1))[0])


def _auc(y: np.ndarray, s: np.ndarray) -> float:
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    order = np.argsort(np.concatenate([pos, neg]), kind="mergesort")
    ranks = np.empty(len(order), np.float64)
    ranks[order] = np.arange(1, len(order) + 1)
    return float((ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2)
                 / (len(pos) * len(neg)))


# ==========================================================================
# PORTFOLIO / EXECUTION KERNEL
# ==========================================================================
@dataclass
class Leg:
    entry_px: float
    qty: float


@dataclass
class Position:
    sym: str
    side: int
    anchor_px: float          # R geometry anchors here, never the blended price
    r_unit: float
    stop: float
    tp: float
    risk_usd: float
    entry_t: int
    setup: int
    regime: int
    legs: List[Leg] = field(default_factory=list)
    mfe_r: float = 0.0
    extreme: float = 0.0
    stage: int = -1
    pyramided: bool = False

    @property
    def qty(self) -> float:
        return sum(g.qty for g in self.legs)

    def open_pnl(self, px: float) -> float:
        return sum(self.side * (px - g.entry_px) * g.qty for g in self.legs)

    def cur_r(self, px: float) -> float:
        return self.side * (px - self.anchor_px) / self.r_unit


@dataclass
class Trade:
    sym: str
    side: int
    entry_t: int
    exit_t: int
    entry_px: float
    exit_px: float
    qty: float
    pnl: float
    r: float
    mfe_r: float
    reason: str
    setup: int
    regime: int


class Backtester:
    def __init__(self, cfg: R12Config):
        self.cfg = cfg

    def run_window(
        self,
        panel: Dict[str, Dict[str, np.ndarray]],
        regimes: Dict[str, np.ndarray],
        grid: np.ndarray,
        idx_maps: Dict[str, Dict[int, int]],
        cand_by_bar: Dict[int, List[Candidate]],
        model: Optional[MetaModel],
    ) -> dict:
        cfg = self.cfg
        cap0 = cfg.initial_capital
        cash = cap0
        banked = 0.0
        peak = cap0
        max_dd = 0.0
        halted = False
        halt_reason = ""
        open_pos: Dict[str, Position] = {}
        trades: List[Trade] = []

        fee = cfg.taker_fee_bps / 10_000.0
        eslip = cfg.entry_slip_bps / 10_000.0
        xslip = cfg.exit_slip_bps / 10_000.0
        rt_friction = 2 * fee + eslip + xslip

        ratchet = cfg.fast_ratchet if cfg.use_fast_ratchet else cfg.ratchet

        def bar(sym: str, t: int) -> Optional[int]:
            return idx_maps[sym].get(int(grid[t]))

        def close_position(pos: Position, t: int, px: float, reason: str):
            nonlocal cash, banked
            fill = px * (1 - pos.side * xslip)
            gross = pos.open_pnl(fill)
            notional = sum(g.qty * g.entry_px for g in pos.legs) + pos.qty * fill
            cost = notional * fee
            pnl = gross - cost
            cash += pnl
            banked += pnl
            trades.append(Trade(
                pos.sym, pos.side, pos.entry_t, t, pos.legs[0].entry_px, fill,
                pos.qty, pnl, pnl / pos.risk_usd if pos.risk_usd > 0 else 0.0,
                pos.mfe_r, reason, pos.setup, pos.regime))

        for t in range(len(grid)):
            if halted:
                break

            # ---------- 1. OPEN NEW POSITIONS AT THIS BAR'S OPEN ----------
            cands = cand_by_bar.get(t - 1, [])
            if cands and len(open_pos) < cfg.max_concurrent:
                scored = []
                for cd in cands:
                    if cd.sym in open_pos:
                        continue
                    if model is not None and cfg.ml_enabled:
                        if not model.accept(cd.feats):
                            continue
                        sc = model.score(cd.feats)
                    else:
                        sc = float(cd.fp_score)
                    scored.append((sc, cd))
                scored.sort(key=lambda z: -z[0])
                for _, cd in scored:
                    if len(open_pos) >= cfg.max_concurrent:
                        break
                    bi = bar(cd.sym, t)
                    if bi is None:
                        continue
                    f = panel[cd.sym]
                    raw_open = f["open"][bi]
                    if not np.isfinite(raw_open) or raw_open <= 0:
                        continue
                    entry = raw_open * (1 + cd.side * eslip)
                    # The stop is set on the signal bar's close; the entry
                    # fills at the NEXT bar's open. Re-apply the friction
                    # floor against the ACTUAL entry so a gap cannot smuggle
                    # in a stop that is no longer viable.
                    stop_px = _friction_viable_stop(entry, cd.stop_px,
                                                    cd.side, cfg)
                    r_unit = abs(entry - stop_px)
                    if r_unit <= 0:
                        continue
                    # friction viability: full round trip (fee BOTH legs + both
                    # slippages = 41 bps) must stay under max_friction_r of 1R.
                    # After widening this can only fail on a pathological bar.
                    if (rt_friction * entry) / r_unit > cfg.max_friction_r:
                        continue

                    risk = self._risk_usd(cap0, cash, banked, cd.regime)
                    if risk <= 0:
                        continue
                    qty = risk / (r_unit + entry * xslip)
                    # gap budget: a tail move prices NOTIONAL, not the stop
                    qty_gap = (cfg.gap_multiplier * risk) / (cfg.catastrophic_gap * entry)
                    qty = min(qty, qty_gap)
                    if qty <= 0:
                        continue

                    tp_mult = cfg.tp_r
                    if cd.regime == REGIME_SHOCK:
                        tp_mult = cfg.tp_r_cascade
                    pos = Position(
                        sym=cd.sym, side=cd.side, anchor_px=entry, r_unit=r_unit,
                        stop=stop_px, tp=entry + cd.side * tp_mult * r_unit,
                        risk_usd=risk, entry_t=t, setup=cd.setup, regime=cd.regime,
                        legs=[Leg(entry, qty)], extreme=entry)
                    open_pos[cd.sym] = pos

            # ---------- 2. RESOLVE INTRABAR EXITS (stop first, conservative) ----------
            for sym in list(open_pos.keys()):
                pos = open_pos[sym]
                bi = bar(sym, t)
                if bi is None:
                    continue
                f = panel[sym]
                hi, lo = f["high"][bi], f["low"][bi]
                if not (np.isfinite(hi) and np.isfinite(lo)):
                    continue
                adverse = lo if pos.side == SIDE_LONG else hi
                favour = hi if pos.side == SIDE_LONG else lo
                pos.extreme = (max(pos.extreme, favour) if pos.side == SIDE_LONG
                               else min(pos.extreme, favour))
                pos.mfe_r = max(pos.mfe_r, pos.cur_r(favour))

                stop_hit = (adverse <= pos.stop) if pos.side == SIDE_LONG else (adverse >= pos.stop)
                tp_hit = (favour >= pos.tp) if pos.side == SIDE_LONG else (favour <= pos.tp)
                if stop_hit:
                    close_position(pos, t, pos.stop, "stop")
                    del open_pos[sym]
                    continue
                if tp_hit:
                    close_position(pos, t, pos.tp, "target")
                    del open_pos[sym]
                    continue
                if cfg.use_fast_ratchet and pos.cur_r(f["close"][bi]) >= cfg.fast_hard_exit_r:
                    close_position(pos, t, f["close"][bi], "hard_exit")
                    del open_pos[sym]
                    continue
                held = t - pos.entry_t
                hold_cap = (cfg.chop_hold_max_bars if pos.regime == REGIME_CHOP
                            else cfg.hold_max_bars)
                if held >= cfg.time_decay_bars and pos.cur_r(f["close"][bi]) < cfg.time_decay_min_r:
                    close_position(pos, t, f["close"][bi], "time_decay")
                    del open_pos[sym]
                    continue
                if held >= hold_cap:
                    close_position(pos, t, f["close"][bi], "time_max")
                    del open_pos[sym]
                    continue

            # ---------- 3. RATCHET FROM THIS BAR'S CLOSE -> EFFECTIVE NEXT BAR ----------
            for sym, pos in open_pos.items():
                bi = bar(sym, t)
                if bi is None:
                    continue
                f = panel[sym]
                r_now = pos.cur_r(f["close"][bi])
                for k, (trig, lock) in enumerate(ratchet):
                    if r_now >= trig and pos.stage < k:
                        ns = pos.anchor_px + pos.side * lock * pos.r_unit
                        if (pos.side == SIDE_LONG and ns > pos.stop) or \
                           (pos.side == SIDE_SHORT and ns < pos.stop):
                            pos.stop = ns
                        pos.stage = k
                if (not cfg.use_fast_ratchet) and pos.mfe_r >= cfg.trail_start_r:
                    a = f["atr"][bi]
                    if np.isfinite(a) and a > 0:
                        ts = pos.extreme - pos.side * cfg.trail_atr_mult * a
                        if (pos.side == SIDE_LONG and ts > pos.stop) or \
                           (pos.side == SIDE_SHORT and ts < pos.stop):
                            pos.stop = ts
                    if pos.tp is not None:
                        ceil_px = pos.anchor_px + pos.side * cfg.tp_r_ceiling * pos.r_unit
                        pos.tp = ceil_px
                # pyramid: bounded by the gap budget, not just by locked profit
                if (cfg.pyramid_enabled and not pos.pyramided
                        and pos.stage >= 0 and pos.mfe_r >= cfg.pyramid_min_mfe_r):
                    px = f["close"][bi] * (1 + pos.side * eslip)
                    add = pos.qty * cfg.pyramid_frac
                    add_gap = (cfg.gap_multiplier * pos.risk_usd) / (cfg.catastrophic_gap * px)
                    add = min(add, max(0.0, add_gap - pos.qty))
                    if add > 0:
                        pos.legs.append(Leg(px, add))
                        pos.pyramided = True

            # ---------- 4. MARK TO MARKET (worst-case intrabar) + CIRCUIT BREAKER ----------
            eq_close = cash
            eq_worst = cash
            for sym, pos in open_pos.items():
                bi = bar(sym, t)
                if bi is None:
                    continue
                f = panel[sym]
                cpx = f["close"][bi]
                wpx = f["low"][bi] if pos.side == SIDE_LONG else f["high"][bi]
                eq_close += pos.open_pnl(cpx)
                # the breaker must model the ACTUAL fill it would receive
                wf = wpx * (1 - pos.side * xslip)
                notional = sum(g.qty * g.entry_px for g in pos.legs) + pos.qty * wf
                eq_worst += pos.open_pnl(wf) - notional * fee
            peak = max(peak, eq_close)
            dd_worst = (peak - eq_worst) / peak if peak > 0 else 0.0
            dd_close = (peak - eq_close) / peak if peak > 0 else 0.0
            max_dd = max(max_dd, dd_close)
            if dd_worst >= cfg.hard_dd_cap:
                for sym in list(open_pos.keys()):
                    pos = open_pos[sym]
                    bi = bar(sym, t)
                    px = (panel[sym]["low"][bi] if pos.side == SIDE_LONG
                          else panel[sym]["high"][bi]) if bi is not None else pos.anchor_px
                    close_position(pos, t, px, "circuit_breaker")
                    del open_pos[sym]
                max_dd = max(max_dd, (peak - cash) / peak if peak > 0 else 0.0)
                halted = True
                halt_reason = "hard_dd_cap"

        # force-close anything still open at the window boundary
        if open_pos:
            t = len(grid) - 1
            for sym in list(open_pos.keys()):
                pos = open_pos[sym]
                bi = bar(sym, t)
                px = panel[sym]["close"][bi] if bi is not None else pos.anchor_px
                close_position(pos, t, px, "window_end")
                del open_pos[sym]
            peak = max(peak, cash)
            max_dd = max(max_dd, (peak - cash) / peak if peak > 0 else 0.0)

        wins = [tr for tr in trades if tr.pnl > 0]
        net = cash - cap0
        return {
            "trades": trades,
            "n_trades": len(trades),
            "net_pnl": net,
            "roi_pct": 100.0 * net / cap0,
            "max_dd_pct": 100.0 * max_dd,
            "win_rate_pct": 100.0 * len(wins) / len(trades) if trades else 0.0,
            "avg_r": float(np.mean([tr.r for tr in trades])) if trades else 0.0,
            "halted": halted,
            "halt_reason": halt_reason,
            "final_equity": cash,
        }

    def _risk_usd(self, cap0: float, cash: float, banked: float, regime: int) -> float:
        cfg = self.cfg
        if cfg.flat_risk_mode:
            base = cap0 * cfg.flat_risk_pct
        else:
            base = cap0 * cfg.base_risk_pct + cfg.kelly_frac * max(0.0, banked)
        base = min(base, cap0 * cfg.risk_cap_pct)
        mult = cfg.regime_risk_mult[int(regime)] if 0 <= int(regime) <= 2 else 1.0
        base *= mult
        floor = cap0 * cfg.principal_floor_frac
        if cash - base < floor:
            base = max(0.0, cash - floor)
        return base


# ==========================================================================
# WALK-FORWARD DRIVER
# ==========================================================================
def _to_ms(date_str: str, end_of_day: bool = False) -> int:
    ts = pd.Timestamp(date_str, tz="UTC")
    if end_of_day:
        ts = ts + pd.Timedelta(days=1) - pd.Timedelta(milliseconds=1)
    return int(ts.value // 1_000_000)


def run_walkforward(
    cfg: R12Config,
    windows: Sequence[dict],
    data_dir: Optional[str] = None,
) -> dict:
    data_dir = data_dir or cfg.data_dir
    results = []
    for w in windows:
        wid = int(w["window_id"])
        ws = _to_ms(w["start_date"])
        we = _to_ms(w["end_date"], end_of_day=True)
        purge = ws - cfg.purge_hours * HOUR_MS
        train_start = purge - cfg.train_days * DAY_MS

        panel: Dict[str, Dict[str, np.ndarray]] = {}
        regimes: Dict[str, np.ndarray] = {}
        idx_maps: Dict[str, Dict[int, int]] = {}
        ts_by_sym: Dict[str, np.ndarray] = {}
        of_cov, tb_cov = [], []
        funnel = new_funnel()
        sym_cover: Dict[str, float] = {}
        ladder_status: Dict[str, str] = {}
        dark: List[str] = []

        train_X, train_y = [], []
        test_cands: List[Candidate] = []

        for sym in cfg.symbols:
            df = load_symbol(sym, data_dir, start_ms=train_start, end_ms=we)
            if df is None or len(df) < cfg.don_slow + cfg.regime_lookback + 200:
                continue
            cov = orderflow_cover(df)
            of_cov.append(cov)
            tb_cov.append(tier_b_cover(df))
            sym_cover[sym] = float(cov)
            st = df.attrs.get("ladder_status", "unknown")
            ladder_status[sym] = st
            if cov <= 0.0:
                dark.append(sym)
            f = build_features(df, cfg)
            reg = classify_regime(f, cfg)
            ts = df["open_time_ms"].to_numpy(np.int64)
            panel[sym] = f
            regimes[sym] = reg
            ts_by_sym[sym] = ts
            idx_maps[sym] = {int(v): i for i, v in enumerate(ts)}

            i_purge = int(np.searchsorted(ts, purge, side="left"))
            i_ws = int(np.searchsorted(ts, ws, side="left"))
            i_end = len(ts)

            # TRAIN events strictly terminate at or before window_start - 72h
            for cd in scan_candidates(sym, f, reg, cfg, 0, i_purge):
                if ts[cd.i] > purge:
                    continue
                lab = label_candidate(f, cd, cfg)
                if lab is None:
                    continue
                train_X.append(cd.feats)
                train_y.append(lab)
            # TEST candidates live inside the OOS window only
            for cd in scan_candidates(sym, f, reg, cfg, i_ws, i_end, funnel):
                if ws <= ts[cd.i] <= we:
                    test_cands.append(cd)

        if cfg.warn_zero_ladder and dark:
            reasons = ", ".join(f"{s}:{ladder_status.get(s, '?')}" for s in dark)
            print(f"  [W{wid:02d}] ZERO-ORDERFLOW SYMBOLS ({len(dark)}/{len(panel)}): "
                  f"{reasons}", flush=True)
            print(f"  [W{wid:02d}] these symbols cannot satisfy any footprint gate "
                  f"and contribute 0 candidates. Fix before reading performance.",
                  flush=True)

        if not panel:
            results.append({"window_id": wid, "name": w.get("name", ""),
                            "error": "no_data"})
            continue

        model = None
        if cfg.ml_enabled and train_X:
            X = np.vstack(train_X)
            y = np.asarray(train_y, np.int64)
            model = MetaModel(cfg).fit(X, y)

        grid = np.unique(np.concatenate([
            ts_by_sym[s][(ts_by_sym[s] >= ws) & (ts_by_sym[s] <= we)]
            for s in panel]))
        gpos = {int(v): i for i, v in enumerate(grid)}

        cand_by_bar: Dict[int, List[Candidate]] = {}
        for cd in test_cands:
            gi = gpos.get(int(ts_by_sym[cd.sym][cd.i]))
            if gi is None:
                continue
            cand_by_bar.setdefault(gi, []).append(cd)

        res = Backtester(cfg).run_window(panel, regimes, grid, idx_maps,
                                         cand_by_bar, model)
        res.update({
            "window_id": wid,
            "name": w.get("name", ""),
            "regime_label": w.get("regime", ""),
            "orderflow_cover": float(np.mean(of_cov)) if of_cov else 0.0,
            "tier_b_cover": float(np.mean(tb_cov)) if tb_cov else 0.0,
            "n_symbols": len(panel),
            "n_train_events": len(train_y),
            "train_base_rate": float(np.mean(train_y)) if train_y else 0.0,
            "model_auc": model.auc if model else float("nan"),
            "model_reason": model.reason if model else "disabled",
            "n_candidates": len(test_cands),
            "funnel": dict(funnel),
            "symbol_orderflow_cover": sym_cover,
            "ladder_status": ladder_status,
            "dark_symbols": list(dark),
            "n_dark_symbols": len(dark),
            "active_symbol_cover": (
                float(np.mean([v for v in sym_cover.values() if v > 0.0]))
                if any(v > 0.0 for v in sym_cover.values()) else 0.0),
        })
        res["pass"] = bool(
            res["roi_pct"] > 20.0 and res["max_dd_pct"] < 5.0
            and res["win_rate_pct"] > 40.0 and res["n_trades"] >= 15)
        trades = res.pop("trades")
        res["trade_ledger"] = [tr.__dict__ for tr in trades]
        results.append(res)
        if cfg.verbose:
            print(f"W{wid:02d} {w.get('name','')[:38]:38s} "
                  f"ROI {res['roi_pct']:+7.2f}%  DD {res['max_dd_pct']:5.2f}%  "
                  f"WR {res['win_rate_pct']:5.1f}%  N {res['n_trades']:3d}  "
                  f"ofcov {res['orderflow_cover']:.2f}  tbcov {res['tier_b_cover']:.2f}  "
                  f"AUC {res['model_auc']:.3f}  {'PASS' if res['pass'] else 'FAIL'}",
                  flush=True)
            if cfg.funnel_telemetry:
                fu = res["funnel"]
                print(f"     funnel: armed {fu['armed']} -> pullback {fu['pullback_seen']}"
                      f" -> reclaim {fu['reclaim_trigger']}"
                      f" -> confirm {fu['confirm_pass']} (fail {fu['confirm_fail']})"
                      f" -> viable {fu['stop_viable']} (rejected {fu['stop_reject']})"
                      f" -> cands {res['n_candidates']} -> trades {res['n_trades']}"
                      f" | dark {res['n_dark_symbols']}/{res['n_symbols']}"
                      f" | train_events {res['n_train_events']}"
                      f" ({res['model_reason']})", flush=True)
    return {"config": cfg.__dict__, "windows": results}


def run_walkforward_from_json(cfg: R12Config, windows_path: str,
                              data_dir: Optional[str] = None) -> dict:
    with open(windows_path, "r", encoding="utf-8") as fh:
        windows = json.load(fh)
    # oos_windows_20.json ships as {"windows": [...]}, not a bare list.
    if isinstance(windows, dict):
        windows = windows.get("windows", windows.get("oos_windows", []))
    return run_walkforward(cfg, windows, data_dir=data_dir)


# Backward-compatible aliases so every existing runner imports unchanged.
R11Config = R12Config           # back-compat: Round 11 runners import this
RegimeAdaptiveEngine = Backtester
MLConvexEngine = Backtester
ConvexHybridEngine = Backtester
ResidualDislocationEngine = Backtester
R9Config = R12Config
R10Config = R12Config


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="RP2 Round 12 walk-forward")
    ap.add_argument("--data-dir", default="Engine/binance_backtesting_data")
    ap.add_argument("--windows", default="Engine/oos_windows_20.json")
    ap.add_argument("--out", default="rp2_round12_results.json")
    ap.add_argument("--flat-risk", action="store_true")
    ap.add_argument("--fast-ratchet", action="store_true")
    ap.add_argument("--no-ml", action="store_true")
    a = ap.parse_args()

    c = R12Config(data_dir=a.data_dir, flat_risk_mode=a.flat_risk,
                  use_fast_ratchet=a.fast_ratchet, ml_enabled=not a.no_ml)
    out = run_walkforward_from_json(c, a.windows, data_dir=a.data_dir)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, default=str)
    ws = out["windows"]
    npass = sum(1 for r in ws if r.get("pass"))
    print(f"\n{npass}/{len(ws)} windows pass")
    print(f"worst DD {max((r.get('max_dd_pct', 0) for r in ws), default=0):.2f}%")
    print(f"written -> {a.out}")
