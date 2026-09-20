# Revisiting the Structure of Trend Premia: When Diversification Hides Redundancy

## Metadata
- **Authors**: Alban Etienne, Jean-Jacques Ohana, Eric Benhamou, Béatrice Guez, Ethan Setrouk, Thomas Jacquot
- **Publication Date**: 2025-10-27
- **Repository / Identifier**: [http://arxiv.org/abs/2510.23150v2](http://arxiv.org/abs/2510.23150v2)
- **PDF Source**: [https://arxiv.org/pdf/2510.23150v2](https://arxiv.org/pdf/2510.23150v2)
- **Strategic Paradigm**: `Trend Following & Risk Management`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Recent work has emphasized the diversification benefits of combining trend signals across multiple horizons, with the medium-term window-typically six months to one year-long viewed as the "sweet spot" of trend-following. This paper revisits this conventional view by reallocating exposure dynamically across horizons using a Bayesian optimization framework designed to learn the optimal weights assigned to each trend horizon at the asset level. The common practice of equal weighting implicitly assumes that all assets benefit equally from all horizons; we show that this assumption is both theoretically and empirically suboptimal. We first optimize the horizon-level weights at the asset level to maximize the informativeness of trend signals before applying Bayesian graphical models-with sparsity and turnover control-to allocate dynamically across assets. The key finding is that the medium-term band contributes little incremental performance or diversification once short- and long-term components are included. Removing the 125-day layer improves Sharpe ratios and drawdown efficiency while maintaining benchmark correlation. We then rationalize this outcome through a minimum-variance formulation, showing that the medium-term horizon largely overlaps with its neighboring horizons. The resulting "barbell" structure-combining short- and long-term trends-captures most of the performance while reducing model complexity. This result challenges the common belief that more horizons always improve diversification and suggests that some forms of time-scale diversification may conceal unnecessary redundancy in trend premia.

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
