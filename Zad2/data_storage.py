from MovingAverageCrossoverStrategy import Macs
import xAPIConnector


class DataStorage:
    """ Store all needed data of a stock """
    def __init__(self, symbols, short_window, long_window, command_execute):
        """ symbols - stocks symbols
            short_window - length of the short moving average window
            long_window - length of the long moving average window
            command_execute - API function that executes commands"""

        # Create a new Macs object for every stock
        self.data = {s: Macs(short_window, long_window) for s in symbols}
        self.command_execute = command_execute

    def fetch_data(self, msg):
        """ Fetch data of all stocks based on:
            msg - message received from API """

        # Stock symbol
        symbol = msg['data']['symbol']
        # Ask price
        ask = msg['data']['ask']
        # Bid price
        bid = msg['data']['bid']
        # Stock to update (Macs object)
        s = self.data.get(symbol)
        # Update prices
        s.update(ask)
        # Trade
        self.transaction(symbol, ask, bid)

    def transaction(self, symbol, ask, bid):
        """ Perfom transactions based on generated signlas.
            name - name of the stock to trade
            price - price of the stock to trade """

        # Stock to trade
        stock = self.data.get(symbol)

        if stock.position == 1:
            # ZADANIE 2 <--------------------------------------------
            self.open_buy(symbol, ask)
        if stock.position == -1:
            self.close_buy(symbol, bid)
            # ZADANIE 2 <--------------------------------------------

    def open_buy(self, symbol, price):
        """ Open long position.
            symbol - symbol of the stock to trade
            price - price of the stock to trade """

        transaction = {
            "tradeTransInfo": {
                "cmd": xAPIConnector.TransactionSide.BUY,
                "order": 0,
                "price": price,
                "symbol": symbol,
                "type": xAPIConnector.TransactionType.ORDER_OPEN,
                "volume": 1
            }
        }
        response = self.command_execute('tradeTransaction', transaction)
        print('Open buy ', symbol, ' for ', price, ', status: ', response['status'])

    def close_buy(self, symbol, price):
        """ Close long position.
            symbol - symbol of the stock to trade
            price - price of the stock to trade """

        # List opened positions
        transaction = {
            "openedOnly": True
        }
        trades = self.command_execute('getTrades', transaction)
        # Get latest position
        for trade in trades['returnData']:
            if trade['symbol'] == symbol:
                last_position = trade
                break
        # Extract order ID
        order = last_position['order']

        transaction = {
            "tradeTransInfo": {
                "cmd": xAPIConnector.TransactionSide.BUY,
                "order": order,
                "price": price,
                "symbol": symbol,
                "type": xAPIConnector.TransactionType.ORDER_CLOSE,
                "volume": 1
            }
        }
        response = self.command_execute('tradeTransaction', transaction)
        print('Close buy ', symbol, ' for ', price, ', status: ', response['status'])

    # ZADANIE 2 <--------------------------------------------

    def raport(self):
        for symbol, obj in self.data.items():
            obj.raport(symbol)