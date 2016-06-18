from __future__ import print_function

from copy import deepcopy
from decimal import Decimal, getcontext, ROUND_HALF_DOWN
import logging
import os

import pandas as pd

from qsforex.event.event import OrderEvent
from qsforex.performance.performance import create_drawdowns
from qsforex.portfolio.position import Position
from qsforex.settings import OUTPUT_RESULTS_DIR


class Portfolio(object):
    def __init__(
        self, home_currency="USD", 
        leverage=20, equity=100000.00, 
        risk_per_trade=Decimal("0.02"), backtest=True
    ):
        self.home_currency = home_currency  # Account denomination (e.g. GBP)
        self.leverage = leverage
        self.equity = Decimal(equity)
        self.balance = deepcopy(self.equity)
        self.risk_per_trade = risk_per_trade
        self.backtest = backtest
        self.order_num = 0
        self.pairs = []
        self.trade_lots = self.calc_risk_position_size()
        #self.positions = defaultdict(list)
        if self.backtest:
            self.backtest_file = self.create_equity_file()
        self.logger = logging.getLogger(__name__)

    def add_pair(self, pair):
        self.pairs.append(pair)
        
    def calc_risk_position_size(self):
        return self.equity * self.risk_per_trade

    def create_equity_file(self):
        filename = "backtest.csv"
        out_file = open(os.path.join(OUTPUT_RESULTS_DIR, filename), "w")
        header = "Order,Pair,Open Time,Close Time,PNL,lots,Balance,Position Type,Close Type,Take Profit,Stop Loss,Trailing Stop"
        for pair in self.pairs:
            header += ",%s" % pair
        header += "\n"
        out_file.write(header)
        if self.backtest:
            print(header[:-2])
        return out_file

    def output_results(self):
        # Closes off the Backtest.csv file so it can be 
        # read via Pandas without problems
        self.backtest_file.close()
        
        in_filename = "backtest.csv"
        out_filename = "equity.csv" 
        in_file = os.path.join(OUTPUT_RESULTS_DIR, in_filename)
        out_file = os.path.join(OUTPUT_RESULTS_DIR, out_filename)

        # Create equity curve dataframe
        df = pd.read_csv(in_file, index_col=0)
        df.dropna(inplace=True)
        df["Total"] = df.sum(axis=1)
        df["Returns"] = df["Total"].pct_change()
        df["Equity"] = (1.0+df["Returns"]).cumprod()
        
        # Create drawdown statistics
        drawdown, max_dd, dd_duration = create_drawdowns(df["Equity"])
        df["Drawdown"] = drawdown
        df.to_csv(out_file, index=True)
        
        print("Simulation complete and results exported to %s" % out_filename)

    def update_portfolio(self, pair, position, extra=""):
        self.balance += position.pnl
        self.order_num += 1
        if self.backtest:
            out_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (self.order_num, pair, position.open_time, position.close_time, position.pnl, position.lots, self.balance, position.position_type, position.close_type, position.take_profit, position.stop_loss, position.trailing_stop, extra)
            out_line += "\n"
            print(out_line[:-2])
            self.backtest_file.write(out_line)
        """
        This updates all positions ensuring an up to date
        unrealised profit and loss (PnL).
        """
        
        """currency_pair = tick_event.instrument
        if currency_pair in self.positions:
            ps = self.positions[currency_pair]
            ps.update_position_price()
        if self.backtest:
            out_line = "%s,%s" % (tick_event.time, self.balance)
            for pair in self.ticker.pairs:
                if pair in self.positions:
                    out_line += ",%s" % self.positions[pair].profit_base
                else:
                    out_line += ",0.00"
            out_line += "\n"
            print(out_line[:-2])
            self.backtest_file.write(out_line)"""
        pass

    #Going to move this out of the portfolio class, strategy class or new order class?
    """def execute_signal(self, signal_event):
        # Check that the prices ticker contains all necessary
        # currency pairs prior to executing an order
        execute = True
        tp = self.ticker.prices
        for pair in tp:
            if tp[pair]["ask"] is None or tp[pair]["bid"] is None:
                execute = False

        # All necessary pricing data is available,
        # we can execute
        if execute:
            side = signal_event.side
            currency_pair = signal_event.instrument
            lots = int(self.trade_lots)
            time = signal_event.time
            
            # If there is no position, create one
            if currency_pair not in self.positions:
                if side == "buy":
                    position_type = "long"
                else:
                    position_type = "short"
                    
                ps = Position(
                    position_type, currency_pair, lots, tick, current_index+1
                )
                self.add_new_position(
                    ps
                )

            # If a position exists add or remove lots
            else:
                ps = self.positions[currency_pair]

                if side == "buy" and ps.position_type == "long":
                    self.add_position_lots(currency_pair, lots)

                elif side == "sell" and ps.position_type == "long":
                    if lots == ps.lots:
                        self.close_position(currency_pair)
                    # TODO: Allow lots to be added/removed
                    elif lots < ps.lots:
                        return
                    elif lots > ps.lots:
                        return

                elif side == "buy" and ps.position_type == "short":
                    if lots == ps.lots:
                        self.close_position(currency_pair)
                    # TODO: Allow lots to be added/removed
                    elif lots < ps.lots:
                        return
                    elif lots > ps.lots:
                        return
                        
                elif side == "sell" and ps.position_type == "short":
                    self.add_position_lots(currency_pair, lots)

            order = OrderEvent(currency_pair, lots, "market", side)
            self.events.put(order)

            self.logger.info("Portfolio Balance: %s" % self.balance)
        else:
            self.logger.info("Unable to execute order as price data was insufficient.")
        
        """
