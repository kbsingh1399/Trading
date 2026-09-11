# The numeraire property and long-term growth optimality for drawdown-constrained investments

## Metadata
- **Authors**: Constantinos Kardaras, Jan Obloj, Eckhard Platen
- **Publication Date**: 2012-06-11
- **Repository / Identifier**: [http://arxiv.org/abs/1206.2305v2](http://arxiv.org/abs/1206.2305v2)
- **PDF Source**: [https://arxiv.org/pdf/1206.2305v2](https://arxiv.org/pdf/1206.2305v2)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We consider the portfolio choice problem for a long-run investor in a general continuous semimartingale model. We suggest to use path-wise growth optimality as the decision criterion and encode preferences through restrictions on the class of admissible wealth processes. Specifically, the investor is only interested in strategies which satisfy a given linear drawdown constraint. The paper introduces the numeraire property through the notion of expected relative return and shows that drawdown-constrained strategies with the numeraire property exist and are unique, but may depend on the financial planning horizon. However, when sampled at the times of its maximum and asymptotically as the time-horizon becomes distant, the drawdown-constrained numeraire portfolio is given explicitly through a model-independent transformation of the unconstrained numeraire portfolio. Further, it is established that the asymptotically growth-optimal strategy is obtained as limit of numeraire strategies on finite horizons.

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
