import bs4 as bs
import datetime as dt 
import matplotlib.pyplot as plt
from matplotlib import style
import os
import pandas as pd 
import pandas_datareader.data as web
from pandas_datareader import data as pdr
import pickle
import requests
import yfinance as yf
import seaborn as sns

style.use('ggplot')

yf.pdr_override()

def save_sp500_tickers():
	resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
	soup = bs.BeautifulSoup(resp.text)
	table = soup.find('table', {'class': 'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker)
	with open("sp500tickers.pickle", "wb") as f:
		pickle.dump(tickers, f)
	return tickers

def get_data_from_yahoo(reload_sp500 = False):
	if reload_sp500:
		tickers = save_sp500_tickers()
	else:
		with open("sp500tickers.pickle", "rb") as f:
			tickers = pickle.load(f)
	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')
	start = dt.datetime(2010, 1, 1)
	end = dt.datetime(2020, 7, 21)

	for ticker in tickers:
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = pdr.get_data_yahoo(ticker, start, end)
			df.reset_index(inplace=True)
			df.set_index("Date", inplace=True)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {}'.format(ticker))

def compile_data():
	with open("sp500tickers.pickle", "rb") as f:
		tickers = pickle.load(f)

	main_df = pd.DataFrame()

	for count, ticker in enumerate(tickers):
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		df.set_index('Date', inplace = True)

		df.rename(columns = {'Adj Close': ticker}, inplace = True)
		df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace = True)

		if main_df.empty:
			main_df = df
		else:
			main_df = main_df.join(df, how = 'outer')

		if count % 10 == 0:
			print(count)

	print(main_df.head())
	main_df.to_csv('sp500_joined_closes.csv')

def visualize_data():
	df = pd.read_csv('sp500_joined_closes.csv')
	df_corr = df.corr()
	sns.heatmap(df_corr, cmap="RdYlGn")
	plt.show()

visualize_data()

