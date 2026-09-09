# MASTER QUANTITATIVE MISSION PROMPT: TRADINGVIEW STRATEGY SUITE HARNESS
## DECONSTRUCTION, ORDERFLOW & ML ENHANCEMENT ACROSS ALL 20 QUARTERLY OOS WINDOWS (2021-2025)
## TARGET PLATFORM: CLAUDE OPUS 5 (OX ALPHA / ARENA.AI)
==============================================================================================================

### 1. MISSION DIRECTIVE & CORE CONSTRAINTS
You are acting as the Chief Quantitative Architect for an institutional crypto proprietary trading desk. You operate in a brand new chat session with zero memory, zero chat context, and zero external repository access. Every specification, formula, dataset definition, and friction model is self-contained in this prompt.

Your objective is to ingest, analyze, improve, and backtest a suite of 25 distinct TradingView & institutional strategy archetypes (including Toby Crabel NR7/NR4) extracted directly from production TradingView community strategies. Every strategy in Section 4 is provided with its complete, self-contained mathematical rulebook, indicator parameters, entry/exit conditions, failure modes, and required institutional orderflow/ML upgrades.

You must:
1. Evaluate all 25 strategy archetypes under full 41.0 bps round-trip taker frictions on the Certified Genuine 11 Binance USDT-M Perpetuals on a causal 4-Hour clock across all 20 quarterly OOS windows (2021-2025).
2. Enhance each archetype using our institutional orderflow suite (CVD Divergence, Spot vs Futures Delta Disparity, Liquidation Z-scores, Bar Close Efficiency) and Machine Learning meta-classifier overlay (LightGBM/XGBoost).
3. Select the top complementary strategy sleeves and build a unified, drop-in Python engine that achieves a verified 20/20 PASS across all 20 quarterly windows.

==============================================================================================================
### 2. DATASET PROVENANCE & INSTITUTIONAL FRICTION MODEL
- Universe: Certified Genuine 11 Binance USDT-M Perpetuals (BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH). Speculative synthetic altcoins (PEPE, WIF, TIA, INJ) lacking 2020-2022 historical depth are quarantined.
- Historical Coverage: September 2020 to March 2026 (3,467,571 15-minute bars resampled to 13,178 causal 4-hour bars per asset). Zero nulls, 100% monotonic timestamps.
- Full Exchange Frictions (Mandatory):
  * Taker Fee per side: 0.0008 (8 bps per side = 16 bps round-trip)
  * Entry Slippage: 0.0010 (10 bps)
  * Stop-Loss Exit Slippage: 0.0015 (15 bps)
  * Total Round-Trip Execution Drag: 41.0 bps (0.0041)
- Portfolio Governor & Risk Budget (Fixed 5,000.00 USD Capital):
  * Initial Capital: 5,000.00 USD
  * Base Risk per Trade: 35.00 to 45.00 USD (0.70% to 0.90%)
  * Drawdown Defense Risk: 15.00 USD (armed when drawdown >= 2.00% / 100.00 USD)
  * House Money Risk: 100.00 USD (unlocked strictly at net profit >= +50.00 USD)
  * Hard Circuit Breaker (Max Drawdown Limit): 4.50% (225.00 USD)
  * Max Concurrent Positions: 2 open trades across all 11 symbols simultaneously
  * Max Leverage: 10.0x (Max Notional: 50,000.00 USD)
- Quarter Pass Criteria (All 4 conditions required simultaneously):
  1. Net ROI >= +10.00% (+500.00 USD net on 5,000.00 USD capital)
  2. Max Drawdown <= 4.50% (225.00 USD hard stop)
  3. Win Rate >= 40.0%
  4. Completed Trades >= 15 per quarter across active sleeves

==============================================================================================================
### 3. THE 20 CANONICAL OUT-OF-SAMPLE (OOS) QUARTERS (2021-2025)
All 20 non-overlapping quarterly windows must be evaluated sequentially with strict causal 72-hour purge boundaries (t_purge = t_start - 72h):
Q01: 2021-01-01 to 2021-03-31 (Historic Bull Run Expansion)
Q02: 2021-04-01 to 2021-06-30 (May 19 Capitulation & Great Flush)
Q03: 2021-07-01 to 2021-09-30 (Summer Recovery & El Salvador Day)
Q04: 2021-10-01 to 2021-12-31 (69k USD Blowoff Top & Macro Reversal)
Q05: 2022-01-01 to 2022-03-31 (Fed Tightening & Initial Macro Selloff)
Q06: 2022-04-01 to 2022-06-30 (Terra-LUNA & 3AC/Celsius Insolvency Crash)
Q07: 2022-07-01 to 2022-09-30 (Post-Contagion Summer Range & ETH Merge)
Q08: 2022-10-01 to 2022-12-31 (FTX Bankruptcy Cycle Low Flush)
Q09: 2023-01-01 to 2023-03-31 (V-Shape Rebound & SVB Bailout Short Squeeze)
Q10: 2023-04-01 to 2023-06-30 (Range Grind & BlackRock Spot ETF Ignition)
Q11: 2023-07-01 to 2023-09-30 (Summer Flash Flush & Ripple Court Victory)
Q12: 2023-10-01 to 2023-12-31 (Uptober to 44k USD ETF Front-Running Rally)
Q13: 2024-01-01 to 2024-03-31 (Spot ETF Approval to 73.7k USD Cycle ATH)
Q14: 2024-04-01 to 2024-06-30 (Post-Halving Shakeout & Grayscale Outflows)
Q15: 2024-07-01 to 2024-09-30 (August 5 Yen Carry Crash & Fast Recovery)
Q16: 2024-10-01 to 2024-12-31 (US Election Mega Breakout to 99k USD)
Q17: 2025-01-01 to 2025-03-31 (Inauguration Cycle Consolidation)
Q18: 2025-04-01 to 2025-06-30 (Mid-Cycle Expansion & Altcoin Rotation)
Q19: 2025-07-01 to 2025-09-30 (Derivative Expiry & Volatility Compression)
Q20: 2025-10-01 to 2025-12-31 (Late-Cycle Microstructure Expansion)

==============================================================================================================
### 4. FULLY SELF-EXPLANATORY DECONSTRUCTED STRATEGY CARDS (ALL 25 ARCHETYPES)
Below is the complete forensic catalog of all 25 TradingView & institutional strategies. Each card details the exact mathematical rules, parameters, entry/exit logic, failure modes in crypto, and required orderflow/ML solutions:

