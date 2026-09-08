# RP2 Round 13 — Contract Realignment and Real-Ladder Recovery

## Canonical contract

The runner must load `Engine/target_oos_criteria.json` as the single source of truth:

- ROI strictly greater than 10.0%
- Maximum drawdown strictly less than 5.0%
- Win rate strictly greater than 40.0%
- Configured target barrier at least 4.0R
- At least 15 trades

Risk controls remain 5,000 USD initial capital, a 4.5% or 225 USD circuit breaker, 2 concurrent positions, and full 41 bps round-trip friction: 8 bps taker per leg, 10 bps entry slippage, and 15 bps exit slippage.

## Implementation contract

1. Remove stale hard-coded 20.0% verdict, display, and attribution thresholds. Load and inject all five criteria once.
2. In `aggregate_ladder()`, trust `total_vol_coin` only when finite and strictly positive. Otherwise reconstruct the rung total from finite nonnegative `bid_vol_coin + ask_vol_coin`.
3. Make the fast ratchet the unified default:
   - +0.80R close schedules a stop at entry +0.15R for the next bar.
   - +1.50R close schedules a stop at entry +0.80R for the next bar.
   - +2.50R close schedules realization at the next bar open.
   - Keep the exchange-resident +4.00R target barrier and +6.00R shock target.
4. Keep the old 1.0R/2.0R/3.2R schedule only as `--legacy-ratchet` ablation.
5. Retain the Donchian displacement → pullback → reclaim state machine. Require responsive reclaim alignment: EMA 8 above EMA 21 and close above EMA 50 for longs; inverse for shorts.
6. Keep footprint absorption/exhaustion in the side-aware ladder score, normalized CVD divergence as an absolute veto, and TIER_B fields masked and prohibited from entry gating.

## Causality

- Rolling features exclude the current bar.
- Closed bar t-1 decisions fill at bar t open.
- Ratchets computed from bar j close become effective only on bar j+1.
- The +2.50R close condition fills only at the following available bar open.
- Stop resolves before target if both touch intrabar.
- Training terminates at or before OOS start minus 72 hours.
- GBDT bins and Ridge normalization are frozen OOS.
- No date/window keyed parameters or OOS grid searches.

## Verification

The completed drop-in implementation passes 132 deterministic invariants with 0 failures. Added regressions cover the zero-`total_vol_coin` bid-plus-ask fallback, criteria injection, responsive ribbon gating, default ratchet, and next-bar-open +2.50R execution.

This fixture result is not a market-performance claim. The real run is:

```bash
python Engine/runners/run_rp2_round12_walkforward.py \
  --data-dir Engine/binance_backtesting_data \
  --windows Engine/oos_windows_20.json \
  --criteria Engine/target_oos_criteria.json \
  --out rp2_round13_results.json
```

A valid result requires 18 of 18 dual-parquet pairs, no dark symbols, `orderflow_cover == 1.0` in every evaluated window, and complete scorecards, funnels, diagnostics, and trade ledgers.