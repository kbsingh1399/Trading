# OX ALPHA 56 — verification artifacts
Target: origin/main @ d4e1433 (P1 remediation; parent line d99bb26 verified in OX55).
Sandbox: repo-root checkout of origin/main (scripts use VERIFY_ROOT/ROOT=/tmp/ox55_verify post-update).
- `ox56_functional_tests.py` — 26 checks: H(headless×8 modules+connect) G(freeze %-leg, $-leg, ladder+per-trade parity) I(setup unification).
- `ox56_canonical_wf.py` / `ox56_repro_perwindow.py` — canonical walkforward + per-window sweeps.
- CSVs — P1-code scorecards: `ox56_canonical_post` (14/20 default span), `ox56_canonical_fullhist` (17/20), `ox56_parallel_perwindow` (15/20).
