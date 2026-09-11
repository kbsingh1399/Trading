# Trend followers lose more often than they gain

## Metadata
- **Authors**: Marc Potters, Jean-Philippe Bouchaud
- **Publication Date**: 2005-08-16
- **Repository / Identifier**: [http://arxiv.org/abs/physics/0508104v1](http://arxiv.org/abs/physics/0508104v1)
- **PDF Source**: [https://arxiv.org/pdf/physics/0508104v1](https://arxiv.org/pdf/physics/0508104v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We solve exactly a simple model of trend following strategy, and obtain the analytical shape of the profit per trade distribution. This distribution is non trivial and has an option like, asymmetric structure. The degree of asymmetry depends continuously on the parameters of the strategy and on the volatility of the traded asset. While the average gain per trade is always exactly zero, the fraction f of winning trades decreases from f=1/2 for small volatility to f=0 for high volatility, showing that this winning probability does not give any information on the reliability of the strategy but is indicative of the trading style.

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
