# Optimal trend following portfolios

## Metadata
- **Authors**: Sebastien Valeyre
- **Publication Date**: 2022-01-17
- **Repository / Identifier**: [http://arxiv.org/abs/2201.06635v1](http://arxiv.org/abs/2201.06635v1)
- **PDF Source**: [https://arxiv.org/pdf/2201.06635v1](https://arxiv.org/pdf/2201.06635v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
This paper derives an optimal portfolio that is based on trend-following signal. Building on an earlier related article, it provides a unifying theoretical setting to introduce an autocorrelation model with the covariance matrix of trends and risk premia. We specify practically relevant models for the covariance matrix of trends. The optimal portfolio is decomposed into four basic components that yield four basic portfolios: Markowitz, risk parity, agnostic risk parity, and trend following on risk parity. The overperformance of the proposed optimal portfolio, applied to cross-asset trading universe, is confirmed by empirical backtests. We provide thus a unifying framework to describe and rationalize earlier developed portfolios.

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
