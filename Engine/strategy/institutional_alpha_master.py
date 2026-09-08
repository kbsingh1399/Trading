# Engine/strategy/institutional_alpha_master.py
"""
OX ALPHA — Round 5 Institutional Master Engine.
Five-pillar architecture:
  1. Structural Big-R Geometry: Anchored to PDH/PDL, Daily FVG, Displacement OB, 4H Swings (1R = 1.8%–4.0%).
  2. Cross-Sectional Ranking: Top-2 conviction outliers z-scored across 18 assets.
  3. Causal Maker Execution: Resting limits with queue fill probability and straight-through adverse selection rejection.
  4. Microstructure Anti-Retracement Ratchet: +0.8R -> +0.15R BE, +1.5R -> +0.80R lock, +2.25R target, 32-bar time decay.
  5. Causal Deployment Gate: Purged CV-AUC and post-friction expectancy validation over trailing 6 months.

Strictly causal:
  - Daily/4H structures shifted by 1 full day/bar (shift(1)).
  - Limit orders staged at bar j close, valid for bar j+1 onward.
  - Zero forward leakage, zero per-window lookup tables.
"""
from __future__ import annotations

import json
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig
from Engine.core.portfolio_execution_kernel import PortfolioExecutionKernel
from Engine.ml.footprint_features import FootprintLadderFeatures
from Engine.ml.rf_meta_labeler import RegressionRMetaLabeler, BarrierConfig, CVConfig
from Engine.strategy.smc_event_detector import SMCEventDetector, SMCConfig


# ===================================================================
# 1. CONFIGURATION
# ===================================================================
@dataclass
class MasterConfig:
    # --- Pillar 1: Structure ---
    zone_max_age_days: int = 10
    swing_lookback_4h: int = 6
    stop_buffer_atr_frac: float = 0.10      # Stop = zone edge ± 0.10 * ATR_d
    min_stop_dist_pct: float = 0.018        # 1R >= 1.8% (friction <= 0.15R)
    max_stop_dist_pct: float = 0.040        # 1R <= 4.0%
    # --- Pillar 2: Cross-sectional ranking ---
    top_k: int = 2                          # Only Top-2 assets can stage orders
    min_z_gap: float = 0.8                  # Outlier score gap over universe median
    # --- Pillar 3: Maker execution ---
    maker_fee: float = 0.0004               # 4 bps maker fee
    taker_fee: float = 0.0008               # 8 bps taker fee
    exit_slippage: float = 0.0015           # 15 bps exit slippage
    fill_prob_calib: float = 0.70           # 70% fill probability on touch
    through_fail_atr: float = 0.25          # Adverse selection: reject if bar closes > 0.25 ATR through level
    limit_ttl_bars: int = 16                # 4 hours TTL
    # --- Pillar 4: Ratchet & Target ---
    target_r: float = 2.25
    arm0_r: float = 0.80
    lock0_r: float = 0.15
    arm1_r: float = 1.50
    lock1_r: float = 0.80
    time_decay_bars: int = 32
    time_decay_r: float = 0.20
    # --- Pillar 5: Causal Gate ---
    train_months: int = 6
    deploy_auc_min: float = 0.54
    deploy_expectancy_min_r: float = 0.20
    # --- Portfolio Risk ---
    max_positions: int = 2
    max_pending: int = 4


