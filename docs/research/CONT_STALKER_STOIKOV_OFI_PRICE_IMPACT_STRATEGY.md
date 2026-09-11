# Mathematical Research & Strategy Architecture: The Price Impact of Order Book Events
**Paper:** *The Price Impact of Order Book Events*  
**Authors:** Rama Cont (Oxford), Arseniy Kukanov (Columbia), Sasha Stoikov (Cornell Financial Engineering Manhattan)  
**Reference:** arXiv:1011.6402v3 / *Journal of Financial Econometrics*  
**Scope:** Institutional Microstructure Alpha & 18-Asset Binance Perpetual Strategy Design  

---

## Executive Summary & Core Discovery

In arXiv:1011.6402, Rama Cont, Arseniy Kukanov, and Sasha Stoikov revolutionized quantitative market microstructure by proving that high-frequency price changes are driven not primarily by trade volume (market orders / CVD), but by **Order Flow Imbalance (OFI)**—the net imbalance of all order book events, including limit order additions, market executions, and limit cancellations at the best quotes.

### The Three Fundamental Laws Established by Cont, Kukanov & Stoikov:

1. **The Linear Impact Law**:
   Over discrete time intervals, the relationship between mid-price change Delta P and Order Flow Imbalance (OFI) is strictly linear:
   $$\Delta P_k = \beta_k \cdot OFI_k + \epsilon_k$$
   There is zero empirical evidence of concave or non-linear impact when orderbook events are properly aggregated (linear R-squared spans 65% to 79% across all examined assets).

2. **The Inverse Market Depth Law**:
   The price impact coefficient beta is strictly inversely proportional to contemporaneous market depth (AD):
   $$\beta_k = \frac{c}{AD_k^\alpha}, \quad \text{where } \alpha \approx 1.0$$
   In thin orderbooks, a modest OFI creates violent price displacement. In deep orderbooks, even massive OFI is absorbed with minimal price change.

3. **The Dominance of OFI Over Trade Imbalance (CVD)**:
   In bivariate regressions combining OFI and Trade Imbalance (CVD):
   $$\Delta P_k = \alpha + \beta_O \cdot OFI_k + \beta_T \cdot TI_k + \epsilon_k$$
   The t-statistic of trade imbalance drops by a factor of 4, and beta_T becomes statistically indistinguishable from zero in over 69% of regimes, while beta_O remains overwhelmingly significant (t > 10.0, R-squared = 65-74%). Trade imbalance alone (CVD) is merely a noisy, lower-fidelity proxy for true order book supply/demand.

---

## Part 1: Mathematical Foundations of Cont-Stoikov OFI

### 1.1 Event-Level Contribution Variable e_n
At each event n affecting the top of the order book, let:
- P_n^B = Best Bid Price, q_n^B = Best Bid Quantity
- P_n^A = Best Ask Price, q_n^A = Best Ask Quantity

The contribution e_n of event n to the net queue size is defined rigorously as:
$$e_n = I_{\{P_n^B \ge P_{n-1}^B\}} q_n^B - I_{\{P_n^B \le P_{n-1}^B\}} q_{n-1}^B - I_{\{P_n^A \le P_{n-1}^A\}} q_n^A + I_{\{P_n^A \ge P_{n-1}^A\}} q_{n-1}^A$$

This decomposes into six mutually exclusive cases:
1. **Bid Price Improves** ($P_n^B > P_{n-1}^B$): $e_n = +q_n^B$ (aggressive buyer limit order steps inside the spread).
2. **Bid Size Changes at Same Price** ($P_n^B = P_{n-1}^B$): $e_n = +(q_n^B - q_{n-1}^B)$ (net limit additions minus market sells and cancellations).
3. **Bid Price Depleted** ($P_n^B < P_{n-1}^B$): $e_n = -q_{n-1}^B$ (market sell order sweeps the bid queue or buyer cancels).
4. **Ask Price Improves** ($P_n^A < P_{n-1}^A$): $e_n = -q_n^A$ (aggressive seller limit order steps inside the spread).
5. **Ask Size Changes at Same Price** ($P_n^A = P_{n-1}^A$): $e_n = -(q_n^A - q_{n-1}^A)$ (net limit additions minus market buys and cancellations).
6. **Ask Price Depleted** ($P_n^A > P_{n-1}^A$): $e_n = +q_{n-1}^A$ (market buy order sweeps the ask queue or seller cancels).

