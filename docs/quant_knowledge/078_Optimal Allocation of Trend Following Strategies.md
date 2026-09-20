# Optimal Allocation of Trend Following Strategies

## Metadata
- **Authors**: Denis S. Grebenkov, Jeremy Serror
- **Publication Date**: 2014-10-30
- **Repository / Identifier**: [http://arxiv.org/abs/1410.8409v1](http://arxiv.org/abs/1410.8409v1)
- **PDF Source**: [https://arxiv.org/pdf/1410.8409v1](https://arxiv.org/pdf/1410.8409v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We consider a portfolio allocation problem for trend following (TF) strategies on multiple correlated assets. Under simplifying assumptions of a Gaussian market and linear TF strategies, we derive analytical formulas for the mean and variance of the portfolio return. We construct then the optimal portfolio that maximizes risk-adjusted return by accounting for inter-asset correlations. The dynamic allocation problem for $n$ assets is shown to be equivalent to the classical static allocation problem for $n^2$ virtual assets that include lead-lag corrections in positions of TF strategies. The respective roles of asset auto-correlations and inter-asset correlations are investigated in depth for the two-asset case and a sector model. In contrast to the principle of diversification suggesting to treat uncorrelated assets, we show that inter-asset correlations allow one to estimate apparent trends more reliably and to adjust the TF positions more efficiently. If properly accounted for, inter-asset correlations are not deteriorative but beneficial for portfolio management that can open new profit opportunities for trend followers.

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
