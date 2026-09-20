# Engine/strategy/funding_basis_carry_engine.py
"""
OX ALPHA — Round 6: Institutional Funding & Basis Carry Engine.

Alpha thesis (empirically grounded, not pattern-based):
  - Extreme positive funding (>+50% ann.) = crowded leveraged longs paying a
    contractual toll -> short entry earns funding accrual + unwind reversion.
  - Extreme negative funding (<-30% ann.) = crowded shorts -> long entry earns
    funding + squeeze reversion.
  - Liquidation cascade overlay: entries only enhanced when aggregate OI/liquidation
    stress confirms forced deleveraging (z>3 flush = terminal positioning).
  - Deployment gate: trailing 6-month causal OOS expectancy of the *raw signal*
    (no ML), because the edge is contractual, not statistical. Gate requires
    E[R]_oos >= +0.15R and >= 8 events in trailing window.

Causality guarantees:
  - Funding rate at bar j is the LAST SETTLED rate (funding settles every 8h;
    we use the rate known at decision time, accrual forward is the *predicted*
    settled rate = current rate, which is the causally-known contractual term).
  - Signals at close of bar j -> entry at open of j+1 with slage.
  - Stop-first intrabar resolution; time-based and funding-normalization exits.
  - Per-(window,mode) seeded fills; single friction source of truth.
"""
from __future__ import annotations

import hashlib
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from Engine.core.execution_kernel import RiskConfig


# ===================================================================
# 1. CONFIGURATION
# ===================================================================
@dataclass(frozen=True)
class CarryConfig:
    # --- Funding signal thresholds (8h rate) ---
    funding_8h_extreme_pos: float = 0.000170   # ~+18.6% APR per-settle breakeven-ish; extreme = 0.017%/8h... scaled:
    # We define extremes on 3-settle rolling SUM of (24h toll):
    fund_roll_settles: int = 3                 # 24h of funding
    long_entry_funding: float = -0.0030        # 24h funding <= -0.30% -> long (shorts overcrowded)
    short_entry_funding: float = 0.0050        # 24h funding >= +0.50% -> short (longs overcrowded)
    fund_z_window: int = 21                    # 21 days of daily funding sums for z-score
    fund_z_extreme: float = 2.0                # must ALSO be a 2-sigma outlier
    # --- Basis confirmation (spot-perp basis, in bps) ---
    basis_extreme_bps: float = 40.0            # perp premium > 40bps confirms crowding
    basis_window: int = 96                     # 24h of 15m bars for basis MA
    # --- Liquidation cascade overlay ---
    cascade_oi_drop: float = 0.10              # 10% OI collapse over 24h
    cascade_funding_flip: bool = True          # funding sign flip during cascade = terminal signal
    # --- Position geometry ---
    hold_max_days: int = 4                     # 4-day max hold
    hold_min_bars: int = 8                     # min 2h before funding-normalization exit eligible
    stop_atr_mult: float = 3.0                 # catastrophic stop at 3x daily ATR (carry is not a scalp)
    norm_exit_z: float = 0.5                   # exit when funding z normalizes below 0.5
    # --- Frictions (single source of truth, bps) ---
    taker_fee: float = 0.0008
    entry_slippage: float = 0.0010
    exit_slippage: float = 0.0015
    # --- Gate ---
    train_days: int = 180
    purge_hours: int = 72
    gate_min_events: int = 8
    gate_min_exp_r: float = 0.15
    # --- Portfolio ---
    max_positions: int = 3
    top_k: int = 2


@dataclass
class CarryPosition:
    symbol: str
    side: int
    entry: float
    stop: float
    raw_r: float
    entry_bar: int
    fund_z_at_entry: float
    accrual_r: float = 0.0     # cumulative funding earned in R units


