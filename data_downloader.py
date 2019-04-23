"""Download the data from Nasdaq.com and convert it to JSON"""

import pickle
import requests
import time

from bs4 import BeautifulSoup


class DataDownloader:
    """Download the data from NASDAQ.com and save it as a pickle"""

    def __init__(self, tickers, pickled_name=None):
        """
        Initialize the class with the input parameters

        :param (str|list) tickers: ticker to download and to collect the data from
        :param str pickled_name: name of the pickled_file to be processed
        """
        self._tickers = tickers
        self._results = dict()
        for ticker in self._tickers:
            self._ticker_being_processed = ticker
            print(f'Getting dividend data for ticker {ticker}...')
            self._results[self._ticker_being_processed] = self._parse_div_data_from_nasdaq(ticker)
            time.sleep(2)  # We do not want to make the scraping too aggressive!
        if pickled_name is not None:
            self._write_data_to_pickle(pickled_name)

    def _parse_div_data_from_nasdaq(self, ticker):  # Private function - it should not be called directly
        """
        Parse the data from NASDAQ.com and store it in memory

        :param: str ticker: ticker to be processed
        :return: a JSON Object with all the available data
        """
        web_address = f'https://www.nasdaq.com/en/symbol/{ticker.lower()}/dividend-history'
        downloaded_web_page = requests.get(web_address)
        soup = BeautifulSoup(downloaded_web_page.text, 'html.parser')
        table = soup.find('table', {'id': 'quotes_content_left_dividendhistoryGrid'})
        try:
            parsed_table = self._get_table_data(table)
        except AttributeError:
            print(f'It seems that {ticker} has never paid a dividend. Nothing to download.')
            return None
        table_to_json = self._build_json_table(parsed_table)
        return table_to_json

    def _get_table_data(self, table_object):
        """
        Take the parsed tags, read and catalog them

        :param bs4.element.Tag table_object: BS4 Table Object
        :return: a dictionary with headers and rows lists as properties
        """
        table_headers_tags = table_object.findAll('a')
        table_headers_text = [i.text for i in table_headers_tags]
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
        table_data = {'headers': table_headers_text, 'rows': output_rows}
        return table_data

    def _build_json_table(self, parsed_table_data):
        """
        Build the JSON Table starting from the parsed data

        :param dict parsed_table_data: dictionary with the headers and the rows data
        :return: a converted JSON object
        """
        headers = parsed_table_data.get('headers', {})
        rows = parsed_table_data.get('rows', {})
        json_results = [dict(zip(headers, row)) for row in rows]
        return json_results

    def _write_data_to_pickle(self, filename):
        """
        Pickle the data to work offline

        :param str filename: filename of the desired pickle output
        :return: a pickled file
        """
        pickle.dump(self._results, open(filename, 'wb'))

    def get_results(self):
        """Get the private variable where are stored all the results and return it"""
        return self._results
