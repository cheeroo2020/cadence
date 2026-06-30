# Markets, Honestly — A Field Manual

### Module A · How markets really behave

A plain-English companion to your Cadence trading bot. You bring the curiosity; the code is run for you. Every lesson here was tested on real market data (AAPL and PTON, via Alpaca) and tied back to the three layers of your Lupine Systems project — Aiva, Rail, Cloked — so studying one teaches you the other.

Nothing in this manual is financial advice. It is a learning tool. The bot runs on paper money (fake money) by design.


## The one idea behind everything

Your trading bot and Lupine do the same four things, in the same order:

- Decide — score the options, pick a winner.  →  this is Aiva.
- Execute — carry the decision out through validated steps.  →  this is Rail.
- Record — keep a tamper-evident log of what happened.  →  this is Cloked.
- Verify — trust only what you have tested and can reproduce.  →  this is the determinism value underneath all three.

Keep that loop in mind. Every lesson below is really a lesson about one of those four steps.


## Lesson 1 — Activity is a cost

The most expensive instinct in trading is the urge to do something. Your bot's strategy traded 30 times over two years and lost money, while simply buying once and holding did nothing and won comfortably.

![Your bot (5/20) ended at $9,343. Doing nothing ended at $12,892. Same stock, same two years.](images/lesson1_equity.png)

*Your bot (5/20) ended at $9,343. Doing nothing ended at $12,892. Same stock, same two years.*

Why does action cost so much? Whipsaw (buying high and selling low as the signal flips), being in cash during the best rebounds, and — in the real world — fees, the bid/ask spread, and taxes on every trade. Action has a price tag; inaction is free.

Stretch it to five years and the pattern becomes overwhelming. The only thing that changes between these three is how often the strategy acts:

![Do nothing: +112%. Slow strategy (9 trades): +12%. Fast strategy (82 trades): −47%. Less action, far better outcome.](images/lesson1_bars.png)

*Do nothing: +112%. Slow strategy (9 trades): +12%. Fast strategy (82 trades): −47%. Less action, far better outcome.*

Trading less helped enormously — the slow strategy beat the fast one by a mile. But notice: even the disciplined, trade-rarely strategy still lost badly to doing nothing. On an asset that mostly rises and recovers, no trend rule beats holding, because to follow a trend you must sometimes sell — and every time you are out, you risk missing the rebound that makes the money.

> **Lupine bridge → Aiva** — Aiva's whole job is to decide whether and how value should move. The smartest router always keeps "don't move / hold" as a candidate option, and only acts when acting genuinely beats holding. A bot that trades on every signal is a router that moves value on every request — it bleeds value to friction. Earn the right to act.

> 🔑 **Takeaway:** Doing nothing is a strategy, and usually a strong one. Every action must beat it, or you should not take the action.


## Reference — how a moving-average crossover works

A moving average (MA) is just the average price over the last N days, recalculated daily; it smooths out the noise so you can see the direction. A fast MA uses a short window and reacts quickly; a slow MA uses a long window and reacts slowly. Your bot watches a fast 5-day and a slow 20-day average (that is what "5/20" means).

![When the fast line crosses above the slow line it is a golden cross (buy). When it crosses below, a death cross (sell). The choppy middle, where it sells low then buys back higher, is whipsaw.](images/concept_crossover.png)

*When the fast line crosses above the slow line it is a golden cross (buy). When it crosses below, a death cross (sell). The choppy middle, where it sells low then buys back higher, is whipsaw.*


## Lesson 2 — When trading earns its keep

If trend-following always loses to holding, why does anyone use it? Because not every asset goes up forever. Buy-and-hold only wins when the asset recovers. Here is PTON, which peaked near $126 and fell to under $6 — and never came back.

![Holding turned $10,000 into $2,354 (−76%). Trend-following (50/200) turned it into $5,471 (−45%) — it got you out and preserved more than twice as much.](images/lesson2_pton.png)

*Holding turned $10,000 into $2,354 (−76%). Trend-following (50/200) turned it into $5,471 (−45%) — it got you out and preserved more than twice as much.*

Be honest about what happened: trend-following still LOST money on PTON. But it lost far less, because the death cross pulled it out to cash partway down and kept it out. That is the point — trend-following is not a profit engine, it is insurance against ruin. It shines in exactly the situation where buy-and-hold is a catastrophe.

> **Lupine bridge → Aiva (exposure & failure risk)** — Aiva does not only score cost and speed — it scores the risk of getting it wrong. A route that is slightly cheaper but exposes you to ruin is not a winner. PTON is the corridor that fails; the value of a good decision layer is knowing when to stop sending value down it.

