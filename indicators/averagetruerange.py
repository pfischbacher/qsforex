from decimal import Decimal, ROUND_HALF_UP
import collections, itertools

class AverageTrueRange(object):

    def __init__(
        self, bars, period, prev_ATR=None, shift=0
    ):
        self.period = period
        self.shift = shift
        self.bars = bars
        self.value = self.getValue(bars, period, prev_ATR, shift)

        
    def getValue(self, bars, period, prev_ATR, shift):
        previous_close = None
        cnt = 0
        total = 0
        a = len(bars)-period-shift
        b = len(bars)-shift
        if prev_ATR == None:
            for bar in collections.deque(itertools.islice(bars, a, b)):
                cnt +=1
                if a > 0 and previous_close == None:
                    previous_close = bar.close
                if previous_close != None:
                    true_range = max(bar.high - bar.low, abs(bar.high - previous_close), abs(bar.low - previous_close))
                else:
                    true_range = bar.high - bar.low
                    
                previous_close = bar.close
                total += true_range
                
            result = total/period
        else:
            bar = bars[-1-shift]
            previous_close = bars[-2-shift].close
            true_range = max(bar.high - bar.low, abs(bar.high - previous_close), abs(bar.low - previous_close))
            result = (prev_ATR * (period-1) + true_range)/period
            
        return Decimal(result).quantize(Decimal("0.000001"), ROUND_HALF_UP)
        
    def __str__(self):
        return "Value: %s, Period: %s, Previous ATR: %s, Shift: %s" % (
            str(self.value), str(self.period), 
            str(self.prev_ATR), str(self.shift)
        )

    def __repr__(self):
        return str(self)
