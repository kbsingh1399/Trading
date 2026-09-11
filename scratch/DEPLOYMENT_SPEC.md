# DEPLOYMENT SPEC — "Trend Harvest" (validated 2026-09-12 branch arena/01a09166-trading)

**Status:** evidence-backed positive-edge configuration for live deployment.
**NOT a 20/20 mandate pass** — joint criteria still unmet (see §6); this is the
best-validated REAL-MONEY configuration from ~500 causal variants.

## 1. Signal families (all weekly-hold trend, SURV geometry)
Trades taken from the trailing-family gate ∩ BTC-tide guard over these families
(prices/metrics from Engine/binance_backtesting_data, 15m bars):

| Fam | Signal (causal inputs at bar close i) | Side |
|-----|----------------------------------------|------|
| T1  | close > donchian(384-bar) high (tide-consistent optional) / < low | long/short |
| T2  | sign(7d return) != 0; strong variant |r7_z|>1.5 | long/short |
| T3  | tide==long & 4h pullback <= -1.5% (mirror for shorts) | long/short |
| T6  | cross-sectional 7d momentum rank >0.89 / <0.11 (18-symbol universe) | long/short |

Geometry (SURV_W, R-unit = 15m ATR14 x 16 ≈ 16h-vol): horizon 1344 bars (14d),
initial stop -1R, BE-ratchet 1.0R->+0.15R, R-trail arms at +1.2R (distance 1.8R),
cooldown 96 bars per symbolfamily. HOLD 2.5-3.5 days typical.

## 2. Execution rules (live mapping)
- ENTRY: LIMIT at signal-bar close; cancel if unfilled after 8 bars (2h).
  (Model assumption maker25: 2bps entry fee. The config ALSO validated at taker41.)
- EXITS: stop/limit orders at -1R / ratchet / trail / 14d time stop (taker
  fees 8bps + 15bps slippage assumed; stress-tested +10bps).
- SYMBOL UNIVERSE: the 18 USDT perps in the data dir (BTC/ETH/majors; sizes below).
- POSITION LIMITS: max 5 concurrent; max 2 same-direction; 1 per symbol.
- TIDE GUARD (beta overlay): longs only when BTC 7d return > 0; shorts only when < 0.
- FAMILY GATE: per month (or rolling), allow families whose trailing 60d net
  expectancy > 0; fallback top-3 by trailing mean. Recompute monthly.
- METRICS OUTAGE RULE: T5/T9 (metric-input families) excluded when feeds imputed;
  price-only families may trade with metric features zeroed.
- SIZING: flat $40 risk per trade on $5,000 (0.8%); NOTIONAL ≈ $1.2-2.5k/position
  (stop ~1.6-3.2% = 16h ATR-scale). Liquidity trivial for majors.
- KILL SWITCH: halt new entries if live equity DD > 10% from peak or rolling 60d
  realized expectancy < all-in cost; resume only after re-qualification.

## 3. Validated out-of-sample (20 mandate windows, 2021-05 .. 2026-03)
Continuous live-equivalent book (C2 = tide guard + dir cap 2 + book 5 + $40):

| Fee regime | Total ROI | Avg monthly | Max DD | Pos months | Trades | WR | P(null>=obs) |
|------------|-----------|-------------|--------|-----------|--------|-----|--------------|
| taker 41bps (mandate) | **+42.5%** | +2.12% | **6.5%** | 13/20 | 244 | ~50% | **0.037** |
| maker 25bps | +39.5% | +1.97% | 9.0% | 13/20 | 260 | ~50% | 0.053 |
| maker +10bps stress | +37.1% | +1.85% | 9.2% | 13/20 | 260 | ~50% | 0.053 |

Null = 300 sims, matched per-window trade counts, random candidate subsets,
identical book/risk policy. Multiple-testing caveat: this config is the best
survivor of ~500 tried; deflated true confidence is weaker than 3.7-5.3%.

Per-window (20 isolated $5k books, C2): 1/20 full-criteria passes; many windows
<15 trades (mandate floor) — weekly trend cannot sustain 15 fills/month at book caps.
Dir-cap-1 variant (safety-first): DD 3.95%, ROI +13.4%, 129 trades — documented, not chosen.

## 4. Why ML was removed
Every ML/gating selector measured at-or-below random-ranking on this pool
(stage2/3/4 reality checks). The edge lives in the fat right tail (+5..15R,
5-8% of trades): monetize via BREADTH + risk budgeting, not cherry-picking.

## 5. Deployment ramp (recommend)
1. Paper-trade 4-8 weeks on live data with this spec (forward validation is the
   only true test; my P=3.7% is backtest-null-referenced).
2. If live expectancy >= cost + 2bps after >= 60 trades: go live at $40 risk.
3. Scale risk only with house money (per mission overlay), never martingale.

## 6. Mandate criteria — final honest state
Joint all-20 (ROI>=10% & DD<5% & WR>=40% & >=15 trades/window): NOT achieved by
any causal configuration of this campaign (best: 4/20). The 15-trades/window floor
is incompatible with weekly-hold trend + risk caps; +10%/month every month is
incompatible with a +2%/month-mean fat-tailed distribution. See MISSION_REPORT.md
§v3 for the corrected bps-accounting discovery (R-unit convention fix) and the
full run ledger.
