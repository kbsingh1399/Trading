"""
Engine/ml/train_calibrate_meta_pipeline.py
Institutional Two-Stage Meta-Labeling Training & Calibration Pipeline
Implements Marcos Lopez de Prado's Meta-Labeling framework across 23 Out-Of-Sample Windows (2021-2026).

Compares:
1. Baseline: Uncurated setup candidates
2. Global Pooled Meta-Labeler: Single model across all assets
3. Asset-Specialized Meta-Labeler:
   - BTC, ETH, BCH: Random Forest (averages high-frequency market-maker noise)
   - DOGE, LINK: Shallow LightGBM (captures non-linear liquidation cascades)
   - SOL, XRP, BNB, ADA, TRX, DOT, LTC: Dual-Model Ensemble (60% Ridge + 40% LightGBM)
"""
from __future__ import annotations

import json
import time
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss
import lightgbm as lgb
import warnings

warnings.filterwarnings("ignore")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from Engine.core.fast_numba_oos_engine import (
    compile_dataset_with_numba, WINDOWS_PATH, FEATURE_COLS, CAPITAL,
    MIN_ROI, MAX_DD, MIN_WR, MIN_TRADES
)
from numba import njit

# Meta-labeler feature set (strictly stationary, unit-free)
META_FEATURES = [
    "vwap_zscore", "long_liq_zs", "short_liq_zs", "zc_norm", "sf_div",
    "val_dist", "vah_dist", "taker_ratio", "rsi_14", "atr_ratio",
    "volume_ratio", "slope200", "funding_rate_pct", "basis_index_bps",
    "vol_strain", "hour", "tide_align",
    "pdl_dist", "pdh_dist", "pwl_dist", "pwh_dist",
    "pdl_sweep_bull", "pdh_sweep_bear"
]

MAJORS = {"BTCUSDT", "ETHUSDT", "BCHUSDT"}
MOMENTUM_ALTS = {"DOGEUSDT", "LINKUSDT"}

@njit(fastmath=True)
def simulate_fast_portfolio(
    event_times: np.ndarray,
    event_r_gains: np.ndarray,
    event_risks: np.ndarray,
    event_hold_ms: np.ndarray,
    event_syms: np.ndarray,
    capital: float = 5000.0,
    max_concurrent: int = 3,
    milestone_pnl: float = 500.0,
    dd_stop_pct: float = 4.85
):
    n = len(event_times)
    equity = capital
    peak_equity = capital
    max_dd_pct = 0.0

    pos_active = np.zeros(max_concurrent, dtype=np.bool_)
    pos_end_times = np.zeros(max_concurrent, dtype=np.int64)
    pos_syms = np.full(max_concurrent, -1, dtype=np.int64)

    tr_count = 0
    win_count = 0
    locked = False

    trade_pnls = np.zeros(n, dtype=np.float64)

    for i in range(n):
        t = event_times[i]
        r = event_r_gains[i]
        base_r = event_risks[i]
        hold = event_hold_ms[i]
        sym = event_syms[i]

        # Release expired positions
        for p in range(max_concurrent):
            if pos_active[p] and t >= pos_end_times[p]:
                pos_active[p] = False
                pos_syms[p] = -1

        if locked:
            continue

        if max_dd_pct >= dd_stop_pct:
            locked = True
            continue

        # Count active positions
        active_count = 0
        slot = -1
        sym_already = False

        for p in range(max_concurrent):
            if pos_active[p]:
                active_count += 1
                if pos_syms[p] == sym:
                    sym_already = True
            elif slot == -1:
                slot = p

        if active_count >= max_concurrent or slot == -1 or sym_already:
            continue

        # Milestone lock
        if (peak_equity - capital) >= milestone_pnl and tr_count >= 15:
            floor_stop = max(capital + milestone_pnl, peak_equity - 120.0)
            if equity <= floor_stop:
                locked = True
                continue

        # Dynamic Risk Budgeting
        cur_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
        cur_profit = equity - capital

        is_milestone = (peak_equity - capital) >= milestone_pnl
        if is_milestone:
            cushion = max(0.0, equity - (capital + milestone_pnl))
            trade_risk = min(10.0, cushion * 0.20)
            if trade_risk <= 0.0:
                locked = True
                continue
        elif cur_dd >= 2.0 or cur_profit < -50.0:
            trade_risk = min(base_r * 0.40, 14.0)
        elif cur_profit >= 120.0:
            trade_risk = min(base_r * 1.35, 48.0)
        else:
            trade_risk = min(base_r, 36.0)

        if (not is_milestone) and max_dd_pct >= 1.80:
            trade_risk = trade_risk * 0.5

        # Open position
        pos_active[slot] = True
        pos_end_times[slot] = t + hold
        pos_syms[slot] = sym

        pnl = r * trade_risk
        equity += pnl
        if equity > peak_equity:
            peak_equity = equity
        dd = ((peak_equity - equity) / peak_equity) * 100.0
        if dd > max_dd_pct:
            max_dd_pct = dd

        trade_pnls[tr_count] = pnl
        tr_count += 1
        if r > 0:
            win_count += 1

    return equity - capital, max_dd_pct, tr_count, win_count, trade_pnls[:tr_count]


