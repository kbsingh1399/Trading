# Data Expansion Blueprint — measured, not assumed

**Branch:** `arena/01a0a5bf-trading`

Every number below was measured on this repository's own data this session. The
external availability claims are cited.

---

## 1. Direct answer: cross-sectional expansion is mathematically ruled out

I measured the cross-symbol correlation of the volatility rank — the exact
quantity whose episodes form our ceiling:

```
core-11 common window 2020-11 .. 2026-09, 12,806 4h bars
cross-symbol vol-rank correlation: mean 0.697
                                   min  0.463  (BTCUSDT-TRXUSDT)
                                   max  0.864  (ADAUSDT-DOTUSDT)
correlation with BTC:              mean 0.654
```

At ρ = 0.697 the effective number of independent series is `k / (1 + (k−1)ρ)`:

| symbols k | 11 | 18 | 30 | 40 | 50 | 100 |
|---|---|---|---|---|---|---|
| **n_eff** | **1.380** | 1.402 | 1.416 | 1.421 | 1.424 | **1.430** |

**Going from 11 symbols to 100 moves n_eff from 1.380 to 1.430.** Adding 89
altcoins buys 3.6% more independent information. Crypto volatility is one
factor with eighteen noisy observations of it, not eighteen independent
regimes.

So the answer to your question 2 is unambiguous: **neither, if the goal is
statistical power** — and between the two, cross-sectional is not merely
weaker, it is asymptotically useless. It adds *trades*, and trades inside one
episode are not independent.

One incidental finding: the repository already holds **18 symbols** with
master parquets while `CORE_SYMBOLS` uses **11**. APT, ARB, AVAX, NEAR, OP, SOL
and SUI are sitting unused. Adding them is free and worth doing for
diversification, but it will not move the ceiling — n_eff goes 1.380 → 1.402.

---

## 2. Temporal expansion is the only axis that adds episodes — and it is capped

Episode rate measured on this dataset (any-core-symbol `vol_rank ≥ 0.88`,
60-day gap clustering):

```
8 clusters over 5.77 years  ->  1.39 episodes/year
2021-05  2022-05  2023-06  2023-10  2024-07  2025-10  2026-02  2026-06
```

| n episodes required | years needed |
|---|---|
| 10 | 7.2 |
| 20 | 14.4 |
| **30** | **21.7** |

Against available history:

| source | years | episodes |
|---|---|---|
| this dataset (2020-09 →) | 5.8 | 8 |
| Binance USDT-M perp inception (2019-09) | 6.8 | ~9 |
| CME BTC futures (2017-12) | 8.6 | ~12 |
| BTC spot (2010 →) | 15.8 | ~22 |
| equity index futures (1986 →) | 40+ | ~48 |

**Crypto perpetual futures physically cannot supply 30 episodes.** The
instrument is 8 years old and the maximum backward extension of our current
series is about one year, worth one extra episode.

A caveat worth stating: the episode count is **definition-sensitive**. I get 5
(BTC alone, my reimplementation), 6 (BTC via the 4h cache, which is what the
trade-level analysis used), 7 and 8 (other reimplmentations and the any-of-11
union). The ceiling is real but it is somewhere in 5–8, not a single precise
number.

### I also checked whether a different conditioning variable would yield more events

All of these are already in the data:

| conditioning variable | episodes | bars firing |
|---|---|---|
| BTC `vol_rank ≥ 0.88` (current) | **7** | 1,458 |
| `funding_rate_pct` \|z\| ≥ 2 | 1 | 77,753 |
| `oi_change_pct` \|z\| ≥ 2.5 | 1 | 34,360 |
| `long_liq_zs ≥ 2` | 1 | 61,422 |
| `short_liq_zs ≥ 2` | 1 | 45,540 |
| `liq_imbalance_ratio` \|z\| ≥ 2.5 | 1 | 23,693 |

They fire on 1–3% of bars *per symbol* and, unioned across symbols, chain
together under the 60-day gap rule into a single episode. At these thresholds
they are persistent states, not events. Tightening them into sparse events is
possible but is itself a tuning exercise on n=7 — precisely the curve-fitting
you correctly want to avoid. **`vol_rank` is the best available conditioning
variable, not the worst.**

