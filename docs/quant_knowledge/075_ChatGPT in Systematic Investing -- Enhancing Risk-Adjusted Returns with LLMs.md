# ChatGPT in Systematic Investing -- Enhancing Risk-Adjusted Returns with LLMs

## Metadata
- **Authors**: Nikolas Anic, Andrea Barbon, Ralf Seiz, Carlo Zarattini
- **Publication Date**: 2025-10-30
- **Repository / Identifier**: [http://arxiv.org/abs/2510.26228v1](http://arxiv.org/abs/2510.26228v1)
- **PDF Source**: [https://arxiv.org/pdf/2510.26228v1](https://arxiv.org/pdf/2510.26228v1)
- **Strategic Paradigm**: `Cross-Sectional Momentum & Relative Strength`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
This paper investigates whether large language models (LLMs) can improve cross-sectional momentum strategies by extracting predictive signals from firm-specific news. We combine daily U.S. equity returns for S&P 500 constituents with high-frequency news data and use prompt-engineered queries to ChatGPT that inform the model when a stock is about to enter a momentum portfolio. The LLM evaluates whether recent news supports a continuation of past returns, producing scores that condition both stock selection and portfolio weights. An LLM-enhanced momentum strategy outperforms a standard long-only momentum benchmark, delivering higher Sharpe and Sortino ratios both in-sample and in a truly out-of-sample period after the model's pre-training cut-off. These gains are robust to transaction costs, prompt design, and portfolio constraints, and are strongest for concentrated, high-conviction portfolios. The results suggest that LLMs can serve as effective real-time interpreters of financial news, adding incremental value to established factor-based investment strategies.

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
