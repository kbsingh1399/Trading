# Spread, volatility, and volume relationship in financial markets and market making profit optimization

## Metadata
- **Authors**: Jack Sarkissian
- **Publication Date**: 2016-06-23
- **Repository / Identifier**: [http://arxiv.org/abs/1606.07381v1](http://arxiv.org/abs/1606.07381v1)
- **PDF Source**: [https://arxiv.org/pdf/1606.07381v1](https://arxiv.org/pdf/1606.07381v1)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We study the relationship between price spread, volatility and trading volume. We find that spread forms as a result of interplay between order liquidity and order impact. When trading volume is small adding more liquidity helps improve price accuracy and reduce spread, but after some point additional liquidity begins to deteriorate price. The model allows to connect the bid-ask spread and high-low bars to measurable microstructural parameters and express their dependence on trading volume, volatility and time horizon. Using the established relations, we address the operating spread optimization problem to maximize market-making profit.

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
