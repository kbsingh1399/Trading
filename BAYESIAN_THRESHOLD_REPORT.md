# Bayesian Adaptive Probability Threshold — OOS Walk-Forward Report

**Branch:** `arena/01a0a5bf-trading` · **Commits:** `0479f52`, `4e20844`, `811e7d7`
**Baseline accepted for this checkout: +5,553.70 USD** (674 trades, 10/20 PASS)

---

## Verdict

Both variants were implemented, verified, and run end-to-end. **Neither beats the baseline,
and the reason is now identified with evidence: the quantity the tracker adapts to has no
predictive content, because the ML model is retrained from scratch every window.**

| Variant | Total PnL | Trades | Pass | vs baseline |
|---|---|---|---|---|
| Unpatched baseline | +5,553.70 | 674 | 10/20 | — |
| v1: cumulative posterior + relief branch | +5,168.48 | 659 | 10/20 | **−385.22** |
| v2: decaying (d=0.98), penalty-only | +5,397.98 | 624 | 10/20 | **−155.72** |

v2 is a real improvement over v1 (+229.50) — removing the relief branch and adding decay both
helped, exactly as predicted. But it still loses to baseline.

---

## Decay-factor sweep (9 values, real runner entry point each time)

`decay` chosen from ESS theory, **not** from OOS PnL: per-trade decay `d` converges the data
mass to `ESS* = d/(1−d)`, so the stated 40–60-trade target implies `d ∈ [0.9756, 0.9839]`;
`d = 0.98` → ESS* 49, mid-range. The suggested 0.90/0.95 give ESS* of only 9 and 19 — 2.5–5×
shorter than the target.

| decay | ESS* | Total PnL | vs baseline | Trades | Pass | pen / sev windows | WR@in range |
|---|---|---|---|---|---|---|---|
| 1.000 | ∞ | +5,553.70 | **+0.00** | 674 | 10 | 0 / 0 | [0.5000, 0.6491] |
| 0.995 | 199 | +5,553.70 | **+0.00** | 674 | 10 | 0 / 0 | [0.4932, 0.6492] |
| 0.990 | 99 | +5,553.70 | **+0.00** | 674 | 10 | 0 / 0 | [0.4653, 0.6494] |
| 0.985 | 66 | +5,393.95 | −159.75 | 639 | 10 | 2 / 0 | [0.4326, 0.6498] |
| **0.980** | **49** | **+5,397.98** | **−155.72** | 624 | 10 | 4 / 0 | [0.4082, 0.6504] |
| 0.970 | 32 | +4,661.57 | −892.13 | 578 | 9 | 7 / 1 | [0.3453, 0.6520] |
| 0.960 | 24 | +4,669.38 | −884.32 | 577 | 9 | 7 / 2 | [0.3119, 0.6540] |
| 0.950 | 19 | +4,686.28 | −867.42 | 577 | 9 | 7 / 3 | [0.2898, 0.6561] |
| 0.900 | 9 | +5,063.41 | −490.29 | 581 | 8 | 7 / 3 | [0.2947, 0.6787] |

**The pattern is unambiguous.** The three settings that match baseline (+0.00) are precisely
the three where the governor never fires. All six settings where it activates are worse —
every single one. The maximum across the whole sweep is a three-way tie at +5,553.70, shared by
`decay` = 1.000 / 0.995 / 0.990 — i.e. by the settings where the tracker does nothing.
There is no decay value at which this mechanism adds value.

---

## Root cause — the signal has no predictive content

The runner retrains the ML models **inside** the window loop
(`run_20_oos_dual_model.py:152`, loop begins `:133`):

```python
for w in windows:
    ...
    ridge, clf, mu, sd, calib_thresh = engine.train_models(train_set)
```

So the win rate realised in window *k* belongs to a **different model** than window *k+1*'s.
The tracker gates model *k+1* on model *k*'s performance — a quantity that is not stationary
by construction. Measuring the tracker's own forecasting skill directly:

| Test | Result |
|---|---|
| Pearson *r*, posterior WR@entry vs that window's realised WR | **+0.032** (n=20) |
| Pearson *r*, posterior WR@entry vs that window's net PnL | **+0.039** |
| Mean absolute error of the posterior vs realised WR | **13.0 percentage points** |
| Lag-1 autocorrelation of realised per-window WR | +0.2274 (SE ≈ 1/√20 = 0.224, ~1.0 SE — not distinguishable from zero at n=20) |

A correlation of +0.03 is zero. The governor is applying a ±2–4 bp threshold penalty on
essentially random information, so in expectation it can only subtract value — and it does.

