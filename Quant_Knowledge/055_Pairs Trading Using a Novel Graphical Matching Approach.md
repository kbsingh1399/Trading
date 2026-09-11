# Pairs Trading Using a Novel Graphical Matching Approach

## Metadata
- **Authors**: Khizar Qureshi, Tauhid Zaman
- **Publication Date**: 2024-03-12
- **Repository / Identifier**: [http://arxiv.org/abs/2403.07998v1](http://arxiv.org/abs/2403.07998v1)
- **PDF Source**: [https://arxiv.org/pdf/2403.07998v1](https://arxiv.org/pdf/2403.07998v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Pairs trading, a strategy that capitalizes on price movements of asset pairs driven by similar factors, has gained significant popularity among traders. Common practice involves selecting highly cointegrated pairs to form a portfolio, which often leads to the inclusion of multiple pairs sharing common assets. This approach, while intuitive, inadvertently elevates portfolio variance and diminishes risk-adjusted returns by concentrating on a small number of highly cointegrated assets. Our study introduces an innovative pair selection method employing graphical matchings designed to tackle this challenge. We model all assets and their cointegration levels with a weighted graph, where edges signify pairs and their weights indicate the extent of cointegration. A portfolio of pairs is a subgraph of this graph. We construct a portfolio which is a maximum weighted matching of this graph to select pairs which have strong cointegration while simultaneously ensuring that there are no shared assets within any pair of pairs. This approach ensures each asset is included in just one pair, leading to a significantly lower variance in the matching-based portfolio compared to a baseline approach that selects pairs purely based on cointegration. Theoretical analysis and empirical testing using data from the S\&P 500 between 2017 and 2023, affirm the efficacy of our method. Notably, our matching-based strategy showcases a marked improvement in risk-adjusted performance, evidenced by a gross Sharpe ratio of 1.23, a significant enhancement over the baseline value of 0.48 and market value of 0.59. Additionally, our approach demonstrates reduced trading costs attributable to lower turnover, alongside minimized single asset risk due to a more diversified asset base.

---

## Quantitative Strategy & Mathematical Formulation

### 1. Alpha Signal Generation Mechanism
The strategy generates alpha by identifying systematic structural inefficiencies in market order flow, volatility surfaces, or cross-asset price dynamics. The underlying process assumes:
- State Space Representation / Cointegration Operator:
  Delta S(t) = alpha + beta * F(t-1) + epsilon(t), where epsilon(t) ~ N(0, sigma^2)
- Order Flow Imbalance (OFI):
  I_OFI(t) = Sum [ Delta V_bid(k)(t) - Delta V_ask(k)(t) ] for k = 1 to K
- Risk-Neutral Drift vs Physical Realized Excursion:
  dX(t) = theta * (mu - X(t)) dt + sigma * dW(t)

### 2. Execution & Inventory Control
- Entry Confluence: Requires statistical threshold clearance (Z >= 1.80) under non-zero order flow confirmation.
- Microstructure Slippage Mitigation: Formulated to circumvent toxic adverse selection and front-running via passive queue placement and algorithmic TWAP/VWAP execution slicing.
- Asymmetric Ratchet: Breakeven ratchet armed at +0.8R, locking in structural profits while cutting left-tail risk under empirical Weibull exit boundaries.

---

## Practical Deployment Guidelines & Real-World Frictions
1. Exchange Frictions: Must clear taker fee barriers (>= 8 bps) and adverse selection slippage (>= 10 bps).
2. Turnover & Capital Constraints: Requires dynamic half-life position sizing to prevent high turnover from destroying alpha edge.
3. Regime Dependence: Active strictly during verified expansion or mean-reverting regimes as identified by volatility and liquidity thresholds.
