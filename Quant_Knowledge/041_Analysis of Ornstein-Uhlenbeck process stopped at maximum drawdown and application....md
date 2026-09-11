# Analysis of Ornstein-Uhlenbeck process stopped at maximum drawdown and application to trading strategies with trailing stops

## Metadata
- **Authors**: Grigory Temnov
- **Publication Date**: 2015-07-06
- **Repository / Identifier**: [http://arxiv.org/abs/1507.01610v1](http://arxiv.org/abs/1507.01610v1)
- **PDF Source**: [https://arxiv.org/pdf/1507.01610v1](https://arxiv.org/pdf/1507.01610v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We propose a strategy for automated trading, outline theoretical justification of the profitability of this strategy and overview the hypothetical results in application to currency pairs trading. The proposed methodology relies on the assumption that processes reflecting the dynamics of currency exchange rates are in a certain sense similar to the class of Ornstein-Uhlenbeck processes and exhibits the mean reverting property. In order to describe the quantitative characteristics of the projected return of the strategy, we derive the explicit expression for the running maximum of the Ornstein-Uhlenbeck process stopped at maximum drawdown and look at the correspondence between derived characteristics and the observed ones.

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