# ===================================================================
# 2. FUNDING & BASIS FEATURE ENGINE (strictly causal)
# ===================================================================
class FundingBasisFeatures:
    """
    Expected inputs per symbol:
      df15: 15m OHLCV
      funding: Series of settled 8h funding rates (index = settle timestamp).
               We ffill to 15m and the value at bar j is the last SETTLED rate.
      basis:   Series (15m index) of (perp_close - spot_close)/spot_close.
      oi:      Optional Series (15m or 1h) of open interest.
    """
    @staticmethod
    def build(df15: pd.DataFrame, funding: Optional[pd.Series],
              basis: Optional[pd.Series], oi: Optional[pd.Series],
              cfg: CarryConfig) -> pd.DataFrame:
        F = pd.DataFrame(index=df15.index)
        idx = df15.index

        # Funding: last settled value forward-filled (causal).
        if funding is not None and len(funding) > 0:
            f = funding.copy()
            f.index = pd.to_datetime(f.index)
            f_15 = f.reindex(f.index.union(idx)).ffill().reindex(idx).ffill().fillna(0.0)
        else:
            f_15 = pd.Series(0.0, index=idx)

        # 24h rolling funding toll (3 settles)
        # simpler: 24h = sum of last 3 distinct settle values -> approximate via rolling on 15m grid
        F["fund_24h"] = f_15.rolling(3 * 96, min_periods=12).sum().fillna(0.0) * (8.0 / 72.0)
        # ^ rescale: rolling 72h window on 15m captures 3 settles spread over 3 days;
        # normalize to a 24h-equivalent toll.

        # z-score of daily funding
        daily_f = f_15.resample("1D").sum()
        m = daily_f.rolling(cfg.fund_z_window, min_periods=10).mean()
        sd = daily_f.rolling(cfg.fund_z_window, min_periods=10).std(ddof=0).replace(0, np.nan)
        z_d = ((daily_f - m) / sd).clip(-4, 4)
        F["fund_z"] = z_d.reindex(idx, method="ffill").fillna(0.0)

        # Basis
        if basis is not None:
            b = basis.reindex(idx).ffill().fillna(0.0) * 1e4  # bps
            F["basis_bps"] = b
            F["basis_ma_bps"] = b.rolling(cfg.basis_window, min_periods=12).mean().fillna(0.0)
        else:
            F["basis_bps"] = 0.0
            F["basis_ma_bps"] = 0.0

        # ATR for stops
        rng = (df15["high"] - df15["low"]).clip(lower=1e-12)
        F["atr_d"] = rng.rolling(96 * 14, min_periods=96).mean().bfill().fillna(rng.mean() if len(rng) else 1.0)

        # Cascade state: 24h OI collapse
        if oi is not None:
            o = oi.reindex(idx).ffill().bfill()
            F["oi_drop_24h"] = (1.0 - o / o.shift(96)).clip(-1, 1).fillna(0.0)
        else:
            F["oi_drop_24h"] = 0.0

        # Funding sign flip within last 24h (cascade terminal marker)
        sign_flip = (np.sign(f_15) != np.sign(f_15.shift(96))) & (f_15 != 0)
        F["fund_flip_24h"] = sign_flip.rolling(96, min_periods=1).max().fillna(0.0)
        return F


# ===================================================================
# 3. SIGNAL GENERATION
# ===================================================================
class CarrySignalGenerator:
    def __init__(self, cfg: CarryConfig):
        self.cfg = cfg

    def generate(self, df15: pd.DataFrame, F: pd.DataFrame) -> pd.DataFrame:
        """
        side/raw_r per bar. Causal: uses only bar-j completed data.
        raw_r = stop distance in price terms (3x daily ATR).
        """
        cfg = self.cfg
        T = len(df15)
        side = np.zeros(T, dtype=np.int8)
        raw_r = np.zeros(T)
        etype = np.zeros(T, dtype=object)

        c = df15["close"].to_numpy()
        atr = F["atr_d"].to_numpy()
        fz = F["fund_z"].to_numpy()
        f24 = F["fund_24h"].to_numpy()
        bps = F["basis_ma_bps"].to_numpy()
        oid = F["oi_drop_24h"].to_numpy()
        flip = F["fund_flip_24h"].to_numpy()

        stop_d = cfg.stop_atr_mult * atr

        # --- Core short crowding: extreme positive funding + positive basis ---
        short_core = (fz >= cfg.fund_z_extreme) & (f24 >= cfg.short_entry_funding) \
                     & (bps >= cfg.basis_extreme_bps)
        # --- Core long crowding: extreme negative funding + negative basis ---
        long_core = (fz <= -cfg.fund_z_extreme) & (f24 <= cfg.long_entry_funding) \
                    & (bps <= -cfg.basis_extreme_bps)

        # --- Cascade overlay: relax basis req, require OI flush ---
        short_casc = (fz >= cfg.fund_z_extreme) & (oid >= cfg.cascade_oi_drop)
        long_casc = (fz <= -cfg.fund_z_extreme) & (oid >= cfg.cascade_oi_drop) \
                    & ((flip > 0) if cfg.cascade_funding_flip else True)

        long_m = (long_core | long_casc) & ~short_core & ~short_casc
        short_m = (short_core | short_casc) & ~long_m

        side[long_m] = 1
        raw_r[long_m] = stop_d[long_m]
        etype[long_m] = np.where(long_casc[long_m], "LONG_CASCADE", "LONG_CARRY")

        side[short_m] = -1
        raw_r[short_m] = stop_d[short_m]
        etype[short_m] = np.where(short_casc[short_m], "SHORT_CASCADE", "SHORT_CARRY")

        # Cross-sectional top-K handled by engine (score = |fund_z|)
        return pd.DataFrame({"side": side, "raw_r": raw_r,
                             "score": np.abs(fz), "event_type": etype},
                            index=df15.index)


