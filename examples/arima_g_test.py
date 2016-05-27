from __future__ import print_function
import timeit
from datetime import datetime
from qsforex.backtest.backtest import Backtest
from qsforex.execution.execution import SimulatedExecution
from qsforex.portfolio.portfolio import Portfolio
from qsforex import settings
from qsforex.strategy.arima_garch_strategy import ArimaGarchStrategy as AGS
from qsforex.data.price import HistoricCSVPriceHandler


if __name__ == "__main__":
    # Trade on GBP/USD and EUR/USD
    #pairs = ["GBPUSD"]
    pairs = ["EURUSD"]
    startdate = datetime(2014, 1, 1) 
    enddate = datetime(2016, 3, 10) 
    portfolio = Portfolio(
        equity=1000, backtest=True
    )
    """Create the strategy parameters for the Test Strategy
    This needs to be expanded to handle multiple strategies/strategy params for multiple currencies."""
    strategy_params = {
        "starttime":startdate,
        "endtime":enddate,
	    "lots":0.1,
        "leverage":10, 
        "currency_factor":1,
        "max_spread":5,
        "max_orders":2
    }
    
    start_time = timeit.default_timer()

    # Create and execute the backtest
    backtest = Backtest(
        portfolio, pairs,
        startdate, enddate,
        HistoricCSVPriceHandler, 
        AGS, strategy_params, 
        SimulatedExecution, 
        equity=settings.EQUITY, heartbeat=0.0, max_iters=10000000
    )
    backtest.simulate_trading()
    print("Processing Time", timeit.default_timer() - start_time)
    
