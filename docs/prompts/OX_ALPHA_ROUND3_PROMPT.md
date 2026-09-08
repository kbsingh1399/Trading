# OX ALPHA — ROUND 3 MASTER QUANT CONSULTATION PROMPT

> **TO BE PASTED INTO A FRESH SESSION AT OXALPHA.COM/CHAT**
> **ROLE**: Elite Quantitative Portfolio Manager, Microstructure Researcher & Machine Learning Engineer.
> **OBJECTIVE**: Review Round 2 empirical backtest results, solve the CV-AUC = 0.502 meta-labeling barrier, and engineer high-expectancy alpha on the 18-asset Binance USDT-M institutional backtest universe across 20 Out-of-Sample (OOS) windows.

---

## 1. EXECUTIVE CONTEXT & ROUND 2 RECAP

We are optimizing a quantitative crypto trading system across **18 Binance USDT-M Perpetual assets** (`BTC, ETH, XRP, SOL, BNB, DOGE, ADA, TRX, LINK, AVAX, SUI, NEAR, DOT, LTC, BCH, APT, OP, ARB`), consisting of **3,467,571 continuous 15-minute bars (2020–2026, 0 nulls, monotonic timestamps)**.

### Target Validation Criteria Across 20 OOS 1-Month Windows:
- **Min ROI**: `> 20.0%` per window
- **Max Drawdown**: `< 5.0%` (Hard circuit breaker: `4.5%` / `$225` on `$5,000` capital)
- **Min Win Rate**: `> 40.0%`
- **Min Trade Count**: `>= 6` trades per window
- **Strict Real-World Frictions**: 8 bps taker fee, 10 bps entry slippage, 15 bps exit slippage (33 bps round-trip).
- **Execution**: Signal at bar $j$ close $\to$ filled at `Open[j+1]`. Stop-first intrabar ambiguity check.

---

## 2. ROUND 2 IMPLEMENTATION & EMPIRICAL BACKTEST RESULTS

We implemented all three Round 2 modules exactly as specified:
1. `PooledInstitutionalMetaLabeler` in `Engine/ml/pooled_meta_labeler.py`.
2. `PortfolioExecutionKernel` in `Engine/core/portfolio_execution_kernel.py` (max 2 concurrent positions, shared $5k equity, 4.5% DD breaker).
3. `MultiAssetWalkForwardRunner` in `Engine/runners/multi_asset_walk_forward_runner.py`.

### Empirical Run: Window 1 (May 2021 Great Liquidation Crash: 2021-05-01 -> 2021-05-31)
Here are the exact numbers from the live execution log:

```
>>> Loading 18 institutional asset parquets...
>>> Successfully loaded 18 symbols in 6.77s.

================================================================================
>>> RUNNING WINDOW 1 FOR S1 (LIQUIDATION CASCADE) <<<
================================================================================
W01 | 2021-05-01 -> 2021-05-31 | N  25 | PnL    -84.58$ | ROI   -1.69% | DD  4.71% | WR  44.0% | AUC 0.502 | tau 0.564 | FAIL

Window 1 Result Summary:
  window_id: 1
  name: May 2021 Great Liquidation Crash
  start_date: 2021-05-01
  end_date: 2021-05-31
  trades: 25
  net_pnl: -84.58$
  roi_pct: -1.69%
  max_dd_pct: 4.71%
  win_rate_pct: 44.0%
  passed: False (Failed ROI > 20%)
  cv_auc: 0.5015
  tau: 0.5642
  n_train_events: 1886
  pos_rate: 0.3871
```

---

## 3. DEEP FORENSIC DIAGNOSTIC OF THE 0.502 CV-AUC

The cross-asset pooling worked as intended for sample depth:
- **1,886 training events** pooled across all 18 symbols in the trailing 365-day training window (with a 72-hour causal purge gap).
- Base positive rate (reaching +2.5R before -1.0R): **38.71%**.
- However, **CV-AUC across the 5 purged folds was 0.5015** (0.531, 0.509, 0.435, 0.518, 0.515). The GBDT model has virtually zero rank-ordering discrimination.

