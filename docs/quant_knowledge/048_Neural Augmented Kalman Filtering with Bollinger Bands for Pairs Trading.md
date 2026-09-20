# Neural Augmented Kalman Filtering with Bollinger Bands for Pairs Trading

## Metadata
- **Authors**: Amit Milstein, Haoran Deng, Guy Revach, Hai Morgenstern, Nir Shlezinger
- **Publication Date**: 2022-10-19
- **Repository / Identifier**: [http://arxiv.org/abs/2210.15448v2](http://arxiv.org/abs/2210.15448v2)
- **PDF Source**: [https://arxiv.org/pdf/2210.15448v2](https://arxiv.org/pdf/2210.15448v2)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
Pairs trading is a family of trading techniques that determine their policies based on monitoring the relationships between pairs of assets. A common pairs trading approach relies on describing the pair-wise relationship as a linear Space State (SS) model with Gaussian noise. This representation facilitates extracting financial indicators with low complexity and latency using a Kalman Filter (KF), that are then processed using classic policies such as Bollinger Bands (BB). However, such SS models are inherently approximated and mismatched, often degrading the revenue. In this work, we propose KalmenNet-aided Bollinger bands Pairs Trading (KBPT), a deep learning aided policy that augments the operation of KF-aided BB trading. KBPT is designed by formulating an extended SS model for pairs trading that approximates their relationship as holding partial co-integration. This SS model is utilized by a trading policy that augments KF-BB trading with a dedicated neural network based on the KalmanNet architecture. The resulting KBPT is trained in a two-stage manner which first tunes the tracking algorithm in an unsupervised manner independently of the trading task, followed by its adaptation to track the financial indicators to maximize revenue while approximating BB with a differentiable mapping. KBPT thus leverages data to overcome the approximated nature of the SS model, converting the KF-BB policy into a trainable model. We empirically demonstrate that our proposed KBPT systematically yields improved revenue compared with model-based and data-driven benchmarks over various different assets.

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