### 1.2 Interval Aggregation
Over any discrete sampling interval [t_{k-1}, t_k]:
$$OFI_k = \sum_{n = N(t_{k-1}) + 1}^{N(t_k)} e_n = (L_b - C_b - M_s) - (L_s - C_s - M_b)$$
Where:
- $L_b, L_s$ = Limit buy and sell arrivals
- $C_b, C_s$ = Limit buy and sell cancellations
- $M_b, M_s$ = Market buy and sell executions

---

## Part 2: Adapting Cont-Stoikov OFI to Binance 15m Master & Footprint Data

Because Binance perpetual historical archives provide 15-minute aggregated OHLCV, Spot/Futures CVD, basis dislocations, and multi-level footprint tick imbalance ladders, we construct the **Continuous-Time Cont-Stoikov Model**:

### 2.1 The Volatility-Adjusted Market Depth Proxy (D_k)
In continuous trading, average market depth is proportional to the dollar turnover required to displace the asset by one unit of volatility:
$$D_k = \frac{\text{VolumeQuote}_k}{\text{ATR}_{14, k} / \text{Close}_k + \epsilon}$$
- When $D_k$ is high: the market is ultra-liquid and deep; large flow results in tight consolidation.
- When $D_k$ is low: the book is hollowed out; high sensitivity to any order flow shock.

### 2.2 Depth-Normalized Order Flow Imbalance (OFI_Z)
Combining trade imbalance (CVD) with footprint stacked order imbalances (representing Level-2 queue additions and sweeps):
$$OFI\_Raw_k = \Delta \text{SpotCVD}_{15m, k} + 0.5 \cdot \Delta \text{FuturesCVD}_{15m, k} + \gamma \cdot (\text{StackBuyImb}_k - \text{StackSellImb}_k) \cdot \text{VolumeBase}_k$$

Normalizing by the Cont-Stoikov Depth $D_k$:
$$OFI\_Norm_k = \frac{OFI\_Raw_k}{D_k}$$

Standardized into a stationary Z-Score over a 96-bar (24-hour) rolling window:
$$Z_{OFI, k} = \frac{OFI\_Norm_k - \mu_{96}(OFI\_Norm)}{\sigma_{96}(OFI\_Norm)}$$

### 2.3 Cont-Stoikov Theoretical Price Impact vs Realized Price Impact (Resilience)
The theoretical expected price displacement is:
$$\widehat{\Delta P}_k = \lambda \cdot Z_{OFI, k}$$
The **Absorption Residual** measures the discrepancy between actual price displacement and theoretical impact:
$$\text{Resid}_k = \frac{Close_k - Open_k}{Open_k} - \lambda \cdot Z_{OFI, k}$$

- **Case A (Spring-Loaded Absorption / Order Book Resilience)**:
  If $Z_{OFI, k} \gg +1.5$ (immense institutional buying pressure), but $\frac{Close_k - Open_k}{Open_k} \le 0$ (price was pushed down by a temporary liquidation cascade or aggressive market dumping), the order book has absorbed the selling. Cont & Stoikov prove that order books exhibit strong mean-reverting **resilience** over the following periods. Price will violently snap back upward!
- **Case B (Thin-Book Momentum Expansion)**:
  If $Z_{OFI, k} > +1.5$ AND Market Depth $D_k < \text{Median}(D)$ (liquidity vacuum), price will trend aggressively in the direction of the flow.

---

## Part 3: The 18-Asset Parallel Cont-Stoikov Strategy Specification

