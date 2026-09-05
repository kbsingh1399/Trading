"""
================================================================================
BINANCE HISTORICAL ARCHIVE & REST FETCHER (USDT-M FUTURES + SPOT)
================================================================================
Streams
  1. Futures 15m klines      data.binance.vision monthly -> daily -> fapi REST tail
  2. Spot 15m klines         data.binance.vision monthly -> daily -> api  REST tail
  3. Futures official metrics (5m)  daily archives -> futures/data REST bridge
  4. Funding rate history    fapi /fapi/v1/fundingRate (paginated, incremental cache)

Design
  * Every archive object is cached as Parquet under ``cache_dir`` and never
    re-downloaded. 404s (pre-listing / archive lag) are memoised per process.
  * One shared ``HttpClient`` per fetcher: exponential backoff, 418/429 latch.
  * All timestamps are normalised to Unix **milliseconds** (newer archives ship
    microseconds) and every frame is de-duplicated + sorted on its key.
  * Only *closed* candles are ever returned (REST tail is filtered on
    ``close_time < now``).
================================================================================
"""

from __future__ import annotations

import io
import json
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from .http_client import FetchError, HttpClient

BAR_MS = 900_000
DAY_MS = 86_400_000
VISION = "https://data.binance.vision/data"
FAPI = "https://fapi.binance.com"
SAPI = "https://api.binance.com"

KLINE_COLS = [
    "open_time", "open", "high", "low", "close", "volume", "close_time",
    "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore",
]
KLINE_OUT = [
    "open_time", "open", "high", "low", "close", "volume", "close_time",
    "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume",
]
METRIC_COLS = [
    "timestamp_ms", "sum_open_interest", "sum_open_interest_value",
    "count_toptrader_long_short_ratio", "sum_toptrader_long_short_ratio",
    "count_long_short_ratio", "sum_taker_long_short_vol_ratio",
]
USDC_METRICS_FLOOR = "2023-03-01"   # USDC-margined perps did not exist before this


