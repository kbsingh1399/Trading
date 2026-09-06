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

from datetime import datetime, timezone

import pandas as pd

ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
REPO_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import Engine.run_historical_pipeline as rp  # noqa: E402
from Engine.core.schema import ladder_filename, manifest_filename, master_filename  # noqa: E402
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

    def fetch_futures_klines(self, *a, **k):
        return self.s[0].copy()

    def fetch_spot_klines(self, *a, **k):
        return self.s[1].copy()

    def fetch_metrics(self, *a, **k):
        return self.s[3].copy()

    def fetch_funding_rates(self, *a, **k):
        return self.s[2].copy()

    def fetch_footprint(self, *a, **k):
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

    def boom(*args, **kwargs):
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


def test_manifest_hash_and_ladder_contract() -> None:
    print("\n4. fast-skip rejects missing/invalid SHA256, file tampering, and missing declared ladders")
    with tempfile.TemporaryDirectory() as d:
        _run(d, None)
        mpath = os.path.join(d, master_filename("DOGEUSDT"))
        lpath = os.path.join(d, ladder_filename("DOGEUSDT"))
        ppath = os.path.join(d, manifest_filename("DOGEUSDT"))

        check("baseline: current", rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))

        with open(ppath, encoding="utf-8") as fh:
            valid_man = json.load(fh)

        # 4a: Missing master_sha256
        man_no_sha = dict(valid_man)
        man_no_sha["master_sha256"] = None
        with open(ppath, "w", encoding="utf-8") as fh:
            json.dump(man_no_sha, fh)
        check("missing master_sha256 -> rejected", not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))

        # 4b: Malformed / short hash
        man_bad_sha = dict(valid_man)
        man_bad_sha["master_sha256"] = "abc123not64hex"
        with open(ppath, "w", encoding="utf-8") as fh:
            json.dump(man_bad_sha, fh)
        check("malformed master_sha256 -> rejected", not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))

        # 4c: Tampered master file bytes
        with open(ppath, "w", encoding="utf-8") as fh:
            json.dump(valid_man, fh)
        with open(mpath, "ab") as fh:
            fh.write(b"\x00\x00\x00corrupt")
        check("tampered master file bytes -> rejected", not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))

        # Restore file by re-running
        _run(d, None)
        check("re-export restored current status", rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))

        # 4d: Ladder deleted when declared in manifest
        check("ladder exists on disk after export", os.path.exists(lpath))
        if os.path.exists(lpath):
            os.remove(lpath)
            check("ladder deleted while declared in manifest -> rejected", not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9))


def test_corrupt_archive_raises_archive_parse_error() -> None:
    print("\n5. corrupt archive (HTTP 200 with invalid zip/csv) raises ArchiveParseError")
    from Engine.pipeline.binance_historical_fetcher import BinanceHistoricalFetcher, ArchiveParseError

    class _FakeHttp:
        def get_optional(self, url: str):
            return b"THIS_IS_NOT_A_VALID_ZIP_ARCHIVE_DATA"

    with tempfile.TemporaryDirectory() as d:
        cf = BinanceHistoricalFetcher(cache_dir=os.path.join(d, "cache"), max_workers=1, http=_FakeHttp(), log=QUIET)
        raised = False
        try:
            cf.fetch_metrics("BTCUSDT", "2024-01-01", now=datetime(2024, 1, 2, tzinfo=timezone.utc))
        except ArchiveParseError as exc:
            raised = True
            check("ArchiveParseError raised on corrupt archive", True, f"{exc}")
        except Exception as exc:
            check(f"Unexpected exception {type(exc).__name__}", False, f"{exc}")
        if not raised:
            check("ArchiveParseError was NOT raised", False)


if __name__ == "__main__":
    print("=" * 92)
    print("Fail-closed export gate")
    print("=" * 92)
    test_manifest_failure_leaves_no_partial_artifacts()
    test_exporter_honour_leaves_a_certified_pair()
    test_certificate_is_what_grants_the_skip()
    test_manifest_hash_and_ladder_contract()
    test_corrupt_archive_raises_archive_parse_error()
    print("\n" + "=" * 92)
    print(f"{sum(results)}/{len(results)} assertions passed")
    print("=" * 92)
    sys.exit(0 if all(results) else 1)
