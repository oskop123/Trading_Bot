import numpy as np
import pandas as pd


class MovingAverageCrossStrategy:
    """    
    Requires:
    symbol - A stock symbol on which to form a strategy on.
    bars - A DataFrame of bars for the above symbol.
    short_window - Lookback period for short moving average.
    long_window - Lookback period for long moving average."""

    short_window = 40
    long_window = 100

    def __init__(self, symbol, bars):
        self.symbol = symbol
        self.bars = bars
        self.signals = pd.DataFrame(index=bars.index)
        self.signals['signal'] = 0.0

    def calculate(self):
        self.signals['short_mavg'] = self.bars['Close'].rolling(
            window=MovingAverageCrossStrategy.short_window, min_periods=1, center=False).mean()

        self.signals['long_mavg'] = self.bars['Close'].rolling(
            window=MovingAverageCrossStrategy.long_window, min_periods=1, center=False).mean()

        self.signals['signal'][MovingAverageCrossStrategy.short_window:] = np.where(
            self.signals['short_mavg'][MovingAverageCrossStrategy.short_window:]
            > self.signals['long_mavg'][MovingAverageCrossStrategy.short_window:], 1.0, 0.0)

        self.signals['positions'] = self.signals['signal'].diff()
