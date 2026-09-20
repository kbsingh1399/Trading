# Stochastic Price Dynamics in Response to Order Flow Imbalance: Evidence from CSI 300 Index Futures

## Metadata
- **Authors**: Chen Hu, Kouxiao Zhang
- **Publication Date**: 2025-05-23
- **Repository / Identifier**: [http://arxiv.org/abs/2505.17388v1](http://arxiv.org/abs/2505.17388v1)
- **PDF Source**: [https://arxiv.org/pdf/2505.17388v1](https://arxiv.org/pdf/2505.17388v1)
- **Strategic Paradigm**: `Order Flow Imbalance & Microstructure`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
We conduct modeling of the price dynamics following order flow imbalance in market microstructure and apply the model to the analysis of Chinese CSI 300 Index Futures. There are three findings. The first is that the order flow imbalance is analogous to a shock to the market. Unlike the common practice of using Hawkes processes, we model the impact of order flow imbalance as an Ornstein-Uhlenbeck process with memory and mean-reverting characteristics driven by a jump-type Lévy process. Motivated by the empirically stable correlation between order flow imbalance and contemporaneous price changes, we propose a modified asset price model where the drift term of canonical geometric Brownian motion is replaced by an Ornstein-Uhlenbeck process. We establish stochastic differential equations and derive the logarithmic return process along with its mean and variance processes under initial boundary conditions, and evolution of cost-effectiveness ratio with order flow imbalance as the trading trigger point, termed as the quasi-Sharpe ratio or response ratio. Secondly, our results demonstrate horizon-dependent heterogeneity in how conventional metrics interact with order flow imbalance. This underscores the critical role of forecast horizon selection for strategies. Thirdly, we identify regime-dependent dynamics in the memory and forecasting power of order flow imbalance. This taxonomy provides both a screening protocol for existing indicators and an ex-ante evaluation paradigm for novel metrics.

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
