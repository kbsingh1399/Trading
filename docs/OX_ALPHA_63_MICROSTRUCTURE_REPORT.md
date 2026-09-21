# OX_ALPHA_63 — Institutional Microstructure Architecture: Final Report

**Date:** 2026-09-21 | **Branch:** `arena/01a0bf23-trading` | **Program:** single-shot, pre-registered
**Protocol:** `docs/ox63_research/PROTOCOL.md` (filed before any OX63 computation; amendments A1–A2 pre-compute)
**Directive:** `docs/prompts/Ox_Alpha_63_Institutional_Microstructure_Architecture.txt`

---

## 1. Verdict

**The mandated package is REJECTED under the pre-registered conjunction.** Every institutional
standard fails under both economics. No iteration was performed (single-shot honored).

| Standard | Research $50 | Production $10 | Conjunction |
|---|---|---|---|
| Sharpe ≥ 1.50 (Mon–Fri daily, rf=0, √252) | −3.039 ❌ | −3.132 ❌ | ❌ |
| Profit factor ≥ 1.35 | 0.712 ❌ | 0.739 ❌ | ❌ |
| Portfolio maxDD ≤ 10% | 51.80% ❌ | 33.13% ❌ | ❌ |
| 2024 PnL > 0 (completed year) | −$1,100.54 ❌ | −$616.20 ❌ | ❌ |
| 2025 PnL > 0 (completed year) | −$854.05 ❌ | −$649.05 ❌ | ❌ |

Portfolio net: **−$2,549.48** ($50, 576 filed executions) / **−$1,558.07** ($10, 1,624 filed executions),
capital $5,000. Per-window disclosure: **0/20 PASS under both economics** (criterion disclosed only;
portfolio standards replaced it per protocol §4).

## 2. Evidence grade (honesty)

**EXPLORATORY-CONFIRMATORY HYBRID** (protocol §1). F6 was selected for refinement because of its
OX62 W09 (+20.8R) — outcome-informed selection — and OX62-CV showed F6 does not replicate (0/20).
The refinements are structural priors (scaling mechanics, MSB doctrine), evaluated single-shot with
full reporting. **Funded-live deployment still requires future-data validation.** Nothing in this
report is tuned: all implementer's choices (P1–P17) were filed before compute; the only two
amendments (A1 Sharpe day-count/union rule, A2 lock-assignment clarification) are pre-compute.

## 3. What was built (mandates M2–M4 — all delivered)

**M2 — 2-stage scaling engine + veto relaxation.**
- Kernel (`Engine/core/strategy_kernel.py`, additive only): `UX_TP1_R=1.10`, `UX_TP1_FRAC=0.50`,
  `UX_TP1_LOCK_R=0.15`, `UX_MIN_R_EFF_SCALED=1.20`, `_ux_exit_scaled_long/short` (bar order:
  gap-SL → SL → TP1 → runner-SL → TP2 → Friday → decay → ratchet → reversal; gap through TP1
  banks at TP1 exactly, no surplus). Monolithic `_ux_exit_*` untouched (source-guarded by test).
- `Engine/forex_engine.py`: `MIN_STRUCTURAL_R_EFF` 2.50 → **1.20** (mandated; this also aligns the
  code with its own `calculate_adaptive_sl_tp` docstring, which already claimed "1.20 to 3.50");
  `close_partial()` (fractional close, partial ledger, live-MT5 branch with broker-step flooring);
  TP1 block in `manage_open_trades` (fires before TP2, falls through for same-tick runner
  management, rollover-suppressed with retry, `tp=0` guard preserves monolithic behavior).
- `Engine/live/order_manager.py`: full mirror (`close_partial`, TP1 block with SL-priority guard,
  `tp1_scaled`/`partial_pnl` schema, redundant stage-1 re-fire suppressed post-TP1).
- Kernel also gained `close_4h_asof` (shift(1) + backward-asof, existing pattern) for the MSB anchor.

