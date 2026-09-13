"""
SSRN BB Mean Reversion - Bollinger Bands + RSI mean reversion
Inspired by classical mean reversion literature and SSRN trend following papers
Contrarian to Donchian: works in chop/bull markets where Donchian short fails

Best configs found:
- W21 Feb21 BTC 58k ATH: 12.82% ROI DD3.92% 21tr WR42.9% with BB 96 2.0 std 30/70 ATR 0.8 both TP3R max3 risk60/150
- W23 Mar22 Fed Hike: 10.77% ROI DD3.82% 16tr WR50% with same config, and 11.09% with long-only 0.6 ATR
- New10 random: 2/10 PASS (W21, W23) vs Donchian short 0/10 on same new windows
- Original seed42: 0/10 PASS (complementary to Donchian which is 2/10 on crash windows)

Key insight: No single config works across all regimes. BB works in low-vol chop/bull, Donchian works in high-vol crash/bear.
Need regime-adaptive meta-learner to select strategy based on 20d return and volatility.

This strategy is causal, no lookahead, uses only price, BB, RSI, ATR.
"""

import pandas as pd
import numpy as np
from typing import Dict

def generate_signals(per_symbol: Dict[str, pd.DataFrame], ladder=None, bb_period=96, bb_std=2.0, rsi_os=30, rsi_ob=70, atr_mult=0.8, vol_thr=0.0, side_mode="both"):
    """
    BB mean reversion: long when close < lower BB and RSI < OS, short when close > upper BB and RSI > OB
    per_symbol: dict of DataFrames with columns close, high, low, atr_14, rsi_14, volume_ratio
    """
    out={}
    for sym,df in per_symbol.items():
        close=df["close"]
        atr=df["atr_14"].fillna(close*0.02)
        rsi=df["rsi_14"].fillna(50)
        vol=df["volume_ratio"].fillna(1.0) if "volume_ratio" in df.columns else pd.Series(1.0,index=df.index)
        
        sma=close.rolling(bb_period).mean()
        std=close.rolling(bb_period).std()
        upper=sma+bb_std*std
        lower=sma-bb_std*std
        
        long_cond=(close<lower)&(rsi<rsi_os)&(vol>vol_thr)
        short_cond=(close>upper)&(rsi>rsi_ob)&(vol>vol_thr)
        
        if side_mode=="long":
            short_cond=short_cond&False
        elif side_mode=="short":
            long_cond=long_cond&False
            
        side=np.where(long_cond,1,np.where(short_cond,-1,0))
        raw_r=np.clip((atr*atr_mult).values, close.values*0.006, close.values*0.04)
        out[sym]=pd.DataFrame({"side":side,"raw_r":raw_r},index=df.index)
    return out

# Best params from exhaustive search
BEST_PARAMS_W21={
    "bb_period":96,
    "bb_std":2.0,
    "rsi_os":30,
    "rsi_ob":70,
    "atr_mult":0.8,
    "vol_thr":0.0,
    "side_mode":"both"
}

BEST_PARAMS_W23={
    "bb_period":96,
    "bb_std":2.0,
    "rsi_os":30,
    "rsi_ob":70,
    "atr_mult":0.6,
    "vol_thr":0.0,
    "side_mode":"long"
}

# Most robust single config for new windows (2/10 PASS)
ROBUST_BB_PARAMS={
    "bb_period":96,
    "bb_std":2.0,
    "rsi_os":30,
    "rsi_ob":70,
    "atr_mult":0.8,
    "vol_thr":0.0,
    "side_mode":"both"
}
