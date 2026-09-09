# Institutional meta-labeling integration

## Configuration

The confirmed target is 4R and the minimum trade count is 15. The current
`Engine/target_oos_criteria.json` sets ROI > 10%, drawdown < 5%, and win rate > 40%.
The evaluator reads these thresholds directly. Each run records the criteria,
ratchet parameters, source hashes and input parquet hash.

Existing repository risk and ratchet settings are preserved: base risk $55,
defense risk $15, a 4.5% drawdown halt, locks of +0.20R at +0.70R,
+0.75R at +1.20R, and +1.40R at +1.80R. The target is now 4R.
These settings supersede the older 2.5R example for this evaluation.

## Shared execution and label contract

For a primary event at the close of bar t, entry occurs at open[t+1] with
directional entry slippage. R is the event's raw_r price distance, not an
unrelated ATR multiple invented by the labeler. Entry-bar stop and target
checks execute immediately. On an ambiguous OHLC bar, the existing stop is
checked before the target. Newly armed ratchets bind on the next bar.
Exiting intrabar cannot retroactively permit another fill at that bar's open.

The target fill is capped at the configured target, including favorable gaps.
Market and stop exits include adverse exit slippage. Both fills incur fees.
Quantity is based on the all-in expected loss at the initial stop. Realized
gap losses are not clipped to the planned risk or drawdown limit.

The vertical condition is conditional, not a compulsory 24-bar holding limit:

    age >= 24 and direction * (close - entry) / raw_r < 0.20

Age includes the entry bar. Trades surviving this condition can continue until
a stop or target. Events unresolved at the training cutoff are censored and
excluded from training, rather than assigned a loss.

    y_meta = 1 if exit_reason in {TARGET_BAR, TARGET_OPEN} else 0
    label_end < oos_start - 72 hours
    cv_train_label_end < validation_start - 72 hours

Independent setup labels share the kernel's execution rules. Account-level
drawdown halts additionally constrain the realized backtest; they do not
redefine the independent setup label.

## Features and calibration

The classifier sees only primary events. Canonical `zc_div` is a base-volume
difference, so the feature extractor divides it by base volume. Futures
per-bar taker delta divided by volume is used when an explicit
`fp_delta_ratio` column is absent; it does not invent footprint ladder data.
RSI is divided by 100, ATR by close, and volume by its preceding 20-bar mean.
Short-event features are reflected into the long-event coordinate system.
Missing or nonfinite feature rows abstain.

XGBoost uses depth 3, 120 estimators, learning rate 0.03, subsample and column
subsample 0.8, L1 1.5, L2 3.5, minimum child weight 15 and a fixed seed.
Expanding chronological folds generate predictions for sigmoid calibration.
The 0.5 acceptance threshold is fixed before OOS. No OOS quantile, search or
failed-window threshold adjustment occurs. The reported Brier score is the raw
out-of-fold score, not an in-sample score from fitting the calibrator.

Calibration and model parameter references:
[scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html),
[XGBoost parameters](https://xgboost.readthedocs.io/en/stable/parameter.html).

## Integration recipe for all eight strategies

```python
import json
from dataclasses import replace
from pathlib import Path
import pandas as pd

from Engine.core.execution_kernel import RatchetConfig
from Engine.optimize_individual_assets import STRATEGIES, evaluate_window, passes_criteria

engine = Path(r"C:\Users\SIGMA\Documents\Trading\Engine")
criteria = json.loads((engine / "target_oos_criteria.json").read_text())["target_criteria"]
ratchet = replace(RatchetConfig(), min_target_r=criteria["min_r_multiple"])
bars = pd.read_parquet(engine / "binance_backtesting_data/BTCUSDT_15m_master_2020_2026.parquet")

for strategy_class in STRATEGIES:
    result = evaluate_window(
        strategy_class(ratchet_cfg=ratchet), bars,
        pd.Timestamp("2021-05-01", tz="UTC"),
        pd.Timestamp("2021-06-01", tz="UTC"),
    )
    assert passes_criteria(result, criteria), strategy_class.__name__
```

`evaluate_window` generates native primary candidates with historical warmup,
fits only before the purged boundary, filters OOS candidates and resets capital
at the OOS boundary. S1, S2 and all six SMC classes also accept a fitted labeler
through their optional `run(..., meta_labeler=labeler)` argument. The latter
requires callers to supply adequate causal feature warmup.

Run the complete per-asset fail-fast evaluation:

```powershell
python Engine/optimize_individual_assets.py --all-assets
python -m pytest Engine/verification/test_institutional_meta.py -q
```

Reports live in `docs/reviews/meta_labeling`. A missing historical window or
insufficient training support is NOT_EVALUABLE, never a skipped pass. A failed
window terminates that strategy's sequence. The implementation does not certify
upstream model-derived feature provenance or imply that predictive filtering
guarantees the requested returns.

## Verified run: 2026-09-09

- Regression tests: 23 passed.
- Asset-strategy sequences attempted: 144 (18 assets × 8 strategies).
- First-window metric failures: 79; each produced zero accepted trades.
- Insufficient resolved event/class support: 22.
- Insufficient purged calibration support: 11.
- Incomplete or pre-listing first-window coverage: 32.
- Total executed trades: 0. No sequence advanced to window 2.

For example, BTC Edgeful training had 26 target hits among 1,070 resolved
events. This run provides no evidence that the primary setups support the
requested pass criteria. Thresholds were not lowered in response to OOS results.
