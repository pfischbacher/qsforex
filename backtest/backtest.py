from __future__ import print_function

try:
    import Queue as queue
except ImportError:
    import queue
import time

from qsforex import settings


class Backtest(object):
    """
    Enscapsulates the settings and components for carrying out
    an event-driven backtest on the foreign exchange markets.
    """
	#max_iters=10000000000
    def __init__(
        self, portfolio, pairs, startdate, enddate, data_handler,
        strategy, 
        strategy_params, execution, 
        equity=1000.0, heartbeat=0.0, 
        max_iters=10000000000
    ):
        """
        Initialises the backtest.
        """
        self.portfolio = portfolio
        self.pairs = pairs
        self.events = queue.Queue()
        self.csv_dir = settings.HISTORICALDATA_DIR
        self.ticker = data_handler(self.pairs, self.events, self.csv_dir, startdate, enddate)
        self.startdate = startdate
        self.enddate = enddate
        self.strategy_params = strategy_params
        self.equity = equity
        self.heartbeat = heartbeat
        self.max_iters = max_iters
        """self.portfolio = portfolio(
            self.ticker, self.events, equity=self.equity, backtest=True
        )"""
        
        for pair in self.pairs:
            self.portfolio.add_pair(pair)
            self.strategy = strategy(
                self.portfolio, pair, self.events, **self.strategy_params
            )
        self.execution = execution()

    def _run_backtest(self):
        """
        Carries out an infinite while loop that polls the 
        events queue and directs each event to either the
        strategy component of the execution handler. The
        loop will then pause for "heartbeat" seconds and
        continue unti the maximum number of iterations is
        exceeded.
        """
        print("Running Backtest...")
        iters = 0
        #while iters < self.max_iters and self.ticker.continue_backtest:
        for i in xrange(self.max_iters):
            try:
                event = self.events.get(False)
            except queue.Empty:
                self.ticker.stream_next_tick()
                if not self.ticker.continue_backtest:
                    break
            except KeyboardInterrupt:
                break
            else:
                if event is not None:
                    if event.type == 'TICK':
                        #self.strategy.calculate_signals(event)
                        if self.startdate < event.time and event.time <= self.enddate:
                            #pass
                            self.strategy.on_tick(event)
                            #self.portfolio.update_portfolio(event)
                    """Want to remove and let the strategy class do the signal and orderhandling.
                    elif event.type == 'BAR':
                        self.strategy.calculate_signals(event)
                        self.portfolio.update_portfolio(event)
                    elif event.type == 'SIGNAL':
                        print('Execute Signal')
                        #self.portfolio.execute_signal(event)
                    elif event.type == 'ORDER':
                        self.execution.execute_order(event)
                    """    
            time.sleep(self.heartbeat)
            iters += 1

    def _output_performance(self):
        """
        Outputs the strategy performance from the backtest.
        """
        print("Calculating Performance Metrics...")
        self.portfolio.output_results()

    def simulate_trading(self):
        """
        Simulates the backtest and outputs portfolio performance.
        """
        self._run_backtest()
        #self._output_performance()
        print("Backtest complete.")
