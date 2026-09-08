# RP2 ROUND 11 — Regime-Adaptive Reclaim Engine

**Status:** code complete, 81/81 invariants verified, **NOT yet validated on real data**
**Supersedes:** `rp2_round10_convex_trend_following_ml.py`

---

## 0. READ THIS FIRST — no performance claim is made here

Round 11 has **not** been run against the real corpus. The session that authored
it had all external network egress denied by the sandbox proxy (every host,
including `raw.githubusercontent.com` and `objects.githubusercontent.com`,
returned HTTP 403 with header `x-deny-reason`), so the 2.2 GB parquet dataset was
physically unreachable and `pip install` was impossible.

Everything in this document is a **design and invariant** claim, verified by
`verify_rp2_round11.py`. The 20-window scorecard must be produced locally:

```bash
python Engine/runners/run_rp2_round11_walkforward.py \
    --data-dir Engine/binance_backtesting_data \
    --windows  Engine/oos_windows_20.json \
    --out      rp2_round11_results.json
```

The runner **refuses to run** without both parquet files per symbol and will
never fall back to synthetic data.

---

## 1. Round 10 root cause — it was a DATA PROVENANCE failure, not a signal failure

Round 10 was not merely badly tuned. It was gated on columns that **do not exist**
for roughly 40% of the walk-forward period.

From `Engine/binance_backtesting_data/*_dataset_manifest.json`, field
`provenance.metrics_unavailable_fraction_by_year`:

| Symbol | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| ADAUSDT | 1.0 | 0.9189 | **0.8656** | 0.0001 | 0.0008 | 0.0004 | 0.0 |
| BTCUSDT | — | 0.0039 | **0.8656** | ~0 | ~0 | ~0 | ~0 |

The Binance **derivatives metrics archive** is missing (and forward-filled) across
these spans. Round 10 gated entries on `taker_volume_ratio`, `whale_index` and the
liquidation z-scores — all metrics-archive columns.

OOS windows W1–W8 span 2021-05 → 2022-11. So **8 of 20 windows were gated on
flat-lined, interpolated values masquerading as live orderflow.** `Engine/core/schema.py`
states this explicitly for `is_imputed_metrics`:

> RETROSPECTIVE ONLY: not for contemporaneous live signals.

Round 10's -4.25% ROI / 21.9% win rate on W1 is what a gate looks like when its
input is a constant.

---

## 2. The fix — a two-tier data contract

**TIER_A — provably real on every bar. Only these may gate an entry.**
OHLCV, `volume_base/quote`, `volume_sma9`, `trade_count`, `rsi_14`, `atr_14`,
`atr_100`, `ema_8/21/50/200/800`, `future_cvd_15m`, `spot_cvd_15m`, `zc_div`,
`taker_buy_count`, `taker_sell_count`, `taker_buy_vol_btc`, `taker_sell_vol_btc`,
`avg_trade_size_usd`, `spot_close`, `session_vwap`, `vwap_zscore`, `volume_ratio`,
`session_vah/val`, `prev_day_vah/val`, **and the entire footprint ladder**
(manifests report `synthetic_rungs: 0` for all 18 symbols).

**TIER_B — metrics archive, quarantined. May NEVER gate an entry.**
`funding_rate_pct`, `basis_usd`, `open_interest_k/usd`, `oi_change_pct`,
`long_liq_usd`, `short_liq_usd`, `ls_ratio_global`, `ls_ratio_top`,
`top_account_ratio`, `whale_index`, `taker_volume_ratio`, `long_liq_zs`,
`short_liq_zs`, `liq_imbalance_ratio`.

TIER_B enters the ML matrix **only multiplied by an availability mask**
(`tierb_avail = is_imputed_metrics < 0.5`) and paired with that mask, so the model
learns to ignore it in the eras where it is absent. Enforced by invariants 4.1–4.8.

---

## 3. The sizing arithmetic — why flat 1.0% risk cannot work

Target: +20% on 5,000 USD = +1,000 USD per month, with max drawdown < 5%.

At flat 1.0% risk (50 USD = 1R), +1,000 USD requires **+20R net**.
A clean 4R:1R at exactly 40% win rate gives `0.40*4 - 0.60*1 = +1.00R` per trade
before friction — about 20 trades gross, ~26 after 41 bps round trip.

But at a 60% loss rate over ~26 trades, the **expected longest losing run is ~4.5**,
and **5 consecutive flat 1.0% losses consume the entire 5% drawdown budget.**

