import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Function to load the data from many tickers form startdate to enddate
def get(tickers, startdate, enddate):
    def data(ticker):
        return pdr.get_data_yahoo(ticker, start=startdate, end=enddate)
    datas = map(data, tickers)
    return pd.concat(datas, keys=tickers, names=['Ticker', 'Date'])

# Tickers to load
tickers = ['AAPL', 'MSFT', 'IBM', 'GOOG']
# Load the stocks
all_data = get(tickers, datetime.date(2006, 10, 1), datetime.date.today())
# Reconstruct the DataFrame to display the 'Adj Close' prices from all Tickers sorted by Date
daily_close_px = all_data['Adj Close'].reset_index().pivot('Date', 'Ticker', 'Adj Close')
# Calculate the daily percentage change for 'daily_close_px'
daily_pct_change = daily_close_px.pct_change()
# Plot the distribution
#daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))
# Show the plot
#plt.show()

# Get 'AAPL' from 'daily_close_px'
aapl = pdr.get_data_yahoo('AAPL', start=datetime.datetime(2006, 10, 1), end=datetime.date.today())
# Isolate the adjusted closing price
adj_close_px = aapl['Adj Close']
# Calculate the moving average
aapl['mov_avg_40'] = adj_close_px.rolling(window=40).mean()
aapl['mov_avg_252'] = adj_close_px.rolling(window=252).mean()
# Plot the moving averages
#aapl[['Adj Close', 'mov_avg_40', 'mov_avg_252']].plot()
#plt.show()

# Volatility calculation
min_periods = 75
vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)
#vol.plot()
#plt.show()

import statsmodels.api as sm

# Isolate the adjusted close price
all_adj_close = all_data[['Adj Close']]
# Calculate the returns
all_returns = np.log(all_adj_close / all_adj_close.shift(1))
# Isolate the AAPL returns
aapl_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'AAPL']
aapl_returns.index = aapl_returns.index.droplevel('Ticker')
# Isolate the MSFT returns
msft_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'MSFT']
msft_returns.index = msft_returns.index.droplevel('Ticker')
# Create a new data frame
return_data = pd.concat([aapl_returns, msft_returns], axis=1)[1:]
return_data.columns = ['AAPL', 'MSFT']

# Regression
X = sm.add_constant(return_data['AAPL'])
model = sm.OLS(return_data['MSFT'],X).fit()
# Plot the returns of AAPL and MSFT
plt.plot(return_data['AAPL'], return_data['MSFT'], 'r.')
ax = plt.axis()
x = np.linspace(ax[0], ax[1] + 0.01)
plt.plot(x, model.params[0] + model.params[1] * x, 'b', lw=2)
plt.grid(True)
plt.axis('tight')
plt.xlabel('Apple returns')
plt.ylabel('Microsoft returns')