The failure mode is visible in the scorecard. At W10 entry the posterior read **0.4168**
(driven by W07/W08/W09 win rates of 38.1% / 30.0% / 16.7%), firing the +0.02 penalty. W10's
freshly-retrained model then delivered **57.4%** in baseline. The penalty lifted the effective
threshold from 0.4803 to 0.5003, cut S1 entries from 29 to 1, and turned a **+510.86 PASS
into a −113.42 FAIL** (−624.28). The governor correctly remembered a bad model and punished a
good one.

---

## What *did* work

1. **Removing the relief branch was right.** v1's −0.01 relief loosened entries into the
   Jan-2022 macro tightening and flipped W04 from +736.83 to −111.99. Penalty-only eliminates
   that entire failure class, worth +229.50 over v1.
2. **Decay made the mechanism responsive**, as designed: the posterior now actually reaches
   below 0.45 (0.4082 at W11, 0.4318 at W09, 0.4408 at W15) and the penalty fires in 4
   windows — something the cumulative posterior could never do (min entry WR 0.5000, penalty
   fired 0/20).
3. **Plumbing is side-effect-free.** Whenever the governor is inert, output is *bit-identical*
   to baseline — same 674 trades, same +5,553.70, at three independent decay settings. And in
   v1, all 17 windows with Δthresh = 0.000 were bit-identical. The integration is clean.
4. **Memory continuity holds** across all 20 windows at every decay setting.

---

## Recommendation

**Do not ship this enhancement.** The ablation cannot succeed at any decay value, because the
premise assumes a persistent strategy-level win rate and this architecture does not have one.

Two directions that would make the premise valid:

- **Track something that persists.** Regime statistics (BTC realised vol, tide alignment,
  cross-sectional dispersion) are properties of the *market*, not of the model, so they
  survive refits. Gate on those instead.
- **Or stop refitting per window.** A single frozen model evaluated across all 20 windows
  *would* have a persistent win rate, making a Beta-Binomial governor meaningful. That is a
  much larger architectural change.

If a defensive governor is needed today, gate on trailing **drawdown** rather than win rate —
the existing Hsieh-Barmish damping and the 4.40% circuit breaker already do this on a
quantity that is actually persistent.

---

## v2 scorecard (decay = 0.98, penalty-only)

| W# | Window | Trades | S1 | T1 | WR | Net PnL | ROI | Max DD | Status | WR@in | n@in | Δthr | eff_thr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W01 | May 2021 Great Liquidation Crash | 47 | 37 | 10 | 66.0% | +628.30 | +12.57% | 2.01% | PASS | 0.5000 | 0 | +0.000 | 0.5120 |
| W02 | September 2021 El Salvador Flash Crash | 29 | 18 | 11 | 55.2% | +210.71 | +4.21% | 4.62% | PROFIT | 0.6360 | 37 | +0.000 | 0.5120 |
| W03 | November 2021 Cycle Peak Reversal | 18 | 11 | 7 | 50.0% | +26.57 | +0.53% | 4.28% | PROFIT | 0.6504 | 55 | +0.000 | 0.5120 |
| W04 | January 2022 Fed Macro Tightening | 47 | 24 | 23 | 57.4% | +736.83 | +14.74% | 3.44% | PASS | 0.5962 | 66 | +0.000 | 0.5060 |
| W05 | May 2022 Terra-Luna Systemic Shock | 60 | 37 | 23 | 46.7% | +500.04 | +10.00% | 3.69% | PASS | 0.6275 | 90 | +0.000 | 0.4994 |
| W06 | June 2022 3AC & Celsius Capitulation | 57 | 37 | 20 | 57.9% | +546.66 | +10.93% | 3.30% | PASS | 0.4591 | 127 | +0.000 | 0.4927 |
| W07 | September 2022 ETH Merge Chop & Grind | 21 | 11 | 10 | 38.1% | −224.93 | −4.50% | 4.50% | FAIL | 0.4830 | 164 | +0.000 | 0.4873 |
| W08 | November 2022 FTX Collapse Bottom | 10 | 3 | 7 | 30.0% | −181.04 | −3.62% | 4.42% | FAIL | 0.4596 | 175 | +0.000 | 0.4804 |
| W09 | January 2023 Bullish Short Squeeze | 6 | 4 | 2 | 16.7% | +34.31 | +0.69% | 3.29% | PROFIT | 0.4318 | 178 | **+0.020** | 0.4750 |
| W10 | March 2023 SVB Bank Run & USDC Depeg | 13 | 1 | 12 | 46.2% | −113.42 | −2.27% | 5.41% | FAIL | 0.4168 | 182 | **+0.020** | 0.5003 |
| W11 | June 2023 BlackRock Spot ETF Momentum | 28 | 8 | 20 | 64.3% | +665.48 | +13.31% | 2.96% | PASS | 0.4082 | 183 | **+0.020** | 0.4967 |
| W12 | August 2023 Mid-Summer Flash Liquidation | 22 | 2 | 20 | 63.6% | +244.64 | +4.89% | 3.23% | PROFIT | 0.4603 | 191 | +0.000 | 0.4742 |
| W13 | October 2023 Uptober Spot ETF Ignition | 19 | 3 | 16 | 73.7% | +608.33 | +12.17% | 1.37% | PASS | 0.4621 | 193 | +0.000 | 0.4728 |
| W14 | January 2024 Spot ETF Approval Shakeout | 20 | 8 | 12 | 50.0% | +29.61 | +0.59% | 2.55% | PROFIT | 0.4748 | 196 | +0.000 | 0.4728 |
| W15 | March 2024 Pre-Halving ATH Run | 40 | 21 | 19 | 62.5% | +504.62 | +10.09% | 0.97% | PASS | 0.4408 | 204 | **+0.020** | 0.4920 |
| W16 | August 2024 Global Carry Trade Liquidation | 34 | 23 | 11 | 50.0% | +517.00 | +10.34% | 1.51% | PASS | 0.4850 | 225 | +0.000 | 0.4680 |
| W17 | November 2024 US Election Mega Breakout | 73 | 44 | 29 | 54.8% | +507.29 | +10.15% | 3.40% | PASS | 0.4875 | 248 | +0.000 | 0.4679 |
| W18 | February 2025 Post-Inauguration Consolidation | 11 | 7 | 4 | 54.5% | −215.83 | −4.32% | 4.48% | FAIL | 0.5061 | 292 | +0.000 | 0.4683 |
| W19 | July 2025 Mid-Year Volatility Expansion | 50 | 19 | 31 | 62.0% | +596.01 | +11.92% | 3.64% | PASS | 0.5147 | 299 | +0.000 | 0.4658 |
| W20 | March 2026 Late-Cycle Microstructure Shock | 19 | 16 | 3 | 31.6% | −223.19 | −4.46% | 4.46% | FAIL | 0.5110 | 318 | +0.000 | 0.4605 |

