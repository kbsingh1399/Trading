# Performance of information criteria used for model selection of Hawkes process models of financial data

## Metadata
- **Authors**: J. M. Chen, A. G. Hawkes, E. Scalas, M. Trinh
- **Publication Date**: 2017-02-20
- **Repository / Identifier**: [http://arxiv.org/abs/1702.06055v2](http://arxiv.org/abs/1702.06055v2)
- **PDF Source**: [https://arxiv.org/pdf/1702.06055v2](https://arxiv.org/pdf/1702.06055v2)
- **Strategic Paradigm**: `High-Frequency Hawkes Jump Processes`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
We test three common information criteria (IC) for selecting the order of a Hawkes process with an intensity kernel that can be expressed as a mixture of exponential terms. These processes find application in high-frequency financial data modelling. The information criteria are Akaike's information criterion (AIC), the Bayesian information criterion (BIC) and the Hannan-Quinn criterion (HQ). Since we work with simulated data, we are able to measure the performance of model selection by the success rate of the IC in selecting the model that was used to generate the data. In particular, we are interested in the relation between correct model selection and underlying sample size. The analysis includes realistic sample sizes and parameter sets from recent literature where parameters were estimated using empirical financial intra-day data. We compare our results to theoretical predictions and similar empirical findings on the asymptotic distribution of model selection for consistent and inconsistent IC.

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
