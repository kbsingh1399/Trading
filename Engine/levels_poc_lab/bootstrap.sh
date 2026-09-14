#!/usr/bin/env bash
# Rebuild the lab environment after a sandbox reset (venv + deps + derived caches).
set -e
cd "$(dirname "$0")/../.."
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip >/dev/null 2>&1
.venv/bin/pip install -q pandas numpy numba lightgbm scikit-learn pyarrow >/dev/null 2>&1
if [ "$(ls /tmp/lpl_cache/*_bw0.00050.parquet 2>/dev/null | wc -l)" -lt 18 ]; then
  .venv/bin/python - <<'PY'
import os
from Engine.levels_poc_lab.data import build_symbol_features, _downcast, ALL_SYMBOLS, CACHE_DIR
os.makedirs(CACHE_DIR, exist_ok=True)
for s in ALL_SYMBOLS:
    f = build_symbol_features(s); _downcast(f)
    f.to_parquet(CACHE_DIR / f"{s}_bw0.00050.parquet", index=False)
PY
fi
echo "lab environment ready"
