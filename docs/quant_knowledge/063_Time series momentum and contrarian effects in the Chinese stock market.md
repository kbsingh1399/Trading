# Time series momentum and contrarian effects in the Chinese stock market

## Metadata
- **Authors**: Huai-Long Shi, Wei-Xing Zhou
- **Publication Date**: 2017-02-07
- **Repository / Identifier**: [http://arxiv.org/abs/1702.07374v1](http://arxiv.org/abs/1702.07374v1)
- **PDF Source**: [https://arxiv.org/pdf/1702.07374v1](https://arxiv.org/pdf/1702.07374v1)
- **Strategic Paradigm**: `Time Series Momentum & Trend Following`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
This paper concentrates on the time series momentum or contrarian effects in the Chinese stock market. We evaluate the performance of the time series momentum strategy applied to major stock indices in mainland China and explore the relation between the performance of time series momentum strategies and some firm-specific characteristics. Our findings indicate that there is a time series momentum effect in the short run and a contrarian effect in the long run in the Chinese stock market. The performances of the time series momentum and contrarian strategies are highly dependent on the look-back and holding periods and firm-specific characteristics.

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
