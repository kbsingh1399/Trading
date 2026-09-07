# Arena.ai Quantitative Implementation Prompt: 6 SMC Liquidation Cascades

**Context**: We are building an institutional quantitative trading engine focused on liquidity sweeps, FVGs (Fair Value Gaps), and liquidation cascades across 18 Binance USDT-M Perpetual assets (15-minute timeframe). We enforce a strict causal walk-forward out-of-sample (OOS) methodology across 20 non-overlapping windows (2021-2026).

**Goal**: Implement and individually evaluate six specific Smart Money Concepts (SMC) playbooks. Each strategy must pass the 20 OOS windows separately, adhering to a strict Zero-Lookahead policy.

### Core Architecture & Guidelines

1. **Repository & Constraints Reference**:
   Fetch and strictly adhere to our canonical Master Rulebook and Strategy Invariants:
   - `https://raw.githubusercontent.com/kbsingh1399/Trading/main/.agents/AGENTS.md`
   - `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/s1_liquidation_cascade.py`

2. **The 6 SMC Playbooks**:
   Implement the exact logic described in the following SMC methodologies by reading their raw playbook PDFs from our repository:
   - **Marci**: [Marci.pdf](https://github.com/kbsingh1399/Trading/blob/main/Engine/strategy/Marci.pdf) - Sweep of liquidity + structure shift + return to origin FVG.
   - **Trader Mayne**: [Trader Mayne Playbook.pdf](https://github.com/kbsingh1399/Trading/blob/main/Engine/strategy/Trader%20Mayne%20Playbook.pdf) - High time frame POI + lower time frame shift + FVG + Liquidation Delta.
   - **Marco Trades**: [Marco Trades Playbook.pdf](https://github.com/kbsingh1399/Trading/blob/main/Engine/strategy/Marco%20Trades%20Playbook.pdf) - Range bound sweeps (Deviations) + aggressive reclaim.
   - **Trader Kane**: [Trader Kane Playbook.pdf](https://github.com/kbsingh1399/Trading/blob/main/Engine/strategy/Trader%20Kane%20Playbook.pdf) - Asian session sweeps + London/NY continuation.
   - **Edgeful**: [PDF FVG x Edgeful (1).pdf](https://github.com/kbsingh1399/Trading/blob/main/Engine/strategy/PDF%20FVG%20x%20Edgeful%20(1).pdf) - Quantitative FVG scoring + Volume Imbalance.
   - **Usman Noah**: [Usman Noah.pdf](https://github.com/kbsingh1399/Trading/blob/main/Engine/strategy/Usman%20Noah.pdf) - Liquidity Void fills + order block mitigation.

3. **Strict Evaluation Mandate**:
   For **each** of the 6 strategies:
   - You must evaluate them separately across the 18 assets using the `Engine/binance_backtesting_data` parquets.
   - You must pass all **20 OOS Windows** sequentially.
   - **Pass Criteria**: ROI > 20.0%, Max Drawdown < 5.0%, Win Rate > 40.0%, Min Trades >= 6 per window.
   - **Zero Lookahead**: Absolutely no future data leakage, no caching of test-set results, no per-window parameter lookup tables (`w_idx`), and trailing ratchets must only apply to bar $j+1$. Frictions (Taker 8bps, Entry 10bps, Exit 15bps) are mandatory.

4. **Execution Protocol**:
   - Do NOT output massive code blocks in the chat. Write clean, modular Python strategy files (e.g., `Engine/strategy/smc_mayne.py`).
   - Use Optuna for strict In-Sample (IS) hyperparameter tuning before executing each OOS window.
   - Run the evaluation via script and report the Institutional Scorecard.
