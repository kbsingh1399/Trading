"""
================================================================================
OFFLINE END-TO-END PIPELINE TESTS (no network)
================================================================================
Runs the complete processor -> ladder -> council -> exporter chain on
deterministic synthetic streams that mimic Binance archives (including
exchange-downtime gaps, missing spot candles, sparse funding events and
5-minute metrics snapshots), then proves:

  1. Council PASS on clean output; every canonical column present with the
     contracted dtype; both Parquet files re-load with identical content.
  2. PREFIX INVARIANCE (zero lookahead): for every numeric feature,
     process(streams[:k]) == process(streams)[:k] at several cut points.
     A feature that peeks at t+1 cannot satisfy this.
  3. Event-stream causality: shifting a funding / metrics observation to one
     millisecond AFTER a bar's close changes that bar's value -> the join uses
     close_time (not open_time) and never reads observations after close.
  4. Negative controls: the council rejects (a) a missing candle, (b) a
     duplicated candle, (c) an injected NaN, (d) a stale spot delta on an
     UNAVAILABLE bar, (e) a ladder missing a POC, and reports bar index +
     timestamp for each.
  5. Kernel equivalence: vectorised RMA / EMA / SMA / session CVD equal the
     textbook per-bar recursions bit-for-bit or to 1e-9.

Run:  python -m Engine.verification.test_pipeline_offline
================================================================================
"""

from __future__ import annotations

import os
import sys
import tempfile
import time

import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Engine.core.canonical_indicators import (  # noqa: E402
    compute_ema_series,
    compute_session_cvd,
    compute_sma_series,
    compute_wilder_rma_series,
)
from Engine.core.schema import (  # noqa: E402
    BAR_MS,
    CANONICAL_COLUMNS,
    COLUMN_DTYPES,
    LADDER_COLUMNS,
    LADDER_DTYPES,
    LEGACY_COLUMNS,
)
from Engine.pipeline.footprint_ladder import assemble_ladder  # noqa: E402
from Engine.pipeline.historical_metrics_processor import HistoricalMetricsProcessor  # noqa: E402
from Engine.pipeline.parquet_exporter import ParquetExporter  # noqa: E402
from Engine.pipeline.tick_footprint_fetcher import build_ladder_from_trades  # noqa: E402
from Engine.verification.verify_parquet_integrity import run_council  # noqa: E402

QUIET = lambda *_a, **_k: None  # noqa: E731


# ------------------------------------------------------------------------------
# Synthetic Binance-like streams
# ------------------------------------------------------------------------------
def make_streams(n_bars: int = 96 * 45, seed: int = 7, price0: float = 0.085, gap_at: int | None = 1500, gap_len: int = 7):
    rng = np.random.default_rng(seed)
    t0 = 1_598_918_400_000  # 2020-09-01 00:00 UTC
    ot = t0 + np.arange(n_bars, dtype=np.int64) * BAR_MS
    ret = rng.normal(0, 0.003, n_bars)
    close = price0 * np.exp(np.cumsum(ret))
    open_ = np.empty_like(close)
    open_[0] = price0
    open_[1:] = close[:-1]
    high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.0015, n_bars)))
    low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.0015, n_bars)))
    vol = rng.gamma(2.0, 2_000_000, n_bars)
    tb = vol * np.clip(rng.normal(0.5, 0.08, n_bars), 0.1, 0.9)
    cnt = np.maximum(1, (vol / 900).astype(np.int64))
    kl = pd.DataFrame({
        "open_time": ot, "open": open_, "high": high, "low": low, "close": close, "volume": vol,
        "close_time": ot + BAR_MS - 1, "quote_volume": vol * close, "count": cnt,
        "taker_buy_volume": tb, "taker_buy_quote_volume": tb * close,
    })
    if gap_at is not None:
        kl = kl.drop(index=range(gap_at, gap_at + gap_len)).reset_index(drop=True)   # exchange downtime

    spot_close = close * (1 - rng.normal(0.0002, 0.0003, n_bars))
    svol = vol * 0.6
    stb = svol * np.clip(rng.normal(0.5, 0.08, n_bars), 0.1, 0.9)
    spot = pd.DataFrame({"open_time": ot, "spot_close": spot_close, "spot_volume": svol, "spot_taker_buy_volume": stb})
    spot_drop = [i for i in list(range(400, 405)) + [2000] if i < n_bars]
    spot = spot.drop(index=spot_drop).reset_index(drop=True)  # missing spot candles

    f_times = np.arange(t0, ot[-1] + 1, 8 * 3_600_000, dtype=np.int64)
    funding = pd.DataFrame({"fundingTime": f_times, "fundingRate": rng.normal(0.0001, 0.00015, f_times.size)})

    m_times = np.arange(t0 - 2 * 3_600_000, ot[-1] + 1, 5 * 60_000, dtype=np.int64)
    oi = 5e8 * np.exp(np.cumsum(rng.normal(0, 0.001, m_times.size)))
    metrics = pd.DataFrame({
        "timestamp_ms": m_times, "sum_open_interest": oi, "sum_open_interest_value": oi * price0,
        "count_toptrader_long_short_ratio": np.clip(rng.normal(1.8, 0.1, m_times.size), 0.5, 5),
        "sum_toptrader_long_short_ratio": np.clip(rng.normal(1.2, 0.1, m_times.size), 0.5, 5),
        "count_long_short_ratio": np.clip(rng.normal(2.1, 0.1, m_times.size), 0.5, 5),
        "sum_taker_long_short_vol_ratio": np.clip(rng.normal(1.0, 0.1, m_times.size), 0.2, 5),
    })
    metrics.loc[metrics.sample(frac=0.02, random_state=1).index, "sum_taker_long_short_vol_ratio"] = np.nan  # sparse column
    return kl, spot, funding, metrics


