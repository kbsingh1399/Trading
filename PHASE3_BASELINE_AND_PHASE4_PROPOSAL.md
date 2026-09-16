# Phase 3 Result + Phase 4 Research Proposal

**Branch:** `arena/01a0a5bf-trading` · **Commits:** `81eaa77` (Phase 3) · this document

---

# PART 1 — Phase 3: the final ultra-hardened baseline

## What was removed

`score_test_candidates` lowered `effective_calib_thresh` by `vol_shift_amt` (0.025) whenever
trailing BTC 30d ATR fell below `vol_shift_thresh` (0.92). That is an accelerator — the system
traded **more** aggressively in calm conditions. It is gone from
`Engine/strategy/s1_dual_model_orderflow.py` (constructor params, instance attributes, the
`score_test_candidates` signature and the branch), along with the now-dead `trailing_vol`
plumbing in `run_20_oos_dual_model.py` and `local_engine.py`.

**Verification:** `scratch/test_friction_parity.py` extended to **30 assertions, 0 failures**. No
`vol_shift_*` or `trailing_vol_pct` remains in code, no threshold-lowering arithmetic remains,
both signatures are clean, and the `regime_delta` penalty-only clamp is intact.

## The relief branch was far less active than the `eff_thr` drift suggested

I checked which windows it actually fired in rather than inferring from the drift:

| Window set | Windows where it fired | Effect |
|---|---|---|
| Primary | **1 / 20** — W09 Jan-2023 short squeeze (0.3892 → 0.3642) | **+24.06** |
| Holdout | **0 / 20** — never fired | 0.00 |
| Expanded | **1 / 25** — Sep-2023 (0.3712 → 0.3462) | **0.00** |
| **Total** | **2 / 65** | **+24.06** |

The expanded window is worth noting: its threshold *did* move, but **no candidate score fell in
the 0.3462–0.3712 band**, so trades and PnL are bit-identical. I verified this per-window rather
than assuming it from the unchanged total.

So the progressive `eff_thr` drift (0.4507 → 0.3308) I flagged last turn was mostly per-window
recalibration of `calib_thresh` itself, not the accelerator. The accelerator was real but rare.

## FINAL BASELINE — governor disabled, 41.0 bps both sleeves, no ATR floor, zero accelerators

| Window set | Trades | PnL | ROI | Pass |
|---|---|---|---|---|
| Primary (20) | 326 | **+315.90** | +6.32% | 3/20 |
| Holdout (20 random) | 288 | **−88.03** | −1.76% | 1/20 |
| Expanded (25) | 444 | **−2,158.49** | −43.17% | 1/25 |
| **POOLED (65)** | **1,058** | **−1,930.62** | — | **5/65** |

This is the ground truth. Every subsequent claim must beat **−1,930.62 pooled** / **+315.90
primary**, not the +5,553.70 that no longer exists.

---

# PART 2 — Phase 4: targeted triage of the 883-paper corpus

## Method

The corpus is **2.2 GB across 897 files** on `origin/main` (commit `453ff9b`), which is too
large to merge into this branch without breaching the artifact budget, so I extracted
individual PDFs from the git object store on demand rather than checking them out.

`papers/FULL_883_PAPERS_ANALYSIS.json` carries title, abstract, domain, crypto-relevance and
page count for all **883** papers. I scored every one against the four focus areas
(maker-rebate 3.0, adverse-selection 3.0, execution-cost 2.5, microstructure 1.5), weighted by
crypto relevance. **552 of 883** touch at least one. Then I extracted and read the top unique
hits in full.

**Caution on the corpus metadata:** the per-paper `actionable_strategy` field is
auto-generated boilerplate. The identical string *"Asymmetric Spread Quoting: Avellaneda-Stoikov
inventory skew to capture maker rebate and eliminate 41 bps friction"* is attached to *Illiquid
Bitcoin Options*, *Deep Learning for Digital Asset Limit Order Books*, and *How informative is
the Order Book Beyond the Best* — three unrelated papers. **It carries no information and must
not be cited as a finding.** Everything below comes from reading the PDFs.

## The papers that matter