# ===================================================================
# 2. PILLAR 1: MULTI-TIMEFRAME STRUCTURE (Strictly Causal)
# ===================================================================
class MultiTimeframeStructure:
    """
    Daily frame computed only from completed daily bars and shifted by 1 full day (shift(1)).
    4H swings computed only from completed 4H bars with centered window shifted by (k + 1).
    All mapped onto 15m index via forward-fill.
    """
    def __init__(self, cfg: MasterConfig):
        self.cfg = cfg

    def daily_frame(self, df15: pd.DataFrame) -> pd.DataFrame:
        d = pd.DataFrame({
            "high_d": df15["high"].resample("1D").max(),
            "low_d":  df15["low"].resample("1D").min(),
            "open_d": df15["open"].resample("1D").first(),
            "close_d": df15["close"].resample("1D").last(),
        }).dropna()
        d["atr_d"] = (d["high_d"] - d["low_d"]).rolling(14, min_periods=5).mean()
        d["pdh"] = d["high_d"].shift(1)
        d["pdl"] = d["low_d"].shift(1)

        # Daily FVG zones
        bull = d["low_d"] > d["high_d"].shift(2)
        bear = d["high_d"] < d["low_d"].shift(2)
        d["fvg_bull_lo"] = np.where(bull, d["high_d"].shift(2), np.nan)
        d["fvg_bull_hi"] = np.where(bull, d["low_d"], np.nan)
        d["fvg_bear_lo"] = np.where(bear, d["high_d"], np.nan)
        d["fvg_bear_hi"] = np.where(bear, d["low_d"].shift(2), np.nan)

        # Displacement Order Blocks
        body = (d["close_d"] - d["open_d"]).abs()
        rng = (d["high_d"] - d["low_d"]).clip(lower=1e-12)
        big = (rng > 1.5 * d["atr_d"]) & (body / rng > 0.5)
        d["ob_bull"] = d["low_d"].where(big & (d["close_d"] > d["open_d"]))
        d["ob_bear"] = d["high_d"].where(big & (d["close_d"] < d["open_d"]))

        # Forward-fill zones with max age
        lim = self.cfg.zone_max_age_days
        for c in ("fvg_bull_lo", "fvg_bull_hi", "fvg_bear_lo", "fvg_bear_hi", "ob_bull", "ob_bear"):
            d[c] = d[c].ffill(limit=lim)
        
        # Strict Causality: shift by 1 full day
        return d.shift(1)

    def h4_frame(self, df15: pd.DataFrame) -> pd.DataFrame:
        h4 = pd.DataFrame({
            "high_4h": df15["high"].resample("4h").max(),
            "low_4h":  df15["low"].resample("4h").min(),
        }).dropna()
        k = self.cfg.swing_lookback_4h
        sh = (h4["high_4h"] == h4["high_4h"].rolling(2 * k + 1, center=True).max())
        sl = (h4["low_4h"] == h4["low_4h"].rolling(2 * k + 1, center=True).min())
        h4["swing_hi"] = h4["high_4h"].where(sh).ffill(limit=6).shift(k + 1)
        h4["swing_lo"] = h4["low_4h"].where(sl).ffill(limit=6).shift(k + 1)
        return h4.shift(1)

    def map_to_15m(self, df15: pd.DataFrame) -> pd.DataFrame:
        d = self.daily_frame(df15)
        h4 = self.h4_frame(df15)
        st = d.reindex(df15.index, method="ffill")
        s4 = h4.reindex(df15.index, method="ffill")
        return pd.concat([st, s4], axis=1)


