import collections
import csv
from statistics import mean
import pandas as pd
import matplotlib.pyplot as plt


class Macs:
    """ Moving Average Crossover Strategy """
    def __init__(self, short_window, long_window):
        """ short_window - short window length
            long_window - long window length """
        self.price = []
        self.long_window = long_window
        self.long_average = []
        self.short_window = short_window
        self.short_average = []
        self.last_signal = 0
        self.position = 0
        self.positions = []

    def update(self, ask):
        """ Update the price list and calculate strategy """
        self.price.append(ask)
        self.strategy()

    def strategy(self):
        """ Calculate buy/sell signals """
        if len(self.price) >= self.long_window:
            windows = self.calculate_windows()
            signal = 1 if windows[0] > windows[1] else 0
            self.position = signal - self.last_signal
            self.positions.append(self.position)
            self.last_signal = signal

    def calculate_windows(self):
        """ Calculate long and short moving averages """
        _short = mean(self.price[-self.short_window:])
        _long = mean(self.price[-self.long_window:])
        self.short_average.append(_short)
        self.long_average.append(_long)
        return _short, _long
    
    def raport(self, symbol):
        """ Save the data into a .csv file and plot """
        self.price = self.price[50:]
        df = pd.DataFrame(list(zip(*[self.price, self.short_average, self.long_average, self.positions])))
        df.columns = ['Price', 'Short average', 'Long average', 'Positions']
        df.to_csv(symbol+'.csv', index=False)

        fig = plt.figure()
        ax1 = fig.add_subplot(111,  ylabel='Price')
        # Plot price
        df['Price'].plot(ax=ax1, color='r', lw=2.)
        # Plot both averages
        df[['Short average', 'Long average']].plot(ax=ax1, lw=2.)
        # Plot the buy signals
        ax1.plot(df.loc[df.Positions == 1.0].index, 
                df['Short average'][df['Positions'] == 1.0],
                '^', markersize=10, color='m')
        # Plot the sell signals
        ax1.plot(df.loc[df.Positions == -1.0].index, 
                df['Short average'][df['Positions'] == -1.0],
                'v', markersize=10, color='k')
        plt.title(symbol)
        plt.savefig(symbol+'.png')