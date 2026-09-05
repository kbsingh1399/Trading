"""
Agent-3 schema-council calibration guard (multi-asset universe).
================================================================================================
Guards the two calibrations that rejected ETHUSDT [2/18] and would reject every asset whose
Binance Vision metrics archive starts after the export window:

  1. regime_dead_feature   -- the year scan must judge ONLY bars the export discloses as
                              carrying metrics; a legitimate pre-archive absence (honestly
                              marked metrics_available=0) is a coverage fact, not a regime.
  2. precision_collapse    -- basis_usd is a bounded *spread* (its cardinality is capped by
                              band width / asset tick) and must never be judged against close
                              cardinality; what must be caught is collapse onto one value.

Both directions are asserted: the false positive must be gone AND the real defect class (§4.1
fabrication, interior download holes, fabricated basis) must still be rejected.

Cases that need a real export are skipped when it is absent (parquets are git-ignored at
b836aa0) -- and case 2 auto-upgrades from an emulated ETHUSDT frame to the REAL ETHUSDT
parquet the moment the batch lands it, so re-run this file right after [2/18] completes.

    python3 Engine/verification/test_schema_calibration.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
REPO_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import Engine.verification.verify_parquet_integrity as vpi  # noqa: E402
from Engine.verification.verify_parquet_integrity import (  # noqa: E402
    agent_microstructure, agent_schema, metrics_coverage_report,
)

DATA_DIR = os.path.join(ENGINE_DIR, "binance_backtesting_data")
CANARY = os.path.join(DATA_DIR, "BTCUSDT_15m_master_2020_2026.parquet")

# exactly what historical_metrics_processor emits when no metrics rows exist for a bar
FALLBACK = {"open_interest_k": 0.0, "open_interest_usd": 0.0, "oi_change_pct": 0.0,
            "ls_ratio_global": 1.0, "ls_ratio_top": 1.0, "top_account_ratio": 1.0,
            "whale_index": 100.0, "ls_count_ratio": 1.0, "ls_volume_ratio": 1.0,
            "top_pos_proportion": 1.0, "top_acct_proportion": 1.0,
            "global_pos_proportion": 1.0, "global_acct_proportion": 1.0}

_checks = []


def check(label: str, cond: bool, detail: str = "") -> None:
    _checks.append((label, bool(cond)))
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if detail:
        print(f"         {detail}")


def _names(findings) -> dict:
    out: dict = {}
    for f in findings:
        out[f.check] = out.get(f.check, 0) + 1
    return out


def _mark_no_metrics(df: pd.DataFrame, mask: np.ndarray) -> pd.DataFrame:
    """Apply the documented fallback values and mark the bars honestly unavailable."""
    for col, val in FALLBACK.items():
        if col in df:
            df.loc[mask, col] = val
    if "taker_volume_ratio" in df:
        df.loc[mask, "taker_volume_ratio"] = 1.0
    df.loc[mask, "metrics_available"] = 0
    df.loc[mask, "is_imputed_metrics"] = 1
    return df


def _year_mask(df: pd.DataFrame, year: int) -> np.ndarray:
    return pd.to_datetime(df["open_time_ms"].to_numpy("int64"), unit="ms", utc=True).year == year


def _slice(df: pd.DataFrame, lo: int, hi: int) -> pd.DataFrame:
    """Contiguous slice re-anchored so index-relative agents see a real file head."""
    out = df.iloc[lo:hi].reset_index(drop=True)
    for c in ("atr_contraction", "squeeze_on", "return_1", "ema_slope_1h", "dist_ema_1h"):
        if c in out:
            out[c] = 0.0
    return out


def main() -> int:
    print("=" * 100)
    print("Agent-3 schema-council calibration guard")
    print("=" * 100)
    if not os.path.exists(CANARY):
        print(f"  SKIP: real export not present ({os.path.basename(CANARY)} is git-ignored)")
        print("        run: python3 Engine/run_historical_pipeline.py --symbol BTCUSDT "
              "--start-date 2020-09-01 --write-parquet")
        return 0
    base = pd.read_parquet(CANARY)
    lad_path = os.path.join(DATA_DIR, "BTCUSDT_15m_footprint_ladder.parquet")
    lad = pd.read_parquet(lad_path) if os.path.exists(lad_path) else None
    print(f"  canary: {len(base):,} real BTCUSDT bars\n")

    # 1 -- no new false positives on the certified canary
    print("1. canary must stay clean")
    check("as-shipped BTCUSDT has no regime_dead_feature",
          "regime_dead_feature" not in _names(agent_schema(base, lad)))
    check("as-shipped BTCUSDT has no precision_collapse",
          "precision_collapse" not in _names(agent_schema(base, lad)))
    check("as-shipped BTCUSDT has no metrics_interior_hole",
          "metrics_interior_hole" not in _names(agent_schema(base, lad)))
    r = metrics_coverage_report(base)
    print(f"         coverage: skipped_years={r['skipped_years']}, "
          f"longest interior hole={r['longest_interior_hole_bars']:,} bars, "
          f"first available={r['metrics_first_available_utc']}")

    # 2 -- the ETHUSDT case: legitimate pre-archive absence must be accepted
    print("\n2. legitimate pre-archive absence must be accepted")
    eth_real = os.path.join(DATA_DIR, "ETHUSDT_15m_master_2020_2026.parquet")
    if os.path.exists(eth_real):
        eth = pd.read_parquet(eth_real)
        src = "REAL ETHUSDT export"
    else:
        eth = _mark_no_metrics(base.copy(), _year_mask(base, 2020))
        src = "emulated on BTCUSDT (metrics rows removed for 2020, marked unavailable)"
    n = _names(agent_schema(eth, lad, attested_months=set()))
    check(f"{src}, UNATTESTED: still rejected -- a metrics-free year is not excused by its own flag",
          "metrics_coverage_unattested" in n and "regime_dead_feature" not in n,
          f"findings={n or 'none'}")
    months = sorted(set(pd.to_datetime(eth.loc[_year_mask(eth, 2020), "open_time_ms"].to_numpy("int64"),
                                       unit="ms", utc=True).strftime("%Y-%m")))
    n_att = _names(agent_schema(eth, lad, attested_months=set(months)))
    check(f"{src}, ATTESTED absent from the archive {months[0]}..{months[-1]}: accepted",
          not n_att, f"findings={n_att or 'none'}")
    check("a skipped year is reported by the coverage report, never silently ignored",
          2020 in metrics_coverage_report(eth)["skipped_years"],
          f"skipped_years={metrics_coverage_report(eth)['skipped_years']}")
    import json as _json
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "BTCUSDT_dataset_manifest.json"), "w") as fh:
            _json.dump({"provenance": {"metrics_archive_absent_months": months + ["2021-04-15"]}}, fh)
        got = vpi._attested_absent_months("BTCUSDT", target_dir=d)
        check("the exemption is read from the manifest the downloader wrote (day keys normalised to months)",
              got == set(months) | {"2021-04"}, f"read {sorted(got)}")
        check("no manifest -> no exemption (fail closed)",
              vpi._attested_absent_months("NOSUCHUSDT", target_dir=d) == set())
        # full contract: what the fetcher records -> what the manifest carries -> what the council reads
        from Engine.pipeline.parquet_exporter import ParquetExporter
        with tempfile.TemporaryDirectory() as d2:
            ParquetExporter(d2).write_manifest(
                eth, "BTCUSDT", {}, {"passed": True},
                metrics_absent_days=[f"{mm}-15" for mm in months])   # one observed 404 day per month
            saved = vpi.DEFAULT_TARGET
            try:
                vpi.DEFAULT_TARGET = d2
                n_mani = _names(agent_schema(eth, lad))              # no explicit kwarg at all
            finally:
                vpi.DEFAULT_TARGET = saved
            check("the exemption works through the real manifest (fetcher -> exporter -> council)",
                  not n_mani, f"findings={n_mani or 'none'}")

    # 3 -- the §4.1 defect class must NOT be weakened
    print("\n3. real fabrication must still be rejected")
    fab = base.copy()
    m20 = _year_mask(fab, 2020)
    for col, val in FALLBACK.items():
        if col in fab:
            fab.loc[m20, col] = val
    fab.loc[m20, "metrics_available"] = 1          # the lie: marked fresh while constant
    fab.loc[m20, "is_imputed_metrics"] = 0
    n = _names(agent_schema(fab, lad, attested_months=set()))
    check("sentinels marked metrics_available=1 still raise regime_dead_feature",
          n.get("regime_dead_feature", 0) >= 6, f"findings={n or 'none'}")
    n_micro = _names(agent_microstructure(fab, lad))
    check("and still raise oi_impossible_zero in Agent 4 (pre-export gate)",
          "oi_impossible_zero" in n_micro, f"agent4={n_micro or 'none'}")

    # 4 -- interior download holes must not pass on the availability flag alone
    print("\n4. interior holes vs contiguous prefix")
    idx = np.arange(len(base))
    hole = _mark_no_metrics(base.copy(), (idx >= 60_000) & (idx < 65_000))
    n = _names(agent_schema(hole, lad))
    check("5,000-bar interior gap with no metrics content is REJECTED",
          "metrics_interior_hole" in n, f"findings={n or 'none'}")
    hole_month = pd.to_datetime(base.loc[62_000, "open_time_ms"], unit="ms", utc=True).strftime("%Y-%m")
    n = _names(agent_schema(hole, lad, attested_months={hole_month}))
    check("an ATTESTED interior gap (source rewrote that archive) is ACCEPTED",
          "metrics_interior_hole" not in n, f"findings={n or 'none'}")
    n = _names(agent_schema(eth, lad, attested_months=set()))
    check("a head gap with no attestation is REJECTED (this is the §4.1 fixture's shape)",
          "metrics_coverage_unattested" in n)
    tail = _mark_no_metrics(base.copy(), np.arange(len(base)) >= len(base) - 5_000)
    n = _names(agent_schema(tail, lad))
    check("a trailing gap (not yet published) is ACCEPTED, not rejected",
          "metrics_interior_hole" not in n, f"findings={n or 'none'}")

    # 5 -- basis precision: category error gone, real collapse still caught
    print("\n5. basis_usd precision")
    rng = np.random.default_rng(7)
    et = base.copy()
    # reproduce the exact cardinalities that killed ETHUSDT: 1,428 distinct basis vs 148,108
    # distinct closes. linspace-mapped rows keep every close value present, so the old rule's
    # threshold lands just above the basis cardinality (0.964% vs its 1.000% cliff).
    closes = np.round(np.linspace(1800.0, 4000.0, 148_108), 2)
    et["close"] = closes[np.linspace(0, len(closes) - 1, len(et)).astype(int)]
    et["basis_usd"] = rng.choice(np.round(np.linspace(-10.5, 13.5, 1428), 2), len(et))
    nu_b, nu_c = int(et["basis_usd"].nunique()), int(et["close"].nunique())
    cliff = max(50, nu_c * 0.01)
    old_fired = nu_b < cliff
    fired = [f for f in agent_schema(et, lad) if f.check == "precision_collapse" and "basis" in f.message]
    check(f"ETH-like {nu_b:,} distinct basis vs {nu_c:,} distinct closes is NOT a defect",
          old_fired and not fired,
          f"pre-patch rule: {nu_b} < {cliff:.0f} -> REJECT | calibrated: no finding "
          f"(margin was {(cliff - nu_b) / cliff:.1%} below an arbitrary cliff)")
    check("the pre-patch rule really did reject this frame (test is not vacuous)", old_fired)
    bz = base.copy()
    bz["basis_usd"] = 0.0
    fired = [f for f in agent_schema(bz, lad) if f.check == "precision_collapse" and "basis" in f.message]
    check("basis_usd collapsed onto one value (spot fabricated from close) IS rejected", bool(fired),
          str(fired[:1] or ""))

    print("\n" + "=" * 100)
    bad = [lab for lab, ok in _checks if not ok]
    print(f"{len(_checks) - len(bad)}/{len(_checks)} calibration assertions passed"
          + (f"   FAILED: {bad}" if bad else ""))
    print("=" * 100)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