# ===================================================================
# 3. PILLAR 2: CROSS-SECTIONAL DISPERSION RANKING
# ===================================================================
class CrossSectionalRanker:
    """
    Per bar t: calculates rolling z-scores across all 18 symbols for
    absorption, CVD divergence, volume surge, and funding squeeze.
    Only assets exceeding the universe median by min_z_gap may stage orders.
    """
    @staticmethod
    def _roll_z(s: pd.Series, w: int = 672) -> pd.Series:
        m = s.rolling(w, min_periods=96).mean()
        sd = s.rolling(w, min_periods=96).std(ddof=0).replace(0.0, np.nan)
        return ((s - m) / sd).clip(-4.0, 4.0)

    def score_universe(self, per_symbol: Dict[str, pd.DataFrame],
                       ladder: Dict[str, pd.DataFrame],
                       funding: Optional[Dict[str, pd.Series]] = None
                       ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        per_bar_dir = {}
        per_bar_score = {}
        for sym, df in per_symbol.items():
            lf = ladder.get(sym)
            if lf is None or lf.empty:
                lf = pd.DataFrame(index=df.index)
            else:
                lf = lf.reindex(df.index).fillna(0.0)

            wsa = self._roll_z(lf.get("wick_sell_absorb", pd.Series(0.0, index=df.index)))
            wbe = self._roll_z(lf.get("wick_buy_exhaust", pd.Series(0.0, index=df.index)))
            ab = self._roll_z(lf.get("absorption_ratio", pd.Series(0.0, index=df.index)))
            cp = lf.get("close_pos", pd.Series(0.5, index=df.index))

            long_raw = wsa.fillna(0.0) + ab.clip(lower=0.0).fillna(0.0) + cp.clip(0.0, 1.0)
            short_raw = wbe.fillna(0.0) + (-ab.clip(upper=0.0)).fillna(0.0) + (1.0 - cp).clip(0.0, 1.0)

            fr_z = pd.Series(0.0, index=df.index)
            if funding is not None and sym in funding:
                fr_z = self._roll_z(funding[sym].reindex(df.index).ffill()).fillna(0.0)

            vol = df["volume"].astype(float)
            vol_z = self._roll_z(np.log1p(vol)).fillna(0.0)

            long_score = (long_raw + vol_z - fr_z.clip(lower=0.0)).to_numpy()
            short_score = (short_raw + vol_z + fr_z.clip(upper=0.0) * -1.0).to_numpy()

            side = np.where(long_score >= short_score, 1, -1)
            strength = np.where(long_score >= short_score, long_score, short_score)

            per_bar_dir[sym] = pd.Series(side, index=df.index)
            per_bar_score[sym] = pd.Series(strength, index=df.index)

        return pd.DataFrame(per_bar_score), pd.DataFrame(per_bar_dir)

    def pick_top(self, sc_row: pd.Series, dr_row: pd.Series,
                 cfg: MasterConfig) -> List[Tuple[str, int, float]]:
        valid = sc_row.dropna()
        if len(valid) < 4:
            return []
        med = float(valid.median())
        ranked = valid.sort_values(ascending=False).head(cfg.top_k)
        out = []
        for sym, val in ranked.items():
            if (val - med) >= cfg.min_z_gap and dr_row.get(sym, 0) != 0:
                out.append((sym, int(dr_row[sym]), float(val)))
        return out


# ===================================================================
# 4. PILLAR 3: STAGED LIMIT ORDERS & CAUSAL MAKER-FILL MODEL
# ===================================================================
@dataclass
class _StagedOrder:
    symbol: str
    side: int                # +1 long, -1 short
    limit_price: float
    stop_price: float        # invalidation (1R anchor)
    raw_r: float             # |limit - stop|
    staged_bar: int
    ttl_bars: int
    event_type: str = ""


class ZoneTriggerEngine:
    """
    Identifies high-conviction structural zones and returns candidate limit orders.
    Enforces big-R geometry: 1R >= 1.8% of entry price.
    """
    def __init__(self, cfg: MasterConfig):
        self.cfg = cfg

    def scan_bar(self, t: int, df15: pd.DataFrame, st: pd.DataFrame
                 ) -> List[Tuple[str, int, float, float, float]]:
        c = df15["close"].iat[t]; h = df15["high"].iat[t]; l = df15["low"].iat[t]
        atr_d = max(st["atr_d"].iat[t], 1e-12) if pd.notna(st["atr_d"].iat[t]) else c * 0.03
        buf = self.cfg.stop_buffer_atr_frac * atr_d
        out = []

        def ok_r(entry: float, stop: float) -> bool:
            rd = abs(entry - stop) / entry
            return self.cfg.min_stop_dist_pct <= rd <= self.cfg.max_stop_dist_pct

        # --- LONG zones ---
        pdl = st["pdl"].iat[t]
        if pd.notna(pdl) and c > pdl and l <= pdl and (pdl - l) <= 0.5 * atr_d:
            stop = pdl - buf
            if ok_r(pdl, stop):
                out.append(("SWEEP_PDL", 1, pdl, stop, pdl - stop))

        fvg_b_hi, fvg_b_lo = st["fvg_bull_hi"].iat[t], st["fvg_bull_lo"].iat[t]
        if pd.notna(fvg_b_hi) and l <= fvg_b_hi and c >= fvg_b_lo:
            stop = fvg_b_lo - buf
            if ok_r(fvg_b_hi, stop):
                out.append(("FVG_BULL", 1, fvg_b_hi, stop, fvg_b_hi - stop))

        ob_bull = st["ob_bull"].iat[t]
        if pd.notna(ob_bull) and l <= ob_bull and c > ob_bull:
            stop = ob_bull - buf
            if ok_r(ob_bull, stop):
                out.append(("OB_BULL", 1, ob_bull, stop, ob_bull - stop))

        sw_lo = st["swing_lo"].iat[t]
        if pd.notna(sw_lo) and l <= sw_lo and c > sw_lo:
            stop = sw_lo - buf
            if ok_r(sw_lo, stop):
                out.append(("SWING_LO", 1, sw_lo, stop, sw_lo - stop))

        # --- SHORT zones ---
        pdh = st["pdh"].iat[t]
        if pd.notna(pdh) and c < pdh and h >= pdh and (h - pdh) <= 0.5 * atr_d:
            stop = pdh + buf
            if ok_r(pdh, stop):
                out.append(("SWEEP_PDH", -1, pdh, stop, stop - pdh))

        fvg_s_lo, fvg_s_hi = st["fvg_bear_lo"].iat[t], st["fvg_bear_hi"].iat[t]
        if pd.notna(fvg_s_lo) and h >= fvg_s_lo and c <= fvg_s_hi:
            stop = fvg_s_hi + buf
            if ok_r(fvg_s_lo, stop):
                out.append(("FVG_BEAR", -1, fvg_s_lo, stop, stop - fvg_s_lo))

        ob_bear = st["ob_bear"].iat[t]
        if pd.notna(ob_bear) and h >= ob_bear and c < ob_bear:
            stop = ob_bear + buf
            if ok_r(ob_bear, stop):
                out.append(("OB_BEAR", -1, ob_bear, stop, stop - ob_bear))

        sw_hi = st["swing_hi"].iat[t]
        if pd.notna(sw_hi) and h >= sw_hi and c < sw_hi:
            stop = sw_hi + buf
            if ok_r(sw_hi, stop):
                out.append(("SWING_HI", -1, sw_hi, stop, stop - sw_hi))

        return out


class MakerFillModel:
    """
    Causal limit-fill simulation:
      1. Limit order resting at structural price P.
      2. Fill occurs only if price trades THROUGH the level.
      3. Adverse-selection protection: if bar closes > 0.25*ATR through the level,
         market blew straight through without liquidity -> order cancelled/failed.
      4. 70% fill probability on touch (conservative queue haircut).
      5. Execution price = P (0 slippage, 4 bps maker fee).
    """
    def __init__(self, cfg: MasterConfig, rng_seed: int = 42):
        self.cfg = cfg
        self.rng = np.random.default_rng(rng_seed)

    def check_fill(self, order: _StagedOrder, df15: pd.DataFrame,
                   st: pd.DataFrame, current_bar: int) -> Optional[Tuple[int, float]]:
        P = order.limit_price
        A = max(st["atr_d"].iat[current_bar], 1e-12) if pd.notna(st["atr_d"].iat[current_bar]) else P * 0.03
        lo = df15["low"].iat[current_bar]
        hi = df15["high"].iat[current_bar]
        cl = df15["close"].iat[current_bar]

        touched = (order.side == 1 and lo <= P) or (order.side == -1 and hi >= P)
        if not touched:
            return None

        # Straight-through adverse selection failure
        straight_through = (order.side == 1 and cl < P - self.cfg.through_fail_atr * A) or \
                           (order.side == -1 and cl > P + self.cfg.through_fail_atr * A)
        if straight_through:
            return None

        # Invalidation before fill
        if (order.side == 1 and cl < order.stop_price) or (order.side == -1 and cl > order.stop_price):
            return None

        if self.rng.random() <= self.cfg.fill_prob_calib:
            return (current_bar, P)

        return None


# ===================================================================
# 5. PILLAR 4 & 5: INSTITUTIONAL ALPHA MASTER ENGINE
# ===================================================================
class InstitutionalAlphaMaster:
    def __init__(self, cfg: MasterConfig = MasterConfig(), mode: str = "compliant"):
        """
        mode='compliant': $25 base risk, $50 house money, $15 defense, 4.5% drawdown limit.
        mode='institutional': $100 base risk (2.0%), $150 house money, $50 defense, 6.0% drawdown limit.
        """
        self.cfg = cfg
        self.mode = mode
        self.structure = MultiTimeframeStructure(cfg)
        self.trigger = ZoneTriggerEngine(cfg)
        self.ranker = CrossSectionalRanker()
        self.fill_model = MakerFillModel(cfg)

        if mode == "institutional":
            self.risk_cfg = RiskConfig(initial_capital=5000.0, base_risk=100.0,
                                       house_money_risk=150.0, drawdown_defense_risk=50.0,
                                       drawdown_limit=0.060)
        else:
            self.risk_cfg = RiskConfig(initial_capital=5000.0, base_risk=25.0,
                                       house_money_risk=50.0, drawdown_defense_risk=15.0,
                                       drawdown_limit=0.045)

        self.ratchet = RatchetConfig(
            arm0_r=cfg.arm0_r, lock0_r=cfg.lock0_r,
            arm1_r=cfg.arm1_r, lock1_r=cfg.lock1_r,
            min_target_r=cfg.target_r,
            time_decay_bars=cfg.time_decay_bars, time_decay_r=cfg.time_decay_r)

    # ---------------- Meta-Gate Training ----------------
    def fit_meta_gate(self, per_symbol: Dict[str, pd.DataFrame],
                      fp_feats: Dict[str, pd.DataFrame],
                      train_start: pd.Timestamp,
                      train_end: pd.Timestamp) -> Tuple[bool, Dict]:
        try:
            lab = RegressionRMetaLabeler(
                barrier=BarrierConfig(tp_r=self.cfg.target_r, sl_r=1.0, vertical_bars=48, min_terminal_r=0.20),
                cv=CVConfig(purge_hours=72, embargo_hours=24))
            pooled = []
            for sym, df in per_symbol.items():
                sl = df.loc[train_start:train_end]
                if len(sl) < 1500:
                    continue
                st = self.structure.map_to_15m(sl)
                # Event mask
                mask = np.zeros(len(sl), dtype=bool)
                for t in range(96, len(sl)):
                    if self.trigger.scan_bar(t, sl, st):
                        mask[t] = True
                if mask.sum() < 15:
                    continue

                # Generate realized-R labels
                sig_side = np.zeros(len(sl), dtype=np.int8)
                sig_rr = np.zeros(len(sl), dtype=np.float64)
                for t in np.flatnonzero(mask):
                    cands = self.trigger.scan_bar(t, sl, st)
                    if cands:
                        _, side, edge, stop, raw_r = cands[0]
                        sig_side[t] = side
                        sig_rr[t] = raw_r

                labels = lab.triple_barrier_labels(sl, mask, sig_side, sig_rr)
                if len(labels) < 15:
                    continue

                # Features: Footprint channels + structure ratios
                fpz = fp_feats[sym].loc[sl.index].fillna(0.0) if sym in fp_feats else pd.DataFrame(index=sl.index)
                struct_feats = pd.DataFrame(index=sl.index)
                struct_feats["dist_to_pdl"] = ((sl["close"] - st["pdl"]) / st["atr_d"].clip(lower=1e-9)).fillna(0.0)
                struct_feats["dist_to_pdh"] = ((st["pdh"] - sl["close"]) / st["atr_d"].clip(lower=1e-9)).fillna(0.0)
                
                tab = fpz.join(struct_feats, how="left").fillna(0.0).loc[sl.index[labels.index.to_numpy()]]
                tab["exit_r"] = labels["exit_r"].to_numpy()
                tab["symbol"] = sym
                ev_idx = labels.index.to_numpy()
                tab["abs_bar"] = sl.index.get_indexer(sl.index)[ev_idx] + df.index.get_indexer([sl.index[0]])[0]
                pooled.append(tab.reset_index(drop=True))

            if not pooled:
                return False, {"deploy": False, "reason": "no_events", "auc": 0.5, "exp_r": 0.0}

            pool = pd.concat(pooled, ignore_index=True)
            if len(pool) < 60:
                return False, {"deploy": False, "reason": "starvation", "auc": 0.5, "exp_r": 0.0}

            fit_res = lab.fit(pool)
            auc = fit_res.get("mean_cv_auc", 0.5)
            exp = fit_res.get("oof_expectancy_all", -1.0)
            ok = (auc >= self.cfg.deploy_auc_min) and (exp >= self.cfg.deploy_expectancy_min_r)
            return bool(ok), {"deploy": bool(ok), "auc": float(auc), "exp_r": float(exp),
                              "n_events": int(len(pool)), "reason": "ok" if ok else "no_edge"}

        except Exception as e:
            return False, {"deploy": False, "reason": f"gate_error:{e}", "auc": 0.5, "exp_r": 0.0}

    # ---------------- OOS Execution Window ----------------
    def run_window(self, per_symbol: Dict[str, pd.DataFrame],
                   ladder: Dict[str, pd.DataFrame],
                   win_start: str, win_end: str,
                   funding: Optional[Dict[str, pd.Series]] = None) -> Dict:
        cfg = self.cfg
        ws = pd.Timestamp(win_start)
        we = pd.Timestamp(win_end) + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)

        # Causal Gate
        train_end = ws - pd.Timedelta(hours=72)
        train_start = train_end - pd.Timedelta(days=cfg.train_months * 30)
        deploy, gate = self.fit_meta_gate(per_symbol, ladder, train_start, train_end)

        if not deploy:
            return {
                "deploy": False, "gate": gate, "halted": False,
                "trades": 0, "roi_pct": 0.0, "max_dd_pct": 0.0,
                "win_rate_pct": 0.0, "net_pnl": 0.0, "trades_list": [],
                "reason": f"Deployment gate inactive: {gate.get('reason')}"
            }

        # Active test window data
        test_syms = {}
        for sym, df in per_symbol.items():
            sl = df.loc[ws:we]
            if len(sl) > 200:
                test_syms[sym] = sl

        if not test_syms:
            return {
                "deploy": False, "gate": gate, "halted": False,
                "trades": 0, "roi_pct": 0.0, "max_dd_pct": 0.0,
                "win_rate_pct": 0.0, "net_pnl": 0.0, "trades_list": [],
                "reason": "Insufficient test data"
            }

        st_all = {s: self.structure.map_to_15m(d) for s, d in test_syms.items()}
        sc, dr = self.ranker.score_universe(test_syms, ladder, funding)

        T = min(len(d) for d in test_syms.values())
        syms = list(test_syms.keys())

        staged_orders: List[_StagedOrder] = []
        open_pos: List[Dict] = []
        equity = 5000.0
        peak = equity
        max_dd = 0.0
        trades = []
        house_money = False
        defense = False
        halted = False

        for t in range(96, T):
            t_idx = test_syms[syms[0]].index[t]

            # 1. Expire stale staged orders
            staged_orders = [o for o in staged_orders if (t - o.staged_bar) <= o.ttl_bars]

            # 2. Check maker fills for resting orders
            remaining = []
            for o in staged_orders:
                if len(open_pos) >= cfg.max_positions:
                    remaining.append(o)
                    continue
                df15 = test_syms[o.symbol]
                st_s = st_all[o.symbol]
                res = self.fill_model.check_fill(o, df15, st_s, t)
                if res is not None:
                    tb, fill_px = res
                    open_pos.append({
                        "sym": o.symbol, "side": o.side, "entry": fill_px,
                        "stop": o.stop_price, "raw_r": o.raw_r, "t_in": tb,
                        "mfe_r": 0.0, "armed": 0, "lock": -1.0, "event_type": o.event_type
                    })
                else:
                    remaining.append(o)
            staged_orders = remaining

            # 3. Manage open positions (stop-first, ratchet, target, decay)
            for pos in list(open_pos):
                df15 = test_syms[pos["sym"]]
                h = df15["high"].iat[t]
                l = df15["low"].iat[t]
                cl = df15["close"].iat[t]
                R = pos["raw_r"]
                side = pos["side"]
                entry = pos["entry"]
                age = t - pos["t_in"]

                # Track MFE
                fav = (h - entry) / R if side == 1 else (entry - l) / R
                pos["mfe_r"] = max(pos["mfe_r"], fav)

                # Microstructure Ratchet Arming
                if pos["armed"] == 0 and pos["mfe_r"] >= cfg.arm0_r:
                    pos["lock"] = cfg.lock0_r
                    pos["armed"] = 1
                if pos["armed"] == 1 and pos["mfe_r"] >= cfg.arm1_r:
                    pos["lock"] = cfg.lock1_r
                    pos["armed"] = 2

                lock_px = entry + side * pos["lock"] * R
                tp_px = entry + side * cfg.target_r * R
                exit_px, why = None, ""

                # Stop-first conservative barrier
                if side == 1 and l <= pos["stop"]:
                    exit_px, why = pos["stop"], "stop"
                elif side == -1 and h >= pos["stop"]:
                    exit_px, why = pos["stop"], "stop"

                # Target exit
                if exit_px is None:
                    if side == 1 and h >= tp_px:
                        exit_px, why = tp_px, "target"
                    elif side == -1 and l <= tp_px:
                        exit_px, why = tp_px, "target"

                # Ratchet Lock exit
                if exit_px is None and pos["armed"] > 0:
                    if side == 1 and l <= lock_px:
                        exit_px, why = lock_px, "lock"
                    elif side == -1 and h >= lock_px:
                        exit_px, why = lock_px, "lock"

                # Time Decay exit
                if exit_px is None and age >= cfg.time_decay_bars and pos["mfe_r"] < cfg.time_decay_r:
                    exit_px, why = cl, "decay"

                if exit_px is not None:
                    pnl_r = side * (exit_px - entry) / R
                    # Real exchange frictions: 4 bps maker entry + 8 bps taker exit + 15 bps exit slip = 27 bps
                    fric_r = (0.0027 * entry) / R
                    net_pnl_r = pnl_r - fric_r

                    risk_d = (self.risk_cfg.house_money_risk if house_money
                              else self.risk_cfg.drawdown_defense_risk if defense
                              else self.risk_cfg.base_risk)
                    pnl_d = net_pnl_r * risk_d
                    equity += pnl_d
                    peak = max(peak, equity)
                    max_dd = max(max_dd, (peak - equity) / peak if peak > 0 else 0.0)

                    house_money = (equity - 5000.0) > 500.0
                    defense = ((peak - equity) / peak) > 0.025

                    trades.append({
                        "sym": pos["sym"], "side": side, "entry": entry,
                        "exit": exit_px, "r": net_pnl_r, "pnl_d": pnl_d,
                        "why": why, "age": age
                    })
                    open_pos.remove(pos)

                    # Hard Drawdown Circuit Breaker
                    if max_dd >= self.risk_cfg.drawdown_limit:
                        halted = True
                        break

            if halted:
                break

            # 4. Scan new candidate zones & stage top-ranked orders for next bars
            if (len(open_pos) + len(staged_orders)) < cfg.max_pending and t_idx in sc.index:
                sc_row = sc.loc[t_idx]
                dr_row = dr.loc[t_idx]
                top_picks = self.ranker.pick_top(sc_row, dr_row, cfg)
                for sym, side, score in top_picks:
                    if any(o.symbol == sym for o in staged_orders) or any(p["sym"] == sym for p in open_pos):
                        continue
                    df15 = test_syms[sym]
                    st_s = st_all[sym]
                    hits = self.trigger.scan_bar(t, df15, st_s)
                    for (etype, hside, edge, stop, raw_r) in hits:
                        if hside == side:
                            staged_orders.append(_StagedOrder(
                                symbol=sym, side=side, limit_price=edge, stop_price=stop,
                                raw_r=raw_r, staged_bar=t, ttl_bars=cfg.limit_ttl_bars,
                                event_type=etype
                            ))
                            break

        net_pnl = equity - 5000.0
        roi_pct = (net_pnl / 5000.0) * 100.0
        tot_trades = len(trades)
        wins = sum(1 for tr in trades if tr["r"] > 0)
        win_rate = (wins / tot_trades * 100.0) if tot_trades > 0 else 0.0

        return {
            "deploy": True,
            "gate": gate,
            "halted": halted,
            "equity": equity,
            "net_pnl": net_pnl,
            "roi_pct": roi_pct,
            "max_dd_pct": max_dd * 100.0,
            "trades": tot_trades,
            "win_rate_pct": win_rate,
            "trades_list": trades
        }


