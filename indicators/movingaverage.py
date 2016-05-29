from decimal import Decimal, ROUND_HALF_DOWN
from collections import deque
import itertools

class MovingAverage(object):

    def __init__(self, bars, period, shift=0, alpha=0, price_type="close"):
        self.bars = bars
        self.period = period
        self.shift=shift
        self.alpha = alpha
        self.price_type=price_type
        self.value = self.getValue(bars, period, shift, alpha, price_type)
        
    def getValue(self, bars, period, shift, alpha, price_type):
        result = 0
        total=0
        bars_set = deque(itertools.islice(bars, len(bars)-period-shift, len(bars)-shift))

        for bar in bars_set:
            total += getattr(bar,price_type)
        
        result = getattr(bars[-1-shift], price_type) * alpha + total/period * (1-alpha)
        
        return Decimal(result)
        
    def __str__(self):
        return "Value: %s, Period: %s, Shift: %s, Alpha: %s, Price Type: %s" % (
            str(self.value), str(self.period), 
            str(self.shift), str(self.alpha), str(self.price_type)
        )

    def __repr__(self):
        return str(self)
        
class MovingAverageSlope(object):
    def __init__(self, bars, period, shift=0, alpha=0, price_type="close"):
        self.period = period
        self.shift = shift
        self.alpha = alpha
        self.price_type = price_type
        self.MA1 = MovingAverage(bars, period, shift, alpha, price_type)
        self.MA2 = MovingAverage(bars, period, shift+1, alpha, price_type)
        self.value = self.MA2.value - self.MA1.value
    
    def __str__(self):
        return "Value: %s, Period: %s, Shift: %s, Alpha: %s, Price Type: %s" % (
            str(self.value), str(self.period), 
            str(self.shift), str(self.alpha), str(self.price_type)
        )

    def __repr__(self):
        return str(self)
