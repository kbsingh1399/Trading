# MASTER QUANTITATIVE MISSION PROMPT: TRADINGVIEW STRATEGY SUITE HARNESS
## EVALUATION, ORDERFLOW & ML ENHANCEMENT ACROSS ALL 20 QUARTERLY OOS WINDOWS (2021-2025)
## TARGET PLATFORM: CLAUDE OPUS 5 (OX ALPHA / ARENA.AI)
==============================================================================================================

### 1. MISSION DIRECTIVE & CORE CONSTRAINTS
You are acting as the Chief Quantitative Architect for an institutional crypto proprietary trading desk. You operate in a brand new chat session with zero memory, zero chat context, and zero external repository access. Every specification, formula, dataset definition, and friction model is self-contained in this prompt.

Your objective is to ingest, filter, synthesize, and rigorously backtest a suite of 24 distinct TradingView strategy archetypes extracted directly from production TradingView community strategies. You must:
1. Filter out all retail noise (unrealistic fills, zero-fee assumptions, discretionary visual indicators, repainting Pine Script functions).
2. Enhance EVERY strategy archetype with institutional orderflow features (CVD Divergence, Spot vs Futures Delta Disparity, Liquidation Z-scores, Bar Close Efficiency) and a Machine Learning meta-classifier overlay (LightGBM/XGBoost on stationary orderflow features).
3. Execute a strict 20-Quarter Out-of-Sample (OOS) Walk-Forward backtest (Q1 2021 - Q4 2025) on the Certified Genuine 11 Binance USDT-M Perpetuals on a causal 4-Hour clock under full 41.0 bps round-trip taker frictions.
4. Identify the winning strategy archetypes and combine them into a multi-sleeve portfolio that achieves a verified 20/20 PASS across all 20 quarters.

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
### 4. DECONSTRUCTED TRADINGVIEW STRATEGY SUITE (24 ARCHETYPES)
The 24 extracted TradingView strategies have been filtered of web UI noise and categorized into 4 core architectural families:

#### Family 1: Volatility Squeeze & Compression Breakouts
- **Power Surge | BB Momentum Squeeze Release** (Ref: `web_page_text (22).txt`)
  * Core Mechanism: Power Surge trades the moment volatility compression turns into directional momentum. It combines two mechanisms: a Bull/Bear Power Oscillator that measures how forcefully price is pushing beyond its own Bollinger Band envelope (0–100 scale), and a classic BB-inside-Keltner-Channel squeeze filter that identifies periods of volatility contraction. Entries only trigger when the oscillator crosses above/below a threshold within a defined window after a squeeze has just released — filtering out rand
  * Key Indicators: Bollinger Bands, ATR, Keltner, Momentum
- **CRT SNIPER** (Ref: `web_page_text (19).txt`)
  * Core Mechanism: CRT SNIPER is a rules-based futures strategy built around Candle Range Theory (CRT) and designed to capture directional expansion after important session-based range formations. Default configuration: CRT SNIPER has been developed and optimized primarily for MNQ on the 1-minute chart. Other instruments and timeframes may behave differently and should be tested independently before use. The strategy combines higher-timeframe directional context with lower-timeframe confirmation and structured tra
  * Key Indicators: Fair Value Gap, Breakout
- **Daybreak Strategy [Achira Meegasthanne]** (Ref: `web_page_text (20).txt`)
  * Core Mechanism: Daybreak Strategy is an Opening Range Breakout (ORB) strategy designed to capture potential directional moves based on the high and low of the 9:00 opening candle on the 1-hour timeframe. The strategy places breakout stop orders above and below the opening range, with the entry distance dynamically adjusted using ATR and the selected Sensitivity. The strategy is specifically designed to operate on the 1-hour timeframe. The opening range is taken from the 9:00 candle, making the 1H timeframe impo
  * Key Indicators: ATR, Breakout
- **Execution-Aware Trend [BSL]** (Ref: `web_page_text (15).txt`)
  * Core Mechanism: Execution-Aware Trend is a deliberately ordinary trend-and-breakout strategy whose main product is visible testing discipline. It answers “what did this exact ruleset simulate after declared costs, next-tick execution and a fixed sample split?” It does not predict the next move and does not claim an edge. This is an original BarState Labs implementation created from an independent written specification. It does not reproduce another publication’s source, Trend qualification uses a fast and slow 
  * Key Indicators: EMA, ATR, Breakout
- **DNSE VN301!, BB-SMA Trend Following** (Ref: `web_page_text (3).txt`)
  * Core Mechanism: "Bollinger Bands Breakout with SMA Trend Filter" is a volatility-based trend-following strategy designed to capture strong directional price movements when price breaks beyond its recent volatility range. The strategy uses Bollinger Bands with a default SMA(20) basis and 2.0 standard deviations to identify bullish breakouts above the upper band and bearish breakouts below the lower band. To improve signal quality, the strategy combines Bollinger Band breakouts with a mandatory SMA(200) trend fil
  * Key Indicators: SMA, Bollinger Bands, Breakout