---

## 3. What n=30 would actually buy

Minimum detectable effect, paired t on episode-level effects, two-sided
α=0.05, 80% power, `MDE = (t_crit + t_beta)/√n`:

| n | crit \|t\| | MDE (SD) |
|---|---|---|
| 6 | 2.571 | 1.425 |
| **7** | **2.447** | **1.267** ← we are here |
| 15 | 2.145 | 0.778 |
| **31** | **2.042** | **0.520** ← your target |
| 60 | 2.001 | 0.368 |

| effect size | n needed | years of crypto-perp history |
|---|---|---|
| 1.0 SD | 10 | 8.2 |
| 0.8 SD | 15 | 12.4 |
| 0.6 SD | 24 | 19.8 |
| 0.5 SD | 34 | 28.0 |
| 0.4 SD | 52 | 42.9 |

**n>30 buys the ability to detect a ~0.5 SD episode-level effect.** That is a
genuinely useful threshold — it is roughly where a real risk filter lives. But
it costs 28 years of a market that is 8 years old.

---

## 4. The reframe: you are asking for two different things

**Goal A — statistical power for the volatility-regime question.**
Capped at ~9 episodes in crypto perps. **Unreachable.** No pipeline fixes this.

**Goal B — capability: implementing the methods we found unimplementable.**
Felder microprice, Cont multi-level OFI, Tapiero depth, and the Rajendran
adverse-selection classifier all need bid/ask/depth/spread. **This is
achievable** — and it is a completely separate investment from Goal A.

The blueprint below treats them separately, because conflating them is how a
team spends money on data and still can't answer the question.

---

## 5. Recommendation

### Tier 0 — free, do it now (no data acquisition)

1. **Stop testing filters on n≤8.** Adopt cluster-robust inference: use all
   1,135 trades but compute standard errors at the episode-cluster level. This
   does not create power; it stops us mistaking 180 correlated trades for 180
   observations.
2. **Add the 7 unused symbols** (APT, ARB, AVAX, NEAR, OP, SOL, SUI) to
   `CORE_SYMBOLS` for diversification — with the explicit understanding that
   n_eff moves 1.380 → 1.402 and the ceiling does not move.
3. **Only ship effects ≥ 1.27 SD** on episode-level tests, or ship nothing.
   That is what n=7 can actually resolve.
4. **Repurpose the CVaR harness from validation to monitoring.** It cannot
   prove a gate works on n=7, but it is the right instrument for detecting
   regime deterioration live.

**Tier 0 fixes the decision problem without spending anything. It is the only
tier I recommend committing to now.**

### Tier 1 — Goal B, capability (real cost, real payoff)

This is what actually unblocks the literature. Verified availability:

