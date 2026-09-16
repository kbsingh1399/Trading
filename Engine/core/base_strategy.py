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
        w_path = Path(windows_path) if windows_path else engine_dir / "oos_windows_20.json"

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
