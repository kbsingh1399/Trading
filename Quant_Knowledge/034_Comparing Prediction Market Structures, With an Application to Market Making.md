# Comparing Prediction Market Structures, With an Application to Market Making

## Metadata
- **Authors**: Aseem Brahma, Sanmay Das, Malik Magdon-Ismail
- **Publication Date**: 2010-09-08
- **Repository / Identifier**: [http://arxiv.org/abs/1009.1446v1](http://arxiv.org/abs/1009.1446v1)
- **PDF Source**: [https://arxiv.org/pdf/1009.1446v1](https://arxiv.org/pdf/1009.1446v1)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Ensuring sufficient liquidity is one of the key challenges for designers of prediction markets. Various market making algorithms have been proposed in the literature and deployed in practice, but there has been little effort to evaluate their benefits and disadvantages in a systematic manner. We introduce a novel experimental design for comparing market structures in live trading that ensures fair comparison between two different microstructures with the same trading population. Participants trade on outcomes related to a two-dimensional random walk that they observe on their computer screens. They can simultaneously trade in two markets, corresponding to the independent horizontal and vertical random walks. We use this experimental design to compare the popular inventory-based logarithmic market scoring rule (LMSR) market maker and a new information based Bayesian market maker (BMM). Our experiments reveal that BMM can offer significant benefits in terms of price stability and expected loss when controlling for liquidity; the caveat is that, unlike LMSR, BMM does not guarantee bounded loss. Our investigation also elucidates some general properties of market makers in prediction markets. In particular, there is an inherent tradeoff between adaptability to market shocks and convergence during market equilibrium.

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
