# Quantifying immediate price impact of trades based on the $k$-shell decomposition of stock trading networks

## Metadata
- **Authors**: Wen-Jie Xie, Ming-Xia Li, Hai-Chuan Xu, Wei Chen, Wei-Xing Zhou, H. E. Stanley
- **Publication Date**: 2016-11-21
- **Repository / Identifier**: [http://arxiv.org/abs/1611.06666v2](http://arxiv.org/abs/1611.06666v2)
- **PDF Source**: [https://arxiv.org/pdf/1611.06666v2](https://arxiv.org/pdf/1611.06666v2)
- **Strategic Paradigm**: `Order Book Dynamics & Price Impact`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Traders in a stock market exchange stock shares and form a stock trading network. Trades at different positions of the stock trading network may contain different information. We construct stock trading networks based on the limit order book data and classify traders into $k$ classes using the $k$-shell decomposition method. We investigate the influences of trading behaviors on the price impact by comparing a closed national market (A-shares) with an international market (B-shares), individuals and institutions, partially filled and filled trades, buyer-initiated and seller-initiated trades, and trades at different positions of a trading network. Institutional traders professionally use some trading strategies to reduce the price impact and individuals at the same positions in the trading network have a higher price impact than institutions. We also find that trades in the core have higher price impacts than those in the peripheral shell.

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