- **Binance futures L2 is available from January 2020** — `S_Depth` snapshots
  (BTC/USDT only) and `T_Depth` tick-level (all symbols), but it requires a
  **whitelisted futures account** and is downloaded via a signed API, not a
  public bucket. [4](https://stackoverflow.com/questions/72066143/i-cant-get-binance-futures-order-book-historical-data)
- **`data.binance.vision` bookTicker is stale** — reported last updated in
  2024. Do not build a pipeline on it. [10](https://dev.binance.vision/t/how-and-where-can-i-get-the-history-bookticker-data/36122)
- **Tardis.dev** carries Binance spot `incremental_book_L2` for BTCUSDT from
  **2019-12-01** (paid vendor). [7](https://docs.tardis.dev/historical-data-details/binance)
- **Bybit** publishes L2 order book at 200 levels, roughly 2+ years. [1](https://www.reddit.com/r/algotrading/comments/1pfsixt/order_book_data_for_btc/)
- **The Rajendran & Singaravelu dataset itself** — the paper I recommended in
  Phase 4 — is reported to distribute 1 year of processed L2 features as CSV
  via its SSRN page (abstract 6344338). [1](https://www.reddit.com/r/algotrading/comments/1pfsixt/order_book_data_for_btc/) **This is the highest-value, lowest-cost single step in this entire document**, and I have not verified it myself — it is a third-party claim about that SSRN listing.

Note what Tier 1 does **not** do: it does not add a single volatility episode.
It lets us *build* the adverse-selection model. Whether that model helps is
still constrained by n≤8 for regime-level claims — though adverse selection is
a **trade-level** phenomenon and may be testable at trade level with clustered
errors, which is a materially better-powered question.

### Tier 2 — Goal A, the only real route to n>30

**Validate the mechanism on equity index futures, then transfer.** 40+ years
gives ~48 episodes. The mechanism under test is asset-agnostic: *does a
volatility-regime gate reduce triple-barrier tail losses?* If it does on 48
episodes of ES/NQ and fails on 7 episodes of BTC, the crypto result was noise.
If it holds on both, we have real evidence.

Cost: a new instrument adapter (different session hours, tick sizes, contract
rolls, no 24/7 trading, no funding). Transfer risk is real and must be treated
as a hypothesis, not an assumption.

---

## 6. Architecture and validation requirements (for whichever tier proceeds)

### Pipeline

```
raw/                    immutable, content-addressed, never rewritten
  binance/{sym}/{stream}/{YYYY-MM}.zip
  vendor/{tardis,bybit}/...
stage1/                 decoded, schema-validated, timezone-normalised UTC
stage2/                 resampled to 15m + 4h, features attached
master/                 {SYM}_15m_master.parquet  +  {SYM}_4h.parquet
manifest/               one JSON per symbol per stage
```

Rules that must be enforced in code, not convention:

1. **Content-addressed raw storage.** Hash every downloaded file; re-downloads
   must reproduce the same hash or the build fails. This is how we would have
   caught the `atr_pct` vs `trailing_30d_atr_pct` bug in Phase 1 at ingest
   rather than in a backtest.
2. **Sequence-validated L2 reconstruction.** Order book rebuilds must verify
   the `U`/`u` sequence numbers and restart from a snapshot on any gap. A
   silently gapped book fabricates depth.
3. **Provenance in every row.** Each master row carries the source file hash
   and the ingest timestamp.
4. **No in-place mutation.** A rebuild produces a new version; the old one
   stays addressable so any published number can be reproduced exactly.

### Validation gates (each one a hard fail)

| gate | test |
|---|---|
| completeness | bar count == expected for the date range; no gaps > 1 interval |
| monotonicity | `open_time_ms` strictly increasing, no duplicates |
| OHLC sanity | `low ≤ min(open,close) ≤ max(open,close) ≤ high` on 100% of bars |
| no future data | every derived feature at bar *t* recomputes identically from data `< t` |
| volume reconciliation | `taker_buy_vol + taker_sell_vol ≈ volume_base` within tolerance |
| corporate-action / roll | futures contract rolls documented and adjusted |
| survivorship | the symbol list is fixed *before* the backtest, and delisted assets are retained |
| **episode census** | the independent-episode count is reported with every result |
| **cost reconciliation** | realised bps matches `ROUND_TRIP_BPS` exactly |

The last two are new and come directly from what we learned: every result must
state its effective n, and every cost must reconcile to the single constant.

### Statistical protocol

- Report **episode-clustered n** alongside trade n on every scorecard.
- Report the **MDE** for the n actually achieved, so a null result is
  distinguishable from an underpowered one.
- **Pre-register** every threshold before running, as we did for the 3.0×/1.5×
  stress schedule.
- Score gates by **CVaR efficiency vs random**, never by PnL.

---

## 7. What I have not verified

- The claim that the Rajendran & Singaravelu L2 feature CSV is downloadable
  from SSRN comes from a third-party forum post, not from SSRN. **Verify before
  budgeting around it.**
- Binance's L2 whitelist terms, current pricing and retention may have changed;
  the January-2020 start date is from a 2022 Stack Overflow answer.
- I did not price Tardis.dev or Bybit data, and did not confirm Bybit's exact
  retention window.
- The episode rate of 1.39/year is an estimate from 8 observed episodes; its
  own sampling error is large, so the "21.7 years" figure is indicative.
- Whether the adverse-selection mechanism transfers from equities to crypto
  perpetuals is untested — that is the entire risk in Tier 2.
