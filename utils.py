"""Collects any utility tool for the script"""

import requests

from datetime import datetime
from io import BytesIO

import dateparser
import pandas as pd


class YahooFinanceDownloader:
    """Downloads the last N years of data from Yahoo! Finance"""

    def __init__(self, ticker, start_date, end_date=None):
        """
        Initialize the class with the given input
        :param str or list ticker: single ticker or list of tickers to use to download the data from Yahoo! Finance
        :param str start_date: start date of the query period in a string format YYYY-MM-DD (or similar)
        :param str end_date: end date of the query period in a string format YYYY-MM-DD (or similar)
        """

        self.__ticker = ticker
        self.__start_date = start_date
        self.__end_date = end_date
        self.__validate_inputs()
        self.__raw_query_results = self.__download_file()
        self.__parsed_results = self.__parse_results()

    def __validate_inputs(self):
        """
        Validates start_date and end_date and checks their congruence
        :return: formatted and validated date formats
        :rtype: None
        """
        self.__start_date = dateparser.parse(self.__start_date).timestamp()
        self.__end_date = dateparser.parse(self.__end_date).timestamp() if self.__end_date is not None \
            else datetime.today().timestamp()

    def __download_file(self):
        """
        Download the file give a set of inputs
        :return: the downloaded content of the file
        :rtype: requests.models.Response
        """

        period1 = int(self.__start_date)
        period2 = int(self.__end_date)
        self.__url = f"https://query1.finance.yahoo.com/v7/finance/download/{self.__ticker}?period1=" \
                     f"{period1}&period2={period2}&interval=1d&events=history&" \
                     f"includeAdjustedClose=true"
        return requests.get(self.__url)

    def get_raw_results(self):
        """
        Get the downloaded raw results"
        :return: a string text with the results
        :rtype: str
        """
        return self.__raw_query_results.text

    def __parse_results(self):
        """
        Parse results in a Pandas DF
        :return: a DataFrame with the parsed resutls
        :rtype: pd.DataFrame
        """
        return pd.read_csv(BytesIO(self.__download_file().content))

    def get_parsed_results(self):
        """
        Get the parsed results in a DataFrame
        :return: raw results parsed in a DataFrame
        :rtype: pd.DataFrame
        """
        return self.__parsed_results
