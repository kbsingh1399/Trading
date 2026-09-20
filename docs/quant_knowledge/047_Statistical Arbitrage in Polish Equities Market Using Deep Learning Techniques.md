# Statistical Arbitrage in Polish Equities Market Using Deep Learning Techniques

## Metadata
- **Authors**: Marek Adamczyk, Michał Dąbrowski
- **Publication Date**: 2025-11-20
- **Repository / Identifier**: [http://arxiv.org/abs/2512.02037v1](http://arxiv.org/abs/2512.02037v1)
- **PDF Source**: [https://arxiv.org/pdf/2512.02037v1](https://arxiv.org/pdf/2512.02037v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We study a systematic approach to a popular Statistical Arbitrage technique: Pairs Trading. Instead of relying on two highly correlated assets, we replace the second asset with a replication of the first using risk factor representations. These factors are obtained through Principal Components Analysis (PCA), exchange traded funds (ETFs), and, as our main contribution, Long Short Term Memory networks (LSTMs). Residuals between the main asset and its replication are examined for mean reversion properties, and trading signals are generated for sufficiently fast mean reverting portfolios.   Beyond introducing a deep learning based replication method, we adapt the framework of Avellaneda and Lee (2008) to the Polish market. Accordingly, components of WIG20, mWIG40, and selected sector indices replace the original S&P500 universe, and market parameters such as the risk free rate and transaction costs are updated to reflect local conditions.   We outline the full strategy pipeline: risk factor construction, residual modeling via the Ornstein Uhlenbeck process, and signal generation. Each replication technique is described together with its practical implementation. Strategy performance is evaluated over two periods: 2017-2019 and the recessive year 2020.   All methods yield profits in 2017-2019, with PCA achieving roughly 20 percent cumulative return and an annualized Sharpe ratio of up to 2.63. Despite multiple adaptations, our conclusions remain consistent with those of the original paper. During the COVID-19 recession, only the ETF based approach remains profitable (about 5 percent annual return), while PCA and LSTM methods underperform. LSTM results, although negative, are promising and indicate potential for future optimization.

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
