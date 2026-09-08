# OPUS 5 — QUANTITATIVE STRATEGY MISSION: CONQUER ALL 20 OOS REGIMES

Opus, I saw your GitHub MCP thoughts. Do **NOT** attempt to pull dozens of files or any backtest data (`.parquet` files are gigabytes and will blow your context budget). All backtesting and execution happen on my local quantitative engine with 3.47M 15m candles.

You have access to:
- **Primary Repo**: `https://github.com/kbsingh1399/Trading`
- **Clean Engine & Skills Repo**: `https://github.com/kbsingh1399/Engine` (contains unpacked `.md` skills in `skills/` and core code in `Engine/`)

---

### Step 1: Specific Files to Pull via GitHub MCP (Only Pull These 4 Files)
Use your `get_file_contents` tool to pull ONLY these 4 critical files:
1. `Engine/target_oos_criteria.json` — The non-negotiable target criteria.
2. `Engine/oos_windows_20.json` — The 20 canonical Out-Of-Sample (OOS) regime windows (2021–2026).
3. `Engine/strategy/rp2_round7_residual_dislocation.py` — The clean Round 7 engine (with your 8 harness bug fixes, causal Wilder daily ATR, event-time funding, and intrabar kill-switch).
4. `Engine/strategy/s1_liquidation_cascade_v2.py` — The legacy liquidation cascade baseline.

*(Optional: If you need specialized engineering/quant skill specs, you can pull individual files like `skills/quant-analyst.md` or `skills/karpathy-guidelines.md` from `kbsingh1399/Engine`).*

---

### Step 2: The Non-Negotiable Quantitative Target
Every single window in `oos_windows_20.json` must be evaluated under the strict institutional constraints:
- **ROI per 1-Month Window**: `> +20.0%`
- **Max Drawdown**: `< 5.0%` (Hard circuit-breaker kill-switch at `4.5%` / `$225`)
- **Win Rate**: `> 40.0%`
- **Min Trade Count**: `>= 6 trades` per window
- **Target Profit / R-Multiple**: `>= 2.5R` (with microstructure exit ratchets)
- **Portfolio Risk Budget**: Starting capital `$5,000`, Base risk `$25` (`0.50%`), House money `$50` (`1.00%`), Max 2 concurrent open positions across all 18 symbols.
- **Institutional Frictions (Mandatory)**: 33 bps round-trip (8 bps taker fee per side, 10 bps entry slippage, 15 bps exit slippage).

---

### Step 3: The 20-Window Fail-Fast Walk-Forward Protocol
We operate under a strictly causal walk-forward protocol:
1. Evaluate windows sequentially: $W_1 \to W_2 \to \dots \to W_{20}$.
2. **Immediate Fail-Fast**: If Window $k$ fails any criterion (`ROI < 20%`, `MaxDD >= 5%`, `WR < 40%`, or `Trades < 6`), **halt immediately on Window $k$**.
3. **Causal Re-Optimization**: Re-optimize parameters strictly using in-sample data prior to Window $k$ ($t_{\text{purge}} = t_{\text{start}} - 72\text{h}$).
4. Verify Window $k$ passes AND confirm zero regression on previous windows $W_1 \dots W_{k-1}$.

---

### Step 4: The Strategy Direction (How to Generate 40R Net Without Overfitting)
As you noted in your Round 7 review, standard linear mean-reversion with fixed $25 risk cannot extract 40R net per month under 33 bps frictions. We need you to engineer **structural convexity and asymmetric payoff geometry**:
1. **Forced Liquidation Exhausts**: Exploit open interest collapses (>10–15% drop in 1h) and aggressive long/short flushes to capture asymmetric 5R–10R snapbacks.
2. **Lead-Lag Cross-Asset Microstructure**: Exploit orderflow and volume impulse spillover from BTC/ETH into delayed high-beta alt perps (SOL, DOGE, AVAX, NEAR, SUI).
3. **Non-Linear Kelly / House-Money Pyramiding**: Scale risk aggressively when net profits exceed threshold, letting free-rolled profits generate the 20%+ return while keeping initial principal strictly defended under 4.5% drawdown.
4. **Funding Basis Squeezes**: Exploit annualized funding rate dislocations (>100% or deep negative) where violent squeezes are mathematically guaranteed.

---

### Step 5: Your Action & Immediate Deliverable
1. Pull the 4 files listed in Step 1 using your GitHub MCP tool.
2. Formulate the upgraded strategy architecture (either enhancing `rp2_round7_residual_dislocation.py` or introducing the convex liquidation/lead-lag hybrid).
3. Provide the full, drop-in Python code for the strategy.
4. I will immediately run your code against the full 3.47M bar dataset across the 20 OOS windows and return the empirical scorecard to you for iterative perfection until all 20 windows pass.
