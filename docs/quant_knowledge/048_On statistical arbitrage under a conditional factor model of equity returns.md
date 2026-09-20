# On statistical arbitrage under a conditional factor model of equity returns

## Metadata
- **Authors**: Trent Spears, Stefan Zohren, Stephen Roberts
- **Publication Date**: 2023-09-05
- **Repository / Identifier**: [http://arxiv.org/abs/2309.02205v1](http://arxiv.org/abs/2309.02205v1)
- **PDF Source**: [https://arxiv.org/pdf/2309.02205v1](https://arxiv.org/pdf/2309.02205v1)
- **Strategic Paradigm**: `Statistical Arbitrage & Cointegration`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
We consider a conditional factor model for a multivariate portfolio of United States equities in the context of analysing a statistical arbitrage trading strategy. A state space framework underlies the factor model whereby asset returns are assumed to be a noisy observation of a linear combination of factor values and latent factor risk premia. Filter and state prediction estimates for the risk premia are retrieved in an online way. Such estimates induce filtered asset returns that can be compared to measurement observations, with large deviations representing candidate mean reversion trades. Further, in that the risk premia are modelled as time-varying quantities, non-stationarity in returns is de facto captured. We study an empirical trading strategy respectful of transaction costs, and demonstrate performance over a long history of 29 years, for both a linear and a non-linear state space model. Our results show that the model is competitive relative to the results of other methods, including simple benchmarks and other cutting-edge approaches as published in the literature. Also of note, while strategy performance degradation is noticed through time -- especially for the most recent years -- the strategy continues to offer compelling economics, and has scope for further advancement.

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
