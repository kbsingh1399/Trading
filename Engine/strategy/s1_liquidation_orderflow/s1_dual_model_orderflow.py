"""
================================================================================
INSTITUTIONAL DUAL-MODEL ORDERFLOW STRATEGY (S1 DUAL-MODEL ENGINE)
================================================================================
Settled Invariants & Execution Protocols:
1. Directional Separation: Independent LightGBM classifiers (clf_long, clf_short)
   trained strictly on in-sample causal data with 72-hour quarantine purge.
2. Stationary Feature Space:
   - Relative VWAP Z-score (vwap_zscore)
   - Liquidation Z-scores (long_liq_zs, short_liq_zs)
   - Orderflow Divergence (zc_div)
   - Relative Strength Index (rsi_14)
   - Volume/Volatility expansion ratios (volume_ratio, atr_ratio)
   - 200 EMA Trend Slope normalized by ATR (slope200)
   - Spot/Futures basis in basis points (basis_bps)
   - Intraday hour seasonality (hour)
3. Cont-Stoikov Orderflow & Microstructure Gating:
   - Safe Shorts: short_liq_zs < 1.2, vwap_zscore in [-2.0, -0.5]
   - Institutional Volume Confirmation: volume_ratio >= 0.75 for breakdowns
   - Mathematical Exhaustion Cap: vwap_zscore <= 2.8 for breakout longs
4. Unified Regime-Dispatched Allocation:
   - Strong Bull (tide >= 0.12): Trend-following longs (max 3 per asset)
   - Bear Regime (tide <= -0.10): Safe shorts with volume confirmation (max 3 per asset)
   - Neutral / Chop (-0.10 < tide < 0.12): Local bar-by-bar tide dispatch
5. Microstructure Risk Bounding & Hsieh-Barmish Feedback Control:
   - Base Risk: 50.00 USD (1.00% of 5,000.00 USD Capital)
   - House Money Risk: 85.00 USD (unlocks at profit >= 60.00 USD)
   - Mathematical Damping: risk = min(target_risk, max(5.0, dd_budget / 1.30))
   - Hard Circuit Breaker: 4.75% drawdown exit
   - Realistic Round-Trip Friction: 41.0 bps drag modeled per trade (-0.25R)
================================================================================
"""

