# OX-ALPHA-64 — Literature Candidates, Single-Shot (A/B/C)

**Date:** 2026-09-21 · **Program status:** COMPLETE — verdicts filed, no iteration performed.
**Protocol:** `docs/ox64_research/PROTOCOL.md` (pre-registered BEFORE any OX64 compute; frozen incl. amendment A1).
**Evidence grade:** EXPLORATORY-CONFIRMATORY HYBRID — candidate *program* was outcome-informed by OX62
(§1 of protocol), but all three frozen formulas, gates, metrics, and the conjunction rule were fixed
before the single-shot run. Standard: institutional portfolio (Sharpe≥1.5, PF≥1.35, DD≤10%,
2024>0, 2025>0) under BOTH $50 and $10 economics.

## 1. Candidates (literature mapping)

| # | Candidate | Paper formula (native) | Adaptation (pre-registered) |
|---|-----------|------------------------|------------------------------|
| A | TSMOM-12M | Moskowitz-Ooi-Pedersen 2012: sign(past-12M return), 1M hold | 252-trading-day formation, month-end signals, 1-calendar-month hold, R=1.5×ATR20d, no SL/TP |
| B | Daily reversal | Jegadeesh 1990 / Lehmann 1990 (time-series form) | Fade prior-day move if \|f\|>0.5σ20d, hold 1 trading day, same R |
| C | Vol-managed F6 | Moreira-Muir 2017: scale by 1/RV² | F6R + verbatim OX62 mono geometry, per-trade mult=clamp(σ20/med60,0.5,2.0) |

Survey covered TSMOM + critiques, currency momentum, intraday momentum (Gao et al. 2018),
volatility-managed portfolios, reversal/pairs (GGR), carry/value/VRP (excluded: no rates /
fundamentals / options data). Full survey with sources is preserved in the session record;
implementability filter documented in PROTOCOL §1.

## 2. Material data disclosure (discovered during OX64)

**15-minute density exists only from ~2023.** Median bars/day = 1 (daily backfill) for all years
before 2023 (GAS: before 2024); 2024+ medians are 86–96. Verified per asset/year in §4 of session
record. Consequences, all handled by pre-registered gates (no protocol change was needed):
- A needs 252 dense trading days → first EURUSD signal 2024-03-29 (not 2023-09); XAUCNH 2025-05;
  GAS later still. A's evaluation span compresses to ~24 monthly vintages.
- B/C gates (21/60 trading days) clear before W01 for all dense-from-2023 assets.
- OX62/OX63 unaffected (all spans ≥2023-09, dense region); their "2015–2026" range labels
  describe file coverage, not 15m density.

## 3. Method (frozen; one-line each)

- Q0: trading day = ≥10 bars; all trailing stats causal (days ≤ signal day). Truncation test T6
  proves zero look-ahead for A/B/C.
- A: month-end sign(12M formation); flat iff exactly 0.0; entry = first KZ open after month-end;
  exit = next-month-end close; r = dir×(exit−entry)/R − 0.08, R = 1.5×ATR20d.
- B: direction = −sign(prior-day return) gated |f|>0.5σ20d; entry = first KZ open; exit = next
  trading-day close (never holds weekends by construction, T7); same R/r.
- C: F6R masks + verbatim OX62 monolithic exits; r_C = (r_mono+0.08)/mult−0.08; mult neutral 1.0
  when stats unavailable; geometry bit-identical to mono (T5; pool n=890 = P12 exactly).
- C-scaled disclosure: OX63 scaled exits + same mult (pool n=2254 = OX63 exactly).
- Replay: OX63 replay_economics + portfolio_metrics verbatim (governor, rounding, DD estimator).

## 4. Results

### 4.1 Portfolio metrics (single-shot)