> 🔑 **Takeaway:** Trend-following is insurance, not income. Judge it by the disasters it helps you avoid, not by whether it beats a winner.


## Lesson 3 — Why most strategies fail (and how not to fool yourself)

It is dangerously easy to find a strategy that looks brilliant on past data. We tried eight different MA combinations on the first half of AAPL's history and kept the best one (a 10/50 crossover, up 39% on that stretch). Then we ran that exact "winning" combo on the second half — fresh data it had never seen.

![The combo that looked best on its tuning data (+39%) degraded to +26% on fresh data — and still lost to doing nothing (+57%). Tuning to the past does not transfer to the future.](images/lesson3_overfit.png)

*The combo that looked best on its tuning data (+39%) degraded to +26% on fresh data — and still lost to doing nothing (+57%). Tuning to the past does not transfer to the future.*

This is overfitting: tuning a strategy so tightly to past data that it memorises noise instead of learning a real pattern, then collapses on new data. The cure is simple and strict — always test on data you did not tune on ("out-of-sample"), and be suspicious of any backtest that looks too good.

> **Lupine bridge → Cloked** — Cloked exists so a decision can be checked, not just claimed. The same discipline protects you here: keep an honest, reproducible record, and never fake depth. A result you cannot reproduce on fresh data is not evidence — it is a story.

> 🔑 **Takeaway:** Always benchmark against doing nothing, always test on data you did not tune on, and distrust results that look too good.


## Lesson 4 — Risk before reward

Returns are what you brag about; drawdown is what makes you quit. Drawdown is the worst drop from a previous peak — how much pain you had to sit through. Here is the fast 5/20 strategy's pain over five years:

![The fast strategy put you through a 75% drop from its peak. Most people abandon a strategy long before that — which locks in the loss.](images/lesson4_drawdown.png)

*The fast strategy put you through a 75% drop from its peak. Most people abandon a strategy long before that — which locks in the loss.*

Two defences. First, position sizing: never put everything on one bet. Your bot buys just $10 at a time in fractional shares — intentionally tiny, so no single trade can hurt you. Second, ask "how much can I lose?" before "how much can I make?" A strategy you cannot emotionally survive is not a strategy you own.

> **Lupine bridge → Rail** — Rail is the layer of safety switches and validated steps — nothing moves except through allowed transitions. Your bot's paper=True flag and small fixed bet size are exactly that: hard guardrails that cap the damage of any single decision.

> 🔑 **Takeaway:** Decide what you can afford to lose first. Survival comes before profit.


## Glossary

| Term | Plain English |
|---|---|
| Moving average (MA) | The average price over the last N days, recalculated daily. Smooths noise to reveal direction. |
| Fast / slow MA | Fast = short window, reacts quickly. Slow = long window, reacts slowly. |
| 5/20, 50/200 | The two window lengths of a strategy: a fast MA paired with a slow MA. 50/200 trades far less often than 5/20. |
| Crossover | The moment the fast line crosses the slow line — the buy/sell trigger. |
| Golden cross | Fast crosses above slow → bullish → buy. |
| Death cross | Fast crosses below slow → bearish → sell. |
| Whipsaw | Crosses flipping back and forth in choppy markets, causing losing buy-high/sell-low trades. |
| Buy-and-hold | The "do nothing" benchmark: buy once, never sell. The bar every strategy must beat. |
| Backtest | Replaying a strategy on past prices to see how it would have done — testing before risking money. |
| Drawdown | The worst peak-to-bottom drop along the way. Measures pain and risk, not just final return. |
| Overfitting | Tuning a strategy so tightly to past data that it fails on new data. |
| In-sample / out-of-sample | Data you tuned on / fresh data you did not. A strategy must work out-of-sample to be real. |
| Position sizing | How much you put on a single trade. Small sizes cap the damage of being wrong. |
| Trend-following | Betting that a move continues (your bot). Insurance against assets that fall and stay down. |
| Mean-reversion | The opposite bet: that what moved too far snaps back. |


## What you've learned, and what's next

- Lesson 1 — activity is a cost; doing nothing usually wins.  (Aiva: earn the right to act.)
- Lesson 2 — trend-following is insurance for when assets crash.  (Aiva: score the risk of ruin.)
- Lesson 3 — test out-of-sample or you will fool yourself.  (Cloked: honest, reproducible evidence.)
- Lesson 4 — survival before profit; mind the drawdown.  (Rail: guardrails on every move.)

Module B covers the honest path to real money — diversification, index investing, fees and taxes, and the rare cases where active trading makes sense. Module C is the capstone, where you will see your bot and Lupine are the same machine. Ask for them whenever you are ready.

Reminder: educational only, not financial advice. Keep it on paper money until your understanding is well ahead of your confidence.
