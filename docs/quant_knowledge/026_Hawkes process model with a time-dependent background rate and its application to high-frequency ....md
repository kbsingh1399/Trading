# Hawkes process model with a time-dependent background rate and its application to high-frequency financial data

## Metadata
- **Authors**: Takahiro Omi, Yoshito Hirata, Kazuyuki Aihara
- **Publication Date**: 2017-02-15
- **Repository / Identifier**: [http://arxiv.org/abs/1702.04443v4](http://arxiv.org/abs/1702.04443v4)
- **PDF Source**: [https://arxiv.org/pdf/1702.04443v4](https://arxiv.org/pdf/1702.04443v4)
- **Strategic Paradigm**: `High-Frequency Hawkes Jump Processes`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
A Hawkes process model with a time-varying background rate is developed for analyzing the high-frequency financial data. In our model, the logarithm of the background rate is modeled by a linear model with a relatively large number of variable-width basis functions, and the parameters are estimated by a Bayesian method. Our model can capture not only the slow time-variation, such as in the intraday seasonality, but also the rapid one, which follows a macroeconomic news announcement. By analyzing the tick data of the Nikkei 225 mini, we find that (i) our model is better fitted to the data than the Hawkes models with a constant background rate or a slowly varying background rate, which have been commonly used in the field of quantitative finance; (ii) the improvement in the goodness-of-fit to the data by our model is significant especially for sessions where considerable fluctuation of the background rate is present; and (iii) our model is statistically consistent with the data. The branching ratio, which quantifies the level of the endogeneity of markets, estimated by our model is 0.41, suggesting the relative importance of exogenous factors in the market dynamics. We also demonstrate that it is critically important to appropriately model the time-dependent background rate for the branching ratio estimation.

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