def make_trades(kl_rows: pd.DataFrame, seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parts = []
    for r in kl_rows.itertuples(index=False):
        k = 400
        tt = r.open_time + np.sort(rng.integers(0, BAR_MS, k))
        px = np.round(rng.uniform(r.low, r.high, k), 5)
        qty = np.full(k, r.volume / k)
        nb = int(round(k * r.taker_buy_volume / r.volume))
        ibm = np.array([False] * nb + [True] * (k - nb))
        rng.shuffle(ibm)
        parts.append(pd.DataFrame({"transact_time": tt, "price": px, "quantity": qty, "is_buyer_maker": ibm}))
    return pd.concat(parts, ignore_index=True)


def process(kl, spot, funding, metrics, fp=None, symbol="DOGEUSDT"):
    return HistoricalMetricsProcessor(log=QUIET).process_master_dataset(kl, metrics, funding, fp, spot, symbol=symbol)


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------
def test_kernels():
    rng = np.random.default_rng(0)
    x = rng.gamma(2, 3, 5000)
    ref = np.empty_like(x)
    ref[0] = x[0]
    for i in range(1, 14):
        ref[i] = (ref[i - 1] * i + x[i]) / (i + 1)
    for i in range(14, x.size):
        ref[i] = ref[i - 1] + (x[i] - ref[i - 1]) / 14
    assert np.abs(compute_wilder_rma_series(x, 14) - ref).max() < 1e-9
    e = np.empty_like(x)
    e[0] = x[0]
    k = 2 / 801
    for i in range(1, x.size):
        e[i] = x[i] * k + e[i - 1] * (1 - k)
    assert np.abs(compute_ema_series(x, 800) - e).max() < 1e-9
    s = np.array([np.mean(x[max(0, i - 8): i + 1]) for i in range(x.size)])
    assert np.abs(compute_sma_series(x, 9) - s).max() < 1e-9
    ts = 1_598_918_400_000 + np.arange(x.size) * BAR_MS
    cvd, cur, acc = np.empty_like(x), -1, 0.0
    for i in range(x.size):
        d = ts[i] // 86_400_000
        if d != cur:
            cur, acc = d, 0.0
        acc += x[i]
        cvd[i] = acc
    assert np.abs(compute_session_cvd(ts, x) - cvd).max() < 1e-9
    print("  [PASS] kernels equal per-bar recursions")


def test_clean_pipeline_and_export():
    kl, spot, funding, metrics = make_streams()
    trades = make_trades(kl.iloc[3000:3100])
    fp_summary, fp_ladder = build_ladder_from_trades(trades, 0.00003)
    master = process(kl, spot, funding, metrics, fp_summary)
    assert list(master.columns) == CANONICAL_COLUMNS
    assert master.columns[: len(LEGACY_COLUMNS)].tolist() == LEGACY_COLUMNS
    for col, dt in COLUMN_DTYPES.items():
        if dt != "string":
            assert str(master[col].dtype) == dt, (col, master[col].dtype)
    assert (master["future_flow_source"] == "TICK_EXACT").sum() == 100
    assert master["is_synthetic"].sum() == 7
    assert (master["spot_flow_source"] == "UNAVAILABLE").sum() == 6
    assert master["atr_14"].nunique() > 1000, "sub-dollar precision collapse"
    ladder, stats = assemble_ladder(master, fp_ladder)
    assert stats["tick_exact_candles"] == 100 and stats["synthetic_candles"] == len(master) - 100
    rep = run_council(master, ladder, "DOGEUSDT", log=QUIET)
    assert rep.passed, [str(f) for f in rep.findings]
    with tempfile.TemporaryDirectory() as d:
        ex = ParquetExporter(d)
        ex.export_master(master, "DOGEUSDT")
        ex.export_ladder(ladder, "DOGEUSDT")
        ex.write_manifest(master, "DOGEUSDT", stats, rep.to_dict())
        m2 = pd.read_parquet(os.path.join(d, "DOGEUSDT_15m_master_2020_2026.parquet"))
        l2 = pd.read_parquet(os.path.join(d, "DOGEUSDT_15m_footprint_ladder.parquet"))
        assert list(m2.columns) == CANONICAL_COLUMNS and list(l2.columns) == LADDER_COLUMNS
        assert all(str(l2[c].dtype) == LADDER_DTYPES[c] for c in LADDER_COLUMNS)
        num = [c for c in CANONICAL_COLUMNS if COLUMN_DTYPES[c] != "string"]
        assert np.array_equal(m2[num].to_numpy(np.float64), master[num].to_numpy(np.float64))
        rep2 = run_council(m2, l2, "DOGEUSDT", log=QUIET)
        assert rep2.passed
    print(f"  [PASS] clean pipeline: {len(master):,} bars, {len(ladder):,} rungs, council PASS, round-trip identical")
    return master, ladder, kl, spot, funding, metrics


def test_prefix_invariance(kl, spot, funding, metrics):
    full = process(kl, spot, funding, metrics)
    num = [c for c in CANONICAL_COLUMNS if COLUMN_DTYPES[c] not in ("string",)]
    for cut in (97, 1000, 1503, 2500, len(kl) - 1):
        cut_ms = int(kl["open_time"].iloc[cut - 1])
        part = process(
            kl.iloc[:cut],
            spot[spot["open_time"] <= cut_ms],
            funding[funding["fundingTime"] <= cut_ms + BAR_MS - 1],
            metrics[metrics["timestamp_ms"] <= cut_ms + BAR_MS - 1],
        )
        k = len(part)
        a = part[num].to_numpy(np.float64)
        b = full[num].iloc[:k].to_numpy(np.float64)
        diff = np.abs(a - b)
        bad = np.flatnonzero(diff.max(axis=0) > 1e-9)
        assert bad.size == 0, f"lookahead in {[num[j] for j in bad]} at cut {cut}"
    print("  [PASS] prefix invariance: all numeric features causal at 5 cut points")


def test_event_join_uses_close_time(kl, spot, funding, metrics):
    base = process(kl, spot, funding, metrics)
    i = 800
    close_ms = int(base["close_time_ms"].iloc[i])
    # funding event exactly at close -> visible to bar i; one ms later -> not visible
    f_at = pd.concat([funding, pd.DataFrame({"fundingTime": [close_ms], "fundingRate": [0.0123]})])
    f_after = pd.concat([funding, pd.DataFrame({"fundingTime": [close_ms + 1], "fundingRate": [0.0123]})])
    at = process(kl, spot, f_at, metrics)
    after = process(kl, spot, f_after, metrics)
    assert abs(at["funding_rate_pct"].iloc[i] - 1.23) < 1e-9
    assert abs(after["funding_rate_pct"].iloc[i] - base["funding_rate_pct"].iloc[i]) < 1e-9
    assert abs(after["funding_rate_pct"].iloc[i + 1] - 1.23) < 1e-9
    m_at = pd.concat([metrics, pd.DataFrame({"timestamp_ms": [close_ms], "sum_open_interest": [9.9e9], "sum_open_interest_value": [1e9],
                                             "count_toptrader_long_short_ratio": [1.0], "sum_toptrader_long_short_ratio": [1.0],
                                             "count_long_short_ratio": [1.0], "sum_taker_long_short_vol_ratio": [1.0]})])
    m_after = m_at.copy()
    m_after.iloc[-1, m_after.columns.get_loc("timestamp_ms")] = close_ms + 1
    assert abs(process(kl, spot, funding, m_at)["open_interest_k"].iloc[i] - 9.9e6) < 1e-6
    assert abs(process(kl, spot, funding, m_after)["open_interest_k"].iloc[i] - base["open_interest_k"].iloc[i]) < 1e-9
    print("  [PASS] event streams joined on close_time_ms with <= semantics (no post-close leakage)")


def test_negative_controls(master, ladder):
    def checks(m, l):
        return {f.check: f for f in run_council(m, l, "DOGEUSDT", log=QUIET).findings}

    m = master.drop(index=1234).reset_index(drop=True)
    f = checks(m, ladder)
    assert "cadence" in f and f["cadence"].bar_index == 1234 and f["cadence"].timestamp_utc.startswith("2020-09-13"), f.get("cadence")

    m = pd.concat([master.iloc[:2000], master.iloc[[1999]], master.iloc[2000:]]).reset_index(drop=True)
    f = checks(m, ladder)
    assert "duplicates" in f and f["duplicates"].bar_index == 2000

    m = master.copy()
    m.loc[777, "rsi_14"] = np.nan
    f = checks(m, ladder)
    assert "nulls" in f and f["nulls"].bar_index == 777

    m = master.copy()
    idx = m.index[m["spot_flow_source"] == "UNAVAILABLE"][0]
    m.loc[idx, "spot_cvd_15m"] = 123.0
    f = checks(m, ladder)
    assert "spot_unavailable_zero" in f and f["spot_unavailable_zero"].bar_index == idx

    l = ladder.copy()
    first_ts = l["open_time_ms"].iloc[0]
    l.loc[l["open_time_ms"] == first_ts, "is_poc"] = np.int8(0)
    f = checks(master, l)
    assert "ladder_poc" in f and f["ladder_poc"].open_time_ms == first_ts

    m = master.copy()
    m["ema_8"] = m["ema_8"].shift(-1).ffill()   # classic lookahead
    f = checks(m, ladder)
    assert "ema_8_recursion" in f

    m = master.copy()
    m["session_vwap"] = m["session_vwap"].rolling(3, center=True).mean().bfill().ffill()   # centred window
    f = checks(m, ladder)
    assert "vwap_rederive" in f

    # A1 impossible open interest check: open_interest_k == 0 while metrics_available == 1
    m = master.copy()
    avail_idx = m.index[m["metrics_available"] == 1][0]
    m.loc[avail_idx, "open_interest_k"] = 0.0
    f = checks(m, ladder)
    assert "oi_impossible_zero" in f and f["oi_impossible_zero"].bar_index == avail_idx
    print("  [PASS] negative controls: gap, duplicate, NaN, stale spot, missing POC, shifted EMA, centred VWAP, impossible OI all rejected with bar index + timestamp")


def test_precision_on_sub_dollar_asset(master):
    for col in ("ema_8", "ema_800", "atr_14", "basis_usd", "fp_poc", "session_vwap"):
        assert master[col].nunique() > 1000, f"{col} precision collapse ({master[col].nunique()} distinct)"
    # value area is bucket-quantised by design (merge level 0.0001); legacy output had 8 distinct values over 6 years
    assert master["session_vah"].nunique() > 100, f"session_vah collapsed ({master['session_vah'].nunique()} distinct)"
    print("  [PASS] sub-dollar asset (price ~0.085) keeps full precision on price-scale features")


def test_orchestrator_end_to_end():
    """run_pipeline with the network layer replaced by the synthetic streams; exercises slice, gate, export, skip."""
    import Engine.run_historical_pipeline as rp

    kl, spot, funding, metrics = make_streams(n_bars=96 * 40)
    trades = make_trades(kl.iloc[2000:2050])
    fp_summary, fp_ladder = build_ladder_from_trades(trades, 0.00003)

    class FakeFetcher:
        def __init__(self, *a, **k): pass
        def fetch_futures_klines(self, symbol, start_date, now=None): return kl.copy()
        def fetch_spot_klines(self, symbol, start_date, now=None): return spot.copy()
        def fetch_metrics(self, symbol, start_date, now=None): return metrics.copy()
        def fetch_funding_rates(self, symbol, start_time_ms): return funding.copy()

    class FakeFootprint:
        def __init__(self, *a, **k): pass
        def fetch_footprint(self, symbol, start_date, now=None): return fp_summary.copy(), fp_ladder.copy()

    orig = rp.BinanceHistoricalFetcher, rp.TickFootprintFetcher
    rp.BinanceHistoricalFetcher, rp.TickFootprintFetcher = FakeFetcher, FakeFootprint
    try:
        with tempfile.TemporaryDirectory() as d:
            ok = rp.run_pipeline("DOGEUSDT", start_date_str="2020-09-03", target_dir=d, cache_dir=os.path.join(d, "cache"),
                                 max_workers=2, footprint_days=5, run_audit=True, log=QUIET)
            assert ok
            m = pd.read_parquet(os.path.join(d, "DOGEUSDT_15m_master_2020_2026.parquet"))
            l = pd.read_parquet(os.path.join(d, "DOGEUSDT_15m_footprint_ladder.parquet"))
            assert m["datetime_utc"].iloc[0] == "2020-09-03 00:00:00", m["datetime_utc"].iloc[0]
            assert abs(m["future_cvd_lifetime"].iloc[0] - m["future_cvd_15m"].iloc[0]) < 1e-6
            # warm-up bars were used: ema_800 at the first exported bar differs from the close (seeded 192 bars earlier)
            assert abs(m["ema_800"].iloc[0] - m["close"].iloc[0]) > 1e-9
            assert (m["future_flow_source"] == "TICK_EXACT").sum() == 50
            assert set(l["rung_source"].unique()) == {0, 1}
            assert np.isin(m["open_time_ms"].to_numpy(), l["open_time_ms"].unique()).all()
            import json
            man = json.load(open(os.path.join(d, "DOGEUSDT_dataset_manifest.json")))
            assert man["verification"]["passed"] and man["schema_version"] == "2.0"
            # fast-skip honours the contract (fresh file -> skip); age check ignored by passing a huge window
            assert rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9)
            # legacy-shaped ladder (no rung_source) must NOT be skipped
            l.drop(columns="rung_source").to_parquet(os.path.join(d, "DOGEUSDT_15m_footprint_ladder.parquet"), index=False)
            assert not rp.existing_output_is_current(d, "DOGEUSDT", max_age_hours=1e9)
    finally:
        rp.BinanceHistoricalFetcher, rp.TickFootprintFetcher = orig
    print("  [PASS] orchestrator end-to-end: warm-up slice, dual-table export, manifest, contract-aware fast-skip")


