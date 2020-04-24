import datetime

import pandas as pd
import pandas_datareader as pdr

aapl = pdr.get_data_yahoo('AAPL',
                          start=datetime.datetime(2006, 10, 1),
                          end=datetime.datetime(2020, 3, 20))

# Return first rows of aapl
aapl.head()

# Return last rows of aapl
aapl.tail()

# Return statistics of aapl
aapl.describe()

# Save data to .csv
aapl.to_csv('AAPL.csv')

# Read data from .csv
Data = pd.read_csv('AAPL.csv', header=0, index_col='Date', parse_dates=True)

# Inspect the index
aapl.index

# Inspect the columns
aapl.columns

# Take the last 10 rows of the column 'Close'
aapl['Close'][-10:]

# Take the rows from November to December 2006
aapl.loc[pd.Timestamp('2006-11-01'):pd.Timestamp('2006-12-31')]

# Take the rows from 2007
aapl.loc['2007']

# Take the rows from nr 22 to 43
aapl.iloc[22:43]

# Take the 'Open' and 'Close' columns from the first and last day of November 2006
aapl.iloc[[22, 43], [0, 3]]

# Sample 20 random rows
aapl.sample(20)

# Resample by months
aapl.resample('M').mean()

# Add a price difference column
aapl['Diff'] = aapl.Open - aapl.Close

# Delete a column
del aapl['Diff']

# Plot the closing prices of aapl

# aapl['Close'].plot(grid=True)
# plt.show()

# Daily percentage change
daily_close = aapl['Adj Close']
daily_pct_change = daily_close.pct_change()
daily_pct_change.fillna(0, inplace=True)

# Calculate the monthly returns
monthly = aapl.resample('BM').apply(
    lambda x: x[-1])  # Resample by Bussines Month and take the last observation as value
monthly.pct_change()

# Calculate quarterly returns
quarterly = aapl.resample("4M").mean()  # Resample by 4 Months and take mean as value
quarterly.pct_change()

# Calculate daily returns
daily_close = aapl['Adj Close']
daily_pct_change = daily_close / daily_close.shift(1) - 1

# Plot the distribution of `daily_pct_c`
# daily_pct_change.hist(bins=50)
daily_pct_change.describe()
# plt.show()

# Calculate the cumulative daily returns
cum_daily_return = (1 + daily_pct_change).cumprod()
# cum_daily_return.plot()
# plt.show()

# Calculate the cumulative monthly returns
cum_monthly_return = cum_daily_return.resample('M').mean()
# cum_monthly_return.plot()
# plt.show()
