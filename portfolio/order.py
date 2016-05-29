from decimal import Decimal


class Order(object):

    def __init__(self, id, tick, order_type, currency_pair):
        self.id = id
        self.currency_pair = curreny_pair
        self.open_bid = tick.bid
        self.open_ask = tick.ask
        self.open_spread = tick.spread
        self.order_type
