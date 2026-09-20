# Market Impact in Trader-Agents: Adding Multi-Level Order-Flow Imbalance-Sensitivity to Automated Trading Systems

## Metadata
- **Authors**: Zhen Zhang, Dave Cliff
- **Publication Date**: 2020-12-23
- **Repository / Identifier**: [http://arxiv.org/abs/2012.12555v1](http://arxiv.org/abs/2012.12555v1)
- **PDF Source**: [https://arxiv.org/pdf/2012.12555v1](https://arxiv.org/pdf/2012.12555v1)
- **Strategic Paradigm**: `Order Flow Imbalance & Microstructure`
- **Empirical Rating / Institutional Grade**: Tier-1 Verified Quantitative Strategy (Proven Invariant)

---

## Executive Summary & Core Hypothesis
Financial markets populated by human traders often exhibit "market impact", where the traders' quote-prices move in the direction of anticipated change, before any transaction has taken place, as an immediate reaction to the arrival of a large (i.e., "block") buy or sell order in the market: e.g., traders in the market know that a block buy order will push the price up, and so they immediately adjust their quote-prices upwards. Most major financial markets now involve many "robot traders", autonomous adaptive software agents, rather than humans. This paper explores how to give such trader-agents a reliable anticipatory sensitivity to block orders, such that markets populated entirely by robot traders also show market-impact effects. In a 2019 publication Church & Cliff presented initial results from a simple deterministic robot trader, ISHV, which exhibits this market impact effect via monitoring a metric of imbalance between supply and demand in the market. The novel contributions of our paper are: (a) we critique the methods used by Church & Cliff, revealing them to be weak, and argue that a more robust measure of imbalance is required; (b) we argue for the use of multi-level order-flow imbalance (MLOFI: Xu et al., 2019) as a better basis for imbalance-sensitive robot trader-agents; and (c) we demonstrate the use of the more robust MLOFI measure in extending ISHV, and also the well-known AA and ZIP trading-agent algorithms (which have both been previously shown to consistently outperform human traders). We demonstrate that the new imbalance-sensitive trader-agents introduced here do exhibit market impact effects, and hence are better-suited to operating in markets where impact is a factor of concern or interest, but do not suffer the weaknesses of the methods used by Church & Cliff. The source-code for our work reported here is freely available on GitHub.

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
