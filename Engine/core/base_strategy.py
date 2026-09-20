"""
================================================================================
CORE: BASE STRATEGY & CONFIGURATION ARCHITECTURE FOR FOREX & CFD ENGINES
================================================================================
Location: Engine/core/base_strategy.py
Architecture: Modular SRP, Type-Safe, Extensible Strategy Plugin Pattern

Provides the canonical contract and configuration abstractions for:
1. Target Criteria ingestion (target_oos_criteria.json)
2. 20 OOS Window definitions (oos_windows_20.json)
3. Standardized Strategy Signal & Backtest Result data schemas
4. Abstract Base Strategy (BaseForexStrategy) interface
5. Dynamic Strategy Registry (StrategyRegistry) for frictionless plug-and-play
================================================================================
"""
from __future__ import annotations

import os
import sys
import json
import logging
import importlib.util
from abc import ABC, abstractmethod
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Type

import numpy as np
import pandas as pd


# -------------------------------------------------------------------------
# 1. CONFIGURATION DATA MODELS
# -------------------------------------------------------------------------
@dataclass
class TargetCriteria:
    min_roi_percent: float = 10.0
    max_dd_percent: float = 5.0
    min_winrate_percent: float = 40.0
    min_r_multiple: float = 4.0
    min_trades: int = 15
    risk_per_trade_percent: float = 1.0
    initial_capital_usd: float = 5000.0
    base_risk_usd: float = 50.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TargetCriteria:
        tc = data.get("target_criteria", data)
        return cls(
            min_roi_percent=float(tc.get("min_roi_percent", 10.0)),
            max_dd_percent=float(tc.get("max_dd_percent", 5.0)),
            min_winrate_percent=float(tc.get("min_winrate_percent", 40.0)),
            min_r_multiple=float(tc.get("min_r_multiple", 4.0)),
            min_trades=int(tc.get("min_trades", 15)),
            risk_per_trade_percent=float(tc.get("risk_per_trade_percent", 1.0)),
            initial_capital_usd=float(tc.get("initial_capital_usd", 5000.0)),
            base_risk_usd=float(tc.get("base_risk_usd", 50.0)),
        )


@dataclass
class ExecutionMode:
    parallel_assets: bool = True
    total_assets: int = 18
    optimization_mode: str = "individual_asset_best"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ExecutionMode:
        em = data.get("execution_mode", data)
        return cls(
            parallel_assets=bool(em.get("parallel_assets", True)),
            total_assets=int(em.get("total_assets", 18)),
            optimization_mode=str(em.get("optimization_mode", "individual_asset_best")),
        )


@dataclass
class OOSWindow:
    window_id: int
    name: str
    start_date: str
    end_date: str
    regime: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> OOSWindow:
        return cls(
            window_id=int(data["window_id"]),
            name=str(data.get("name", f"Window {data['window_id']}")),
            start_date=str(data["start_date"]),
            end_date=str(data["end_date"]),
            regime=str(data.get("regime", "Unknown")),
            description=str(data.get("description", "")),
        )


