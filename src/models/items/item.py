
__author__ = 'Timur'

import requests
from bs4 import BeautifulSoup
import re
from src.common.database import Database
import src.models.items.contants as ItemConstants

class Item(object):
    def __init__(self, name, url, store):
        self.name = name
        self.url = url
        self.store = store # store where the item lives

        # price won't be a passing parameter anymore, it will be a query
        # we access python properties instead having to raise methods
        tag_name = store.tag_name
        query = store.query
        # the query result, a string price, will be stored to self.price
        self.price = self.load_price(tag_name, query)

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self, tag_name, query):
        #Amazon: <span id="priceblock_dealprice" class="a-size-medium a-color-price">£699.00</span>
        request = requests.get(self.url)
        content = request.content # get the content
        soup = BeautifulSoup(content, "html.parser") # parse the HTML
        # find the element
        # i.e. tag_name = "span", id ={"priceblock_dealprice"}
        element = soup.find(tag_name, query)
        string_price = element.text.strip() # remove white spaces in text

        pattern = re.compile("(\d+.\d+)") #regular expression for dollar and cents
        # if the amount has two amounts such as $100.22 $89.99
        # the above pattern would only identify the first amount, not the second one
        match = pattern.search(string_price)
        # this will appoint the first amount and return the string_price
        return match.group()

    def save_to_mongo(self):
        # Insert JSON representation
        Database.insert(collection=ItemConstants.COLLECTION,
                        data=self.json())

    @classmethod
    def from_mongo(cls, name):
        # Search collection
        item_data = Database.find_one(collection=ItemConstants.COLLECTION,
                                      query={'name':name})
        # use Argument unpacking to return python dictionary
        return cls(**item_data)

    def json(self):
        return {
            "name": self.name,
            "url" : self.url
        }




