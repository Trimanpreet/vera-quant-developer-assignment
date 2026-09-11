from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from decimal import Decimal
from pathlib import Path

@dataclass
class PortfolioState:
    position: int = 0
    cash: str = "100000.00"
    realized_pnl: str = "0.00"
    peak_equity: str = "100000.00"
    last_client_order_id: str = ""

    @property
    def cash_decimal(self): return Decimal(self.cash)
    @property
    def realized_decimal(self): return Decimal(self.realized_pnl)
    @property
    def peak_decimal(self): return Decimal(self.peak_equity)

class StateStore:
    def __init__(self, path: str | Path): self.path = Path(path)
    def save(self, state: PortfolioState):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(asdict(state), indent=2))
        tmp.replace(self.path)
    def load(self) -> PortfolioState:
        if not self.path.exists(): return PortfolioState()
        return PortfolioState(**json.loads(self.path.read_text()))
