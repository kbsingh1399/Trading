"""
Unit and Integration Tests: Baskets, Asset Selector & MT5 Crypto Data Integrity
================================================================================
Verifies:
1. Parquet integrity for exported MT5 crypto assets in Forex_Backtesting_Data/
   - Columns, types, monotonicity, non-empty, no nulls.
2. ASSET_BASKETS structure and schema compliance in Engine/core/schema.py
   - Dict structure, required baskets (Crypto, Forex, CFD), symbol formatting,
     no duplicates, and broker symbol resolution (clean_broker_symbol).
3. Engine/core/asset_selector.py dynamic ranking, selection, edge case handling
   - Empty basket, invalid basket, top_n > basket size, top_n <= 0,
     metric-based ranking, fallback behavior, active multiverse universe.
"""

import os
from pathlib import Path
from typing import List, Dict
import pytest
import polars as pl
import pandas as pd
import numpy as np

from Engine.core.schema import (
    ASSET_BASKETS,
    BROKER_SUFFIXES,
    clean_broker_symbol,
)
from Engine.core.asset_selector import (
    AssetSelector,
    get_top_assets,
    get_active_multiverse_universe,
)

FOREX_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "Forex_Backtesting_Data"

# Expected schema for MT5 real parquet files
EXPECTED_COLUMNS = [
    "time",
    "datetime",
    "open",
    "high",
    "low",
    "close",
    "tick_volume",
    "spread",
    "real_volume",
    "day_of_week",
    "session",
    "is_kill_zone",
]

EXPECTED_BASKETS = ["Crypto", "Forex", "CFD"]

EXPECTED_CRYPTO_SYMBOLS = [
    "BTCUSD", "ETHUSD", "SOLUSD", "XRPUSD", "BNBUSD",
    "LTCUSD", "ADAUSD", "DOTUSD", "BCHUSD"
]

EXPECTED_FOREX_SYMBOLS = [
    "EURUSD", "NZDUSD", "AUDCHF", "EURHUF", "USDSEK",
    "EURSEK", "USDHKD", "EURCNH", "NZDCNH"
]

EXPECTED_CFD_SYMBOLS = [
    "GER40", "AU200", "FR40", "US2000", "GAS",
    "NICKEL", "LEAD", "XAUCNH", "GAUCNH"
]


# ==============================================================================
# 1. ASSET_BASKETS & Schema Compliance Tests
# ==============================================================================

class TestAssetBasketsSchema:
    """Verifies ASSET_BASKETS definition and broker symbol normalization."""

    def test_baskets_dict_structure(self):
        """ASSET_BASKETS must be a dict containing Crypto, Forex, and CFD."""
        assert isinstance(ASSET_BASKETS, dict)
        for basket_name in EXPECTED_BASKETS:
            assert basket_name in ASSET_BASKETS, f"Missing basket: {basket_name}"
            assert isinstance(ASSET_BASKETS[basket_name], list)
            assert len(ASSET_BASKETS[basket_name]) > 0, f"Basket {basket_name} is empty"

    def test_crypto_basket_symbols(self):
        """Crypto basket must contain all target perpetual/CFD pairs."""
        crypto_symbols = ASSET_BASKETS["Crypto"]
        for expected in EXPECTED_CRYPTO_SYMBOLS:
            assert expected in crypto_symbols, f"Expected {expected} in Crypto basket"
        assert len(crypto_symbols) >= len(EXPECTED_CRYPTO_SYMBOLS)

    def test_forex_basket_symbols(self):
        """Forex basket must match institutional specification."""
        forex_symbols = ASSET_BASKETS["Forex"]
        for expected in EXPECTED_FOREX_SYMBOLS:
            assert expected in forex_symbols, f"Expected {expected} in Forex basket"
        assert len(forex_symbols) >= len(EXPECTED_FOREX_SYMBOLS)

    def test_cfd_basket_symbols(self):
        """CFD basket must match institutional specification."""
        cfd_symbols = ASSET_BASKETS["CFD"]
        for expected in EXPECTED_CFD_SYMBOLS:
            assert expected in cfd_symbols, f"Expected {expected} in CFD basket"
        assert len(cfd_symbols) >= len(EXPECTED_CFD_SYMBOLS)

    def test_no_duplicate_symbols_in_baskets(self):
        """No basket may contain duplicate symbols."""
        for name, symbols in ASSET_BASKETS.items():
            assert len(symbols) == len(set(symbols)), f"Duplicate symbols in basket {name}"

    @pytest.mark.parametrize("raw,expected", [
        ("BTCUSD.pi", "BTCUSD"),
        ("ETHUSD.p", "ETHUSD"),
        ("SOLUSD.m", "SOLUSD"),
        ("XRPUSD_i", "XRPUSD"),
        ("EURUSD.p", "EURUSD"),
        ("GER40.m", "GER40"),
        ("BTCUSD", "BTCUSD"),
        ("", ""),
    ])
    def test_clean_broker_symbol(self, raw, expected):
        """clean_broker_symbol strips broker-specific raw suffixes."""
        assert clean_broker_symbol(raw) == expected