class AssetSpecializedMetaPipeline:
    def __init__(self, quantile_threshold: float = 0.70):
        self.quantile_thresh = quantile_threshold
        self.models = {}
        self.mu = None
        self.sd = None
        self.tau_thresholds = {}

    def fit(self, train_df: pd.DataFrame):
        X_all = train_df[META_FEATURES].to_numpy(float)
        y_all = train_df["label_y"].to_numpy(int)

        self.mu = np.nanmean(X_all, axis=0)
        self.sd = np.nanstd(X_all, axis=0)
        self.sd[self.sd == 0] = 1.0

        # Train models per asset class
        # 1. Majors: Random Forest
        majors_mask = train_df["symbol"].isin(MAJORS).to_numpy()
        if majors_mask.sum() >= 200:
            rf = RandomForestClassifier(
                n_estimators=100, max_depth=4, min_samples_leaf=20, random_state=42, n_jobs=-1
            )
            rf.fit(X_all[majors_mask], y_all[majors_mask])
            self.models["majors_rf"] = rf
            p_majors = rf.predict_proba(X_all[majors_mask])[:, 1]
            self.tau_thresholds["majors"] = float(np.percentile(p_majors, self.quantile_thresh * 100))

        # 2. Momentum Alts: LightGBM
        mom_mask = train_df["symbol"].isin(MOMENTUM_ALTS).to_numpy()
        if mom_mask.sum() >= 200:
            lgbm = lgb.LGBMClassifier(
                n_estimators=100, max_depth=3, learning_rate=0.03, num_leaves=7,
                min_child_samples=30, reg_alpha=1.5, reg_lambda=3.0, random_state=42, n_jobs=-1, verbose=-1
            )
            lgbm.fit(X_all[mom_mask], y_all[mom_mask])
            self.models["mom_lgbm"] = lgbm
            p_mom = lgbm.predict_proba(X_all[mom_mask])[:, 1]
            self.tau_thresholds["momentum"] = float(np.percentile(p_mom, self.quantile_thresh * 100))

        # 3. Trend/Mean-Reversion: Dual Model (60% Ridge + 40% LightGBM)
        other_mask = (~majors_mask) & (~mom_mask)
        if other_mask.sum() >= 200:
            X_s = np.nan_to_num(np.clip((X_all[other_mask] - self.mu) / self.sd, -5.0, 5.0), nan=0.0)
            ridge = LogisticRegression(C=0.1, max_iter=500, random_state=42)
            ridge.fit(X_s, y_all[other_mask])
            
            lgbm_other = lgb.LGBMClassifier(
                n_estimators=100, max_depth=3, learning_rate=0.03, num_leaves=7,
                min_child_samples=30, reg_alpha=1.5, reg_lambda=3.0, random_state=42, n_jobs=-1, verbose=-1
            )
            lgbm_other.fit(X_all[other_mask], y_all[other_mask])
            self.models["other_ridge"] = ridge
            self.models["other_lgbm"] = lgbm_other

            p_ens = 0.60 * ridge.predict_proba(X_s)[:, 1] + 0.40 * lgbm_other.predict_proba(X_all[other_mask])[:, 1]
            self.tau_thresholds["other"] = float(np.percentile(p_ens, self.quantile_thresh * 100))

    def predict_probabilities(self, test_df: pd.DataFrame) -> np.ndarray:
        n = len(test_df)
        probs = np.zeros(n, dtype=np.float64)
        pass_gate = np.zeros(n, dtype=np.bool_)

        X_te = test_df[META_FEATURES].to_numpy(float)
        X_te_s = np.nan_to_num(np.clip((X_te - self.mu) / self.sd, -5.0, 5.0), nan=0.0)
        symbols = test_df["symbol"].to_numpy()

        for i in range(n):
            sym = symbols[i]
            x_raw = X_te[i:i+1]
            x_s = X_te_s[i:i+1]

            if sym in MAJORS and "majors_rf" in self.models:
                p = self.models["majors_rf"].predict_proba(x_raw)[0, 1]
                tau = self.tau_thresholds.get("majors", 0.55)
            elif sym in MOMENTUM_ALTS and "mom_lgbm" in self.models:
                p = self.models["mom_lgbm"].predict_proba(x_raw)[0, 1]
                tau = self.tau_thresholds.get("momentum", 0.55)
            elif "other_ridge" in self.models and "other_lgbm" in self.models:
                p_r = self.models["other_ridge"].predict_proba(x_s)[0, 1]
                p_l = self.models["other_lgbm"].predict_proba(x_raw)[0, 1]
                p = 0.60 * p_r + 0.40 * p_l
                tau = self.tau_thresholds.get("other", 0.55)
            else:
                p = 0.50
                tau = 0.50

            probs[i] = p
            pass_gate[i] = p >= tau

        return probs, pass_gate


