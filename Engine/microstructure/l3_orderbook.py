"""
High-Performance In-Memory Level 3 (Market-by-Order) Order Book Engine.
Maintains granular order state, price-time queues, simulated limit order priority,
and microstructure latency & cancel diagnostics.
"""

from __future__ import annotations
import bisect
import time
from collections import OrderedDict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass(slots=True)
class L3Order:
    """Individual Market-by-Order record."""
    order_id: int
    price: float
    amount: float
    side: str  # 'bid' or 'ask'
    timestamp_ns: int


class PriceLevel:
    """Price level aggregating FIFO queue of individual orders."""
    __slots__ = ("price", "orders", "total_volume")

    def __init__(self, price: float):
        self.price: float = price
        self.orders: OrderedDict[int, L3Order] = OrderedDict()
        self.total_volume: float = 0.0

    def add_order(self, order: L3Order) -> None:
        if order.order_id in self.orders:
            prev_order = self.orders[order.order_id]
            self.total_volume -= prev_order.amount
        self.orders[order.order_id] = order
        self.total_volume += order.amount

    def remove_order(self, order_id: int) -> Optional[L3Order]:
        order = self.orders.pop(order_id, None)
        if order is not None:
            self.total_volume -= order.amount
            if self.total_volume < 1e-9:
                self.total_volume = 0.0
        return order

    @property
    def order_count(self) -> int:
        return len(self.orders)


@dataclass
class SimulatedOrder:
    """Simulated passive limit order tracking real-time queue position."""
    order_id: str
    side: str
    price: float
    size: float
    initial_volume_ahead: float = 0.0
    current_volume_ahead: float = 0.0
    initial_orders_ahead: int = 0
    current_orders_ahead: int = 0
    creation_time_ns: int = 0
    is_filled: bool = False
    fill_time_ns: int = 0
    preceding_order_ids: Set[int] = field(default_factory=set)

    @property
    def queue_progress_pct(self) -> float:
        if self.initial_volume_ahead <= 1e-9:
            return 100.0
        drained = self.initial_volume_ahead - self.current_volume_ahead
        return max(0.0, min(100.0, (drained / self.initial_volume_ahead) * 100.0))


