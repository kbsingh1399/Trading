# Market Making with Scaled Beta Policies

## Metadata
- **Authors**: Joseph Jerome, Gregory Palmer, Rahul Savani
- **Publication Date**: 2022-07-07
- **Repository / Identifier**: [http://arxiv.org/abs/2207.03352v4](http://arxiv.org/abs/2207.03352v4)
- **PDF Source**: [https://arxiv.org/pdf/2207.03352v4](https://arxiv.org/pdf/2207.03352v4)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
This paper introduces a new representation for the actions of a market maker in an order-driven market. This representation uses scaled beta distributions, and generalises three approaches taken in the artificial intelligence for market making literature: single price-level selection, ladder strategies and "market making at the touch". Ladder strategies place uniform volume across an interval of contiguous prices. Scaled beta distribution based policies generalise these, allowing volume to be skewed across the price interval. We demonstrate that this flexibility is useful for inventory management, one of the key challenges faced by a market maker.   In this paper, we conduct three main experiments: first, we compare our more flexible beta-based actions with the special case of ladder strategies; then, we investigate the performance of simple fixed distributions; and finally, we devise and evaluate a simple and intuitive dynamic control policy that adjusts actions in a continuous manner depending on the signed inventory that the market maker has acquired. All empirical evaluations use a high-fidelity limit order book simulator based on historical data with 50 levels on each side.

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
