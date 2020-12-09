"""Forecast the next expected dividend given actual data"""

import numpy as np

from utils import YahooFinanceDownloader


class FairPriceCalc:
    """Calculate the fair price for the selected tickers"""

    def __init__(self, json_tickers_data):
        """
        Initialize the class parsing the input

        :param dict json_tickers_data: JSON object with the data results
        """
        self._dividend_data = json_tickers_data
        self._market_return =
        self._rf = input("Enter the Risk-Free rate: ")
        self.dividend_stats = self._calculate_dividend_stats()
        self._market_data = Utils.import_csv_data('data.csv')
        self.results = self._calculate_implied_discount_rate()

    def _calculate_dividend_stats(self):
        """Calculate the dividend stats of the JSON data"""

        stats = dict()
        for ticker in self._dividend_data:
            dividend_list = list()
            if self._dividend_data[ticker] is not None:
                for record in self._dividend_data[ticker]:
                    dividend_list.append(float(record.get('Cash Amount')))
            if dividend_list:
                stats[ticker] = dict()
                stats[ticker]['mean'] = np.mean(dividend_list)
                stats[ticker]['median'] = np.median(dividend_list)
                stats[ticker]['variance'] = np.var(dividend_list)
        return stats

    def _calculate_implied_discount_rate(self):
        """Calculate the discount rate with the Gordon Growth Model"""
        # https://www.investopedia.com/terms/g/gordongrowthmodel.asp
        implied_discount_rates = dict()
        tickers_to_analyze = list(self._dividend_data.keys())
        for ticker in tickers_to_analyze:
            model_inputs = self._extract_model_inputs(ticker)
            expected_dividend = model_inputs['d'] * (1 + model_inputs['g'])
            print(model_inputs)
            if model_inputs.get('price') == 0:
                impl_disc_rate = None
            else:
                impl_disc_rate = (expected_dividend + model_inputs.get('g', 0) * model_inputs.get('price', 0)
                                  ) / model_inputs.get('price', 0)
            implied_discount_rates[ticker] = impl_disc_rate
        return implied_discount_rates

    def _extract_model_inputs(self, ticker):
        """
        Make some data manipulation to extract clean model inputs

        :param str ticker: ticker being analyzed
        :return: a dictionary with all the clean inputs
        """
        gordon_growth_model_inputs = dict()
        try:
            gordon_growth_model_inputs['g'] = float(self._market_data.get(ticker, {}).get('g', 0)) / 100
            gordon_growth_model_inputs['price'] = float(self._market_data.get(ticker, {}).get('price', 0))
            gordon_growth_model_inputs['beta'] = float(self._market_data.get(ticker, {}).get('beta', 0))
        except ValueError:
            print(f'Invalid inputs for ticker {ticker}. Impossible to estimate fair price.')
            gordon_growth_model_inputs['g'] = 0  # Zero-out the GGM
            gordon_growth_model_inputs['price'] = 0
        if self._dividend_data.get(ticker) is not None:
            gordon_growth_model_inputs['d'] = float(self._dividend_data.get(ticker, {})[0].get('Cash Amount', {})) * 4
        else:
            gordon_growth_model_inputs['d'] = 0
        return gordon_growth_model_inputs
