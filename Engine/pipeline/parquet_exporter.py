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


def _atomic_write(df: pd.DataFrame, path: str, schema: pa.Schema, row_group_size: Optional[int]) -> None:
    table = pa.Table.from_pandas(df, schema=schema, preserve_index=False)
    tmp = path + ".tmp"
    pq.write_table(table, tmp, compression="snappy", row_group_size=row_group_size, use_dictionary=True, write_statistics=True)
    os.replace(tmp, path)

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
                       verification: Dict[str, Any], metrics_absent_days: Optional[List[str]] = None) -> str:
        mpath, lpath = self.master_path(symbol), self.ladder_path(symbol)
        manifest = {
            "symbol": symbol,
            "timeframe": "15m",
            "total_rows": int(len(master)),
            "columns": list(master.columns),
            "column_count": int(len(master.columns)),
            "start_time_utc": str(master["datetime_utc"].iloc[0]),
            "end_time_utc": str(master["datetime_utc"].iloc[-1]),
            "exported_at_utc": datetime.now(timezone.utc).isoformat(),
            "master_file": os.path.basename(mpath),
            "master_sha256": _file_sha256(mpath),
            "master_size_mb": round(os.path.getsize(mpath) / 1_048_576, 2) if os.path.exists(mpath) else None,
            "ladder_file": os.path.basename(lpath) if os.path.exists(lpath) else None,
            "ladder_sha256": _file_sha256(lpath),
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
