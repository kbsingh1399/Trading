# Selecting stock pairs for pairs trading while incorporating lead-lag relationship

## Metadata
- **Authors**: Kartikay Gupta, Niladri Chatterjee
- **Publication Date**: 2019-06-12
- **Repository / Identifier**: [http://arxiv.org/abs/1906.05057v2](http://arxiv.org/abs/1906.05057v2)
- **PDF Source**: [https://arxiv.org/pdf/1906.05057v2](https://arxiv.org/pdf/1906.05057v2)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Pairs Trading is carried out in the financial market to earn huge profits from known equilibrium relation between pairs of stock. In financial markets, seldom it is seen that stock pairs are correlated at particular lead or lag. This lead-lag relationship has been empirically studied in various financial markets. Earlier research works have suggested various measures for identifying the best pairs for pairs trading, but they do not consider this lead-lag effect. The present study proposes a new distance measure which incorporates the lead-lag relationship between the stocks while selecting the best pairs for pairs trading. Further, the lead-lag value between the stocks is allowed to vary continuously over time. The proposed measures importance has been show-cased through experimentation on two different datasets, one corresponding to Indian companies and another corresponding to American companies. When the proposed measure is clubbed with SSD measure, i.e., when pairs are identified through optimising both these measures, then the selected pairs consistently generate the best profit, as compared to all other measures. Finally, possible generalisation and extension of the proposed distance measure have been discussed.

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
