    # OPUS 5 — ROUND 7 ARCHITECT DIRECTIVE: EXPANDING HORIZONS

    ## 1. Context & Feedback on Your Round 7 ResidualDislocationEngine
    Opus 5, we received your thorough audit, your dissection of the 8 harness defects in Round 6, and your drop-in ResidualDislocationEngine (v7.0).

    We immediately executed the engine on the verification harness. The results confirmed your instrumentation:
    - **Intrabar Kill-Switch**: Verified. W01 tripped the hard drawdown stop at 4.4991% and halted immediately.
    - **Microstructure Ratchet & Causal ATR**: Verified. 1R was confirmed at ~358 bps (Wilder daily ATR), eliminating the friction destruction where 33 bps had been eating 1.2R. Slippage and maker/taker fees accrued exactly as specified.
    - **Event-Time Funding**: Verified. Accrual occurred strictly at discrete settlement bars rather than bar-by-bar ffill overcounts.
    - **Gate Performance**: Purged numpy logistic meta-labeling trained with zero lookahead, achieving train AUC 0.57–0.63.

    Empirical verification baseline on the synthetic test panel:
    ```
    window_id  deploy  trades  roi_pct  max_dd_pct  win_rate_pct   avg_r  profit_factor  halted gate_reason
    0       W01    True      19  -4.4812      4.4991         10.53 -0.5119          0.096    True          ok
    1       W02    True     127  -1.4486      4.1395         59.06  0.0181          0.982   False          ok
    2       W03    True     102  -1.3169      3.4782         50.98  0.0310          1.014   False          ok
    ```

    ---

    ## 2. The Mandate & The Pushback on Target Criteria
    We noted your core mathematical critique regarding our target criteria:
    > "Your acceptance criteria are the real defect. +20% ROI/month at <5% max DD from >=6 trades, at $25 base risk on $5,000, means +$1,000/month = 40R net from ~6–20 trades (averaging +2R to +6.6R net per trade). No institutional book on earth runs that... Renegotiate to 2–4% per month at <5% DD, profit factor > 1.25, >=30 trades/window."

    We understand your mathematical reality check: linear cross-sectional mean reversion with symmetric stops and fixed $25 risk cannot sustainably generate 40R/month under 33 bps round-trip frictions without overfitting.

    **However, the challenge from the trading desk remains: EXPAND YOUR HORIZONS.**

    We cannot simply accept 2% per month or declare defeat against double-digit targets. If standard linear reversion, classical carry, and retail SMC cannot produce the required convexity, what **extreme, non-linear, structural quantitative paradigm** CAN?

    ---

    ## 3. The Challenge: Extreme New Paradigms for Convex Edge
    We need you to explore and engineer strategies that fundamentally exploit crypto-market microstructure anomalies with true non-linear payoff structures:

    1. **Forced Liquidation Cascades / Price-Insensitive Unwinds**:
    - During cascading liquidations, counterparties are forced market order dumpers with zero price elasticity.
    - Instead of catching falling knives or standard reversion, how do we systematically enter *with* the cascade or catch the exact structural exhaust point where open interest collapses by >10-15% in a 1-hour window, capturing asymmetric 5R–10R explosive snapbacks?

    2. **Lead-Lag Cross-Asset Microstructure / Eigen-Dislocations**:
    - In the 18 Binance USDT-M perps (BTC, ETH, SOL, XRP, DOGE, etc.), high-beta alts lag BTC/ETH orderflow bursts by 1 to 4 bars (15m to 60m).
    - Can we exploit high-frequency orderflow / volume impulse spillover from BTC/ETH into delayed alt perps?

    3. **Dynamic Asymmetric Sizing & Volatility Regimes**:
    - Fixed $25 base risk is linear. What if sizing scales non-linearly with signal conviction (e.g., fractional Kelly conditioned on extreme funding + liquidation z-score > 2.5), using aggressive profit-pyramiding on free-rolling "house money"?

    4. **Funding Basis Convexity & Dislocation Squeezes**:
    - In extreme structural imbalances where annualized funding hits 100%+ or deep negative rates, short/long squeezes are mathematically guaranteed to unwind violently. How do we structure a convexity capture engine that feeds on these regime dislocations?

    ---

    ## 4. Required Deliverable
    Do not provide generic advice, high-level theory, or retail indicators (no MACD/RSI).

    We need you to:
    1. **Formulate the Mathematical Paradigm**: Specify the exact quantitative thesis and equations that offer the structural asymmetry needed for high ROI under tight drawdown.
    2. **Provide the Full Drop-In Python Implementation**:
    - Single standalone script, fully runnable with zero missing imports (numpy/pandas only, no sklearn).
    - Must adhere to the settled institutional constraints:
        - 18 Binance USDT-M perpetuals.
        - 33 bps frictions (8 bps fee, 10 bps entry slippage, 15 bps exit slippage).
        - Intrabar 4.5% hard drawdown kill-switch.
        - Bar-by-bar next-open execution.
        - Fully causal feature engineering (no lookahead).

    ---

    ## 5. FULL UNABRIDGED SOURCE CODE (CURRENT ENGINE v7.0)
    ```python
    """
    RP2 / ROUND 7 -- CROSS-SECTIONAL RESIDUAL-DISLOCATION ENGINE (v7.0)
    Drop-in replacement for FundingBasisCarryEngine.

    Architecture
    Alpha : beta-neutral residual dislocation vs. an equal-weight universe index, vol-normalised, cross-sectionally ranked each bar.
    Overlays: event-time funding carry tilt, OI-impulse, Amihud illiquidity penalty, realised-vol regime filter.
    Meta-overlay : purged triple-barrier meta-labeling. A numpy logistic model (no sklearn dependency) is fit ONLY on the purged training window and gates every live signal on E[R] > 0 post-friction.
    Execution : bar-by-bar, next-bar-open fills, single-count slippage, exact maker/taker notional fees, event-time funding accrual, true causal Wilder daily ATR, multi-tier ratchet, intrabar mark-to-market equity + hard drawdown kill-switch.
    """

    from __future__ import annotations

    import math
    from dataclasses import dataclass, field
    from typing import Dict, List, Optional, Tuple

    import numpy as np
    import pandas as pd

    BARS_PER_DAY = 96  # 15m bars
    BARS_PER_HOUR = 4

    # ===========================================================================
    # 0. CONFIG
    # ===========================================================================
    @dataclass
    class RiskConfig:
        initial_capital: float = 5000.0
        base_risk: float = 25.0
        house_money_risk: float = 50.0
        drawdown_defense_risk: float = 15.0
        drawdown_limit: float = 0.045  # hard kill-switch, intrabar
        dd_defense_trigger: float = 0.025
        house_money_trigger: float = 50.0
        max_gross_leverage: float = 5.0  # notional / equity cap, per book
        max_symbol_leverage: float = 2.0  # notional / equity cap, per name

    @dataclass(frozen=True)
    class R7Config:
        # ---- residual dislocation alpha ----
        beta_window: int = BARS_PER_DAY * 10  # rolling OLS beta lookback
        disloc_window: int = BARS_PER_DAY // 2  # 12h residual accumulation
        zscore_window: int = BARS_PER_DAY * 5  # residual-z normaliser
        entry_z: float = 1.8  # |z| gate on residual
        xs_rank_gate: float = 0.15  # trade top/bottom 15% only
        
        # ---- regime / quality filters ----
        rv_fast: int = BARS_PER_DAY  # 24h realised vol
        rv_slow: int = BARS_PER_DAY * 10  # 10d realised vol
        rv_ratio_max: float = 2.25  # kill entries in vol explosions
        rv_ratio_min: float = 0.55  # kill entries in dead tape
        illiq_window: int = BARS_PER_DAY * 5
        illiq_max_pctile: float = 0.85  # drop worst 15% Amihud names
        
        # ---- carry / flow overlays ----
        fund_z_window: int = 63  # 63 settlements = 21 days
        fund_tilt_w: float = 0.35  # weight of carry in composite
        oi_window: int = BARS_PER_DAY
        oi_tilt_w: float = 0.20
        disloc_w: float = 1.00
        
        # ---- position geometry (all in TRUE daily-ATR units) ----
        stop_atr_mult: float = 0.85
        atr_period: int = 14
        hold_max_bars: int = BARS_PER_DAY * 3
        hold_min_bars: int = 4
        ratchet_tiers: Tuple[Tuple[float, float], ...] = (
            (1.00, 0.10),  # at +1.00R -> stop to +0.10R
            (1.75, 0.85),  # at +1.75R -> stop to +0.85R
            (2.50, 1.60),  # at +2.50R -> stop to +1.60R
        )
        trail_atr_mult: float = 1.10  # after top tier, chandelier
        take_profit_r: float = 4.0
        exit_on_z_decay: float = 0.35  # residual mean-reverted
        
        # ---- frictions (exact) ----
        taker_fee: float = 0.0008  # 8 bps per side, on notional
        entry_slippage: float = 0.0010  # 10 bps, applied ONCE, in px
        exit_slippage: float = 0.0015  # 15 bps, applied ONCE, in px
        
        # ---- purged walk-forward gate ----
        train_days: int = 180
        purge_hours: int = 72
        gate_min_events: int = 40
        gate_min_exp_r: float = 0.04
        gate_min_auc: float = 0.53
        
        # ---- meta-labeling ----
        meta_l2: float = 1.0
        meta_iters: int = 400
        meta_lr: float = 0.35
        meta_min_train: int = 60
        meta_prob_floor: float = 0.50
        
        # ---- portfolio ----
        max_positions: int = 2  # spec: max 2 concurrent
        top_k_per_bar: int = 2
        cooldown_bars: int = BARS_PER_DAY // 4  # per-symbol re-entry cooldown

    @dataclass
    class Position:
        symbol: str
        col: int
        side: int
        entry_px: float
        qty: float
        r_px: float  # 1R in price units (stop distance)
        stop_px: float
        entry_bar: int
        atr_at_entry: float
        tier: int = 0
        funding_pnl: float = 0.0  # dollars, event-time accrual
        fees_paid: float = 0.0  # dollars
        mfe_r: float = 0.0

    # ===========================================================================
    # 1. PANEL ALIGNMENT (fixes positional-index misalignment)
    # ===========================================================================
    class Panel:
        """Timestamp-aligned OHLCV cube. NO forward-filling of prices: a symbol with a missing bar is simply untradeable on that bar (`valid` mask)."""

        __slots__ = ("index", "symbols", "open", "high", "low", "close",
                    "volume", "valid", "T", "N")

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

            def cube(col: str) -> np.ndarray:
                m = np.full((self.T, self.N), np.nan, dtype=np.float64)
                for j, s in enumerate(self.symbols):
                    d = clean[s]
                    if col in d.columns:
                        m[:, j] = d[col].reindex(self.index).to_numpy(dtype=np.float64)
                return m

            self.open = cube("open")
            self.high = cube("high")
            self.low = cube("low")
            self.close = cube("close")
            self.volume = cube("volume")
            if np.all(np.isnan(self.volume)):
                self.volume = np.ones_like(self.close)
            self.valid = (
                np.isfinite(self.open) & np.isfinite(self.high)
                & np.isfinite(self.low) & np.isfinite(self.close)
                & (self.close > 0)
            )

        def slice(self, start: pd.Timestamp, end: pd.Timestamp) -> "Panel":
            lo = int(self.index.searchsorted(start, side="left"))
            hi = int(self.index.searchsorted(end, side="right"))
            p = Panel.__new__(Panel)
            p.index = self.index[lo:hi]
            p.symbols = list(self.symbols)
            p.open, p.high = self.open[lo:hi], self.high[lo:hi]
            p.low, p.close = self.low[lo:hi], self.close[lo:hi]
            p.volume, p.valid = self.volume[lo:hi], self.valid[lo:hi]
            p.T, p.N = p.close.shape
            return p

    # ===========================================================================
    # 2. CAUSAL PRIMITIVES
    # ===========================================================================
    def _roll_mean(a: np.ndarray, w: int) -> np.ndarray:
        return pd.DataFrame(a).rolling(w, min_periods=max(2, w // 4)).mean().to_numpy()

    def _roll_std(a: np.ndarray, w: int) -> np.ndarray:
        return pd.DataFrame(a).rolling(w, min_periods=max(2, w // 4)).std(ddof=0).to_numpy()

    def _roll_sum(a: np.ndarray, w: int) -> np.ndarray:
        return pd.DataFrame(a).rolling(w, min_periods=max(2, w // 4)).sum().to_numpy()

    def causal_daily_atr(panel: Panel, period: int = 14) -> np.ndarray:
        """TRUE Wilder ATR on *daily* bars, shifted one day, mapped onto the 15m grid."""
        out = np.full((panel.T, panel.N), np.nan, dtype=np.float64)
        for j in range(panel.N):
            s = pd.DataFrame(
                {"high": panel.high[:, j], "low": panel.low[:, j], "close": panel.close[:, j]},
                index=panel.index
            ).dropna()
            if len(s) < BARS_PER_DAY * 3:
                continue
            d = s.resample("1D").agg(high=("high", "max"), low=("low", "min"), close=("close", "last")).dropna()
            if len(d) < 3:
                continue
            pc = d["close"].shift(1)
            tr = pd.concat([(d["high"] - d["low"]).abs(), (d["high"] - pc).abs(), (d["low"] - pc).abs()], axis=1).max(axis=1)
            atr = tr.ewm(alpha=1.0 / period, adjust=False, min_periods=min(period, len(tr))).mean()
            atr = atr.shift(1)  # <-- strictly causal
            out[:, j] = atr.reindex(panel.index, method="ffill").to_numpy()
        
        # last-resort floor: 1.2% of price, prevents zero-R division
        floor = 0.012 * panel.close
        out = np.where(np.isfinite(out) & (out > 0), out, floor)
        return np.maximum(out, 1e-12)

    def event_time_funding(panel: Panel, funding: Optional[Dict[str, pd.Series]], fz_window: int = 63) -> Tuple[np.ndarray, np.ndarray]:
        """Return (rate_at_settlement_bar, causal_funding_z)."""
        ev = np.zeros((panel.T, panel.N), dtype=np.float64)
        fz = np.zeros((panel.T, panel.N), dtype=np.float64)
        if not funding:
            return ev, fz
        for j, s in enumerate(panel.symbols):
            f = funding.get(s)
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
            pos, vals = pos[ok], f.to_numpy(dtype=np.float64)[ok]
            np.add.at(ev, (pos, np.full(pos.shape, j)), vals)

            roll = f.rolling(fz_window, min_periods=8)
            z_ev = (f - roll.mean()) / roll.std(ddof=0).replace(0, np.nan)
            z_ev = z_ev.clip(-4, 4).shift(1)  # only prior settlements
            fz[:, j] = (z_ev.reindex(panel.index, method="ffill")
                            .fillna(0.0).to_numpy())
        return ev, np.nan_to_num(fz)

    # ===========================================================================
    # 3. ALPHA FACTORY -- cross-sectional residual dislocation
    # ===========================================================================
    class AlphaFactory:
        """All features at row t are computable from information up to and including the CLOSE of bar t. Trading happens at open of t+1."""

        def __init__(self, cfg: R7Config):
            self.cfg = cfg

        def build(self, panel: Panel,
                funding: Optional[Dict[str, pd.Series]] = None,
                oi: Optional[Dict[str, pd.Series]] = None) -> Dict[str, np.ndarray]:
            cfg = self.cfg
            C = panel.close
            with np.errstate(divide="ignore", invalid="ignore"):
                ret = np.diff(np.log(np.where(C > 0, C, np.nan)), axis=0,
                            prepend=np.nan)
            ret = np.nan_to_num(ret, nan=0.0, posinf=0.0, neginf=0.0)

            # --- equal-weight universe index return (the "market" leg) ---
            vmask = panel.valid.astype(np.float64)
            denom = np.maximum(vmask.sum(axis=1, keepdims=True), 1.0)
            mkt = (ret * vmask).sum(axis=1, keepdims=True) / denom

            # --- rolling OLS beta of each name on the index (causal) ---
            w = cfg.beta_window
            cov = _roll_mean(ret * mkt, w) - _roll_mean(ret, w) * _roll_mean(mkt, w)
            var = np.maximum(_roll_mean(mkt * mkt, w) - _roll_mean(mkt, w) ** 2, 1e-18)
            beta = np.clip(np.nan_to_num(cov / var, nan=1.0), -3.0, 3.0)

            resid = ret - beta * mkt  # idiosyncratic
            disloc = _roll_sum(resid, cfg.disloc_window)  # accumulated
            mu = _roll_mean(disloc, cfg.zscore_window)
            sd = np.maximum(_roll_std(disloc, cfg.zscore_window), 1e-12)
            z = np.nan_to_num((disloc - mu) / sd)
            z = np.clip(z, -6.0, 6.0)

            # --- realised-vol regime ---
            rv_f = _roll_std(resid, cfg.rv_fast) * math.sqrt(BARS_PER_DAY)
            rv_s = _roll_std(resid, cfg.rv_slow) * math.sqrt(BARS_PER_DAY)
            rv_ratio = np.nan_to_num(rv_f / np.maximum(rv_s, 1e-12), nan=1.0)

            # --- Amihud illiquidity (|ret| / dollar volume), cross-sec pctile ---
            dv = np.maximum(panel.close * np.nan_to_num(panel.volume), 1.0)
            amihud = _roll_mean(np.abs(ret) / dv, cfg.illiq_window)
            illiq_pct = _xs_pctile(np.nan_to_num(amihud, nan=np.inf))

            # --- funding carry tilt (event-time, causal) ---
            fund_ev, fund_z = event_time_funding(panel, funding, cfg.fund_z_window)

            # --- open-interest impulse ---
            oi_imp = np.zeros_like(C)
            if oi:
                for j, s in enumerate(panel.symbols):
                    o = oi.get(s)
                    if o is None or len(o) == 0:
                        continue
                    o = o.copy()
                    o.index = pd.DatetimeIndex(pd.to_datetime(o.index))
                    o = o[~o.index.duplicated(keep="last")].sort_index()
                    o = o.reindex(panel.index.union(o.index)).ffill().reindex(panel.index)
                    v = o.to_numpy(dtype=np.float64)
                    prev = np.roll(v, cfg.oi_window)
                    prev[:cfg.oi_window] = np.nan
                    with np.errstate(invalid="ignore", divide="ignore"):
                        oi_imp[:, j] = np.nan_to_num(np.clip(v / prev - 1.0, -1, 1))

            # --- composite score: mean-reversion of residual + carry + flow ---
            # negative z  => name is cheap vs its beta-implied path => go LONG
            raw = (-cfg.disloc_w * z
                - cfg.fund_tilt_w * fund_z          # pay-to-be-long => short bias
                - cfg.oi_tilt_w * np.sign(z) * oi_imp)
            raw = np.where(panel.valid, raw, np.nan)
            xs_rank = _xs_pctile(raw)                  # 0..1, NaN-safe

            return {
                "ret": ret, "mkt": np.repeat(mkt, panel.N, axis=1), "beta": beta,
                "resid_z": z, "score": np.nan_to_num(raw), "xs_rank": xs_rank,
                "rv_ratio": rv_ratio, "illiq_pct": illiq_pct,
                "fund_event": fund_ev, "fund_z": fund_z, "oi_imp": oi_imp,
                "atr": causal_daily_atr(panel, cfg.atr_period),
            }

        def signals(self, panel: Panel, F: Dict[str, np.ndarray]) -> np.ndarray:
            """side matrix in {-1,0,+1}, valid at bar t, executable at t+1."""
            cfg = self.cfg
            z, rk = F["resid_z"], F["xs_rank"]
            regime = (F["rv_ratio"] <= cfg.rv_ratio_max) & (F["rv_ratio"] >= cfg.rv_ratio_min)
            liq = F["illiq_pct"] <= cfg.illiq_max_pctile
            base = panel.valid & regime & liq & np.isfinite(F["atr"])
            long_m = base & (z <= -cfg.entry_z) & (rk >= 1.0 - cfg.xs_rank_gate)
            short_m = base & (z >= cfg.entry_z) & (rk <= cfg.xs_rank_gate)
            side = np.zeros_like(z, dtype=np.int8)
            side[long_m] = 1
            side[short_m & ~long_m] = -1
            return side

    def _xs_pctile(a: np.ndarray) -> np.ndarray:
        """Row-wise cross-sectional percentile in [0,1], NaN -> 0.5."""
        out = np.full(a.shape, 0.5, dtype=np.float64)
        fin = np.isfinite(a)
        cnt = fin.sum(axis=1)
        for t in np.nonzero(cnt > 1)[0]:
            row, m = a[t], fin[t]
            r = pd.Series(row[m]).rank(pct=True).to_numpy()
            out[t, m] = r
        return out

    # ===========================================================================
    # 4. META-LABELING OVERLAY (numpy logistic regression, zero deps)
    # ===========================================================================
    class MetaModel:
        def __init__(self, cfg: R7Config):
            self.cfg = cfg
            self.w: Optional[np.ndarray] = None
            self.b: float = 0.0
            self.mu: Optional[np.ndarray] = None
            self.sd: Optional[np.ndarray] = None
            self.thresh: float = 0.5
            self.auc: float = 0.5
            self.n_train: int = 0

        @staticmethod
        def _sig(x: np.ndarray) -> np.ndarray:
            return 1.0 / (1.0 + np.exp(-np.clip(x, -35, 35)))

        def fit(self, X: np.ndarray, y: np.ndarray, r: np.ndarray) -> "MetaModel":
            cfg = self.cfg
            self.n_train = len(y)
            if self.n_train < cfg.meta_min_train or len(np.unique(y)) < 2:
                self.w = None
                return self
            self.mu = X.mean(axis=0)
            self.sd = np.maximum(X.std(axis=0), 1e-9)
            Z = (X - self.mu) / self.sd
            n, k = Z.shape
            w = np.zeros(k)
            b = 0.0
            # class-balanced gradient descent w/ L2
            pw = np.where(y > 0, (len(y) / max(2 * y.sum(), 1.0)),
                        (len(y) / max(2 * (len(y) - y.sum()), 1.0)))
            for _ in range(cfg.meta_iters):
                p = self._sig(Z @ w + b)
                g = (p - y) * pw
                gw = Z.T @ g / n + cfg.meta_l2 * w / n
                gb = g.mean()
                w -= cfg.meta_lr * gw
                b -= cfg.meta_lr * gb
            self.w, self.b = w, b
            p_in = self.predict(X)
            self.auc = _auc(y, p_in)
            # choose the probability cut that maximises in-train expected R,
            # subject to keeping >= 20% of the events (anti-overfit floor)
            best, best_e = cfg.meta_prob_floor, -1e9
            for q in np.arange(0.30, 0.86, 0.02):
                cut = float(q)
                m = p_in >= cut
                if m.sum() < max(15, 0.20 * len(p_in)):
                    continue
                e = float(r[m].mean())
                if e > best_e:
                    best_e, best = e, cut
            self.thresh = max(best, cfg.meta_prob_floor)
            return self

        def predict(self, X: np.ndarray) -> np.ndarray:
            if self.w is None:
                return np.full(len(X), 1.0)
            Z = (X - self.mu) / self.sd
            return self._sig(Z @ self.w + self.b)

        def accept(self, x: np.ndarray) -> bool:
            if self.w is None:
                return True
            return bool(self.predict(x.reshape(1, -1))[0] >= self.thresh)

    def _auc(y: np.ndarray, p: np.ndarray) -> float:
        pos, neg = p[y > 0], p[y <= 0]
        if len(pos) == 0 or len(neg) == 0:
            return 0.5
        r = pd.Series(np.concatenate([pos, neg])).rank().to_numpy()
        return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))

    # ===========================================================================
    # 5. ENGINE
    # ===========================================================================
    FEATURE_KEYS = ("resid_z", "score", "xs_rank", "rv_ratio", "fund_z", "oi_imp", "beta", "illiq_pct")

    class ResidualDislocationEngine:
        def __init__(self, mode: str = "compliant", cfg: R7Config = R7Config(), risk: Optional[RiskConfig] = None):
            self.cfg = cfg
            self.mode = mode
            if risk is not None:
                self.risk = risk
            elif mode == "institutional":
                self.risk = RiskConfig(base_risk=100.0, house_money_risk=150.0, drawdown_defense_risk=50.0, drawdown_limit=0.060)
            else:
                self.risk = RiskConfig()
            self.alpha = AlphaFactory(cfg)

        # ------------------------------------------------------------------
        # 5a. triple-barrier label generator (used by gate + meta model)
        # ------------------------------------------------------------------
        def _label_events(self, panel: Panel, F: Dict[str, np.ndarray],
                        side: np.ndarray, max_events_per_sym: int = 4000
                        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
            cfg = self.cfg
            O, H, L, C = panel.open, panel.high, panel.low, panel.close
            atr, ev = F["atr"], F["fund_event"]
            feats, ys, rs = [], [], []
            horizon = cfg.hold_max_bars
            warm = max(cfg.beta_window, cfg.zscore_window) + 5

            for j in range(panel.N):
                ts = np.nonzero(side[warm:panel.T - 2, j] != 0)[0] + warm
                if len(ts) == 0:
                    continue
                if len(ts) > max_events_per_sym:
                    ts = ts[np.linspace(0, len(ts) - 1, max_events_per_sym).astype(int)]
                last_close = -10 ** 9
                for t in ts:
                    if t <= last_close:                     # no overlapping labels
                        continue
                    s = int(side[t, j])
                    nxt = t + 1
                    if not panel.valid[nxt, j]:
                        continue
                    R = cfg.stop_atr_mult * atr[t, j]
                    if not np.isfinite(R) or R <= 0:
                        continue
                    entry = O[nxt, j] * (1.0 + cfg.entry_slippage * s)
                    stop = entry - s * R
                    tp = entry + s * cfg.take_profit_r * R
                    end = min(nxt + horizon, panel.T - 1)
                    exit_px, k = C[end, j], end
                    fpnl = 0.0
                    for u in range(nxt, end + 1):
                        if not panel.valid[u, j]:
                            continue
                        fpnl += -s * ev[u, j] * entry       # event-time funding
                        if (s == 1 and L[u, j] <= stop) or (s == -1 and H[u, j] >= stop):
                            exit_px, k = stop, u
                            break
                        if (s == 1 and H[u, j] >= tp) or (s == -1 and L[u, j] <= tp):
                            exit_px, k = tp, u
                            break
                    exit_fill = exit_px * (1.0 - cfg.exit_slippage * s)
                    gross = s * (exit_fill - entry) + fpnl
                    fee = cfg.taker_fee * (entry + abs(exit_fill))
                    net_r = (gross - fee) / R
                    x = np.array([F[k_][t, j] for k_ in FEATURE_KEYS] + [float(s)])
                    if not np.all(np.isfinite(x)):
                        continue
                    feats.append(x)
                    rs.append(net_r)
                    ys.append(1.0 if net_r > 0 else 0.0)
                    last_close = k
            if not feats:
                return (np.zeros((0, len(FEATURE_KEYS) + 1)),
                        np.zeros(0), np.zeros(0))
            return np.asarray(feats), np.asarray(ys), np.asarray(rs)

        # ------------------------------------------------------------------
        # 5b. purged gate + meta-model fit  (training data only)
        # ------------------------------------------------------------------
        def fit_gate(self, panel: Panel, funding, oi,
                    train_start: pd.Timestamp, train_end: pd.Timestamp
                    ) -> Tuple[bool, MetaModel, Dict]:
            cfg = self.cfg
            # purge: nothing within `purge_hours` of the OOS boundary
            tr = panel.slice(train_start, train_end - pd.Timedelta(hours=cfg.purge_hours))
            if tr.T < max(cfg.beta_window, cfg.zscore_window) + BARS_PER_DAY * 5:
                return False, MetaModel(cfg), {"deploy": False, "reason": "insufficient_train"}
            F = self.alpha.build(tr, funding, oi)
            side = self.alpha.signals(tr, F)
            X, y, r = self._label_events(tr, F, side)
            n = len(y)
            if n < cfg.gate_min_events:
                return False, MetaModel(cfg), {"deploy": False, "n_events": n,
                                            "reason": "starvation"}
            meta = MetaModel(cfg).fit(X, y, r)
            p = meta.predict(X)
            sel = p >= meta.thresh
            exp_r = float(r[sel].mean()) if sel.sum() else float(r.mean())
            wr = float((y[sel] > 0).mean() * 100.0) if sel.sum() else 0.0
            ok = (n >= cfg.gate_min_events
                and exp_r >= cfg.gate_min_exp_r
                and meta.auc >= cfg.gate_min_auc)
            info = {"deploy": ok, "n_events": n, "n_selected": int(sel.sum()),
                    "exp_r": round(exp_r, 4), "raw_exp_r": round(float(r.mean()), 4),
                    "train_auc": round(meta.auc, 4),
                    "meta_thresh": round(meta.thresh, 3),
                    "train_win_rate": round(wr, 2),
                    "reason": "ok" if ok else
                            ("starvation" if n < cfg.gate_min_events else
                            "no_auc" if meta.auc < cfg.gate_min_auc else "no_edge")}
            return ok, meta, info

        # ------------------------------------------------------------------
        # 5c. OOS execution: bar-by-bar, intrabar MTM, hard DD kill-switch
        # ------------------------------------------------------------------
        def run_window(self, per_symbol: Dict[str, pd.DataFrame],
                    funding: Optional[Dict[str, pd.Series]] = None,
                    basis: Optional[Dict[str, pd.Series]] = None,
                    oi: Optional[Dict[str, pd.Series]] = None,
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
            base = {"window_id": window_id, "gate": gate, "deploy": ok,
                    "trades": 0, "roi_pct": 0.0, "max_dd_pct": 0.0,
                    "win_rate_pct": 0.0, "net_pnl": 0.0,
                    "equity": rk.initial_capital, "halted": False, "trades_list": []}
            if not ok:
                base["reason"] = f"Gate inactive: {gate.get('reason')}"
                return base

            # OOS panel needs warm-up history for causal features; we build the
            # features on [ws - warmup, we] then execute ONLY inside [ws, we].
            warm_bars = max(cfg.beta_window, cfg.zscore_window, cfg.rv_slow) + BARS_PER_DAY
            warm_start = ws - pd.Timedelta(minutes=15 * warm_bars)
            p = full.slice(warm_start, we)
            if p.T < warm_bars // 2:
                base["reason"] = "no_test_data"
                return base
            t0 = int(p.index.searchsorted(ws, side="left"))
            if p.T - t0 < 50:
                base["reason"] = "no_test_data"
                return base

            F = self.alpha.build(p, funding, oi)
            side_m = self.alpha.signals(p, F)
            atr, ev = F["atr"], F["fund_event"]
            O, H, L, C = p.open, p.high, p.low, p.close

            equity = rk.initial_capital
            peak = equity
            max_dd = 0.0
            positions: List[Position] = []
            trades: List[Dict] = []
            equity_curve: List[Tuple[pd.Timestamp, float]] = []
            cooldown = np.full(p.N, -10 ** 9, dtype=np.int64)
            halted = False

            def mtm(t: int, worst: bool) -> float:
                eq = equity
                for q in positions:
                    px = (L[t, q.col] if q.side == 1 else H[t, q.col]) if worst else C[t, q.col]
                    if not np.isfinite(px):
                        px = q.entry_px
                    eq += q.side * (px - q.entry_px) * q.qty + q.funding_pnl
                return eq

            def close_position(q: Position, t: int, px: float, why: str):
                nonlocal equity
                fill = px * (1.0 - cfg.exit_slippage * q.side)
                exit_fee = cfg.taker_fee * abs(fill) * q.qty
                pnl = q.side * (fill - q.entry_px) * q.qty + q.funding_pnl - exit_fee
                equity += pnl
                q.fees_paid += exit_fee
                trades.append({
                    "window_id": window_id, "sym": q.symbol, "side": q.side,
                    "entry_ts": p.index[q.entry_bar], "exit_ts": p.index[t],
                    "entry_px": round(q.entry_px, 8), "exit_px": round(fill, 8),
                    "qty": q.qty, "r_px": q.r_px,
                    "r_multiple": round(pnl / (q.r_px * q.qty), 4),
                    "pnl_d": round(pnl, 4), "fees_d": round(q.fees_paid, 4),
                    "funding_d": round(q.funding_pnl, 4),
                    "bars_held": t - q.entry_bar, "why": why,
                    "mfe_r": round(q.mfe_r, 3),
                })
                cooldown[q.col] = t + cfg.cooldown_bars

            # ---------------- main bar loop ----------------
            for t in range(t0, p.T):
                # (1) event-time funding accrual on OPEN positions
                for q in positions:
                    if ev[t, q.col] != 0.0 and p.valid[t, q.col]:
                        q.funding_pnl += -q.side * ev[t, q.col] * C[t, q.col] * q.qty

                # (2) intrabar risk check BEFORE anything else -> hard kill-switch
                eq_worst = mtm(t, worst=True)
                dd_worst = (peak - eq_worst) / peak if peak > 0 else 0.0
                if dd_worst >= rk.drawdown_limit and positions:
                    for q in list(positions):
                        px = C[t, q.col] if np.isfinite(C[t, q.col]) else q.entry_px
                        close_position(q, t, px, "dd_killswitch")
                    positions.clear()
                    halted = True

                # (3) exits
                for q in list(positions):
                    j = q.col
                    if not p.valid[t, j]:
                        continue
                    h_, l_, c_ = H[t, j], L[t, j], C[t, j]
                    held = t - q.entry_bar
                    fav = (h_ - q.entry_px) if q.side == 1 else (q.entry_px - l_)
                    q.mfe_r = max(q.mfe_r, fav / q.r_px)
                    exit_px, why = None, ""

                    # stop first (pessimistic intrabar ordering)
                    if (q.side == 1 and l_ <= q.stop_px) or (q.side == -1 and h_ >= q.stop_px):
                        exit_px, why = q.stop_px, "stop" if q.tier == 0 else "ratchet"
                    else:
                        tp = q.entry_px + q.side * cfg.take_profit_r * q.r_px
                        if (q.side == 1 and h_ >= tp) or (q.side == -1 and l_ <= tp):
                            exit_px, why = tp, "take_profit"
                        elif held >= cfg.hold_max_bars:
                            exit_px, why = c_, "time"
                        elif (held >= cfg.hold_min_bars
                            and abs(F["resid_z"][t, j]) <= cfg.exit_on_z_decay):
                            exit_px, why = c_, "signal_decay"

                    if exit_px is not None:
                        close_position(q, t, exit_px, why)
                        positions.remove(q)
                        continue

                    # ratchet: tiers, then chandelier trail on daily ATR
                    for tier_i, (trig, lock) in enumerate(cfg.ratchet_tiers, start=1):
                        if q.tier < tier_i and q.mfe_r >= trig:
                            new_stop = q.entry_px + q.side * lock * q.r_px
                            q.stop_px = max(q.stop_px, new_stop) if q.side == 1 \
                                else min(q.stop_px, new_stop)
                            q.tier = tier_i
                    if q.tier >= len(cfg.ratchet_tiers):
                        trail = (h_ - cfg.trail_atr_mult * atr[t, j]) if q.side == 1 \
                            else (l_ + cfg.trail_atr_mult * atr[t, j])
                        q.stop_px = max(q.stop_px, trail) if q.side == 1 \
                            else min(q.stop_px, trail)

                # (4) mark-to-market equity, peak, drawdown (bar-by-bar, not at close-only)
                eq_now = mtm(t, worst=False)
                eq_low = mtm(t, worst=True)
                peak = max(peak, eq_now)
                max_dd = max(max_dd, (peak - eq_low) / peak if peak > 0 else 0.0)
                equity_curve.append((p.index[t], eq_now))
                if halted:
                    break

                # (5) entries -> filled at OPEN of t+1
                if t >= p.T - 1 or len(positions) >= cfg.max_positions:
                    continue
                held_syms = {q.col for q in positions}
                cands = []
                for j in range(p.N):
                    if side_m[t, j] == 0 or j in held_syms or t < cooldown[j]:
                        continue
                    if not (p.valid[t, j] and p.valid[t + 1, j]):
                        continue
                    x = np.array([F[k_][t, j] for k_ in FEATURE_KEYS]
                                + [float(side_m[t, j])])
                    if not np.all(np.isfinite(x)) or not meta.accept(x):
                        continue
                    cands.append((float(meta.predict(x.reshape(1, -1))[0]),
                                abs(float(F["resid_z"][t, j])), j))
                cands.sort(key=lambda v: (-v[0], -v[1]))

                for prob, _, j in cands[:cfg.top_k_per_bar]:
                    if len(positions) >= cfg.max_positions:
                        break
                    s = int(side_m[t, j])
                    R = cfg.stop_atr_mult * atr[t, j]
                    if not np.isfinite(R) or R <= 0:
                        continue
                    entry = O[t + 1, j] * (1.0 + cfg.entry_slippage * s)
                    if not np.isfinite(entry) or entry <= 0:
                        continue

                    dd_now = (peak - eq_now) / peak if peak > 0 else 0.0
                    net_profit = eq_now - rk.initial_capital
                    risk_d = (rk.drawdown_defense_risk if dd_now > rk.dd_defense_trigger
                            else rk.house_money_risk if net_profit > rk.house_money_trigger
                            else rk.base_risk)
                    qty = risk_d / R
                    notional = qty * entry
                    cap = min(rk.max_symbol_leverage * eq_now,
                            rk.max_gross_leverage * eq_now
                            - sum(q.qty * q.entry_px for q in positions))
                    if cap <= 0:
                        continue
                    if notional > cap:
                        qty = cap / entry
                    if qty <= 0:
                        continue

                    entry_fee = cfg.taker_fee * entry * qty
                    equity -= entry_fee
                    pos = Position(symbol=p.symbols[j], col=j, side=s, entry_px=entry,
                                qty=qty, r_px=R, stop_px=entry - s * R,
                                entry_bar=t + 1, atr_at_entry=atr[t, j],
                                fees_paid=entry_fee)
                    positions.append(pos)

            # ---------------- force-flat at window end ----------------
            if positions:
                t_end = min(p.T - 1, max(t0, len(p.index) - 1))
                for q in list(positions):
                    px = C[t_end, q.col] if np.isfinite(C[t_end, q.col]) else q.entry_px
                    close_position(q, t_end, px, "window_end")
                positions.clear()
                eq_now = equity
                peak = max(peak, eq_now)
                max_dd = max(max_dd, (peak - eq_now) / peak if peak > 0 else 0.0)
                equity_curve.append((p.index[t_end], eq_now))

            net = equity - rk.initial_capital
            wins = sum(1 for tr in trades if tr["pnl_d"] > 0)
            rs = np.array([tr["r_multiple"] for tr in trades]) if trades else np.zeros(0)
            gross_win = sum(tr["pnl_d"] for tr in trades if tr["pnl_d"] > 0)
            gross_loss = -sum(tr["pnl_d"] for tr in trades if tr["pnl_d"] <= 0)

            return {
                "window_id": window_id, "deploy": True, "gate": gate,
                "halted": halted, "equity": round(equity, 2),
                "net_pnl": round(net, 2),
                "roi_pct": round(net / rk.initial_capital * 100.0, 4),
                "max_dd_pct": round(max_dd * 100.0, 4),
                "trades": len(trades),
                "win_rate_pct": round(wins / len(trades) * 100.0, 2) if trades else 0.0,
                "avg_r": round(float(rs.mean()), 4) if len(rs) else 0.0,
                "expectancy_d": round(net / len(trades), 4) if trades else 0.0,
                "profit_factor": round(gross_win / gross_loss, 3) if gross_loss > 0 else float("inf"),
                "total_fees_d": round(sum(tr["fees_d"] for tr in trades), 4),
                "total_funding_d": round(sum(tr["funding_d"] for tr in trades), 4),
                "equity_curve": equity_curve,
                "trades_list": trades,
                "reason": "ok",
            }

        # ------------------------------------------------------------------
        # 5d. walk-forward driver
        # ------------------------------------------------------------------
        def run_walkforward(self, per_symbol: Dict[str, pd.DataFrame],
                            windows: List[Tuple[str, str]],
                            funding=None, basis=None, oi=None) -> pd.DataFrame:
            panel = Panel(per_symbol)
            rows = []
            for i, (a, b) in enumerate(windows, start=1):
                r = self.run_window(per_symbol, funding, basis, oi, a, b,
                                    window_id=f"W{i:02d}", panel=panel)
                rows.append({k: v for k, v in r.items()
                            if k not in ("trades_list", "equity_curve", "gate")}
                            | {"gate_reason": r["gate"].get("reason"),
                            "gate_exp_r": r["gate"].get("exp_r"),
                            "gate_auc": r["gate"].get("train_auc"),
                            "gate_n": r["gate"].get("n_events")})
            return pd.DataFrame(rows)

    # ===========================================================================
    # 6. SELF-TEST / DEMO (synthetic panel; swap in your real loaders)
    # ===========================================================================
    def _synth_panel(symbols: List[str], start: str, periods: int, seed: int = 7):
        rs = np.random.default_rng(seed)
        idx = pd.date_range(start, periods=periods, freq="15min", tz=None)
        mkt = rs.normal(0, 0.0016, periods).cumsum()
        per_symbol, funding, oi = {}, {}, {}
        for k, s in enumerate(symbols):
            beta = 0.6 + 0.9 * rs.random()
            idio = rs.normal(0, 0.0022, periods)
            # inject genuine mean-reverting idiosyncratic component (AR(1), phi<1)
            e = np.zeros(periods)
            for i in range(1, periods):
                e[i] = 0.985 * e[i - 1] + idio[i]
            logp = math.log(10 + 90 * rs.random()) + beta * mkt + e
            c = np.exp(logp)
            rng_ = np.abs(rs.normal(0, 0.0018, periods)) * c
            o = np.concatenate([[c[0]], c[:-1]])
            h = np.maximum(o, c) + rng_
            l = np.minimum(o, c) - rng_
            v = rs.lognormal(11, 0.5, periods)
            per_symbol[s] = pd.DataFrame({"open": o, "high": h, "low": l, "close": c, "volume": v}, index=idx)
            f_idx = pd.date_range(idx[0].normalize(), idx[-1], freq="8h")
            funding[s] = pd.Series(rs.normal(0.0001, 0.00018, len(f_idx)), index=f_idx)
            oi[s] = pd.Series(rs.lognormal(15, 0.15, periods).cumsum() / 1e3, index=idx)
        return per_symbol, funding, oi

    if __name__ == "__main__":
        SYMS = ["BTC", "ETH", "XRP", "SOL", "BNB", "DOGE", "ADA", "TRX", "LINK", "AVAX", "SUI", "NEAR", "DOT", "LTC", "BCH", "APT", "OP", "ARB"]
        px, fund, oi_ = _synth_panel(SYMS, "2024-01-01", 96 * 260)
        
        eng = ResidualDislocationEngine(mode="compliant")
        wins = [("2024-07-01", "2024-07-31"),
                ("2024-08-01", "2024-08-31"),
                ("2024-09-01", "2024-09-30")]
        res = eng.run_walkforward(px, wins, funding=fund, oi=oi_)
        pd.set_option("display.width", 200, "display.max_columns", 50)
        print(res[["window_id", "deploy", "trades", "roi_pct", "max_dd_pct",
                "win_rate_pct", "avg_r", "profit_factor", "halted",
                "gate_reason", "gate_exp_r", "gate_auc", "gate_n"]])

    ```
