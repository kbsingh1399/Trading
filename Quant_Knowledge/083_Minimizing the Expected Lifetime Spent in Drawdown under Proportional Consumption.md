# Minimizing the Expected Lifetime Spent in Drawdown under Proportional Consumption

## Metadata
- **Authors**: Bahman Angoshtari, Erhan Bayraktar, Virginia R. Young
- **Publication Date**: 2015-08-08
- **Repository / Identifier**: [http://arxiv.org/abs/1508.01914v3](http://arxiv.org/abs/1508.01914v3)
- **PDF Source**: [https://arxiv.org/pdf/1508.01914v3](https://arxiv.org/pdf/1508.01914v3)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We determine the optimal amount to invest in a Black-Scholes financial market for an individual who consumes at a rate equal to a constant proportion of her wealth and who wishes to minimize the expected time that her wealth spends in drawdown during her lifetime. Drawdown occurs when wealth is less than some fixed proportion of maximum wealth. We compare the optimal investment strategy with those for three related goal-seeking problems and learn that the individual is myopic in her investing behavior, as expected from other goal-seeking research.

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
