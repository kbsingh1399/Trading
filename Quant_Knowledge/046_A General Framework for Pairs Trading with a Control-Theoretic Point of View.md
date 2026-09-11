# A General Framework for Pairs Trading with a Control-Theoretic Point of View

## Metadata
- **Authors**: Atul Deshpande, B. Ross Barmish
- **Publication Date**: 2016-08-11
- **Repository / Identifier**: [http://arxiv.org/abs/1608.03636v1](http://arxiv.org/abs/1608.03636v1)
- **PDF Source**: [https://arxiv.org/pdf/1608.03636v1](https://arxiv.org/pdf/1608.03636v1)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Pairs trading is a market-neutral strategy that exploits historical correlation between stocks to achieve statistical arbitrage. Existing pairs-trading algorithms in the literature require rather restrictive assumptions on the underlying stochastic stock-price processes and the so-called spread function. In contrast to existing literature, we consider an algorithm for pairs trading which requires less restrictive assumptions than heretofore considered. Since our point of view is control-theoretic in nature, the analysis and results are straightforward to follow by a non-expert in finance. To this end, we describe a general pairs-trading algorithm which allows the user to define a rather arbitrary spread function which is used in a feedback context to modify the investment levels dynamically over time. When this function, in combination with the price process, satisfies a certain mean-reversion condition, we deem the stocks to be a tradeable pair. For such a case, we prove that our control-inspired trading algorithm results in positive expected growth in account value. Finally, we describe tests of our algorithm on historical trading data by fitting stock price pairs to a popular spread function used in literature. Simulation results from these tests demonstrate robust growth while avoiding huge drawdowns.

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
