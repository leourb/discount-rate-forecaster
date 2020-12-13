"""Download the data from Dividata to JSON or DataFrame and calculate inputs"""

import dateparser
import pickle
import requests

from datetime import datetime
from io import BytesIO

import pandas as pd

from bs4 import BeautifulSoup


class DividendDataDownloader:
    """Download the data from Dividata.com and save it as a pickle"""

    def __init__(self, ticker, pickled_name=None):
        """
        Initialize the class with the input parameters
        :param str ticker: ticker to download and to collect the data from
        :param str pickled_name: name of the pickled_file to be processed
        """
        self.__ticker = ticker
        self.__results = None
        print(f'Getting dividend data for ticker {ticker}...')
        self.__html_downloaded_table = self.__parse_div_data_from_dividata(ticker)
        if self.__html_downloaded_table:
            self.__results = self.__build_json_table(self.__html_downloaded_table)
        if pickled_name:
            self.__write_data_to_pickle(pickled_name)

    def __parse_div_data_from_dividata(self, ticker):
        """
        Parse the data from dividata.com and store it in memory
        :param str ticker: ticker to be processed
        :return: a JSON Object with all the available data
        :rtype: dict
        """
        web_address = f'https://dividata.com/stock/{ticker.lower()}/dividend'
        downloaded_web_page = requests.get(web_address)
        soup = BeautifulSoup(downloaded_web_page.text, 'html.parser')
        table = soup.find("table", class_="table table-striped table-hover")
        try:
            parsed_table = self.__get_table_data(table)
        except AttributeError:
            print(f'It seems that {ticker} has never paid a dividend. Nothing to download.')
            return None
        return parsed_table

    def __get_table_data(self, table_object):
        """
        Take the parsed tags, read and catalog them
        :param bs4.element.Tag table_object: BS4 Table Object
        :return: a dictionary with headers and rows lists as properties
        :rtype: dict
        """
        table_rows = table_object.findAll('tr')
        output_rows = list()
        for table_row in table_rows:
            columns = table_row.findAll('td')
            output_row = list()
            for column in columns:
                output_row.append(column.text.strip())
            if not output_row:
                continue
            output_rows.append(output_row)
        table_data = {'headers': ["Ex-Dividend Date", "Dividend Amount"], 'rows': output_rows}
        return table_data

    def __format_table_content(self, row_list):
        """
        Remove the Dollar sign implicitly converting the amount in numbers and converts the dates to datetime
        :param list row_list: list of rows with format [Ex-Div Date, Amount]
        :return: a list of rows with the same format in input and a numeric amount
        :rtype: list
        """
        for row in row_list:
            try:
                row[0] = dateparser.parse(row[0])
                row[1] = float(row[1].split("$")[1])
            except IndexError:
                row[1] = 0
        return row_list

    def __build_json_table(self, parsed_table_data):
        """
        Build the JSON Table starting from the parsed data
        :param dict parsed_table_data: dictionary with the headers and the rows data
        :return: a converted JSON object
        :rtype: list
        """
        headers = parsed_table_data.get('headers', {})
        rows = self.__format_table_content(parsed_table_data.get('rows', {}))
        json_results = [dict(zip(headers, row)) for row in rows]
        return json_results

    def __write_data_to_pickle(self, filename):
        """
        Pickle the data to work offline
        :param str filename: filename of the desired pickle output
        :return: a pickled file
        :rtype: None
        """
        pickle.dump(self.__results, open(filename, 'wb'))

    def get_results(self):
        """
        Get the private variable where are stored all the results and return it
        :return: the parsed JSON results
        :rtype: dict
        """
        return self.__results

    def get_results_as_df(self):
        """
        Get the results in a DataFrame format
        :return: converted DataFrame results
        :rtype: pd.DataFrame
        """
        return pd.DataFrame(self.__results)


class YahooFinanceDownloader:
    """Download data from Yahoo! Finance from the start_date to the end_date"""

    def __init__(self, ticker, start_date, end_date=None):
        """
        Initialize the class with the given input
        :param str ticker: single ticker or list of tickers to use to download the data from Yahoo! Finance
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
        :return: a DataFrame with the parsed results
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
