# OPUS 5 MASTER DIRECTIVE: AUTONOMOUS BUILD & VERIFICATION OF CONVEX TREND-FOLLOWING ENGINE ACROSS ALL 20 OOS WINDOWS

Opus, you have proven that your embedded Python sandbox can autonomously execute, instrument, and verify trading engines. 
Now, we are giving you full architectural command to design, forward test, and iterate on an **Adaptive Convex Trend-Following Engine with Causal ML** until all 20 OOS windows satisfy `target_oos_criteria.json`.

---

## 1. Mandatory Protocol: Load Rules & Skills First

Before generating the architecture, you must query and ingest via GitHub MCP (`kbsingh1399/Engine` or `kbsingh1399/Trading`):
1. **Master Enforcement Rules**: `.agents/rules/AGENTS.md` (and `.agents/AGENTS.md`). Ingest all 12 core domains, including the 20 OOS Windows Protocol (§10), Institutional Anti-Lookahead Blacklist (§14), and Karpathy Directives (§6).
2. **Target Criteria & Windows**:
   - `Engine/target_oos_criteria.json`:
     - **Min ROI per 1-Month Window**: `> +20.0%`
     - **Max Drawdown**: `< 5.0%` (Hard circuit-breaker stop at `4.5%` / `$225` on `$5,000` capital)
     - **Min Win Rate**: `> 40.0%`
     - **Take-Profit Target**: `>= 4.0R` (Upper barrier $\ge 4.0	ext{R}$, extending to $8.0	ext{R}$ in strong momentum)
     - **Min Trades per Window**: `>= 15 trades`
     - **Frictions**: Strict 33 bps round-trip (8 bps taker fee in/out, 10 bps entry slippage, 15 bps stop slippage).
   - `Engine/oos_windows_20.json`: 20 non-overlapping 1-month windows (W01 May-2021 to W20 Mar-2026).
3. **Core Institutional Skills (in `skills/`)**:
   - `skills/training-machine-learning-models.md`
   - `skills/engineering-features-for-machine-learning.md`
   - `skills/backtesting-trading-strategies.md`
   - `skills/trader-risk.md`
   - `skills/karpathy-guidelines.md`

---

## 2. Empirical Ground Truth from Round 9 Real-Data Execution

We ran your Round 9 engine (`rp2_round9_ml_convex_engine.py`) on our real 18-asset Binance master parquets for Window 1 (May 2021 Liquidation Crash). Here is what the real trade ledger revealed:
- **Trained GBDT & Invariants**: Worked flawlessly! Pure NumPy GBDT fit on 7,750 pre-purge events with out-of-sample validation AUC = **0.6282**.
- **Trades & Win Rate**: 30 trades (passed $\ge 15$ floor), 43.33% Win Rate (passed $> 40\%$ floor).
- **Capital Defense**: Max Drawdown was rock-solid at **3.84%** during a 50% market crash.
- **The Exact Failure Vector**:
  - `target` (+4.0R) exits = **0 trades**.
  - 7 trades achieved explosive MFE between $+1.5	ext{R}$ and $+3.07	ext{R}$ (DOT reached $+3.07	ext{R}$, DOGE $+2.56	ext{R}$, ETH $+1.88	ext{R}$, LTC $+1.72	ext{R}$, ADA $+1.72	ext{R}$).
  - BUT all 7 were prematurely knocked out on minor 15-minute pullbacks by the tight ratchet stop (locking at $+0.8	ext{R}$), exiting at $+0.60	ext{R}$ to $+0.70	ext{R}$!
  - Result: Average win was only $+0.60	ext{R}$ while average loss was $-0.80	ext{R}$, capping ROI at $-2.32\%$.
- **Takeaway**: Crypto trends have massive volatility. A ratchet that trails too tightly suffocates winning runs. Winning trades MUST be given room to breathe so they can expand into $+4.0	ext{R}$ to $+8.0	ext{R}$ home runs!

---

## 3. Architecture: Adaptive Convex Trend-Following Engine

Mean-reversion and flush-reclaim setups are inherently range-bound. In contrast, **crypto perpetuals are defined by massive directional momentum regimes** (W01 May-21 crash, W03 Nov-21 top, W05 Luna, W06 3AC, W09 Jan-23 rally, W11/W13/W15/W17 bull breakouts). A trend-following strategy naturally captures the 4R–10R right-tail skew required for $+20\%$ monthly ROI.

