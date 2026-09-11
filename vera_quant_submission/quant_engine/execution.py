from __future__ import annotations
import time
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(str, Enum):
    NEW = "NEW"
    FILLED = "FILLED"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class Order:
    order_id: str
    client_order_id: str
    symbol: str
    side: Side
    quantity: int
    price: Decimal

@dataclass
class Fill:
    order: Order
    status: OrderStatus
    fill_price: Decimal
    fees: Decimal

class PaperBroker:
    """Deterministic broker used for tests/backtests; no network side effects."""
    def __init__(self, tick_size: Decimal = Decimal("0.05"), slippage_bps: Decimal = Decimal("1")):
        self.tick_size = tick_size
        self.slippage_bps = slippage_bps
        self.orders: dict[str, Fill] = {}

    def _round_tick(self, price: Decimal) -> Decimal:
        ticks = (price / self.tick_size).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        return ticks * self.tick_size

    def place(self, order: Order) -> Fill:
        if order.client_order_id in self.orders:
            return self.orders[order.client_order_id]
        direction = Decimal("1") if order.side is Side.BUY else Decimal("-1")
        slip = order.price * self.slippage_bps / Decimal("100000")
        fill_price = self._round_tick(order.price + direction * slip)
        fee = (fill_price * order.quantity * Decimal("0.0003")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        fill = Fill(order, OrderStatus.FILLED, fill_price, fee)
        self.orders[order.client_order_id] = fill
        return fill

    def reconcile(self) -> dict[str, Fill]:
        return dict(self.orders)

class RetryPolicy:
    def __init__(self, attempts: int = 3, base_delay: float = 0.05):
        self.attempts, self.base_delay = attempts, base_delay

    def run(self, fn):
        last = None
        for n in range(self.attempts):
            try:
                return fn()
            except Exception as exc:
                last = exc
                if n + 1 < self.attempts:
                    time.sleep(self.base_delay * (2 ** n))
        raise last
