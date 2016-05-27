import os
import os.path
import sys

import pandas as pd
import numpy as np
import matplotlib.pylab as plt

from matplotlib.pylab import rcParams

from statsmodels.tsa.arima_model import ARIMA

rcParams['figure.figsize'] = 15, 6
"""
import quandl

quandl.ApiConfig.api_key = 'RpsoJjttGSe1pAxzwH_H'
quandl.ApiConfig.api_version = '2015-04-09'

data = quandl.get('NSE/OIL')"""

#import pandas.io.data as web
from pandas_datareader import data

from pprint import pprint

eurusd = data.DataReader('DEXUSEU', 'fred')

print(eurusd)
data_set_log = np.log(eurusd)
data_set = data_set_log - data_set_log.shift()
data_set.dropna(inplace=True)

windowLength = 500
foreLength = len(data_set) - windowLength
foreLength = 5
#print ('Forelength=', foreLength)
#print ('Data Set=', data_set)
#plt.plot(data_set)
#plt.show()
import warnings
warnings.simplefilter('default')

for d in range(0,foreLength):
    print ('d=', d)
    data_set_offset = data_set[(1+d):(windowLength+d)]
    final_order = np.array([0,0,0])
    final_aic = None
    try:
        for p in range(0,5):
            for q in range(0,5):
                if p is not 0 and q is not 0:

                    try:
                        arima_model = ARIMA(data_set_offset, order=(p, 0, q))
                    except:
                        #e = sys.exc_info()[0]
                        #print ( "<p>Error: %s</p>" % e )
                            
                    if arima_model is not None:
                        try:
                            arima_fit = arima_model.fit(disp=-1)
                            current_aic = arima_fit.aic
                            if final_aic is None or current_aic < final_aic:
                                final_aic = current_aic
                                final_order = np.array([p, 0, q])
                                final_arima = arima(data_set_offset, order=final_order)                 
                        except:
                           #e = sys.exc_info()[0]
                           #print 'No Fit (', e , ')'

    except KeyboardInterrupt:
        print 'User Interrupted'
        break

    print 'Final Order=', final_order
