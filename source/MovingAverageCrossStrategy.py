import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def moving_average_cross_strategy(bars, short_window, long_window):
    """Create signals dataframeusing moving average cross strategy based on short and long windows and bars of given stock"""
    # Create signals data frame
    signals = pd.DataFrame(index=bars.index)
    signals['signal'] = 0.0
    # Add stock price
    signals['price'] = bars['Close']
    # Add moving averages
    signals['short_mavg'] = bars['Close'].rolling(
        window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = bars['Close'].rolling(
        window=long_window, min_periods=1, center=False).mean()
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    signals = signals.fillna(0.0)
    return signals


def moving_average_cross_plot(signals):
    """Plot the strategy results"""
    # Create figure
    fig = plt.figure()
    # Define Y-axis
    ax1 = fig.add_subplot(111, ylabel='Price')
    # Plot stock price
    signals['price'].plot(ax=ax1, color='r', lw=2.)
    # Plot both moving averages
    signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)
    # Plot entry and points
    ax1.plot(signals.loc[signals.positions == 1.0].index, signals.short_mavg[signals.positions == 1.0], '^',
             markersize=10, color='m')
    # Plot exit points
    ax1.plot(signals.loc[signals.positions == -1.0].index, signals.short_mavg[signals.positions == -1.0], 'v',
             markersize=10, color='k')
    # Show plot
    plt.show()
