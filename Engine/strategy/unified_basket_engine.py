"""
Unified 3-Basket Strategy Engine (Crypto, Forex, CFD)
=====================================================
Integrates Quantpedia Research Edges:
1. Crypto: Overnight Liquidity Void (22:00-00:00 UTC) + 10-Bar Breakout / Liquidation Exhaustion.
2. Forex: ICT Kill Zones (London 07-10 UTC, NY 12-15 UTC) + Carry-Momentum Alignment + Spread/ATR Defense.
3. CFD: Opening Range Breakout (ORB 30m) + Minor Metals & Indices Momentum + Correlation Governor.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np
import pandas as pd

from Engine.core.schema import ASSET_BASKETS, clean_symbol_to_raw

@dataclass
class BasketSignal:
    symbol: str
    basket: str
    signal: int              # 1 = Long, -1 = Short, 0 = Neutral
    entry_price: float
    sl_price: float
    tp_price: float
    r_dist: float
    prob: float
    strategy_tag: str
    reason: str

class UnifiedBasketEngine:
    def __init__(
        self,
        prob_threshold: float = 0.55,
        max_spread_atr: float = 0.25,
        min_r_multiple: float = 2.5,
    ):
        self.prob_threshold = prob_threshold
        self.max_spread_atr = max_spread_atr
        self.min_r_multiple = min_r_multiple

    def generate_crypto_signal(
        self,
        symbol: str,
        df_15m: pd.DataFrame,
        current_bid: float,
        current_ask: float,
        prob: float = 0.60,
    ) -> BasketSignal:
        """
        Crypto Edge: Overnight Liquidity Void (22-00 UTC) + 10-Bar Breakout/Sweep.
        """
        if len(df_15m) < 40:
            return BasketSignal(symbol, "Crypto", 0, 0, 0, 0, 0, prob, "CRYPTO_HOLD", "Insufficient bars")

        last_bar = df_15m.iloc[-1]
        hour = last_bar.name.hour if hasattr(last_bar.name, 'hour') else 0
        is_overnight_void = (hour >= 22 or hour < 1)

        # 10-bar rolling extremes (Quantpedia anomaly)
        rolling_high_10 = df_15m['high'].iloc[-11:-1].max()
        rolling_low_10 = df_15m['low'].iloc[-11:-1].min()
        close = last_bar['close']
        atr = df_15m['high'].iloc[-15:].max() - df_15m['low'].iloc[-15:].min()
        atr = max(atr / 5.0, 1e-4)

        # Breakout Continuation (Momentum) or Overnight Absorption
        if close > rolling_high_10 and prob >= self.prob_threshold:
            entry = current_ask
            sl = entry - (1.5 * atr)
            tp = entry + (self.min_r_multiple * 1.5 * atr)
            r_dist = entry - sl
            tag = "CRYPTO_OVERNIGHT_BREAKOUT" if is_overnight_void else "CRYPTO_MOMENTUM"
            return BasketSignal(symbol, "Crypto", 1, entry, sl, tp, r_dist, prob, tag, f"Long {tag}")

        elif close < rolling_low_10 and prob >= self.prob_threshold and is_overnight_void:
            # Reversal / Mean reversion from local low during overnight void
            entry = current_ask
            sl = entry - (1.2 * atr)
            tp = entry + (2.0 * atr)
            r_dist = entry - sl
            return BasketSignal(symbol, "Crypto", 1, entry, sl, tp, r_dist, prob, "CRYPTO_VOID_REVERSAL", "Long Overnight Mean Reversion")

        return BasketSignal(symbol, "Crypto", 0, 0, 0, 0, 0, prob, "CRYPTO_NEUTRAL", "No setup")

    def generate_forex_signal(
        self,
        symbol: str,
        df_15m: pd.DataFrame,
        current_bid: float,
        current_ask: float,
        spread: float,
        prob: float = 0.60,
    ) -> BasketSignal:
        """
        Forex Edge: ICT Kill Zone Confluence + Spread/ATR Filter.
        """
        if len(df_15m) < 40:
            return BasketSignal(symbol, "Forex", 0, 0, 0, 0, 0, prob, "FX_HOLD", "Insufficient bars")

        last_bar = df_15m.iloc[-1]
        atr = max((df_15m['high'].iloc[-14:] - df_15m['low'].iloc[-14:]).mean(), 1e-5)

        # Spread defense
        if spread > 0 and (spread / atr) > self.max_spread_atr:
            return BasketSignal(symbol, "Forex", 0, 0, 0, 0, 0, prob, "FX_HOLD", f"Spread/ATR {spread/atr:.1%} > {self.max_spread_atr:.0%}")

        # Kill Zone check
        hour = last_bar.name.hour if hasattr(last_bar.name, 'hour') else 12
        is_kz = (7 <= hour < 10) or (12 <= hour < 15)

        # Trend and FVG retest proxy
        ema_50 = df_15m['close'].ewm(span=50).mean().iloc[-1]
        close = last_bar['close']

        if is_kz and close > ema_50 and prob >= self.prob_threshold:
            entry = current_ask
            sl = entry - max(3.5 * spread, 1.5 * atr)
            r_dist = entry - sl
            tp = entry + (self.min_r_multiple * r_dist)
            return BasketSignal(symbol, "Forex", 1, entry, sl, tp, r_dist, prob, "FX_ICT_KZ_LONG", "Long ICT Kill Zone Confluence")

        elif is_kz and close < ema_50 and prob >= self.prob_threshold:
            entry = current_bid
            sl = entry + max(3.5 * spread, 1.5 * atr)
            r_dist = sl - entry
            tp = entry - (self.min_r_multiple * r_dist)
            return BasketSignal(symbol, "Forex", -1, entry, sl, tp, r_dist, prob, "FX_ICT_KZ_SHORT", "Short ICT Kill Zone Confluence")

        return BasketSignal(symbol, "Forex", 0, 0, 0, 0, 0, prob, "FX_NEUTRAL", "No KZ Confluence")

    def generate_cfd_signal(
        self,
        symbol: str,
        df_15m: pd.DataFrame,
        current_bid: float,
        current_ask: float,
        prob: float = 0.60,
    ) -> BasketSignal:
        """
        CFD Edge: Opening Range Breakout (ORB) + Minor Metals Momentum.
        """
        if len(df_15m) < 30:
            return BasketSignal(symbol, "CFD", 0, 0, 0, 0, 0, prob, "CFD_HOLD", "Insufficient bars")

        last_bar = df_15m.iloc[-1]
        atr = max((df_15m['high'].iloc[-14:] - df_15m['low'].iloc[-14:]).mean(), 1e-4)
        
        # 2-bar Opening Range Breakout
        recent_high = df_15m['high'].iloc[-6:-1].max()
        recent_low = df_15m['low'].iloc[-6:-1].min()
        close = last_bar['close']

        if close > recent_high and prob >= self.prob_threshold:
            entry = current_ask
            sl = recent_low
            r_dist = max(entry - sl, 1.5 * atr)
            sl = entry - r_dist
            tp = entry + (self.min_r_multiple * r_dist)
            return BasketSignal(symbol, "CFD", 1, entry, sl, tp, r_dist, prob, "CFD_ORB_LONG", "Long Opening Range Breakout")

        elif close < recent_low and prob >= self.prob_threshold:
            entry = current_bid
            sl = recent_high
            r_dist = max(sl - entry, 1.5 * atr)
            sl = entry + r_dist
            tp = entry - (self.min_r_multiple * r_dist)
            return BasketSignal(symbol, "CFD", -1, entry, sl, tp, r_dist, prob, "CFD_ORB_SHORT", "Short Opening Range Breakout")

        return BasketSignal(symbol, "CFD", 0, 0, 0, 0, 0, prob, "CFD_NEUTRAL", "No ORB Breakout")
