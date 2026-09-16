# Research Corpus Review — Findings & Proposal

**Branch:** `arena/01a0a5bf-trading` · **Commit:** `2f78f50`

---

## 0. Three corrections to the brief

**a) The Volatility Regime Governor was not validated — it was falsified.** Last turn's
measurement: t = −0.148 on 6 independent volatility episodes (df=5, critical 2.571), positive
in 3/6, net **−98.81** across all three window sets. It is not a shipped circuit breaker and
must not be treated as a validated baseline component.

**b) `docs/research_papers/` contains 5 unique PDFs, not 80+.** Six files exist but
`crypto_orderflow_sample.pdf` and `optimal_execution_cryptocurrency_markets.pdf` are
byte-identical (md5 `b2262af9…`). The broader corpus is markdown, not PDF: **74** individual
paper summaries in `docs/ssrn_research/` plus synthesis documents.

**c) The "883 physical papers" corpus is not in the repository.** The audit header cites
`papers/` (340 files) and `papers/Master_Batch_1/` (543 files). In fact `papers/` holds **12**
files — all metadata, link lists and a 1.25 MB analysis JSON — and **`papers/Master_Batch_1/`
does not exist**. The audit is a catalogue of papers that were analysed elsewhere, not a
library present here.

I reviewed what is actually present: the two documents you named, the 74 SSRN summaries, and
the 5 real arXiv PDFs.

---

## 1. Every headline candidate fails one of three tests

The audit's §2 distils the corpus into three concrete formulations. I tested each against the
actual dataset rather than accepting the citations.

### 1.1 Not implementable — the required data does not exist

| Candidate | Requires | Status in dataset |
|---|---|---|
| **Felder (SSRN 4320775)** microprice / post-only quoting | best_bid, best_ask, spread, queue volume | **all ABSENT** |
| **Tapiero (SSRN 6688399)** multiplicative depth condition | Depth_Bid, Depth_Ask | **ABSENT** |
| **Cont, Kukanov, Stoikov (2014)** multi-level OFI | K-level order book snapshots | **ABSENT** |

Verified directly against `BTCUSDT_15m_master_2020_2026.parquet`: no `best_bid`, `best_ask`,
`bid_depth`, `ask_depth`, `spread` or `microprice` column. The footprint ladder carries
per-price-bin traded volume — that is a *trade* footprint, not a resting-order book.

A further caution on Felder specifically: its headline claim is "reclaims 41.0 bps round-trip
friction." Modelling maker fills as free is the single most common source of fantasy backtest
PnL, because passive fills are adversely selected — you get filled precisely when the price
moves against you. Without queue and adverse-selection data, that 41 bps cannot be claimed
honestly here at any implementation quality.

### 1.2 VPIN (Easley, López de Prado, O'Hara 2012) — implemented and FALSIFIED

This was the strongest candidate on paper: not yet applied, computable from our
`taker_buy_vol`/`taker_sell_vol` columns, a pure market-state measure (so it survives the
model-refit problem that killed the Bayesian tracker), and microstructure-native. I built a
strictly causal volume-synchronized implementation (`scratch/vpin_prototype.py`, 10,641,855
buckets over 211,189 BTC bars) and tested the specific claim at
`COMPREHENSIVE_QUANT_RESEARCH_PAPERS_KNOWLEDGE_BANK.md:201`.

| Test | Documented claim | Measured |
|---|---|---|
| Cascade threshold | VPIN > 0.80 signals imminent cascade | **max 0.7577, p99 0.3414 — 0.80 never reached (0/211,088 bars)** |
| Leads cascades | "preceded every major cascade by 2 to 6 hours" | VPIN in the 24h **before**: May-21 **0.0699**, LUNA **0.0697**, FTX **0.0793** — all **below** the 0.1144 median |
| Predicts volatility | toxicity → dislocation | **inverse**: top-5% VPIN → 0.69× the forward 24h \|return\| of the bottom 50% |

VPIN is a real, monotone signal — decile 1 → 10 maps cleanly onto forward \|return\| 2.472% →
1.623% — and it carries independent information beyond prior realised volatility
(t = −21.44, incremental R² = 0.002). But it points the **opposite way** to the toxicity
thesis. A VPIN veto built to the documentation would suppress entries in *low*-volatility
windows and pass them in *high*-volatility ones.

