# Master plan: seven SMC playbook families, individual assets, causal evaluation

Prepared 2026-09-07 for C:/Users/SIGMA/Documents/Trading.

**Status: implementation blueprint, gated by the unresolved data findings in the [forensic report](C:/Users/SIGMA/Documents/Trading/docs/reviews/data-provenance-forensic-report.md). No strategy performance is certified.**

The current user instruction supersedes the earlier shared-portfolio proposal. Every experiment, wallet, exposure limit, optimization record and score is per asset. Cross-asset portfolios remain out of scope until individual acceptance is established.

## 1. Define what can be certified

There are seven requested families: Mayne, Marco, Kane, Edgeful, Usman Noah, Marci, and S1/S2 confluence/ML. With 18 assets this is 126 family–asset tracks. Because S1 and S2 are separate implementations, retaining both produces 144 implementation–asset tracks. Keep their scores separate; do not choose the winning variant after inspecting OOS.

Two limits must remain visible.

First, all 18 assets cannot pass the original 2021–2026 calendar windows individually. APTUSDT perpetuals launched on 2022-10-19, after the early windows, as documented by [Binance's launch announcement](https://www.binance.com/en/support/announcement/detail/f9df5bba5e1c4f1e9289240d0f9344e2). Binance's [ARB announcement](https://www.binance.com/en/square/post/334762) likewise places its launch in March 2023. Local schema also lists SUI in May 2023 and OP in June 2022; confirm exact first-trade timestamps from source data before admission. Pre-listing periods cannot contain genuine trades.

Preserve the original 20 windows and report NOT_LISTED/INSUFFICIENT_HISTORY explicitly. Do not fabricate bars, silently drop windows, or call a smaller denominator 20/20. If the user later authorizes a revised objective, alternatives are 20 predetermined post-listing windows per asset or a common later calendar. Neither is a pass of the original calendar.

Second, repeatedly retuning after seeing a failed OOS window turns that window into development evidence. Fitting only on preceding IS prevents direct future-row training but does not remove researcher selection from retries. Scikit-learn's [cross-validation guidance](https://scikit-learn.org/stable/modules/cross_validation) explains this distinction between model selection and test evaluation. Keep the requested fail-fast development loop, record every attempt, then freeze the final procedure for untouched or prospective validation.

## 2. Freeze the numerical and temporal contract

Write one validated configuration consumed by labels, simulation, scoring and reports. Pin its hash before running a track.

| Contract | Required behavior |
|---|---|
| Account | Independent $5,000 account per asset/implementation/window; no transfers or cross-asset netting. |
| Base risk | $25. Preserve a fixed-risk baseline; any historical $50 house-money/$15 defense policy is a separately declared fixed policy, never a rescue selected after OOS loss. |
| Target | Exactly 2.5 initial stop-distance R from the actual filled entry. No 3R/5R variants or target inflation. |
| BE ratchet | Once +0.8R has been observed, arm stop at entry +0.15R for a long, mirrored for a short. |
| Profit ratchet | Once +1.5R has been observed, arm stop at entry +0.80R, mirrored for a short. |
| Ratchet timing | A stop level inferred from bar t becomes effective only on the next bar. |
| Decay | Planning assumption pending the user's optional clarification: preserve the earlier conditional rule, close after 24 bars if maximum favorable excursion has never reached +0.2R. An unconditional 24-bar cap is a different rule and must be explicit. |
| Entry timing | Features available at bar close; place the order for the next executable open with 10 bps adverse entry slippage. Reject invalid geometry after a gap. |
| Fees and exits | 8 bps taker fee on each fill; 15 bps adverse stop slippage. Explicitly specify market decay/terminal-fill slippage and target order type. Do not silently grant a taker zero-slippage market exit. |
| Risk control | 4.5%/$225 budget based on initial capital as previously requested; also report peak-to-trough DD. Reserve cost-aware loss capacity before entry and act on open-exposure breaches. |
| Pass | Retain the stricter established criteria: ROI >20%, MaxDD <5%, WR >40%, closed trades >=6. The latest '<20/<40' fail wording differs at equality; do not promote exact-boundary cases without resolving that contract. |
| Window | UTC [start, midnight after end date); include the final day's 96 bars. |
| IS boundary | All fitting/calibration strictly before OOS start minus 72 hours; included labels must finish before their allowed training cutoff. |
| Warm-up | Load only prior feature/state history; no cash or positions carried into the independent window unless explicitly part of the frozen contract. |
| Reporting | Full closed-window net PnL, settlement costs, realized funding, and marked exposure; never stop early at +20% to lock a pass. |

Price-distance R and net dollar-risk R are different after friction. Store both initial_stop_distance and all_in_risk_dollars. Calculate target/ratchets in the former and position sizing/performance in the latter. A stop budget is not a guaranteed maximum loss through price gaps; report actual overshoots.

## 3. Phase A — certify the data before optimizing

A1. Freeze a manifest inventory of all named contracts, exact listing timestamps, raw source dates and current download paths. The present folder has only 11 masters. Locate or reconstruct missing SOL/AVAX/NEAR history and post-listing SUI/APT/OP/ARB history; never synthesize pre-listing prices.

A2. Preserve source evidence: source URLs/content hashes, download time, exchange event time, publication/availability assumptions, raw and derived schema versions, dependency versions and model training lineage. Store data generation identifiers in each evaluation.

A3. Repair the confirmed USDC end-date dependency. Keep USDT OI separate from optional aggregate OI. Add a regression that extending a request cannot change any common historical record.

A4. Separate causal availability from retrospective quality. Export spot source, synthetic-bar flags, per-metric age and actual knowledge time. Do not use a full-run stale-data flag for historical trading decisions.

A5. Fix the empty-metrics crash, eliminate unflagged blanket zero fill, implement field-specific freshness and missing-data policies, and recompute affected indicators. Ensure manifest coverage counts come from observed source flags.

A6. Resolve liquidation-model lineage. Recover the calibration data and as-of artifacts or replace the signal input with an explicitly identified, causally constructed research proxy. Rebuild all dependent liquidation scores. A global 2026-trained generator cannot certify 2021 features.

A7. Run the deterministic causality suite: full/prefix equality, future suffix perturbation, day/month boundaries, missing/recovered streams, duplicate observations, timestamp units, funding events and upstream model changes.

A8. Verify raw sample reproduction and full rung/master volume conservation. Numerical integrity, available history, causal inputs and provenance must all pass. Write an immutable data certificate describing the exact scope and remaining limitations.

Exit gate: no unresolved blocker affecting data consumed by the strategy. If this gate fails, the track is DATA_BLOCKED, not STRATEGY_FAILED.

## 4. Phase B — repair the simulation contract

B1. Centralize settlement and risk arithmetic in one reusable engine routine. Keep playbook signal logic in its existing strategy file; avoid copied execution implementations and new v2 variants. One tested execution kernel must also produce labels.

B2. Repair long time-decay PnL before evaluating anything. Seven implementations reset direction before using it. Preserve side, quantity, entry, stop, fees and funding until settlement is complete.

B3. Queue signals at close and execute at next open. Define gaps beyond planned stops/targets, exchange tick/quantity steps, minimum notional, and maximum permissible leverage. At t+1 use t's known ATR/structural levels, not ATR recomputed from t+1 high/low.

B4. Size from all-in expected stop loss, including entry and stop fees and adverse slippage. Debit entry fees immediately; account for settled funding and open liquidation costs. Do not award the same nominal risk to structurally different losses.

B5. Enforce hard drawdown handling on existing exposure as well as new entry admission. If OHLC ordering is ambiguous, use a documented conservative stop-first path or finer execution data. Close-only equity is insufficient evidence for an intrabar drawdown bound.

B6. Set exact target and ratchet geometry in every playbook. Fix Marci's stop-distance denominator mismatch, Kane's variable target and Usman's 3R target. Remove Marco's extra ratchet offsets if the fixed price-level invariant is retained.

B7. Advance structure state every market bar, even during an open position: pivot confirmation, pool/FVG age, invalidation, session extremes and sweep timers. Current FVG/pool updates inside the flat-position branch can freeze their clocks.

B8. Warm indicators/structure from preceding bars without allowing pre-window entries. Reset cash and trade state at the window boundary. Define window-end forced settlement and cancellation of pending entries.

B9. Produce a chronological event ledger: signal, rejection, pending order, fill, risk change, ratchet armed/effective, funding, exit and equity mark. Reconcile final equity to all ledger cashflows.

Exit gate: the focused execution test matrix in section 11 passes for long and short paths. No optimization is allowed to compensate for a broken ledger.

## 5. Phase C — playbook fidelity and specific repairs

The current files are simplified numerical proxies. The original playbook PDFs are shown as deleted in the working tree. Do not claim exact author/playbook fidelity until the authoritative material is recovered or the user approves the numerical specification. Preserve unrelated user changes.

### Mayne — sweep, higher-timeframe context, reclaim/breaker

Current code: rolling four-bar liquidation spike, flow/RSI/VWAP confluence, and close relative to EMA800 ([smc_mayne.py:160](C:/Users/SIGMA/Documents/Trading/Engine/strategy/smc_mayne.py:160)). It does not explicitly model a breaker block despite its header.

Define a causal sequence of confirmed HTF point of interest, liquidity sweep, reclaim, optional breaker confirmation and next-bar entry. Use completed HTF candles; an EMA800 on 15m bars is a trend proxy, not automatically the original HTF structure.

Candidate parameters may include sweep-recency, structural stop buffer and trend-strength threshold, within a small predetermined IS-only range. Keep 2.5R and the ratchets invariant. Reuse the existing cost-aware sizing formula only after independent long/short tests.

Measure funnel losses at sweep, trend alignment, reclaim, model approval and execution. Verify an HTF reversal late in a candle cannot change an earlier lower-timeframe signal.

### Marco — liquidity pools and sweep traps

Current pivot code compares high/low at t-3 against observations around t-10 ([smc_marco.py:156](C:/Users/SIGMA/Documents/Trading/Engine/strategy/smc_marco.py:156)), rather than a coherent symmetric pivot neighborhood.

Define pivot width and the confirmation delay explicitly. Register a pool only at confirmation time; optionally cluster nearby confirmed levels with an ATR-scaled tolerance. Age and invalidate pools on every bar. Separate pool consumption by market mitigation from rejection by the ML filter.

Require sweep beyond a preexisting pool followed by close reclaim; execution occurs later. Tune confirmation width, pool age and sweep buffer only within IS. Verify no pool exists before its confirmation and appending bars does not move past pool events. Standardize Marco's extra friction-adjusted ratchet levels to the shared invariant.

### Kane — accumulation, manipulation, distribution

Current code computes an accumulation range but its trigger is a local pinbar/sweep; the range does not constrain entry. Targets are variable with a 2R minimum ([smc_kane.py:146](C:/Users/SIGMA/Documents/Trading/Engine/strategy/smc_kane.py:146)).

Define accumulation using completed prior bars, then a subsequent range sweep, return/reclaim and distribution confirmation. Use separate state timestamps so an entire narrative cannot be inferred retrospectively from one candle. Place a structural stop outside the manipulation extreme plus a predeclared buffer; set exactly 2.5R from the filled entry.

Tune accumulation duration, normalized range width, sweep penetration and setup expiry in training only. Tests must prove no entry without prior accumulation and no target based on future distribution extremes.

### Edgeful — displacement FVG and later mitigation

Current code creates an FVG at t and evaluates it for mitigation at that same t. For a new bullish FVG, low[t] equals its stored top, so the touch condition is automatically satisfied ([smc_edgeful.py:145](C:/Users/SIGMA/Documents/Trading/Engine/strategy/smc_edgeful.py:145)).

Require formation_time < mitigation_time. Record displacement size, gap width, direction, creation time and invalidation level. Advance gap age every bar; permit only the defined retest/mitigation policy. Use signed directional confirmation consistently instead of the same zc_div inequality on both sides by accident.

Tune gap width relative to ATR, displacement, gap age and retest depth in IS. Tests must exclude same-formation-bar entries, stale gaps, repeated consumed gaps and favorable fills through invalidation.

### Usman Noah — prior-day sweep, engulfing FVG, mitigation

Current code approximates prior-day high/low sweeps with an engulfing FVG and later mitigation. It initializes day extremes while skipping the first two loop bars, ages gaps only while flat, and targets 3R ([smc_usman_noah.py:67](C:/Users/SIGMA/Documents/Trading/Engine/strategy/smc_usman_noah.py:67), [:227](C:/Users/SIGMA/Documents/Trading/Engine/strategy/smc_usman_noah.py:227)).

Seed complete prior UTC-day highs/lows from warm-up. Record sweep time, later engulfing displacement, confirmed FVG and subsequent mitigation separately. Decide whether reclaim is mandatory; a mere breach is not automatically absorption.

Set 2.5R and common settlement. Tune sweep validity duration, engulfing/displacement strength, FVG expiry and stop buffer in IS. Test midnight resets, partial first days, sweep expiry during a position, and both directions.

### Marci — trend, pullback, confirmed fractal, continuation

Current code uses EMA200 slope, Bollinger pullback, a confirmed three-bar fractal and momentum break ([smc_marci.py:156](C:/Users/SIGMA/Documents/Trading/Engine/strategy/smc_marci.py:156)). This is a trendline-break proxy, not a reconstructed trendline.

Fix risk geometry first: the stop adds an ATR buffer after r_ is calculated. Compute r_ from the final actual stop and entry; use it for quantity, 2.5R target and both ratchets.

Warm Bollinger state from preceding history. Keep confirmed fractal timing explicit and evaluate trend slope in normalized units. Tune pullback depth, normalized slope, confirmation strength and stop buffer inside IS. Check mirrored directional confluence and that every target is exactly 2.5 times initial stop distance.

### S1/S2 — liquidation confluence and meta-labeling

S1 currently uses liquidation Z >1.2 and candle direction; S2 uses the strict six-condition confluence ([s1_liquidation_cascade.py:169](C:/Users/SIGMA/Documents/Trading/Engine/strategy/s1_liquidation_cascade.py:169)). They are not interchangeable versions of the same entry population.

Retain the mandatory six-condition rule as the reference S2 baseline. Separate any relaxed event generator as its own declared S1 research specification; do not silently relax invariants to increase trades. Complete upstream liquidation provenance before either is eligible.

Train on the actual events each implementation can trade. Replace the current current-open/5-ATR label with realized net outcome from the common 2.5R kernel. Drop censored observations. Compare the unfiltered baseline, a simple interpretable filter and a regularized shallow model using purged IS validation.

Record how many strict signals exist before filtering. A filter cannot create additional opportunities, and selecting 5% of all bars does not guarantee selecting any confluence bars.

## 6. Phase D — chronological ML and regime research

D1. Build event records containing asset, playbook, signal/availability/entry time, direction, immutable features, stop geometry, label completion time and net execution outcome.

D2. Use expanding or rolling chronological IS folds with a time-based 72-hour separation. Also remove overlapping event outcome intervals. A row-count gap alone is insufficient when bars or candidate events are irregular.

D3. Fit preprocessing, feature selection, regime transforms, models and calibrators inside each fold. Generate out-of-fold training predictions; never calibrate using in-sample fitted scores or OOS distributions. This follows the train/test separation described in [scikit-learn's leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html).

D4. Start with no-ML, then regularized logistic or shallow gradient-boosted filters. Retain the router's depth <=4 and L1/L2 constraints for tree experiments. Class weighting is an objective choice, not proof of calibrated winning probability.

D5. Use candidate-conditioned net expectancy or net-positive classification with calibrated expected gain/loss estimates. Assess PR curves, calibration, Brier/log loss and net trade metrics. Brier score alone is not a profitability criterion.

D6. Candidate features: normalized spot/futures delta, raw divergence plus explicitly named normalized versions, ATR/price, trailing volatility, normalized trend slope, price/VWAP distance, structure geometry, and point-in-time available OI/funding. No raw timestamp/window identity, retrospective event description or month-specific lookup table.

D7. Prefer observable trailing regime descriptors first: trend strength, volatility percentile against prior history and compression. If clustering is tested, fit centroids only inside training, assign forward without refitting on OOS, and prove prefix stability. Never use future HMM smoothing or retrospectively named bull/crash regimes as predictors.

D8. Use a small predeclared parameter/search budget per family, fixed seeds and deterministic tie-breaking. Begin with coarse structural choices, then a small local robustness check. Log every candidate, including failures; do not escalate to unbounded sweeps after each OOS miss.

D9. Select using IS validation expectancy, drawdown, trade support and parameter stability together. Reject isolated optima that vanish with small neighboring parameter changes. A model is admitted only when its intended improvement survives the fixed validation protocol.

D10. Freeze the entire selection procedure. Per-window fitted weights may change under that procedure; manual window-specific rules may not. Keep each asset's data independent at this stage.

## 7. Phase E — opportunity and feasibility gates

Before expensive fitting, count eligible events and executable opportunities on training validation. Project whether the fixed risk and capped target can support the requested ROI without treating an OOS maximum-profit path as a tradable policy.

At $25 risk, a 20% return on $5,000 requires more than 40 net R. Even 16 perfect 2.5R trades only reach 20% gross before friction; exceeding 20% requires at least 17 such winners under capped target fills, and more with costs, losses and early exits.

The earlier fresh ETH scan found only six raw strict-confluence candidates in February 2025. On the current uncorrected features, six capped full-target wins at $25 yield at most $375 gross (7.5%); even $50 each gives $750 (15%). This is a diagnostic upper bound for that fixed candidate set, not a valid strategy result or proof about causally rebuilt features.

If opportunities are insufficient, mark the specific constraint conflict. Do not solve it by increasing risk beyond the fixed contract, fabricating signals, silently altering alpha thresholds, excluding hard windows or changing 2.5R. Any revised entry definition must be a documented research variant evaluated independently.

## 8. Phase F — fail-fast walk-forward protocol

For each asset and each declared implementation:

1. Preflight all 20 windows for listing/coverage and valid IS availability. Preserve every window in the report, including unavailable ones.
2. Load the frozen data/config/code provenance. Reject a mixed or uncertified dataset.
3. At window k, form the pre-k IS dataset ending before start_k minus 72 hours and admit only fully resolved labels.
4. Run the predefined IS-only selection and calibration protocol. If no model/candidate qualifies, record NO_VALID_IS_MODEL; do not lower the threshold using test predictions.
5. Freeze the selected artifact and record its cutoff/hash before opening OOS.
6. Run the complete OOS interval with fixed causal inference and identical execution rules.
7. Reconcile net PnL, funding, fees, drawdown and closed-trade counts. Evaluate all strict criteria.
8. If any criterion fails, mark FAIL and immediately halt that implementation–asset track. Never advance it to k+1. Other independent asset tracks may be scheduled only under the same declared policy.
9. Investigate failures from the event funnel and existing correctness evidence. Re-optimization uses preceding IS only, as requested. Retried OOS is explicitly a DEVELOPMENT_REPLAY, with full attempt history.
10. After a change, replay earlier windows as regression checks under the same causal procedure. These checks do not restore their untouched status.
11. A fresh certification run starts from the first applicable original window with one frozen procedure and no discretionary retries inside the run.
12. Claim independent generalization only on untouched/prospective data reserved after development. Keep that claim separate from a 20-window historical development score.

Suggested state machine: DATA_BLOCKED / NOT_LISTED / INSUFFICIENT_HISTORY / READY / IS_REJECTED / OOS_RUNNING / FAIL / DEVELOPMENT_REPLAY / PASS. Never map unavailable, failed or unrun to PASS.

The original window descriptions contain retrospective regime narratives. Retain names for reporting only; they are prohibited inputs to fitting, routing or threshold selection.

## 9. Phase G — failure diagnosis and controlled iteration

| Observed problem | First investigation | Permitted response |
|---|---|---|
| Zero raw signals | Units, source availability, state transitions, confirmation delays | Repair contracts/bugs; change entry rules only as declared research. |
| Raw signals but zero model approvals | Candidate-population mismatch, calibration, train score distribution | Rebuild aligned labels/calibration inside IS. |
| Too few closed trades | Overlapping setups, stale state, terminal settlement, genuine scarcity | Repair state/accounting; report feasibility if scarcity persists. |
| High win rate but weak ROI | Net R distribution, friction/stop ratio, many small ratchet exits | Diagnose IS expectancy; preserve fixed target/locks. |
| Low win rate | Invalid setup sequencing, noisy proxies, direction errors | Repair specifications, then IS-only filter comparison. |
| Drawdown breach | Position sizing, gaps, simultaneous exposure, risk budget | Correct execution/governor; do not clamp losses. |
| Performance disappears after costs | Stop too narrow relative to fees/slippage | Cost-aware admission and structural-risk specification. |
| One failed month after many retries | Selection overfit or regime dependence | Stop retry escalation; retain failures and validate on new data. |
| Sudden feature distribution shift | Source/model/venue change or imputation transition | Repair provenance; never infer a regime label from future outcomes. |

## 10. Run artifacts and reproducibility

For each run, record:
- Source commit or exact source hashes including dirty files; Python/library versions and seeds.
- Dataset generation/hash manifest, actual coverage, listing timestamps and quality-policy version.
- Upstream liquidation model hashes/cutoffs, downstream model/calibrator hashes/cutoffs and label specification.
- IS/validation/OOS bounds, embargo/purge rules, event-overlap exclusions and warm-up spans.
- Candidate count at every filter, rejected-entry reasons, risk denials, execution ledger, marked-equity curve and all exits.
- Fees, slippage, funding, notional/leverage, exact R geometry and drawdown overshoots.
- Attempt number, prior failures, classification as first OOS evaluation or development replay, and per-criterion pass results.

Cache only by these complete dependencies. A source/stop/friction/data change invalidates affected labels and trade caches. Saved reports are evidence records, never substitutes for fresh execution of a claimed pass.

## 11. Verification matrix

| Layer | Required cases |
|---|---|
| Data time | Future suffix mutation; split at day/month boundary; incomplete last candle; source timestamp later than decision. |
| Missing data | Initial absence, interior gap, long outage, recovery, empty metrics; no future fill; source flags retained. |
| Model lineage | Future-trained upstream artifact rejected; wrong hash/schema rejected; ML fallback explicitly versioned. |
| Flow | Buy/sell conservation, spot/futures units, daily resets, exported lifetime reanchoring, missing spot sentinel. |
| Setup state | Confirmed pivots only, no FVG mitigation on creation bar, age advances during positions, prior-day warm-up. |
| Entry | Next-open execution, gap-invalidated setup, quantity/tick precision, insufficient capital/margin. |
| Exit | Long/short stops, target, gap-through-stop, simultaneous touch, conditional/unconditional decay contract. |
| Ratchets | Just below/at each trigger, activation one bar later, both directions, no favorable same-bar stop. |
| Accounting | Entry/exit fees, adverse slippage, funding timestamps, terminal position, exact ledger reconciliation. |
| Risk | Cost-aware sizing, budget admission, drawdown while open, realized overshoot, no early profit lock of a window. |
| Learning | Unresolved labels excluded, 72-hour chronological purge, validation-only calibration, no test percentile. |
| Reporting | All 20 windows retained; strict equality boundaries; first-failure halt; missing asset not counted as pass. |

These are behavioral tests, not assertions that merely mirror the implementation. Validate the corrected pipeline on a small deterministic fixture, then a representative historical slice, then the complete certified asset data. Only expand tests when unresolved findings justify it.

## 12. Work order and completion criteria

Milestone 1: close data blockers and publish the revised provenance certificate. Deliver regenerated versioned data, not overwritten historical evidence.

Milestone 2: close execution/risk defects across existing strategy files with the shared tested contract.

Milestone 3: sign off explicit numerical definitions for all seven families and establish per-asset no-ML baselines.

Milestone 4: add aligned labels, training-only validation/calibration and tightly bounded model comparisons.

Milestone 5: run the fail-fast development tracks, retaining every failed attempt and unavailable window.

Milestone 6: freeze candidates and run independent validation. Individual acceptance precedes any portfolio investigation.

Completion means the requested metrics are actually measured from the declared causal data and execution contract, with no missing or relabeled windows. If a track cannot meet them, the deliverable is its verified failure and specific constraint diagnosis. No architecture or optimizer can honestly guarantee that every asset has the required opportunity in every month.

