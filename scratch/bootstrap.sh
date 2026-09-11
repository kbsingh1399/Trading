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
# hunt resume support: variant pools + hunt deps
if [ -d scratch/hunt ] && [ -f scratch/hunt/optuna_hunt.db ]; then echo "[bootstrap] hunt state present, leaving intact"; fi
for PR in taker41 maker25; do
  if [ ! -f "scratch/variant_pool_${PR}.parquet" ]; then
    for GG in SURV_L SURV_XL; do
      SURV_ONLY=1 GEO_OVR=$GG PROFILE=$PR .venv/bin/python -u scratch/strategy_battery.py > scratch/battery_${PR}_${GG}.log 2>&1
    done
    PROFILE=$PR .venv/bin/python -u scratch/build_variant_pools.py
  fi
done
