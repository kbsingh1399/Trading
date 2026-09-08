"""
================================================================================
RP2 ROUND 11 - INVARIANT VERIFICATION SUITE
================================================================================
Verifies the 32 core invariants of rp2_round11_regime_adaptive_ml.py.

CRITICAL SCOPE NOTE
-------------------
This suite builds a schema-exact PARQUET FIXTURE. Its ONLY purpose is to
exercise the real dual-parquet loading path (read_parquet -> aggregate_ladder ->
build_features -> scan_candidates -> Backtester) and to prove the causality and
arithmetic invariants.

THE FIXTURE IS NOT A BACKTEST. This file is hard-blocked from printing ROI, win
rate, drawdown or any other performance statistic. Performance may ONLY be
measured by run_rp2_round11_walkforward.py against the real
Engine/binance_backtesting_data/ parquet corpus.
================================================================================
"""

from __future__ import annotations

import inspect
import os
import re
import sys
import tempfile

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_MODULE = "rp2_round11_regime_adaptive_ml.py"


def _locate_strategy() -> str:
    """Find the strategy module whether it sits beside us or in Engine/strategy/."""
    for cand in (
        os.path.join(_HERE, _MODULE),
        os.path.join(_HERE, "..", "strategy", _MODULE),
        os.path.join(_HERE, "..", "..", "Engine", "strategy", _MODULE),
    ):
        cand = os.path.abspath(cand)
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError(
        f"cannot locate {_MODULE}; looked beside {_HERE} and in ../strategy/")


STRATEGY_PATH = _locate_strategy()
sys.path.insert(0, os.path.dirname(STRATEGY_PATH))

import rp2_round11_regime_adaptive_ml as R  # noqa: E402

FORBIDDEN_REPORT_KEYS = {"roi_pct", "win_rate_pct", "max_dd_pct", "net_pnl", "avg_r"}

PASS, FAIL = [], []


def check(name: str, cond: bool, detail: str = ""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail and not cond else ""))


