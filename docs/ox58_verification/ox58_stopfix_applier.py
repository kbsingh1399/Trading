"""OX58-E4: Stop-erasure fix + trade-tracing applier (replaces lost .diff).

Applies to a PRISTINE copy of Engine/runners/run_23_oos_altcoin_suite.py
@ main 15c5e21 (the 5-sleeve tree with the S2/S4 precompile loop):
  Patch A (the fix): 4x `stopped_out` flags; the MTM fallback fires only for
                     TRUE expiries (no stop, no TP), never for stopped trades.
  Patch B (tracing): njit emits the event index per executed trade; the record
                     loop attaches symbol/strategy/r_gain/risk/prob. Proven to
                     have zero economic effect (unp+symbols rerun reproduced the
                     headline bit-for-bit: 23/23, 6,484, +$23,898.46).

Usage:  python3 ox58_stopfix_applier.py <pristine-tree> <overlay-tree> [--trace-only]
  Copies <pristine-tree>/Engine to <overlay-tree>/Engine, applies Patch A
  (unless --trace-only) + Patch B. Symlink data dirs into the overlay manually.

RECONSTRUCTED 2026-09-21 from verified session records; semantically identical
to the applied patch of 2026-09-20 (assert counts guard drift).
Does NOT apply at HEAD (6da9d7f): S2/S4 were removed from the runner.
"""
import shutil
import sys
from pathlib import Path

src = Path(sys.argv[1]); dst = Path(sys.argv[2])
trace_only = "--trace-only" in sys.argv
(dst / "Engine").parent.mkdir(parents=True, exist_ok=True)
if (dst / "Engine").exists():
    shutil.rmtree(dst / "Engine")
shutil.copytree(src / "Engine", dst / "Engine")

p = dst / "Engine" / "runners" / "run_23_oos_altcoin_suite.py"
s = p.read_text()

if not trace_only:
    n0 = s.count("r_gain = -1.0\n")
    s = s.replace("r_gain = -1.0\n", "r_gain = -1.0; stopped_out = False\n")
    n1 = s.count("if lows[j] <= stop_p: r_gain = -1.0; break")
    s = s.replace("if lows[j] <= stop_p: r_gain = -1.0; break",
                  "if lows[j] <= stop_p: r_gain = -1.0; stopped_out = True; break")
    n2 = s.count("if highs[j] >= stop_p: r_gain = -1.0; break")
    s = s.replace("if highs[j] >= stop_p: r_gain = -1.0; break",
                  "if highs[j] >= stop_p: r_gain = -1.0; stopped_out = True; break")
    n3 = s.count("if r_gain == -1.0 and highs[min(i+24, n_bars-1)] > stop_p:")
    s = s.replace("if r_gain == -1.0 and highs[min(i+24, n_bars-1)] > stop_p:",
                  "if (not stopped_out) and r_gain == -1.0 and highs[min(i+24, n_bars-1)] > stop_p:")
    n4 = s.count("if r_gain == -1.0 and lows[min(i+24, n_bars-1)] < stop_p:")
    s = s.replace("if r_gain == -1.0 and lows[min(i+24, n_bars-1)] < stop_p:",
                  "if (not stopped_out) and r_gain == -1.0 and lows[min(i+24, n_bars-1)] < stop_p:")
    print("PatchA counts (expect 4 2 2 2 2):", n0, n1, n2, n3, n4)
    assert (n0, n1, n2, n3, n4) == (4, 2, 2, 2, 2)

o = "trade_sleeves = np.zeros(n, dtype=np.int8)\n"
assert s.count(o) == 1
s = s.replace(o, o + "    trade_evidx = np.zeros(n, dtype=np.int64)\n")
o = "trade_sleeves[tr_count] = slv\n"
assert s.count(o) == 1
s = s.replace(o, o + "        trade_evidx[tr_count] = i\n")
o = ("return equity - capital, max_dd_pct, tr_count, win_count, s1_tr, t1_tr, orb_tr, s2_tr, "
     "trade_pnls[:tr_count], trade_times[:tr_count], trade_sleeves[:tr_count]")
assert s.count(o) == 1
s = s.replace(o, o + ", trade_evidx[:tr_count]")
o = ("net_pnl, max_dd, tr_count, win_count, s1_tr, t1_tr, orb_tr, s2_tr, tr_pnls, tr_times, tr_sleeves "
     "= simulate_elite_portfolio(")
assert s.count(o) == 1
s = s.replace(o, ("net_pnl, max_dd, tr_count, win_count, s1_tr, t1_tr, orb_tr, s2_tr, tr_pnls, tr_times, "
                  "tr_sleeves, tr_evidx = simulate_elite_portfolio("))
o = """        for tp, tt, ts in zip(tr_pnls, tr_times, tr_sleeves):
            all_executed_trades.append({
                "window_id": w_id, "time": int(tt), "pnl": float(tp), "sleeve": int(ts)
            })"""
assert s.count(o) == 1
s = s.replace(o, """        for tp, tt, ts, te in zip(tr_pnls, tr_times, tr_sleeves, tr_evidx):
            _ev = combined[int(te)]
            all_executed_trades.append({
                "window_id": w_id, "time": int(tt), "pnl": float(tp), "sleeve": int(ts),
                "symbol": str(_ev["symbol"]), "strategy": str(_ev["strategy"]),
                "r_gain": float(_ev["r_gain"]), "risk": float(_ev["risk"]), "prob": float(_ev["prob"])
            })""")
p.write_text(s)
print("PatchB (tracing) applied OK ->", p)
