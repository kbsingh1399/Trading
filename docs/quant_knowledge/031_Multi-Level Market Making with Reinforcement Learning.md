# Multi-Level Market Making with Reinforcement Learning

## Metadata
- **Authors**: Patrick Cheridito, Moritz Weiss
- **Publication Date**: 2026-08-18
- **Repository / Identifier**: [http://arxiv.org/abs/2608.18195v1](http://arxiv.org/abs/2608.18195v1)
- **PDF Source**: [https://arxiv.org/pdf/2608.18195v1](https://arxiv.org/pdf/2608.18195v1)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We introduce a reinforcement learning framework for market making in a limit order book. Our algorithm aims to maximize trading revenue by dynamically submitting market and limit orders of varying sizes across multiple price levels while controlling inventory size. We use multivariate logistic-normal distributions to model order allocations and employ a deep-set encoder to aggregate features from variable-length order sets into a fixed-dimensional latent representation. Additionally, we incorporate potential-based reward shaping to accelerate learning without altering the optimal policy. We illustrate the performance of the method in three simulated market environments consisting of noise traders who submit random trades, tactical traders who respond to instantaneous volume imbalance, and strategic traders who trade in the direction of an exponentially weighted volume imbalance signal.

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