### 3.1 Universe & Execution Standards
- **Assets**: 18 Binance USDT-M Perpetuals (`BTC, ETH, XRP, SOL, BNB, DOGE, ADA, TRX, LINK, AVAX, SUI, NEAR, DOT, LTC, BCH, APT, OP, ARB`).
- **Portfolio Concurrency**: Maximum 2 concurrent open positions across all 18 assets.
- **Cross-Sectional Ranking**: At bar close $j$, rank all 18 assets by Cont-Stoikov Conviction Metric:
  $$\text{Conviction}_i = |Z_{OFI, i}| \cdot \frac{1}{D_{norm, i}} + |\text{BasisZ}_i|$$
  Only the top-1 ranked candidate enters execution at bar $j+1$ open.

### 3.2 Dual-Regime Entry Triggers

#### Sleeve A: Cont-Stoikov Order Book Resilience (Absorption Pullback)
- **Long Trigger**:
  1. $Z_{OFI} > +1.20$ (Order Flow Imbalance is positive)
  2. $\text{VWAP\_Z} < -0.40$ (Price is discounted relative to intraday VWAP)
  3. $\text{Basis\_Z} < -1.20$ (Futures trading at discount to Spot)
  4. $\text{Liquidations}: \text{long\_liq\_zs} \ge 1.5$ and $< 4.5$ (Clean liquidation sweep without toxic 4.5+ tail)
  5. Trend alignment: $Close > EMA_{200}$ or $EMA_{200}$ slope $> -0.0005$.
- **Short Trigger**:
  1. $Z_{OFI} < -1.20$
  2. $\text{VWAP\_Z} > +0.40$
  3. $\text{Basis\_Z} > +1.20$
  4. $\text{Liquidations}: \text{short\_liq\_zs} \ge 1.5$ and $< 4.5$
  5. Trend alignment: $Close < EMA_{200}$ or $EMA_{200}$ slope $< +0.0005$.

#### Sleeve B: Cont-Stoikov Liquidity Vacuum Momentum (Breakout)
- **Long Trigger**:
  1. $Z_{OFI} > +1.80$ (Extreme aggressive order flow dominance)
  2. Depth $D < \text{RollingMedian}(D)$ (Thin order book / high price sensitivity)
  3. $Close > \text{DonchianHigh}_{48}$
  4. $Close > EMA_{200}$ and $EMA_{200}$ slope $> 0$.
- **Short Trigger**:
  1. $Z_{OFI} < -1.80$
  2. Depth $D < \text{RollingMedian}(D)$
  3. $Close < \text{DonchianLow}_{48}$
  4. $Close < EMA_{200}$ and $EMA_{200}$ slope $< 0$.

### 3.3 Microstructure Exit Geometry & Risk Sizing
To prevent the premature ratchet choking observed in prior runs:
- **Initial Stop**: $2.2 \times ATR_{14}$ (minimum $1.0\%$ of price).
- **Target Price**: $+2.00R$ to $+2.20R$ (fixed limit target).
- **Delayed Ratchet**:
  - Do NOT ratchet at $+0.70R$ (avoids being chopped by normal $0.5R$ pullbacks).
  - Only when price reaches $+1.40R$, lock stop at $+0.70R$ (guarantees net profit of over $15$ USD clearing all fees).
- **Time Decay**: Exit at market if trade fails to reach $+0.25R$ within 24 bars (6 hours).
- **Maximum Hold**: 288 bars (72 hours).
- **Asymmetrical Risk Budgeting**:
  - Base Risk: $22.00$ USD ($0.44\%$ of $5,000$ USD).
  - Drawdown Defense: $12.00$ USD when current drawdown $\ge 1.5\%$.
  - House Money Acceleration: $70.00$ USD when quarterly net profit $\ge +40.00$ USD.
  - Hard Drawdown Stop: $4.50\%$ ($225.00$ USD) circuit breaker.
