"""OX58-E1: Suite-wide S2/S4 stop-erasure quantification.

Replays the EXACT S2/S4 precompile loop from
Engine/runners/run_23_oos_altcoin_suite.py (lines ~232-300 @ main 15c5e21)
over all 11 masters and counts, for every stopped-out trade, whether the
`if r_gain == -1.0 and ...` fallback overwrites the stop with bar-24 MTM.

Usage:  python3 ox58_erasure_quantify.py [REPO_ROOT]
Repo root must contain Engine/ and binance_backtesting_data/.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
from Engine.core.canonical_indicators import (
    compute_bollinger_bandwidth_zscore, compute_adx_series, compute_kairi_zscore,
)

DATA = ROOT / "binance_backtesting_data"
SYMS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT", "ADAUSDT",
        "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT"]

tot = stopped = tp = exp = over = 0
dR = []
for sym in SYMS:
    df = pd.read_parquet(
        DATA / f"{sym}_15m_master_2020_2026.parquet",
        columns=["open_time_ms", "open", "high", "low", "close", "rsi_14", "atr_14", "ema_200"],
    ).dropna().reset_index(drop=True)
    closes = df["close"].to_numpy(float); opens = df["open"].to_numpy(float)
    highs = df["high"].to_numpy(float); lows = df["low"].to_numpy(float)
    rsis = df["rsi_14"].to_numpy(float); atrs = df["atr_14"].to_numpy(float)
    ema200 = df["ema_200"].to_numpy(float)
    upper, lower, bw, zbw = compute_bollinger_bandwidth_zscore(closes, 96, 2.0, 96)
    _, _, adx = compute_adx_series(highs, lows, closes, 14)
    zkri = compute_kairi_zscore(closes, atrs, 20, 96)
    n = len(df)
    for i in range(200, n - 25):
        dist = atrs[i]
        if dist <= 0:
            continue
        if zbw[i] > 1.85 or adx[i] > 32.0:
            continue
        legs = []
        if closes[i] < lower[i] and rsis[i] < 32.0:
            legs.append((1, 2.2))
        elif closes[i] > upper[i] and rsis[i] > 68.0 and closes[i] <= ema200[i] * 1.01:
            legs.append((-1, 2.2))
        if zkri[i] < -1.75 and rsis[i] < 32.0 and closes[i] >= lower[i]:
            legs.append((1, 2.0))
        elif zkri[i] > 1.75 and rsis[i] > 68.0 and closes[i] <= upper[i] and closes[i] <= ema200[i] * 1.01:
            legs.append((-1, 2.0))
        for side, tgt in legs:
            entry = opens[i + 1] * (1 + 0.0010 * side)
            target = entry + side * tgt * dist
            stop = entry - side * 1.0 * dist
            was_stopped, r = False, -1.0
            for j in range(i + 1, i + 25):
                hs = (lows[j] <= stop) if side == 1 else (highs[j] >= stop)
                ht = (highs[j] >= target) if side == 1 else (lows[j] <= target)
                if hs:
                    r, was_stopped = -1.0, True
                    break
                if ht:
                    r = tgt
                    break
            tot += 1
            if was_stopped:
                stopped += 1
                lh = highs[min(i + 24, n - 1)] if side == 1 else lows[min(i + 24, n - 1)]
                cond = (lh > stop) if side == 1 else (lh < stop)
                if cond:  # suite fallback overwrites this stop
                    over += 1
                    mtm = ((closes[min(i + 24, n - 1)] - entry) / dist) if side == 1 else \
                          ((entry - closes[min(i + 24, n - 1)]) / dist)
                    dR.append(mtm - (-1.0))
            elif r > 0:
                tp += 1
            else:
                exp += 1

dR = np.array(dR)
print(f"candidates={tot} stopped={stopped} tp={tp} expiry={exp}")
print(f"stops overwritten: {over}/{stopped} = {100 * over / stopped:.1f}% "
      f"({100 * over / tot:.1f}% of ALL candidates)")
print(f"mean inflation per overwritten stop: {dR.mean():+.3f}R | total: {dR.sum():+,.0f}R")
