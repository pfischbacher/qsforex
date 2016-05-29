from decimal import Decimal, getcontext, ROUND_HALF_DOWN, ROUND_HALF_UP
from qsforex import settings

class Position(object):
    def __init__(
        self, pair, position_type, open_tick, lots, position_index,
        take_profit = 0, stop_loss = 0, trailing_stop = 0
    ):
        #self.home_currency = home_currency  # Account denomination (e.g. GBP)
        self.position_type = position_type  # Long or short
        self.pair = pair  # Intended traded currency pair
        self.open_time = open_tick.time
        self.open_price = self.get_price(open_tick)
        self.lots = lots
        self.index = position_index
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.trailing_stop = trailing_stop
        self.set_up_currencies()
        self.state = "open"
        self.start_trailing_stop = False
        self.ticksize = Decimal("0.00001")
        self.init_conditions()
        #self.profit_base = self.calculate_profit_base()
        #self.profit_perc = self.calculate_profit_perc()
        
        
    def get_price(self, tick):
        result = 0
        if self.position_type == "long":
            result = tick.ask
        elif self.position_type == "short":
            result = tick.bid
        return result
        
    def set_up_currencies(self):
        self.base_currency = self.pair[:3]    # For EUR/USD, this is EUR
        self.quote_currency = self.pair[3:]   # For EUR/USD, this is USD

    def number_units(self):
        return int(settings.LOTSIZE * self.lots)

    def calculate_pips(self):
        mult = Decimal("1")
        if self.position_type == "long":
            mult = Decimal("1")
        elif self.position_type == "short":
            mult = Decimal("-1")
        pips = (mult * (self.cur_price - self.avg_price)).quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )
        
        return pips

    def calculate_profit_base(self):
        pips = self.calculate_pips()
        qh_close = 1
        #ticker_qh = self.ticker.prices[self.quote_home_pair]
        ticker_qh = self.ticker.prices.get(self.quote_home_pair, None)
        if ticker_qh != None:
            if self.position_type == "long":
                qh_close = ticker_qh["bid"]
            else:
                qh_close = ticker_qh["ask"]
        profit = pips * qh_close * self.lots
        return profit.quantize(self.ticksize), ROUND_HALF_DOWN

    def calculate_profit_perc(self):
        return (
            self.profit_base / self.lots * Decimal("100.00")).quantize(self.ticksize, ROUND_HALF_DOWN
        )
    
    def init_conditions(self):
        self.set_stop_loss()
        self.set_take_profit()
        
    def set_stop_loss(self):
        if self.stop_loss > 0:
            if self.position_type == "long":
                self.stop_loss_limit = self.open_price - self.stop_loss * self.ticksize
            elif self.position_type == "short":
                self.stop_loss_limit = self.open_price + self.stop_loss * self.ticksize
        
    def set_take_profit(self):
        if self.take_profit > 0:
            if self.position_type == "long":
                self.take_profit_limit = self.open_price + self.take_profit * self.ticksize
            elif self.position_type == "short":
                    self.take_profit_limit = self.open_price - self.take_profit * self.ticksize
    
    def take_profit_trigger(self, tick):
        if self.take_profit_limit is not None:
            if self.position_type == "long":
                if tick.bid >= self.take_profit_limit:
                    self.close_position(tick.bid, tick.time, "Take Profit")
            elif self.position_type == "short":
                if tick.ask <= self.take_profit_limit:
                    self.close_position(tick.ask, tick.time, "Take Profit")
        
    def stop_loss_trigger(self, tick):
        if self.start_trailing_stop:
            label = "Trailing Stop"
        else:
            label = "Stop Loss"
        if self.stop_loss_limit is not None:
            if self.position_type == "long":
                if tick.bid <= self.stop_loss_limit:
                    self.close_position(tick.bid, tick.time, label)
            elif self.position_type == "short":
                if tick.ask >= self.stop_loss_limit:
                    self.close_position(tick.ask, tick.time, label)

    def set_trailing_stop(self, tick):
        if self.start_trailing_stop:
            if self.position_type == "long":
                if tick.bid - self.trailing_stop * self.ticksize > self.stop_loss_limit:
                    self.stop_loss_limit = Decimal(tick.bid - self.trailing_stop * self.ticksize).quantize(self.ticksize, ROUND_HALF_DOWN)
                   
            elif self.position_type == "short":
                if tick.ask + self.trailing_stop * self.ticksize < self.stop_loss_limit:
                    self.stop_loss_limit = Decimal(tick.ask  + self.trailing_stop * self.ticksize).quantize(self.ticksize, ROUND_HALF_UP)
                    
        elif self.trailing_stop > 0:
            if self.position_type == "long":
                if tick.bid - self.open_price > self.trailing_stop * self.ticksize:
                    self.start_trailing_stop = True
                    self.stop_loss_limit = Decimal(tick.bid - self.trailing_stop * self.ticksize).quantize(self.ticksize, ROUND_HALF_UP)
                
            elif self.position_type == "short":
                if self.open_price - tick.ask > self.trailing_stop * self.ticksize:
                    self.start_trailing_stop = True
                    self.stop_loss_limit = (tick.ask + self.trailing_stop * self.ticksize).quantize(self.ticksize)
                
            #print('position.py', 'Trailing Stop', self.trailing_stop, 'Stop Loss', self.stop_loss)
        
    def update_position(self, tick):
        self.update_conditions(tick)
        self.set_trailing_stop(tick)
        self.take_profit_trigger(tick)
        self.stop_loss_trigger(tick)

    def update_conditions(self, tick):
        if self.position_type == "long":
            price = tick.bid
            self.unrealize_pnl = Decimal((tick.bid - self.open_price) * self.number_units()).quantize(Decimal("0.0001"), ROUND_HALF_DOWN)
        elif self.position_type == "short":
            price = tick.ask
            self.unrealize_pnl = Decimal((self.open_price - tick.ask) * self.number_units()).quantize(Decimal("0.0001"), ROUND_HALF_DOWN)
     
    
    def update_position_price(self, tick):
        """ticker_cur = self.ticker.prices[self.pair]
        if self.position_type == "long":
            self.cur_price = Decimal(str(ticker_cur["bid"]))
        else:
            self.cur_price = Decimal(str(ticker_cur["ask"]))
        self.profit_base = self.calculate_profit_base()
        self.profit_perc = self.calculate_profit_perc()"""
        pass
    
    def close_position(self, price, time, close_type):
        self.close_price = price
        self.close_time = time
        self.close_type = close_type
        self.pnl = self.unrealize_pnl
        #print("Position.py", "pnl", self.pnl, "Close Type", close_type)   
        self.state = "closed"
        self.unrealize_pnl = 0
            
        """self.update_position_price()
        # Calculate PnL
        pnl = self.calculate_pips() * qh_close * self.lots
        getcontext().rounding = ROUND_HALF_DOWN
        return pnl.quantize(Decimal("0.01"))"""
    
    #Not sure how to add/remove lots to a position, need to look into this more.    
    """
    def add_lots(self, lots):
        cp = self.ticker.prices[self.pair]
        if self.position_type == "long":
            add_price = cp["ask"]
        else:
            add_price = cp["bid"]
        new_total_lots = self.lots + lots
        new_total_cost = self.avg_price*self.lots + add_price*lots
        self.avg_price = new_total_cost/new_total_lots
        self.lots = new_total_lots
        self.update_position_price()

    def remove_lots(self, lots):
        dec_lots = Decimal(str(lots))
        qh_close = 1
        ticker_cp = self.ticker.prices[self.pair]
        ticker_qh = self.ticker.prices.get(self.quote_home_pair, None)
        if self.position_type == "long":
            remove_price = ticker_cp["bid"]
            if ticker_qh != None:
                qh_close = ticker_qh["ask"]
        else:
            remove_price = ticker_cp["ask"]
            if ticker_qh != None:
                qh_close = ticker_qh["bid"]
    
        self.lots -= dec_lots
        self.update_position_price()
        # Calculate PnL
        pnl = self.calculate_pips() * qh_close * dec_lots
        getcontext().rounding = ROUND_HALF_DOWN
        return pnl.quantize(Decimal("0.01"))
    """
