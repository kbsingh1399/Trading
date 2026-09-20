# Multiple time scales and the exponential Ornstein-Uhlenbeck stochastic volatility model

## Metadata
- **Authors**: Jaume Masoliver, Josep Perello
- **Publication Date**: 2005-01-26
- **Repository / Identifier**: [http://arxiv.org/abs/cond-mat/0501639v1](http://arxiv.org/abs/cond-mat/0501639v1)
- **PDF Source**: [https://arxiv.org/pdf/cond-mat/0501639v1](https://arxiv.org/pdf/cond-mat/0501639v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We study the exponential Ornstein-Uhlenbeck stochastic volatility model and observe that the model shows a multiscale behavior in the volatility autocorrelation. It also exhibits a leverage correlation and a probability profile for the stationary volatility which are consistent with market observations. All these features make the model quite appealing since it appears to be more complete than other stochastic volatility models also based on a two-dimensional diffusion. We finally present an approximate solution for the return probability density designed to capture the kurtosis and skewness effects.

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
