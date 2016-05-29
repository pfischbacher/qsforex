import copy

from qsforex.event.event import SignalEvent

class CustomSlopes(object):
    """
    A custom strategy developed to estimate the trend direction and volatility of the movement. 
    """

    """
	extern double Lots      =0.1;
	extern int Leverage      =10;
	extern double Currency_Factor      =1;
	extern double Max_Spread = 1;
	extern int ATR_Slope_Period = 90;
	extern int Max_Orders = 2;
	extern double modifier_TP = 4.0;
	extern double modifier_SL = 4.0;
	extern double modifier_TS = 0.3;
	extern double slope_denominator = 5.5;
    """
    def __init__(
        self, pairs, events, 
        lots=0.1, leverage=10, currency_factor = 1, max_spread=0.5, slope_denominator=5.5, ATR_period = 90, max_orders=2, TP_mod=3.9, SL_mod=3.9,TS_mod = 0.3
    ):
        self.pairs = pairs
        self.pairs_dict = self.create_pairs_dict()
        self.events = events      
        self.lots = lots
		self.leverage = leverage
		self.currency_factor = currency_factor
		self.max_spread = max_spread
		self.slope_denominator = slope_denominator
		self.ATR_period = ATR_period
		self.max_orders = max_orders
		self.TP_mod = TP_mod
		self.SL_mod = SL_mod
		self.TS_mod = TS_mod

    def create_pairs_dict(self):
        attr_dict = {
            "ticks": 0,
            "invested": False,
            "short_sma": None,
            "long_sma": None
        }
        pairs_dict = {}
        for p in self.pairs:
            pairs_dict[p] = copy.deepcopy(attr_dict)
        return pairs_dict

	def get_spread(self, ask, bid):
		return (ask-bid)

	def get_ATR(period, shift=0):
		return(0)

    def calc_rolling_sma(self, sma_m_1, window, price):
        return ((sma_m_1 * (window - 1)) + price) / window

    def calculate_signals(self, event):
        if event.type == 'TICK':
            pair = event.instrument
            price = event.bid
            pd = self.pairs_dict[pair]
            if pd["ticks"] == 0:
                pd["short_sma"] = price
                pd["long_sma"] = price
            else:
                pd["short_sma"] = self.calc_rolling_sma(
                    pd["short_sma"], self.short_window, price
                )
                pd["long_sma"] = self.calc_rolling_sma(
                    pd["long_sma"], self.long_window, price
                )
            # Only start the strategy when we have created an accurate short window
            if pd["ticks"] > self.short_window:
                if pd["short_sma"] > pd["long_sma"] and not pd["invested"]:
                    signal = SignalEvent(pair, "market", "buy", event.time)
                    self.events.put(signal)
                    pd["invested"] = True
                if pd["short_sma"] < pd["long_sma"] and pd["invested"]:
                    signal = SignalEvent(pair, "market", "sell", event.time)
                    self.events.put(signal)
                    pd["invested"] = False
            pd["ticks"] += 1

class ATR(object):

	def __init__(
        self, period, shift=0, events
    ):
	self.period = period
	self.shift = shift
	self.events = events
	self.ATR_array = {}

	def get_ATR(self, n):
		for (event in self.events):
			 	
		if(n!=0):

		
		prev_ATR = 0;
		true_range = 0;
		result = prev_ATR * (period-1) + true_range / period
		return(0);	
