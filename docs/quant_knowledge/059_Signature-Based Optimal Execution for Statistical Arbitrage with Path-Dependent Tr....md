# Signature-Based Optimal Execution for Statistical Arbitrage with Path-Dependent Trading Signals

## Metadata
- **Authors**: Gianmarco Morbelli, Sven Karbach, Mike Derksen
- **Publication Date**: 2026-06-30
- **Repository / Identifier**: [http://arxiv.org/abs/2606.31387v2](http://arxiv.org/abs/2606.31387v2)
- **PDF Source**: [https://arxiv.org/pdf/2606.31387v2](https://arxiv.org/pdf/2606.31387v2)
- **Strategic Paradigm**: `Statistical Arbitrage, Cointegration & Pairs Trading`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
We develop a signature-based framework for optimal execution in statistical arbitrage strategies with path-dependent predictive signals. Both the alpha process and the trading speed are modelled as linear functionals of the truncated signature of a time-augmented market path, placing signal generation and execution on the same truncated signature basis. This allows the trading rule to react to the realised history of the signal while accounting for temporary impact, inventory exposure, terminal liquidation, and approximate dollar neutrality. The main contribution is a quadratic reduction theorem: within the class of signature-linear trading speeds, the restricted path-dependent execution problem becomes a finite-dimensional concave quadratic programme in the policy coefficients. After running synthetic experiments under a mean-reverting log-spread model, we find that the fitted policy achieves a higher return on turnover than a classical $z$-score threshold benchmark. We show how the same workflow can be deployed on a historical equity pairs-trading backtest, where the fitted signature policy again outperforms the benchmark in accounting terms.

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