# ==============================================================================
# 2. AssetSelector Dynamic Ranking & Edge Case Tests
# ==============================================================================

class TestAssetSelector:
    """Verifies dynamic ranking, selection, and edge case handling."""

    def test_default_initialization(self):
        """AssetSelector initializes with default ASSET_BASKETS."""
        selector = AssetSelector()
        assert selector.baskets == ASSET_BASKETS
        assert selector.metrics_path.name == "oos_20_windows_forex_results.csv"

    def test_get_top_assets_valid_basket(self):
        """get_top_assets returns requested number of assets from basket."""
        selector = AssetSelector()
        top_3 = selector.get_top_assets("Crypto", top_n=3)
        assert len(top_3) == 3
        for sym in top_3:
            assert sym in ASSET_BASKETS["Crypto"]

    def test_edge_case_empty_basket(self):
        """Empty basket returns empty list without error."""
        custom_selector = AssetSelector(baskets={"EmptyBasket": []})
        result = custom_selector.get_top_assets("EmptyBasket", top_n=5)
        assert result == []

    def test_edge_case_invalid_basket_raises(self):
        """Querying an invalid basket raises ValueError."""
        selector = AssetSelector()
        with pytest.raises(ValueError, match="Invalid basket name"):
            selector.get_top_assets("NonExistentBasket", top_n=3)

    def test_edge_case_top_n_greater_than_basket_size(self):
        """top_n > basket size returns all assets in the basket without error."""
        selector = AssetSelector()
        basket_len = len(ASSET_BASKETS["Crypto"])
        result = selector.get_top_assets("Crypto", top_n=100)
        assert len(result) == basket_len
        assert set(result) == set(ASSET_BASKETS["Crypto"])

    def test_edge_case_top_n_zero_or_negative(self):
        """top_n <= 0 returns empty list."""
        selector = AssetSelector()
        assert selector.get_top_assets("Crypto", top_n=0) == []
        assert selector.get_top_assets("Crypto", top_n=-5) == []

    def test_dynamic_ranking_with_custom_metrics(self):
        """Assets with superior metrics rank higher than underperforming ones."""
        # Synthetic metrics where SOLUSD and ETHUSD outperform BTCUSD
        metrics = pd.DataFrame([
            {"Symbol": "BTCUSD", "WinRate%": 40.0, "Net_ROI%": 5.0, "MaxDD%": 4.0, "Calmar": 1.25},
            {"Symbol": "ETHUSD", "WinRate%": 60.0, "Net_ROI%": 25.0, "MaxDD%": 2.5, "Calmar": 10.0},
            {"Symbol": "SOLUSD", "WinRate%": 75.0, "Net_ROI%": 45.0, "MaxDD%": 2.0, "Calmar": 22.5},
            {"Symbol": "XRPUSD", "WinRate%": 30.0, "Net_ROI%": -2.0, "MaxDD%": 6.0, "Calmar": -0.33},
        ])
        selector = AssetSelector()
        ranked = selector.rank_basket("Crypto", metrics_df=metrics)
        # SOLUSD should rank 1st, ETHUSD 2nd, BTCUSD 3rd
        assert ranked[0] == "SOLUSD"
        assert ranked[1] == "ETHUSD"
        assert ranked[2] == "BTCUSD"

    def test_fallback_when_metrics_missing(self):
        """Missing or None metrics gracefully fall back to canonical basket order."""
        selector = AssetSelector()
        empty_df = pd.DataFrame()
        result = selector.rank_basket("Crypto", metrics_df=empty_df, top_n=3)
        assert result == ASSET_BASKETS["Crypto"][:3]

    def test_active_multiverse_universe(self):
        """get_active_multiverse_universe aggregates top assets across all baskets."""
        selector = AssetSelector()
        top_2_all = selector.get_active_multiverse_universe(top_n_per_basket=2)
        # 3 baskets x 2 assets = 6 total assets
        assert len(top_2_all) == 6
        assert len(set(top_2_all)) == 6  # All distinct

    def test_module_convenience_functions(self):
        """Module-level get_top_assets and get_active_multiverse_universe work."""
        top_crypto = get_top_assets("Crypto", top_n=2)
        assert len(top_crypto) == 2
        universe = get_active_multiverse_universe(top_n_per_basket=1)
        assert len(universe) == 3


# ==============================================================================
# 3. Parquet Data Integrity Tests (Forex_Backtesting_Data)
# ==============================================================================

