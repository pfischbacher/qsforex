import time
from datetime import date, timedelta, datetime
import numpy
from qsforex.event.bars import Bars
#http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python
class Timeframe(object):

    def __init__(
        self, instrument, number_bars, period=timedelta(seconds=1), ticks=None
    ):
        self.period = period
        self.bars = Bars(number_bars)
        self.instrument = instrument
        if ticks is not None:
            pass
        else:
            pass
        
    def addTick(self, tick):
        time = datetime(tick.time.year, tick.time.month, tick.time.day, tick.time.hour, tick.time.minute, tick.time.second, tick.time.microsecond)
        bar_time = self.round_time(time, self.period, 'down')

        if hasattr(self, 'prev_tick'):
            interval = tick.time - self.bars.current_bar.time
            if interval >= self.period:
                self.bars.newBar(bar_time, tick)
            else:
                self.bars.addToOpenBar(bar_time, tick)
        else:
            self.bars.newBar(bar_time, tick)
        self.prev_tick = tick
        
                
    def round_time(self, dt=None, date_delta=timedelta(seconds=1), to='average'):
        """
        Round a datetime object to a multiple of a timedelta
        dt : datetime.datetime object, default now.
        dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
        from:  http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python
        """
        round_to = date_delta.total_seconds()
        if dt is None:
            dt = datetime.now()
        seconds = (dt - dt.min).seconds

        if to == 'up':
            # // is a floor division, not a comment on following line (like in javascript):
            rounding = (seconds + round_to) // round_to * round_to
        elif to == 'down':
            rounding = seconds // round_to * round_to
        else:
            rounding = (seconds + round_to / 2) // round_to * round_to
        
        return dt + timedelta(0, rounding - seconds, -int(dt.microsecond) )
    
    def getBars(self, number=None):
        return self.bars[-number:]
        
    def getCurrentBar(self):
        return self.bars.current_bar
        
    def getLastBar(self):
        return self.bars.getLastBar()
    
    def getSize(self):
        return (len(self.bars.bars))
        
    def getInstrument(self):
        return (self.bars.bars[0].instrument)

