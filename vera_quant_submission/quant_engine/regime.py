from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Regime(str, Enum):
    RISK_ON = "risk_on"
    NEUTRAL = "neutral"
    RISK_OFF = "risk_off"

@dataclass(frozen=True)
class RegimeConfig:
    risk_on_threshold: float = 0.50
    risk_off_threshold: float = -0.50

@dataclass(frozen=True)
class RegimeState:
    score: float
    regime: Regime
    multiplier: float
    circuit_breaker: bool

class MacroRegimeEngine:
    def __init__(self, config: RegimeConfig | None = None):
        self.config = config or RegimeConfig()

    def evaluate(self, proxies: dict[str, float]) -> RegimeState:
        # Inputs are normalized proxy scores in [-1, 1]. Equal weighting avoids hidden bias.
        score = sum(proxies.values()) / len(proxies) if proxies else 0.0
        if score >= self.config.risk_on_threshold:
            regime, multiplier = Regime.RISK_ON, 1.0
        elif score <= self.config.risk_off_threshold:
            regime, multiplier = Regime.RISK_OFF, 0.5
        else:
            regime, multiplier = Regime.NEUTRAL, 0.75
        breaker = abs(score) >= 0.90
        return RegimeState(score, regime, multiplier, breaker)
