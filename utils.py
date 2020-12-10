"""Collects any utility tool for the script"""

from datetime import datetime, timedelta

from data_downloader import DividendDataDownloader, YahooFinanceDownloader


class CalculateInputs:
    """Calculates the inputs to be passed in other modules"""

    def __init__(self, ticker):
        """
        Initialize the class
        :param str ticker: ticker of the stock to download the data
        """
        self.__today = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        self.__index_data = YahooFinanceDownloader("^GSPC", self.__today).get_parsed_results()
        self.__risk_free_data = YahooFinanceDownloader("^TNX", self.__today).get_parsed_results()
        self.__ticker_data = YahooFinanceDownloader(ticker, self.__today).get_parsed_results()
        self.__index_return = self.__calculate_returns(self.__index_data)
        self.__risk_free_return = float(self.__risk_free_data["Adj Close"].tail(1).values[0]) / 100
        self.__dividend_data = DividendDataDownloader(ticker).get_results_as_df()
        self.__dividend_growth = self.__calculate_dividend_growth()
        self.__dividend_stats = self.__calculate_dividend_stats()

    def __calculate_returns(self, dataframe):
        """
        Calculate the return given a dataset
        :param pd.DataFrame dataframe: DataFrame with the series to analyze
        :return: a float with the value of the return over the period
        :rtype: float
        """
        try:
            security_return = (dataframe["Adj Close"].tail(1).values /
                               dataframe["Adj Close"].head(1).values - 1)[0]
        except IndexError:
            print("Impossible to get return for the series.")
            security_return = 0
        return security_return

    def __calculate_dividend_stats(self):
        """
        Calculate the dividend stats of the JSON data
        :return: populated dictionary
        :rtype: dict
        """
        stats = dict()
        stats['mean'] = self.__dividend_data["Dividend Amount"].mean()
        stats['median'] = self.__dividend_data["Dividend Amount"].median()
        stats['std'] = self.__dividend_data["Dividend Amount"].std()
        return stats

    def __calculate_dividend_growth(self):
        """
        Calculate dividend growth (g) to feed the model
        :return: the value of the growth of the last 4 dividends compared to last year
        :rtype: float
        """
        this_year_dividend = float(self.__dividend_data["Dividend Amount"].head(4).sum())
        last_year_dividend = float(self.__dividend_data["Dividend Amount"][5:9].sum())
        g_rate = (this_year_dividend / last_year_dividend) - 1
        return g_rate

    def get_market_return(self):
        """
        Get the calculated market return
        :return: the value of the calculated market return
        :rtype: float
        """
        return self.__index_return

    def get_risk_free_return(self):
        """
        Get the calculated risk-free return
        :return: the value of the calculated risk-free return
        :rtype: float
        """
        return self.__risk_free_return

    def get_risk_free_data(self):
        """
        Get the downloaded risk-free data
        :return: downloaded Risk-Free data
        :rtype: pd.DataFrame
        """
        return self.__risk_free_data

    def get_market_data(self):
        """
        Get the downloaded index data
        :return: downloaded index data
        :rtype: pd.DataFrame
        """
        return self.__index_data

    def get_ticker_data(self):
        """
        Get the downloaded ticker data
        :return: downloaded index data
        :rtype: pd.DataFrame
        """
        return self.__ticker_data

    def get_dividend_stats(self):
        """
        Get the calculated dividend stats
        :return: calculated dividend stats
        :rtype: dict
        """
        return self.__dividend_stats

    def get_dividend_growth(self):
        """
        Get the calculated dividend growth
        :return: calculated dividend growth
        :rtype: float
        """
        return self.__dividend_growth

    def get_dividend_data(self):
        """
        Get the downloaded dividend data
        :return: downloaded dividend data
        :rtype: dict
        """
        return self.__dividend_data
