from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass(frozen=True)
class Contract:
    exchange: str
    symbol: str
    lot_size: int
    tick_size: Decimal
    price_quotation: str
    expiry: date
    delivery_staggering: str = "N/A"

# Illustrative metadata only. Production values must come from the exchange's current contract master.
MCX_EXAMPLE = Contract("MCX", "DEMO", 1, Decimal("0.05"), "per quoted unit", date(2099, 1, 1), "contract-specific")
NSE_FO_EXAMPLE = Contract("NSE", "DEMO-FUT", 1, Decimal("0.05"), "per underlying unit", date(2099, 1, 1))

@dataclass(frozen=True)
class CostModel:
    brokerage_rate: Decimal = Decimal("0.0003")
    stt_rate: Decimal = Decimal("0.0001")
    ctt_rate: Decimal = Decimal("0.0000")

    def estimate(self, turnover: Decimal, exchange: str, sell_turnover: Decimal = Decimal("0")) -> Decimal:
        brokerage = turnover * self.brokerage_rate
        if exchange == "NSE":
            return brokerage + sell_turnover * self.stt_rate
        if exchange == "MCX":
            return brokerage + sell_turnover * self.ctt_rate
        return brokerage
