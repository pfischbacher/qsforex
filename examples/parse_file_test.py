import os

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_HALF_UP
import pandas as pd
import numpy as np
#from collections import defaultdict
from qsforex.settings import CSV_DATA_DIR
from qsforex.settings import HISTORICALDATA_DIR
from qsforex.settings import OUTPUT_RESULTS_DIR

def get_file():
    csv_dir = 'forecasts_Oanda_EURUSD_D1_2.csv'
    file_path = os.path.join(CSV_DATA_DIR, csv_dir)
    rows = pd.io.parsers.read_csv(
            file_path, header=False, index_col=0,
            parse_dates=True, dayfirst=True,
            names=( "Direction", "Sigma")
    )
    row = rows.tail(1)
    print(__file__, "FILE=", rows)
    test_date = datetime(2016, 6, 2, 0, 0)
    test_date_str = test_date.strftime("%Y-%m-%d %H:%M:%S")
    test_date_64 = np.datetime64(test_date)
    print (__file__, 'Date=', row.index)
    #print (__file__, 'datetime=', test_date)
    print (__file__, 'datetime string=', test_date_str)
    i = rows.index.searchsorted(test_date)
    value = rows.index[i]
    print(__file__,'i=', i)
    print(__file__, 'ROW FROM DATE=', rows.loc['2016-06-02'])
    #print(__file__, 'ROW FROM DATE=', rows[test_date_str])
    for index, row in rows.iterrows():
        #print('Line=', row)
        #print('Data=', index)
        #print('Direction=', row['Direction'])
        #print 'Volatility=%.5f' % (row['Sigma'])
        #print('Date=', pd.to_datetime(row, format="%Y-%m-%d"))
        #print('Row=', row)
        pass
    #print ('parse_file_test.py', 'FILE DATA33=', rows)

    return rows

the_file = get_file()
