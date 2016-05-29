from qsforex.event.event import Event
from collections import deque

class Bars(object):
    def __init__(self, size, instrument=''):
        self.size = size
        self.instrument = instrument
        bars=[]
        self.bars = deque([])
        self.index = 0

    def newBar(self, time, tick):
        if self.index > 0:
            self.bars[self.index-1].state = 'closed'
            
        if not len(self.bars) < self.size:
             self.removeBar()
        
        self.index += 1
        self.current_bar = Bar(time, tick, self.index)     
        self.bars.append(self.current_bar)

    def removeBar(self):
        self.bars.popleft()
        self.index -=1

    def addToOpenBar(self, time, tick):
        self.current_bar.addTick(tick)
    
    def getLastBar(self):
        return self.bars[len(self.bars)-1]

    def __repr__(self):
        return self.bars

class Bar(object):

    def __init__(self, time, tick, index):
        self.type = 'BAR'
        self.index = index
        self.instrument = tick.instrument
        self.time = time
        init_value = (tick.bid+tick.ask)/2
        self.open = init_value
        self.close = init_value
        self.high = init_value
        self.low = init_value
        self.state = 'open'

    def addTick(self, tick):
        value = (tick.bid+tick.ask)/2
        self.close = value
        self.high = max(self.high, self.open, self.close, value)
        self.low = min(self.low, self.open, self.close, value)

    def __str__(self):
        return "Type: %s, Instrument: %s, Time: %s, Open: %s, Close: %s, High: %s, Low: %s" % (
            str(self.type), str(self.instrument), 
            str(self.time), str(self.open), str(self.close), str(self.high), str(self.low)
        )

    def __repr__(self):
        return str(self)
