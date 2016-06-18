from decimal import Decimal, ROUND_HALF_DOWN
from collections import deque
import itertools
from statsmodels.tsa.arima_model import ARIMA

class Arima(object):

    def __init__(self, bars, period, shift=0, alpha=0, price_type="close"):
        self.bars = bars
        self.period = period
        self.shift=shift
        self.alpha = alpha
        self.price_type=price_type
        self.value = self.getValue(bars, period, shift, alpha, price_type)
        
windowLength = 500
    
    def getReturns(self, bars):
        spReturns[0] = 0;
        spReturns = diff(log(close_price))
spReturns[as.character(head(index(close_price),1))] = 0
        
    def getOrder(self, bars):
        spReturns = diff(log(close_price))
spReturns[as.character(head(index(close_price),1))] = 0

windowLength = 500
foreLength = length(spReturns) - windowLength
forecasts <- vector(mode="character", length = foreLength)

for (d in 0:foreLength) {
  spReturnsOffset = spReturns[(1+d):(windowLength+d)]
  final.aic <- Inf
  final.order <- c(0,0,0)
  for (p in 0:5) for (q in 0:5) {
    if (p == 0 && q == 0) {
      next
    }
    arimaFit = tryCatch(
      arima(spReturnsOffset,
        order=c(p, 0, q)
      ),
      error=function( err ) FALSE,
      warning=function( err ) FALSE
    )
  
    if( !is.logical( arimaFit ) ) {
      current.aic <- AIC(arimaFit)
      if (current.aic < final.aic) {
        final.aic <- current.aic
        final.order <- c(p, 0, q)
        final.arima <- arima(spReturnsOffset, order=final.order)
      }
    } else {
      next
    }
  }
  spec = ugarchspec(
    variance.model=list(garchOrder=c(1,1)),
    mean.model=list(armaOrder=c(final.order[1], final.order[3]), include.mean=T),
    distribution.model="sged"
  )
  fit = tryCatch(
    ugarchfit(
      spec, spReturnsOffset, solver = 'hybrid'
    ),
    error=function(e) e, warning=function(w) w
  )
  if(is(fit, "warning")) {
    forecasts[d+1] = paste(index(spReturnsOffset[windowLength]), 1, sep=",")
    print(paste(index(spReturnsOffset[windowLength]), 1, sep=","))
  } else {
    fore = ugarchforecast(fit, n.ahead=1)
    ind = fore@forecast$seriesFor
    forecasts[d+1] = paste(colnames(ind), ifelse(ind[1] < 0, -1, 1), sep=",")
    print(paste(colnames(ind), ifelse(ind[1] < 0, -1, 1), sep=",")) 
  }
}
        
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
