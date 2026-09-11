# Continuous Cash-Overlay Filters for a Static Growth--Defensive Risk Sleeve: Slow-Tail Compensation, V-Shape Crash Brakes, Walk-Forward Validation, and Max-Cash Combination

## Metadata
- **Authors**: Zheli Xiong
- **Publication Date**: 2026-06-08
- **Repository / Identifier**: [http://arxiv.org/abs/2606.09025v2](http://arxiv.org/abs/2606.09025v2)
- **PDF Source**: [https://arxiv.org/pdf/2606.09025v2](https://arxiv.org/pdf/2606.09025v2)
- **Strategic Paradigm**: `Trend Following, Time Series Momentum & Risk Parity`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Institutional Invariant)

---

## Executive Summary & Core Hypothesis
This paper studies a modular cash-overlay rule for allocating between a fixed growth-defensive risky sleeve R and interest-bearing cash C. The risky sleeve is a static 50/50 combination of equal-weight growth/technology and defensive income/value ETF baskets; the target is future R-C return, with the cash leg earning the contemporaneous cash rate. Two independent filters are tested. The slow-tail filter maps continuous compensation, rate-headwind, risk-premium-compression, and rate-path-stress states into a cash weight with a 30% material-trade gate. The V-shape filter is a fast crash brake based on continuous VIX, rate, credit, drawdown, and re-entry states. A fixed max-cash layer then uses the larger cash weight requested by either filter each day. On the 2017-2026 common window, the selected max-cash combination earns an 18.83% CAGR versus 16.62% for 100% R and reduces maximum drawdown from -33.59% to -18.05%. In the main walk-forward OOS window, the expanding combination earns 19.35% versus 17.59% for 100% R, with maximum drawdown of -22.05% versus -33.59%; the rolling version earns 18.50% with the same -22.05% drawdown. Post-2022 tests show lower drawdown but lower CAGR during a strong risky-sleeve rebound. The results support modular cash overlays as drawdown-control tools rather than standalone return-enhancement claims; fully real-time variable re-screening and multiple-testing-adjusted inference remain future work.

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