> Flat 1.0% risk is arithmetically self-defeating: variance breaches the drawdown
> ceiling before the edge has room to express itself.

Second incompatibility: the mission's suggested **2.5R hard exit** yields
`0.40*2.5 - 0.60 = +0.40R` per trade → roughly **+6% ROI at 15 trades**. A 2.5R cap
**cannot** reach +20% at the mandated trade count. The 4.0R barrier (extending to
6.0R–8.0R on liquidation cascades) is load-bearing, not decorative.

**Resolution — house-money sizing:**

```
risk_usd = base_risk(0.35%) + kelly_frac(0.42) * max(0, banked_profit)
           capped at risk_cap_pct = 2.0%
           hard floor at principal_floor_frac = 0.955 of starting capital
```

Opening risk is 0.35%, so five straight opening losses cost 1.75% — comfortably
inside the 5% budget (invariant 3.5). Risk expands only against **realised** profit,
so the principal is never the thing at risk. `--flat-risk` reproduces the naive
1.0% behaviour for side-by-side comparison.

---

## 4. Strategy architecture

### 4.1 Entry: DISPLACEMENT → PULLBACK → RECLAIM

Round 10 bought the breakout and died in retracement traps. Round 11 **never buys
the break**. A three-state machine, strictly left-to-right with no forward reads:

1. **ARM** — bar breaks the Donchian-55 channel (channel excludes the current bar),
   bar range >= `1.45 * ATR14`, EMA ribbon aligned.
2. **PULLBACK** — a later bar retraces between `0.25` and `1.30` ATR from the impulse
   extreme without closing back through the broken level. Deeper → disarm.
3. **RECLAIM** — a bar closes beyond the pullback swing extreme with orderflow
   confirming. Decision is that bar; **fill is the next bar's open.**

The stop sits under the *pullback* extreme (tight 1R) while the 4R target is
anchored to the *impulse*. This is the whole point: it materially improves
friction-per-R versus stopping under the breakout bar.

### 4.2 Confirmation — weighted score, not a conjunctive AND

Measured marginal pass rates for the Round 10-style gates were roughly
`cvd_z 0.217`, `fp_delta 0.181`, `fp_score 0.130` — a joint pass rate near **0.004**.
That starves the ">= 15 trades per window" floor regardless of setup quality.
(Harness measurement: of 99 valid reclaims, the 4-way AND admitted **zero**.)

Round 11 accumulates a weighted confirmation score out of 8.0 and requires >= 3.0:

| component | weight | threshold |
|---|---|---|
| `cvd_z` (side-aware) | 2.0 | 1.00 |
| `fp_delta_ratio` | 2.0 | 0.12 |
| `footprint_score` (0..6) | 3.0 | 3 |
| `taker_imb` | 1.0 | 0.05 |

Half credit at 50% of threshold, so no single marginal reading vetoes a textbook setup.

**The institutional spot-distribution check remains an ABSOLUTE VETO** — it is a risk
control, not a confirmation, and cannot be scored away (invariant 4.7):
longs vetoed when `zc_div_z <= -0.80`, shorts symmetrically.

### 4.3 Regime classifier

Causal 3-state TREND / CHOP / SHOCK from trailing `rv_rank` (realised-vol percentile)
and `eff_ratio` (efficiency ratio). Modulates the risk multiplier
`(1.00, 0.55, 0.75)` and hold caps through a **fixed closed-form mapping** — never a
per-window lookup table (invariants 6.1–6.4).

### 4.4 ML overlay

Dependency-free (numpy + pandas only; **no sklearn, no scipy**):
`_HistGBDT` (histogram GBDT on logistic loss, train-only bin edges) blended 0.60 /
0.40 with `_RidgeLogit` (train-only mu/sd), PAVA isotonic calibration, triple-barrier
labels (+4R / -1R, 96-bar horizon).

**Quantile thresholding, not an absolute probability grid.** The +4R base rate is only
2–8%, so calibrated probabilities never clear a 0.30 absolute cut and such a grid
silently disables the model — a lesson paid for in an earlier round. `gate_soft=True`
falls back to raw setups when no positive-EV quantile exists.

### 4.5 Exit ratchet (anti-suffocation)

| trigger | stop moves to |
|---|---|
| +1.0R | entry +0.10R (breakeven lock) |
| +2.0R | entry +1.00R (profit lock) |
| +3.2R | entry +2.20R (protect the approach to 4R) |
| >= +3.5R | 2.2 × ATR14 chandelier trail from the running extreme |

