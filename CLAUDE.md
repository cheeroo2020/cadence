# Project context

A minimal daily trading bot running on Alpaca **paper trading** (fake money). Built as a learning project to understand the full pipeline end to end: market data in, strategy logic, order execution. Not a money-making system — the strategy is intentionally simple so every moving part is visible.

## Current status

- Bot code is written and working: `daily_bot.py`.
- Alpaca paper connection has been tested successfully (account reachable, paper buying power confirmed).
- Keys are loaded from a local `.env` file (gitignored). `.env.example` is the committed template.
- Repo is being set up; first push to GitHub in progress.

## Strategy

For one stock, once per day, compares a short moving average (5d) to a long one (20d):
- Buy $10 (fractional) when short MA crosses above long MA.
- Sell the whole position when short MA crosses below long MA.

Settings live in the block at the top of `daily_bot.py` (symbol, dollar amount, MA windows).

## Stack

- Python 3.13
- `alpaca-py` for trading + market data
- `python-dotenv` for loading keys from `.env`

## Conventions / decisions

- `paper=True` stays hardcoded until the strategy has been tested for weeks. This is the safety switch.
- Secrets never go in code or git. `.env` is gitignored; only `.env.example` is committed.
- The bot only acts when US markets are open; outside hours it prints "Market is closed" and exits. That is expected, not a bug.

## Next steps

1. Confirm the bot still connects when reading keys from `.env` (run `python3 daily_bot.py`; expect "Market is closed" outside US hours).
2. Regenerate the Alpaca paper keys — the originals were shown in a screenshot and should be rotated as a hygiene habit.
3. Once connection is confirmed, let it run on paper and observe behaviour over time.
4. Add a daily scheduler (cron locally, or a GitHub Actions cron job) so it runs each trading day automatically.
5. Optionally prototype strategy ideas visually in TradingView (free tier) and port the buy/sell rule into the bot.

## Note if the repo is ever made public

The README and this file describe the project as a trading bot. The repo is private for now. If it's ever made public, genericize these if discretion matters.
