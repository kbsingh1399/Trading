# OPUS 5 MASTER DIRECTIVE: AUTONOMOUS RESEARCH & QUANTITATIVE BLUEPRINT TO CRACK ALL 20 OOS WINDOWS (DO NOT STOP UNTIL 20/20 PASS)

Opus 5, your Round 14 forensic investigation is the most rigorous, scientifically honest, and illuminating breakthrough of this entire project.
By measuring on real Kusto data instead of fabricating, you isolated the exact mathematical pathology:
1. **The Orderflow Gate Triples the Raw Edge**: Raw breakouts drift +0.57 ATR; your footprint gate lifts that to +1.92 ATR (96 bars) and +3.14 ATR (192 bars). The edge is real!
2. **The 15m Geometry & Friction Trap**: On 15m bars, ATR is only ~0.31% of price, making 41 bps friction consume 0.22R to 1.02R of every trade, while a tight 2.2*ATR chandelier at wide stops becomes a 0.37R choke that hit 4R in only 3.08% of trades.
3. **Gated Shorts are Anti-Predictive**: Price rose 1.14 ATR against them across regimes.

You are now officially commanded by the Principal to **build a system that cracks all 20 Out-Of-Sample windows, and DO NOT STOP until all 20 windows pass.**

You have:
- **Kusto Query MCP Server**: For lightning-fast server-side KQL execution and backtesting on real data.
- **GitHub MCP Server**: Repository `kbsingh1399/Trading` and `kbsingh1399/Engine` (branch: main).
- **Web Search Tool**: Enabled in your environment ("Search all websites").

---

## 1. Mandatory Research & Scouting Directive (Scout the Entire Ecosystem)

You are instructed to use your live search capabilities to scout across the entire spectrum of quantitative literature, institutional hedge fund blueprints, and top-tier crypto retail models:

### 1.1 Institutional Research & Literature (Search Academic & Quant Papers)
- **AQR Capital Management / Moskowitz, Ooi, Pedersen**: "Time Series Momentum" (TSMOM) across cross-sectional volatility-scaled crypto regimes.
- **Marcos López de Prado (De Prado)**:
  * *Meta-Labeling*: Use your orderflow breakout as the primary sign classifier, then train a shallow secondary model to predict *trade size / trade execution probability* to filter false entries.
  * *Triple-Barrier Method with Volatility-Adjusted Horizons*: Replace fixed bar decay with dynamic vertical time-barriers anchored to realized volatility.
- **Easley, López de Prado, O'Hara**: *Volume-Synchronized Probability of Toxicity (VPIN)* and Order Flow Imbalance (OFI) to detect toxic market maker inventory flushes.
- **Trend-Following CTAs (Man AHL, Winton, Dunn Capital)**: Multi-speed trend filtering, volatility targeting, and asymmetric skew extraction.

### 1.2 Retail Space & Practitioner Quantitative Setups
- **Multi-Timeframe Anchored VWAP (AVWAP) & Value Area Breakouts**: Long breakouts from Weekly/Monthly Developing Value Area High (VAH) confirmed by Delta expansion.
- **Wyckoff Jump-Across-the-Creek (JAC) & Absorption Breakouts**: Re-accumulation range breaks where high volume produces no price rejection.
- **Institutional Smart Money Concepts (SMC)**: High-timeframe Liquidity Sweeps with Lower-Timeframe Market Structure Shifts (MSS) and Fair Value Gap (FVG) entries.

---

## 2. Critical Architectural Redesign Mandates (Resolving the 3 Conflicts)

To eliminate the friction choke and mathematically open the path to passing all 20 windows:

### 2.1 Contract Conflict #1 Resolved — Target vs Mean Realized R
- `min_r_multiple: 4` in target_oos_criteria.json specifies the **Take-Profit Target Barrier on winning runner distributions** (gross >= 4.0R, scaling to 6R-8R on liquidation bursts).
- It does NOT require mean realized R of the entire pooled distribution (which is mathematically bounded by win rate). A strategy with 45% win rate, 0.40R average win, and -0.20R average loss is overwhelmingly profitable!