#### [ST-01] Power Surge | BB Momentum Squeeze Release
- **Reference File**: `web_page_text (22).txt` | **Category**: Family 1: Volatility Squeeze & Compression Breakouts
- **Indicators & Parameters**: Bollinger Bands (20, 2.0), Keltner Channels (20, 1.5 ATR), Bull/Bear Power Oscillator (0-100)
- **Core Concept**: Trades volatility expansion following tight compression. Detects when Bollinger Bands contract inside Keltner Channels (John Carter Squeeze). The trigger occurs when the squeeze releases (BB expands outside KC) and Bull/Bear Power accelerates.
- **Exact Long Entry Rules**:
  * Squeeze Active: Bollinger Upper Band < Keltner Upper Band AND Bollinger Lower Band > Keltner Lower Band within the last 5 bars.
  * Squeeze Release: Current bar Bollinger Upper Band crosses above Keltner Upper Band.
  * Momentum Confirmation: Bull Power Oscillator crosses above 50 (or crosses above upper trigger threshold).
  * Bar Filter: Current bar close > open (bullish candle).
- **Exact Short Entry Rules**:
  * Squeeze Active: BB inside KC within the last 5 bars.
  * Squeeze Release: Bollinger Lower Band crosses below Keltner Lower Band.
  * Momentum Confirmation: Bear Power Oscillator crosses below 50.
  * Bar Filter: Current bar close < open (bearish candle).
- **Stop Loss & Target Geometry**: Stop Loss placed at opposite Keltner Channel or 1.5x ATR from entry. Target: 2.0R to 2.5R or trailing band exit.
- **Crypto Failure Mode**: In crypto, volatility squeezes frequently generate 'head-fakes' (breaking out 1 bar then violently reversing into liquidations). 41 bps friction destroys sub-hourly scalping.
- **Orderflow & ML Enhancement**: Require Quiet-Flow confirmation (|cvd_z| <= 1.0, no exhaustion spike) + positive spot CVD slope (spot_cvd.diff(4) > 0) + Bar Close Efficiency >= 0.65. Filter through LightGBM P(Win) >= 0.62.

#### [ST-02] CRT SNIPER (Candle Range Theory)
- **Reference File**: `web_page_text (19).txt` | **Category**: Family 1: Volatility Squeeze & Compression Breakouts
- **Indicators & Parameters**: Session Opening Ranges, Higher Timeframe Fair Value Gaps (FVG), Range Contraction
- **Core Concept**: Candle Range Theory establishes that every major expansion starts with a reference range. The strategy marks the high and low of a reference consolidation range (e.g. 4-hour open range) and waits for liquidity sweeps followed by impulsive breakout expansion.
- **Exact Long Entry Rules**:
  * Establish reference range [Range_Low, Range_High] over prior N bars.
  * Liquidity sweep: Price dips below Range_Low but closes back inside the range (sweep/reclaim).
  * Impulsive expansion: Bar closes above Range_High with expansion volume (> 1.3x rolling volume).
  * FVG Creation: Leaves a 3-bar Fair Value Gap (Bar 1 High < Bar 3 Low).
- **Exact Short Entry Rules**:
  * Establish reference range [Range_Low, Range_High].
  * Liquidity sweep: Price spikes above Range_High but closes back inside (sweep/reclaim).
  * Impulsive breakdown: Bar closes below Range_Low with expansion volume.
  * FVG Creation: Leaves a 3-bar Fair Value Gap (Bar 1 Low > Bar 3 High).
- **Stop Loss & Target Geometry**: Stop Loss placed at the liquidity sweep extreme. Target: 2.5R or opposite session liquidity pool.
- **Crypto Failure Mode**: Retail CRT relies on 1m/5m MNQ sessions. In crypto perpetuals, sweep levels cascade into forced margin liquidations, turning 'false breakouts' into multi-day trend moves.
- **Orderflow & ML Enhancement**: Anchor to 4-Hour clock. Longs require Spot CVD divergence (zc_div > 0.8) and Delta Disparity (Spot Delta > 0, Futures Delta < 0). Governed strictly by the Bitcoin 4h Macro Tide Gate.

#### [ST-03] Daybreak Strategy (Opening Range Breakout / ORB)
- **Reference File**: `web_page_text (20).txt` | **Category**: Family 1: Volatility Squeeze & Compression Breakouts
- **Indicators & Parameters**: Opening Range High/Low, ATR(14), Sensitivity Multiplier
- **Core Concept**: Classic Opening Range Breakout adapted for volatile instruments. Calculates the high and low of the opening reference bar and projects dynamic entry buffer triggers using ATR sensitivity.
- **Exact Long Entry Rules**:
  * Identify opening reference bar range [OR_Low, OR_High].
  * Trigger Level: Entry_Long = OR_High + (Sensitivity * ATR).
  * Execution: Buy stop order triggered when market trades at or above Entry_Long.
- **Exact Short Entry Rules**:
  * Identify opening reference bar range [OR_Low, OR_High].
  * Trigger Level: Entry_Short = OR_Low - (Sensitivity * ATR).
  * Execution: Sell stop order triggered when market trades at or below Entry_Short.
- **Stop Loss & Target Geometry**: Stop Loss placed at OR Midpoint or opposite OR boundary. Target: 2.0R to 2.5R.
- **Crypto Failure Mode**: Crypto has no market open (24/7/365). Arbitrary daily opens generate inconsistent ranges. Breakouts without orderflow confirmation suffer 75% retracement rates.
- **Orderflow & ML Enhancement**: Replace arbitrary time opens with 20-bar Donchian High/Low on 4h bars (80h structural boundary). Require volume ratio > 1.30 and spot accumulation.

#### [ST-04] Execution-Aware Trend [BSL]
- **Reference File**: `web_page_text (15).txt` | **Category**: Family 1: Volatility Squeeze & Compression Breakouts
- **Indicators & Parameters**: Fast EMA(20), Slow EMA(50), ATR(14), Declared Frictional Slippage Model
- **Core Concept**: A trend-and-breakout strategy built around realistic next-tick execution, cost accounting, and strict out-of-sample sample splits. Eliminates bar-magnifier lookahead bias.
- **Exact Long Entry Rules**:
  * Trend Filter: Fast EMA > Slow EMA.
  * Breakout Trigger: Close crosses above highest high of last 20 bars.
  * Next-Tick Fill: Entry simulated on next bar Open + full taker fee + slippage penalty.
- **Exact Short Entry Rules**:
  * Trend Filter: Fast EMA < Slow EMA.
  * Breakdown Trigger: Close crosses below lowest low of last 20 bars.
  * Next-Tick Fill: Entry simulated on next bar Open - full taker fee - slippage penalty.
- **Stop Loss & Target Geometry**: Stop Loss: Entry - 1.5 * ATR. Target: 2.5R with piecewise breakeven ratchet at +0.8R.
- **Crypto Failure Mode**: Standard Donchian breakouts suffer heavy whipsaws during sideways macro regimes (e.g. 2022 crypto winter and summer 2023).
- **Orderflow & ML Enhancement**: This is the structural backbone of Sleeve T1! Upgraded with the Quiet-Flow Inversion Gate (|cvd_z| <= 1.0) and Bar Close Efficiency >= 0.65.

