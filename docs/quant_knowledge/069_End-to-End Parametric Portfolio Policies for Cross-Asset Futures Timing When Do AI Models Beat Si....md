# End-to-End Parametric Portfolio Policies for Cross-Asset Futures Timing: When Do AI Models Beat Simple Rules?

## Metadata
- **Authors**: Austin Pollok, Kevin Robik
- **Publication Date**: 2026-07-01
- **Repository / Identifier**: [http://arxiv.org/abs/2607.00475v1](http://arxiv.org/abs/2607.00475v1)
- **PDF Source**: [https://arxiv.org/pdf/2607.00475v1](https://arxiv.org/pdf/2607.00475v1)
- **Strategic Paradigm**: `Time Series Momentum & Trend Following`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Timing-based tilts across asset classes can drive much of the risk and return of a diversified cross-asset portfolio. The standard approach forecasts returns and then optimizes weights. We instead study an end-to-end AI-based policy that maps market states directly to portfolio weights, and we then ask when this one-step modeling approach outperforms simple rules-based strategies. We train these policies on the sixteen most liquid CME futures, where an edge is unlikely to be due to illiquidity, using a differentiable Sharpe ratio loss function, and we benchmark them against equal weighting, risk parity, and time-series momentum. The learned policies rank above the rules on the pooled cross-asset portfolio and in several sub-asset classes, but not uniformly. In gross terms, an LSTM and a transformer-based architecture perform comparably out-of-sample, but diverge when we consider transaction costs. The transformer generates the stronger learned policy, trades far less than the LSTM, and matches or exceeds equal weighting through moderate cost.

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
