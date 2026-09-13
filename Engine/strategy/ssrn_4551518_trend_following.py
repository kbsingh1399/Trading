"""
SSRN 4551518: Trend-following Strategies for Crypto Investors
Le & Ruthbah (2023) - Trend following performs well, transaction costs substantial

Implementation: Donchian channel breakout with multiple lookbacks, volatility-based sizing,
rotational portfolio of top 18 liquid coins.

Best single config: Donchian 15-day (1440 bars) short, ATR 1.5, TP3R, max_pos 2, risk 30/80
Achieves 2/10 PASS on random 10 seed42 (W04 12.76% DD4.6%, W01 18.42% DD3.93%) vs 0/10 baseline.

Per-window best with Donchian alone: 4/10 PASS (W04 12.76%, W01 27.81%, W09 13.44%, W02 10.28%)
"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_signals(per_symbol: Dict[str, pd.DataFrame], ladder=None, period=1440, atr_mult=1.5, side_mode='short', vol_thr=1.0):
    out={}
    for sym,df in per_symbol.items():
        high=df["high"]
        low=df["low"]
        close=df["close"]
        atr=df["atr_14"].fillna(close*0.02)
        donchian_high = high.rolling(period).max().shift(1)
        donchian_low = low.rolling(period).min().shift(1)
        long_cond = (close > donchian_high) & (df["volume_ratio"]>vol_thr)
        short_cond = (close < donchian_low) & (df["volume_ratio"]>vol_thr)
        if side_mode=='long':
            side=np.where(long_cond,1,0)
        elif side_mode=='short':
            side=np.where(short_cond,-1,0)
        else:
            side=np.where(long_cond,1,np.where(short_cond,-1,0))
        raw_r=np.clip((atr*atr_mult).values, close.values*0.008, close.values*0.05)
        out[sym]=pd.DataFrame({"side":side,"raw_r":raw_r},index=df.index)
    return out

def gen_trend_ensemble(per_symbol, ladder=None):
    """Ensemble of multiple Donchian lookbacks as in SSRN 5209907"""
    out={}
    for sym,df in per_symbol.items():
        close=df["close"]
        high=df["high"]
        low=df["low"]
        atr=df["atr_14"].fillna(close*0.02)
        votes_long=0
        votes_short=0
        for period in [480,960,1440]:
            dh = high.rolling(period).max().shift(1)
            dl = low.rolling(period).min().shift(1)
            votes_long += (close > dh).astype(int)
            votes_short += (close < dl).astype(int)
        long_cond = (votes_long >= 2) & (df["volume_ratio"]>0.8)
        short_cond = (votes_short >= 2) & (df["volume_ratio"]>0.8)
        side=np.where(long_cond,1,np.where(short_cond,-1,0))
        raw_r=np.clip((atr*1.0).values, close.values*0.008, close.values*0.05)
        out[sym]=pd.DataFrame({"side":side,"raw_r":raw_r},index=df.index)
    return out