**Totals: 10/20 PASS · 624 trades · +5,397.98 USD (+107.96% ROI)**
Terminal state: `Beta(21.964, 27.980)`, lifetime n=334, decayed eff_n=49.94, posterior WR
0.4398, final Δthresh +0.020. Severe +0.04 branch: never fired at d=0.98 (fired in 3 windows
at d≤0.96).

### v2 attribution (only 4 windows differ from baseline)

| Window | Baseline | v2 | Δ | Cause |
|---|---|---|---|---|
| W09 | +34.31 | +34.31 | 0.00 | penalty fired, no behavioural change |
| W10 | +510.86 | −113.42 | **−624.28** | penalty cut S1 29→1; PASS→FAIL |
| W11 | +200.96 | +665.48 | **+464.52** | penalty helped |
| W15 | +500.59 | +504.62 | +4.03 | negligible |
| *net* | | | **−155.72** | |

---

## Verification performed

- **Unit tests** on `BayesianThresholdState`: relief branch confirmed absent from
  `threshold_delta` source; penalty-only invariant verified non-negative over a 199×199
  (alpha, beta) grid; boundaries exact at WR = 0.34/0.35/0.44/0.45/0.60/0.80; ESS converges to
  49.99 at d=0.98 (theory 49.0, +1 for the current trade).
- **Full 20-window suite run 10×** — once per decay value, each via the real
  `Engine/run_20_oos_dual_model.py` entry point (not a re-implementation).
- **Inertness control**: three independent decay settings reproduce baseline exactly.
- **Bug found and fixed**: `--decay 1.0` raised `ZeroDivisionError` in the ESS print.

## Environment notes (unchanged from v1)

`scratch/cache_multi_tf` is absent from the repo and had to be reconstructed
(`scratch/build_cache_multi_tf.py`); the documented +6,454.66 is not reachable here.
`fast_numba_oos_engine.py` paths were hard-pinned to `C:\Users\SIGMA\...`. Windows are
**monthly**, not 3-month quarterly. Verified 15m masters: 2,323,304 bars across 11 symbols.

## Reproduction

```bash
pip install numpy pandas pyarrow scikit-learn lightgbm numba
python3 scratch/build_cache_multi_tf.py                          # reconstruct 4h artefact
python3 Engine/run_20_oos_dual_model.py --decay 0.98             # v2 primary run
python3 scratch/sweep_decay.py                                   # full 9-point sweep
```

Logs: `scratch/patched_decay098.log`, `scratch/sweep_out.log`, `scratch/sweep/*.json`
(gitignored — `scratch/` is a build directory).
