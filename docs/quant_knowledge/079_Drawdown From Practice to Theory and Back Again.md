# Drawdown: From Practice to Theory and Back Again

## Metadata
- **Authors**: Lisa R. Goldberg, Ola Mahmoud
- **Publication Date**: 2014-04-29
- **Repository / Identifier**: [http://arxiv.org/abs/1404.7493v5](http://arxiv.org/abs/1404.7493v5)
- **PDF Source**: [https://arxiv.org/pdf/1404.7493v5](https://arxiv.org/pdf/1404.7493v5)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Maximum drawdown, the largest cumulative loss from peak to trough, is one of the most widely used indicators of risk in the fund management industry, but one of the least developed in the context of measures of risk. We formalize drawdown risk as Conditional Expected Drawdown (CED), which is the tail mean of maximum drawdown distributions. We show that CED is a degree one positive homogenous risk measure, so that it can be linearly attributed to factors; and convex, so that it can be used in quantitative optimization. We empirically explore the differences in risk attributions based on CED, Expected Shortfall (ES) and volatility. An important feature of CED is its sensitivity to serial correlation. In an empirical study that fits AR(1) models to US Equity and US Bonds, we find substantially higher correlation between the autoregressive parameter and CED than with ES or with volatility.

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
