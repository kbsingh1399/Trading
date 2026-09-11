#!/bin/bash
# Post-wipe bootstrap: env + data cache + union pools. Idempotent. ~5 min.
cd "$(dirname "$0")/.."
set -e
[ -x .venv/bin/python ] || { python3 -m venv .venv && .venv/bin/pip install --only-binary=:all: --quiet numpy pandas pyarrow numba lightgbm hmmlearn optuna scikit-learn; }
[ -f scratch/cache_battery_v2.pkl ] || { echo "[bootstrap] rebuilding store cache..."; .venv/bin/python -c "
import sys; from pathlib import Path; sys.path.insert(0,'.')
from scratch.strategy_battery import get_store
get_store(); print('[bootstrap] cache ready')"; }
for PR in taker41 maker25 maker35; do
  if [ ! -f "scratch/union_pool_v2_${PR}.parquet" ]; then
    echo "[bootstrap] battery+pool gen $PR"
    PROFILE=$PR .venv/bin/python -u scratch/strategy_battery.py > scratch/battery_stage1_v2_${PR}.log 2>&1
    PROFILE=$PR .venv/bin/python -u scratch/rebuild_union.py
  fi
done
echo "[bootstrap] DONE"
