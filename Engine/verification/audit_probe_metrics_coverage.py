"""
================================================================================
AUDIT PROBE: council blind spot to partially-available official metrics
        (docs/PIPELINE_VERIFICATION_CERTIFICATION.md §4.1 -- BLOCKING finding)
================================================================================
Binance's /futures/data/* REST endpoints serve only the latest 30 days, so the
2020->present metrics history comes entirely from the data.binance.vision daily
archives. If those start after the export window (long/short-ratio series begin
materially later than the kline archives), the processor substitutes *legal*
constants for the missing range:

    open_interest_k := 0.0    ls_ratio_global := 1.0    ls_ratio_top := 1.0
    top_account_ratio := 1.0  whale_index := 100.0      oi_change_pct := 0.0

Those values pass every dtype, domain, null and identity check the 3-agent
council performs, and Agent 3's `dead_feature` scan only fires when a column is
constant over the WHOLE file -- so a regime-split series is invisible.

This probe builds DOGE-scale bars where the metrics archive begins mid-sample and
shows `CouncilReport.passed == True` over a fabricated 40 % of rows. It exits 1
when the blind spot reproduces (i.e. the council accepted fabricated data), 0 if
a future fix starts rejecting it.

Usage: python3 -m Engine.verification.audit_probe_metrics_coverage
================================================================================
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Engine.pipeline.binance_historical_fetcher import assemble_ladder  # noqa: E402
from Engine.pipeline.historical_metrics_processor import HistoricalMetricsProcessor  # noqa: E402
from Engine.verification.verify_parquet_integrity import run_council  # noqa: E402

BAR_MS = 900_000
N = 40_000
METRICS_FRACTION = 0.60          # archive covers the last 60 % of the sample


def build_streams():
    rng = np.random.default_rng(11)
    ot = 1_598_918_400_000 + np.arange(N) * BAR_MS
    c = 0.085 * np.exp(np.cumsum(rng.normal(0, 6e-3, N)))          # realistic DOGE scale
    o = np.concatenate([[c[0]], c[:-1]])
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 3e-3, N)))
    l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 3e-3, N)))
    vb = np.abs(rng.gamma(2, 5e8, N))
    klines = pd.DataFrame({
        "open_time": ot, "open": o, "high": h, "low": l, "close": c,
        "volume": vb, "close_time": ot + BAR_MS - 1, "quote_volume": vb * c,
        "count": rng.integers(500, 5000, N), "taker_buy_volume": vb * 0.52,
        "taker_buy_quote_volume": vb * c * 0.52,
    })
    spot = pd.DataFrame({
        "open_time": ot, "spot_close": c * (1 - rng.normal(0, 1e-4, N)),
        "spot_volume": vb * 1.3, "spot_taker_buy_volume": vb * 1.3 * 0.49,
    })
    funding = pd.DataFrame({"fundingTime": ot[::32], "fundingRate": rng.normal(0, 1e-4, N // 32)})

    mstart = int(ot[0]) + int(METRICS_FRACTION * N) * BAR_MS
    mt = np.arange(mstart, int(ot[-1]) - 1, 5 * 60_000)
    metrics = pd.DataFrame({
        "timestamp_ms": mt,
        "sum_open_interest": np.abs(rng.normal(2e9, 1e8, len(mt))),
        "sum_open_interest_value": np.abs(rng.normal(2e5, 1e4, len(mt))) * 1000,
        "count_long_short_ratio": np.abs(rng.normal(2.4, 0.3, len(mt))) + 0.5,
        "sum_toptrader_long_short_ratio": np.abs(rng.normal(1.8, 0.3, len(mt))) + 0.5,
        "count_toptrader_long_short_ratio": np.abs(rng.normal(2.0, 0.3, len(mt))) + 0.5,
        "sum_taker_long_short_vol_ratio": np.abs(rng.normal(1.1, 0.2, len(mt))) + 0.2,
    })
    return ot, mstart, klines, spot, funding, metrics


def main() -> int:
    ot, mstart, klines, spot, funding, metrics = build_streams()
    print("=" * 78)
    print("metrics archive coverage vs export window")
    print("=" * 78)
    print(f"  first exported bar  : {pd.to_datetime(int(ot[0]), unit='ms', utc=True)}")
    print(f"  first metrics row   : {pd.to_datetime(mstart, unit='ms', utc=True)}")
    pre = ot < mstart
    print(f"  bars with NO metrics: {int(pre.sum()):,}/{N:,}  ({100 * pre.mean():.1f} %)\n")

    master = HistoricalMetricsProcessor(log=lambda m: None).process_master_dataset(
        klines, metrics, funding, None, spot, symbol="DOGEUSDT")
    ladder, _ = assemble_ladder(master, None)

    print("-" * 78)
    print("fabricated head vs real tail (a whole-column nunique test cannot see this)")
    print("-" * 78)
    for col in ("open_interest_k", "ls_ratio_global", "ls_ratio_top", "top_account_ratio",
                "whale_index", "taker_volume_ratio", "oi_change_pct"):
        head, tail = master.loc[pre, col], master.loc[~pre, col]
        print(f"  {col:22} head: mean={head.mean():>12,.4f} nunique={head.nunique():>3} | "
              f"tail nunique={tail.nunique():>7,}")

    print("\n" + "-" * 78)
    print("sub-dollar precision (Task 1.1 mitigation) -- independent of the above")
    print("-" * 78)
    for col in ("ema_8", "atr_14", "basis_usd", "close"):
        print(f"  {col:12} nunique={master[col].nunique():>7,}   "
              f"atr_14==0 on {100 * (master['atr_14'] == 0).mean():.2f} % of bars")
    print("  (legacy shipped data: DOGE atr_14==0 on 97.0 % of bars, 73 distinct ema_8)")

    # The fixture's head is value-identical to a legitimate pre-archive absence, so the ONLY thing
    # that must decide it is the download inventory. Assert the defect shape explicitly: run the
    # council with an attestation of "nothing is absent at the source". Passing nothing instead would
    # let agent_schema fall back to the symbol's real manifest, which for DOGEUSDT genuinely attests
    # 2020-09..2021-11 as absent -- excusing the fixture for a reason that has nothing to do with it.
    report = run_council(master, ladder, "DOGEUSDT", log=lambda m: None, attested_months=set())
    print("\n" + "=" * 78)
    print(f"COUNCIL VERDICT (no attestation): passed={report.passed}  {report.agent_status}")
    print("=" * 78)
    for f in report.findings[:10]:
        print(f"   -> {f}")

    # and the other side of the same line: the identical frame, with the source attesting those
    # months as never published, must be accepted. That is the ETHUSDT/DOGEUSDT 2020 case.
    head_months = sorted(set(pd.to_datetime(master.loc[pre, "open_time_ms"].to_numpy("int64"),
                                            unit="ms", utc=True).strftime("%Y-%m")))
    rep_att = run_council(master, ladder, "DOGEUSDT", log=lambda m: None, attested_months=set(head_months))
    excused = {f.check for f in rep_att.findings} & {"regime_dead_feature", "metrics_coverage_unattested",
                                                     "metrics_interior_hole"}
    print(f"\n  same frame, ATTESTED absent ({head_months[0]}..{head_months[-1]}): passed={rep_att.passed}, "
          f"coverage findings={sorted(excused) or 'none'}")

    fabricated = int(pre.sum())
    if report.passed:
        print(f"\n  BLIND SPOT REPRODUCED: the council ACCEPTED an export whose first {fabricated:,} bars")
        print("  carry fabricated OI/L-S/whale/taker values (only `metrics_available` marks them).")
        print("  Required fix: per-year availability gate + is_imputed flag + regime-split dead-feature scan")
        print("  (see docs/PIPELINE_VERIFICATION_CERTIFICATION.md §4.1).")
        return 1
    print("\n  Council now rejects partially-fabricated metrics -> fix verified in place.")
    if excused or rep_att.passed is not True:
        print("  ** the attested twin did not behave as the calibration promises (see above) **")
        return 1
    print("  and honours an attested pre-archive absence -> multi-asset calibration verified in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
