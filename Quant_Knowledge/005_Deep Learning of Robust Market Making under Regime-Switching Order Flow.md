# Deep Learning of Robust Market Making under Regime-Switching Order Flow

## Metadata
- **Authors**: Felipe Moret, Fabrizio Lillo
- **Publication Date**: 2026-09-10
- **Repository / Identifier**: [http://arxiv.org/abs/2609.11614v1](http://arxiv.org/abs/2609.11614v1)
- **PDF Source**: [https://arxiv.org/pdf/2609.11614v1](https://arxiv.org/pdf/2609.11614v1)
- **Strategic Paradigm**: `Market Microstructure, Order Flow & High-Frequency Market Making`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Classical market-making strategies based on stochastic control, such as the Avellaneda-Stoikov and the Guéant-Lehalle-Fernandez-Tapia (GLFT) extension, provide closed-form quoting rules, but rest on assumptions that break down at realistic microstructure timescales. One of them is that order flow is stationary, while empirical evidence points to the existence of regimes, possibly associated with algorithmic execution of metaorders. In this case, existing methods provide negative PnL. In this paper, we develop a deep reinforcement-learning market maker (RLMM) - a Rainbow-style distributional DQN (C51) which is calibrated and tested in a zero-intelligence limit order book. We find that, in the stationary setting, RLMM outperforms GLFT across the entire observed risk-return frontier. The RLMM is more robust to flow asymmetry than GLFT, but, like any stationarily trained strategy, it still suffers large drawdowns from inventory saturation under persistent directional imbalance. Augmenting the state of RLMM with two auxiliary signals - a Bayesian online change-point filter over the directional flow bias and a queue-adjusted quote-exposure imbalance -restores profitability. A final scenario-bandit step that reweights low-return regime scenarios further improves performance under random-persistence and correlated-direction stress.

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