def test_repair_gate():
    """The gate must repair a stale-spot violation causally and re-verify to PASS; unrepairable -> reject."""
    import Engine.run_historical_pipeline as rp
    kl, spot, funding, metrics = make_streams(n_bars=96 * 10, gap_at=300, gap_len=3)
    master = process(kl, spot, funding, metrics)
    ladder, _ = assemble_ladder(master, None)
    bad = master.copy()
    idx = bad.index[bad["spot_flow_source"] == "UNAVAILABLE"][0]
    bad.loc[idx, "spot_cvd_15m"] = 42.0
    rep = run_council(bad, ladder, "DOGEUSDT", log=QUIET)
    assert not rep.passed
    fixed, ladder2, changed = rp.causal_repair(bad, ladder, rep, QUIET)
    assert changed
    rep2 = run_council(fixed, ladder2, "DOGEUSDT", log=QUIET)
    assert rep2.passed, [str(f) for f in rep2.findings]
    # a missing candle has no causal repair -> stays rejected
    gap = master.drop(index=500).reset_index(drop=True)
    rep3 = run_council(gap, ladder, "DOGEUSDT", log=QUIET)
    _, _, changed3 = rp.causal_repair(gap, ladder, rep3, QUIET)
    assert not changed3 or not run_council(*rp.causal_repair(gap, ladder, rep3, QUIET)[:2], "DOGEUSDT", log=QUIET).passed
    print("  [PASS] gate: stale spot repaired causally -> PASS; missing candle -> stays REJECTED")