#### [ST-05] BB-SMA Trend Following [DNSE VN301!]
- **Reference File**: `web_page_text (3).txt` | **Category**: Family 1: Volatility Squeeze & Compression Breakouts
- **Indicators & Parameters**: Bollinger Bands (20, 2.0 SD), SMA(200)
- **Core Concept**: Combines dynamic volatility channel breakouts with a macro moving average filter to ensure trades are taken only in the direction of the secular trend.
- **Exact Long Entry Rules**:
  * Macro Filter: Close > SMA(200).
  * Volatility Breakout: Close crosses above Upper Bollinger Band.
  * Band Expansion: (Upper BB - Lower BB) > rolling 20-bar mean band width.
- **Exact Short Entry Rules**:
  * Macro Filter: Close < SMA(200).
  * Volatility Breakdown: Close crosses below Lower Bollinger Band.
  * Band Expansion: Band width expanding.
- **Stop Loss & Target Geometry**: Stop Loss: Middle Bollinger Band (SMA 20) or Entry - 1.5 * ATR. Target: Trailing upper band or 2.5R.
- **Crypto Failure Mode**: Entering when price touches the outer band often enters at extreme overbought conditions right before mean-reversion pullbacks.
- **Orderflow & ML Enhancement**: Enforce Non-Overextension rule (|Close - EMA 20| <= 1.5 * ATR) + Spot CVD velocity (diff3 > 0) to verify institutional buying rather than retail FOMO.

#### [ST-06] Gradient Ribbon | EMA Slope-Acceleration System
- **Reference File**: `web_page_text (25).txt` | **Category**: Family 2: Multi-Timeframe Trend Following & Slope Acceleration
- **Indicators & Parameters**: 5-EMA Ribbon (8, 13, 21, 34, 55), Per-line Slope Derivative (dEMA/dt), Acceleration Delta
- **Core Concept**: Traditional ribbons check moving average ordering, which lags significantly. Gradient Ribbon calculates the first and second derivatives of each EMA line, detecting trend ignition when slopes diverge and expand apart.
- **Exact Long Entry Rules**:
  * Ribbon Stacking: EMA(8) > EMA(13) > EMA(21) > EMA(34) > EMA(55).
  * Slope Acceleration: d/dt(EMA 8) > d/dt(EMA 21) > 0 (ribbon expanding outward).
  * Ignition Trigger: Slope acceleration exceeds historical threshold while Ribbon Width expands by > 20% over 3 bars.
- **Exact Short Entry Rules**:
  * Ribbon Stacking: EMA(8) < EMA(13) < EMA(21) < EMA(34) < EMA(55).
  * Slope Acceleration: d/dt(EMA 8) < d/dt(EMA 21) < 0 (downward acceleration).
  * Ignition Trigger: Ribbon expanding downward.
- **Stop Loss & Target Geometry**: Stop Loss: Lowest EMA line (EMA 55) or 1.5 * ATR. Target: Partial at +1.5R, trail remainder until EMA(8) crosses EMA(21).
- **Crypto Failure Mode**: High correlation among 5 EMAs causes late entries at trend maturity during crypto blow-off moves. Heavy stop-outs on sharp mean-reversions.
- **Orderflow & ML Enhancement**: Combine Ribbon slope acceleration with Delta Dominance (Buy Vol / Total Vol >= 0.55) and Bitcoin 4h Macro Tide Gate.

#### [ST-07] Bitcoin SuperFlip | Supertrend EMA Trend System
- **Reference File**: `web_page_text (9).txt` | **Category**: Family 2: Multi-Timeframe Trend Following & Slope Acceleration
- **Indicators & Parameters**: Supertrend (ATR 10, Multiplier 3.0), EMA(200), ADX(14)
- **Core Concept**: A trend-following system designed specifically for Bitcoin. Uses a dynamic ATR-based volatility envelope that flips polarity when price breaches the trailing stop boundary, filtered by macro EMA.
- **Exact Long Entry Rules**:
  * Macro Trend: Price > EMA(200) AND EMA(200) slope > 0.
  * Supertrend Flip: Supertrend line flips from Red (Resistance) to Green (Support).
  * Strength Filter: ADX(14) >= 20 (confirming non-ranging market).
- **Exact Short Entry Rules**:
  * Macro Trend: Price < EMA(200) AND EMA(200) slope < 0.
  * Supertrend Flip: Supertrend line flips from Green to Red.
  * Strength Filter: ADX(14) >= 20.
- **Stop Loss & Target Geometry**: Stop Loss: Trailing Supertrend line value. Target: Reversal flip or fixed +2.5R target.
- **Crypto Failure Mode**: Supertrend chops severely during 2-3 month sideways consolidation periods, incurring rapid consecutive drawdowns that breach the 4.5% circuit breaker.
- **Orderflow & ML Enhancement**: Add Volatility Compression Inversion Gate: Only take Supertrend flips that emerge from low-volatility regimes (rolling ATR percentile < 40th percentile) with confirmed spot volume expansion.

#### [ST-08] SMA ADX/DI Trend Following Strategy
- **Reference File**: `web_page_text (21).txt` | **Category**: Family 2: Multi-Timeframe Trend Following & Slope Acceleration
- **Indicators & Parameters**: SMA(89), ADX(14), +DI / -DI directional indicators
- **Core Concept**: Combines a Fibonacci moving average slope (SMA 89) with Wilder's DMI directional system. Requires triple confluence: baseline trend slope, directional dominance (+DI > -DI), and trend intensity (ADX > 25).
- **Exact Long Entry Rules**:
  * Baseline Slope: SMA(89) > SMA(89)[1] AND Close > SMA(89).
  * Directional Dominance: +DI crosses above -DI.
  * Trend Intensity: ADX(14) > 25 and rising.
- **Exact Short Entry Rules**:
  * Baseline Slope: SMA(89) < SMA(89)[1] AND Close < SMA(89).
  * Directional Dominance: -DI crosses above +DI.
  * Trend Intensity: ADX(14) > 25 and rising.
- **Stop Loss & Target Geometry**: Stop Loss: Entry - 1.5 * ATR. Target: 2.5R with time decay exit at 24 bars.
- **Crypto Failure Mode**: ADX is notoriously lagging. By the time ADX rises above 25 on 4h bars, 60% of the directional move has already occurred.
- **Orderflow & ML Enhancement**: Replace lagging ADX with leading Orderflow Delta Momentum: Volume Ratio > 1.30 + Spot CVD Velocity (diff3 > 0). Enforce Bar Close Efficiency >= 0.65.

#### [ST-09] Universal Aggressive Trend MACD v3.3
- **Reference File**: `web_page_text (5).txt` | **Category**: Family 2: Multi-Timeframe Trend Following & Slope Acceleration
- **Indicators & Parameters**: Fast MACD (8, 21, 5), Baseline EMA(100), ATR Trailing Profit Ratchet
- **Core Concept**: An aggressive trend-following momentum engine. Waits for MACD histogram expansion in alignment with a structural moving average, entering early in the momentum cycle with dynamic profit-locking.
- **Exact Long Entry Rules**:
  * Trend Bias: Close > EMA(100).
  * Momentum Expansion: MACD line crosses above Signal line while MACD Histogram > 0 and increasing.
  * Zero-Line Alignment: MACD cross occurs near or above the zero line.
