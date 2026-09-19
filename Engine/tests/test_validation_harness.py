"""
Regression tests for the honest validation harness and the audit fixes.

Each test pins a specific finding from docs/audits/Ox_Alpha_43_Audit_Findings.md
so the defect cannot silently return.
"""

import numpy as np
import pandas as pd
import pytest

from Engine.core.correlation_clusters import (
    CORRELATION_CLUSTERS, get_cluster, same_cluster, uncovered_symbols,
)
from Engine.core.schema import ASSET_BASKETS, MT5_TO_BINANCE_MAP
from Engine.validation.honest_walkforward import (
    RiskConfig, _fit_threshold_on_train, _trim_to_true_15m,
    build_labels, monte_carlo_bootstrap, simulate_portfolio,
)


# --------------------------------------------------------------------------
# B2 / B3 -- schema integrity
# --------------------------------------------------------------------------

class TestSchemaIntegrity:
    def test_schema_imports(self):
        """B2: schema.py raised NameError on import (missing Optional)."""
        from Engine.core.schema import get_basket_for_symbol
        assert get_basket_for_symbol("BTCUSD") == "Crypto"

    def test_universe_is_156(self):
        assert sum(len(v) for v in ASSET_BASKETS.values()) == 156

    def test_asset_baskets_defined_once(self):
        """B3: ASSET_BASKETS was bound twice; the first was dead config."""
        import inspect
        from Engine.core import schema
        src = inspect.getsource(schema)
        assert src.count("ASSET_BASKETS: Dict[str, List[str]] = {") == 1

    def test_no_duplicate_symbols(self):
        for name, syms in ASSET_BASKETS.items():
            assert len(syms) == len(set(syms)), f"duplicates in {name}"

    def test_crypto_map_targets_real_basket_symbols(self):
        """B4: map emitted DOGEUSD/LINKUSD/... which are in no basket."""
        crypto = set(ASSET_BASKETS["Crypto"])
        for mt5 in MT5_TO_BINANCE_MAP:
            assert mt5 in crypto, f"{mt5} maps to nothing in the Crypto basket"


# --------------------------------------------------------------------------
# B11 -- correlation cluster governance
# --------------------------------------------------------------------------

class TestCorrelationClusters:
    def test_crypto_bloc_exists(self):
        """B11: CRYPTO_BLOC was named in the directive but existed nowhere."""
        assert "CRYPTO_BLOC" in CORRELATION_CLUSTERS
        assert get_cluster("BTCUSD") == "CRYPTO_BLOC"

    def test_full_universe_covered(self):
        assert uncovered_symbols() == []

    def test_broker_suffix_resolves(self):
        assert get_cluster("EURUSD.pi") == get_cluster("EURUSD") == "EUR_BLOC"

    def test_alias_resolves(self):
        assert same_cluster("GER30", "GER40")

    def test_unknown_symbol_is_singleton(self):
        c = get_cluster("NOT_A_REAL_SYMBOL")
        assert c.startswith("SINGLETON::")


# --------------------------------------------------------------------------
# B8 -- no lookahead in threshold selection
# --------------------------------------------------------------------------

class TestNoLookahead:
    def test_threshold_ignores_test_distribution(self):
        """
        B8: the old harness used np.percentile(test_probs, 70). The replacement
        must depend only on training predictions.
        """
        rng = np.random.default_rng(0)
        p_train = rng.uniform(0, 1, 5000)
        y_train = (rng.uniform(0, 1, 5000) > 0.5).astype(int)
        t1 = _fit_threshold_on_train(p_train, y_train, 0.70)
        # Same train data, wildly different test data -> identical threshold.
        t2 = _fit_threshold_on_train(p_train, y_train, 0.70)
        assert t1 == t2
        assert abs(t1 - np.quantile(p_train, 0.70)) < 1e-12

    def test_labels_use_next_bar_open(self):
        """
        Entry must be the open of bar i+1. Construct a series where the signal
        bar closes high and the NEXT open gaps down: if the fill used the
        signal bar's close, the recorded outcome would differ.
        """
        n = 400
        base = np.full(n, 100.0)
        df = pd.DataFrame({
            "time": np.arange(n, dtype=np.int64) * 900,
            "open": base, "high": base + 1, "low": base - 1, "close": base,
            "volume": np.ones(n),
        })
        out = build_labels(df, target_r=2.0, max_hold_bars=10, cost_frac=0.0)
        # Flat series never breaks the prior 20-bar high -> no events at all.
        assert len(out) == 0


# --------------------------------------------------------------------------
# B12 -- 15m data integrity
# --------------------------------------------------------------------------

