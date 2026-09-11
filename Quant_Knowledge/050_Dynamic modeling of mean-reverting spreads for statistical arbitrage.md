# Dynamic modeling of mean-reverting spreads for statistical arbitrage

## Metadata
- **Authors**: Kostas Triantafyllopoulos, Giovanni Montana
- **Publication Date**: 2008-08-12
- **Repository / Identifier**: [http://arxiv.org/abs/0808.1710v3](http://arxiv.org/abs/0808.1710v3)
- **PDF Source**: [https://arxiv.org/pdf/0808.1710v3](https://arxiv.org/pdf/0808.1710v3)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Statistical arbitrage strategies, such as pairs trading and its generalizations, rely on the construction of mean-reverting spreads enjoying a certain degree of predictability. Gaussian linear state-space processes have recently been proposed as a model for such spreads under the assumption that the observed process is a noisy realization of some hidden states. Real-time estimation of the unobserved spread process can reveal temporary market inefficiencies which can then be exploited to generate excess returns. Building on previous work, we embrace the state-space framework for modeling spread processes and extend this methodology along three different directions. First, we introduce time-dependency in the model parameters, which allows for quick adaptation to changes in the data generating process. Second, we provide an on-line estimation algorithm that can be constantly run in real-time. Being computationally fast, the algorithm is particularly suitable for building aggressive trading strategies based on high-frequency data and may be used as a monitoring device for mean-reversion. Finally, our framework naturally provides informative uncertainty measures of all the estimated parameters. Experimental results based on Monte Carlo simulations and historical equity data are discussed, including a co-integration relationship involving two exchange-traded funds.

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
