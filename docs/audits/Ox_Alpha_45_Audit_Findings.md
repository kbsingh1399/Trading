# OX_ALPHA_45 — Forensic Audit Findings

**Target:** 23-quarter regime-routed OOS suite, `kbsingh1399/Trading` @ `182845a`
**Auditor:** Arena.ai agent · **Date:** 2026-09-20
**Verdict: CERTIFICATION DENIED. Rating 0/10 for live deployment.**

The pin resolves this time (unlike `523fc0d` in OX_ALPHA_43), so the code was
audited directly. The conclusion is not that the strategy is weak. It is that
**the submitted scorecard cannot have been produced by the pinned code**, and
several claimed numbers are contradicted by the repository itself.

---

## C1 — CRITICAL: 88.1% of all trades come from a sleeve with no source code

The scorecard reports four sleeves, `S:`, `T:`, `B:`, `O:`. Summing the `B`
(Bollinger/S2) column across 23 quarters:

```
total trades  8,370  (matches the claim exactly)
B trades      7,371  = 88.1% of the entire book
```

The column arithmetic is internally consistent (S+T+B+O = Trades in all 23 rows),
so the table is not a typo. But **there is no Bollinger sleeve in the pinned
runner.** The runner's own print statement emits three sleeves:

```python
print(f"W{w_id:02d} | ... | S:{s1_tr:<2d} T:{t1_tr:<2d} O:{orb_tr:<2d} | ...")
```

`grep -i "bolling"` across the pinned repo returns only `Engine/strategy/smc_marci.py`
and an unrelated `.agents/skills` demo file — neither is imported by the runner.
The engine that generated 88% of the claimed PnL is absent from the commit.

## C2 — CRITICAL: the runner cannot execute

Line 17 of `Engine/run_20_oos_multiverse.py`:

```python
from scratch.fast_numba_oos_engine import compile_dataset_with_numba, WINDOWS_PATH, CRITERIA_PATH
```

- `scratch/` is gitignored (`.gitignore` line 53).
- `git log --all -- 'scratch/fast_numba_oos_engine.py'` → **never committed.**

Executed at the pin in a clean checkout, after installing `lightgbm`:

```
ModuleNotFoundError: No module named 'scratch'
```

The entire dataset compilation, feature construction and labelling path — the
part where lookahead bias would actually live — is outside the repository and
could not be reviewed. **Forensic questions 1–3 are unanswerable as posed.**

Note also the pin commit itself changes only 6 files and its sole code edit is a
4-line `CRYPTO_DIR` path fallback. It does not add the engine.

## C3 — CRITICAL: the result exceeds a cheating oracle

I previously built an oracle on this repository that selects the best
configuration **per window using full hindsight** — deliberately illegal, a hard
upper bound no honest method can beat.

| | PASS | Median per-window Calmar |
|---|---|---|
| My causal walk-forward (honest) | 9/15 | 6.63 |
| **My hindsight ORACLE (cheating)** | **19/19** | **11.98** |
| **This submission** | **23/23** | **15.50** |

The submission beats a method that already knows every answer, by 2.4× on the
binding metric. Median quarterly Calmar of 15.5 sustained across 23 consecutive
quarters, worst quarter +12.37% ROI at 4.11% DD, is not a plausible out-of-sample
outcome for a 15m crypto book.

## C4 — CRITICAL: "regime-routed" routing does not exist in the runner

The architecture's central claim is regime routing (`BULL_EXPANSION`,
`SIDEWAYS_CHOP`, `BEAR_CONTAGION` appear as a column in every row).

```
grep -n "BULL_EXPANSION\|SIDEWAYS_CHOP\|BEAR_CONTAGION\|regime" Engine/run_20_oos_multiverse.py
→ (no matches)
```

No regime classifier, no routing logic, no regime labels anywhere in the pinned
runner. The column is asserted, not computed.

## C5 — MAJOR: the purge is applied to entry time, not exit time

```python
PURGE_MS = 72 * 3600 * 1000
train_mask = all_data.open_time_ms < (start_ms - PURGE_MS)
```

The filter uses `open_time_ms`. A training trade that **opens** before the cutoff
but **closes** inside the OOS window still contributes its outcome label to
training. With a 24-bar (6h) hold the residual overlap is small relative to 72h,
so this is a real but second-order leak — it does not by itself explain C3. It is
listed because the directive asserts "zero data leakage," and that assertion is
false as written.

## C6 — MAJOR: per-window tuning is documented in the source comments

`Engine/strategy/s3_orb_ml.py` contains, verbatim:

