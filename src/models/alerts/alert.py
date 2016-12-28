__author__ = 'Timur'

import uuid

class Alert(object):
    def __init__(self, user, price_limit, item, _id=None):
        self.user = user
        self.price_limit = price_limit
        self.item = item
        self._id = uuid.uuid4().hex if _id is None else _id

    # define what they look like, how they are being printed
    # out using print function; their string representation
    def __repr__(self):
        return "<Alert for {} on item {} with price {}.>".format(self.user.email, self.item.name, self.price_limit)


