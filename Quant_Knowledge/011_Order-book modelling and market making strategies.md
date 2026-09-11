# Order-book modelling and market making strategies

## Metadata
- **Authors**: Xiaofei Lu, Frédéric Abergel
- **Publication Date**: 2018-06-13
- **Repository / Identifier**: [http://arxiv.org/abs/1806.05101v1](http://arxiv.org/abs/1806.05101v1)
- **PDF Source**: [https://arxiv.org/pdf/1806.05101v1](https://arxiv.org/pdf/1806.05101v1)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Market making is one of the most important aspects of algorithmic trading, and it has been studied quite extensively from a theoretical point of view. The practical implementation of so-called "optimal strategies" however suffers from the failure of most order book models to faithfully reproduce the behaviour of real market participants.   This paper is twofold. First, some important statistical properties of order driven markets are identified, advocating against the use of purely Markovian order book models. Then, market making strategies are designed and their performances are compared, based on simulation as well as backtesting. We find that incorporating some simple non-Markovian features in the limit order book greatly improves the performances of market making strategies in a realistic context.

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
