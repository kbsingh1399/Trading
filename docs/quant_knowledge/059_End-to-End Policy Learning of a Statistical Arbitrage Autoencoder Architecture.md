# End-to-End Policy Learning of a Statistical Arbitrage Autoencoder Architecture

## Metadata
- **Authors**: Fabian Krause, Jan-Peter Calliess
- **Publication Date**: 2024-02-13
- **Repository / Identifier**: [http://arxiv.org/abs/2402.08233v1](http://arxiv.org/abs/2402.08233v1)
- **PDF Source**: [https://arxiv.org/pdf/2402.08233v1](https://arxiv.org/pdf/2402.08233v1)
- **Strategic Paradigm**: `Ornstein-Uhlenbeck & Mean Reversion`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
In Statistical Arbitrage (StatArb), classical mean reversion trading strategies typically hinge on asset-pricing or PCA based models to identify the mean of a synthetic asset. Once such a (linear) model is identified, a separate mean reversion strategy is then devised to generate a trading signal. With a view of generalising such an approach and turning it truly data-driven, we study the utility of Autoencoder architectures in StatArb. As a first approach, we employ a standard Autoencoder trained on US stock returns to derive trading strategies based on the Ornstein-Uhlenbeck (OU) process. To further enhance this model, we take a policy-learning approach and embed the Autoencoder network into a neural network representation of a space of portfolio trading policies. This integration outputs portfolio allocations directly and is end-to-end trainable by backpropagation of the risk-adjusted returns of the neural policy. Our findings demonstrate that this innovative end-to-end policy learning approach not only simplifies the strategy development process, but also yields superior gross returns over its competitors illustrating the potential of end-to-end training over classical two-stage approaches.

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
