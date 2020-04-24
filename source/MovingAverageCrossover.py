import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as pdr

aapl = pdr.get_data_yahoo('AAPL', start=datetime.date(2012, 10, 1), end=datetime.date.today())

# Init. the short and long windows
short_window = 40
long_window = 100

# Init. the signals dataframe with  the signal column
signals = pd.DataFrame(index=aapl.index)
signals['signal'] = 0.0

# Create Short Simple Moving Average
signals['short_mavg'] = aapl['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

# Create Long Simple Moving Average
signals['long_mavg'] = aapl['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# Create signals
signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:],
                                            1.0, 0.0)

# Generate trading orders
signals['position'] = signals['signal'].diff()

# Plot
# Init. the figure
fig = plt.figure()

# Add a subplot anad label for y-axis
ax1 = fig.add_subplot(111, ylabel='Price in $')

# Plot the closing price
aapl['Close'].plot(ax=ax1, color='r', lw=2.)

# Plot the short and long moving averages
signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2., grid=True)

# Plot the buy signals
ax1.plot(signals.loc[signals.position == 1.0].index, signals.short_mavg[signals.position == 1.0], '^', markersize=10,
         color='m')

# Plot the sell signals
ax1.plot(signals.loc[signals.position == -1.0].index, signals.short_mavg[signals.position == -1.0], 'v', markersize=10,
         color='k')

plt.show()
