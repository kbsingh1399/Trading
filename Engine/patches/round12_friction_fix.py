"""
================================================================================
ROUND 12 -- FRICTION VIABILITY FIX (the Round 11 kill switch)
================================================================================
Deterministic, auditable transformation applied to the Round 11 strategy file.
Run it against a copy of rp2_round11_regime_adaptive_ml.py (renamed to the
Round 12 module) to reproduce the single highest-impact change in Round 12.

WHY
---
Round 11 shipped `max_friction_r = 0.22`. The entry gate is

    (rt_friction * entry) / r_unit <= max_friction_r

With 41 bps round-trip friction (8 bps taker x2 + 10 bps entry slip + 15 bps
exit slip) that demands

    r_unit / entry >= 0.0041 / 0.22 = 1.864% of price

on a FIFTEEN-MINUTE bar. Measured stop distances of actually-emitted
candidates:

    p5 0.2120% | p25 0.2920% | p50 0.3888% | p75 0.5314% | p95 0.9229%
    p100 1.1146%

Candidates satisfying the gate: 0 of 58. Entry-gate census before the fix:

    {'friction_reject': 58}      # 100% of candidates, every window

This was not a strict threshold. It was an unconditional kill switch, and it
is the dominant cause of Round 11's 10 trades across 20 months. Note that no
relaxation of disp_atr_mult, arm_expiry_bars or conf_min_score could ever
have reached it: those govern candidate PRODUCTION, while every candidate
produced was destroyed downstream at CONSUMPTION.

THE DERIVED REPLACEMENT (not a fudge)
-------------------------------------
Maximise  ratio = n * E_net / L_max  (must exceed 4.0), where

    E_net  = E_gross - rt_friction / s        s = stop as a fraction of price
    n      = slots * 2880 / hold              throughput is concurrency-bound
    hold  ~= (tp * s / atr_frac)^2            diffusive time to travel 4s
    L_max  = log(n(1-wr)) / log(1/(1-wr))     expected longest losing run

A wider stop buys lower friction but costs throughput quadratically. The
optimum is broad, at s = 0.70% of price. Sized on the PESSIMISTIC wr = 0.40,
one configuration holds across the whole plausible win-rate band:

    wr 0.40 -> n~90  E_net +0.414R  ratio  4.77  PASS
    wr 0.44 -> n~90  E_net +0.614R  ratio  8.18  PASS
    wr 0.48 -> n~90  E_net +0.814R  ratio 12.46  PASS

ratio exceeds 4.0 for s in 0.40%..1.25%, so this is a plateau, not a knife
edge.

SECOND, STRUCTURAL CHANGE
-------------------------
A too-tight stop is now WIDENED to the viable floor rather than discarding
the setup. Risk is unaffected: position size is qty = risk / r_unit, so a
wider stop simply buys fewer units. The setup survives and friction is
bounded by construction.

ORDERING MATTERS
----------------
min_stop_atr/max_stop_atr is a STRUCTURE-quality filter and must be evaluated
on the raw swing stop. The friction floor is an EXECUTION constraint applied
afterwards. Applying the floor first made the band re-reject the very stops
just repaired, throwing away 38 of 58 candidates.

RESULT (fixture, one 28-day window, 2 symbols)
    before: 58 candidates ->  0 admissible ->  0 trades
    after : 58 candidates -> 58 admissible -> 18 trades
================================================================================
"""

import io
import sys

P = sys.argv[1] if len(sys.argv) > 1 else "rp2_round12_regime_adaptive_ml.py"
src = io.open(P, encoding="utf-8").read()
orig = src

# ---------------------------------------------------------------- 1. config
old_cfg = "    max_friction_r: float = 0.22           # friction may not exceed 22% of 1R"
new_cfg = '''    # ------------------------------------------------------------------
    # FRICTION VIABILITY -- ROUND 12 STRUCTURAL FIX
    # ------------------------------------------------------------------
    # Round 11's 0.22 demanded a stop >= 1.864% of price on 15-minute bars
    # while measured stops were 0.21%-1.11% (median 0.389%). NOT ONE
    # candidate could ever clear it. See Engine/docs/RP2_ROUND12_SPEC.md.
    #
    # 0.60 is DERIVED by maximising n * E_net / L_max subject to > 4.0,
    # sized on the pessimistic wr = 0.40. The optimum is a plateau
    # (ratio > 4.0 for stops 0.40%..1.25%), not a knife edge.
    max_friction_r: float = 0.60           # 0.0041 / 0.60 -> 0.683% stop floor
    widen_tight_stops: bool = True         # widen instead of reject'''
assert old_cfg in src, "config anchor missing"
src = src.replace(old_cfg, new_cfg)

# ---------------------------------------------------------------- 2. helper
anchor = "def scan_candidates("
assert src.count(anchor) == 1, "scan_candidates anchor not unique"
helper = '''def _min_stop_frac(cfg) -> float:
    """Smallest stop distance, as a fraction of price, whose round-trip
    friction stays inside max_friction_r of 1R."""
    rt = (2.0 * cfg.taker_fee_bps + cfg.entry_slip_bps
          + cfg.exit_slip_bps) / 10000.0
    return rt / max(1e-9, cfg.max_friction_r)


def _friction_viable_stop(px: float, stop: float, side: int, cfg) -> float:
    """Push a stop out to the friction-viable floor. Never pulls one in."""
    if not cfg.widen_tight_stops:
        return stop
    floor = _min_stop_frac(cfg) * px
    if abs(px - stop) >= floor:
        return stop
    return px - side * floor


'''
src = src.replace(anchor, helper + anchor, 1)