TP ceiling 8R; cascade TP 6R in SHOCK. `--fast-ratchet` implements the mission's
alternative (+0.8R / +1.5R locks, 2.5R hard exit) — provided for comparison, but see
section 3 for why a 2.5R cap cannot reach +20%.

### 4.6 Pyramiding

At most **one** 0.50× add leg, only when the stop is locked at breakeven-or-better
**and** MFE >= 1.20R, bounded by the gap budget. R geometry always anchors to the
first-leg entry, never the blended price.

---

## 5. Execution kernel — deliberate ordering

Per bar `t`:

1. Open positions from candidates decided at bar `t-1`, filled at `open[t] * (1 ± eslip)`.
2. Resolve intrabar exits from `high[t]`/`low[t]`, **stop checked before target** (conservative).
3. Ratchet from `close[t]`, effective `t+1` — done *after* step 2 so a favourable
   extreme cannot ratchet and exit within the same bar.
4. Mark to market and test the drawdown breaker on the **worst-case intrabar fill
   including exit slippage and fees**, not the close.

Sizing: `qty = risk / (r_unit + entry * xslip)` so the realised stop loss stays <= `risk_usd`.
Separately `qty_gap = (3.0 * risk) / (0.12 * entry)`, and the minimum is taken — a tail
gap prices **notional**, not the stop.
Friction viability filter: reject the setup if `(41 bps * entry) / r_unit > 0.22`.

### Note on the "33 bps" headline

The mandate enumerates four legs — 8 bps taker entry + 8 bps taker exit + 10 bps entry
slippage + 15 bps stop slippage — which sum to **41 bps, not 33**. The 33 bps label
charges the taker fee only once. **Round 11 models the full 41 bps** (fee on both legs).
Never model less friction than reality.

---

## 6. Causality contract

- Every feature shifted 1 bar before use; Donchian excludes the current bar.
- **Truncation test** (invariants 1.11–1.14): features, regime labels and setups at bar
  `i` are bit-identical when all bars after `i` are deleted from the input. This is the
  strongest available proof of no lookahead.
- Training events terminate at or before `window_start - 72h` (`purge_hours=72`).
- GBDT bin edges and Ridge mu/sd are frozen on train and immutable at test (5.4, 5.5).
- No RNG anywhere in the strategy module (7.1); two identical runs are bit-identical (7.3).
- CVD is scale-normalised before z-scoring because the raw level has a unit root.

---

## 7. Verification

```bash
python Engine/verification/verify_rp2_round11.py
```

**81/81 invariants pass.** Groups: causality/anti-lookahead, execution & fill semantics,
risk & drawdown governor, data provenance, ML purge & freeze, no-lookup-table,
determinism & end-to-end, mission-criteria wiring, fixture containment.

The suite builds a schema-exact **parquet fixture** solely to exercise the real
dual-parquet code path. The fixture is deterministic (a logistic map, no RNG) and the
suite is **hard-blocked from printing any performance metric** (invariant 9.1). It is a
harness, not a backtest, and must never be cited as evidence of edge.

### Bugs this verification actually caught

1. **`va_lo`/`va_hi` were entirely NaN.** They were seeded with NaN and reduced with
   `np.minimum.at`; since `min(nan, x) = nan`, the value-area band was silently dead
   for every candle. Now seeded ±inf.
2. **Dead armed state.** An armed setup past `arm_expiry_bars` with `pb_seen=True`
   could neither fire nor reset until a later stale sweep — it froze. Now disarms
   unconditionally on expiry.
3. **The conjunctive confirmation AND admitted 0 of 99 valid reclaims** (section 4.2).

---

## 8. Open risks

- **No real-data validation has occurred.** Whether the strategy passes is unknown.
- The ">= 15 trades per window with max 2 concurrent positions" constraint is tight;
  if windows come in thin, `conf_min_score` is the correct first dial (it is a
  continuous knob, not a cliff) — but any retune must be applied **globally**, never
  per window.
- Windows are non-contiguous, cherry-picked event months (W1 2021-05 Great Liquidation
  Crash, W5 2022-05 Terra-Luna, W8 2022-11 FTX, W7/W18 low-vol chop). A trend engine
  will structurally struggle on the chop windows; expect those to be the binding
  constraint, and read the runner's FAILURE ATTRIBUTION block before changing anything.
