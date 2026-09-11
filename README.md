# Quant Developer Assignment

A Python-based quantitative trading engine prototype implementing core requirements from the Vera Developers Quant Developer assignment.

## Features

* ATR-based grid and stop-and-reverse strategy
* Position caps and kill switch
* Technical analysis indicators:

  * SMA
  * RSI
  * ATR
  * OBV
* Macro Regime Engine with:

  * Regime scoring
  * Parameter overrides
  * Circuit breakers
* Order and state management

  * Idempotent order placement
  * Order reconciliation
  * Position and P&L tracking
  * Restart state recovery
* Backtesting

  * Bar-accurate execution
  * Slippage and transaction costs
  * Walk-forward testing
  * No-lookahead signal handling
* Async tick pipeline with bounded queues and graceful shutdown
* Retry policy with exponential backoff
* Illustrative NSE/MCX contract metadata
* Structured trade blotter and backtest report
* Automated regression tests

## Project Structure

```text
quant_engine/
├── ta.py
├── regime.py
├── execution.py
├── strategy.py
├── state.py
├── backtest.py
├── market_data.py
└── contracts.py

tests/
├── test_ta.py
├── test_strategy.py
├── test_execution.py
├── test_state.py
└── test_backtest.py

scripts/
└── sdlc_check.py

demo.py
requirements.txt
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Tests

```bash
python -m pytest -q
```

Expected result:

```text
9 passed
```

## Run Demo

```bash
python demo.py
```

The demo generates synthetic market data and runs the strategy/backtest without connecting to a live broker.

## Important Note

This submission is a paper/synthetic-data implementation.

No live trading orders are placed and no broker credentials are included. Zerodha Kite Connect, live tick vendors, and production market-data connections are represented through integration-ready abstractions because the assignment instructions do not provide broker credentials, account details, or a required live instrument/data set.

The implementation is intended to demonstrate the required engineering concepts while keeping live trading disabled.

## Engineering Approach

The project emphasizes:

* deterministic calculations
* separation of strategy, execution, state, and data concerns
* explicit risk controls
* idempotency
* restart recovery
* no-lookahead backtesting
* transaction-cost modelling
* regression testing
* asynchronous market-data handling

## Author

Quant Developer Assignment Submission