#### Family 2: Multi-Timeframe Trend Following & Slope Acceleration
- **Gradient Ribbon | EMA Ribbon Slope-Acceleration System** (Ref: `web_page_text (25).txt`)
  * Core Mechanism: Gradient Ribbon | EMA Ribbon Slope-Acceleration System Most EMA ribbon strategies only check if the moving averages are stacked in order — but a ribbon can stay stacked long after the actual trend has run out of steam. Gradient Ribbon looks past the stacking and measures the slope of each EMA directly, only signaling when the ribbon is actively accelerating apart. It catches trend ignition early and flags deceleration before the EMAs ever cross. 5-EMA ribbon (8/13/21/34/55) with per-line slope c
  * Key Indicators: RSI, EMA, ATR, Momentum
- **Bitcoin SuperFlip | Supertrend EMA Trend-Following Strategy** (Ref: `web_page_text (9).txt`)
  * Core Mechanism: Bitcoin SuperFlip | Supertrend EMA Trend-Following Strategy This is a trend-following, not mean-reversion system. It will have a lower win rate than a typical scalping strategy, and that is by design — trend systems make their money from a smaller number of large winning trades that outweigh a higher frequency of small losses. Supertrend (ATR-based) tracks the prevailing trend direction and flips when price crosses its dynamic ATR band. This flip is the core trigger for both entries and exits. E
  * Key Indicators: EMA, ATR, Supertrend, ADX
- **DNSE VN301!, SMA ADX/DI Trend Following Strategy** (Ref: `web_page_text (21).txt`)
  * Core Mechanism: DNSE VN301!, SMA ADX/DI Trend Following Strategy "SMA ADX DI Trend Following" is a trend-following strategy designed to identify and capture directional price movements by combining SMA slope analysis with ADX trend-strength confirmation and DI directional signals. The strategy uses SMA(89) to determine the primary trend direction, while ADX(14) confirms that the market has sufficient trend strength and DI identifies whether bullish or bearish pressure is dominant. By requiring agreement between
  * Key Indicators: SMA, ADX, Momentum
- **Universal Aggressive Trend MACD v3.3 - Trailing TP** (Ref: `web_page_text (5).txt`)
  * Core Mechanism: Universal Aggressive Trend MACD v3.3 - Trailing TP Universal Aggressive Trend MACD v3.3 - Trailing TP This strategy is an automated trend-following system designed to catch strong price movements while filtering out choppy, sideways markets. Think of it as a sniper that waits for momentum to shift in the direction of the overall trend, enters the trade, and then uses a smart profit-locking mechanism to squeeze as much gain as possible out of the move. The system relies on a few core mechanics to
  * Key Indicators: MACD, EMA, ATR, ADX, Momentum
- **Asymmetric Trend Strategy [QuantAlgo]** (Ref: `web_page_text (7).txt`)
  * Core Mechanism: The Asymmetric Trend Strategy is a trend-following system built around an intentional imbalance between how a move is followed and what it takes to end it. Most trailing methods place the same margin on either side of price, which forces a single compromise: track tightly and ordinary noise closes healthy positions early, or track loosely and return a large share of the advance at the exit. This script separates those two jobs and sizes them independently, drawing its reference up close behind p
  * Key Indicators: 

#### Family 3: Orderflow & Volume-Confirmed Pullback Absorption
- **EMA Pullback Trend Continuation Strategy with Volume and Momentu** (Ref: `web_page_text (16).txt`)
  * Core Mechanism: EMA Pullback Trend Continuation Strategy with Volume and Momentu Most trend-following strategies share the same flaw: they enter on breakouts. A stock breaks above resistance, the moving average crosses over, the indicator fires — and the entry price is at the top of the move that just happened. The trader is buying strength into a market that has already moved. When the move pauses or retraces, as nearly every trending move does, the position immediately goes underwater. The trader who waited f
  * Key Indicators: RSI, EMA, ATR, Momentum, Breakout, Pullback
- **Trend Trigger | EMA Trend Filter + MTF Stochastic Entry with ATR** (Ref: `web_page_text (18).txt`)
  * Core Mechanism: Trend Trigger | EMA Trend Filter + MTF Stochastic Entry with ATR This strategy combines two proven, independent mechanisms rather than inventing a new indicator: a slow-moving EMA trend filter decides which direction is permitted, and a higher-timeframe-confirmed stochastic oscillator decides when to actually enter. Trend and timing are handled by separate logic layers so each does one job well, instead of stacking multiple overlapping conditions that rarely align. Trend permission (EMA 38/62): 
  * Key Indicators: EMA, ATR, Stochastic, Momentum, Pullback
- **Golden Trident | Swing-Anchored VWAP Trend System** (Ref: `web_page_text (13).txt`)
  * Core Mechanism: Golden Trident | Swing-Anchored VWAP Trend System Golden Trident is a long-only, daily-timeframe trend-following strategy built specifically for XAUUSD (spot gold). Rather than relying on a lagging moving-average crossover or a single volatility band, it reads market structure directly — tracking swing highs and lows to determine trend direction — and pairs that with a volume-weighted anchor price that resets at every structural trend change. This gives the strategy a "fair value" reference line
  * Key Indicators: EMA, ATR, VWAP
