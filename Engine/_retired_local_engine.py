"""
================================================================================
INSTITUTIONAL QUANTITATIVE MASTER LOCAL TRADING ENGINE
================================================================================
Module: Engine/local_engine.py
Architecture: Deep Module (Clean Code, Karpathy Directives, Unified Execution)

Settled Quantitative Invariants:
1. Universe: 11 Certified Genuine Binance USDT-M Perpetuals
   (BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH)
2. Directional Separation: Independent LightGBM + Ridge foundations trained strictly
   on in-sample causal data with a 72-hour quarantine purge (t_purge = t_start - 72h).
3. Microstructure Ratchets & Gating:
   - S1: 15m liquidation sweep pullback with Cont-Stoikov microstructure gates.
   - T1: 4h pure Donchian channel breakout with Spot CVD confirmation.
   - Piecewise Ratchet: BE lock at +0.70R to +0.80R, Profit lock at +1.50R, Target +2.20R to +2.50R.
   - Realistic Friction: 41.0 bps round-trip drag modeled per trade (-0.25R).
4. Asymmetric Risk Budgeting & Feedback Control:
   - 5,000.00 USD initial capital base.
   - Base Risk: 54.00 USD | House Money Cap: 90.00 USD (compounding rate: 0.20 above 50 USD).
   - Two-Stage Profit Protection Floor: Arms at +180.00 USD, locks floor at +75.00 USD.
   - Circuit Defense: 14.00 USD risk armed when drawdown >= 2.0% or consec_losses >= 2.
   - Mathematical Invariant: win_r_reset_thresh = 0.90 (scratch wins do not reset loss penalty).
   - Causal Covariate Shift Calibration: -0.025 probability threshold shift when trailing 30d ATR < 0.92%.

Execution Modes:
- 'oos': Evaluates all 20 canonical Out-Of-Sample benchmark quarterly windows (2021-2026).
- 'window': Evaluates a single specific OOS window (e.g. Window 12 or 14) with full trade tracing.
- 'custom': Evaluates any arbitrary user-defined date range with strictly causal prior data.
================================================================================
"""

from __future__ import annotations

import os
import sys
import time
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd

# Add repository root to Python path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scratch.fast_numba_oos_engine import (
    compile_dataset_with_numba,
    WINDOWS_PATH,
    CRITERIA_PATH,
)
from Engine.strategy._retired_s1_dual_model_orderflow import (
    InstitutionalDualModelEngine,
)


@dataclass(frozen=True)
class EngineConfig:
    """Immutable institutional risk, execution, and universe configuration."""
    capital: float = 5000.0
    base_risk: float = 54.0
    house_risk_max: float = 90.0
    defense_risk: float = 14.0
    milestone_risk: float = 10.0
    trans_risk: float = 35.0
    trans_thresh: float = 480.0
    t1_base_risk: float = 42.0
    t1_trans_risk: float = 22.0
    cushion_multiplier: float = 0.25
    milestone_profit_usd: float = 500.0
    max_concurrent: int = 3
    max_s1_concurrent: int = 2
    max_t1_concurrent: int = 2
    cooldown_bars: int = 4
    win_r_reset_thresh: float = 0.90
    conf_prob_thresh: float = 0.46
    conf_mult: float = 1.35
    max_dd_limit: float = 4.40
    stage1_arm_profit: float = 180.0
    stage1_floor_profit: float = 75.0
    house_compounding_rate: float = 0.20
    house_compounding_start: float = 50.0
    purge_hours: int = 72
    round_trip_friction_bps: float = 41.0
    random_state: int = 42


@dataclass
class TradeRecord:
    """Detailed record of an executed trade event."""
    trade_id: int
    entry_time: str
    exit_time: str
    symbol: str
    strategy: str
    realized_r: float
    risk_usd: float
    pnl_usd: float
    running_equity: float
    running_dd_pct: float
    win: int
    hold_bars: int


