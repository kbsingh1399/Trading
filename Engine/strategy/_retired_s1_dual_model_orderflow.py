"""
################################################################################
#                                                                              #
#   RETIRED 2026-09-16  --  S1 15m DUAL-MODEL ML SLEEVE. DO NOT USE.           #
#                                                                              #
#   Kept ONLY so the S1 teardown (scratch/diag_s1_autopsy.py) and the committed #
#   historical ledgers stay reproducible. No live path imports this module.    #
#                                                                              #
#   Why it was retired (S1_TEARDOWN.md, 52,252 candidates, 18 symbols):        #
#     * GROSS expectancy +0.0058 R, t = +0.85, p = 0.396. The entry signal is  #
#       statistically indistinguishable from a coin flip. Setting transaction  #
#       costs to exactly 0.0 bps would still not make it profitable.           #
#     * Its risk unit, the 15m ATR-14, is a median 0.527% of price -- SMALLER  #
#       than the 0.410% round trip. Friction was 0.779 R, i.e. 64.9% of the    #
#       1.2R stop was consumed before price moved at all.                      #
#     * OOS AUC 0.5217 against in-sample 0.8592. The strongest feature,        #
#       vol_strain, correlates +0.1027 with the label but only +0.0142 with    #
#       the GROSS outcome and -0.4865 with fric_r: the model learned the cost  #
#       function, not the market.                                              #
#                                                                              #
#   The surviving sleeve is Engine/strategy/t1_breakout.py (4h Donchian).      #
#   T1 generation below now DELEGATES to that module so there is exactly one   #
#   copy of the T1 logic in the repository.                                    #
#                                                                              #
################################################################################
"""


from __future__ import annotations
from pathlib import Path
from typing import Tuple, Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

import sys as _sys
from pathlib import Path as _Path
_ROOT = _Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))
from Engine.execution_costs import ROUND_TRIP_BPS, ROUND_TRIP_FRAC, build_stress_series
import lightgbm as lgb

FEATURE_COLS = [
    "vwap_zscore", "long_liq_zs", "short_liq_zs", "zc_norm", "sf_div",
    "val_dist", "vah_dist", "taker_ratio", "rsi_14", "atr_ratio",
    "volume_ratio", "slope200", "funding_rate_pct", "basis_index_bps",
    "vol_strain", "hour", "tide_align", "signal_side", "sleeve_id"
]


