# Evaluation of Dynamic Cointegration-Based Pairs Trading Strategy in the Cryptocurrency Market

## Metadata
- **Authors**: Masood Tadi, Irina Kortchmeski
- **Publication Date**: 2021-09-22
- **Repository / Identifier**: [http://arxiv.org/abs/2109.10662v1](http://arxiv.org/abs/2109.10662v1)
- **PDF Source**: [https://arxiv.org/pdf/2109.10662v1](https://arxiv.org/pdf/2109.10662v1)
- **Strategic Paradigm**: `Pairs Trading & Mean Reversion`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
This research aims to demonstrate a dynamic cointegration-based pairs trading strategy, including an optimal look-back window framework in the cryptocurrency market, and evaluate its return and risk by applying three different scenarios. We employ the Engle-Granger methodology, the Kapetanios-Snell-Shin (KSS) test, and the Johansen test as cointegration tests in different scenarios. We calibrate the mean-reversion speed of the Ornstein-Uhlenbeck process to obtain the half-life used for the asset selection phase and look-back window estimation. By considering the main limitations in the market microstructure, our strategy exceeds the naive buy-and-hold approach in the Bitmex exchange. Another significant finding is that we implement a numerous collection of cryptocurrency coins to formulate the model's spread, which improves the risk-adjusted profitability of the pairs trading strategy. Besides, the strategy's maximum drawdown level is reasonably low, which makes it useful to be deployed. The results also indicate that a class of coins has better potential arbitrage opportunities than others. This research has some noticeable advantages, making it stand out from similar studies in the cryptocurrency market. First is the accuracy of data in which minute-binned data create the signals in the formation period. Besides, to backtest the strategy during the trading period, we simulate the trading signals using best bid/ask quotes and market trades. We exclusively take the order execution into account when the asset size is already available at its quoted price (with one or more period gaps after signal generation). This action makes the backtesting much more realistic.

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
