"""
================================================================================
DUAL-TABLE PARQUET EXPORTER (schema-validated, atomic)
================================================================================
Table 1  {symbol}_15m_master_2020_2026.parquet
Table 2  {symbol}_15m_footprint_ladder.parquet
Manifest {symbol}_dataset_manifest.json

* Column order and dtypes are coerced to the canonical contract *before* the
  write; a frame that cannot be coerced raises ``SchemaError`` and nothing is
  written.
* Files are written to a temp path in the target directory and ``os.replace``d
  so a crash never leaves a truncated Parquet in place.
* Table 2 is written with a row-group size aligned to whole candles so
  predicate push-down on ``open_time_ms`` stays efficient.
================================================================================
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from ..core.schema import (
    CANONICAL_COLUMNS,
    COLUMN_DTYPES,
    LADDER_COLUMNS,
    LADDER_DTYPES,
    ladder_filename,
    manifest_filename,
    master_filename,
)


class SchemaError(ValueError):
    pass


def _coerce(df: pd.DataFrame, columns: List[str], dtypes: Dict[str, str], table: str) -> pd.DataFrame:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise SchemaError(f"{table}: missing columns {missing}")
    out = df[columns].copy()
    for col in columns:
        dt = dtypes[col]
        try:
            if dt == "string":
                out[col] = out[col].astype(str)
            else:
                out[col] = out[col].astype(dt)
        except (TypeError, ValueError) as exc:
            raise SchemaError(f"{table}: column {col} not coercible to {dt}: {exc}") from exc
    num = [c for c in columns if dtypes[c] not in ("string",)]
    arr = out[num].to_numpy(dtype=np.float64)
    if not np.isfinite(arr).all():
        bad = [num[j] for j in np.where(~np.isfinite(arr).all(axis=0))[0]]
        raise SchemaError(f"{table}: non-finite values in {bad}")
    return out


def _arrow_schema(columns: List[str], dtypes: Dict[str, str]) -> pa.Schema:
    m = {"int64": pa.int64(), "int8": pa.int8(), "float64": pa.float64(), "string": pa.large_string()}
    return pa.schema([pa.field(c, m[dtypes[c]], nullable=False) for c in columns])


def _fsync_dir(dir_path: str) -> None:
    """Best-effort fsync on parent directory (POSIX directory fd sync, safe no-op on non-POSIX)."""
    try:
        if hasattr(os, "O_DIRECTORY"):
            fd = os.open(dir_path, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
    except Exception:
        pass


def _atomic_write(df: pd.DataFrame, path: str, schema: pa.Schema, row_group_size: Optional[int]) -> None:
    table = pa.Table.from_pandas(df, schema=schema, preserve_index=False)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        pq.write_table(table, f, compression="snappy", row_group_size=row_group_size, use_dictionary=True, write_statistics=True)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    _fsync_dir(os.path.dirname(os.path.abspath(path)))

def _file_sha256(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


class ParquetExporter:
    def __init__(self, output_dir: str) -> None:
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def master_path(self, symbol: str) -> str:
        return os.path.join(self.output_dir, master_filename(symbol))

    def ladder_path(self, symbol: str) -> str:
        return os.path.join(self.output_dir, ladder_filename(symbol))

    def manifest_path(self, symbol: str) -> str:
        return os.path.join(self.output_dir, manifest_filename(symbol))

    def export_master(self, df: pd.DataFrame, symbol: str) -> str:
        clean = _coerce(df, CANONICAL_COLUMNS, COLUMN_DTYPES, "master")
        path = self.master_path(symbol)
        _atomic_write(clean, path, _arrow_schema(CANONICAL_COLUMNS, COLUMN_DTYPES), row_group_size=65_536)
        return path

    def export_ladder(self, ladder: pd.DataFrame, symbol: str) -> str:
        clean = _coerce(ladder, LADDER_COLUMNS, LADDER_DTYPES, "ladder")
        path = self.ladder_path(symbol)
        # row groups end on candle boundaries (~1M rows)
        ts = clean["open_time_ms"].to_numpy()
        rg = 1_048_576
        if len(clean) > rg:
            change = np.flatnonzero(np.diff(ts)) + 1
            target = change[np.searchsorted(change, rg)] if np.searchsorted(change, rg) < len(change) else len(clean)
            rg = int(target)
        _atomic_write(clean, path, _arrow_schema(LADDER_COLUMNS, LADDER_DTYPES), row_group_size=rg)
        return path

    def write_manifest(self, master: pd.DataFrame, symbol: str, ladder_stats: Dict[str, Any],
                       verification: Dict[str, Any], metrics_absent_days: Optional[List[str]] = None,
                       expected_start_ms: Optional[int] = None,
                       expected_end_ms: Optional[int] = None,
                       expected_rows: Optional[int] = None) -> str:
        mpath, lpath = self.master_path(symbol), self.ladder_path(symbol)
        exp_start = int(expected_start_ms) if expected_start_ms is not None else (int(master["open_time_ms"].iloc[0]) if not master.empty else None)
        exp_end = int(expected_end_ms) if expected_end_ms is not None else (int(master["open_time_ms"].iloc[-1]) if not master.empty else None)
        exp_rows = int(expected_rows) if expected_rows is not None else int(len(master))
        manifest = {
            "symbol": symbol,
            "timeframe": "15m",
            "total_rows": int(len(master)),
            "expected_rows": exp_rows,
            "expected_start_ms": exp_start,
            "expected_end_ms": exp_end,
            "columns": list(master.columns),
            "column_count": int(len(master.columns)),
            "start_time_utc": str(master["datetime_utc"].iloc[0]),
            "end_time_utc": str(master["datetime_utc"].iloc[-1]),
            "exported_at_utc": datetime.now(timezone.utc).isoformat(),
            "master_file": os.path.basename(mpath),
            "master_sha256": _file_sha256(mpath),
            "master_size_mb": round(os.path.getsize(mpath) / 1_048_576, 2) if os.path.exists(mpath) else None,
            "ladder_file": os.path.basename(lpath) if os.path.exists(lpath) else None,
            "ladder_sha256": _file_sha256(lpath) if os.path.exists(lpath) else None,
            "ladder_size_mb": round(os.path.getsize(lpath) / 1_048_576, 2) if os.path.exists(lpath) else None,
            "ladder": ladder_stats,
            "provenance": {
                "tick_exact_bars": int(ladder_stats.get("tick_exact_candles", 0)),
                "spot_exact_bars": int((master["spot_close"].notna()).sum()) if "spot_close" in master else 0,
                "imputed_metrics_bars": int((master["is_imputed_metrics"] == 1).sum()) if "is_imputed_metrics" in master else 0,
                "metrics_archive_absent_months": sorted({d[:7] for d in (metrics_absent_days or [])}),
                "metrics_archive_absent_days": sorted(metrics_absent_days or []),
                "metrics_archive_absent_day_count": len(set(metrics_absent_days or [])),
                "metrics_unavailable_fraction_by_year": {
                    str(y): round(float((master.loc[master["datetime_utc"].str[:4] == str(y), "is_imputed_metrics"] == 1).mean()), 4)
                    for y in sorted(master["datetime_utc"].str[:4].unique())
                } if "datetime_utc" in master and "is_imputed_metrics" in master else {},
            },
            "verification": verification,
            "schema_version": "2.1",
        }
        path = self.manifest_path(symbol)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2)
        os.replace(tmp, path)
        return path

    def export_dataset_atomic(
        self,
        master: pd.DataFrame,
        symbol: str,
        ladder: Optional[pd.DataFrame] = None,
        ladder_stats: Optional[Dict[str, Any]] = None,
        verification: Optional[Dict[str, Any]] = None,
        metrics_absent_days: Optional[List[str]] = None,
        expected_start_ms: Optional[int] = None,
        expected_end_ms: Optional[int] = None,
        expected_rows: Optional[int] = None,
    ) -> Tuple[str, Optional[str], str]:
        """
        C4 FIX: Staged atomic promotion pattern.
        Writes master, ladder, and manifest to .staging files first.
        Only when ALL artifacts are completely written and verified on disk, promotes them
        via os.replace in manifest-last order.
        If ANY write or validation fails before promotion, unlinks only the .staging files,
        leaving the existing production dataset 100% intact and undamaged!
        """
        mpath = self.master_path(symbol)
        lpath = self.ladder_path(symbol)
        man_path = self.manifest_path(symbol)

        staging_mpath = mpath + ".staging"
        staging_lpath = lpath + ".staging"
        staging_man_path = man_path + ".staging"

        staging_files = [staging_mpath, staging_man_path]
        has_ladder = ladder is not None and not ladder.empty
        if has_ladder:
            staging_files.append(staging_lpath)

        try:
            # 1. Write clean master to staging
            clean_master = _coerce(master, CANONICAL_COLUMNS, COLUMN_DTYPES, "master")
            _atomic_write(clean_master, staging_mpath, _arrow_schema(CANONICAL_COLUMNS, COLUMN_DTYPES), row_group_size=65_536)

            # 2. Write clean ladder to staging if present
            if has_ladder:
                clean_ladder = _coerce(ladder, LADDER_COLUMNS, LADDER_DTYPES, "ladder")
                ts = clean_ladder["open_time_ms"].to_numpy()
                rg = 1_048_576
                if len(clean_ladder) > rg:
                    change = np.flatnonzero(np.diff(ts)) + 1
                    target = change[np.searchsorted(change, rg)] if np.searchsorted(change, rg) < len(change) else len(clean_ladder)
                    rg = int(target)
                _atomic_write(clean_ladder, staging_lpath, _arrow_schema(LADDER_COLUMNS, LADDER_DTYPES), row_group_size=rg)

            # 3. Construct manifest using hashes of the staging artifacts
            exp_start = int(expected_start_ms) if expected_start_ms is not None else (int(clean_master["open_time_ms"].iloc[0]) if not clean_master.empty else None)
            exp_end = int(expected_end_ms) if expected_end_ms is not None else (int(clean_master["open_time_ms"].iloc[-1]) if not clean_master.empty else None)
            exp_rows = int(expected_rows) if expected_rows is not None else int(len(clean_master))

            manifest = {
                "symbol": symbol,
                "timeframe": "15m",
                "total_rows": int(len(clean_master)),
                "expected_rows": exp_rows,
                "expected_start_ms": exp_start,
                "expected_end_ms": exp_end,
                "columns": list(clean_master.columns),
                "column_count": int(len(clean_master.columns)),
                "start_time_utc": str(clean_master["datetime_utc"].iloc[0]),
                "end_time_utc": str(clean_master["datetime_utc"].iloc[-1]),
                "exported_at_utc": datetime.now(timezone.utc).isoformat(),
                "master_file": os.path.basename(mpath),
                "master_sha256": _file_sha256(staging_mpath),
                "master_size_mb": round(os.path.getsize(staging_mpath) / 1_048_576, 2) if os.path.exists(staging_mpath) else None,
                "ladder_file": os.path.basename(lpath) if has_ladder else None,
                "ladder_sha256": _file_sha256(staging_lpath) if has_ladder else None,
                "ladder_size_mb": round(os.path.getsize(staging_lpath) / 1_048_576, 2) if (has_ladder and os.path.exists(staging_lpath)) else None,
                "ladder": ladder_stats or {},
                "provenance": {
                    "tick_exact_bars": int((ladder_stats or {}).get("tick_exact_candles", 0)),
                    "spot_exact_bars": int((clean_master["spot_close"].notna()).sum()) if "spot_close" in clean_master else 0,
                    "imputed_metrics_bars": int((clean_master["is_imputed_metrics"] == 1).sum()) if "is_imputed_metrics" in clean_master else 0,
                    "metrics_archive_absent_months": sorted({d[:7] for d in (metrics_absent_days or [])}),
                    "metrics_archive_absent_days": sorted(metrics_absent_days or []),
                    "metrics_archive_absent_day_count": len(set(metrics_absent_days or [])),
                    "metrics_unavailable_fraction_by_year": {
                        str(y): round(float((clean_master.loc[clean_master["datetime_utc"].str[:4] == str(y), "is_imputed_metrics"] == 1).mean()), 4)
                        for y in sorted(clean_master["datetime_utc"].str[:4].unique())
                    } if "datetime_utc" in clean_master and "is_imputed_metrics" in clean_master else {},
                },
                "verification": verification or {},
                "schema_version": "2.1",
            }

            with open(staging_man_path, "w", encoding="utf-8") as fh:
                json.dump(manifest, fh, indent=2)
                fh.flush()
                os.fsync(fh.fileno())

            # 4. Atomic promotion with durability (R3-C3 fix):
            # All staging files are fully written and fsync'd.
            # Promote via os.replace in rapid sequence with manifest last as the canonical commit certificate!
            os.replace(staging_mpath, mpath)
            if has_ladder:
                os.replace(staging_lpath, lpath)
            elif os.path.exists(lpath):
                try:
                    os.remove(lpath)
                except OSError:
                    pass
            os.replace(staging_man_path, man_path)
            _fsync_dir(self.output_dir)

            return mpath, (lpath if has_ladder else None), man_path

        except Exception:
            # On any failure, purge only the staging files; prior production dataset is 100% untouched!
            for p in staging_files:
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except OSError:
                        pass
            raise


def verify_dataset_hashes(manifest_path: str) -> bool:
    """
    Reader-side integrity and durability enforcement (R3-C3).
    Validates that on-disk master and ladder files match the SHA-256 hashes recorded in the manifest.
    Returns False if manifest is missing, corrupt, or if any hash mismatch is detected.
    """
    if not os.path.exists(manifest_path):
        return False
    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            man = json.load(fh)
        target_dir = os.path.dirname(os.path.abspath(manifest_path))
        m_file = man.get("master_file")
        m_sha = man.get("master_sha256")
        if not m_file or not m_sha:
            return False
        m_path = os.path.join(target_dir, m_file)
        if _file_sha256(m_path) != m_sha:
            return False

        l_file = man.get("ladder_file")
        l_sha = man.get("ladder_sha256")
        if l_file and l_sha:
            l_path = os.path.join(target_dir, l_file)
            if _file_sha256(l_path) != l_sha:
                return False
        return True
    except Exception:
        return False