class EngineConfig:
    """Robust parser and provider for trading engine criteria and OOS windows."""
    def __init__(
        self,
        criteria: Optional[TargetCriteria] = None,
        execution_mode: Optional[ExecutionMode] = None,
        windows: Optional[List[OOSWindow]] = None,
        criteria_path: Optional[Path] = None,
        windows_path: Optional[Path] = None
    ):
        self.criteria = criteria or TargetCriteria()
        self.execution_mode = execution_mode or ExecutionMode()
        self.windows = windows or []
        self.criteria_path = criteria_path
        self.windows_path = windows_path

    @classmethod
    def load(
        cls,
        criteria_path: Optional[Path | str] = None,
        windows_path: Optional[Path | str] = None
    ) -> EngineConfig:
        engine_dir = Path(__file__).resolve().parent.parent
        c_path = Path(criteria_path) if criteria_path else engine_dir / "target_oos_criteria.json"
        forex_w = engine_dir / "oos_windows_forex_20.json"
        default_w = forex_w if forex_w.exists() else (engine_dir / "oos_windows_20.json")
        w_path = Path(windows_path) if windows_path else default_w

        target_crit = TargetCriteria()
        exec_mode = ExecutionMode()
        if c_path.exists():
            try:
                with open(c_path, "r", encoding="utf-8") as f:
                    raw_c = json.load(f)
                target_crit = TargetCriteria.from_dict(raw_c)
                exec_mode = ExecutionMode.from_dict(raw_c)
                logging.info(f"Loaded criteria from {c_path}")
            except Exception as e:
                logging.error(f"Failed to parse criteria JSON at {c_path}: {e}")
        else:
            logging.warning(f"Criteria file not found at {c_path}, using defaults.")

        windows_list: List[OOSWindow] = []
        if w_path.exists():
            try:
                with open(w_path, "r", encoding="utf-8") as f:
                    raw_w = json.load(f)
                if isinstance(raw_w, list):
                    for w in raw_w:
                        windows_list.append(OOSWindow.from_dict(w))
                logging.info(f"Loaded {len(windows_list)} OOS windows from {w_path}")
            except Exception as e:
                logging.error(f"Failed to parse windows JSON at {w_path}: {e}")
        else:
            logging.warning(f"Windows file not found at {w_path}.")

        return cls(
            criteria=target_crit,
            execution_mode=exec_mode,
            windows=windows_list,
            criteria_path=c_path,
            windows_path=w_path
        )

    def get_window(self, window_id: int) -> Optional[OOSWindow]:
        for w in self.windows:
            if w.window_id == window_id:
                return w
        return None

    def evaluate_pass_criteria(
        self,
        metrics: Dict[str, Any]
    ) -> Tuple[bool, Dict[str, bool], List[str]]:
        """Evaluates whether backtest metrics satisfy target OOS criteria."""
        roi = float(metrics.get("net_roi_pct", metrics.get("roi", 0.0)))
        max_dd = abs(float(metrics.get("max_dd_pct", metrics.get("max_dd", 0.0))))
        win_rate = float(metrics.get("win_rate", 0.0))
        trades = int(metrics.get("total_trades", metrics.get("trades", 0)))
        net_r = float(metrics.get("net_r", 0.0))

        checks = {
            "roi": roi >= self.criteria.min_roi_percent,
            "max_dd": max_dd <= self.criteria.max_dd_percent,
            "win_rate": win_rate >= self.criteria.min_winrate_percent,
            "trades": trades >= self.criteria.min_trades,
            "min_r": net_r >= self.criteria.min_r_multiple,
        }

        failures = []
        if not checks["roi"]:
            failures.append(f"ROI ({roi:+.2f}%) < Target ({self.criteria.min_roi_percent:+.2f}%)")
        if not checks["max_dd"]:
            failures.append(f"Max DD ({max_dd:.2f}%) > Limit ({self.criteria.max_dd_percent:.2f}%)")
        if not checks["win_rate"]:
            failures.append(f"Win Rate ({win_rate:.1f}%) < Target ({self.criteria.min_winrate_percent:.1f}%)")
        if not checks["trades"]:
            failures.append(f"Trades ({trades}) < Target ({self.criteria.min_trades})")
        if not checks["min_r"]:
            failures.append(f"Net R ({net_r:+.2f}R) < Target ({self.criteria.min_r_multiple:+.2f}R)")

        overall_pass = all(checks.values())
        return overall_pass, checks, failures


# -------------------------------------------------------------------------
# 2. STANDARDIZED STRATEGY SIGNAL & RESULTS SCHEMAS
# -------------------------------------------------------------------------
@dataclass
class StrategySignal:
    symbol: str
    signal: int  # 1: BUY, -1: SELL, 0: FLAT / HOLD
    prob: float = 0.0
    entry_price: float = 0.0
    sl_price: float = 0.0
    tp_price: float = 0.0
    risk_usd: float = 50.0
    strategy_tag: str = ""
    reason: str = "HOLD"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_buy(self) -> bool:
        return self.signal > 0

    @property
    def is_sell(self) -> bool:
        return self.signal < 0

    @property
    def is_active(self) -> bool:
        return self.signal != 0


