"""
Canonical Correlation Cluster Registry (single source of truth)
===============================================================

Audit Ox_Alpha_43, finding B11: correlation clusters were declared independently
in three places with divergent membership --

    Engine/forex_engine.py:157
    Engine/live/order_manager.py:20
    Engine/research/signal_auction.py:77

`signal_auction` carried a materially broader set than the other two, and
`CRYPTO_BLOC` -- named in the production directive -- existed in none of them.
No copy was imported by the backtest, so cluster governance was claimed but
never exercised in any reported result.

This module is now the one definition. It covers the full 156-asset universe
declared in Engine/core/schema.py, including the crypto basket.

Governance rule: at most one concurrent open position per cluster. Symbols that
belong to no cluster are treated as their own singleton cluster (they can only
collide with themselves).
"""

from typing import Dict, List, Optional, Set

from Engine.core.schema import ASSET_BASKETS, raw_symbol_to_clean

CORRELATION_CLUSTERS: Dict[str, Set[str]] = {
    "EUR_BLOC": {
        "EURUSD", "EURSEK", "EURCNH", "EURHUF", "EURAUD", "EURCAD", "EURCHF",
        "EURGBP", "EURJPY", "EURNZD", "EURSGD", "EURMXN", "EURNOK", "EURHKD",
        "EURZAR",
    },
    "USD_BLOC": {
        "NZDUSD", "AUDUSD", "GBPUSD", "USDCAD", "USDJPY", "USDCHF", "USDSGD",
        "USDCNH", "USDSEK", "USDHKD", "USDMXN", "USDNOK", "USDZAR", "USDHUF",
        "USDTHB",
    },
    "JPY_BLOC": {
        "AUDJPY", "CADJPY", "CHFJPY", "GBPJPY", "NZDJPY", "SGDJPY", "ZARJPY",
        "NOKJPY", "CNHJPY",
    },
    "CHF_BLOC": {"AUDCHF", "CADCHF", "GBPCHF", "NZDCHF", "CHFSGD"},
    "CNH_BLOC": {"NZDCNH", "XAUCNH", "GAUCNH", "AUDCNH", "GBPCNH"},
    "AUD_BLOC": {"AUDNZD", "AUDSGD", "AUDCAD"},
    "NZD_BLOC": {"NZDCAD", "NZDSGD"},
    "GBP_BLOC": {
        "GBPNZD", "GBPAUD", "GBPCAD", "GBPSGD", "GBPNOK", "GBPSEK", "GBPHKD",
        "GBPCNH",
    },
    "SCANDI_BLOC": {"NOKSEK", "GBPSEK", "EURNOK"},
    "INDEX_BLOC": {
        "GER40", "GER30", "FR40", "AU200", "US2000", "DJ30", "SP500", "NAS100",
        "CHINA50", "CHINAH", "UK100", "JP225", "STOXX50", "HK50", "NETH25",
        "SWISS20",
    },
    "PRECIOUS_BLOC": {
        "XAUUSD", "XAUAUD", "XAUEUR", "XAUGBP", "XAUSGD", "XAGUSD", "XAGAUD",
        "XAGEUR", "XAGSGD", "XPDUSD", "XPTUSD", "GAUUSD",
    },
    "COMMODITY_BLOC": {
        "GAS", "NICKEL", "LEAD", "COPPER", "ALUMINIUM", "ZINC", "UKBRENT",
        "USWTI",
    },
    "CRYPTO_BLOC": set(ASSET_BASKETS["Crypto"]),
}

_SYMBOL_TO_CLUSTER: Dict[str, str] = {}
for _cluster, _members in CORRELATION_CLUSTERS.items():
    for _sym in _members:
        _SYMBOL_TO_CLUSTER.setdefault(_sym, _cluster)


def get_cluster(symbol: str) -> str:
    """
    Return the correlation cluster for a symbol (clean or broker-raw form).

    Symbols with no declared cluster get a singleton cluster keyed on the symbol
    itself, so the one-position-per-cluster rule degrades to one-per-symbol
    rather than silently allowing unlimited correlated exposure.
    """
    clean = raw_symbol_to_clean(symbol)
    return _SYMBOL_TO_CLUSTER.get(clean, f"SINGLETON::{clean}")


def same_cluster(symbol_a: str, symbol_b: str) -> bool:
    """True when two symbols share a correlation cluster."""
    return get_cluster(symbol_a) == get_cluster(symbol_b)


def uncovered_symbols() -> List[str]:
    """
    Universe symbols that fall through to a singleton cluster. Useful as a
    coverage assertion in tests -- a growing list means new instruments were
    added to schema.py without cluster governance.
    """
    out: List[str] = []
    for basket_symbols in ASSET_BASKETS.values():
        for sym in basket_symbols:
            if sym not in _SYMBOL_TO_CLUSTER:
                out.append(sym)
    return sorted(out)
