# Statistical Arbitrage Risk Premium by Machine Learning

## Metadata
- **Authors**: Raymond C. W. Leung, Yu-Man Tam
- **Publication Date**: 2021-03-18
- **Repository / Identifier**: [http://arxiv.org/abs/2103.09987v1](http://arxiv.org/abs/2103.09987v1)
- **PDF Source**: [https://arxiv.org/pdf/2103.09987v1](https://arxiv.org/pdf/2103.09987v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
How to hedge factor risks without knowing the identities of the factors? We first prove a general theoretical result: even if the exact set of factors cannot be identified, any risky asset can use some portfolio of similar peer assets to hedge against its own factor exposures. A long position of a risky asset and a short position of a "replicate portfolio" of its peers represent that asset's factor residual risk. We coin the expected return of an asset's factor residual risk as its Statistical Arbitrage Risk Premium (SARP). The challenge in empirically estimating SARP is finding the peers for each asset and constructing the replicate portfolios. We use the elastic-net, a machine learning method, to project each stock's past returns onto that of every other stock. The resulting high-dimensional but sparse projection vector serves as investment weights in constructing the stocks' replicate portfolios. We say a stock has high (low) Statistical Arbitrage Risk (SAR) if it has low (high) R-squared with its peers. The key finding is that "unique" stocks have both a higher SARP and higher excess returns than "ubiquitous" stocks: in the cross-section, high SAR stocks have a monthly SARP (monthly excess returns) that is 1.101% (0.710%) greater than low SAR stocks. The average SAR across all stocks is countercyclical. Our results are robust to controlling for various known priced factors and characteristics.

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
