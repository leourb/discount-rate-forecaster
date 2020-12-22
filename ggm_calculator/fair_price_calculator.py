"""Forecast the next expected dividend given actual data"""

import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from ggm_calculator.utils import CalculateInputs


class FairPriceCalc:
    """Calculate the fair price for the selected tickers"""

    def __init__(self, ticker):
        """
        Initialize the class parsing the input
        :param str ticker: ticker of the company for which to estimate the fair price
        """
        self.__inputs = CalculateInputs(ticker)
        if self.__inputs.get_dividend_data().empty:
            self.__fair_price = None
            return self.__fair_price
        self.__dividend_data = self.__inputs.get_dividend_data()
        self.__dividend_growth = self.__inputs.get_dividend_growth()
        self.__rf = self.__inputs.get_risk_free_return()
        self.__market_return = self.__inputs.get_market_return()
        self.__market_data = self.__inputs.get_market_data()
        self.__ticker_data = self.__inputs.get_ticker_data()
        self.__regression_results = self.__perform_regression()
        self.__roe = self.__estimate_roe_with_capm()
        self.__fair_price = self.__calculates_future_price()

    def __perform_regression(self):
        """
        Calculate the Beta to then estimate the value of the ROE using the CAPM
        :return: a dictionary with the statistics of the regression
        :rtype: dict
        """
        results = dict()
        mkt_data = self.__inputs.get_market_data()
        stock_data = self.__inputs.get_ticker_data()
        mkt_data["Log Price"] = np.log(mkt_data["Adj Close"])
        stock_data["Log Price"] = np.log(stock_data["Adj Close"])
        mkt_data["Log Returns"] = mkt_data["Log Price"] - mkt_data["Log Price"].shift(1)
        stock_data["Log Returns"] = stock_data["Log Price"] - stock_data["Log Price"].shift(1)
        mkt_data["Log Returns"].fillna(method='bfill', inplace=True)
        mkt_data["Log Returns"].fillna(method='ffill', inplace=True)
        stock_data["Log Returns"].fillna(method='bfill', inplace=True)
        stock_data["Log Returns"].fillna(method='ffill', inplace=True)
        mkt_x = np.vstack(mkt_data["Log Returns"].values)
        mkt_x_train = mkt_x[:-20]
        mkt_x_test = mkt_x[-20:]
        stock_y_train = stock_data["Log Returns"].values[:-20]
        stock_y_test = stock_data["Log Returns"].values[-20:]
        regr = LinearRegression()
        regr.fit(mkt_x_train, stock_y_train)
        stock_y_pred = regr.predict(mkt_x_test)
        results["beta"] = regr.coef_[0]
        results["r2"] = r2_score(stock_y_test, stock_y_pred)
        results["mse"] = mean_squared_error(stock_y_test, stock_y_pred)
        return results

    def __estimate_roe_with_capm(self):
        """
        Estimates the ROE by using the CAPM model
        :return: an estimate of the ROE calculated using the CAPM
        :rtype: float
        """
        capm = self.__rf + self.__regression_results.get("beta", 0) * (self.__market_return - self.__rf)
        return capm

    def __calculates_future_price(self):
        """
        Calculate the discount rate with the Gordon Growth Model
        :return: the value of the estimated future fair price
        :rtype: float
        """
        if self.__dividend_growth is None:
            return None
        yearly_dividend = float(self.__dividend_data["Dividend Amount"].head(4).sum())
        expected_dividend = yearly_dividend * (1 + self.__dividend_growth)
        fair_price = expected_dividend / (self.__roe - self.__dividend_growth)
        return fair_price

    def get_inputs(self):
        """
        Return the inputs calculated by the CalculateInputs class
        :return: a CalculateInputs class object
        :rtype: CalculateInputs
        """
        return self.__inputs

    def get_dividend_stats(self):
        """
        Return the calculated dividend stats
        :return: a dictionary with the calculated stats
        :rtype: dict
        """
        return self.__inputs.get_dividend_stats()

    def get_estimated_fair_price(self):
        """
        Return the estimated fair price
        :return: a value for the fair price
        :rtype: float
        """
        return self.__fair_price

    def get_estimated_roe(self):
        """
        Return the estimated ROE
        :return: the calculated ROE
        :rtype: float
        """
        return self.__roe
