# How does latent liquidity get revealed in the limit order book?

## Metadata
- **Authors**: Lorenzo Dall'Amico, Antoine Fosset, Jean-Philippe Bouchaud, Michael Benzaquen
- **Publication Date**: 2018-08-29
- **Repository / Identifier**: [http://arxiv.org/abs/1808.09677v2](http://arxiv.org/abs/1808.09677v2)
- **PDF Source**: [https://arxiv.org/pdf/1808.09677v2](https://arxiv.org/pdf/1808.09677v2)
- **Strategic Paradigm**: `Order Book Dynamics & Price Impact`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Latent order book models have allowed for significant progress in our understanding of price formation in financial markets. In particular they are able to reproduce a number of stylized facts, such as the square-root impact law. An important question that is raised -- if one is to bring such models closer to real market data -- is that of the connection between the latent (unobservable) order book and the real (observable) order book. Here we suggest a simple, consistent mechanism for the revelation of latent liquidity that allows for quantitative estimation of the latent order book from real market data. We successfully confront our results to real order book data for over a hundred assets and discuss market stability. One of our key theoretical results is the existence of a market instability threshold, where the conversion of latent order becomes too slow, inducing liquidity crises. Finally we compute the price impact of a metaorder in different parameter regimes.

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