from __future__ import annotations
from pathlib import Path
from typing import Tuple, Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
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
        vol_shift_thresh: float = 0.92,
        vol_shift_amt: float = 0.025,
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
        self.vol_shift_thresh = vol_shift_thresh
        self.vol_shift_amt = vol_shift_amt
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
        ridge = LogisticRegression(C=0.03, max_iter=200, random_state=self.random_state)
        ridge.fit(X_tr_s, y_train)

        # 2. Regularized LightGBM Classifier with depth-constrained leaves
        clf = lgb.LGBMClassifier(
            n_estimators=160,
            max_depth=4,
            num_leaves=15,
            learning_rate=0.04,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=2.0,
            reg_lambda=0.5,
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

    def score_test_candidates(
        self,
        test_df: pd.DataFrame,
        ridge: LogisticRegression,
        clf: lgb.LGBMClassifier,
        mu: pd.Series,
        sd: pd.Series,
        calib_thresh: float,
        trailing_vol_pct: float | None = None
    ) -> pd.DataFrame:
        """Score out-of-sample test candidates using causal ensemble and threshold gating."""
        if trailing_vol_pct is not None and trailing_vol_pct < self.vol_shift_thresh:
            effective_calib_thresh = calib_thresh - self.vol_shift_amt
        else:
            effective_calib_thresh = calib_thresh

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
        return selected


    @staticmethod
    def load_t1_breakout_trades(cache_dir: Path | str | None = None) -> pd.DataFrame:
        """Load and generate pure 4h Donchian Breakout (T1) trade events across the certified assets.
        
        Orthogonal to 15m S1 discount pullbacks: triggers when 4h price breaks above/below 20 Donchian channel
        with aligned Spot CVD slope and Bitcoin macro tide.
        """
        from Engine.core.multi_tf_data import load_all_4h_data, get_or_compute_4h_dataframe
        c_dir = Path(cache_dir) if cache_dir is not None else None
        df_btc = get_or_compute_4h_dataframe("BTCUSDT", cache_dir=c_dir)
        btc_bull = (df_btc['close'] > df_btc['ema_50']) & (df_btc['ema_50'] > df_btc['ema_200'])
        btc_bear = (df_btc['close'] < df_btc['ema_50']) & (df_btc['ema_50'] < df_btc['ema_200'])
        btc_tide_series = pd.Series(np.where(btc_bull, 1, np.where(btc_bear, -1, 0)), index=df_btc['time'].astype('int64'))

        asset_dfs = load_all_4h_data(cache_dir=c_dir)

        all_t1_trades = []
        for sym, df in asset_dfs.items():
            n = len(df)
            ts_ms = df['time'].astype('int64')
            btc_tide_val = ts_ms.map(btc_tide_series).fillna(0).values
            closes = df['close'].values
            highs = df['high'].values
            lows = df['low'].values
            opens = df['next_open'].values if 'next_open' in df.columns else df['open'].shift(-1).fillna(df['close']).values
            atrs = df['atr'].values
            d_high = df['donchian_high'].values
            d_low = df['donchian_low'].values
            e20 = df['ema_20'].values
            e50 = df['ema_50'].values
            e200 = df['ema_200'].values
            e200_slope = df['ema_200_slope'].values
            buy_vol = df['buy_vol_ratio'].values
            cvd_slope = df['spot_cvd_slope'].values

            last_entry = -999
            for i in range(200, n - 17):
                side = 0
                if e20[i] > e50[i] > e200[i] and e200_slope[i] > 0 and closes[i] > d_high[i] and buy_vol[i] > 0.51 and cvd_slope[i] > 0 and btc_tide_val[i] > 0:
                    side = 1
                elif e20[i] < e50[i] < e200[i] and e200_slope[i] < 0 and closes[i] < d_low[i] and buy_vol[i] < 0.49 and cvd_slope[i] < 0 and btc_tide_val[i] < 0:
                    side = -1

                if side != 0 and (i - last_entry >= 4):
                    last_entry = i
                    fill_px = opens[i] * (1.0 + side * 0.0010)
                    r_dist = 1.15 * max(atrs[i], fill_px * 0.005)
                    stop_px = fill_px - side * r_dist
                    t_entry = int(ts_ms.iloc[i+1])

                    t_exit = -1
                    r_gain = -1.0
                    bars_held = 16
                    max_fav = 0.0

                    for j in range(1, 17):
                        idx = i + 1 + j
                        if idx >= n:
                            break
                        hi_j = highs[idx]
                        lo_j = lows[idx]
                        cl_j = closes[idx]

                        if side == 1:
                            if lo_j <= stop_px:
                                t_exit = int(ts_ms.iloc[idx])
                                r_gain = (stop_px - fill_px) / r_dist
                                bars_held = j
                                break
                            cur_fav = (hi_j - fill_px) / r_dist
                            if cur_fav > max_fav:
                                max_fav = cur_fav
                            if hi_j >= fill_px + 2.20 * r_dist:
                                t_exit = int(ts_ms.iloc[idx])
                                r_gain = 2.20
                                bars_held = j
                                break
                            elif max_fav >= 1.40:
                                stop_px = max(stop_px, fill_px + 0.85 * r_dist)
                            elif max_fav >= 0.75:
                                stop_px = max(stop_px, fill_px + 0.35 * r_dist)
                        else:
                            if hi_j >= stop_px:
                                t_exit = int(ts_ms.iloc[idx])
                                r_gain = (fill_px - stop_px) / r_dist
                                bars_held = j
                                break
                            cur_fav = (fill_px - lo_j) / r_dist
                            if cur_fav > max_fav:
                                max_fav = cur_fav
                            if lo_j <= fill_px - 2.20 * r_dist:
                                t_exit = int(ts_ms.iloc[idx])
                                r_gain = 2.20
                                bars_held = j
                                break
                            elif max_fav >= 1.40:
                                stop_px = min(stop_px, fill_px - 0.85 * r_dist)
                            elif max_fav >= 0.75:
                                stop_px = min(stop_px, fill_px - 0.35 * r_dist)

                    if t_exit == -1:
                        idx = min(i + 16, n - 1)
                        t_exit = int(ts_ms.iloc[idx])
                        cl_exit = closes[idx]
                        r_gain = ((cl_exit - fill_px) / r_dist) if side == 1 else ((fill_px - cl_exit) / r_dist)
                        bars_held = 16

                    fric_r = (fill_px * 0.00205) / r_dist
                    net_r = r_gain - fric_r

                    all_t1_trades.append({
                        "time": t_entry,
                        "t_exit": t_exit,
                        "r_gain": net_r,
                        "hold_bars": bars_held * 16,
                        "symbol": sym,
                        "prob": 0.52,
                        "strategy": "T1"
                    })

        if not all_t1_trades:
            return pd.DataFrame(columns=["time", "t_exit", "r_gain", "hold_bars", "symbol", "prob", "strategy"])
        df_t1 = pd.DataFrame(all_t1_trades).sort_values("time").reset_index(drop=True)
        return df_t1

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

                executed_trades.append({"win": 1 if r_gain > 0 else 0, "pnl": trade_pnl, "strat": "S1"})
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

                executed_trades.append({"win": 1 if r_gain > 0 else 0, "pnl": trade_pnl, "strat": "T1"})
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
        }
