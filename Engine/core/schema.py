"""
================================================================================
CANONICAL MARKET DATA SCHEMA & COLUMN SPECIFICATIONS
================================================================================
Single source of truth for the dual-table Parquet contract:

  Table 1  {symbol}_15m_master_2020_2026.parquet   (one row per 15m candle)
  Table 2  {symbol}_15m_footprint_ladder.parquet   (one row per price rung per candle)

Backward compatibility contract
-------------------------------
The first 56 entries of CANONICAL_COLUMNS are byte-for-byte identical (name,
order, dtype) to the legacy schema consumed by quant_strategy_suite.py,
run_expanding_walkforward_ml.py, trend_orderflow_features.py and the live
monitor. New features are only ever APPENDED after ``is_imputed_metrics``.
================================================================================
"""

from typing import Dict, List, Optional, Tuple

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

# ------------------------------------------------------------------------------
# CVD Lifetime Rounding Contract (R3-C2 Invariant):
# Both future_cvd_15m and spot_cvd_15m are quantized to COIN_DP (8 decimal places)
# per bar. future_cvd_lifetime and spot_cvd_lifetime are defined as the exact
# cumulative sum of these quantized deltas:
#   future_cvd_lifetime[t] = np.round(future_cvd_lifetime[t-1] + future_cvd_15m[t], COIN_DP)
# This mathematical contract applies identically in both full-rebuild and
# incremental-append paths, guaranteeing atol=0.0 bit-parity across all bars.
# ------------------------------------------------------------------------------

CANONICAL_COLUMNS: List[str] = [
    # 1. Timestamps & Identification
    "open_time_ms",           # int64  candle open, Unix ms
    "close_time_ms",          # int64  candle close, Unix ms (= open + 899_999)
    "datetime_utc",           # string "YYYY-MM-DD HH:MM:SS" of open
    "symbol",                 # string
    # 2. OHLCV Core (100% Raw Binance Futures)
    "open", "high", "low", "close",
    "volume_base",            # float64 base-asset volume
    "volume_quote",           # float64 USDT volume
    "volume_sma9",            # float64 9-bar SMA of quote volume
    "trade_count",            # int64
    # 3. Momentum & Volatility (Deterministic Math)
    "rsi_14", "atr_14", "atr_100",
    # 4. EMAs (Mathematical trendlines)
    "ema_8", "ema_21", "ema_50", "ema_200", "ema_800",
    # 5. CVD (100% Real Binance Futures Taker Flow)
    "future_cvd_15m", "future_cvd_session", "future_cvd_lifetime",
    # 6. Spot CVD (100% Real Binance Spot Taker Flow)
    "spot_cvd_15m", "spot_cvd_session", "spot_cvd_lifetime",
    # 7. Funding & Basis
    "funding_rate_pct",       # float64 last settled 8h rate in percent, ffilled
    "basis_usd",              # float64 futures close - spot close
    # 8. Open Interest (100% Real Binance Derivatives Metrics)
    "open_interest_k",        # float64 OI in thousands of contracts (coins)
    "open_interest_usd",
    "oi_change_pct",          # float64 15m pct change of OI
    # 9. Liquidations (Calibrated Institutional Liquidation Model)
    "long_liq_usd", "short_liq_usd",
    # 10. Positioning (100% Real Binance Accounts Metrics)
    "ls_ratio_global",        # global account long/short ratio
    "ls_ratio_top",           # top-trader POSITION long/short ratio
    "top_account_ratio",      # top-trader ACCOUNT long/short ratio
    "whale_index",
    "taker_volume_ratio",     # official taker buy/sell volume ratio
    # 11. Session Value Area (Mathematical Volume Profiling)
    "session_vah", "session_val", "prev_day_vah", "prev_day_val",
    # 12. Trade Execution & Sizing (100% Real Binance Trades)
    "taker_buy_count", "taker_sell_count",
    "taker_buy_vol_btc", "taker_sell_vol_btc",
    "avg_trade_size_usd",
    # 13. Spot Ground Truth & Extended Features
    "spot_close",             # float64 spot close matched 1:1 from Binance Spot
    "session_vwap",           # float64 volume-weighted average price since 00:00 UTC
    "vwap_zscore",            # float64 (close - vwap) / rolling_std(close - vwap, 24)
    "volume_ratio",           # float64 volume_base / SMA9(volume_base)
    "zc_div",                 # float64 spot_cvd_15m - future_cvd_15m
    "long_liq_zs",            # float64 rolling-96 z-score of |long_liq_usd|
    "short_liq_zs",           # float64 rolling-96 z-score of short_liq_usd
    "liq_imbalance_ratio",    # float64 (short - |long|) / (short + |long|) in [-1, 1]
    "is_imputed_metrics",     # int8 1 = ex-post data-quality quarantine (official metrics missing/frozen/imputed, e.g. 2022 API outage or Binance reporting halt). RETROSPECTIVE ONLY: not for contemporaneous live signals.
    # 15. Index Price (100% Real Binance Vision indexPriceKlines — multi-exchange composite)
    "index_close",            # float64 Binance index price 15m close; 0.0 if no archive exists for this asset/bar
    "basis_index_bps",        # float64 (futures_close - index_close) / index_close * 10^4 in basis points; 0.0 when index_close unavailable
]

