# What this script does

The script scrapes dividends data from Nasdaq.com, standardize it and then calculates the
*market implied discount rate* using the _Gordon Growth Model_.

The higher the discount rate, the higher the risk but higher is the expected return (as this implies market data is a remunerated return).


# Usage

List of allowable tickers: [!https://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx](here)

`python main.py AAPL` to get the analysis for a single ticker

`python main.py AAPL AMZN FB` ti get the analysis for multiple tickers. There is no limit on the number of tickers in input.

`python main.py --offline name_of_the_pickle_file` to work with offline data (the pickle file is automatically generated at each online query)