- **Momentum Trail Strategy [BadRock]** (Ref: `web_page_text (12).txt`)
  * Core Mechanism: Momentum Trail Strategy is a confirmed-bar momentum strategy with risk-based position sizing and intrabar protective exits. The entry model is intentionally compact. It combines three established technical-analysis concepts, but each component performs a different task: • Session VWAP slope acts as a directional session filter. • RSI acts as a headroom veto so the strategy does not accept every already-extended momentum event. After a confirmed signal, the strategy submits one market entry and s
  * Key Indicators: RSI, MACD, VWAP, Momentum
- **Sequence Snap | RSI-Confirmed Reversal Scalper** (Ref: `web_page_text (1).txt`)
  * Core Mechanism: Sequence Snap | RSI-Confirmed Reversal Scalper Explanation This strategy hunts for a specific price-action pattern: a candle that closes against the prevailing short-term move, followed by a run of consecutive candles pushing hard in the opposite direction — each one holding above (or below) the reversal candle's extreme. Once that shape completes, RSI is checked to confirm real momentum is behind the move rather than just noise. Entries use a single fixed stop (placed at the reversal candle's l
  * Key Indicators: RSI, MACD, EMA, SMA, Bollinger Bands, ATR, VWAP, Supertrend, ADX, Stochastic, Keltner, Fair Value Gap, Momentum, Breakout, Pullback, Monte Carlo

#### Family 4: Multi-Regime Adaptive & Structural Systems
- **Regime Trinity Strategy [BadRock]** (Ref: `web_page_text (14).txt`)
  * Core Mechanism: Regime Trinity Strategy [BadRock] is an adaptive intraday strategy built around one idea: different market conditions should not be traded with the same entry logic. Instead of forcing a single setup across every environment, Trinity evaluates the current regime and routes confirmed opportunities through three behavior families: • Reversal — sweep/reclaim behavior around recent structure, mainly when the market is rotating or range-like. • Expansion — compression, breakout and retest behavior as
  * Key Indicators: ATR, Momentum, Breakout
- **Strategy Builder - Backtest, Risk & Monte Carlo [BadRock]** (Ref: `web_page_text (17).txt`)
  * Core Mechanism: Strategy Builder - Backtest, Risk & Monte Carlo [BadRock] ====================================================================== The script can work as a standalone strategy using its built-in BadRock setup families, or as an execution/backtest layer for compatible external indicators. Its purpose is not to claim that one fixed signal model works on every market. The purpose is to make signal ideas comparable under the same execution rules and to expose how much of a result comes from the signal
  * Key Indicators: EMA, ATR, VWAP, Breakout, Pullback, Monte Carlo
- **Market Engine v1.3 | Independent SWING + Fast SCALP** (Ref: `web_page_text (8).txt`)
  * Core Mechanism: Market Engine v1.3 | Independent SWING + Fast SCALP Market Engine v1.3 | Independent SWING + Fast SCALP Two independent engines. Four clear signals. One organized trading workflow. Built for NQ and MNQ futures, it separates longer intraday opportunities from short-term momentum shifts—helping you understand not just the direction of a signal, but the type of trade it represents. Identifies a bullish structural opportunity supported by multiple confirmations. Identifies a bearish structural oppor
  * Key Indicators: ATR, VWAP, Momentum
- **Momentum Sequence Strategy+ [Herman]** (Ref: `web_page_text (10).txt`)
  * Core Mechanism: Momentum Sequence Strategy [Herman] is an open-source, rules-based price-action strategy designed to test momentum continuation following a defined candle sequence. The strategy does not use moving averages, oscillators, volume indicators, or higher-timeframe data. Its signals are derived entirely from the relationship between consecutive OHLC candles. The objective is to identify situations where an initial candle establishes a protected price extreme and is followed by a sequence of candles sh
  * Key Indicators: Momentum

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
1. **Strategy Elimination & Selection Matrix**: Rank all 24 TradingView archetypes by their mathematical viability in crypto perpetuals. Eliminate unviable retail toys; select the top 3-4 complementary archetypes.
2. **Executable Drop-In Python Module**: Provide complete, drop-in, syntax-error-free Python code implementing the selected multi-sleeve architecture with the full portfolio governor and orderflow/ML gates.
3. **Audited 20-Quarter Scorecard Table**: Output the verified console metrics across all 20 quarterly OOS windows formatted with Quarter, Period, Trades, Net R, Net USD, ROI %, MaxDD %, Win Rate %, and Status (PASS/FAIL).
4. **Zero Lookahead Attestation**: Explicitly verify the complete absence of WINDOW_CONFIGURATIONS[w_idx], test-set snooping, static result caches, or intra-bar ratchet leaks.