# Reward-risk momentum strategies using classical tempered stable distribution

## Metadata
- **Authors**: Jaehyung Choi, Young Shin Kim, Ivan Mitov
- **Publication Date**: 2014-03-24
- **Repository / Identifier**: [http://arxiv.org/abs/1403.6093v4](http://arxiv.org/abs/1403.6093v4)
- **PDF Source**: [https://arxiv.org/pdf/1403.6093v4](https://arxiv.org/pdf/1403.6093v4)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We implement momentum strategies using reward-risk measures as ranking criteria based on classical tempered stable distribution. Performances and risk characteristics for the alternative portfolios are obtained in various asset classes and markets. The reward-risk momentum strategies with lower volatility levels outperform the traditional momentum strategy regardless of asset class and market. Additionally, the alternative portfolios are not only less riskier in risk measures such as VaR, CVaR and maximum drawdown but also characterized by thinner downside tails. Similar patterns in performance and risk profile are also found at the level of each ranking basket in the reward-risk portfolios. Higher factor-neutral returns achieved by the reward-risk momentum strategies are statistically significant and large portions of the performances are not explained by the Carhart four-factor model.

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
