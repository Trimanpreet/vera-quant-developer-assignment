from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from .ta import atr, trend_signal
from .execution import Side

@dataclass(frozen=True)
class StrategyConfig:
    atr_period: int = 14
    grid_atr_multiple: Decimal = Decimal("0.75")
    max_position: int = 3
    max_pyramids: int = 3
    kill_drawdown: Decimal = Decimal("0.05")

@dataclass(frozen=True)
class Signal:
    side: Side | None
    quantity: int = 0
    reason: str = ""

class GridStopReverseStrategy:
    def __init__(self, config: StrategyConfig | None = None):
        self.config = config or StrategyConfig()

    def signal(self, highs, lows, closes, position: int, peak_equity: Decimal, equity: Decimal, regime_multiplier: Decimal = Decimal("1")) -> Signal:
        if peak_equity > 0 and (peak_equity - equity) / peak_equity >= self.config.kill_drawdown:
            return Signal(None, 0, "kill_switch")
        if len(closes) < self.config.atr_period + 1:
            return Signal(None, 0, "warmup")
        a = Decimal(str(atr(highs, lows, closes, self.config.atr_period)))
        spacing = a * self.config.grid_atr_multiple
        trend = trend_signal(closes)
        if trend > 0 and position < self.config.max_position:
            qty = min(1, self.config.max_position - position)
            return Signal(Side.BUY, qty, f"grid_buy spacing={spacing:.4f} regime={regime_multiplier}")
        if trend < 0 and position > -self.config.max_position:
            qty = min(1, self.config.max_position + position)
            return Signal(Side.SELL, qty, f"grid_sell spacing={spacing:.4f} regime={regime_multiplier}")
        # Stop-and-reverse: if trend flips against an existing position, cross to the other side.
        if trend > 0 and position < 0:
            return Signal(Side.BUY, min(self.config.max_position, -position + 1), "stop_and_reverse")
        if trend < 0 and position > 0:
            return Signal(Side.SELL, min(self.config.max_position, position + 1), "stop_and_reverse")
        return Signal(None, 0, "hold")
