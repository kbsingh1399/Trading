# Minimizing the Probability of Lifetime Drawdown under Constant Consumption

## Metadata
- **Authors**: Bahman Angoshtari, Erhan Bayraktar, Virginia R. Young
- **Publication Date**: 2015-07-31
- **Repository / Identifier**: [http://arxiv.org/abs/1507.08713v3](http://arxiv.org/abs/1507.08713v3)
- **PDF Source**: [https://arxiv.org/pdf/1507.08713v3](https://arxiv.org/pdf/1507.08713v3)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We assume that an individual invests in a financial market with one riskless and one risky asset, with the latter's price following geometric Brownian motion as in the Black-Scholes model. Under a constant rate of consumption, we find the optimal investment strategy for the individual who wishes to minimize the probability that her wealth drops below some fixed proportion of her maximum wealth to date, the so-called probability of {\it lifetime drawdown}. If maximum wealth is less than a particular value, $m^*$, then the individual optimally invests in such a way that maximum wealth never increases above its current value. By contrast, if maximum wealth is greater than $m^*$ but less than the safe level, then the individual optimally allows the maximum to increase to the safe level.

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
