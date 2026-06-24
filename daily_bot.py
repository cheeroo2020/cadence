"""
daily_bot.py — a minimal daily trading bot for Alpaca (PAPER trading).

What it does:
  Once a day, it looks at one stock, compares a short moving average to a
  longer one, and:
    - buys $10 of it if the short MA crosses above the long MA (uptrend)
    - sells the whole position if the short MA drops below the long MA

This is a learning skeleton, not a money-maker. The strategy is deliberately
simple so you can see every moving part. Run it on PAPER for weeks before you
even think about real money.

------------------------------------------------------------------------
SETUP:
  1. pip install -r requirements.txt
  2. Copy .env.example to .env and paste your Alpaca PAPER keys into it.
  3. python3 daily_bot.py
------------------------------------------------------------------------
"""

import os

from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

# Load keys from the .env file (if present). Also works with exported env vars.
load_dotenv()

# ---- Settings you can change -------------------------------------------------
SYMBOL = "AAPL"        # the stock to trade
DOLLARS_PER_BUY = 10   # how much to spend per buy (fractional shares)
SHORT_WINDOW = 5       # short moving average, in days
LONG_WINDOW = 20       # long moving average, in days
# -----------------------------------------------------------------------------

API_KEY = os.environ["ALPACA_KEY"]
API_SECRET = os.environ["ALPACA_SECRET"]

# paper=True is the safety switch — keep it True until you've tested for weeks.
trading = TradingClient(API_KEY, API_SECRET, paper=True)
data = StockHistoricalDataClient(API_KEY, API_SECRET)


def get_recent_closes(symbol, days):
    """Pull daily closing prices for the last `days` trading days."""
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=datetime.now() - timedelta(days=days * 2),  # buffer for weekends/holidays
    )
    bars = data.get_stock_bars(request).df
    closes = bars["close"].tolist()
    return closes


def moving_average(values, window):
    """Average of the last `window` values."""
    return sum(values[-window:]) / window


def currently_holding(symbol):
    """Return True if we already own this stock."""
    positions = trading.get_all_positions()
    return any(p.symbol == symbol for p in positions)


def buy(symbol, dollars):
    """Buy a dollar amount (fractional shares)."""
    order = MarketOrderRequest(
        symbol=symbol,
        notional=dollars,           # spend this many dollars, not whole shares
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
    )
    trading.submit_order(order)
    print(f"BUY  ${dollars} of {symbol}")


def sell_all(symbol):
    """Close the entire position in this stock."""
    trading.close_position(symbol)
    print(f"SELL all {symbol}")


def run():
    # 1. Only act when the market is open.
    clock = trading.get_clock()
    if not clock.is_open:
        print("Market is closed. Doing nothing.")
        return

    # 2. Get the data and compute the two moving averages.
    closes = get_recent_closes(SYMBOL, LONG_WINDOW)
    if len(closes) < LONG_WINDOW:
        print("Not enough price history yet. Doing nothing.")
        return

    short_ma = moving_average(closes, SHORT_WINDOW)
    long_ma = moving_average(closes, LONG_WINDOW)
    holding = currently_holding(SYMBOL)

    print(f"{SYMBOL}: short MA={short_ma:.2f}, long MA={long_ma:.2f}, holding={holding}")

    # 3. The decision.
    if short_ma > long_ma and not holding:
        buy(SYMBOL, DOLLARS_PER_BUY)      # uptrend and we're out -> get in
    elif short_ma < long_ma and holding:
        sell_all(SYMBOL)                  # downtrend and we're in -> get out
    else:
        print("No change. Doing nothing.")


if __name__ == "__main__":
    run()
