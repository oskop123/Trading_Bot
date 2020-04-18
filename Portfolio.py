from MovingAverageCrossover import signals as signals
from MovingAverageCrossover import aapl as aapl
import pandas as pd
import pandas_datareader as pdr

# Set the initial capital
initial_capital = float(100000.0)

# Create a dataframe 'positions'
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# Buy 100 shares
positions['AAPL'] = 100*signals['signal']

# Initialize the portfolio with value owned
portfolio = positions.multiply(aapl['Adj Close'], axis=0)

# Store the difference in shares owned
pos_diff = positions.diff()


# Add cash to portfolio
portfolio['cash'] = initial_capital - (pos_diff.multiply(aapl['Adj Close'], axis=0)).sum(axis=1).cumsum()

# Add 'holdings' to portfolio
portfolio['holdings'] = (positions.multiply(aapl['Adj Close'], axis=0)).sum(axis=1)

# Add 'total' to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Add 'returns' to portfolio
portfolio['returns'] = portfolio['total'].pct_change()
