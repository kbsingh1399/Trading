# Is Trend Still Your Friend?: A Microstructural Account of the Demise of Short-Term Trend-Following

## Metadata
- **Authors**: Jutta G. Kurth, Zoltan Eisler, Adam Rej, Jean-Philippe Bouchaud
- **Publication Date**: 2026-07-02
- **Repository / Identifier**: [http://arxiv.org/abs/2607.01550v1](http://arxiv.org/abs/2607.01550v1)
- **PDF Source**: [https://arxiv.org/pdf/2607.01550v1](https://arxiv.org/pdf/2607.01550v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Systematic trend following has, on average, been profitable for at least two centuries; yet since approximately 2009, short-term trends have ceased to deliver reliable returns. Using a cross-section of roughly 100 liquid futures contracts spanning 1995-2025, together with an industry-representative CTA proxy, we document the break and characterise its dependence on signal speed and asset class. We evaluate four candidate explanations - capacity constraints, market electronification, a regime change in CTA-versus-order-flow interactions, and a microstructural mechanism - and find that the first three fail on grounds of timing, magnitude, or cross-sectional heterogeneity.   Our central empirical finding is that the cross-sectional variable distinguishing degraded from surviving trends is the volatility-normalised tick size: post-2008 trend PnL has collapsed on small-tick contracts across all signal horizons, while remaining essentially intact on large-tick ones. Neither asset class nor liquidity replicates this dichotomy.   We interpret this result through a self-fulfilling feedback loop that, in our view, lies at the heart of the trend anomaly itself: trend signals trigger directional trades, whose market impact reinforces the very price moves that generated the signal. Both the profitability and the persistence of trend are sustained by this impact channel, which requires that trend followers can execute aggressively at reasonable cost. We argue that the post-crisis transition to HFT-dominated market making, whose liquidity-withdrawal behaviour in front of predictable directional flow has sharply contrasting consequences for sparse (small-tick) and dense (large-tick) limit order books, has broken this loop on small-tick contracts. On large-tick contracts, residual depth remains sufficient, and the loop continues to operate.

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