# Backward compatibility aliases
LEGACY_COLUMNS: List[str] = CANONICAL_COLUMNS
EXTENDED_COLUMNS: List[str] = []

COLUMN_DTYPES: Dict[str, str] = {
    "open_time_ms": "int64", "close_time_ms": "int64",
    "datetime_utc": "string", "symbol": "string",
    "is_imputed_metrics": "int8",
    "trade_count": "int64", "taker_buy_count": "int64", "taker_sell_count": "int64",
}
for _c in CANONICAL_COLUMNS:
    COLUMN_DTYPES.setdefault(_c, "float64")

STRING_VOCAB: Dict[str, Tuple[str, ...]] = {}

# Columns that are legitimately constant over long stretches
ALLOWED_CONSTANT_COLUMNS: Tuple[str, ...] = (
    "symbol", "is_imputed_metrics",
)

# ------------------------------------------------------------------------------
# Fixed Institutional Price Merge Levels (Deterministic Order Flow Geometry)
# ------------------------------------------------------------------------------
FIXED_MERGE_STEPS: Dict[str, float] = {
    "BTCUSDT": 50.0,        # Standard Exocharts / Sierra Chart $50 bucket
    "ETHUSDT": 2.0,         # Standard Exocharts / Sierra Chart $2 bucket
    "SOLUSDT": 0.20,        # Sub-dollar microstructure (20 cents)
    "BNBUSDT": 1.00,        # Dollar bucket
    "DOGEUSDT": 0.0010,     # 10-pip bucket
    "XRPUSDT": 0.0020,      # 20-pip bucket
    "ADAUSDT": 0.0010,      # 10-pip bucket
    "TRXUSDT": 0.0002,      # 2-pip bucket
    "LINKUSDT": 0.04,       # 4-cent bucket
    "AVAXUSDT": 0.10,       # 10-cent bucket
    "SUIUSDT": 0.010,       # 1-cent bucket
    "NEARUSDT": 0.02,       # 2-cent bucket
    "DOTUSDT": 0.02,        # 2-cent bucket
    "LTCUSDT": 0.20,        # 20-cent bucket
    "BCHUSDT": 1.00,        # Dollar bucket
    "APTUSDT": 0.02,        # 2-cent bucket
    "OPUSDT": 0.010,        # 1-cent bucket
    "ARBUSDT": 0.004,       # 4-tenth cent bucket
}