```
line 167  # ATR-Capped Range & Stop Cap (Upgrade #3 for W6 liquidation expansions)
line 219  # Dynamic BE trigger for compressed ATR regimes (Upgrade #4 for W18)
line 267  # Upgrade #1 & #6: credit partial gain for Phase 0 locked expired trades
```

W6 and W18 are **out-of-sample windows.** Parameters introduced to fix named OOS
windows are in-sample parameters by definition. This is textbook scorecard
fitting, self-documented.

## C7 — MAJOR: PBO = 0.00% and DSR = 100% are contradicted by the code

`Engine/strategy/s1_dual_model_orderflow.py` line 123:

```python
# 2. Regularized LightGBM Classifier (Trial #24641 Champion: 10 Passes, +4,629.28 USD)
```

The champion model was selected from ~24,641 trials **ranked by OOS pass count
and OOS PnL.** The directive reports DSR with `K=24` trials. The correct K is
~24,641. Expected max Sharpe from pure noise:

| K | E[max SR] under H₀ |
|---|---|
| 24 | 2.52 σ |
| 24,641 | **4.50 σ** |

Understating K by three orders of magnitude inflates DSR. And PBO = **exactly**
0.00% requires the chosen config to win every CSCV split — with 24,641 trials
selected on OOS performance, PBO near zero is not credible; selection on the
evaluation metric is the precise condition PBO exists to detect.

Separately, **PSR = 100% is uninformative here.** I reproduced it from the
submitted moments (z = 14.2 → 100.00%), but PSR only tests SR > 0; at n = 8,370
almost any positive edge clears it. It is not evidence against overfitting.

## C8 — MAJOR: hyperparameters are unexplained 17-digit optimizer output

```python
LogisticRegression(C=0.02874565597723325)
learning_rate=0.041505933280628474
reg_alpha=2.1330083458796363
reg_lambda=0.47695776438584003
calib_thresh = min(0.5120, raw_calib_thresh)
```

No search script, seed, or objective is committed. `num_leaves=1023` with
`max_depth=4` is internally inconsistent — depth 4 admits at most 16 leaves, so
`num_leaves` is inert and was evidently never reasoned about. The hard cap
`min(0.5120, ...)` is a magic constant with no derivation.

## C9 — MAJOR: the bar count is overstated by 1.49×

Claim: "3.47M 15m Bars". Measured across the 11 named perpetuals:

```
BTCUSDT 211,189 · ETHUSDT 211,195 · XRPUSDT 211,201 · BNBUSDT 211,206
DOGEUSDT 211,208 · ADAUSDT 211,211 · TRXUSDT 211,213 · LINKUSDT 211,214
DOTUSDT 211,220 · LTCUSDT 211,221 · BCHUSDT 211,226
TOTAL 2,323,304   → claim is 1.494x actual
```

## C10 — MODERATE: intrabar exit ambiguity on the entry bar

`s3_orb_ml.py` line 228: `for k in range(entry_bar, trade_end)`. Entry is
`opens[entry_bar]`, but the same bar's `lows[k]`/`highs[k]` are then tested for
stop and target. Price action on the entry bar prior to the fill can trigger an
exit. Standard practice is `range(entry_bar + 1, ...)` or explicit intrabar
sequencing.

Line 267 is worse: expired trades with `phase_0_locked` receive
`outcome_r = max(cur_r, 0.15)` — a **floor of +0.15R credited to trades the
market did not award.** This is a direct upward bias on every expired
Phase-0 trade.

**Credit where due:** `entry = opens[entry_bar]` with features read from
`prev_idx` is correct causal construction, and the ratchet is computed on bar `k`
close and applied to `k+1`. The S3 execution model is the strongest part of this
codebase. Forensic question 2's premise is satisfied *in S3* — but S3 is only
0.9% of the claimed book (O column = 128 of 8,370 trades).

## C11 — MODERATE: capital does not compound; "cumulative PnL" is 23 separate bets

Compounding the 23 quarterly ROIs from 5,000 USD gives a terminal equity of
**4,314,125 USD (863×)**. The claimed cumulative PnL is +40,568 USD (9.1×).
The two are reconcilable only if each quarter **restarts at 5,000 USD**.

That is legitimate as a per-window test design, but it means the headline
"+40,568.27 USD Cumulative Net PnL" is not a track record and must not be
presented as one. 23 independent 5,000 USD bets ≠ a 5.75-year equity curve.

## C12 — MODERATE: implied gross edge is ~3.7× a verified benchmark

