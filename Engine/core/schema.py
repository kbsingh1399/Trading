"""
================================================================================
CANONICAL MARKET DATA SCHEMA & COLUMN SPECIFICATIONS
================================================================================
Single source of truth for the dual-table Parquet contract:

  Table 1  {symbol}_15m_master_2020_2026.parquet   (one row per 15m candle)
  Table 2  {symbol}_15m_footprint_ladder.parquet   (one row per price rung per candle)

Backward compatibility contract
-------------------------------
The first 62 entries of CANONICAL_COLUMNS are byte-for-byte identical (name,
order, dtype) to the legacy schema consumed by quant_strategy_suite.py,
run_expanding_walkforward_ml.py, trend_orderflow_features.py and the live
monitor. New features are only ever APPENDED after ``metrics_available``.
================================================================================
"""

from typing import Dict, List, Tuple

BAR_MS: int = 900_000                      # 15 minutes
DAY_MS: int = 86_400_000
MASTER_FILENAME_TEMPLATE = "{symbol}_15m_master_2020_2026.parquet"
LADDER_FILENAME_TEMPLATE = "{symbol}_15m_footprint_ladder.parquet"
MANIFEST_FILENAME_TEMPLATE = "{symbol}_dataset_manifest.json"

# ------------------------------------------------------------------------------
# Numeric precision policy (decimal places). Prices are stored at Binance's
# maximum tick precision so sub-dollar assets (DOGE, TRX, ADA...) never collapse.
# ------------------------------------------------------------------------------
PRICE_DP: int = 8
COIN_DP: int = 8
USD_DP: int = 2
RATIO_DP: int = 6
PCT_DP: int = 6

LEGACY_COLUMNS: List[str] = [
    # 1. Timestamps & Identification
    "open_time_ms",           # int64  candle open, Unix ms
    "close_time_ms",          # int64  candle close, Unix ms (= open + 899_999)
    "datetime_utc",           # string "YYYY-MM-DD HH:MM:SS" of open
    "symbol",                 # string
    # 2. OHLCV Core
    "open", "high", "low", "close",
    "volume_base",            # float64 base-asset volume
    "volume_quote",           # float64 USDT volume
    "volume_sma9",            # float64 9-bar SMA of quote volume
    "trade_count",            # int64
    # 3. Momentum & Volatility
    "rsi_14", "atr_14", "atr_100",
    # 4. EMAs (seeded from first warm-up bar, 2019/2020 history)
    "ema_8", "ema_21", "ema_50", "ema_200", "ema_800",
    # 5. CVD
    "future_cvd_15m", "future_cvd_session", "future_cvd_lifetime",
    "spot_cvd_15m", "spot_cvd_session", "spot_cvd_lifetime",
    # 6. Rates, basis, open interest
    "funding_rate_pct",       # float64 last settled 8h rate in percent, ffilled
    "basis_usd",              # float64 futures close - spot close
    "open_interest_k",        # float64 OI in thousands of contracts (coins)
    "open_interest_usd",
    "oi_change_pct",          # float64 15m pct change of OI, winsorised +-100
    # 7. Liquidations (signed: long <= 0, short >= 0)
    "long_liq_usd", "short_liq_usd",
    # 8. Positioning
    "ls_ratio_global",        # global account long/short ratio
    "ls_ratio_top",           # top-trader POSITION long/short ratio
    "top_account_ratio",      # top-trader ACCOUNT long/short ratio
    "whale_index",
    "taker_volume_ratio",     # official taker buy/sell volume ratio
    # 9. Footprint & microstructure
    "fp_delta", "fp_poc", "fp_poc_vol_ratio", "fp_stacked_buy_imb", "fp_stacked_sell_imb",
    "session_vah", "session_val", "prev_day_vah", "prev_day_val",
    "taker_buy_count", "taker_sell_count",
    "taker_buy_vol_btc", "taker_sell_vol_btc",
    "max_trade_vol_btc", "avg_trade_size_usd",
    # 10. Depth proxies (positive magnitudes)
    "bid_depth_usd", "ask_depth_usd", "bid_depth_coin", "ask_depth_coin",
    # 11. Provenance
    "future_flow_source",     # TICK_EXACT | KLINE_APPROX
    "spot_flow_source",       # SPOT_EXACT | UNAVAILABLE
    "poc_source",             # TICK_EXACT | OHLC_APPROX
    "is_synthetic",           # int8 1 = bar reconstructed across exchange downtime
    "metrics_available",      # int8 1 = official metrics snapshot <= 6h old at close
]

EXTENDED_COLUMNS: List[str] = [
    "spot_close",             # float64 spot close matched 1:1 (ffilled when UNAVAILABLE)
    "session_vwap",           # float64 volume-weighted average price since 00:00 UTC
    "vwap_zscore",            # float64 (close - vwap) / rolling_std(close - vwap, 24)
    "volume_ratio",           # float64 volume_base / SMA9(volume_base)
    "zc_div",                 # float64 spot_cvd_15m - future_cvd_15m
    "long_liq_zs",            # float64 rolling-96 z-score of |long_liq_usd|
    "short_liq_zs",           # float64 rolling-96 z-score of short_liq_usd
    "liq_imbalance_ratio",    # float64 (short - |long|) / (short + |long|) in [-1, 1]
    "is_imputed_metrics",     # int8 1 = official metrics imputed/unavailable at bar
    "is_warmup_converged",    # int8 1 = indicators converged (>= 3,200 warm-up bars)
]

