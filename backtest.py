"""
backtest.py -- test the bot's strategy on REAL PAST prices, risk-free.

This is the educational core. Before you ever risk money (even fake money over
weeks), you ask: "if I had run this strategy over the last couple of years,
would it have made or lost money -- and would it have beaten just buying and
holding the stock?"

It replays history day by day using the SAME rule as daily_bot.py:
  - short moving average crosses ABOVE long  -> buy (go all-in, simulated)
  - short moving average crosses BELOW long  -> sell (go to cash)

Nothing here touches your real (paper) account. It only reads old prices.

Run:  python3 backtest.py
"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# ---- Same knobs as the bot. Change these and re-run to learn. ----------------
SYMBOL = "AAPL"
SHORT_WINDOW = 5
LONG_WINDOW = 20
YEARS_BACK = 2
STARTING_CASH = 10_000   # pretend bankroll, just for the simulation
# -----------------------------------------------------------------------------

API_KEY = os.environ["ALPACA_KEY"]
API_SECRET = os.environ["ALPACA_SECRET"]
data = StockHistoricalDataClient(API_KEY, API_SECRET)


def moving_average(values, window):
    return sum(values[-window:]) / window


def get_history(symbol, years):
    req = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=datetime.now() - timedelta(days=int(years * 365)),
    )
    df = data.get_stock_bars(req).df
    closes = df["close"].tolist()
    dates = [ts.strftime("%Y-%m-%d") for ts in df.index.get_level_values("timestamp")]
    return dates, closes


def run():
    dates, closes = get_history(SYMBOL, YEARS_BACK)
    if len(closes) <= LONG_WINDOW:
        print("Not enough price history.")
        return

    # --- Strategy simulation -------------------------------------------------
    cash = STARTING_CASH
    shares = 0.0
    trades = []          # (date, side, price)
    equity_curve = []    # portfolio value each day, to measure the worst drop

    for i in range(LONG_WINDOW, len(closes)):
        window = closes[: i + 1]
        short_ma = moving_average(window, SHORT_WINDOW)
        long_ma = moving_average(window, LONG_WINDOW)
        price = closes[i]
        holding = shares > 0

        if short_ma > long_ma and not holding:
            shares = cash / price          # go all-in
            cash = 0.0
            trades.append((dates[i], "BUY", price))
        elif short_ma < long_ma and holding:
            cash = shares * price          # sell everything
            shares = 0.0
            trades.append((dates[i], "SELL", price))

        equity_curve.append(cash + shares * price)

    strategy_final = cash + shares * closes[-1]

    # --- The benchmark: just buy on day one and hold the whole time ----------
    start_price = closes[LONG_WINDOW]
    hold_shares = STARTING_CASH / start_price
    hold_final = hold_shares * closes[-1]

    # --- Worst peak-to-trough drop (max drawdown) ----------------------------
    peak = equity_curve[0]
    max_dd = 0.0
    for v in equity_curve:
        peak = max(peak, v)
        max_dd = max(max_dd, (peak - v) / peak)

    def pct(final):
        return (final / STARTING_CASH - 1) * 100

    print(f"=== BACKTEST: {SHORT_WINDOW}/{LONG_WINDOW} crossover on {SYMBOL} "
          f"({dates[LONG_WINDOW]} -> {dates[-1]}) ===\n")
    print(f"Starting cash:            ${STARTING_CASH:,.0f}\n")
    print(f"STRATEGY (the bot's rule)")
    print(f"  Final value:            ${strategy_final:,.0f}   ({pct(strategy_final):+.1f}%)")
    print(f"  Number of trades:       {len(trades)}")
    print(f"  Worst drop along way:   -{max_dd*100:.1f}%\n")
    print(f"BENCHMARK (just buy & hold, do nothing)")
    print(f"  Final value:            ${hold_final:,.0f}   ({pct(hold_final):+.1f}%)\n")

    verdict = "BEAT" if strategy_final > hold_final else "LOST TO"
    diff = abs(strategy_final - hold_final)
    print(f">>> The strategy {verdict} buy-and-hold by ${diff:,.0f}.")
    if strategy_final <= hold_final:
        print("    Lesson: the clever rule did NOT beat doing nothing. "
              "That's the most common result -- and exactly why we test first.")

    print("\nLast few simulated trades:")
    for d, side, p in trades[-6:]:
        print(f"  {d}  {side:4}  @ ${p:.2f}")


if __name__ == "__main__":
    run()