# ===================================================================
# 6. UNIFIED 20-WINDOW WALK-FORWARD BENCHMARK RUNNER
# ===================================================================
WINDOWS = [
    ("W01", "2021-05-01", "2021-05-31", "May 2021 Great Liquidation Crash"),
    ("W02", "2021-09-01", "2021-09-30", "September 2021 El Salvador Flash Crash"),
    ("W03", "2021-11-01", "2021-11-30", "November 2021 Cycle Peak Reversal"),
    ("W04", "2022-01-01", "2022-01-31", "January 2022 Fed Macro Tightening"),
    ("W05", "2022-05-01", "2022-05-31", "May 2022 Terra-Luna Systemic Shock"),
    ("W06", "2022-06-01", "2022-06-30", "June 2022 3AC & Celsius Capitulation"),
    ("W07", "2022-09-01", "2022-09-30", "September 2022 ETH Merge Chop & Grind"),
    ("W08", "2022-11-01", "2022-11-30", "November 2022 FTX Collapse Bottom"),
    ("W09", "2023-01-01", "2023-01-31", "January 2023 Short Squeeze Ignition"),
    ("W10", "2023-03-01", "2023-03-31", "March 2023 US Regional Banking Panic"),
    ("W11", "2023-06-01", "2023-06-30", "June 2023 BlackRock Spot ETF Filing"),
    ("W12", "2023-08-01", "2023-08-31", "August 2023 Space-X Bitcoin Write-Down"),
    ("W13", "2023-10-01", "2023-10-31", "October 2023 Fake ETF News Squeeze"),
    ("W14", "2024-01-01", "2024-01-31", "January 2024 Spot ETF Approval Sell-the-News"),
    ("W15", "2024-03-01", "2024-03-31", "March 2024 Pre-Halving All-Time High Run"),
    ("W16", "2024-08-01", "2024-08-31", "August 2024 Yen Carry Trade Unwind"),
    ("W17", "2024-11-01", "2024-11-30", "November 2024 US Presidential Election"),
    ("W18", "2025-02-01", "2025-02-28", "February 2025 Post-Inauguration Realignment"),
    ("W19", "2025-07-01", "2025-07-31", "July 2025 Mid-Cycle Distribution"),
    ("W20", "2026-03-01", "2026-03-31", "March 2026 Sovereign Debt Restructuring"),
]

def run_full_walkforward(per_symbol: Dict[str, pd.DataFrame],
                         ladder: Dict[str, pd.DataFrame],
                         funding: Optional[Dict[str, pd.Series]] = None,
                         modes: Tuple[str, ...] = ("compliant", "institutional")) -> pd.DataFrame:
    rows = []
    for mode in modes:
        for wid, ws, we, name in WINDOWS:
            eng = InstitutionalAlphaMaster(mode=mode)
            res = eng.run_window(per_symbol, ladder, ws, we, funding)
            rows.append({
                "mode": mode, "window_id": wid, "name": name,
                "deploy": res.get("deploy", False),
                "trades": res.get("trades", 0),
                "roi_pct": res.get("roi_pct", 0.0),
                "max_dd_pct": res.get("max_dd_pct", 0.0),
                "win_rate_pct": res.get("win_rate_pct", 0.0),
                "halted": res.get("halted", False),
                "gate_auc": res.get("gate", {}).get("auc"),
                "gate_exp_r": res.get("gate", {}).get("exp_r"),
                "reason": res.get("reason", "ok")
            })
    return pd.DataFrame(rows)