- **Exact Short Entry Rules**:
  * Trend Bias: Close < EMA(100).
  * Momentum Expansion: MACD line crosses below Signal line while Histogram < 0 and decreasing.
  * Zero-Line Alignment: MACD cross occurs near or below zero.
- **Stop Loss & Target Geometry**: Stop Loss: Swing low of last 5 bars or 1.5 * ATR. Target: Multi-stage profit lock (+0.8R to BE, +1.5R to +0.8R, target +2.5R).
- **Crypto Failure Mode**: MACD generates excessive false crosses during crypto range-bound regimes, leading to capital bleed.
- **Orderflow & ML Enhancement**: Filter MACD crosses with Spot-versus-Futures Delta Disparity and require that the bar delta z-score >= 0.80 for longs.

#### [ST-10] Asymmetric Trend Strategy [QuantAlgo]
- **Reference File**: `web_page_text (7).txt` | **Category**: Family 2: Multi-Timeframe Trend Following & Slope Acceleration
- **Indicators & Parameters**: Asymmetric Trailing Envelope, Trend Momentum Indicator, Volatility Scaler
- **Core Concept**: Addresses the classic trend-following trade-off: tight trailing stops exit winners too early, loose trailing stops give back too much profit. Uses an asymmetric volatility envelope that trails loosely during initial expansion and tightens aggressively as move matures.
- **Exact Long Entry Rules**:
  * Trend Ignition: Price breaks above upper asymmetric envelope.
  * Momentum Confirmation: Trend Momentum Indicator > 0.
  * Asymmetric Stop Arming: Initial stop placed loosely at Entry - 2.0 * ATR; shifts to tight +0.8R trail once price exceeds +1.5R.
- **Exact Short Entry Rules**:
  * Trend Breakdown: Price breaks below lower asymmetric envelope.
  * Momentum Confirmation: Trend Momentum Indicator < 0.
  * Asymmetric Stop: Loose initial stop, tight trailing ratchet after +1.5R gain.
- **Stop Loss & Target Geometry**: Asymmetric Ratchet: Target +2.5R.
- **Crypto Failure Mode**: Without an exchange friction model, asymmetric envelopes overtrade during low-volatility periods.
- **Orderflow & ML Enhancement**: Integrate directly into our Microstructure Piecewise Ratchet (+0.8R to BE+0.15R, +1.5R to +0.8R, target +2.5R, 24-bar time decay).

#### [ST-11] EMA Pullback Trend Continuation with Volume
- **Reference File**: `web_page_text (16).txt` | **Category**: Family 3: Orderflow & Volume-Confirmed Pullback Absorption
- **Indicators & Parameters**: Macro EMA(200), Pullback EMA(21), Volume SMA(20), RSI(14)
- **Core Concept**: Exploits the core flaw of breakout strategies (buying high into resistance). Waits for a verified higher-timeframe trend, then enters strictly on pullbacks into the dynamic support of the 21 EMA with low volume (absorption), followed by an impulsive rejection bar.
- **Exact Long Entry Rules**:
  * Macro Trend: Price > EMA(200) AND EMA(200) slope > 0.
  * Pullback Phase: Price pulls back to touch or enter the zone between EMA(21) and EMA(50).
  * Exhaustion Volume: Volume during pullback bars is declining (< Volume SMA 20).
  * Rejection Bar: Bullish rejection candle forms at EMA(21) with RSI bouncing off 40-45 support.
- **Exact Short Entry Rules**:
  * Macro Trend: Price < EMA(200) AND EMA(200) slope < 0.
  * Pullback Phase: Price rallies to retest underside of EMA(21).
  * Exhaustion Volume: Declining volume on counter-trend bounce.
  * Rejection Bar: Bearish rejection candle at EMA(21) with RSI rejecting 55-60 resistance.
- **Stop Loss & Target Geometry**: Stop Loss: Placed just below the pullback swing low. Target: Prior swing high or +2.5R.
- **Crypto Failure Mode**: During sharp liquidation events (e.g. May 2021, Nov 2022), pullbacks do not bounce at EMA 21—they slice through EMA 200 and cascade.
- **Orderflow & ML Enhancement**: This is the blueprint for Sleeve T2! Add Long Liquidation Surge (long_liq_zs > 1.20) + CVD Divergence (zc_div > 0.80) to confirm institutional absorption before entering.

#### [ST-12] Trend Trigger | EMA Filter + MTF Stochastic + ATR
- **Reference File**: `web_page_text (18).txt` | **Category**: Family 3: Orderflow & Volume-Confirmed Pullback Absorption
- **Indicators & Parameters**: EMA(38), EMA(62), Higher-Timeframe Stochastic (14, 3, 3), ATR(14)
- **Core Concept**: Decouples trend identification from entry timing. Uses an intermediate EMA ribbon (38/62) to grant directional permission, while a higher-timeframe Stochastic oscillator timing engine executes only when market reaches oversold extremes within an uptrend.
- **Exact Long Entry Rules**:
  * Trend Permission: EMA(38) > EMA(62).
  * Timing Trigger: Higher-timeframe Stochastic %K crosses above %D from below 20 (oversold reset).
  * Structural Filter: Current bar close > EMA(38).
- **Exact Short Entry Rules**:
  * Trend Permission: EMA(38) < EMA(62).
  * Timing Trigger: Higher-timeframe Stochastic %K crosses below %D from above 80 (overbought reset).
  * Structural Filter: Current bar close < EMA(38).
- **Stop Loss & Target Geometry**: Stop Loss: Entry - 1.5 * ATR. Target: 2.0R to 2.5R.
- **Crypto Failure Mode**: Stochastic oscillators pin at oversold/overbought levels for weeks during sustained crypto bull/bear runs, triggering premature counter-trend traps.
- **Orderflow & ML Enhancement**: Replace Stochastic with Rolling VWAP Z-score (VWAP Z < -0.50) + Spot CVD velocity (diff3 > 0) to verify genuine institutional accumulation.

#### [ST-13] Golden Trident | Swing-Anchored VWAP Trend System
- **Reference File**: `web_page_text (13).txt` | **Category**: Family 3: Orderflow & Volume-Confirmed Pullback Absorption
- **Indicators & Parameters**: Swing High/Low Structure (HH/HL, LH/LL), Anchored VWAP, ATR(14)
- **Core Concept**: Replaces lagging moving averages with structural swing-anchored VWAP. Detects genuine market structure breaks (Higher High + Higher Low), anchors VWAP to the structural pivot low, and trades retests of the anchored VWAP fair-value line.
- **Exact Long Entry Rules**:
  * Market Structure: Formation of confirmed Higher Low (HL) followed by Higher High (HH).
  * VWAP Anchor: Anchor VWAP to the confirmed swing low pivot.
  * Pullback & Acceptance: Price pulls back to test Anchored VWAP line.
  * Trigger: Bullish price rejection holding above Anchored VWAP.
