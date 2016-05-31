from decimal import Decimal
import os


ENVIRONMENTS = { 
    "streaming": {
        "real": "stream-fxtrade.oanda.com",
        "practice": "stream-fxpractice.oanda.com",
        "sandbox": "stream-sandbox.oanda.com"
    },
    "api": {
        "real": "api-fxtrade.oanda.com",
        "practice": "api-fxpractice.oanda.com",
        "sandbox": "api-sandbox.oanda.com"
    }
}

os.environ["QSFOREX_CSV_DATA_DIR"] = "../../data/csv"
os.environ["QSFOREX_HISTORICALDATA_DIR"] = "../../data/historicaldata"
os.environ["QSFOREX_OUTPUT_RESULTS_DIR"] = "../../data/results" 

CSV_DATA_DIR = os.environ.get('QSFOREX_CSV_DATA_DIR', None)
HISTORICALDATA_DIR = os.environ.get('QSFOREX_HISTORICALDATA_DIR', None)
OUTPUT_RESULTS_DIR = os.environ.get('QSFOREX_OUTPUT_RESULTS_DIR', None)

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]
ACCESS_TOKEN = os.environ.get('OANDA_API_ACCESS_TOKEN', None)
ACCOUNT_ID = os.environ.get('OANDA_API_ACCOUNT_ID', None)

BASE_CURRENCY = "USD"
EQUITY = Decimal("10000.00")
