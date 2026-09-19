"""
Dynamic Asset Selector & Multi-Basket Ranking Engine
=====================================================
Selects top-performing assets within decoupled institutional baskets (Crypto, Forex, CFD)
based on rolling performance metrics (Win Rate, Calmar, Net R / ROI, Drawdown).

Edge Cases Handled:
- Empty basket -> returns []
- Invalid basket name -> raises ValueError
- top_n <= 0 -> returns []
- top_n > basket size -> returns all assets in the basket
- Missing or None metrics -> graceful fallback to canonical basket order
"""

from typing import Dict, List, Optional, Union
from pathlib import Path
import pandas as pd
import numpy as np

from Engine.core.schema import ASSET_BASKETS

DEFAULT_METRICS_PATH = Path(__file__).resolve().parent.parent / "research" / "oos_20_windows_forex_results.csv"


class AssetSelector:
    """
    Dynamic ranking and asset selection for multi-basket multiverse trading.
    """

    def __init__(
        self,
        baskets: Optional[Dict[str, List[str]]] = None,
        metrics_path: Optional[Union[str, Path]] = None,
    ):
        self.baskets: Dict[str, List[str]] = baskets if baskets is not None else ASSET_BASKETS
        self.metrics_path: Path = Path(metrics_path) if metrics_path else DEFAULT_METRICS_PATH

    def load_metrics(self, path: Optional[Union[str, Path]] = None) -> Optional[pd.DataFrame]:
        """Load recent performance metrics CSV if available."""
        target_path = Path(path) if path else self.metrics_path
        if target_path.exists():
            try:
                return pd.read_csv(target_path)
            except Exception:
                return None
        return None

    def rank_basket(
        self,
        basket_name: str,
        top_n: Optional[int] = None,
        metrics_df: Optional[pd.DataFrame] = None,
    ) -> List[str]:
        """
        Rank assets within a specified basket and return the top_n assets.

        Parameters
        ----------
        basket_name : str
            Name of the basket (e.g. 'Crypto', 'Forex', 'CFD').
        top_n : Optional[int]
            Number of top assets to return. If None, returns all ranked assets.
        metrics_df : Optional[pd.DataFrame]
            DataFrame containing performance metrics. If None, attempts to load from metrics_path.

        Returns
        -------
        List[str]
            List of selected asset symbols in ranked order.

        Raises
        ------
        ValueError
            If basket_name is not in baskets.
        """
        if basket_name not in self.baskets:
            raise ValueError(
                f"Invalid basket name '{basket_name}'. Available baskets: {list(self.baskets.keys())}"
            )

        basket_assets = self.baskets[basket_name]
        if not basket_assets:
            return []

        if top_n is not None and top_n <= 0:
            return []

        # If no metrics provided, attempt to load
        if metrics_df is None:
            metrics_df = self.load_metrics()

        # If metrics are still missing or empty, fall back to default order
        if metrics_df is None or metrics_df.empty:
            return list(basket_assets[:top_n]) if top_n is not None else list(basket_assets)

        # Check if symbol/asset column exists in metrics_df
        symbol_col = None
        for col in ["Symbol", "symbol", "Asset", "asset"]:
            if col in metrics_df.columns:
                symbol_col = col
                break

        if symbol_col is None:
            # Metrics dataframe does not have per-asset breakdown; fallback to basket order
            return list(basket_assets[:top_n]) if top_n is not None else list(basket_assets)

        # Compute ranking score per symbol
        scores: Dict[str, float] = {}
        for asset in basket_assets:
            asset_rows = metrics_df[metrics_df[symbol_col] == asset]
            if asset_rows.empty:
                # Default neutral score for assets without recorded trades
                scores[asset] = -1e9
                continue

            # Composite metric: Calmar * (WinRate / 100) or Net_R / MaxDD
            calmar = asset_rows["Calmar"].mean() if "Calmar" in asset_rows.columns else 0.0
            win_rate = asset_rows["WinRate%"].mean() if "WinRate%" in asset_rows.columns else 50.0
            net_roi = asset_rows["Net_ROI%"].mean() if "Net_ROI%" in asset_rows.columns else 0.0
            max_dd = asset_rows["MaxDD%"].mean() if "MaxDD%" in asset_rows.columns else 5.0

            # Composite score favoring high win rate, high ROI, low DD
            score = (win_rate / 100.0) * net_roi / (max_dd + 1e-4) + calmar
            scores[asset] = score

        # Sort assets descending by score; preserve original order for ties
        ranked = sorted(basket_assets, key=lambda a: scores.get(a, -1e9), reverse=True)

        if top_n is not None:
            return ranked[:top_n]
        return ranked

    def get_top_assets(
        self,
        basket_name: str,
        top_n: int = 3,
        metrics_df: Optional[pd.DataFrame] = None,
    ) -> List[str]:
        """Convenience method to retrieve top_n assets from a basket."""
        return self.rank_basket(basket_name=basket_name, top_n=top_n, metrics_df=metrics_df)

    def get_active_multiverse_universe(
        self,
        top_n_per_basket: int = 3,
        metrics_df: Optional[pd.DataFrame] = None,
    ) -> List[str]:
        """
        Retrieve combined top assets across all active baskets.

        Returns
        -------
        List[str]
            Unified list of top assets across Crypto, Forex, and CFD baskets.
        """
        active_universe: List[str] = []
        for basket_name in self.baskets:
            top_assets = self.get_top_assets(
                basket_name=basket_name,
                top_n=top_n_per_basket,
                metrics_df=metrics_df,
            )
            active_universe.extend(top_assets)
        return active_universe


# Module-level convenience functions
_default_selector = AssetSelector()


def get_top_assets(
    basket_name: str,
    top_n: int = 3,
    metrics_df: Optional[pd.DataFrame] = None,
) -> List[str]:
    """Get top N assets from the specified basket."""
    return _default_selector.get_top_assets(basket_name, top_n, metrics_df)


def get_active_multiverse_universe(
    top_n_per_basket: int = 3,
    metrics_df: Optional[pd.DataFrame] = None,
) -> List[str]:
    """Get combined top assets across all baskets."""
    return _default_selector.get_active_multiverse_universe(top_n_per_basket, metrics_df)
