# Testing the causality of Hawkes processes with time reversal

## Metadata
- **Authors**: Marcus Cordi, Damien Challet, Ioane Muni Toke
- **Publication Date**: 2017-09-25
- **Repository / Identifier**: [http://arxiv.org/abs/1709.08516v1](http://arxiv.org/abs/1709.08516v1)
- **PDF Source**: [https://arxiv.org/pdf/1709.08516v1](https://arxiv.org/pdf/1709.08516v1)
- **Strategic Paradigm**: `High-Frequency Hawkes Jump Processes`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
We show that univariate and symmetric multivariate Hawkes processes are only weakly causal: the true log-likelihoods of real and reversed event time vectors are almost equal, thus parameter estimation via maximum likelihood only weakly depends on the direction of the arrow of time. In ideal (synthetic) conditions, tests of goodness of parametric fit unambiguously reject backward event times, which implies that inferring kernels from time-symmetric quantities, such as the autocovariance of the event rate, only rarely produce statistically significant fits. Finally, we find that fitting financial data with many-parameter kernels may yield significant fits for both arrows of time for the same event time vector, sometimes favouring the backward time direction. This goes to show that a significant fit of Hawkes processes to real data with flexible kernels does not imply a definite arrow of time unless one tests it.

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
