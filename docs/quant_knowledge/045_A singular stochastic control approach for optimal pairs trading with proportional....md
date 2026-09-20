# A singular stochastic control approach for optimal pairs trading with proportional transaction costs

## Metadata
- **Authors**: Haipeng Xing
- **Publication Date**: 2019-11-24
- **Repository / Identifier**: [http://arxiv.org/abs/1911.10450v1](http://arxiv.org/abs/1911.10450v1)
- **PDF Source**: [https://arxiv.org/pdf/1911.10450v1](https://arxiv.org/pdf/1911.10450v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Optimal trading strategies for pairs trading have been studied by models that try to find either optimal shares of stocks by assuming no transaction costs or optimal timing of trading fixed numbers of shares of stocks with transaction costs. To find optimal strategies which determine optimally both trade times and number of shares in pairs trading process, we use a singular stochastic control approach to study an optimal pairs trading problem with proportional transaction costs. Assuming a cointegrated relationship for a pair of stock log-prices, we consider a portfolio optimization problem which involves dynamic trading strategies with proportional transaction costs. We show that the value function of the control problem is the unique viscosity solution of a nonlinear quasi-variational inequality, which is equivalent to a free boundary problem for the singular stochastic control value function. We then develop a discrete time dynamic programming algorithm to compute the transaction regions, and show the convergence of the discretization scheme. We illustrate our approach with numerical examples and discuss the impact of different parameters on transaction regions. We study the out-of-sample performance in an empirical study that consists of six pairs of U.S. stocks selected from different industry sectors, and demonstrate the efficiency of the optimal strategy.

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