- **Exact Short Entry Rules**:
  * Market Structure: Formation of confirmed Lower High (LH) followed by Lower Low (LL).
  * VWAP Anchor: Anchor VWAP to the confirmed swing high pivot.
  * Pullback & Acceptance: Price rallies to test Anchored VWAP line from below.
  * Trigger: Bearish price rejection holding below Anchored VWAP.
- **Stop Loss & Target Geometry**: Stop Loss: Below swing anchor low. Target: 2.5R or retest of structural highs.
- **Crypto Failure Mode**: Discretionary swing pivot identification suffers from lookback sensitivity; in choppy markets, swing points repaint or fail rapidly.
- **Orderflow & ML Enhancement**: Anchor VWAP daily (6 bars on 4h clock). Confirm anchored VWAP retest with Delta Disparity (Spot Delta > 0, Futures Delta < 0) and Bar Close Efficiency >= 0.65.

#### [ST-14] Momentum Trail Strategy [BadRock]
- **Reference File**: `web_page_text (12).txt` | **Category**: Family 3: Orderflow & Volume-Confirmed Pullback Absorption
- **Indicators & Parameters**: Session VWAP, VWAP Slope, RSI(14) Headroom Filter, Intrabar Protective Exit
- **Core Concept**: Confirmed-bar momentum model with dynamic headroom filtering. Uses session VWAP slope for directional bias, requires RSI to be in a non-exhausted zone (RSI 45-60 for longs) to ensure headroom exists, and enforces risk-budgeted position sizing.
- **Exact Long Entry Rules**:
  * Session Bias: Session VWAP slope > 0 AND Price > Session VWAP.
  * Headroom Veto: RSI(14) between 45 and 62 (not overbought, room to expand).
  * Confirmed Bar: Current bar closes in upper 30% of its range with positive momentum.
- **Exact Short Entry Rules**:
  * Session Bias: Session VWAP slope < 0 AND Price < Session VWAP.
  * Headroom Veto: RSI(14) between 38 and 55.
  * Confirmed Bar: Current bar closes in lower 30% of range.
- **Stop Loss & Target Geometry**: Stop Loss: Entry - 1.5 * ATR. Target: 2.5R with intrabar trailing stop.
- **Crypto Failure Mode**: RSI headroom filters frequently block the best vertical breakout trades in crypto, where RSI remains above 70 for the entire duration of a 30% rally.
- **Orderflow & ML Enhancement**: Replace RSI headroom with Orderflow Inversion Gate (|cvd_z| <= 1.0) and verify that Futures Delta is confirmed by Spot CVD Slope.

#### [ST-15] Sequence Snap | RSI-Confirmed Reversal Scalper
- **Reference File**: `web_page_text (1).txt` | **Category**: Family 3: Orderflow & Volume-Confirmed Pullback Absorption
- **Indicators & Parameters**: Consecutive Candle Sequence (1-3 reversal candles), RSI(14) Divergence, ATR
- **Core Concept**: Hunts for specific price action reversal sequences: an initial counter-trend candle followed by consecutive candles closing in the new direction, each holding above the reversal low. Validated by RSI momentum slope.
- **Exact Long Entry Rules**:
  * Reversal Candle: Bearish candle establishes a swing low.
  * Confirmation Sequence: Next 2-3 consecutive candles are bullish, with each low holding strictly above the reversal candle low.
  * RSI Confirmation: RSI(14) > 50 and sloping upward.
  * Trigger: Market entry on close of the confirmation sequence.
- **Exact Short Entry Rules**:
  * Reversal Candle: Bullish candle establishes a swing high.
  * Confirmation Sequence: Next 2-3 consecutive candles are bearish, holding below the high.
  * RSI Confirmation: RSI(14) < 50 and sloping downward.
  * Trigger: Market entry on close of sequence.
- **Stop Loss & Target Geometry**: Stop Loss: Extreme of the reversal candle. Target: 1.5R to 2.0R.
- **Crypto Failure Mode**: Naive candle sequence reversal models fail catastrophically during strong trends (taking counter-trend reversals during runaway bull/bear runs).
- **Orderflow & ML Enhancement**: Enforce strict Bitcoin 4h Macro Tide Gate: Long sequences permitted ONLY when BTC Macro Tide is BULL; Short sequences permitted ONLY when Macro Tide is BEAR.

#### [ST-16] Regime Trinity Strategy [BadRock]
- **Reference File**: `web_page_text (14).txt` | **Category**: Family 4: Multi-Regime Adaptive Systems & Advanced Execution
- **Indicators & Parameters**: Regime Classifier (Volatility Ratio, ADX, ATR), 3 Sub-Engines (Reversal, Expansion, Trend)
- **Core Concept**: Recognizes that no single entry logic works across all market conditions. Trinity classifies the active market regime into (1) Range/Rotation, (2) Breakout/Expansion, or (3) Trend/Continuation, and dynamically routes signals through specialized behavior modules.
- **Exact Long Entry Rules**:
  * Regime 1 (Range): If ATR is compressing and ADX < 20, route to Reversal Module (sweep/reclaim of support).
  * Regime 2 (Expansion): If ATR is expanding from compression, route to Breakout Module (Donchian breakout).
  * Regime 3 (Trend): If ADX > 25 and EMA 50 > EMA 200, route to Pullback Module (EMA 21 retest).
- **Exact Short Entry Rules**:
  * Mirror logic for short regimes, dynamically routing between breakdown expansion and resistance fades.
- **Stop Loss & Target Geometry**: Regime-specific: Reversal setups use tight structural stops (1.0 ATR); Trend setups use wide trailing stops (2.0 ATR).
- **Crypto Failure Mode**: High complexity and overfitting risk when switching between 3 regimes on uncalibrated indicators.
- **Orderflow & ML Enhancement**: This perfectly mirrors our Triple Trend-Following Orderflow Suite (Sleeves T1, T2, T3)! Harmonize the 3 sleeves under our fixed Portfolio Governor.

#### [ST-17] Strategy Builder & Monte Carlo Risk [BadRock]
- **Reference File**: `web_page_text (17).txt` | **Category**: Family 4: Multi-Regime Adaptive Systems & Advanced Execution
- **Indicators & Parameters**: Monte Carlo Resampling, Risk-of-Ruin Calculator, Max Drawdown Simulator
- **Core Concept**: An institutional backtesting and risk framework. Rather than reporting a single historical equity curve, it runs 1,000 Monte Carlo trade reshuffles to calculate the 95th-percentile Max Drawdown and probability of ruin under variable slippage.
- **Exact Long Entry Rules**:
  * Evaluates candidate long signals against a fixed risk budget (5,000.00 USD capital, 0.70% to 0.90% base risk).
  * Sizing Gate: Position Size = Base Risk / (Entry - Stop Loss distance in USD).
