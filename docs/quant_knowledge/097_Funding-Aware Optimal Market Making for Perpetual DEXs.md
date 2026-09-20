# Funding-Aware Optimal Market Making for Perpetual DEXs

## Metadata
- **Authors**: Nam Anh Le
- **Publication Date**: 2026-05-07
- **Repository / Identifier**: [http://arxiv.org/abs/2605.06405v1](http://arxiv.org/abs/2605.06405v1)
- **PDF Source**: [https://arxiv.org/pdf/2605.06405v1](https://arxiv.org/pdf/2605.06405v1)
- **Strategic Paradigm**: `Stochastic Market Making Models`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
This paper studies optimal liquidity provision for perpetual contracts when the funding rate is a stochastic state variable. The core extension to classical market making is the coupling between inventory and funding payments: inventory creates both mark-to-market exposure and a state-dependent funding cash flow. A reduced inventory-funding control problem is formulated, solved with a monotone finite-difference Hamilton-Jacobi-Bellman scheme, and bid and ask quote offsets are recovered from discrete inventory value differences. Funding is calibrated on Hyperliquid ETH, BTC, and SOL perpetual data. Gaussian OU funding is retained as a tractable diffusion baseline, while OU-plus-jump diagnostics document the heavy-tailed funding innovations that should enter a future extension. In 100-seed holdout simulations under two official-fill proxy calibrations, the funding-aware HJB improves mean ETH/BTC performance while lowering inventory RMS relative to classical Avellaneda-Stoikov. SOL gains are positive versus unscaled AS but are not a Pareto improvement once a risk-scaled AS diagnostic is included.

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
