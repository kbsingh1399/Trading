# OPUS 5 MASTER DIRECTIVE: CONTINUOUS AUTONOMOUS LOOP MANDATE (MULTI-SLEEVE ENSEMBLE UNTIL 20/20 JOINT PASSES)

Opus 5, Round 15 is a magnificent empirical triumph:
- **+85.00R Swing**: From -71.77R in Round 14 to **+13.23R (+330.75 USD)**.
- **20/20 Drawdown Compliance**: Max Drawdown < 4.5% in every single window.
- **Decisive Microstructure Discoveries**:
  * 4-hour clock solved friction drag (0.089R vs 0.382R on 15m).
  * Inverted quiet-flow gate (`cvd_z <= 1.0` and no stacked-sell) quadrupled edge (+2.970 ATR vs +0.724 ATR, confirming VPIN adverse selection and Wyckoff "no supply").
  * W17 delivered **+13.72R (+343.00 USD) with 81.8% Win Rate and 13.45 R/DD**!

You isolated the single remaining barrier: A single-sleeve long-only trend follower cannot structurally generate trades during bear cascades (W4, W6, W12, W18) because the bullish ribbon only exists on 1.5%–7.0% of bars.

---

## ⛔ STRICT PRINCIPAL MANDATE: KEEP RUNNING CONTINUOUSLY UNTIL ALL 20/20 PASS

**DO NOT STOP. DO NOT PAUSE FOR FURTHER USER DECISIONS OR CONFIRMATIONS.**
You are strictly ordered to execute an **AUTONOMOUS CONTINUOUS EXECUTION LOOP**:
1. Execute Round 16 (Multi-Sleeve Ensemble).
2. If 20/20 passes, declare victory and output the certified deliverables.
3. If any window fails: **DO NOT STOP. DO NOT ASK FOR PERMISSION.** Immediately diagnose using in-sample causal data, adjust sleeve blend or parameters, and immediately execute Round 17 $\to$ Round 18 $\to$ Round 19...
4. **KEEP RUNNING ITERATIVELY UNTIL ALL 20 OUT OF 20 WINDOWS JOINTLY PASS!**

All necessary approvals, design authority, and architectural specifications are officially granted below:

---

## 1. Principal's Specification Amendments & Approvals

### 1.1 Full Approval of Cross-Sectional Relative-Strength (CS-RS) Engine (Genuine 11)
- You are fully authorized to deploy a market-neutral / relative-strength long/short engine across the Genuine 11 (`BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH`).
- In bear regimes (W4, W6, W8, W12, W18), altcoins experience severe cross-sectional return dispersion. Long the top 2 RS leaders and short the bottom 2 RS laggards to generate consistent trade supply and positive alpha without net long-beta exposure!

### 1.2 Full Approval of Sleeve C: Liquidation Cascade Absorption (Mayne / Marco)
- In deep bear capitulation flushes where 4h trend filters are silent, forced liquidation cascades (`long_liq_zs > 1.80`, `zc_div > 0.80`, Spot CVD whale absorption) generate violent V-shaped mean-reverting bounces.
- In W02 and prior tests, this exact setup produced 71.4% to 86.7% win rates and over +1,052.00 USD net profit!
- Combining the **4h Quiet-Flow Trend Sleeve** (active in bull regimes) with the **Liquidation Absorption Sleeve** (active in bear flushes) naturally supplies qualifying trades across all market regimes.

### 1.3 Portfolio Aggregate Trade-Count Floor
- The trade-count floor of $\ge 15$ trades per window is evaluated at the **AGGREGATE PORTFOLIO LEVEL** across all 3 active sleeves combined.
- As long as the portfolio generates $\ge 15$ completed trades in the window with Net ROI $> +10.0\%$, MaxDD $< 4.5\%$, and Win Rate $> 40.0\%$, the window is a certified PASS.

---

## 2. Multi-Sleeve Architectural Blueprint

