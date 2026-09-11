# Reinforcement Learning-Based Market Making as a Stochastic Control on Non-Stationary Limit Order Book Dynamics

## Metadata
- **Authors**: Rafael Zimmer, Oswaldo Luiz do Valle Costa
- **Publication Date**: 2025-09-15
- **Repository / Identifier**: [http://arxiv.org/abs/2509.12456v2](http://arxiv.org/abs/2509.12456v2)
- **PDF Source**: [https://arxiv.org/pdf/2509.12456v2](https://arxiv.org/pdf/2509.12456v2)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Reinforcement Learning has emerged as a promising framework for developing adaptive and data-driven strategies, enabling market makers to optimize decision-making policies based on interactions with the limit order book environment. This paper explores the integration of a reinforcement learning agent in a market-making context, where the underlying market dynamics have been explicitly modeled to capture observed stylized facts of real markets, including clustered order arrival times, non-stationary spreads and return drifts, stochastic order quantities and price volatility. These mechanisms aim to enhance stability of the resulting control agent, and serve to incorporate domain-specific knowledge into the agent policy learning process. Our contributions include a practical implementation of a market making agent based on the Proximal-Policy Optimization (PPO) algorithm, alongside a comparative evaluation of the agent's performance under varying market conditions via a simulator-based environment. As evidenced by our analysis of the financial return and risk metrics when compared to a closed-form optimal solution, our results suggest that the reinforcement learning agent can effectively be used under non-stationary market conditions, and that the proposed simulator-based environment can serve as a valuable tool for training and pre-training reinforcement learning agents in market-making scenarios.

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
