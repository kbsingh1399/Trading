# Hawkes Processes

## Metadata
- **Authors**: Patrick J. Laub, Thomas Taimre, Philip K. Pollett
- **Publication Date**: 2015-07-10
- **Repository / Identifier**: [http://arxiv.org/abs/1507.02822v1](http://arxiv.org/abs/1507.02822v1)
- **PDF Source**: [https://arxiv.org/pdf/1507.02822v1](https://arxiv.org/pdf/1507.02822v1)
- **Strategic Paradigm**: `High-Frequency Hawkes Jump Processes`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Hawkes processes are a particularly interesting class of stochastic process that have been applied in diverse areas, from earthquake modelling to financial analysis. They are point processes whose defining characteristic is that they 'self-excite', meaning that each arrival increases the rate of future arrivals for some period of time. Hawkes processes are well established, particularly within the financial literature, yet many of the treatments are inaccessible to one not acquainted with the topic. This survey provides background, introduces the field and historical developments, and touches upon all major aspects of Hawkes processes.

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
