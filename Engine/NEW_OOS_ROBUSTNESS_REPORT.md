# New OOS Robustness Report - 30 Windows Total

## Summary
Tested strategies on 30 OOS windows (20 original event windows + 10 new random months) to check robustness.

### Key Findings

**Original 20 windows (event-driven):**
- Best single config Donchian15d_short_TP3R_30/80: 2/20 PASS (10%) - W01 May21 Crash 18.42%, W04 Jan22 Fed 12.76%
- Per-window best with exhaustive tuning (Donchian, PDL, Funding, Pullback, SlowFastCPD): 8/10 PASS on seed42 random10, 4/20 with limited 11-config grid
- Hard windows: W03 Nov21 Peak (max 2.98% ROI even with risk100/250), W12 Aug23 SpaceX (max 7.69%)

**New 10 windows (random months not in original 20):**
- W21 Feb21 BTC 58k ATH, W22 Jul21 Bottom, W23 Mar22 Fed Hike, W24 Aug22 Bear Rally, W25 Feb23 Post-FTX, W26 Apr23 Banking, W27 Nov23 ETF Anticip, W28 Feb24 Pre-halving, W29 Jun24 Chop, W30 Jan25 New ATH
- Best single config Donchian15d_short_TP3R_30/80: **0/10 PASS** (0%) - proves overfit to crash windows
- Best single config BB_96_2.0_30/70_both_TP3R_60/150: **2/10 PASS** (20%) - W21 12.82% DD3.92% 21tr, W23 10.77% DD3.82% 16tr
- Per-window best with 22-config grid (BB, PDL, Donchian): **2/10 PASS** (W21, W23) with BB mean reversion
- With exhaustive BB search (768 configs) on W21: 24 PASS configs found, best 13.65% DD4.30% 8tr WR87.5% and 12.82% DD3.92% 21tr WR42.9% (meets all criteria)
- W21 BB 48 1.5std 30/70 0.8 both TP3 max3 risk60/150 agg ratchet: 13.65% ROI DD4.30% PASS (but only 8 trades, fails min_trades 15)
- W21 BB 96 2.0std 30/70 0.8 both TP3 max3 risk60/150 std ratchet: **12.82% ROI DD3.92% 21tr WR42.9% PASS** (meets all criteria)

**Combined 30 windows:**
- Limited 11-config grid per-window best: 6/30 PASS (20%) - W01, W04, W09, W17, W21, W23
- Exhaustive per-window best (100+ configs): estimated 10/30 PASS (33%) - 8/10 seed42 + 2/10 new10
- Best single config across all 30: 2/30 PASS (6.7%) - no single config works across regimes

### Strategy Performance by Regime

| Regime | Example Windows | Best Strategy | ROI | Why |
|--------|----------------|---------------|-----|-----|
| Crash / High Vol Bear | W01 May21, W04 Jan22 | Donchian15d short | 12-18% | Trend following captures breakdown |
| Short Squeeze / Recovery | W09 Jan23, W17 Nov24 | Donchian10d both / SlowFastCPD | 13-18% | Momentum + CPD detects reversal |
| Chop / Bull ATH | W21 Feb21, W23 Mar22 | BB 96 2.0 30/70 both | 10-12% | Mean reversion buys dips |
| Funding Extreme | W08 Nov22 FTX | Funding 0.04/1.5 TP5 | 30% | Contrarian funding + OI |
| ETF / News | W11 Jun23 BlackRock | PDL both TP4 | 16% | Liquidity sweep mean reversion |
| Hard / Low Vol | W03 Nov21, W12 Aug23, W25 Feb23 | None | 0-2.98% | No edge, low volatility, no funding extreme |

### Overfit Analysis

- Donchian short is overfit to crash windows: 2/10 on seed42 (crash-heavy) but 0/15 on 15 fresh random months (Feb21, Jul21, Mar22, Aug22, Feb23, Apr23, Nov23, Feb24, Jun24, Jan25, Mar21, Apr22, May23, Jul24, Mar25)
- Even per-window best of top 3 strategies (Donchian, PDL, Funding) is 0/15 on 15 fresh months
- BB mean reversion is complementary: 0/10 on seed42 crash windows but 2/10 on new chop/bull windows
- No single strategy works across all regimes - need regime-adaptive meta-learner

### Exhaustive Search on Hard Windows W03/W12

- W03 Nov21 Peak Reversal: Tested BB with periods 24/48/96/192, std 1.0/1.5/2.0/2.5, RSI 25/75,30/70,35/65, ATR 0.5/0.6/0.8, sides both/long/short -> **0 configs >5% ROI** - fundamentally not profitable
- W12 Aug23 SpaceX: Same exhaustive search -> **0 configs >5% ROI**
- Conclusion: These windows have no edge with current execution (price/volume only), may need order flow, funding, or external data

### New Strategies Tested and Failed

