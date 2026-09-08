# Engine/runners/round3_runner.py
from __future__ import annotations
import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Optional

from Engine.ml.footprint_features import FootprintLadderFeatures
from Engine.ml.rf_meta_labeler import RegressionRMetaLabeler, BarrierConfig, CVConfig
from Engine.strategy.s1_liquidation_cascade_v2 import S1LiquidationCascadeV2
from Engine.core.portfolio_execution_kernel import PortfolioExecutionKernel
from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig


class Round3MultiAssetRunner:
    """
    Round-3 Pipeline per OOS Window:
      1. Extract footprint features per symbol (train + OOS slices, causal).
      2. Merge into symbol frames -> S1v2 emits flush->reclaim signals.
      3. Pool reclaim events -> friction-adjusted R-regression labeler,
         single-feature probe gate, purged WF-CV, tau_R calibration.
      4. Probe gate: if no single feature AUC-0.5 > 0.04 and best pair < 0.56,
         return {'deploy': False} - honest no-trade verdict.
      5. Else gate signals at tau_R -> portfolio kernel (max 2 positions, 4.5% DD).
    """

    def __init__(self,
                 per_symbol_data: Dict[str, pd.DataFrame],
                 ladder_dir: str = "Engine/binance_backtesting_data",
                 windows_json_path: str = "Engine/oos_windows_20.json",
                 targets_json_path: str = "Engine/target_oos_criteria.json",
                 train_lookback_days: int = 365,
                 purge_hours: int = 72,
                 max_positions: int = 2):
        self.data = per_symbol_data
        self.ladder_dir = ladder_dir
        with open(windows_json_path, "r", encoding="utf-8") as f:
            self.windows: List[Dict] = json.load(f)
        with open(targets_json_path, "r", encoding="utf-8") as f:
            self.targets = json.load(f)["target_criteria"]
        self.lookback = pd.Timedelta(days=train_lookback_days)
        self.purge = pd.Timedelta(hours=purge_hours)
        self.max_positions = max_positions
        self.fp_extractor = FootprintLadderFeatures()
        self.enriched_data: Optional[Dict[str, pd.DataFrame]] = None

    def get_enriched_data(self) -> Dict[str, pd.DataFrame]:
        if self.enriched_data is not None:
            return self.enriched_data
        enriched = {}
        for sym, df_sym in self.data.items():
            lad_path = os.path.join(self.ladder_dir, f"{sym}_15m_footprint_ladder.parquet")
            if os.path.exists(lad_path):
                try:
                    agg = self.fp_extractor.load_and_aggregate(lad_path)
                    feats = self.fp_extractor.build_features(agg, ohlc=df_sym)
                    df2 = df_sym.join(feats, how="left").fillna(0.0)
                    enriched[sym] = df2
                except Exception as e:
                    enriched[sym] = df_sym.copy()
            else:
                enriched[sym] = df_sym.copy()
        self.enriched_data = enriched
        return self.enriched_data

    def run_window(self, w: Dict, verbose: bool = True) -> Dict:
        ws = pd.Timestamp(w["start_date"])
        we = pd.Timestamp(w["end_date"]) + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
        train_end = ws - self.purge
        train_start = train_end - self.lookback

        enriched = self.get_enriched_data()

        strat = S1LiquidationCascadeV2()
        labeler = RegressionRMetaLabeler(
            barrier=BarrierConfig(tp_r=2.00, sl_r=1.00, vertical_bars=32, min_terminal_r=0.20),
            cv=CVConfig(purge_hours=72, embargo_hours=24)
        )

        train_slices = {s: d.loc[train_start:train_end] for s, d in enriched.items()}
        pooled = labeler.pool_events(train_slices, strat, train_start, train_end)

        probe = labeler.probe_features(pooled)
        best_single = probe["raw_auc_abs"].max() if "raw_auc_abs" in probe else 0.0
        best_pair = probe["best_pair_auc"].iloc[0] if "best_pair_auc" in probe else 0.5
        if verbose:
            print(f"\n--- Feature Probe for W{w['window_id']:02d} ---")
            print(f"Top 5 single features:\n{probe[['feature', 'raw_auc_mean', 'raw_auc_abs']].head(5)}")
            print(f"Best pair: {probe['best_pair'].iloc[0]} -> AUC: {best_pair:.4f}")

        # Kill switch: if no single feature |AUC - 0.5| >= 0.04 and best pair < 0.56
        if best_single < 0.04 and best_pair < 0.56:
            if verbose:
                print(f"[KILL-SWITCH] No discriminatory signal (best single: {best_single:.3f}, best pair: {best_pair:.3f})")
            return {
                "window_id": w["window_id"], "name": w["name"], "deploy": False,
                "reason": f"Probe below threshold: single={best_single:.3f}, pair={best_pair:.3f}",
                "trades": 0, "net_pnl": 0.0, "roi_pct": 0.0, "max_dd_pct": 0.0,
                "win_rate_pct": 0.0, "passed": False
            }

        fit = labeler.fit(pooled)
        if fit["mean_cv_auc"] < 0.53:
            if verbose:
                print(f"[GATE-OFF] Mean CV-AUC {fit['mean_cv_auc']:.3f} < 0.53. Gating all trades.")
            return {
                "window_id": w["window_id"], "name": w["name"], "deploy": False,
                "reason": f"CV-AUC {fit['mean_cv_auc']:.3f} < 0.53",
                "trades": 0, "net_pnl": 0.0, "roi_pct": 0.0, "max_dd_pct": 0.0,
                "win_rate_pct": 0.0, "passed": False
            }

        gated, oos = {}, {}
        for sym, d in enriched.items():
            sl = d.loc[ws:we]
            if len(sl) < 50:
                continue
            sig = strat.generate_signals(sl.copy())
            gated[sym] = labeler.score_signals(sl, sig)
            oos[sym] = sl

        kernel = PortfolioExecutionKernel(
            symbols=list(oos.keys()),
            risk=RiskConfig(
                base_risk=100.0 if fit["oof_expectancy_all"] > 0.3 else 50.0,
                house_money_risk=75.0,
                drawdown_defense_risk=25.0,
                drawdown_limit=0.045
            ),
            fric=FrictionConfig(),
            ratchet=RatchetConfig(
                arm0_r=0.60, lock0_r=0.25,
                arm1_r=1.20, lock1_r=0.75,
                min_target_r=2.00,
                time_decay_bars=32,
                time_decay_r=0.10
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
            "best_single_auc": best_single,
            "best_pair_auc": best_pair
        })
        if verbose:
            tag = "PASS" if passed else "FAIL"
            print(f"W{w['window_id']:02d} | N {res['trades']:3d} | PnL {res['net_pnl']:+9.2f}$ | "
                  f"ROI {res['roi_pct']:+7.2f}% | DD {res['max_dd_pct']:5.2f}% | "
                  f"WR {res['win_rate_pct']:5.1f}% | AUC {res['cv_auc']:.3f} | {tag}")
        return res