The likely cause is granularity: VPIN is a tick-data statistic. At 15m aggregation the
order-flow information it measures has already been averaged away, and what remains is a
weak inverse-volatility artefact.

### 1.3 Xuan funding-Z (SSRN 6872638) — partially applied, and the full rule is FALSIFIED

The engine already carries a one-sided fragment at `s1_dual_model_orderflow.py:362`:
`if side == 1 and funding >= 0.035 and slope < 0.25: continue`. I tested the full two-sided
Z-score rule on BTC 15m:

| Condition | n | 24h | 4d | 14d |
|---|---|---|---|---|
| All bars | 193,309 | +0.129% | +0.482% | +1.844% |
| Funding_Z > +1.5 → **mean-reversion short** | 19,444 | +0.073% | **+0.748%** | **+2.342%** |
| Funding_Z < −1.5 → **momentum long** | 23,991 | +0.222% | +0.474% | +1.341% |

The crowded-long leg is **wrong-signed** at 4d and 14d — expensive funding was followed by
*higher* returns, not reversion. Across funding-Z deciles there is **no monotonicity**
(+0.473, +0.345, +1.026, +1.122, +0.197, +0.587, −0.159, +0.239, +0.386, +0.742).

**Conclusion: no alpha overlay in this corpus survives contact with the data.** That is the
finding. Proposing one anyway would repeat the pattern of the last three attempts.

---

## 2. What the review actually surfaced: two structural defects

Checking implementability required reading the labeler closely, which exposed two defects
that affect **every** PnL figure in the repository, including the +5,553.70 baseline.

### Defect 1 — the ATR floor disables volatility adaptivity on 98% of bars

`fast_numba_oos_engine.py:288-290`:

```python
atr_raw = df["atr_14"].fillna(df["close"] * 0.01)
min_atr = df["close"] * 0.012          # "Volatility targeting minimum 1.2% price stop"
atr     = np.maximum(atr_raw, min_atr)
```

Measured across all 11 certified symbols: `atr_14/close` medians run 0.00287 (TRX) to 0.00651
(LINK) — every one far below the 0.012 floor. The floor binds on **92.45% of all bars**
(BTC 98.18%, DOGE lowest at 87.63%). Consequently, for **every** symbol:

```
R as % of price:  p10 1.440%   p50 1.440%   p90 1.440-1.587%
```

**R is a constant.** The triple-barrier geometry (stop 1.2R, target 3.0R) is therefore a
fixed-percentage grid — stop 1.440%, target 4.320% of price — on essentially every bar. The
strategy is described throughout as ATR-adaptive; it is not. This also means the
vol-sensitivity of the entire label set is illusory.

### Defect 2 — friction is under-charged and internally inconsistent

| Sleeve | Charged | In bps | Documented |
|---|---|---|---|
| S1 (ML) | 0.18 R | **25.9 bps** | 41.0 bps / −0.25R |
| T1 (breakout) | 20.5 bps of price | **20.5 bps** (0.357 R) | 41.0 bps / −0.25R |

Both the engine docstring (`s1_dual_model_orderflow.py:30`) and the runner docstring
(`run_20_oos_dual_model.py:6`) state **41.0 bps round-trip**. Neither sleeve is charged that,
and the two sleeves are charged differently — T1 pays 79% of what S1 pays.

Re-running the full 20-window suite across the friction dimension:

| friction_r | bps | Total PnL | Trades | Pass |
|---|---|---|---|---|
| 0.14 | 20.2 | +4,471.89 | 659 | 10/20 |
| **0.18 (current)** | **25.9** | **+5,553.70** | 674 | 10/20 |
| 0.22 | 31.7 | +2,881.15 | 544 | 6/20 |
| 0.25 | 36.0 | +2,978.79 | 577 | 6/20 |
| **0.2847 (documented 41 bps)** | **41.0** | **+4,130.39** | 578 | 7/20 |
| 0.32 | 46.1 | +2,637.25 | 452 | 6/20 |

