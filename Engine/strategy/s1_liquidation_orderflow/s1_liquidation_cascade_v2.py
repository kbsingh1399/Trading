# Engine/strategy/s1_liquidation_cascade_v2.py
from __future__ import annotations
import numpy as np
import pandas as pd


class S1LiquidationCascadeV2:
    """
    Two-stage liquidation-cascade entry:
      STAGE 1 (detect, bar t):   long_liq_zs > 1.8 -> mark FLUSH, record flush_low,
                                 flush_mid = (flush_high + flush_low)/2, arm for `confirm_bars`.
      STAGE 2 (reclaim, bar t+k): close > flush_mid AND absorption confirmed
                                 (footprint wick_sell_absorb OR higher-low structure)
                                 -> signal at reclaim close, filled at Open[k+1].
    Stop = flush_low - buffer (BELOW the absorbed level - the invalidation line,
    not an arbitrary 1R). raw_r = entry - stop. Target = 2.0R.
    Expires if no reclaim within confirm_bars.
    """

    def __init__(self,
                 liq_zs_thresh: float = 1.8,
                 rsi_max: float = 40.0,
                 vwap_max: float = -0.5,
                 confirm_bars: int = 8,
                 stop_buffer_atr_frac: float = 0.15,
                 short_mirror: bool = True):
        self.liq = liq_zs_thresh
        self.rsi_max = rsi_max
        self.vwap_max = vwap_max
        self.confirm = confirm_bars
        self.buf = stop_buffer_atr_frac
        self.mirror = short_mirror

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        T = len(df)
        idx = df.index
        sig = pd.DataFrame({"side": np.zeros(T, dtype=np.int8),
                            "raw_r": np.zeros(T, dtype=np.float64)}, index=idx)

        get = lambda n, d: df.get(n, pd.Series(d, index=idx)).astype(np.float64)
        long_liq = get("long_liq_zs", np.zeros(T)).to_numpy()
        short_liq = get("short_liq_zs", np.zeros(T)).to_numpy()
        rsi = get("rsi_14", np.full(T, 50.0)).to_numpy()
        vwz = get("vwap_zscore", get("dist_to_vwap_zs", np.zeros(T))).to_numpy()
        cl_series = df["close"].astype(np.float64)
        atr = get("atr_14", cl_series * 0.002).clip(lower=1e-12).to_numpy()

        o = df["open"].to_numpy(np.float64)
        h = df["high"].to_numpy(np.float64)
        l = df["low"].to_numpy(np.float64)
        c = cl_series.to_numpy(np.float64)

        # Footprint absorption or price-action fallback
        absorb = np.zeros(T)
        if "wick_sell_absorb" in df.columns:
            ab = df["wick_sell_absorb"].to_numpy(np.float64)
            mu = pd.Series(ab).rolling(96, min_periods=1).mean().to_numpy()
            sd = pd.Series(ab).rolling(96, min_periods=1).std(ddof=0).to_numpy()
            sd = np.where(sd < 1e-12, 1.0, sd)
            absorb = np.clip((ab - mu) / sd, -5, 5)

        higher_low = (l[1:] > l[:-1]).astype(np.float64)
        higher_low = np.concatenate([[0.0], higher_low])
        hl3 = pd.Series(higher_low).rolling(3, min_periods=1).mean().to_numpy()

        # STAGE 1: Flush detection
        flush_long = long_liq > self.liq
        flush_short = (short_liq > self.liq) if self.mirror else np.zeros(T, dtype=bool)

        cur_side, cur_low, cur_hi, cur_exp = 0, np.nan, np.nan, -1
        for t in range(1, T):
            # 1. Expire stale arm
            if cur_side != 0 and t > cur_exp:
                cur_side = 0

            # 2. Flush detection
            is_long_flush = (long_liq[t] > self.liq) and (rsi[t] < self.rsi_max) and (vwz[t] < self.vwap_max)
            is_short_flush = (short_liq[t] > self.liq) and (rsi[t] > (100.0 - self.rsi_max)) and (vwz[t] > -self.vwap_max) if self.mirror else False

            if is_long_flush:
                cur_side = 1
                cur_low = l[t]
                cur_hi = h[t]
                cur_exp = t + self.confirm
                continue
            elif is_short_flush:
                cur_side = -1
                cur_low = l[t]
                cur_hi = h[t]
                cur_exp = t + self.confirm
                continue
            elif cur_side == 1 and long_liq[t] > self.liq:
                cur_low = min(cur_low, l[t])
                cur_hi = max(cur_hi, h[t])
                cur_exp = t + self.confirm
            elif cur_side == -1 and short_liq[t] > self.liq:
                cur_low = min(cur_low, l[t])
                cur_hi = max(cur_hi, h[t])
                cur_exp = t + self.confirm

            # 3. Reclaim check if armed
            if cur_side == 1:
                mid = (cur_low + cur_hi) / 2.0
                reclaim = c[t] > mid
                absorption = (absorb[t] > 0.5) or (hl3[t] >= (2.0 / 3.0))
                stop = cur_low - self.buf * atr[t]
                if reclaim and absorption and c[t] > stop:
                    sig.iat[t, 0] = 1
                    sig.iat[t, 1] = max(c[t] - stop, atr[t] * 0.3)
                    # Disarm immediately to prevent duplicate consecutive entries
                    cur_side = 0
            elif cur_side == -1:
                mid = (cur_low + cur_hi) / 2.0
                reclaim = c[t] < mid
                absorption = (absorb[t] < -0.5) or (hl3[t] >= (2.0 / 3.0))
                stop = cur_hi + self.buf * atr[t]
                if reclaim and absorption and c[t] < stop:
                    sig.iat[t, 0] = -1
                    sig.iat[t, 1] = max(stop - c[t], atr[t] * 0.3)
                    # Disarm immediately to prevent duplicate consecutive entries
                    cur_side = 0

        return sig

