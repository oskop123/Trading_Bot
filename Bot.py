import datetime
import pandas as pd
import pandas_datareader as pdr
import numpy as np 
import matplotlib.pyplot as plt
from MovingAverageCrossStrategy import moving_average_cross_strategy, moving_average_cross_plot
from Portfolio import portfolio, portfolio_plot

if __name__ == "__main__":
    # Load stock data
    initial_capital = float(10000.0)                                        # Initial capital
    symbol = 'AAPL'                                                         # Stock symbol
    time_start = datetime.datetime.today() - datetime.timedelta(days=200)   # Period start
    time_stop = datetime.date.today()                                       # Period stop
    bars = pdr.DataReader(symbol, "yahoo", time_start, time_stop)           # Load data (daily interval)

    # Use movin average cross strategy
    signals = moving_average_cross_strategy(bars, 10, 30)   # Generate signals
    portfolio = portfolio(symbol, signals, initial_capital) # Manage portfolio using signals

    # Plot results
    moving_average_cross_plot(signals)  # Plot strategy results
    portfolio_plot(portfolio)           # Plot portfolio value