@dataclass
class ExecutionSummary:
    """Statistical and performance summary for an evaluation window or period."""
    name: str
    start_date: str
    end_date: str
    trades: int
    s1_trades: int
    t1_trades: int
    wins: int
    win_rate: float
    net_pnl: float
    net_roi: float
    max_dd: float
    profit_factor: float
    avg_r: float
    expectancy_usd: float
    status: str
    trades_detail: List[TradeRecord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["trades_detail"] = [asdict(t) for t in self.trades_detail]
        return d


class LocalTradingEngine:
    """Deep module orchestrating data compilation, model training, and trade execution."""

    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self.reports_dir = REPO_ROOT / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir = REPO_ROOT / "scratch" / "cache_multi_tf"

        # Instantiate strategy core
        self.strategy_engine = InstitutionalDualModelEngine(
            capital=self.config.capital,
            base_risk=self.config.base_risk,
            house_risk_max=self.config.house_risk_max,
            defense_risk=self.config.defense_risk,
            milestone_risk=self.config.milestone_risk,
            trans_risk=self.config.trans_risk,
            trans_thresh=self.config.trans_thresh,
            t1_base_risk=self.config.t1_base_risk,
            t1_trans_risk=self.config.t1_trans_risk,
            cushion_multiplier=self.config.cushion_multiplier,
            milestone_profit_usd=self.config.milestone_profit_usd,
            max_concurrent=self.config.max_concurrent,
            max_s1_concurrent=self.config.max_s1_concurrent,
            max_t1_concurrent=self.config.max_t1_concurrent,
            cooldown_bars=self.config.cooldown_bars,
            win_r_reset_thresh=self.config.win_r_reset_thresh,
            conf_prob_thresh=self.config.conf_prob_thresh,
            conf_mult=self.config.conf_mult,
            max_dd_limit=self.config.max_dd_limit,
            stage1_arm_profit=self.config.stage1_arm_profit,
            stage1_floor_profit=self.config.stage1_floor_profit,
            house_compounding_rate=self.config.house_compounding_rate,
            house_compounding_start=self.config.house_compounding_start,
            random_state=self.config.random_state,
        )

        self._dataset: Optional[pd.DataFrame] = None
        self._df_t1: Optional[pd.DataFrame] = None
        self._df_btc: Optional[pd.DataFrame] = None

    def initialize(self) -> None:
        """Initialize and cache multi-asset data, T1 breakout events, and BTC volatility series."""
        if self._dataset is None:
            print("\n[LocalTradingEngine] Compiling multi-asset 15m dataset with Numba JIT...")
            t0 = time.perf_counter()
            self._dataset = compile_dataset_with_numba()
            print(f"[LocalTradingEngine] Loaded {len(self._dataset):,d} candidate bars in {time.perf_counter() - t0:.2f}s.")

        if self._df_t1 is None:
            print("[LocalTradingEngine] Generating 4h T1 Quiet-Flow Breakout signals...")
            t0 = time.perf_counter()
            self._df_t1 = self.strategy_engine.load_t1_breakout_trades(cache_dir=self.cache_dir)
            print(f"[LocalTradingEngine] Loaded {len(self._df_t1):,d} T1 signals in {time.perf_counter() - t0:.2f}s.")

        if self._df_btc is None:
            btc_path = self.cache_dir / "BTCUSDT_4h.parquet"
            if btc_path.exists():
                df_btc = pd.read_parquet(btc_path)
                df_btc['time'] = pd.to_datetime(df_btc['time'], utc=True)
                df_btc.sort_values('time', inplace=True)
                df_btc.reset_index(drop=True, inplace=True)
                df_btc['atr_pct'] = (df_btc['atr'] / df_btc['close']) * 100.0
                df_btc['trailing_30d_atr_pct'] = df_btc['atr_pct'].rolling(180).mean()
                self._df_btc = df_btc

    def _get_trailing_btc_vol(self, start_ts: pd.Timestamp) -> float:
        """Causally compute 30-day trailing Bitcoin ATR % prior to window start."""
        if self._df_btc is not None:
            sub = self._df_btc[self._df_btc['time'] < start_ts]
            if len(sub) > 0 and not np.isnan(sub['trailing_30d_atr_pct'].iloc[-1]):
                return float(sub['trailing_30d_atr_pct'].iloc[-1])
        return 1.75

    def execute_period(
        self,
        start_date: str,
        end_date: str,
        name: str = "Evaluation Period",
        min_roi: float = 10.0,
        max_dd_target: float = 5.0,
        min_wr: float = 40.0,
        min_trades: int = 15,
    ) -> ExecutionSummary:
        """Causally train and execute strategy over any specified time boundary."""
        self.initialize()
        assert self._dataset is not None
        assert self._df_t1 is not None

        start_ts = pd.Timestamp(start_date, tz="UTC")
        end_ts = pd.Timestamp(end_date + " 23:59:59" if len(end_date) == 10 else end_date, tz="UTC")
        start_ms = start_ts.value // 1_000_000
        end_ms = end_ts.value // 1_000_000
        purge_ms = self.config.purge_hours * 3600 * 1000

        # Causal partition: train data strictly precedes (start_ms - 72h)
        train_mask = self._dataset.open_time_ms < (start_ms - purge_ms)
        test_mask = (self._dataset.open_time_ms >= start_ms) & (self._dataset.open_time_ms <= end_ms)

        train_set = self._dataset[train_mask]
        test_set = self._dataset[test_mask]

        if len(train_set) < 500 or len(test_set) == 0:
            return ExecutionSummary(
                name=name, start_date=start_date, end_date=end_date, trades=0, s1_trades=0, t1_trades=0,
                wins=0, win_rate=0.0, net_pnl=0.0, net_roi=0.0, max_dd=0.0, profit_factor=0.0,
                avg_r=0.0, expectancy_usd=0.0, status="INSUFFICIENT_DATA"
            )

        # Causal model fitting & threshold scaling
        ridge, clf, mu, sd, calib_thresh = self.strategy_engine.train_models(train_set)
        selected = self.strategy_engine.score_test_candidates(
            test_set, ridge, clf, mu, sd, calib_thresh
        )

        # Extract S1 candidate events
        s1_events: List[Dict[str, Any]] = []
        for idx in range(len(selected)):
            prob = float(selected["prob"].iloc[idx])
            tide = float(selected["btc_macro_tide"].iloc[idx]) if "btc_macro_tide" in selected.columns else 0.0
            side = int(selected["signal_side"].iloc[idx]) if "signal_side" in selected.columns else 1
            c_thresh = float(selected["calib_thresh"].iloc[idx])

            if side == -1 and tide > 0.0:
                continue
            if side == 1 and tide < 0.0 and prob < (c_thresh + 0.020):
                continue
            funding = float(selected["funding_rate_pct"].iloc[idx]) if "funding_rate_pct" in selected.columns else 0.0
            slope = float(selected["slope200"].iloc[idx]) if "slope200" in selected.columns else 0.0
            if side == 1 and (funding >= 0.035) and (slope < 0.25):
                continue

            if prob >= c_thresh:
                s1_events.append({
                    "time": int(selected["open_time_ms"].iloc[idx]),
                    "prob": prob,
                    "r_gain": float(selected["realized_r"].iloc[idx]),
                    "hold_bars": int(selected["bars_held"].iloc[idx]),
                    "symbol": str(selected["symbol"].iloc[idx]),
                    "strategy": "S1"
                })

        # Extract T1 candidate events
        t1_mask = (self._df_t1["time"] >= start_ms) & (self._df_t1["time"] <= end_ms)
        t1_events = self._df_t1[t1_mask].to_dict("records")

        # Synchronize event streams chronologically
        combined = s1_events + t1_events
        combined.sort(key=lambda x: (x["time"], -x["prob"]))

        equity = self.config.capital
        peak_equity = self.config.capital
        cur_max_dd_pct = 0.0
        consec_losses_s1 = 0
        s1_positions: List[tuple[int, float]] = []
        t1_positions: List[tuple[int, float]] = []
        symbol_cooldown: Dict[str, int] = {}
        trade_records: List[TradeRecord] = []
        s1_count = 0
        t1_count = 0
        stage1_armed = False

        for ev in combined:
            if cur_max_dd_pct >= self.config.max_dd_limit:
                continue

            t_entry = ev["time"]
            strat = ev["strategy"]
            sym = ev["symbol"]
            r_gain = ev["r_gain"]
            prob = ev["prob"]
            hold_ms = int(ev["hold_bars"]) * 15 * 60 * 1000

            # Prune expired positions
            s1_positions = [p for p in s1_positions if p[0] > t_entry]
            t1_positions = [p for p in t1_positions if p[0] > t_entry]

            if sym in symbol_cooldown and t_entry < symbol_cooldown[sym]:
                continue

            current_profit = equity - self.config.capital

            # Two-Stage Profit Floor (Stage 1 Floor Lock)
            if self.config.stage1_arm_profit > 0.0 and current_profit >= self.config.stage1_arm_profit:
                stage1_armed = True

            if stage1_armed and self.config.stage1_floor_profit > 0.0 and current_profit <= self.config.stage1_floor_profit:
                continue

            cur_peak_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
            cur_cap_dd = ((self.config.capital - equity) / self.config.capital) * 100.0 if equity < self.config.capital else 0.0

            if current_profit >= 180.0:
                cur_max_s1 = 3
                cur_max_tot = 4
                cur_max_risk_budget = 130.0
            else:
                cur_max_s1 = self.config.max_s1_concurrent
                cur_max_tot = self.config.max_concurrent
                cur_max_risk_budget = 110.0

            if strat == "S1":
                if len(s1_positions) >= cur_max_s1 or len(s1_positions) + len(t1_positions) >= cur_max_tot:
                    continue

                if (peak_equity - self.config.capital) >= self.config.milestone_profit_usd:
                    cushion = max(0.0, equity - (self.config.capital + self.config.milestone_profit_usd))
                    risk_amt = min(self.config.milestone_risk, cushion * self.config.cushion_multiplier)
                elif current_profit >= self.config.trans_thresh:
                    risk_amt = self.config.trans_risk
                elif cur_cap_dd >= 2.0 or cur_peak_dd >= 4.0 or consec_losses_s1 >= 2:
                    risk_amt = self.config.defense_risk
                elif consec_losses_s1 == 1:
                    risk_amt = 30.0 if current_profit < 0.0 else (self.config.base_risk * (self.config.conf_mult if prob >= self.config.conf_prob_thresh else 1.0))
                else:
                    conf = self.config.conf_mult if prob >= self.config.conf_prob_thresh else 1.0
                    base_s = self.config.base_risk * conf
                    if current_profit >= self.config.house_compounding_start:
                        risk_amt = min(self.config.house_risk_max, base_s + current_profit * self.config.house_compounding_rate)
                    else:
                        risk_amt = base_s

                if risk_amt <= 0.0:
                    continue

                current_open_risk = sum(p[1] for p in s1_positions) + sum(p[1] for p in t1_positions)
                final_risk = min(risk_amt, max(14.0, cur_max_risk_budget - current_open_risk))
                s1_positions.append((t_entry + hold_ms, final_risk))
                trade_pnl = r_gain * final_risk
                equity += trade_pnl
                if equity > peak_equity:
                    peak_equity = equity
                dd_pct = ((peak_equity - equity) / peak_equity) * 100.0
                if dd_pct > cur_max_dd_pct:
                    cur_max_dd_pct = dd_pct

                if r_gain >= self.config.win_r_reset_thresh:
                    consec_losses_s1 = 0
                else:
                    consec_losses_s1 += 1
                    symbol_cooldown[sym] = t_entry + self.config.cooldown_bars * 15 * 60 * 1000

                entry_str = str(pd.to_datetime(t_entry, unit="ms", utc=True))[:19]
                exit_str = str(pd.to_datetime(t_entry + hold_ms, unit="ms", utc=True))[:19]
                trade_records.append(TradeRecord(
                    trade_id=len(trade_records) + 1,
                    entry_time=entry_str,
                    exit_time=exit_str,
                    symbol=sym,
                    strategy="S1",
                    realized_r=round(r_gain, 4),
                    risk_usd=round(final_risk, 2),
                    pnl_usd=round(trade_pnl, 2),
                    running_equity=round(equity, 2),
                    running_dd_pct=round(dd_pct, 2),
                    win=1 if r_gain > 0 else 0,
                    hold_bars=int(ev["hold_bars"])
                ))
                s1_count += 1

            else:  # T1 Breakout
                if len(t1_positions) >= self.config.max_t1_concurrent or len(s1_positions) + len(t1_positions) >= cur_max_tot:
                    continue

                if (peak_equity - self.config.capital) >= self.config.milestone_profit_usd:
                    cushion = max(0.0, equity - (self.config.capital + self.config.milestone_profit_usd))
                    risk_amt = min(8.0, cushion * self.config.cushion_multiplier)
                elif current_profit >= self.config.trans_thresh:
                    risk_amt = self.config.t1_trans_risk
                elif cur_cap_dd >= 2.0 or cur_peak_dd >= 4.0:
                    risk_amt = self.config.defense_risk
                else:
                    risk_amt = self.config.t1_base_risk

                if risk_amt <= 0.0:
                    continue

                current_open_risk = sum(p[1] for p in s1_positions) + sum(p[1] for p in t1_positions)
                final_risk = min(risk_amt, max(14.0, cur_max_risk_budget - current_open_risk))
                t1_positions.append((t_entry + hold_ms, final_risk))
                trade_pnl = r_gain * final_risk
                equity += trade_pnl
                if equity > peak_equity:
                    peak_equity = equity
                dd_pct = ((peak_equity - equity) / peak_equity) * 100.0
                if dd_pct > cur_max_dd_pct:
                    cur_max_dd_pct = dd_pct

                entry_str = str(pd.to_datetime(t_entry, unit="ms", utc=True))[:19]
                exit_str = str(pd.to_datetime(t_entry + hold_ms, unit="ms", utc=True))[:19]
                trade_records.append(TradeRecord(
                    trade_id=len(trade_records) + 1,
                    entry_time=entry_str,
                    exit_time=exit_str,
                    symbol=sym,
                    strategy="T1",
                    realized_r=round(r_gain, 4),
                    risk_usd=round(final_risk, 2),
                    pnl_usd=round(trade_pnl, 2),
                    running_equity=round(equity, 2),
                    running_dd_pct=round(dd_pct, 2),
                    win=1 if r_gain > 0 else 0,
                    hold_bars=int(ev["hold_bars"])
                ))
                t1_count += 1

        n_trades = len(trade_records)
        wins = sum(tr.win for tr in trade_records)
        wr = (wins / n_trades * 100.0) if n_trades > 0 else 0.0
        net_pnl = equity - self.config.capital
        net_roi = (net_pnl / self.config.capital) * 100.0

        gross_profit = sum(tr.pnl_usd for tr in trade_records if tr.pnl_usd > 0)
        gross_loss = abs(sum(tr.pnl_usd for tr in trade_records if tr.pnl_usd < 0))
        pf = (gross_profit / gross_loss) if gross_loss > 0 else (99.0 if gross_profit > 0 else 0.0)
        avg_r = float(np.mean([tr.realized_r for tr in trade_records])) if n_trades > 0 else 0.0
        exp_usd = net_pnl / n_trades if n_trades > 0 else 0.0

        is_pass = (net_roi >= min_roi) and (cur_max_dd_pct <= max_dd_target) and (wr >= min_wr) and (n_trades >= min_trades)
        status = "PASS" if is_pass else ("PROFIT" if net_pnl > 0 and cur_max_dd_pct <= max_dd_target else ("CASH" if n_trades == 0 else "FAIL"))

        return ExecutionSummary(
            name=name,
            start_date=start_date,
            end_date=end_date,
            trades=n_trades,
            s1_trades=s1_count,
            t1_trades=t1_count,
            wins=wins,
            win_rate=round(wr, 1),
            net_pnl=round(net_pnl, 2),
            net_roi=round(net_roi, 2),
            max_dd=round(cur_max_dd_pct, 2),
            profit_factor=round(pf, 2),
            avg_r=round(avg_r, 3),
            expectancy_usd=round(exp_usd, 2),
            status=status,
            trades_detail=trade_records
        )

    def run_window(self, window_id: int, export_trades: bool = True) -> ExecutionSummary:
        """Run a single canonical benchmark OOS window and optionally export trades."""
        with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
            windows = json.load(f)
        matched = [w for w in windows if w["window_id"] == window_id]
        if not matched:
            raise ValueError(f"Window ID {window_id} not found in {WINDOWS_PATH}")
        w = matched[0]

        summary = self.execute_period(
            start_date=w["start_date"],
            end_date=w["end_date"],
            name=f"W{window_id:02d}: {w['name']}"
        )

        if export_trades and summary.trades_detail:
            out_csv = self.reports_dir / f"trades_w{window_id:02d}.csv"
            out_parquet = self.reports_dir / f"trades_w{window_id:02d}.parquet"
            df_trades = pd.DataFrame([asdict(t) for t in summary.trades_detail])
            df_trades.to_csv(out_csv, index=False)
            df_trades.to_parquet(out_parquet, index=False)
            print(f"[LocalTradingEngine] Exported {len(df_trades)} trades to {out_csv.name} and {out_parquet.name}")

        return summary

    def run_walkforward(self, export_reports: bool = True) -> List[ExecutionSummary]:
        """Run all 20 canonical OOS windows and print the master multiverse scorecard."""
        with open(WINDOWS_PATH, "r", encoding="utf-8") as f:
            windows = json.load(f)

        print("\n" + "=" * 135)
        print("INSTITUTIONAL QUANTITATIVE MASTER ENGINE: 20 OUT-OF-SAMPLE (OOS) WALK-FORWARD AUDIT")
        print("=" * 135)
        print(f"{'W#':<3} | {'Window Name':<38} | {'Trades':<6} | {'S1 Tr':<6} | {'T1 Tr':<6} | {'Win Rate':<8} | {'Net PnL':<12} | {'Net ROI':<9} | {'Max DD':<7} | {'Status':<6}")
        print("-" * 135)

        summaries: List[ExecutionSummary] = []
        all_trades: List[TradeRecord] = []
        passed_count = 0
        total_trades = 0
        total_pnl = 0.0

        for w in windows:
            w_id = w["window_id"]
            w_name = w["name"]
            summary = self.execute_period(
                start_date=w["start_date"],
                end_date=w["end_date"],
                name=f"W{w_id:02d}: {w_name}"
            )
            summaries.append(summary)
            all_trades.extend(summary.trades_detail)

            if summary.status == "PASS":
                passed_count += 1
            total_trades += summary.trades
            total_pnl += summary.net_pnl

            print(f"W{w_id:02d} | {w_name[:38]:<38} | {summary.trades:<6d} | {summary.s1_trades:<6d} | {summary.t1_trades:<6d} | {summary.win_rate:>5.1f}%  | {summary.net_pnl:>+10.2f} USD | {summary.net_roi:>+7.2f}% | {summary.max_dd:>5.2f}% | {summary.status:<6}")

        print("=" * 135)
        tot_roi = (total_pnl / self.config.capital) * 100.0
        print(f"MASTER MULTIVERSE SCORECARD: Passed: {passed_count}/20 | Total Trades: {total_trades:,d} | Total PnL: {total_pnl:+,.2f} USD (ROI: {tot_roi:+.2f}%)")
        print("=" * 135)

        if export_reports:
            timestamp = int(time.time())
            scorecard_json = self.reports_dir / f"scorecard_20_oos_{timestamp}.json"
            trades_csv = self.reports_dir / f"trades_all_20_oos_{timestamp}.csv"
            trades_parquet = self.reports_dir / f"trades_all_20_oos_{timestamp}.parquet"

            payload = {
                "timestamp": timestamp,
                "passed_count": passed_count,
                "total_windows": len(windows),
                "total_trades": total_trades,
                "total_pnl_usd": round(total_pnl, 2),
                "total_roi_pct": round(tot_roi, 2),
                "windows": [s.to_dict() for s in summaries]
            }
            with open(scorecard_json, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

            if all_trades:
                df_all = pd.DataFrame([asdict(t) for t in all_trades])
                df_all.to_csv(trades_csv, index=False)
                df_all.to_parquet(trades_parquet, index=False)

            print(f"[LocalTradingEngine] Reports saved to {scorecard_json.name} and {trades_parquet.name}")

        return summaries


def main():
    parser = argparse.ArgumentParser(
        description="Institutional Local Trading Engine CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--mode",
        choices=["oos", "window", "custom"],
        default="oos",
        help="Execution mode: 'oos' for all 20 windows, 'window' for a single window, 'custom' for date range."
    )
    parser.add_argument(
        "--window",
        type=int,
        default=12,
        help="Target window ID when using --mode window (e.g. 12, 14)."
    )
    parser.add_argument(
        "--start",
        type=str,
        default="2023-08-01",
        help="Start date (YYYY-MM-DD) for custom mode."
    )
    parser.add_argument(
        "--end",
        type=str,
        default="2023-08-31",
        help="End date (YYYY-MM-DD) for custom mode."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Custom Period",
        help="Descriptive label for custom mode."
    )
    parser.add_argument(
        "--no-export",
        action="store_true",
        help="Disable automatic trade logging to CSV/Parquet."
    )

    args = parser.parse_args()

    engine = LocalTradingEngine()

    if args.mode == "oos":
        engine.run_walkforward(export_reports=not args.no_export)
    elif args.mode == "window":
        print(f"\n--- Running Single Window W{args.window:02d} ---")
        summary = engine.run_window(window_id=args.window, export_trades=not args.no_export)
        print(f"\nResult: {summary.name}")
        print(f"Trades: {summary.trades} (S1: {summary.s1_trades}, T1: {summary.t1_trades}) | Win Rate: {summary.win_rate:.1f}%")
        print(f"Net PnL: {summary.net_pnl:+,.2f} USD | Net ROI: {summary.net_roi:+.2f}% | Max DD: {summary.max_dd:.2f}% | Status: {summary.status}")
        if summary.trades_detail:
            print("\nExecuted Trades Sample:")
            print(f"{'Time':<20} | {'Sym':<8} | {'Strat':<5} | {'R-Gain':<8} | {'Risk':<6} | {'PnL':<10} | {'Equity':<10}")
            print("-" * 75)
            for t in summary.trades_detail[:15]:
                print(f"{t.entry_time:<20} | {t.symbol:<8} | {t.strategy:<5} | {t.realized_r:+7.2f}R | {t.risk_usd:5.1f} | {t.pnl_usd:+8.2f} USD | {t.running_equity:8.2f} USD")
            if len(summary.trades_detail) > 15:
                print(f"... and {len(summary.trades_detail) - 15} more trades.")
    elif args.mode == "custom":
        print(f"\n--- Running Custom Date Range ({args.start} to {args.end}) ---")
        summary = engine.execute_period(
            start_date=args.start,
            end_date=args.end,
            name=args.name
        )
        print(f"\nResult: {summary.name}")
        print(f"Trades: {summary.trades} (S1: {summary.s1_trades}, T1: {summary.t1_trades}) | Win Rate: {summary.win_rate:.1f}%")
        print(f"Net PnL: {summary.net_pnl:+,.2f} USD | Net ROI: {summary.net_roi:+.2f}% | Max DD: {summary.max_dd:.2f}% | Status: {summary.status}")


if __name__ == "__main__":
    main()
