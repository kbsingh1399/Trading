"""Meta-labelling gate for the levels / POC lab (Lopez de Prado, 2018).

The geometric families generate far more candidates than the portfolio can (or
should) trade.  This module learns, from *pre-window* events only, the
probability that a candidate reaches a profitable exit under the certified
execution geometry (target ``target_r`` net R, structural stop, 41 bps friction),
then lets the portfolio trade only the highest-ranked candidates.

Training hygiene
----------------
* features are computed at the signal candle only;
* labels come from the same triple-barrier geometry the kernel executes;
* for window *w* the model sees only events with ``signal_time < start - 72h``;
* the probability threshold is calibrated on the *training* set's quantiles so the
  expected candidate count per month is an input, not a fitted free parameter.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .signals import FRICTION_FLOOR, FamilySpec, build_signal_frame, naked_poc_series
from .studies import batch_outcomes

FEATURE_COLUMNS = [
    # level geometry
    "d_pwh", "d_pwl", "d_pmh", "d_pml", "d_ath", "d_pdh", "d_pdl", "d_pqh", "d_pql",
    "bars_since_ath",
    # value / POC geometry
    "d_dev_poc", "d_dev_vah", "d_dev_val", "d_dev_lvn", "d_prior_poc", "d_prior_vah",
    "d_prior_val", "d_prior_poc_low", "d_prior_poc_high", "z_dev_poc", "dev_share", "poc_delta",
    # regime / flow
    "atr_ratio", "volume_rel", "atr_z", "rsi_14", "flow4", "flow_ratio",
    "trend_up", "trend_dn", "slope200", "slope200_4h", "ret_96", "ret_672", "rv_24h",
    "d_sess_vwap", "d_week_open", "d_month_open", "taker_volume_ratio",
    # positioning / derivatives flow (funding, basis, liquidations, OI, spot-vs-perp CVD)
    "funding_z", "funding_8", "basis_rel", "liq_net", "liq_intensity", "liq_cum8",
    "oi_rel", "oi_roc96", "zc_div_z", "avg_trade_rel", "taker_ratio_c",
    # CUSUM structural-move event features (see cusum.py)
    "cs_up_age", "cs_dn_age", "cs_dir", "cs_pressure",
    # order flow from the shipped footprint ladder (candle-level, causal)
    "ld_delta_rel", "ld_cvd_4", "ld_cvd_8", "ld_cvd_32", "ld_delta_z",
    "ld_imb_net", "ld_imb_net_8", "ld_stack_net", "ld_d_poc", "ld_d_vah", "ld_d_val",
    "ld_va_width", "ld_va_pos", "ld_bins_rel", "ld_rel_vol",
    "ld_delta_hi_rel", "ld_delta_lo_rel", "ld_delta_skew", "ld_poc_range_pos",
    "ld_buyimb_hi_frac",
    # macro (BTC) context + universe volatility state
    "btc_tide", "btc_ret_96", "btc_atr_z", "mkt_atr_pct_z",
    # event meta
    "side", "stop_rel", "sleeve", "hour",
]


def event_table(f: pd.DataFrame, specs: list[FamilySpec], btc: pd.DataFrame,
                target_r: float = 4.0, horizon: int = 288, priority=None,
                pending: int = 0, pending_step: int = 4) -> pd.DataFrame:
    """Resolved candidate events for one symbol, with features + realised net R."""
    from .signals import build_signal_frame

    t = f.open_time_ms.to_numpy(np.int64)
    day = t // 86_400_000
    naked = naked_poc_series(day, f.sess_poc.to_numpy(float), f.low.to_numpy(float),
                             f.high.to_numpy(float), f.close.to_numpy(float))
    sig = build_signal_frame(f, specs, naked=naked, priority=priority,
                             pending=pending, pending_step=pending_step)
    idx = np.flatnonzero(sig.signal.to_numpy() != 0)
    if len(idx) == 0:
        return pd.DataFrame()
    o = f.open.to_numpy(float)
    h = f.high.to_numpy(float)
    lo = f.low.to_numpy(float)
    c = f.close.to_numpy(float)
    side = sig.signal.to_numpy()[idx]
    dist = sig.stop_distance.to_numpy()[idx]
    idx = idx[idx + 1 < len(c)]
    side = side[: len(idx)]
    dist = dist[: len(idx)]
    if len(idx) == 0:
        return pd.DataFrame()
    r = batch_outcomes(o, h, lo, c, idx, side, dist, target_r, horizon)
    row = f.iloc[idx]
    out = pd.DataFrame({col: row[col].to_numpy() for col in FEATURE_COLUMNS if col in row})
    for col in FEATURE_COLUMNS:
        if col not in out:
            out[col] = 0.0
    out["side"] = side
    out["stop_rel"] = dist / c[idx]
    out["sleeve"] = sig.sleeve.to_numpy()[idx]
    out["hour"] = ((t[idx] % 86_400_000) // 3_600_000).astype(np.int64)
    out["family"] = sig.family.to_numpy()[idx]
    out["open_time_ms"] = t[idx]
    out["t"] = t[idx]
    out["symbol"] = f.symbol.iloc[0]
    out["net_r"] = r
    out["label"] = (r > 0).astype(np.int8)
    btc_ctx = btc.set_index("open_time_ms")
    out["btc_ret_96"] = btc_ctx.ret_96.reindex(t[idx]).to_numpy(float)
    out["btc_atr_z"] = btc_ctx.atr_z.reindex(t[idx]).to_numpy(float)
    out["btc_tide"] = np.where(
        btc_ctx.close.reindex(t[idx]).to_numpy(float) > btc_ctx.e200_4h.reindex(t[idx]).to_numpy(float),
        1.0, -1.0)
    return out


class ProbEnsemble:
    """Average predicted probabilities of several learners.

    Every member is a classifier whose output is already on the probability scale,
    so a plain average is a scale-consistent combination (no rank normalisation
    needed) and keeps ``GateModel.predict`` unchanged.  The members are deliberately
    different in inductive bias: a deep gradient-boosted tree ensemble (interactions,
    monotone splits), a randomised tree ensemble (variance reduction on noisy tails)
    and a small multi-layer perceptron (smooth, high-order interactions over
    standardised features).  The literature that motivated this -- SSRN 5209907
    (Donchian breakouts with ATR sizing), SSRN 4824172 (intraday momentum with
    dynamic exits) and the ML meta-labelling line of Lopez de Prado -- all report
    that ensembling and label design matter more than the individual learner.
    """

    def __init__(self, models, scaler=None, needs_scale=None, names=None, imputer=None):
        self.models = models
        self.scaler = scaler
        self.needs_scale = needs_scale or [False] * len(models)
        self.names = names or [f"m{i}" for i in range(len(models))]
        self.imputer = imputer

    def predict_proba(self, X):
        Z = X.to_numpy(np.float32) if hasattr(X, "to_numpy") else np.asarray(X, np.float32)
        if self.imputer is not None:
            Z = self.imputer.transform(Z).astype(np.float32)
        cols = []
        for m, scale in zip(self.models, self.needs_scale):
            z = self.scaler.transform(Z) if scale else Z
            cols.append(m.predict_proba(z)[:, 1])
        p = np.mean(cols, axis=0)
        return np.column_stack([1.0 - p, p])

    def predict(self, X):
        return self.predict_proba(X)[:, 1]


def _fit_ensemble(train: pd.DataFrame, feats: list[str], y: np.ndarray,
                  params: dict, seed: int, max_mlp_rows: int = 120_000) -> ProbEnsemble:
    """LightGBM (deep) + ExtraTrees + histogram GBM + a small MLP, probability-averaged."""
    import lightgbm as lgb
    from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler

    X = train[feats].to_numpy(np.float32)
    # Shared imputation: ExtraTrees and the MLP reject NaN, and a single imputed
    # matrix keeps every member looking at the same data.
    imputer = SimpleImputer(strategy="median").fit(X)
    X = imputer.transform(X).astype(np.float32)
    models, scales, names = [], [], []

    gbm = lgb.LGBMClassifier(**(params | dict(max_depth=7, num_leaves=95,
                                              min_child_samples=80, n_estimators=500)))
    gbm.fit(X, y)
    models.append(gbm); scales.append(False); names.append("lgb-deep")

    et = ExtraTreesClassifier(n_estimators=250, max_depth=14, min_samples_leaf=40,
                              max_features="sqrt", n_jobs=2, random_state=seed)
    et.fit(X, y)
    models.append(et); scales.append(False); names.append("extratrees")

    hgb = HistGradientBoostingClassifier(max_depth=6, learning_rate=0.05, max_iter=250,
                                         min_samples_leaf=60, l2_regularization=1.0,
                                         random_state=seed)
    hgb.fit(X, y)
    models.append(hgb); scales.append(False); names.append("histgbm")

    # The neural member: standardise, cap the sample for runtime, early stopping.
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))[: min(len(X), max_mlp_rows)]
    scaler = StandardScaler().fit(X[idx])
    mlp = MLPClassifier(hidden_layer_sizes=(64, 32), alpha=1e-3, batch_size=4096,
                        learning_rate_init=2e-3, max_iter=30, early_stopping=True,
                        n_iter_no_change=5, validation_fraction=0.12,
                        random_state=seed)
    mlp.fit(scaler.transform(X[idx]), y[idx])
    models.append(mlp); scales.append(True); names.append("mlp")
    return ProbEnsemble(models=models, scaler=scaler, needs_scale=scales, names=names,
                        imputer=imputer)


@dataclass
class GateModel:
    booster: object
    threshold: float
    features: list[str]
    mode: str = "clf"          # "clf" = P(net_r > label_r); "reg" = E[net_r]
    label_r: float = 0.0

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        z = X[self.features].to_numpy(np.float32)
        if self.mode == "reg":
            return np.asarray(self.booster.predict(z), float)
        return self.booster.predict_proba(z)[:, 1]


def train_gate(events: pd.DataFrame, target_cands_per_month: float = 25.0,
               min_prob: float = 0.30, seed: int = 42,
               label_r: float | None = None, regressor: bool = False,
               kind: str = "lgb") -> GateModel:
    """Fit a LightGBM model on historical events and calibrate a threshold.

    ``label_r=None`` reproduces the original direction label (``net_r > 0``).
    ``label_r=r`` fits ``P(net_r > r)``, i.e. the probability of a *meaningful*
    win rather than a scratch win -- under a 4R-target/time-stop geometry the
    direction label is dominated by tiny time-stop scratches, which is why the
    selected set can show a 58 % hit rate and still lose money.
    ``regressor=True`` fits ``E[net_r]`` directly and ranks on expected R.
    """
    import lightgbm as lgb

    train = events.dropna(subset=["label"]).copy()
    feats = [c for c in FEATURE_COLUMNS if c in train.columns]
    X = train[feats].to_numpy(np.float32)
    params = dict(n_estimators=350, learning_rate=0.03, max_depth=4, num_leaves=31,
                  min_child_samples=200, subsample=0.8, colsample_bytree=0.7,
                  reg_alpha=1.0, reg_lambda=1.0, random_state=seed, n_jobs=2, verbose=-1)
    if regressor:
        y = train["net_r"].to_numpy(np.float32)
        if label_r is not None:   # asymmetric: penalise the stop-outs harder
            y = np.where(y < -1.0, -label_r, y)
        model = lgb.LGBMRegressor(**params)
        model.fit(X, y)
    else:
        y = (train["net_r"].to_numpy(np.float32) > (0.0 if label_r is None else label_r))
        y = y.astype(np.int8)
        if kind == "lgb":
            model = lgb.LGBMClassifier(**params)
            model.fit(X, y)
        elif kind == "deep":
            model = lgb.LGBMClassifier(**(params | dict(max_depth=7, num_leaves=95,
                                                        min_child_samples=80,
                                                        n_estimators=500)))
            model.fit(X, y)
        elif kind == "ens":
            model = _fit_ensemble(train, feats, y, params, seed)
        else:
            raise ValueError(f"unknown gate kind: {kind}")
    p = (np.asarray(model.predict(X), float) if regressor
         else model.predict_proba(X)[:, 1])
    months = max(1.0, (train.t.max() - train.t.min()) / (30.4 * 86_400_000))
    rate = len(train) / months
    q = 1.0 - min(0.98, max(0.02, target_cands_per_month / max(rate, 1e-9)))
    thr = float(np.quantile(p, q))
    if not regressor:
        thr = max(thr, min_prob)
    return GateModel(booster=model, threshold=thr, features=feats,
                     mode="reg" if regressor else "clf",
                     label_r=0.0 if label_r is None else float(label_r))


def apply_gate(signals: pd.DataFrame, events: pd.DataFrame, gate: GateModel,
               per_bar: bool = True) -> pd.DataFrame:
    """Keep only gated candidates and use the model probability as the ranking score."""
    out = signals.copy()
    keep = pd.Series(False, index=out.index)
    prob = pd.Series(0.0, index=out.index)
    if len(events):
        p = gate.predict(events)
        ev = events.assign(prob=p)
        ev = ev[ev.prob >= gate.threshold]
        sel = ev.set_index(["symbol", "open_time_ms"])["prob"]
        key = pd.MultiIndex.from_arrays([out.get("symbol", pd.Series("", index=out.index)), out.open_time_ms])
        prob = pd.Series(sel.reindex(key).to_numpy(float), index=out.index).fillna(0.0)
        keep = prob > 0
    out.loc[~keep, "signal"] = 0
    out.loc[~keep, "stop_distance"] = np.nan
    out["score"] = out["score"] * 0.0 + prob
    return out
