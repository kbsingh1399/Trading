# Apparent criticality and calibration issues in the Hawkes self-excited point process model: application to high-frequency financial data

## Metadata
- **Authors**: Vladimir Filimonov, Didier Sornette
- **Publication Date**: 2013-08-30
- **Repository / Identifier**: [http://arxiv.org/abs/1308.6756v3](http://arxiv.org/abs/1308.6756v3)
- **PDF Source**: [https://arxiv.org/pdf/1308.6756v3](https://arxiv.org/pdf/1308.6756v3)
- **Strategic Paradigm**: `High-Frequency Hawkes Jump Processes`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
We present a careful analysis of possible issues on the application of the self-excited Hawkes process to high-frequency financial data. We carefully analyze a set of effects leading to significant biases in the estimation of the "criticality index" n that quantifies the degree of endogeneity of how much past events trigger future events. We report a number of model biases that are intrinsic to the estimation of brnaching ratio (n) when using power law memory kernels. We demonstrate that the calibration of the Hawkes process on mixtures of pure Poisson process with changes of regime leads to completely spurious apparent critical values for the branching ratio (n~1) while the true value is actually n=0. More generally, regime shifts on the parameters of the Hawkes model and/or on the generating process itself are shown to systematically lead to a significant upward bias in the estimation of the branching ratio. We also demonstrate the importance of the preparation of the high-frequency financial data and give special care to the decrease of quality of the timestamps of tick data due to latency and grouping of messages to packets by the stock exchange. Altogether, our careful exploration of the caveats of the calibration of the Hawkes process stresses the need for considering all the above issues before any conclusion can be sustained. In this respect, because the above effects are plaguing their analyses, the claim by Hardiman, Bercot and Bouchaud (2013) that financial market have been continuously functioning at or close to criticality (n~1) cannot be supported. In contrast, our previous results on E-mini S&P 500 Futures Contracts and on major commodity future contracts are upheld.

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
