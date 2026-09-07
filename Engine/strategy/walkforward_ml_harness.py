"""
================================================================================
INSTITUTIONAL WALK-FORWARD ML HARNESS
================================================================================
Wraps any base strategy simulator and applies a Machine Learning overlay.
Trains sequentially across 20 OOS windows using causal data.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import json
import time

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    from sklearn.ensemble import RandomForestClassifier
    HAS_XGB = False

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Engine.strategy.smc_mayne import SMCMayneSimulator, RiskConfig, FrictionConfig
from Engine.strategy.smc_marco import SMCMarcoSimulator
from Engine.strategy.smc_kane import SMCKaneSimulator
from Engine.strategy.smc_edgeful import SMCEdgefulSimulator
from Engine.strategy.smc_usman_noah import SMCUsmanNoahSimulator
from Engine.strategy.smc_marci import SMCMarciSimulator

class MLWalkForwardHarness:
    def __init__(self, parquet_path: Path, windows_json: Path, simulator_class):
        self.parquet_path = parquet_path
        self.windows_json = windows_json
        self.simulator_class = simulator_class
        
        with open(windows_json, "r") as f:
            self.windows = json.load(f)
            
        print("Loading Master Data...")
        self.df = pd.read_parquet(parquet_path)
        if "datetime_utc" in self.df.columns and pd.api.types.is_string_dtype(self.df["datetime_utc"]):
            self.df["datetime_utc"] = pd.to_datetime(self.df["datetime_utc"])
        elif "datetime" in self.df.columns and pd.api.types.is_string_dtype(self.df["datetime"]):
            self.df["datetime"] = pd.to_datetime(self.df["datetime"])
            self.df.rename(columns={"datetime": "datetime_utc"}, inplace=True)
            
        print(f"Data Loaded: {len(self.df)} rows")
        
        # Compute Rolling Features
        self.df["long_liq_roll"] = self.df["long_liq_zs"].rolling(4).max().fillna(0)
        self.df["short_liq_roll"] = self.df["short_liq_zs"].rolling(4).max().fillna(0)
        self.df["delta_spot"] = self.df["spot_cvd_15m"].diff().fillna(0)
        self.df["delta_fut"] = self.df["future_cvd_15m"].diff().fillna(0)
        
    def extract_features(self, df: pd.DataFrame, t: int) -> np.ndarray:
        """Extracts the feature vector at bar t"""
        # Features: RSI, VWAP Z-score, Liquidations, CVD, ATR, Vol Ratio
        return np.array([
            df["rsi_14"].iloc[t],
            df["vwap_zscore"].iloc[t],
            df["long_liq_roll"].iloc[t],
            df["short_liq_roll"].iloc[t],
            df["zc_div"].iloc[t],
            df["delta_spot"].iloc[t],
            df["delta_fut"].iloc[t],
            df["volume_ratio"].iloc[t],
            df["ls_ratio_global"].iloc[t] if "ls_ratio_global" in df.columns else 1.0,
            df["atr_14"].iloc[t] / df["close"].iloc[t] * 100.0 # ATR %
        ])
        
    def _run_base_simulation(self, df_train: pd.DataFrame):
        """Runs the simulator in signal-generation mode to collect all raw trades"""
        sim = self.simulator_class(risk_cfg=RiskConfig(), fric_cfg=FrictionConfig())
        return sim.run(df_train, training_mode=True)
        
    def train_model(self, trades: List[Dict], df: pd.DataFrame):
        """Trains the ML classifier on historical trades"""
        X = []
        y = []
        for tr in trades:
            # Reconstruct the feature vector at the exact entry bar
            idx = tr["entry_bar"]
            features = self.extract_features(df, idx)
            X.append(features)
            # Target: 1 if trade hit at least 1.0R (solid base hit), 0 otherwise
            # A good trade is one that reached target or locked in solid profit
            r = tr.get("r", 0.0)
            if r >= 1.0:
                y.append(1)
            else:
                y.append(0)
                
        X = np.array(X)
        y = np.array(y)
        
        if len(y) < 3 or sum(y) < 1:
            print(f"Train model failed: len(y)={len(y)}, sum(y)={sum(y)}")
            return None
            
        if HAS_XGB:
            pos_weight = (len(y) - sum(y)) / sum(y) if sum(y) > 0 else 1.0
            model = XGBClassifier(
                max_depth=4,
                learning_rate=0.05,
                n_estimators=100,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=1.0,
                reg_lambda=3.0,
                scale_pos_weight=pos_weight,
                random_state=42
            )
        else:
            model = RandomForestClassifier(
                n_estimators=100, 
                max_depth=4,
                min_samples_leaf=5,
                random_state=42,
                class_weight='balanced'
            )
            
        model.fit(X, y)
        return model

    def evaluate_window(self, model, df_test: pd.DataFrame, threshold: float = 0.55):
        """Evaluates the test window, filtering trades through the ML model dynamically"""
        def ml_filter(t: int, side: str) -> bool:
            if model is None:
                return True
            X_t = self.extract_features(df_test, t).reshape(1, -1)
            prob = model.predict_proba(X_t)[0][1]
            return prob >= threshold

        sim = self.simulator_class(risk_cfg=RiskConfig(), fric_cfg=FrictionConfig())
        res = sim.run(df_test, filter_func=ml_filter)
        return {
            "roi_pct": res["roi_pct"],
            "max_dd_pct": res["max_dd_pct"],
            "win_rate_pct": res["win_rate_pct"],
            "trades": res["trades"],
            "net_pnl": res["net_pnl"]
        }

    def run_walkforward(self):
        print("=" * 80)
        print(f"ML WALK-FORWARD HARNESS – {self.simulator_class.__name__}")
        print("=" * 80)
        
        results = []
        
        # Determine the start of the first window
        w1_start = pd.to_datetime(self.windows[0]["start_date"])
        
        for w_idx, w in enumerate(self.windows, start=1):
            w_name = w["name"]
            win_start = pd.to_datetime(w["start_date"])
            win_end = pd.to_datetime(w["end_date"]) + pd.Timedelta(days=1)
            
            # 1. Train Data: All data prior to this window (up to win_start - 72h)
            train_end = win_start - pd.Timedelta(hours=72)
            df_train = self.df[self.df["datetime_utc"] < train_end].copy().reset_index(drop=True)
            
            # 2. Test Data: The current window (+72h purge history)
            purge_start = win_start - pd.Timedelta(hours=72)
            df_test = self.df[(self.df["datetime_utc"] >= purge_start) & (self.df["datetime_utc"] < win_end)].copy().reset_index(drop=True)
            
            if len(df_test) < 100:
                print(f"Skipping W{w_idx:02d} (Not enough data)")
                continue
                
            t0 = time.time()
            
            # Train ML Model
            model = None
            threshold = 0.50
            if len(df_train) > 1000:
                raw_train_res = self._run_base_simulation(df_train)
                model = self.train_model(raw_train_res["trades_list"], df_train)
                # Optimize threshold
                if model:
                    best_roi = -999
                    best_th = 0.50
                    for th in [0.35, 0.40, 0.45, 0.50, 0.55, 0.60]:
                        eval_res = self.evaluate_window(model, df_train[-10000:], threshold=th)
                        if eval_res["roi_pct"] > best_roi and eval_res["trades"] >= 5:
                            best_roi = eval_res["roi_pct"]
                            best_th = th
                    threshold = best_th
                    
            # Evaluate on OOS Window
            res = self.evaluate_window(model, df_test, threshold=threshold)
            t1 = time.time()
            
            status = "PASS" if (res["roi_pct"] > 20.0 and res["max_dd_pct"] < 5.0 and res["win_rate_pct"] > 40.0 and res["trades"] >= 6) else "FAIL"
            
            print(f"[{status}] W{w_idx:02d} | ML Thresh: {threshold:.2f} | ROI: {res['roi_pct']:+.2f}% | MaxDD: {res['max_dd_pct']:.2f}% | WR: {res['win_rate_pct']:.1f}% | Trades: {res['trades']} | Time: {t1-t0:.2f}s")
            
            results.append({
                "w_idx": w_idx,
                "name": w_name,
                "roi": res["roi_pct"],
                "mdd": res["max_dd_pct"],
                "wr": res["win_rate_pct"],
                "trades": res["trades"],
                "status": status
            })
            
            if status == "FAIL" and "--strict-fail-fast" in sys.argv:
                print("\n[!] STRICT FAIL-FAST TRIGGERED. Halting optimization.")
                break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", type=str, default="mayne", choices=["mayne", "marco", "kane", "edgeful", "usman", "marci"])
    args, unknown = parser.parse_known_args()
    
    mapping = {
        "mayne": SMCMayneSimulator,
        "marco": SMCMarcoSimulator,
        "kane": SMCKaneSimulator,
        "edgeful": SMCEdgefulSimulator,
        "usman": SMCUsmanNoahSimulator,
        "marci": SMCMarciSimulator
    }
    
    harness = MLWalkForwardHarness(
        Path("Engine/binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet"),
        Path("Engine/oos_windows_20.json"),
        mapping[args.strategy]
    )
    harness.run_walkforward()
