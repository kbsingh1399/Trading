# OPUS 5 AUTONOMOUS 20-WINDOW KQL CONQUEST DIRECTIVE

## 1. Architectural Decision: Option A Approved
You are authorized to proceed with **Option A**:
- Deploy the verified diagonal footprint imbalance reconstruction (`ask_vol[i] / bid_vol[i-1] >= 3.0` with run length >= 3) uniformly across all 18 symbols in `Trading / binance_footprint_ladder_15m`.
- Ensure homogeneous gating across all 18 institutional contracts (BTC, ETH, SOL, AVAX, NEAR, OP, SUI, ARB, APT, ADA, DOGE, DOT, LINK, LTC, BCH, TRX, XRP, BNB).
- Report `flag_source: reconstructed` in the candidate trade ledger metadata for full audit transparency.

---

## 2. Settled Target Pass Criteria (Per Window)
Across each of the 20 Out-Of-Sample (OOS) 1-month windows (2021 to 2026), your strategy must simultaneously achieve:
1. **Minimum ROI**: > +10.0% (+500.00 USD net on 5,000.00 USD initial capital).
2. **Maximum Drawdown**: < 4.50% (hard stop at 225.00 USD; immediate window termination if breached).
3. **Minimum Win Rate**: > 40.0%.
4. **Minimum Trades**: >= 15 completed trades per window across the universe.

---

## 3. Portfolio Risk & Execution Invariants
- **Universe**: 18 Institutional Binance USDT-M Perpetual contracts from `Trading / binance_master_15m` and `Trading / binance_footprint_ladder_15m`.
- **Max Concurrency**: Maximum 2 open positions across all 18 symbols simultaneously.
- **Round-Trip Frictions**: Full 41 bps notional deducted on every trade (8 bps entry fee, 8 bps exit fee, 10 bps entry slippage, 15 bps stop slippage).
- **Position Sizing Engine**:
  - Initial Capital: 5,000.00 USD.
  - Base Risk: 90.00 to 95.00 USD (1.80% to 1.90% per trade).
  - House Money Risk: 160.00 to 170.00 USD (activated when window accumulated net profit > 50.00 USD).
  - Drawdown Defense Risk: 20.00 USD (activated when mark-to-market drawdown exceeds 2.00%).
  - Hard Drawdown Stop: 4.50% (225.00 USD).
- **Microstructure Exit Ratchet**:
  - Target: +2.50R resting limit exit.
  - Breakeven Lock: When favorable price excursion reaches >= +0.80R, move stop to entry +0.20R.
  - Profit Lock: When favorable price excursion reaches >= +1.50R, move stop to entry +0.85R.
  - Time Decay: Exit at market if price fails to reach +0.20R within 24 bars (6 hours).
  - Causal Execution: Stops and ratchets arm at bar close and take effect strictly on subsequent bars (j+1).

---

## 4. The 20 Canonical OOS Windows (2021-2026)
- Window 01: 2021-05-01 to 2021-05-31 (May Liquidation Crash)
- Window 02: 2021-09-01 to 2021-09-30 (Autumn Expansion)
- Window 03: 2021-11-01 to 2021-11-30 (ATH Distribution)
- Window 04: 2022-01-01 to 2022-01-31 (Range Breakdown)
- Window 05: 2022-05-01 to 2022-05-31 (Terra/LUNA Crash)
- Window 06: 2022-06-01 to 2022-06-30 (3AC Liquidation Floor)
- Window 07: 2022-09-01 to 2022-09-30 (Pre-FTX Dead Chop)
- Window 08: 2022-11-01 to 2022-11-30 (FTX Capitulation)
- Window 09: 2023-01-01 to 2023-01-31 (Jan Relief Rally)
- Window 10: 2023-03-01 to 2023-03-31 (USDC Depeg / Bank Run)
- Window 11: 2023-06-01 to 2023-06-30 (SEC Lawsuits)
- Window 12: 2023-08-01 to 2023-08-31 (Aug Flush)
- Window 13: 2023-10-01 to 2023-10-31 (Uptrend Breakout)
- Window 14: 2024-01-01 to 2024-01-31 (ETF Sell-the-News)
- Window 15: 2024-03-01 to 2024-03-31 (Pre-Halving ATH)
- Window 16: 2024-08-01 to 2024-08-31 (Yen Carry Unwind)
- Window 17: 2024-11-01 to 2024-11-30 (Post-Election Surge)
- Window 18: 2025-02-01 to 2025-02-28 (Macro Trend Expansion)
- Window 19: 2025-07-01 to 2025-07-31 (Summer Chop)
- Window 20: 2026-03-01 to 2026-03-31 (Late Cycle Expansion)

---

## 5. Autonomous Loop Directive
1. **Server-Side KQL Generation**:
   Run the KQL scan state machine with `partition by symbol` on `Trading / binance_master_15m` and `Trading / binance_footprint_ladder_15m` to generate candidate entry/exit events.
2. **Local Portfolio Risk Arbitration**:
   Simulate portfolio equity, max 2 concurrent positions, dynamic house money risk, and ratchet execution.
3. **Sequential Non-Halting Walk-Forward**:
   Execute Window 1, Window 2, and sequentially advance through all 20 windows.
   - If a window fails any of the 4 criteria, report exact failure analytics (e.g. churn vs knife-catching) and re-calibrate causally before progressing.
   - Do NOT stop until all 20 windows achieve verified passes.
4. **Communication Formatting**:
   - Strictly plain-text tables and scorecards.
   - NEVER print dollar signs ($) or raw LaTeX math blocks. Use "USD" or spell out currency.
