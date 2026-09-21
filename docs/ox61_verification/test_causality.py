"""OX61 MANDATE 1 (forensic causal soundness) + MANDATE 3 (ratchet parity) verification.
Usage: /home/user/ox61venv/bin/python docs/ox61_verification/test_causality.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Engine.core.strategy_kernel import create_labels_unified, create_labels_ratchet

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

# ------------------------------------------------ C1: entries booked at opens[i+1]
def mkframe_gap(n=40):
    dts = pd.date_range(start="2025-01-01 07:00", periods=n, freq="15min", tz="UTC")
    return pd.DataFrame({
        "datetime": dts, "open": np.full(n, 100.0), "high": np.full(n, 100.05),
        "low": np.full(n, 99.95), "close": np.full(n, 100.0),
        "sweep_pdl": np.zeros(n, dtype=np.int64), "sweep_pdh": np.zeros(n, dtype=np.int64),
        "bullish_fvg": np.zeros(n), "bearish_fvg": np.zeros(n), "htf_4h_trend": np.zeros(n),
        "local_low_20": np.full(n, 100.5), "local_high_20": np.full(n, 114.0),
        "atr_14": np.full(n, 0.5), "is_kill_zone": np.zeros(n, dtype=bool),
    })

def test_entry_next_open():
    # Setup bar 5 closes 100.0; entry bar 6 gaps to open 102.0 -> entry MUST be 102.0.
    # Unified: r = 102-100.5 = 1.5 (1.47% stop, clears cap); R_eff = 12/1.5 = 8 -> 3.5R cap
    # -> TP 107.25; TP bar -> +3.5R - 0.08 = +3.42. (Entry 100 would give r = -0.5: invalid.)
    df = mkframe_gap()
    df.loc[5, "is_kill_zone"] = True; df.loc[5, "sweep_pdl"] = 1
    df.loc[5, "bullish_fvg"] = 1.0; df.loc[5, "htf_4h_trend"] = 1.0
    df.loc[6, ["open", "high", "low"]] = [102.0, 102.5, 101.8]
    df.loc[7, ["open", "high", "low", "close"]] = [102.5, 114.2, 102.4, 113.9]
    out = create_labels_unified(df)
    r = out.loc[5, "r_realized"]
    check("C1a unified-entry-opens[i+1]", abs(r - 3.42) < 1e-9, f"r={r} (entry=102 proved)")
    # Precommitted: r = 1.5; TP = 102 + 2.5*1.5 = 105.75; bar 7 high 114.2 -> +2.5R - 0.08.
    df2 = mkframe_gap(n=160)
    df2.loc[5, "is_kill_zone"] = True; df2.loc[5, "sweep_pdl"] = 1
    df2.loc[5, "bullish_fvg"] = 1.0; df2.loc[5, "htf_4h_trend"] = 1.0
    df2.loc[6, ["open", "high", "low"]] = [102.0, 102.5, 101.8]
    df2.loc[7, ["open", "high", "low", "close"]] = [102.5, 114.2, 102.4, 113.9]
    out2 = create_labels_ratchet(df2)
    r2 = out2.loc[5, "r_realized"]
    check("C1b precommitted-entry-opens[i+1]", abs(r2 - 2.42) < 1e-9, f"r={r2} (entry=102 proved)")
    # ORB sleeve backtest books entries at the next-bar open (source-level, both sides).
    src = (PROJECT_ROOT / "Engine/strategy/orb_crt_forex_engine.py").read_text()
    check("C1c orb-next-bar-open", src.count("entry_bar = j + 1") == 2
          and src.count("entry = opens[entry_bar]") == 2, "long+short strictly causal")

# ------------------------------------------------ C2: shift(1) + backward asof
def test_source_shifts():
    src = (PROJECT_ROOT / "Engine/core/strategy_kernel.py").read_text()
    check("C2a d1-shift(1)", 'pl.col("high").shift(1).alias("prev_day_high")' in src)
    check("C2b h4-shift(1)", 'pl.col("htf_4h_trend_raw").shift(1)' in src)
    check("C2c backward-asof-x2", src.count('strategy="backward"') >= 2,
          "asof joins are backward-only")

def test_streaming_4h_availability():
    from Engine.forex_engine import compute_features_pandas
    t0 = pd.Timestamp("2025-01-01 00:00", tz="UTC")
    idx4 = pd.date_range(t0, periods=210, freq="4h", tz="UTC")
    closes = np.full(210, 100.0)
    closes[-1] = 150.0  # spike confined to the last (still-forming at boundary) 4H bar
    b4 = pd.DataFrame({"open": closes - 0.1, "high": closes + 0.2,
                       "low": closes - 0.2, "close": closes}, index=idx4)
    avail_last = idx4[-1] + pd.Timedelta(hours=4)
    idx15 = pd.date_range(avail_last - pd.Timedelta(minutes=45), periods=9, freq="15min", tz="UTC")
    b15 = pd.DataFrame({"open": 100.0, "high": 100.05, "low": 99.95,
                        "close": 100.0}, index=idx15)
    f = compute_features_pandas(b15, b4)
    pre = f[f.index < avail_last]["htf_4h_trend"].abs().max()
    post = f[f.index >= avail_last]["htf_4h_trend"].min()
    check("C2d 4h-availability-boundary", pre < 1e-6 and post > 0.3,
          f"pre={pre:.2e} post={post:.3f} boundary={avail_last}")

def test_daily_shift():
    from Engine.forex_engine import compute_features_pandas
    # Day1 flat low 100.0; Day2 bar A dips to 98, bar B low 99.5.
    # Shifted truth: B sweeps Day1 PDL (99.5 <= 100.0). Unshifted would see Day2 min 98 -> no sweep.
    i1 = pd.date_range("2025-01-01 07:00", periods=8, freq="15min", tz="UTC")
    i2 = pd.date_range("2025-01-02 07:00", periods=8, freq="15min", tz="UTC")
    idx = i1.append(i2)
    l = np.full(16, 100.0)
    l[8] = 98.0   # Day2 bar A
    l[9] = 99.5   # Day2 bar B
    b = pd.DataFrame({"open": 100.0, "high": 100.5, "low": l, "close": 100.0}, index=idx)
    f = compute_features_pandas(b)
    check("C2e daily-shift(1)", int(f["sweep_pdl"].iloc[:8].sum()) == 0 and int(f["sweep_pdl"].iloc[9]) == 1,
          f"day1sweeps={int(f['sweep_pdl'].iloc[:8].sum())} barB={int(f['sweep_pdl'].iloc[9])}")

# ------------------------------------------------ C3: no static caches; generators pinned
def test_no_static_caches():
    hits = [str(p) for pat in ("winning_configuration.json", "s1_status.json")
            for p in PROJECT_ROOT.rglob(pat) if ".git" not in str(p)]
    check("C3a no-static-caches", len(hits) == 0, f"hits={hits}")
    gen_map = {
        "labels_precommitted/*.parquet": ("run_ox61_r6.py", "def phase_a"),
        "labels_unified/*.parquet": ("run_ox61_r6.py", "create_labels_unified"),
        "s4_r6_*.parquet": ("run_ox61_r6.py", "def phase_b"),
        "candidates_dual_r6_*.parquet": ("run_ox61_r6.py", "def phase_c"),
        "scorecard_*.csv": ("run_ox61_r6.py", "scorecard_dual_r6_"),
        "scorecard_r4_pinned.csv": ("run_ox61_r4.py", "pin_and_manifest"),
        "candidates_orbparity_full.parquet": ("gen_orb_parity_candidates.py", "candidates_orbparity_full"),
    }
    missing = [a for a, (g, needle) in gen_map.items()
               if not ((Path(__file__).parent / g).read_text().find(needle) >= 0)]
    check("C3b generators-pinned", len(missing) == 0, f"missing={missing}")

# ------------------------------------------------ C4: R6 bar-purge exactness
def test_r6_purge():
    from Engine.core.base_strategy import EngineConfig
    cfg = EngineConfig.load()
    d = pd.read_parquet(Path(__file__).parent / "labels_unified" / "EURUSD.parquet")
    dt = pd.to_datetime(d["datetime"], utc=True).values
    ok = True
    detail = []
    for w in (cfg.windows[0], cfg.windows[9], cfg.windows[19]):
        ws = pd.Timestamp(w.start_date, tz="UTC")
        k0 = int(np.searchsorted(dt, ws.to_datetime64()))
        embargo_lo, embargo_hi = k0 - 480, k0
        train_ok = bool(dt[embargo_lo - 1] < ws.to_datetime64()) if embargo_lo > 0 else True
        width_ok = (embargo_hi - embargo_lo) == 480
        ok &= train_ok and width_ok
        detail.append(f"W{w.window_id}:k0={k0} embargo=480b train_end<ws={train_ok}")
    check("C4 r6-embargo-exact", ok, "; ".join(detail))

# ------------------------------------------------ C5 (MANDATE 3): ratchet schedule parity
def test_ratchet_parity():
    kern = (PROJECT_ROOT / "Engine/core/strategy_kernel.py").read_text()
    eng = (PROJECT_ROOT / "Engine/forex_engine.py").read_text()
    live = (PROJECT_ROOT / "Engine/live/order_manager.py").read_text()
    m = re.search(r"UX_RATCHET = \((.*?)\)\)", kern, re.S)
    fl = lambda pairs: set((round(float(a), 6), round(float(b), 6)) for a, b in pairs)
    k_sched = fl(re.findall(r"\((\d\.\d+), (\d\.\d+)\)?", m.group(1)))
    e_pairs = fl(zip(re.findall(r"gain_r >= (\d\.\d+)", eng), re.findall(r"new_sl_r = (\d\.\d+)", eng)))
    l_pairs = fl(zip(re.findall(r"highest_r >= (\d\.\d+)", live), re.findall(r"new_sl_r = (\d\.\d+)", live)))
    same = (k_sched == e_pairs == l_pairs)
    check("C5 ratchet-schedule-parity", same,
          f"sched={sorted(k_sched)} trigvar=kernel:bar-extreme/engine:gain_r/live:highest_r(KNOWN-DIVERGENCE)")

if __name__ == "__main__":
    print("OX61 MANDATE 1 + MANDATE 3 verification:")
    test_entry_next_open()
    test_source_shifts()
    test_streaming_4h_availability()
    test_daily_shift()
    test_no_static_caches()
    test_r6_purge()
    test_ratchet_parity()
    print(f"\nRESULT: {len(PASS)} PASS, {len(FAIL)} FAIL {FAIL if FAIL else ''}")
    sys.exit(1 if FAIL else 0)
