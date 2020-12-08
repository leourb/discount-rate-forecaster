"""Download the data from Nasdaq.com and convert it to JSON"""

import pickle
import requests
import time

import pandas as pd

from bs4 import BeautifulSoup


class DataDownloader:
    """Download the data from NASDAQ.com and save it as a pickle"""

    def __init__(self, tickers, pickled_name=None):
        """
        Initialize the class with the input parameters
        :param (str|list) tickers: ticker to download and to collect the data from
        :param str pickled_name: name of the pickled_file to be processed
        """
        self.__tickers = tickers
        self.__results = dict()
        for ticker in self.__tickers:
            self.__ticker_being_processed = ticker
            print(f'Getting dividend data for ticker {ticker}...')
            self.__html_downloaded_table = self.__parse_div_data_from_dividata(ticker)
            if self.__html_downloaded_table is not None:
                self.__results[self.__ticker_being_processed] = self.__build_json_table(self.__html_downloaded_table)
                time.sleep(2)  # We do not want to make the scraping too aggressive!
        if pickled_name is not None:
            self.__write_data_to_pickle(pickled_name)

    def __parse_div_data_from_dividata(self, ticker):  # Private function - it should not be called directly
        """
        Parse the data from dividata.com and store it in memory
        :param: str ticker: ticker to be processed
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

    def __remove_dollar_sign(self, row_list):
        """
        Remove the Dollar sign implicitly converting the amount in numbers
        :param row_list: list of rows with format [Ex-Div Date, Amount]
        :return: a list of rows with the same format in input and a numeric amount
        :rtype: list
        """
        for row in row_list:
            try:
                row[1] = row[1].split("$")[1]
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
        rows = self.__remove_dollar_sign(parsed_table_data.get('rows', {}))
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
        :rtype: list
        """
        list_of_results = dict()
        for i in list(self.__results.keys()):
            list_of_results[i] = pd.DataFrame(self.__results[i])
        return list_of_results