| Paper | What it actually establishes |
|---|---|
| **Rajendran & Singaravelu (2026), ssrn-6344338** | LightGBM toxicity classifier, 31.08M second-level BTC/USDT Bybit observations, Feb-2025→Feb-2026, walk-forward. 21 features / 6 groups. Mean daily ROC-AUC **0.799**. TailScore gate cuts CVaR₉₉ by 2.33%, **25.85× better than random gating**. |
| **Tiniç, Sensoy, Akyildirim, Corbet (2022), ssrn-4175306** | Adverse selection component of the effective spread ≈ **10% of the effective spread** in crypto. Adverse selection costs predict intraday volatility, liquidity, toxicity and returns. |
| **Lim (2026), ssrn-6891658** | Bybit BTCUSDT, 50-level book, 7.16M sub-fills → 14,704 parent orders, across a 9% cascade + 4 stress events. **Displayed depth is a biased proxy for executable liquidity precisely when execution risk is greatest**; hidden depth ratio is *larger* during cascades. |
| **Nguyen & Bui (2025), ssrn-6280958** | Delta-neutral grid MM, Gate.io tick data, 52 days. Maker −0.025% / taker 0.075%. **P&L attribution: spread+grid 76%, funding 18%, maker rebate only 6%.** |
| **Tripathi (2026), ssrn-6444878** | Dynamic transaction-cost modelling: **penalises execution friction at 3× baseline during high-volatility expansions**. BTC trend performance robust to stressed costs (p=0.195); traditional assets degrade (p<0.001). |

---

## Answer to the question: can we go from Taker to Maker and reclaim 41 bps?

**No. The arithmetic does not permit it.**

Our own knowledge bank decomposes the 41 bps at
`COMPREHENSIVE_QUANT_RESEARCH_PAPERS_KNOWLEDGE_BANK.md:305`:

| Component | Round-trip |
|---|---|
| Exchange fee | **16 bps** (8 per leg) |
| Slippage / market impact | **25 bps** |
| **Total** | **41 bps** |

Only the **16 bps fee component** is addressable by becoming a maker. The other **25 bps is
market impact**, and a passive limit order does not eliminate impact — it **converts it into
adverse selection**. You stop paying the spread and start getting filled preferentially when
price moves against you. Tiniç et al. measure that cost directly: ~10% of the effective spread.

Three independent confirmations:

1. **The corpus contradicts its own headline.** The knowledge bank's banner says
   *"Predictive Post-Only Maker Limit Quoting Algorithm (Reclaiming 41 bps Taker Drag)"* (line
   29) and its table claims *"0.0 bps (Pure Mid/Spread Fill)"* with *"+46.0 bps total alpha
   reclaim"* and a *"+165.44% Net ROI Swing."* But its **own** fee row says the saving is
   **+16 bps**. A model that books zero slippage *and* negative slippage while paying nothing
   for adverse selection is the free-maker-fill fallacy — the same class of fantasy we just
   spent two phases removing.
2. **The one paper that actually harvests rebates says the rebate is trivial.** Nguyen & Bui
   run a purpose-built maker system on real tick data and attribute **6% of P&L** to the maker
   rebate. Spread capture (76%) is the edge, and spread capture requires carrying inventory —
   a different strategy from directional breakout trading, not an overlay on ours.
3. **Rebates require volume tiers we do not have.** The −0.025% maker rate is explicitly
   "consistent with high-volume maker tiers." At base tier, maker is a *reduced fee*, not a
   rebate.

**Verdict: reject.** The maximum honest recovery is 16 bps round-trip (39% of 41), it demands
tick + LOB data we do not hold, and it requires becoming an inventory-carrying market maker.

## The adverse-selection predictor: partially implementable, and the literature confirms our VPIN falsification

Rajendran & Singaravelu is the most directly relevant paper in the corpus. Mapping its 21
features against our 58 actual columns:

| Feature group | Features | Available to us? |
|---|---|---|
| Spread state (`ob_spread*`, `ob_thin_book_flag`) | 4 | **NO** — no bid/ask/spread column |
| Order flow imbalance (`ob_imbalance_l1`, `ob_ofi_proxy`, `ob_ofi_z_30`) | 3 | **NO** — needs L1 quote quantities + add/cancel events. Our CVD and taker buy/sell are *trade* imbalance, not *quote* imbalance |
| Passive retreat (`ob_net_passive_z_30`, `ob_upd_imb`) | 2 | **NO** — needs order add/cancel events |
| Volatility (`ob_rv_30`, `ob_impact_pressure`) | 2 | **PARTIAL** — rv yes at 15m; impact_pressure needs spread |
| Trade flow (`tr_*`) | 7 | **~5** — volume/count imbalance, flow autocorr, rv, volume-z. Not tick imbalance |
| Activity (`tr_log_volume`, `tr_log_trade_count`, `tr_no_trade_flag`) | 3 | **YES** |

