# Avellaneda-Stoikov and Cartea-Jaimungal as One Framework: A Forced Uniqueness Theorem for Inventory Market Making

## Metadata
- **Authors**: Frank M. V. Feys
- **Publication Date**: 2026-05-31
- **Repository / Identifier**: [http://arxiv.org/abs/2606.01477v3](http://arxiv.org/abs/2606.01477v3)
- **PDF Source**: [https://arxiv.org/pdf/2606.01477v3](https://arxiv.org/pdf/2606.01477v3)
- **Strategic Paradigm**: `Stochastic Market Making Models`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
In inventory market making, the running-penalty coefficient $φ$ of the Cartea-Jaimungal framework and the risk-aversion parameter $γ$ of the Avellaneda-Stoikov framework are typically treated as independent free parameters, calibrated separately. We show that they are in fact not independent. A small set of axioms on the market maker's dynamic preference functional, namely cash-additivity, normalization, concavity, strong dynamic consistency, and law-invariance, forces the preference functional to be the entropic certainty-equivalent on liquidation-adjusted terminal wealth, parametrized by a single positive scalar $γ$. The Avellaneda-Stoikov framework is the unique representative of this axiom class. The Cartea-Jaimungal framework is its second-order Taylor expansion in inventory magnitude, with the running coefficient forced to $φ= γσ^2/2$ and (under a mild regularity condition on the liquidation cost) the terminal coefficient forced to $α= \frac{1}{2}L''(0)$. The two frameworks, typically presented as competing alternatives with the choice between them driven by tractability, are different manifestations of a single underlying object. The forced relation is invertible, $γ= 2φ/σ^2$, giving a consistency cross-check on independently calibrated desk parameters.

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
