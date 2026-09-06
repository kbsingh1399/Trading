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


# ---------------------------------------------------------------------------
# Helpers for verify_symbol negative tests (no full pipeline needed)
# ---------------------------------------------------------------------------

def _write_synthetic_pair(d: str, sym: str, n_rows: int = 100) -> dict:
    """Write a minimal but schema-valid master + ladder + manifest.

    Returns the manifest dict so callers can mutate specific fields.
    """
    import hashlib
    import numpy as np
    import Engine.run_historical_pipeline as rp
    from Engine.core.schema import (
        BAR_MS, CANONICAL_COLUMNS, COLUMN_DTYPES,
        LADDER_COLUMNS, LADDER_DTYPES,
        ladder_filename, manifest_filename, master_filename,
    )
    import pyarrow as pa
    import pyarrow.parquet as pq

    # --- master ---
    t0 = 1_609_459_200_000  # 2021-01-01 00:00 UTC
    ts = np.arange(t0, t0 + n_rows * BAR_MS, BAR_MS, dtype=np.int64)
    master_data = {}
    for col in CANONICAL_COLUMNS:
        dtype = COLUMN_DTYPES.get(col, "float64")
        if dtype in ("int64", "int32", "int16", "int8"):
            master_data[col] = np.zeros(n_rows, dtype=np.int64)
        elif dtype == "float64":
            master_data[col] = np.ones(n_rows, dtype=np.float64)
        else:  # object / string
            master_data[col] = [""] * n_rows
    master_data["open_time_ms"] = ts
    master_data["close_time_ms"] = ts + 899_999
    master_data["symbol"] = [sym] * n_rows
    master_data["datetime_utc"] = ["2021-01-01 00:00:00"] * n_rows
    if "spot_flow_source" in CANONICAL_COLUMNS:
        master_data["spot_flow_source"] = ["UNAVAILABLE"] * n_rows
    master_df = pd.DataFrame(master_data)[CANONICAL_COLUMNS]

    mpath = os.path.join(d, master_filename(sym))
    master_df.to_parquet(mpath, index=False)

    # --- ladder ---
    ladder_data = {}
    for col in LADDER_COLUMNS:
        dtype = LADDER_DTYPES.get(col, "float64")
        if dtype in ("int64", "int32", "int16", "int8"):
            ladder_data[col] = np.zeros(5, dtype=np.int64)
        elif dtype == "float64":
            ladder_data[col] = np.ones(5, dtype=np.float64)
        else:
            ladder_data[col] = [""] * 5
    ladder_data["open_time_ms"] = ts[:5]
    ladder_df = pd.DataFrame(ladder_data)[LADDER_COLUMNS]
    lpath = os.path.join(d, ladder_filename(sym))
    ladder_df.to_parquet(lpath, index=False)

    # --- hashes ---
    def _sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    exp_start_ms = int(ts[0])
    exp_end_ms = int(ts[-1])
    calc_rows = int((((exp_end_ms // BAR_MS) * BAR_MS) - ((exp_start_ms // BAR_MS) * BAR_MS)) // BAR_MS + 1)

    manifest = {
        "schema_version": "2.1",
        "symbol": sym,
        "master_file": os.path.basename(mpath),
        "ladder_file": os.path.basename(lpath),
        "master_sha256": _sha(mpath),
        "ladder_sha256": _sha(lpath),
        "total_rows": n_rows,
        "expected_rows": calc_rows,
        "expected_start_ms": exp_start_ms,
        "expected_end_ms": exp_end_ms,
        "verification": {"passed": True, "agent_status": {}},
    }
    ppath = os.path.join(d, manifest_filename(sym))
    with open(ppath, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh)
    return manifest


def _vs(d, sym):
    """Thin wrapper so test bodies read cleanly."""
    from Engine.verification.verify_parquet_integrity import verify_symbol
    return verify_symbol(d, sym, log=QUIET)


def test_verify_symbol_negative_contracts() -> None:
    print("\n6. verify_symbol: manifest-contract negative cases")
    from Engine.core.schema import manifest_filename

    SYM = "DOGEUSDT"
    with tempfile.TemporaryDirectory() as d:
        # 6a baseline — synthetic pair must pass verify_symbol so we know the helper works.
        _write_synthetic_pair(d, SYM)
        # NOTE: a synthetic pair will likely fail Agent1/Agent2 math checks; what we are
        # testing here is that the Council:ManifestContract layer fires correctly for each
        # tampered field.  We patch the manifest after the parquets are written.
        ppath = os.path.join(d, manifest_filename(SYM))

        def _reload():
            with open(ppath, encoding="utf-8") as fh:
                return json.load(fh)

        def _dump(m):
            with open(ppath, "w", encoding="utf-8") as fh:
                json.dump(m, fh)

        good = _reload()

        # 6a: missing manifest file
        os.remove(ppath)
        rep = _vs(d, SYM)
        check("6a missing_manifest -> passed=False", not rep.passed)
        check("6a check key is 'missing_manifest'",
              any(f.check == "missing_manifest" for f in rep.findings))

        # 6b: corrupt (non-JSON) manifest
        with open(ppath, "w") as fh:
            fh.write("{not valid json")
        rep = _vs(d, SYM)
        check("6b corrupt JSON -> passed=False", not rep.passed)
        check("6b check key is 'unreadable_manifest'",
              any(f.check == "unreadable_manifest" for f in rep.findings))

        # 6c: expected_rows is None
        m = dict(good); m["expected_rows"] = None; _dump(m)
        rep = _vs(d, SYM)
        check("6c expected_rows=None -> passed=False", not rep.passed)
        check("6c check key is 'manifest_expected_rows'",
              any(f.check == "manifest_expected_rows" for f in rep.findings))

        # 6d: expected_rows is a string instead of int
        m = dict(good); m["expected_rows"] = "lots"; _dump(m)
        rep = _vs(d, SYM)
        check("6d expected_rows='lots' -> passed=False", not rep.passed)
        check("6d check key is 'manifest_expected_rows'",
              any(f.check == "manifest_expected_rows" for f in rep.findings))

        # 6e: expected_start_ms missing
        m = dict(good); del m["expected_start_ms"]; _dump(m)
        rep = _vs(d, SYM)
        check("6e missing expected_start_ms -> passed=False", not rep.passed)
        check("6e check key is 'manifest_expected_start'",
              any(f.check == "manifest_expected_start" for f in rep.findings))

        # 6f: expected_rows mathematically inconsistent with start/end
        m = dict(good); m["expected_rows"] = good["expected_rows"] + 9999; _dump(m)
        rep = _vs(d, SYM)
        check("6f rows math inconsistent -> passed=False", not rep.passed)
        check("6f check key is 'manifest_rows_inconsistent'",
              any(f.check == "manifest_rows_inconsistent" for f in rep.findings))

        # 6g: master actual row count != expected_rows (restore good manifest, truncate parquet)
        _dump(good)
        from Engine.core.schema import master_filename
        master_df = pd.read_parquet(os.path.join(d, master_filename(SYM)))
        truncated = master_df.iloc[:10]
        truncated.to_parquet(os.path.join(d, master_filename(SYM)), index=False)
        rep = _vs(d, SYM)
        check("6g master row count mismatch -> passed=False", not rep.passed)
        check("6g check key is 'master_rows_mismatch'",
              any(f.check == "master_rows_mismatch" for f in rep.findings))

        # 6h: ladder missing (verify_symbol must refuse — ladder is unconditionally mandatory)
        _write_synthetic_pair(d, SYM)  # restore full pair
        from Engine.core.schema import ladder_filename
        os.remove(os.path.join(d, ladder_filename(SYM)))
        rep = _vs(d, SYM)
        check("6h missing ladder -> passed=False", not rep.passed)
        check("6h check key is 'missing_ladder'",
              any(f.check == "missing_ladder" for f in rep.findings))


def test_null_ladder_file_in_manifest_cannot_bypass_fast_skip() -> None:
    print("\n7. SOL regression: manifest[ladder_file]=null must NOT grant fast-skip")
    SYM = "DOGEUSDT"
    with tempfile.TemporaryDirectory() as d:
        # Build a full certified artifact first.
        ok = _run(d, None)
        if not ok:
            check("baseline run succeeded (required for regression)", False)
            return
        check("baseline: export succeeded", ok is True)
        check("baseline: fast-skip accepts it",
              rp.existing_output_is_current(d, SYM, max_age_hours=1e9))

        # Now mutate the manifest to set ladder_file to null — the SOL-identified bypass.
        from Engine.core.schema import manifest_filename
        ppath = os.path.join(d, manifest_filename(SYM))
        with open(ppath, encoding="utf-8") as fh:
            m = json.load(fh)
        m["ladder_file"] = None
        with open(ppath, "w", encoding="utf-8") as fh:
            json.dump(m, fh)

        check("ladder_file=null in manifest -> fast-skip REJECTED (not current)",
              not rp.existing_output_is_current(d, SYM, max_age_hours=1e9))


if __name__ == "__main__":
    print("=" * 92)
    print("Fail-closed export gate + verify_symbol negative contracts")
    print("=" * 92)
    test_manifest_failure_leaves_no_partial_artifacts()
    test_exporter_honour_leaves_a_certified_pair()
    test_certificate_is_what_grants_the_skip()
    test_manifest_hash_and_ladder_contract()
    test_corrupt_archive_raises_archive_parse_error()
    test_verify_symbol_negative_contracts()
    test_null_ladder_file_in_manifest_cannot_bypass_fast_skip()
    print("\n" + "=" * 92)
    print(f"{sum(results)}/{len(results)} assertions passed")
    print("=" * 92)
    sys.exit(0 if all(results) else 1)
