# UNIVERSAL MASTER DIRECTIVE: TRIPLE TREND-FOLLOWING ORDERFLOW SUITE (ROUND 18: 20/20 OOS NON-STOP MANDATE)
> **Target Frontier Models:** Claude Opus 5 (Copilot Studio / Ox Alpha), GLM-5/4 (Zhipu AI), Arena.ai Multi-Agent Council
> **Canonical GitHub Repository:** `https://github.com/kbsingh1399/Trading` (Branch: `main` & `arena/01a082b5-trading`)
> **Knowledge Compendium:** `https://raw.githubusercontent.com/kbsingh1399/Trading/main/docs/specs/INSTITUTIONAL_QUANT_KNOWLEDGE_PACK.md`
> **Kusto Data Cluster:** `https://kvc-u9tczy1a0qyc38exr3.northeurope.kusto.windows.net`
> **Data Ingestion URL:** `https://ingest-kvc-u9tczy1a0qyc38exr3.northeurope.kusto.windows.net`
> **Evaluation Horizon:** 20 Non-Overlapping Quarterly Windows (Q1 2021 to Q4 2025)
> **Currency Unit:** Strict institutional USD (zero dollar symbols used)

================================================================================
EXECUTIVE MANDATE & THE ROUND 18 NON-STOP DIRECTIVE (ALL 20/20 PASS MANDATORY)
================================================================================
You are the Lead Quantitative Architect and Chief Investment Officer. 

CRITICAL DIRECTIVE: YOU ARE STRICTLY FORBIDDEN FROM STOPPING, HALTING, OR PROPOSING RELAXATIONS OF THE TARGETS (e.g. suggesting +2.00% ROI). 
Target relaxation is CATEGORICALLY REJECTED. The institutional requirement remains inviolable:
- Net ROI > +10.00% (+500.00 USD net on 5,000.00 USD capital) in EVERY single quarter.
- Max Drawdown < 4.50% (225.00 USD hard circuit breaker) in EVERY single quarter.
- Win Rate > 40.0% aggregate.
- Completed Trades >= 15 per quarter across all sleeves combined.
- ALL 20 OUT OF 20 OOS QUARTERS MUST PASS JOINTLY.

You are ordered to execute an autonomous, continuous loop of causal refinement and backtesting until ALL 20/20 QUARTERS SIMULTANEOUSLY PASS THE CRITERIA. Do NOT stop after Round 17's 1/20 pass. Your own Round 17 autopsy uncovered the exact structural defects causing the shortfall. You must now implement the direct mathematical solutions to those defects and iterate until 20/20 victory is achieved.

================================================================================
THE FIVE EMPIRICAL DEFECTS FROM ROUND 17 & THEIR IMMEDIATE MATHEMATICAL CURES
================================================================================
In Round 17, you proved that the underlying raw signals produce strong positive alpha (+224.34 R, +0.0639 R/trade raw, with T1 at +0.1618 R and T3 at +0.2348 R), but the portfolio simulation degraded to -26.17 R under naive allocation. You identified five exact defects. Here are their mandatory institutional cures:

1. **CURE DEFECT 1: ELIMINATE THE SLEEVE T2 SLOT-HOG TRAP**:
   - *Empirical Finding*: Sleeve T2 supplied 70.2% of all signals at an anemic +0.0159 R/trade, hogging both concurrency slots and starving high-expectancy sleeves T1 (+0.1618 R/trade) and T3 (+0.2348 R/trade). Dropping T2 alone converted net R from -26.17 R to +35.63 R!
   - *Mandatory Fix*: 
     * EITHER completely purge T2 and operate a dual-sleeve high-expectancy suite (T1 Quiet-Flow Breakout + T3 Delta Momentum Expansion).
     * OR implement an **Edge-Per-Slot Concurrency Allocator**: Concurrency slots 1 and 2 are strictly reserved for high-expectancy sleeves T3 and T1. T2 signals are vetoed whenever any T1/T3 signal is active or has fired within the trailing 3 bars.
     * OR re-engineer T2 into a high-conviction **Trapped-Short Climax Reversal** requiring extreme multi-bar volume exhaustion (volume > 2.5x mean) and verified stacked footprint absorption, cutting signal count by 80% while raising expectancy to > +0.25 R/trade.

