# Daily Trading Bot

A minimal daily trading bot for Alpaca, running on **paper trading** (fake money). Built as a learning project to understand the full pipeline: market data in, strategy logic, order execution.

This is a skeleton for learning the mechanics, not a money-making system. The strategy is deliberately simple. Run it on paper for weeks before considering real money.

## Strategy

Once a day, for one stock, it compares a short moving average to a longer one:

- Buys $10 of the stock when the short MA crosses **above** the long MA (uptrend forming)
- Sells the whole position when the short MA drops **below** the long MA (uptrend fading)

Edit the settings block at the top of `daily_bot.py` to change the stock, dollar amount, or moving-average windows.

## Setup

1. Create a free account at [alpaca.markets](https://alpaca.markets) and switch to **Paper Trading**.
2. Generate paper API keys from the dashboard.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy the env template and add your keys:
   ```
   cp .env.example .env
   ```
   Then open `.env` and paste your real paper key and secret.
5. Run it:
   ```
   python3 daily_bot.py
   ```

## Notes

- `paper=True` in the code is the safety switch. It stays True until the strategy has been tested thoroughly.
- The bot only trades when US markets are open. Outside hours it prints "Market is closed" and stops — that is expected behaviour, not an error.
- Running the script once places at most one trade. To trade daily, schedule it (cron, or a GitHub Actions cron job).
- `.env` holds your keys and is gitignored. It must never be committed.

## Security

Never commit `.env` or paste keys anywhere public. If a key is ever exposed, regenerate it immediately from the Alpaca dashboard.
