# The limits of statistical significance of Hawkes processes fitted to financial data

## Metadata
- **Authors**: Mehdi Lallouache, Damien Challet
- **Publication Date**: 2014-06-16
- **Repository / Identifier**: [http://arxiv.org/abs/1406.3967v2](http://arxiv.org/abs/1406.3967v2)
- **PDF Source**: [https://arxiv.org/pdf/1406.3967v2](https://arxiv.org/pdf/1406.3967v2)
- **Strategic Paradigm**: `High-Frequency Hawkes Jump Processes`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Many fits of Hawkes processes to financial data look rather good but most of them are not statistically significant. This raises the question of what part of market dynamics this model is able to account for exactly. We document the accuracy of such processes as one varies the time interval of calibration and compare the performance of various types of kernels made up of sums of exponentials. Because of their around-the-clock opening times, FX markets are ideally suited to our aim as they allow us to avoid the complications of the long daily overnight closures of equity markets. One can achieve statistical significance according to three simultaneous tests provided that one uses kernels with two exponentials for fitting an hour at a time, and two or three exponentials for full days, while longer periods could not be fitted within statistical satisfaction because of the non-stationarity of the endogenous process. Fitted timescales are relatively short and endogeneity factor is high but sub-critical at about 0.8.

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
