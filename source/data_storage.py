from MovingAverageCrossoverStrategy import Macs
import xAPIConnector


class DataStorage:
    def __init__(self, symbols, short_window, long_window, command_execute):
        self.data = {s: Macs(short_window, long_window) for s in symbols}
        self.command_execute = command_execute

    def fetch_data(self, msg):
        s = self.data.get(msg['data']['symbol'])
        s.update(msg['data']['ask'])
        self.transaction(msg['data']['symbol'], s.current_price())

    def transaction(self, name, price):
        if self.data.get(name).position == 1:
            self.buy(name, price)
        if self.data.get(name).position == -1:
            self.sell(name, price)

    def buy(self, name, price):  # long_open
        transaction = {
            "tradeTransInfo": {
                "cmd": xAPIConnector.TransactionSide.BUY,
                "order": 0,
                "price": price,
                "symbol": name,
                "type": xAPIConnector.TransactionType.ORDER_OPEN,
                "volume": 10
            }
        }
        self.command_execute('tradeTransaction', transaction)
        print('Buy ', name, ' for ', price)

    def sell(self, name, price):  # long_close
        transaction = {
            "openedOnly": True
        }
        trades = self.command_execute('getTrades', transaction)
        order = trades['returnData'][0]['order']  # Extract the order number
        transaction = {
            "tradeTransInfo": {
                "cmd": xAPIConnector.TransactionSide.BUY,
                "order": order,
                "price": price,
                "symbol": name,
                "type": xAPIConnector.TransactionType.ORDER_CLOSE,
                "volume": 10
            }
        }
        self.command_execute('tradeTransaction', transaction)
        print('Sell ', name, ' for ', price)