2. **CURE DEFECT 2: TWO-SIDED SYMMETRIC TREND FOLLOWING (SOLVING 2022 BEAR REGIME)**:
   - *Empirical Finding*: 2022 suffered -0.4596 R/trade because long-only trend-following bled against secular macro bear cascades (LUNA crash Q2 2022, FTX collapse Q4 2022). Trend following cannot be long-only over a 5-year crypto horizon!
   - *Mandatory Fix*: 
     * **Symmetric Two-Sided Trend Following**: When 4h EMA 50 < EMA 200 and EMA 200 slope is negative (macro downtrend), trigger SHORT signals:
       - Short Quiet-Flow Breakdown (Donchian lower channel breakdown, |cvd_z| <= 1.00, zero stacked buy imbalances, spot CVD slope negative).
       - Short Delta Momentum Expansion (relative volume > 1.5x, sell_vol / (buy_vol + sell_vol) >= 0.513, downward price expansion).
     * **Macro Bear Long Veto**: When 4h EMA 50 < EMA 200 by more than 1.5*ATR, ALL long pullbacks and long breakouts are strictly vetoed. This single causal rule eliminates 2022 long whipsaws and converts 2022 from -0.46 R into positive Crisis Alpha (Greyserman & Kaminski 2014).

3. **CURE DEFECT 3: DIMENSIONLESS VOLUME NORMALIZATION**:
   - *Empirical Finding*: The priority key `volume / ATR` scaled as 1/price, distorting cross-asset ranking (TRX showed 5.3e11 vs BCH 1.2e4 purely due to nominal price scale).
   - *Mandatory Fix*: Use strictly dimensionless relative volume:
     `rel_vol = volume / rolling_mean_20(volume)`
     Prioritize concurrent signals by: `rel_vol * sleeve_historical_edge`.

4. **CURE DEFECT 4: FROZEN CONFIG F ANTI-SUFFOCATION RATCHET**:
   - *Empirical Finding*: The tight baseline ratchet (+0.80R -> +0.35R) suffocated winning trades (+0.031 R/trade). The design-frozen Config F delivered 8.6x more edge (+0.2682 R/trade, 52.3% win rate).
   - *Mandatory Fix*: Lock in Config F across all sleeves:
     * Initial Stop: 2.5 * ATR (or structural swing boundary).
     * Phase 0 Ratchet: At +1.20R price gain, move stop to Entry +0.30R (guaranteeing profit and clearing 41 bps friction).
     * Phase 1 Ratchet: At +2.20R price gain, move stop to Entry +1.10R.
     * Phase 2 Ratchet: At +3.50R price gain, move stop to Entry +2.40R.
     * Profit Target: +6.00R (allows convex trend runners to capture full drift).
     * Time Decay Exit: Exit at market if trade fails to reach +0.20R within 24 bars (96 hours).

5. **CURE DEFECT 5: CALIBRATED QUANTILE ANCHORS**:
   - *Empirical Finding*: The original directive's `buy_vol / (buy_vol + sell_vol) >= 0.60` was above the 99th percentile (p99 = 0.5909) due to the Central Limit Theorem across 16 15m bars, starving T3 supply to n=6.
   - *Mandatory Fix*: Anchor delta dominance to the design-set 75th percentile:
     `buy_share >= 0.513` for longs (`sell_share >= 0.513` for shorts). At p75, T3 yielded +3.09 ATR drift and +0.2348 R/trade!

================================================================================
SECTION 1: THE TRIPLE TREND-FOLLOWING ORDERFLOW SUITE SPECIFICATION
================================================================================
You must implement the following refined, two-sided 4-Hour Trend-Following Strategy Suite:

### STRATEGY 1: TWO-SIDED QUIET-FLOW STRUCTURAL BREAKOUT (SLEEVE T1)
- **Trend Filter**: 
  * Long: 4h Donchian 20-period upper channel breakout, EMA 21 > EMA 50 > EMA 200, EMA 200 slope >= 0.
  * Short: 4h Donchian 20-period lower channel breakdown, EMA 21 < EMA 50 < EMA 200, EMA 200 slope <= 0.
- **Orderflow Inversion Gate**:
  * Normalized CVD Z-Score: `|cvd_z| <= 1.00` (avoids retail climax exhaustion).
  * Footprint Ladder: Zero adverse stacked imbalances (`stacked_sell == 0` for longs; `stacked_buy == 0` for shorts).
  * Spot CVD Confirmation: Spot CVD ROC is positive for longs, negative for shorts.

### STRATEGY 2: MACRO BEAR EXPANSION & STRUCTURAL BREAKDOWN (SLEEVE T2 - RE-ENGINEERED)
- **Economic Rationale**: Replaces the low-expectancy long pullback trap. Operates as a specialized Crisis Alpha sleeve capturing violent liquidation flushes during macro bear regimes (e.g. 2022).
- **Trend Filter**: 4h EMA 50 < EMA 200 by >= 1.0*ATR, EMA 200 slope < 0 over trailing 12 bars (3 days).
- **Orderflow Breakdown Gate**:
  * Liquidation Cascade / Trap: Long liquidations spike (`long_liq_zs >= 1.50`) as leveraged longs are forced to liquidate into bids.
  * Orderflow Imbalance: Footprint prints stacked sell imbalances (`stacked_sell == 1` across >= 3 contiguous rungs).
  * Net Negative Delta: 4h delta is strongly negative (`net_cvd < 0` and `delta_z < -1.00`).
  * Price Action: Invalidation stop placed tightly above the breakdown candle high (+1.5*ATR max).

### STRATEGY 3: INSTITUTIONAL ACCUMULATION & DELTA MOMENTUM EXPANSION (SLEEVE T3)
- **Trend Filter**: Active 4h trend (EMA 50 > EMA 200 for longs; EMA 50 < EMA 200 for shorts).
- **Orderflow Inversion Gate**:
  * Relative Volume Expansion: 4h Bar Volume expands > 1.50x relative to its rolling 20-bar mean (`volume / mean20(volume) >= 1.50`).
  * Delta Dominance: Calibrated p75 threshold: `buy_vol / (buy_vol + sell_vol) >= 0.513` for longs (`sell_vol / (buy_vol + sell_vol) >= 0.513` for shorts).
  * CVD Velocity: Spot CVD ROC confirms direction (`spot_cvd_roc > 0` for longs; `< 0` for shorts).
  * Non-Overextended Geometry: Entry price is within 1.50*ATR of the 20 EMA.

================================================================================
SECTION 2: PORTFOLIO CONCURRENCY & CAPITAL RISK BUDGET
================================================================================
1. **Initial Portfolio Capital**: 5,000.00 USD.
2. **Fixed Risk Budgeting per Trade**:
   - Base Risk: 35.00 USD (0.70% of initial capital).
   - House Money Risk: 80.00 to 100.00 USD (unlocked when net cumulative closed profit exceeds +50.00 USD).
   - Drawdown Defense Risk: 15.00 to 20.00 USD (armed whenever open/closed drawdown exceeds 2.00% / 100.00 USD).
   - Hard Drawdown Circuit Breaker: 4.50% (225.00 USD).
3. **Edge-Weighted Portfolio Concurrency Gate**:
   - Maximum 2 open positions across ALL 11 assets simultaneously.
   - Prioritize candidates by: `sleeve_priority_weight * (volume / rolling_mean_20(volume))` where T3 weight = 1.5, T1 weight = 1.2, T2 weight = 1.0.
