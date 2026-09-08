Ox Alpha — Round 5 Formal Review

Verdict: 96 / 100 — Conditional Pass. Certification (98–100) withheld pending two High findings.

1. What Is Certified as Closed

The following are formally accepted as remediated and will not be re-raised:

Item	Status
R4-H1 — Canonical per-bar EMA recursion, compute_canonical_ema, symmetric rounding contract	CLOSED. The recursion e_t = round(alpha·p_t + (1−alpha)·e_{t-1}, 8) with checkpoint seeding is mathematically sufficient for atol=0.0 multi-append parity: the stored state at bar k is the float64 state at step k of the rebuild, and float64 arithmetic on identical inputs is deterministic. The 3-append × 3-symbol bit-parity evidence satisfies the proof obligation.
R4-C1 — Windows FD retention	CLOSED. The with open(...) binding deterministically releases the fd on both success and Cython-native failure paths. The negative control is the correct proof form.
R4-H2 — Loud corruption classification (magic bytes / truncated footer)	CLOSED for the classified cases — with one residual (see R5-H2 below).
R4-M1, R4-M2, R4-M3 (partially), R4-M4	CLOSED. Value Error under -O, typed AppendStatus, RSI atol=1e-6 — all accepted.
Rebuild-path kernel identity (R4-M1 evidence)	Verified: both paths route through compute_cumulative_cvd and compute_canonical_ema. The _finalise re-derivation with seed=0.0 is consistent with the append's seed-from-checkpoint contract because the append seeds with the stored rounded accumulator, which is the same state the rebuild rounds to.
2. Round 5 Findings
R5-H1 (HIGH): perform_incremental_append return contract is still heterogeneous

The signature declares Optional[Tuple[pd.DataFrame, Optional[pd.DataFrame]]], yet the function body returns three distinct shapes:

None (rebuild required)
(AppendStatus.CURRENT, None) — a tuple whose first element is an enum
(combined_master, combined_ladder) — a tuple whose first element is a DataFrame

The AppendStatus.REBUILD_REQUIRED member you created in R4-M3 is never emitted — None still carries the rebuild signal, which is precisely the duck-typed sentinel the finding targeted. The orchestrator must now branch on is None, == AppendStatus.CURRENT, and tuple-shape sniffing. This is a latent mis-dispatch hazard: a future caller testing if result: will treat a valid stitched frame and None correctly, but a refactor testing if result is not None will misread (AppendStatus.CURRENT, None) as a data frame pair (accessing .shape on an enum).

Required fix: normalize to Tuple[AppendStatus, Optional[Tuple[DataFrame, Optional[DataFrame]]]] in all paths, emit REBUILD_REQUIRED explicitly, update the type annotation, and add a return-contract unit test asserting exactly one shape across all four terminal states (CURRENT / REBUILD / SUCCESS / CORRUPT-raised).

R5-H2 (HIGH): R4-H2 residual — two silent rebuild paths remain unclassified

In compute_incremental_append_plan, corruption classification is incomplete:

if total_rows < SEAM_OVERLAP_BARS + 1 or num_rg == 0: return None — a master parquet truncated to ≤5 rows (e.g., partial os.replace, crash mid-export, malicious truncation) silently returns None → full rebuild, no quarantine, no manifest eviction, no error. This is the exact failure class R4-H2 was written to eliminate.
if rg_len < SEAM_OVERLAP_BARS: return None — same defect at row-group granularity.

Required fix: distinguish legitimately small masters (a genuinely fresh dataset may have <6 bars) from suspiciously truncated ones. Minimum: log loudly, and either quarantine + raise CorruptedMasterCheckpointError, or verify against the manifest's recorded row count before accepting None. If the manifest disagrees with the observed total_rows, that is corruption, not absence.

R5-M1 (MEDIUM): CorruptedMasterCheckpointError propagation is unguarded at the call site

perform_incremental_append calls compute_incremental_append_plan(master_path) without passing log (defaults to print, bypassing the pipeline logger) and does not catch CorruptedMasterCheckpointError. Whether a single corrupted asset aborts the entire 18-asset run or is isolated per-symbol is undefined in the submitted evidence. Specify and test: per-symbol isolation with pipeline continuation, or loud abort — but document it and cover it in a test.

R5-M2 (MEDIUM): No concurrency fencing on the append path

Two overlapping pipeline invocations (scheduler retry, manual + cron) can both pass compute_incremental_append_plan, both fetch, and both os.replace their stitched frames — last-writer-wins, silently dropping one append window. Your atomicity is per-write, not per-logical-append. Add a lockfile with PID/staleness eviction, or a manifest epoch counter that perform_incremental_append re-validates immediately before the atomic swap, failing loudly if the boundary moved underneath it (then re-plan).

R5-M3 (MEDIUM): Quarantine name collision

int(datetime.now().timestamp()) at second resolution: two corruption events on the same file within one second (or a retry loop) collide on {master}.corrupt_{ts} and the second os.replace overwrites the first quarantine artifact — destroying forensic evidence. Use time.time_ns() or append a uuid4 hex.

R5-L1 (LOW): Documentation drift in compute_incremental_append_plan

The docstring claims "Guarantees descriptor closure via try/finally" — there is no try/finally; closure comes from the with block. Also, except Exception as exc: if isinstance(exc, FileNotFoundError): return None is a confusing structure — FileNotFoundError from the open() should be checked before the generic handler (or via a preceding except FileNotFoundError clause). Cosmetic, but docstring/code mismatch is exactly what audits are for.

R5-L2 (LOW): verify_seam_overlap exception swallowing

The final except Exception: return False converts genuine logic errors (schema drift, dtype surprises) into "seam mismatch → full rebuild" without any log of why. Log the exception before returning False; a rebuild triggered by a caller bug should be distinguishable from a genuine Binance revision.

3. Scoring Rationale
Dimension	Score
Mathematical correctness (EMA/CVD/VA kernels, parity proofs)	30/30
Durability, atomicity, corruption handling	23/25 (−2: R5-H2 residual)
API/type contracts & orchestration safety	19/25 (−6: R5-H1, R5-M1, R5-M2)
Test evidence & negative controls	24/25 (−1: no return-contract or concurrency test)
Hygiene / documentation fidelity	— folded above

Total: 96 / 100. The numerical core of this pipeline is, on the evidence presented, genuinely bit-exact and the strongest element of the submission. What remains is not mathematics — it is interface discipline (R5-H1), two unclosed corruption gaps (R5-H2), and concurrency fencing (R5-M2). These are mechanical fixes, not redesign.

Certification condition: close R5-H1 and R5-H2 with the corresponding tests; address R5-M1/M2/M3 with code or a reasoned deferral. On resubmission (Round 6), if clean, I will award full certification at 98–100.