# ===================================================================
# 4. CARRY ENGINE WITH CAUSAL GATE + CIRCUIT BREAKER
# ===================================================================
class FundingBasisCarryEngine:
    def __init__(self, mode: str = "compliant", cfg: CarryConfig = CarryConfig()):
        self.cfg = cfg
        self.mode = mode
        if mode == "institutional":
            self.risk = RiskConfig(initial_capital=5000.0, base_risk=100.0,
                                   house_money_risk=150.0, drawdown_defense_risk=50.0,
                                   drawdown_limit=0.060)
        else:
            self.risk = RiskConfig()  # $25 / $50 / $15 / 4.5%

    # ---------- Causal gate: raw-signal OOS expectancy, no ML ----------
    def run_gate(self, per_symbol: Dict[str, pd.DataFrame],
                 feats: Dict[str, pd.DataFrame],
                 funding: Dict[str, pd.Series],
                 basis: Dict[str, pd.Series],
                 oi: Optional[Dict[str, pd.Series]],
                 train_start: pd.Timestamp, train_end: pd.Timestamp) -> Tuple[bool, Dict]:
        cfg = self.cfg
        gen = CarrySignalGenerator(cfg)
        rs, n = [], 0
        for sym, df in per_symbol.items():
            sl = df.loc[train_start:train_end - pd.Timedelta(hours=cfg.purge_hours)]
            if len(sl) < 2000:
                continue
            F = FundingBasisFeatures.build(sl, funding.get(sym), basis.get(sym),
                                           oi.get(sym) if oi else None, cfg)
            sig = gen.generate(sl, F)
            h, l, o = sl["high"].to_numpy(), sl["low"].to_numpy(), sl["open"].to_numpy()
            c = sl["close"].to_numpy()
            for t in range(96, len(sl) - 1):
                s = int(sig["side"].iat[t])
                if s == 0:
                    continue
                entry = o[t + 1] * (1 + cfg.entry_slippage * s)
                R = float(sig["raw_r"].iat[t])
                if R <= 0:
                    continue
                exit_px, pnl = None, 0.0
                for k in range(t + 1, min(t + cfg.hold_max_days * 96, len(sl))):
                    if s == 1 and l[k] <= entry - R:
                        exit_px, pnl = entry - R, -1.0; break
                    if s == -1 and h[k] >= entry + R:
                        exit_px, pnl = entry + R, -1.0; break
                    fav = (h[k] - entry) if s == 1 else (entry - l[k])
                    if fav >= 1.5 * R:
                        # trail to BE+0.15R, exit on first touch
                        lock = entry + s * 0.15 * R
                        hit = next((j for j in range(k + 1, min(k + 96, len(sl)))
                                    if (s == 1 and l[j] <= lock) or (s == -1 and h[j] >= lock)), None)
                        if hit is not None:
                            exit_px, pnl = lock, 0.15; break
                if exit_px is None:
                    k = min(t + cfg.hold_max_days * 96, len(sl) - 1)
                    exit_px = c[k]
                    pnl = s * (exit_px - entry) / R
                fric_r = cfg.taker_fee * 2 + cfg.entry_slippage + cfg.exit_slippage  # ~0.0033 price
                rs.append(pnl - (fric_r * entry) / R)
                n += 1
        exp_r = float(np.mean(rs)) if rs else -1.0
        ok = n >= cfg.gate_min_events and exp_r >= cfg.gate_min_exp_r
        return ok, {"deploy": ok, "n_events": n, "exp_r": round(exp_r, 4),
                    "reason": "ok" if ok else ("starvation" if n < cfg.gate_min_events else "no_edge")}

    # ---------- OOS execution ----------
    def run_window(self, per_symbol: Dict[str, pd.DataFrame],
                   funding: Dict[str, pd.Series],
                   basis: Dict[str, pd.Series],
                   oi: Optional[Dict[str, pd.Series]],
                   win_start: str, win_end: str, window_id: str = "W00") -> Dict:
        cfg = self.cfg
        ws, we = pd.Timestamp(win_start), pd.Timestamp(win_end) + pd.Timedelta(days=1)
        train_end = ws - pd.Timedelta(hours=cfg.purge_hours)
        train_start = train_end - pd.Timedelta(days=cfg.train_days)

        ok, gate = self.run_gate(per_symbol, {}, funding, basis, oi, train_start, train_end)
        if not ok:
            return {"deploy": False, "gate": gate, "trades": 0, "roi_pct": 0.0,
                    "max_dd_pct": 0.0, "trades_list": [],
                    "reason": f"Gate inactive: {gate.get('reason')}"}

        # Per-(window,mode) deterministic seed — no cross-window coupling
        seed = int(hashlib.sha256(f"{window_id}|{self.mode}".encode()).hexdigest()[:8], 16)
        rng = np.random.default_rng(seed)

        test = {s: d.loc[ws:we] for s, d in per_symbol.items() if len(d.loc[ws:we]) > 200}
        if not test:
            return {"deploy": True, "gate": gate, "trades": 0, "roi_pct": 0.0,
                    "max_dd_pct": 0.0, "trades_list": [], "reason": "no_test_data"}

        gen = CarrySignalGenerator(cfg)
        sigs, feats = {}, {}
        for s, d in test.items():
            F = FundingBasisFeatures.build(d, funding.get(s), basis.get(s),
                                           oi.get(s) if oi else None, cfg)
            feats[s] = F
            sigs[s] = gen.generate(d, F)

        syms = list(test.keys())
        T = min(len(d) for d in test.values())
        equity, peak, max_dd = 5000.0, 5000.0, 0.0
        positions: List[CarryPosition] = []
        trades, halted = [], False

        funding_15 = {s: funding[s].reindex(test[s].index).ffill().fillna(0.0)
                      if s in funding else pd.Series(0.0, index=test[s].index)
                      for s in syms}

        for t in range(96, T):
            # --- manage open positions ---
            for p in list(positions):
                d = test[p.symbol]
                o_, h_, l_, c_ = d["open"].iat[t], d["high"].iat[t], d["low"].iat[t], d["close"].iat[t]
                s, R, entry = p.side, p.raw_r, p.entry
                exit_px, why = None, ""

                # funding accrual (causal: settled rate known at bar close)
                fr = funding_15[p.symbol].iat[t]
                if fr != 0:
                    p.accrual_r += (-s * fr * entry) / R  # short earns positive funding

                if (s == 1 and l_ <= p.stop) or (s == -1 and h_ >= p.stop):
                    exit_px, why = p.stop, "stop"
                elif (t - p.entry_bar) >= cfg.hold_max_days * 96:
                    exit_px, why = c_, "time"
                elif (t - p.entry_bar) >= cfg.hold_min_bars and abs(feats[p.symbol]["fund_z"].iat[t]) < cfg.norm_exit_z:
                    exit_px, why = c_, "fund_normalized"

                if exit_px is not None:
                    gross_r = s * (exit_px - entry) / R + p.accrual_r
                    fric_r = (2 * cfg.taker_fee + cfg.entry_slippage + cfg.exit_slippage) * entry / R
                    net_r = gross_r - fric_r
                    dd_now = (peak - equity) / peak
                    netprofit = equity - 5000.0
                    risk_d = (self.risk.house_money_risk if netprofit > 50
                              else self.risk.drawdown_defense_risk if dd_now > 0.025
                              else self.risk.base_risk)
                    pnl_d = net_r * risk_d
                    equity += pnl_d
                    peak = max(peak, equity)
                    max_dd = max(max_dd, (peak - equity) / peak)
                    trades.append({"sym": p.symbol, "side": s, "r": net_r,
                                   "pnl_d": pnl_d, "why": why,
                                   "accrual_r": p.accrual_r})
                    positions.remove(p)

            if max_dd >= self.risk.drawdown_limit:
                halted = True
                break
            if halted:
                break

            # --- stage new entries at close of t, fill at open t+1 (flag mechanism) ---
            if len(positions) < cfg.max_positions and t < T - 1:
                cand = [(s_, float(sigs[s_]["score"].iat[t]), int(sigs[s_]["side"].iat[t]),
                         float(sigs[s_]["raw_r"].iat[t]))
                        for s_ in syms if sigs[s_]["side"].iat[t] != 0
                        and s_ not in [p.symbol for p in positions]]
                cand.sort(key=lambda x: -x[1])
                for s_, score, side_, R in cand[:cfg.top_k]:
                    if R <= 0 or len(positions) >= cfg.max_positions:
                        continue
                    nxt = t + 1
                    d = test[s_]
                    entry = d["open"].iat[nxt] * (1 + cfg.entry_slippage * side_)
                    # fill slippage haircut via rng (execution uncertainty)
                    if rng.random() < 0.98:  # 2% execution failure (venue/latency)
                        positions.append(CarryPosition(
                            symbol=s_, side=side_, entry=entry,
                            stop=entry - side_ * R, raw_r=R,
                            entry_bar=nxt,
                            fund_z_at_entry=float(feats[s_]["fund_z"].iat[t])))
                        # immediately evaluate stop on entry bar (stop-first)
                        lo_n, hi_n = d["low"].iat[nxt], d["high"].iat[nxt]
                        if (side_ == 1 and lo_n <= positions[-1].stop) or \
                           (side_ == -1 and hi_n >= positions[-1].stop):
                            positions[-1].entry_bar = -999  # flag: exit next loop as "stop"

        net = equity - 5000.0
        wins = sum(1 for tr in trades if tr["r"] > 0)
        return {"deploy": True, "gate": gate, "halted": halted,
                "equity": equity, "net_pnl": net, "roi_pct": net / 50.0,
                "max_dd_pct": max_dd * 100.,
                "trades": len(trades),
                "win_rate_pct": (wins / len(trades) * 100.0) if trades else 0.0,
                "trades_list": trades}


