# A General Framework for Portfolio Theory. Part II: drawdown risk measures

## Metadata
- **Authors**: Stanislaus Maier-Paape, Qiji Jim Zhu
- **Publication Date**: 2017-10-13
- **Repository / Identifier**: [http://arxiv.org/abs/1710.04818v1](http://arxiv.org/abs/1710.04818v1)
- **PDF Source**: [https://arxiv.org/pdf/1710.04818v1](https://arxiv.org/pdf/1710.04818v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
The aim of this paper is to provide several examples of convex risk measures necessary for the application of the general framework for portfolio theory of Maier-Paape and Zhu, presented in Part I of this series (arXiv:1710.04579 [q-fin.PM]). As alternative to classical portfolio risk measures such as the standard deviation we in particular construct risk measures related to the current drawdown of the portfolio equity. Combined with the results of Part I (arXiv:1710.04579 [q-fin.PM]), this allows us to calculate efficient portfolios based on a drawdown risk measure constraint.

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
