import websocket
import datetime


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


liq = BinanceLiquidationFeeder()
liq.ws.run_forever()
