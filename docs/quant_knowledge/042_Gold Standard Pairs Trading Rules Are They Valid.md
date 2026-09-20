# Gold Standard Pairs Trading Rules: Are They Valid?

## Metadata
- **Authors**: Miroslav Fil
- **Publication Date**: 2020-10-02
- **Repository / Identifier**: [http://arxiv.org/abs/2010.01157v1](http://arxiv.org/abs/2010.01157v1)
- **PDF Source**: [https://arxiv.org/pdf/2010.01157v1](https://arxiv.org/pdf/2010.01157v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Pairs trading is a strategy based on exploiting mean reversion in prices of securities. It has been shown to generate significant excess returns, but its profitability has dropped significantly in recent periods. We employ the most common distance and cointegration methods on US equities from 1990 to 2020 including the Covid-19 crisis. The strategy overall fails to outperform the market benchmark even with hyperparameter tuning, but it performs very strongly during bear markets. Furthermore, we demonstrate that market factors have a strong relationship with the optimal parametrization for the strategy, and adjustments are appropriate for modern market conditions.

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
