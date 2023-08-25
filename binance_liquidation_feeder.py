import datetime

import requests
import websocket


class BinanceLiquidationFeeder:
    def __init__(self, discord_webhook_url=None, slack_webhook_url=None):
        self.socket = "wss://fstream.binance.com/ws/!forceOrder@arr"
        self.ws = websocket.WebSocketApp(
            self.socket, on_message=self.on_message, on_open=self.on_open
        )
        self.symbol: str = ""
        self.order_quantity = 0
        self.event_time: int = 0
        self.average_price: float = 0.0
        self.side = ""
        self.price: float = 0.0
        self.order_last_filled_quantity = 0.0
        self.order_filled_accumulated_quantity = 0
        self.order_trade_time = 0
        self._discord_webhook_url = discord_webhook_url
        self._slack_webhook_url = slack_webhook_url

    def print_result(self):
        """
        Print liquidated orders.
        :return: None
        """
        amount = int(self.order_quantity * self.average_price)
        print(f"==> symbol={self.symbol}")
        print(f"==> side={self.side} | ", end="")
        if self.side == "BUY":
            print("shorts liquidated")
        else:
            print("longs liquidated")

        print(
            f"==> order_quantity: {self.order_quantity} {self.symbol.replace('USDT', '')}"
        )
        print(f"==> event_time: {self.event_time}")
        print(
            f"==> order_last_filled_quantity: {self.order_last_filled_quantity} {self.symbol.replace('USDT', '')}"
        )
        print(
            f"==> order_filled_accumulated_quantity: {self.order_filled_accumulated_quantity} {self.symbol.replace('USDT', '')}"
        )
        print(f"==> order_trade_time: {self.order_trade_time}")
        print(f"==> price: {self.price} USDT")
        print(f"==> average_price: {self.average_price} USDT")
        print(f"==> liq_amount_in_USDT: {amount} USDT")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    @staticmethod
    def on_open(ws):
        """
        Message when open connection.

        :param ws: Websocket class
        :return: None
        """
        print("-+-+-+-+-Open connection-+-+-+-+-")

    def on_message(self, ws, message):
        """
        Fetch liquidation order streams.

        :param ws: Websocket class
        :param message: messages
        :return: None
        """
        for item in message.split(","):
            item = (
                item.replace("}", "")
                .replace("{", "")
                .replace('"', "")
                .replace("o:s:", "s:")
            )
            if "forceOrder" not in item:
                _item = item.split(":")
                if _item[0] == "E":
                    timestamp_sec = int(_item[1]) / 1000
                    jst = datetime.timezone(datetime.timedelta(hours=9))
                    japan_time = datetime.datetime.fromtimestamp(timestamp_sec, jst)
                    self.event_time = japan_time
                elif _item[0] == "s":
                    self.symbol = _item[1]
                elif _item[0] == "S":
                    self.side = _item[1]
                elif _item[0] == "q":
                    self.order_quantity = float(_item[1])
                elif _item[0] == "p":
                    self.price = _item[1]
                elif _item[0] == "ap":
                    self.average_price = float(_item[1])
                elif _item[0] == "l":
                    self.order_last_filled_quantity = _item[1]
                elif _item[0] == "z":
                    self.order_filled_accumulated_quantity = _item[1]
                elif _item[0] == "T":
                    timestamp_sec = int(_item[1]) / 1000
                    jst = datetime.timezone(datetime.timedelta(hours=9))
                    japan_time = datetime.datetime.fromtimestamp(timestamp_sec, jst)
                    self.order_trade_time = japan_time

        self.print_result()
        if self._discord_webhook_url is not None:
            self.post_discord()
        if self._slack_webhook_url is not None:
            self.post_slack()

    def post_discord(self, username="binance-liquidation-feeder"):
        data = {
            "username": username,
            "embeds": [
                {
                    "title": "Liquidated!",
                    "color": 0x206694 if self.side == "BUY" else 0x992D22,
                    "fields": [
                        {"name": "symbol", "value": self.symbol, "inline": True},
                        {"name": "side", "value": self.side, "inline": True},
                        {
                            "name": "liquidated side",
                            "value": "shorts liquidated"
                            if self.side == "BUY"
                            else "longs liquidated",
                            "inline": True,
                        },
                        {
                            "name": "price",
                            "value": str(self.price) + " USDT",
                            "inline": True,
                        },
                        {
                            "name": "liq_amount_in_USDT",
                            "value": str(int(self.order_quantity * self.average_price))
                            + " USDT",
                            "inline": True,
                        },
                    ],
                }
            ],
        }
        requests.post(self._discord_webhook_url, json=data)

    def post_slack(self, username="binance-liquidation-feeder"):
        data = {
            "attachments": [
                {
                    "author_name": username,
                    "color": "good" if self.side == "BUY" else "danger",
                    "fields": [
                        {
                            "title": "symbol",
                            "value": self.symbol,
                        },
                        {
                            "title": "side",
                            "value": self.side,
                        },
                        {
                            "title": "liquidated side",
                            "value": "shorts liquidated"
                            if self.side == "BUY"
                            else "longs liquidated",
                        },
                        {
                            "title": "price",
                            "value": str(self.price) + " USDT",
                        },
                        {
                            "title": "liq_amount_in_USDT",
                            "value": str(int(self.order_quantity * self.average_price))
                            + " USDT",
                        },
                    ],
                }
            ]
        }
        requests.post(self._slack_webhook_url, json=data)


liq = BinanceLiquidationFeeder()
liq.ws.run_forever()
