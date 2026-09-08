# Engine/runners/multi_asset_walk_forward_runner.py
from __future__ import annotations

import os
import glob
import json
import time
import numpy as np
import pandas as pd
from typing import Dict, List, Type, Optional

from Engine.ml.pooled_meta_labeler import (
    PooledInstitutionalMetaLabeler, BarrierConfig, CVConfig, ModelConfig, GateConfig)
from Engine.core.portfolio_execution_kernel import PortfolioExecutionKernel
from Engine.core.execution_kernel import RiskConfig, FrictionConfig, RatchetConfig


def load_symbol_data(data_dir: str = "Engine/binance_backtesting_data",
                     symbols: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
    """
    Load 15m master parquets for requested symbols, parse datetime_utc,
    set as DatetimeIndex, sort chronologically, and ensure tz-naive.
    """
    data = {}
    pattern = os.path.join(data_dir, "*_15m_master_2020_2026.parquet")
    files = sorted(glob.glob(pattern))
    for f in files:
        sym = os.path.basename(f).split("_")[0]
        if symbols is not None and sym not in symbols and f"{sym}USDT" not in symbols:
            continue
        df = pd.read_parquet(f)
        df["datetime_utc"] = pd.to_datetime(df["datetime_utc"])
        if df["datetime_utc"].dt.tz is not None:
            df["datetime_utc"] = df["datetime_utc"].dt.tz_convert(None)
        df.set_index("datetime_utc", inplace=True)
        df.sort_index(inplace=True)
        data[sym] = df
    return data


class MultiAssetWalkForwardRunner:
    """
    Full 20-window walk-forward across 18 assets.

    Per window:
      1. Training slice: [window_start - 365d, window_start - 72h]  (causal purge)
      2. Pool events from all 18 symbols -> fit pooled meta-labeler (purged WF-CV)
      3. OOS slice: score + quantile-gate each symbol's primary signals
      4. Execute via PortfolioExecutionKernel (max 2 concurrent, shared 4.5% breaker)
    """

    STRATEGY_CLASSES: Dict[str, type] = {}

    @classmethod
    def register(cls, name: str, strategy_cls: type) -> None:
        cls.STRATEGY_CLASSES[name] = strategy_cls

    def __init__(self,
                 per_symbol_data: Dict[str, pd.DataFrame],
                 windows_json_path: str = "Engine/oos_windows_20.json",
                 targets_json_path: str = "Engine/target_oos_criteria.json",
                 labeler: Optional[PooledInstitutionalMetaLabeler] = None,
                 train_lookback_days: int = 365,
                 purge_hours: int = 72,
                 max_positions: int = 2):
        self.data = per_symbol_data
        with open(windows_json_path, "r", encoding="utf-8") as f:
            self.windows: List[Dict] = json.load(f)
        with open(targets_json_path, "r", encoding="utf-8") as f:
            self.targets = json.load(f)["target_criteria"]
        self.labeler = labeler or PooledInstitutionalMetaLabeler(
            barrier=BarrierConfig(),
            cv=CVConfig(purge_hours=purge_hours),
            model=ModelConfig(),
            gate=GateConfig())
        self.lookback = pd.Timedelta(days=train_lookback_days)
        self.purge = pd.Timedelta(hours=purge_hours)
        self.max_positions = max_positions

    def _index(self) -> pd.DatetimeIndex:
        return self.data[next(iter(self.data))].index

    def run_window(self, strategy_cls: type, w: Dict, verbose: bool = True) -> Dict:
        ws = pd.Timestamp(w["start_date"])
        we = pd.Timestamp(w["end_date"]) + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
        train_end = ws - self.purge          # 72h causal purge gap
        train_start = train_end - self.lookback

        # ---------- 1) Pool training events across all symbols ----------
        pooled = self.labeler.pool_events(self.data, strategy_cls(), train_start, train_end)

        # ---------- 2) Fit pooled labeler (purged grouped WF-CV + tau calibration) ----------
        fit_info = self.labeler.fit(pooled)

        # ---------- 3) Score + gate OOS signals per symbol ----------
        gated: Dict[str, pd.DataFrame] = {}
        oos_data: Dict[str, pd.DataFrame] = {}
        for sym, df_sym in self.data.items():
            sl = df_sym.loc[ws:we]
            if len(sl) < self.labeler.barrier.vertical_bars + 48:
                continue
            sig = strategy_cls().generate_signals(sl.copy())
            gated[sym] = self.labeler.score_signals(sl, sig)
            oos_data[sym] = sl

        # ---------- 4) Portfolio execution ----------
        kernel = PortfolioExecutionKernel(
            symbols=list(oos_data.keys()),
            risk=RiskConfig(),
            fric=FrictionConfig(),
            ratchet=RatchetConfig(min_target_r=self.targets.get("min_r_multiple", 2.5)),
            max_positions=self.max_positions)
        res = kernel.run(oos_data, gated)

        # ---------- 5) Pass/fail criteria evaluation ----------
        passed = (
            res["roi_pct"] > self.targets["min_roi_percent"]
            and res["max_dd_pct"] < self.targets["max_dd_percent"]
            and res["win_rate_pct"] > self.targets["min_winrate_percent"]
            and res["trades"] >= self.targets["min_trades"]
        )
        row = {
            "window_id": w["window_id"],
            "name": w["name"],
            "start_date": w["start_date"],
            "end_date": w["end_date"],
            "trades": res["trades"],
            "net_pnl": res["net_pnl"],
            "roi_pct": res["roi_pct"],
            "max_dd_pct": res["max_dd_pct"],
            "win_rate_pct": res["win_rate_pct"],
            "passed": passed,
            "cv_auc": fit_info["mean_cv_auc"],
            "tau": fit_info["calibrated_tau"],
            "n_train_events": fit_info["n_events"],
            "pos_rate": fit_info["positive_rate"],
        }
        if verbose:
            tag = "PASS" if passed else "FAIL"
            print(f"W{w['window_id']:02d} | {w['start_date']} -> {w['end_date']} | "
                  f"N {row['trades']:3d} | PnL {row['net_pnl']:+9.2f}$ | "
                  f"ROI {row['roi_pct']:+7.2f}% | DD {row['max_dd_pct']:5.2f}% | "
                  f"WR {row['win_rate_pct']:5.1f}% | AUC {row['cv_auc']:.3f} | "
                  f"tau {row['tau']:.3f} | {tag}")
        return row

    def run_strategy(self, strategy_name: str, verbose: bool = True) -> pd.DataFrame:
        if strategy_name not in self.STRATEGY_CLASSES:
            raise KeyError(f"Strategy '{strategy_name}' not registered. Use MultiAssetWalkForwardRunner.register(...) first.")
        cls = self.STRATEGY_CLASSES[strategy_name]
        rows = [self.run_window(cls, w, verbose=verbose) for w in self.windows]
        df = pd.DataFrame(rows)

        n_pass = int(df["passed"].sum())
        print("=" * 95)
        print(f"STRATEGY: {strategy_name} | PASSED {n_pass}/{len(self.windows)} windows")
        print("=" * 95)
        print(df.to_string(index=False))
        return df

    def run_all(self, verbose: bool = True) -> Dict[str, pd.DataFrame]:
        return {name: self.run_strategy(name, verbose=verbose)
                for name in self.STRATEGY_CLASSES}


# Auto-register all available strategies
def register_standard_strategies():
    from Engine.strategy.s1_liquidation_cascade import LiquidationCascadeSimulator
    from Engine.strategy.s2_institutional_ml import S2InstitutionalMLSimulator
    from Engine.strategy.smc_marco import SMCMarcoSimulator
    from Engine.strategy.smc_edgeful import SMCEdgefulSimulator
    from Engine.strategy.smc_mayne import SMCMayneSimulator
    from Engine.strategy.smc_kane import SMCKaneSimulator
    from Engine.strategy.smc_marci import SMCMarciSimulator
    from Engine.strategy.smc_usman_noah import SMCUsmanNoahSimulator

    MultiAssetWalkForwardRunner.register("s1", LiquidationCascadeSimulator)
    MultiAssetWalkForwardRunner.register("s2", S2InstitutionalMLSimulator)
    MultiAssetWalkForwardRunner.register("marco", SMCMarcoSimulator)
    MultiAssetWalkForwardRunner.register("edgeful", SMCEdgefulSimulator)
    MultiAssetWalkForwardRunner.register("mayne", SMCMayneSimulator)
    MultiAssetWalkForwardRunner.register("kane", SMCKaneSimulator)
    MultiAssetWalkForwardRunner.register("marci", SMCMarciSimulator)
    MultiAssetWalkForwardRunner.register("usman_noah", SMCUsmanNoahSimulator)


if __name__ == "__main__":
    t0 = time.time()
    print("Loading 18 institutional asset parquets...")
    per_symbol = load_symbol_data("Engine/binance_backtesting_data")
    print(f"Successfully loaded {len(per_symbol)} symbols in {time.time()-t0:.2f}s.")

    register_standard_strategies()

    runner = MultiAssetWalkForwardRunner(
        per_symbol_data=per_symbol,
        windows_json_path="Engine/oos_windows_20.json",
        targets_json_path="Engine/target_oos_criteria.json",
        train_lookback_days=365,
        purge_hours=72,
        max_positions=2,
    )

    print("\nRunning S1 Liquidation Cascade Walk-Forward across all 20 windows...")
    res_s1 = runner.run_strategy("s1")
    os.makedirs("results", exist_ok=True)
    res_s1.to_csv("results/s1_pooled_wf_20win.csv", index=False)
