import websocket
import datetime
import configparser
import requests

config_ini = configparser.ConfigParser()
config_ini.read('../config.ini', encoding='utf-8')


class BinanceLiquidationFeeder:
    def __init__(self):
        self.socket = "wss://fstream.binance.com/ws/!forceOrder@arr"
        self.ws = websocket.WebSocketApp(
            self.socket,
            on_message=self.on_message,
            on_open=self.on_open
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

        print(f"==> order_quantity: {self.order_quantity} {self.symbol.replace('USDT', '')}")
        print(f"==> event_time: {self.event_time}")
        print(f"==> order_last_filled_quantity: {self.order_last_filled_quantity} {self.symbol.replace('USDT', '')}")
        print(f"==> order_filled_accumulated_quantity: {self.order_filled_accumulated_quantity} {self.symbol.replace('USDT', '')}")
        print(f"==> order_trade_time: {self.order_trade_time}")
        print(f"==> price: {self.price} USDT")
        print(f"==> average_price: {self.average_price} USDT")
        print(f"==> liq_amount_in_USDT: {amount} USDT")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    def notify_discord(self):
        amount = int(self.order_quantity * self.average_price)
        message = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
        message += f"==> symbol={self.symbol}\n"
        message += f"==> side={self.side} | \n"
        if self.side == "BUY":
            message += "shorts liquidated\n"
        else:
            message += "longs liquidated\n"

        message += f"==> order_quantity: {self.order_quantity} {self.symbol.replace('USDT', '')}\n"
        message += f"==> event_time: {self.event_time}\n"
        message += f"==> order_last_filled_quantity: {self.order_last_filled_quantity} " \
                   f"{self.symbol.replace('USDT', '')}\n"
        message += f"==> order_filled_accumulated_quantity: {self.order_filled_accumulated_quantity} " \
                   f"{self.symbol.replace('USDT', '')}\n"
        message += f"==> order_trade_time: {self.order_trade_time}\n"
        message += f"==> price: {self.price} USDT\n"
        message += f"==> average_price: {self.average_price} USDT\n"
        message += f"==> liq_amount_in_USDT: {amount} USDT\n"

        self.post_discord(message=message)


    def on_open(self, ws):
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
            item = item.replace("}", "").replace("{", "").replace('"', "").replace("o:s:", "s:")
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
        if config_ini.get('NOTIFY', 'DISCORD_WEBHOOK_URL') != 'YOUR_DISCORD_WEBHOOK_URL':
            self.notify_discord()

    @staticmethod
    def post_discord(
            message: str,
            webhook_url=config_ini.get('NOTIFY', 'DISCORD_WEBHOOK_URL'),
            username='binance-liquidation-feeder'
    ):
        data = {
            "content": message,
            "username": username
        }
        requests.post(webhook_url, json=data)


liq = BinanceLiquidationFeeder()
liq.ws.run_forever()
