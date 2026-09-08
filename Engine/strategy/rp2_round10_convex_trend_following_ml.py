"""
===============================================================================
 RP2 ROUND 10 -- ADAPTIVE CONVEX TREND-FOLLOWING ENGINE
 ON ORDERFLOW & FOOTPRINT STEROIDS
 rp2_round10_convex_trend_following_ml.py
===============================================================================

 Supersedes: rp2_round9_ml_convex_engine.py
 Consumes  : Engine/ml/footprint_confirmation.py (logic ported, vectorised)

 WHAT CHANGED FROM ROUND 9 AND WHY
 ---------------------------------
 Round 9 established the causal ML contract and the risk physics. Its
 remaining structural limit was that EVERY setup was a FADE (liquidation
 exhaust, funding squeeze, volume shock all sell strength / buy weakness).
 A fade's payoff is bounded by the dislocation it fades, so the +4R barrier
 was reachable but the 10R-25R multi-day directional waves that crypto
 perpetual regimes actually produce were structurally unreachable.

   (1) NEW PRIMARY SETUP -- TREND BREAKOUT IGNITION (SETUP_TREND).
       Donchian(20/55) channel break with an EMA20>EMA50>EMA200 ribbon,
       taken ONLY on confirmed orderflow aggression:
           is_stacked_buy_imb  OR  (taker_volume_ratio >= 1.25 AND cvd > 0)
       This is the filter that removes low-volume chop traps: a breakout
       with no aggressive volume lifting the book is a liquidity vacuum,
       not a trend.

   (2) CVD ACCELERATION + DIVERGENCE VETO.
       Longs require expanding CVD (cvd_z >= 1.2) and are VETOED when price
       prints a new high while spot CVD distributes (zc_div <= -0.8) --
       the classic institutional distribution trap.

   (3) LIQUIDATION SQUEEZE ROCKET FUEL (SETUP_TREND_SQZ).
       A long breakout coinciding with short_liq_zs >= 1.5 means forced
       buy-ins are supplying the fuel. Those are tagged for extended
       targets: 6.0R, or 8.0R when the squeeze is extreme.

   (4) ANTI-SUFFOCATION RATCHET -- the critical Round 9 lesson.
       In the real-data Round 9 run, 7 trades reached +1.5R to +3.07R MFE
       and were then stopped at +0.60R because the lock sat too close.
       Round 10 widens every tier and defers the chandelier:
           +1.0R -> BE +0.10R      (was +0.8R -> +0.15R)
           +2.0R -> entry +1.00R   (was +1.5R -> +0.80R)
           +3.2R -> entry +2.20R   (was +2.5R -> +2.00R)
           past +3.5R -> chandelier at 2.2 x ATR_14 from the running extreme
       The chandelier is 2.2 ATR (was 1.20), which is what lets a 5R-8R
       runner mature instead of being scratched by noise.

   (5) TREND POSITIONS BREATHE ON A DIFFERENT CLOCK.
       Fades are mean-reverting and must resolve fast (24-bar decay, 96-bar
       cap). A multi-day wave cannot. Trend setups get a 48-bar decay and a
       672-bar (7-day) cap, applied per-setup.

   (6) PYRAMIDING ON HOUSE MONEY.
       One 0.50x add once the stop is locked at breakeven-or-better, so the
       add can never convert a locked winner into a loser. R-geometry is
       anchored to the ORIGINAL entry (`anchor_px`), never to the blended
       average, so the ratchet cannot jump when a leg is added.

 GRACEFUL DEGRADATION (IMPORTANT)
 --------------------------------
 Every orderflow / footprint column is OPTIONAL. When a column is absent the
 engine substitutes a documented causal proxy and reports which real feeds
 were actually present via `orderflow_cover` on the scorecard. Never read a
 pass/fail without reading that field -- a run with `orderflow_cover` near 0
 is not testing the orderflow thesis at all.

 Columns consumed when present (per-symbol frame or via `extra=` dict):
   future_cvd_15m, spot_cvd_15m, zc_div, taker_volume_ratio,
   taker_buy_vol_btc, taker_sell_vol_btc,
   is_stacked_buy_imb, is_stacked_sell_imb, poc_shift, absorption_ratio,
   wick_sell_absorb, wick_buy_exhaust, close_pos,
   long_liq_zs, short_liq_zs, top_account_ratio, ls_ratio_top, whale_index,
   open_interest_usd, oi_change_pct, funding_rate, rsi_14, atr_14

 THE ML CONTRACT (unchanged from Round 9, still strictly causal)
 ---------------------------------------------------------------
   For window k spanning [t_start, t_end]:
     train on events with t <= t_start - 72h        (PURGE)
     validate on the last `val_frac` of that span   (also < t_start - 72h)
     select the probability threshold p* on validation ONLY, as a QUANTILE
       of the validation score distribution (never an absolute probability --
       the +4R base rate is ~3-10%, so absolute cut-offs are unreachable)
     predict on [t_start, t_end], never refit inside the window

 DEPENDENCIES
 ------------
   Required: numpy, pandas.  Optional: scikit-learn (never required).

 PUBLIC API (drop-in compatible with Round 7 / 8 / 9 runners)
 ------------------------------------------------------------
   eng = TrendConvexEngine()
   res = eng.run_window(per_symbol, funding=..., oi=..., extra=...,
                        win_start=..., win_end=..., window_id="W01")
   card = eng.run_walkforward(per_symbol, windows, fail_fast=True)

   Aliases exported for older runners:
     MLConvexEngine = ConvexHybridEngine = ResidualDislocationEngine
       = TrendConvexEngine
===============================================================================
"""

from __future__ import annotations

import json
import math
import warnings
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)

try:                                    # optional, never required
    from sklearn.ensemble import HistGradientBoostingClassifier as _SkHGB
    _HAS_SK = True
except Exception:                       # pragma: no cover
    _SkHGB = None
    _HAS_SK = False

__all__ = ["TrendConvexEngine", "MLConvexEngine", "ConvexHybridEngine",
           "ResidualDislocationEngine", "FootprintConfirmation", "Panel",
           "R10Config", "R9Config", "RiskConfig", "run_walkforward_from_json"]

BARS_PER_DAY = 96                       # 15-minute bars
BARS_PER_HOUR = 4

SETUP_LIQ, SETUP_LEADLAG, SETUP_FUND, SETUP_VOL = 1, 2, 3, 4
SETUP_TREND, SETUP_TREND_SQZ = 5, 6
SETUP_NAME = {0: "none", 1: "liq_exhaust", 2: "lead_lag",
              3: "funding_squeeze", 4: "vol_shock",
              5: "trend_ignition", 6: "trend_squeeze"}
# Setups that ride a directional wave rather than fade a dislocation. They
# need a slower clock and a looser trail; everything else is a fade.
TREND_SETUPS = frozenset((SETUP_TREND, SETUP_TREND_SQZ))


# ===========================================================================
# 0. CONFIGURATION
# ===========================================================================
@dataclass
class RiskConfig:
    """Directive 3.E -- dynamic house-money / non-linear position sizing."""
    initial_capital: float = 5_000.0
    base_risk: float = 25.00            # 0.50% of 5,000
    kelly_frac: float = 0.40            # Risk = 25 + 0.40 * max(0, realised)
    max_risk_per_trade: float = 200.00  # hard cap
    # Hard capital-protection floor: never open risk that could take realised
    # equity through 4.5% drawdown. 5000 * (1 - 0.045) = 4775.
    capital_floor: float = 4_775.00
    drawdown_limit: float = 0.045       # intrabar circuit breaker (4.5% / $225)
    dd_defense_trigger: float = 0.028   # de-risk before the breaker trips
    drawdown_defense_risk: float = 12.50
    max_positions: int = 2              # across all 18 symbols
    max_symbol_leverage: float = 8.0
    max_gross_leverage: float = 12.0
    # ---- gap-aware drawdown budget -------------------------------------
    # The circuit breaker fires only once a breach is OBSERVED, and can then
    # exit no better than that bar's extreme. So a 4.5% trigger can realise
    # more than 5.0% if open risk is large when the gap hits. We therefore
    # cap *total exposed risk* against the remaining distance to the hard
    # ceiling, inflated by a gap multiplier for overshoot beyond the stop.
    hard_dd_cap: float = 0.045          # dollars-from-peak budget
    # Empirically (W11 synthetic) a stop can be gapped through at 2.63x its
    # width on a violent bar, so budgeting at 2.0x is not conservative enough.
    # 3.0x covers every observed overshoot with margin.
    gap_multiplier: float = 3.0
    # Stop-distance sizing cannot bound loss when the stop is GAPPED THROUGH:
    # a wick can travel any distance. So we additionally bound each position by
    # its TAIL NOTIONAL exposure -- the loss it would take on a catastrophic
    # adverse move -- against the remaining drawdown budget. This is what makes
    # the <5% ceiling hold structurally rather than empirically.
    catastrophic_gap: float = 0.12      # 12% instantaneous adverse move
    # ---- pyramiding (Round 10 directive 3.5) ---------------------------
    # One add-on leg at 0.50x the original size, allowed ONLY once the stop
    # is locked at breakeven-or-better, so the add can never turn a locked
    # winner into a loser. Sized against the SAME budget as a fresh entry.
    pyramid_frac: float = 0.50
    pyramid_max_legs: int = 1
    pyramid_min_mfe_r: float = 1.20     # must have proven itself first


@dataclass
class R10Config:
    # ---------- frictions (exact, mandatory, 33 bps round trip) ----------
    taker_fee: float = 0.0008           # 8 bps per side on notional
    entry_slippage: float = 0.0010      # 10 bps, applied ONCE in price space
    exit_slippage: float = 0.0015       # 15 bps, applied ONCE in price space
    # Round-trip friction may never exceed this fraction of 1R. This is the
    # single most important guard in the engine: it is what makes low-vol chop
    # windows (W07, W18) survivable instead of a friction bleed.
    max_friction_r: float = 0.30        # => 1R must be >= ~137 bps

    # ---------- Directive 3.A: event-conditioned sampling ----------
    ev_liq_z: float = 1.5               # long_liq_zs / short_liq_zs >= 1.5
    ev_funding_ann: float = 0.50        # |funding_annualised| >= 50%
    ev_lead_z: float = 1.8              # |lead_impulse_z| >= 1.8
    ev_volume_z: float = 2.0            # volume_z >= 2.0
    flush_lookback: int = 8             # bars used to find the flush extreme

    # ---------- Directive 3.A: triple barrier ----------
    barrier_up_r: float = 4.0           # +4.0R profit barrier
    barrier_dn_r: float = 1.0           # -1.0R stop barrier
    barrier_bars: int = 24              # 24 bars == 6 hours vertical barrier

    # ---------- Directive 3.D: payoff geometry ----------
    stop_atr_mult: float = 0.20         # flush extreme -/+ 0.20 * ATR_14
    atr_bars: int = 14                  # ATR_14 on the 15m grid (for the stop)
    tp_r: float = 4.0                   # primary target
    tp_r_cascade: float = 6.0           # extreme liquidation cascade target
    tp_r_rocket: float = 8.0            # squeeze-fuelled trend breakout
    cascade_liq_z: float = 3.0
    cascade_oi_drop: float = -0.15

    # ---------- Round 10: TREND IGNITION + ORDERFLOW CONFIRMATION ----------
    donchian_fast: int = 20             # 20-bar channel break
    donchian_slow: int = 55             # 55-bar channel break (stronger)
    ema_fast: int = 20
    ema_mid: int = 50
    ema_slow: int = 200
    trend_stop_atr: float = 1.60        # trend stop is ATR-based, not a wick
    trend_min_adx_z: float = -0.25      # weak persistence filter
    # orderflow ignition gate (directive 3.1)
    of_taker_ratio: float = 1.25        # taker buy/sell >= 1.25 (or <= 1/1.25)
    of_cvd_z_min: float = 1.20          # expanding CVD (directive 3.2)
    of_zc_div_veto: float = 0.80        # veto |zc_div| against the trade side
    # footprint confirmation (Engine/ml/footprint_confirmation.py)
    fp_min_score: int = 3               # conf_score >= 3 of 6
    fp_required_for_trend: bool = True  # trend entries must be confirmed
    # liquidation squeeze rocket fuel (directive 3.3)
    sqz_liq_z: float = 1.50
    sqz_liq_z_extreme: float = 3.00
    # anti-retracement ratchet: (gain_r, new stop at entry + lock_r)
    # ---- ANTI-SUFFOCATION RATCHET (Round 10 directive 3.4) ----
    # Round 9 real-data evidence: 7 trades reached +1.5R..+3.07R MFE and were
    # stopped at +0.60R. Every tier is widened and the chandelier deferred so
    # that a 5R-8R runner has room to mature.
    ratchet: Tuple[Tuple[float, float], ...] = (
        (1.00, 0.10),                   # BE + 0.10R
        (2.00, 1.00),                   # profit lock
        (3.20, 2.20),                   # protect the approach to 4R+
    )
    trail_start_r: float = 3.50         # chandelier arms only past +3.5R
    trail_atr_mult: float = 2.20        # 2.2 x ATR_14 from running extreme
    time_decay_bars: int = 24           # exit if < +0.2R after 24 bars
    time_decay_min_r: float = 0.20
    hold_max_bars: int = 96             # absolute cap (24h) -- FADES
    # Trend waves run for days; a fade's clock would scratch them at noise.
    trend_time_decay_bars: int = 48     # 12h
    trend_hold_max_bars: int = 672      # 7 days
    # 1R may never be degenerate relative to the instrument's daily range
    r_floor_frac_datr: float = 0.22
    r_cap_frac_datr: float = 1.40

    # ---------- Directive 3.B: ML ----------
    train_days: int = 400               # in-sample span before the purge
    purge_hours: int = 72               # strict causal purge
    val_frac: float = 0.25              # tail of train used for threshold pick
    max_train_events: int = 80_000
    min_train_events: int = 400
    gbdt_rounds: int = 140
    gbdt_lr: float = 0.06
    gbdt_max_depth: int = 4             # <= 4 (directive)
    gbdt_min_leaf: int = 20             # >= 20 (directive)
    gbdt_reg_lambda: float = 3.0        # >= 3.0 (directive)
    gbdt_min_split_gain: float = 1.0    # acts as reg_alpha >= 1.0
    gbdt_bins: int = 32
    ridge_l2: float = 3.0
    ridge_iters: int = 220
    ridge_lr: float = 0.35
    ensemble_w_gbdt: float = 0.60       # blend weight, remainder to ridge
    # dynamic threshold search
    # Threshold search is over QUANTILES of the validation probability
    # distribution, not absolute probabilities -- the +4R barrier base rate
    # is ~3-10%, so absolute cut-offs like 0.30 are unreachable by a
    # calibrated model and would disable the classifier entirely.
    sel_q_lo: float = 0.50              # consider the top 50% ... 
    sel_q_hi: float = 0.995             # ... down to the top 0.5% of signals
    p_grid_n: int = 49
    target_trades_per_window: int = 15
    trade_headroom: float = 2.2         # sample this many x the floor
    min_val_events: int = 60
    # if the model finds no edge, fall back to the raw event sampler rather
    # than silently sitting flat (the Round 6 failure mode) -- but report it.
    soft_fallback: bool = True
    fallback_p_quantile: float = 0.70

    # ---------- execution ----------
    top_k_per_bar: int = 2
    cooldown_bars: int = BARS_PER_HOUR * 2
    warmup_bars: int = BARS_PER_DAY * 3


