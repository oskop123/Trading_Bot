import datetime
import time
import xAPIConnector
import data_storage

import pandas_datareader as pdr

from MovingAverageCrossStrategy import moving_average_cross_strategy, moving_average_cross_plot
from Portfolio import portfolio, portfolio_plot


def main():
    # enter your login credentials here
    user_id = 11096095
    password = "r7vZ9U8vsStd"
    symbols = ('EURUSD', 'EURGBP', 'EURJPY')
    short_window = 10
    long_window = 40

    # create & connect to RR socket
    client = xAPIConnector.APIClient()

    # connect to RR socket, login
    login_response = client.execute(xAPIConnector.loginCommand(userId=user_id, password=password))

    # check if user logged in correctly
    if not login_response['status']:
        print('Login failed. Error code: {0}'.format(login_response['errorCode']))
        return

    # get ssId from login response
    ssid = login_response['streamSessionId']

    # create class for data storing
    data = data_storage.DataStorage(symbols, short_window, long_window, client.commandExecute)

    # create & connect to Streaming socket with given ssID
    # and functions for processing ticks, trades, profit and tradeStatus
    sclient = xAPIConnector.APIStreamClient(ssId=ssid, tickFun=data.fetch_data)

    # subscribe for prices
    sclient.subscribePrices(symbols)

    # this is an example, make it run for 5 seconds
    time.sleep(9999)

    # gracefully close streaming socket
    sclient.disconnect()

    # gracefully close RR socket
    client.disconnect()

    '''
    # Load stock data
    initial_capital = float(10000.0)  # Initial capital
    symbol = 'AAPL'  # Stock symbol
    time_start = datetime.datetime.today() - datetime.timedelta(days=200)  # Period start
    time_stop = datetime.date.today()  # Period stop
    bars = pdr.DataReader(symbol, "yahoo", time_start, time_stop)  # Load data (daily interval)

    # Use movin average cross strategy
    signals = moving_average_cross_strategy(bars, 10, 30)  # Generate signals
    portfolio = portfolio(symbol, signals, initial_capital)  # Manage portfolio using signals

    # Plot results
    moving_average_cross_plot(signals)  # Plot strategy results
    portfolio_plot(portfolio)  # Plot portfolio value
    '''


if __name__ == "__main__":
    main()