class TestParquetDataIntegrity:
    """Verifies MT5 exported parquet files conform to institutional standards."""

    def _validate_parquet_frame(self, df: pl.DataFrame, file_path: Path):
        """Helper to enforce strict Parquet schema & data integrity invariants."""
        # 1. Non-empty
        assert len(df) > 0, f"{file_path.name} is empty"

        # 2. Required columns present
        for col in EXPECTED_COLUMNS:
            assert col in df.columns, f"Missing column {col} in {file_path.name}"

        # 3. Monotonic timestamps
        time_series = df["time"].to_numpy()
        is_strictly_monotonic = np.all(np.diff(time_series) > 0)
        assert is_strictly_monotonic, f"Timestamps in {file_path.name} are not strictly monotonic"

        # 4. Zero nulls in core pricing & timestamp fields
        core_cols = ["time", "datetime", "open", "high", "low", "close"]
        for col in core_cols:
            null_count = df[col].null_count()
            assert null_count == 0, f"Column {col} has {null_count} nulls in {file_path.name}"

        # 5. Price sanity: high >= low, high >= open, high >= close
        highs = df["high"].to_numpy()
        lows = df["low"].to_numpy()
        opens = df["open"].to_numpy()
        closes = df["close"].to_numpy()
        assert np.all(highs >= lows), f"high < low found in {file_path.name}"
        assert np.all(highs >= opens), f"high < open found in {file_path.name}"
        assert np.all(highs >= closes), f"high < close found in {file_path.name}"
        assert np.all(lows <= opens), f"low > open found in {file_path.name}"
        assert np.all(lows <= closes), f"low > close found in {file_path.name}"

        # 6. Session categorization sanity (case-insensitive & handles unclassified/closed bars)
        sessions = set(df["session"].unique().to_list())
        normalized_sessions = {
            s.lower().replace(" ", "_") if s is not None else "off_hours"
            for s in sessions
        }
        valid_sessions = {"asian", "london", "new_york", "london_close", "close", "off_hours", "off"}
        assert normalized_sessions.issubset(valid_sessions), f"Invalid sessions {sessions} in {file_path.name}"

        # 7. Kill zone is boolean or integer binary (0/1)
        assert df["is_kill_zone"].dtype in (pl.Boolean, pl.Int32, pl.Int8, pl.UInt8, pl.Int64), f"is_kill_zone not Boolean/Int in {file_path.name}"

    def test_schema_contract_with_synthetic_crypto_fixture(self, tmp_path):
        """
        Validates that the export schema specification correctly passes
        the strict validation pipeline using a synthetic crypto bar sequence.
        """
        n_bars = 100
        start_ts = 1700000000
        times = [start_ts + i * 900 for i in range(n_bars)]
        opens = [50000.0 + i * 10 for i in range(n_bars)]
        highs = [p + 50.0 for p in opens]
        lows = [p - 50.0 for p in opens]
        closes = [p + 5.0 for p in opens]

        fixture_df = pl.DataFrame({
            "time": times,
            "datetime": pl.from_epoch(pl.Series("time", times), time_unit="s").dt.replace_time_zone("UTC"),
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "tick_volume": [100 + i for i in range(n_bars)],
            "spread": [2] * n_bars,
            "real_volume": [50 + i for i in range(n_bars)],
            "day_of_week": [i % 7 for i in range(n_bars)],
            "session": ["london"] * n_bars,
            "is_kill_zone": [True] * n_bars,
        })

        test_file = tmp_path / "BTCUSD_15m_real.parquet"
        fixture_df.write_parquet(test_file, compression="zstd")

        read_df = pl.read_parquet(test_file)
        self._validate_parquet_frame(read_df, test_file)

    def test_existing_forex_cfd_parquet_integrity(self):
        """
        Verifies existing Forex and CFD parquet files in Forex_Backtesting_Data/
        strictly comply with the Parquet contract.
        """
        assert FOREX_DATA_DIR.exists(), f"Forex_Backtesting_Data dir does not exist: {FOREX_DATA_DIR}"
        sample_symbols = ["EURUSD", "GER40", "US2000", "GAS"]
        checked = 0
        for sym in sample_symbols:
            p = FOREX_DATA_DIR / f"{sym}_15m_real.parquet"
            if p.exists():
                df = pl.read_parquet(p)
                self._validate_parquet_frame(df, p)
                checked += 1
        assert checked > 0, "No sample parquet files found in Forex_Backtesting_Data"

    def test_exported_mt5_crypto_parquet_integrity(self):
        """
        Verifies all exported MT5 crypto parquet files in Forex_Backtesting_Data/.
        If MT5 export has completed for any crypto pairs, validates them;
        otherwise reports status cleanly.
        """
        crypto_files = list(FOREX_DATA_DIR.glob("*USD_*_real.parquet"))
        crypto_symbols_found = set()

        for f in crypto_files:
            sym = f.name.split("_")[0]
            if sym in EXPECTED_CRYPTO_SYMBOLS:
                crypto_symbols_found.add(sym)
                df = pl.read_parquet(f)
                self._validate_parquet_frame(df, f)

        if not crypto_symbols_found:
            pytest.skip("MT5 crypto parquet files not yet exported to Forex_Backtesting_Data (pending MT5 export)")
        else:
            assert len(crypto_symbols_found) > 0