@dataclass
class Position:
    symbol: str
    col: int
    side: int                           # +1 long, -1 short
    setup: int
    r_px: float                         # 1R in price units
    anchor_px: float                    # ORIGINAL entry -- all R geometry
    stop_px: float
    tp_px: float
    tp_r: float
    entry_bar: int
    legs: List[Tuple[float, float]] = field(default_factory=list)
    fees_paid: float = 0.0
    funding_pnl: float = 0.0
    risk_d: float = 0.0                 # dollars at risk at entry
    tier: int = 0
    mfe_r: float = 0.0
    p_hat: float = 0.0
    conf_score: int = 0
    n_adds: int = 0
    run_ext: float = float("nan")       # running high (long) / low (short)

    @property
    def qty(self) -> float:
        return sum(q for _, q in self.legs)

    @property
    def entry_px(self) -> float:
        n = self.qty
        return (sum(e * q for e, q in self.legs) / n) if n > 0 else float("nan")

    @property
    def notional(self) -> float:
        return abs(self.entry_px * self.qty)

    def open_pnl(self, px: float) -> float:
        """NET open P&L: gross + funding - every fee accrued so far. Keeping a
        single definition of P&L is what makes the equity curve, the intrabar
        drawdown check and the trade ledger reconcile exactly."""
        return (sum(self.side * (px - e) * q for e, q in self.legs)
                + self.funding_pnl - self.fees_paid)


# ===========================================================================
# 1. PANEL -- timestamp-aligned cube
# ===========================================================================
_EXTRA_COLS = (
    # --- legacy (Round 7-9) ------------------------------------------------
    "long_liq_zs", "short_liq_zs", "open_interest", "oi",
    "funding_rate", "cvd", "taker_buy_volume", "wick_sell_absorb",
    "wick_buy_absorb", "rsi_14", "vwap_zscore", "dist_to_vwap_zs", "atr_14",
    # --- Round 10 A: delta / CVD dynamics ---------------------------------
    "future_cvd_15m", "spot_cvd_15m", "zc_div", "taker_volume_ratio",
    "taker_buy_vol_btc", "taker_sell_vol_btc",
    # --- Round 10 B: footprint ladder microstructure ----------------------
    "is_stacked_buy_imb", "is_stacked_sell_imb", "poc_shift",
    "absorption_ratio", "wick_buy_exhaust", "close_pos",
    # --- Round 10 C: institutional positioning ----------------------------
    "top_account_ratio", "ls_ratio_top", "whale_index",
    "open_interest_usd", "oi_change_pct",
)


class Panel:
    """Timestamp-aligned OHLCV(+extras) cube. Prices are NEVER forward-filled:
    a symbol missing a bar is untradeable on that bar (`valid` mask)."""

    __slots__ = ("index", "symbols", "open", "high", "low", "close",
                 "volume", "valid", "T", "N", "extras")

    def __init__(self, per_symbol: Dict[str, pd.DataFrame],
                 extra: Optional[Dict[str, pd.DataFrame]] = None):
        """`extra` lets orderflow/footprint feeds arrive as a separate
        {symbol -> frame} mapping instead of being merged into the OHLCV
        frames. Columns are joined on the timestamp index; a symbol missing
        a feed simply falls back to the documented proxy."""
        if extra:
            merged = {}
            for k, d in per_symbol.items():
                e = extra.get(k)
                if e is None or len(e) == 0:
                    merged[k] = d
                    continue
                e = e.copy()
                e.index = pd.DatetimeIndex(pd.to_datetime(e.index))
                e = e[~e.index.duplicated(keep="last")].sort_index()
                add = [c for c in e.columns if c not in d.columns]
                merged[k] = d.join(e[add], how="left") if add else d
            per_symbol = merged
        clean: Dict[str, pd.DataFrame] = {}
        for s, d in per_symbol.items():
            if d is None or len(d) == 0:
                continue
            d = d.copy()
            d.index = pd.DatetimeIndex(pd.to_datetime(d.index))
            d = d[~d.index.duplicated(keep="last")].sort_index()
            clean[s] = d
        if not clean:
            raise ValueError("Panel: no usable symbol frames")

        idx = None
        for d in clean.values():
            idx = d.index if idx is None else idx.union(d.index)
        self.index = pd.DatetimeIndex(idx)
        self.symbols = sorted(clean.keys())
        self.T, self.N = len(self.index), len(self.symbols)

        def cube(col: str) -> Optional[np.ndarray]:
            if not any(col in d.columns for d in clean.values()):
                return None
            m = np.full((self.T, self.N), np.nan, dtype=np.float64)
            for j, s in enumerate(self.symbols):
                d = clean[s]
                if col in d.columns:
                    m[:, j] = (pd.to_numeric(d[col], errors="coerce")
                               .reindex(self.index).to_numpy(dtype=np.float64))
            return m

        self.open, self.high = cube("open"), cube("high")
        self.low, self.close = cube("low"), cube("close")
        vol = cube("volume")
        self.volume = vol if vol is not None else np.ones((self.T, self.N))
        if not np.any(np.isfinite(self.volume)):
            self.volume = np.ones((self.T, self.N))
        self.extras = {c: v for c, v in ((c, cube(c)) for c in _EXTRA_COLS)
                       if v is not None}
        self.valid = (np.isfinite(self.open) & np.isfinite(self.high)
                      & np.isfinite(self.low) & np.isfinite(self.close)
                      & (self.close > 0))

    def slice(self, start, end) -> "Panel":
        lo = int(self.index.searchsorted(pd.Timestamp(start), side="left"))
        hi = int(self.index.searchsorted(pd.Timestamp(end), side="right"))
        p = Panel.__new__(Panel)
        p.index = self.index[lo:hi]
        p.symbols = list(self.symbols)
        p.open, p.high = self.open[lo:hi], self.high[lo:hi]
        p.low, p.close = self.low[lo:hi], self.close[lo:hi]
        p.volume, p.valid = self.volume[lo:hi], self.valid[lo:hi]
        p.extras = {k: v[lo:hi] for k, v in self.extras.items()}
        p.T, p.N = p.close.shape
        return p


