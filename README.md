# Telegram signal formats AlgoVesta reads

Example Telegram signal messages and the trade that [AlgoVesta](https://algovesta.com)'s signal parser reads from each of them: symbol, side, entry, stop-loss and take-profit targets. Use it to check whether a channel's format is supported before you connect the channel, or as a test set for your own parser.

> Trading involves substantial risk of loss. Software, not advice.

## What is in this repository?

| Path | What it is |
|---|---|
| `formats.json` | 20 synthetic messages with the parser's output for each: 13 forex/metals/index entries, 3 forex messages that are not entries, 4 crypto entries. |
| `tests/validate.py` | Consistency checks that run in CI (Python 3, no dependencies). |

None of the messages is copied from a real channel. They imitate formats that appear in public channels: free text, labelled lines, emoji bullets, entry zones, numbered target lists and one-line signals.

## How do I check my channel's format?

1. Find the example in `formats.json` closest to how your channel writes a signal.
2. Paste one real message into the free [signal parser test page](https://algovesta.com/signal-parser.html) and compare what it shows with the `expect` block.
3. In the AlgoVesta dashboard connect Telegram, pick the channel and start on paper trading (crypto) or a broker demo account (MetaTrader 5) before trading real money.

The test page is a preview. On a small share of real messages the preview and the live parser read a message differently, so judge a channel by the first signals on a paper or demo account, not by the preview alone.

## What does each field mean?

| Field | Meaning |
|---|---|
| `market` | `forex` for MetaTrader 5 symbols (FX pairs, gold, silver, indices); `crypto` for exchange pairs. |
| `intent` | Forex messages only. `ENTRY` opens a trade. `RESULT` (for example "TP1 hit +40 pips") and `MANAGEMENT` (for example "close half") never open a new trade. `NONE` means no symbol was found. |
| `symbol` | Canonical symbol. `Gold` and `GOLD` become `XAUUSD`; `BTC/USDT` and `#SOL/USDT` become `BTCUSDT` and `SOLUSDT`. Your broker's suffix is added when the order is sent. |
| `side` | `buy` or `sell`. `long` and `short` in the message mean the same. |
| `entry` / `entry_range` | One price, or a `[low, high]` zone in either order. `null` means a market order at the current price. |
| `sl` | Stop-loss price. `null` means the message has none and your bot's stop-loss setting is used. On MetaTrader 5 a trade is opened only when both a stop-loss and a take-profit are known, from the message or from your bot's pip settings. |
| `tp_list` | Targets in the order given. On MetaTrader 5 each target becomes its own position with the same stop-loss. |
| `order_type` | Forex only: `market`, `limit` or `stop`. |
| `leverage` | Crypto only, when the message states it; your bot setting and the exchange limit still apply. |

## Which formats are not in this list?

- **Crypto messages without labels.** The rule-based crypto parser reads `Entry:`, `SL:` / `Stop loss:` and `TP1:` / `Target 1:` with a colon. Other crypto layouts can still be read by an AI extractor on the live path, but that result depends on the model, so it is not listed here as a guaranteed format.
- **Numbered lists without a separator** such as `TP 1 4642`: the index can be mistaken for a price, so the parser does not read it.
- **Messages that edit an earlier signal.** Handle these by checking the channel's first signals on a paper or demo account.
- **Cancel messages** such as `Cancel the pending EURUSD buy limit` are never read as a new entry. On MT5 a cancel that names a pending order cancels the bot's waiting order for that symbol; it does not close open positions.

Every parsed signal also passes your bot's risk rules (allowed symbols, position caps, daily loss limit) before an order is placed.

## How is this file tested?

- `python tests/validate.py` (CI) checks every example: a buy has its stop-loss below and targets above the entry, a sell the other way round, targets are in order, and non-entry examples state only their intent.
- Before this file is changed, the AlgoVesta team runs every message through the production parser and the preview, and compares every field of `expect`. An example is only listed when both read the same symbol and side.

The list is reviewed every six months and whenever the parser changes.

## Related repositories

- [AlgoVesta/mcp](https://github.com/AlgoVesta/mcp): MCP server documentation for AI assistants.
- [AlgoVesta/algovesta-tradingview-templates](https://github.com/AlgoVesta/algovesta-tradingview-templates): TradingView webhook JSON templates and Pine Script examples.
- [AlgoVesta/algovesta-mcp-examples](https://github.com/AlgoVesta/algovesta-mcp-examples): Python examples that call the MCP server in paper mode.

## License

MIT. See [LICENSE](LICENSE).