| Cand | Econ | Trades | Sharpe | PF | DD% | 2023 | 2024 | 2025 | 2026 | Net $ |
|------|------|--------|--------|----|-----|------|------|------|------|-------|
| A | $50 | 50 | 0.998 | 1.109 | 8.98 | +143.70 | +201.13 | +10.35 | −161.26 | +193.91 |
| A | $10 | 54 | −0.115 | 0.979 | 2.22 | +28.74 | +37.97 | −25.22 | −50.40 | −8.92 |
| B | $50 | 1197 | −3.527 | 0.603 | 58.21 | −540.55 | −998.45 | −1089.18 | −279.94 | −2,908.12 |
| B | $10 | 1304 | −4.125 | 0.599 | 20.68 | −206.08 | −316.88 | −446.38 | −60.38 | −1,029.71 |
| C | $50 | 521 | 0.548 | 1.066 | 16.01 | +429.82 | +0.17 | +93.92 | −5.06 | +518.85 |
| C | $10 | 711 | −0.084 | 0.986 | 7.48 | +101.51 | +46.24 | −162.25 | −32.01 | −46.52 |
| Cs | $50 | 577 | −2.080 | 0.784 | 43.38 | −349.81 | −890.36 | −695.10 | +16.63 | −1,918.64 |
| Cs | $10 | 1624 | −2.640 | 0.766 | 30.99 | −214.44 | −615.51 | −556.48 | −53.04 | −1,439.47 |

Pool baselines: A n=318 avgR −0.031 WR 51.9%; B n=6051 avgR −0.081 WR 40.3%;
C n=890 avgR −0.034 WR 53.8%; Cs n=2254 avgR −0.108 WR 54.5%.
Window-PASS (20-window scorecards): A 0/0, B 0/0, C 1/0, Cs 0/0.

### 4.2 Conjunction verdicts (each standard must hold under BOTH economics)

| Standard | A | B | C |
|----------|---|---|---|
| Sharpe ≥ 1.50 | ✗ (0.998 / −0.115) | ✗ | ✗ (0.548 / −0.084) |
| PF ≥ 1.35 | ✗ (1.109 / 0.979) | ✗ | ✗ (1.066 / 0.986) |
| DD ≤ 10% | ✓ (8.98 / 2.22) | ✗ (58.2 / 20.7) | ✗ (16.01 / 7.48) |
| 2024 PnL > 0 | ✓ | ✗ | ✓ |
| 2025 PnL > 0 | ✗ (+10.35 / **−25.22**) | ✗ | ✗ (+93.92 / **−162.25**) |
| **Conjunction** | **2/5 — FAIL** | **0/5 — FAIL** | **1/5 — FAIL** |

**Program verdict: 0/3 candidates deployable. No selection, no iteration, no post-hoc sign flips
were performed — the single-shot rule was honored.**

## 5. Honest observations (noted, NOT acted on)

1. **A-$50 Sharpe 0.998** is the closest anything has come to the 1.5 bar (P12-mono was 0.44) —
   but n=50, and A-$10 fails outright. Thin + economics-fragile. Any follow-up would be a NEW
   pre-registered program, not an extension of this one.
2. **C-$50 beats P12-mono-$50** (+$518.85 vs +$371.35, Sharpe 0.55 vs 0.44): vol-managed sizing
   helped in the direction Moreira-Muir predicts — but C-$10 fails, so the treatment is
   insufficient, not validated.
3. **B is decisively dead**: pool WR 40.3% means fades lose systematically — daily continuation
   dominates this span. The sign was pre-registered; flipping it post-hoc would be p-hacking.
4. A executed only 50–54 of 318 pool (1-month holds collide with the 2-concurrent governor) —
   a structural mismatch between monthly strategies and the intraday governor worth remembering.

## 6. Reproducibility

- Harness: `docs/ox64_research/` — `ox64_lib.py`, `run_ox64.py`, `test_ox64_signals.py` (10/10),
  `PROTOCOL.md`, `manifest_ox64.json`, 8 scorecards (CSVs committed; parquets git-ignored).
- Gate before single-shot: OX64 10/10 + OX63 36/36 + OX62 9/9 + execution-safety 8/8.
- `run_ox64.py --check-only`: all artifact hashes + full in-memory pipeline re-run match
  (20/20 logical hashes) — determinism proven.
- Economics parity: $50 proof-run from OX63 still reproduces HEAD scorecards; no engine file
  was touched by OX64 (research-dir-only change).

## 7. Standing-order status

The 20/20 goal is unmet and OX64 exhausted the implementable classics: neither paper-native
momentum (A), short-term reversal (B), nor vol-managed sizing of our best geometry (C) survives
institutional standards under both economics. The failure pattern is consistent across OX62–OX64:
gross edges ≈ 0–55bp/trade cannot clear 8bp-equivalent friction plus the portfolio-level
governor/concurrency structure. Any continuation must change the structure (costs, governor,
data, or edge family) under a NEW pre-registered protocol — not by re-mining these three.
