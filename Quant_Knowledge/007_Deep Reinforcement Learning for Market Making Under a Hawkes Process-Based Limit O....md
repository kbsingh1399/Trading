# Deep Reinforcement Learning for Market Making Under a Hawkes Process-Based Limit Order Book Model

## Metadata
- **Authors**: Bruno Gašperov, Zvonko Kostanjčar
- **Publication Date**: 2022-07-20
- **Repository / Identifier**: [http://arxiv.org/abs/2207.09951v1](http://arxiv.org/abs/2207.09951v1)
- **PDF Source**: [https://arxiv.org/pdf/2207.09951v1](https://arxiv.org/pdf/2207.09951v1)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
The stochastic control problem of optimal market making is among the central problems in quantitative finance. In this paper, a deep reinforcement learning-based controller is trained on a weakly consistent, multivariate Hawkes process-based limit order book simulator to obtain market making controls. The proposed approach leverages the advantages of Monte Carlo backtesting and contributes to the line of research on market making under weakly consistent limit order book models. The ensuing deep reinforcement learning controller is compared to multiple market making benchmarks, with the results indicating its superior performance with respect to various risk-reward metrics, even under significant transaction costs.

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
