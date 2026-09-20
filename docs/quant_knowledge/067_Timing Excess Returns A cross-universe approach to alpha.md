# Timing Excess Returns A cross-universe approach to alpha

## Metadata
- **Authors**: Marc Rohloff, Alexander Vogt
- **Publication Date**: 2020-02-11
- **Repository / Identifier**: [http://arxiv.org/abs/2002.04304v1](http://arxiv.org/abs/2002.04304v1)
- **PDF Source**: [https://arxiv.org/pdf/2002.04304v1](https://arxiv.org/pdf/2002.04304v1)
- **Strategic Paradigm**: `Time Series Momentum & Trend Following`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
We present a simple model that uses time series momentum in order to construct strategies that systematically outperform their benchmark. The simplicity of our model is elegant: We only require a benchmark time series and several related investable indizes, not requiring regression or other models to estimate our parameters. We find that our one size fits all approach delivers significant outperformance in both equity and bond markets while meeting the ex-ante risk requirements, nearly doubling yearly returns vs. the MSCI World and Bloomberg Barclays Euro Aggregate Corporate Bond benchmarks in a long-only backtest. We then combine both approaches into an absolute return strategy by benchmarking vs. the Eonia Total Return Index and find significant outperformance at a sharpe ratio of 1.8. Furthermore, we demonstrate that our model delivers a benefit versus a static portfolio with fixed mean weights, showing that timing of excess return momentum has a sizeable benefit vs. static allocations. This also applies to the passively investable equity factors, where we outperform a static factor exposure portfolio with statistical significance. Also, we show that our model delivers an alpha after deducting transaction costs.

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
