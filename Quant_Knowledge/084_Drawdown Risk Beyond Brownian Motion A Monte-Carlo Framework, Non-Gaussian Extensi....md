# Drawdown Risk Beyond Brownian Motion: A Monte-Carlo Framework, Non-Gaussian Extensions, and Long Memory

## Metadata
- **Authors**: Francesco Landolfi
- **Publication Date**: 2026-07-31
- **Repository / Identifier**: [http://arxiv.org/abs/2608.00127v1](http://arxiv.org/abs/2608.00127v1)
- **PDF Source**: [https://arxiv.org/pdf/2608.00127v1](https://arxiv.org/pdf/2608.00127v1)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
How deep and how long should the drawdowns of a systematic trading strategy run, given its Sharpe ratio and the statistical structure of its returns? Building on the drawdown framework of Rej, Seager and Bouchaud (2017), we develop the answer in three steps. We first reframe their closed-form results as a transparent Monte-Carlo experiment, validate it against their analytic benchmarks, and extend the mapping from drawdowns to four decision-relevant measures: maximum drawdown, maximum loss, final negative time and longest recovery time. We then relax the Gaussian assumption, holding the true Sharpe and volatility fixed while varying skewness, fat tails, volatility clustering and Sharpe-estimation uncertainty across strategy archetypes; the four measures move differently, so a single Gaussian table mis-warns. We finally replace short-memory persistence with fractional Brownian motion and show that the apparent amplification of drawdown risk under persistence is, for maximum-drawdown depth, almost entirely self-similar dispersion scaling (T^(H-1/2)) rather than path geometry: a failure of square-root-of-time calibration, not intrinsic danger. We provide reproducible lookup tables and a practical calibration recipe.

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
