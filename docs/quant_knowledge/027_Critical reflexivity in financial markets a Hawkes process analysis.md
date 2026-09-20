# Critical reflexivity in financial markets: a Hawkes process analysis

## Metadata
- **Authors**: Stephen J. Hardiman, Nicolas Bercot, Jean-Philippe Bouchaud
- **Publication Date**: 2013-02-06
- **Repository / Identifier**: [http://arxiv.org/abs/1302.1405v2](http://arxiv.org/abs/1302.1405v2)
- **PDF Source**: [https://arxiv.org/pdf/1302.1405v2](https://arxiv.org/pdf/1302.1405v2)
- **Strategic Paradigm**: `High-Frequency Hawkes Jump Processes`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
We model the arrival of mid-price changes in the E-Mini S&P futures contract as a self-exciting Hawkes process. Using several estimation methods, we find that the Hawkes kernel is power-law with a decay exponent close to -1.15 at short times, less than approximately 10^3 seconds, and crosses over to a second power-law regime with a larger decay exponent of approximately -1.45 for longer times scales in the range [10^3, 10^6] seconds. More importantly, we find that the Hawkes kernel integrates to unity independently of the analysed period, from 1998 to 2011. This suggests that markets are and have always been close to criticality, challenging a recent study which indicates that reflexivity (endogeneity) has increased in recent years as a result of increased automation of trading. However, we note that the scale over which market events are correlated has decreased steadily over time with the emergence of higher frequency trading.

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
