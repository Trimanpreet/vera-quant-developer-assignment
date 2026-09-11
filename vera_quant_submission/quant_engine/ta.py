from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Sequence


def _check(values: Sequence[float], period: int) -> None:
    if period <= 0 or len(values) < period:
        raise ValueError("not enough observations")


def sma(values: Sequence[float], period: int) -> float:
    _check(values, period)
    return sum(values[-period:]) / period


def rsi(values: Sequence[float], period: int = 14) -> float:
    if period <= 0 or len(values) < period + 1:
        raise ValueError("not enough observations")
    gains = losses = 0.0
    window = values[-(period + 1):]
    for a, b in zip(window, window[1:]):
        delta = b - a
        if delta >= 0:
            gains += delta
        else:
            losses -= delta
    if losses == 0:
        return 100.0
    rs = (gains / period) / (losses / period)
    return 100.0 - 100.0 / (1.0 + rs)


def atr(high: Sequence[float], low: Sequence[float], close: Sequence[float], period: int = 14) -> float:
    if len(high) != len(low) or len(low) != len(close) or len(close) < period + 1:
        raise ValueError("invalid OHLC series")
    trs = []
    for i in range(1, len(close)):
        trs.append(max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1])))
    return sum(trs[-period:]) / period


def obv(close: Sequence[float], volume: Sequence[float]) -> int:
    if len(close) != len(volume) or not close:
        raise ValueError("invalid close/volume series")
    total = 0
    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            total += int(volume[i])
        elif close[i] < close[i - 1]:
            total -= int(volume[i])
    return total


def trend_signal(close: Sequence[float], fast: int = 5, slow: int = 20) -> int:
    if len(close) < slow:
        return 0
    f, s = sma(close, fast), sma(close, slow)
    return 1 if f > s else -1 if f < s else 0
