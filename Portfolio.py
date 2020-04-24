import datetime
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt

class Portfolio:
    """Keeps track of the portfolio of a stock based on signals passed by a strategy

    Requires:
    symbol - A stock symbol
    bars - A DataFrame of bars for a symbol set.
    signals - A pandas DataFrame of signals (1, 0, -1) for each symbol.
    initial_capital - The amount in cash at the start of the portfolio."""

    def __init__(self, symbol, signals, initial_capital):
        # Initialize the variables
        self.symbol = symbol
        self.bars = bars
        self.signals = signals
        self.initial_capital = float(initial_capital)
        self.positions = self.generate_positions()

    def generate_positions(self):
        # Generate positions from signals
        positions = pd.DataFrame(index=self.signals.index).fillna(0.0)
        positions[self.symbol] = 100*signals['signal']
        return positions

    def calculate(self):
        portfolio = self.positions*self.bars['Close']
        pos_diff = self.positions.diff()
        portfolio['holdings'] = (self.positions*self.bars['Close']).sum(axis=1)
        portfolio['cash'] = self.initial_capital - (pos_diff*self.bars['Close']).sum(axis=1).cumsum()
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        return portfolio