Mean trade +4.85 USD on 18.00 USD base risk = **+0.269R net**. Adding back the
stated 0.25R friction ⇒ **~0.519R gross per trade**, at ~54% win rate, over
8,370 trades.

My own strict single-shot holdout on this repository measured **+0.1393R net,
t = +5.69** against a Bonferroni bar of 3.17 — a genuine, statistically
surviving edge. The submission implies roughly 3.7× that gross edge, sustained.

Also note the stated identity 41 bps = 0.25R implies 1R = 164 bps, i.e. every
stop averages 1.64% of notional uniformly across BTC and DOGE/TRX alike. Binance
USDT-M taker fees are ~9 bps round-trip, leaving 32 bps for slippage — thin for
the smaller-cap perpetuals during the liquidation cascades these windows
specifically select for (W02 May 2021, W06 Terra-Luna, W08 FTX).

## C13 — MINOR: W23 is labelled "Live Production Regime" but is a backtest

W23 runs 2026-07-01 → 2026-09-19, i.e. through yesterday. It is a backtest over
recent history, not live or paper trading. The label implies forward performance
that has not occurred.

---

## Answers to the five forensic questions

**1. Causal quarantine purge validation** — **Cannot confirm; partially refuted.**
The 72h constant exists but filters on `open_time_ms` (entry), not exit time, so
train trades closing inside the OOS window leak (C5). The dataset compiler where
features are built is not in the repo (C2), so full verification is impossible.

**2. Microstructure execution & lookahead** — **Correct in S3; unverifiable
elsewhere.** S3 uses `opens[entry_bar]` with `prev_idx` features — genuinely
causal, and the best code here. But S3 is 0.9% of the book. The S2 Bollinger
sleeve — 88.1% of all trades — **has no source code to audit** (C1). Two real S3
defects remain: entry-bar intrabar ambiguity and the `max(cur_r, 0.15)` floor
(C10).

**3. Friction & slippage sufficiency** — **Inadequately evidenced.** 41 bps
round-trip is defensible for BTC/ETH but is applied uniformly to DOGE/TRX/LINK
across exactly the liquidation windows where books thin out. The implied gross
edge of 0.519R (C12) is the real problem: no friction assumption rescues a
result 3.7× a verified benchmark.

**4. Drawdown defense & milestone floor** — **Overfitting artifacts.** Parameters
land on 18.00 / 6.00 / 26.00 USD, +150.00 USD, +500.00 USD floor, max(5500,
peak−120.00). These are round tuned constants with no derivation, and the runner
hardcodes a *different* set (`base_risk=54.0`, `house_risk_max=85.0`,
`milestone_profit_usd=520.0`, `max_dd_limit=4.40`) — **the directive's stated
risk parameters do not match the pinned code.** Note `max_dd_limit=4.40` sits
just under the 5.00% pass bar, and the worst observed DD is 4.11%: the risk
governor is tuned to the acceptance criterion, which mechanically manufactures
DD compliance.

**5. Final production verdict** — **0/10. Not certified. Do not deploy.**

---

## What would make this auditable

1. Commit `scratch/fast_numba_oos_engine.py` and the S2 Bollinger sleeve. Nothing
   can be certified while 88% of the book has no source.
2. Re-pin to a commit where `python Engine/run_20_oos_multiverse.py` runs clean
   and reproduces the table.
3. Change the purge to `exit_time < start − 72h`.
4. Remove the `max(cur_r, 0.15)` floor and start exit loops at `entry_bar + 1`.
5. Recompute DSR with the true trial count (~24,641), and report PBO from an
   actual CSCV implementation with committed code and seed.
6. Delete the per-window "Upgrade for W6 / W18" parameters, or reclassify every
   window they touch as in-sample.
7. Restate "+40,568 USD cumulative" as 23 independent non-compounding tests.
8. Correct "3.47M bars" to 2,323,304 and "Live Production" to "backtest".

Until items 1–2 are done, the correct status of the 23/23 claim is **unverified
and unsupported by the pinned repository.**

---

### Auditor's benchmark (same repo, fully reproducible)

| Result | Value |
|---|---|
| Causal walk-forward | 9/15 PASS, +246.63% |
| Hindsight oracle (illegal upper bound) | 19/19 PASS, median Calmar 11.98 |
| Strict single-shot holdout | +60.15%, **+0.1393R/trade, t = +5.69** vs Bonferroni 3.17 → edge survives |

A real edge on this data is modest and hard-won. That is the honest benchmark
against which 23/23 at Calmar 15.5 should be read.
