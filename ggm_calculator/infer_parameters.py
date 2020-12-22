"""This module infers the parameters of the GGM from the merket price"""

from ggm_calculator.fair_price_calculator import FairPriceCalc


class InferParameters:
    """Infer the parameters g and r from the Market Prices"""

    def __init__(self, ticker):
        """
        Initialize the class with the given ticker
        :param str ticker: ticker of the stock to analyze
        """
        self.__ticker = ticker
        self.__inputs = FairPriceCalc(self.__ticker)
        if self.__inputs.get_estimated_fair_price() is None:
            self.__infer_g = None
            self.__infer_r = None
            return
        self.__last_price = self.__inputs.get_inputs().get_ticker_data().tail(1)["Adj Close"].values[0]
        self.__dividend_growth = self.__inputs.get_inputs().get_dividend_growth()
        self.__dividend_data = self.__inputs.get_inputs().get_dividend_data()
        self.__required_return = self.__inputs.get_estimated_roe()
        self.__infer_g = self.__infer_growth_from_mkt_price()
        self.__infer_r = self.__infer_required_return_from_mkt_price()

    def __infer_growth_from_mkt_price(self):
        """
        Infer the growth g according to the Gordon Growth Model
        :return: the value of g
        :rtype: float
        """
        yearly_dividend = float(self.__dividend_data["Dividend Amount"].head(4).sum())
        expected_dividend = yearly_dividend * (1 + self.__dividend_growth)
        growth = self.__required_return - (expected_dividend / self.__last_price)
        return growth

    def __infer_required_return_from_mkt_price(self):
        """
        Infer the required return r according to the Gordon Growth Model
        :return: the value of r
        :rtype: float
        """
        yearly_dividend = float(self.__dividend_data["Dividend Amount"].head(4).sum())
        expected_dividend = yearly_dividend * (1 + self.__dividend_growth)
        required_return = (expected_dividend/self.__last_price) + self.__dividend_growth
        return required_return

    def get_inferred_g(self):
        """
        Get the inferred g
        :return: the value of g
        :rtype: float
        """
        return self.__infer_g

    def get_inferred_r(self):
        """
        Get the inferred r
        :return: the value of r
        :rtype: float
        """
        return self.__infer_r
