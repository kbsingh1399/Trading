"""
RP2 / ROUND 8 -- CONVEX LIQUIDATION x LEAD-LAG x FUNDING-SQUEEZE HYBRID (v8.0)
=============================================================================
Drop-in successor to `rp2_round7_residual_dislocation.ResidualDislocationEngine`.
Same public API:

    eng = ConvexHybridEngine(mode="compliant")
    res = eng.run_window(per_symbol, funding=..., oi=..., basis=...,
                         win_start="2021-05-01", win_end="2021-05-31",
                         window_id="W01")
    df  = eng.run_walkforward(per_symbol, windows, funding=..., oi=...,
                              fail_fast=True)

WHY THIS ENGINE EXISTS
----------------------
Round 7 (residual dislocation) is a *linear, symmetric* mean-reversion book.
Its payoff geometry caps at ~4R and its hit-rate/edge product cannot produce
40R net/month at $25 fixed risk under 33 bps round-trip. Round 8 replaces the
payoff geometry, not just the alpha:

  1. FORCED-LIQUIDATION EXHAUST  (setup 1) : OI collapse >= 10-15% in 1h +
     directional liquidation impulse + two-stage flush/reclaim. Stop sits at
     the structural invalidation (the flush extreme), so 1R is SMALL relative
     to the snapback -> 5R-10R right tail. This is the convexity engine.
  2. LEAD-LAG CROSS-ASSET SPILLOVER (setup 2) : BTC/ETH 1h orderflow impulse
     that high-beta alts (SOL/DOGE/AVAX/NEAR/SUI/APT/ARB/OP) have NOT yet
     repriced. Short horizon (<= 6h), 3R target. This is the trade-count
     engine -- it is what gets each window over the >= 6 trades floor.
  3. FUNDING SQUEEZE (setup 3) : annualised funding >= +100% (crowded longs,
     price failing highs -> short) or <= -60% (capitulation + reclaim -> long).
     Mathematically forced flows, 4R target.
  4. NON-LINEAR KELLY / HOUSE-MONEY PYRAMIDING : risk per trade is
     base + kelly_frac * banked_profit, with a hard PRINCIPAL FLOOR --
     realised equity may never fall below initial*(1-0.045). Free-rolled
     profit does the compounding; principal is never exposed to it.

ALL ROUND-7 HARNESS FIXES ARE PRESERVED
---------------------------------------
  * timestamp-union Panel, no positional `.iat[t]` misalignment
  * true causal Wilder DAILY ATR (shifted one day, ffilled onto 15m grid)
  * event-time funding accrual (exactly at settlement bars, not every bar)
  * slippage applied ONCE, in price space, never double-counted in R
  * fees on true notional, both sides
  * bar-by-bar intrabar mark-to-market equity + hard 4.5% kill-switch that
    can fire INTRA-trade (not only at trade close)
  * `entry_bar = t+1` (never a sentinel), same-bar stop-outs are real stops
  * no RNG anywhere -- fully deterministic
  * purged (72h) walk-forward gate + meta-label model fit on TRAIN ONLY

Author: Opus 5, 2026-09-08. Deterministic, numpy/pandas only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

BARS_PER_DAY = 96          # 15m bars
BARS_PER_HOUR = 4
SETUP_LIQ, SETUP_LEADLAG, SETUP_FUND = 1, 2, 3
SETUP_NAME = {0: "none", 1: "liq_exhaust", 2: "lead_lag", 3: "funding_squeeze"}


# ===========================================================================
# 0. CONFIG
# ===========================================================================
@dataclass
class RiskConfig:
    initial_capital: float = 5000.0
    base_risk: float = 25.0                 # 0.50%
    house_money_risk: float = 50.0          # 1.00% -- floor once free-rolling
    drawdown_defense_risk: float = 15.0     # 0.30% when bleeding
    drawdown_limit: float = 0.045           # hard intrabar kill-switch (4.5% / $225)
    dd_defense_trigger: float = 0.025       # de-risk at 2.5% dd
    house_money_trigger: float = 50.0       # banked profit that unlocks tier 2
    # --- non-linear Kelly on BANKED (realised) profit only ---
    kelly_frac: float = 0.42                # risk = base + 0.42 * banked_profit
    max_risk_per_trade: float = 400.0       # 8% of initial, hard cap
    principal_floor_frac: float = 0.045     # realised equity never < 95.5% of init
    # --- pyramiding (funded strictly by OPEN profit) ---
    pyramid_enabled: bool = True
    pyramid_trigger_r: float = 1.50         # add once MFE >= 1.5R AND stop >= BE
    pyramid_frac: float = 0.60              # add qty = 0.60 * initial qty
    pyramid_max_adds: int = 1
    # --- leverage sanity ---
    max_gross_leverage: float = 6.0
    max_symbol_leverage: float = 3.0


@dataclass(frozen=True)
class R8Config:
    # ---------- universe roles ----------
    leaders: Tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "BTC", "ETH")
    high_beta: Tuple[str, ...] = ("SOLUSDT", "DOGEUSDT", "AVAXUSDT", "NEARUSDT",
                                  "SUIUSDT", "APTUSDT", "ARBUSDT", "OPUSDT",
                                  "SOL", "DOGE", "AVAX", "NEAR", "SUI", "APT",
                                  "ARB", "OP")

    # ---------- setup 1: forced-liquidation exhaust ----------
    oi_collapse_1h: float = -0.10           # >= 10% OI destroyed in 1h
    oi_collapse_strong: float = -0.15
    liq_z_thresh: float = 2.00              # liquidation-impulse z
    flush_confirm_bars: int = 10            # reclaim must arrive within 10 bars (2.5h)
    flush_stop_buf_atr: float = 0.18        # stop = flush extreme -/+ 0.18 * daily ATR
    flush_min_r_atr: float = 0.22           # 1R floor in daily-ATR units (anti micro-R)
    flush_max_r_atr: float = 1.30           # 1R ceiling (anti giant-R)
    liq_take_profit_r: float = 8.0          # the convex right tail
    liq_hold_max_bars: int = BARS_PER_DAY * 2

    # ---------- setup 2: lead-lag spillover ----------
    ll_impulse_bars: int = 4                # 1h leader impulse
    ll_impulse_z: float = 2.10
    ll_lag_ratio_max: float = 0.45          # alt has repriced < 45% of beta-implied move
    ll_stop_atr: float = 0.55
    ll_take_profit_r: float = 3.0
    ll_hold_max_bars: int = BARS_PER_HOUR * 6
    ll_min_beta: float = 0.80

    # ---------- setup 3: funding squeeze ----------
    fund_ann_long_crowd: float = 1.00       # +100% annualised -> shorts get paid
    fund_ann_short_crowd: float = -0.60     # -60% annualised -> longs get paid
    fund_confirm_bars: int = 8
    fund_stop_atr: float = 0.90
    fund_take_profit_r: float = 4.0
    fund_hold_max_bars: int = BARS_PER_DAY

    # ---------- shared geometry ----------
    atr_period: int = 14
    hold_min_bars: int = 2
    ratchet_tiers: Tuple[Tuple[float, float], ...] = (
        (1.00, 0.10),      # +1.00R -> lock +0.10R  (free-roll, pyramid unlocks)
        (2.00, 1.05),      # +2.00R -> lock +1.05R
        (3.50, 2.40),      # +3.50R -> lock +2.40R
        (5.50, 4.20),      # +5.50R -> lock +4.20R
    )
    trail_atr_mult: float = 1.15            # chandelier after top tier
    cooldown_bars: int = BARS_PER_HOUR * 3  # per-symbol re-entry cooldown
    max_positions: int = 2                  # spec: max 2 concurrent
    top_k_per_bar: int = 2

    # ---------- regime / quality filters ----------
    rv_fast: int = BARS_PER_DAY
    rv_slow: int = BARS_PER_DAY * 10
    rv_ratio_max: float = 4.00              # liquidation events ARE vol spikes: loose
    rv_ratio_min: float = 0.35
    illiq_window: int = BARS_PER_DAY * 5
    illiq_max_pctile: float = 0.90
    beta_window: int = BARS_PER_DAY * 10
    zscore_window: int = BARS_PER_DAY * 5

    # ---------- frictions (exact, mandatory) ----------
    taker_fee: float = 0.0008               # 8 bps per side on notional
    entry_slippage: float = 0.0010          # 10 bps, applied ONCE in price
    exit_slippage: float = 0.0015           # 15 bps, applied ONCE in price
    # Round-trip friction must never exceed this fraction of 1R. This is THE
    # fix for the Round-6 failure mode: in low-vol chop (W07, W18) a tight 1R
    # makes 33-41 bps of friction cost ~0.5R per trade, which mathematically
    # cannot be recovered at a 40% win rate. Trades whose 1R is too small
    # relative to cost are simply not taken.
    max_friction_r: float = 0.25            # => 1R must be >= ~165 bps

    # ---------- purged walk-forward gate ----------
    train_days: int = 180
    purge_hours: int = 72
    gate_min_events: int = 30
    gate_min_exp_r: float = 0.02
    gate_min_auc: float = 0.52
    gate_soft: bool = True                  # if gate fails, trade UNGATED base setups
                                            # (fail-loud in `gate`, never silently flat)

    # ---------- meta-labeling ----------
    meta_l2: float = 1.0
    meta_iters: int = 450
    meta_lr: float = 0.35
    meta_min_train: int = 50
    meta_prob_floor: float = 0.42


@dataclass
class Position:
    symbol: str
    col: int
    side: int
    setup: int
    r_px: float                 # 1R in price units, FIXED at entry
    stop_px: float
    entry_bar: int
    tp_r: float
    hold_max: int
    legs: List[Tuple[float, float]] = field(default_factory=list)  # (fill_px, qty)
    tier: int = 0
    adds: int = 0
    funding_pnl: float = 0.0
    fees_paid: float = 0.0
    mfe_r: float = 0.0
    risk_d: float = 0.0

    @property
    def qty(self) -> float:
        return sum(q for _, q in self.legs)

    @property
    def entry_px(self) -> float:
        return self.legs[0][0]

    @property
    def notional(self) -> float:
        return sum(px * q for px, q in self.legs)

    def open_pnl(self, px: float) -> float:
        """NET open P&L: gross + funding - all fees accrued so far (entry, adds).
        Netting fees here keeps the equity curve, the MTM drawdown check and the
        trade ledger on one single definition of P&L (they must reconcile)."""
        return (sum(self.side * (px - e) * q for e, q in self.legs)
                + self.funding_pnl - self.fees_paid)


# ===========================================================================
# 1. PANEL -- timestamp-aligned cube (fixes positional misalignment)
# ===========================================================================
_EXTRA_COLS = ("long_liq_zs", "short_liq_zs", "open_interest", "oi",
               "funding_rate", "cvd", "taker_buy_volume", "wick_sell_absorb",
               "wick_buy_absorb", "rsi_14", "vwap_zscore")


class Panel:
    """Timestamp-aligned OHLCV(+extras) cube. Prices are NEVER forward-filled:
    a symbol with a missing bar is untradeable on that bar (`valid` mask)."""

    __slots__ = ("index", "symbols", "open", "high", "low", "close",
                 "volume", "valid", "T", "N", "extras")

    def __init__(self, per_symbol: Dict[str, pd.DataFrame]):
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
            present = any(col in d.columns for d in clean.values())
            if not present:
                return None
            m = np.full((self.T, self.N), np.nan, dtype=np.float64)
            for j, s in enumerate(self.symbols):
                d = clean[s]
                if col in d.columns:
                    m[:, j] = pd.to_numeric(d[col], errors="coerce") \
                                .reindex(self.index).to_numpy(dtype=np.float64)
            return m

        self.open = cube("open")
        self.high = cube("high")
        self.low = cube("low")
        self.close = cube("close")
        vol = cube("volume")
        self.volume = vol if vol is not None else np.ones((self.T, self.N))
        if np.all(~np.isfinite(self.volume)):
            self.volume = np.ones((self.T, self.N))
        self.extras = {c: cube(c) for c in _EXTRA_COLS}
        self.extras = {k: v for k, v in self.extras.items() if v is not None}
        self.valid = (np.isfinite(self.open) & np.isfinite(self.high)
                      & np.isfinite(self.low) & np.isfinite(self.close)
                      & (self.close > 0))

    def slice(self, start: pd.Timestamp, end: pd.Timestamp) -> "Panel":
        lo = int(self.index.searchsorted(start, side="left"))
        hi = int(self.index.searchsorted(end, side="right"))
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
# 2. CAUSAL PRIMITIVES
# ===========================================================================
def _roll(a: np.ndarray, w: int, how: str) -> np.ndarray:
    r = pd.DataFrame(a).rolling(w, min_periods=max(2, w // 4))
    return {"mean": r.mean, "std": (lambda: r.std(ddof=0)), "sum": r.sum,
            "max": r.max, "min": r.min}[how]().to_numpy()


def _xs_pctile(a: np.ndarray) -> np.ndarray:
    """Vectorised row-wise cross-sectional percentile in (0,1]; NaN -> 0.5."""
    fin = np.isfinite(a)
    b = np.where(fin, a, np.inf)
    order = np.argsort(b, axis=1, kind="stable")
    ranks = np.empty_like(order)
    rows = np.arange(a.shape[0])[:, None]
    ranks[rows, order] = np.arange(a.shape[1])[None, :]
    cnt = fin.sum(axis=1, keepdims=True)
    out = (ranks + 1.0) / np.maximum(cnt, 1.0)
    out = np.where(fin & (cnt > 1), out, 0.5)
    return out


def causal_daily_atr(panel: Panel, period: int = 14) -> np.ndarray:
    """TRUE Wilder ATR on DAILY bars, shifted one day, mapped to the 15m grid.
    ATR used at any 15m bar of day D is computed from data through D-1 close."""
    out = np.full((panel.T, panel.N), np.nan, dtype=np.float64)
    for j in range(panel.N):
        s = pd.DataFrame({"high": panel.high[:, j], "low": panel.low[:, j],
                          "close": panel.close[:, j]}, index=panel.index).dropna()
        if len(s) < BARS_PER_DAY * 3:
            continue
        d = s.resample("1D").agg(high=("high", "max"), low=("low", "min"),
                                 close=("close", "last")).dropna()
        if len(d) < 3:
            continue
        pc = d["close"].shift(1)
        tr = pd.concat([(d["high"] - d["low"]).abs(),
                        (d["high"] - pc).abs(),
                        (d["low"] - pc).abs()], axis=1).max(axis=1)
        atr = tr.ewm(alpha=1.0 / period, adjust=False,
                     min_periods=min(period, len(tr))).mean().shift(1)
        out[:, j] = atr.reindex(panel.index, method="ffill").to_numpy()
    floor = 0.012 * panel.close
    out = np.where(np.isfinite(out) & (out > 0), out, floor)
    return np.maximum(np.nan_to_num(out, nan=1e-12), 1e-12)


def event_time_funding(panel: Panel, funding: Optional[Dict[str, pd.Series]]
                       ) -> Tuple[np.ndarray, np.ndarray]:
    """(rate charged AT settlement bar, causal annualised rate ffilled).
    Falls back to a `funding_rate` column in the panel if no dict is given."""
    ev = np.zeros((panel.T, panel.N), dtype=np.float64)
    ann = np.zeros((panel.T, panel.N), dtype=np.float64)

    if not funding and "funding_rate" in panel.extras:
        fr = panel.extras["funding_rate"]
        for j in range(panel.N):
            s = pd.Series(fr[:, j], index=panel.index)
            settle = s.ne(s.shift(1)) & s.notna()
            ev[:, j] = np.where(settle.to_numpy(), np.nan_to_num(fr[:, j]), 0.0)
            ann[:, j] = np.nan_to_num(pd.Series(fr[:, j], index=panel.index)
                                      .shift(1).ffill().to_numpy()) * 3.0 * 365.0
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


def oi_cube(panel: Panel, oi: Optional[Dict[str, pd.Series]]) -> Optional[np.ndarray]:
    if oi:
        m = np.full((panel.T, panel.N), np.nan)
        for j, s in enumerate(panel.symbols):
            o = oi.get(s)
            if o is None or len(o) == 0:
                continue
            o = o.copy()
            o.index = pd.DatetimeIndex(pd.to_datetime(o.index))
            o = o[~o.index.duplicated(keep="last")].sort_index()
            m[:, j] = o.reindex(panel.index.union(o.index)).ffill() \
                       .reindex(panel.index).to_numpy(dtype=np.float64)
        return m
    for k in ("open_interest", "oi"):
        if k in panel.extras:
            return panel.extras[k]
    return None


# ===========================================================================
# 3. FEATURE FACTORY
#    Every value at row t uses information up to and including CLOSE of bar t.
#    Execution always happens at OPEN of bar t+1.
# ===========================================================================
class FeatureFactory:
    def __init__(self, cfg: R8Config):
        self.cfg = cfg

    def build(self, p: Panel, funding=None, oi=None) -> Dict[str, np.ndarray]:
        cfg = self.cfg
        C, H, L, O = p.close, p.high, p.low, p.open
        with np.errstate(divide="ignore", invalid="ignore"):
            ret = np.diff(np.log(np.where(C > 0, C, np.nan)), axis=0, prepend=np.nan)
        ret = np.nan_to_num(ret)

        vmask = p.valid.astype(np.float64)
        denom = np.maximum(vmask.sum(axis=1, keepdims=True), 1.0)
        mkt = (ret * vmask).sum(axis=1, keepdims=True) / denom

        # ---- causal rolling beta on the equal-weight index ----
        w = cfg.beta_window
        cov = _roll(ret * mkt, w, "mean") - _roll(ret, w, "mean") * _roll(mkt, w, "mean")
        var = np.maximum(_roll(mkt * mkt, w, "mean") - _roll(mkt, w, "mean") ** 2, 1e-18)
        beta = np.clip(np.nan_to_num(cov / var, nan=1.0), -3.0, 3.0)
        resid = ret - beta * mkt

        # ---- realised-vol regime + Amihud illiquidity ----
        rv_f = _roll(resid, cfg.rv_fast, "std") * math.sqrt(BARS_PER_DAY)
        rv_s = _roll(resid, cfg.rv_slow, "std") * math.sqrt(BARS_PER_DAY)
        rv_ratio = np.nan_to_num(rv_f / np.maximum(rv_s, 1e-12), nan=1.0)
        dv = np.maximum(C * np.nan_to_num(p.volume), 1.0)
        illiq_pct = _xs_pctile(np.nan_to_num(_roll(np.abs(ret) / dv,
                                                   cfg.illiq_window, "mean"),
                                             nan=np.inf))

        # ---- residual dislocation z (kept from R7: useful meta feature) ----
        disloc = _roll(resid, BARS_PER_DAY // 2, "sum")
        zmu = _roll(disloc, cfg.zscore_window, "mean")
        zsd = np.maximum(_roll(disloc, cfg.zscore_window, "std"), 1e-12)
        resid_z = np.clip(np.nan_to_num((disloc - zmu) / zsd), -6, 6)

        atr = causal_daily_atr(p, cfg.atr_period)
        fund_ev, fund_ann = event_time_funding(p, funding)

        # ---- open interest impulse (1h) ----
        OI = oi_cube(p, oi)
        if OI is not None:
            prev = np.roll(OI, BARS_PER_HOUR, axis=0)
            prev[:BARS_PER_HOUR] = np.nan
            with np.errstate(invalid="ignore", divide="ignore"):
                oi_1h = np.clip(np.nan_to_num(OI / prev - 1.0, nan=0.0,
                                              posinf=0.0, neginf=0.0), -1.0, 1.0)
            prev4 = np.roll(OI, BARS_PER_DAY, axis=0)
            prev4[:BARS_PER_DAY] = np.nan
            oi_1d = np.clip(np.nan_to_num(OI / prev4 - 1.0), -1.0, 1.0)
        else:
            oi_1h = np.zeros_like(C)
            oi_1d = np.zeros_like(C)

        # ---- directional liquidation impulse ----
        if "long_liq_zs" in p.extras and "short_liq_zs" in p.extras:
            long_liq = np.nan_to_num(p.extras["long_liq_zs"])
            short_liq = np.nan_to_num(p.extras["short_liq_zs"])
        else:
            # proxy: range-expansion x volume-surge, signed by bar direction
            rng = np.maximum(H - L, 1e-12) / np.maximum(C, 1e-12)
            vz_mu = _roll(p.volume, BARS_PER_DAY * 5, "mean")
            vz_sd = np.maximum(_roll(p.volume, BARS_PER_DAY * 5, "std"), 1e-12)
            vz = np.nan_to_num((p.volume - vz_mu) / vz_sd)
            imp = rng * np.maximum(vz, 0.0)
            imu = _roll(imp, BARS_PER_DAY * 5, "mean")
            isd = np.maximum(_roll(imp, BARS_PER_DAY * 5, "std"), 1e-12)
            iz = np.clip(np.nan_to_num((imp - imu) / isd), 0.0, 12.0)
            body_dn = (C < O)
            long_liq = np.where(body_dn, iz, 0.0)    # longs being force-sold
            short_liq = np.where(~body_dn, iz, 0.0)  # shorts being squeezed

        # ---- absorption confirmation ----
        higher_low = np.zeros_like(C)
        higher_low[1:] = (L[1:] > L[:-1]).astype(np.float64)
        lower_high = np.zeros_like(C)
        lower_high[1:] = (H[1:] < H[:-1]).astype(np.float64)
        hl3 = _roll(higher_low, 3, "mean")
        lh3 = _roll(lower_high, 3, "mean")

        # ---- lead-lag: leader composite impulse ----
        lead_cols = [j for j, s in enumerate(p.symbols)
                     if s.upper() in {x.upper() for x in cfg.leaders}]
        if not lead_cols:                        # fall back to the 2 largest by $vol
            lead_cols = list(np.argsort(-np.nan_to_num(dv).mean(axis=0))[:2])
        k = cfg.ll_impulse_bars
        cum = pd.DataFrame(ret).rolling(k, min_periods=k).sum().to_numpy()
        lead_slice = np.nan_to_num(cum[:, lead_cols], nan=0.0)
        lead_imp = lead_slice.mean(axis=1, keepdims=True)
        lmu = _roll(lead_imp, cfg.zscore_window, "mean")
        lsd = np.maximum(_roll(lead_imp, cfg.zscore_window, "std"), 1e-12)
        lead_z = np.clip(np.nan_to_num((lead_imp - lmu) / lsd), -8, 8)
        lead_z_full = np.repeat(lead_z, p.N, axis=1)
        expected = beta * lead_imp                                   # beta-implied
        with np.errstate(divide="ignore", invalid="ignore"):
            lag_ratio = np.where(np.abs(expected) > 1e-9,
                                 np.nan_to_num(cum / expected), 1.0)
        lag_ratio = np.clip(lag_ratio, -5.0, 5.0)

        return {
            "ret": ret, "beta": beta, "resid_z": resid_z,
            "rv_ratio": rv_ratio, "illiq_pct": illiq_pct, "atr": atr,
            "fund_event": fund_ev, "fund_ann": fund_ann,
            "oi_1h": oi_1h, "oi_1d": oi_1d,
            "long_liq": long_liq, "short_liq": short_liq,
            "hl3": hl3, "lh3": lh3,
            "lead_z": lead_z_full, "lag_ratio": lag_ratio, "cum_k": np.nan_to_num(cum),
            "xs_mom": _xs_pctile(np.nan_to_num(cum)),
        }


# ===========================================================================
# 4. SETUP DETECTORS -> (side, structural stop anchor, setup id)
# ===========================================================================
class SetupDetector:
    def __init__(self, cfg: R8Config):
        self.cfg = cfg

    def detect(self, p: Panel, F: Dict[str, np.ndarray]
               ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        cfg = self.cfg
        T, N = p.T, p.N
        side = np.zeros((T, N), dtype=np.int8)
        stop = np.full((T, N), np.nan, dtype=np.float64)
        setup = np.zeros((T, N), dtype=np.int8)

        H, L, C, O = p.high, p.low, p.close, p.open
        atr = F["atr"]
        base_ok = (p.valid
                   & (F["rv_ratio"] <= cfg.rv_ratio_max)
                   & (F["rv_ratio"] >= cfg.rv_ratio_min)
                   & (F["illiq_pct"] <= cfg.illiq_max_pctile)
                   & np.isfinite(atr))

        hb = {x.upper() for x in cfg.high_beta}
        lead_set = {x.upper() for x in cfg.leaders}

        # ---------- setup 1: two-stage forced-liquidation exhaust ----------
        long_liq, short_liq = F["long_liq"], F["short_liq"]
        oi_1h = F["oi_1h"]
        hl3, lh3 = F["hl3"], F["lh3"]

        for j in range(N):
            arm_side, f_lo, f_hi, expiry = 0, np.nan, np.nan, -1
            for t in range(1, T):
                if arm_side != 0 and t > expiry:
                    arm_side = 0

                oi_crash = oi_1h[t, j] <= cfg.oi_collapse_1h
                lflush = (long_liq[t, j] >= cfg.liq_z_thresh) and oi_crash
                sflush = (short_liq[t, j] >= cfg.liq_z_thresh) and oi_crash

                if lflush:
                    if arm_side == 1:
                        f_lo, f_hi = min(f_lo, L[t, j]), max(f_hi, H[t, j])
                    else:
                        arm_side, f_lo, f_hi = 1, L[t, j], H[t, j]
                    expiry = t + cfg.flush_confirm_bars
                    continue
                if sflush:
                    if arm_side == -1:
                        f_lo, f_hi = min(f_lo, L[t, j]), max(f_hi, H[t, j])
                    else:
                        arm_side, f_lo, f_hi = -1, L[t, j], H[t, j]
                    expiry = t + cfg.flush_confirm_bars
                    continue

                if arm_side == 0 or not base_ok[t, j]:
                    continue
                mid = 0.5 * (f_lo + f_hi)
                a = atr[t, j]
                if arm_side == 1:
                    # longs were flushed -> we buy the exhaustion reclaim
                    if C[t, j] > mid and (hl3[t, j] >= 2.0 / 3.0):
                        s_px = f_lo - cfg.flush_stop_buf_atr * a
                        r = C[t, j] - s_px
                        if cfg.flush_min_r_atr * a <= r <= cfg.flush_max_r_atr * a:
                            side[t, j], stop[t, j], setup[t, j] = 1, s_px, SETUP_LIQ
                            arm_side = 0
                else:
                    if C[t, j] < mid and (lh3[t, j] >= 2.0 / 3.0):
                        s_px = f_hi + cfg.flush_stop_buf_atr * a
                        r = s_px - C[t, j]
                        if cfg.flush_min_r_atr * a <= r <= cfg.flush_max_r_atr * a:
                            side[t, j], stop[t, j], setup[t, j] = -1, s_px, SETUP_FUND * 0 + SETUP_LIQ
                            arm_side = 0

        # ---------- setup 2: lead-lag spillover (vectorised) ----------
        lead_z, lag_ratio = F["lead_z"], F["lag_ratio"]
        is_hb = np.array([(s.upper() in hb) and (s.upper() not in lead_set)
                          for s in p.symbols], dtype=bool)[None, :]
        ll_base = base_ok & is_hb & (F["beta"] >= cfg.ll_min_beta) & (setup == 0)
        up = ll_base & (lead_z >= cfg.ll_impulse_z) & (lag_ratio <= cfg.ll_lag_ratio_max)
        dn = ll_base & (lead_z <= -cfg.ll_impulse_z) & (lag_ratio <= cfg.ll_lag_ratio_max)
        ll_stop_up = C - cfg.ll_stop_atr * atr
        ll_stop_dn = C + cfg.ll_stop_atr * atr
        side = np.where(up & (side == 0), 1, side).astype(np.int8)
        stop = np.where(up & (setup == 0), ll_stop_up, stop)
        setup = np.where(up & (setup == 0), SETUP_LEADLAG, setup).astype(np.int8)
        side = np.where(dn & (side == 0), -1, side).astype(np.int8)
        stop = np.where(dn & (setup == 0), ll_stop_dn, stop)
        setup = np.where(dn & (setup == 0), SETUP_LEADLAG, setup).astype(np.int8)

        # ---------- setup 3: funding squeeze ----------
        ann = F["fund_ann"]
        hi_24 = _roll(H, BARS_PER_DAY, "max")
        lo_12 = _roll(L, BARS_PER_DAY // 2, "min")
        crowd_long = (base_ok & (setup == 0) & (ann >= cfg.fund_ann_long_crowd)
                      & (C < hi_24 * 0.995) & (F["cum_k"] < 0))
        crowd_short = (base_ok & (setup == 0) & (ann <= cfg.fund_ann_short_crowd)
                       & (C > lo_12 * 1.005) & (F["cum_k"] > 0))
        fs_stop_dn = np.maximum(hi_24, C + cfg.fund_stop_atr * atr)
        fs_stop_up = np.minimum(lo_12, C - cfg.fund_stop_atr * atr)
        side = np.where(crowd_long & (side == 0), -1, side).astype(np.int8)
        stop = np.where(crowd_long & (setup == 0), fs_stop_dn, stop)
        setup = np.where(crowd_long & (setup == 0), SETUP_FUND, setup).astype(np.int8)
        side = np.where(crowd_short & (side == 0), 1, side).astype(np.int8)
        stop = np.where(crowd_short & (setup == 0), fs_stop_up, stop)
        setup = np.where(crowd_short & (setup == 0), SETUP_FUND, setup).astype(np.int8)

        bad = ~np.isfinite(stop)
        side[bad] = 0
        setup[bad] = 0
        return side, stop, setup


# ===========================================================================
# 5. META-LABEL MODEL (numpy logistic, zero external deps, deterministic)
# ===========================================================================
FEATURE_KEYS = ("resid_z", "rv_ratio", "illiq_pct", "beta", "fund_ann",
                "oi_1h", "oi_1d", "long_liq", "short_liq", "lead_z",
                "lag_ratio", "xs_mom")


class MetaModel:
    def __init__(self, cfg: R8Config):
        self.cfg = cfg
        self.w: Optional[np.ndarray] = None
        self.b = 0.0
        self.mu = self.sd = None
        self.thresh = 0.5
        self.auc = 0.5
        self.n_train = 0

    @staticmethod
    def _sig(x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -35, 35)))

    def fit(self, X, y, r) -> "MetaModel":
        cfg = self.cfg
        self.n_train = len(y)
        if self.n_train < cfg.meta_min_train or len(np.unique(y)) < 2:
            self.w = None
            return self
        self.mu = X.mean(axis=0)
        self.sd = np.maximum(X.std(axis=0), 1e-9)
        Z = (X - self.mu) / self.sd
        n, k = Z.shape
        w, b = np.zeros(k), 0.0
        npos = max(float(y.sum()), 1.0)
        nneg = max(float(len(y) - y.sum()), 1.0)
        pw = np.where(y > 0, len(y) / (2 * npos), len(y) / (2 * nneg))
        for _ in range(cfg.meta_iters):
            g = (self._sig(Z @ w + b) - y) * pw
            w -= cfg.meta_lr * (Z.T @ g / n + cfg.meta_l2 * w / n)
            b -= cfg.meta_lr * g.mean()
        self.w, self.b = w, b
        p_in = self.predict(X)
        self.auc = _auc(y, p_in)
        best, best_e = cfg.meta_prob_floor, -1e9
        for q in np.arange(0.30, 0.86, 0.02):
            m = p_in >= q
            if m.sum() < max(12, 0.20 * len(p_in)):
                continue
            e = float(r[m].mean())
            if e > best_e:
                best_e, best = e, float(q)
        self.thresh = max(best, cfg.meta_prob_floor)
        return self

    def predict(self, X):
        if self.w is None:
            return np.full(len(X), 1.0)
        return self._sig(((X - self.mu) / self.sd) @ self.w + self.b)

    def accept(self, x) -> bool:
        if self.w is None:
            return True
        return bool(self.predict(x.reshape(1, -1))[0] >= self.thresh)


def _auc(y, p) -> float:
    pos, neg = p[y > 0], p[y <= 0]
    if len(pos) == 0 or len(neg) == 0:
        return 0.5
    r = pd.Series(np.concatenate([pos, neg])).rank().to_numpy()
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0)
                 / (len(pos) * len(neg)))


# ===========================================================================
# 6. ENGINE
# ===========================================================================
class ConvexHybridEngine:
    """Round 8 convex liquidation / lead-lag / funding-squeeze hybrid."""

    def __init__(self, mode: str = "compliant",
                 cfg: R8Config = R8Config(),
                 risk: Optional[RiskConfig] = None):
        self.cfg = cfg
        self.mode = mode
        if risk is not None:
            self.risk = risk
        elif mode == "institutional":
            self.risk = RiskConfig(base_risk=100.0, house_money_risk=150.0,
                                   drawdown_defense_risk=50.0,
                                   drawdown_limit=0.060, kelly_frac=0.50)
        else:
            self.risk = RiskConfig()
        self.feat = FeatureFactory(cfg)
        self.det = SetupDetector(cfg)

    # -- per-setup geometry -------------------------------------------------
    def _geometry(self, setup: int) -> Tuple[float, int]:
        c = self.cfg
        if setup == SETUP_LIQ:
            return c.liq_take_profit_r, c.liq_hold_max_bars
        if setup == SETUP_LEADLAG:
            return c.ll_take_profit_r, c.ll_hold_max_bars
        return c.fund_take_profit_r, c.fund_hold_max_bars

    # ------------------------------------------------------------------
    # 6a. purged triple-barrier labelling (train only)
    # ------------------------------------------------------------------
    def _label_events(self, p: Panel, F, side, stop_a, setup,
                      max_per_sym: int = 3000):
        cfg = self.cfg
        O, H, L, C = p.open, p.high, p.low, p.close
        ev = F["fund_event"]
        feats, ys, rs = [], [], []
        warm = max(cfg.beta_window, cfg.zscore_window) + 5

        for j in range(p.N):
            ts = np.nonzero(side[warm:p.T - 2, j] != 0)[0] + warm
            if len(ts) == 0:
                continue
            if len(ts) > max_per_sym:
                ts = ts[np.linspace(0, len(ts) - 1, max_per_sym).astype(int)]
            last_close = -10 ** 9
            for t in ts:
                if t <= last_close:
                    continue
                s = int(side[t, j])
                nxt = t + 1
                if not p.valid[nxt, j]:
                    continue
                entry = O[nxt, j] * (1.0 + cfg.entry_slippage * s)
                R = abs(entry - stop_a[t, j])
                if not np.isfinite(R) or R <= 0:
                    continue
                tp_r, hmax = self._geometry(int(setup[t, j]))
                stop_px = entry - s * R
                tp_px = entry + s * tp_r * R
                end = min(nxt + hmax, p.T - 1)
                exit_px, k, fp = C[end, j], end, 0.0
                for u in range(nxt, end + 1):
                    if not p.valid[u, j]:
                        continue
                    fp += -s * ev[u, j] * entry
                    if (s == 1 and L[u, j] <= stop_px) or (s == -1 and H[u, j] >= stop_px):
                        exit_px, k = stop_px, u
                        break
                    if (s == 1 and H[u, j] >= tp_px) or (s == -1 and L[u, j] <= tp_px):
                        exit_px, k = tp_px, u
                        break
                fill = exit_px * (1.0 - cfg.exit_slippage * s)
                gross = s * (fill - entry) + fp
                fee = cfg.taker_fee * (entry + abs(fill))
                net_r = (gross - fee) / R
                x = np.array([F[key][t, j] for key in FEATURE_KEYS]
                             + [float(s), float(setup[t, j])])
                if not np.all(np.isfinite(x)):
                    continue
                feats.append(x)
                rs.append(net_r)
                ys.append(1.0 if net_r > 0 else 0.0)
                last_close = k
        if not feats:
            return (np.zeros((0, len(FEATURE_KEYS) + 2)), np.zeros(0), np.zeros(0))
        return np.asarray(feats), np.asarray(ys), np.asarray(rs)

    # ------------------------------------------------------------------
    # 6b. purged gate (fit on TRAIN window only, 72h purge)
    # ------------------------------------------------------------------
    def fit_gate(self, panel: Panel, funding, oi, train_start, train_end):
        cfg = self.cfg
        tr = panel.slice(train_start, train_end - pd.Timedelta(hours=cfg.purge_hours))
        need = max(cfg.beta_window, cfg.zscore_window) + BARS_PER_DAY * 5
        if tr.T < need:
            return False, MetaModel(cfg), {"deploy": False, "reason": "insufficient_train",
                                           "n_events": 0}
        F = self.feat.build(tr, funding, oi)
        side, stop_a, setup = self.det.detect(tr, F)
        X, y, r = self._label_events(tr, F, side, stop_a, setup)
        n = len(y)
        if n < cfg.gate_min_events:
            return False, MetaModel(cfg), {"deploy": False, "n_events": n,
                                           "reason": "starvation"}
        meta = MetaModel(cfg).fit(X, y, r)
        p_in = meta.predict(X)
        sel = p_in >= meta.thresh
        exp_r = float(r[sel].mean()) if sel.sum() else float(r.mean())
        wr = float((y[sel] > 0).mean() * 100.0) if sel.sum() else 0.0
        ok = (n >= cfg.gate_min_events and exp_r >= cfg.gate_min_exp_r
              and meta.auc >= cfg.gate_min_auc)
        info = {"deploy": ok, "n_events": n, "n_selected": int(sel.sum()),
                "exp_r": round(exp_r, 4), "raw_exp_r": round(float(r.mean()), 4),
                "train_auc": round(meta.auc, 4), "meta_thresh": round(meta.thresh, 3),
                "train_win_rate": round(wr, 2),
                "setup_mix": {SETUP_NAME[k]: int((X[:, -1] == k).sum())
                              for k in (1, 2, 3)},
                "reason": "ok" if ok else ("starvation" if n < cfg.gate_min_events
                                           else "no_auc" if meta.auc < cfg.gate_min_auc
                                           else "no_edge")}
        return ok, meta, info

    # ------------------------------------------------------------------
    # 6c. OOS execution
    # ------------------------------------------------------------------
    def run_window(self, per_symbol: Dict[str, pd.DataFrame],
                   funding=None, basis=None, oi=None,
                   win_start: str = "", win_end: str = "",
                   window_id: str = "W00",
                   panel: Optional[Panel] = None) -> Dict:
        cfg, rk = self.cfg, self.risk
        full = panel if panel is not None else Panel(per_symbol)
        ws = pd.Timestamp(win_start)
        we = pd.Timestamp(win_end) + pd.Timedelta(days=1)
        train_end = ws - pd.Timedelta(hours=cfg.purge_hours)
        train_start = train_end - pd.Timedelta(days=cfg.train_days)

        ok, meta, gate = self.fit_gate(full, funding, oi, train_start, train_end)
        base = {"window_id": window_id, "gate": gate, "deploy": ok, "trades": 0,
                "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0,
                "avg_r": 0.0, "net_pnl": 0.0, "equity": rk.initial_capital,
                "halted": False, "trades_list": [], "equity_curve": [],
                "setup_mix": {}, "reason": f"gate_{gate.get('reason')}"}
        if not ok and not cfg.gate_soft:
            return base
        if not ok:
            meta = MetaModel(cfg)          # ungated fallback: trade raw setups

        warm_bars = max(cfg.beta_window, cfg.zscore_window, cfg.rv_slow) + BARS_PER_DAY
        p = full.slice(ws - pd.Timedelta(minutes=15 * warm_bars), we)
        if p.T < warm_bars // 2:
            base["reason"] = "no_test_data"
            return base
        t0 = int(p.index.searchsorted(ws, side="left"))
        if p.T - t0 < 50:
            base["reason"] = "no_test_data"
            return base

        F = self.feat.build(p, funding, oi)
        side_m, stop_m, setup_m = self.det.detect(p, F)
        atr, ev = F["atr"], F["fund_event"]
        O, H, L, C = p.open, p.high, p.low, p.close

        equity = rk.initial_capital            # REALISED equity (cash)
        peak = equity
        max_dd = 0.0
        principal_floor = rk.initial_capital * (1.0 - rk.principal_floor_frac)
        positions: List[Position] = []
        trades: List[Dict] = []
        curve: List[Tuple[pd.Timestamp, float]] = []
        cooldown = np.full(p.N, -10 ** 9, dtype=np.int64)
        halted = False

        def mtm(t: int, worst: bool) -> float:
            eq = equity
            for q in positions:
                px = (L[t, q.col] if q.side == 1 else H[t, q.col]) if worst else C[t, q.col]
                if not np.isfinite(px):
                    px = q.entry_px
                eq += q.open_pnl(px)
            return eq

        def close_position(q: Position, t: int, px: float, why: str):
            nonlocal equity
            fill = px * (1.0 - cfg.exit_slippage * q.side)
            q.fees_paid += cfg.taker_fee * abs(fill) * q.qty   # exit taker fee
            pnl = q.open_pnl(fill)          # already net of ALL fees + funding
            equity += pnl
            trades.append({
                "window_id": window_id, "sym": q.symbol, "side": q.side,
                "setup": SETUP_NAME[q.setup],
                "entry_ts": p.index[q.entry_bar], "exit_ts": p.index[t],
                "entry_px": round(q.entry_px, 8), "exit_px": round(fill, 8),
                "qty": q.qty, "r_px": q.r_px, "risk_d": round(q.risk_d, 2),
                "r_multiple": round(pnl / max(q.risk_d, 1e-9), 4),
                "pnl_d": round(pnl, 4), "fees_d": round(q.fees_paid, 4),
                "funding_d": round(q.funding_pnl, 4),
                "bars_held": t - q.entry_bar, "adds": q.adds,
                "why": why, "mfe_r": round(q.mfe_r, 3),
            })
            cooldown[q.col] = t + cfg.cooldown_bars

        # ------------------------- main bar loop -------------------------
        for t in range(t0, p.T):
            # (1) event-time funding accrual on OPEN positions
            for q in positions:
                if ev[t, q.col] != 0.0 and p.valid[t, q.col]:
                    q.funding_pnl += -q.side * ev[t, q.col] * C[t, q.col] * q.qty

            # (2) HARD intrabar drawdown kill-switch, checked BEFORE anything
            eq_worst = mtm(t, worst=True)
            if peak > 0 and (peak - eq_worst) / peak >= rk.drawdown_limit and positions:
                for q in list(positions):
                    px = C[t, q.col] if np.isfinite(C[t, q.col]) else q.entry_px
                    close_position(q, t, px, "dd_killswitch")
                positions.clear()
                halted = True

            # (3) exits / ratchets
            for q in list(positions):
                j = q.col
                if not p.valid[t, j]:
                    continue
                h_, l_, c_ = H[t, j], L[t, j], C[t, j]
                held = t - q.entry_bar
                fav = (h_ - q.entry_px) if q.side == 1 else (q.entry_px - l_)
                q.mfe_r = max(q.mfe_r, fav / q.r_px)
                exit_px, why = None, ""

                # pessimistic intrabar ordering: stop is always checked first
                if (q.side == 1 and l_ <= q.stop_px) or (q.side == -1 and h_ >= q.stop_px):
                    exit_px, why = q.stop_px, ("stop" if q.tier == 0 else "ratchet")
                else:
                    tp = q.entry_px + q.side * q.tp_r * q.r_px
                    if (q.side == 1 and h_ >= tp) or (q.side == -1 and l_ <= tp):
                        exit_px, why = tp, "take_profit"
                    elif held >= q.hold_max:
                        exit_px, why = c_, "time"

                if exit_px is not None:
                    close_position(q, t, exit_px, why)
                    positions.remove(q)
                    continue

                for tier_i, (trig, lock) in enumerate(cfg.ratchet_tiers, start=1):
                    if q.tier < tier_i and q.mfe_r >= trig:
                        new_stop = q.entry_px + q.side * lock * q.r_px
                        q.stop_px = (max(q.stop_px, new_stop) if q.side == 1
                                     else min(q.stop_px, new_stop))
                        q.tier = tier_i
                if q.tier >= len(cfg.ratchet_tiers):
                    trail = (h_ - cfg.trail_atr_mult * atr[t, j]) if q.side == 1 \
                        else (l_ + cfg.trail_atr_mult * atr[t, j])
                    q.stop_px = (max(q.stop_px, trail) if q.side == 1
                                 else min(q.stop_px, trail))

                # (3b) PYRAMID -- only once stop >= breakeven, funded by open profit
                if (rk.pyramid_enabled and q.adds < rk.pyramid_max_adds
                        and q.tier >= 1 and q.mfe_r >= rk.pyramid_trigger_r
                        and t + 1 < p.T and p.valid[t + 1, j] and held >= 1):
                    beyond_be = (q.stop_px - q.entry_px) * q.side >= 0.0
                    if beyond_be:
                        add_px = O[t + 1, j] * (1.0 + cfg.entry_slippage * q.side)
                        if np.isfinite(add_px) and add_px > 0:
                            add_qty = rk.pyramid_frac * q.legs[0][1]
                            # fee accrues into the position (netted via open_pnl)
                            q.fees_paid += cfg.taker_fee * add_px * add_qty
                            q.legs.append((add_px, add_qty))
                            q.adds += 1

            # (4) mark-to-market equity / peak / drawdown, bar-by-bar
            eq_now = mtm(t, worst=False)
            eq_low = mtm(t, worst=True)
            peak = max(peak, eq_now)
            if peak > 0:
                max_dd = max(max_dd, (peak - eq_low) / peak)
            curve.append((p.index[t], eq_now))
            if halted:
                break

            # (5) entries -> filled at OPEN of t+1
            if t >= p.T - 1 or len(positions) >= cfg.max_positions:
                continue
            held_cols = {q.col for q in positions}
            cands = []
            for j in range(p.N):
                if side_m[t, j] == 0 or j in held_cols or t < cooldown[j]:
                    continue
                if not (p.valid[t, j] and p.valid[t + 1, j]):
                    continue
                x = np.array([F[k_][t, j] for k_ in FEATURE_KEYS]
                             + [float(side_m[t, j]), float(setup_m[t, j])])
                if not np.all(np.isfinite(x)) or not meta.accept(x):
                    continue
                prob = float(meta.predict(x.reshape(1, -1))[0])
                # convexity preference: liquidation exhausts first
                prio = 2 if setup_m[t, j] == SETUP_LIQ else (1 if setup_m[t, j] == SETUP_FUND else 0)
                cands.append((prio, prob, j))
            cands.sort(key=lambda v: (-v[0], -v[1]))

            for _, _, j in cands[:cfg.top_k_per_bar]:
                if len(positions) >= cfg.max_positions:
                    break
                s = int(side_m[t, j])
                entry = O[t + 1, j] * (1.0 + cfg.entry_slippage * s)
                if not np.isfinite(entry) or entry <= 0:
                    continue
                R = abs(entry - stop_m[t, j])
                if not np.isfinite(R) or R <= 1e-12:
                    continue
                # ---------- FRICTION VIABILITY FILTER ----------
                friction_px = entry * (2.0 * cfg.taker_fee
                                       + cfg.entry_slippage + cfg.exit_slippage)
                if friction_px > cfg.max_friction_r * R:
                    continue

                # ---------- NON-LINEAR KELLY / HOUSE-MONEY SIZING ----------
                banked = equity - rk.initial_capital
                dd_now = (peak - eq_now) / peak if peak > 0 else 0.0
                if dd_now > rk.dd_defense_trigger:
                    risk_d = rk.drawdown_defense_risk
                elif banked > rk.house_money_trigger:
                    risk_d = max(rk.house_money_risk,
                                 rk.base_risk + rk.kelly_frac * banked)
                else:
                    risk_d = rk.base_risk
                risk_d = min(risk_d, rk.max_risk_per_trade)
                # PRINCIPAL DEFENCE: worst case on this trade + open risk of the
                # book may never take realised equity below the floor.
                open_risk = sum(abs(q.stop_px - q.entry_px) * q.qty
                                for q in positions)
                headroom = max(equity - open_risk - principal_floor, 0.0)
                risk_d = min(risk_d, headroom)
                if risk_d <= 1e-6:
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

                tp_r, hmax = self._geometry(int(setup_m[t, j]))
                fee = cfg.taker_fee * entry * qty   # netted via Position.open_pnl
                positions.append(Position(
                    symbol=p.symbols[j], col=j, side=s, setup=int(setup_m[t, j]),
                    r_px=R, stop_px=entry - s * R, entry_bar=t + 1,
                    tp_r=tp_r, hold_max=hmax, legs=[(entry, qty)],
                    fees_paid=fee, risk_d=qty * R))   # actual $ at risk post-caps

        # ---------------- force-flat at window end ----------------
        if positions:
            t_end = p.T - 1
            for q in list(positions):
                px = C[t_end, q.col] if np.isfinite(C[t_end, q.col]) else q.entry_px
                close_position(q, t_end, px, "window_end")
            positions.clear()
            peak = max(peak, equity)
            if peak > 0:
                max_dd = max(max_dd, (peak - equity) / peak)
            curve.append((p.index[t_end], equity))

        net = equity - rk.initial_capital
        wins = sum(1 for x in trades if x["pnl_d"] > 0)
        rs = np.array([x["r_multiple"] for x in trades]) if trades else np.zeros(0)
        gw = sum(x["pnl_d"] for x in trades if x["pnl_d"] > 0)
        gl = -sum(x["pnl_d"] for x in trades if x["pnl_d"] <= 0)
        mix: Dict[str, int] = {}
        for x in trades:
            mix[x["setup"]] = mix.get(x["setup"], 0) + 1

        return {
            "window_id": window_id, "deploy": True, "gate": gate, "halted": halted,
            "equity": round(equity, 2), "net_pnl": round(net, 2),
            "roi_pct": round(net / rk.initial_capital * 100.0, 4),
            "max_dd_pct": round(max_dd * 100.0, 4),
            "trades": len(trades),
            "win_rate_pct": round(wins / len(trades) * 100.0, 2) if trades else 0.0,
            "avg_r": round(float(rs.mean()), 4) if len(rs) else 0.0,
            "max_r": round(float(rs.max()), 4) if len(rs) else 0.0,
            "expectancy_d": round(net / len(trades), 4) if trades else 0.0,
            "profit_factor": round(gw / gl, 3) if gl > 0 else float("inf"),
            "total_fees_d": round(sum(x["fees_d"] for x in trades), 4),
            "total_funding_d": round(sum(x["funding_d"] for x in trades), 4),
            "setup_mix": mix, "equity_curve": curve, "trades_list": trades,
            "reason": "ok",
        }

    # ------------------------------------------------------------------
    # 6d. scorecard + fail-fast walk-forward driver
    # ------------------------------------------------------------------
    @staticmethod
    def score(r: Dict) -> Dict:
        crit = {
            "roi": r["roi_pct"] > 20.0,
            "dd": r["max_dd_pct"] < 5.0,
            "wr": r["win_rate_pct"] > 40.0,
            "trades": r["trades"] >= 6,
            "avg_r": r["avg_r"] >= 2.5,
        }
        return {"pass": all(crit.values()),
                "failed": [k for k, v in crit.items() if not v], **crit}

    def run_walkforward(self, per_symbol: Dict[str, pd.DataFrame],
                        windows: Sequence[Tuple[str, str]],
                        funding=None, basis=None, oi=None,
                        fail_fast: bool = True) -> pd.DataFrame:
        panel = Panel(per_symbol)
        rows = []
        for i, (a, b) in enumerate(windows, start=1):
            r = self.run_window(per_symbol, funding, basis, oi, a, b,
                                window_id=f"W{i:02d}", panel=panel)
            sc = self.score(r)
            rows.append({
                "window_id": r["window_id"], "start": a, "end": b,
                "deploy": r["deploy"], "trades": r["trades"],
                "roi_pct": r["roi_pct"], "max_dd_pct": r["max_dd_pct"],
                "win_rate_pct": r["win_rate_pct"], "avg_r": r["avg_r"],
                "max_r": r.get("max_r", 0.0),
                "profit_factor": r.get("profit_factor", 0.0),
                "halted": r["halted"], "setup_mix": r.get("setup_mix", {}),
                "gate_reason": r["gate"].get("reason"),
                "gate_exp_r": r["gate"].get("exp_r"),
                "gate_auc": r["gate"].get("train_auc"),
                "gate_n": r["gate"].get("n_events"),
                "PASS": sc["pass"], "failed_criteria": ",".join(sc["failed"]),
            })
            if fail_fast and not sc["pass"]:
                break
        return pd.DataFrame(rows)


# Backwards-compatible alias so an existing runner importing the R7 name works.
ResidualDislocationEngine = ConvexHybridEngine


# ===========================================================================
# 7. SELF-TEST (synthetic panel with injected liquidation cascades)
# ===========================================================================
def _synth_panel(symbols: List[str], start: str, periods: int, seed: int = 11):
    rs = np.random.default_rng(seed)
    idx = pd.date_range(start, periods=periods, freq="15min")
    mkt = rs.normal(0, 0.0016, periods)
    # inject 40 cascade shocks into the market leg
    shock_t = rs.choice(np.arange(200, periods - 200), size=40, replace=False)
    for st in shock_t:
        sgn = -1.0 if rs.random() < 0.65 else 1.0
        mkt[st:st + 3] += sgn * rs.uniform(0.012, 0.035)
        mkt[st + 3:st + 14] -= sgn * rs.uniform(0.004, 0.016) / 11.0
    mkt_c = mkt.cumsum()
    per_symbol, funding, oi = {}, {}, {}
    for s in symbols:
        beta = 0.7 + 1.1 * rs.random()
        e = np.zeros(periods)
        idio = rs.normal(0, 0.0022, periods)
        for i in range(1, periods):
            e[i] = 0.985 * e[i - 1] + idio[i]
        c = np.exp(math.log(10 + 90 * rs.random()) + beta * mkt_c + e)
        rng_ = np.abs(rs.normal(0, 0.0020, periods)) * c
        o = np.concatenate([[c[0]], c[:-1]])
        h = np.maximum(o, c) + rng_
        l = np.minimum(o, c) - rng_
        v = rs.lognormal(11, 0.5, periods)
        oi_s = rs.lognormal(15, 0.05, periods)
        for st in shock_t:                        # OI destruction at the cascade
            v[st:st + 3] *= rs.uniform(4, 12)
            oi_s[st + 1:] *= rs.uniform(0.80, 0.90)
        per_symbol[s] = pd.DataFrame({"open": o, "high": h, "low": l,
                                      "close": c, "volume": v}, index=idx)
        oi[s] = pd.Series(oi_s, index=idx)
        f_idx = pd.date_range(idx[0].normalize(), idx[-1], freq="8h")
        funding[s] = pd.Series(rs.normal(0.0001, 0.00030, len(f_idx)), index=f_idx)
    return per_symbol, funding, oi


if __name__ == "__main__":
    SYMS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT", "DOGEUSDT",
            "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT", "SUIUSDT", "NEARUSDT",
            "DOTUSDT", "LTCUSDT", "BCHUSDT", "APTUSDT", "OPUSDT", "ARBUSDT"]
    px, fund, oi_ = _synth_panel(SYMS, "2024-01-01", 96 * 300)
    eng = ConvexHybridEngine(mode="compliant")
    wins = [("2024-08-01", "2024-08-31"), ("2024-09-01", "2024-09-30"),
            ("2024-10-01", "2024-10-31")]
    res = eng.run_walkforward(px, wins, funding=fund, oi=oi_, fail_fast=False)
    pd.set_option("display.width", 240, "display.max_columns", 60)
    print(res[["window_id", "deploy", "trades", "roi_pct", "max_dd_pct",
               "win_rate_pct", "avg_r", "max_r", "halted", "setup_mix",
               "gate_reason", "gate_auc", "gate_n", "PASS", "failed_criteria"]])
