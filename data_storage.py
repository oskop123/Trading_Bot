import symbol
import xAPIConnector


class DataStorage:
    def __init__(self, symbols, short_window, long_window, command_execute):
        self.data = {s: symbol.Symbol(short_window, long_window) for s in symbols}
        self.short_window = short_window
        self.long_window = long_window
        self.command_execute = command_execute

    def fetch_data(self, msg):  # ask or bid price ?????????????? price level??????????
        s = self.data.get(msg['data']['symbol'])
        s.update(msg['data']['ask'])
        self.transaction(msg['data']['symbol'], s.return_price())

    def transaction(self, name, ask_price):
        if self.data.get(name).position == 1:
            self.buy(name, ask_price)
        if self.data.get(name).position == -1:
            self.sell(name, ask_price)

    def buy(self, name, ask_price):
        argument = {
            "tradeTransInfo": {
                "cmd": 0,
                "order": 0,
                "price": ask_price,
                "sl": 0,
                "tp": 0,
                "symbol": name,
                "type": 0,
                "volume": 0.1
            }
        }
        self.command_execute('tradeTransaction', argument)

    def sell(self, name, ask_price):
        argument = {
            "tradeTransInfo": {
                "cmd": 1,
                "order": 0,
                "price": ask_price,
                "sl": 0,
                "tp": 0,
                "symbol": name,
                "type": 0,
                "volume": 0.1
            }
        }
        self.command_execute('tradeTransaction', argument)