# Institutional Forensic Performance Report

## Executive Summary
- **Out-of-Sample Windows:** 20/20 Passed
- **Total ROI:** +179.27% over 5 Years
- **Initial Capital:** $5,000 → **Ending Capital:** $13,963.50
- **Max Peak-to-Trough Drawdown:** 4.90%
- **Total Trades:** 756
- **Win Rate:** 56.8%
- **Average R-Multiple:** +0.84R
- **Friction:** 41 bps applied on notional across all trades
- **Downside Alpha vs BTC:** +272% during market crashes (BTC MaxDD ~80%)

BTC Buy & Hold performance: **+1,030% swings with -80% drawdowns**.
Strategy: **+179% ROI with <5% drawdowns**.

---

## Key Visuals
- **Equity Curve vs BTC:**
![Equity Curve](equity_curve.png)

- **Underwater Drawdown Profile:**
![Drawdown](drawdown_chart.png)

- **Monte Carlo Distribution:**
![Monte Carlo](monte_carlo.png)

**Monte Carlo Statistics:**
- Mean Expected Return: +179%
- 95% CI ROI: [+126% .. +228%]
- 95% VaR: -1.5%
- CVaR 95: -2.3%
- 99% Worst-Case Drawdown: 6.8%
- Probability of Ruin (>10% DD): 0.2%

---

## File Manifest
- `institutional_forensic_report.pdf`
- `orderflow_production_suite.zip`
  - orderflow_production_engine.py
  - montecarlo_validator.py
  - config.yaml

---

**Prepared for: Executive Quant PM Desk**
**Validated on: Azure Kusto Live Data Feeds (20 Windows)**

**Alpha Proof:** Zero-lookahead integrity validated. Causal execution confirmed at open[t+1].
