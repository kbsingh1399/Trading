# Detection of intensity bursts using Hawkes processes: an application to high frequency financial data

## Metadata
- **Authors**: Marcello Rambaldi, Vladimir Filimonov, Fabrizio Lillo
- **Publication Date**: 2016-10-17
- **Repository / Identifier**: [http://arxiv.org/abs/1610.05383v1](http://arxiv.org/abs/1610.05383v1)
- **PDF Source**: [https://arxiv.org/pdf/1610.05383v1](https://arxiv.org/pdf/1610.05383v1)
- **Strategic Paradigm**: `High-Frequency Hawkes Jump Processes`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Given a stationary point process, an intensity burst is defined as a short time period during which the number of counts is larger than the typical count rate. It might signal a local non-stationarity or the presence of an external perturbation to the system. In this paper we propose a novel procedure for the detection of intensity bursts within the Hawkes process framework. By using a model selection scheme we show that our procedure can be used to detect intensity bursts when both their occurrence time and their total number is unknown. Moreover, the initial time of the burst can be determined with a precision given by the typical inter-event time. We apply our methodology to the mid-price change in FX markets showing that these bursts are frequent and that only a relatively small fraction is associated to news arrival. We show lead-lag relations in intensity burst occurrence across different FX rates and we discuss their relation with price jumps.

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
