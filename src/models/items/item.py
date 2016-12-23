__author__ = 'Timur'

import requests
from bs4 import BeautifulSoup
import re

class Item(object):
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_item(self, tag_name, query):
        request = requests.get(self.url)
        content = request.content # get the content
        soup = BeautifulSoup(content, "html.parser") # parse the HTML
        # find the element
        # i.e. tag_name = "span", id ={"priceblock_ourprice"}
        element = soup.find(tag_name, query)
        string_price = element.text.strip() # remove white spaces in text

        pattern = re.compile("(\d+.\d+)") #regular expression for dollar and cents
        # if the amount has two amounts such as $100.22 $89.99
        # the above pattern would only identify the first amount, not the second one
        match = pattern.search(string_price)
        # this will appoint the first amount and assign it to self.price
        self.price = match.group()





