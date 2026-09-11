from __future__ import annotations
import csv, json
from dataclasses import dataclass, asdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from .execution import Order, Side, PaperBroker
from .strategy import GridStopReverseStrategy
from .regime import MacroRegimeEngine

@dataclass(frozen=True)
class Bar:
    timestamp: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int

class Backtester:
    def __init__(self, strategy: GridStopReverseStrategy, broker: PaperBroker | None = None, starting_cash=Decimal("100000")):
        self.strategy, self.broker = strategy, broker or PaperBroker()
        self.starting_cash = starting_cash

    def run(self, bars: list[Bar], macro: MacroRegimeEngine | None = None):
        cash = self.starting_cash
        position = 0
        avg_cost = Decimal("0")
        peak = cash
        trades = []
        regime_engine = macro or MacroRegimeEngine()
        for i in range(1, len(bars)):
            history = bars[:i]  # current bar excluded from signal inputs
            if len(history) < 21: continue
            regime = regime_engine.evaluate({"risk_proxy": Decimal("0.1")})
            signal = self.strategy.signal(
                [float(x.high) for x in history], [float(x.low) for x in history], [float(x.close) for x in history],
                position, peak, cash + position * bars[i-1].close, Decimal(str(regime.multiplier))
            )
            if not signal.side or not signal.quantity: continue
            # Signal from bar i-1 is filled at bar i open => no lookahead.
            order = Order(f"ord-{i}", f"client-{bars[i].timestamp}-{signal.side.value}", "DEMO", signal.side, signal.quantity, bars[i].open)
            fill = self.broker.place(order)
            signed_qty = signal.quantity if signal.side is Side.BUY else -signal.quantity
            cash -= fill.fill_price * signed_qty
            cash -= fill.fees
            position += signed_qty
            if position:
                avg_cost = ((avg_cost * (position - signed_qty)) + fill.fill_price * signed_qty) / position if position != signed_qty else fill.fill_price
            equity = cash + position * bars[i].close
            peak = max(peak, equity)
            trades.append({"timestamp": bars[i].timestamp, "side": signal.side.value, "qty": signal.quantity, "fill": str(fill.fill_price), "fees": str(fill.fees), "position": position, "equity": str(equity), "reason": signal.reason})
        final_equity = cash + position * bars[-1].close
        return {"starting_cash": str(self.starting_cash), "ending_equity": str(final_equity), "return": str((final_equity / self.starting_cash) - 1), "position": position, "trades": trades}


def walk_forward(bars: list[Bar], strategy_factory, train_size=60, test_size=30):
    reports = []
    start = 0
    while start + train_size + test_size <= len(bars):
        test = bars[start + train_size:start + train_size + test_size]
        reports.append(Backtester(strategy_factory()).run(test))
        start += test_size
    return reports