### XGBoost Feature Importances on the 1,886 Pooled Events:
```
dist_to_vwap_zs    0.0908
fp_delta_ratio     0.0870
atr_norm_zs        0.0860
body_ratio         0.0859
atr_norm           0.0856
ret_zs             0.0843
close_pos          0.0831
rsi_c              0.0817
volume_ratio       0.0816
short_liq_zs       0.0799
long_liq_zs        0.0792
cvd_zs             0.0749
zc_div             0.0000
```
Notice: Every single feature has ~8% importance (completely uniform, meaning the tree splits randomly without finding strong signal nodes), and `zc_div` has 0.0000 importance because S1's primary rule already hard-filtered `zc_div > 0.8`.

### Raw Correlation with Binary Label $y \in \{0, 1\}$:
```
zc_div             +0.0625
atr_norm           +0.0584
long_liq_zs        +0.0501
volume_ratio       -0.0154
fp_delta_ratio     -0.0170
atr_norm_zs        -0.0265
cvd_zs             -0.0387
close_pos          -0.0624
body_ratio         -0.0665
short_liq_zs       -0.0675
ret_zs             -0.0728
rsi_c              -0.0740
dist_to_vwap_zs    -0.0778
```

### Direction Alignment Experiment:
We hypothesized that signed market features (`dist_to_vwap_zs`, `cvd_zs`, `ret_zs`, `body_ratio`) were canceling out because Long trades (1,105 events, 41.3% win rate) and Short trades (781 events, 35.1% win rate) were mixed together into a single binary classifier.
We tested multiplying signed features by `side` (`feature * side`) and splitting liquidation into `trigger_liq_zs` vs `counter_liq_zs`.
**Result**: Mean CV-AUC was **0.4864** (Fold AUCs: [0.551, 0.504, 0.463, 0.490, 0.423]).
The individual feature correlations with $y$ collapsed even further toward zero (-0.03 to +0.03).

---

## 4. THE CORE QUANTITATIVE QUESTIONS FOR ROUND 3

1. **Why do standard 15m rolling features fail to separate winning from losing liquidation cascades?**
   - After a massive long liquidation spike (`long_liq_zs > 1.8`), why is rolling CVD z-score, volume ratio, or distance to VWAP uninformative about whether price will bounce +2.5R or continue capitulating?
   
2. **Footprint Ladder Exploitation**:
   - In our dataset, each asset has a companion `{symbol}_15m_footprint_ladder.parquet` file containing granular price-bin order flow:
     `open_time_ms, price_bin, bid_vol_coin, ask_vol_coin, delta_vol_coin, bid_trade_count, ask_trade_count`.
   - How can we aggregate the footprint ladder into stationary, high-signal features that detect **trapped seller absorption** (e.g., massive sell volume hitting bids at the candle low without pushing price lower, followed by delta divergence)?

3. **Primary Signal vs Secondary Gate Reformulation**:
   - Is S1's primary entry rule (`long_liq_zs > 1.8 & zc_div > 0.8 & spot > 0 & futures < 0 & rsi < 40 & vwap < -0.5`) too rigid, or entering too early (on the flush candle rather than the absorption/reclaim candle)?
   - Should the primary signal trigger on the **liquidation flush**, but the execution kernel wait for a **confirmation/reclaim bar**?

4. **Exit Target Geometry & Expectancy**:
   - In W01, the strategy achieved a **44.0% win rate** and **4.71% max DD**, but lost **-$84.58** due to 33 bps frictions and time-decay exits.
   - At +2.5R target / -1.0R stop with 24-bar time decay, what is the optimal exit ratchet geometry to convert a 44% win rate into a positive ROI?

---

## 5. CURRENT CODEBASE IN PRODUCTION

