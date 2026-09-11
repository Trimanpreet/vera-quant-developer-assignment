# Quant Trading Engine — Vera Developers Assignment

A production-oriented, paper-trading/backtesting reference implementation based on the supplied Quant Developer instructions.

## What is implemented
- Grid and stop-and-reverse strategy engines with ATR spacing, pyramiding, position caps and kill switches.
- Technical analysis module: SMA trend, RSI momentum, ATR volatility and OBV volume; each calculation has tests and is implemented once.
- Macro Regime Engine with proxy scoring, regime states, parameter overrides and circuit breakers.
- Broker abstraction with idempotent order placement, retry/backoff, reconnect/resync hooks and a paper broker.
- Bar-accurate backtester with slippage, brokerage/taxes, walk-forward evaluation and explicit no-lookahead signal timing.
- Order/position/P&L state persistence and recovery after restart.
- Structured JSON logging and trade blotter output.
- Async market-data consumer with bounded queue/back-pressure and graceful shutdown.
- Indian-market contract metadata examples for NSE/MCX mechanics; no live credentials are included.
- Regression tests for strategy, execution, accounting and no-lookahead behaviour.
- SDLC helper script for test/lint-style checks.

## Important scope decision
The supplied document is a one-page engineering specification and does not provide a concrete ticker, dataset, capital amount, or broker credentials. Therefore this submission uses deterministic synthetic OHLCV data and a paper broker. It does **not** place real orders.

The implementation is designed so a real Kite Connect adapter and real market data can be plugged in without changing the strategy/backtest accounting core.

## Run
```bash
python -m pytest -q
python demo.py
```

The demo writes `data/trades.csv` and `data/backtest_report.json`.

## Project layout
- `quant_engine/ta.py` — technical indicators
- `quant_engine/strategy.py` — grid + stop/reverse logic
- `quant_engine/regime.py` — macro regime scoring and circuit breakers
- `quant_engine/execution.py` — orders, paper broker, idempotency and retries
- `quant_engine/backtest.py` — bar-accurate backtest engine
- `quant_engine/state.py` — persisted state/recovery
- `quant_engine/market_data.py` — async bounded market-data pipeline
- `quant_engine/contracts.py` — Indian-market contract metadata
- `demo.py` — reproducible end-to-end demonstration
- `tests/` — regression/unit tests
- `scripts/sdlc_check.py` — repeatable SDLC check

## No-lookahead rule
Signals are generated from bar `t` but orders are filled at bar `t+1` open. This prevents the strategy from using the current bar's close to trade at that same close.

## Numerical discipline
Money is represented using `Decimal` at accounting boundaries. The backtest applies explicit tick rounding, slippage and transaction costs rather than treating them as approximate.

## Real broker integration
Credentials should be supplied through environment variables/secrets in a real deployment. The repository intentionally contains no API keys, access tokens or personal credentials.
