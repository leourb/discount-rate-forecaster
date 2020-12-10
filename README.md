# Abstract

This is an implementation of the [Gordon Growth Model](https://en.wikipedia.org/wiki/Dividend_discount_model) which
presumes that a fair price of a stock is the expected value of their cash-flows (i.e. of their dividends).

The data comes from:

1. Dividend Data: [DiviData](https://dividata.com/)
2. Timeseries: [Yahoo! Finance](https://finance.yahoo.com/)

# Usage

The script is pretty simple to run. In order to get the calculated fair price of the stock according to the model it 
is sufficient to run it as described in `main.py`:

```python
from fair_price_calculator import FairPriceCalc

print(FairPriceCalc("AAPL").fair_price)
```

## Modules

There are 3 modules used by the model:
1. **data_downloader**: downloads both dividend and market data;
2. **utils**: calculates the inputs of the model;
3. **fair_price_calculator**: calculates the fair price according to the model;

### Classes

#### data_downloader.YahooFinanceDownloader

        """
        Initialize the class with the given input
        :param str ticker: single ticker or list of tickers to use to download the data from Yahoo! Finance
        :param str start_date: start date of the query period in a string format YYYY-MM-DD (or similar)
        :param str end_date: end date of the query period in a string format YYYY-MM-DD (or similar)
        """

The class downloads the data from [Yahoo! Finance](https://finance.yahoo.com/), natively in CSV. However, the class
returns the data in two different formats, CSV and `pandas.DataDrame`. The main usage in this package has been done
using the `pandas` data format.

#### data_downloader.DividendDataDownloader

        """
        Initialize the class with the input parameters
        :param str ticker: ticker to download and to collect the data from
        :param str pickled_name: name of the pickled_file to be processed
        """

The class downloads the data from [Dividata.com](https://dividata.com/). The data scraping process is done using
`bs4` and the table is then formatted in JSON and `pandas.DataFrame`.

#### utils.CalculateInputs

        """
        Initialize the class
        :param str ticker: ticker of the stock to download the data
        """

This calculates collects the inputs to be then passed to the main module `fair_price_calculator.py`

#### fair_price_calculator.FairPriceCalc

        """
        Initialize the class parsing the input
        :param str ticker: ticker of the company for which to estimate the fair price
        """

This is the main class of the model. It calculates the **beta** of the stock and estimates the **ROE** of the company.
These two main inputs, with all the other calculated data in the other classes, is then passed to the main model to
estimate the fair price.

## Financial Considerations

![img.png](img.png)

<div style="text-align: justify">
The Gordon Growth Model (GGM) is one of the models used as fair price estimator. The main concept is that a fair 
price (which is <u>usually</u> **different** from the <u>market price</u>) can be calculated as a perpetuity of the
expected dividend (i.e. the dividend for the next year) remunerated at the Cost of Capital, estimated with the CAPM, 
minus the perpetuity growth of dividends.
  - As mentioned, the ROE (_r_) has been estimated used the CAPM, a well-known model in the financial industry.
    To estimate the model's _beta_, last year's daily data has been used and as index to represent the market variable 
    the **S&P's 500**;
  - The growth parameter (_g_) is estimated as the ratio of the dividend growth of the last year. The data under 
    consideration is US data where dividends are quarterly. So the script calculates the last 4 quarters dividends
    and then compare it against the last 4 quarters dividends to then estimate the dividend growth;
  - The fair price calculated is, most of the time, **surrealistic**. Why? There are many reasons to this. 
    Some explanations may be:
    - Dividend yield is too low;
    - Dividend are paid are not constant;
    - The estimation of parameters (_g_ and _r_) makes the output, sometimes, surrealistic;
</div>