**M3 — F6R refinement.** F6{d:1.0} with `htf>0` → `(htf>0 | msb_bull)` (long, mirror short), where MSB
is a 20-bar 4H-close Donchian break on the shifted as-of series (P3/P11, mandate M3.1; verified
`htf_4h_trend` ≡ 4H EMA-200 5-bar slope, so the filed formula implements the mandate verbatim).
KZ / Friday-entry / floor / cap / fallback-2.5R / friction-0.08R rules unchanged (P2/P4).

**M4 — verification.** 36 new checks green (11 scaled-engine + 8 paper-manager + 6 live-mirror +
11 MSB/F6R/candidate); frozen suites green (35 ox61 + 9 ox62 + 8 execution-safety; prelaunch
TEST 1–5 green, TEST 6 pre-existing crash unchanged); **R4 pins reproduce to the byte.**

## 4. Results

### 4.1 Candidate pools (filed)

| Pool | n | avgR | Win% | netR | scaled@TP1 |
|---|---|---|---|---|---|
| F6R scaled (veto 1.20) | 2,254 | −0.1159 | 55.7 | −261.32 | 38.46% |
| F6R mono (veto 2.50, P12 counterfactual) | 890 | −0.0546 | 55.1 | −48.59 | — |

The veto relaxation admitted 2.5× candidates (1,364 extra setups in the 1.20–2.50 R_eff band).
The MSB expansion itself is a near-no-op: EURUSD F6 540/550 → F6R 548/558 signals (+1.5%);
mono pool 890 vs OX62 F6 887 (+3 admitted).

### 4.2 Portfolio metrics (filed per-window executions, time-sorted continuous equity)

| Economics | Trades | Sharpe | PF | maxDD | 2023* | 2024 | 2025 | 2026* | Net |
|---|---|---|---|---|---|---|---|---|---|
| $50 research | 576 | −3.039 | 0.712 | 51.80% | −421.38 | −1,100.54 | −854.05 | −173.52 | −2,549.48 |
| $10 production | 1,624 | −3.132 | 0.739 | 33.13% | −220.79 | −616.20 | −649.05 | −72.03 | −1,558.07 |
| mono $50 (P12) | 513 | 0.437 | 1.049 | 15.45% | +375.11 | +281.81 | −200.50 | −85.06 | +371.35 |

\* partial-year disclosure (span starts 2023-09-15, ends 2026-03-31); 2024/2025 fully covered.

### 4.3 Per-window disclosure (scaled; PASS/FAIL vs untouched legacy criterion, informational)

$50 economics, 0/20: every window negative except W04 (+$52.02) and W12 (+$19.88); all windows
reach 4.4–4.8% local DD (freeze territory — the governor truncates each window, which is why
executed counts are low: 576 of 2,254 candidates survive).

$10 economics, 0/20: slower DD accumulation → fewer freezes → 1,624 executions, still negative
in 17/20 windows (positives: W05 +$7.23, W13 +$65.53, W20 +$52.62).

P12 counterfactual (mono 2.5R, identical F6R signals), 1/20: **W09 PASS (+$598.77, +20.79R)** —
the same W09 alpha OX62 found for F6, reproduced to the R. All other windows disclosed FAIL;
portfolio net +$371.35, Sharpe 0.437, PF 1.049 — below institutional standards but strictly
better than scaled on every metric.

Full tables: `docs/ox63_research/scorecard_ox63_{50,10,mono50}.csv`.

### 4.4 Mechanism (why the package failed)

1. **TP1 caps the tail that carried the edge.** Scaled W09: 62.8% win rate yet −1.39R net, vs mono
   W09 +20.79R at 72.7% WR on nearly identical trade counts (43 vs 44). Banking half at +1.10R
   converts a positive-skew strategy into negative expectancy when the edge lives in runners.
2. **The relaxed veto adversely selects.** The 1.20–2.50 R_eff band contributes volume at worse
   mean-R (pool avgR −0.116 vs −0.055); winners capped, losers still −1.0R.
