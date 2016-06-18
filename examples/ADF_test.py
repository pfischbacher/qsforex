# Import the Time Series library
import statsmodels.tsa.stattools as ts

# Import Datetime and the Pandas DataReader
from datetime import datetime
from pandas.io.data import DataReader

# Download the Google OHLCV data from 1/1/2000 to 1/1/2013
goog = DataReader("GOOG", "yahoo", datetime(2000,1,1), datetime(2013,1,1))

# Output the results of the Augmented Dickey-Fuller test for Google
# with a lag order value of 1
test = ts.adfuller(goog['Adj Close'], 1)
print(test)
