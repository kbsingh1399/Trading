r"""
================================================================================
T1 QUIET-FLOW DONCHIAN BREAKOUT SLEEVE  --  the surviving engine
================================================================================
Home of the 4h breakout sleeve after the S1 15m ML sleeve was retired on
2026-09-16 (see S1_TEARDOWN.md). Extracted verbatim from
Engine/strategy/s1_dual_model_orderflow.py so that the T1 signal generation and
execution path are bit-identical to what the dual-model runner used -- with one
deliberate exception, the friction-stress bugfix noted at the join below.

Why T1 survives and S1 did not (scratch/diag_t1_autopsy.py, 2,972 trades):

                        S1 (15m ML)      T1 (4h breakout)
    median 1R           0.527% of px     2.884% of px      (5.47x larger)
    friction            0.779 R          0.199 R           (19.9% of stop)
    GROSS expectancy    +0.0058 R        +0.1164 R
    gross t-stat        +0.85 (p=0.40)   +5.47 (p<1e-7)
    NET expectancy      -1.1385 R        -0.0826 R

S1 had no gross edge to select and a risk unit smaller than its own round trip.
T1 has a statistically robust gross edge and a survivable cost ratio; it is
currently ~41% of a cost reduction away from break-even. That is a solvable
problem. S1's was not.

CAUSALITY: donchian_high/low are `.shift(1)` so the channel excludes the current
bar; entry fills on the NEXT bar's open; the exit scan starts at i+2; and the
stress multiplier is joined on a grid keyed by 4h bar CLOSE. Nothing here can
see the future.
================================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

import sys as _sys

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))

from Engine.execution_costs import ROUND_TRIP_FRAC, build_stress_series

# Entry slippage applied to the next bar's open, in fraction of price. Note this
# is IN ADDITION to ROUND_TRIP_BPS, which itself already contains ~25 bps of
# slippage, so T1 models ~51 bps per round trip. That is deliberately
# conservative -- it overstates cost and therefore cannot inflate T1's result.
T1_ENTRY_SLIPPAGE_FRAC = 0.0010

# Exit geometry, in R units. 1R = 1.15 * max(4h ATR, 0.5% of price).
T1_HORIZON_BARS = 16          # 16 x 4h = 64 hours
T1_TARGET_R = 2.20
T1_STOP_R = 1.00
T1_RATCHET = ((1.40, 0.85), (0.75, 0.35))   # max favourable excursion -> locked stop
T1_MIN_BARS_BETWEEN_ENTRIES = 4


def load_t1_breakout_trades(cache_dir: Path | str | None = None) -> pd.DataFrame:
    """Generate pure 4h Donchian breakout (T1) trade events across the certified assets.

    Trigger: 4h close breaks the prior-20-bar Donchian channel with EMA stack
    alignment (ema20 > ema50 > ema200 longs / inverse shorts), a same-signed
    200-EMA slope, spot CVD slope agreement, taker-flow confirmation, and an
    aligned Bitcoin macro tide. Entries fill on the following bar's open.
    """
    if cache_dir is None:
        cache_dir = _ROOT / "scratch" / "cache_multi_tf"
    else:
        cache_dir = Path(cache_dir)

    df_btc = pd.read_parquet(cache_dir / "BTCUSDT_4h.parquet")
    df_btc["time"] = pd.to_datetime(df_btc["time"], utc=True)
    btc_bull = (df_btc["close"] > df_btc["ema_50"]) & (df_btc["ema_50"] > df_btc["ema_200"])
    btc_bear = (df_btc["close"] < df_btc["ema_50"]) & (df_btc["ema_50"] < df_btc["ema_200"])
    btc_tide_series = pd.Series(np.where(btc_bull, 1, np.where(btc_bear, -1, 0)),
                                index=df_btc["time"].astype("int64"))

    # Causal volatility-regime friction stress, indexed by 4h bar CLOSE
    # (avail_time), so an as-of join can only see completed bars.
    _stress = build_stress_series(cache_dir).sort_values("avail_time").reset_index(drop=True)

    all_t1_trades = []
    for p in sorted(cache_dir.glob("*_4h.parquet")):
        sym = p.stem.replace("_4h", "")
        df = pd.read_parquet(p)
        df["time"] = pd.to_datetime(df["time"], utc=True)
        df = df.sort_values("time").reset_index(drop=True)
        n = len(df)
        ts_ms = df["time"].astype("int64")

        # BUGFIX 2026-09 (was silently costing T1 its entire stress schedule).
        # The 4h cache stores `time` as datetime64[ms, UTC], so .astype("int64")
        # yields MILLISECONDS. pd.to_datetime(int64) without unit= assumes
        # NANOSECONDS, which mapped every bar to 1970-01-01 00:26; the merge_asof
        # then matched 0.00% of 13,200 bars, returned NaN, and the
        # np.where(isfinite(...)) fallback below converted all of it to 1.0x.
        # Net effect: T1 never received the Phase 4A regime stress while S1 did,
        # understating T1 friction by 0.0316 R/trade. The guard makes a
        # recurrence raise instead of silently degrading to 1.0x.
        _bt = pd.DataFrame({"bt": pd.to_datetime(ts_ms.values, unit="ms", utc=True)
                            .astype("datetime64[ns, UTC]")})
        _sm = pd.merge_asof(_bt, _stress, left_on="bt", right_on="avail_time",
                            direction="backward")["mult"].to_numpy(float)
        _match_rate = float(np.isfinite(_sm).mean())
        if _match_rate < 0.99:
            raise RuntimeError(
                f"T1 friction-stress join matched only {_match_rate*100:.2f}% of {sym} 4h bars "
                f"to build_stress_series(); the multiplier would silently degrade to 1.0x. "
                f"left dtype={_bt['bt'].dtype} range=[{_bt['bt'].min()} .. {_bt['bt'].max()}], "
                f"right dtype={_stress['avail_time'].dtype}. This is the 1970-epoch unit bug "
                f"returning -- fix the join, do not paper over it."
            )
        stress_vals = np.where(np.isfinite(_sm), _sm, 1.0)

        btc_tide_val = ts_ms.map(btc_tide_series).fillna(0).values
        closes = df["close"].values
        highs = df["high"].values
        lows = df["low"].values
        opens = (df["next_open"].values if "next_open" in df.columns
                 else df["open"].shift(-1).fillna(df["close"]).values)
        atrs = df["atr"].values
        d_high = df["donchian_high"].values
        d_low = df["donchian_low"].values
        e20 = df["ema_20"].values
        e50 = df["ema_50"].values
        e200 = df["ema_200"].values
        e200_slope = df["ema_200_slope"].values
        buy_vol = df["buy_vol_ratio"].values
        cvd_slope = df["spot_cvd_slope"].values

        last_entry = -999
        for i in range(200, n - (T1_HORIZON_BARS + 1)):
            side = 0
            if (e20[i] > e50[i] > e200[i] and e200_slope[i] > 0 and closes[i] > d_high[i]
                    and buy_vol[i] > 0.51 and cvd_slope[i] > 0 and btc_tide_val[i] > 0):
                side = 1
            elif (e20[i] < e50[i] < e200[i] and e200_slope[i] < 0 and closes[i] < d_low[i]
                    and buy_vol[i] < 0.49 and cvd_slope[i] < 0 and btc_tide_val[i] < 0):
                side = -1

            if side != 0 and (i - last_entry >= T1_MIN_BARS_BETWEEN_ENTRIES):
                last_entry = i
                fill_px = opens[i] * (1.0 + side * T1_ENTRY_SLIPPAGE_FRAC)
                r_dist = 1.15 * max(atrs[i], fill_px * 0.005)
                stop_px = fill_px - side * r_dist
                t_entry = int(ts_ms.iloc[i + 1])

                t_exit = -1
                r_gain = -1.0
                bars_held = T1_HORIZON_BARS
                max_fav = 0.0

                for j in range(1, T1_HORIZON_BARS + 1):
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
                        if hi_j >= fill_px + T1_TARGET_R * r_dist:
                            t_exit = int(ts_ms.iloc[idx])
                            r_gain = T1_TARGET_R
                            bars_held = j
                            break
                        elif max_fav >= T1_RATCHET[0][0]:
                            stop_px = max(stop_px, fill_px + T1_RATCHET[0][1] * r_dist)
                        elif max_fav >= T1_RATCHET[1][0]:
                            stop_px = max(stop_px, fill_px + T1_RATCHET[1][1] * r_dist)
                    else:
                        if hi_j >= stop_px:
                            t_exit = int(ts_ms.iloc[idx])
                            r_gain = (fill_px - stop_px) / r_dist
                            bars_held = j
                            break
                        cur_fav = (fill_px - lo_j) / r_dist
                        if cur_fav > max_fav:
                            max_fav = cur_fav
                        if lo_j <= fill_px - T1_TARGET_R * r_dist:
                            t_exit = int(ts_ms.iloc[idx])
                            r_gain = T1_TARGET_R
                            bars_held = j
                            break
                        elif max_fav >= T1_RATCHET[0][0]:
                            stop_px = min(stop_px, fill_px - T1_RATCHET[0][1] * r_dist)
                        elif max_fav >= T1_RATCHET[1][0]:
                            stop_px = min(stop_px, fill_px - T1_RATCHET[1][1] * r_dist)

                if t_exit == -1:
                    idx = min(i + T1_HORIZON_BARS, n - 1)
                    t_exit = int(ts_ms.iloc[idx])
                    cl_exit = closes[idx]
                    r_gain = ((cl_exit - fill_px) / r_dist) if side == 1 else ((fill_px - cl_exit) / r_dist)
                    bars_held = T1_HORIZON_BARS

                # Same round-trip constant as the retired S1 labeler, stressed by
                # the same causal volatility-regime multiplier (Phase 4A).
                fric_r = (fill_px * ROUND_TRIP_FRAC * stress_vals[i]) / r_dist
                net_r = r_gain - fric_r

                all_t1_trades.append({
                    "time": t_entry,
                    "t_exit": t_exit,
                    "r_gain": net_r,
                    "gross_r": r_gain,
                    "fric_r": fric_r,
                    "stress": float(stress_vals[i]),
                    "r_dist": r_dist,
                    "fill_px": fill_px,
                    "side": int(side),
                    # hold_bars is expressed in 15m bars (4h bars x 16) because the
                    # executor's position-release clock is denominated in 15m.
                    "hold_bars": bars_held * 16,
                    "symbol": sym,
                    "prob": 0.52,
                    "strategy": "T1",
                })

    df_t1 = pd.DataFrame(all_t1_trades).sort_values("time").reset_index(drop=True)
    return df_t1


class T1ExecutionEngine:
    """Position sizing, concurrency and drawdown control for the T1 sleeve alone.

    Behaviourally identical to the T1 branch of the retired dual-model
    simulate_execution() with the S1 event list empty, so scorecards remain
    comparable to the historical dual-sleeve runs.
    """

    def __init__(
        self,
        capital: float = 5000.0,
        defense_risk: float = 14.0,
        milestone_risk: float = 10.0,
        trans_risk: float = 35.0,
        trans_thresh: float = 480.0,
        t1_base_risk: float = 42.0,
        t1_trans_risk: float = 22.0,
        cushion_multiplier: float = 0.25,
        milestone_profit_usd: float = 500.0,
        max_concurrent: int = 3,
        max_t1_concurrent: int = 2,
        max_dd_limit: float = 4.40,
        stage1_arm_profit: float = 180.0,
        stage1_floor_profit: float = 75.0,
    ):
        self.capital = capital
        self.defense_risk = defense_risk
        self.milestone_risk = milestone_risk
        self.trans_risk = trans_risk
        self.trans_thresh = trans_thresh
        self.t1_base_risk = t1_base_risk
        self.t1_trans_risk = t1_trans_risk
        self.cushion_multiplier = cushion_multiplier
        self.milestone_profit_usd = milestone_profit_usd
        self.max_concurrent = max_concurrent
        self.max_t1_concurrent = max_t1_concurrent
        self.max_dd_limit = max_dd_limit
        self.stage1_arm_profit = stage1_arm_profit
        self.stage1_floor_profit = stage1_floor_profit

    def simulate_execution(self, t1_df: pd.DataFrame, start_ms: int, end_ms: int) -> Dict[str, Any]:
        equity = self.capital
        peak_equity = self.capital
        cur_max_dd_pct = 0.0
        t1_positions: List[Tuple[int, float]] = []
        executed_trades: List[Dict[str, Any]] = []
        stage1_armed = False

        if t1_df is None or len(t1_df) == 0:
            return {"net_pnl": 0.0, "net_roi": 0.0, "max_dd": 0.0, "win_rate": 0.0,
                    "trades": 0, "s1_trades": 0, "t1_trades": 0, "equity": equity,
                    "trade_ledger": []}

        t1_mask = (t1_df["time"] >= start_ms) & (t1_df["time"] <= end_ms)
        events = t1_df[t1_mask].to_dict("records")
        events.sort(key=lambda x: (x["time"], -x["prob"]))

        for ev in events:
            if cur_max_dd_pct >= self.max_dd_limit:
                continue

            t_entry = ev["time"]
            sym = ev["symbol"]
            r_gain = ev["r_gain"]
            hold_ms = int(ev["hold_bars"]) * 15 * 60 * 1000

            t1_positions = [p for p in t1_positions if p[0] > t_entry]

            current_profit = equity - self.capital

            if self.stage1_arm_profit > 0.0 and current_profit >= self.stage1_arm_profit:
                stage1_armed = True
            if stage1_armed and self.stage1_floor_profit > 0.0 and current_profit <= self.stage1_floor_profit:
                continue

            cur_peak_dd = ((peak_equity - equity) / peak_equity) * 100.0 if peak_equity > 0 else 0.0
            cur_cap_dd = ((self.capital - equity) / self.capital) * 100.0 if equity < self.capital else 0.0

            # House Money Capacity Surge: expand slots once verified profit >= 180 USD.
            if current_profit >= 180.0:
                cur_max_tot = 4
                cur_max_risk_budget = 130.0
            else:
                cur_max_tot = self.max_concurrent
                cur_max_risk_budget = 110.0

            if len(t1_positions) >= self.max_t1_concurrent:
                continue
            if len(t1_positions) >= cur_max_tot:
                continue

            if (peak_equity - self.capital) >= self.milestone_profit_usd:
                # Continuous CPPI cushion risk compression above milestone (Black-Perold 1992)
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

            current_open_risk = sum(p[1] for p in t1_positions)
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
                                    "risk_usd": final_risk,
                                    "gross_r": ev.get("gross_r"), "stress": ev.get("stress")})

        n_trades = len(executed_trades)
        wr = (sum(tr["win"] for tr in executed_trades) / n_trades * 100.0) if n_trades > 0 else 0.0
        net_pnl = equity - self.capital

        return {
            "net_pnl": net_pnl,
            "net_roi": (net_pnl / self.capital) * 100.0,
            "max_dd": cur_max_dd_pct,
            "win_rate": wr,
            "trades": n_trades,
            "s1_trades": 0,
            "t1_trades": n_trades,
            "equity": equity,
            "trade_ledger": executed_trades,
        }