@dataclass
class BacktestResult:
    strategy_name: str
    start_date: str
    end_date: Optional[str]
    window_id: Optional[int]
    total_trades: int
    win_rate: float
    profit_factor: float
    net_r: float
    net_pnl_usd: float
    net_roi_pct: float
    max_dd_pct: float
    buy_hold_return_pct: float
    passed_criteria: bool
    criteria_checks: Dict[str, bool] = field(default_factory=dict)
    failure_reasons: List[str] = field(default_factory=list)
    per_asset_summary: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    trades_df: Optional[pd.DataFrame] = None


# -------------------------------------------------------------------------
# 3. ABSTRACT BASE STRATEGY INTERFACE
# -------------------------------------------------------------------------
class BaseForexStrategy(ABC):
    """Canonical abstract base class for all Forex & CFD trading strategies."""
    name: str = "base_strategy"
    description: str = "Base Strategy Interface"

    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig.load()
        self.initialized = False

    @abstractmethod
    def initialize(self, config: Optional[EngineConfig] = None) -> None:
        """Initializes model weights, indicators, buffers, and configurations."""
        pass

    @abstractmethod
    def generate_signal(
        self,
        symbol: str,
        buffer_15m: pd.DataFrame,
        buffer_4h: Optional[pd.DataFrame] = None,
        current_tick: Optional[Any] = None
    ) -> StrategySignal:
        """Generates real-time trade signals from latest market buffers."""
        pass

    @abstractmethod
    def run_backtest(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        save_plot: bool = True
    ) -> BacktestResult:
        """Executes full historical backtest / walk-forward evaluation."""
        pass