3. **Freeze dynamics differ by economics** (576 vs 1,624 executions) but both converge negative —
   the loss is in the trade stream, not the governor.
4. **MSB adds ~nothing** (+1.5% signals): the 4H structural anchor rarely binds beyond the EMA
   slope on sweep bars. Refinement direction exhausted, not just the parameters.

### 4.5 Cross-program consistency (causal verification)

- Mono-2.5R replay of F6R reproduces OX62 F6 W09 **exactly** (+20.7897R PASS) — independent code
  path, same alpha. The harness is sound; the signal is real-but-fragile and scaling kills it.
- Unscaled-path parity proven: pre-TP1 full-stop and decay legs are bit-identical between the
  monolithic and scaled sims (S8a/S8b), so all performance delta is attributable to the
  treatment (veto + TP1 interposition), not plumbing drift.
- Determinism: `run_ox63.py --check-only` — all filed artifact hashes match and the in-memory
  re-run reproduces every logical hash (2,254 / 890 / 576 / 1,624 / 513 rows).

### 4.6 R4 caveat (pre-existing, not OX63-caused)

`run_ox61_r4.py --check-only` rewrites the working `scorecard_dual_r6_{unified,precommitted}.csv`
files (despite its "no overwrite" docstring) under the CURRENT tip economics. On this tip the
committed criteria carry `base_risk_usd=10` (merge `f48e5a5`, which explicitly discloses that the
R4 pin "must be re-run to re-certify under base_risk_usd=10"), while the pinned scorecards were
generated under $50 — so any regeneration necessarily drifts. Proof of OX63 innocence: re-running
R6-phase-C with the economics overridden back to $50 reproduces the committed scorecards EXACTLY
(maxdiff 0.0, both tags) on the modified code. Pinned R4 artifacts still hash-match. Related
pre-existing harness blind spot: the R4 byte-check never re-verifies replayed scorecard VALUES
(it re-hashes the pinned copies it does not regenerate), so economics drift passes silently.
Working files were restored to committed values; no OX61 files are touched by this commit.

## 5. Reproducibility

```
venv/bin/python docs/ox63_research/run_ox63.py              # single-shot pipeline (~5 s)
venv/bin/python docs/ox63_research/run_ox63.py --check-only # hash + determinism proof
venv/bin/python docs/ox63_research/test_ox63_{scaled,manager,mirror,msb}.py
```

Manifest: `docs/ox63_research/manifest_ox63.json` (params read from kernel constants, pool +
portfolio metrics, conjunction booleans, artifact sha256, code hashes).
Filed artifacts: `cand_ox63_F6R{,_mono}.parquet`, `exec_ox63_{50,10,mono50}.parquet`,
`scorecard_ox63_{50,10,mono50}.csv`.

## 6. Files changed

- `Engine/core/strategy_kernel.py` — additive: `close_4h_asof` col, TP1 constants, scaled exits.
- `Engine/forex_engine.py` — veto 1.20, `close_partial`, TP1 block, `tp1_scaled` schema.
- `Engine/live/order_manager.py` — live mirror of the above.
- `docs/ox63_research/` — protocol, lib, pipeline, 4 test suites, manifest, filed artifacts.
- `docs/OX_ALPHA_63_MICROSTRUCTURE_REPORT.md` — this report.

## 7. Recommendation

**STOP on this direction.** The pre-registered hypothesis — that 2-stage scaling + veto relaxation
+ MSB anchoring would lift F6 to institutional portfolio standards — is rejected 0/5 on the
conjunction under both economics, and the P12 decomposition shows the treatment is actively
harmful vs monolithic exits on identical signals. Retain the infrastructure (the scaling engine is
certified, tested, and live-mirrored) for any future family whose edge is proven to live in
win-rate rather than tail skew. Any further F6 work requires new structural priors and
future-data validation — not more iteration on 2023–2026.
