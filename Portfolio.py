import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def portfolio(symbol, signals, initial_capital):
    """Create a portfolio based on given: stock symbol, signals from a strategy and initial capital.
    The portfolio contains: stocks values, signals, holdings, available cash, total cash and returns %."""
    # Create data frame for current positions
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions[symbol] = 100*signals['signal']
    # Create portfolio
    portfolio = positions.multiply(signals['price'], axis=0)
    # Add signals
    portfolio['signal'] = signals['positions']
    # Add the buy and sell shares commands
    pos_diff = positions.diff()
    # Add holdings
    portfolio['holdings'] = positions.multiply(signals['price'], axis=0).sum(axis=1)
    # Add cash
    portfolio['cash'] = initial_capital - pos_diff.multiply(signals['price'], axis=0).sum(axis=1).cumsum()
    # Add total amount of cash
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    # Add % change
    portfolio['returns'] = portfolio['total'].pct_change().fillna(0.0)
    return portfolio

def portfolio_plot(portfolio):
    """"Plot the given portfolio"""
    # Create figure
    fig = plt.figure()
    # Define Y-axis
    ax1 = fig.add_subplot(111, ylabel='Portfolio value')
    # Plot total value
    portfolio['total'].plot(ax=ax1, color='r', lw=2.)
    # Plot entry and points
    ax1.plot(portfolio.loc[portfolio.signal == 1.0].index, portfolio['total'][portfolio.signal == 1.0], '^',    markersize=10, color='m')
    # Plot exit points
    ax1.plot(portfolio.loc[portfolio.signal == -1.0].index, portfolio['total'][portfolio.signal == -1.0], 'v', markersize=10, color='k')
    # Show plot
    plt.show()