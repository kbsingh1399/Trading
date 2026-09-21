# OX ALPHA 55 — verification artifacts
Target: origin/main @ d99bb26 (remediation commit 5d67a81), verified via sparse checkout.
- `ox55_functional_tests.py` — 24 checks (A–F); set VERIFY_ROOT to a main-tree checkout, run headless.
- `ox55_repro_20w.py [parallel|fvg]` — per-window sleeve/interleave sweep (no candidate cache).
- `ox55_canonical_wf.py` — canonical `run_walkforward` path (precompute cache + per-window interleave); ROOT env selects tree, PRE=1 stubs mt5 for pre-remediation code.
- `ox55_repro_pre.py` — same as repro, pinned to the pre-remediation overlay + mt5 stub.
- CSVs — sweep outputs: `ox55_parallel_20w` (post per-window), `ox55_pre_20w` (pre per-window), `ox55_canonical_pre` / `ox55_canonical_post` (default span), `ox55_canonical_post_fullhist`, `ox55_fvg_20w` (FVG sleeve post).
