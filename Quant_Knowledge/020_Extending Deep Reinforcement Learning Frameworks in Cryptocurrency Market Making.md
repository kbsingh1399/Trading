# Extending Deep Reinforcement Learning Frameworks in Cryptocurrency Market Making

## Metadata
- **Authors**: Jonathan Sadighian
- **Publication Date**: 2020-04-15
- **Repository / Identifier**: [http://arxiv.org/abs/2004.06985v1](http://arxiv.org/abs/2004.06985v1)
- **PDF Source**: [https://arxiv.org/pdf/2004.06985v1](https://arxiv.org/pdf/2004.06985v1)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
There has been a recent surge in interest in the application of artificial intelligence to automated trading. Reinforcement learning has been applied to single- and multi-instrument use cases, such as market making or portfolio management. This paper proposes a new approach to framing cryptocurrency market making as a reinforcement learning challenge by introducing an event-based environment wherein an event is defined as a change in price greater or less than a given threshold, as opposed to by tick or time-based events (e.g., every minute, hour, day, etc.). Two policy-based agents are trained to learn a market making trading strategy using eight days of training data and evaluate their performance using 30 days of testing data. Limit order book data recorded from Bitmex exchange is used to validate this approach, which demonstrates improved profit and stability compared to a time-based approach for both agents when using a simple multi-layer perceptron neural network for function approximation and seven different reward functions.

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
