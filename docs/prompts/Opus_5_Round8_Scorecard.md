# OPUS 5 — ROUND 8 EMPIRICAL AUDIT & TUNING DIRECTIVE

Opus, we immediately executed your `rp2_round8_convex_liquidation_leadlag.py` on our real 18-asset Binance master parquet dataset for **Window 1 (May 2021 Great Liquidation Crash: 2021-05-01 to 2021-05-31)**.

Here are the exact answers to your questions and the live empirical scorecard:

---

## 1. Real Data Columns Confirmation
Our production master dataset (`*_15m_master_2020_2026.parquet`) has all real institutional features:
- `long_liq_zs` & `short_liq_zs`: **Real institutional liquidation z-scores** (NOT synthetic proxies!).
- `open_interest`: Mapped from `open_interest_usd` (true USD open interest).
- `funding_rate`: Mapped from `funding_rate_pct / 100.0` (true 8h settlement rate in decimal).
- `volume`: Mapped from `volume_base`.
- Universe depth: 14 symbols actively traded in May 2021 (SUI, APT, ARB, OP launched in 2022–2023).

---

## 2. Real Empirical Scorecard (Window 1: May 2021)
```
================== REAL DATA W01 RESULT ==================
Window ID     : W01 (May 2021 Great Liquidation Crash)
Deploy        : True (Gate ok, Train AUC: 0.5875 across 909 events)
Trades        : 31 (PASSED >= 6 floor)
ROI %         : -2.16%
Max DD %      : 3.20% (PASSED < 5.0% target, zero circuit-breaker trip!)
Win Rate %    : 58.06% (PASSED > 40.0% target! 18 wins / 31 trades)
Avg R         : -0.1284
Max R         : 1.1581
Profit Factor : 0.512
Halted        : False
Setup Mix     : {'funding_squeeze': 27, 'lead_lag': 4, 'liq_exhaust': 0}
==========================================================
```

---

## 3. Forensic Diagnosis: Why W01 Failed the ROI Target
1. **Capital Defense & Win Rate Were Stellar**:
   - Max Drawdown stayed at **3.20%** during a 50% Bitcoin collapse!
   - Win Rate was **58.06%** under strict 33 bps frictions.
   - The purged numpy logistic gate trained cleanly (`AUC = 0.5875`).

2. **The Bottleneck: `liq_exhaust` Took Exactly ZERO Trades**:
   - `liq_exhaust` is the sole source of the 5R–8R right-tail trades you designed to reach +20% ROI.
   - In May 2021, `setup_mix` was: `funding_squeeze: 27`, `lead_lag: 4`, **`liq_exhaust: 0`**.
   - Diagnostics on BTC alone show that liquidation events DID occur:
     - `long_liq_zs >= 2.0 & oi_1h <= -10%`: 9 bars.
     - `long_liq_zs >= 1.8 & oi_1h <= -5%`: 18 bars.
     - `long_liq_zs >= 1.5 & oi_1h <= -3%`: 46 bars.
   - However, the combination of `oi_collapse_1h <= -0.10` AND `liq_z_thresh >= 2.0` AND the strict 2/3 candle reclaim (`hl3 >= 2/3`) AND `flush_min_r_atr` / `max_friction_r` completely filtered out all entries!

3. **`funding_squeeze` Asymmetry Trap**:
   - `funding_squeeze` took 27 trades with a 58% win rate, but `Max R` was only **1.1581R**.
   - Taking 1.0R–1.15R on wins while taking −1.0R on stops (plus 33 bps frictions) yields a Profit Factor of only 0.512 despite winning 58% of trades.

---

## 4. Your Tuning Order (As You Requested)
Following your exact roadmap:
1. **Unlock `SETUP_LIQ`**:
   - Adjust `oi_collapse_1h` (e.g. from `-0.10` to `-0.05` or look at 2h/4h rolling collapse) and `liq_z_thresh` (e.g. from `2.0` to `1.75`).
   - Relax the flush reclaim confirmation (e.g. `hl3 >= 0.50` instead of `2/3`, or allow a multi-bar reclaim window up to 12 bars).
   - Ensure `liq_exhaust` entries take priority over `funding_squeeze` when slots are limited.
2. **Expand `funding_squeeze` & `lead_lag` Payoff Geometry**:
   - Allow winners in `funding_squeeze` to run toward 2.5R–4.0R with the multi-tier ratchet rather than exiting prematurely.
3. **Activate Kelly / House-Money Pyramiding**:
   - Once the 5R–8R liquidation trades start hitting, let the 0.60× pyramid add and Kelly scaling multiply the gains into +20%+ ROI.

Please deliver the tuned Round 8.1 update to `rp2_round8_convex_liquidation_leadlag.py` so we can re-test Window 1!
