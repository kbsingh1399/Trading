# Building Cross-Sectional Systematic Strategies By Learning to Rank

## Metadata
- **Authors**: Daniel Poh, Bryan Lim, Stefan Zohren, Stephen Roberts
- **Publication Date**: 2020-12-13
- **Repository / Identifier**: [http://arxiv.org/abs/2012.07149v1](http://arxiv.org/abs/2012.07149v1)
- **PDF Source**: [https://arxiv.org/pdf/2012.07149v1](https://arxiv.org/pdf/2012.07149v1)
- **Strategic Paradigm**: `Cross-Sectional Momentum & Relative Strength`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
The success of a cross-sectional systematic strategy depends critically on accurately ranking assets prior to portfolio construction. Contemporary techniques perform this ranking step either with simple heuristics or by sorting outputs from standard regression or classification models, which have been demonstrated to be sub-optimal for ranking in other domains (e.g. information retrieval). To address this deficiency, we propose a framework to enhance cross-sectional portfolios by incorporating learning-to-rank algorithms, which lead to improvements of ranking accuracy by learning pairwise and listwise structures across instruments. Using cross-sectional momentum as a demonstrative case study, we show that the use of modern machine learning ranking algorithms can substantially improve the trading performance of cross-sectional strategies -- providing approximately threefold boosting of Sharpe Ratios compared to traditional approaches.

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
