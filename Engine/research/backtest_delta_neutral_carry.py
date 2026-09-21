"""OX66 Mandate 1: cost-aware, hysteresis-gated delta-neutral backtest.

Strategy: hold up to K=3 spot-long/perp-short pairs (1x/1x) on the highest
settled funding rates, rotating ONLY via the shared carry policy
(Engine/live/carry_policy.py): 72h cooldown, 0.005%/8h hurdle, expected
accrual > 2x rotation friction, single-leg swaps, inversion liquidation.

Data: tracked `binance_backtesting_data/*_15m_master_2020_2026.parquet`
(`funding_rate_pct` in %/8h, `basis_index_bps`, `open_time_ms`).

Causality: decisions at settlement T_k use values sampled at T_k (funding
column changes ONLY on 00/08/16:00 UTC boundaries — verified 100% on BTC,
so no intra-interval foresight). Accrual for interval [T_k, T_k+1) is the
rate settled at T_k+1. Basis P&L is signed realized (entry-exit) plus MTM.

Economics: equity E; deployed (1-buffer); per-pair notional from CURRENT
equity at entry; existing pairs not resized (no churn from compounding).
Fees/spread per OX66 mandate (8/5bps + 2/1bps RT spread); 10bps spot leg
reported as pre-committed sensitivity.

Usage: /home/user/ox61venv/bin/python Engine/research/backtest_delta_neutral_carry.py
Writes: Engine/research/carry_backtest_results.json + carry_backtest_regimes.csv
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from Engine.live.carry_policy import (CarryPolicyConfig, pair_notional_usd,  # noqa: E402
                                      open_leg_cost_usd, close_leg_cost_usd,
                                      select_swaps)

SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT", "ADAUSDT",
           "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT"]
DATA_DIR = REPO / "binance_backtesting_data"
WINDOWS_PATH = REPO / "Engine" / "oos_windows_20.json"
START_CAPITAL = 5000.0
MS_8H = 8 * 3600 * 1000


def load_settlement_panel() -> tuple[pd.DatetimeIndex, pd.DataFrame, pd.DataFrame]:
    """Build causal 8h-settlement grids of funding (%/8h) and basis (bps)."""
    rates, basis = {}, {}
    for sym in SYMBOLS:
        df = pd.read_parquet(DATA_DIR / f"{sym}_15m_master_2020_2026.parquet",
                             columns=["open_time_ms", "funding_rate_pct", "basis_index_bps"])
        df = df.sort_values("open_time_ms").reset_index(drop=True)
        ts = pd.to_datetime(df["open_time_ms"], unit="ms", utc=True)
        # settlement bars: exactly 00:00/08:00/16:00 UTC
        m = ts.dt.minute.eq(0) & ts.dt.hour.isin([0, 8, 16])
        sub = df.loc[m].copy()
        sub["ts"] = ts[m]
        sub = sub.drop_duplicates("ts").set_index("ts").sort_index()
        rates[sym] = sub["funding_rate_pct"].astype(float)
        basis[sym] = sub["basis_index_bps"].astype(float)
    R = pd.DataFrame(rates).sort_index()
    B = pd.DataFrame(basis).sort_index()
    # common grid: inner join (all assets cover 2020-09+; grid intersection)
    common = R.dropna().index
    return common, R.loc[common], B.loc[common].ffill().fillna(0.0)


def run_backtest(cfg: CarryPolicyConfig):
    grid, R, B = load_settlement_panel()
    equity = START_CAPITAL
    holdings: dict[str, dict] = {}  # sym -> entry_ms, rate_pct, notional, basis_entry, qty_note
    eq_curve = []
    gross_funding = 0.0
    fee_drag = 0.0
    basis_pnl = 0.0
    rotations = 0
    notional_rotated = 0.0
    peak, max_dd = equity, 0.0

    for ts in grid:
        now_ms = int(ts.value // 1_000_000)
        r_now = R.loc[ts].to_dict()
        b_now = B.loc[ts].to_dict()

        # 1. Accrue settled rate on pairs held through this settlement.
        for sym, h in holdings.items():
            accrual = h["notional"] * (r_now[sym] / 100.0)
            equity += accrual
            gross_funding += accrual

        # 2. Policy decision (predictor = just-settled rate).
        for sym, h in holdings.items():
            h["neg_streak"] = h.get("neg_streak", 0) + 1 if r_now[sym] < 0.0 else 0
        ranked = sorted(r_now.items(), key=lambda kv: kv[1], reverse=True)
        exits, entries = select_swaps(ranked, holdings, now_ms, cfg)

        # 3. Execute exits (fees + realized signed basis).
        for sym in exits:
            h = holdings.pop(sym)
            fee = close_leg_cost_usd(h["notional"], cfg)
            equity -= fee
            fee_drag += fee
            bp = h["notional"] * (h["basis_entry"] - b_now[sym]) / 1e4
            equity += bp
            basis_pnl += bp
            rotations += 1
            notional_rotated += h["notional"]

        # 4. Execute entries (sized from current equity; fees; record basis).
        for sym in entries:
            notion = pair_notional_usd(equity, cfg)
            fee = open_leg_cost_usd(notion, cfg)
            equity -= fee
            fee_drag += fee
            holdings[sym] = {"entry_ms": now_ms, "rate_pct": r_now[sym],
                             "notional": notion, "basis_entry": b_now[sym],
                             "neg_streak": 0}
            notional_rotated += notion

        # 5. MTM (unrealized basis on open pairs) for the equity mark.
        mtm = sum(h["notional"] * (h["basis_entry"] - b_now[s]) / 1e4
                  for s, h in holdings.items())
        mtm_equity = equity + mtm
        peak = max(peak, mtm_equity)
        dd = (peak - mtm_equity) / peak * 100.0 if peak > 0 else 0.0
        max_dd = max(max_dd, dd)
        eq_curve.append((ts, mtm_equity))

    eq = pd.DataFrame(eq_curve, columns=["ts", "equity"]).set_index("ts").sort_index()
    # remaining open pairs: realize closing friction + basis at final mark
    b_last = B.iloc[-1].to_dict()
    for sym, h in holdings.items():
        fee = close_leg_cost_usd(h["notional"], cfg)
        equity -= fee
        fee_drag += fee
        bp = h["notional"] * (h["basis_entry"] - b_last[sym]) / 1e4
        equity += bp
        basis_pnl += bp
    net = equity - START_CAPITAL
    years = (grid[-1] - grid[0]).total_seconds() / (365.25 * 86400)
    cagr = (equity / START_CAPITAL) ** (1.0 / years) - 1.0
    daily = eq["equity"].resample("1D").last().pct_change().dropna()
    sharpe = (daily.mean() / daily.std() * np.sqrt(365.0)) if daily.std() > 0 else 0.0
    return {
        "equity_end": round(equity, 2), "net_pnl": round(net, 2),
        "roi_pct": round(net / START_CAPITAL * 100, 2),
        "cagr_pct": round(cagr * 100, 2),
        "max_dd_pct": round(max_dd, 2),
        "sharpe_daily": round(float(sharpe), 3),
        "gross_funding": round(gross_funding, 2),
        "fee_drag": round(fee_drag, 2),
        "basis_pnl": round(basis_pnl, 2),
        "rotations": rotations,
        "notional_rotated": round(notional_rotated, 2),
        "n_settlements": len(grid),
        "span": [str(grid[0].date()), str(grid[-1].date())],
        "eq_curve": eq,
    }


def attribute_regimes(eq: pd.DataFrame):
    windows = json.load(open(WINDOWS_PATH))
    rows = []
    for w in windows:
        s = pd.Timestamp(w["start_date"], tz="UTC")
        e = pd.Timestamp(w["end_date"], tz="UTC") + pd.Timedelta(days=1) - pd.Timedelta(milliseconds=1)
        sub = eq[(eq.index >= s) & (eq.index <= e)]["equity"]
        if len(sub) < 2:
            rows.append({"window_id": w["window_id"], "name": w["name"],
                         "start_eq": None, "end_eq": None, "pnl": None,
                         "roi_pct": None, "max_dd_pct": None, "status": "NO_DATA"})
            continue
        start_eq = float(eq[eq.index < s]["equity"].iloc[-1]) if (eq.index < s).any() else START_CAPITAL
        end_eq = float(sub.iloc[-1])
        peak = float(sub.cummax().max())
        trough = float((sub.cummax() - sub).max())
        dd = trough / peak * 100.0 if peak > 0 else 0.0
        pnl = end_eq - start_eq
        rows.append({"window_id": w["window_id"], "name": w["name"],
                     "start_eq": round(start_eq, 2), "end_eq": round(end_eq, 2),
                     "pnl": round(pnl, 2),
                     "roi_pct": round(pnl / start_eq * 100, 2),
                     "max_dd_pct": round(dd, 2),
                     "status": "PROFIT" if pnl > 0 else "LOSS"})
    return rows


def main():
    print("Loading settlement panel (11 assets, causal 8h grid)...", flush=True)
    results = {}
    for tag, fee_spot in [("mandated_8bps_spot", 0.0008), ("sensitivity_10bps_spot", 0.0010)]:
        cfg = CarryPolicyConfig(fee_spot=fee_spot)
        print(f"Running backtest [{tag}]...", flush=True)
        out = run_backtest(cfg)
        eq = out.pop("eq_curve")
        out["regimes"] = attribute_regimes(eq)
        results[tag] = out
        n_prof = sum(1 for r in out["regimes"] if r["status"] == "PROFIT")
        print(f"  [{tag}] net={out['net_pnl']:+.2f} ROI={out['roi_pct']:+.2f}% "
              f"CAGR={out['cagr_pct']:+.2f}% DD={out['max_dd_pct']:.2f}% "
              f"Sharpe={out['sharpe_daily']} gross={out['gross_funding']:+.2f} "
              f"fees={out['fee_drag']:.2f} basis={out['basis_pnl']:+.2f} "
              f"rotations={out['rotations']} regimes_profit={n_prof}/23", flush=True)

    with open(REPO / "Engine" / "research" / "carry_backtest_results.json", "w") as f:
        json.dump(results, f, indent=1)
    reg_rows = []
    for tag, out in results.items():
        for r in out["regimes"]:
            reg_rows.append({"leg": tag, **r})
    pd.DataFrame(reg_rows).to_csv(REPO / "Engine" / "research" / "carry_backtest_regimes.csv",
                                 index=False)
    print("Wrote carry_backtest_results.json + carry_backtest_regimes.csv", flush=True)


if __name__ == "__main__":
    main()
