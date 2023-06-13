import websocket


class Liq:
    def __init__(self):
        self.socket = "wss://fstream.binance.com/ws/!forceOrder@arr"
        self.ws = websocket.WebSocketApp(self.socket, on_message=self.on_message, on_close=self.on_close)
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
        amount = int(self.order_quantity * self.average_price)
        print(f"==> symbol={self.symbol}")
        print(f"==> side={self.side} | ", end="")
        if self.side == "BUY":
            print("shorts liquadated")
        else:
            print("longs liquadated")

        print(f"==> order_quantity={self.order_quantity}")
        print(f"==> event_time={self.event_time}")
        print(f"==> order_last_filled_quantity={self.order_last_filled_quantity}")
        print(f"==> order_filled_accumulated_quantity={self.order_filled_accumulated_quantity}")
        print(f"==> order_trade_time={self.order_trade_time}")
        print(f"==> price={self.price}")
        print(f"==> average_price={self.average_price}")
        print(f"==> liq_amount={amount}")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    def on_message(self, ws, message):
        """Fetch liquidation Order Streams.

        __ https://binance-docs.github.io/apidocs/futures/en/#liquidation-order-streams
        """
        for item in message.split(","):
            item = item.replace("}", "").replace("{", "").replace('"', "").replace("o:s:", "s:")
            if "forceOrder" not in item:
                _item = item.split(":")
                if _item[0] == "E":
                    self.event_time = int(_item[1])
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
                    self.order_trade_time = _item[1]

        self.print_result()

    def on_close(self):
        print("closed")


liq = Liq()
liq.ws.run_forever()
