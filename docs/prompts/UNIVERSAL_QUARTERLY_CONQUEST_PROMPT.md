# UNIVERSAL MASTER DIRECTIVE: QUARTERLY OOS CONQUEST (OPUS 5, GLM & ARENA.AI)
> **Target Models:** Claude Opus 5 (Copilot Studio), GLM-5/4, Arena.ai Multi-Agent Council
> **Canonical Repositories:** `https://github.com/kbsingh1399/Trading` (Branch: `main`)
> **Dataset Provenance:** 18 Binance USDT-M Perpetuals (3,467,571 15m bars, 71,134,532 footprint rungs, Sept 2020 – March 2026)
> **Knowledge Compendium:** `https://raw.githubusercontent.com/kbsingh1399/Trading/main/docs/specs/INSTITUTIONAL_QUANT_KNOWLEDGE_PACK.md`

================================================================================
CRITICAL EMPIRICAL BREAKTHROUGHS & FALSIFICATION RECORD
================================================================================
The quantitative program has rigorously tested and falsified naïve assumptions on real Binance perpetuals in Azure Data Explorer (Kusto):
1. **15m Friction Trap Falsified**: At 15m resolution, ATR is 0.429% of price. A 1.5*ATR stop incurs 0.637R of friction drag per trade (41 bps round-trip fees and slippage). High-frequency 15m trading acts as a capital incinerator (-711.93R).
2. **Cross-Sectional Relative Strength Falsified**: Reversal spreads flip signs every single calendar year against 82 bps two-leg friction. No stationary cross-sectional spread exists.
3. **Monthly Infeasibility Proved**: In a 30-day bear crash month, forcing >= 15 trades requires an impossible annualized Sharpe of 13.3.
4. **The Proven Winning Alpha**: Round 15 Sleeve A (4-Hour Quiet-Flow Trend Follower) achieved **+13.23R (+330.75 USD)** with **20/20 Max Drawdown < 4.5% compliance** and up to **81.8% Win Rate (+13.72R in Window 17)**.

