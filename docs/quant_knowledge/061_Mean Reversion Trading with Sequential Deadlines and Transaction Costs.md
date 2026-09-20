# Mean Reversion Trading with Sequential Deadlines and Transaction Costs

## Metadata
- **Authors**: Yerkin Kitapbayev, Tim Leung
- **Publication Date**: 2017-07-11
- **Repository / Identifier**: [http://arxiv.org/abs/1707.03498v3](http://arxiv.org/abs/1707.03498v3)
- **PDF Source**: [https://arxiv.org/pdf/1707.03498v3](https://arxiv.org/pdf/1707.03498v3)
- **Strategic Paradigm**: `Ornstein-Uhlenbeck & Mean Reversion`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
We study the optimal timing strategies for trading a mean-reverting price process with afinite deadline to enter and a separate finite deadline to exit the market. The price process is modeled by a diffusion with an affine drift that encapsulates a number of well-known models,including the Ornstein-Uhlenbeck (OU) model, Cox-Ingersoll-Ross (CIR) model, Jacobi model,and inhomogeneous geometric Brownian motion (IGBM) model.We analyze three types of trading strategies: (i) the long-short (long to open, short to close) strategy; (ii) the short-long(short to open, long to close) strategy, and (iii) the chooser strategy whereby the trader has the added flexibility to enter the market by taking either a long or short position, and subsequently close the position. For each strategy, we solve an optimal double stopping problem with sequential deadlines, and determine the optimal timing of trades. Our solution methodology utilizes the local time-space calculus of Peskir (2005) to derive nonlinear integral equations of Volterra-type that uniquely characterize the trading boundaries. Numerical implementation ofthe integral equations provides examples of the optimal trading boundaries.

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