class InstitutionalDualModelEngine:
    def __init__(
        self,
        capital: float = 5000.0,
        base_risk: float = 54.0,
        house_risk_max: float = 90.0,
        defense_risk: float = 14.0,
        milestone_risk: float = 10.0,
        trans_risk: float = 35.0,
        trans_thresh: float = 480.0,
        t1_base_risk: float = 42.0,
        t1_trans_risk: float = 22.0,
        cushion_multiplier: float = 0.25,
        milestone_profit_usd: float = 500.0,
        max_concurrent: int = 3,
        max_s1_concurrent: int = 2,
        max_t1_concurrent: int = 2,
        cooldown_bars: int = 4,
        win_r_reset_thresh: float = 0.90,
        conf_prob_thresh: float = 0.46,
        conf_mult: float = 1.35,
        max_dd_limit: float = 4.40,
        stage1_arm_profit: float = 180.0,
        stage1_floor_profit: float = 75.0,
        house_compounding_rate: float = 0.20,
        house_compounding_start: float = 50.0,
        min_train_rows_per_symbol: int = 500,
        random_state: int = 42
    ):
        self.capital = capital
        self.base_risk = base_risk
        self.house_risk_max = house_risk_max
        self.defense_risk = defense_risk
        self.milestone_risk = milestone_risk
        self.trans_risk = trans_risk
        self.trans_thresh = trans_thresh
        self.t1_base_risk = t1_base_risk
        self.t1_trans_risk = t1_trans_risk
        self.cushion_multiplier = cushion_multiplier
        self.milestone_profit_usd = milestone_profit_usd
        self.max_concurrent = max_concurrent
        self.max_s1_concurrent = max_s1_concurrent
        self.max_t1_concurrent = max_t1_concurrent
        self.cooldown_bars = cooldown_bars
        self.win_r_reset_thresh = win_r_reset_thresh
        self.conf_prob_thresh = conf_prob_thresh
        self.conf_mult = conf_mult
        self.max_dd_limit = max_dd_limit
        self.stage1_arm_profit = stage1_arm_profit
        self.stage1_floor_profit = stage1_floor_profit
        self.house_compounding_rate = house_compounding_rate
        self.house_compounding_start = house_compounding_start
        self.min_train_rows_per_symbol = min_train_rows_per_symbol
        self.random_state = random_state

    def train_models(
        self,
        train_df: pd.DataFrame
    ) -> Tuple[LogisticRegression, lgb.LGBMClassifier, pd.Series, pd.Series, float]:
        """Train regularized linear foundation and shallow tree ensemble on in-sample data."""
        X_train = train_df[FEATURE_COLS]
        y_train = train_df["label_y"].to_numpy()

        mu = X_train.mean(axis=0)
        sd = X_train.std(axis=0).replace(0, 1.0)
        X_tr_s = np.nan_to_num(((X_train - mu) / sd).clip(-5.0, 5.0).to_numpy(float), nan=0.0)

        # 1. L2 Regularized Ridge Foundation (C=0.028746)
        ridge = LogisticRegression(C=0.02874565597723325, max_iter=200, random_state=self.random_state)
        ridge.fit(X_tr_s, y_train)

        # 2. Regularized LightGBM Classifier (Trial #24641 Champion: 10 Passes, +4,629.28 USD)
        clf = lgb.LGBMClassifier(
            n_estimators=160,
            max_depth=4,
            num_leaves=1023,
            learning_rate=0.041505933280628474,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=2.1330083458796363,
            reg_lambda=0.47695776438584003,
            random_state=self.random_state,
            verbose=-1,
            n_jobs=2
        )
        clf.fit(X_train, y_train)

        # 3. In-Sample Monthly Quantile Threshold Calibration (60% Ridge + 40% LightGBM)
        train_probs_ridge = ridge.predict_proba(X_tr_s)[:, 1]
        train_probs_lgb = clf.predict_proba(X_train)[:, 1]
        train_probs = 0.60 * train_probs_ridge + 0.40 * train_probs_lgb

        n_train_months = max(1.0, (train_df.open_time_ms.max() - train_df.open_time_ms.min()) / (30.4375 * 86_400_000))
        cands_per_month = len(train_df) / n_train_months
        calib_q = max(0.60, min(0.96, 1.0 - (42.0 / cands_per_month)))
        raw_calib_thresh = float(np.quantile(train_probs, calib_q))
        # Stationary upper bound: prevents small-sample over-pruning in early epochs (Oxford-Man 2020)
        calib_thresh = min(0.5120, raw_calib_thresh)

        return ridge, clf, mu, sd, calib_thresh

    # ========================================================================
    # PER-SYMBOL TRAINING  --  decouples the universe from the predictions
    # ========================================================================
    # Before this refactor the runner did:
    #       train_set = all_data[train_mask]          # ALL symbols pooled
    #       ridge, clf, ... = engine.train_models(train_set)
    # so the S1 model was a single cross-sectional model fitted on every symbol
    # at once. Adding or removing a symbol therefore changed the fitted
    # coefficients and silently rewrote the predictions -- and the history --
    # of every OTHER symbol. Measured effect: adding 7 altcoins moved the
    # original 11 symbols' pooled PnL by +3,203.83 USD while the 7 newcomers
    # themselves contributed -739.53. Attribution was impossible.
    #
    # Each symbol now gets its own model fitted only on its own history, so a
    # universe change cannot touch another symbol's predictions. Symbols with
    # insufficient history, or with only one class present in the training
    # window, are skipped entirely for that window rather than silently
    # borrowing a pooled model.
    # ========================================================================
    def train_models_by_symbol(self, train_df: pd.DataFrame) -> Dict[str, tuple]:
        """Fit an independent model per symbol. Returns {symbol: (ridge, clf, mu, sd, thresh)}."""
        models: Dict[str, tuple] = {}
        for sym, sub in train_df.groupby("symbol", sort=True):
            if len(sub) < self.min_train_rows_per_symbol:
                continue
            if sub["label_y"].nunique() < 2:
                continue          # single-class window: no classifier can be fitted
            sub = sub.sort_values("open_time_ms").reset_index(drop=True)
            models[sym] = self.train_models(sub)
        return models

    def score_test_candidates_by_symbol(
        self,
        test_df: pd.DataFrame,
        models: Dict[str, tuple],
        regime_delta: float = 0.0
    ) -> pd.DataFrame:
        """Score each symbol's test rows with that symbol's own model."""
        frames = []
        skipped = []
        thresholds = []
        for sym, sub in test_df.groupby("symbol", sort=True):
            if sym not in models:
                skipped.append(sym)
                continue
            ridge, clf, mu, sd, thr = models[sym]
            out = self.score_test_candidates(
                sub, ridge, clf, mu, sd, thr, regime_delta=regime_delta
            )
            thresholds.append(float(out.attrs.get("effective_calib_thresh", thr)))
            frames.append(out)

        if not frames:
            empty = test_df.iloc[0:0].copy()
            empty["prob"] = pd.Series(dtype=float)
            empty["calib_thresh"] = pd.Series(dtype=float)
            empty.attrs.update(
                effective_calib_thresh=0.0, regime_delta=max(0.0, float(regime_delta)),
                symbols_modeled=[], symbols_skipped=skipped,
            )
            return empty

        selected = pd.concat(frames, ignore_index=True)
        selected.sort_values(by=["open_time_ms", "prob"], ascending=[True, False], inplace=True)
        selected.reset_index(drop=True, inplace=True)
        selected.attrs.update(
            # Summary of the per-symbol thresholds; the runner reports this.
            effective_calib_thresh=float(np.mean(thresholds)) if thresholds else 0.0,
            regime_delta=max(0.0, float(regime_delta)),
            symbols_modeled=sorted(models.keys()),
            symbols_skipped=skipped,
            n_thresholds=len(thresholds),
        )
        return selected

    def score_test_candidates(
        self,
        test_df: pd.DataFrame,
        ridge: LogisticRegression,
        clf: lgb.LGBMClassifier,
        mu: pd.Series,
        sd: pd.Series,
        calib_thresh: float,
        regime_delta: float = 0.0
    ) -> pd.DataFrame:
        """Score out-of-sample test candidates using causal ensemble and threshold gating."""
        # PHASE 3: the relief branch is gone. The calibration threshold is FLAT.
        # It formerly dropped by vol_shift_amt (0.025) whenever trailing BTC
        # volatility fell below vol_shift_thresh (0.92), i.e. the system traded
        # *more* aggressively in calm conditions -- an accelerator that walked
        # it into macro tightenings. Governance here is penalty-only.
        effective_calib_thresh = calib_thresh

        # --- Regime Governor ------------------------------------------------
        # Penalty-only defensive adjustment derived from persistent MARKET state
        # (BTC realised volatility, tide alignment, cross-sectional dispersion)
        # evaluated strictly before this window opened. Never negative.
        regime_delta = max(0.0, float(regime_delta))
        effective_calib_thresh += regime_delta

        X_test = test_df[FEATURE_COLS]
        X_te_s = np.nan_to_num(((X_test - mu) / sd).clip(-5.0, 5.0).to_numpy(float), nan=0.0)

        test_probs_ridge = ridge.predict_proba(X_te_s)[:, 1]
        test_probs_lgb = clf.predict_proba(X_test)[:, 1]
        test_probs = 0.60 * test_probs_ridge + 0.40 * test_probs_lgb

        selected = test_df.copy()
        selected["prob"] = test_probs
        selected["calib_thresh"] = effective_calib_thresh
        # Oxford-Man (2020) Cross-Sectional Ranking Priority:
        # At identical timestamps, prioritize higher model probability candidates first
        selected.sort_values(by=["open_time_ms", "prob"], ascending=[True, False], inplace=True)
        selected.reset_index(drop=True, inplace=True)
        selected.attrs["regime_delta"] = regime_delta
        selected.attrs["effective_calib_thresh"] = effective_calib_thresh
        return selected


    @staticmethod
    def load_t1_breakout_trades(cache_dir=None) -> pd.DataFrame:
        """RETIRED shim. Delegates to Engine.strategy.t1_breakout, the single
        source of truth for the T1 sleeve, so this frozen file cannot drift."""
        from Engine.strategy.t1_breakout import load_t1_breakout_trades as _t1
        return _t1(cache_dir)

    def simulate_execution(
        self,
        selected: pd.DataFrame,
        t1_df: pd.DataFrame | None = None,
        start_ms: int | None = None,
        end_ms: int | None = None,
    ) -> Dict[str, Any]:
        equity = self.capital
        peak_equity = self.capital
        cur_max_dd_pct = 0.0
        consec_losses_s1 = 0
        s1_positions: List[Tuple[int, float]] = []
        t1_positions: List[Tuple[int, float]] = []
        symbol_cooldown: Dict[str, int] = {}
        executed_trades: List[Dict[str, Any]] = []
        s1_count = 0
        t1_count = 0
        stage1_armed = False

        # Extract S1 candidate events
        s1_events: List[Dict[str, Any]] = []
        for idx in range(len(selected)):
            prob = float(selected["prob"].iloc[idx])
            tide = float(selected["btc_macro_tide"].iloc[idx]) if "btc_macro_tide" in selected.columns else 0.0
            side = int(selected["signal_side"].iloc[idx]) if "signal_side" in selected.columns else 1
            calib_thresh = float(selected["calib_thresh"].iloc[idx]) if "calib_thresh" in selected.columns else 0.45

            # Macro Tide Asymmetry (Liu, Tsyvinski, Wu 2022) & Soft Bear Tide Veto
            if side == -1 and tide > 0.0:
                continue
            if side == 1 and tide < 0.0 and prob < (calib_thresh + 0.020):
                continue

            # Refined Xuan (2026, SSRN-6872638) Distribution Veto
            funding = float(selected["funding_rate_pct"].iloc[idx]) if "funding_rate_pct" in selected.columns else 0.0
            slope = float(selected["slope200"].iloc[idx]) if "slope200" in selected.columns else 0.0
            if side == 1 and (funding >= 0.035) and (slope < 0.25):
                continue

            if prob >= calib_thresh:
                s1_events.append({
                    "time": int(selected["open_time_ms"].iloc[idx]),
                    "prob": prob,
                    "r_gain": float(selected["realized_r"].iloc[idx]),
                    "hold_bars": int(selected["bars_held"].iloc[idx]),
                    "symbol": str(selected["symbol"].iloc[idx]),
                    "strategy": "S1"
                })

        # Extract T1 candidate events if provided
        t1_events: List[Dict[str, Any]] = []
        if t1_df is not None and len(t1_df) > 0:
            if start_ms is None and len(selected) > 0:
                start_ms = int(selected["open_time_ms"].min())
            if end_ms is None and len(selected) > 0:
                end_ms = int(selected["open_time_ms"].max())

            if start_ms is not None and end_ms is not None:
                t1_mask = (t1_df["time"] >= start_ms) & (t1_df["time"] <= end_ms)
                t1_sub = t1_df[t1_mask]
                t1_events = t1_sub.to_dict("records")
            else:
                t1_events = t1_df.to_dict("records")

        combined = s1_events + t1_events
        combined.sort(key=lambda x: (x["time"], -x["prob"]))

        for ev in combined:
            if cur_max_dd_pct >= self.max_dd_limit:
                continue

            t_entry = ev["time"]
            strat = ev["strategy"]
            sym = ev["symbol"]
            r_gain = ev["r_gain"]
            prob = ev["prob"]
            hold_ms = int(ev["hold_bars"]) * 15 * 60 * 1000

            # Prune closed positions based on entry timestamp
            s1_positions = [p for p in s1_positions if p[0] > t_entry]
            t1_positions = [p for p in t1_positions if p[0] > t_entry]

            if sym in symbol_cooldown and t_entry < symbol_cooldown[sym]:
                continue

            current_profit = equity - self.capital

            # Two-Stage Profit Floor (Stage 1 Floor Lock)
            if self.stage1_arm_profit > 0.0 and current_profit >= self.stage1_arm_profit:
                stage1_armed = True

            if stage1_armed and self.stage1_floor_profit > 0.0 and current_profit <= self.stage1_floor_profit:
                continue

            cur_peak_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
            cur_cap_dd = ((self.capital - equity) / self.capital) * 100.0 if equity < self.capital else 0.0

            # House Money Capacity Surge: expand slots once verified profit >= 180.0 USD
            if current_profit >= 180.0:
                cur_max_s1 = 3
                cur_max_tot = 4
                cur_max_risk_budget = 130.0
            else:
                cur_max_s1 = self.max_s1_concurrent
                cur_max_tot = self.max_concurrent
                cur_max_risk_budget = 110.0

            if strat == "S1":
                if len(s1_positions) >= cur_max_s1:
                    continue
                if len(s1_positions) + len(t1_positions) >= cur_max_tot:
                    continue

                if (peak_equity - self.capital) >= self.milestone_profit_usd:
                    # Continuous CPPI cushion risk compression above milestone (Black-Perold 1992)
                    cushion = max(0.0, equity - (self.capital + self.milestone_profit_usd))
                    risk_amt = min(self.milestone_risk, cushion * self.cushion_multiplier)
                elif current_profit >= self.trans_thresh:
                    risk_amt = self.trans_risk
                elif cur_cap_dd >= 2.0 or cur_peak_dd >= 4.0 or consec_losses_s1 >= 2:
                    risk_amt = self.defense_risk
                elif consec_losses_s1 == 1:
                    if current_profit < 0.0:
                        risk_amt = 30.0
                    else:
                        conf = self.conf_mult if prob >= self.conf_prob_thresh else 1.0
                        risk_amt = self.base_risk * conf
                else:
                    conf = self.conf_mult if prob >= self.conf_prob_thresh else 1.0
                    base_s = self.base_risk * conf
                    if current_profit >= self.house_compounding_start:
                        risk_amt = min(self.house_risk_max, base_s + current_profit * self.house_compounding_rate)
                    else:
                        risk_amt = base_s

                if risk_amt <= 0.0:
                    continue

                current_open_risk = sum(p[1] for p in s1_positions) + sum(p[1] for p in t1_positions)
                remaining_risk_budget = max(14.0, cur_max_risk_budget - current_open_risk)
                final_risk = min(risk_amt, remaining_risk_budget)

                s1_positions.append((t_entry + hold_ms, final_risk))
                trade_pnl = r_gain * final_risk
                equity += trade_pnl
                if equity > peak_equity:
                    peak_equity = equity
                dd_pct = ((peak_equity - equity) / peak_equity) * 100.0
                if dd_pct > cur_max_dd_pct:
                    cur_max_dd_pct = dd_pct

                if r_gain >= self.win_r_reset_thresh:
                    consec_losses_s1 = 0
                else:
                    consec_losses_s1 += 1
                    symbol_cooldown[sym] = t_entry + self.cooldown_bars * 15 * 60 * 1000

                executed_trades.append({"win": 1 if r_gain > 0 else 0, "pnl": trade_pnl, "strat": "S1",
                                    "time": t_entry, "symbol": sym, "r_gain": r_gain,
                                    "risk_usd": final_risk})
                s1_count += 1

            else:  # T1 Breakout
                if len(t1_positions) >= self.max_t1_concurrent:
                    continue
                if len(s1_positions) + len(t1_positions) >= cur_max_tot:
                    continue

                if (peak_equity - self.capital) >= self.milestone_profit_usd:
                    # Continuous CPPI cushion risk compression above milestone
                    cushion = max(0.0, equity - (self.capital + self.milestone_profit_usd))
                    risk_amt = min(8.0, cushion * self.cushion_multiplier)
                elif current_profit >= self.trans_thresh:
                    risk_amt = self.t1_trans_risk
                elif cur_cap_dd >= 2.0 or cur_peak_dd >= 4.0:
                    risk_amt = self.defense_risk
                else:
                    risk_amt = self.t1_base_risk

                if risk_amt <= 0.0:
                    continue

                current_open_risk = sum(p[1] for p in s1_positions) + sum(p[1] for p in t1_positions)
                remaining_risk_budget = max(14.0, cur_max_risk_budget - current_open_risk)
                final_risk = min(risk_amt, remaining_risk_budget)

                t1_positions.append((t_entry + hold_ms, final_risk))
                trade_pnl = r_gain * final_risk
                equity += trade_pnl
                if equity > peak_equity:
                    peak_equity = equity
                dd_pct = ((peak_equity - equity) / peak_equity) * 100.0
                if dd_pct > cur_max_dd_pct:
                    cur_max_dd_pct = dd_pct

                executed_trades.append({"win": 1 if r_gain > 0 else 0, "pnl": trade_pnl, "strat": "T1",
                                    "time": t_entry, "symbol": sym, "r_gain": r_gain,
                                    "risk_usd": final_risk})
                t1_count += 1

        n_trades = len(executed_trades)
        wr = (sum(tr["win"] for tr in executed_trades) / n_trades * 100.0) if n_trades > 0 else 0.0
        net_pnl = equity - self.capital
        net_roi = (net_pnl / self.capital) * 100.0

        return {
            "net_pnl": net_pnl,
            "net_roi": net_roi,
            "max_dd": cur_max_dd_pct,
            "win_rate": wr,
            "trades": n_trades,
            "s1_trades": s1_count,
            "t1_trades": t1_count,
            "equity": equity,
            # Trade-level ledger for the CVaR harness (Engine/strategy/cvar_gate_harness.py).
            # Time-ordered, post-cost r_gain plus the USD risk actually deployed.
            "trade_ledger": executed_trades,
        }
