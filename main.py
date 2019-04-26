"""Main module that executes the script"""

import sys

from data_downloader import DataDownloader
from fair_price_calculator import FairPriceCalc
from utils import Utils

from pprint import pprint

if __name__ == "__main__":
    # We want the script to run only if called directly
    # https://docs.python.org/3/library/__main__.html
    print(f'Executing script {sys.argv[0]} now')
    if len(sys.argv) <= 1:
        print('No ticker provided. Please call the script like: "python main.py AMZN FB AAPL" or '
              '"python --offline filename"')
        sys.exit(1)
    if "--offline" in sys.argv[1]:
        try:
            json_list_of_dividends = Utils.from_pickle(sys.argv[2])
        except IndexError:
            print('Must provide a valid pickle filename in order to start the offline mode.')
            sys.exit(1)
        except FileNotFoundError:
            print('A valid argument needs to be passed. Please try again.')
            sys.exit(1)
    else:
        json_list_of_dividends = DataDownloader(sys.argv[1:], 'download_data.pickle').get_results()
    pprint(FairPriceCalc(json_list_of_dividends).results)  # The HIGHEST IRR will be the best growth stock

