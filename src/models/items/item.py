__author__ = 'Timur'

import requests
from bs4 import BeautifulSoup
import re
from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store
import uuid

class Item(object):
    def __init__(self, url, name=None, price=None, _id=None):

        self.url = url
        store = Store.find_by_url(url) # store where the item lives

        # price won't be a passing parameter anymore, it will be a query
        # we access python properties instead having to raise methods
        self.tag_name = store.tag_name

        # e.g. Item("Wool Blend Peacoat",
        # "http://www.johnlewis.com/kin-by-john-lewis-wool-blend-peacoat-navy/p3033177",
        # Store("John Lewis",
        #       "http://www.johnlewis.com/",
        #       "span",
        #       {"itemprop":"price","class":"now-price"}))
        self.pricequery = store.pricequery

        # the query result, a string price, will be stored to self.price
        # initially it will be None, subsequently it will download price from database
        self.price = None if price is None else price

        # when an Item is created, it won't automatically load price or name
        # one need to call the method to web scrape price and name

        # e.g. Item("Wool Blend Peacoat",
        # "http://www.johnlewis.com/kin-by-john-lewis-wool-blend-peacoat-navy/p3033177",
        # Store("John Lewis",
        #       "http://www.johnlewis.com/",
        #       "span",
        #       {"itemprop":"name"}))
        self.namequery = store.namequery
        # the query result, a string price, will be stored to self.price
        self.name = self.load_name() if name is None else name

        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        #<span itemprop="price" class="now-price">£145.00</span>
        request = requests.get(self.url)
        content = request.content # get the content
        soup = BeautifulSoup(content, "html.parser") # parse the HTML
        # find the element
        # i.e. tag_name = "span", id ={"priceblock_dealprice"}
        element = soup.find(self.tag_name, self.pricequery)
        string_price = element.text.strip() # remove white spaces in text

        pattern = re.compile("(\d+.\d+)") #regular expression for dollar and cents
        # if the amount has two amounts such as $100.22 $89.99
        # the above pattern would only identify the first amount, not the second one
        match = pattern.search(string_price)
        # match.group() will appoint the first amount and return the string_price
        # we appoint self.price whenever we load price
        self.price = float(match.group())

        return self.price

    def load_name(self):
        #<span itemprop="name">Kin by John Lewis Wool Blend Peacoat, Navy</span>
        request = requests.get(self.url)
        content = request.content # get the content
        soup = BeautifulSoup(content, "html.parser") # parse the HTML
        # find the element
        # i.e. tag_name = "span", id ={"name"}
        element = soup.find(self.tag_name, self.namequery)
        # No need regex at all (one can get the text of an element by doing element.text).
        return element.text

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(collection=ItemConstants.COLLECTION,
                                       query={"_id": item_id}))

    def save_to_mongo(self):
        # Insert JSON representation
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, data=self.json())

    @classmethod
    def from_mongo(cls, name):
        # Search collection
        item_data = Database.find_one(collection=ItemConstants.COLLECTION,
                                      query={'name':name})
        # use Argument unpacking to return python dictionary
        return cls(**item_data)

    def json(self):
        return {
            "url" : self.url,
            "name": self.name,
            "_id" : self._id,
            "price": self.price
        }




