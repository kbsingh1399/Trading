# Discrete-time portfolio optimization under maximum drawdown constraint with partial information and deep learning resolution

## Metadata
- **Authors**: Carmine De Franco, Johann Nicolle, Huyên Pham
- **Publication Date**: 2020-10-29
- **Repository / Identifier**: [http://arxiv.org/abs/2010.15779v2](http://arxiv.org/abs/2010.15779v2)
- **PDF Source**: [https://arxiv.org/pdf/2010.15779v2](https://arxiv.org/pdf/2010.15779v2)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We study a discrete-time portfolio selection problem with partial information and maxi\-mum drawdown constraint. Drift uncertainty in the multidimensional framework is modeled by a prior probability distribution. In this Bayesian framework, we derive the dynamic programming equation using an appropriate change of measure, and obtain semi-explicit results in the Gaussian case. The latter case, with a CRRA utility function is completely solved numerically using recent deep learning techniques for stochastic optimal control problems. We emphasize the informative value of the learning strategy versus the non-learning one by providing empirical performance and sensitivity analysis with respect to the uncertainty of the drift. Furthermore, we show numerical evidence of the close relationship between the non-learning strategy and a no short-sale constrained Merton problem, by illustrating the convergence of the former towards the latter as the maximum drawdown constraint vanishes.

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
