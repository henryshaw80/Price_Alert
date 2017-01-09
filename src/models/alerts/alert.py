__author__ = 'Timur'

import uuid
import _datetime
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item

class Alert(object):
    def __init__(self, user_email, price_limit, item_id, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = _datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    # define what they look like, how they are being printed
    # out using print function; their string representation
    # self.item.name : python object data
    # self.item['name'] : python dictionary data
    def __repr__(self):
        return "<Alert for {} on item {} with price {}.>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price limit reached for {}".format(self.item.name),
                "text": "we've found a deal! {}".format(self.item.url)
            }
        )

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        # current time minus 10 minutes
        last_updated_limit = _datetime.datetime.utcnow() - _datetime.timedelta(minutes=minutes_since_update)

        # if last_checked is less than equal to 10 minutes ago, return object of type Alert for each of the element
        # in mongodb cursor, which is reading from AlertConstants.COLLECTION
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"last_checked": {"$lte": last_updated_limit}})]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        # since we cannot save Python object (i.e. item and user) into mongodb
        # we will save user.json and item.json for each alert
        # However, this would duplicates the data since we already saved
        # user.json() and item.json() in mongodb
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = _datetime.datetime.utcnow() # to update last_checked to now
        self.save_to_mongo() # we are saving last_checked to mongodb
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in
                Database.find(AlertConstants.COLLECTION,
                              {'user_email': user_email})]