CANONICAL_COLUMNS: List[str] = LEGACY_COLUMNS + EXTENDED_COLUMNS

COLUMN_DTYPES: Dict[str, str] = {
    "open_time_ms": "int64", "close_time_ms": "int64",
    "datetime_utc": "string", "symbol": "string",
    "future_flow_source": "string", "spot_flow_source": "string", "poc_source": "string",
    "is_synthetic": "int8", "metrics_available": "int8",
    "is_imputed_metrics": "int8", "is_warmup_converged": "int8",
    "trade_count": "int64", "taker_buy_count": "int64", "taker_sell_count": "int64",
}
for _c in CANONICAL_COLUMNS:
    COLUMN_DTYPES.setdefault(_c, "float64")

STRING_VOCAB: Dict[str, Tuple[str, ...]] = {
    "future_flow_source": ("TICK_EXACT", "KLINE_APPROX"),
    "spot_flow_source": ("SPOT_EXACT", "UNAVAILABLE"),
    "poc_source": ("TICK_EXACT", "OHLC_APPROX"),
}

# Columns that are legitimately constant over long stretches (excluded from the
# dead-feature detector in the verification council).
ALLOWED_CONSTANT_COLUMNS: Tuple[str, ...] = (
    "symbol", "is_synthetic", "metrics_available", "is_imputed_metrics", "is_warmup_converged",
    "future_flow_source", "spot_flow_source", "poc_source", "fp_poc_vol_ratio", "fp_stacked_buy_imb",
    "fp_stacked_sell_imb", "max_trade_vol_btc",
)

# ------------------------------------------------------------------------------
# Table 2: footprint ladder
# ------------------------------------------------------------------------------
LADDER_COLUMNS: List[str] = [
    "open_time_ms",      # int64  FK -> Table 1
    "price_bin",         # float64 rung price (bin_idx * bin_step)
    "bid_vol_coin",      # float64 taker-sell volume executed at the rung
    "ask_vol_coin",      # float64 taker-buy volume executed at the rung
    "net_delta_coin",    # float64 ask - bid
    "is_buy_imbalance",  # int8   diagonal ask/bid >= 3:1 vs rung below
    "is_sell_imbalance", # int8   diagonal bid/ask >= 3:1 vs rung above
    "is_poc",            # int8   exactly one per candle
    "trade_count",       # int64
    "rung_source",       # int8   0 = exact aggTrades tick, 1 = causal synthetic
]
LADDER_DTYPES: Dict[str, str] = {
    "open_time_ms": "int64", "price_bin": "float64", "bid_vol_coin": "float64",
    "ask_vol_coin": "float64", "net_delta_coin": "float64", "is_buy_imbalance": "int8",
    "is_sell_imbalance": "int8", "is_poc": "int8", "trade_count": "int64", "rung_source": "int8",
}
RUNG_SOURCE_TICK: int = 0
RUNG_SOURCE_SYNTHETIC: int = 1

# ------------------------------------------------------------------------------
# Universe
# ------------------------------------------------------------------------------
SYMBOLS: List[str] = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT",
    "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT", "AVAXUSDT",
    "SUIUSDT", "NEARUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT",
]

# First trading day of each USDT-M perpetual. Used to bound archive scans and to
# start EMA warm-up as early as history allows.
FUTURES_LISTING_DATES: Dict[str, str] = {
    "BTCUSDT": "2019-09-08", "ETHUSDT": "2019-11-27", "XRPUSDT": "2020-01-06",
    "SOLUSDT": "2020-09-14", "BNBUSDT": "2020-02-10", "DOGEUSDT": "2020-07-10",
    "ADAUSDT": "2020-01-31", "TRXUSDT": "2020-01-15", "LINKUSDT": "2020-01-17",
    "AVAXUSDT": "2020-09-23", "SUIUSDT": "2023-05-03", "NEARUSDT": "2020-10-15",
    "DOTUSDT": "2020-08-18", "LTCUSDT": "2020-01-09", "BCHUSDT": "2020-01-15",
    "APTUSDT": "2022-10-19", "OPUSDT": "2022-06-01", "ARBUSDT": "2023-03-23",
}

DEFAULT_START_DATE: str = "2020-09-01"
WARMUP_START_DATE: str = "2019-09-01"


def master_filename(symbol: str) -> str:
    return MASTER_FILENAME_TEMPLATE.format(symbol=symbol)


def ladder_filename(symbol: str) -> str:
    return LADDER_FILENAME_TEMPLATE.format(symbol=symbol)


def manifest_filename(symbol: str) -> str:
    return MANIFEST_FILENAME_TEMPLATE.format(symbol=symbol)
