"""OX58-E2: BinanceBroker mock tests (no network).

T1: modify_sltp when the new-SL placement returns None.
    EXPECTED (bug): TypeError 'argument of type NoneType is not iterable'
    from `elif ("algoId" in new_sl_res ...)` — the Step-5 naked-guard that was
    supposed to catch this failure sits AFTER the crash line and never runs.
T2: _request honours Retry-After on 429 then succeeds on retry.
T3: _request sleeps min(Retry-After,60) on 418, returns None, no retry.

Usage:  python3 ox58_broker_mocks.py [REPO_ROOT]
"""
import io
import sys
import urllib.error
import urllib.request as urlreq
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from Engine.brokers.binance_broker import BinanceBroker  # noqa: E402

print("=== T1: modify_sltp with failed SL placement (None) ===")
b = BinanceBroker(dry_run=False, api_key="k", secret_key="s")
b._format_price = lambda sym, px, direction="nearest": round(float(px), 2)


def fake_request(method, endpoint, params=None, signed=True, max_retries=3):
    if endpoint == "/fapi/v2/account":
        return {"positions": [{"symbol": "BTCUSDT", "positionAmt": "0.5"}]}
    if endpoint == "/fapi/v1/openAlgoOrders":
        return {"orders": [{"algoId": 111, "orderType": "STOP_MARKET"}]}
    if endpoint == "/fapi/v1/algoOrder" and method == "POST":
        return None  # placement failed
    if endpoint == "/fapi/v1/algoOrder" and method == "DELETE":
        return {"status": "CANCELLED"}
    return None


b._request = fake_request
try:
    print("returned:", b.modify_sltp("BTCUSDT", 123, 60000.0, 70000.0))
except TypeError as e:
    print("TypeError RAISED:", e)

print("\n=== T2: 429 with Retry-After=7, then success ===")
b2 = BinanceBroker(dry_run=False, api_key="k", secret_key="s")
sleeps = []
b2._backoff_sleep = lambda s: sleeps.append(round(s, 2))
calls = {"n": 0}


class FakeResp:
    headers = {"X-MBX-USED-WEIGHT-1M": "10"}

    def read(self):
        return b'{"ok":1}'

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def fake_429(req, timeout=15):
    calls["n"] += 1
    if calls["n"] == 1:
        raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests",
                                     hdrs={"Retry-After": "7"},
                                     fp=io.BytesIO(b'{"code":-1003,"msg":"rate"}'))
    return FakeResp()


urlreq.urlopen = fake_429
print("result:", b2._request("GET", "/fapi/v1/ping", signed=False, max_retries=3),
      "| calls:", calls["n"], "| sleeps:", sleeps)

print("\n=== T3: 418 with Retry-After=120 (expect cap 60, no retry) ===")


def fake_418(req, timeout=15):
    calls["n"] += 1
    raise urllib.error.HTTPError(req.full_url, 418, "IP banned",
                                 hdrs={"Retry-After": "120"},
                                 fp=io.BytesIO(b"banned"))


urlreq.urlopen = fake_418
calls["n"] = 0
sleeps.clear()
print("result:", b2._request("GET", "/fapi/v1/ping", signed=False, max_retries=3),
      "| calls:", calls["n"], "| sleeps:", sleeps)
