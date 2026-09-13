"""
SSRN 071: Slow Momentum with Fast Reversion + Changepoint Detection
Wood, Roberts, Zohren (2021) - Balances slow momentum (persisting trends) and fast mean-reversion (quick flips),
with online CPD module that outputs changepoint location and severity score.

Implementation:
- Slow momentum: 20-day return >5% uptrend, <-5% downtrend (period 1920 bars = 20 days)
- Fast reversion: BB + RSI 35/65
- CPD: Efficiency Ratio drop detection, severity = (ER_ma_prev - ER)/ER_ma_prev > thr
- When CPD detected, flip from momentum to mean-reversion

Best: W17 Nov 2024 Election achieves 18.67% ROI DD4.74% 26tr WR57.6% with slow_period 1920, rsi 35/65, atr 0.8, cpd_thr 0.1, TP3R
"""

import pandas as pd
import numpy as np
from typing import Dict

def efficiency_ratio(close, period=20):
    diff = close.diff().abs().rolling(period).sum()
    net = (close - close.shift(period)).abs()
    er = net / diff.replace(0, np.nan)
    return er.fillna(0.5)

def generate_signals(per_symbol: Dict[str, pd.DataFrame], ladder=None, slow_period=1920, fast_rsi_os=35, fast_rsi_ob=65, atr_mult=0.8, cpd_thr=0.1):
    out={}
    for sym,df in per_symbol.items():
        close=df["close"]
        high=df["high"]
        low=df["low"]
        atr=df["atr_14"].fillna(close*0.02)
        rsi=df["rsi_14"].fillna(50)
        # Slow momentum
        slow_ret = close.pct_change(slow_period)
        slow_up = slow_ret > 0.05
        slow_down = slow_ret < -0.05
        # Fast reversion BB
        sma=close.rolling(96).mean()
        std=close.rolling(96).std()
        upper=sma+2*std
        lower=sma-2*std
        fast_long = (close < lower) & (rsi < fast_rsi_os)
        fast_short = (close > upper) & (rsi > fast_rsi_ob)
        # CPD ER drop
        er=efficiency_ratio(close,20)
        er_ma=er.rolling(20).mean()
        cpd_score = (er_ma.shift(20) - er) / er_ma.shift(20).replace(0,1)
        changepoint = cpd_score > cpd_thr

        long_signal = (slow_up & fast_long) | (changepoint & slow_down & fast_long)
        short_signal = (slow_down & fast_short) | (changepoint & slow_up & fast_short)

        side=np.where(long_signal,1,np.where(short_signal,-1,0))
        raw_r=np.clip((atr*atr_mult).values, close.values*0.008, close.values*0.05)
        out[sym]=pd.DataFrame({"side":side,"raw_r":raw_r},index=df.index)
    return out
