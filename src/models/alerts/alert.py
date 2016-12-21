__author__ = 'Timur'

class Alert(object):
    def __init__(self, user, price_limit, item):
        self.user = user
        self.price_limit = price_limit
        self.item = item

    # define what they look like, how they are being printed
    # out using print function; their string representation
    def __repr__(self):
        return "<Alert for {} on item {} with price {}.>".format(self.user.email, self.item.name, self.price_limit)


