import numpy as np
import pandas as pd


class MovingAverageCrossStrategy:
    """    
    Requires:
    symbol - A stock symbol on which to form a strategy on.
    bars - A DataFrame of bars for the above symbol.
    short_window - Lookback period for short moving average.
    long_window - Lookback period for long moving average."""

    def __init__(self, symbol, bars, short_window, long_window):
        self.symbol = symbol
        self.bars = bars
        self.short_window = short_window
        self.long_window = long_window
        self.signals = pd.DataFrame(index=bars.index)

    def calculate(self):
        self.signals['signal'] = 0.0
        self.signals['short_mavg'] = self.bars['Close'].rolling(
            window=self.short_window, min_periods=1, center=False).mean()

        self.signals['long_mavg'] = self.bars['Close'].rolling(
            window=self.long_window, min_periods=1, center=False).mean()

        self.signals['signal'][self.short_window:] = np.where(
            self.signals['short_mavg'][self.short_window:]
            > self.signals['long_mavg'][self.short_window:], 1.0, 0.0)

        self.signals['positions'] = self.signals['signal'].diff()

        return self.signals
