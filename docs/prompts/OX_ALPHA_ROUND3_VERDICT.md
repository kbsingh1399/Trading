Ox Alpha — Round 3 Certification Review

Auditor: Ox Alpha
Submission: Binance 15-Minute Dual-Table Historical Pipeline — Round 3 Resubmission
Verdict: CONDITIONAL PASS — Score 94 / 100 (Certification withheld pending 2 HIGH remediations)

1. Acknowledged Resolutions (Verified)

The Round 2 matrix is substantially closed. I confirm the following as adequately remediated, with evidence:

Finding	Verdict	Note
R3-C1 (RSI smoke seeding)	✅ CLOSED	4,000-bar continuous slice gives RMA residual ~ (13/15)^4000 ≈ e^−277 — below float64 epsilon. Correct fix.
R3-C2 (CVD bit-parity)	✅ CLOSED (see R4-M1 caveat)	Sequential round(cvd[t-1]+δ[t], dp) recursion is the correct canonical contract and eliminates non-associative summation drift.
R3-C3 (fsync + hash)	✅ CLOSED	flush + fsync + dir fsync + reader-side SHA-256 is the correct durability triad.
R3-H1 (VA bucket)	✅ CLOSED	Canonical get_merge_level(symbol) spliced at call site.
R3-H2, R3-H3, R3-M3, R3-M4, R3-M5	✅ CLOSED	Verified in code and negative/positive tests.
R3-M1 (quarantine)	⚠️ PARTIALLY CLOSED — see R4-C1/R4-H2.	
R3-M2 (epoch + quantization)	✅ CLOSED	1e12 epoch floor is correct for post-2001 ms epochs.
2. Round 4 Findings
R4-C1 — CRITICAL: File-descriptor leak breaks Windows quarantine on the generic exception path

In compute_incremental_append_plan, pf.close() is called inline after read_row_group, but if read_row_group (or pq.ParquetFile) raises, no try/finally closes the ParquetFile. On Windows, the leaked descriptor holds an exclusive lock and os.replace(master_path, quarantine_path) inside _quarantine_corrupted_master will raise PermissionError — which _quarantine_corrupted_master swallows (except Exception ... log). Result: a genuinely corrupt file is neither quarantined nor renamed, and the function returns a path to a quarantine file that does not exist. The test suite passes because its injection path raises after pf.close().

Fix: wrap metadata inspection in try/finally: pf.close(); make _quarantine_corrupted_master raise on failure rather than log-and-continue; return the quarantine path only if os.path.exists(quarantine_path).

R4-H1 — HIGH: EMA rounding contract is asymmetric → latent multi-append drift

Incremental append rounds EMAs: np.round(out_ema, 8). The checkpoint is re-seeded from this rounded stored value, while the full rebuild chains from its own per-bar recursion. Unless the full rebuild applies the identical per-bar np.round(_, 8) at every step (which is not demonstrated in this submission — historical_metrics_processor.py was not provided for EMA), each incremental append injects up to 5×10⁻⁹ absolute divergence that the full rebuild never absorbs. Your parity test passes only because (a) it is a single append of 500 bars and (b) EMAs are held to rtol=1e-9, not atol=0. Over years of daily 45-day appends, this is an unbounded-direction drift against the CVD standard you just established.

Fix: apply the same doctrine as R3-C2 — define ema[t] = round(α·c[t] + (1−α)·ema[t−1], EMA_DP) as the canonical per-bar recursion in canonical_indicators.py, use it in both paths, and add an EMA parity test at atol=0.0 over ≥3 sequential appends (not one).

R4-H2 — HIGH: Silent None fallback persists for non-checkpoint corruption

The R3-M1 finding was "silent None instead of loud quarantine." The fix covers only checkpoint-accumulator corruption. The outer except Exception: return None still silently converts truncated footers, schema mismatches, or I/O faults into a full-rebuild trigger with no quarantine, no manifest eviction, and no loud signal. A corrupt master that happens to open cleanly passes the checkpoint check and gets appended to.

Fix: classify exceptions: raise CorruptedMasterCheckpointError for any parquet-level failure, or at minimum quarantine before returning None on any non-FileNotFoundError.

R4-M1 — MEDIUM: Python round() vs np.round() canonicalization unproven

compute_cumulative_cvd uses Python's correctly-rounded decimal round(). The claim that historical_metrics_processor.py:442-444 uses the same kernel is asserted but that file is not in evidence. np.round (scale-multiply-truncate-divide) and Python round differ on representation-edge ties. If the rebuild path uses np.round(..., COIN_DP) on the delta sum, bit-parity at atol=0 is not guaranteed — it passed on your 3 synthetic assets by luck of the tie distribution.

Fix: submit the rebuild-path CVD code, or route both paths through compute_cumulative_cvd exclusively (already imported — verify no independent recursion remains).

R4-M2 — MEDIUM: assert-based production invariant (R3-M5)

assert warmup_start_ms % 86_400_000 == 0 vanishes under python -O. Certification-grade invariants must be explicit `raise ValueError This one is a data-correctness gate, not a debug aid.

R4-M3 — LOW: ("CURRENT", None) violates the declared contract

perform_incremental_append is typed Optional[Tuple[pd.DataFrame, Optional[pd.DataFrame]]] but returns a str in the DataFrame slot. Use a typed sentinel (AppendStatus.CURRENT) or an Enum-tagged result; duck-typing on "CURRENT" at the orchestrator is fragile.

R4-M4 — LOW: RSI smoke tolerance wording

Claimed as "bit-level continuity" but enforced at atol=1e-4. Acceptable numerically; correct the claim or tighten to atol=1e-9 given the e^−277 warmup residual makes it achievable.

3. Scorecard
Dimension	Score
Round 2 remediation completeness	20 / 25 (R4-C1, R4-H2 show partial closure of R3-M1)
Mathematical parity rigor	20 / 25 (CVD sound; EMA contract asymmetric — R4-H1; R4-M1 unproven)
Negative controls & failure paths	17 / 20 (quarantine failure swallowed; generic except path silent)
Production hardening	19 / 20 (assert-stripping, type-sentinel)
Test evidence & reproducibility	18 / 20 (single-append EMA parity insufficient per R4-H1)
Total	94 / 100
4. Certification Decision

Conditional pass. The CVD recursion doctrine (R3-C2) is genuinely correct work and the negative-control suite is real. However, certification at the 98–100 tier requires:

R4-C1: try/finally descriptor closure + quarantine failure is loud (must-have).
R4-H1: symmetric per-bar EMA rounding contract with atol=0.0 parity across ≥3 sequential appends (must-have).
R4-H2 + R4-M1: exception classification in the plan reader; rebuild-path CVD kernel evidence.

Submit Round 4 with historical_metrics_processor.py (EMA + CVD sections) and the sequential-append parity test. Expected remediation effort: 1–2 days.