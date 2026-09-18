"""
Bitfinex Level 3 (R0 Market-by-Order) WebSocket Feed Client.
Connects to wss://api-pub.bitfinex.com/ws/2 and streams live order updates.
"""

from __future__ import annotations
import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional
import websockets

from Engine.microstructure.l3_orderbook import L3OrderBook

logger = logging.getLogger("BitfinexL3Feed")


class BitfinexL3Feed:
    """
    Asynchronous WebSocket streaming client for Bitfinex R0 order books.
    Processes full snapshots and incremental updates, piping them into L3OrderBook.
    """

    WS_URL = "wss://api-pub.bitfinex.com/ws/2"

    def __init__(
        self,
        symbol: str = "tBTCUSD",
        orderbook: Optional[L3OrderBook] = None,
        book_len: int = 100,
        on_update_callback: Optional[Callable[[L3OrderBook], None]] = None,
    ):
        self.symbol: str = symbol
        self.book_len: int = book_len
        self.orderbook: L3OrderBook = orderbook or L3OrderBook(symbol=symbol)
        self.on_update_callback = on_update_callback
        
        self.channel_id: Optional[int] = None
        self.is_running: bool = False
        self._ws: Optional[websockets.WebSocketClientProtocol] = None
        self._task: Optional[asyncio.Task] = None
        self.snapshot_received: bool = False
        self.messages_count: int = 0
        self.last_heartbeat_time: float = 0.0

    async def connect_and_stream(self, max_duration_sec: Optional[float] = None) -> None:
        """Connect to WebSocket and stream live Level 3 book messages."""
        self.is_running = True
        sub_message = {
            "event": "subscribe",
            "channel": "book",
            "symbol": self.symbol,
            "prec": "R0",
            "freq": "F0",
            "len": str(self.book_len),
        }

        start_time = asyncio.get_event_loop().time()

        while self.is_running:
            try:
                async with websockets.connect(
                    self.WS_URL,
                    ping_interval=15,
                    ping_timeout=10,
                    close_timeout=5,
                    max_size=10_000_000,
                ) as ws:
                    self._ws = ws
                    await ws.send(json.dumps(sub_message))
                    logger.info(f"Subscribed to Bitfinex R0 feed for {self.symbol}")

                    async for raw_msg in ws:
                        if not self.is_running:
                            break

                        if max_duration_sec is not None:
                            if asyncio.get_event_loop().time() - start_time >= max_duration_sec:
                                self.is_running = False
                                break

                        self._process_raw_message(raw_msg)

            except asyncio.CancelledError:
                self.is_running = False
                break
            except Exception as e:
                logger.warning(f"WebSocket connection error: {e}. Reconnecting in 2s...")
                if not self.is_running:
                    break
                await asyncio.sleep(2.0)

    def _process_raw_message(self, raw_msg: str) -> None:
        """Parse incoming JSON payload and apply to the L3 order book."""
        try:
            data = json.loads(raw_msg)
        except Exception:
            return

        self.messages_count += 1

        # Event handshake
        if isinstance(data, dict):
            if data.get("event") == "subscribed" and data.get("channel") == "book":
                self.channel_id = data.get("chanId")
                logger.info(f"Book subscribed with channel ID: {self.channel_id}")
            return

        # Data messages: [chanId, ...]
        if isinstance(data, list) and len(data) >= 2:
            chan_id = data[0]
            if self.channel_id is not None and chan_id != self.channel_id:
                return

            payload = data[1]

            # Heartbeat
            if payload == "hb":
                self.last_heartbeat_time = asyncio.get_event_loop().time()
                return

            # Snapshot: [chanId, [ [order_id, price, amount], ... ]]
            if isinstance(payload, list) and len(payload) > 0 and isinstance(payload[0], list):
                self.orderbook.handle_snapshot(payload)
                self.snapshot_received = True
                if self.on_update_callback:
                    self.on_update_callback(self.orderbook)
                return

            # Incremental single order update: [chanId, [order_id, price, amount]]
            if isinstance(payload, list) and len(payload) >= 3:
                order_id = int(payload[0])
                price = float(payload[1])
                amount = float(payload[2])
                self.orderbook.handle_update(order_id, price, amount)
                if self.on_update_callback:
                    self.on_update_callback(self.orderbook)
                return

            # Alternative flat payload: [chanId, order_id, price, amount]
            if len(data) >= 4 and isinstance(data[1], (int, float)):
                order_id = int(data[1])
                price = float(data[2])
                amount = float(data[3])
                self.orderbook.handle_update(order_id, price, amount)
                if self.on_update_callback:
                    self.on_update_callback(self.orderbook)
                return

    def stop(self) -> None:
        """Gracefully terminate feed loop."""
        self.is_running = False