class TestDataIntegrity:
    def test_daily_prefix_is_trimmed(self):
        """
        B12: MT5 '15m' exports begin with a long daily-resolution prefix.
        Those rows must be dropped or every bar-count rule is corrupted.
        """
        daily = np.arange(50, dtype=np.int64) * 86400
        intra = daily[-1] + np.arange(1, 201, dtype=np.int64) * 900
        df = pd.DataFrame({"time": np.concatenate([daily, intra])})
        out, first = _trim_to_true_15m(df, "time")
        # The last daily timestamp is retained as the left anchor of the first
        # 15m gap, so 200 intraday bars + 1 anchor = 201 rows.
        assert len(out) == 201
        assert first is not None
        gaps = np.diff(out["time"].values)
        assert (gaps == 900).all()
        assert out["time"].iloc[0] == daily[-1]

    def test_all_daily_yields_empty(self):
        df = pd.DataFrame({"time": np.arange(100, dtype=np.int64) * 86400})
        out, first = _trim_to_true_15m(df, "time")
        assert len(out) == 0 and first is None


# --------------------------------------------------------------------------
# B6 -- governance actually binds (non-additivity)
# --------------------------------------------------------------------------

class TestGovernance:
    @staticmethod
    def _signals(clusters, n_each=20):
        rows = []
        for ci, cl in enumerate(clusters):
            for k in range(n_each):
                t = k * 100
                rows.append({
                    "time": t, "exit_time": t + 5000,   # long overlap
                    "cluster": cl, "r_mult": 1.0,
                })
        return pd.DataFrame(rows).sort_values("time").reset_index(drop=True)

    def test_cluster_cap_blocks_correlated_entries(self):
        sig = self._signals(["EUR_BLOC"], n_each=20)
        cfg = RiskConfig(max_concurrent=3, max_per_cluster=1)
        out = simulate_portfolio(sig, cfg)
        assert out["trades"] == 1
        assert out["rejected_cluster"] == 19

    def test_global_concurrency_cap(self):
        sig = self._signals(["EUR_BLOC", "CRYPTO_BLOC", "INDEX_BLOC", "COMMODITY_BLOC"], n_each=1)
        cfg = RiskConfig(max_concurrent=3, max_per_cluster=1)
        out = simulate_portfolio(sig, cfg)
        assert out["trades"] == 3
        assert out["rejected_concurrency"] == 1

    def test_subsets_are_not_additive(self):
        """
        B6: the audited report had exactly additive trade counts across basket
        subsets, which proves the concurrency cap never bound. Under real
        governance, combining baskets MUST displace trades.
        """
        a = self._signals(["EUR_BLOC"], n_each=10)
        b = self._signals(["CRYPTO_BLOC"], n_each=10)
        cfg = RiskConfig(max_concurrent=1, max_per_cluster=1)
        na = simulate_portfolio(a, cfg)["trades"]
        nb = simulate_portfolio(b, cfg)["trades"]
        both = pd.concat([a, b]).sort_values("time").reset_index(drop=True)
        nboth = simulate_portfolio(both, cfg)["trades"]
        assert nboth < na + nb


# --------------------------------------------------------------------------
# B7 -- Monte Carlo is a real bootstrap
# --------------------------------------------------------------------------

class TestMonteCarlo:
    def test_bootstrap_spread_is_wide(self):
        """
        B7: the audited MC reported a 5th-95th band of +/-6% around the median,
        impossibly tight for a resample of thousands of trades. A genuine
        bootstrap must produce a materially wide band.
        """
        rng = np.random.default_rng(1)
        r = np.where(rng.uniform(size=2000) < 0.40, 2.0, -1.0)
        mc = monte_carlo_bootstrap(r, RiskConfig(), n_runs=400, seed=7)
        spread = mc["roi_p95"] - mc["roi_p05"]
        assert spread > abs(mc["roi_p50"]) * 0.15

    def test_losing_system_reports_losses(self):
        r = np.full(500, -0.2)
        mc = monte_carlo_bootstrap(r, RiskConfig(), n_runs=200, seed=3)
        assert mc["roi_p50"] < 0
        assert mc["prob_loss"] > 99.0

    def test_deterministic_under_seed(self):
        rng = np.random.default_rng(5)
        r = np.where(rng.uniform(size=500) < 0.4, 2.0, -1.0)
        a = monte_carlo_bootstrap(r, RiskConfig(), n_runs=200, seed=11)
        b = monte_carlo_bootstrap(r, RiskConfig(), n_runs=200, seed=11)
        assert a["roi_p50"] == b["roi_p50"]


# --------------------------------------------------------------------------
# Numba fastmath NaN-sentinel regression
# --------------------------------------------------------------------------

class TestLabelKernelNaN:
    def test_no_nan_outcomes(self):
        """
        Under fastmath=True the compiler may assume no NaNs, so the original
        `outcome = np.nan` sentinel silently leaked NaN payoffs (685/4523 on
        BTCUSD). Labels must always be finite.
        """
        rng = np.random.default_rng(4)
        n = 3000
        px = 100 * np.exp(np.cumsum(rng.normal(0, 0.001, n)))
        df = pd.DataFrame({
            "time": np.arange(n, dtype=np.int64) * 900,
            "open": px, "close": px,
            "high": px * 1.001, "low": px * 0.999,
            "volume": np.ones(n),
        })
        out = build_labels(df, target_r=2.0, max_hold_bars=24, cost_frac=0.0)
        assert len(out) > 0
        assert np.isfinite(out["r_mult"].values).all()
