from binance_liquidation_feeder import BinanceLiquidationFeeder

# feeding forever
liq = BinanceLiquidationFeeder()
liq.ws.run_forever()

# If you want to notify to Discord or Slack, you can use the following code.
# liq = BinanceLiquidationFeeder(discord_webhook_url='https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#                                slack_webhook_url='https://hooks.slack.com/services/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
# liq.ws.run_forever()
