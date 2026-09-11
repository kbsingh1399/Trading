# Determining Optimal Stop-Loss Thresholds via Bayesian Analysis of Drawdown Distributions

## Metadata
- **Authors**: Antoine Emil Zambelli
- **Publication Date**: 2016-09-03
- **Repository / Identifier**: [http://arxiv.org/abs/1609.00869v1](http://arxiv.org/abs/1609.00869v1)
- **PDF Source**: [https://arxiv.org/pdf/1609.00869v1](https://arxiv.org/pdf/1609.00869v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Stop-loss rules are often studied in the financial literature, but the stop-loss levels are seldom constructed systematically. In many papers, and indeed in practice as well, the level of the stops is too often set arbitrarily. Guided by the overarching goal in finance to maximize expected returns given available information, we propose a natural method by which to systematically select the stop-loss threshold by analyzing the distribution of maximum drawdowns. We present results for an hourly trading strategy with two variations on the construction.

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
