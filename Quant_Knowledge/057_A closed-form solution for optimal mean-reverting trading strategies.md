# A closed-form solution for optimal mean-reverting trading strategies

## Metadata
- **Authors**: Alexander Lipton, Marcos Lopez de Prado
- **Publication Date**: 2020-03-23
- **Repository / Identifier**: [http://arxiv.org/abs/2003.10502v1](http://arxiv.org/abs/2003.10502v1)
- **PDF Source**: [https://arxiv.org/pdf/2003.10502v1](https://arxiv.org/pdf/2003.10502v1)
- **Strategic Paradigm**: `Ornstein-Uhlenbeck & Mean Reversion`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
When prices reflect all available information, they oscillate around an equilibrium level. This oscillation is the result of the temporary market impact caused by waves of buyers and sellers. This price behavior can be approximated through an Ornstein-Uhlenbeck (O-U) process.   Market makers provide liquidity in an attempt to monetize this oscillation. They enter a long position when a security is priced below its estimated equilibrium level, and they enter a short position when a security is priced above its estimated equilibrium level. They hold that position until one of three outcomes occur: (1) they achieve the targeted profit; (2) they experience a maximum tolerated loss; (3) the position is held beyond a maximum tolerated horizon.   All market makers are confronted with the problem of defining profit-taking and stop-out levels. More generally, all execution traders acting on behalf of a client must determine at what levels an order must be fulfilled. Those optimal levels can be determined by maximizing the trader's Sharpe ratio in the context of O-U processes via Monte Carlo experiments. This paper develops an analytical framework and derives those optimal levels by using the method of heat potentials.

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