# -------------------------------------------------------------------------
# 4. STRATEGY REGISTRY (FACTORY PATTERN)
# -------------------------------------------------------------------------
class StrategyRegistry:
    """Central registry and factory for plug-and-play trading strategies."""
    _strategies: Dict[str, Type[BaseForexStrategy]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register a strategy class by unique key."""
        def decorator(subclass: Type[BaseForexStrategy]):
            key = name.lower()
            cls._strategies[key] = subclass
            return subclass
        return decorator

    @classmethod
    def get(cls, name: str) -> Type[BaseForexStrategy]:
        """Retrieves a registered strategy class by name."""
        key = name.lower()
        if key not in cls._strategies:
            available = ", ".join(cls._strategies.keys())
            raise KeyError(f"Strategy '{name}' not found in registry. Available: [{available}]")
        return cls._strategies[key]

    @classmethod
    def list_strategies(cls) -> List[str]:
        """Lists all currently registered strategy keys."""
        return list(cls._strategies.keys())

    @classmethod
    def load_from_module(
        cls,
        module_path: str | Path,
        class_name: Optional[str] = None
    ) -> Type[BaseForexStrategy]:
        """Dynamically imports a Python file and extracts a BaseForexStrategy subclass."""
        path = Path(module_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Strategy module file not found: {path}")

        module_name = f"dynamic_strat_{path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, str(path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module specification from {path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Find target class
        if class_name:
            target_cls = getattr(module, class_name, None)
            if target_cls and issubclass(target_cls, BaseForexStrategy):
                return target_cls
            raise AttributeError(f"Class '{class_name}' in {path} does not inherit from BaseForexStrategy")

        # Auto-discover subclass of BaseForexStrategy
        candidates = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, BaseForexStrategy)
                and attr is not BaseForexStrategy
            ):
                candidates.append(attr)

        if not candidates:
            raise ValueError(f"No BaseForexStrategy subclass found in {path}")

        return candidates[0]


# -------------------------------------------------------------------------
# 5. PARALLEL MULTI-SLEEVE STRATEGY
# -------------------------------------------------------------------------
FOREX_CLUSTER_MAP: Dict[str, str] = {
    'EURUSD': 'EUR', 'EURHUF': 'EUR', 'EURSEK': 'EUR', 'EURCNH': 'EUR', 'AUDCHF': 'EUR',
    'NZDUSD': 'PACIFIC', 'USDHKD': 'PACIFIC', 'NZDCNH': 'PACIFIC', 'USDSEK': 'PACIFIC',
    'GER40': 'EQUITY', 'GER30': 'EQUITY', 'FR40': 'EQUITY', 'AU200': 'EQUITY', 'US2000': 'EQUITY',
    'GAS': 'COMMODITY', 'NICKEL': 'COMMODITY', 'LEAD': 'COMMODITY', 'XAUCNH': 'COMMODITY', 'GAUCNH': 'COMMODITY'
}


@StrategyRegistry.register("parallel")
@StrategyRegistry.register("dual")
@StrategyRegistry.register("all")
class ParallelForexStrategy(BaseForexStrategy):
    """
    Parallel Multi-Sleeve Execution Strategy.
    Simultaneously executes multiple registered strategies (e.g. FVG_ML + ORB_CRT)
    across all assets in parallel, evaluating independent sleeve signals, confluence,
    and enforcing institutional portfolio concurrency, cluster limits, and dynamic risk.
    """
    name: str = "parallel"
    description: str = "Dual-Sleeve Parallel Strategy (FVG_ML + ORB_CRT)"

    def __init__(self, config: Optional[EngineConfig] = None, strategy_names: Optional[List[str]] = None):
        super().__init__(config=config)
        self.strategy_names = strategy_names or ["fvg_ml", "orb_crt"]
        self.sleeves: Dict[str, BaseForexStrategy] = {}
        self._cached_candidate_trades: Optional[pd.DataFrame] = None
        self.initialize(self.config)

    def initialize(self, config: Optional[EngineConfig] = None) -> None:
        if config is not None:
            self.config = config
        
        # Ensure strategy sleeves are registered in StrategyRegistry
        try:
            import Engine.strategy.s4_fvg_ml.s4_fvg_ml_forex_engine
        except Exception:
            try:
                import Engine.strategy.s4_fvg_ml.s4_fvg_ml_forex
            except Exception:
                pass
        try:
            import Engine.strategy.orb_crt_forex_engine
        except Exception:
            try:
                import Engine.strategy.orb_crt_forex
            except Exception:
                pass

        self.sleeves = {}
        for s_name in self.strategy_names:
            try:
                s_cls = StrategyRegistry.get(s_name)
                s_inst = s_cls(config=self.config)
                s_inst.initialize(self.config)
                self.sleeves[s_name] = s_inst
                logging.info(f"Parallel sleeve '{s_name}' loaded successfully.")
            except Exception as e:
                logging.warning(f"Could not load parallel sleeve '{s_name}': {e}")
        self.initialized = True

    def precompute_candidates(
        self,
        start_date: str = "2023-09-01",
        end_date: str = "2026-03-31",
        symbols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Precomputes and caches candidate trade setups across all sleeves for ultra-fast walk-forward."""
        all_candidates = []
        for name, strat in self.sleeves.items():
            try:
                res = strat.run_backtest(start_date=start_date, end_date=end_date, symbols=symbols, save_plot=False)
                if res.trades_df is not None and not res.trades_df.empty:
                    tdf = res.trades_df.copy()
                    tdf["sleeve"] = strat.name.upper()
                    if "hold_bars" not in tdf.columns:
                        tdf["hold_bars"] = 24 if "FVG" in strat.name.upper() else 30
                    if "cluster" not in tdf.columns:
                        tdf["cluster"] = tdf["asset"].map(lambda x: FOREX_CLUSTER_MAP.get(x, "OTHER"))
                    all_candidates.append(tdf)
            except Exception as e:
                logging.warning(f"Error precomputing candidate setups for sleeve '{name}': {e}")

        if all_candidates:
            comb = pd.concat(all_candidates, ignore_index=True)
            comb["datetime"] = pd.to_datetime(comb["datetime"], utc=True)
            self._cached_candidate_trades = comb.sort_values("datetime").reset_index(drop=True)
        else:
            self._cached_candidate_trades = pd.DataFrame()
        return self._cached_candidate_trades

    def generate_signal(
        self,
        symbol: str,
        buffer_15m: pd.DataFrame,
        buffer_4h: Optional[pd.DataFrame] = None,
        current_tick: Optional[Any] = None
    ) -> StrategySignal:
        active_signals: List[Tuple[str, StrategySignal]] = []
        hold_reasons: List[str] = []

        for name, strat in self.sleeves.items():
            try:
                sig = strat.generate_signal(symbol, buffer_15m, buffer_4h, current_tick=current_tick)
                if sig.is_active:
                    active_signals.append((name, sig))
                else:
                    hold_reasons.append(f"{strat.name.upper()}:{sig.reason}")
            except Exception as e:
                hold_reasons.append(f"{name.upper()}:Error({e})")

        if not active_signals:
            summary_reason = " | ".join(hold_reasons) if hold_reasons else "HOLD"
            return StrategySignal(symbol=symbol, signal=0, reason=summary_reason)

        if len(active_signals) >= 2:
            s1_name, sig1 = active_signals[0]
            s2_name, sig2 = active_signals[1]
            if sig1.signal == sig2.signal:
                return StrategySignal(
                    symbol=symbol,
                    signal=sig1.signal,
                    prob=max(sig1.prob, sig2.prob),
                    entry_price=sig1.entry_price,
                    sl_price=sig1.sl_price,
                    tp_price=sig1.tp_price,
                    risk_usd=sig1.risk_usd,
                    strategy_tag="DUAL(FVG+ORB)",
                    reason=f"CONFLUENCE: {sig1.strategy_tag} + {sig2.strategy_tag}",
                    metadata={"s1": sig1.metadata, "s2": sig2.metadata}
                )
            else:
                s1_dir = "BUY" if sig1.signal > 0 else "SELL"
                s2_dir = "BUY" if sig2.signal > 0 else "SELL"
                return StrategySignal(
                    symbol=symbol,
                    signal=0,
                    reason=f"CONFLICT VETO: {sig1.strategy_tag}({s1_dir}) vs {sig2.strategy_tag}({s2_dir})"
                )

        return active_signals[0][1]

    def run_backtest(
        self,
        start_date: str = "2025-12-01",
        end_date: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        save_plot: bool = True
    ) -> BacktestResult:
        criteria = self.config.criteria
        initial_capital = criteria.initial_capital_usd
        base_risk = criteria.base_risk_usd
        dd_mult = 0.55
        house_mult = 1.30
        pass_lock_mult = 0.15

        # Obtain candidates from cache or compute on-the-fly
        if self._cached_candidate_trades is not None and not self._cached_candidate_trades.empty:
            candidates = self._cached_candidate_trades.copy()
            if start_date:
                s_dt = pd.to_datetime(start_date, utc=True)
                candidates = candidates[candidates["datetime"] >= s_dt]
            if end_date:
                e_dt = pd.to_datetime(end_date, utc=True)
                candidates = candidates[candidates["datetime"] <= e_dt]
            if symbols:
                candidates = candidates[candidates["asset"].isin(symbols)]
        else:
            all_candidates = []
            for name, strat in self.sleeves.items():
                try:
                    res = strat.run_backtest(start_date=start_date, end_date=end_date, symbols=symbols, save_plot=False)
                    if res.trades_df is not None and not res.trades_df.empty:
                        tdf = res.trades_df.copy()
                        tdf["sleeve"] = strat.name.upper()
                        if "hold_bars" not in tdf.columns:
                            tdf["hold_bars"] = 24 if "FVG" in strat.name.upper() else 30
                        if "cluster" not in tdf.columns:
                            tdf["cluster"] = tdf["asset"].map(lambda x: FOREX_CLUSTER_MAP.get(x, "OTHER"))
                        all_candidates.append(tdf)
                except Exception as e:
                    logging.warning(f"Error executing backtest for sleeve '{name}': {e}")

            if all_candidates:
                comb = pd.concat(all_candidates, ignore_index=True)
                comb["datetime"] = pd.to_datetime(comb["datetime"], utc=True)
                candidates = comb.sort_values("datetime").reset_index(drop=True)
            else:
                candidates = pd.DataFrame()

        if candidates.empty:
            return BacktestResult(
                strategy_name="parallel_dual_sleeve",
                start_date=start_date,
                end_date=end_date,
                window_id=None,
                total_trades=0,
                win_rate=0.0,
                profit_factor=0.0,
                net_r=0.0,
                net_pnl_usd=0.0,
                net_roi_pct=0.0,
                max_dd_pct=0.0,
                buy_hold_return_pct=0.0,
                passed_criteria=False,
                failure_reasons=["No candidate trades found for parallel execution"],
                per_asset_summary={},
                trades_df=pd.DataFrame()
            )

        active_positions: List[Dict[str, Any]] = []
        executed: List[Dict[str, Any]] = []
        w_eq = initial_capital
        w_peak = initial_capital
        w_curve = [w_eq]
        w_in_defense = False

        for _, row in candidates.iterrows():
            t_entry = row["datetime"]
            cluster = row.get("cluster", FOREX_CLUSTER_MAP.get(row["asset"], "OTHER"))
            asset = row["asset"]
            r_real = float(row.get("r_realized", row.get("outcome_r", 0.0)))
            sleeve = row.get("sleeve", "PARALLEL")
            bars_held = int(row.get("hold_bars", 24))

            # Expire finished positions
            active_positions = [p for p in active_positions if p["exit_time"] > t_entry]

            # Concurrency Invariant: Max 2 concurrent positions across portfolio
            if len(active_positions) >= 2:
                continue
            # Cluster Invariant: Max 1 position per currency/asset cluster
            if any(p["cluster"] == cluster for p in active_positions):
                continue
            # Asset Invariant: Max 1 position per individual asset
            if any(p["asset"] == asset for p in active_positions):
                continue

            curr_dd = (w_peak - w_eq) / w_peak * 100.0 if w_peak > 0 else 0.0
            dd_usd = max(0.0, w_peak - w_eq)
            current_pnl = w_eq - initial_capital
            n_done = len(executed)

            # Institutional Dynamic Risk State Machine (100% Parity with Live Governor)
            if curr_dd >= 4.50 or dd_usd >= 225.0:
                # Hard Freeze: Portfolio hit 4.5% / $225 limit - freeze further execution
                w_in_defense = True
                continue
            elif current_pnl >= 500.0 and n_done >= 15:
                risk = base_risk * pass_lock_mult
            elif curr_dd >= 3.0:
                w_in_defense = True
                risk = base_risk * dd_mult * 0.60
            elif curr_dd >= 1.8 or (w_in_defense and curr_dd >= 1.50):
                w_in_defense = True
                risk = base_risk * dd_mult
            else:
                w_in_defense = False
                if current_pnl >= 80.0 and curr_dd < 1.0:
                    risk = base_risk * house_mult
                else:
                    risk = base_risk

            # Transaction friction (8 bps on risk allocation)
            pnl = r_real * risk - (risk * 0.0008)
            w_eq += pnl
            if w_eq > w_peak:
                w_peak = w_eq
            w_curve.append(w_eq)

            exit_time = t_entry + pd.Timedelta(minutes=15 * bars_held)
            active_positions.append({"exit_time": exit_time, "cluster": cluster, "asset": asset})
            executed.append({
                "datetime": t_entry,
                "asset": asset,
                "cluster": cluster,
                "sleeve": sleeve,
                "r_realized": r_real,
                "outcome_r": r_real,
                "risk_usd": risk,
                "pnl": pnl,
                "pnl_usd": pnl,
                "equity": w_eq,
                "exit_time": exit_time
            })

        if not executed:
            return BacktestResult(
                strategy_name="parallel_dual_sleeve",
                start_date=start_date,
                end_date=end_date,
                window_id=None,
                total_trades=0,
                win_rate=0.0,
                profit_factor=0.0,
                net_r=0.0,
                net_pnl_usd=0.0,
                net_roi_pct=0.0,
                max_dd_pct=0.0,
                buy_hold_return_pct=0.0,
                passed_criteria=False,
                failure_reasons=["All candidate trades filtered by concurrency or cluster limits"],
                per_asset_summary={},
                trades_df=pd.DataFrame()
            )

        ex_df = pd.DataFrame(executed)
        ex_df["cum_pnl"] = ex_df["pnl_usd"].cumsum()
        ex_df["equity"] = initial_capital + ex_df["cum_pnl"]
        ex_df["peak"] = ex_df["equity"].cummax()
        ex_df["dd"] = (ex_df["peak"] - ex_df["equity"]) / ex_df["peak"]

        curve_arr = np.array(w_curve)
        pks = np.maximum.accumulate(curve_arr)
        max_dd = float(np.max((pks - curve_arr) / pks) * 100.0) if len(curve_arr) > 0 else 0.0

        total_trades = len(ex_df)
        wins = ex_df[ex_df["pnl_usd"] > 0]
        losses = ex_df[ex_df["pnl_usd"] < 0]
        win_rate = (len(wins) / total_trades * 100.0) if total_trades > 0 else 0.0

        gross_profit = wins["pnl_usd"].sum() if not wins.empty else 0.0
        gross_loss = abs(losses["pnl_usd"].sum()) if not losses.empty else 0.0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 99.9

        net_pnl = float(ex_df["pnl_usd"].sum())
        net_r = float(ex_df["r_realized"].sum())
        net_roi = (net_pnl / initial_capital) * 100.0

        per_asset = {}
        all_syms = symbols or (list(ex_df["asset"].unique()) if "asset" in ex_df.columns else [])
        for sym in all_syms:
            sym_trades = ex_df[ex_df["asset"] == sym]
            n_t = len(sym_trades)
            if n_t > 0:
                w_t = (sym_trades["pnl_usd"] > 0).sum()
                wr_t = (w_t / n_t * 100.0)
                tot_r_t = float(sym_trades["r_realized"].sum())
                pnl_t = float(sym_trades["pnl_usd"].sum())
                per_asset[sym] = {"trades": n_t, "win_rate": wr_t, "net_r": tot_r_t, "pnl": pnl_t}
            else:
                per_asset[sym] = {"trades": 0, "win_rate": 0.0, "net_r": 0.0, "pnl": 0.0}

        passed_crit, checks, failures = self.config.evaluate_pass_criteria({
            "net_roi_pct": net_roi,
            "max_dd_pct": max_dd,
            "win_rate": win_rate,
            "total_trades": total_trades,
            "net_r": net_r
        })

        if save_plot:
            try:
                import matplotlib
                matplotlib.use('Agg')
                import matplotlib.pyplot as plt
                plot_dir = Path("Engine/artifacts")
                plot_dir.mkdir(parents=True, exist_ok=True)
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

                ax1.plot(ex_df.index, ex_df["equity"], label="Parallel Dual-Sleeve Portfolio Equity", color="#00ffcc", lw=1.8)
                ax1.axhline(initial_capital, color="gray", linestyle="--", alpha=0.5, label="Initial Capital (5,000 USD)")
                ax1.set_title("Parallel Dual-Sleeve (FVG_ML + ORB_CRT) Governed Equity Curve", fontsize=13, fontweight="bold", pad=10)
                ax1.set_ylabel("Account Equity (USD)", fontsize=10)
                ax1.grid(True, alpha=0.25)
                ax1.legend(loc="upper left")

                ax2.fill_between(ex_df.index, -ex_df["dd"] * 100.0, 0, color="#ff3366", alpha=0.4, label="Underwater Drawdown (%)")
                ax2.axhline(-self.config.criteria.max_dd_percent, color="red", linestyle=":", label=f"Max Allowed DD (-{self.config.criteria.max_dd_percent}%)")
                ax2.set_ylabel("Drawdown %", fontsize=10)
                ax2.set_xlabel("Completed Trade Index", fontsize=10)
                ax2.grid(True, alpha=0.25)
                ax2.legend(loc="lower left")

                plt.tight_layout()
                plot_path = plot_dir / "parallel_forex_equity_curve.png"
                fig.savefig(plot_path, dpi=300)
                plt.close(fig)
            except Exception as e:
                logging.warning(f"Could not generate plot: {e}")

        return BacktestResult(
            strategy_name="parallel_dual_sleeve",
            start_date=start_date,
            end_date=end_date,
            window_id=None,
            total_trades=total_trades,
            win_rate=win_rate,
            profit_factor=profit_factor,
            net_r=net_r,
            net_pnl_usd=net_pnl,
            net_roi_pct=net_roi,
            max_dd_pct=max_dd,
            buy_hold_return_pct=0.0,
            passed_criteria=passed_crit,
            criteria_checks=checks,
            failure_reasons=failures,
            per_asset_summary=per_asset,
            trades_df=ex_df
        )

