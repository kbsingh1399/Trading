"""stage2_ensemble.py v2 — ML + HMM gating over battery-v2 pools; walk-forward
family expectancy gate; mandate executor; block-bootstrap Monte Carlo.

Causal chain per window k: fit GaussianHMM(2) on BTC 4h returns from TRAIN
ONLY → causal forward-filter states → family gate (trailing 60d net expectancy
per family on train > 0, fallback top-3) → two LGBM heads (regressor on
clipped r + classifier on r>0) → blended score → daily top-1 → executor
(concurrency 3, house-money 40→100, DD-defense 20). No test-row feature uses
future test rows.

Monte Carlo: block bootstrap (block=10 trades, 5000 paths) over the global
executed sequence → P(pooled ROI >= +10%/mo-equivalent), P(pooled DD > 5%).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO_PRE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_PRE))

import numpy as np
import pandas as pd
import lightgbm as lgb
from hmmlearn.hmm import GaussianHMM

REPO = Path(__file__).resolve().parent.parent
POOL_DIR = REPO / "scratch" / "battery_pools_v2"
OUT_JSON = REPO / "scratch" / "ml_reversal_results" / "stage2_v2_scorecard.json"
WINDOWS_PATH = REPO / "Engine" / "oos_windows_20.json"
CRITERIA_PATH = REPO / "Engine" / "target_oos_criteria.json"
BTC_PARQUET = REPO / "Engine" / "binance_backtesting_data" / "BTCUSDT_15m_master_2020_2026.parquet"
PURGE_MS = 72 * 3600 * 1000

FEATURE_COLS = ["vwap_zscore", "rsi_14", "atr_ratio", "volume_ratio",
                "funding_rate_pct", "basis_index_bps", "tide", "hour", "dow",
                "mom_3d", "ret_672", "fund_z", "basis_z", "oi_z", "lst_z",
                "dist90hi", "ret_1344", "r7_z", "xs_rank", "side",
                "fam_id", "geo_id", "hmm_state"]


def augment_pools(store: dict) -> pd.DataFrame:
    from scratch.strategy_battery import spec_list, GEOS
    geo_of = {(f, t): g for f, t, g in spec_list()}
    geo_ids = {g: i for i, g in enumerate(GEOS)}
    fams = {}
    for f, t, g in spec_list():
        fams.setdefault(f, len(fams))
    parts = []
    for f in sorted(POOL_DIR.glob("*.parquet")):
        fam, tag = f.stem.split("__")
        geo_key = geo_of[(fam, tag)]
        pool = pd.read_parquet(f)
        for sym, sub in pool.groupby("sym"):
            if sym not in store:
                continue
            d = store[sym]
            pos = pd.Index(d.open_time_ms).get_indexer(sub["t"])
            ok = pos >= 0
            sub = sub[ok].reset_index(drop=True)
            pos = pos[ok]

            def col(name, fill):
                if name in d.columns:
                    return d[name].fillna(fill).to_numpy()[pos]
                return np.full(len(pos), fill)

            feat = pd.DataFrame({
                "vwap_zscore": col("vwap_zscore", 0.0),
                "rsi_14": col("rsi_14", 50.0),
                "atr_ratio": col("atr_ratio", 1.0),
                "volume_ratio": col("volume_ratio", 1.0),
                "funding_rate_pct": col("funding_rate_pct", 0.0),
                "basis_index_bps": col("basis_index_bps", 0.0),
                "tide": col("tide", 0),
                "hour": col("hour", 0),
                "dow": col("dow", 0),
                "mom_3d": col("ret_288", 0.0),
                "ret_672": col("ret_672", 0.0),
                "fund_z": col("fund_z", 0.0),
                "basis_z": col("basis_z", 0.0),
                "oi_z": col("oi_z", 0.0),
                "lst_z": col("lst_z", 0.0),
                "dist90hi": col("dist90hi", 0.0),
                "ret_1344": col("ret_1344", 0.0),
                "r7_z": col("r7_z", 0.0),
                "xs_rank": col("xs_rank", 0.5),
                "t": sub["t"].to_numpy(),
                "r": sub["r"].to_numpy(),
                "side": sub["side"].to_numpy(),
                "bars": sub["bars"].to_numpy(),
                "sym": sym,
                "fam": fam,
                "fam_id": fams[fam],
                "geo_id": geo_ids[geo_key],
            })
            parts.append(feat)
    big = pd.concat(parts, ignore_index=True).sort_values("t").reset_index(drop=True)
    return big


def btc_4h_returns():
    df = pd.read_parquet(BTC_PARQUET, columns=["open_time_ms", "close"])
    return pd.Series(df["close"].pct_change(16).to_numpy(), index=df["open_time_ms"].to_numpy())


def fit_forward_states(train_rets, test_rets, seed=7):
    hmm = GaussianHMM(n_components=2, covariance_type="diag", n_iter=100,
                      random_state=seed, tol=1e-3)
    hmm.fit(train_rets.reshape(-1, 1))
    vari = hmm.covars_.ravel()
    order = np.argsort(-vari)  # state 0 = highest vol
    means = hmm.means_.ravel()
    stds = np.sqrt(np.maximum(hmm.covars_.ravel(), 1e-12))
    A = hmm.transmat_
    pi = hmm.startprob_
    alpha = pi * np.exp(-(test_rets[0] - means) ** 2 / (2 * stds ** 2)) / (stds * np.sqrt(2 * np.pi))
    s = alpha.sum()
    alpha = alpha / s if s > 0 else np.ones_like(alpha) / len(alpha)
    states = np.zeros(len(test_rets), dtype=int)
    for k in range(len(test_rets)):
        states[k] = int(np.argmax(alpha))
        if k + 1 < len(test_rets):
            lik = np.exp(-(test_rets[k + 1] - means) ** 2 / (2 * stds ** 2)) / (stds * np.sqrt(2 * np.pi))
            alpha = (alpha @ A) * lik
            s = alpha.sum()
            alpha = alpha / s if s > 0 else np.ones_like(alpha) / len(alpha)
    remap = {old: new for new, old in enumerate(order)}
    return np.array([remap[x] for x in states], dtype=float)


def block_bootstrap_mc(trade_pnl: np.ndarray, capital: float, horizon_n: int,
                       block: int = 10, paths: int = 5000, seed=11):
    """Monthly-equivalent ROI/DD distribution by resampling executed-trade blocks."""
    if len(trade_pnl) < 5:
        return {}
    rng = np.random.default_rng(seed)
    n = len(trade_pnl)
    nb = int(np.ceil(n / block))
    rois = np.empty(paths)
    dds = np.empty(paths)
    for p in range(paths):
        seq = []
        while len(seq) < horizon_n:
            b = rng.integers(0, nb)
            seq.extend(trade_pnl[b * block:(b + 1) * block])
        eq = capital + np.cumsum(np.array(seq[:horizon_n]))
        peak = np.maximum.accumulate(eq)
        dds[p] = np.max((peak - eq) / peak * 100)
        rois[p] = (eq[-1] - capital) / capital * 100
    return {"P_ROI>=10": float((rois >= 10).mean()), "P_DD>5": float((dds > 5).mean()),
            "median_ROI": float(np.median(rois)), "median_DD": float(np.median(dds)),
            "p05_ROI": float(np.quantile(rois, 0.05)), "p95_ROI": float(np.quantile(rois, 0.95))}


def run():
    from scratch.strategy_battery import get_store
    t_all = time.perf_counter()
    with open(CRITERIA_PATH) as f:
        criteria = json.load(f)["target_criteria"]
    with open(WINDOWS_PATH) as f:
        windows = json.load(f)
    CAPITAL = criteria.get("initial_capital_usd", 5000.0)
    MIN_ROI = criteria.get("min_roi_percent", 10.0)
    MAX_DD = criteria.get("max_dd_percent", 5.0)
    MIN_WR = criteria.get("min_winrate_percent", 40.0)
    MIN_TRADES = criteria.get("min_trades", 15)

    print("[stage2] loading store + augmenting...", flush=True)
    store = get_store()
    big = augment_pools(store)
    big.to_parquet(REPO / "scratch" / "union_pool_v2.parquet", index=False)
    print(f"[stage2] union: {len(big):,d} | net r mean {big.r.mean():+.4f}", flush=True)

    btc_ret4 = btc_4h_returns()
    btc_index = btc_ret4.index

    results = []
    pass_count = 0
    total_pnl = 0.0
    all_pnl = []

    print("=" * 128, flush=True)
    print(f"{'W#':<3} | {'Window':<38} | {'Cands':<7} | {'Trades':<6} | {'WinRate':<8} | {'Net PnL':<12} | {'Net ROI':<9} | {'MaxDD':<7} | {'Verdict':<6}", flush=True)
    print("-" * 128, flush=True)

    for w in windows:
        w_id, w_name = w["window_id"], w["name"]
        start_ms = pd.Timestamp(w["start_date"], tz="UTC").value // 1_000_000
        end_ms = pd.Timestamp(w["end_date"] + " 23:59:59", tz="UTC").value // 1_000_000
        cutoff = start_ms - PURGE_MS

        train = big[big.t < cutoff]
        test = big[(big.t >= start_ms) & (big.t <= end_ms)]
        if len(train) < 400 or len(test) == 0:
            print(f"W{w_id:02d} | {w_name[:38]:<38} | skipped (train {len(train)})", flush=True)
            continue

        # ---- causal HMM states
        tr_btc = btc_ret4[btc_index < cutoff].dropna().to_numpy()
        te_btc_s = btc_ret4[(btc_index >= cutoff - 200 * 86_400_000) & (btc_index <= end_ms)].dropna()
        try:
            states = fit_forward_states(tr_btc, te_btc_s.to_numpy())
            state_map = pd.Series(states, index=te_btc_s.index.to_numpy())
            hmm_train = train["t"].map(state_map).fillna(0.0).to_numpy()
            hmm_test = test["t"].map(state_map).fillna(0.0).to_numpy()
        except Exception:
            hmm_train = np.zeros(len(train))
            hmm_test = np.zeros(len(test))
        train = train.copy()
        test = test.copy()
        train["hmm_state"] = hmm_train
        test["hmm_state"] = hmm_test

        # ---- walk-forward family gate: trailing 60d train expectancy
        trail_win = cutoff - 60 * 86_400_000
        fam_trail = train[train.t >= trail_win].groupby("fam")["r"].mean()
        ok_fams = set(fam_trail[fam_trail > 0].index)
        if len(ok_fams) < 3:
            ok_fams = set(fam_trail.sort_values(ascending=False).head(5).index)
        train_g = train[train.fam.isin(ok_fams)]
        test_g = test[test.fam.isin(ok_fams)]
        if len(test_g) == 0:
            train_g, test_g = train, test

        # bound training pool to last 540 days (causal, bounds runtime)
        t0 = cutoff - 540 * 86_400_000
        train_g = train_g[train_g.t >= t0]
        ml_on = len(train_g) >= 400
        if not ml_on and len(train) >= 400:
            train_g, test_g = train[train.t >= t0], test
            ml_on = len(train_g) >= 400
        if not ml_on:
            print(f"W{w_id:02d} | {w_name[:38]:<38} | skipped (gated train {len(train_g)})", flush=True)
            continue

        # ML fallback if still short: rank by family trailing mean
        if not ml_on:
            fam_mean = fam_trail.to_dict()
            score = test_g["fam"].map(fam_mean).fillna(-1.0).to_numpy()
            days = pd.to_datetime(test_g["t"].to_numpy(), unit="ms", utc=True).normalize()
            sel = []
            for _, arr in pd.Series(np.arange(len(test_g)), index=days).groupby(level=0):
                arr = np.asarray(arr)
                sel.append(int(arr[np.argmax(score[arr])]))
            sel = np.array(sorted(sel), dtype=int)
            tt = test_g["t"].to_numpy(); rr = test_g["r"].to_numpy()
            bars = test_g["bars"].to_numpy(); syms = test_g["sym"].to_numpy()
            X_tr = None
        else:
            X_tr = train_g[FEATURE_COLS]
        if X_tr is not None:
            y_reg = np.clip(train_g["r"].to_numpy(), -1.6, 4.0)
            y_cls = (train_g["r"] > 0).astype(int).to_numpy()
        reg = lgb.LGBMRegressor(n_estimators=150, max_depth=3, learning_rate=0.03,
                                subsample=0.8, colsample_bytree=0.8, reg_alpha=2.0,
                                reg_lambda=4.0, random_state=42, verbose=-1, n_jobs=-1)
        clf = lgb.LGBMClassifier(n_estimators=150, max_depth=3, learning_rate=0.03,
                                 subsample=0.8, colsample_bytree=0.8, reg_alpha=2.0,
                                 reg_lambda=4.0, random_state=42, verbose=-1, n_jobs=-1)
        if X_tr is not None:
            reg.fit(X_tr, y_reg)
            clf.fit(X_tr, y_cls)
            X_te = test_g[FEATURE_COLS]
            zr = (reg.predict(X_te) - reg.predict(X_tr).mean()) / (reg.predict(X_tr).std() + 1e-9)
            score = zr + 2.0 * (clf.predict_proba(X_te)[:, 1] - 0.5)

        # daily top-2: best overall + best fast/mid-geo (keeps book fluid)
        if X_tr is not None:
            days = pd.to_datetime(test_g["t"].to_numpy(), unit="ms", utc=True).normalize()
            sel = []
            gids = test_g["geo_id"].to_numpy()
            for _, arr in pd.Series(np.arange(len(test_g)), index=days).groupby(level=0):
                arr = np.asarray(arr)
                sel.append(int(arr[np.argmax(score[arr])]))
                fast = arr[gids[arr] <= 1]
                if len(fast):
                    sel.append(int(fast[np.argmax(score[fast])]))
            sel = np.array(sorted(set(sel)), dtype=int)

        # ---- executor
        tt = test_g["t"].to_numpy()
        rr = test_g["r"].to_numpy()
        bars = test_g["bars"].to_numpy()
        syms = test_g["sym"].to_numpy()
        open_pos = []
        executed = []
        equity, peak, cur_dd = CAPITAL, CAPITAL, 0.0
        for k in sel:
            t_entry = tt[k]
            open_pos = [op for op in open_pos if op[0] > t_entry]
            if syms[k] in [op[1] for op in open_pos]:
                continue
            if len(open_pos) >= 4:
                continue
            open_pos.append((t_entry + int(bars[k]) * 900_000, syms[k]))
            r_gain = rr[k]
            if cur_dd >= 2.0:
                risk = 20.0
            elif (equity - CAPITAL) >= 50.0:
                risk = min(100.0, 40.0 + (equity - CAPITAL) * 0.40)
            else:
                risk = 40.0
            pnl = r_gain * risk
            executed.append({"t": int(t_entry), "r": float(r_gain), "pnl": float(pnl)})
            equity += pnl
            peak = max(peak, equity)
            cur_dd = max(cur_dd, (peak - equity) / peak * 100)

        n_tr = len(executed)
        wr = (sum(1 for e in executed if e["r"] > 0) / n_tr * 100) if n_tr else 0.0
        pnl = sum(e["pnl"] for e in executed)
        roi = pnl / CAPITAL * 100
        is_pass = (roi >= MIN_ROI) and (cur_dd <= MAX_DD) and (wr >= MIN_WR) and (n_tr >= MIN_TRADES)
        pass_count += int(is_pass)
        status = "PASS" if is_pass else ("FAIL" if n_tr else "CASH")
        total_pnl += pnl
        all_pnl.append(np.array([e["pnl"] for e in executed]))
        print(f"W{w_id:02d} | {w_name[:38]:<38} | {len(test_g):<7d} | {n_tr:<6d} | {wr:>6.1f}%  | {pnl:>+10.2f} USD | {roi:>+7.2f}% | {cur_dd:>5.2f}% | {status:<6}", flush=True)
        results.append({"window_id": w_id, "name": w_name, "candidates": int(len(test_g)),
                        "trades": n_tr, "win_rate": wr, "pnl_usd": pnl, "roi_pct": roi,
                        "max_dd_pct": cur_dd, "status": status, "ok_fams": sorted(ok_fams)})

    print("=" * 128, flush=True)
    print(f"STAGE2-v2 SUMMARY: total PnL {total_pnl:+,.2f} USD ({total_pnl/CAPITAL*100:+.2f}%) | PASS {pass_count}/20 | {time.perf_counter()-t_all:.0f}s", flush=True)

    flat = np.concatenate([p for p in all_pnl if len(p)]) if all_pnl else np.array([])
    mc = block_bootstrap_mc(flat, CAPITAL, horizon_n=25)
    print(f"[MC] monthly-equivalent (25 trades) via block bootstrap: {mc}", flush=True)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"results": results, "total_pnl": total_pnl,
                                    "pass_count": pass_count, "mc": mc}, indent=2))
    print(f"[stage2] wrote {OUT_JSON}", flush=True)
    return results, mc


if __name__ == "__main__":
    run()