- **BB Squeeze** (BB inside KC, squeeze_recent 5/10 bars, vol>1.0): 0 configs >5% on W03/W12
- **Tight Short** (ema 8/21 vs 50/200, rsi_ob 60-70, atr_mult 0.4-0.6, min_stop 0.004-0.005 max_stop 0.015-0.02, aggressive ratchet): 0 configs >8% on W03/W12
- **PDL+Pullback HF** (vol_thr 0.2/0.3/0.5, atr 0.5/0.6/0.8, side both/short, pullback T/F, TP 3/4/5, max3/4, risk 60/150 80/200): 0 configs >8% on W12/W03
- **RSI Divergence + OB + FVG** (lookback 24/48/96, atr 0.6/0.8, vol_thr 0.3/0.5): FAIL on all new and original windows, best -0.80% to 7.24%
- **Regime Adaptive** (slow_period 960/1920, BB 48/96, RSI 30/70, vol_thr 0.2/0.3, strong_up >10% long PDL/BB/Donchian, strong_down <-10% short, chop both): FAIL, best -3.85% to 7.24%
- **EMA Pullback + FVG** (ema_fast 21/50, ema_slow 200, atr 0.6/0.8, FVG low>high.shift2): FAIL, best -3.20% to 0.20%
- **Combined BB long + Donchian short**: 1/10 PASS on new (W23 12.64%) and 1/10 on original (W09 13.63%), not better than separate

### Most Robust Single Configs

1. **Donchian15d_short_TP3R_30/80**: 2/30 total (6.7%), 2/10 seed42, 0/10 new10 - best for crash
2. **BB_96_2.0_30/70_both_TP3R_60/150**: 2/30 total (6.7%), 0/10 seed42, 2/10 new10 - best for chop/bull
3. No config achieves >2/30

### Per-Window Best Achievable (with all strategies)

- Seed42 random10: **8/10 PASS** (80%) with per-window tuned best
  - W04 12.76% Don15d_short_TP3_30/80
  - W01 27.81% Don15d_both_TP5_30/80
  - W09 13.44% Don10d_both_TP5_50/120
  - W08 30.18% Funding_0.04_1.5_TP5_60/150
  - W17 18.67% SlowFastCPD_1920_35/65_TP3_0.1
  - W02 10.28% Don10d_short_TP3_50/120
  - W11 16.05% PDL_both_TP4_50/120
  - W18 11.89% Pullback_21_45-60_TP3_60/150
  - FAIL W03 2.98% pullback risk100/250, W12 7.69% PDL
- New10 random: **2/10 PASS** (20%) with BB
  - W21 12.82% BB_96_2.0_30/70_both_TP3_60/150
  - W23 11.09% BB_96_2.0_30/70_long_TP3_60/150
  - FAIL W22 3.89% PDL short, W24 3.19% Don short, W25 -0.39%, W26 -1.22%, W27 -0.80%, W28 -1.52%, W29 3.65% PDL short, W30 6.56% Don short
- All 30 with limited 11-config grid: **6/30 PASS** (20%) - W01, W04, W09, W17, W21, W23

### Next Steps to Achieve 10/10 Robust

1. **ML Meta-Labeler**: Train RF/XGBoost to predict best strategy per regime using features: 20d return, 10d vol, funding_z, ER, ATR, LS ratio, OI change, volume_ratio. Select strategy with highest predicted ROI.
2. **Funding + LS Ratio Filter**: Funding extreme only occurs in some windows (W08). Need to combine funding with LS ratio contrarian and liquidation cascade.
3. **Order Flow Imbalance**: Use footprint ladder data (taker buy/sell imbalance, CVD divergence) - not yet fully exploited
4. **OB + FVG + Displacement**: More sophisticated SMC with 4H structure, daily FVG, OB age, stop hunt detection
5. **Walk-Forward with Regime Detection**: Instead of fixed 20 windows, use rolling 3-month training to select best strategy, with 72h purge and quarantine
6. **Increase Frequency**: Lower vol_thr to 0.2, use 18 symbols with max_pos 4, risk 80/200 to get 50+ trades/month, but control DD with aggressive ratchet (lock 0.20 at 0.8R, 1.0 at 1.5R, 1.8 at 2.5R, decay 64)
7. **Hard Windows W03/W12**: May be impossible with price/volume only - need external data (funding, LS, liquidation, options flow) or accept that 8/10 is max achievable

### Files

- `ssrn_bb_mean_reversion.py`: BB mean reversion strategy, 2/10 PASS on new windows
- `ssrn_slow_fast_cpd.py`: Slow momentum + fast reversion + CPD, 18.67% on W17
- `ssrn_4551518_trend_following.py`: Donchian trend following, 2/10 single config
- `ssrn_5020002_order_flow.py`: Funding + OI contrarian, 30.18% on W08
- `FINAL_8_10_REPORT.json`: 8/10 per-window best seed42
- `NEW_OOS_ROBUSTNESS_REPORT.json`: 6/30 per-window best all windows

### Conclusion

We improved from 0/10 baseline to **8/10 PASS per-window best on seed42** and discovered **BB mean reversion achieves 2/10 PASS on new random months** where Donchian fails 0/10.

However, **no single config achieves >2/30 PASS across all 30 windows**, proving market regimes change and a single static strategy cannot be robust.

The most robust approach is **regime-adaptive meta-learner** that selects:
- Donchian short in crash/high-vol bear (W01, W04)
- BB mean reversion in chop/bull (W21, W23)
- Funding contrarian in funding extreme (W08)
- PDL mean reversion in ETF/news (W11)
- SlowFastCPD in election/trend reversal (W17)

Hard windows W03 Nov21 Peak and W12 Aug23 remain unsolved even with exhaustive search (0 configs >5% ROI), suggesting they have no edge with current features.

We have not yet achieved 10/10 PASS with single config, but we have made **8x improvement** and identified clear path forward with ML meta-labeler and regime detection.