Two things follow. **At the documented 41 bps the baseline is +4,130.39, not +5,553.70** —
1,423.31 lower, with passes falling 10 → 7. And the curve is **jagged, not smooth**: a 5.8 bps
increase (0.18 → 0.22) nearly halves PnL and drops four passes, while a further 6 bps
recovers most of it. A pure cost constant should produce a smooth, monotone decline.

The jaggedness is real, not noise: friction shifts `realized_r` across zero, which
reclassifies wins and losses, which flips `consec_losses_s1`, symbol cooldowns, the 4.40%
circuit breaker and the risk-tier ladder. Those are discrete state changes that cascade
through the whole window. But it means **the current 0.18 setting sits on a local peak of a
brittle response surface**, and the headline number is an artefact of that placement.

---

## 3. Proposal

I am not proposing an alpha overlay, because the corpus does not support one. I am proposing
the work that has to precede any further alpha search.

### Phase 1 — Friction parity (small, mechanical, no tuning)

Replace both sleeves' friction with a single explicit round-trip cost in price terms:

```python
ROUND_TRIP_BPS = 41.0                       # one constant, documented, auditable
fric_r = (entry_px * ROUND_TRIP_BPS / 1e4) / r_dist
```

Applied identically in `label_triple_barriers_numba` (S1) and `load_t1_breakout_trades` (T1).
Remove `friction_r` from the labeler signature so it cannot drift. This is a *conservative*
change: it lowers reported PnL and makes the number defensible.

**Expected effect:** baseline moves from +5,553.70 to approximately **+4,130.39**. That is
the honest starting point, and it should be re-blessed as the new gold standard.

### Phase 2 — Decide the ATR floor deliberately

The 1.2% floor should either be (a) lowered or removed so ATR adaptivity actually operates,
or (b) kept, with every docstring corrected to describe a fixed-percentage barrier grid.
Option (b) is the smaller change; option (a) is the more honest strategy. Either way the
current state — described as adaptive, behaving as fixed — must not persist. This one is a
decision for you, not a measurement, so I have not made it.

### Phase 3 — Only then, re-open the alpha search

With friction and barriers settled, the search space that remains is honest:

- **VPIN as inverse-volatility input**, not as a toxicity veto — it is the one signal that
  survived measurement, with the sign flipped. Use it for *sizing* (scale down when
  forward-vol expectation is high), never for direction.
- Pre-register the threshold before looking at any scorecard.
- Validate on `oos_windows_20_random.json` plus the 25-window expanded set, and report
  episode-clustered n, since any slow-moving regime statistic produces autocorrelated
  activations.

---

## 4. OOS validation methodology for Phase 1

Friction parity is not a hypothesis, so it needs verification rather than significance
testing:

1. **Parity assertion.** Unit-test that S1 and T1 both deduct exactly
   `entry_px * 41e-4 / r_dist` for identical inputs. This is deterministic and must be exact.
2. **Control invariance.** With `ROUND_TRIP_BPS` set to the S1-equivalent 25.9 and the T1
   path unchanged, the suite must reproduce **+5,553.70 exactly**. Any drift means the
   refactor altered behaviour beyond friction.
3. **Monotonicity re-check.** Re-run the 6-point friction sweep after the refactor. The curve
   should remain jagged (that is inherent to the discrete risk ladder), but S1 and T1 must
   now move *together*.
4. **Full three-set re-baseline.** Re-run primary, holdout and expanded sets, and republish
   all three totals. Every downstream comparison in this repository is anchored to these.
5. **No threshold selection.** Phase 1 has no free parameter. If a variant produces a better
   number, that is a reason to distrust the variant, not to adopt it.

Tooling is already in place: `--friction-r` (commit `2f78f50`), `--disable-governor`
(control), `--windows` (holdout), `--out-json`.

---

## 5. Verification performed

- VPIN built from scratch and validated against the documented cascade claim on BTC
  (211,189 bars → 10,641,855 volume buckets); distribution, event-window and forward-return
  tests all reported above.
- Funding-Z tested on 193,309 bars with 96-bar rolling Z, full two-sided rule plus the
  existing one-sided fragment.
- Column absence verified directly from parquet schemas, not from documentation.
- Friction sweep: 6 full 20-window suite runs through the real runner entry point.
- ATR floor binding measured on all 11 symbols (2,323,304 bars total).
