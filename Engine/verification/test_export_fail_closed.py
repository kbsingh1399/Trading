"""
Fail-closed export gate: a rejected export must leave nothing behind, and no pair of parquets
counts as current without a passing verification certificate.

Reproduces the leak that existed before the fix: `run_pipeline` wrote master + ladder, then
`write_manifest` raised, and the `except SchemaError` branch returned without removing the two
parquets -- leaving never-audited data that `existing_output_is_current()` (which only looked at
the two parquets) would let a later run skip.

    python3 Engine/verification/test_export_fail_closed.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

import pandas as pd

ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
REPO_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import Engine.run_historical_pipeline as rp  # noqa: E402
from Engine.core.schema import master_filename  # noqa: E402
from Engine.core.schema import master_filename  # noqa: E402
from Engine.pipeline.binance_historical_fetcher import build_ladder_from_trades  # noqa: E402
from Engine.pipeline.parquet_exporter import ParquetExporter, SchemaError  # noqa: E402
from Engine.verification.test_pipeline_offline import make_streams, make_trades  # noqa: E402

QUIET = lambda *_a, **_k: None  # noqa: E731
results = []


def check(label, cond, detail=""):
    results.append(bool(cond))
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if detail:
        print(f"         {detail}")


class _FakeFetcher:
    """Mirrors the orchestrator's fetch calls onto synthetic streams."""

    def __init__(self, streams, fp=(None, None)):
        self.s = streams
        self.fp = fp

    def fetch_futures_klines(self, symbol, start_date, now=None):
        return self.s[0].copy()

    def fetch_spot_klines(self, symbol, start_date, now=None):
        return self.s[1].copy()

    def fetch_metrics(self, symbol, start_date, now=None):
        return self.s[3].copy()

    def fetch_funding_rates(self, symbol, start_time_ms):
        return self.s[2].copy()

    def fetch_footprint(self, symbol, start_date, now=None):
        fp_ladder, fp_summary = self.fp
        l_df = fp_ladder.copy() if fp_ladder is not None else pd.DataFrame()
        s_df = fp_summary.copy() if fp_summary is not None else pd.DataFrame()
        return l_df, s_df


def _run(d, boom):
    """Run the orchestrator into d, with write_manifest replaced by `boom` (may raise)."""
    kl, spot, funding, metrics = make_streams(n_bars=96 * 40)
    trades = make_trades(kl.iloc[2000:2050])
    fp_summary, fp_ladder = build_ladder_from_trades(trades, 0.00003)

    fetcher_cls = lambda *a, **k: _FakeFetcher((kl, spot, funding, metrics), fp=(fp_ladder, fp_summary))  # noqa: E731
    orig = (rp.BinanceHistoricalFetcher, ParquetExporter.write_manifest)
    rp.BinanceHistoricalFetcher = fetcher_cls
    if boom is not None:
        ParquetExporter.write_manifest = boom
    try:
        return rp.run_pipeline("DOGEUSDT", start_date_str="2020-09-03", target_dir=d,
                               cache_dir=os.path.join(d, "cache"), max_workers=2, footprint_days=5,
                               run_audit=True, log=QUIET, force=True)
    finally:
        rp.BinanceHistoricalFetcher = orig[0]
        ParquetExporter.write_manifest = orig[1]


def test_manifest_failure_leaves_no_partial_artifacts() -> None:
    print("\n1. a manifest write that dies after the parquets are on disk")

    def boom(self, master, symbol, ladder_stats, verification, metrics_absent_days=None):
        raise SchemaError("simulated: manifest rejected")

    with tempfile.TemporaryDirectory() as d:
        ok = _run(d, boom)
        left = sorted(f for f in os.listdir(d) if not f.startswith("cache"))
        check("run_pipeline returns False (export refused)", ok is False, f"returned {ok!r}")
        check("no master/ladder parquet survives the refusal", not any(f.endswith(".parquet") for f in left),
              f"directory holds: {left}")
        check("and the directory is therefore not skippable on the next run",
              not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))


def test_exporter_honour_leaves_a_certified_pair() -> None:
    print("\n2. control: the same run with a working exporter")
    with tempfile.TemporaryDirectory() as d:
        ok = _run(d, None)
        man = json.load(open(os.path.join(d, "DOGEUSDT_dataset_manifest.json")))
        check("export succeeds", ok is True)
        check("manifest records a passing council", man["verification"]["passed"] is True,
              f"agents={man['verification'].get('agent_status')}")
        check("and the fast-skip gate accepts it as current",
              rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))


def test_certificate_is_what_grants_the_skip() -> None:
    print("\n3. the certificate, not the file mtimes, is what authorises a skip")
    with tempfile.TemporaryDirectory() as d:
        _run(d, None)
        mpath = os.path.join(d, master_filename("DOGEUSDT"))
        ppath = os.path.join(d, "DOGEUSDT_dataset_manifest.json")

        check("baseline: current", rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))
        os.remove(ppath)
        check("manifest deleted -> not current (never-audited data cannot be skipped)",
              not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))

        json.dump({"verification": {"passed": False}}, open(ppath, "w"))
        check("manifest says council FAILED -> not current",
              not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))
        open(ppath, "w").write("{ truncated")
        check("manifest unreadable -> not current (fail closed)",
              not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))
        print(f"         (master on disk throughout: {os.path.exists(mpath)}, "
              f"{os.path.getsize(mpath) / 1_048_576:.1f} MB)")


if __name__ == "__main__":
    print("=" * 92)
    print("Fail-closed export gate")
    print("=" * 92)
    test_manifest_failure_leaves_no_partial_artifacts()
    test_exporter_honour_leaves_a_certified_pair()
    test_certificate_is_what_grants_the_skip()
    print("\n" + "=" * 92)
    print(f"{sum(results)}/{len(results)} assertions passed")
    print("=" * 92)
    sys.exit(0 if all(results) else 1)