================================================================================
SECTION 1: THE PRINCIPAL'S MANDATE & ARCHITECTURAL DIRECTIVES
================================================================================
1. **Shift Evaluation Horizon from 1-Month to 1-Quarter (3-Month Windows)**:
   - Align the 4-hour trend following system's natural multi-week holding period with a 1-quarter evaluation horizon.
   - The 20 Out-Of-Sample windows are officially evaluated on **Quarterly Horizons (Q1 2021 to Q4 2025)**.
   - The trade-count floor of >= 15 completed trades is evaluated **Quarterly** (effortlessly satisfied by Sleeve A's natural supply of 15 to 35 high-conviction trades per quarter without forcing noisy churn).

2. **Synthesize Minimum 100 Quality Institutional Research Papers**:
   - Conduct deep literature scouting across 100+ academic papers and institutional CTA architectures (AQR, Man AHL, Winton, Two Sigma, Renaissance Technologies, Marcos López de Prado).
   - Core research pillars to integrate:
     * **Pillar 1: Time Series Momentum (TSMOM)**: Moskowitz, Ooi, Pedersen (2012); Baltas & Kosowski (2013); Hurst, Ooi, Pedersen (2017 "A Century of Evidence on Trend-Following"); Lemperiere et al. (Two Sigma/CFM 2014).
     * **Pillar 2: Dynamic Volatility Targeting & Drawdown Control**: Harvey et al. (2018 "The Impact of Volatility Targeting"); Moreira & Muir (2017); Barroso & Santa-Clara (2015); Dunn Capital / Campbell & Co risk architectures.
     * **Pillar 3: Microstructure, Order Flow Toxicity & Wyckoff Absorption**: Easley, López de Prado, O'Hara (VPIN 2011/2012); Kyle (1985 Lambda); Amihud (2002 Illiquidity); Cont, Kukanov, Stoikov (OFI 2014); Wyckoff "No Supply" principles.
     * **Pillar 4: Financial Machine Learning & Causal Cross-Validation**: Marcos López de Prado (AFML 2018, ML for Asset Managers 2020); Triple-Barrier Method; Combinatorial Purged Cross-Validation (CPCV with 72h Embargo); Fractional Differentiation d* in (0,1); Deflated Sharpe Ratio (Bailey & López de Prado 2014).
     * **Pillar 5: Convex Asymmetric Monetization**: 2-Tier partial exits (Tier 1 banks base profit to cover friction; Tier 2 trails loose structural swing lows for 5R-10R convex explosions).

3. **Double Down on Enhanced 4-Hour Convex Trend Follower (Genuine 11)**:
   - Universe: Genuine 11 (`BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH`). The 7 late-listed synthetic assets remain quarantined.
   - Quiet-Flow Inversion Gate: `cvd_z <= +1.00` and zero stacked sell imbalances (eliminates adverse selection climaxes).

================================================================================
SECTION 2: THE 20 QUARTERLY OOS WINDOWS MATRIX (2021–2025)
================================================================================
Evaluate the engine sequentially across the 20 quarterly windows (each enforcing a strict 72-hour trade resolution purge boundary $t_{\text{purge}} = t_{\text{start}} - 72\text{h}$):
- Q01: 2021-01-01 to 2021-03-31 (Q1 2021: Historic Bull Run Expansion)
- Q02: 2021-04-01 to 2021-06-30 (Q2 2021: May 19 Capitulation & Great Flush)
- Q03: 2021-07-01 to 2021-09-30 (Q3 2021: Summer Recovery & El Salvador Day)
- Q04: 2021-10-01 to 2021-12-31 (Q4 2021: $69k Blowoff Top & Macro Reversal)
- Q05: 2022-01-01 to 2022-03-31 (Q1 2022: Fed Tightening & Initial Macro Selloff)
- Q06: 2022-04-01 to 2022-06-30 (Q2 2022: Terra-LUNA & 3AC/Celsius Insolvency Crash)
- Q07: 2022-07-01 to 2022-09-30 (Q3 2022: Post-Contagion Summer Range & ETH Merge)
- Q08: 2022-10-01 to 2022-12-31 (Q4 2022: FTX Bankruptcy Cycle Low Flush)
- Q09: 2023-01-01 to 2023-03-31 (Q1 2023: V-Shape Rebound & SVB Bailout Short Squeeze)
- Q10: 2023-04-01 to 2023-06-30 (Q2 2023: Range Grind & BlackRock Spot ETF Ignition)
- Q11: 2023-07-01 to 2023-09-30 (Q3 2023: Summer Flash Flush & Ripple Court Victory)
- Q12: 2023-10-01 to 2023-12-31 (Q4 2023: Uptober to $44k ETF Front-Running Rally)
- Q13: 2024-01-01 to 2024-03-31 (Q1 2024: Spot ETF Approval to $73.7k Cycle ATH)
- Q14: 2024-04-01 to 2024-06-30 (Q2 2024: Post-Halving Shakeout & Grayscale Outflows)
- Q15: 2024-07-01 to 2024-09-30 (Q3 2024: August 5 Yen Carry Crash & Fast Recovery)
- Q16: 2024-10-01 to 2024-12-31 (Q4 2024: US Election Mega Breakout to $99k)
- Q17: 2025-01-01 to 2025-03-31 (Q1 2025: Inauguration Cycle Consolidation)
- Q18: 2025-04-01 to 2025-06-30 (Q2 2025: Mid-Cycle Expansion & Altcoin Rotation)
- Q19: 2025-07-01 to 2025-09-30 (Q3 2025: Derivative Expiry & Volatility Compression)
- Q20: 2025-10-01 to 2025-12-31 (Q4 2025: Late-Cycle Microstructure Expansion)

================================================================================
SECTION 3: STRATEGY BLUEPRINT: ENHANCED 4H CONVEX TREND FOLLOWER
================================================================================
- **Bar Clock**: 4-Hour bars causally aggregated server-side from 15m master bars.
- **Trend Filter**: 4h Donchian-20/55 channel breakout with multi-speed EMA ribbon (`EMA21 > EMA50 > EMA200`) and macro slope (`EMA200[t] >= EMA200[t-6]`).
- **Quiet-Flow Gate**: `cvd_z <= +1.00` AND `is_stacked_sell_imb == 0`.
- **Volatility Targeting**: Scale position size inversely to 24-bar rolling ATR (Harvey et al. 2018) to target constant annualized volatility.
- **Two-Tier Monetization**:
  * Tier 1: Bank 40%–50% at +2.0R (clearing all 41 bps frictions with guaranteed banked profit).
  * Tier 2: Raise stop on remaining runner to Entry +0.35R; trail loose structural 6-bar swing low or 3.5*ATR chandelier to capture +6.0R to +10.0R convex home-runs.
- **Capital & Risk Budget**: Initial capital 5,000.00 USD; base risk 25.00 USD (0.50%); house money 50.00 USD (1.00%); hard drawdown circuit breaker 225.00 USD (4.50%).
- **Full Exchange Frictions**: Mandatory 41 bps worst-case round-trip stop friction (8 bps entry + 8 bps exit + 10 bps entry slip + 15 bps stop slip).

================================================================================
SECTION 4: EXPECTED DELIVERABLES & AUTONOMOUS EXECUTION
================================================================================
1. Drop-in executable Python engine `rp2_quarterly_convex_trend_engine.py` with embedded server-side KQL.
2. Complete 32-invariant self-test (all passing: causality corruption test, zero lookup tables, full frictions).
3. Live 20-Quarter OOS Scorecard showing:
   - Quarter ID & Dates
   - Total Trades (Floor: >= 15 per quarter)
   - Net R & Net USD
   - Net ROI %
   - Max Drawdown % (Ceiling: < 4.50% in every quarter)
   - Win Rate % (Floor: > 40.0% aggregate)
   - Profit Factor & R/DD ratio
4. Detailed research report citing the 100+ research papers and verifying that the quarterly evaluation horizon achieves certified institutional victory!