# ------------------------------------- 3. long branch: structure THEN floor
old_long = """                fn["confirm_pass"] += 1
                stop = min(arm.pb_ext, l[j]) - 0.10 * a
                da = (c[j] - stop) / a
                if cfg.min_stop_atr <= da <= cfg.max_stop_atr:
                    fn["stop_viable"] += 1
                    out.append(Candidate(
                        sym, j, SIDE_LONG, c[j], stop, SETUP_RECLAIM_LONG, fp,
                        int(reg[j]),
                        _feature_vector(f, j, SIDE_LONG, da, fp, int(reg[j]))))"""
new_long = """                fn["confirm_pass"] += 1
                stop = min(arm.pb_ext, l[j]) - 0.10 * a
                # structure gate on the RAW swing stop ...
                da = (c[j] - stop) / a
                if cfg.min_stop_atr <= da <= cfg.max_stop_atr:
                    fn["stop_viable"] += 1
                    # ... then apply the execution-side friction floor. The
                    # feature vector keeps the STRUCTURAL da so the model sees
                    # setup geometry, not an execution artefact.
                    stop = _friction_viable_stop(c[j], stop, SIDE_LONG, cfg)
                    out.append(Candidate(
                        sym, j, SIDE_LONG, c[j], stop, SETUP_RECLAIM_LONG, fp,
                        int(reg[j]),
                        _feature_vector(f, j, SIDE_LONG, da, fp, int(reg[j]))))"""
assert old_long in src, "long branch anchor missing"
src = src.replace(old_long, new_long)

# ------------------------------------ 4. short branch: structure THEN floor
old_short = """            fn["confirm_pass"] += 1
            stop = max(arm.pb_ext, h[j]) + 0.10 * a
            da = (stop - c[j]) / a
            if cfg.min_stop_atr <= da <= cfg.max_stop_atr:
                fn["stop_viable"] += 1
                out.append(Candidate(
                    sym, j, SIDE_SHORT, c[j], stop, SETUP_RECLAIM_SHORT, fp,
                    int(reg[j]),
                    _feature_vector(f, j, SIDE_SHORT, da, fp, int(reg[j]))))"""
new_short = """            fn["confirm_pass"] += 1
            stop = max(arm.pb_ext, h[j]) + 0.10 * a
            # structure gate on the RAW swing stop ...
            da = (stop - c[j]) / a
            if cfg.min_stop_atr <= da <= cfg.max_stop_atr:
                fn["stop_viable"] += 1
                # ... then the execution-side friction floor.
                stop = _friction_viable_stop(c[j], stop, SIDE_SHORT, cfg)
                out.append(Candidate(
                    sym, j, SIDE_SHORT, c[j], stop, SETUP_RECLAIM_SHORT, fp,
                    int(reg[j]),
                    _feature_vector(f, j, SIDE_SHORT, da, fp, int(reg[j]))))"""
assert old_short in src, "short branch anchor missing"
src = src.replace(old_short, new_short)

# ------------------------- 5. entry gate: widen, reject only if STILL bad
old_gate = """                    entry = raw_open * (1 + cd.side * eslip)
                    r_unit = abs(entry - cd.stop_px)
                    if r_unit <= 0:
                        continue
                    # friction viability: full round trip (fee BOTH legs + both
                    # slippages = 41 bps) must stay under max_friction_r of 1R
                    if (rt_friction * entry) / r_unit > cfg.max_friction_r:
                        continue"""
new_gate = """                    entry = raw_open * (1 + cd.side * eslip)
                    # The stop is set on the signal bar's close; the entry
                    # fills at the NEXT bar's open. Re-apply the friction
                    # floor against the ACTUAL entry so a gap cannot smuggle
                    # in a stop that is no longer viable.
                    stop_px = _friction_viable_stop(entry, cd.stop_px,
                                                    cd.side, cfg)
                    r_unit = abs(entry - stop_px)
                    if r_unit <= 0:
                        continue
                    # friction viability: full round trip (fee BOTH legs + both
                    # slippages = 41 bps) must stay under max_friction_r of 1R.
                    # After widening this can only fail on a pathological bar.
                    if (rt_friction * entry) / r_unit > cfg.max_friction_r:
                        continue"""
assert old_gate in src, "entry gate anchor missing"
src = src.replace(old_gate, new_gate)

# the Position must be armed with the WIDENED stop, not the raw candidate stop
old_pos = """                        stop=cd.stop_px, tp=entry + cd.side * tp_mult * r_unit,"""
new_pos = """                        stop=stop_px, tp=entry + cd.side * tp_mult * r_unit,"""
assert old_pos in src, "position anchor missing"
src = src.replace(old_pos, new_pos)

assert src != orig, "no change applied"
io.open(P, "w", encoding="utf-8").write(src)
compile(src, P, "exec")
print(f"friction fix applied to {P}: {len(orig)} -> {len(src)} bytes")