4. **Full Exchange Frictions**:
   - Mandatory 41 bps worst-case round-trip stop friction (8 bps entry + 8 bps exit + 10 bps entry slippage + 15 bps stop slippage).

================================================================================
SECTION 3: THE 20 QUARTERLY OOS WINDOWS MATRIX (2021–2025)
================================================================================
Evaluate the multi-sleeve engine sequentially across all 20 quarterly windows, enforcing a strict 72-hour trade resolution purge boundary ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$):
- Q01: 2021-01-01 to 2021-03-31 (Q1 2021: Historic Bull Run Expansion)
- Q02: 2021-04-01 to 2021-06-30 (Q2 2021: May 19 Capitulation & Great Flush)
- Q03: 2021-07-01 to 2021-09-30 (Q3 2021: Summer Recovery & El Salvador Day)
- Q04: 2021-10-01 to 2021-12-31 (Q4 2021: 69k USD Blowoff Top & Macro Reversal)
- Q05: 2022-01-01 to 2022-03-31 (Q1 2022: Fed Tightening & Initial Macro Selloff)
- Q06: 2022-04-01 to 2022-06-30 (Q2 2022: Terra-LUNA & 3AC/Celsius Insolvency Crash)
- Q07: 2022-07-01 to 2022-09-30 (Q3 2022: Post-Contagion Summer Range & ETH Merge)
- Q08: 2022-10-01 to 2022-12-31 (Q4 2022: FTX Bankruptcy Cycle Low Flush)
- Q09: 2023-01-01 to 2023-03-31 (Q1 2023: V-Shape Rebound & SVB Bailout Short Squeeze)
- Q10: 2023-04-01 to 2023-06-30 (Q2 2023: Range Grind & BlackRock Spot ETF Ignition)
- Q11: 2023-07-01 to 2023-09-30 (Q3 2023: Summer Flash Flush & Ripple Court Victory)
- Q12: 2023-10-01 to 2023-12-31 (Q4 2023: Uptober to 44k USD ETF Front-Running Rally)
- Q13: 2024-01-01 to 2024-03-31 (Q1 2024: Spot ETF Approval to 73.7k USD Cycle ATH)
- Q14: 2024-04-01 to 2024-06-30 (Q2 2024: Post-Halving Shakeout & Grayscale Outflows)
- Q15: 2024-07-01 to 2024-09-30 (Q3 2024: August 5 Yen Carry Crash & Fast Recovery)
- Q16: 2024-10-01 to 2024-12-31 (Q4 2024: US Election Mega Breakout to 99k USD)
- Q17: 2025-01-01 to 2025-03-31 (Q1 2025: Inauguration Cycle Consolidation)
- Q18: 2025-04-01 to 2025-06-30 (Q2 2025: Mid-Cycle Expansion & Altcoin Rotation)
- Q19: 2025-07-01 to 2025-09-30 (Q3 2025: Derivative Expiry & Volatility Compression)
- Q20: 2025-10-01 to 2025-12-31 (Q4 2025: Late-Cycle Microstructure Expansion)

================================================================================
SECTION 4: EXECUTION MANDATE & NON-STOP AUTONOMOUS PROTOCOL
================================================================================
1. **Continuous Execution**: You must run the revised architecture against the dataset and iterate until you reach a clean 20/20 joint pass.
2. **Deliverables**:
   - `rp3_trend_following_orderflow_engine.py`: Updated python engine with all cures implemented.
   - `rp3_round18_oos_scorecard.csv`: Complete 20-quarter scorecard demonstrating Net ROI > +10.00%, MaxDD < 4.50%, Win Rate > 40.0%, Trades >= 15 for ALL 20 quarters.
   - `RP3_ROUND18_REPORT.md`: Comprehensive engineering report detailing how two-sided trend-following and edge-per-slot allocation resolved the 2022 bear drag and achieved 20/20 institutional victory.
