# OPUS 5 — ROUND 9 REAL DATA SCORECARD & SURGICAL CALIBRATION DIRECTIVE

Opus, we immediately executed your `rp2_round9_ml_convex_engine.py` on our real 18-asset Binance master parquet dataset for **Window 1 (May 2021 Great Liquidation Crash)**.

Your Round 9 architecture produced a **massive structural breakthrough** on real data. Here is the verified empirical scorecard and the granular trade ledger diagnosis:

---

## 1. Real Empirical Scorecard (Window 1: May 2021)

```
================== REAL DATA W01 RESULT (ROUND 9) ==================
Window ID     : W01 (May 2021 Great Liquidation Crash)
Trades        : 30 (PASSED >= 15 floor!)
Win Rate %    : 43.33% (PASSED > 40.0% floor!)
Max DD %      : 3.84% (PASSED < 5.0% target, ZERO circuit-breaker trip!)
ROI %         : -2.32%
Avg R         : -0.1947
Max R         : 1.9585 (Substantial expansion over Round 8's 1.1581R)
Profit Factor : 0.512
Model AUC     : 0.6282 (Trained causally on 7,750 pre-purge events)
Model p*      : 0.0337 (Quantile selection worked as designed)
Setup Mix     : {'liq_exhaust': 10, 'funding_squeeze': 17, 'lead_lag': 2, 'vol_shock': 1}
====================================================================
```

---

## 2. The Breakthroughs Confirmed on Real Data
1. **`liq_exhaust` is UNLOCKED**: Decoupling the loose event sampler from the trained GBDT classifier completely solved the Round 8 zero-trade failure. `liq_exhaust` generated **10 high-conviction trades** in May 2021!
2. **Capital Defense Ceilings Bound Completely**: During the violent 50% Bitcoin liquidation collapse, Max Drawdown held at **3.84%** (well beneath your 4.46% synthetic ceiling and our 5.0% hard limit). Your gap-multiplier budget and tail-notional exposure bounds (`catastrophic_gap=0.12`) worked flawlessly.
3. **Causal GBDT Trained Cleanly**: The pure NumPy histogram GBDT and Ridge ensemble fit smoothly on 7,750 real pre-purge events with an out-of-sample validation AUC of **0.6282**.
4. **Trade Floor Cleared**: 30 trades easily cleared the $\ge 15$ trade mandate.

---

## 3. The Forensic Discovery: Why W01 Did Not Clear +20% ROI

We dumped and audited the full 30-trade ledger. Here is the exact mathematical bottleneck:

### A. Exit Reason Breakdown
- `stop`: 23 trades
- `time_decay`: 7 trades
- **`target` (+4.0R): 0 trades** (Zero trades were permitted to reach the +4.0R target!)

### B. MFE vs Realized R (The Ratchet Suffocation Trap)
Look at the Maximum Favorable Excursion (MFE) vs the realized exit R:
- `DOTUSDT funding_squeeze`: Reached **MFE = +3.066R**! But exited at **+1.938R** on a stop pullback.
- `DOGEUSDT vol_shock`: Reached **MFE = +2.558R**! Exited at **+1.958R**.
- `ETHUSDT liq_exhaust`: Reached **MFE = +1.881R**! Exited at **+0.683R**.
- `LTCUSDT liq_exhaust`: Reached **MFE = +1.724R**! Exited at **+0.645R**.
- `ADAUSDT funding_squeeze`: Reached **MFE = +1.718R**! Exited at **+0.708R**.
- `XRPUSDT funding_squeeze`: Reached **MFE = +1.675R**! Exited at **+0.699R**.
- `DOTUSDT funding_squeeze`: Reached **MFE = +1.547R**! Exited at **+0.656R**.
- `LTCUSDT liq_exhaust`: Reached **MFE = +1.391R**! Exited at **-0.022R**.

**Summary**: 
- The strategy successfully found explosive 1.5R to 3.0R runners!
- However, the multi-tier ratchet (moving stops to +0.8R lock at +1.5R gain, or trailing ATR) choked the trades during normal 15m pullbacks.
- Consequently:
  - **Mean Winning Trade**: $+0.602	ext{R}$
  - **Mean Losing Trade**: $-0.804	ext{R}$ (to $-1.15	ext{R}$ with 33 bps frictions)
  - Result: With a 43.3% win rate, $+0.60	ext{R}$ wins cannot overcome $-0.80	ext{R}$ losses.

---

## 4. Resolution to Your Question in §100 (`min_r_multiple: 4`)
You noted the mathematical contradiction: requiring **average realized R** $\ge 4.0	ext{R}$ alongside a $40\%$ win-rate floor is mathematically impossible (it requires a 100% win rate).

**Official Clarification**:
- `min_r_multiple: 4` is the **Target Take-Profit Barrier** (`tp_r = 4.0R`), which the engine already targets.
- In `criteria_check`, evaluate `res["max_r"] >= 3.5` (or verify `tp_r >= 4.0`), while requiring **`avg_r >= 0.35`** (or `roi_pct >= 20.0%`).

---

## 5. Surgical Calibration Roadmap for Round 9.1

1. **Widen Ratchet Breathing Room**:
   - Give runners room to breathe so MFE of 2.0R–3.0R can reach the +4.0R target instead of getting clipped at +0.65R.
   - For example:
     - Tier 1: At $+1.0	ext{R}$ gain $	o$ Move stop to Breakeven $+0.10	ext{R}$.
     - Tier 2: At $+2.0	ext{R}$ gain $	o$ Move stop to $+1.0	ext{R}$.
     - Tier 3: At $+3.2	ext{R}$ gain $	o$ Move stop to $+2.2	ext{R}$.
     - Full Target: Exit at $+4.0	ext{R}$ (or $+6.0	ext{R}$ on cascades).
2. **Relax Time Decay**:
   - 7 trades exited via `time_decay` after 24 bars while still consolidating. Extend `time_decay_bars` to 36 bars (9 hours) or relax `time_decay_min_r` to $+0.10	ext{R}$ so multi-hour setups have time to expand.
3. **Compound with House Money**:
   - Once 2 to 3 trades reach +3.0R to +4.0R, the banked profit activates the house-money scaling ($25 + 0.35 	imes 	ext{banked}$), compounding the monthly ROI straight past $+20.0\%$!

Please deliver the tuned Round 9.1 engine so we can re-verify Window 1 and advance across the full 20-window walk-forward!
