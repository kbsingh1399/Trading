# OPUS 5 MASTER DIRECTIVE: AUTONOMOUS TREND-FOLLOWING ENGINE VIA GITHUB MCP

Opus, all target criteria, master enforcement rules, baseline engines, and institutional skills are committed and pushed to our public GitHub repositories on branch `main`. 

Use your GitHub MCP server or direct HTTP raw pulls to fetch every required file from the exact links below. Do not assume or hallucinate; pull the live files directly.

---

## 1. Git Repository Access & Pull Information

### Repositories (Branch: `main`)
- **Primary Trading Repository**: `https://github.com/kbsingh1399/Trading`
- **Quantitative Engine & Skills Catalog**: `https://github.com/kbsingh1399/Engine`

### Core Canonical Files to Pull (Raw GitHub URLs)
1. **Master Agent Enforcement Rules & Protocols**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/.agents/rules/AGENTS.md`
   *(Contains the 20 OOS Windows Protocol, Anti-Lookahead Blacklist, Karpathy Directives, and Execution Gates)*

2. **Target Acceptance Criteria**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/target_oos_criteria.json`
   *(Target: ROI >= 20.0%, MaxDD < 5.0%, Win Rate >= 40.0%, Target R >= 4.0R, Min Trades >= 15 per window)*

3. **20 Out-Of-Sample (OOS) Windows Specification**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/oos_windows_20.json`
   *(W01 May-2021 through W20 Mar-2026)*

4. **Working Round 9 Engine Baseline**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/rp2_round9_ml_convex_engine.py`
   *(Your verified pure-NumPy Histogram GBDT + Ridge Logistic engine)*

### Institutional Skills to Pull (From `https://github.com/kbsingh1399/Engine/tree/main/skills/`)
- **ML Model Training**: `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/training-machine-learning-models.md`
- **Feature Engineering**: `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/engineering-features-for-machine-learning.md`
- **Backtesting Invariants**: `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/backtesting-trading-strategies.md`
- **Risk & Sizing**: `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/trader-risk.md`
- **Karpathy Directives**: `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/karpathy-guidelines.md`

---

## 2. Empirical Ground Truth from Round 9 Real-Data Execution

We executed your `rp2_round9_ml_convex_engine.py` on our real 18-asset Binance master parquets for **Window 1 (May 2021 Liquidation Crash)**.
- **What Worked**:
  - GBDT trained causally on 7,750 pre-purge events with validation AUC = `0.6282`.
  - Max Drawdown was rock-solid at `3.84%` during Bitcoin's 50% crash (gap budget and tail-notional caps held).
  - Generated 30 trades at a 43.33% win rate.
- **The Bottleneck**:
  - Zero trades reached the +4.0R target because the trailing ratchet stop locked too tightly (+0.8R lock at +1.5R gain).
  - 7 explosive trades that reached MFE between +1.5R and +3.07R (DOT +3.07R, DOGE +2.56R, ETH +1.88R, LTC +1.72R) were stopped out on minor pullbacks at +0.60R to +0.70R.
  - Wins averaged only +0.60R against -0.80R losses, yielding -2.32% ROI.
- **Conclusion**: Crypto trends have wide intraday swings. Tight trailing stops suffocate the right tail. Runners must be given breathing room to mature into +4.0R to +8.0R payoffs!

---

## 3. Mission Directive: Build Adaptive Convex Trend-Following Engine (Round 10)

Design, simulate, and deliver an **Adaptive Convex Trend-Following Engine with Causal ML** (`rp2_round10_convex_trend_following_ml.py`):

1. **Multi-Horizon Trend Identification**:
   - Donchian channel breakouts (20-bar & 55-bar) aligned with EMA ribbons ($EMA_{20} > EMA_{50} > EMA_{200}$).
   - Chop filter: $	ext{ADX}_{14} \ge 22$ and expanding ATR ($	ext{ATR}_{14} / 	ext{rolling\_mean}(	ext{ATR}, 96) \ge 1.0$). Stay flat in low-volatility compression.
   - Volume and Open Interest expansion ($Z_{	ext{vol}} \ge 1.5, \Delta	ext{OI}_{1	ext{h}} > 0$).
2. **Causal GBDT Overlay**:
   - Condition samples on trend breakouts; train on pre-purge events ($t \le t_{	ext{start}} - 72	ext{h}$) to predict probability of hitting **+4.0R** before -1.0R.
3. **Anti-Suffocation Ratchet Geometry**:
   - Stop at swing extreme ($1.0 	imes 	ext{ATR}_{14}$). Target: $+4.0	ext{R}$ (extending to $+8.0	ext{R}$ on volume surges).
   - Progressive ratchet: Breakeven lock at $+1.0	ext{R}$, profit lock at $+2.0	ext{R}$ ($	o +1.0	ext{R}$), $+3.2	ext{R}$ ($	o +2.2	ext{R}$), followed by a loose $2.2 	imes 	ext{ATR}_{14}$ chandelier trailing stop.
4. **Pyramiding & House Money**:
   - Add $0.50	imes$ pyramid once stop is locked at BE; scale risk with banked profit ($25 + 0.40 	imes 	ext{banked}$, cap $200); protect $\$4,775$ hard floor.

---

## 4. Autonomous Simulation Loop in Sandbox

Execute your autonomous simulation and calibration loop inside your sandbox:
1. Pull the files from the GitHub URLs above.
2. Simulate across the 20 windows in `Engine/oos_windows_20.json`.
3. Verify all 24 invariants (zero lookahead, 72h purge, 4.5% kill-switch, determinism).
4. Output the drop-in Python file `rp2_round10_convex_trend_following_ml.py` and the 20-window scorecard.

Opus, pull the files from GitHub and conquer the 20 windows!
