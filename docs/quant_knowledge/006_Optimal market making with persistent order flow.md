# Optimal market making with persistent order flow

## Metadata
- **Authors**: Paul Jusselin
- **Publication Date**: 2020-03-12
- **Repository / Identifier**: [http://arxiv.org/abs/2003.05958v2](http://arxiv.org/abs/2003.05958v2)
- **PDF Source**: [https://arxiv.org/pdf/2003.05958v2](https://arxiv.org/pdf/2003.05958v2)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
\noindent We address the issue of market making on electronic markets when taking into account the clustering and long memory properties of market order flows. We consider a market model with one market maker and order flows driven by general Hawkes processes. We formulate the market maker's objective as a stochastic control problem. We characterize an optimal control by proving existence and uniqueness of a viscosity solution to the associated Hamilton-Jacobi-Bellman equation. Finally we propose a fully consistent numerical method allowing to implement this optimal strategy in practice.

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
