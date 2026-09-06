"""
Historical Binance ingestion, feature processing, ladder assembly and Parquet export.
Consolidated under BinanceHistoricalFetcher.
"""

from .binance_historical_fetcher import (
    ArchiveParseError,
    BinanceHistoricalFetcher,
    aggregate_trades_to_ladder,
    assemble_ladder,
    build_ladder_from_trades,
    synthesize_causal_ladder,
)
from .historical_metrics_processor import HistoricalMetricsProcessor
from .http_client import FetchError, HttpClient
from .parquet_exporter import ParquetExporter, SchemaError

__all__ = [
    "ArchiveParseError",
    "BinanceHistoricalFetcher",
    "HistoricalMetricsProcessor",
    "ParquetExporter",
    "SchemaError",
    "HttpClient",
    "FetchError",
    "assemble_ladder",
    "synthesize_causal_ladder",
    "build_ladder_from_trades",
    "aggregate_trades_to_ladder",
]