def run_meta_calibration_benchmark():
    t_start = time.perf_counter()
    print("=" * 135)
    print("LOPEZ DE PRADO TWO-STAGE META-LABELING CALIBRATION BENCHMARK (23 OOS WINDOWS, 2021-2026)")
    print("=" * 135)

    all_data = compile_dataset_with_numba()

    with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
        windows = json.load(f)

    PURGE_MS = 72 * 3600 * 1000

    # Symbol encoding for fast JIT simulation
    core_syms = sorted(all_data["symbol"].unique())
    sym_map = {s: i for i, s in enumerate(core_syms)}
    all_data["sym_id"] = all_data["symbol"].map(sym_map)

    results_baseline = []
    results_meta = []

    print("\n" + "-" * 135)
    print(f"{'W#':<3} | {'Window Name':<36} | {'Base Tr':<7} | {'Base WR':<7} | {'Base ROI':<8} | {'Meta Tr':<7} | {'Meta WR':<7} | {'Meta ROI':<9} | {'Max DD':<7} | {'Status':<6}")
    print("-" * 135)

    passed_base = 0
    passed_meta = 0

    for w in windows:
        w_id = w["window_id"]
        w_name = w["name"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        purge_ms = start_ms - PURGE_MS

        train_mask = all_data["open_time_ms"] < purge_ms
        test_mask = (all_data["open_time_ms"] >= start_ms) & (all_data["open_time_ms"] <= end_ms)

        train_set = all_data[train_mask]
        test_set = all_data[test_mask]

        if len(train_set) < 500 or len(test_set) == 0:
            continue

        # 1. Baseline Simulation (All uncurated candidates)
        ev_times_b = test_set["open_time_ms"].to_numpy(np.int64)
        ev_rgains_b = test_set["realized_r"].to_numpy(np.float64)
        ev_risks_b = np.full(len(test_set), 36.0, dtype=np.float64)
        ev_holds_b = (test_set["bars_held"].to_numpy(np.int64) * 15 * 60 * 1000)
        ev_syms_b = test_set["sym_id"].to_numpy(np.int64)

        pnl_b, dd_b, tr_b, win_b, _ = simulate_fast_portfolio(
            ev_times_b, ev_rgains_b, ev_risks_b, ev_holds_b, ev_syms_b,
            capital=CAPITAL, max_concurrent=3, milestone_pnl=500.0, dd_stop_pct=4.85
        )
        roi_b = (pnl_b / CAPITAL) * 100.0
        wr_b = (win_b / tr_b * 100.0) if tr_b > 0 else 0.0

        # 2. Asset-Specialized Meta-Labeler Training & Scoring
        pipeline = AssetSpecializedMetaPipeline(quantile_threshold=0.65)
        pipeline.fit(train_set)
        probs, pass_gate = pipeline.predict_probabilities(test_set)

        gated_set = test_set[pass_gate]

        if len(gated_set) > 0:
            ev_times_m = gated_set["open_time_ms"].to_numpy(np.int64)
            ev_rgains_m = gated_set["realized_r"].to_numpy(np.float64)
            ev_risks_m = np.full(len(gated_set), 36.0, dtype=np.float64)
            ev_holds_m = (gated_set["bars_held"].to_numpy(np.int64) * 15 * 60 * 1000)
            ev_syms_m = gated_set["sym_id"].to_numpy(np.int64)

            pnl_m, dd_m, tr_m, win_m, _ = simulate_fast_portfolio(
                ev_times_m, ev_rgains_m, ev_risks_m, ev_holds_m, ev_syms_m,
                capital=CAPITAL, max_concurrent=3, milestone_pnl=500.0, dd_stop_pct=4.85
            )
            roi_m = (pnl_m / CAPITAL) * 100.0
            wr_m = (win_m / tr_m * 100.0) if tr_m > 0 else 0.0
        else:
            pnl_m, dd_m, tr_m, win_m, roi_m, wr_m = 0.0, 0.0, 0, 0, 0.0, 0.0

        is_pass_m = (roi_m >= MIN_ROI) and (dd_m <= MAX_DD) and (wr_m >= MIN_WR) and (tr_m >= MIN_TRADES)
        status_m = "PASS" if is_pass_m else ("PROFIT" if pnl_m > 0 and dd_m <= MAX_DD else "FAIL")

        if (roi_b >= MIN_ROI) and (dd_b <= MAX_DD) and (wr_b >= MIN_WR) and (tr_b >= MIN_TRADES):
            passed_base += 1
        if is_pass_m:
            passed_meta += 1

        print(f"W{w_id:02d} | {w_name[:36]:<36} | {tr_b:<7d} | {wr_b:>5.1f}%  | {roi_b:>+6.1f}%  | {tr_m:<7d} | {wr_m:>5.1f}%  | {roi_m:>+7.2f}%  | {dd_m:>5.2f}% | {status_m:<6}")

        results_baseline.append({"window_id": w_id, "pnl": pnl_b, "roi": roi_b, "wr": wr_b, "trades": tr_b, "dd": dd_b})
        results_meta.append({"window_id": w_id, "pnl": pnl_m, "roi": roi_m, "wr": wr_m, "trades": tr_m, "dd": dd_m, "status": status_m})

    df_b = pd.DataFrame(results_baseline)
    df_m = pd.DataFrame(results_meta)

    print("\n" + "=" * 135)
    print("META-LABELING SUMMARY PERFORMANCE COMPARISON ACROSS 23 OUT-OF-SAMPLE REGIMES")
    print("=" * 135)
    print(f"Metric                        | Baseline (No ML Filter)     | Asset-Specialized Meta-Labeler")
    print("-" * 90)
    print(f"Total Net PnL (USD)           | {df_b['pnl'].sum():>+14.2f} USD         | {df_m['pnl'].sum():>+14.2f} USD")
    print(f"Total Completed Trades        | {df_b['trades'].sum():>14,d} trades      | {df_m['trades'].sum():>14,d} trades")
    print(f"Average Win Rate              | {df_b['wr'].mean():>14.1f}%             | {df_m['wr'].mean():>14.1f}%")
    print(f"Passing Windows (Outright)    | {passed_base:>14d} / 23          | {passed_meta:>14d} / 23")
    print(f"Profitable Windows (PnL > 0)  | {(df_b['pnl'] > 0).sum():>14d} / 23          | {(df_m['pnl'] > 0).sum():>14d} / 23")
    print(f"Average Quarterly Max DD      | {df_b['dd'].mean():>14.2f}%             | {df_m['dd'].mean():>14.2f}%")
    print(f"Elapsed Benchmark Time        | {time.perf_counter() - t_start:>14.2f} seconds")
    print("=" * 135)

if __name__ == "__main__":
    run_meta_calibration_benchmark()
