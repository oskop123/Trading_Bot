from MovingAverageCrossoverStrategy import Macs
import xAPIConnector


class DataStorage:
    def __init__(self, symbols, short_window, long_window, command_execute):
        self.data = {s: Macs(short_window, long_window) for s in symbols}
        self.command_execute = command_execute

    def fetch_data(self, msg):
        s = self.data.get(msg['data']['symbol'])
        s.update(msg['data']['ask'])
        self.transaction(msg['data']['symbol'], s.return_price())

    def transaction(self, name, ask_price):
        if self.data.get(name).position == 1:
            self.buy(name, ask_price)
            print('Buy ', name, ' for ', ask_price)
            print(self.trade_response)
        if self.data.get(name).position == -1:
            self.sell(name, ask_price)
            print('Sell ', name, ' for ', ask_price)
            print(self.trade_response)

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
                "volume": 10
            }
        }
        self.trade_response = self.command_execute('tradeTransaction', argument)    # Open the position

    def sell(self, name, ask_price):
        argument = {
            "openedOnly": True
        }
        trades = self.command_execute('getTrades', argument)
        order = trades['returnData'][0]['order']    # Extract the order number
        argument = {
            "tradeTransInfo": {
                "cmd": 0,
                "order": order,
                "price": ask_price,
                "sl": 0,
                "tp": 0,
                "symbol": name,
                "type": 2,
                "volume": 10
            }
        }
        self.trade_response = self.command_execute('tradeTransaction', argument)    # Close the position