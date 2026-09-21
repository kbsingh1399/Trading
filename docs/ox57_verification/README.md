# OX ALPHA 57 — verification artifacts
Target: origin/main @ 9559471 (residual-fix commit 4806800 over OX56 baseline d4e1433).
Sandbox: repo-root checkout of origin/main (scripts use /tmp/ox57_verify).
- `ox57_functional_tests.py` — 14 checks: J(backtest hysteresis hold/release/re-entry/parity) K(engine connect, defense persistence round-trip, docstring, friction comment).
- `ox56_regression_delta.py` — OX56 suite with the single H.eng-connect expectation flipped for 4806800 (original pinned in docs/ox56_verification/).
- `ox57_canonical_wf.py` / `ox57_repro.py` — canonical walkforward + per-window sweeps.
- CSVs — `ox57_canonical_post` (14/20), `ox57_canonical_fullhist` (17/20), `ox57_parallel_perwindow` (15/20).