def test_fetcher_against_mock_binance():
    """Spins a local HTTP server that mimics data.binance.vision + fapi/api and runs the real fetcher against it."""
    import io, json, threading, zipfile
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from socketserver import ThreadingMixIn
    from datetime import datetime, timezone, timedelta
    from Engine.pipeline import binance_historical_fetcher as bf
    from Engine.pipeline.http_client import HttpClient


    BAR=900000
    kl, spot, funding, metrics = make_streams(n_bars=96*70, seed=5, price0=100.0, gap_at=None)
    t0=int(kl.open_time.iloc[0]); tN=int(kl.open_time.iloc[-1])
    now = datetime.fromtimestamp((tN+BAR)/1000, tz=timezone.utc) + timedelta(minutes=7)
    def month_of(ms): d=datetime.fromtimestamp(ms/1000,tz=timezone.utc); return f"{d.year}-{d.month:02d}"
    def day_of(ms): return datetime.fromtimestamp(ms/1000,tz=timezone.utc).strftime("%Y-%m-%d")
    kl["ym"]=kl.open_time.map(month_of); kl["ymd"]=kl.open_time.map(day_of)
    cur_ym=f"{now.year}-{now.month:02d}"; today=now.strftime("%Y-%m-%d")
    downtime = set(kl.open_time.iloc[3000:3005])
    missing_day = kl.ymd.iloc[1000]
    rest_calls=[]; rl_hits={"n":0}
    spot_k=spot.rename(columns={"spot_close":"close","spot_volume":"volume","spot_taker_buy_volume":"taker_buy_volume"}).copy()
    spot_k=spot_k.assign(open=spot_k.close,high=spot_k.close,low=spot_k.close,close_time=spot_k.open_time+BAR-1,quote_volume=spot_k.volume*spot_k.close,count=10,taker_buy_quote_volume=spot_k.taker_buy_volume*spot_k.close)
    spot_k["ym"]=spot_k.open_time.map(month_of); spot_k["ymd"]=spot_k.open_time.map(day_of)
    def kline_csv(df, header, micro=False):
        d=df.copy()
        if micro: d["open_time"]=d.open_time*1000; d["close_time"]=d.close_time*1000
        d["ignore"]=0
        cols=["open_time","open","high","low","close","volume","close_time","quote_volume","count","taker_buy_volume","taker_buy_quote_volume","ignore"]
        return d[cols].to_csv(index=False, header=header)
    def zipped(name, text):
        b=io.BytesIO()
        with zipfile.ZipFile(b,"w") as z: z.writestr(name,text)
        return b.getvalue()
    class H(BaseHTTPRequestHandler):
        def log_message(self,*a): pass
        def _send(self,code,body=b"",hdr=None):
            self.send_response(code)
            for k,v in (hdr or {}).items(): self.send_header(k,v)
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        def do_GET(self):
            p=self.path
            try:
                if "/monthly/klines/" in p:
                    ym=p.split("-15m-")[-1][:7]
                    if ym==cur_ym: return self._send(404)
                    if "/spot/" in p:
                        part=spot_k[spot_k.ym==ym]
                        if part.empty: return self._send(404)
                        return self._send(200, zipped("x.csv", kline_csv(part, header=False)))
                    part=kl[(kl.ym==ym)&(~kl.open_time.isin(downtime))&(kl.ymd!=missing_day)]
                    if part.empty: return self._send(404)
                    return self._send(200, zipped("x.csv", kline_csv(part, header=(ym>="2020-10"), micro=(ym>="2020-11"))))
                if "/daily/klines/" in p:
                    ymd=p.split("-15m-")[-1][:10]
                    if ymd>=today: return self._send(404)
                    if "/spot/" in p:
                        part=spot_k[spot_k.ymd==ymd]
                        if part.empty: return self._send(404)
                        return self._send(200, zipped("x.csv", kline_csv(part, header=False)))
                    if ymd==missing_day: return self._send(404)
                    part=kl[(kl.ymd==ymd)&(~kl.open_time.isin(downtime))]
                    if part.empty: return self._send(404)
                    return self._send(200, zipped("x.csv", kline_csv(part, header=True)))
                if "/fapi/v1/klines" in p or "/api/v3/klines" in p:
                    rest_calls.append(p)
                    if len(rest_calls)==1:
                        rl_hits["n"]+=1; return self._send(429, b"{}", {"Retry-After":"1"})
                    q=dict(x.split("=") for x in p.split("?")[1].split("&")); st=int(q["startTime"]); et=int(q.get("endTime",tN+BAR))
                    src=kl if "fapi" in p else spot_k
                    part=src[(src.open_time>=st)&(src.open_time<=et)&(~src.open_time.isin(downtime))].head(1500)
                    rows=[[int(r.open_time),str(r.open),str(r.high),str(r.low),str(r.close),str(r.volume),int(r.close_time),str(r.quote_volume),int(r.count),str(r.taker_buy_volume),str(r.taker_buy_quote_volume),"0"] for r in part.itertuples()]
                    rows.append([tN+BAR,"1","1","1","1","1",tN+2*BAR-1,"1",1,"1","1","0"])   # forming candle
                    return self._send(200, json.dumps(rows).encode())
                if "/daily/metrics/" in p:
                    sym=p.split("/metrics/")[1].split("/")[0]; ymd=p.split("-metrics-")[-1][:10]
                    if sym.endswith("USDC") or ymd>=today: return self._send(404)
                    m=metrics.copy(); m["create_time"]=pd.to_datetime(m.timestamp_ms,unit="ms",utc=True).dt.strftime("%Y-%m-%d %H:%M:%S"); m["ymd"]=m.create_time.str[:10]; m["symbol"]=sym
                    part=m[m.ymd==ymd]
                    if part.empty: return self._send(404)
                    cols=["create_time","symbol","sum_open_interest","sum_open_interest_value","count_toptrader_long_short_ratio","sum_toptrader_long_short_ratio","count_long_short_ratio","sum_taker_long_short_vol_ratio"]
                    return self._send(200, zipped("m.csv", part[cols].to_csv(index=False)))
                if "/futures/data/" in p:
                    key=p.split("/futures/data/")[1].split("?")[0]
                    m=metrics.tail(500)
                    mp={"openInterestHist":lambda r:{"timestamp":int(r.timestamp_ms),"sumOpenInterest":str(r.sum_open_interest),"sumOpenInterestValue":str(r.sum_open_interest_value)},
                        "globalLongShortAccountRatio":lambda r:{"timestamp":int(r.timestamp_ms),"longShortRatio":str(r.count_long_short_ratio)},
                        "topLongShortPositionRatio":lambda r:{"timestamp":int(r.timestamp_ms),"longShortRatio":str(r.sum_toptrader_long_short_ratio)},
                        "topLongShortAccountRatio":lambda r:{"timestamp":int(r.timestamp_ms),"longShortRatio":str(r.count_toptrader_long_short_ratio)},
                        "takerlongshortRatio":lambda r:{"timestamp":int(r.timestamp_ms),"buySellRatio":str(r.sum_taker_long_short_vol_ratio)}}
                    return self._send(200, json.dumps([mp[key](r) for r in m.itertuples()]).encode())
                if "/fapi/v1/fundingRate" in p:
                    q=dict(x.split("=") for x in p.split("?")[1].split("&")); st=int(q["startTime"])
                    part=funding[funding.fundingTime>=st].head(1000)
                    return self._send(200, json.dumps([{"symbol":"BTCUSDT","fundingTime":int(r.fundingTime),"fundingRate":str(r.fundingRate),"markPrice":"1"} for r in part.itertuples()]).encode())
                return self._send(404)
            except Exception:
                import traceback; traceback.print_exc(); return self._send(500)
    class TS(ThreadingMixIn, HTTPServer): daemon_threads=True
    srv=TS(("127.0.0.1",0),H); port=srv.server_address[1]; threading.Thread(target=srv.serve_forever,daemon=True).start()
    bf.VISION=f"http://127.0.0.1:{port}/data"; bf.FAPI=f"http://127.0.0.1:{port}"; bf.SAPI=f"http://127.0.0.1:{port}"
    with tempfile.TemporaryDirectory() as cache:
        http=HttpClient(base_delay=0.05, rate_limit_cooldown=1.0)
        f=bf.BinanceHistoricalFetcher(cache_dir=cache,max_workers=8,http=http,log=QUIET)
        start=datetime.fromtimestamp(t0/1000,tz=timezone.utc).strftime("%Y-%m-%d")
        t=time.time(); fut=f.fetch_futures_klines("BTCUSDT",start,now); ta=time.time()-t
        sp=f.fetch_spot_klines("BTCUSDT",start,now)
        me=f.fetch_metrics("BTCUSDT",start,now)
        fr=f.fetch_funding_rates("BTCUSDT",t0)
        expected=len(kl)-len(downtime)
        print(f"futures bars={len(fut)} expected={expected} (downtime={len(downtime)}) | spot={len(sp)}/{len(spot)} | metrics={len(me)}/{len(metrics)} | funding={len(fr)}/{len(funding)} | {ta:.1f}s")
        assert len(fut)==expected, "gap repair / dedupe failed"
        assert fut.open_time.is_monotonic_increasing and fut.open_time.is_unique
        assert fut.open_time.max()==tN, "REST tail missing or forming candle leaked"
        mdb = kl[kl.ymd==missing_day]; assert fut.open_time.isin(mdb.open_time).sum()==len(mdb), "missing-day REST repair failed"
        assert fut.dtypes["open_time"]=="int64" and fut.dtypes["count"]=="int64" and fut.dtypes["close"]=="float64"
        assert (fut.open_time>1e12).all() and (fut.open_time<2e12).all(), "microsecond normalisation failed"
        assert rl_hits["n"]==1 and http.stats["rate_limited"]==1, "429 latch not exercised"
        assert len(sp)==len(spot) and list(sp.columns)==["open_time","spot_close","spot_volume","spot_taker_buy_volume"]
        start_day_ms=int(datetime.strptime(start,"%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()*1000)
        exp_metrics=int((metrics.timestamp_ms>=start_day_ms).sum())   # rows before the requested start day are out of scope
        assert len(me)==exp_metrics, (len(me), exp_metrics)
        assert me.timestamp_ms.is_monotonic_increasing and me.timestamp_ms.is_unique
        assert len(fr)==len(funding)
        before=http.stats["requests"]; fut2=f.fetch_futures_klines("BTCUSDT",start,now); after=http.stats["requests"]
        assert fut2.equals(fut); print(f"cache hit: {after-before} HTTP calls on re-run | http stats {http.stats}")
        from Engine.pipeline.historical_metrics_processor import HistoricalMetricsProcessor
        from Engine.pipeline.footprint_ladder import assemble_ladder
        from Engine.verification.verify_parquet_integrity import run_council
        m=HistoricalMetricsProcessor(log=QUIET).process_master_dataset(fut,me,fr,None,sp,symbol="BTCUSDT")
        lad,_=assemble_ladder(m,None); rep=run_council(m,lad,"BTCUSDT",log=QUIET)
        print("council on fetched streams:", rep.passed, rep.agent_status, "| synthetic bars:", int(m.is_synthetic.sum()), "| metrics_available:", int(m.metrics_available.sum()),"/",len(m))
        for fdg in rep.findings: print("  ", fdg)
        assert rep.passed and int(m.is_synthetic.sum())==len(downtime)
    print("  [PASS] fetcher vs Binance-shaped mock server: monthly/daily/REST stitching, us->ms, header/no-header, missing-day repair, 429 latch, forming-candle exclusion, cache hits")


def test_metrics_validity_and_quarantine_regression(kl, spot, funding, metrics):
    """Regression test for A1 (impossible OI filter) and A1b (_stale_runs_mask quarantine)."""
    from Engine.pipeline.historical_metrics_processor import _stale_runs_mask, HistoricalMetricsProcessor
    # 1. Test _stale_runs_mask unit logic
    vals = np.ones(500)
    oi_moves = np.ones(500, dtype=bool)
    mask = _stale_runs_mask(vals, threshold=288, oi_moves=oi_moves, min_moving=0.90)
    assert mask.all(), "stale_runs_mask failed to flag 500-bar identical run with moving OI"
    # tape down: oi_moves is False
    mask_dead_tape = _stale_runs_mask(vals, threshold=288, oi_moves=~oi_moves, min_moving=0.90)
    assert not mask_dead_tape.any(), "stale_runs_mask should not flag when tape is down"

    # 2. Test processor end-to-end with injected 400-bar frozen run in metrics
    me = metrics.copy()
    freeze_start = 500
    freeze_len = 400
    me.loc[freeze_start:freeze_start + freeze_len, "sum_toptrader_long_short_ratio"] = 1.073470
    proc = HistoricalMetricsProcessor(log=QUIET)
    m = proc.process_master_dataset(kl, me, funding, None, spot, symbol="DOGEUSDT")
    assert "is_imputed_metrics" in m and "metrics_available" in m
    imputed = m["is_imputed_metrics"].to_numpy()
    avail = m["metrics_available"].to_numpy()
    assert (imputed == (avail == 0)).all(), "is_imputed_metrics != (metrics_available == 0) contract violated"
    print("  [PASS] regression: _stale_runs_mask, oi_impossible_zero, and causal imputation invariants verified")


def main() -> int:
    t0 = time.time()
    print("OFFLINE PIPELINE TEST SUITE")
    test_kernels()
    master, ladder, kl, spot, funding, metrics = test_clean_pipeline_and_export()
    test_precision_on_sub_dollar_asset(master)
    test_prefix_invariance(kl, spot, funding, metrics)
    test_event_join_uses_close_time(kl, spot, funding, metrics)
    test_negative_controls(master, ladder)
    test_metrics_validity_and_quarantine_regression(kl, spot, funding, metrics)
    test_orchestrator_end_to_end()
    test_repair_gate()
    test_fetcher_against_mock_binance()
    print(f"ALL TESTS PASSED in {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
