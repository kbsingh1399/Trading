# Engine/runners/smc_footprint_runner.py
from __future__ import annotations

import os
import json
import time
import numpy as np
import pandas as pd
from typing import Dict, List, Optional

from Engine.ml.footprint_features import FootprintLadderFeatures
from Engine.ml.smc_meta_labeler import SMCRegressionMetaLabeler
from Engine.core.portfolio_execution_kernel import PortfolioExecutionKernel
from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig


class SMCFootprintRunner:
    """
    Round-4 Unified Walk-Forward Runner:
      [Raw SMC Macro Structure] -> [Footprint Order Flow Confirmation] ->
      [ML Continuous R-Meta-Labeling] -> [Causal Portfolio Execution]
    """

    def __init__(self, per_symbol_data: Dict[str, pd.DataFrame],
                 ladder_dir: str = "Engine/binance_backtesting_data",
                 windows_json_path: str = "Engine/oos_windows_20.json",
                 targets_json_path: str = "Engine/target_oos_criteria.json",
                 min_conf_score: int = 3,
                 max_positions: int = 2):
        self.data = per_symbol_data
        self.ladder_dir = ladder_dir
        with open(windows_json_path, "r", encoding="utf-8") as f:
            self.windows: List[Dict] = json.load(f)
        with open(targets_json_path, "r", encoding="utf-8") as f:
            self.targets = json.load(f)["target_criteria"]
        self.min_conf = min_conf_score
        self.max_positions = max_positions

        # Pre-compute footprint features once across all symbols
        print(f"Pre-computing Footprint Ladder features across {len(per_symbol_data)} symbols...")
        t0 = time.time()
        fp = FootprintLadderFeatures()
        self.ladder_feats: Dict[str, pd.DataFrame] = {}
        for sym, df_sym in per_symbol_data.items():
            lad_path = os.path.join(ladder_dir, f"{sym}_15m_footprint_ladder.parquet")
            if os.path.exists(lad_path):
                try:
                    agg = fp.load_and_aggregate(lad_path)
                    self.ladder_feats[sym] = fp.build_features(agg, ohlc=df_sym)
                except Exception as e:
                    print(f"Warning: Failed to load ladder for {sym}: {e}")
                    self.ladder_feats[sym] = pd.DataFrame(index=df_sym.index)
            else:
                self.ladder_feats[sym] = pd.DataFrame(index=df_sym.index)
        print(f"Loaded and aggregated footprint features in {time.time() - t0:.2f}s")

    def run_window(self, w: Dict, verbose: bool = True) -> Dict:
        labeler = SMCRegressionMetaLabeler(min_conf_score=self.min_conf)
        ws = pd.Timestamp(w["start_date"])
        we = pd.Timestamp(w["end_date"]) + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
        train_end = ws - pd.Timedelta(hours=72)
        train_start = train_end - pd.Timedelta(days=365)

        # 1) Pool confirmed SMC events (train slice, all 18 assets)
        train_slices = {s: d.loc[train_start:train_end] for s, d in self.data.items()}
        try:
            pooled = labeler.pool_smc(train_slices, self.ladder_feats, train_start, train_end)
        except Exception as e:
            if verbose:
                print(f"W{w['window_id']:02d} | Failed to pool events: {e}")
            return {
                "window_id": w["window_id"], "name": w["name"], "deploy": False,
                "reason": f"Pool error: {e}", "trades": 0, "roi_pct": 0.0,
                "max_dd_pct": 0.0, "win_rate_pct": 0.0, "passed": False
            }

        # 2) Feature probe gate (honest kill-switch)
        probe = labeler.probe_features(pooled)
        best_single = probe["raw_auc_abs"].max() if "raw_auc_abs" in probe else 0.0
        best_pair = probe["best_pair_auc"].iloc[0] if "best_pair_auc" in probe else 0.5
        if verbose:
            print(f"\n--- W{w['window_id']:02d} ({w['name']}) SMC Probe ---")
            print(f"Pooled events: {len(pooled)} | Base positive rate: {pooled['y'].mean():.3f}")
            print(f"Top 5 probe features:\n{probe[['feature', 'raw_auc_mean', 'raw_auc_abs']].head(5)}")
            print(f"Best pair: {probe['best_pair'].iloc[0]} -> AUC: {best_pair:.4f}")

        # Kill-switch: if no signal exists
        if best_single < 0.03 and best_pair < 0.54:
            if verbose:
                print(f"W{w['window_id']:02d} | NO DEPLOY: probe below threshold (single={best_single:.3f}, pair={best_pair:.3f})")
            return {
                "window_id": w["window_id"], "name": w["name"], "deploy": False,
                "reason": f"Probe below threshold: single={best_single:.3f}, pair={best_pair:.3f}",
                "trades": 0, "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0, "passed": False
            }

        fit = labeler.fit(pooled)
        if fit["mean_cv_auc"] < 0.53:
            if verbose:
                print(f"W{w['window_id']:02d} | NO DEPLOY: CV-AUC {fit['mean_cv_auc']:.3f} < 0.53")
            return {
                "window_id": w["window_id"], "name": w["name"], "deploy": False,
                "reason": f"CV-AUC {fit['mean_cv_auc']:.3f} < 0.53", "trades": 0,
                "roi_pct": 0.0, "max_dd_pct": 0.0, "win_rate_pct": 0.0, "passed": False
            }

        # 3) OOS evaluation: detect -> confirm -> score -> gate
        gated, oos = {}, {}
        for sym, d in self.data.items():
            sl = d.loc[ws:we]
            if len(sl) < 50:
                continue
            sig = labeler.detector.generate_signals(sl.copy())
            if sym in self.ladder_feats:
                gated[sym] = labeler.score_smc(sl, self.ladder_feats[sym].loc[sl.index], sig)
            else:
                gated[sym] = sig
            oos[sym] = sl

        # 4) Causal Portfolio Execution Kernel (2.25R target, 1.00R stop, 32h time decay)
        kernel = PortfolioExecutionKernel(
            symbols=list(oos.keys()),
            risk=RiskConfig(
                base_risk=100.0 if fit["oof_expectancy_all"] > 0.30 else 50.0,
                house_money_risk=150.0,
                drawdown_defense_risk=50.0,
                drawdown_limit=0.045
            ),
            fric=FrictionConfig(),
            ratchet=RatchetConfig(
                arm0_r=1.00, lock0_r=0.35,
                arm1_r=1.60, lock1_r=0.90,
                min_target_r=2.25,
                time_decay_bars=128,
                time_decay_r=0.30
            ),
            max_positions=self.max_positions
        )
        res = kernel.run(oos, gated)

        passed = (
            res["roi_pct"] > self.targets["min_roi_percent"]
            and res["max_dd_pct"] < self.targets["max_dd_percent"]
            and res["win_rate_pct"] > self.targets["min_winrate_percent"]
            and res["trades"] >= self.targets["min_trades"]
        )

        res.update({
            "window_id": w["window_id"],
            "name": w["name"],
            "start_date": w["start_date"],
            "end_date": w["end_date"],
            "passed": passed,
            "deploy": True,
            "cv_auc": fit["mean_cv_auc"],
            "tau_r": fit["calibrated_tau_r"],
            "oof_expectancy": fit["oof_expectancy_all"],
            "n_events": fit["n_events"]
        })

        if verbose:
            tag = "PASS" if passed else "FAIL"
            print(f"W{w['window_id']:02d} | N {res['trades']:3d} | PnL {res['net_pnl']:+9.2f}$ | "
                  f"ROI {res['roi_pct']:+7.2f}% | DD {res['max_dd_pct']:5.2f}% | "
                  f"WR {res['win_rate_pct']:5.1f}% | AUC {res['cv_auc']:.3f} | {tag}")
        return res
