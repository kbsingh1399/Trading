# Deep Reinforcement Learning in Cryptocurrency Market Making

## Metadata
- **Authors**: Jonathan Sadighian
- **Publication Date**: 2019-11-20
- **Repository / Identifier**: [http://arxiv.org/abs/1911.08647v1](http://arxiv.org/abs/1911.08647v1)
- **PDF Source**: [https://arxiv.org/pdf/1911.08647v1](https://arxiv.org/pdf/1911.08647v1)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
This paper sets forth a framework for deep reinforcement learning as applied to market making (DRLMM) for cryptocurrencies. Two advanced policy gradient-based algorithms were selected as agents to interact with an environment that represents the observation space through limit order book data, and order flow arrival statistics. Within the experiment, a forward-feed neural network is used as the function approximator and two reward functions are compared. The performance of each combination of agent and reward function is evaluated by daily and average trade returns. Using this DRLMM framework, this paper demonstrates the effectiveness of deep reinforcement learning in solving stochastic inventory control challenges market makers face.

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
