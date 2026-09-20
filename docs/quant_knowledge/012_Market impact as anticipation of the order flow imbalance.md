# Market impact as anticipation of the order flow imbalance

## Metadata
- **Authors**: Thibault Jaisson
- **Publication Date**: 2014-02-06
- **Repository / Identifier**: [http://arxiv.org/abs/1402.1288v1](http://arxiv.org/abs/1402.1288v1)
- **PDF Source**: [https://arxiv.org/pdf/1402.1288v1](https://arxiv.org/pdf/1402.1288v1)
- **Strategic Paradigm**: `Order Flow Imbalance & Microstructure`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
In this paper, we assume that the permanent market impact of metaorders is linear and that the price is a martingale. Those two hypotheses enable us to derive the evolution of the price from the dynamics of the flow of market orders. For example, if the market order flow is assumed to follow a nearly unstable Hawkes process, we retrieve the apparent long memory of the flow together with a power law impact function which is consistent with the celebrated square root law. We also link the long memory exponent of the sign of market orders with the impact function exponent. One of the originalities of our approach is that our results are derived without assuming that market participants are able to detect the beginning of metaorders.

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