- **Exact Short Entry Rules**:
  * Evaluates candidate short signals against a fixed risk budget.
  * Enforces strict portfolio position limits (Max 2 open positions across all 11 symbols simultaneously).
- **Stop Loss & Target Geometry**: Mandatory Hard Circuit Breaker at 4.5% drawdown.
- **Crypto Failure Mode**: Retail implementations lack real taker fees and execution slippage modeling.
- **Orderflow & ML Enhancement**: Directly embedded into our Portfolio Governor (41.0 bps round-trip friction, 10x leverage cap, Drawdown Defense at 2.0%, Hard Stop at 4.5%).

#### [ST-18] Market Engine v1.3 | Dual Speed (SWING + SCALP)
- **Reference File**: `web_page_text (8).txt` | **Category**: Family 4: Multi-Regime Adaptive Systems & Advanced Execution
- **Indicators & Parameters**: Structural Trend Engine (Daily/4H), Intraday Liquidity Engine (15M/1H), VWAP
- **Core Concept**: A dual-speed trading architecture. Engine A operates on macro structure (trend following), while Engine B executes tactical scalps at key intraday orderbook liquidity levels in the direction of Engine A.
- **Exact Long Entry Rules**:
  * Engine A (Macro): Daily/4H EMA ribbon bullish + price > VWAP.
  * Engine B (Micro): Intraday pullback to liquidity sweep level with volume absorption.
- **Exact Short Entry Rules**:
  * Engine A (Macro): Macro EMA ribbon bearish + price < VWAP.
  * Engine B (Micro): Intraday rally to liquidity sweep resistance.
- **Stop Loss & Target Geometry**: Swing target: 2.5R to 4.0R; Scalp target: 1.5R.
- **Crypto Failure Mode**: Running fast intraday scalps alongside macro swings causes fee accumulation that destroys net returns.
- **Orderflow & ML Enhancement**: Unify both speeds onto the 4-Hour clock: macro structure handled by Bitcoin Macro Tide Gate; tactical execution handled by Sleeve T3 Delta Expansion.

#### [ST-19] Momentum Sequence Strategy+ [Herman]
- **Reference File**: `web_page_text (10).txt` | **Category**: Family 4: Multi-Regime Adaptive Systems & Advanced Execution
- **Indicators & Parameters**: Pure OHLC Price Action, Protected Candle Extreme, 5 Confirmation Bars
- **Core Concept**: A pure, indicator-free price action system. Identifies an initial 'Main Candle' that establishes a protected price extreme, followed by a sequence of 5 consecutive confirmation candles showing uninterrupted directional progress.
- **Exact Long Entry Rules**:
  * Main Candle: Must be a distinct bearish candle establishing a protected low.
  * Confirmation Sequence: The following 5 consecutive candles must ALL be bullish.
  * Structural Integrity: The low of every confirmation candle must remain strictly above the low of the Main Candle.
  * Progressive Momentum: Each bullish candle must close higher than the previous candle close.
  * Trigger: Market buy order on close of 5th confirmation candle.
- **Exact Short Entry Rules**:
  * Main Candle: Must be a distinct bullish candle establishing a protected high.
  * Confirmation Sequence: The following 5 consecutive candles must ALL be bearish.
  * Structural Integrity: The high of every confirmation candle must remain strictly below the high of the Main Candle.
  * Progressive Momentum: Each bearish candle must close lower than the previous candle close.
  * Trigger: Market sell order on close of 5th confirmation candle.
- **Stop Loss & Target Geometry**: Stop Loss: Placed at the extreme of the Main Candle (Low for longs, High for shorts). Target: 1.5R to 2.5R.
- **Crypto Failure Mode**: In crypto, waiting for 5 consecutive 4h candles means price has already moved 20 hours in one direction, entering right at momentum exhaustion.
- **Orderflow & ML Enhancement**: Reduce sequence requirement to 2 confirmation candles + require Volume Ratio > 1.30 and Spot CVD diff3 > 0. Filter via LightGBM.

#### [ST-20] Tokyo Drift | Session-Based VWAP Trend Strategy
- **Reference File**: `web_page_text (11).txt` | **Category**: Family 3: Orderflow & Volume-Confirmed Pullback Absorption
- **Indicators & Parameters**: Session Anchored VWAP, VWAP Slope, RSI(14), ATR(14)
- **Core Concept**: Anchors VWAP at the start of each major trading session (Asia, London, New York). Uses the slope of the anchored VWAP to determine directional bias, and executes on short-term RSI oversold/overbought resets back to the VWAP line.
- **Exact Long Entry Rules**:
  * Session Bias: Anchored VWAP slope > 0 AND Close > Anchored VWAP.
  * RSI Reset: RSI(14) pulls back below 45 without price closing below VWAP.
  * Re-expansion Trigger: RSI crosses back above 50 while candle closes bullish.
- **Exact Short Entry Rules**:
  * Session Bias: Anchored VWAP slope < 0 AND Close < Anchored VWAP.
  * RSI Reset: RSI(14) rallies above 55 without price closing above VWAP.
  * Re-expansion Trigger: RSI crosses back below 50 while candle closes bearish.
- **Stop Loss & Target Geometry**: Stop Loss: Other side of Anchored VWAP or 1.5 * ATR. Target: 2.5R.
- **Crypto Failure Mode**: Traditional forex/futures session timing fails in 24/7 crypto where volume is continuous.
- **Orderflow & ML Enhancement**: Anchor VWAP to rolling 24-hour daily boundary (6 bars on 4h clock). Add Delta Disparity (Spot Delta > 0, Futures Delta < 0) for absorption verification.

#### [ST-21] Magic Hour Blueprint (NY Open Range Breakout)
- **Reference File**: `web_page_text (23).txt` | **Category**: Family 1: Volatility Squeeze & Compression Breakouts
- **Indicators & Parameters**: Reference Range (08:12 to 09:12 EST), Session High/Low, ATR(14)
- **Core Concept**: Tracks pre-market price development in the 60 minutes prior to the New York cash open. Establishes the reference range and trades the breakout when commercial institutional volume enters.
- **Exact Long Entry Rules**:
  * Mark High and Low of the 60-minute pre-market window.
  * Trigger: Bar closes above the Magic Hour High with expanding volume.
  * Retest: Optional limit entry on retest of the broken high.
- **Exact Short Entry Rules**:
  * Mark High and Low of pre-market window.
  * Trigger: Bar closes below the Magic Hour Low with expanding volume.
  * Retest: Optional limit entry on retest of broken low.