class L3OrderBook:
    """
    In-memory Market-by-Order book with O(1) order lookup, sorted price ladders,
    exact FIFO queue positions, and real-time microstructure forensics.
    """

    def __init__(self, symbol: str = "tBTCUSD"):
        self.symbol: str = symbol
        self.orders: Dict[int, L3Order] = {}
        self.bids: Dict[float, PriceLevel] = {}
        self.asks: Dict[float, PriceLevel] = {}
        
        # Ascending sorted price lists for bisect search
        # Bids: [-1] is best bid
        # Asks: [0] is best ask
        self.bid_prices: List[float] = []
        self.ask_prices: List[float] = []
        
        # Simulated passive orders
        self.simulated_orders: Dict[str, SimulatedOrder] = {}
        
        # Microstructure & throughput telemetry
        self.total_updates: int = 0
        self.total_cancels: int = 0
        self.rapid_cancels: int = 0  # Cancelled in < 500ms (potential spoof/quote pull)
        self.cancel_latencies_ms: deque[float] = deque(maxlen=1000)
        self.last_update_ns: int = time.perf_counter_ns()
        self.processing_times_us: deque[float] = deque(maxlen=1000)

    def handle_snapshot(self, raw_orders: List[List[float]]) -> None:
        """Initialize book from an exchange R0 snapshot."""
        self.orders.clear()
        self.bids.clear()
        self.asks.clear()
        self.bid_prices.clear()
        self.ask_prices.clear()

        now_ns = time.perf_counter_ns()
        for item in raw_orders:
            if len(item) < 3:
                continue
            order_id = int(item[0])
            price = float(item[1])
            amount = float(item[2])
            if price > 0:
                self._add_or_update_order(order_id, price, amount, now_ns)

    def handle_update(self, order_id: int, price: float, amount: float) -> None:
        """
        Process an incremental R0 update message.
        Bitfinex Protocol semantics:
        - price > 0: Add or update order
        - price == 0: Delete / cancel / execute order
        """
        t0 = time.perf_counter_ns()
        self.total_updates += 1

        if price == 0.0 or price == 0:
            self._remove_order(order_id, t0)
        else:
            self._add_or_update_order(order_id, price, amount, t0)

        elapsed_us = (time.perf_counter_ns() - t0) / 1000.0
        self.processing_times_us.append(elapsed_us)
        self.last_update_ns = t0

    def _add_or_update_order(self, order_id: int, price: float, amount: float, timestamp_ns: int) -> None:
        side = "bid" if amount > 0 else "ask"
        abs_amount = abs(amount)

        if order_id in self.orders:
            existing_order = self.orders[order_id]
            old_price = existing_order.price
            old_side = existing_order.side

            # Price changed: move across price levels
            if old_price != price or old_side != side:
                self._remove_from_ladder(existing_order)
                new_order = L3Order(order_id, price, abs_amount, side, timestamp_ns)
                self.orders[order_id] = new_order
                self._insert_into_ladder(new_order)
            else:
                # Size changed at same price
                delta = abs_amount - existing_order.amount
                existing_order.amount = abs_amount
                ladder = self.bids if side == "bid" else self.asks
                if price in ladder:
                    ladder[price].total_volume += delta
                self._on_order_modified(order_id, price, side, delta)
        else:
            new_order = L3Order(order_id, price, abs_amount, side, timestamp_ns)
            self.orders[order_id] = new_order
            self._insert_into_ladder(new_order)

    def _remove_order(self, order_id: int, timestamp_ns: int) -> None:
        order = self.orders.pop(order_id, None)
        if order is None:
            return

        self._remove_from_ladder(order)
        self.total_cancels += 1
        lifetime_ms = (timestamp_ns - order.timestamp_ns) / 1_000_000.0
        self.cancel_latencies_ms.append(lifetime_ms)

        if lifetime_ms < 500.0:
            self.rapid_cancels += 1

        self._on_order_cancelled_or_executed(order)

    def _insert_into_ladder(self, order: L3Order) -> None:
        price = order.price
        if order.side == "bid":
            if price not in self.bids:
                self.bids[price] = PriceLevel(price)
                bisect.insort(self.bid_prices, price)
            self.bids[price].add_order(order)
        else:
            if price not in self.asks:
                self.asks[price] = PriceLevel(price)
                bisect.insort(self.ask_prices, price)
            self.asks[price].add_order(order)

    def _remove_from_ladder(self, order: L3Order) -> None:
        price = order.price
        if order.side == "bid":
            level = self.bids.get(price)
            if level is not None:
                level.remove_order(order.order_id)
                if level.order_count == 0:
                    del self.bids[price]
                    idx = bisect.bisect_left(self.bid_prices, price)
                    if idx < len(self.bid_prices) and self.bid_prices[idx] == price:
                        self.bid_prices.pop(idx)
        else:
            level = self.asks.get(price)
            if level is not None:
                level.remove_order(order.order_id)
                if level.order_count == 0:
                    del self.asks[price]
                    idx = bisect.bisect_left(self.ask_prices, price)
                    if idx < len(self.ask_prices) and self.ask_prices[idx] == price:
                        self.ask_prices.pop(idx)

    # ------------------ Simulated Limit Order & Queue Tracking ------------------

    def place_simulated_order(self, sim_id: str, side: str, price: float, size: float) -> SimulatedOrder:
        """Place a simulated passive order and snapshot the exact orders ahead in the queue."""
        now_ns = time.perf_counter_ns()
        ladder = self.bids if side == "bid" else self.asks
        level = ladder.get(price)

        vol_ahead = 0.0
        orders_ahead = 0
        preceding_ids: Set[int] = set()

        if level is not None:
            vol_ahead = level.total_volume
            orders_ahead = level.order_count
            preceding_ids = set(level.orders.keys())

        sim_order = SimulatedOrder(
            order_id=sim_id,
            side=side,
            price=price,
            size=size,
            initial_volume_ahead=vol_ahead,
            current_volume_ahead=vol_ahead,
            initial_orders_ahead=orders_ahead,
            current_orders_ahead=orders_ahead,
            creation_time_ns=now_ns,
            preceding_order_ids=preceding_ids,
        )
        self.simulated_orders[sim_id] = sim_order
        return sim_order

    def cancel_simulated_order(self, sim_id: str) -> Optional[SimulatedOrder]:
        return self.simulated_orders.pop(sim_id, None)

    def _on_order_cancelled_or_executed(self, cancelled_order: L3Order) -> None:
        """When an order leaves the book, advance simulated queue positions if it was ahead."""
        for sim in self.simulated_orders.values():
            if sim.is_filled or sim.side != cancelled_order.side or sim.price != cancelled_order.price:
                continue

            if cancelled_order.order_id in sim.preceding_order_ids:
                sim.preceding_order_ids.discard(cancelled_order.order_id)
                sim.current_volume_ahead = max(0.0, sim.current_volume_ahead - cancelled_order.amount)
                sim.current_orders_ahead = max(0, sim.current_orders_ahead - 1)

                if sim.current_volume_ahead <= 1e-9:
                    sim.is_filled = True
                    sim.fill_time_ns = time.perf_counter_ns()

    def _on_order_modified(self, order_id: int, price: float, side: str, delta_amount: float) -> None:
        """When an order size changes ahead of us, update remaining queue volume."""
        for sim in self.simulated_orders.values():
            if sim.is_filled or sim.side != side or sim.price != price:
                continue

            if order_id in sim.preceding_order_ids:
                sim.current_volume_ahead = max(0.0, sim.current_volume_ahead + delta_amount)
                if sim.current_volume_ahead <= 1e-9:
                    sim.is_filled = True
                    sim.fill_time_ns = time.perf_counter_ns()

    # ------------------ Best Quotes & Microstructure Metrics ------------------

    def best_bid(self) -> Optional[Tuple[float, float]]:
        if not self.bid_prices:
            return None
        price = self.bid_prices[-1]
        level = self.bids.get(price)
        return (price, level.total_volume) if level else None

    def best_ask(self) -> Optional[Tuple[float, float]]:
        if not self.ask_prices:
            return None
        price = self.ask_prices[0]
        level = self.asks.get(price)
        return (price, level.total_volume) if level else None

    def spread(self) -> Optional[float]:
        bb = self.best_bid()
        ba = self.best_ask()
        if bb is None or ba is None:
            return None
        return ba[0] - bb[0]

    def spread_bps(self) -> Optional[float]:
        bb = self.best_bid()
        ba = self.best_ask()
        if bb is None or ba is None or bb[0] <= 0:
            return None
        return ((ba[0] - bb[0]) / bb[0]) * 10000.0

    def mid_price(self) -> Optional[float]:
        bb = self.best_bid()
        ba = self.best_ask()
        if bb is None or ba is None:
            return None
        return (bb[0] + ba[0]) / 2.0

    def micro_price(self) -> Optional[float]:
        """Volume-weighted micro-price reflecting order book pressure."""
        bb = self.best_bid()
        ba = self.best_ask()
        if bb is None or ba is None:
            return None
        p_bid, v_bid = bb
        p_ask, v_ask = ba
        tot = v_bid + v_ask
        if tot <= 1e-9:
            return (p_bid + p_ask) / 2.0
        return (v_bid * p_ask + v_ask * p_bid) / tot

    def order_book_imbalance(self, depth: int = 5) -> Optional[float]:
        """Normalized depth order book imbalance between -1.0 (all ask) and +1.0 (all bid)."""
        bid_vol = 0.0
        ask_vol = 0.0

        n_bids = min(depth, len(self.bid_prices))
        for i in range(1, n_bids + 1):
            p = self.bid_prices[-i]
            bid_vol += self.bids[p].total_volume

        n_asks = min(depth, len(self.ask_prices))
        for i in range(n_asks):
            p = self.ask_prices[i]
            ask_vol += self.asks[p].total_volume

        total = bid_vol + ask_vol
        if total <= 1e-9:
            return 0.0
        return (bid_vol - ask_vol) / total

    def get_ladder(self, depth: int = 5) -> Dict:
        """Retrieve top-N bid and ask levels with order counts and aggregated volumes."""
        bids_out = []
        n_bids = min(depth, len(self.bid_prices))
        for i in range(1, n_bids + 1):
            p = self.bid_prices[-i]
            level = self.bids[p]
            bids_out.append({
                "price": p,
                "volume": round(level.total_volume, 4),
                "orders": level.order_count,
            })

        asks_out = []
        n_asks = min(depth, len(self.ask_prices))
        for i in range(n_asks):
            p = self.ask_prices[i]
            level = self.asks[p]
            asks_out.append({
                "price": p,
                "volume": round(level.total_volume, 4),
                "orders": level.order_count,
            })

        return {"bids": bids_out, "asks": asks_out}

    def get_metrics(self) -> Dict:
        """Summary diagnostics and throughput metrics."""
        avg_proc_us = (
            sum(self.processing_times_us) / len(self.processing_times_us)
            if self.processing_times_us
            else 0.0
        )
        avg_cancel_life_ms = (
            sum(self.cancel_latencies_ms) / len(self.cancel_latencies_ms)
            if self.cancel_latencies_ms
            else 0.0
        )
        rapid_cancel_rate = (
            (self.rapid_cancels / self.total_cancels * 100.0)
            if self.total_cancels > 0
            else 0.0
        )

        bb = self.best_bid()
        ba = self.best_ask()

        return {
            "symbol": self.symbol,
            "total_orders": len(self.orders),
            "bid_levels": len(self.bids),
            "ask_levels": len(self.asks),
            "best_bid": bb[0] if bb else None,
            "best_bid_vol": round(bb[1], 4) if bb else None,
            "best_ask": ba[0] if ba else None,
            "best_ask_vol": round(ba[1], 4) if ba else None,
            "spread_usd": round(self.spread(), 2) if self.spread() is not None else None,
            "spread_bps": round(self.spread_bps(), 2) if self.spread_bps() is not None else None,
            "micro_price": round(self.micro_price(), 2) if self.micro_price() is not None else None,
            "obi_top5": round(self.order_book_imbalance(5), 4) if self.order_book_imbalance() is not None else None,
            "total_updates": self.total_updates,
            "total_cancels": self.total_cancels,
            "rapid_cancels_pct": round(rapid_cancel_rate, 1),
            "avg_cancel_lifetime_ms": round(avg_cancel_life_ms, 1),
            "avg_processing_latency_us": round(avg_proc_us, 2),
        }
