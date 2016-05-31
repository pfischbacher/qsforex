import os

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_HALF_UP
import pandas as pd
#from collections import defaultdict
from qsforex.settings import CSV_DATA_DIR
from qsforex.settings import HISTORICALDATA_DIR
from qsforex.settings import OUTPUT_RESULTS_DIR

def get_file():
    csv_dir = 'Oanda_EURUSD_D1.csv'
    file_path = os.path.join(CSV_DATA_DIR, csv_dir)
    file = pd.io.parsers.read_csv(
            file_path, header=False, index_col=0, 
            parse_dates=True, dayfirst=True,
            names=("Date", "Direction")
    )
    print ('parse_file_test.py', 'FILE DATA=', file);
    return file

file = get_file()