- **Stop Loss & Target Geometry**: Stop Loss: Opposite side of the reference range. Target: 2.0R to 2.5R.
- **Crypto Failure Mode**: US equity pre-market hours have no direct structural correlation with global crypto perpetual orderflow.
- **Orderflow & ML Enhancement**: Replace pre-market window with 20-bar Donchian channel on 4h bars, requiring quiet orderflow (|cvd_z| <= 1.0) and spot accumulation.

#### [ST-22] Trend Surfer | Multi-EMA Crossover with Dynamic RSI
- **Reference File**: `web_page_text (24).txt` | **Category**: Family 2: Multi-Timeframe Trend Following & Slope Acceleration
- **Indicators & Parameters**: Fast EMA(9), Medium EMA(21), Slow EMA(50), Dynamic RSI Bands
- **Core Concept**: Classic triple moving average crossover system enhanced with dynamic RSI bands that adapt to market volatility rather than using static 70/30 levels.
- **Exact Long Entry Rules**:
  * EMA Crossover: EMA(9) crosses above EMA(21) with both above EMA(50).
  * Dynamic RSI: RSI crosses above its rolling 20-bar SMA.
  * Candle Confirmation: Bullish close above all three EMAs.
- **Exact Short Entry Rules**:
  * EMA Crossover: EMA(9) crosses below EMA(21) with both below EMA(50).
  * Dynamic RSI: RSI crosses below its rolling SMA.
  * Candle Confirmation: Bearish close below all three EMAs.
- **Stop Loss & Target Geometry**: Stop Loss: EMA(50) or 1.5 * ATR. Target: 2.5R.
- **Crypto Failure Mode**: Moving average crossovers lag significantly on 4h bars, buying tops and selling bottoms in ranging markets.
- **Orderflow & ML Enhancement**: Upgrade to Donchian price breakout + Quiet-Flow gate (|cvd_z| <= 1.0) to enter BEFORE moving averages finish crossing.

#### [ST-23] Dynamic ATR Channel Breakout
- **Reference File**: `web_page_text (4).txt` | **Category**: Family 1: Volatility Squeeze & Compression Breakouts
- **Indicators & Parameters**: Keltner ATR Channel (EMA 20 +/- 2.0 ATR), Volume SMA(20)
- **Core Concept**: Volatility envelope breakout strategy. Identifies strong directional momentum when price closes outside an ATR-scaled channel around an exponential moving average.
- **Exact Long Entry Rules**:
  * Breakout: Close crosses above EMA(20) + 2.0 * ATR.
  * Volume Spike: Volume > 1.5x Volume SMA(20).
  * Close Efficiency: Close in top 25% of candle range.
- **Exact Short Entry Rules**:
  * Breakdown: Close crosses below EMA(20) - 2.0 * ATR.
  * Volume Spike: Volume > 1.5x Volume SMA(20).
  * Close Efficiency: Close in bottom 25% of candle range.
- **Stop Loss & Target Geometry**: Stop Loss: EMA(20) line. Target: 2.5R with piecewise profit ratchet.
- **Crypto Failure Mode**: Closing 2.0 ATRs away from the EMA 20 is heavily overextended. Mean reversion pullbacks immediately hit stops.
- **Orderflow & ML Enhancement**: Enforce Non-Overextension check (|Close - EMA 20| <= 1.5 * ATR) so trades enter early in the breakout rather than at extreme exhaustion.

#### [ST-24] Volatility Compression & Breakout (VCB)
- **Reference File**: `web_page_text (6).txt` | **Category**: Family 1: Volatility Squeeze & Compression Breakouts
- **Indicators & Parameters**: Historical Volatility Ratio (HVR), Donchian Channel(20), Volume Expansion
- **Core Concept**: Calculates the ratio of short-term historical volatility (10 bars) to long-term historical volatility (50 bars). When ratio falls below 0.50 (extreme compression), prepares for explosive breakout.
- **Exact Long Entry Rules**:
  * Volatility Compression: 10-bar ATR / 50-bar ATR < 0.60.
  * Breakout Trigger: Close crosses above 20-bar Donchian High.
  * Volume Confirmation: Volume > 1.30x 20-bar volume SMA.
- **Exact Short Entry Rules**:
  * Volatility Compression: 10-bar ATR / 50-bar ATR < 0.60.
  * Breakdown Trigger: Close crosses below 20-bar Donchian Low.
  * Volume Confirmation: Volume > 1.30x 20-bar volume SMA.
- **Stop Loss & Target Geometry**: Stop Loss: Donchian Midpoint or 1.5 * ATR. Target: 2.5R.
- **Crypto Failure Mode**: Fails during fakeouts where price briefly breaches the Donchian channel then snaps back inside.
- **Orderflow & ML Enhancement**: Inject the Bar Close Efficiency Gate (>= 0.65) and require Spot CVD Slope > 0 to confirm genuine accumulation.

#### [ST-25] Toby Crabel NR7 / NR4 Volatility Contraction & Absorption Pullback
- **Reference File**: `web_page_text (27).txt` | **Category**: Family 1 & 3 Hybrid: Volatility Contraction & Absorption Pullback
- **Indicators & Parameters**: Absolute Bar Range (High - Low), Rolling 6-bar Minimum Range Min(6, Range), Inside Bar Filter (High < High[1] and Low > Low[1]), Macro EMA(200), Pullback Oscillator (CCI 10 or VWAP Z-score)
- **Core Concept**: Derived from Toby Crabel's foundational work 'Day Trading with Short Term Price Patterns'. Based on the core market invariant that extreme volatility contraction (the narrowest range in 4 or 7 bars) invariably precedes explosive volatility expansion. Operates in two distinct modes: (A) Pure Compression Breakout, and (B) Trend Pullback Absorption (NR7 printed at key dynamic support during an oversold pullback).
- **Exact Long Entry Rules**:
  * Mode A (Breakout Expansion): Current bar range is narrowest of last 7 bars (Range < Min(6, Range)). Subsequent bar breaks and closes above the NR7 High with expanding volume.
  * Mode B (Absorption Pullback): Macro Trend is Bullish (Price > EMA 200). Market pulls back into dynamic support (EMA 21 or VWAP Z < -0.50) with oversold momentum (CCI < -100). Price prints an NR4/NR7 inside bar (selling volume dries up). Trigger on break and close above the NR7 High.
- **Exact Short Entry Rules**:
  * Mode A (Breakdown Expansion): Current bar is an NR7 bar. Subsequent bar breaks and closes below the NR7 Low with expanding volume.
  * Mode B (Absorption Rally): Macro Trend is Bearish (Price < EMA 200). Market rallies into dynamic resistance with overbought momentum (CCI > +100). Price prints an NR4/NR7 inside bar. Trigger on break and close below the NR7 Low.