### 2.2 Bar Clock & Multi-Timeframe Escalation (Crush the Friction Ratio)
- As you recommended, escalate the primary structural clock to **1-Hour (or 4-Hour)**, or employ **Multi-Timeframe Nesting**:
  * Macro Trend & Donchian / Volatility Channels evaluated on 1h bars (where ATR is ~1.2% - 2.5% of price).
  * At 1.5% ATR, 41 bps friction is only **0.07R - 0.10R** (eliminating 85% of friction drag!).
  * Microstructure Entry & Footprint confirmation triggered on 15m orderflow.

### 2.3 Directional Asymmetry (Long Dominance / Restricted Shorting)
- Long breakouts have structural drift (+3.14 ATR at 192 bars with your gate).
- Drop unconstrained shorting. Either:
  * **Long-Only Engine**: Trade high-conviction long momentum and liquidation absorption.
  * **Regime-Gated Shorts**: Shorts permitted ONLY during confirmed macro bear cascades (e.g. BTC daily 200 EMA slope negative, net positive funding where retail is trapped long, and `short_liq_zs < 0.50`).

### 2.4 Decouple the Ratchet & Introduce 2-Tier Profit Taking
- Scrap the fixed 2.2*ATR trail that choked runners at 0.37R.
- Implement **Asymmetric Partial Monetization**:
  * **Tier 1 (Base Profit Banked)**: Take 40% to 50% profit at +1.5R to +2.0R. This covers all round-trip frictions and guarantees that every runner is net-positive in real USD.
  * **Tier 2 (Convex Macro Runner)**: Move stop on remaining position to Entry +0.35R. Trail remaining 50% runner using a loose structure trail (e.g. trailing the lowest low of the last 6 1-hour bars, or 3.5*ATR), giving 5R-8R runners room to ride macro waves.

### 2.5 Genuine 11 Universe (100% Certified)
- Trade strictly the **Genuine 11** universe: `BTC, ETH, XRP, BNB, DOGE, ADA, TRX, LINK, DOT, LTC, BCH`.
- Maintain `orderflow_cover = 1.0` and zero synthetic data.

---

## 3. Pass Criteria Across All 20 OOS Windows

Pass all 20 Out-Of-Sample regimes in `oos_windows_20.json`:
- **Net ROI per 1-Month Window**: > +10.0% (target > +20.0% / +1,000.00 USD on 5,000.00 USD capital)
- **Maximum Drawdown**: < 4.5% (225.00 USD hard circuit breaker)
- **Win Rate**: > 40.0%
- **Completed Trades**: >= 15 completed trades per window
- **Real Institutional Frictions**: Full 41 bps worst-case stop friction (8 bps taker entry, 8 bps taker exit, 10 bps entry slip, 15 bps stop slip).

---

## 4. Autonomous Execution Loop (Do Not Stop Until Cracked)

Opus, execute this research and engineering loop inside your sandbox and Kusto connection:
1. Scout the literature via web search for crypto multi-timeframe orderflow trend strategies.
2. Ingest the 1-hour / multi-timeframe bar data from Kusto.
3. Test candidate architectures on non-OOS design months to tune barrier economics and partial-exit geometry.
4. Run the full 20-window walk-forward validation in KQL.
5. If any window fails, adjust the macro regime filter or friction amortization, and re-test.
6. **Deliver**:
   - Complete architectural and research write-up (citing the papers and setups you leveraged).
   - Complete drop-in, production-ready script `rp2_round15_unstoppable_trend_engine.py` (with server-side KQL and self-test).
   - Consolidated 20-Window Scorecard proving joint pass across all 20 regimes.

Opus, you have the data, the tools, and the mandate. Do not stop until you crack all 20 windows!