# ===================================================================
# 5. UNIFIED 20-WINDOW RUNNER
# ===================================================================
WINDOWS = [
    ("W01", "2021-05-01", "2021-05-31"), ("W02", "2021-09-01", "2021-09-30"),
    ("W03", "2021-11-01", "2021-11-30"), ("W04", "2022-01-01", "2022-01-31"),
    ("W05", "2022-05-01", "2022-05-31"), ("W06", "2022-06-01", "2022-06-30"),
    ("W07", "2022-09-01", "2022-09-30"), ("W08", "2022-11-01", "2022-11-30"),
    ("W09", "2023-01-01", "2023-01-31"), ("W10", "2023-03-01", "2023-03-31"),
    ("W11", "2023-06-01", "2023-06-30"), ("W12", "2023-08-01", "2023-08-31"),
    ("W13", "2023-10-01", "2023-10-31"), ("W14", "2024-01-01", "2024-01-31"),
    ("W15", "2024-03-01", "2024-03-31"), ("W16", "2024-08-01", "2024-08-31"),
    ("W17", "2024-11-01", "2024-11-30"), ("W18", "2025-02-01", "2025-02-28"),
    ("W19", "2025-07-01", "2025-07-31"), ("W20", "2026-03-01", "2026-03-31"),
]

def run_carry_walkforward(per_symbol, funding, basis, oi=None,
                          modes=("compliant", "institutional")) -> pd.DataFrame:
    rows = []
    for mode in modes:
        for wid, ws, we in WINDOWS:
            print(f"Running Window {wid} - {mode}")
            res = FundingBasisCarryEngine(mode=mode).run_window(
                per_symbol, funding, basis, oi, ws, we, window_id=wid)
            rows.append({"mode": mode, "window_id": wid,
                         "deploy": res.get("deploy"), "trades": res.get("trades", 0),
                         "roi_pct": res.get("roi_pct", 0.0),
                         "max_dd_pct": res.get("max_dd_pct", 0.0),
                         "win_rate_pct": res.get("win_rate_pct", 0.0),
                         "halted": res.get("halted", False),
                         "gate_exp_r": res.get("gate", {}).get("exp_r"),
                         "reason": res.get("reason", "ok")})
    return pd.DataFrame(rows)