**~8–9 of 21 features are buildable, and the three highest-information groups are entirely
absent.** Resolution also differs: they work at 1 second, we have 15-minute bars.

**Most importantly, their ablation independently vindicates our VPIN finding.** Under identical
conditions their full classifier reaches **2.11×** efficiency while **the VPIN proxy reaches
0.30× — below the random benchmark.** Last turn I falsified VPIN on our own data (never reaches
0.80; below-median before all three cascades; inverse-signed). A 2026 paper on 31M
second-level observations reached the same conclusion by a different route. That is now a
settled result, not a quirk of our aggregation.

Note also their headline honesty: at the 0.1% gate, **precision is 6.07% and recall 1.99%**
(F1 = 0.030). The value is in tail concentration, not in classifying toxic seconds accurately.

---

## What I recommend instead

### 4A — Regime-dependent execution cost stress *(recommended, implementable now)*

We currently charge a **static 41 bps in every regime**. Tripathi stresses friction at **3×
baseline during high-volatility expansions**; Lim shows displayed-liquidity proxies are most
biased during cascades. Both point the same way: our cost model is too optimistic exactly where
the system takes the most damage.

```python
# Engine/execution_costs.py
def round_trip_bps(vol_regime_multiplier: float) -> float:
    """Stress the base cost by realised-vol regime. Defensive-only: multiplier >= 1.0."""
    return ROUND_TRIP_BPS * max(1.0, float(vol_regime_multiplier))
```

Multiplier driven by the **same** rolling-365d BTC volatility rank the governor already
computes — no new data, no lookahead, and **penalty-only**, consistent with the standing
defensive-only constraint. This will lower the baseline further. That is the point: we would
rather know the honest number now than discover it in live capital.

### 4B — Adopt the TailScore/CVaR evaluation architecture *(recommended, methodological)*

Rajendran & Singaravelu's real contribution is not their features — it is their **evaluation
metric**. They do not judge a gate by PnL. They judge it by **CVaR₉₉ reduction versus an
equal-sized random gate**, reporting an efficiency ratio. That is exactly the discipline we
lack: three Phase-1 mechanisms each produced a plausible positive PnL that turned out to be an
artefact. A CVaR-efficiency benchmark against random gating cannot be gamed by tuning, because
the control is generated from the same distribution.

Proposal: build `scratch/cvar_gate_harness.py` that scores any proposed entry veto by
CVaR₉₉ efficiency vs random, episode-clustered, before any PnL is ever looked at.

### 4C — Reject the maker transition

For the reasons above. If it is ever revisited it needs millisecond tick + 50-level book data
and a fill model with explicit adverse selection — a new data pipeline, not a code change.

---

## Validation methodology for 4A

1. **Defensive invariant.** Unit-test `max(1.0, ...)` over 20,000 random multipliers: the
   function must never return below `ROUND_TRIP_BPS`. (Same pattern as the governor's
   min-delta test, which passed 20,000/20,000.)
2. **Control invariance.** With the multiplier pinned to 1.0 the three sets must reproduce
   **+315.90 / −88.03 / −2,158.49** exactly.
3. **Pre-register the schedule before running.** E.g. rank ≥ 0.88 → 3.0×, ≥ 0.70 → 1.5×, else
   1.0×. Written down first, then measured once. No selection by outcome.
4. **Episode-clustered reporting.** Any volatility-ranked statistic produces autocorrelated
   activations. Report n as independent episodes with a 2-month gap, as we did for the governor
   (n=6, not 9).
5. **All three window sets**, and the honest expectation is that every total goes **down**.

## What I have *not* verified

- I read 9 of the 883 PDFs in full plus titles/abstracts for all 883. The four focus areas
  surfaced 552 candidates; I ranked them and read the top tier. A deeper sweep may surface
  more, but nothing in the top 30 changes the maker-rebate arithmetic, which is a data-
  availability and fee-structure constraint rather than a literature gap.
- Nguyen & Bui's Sharpe > 3.0 is a 52-day backtest by a commercial research firm on its own
  simulation. I have not validated it and would not treat it as evidence.
- I have not verified Binance's current published fee tiers; the −0.025% / 0.075% figures are
  the paper's assumption, quoted as such.