### A. Multi-Horizon Trend Identification
- **Donchian Breakout Channels**: 20-bar and 55-bar rolling highs/lows on 15m candles.
- **Moving Average Ribbon**: $EMA_{20} > EMA_{50} > EMA_{200}$ for confirmed bull momentum (reversed for bear momentum).
- **ADX & Volatility Expansion Filter**: Only trade when $	ext{ADX}_{14} \ge 22$ and $	ext{ATR}_{14} / 	ext{rolling\_mean}(	ext{ATR}, 96) \ge 1.0$. In low-volatility chop ($	ext{ADX} < 20$), stay flat or trade ultra-tight stops.
- **Volume & Open Interest Surge**: Directional volume $Z \ge 1.5$ and positive Open Interest expansion ($\Delta	ext{OI}_{1	ext{h}} > 0$) confirming aggressive trend initiation.

### B. Causal ML Classifier Overlay (Event-Conditioned)
- Condition candidate trend entries on Donchian breakout or EMA pullback signals.
- Train the shallow GBDT / Ridge ensemble (`max_depth <= 4`, `reg_lambda >= 3.0`) strictly on in-sample data prior to $t_{	ext{start}} - 72	ext{h}$.
- Target Label: Does the breakout hit **$+4.0	ext{R}$** before $-1.0	ext{R}$ or 36-bar (9h) expiry?
- Gate entries using the validation score quantile grid (`p*`).

### C. Convex Payoff Geometry & Wide-Breathing Ratchets
- **Initial Stop**: Set at swing extreme or $1.0 	imes 	ext{ATR}_{14}$.
- **Target**: Base $+4.0	ext{R}$, extending to $+8.0	ext{R}$ during extreme volume/OI momentum breakouts.
- **Anti-Suffocation Ratchet Schedule**:
  - Gain $\ge +1.0	ext{R} 	o$ Move stop to Breakeven $+0.10	ext{R}$.
  - Gain $\ge +2.0	ext{R} 	o$ Move stop to Entry $+1.00	ext{R}$.
  - Gain $\ge +3.2	ext{R} 	o$ Move stop to Entry $+2.20	ext{R}$.
  - Chandelier Trailing Stop: Once past $+3.5	ext{R}$, trail stop at $2.2 	imes 	ext{ATR}_{14}$ from the running high, allowing 5R–8R mega-runners to mature!
- **Time Decay**: Allow 36 bars (9 hours) before checking time decay ($< +0.10	ext{R}$), giving multi-hour trend waves adequate time to develop.

### D. Pyramiding & Dynamic House-Money Sizing
- Base Risk: `$25.00` (0.50% of `$5,000`).
- House-Money Scaling: $	ext{Risk} = \$25 + 0.40 	imes \max(0, 	ext{Banked Realised Profit})$, capped at `$200`.
- Convex Pyramiding: When a trade reaches $+1.5	ext{R}$ and stop is locked at BE, allow a single $0.50	imes$ pyramid add on trend continuation.
- Capital Protection Floor: Zero trade risk if $	ext{Equity} - 	ext{Open Risk} \le \$4,775$ (4.5% drawdown limit).

---

## 4. Your Autonomous Execution Mandate

Run an autonomous development, simulation, and calibration loop inside your sandbox:
1. **Simulate**: Test the trend-following engine across all 20 windows using your synthetic panel harness.
2. **Diagnose & Calibrate**: Check where individual windows fall short of `target_oos_criteria.json` (e.g. low-vol windows like W07/W18 needing tighter chop filters, vs explosive windows like W01/W05 needing wider trailing stops).
3. **Verify All Invariants**: Zero lookahead, 72h causal purge, gap-multiplier budget ($4.5\%$ hard ceiling), no RNG.
4. **Deliver**:
   - Output the complete, drop-in, single-file script `rp2_round10_convex_trend_following_ml.py` (with class `ConvexTrendML` aliased to `MLConvexEngine`).
   - Output the consolidated 20-window scorecard table.

Opus, the rules are loaded and the parameters are clear. Build the trend-following engine, run your autonomous verification loop, and deliver Round 10!
