from datetime import datetime, date, timedelta

import pandas as pd
import pandas_datareader as web

from backtest import orderbook
from backtest import back_trader
from backtest import data_for_analysis

ticker_list = ['VNQ','EEM','EFA','QQQ','SPY']

# I need this to be able to work if you input a holiday
start_time = date(2009, 6, 3) # at market open?
# t=datetime.date.today()
end_time = date.today() # should this be at open or close?

stock_series = []
for ticker in ticker_list:
    prices = web.DataReader(ticker, start=start_time, end = end_time, data_source='yahoo')['Adj Close']
    # print(prices.columns)
    # prices = prices.rename(columns={'Adj Close': ticker})
    prices.name = ticker

    stock_series.append(prices) # do I have to convert from series to list

df_stocks = pd.concat(stock_series, axis=1)
print(df_stocks.head())

# should df_stocks be a param in orderbook?
new_order_book = orderbook(ticker_list, df_stocks)
new_data_analysis = data_for_analysis(start_time, end_time)

new_back_trader = back_trader(new_order_book, new_data_analysis)

# make sure only methods like these use self, good thought experiment
new_back_trader.run(start_time, end_time, ticker_list)