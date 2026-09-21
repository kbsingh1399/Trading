# OX64 — LITERATURE CANDIDATE PROTOCOL (pre-registered)

**Objective:** single-shot test of 3 literature-grounded strategies, pre-specified from papers,
against the institutional portfolio standards (Sharpe ≥ 1.50, PF ≥ 1.35, DD ≤ 10%,
positive completed-year PnL 2024/2025, conjunction under BOTH $50 and $10 economics).
**Status:** written BEFORE any OX64 computation. Candidate set FROZEN at A+B+C; no paper-mining
beyond these three; no iteration under any result. Deviations require a dated amendment.

## 1. EVIDENCE GRADING (honesty)

**EXPLORATORY-CONFIRMATORY HYBRID (program-selection outcome-informed).** The decision to run a
literature program at all was caused by OX62/OX62-CV/OX63 failing — that selection is
outcome-informed and disclosed. WITHIN the program, evaluation is confirmatory: candidates are
theory-first (named papers below), formulas exact and filed before compute, all 3 reported,
no selection on results, no tuning of any constant. Portfolio metrics are the claim; per-window
tables are disclosure. **Funded-live still requires future-data validation.**

## 2. FROZEN (certified — must stay green)

- All OX61/OX62/OX63 suites (35 + 9 + 36 checks), 8 execution-safety, prelaunch TEST 1–5
  (TEST 6 pre-existing crash unchanged). R4 pins byte-reproduce.
- OX64 adds NO kernel/engine changes (pure `docs/ox64_research/` addition). If an engine change
  becomes necessary, it requires an amendment + full re-green.

## 3. CANDIDATES (exact formulas)

Shared definitions: UTC calendar days; a TRADING DAY has ≥10 15m bars else NaN (Q0). Daily bars
resampled (open=first, high=max, low=min, close=last). SIMPLE returns everywhere. σ20d = sample
stdev (ddof=1) of past 20 daily returns. ATR20d = mean of past 20 daily (high−low), min 15 days.
KZ = kernel `is_kill_zone` col (unchanged). Friction 0.08R. Span/window filtering + SPAN_END clip
identical to OX62/OX63. Replay + portfolio metrics = `ox63_lib` code reused verbatim.

**A — TSMOM-12M (Moskowitz–Ooi–Pedersen 2012).** At each month-end close S (last trading day of
calendar month M): formation = close[S]/close[S−12M]−1 over daily closes (need full 252 trading
days; else no signal). LONG if >0, SHORT if <0, flat if ==0 (Q1). NO threshold (paper-faithful).
Entry: open of first KZ bar strictly after last bar of S. Exit: close of last bar of last
trading day of month M+1 (1-calendar-month hold). NO SL/TP/ratchet/decay/Friday-closeout
(paper holds continuously; weekend-gap exposure disclosed). R numeraire = 1.5×ATR20d at entry
(ATR ∝ σ ⇒ fixed-$ risk = vol-scaled sizing, the paper's 1/σ rule in R units). r = signed
month-return/R − 0.08. Missing entry/exit bar → no candidate (truncation). Deviation disclosed:
price return, not excess (no risk-free data).

**B — Daily short-term reversal (Jegadeesh 1990 / Lehmann 1990, time-series form).** At each
trading-day close S: f = day_return[S]. T = 0.5×σ20d (Q2). LONG if f < −T, SHORT if f > +T,
else flat; σ20d ≤ 0 or NaN → flat. Entry: first KZ open strictly after last bar of S. Exit:
close of last bar of next trading day (never holds weekends by construction; no Friday rule
needed). No SL/TP (paper-faithful 1-day hold). R = 1.5×ATR20d; r = signed day-return/R − 0.08.
Truncation rule as A.

**C — Vol-managed F6 (Moreira–Muir 2017, per-trade form).** F6R signals + OX62 monolithic
plumbing VERBATIM (KZ gate, next-open entry, Friday veto, 1.5×ATR floor, veto 2.50, fallback
2.5R, cap 3.50, monolithic exits) — geometry bit-identical to the P12-mono stream. Sizing:
mult = clamp(σ20d(S)/median60(σ20d), 0.5, 2.0), computed from daily closes ≤ signal date S
(Q3); unavailable → 1.0. r_C = r_pre_mono/mult − 0.08. Any C-vs-mono delta is pure sizing
(testable property: identical datetime/asset/hold/reason, r scaled by 1/mult). Deviation
disclosed: MM's second-stage c-normalization skipped (base_risk sets absolute scale).

## 4. PRE-COMMITMENTS (Q0–Q8)

- **Q0:** trading day = ≥10 bars; **Q1:** A zero-formation → flat; **Q2:** B threshold 0.5×σ20d;
  **Q3:** C mult cap [0.5, 2.0], neutral 1.0 if unavailable; **Q4:** R = 1.5×ATR20d (A/B),
  geometric r/mult (C); **Q5:** A/B exit reason code 4 = HORIZON (replay ignores; disclosure);
- **Q6 (engines):** PRIMARY verdict = monolithic engine (signal isolation, OX62-comparable).
  C additionally replayed under the scaled engine as deployability disclosure (not in verdict).
  A/B are hold-to-horizon by construction (no scaled form exists) — structural, disclosed.
- **Q7 (verdict):** conjunction of the 5 standards under BOTH economics, per candidate,
  computed by reused `portfolio_metrics`. No cross-candidate selection: all 3 verdicts reported.
- **Q8 (prohibitions):** no threshold/horizon/asset/economics search; no re-running with
  different constants; reruns only for the determinism proof. Rerun of the full pipeline is
  allowed ONCE to confirm determinism (hashes must match); that rerun is the --check-only proof.

## 5. REPRODUCIBILITY

`run_ox64.py` + `manifest_ox64.json` (params, pools, portfolios, verdicts, artifact sha256,
code hashes, logical hashes) + `--check-only` byte/logical proof. Filed artifacts:
`cand_ox64_{A,B,C}.parquet`, `exec_ox64_{A,B,C}_{50,10}.parquet` (+C scaled), scorecard CSVs.

## 6. AMENDMENTS

- **A1 (pre-compute clarification, before any OX64 compute):** (a) "signed month/day-return/R"
  means signed PRICE MOVE divided by R: r = direction×(exit−entry)/R − 0.08 (R is a price
  distance, so return/R would mix units). (b) C rescale operates on filed mono r (rounded 4dp):
  r_C = round((r_mono+0.08)/mult − 0.08, 4); rounding epsilon ≤1e-4, deterministic, immaterial.
  (c) C-scaled disclosure = OX63 scaled exits on F6R masks + same mult rescale
  (r = round((r_scaled+0.08)/mult − 0.08, 4)), replayed under both economics.
