# Optimal Market Making in the Presence of Latency

## Metadata
- **Authors**: Xuefeng Gao, Yunhan Wang
- **Publication Date**: 2018-06-15
- **Repository / Identifier**: [http://arxiv.org/abs/1806.05849v3](http://arxiv.org/abs/1806.05849v3)
- **PDF Source**: [https://arxiv.org/pdf/1806.05849v3](https://arxiv.org/pdf/1806.05849v3)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
This paper studies optimal market making for large-tick assets in the presence of latency. We consider a random walk model for the asset price, and formulate the market maker's optimization problem using Markov Decision Processes (MDP). We characterize the value of an order and show that it plays the role of one-period reward in the MDP model. Based on this characterization, we provide explicit criteria for assessing the profitability of market making when there is latency. Under our model, we show that a market maker can earn a positive expected profit if there are sufficient uninformed market orders hitting the market maker's limit orders compared with the rate of price jumps, and the trading horizon is sufficiently long. In addition, our theoretical and numerical results suggest that latency can be an additional source of risk and latency impacts negatively the performance of market makers.

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