# ===========================================================================
# 2. CAUSAL PRIMITIVES  (carried over from Round 8, invariant-verified)
# ===========================================================================
def _roll(a: np.ndarray, w: int, how: str) -> np.ndarray:
    r = pd.DataFrame(a).rolling(w, min_periods=max(2, w // 4))
    return {"mean": r.mean, "std": (lambda: r.std(ddof=0)), "sum": r.sum,
            "max": r.max, "min": r.min, "median": r.median}[how]().to_numpy()


def _z(a: np.ndarray, w: int) -> np.ndarray:
    mu, sd = _roll(a, w, "mean"), _roll(a, w, "std")
    return np.clip(np.nan_to_num((a - mu) / np.where(sd > 1e-12, sd, np.nan),
                                 nan=0.0, posinf=0.0, neginf=0.0), -8.0, 8.0)


def _xs_pctile(a: np.ndarray) -> np.ndarray:
    """Row-wise cross-sectional percentile in (0,1]; NaN -> 0.5."""
    fin = np.isfinite(a)
    b = np.where(fin, a, np.inf)
    order = np.argsort(b, axis=1, kind="stable")
    ranks = np.empty_like(order)
    rows = np.arange(a.shape[0])[:, None]
    ranks[rows, order] = np.arange(a.shape[1])[None, :]
    cnt = fin.sum(axis=1, keepdims=True)
    out = (ranks + 1.0) / np.maximum(cnt, 1.0)
    return np.where(fin & (cnt > 1), out, 0.5)


def causal_daily_atr(panel: Panel, period: int = 14) -> np.ndarray:
    """TRUE Wilder ATR on DAILY bars, shifted one day, mapped to the 15m grid.
    The ATR used at any 15m bar of day D is computed only from data <= D-1."""
    out = np.full((panel.T, panel.N), np.nan, dtype=np.float64)
    for j in range(panel.N):
        s = pd.DataFrame({"high": panel.high[:, j], "low": panel.low[:, j],
                          "close": panel.close[:, j]},
                         index=panel.index).dropna()
        if len(s) < BARS_PER_DAY * 3:
            continue
        d = s.resample("1D").agg(high=("high", "max"), low=("low", "min"),
                                 close=("close", "last")).dropna()
        if len(d) < 3:
            continue
        pc = d["close"].shift(1)
        tr = pd.concat([(d["high"] - d["low"]).abs(), (d["high"] - pc).abs(),
                        (d["low"] - pc).abs()], axis=1).max(axis=1)
        atr = (tr.ewm(alpha=1.0 / period, adjust=False,
                      min_periods=min(period, len(tr))).mean().shift(1))
        out[:, j] = atr.reindex(panel.index, method="ffill").to_numpy()
    floor = 0.012 * panel.close
    out = np.where(np.isfinite(out) & (out > 0), out, floor)
    return np.maximum(np.nan_to_num(out, nan=1e-12), 1e-12)


def causal_bar_atr(panel: Panel, period: int = 14) -> np.ndarray:
    """Wilder ATR_14 on the 15m grid, shifted one bar (used for stop padding)."""
    pc = np.vstack([np.full((1, panel.N), np.nan), panel.close[:-1]])
    tr = np.nanmax(np.dstack([np.abs(panel.high - panel.low),
                              np.abs(panel.high - pc),
                              np.abs(panel.low - pc)]), axis=2)
    atr = (pd.DataFrame(tr).ewm(alpha=1.0 / period, adjust=False,
                                min_periods=period).mean().shift(1).to_numpy())
    floor = 0.0008 * panel.close
    atr = np.where(np.isfinite(atr) & (atr > 0), atr, floor)
    return np.maximum(np.nan_to_num(atr, nan=1e-12), 1e-12)


def event_time_funding(panel: Panel, funding) -> Tuple[np.ndarray, np.ndarray]:
    """(rate charged AT the settlement bar, causal annualised rate ffilled).
    Funding must accrue ~3x/day in EVENT time, never on every 15m bar."""
    ev = np.zeros((panel.T, panel.N), dtype=np.float64)
    ann = np.zeros((panel.T, panel.N), dtype=np.float64)

    if not funding and "funding_rate" in panel.extras:
        fr = panel.extras["funding_rate"]
        for j in range(panel.N):
            s = pd.Series(fr[:, j], index=panel.index)
            settle = s.ne(s.shift(1)) & s.notna()
            ev[:, j] = np.where(settle.to_numpy(), np.nan_to_num(fr[:, j]), 0.0)
            ann[:, j] = np.nan_to_num(s.shift(1).ffill().to_numpy()) * 3.0 * 365.0
        return ev, ann
    if not funding:
        return ev, ann

    for j, sym in enumerate(panel.symbols):
        f = funding.get(sym)
        if f is None or len(f) == 0:
            continue
        f = f.copy()
        f.index = pd.DatetimeIndex(pd.to_datetime(f.index))
        f = f[~f.index.duplicated(keep="last")].sort_index()
        f = f[(f.index >= panel.index[0]) & (f.index <= panel.index[-1])]
        if len(f) == 0:
            continue
        pos = panel.index.searchsorted(f.index, side="left")
        ok = pos < panel.T
        np.add.at(ev, (pos[ok], np.full(int(ok.sum()), j)),
                  f.to_numpy(dtype=np.float64)[ok])
        a = (f * 3.0 * 365.0).shift(1)          # only PRIOR settlements
        ann[:, j] = a.reindex(panel.index, method="ffill").fillna(0.0).to_numpy()
    return ev, np.nan_to_num(ann)


def oi_cube(panel: Panel, oi) -> Optional[np.ndarray]:
    if oi:
        m = np.full((panel.T, panel.N), np.nan)
        for j, s in enumerate(panel.symbols):
            o = oi.get(s)
            if o is None or len(o) == 0:
                continue
            o = o.copy()
            o.index = pd.DatetimeIndex(pd.to_datetime(o.index))
            o = o[~o.index.duplicated(keep="last")].sort_index()
            m[:, j] = (o.reindex(panel.index.union(o.index)).ffill()
                        .reindex(panel.index).to_numpy(dtype=np.float64))
        return m
    for k in ("open_interest", "oi"):
        if k in panel.extras:
            return panel.extras[k]
    return None


# ===========================================================================
# 3. FEATURE ENGINEERING  (Directive 3.C -- stationary + microstructure only)
# ===========================================================================
FEATURE_NAMES: Tuple[str, ...] = (
    "long_liq_z", "short_liq_z", "liq_imbalance",
    "oi_d1h", "oi_d4h", "oi_d12h", "oi_z",
    "fund_ann", "fund_spread", "fund_velocity",
    "lead_z", "lag_ratio", "beta_resid_z",
    "reclaim_ratio", "body_ratio", "upper_wick", "lower_wick",
    "vol_z", "rv_ratio", "atr_pct", "ret_1h_z", "ret_4h_z",
    "xs_ret_pct", "dist_vwap_z", "rsi_norm", "hour_sin", "hour_cos",
    # ---- Round 10: orderflow / footprint / trend structure ----
    "cvd_z", "cvd_slope_z", "zc_div", "taker_ratio_z", "taker_imb",
    "fp_stacked", "fp_poc_z", "fp_absorb_z", "fp_conf",
    "don_pos_fast", "don_pos_slow", "ema_ribbon", "ema_slope_z",
    "trend_persist", "whale_z", "smart_skew",
)


class FeatureFactory:
    """All features are stationary (z-scores, ratios, percentage deltas) and
    strictly causal: every rolling statistic at bar t uses only bars <= t."""

    def __init__(self, cfg: R10Config):
        self.cfg = cfg

    def build(self, p: Panel, funding=None, oi=None) -> Dict[str, np.ndarray]:
        cfg = self.cfg
        C, H, L, O, V = p.close, p.high, p.low, p.open, p.volume
        F: Dict[str, np.ndarray] = {}

        datr = causal_daily_atr(p, 14)
        batr = causal_bar_atr(p, cfg.atr_bars)
        F["_daily_atr"], F["_bar_atr"] = datr, batr

        prev_c = np.vstack([np.full((1, p.N), np.nan), C[:-1]])
        ret = np.nan_to_num(np.log(np.where(C > 0, C, np.nan) /
                                   np.where(prev_c > 0, prev_c, np.nan)))
        F["_ret"] = ret

        # ---------- candle geometry (normalised, Directive 3.C) ----------
        rng = np.maximum(H - L, 1e-9)
        F["reclaim_ratio"] = np.nan_to_num((C - L) / rng, nan=0.5)
        F["body_ratio"] = np.nan_to_num((C - O) / rng, nan=0.0)
        F["upper_wick"] = np.nan_to_num((H - np.maximum(O, C)) / rng, nan=0.0)
        F["lower_wick"] = np.nan_to_num((np.minimum(O, C) - L) / rng, nan=0.0)

        # ---------- volume / volatility ----------
        F["vol_z"] = _z(np.nan_to_num(V), BARS_PER_DAY * 3)
        rv_s = _roll(np.abs(ret), BARS_PER_HOUR * 4, "mean")
        rv_l = _roll(np.abs(ret), BARS_PER_DAY * 3, "mean")
        F["rv_ratio"] = np.clip(np.nan_to_num(rv_s / np.where(rv_l > 1e-12,
                                                              rv_l, np.nan),
                                              nan=1.0), 0.0, 8.0)
        F["atr_pct"] = np.clip(np.nan_to_num(datr / np.where(C > 0, C, np.nan),
                                             nan=0.02), 0.0, 0.5)
        F["ret_1h_z"] = _z(_roll(ret, BARS_PER_HOUR, "sum"), BARS_PER_DAY * 5)
        F["ret_4h_z"] = _z(_roll(ret, BARS_PER_HOUR * 4, "sum"),
                           BARS_PER_DAY * 5)
        F["xs_ret_pct"] = _xs_pctile(_roll(ret, BARS_PER_HOUR, "sum"))

        # ---------- liquidation impulse ----------
        F["long_liq_z"], F["short_liq_z"] = self._liq(p, ret, F["vol_z"])
        F["liq_imbalance"] = np.clip(F["long_liq_z"] - F["short_liq_z"], -12, 12)

        # ---------- open interest, multi-horizon (Directive 3.C) ----------
        OI = oi_cube(p, oi)
        if OI is not None and np.any(np.isfinite(OI)):
            OI = pd.DataFrame(OI).ffill().to_numpy()
            for name, k in (("oi_d1h", BARS_PER_HOUR),
                            ("oi_d4h", BARS_PER_HOUR * 4),
                            ("oi_d12h", BARS_PER_HOUR * 12)):
                prev = np.vstack([np.full((k, p.N), np.nan), OI[:-k]])
                F[name] = np.clip(np.nan_to_num(OI / np.where(prev > 0, prev,
                                                              np.nan) - 1.0,
                                                nan=0.0), -0.9, 3.0)
            F["oi_z"] = _z(F["oi_d1h"], BARS_PER_DAY * 3)
            F["_has_oi"] = np.ones(1)
        else:
            # Proxy: OI collapse is mechanically accompanied by a volume spike
            # into a range expansion. Weaker than real OI -- flagged so the
            # scorecard can report it.
            for name in ("oi_d1h", "oi_d4h", "oi_d12h"):
                F[name] = np.zeros_like(C)
            F["oi_z"] = np.zeros_like(C)
            F["_has_oi"] = np.zeros(1)

        # ---------- funding: level, spread, velocity (Directive 3.C) ----------
        ev, ann = event_time_funding(p, funding)
        F["_fund_event"] = ev
        F["fund_ann"] = np.clip(ann, -6.0, 6.0)
        base = _roll(ann, BARS_PER_HOUR * 24, "mean")
        F["fund_spread"] = np.clip(np.nan_to_num(ann - base), -6.0, 6.0)
        prev8 = np.vstack([np.full((BARS_PER_HOUR * 8, p.N), np.nan),
                           ann[:-BARS_PER_HOUR * 8]])
        F["fund_velocity"] = np.clip(np.nan_to_num(ann - prev8), -6.0, 6.0)

        # ---------- cross-asset lead-lag (Directive 3.C) ----------
        F["lead_z"], F["lag_ratio"], F["beta_resid_z"] = self._leadlag(p, ret)

        # ---------- session seasonality (bounded, stationary) ----------
        hod = p.index.hour.to_numpy(dtype=np.float64)[:, None] * np.ones((1, p.N))
        F["hour_sin"] = np.sin(2 * np.pi * hod / 24.0)
        F["hour_cos"] = np.cos(2 * np.pi * hod / 24.0)

        # ---------- vwap / rsi passthroughs ----------
        for src, dst, dflt in (("dist_to_vwap_zs", "dist_vwap_z", 0.0),
                               ("vwap_zscore", "dist_vwap_z", 0.0)):
            if dst not in F and src in p.extras:
                F[dst] = np.clip(np.nan_to_num(p.extras[src]), -8, 8)
        if "dist_vwap_z" not in F:
            vw = _roll(C * np.nan_to_num(V, nan=1.0), BARS_PER_DAY, "sum") / \
                 np.maximum(_roll(np.nan_to_num(V, nan=1.0), BARS_PER_DAY,
                                  "sum"), 1e-9)
            F["dist_vwap_z"] = _z(np.nan_to_num(C - vw), BARS_PER_DAY * 3)
        if "rsi_14" in p.extras:
            F["rsi_norm"] = np.nan_to_num(p.extras["rsi_14"] / 100.0 - 0.5,
                                          nan=0.0)
        else:
            up = np.where(ret > 0, ret, 0.0)
            dn = np.where(ret < 0, -ret, 0.0)
            au = _roll(up, 14, "mean")
            ad = _roll(dn, 14, "mean")
            rs = np.nan_to_num(au / np.where(ad > 1e-12, ad, np.nan), nan=1.0)
            F["rsi_norm"] = (1.0 - 1.0 / (1.0 + rs)) - 0.5

        # ---------- Round 10: orderflow, footprint, trend structure ------
        self._orderflow(p, F, ret)
        self._footprint(p, F)
        self._trend(p, F, ret)

        for k in FEATURE_NAMES:
            F[k] = np.nan_to_num(F[k], nan=0.0, posinf=0.0, neginf=0.0)
        return F

    # -------------------------------------------------------------------
    # Round 10 -- A. DELTA / CVD DYNAMICS
    # -------------------------------------------------------------------
    def _orderflow(self, p: Panel, F, ret):
        """Cumulative volume delta, taker aggression and spot-vs-futures
        divergence. Every real column is optional; each has a causal proxy
        and every substitution is counted in `_of_cover` so the scorecard can
        say how much of the orderflow thesis was actually exercised."""
        cfg = self.cfg
        C, V = p.close, p.volume
        T, N = p.T, p.N
        have, want = 0, 0

        def get(col):
            nonlocal have, want
            want += 1
            v = p.extras.get(col)
            if v is None or not np.any(np.isfinite(v)):
                return None
            have += 1
            return np.nan_to_num(v)

        # ---- futures CVD ------------------------------------------------
        fut = get("future_cvd_15m")
        if fut is None:
            fut = get("cvd")
        if fut is None:
            # Proxy: signed volume. Its LEVEL is non-stationary, so it is only
            # ever used through a z-score / slope below, never raw.
            tb = p.extras.get("taker_buy_volume")
            if tb is not None and np.any(np.isfinite(tb)):
                delta = 2.0 * np.nan_to_num(tb) - np.nan_to_num(V)
            else:
                delta = np.sign(ret) * np.nan_to_num(V)
            fut = np.nancumsum(delta, axis=0)

        # CVD must be differenced before z-scoring: the cumulative level has
        # a unit root and would leak a trend proxy rather than orderflow.
        d_cvd = np.vstack([np.zeros((1, N)), np.diff(fut, axis=0)])
        scale = np.maximum(_roll(np.abs(d_cvd), BARS_PER_DAY * 3, "mean"), 1e-12)
        F["cvd_z"] = np.clip(_z(d_cvd / scale, BARS_PER_DAY * 3), -8, 8)
        F["cvd_slope_z"] = np.clip(
            _z(_roll(d_cvd / scale, BARS_PER_HOUR * 4, "sum"),
               BARS_PER_DAY * 3), -8, 8)
        F["_cvd_raw"] = d_cvd

        # ---- spot vs futures divergence (institutional distribution) -----
        zc = get("zc_div")
        if zc is None:
            spot = get("spot_cvd_15m")
            if spot is not None:
                d_spot = np.vstack([np.zeros((1, N)), np.diff(spot, axis=0)])
                ss = np.maximum(_roll(np.abs(d_spot), BARS_PER_DAY * 3, "mean"),
                                1e-12)
                zc = (_z(d_spot / ss, BARS_PER_DAY * 3)
                      - _z(d_cvd / scale, BARS_PER_DAY * 3))
            else:
                # Proxy: price advancing while delta contracts.
                zc = _z(np.sign(ret) * np.abs(F["cvd_z"]) - F["cvd_z"],
                        BARS_PER_DAY * 3)
        F["zc_div"] = np.clip(np.nan_to_num(zc), -8, 8)

        # ---- taker aggression -------------------------------------------
        tr = get("taker_volume_ratio")
        if tr is None:
            tbv, tsv = get("taker_buy_vol_btc"), get("taker_sell_vol_btc")
            if tbv is not None and tsv is not None:
                tr = tbv / np.maximum(tsv, 1e-12)
            else:
                tb = p.extras.get("taker_buy_volume")
                if tb is not None and np.any(np.isfinite(tb)):
                    tb = np.nan_to_num(tb)
                    tr = tb / np.maximum(np.nan_to_num(V) - tb, 1e-12)
                else:
                    # Proxy: close position within the bar as a stand-in for
                    # who won the auction. Weak, and flagged as such.
                    tr = np.exp(2.0 * (F["reclaim_ratio"] - 0.5))
        tr = np.clip(np.nan_to_num(tr, nan=1.0), 0.02, 50.0)
        F["_taker_ratio"] = tr
        F["taker_ratio_z"] = np.clip(_z(np.log(tr), BARS_PER_DAY * 3), -8, 8)
        F["taker_imb"] = np.clip((tr - 1.0) / (tr + 1.0), -1.0, 1.0)

        # ---- institutional positioning ----------------------------------
        wi = get("whale_index")
        F["whale_z"] = (np.clip(_z(wi, BARS_PER_DAY * 3), -8, 8)
                        if wi is not None else np.zeros((T, N)))
        top = get("top_account_ratio")
        if top is None:
            top = get("ls_ratio_top")
        F["smart_skew"] = (np.clip(_z(np.log(np.clip(top, 0.02, 50.0)),
                                      BARS_PER_DAY * 3), -8, 8)
                           if top is not None else np.zeros((T, N)))
        F["_of_cover"] = np.array([have / max(want, 1)])

    # -------------------------------------------------------------------
    # Round 10 -- B. FOOTPRINT LADDER MICROSTRUCTURE
    # -------------------------------------------------------------------
    def _footprint(self, p: Panel, F):
        """Stacked imbalances, POC migration and wick absorption. Mirrors
        Engine/ml/footprint_confirmation.py, vectorised over the panel."""
        T, N = p.T, p.N
        C, O, H, L = p.close, p.open, p.high, p.low

        def col(name, dflt=None):
            v = p.extras.get(name)
            if v is None or not np.any(np.isfinite(v)):
                return dflt
            return np.nan_to_num(v)

        sb = col("is_stacked_buy_imb")
        ss = col("is_stacked_sell_imb")
        if sb is None or ss is None:
            # Proxy for a 3+ level stacked imbalance: a strongly one-sided
            # bar (body dominates range) on above-average aggression.
            strong = (F["body_ratio"] >= 0.55) & (F["taker_imb"] >= 0.10)
            weak = (F["body_ratio"] <= -0.55) & (F["taker_imb"] <= -0.10)
            sb = strong.astype(np.float64) if sb is None else sb
            ss = weak.astype(np.float64) if ss is None else ss
        sb = sb > 0.5
        ss = ss > 0.5
        # backward-looking OR over the last 2 bars (matches the repo module)
        sb2 = sb | np.vstack([np.zeros((1, N), bool), sb[:-1]])
        ss2 = ss | np.vstack([np.zeros((1, N), bool), ss[:-1]])
        F["_sb2"], F["_ss2"] = sb2, ss2
        F["fp_stacked"] = sb2.astype(np.float64) - ss2.astype(np.float64)

        poc = col("poc_shift")
        if poc is None:
            # Proxy: migration of the volume-weighted mid over 8 bars.
            mid = (H + L + 2.0 * C) / 4.0
            poc = mid - _roll(mid, 8, "mean")
        F["fp_poc_z"] = np.clip(_z(poc, BARS_PER_DAY), -8, 8)

        ab = col("absorption_ratio")
        if ab is None:
            # Proxy: aggressive volume into a wick that made no progress.
            ab = (F["lower_wick"] - F["upper_wick"]) * np.maximum(F["vol_z"], 0)
        F["fp_absorb_z"] = np.clip(_z(ab, BARS_PER_DAY), -8, 8)
        F["_absorb"] = ab

        wsa = col("wick_sell_absorb")
        wbe = col("wick_buy_exhaust", col("wick_buy_absorb"))
        F["_wsa_z"] = (np.clip(_z(wsa, BARS_PER_DAY), -8, 8)
                       if wsa is not None
                       else np.clip(_z(F["lower_wick"] * np.maximum(F["vol_z"], 0),
                                       BARS_PER_DAY), -8, 8))
        F["_wbe_z"] = (np.clip(_z(wbe, BARS_PER_DAY), -8, 8)
                       if wbe is not None
                       else np.clip(_z(F["upper_wick"] * np.maximum(F["vol_z"], 0),
                                       BARS_PER_DAY), -8, 8))
        cp = col("close_pos")
        F["_close_pos"] = cp if cp is not None else (2.0 * F["reclaim_ratio"] - 1.0)
        F["fp_conf"] = np.zeros((T, N))     # filled per-side by the sampler

    # -------------------------------------------------------------------
    # Round 10 -- C. TREND STRUCTURE (Donchian + EMA ribbon)
    # -------------------------------------------------------------------
    def _trend(self, p: Panel, F, ret):
        """All trend structure is computed on bars <= t and then SHIFTED one
        bar, so a breakout is only visible on the bar AFTER it completed."""
        cfg = self.cfg
        C, H, L = p.close, p.high, p.low
        T, N = p.T, p.N

        def ema(a, span):
            return (pd.DataFrame(a).ewm(span=span, adjust=False,
                                        min_periods=max(2, span // 4))
                    .mean().to_numpy())

        e_f, e_m, e_s = (ema(C, cfg.ema_fast), ema(C, cfg.ema_mid),
                         ema(C, cfg.ema_slow))
        F["_ema_f"], F["_ema_m"], F["_ema_s"] = e_f, e_m, e_s
        up = (e_f > e_m) & (e_m > e_s)
        dn = (e_f < e_m) & (e_m < e_s)
        F["ema_ribbon"] = up.astype(np.float64) - dn.astype(np.float64)
        sl = np.nan_to_num((e_f - np.vstack([np.full((BARS_PER_HOUR * 6, N),
                                                     np.nan),
                                             e_f[:-BARS_PER_HOUR * 6]]))
                           / np.where(C > 0, C, np.nan))
        F["ema_slope_z"] = np.clip(_z(sl, BARS_PER_DAY * 3), -8, 8)

        # Donchian channels EXCLUDING the current bar (shift by 1) so that a
        # "break of the prior 20-bar high" cannot be satisfied by the very
        # bar being tested -- that would be look-ahead within the bar.
        def don(w):
            hi = _roll(H, w, "max")
            lo = _roll(L, w, "min")
            hi = np.vstack([np.full((1, N), np.nan), hi[:-1]])
            lo = np.vstack([np.full((1, N), np.nan), lo[:-1]])
            rng = np.maximum(hi - lo, 1e-12)
            pos = np.clip(np.nan_to_num((C - lo) / rng, nan=0.5), -0.5, 1.5)
            return hi, lo, pos

        hi_f, lo_f, pos_f = don(cfg.donchian_fast)
        hi_s, lo_s, pos_s = don(cfg.donchian_slow)
        F["_don_hi_f"], F["_don_lo_f"] = hi_f, lo_f
        F["_don_hi_s"], F["_don_lo_s"] = hi_s, lo_s
        F["don_pos_fast"], F["don_pos_slow"] = pos_f, pos_s

        # trend persistence: fraction of the last 24 bars closing in the
        # ribbon's direction -- a cheap, stationary ADX substitute.
        sgn = np.sign(np.nan_to_num(ret))
        F["trend_persist"] = np.clip(_roll(sgn, BARS_PER_HOUR * 6, "mean"),
                                     -1.0, 1.0)

    # -------------------------------------------------------------------
    def _liq(self, p: Panel, ret, vol_z):
        """Real liquidation z-scores when present; otherwise a signed
        range-expansion x volume-surge proxy."""
        if "long_liq_zs" in p.extras and "short_liq_zs" in p.extras:
            lo = np.clip(np.nan_to_num(p.extras["long_liq_zs"]), 0.0, 12.0)
            sh = np.clip(np.nan_to_num(p.extras["short_liq_zs"]), 0.0, 12.0)
            return lo, sh
        rng = np.maximum(p.high - p.low, 1e-12) / np.maximum(p.close, 1e-12)
        rng_z = _z(rng, BARS_PER_DAY * 3)
        imp = np.maximum(rng_z, 0.0) * np.maximum(vol_z, 0.0)
        iz = np.clip(_z(imp, BARS_PER_DAY * 3), 0.0, 12.0)
        dn = p.close < p.open
        return np.where(dn, iz, 0.0), np.where(~dn, iz, 0.0)

    def _leadlag(self, p: Panel, ret):
        """BTC/ETH impulse spillover into delayed high-beta alts."""
        k = BARS_PER_HOUR
        lead_syms = [s for s in ("BTCUSDT", "ETHUSDT", "BTC", "ETH")
                     if s in p.symbols]
        lead_cols = [p.symbols.index(s) for s in lead_syms]
        cum = _roll(ret, k, "sum")
        if lead_cols:
            lead = np.nan_to_num(cum[:, lead_cols]).mean(axis=1, keepdims=True)
        else:                              # no majors: use the equal-weight index
            lead = np.nan_to_num(cum).mean(axis=1, keepdims=True)
        lead_z = np.clip(_z(np.repeat(lead, p.N, axis=1), BARS_PER_DAY * 5),
                         -8, 8)
        denom = np.where(np.abs(lead) > 1e-9, np.abs(lead), np.nan)
        lag_ratio = np.clip(np.nan_to_num(cum / denom, nan=1.0), -5.0, 5.0)

        # beta-residual dislocation vs the equal-weight universe (Round 7)
        idx = np.repeat(np.nan_to_num(ret).mean(axis=1, keepdims=True), p.N, 1)
        w = BARS_PER_DAY * 5
        cov = _roll(ret * idx, w, "mean") - _roll(ret, w, "mean") * _roll(idx, w, "mean")
        var = _roll(idx * idx, w, "mean") - _roll(idx, w, "mean") ** 2
        beta = np.clip(np.nan_to_num(cov / np.where(var > 1e-14, var, np.nan),
                                     nan=1.0), -3.0, 3.0)
        resid = _roll(ret - beta * idx, BARS_PER_HOUR * 6, "sum")
        return lead_z, lag_ratio, _z(np.nan_to_num(resid), BARS_PER_DAY * 5)


# ===========================================================================
# 3b. FOOTPRINT CONFIRMATION GATE
#     Port of Engine/ml/footprint_confirmation.py, vectorised over the panel.
# ===========================================================================
class FootprintConfirmation:
    """Binary confirmation gate scored 0..6 on ladder microstructure.

    Faithful to the repo module's scoring, with one deliberate change: the
    repo evaluates a single `side` column, whereas the sampler needs to know
    the score for a HYPOTHESISED side before it has committed to one. So the
    score is computed for a supplied side mask instead of a side column.

    Components (1 point each, capped at 6):
      1. wick absorption in the trade's favour        (wick_sell_absorb z)
      2. absorption ratio agreeing with the side      (absorption_ratio z)
      3. POC migrating in the trade's direction       (poc_shift z)
      4. close position inside the bar agreeing       (close_pos)
      5. stacked imbalance in the last 2 bars         (is_stacked_*_imb)
      6. taker aggression agreeing with the side      (taker_volume_ratio)
    """

    def __init__(self, cfg):
        self.cfg = cfg

    def score(self, F, side: int) -> np.ndarray:
        """`side` is +1 or -1; returns an integer score array (T, N)."""
        wsa, wbe = F["_wsa_z"], F["_wbe_z"]
        absr, absz = F["_absorb"], F["fp_absorb_z"]
        poc, cp = F["fp_poc_z"], F["_close_pos"]
        sb2, ss2 = F["_sb2"], F["_ss2"]
        imb = F["taker_imb"]

        sc = np.zeros(wsa.shape, dtype=np.int16)
        if side == 1:
            sc += (wsa >= 1.0)
            sc += ((absz >= 0.5) & (absr > 0))
            sc += (poc >= 0.3)
            sc += (cp >= 0.3)
            sc += sb2
            sc += (imb >= 0.10)
        else:
            sc += (wbe >= 1.0)
            sc += ((absz <= -0.5) & (absr < 0))
            sc += (poc <= -0.3)
            sc += (cp <= -0.3)
            sc += ss2
            sc += (imb <= -0.10)
        return np.minimum(sc, 6)

    def confirmed(self, F, side: int) -> np.ndarray:
        return self.score(F, side) >= self.cfg.fp_min_score


# ===========================================================================
# 4. EVENT SAMPLER  (Directive 3.A -- LOOSE + DISJUNCTIVE, not a trade signal)
# ===========================================================================
class EventSampler:
    """Round 8's fatal bug was a CONJUNCTIVE static gate whose joint hit rate
    went to zero off-regime. Here the sampler is DISJUNCTIVE and loose: it only
    decides *where to look*. The classifier decides *whether to trade*."""

    def __init__(self, cfg: R10Config):
        self.cfg = cfg
        self.fp = FootprintConfirmation(cfg)

    def detect(self, p: Panel, F) -> Tuple[np.ndarray, np.ndarray,
                                           np.ndarray, np.ndarray]:
        cfg = self.cfg
        T, N = p.T, p.N
        side = np.zeros((T, N), dtype=np.int8)
        stop = np.full((T, N), np.nan)
        setup = np.zeros((T, N), dtype=np.int8)

        batr = F["_bar_atr"]
        lo_ext = _roll(p.low, cfg.flush_lookback, "min")
        hi_ext = _roll(p.high, cfg.flush_lookback, "max")
        # stop at the flush extreme -/+ 0.20 * ATR_14  (Directive 3.D)
        stop_long = lo_ext - cfg.stop_atr_mult * batr
        stop_short = hi_ext + cfg.stop_atr_mult * batr

        llz, slz = F["long_liq_z"], F["short_liq_z"]
        fann = F["fund_ann"]
        lead, lag = F["lead_z"], F["lag_ratio"]
        volz, recl = F["vol_z"], F["reclaim_ratio"]

        base_ok = p.valid & np.isfinite(batr) & (batr > 0)

        def assign(mask, s_side, s_setup, s_stop):
            free = mask & (setup == 0) & base_ok
            side[free] = s_side
            setup[free] = s_setup
            stop[free] = s_stop[free]

        # ===================================================================
        # ROUND 10 -- TREND IGNITION, evaluated FIRST (highest priority).
        # A breakout is only a trade when aggressive volume is lifting the
        # book. Without that confirmation it is a liquidity vacuum, and it
        # is exactly those that produce the chop-trap losses.
        # ===================================================================
        cvdz, cvds = F["cvd_z"], F["cvd_slope_z"]
        zc, timb = F["zc_div"], F["taker_imb"]
        ribbon, persist = F["ema_ribbon"], F["trend_persist"]
        sb2, ss2 = F["_sb2"], F["_ss2"]
        tratio = F["_taker_ratio"]

        # -- structural break of the prior-N-bar channel (channels already
        #    exclude the current bar, so this is not an intrabar peek) ----
        brk_up = (p.high >= F["_don_hi_f"]) | (p.close > F["_don_hi_f"])
        brk_dn = (p.low <= F["_don_lo_f"]) | (p.close < F["_don_lo_f"])
        brk_up_s = (p.high >= F["_don_hi_s"]) | (p.close > F["_don_hi_s"])
        brk_dn_s = (p.low <= F["_don_lo_s"]) | (p.close < F["_don_lo_s"])

        # -- directive 3.1: orderflow ignition ---------------------------
        ign_long = sb2 | ((tratio >= cfg.of_taker_ratio) & (F["_cvd_raw"] > 0))
        ign_short = ss2 | ((tratio <= 1.0 / cfg.of_taker_ratio)
                           & (F["_cvd_raw"] < 0))

        # -- directive 3.2: CVD acceleration + distribution veto ---------
        cvd_ok_long = (cvdz >= cfg.of_cvd_z_min) | (cvds >= cfg.of_cvd_z_min)
        cvd_ok_short = (cvdz <= -cfg.of_cvd_z_min) | (cvds <= -cfg.of_cvd_z_min)
        veto_long = zc <= -cfg.of_zc_div_veto      # spot distributing into highs
        veto_short = zc >= cfg.of_zc_div_veto      # spot accumulating into lows

        # -- footprint ladder confirmation (repo module) -----------------
        if cfg.fp_required_for_trend:
            fp_long = self.fp.confirmed(F, +1)
            fp_short = self.fp.confirmed(F, -1)
        else:
            fp_long = np.ones_like(brk_up, dtype=bool)
            fp_short = np.ones_like(brk_up, dtype=bool)

        ribbon_up = (ribbon > 0) | (brk_up_s & (persist >= cfg.trend_min_adx_z))
        ribbon_dn = (ribbon < 0) | (brk_dn_s & (persist <= -cfg.trend_min_adx_z))

        trend_long = (brk_up & ribbon_up & ign_long & cvd_ok_long
                      & ~veto_long & fp_long)
        trend_short = (brk_dn & ribbon_dn & ign_short & cvd_ok_short
                       & ~veto_short & fp_short)

        # ATR-based trend stop: a wick stop is far too tight for a wave, and
        # a breakout that immediately loses 1.6 ATR has failed by definition.
        t_stop_long = p.close - cfg.trend_stop_atr * batr
        t_stop_short = p.close + cfg.trend_stop_atr * batr
        # never inside the structure that was broken
        t_stop_long = np.minimum(t_stop_long, F["_don_lo_f"])
        t_stop_short = np.maximum(t_stop_short, F["_don_hi_f"])
        t_stop_long = np.where(np.isfinite(t_stop_long), t_stop_long,
                               p.close - cfg.trend_stop_atr * batr)
        t_stop_short = np.where(np.isfinite(t_stop_short), t_stop_short,
                                p.close + cfg.trend_stop_atr * batr)

        # -- directive 3.3: liquidation-squeeze rocket fuel ---------------
        # A long breakout while shorts are being force-liquidated is being
        # fed by forced buy-ins. Tagged separately for a 6R-8R target.
        sqz_long = trend_long & (slz >= cfg.sqz_liq_z)
        sqz_short = trend_short & (llz >= cfg.sqz_liq_z)
        assign(sqz_long, +1, SETUP_TREND_SQZ, t_stop_long)
        assign(sqz_short, -1, SETUP_TREND_SQZ, t_stop_short)
        assign(trend_long, +1, SETUP_TREND, t_stop_long)
        assign(trend_short, -1, SETUP_TREND, t_stop_short)

        # -- 1. forced-liquidation exhaust (highest information content) ----
        long_flush = (llz >= cfg.ev_liq_z) & (recl >= 0.40)
        short_flush = (slz >= cfg.ev_liq_z) & (recl <= 0.60)
        assign(long_flush, +1, SETUP_LIQ, stop_long)      # fade the long flush
        assign(short_flush, -1, SETUP_LIQ, stop_short)    # fade the short squeeze

        # -- 2. funding basis squeeze --------------------------------------
        assign(fann >= cfg.ev_funding_ann, -1, SETUP_FUND, stop_short)
        assign(fann <= -cfg.ev_funding_ann, +1, SETUP_FUND, stop_long)

        # -- 3. cross-asset lead-lag spillover (follow the lead) -----------
        laggy = np.abs(lag) <= 0.55
        assign((lead >= cfg.ev_lead_z) & laggy, +1, SETUP_LEADLAG, stop_long)
        assign((lead <= -cfg.ev_lead_z) & laggy, -1, SETUP_LEADLAG, stop_short)

        # -- 4. raw volume shock (fade in the direction of the reclaim) ----
        assign((volz >= cfg.ev_volume_z) & (recl >= 0.65), +1, SETUP_VOL,
               stop_long)
        assign((volz >= cfg.ev_volume_z) & (recl <= 0.35), -1, SETUP_VOL,
               stop_short)

        # ---- geometry sanity: 1R bounded relative to the daily range -----
        datr = F["_daily_atr"]
        entry_ref = p.close
        raw_r = np.abs(entry_ref - stop)
        r_lo = cfg.r_floor_frac_datr * datr
        r_hi = cfg.r_cap_frac_datr * datr
        R = np.clip(np.where(np.isfinite(raw_r), raw_r, np.nan), r_lo, r_hi)
        stop = np.where(setup != 0, entry_ref - side * R, np.nan)

        # record the footprint confirmation score for the chosen side so the
        # classifier can use it as a feature (not just as a gate)
        conf = np.zeros_like(stop)
        sc_l, sc_s = self.fp.score(F, +1), self.fp.score(F, -1)
        conf = np.where(side == 1, sc_l, np.where(side == -1, sc_s, 0))
        F["fp_conf"] = conf.astype(np.float64) / 6.0

        bad = ~np.isfinite(stop) | ~np.isfinite(R) | (R <= 0)
        side[bad], setup[bad] = 0, 0
        # warmup
        side[:cfg.warmup_bars], setup[:cfg.warmup_bars] = 0, 0
        return side, stop, setup, np.nan_to_num(R)


# ===========================================================================
# 5. TRIPLE-BARRIER LABELLING  (Directive 3.A)
# ===========================================================================
def triple_barrier(p: Panel, rows, cols, sides, entries, R,
                   cfg: R10Config) -> Tuple[np.ndarray, np.ndarray]:
    """Label each candidate event by whether price reaches +barrier_up_r
    BEFORE -barrier_dn_r, within barrier_bars.

    Returns (y, r_real):
      y      : 1 if the +4R barrier is hit first, else 0
      r_real : the realised R of the barrier outcome (+4, -1, or the
               time-barrier mark-out), used for expected-value threshold
               selection rather than raw accuracy.

    Entry is at the NEXT bar's open (never the signal bar's close), matching
    live execution exactly.
    """
    n = len(rows)
    y = np.zeros(n, dtype=np.int8)
    r_real = np.zeros(n, dtype=np.float64)
    H, L, C = p.high, p.low, p.close
    T = p.T
    hz = cfg.barrier_bars

    for i in range(n):
        t0, j, s = int(rows[i]) + 1, int(cols[i]), int(sides[i])
        e, r = entries[i], R[i]
        if r <= 0 or not np.isfinite(e) or t0 >= T:
            r_real[i] = 0.0
            continue
        up = e + s * cfg.barrier_up_r * r
        dn = e - s * cfg.barrier_dn_r * r
        t1 = min(t0 + hz, T - 1)
        hh, ll = H[t0:t1 + 1, j], L[t0:t1 + 1, j]
        if s > 0:
            hit_up = np.flatnonzero(hh >= up)
            hit_dn = np.flatnonzero(ll <= dn)
        else:
            hit_up = np.flatnonzero(ll <= up)
            hit_dn = np.flatnonzero(hh >= dn)
        iu = hit_up[0] if hit_up.size else 10 ** 9
        idn = hit_dn[0] if hit_dn.size else 10 ** 9
        if iu < idn:
            y[i], r_real[i] = 1, cfg.barrier_up_r
        elif idn < iu:
            y[i], r_real[i] = 0, -cfg.barrier_dn_r
        else:
            # both in the same bar (or neither): resolve conservatively as a
            # loss when ambiguous, otherwise mark out at the vertical barrier.
            if iu < 10 ** 9:
                y[i], r_real[i] = 0, -cfg.barrier_dn_r
            else:
                px = C[t1, j]
                r_real[i] = (0.0 if not np.isfinite(px)
                             else float(s * (px - e) / r))
                y[i] = 0
    return y, r_real


# ===========================================================================
# 6. MACHINE LEARNING  (Directive 3.B)
# ===========================================================================
class _HistGBDT:
    """Deterministic, dependency-free histogram gradient-boosted trees on the
    logistic loss.

    Regularisation exactly as directed:
        max_depth <= 4, min_samples_leaf >= 20,
        reg_lambda >= 3.0 (leaf shrinkage), reg_alpha >= 1.0 (min split gain).
    """

    def __init__(self, cfg: R10Config):
        self.c = cfg
        self.edges: Optional[np.ndarray] = None
        self.trees: List[List[Tuple]] = []
        self.base = 0.0

    # ---- binning is fit on TRAIN ONLY (no test statistics leak in) ----
    def _fit_bins(self, X):
        nb = self.c.gbdt_bins
        qs = np.linspace(0.0, 1.0, nb + 1)[1:-1]
        self.edges = np.quantile(X, qs, axis=0).T          # (n_feat, nb-1)

    def _bin(self, X):
        out = np.empty(X.shape, dtype=np.int16)
        for f in range(X.shape[1]):
            out[:, f] = np.searchsorted(self.edges[f], X[:, f], side="left")
        return out

    def fit(self, X, y):
        c = self.c
        n, m = X.shape
        self._fit_bins(X)
        B = self._bin(X)
        p0 = float(np.clip(y.mean(), 1e-4, 1 - 1e-4))
        self.base = math.log(p0 / (1 - p0))
        F = np.full(n, self.base)
        nb = c.gbdt_bins

        for _ in range(c.gbdt_rounds):
            prob = 1.0 / (1.0 + np.exp(-np.clip(F, -35, 35)))
            g = prob - y                                    # gradient
            h = np.maximum(prob * (1.0 - prob), 1e-6)       # hessian
            node = np.zeros(n, dtype=np.int32)
            tree: List[Tuple] = []
            n_nodes = 1
            splits: Dict[int, Tuple[int, int]] = {}

            for _d in range(c.gbdt_max_depth):
                Gs = np.bincount(node, weights=g, minlength=n_nodes)
                Hs = np.bincount(node, weights=h, minlength=n_nodes)
                Ns = np.bincount(node, minlength=n_nodes)
                parent = Gs ** 2 / (Hs + c.gbdt_reg_lambda)
                best = {}
                for f in range(m):
                    code = node.astype(np.int64) * nb + B[:, f]
                    gg = np.bincount(code, weights=g, minlength=n_nodes * nb)
                    hh = np.bincount(code, weights=h, minlength=n_nodes * nb)
                    cc = np.bincount(code, minlength=n_nodes * nb)
                    gg = gg.reshape(n_nodes, nb).cumsum(1)
                    hh = hh.reshape(n_nodes, nb).cumsum(1)
                    cc = cc.reshape(n_nodes, nb).cumsum(1)
                    gL, hL, cL = gg[:, :-1], hh[:, :-1], cc[:, :-1]
                    gR = Gs[:, None] - gL
                    hR = Hs[:, None] - hL
                    cR = Ns[:, None] - cL
                    gain = (gL ** 2 / (hL + c.gbdt_reg_lambda)
                            + gR ** 2 / (hR + c.gbdt_reg_lambda)
                            - parent[:, None])
                    gain = np.where((cL >= c.gbdt_min_leaf)
                                    & (cR >= c.gbdt_min_leaf), gain, -np.inf)
                    bi = np.argmax(gain, axis=1)
                    bv = gain[np.arange(n_nodes), bi]
                    for nd in range(n_nodes):
                        if bv[nd] > best.get(nd, (-np.inf,))[0]:
                            best[nd] = (bv[nd], f, int(bi[nd]))

                new_node = node.copy()
                grew = False
                for nd, (gv, f, thr) in best.items():
                    if not np.isfinite(gv) or gv <= c.gbdt_min_split_gain:
                        continue
                    sel = node == nd
                    if not sel.any():
                        continue
                    right = sel & (B[:, f] > thr)
                    left_id, right_id = n_nodes, n_nodes + 1
                    new_node[sel] = left_id
                    new_node[right] = right_id
                    splits[nd] = (f, thr)
                    tree.append((nd, f, thr, left_id, right_id))
                    n_nodes += 2
                    grew = True
                if not grew:
                    break
                node = new_node

            Gs = np.bincount(node, weights=g, minlength=n_nodes)
            Hs = np.bincount(node, weights=h, minlength=n_nodes)
            leaf_val = -Gs / (Hs + c.gbdt_reg_lambda)
            F = F + c.gbdt_lr * leaf_val[node]
            self.trees.append([tree, leaf_val])
        return self

    def decision(self, X):
        B = self._bin(X)
        F = np.full(X.shape[0], self.base)
        for tree, leaf_val in self.trees:
            node = np.zeros(X.shape[0], dtype=np.int32)
            for nd, f, thr, li, ri in tree:
                sel = node == nd
                if not sel.any():
                    continue
                node[sel] = np.where(B[sel, f] > thr, ri, li)
            F = F + self.c.gbdt_lr * leaf_val[node]
        return F

    def predict_proba(self, X):
        return 1.0 / (1.0 + np.exp(-np.clip(self.decision(X), -35, 35)))


class _RidgeLogit:
    """L2-regularised logistic regression, full-batch gradient descent on
    standardised features. Deterministic, no RNG, no external solver."""

    def __init__(self, cfg: R10Config):
        self.c = cfg
        self.w = None
        self.b = 0.0
        self.mu = None
        self.sd = None

    def fit(self, X, y):
        self.mu = X.mean(0)
        self.sd = np.maximum(X.std(0), 1e-8)
        Z = (X - self.mu) / self.sd
        n, m = Z.shape
        self.w = np.zeros(m)
        self.b = math.log(max(y.mean(), 1e-4) / max(1 - y.mean(), 1e-4))
        for _ in range(self.c.ridge_iters):
            pr = 1.0 / (1.0 + np.exp(-np.clip(Z @ self.w + self.b, -35, 35)))
            err = pr - y
            gw = Z.T @ err / n + self.c.ridge_l2 * self.w / n
            gb = err.mean()
            self.w -= self.c.ridge_lr * gw
            self.b -= self.c.ridge_lr * gb
        return self

    def predict_proba(self, X):
        Z = (X - self.mu) / self.sd
        return 1.0 / (1.0 + np.exp(-np.clip(Z @ self.w + self.b, -35, 35)))


def _auc(y, p) -> float:
    y = np.asarray(y).astype(float)
    if y.min() == y.max():
        return 0.5
    r = pd.Series(p).rank().to_numpy()
    n1, n0 = y.sum(), (1 - y).sum()
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


class MLEnsemble:
    """GBDT + ridge logistic, blended, then probability-CALIBRATED on the
    validation fold with a monotone binned reliability map (isotonic-lite).
    A calibrated probability is required because the trade rule is a level
    test P(hit +4R) >= p*, not a ranking."""

    def __init__(self, cfg: R10Config):
        self.c = cfg
        self.gb: Optional[_HistGBDT] = None
        self.sk = None
        self.lr: Optional[_RidgeLogit] = None
        self.cal_x: Optional[np.ndarray] = None
        self.cal_y: Optional[np.ndarray] = None
        self.auc_val = 0.5

    def fit(self, Xtr, ytr, Xva, yva):
        self.gb = _HistGBDT(self.c).fit(Xtr, ytr)
        self.lr = _RidgeLogit(self.c).fit(Xtr, ytr)
        if _HAS_SK:
            try:
                self.sk = _SkHGB(max_depth=self.c.gbdt_max_depth,
                                 min_samples_leaf=self.c.gbdt_min_leaf,
                                 l2_regularization=self.c.gbdt_reg_lambda,
                                 learning_rate=self.c.gbdt_lr,
                                 max_iter=self.c.gbdt_rounds,
                                 early_stopping=False,
                                 random_state=0).fit(Xtr, ytr)
            except Exception:
                self.sk = None
        praw = self._raw(Xva)
        self.auc_val = _auc(yva, praw)
        self._calibrate(praw, yva)
        return self

    def _raw(self, X):
        w = self.c.ensemble_w_gbdt
        p = w * self.gb.predict_proba(X) + (1 - w) * self.lr.predict_proba(X)
        if self.sk is not None:
            try:
                p = 0.5 * p + 0.5 * self.sk.predict_proba(X)[:, 1]
            except Exception:
                pass
        return np.clip(p, 1e-6, 1 - 1e-6)

    def _calibrate(self, p, y, nbin: int = 12):
        """Monotone (pool-adjacent-violators) reliability map on the val fold."""
        order = np.argsort(p)
        p, y = p[order], y[order].astype(float)
        n = len(p)
        if n < nbin * 4:
            self.cal_x, self.cal_y = None, None
            return
        edges = np.linspace(0, n, nbin + 1).astype(int)
        bx = np.array([p[a:b].mean() for a, b in zip(edges[:-1], edges[1:])])
        by = np.array([y[a:b].mean() for a, b in zip(edges[:-1], edges[1:])])
        bw = np.array([b - a for a, b in zip(edges[:-1], edges[1:])],
                      dtype=float)
        # PAVA -- enforce monotone non-decreasing calibration
        i = 0
        while i < len(by) - 1:
            if by[i] > by[i + 1] + 1e-12:
                tot = bw[i] + bw[i + 1]
                by[i] = (by[i] * bw[i] + by[i + 1] * bw[i + 1]) / tot
                bx[i] = (bx[i] * bw[i] + bx[i + 1] * bw[i + 1]) / tot
                bw[i] = tot
                by = np.delete(by, i + 1)
                bx = np.delete(bx, i + 1)
                bw = np.delete(bw, i + 1)
                i = max(i - 1, 0)
            else:
                i += 1
        self.cal_x, self.cal_y = bx, by

    def predict_proba(self, X):
        p = self._raw(X)
        if self.cal_x is None or len(self.cal_x) < 2:
            return p
        return np.clip(np.interp(p, self.cal_x, self.cal_y), 1e-6, 1 - 1e-6)


# ===========================================================================
# 7. THE ENGINE
# ===========================================================================
class TrendConvexEngine:
    """ML-gated convex perpetual engine, causal walk-forward."""

    def __init__(self, cfg: Optional[R10Config] = None,
                 risk: Optional[RiskConfig] = None):
        self.cfg = cfg or R10Config()
        self.risk = risk or RiskConfig()
        self.feat = FeatureFactory(self.cfg)
        self.sampler = EventSampler(self.cfg)
        self._panel_cache: Optional[Panel] = None

    # ------------------------------------------------------------------
    def _stack(self, F, rows, cols) -> np.ndarray:
        return np.column_stack([F[k][rows, cols] for k in FEATURE_NAMES])

    def _events(self, p: Panel, F, lo: int, hi: int):
        """All sampled events with bar index in [lo, hi)."""
        side, stop, setup, R = self.sampler.detect(p, F)
        rows, cols = np.nonzero(setup != 0)
        keep = (rows >= lo) & (rows < hi)
        rows, cols = rows[keep], cols[keep]
        return (rows, cols, side[rows, cols], stop[rows, cols],
                setup[rows, cols], R[rows, cols])

    # ------------------------------------------------------------------
    def fit_model(self, p: Panel, F, t_train_end: int):
        """Train strictly on events at t <= t_train_end (already purged)."""
        cfg = self.cfg
        lo = max(cfg.warmup_bars, t_train_end - cfg.train_days * BARS_PER_DAY)
        rows, cols, sides, stops, setups, R = self._events(p, F, lo,
                                                           t_train_end)
        if len(rows) < cfg.min_train_events:
            return None, {"reason": f"insufficient_train_events:{len(rows)}",
                          "auc": 0.5, "n": int(len(rows)), "p_star": 1.01}

        if len(rows) > cfg.max_train_events:      # keep the MOST RECENT
            sel = np.argsort(rows)[-cfg.max_train_events:]
            rows, cols = rows[sel], cols[sel]
            sides, stops, setups, R = sides[sel], stops[sel], setups[sel], R[sel]

        entries = np.array([p.open[min(int(t) + 1, p.T - 1), int(j)]
                            for t, j in zip(rows, cols)])
        entries = entries * (1.0 + cfg.entry_slippage * sides)
        y, r_real = triple_barrier(p, rows, cols, sides, entries, R, cfg)
        X = self._stack(F, rows, cols)
        ok = np.isfinite(X).all(1) & np.isfinite(entries) & (R > 0)
        X, y, r_real, rows = X[ok], y[ok], r_real[ok], rows[ok]
        if len(y) < cfg.min_train_events or y.min() == y.max():
            return None, {"reason": f"degenerate_labels:{len(y)}", "auc": 0.5,
                          "n": int(len(y)), "p_star": 1.01}

        # ---- causal split: the validation fold is the TAIL of train ----
        cut = int(len(y) * (1.0 - cfg.val_frac))
        srt = np.argsort(rows, kind="stable")
        X, y, r_real = X[srt], y[srt], r_real[srt]
        Xtr, ytr = X[:cut], y[:cut]
        Xva, yva, rva = X[cut:], y[cut:], r_real[cut:]
        if len(Xva) < cfg.min_val_events or ytr.min() == ytr.max():
            return None, {"reason": f"thin_validation:{len(Xva)}", "auc": 0.5,
                          "n": int(len(y)), "p_star": 1.01}

        model = MLEnsemble(cfg).fit(Xtr, ytr, Xva, yva)
        pva = model.predict_proba(Xva)
        p_star, diag = self._pick_threshold(pva, rva, cfg)
        diag.update({"auc": round(model.auc_val, 4), "n": int(len(y)),
                     "n_val": int(len(yva)), "base_rate": round(float(y.mean()), 4)})
        return model, diag

    def _pick_threshold(self, pva, rva, cfg):
        """Dynamic p*: maximise in-validation expected R per trade, subject to
        producing enough events to clear the >=15 trades/window floor.

        Selection uses realised R (not accuracy) because the objective is
        expected value under a 4:1 payoff, not classification quality.
        """
        # ------------------------------------------------------------------
        # The grid MUST be quantile-based, not absolute.  The +4R triple
        # barrier has a base rate of roughly 3-10%, so a *calibrated*
        # probability essentially never exceeds 0.30 -- an absolute grid of
        # 0.30..0.90 selects nothing and silently disables the classifier.
        # Selecting on quantiles of the validation probabilities makes the
        # threshold invariant to the base rate and to regime shifts in it.
        # ------------------------------------------------------------------
        qs = np.linspace(cfg.sel_q_lo, cfg.sel_q_hi, cfg.p_grid_n)
        grid = np.unique(np.quantile(pva, qs))
        need = cfg.target_trades_per_window * cfg.trade_headroom
        # validation fold spans some number of "window-equivalents"; require
        # the selected rate to imply at least `need` events per window-equiv.
        best, best_score, rows = None, -np.inf, []
        for q in grid:
            sel = pva >= q
            k = int(sel.sum())
            if k < 12:
                continue
            er = float(rva[sel].mean())
            wr = float((rva[sel] > 0).mean())
            # score: expected R scaled by sqrt(count) -- rewards edge that
            # survives at usable frequency, penalises 3-trade flukes.
            score = er * math.sqrt(k)
            rows.append((q, k, er, wr, score))
            if score > best_score and er > 0:
                best_score, best = score, (q, k, er, wr)
        if best is None:
            if not cfg.soft_fallback:
                return 1.01, {"reason": "no_positive_ev_threshold",
                              "p_star": 1.01}
            q = float(np.quantile(pva, cfg.fallback_p_quantile))
            return q, {"reason": "soft_fallback_no_ev", "p_star": round(q, 4),
                       "exp_r_val": None}
        q, k, er, wr = best
        # relax if the threshold is so strict it cannot supply 15 trades
        frac = k / max(len(pva), 1)
        if frac * need < 1.0 and rows:
            cand = [r for r in rows if r[2] > 0]
            if cand:
                q = min(r[0] for r in cand)
                sel = pva >= q
                er = float(rva[sel].mean())
                wr = float((rva[sel] > 0).mean())
        return float(q), {"reason": "ok", "p_star": round(float(q), 4),
                          "exp_r_val": round(er, 4),
                          "wr_val": round(wr * 100, 2),
                          "sel_frac": round(frac, 4)}

    # ------------------------------------------------------------------
    def _tp_r(self, setup, liq_z, oi_1h) -> float:
        """Directive 3.3: squeeze-fuelled breakouts earn an extended target.
        Everything else keeps the 4R barrier the model was trained on."""
        cfg = self.cfg
        if setup == SETUP_TREND_SQZ:
            # forced buy-ins supply the fuel; extreme squeezes run further
            return (cfg.tp_r_rocket if liq_z >= cfg.sqz_liq_z_extreme
                    else cfg.tp_r_cascade)
        if (setup == SETUP_LIQ and liq_z >= cfg.cascade_liq_z
                and oi_1h <= cfg.cascade_oi_drop):
            return cfg.tp_r_cascade
        return cfg.tp_r

    # ------------------------------------------------------------------
    def run_window(self, per_symbol, win_start, win_end, funding=None,
                   oi=None, window_id: str = "W", panel: Optional[Panel] = None,
                   extra=None, verbose: bool = False) -> Dict:
        cfg, rk = self.cfg, self.risk
        full = panel if panel is not None else Panel(per_symbol, extra=extra)
        ws, we = pd.Timestamp(win_start), pd.Timestamp(win_end)
        if we.hour == 0 and we.minute == 0:
            we = we + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)

        hist_start = ws - pd.Timedelta(days=cfg.train_days + 30)
        p = full.slice(hist_start, we)
        if p.T < cfg.warmup_bars + 50:
            return self._empty(window_id, "insufficient_history")

        F = self.feat.build(p, funding, oi)
        t_start = int(p.index.searchsorted(ws, side="left"))
        t_purge = int(p.index.searchsorted(ws - pd.Timedelta(hours=cfg.purge_hours),
                                           side="left"))
        if t_start >= p.T:
            return self._empty(window_id, "window_not_in_data")

        model, diag = self.fit_model(p, F, t_purge)

        side_m, stop_m, setup_m, R_m = self.sampler.detect(p, F)
        p_star = float(diag.get("p_star", 1.01))

        # ---- score every in-window event ONCE (no refit inside window) ----
        rows, cols = np.nonzero(setup_m != 0)
        inwin = rows >= t_start
        rows, cols = rows[inwin], cols[inwin]
        phat = np.zeros((p.T, p.N))
        if model is not None and len(rows):
            Xw = self._stack(F, rows, cols)
            good = np.isfinite(Xw).all(1)
            pr = np.zeros(len(rows))
            if good.any():
                pr[good] = model.predict_proba(Xw[good])
            phat[rows, cols] = pr
        elif cfg.soft_fallback:
            phat[rows, cols] = 1.0          # ungated fallback, reported loudly
            p_star = 0.5
            diag = dict(diag or {})
            diag["reason"] = diag.get("reason", "no_model") + "|ungated_fallback"

        atr_d, ev = F["_daily_atr"], F["_fund_event"]
        batr_x = F["_bar_atr"]
        llz, slz, oi1 = F["long_liq_z"], F["short_liq_z"], F["oi_d1h"]
        O, H, L, C = p.open, p.high, p.low, p.close

        equity = rk.initial_capital           # REALISED equity (cash)
        peak = equity
        max_dd = 0.0
        positions: List[Position] = []
        trades: List[Dict] = []
        curve: List[Tuple[pd.Timestamp, float]] = []
        cooldown = np.full(p.N, -10 ** 9, dtype=np.int64)
        halted = False

        def mtm(t: int, worst: bool) -> float:
            """Mark to market. In `worst` mode this must value the book at what
            it would ACTUALLY liquidate for -- i.e. at the bar extreme AFTER
            exit slippage and the exit taker fee. Valuing at the raw extreme
            makes the circuit breaker optimistic, which lets realised drawdown
            overshoot the 4.5% trigger and breach the 5.0% hard ceiling."""
            eq = equity
            for q in positions:
                px = (L[t, q.col] if q.side == 1 else H[t, q.col]) if worst \
                    else C[t, q.col]
                if not np.isfinite(px):
                    px = q.entry_px
                if worst:
                    # same fill model as close_position()
                    px = px * (1.0 - cfg.exit_slippage * q.side)
                    eq += q.open_pnl(px) - cfg.taker_fee * abs(px) * q.qty
                else:
                    eq += q.open_pnl(px)
            return eq

        def close_position(q: Position, t: int, px: float, why: str):
            nonlocal equity
            fill = px * (1.0 - cfg.exit_slippage * q.side)
            q.fees_paid += cfg.taker_fee * abs(fill) * q.qty
            pnl = q.open_pnl(fill)            # already net of all fees+funding
            equity += pnl
            trades.append({
                "window_id": window_id, "sym": q.symbol, "side": q.side,
                "setup": SETUP_NAME[q.setup], "p_hat": round(q.p_hat, 4),
                "entry_ts": p.index[q.entry_bar], "exit_ts": p.index[t],
                "entry_px": round(q.entry_px, 8), "exit_px": round(fill, 8),
                "qty": q.qty, "r_px": q.r_px, "risk_d": round(q.risk_d, 2),
                "r_multiple": round(pnl / max(q.risk_d, 1e-9), 4),
                "pnl_d": round(pnl, 4), "fees_d": round(q.fees_paid, 4),
                "funding_d": round(q.funding_pnl, 4),
                "bars_held": t - q.entry_bar, "why": why,
                "mfe_r": round(q.mfe_r, 3), "conf_score": q.conf_score,
                "n_adds": q.n_adds,
            })
            cooldown[q.col] = t + cfg.cooldown_bars

        # ----------------------- main bar loop -----------------------
        for t in range(t_start, p.T):
            # (1) event-time funding on OPEN positions
            for q in positions:
                if ev[t, q.col] != 0.0 and p.valid[t, q.col]:
                    q.funding_pnl += -q.side * ev[t, q.col] * C[t, q.col] * q.qty

            # (2) HARD intrabar circuit breaker (4.5% / $225), before anything
            eq_worst = mtm(t, worst=True)
            if positions and peak > 0 and (peak - eq_worst) / peak >= rk.drawdown_limit:
                for q in list(positions):
                    px = L[t, q.col] if q.side == 1 else H[t, q.col]
                    close_position(q, t, px if np.isfinite(px) else C[t, q.col],
                                   "circuit_breaker")
                positions.clear()
                halted = True
                max_dd = max(max_dd, (peak - eq_worst) / peak)
                curve.append((p.index[t], equity))
                break

            # (3) manage open positions, intrabar-ordered stop-before-target
            for q in list(positions):
                j = q.col
                if not p.valid[t, j]:
                    continue
                h, l_, c_ = H[t, j], L[t, j], C[t, j]
                held = t - q.entry_bar
                if held < 0:
                    continue

                # R geometry is anchored to the ORIGINAL entry, never to the
                # blended average, so adding a pyramid leg cannot retroactively
                # move the ratchet or inflate MFE.
                mfe_px = (h - q.anchor_px) if q.side == 1 else (q.anchor_px - l_)
                q.mfe_r = max(q.mfe_r, mfe_px / max(q.r_px, 1e-12))
                q.run_ext = (max(q.run_ext, h) if q.side == 1
                             else min(q.run_ext, l_)) \
                    if np.isfinite(q.run_ext) else (h if q.side == 1 else l_)

                stop_hit = (l_ <= q.stop_px) if q.side == 1 else (h >= q.stop_px)
                tp_hit = (h >= q.tp_px) if q.side == 1 else (l_ <= q.tp_px)
                if stop_hit:                       # conservative ordering
                    close_position(q, t, q.stop_px, "stop")
                    positions.remove(q)
                    continue
                if tp_hit:
                    close_position(q, t, q.tp_px, "target")
                    positions.remove(q)
                    continue

                # time decay -- trend waves run on a slower clock than fades
                cur_r = (q.side * (c_ - q.anchor_px)) / max(q.r_px, 1e-12)
                is_trend = q.setup in TREND_SETUPS
                decay_bars = (cfg.trend_time_decay_bars if is_trend
                              else cfg.time_decay_bars)
                max_bars = (cfg.trend_hold_max_bars if is_trend
                            else cfg.hold_max_bars)
                if held >= decay_bars and cur_r < cfg.time_decay_min_r:
                    close_position(q, t, c_, "time_decay")
                    positions.remove(q)
                    continue
                if held >= max_bars:
                    close_position(q, t, c_, "max_hold")
                    positions.remove(q)
                    continue

                # ---- ANTI-SUFFOCATION RATCHET (Round 10 directive 3.4) ----
                # Widened tiers. Round 9's real-data run stopped 7 trades at
                # +0.60R that had already shown +1.5R..+3.07R MFE; those tiers
                # were choking the 4R-8R tail this engine exists to harvest.
                for tier_i, (gain_r, lock_r) in enumerate(cfg.ratchet, start=1):
                    if q.mfe_r >= gain_r and q.tier < tier_i:
                        new_stop = q.anchor_px + q.side * lock_r * q.r_px
                        q.stop_px = (max(q.stop_px, new_stop) if q.side == 1
                                     else min(q.stop_px, new_stop))
                        q.tier = tier_i
                # Chandelier arms only PAST +3.5R, and trails at 2.2 x ATR_14
                # from the running extreme -- wide enough for a 5R-8R runner.
                if q.mfe_r >= cfg.trail_start_r:
                    ref = q.run_ext if np.isfinite(q.run_ext) else (
                        h if q.side == 1 else l_)
                    a = batr_x[t, j]
                    if not np.isfinite(a) or a <= 0:
                        a = atr_d[t, j]
                    trail = (ref - cfg.trail_atr_mult * a) if q.side == 1 \
                        else (ref + cfg.trail_atr_mult * a)
                    if np.isfinite(trail):
                        q.stop_px = (max(q.stop_px, trail) if q.side == 1
                                     else min(q.stop_px, trail))

                # ---- PYRAMIDING on house money (directive 3.5) ----
                # Only once the stop is locked at breakeven-or-better, so the
                # add cannot convert a locked winner into a loser.
                if (q.n_adds < rk.pyramid_max_legs
                        and q.mfe_r >= rk.pyramid_min_mfe_r
                        and q.side * (q.stop_px - q.anchor_px) >= 0.0
                        and t + 1 < p.T and p.valid[t + 1, j]):
                    add_px = O[t + 1, j] * (1.0 + cfg.entry_slippage * q.side)
                    locked = q.side * (q.stop_px - q.anchor_px)
                    # the add's own worst case, bounded by the locked profit
                    adverse = max(q.side * (add_px - q.stop_px), 0.0)
                    add_qty = rk.pyramid_frac * q.legs[0][1]
                    # A pyramid leg adds NOTIONAL, and notional is what a gap
                    # bar prices -- not the locked stop. So the add is bound by
                    # the same catastrophic-gap budget as an opening trade,
                    # otherwise pyramiding quietly widens tail drawdown.
                    if peak > 0:
                        room = (rk.hard_dd_cap * peak - max(0.0, peak - equity)
                                - rk.gap_multiplier * sum(
                                    x.risk_d for x in positions))
                        if room <= 0:
                            room = 0.0
                        add_qty = min(add_qty, room / max(
                            add_px * rk.catastrophic_gap, 1e-9))
                    if (np.isfinite(add_px) and add_px > 0 and add_qty > 0
                            and adverse * add_qty <= locked * q.legs[0][1]):
                        q.legs.append((add_px, add_qty))
                        q.fees_paid += cfg.taker_fee * add_px * add_qty
                        q.n_adds += 1

            # (4) bar-by-bar mark-to-market, peak and drawdown
            eq_now, eq_low = mtm(t, worst=False), mtm(t, worst=True)
            peak = max(peak, eq_now)
            if peak > 0:
                max_dd = max(max_dd, (peak - eq_low) / peak)
            curve.append((p.index[t], eq_now))
            if halted or t + 1 >= p.T:
                continue

            # (5) new entries -- ML gated
            if len(positions) >= rk.max_positions:
                continue
            held_cols = {q.col for q in positions}
            cand = []
            for j in range(p.N):
                if (j in held_cols or setup_m[t, j] == 0 or not p.valid[t, j]
                        or t <= cooldown[j] or not p.valid[t + 1, j]):
                    continue
                if phat[t, j] < p_star:
                    continue
                cand.append((-phat[t, j], j))
            if not cand:
                continue
            cand.sort()

            for _, j in cand[:cfg.top_k_per_bar]:
                if len(positions) >= rk.max_positions:
                    break
                s = int(side_m[t, j])
                entry = O[t + 1, j] * (1.0 + cfg.entry_slippage * s)
                if not np.isfinite(entry) or entry <= 0:
                    continue
                R = float(R_m[t, j])
                if not np.isfinite(R) or R <= 1e-12:
                    continue

                # ---- friction viability: 33-41 bps must be <= 30% of 1R ----
                friction_px = entry * (2.0 * cfg.taker_fee + cfg.entry_slippage
                                       + cfg.exit_slippage)
                if friction_px > cfg.max_friction_r * R:
                    continue

                # ---- Directive 3.E: non-linear house-money sizing ----
                realised = equity - rk.initial_capital
                dd_now = (peak - eq_now) / peak if peak > 0 else 0.0
                if dd_now > rk.dd_defense_trigger:
                    risk_d = rk.drawdown_defense_risk
                else:
                    risk_d = rk.base_risk + rk.kelly_frac * max(0.0, realised)
                risk_d = min(risk_d, rk.max_risk_per_trade)

                # ---- HARD capital-protection floor ----
                open_risk = sum(abs(q.stop_px - q.entry_px) * q.qty
                                for q in positions)
                headroom = equity - open_risk - rk.capital_floor
                if headroom <= 0:
                    continue
                risk_d = min(risk_d, headroom)

                # ---- gap-aware drawdown budget --------------------------
                # Remaining loss we can absorb from the running peak before
                # touching the hard ceiling, net of what is already at risk.
                # Dividing by gap_multiplier reserves room for the breaker
                # exiting worse than the stop on a gap bar.
                if peak > 0:
                    dd_budget = rk.hard_dd_cap * peak
                    already = max(0.0, peak - eq_now)
                    # Existing open risk must ALSO be inflated by the gap
                    # multiplier -- those stops can be jumped through too.
                    remaining = (dd_budget - already
                                 - rk.gap_multiplier * open_risk)
                    if remaining <= 0:
                        continue
                    risk_d = min(risk_d, remaining / rk.gap_multiplier)
                    # tail-notional bound: loss under a catastrophic gap must
                    # still fit inside the remaining budget. Expressed as a
                    # risk cap so it composes with the sizing above.
                    risk_d = min(risk_d,
                                 remaining * R / (entry * rk.catastrophic_gap))

                if risk_d < 1.0:
                    continue

                qty = risk_d / R
                cap = min(rk.max_symbol_leverage * eq_now,
                          rk.max_gross_leverage * eq_now
                          - sum(q.notional for q in positions))
                if cap <= 0:
                    continue
                qty = min(qty, cap / entry)
                if qty <= 0:
                    continue

                tp_r = self._tp_r(int(setup_m[t, j]),
                                  max(llz[t, j], slz[t, j]), oi1[t, j])
                fee = cfg.taker_fee * entry * qty   # netted via open_pnl
                positions.append(Position(
                    symbol=p.symbols[j], col=j, side=s,
                    setup=int(setup_m[t, j]), r_px=R, anchor_px=entry,
                    stop_px=entry - s * R, tp_px=entry + s * tp_r * R,
                    tp_r=tp_r, entry_bar=t + 1, legs=[(entry, qty)],
                    fees_paid=fee, risk_d=qty * R, p_hat=float(phat[t, j]),
                    conf_score=int(round(F["fp_conf"][t, j] * 6))))

        # ---------------- force-flat at window end ----------------
        if positions:
            t_end = p.T - 1
            for q in list(positions):
                px = C[t_end, q.col]
                close_position(q, t_end, px if np.isfinite(px) else q.entry_px,
                               "window_end")
            positions.clear()
            curve.append((p.index[t_end], equity))

        return self._score(window_id, equity, max_dd, trades, curve, diag,
                           bool(F["_has_oi"][0]), halted,
                           float(F["_of_cover"][0]))

    # ------------------------------------------------------------------
    def _empty(self, wid, reason) -> Dict:
        return {"window_id": wid, "trades": 0, "roi_pct": 0.0,
                "max_dd_pct": 0.0, "win_rate_pct": 0.0, "avg_r": 0.0,
                "max_r": 0.0, "profit_factor": 0.0, "equity": self.risk.initial_capital,
                "halted": False, "setup_mix": {}, "reason": reason,
                "p_star": None, "auc": None, "exp_r_val": None, "n_train": 0,
                "has_real_oi": False, "orderflow_cover": 0.0,
                "mfe_giveback_r": 0.0, "trades_list": [], "equity_curve": []}

    def _score(self, wid, equity, max_dd, trades, curve, diag, has_oi,
               halted, of_cover: float = 0.0) -> Dict:
        rk = self.risk
        n = len(trades)
        wins = sum(1 for x in trades if x["pnl_d"] > 0)
        rs = [x["r_multiple"] for x in trades]
        gw = sum(x["pnl_d"] for x in trades if x["pnl_d"] > 0)
        gl = -sum(x["pnl_d"] for x in trades if x["pnl_d"] <= 0)
        mix: Dict[str, int] = {}
        for x in trades:
            mix[x["setup"]] = mix.get(x["setup"], 0) + 1
        return {
            "window_id": wid,
            "trades": n,
            "roi_pct": round((equity / rk.initial_capital - 1.0) * 100, 4),
            "max_dd_pct": round(max_dd * 100, 4),
            "win_rate_pct": round(wins / n * 100, 2) if n else 0.0,
            "avg_r": round(float(np.mean(rs)), 4) if n else 0.0,
            "max_r": round(float(np.max(rs)), 4) if n else 0.0,
            "profit_factor": round(gw / gl, 3) if gl > 1e-9 else (
                float("inf") if gw > 0 else 0.0),
            "equity": round(equity, 4),
            "halted": halted,
            "setup_mix": mix,
            "reason": (diag or {}).get("reason", "ok"),
            "p_star": (diag or {}).get("p_star"),
            "auc": (diag or {}).get("auc"),
            "exp_r_val": (diag or {}).get("exp_r_val"),
            "n_train": (diag or {}).get("n", 0),
            "has_real_oi": bool(has_oi),
            # Fraction of the real orderflow feeds that were actually present.
            # A run with orderflow_cover ~0 is NOT testing the orderflow
            # thesis -- it is running on proxies. Always read this field.
            "orderflow_cover": round(float(of_cover), 3),
            "mfe_giveback_r": round(float(np.mean(
                [max(0.0, x["mfe_r"] - x["r_multiple"]) for x in trades])), 3)
            if trades else 0.0,
            "trades_list": trades,
            "equity_curve": curve,
        }

    # ------------------------------------------------------------------
    @staticmethod
    def criteria_check(res: Dict, crit: Optional[Dict] = None
                       ) -> Tuple[bool, str]:
        c = crit or {"min_roi_percent": 20.0, "max_dd_percent": 5.0,
                     "min_winrate_percent": 40.0, "min_r_multiple": 4,
                     "min_trades": 15}
        fails = []
        if res["roi_pct"] < c["min_roi_percent"]:
            fails.append("roi")
        if res["max_dd_pct"] >= c["max_dd_percent"]:
            fails.append("dd")
        if res["win_rate_pct"] < c["min_winrate_percent"]:
            fails.append("wr")
        if res["trades"] < c["min_trades"]:
            fails.append("trades")
        if res["avg_r"] < c["min_r_multiple"]:
            fails.append("avg_r")
        return (len(fails) == 0), ",".join(fails)

    def run_walkforward(self, per_symbol, windows: Sequence[Dict],
                        funding=None, oi=None, extra=None,
                        fail_fast: bool = True,
                        criteria: Optional[Dict] = None,
                        verbose: bool = True) -> pd.DataFrame:
        """Sequential causal walk-forward W01 -> W20 with fail-fast halt."""
        panel = Panel(per_symbol, extra=extra)
        self._panel_cache = panel
        out, halt_at = [], None
        for w in windows:
            wid = w.get("window_id", len(out) + 1)
            wid = f"W{int(wid):02d}" if not isinstance(wid, str) else wid
            res = self.run_window(per_symbol, w["start_date"], w["end_date"],
                                  funding=funding, oi=oi, window_id=wid,
                                  panel=panel)
            ok, why = self.criteria_check(res, criteria)
            row = {k: res[k] for k in ("window_id", "trades", "roi_pct",
                                       "max_dd_pct", "win_rate_pct", "avg_r",
                                       "max_r", "profit_factor", "halted",
                                       "setup_mix", "reason", "p_star", "auc",
                                       "exp_r_val", "n_train", "has_real_oi",
                                       "orderflow_cover", "mfe_giveback_r")}
            row["name"] = w.get("name", "")
            row["regime"] = w.get("regime", "")
            row["PASS"] = ok
            row["failed"] = why
            out.append(row)
            if verbose:
                print(f"{row['window_id']} {'PASS' if ok else 'FAIL':4s} "
                      f"n={row['trades']:3d} roi={row['roi_pct']:8.2f}% "
                      f"dd={row['max_dd_pct']:5.2f}% wr={row['win_rate_pct']:5.1f}% "
                      f"avgR={row['avg_r']:6.2f} p*={row['p_star']} "
                      f"auc={row['auc']} [{row['failed'] or 'ok'}]")
            if not ok and fail_fast:
                halt_at = row["window_id"]
                if verbose:
                    print(f"\n>>> FAIL-FAST HALT at {halt_at}: {why}")
                break
        df = pd.DataFrame(out)
        df.attrs["halted_at"] = halt_at
        return df


# Backwards-compatible aliases so Round 7/8/9 runners import unchanged.
MLConvexEngine = TrendConvexEngine
ConvexHybridEngine = TrendConvexEngine
ResidualDislocationEngine = TrendConvexEngine
R9Config = R10Config


def run_walkforward_from_json(per_symbol, windows_json_path: str,
                              criteria_json_path: Optional[str] = None,
                              funding=None, oi=None, extra=None,
                              fail_fast: bool = True):
    """Convenience entry point matching the repo layout:
        run_walkforward_from_json(px, 'Engine/oos_windows_20.json',
                                  'Engine/target_oos_criteria.json')
    """
    with open(windows_json_path) as f:
        windows = json.load(f)
    crit = None
    if criteria_json_path:
        with open(criteria_json_path) as f:
            crit = json.load(f).get("target_criteria")
    return TrendConvexEngine().run_walkforward(
        per_symbol, windows, funding=funding, oi=oi, extra=extra,
        fail_fast=fail_fast, criteria=crit)


# ===========================================================================
# 8. SYNTHETIC SELF-TEST  (harness proof only -- NOT a performance claim)
# ===========================================================================
def _synth_panel(symbols, start, periods, seed: int = 11):
    rng = np.random.default_rng(seed)
    idx = pd.date_range(start, periods=periods, freq="15min", tz=None)
    mkt = rng.standard_normal(periods) * 0.004
    for i in range(1, periods):                      # vol clustering
        mkt[i] += 0.28 * mkt[i - 1]
    px, fund, oi = {}, {}, {}
    for k, s in enumerate(symbols):
        beta = 0.7 + 0.09 * k
        r = beta * mkt + rng.standard_normal(periods) * 0.0035
        shock = rng.random(periods) < 0.0025          # liquidation cascades
        r[shock] -= 0.05 + rng.random(int(shock.sum())) * 0.05
        # The cascade shocks inject a persistent negative drift (~-1.9e-4 per
        # bar). Over a multi-year panel that compounds to exp(-41) and the
        # series underflows to 0.0, which makes every ratio feature garbage.
        # De-mean so the synthetic series stays in a realistic price range.
        r = r - r.mean()
        c = 100.0 * (1 + k * 0.4) * np.exp(np.cumsum(r))
        hi = c * (1 + np.abs(rng.standard_normal(periods)) * 0.0035)
        lo = c * (1 - np.abs(rng.standard_normal(periods)) * 0.0035)
        op = np.concatenate([[c[0]], c[:-1]])
        vol = np.exp(rng.standard_normal(periods) * 0.5) * 1e6
        vol[shock] *= 9.0
        px[s] = pd.DataFrame({"open": op, "high": np.maximum.reduce([hi, op, c]),
                              "low": np.minimum.reduce([lo, op, c]),
                              "close": c, "volume": vol}, index=idx)
        fidx = idx[::32]                              # 8h == 32 x 15m bars
        fund[s] = pd.Series(rng.standard_normal(len(fidx)) * 0.0004, index=fidx)
        o = np.exp(np.cumsum(rng.standard_normal(periods) * 0.004)) * 1e8
        o[shock] *= 0.80                              # OI collapse on cascade
        oi[s] = pd.Series(np.maximum.accumulate(np.ones(periods)) * o, index=idx)
    return px, fund, oi


if __name__ == "__main__":
    SYMS = ["ADAUSDT", "APTUSDT", "ARBUSDT", "AVAXUSDT", "BCHUSDT", "BNBUSDT",
            "BTCUSDT", "DOGEUSDT", "DOTUSDT", "ETHUSDT", "LINKUSDT", "LTCUSDT",
            "NEARUSDT", "OPUSDT", "SOLUSDT", "SUIUSDT", "TRXUSDT", "XRPUSDT"]
    px, fund, oi = _synth_panel(SYMS, "2023-01-01", 96 * 560)
    wins = [{"window_id": i + 1, "name": f"synthetic-{i+1}",
             "start_date": d, "end_date": e} for i, (d, e) in enumerate(
                [("2024-02-01", "2024-02-29"), ("2024-03-01", "2024-03-31"),
                 ("2024-04-01", "2024-04-30")])]
    eng = TrendConvexEngine()
    print("sklearn available:", _HAS_SK)
    card = eng.run_walkforward(px, wins, funding=fund, oi=oi, fail_fast=False)
    cols = ["window_id", "trades", "roi_pct", "max_dd_pct", "win_rate_pct",
            "avg_r", "max_r", "profit_factor", "p_star", "auc", "n_train",
            "reason", "PASS", "failed"]
    print("\n", card[cols].to_string(index=False))
    print("\nNOTE: synthetic random-walk data. This proves the HARNESS runs "
          "end-to-end and is causal; it is NOT a performance claim.")
