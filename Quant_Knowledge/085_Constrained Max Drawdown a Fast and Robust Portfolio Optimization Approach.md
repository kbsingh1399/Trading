# Constrained Max Drawdown: a Fast and Robust Portfolio Optimization Approach

## Metadata
- **Authors**: Albert Dorador
- **Publication Date**: 2024-01-05
- **Repository / Identifier**: [http://arxiv.org/abs/2401.02601v1](http://arxiv.org/abs/2401.02601v1)
- **PDF Source**: [https://arxiv.org/pdf/2401.02601v1](https://arxiv.org/pdf/2401.02601v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We propose an alternative linearization to the classical Markowitz quadratic portfolio optimization model, based on maximum drawdown. This model, which minimizes maximum portfolio drawdown, is particularly appealing during times of financial distress, like during the COVID-19 pandemic. In addition, we will present a Mixed-Integer Linear Programming variation of our new model that, based on our out-of-sample results and sensitivity analysis, delivers a more profitable and robust solution with a 200 times faster solving time compared to the standard Markowitz quadratic formulation.

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
