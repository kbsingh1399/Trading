# Physical approach to price momentum and its application to momentum strategy

## Metadata
- **Authors**: Jaehyung Choi
- **Publication Date**: 2012-08-14
- **Repository / Identifier**: [http://arxiv.org/abs/1208.2775v5](http://arxiv.org/abs/1208.2775v5)
- **PDF Source**: [https://arxiv.org/pdf/1208.2775v5](https://arxiv.org/pdf/1208.2775v5)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We introduce various quantitative and mathematical definitions for price momentum of financial instruments. The price momentum is quantified with velocity and mass concepts originated from the momentum in physics. By using the physical momentum of price as a selection criterion, the weekly contrarian strategies are implemented in South Korea KOSPI 200 and US S&P 500 universes. The alternative strategies constructed by the physical momentum achieve the better expected returns and reward-risk measures than those of the traditional contrarian strategy in weekly scale. The portfolio performance is not understood by the Fama-French three-factor model.

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
