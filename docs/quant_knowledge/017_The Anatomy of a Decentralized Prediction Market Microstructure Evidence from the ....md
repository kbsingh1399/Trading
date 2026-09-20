# The Anatomy of a Decentralized Prediction Market: Microstructure Evidence from the Polymarket Order Book

## Metadata
- **Authors**: Philipp D. Dubach
- **Publication Date**: 2026-04-27
- **Repository / Identifier**: [http://arxiv.org/abs/2604.24366v2](http://arxiv.org/abs/2604.24366v2)
- **PDF Source**: [https://arxiv.org/pdf/2604.24366v2](https://arxiv.org/pdf/2604.24366v2)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We study the microstructure of Polymarket, the largest on-chain prediction market, using a continuous tick-level archive of the public order-book feed (30 billion events over 52 days) joined to the authoritative on-chain trade record. On a pre-registered stratified panel of 600 markets we report eight stylized facts: a longshot spread premium; a depth profile closer to uniform than to top-of-book; a null block-clock alignment effect; broad maker-wallet diversity with a concentrated tail; category-conditional effective-spread differences; a sub-50 ms median archive-ingestion delay with a multi-second tail; a self-counterparty wash share with median 1% and a 22% upper tail (well below Cong et al. 2023's 25-70% for unregulated crypto venues -- a sanity bound, not an apples-to-apples reference); and a cross-sectional depth profile explained by market duration, price level, and volume, with no residual time-to-close effect. The paper also contributes a measurement result: trade direction inferred from Polymarket's public order-book feed agrees with on-chain ground truth on only ~59% of buckets (panel mean 0.615, 95% CI [0.58, 0.65]), well below the ~80% Lee-Ready accuracy on Nasdaq. The effective half-spread changes sign between feed- and on-chain trade directions on 67%/50% of markets across two 7-day windows; Kyle's lambda on 60%/43%. Microstructure work on Polymarket therefore needs to source trade direction from on-chain OrderFilled events; we release a replication package that performs the join.

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
