[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110//)
# binance-liquidation-feeder
Notify liquidation on Binance.

## Note
This is work in progress.

# Installation
```shell
pip install git+https://github.com/aoki-h-jp/binance-liquidation-feeder
```

# How to use
```python
> python feeder/feeder.py

-+-+-+-+-Open connection-+-+-+-+-
==> symbol=AXSUSDT
==> side=SELL | longs liquidated
==> order_quantity: 5.0 AXS
==> event_time: 2023-06-13 20:22:04.468000+09:00
==> order_last_filled_quantity: 5 AXS
==> order_filled_accumulated_quantity: 5 AXS
==> order_trade_time: 2023-06-13 20:22:04.464000+09:00
==> price: 4.99213 USDT
==> average_price: 5.021 USDT
==> liq_amount_in_USDT: 25 USDT
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
==> symbol=SOLUSDT
==> side=SELL | longs liquidated
==> order_quantity: 16.0 SOL
==> event_time: 2023-06-13 20:22:12.219000+09:00
==> order_last_filled_quantity: 16 SOL
==> order_filled_accumulated_quantity: 16 SOL
==> order_trade_time: 2023-06-13 20:22:12.214000+09:00
==> price: 15.3217 USDT
==> average_price: 15.476 USDT
==> liq_amount_in_USDT: 247 USDT
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

```
## Notify by discord
- Please issue a webhook URL on Discord. like https://discordapp.com/api/webhooks/XXXXXX/XXXXX
- and set the URL in `config.ini` as follows.

```shell
[NOTIFY]
DISCORD_WEBHOOK_URL = https://discordapp.com/api/webhooks/XXXXXX/XXXXX 
```

- Start up in the same way as above, and you are done!