# ------------------------------------------------------------------------------
# Table 2: 100% Real Empirical Footprint Ladder (13 Columns)
# ------------------------------------------------------------------------------
LADDER_COLUMNS: List[str] = [
    "open_time_ms",        # int64  FK -> Table 1 15m candle timestamp
    "price_bin",           # float64 fixed price rung (e.g. 65000.0, 65025.0)
    "bid_vol_coin",        # float64 aggressive sell volume into bid
    "ask_vol_coin",        # float64 aggressive buy volume into ask
    "net_delta_coin",      # float64 ask_vol - bid_vol
    "total_vol_coin",      # float64 ask_vol + bid_vol
    "trade_count",         # int64  trade count executed at this rung
    "is_poc",              # int8   1 if Point of Control of this 15m candle, else 0
    "is_buy_imbalance",    # int8   1 if diagonal buy imbalance >= 3:1 with notional floor
    "is_sell_imbalance",   # int8   1 if diagonal sell imbalance >= 3:1 with notional floor
    "is_stacked_buy_imb",  # int8   1 if part of >= 3 stacked buy imbalance cluster
    "is_stacked_sell_imb", # int8   1 if part of >= 3 stacked sell imbalance cluster
    "is_value_area",       # int8   1 if within 70% Value Area (VAH to VAL)
]
LADDER_DTYPES: Dict[str, str] = {
    "open_time_ms": "int64", "price_bin": "float64", "bid_vol_coin": "float64",
    "ask_vol_coin": "float64", "net_delta_coin": "float64", "total_vol_coin": "float64",
    "trade_count": "int64", "is_poc": "int8", "is_buy_imbalance": "int8",
    "is_sell_imbalance": "int8", "is_stacked_buy_imb": "int8", "is_stacked_sell_imb": "int8",
    "is_value_area": "int8",
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

# ------------------------------------------------------------------------------
# NOTE (audit Ox_Alpha_43, finding B3): a 27-symbol ASSET_BASKETS definition used
# to live here and was silently shadowed by the canonical 156-asset definition
# further down this file. Python kept the later binding, so the small universe
# was unreachable dead config that would have flipped behaviour on any reorder.
# The duplicate has been removed; ASSET_BASKETS is now defined exactly once, in
# section 16 below. Do not reintroduce a second binding.
# ------------------------------------------------------------------------------


def clean_broker_symbol(raw_symbol: str) -> str:
    """
    Map broker raw symbols (e.g. BTCUSD.pi, EURUSD.p, GER40.m) to canonical symbols.
    """
    if not raw_symbol:
        return ""
    clean = raw_symbol.split(".")[0]
    if clean.endswith("_i"):
        clean = clean[:-2]
    return clean.upper()


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


# ------------------------------------------------------------------------------
# 16. Unified Asset Baskets (Crypto, Forex, CFD) & MT5 Broker Mapping
# ------------------------------------------------------------------------------
ASSET_BASKETS: Dict[str, List[str]] = {
    "Crypto": [
        "BTCUSD", "DOTUSD", "ETHUSD", "LTCUSD", "XRPUSD", "ADAUSD", "BCHUSD", "LNKUSD",
        "XLMUSD", "AVXUSD", "DOGUSD", "FILUSD", "GRTUSD", "NERUSD", "SOLUSD", "TRXUSD",
        "UNIUSD", "VETUSD", "XMRUSD", "BNBUSD", "AVEUSD", "ALGUSD", "ATMUSD", "AXSUSD",
        "CHZUSD", "COMUSD", "EGLUSD", "FLWUSD", "IOTUSD", "KSMUSD", "NEOUSD", "XSIUSD",
        "THTUSD", "XTZUSD", "ZECUSD", "MANUSD", "INCUSD", "ARWUSD", "BATUSD", "CELUSD",
        "CHRUSD", "CRVUSD", "ENJUSD", "BARUSD", "LRCUSD", "KAVUSD", "KNCUSD", "ONTUSD",
        "QTMUSD", "SNDUSD", "SKLUSD", "SNXUSD", "STOUSD", "SXPUSD", "YFIUSD", "ZILUSD",
        "ZRXUSD", "DSHUSD"
    ],
    "Forex": [
        "AUDCAD", "AUDCHF", "AUDJPY", "AUDUSD", "CADCHF", "CADJPY", "CHFJPY", "EURAUD",
        "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF",
        "GBPJPY", "GBPUSD", "USDCAD", "USDCHF", "USDJPY", "AUDCNH", "AUDNZD", "AUDSGD",
        "CHFSGD", "CNHJPY", "EURCNH", "EURHKD", "EURHUF", "EURMXN", "EURNOK", "EURNZD",
        "EURSEK", "EURSGD", "EURZAR", "GBPCNH", "GBPHKD", "GBPNOK", "GBPNZD", "GBPSEK",
        "GBPSGD", "NOKJPY", "NOKSEK", "NZDCAD", "NZDCHF", "NZDCNH", "NZDJPY", "NZDSGD",
        "NZDUSD", "SGDJPY", "USDCNH", "USDHKD", "USDHUF", "USDMXN", "USDNOK", "USDSEK",
        "USDSGD", "USDTHB", "USDZAR", "ZARJPY"
    ],
    "CFD": [
        "AU200", "DJ30", "FR40", "GER30", "JP225", "NAS100", "SP500", "STOXX50",
        "UK100", "CHINA50", "CHINAH", "HK50", "NETH25", "SWISS20", "US2000", "GER40",
        "XAGAUD", "XAGEUR", "XAGSGD", "XAGUSD", "XAUAUD", "XAUCNH", "XAUEUR", "XAUGBP",
        "XAUSGD", "XAUUSD", "XPDUSD", "XPTUSD", "GAUCNH", "GAUUSD", "ALUMINIUM", "COPPER",
        "GAS", "LEAD", "NICKEL", "ZINC", "UKBRENT", "USWTI"
    ],
}

# Supported MT5 broker suffixes (e.g. .pi for Forex, .p for CFD/Crypto)
BROKER_SUFFIXES: Tuple[str, ...] = (".pi", ".p", ".r", ".m", ".raw", "")

# Raw symbol alias translations (e.g. sunsetted / renamed instruments)
RAW_SYMBOL_ALIASES: Dict[str, str] = {
    "GER30": "GER40",
    "GER30.p": "GER40.p",
    "US30": "DJ30",
    "US30.p": "DJ30.p",
    "NAS100": "NAS100.p",
    "SPX500": "SP500",
}

# Binance USDT-M to MT5 clean symbol cross-mapping
BINANCE_TO_MT5_MAP: Dict[str, str] = {
    "BTCUSDT": "BTCUSD",
    "ETHUSDT": "ETHUSD",
    "SOLUSDT": "SOLUSD",
    "XRPUSDT": "XRPUSD",
    "BNBUSDT": "BNBUSD",
    "LTCUSDT": "LTCUSD",
    "ADAUSDT": "ADAUSD",
    "DOTUSDT": "DOTUSD",
    "BCHUSDT": "BCHUSD",
    # Audit Ox_Alpha_43 finding B4: these five previously mapped to invented
    # tickers (DOGEUSD, LINKUSD, AVAXUSD, NEARUSD) that appear nowhere in
    # ASSET_BASKETS["Crypto"], so the Binance history on disk could never be
    # joined to the MT5 basket. Corrected to the actual Blueberry MT5 symbols.
    "DOGEUSDT": "DOGUSD",
    "TRXUSDT": "TRXUSD",
    "LINKUSDT": "LNKUSD",
    "AVAXUSDT": "AVXUSD",
    "NEARUSDT": "NERUSD",
    # No MT5 counterpart in the 156-asset Blueberry universe. Kept out of the
    # map deliberately rather than mapped to a symbol the broker does not list:
    #   SUIUSDT, APTUSDT, OPUSDT, ARBUSDT
}

MT5_TO_BINANCE_MAP: Dict[str, str] = {v: k for k, v in BINANCE_TO_MT5_MAP.items()}

# Default broker raw symbol convention per basket
DEFAULT_BROKER_RAW_SYMBOLS: Dict[str, str] = {
    # Crypto (typically .p or raw on MT5)
    "BTCUSD": "BTCUSD.p", "ETHUSD": "ETHUSD.p", "SOLUSD": "SOLUSD.p",
    "XRPUSD": "XRPUSD.p", "BNBUSD": "BNBUSD.p", "LTCUSD": "LTCUSD.p",
    "ADAUSD": "ADAUSD.p", "DOTUSD": "DOTUSD.p", "BCHUSD": "BCHUSD.p",
    # Forex (typically .pi on institutional MT5)
    "EURUSD": "EURUSD.pi", "NZDUSD": "NZDUSD.pi", "AUDCHF": "AUDCHF.pi",
    "EURHUF": "EURHUF.pi", "USDSEK": "USDSEK.pi", "EURSEK": "EURSEK.pi",
    "USDHKD": "USDHKD.pi", "EURCNH": "EURCNH.pi", "NZDCNH": "NZDCNH.pi",
    # CFD (typically .p on MT5)
    "GER40": "GER40.p", "AU200": "AU200.p", "FR40": "FR40.p",
    "US2000": "US2000.p", "GAS": "GAS.p", "NICKEL": "NICKEL.p",
    "LEAD": "LEAD.p", "XAUCNH": "XAUCNH.p", "GAUCNH": "GAUCNH.p",
}


def raw_symbol_to_clean(raw_symbol: str) -> str:
    """
    Converts a broker raw symbol (e.g. 'EURUSD.pi', 'GER40.p', 'GER30', 'BTCUSD.p')
    into its clean canonical symbol (e.g. 'EURUSD', 'GER40', 'BTCUSD').
    """
    sym = raw_symbol.strip()
    if sym in RAW_SYMBOL_ALIASES:
        sym = RAW_SYMBOL_ALIASES[sym]

    upper_sym = sym.upper()
    for suffix in [".PI", ".P", ".R", ".M", ".RAW"]:
        if upper_sym.endswith(suffix):
            sym = sym[:-len(suffix)]
            break

    if sym in RAW_SYMBOL_ALIASES:
        sym = RAW_SYMBOL_ALIASES[sym]

    return sym


def clean_symbol_to_raw(clean_symbol: str, broker_suffix: str = "") -> str:
    """
    Converts a clean canonical symbol to its broker raw symbol with suffix.
    If broker_suffix is omitted or empty, uses the default from DEFAULT_BROKER_RAW_SYMBOLS.
    """
    sym = clean_symbol.strip()
    if broker_suffix:
        return f"{sym}{broker_suffix}"
    return DEFAULT_BROKER_RAW_SYMBOLS.get(sym, sym)


def get_basket_for_symbol(symbol: str) -> Optional[str]:
    """
    Returns the basket name ('Crypto', 'Forex', 'CFD') for a given clean or raw symbol.
    """
    clean = raw_symbol_to_clean(symbol)
    for basket_name, assets in ASSET_BASKETS.items():
        if clean in assets:
            return basket_name
    return None

