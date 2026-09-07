# Arena.ai Quant Strategy Optimization Prompt

**Objective:** Refine the `s1_liquidation_cascade.py` strategy to pass all 20 Out-Of-Sample (OOS) Walk-Forward Windows (2021-2026) under ONE strict causal configuration.

## System Invariants & Target Constraints
- **Target Pass Criteria (per window):** ROI > 20.0%, Max Drawdown < 5.0%, Win Rate > 40.0%, Min Trades >= 6.
- **Risk Budget:** Initial Capital $5,000 | 0.50% base risk ($25) | 1.00% max house money risk | 4.5% ($225) hard DD stop.
- **Microstructure Ratchet:**
  - `arm0_r = 0.8`, `lock0_r = 0.15` (Breakeven Lock)
  - `arm1_r = 1.5`, `lock1_r = 0.8` (Profit Lock)
  - `min_target_r = 2.5` (Max target exit)
  - Time Decay: market exit if `< +0.2R` within 24 bars.
- **Strict Anti-Lookahead:** Zero parameter snooping on `w_idx`, no future MAE sizing, full frictions applied (8bps fee, 10bps entry slippage, 15bps stop slippage). 
- **Current State:** The current raw baseline signal (threshold 0.0) produces trades but breaks the 5.0% MaxDD limit (currently ~5.14%) and has a poor win rate due to excessive stop-outs.

## Action Required
1. **Analyze Playbooks:** Read the following newly integrated institutional SMC and Liquidation playbook PDFs:
   - [Trader Mayne Playbook](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/Trader%20Mayne%20Playbook.pdf)
   - [Marco Trades Playbook](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/Marco%20Trades%20Playbook.pdf)
   - [Trader Kane Playbook](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/Trader%20Kane%20Playbook.pdf)
   - [PDF FVG x Edgeful](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/PDF%20FVG%20x%20Edgeful%20(1).pdf)
   - [Usman Noah](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/Usman%20Noah.pdf)
   - [Marci](https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/Marci.pdf)
2. **Review Codebase:** Fetch the current quantitative architecture directly from git:
   - `s1_liquidation_cascade.py`: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/s1_liquidation_cascade.py
   - `test_20_oos_s1.py`: https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/test_20_oos_s1.py
   - `AGENTS.md` (Constraints): https://raw.githubusercontent.com/kbsingh1399/Trading/main/.agents/rules/AGENTS.md
3. **Refine Signal Confluence:** Incorporate insights from the playbooks to tighten the base entry signal conditions (`long_liq_zs`, `zc_div`, `delta_spot`, `delta_fut`, `rsi_14`, `vwap_zscore`). We need a stronger volatility filter or time-based structural filter to stop the bleeding and boost the win rate.
4. **Deliver minimal exact file edits** for `s1_liquidation_cascade.py` that drop the MaxDD below 5.0% while keeping ROI above 20% on the baseline configuration. Do not break the institutional architecture or introduce lookahead variables.