def _utc(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def _ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def _norm_ms(values: pd.Series) -> pd.Series:
    v = pd.to_numeric(values, errors="coerce")
    v = v.where(v <= 2_000_000_000_000, v // 1000)   # microseconds -> milliseconds
    return v.astype("int64")


def _month_keys(start: datetime, end_exclusive: datetime) -> List[str]:
    keys, y, m = [], start.year, start.month
    while datetime(y, m, 1, tzinfo=timezone.utc) < end_exclusive:
        keys.append(f"{y}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return keys


def _day_keys(start: datetime, end_exclusive: datetime) -> List[str]:
    days, d = [], start.replace(hour=0, minute=0, second=0, microsecond=0)
    while d < end_exclusive:
        days.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=1)
    return days


def _unzip_first(data: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        return zf.read(zf.namelist()[0]).decode("utf-8")


def parse_kline_csv(text: str) -> pd.DataFrame:
    """Parses a Binance Vision kline CSV (with or without header row)."""
    first = text.split("\n", 1)[0]
    has_header = first.lower().startswith("open_time")
    df = pd.read_csv(io.StringIO(text), header=0 if has_header else None)
    df.columns = KLINE_COLS[: len(df.columns)]
    df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()].copy()
    if df.empty:
        return pd.DataFrame(columns=KLINE_OUT)
    df["open_time"] = _norm_ms(df["open_time"])
    df["close_time"] = _norm_ms(df["close_time"])
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype("int64")
    for c in ("open", "high", "low", "close", "volume", "quote_volume", "taker_buy_volume", "taker_buy_quote_volume"):
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")
    return df[KLINE_OUT]


def parse_kline_rest(rows: Sequence[Sequence]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=KLINE_OUT)
    df = pd.DataFrame(rows, columns=KLINE_COLS)
    df["open_time"] = _norm_ms(df["open_time"])
    df["close_time"] = _norm_ms(df["close_time"])
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype("int64")
    for c in ("open", "high", "low", "close", "volume", "quote_volume", "taker_buy_volume", "taker_buy_quote_volume"):
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")
    return df[KLINE_OUT]


def parse_metrics_csv(text: str) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(text))
    if "create_time" not in df.columns:
        return pd.DataFrame(columns=METRIC_COLS)
    ts = pd.to_datetime(df["create_time"], utc=True, errors="coerce")
    df = df[ts.notna()].copy()
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    df["timestamp_ms"] = ((ts[ts.notna()] - epoch) // pd.Timedelta(milliseconds=1)).astype("int64")
    for c in METRIC_COLS[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce") if c in df.columns else np.nan
    return df[METRIC_COLS]


class BinanceHistoricalFetcher:
    def __init__(self, cache_dir: str = "./data_cache", max_workers: int = 16, http: Optional[HttpClient] = None,
                 log: Callable[[str], None] = print) -> None:
        self.cache_dir = os.path.abspath(cache_dir)
        self.max_workers = max(1, max_workers)
        self.metrics_absent_days: List[str] = []
        self.http = http or HttpClient()
        self.log = log
        self.dirs = {
            "fut_klines": os.path.join(self.cache_dir, "klines_15m"),
            "spot_klines": os.path.join(self.cache_dir, "spot_klines_15m"),
            "metrics": os.path.join(self.cache_dir, "metrics_daily"),
            "funding": os.path.join(self.cache_dir, "funding_rates"),
        }
        for d in self.dirs.values():
            os.makedirs(d, exist_ok=True)

    # ------------------------------------------------------------------ cache
    def _cached(self, kind: str, key: str, url: str, parser: Callable[[str], pd.DataFrame]) -> Optional[pd.DataFrame]:
        """Returns parsed archive frame; ``None`` when the object does not exist."""
        path = os.path.join(self.dirs[kind], f"{key}.parquet")
        if os.path.exists(path):
            try:
                return pd.read_parquet(path)
            except Exception as exc:  # corrupt cache -> refetch
                self.log(f"  [CACHE] unreadable {path} ({exc}); refetching")
                os.remove(path)
        data = self.http.get_optional(url)
        if data is None:
            return None
        try:
            df = parser(_unzip_first(data))
        except Exception as exc:
            self.log(f"  [WARN] parse failure {url}: {exc}")
            return None
        tmp = path + ".tmp"
        df.to_parquet(tmp, index=False)
        os.replace(tmp, path)
        return df

    def _parallel(self, fn: Callable[[str], Optional[pd.DataFrame]], keys: Sequence[str], label: str) -> Dict[str, Optional[pd.DataFrame]]:
        out: Dict[str, Optional[pd.DataFrame]] = {}
        if not keys:
            return out
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futs = {pool.submit(fn, k): k for k in keys}
            done = 0
            for fut in as_completed(futs):
                k = futs[fut]
                try:
                    out[k] = fut.result()
                except FetchError as exc:
                    self.log(f"  [ERROR] {label} {k}: {exc}")
                    out[k] = None
                done += 1
                if done % 200 == 0 or done == len(keys):
                    self.log(f"  [FETCHER] {label}: {done}/{len(keys)}")
        return out

    # ------------------------------------------------------------------ klines
    def _fetch_klines(self, market: str, symbol: str, start: datetime, now: datetime) -> pd.DataFrame:
        kind = "fut_klines" if market == "futures" else "spot_klines"
        base = f"{VISION}/futures/um" if market == "futures" else f"{VISION}/spot"
        rest = (f"{FAPI}/fapi/v1/klines" if market == "futures" else f"{SAPI}/api/v3/klines")

        def monthly(ym: str) -> Optional[pd.DataFrame]:
            return self._cached(kind, f"{symbol}-15m-{ym}", f"{base}/monthly/klines/{symbol}/15m/{symbol}-15m-{ym}.zip", parse_kline_csv)

        def daily(ymd: str) -> Optional[pd.DataFrame]:
            return self._cached(kind, f"{symbol}-15m-{ymd}", f"{base}/daily/klines/{symbol}/15m/{symbol}-15m-{ymd}.zip", parse_kline_csv)

        cur_month_start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        months = _month_keys(start, cur_month_start)
        monthly_res = self._parallel(monthly, months, f"{symbol} {market} monthly klines")
        frames = [df for df in monthly_res.values() if df is not None and not df.empty]

        # months missing from the monthly archive (listing gaps, archive lag) -> daily objects
        # Months before listing 404 on both monthly and daily objects; only probe
        # daily objects from the month preceding the first available monthly
        # archive onwards (plus the two most recent months for archive lag).
        first_ok = next((i for i, ym in enumerate(months) if monthly_res.get(ym) is not None), None)
        daily_keys: List[str] = []
        for i, ym in enumerate(months):
            if monthly_res.get(ym) is not None:
                continue
            near_recent = i >= len(months) - 2
            after_listing = first_ok is not None and i >= first_ok - 1
            if near_recent or after_listing:
                y, m = int(ym[:4]), int(ym[5:])
                m_start = datetime(y, m, 1, tzinfo=timezone.utc)
                m_end = datetime(y + (m == 12), 1 if m == 12 else m + 1, 1, tzinfo=timezone.utc)
                daily_keys += _day_keys(max(m_start, start), min(m_end, now))
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        daily_keys += _day_keys(max(cur_month_start, start), today)
        daily_res = self._parallel(daily, daily_keys, f"{symbol} {market} daily klines")
        frames += [df for df in daily_res.values() if df is not None and not df.empty]

        df = self._merge_klines(frames)
        last_ms = int(df["open_time"].iloc[-1]) if not df.empty else _ms(start) - BAR_MS
        tail = self._rest_klines(rest, symbol, last_ms + BAR_MS, _ms(now))
        if not tail.empty:
            df = self._merge_klines([df, tail])
        df = self._repair_gaps(df, rest, symbol, now)
        return df

    def _rest_klines(self, endpoint: str, symbol: str, start_ms: int, end_ms: int) -> pd.DataFrame:
        """Closed candles in [start_ms, end_ms); the candle still forming at ``end_ms`` is never returned."""
        frames: List[pd.DataFrame] = []
        cur = start_ms
        now_ms = min(end_ms, _ms(datetime.now(timezone.utc)))
        while cur < end_ms:
            url = f"{endpoint}?symbol={symbol}&interval=15m&startTime={cur}&endTime={end_ms}&limit=1500"
            raw = self.http.get_optional(url)
            if raw is None:
                break
            rows = json.loads(raw.decode("utf-8"))
            if not isinstance(rows, list) or not rows:
                break
            part = parse_kline_rest(rows)
            part = part[part["close_time"] < now_ms]       # never emit the forming candle
            if part.empty:
                break
            frames.append(part)
            nxt = int(part["open_time"].iloc[-1]) + BAR_MS
            if nxt <= cur or len(rows) < 1500:
                break
            cur = nxt
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=KLINE_OUT)

    @staticmethod
    def _merge_klines(frames: List[pd.DataFrame]) -> pd.DataFrame:
        frames = [f for f in frames if f is not None and not f.empty]
        if not frames:
            return pd.DataFrame(columns=KLINE_OUT)
        df = pd.concat(frames, ignore_index=True)
        df = df[df["open_time"] % BAR_MS == 0]
        df = df.drop_duplicates("open_time", keep="last").sort_values("open_time").reset_index(drop=True)
        return df

    def _repair_gaps(self, df: pd.DataFrame, endpoint: str, symbol: str, now: datetime) -> pd.DataFrame:
        if len(df) < 2:
            return df
        ot = df["open_time"].to_numpy()
        gap_idx = np.where(np.diff(ot) > BAR_MS)[0]
        if gap_idx.size == 0:
            return df
        self.log(f"  [FETCHER] {symbol}: {gap_idx.size} archive gap(s); attempting REST repair")
        patches = []
        for i in gap_idx[:200]:
            patches.append(self._rest_klines(endpoint, symbol, int(ot[i]) + BAR_MS, int(ot[i + 1]) + BAR_MS - 1))
        repaired = self._merge_klines([df] + patches)
        residual = int((np.diff(repaired["open_time"].to_numpy()) > BAR_MS).sum())
        self.log(f"  [FETCHER] {symbol}: residual gaps after repair = {residual} (exchange downtime; reconstructed downstream)")
        return repaired

    def fetch_futures_klines(self, symbol: str, start_date: str, now: Optional[datetime] = None) -> pd.DataFrame:
        now = now or datetime.now(timezone.utc)
        self.log(f"[FETCHER] {symbol}: futures 15m klines from {start_date}")
        df = self._fetch_klines("futures", symbol, _utc(start_date), now)
        if df.empty:
            raise RuntimeError(f"no futures klines retrieved for {symbol}")
        self.log(f"[FETCHER] {symbol}: {len(df):,} futures bars "
                 f"({pd.to_datetime(df['open_time'].iloc[0], unit='ms', utc=True)} -> {pd.to_datetime(df['open_time'].iloc[-1], unit='ms', utc=True)})")
        return df

    def fetch_spot_klines(self, symbol: str, start_date: str, now: Optional[datetime] = None) -> pd.DataFrame:
        now = now or datetime.now(timezone.utc)
        self.log(f"[FETCHER] {symbol}: spot 15m klines from {start_date}")
        df = self._fetch_klines("spot", symbol, _utc(start_date), now)
        if df.empty:
            self.log(f"[WARN] {symbol}: no spot klines available")
            return pd.DataFrame(columns=["open_time", "spot_close", "spot_volume", "spot_taker_buy_volume"])
        out = df[["open_time", "close", "volume", "taker_buy_volume"]].rename(
            columns={"close": "spot_close", "volume": "spot_volume", "taker_buy_volume": "spot_taker_buy_volume"})
        self.log(f"[FETCHER] {symbol}: {len(out):,} spot bars")
        return out.reset_index(drop=True)

    # ------------------------------------------------------------------ metrics
    def fetch_metrics(self, symbol: str, start_date: str, now: Optional[datetime] = None, include_usdc: bool = True) -> pd.DataFrame:
        now = now or datetime.now(timezone.utc)
        start = _utc(start_date)
        self.log(f"[FETCHER] {symbol}: official futures metrics from {start_date}")
        days = _day_keys(start, now)

        def daily(sym: str) -> Callable[[str], Optional[pd.DataFrame]]:
            def _f(ymd: str) -> Optional[pd.DataFrame]:
                return self._cached("metrics", f"{sym}-metrics-{ymd}",
                                    f"{VISION}/futures/um/daily/metrics/{sym}/{sym}-metrics-{ymd}.zip", parse_metrics_csv)
            return _f

        res = self._parallel(daily(symbol), days, f"{symbol} metrics")
        # Coverage inventory: days whose archive object does not exist on the host at all.
        # Recorded here, at the fetch site, because it is the only evidence about the *source*
        # in this pipeline: a frame can come up empty through a parse or join bug, but a None
        # from _cached means Binance published no metrics archive for that day. The council
        # (verify_parquet_integrity.agent_schema) uses it to tell legitimate pre-archive
        # absence apart from fabricated coverage, so it must not be derived from the frame.
        absent = sorted(d for d, df in res.items() if df is None or df.empty)
        self.metrics_absent_days = absent
        if absent:
            self.log(f"[FETCHER] {symbol}: metrics archive absent for {len(absent)} day(s) "
                     f"({absent[0]} .. {absent[-1]})")
        frames = [df for df in res.values() if df is not None and not df.empty]
        primary = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=METRIC_COLS)
        primary = primary.drop_duplicates("timestamp_ms").sort_values("timestamp_ms").reset_index(drop=True)

        usdc_symbol = symbol[:-4] + "USDC" if symbol.endswith("USDT") else None
        if include_usdc and usdc_symbol:
            usdc_days = [d for d in days if d >= USDC_METRICS_FLOOR]
            probe = self._parallel(daily(usdc_symbol), usdc_days[-3:], f"{usdc_symbol} probe") if usdc_days else {}
            if any(v is not None for v in probe.values()):
                ures = self._parallel(daily(usdc_symbol), usdc_days, f"{usdc_symbol} metrics")
                uframes = [df for df in ures.values() if df is not None and not df.empty]
                if uframes:
                    usdc = pd.concat(uframes, ignore_index=True).drop_duplicates("timestamp_ms")
                    usdc = usdc[["timestamp_ms", "sum_open_interest", "sum_open_interest_value"]].rename(
                        columns={"sum_open_interest": "_oi_usdc", "sum_open_interest_value": "_oiv_usdc"})
                    primary = primary.merge(usdc, on="timestamp_ms", how="left")
                    # Bound addition strictly to post-floor rows and use .add(fill_value=0.0) so NaN+NaN remains NaN
                    usdc_floor_ms = _ms(_utc(USDC_METRICS_FLOOR))
                    mask = primary["timestamp_ms"] >= usdc_floor_ms
                    primary.loc[mask, "sum_open_interest"] = primary.loc[mask, "sum_open_interest"].add(
                        primary.loc[mask, "_oi_usdc"], fill_value=0.0
                    )
                    primary.loc[mask, "sum_open_interest_value"] = primary.loc[mask, "sum_open_interest_value"].add(
                        primary.loc[mask, "_oiv_usdc"], fill_value=0.0
                    )
                    primary = primary.drop(columns=["_oi_usdc", "_oiv_usdc"])
                    self.log(f"[FETCHER] {symbol}: aggregated stablecoin OI with {usdc_symbol}")

        bridge = self._rest_metrics_bridge(symbol)
        if not bridge.empty:
            last = int(primary["timestamp_ms"].max()) if not primary.empty else 0
            new = bridge[bridge["timestamp_ms"] > last]
            if not new.empty:
                primary = pd.concat([primary, new], ignore_index=True).sort_values("timestamp_ms").reset_index(drop=True)
                self.log(f"[FETCHER] {symbol}: bridged {len(new)} recent metric rows via REST")
        self.log(f"[FETCHER] {symbol}: {len(primary):,} metric snapshots")
        return primary[METRIC_COLS]

    def _rest_metrics_bridge(self, symbol: str) -> pd.DataFrame:
        endpoints = {
            "oi": (f"{FAPI}/futures/data/openInterestHist", {"sumOpenInterest": "sum_open_interest", "sumOpenInterestValue": "sum_open_interest_value"}),
            "gls": (f"{FAPI}/futures/data/globalLongShortAccountRatio", {"longShortRatio": "count_long_short_ratio"}),
            "tpos": (f"{FAPI}/futures/data/topLongShortPositionRatio", {"longShortRatio": "sum_toptrader_long_short_ratio"}),
            "tacc": (f"{FAPI}/futures/data/topLongShortAccountRatio", {"longShortRatio": "count_toptrader_long_short_ratio"}),
            "tk": (f"{FAPI}/futures/data/takerlongshortRatio", {"buySellRatio": "sum_taker_long_short_vol_ratio"}),
        }
        merged: Optional[pd.DataFrame] = None
        for _, (url, rename) in endpoints.items():
            raw = self.http.get_optional(f"{url}?symbol={symbol}&period=15m&limit=500")
            if raw is None:
                continue
            try:
                rows = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            if not isinstance(rows, list) or not rows:
                continue
            part = pd.DataFrame(rows).rename(columns={"timestamp": "timestamp_ms", **rename})
            keep = ["timestamp_ms"] + list(rename.values())
            part = part[[c for c in keep if c in part.columns]].copy()
            part["timestamp_ms"] = _norm_ms(part["timestamp_ms"])
            for c in rename.values():
                if c in part.columns:
                    part[c] = pd.to_numeric(part[c], errors="coerce")
            merged = part if merged is None else merged.merge(part, on="timestamp_ms", how="outer")
        if merged is None or "sum_open_interest" not in merged.columns:
            return pd.DataFrame(columns=METRIC_COLS)
        for c in METRIC_COLS:
            if c not in merged.columns:
                merged[c] = np.nan
        return merged[METRIC_COLS].sort_values("timestamp_ms").reset_index(drop=True)

    # ------------------------------------------------------------------ funding
    def fetch_funding_rates(self, symbol: str, start_time_ms: int) -> pd.DataFrame:
        cache = os.path.join(self.dirs["funding"], f"{symbol}_funding_rates.parquet")
        cached = pd.DataFrame(columns=["fundingTime", "fundingRate"])
        if os.path.exists(cache):
            try:
                cached = pd.read_parquet(cache)
            except Exception:
                cached = pd.DataFrame(columns=["fundingTime", "fundingRate"])
        cur = start_time_ms
        if not cached.empty:
            cur = max(cur, int(cached["fundingTime"].max()) + 1)
        rows: List[dict] = []
        self.log(f"[FETCHER] {symbol}: funding rates from {pd.to_datetime(cur, unit='ms', utc=True)}")
        while True:
            raw = self.http.get_optional(f"{FAPI}/fapi/v1/fundingRate?symbol={symbol}&startTime={cur}&limit=1000")
            if raw is None:
                break
            data = json.loads(raw.decode("utf-8"))
            if not isinstance(data, list) or not data:
                break
            rows += [{"fundingTime": int(d["fundingTime"]), "fundingRate": float(d["fundingRate"])} for d in data if d.get("fundingRate") not in (None, "")]
            if len(data) < 1000:
                break
            cur = int(data[-1]["fundingTime"]) + 1
        df = pd.concat([cached, pd.DataFrame(rows)], ignore_index=True) if rows else cached
        if df.empty:
            self.log(f"[WARN] {symbol}: no funding history")
            return pd.DataFrame(columns=["fundingTime", "fundingRate"])
        df["fundingTime"] = df["fundingTime"].astype("int64")
        df["fundingRate"] = df["fundingRate"].astype("float64")
        df = df.drop_duplicates("fundingTime").sort_values("fundingTime").reset_index(drop=True)
        tmp = cache + ".tmp"
        df.to_parquet(tmp, index=False)
        os.replace(tmp, cache)
        self.log(f"[FETCHER] {symbol}: {len(df):,} funding events")
        return df[df["fundingTime"] >= start_time_ms].reset_index(drop=True)