- **Stop Loss & Target Geometry**: Stop Loss: Opposite extreme of the NR7 bar (or 1.5 * ATR for buffer). Target: 2.0R to 2.5R with piecewise breakeven ratchet at +0.80R.
- **Crypto Failure Mode**: In crypto, naive NR7 breakouts during sideways markets suffer 70%+ failure rates because retail traders buy the top of the narrow bar right into market maker absorption. Without higher timeframe orderflow, narrow ranges frequently continue into drift decay.
- **Orderflow & ML Enhancement**: Directly powers the Two Concrete Steps to Unlock the 20/20 Pass: (1) Provides the exact micro-absorption trigger for Sleeve T2 (Trapped-Trader Absorption Pullback) when confirmed by Spot vs Futures Delta Disparity (Spot Delta > 0, Futures Delta < 0) and CVD Divergence (zc_div > 0.80); (2) Serves as the micro-regime trigger for the Altcoin Volatility/Breadth Filter.

==============================================================================================================
### 5. MANDATORY ORDERFLOW & MACHINE LEARNING UPGRADE BLUEPRINT
Every TradingView strategy above was designed as a naive technical analysis script on simple OHLCV bars. To achieve institutional positive expectancy under 41.0 bps friction, you MUST enhance each archetype using the following five orderflow and ML layers:

1. **THE BITCOIN 4-HOUR MACRO TIDE GATE (DIRECTIONAL VETO)**:
   Crypto perpetuals cannot be traded in a silo. Directional regime must be governed by Bitcoin macro structure:
   - Macro Bull: BTC EMA 50 > EMA 200 AND BTC Close > EMA 50. STRICTLY VETO ALL SHORT TRADES across all 11 assets.
   - Macro Bear: BTC EMA 50 < EMA 200 AND BTC Close < EMA 50. STRICTLY VETO ALL LONG TRADES across all 11 assets.
   - Neutral / Chop: Enable range absorption sleeves (Family 3/4); disable breakout chasing (Family 1).

2. **THE SPOT-VERSUS-FUTURES DELTA DISPARITY FILTER**:
   Eliminate retail fakeouts by cross-referencing Binance spot accumulation against futures positioning:
   - For Longs: Require positive spot CVD slope (spot_cvd.diff(4) >= 0) and CVD Z-score <= 1.0 (avoids retail exhaustion spikes).
   - For Absorption: Require Delta Disparity (Spot Delta > 0 and Futures Delta < 0) with CVD Z-score divergence (zc_div > 0.80).

3. **THE CAUSAL CVD VELOCITY CALIBRATION (FIXED DIFF OPERATOR)**:
   CRITICAL BUG FIX: Never use pct_change() on cumulative volume delta (CVD is frequently negative in crypto, which inverts the percentage change sign).
   - Use causal difference: spot_cvd_diff3 = spot_cvd[t] - spot_cvd[t-3] > 0 for longs, < 0 for shorts.

4. **THE BAR CLOSE EFFICIENCY GATE (WICK-ABSORPTION VETO)**:
   Do not enter breakouts that leave large upper or lower shadows (indicating aggressive buyers or sellers were absorbed):
   - Long Close Efficiency: (Close - Low) / (High - Low) >= 0.65.
   - Short Close Efficiency: (High - Close) / (High - Low) >= 0.65.

5. **MACHINE LEARNING META-CLASSIFIER OVERLAY (LIGHTGBM / XGBOOST)**:
   Train a shallow gradient boosted tree (max_depth <= 4, min_child_weight >= 50, L1/L2 regularization) strictly on causal in-sample features:
   - Feature Vector: [delta_z, cvd_z, vol_ratio, buy_vol_ratio, dev_ema_20, long_liq_zs, short_liq_zs, atr_ratio, close_eff].
   - Target Label: Binary classification Y = 1 if trade hits +2.0R target before -1.0R stop; Y = 0 otherwise.
   - Execution: Only execute candidate signals when P(Y = 1 | X) >= 0.62.

6. **MICROSTRUCTURE PIECEWISE RATCHET (ANTI-RETRACEMENT)**:
   - Phase 0 (Breakeven Lock): At +0.80R price gain, move stop to Entry + 0.15R (guaranteeing friction clearance).
   - Phase 1 (Profit Lock): At +1.50R price gain, move stop to Entry + 0.80R.
   - Target: Exit at +2.50R (purged legacy moonshots that retrace into stop-outs).
   - Time Decay: Exit at market if trade fails to gain +0.20R within 24 bars (96 hours).

7. **THE TWO CONCRETE STEPS TO UNLOCK THE 20/20 PASS (MANDATORY IMPLEMENTATION)**:
   - **Step 1: Activate Sleeve T2 (Trapped-Trader Absorption Pullback) for Range Regimes**:
     In low-volatility quarters where breakout count is low, Sleeve T2 must step in. Instead of chasing breakouts that fail, Sleeve T2 buys extreme liquidity sweeps at range support with spot CVD absorption (exploiting the Toby Crabel ST-25 NR4/NR7 contraction at key levels), providing 10-15 high-win-rate trades during chop markets to clear the minimum trade quota without incurring fakeout losses.
   - **Step 2: Deploy an Altcoin Volatility/Breadth Filter**:
     When rolling 100-bar ATR is in the bottom 15th percentile across the altcoin universe, disable breakout trading entirely (Sleeve T1 / Family 1) to avoid false-breakout whipsaws during market dormancy. Only permit range absorption (Sleeve T2) or high-conviction orderflow delta expansions (Sleeve T3) during these dormant periods.

==============================================================================================================
### 6. REPOSITORY & CODEBASE ARCHITECTURE REFERENCES (GIT-BASED)
You must interact directly with the production Git repository. Do not invent synthetic architectures. Load and mutate the live files:
- Repository: https://github.com/kbsingh1399/Trading.git (branches: main and arena/01a082b5-trading)
- Production Strategy Engine: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/s1_liquidation_cascade.py
- Canonical Indicators Library: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/canonical_indicators.py
- Data Contracts & Schema: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/core/schema.py
- Integrity Verification Suite: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/verification/verify_parquet_integrity.py
- Historical Pipeline Runner: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/run_historical_pipeline.py

==============================================================================================================
### 7. REQUIRED DELIVERABLES & OUTPUT FORMAT
1. **Strategy Elimination & Selection Matrix**: Rank all 25 TradingView & institutional archetypes by their mathematical viability in crypto perpetuals. Eliminate unviable retail toys; select the top 3-4 complementary archetypes.
2. **Executable Drop-In Python Module**: Provide complete, drop-in, syntax-error-free Python code implementing the selected multi-sleeve architecture with the full portfolio governor and orderflow/ML gates.
3. **Audited 20-Quarter Scorecard Table**: Output the verified console metrics across all 20 quarterly OOS windows formatted with Quarter, Period, Trades, Net R, Net USD, ROI %, MaxDD %, Win Rate %, and Status (PASS/FAIL).
4. **Zero Lookahead Attestation**: Explicitly verify the complete absence of WINDOW_CONFIGURATIONS[w_idx], test-set snooping, static result caches, or intra-bar ratchet leaks.