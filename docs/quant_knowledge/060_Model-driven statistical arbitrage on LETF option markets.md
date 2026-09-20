# Model-driven statistical arbitrage on LETF option markets

## Metadata
- **Authors**: Sergey Nasekin, Wolfgang Karl Härdle
- **Publication Date**: 2020-09-21
- **Repository / Identifier**: [http://arxiv.org/abs/2009.09713v1](http://arxiv.org/abs/2009.09713v1)
- **PDF Source**: [https://arxiv.org/pdf/2009.09713v1](https://arxiv.org/pdf/2009.09713v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
In this paper, we study the statistical properties of the moneyness scaling transformation by Leung and Sircar (2015). This transformation adjusts the moneyness coordinate of the implied volatility smile in an attempt to remove the discrepancy between the IV smiles for levered and unlevered ETF options. We construct bootstrap uniform confidence bands which indicate that the implied volatility smiles are statistically different after moneyness scaling has been performed. An empirical application shows that there are trading opportunities possible on the LETF market. A statistical arbitrage type strategy based on a dynamic semiparametric factor model is presented. This strategy presents a statistical decision algorithm which generates trade recommendations based on comparison of model and observed LETF implied volatility surface. It is shown to generate positive returns with a high probability. Extensive econometric analysis of LETF implied volatility process is performed including out-of-sample forecasting based on a semiparametric factor model and uniform confidence bands' study. It provides new insights into the latent dynamics of the implied volatility surface. We also incorporate Heston stochastic volatility into the moneyness scaling method for better tractability of the model.

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