### Sleeve A: 4-Hour Convex Trend Follower (Your Round 15 Breakthrough)
- **Clock**: 4-Hour bars aggregated server-side from real 15m bars in Kusto.
- **Universe**: Genuine 11 (`BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH`).
- **Entry**: Donchian-20 channel breakout with bullish EMA ribbon (`EMA21 > EMA50 > EMA200`) and positive macro slope (`EMA200[t] >= EMA200[t-6]`).
- **Quiet-Flow Gate**: `cvd_z <= +1.00` AND `is_stacked_sell_imb == 0`.
- **Exit Geometry**:
  * Initial Stop: $2.5 \times \text{ATR}_{14}$ (friction drag is only $0.089\text{R}$).
  * Tier 1: Bank $50\%$ at $+2.0\text{R}$ (clearing friction and locking profit).
  * Tier 2: Raise stop to Entry $+0.35\text{R}$; trail loose $3.5 \times \text{ATR}$ chandelier or 6-bar swing low to target $6.0\text{R}$ ($8.0\text{R}$ on $\text{short\_liq\_zs} \ge 1.50$).
  * Vertical Time Decay: Exit at market if $< +0.20\text{R}$ after 24 bars.

### Sleeve B: Cross-Sectional Relative Strength (CS-RS Long/Short)
- **Clock**: 4-Hour bars.
- **Mechanism**: Compute rolling 180-bar (30d) cumulative excess return of each Genuine 11 asset against the equal-weighted universe benchmark.
- **Execution**: Long Top 2 RS Leaders ($z_{\text{RS}} > +1.0$) / Short Bottom 2 RS Laggards ($z_{\text{RS}} < -1.0$) when dispersion $> 1.5\sigma$.
- **Stop/Exit**: Weekly rebalance or trailing $2.0 \times \text{ATR}$ stop. Beta-balanced dollar sizing ensures zero directional exposure to market crashes.

### Sleeve C: Liquidation Cascade Absorption (Capitulation Flushes)
- **Clock**: 15-Minute bars.
- **Condition**: Fires during systemic forced liquidations when trend sleeve is dormant:
  $$\text{long\_liq\_zs} > 1.80 \quad \land \quad \text{zc\_div} > 0.80 \quad \land \quad \text{RSI} < 35 \quad \land \quad \Delta\text{Spot} > 0 \quad \land \quad \Delta\text{Futures} < 0$$
- **Exit Geometry**:
  * Stop: $1.5 \times \text{ATR}_{14}$ placed below flush wick.
  * Phase 0 Ratchet: At $+0.80\text{R}$ gain, move stop to Entry $+0.15\text{R}$ (BE lock).
  * Phase 1 Profit Lock: At $+1.50\text{R}$ gain, move stop to Entry $+0.80\text{R}$.
  * Take Profit: Target $+2.50\text{R}$ (or VWAP upper band touch).
  * Time Stop: Exit at market if $< +0.20\text{R}$ within 16 15m bars (4 hours).

---

## 3. Portfolio Allocation & Risk Budget
- **Initial Capital**: 5,000.00 USD.
- **Total Concurrent Open Positions**: Max 3 positions across all sleeves simultaneously.
- **Base Risk per Trade**: 25.00 USD (0.50% of initial capital).
- **House Money Risk**: 50.00 USD (1.00% max 2x risk) when net banked profit $> +50.00$ USD.
- **Drawdown Defense Risk**: 15.00 USD (0.30% risk) arming at 2.00% drawdown.
- **Hard Portfolio Circuit Breaker**: 4.50% (225.00 USD hard floor at 4,775.00 USD equity).
- **Full Exchange Frictions**: Mandatory 41 bps worst-case round-trip stop friction ($8\text{ bps}$ entry + $8\text{ bps}$ exit + $10\text{ bps}$ entry slip + $15\text{ bps}$ stop slip).

---

## 4. Autonomous Loop Execution Protocol
1. Synthesize the Multi-Sleeve Engine in KQL server-side and Python reference kernel.
2. Run live 20-window walk-forward evaluation across all 20 non-overlapping OOS windows.
3. Compute the full scorecard:
   - If all 20 windows pass (ROI $> 10.0\%$, MaxDD $< 4.5\%$, WR $> 40.0\%$, Trades $\ge 15$), generate the final pass deliverables and complete the mission.
   - If any window fails: **DO NOT STOP. DO NOT ASK FOR PERMISSION.** Immediately isolate the root cause, re-weight sleeve allocation or refine thresholds causally, and execute the next iteration (Round 17, Round 18...) until **20/20 JOINT PASS IS ACHIEVED!**

Opus, you cracked the physics of 4h trend following. Now execute the multi-sleeve engine and keep running until all 20 out of 20 windows pass!
