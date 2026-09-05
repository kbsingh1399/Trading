"""
================================================================================
RATE-LIMIT-AWARE HTTP CLIENT (Binance Vision archive + fapi/api REST)
================================================================================
* Exponential backoff with full jitter on transient failures.
* HTTP 429 / 418: honours ``Retry-After`` and raises a process-wide cooldown
  latch so *every* worker thread pauses (a single banned IP stalls the pool
  instead of 16 threads compounding the ban).
* HTTP 404 on the immutable archive host is a permanent negative result and is
  memoised for the life of the process.
* Retries are bounded; the final failure is surfaced (never swallowed).
================================================================================
"""

from __future__ import annotations

import random
import threading
import time
import urllib.error
import urllib.request
from typing import Optional, Set

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "*/*",
}

_RATE_LIMIT_CODES = (418, 429)
_TRANSIENT_CODES = (500, 502, 503, 504, 520, 522, 524)


class FetchError(RuntimeError):
    pass


class HttpClient:
    _global_cooldown_until: float = 0.0
    _global_lock: threading.Lock = threading.Lock()
    _global_not_found: Set[str] = set()

    def __init__(
        self,
        max_attempts: int = 6,
        base_delay: float = 0.5,
        max_delay: float = 60.0,
        timeout: float = 30.0,
        min_interval: float = 0.0,
        rate_limit_cooldown: float = 30.0,
        ban_cooldown: float = 120.0,
    ) -> None:
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.timeout = timeout
        self.min_interval = min_interval
        self.rate_limit_cooldown = rate_limit_cooldown
        self.ban_cooldown = ban_cooldown
        self._cooldown_until = 0.0
        self._lock = threading.Lock()
        self._last_call = 0.0
        self._not_found: Set[str] = set()
        self.stats = {"requests": 0, "retries": 0, "rate_limited": 0, "not_found": 0, "failed": 0}

    # ------------------------------------------------------------------ utils
    def _sleep_for_cooldown(self) -> None:
        while True:
            with HttpClient._global_lock:
                g_wait = HttpClient._global_cooldown_until - time.monotonic()
            with self._lock:
                wait = max(self._cooldown_until - time.monotonic(), g_wait)
            if wait <= 0:
                return
            time.sleep(min(wait, 5.0))

    def _throttle(self) -> None:
        if self.min_interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            wait = self._last_call + self.min_interval - now
            self._last_call = max(now, self._last_call + self.min_interval)
        if wait > 0:
            time.sleep(wait)

    def _trip_cooldown(self, seconds: float) -> None:
        until = time.monotonic() + seconds
        with HttpClient._global_lock:
            HttpClient._global_cooldown_until = max(HttpClient._global_cooldown_until, until)
        with self._lock:
            self._cooldown_until = max(self._cooldown_until, until)
            self.stats["rate_limited"] += 1

    def _backoff(self, attempt: int) -> float:
        cap = min(self.max_delay, self.base_delay * (2 ** attempt))
        return random.uniform(0, cap)

    # ------------------------------------------------------------------ API
    def get(self, url: str, timeout: Optional[float] = None, allow_404: bool = True) -> Optional[bytes]:
        """
        Returns the response body, or ``None`` on a 404 when ``allow_404``.
        Raises ``FetchError`` after exhausting retries on any other failure.
        """
        with HttpClient._global_lock:
            if url in HttpClient._global_not_found:
                return None
        with self._lock:
            if url in self._not_found:
                return None
        timeout = timeout or self.timeout
        last_exc: Optional[BaseException] = None
        for attempt in range(self.max_attempts):
            self._sleep_for_cooldown()
            self._throttle()
            with self._lock:
                self.stats["requests"] += 1
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.read()
            except urllib.error.HTTPError as e:
                last_exc = e
                if e.code == 404:
                    with HttpClient._global_lock:
                        HttpClient._global_not_found.add(url)
                    with self._lock:
                        self.stats["not_found"] += 1
                        self._not_found.add(url)
                    if allow_404:
                        return None
                    raise FetchError(f"404 {url}") from e
                if e.code in _RATE_LIMIT_CODES:
                    retry_after = e.headers.get("Retry-After") if e.headers else None
                    server_cool = 0.0
                    if retry_after:
                        try:
                            server_cool = float(retry_after)
                        except ValueError:
                            server_cool = 0.0
                    if server_cool > 0.0:
                        # Server gave explicit instruction: honor it directly (bounded only by a 2-hour emergency sanity ceiling)
                        cool = min(server_cool, 7200.0)
                    else:
                        base = self.rate_limit_cooldown if e.code == 429 else self.ban_cooldown
                        raw_cool = base * (attempt + 1)
                        cool = min(self.max_delay * 10, raw_cool)
                    self._trip_cooldown(cool)
                elif e.code in _TRANSIENT_CODES:
                    time.sleep(self._backoff(attempt))
                else:
                    raise FetchError(f"HTTP {e.code} {url}") from e
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
                last_exc = e
                time.sleep(self._backoff(attempt))
            with self._lock:
                self.stats["retries"] += 1
        with self._lock:
            self.stats["failed"] += 1
        raise FetchError(f"exhausted {self.max_attempts} attempts for {url}: {last_exc!r}")

    def get_optional(self, url: str, timeout: Optional[float] = None) -> Optional[bytes]:
        """Like ``get`` but converts a final failure into ``None`` (caller logs)."""
        try:
            return self.get(url, timeout=timeout)
        except FetchError:
            return None
