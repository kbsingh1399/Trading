# OPUS 5 MASTER DIRECTIVE: AUTONOMOUS TREND-FOLLOWING ENGINE ON ORDERFLOW & FOOTPRINT STEROIDS

Opus, all target criteria, master enforcement rules, baseline engines, institutional skills, and footprint confirmation modules are committed and pushed to our public GitHub repositories on branch `main`.

We have **Institutional Orderflow and Footprint Ladder Data** across all 18 assets (3.47M 15m bars, 2020–2026). You are instructed to put the Adaptive Convex Trend-Following Engine **ON STEROIDS** using real microstructural orderflow and footprint confirmation.

Use your GitHub MCP server or direct HTTP raw pulls to fetch the required files from the exact links below.

---

## 1. Git Repository Access & Core Files to Pull (Raw GitHub URLs)

### Repositories (Branch: `main`)
- **Primary Trading Repository**: `https://github.com/kbsingh1399/Trading`
- **Quantitative Engine & Skills Catalog**: `https://github.com/kbsingh1399/Engine`

### Canonical Direct URLs
1. **Master Enforcement Rules (`AGENTS.md`)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/.agents/rules/AGENTS.md`
   *(20 OOS Windows Protocol, Anti-Lookahead Blacklist, Karpathy Directives)*

2. **Target Acceptance Criteria (`target_oos_criteria.json`)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/target_oos_criteria.json`
   *(Target: ROI >= 20.0%, MaxDD < 5.0%, Win Rate >= 40.0%, Target R >= 4.0R, Min Trades >= 15 per window)*

3. **20 OOS Windows Specification (`oos_windows_20.json`)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/oos_windows_20.json`

4. **Footprint & Orderflow Confirmation Module**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/ml/footprint_confirmation.py`
   *(Production implementation of stacked imbalances, POC migration, and wick absorption)*

5. **Round 9 Baseline Engine (`rp2_round9_ml_convex_engine.py`)**:
   `https://raw.githubusercontent.com/kbsingh1399/Trading/main/Engine/strategy/rp2_round9_ml_convex_engine.py`

6. **Key Skills (from `https://github.com/kbsingh1399/Engine/tree/main/skills/`)**:
   - `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/training-machine-learning-models.md`
   - `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/engineering-features-for-machine-learning.md`
   - `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/backtesting-trading-strategies.md`
   - `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/trader-risk.md`
   - `https://raw.githubusercontent.com/kbsingh1399/Engine/main/skills/karpathy-guidelines.md`

---

## 2. Orderflow & Footprint Data Schema Available in the Master Parquets

Our production datasets contain high-resolution institutional orderflow features:

### A. Delta & CVD Dynamics
- `future_cvd_15m` & `spot_cvd_15m`: 15-minute Cumulative Volume Delta.
- `zc_div`: Institutional Z-Score CVD Divergence (Spot buying while futures selling, or vice-versa).
- `taker_volume_ratio`: Taker Buy Volume / Taker Sell Volume.
- `taker_buy_vol_btc` & `taker_sell_vol_btc`: Aggressive market volume lifting the book.

### B. Footprint Ladder Microstructure (from `footprint_confirmation.py`)
- `is_stacked_buy_imb`: 3+ consecutive price levels of aggressive buying imbalance (>= 300% ratio).
- `is_stacked_sell_imb`: 3+ consecutive price levels of aggressive selling imbalance.
- `poc_shift`: Point of Control value migration upwards (bullish trend) or downwards (bearish trend).
- `absorption_ratio`: Aggressive volume absorbed at wick extremes without price progress.

### C. Institutional Positioning & Cascades
- `long_liq_zs` & `short_liq_zs`: Z-scores of real forced liquidations.
- `top_account_ratio` & `ls_ratio_top`: Smart money / top trader positioning skew.
- `whale_index`: Institutional large-order trade concentration.
- `open_interest_usd` & `oi_change_pct`: True dollar Open Interest expansion.

---

## 3. Putting the Trend-Following Engine on Steroids (Round 10)

Mean-reversion setups are capped by nature. In crypto perpetuals, **macro regimes produce massive 10R to 25R multi-day directional waves**. Combining trend following with orderflow and footprint confirmation creates an unfair institutional edge:

1. **Breakout Ignition via Stacked Imbalances**:
   - A price breakout of the 20/55-bar Donchian channel or EMA ribbon ($EMA_{20} > EMA_{50} > EMA_{200}$) is ONLY taken if confirmed by orderflow aggression:
     $$	ext{is\_stacked\_buy\_imb} == 	ext{True} \quad \lor \quad (	ext{taker\_volume\_ratio} \ge 1.25 \;\land\; 	ext{future\_cvd\_15m} > 0)$$
   - This single filter eliminates up to 80% of low-volume chop traps and false breakouts!

2. **CVD Acceleration & Divergence Confirmation**:
   - Long breakouts must show expanding CVD ($Z_{	ext{cvd}} \ge 1.2$).
   - Avoid trades where price makes a new high but spot CVD shows aggressive distribution (`zc_div < -0.8`), filtering out institutional distribution traps.

3. **Liquidation Squeeze Rocket Fuel**:
   - When a long trend breakout coincides with elevated short liquidations (`short_liq_zs \ge 1.5`), aggressive forced buy-ins trigger a convexity rocket. These setups are tagged for extended targets (**$+6.0	ext{R}$ to $+8.0	ext{R}$**).

4. **Anti-Suffocation Ratchets (The Critical Lesson from Round 9)**:
   - In our Round 9 real-data run, 7 trades reached MFE $+1.5	ext{R}$ to $+3.07	ext{R}$, but were stopped out at $+0.60	ext{R}$ because the trailing stop locked too close.
   - **Wide-Breathing Ratchet Schedule**:
     - Gain $\ge +1.0	ext{R} 	o$ Move stop to Breakeven $+0.10	ext{R}$.
     - Gain $\ge +2.0	ext{R} 	o$ Move stop to Entry $+1.00	ext{R}$.
     - Gain $\ge +3.2	ext{R} 	o$ Move stop to Entry $+2.20	ext{R}$.
     - Chandelier Trailing Stop: Once past $+3.5	ext{R}$, trail at $2.2 	imes 	ext{ATR}_{14}$ from running highs, allowing 5R–8R mega-runners to mature!

5. **Pyramiding & House Money**:
   - Add $0.50	imes$ pyramid leg once stop is locked at BE; scale risk with banked profit ($25 + 0.40 	imes 	ext{banked}$, cap $200); protect $\$4,775$ hard floor (4.5% MaxDD limit).

---

## 4. Autonomous Simulation Loop in Sandbox

Execute your autonomous simulation and calibration loop inside your sandbox:
1. Pull all files from the GitHub URLs above.
2. Ingest the footprint logic from `Engine/ml/footprint_confirmation.py`.
3. Simulate across the 20 windows in `Engine/oos_windows_20.json`.
4. Verify all 24 invariants (zero lookahead, 72h purge, 4.5% kill-switch, determinism).
5. Deliver:
   - Complete drop-in script `rp2_round10_convex_trend_following_ml.py`.
   - Consolidated 20-window scorecard table.

Opus, pull the files from GitHub and build the orderflow-powered trend engine!