### A. `Engine/ml/pooled_meta_labeler.py`
```python
from __future__ import annotations
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

try:
    from xgboost import XGBClassifier
    _BACKEND = "xgb"
except ImportError:
    from lightgbm import LGBMClassifier
    _BACKEND = "lgbm"

@dataclass(frozen=True)
class BarrierConfig:
    tp_r: float = 2.50
    sl_r: float = 1.00
    vertical_bars: int = 24
    min_terminal_r: float = 0.20

@dataclass(frozen=True)
class CVConfig:
    n_folds: int = 6
    purge_hours: int = 72      # 288 bars @15m
    embargo_hours: int = 24    # 96 bars @15m
    min_train_events: int = 100

@dataclass(frozen=True)
class ModelConfig:
    max_depth: int = 4
    min_child_weight: int = 8
    reg_alpha: float = 1.5
    reg_lambda: float = 3.5
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    learning_rate: float = 0.03
    n_estimators: int = 600
    random_state: int = 42

@dataclass(frozen=True)
class GateConfig:
    quantile_grid: Tuple[float, ...] = (0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80)
    min_trades_per_window: int = 6
    bars_per_month: int = 2880

class PooledInstitutionalMetaLabeler:
    def __init__(self,
                 barrier: BarrierConfig = BarrierConfig(),
                 cv: CVConfig = CVConfig(),
                 model: ModelConfig = ModelConfig(),
                 gate: GateConfig = GateConfig()):
        self.barrier = barrier
        self.cv_cfg = cv
        self.model_cfg = model
        self.gate = gate
        self.model_: Optional[object] = None
        self.oof_: Optional[pd.DataFrame] = None
        self.tau_: float = 0.50
        self.fold_aucs_: List[float] = []
        self.feat_cols_: List[str] = []

    def build_features(self, df: pd.DataFrame) -> pd.DataFrame:
        T = len(df)
        idx = df.index
        get = lambda n, d: df.get(n, pd.Series(d, index=idx)).astype(np.float64)
        cl = df["close"].astype(np.float64)
        atr = get("atr_14", cl * 0.002).clip(lower=1e-12)
        vol = get("volume_base", get("volume", pd.Series(np.ones(T), index=idx))).clip(lower=1e-12)
        F = pd.DataFrame(index=idx)

        # Footprint taker delta ratio
        if "taker_buy_vol_btc" in df.columns and "taker_sell_vol_btc" in df.columns:
            tb = df["taker_buy_vol_btc"].astype(np.float64)
            ts = df["taker_sell_vol_btc"].astype(np.float64)
            F["fp_delta_ratio"] = ((tb - ts) / (tb + ts).clip(lower=1e-12)).rolling(12, min_periods=1).mean().fillna(0.0)
        elif "taker_buy_volume" in df.columns:
            tb = df["taker_buy_volume"].astype(np.float64)
            ts = (vol - tb).clip(lower=0.0)
            F["fp_delta_ratio"] = ((tb - ts) / (tb + ts).clip(lower=1e-12)).rolling(12, min_periods=1).mean().fillna(0.0)
        else:
            F["fp_delta_ratio"] = pd.Series(0.0, index=idx)

        cvd = get("future_cvd_15m", pd.Series(np.zeros(T), index=idx))
        d_cvd = cvd.diff().fillna(0.0)
        m = d_cvd.rolling(96, min_periods=1).mean()
        s = d_cvd.rolling(96, min_periods=1).std(ddof=0).clip(lower=1e-12).fillna(1.0)
        F["cvd_zs"] = ((d_cvd - m) / s).clip(-10, 10).fillna(0.0)

        F["long_liq_zs"] = get("long_liq_zs", np.zeros(T)).clip(-10, 10).fillna(0.0)
        F["short_liq_zs"] = get("short_liq_zs", np.zeros(T)).clip(-10, 10).fillna(0.0)
        zc = get("zc_div", pd.Series(np.zeros(T), index=idx))
        F["zc_div"] = zc.clip(-5, 5).fillna(0.0)

        rsi = get("rsi_14", pd.Series(np.full(T, 50.0), index=idx))
        F["rsi_c"] = ((rsi - 50.0) / 50.0).fillna(0.0)

        vwz = df.get("dist_to_vwap_zs", df.get("vwap_zscore", pd.Series(np.zeros(T), index=idx))).astype(np.float64)
        F["dist_to_vwap_zs"] = vwz.clip(-10, 10).fillna(0.0)

        atr_n = (atr / cl).clip(0, 0.05)
        F["atr_norm"] = atr_n.fillna(0.002)
        m2 = atr_n.rolling(96, min_periods=1).mean()
        s2 = atr_n.rolling(96, min_periods=1).std(ddof=0).clip(lower=1e-12).fillna(1.0)
        F["atr_norm_zs"] = ((atr_n - m2) / s2).clip(-10, 10).fillna(0.0)

        vol_base = vol.rolling(96, min_periods=1).mean().clip(lower=1e-12)
        F["volume_ratio"] = (vol / vol_base).clip(0, 10).fillna(1.0)

        rng = (df["high"] - df["low"]).clip(lower=1e-12)
        F["body_ratio"] = ((cl - df["open"]) / rng).clip(-1, 1).fillna(0.0)
        F["close_pos"] = ((cl - df["low"]) / rng * 2.0 - 1.0).clip(-1, 1).fillna(0.0)

        r1 = np.log(cl.clip(lower=1e-12)).diff().fillna(0.0)
        m3 = r1.rolling(96, min_periods=1).mean()
        s3 = r1.rolling(96, min_periods=1).std(ddof=0).clip(lower=1e-12).fillna(1.0)
        F["ret_zs"] = ((r1 - m3) / s3).clip(-10, 10).fillna(0.0)
        return F

    def triple_barrier_labels(self, df: pd.DataFrame, event_mask: np.ndarray,
                              side: np.ndarray, r_dist: np.ndarray) -> pd.DataFrame:
        op, hi, lo, cl = (df[c].values for c in ("open", "high", "low", "close"))
        B = self.barrier
        events = np.flatnonzero(event_mask)
        n = len(df)
        y = np.zeros(len(events), dtype=np.int8)
        t_out = np.zeros(len(events), dtype=np.int64)
        exit_r = np.zeros(len(events), dtype=np.float64)

        for k, t in enumerate(events):
            entry = op[t + 1] if t + 1 < n else cl[t]
            d = max(r_dist[t], 1e-12)
            up = entry + side[t] * B.tp_r * d
            dn = entry - side[t] * B.sl_r * d
            end = min(t + B.vertical_bars, n - 1)
            hit, tout, xr = 0, end, 0.0
            for j in range(t + 1, end + 1):
                stop_hit = lo[j] <= dn if side[t] == 1 else hi[j] >= dn
                tgt_hit = hi[j] >= up if side[t] == 1 else lo[j] <= up
                if stop_hit:                       # conservative stop-first
                    hit, tout, xr = 0, j, -B.sl_r
                    break
                if tgt_hit:
                    hit, tout, xr = 1, j, B.tp_r
                    break
            else:
                xr = side[t] * (cl[end] - entry) / d
                hit = 1 if xr >= B.min_terminal_r else 0
            y[k], t_out[k], exit_r[k] = hit, tout, xr
        return pd.DataFrame({"y_meta": y, "t_out": t_out, "exit_r": exit_r}, index=events)

    def pool_events(self, per_symbol: Dict[str, pd.DataFrame],
                    strategy, train_start: pd.Timestamp,
                    train_end: pd.Timestamp) -> pd.DataFrame:
        frames = []
        for sym, df_sym in per_symbol.items():
            sl = df_sym.loc[train_start:train_end]
            if len(sl) < self.barrier.vertical_bars + 48:
                continue
            sig = strategy.generate_signals(sl.copy())
            mask = sig["side"].to_numpy() != 0
            if mask.sum() < 10:
                continue
            side = np.where(mask, sig["side"].to_numpy(), 1).astype(np.int8)
            labels = self.triple_barrier_labels(sl, mask, side, sig["raw_r"].to_numpy())
            ev = labels.index.to_numpy()
            X = self.build_features(sl).iloc[ev]
            tab = X.reset_index(drop=True)
            tab["symbol"] = sym
            tab["bar_pos"] = ev
            tab["abs_bar"] = df_sym.index.get_indexer(sl.index)[ev]
            tab["y"] = labels["y_meta"].to_numpy()
            tab["t_out"] = labels["t_out"].to_numpy()
            tab["exit_r"] = labels["exit_r"].to_numpy()
            frames.append(tab)
        if not frames:
            raise RuntimeError("PooledMetaLabeler: zero events pooled across symbols.")
        pooled = pd.concat(frames, ignore_index=True)
        feat_cols = [c for c in pooled.columns if c not in ("symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r")]
        pooled[feat_cols] = pooled[feat_cols].clip(-15, 15)
        return pooled

    def _cv_splits(self, pooled: pd.DataFrame) -> List[Tuple[np.ndarray, np.ndarray]]:
        C, B = self.cv_cfg, self.barrier
        purge = (C.purge_hours * 60) // 15
        embargo = (C.embargo_hours * 60) // 15
        edges = np.quantile(pooled["abs_bar"].to_numpy(),
                            np.linspace(0, 1, C.n_folds + 1)).astype(int)
        edges = np.unique(edges)
        splits = []
        for f in range(len(edges) - 2, -1, -1):
            t0, t1 = edges[f], edges[f + 1]
            te = pooled.index[(pooled["abs_bar"] >= t0) & (pooled["abs_bar"] < t1)].to_numpy()
            tr = pooled.index[pooled["abs_bar"] < t0 - purge - embargo].to_numpy()
            tr = tr[~((pooled.loc[tr, "abs_bar"] + B.vertical_bars >= t0 - purge))]
            if len(tr) >= C.min_train_events and len(te) >= 10:
                splits.append((tr, te))
        return splits

    def fit(self, pooled: pd.DataFrame) -> Dict:
        from sklearn.metrics import roc_auc_score
        feat_cols = [c for c in pooled.columns if c not in ("symbol", "bar_pos", "abs_bar", "y", "t_out", "exit_r")]
        X_all = pooled[feat_cols].to_numpy(np.float64)
        y_all = pooled["y"].to_numpy(np.int8)
        r_all = pooled["exit_r"].to_numpy(np.float64)
        t_all = pooled["abs_bar"].to_numpy()

        oof = np.full(len(pooled), np.nan)
        self.fold_aucs_ = []
        for tr, te in self._cv_splits(pooled):
            mdl = self._make_model()
            mdl.fit(X_all[tr], y_all[tr])
            oof[te] = mdl.predict_proba(X_all[te])[:, 1]
            if len(np.unique(y_all[te])) > 1:
                self.fold_aucs_.append(float(roc_auc_score(y_all[te], oof[te])))

        valid = np.isfinite(oof)
        self.tau_ = self._calibrate_tau(oof[valid], y_all[valid], r_all[valid])
        self.model_ = self._make_model()
        self.model_.fit(X_all, y_all)
        self.feat_cols_ = feat_cols
        return {
            "n_events": int(len(pooled)),
            "positive_rate": float(y_all.mean()),
            "mean_cv_auc": float(np.mean(self.fold_aucs_)) if self.fold_aucs_ else float("nan"),
            "fold_aucs": self.fold_aucs_,
            "calibrated_tau": self.tau_,
            "oof_expectancy_all": float(r_all[valid].mean()),
        }

    def _calibrate_tau(self, p: np.ndarray, y: np.ndarray, r: np.ndarray) -> float:
        best_tau, best_exp = 1.0, -np.inf
        for q in sorted(self.gate.quantile_grid):
            tau = float(np.quantile(p, q))
            sel = p >= tau
            n_sel = int(sel.sum())
            if n_sel < self.gate.min_trades_per_window:
                continue
            exp = float(r[sel].mean())
            monthly_events = len(p) / 12.0
            expected_trades = monthly_events * (1.0 - q)
            if exp > best_exp and expected_trades >= self.gate.min_trades_per_window:
                best_exp, best_tau = exp, tau
        if best_exp <= 0:
            return 1.0
        return best_tau
```

---

## 6. REQUIRED ROUND 3 DELIVERABLES

Please deliver actionable, production-grade solutions:

1. **Root-Cause Analysis of Zero AUC**: Why do rolling indicators produce zero rank-order discrimination on post-liquidation bars? What is the actual missing signal?
2. **Order Flow & Footprint Ladder Feature Extractor**: Provide a self-contained Python function that consumes the `{symbol}_15m_footprint_ladder.parquet` dataset and computes true microstructural absorption features (e.g., trapped volume at wick extremes, bid/ask absorption ratios, delta divergences).
3. **Refined Meta-Labeling Model Architecture**: How to update `PooledInstitutionalMetaLabeler` to reach **CV-AUC > 0.58** on out-of-fold validation without lookahead.
4. **Primary Strategy Upgrade**: Concrete code revisions for `Engine/strategy/s1_liquidation_cascade.py` to ensure high-conviction entries that clear the +20% ROI bar after frictions.
