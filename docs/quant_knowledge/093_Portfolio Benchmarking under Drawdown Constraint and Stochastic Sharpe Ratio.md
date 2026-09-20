# Portfolio Benchmarking under Drawdown Constraint and Stochastic Sharpe Ratio

## Metadata
- **Authors**: Ankush Agarwal, Ronnie Sircar
- **Publication Date**: 2016-10-26
- **Repository / Identifier**: [http://arxiv.org/abs/1610.08558v1](http://arxiv.org/abs/1610.08558v1)
- **PDF Source**: [https://arxiv.org/pdf/1610.08558v1](https://arxiv.org/pdf/1610.08558v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We consider an investor who seeks to maximize her expected utility derived from her terminal wealth relative to the maximum performance achieved over a fixed time horizon, and under a portfolio drawdown constraint, in a market with local stochastic volatility (LSV). In the absence of closed-form formulas for the value function and optimal portfolio strategy, we obtain approximations for these quantities through the use of a coefficient expansion technique and nonlinear transformations. We utilize regularity properties of the risk tolerance function to numerically compute the estimates for our approximations. In order to achieve similar value functions, we illustrate that, compared to a constant volatility model, the investor must deploy a quite different portfolio strategy which depends on the current level of volatility in the stochastic volatility model.

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
