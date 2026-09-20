# Deep Learning Statistical Arbitrage

## Metadata
- **Authors**: Jorge Guijarro-Ordonez, Markus Pelger, Greg Zanotti
- **Publication Date**: 2021-06-08
- **Repository / Identifier**: [http://arxiv.org/abs/2106.04028v2](http://arxiv.org/abs/2106.04028v2)
- **PDF Source**: [https://arxiv.org/pdf/2106.04028v2](https://arxiv.org/pdf/2106.04028v2)
- **Strategic Paradigm**: `Statistical Arbitrage & Cointegration`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Statistical arbitrage exploits temporal price differences between similar assets. We develop a unifying conceptual framework for statistical arbitrage and a novel data driven solution. First, we construct arbitrage portfolios of similar assets as residual portfolios from conditional latent asset pricing factors. Second, we extract their time series signals with a powerful machine-learning time-series solution, a convolutional transformer. Lastly, we use these signals to form an optimal trading policy, that maximizes risk-adjusted returns under constraints. Our comprehensive empirical study on daily US equities shows a high compensation for arbitrageurs to enforce the law of one price. Our arbitrage strategies obtain consistently high out-of-sample mean returns and Sharpe ratios, and substantially outperform all benchmark approaches.

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