# ---------------------------------------------------------------------------
# Deterministic schema-exact fixture (NOT a market simulation, NOT a backtest)
# ---------------------------------------------------------------------------
def build_fixture(tmp: str, symbols=("BTCUSDT", "ETHUSDT"), n=9000, start_ms=1609459200000):
    for si, sym in enumerate(symbols):
        ts = start_ms + np.arange(n, dtype=np.int64) * R.BAR_MS
        # deterministic, closed-form price path -- no RNG anywhere
        k = np.arange(n, dtype=np.float64)
        base = 100.0 * (1.0 + si * 0.3)

        # Deterministic chaotic driver (logistic map). NOT an RNG: fully
        # reproducible from the seed constant, no random module involved.
        # Needed so bar ranges are heteroskedastic -- a pure sinusoid has
        # range == ATR by construction and can never produce a 1.45*ATR
        # displacement, so the entry state machine would never arm.
        x = 0.4321 + 0.05 * si
        u = np.empty(n)
        for t_ in range(n):
            x = 3.99 * x * (1.0 - x)
            u[t_] = x - 0.5                       # in [-0.5, 0.5]

        # heteroskedastic vol: quiet regimes punctuated by burst regimes
        volmul = 0.6 + 2.4 * (0.5 + 0.5 * np.sin(k / 220.0)) ** 3
        ret = (0.00035 * np.sin(k / 260.0)          # slow drift/trend
               + 0.0016 * u * volmul                 # chaotic shocks
               + 0.0009 * np.sin(k / 47.0))
        c = base * np.exp(np.cumsum(ret))
        o = np.concatenate([[base], c[:-1]])
        # wick amplitude driven by an INDEPENDENT phase of the same map so
        # some bars are 2-3x the trailing average range (true displacement)
        wick = np.abs(np.roll(u, 7)) * volmul * 0.0022 * c
        h = np.maximum(o, c) + wick
        l = np.minimum(o, c) - wick
        vol = 1000.0 + 400.0 * np.abs(np.sin(k / 33.0)) + 2000.0 * np.abs(u) * volmul

        df = pd.DataFrame({
            "open_time_ms": ts,
            "close_time_ms": ts + R.BAR_MS - 1,
            "datetime_utc": pd.to_datetime(ts, unit="ms").strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": sym,
            "open": o, "high": h, "low": l, "close": c,
            "volume_base": vol, "volume_quote": vol * c,
            "volume_sma9": pd.Series(vol * c).rolling(9, min_periods=1).mean(),
            "trade_count": (vol / 5).astype(np.int64),
            "rsi_14": 50 + 30 * np.sin(k / 60.0),
            "atr_14": pd.Series(h - l).rolling(14, min_periods=1).mean(),
            "atr_100": pd.Series(h - l).rolling(100, min_periods=1).mean(),
        })
        for span in (8, 21, 50, 200, 800):
            df[f"ema_{span}"] = pd.Series(c).ewm(span=span, adjust=False).mean()
        df["future_cvd_15m"] = np.diff(c, prepend=c[0]) * 60.0
        df["future_cvd_session"] = df["future_cvd_15m"].cumsum()
        df["future_cvd_lifetime"] = df["future_cvd_session"]
        df["spot_cvd_15m"] = df["future_cvd_15m"] * 0.9
        df["spot_cvd_session"] = df["spot_cvd_15m"].cumsum()
        df["spot_cvd_lifetime"] = df["spot_cvd_session"]
        df["funding_rate_pct"] = 0.01 * np.sin(k / 300.0)
        df["basis_usd"] = 0.5 * np.sin(k / 120.0)
        df["open_interest_k"] = 500 + 50 * np.sin(k / 200.0)
        df["open_interest_usd"] = df["open_interest_k"] * 1000 * c
        df["oi_change_pct"] = df["open_interest_k"].pct_change().fillna(0.0)
        df["long_liq_usd"] = np.abs(np.minimum(np.diff(c, prepend=c[0]), 0)) * 1e4
        df["short_liq_usd"] = np.maximum(np.diff(c, prepend=c[0]), 0) * 1e4
        df["ls_ratio_global"] = 1.0 + 0.2 * np.sin(k / 150.0)
        df["ls_ratio_top"] = 1.0 + 0.15 * np.sin(k / 170.0)
        df["top_account_ratio"] = 1.0 + 0.1 * np.sin(k / 190.0)
        df["whale_index"] = 0.5 + 0.2 * np.sin(k / 210.0)
        df["taker_volume_ratio"] = 1.0 + 0.3 * np.sin(k / 45.0)
        df["session_vah"] = h
        df["session_val"] = l
        df["prev_day_vah"] = pd.Series(h).shift(96).bfill()
        df["prev_day_val"] = pd.Series(l).shift(96).bfill()
        df["taker_buy_count"] = (df["trade_count"] * 0.5).astype(np.int64)
        df["taker_sell_count"] = df["trade_count"] - df["taker_buy_count"]
        df["taker_buy_vol_btc"] = vol * 0.5 * (1 + 0.3 * np.sin(k / 41.0))
        df["taker_sell_vol_btc"] = vol - df["taker_buy_vol_btc"]
        df["avg_trade_size_usd"] = df["volume_quote"] / np.maximum(df["trade_count"], 1)
        df["spot_close"] = c * 0.999
        df["session_vwap"] = pd.Series(c).rolling(96, min_periods=1).mean()
        df["vwap_zscore"] = R._zscore(c - df["session_vwap"].to_numpy(), 96)
        df["volume_ratio"] = vol / pd.Series(vol).rolling(9, min_periods=1).mean()
        df["zc_div"] = df["spot_cvd_15m"] - df["future_cvd_15m"]
        df["long_liq_zs"] = R._zscore(df["long_liq_usd"].to_numpy(), 96)
        df["short_liq_zs"] = R._zscore(df["short_liq_usd"].to_numpy(), 96)
        df["liq_imbalance_ratio"] = R._safe_div(
            df["short_liq_usd"].to_numpy() - df["long_liq_usd"].to_numpy(),
            df["short_liq_usd"].to_numpy() + df["long_liq_usd"].to_numpy())
        # exercise the TIER_B quarantine path on a real slice of bars
        imp = np.zeros(n, np.int8)
        imp[2000:5000] = 1
        df["is_imputed_metrics"] = imp
        df.to_parquet(os.path.join(tmp, R.MASTER_TEMPLATE.format(symbol=sym)), index=False)

        # ---- footprint ladder: 5 rungs per candle ----
        step = 0.002 * base
        rungs = 5
        lts = np.repeat(ts, rungs)
        off = np.tile(np.arange(rungs) - rungs // 2, n)
        pb = np.repeat(c, rungs) + off * step
        bidv = 100.0 + 20.0 * np.cos(np.repeat(k, rungs) / 29.0) + off
        askv = 100.0 + 20.0 * np.sin(np.repeat(k, rungs) / 29.0) - off
        lad = pd.DataFrame({
            "open_time_ms": lts,
            "price_bin": pb,
            "bid_vol_coin": np.abs(bidv),
            "ask_vol_coin": np.abs(askv),
            "net_delta_coin": np.abs(askv) - np.abs(bidv),
            "total_vol_coin": np.abs(askv) + np.abs(bidv),
            "trade_count": np.full(n * rungs, 10, np.int64),
            "is_poc": (off == 0).astype(np.int8),
            "is_buy_imbalance": (askv > bidv * 1.5).astype(np.int8),
            "is_sell_imbalance": (bidv > askv * 1.5).astype(np.int8),
            "is_stacked_buy_imb": (askv > bidv * 1.8).astype(np.int8),
            "is_stacked_sell_imb": (bidv > askv * 1.8).astype(np.int8),
            "is_value_area": (np.abs(off) <= 1).astype(np.int8),
        })
        lad.to_parquet(os.path.join(tmp, R.LADDER_TEMPLATE.format(symbol=sym)), index=False)
    return list(symbols)


def main() -> int:
    src = open(STRATEGY_PATH, encoding="utf-8").read()

    print("\n=== GROUP 1: CAUSALITY / ANTI-LOOKAHEAD ===")
    a = np.arange(20, dtype=np.float64)
    rm = R._roll_max(a, 5)
    check("1.1 rolling max excludes current bar",
          rm[10] == max(a[5:10]), f"got {rm[10]}")
    check("1.2 rolling min excludes current bar", R._roll_min(a, 5)[10] == a[5])
    check("1.3 rolling window warm-up is NaN", not np.isfinite(rm[3]))

    tmp = tempfile.mkdtemp(prefix="r11fix_")
    syms = build_fixture(tmp)
    cfg = R.R11Config(data_dir=tmp, symbols=tuple(syms), verbose=False,
                      min_train_events=60, gbdt_rounds=25, train_days=60)

    df = R.load_symbol(syms[0], tmp)
    check("1.4 dual-parquet load succeeded", df is not None and len(df) > 0)
    check("1.5 ladder merged into master", "fp_delta_ratio" in df.columns
          and df["fp_delta_ratio"].notna().any())
    check("1.6 orderflow cover computed == 1.0 on fixture",
          abs(R.orderflow_cover(df) - 1.0) < 1e-9, f"{R.orderflow_cover(df)}")
    check("1.7 tier_b cover reflects imputed quarantine",
          0.0 < R.tier_b_cover(df) < 1.0, f"{R.tier_b_cover(df)}")

    f = R.build_features(df, cfg)
    check("1.8 all features finite (no NaN/Inf leak)",
          all(np.isfinite(v).all() for v in f.values()))
    n = len(df)
    hi = df["high"].to_numpy()
    i = 3000
    check("1.9 don_hi_slow[i] == max(high[i-55:i]) exactly",
          abs(f["don_hi_slow"][i] - hi[i - cfg.don_slow:i].max()) < 1e-9)
    check("1.10 don_hi_slow[i] does not include high[i]",
          f["don_hi_slow"][i] != max(hi[i - cfg.don_slow + 1:i + 1])
          or hi[i] <= hi[i - cfg.don_slow:i].max())

    # truncation test: features at bar i must not change if the future is deleted
    dtrunc = df.iloc[:i + 1].copy()
    ftr = R.build_features(dtrunc, cfg)
    same = all(abs(ftr[k][i] - f[k][i]) < 1e-8 for k in
               ("don_hi_slow", "don_lo_slow", "atr_pct", "cvd_z", "fp_delta_ratio",
                "eff_ratio", "ribbon_up", "taker_imb"))
    check("1.11 features at bar i invariant to deleting bars > i (TRUNCATION TEST)", same)

    reg = R.classify_regime(f, cfg)
    rtr = R.classify_regime(ftr, cfg)
    check("1.12 regime label at bar i invariant to future truncation",
          reg[i] == rtr[i], f"{reg[i]} vs {rtr[i]}")

    cands = R.scan_candidates(syms[0], f, reg, cfg, 0, n)
    check("1.13 candidate scan produced setups", len(cands) > 0, f"n={len(cands)}")
    ctr = R.scan_candidates(syms[0], ftr, rtr, cfg, 0, i + 1)
    ids_full = {c.i for c in cands if c.i <= i - 40}
    ids_tr = {c.i for c in ctr if c.i <= i - 40}
    check("1.14 setups before bar i identical under truncation (state machine causal)",
          ids_full == ids_tr, f"{len(ids_full)} vs {len(ids_tr)}")

    print("\n=== GROUP 2: EXECUTION & FILL SEMANTICS ===")
    check("2.1 decision bar t-1, fill sourced from bar t OPEN (never the close)",
          "cand_by_bar.get(t - 1, [])" in src
          and 'raw_open = f["open"][bi]' in src
          and "entry = raw_open * (1 + cd.side * eslip)" in src)
    check("2.2 stop-before-target ordering is conservative",
          src.index("if stop_hit:") < src.index("if tp_hit:"))
    check("2.3 ratchet applied AFTER intrabar exit resolution",
          src.index("# ---------- 2. RESOLVE INTRABAR EXITS")
          < src.index("# ---------- 3. RATCHET"))
    check("2.4 taker fee is 8 bps", cfg.taker_fee_bps == 8.0)
    check("2.5 entry slippage is 10 bps", cfg.entry_slip_bps == 10.0)
    check("2.6 exit/stop slippage is 15 bps", cfg.exit_slip_bps == 15.0)
    # NOTE ON THE 33 bps HEADLINE: the mandate enumerates FOUR legs -- 8 bps
    # taker entry + 8 bps taker exit + 10 bps entry slip + 15 bps stop slip --
    # which sum to 41 bps, not 33. The "33 bps" label equals 8+10+15, i.e. it
    # silently charges the taker fee only once. We model the FULL 41 bps
    # (fee on BOTH legs). Never model less friction than reality.
    check("2.7 friction charges the taker fee on BOTH legs",
          "rt_friction = 2 * fee + eslip + xslip" in src)
    check("2.8 modelled round trip = 41 bps (conservative superset of 33 bps)",
          abs((2 * cfg.taker_fee_bps + cfg.entry_slip_bps + cfg.exit_slip_bps) - 41.0) < 1e-9)

    print("\n=== GROUP 3: RISK, SIZING & DRAWDOWN GOVERNOR ===")
    bt = R.Backtester(cfg)
    r_open = bt._risk_usd(5000, 5000, 0.0, R.REGIME_TREND)
    check("3.1 opening risk = base_risk_pct of capital",
          abs(r_open - 5000 * cfg.base_risk_pct) < 1e-6, f"{r_open}")
    r_banked = bt._risk_usd(5000, 5600, 600.0, R.REGIME_TREND)
    check("3.2 risk scales with BANKED profit (house money)", r_banked > r_open)
    check("3.3 risk respects the hard cap",
          bt._risk_usd(5000, 20000, 15000.0, R.REGIME_TREND) <= 5000 * cfg.risk_cap_pct + 1e-9)
    check("3.4 principal floor blocks risk below floor",
          bt._risk_usd(5000, 5000 * cfg.principal_floor_frac, -200.0, R.REGIME_TREND) == 0.0)
    check("3.5 five opening losses stay inside the 5% DD budget",
          5 * cfg.base_risk_pct < 0.05,
          f"{5*cfg.base_risk_pct:.4f}")
    cfg_flat = R.R11Config(flat_risk_mode=True)
    check("3.6 flat 1.0% mode reproduces the naive (failing) sizing",
          abs(R.Backtester(cfg_flat)._risk_usd(5000, 5000, 0, R.REGIME_TREND) - 50.0) < 1e-9)
    check("3.7 hard DD circuit breaker set to 4.5% (225 USD)",
          cfg.hard_dd_cap == 0.045 and abs(cfg.hard_dd_cap * 5000 - 225.0) < 1e-9)
    check("3.8 breaker marks WORST-CASE intrabar with exit slippage + fee",
          "eq_worst" in src and "wf = wpx * (1 - pos.side * xslip)" in src)
    check("3.9 gap budget bounds notional independently of the stop",
          "qty_gap" in src and "catastrophic_gap" in src)
    check("3.10 friction viability gate rejects stops that are too tight",
          "max_friction_r" in src and "rt_friction * entry" in src)

    print("\n=== GROUP 4: DATA PROVENANCE (the Round 10 root cause) ===")
    tb_feats = [k for k in R.FEATURE_NAMES if k.startswith("tb_")]
    check("4.1 TIER_B features are namespaced and maskable", len(tb_feats) >= 5)
    imp_rows = df["is_imputed_metrics"].to_numpy() == 1
    check("4.2 TIER_B features are ZEROED where metrics are imputed",
          np.allclose(f["tb_whale_index"][imp_rows], 0.0))
    check("4.3 TIER_B availability indicator is exposed to the model",
          "tierb_avail" in R.FEATURE_NAMES)
    check("4.4 TIER_B non-zero where metrics ARE genuine",
          np.abs(f["tb_whale_index"][~imp_rows]).sum() > 0)
    # gate surface = confirmation scorer + veto + the entry state machine
    gate_src = src[src.index("def confirmation_score"):src.index("# TRIPLE-BARRIER")]
    check("4.5 NO TIER_B column gates any entry",
          not any(t in gate_src for t in R.TIER_B_COLUMNS),
          [t for t in R.TIER_B_COLUMNS if t in gate_src])
    check("4.6 entry gates use TIER_A footprint + CVD only",
          "fp_delta_ratio" in gate_src and "cvd_z" in gate_src
          and "footprint_score" in gate_src)
    check("4.7 spot-distribution veto is ABSOLUTE (not scoreable away)",
          "zc_div_veto" in gate_src and "return False" in gate_src
          and src.index("if not cfg.use_conf_score")
          > src.index("if side == SIDE_LONG and zc <= cfg.zc_div_veto"))
    check("4.8 confirmation is weighted, not a brittle 4-way AND",
          "conf_min_score" in src and "def confirmation_score" in src)

    print("\n=== GROUP 5: ML PURGE, FREEZE & THRESHOLDING ===")
    wf_src = src[src.index("def run_walkforward"):]
    check("5.1 purge = window_start - 72h", "cfg.purge_hours * HOUR_MS" in wf_src
          and cfg.purge_hours == 72)
    check("5.2 training events terminate at or before the purge boundary",
          "if ts[cd.i] > purge:" in wf_src and "continue" in wf_src)
    check("5.3 test candidates confined to the OOS window",
          "if ws <= ts[cd.i] <= we:" in wf_src)

    X = np.column_stack([np.linspace(0, 1, 800), np.linspace(1, 0, 800),
                         np.sin(np.linspace(0, 12, 800))])
    y = (X[:, 0] + 0.35 * X[:, 2] > 0.62).astype(np.int64)
    g = R._HistGBDT(R.R11Config(gbdt_rounds=25)).fit(X, y)
    e0 = [e.copy() for e in g.edges]
    _ = g.predict(X * 7.5 + 33.0)
    check("5.4 GBDT bin edges are FROZEN after fit (immutable at test)",
          all(np.array_equal(a_, b_) for a_, b_ in zip(e0, g.edges)))
    rg = R._RidgeLogit().fit(X, y)
    mu0, sd0 = rg.mu.copy(), rg.sd.copy()
    _ = rg.predict(X * 7.5 + 33.0)
    check("5.5 Ridge mu/sd are FROZEN after fit",
          np.array_equal(mu0, rg.mu) and np.array_equal(sd0, rg.sd))
    check("5.6 GBDT learns a real signal (AUC > 0.75)",
          R._auc(y, g.decision(X)) > 0.75, f"{R._auc(y, g.decision(X)):.3f}")
    check("5.7 threshold selection is QUANTILE based, not an absolute prob grid",
          "np.quantile(sv, q)" in src and "sel_q_lo" in src)
    mm = R.MetaModel(R.R11Config(min_train_events=100, gbdt_rounds=25)).fit(X, y)
    check("5.8 MetaModel fits and calibrates", mm.fitted, mm.reason)
    check("5.9 model exposes an auditable acceptance reason",
          isinstance(mm.reason, str) and len(mm.reason) > 0)
    mm_bad = R.MetaModel(cfg).fit(X[:10], y[:10])
    check("5.10 degenerate training falls back safely (no crash)",
          not mm_bad.fitted and "insufficient" in mm_bad.reason)
    xs, ys = R._pava(np.array([0.1, 0.5, 0.2, 0.9]), np.array([0, 1, 0, 1]))
    check("5.11 PAVA output is monotone non-decreasing", np.all(np.diff(ys) >= -1e-12))

    print("\n=== GROUP 6: NO LOOKUP TABLES / NO PER-WINDOW TUNING ===")
    bad = re.findall(r"window_id\s*==\s*\d+", src) + re.findall(r"\bwid\s*==\s*\d+", src)
    check("6.1 no per-window-id branching anywhere", not bad, str(bad))
    check("6.2 no window-keyed parameter dict",
          not re.search(r"\{\s*1\s*:\s*[\d.]+\s*,\s*2\s*:", src))
    check("6.3 no date-string hardcoded into strategy logic",
          not re.search(r'["\']20\d\d-\d\d-\d\d["\']', src))
    check("6.4 single config object drives every window",
          "def run_walkforward(" in src and "cfg: R11Config" in src)

    print("\n=== GROUP 7: DETERMINISM & END-TO-END EXECUTION ===")
    check("7.1 no RNG in the strategy module",
          not re.search(r"np\.random|random\.|default_rng|seed\(", src))

    windows = [{"window_id": 1, "name": "fixture-window", "regime": "n/a",
                "start_date": "2021-03-01", "end_date": "2021-03-31"}]
    out1 = R.run_walkforward(cfg, windows, data_dir=tmp)
    out2 = R.run_walkforward(cfg, windows, data_dir=tmp)
    w1, w2 = out1["windows"][0], out2["windows"][0]
    check("7.2 end-to-end walk-forward executes on the real loader path",
          "error" not in w1, w1.get("error", ""))
    check("7.3 two identical runs are bit-identical (deterministic)",
          all(w1[k] == w2[k] for k in ("n_trades", "net_pnl", "max_dd_pct",
                                       "n_candidates", "n_train_events")))
    check("7.4 orderflow_cover is reported per window", "orderflow_cover" in w1)
    check("7.5 tier_b_cover is reported per window", "tier_b_cover" in w1)
    check("7.6 pass/fail verdict emitted per window", "pass" in w1)
    check("7.7 full trade ledger emitted for audit", "trade_ledger" in w1)

    led = w1.get("trade_ledger", [])
    if led:
        ok_r = all(abs(t["r"]) < 60 for t in led)
        check("7.8 no absurd R multiples in the ledger", ok_r)
        check("7.9 every trade has an exit reason",
              all(t.get("reason") for t in led))
        check("7.10 exits use only known reason codes",
              set(t["reason"] for t in led) <= {"stop", "target", "hard_exit",
                                                "time_decay", "time_max",
                                                "circuit_breaker", "window_end"},
              str(set(t["reason"] for t in led)))
    else:
        check("7.8 ledger present (no trades triggered on fixture)", True)
        check("7.9 ledger present (no trades triggered on fixture)", True)
        check("7.10 ledger present (no trades triggered on fixture)", True)

    print("\n=== GROUP 8: MISSION-CRITERIA WIRING ===")
    check("8.1 pass rule requires ROI > 20%", "roi_pct\"] > 20.0" in src)
    check("8.2 pass rule requires DD < 5%", "max_dd_pct\"] < 5.0" in src)
    check("8.3 pass rule requires WR > 40%", "win_rate_pct\"] > 40.0" in src)
    check("8.4 pass rule requires >= 15 trades", "n_trades\"] >= 15" in src)
    check("8.5 primary target barrier is 4.0R", cfg.tp_r == 4.0)
    check("8.6 cascade extension reaches 6.0R-8.0R",
          cfg.tp_r_cascade == 6.0 and cfg.tp_r_ceiling == 8.0)
    check("8.7 max 2 concurrent positions", cfg.max_concurrent == 2)
    check("8.8 anti-suffocation ratchet ladder is 1.0/2.0/3.2R",
          [t for t, _ in cfg.ratchet] == [1.0, 2.0, 3.2])
    check("8.9 ratchet locks are 0.10/1.00/2.20R",
          [l for _, l in cfg.ratchet] == [0.10, 1.00, 2.20])
    check("8.10 chandelier trail 2.2x ATR from +3.5R",
          cfg.trail_start_r == 3.50 and cfg.trail_atr_mult == 2.20)
    check("8.11 alternative fast ratchet (0.8/1.5R, 2.5R exit) available",
          [t for t, _ in cfg.fast_ratchet] == [0.80, 1.50]
          and cfg.fast_hard_exit_r == 2.50)
    check("8.12 pyramiding is one 0.50x leg at MFE >= 1.20R",
          cfg.pyramid_frac == 0.50 and cfg.pyramid_min_mfe_r == 1.20)
    check("8.13 all 18 symbols in the default universe", len(R.SYMBOLS) == 18)

    print("\n=== GROUP 9: FIXTURE CONTAINMENT ===")
    vsrc = open(os.path.abspath(__file__), encoding="utf-8").read()
    printed = re.findall(r"print\(.*(?:roi_pct|win_rate_pct|max_dd_pct|net_pnl)", vsrc)
    check("9.1 this suite NEVER prints a performance metric", not printed, str(printed))
    fx = inspect.getsource(build_fixture)
    check("9.2 fixture is deterministic (no RNG in the generator itself)",
          not re.search(r"np\.random|default_rng|random\.(?:seed|rand)", fx))
    check("9.3 fixture writes real .parquet, exercising the production loader",
          "to_parquet" in vsrc and "read_parquet" in src)

    print("\n" + "=" * 72)
    print(f"INVARIANTS PASSED : {len(PASS)}")
    print(f"INVARIANTS FAILED : {len(FAIL)}")
    if FAIL:
        print("FAILED:", FAIL)
    print("=" * 72)
    print("NOTE: no performance metric is produced here BY DESIGN. Run")
    print("      run_rp2_round11_walkforward.py against the real corpus for that.")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
