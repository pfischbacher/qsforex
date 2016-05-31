import copy
import os

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_HALF_UP
import pandas as pd
#from collections import defaultdict
from qsforex.settings import CSV_DATA_DIR
from qsforex.settings import HISTORICALDATA_DIR
from qsforex.settings import OUTPUT_RESULTS_DIR

from qsforex.event.event import SignalEvent
from qsforex.event.timeframe import Timeframe
from qsforex.portfolio.position import Position

#Import Desired Indicators


class ArimaGarchStrategy(object):
  
    def __init__(
        self, portfolio, pair, events,
        starttime, endtime,
        lots = 0.1,
        leverage = 10,
        currency_factor = 1,
        max_orders = 2,
        max_spread = 5
    ):
        self.portfolio = portfolio
        self.pair = pair
        self.events = events
        self.period = timedelta(days=1)
        self.timeframe_bars = 500
        self.custom_time = Timeframe(self.pair, self.timeframe_bars, self.period)
        self.starttime = starttime
        self.endtime = endtime
        self.lots =  Decimal(lots)
        self.leverage = leverage
        self.currency_factor = currency_factor
        self.max_spread = Decimal(max_spread)
        self.max_orders = max_orders

        self.ticksize = Decimal("0.00001")
        self.custom_spread = 5
        self.positions = []
        
        self.last_time_check = datetime(2010,1,1)
        self.open_orders = 0
        self.total_orders = 0

    def get_spread(self, tick):
        result = (tick.ask - tick.bid) / self.ticksize 
        if self.custom_spread != None:
            result = self.custom_spread
        return result


    def on_tick(self, event):
        if event.type == 'TICK':
            self.process_tick(event)
        
        self.check_for_trade(event)
        self.check_positions()
        
    def check_for_trade(self, event):
        if self.check_interval():
            self.get_file();
            self.create_order(self.check_direction)
    
    def check_direction(self):
        return 1
    
    def get_file(self):
        self.csv_dir = 'Oanda_EURUSD_D1.csv'
        file_path = os.path.join(CSV_DATA_DIR, self.csv_dir)
        file = pd.io.parsers.read_csv(
                file_path, header=False, index_col=0, 
                parse_dates=True, dayfirst=True,
                names=("Date", "Direction")
        )
        print ('arima_garch_strategy.py', 'FILE DATA=', file);
        return file
        
    def check_positions(self):
        for p in self.positions:
            p.update_position(self.current_tick)

            if (p.state == "closed"):
                self.close_position(p)
            
    def create_order(self, order_type=1):
        self.lots = self.calculate_lots()
        print('arima_garch_strategy.py', 'TRADE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        self.set_order_conditions()
        if order_type == 1:
            ps = Position(self.pair, "long", self.current_tick, self.lots, len(self.positions), self.take_profit, self.stop_loss, self.trailing_stop)
        elif order_type == -1:
            ps = Position(self.pair, "short", self.current_tick, self.lots, len(self.positions), self.take_profit, self.stop_loss, self.trailing_stop)
        self.positions.append(ps)
        self.total_orders +=1
        self.open_orders = len(self.positions)   
        print('arima_garch_strategy.py','Total Orders', self.total_orders, 'Open Orders', self.open_orders)
    
    def add_new_position(self, position):
        current_index = len(self.positions)
        self.positions.append(ps)

    def close_position(self, position):
        ps = self.positions[position.index]
        self.portfolio.update_portfolio(self.pair, ps)
        del[self.positions[position.index]]
        self.open_orders = len(self.positions)
        self.update_positions_index()
    
    def update_positions_index(self):
        if len(self.positions) > 0:
            i = 0
            for p in self.positions:
                p.index = i
                i +=1
        
    def process_tick(self, tick):
        if self.custom_spread != None:
            price = ((tick.ask + tick.bid)/2).quantize(self.ticksize, ROUND_HALF_DOWN)
           
            tick.ask = (price + self.custom_spread * self.ticksize / 2).quantize(self.ticksize, ROUND_HALF_DOWN)
            tick.bid = Decimal(price - self.custom_spread * self.ticksize / 2).quantize(self.ticksize, ROUND_HALF_DOWN)
         
        self.custom_time.addTick(tick)
        self.last_bar = self.custom_time.getLastBar()
        self.current_tick = tick
        self.spread = self.get_spread(tick)

    def set_order_conditions(self):        
        self.take_profit = 0
        self.stop_loss =  0
        self.trailing_stop = 0

    
    def check_interval(self):
        result = False
        last_bar = self.custom_time.getLastBar()
        if last_bar.time - self.last_time_check >= self.period:
            result = True
            self.last_time_check = last_bar.time
        return result

    def check_conditions(self):
        result = False
        if self.check_orders() and self.check_time() and self.check_spread():
            result = True      
        return result
  
    
    def check_orders(self):
        result = False
        if (self.open_orders < self.max_orders):
            result = True
        return result
        
    def check_spread(self):
        result = False
        if (self.spread <= self.max_spread):
            result = True
        return result
     
    def check_time(self):
        result = True
        return result
        
    def get_ATR(self, bars):
        if hasattr(self,"ATR"):
            value = self.ATR.value
        else:
            value = None
            
        result = ATR(bars, self.ATR_period, value, 1)
        return result
    
    def calculate_lots(self):
        return (self.portfolio.balance/10000).quantize(Decimal("0.01"), ROUND_HALF_DOWN)
        #return self.lots

       
    #Not sure how to add/remove lots to a position, need to look into this more.
    """def add_position_lots(self, position, lots):
        result = False
        if position.currency_pair in self.positions:
            if position.index in self.positions[position.currency_pair]
                ps = self.positions[currency_pair][position.index]
                ps.add_lots(lots)
                result = True
        return (result)

    def remove_position_lots(self, position, lots):
        result = False
        if position.currency_pair in self.positions:
            if position.index in self.positions[position.currency_pair]
                ps = self.positions[position.currency_pair][position.index]
                pnl = ps.remove_lots(lots)
                self.balance += pnl
                result = True
        return (result)
    """

