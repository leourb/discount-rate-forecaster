"""Main module that executes the script"""

from infer_parameters import InferParameters

import pandas as pd

pd.set_option('display.max_rows', None)

if __name__ == "__main__":
    InferParameters("AAPL").infer_required_return_from_mkt_price()
