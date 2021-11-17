from datetime import date, timedelta
import pandas as pd
import pandas_market_calendars as mcal

# Does this only do weekdays, is there not prices for weekends?
def daterange(start_date, end_date):
    nyse = mcal.get_calendar('NYSE')
    valid_days = nyse.valid_days(start_date=start_date, end_date=end_date)
    valid_days = [item.date() for item in valid_days]

    for n in range(int((end_date - start_date).days)):
        if (start_date + timedelta(n)) in valid_days:
            yield start_date + timedelta(n)

# capitalize these class names?

class orderbook():
    def __init__(self, ticker_list, prices_df):
        # initialize tickers and each inner_dict that corresponds
        ticker_dict = {}  # keys are tickers

        for ticker in ticker_list:
            ticker_dict[ticker] = {
                "current_shares": 0,
                # what about there being a list of stock share objects at each ticker key, that way we can keep track of mixed purchase prices
                # current_shares is easily gotten by calling len()
                "bought_at_price": 0
            }

        self.dict = ticker_dict
        self.prices_df = prices_df

    # maybe pass price if we want ease of access with some total for asset
    def update(self, ticker, intended_amount):
        # updates the inner_dict values
        # intended_amount of shares
        pass


class data_for_analysis():

    def __init__(self, start_date, end_date):
        date_list = pd.date_range(start=start_date,end=end_date).tolist()
        self.aum_dict = dict.fromkeys(date_list)


    def calculate_current_aum(self, shares_dict, current_date, current_prices, ticker_list):
        # we do this to graph
        # caculate it then add to the ledger
        # aum_dict[datetime(current_date)] = aum
        aum_total = 0

        # don't have to pass in ticker_list but just makes it easier than using shares_dict.keys()
        for ticker in ticker_list:
            print("Current price for ticker: ", current_prices[ticker])
            aum_total += shares_dict[ticker]['current_shares'] * current_prices[ticker] # is this going to be an int or series?

        self.aum_dict[current_date] = aum_total

        return aum_total


class back_trader():

    # how to get current_prices in get_updated_allocations, outer helper function?
    # helper calculation for shares from price and percentages

    def __init__(self, trader_order_book, trader_analysis):
        self.order_book = trader_order_book
        self.analysis_obj = trader_analysis

    def strat(self, prices_df, current_date):
        # returns dict of ticker to percentage

        # the question is, load it all at once, or concatenate as we go when loading data
        # to what extent are we doing the data loading
        pass

    # why did we say to pass the aum?
    def get_updated_allocations(self, perentage_dict):
        """
        percentage_dict : keys are tickers, values is intended percentage allocation
        current_prices : keys are tickers, values are closing prices of current day
        """
        # calculations for what amount of shares to actually buy

        # call update in orderbook
        pass

    # specify param types ?
    def run(self, start_date, end_date, ticker_list):
        """
        loop over each day
        store current_aum
        call strat
        call get updated allocations
        """
        for single_date in daterange(start_date, end_date):
            date_string = single_date.strftime("%Y-%m-%d")
            print(date_string)

            # The usage of self below feels wrong
            current_prices = self.order_book.prices_df.loc[date_string]
            print("Current prices: ", current_prices)
            # takes current percentage allocation (before any reallocation)
            current_aum = self.analysis_obj.calculate_current_aum(self.order_book.dict, date_string, current_prices, ticker_list)
            print(current_aum)
            
            # uncomment once strat is implemented

            # # for every week do this at end of day? maybe yield an additional value in datarange that indicates whether it's Friday
            # # ig call it on first iteration too, with buying power as a run() param, that way the current_shares values start at something
            # percentage_dict = strat(self.order_book.prices_df, single_date) # make sure these are the necessary params
            # # should we pass anything so that we can keep track of bought_at_price
            # get_updated_allocations(percentage_dict)  # pass aum, at this point it's buying power?
