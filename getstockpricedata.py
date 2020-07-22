import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

# start = dt.datetime(2000, 1, 1)
# end = dt.datetime(2020, 7, 20)

# dataframe = web.DataReader('AAPL', 'yahoo', start, end)
# dataframe.to_csv('aapl.csv')

df = pd.read_csv('aapl.csv', parse_dates = True, index_col = 0)
# df['100ma'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean()

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

print(df_ohlc.head())

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan = 1, colspan = 1, sharex = ax1)

# plt.show()