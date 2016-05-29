import copy
from datetime import datetime, timedelta
from decimal import Decimal

from qsforex.event.event import SignalEvent
from qsforex.event.timeframe import Timeframe
from qsforex.portfolio.position import Position

#Import Desired Indicators
from qsforex.indicators.averagetruerange import AverageTrueRange as ATR
from qsforex.indicators.movingaverage import MovingAverage as MA
from qsforex.indicators.movingaverage import MovingAverageSlope as MAS


class TestingStrategy(object):
  
    def __init__(
        self, pair, events, 
        lots = 0.1,
        leverage = 10,
        currency_factor = 1,
        max_orders = 2,
        max_spread = 0.5,
        ATR_period = 90,
        MA1_period = 5,
        MA2_period = 8,
        MA3_period = 13,
        slope_denominator = 5.5,
        TP_mod = 3.9,
        SL_mod = 3.9,
        TS_mod = 0.3
    ):
        self.pairs = pairs
        self.pair = pairs[0]
        self.pairs_dict = self.create_pairs_dict()
        self.events = events
        self.period = timedelta(minutes=15)
        self.timeframe_bars = 100
        self.custom_time = Timeframe(self.timeframe_bars, self.period)
        self.lots =  Decimal(lots)
        self.leverage = leverage
        self.currency_factor = currency_factor
        self.max_spread = Decimal(max_spread)
        self.max_orders = max_orders
        self.slope_denominator = Decimal(slope_denominator)
        self.ATR_period = ATR_period
        self.MA1_period = MA1_period
        self.MA2_period = MA2_period
        self.MA3_period = MA3_period
        self.TP_mod = Decimal(TP_mod)
        self.SL_mod = Decimal(SL_mod)
        self.TS_mod = Decimal(TS_mod)
        self.ticksize = Decimal(0.0001)
        self.custom_spread = Decimal(0.5)
        self.positions = self.positions_set_up()
        
        self.last_time_check = datetime(2010,1,1)
        self.open_orders = 0
        self.total_orders = 0

    def create_pairs_dict(self):
        attr_dict = {
            "ticks": 0,
            "invested": False,
            "timeframe": None
        }
        pairs_dict = {}
        for p in self.pairs:
            pairs_dict[p] = copy.deepcopy(attr_dict)
            self.pairs[p].custom_time = Timeframe(self.timeframe_bars, self.period, p)
        return pairs_dict
        
    def positions_set_up(self):
        return defaultdict(self.pairs)

    def get_spread(self, tick):
        result = (tick.ask - tick.bid) / self.ticksize 
        if self.custom_spread != None:
            result = self.custom_spread
        return result

    def get_ATR(self, period, shift=0):
		return(0)

    def calculate_signals(self, event):
        if event.type == 'TICK':
            self.process_tick(event)
        
        self.check_trade(event)
        self.check_positions()
        
    def check_trade(self, event):
        #print('Check Trade', 'Custom Bars Index', self.custom_time.bars.index, 'ATR Period', self.ATR_period);
        if self.check_interval():
            if self.custom_time.getSize() >= self.ATR_period:
                self.ATR = self.getATR(self.custom_time.bars.bars)
                if self.check_conditions():
                    #print('step 2')
                    self.set_slopes()
                    if self.check_slopes() == 1:
                        self.create_order(1)
                    elif self.check_slopes() == -1:
                        self.create_order(-1)
            else:
                #print('Nope')
                pass
                
    def check_positions(self):
        for position in self.positions:
            print(position)
            
    def create_order(self, order_type=1):
        print('TRADE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        if order_type == 1:
            signal = SignalEvent(self.pair, "market", "buy", self.current_tick.time)
            self.events.put(signal)
            print('buy')
            pass
        elif order_type == -1:
            signal = SignalEvent(self.pair, "market", "sell", self.current_tick.time)
            self.events.put(signal)
            print('sell')
            pass
        #self.open_orders +=1   
        self.total_orders +=1
        print('Total Orders', self.total_orders)
    
    def add_new_position(self, position):
        current_index = len(self.positions[position.currency_pair])
        self.positions[position.currency_pair].append(ps)

    def close_position(self, position):
        result = False
        if position.currency_pair in self.positions:
            if position.index in self.positions[position.currency_pair]:
                ps = self.positions[position.currency_pair][position.index]
                pnl = ps.close_position()
                self.balance += pnl
                del[self.positions[position.currency_pair][position.index]]
                result = True
        return result
    
    def process_tick(self, tick):
        if self.custom_spread != None:
            price = (tick.ask + tick.bid)/2
            tick.ask = price + self.custom_spread/(self.ticksize * 2)
            tick.bid = price - self.custom_spread/(self.ticksize * 2)
        self.custom_time.addTick(tick)
        self.last_bar = self.custom_time.getLastBar()
        self.current_tick = tick
        self.spread = self.get_spread(tick)

    def set_order_conditions(self):
        self.take_profit = self.TP_mod * (self.ATR.value + self.min_slope) / self.ticksize + self.spread;
        self.stop_loss =  self.SL_mod * abs(self.ATR.value - self.min_slope) / self.ticksize + self.spread;
        self.trailing_stop = self.TS_mod * abs(self.ATR.value - abs(self.min_slope)) / self.ticksize;

    def set_slopes(self):
        self.MASlope1 = self.getMASlope(self.custom_time.bars.bars, self.MA1_period)
        self.MASlope2 = self.getMASlope(self.custom_time.bars.bars, self.MA2_period)
        self.MASlope3 = self.getMASlope(self.custom_time.bars.bars, self.MA3_period)
    
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
     
    def check_volatility(self):
        result = False
        self.min_slope = self.ATR.value / self.slope_denominator
        if abs(self.MASlope1.value) >= self.min_slope and abs(self.MASlope2.value) >= self.min_slope and abs(self.MASlope3.value) >= self.min_slope:
            result = True
        return result
        
    def check_slopes(self):
        self.min_slope = self.ATR.value / self.slope_denominator

        result = 0
        if self.MASlope1.value >= self.min_slope and self.MASlope2.value >= self.min_slope and self.MASlope3.value >= self.min_slope:
            result = 1
        elif self.MASlope1.value <= -self.min_slope and self.MASlope2.value <= -self.min_slope and self.MASlope3.value <= -self.min_slope:
            result = -1
        #print('Min Slope', self.min_slope, 'MA1Slope', self.MASlope1.value, 'MA2Slope', self.MASlope2.value,'MA3Slope', self.MASlope3.value)        
        return result
    
    def check_orders(self):
        result = False
        if (self.open_orders < self.max_orders):
            result = True
        #print('orders result', result)
        return result
        
    def check_spread(self):
        result = False
        if (self.spread <= self.max_spread):
            result = True
        #print('spread result', result)
        return result
     
    def check_time(self):
        result = True
        return result
        
    def getATR(self, bars):
        if hasattr(self,"ATR"):
            value = self.ATR.value
        else:
            value = 0
            
        result = ATR(bars, self.ATR_period, value)
        return result

    def getMA(self, bars, period):    
        return Moving_Average(bars, period)
        
    def getMASlope(self, bars, period):
        return MAS(bars, period)
        
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

